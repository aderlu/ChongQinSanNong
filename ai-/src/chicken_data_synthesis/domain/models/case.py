from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class DiseaseSeed:
    """Input seed used to plan one candidate case."""

    disease_name: str
    scenario_hint: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QueryDraft:
    """Stage-one output that contains only the user-facing query and safe metadata."""

    user_query: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GeneratedCase:
    """Final candidate case emitted by the two-stage generation flow."""

    species: str
    user_query: str
    diagnosis: str
    prescription: str
    withdrawal_period: str
    metadata: Dict[str, Any] = field(default_factory=dict)
