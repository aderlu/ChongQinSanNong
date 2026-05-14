from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
MANIFEST = EXPORTS / "runtime_core_manifest.json"
GOLD_INDEX = EXPORTS / "gold_dataset_readiness_index.csv"
DRUG_ROLE_INDEX = EXPORTS / "drug_gold_role_index.csv"
REPORT_JSON = ISSUES / "review_status_migration_2026-05-09.json"
TZ = timezone(timedelta(hours=8))


GOLD_FIELDS = [
    "entity_id",
    "entity_type",
    "page_relpath",
    "source_trust",
    "evidence_coverage",
    "authority_level",
    "risk_class",
    "usage_scope",
    "positive_generation_allowed",
    "negative_trap_allowed",
    "evaluation_allowed",
    "requires_rule_cards",
    "allowed_question_types",
    "blocked_question_types",
    "source_ids",
    "rule_card_ids",
    "missing_critical_fields",
]


DRUG_FIELDS = [
    "drug_id",
    "page_relpath",
    "usage_scope",
    "source_trust",
    "evidence_coverage",
    "authority_level",
    "positive_generation_allowed",
    "negative_trap_allowed",
    "evaluation_allowed",
    "requires_rule_cards",
    "source_ids",
    "blocked_reason",
]


def load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def as_joined(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(x) for x in value if str(x))
    return str(value or "")


def missing_fields(entry: dict[str, object]) -> list[str]:
    required = ["page_id", "path", "entity_type", "source_trust", "evidence_coverage", "authority_level", "risk_class", "usage_scope"]
    missing = [key for key in required if not entry.get(key)]
    if entry.get("source_trust") == "authoritative" and not entry.get("source_ids") and entry.get("entity_type") not in {"rule_card", "synthesis", "comparison", "syndrome"}:
        missing.append("source_ids")
    return missing


def usage_set(entry: dict[str, object]) -> set[str]:
    value = entry.get("usage_scope", [])
    if isinstance(value, list):
        return {str(item) for item in value if str(item)}
    return {item.strip() for item in str(value or "").replace(",", ";").split(";") if item.strip()}


def requires_rule_cards(entry: dict[str, object]) -> list[str]:
    risk = entry.get("risk_class", "")
    etype = entry.get("entity_type", "")
    cards: list[str] = []
    if etype == "drug" or risk == "drug_boundary":
        cards.append("RC-DRUG-001")
    if risk in {"withdrawal_mrl_residue", "food_safety"}:
        cards.append("RC-WITHDRAWAL-MRL-001")
    if risk == "high_regulatory":
        cards.append("RC-DISEASE-REGULATORY-001")
    if usage_set(entry).intersection({"gold_candidate", "diagnosis_support", "differential_support", "control_support"}):
        cards.append("RC-CITATION-001")
    return sorted(set(cards))


def gold_permissions(entry: dict[str, object], required_cards: list[str]) -> tuple[bool, bool, bool]:
    scopes = usage_set(entry)
    risk = entry.get("risk_class", "")
    authority = entry.get("authority_level", "")
    valid = entry.get("source_trust") == "authoritative" and entry.get("evidence_coverage") in {"complete", "partial"}
    high_risk_positive = risk in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"}
    positive = bool(valid and "gold_candidate" in scopes and "audit_only" not in scopes and not high_risk_positive)
    if high_risk_positive and authority == "A0" and "gold_candidate" in scopes:
        positive = True
    if entry.get("entity_type") == "drug" and authority != "A0":
        positive = False
    negative = bool(valid and (entry.get("entity_type") == "drug" or high_risk_positive or "negative_trap" in scopes))
    evaluation = bool(valid and scopes.intersection({"gold_candidate", "negative_trap", "differential_support", "control_support", "regulatory_boundary", "drug_boundary"}))
    if scopes <= {"retrieval"} or "audit_only" in scopes:
        positive = False
    return positive, negative, evaluation


