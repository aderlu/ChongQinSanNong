"""Shared normalization helpers for evaluation payloads."""

from __future__ import annotations

from typing import Any, Dict, Optional


def coerce_payload_to_object(payload: Any) -> Optional[Dict[str, Any]]:
    """Return the first dictionary-like object from a parsed payload."""
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                return item
    return None


def normalize_bool(value: Any) -> bool:
    """Normalize loose truthy values from model outputs."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "pass"}
    return bool(value)


def normalize_score(
    value: Any,
    max_value: float,
    *,
    allow_ratio_scale: bool = False,
    round_digits: int = 2,
) -> float:
    """Normalize a score into the configured range."""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0

    if allow_ratio_scale and 0 <= numeric <= 1:
        numeric *= float(max_value)

    normalized = max(0.0, min(float(max_value), numeric))
    return round(normalized, round_digits)


def normalize_total_score(
    value: Any,
    *,
    allow_ratio_scale: bool = True,
    round_digits: int = 2,
) -> float:
    """Normalize total score using a 100-point scale."""
    return normalize_score(
        value,
        100.0,
        allow_ratio_scale=allow_ratio_scale,
        round_digits=round_digits,
    )


def normalize_judge_payload(
    payload: Any,
    *,
    allow_ratio_scale: bool = True,
    summary_max_length: Optional[int] = None,
    strengths_max_length: Optional[int] = None,
    weaknesses_max_length: Optional[int] = None,
) -> Dict[str, Any]:
    """Normalize a judge/evaluator payload into the shared schema."""
    payload_obj = coerce_payload_to_object(payload) or {}
    normalized = {
        "total_score": normalize_total_score(
            payload_obj.get("total_score"),
            allow_ratio_scale=allow_ratio_scale,
        ),
        "diagnosis_accuracy": normalize_score(
            payload_obj.get("diagnosis_accuracy"),
            30.0,
            allow_ratio_scale=allow_ratio_scale,
        ),
        "pathology_logic": normalize_score(
            payload_obj.get("pathology_logic"),
            20.0,
            allow_ratio_scale=allow_ratio_scale,
        ),
        "prescription_safety": normalize_score(
            payload_obj.get("prescription_safety"),
            30.0,
            allow_ratio_scale=allow_ratio_scale,
        ),
        "data_quality": normalize_score(
            payload_obj.get("data_quality"),
            20.0,
            allow_ratio_scale=allow_ratio_scale,
        ),
        "fatal_risk": normalize_bool(payload_obj.get("fatal_risk")),
        "structured_pass": normalize_bool(payload_obj.get("structured_pass")),
        "summary": str(payload_obj.get("summary", "")).strip(),
        "strengths": str(payload_obj.get("strengths", "")).strip(),
        "weaknesses": str(payload_obj.get("weaknesses", "")).strip(),
    }

    if normalized["total_score"] <= 0:
        normalized["total_score"] = round(
            normalized["diagnosis_accuracy"]
            + normalized["pathology_logic"]
            + normalized["prescription_safety"]
            + normalized["data_quality"],
            2,
        )

    if summary_max_length is not None:
        normalized["summary"] = normalized["summary"][:summary_max_length]
    if strengths_max_length is not None:
        normalized["strengths"] = normalized["strengths"][:strengths_max_length]
    if weaknesses_max_length is not None:
        normalized["weaknesses"] = normalized["weaknesses"][:weaknesses_max_length]

    return normalized
