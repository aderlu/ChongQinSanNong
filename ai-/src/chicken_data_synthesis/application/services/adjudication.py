from __future__ import annotations

import copy
from typing import Any, Dict, Mapping, Optional

ArbiterResult = Dict[str, Any]
TimedArbiterResult = tuple[ArbiterResult | None, float]

from chicken_data_synthesis.application.services.review import compute_score_difference


def _average_metric(judge_a_result: Dict[str, Any], judge_b_result: Dict[str, Any], key: str) -> float:
    """Return the rounded average for a single metric key."""

    return round((judge_a_result.get(key, 0) + judge_b_result.get(key, 0)) / 2, 2)


def build_rule_blocked_final_metrics() -> Dict[str, Any]:
    """Return the legacy final-metrics payload for hard rule-base blocks."""

    return {
        "final_total_score": 0,
        "final_diagnosis_accuracy": 0,
        "final_pathology_logic": 0,
        "final_prescription_safety": 0,
        "final_data_quality": 0,
        "final_label": "reject",
    }


def should_trigger_arbitration(
    judge_a_result: Dict[str, Any],
    judge_b_result: Dict[str, Any],
    arbitration_threshold: float,
) -> bool:
    """Match the legacy arbitration trigger rule used in the main script."""

    return (
        compute_score_difference(judge_a_result, judge_b_result) > float(arbitration_threshold)
        or bool(judge_a_result.get("fatal_risk", False))
        or bool(judge_b_result.get("fatal_risk", False))
    )


def select_final_metrics(
    judge_a_result: Dict[str, Any],
    judge_b_result: Dict[str, Any],
    arbiter_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Choose final metrics from arbiter output or judge averages."""

    if arbiter_result:
        return {
            "final_total_score": arbiter_result.get("final_total_score", 0),
            "final_diagnosis_accuracy": arbiter_result.get("final_diagnosis_accuracy", 0),
            "final_pathology_logic": arbiter_result.get("final_pathology_logic", 0),
            "final_prescription_safety": arbiter_result.get("final_prescription_safety", 0),
            "final_data_quality": arbiter_result.get("final_data_quality", 0),
            "final_label": arbiter_result.get("final_label", "review"),
        }

    avg_total = _average_metric(judge_a_result, judge_b_result, "total_score")
    avg_diag = _average_metric(judge_a_result, judge_b_result, "diagnosis_accuracy")
    avg_logic = _average_metric(judge_a_result, judge_b_result, "pathology_logic")
    avg_safety = _average_metric(judge_a_result, judge_b_result, "prescription_safety")
    avg_quality = _average_metric(judge_a_result, judge_b_result, "data_quality")
    final_label = (
        "pass"
        if avg_total >= 80 and not (judge_a_result.get("fatal_risk") or judge_b_result.get("fatal_risk"))
        else "review"
    )
    return {
        "final_total_score": avg_total,
        "final_diagnosis_accuracy": avg_diag,
        "final_pathology_logic": avg_logic,
        "final_prescription_safety": avg_safety,
        "final_data_quality": avg_quality,
        "final_label": final_label,
    }


def arbitrate_case_with_fallbacks(
    case_data: Dict[str, Any],
    judge_a_result: Dict[str, Any],
    judge_b_result: Dict[str, Any],
    primary_config: Mapping[str, Any],
    *,
    candidate_models: Mapping[str, Mapping[str, Any]],
    arbitrate_case,
) -> TimedArbiterResult:
    """Run arbitration across the configured fallback chain."""

    from chicken_data_synthesis.application.services.review import build_model_fallback_chain

    total_elapsed = 0.0
    for attempt_index, config in enumerate(build_model_fallback_chain(primary_config, candidate_models), start=1):
        result, elapsed = arbitrate_case(case_data, judge_a_result, judge_b_result, copy.deepcopy(dict(config)))
        total_elapsed += elapsed
        if result is not None:
            if attempt_index > 1:
                result["fallback_used"] = True
                result["fallback_attempt"] = attempt_index
                result["arbiter_model"] = config["name"]
            return result, total_elapsed
    return None, total_elapsed
