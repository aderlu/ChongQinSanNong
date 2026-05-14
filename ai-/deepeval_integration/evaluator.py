from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Tuple

from .config import MetricDefinition, build_metric_definitions, load_project_config
from .llm import NonlinearOpenAIDeepEvalLLM

try:
    from chicken_data_synthesis.infrastructure.knowledge import (
        build_llm_wiki_context,
        build_wiki_audit_metadata,
        resolve_llm_wiki_dir,
    )
except ImportError:  # pragma: no cover - optional when used outside the main project package
    build_llm_wiki_context = None
    build_wiki_audit_metadata = None
    resolve_llm_wiki_dir = None

try:
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, LLMTestCaseParams
except ImportError as exc:  # pragma: no cover - runtime dependency guard
    raise ImportError(
        "deepeval 未安装。请先执行 `pip install -r requirements.txt`。"
    ) from exc


@dataclass
class MetricScore:
    key: str
    display_name: str
    score: float
    max_score: int
    reason: str


def _normalize_metric_score(raw_score: Any, max_score: int) -> float:
    try:
        value = float(raw_score)
    except (TypeError, ValueError):
        return 0.0

    if value <= 1.0:
        scaled = value * max_score
    elif value <= 10.0:
        scaled = (value / 10.0) * max_score
    else:
        scaled = value

    return round(max(0.0, min(float(max_score), scaled)), 2)


