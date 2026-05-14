import csv
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

"""runtime 核心清单重建脚本。

由 run_swine_wiki_maintenance_checks.py 在更新后验收阶段调用。
它读取更新后的 wiki/export 数据，重建 runtime_core_manifest.json，
并为后续图谱重建、风险审计和 readiness 检查提供输入。
"""

ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"

MANIFEST = EXPORTS / "runtime_core_manifest.json"
EXCLUDE = EXPORTS / "runtime_exclude_patterns.json"
SUMMARY = EXPORTS / "runtime_core_manifest_summary.md"

TZ = timezone(timedelta(hours=8))


def read_csv(name):
    path = EXPORTS / name
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def exists(relpath):
    return bool(relpath) and (ROOT / relpath).exists()


def split_sources(value):
    if not value:
        return []
    return [x.strip() for x in value.replace(",", ";").split(";") if x.strip()]


def coverage_from_row(row, *, default="partial"):
    coverage = row.get("evidence_coverage", "")
    if coverage in {"complete", "partial", "minimal"}:
        return coverage
    status = row.get("coverage_gap_status", "") or row.get("status", "")
    if status.startswith("source_anchored") and status.endswith(("clinical_page", "drug_evidence_page")):
        return "complete"
    if "partial" in status:
        return "partial"
    if status:
        return "minimal"
    return default


def trust_from_row(row, source_ids):
    value = row.get("source_trust", "")
    if value:
        return value
    return "authoritative" if source_ids else "needs_source_check"


def authority_from_sources(source_ids, entity_type):
    if entity_type == "rule_card":
        return "RC"
    if entity_type == "synthesis":
        return "RULE"
    if entity_type in {"comparison", "syndrome"}:
        return "SRC"
    prefixes = [sid.split("-", 1)[0] for sid in source_ids if sid]
    for level in ["A0", "A1", "A2", "SRC"]:
        if level in prefixes:
            return level
    return "SRC" if source_ids else ""


def question_types_for(entity_type, usage_scope, risk_class):
    if "blocked" in usage_scope:
        return [], ["positive_generation", "evaluation", "sft_training"]
    if entity_type == "disease":
        allowed = ["clinical_summary", "differential_diagnosis", "diagnostic_boundary", "control_boundary"]
        blocked = ["standalone_prescription", "dose_course", "withdrawal_mrl", "unsupported_regulatory_action"]
    elif entity_type == "drug":
        allowed = ["drug_boundary_check", "legality_or_label_boundary", "negative_trap", "retrieval_routing"]
        blocked = ["standalone_prescription", "unsupported_dose_course", "unsupported_withdrawal_mrl", "food_safety_clearance"]
    elif entity_type in {"comparison", "syndrome"}:
        allowed = ["differential_routing", "case_triage", "evaluation_prompt"]
        blocked = ["standalone_treatment", "regulatory_action"]
    elif entity_type in {"rule_card", "synthesis"}:
        allowed = ["generation_policy", "evaluation_policy", "hard_blocking"]
        blocked = ["new_biomedical_fact_generation"]
    else:
        allowed = ["retrieval_routing"]
        blocked = ["positive_generation"]
    if "retrieval" in usage_scope and "generation_context" not in usage_scope:
        allowed = [x for x in allowed if x in {"retrieval_routing", "differential_routing", "case_triage"}]
        blocked = sorted(set(blocked + ["positive_generation", "sft_training"]))
    if risk_class in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"}:
        blocked = sorted(set(blocked + ["unsupported_high_risk_positive_claim"]))
    return allowed, blocked


def add_entry(entries, *, page_id, relpath, entity_type, source_trust,
              evidence_coverage, usage_scope, runtime_tier, allowed_use,
              blocked_use=None, source_ids=None, risk_class="normal_clinical",
              metadata=None):
    source_ids = source_ids or []
    authority_level = authority_from_sources(source_ids, entity_type)
    allowed_question_types, blocked_question_types = question_types_for(entity_type, usage_scope, risk_class)
    entries.append({
        "page_id": page_id,
        "path": relpath,
        "entity_type": entity_type,
        "source_trust": source_trust,
        "evidence_coverage": evidence_coverage,
        "usage_scope": usage_scope,
        "authority_level": authority_level,
        "risk_class": risk_class,
        "allowed_question_types": allowed_question_types,
        "blocked_question_types": blocked_question_types,
        "runtime_tier": runtime_tier,
        "allowed_use": allowed_use,
        "blocked_use": blocked_use or [],
        "source_ids": source_ids,
        "path_exists": exists(relpath),
        "metadata": metadata or {},
    })


