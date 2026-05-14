from __future__ import annotations

"""Governance gates for veterinary LLM Wiki mutations.

This module is intentionally small and dependency-light. It validates that
write operations have an auditable reason and evidence before they enter the
orchestration layer, and it writes machine-readable audit events that can be
reviewed independently from the human-facing ``log.md``.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


WRITE_OPERATIONS = {"create", "update", "delete"}
READ_OPERATIONS = {"read", "query"}
VALID_OPERATIONS = WRITE_OPERATIONS | READ_OPERATIONS
SEMANTIC_ACTIONS = {
    "additive_evidence",
    "supersedes_previous",
    "deprecated_obsolete",
    "orphan_cleanup",
    "accidental_or_invalid",
    "cache_reconciliation",
    "candidate_only",
    "unknown",
}


@dataclass(frozen=True)
class WikiChangeRequest:
    operation: str
    target: str
    reason: str
    evidence: str
    actor: str = "system"
    scope: str = "llm_wiki"
    semantic_action: str = "unknown"
    semantic_confidence: str = "rule_inferred"


@dataclass(frozen=True)
class WikiGovernanceEvent:
    event_id: str
    timestamp: str
    phase: str
    operation: str
    target: str
    actor: str
    reason: str
    evidence: str
    semantic_action: str
    semantic_confidence: str
    status: str
    details: Mapping[str, Any]


def validate_change_request(
    *,
    operation: str,
    target: str,
    reason: str = "",
    evidence: str = "",
    actor: str = "system",
    scope: str = "llm_wiki",
) -> WikiChangeRequest:
    """Validate CRUD governance fields before a mutation is allowed."""

    op = str(operation or "").strip().lower()
    if op not in VALID_OPERATIONS:
        raise ValueError(f"Unsupported wiki governance operation: {operation}")
    target_text = str(target or "").strip()
    if not target_text:
        raise ValueError("target is required for wiki governance.")
    reason_text = str(reason or "").strip()
    evidence_text = str(evidence or "").strip()
    if op in WRITE_OPERATIONS:
        if len(reason_text) < 8:
            raise ValueError("reason is required for wiki write operations and must be specific.")
        if len(evidence_text) < 8:
            raise ValueError("evidence is required for wiki write operations and must be traceable.")
    semantic_action = classify_change_semantics(operation=op, target=target_text, reason=reason_text, evidence=evidence_text)
    if op == "delete" and semantic_action == "unknown":
        raise ValueError(
            "delete operations must state a factual lifecycle reason: "
            "obsolete/deprecated, superseded/replaced, orphan, duplicate, invalid, accidental, or irrelevant."
        )
    return WikiChangeRequest(
        operation=op,
        target=target_text,
        reason=reason_text,
        evidence=evidence_text,
        actor=str(actor or "system").strip() or "system",
        scope=str(scope or "llm_wiki").strip() or "llm_wiki",
        semantic_action=semantic_action,
    )


def append_governance_event(
    wiki_dir: str | Path,
    request: WikiChangeRequest,
    *,
    phase: str,
    status: str,
    details: Mapping[str, Any] | None = None,
) -> WikiGovernanceEvent:
    """Append a governance event to JSONL audit and the human log."""

    root = Path(wiki_dir)
    timestamp = datetime.now().isoformat(timespec="seconds")
    event = WikiGovernanceEvent(
        event_id=_event_id(timestamp, request, phase),
        timestamp=timestamp,
        phase=str(phase or "").strip() or "unknown",
        operation=request.operation,
        target=request.target,
        actor=request.actor,
        reason=request.reason,
        evidence=request.evidence,
        semantic_action=request.semantic_action,
        semantic_confidence=request.semantic_confidence,
        status=str(status or "").strip() or "unknown",
        details=dict(details or {}),
    )
    issues_dir = root / "issues"
    issues_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = issues_dir / f"wiki_governance_audit_{timestamp[:10]}.jsonl"
    with jsonl_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(event), ensure_ascii=False, sort_keys=True) + "\n")
    log_path = root / "log.md"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n"
            f"{timestamp[:10]} governance | phase={event.phase}"
            f" | operation={event.operation}"
            f" | target={event.target}"
            f" | status={event.status}"
            f" | reason={event.reason}"
            f" | evidence={event.evidence}"
            f" | semantic_action={event.semantic_action}"
            f" | event_id={event.event_id}\n"
        )
    return event


def classify_change_semantics(*, operation: str, target: str, reason: str, evidence: str) -> str:
    """Infer the factual lifecycle meaning of a write operation from auditable text.

    The classifier is deliberately conservative and deterministic. LLMs may
    suggest one of these categories in future workflows, but this function is
    the code-level gate used for audit and graph rendering.
    """

    text = f"{operation} {target} {reason} {evidence}".lower()
    if any(token in text for token in ("cache", "mapping", "reconciliation", "映射", "缓存")):
        return "cache_reconciliation"
    if any(token in text for token in ("candidate", "pending_review", "authority_source_discovery", "gap-first", "补齐", "候选")):
        return "candidate_only"
    if any(token in text for token in ("supersede", "superseded", "replace", "replaced", "replacement", "覆盖", "替代", "取代")):
        return "supersedes_previous"
    if any(token in text for token in ("obsolete", "deprecated", "expired", "outdated", "过期", "废止", "弃用", "失效")):
        return "deprecated_obsolete"
    if any(token in text for token in ("orphan", "unreferenced", "no reference", "not referenced", "孤儿", "无引用")):
        return "orphan_cleanup"
    if any(token in text for token in ("duplicate", "invalid", "irrelevant", "accidental", "wrong", "误删", "错误", "无关", "重复")):
        return "accidental_or_invalid"
    if str(operation).lower() == "create":
        return "additive_evidence"
    return "unknown"


def _event_id(timestamp: str, request: WikiChangeRequest, phase: str) -> str:
    safe = "|".join((timestamp, request.operation, request.target, str(phase or "")))
    return f"GOV-{abs(hash(safe)) % 10_000_000:07d}"