def _stringify_case(case_data: Dict[str, Any]) -> str:
    payload = {
        "species": case_data.get("species", "鸡"),
        "diagnosis": case_data.get("diagnosis", ""),
        "prescription": case_data.get("prescription", ""),
        "withdrawal_period": case_data.get("withdrawal_period", ""),
        "metadata": case_data.get("metadata", {}),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _build_test_case(case_data: Dict[str, Any], *, knowledge_context: str = "") -> LLMTestCase:
    context_items = [knowledge_context] if knowledge_context else None
    return LLMTestCase(
        input=case_data.get("user_query", ""),
        actual_output=_stringify_case(case_data),
        context=context_items,
        retrieval_context=context_items,
        additional_metadata={
            "metadata": case_data.get("metadata", {}),
            "llm_wiki_context_attached": bool(knowledge_context),
        },
    )


def _build_wiki_query(case_data: Dict[str, Any]) -> str:
    metadata = case_data.get("metadata") or {}
    disease_name = str(metadata.get("disease_name", "") or "") if isinstance(metadata, dict) else ""
    return "\n".join(
        value
        for value in [
            disease_name,
            str(case_data.get("user_query", "") or ""),
            str(case_data.get("diagnosis", "") or ""),
            str(case_data.get("prescription", "") or ""),
            str(case_data.get("withdrawal_period", "") or ""),
            json.dumps(metadata, ensure_ascii=False),
        ]
        if value.strip()
    )


def _build_deepeval_wiki_context(case_data: Dict[str, Any], project_config: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    if build_llm_wiki_context is None or resolve_llm_wiki_dir is None or build_wiki_audit_metadata is None:
        return "", {}

    query = _build_wiki_query(case_data)
    if not query.strip():
        return "", {}

    try:
        wiki_dir = resolve_llm_wiki_dir(project_config, Path.cwd())
        context = build_llm_wiki_context(query, wiki_dir=wiki_dir, top_k_pages=6, top_k_facts=10)
        audit = build_wiki_audit_metadata(wiki_dir=wiki_dir, knowledge_context=context, query=query)
    except Exception:
        return "", {}
    return context, audit


def _summarize_strengths(scores: Iterable[MetricScore]) -> Tuple[str, str]:
    ordered = sorted(scores, key=lambda item: item.score, reverse=True)
    if not ordered:
        return "", ""
    top = ordered[0].display_name
    bottom = ordered[-1].display_name
    return top[:12], bottom[:12]


def _detect_structured_pass(case_data: Dict[str, Any]) -> bool:
    metadata = case_data.get("metadata") or {}
    required = [
        case_data.get("user_query"),
        case_data.get("diagnosis"),
        case_data.get("prescription"),
        case_data.get("withdrawal_period"),
        metadata.get("disease_name"),
        metadata.get("severity"),
    ]
    return all(bool(str(item).strip()) for item in required)


def _detect_fatal_risk(case_data: Dict[str, Any], metric_scores: List[MetricScore]) -> bool:
    safety = next((item for item in metric_scores if item.key == "prescription_safety"), None)
    if safety is None:
        return False

    reason = safety.reason.lower()
    withdrawal_period = str(case_data.get("withdrawal_period", "")).strip()
    # Only treat explicit safety red flags as fatal. Generic words like "严重" or
    # "unsafe" are too broad in judge rationales and caused false positives.
    keyword_hit = any(
        word in reason
        for word in [
            "禁药",
            "违禁",
            "氯霉素",
            "孔雀石绿",
            "休药期缺失",
            "休药期错误",
            "停药期缺失",
            "停药期错误",
            "剂量错误",
            "剂量过量",
            "严重过量",
            "forbidden drug",
            "prohibited drug",
            "overdose",
            "wrong dosage",
            "missing withdrawal period",
            "invalid withdrawal period",
        ]
    )

    if not withdrawal_period:
        return True
    if safety.score < (safety.max_score * 0.25):
        return True
    if keyword_hit and safety.score < (safety.max_score * 0.6):
        return True
    return False


def _build_final_label(total_score: float, fatal_risk: bool) -> str:
    if fatal_risk:
        return "review"
    return "pass" if total_score >= 80 else "review"


class ChickenCaseDeepEvalEvaluator:
    """Standardized DeepEval wrapper for the project's four scoring dimensions."""

    def __init__(self, judge_config: Dict[str, Any], project_config: Dict[str, Any] | None = None) -> None:
        self.project_config = project_config or load_project_config()
        self.metric_definitions = build_metric_definitions(self.project_config)
        self.model = NonlinearOpenAIDeepEvalLLM(
            base_url=self.project_config["api"]["base_url"],
            model_config=judge_config,
        )
        self.judge_config = dict(judge_config)

    def _build_metric(self, definition: MetricDefinition) -> GEval:
        return GEval(
            name=definition.key,
            criteria=definition.criteria,
            evaluation_steps=definition.evaluation_steps,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.CONTEXT,
                LLMTestCaseParams.RETRIEVAL_CONTEXT,
            ],
            model=self.model,
        )

    def evaluate(self, case_data: Dict[str, Any], judge_label: str = "") -> Dict[str, Any]:
        knowledge_context, wiki_audit = _build_deepeval_wiki_context(case_data, self.project_config)
        test_case = _build_test_case(case_data, knowledge_context=knowledge_context)
        metric_scores: List[MetricScore] = []
        metric_reasons: Dict[str, str] = {}

        for definition in self.metric_definitions:
            metric = self._build_metric(definition)
            metric.measure(test_case)
            normalized_score = _normalize_metric_score(metric.score, definition.max_score)
            reason = (metric.reason or "").strip()
            metric_scores.append(
                MetricScore(
                    key=definition.key,
                    display_name=definition.display_name,
                    score=normalized_score,
                    max_score=definition.max_score,
                    reason=reason,
                )
            )
            metric_reasons[definition.key] = reason

        strengths, weaknesses = _summarize_strengths(metric_scores)
        total_score = round(sum(item.score for item in metric_scores), 2)
        structured_pass = _detect_structured_pass(case_data)
        fatal_risk = _detect_fatal_risk(case_data, metric_scores)
        final_label = _build_final_label(total_score, fatal_risk)
        avg_reason_score = round(mean(item.score for item in metric_scores), 2) if metric_scores else 0.0

        output = {
            "judge_label": judge_label,
            "judge_model": self.judge_config["name"],
            "diagnosis_accuracy": 0.0,
            "pathology_logic": 0.0,
            "prescription_safety": 0.0,
            "data_quality": 0.0,
            "total_score": total_score,
            "fatal_risk": fatal_risk,
            "structured_pass": structured_pass,
            "summary": ("整体较好" if total_score >= 85 else "需要复核")[:12],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "final_label": final_label,
            "metric_reasoning": metric_reasons,
            "avg_metric_score": avg_reason_score,
            "llm_wiki_context": knowledge_context,
            "wiki_audit": wiki_audit,
        }

        for item in metric_scores:
            output[item.key] = item.score

        return output


def evaluate_case_with_deepeval(
    case_data: Dict[str, Any],
    judge_config: Dict[str, Any],
    judge_label: str = "",
    project_config: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    evaluator = ChickenCaseDeepEvalEvaluator(judge_config=judge_config, project_config=project_config)
    return evaluator.evaluate(case_data=case_data, judge_label=judge_label)
