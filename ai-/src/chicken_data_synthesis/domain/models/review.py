from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class RuleCheckResult:
    """Normalized result returned by the guard layer."""

    enabled: bool
    hard_block: bool
    fatal_risk: bool
    codes: List[str] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class JudgeResult:
    """Normalized score payload returned by one judge model."""

    judge_label: str
    judge_model: str
    total_score: float
    diagnosis_accuracy: float
    pathology_logic: float
    prescription_safety: float
    data_quality: float
    fatal_risk: bool = False
    structured_pass: bool = False
    summary: str = ""


@dataclass(frozen=True)
class FinalDecision:
    """Final decision after aggregation and optional arbitration."""

    final_label: str
    final_total_score: float
    needed_arbitration: bool
    arbiter_model: str = ""
    reason: str = ""
