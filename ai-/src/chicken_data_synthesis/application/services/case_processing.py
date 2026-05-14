from __future__ import annotations

import copy
import uuid
from typing import Any, Mapping


CaseResult = dict[str, Any]
JudgeResult = Mapping[str, Any]

DEFAULT_REJECT_METRICS = {
    "final_total_score": 0,
    "final_diagnosis_accuracy": 0,
    "final_pathology_logic": 0,
    "final_prescription_safety": 0,
    "final_data_quality": 0,
    "final_label": "reject",
}


def build_case_result_base(
    index: int,
    disease_name: str,
    generator_key: str,
    generator_model: str,
    *,
    case_id: str | None = None,
) -> CaseResult:
    return {
        "case_id": case_id or str(uuid.uuid4()),
        "index": index,
        "disease_name": disease_name,
        "generator_key": generator_key,
        "generator_model": generator_model,
        "success": False,
        "error": "",
        "generation_seconds": 0.0,
        "judge_a_seconds": 0.0,
        "judge_b_seconds": 0.0,
        "arbiter_seconds": 0.0,
        "needed_arbitration": False,
        "rule_base_result": None,
        "case_data": None,
        "judge_a_result": None,
        "judge_b_result": None,
        "arbiter_result": None,
        "final_metrics": None,
    }


def build_reject_final_metrics(*, label: str = "reject") -> dict[str, Any]:
    result = dict(DEFAULT_REJECT_METRICS)
    result["final_label"] = label
    return result


def merge_case_result(
    result: Mapping[str, Any],
    **updates: Any,
) -> CaseResult:
    merged = copy.deepcopy(dict(result))
    merged.update(updates)
    return merged


def build_case_error_result(
    result: Mapping[str, Any],
    error: str,
    **updates: Any,
) -> CaseResult:
    merged_updates = {"error": error}
    merged_updates.update(updates)
    return merge_case_result(result, **merged_updates)


def build_rule_blocked_result(
    result: Mapping[str, Any],
    rule_base_result: Mapping[str, Any] | None,
    *,
    error: str = "规则底座拦截",
) -> CaseResult:
    return build_case_error_result(
        result,
        error,
        rule_base_result=copy.deepcopy(rule_base_result),
        final_metrics=build_reject_final_metrics(),
    )


def should_require_arbitration(
    judge_a_result: JudgeResult,
    judge_b_result: JudgeResult,
    arbitration_threshold: float,
) -> bool:
    score_diff = abs(float(judge_a_result.get("total_score", 0)) - float(judge_b_result.get("total_score", 0)))
    return (
        score_diff > arbitration_threshold
        or bool(judge_a_result.get("fatal_risk", False))
        or bool(judge_b_result.get("fatal_risk", False))
    )