def disease_entries(entries):
    for row in read_csv("disease_index.csv"):
        status = row.get("coverage_gap_status", "")
        source_ids = [row.get("primary_source_id", "")] if row.get("primary_source_id") else []
        authority_level = authority_from_sources(source_ids, "disease")
        regulatory_required = row.get("regulatory_anchor_required", "").lower() == "yes"
        coverage = coverage_from_row(row)
        trust = trust_from_row(row, source_ids)
        if coverage == "complete":
            tier = "source_anchored"
            if regulatory_required and authority_level != "A0":
                usage_scope = ["retrieval", "diagnosis_support", "differential_support", "control_support", "regulatory_boundary"]
            else:
                usage_scope = ["retrieval", "diagnosis_support", "differential_support", "control_support", "gold_candidate"]
        else:
            tier = "partial"
            usage_scope = ["retrieval", "gap_routing", "audit_only"]
        add_entry(
            entries,
            page_id=row.get("disease_id", ""),
            relpath=row.get("page_relpath", ""),
            entity_type="disease",
            source_trust=trust,
            evidence_coverage=coverage,
            usage_scope=usage_scope,
            runtime_tier=tier,
            risk_class="high_regulatory" if regulatory_required else "diagnostic",
            allowed_use=[
                "disease_recall",
                "clinical_summary_with_source_anchor",
                "differential_routing",
                "control_boundary",
            ],
            blocked_use=[
                "standalone_executable_treatment",
                "standalone_dose_course_withdrawal_mrl",
                "standalone_regulatory_action",
            ],
            source_ids=source_ids,
            metadata={
                "coverage_target": row.get("coverage_target", ""),
                "china_standard_required": row.get("china_standard_required", ""),
                "clinical_page_required": row.get("clinical_page_required", ""),
                "regulatory_anchor_required": row.get("regulatory_anchor_required", ""),
            },
        )


def drug_entries(entries):
    for row in read_csv("drug_page_index.csv"):
        relpath = row.get("page_relpath", "") or row.get("path", "")
        if not relpath.startswith("wiki/drugs/"):
            continue
        status = row.get("status", "")
        coverage = coverage_from_row(row)
        if status == "source_anchored_drug_evidence_page":
            tier = "source_anchored"
            usage_scope = ["retrieval", "drug_boundary", "negative_trap", "gold_candidate"]
        elif status in {"partial_drug_evidence_page", "regulatory_boundary_page"}:
            tier = "partial"
            usage_scope = ["retrieval", "gap_routing", "audit_only"] if status == "partial_drug_evidence_page" else ["retrieval", "drug_boundary", "regulatory_boundary"]
        else:
            tier = "candidate_or_incomplete"
            usage_scope = ["retrieval", "gap_routing", "audit_only"]
        sources = split_sources(row.get("sources", ""))
        add_entry(
            entries,
            page_id=row.get("drug_id", "") or row.get("id", ""),
            relpath=relpath,
            entity_type="drug",
            source_trust=trust_from_row(row, sources),
            evidence_coverage=coverage,
            usage_scope=usage_scope,
            runtime_tier=tier,
            risk_class="withdrawal_mrl_residue" if "RC-WITHDRAWAL-MRL-001" in sources else "drug_boundary",
            allowed_use=[
                "drug_recall",
                "drug_boundary_check",
                "candidate_treatment_routing",
                "contraindication_or_interaction_prompting",
            ],
            blocked_use=[
                "standalone_executable_prescription",
                "standalone_dose_course_withdrawal_mrl",
                "standalone_food_safety_or_residue_claim",
            ],
            source_ids=sources,
            metadata={"updated": row.get("updated", "")},
        )


