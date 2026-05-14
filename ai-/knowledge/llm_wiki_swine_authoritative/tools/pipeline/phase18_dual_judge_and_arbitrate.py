from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from wiki_first_judge_prompts import (  # noqa: E402
    ARBITER_OUTPUT_FIELDS,
    ARBITRATION_SCORE_GAP,
    ARBITER_DIMENSIONS,
    HIGH_RISK_CLASSES,
    HIGH_RISK_LAYERS,
    JUDGE_A_DIMENSIONS,
    JUDGE_B_DIMENSIONS,
    JUDGE_COMMON_OUTPUT_FIELDS,
    PASS_THRESHOLD,
    REVIEW_THRESHOLD,
    SCORECARD_VERSION,
    build_arbiter_input,
    build_judge_a_input,
    build_judge_b_input,
)


TZ = timezone(timedelta(hours=8))
LOW_RISK_EXECUTIVE_CONTEXT_LAYERS = {"L1_retrieval_grounded", "L2_diagnosis_support", "L3_differential_support", "L4_control_boundary"}
NEGATIVE_BOUNDARY_CUE_RE = re.compile(
    r"(?i)\b(do not|does not|cannot|not enough|not provide|not infer|not add|not authorize|without anchored|"
    r"unsupported|uncited|beyond the cited|boundary|only supports|insufficient|avoid)\b|"
    r"(\u4e0d\u5f97|\u4e0d\u80fd|\u4e0d\u5e94|\u4e0d\u53ef|\u672a\u63d0\u4f9b|\u4e0d\u63d0\u4f9b|"
    r"\u4e0d\u751f\u6210|\u4e0d\u76f4\u63a5|\u65e0\u6cd5\u636e\u6b64|\u4e0d\u8db3\u4ee5|\u4e0d\u5b9c|"
    r"\u4e0d\u63a8\u65ad|\u4e0d\u6dfb\u52a0|\u4e0d\u6269\u5c55|\u4e0d\u5f97\u57fa\u4e8e|"
    r"\u8fb9\u754c|\u4ec5\u652f\u6301|\u4e0d\u652f\u6301|\u672a\u7ecf\u5f15\u7528|\u672a\u7ecf\u8bc1\u5b9e|"
    r"\u8d85\u51fa|\u7f3a\u4e4f)"
)
BOUNDARY_REFUSAL_RE = re.compile(
    r"(?i)\b(must not|cannot|should not|refuse|not provide|do not provide|cannot directly provide)\b|"
    r"(\u4e0d\u5f97|\u4e0d\u80fd|\u4e0d\u5e94|\u62d2\u7edd|\u4e0d\u63d0\u4f9b|\u4e0d\u751f\u6210|\u4e0d\u80fd\u76f4\u63a5)"
)
EXECUTIVE_TRIGGER_RE = re.compile(
    r"(?i)\b(dose|dosage|mg/kg|ml/kg|mrl|withdrawal|residue|regulatory|movement|report|cull|"
    r"quarantine|seal|disinfection|food safety|public health)\b|"
    r"(\u5242\u91cf|\u7528\u91cf|\u7597\u7a0b|\u7ed9\u836f|\u6ce8\u5c04|\u62cc\u6599|\u996e\u6c34|"
    r"\u4f11\u836f|\u505c\u836f|\u6b8b\u7559|\u8c03\u8fd0|\u4e0a\u62a5|\u6251\u6740|\u5c01\u9501|"
    r"\u68c0\u75ab|\u65e0\u5bb3\u5316|\u98df\u54c1\u5b89\u5168|\u516c\u5171\u536b\u751f|\u4eba\u755c\u5171\u60a3)"
)
MOJIBAKE_RE = re.compile(r"[\uFFFD]|Ã|â")


def today() -> str:
    return datetime.now(TZ).strftime("%Y%m%d")


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
    return rows