def select_final_metrics(
    judge_a_result: JudgeResult,
    judge_b_result: JudgeResult,
    arbiter_result: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if arbiter_result:
        return {
            "final_total_score": arbiter_result.get("final_total_score", 0),
            "final_diagnosis_accuracy": arbiter_result.get("final_diagnosis_accuracy", 0),
            "final_pathology_logic": arbiter_result.get("final_pathology_logic", 0),
            "final_prescription_safety": arbiter_result.get("final_prescription_safety", 0),
            "final_data_quality": arbiter_result.get("final_data_quality", 0),
            "final_label": arbiter_result.get("final_label", "review"),
        }

    avg_total = round((judge_a_result.get("total_score", 0) + judge_b_result.get("total_score", 0)) / 2, 2)
    avg_diag = round(
        (judge_a_result.get("diagnosis_accuracy", 0) + judge_b_result.get("diagnosis_accuracy", 0)) / 2,
        2,
    )
    avg_logic = round((judge_a_result.get("pathology_logic", 0) + judge_b_result.get("pathology_logic", 0)) / 2, 2)
    avg_safety = round(
        (judge_a_result.get("prescription_safety", 0) + judge_b_result.get("prescription_safety", 0)) / 2,
        2,
    )
    avg_quality = round((judge_a_result.get("data_quality", 0) + judge_b_result.get("data_quality", 0)) / 2, 2)
    final_label = "pass" if avg_total >= 80 and not should_require_arbitration(judge_a_result, judge_b_result, 999999) else "review"
    return {
        "final_total_score": avg_total,
        "final_diagnosis_accuracy": avg_diag,
        "final_pathology_logic": avg_logic,
        "final_prescription_safety": avg_safety,
        "final_data_quality": avg_quality,
        "final_label": final_label,
    }


def apply_final_quality_gates(
    final_metrics: Mapping[str, Any],
    *,
    disease_name: str,
    case_data: Mapping[str, Any],
    rule_base_result: Mapping[str, Any] | None,
    judge_a_result: JudgeResult,
    judge_b_result: JudgeResult,
) -> dict[str, Any]:
    result = dict(final_metrics)
    diagnosis = str(case_data.get("diagnosis", "") or "")
    target = str(disease_name or "").strip()
    target_in_diagnosis = bool(target and target in diagnosis)
    rule_fatal = bool((rule_base_result or {}).get("fatal_risk"))
    judge_fatal = bool(judge_a_result.get("fatal_risk") or judge_b_result.get("fatal_risk"))

    result["target_disease_in_diagnosis"] = target_in_diagnosis
    result["fatal_risk"] = rule_fatal or judge_fatal
    result["rule_fatal_risk"] = rule_fatal

    if not target_in_diagnosis:
        result["target_disease_mismatch"] = True
        result["final_label"] = "review"
        try:
            result["final_diagnosis_accuracy"] = min(float(result.get("final_diagnosis_accuracy", 0) or 0), 20.0)
        except (TypeError, ValueError):
            result["final_diagnosis_accuracy"] = 0
    else:
        result["target_disease_mismatch"] = False

    if result["fatal_risk"] and result.get("final_label") == "pass":
        result["final_label"] = "review"
    return result


def build_completed_case_result(
    result: Mapping[str, Any],
    *,
    case_data: Mapping[str, Any],
    rule_base_result: Mapping[str, Any] | None,
    judge_a_result: JudgeResult,
    judge_b_result: JudgeResult,
    arbitration_threshold: float,
    arbiter_result: Mapping[str, Any] | None = None,
    generation_seconds: float | None = None,
    judge_a_seconds: float | None = None,
    judge_b_seconds: float | None = None,
    arbiter_seconds: float | None = None,
) -> CaseResult:
    needed_arbitration = should_require_arbitration(judge_a_result, judge_b_result, arbitration_threshold)
    final_metrics = apply_final_quality_gates(
        select_final_metrics(judge_a_result, judge_b_result, arbiter_result),
        disease_name=str(result.get("disease_name", "")),
        case_data=case_data,
        rule_base_result=rule_base_result,
        judge_a_result=judge_a_result,
        judge_b_result=judge_b_result,
    )
    updates: dict[str, Any] = {
        "success": True,
        "error": "",
        "case_data": copy.deepcopy(dict(case_data)),
        "rule_base_result": copy.deepcopy(rule_base_result),
        "judge_a_result": copy.deepcopy(dict(judge_a_result)),
        "judge_b_result": copy.deepcopy(dict(judge_b_result)),
        "arbiter_result": copy.deepcopy(arbiter_result),
        "needed_arbitration": needed_arbitration,
        "final_metrics": final_metrics,
    }
    if generation_seconds is not None:
        updates["generation_seconds"] = round(generation_seconds, 2)
    if judge_a_seconds is not None:
        updates["judge_a_seconds"] = round(judge_a_seconds, 2)
    if judge_b_seconds is not None:
        updates["judge_b_seconds"] = round(judge_b_seconds, 2)
    if arbiter_seconds is not None:
        updates["arbiter_seconds"] = round(arbiter_seconds, 2)
    return merge_case_result(result, **updates)


__all__ = [
    "CaseResult",
    "DEFAULT_REJECT_METRICS",
    "build_case_error_result",
    "build_case_result_base",
    "build_completed_case_result",
    "build_reject_final_metrics",
    "build_rule_blocked_result",
    "merge_case_result",
    "select_final_metrics",
    "apply_final_quality_gates",
    "should_require_arbitration",
]