def support_entries(entries):
    for row in read_csv("rule_card_index.csv"):
        add_entry(
            entries,
            page_id=row.get("card_id", ""),
            relpath=row.get("page_relpath", ""),
            entity_type="rule_card",
            source_trust="authoritative",
            evidence_coverage="complete",
            usage_scope=["retrieval", "control_support", "regulatory_boundary", "treatment_boundary", "gold_candidate"],
            runtime_tier="guardrail",
            risk_class="high_regulatory" if row.get("hard_block", "").lower() == "true" else "normal_clinical",
            allowed_use=["hard_blocking", "generation_guardrail", "evaluation_guardrail"],
            source_ids=[],
            metadata={
                "severity": row.get("severity", ""),
                "jurisdiction": row.get("jurisdiction", ""),
                "hard_block": row.get("hard_block", ""),
            },
        )

    for row in read_csv("comparison_index.csv"):
        add_entry(
            entries,
            page_id=row.get("comparison_id", ""),
            relpath=row.get("page_relpath", ""),
            entity_type="comparison",
            source_trust=trust_from_row(row, []),
            evidence_coverage=coverage_from_row(row, default="complete"),
            usage_scope=["retrieval", "differential_support", "gold_candidate"],
            runtime_tier="source_anchored",
            risk_class="diagnostic",
            allowed_use=["differential_diagnosis_routing", "evaluation_expected_coverage"],
        )

    for row in read_csv("syndrome_index.csv"):
        add_entry(
            entries,
            page_id=row.get("syndrome_id", ""),
            relpath=row.get("page_relpath", ""),
            entity_type="syndrome",
            source_trust="authoritative",
            evidence_coverage="complete",
            usage_scope=["retrieval", "diagnosis_support", "differential_support", "gold_candidate"],
            runtime_tier="source_anchored",
            risk_class="diagnostic",
            allowed_use=["syndrome_entrypoint", "case_generation_context", "differential_routing"],
            metadata={"disease_count": row.get("disease_count", "")},
        )

    allowed_synthesis = {
        "swine_case_generation_context",
        "swine_answer_evaluation_rubric",
        "swine_regulatory_blocking_rules_china",
        "swine_drug_and_withdrawal_boundary",
        "swine_dataset_validity_gate",
    }
    for row in read_csv("synthesis_index.csv"):
        sid = row.get("synthesis_id", "")
        if sid not in allowed_synthesis:
            continue
        add_entry(
            entries,
            page_id=sid,
            relpath=row.get("page_relpath", "") or row.get("path", ""),
            entity_type="synthesis",
            source_trust=trust_from_row(row, []),
            evidence_coverage=coverage_from_row(row, default="complete"),
            usage_scope=["retrieval", "control_support", "regulatory_boundary", "treatment_boundary", "gold_candidate"],
            runtime_tier="policy",
            risk_class="high_regulatory" if "regulatory" in sid or "withdrawal" in sid else "normal_clinical",
            allowed_use=["generation_policy", "evaluation_policy", "runtime_boundary"],
            metadata={"title": row.get("title", "")},
        )


def write_exclude_patterns():
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "purpose": "Default denylist for production/evaluation retrieval. The runtime manifest is the allowlist.",
        "exclude_patterns": [
            "raw/**",
            "issues/**",
            "wiki/sessions/**",
            "wiki/exports/**",
            "wiki/knowledge-graph.html",
            "wiki/graph-data.json",
            "wiki/knowledge-graph.md",
            "wiki/evidence_expansions/**",
            "wiki/phase*/**",
            "wiki/synthesis/*treatment_matrix.md",
            "wiki/synthesis/*prescription_matrix.md",
            "wiki/synthesis/sessions/**",
            "exports/*.p0_backup_*",
        ],
        "notes": [
            "Raw files and issue notes remain available for audit or reprocessing, not default runtime retrieval.",
            "Large treatment/prescription matrices should be loaded only by explicit evidence-expansion workflows.",
            "Runtime callers should prefer runtime_core_manifest.json as the positive allowlist.",
        ],
    }
    EXCLUDE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_summary(entries):
    counts = {}
    tiers = {}
    missing = []
    for entry in entries:
        counts[entry["entity_type"]] = counts.get(entry["entity_type"], 0) + 1
        tiers[entry["runtime_tier"]] = tiers.get(entry["runtime_tier"], 0) + 1
        if not entry["path_exists"]:
            missing.append(entry)

    lines = [
        "# Runtime Core Manifest Summary",
        "",
        f"Generated: {datetime.now(TZ).isoformat(timespec='seconds')}",
        "",
        "## Counts By Entity Type",
        "",
    ]
    lines.extend(f"- {key}: {counts[key]}" for key in sorted(counts))
    lines.extend(["", "## Counts By Runtime Tier", ""])
    lines.extend(f"- {key}: {tiers[key]}" for key in sorted(tiers))
    lines.extend(["", "## Missing Paths", ""])
    if missing:
        lines.extend(f"- {x['page_id']} -> {x['path']}" for x in missing)
    else:
        lines.append("- None")
    lines.extend([
        "",
        "## Runtime Principle",
        "",
        "Production and evaluation chains should load this manifest as a positive allowlist.",
        "Files under raw, issues, sessions, graph exports, and large treatment matrices should remain audit/evidence-expansion material unless explicitly requested.",
        "",
    ])
    SUMMARY.write_text("\n".join(lines), encoding="utf-8")


def main():
    """重建 runtime manifest、排除规则和摘要文件。"""
    entries = []
    disease_entries(entries)
    drug_entries(entries)
    support_entries(entries)
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "knowledge_base": str(ROOT),
        "manifest_version": "phase6-phase7-runtime-core-v2",
        "status_contract": {
            "primary_fields": [
                "source_trust",
                "evidence_coverage",
                "usage_scope",
                "authority_level",
                "risk_class"
            ],
            "legacy_fields": [],
            "usability_rule": "A page or fact can be used when source_trust, evidence_coverage, usage_scope, authority_level, and risk_class match the requested task."
        },
        "entries": entries,
    }
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_exclude_patterns()
    write_summary(entries)
    print(json.dumps({
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "exclude_patterns": str(EXCLUDE.relative_to(ROOT)),
        "summary": str(SUMMARY.relative_to(ROOT)),
        "entries": len(entries),
        "missing_paths": sum(1 for x in entries if not x["path_exists"]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