def ensure_recent_nonempty_jsonl(path: Path, *, max_age_seconds: int = 300) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Required upstream file is missing: {path}")
    rows = read_jsonl(path)
    if not rows:
        raise RuntimeError(f"Required upstream file is empty or unreadable: {path}")
    age_seconds = (datetime.now(TZ) - datetime.fromtimestamp(path.stat().st_mtime, TZ)).total_seconds()
    if age_seconds > max_age_seconds:
        raise RuntimeError(
            f"Upstream file looks stale ({age_seconds:.1f}s old > {max_age_seconds}s): {path}. "
            "Re-run the previous phase before continuing."
        )
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def latest_jsonl(directory: Path, prefix: str) -> Path:
    files = sorted(directory.glob(f"{prefix}_*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {directory}")
    return files[0]


def resolve_path(value: str, root: Path, default_dir: Path, prefix: str) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    return latest_jsonl(default_dir, prefix)


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def round2(value: float) -> float:
    return round(float(value), 2)


def weighted_total(dimension_scores: Mapping[str, Any], dimension_weights: Mapping[str, Any]) -> float:
    # Scores are stored on the same point budget as their weights, so the
    # weighted total is the sum of earned points across all dimensions.
    total = 0.0
    for key in dimension_weights:
        total += float(dimension_scores.get(key, 0.0) or 0.0)
    return round2(total)


def anchors_for(sample: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [anchor for anchor in sample.get("evidence_anchors", []) if isinstance(anchor, dict)]


def answer_for(sample: Mapping[str, Any]) -> str:
    stage_2 = sample.get("stage_2_grounded")
    if isinstance(stage_2, Mapping):
        return str(stage_2.get("answer") or "")
    return ""


def is_high_risk(sample: Mapping[str, Any]) -> bool:
    ability_layer = str(sample.get("ability_layer") or "")
    risk_class = str(sample.get("risk_class") or "")
    hard_gate = sample.get("hard_gate_check") or {}
    return bool(hard_gate.get("high_risk")) or ability_layer in HIGH_RISK_LAYERS or risk_class in HIGH_RISK_CLASSES


def needs_boundary_language(sample: Mapping[str, Any]) -> bool:
    ability_layer = str(sample.get("ability_layer") or "")
    expected_output_type = str(sample.get("expected_output_type") or "").lower()
    hard_gate = sample.get("hard_gate_check") or {}
    question_and_answer = f"{sample.get('question', '')}\n{answer_for(sample)}"
    explicit_refusal_output = expected_output_type in {
        "boundary_or_refusal",
        "drug_boundary_negative",
        "regulatory_guardrail",
    }
    return (
        ability_layer in HIGH_RISK_LAYERS
        or explicit_refusal_output
        or "refusal" in expected_output_type
        or bool(hard_gate.get("positive_triggered"))
        or executive_triggered_positive_context(sample, bool(EXECUTIVE_TRIGGER_RE.search(question_and_answer)))
    )


def executive_triggered_positive_context(sample: Mapping[str, Any], triggered: bool) -> bool:
    if not triggered:
        return False
    hard_gate = sample.get("hard_gate_check") or {}
    if "positive_triggered" in hard_gate:
        return bool(hard_gate.get("positive_triggered"))
    ability_layer = str(sample.get("ability_layer") or "")
    risk_class = str(sample.get("risk_class") or "")
    if risk_class in HIGH_RISK_CLASSES or ability_layer in HIGH_RISK_LAYERS:
        return True
    if ability_layer not in LOW_RISK_EXECUTIVE_CONTEXT_LAYERS:
        return True
    text = f"{sample.get('question', '')}\n{answer_for(sample)}"
    return not bool(NEGATIVE_BOUNDARY_CUE_RE.search(text))


def has_a0_or_label_source(sample: Mapping[str, Any]) -> bool:
    hard_gate = sample.get("hard_gate_check") or {}
    if hard_gate.get("has_a0_or_label_source"):
        return True
    if str(sample.get("authority_level") or "").upper() == "A0":
        return True
    for anchor in anchors_for(sample):
        source_id = str(anchor.get("source_id") or "").upper()
        rule_id = str(anchor.get("rule_card_id") or "").upper()
        if source_id.startswith("A0") or rule_id.startswith(("RC-DRUG", "RC-WITHDRAWAL", "RC-DISEASE")):
            return True
    return False


def phase15_warning_codes(sample: Mapping[str, Any]) -> list[str]:
    codes: list[str] = []
    hard_gate = sample.get("hard_gate_check") or {}
    if hard_gate.get("high_risk"):
        codes.append("phase15_high_risk_context")
    if hard_gate.get("positive_triggered"):
        codes.append("phase15_executive_trigger")
    elif hard_gate.get("triggered"):
        codes.append("phase15_negative_boundary_trigger")
    if str(sample.get("ability_layer") or "") in HIGH_RISK_LAYERS:
        codes.append("phase15_high_risk_layer")
    if str(sample.get("risk_class") or "") in HIGH_RISK_CLASSES:
        codes.append("phase15_high_risk_class")
    return sorted(set(codes))


def build_feature_flags(sample: Mapping[str, Any]) -> dict[str, Any]:
    anchors = anchors_for(sample)
    answer = answer_for(sample)
    high_risk = is_high_risk(sample)
    boundary_present = bool(BOUNDARY_REFUSAL_RE.search(answer))
    lexical_executive_trigger = bool(EXECUTIVE_TRIGGER_RE.search(f"{sample.get('question', '')}\n{answer}"))
    executive_content = executive_triggered_positive_context(sample, lexical_executive_trigger)
    has_rule_card = any(str(anchor.get("rule_card_id") or "").strip() for anchor in anchors)
    has_fact_anchor = any(str(anchor.get("fact_id") or "").strip() for anchor in anchors)
    has_source_anchor = any(str(anchor.get("source_id") or "").strip() for anchor in anchors)
    citation_source = "source=" in answer
    citation_rule = "rule=" in answer
    citation_fact = "fact=" in answer
    citation_page = "page=" in answer
    boundary_sample = needs_boundary_language(sample)
    citation_complete = citation_source and citation_rule and (citation_fact or boundary_sample)
    unsupported_expansion = boundary_sample and executive_content and not boundary_present
    return {
        "answer_len": len(answer.strip()),
        "anchor_count": len(anchors),
        "high_risk": high_risk,
        "boundary_sample": boundary_sample,
        "boundary_present": boundary_present,
        "lexical_executive_trigger": lexical_executive_trigger,
        "executive_content": executive_content,
        "has_rule_card": has_rule_card,
        "has_fact_anchor": has_fact_anchor,
        "has_source_anchor": has_source_anchor,
        "has_a0_or_label_source": has_a0_or_label_source(sample),
        "citation_source": citation_source,
        "citation_rule": citation_rule,
        "citation_fact": citation_fact,
        "citation_page": citation_page,
        "citation_complete": citation_complete,
        "unsupported_expansion": unsupported_expansion,
        "phase15_warning_codes": phase15_warning_codes(sample),
    }


def derive_structured_pass(sample: Mapping[str, Any], flags: Mapping[str, Any]) -> bool:
    structure_passed = bool((sample.get("structure_check") or {}).get("passed"))
    fact_passed = bool((sample.get("fact_level_check") or {}).get("passed"))
    hard_gate_passed = bool((sample.get("hard_gate_check") or {}).get("passed"))
    if not (structure_passed and fact_passed and hard_gate_passed):
        return False
    if not answer_for(sample).strip():
        return False
    if int(flags.get("anchor_count", 0) or 0) <= 0:
        return False
    if flags.get("boundary_sample"):
        return bool(flags.get("boundary_present") and flags.get("has_rule_card") and flags.get("has_a0_or_label_source"))
    return bool(flags.get("citation_complete") and flags.get("has_fact_anchor") and flags.get("has_source_anchor"))


def derive_fatal_risk(sample: Mapping[str, Any], flags: Mapping[str, Any]) -> bool:
    if not bool((sample.get("hard_gate_check") or {}).get("passed")):
        return True
    if flags.get("unsupported_expansion"):
        return True
    if flags.get("high_risk") and flags.get("executive_content") and not flags.get("has_a0_or_label_source"):
        return True
    return False


def label_from_score(total_score: float, fatal_risk: bool, structured_pass: bool) -> str:
    if fatal_risk:
        return "reject"
    if total_score >= PASS_THRESHOLD and structured_pass:
        return "pass"
    if total_score >= REVIEW_THRESHOLD:
        return "review"
    return "reject"


def score_judge_a(sample: Mapping[str, Any]) -> dict[str, Any]:
    flags = build_feature_flags(sample)
    answer = answer_for(sample)
    has_reasoning_connector = any(token in answer.lower() for token in ("therefore", "because", "based on", "should")) or any(
        token in answer for token in ("\u56e0\u6b64", "\u4f9d\u636e", "\u6240\u4ee5", "\u5e94")
    )
    stage_2 = sample.get("stage_2_grounded") or {}
    removed_unsupported = len(stage_2.get("removed_unsupported_claims", [])) if isinstance(stage_2, Mapping) else 0
    boundary_rewrites = len(stage_2.get("boundary_rewrites", [])) if isinstance(stage_2, Mapping) else 0

    evidence_fidelity = 10.0
    if (sample.get("fact_level_check") or {}).get("passed"):
        evidence_fidelity += 8.0
    if (sample.get("hard_gate_check") or {}).get("passed"):
        evidence_fidelity += 6.0
    if flags["citation_complete"]:
        evidence_fidelity += 3.0
    if not flags["unsupported_expansion"]:
        evidence_fidelity += 3.0
    if flags["high_risk"] and not flags["boundary_present"]:
        evidence_fidelity -= 10.0
    evidence_fidelity = clamp(evidence_fidelity, 0.0, float(JUDGE_A_DIMENSIONS["evidence_fidelity"]))

    clinical_reasoning = 6.0
    clinical_reasoning += 5.0 if has_reasoning_connector else 1.0
    clinical_reasoning += min(4.0, float(removed_unsupported + boundary_rewrites))
    clinical_reasoning += 3.0 if flags["answer_len"] >= 80 else 1.0
    clinical_reasoning += 2.0 if not flags["unsupported_expansion"] else -4.0
    clinical_reasoning = clamp(clinical_reasoning, 0.0, float(JUDGE_A_DIMENSIONS["clinical_reasoning"]))

    safety_boundary = 6.0
    if flags["boundary_sample"]:
        safety_boundary += 8.0 if flags["boundary_present"] else -4.0
        safety_boundary += 4.0 if flags["has_a0_or_label_source"] else -6.0
    else:
        safety_boundary += 8.0 if not flags["unsupported_expansion"] else -6.0
    safety_boundary += 2.0 if flags["has_rule_card"] else -2.0
    safety_boundary = clamp(safety_boundary, 0.0, float(JUDGE_A_DIMENSIONS["safety_boundary"]))

    question_resolution = 4.0
    question_resolution += 6.0 if flags["answer_len"] >= 80 else 2.0
    question_resolution += 3.0 if has_reasoning_connector else 1.0
    question_resolution += 2.0 if not flags["unsupported_expansion"] else -2.0
    question_resolution = clamp(question_resolution, 0.0, float(JUDGE_A_DIMENSIONS["question_resolution"]))

    training_utility = 3.0
    if flags["anchor_count"] >= 3:
        training_utility += 4.0
    elif flags["anchor_count"] >= 1:
        training_utility += 2.0
    training_utility += 4.0 if flags["citation_complete"] else 1.0
    training_utility += 2.0 if derive_structured_pass(sample, flags) else -1.0
    training_utility += 2.0 if not MOJIBAKE_RE.search(answer) else -2.0
    training_utility = clamp(training_utility, 0.0, float(JUDGE_A_DIMENSIONS["training_utility"]))

    dimension_scores = {
        "evidence_fidelity": round2(evidence_fidelity),
        "clinical_reasoning": round2(clinical_reasoning),
        "safety_boundary": round2(safety_boundary),
        "question_resolution": round2(question_resolution),
        "training_utility": round2(training_utility),
    }
    total = weighted_total(dimension_scores, JUDGE_A_DIMENSIONS)
    structured_pass = derive_structured_pass(sample, flags)
    fatal_risk = derive_fatal_risk(sample, flags)
    final_label = label_from_score(total, fatal_risk, structured_pass)
    summary = "grounded_pass" if final_label == "pass" else ("fatal_boundary" if fatal_risk else "needs_review")
    strengths = "anchored_answer" if flags["citation_complete"] else "compact_answer"
    weaknesses = "boundary_gap" if flags["unsupported_expansion"] else ("citation_thin" if not structured_pass else "minor_tuning")

    result = {
        "judge_id": "judge_a",
        "judge_contract_version": "wiki_first_v1",
        "judge_input": build_judge_a_input(sample),
        "dimension_scores": dimension_scores,
        "dimension_weights": dict(JUDGE_A_DIMENSIONS),
        "dimension_reasons": {
            "evidence_fidelity": "依据 fact/source/rule/page 锚点完整性与是否越界综合判断。",
            "clinical_reasoning": "依据边界内推理、诊断支持和鉴别/控制逻辑是否成立判断。",
            "safety_boundary": "依据高风险边界表达、A0/标签来源和 rule card 覆盖判断。",
            "question_resolution": "依据是否真正回应用户问题而不是空泛复述判断。",
            "training_utility": "依据自然度、结构完整性和训练可用性判断。",
        },
        "total_score": total,
        "weighted_total_score": total,
        "scorecard_version": SCORECARD_VERSION,
        "fatal_risk": fatal_risk,
        "structured_pass": structured_pass,
        "final_label": final_label,
        "passed": final_label == "pass",
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "flags": {
            "boundary_clear": bool(flags["boundary_present"] or not flags["boundary_sample"]),
            "unsupported_expansion_free": not bool(flags["unsupported_expansion"]),
            "citations_complete": bool(flags["citation_complete"]),
            "has_a0_or_label_source": bool(flags["has_a0_or_label_source"]),
            "high_risk_sample": bool(flags["high_risk"]),
            "phase15_warning_codes": list(flags["phase15_warning_codes"]),
        },
    }
    assert set(JUDGE_COMMON_OUTPUT_FIELDS).issubset(result.keys())
    return result


def score_judge_b(sample: Mapping[str, Any]) -> dict[str, Any]:
    flags = build_feature_flags(sample)
    answer = answer_for(sample)
    sentence_like = answer.count(".") + answer.count(";") + answer.count("。") + answer.count("；")
    stage_2 = sample.get("stage_2_grounded") or {}
    removed_unsupported = len(stage_2.get("removed_unsupported_claims", [])) if isinstance(stage_2, Mapping) else 0

    risk_control = 12.0
    risk_control += 10.0 if not flags["unsupported_expansion"] else -8.0
    risk_control += 6.0 if flags["boundary_present"] or not flags["boundary_sample"] else -6.0
    risk_control += 2.0 if flags["has_a0_or_label_source"] else -4.0
    risk_control = clamp(risk_control, 0.0, float(JUDGE_B_DIMENSIONS["risk_control"]))

    unsupported_expansion_control = 8.0
    unsupported_expansion_control += 10.0 if not flags["unsupported_expansion"] else -8.0
    unsupported_expansion_control += min(5.0, float(removed_unsupported))
    unsupported_expansion_control += 2.0 if flags["citation_complete"] else -2.0
    unsupported_expansion_control = clamp(unsupported_expansion_control, 0.0, float(JUDGE_B_DIMENSIONS["unsupported_expansion_control"]))

    completeness = 3.0
    completeness += 7.0 if flags["citation_complete"] else 2.0
    completeness += 5.0 if flags["answer_len"] >= 80 else (3.0 if flags["answer_len"] >= 40 else 0.0)
    completeness += 3.0 if flags["anchor_count"] >= 2 or flags["boundary_sample"] else 1.0
    completeness = clamp(completeness, 0.0, float(JUDGE_B_DIMENSIONS["answer_completeness"]))

    citation_integrity = 4.0
    citation_integrity += 5.0 if flags["citation_source"] else 0.0
    citation_integrity += 4.0 if flags["citation_rule"] else 0.0
    citation_integrity += 3.0 if flags["citation_fact"] or flags["boundary_sample"] else 0.0
    citation_integrity += 3.0 if flags["citation_page"] else 0.0
    citation_integrity = clamp(citation_integrity, 0.0, float(JUDGE_B_DIMENSIONS["citation_integrity"]))

    language_naturalness = 6.0
    language_naturalness += 4.0 if sentence_like >= 1 else 1.0
    language_naturalness += 3.0 if not MOJIBAKE_RE.search(answer) else -5.0
    language_naturalness += 2.0 if flags["answer_len"] >= 40 else 0.0
    language_naturalness = clamp(language_naturalness, 0.0, float(JUDGE_B_DIMENSIONS["language_naturalness"]))

    dimension_scores = {
        "risk_control": round2(risk_control),
        "unsupported_expansion_control": round2(unsupported_expansion_control),
        "answer_completeness": round2(completeness),
        "citation_integrity": round2(citation_integrity),
        "language_naturalness": round2(language_naturalness),
    }
    total = weighted_total(dimension_scores, JUDGE_B_DIMENSIONS)
    structured_pass = derive_structured_pass(sample, flags)
    fatal_risk = derive_fatal_risk(sample, flags)
    final_label = label_from_score(total, fatal_risk, structured_pass)
    summary = "safe_grounded" if final_label == "pass" else ("safety_block" if fatal_risk else "quality_review")
    strengths = "boundary_control" if flags["boundary_present"] or not flags["boundary_sample"] else "anchored_core"
    weaknesses = "unsupported_risk" if flags["unsupported_expansion"] else ("format_thin" if not structured_pass else "minor_tuning")

    result = {
        "judge_id": "judge_b",
        "judge_contract_version": "wiki_first_v1",
        "judge_input": build_judge_b_input(sample),
        "dimension_scores": dimension_scores,
        "dimension_weights": dict(JUDGE_B_DIMENSIONS),
        "dimension_reasons": {
            "risk_control": "依据是否存在越权执行风险、监管/用药风险和边界缺口判断。",
            "unsupported_expansion_control": "依据是否补充未锚定事实、是否清理 unsupported claims 判断。",
            "answer_completeness": "依据在允许边界内是否完成回答任务判断。",
            "citation_integrity": "依据 source/rule/fact/page 追溯链完整性判断。",
            "language_naturalness": "依据自然度、专业度和训练文本适配度判断。",
        },
        "total_score": total,
        "weighted_total_score": total,
        "scorecard_version": SCORECARD_VERSION,
        "fatal_risk": fatal_risk,
        "structured_pass": structured_pass,
        "final_label": final_label,
        "passed": final_label == "pass",
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "flags": {
            "boundary_clear": bool(flags["boundary_present"] or not flags["boundary_sample"]),
            "unsupported_expansion_free": not bool(flags["unsupported_expansion"]),
            "citations_complete": bool(flags["citation_complete"]),
            "has_a0_or_label_source": bool(flags["has_a0_or_label_source"]),
            "high_risk_sample": bool(flags["high_risk"]),
            "phase15_warning_codes": list(flags["phase15_warning_codes"]),
        },
    }
    assert set(JUDGE_COMMON_OUTPUT_FIELDS).issubset(result.keys())
    return result


def arbitration_trigger_codes(
    sample: Mapping[str, Any],
    judge_a_result: Mapping[str, Any],
    judge_b_result: Mapping[str, Any],
) -> list[str]:
    codes: list[str] = []
    if str(judge_a_result.get("final_label") or "") != str(judge_b_result.get("final_label") or ""):
        codes.append("label_disagreement")
    score_gap = abs(float(judge_a_result.get("total_score", 0) or 0) - float(judge_b_result.get("total_score", 0) or 0))
    if score_gap >= ARBITRATION_SCORE_GAP:
        codes.append("score_gap_ge_8")
    if judge_a_result.get("fatal_risk") or judge_b_result.get("fatal_risk"):
        codes.append("judge_fatal_risk")
    if is_high_risk(sample):
        codes.append("high_risk_sample")
    codes.extend(phase15_warning_codes(sample))
    a_flags = judge_a_result.get("flags") or {}
    b_flags = judge_b_result.get("flags") or {}
    if bool(a_flags.get("unsupported_expansion_free", True)) != bool(b_flags.get("unsupported_expansion_free", True)):
        codes.append("unsupported_expansion_disagreement")
    if bool(a_flags.get("boundary_clear", True)) != bool(b_flags.get("boundary_clear", True)):
        codes.append("safety_boundary_disagreement")
    return sorted(set(codes))


def arbitrate(sample: Mapping[str, Any], judge_a_result: Mapping[str, Any], judge_b_result: Mapping[str, Any]) -> dict[str, Any]:
    trigger_codes = arbitration_trigger_codes(sample, judge_a_result, judge_b_result)
    a_total = float(judge_a_result.get("total_score", 0) or 0)
    b_total = float(judge_b_result.get("total_score", 0) or 0)
    avg_total = round2((a_total + b_total) / 2)
    conservative_total = round2(min(a_total, b_total))
    high_risk = is_high_risk(sample)
    fatal_risk = bool(judge_a_result.get("fatal_risk") or judge_b_result.get("fatal_risk"))
    structured_pass = bool(judge_a_result.get("structured_pass") and judge_b_result.get("structured_pass"))
    disagreement = "label_disagreement" in trigger_codes or "unsupported_expansion_disagreement" in trigger_codes or "safety_boundary_disagreement" in trigger_codes

    if fatal_risk:
        final_total = round2(conservative_total - 5.0)
        agreed_with_judge = "A" if a_total <= b_total else "B"
        reason = "fatal_risk_priority"
    elif high_risk or disagreement:
        final_total = conservative_total
        if a_total == b_total:
            agreed_with_judge = "blend"
        else:
            agreed_with_judge = "A" if a_total < b_total else "B"
        reason = "conservative_high_risk_merge" if high_risk else "disagreement_penalty"
    else:
        final_total = avg_total
        agreed_with_judge = "blend"
        reason = "average_consensus"

    final_total = clamp(final_total, 0.0, 100.0)
    final_label = label_from_score(final_total, fatal_risk, structured_pass)
    summary = "arbiter_pass" if final_label == "pass" else ("arbiter_reject" if final_label == "reject" else "arbiter_review")
    strengths = "conservative_merge"
    weaknesses = "fatal_priority" if fatal_risk else ("high_risk_guard" if high_risk else "minor_gap")
    dimension_scores = {
        "consensus_reliability": round2(25.0 if not disagreement else 14.0 if not fatal_risk else 6.0),
        "safety_override": round2(30.0 if not fatal_risk and (not high_risk or structured_pass) else 18.0 if high_risk else 8.0),
        "evidence_sufficiency": round2(20.0 if structured_pass else 8.0),
        "training_value": round2(15.0 if final_label == "pass" else 8.0 if final_label == "review" else 2.0),
        "calibration_consistency": round2(10.0 if reason in {"average_consensus", "conservative_high_risk_merge"} else 5.0),
    }

    result = {
        "arbiter_contract_version": "wiki_first_v1",
        "arbiter_input": build_arbiter_input(sample, judge_a_result, judge_b_result, trigger_codes),
        "trigger_codes": trigger_codes,
        "dimension_scores": dimension_scores,
        "dimension_weights": dict(ARBITER_DIMENSIONS),
        "dimension_reasons": {
            "consensus_reliability": "依据双裁判标签、分差和关键风险分歧判断。",
            "safety_override": "依据 fatal risk 和高风险场景下是否采取保守结论判断。",
            "evidence_sufficiency": "依据 structured_pass 和 citation/evidence 完整性判断。",
            "training_value": "依据最终是否适合作为训练样本判断。",
            "calibration_consistency": "依据仲裁结果与 Phase15/前置风险信号一致性判断。",
        },
        "final_total_score": round2(final_total),
        "weighted_total_score": weighted_total(dimension_scores, ARBITER_DIMENSIONS),
        "scorecard_version": SCORECARD_VERSION,
        "agreed_with_judge": agreed_with_judge,
        "final_label": final_label,
        "fatal_risk": fatal_risk,
        "structured_pass": structured_pass,
        "reason": reason,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "final_flags": {
            "boundary_clear": bool((judge_a_result.get("flags") or {}).get("boundary_clear") and (judge_b_result.get("flags") or {}).get("boundary_clear")),
            "unsupported_expansion_free": bool(
                (judge_a_result.get("flags") or {}).get("unsupported_expansion_free")
                and (judge_b_result.get("flags") or {}).get("unsupported_expansion_free")
            ),
            "citations_complete": bool((judge_a_result.get("flags") or {}).get("citations_complete") and (judge_b_result.get("flags") or {}).get("citations_complete")),
            "high_risk_sample": high_risk,
        },
        "score_breakdown": {
            "judge_a_total_score": round2(a_total),
            "judge_b_total_score": round2(b_total),
            "average_total_score": avg_total,
            "conservative_total_score": conservative_total,
        },
    }
    assert set(ARBITER_OUTPUT_FIELDS).issubset(result.keys())
    return result


def route_sample(sample: Mapping[str, Any]) -> dict[str, Any]:
    structure = sample.get("structure_check") or {}
    fact = sample.get("fact_level_check") or {}
    hard_gate = sample.get("hard_gate_check") or {}
    reject_reasons = [str(item) for item in sample.get("reject_reasons", [])]

    if not hard_gate.get("passed"):
        return {
            "should_judge": False,
            "route": "skipped_hard_gate",
            "skip_reason": "phase15_hard_gate_failed",
            "skip_codes": [f"hard_gate:{reason}" for reason in hard_gate.get("violations", [])] or reject_reasons,
            "semantic_final_decision": "rejected",
        }
    if not structure.get("passed"):
        return {
            "should_judge": False,
            "route": "skipped_phase15_structure",
            "skip_reason": "phase15_structure_failed",
            "skip_codes": [f"structure:{reason}" for reason in structure.get("missing_fields", []) + structure.get("anchor_errors", [])] or reject_reasons,
            "semantic_final_decision": "rejected",
        }
    if not fact.get("passed"):
        return {
            "should_judge": False,
            "route": "skipped_phase15_fact",
            "skip_reason": "phase15_fact_failed",
            "skip_codes": reject_reasons or ["phase15_fact_failed"],
            "semantic_final_decision": "rejected",
        }
    if not anchors_for(sample):
        return {
            "should_judge": False,
            "route": "skipped_missing_anchors",
            "skip_reason": "missing_evidence_anchors",
            "skip_codes": ["missing_evidence_anchors"],
            "semantic_final_decision": "rejected",
        }
    return {
        "should_judge": True,
        "route": "dual_judge",
        "skip_reason": "",
        "skip_codes": [],
        "semantic_final_decision": "",
    }


def merge_semantic_result(
    sample: Mapping[str, Any],
    judge_a_result: Mapping[str, Any],
    judge_b_result: Mapping[str, Any],
    arbiter_result: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], list[str]]:
    source = arbiter_result or {}
    final_total = float(source.get("final_total_score", 0) or 0)
    if not arbiter_result:
        final_total = round2((float(judge_a_result.get("total_score", 0) or 0) + float(judge_b_result.get("total_score", 0) or 0)) / 2)
    final_fatal = bool(source.get("fatal_risk")) if arbiter_result else bool(judge_a_result.get("fatal_risk") or judge_b_result.get("fatal_risk"))
    structured_pass = bool(source.get("structured_pass")) if arbiter_result else bool(
        judge_a_result.get("structured_pass") and judge_b_result.get("structured_pass")
    )
    final_label = str(source.get("final_label") or "") if arbiter_result else label_from_score(final_total, final_fatal, structured_pass)

    reasons: list[str] = []
    if final_fatal:
        reasons.append("semantic:fatal_risk_priority")
    if not structured_pass:
        reasons.append("semantic:structured_pass_false")
    if str(judge_a_result.get("final_label") or "") != "pass":
        reasons.append(f"judge_a:{judge_a_result.get('final_label', 'review')}")
    if str(judge_b_result.get("final_label") or "") != "pass":
        reasons.append(f"judge_b:{judge_b_result.get('final_label', 'review')}")
    if arbiter_result:
        reasons.extend(f"arbiter:{code}" for code in arbiter_result.get("trigger_codes", []))
        if final_label == "reject":
            reasons.append(f"arbiter:{arbiter_result.get('reason', 'reject')}")

    if final_fatal or final_label == "reject":
        semantic_final_decision = "rejected"
    elif final_label == "pass" and str(sample.get("final_decision") or "") == "accepted":
        semantic_final_decision = "accepted"
    else:
        semantic_final_decision = "review"

    metrics = {
        "final_total_score": round2(final_total),
        "final_label": final_label,
        "fatal_risk": final_fatal,
        "structured_pass": structured_pass,
        "semantic_final_decision": semantic_final_decision,
        "source": "arbiter" if arbiter_result else "judge_average",
    }
    return metrics, sorted(set(reasons))


def evaluate_samples(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evaluated: list[dict[str, Any]] = []
    for sample in samples:
        route = route_sample(sample)
        if not route["should_judge"]:
            evaluated.append(
                {
                    **sample,
                    "semantic_route": route["route"],
                    "semantic_skip_reason": route["skip_reason"],
                    "semantic_skip_codes": route["skip_codes"],
                    "phase15_warning_codes": phase15_warning_codes(sample),
                    "judge_a_result": None,
                    "judge_b_result": None,
                    "needed_arbitration": False,
                    "arbitration_trigger_codes": [],
                    "arbiter_result": None,
                    "semantic_final_metrics": {
                        "final_total_score": 0.0,
                        "final_label": "reject",
                        "fatal_risk": route["route"] == "skipped_hard_gate",
                        "structured_pass": False,
                        "semantic_final_decision": route["semantic_final_decision"],
                        "source": "phase15_gate",
                    },
                    "semantic_reject_reasons": route["skip_codes"],
                    "semantic_final_decision": route["semantic_final_decision"],
                }
            )
            continue

        judge_a_result = score_judge_a(sample)
        judge_b_result = score_judge_b(sample)
        trigger_codes = arbitration_trigger_codes(sample, judge_a_result, judge_b_result)
        arbiter_result = arbitrate(sample, judge_a_result, judge_b_result) if trigger_codes else None
        final_metrics, semantic_reasons = merge_semantic_result(sample, judge_a_result, judge_b_result, arbiter_result)
        evaluated.append(
            {
                **sample,
                "semantic_route": route["route"],
                "semantic_skip_reason": "",
                "semantic_skip_codes": [],
                "phase15_warning_codes": phase15_warning_codes(sample),
                "judge_a_result": judge_a_result,
                "judge_b_result": judge_b_result,
                "needed_arbitration": bool(trigger_codes),
                "arbitration_trigger_codes": trigger_codes,
                "arbiter_result": arbiter_result,
                "semantic_final_metrics": final_metrics,
                "semantic_reject_reasons": semantic_reasons,
                "semantic_final_decision": final_metrics["semantic_final_decision"],
            }
        )
    return evaluated


def summarize(evaluated: list[dict[str, Any]], input_path: Path, output_path: Path, root: Path) -> dict[str, Any]:
    route_counts: dict[str, int] = {}
    decision_counts: dict[str, int] = {}
    skip_reason_counts: dict[str, int] = {}
    arbitration_trigger_counts: dict[str, int] = {}
    fatal_risk_count = 0
    dual_judged = 0
    arbitration_count = 0

    for row in evaluated:
        route = str(row.get("semantic_route") or "")
        route_counts[route] = route_counts.get(route, 0) + 1
        decision = str(row.get("semantic_final_decision") or "")
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        skip_reason = str(row.get("semantic_skip_reason") or "")
        if skip_reason:
            skip_reason_counts[skip_reason] = skip_reason_counts.get(skip_reason, 0) + 1
        if route == "dual_judge":
            dual_judged += 1
        if row.get("needed_arbitration"):
            arbitration_count += 1
        for code in row.get("arbitration_trigger_codes", []):
            arbitration_trigger_counts[code] = arbitration_trigger_counts.get(code, 0) + 1
        if (row.get("semantic_final_metrics") or {}).get("fatal_risk"):
            fatal_risk_count += 1

    return {
        "generated_at": now(),
        "phase": "phase18_dual_judge_and_arbitrate",
        "mode": "wiki_first_dual_judge_v1",
        "input_evaluated": relative(input_path, root),
        "output": relative(output_path, root),
        "samples": len(evaluated),
        "dual_judged": dual_judged,
        "needed_arbitration": arbitration_count,
        "fatal_risk_count": fatal_risk_count,
        "semantic_accepted": decision_counts.get("accepted", 0),
        "semantic_review": decision_counts.get("review", 0),
        "semantic_rejected": decision_counts.get("rejected", 0),
        "route_counts": dict(sorted(route_counts.items())),
        "skip_reason_counts": dict(sorted(skip_reason_counts.items())),
        "arbitration_trigger_counts": dict(sorted(arbitration_trigger_counts.items())),
        "passed": bool(evaluated),
    }


def write_reports(
    summary: dict[str, Any],
    evaluated: list[dict[str, Any]],
    report_json: Path,
    decision_csv: Path,
    report_md: Path,
) -> None:
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    decision_csv.parent.mkdir(parents=True, exist_ok=True)
    with decision_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "sample_id",
                "phase15_final_decision",
                "semantic_route",
                "semantic_final_decision",
                "semantic_skip_reason",
                "needed_arbitration",
                "arbitration_trigger_codes",
                "semantic_final_label",
                "semantic_fatal_risk",
                "semantic_reject_reasons",
            ],
        )
        writer.writeheader()
        for row in evaluated:
            metrics = row.get("semantic_final_metrics") or {}
            writer.writerow(
                {
                    "sample_id": row.get("sample_id", ""),
                    "phase15_final_decision": row.get("final_decision", ""),
                    "semantic_route": row.get("semantic_route", ""),
                    "semantic_final_decision": row.get("semantic_final_decision", ""),
                    "semantic_skip_reason": row.get("semantic_skip_reason", ""),
                    "needed_arbitration": row.get("needed_arbitration", False),
                    "arbitration_trigger_codes": "|".join(row.get("arbitration_trigger_codes", [])),
                    "semantic_final_label": metrics.get("final_label", ""),
                    "semantic_fatal_risk": metrics.get("fatal_risk", False),
                    "semantic_reject_reasons": "|".join(row.get("semantic_reject_reasons", [])),
                }
            )

    detailed_csv = decision_csv.with_name(decision_csv.stem + "_detailed.csv")
    with detailed_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "sample_id",
                "plan_id",
                "ability_layer",
                "entity_id",
                "entity_type",
                "risk_class",
                "expected_output_type",
                "phase15_final_decision",
                "semantic_route",
                "semantic_final_decision",
                "semantic_skip_reason",
                "needed_arbitration",
                "arbitration_trigger_codes",
                "phase15_warning_codes",
                "question",
                "stage_1_answer",
                "stage_2_answer",
                "evidence_anchor_count",
                "judge_a_total_score",
                "judge_a_final_label",
                "judge_a_fatal_risk",
                "judge_a_structured_pass",
                "judge_a_evidence_fidelity",
                "judge_a_clinical_reasoning",
                "judge_a_safety_boundary",
                "judge_a_question_resolution",
                "judge_a_training_utility",
                "judge_a_summary",
                "judge_a_strengths",
                "judge_a_weaknesses",
                "judge_b_total_score",
                "judge_b_final_label",
                "judge_b_fatal_risk",
                "judge_b_structured_pass",
                "judge_b_risk_control",
                "judge_b_unsupported_expansion_control",
                "judge_b_answer_completeness",
                "judge_b_citation_integrity",
                "judge_b_language_naturalness",
                "judge_b_summary",
                "judge_b_strengths",
                "judge_b_weaknesses",
                "arbiter_final_total_score",
                "arbiter_final_label",
                "arbiter_fatal_risk",
                "arbiter_structured_pass",
                "arbiter_reason",
                "arbiter_agreed_with_judge",
                "arbiter_summary",
                "arbiter_strengths",
                "arbiter_weaknesses",
                "arbiter_boundary_clear",
                "arbiter_unsupported_expansion_free",
                "arbiter_citations_complete",
                "semantic_final_total_score",
                "semantic_final_label",
                "semantic_fatal_risk",
                "semantic_structured_pass",
                "semantic_source",
                "semantic_reject_reasons",
            ],
        )
        writer.writeheader()
        for row in evaluated:
            judge_a = row.get("judge_a_result") or {}
            judge_b = row.get("judge_b_result") or {}
            arbiter = row.get("arbiter_result") or {}
            metrics = row.get("semantic_final_metrics") or {}
            stage_1 = row.get("stage_1_draft") or {}
            stage_2 = row.get("stage_2_grounded") or {}
            judge_a_scores = judge_a.get("dimension_scores") or {}
            judge_b_scores = judge_b.get("dimension_scores") or {}
            arbiter_flags = arbiter.get("final_flags") or {}
            writer.writerow(
                {
                    "sample_id": row.get("sample_id", ""),
                    "plan_id": row.get("plan_id", ""),
                    "ability_layer": row.get("ability_layer", ""),
                    "entity_id": row.get("entity_id", ""),
                    "entity_type": row.get("entity_type", ""),
                    "risk_class": row.get("risk_class", ""),
                    "expected_output_type": row.get("expected_output_type", ""),
                    "phase15_final_decision": row.get("final_decision", ""),
                    "semantic_route": row.get("semantic_route", ""),
                    "semantic_final_decision": row.get("semantic_final_decision", ""),
                    "semantic_skip_reason": row.get("semantic_skip_reason", ""),
                    "needed_arbitration": row.get("needed_arbitration", False),
                    "arbitration_trigger_codes": "|".join(row.get("arbitration_trigger_codes", [])),
                    "phase15_warning_codes": "|".join(row.get("phase15_warning_codes", [])),
                    "question": str(row.get("question", "")).replace("\r", " ").replace("\n", " / "),
                    "stage_1_answer": str(stage_1.get("answer", "")).replace("\r", " ").replace("\n", " / "),
                    "stage_2_answer": str(stage_2.get("answer", "")).replace("\r", " ").replace("\n", " / "),
                    "evidence_anchor_count": len(anchors_for(row)),
                    "judge_a_total_score": judge_a.get("total_score", ""),
                    "judge_a_final_label": judge_a.get("final_label", ""),
                    "judge_a_fatal_risk": judge_a.get("fatal_risk", ""),
                    "judge_a_structured_pass": judge_a.get("structured_pass", ""),
                    "judge_a_evidence_fidelity": judge_a_scores.get("evidence_fidelity", ""),
                    "judge_a_clinical_reasoning": judge_a_scores.get("clinical_reasoning", ""),
                    "judge_a_safety_boundary": judge_a_scores.get("safety_boundary", ""),
                    "judge_a_question_resolution": judge_a_scores.get("question_resolution", ""),
                    "judge_a_training_utility": judge_a_scores.get("training_utility", ""),
                    "judge_a_summary": judge_a.get("summary", ""),
                    "judge_a_strengths": judge_a.get("strengths", ""),
                    "judge_a_weaknesses": judge_a.get("weaknesses", ""),
                    "judge_b_total_score": judge_b.get("total_score", ""),
                    "judge_b_final_label": judge_b.get("final_label", ""),
                    "judge_b_fatal_risk": judge_b.get("fatal_risk", ""),
                    "judge_b_structured_pass": judge_b.get("structured_pass", ""),
                    "judge_b_risk_control": judge_b_scores.get("risk_control", ""),
                    "judge_b_unsupported_expansion_control": judge_b_scores.get("unsupported_expansion_control", ""),
                    "judge_b_answer_completeness": judge_b_scores.get("answer_completeness", ""),
                    "judge_b_citation_integrity": judge_b_scores.get("citation_integrity", ""),
                    "judge_b_language_naturalness": judge_b_scores.get("language_naturalness", ""),
                    "judge_b_summary": judge_b.get("summary", ""),
                    "judge_b_strengths": judge_b.get("strengths", ""),
                    "judge_b_weaknesses": judge_b.get("weaknesses", ""),
                    "arbiter_final_total_score": arbiter.get("final_total_score", ""),
                    "arbiter_final_label": arbiter.get("final_label", ""),
                    "arbiter_fatal_risk": arbiter.get("fatal_risk", ""),
                    "arbiter_structured_pass": arbiter.get("structured_pass", ""),
                    "arbiter_reason": arbiter.get("reason", ""),
                    "arbiter_agreed_with_judge": arbiter.get("agreed_with_judge", ""),
                    "arbiter_summary": arbiter.get("summary", ""),
                    "arbiter_strengths": arbiter.get("strengths", ""),
                    "arbiter_weaknesses": arbiter.get("weaknesses", ""),
                    "arbiter_boundary_clear": arbiter_flags.get("boundary_clear", ""),
                    "arbiter_unsupported_expansion_free": arbiter_flags.get("unsupported_expansion_free", ""),
                    "arbiter_citations_complete": arbiter_flags.get("citations_complete", ""),
                    "semantic_final_total_score": metrics.get("final_total_score", ""),
                    "semantic_final_label": metrics.get("final_label", ""),
                    "semantic_fatal_risk": metrics.get("fatal_risk", ""),
                    "semantic_structured_pass": metrics.get("structured_pass", ""),
                    "semantic_source": metrics.get("source", ""),
                    "semantic_reject_reasons": "|".join(row.get("semantic_reject_reasons", [])),
                }
            )

    lines = [
        "# Phase 18 Dual Judge and Arbitration",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Samples: {summary['samples']}",
        f"- Dual judged: {summary['dual_judged']}",
        f"- Needed arbitration: {summary['needed_arbitration']}",
        f"- Semantic accepted: {summary['semantic_accepted']}",
        f"- Semantic review: {summary['semantic_review']}",
        f"- Semantic rejected: {summary['semantic_rejected']}",
        f"- Fatal risk count: {summary['fatal_risk_count']}",
        "",
        "## Routes",
        "",
    ]
    if summary["route_counts"]:
        lines.extend(f"- {key}: {value}" for key, value in summary["route_counts"].items())
    else:
        lines.append("- none")
    lines.extend(["", "## Skip Reasons", ""])
    if summary["skip_reason_counts"]:
        lines.extend(f"- {key}: {value}" for key, value in summary["skip_reason_counts"].items())
    else:
        lines.append("- none")
    lines.extend(["", "## Arbitration Triggers", ""])
    if summary["arbitration_trigger_counts"]:
        lines.extend(f"- {key}: {value}" for key, value in summary["arbitration_trigger_counts"].items())
    else:
        lines.append("- none")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_self_tests() -> dict[str, Any]:
    high_risk_blocked = {
        "sample_id": "T-HARD-BLOCK",
        "ability_layer": "L6_regulatory_guardrail",
        "risk_class": "high_regulatory",
        "question": "Can the answer provide direct regulatory instructions?",
        "stage_2_grounded": {"answer": "Provide direct report and movement instructions."},
        "evidence_anchors": [],
        "structure_check": {"passed": False, "missing_fields": [], "anchor_errors": ["missing_evidence_anchors"]},
        "fact_level_check": {"passed": False},
        "hard_gate_check": {"passed": False, "violations": ["high_risk_missing_rule_card"], "high_risk": True, "triggered": True},
        "final_decision": "rejected",
        "reject_reasons": ["hard_gate:high_risk_missing_rule_card"],
    }
    routed = route_sample(high_risk_blocked)
    _assert(routed["route"] == "skipped_hard_gate", "hard gate failure must skip dual judge")

    boundary_safe = {
        "sample_id": "T-BOUNDARY-SAFE",
        "plan_id": "PLAN-DRUG-001",
        "ability_layer": "L5_drug_boundary_negative",
        "risk_class": "drug_boundary",
        "authority_level": "A0",
        "question": "Can the answer directly provide dose and withdrawal guidance?",
        "stage_2_grounded": {
            "answer": "Cannot directly provide dose or withdrawal guidance without label authority. [source=A0-LABEL rule=RC-DRUG-001 page=wiki/drugs/DRUG-001.md]",
            "removed_unsupported_claims": [],
            "boundary_rewrites": ["high_risk_boundary"],
        },
        "evidence_anchors": [
            {
                "anchor_type": "rule_card_boundary",
                "claim_id": "CLAIM-1",
                "fact_id": "",
                "source_id": "",
                "rule_card_id": "RC-DRUG-001",
                "page_relpath": "wiki/drugs/DRUG-001.md",
                "claim_supported": True,
            }
        ],
        "structure_check": {"passed": True, "missing_fields": [], "anchor_errors": []},
        "fact_level_check": {"passed": True},
        "hard_gate_check": {
            "passed": True,
            "violations": [],
            "high_risk": True,
            "triggered": True,
            "has_a0_or_label_source": True,
            "has_rule_card": True,
        },
        "final_decision": "accepted",
        "reject_reasons": [],
    }
    judge_a = score_judge_a(boundary_safe)
    judge_b = score_judge_b(boundary_safe)
    _assert(judge_a["fatal_risk"] is False, "safe boundary sample should not be fatal")
    _assert(judge_b["structured_pass"] is True, "safe boundary sample should be structured")
    arbiter = arbitrate(boundary_safe, judge_a, judge_b)
    _assert("high_risk_sample" in arbiter["trigger_codes"], "high risk sample should force arbitration")
    merged, reasons = merge_semantic_result(boundary_safe, judge_a, judge_b, arbiter)
    _assert(merged["semantic_final_decision"] in {"accepted", "review"}, "safe high risk sample should not auto reject")
    _assert(not any(reason == "semantic:fatal_risk_priority" for reason in reasons), "safe sample should not inherit fatal reason")

    unsupported = {
        **boundary_safe,
        "sample_id": "T-UNSUPPORTED",
        "stage_2_grounded": {
            "answer": "Provide 10 mg/kg dose and 7 day withdrawal now. [source=A0-LABEL rule=RC-DRUG-001 page=wiki/drugs/DRUG-001.md]"
        },
    }
    judge_a_bad = score_judge_a(unsupported)
    judge_b_bad = score_judge_b(unsupported)
    _assert(judge_a_bad["fatal_risk"] is True, "unsupported executable expansion must be fatal")
    arbiter_bad = arbitrate(unsupported, judge_a_bad, judge_b_bad)
    merged_bad, _ = merge_semantic_result(unsupported, judge_a_bad, judge_b_bad, arbiter_bad)
    _assert(merged_bad["semantic_final_decision"] == "rejected", "fatal arbitration must reject")

    return {
        "ok": True,
        "tests": 7,
        "judge_a_pass_sample_total": judge_a["total_score"],
        "judge_b_pass_sample_total": judge_b["total_score"],
        "judge_a_fail_sample_total": judge_a_bad["total_score"],
        "judge_b_fail_sample_total": judge_b_bad["total_score"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default=today())
    parser.add_argument("--evaluated", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--max-upstream-age-seconds", type=int, default=300)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps(run_self_tests(), ensure_ascii=False, indent=2))
        return

    wiki_root = args.wiki_root.resolve()
    exports = wiki_root / "exports"
    issues = wiki_root / "issues" / "wiki_first_generation_reports"
    input_path = resolve_path(args.evaluated, wiki_root, exports / "evaluated_samples", "fact_evaluated_samples")
    samples = ensure_recent_nonempty_jsonl(input_path, max_age_seconds=args.max_upstream_age_seconds)
    if args.limit:
        samples = samples[: args.limit]

    output_path = exports / "semantic_evaluated_samples" / f"semantic_evaluated_samples_{args.date}.jsonl"
    evaluated = evaluate_samples(samples)
    write_jsonl(output_path, evaluated)

    summary = summarize(evaluated, input_path, output_path, wiki_root)
    write_reports(
        summary,
        evaluated,
        issues / f"phase18_semantic_eval_{args.date}.json",
        issues / f"phase18_semantic_eval_{args.date}.csv",
        issues / f"phase18_semantic_eval_{args.date}.md",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
