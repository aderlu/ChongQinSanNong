"""Evaluation adapters and shared normalization helpers."""

from .deepeval_adapter import evaluate_case_with_deepeval_adapter
from .normalizers import (
    coerce_payload_to_object,
    normalize_bool,
    normalize_judge_payload,
    normalize_score,
    normalize_total_score,
)

__all__ = [
    "coerce_payload_to_object",
    "evaluate_case_with_deepeval_adapter",
    "normalize_bool",
    "normalize_judge_payload",
    "normalize_score",
    "normalize_total_score",
]
