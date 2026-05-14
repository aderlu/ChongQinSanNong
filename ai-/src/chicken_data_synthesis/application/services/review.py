from __future__ import annotations

import copy
import time
from typing import Any, Dict, Mapping, Sequence

from chicken_data_synthesis.infrastructure.evaluation import (
    evaluate_case_with_deepeval_adapter,
    normalize_judge_payload,
    normalize_score as normalize_component_score,
    normalize_total_score as normalize_component_total_score,
)
from chicken_data_synthesis.infrastructure.rules import evaluate_rule_base

JudgeResult = Dict[str, Any]
TimedJudgeResult = tuple[JudgeResult | None, float]


def normalize_score(value: Any, scale: float) -> float:
    """Normalize a component score to the requested scale."""

    return normalize_component_score(value, scale, allow_ratio_scale=True)


def normalize_total_score(value: Any) -> float:
    """Normalize either 0-1 or 0-100 total score inputs."""

    return normalize_component_total_score(value, allow_ratio_scale=True)


def normalize_judge_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize judge outputs into the shape used by the legacy pipeline.

    The normalization happens in-place to keep the service interface aligned
    with the legacy main script during migration.
    """

    normalized = normalize_judge_payload(
        result,
        allow_ratio_scale=True,
        summary_max_length=60,
        strengths_max_length=60,
        weaknesses_max_length=60,
    )
    result.update(normalized)
    return result


def compute_score_difference(judge_a_result: Dict[str, Any], judge_b_result: Dict[str, Any]) -> float:
    """Return the absolute total-score gap between two normalized judge results."""

    return abs(
        normalize_total_score(judge_a_result.get("total_score", 0))
        - normalize_total_score(judge_b_result.get("total_score", 0))
    )


def resolve_evaluation_mode(
    run_mode: str,
    cli_mode: str,
    evaluation_config: Mapping[str, Any],
) -> str:
    """Resolve effective evaluation mode using CLI override then config defaults."""

    if cli_mode and cli_mode != "auto":
        return str(cli_mode)

    mode_by_run = evaluation_config.get("mode_by_run", {})
    if isinstance(mode_by_run, Mapping):
        selected = str(mode_by_run.get(run_mode, "")).strip().lower()
        if selected in {"legacy", "deepeval"}:
            return selected

    default_mode = str(evaluation_config.get("default_mode", "legacy")).strip().lower()
    return default_mode if default_mode in {"legacy", "deepeval"} else "legacy"


def build_model_fallback_chain(
    primary_config: Mapping[str, Any],
    candidate_models: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Build a de-duplicated fallback chain from primary config plus candidate references."""

    chain: list[dict[str, Any]] = [copy.deepcopy(dict(primary_config))]
    seen_names = {str(primary_config.get("name", "")).strip()}
    for candidate_key in primary_config.get("fallback_candidates", []) or []:
        candidate = candidate_models.get(str(candidate_key).strip())
        if not candidate:
            continue
        candidate_name = str(candidate.get("name", "")).strip()
        if not candidate_name or candidate_name in seen_names:
            continue
        chain.append(copy.deepcopy(dict(candidate)))
        seen_names.add(candidate_name)
    return chain


def evaluate_rule_base_case(case_data: Dict[str, Any], rule_base_config: Dict[str, Any]) -> Dict[str, Any]:
    """Application-level entry for guard-layer evaluation."""

    return evaluate_rule_base(case_data, rule_base_config)


def evaluate_deepeval_case(
    case_data: Dict[str, Any],
    judge_config: Dict[str, Any],
    judge_label: str,
    project_config: Dict[str, Any],
) -> Dict[str, Any]:
    """Application-level entry for DeepEval-based review."""

    return evaluate_case_with_deepeval_adapter(
        case_data=case_data,
        judge_config=judge_config,
        judge_label=judge_label,
        project_config=project_config,
    )


def evaluate_case_with_mode(
    case_data: Dict[str, Any],
    judge_label: str,
    judge_config: Dict[str, Any],
    *,
    evaluation_mode: str,
    project_config: Dict[str, Any],
    legacy_evaluator,
) -> TimedJudgeResult:
    """Evaluate one case with the requested mode and legacy fallback semantics."""

    if evaluation_mode == "legacy":
        return legacy_evaluator(case_data, judge_label, judge_config)

    started_at = time.perf_counter()
    try:
        result = evaluate_deepeval_case(
            case_data=case_data,
            judge_config=judge_config,
            judge_label=judge_label,
            project_config=project_config,
        )
        result = normalize_judge_result(result)
        result.setdefault("judge_label", judge_label)
        result.setdefault("judge_model", judge_config["name"])
        return result, time.perf_counter() - started_at
    except Exception:
        return legacy_evaluator(case_data, judge_label, judge_config)


def evaluate_case_with_fallbacks(
    case_data: Dict[str, Any],
    judge_label: str,
    primary_config: Mapping[str, Any],
    *,
    candidate_models: Mapping[str, Mapping[str, Any]],
    evaluation_mode: str,
    project_config: Dict[str, Any],
    legacy_evaluator,
) -> TimedJudgeResult:
    """Evaluate a case across the configured fallback chain."""

    total_elapsed = 0.0
    for attempt_index, config in enumerate(build_model_fallback_chain(primary_config, candidate_models), start=1):
        result, elapsed = evaluate_case_with_mode(
            case_data,
            judge_label,
            config,
            evaluation_mode=evaluation_mode,
            project_config=project_config,
            legacy_evaluator=legacy_evaluator,
        )
        total_elapsed += elapsed
        if result is not None:
            if attempt_index > 1:
                result["fallback_used"] = True
                result["fallback_attempt"] = attempt_index
                result["judge_model"] = config["name"]
            return result, total_elapsed
    return None, total_elapsed