def drug_scope(entry: dict[str, object], positive: bool, negative: bool) -> tuple[str, str]:
    risk = entry.get("risk_class", "")
    authority = entry.get("authority_level", "")
    scopes = usage_set(entry)
    if entry.get("source_trust") != "authoritative" or entry.get("evidence_coverage") not in {"complete", "partial"}:
        return "audit_only", "blocked_or_insufficient_evidence"
    if positive and authority == "A0":
        return "positive_drug_candidate", ""
    if negative:
        return "negative_trap", "positive claim requires A0 or label-level source"
    if risk in {"drug_boundary", "withdrawal_mrl_residue", "food_safety"}:
        return "drug_boundary", "drug page is boundary support, not standalone prescription evidence"
    if "gap_routing" in scopes:
        return "gap_routing", "retrieval_or_context_only"
    return "audit_only", "retrieval_or_context_only"


def main() -> None:
    payload = load_manifest()
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        raise TypeError("manifest entries must be a list")

    gold_rows: list[dict[str, object]] = []
    drug_rows: list[dict[str, object]] = []
    usage_counts: dict[str, int] = {}
    blocked_reasons: dict[str, int] = {}

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        scopes = usage_set(entry)
        for scope in scopes:
            usage_counts[scope] = usage_counts.get(scope, 0) + 1
        missing = missing_fields(entry)
        cards = requires_rule_cards(entry)
        positive, negative, evaluation = gold_permissions(entry, cards)
        if missing:
            blocked_reasons["missing_critical_fields"] = blocked_reasons.get("missing_critical_fields", 0) + 1
        gold_rows.append(
            {
                "entity_id": entry.get("page_id", ""),
                "entity_type": entry.get("entity_type", ""),
                "page_relpath": entry.get("path", ""),
                "source_trust": entry.get("source_trust", ""),
                "evidence_coverage": entry.get("evidence_coverage", ""),
                "authority_level": entry.get("authority_level", ""),
                "risk_class": entry.get("risk_class", ""),
                "usage_scope": as_joined(entry.get("usage_scope", [])),
                "positive_generation_allowed": str(positive).lower(),
                "negative_trap_allowed": str(negative).lower(),
                "evaluation_allowed": str(evaluation).lower(),
                "requires_rule_cards": as_joined(cards),
                "allowed_question_types": as_joined(entry.get("allowed_question_types", [])),
                "blocked_question_types": as_joined(entry.get("blocked_question_types", [])),
                "source_ids": as_joined(entry.get("source_ids", [])),
                "rule_card_ids": as_joined(cards),
                "missing_critical_fields": as_joined(missing),
            }
        )
        if entry.get("entity_type") == "drug":
            scope, reason = drug_scope(entry, positive, negative)
            drug_rows.append(
                {
                    "drug_id": entry.get("page_id", ""),
                    "page_relpath": entry.get("path", ""),
                    "usage_scope": scope,
                    "source_trust": entry.get("source_trust", ""),
                    "evidence_coverage": entry.get("evidence_coverage", ""),
                    "authority_level": entry.get("authority_level", ""),
                    "positive_generation_allowed": str(positive).lower(),
                    "negative_trap_allowed": str(negative).lower(),
                    "evaluation_allowed": str(evaluation).lower(),
                    "requires_rule_cards": as_joined(cards),
                    "source_ids": as_joined(entry.get("source_ids", [])),
                    "blocked_reason": reason,
                }
            )

    write_csv(GOLD_INDEX, gold_rows, GOLD_FIELDS)
    write_csv(DRUG_ROLE_INDEX, drug_rows, DRUG_FIELDS)
    report = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "phase": "Phase 6 and Phase 7",
        "review_status_policy": {
            "primary_gate_fields": ["source_trust", "evidence_coverage", "usage_scope", "authority_level", "risk_class"],
            "rule": "Generation, evaluation, and audit gates are derived from the simplified fact/page contract.",
        },
        "entries": len(gold_rows),
        "drug_entries": len(drug_rows),
        "usage_scope_counts": usage_counts,
        "blocked_reason_counts": blocked_reasons,
        "outputs": {
            "gold_dataset_readiness_index": GOLD_INDEX.relative_to(ROOT).as_posix(),
            "drug_gold_role_index": DRUG_ROLE_INDEX.relative_to(ROOT).as_posix(),
        },
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
