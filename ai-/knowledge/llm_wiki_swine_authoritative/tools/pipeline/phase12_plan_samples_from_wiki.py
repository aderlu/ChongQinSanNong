from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues" / "wiki_first_generation_reports"
PLANNED_SAMPLES = EXPORTS / "planned_samples"

RUNTIME_MANIFEST = EXPORTS / "runtime_core_manifest.json"
GOLD_INDEX = EXPORTS / "gold_dataset_readiness_index.csv"
DRUG_ROLE_INDEX = EXPORTS / "drug_gold_role_index.csv"
HARD_BLOCK_RULES = EXPORTS / "exporter_hard_block_rules.json"

TZ = timezone(timedelta(hours=8))
FORBIDDEN_PATH_PARTS = ("raw/", "issues/", "backup", "graph-data.json", "treatment_matrix", "prescription_matrix")

REQUIRED_PLAN_FIELDS = [
    "plan_id",
    "entity_id",
    "entity_type",
    "page_relpath",
    "task_type",
    "ability_layer",
    "source_trust",
    "evidence_coverage",
    "usage_scope",
    "authority_level",
    "risk_class",
    "expected_output_type",
    "training_intent",
    "evidence_depth_class",
    "positive_generation_allowed",
    "negative_trap_allowed",
    "evaluation_allowed",
    "required_rule_cards",
    "question_blueprint",
]


def today_yyyymmdd() -> str:
    return datetime.now(TZ).strftime("%Y%m%d")


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").replace(",", ";").split(";") if item.strip()]


def as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or value == "":
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def normalize_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").upper() or "ENTITY"


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def forbidden_runtime_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(part in normalized for part in FORBIDDEN_PATH_PARTS)


def index_by_page(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("page_relpath", ""): row for row in rows if row.get("page_relpath")}


def derive_rule_cards(row: dict[str, Any], hard_rules: dict[str, Any]) -> list[str]:
    explicit = split_list(row.get("rule_card_ids")) + split_list(row.get("requires_rule_cards"))
    scope = set(split_list(row.get("usage_scope")))
    risk_class = str(row.get("risk_class", ""))
    derived: list[str] = []

    if risk_class == "high_regulatory" or "regulatory_boundary" in scope:
        for rule_name in ("no_source_citation", "unsupported_regulatory_action"):
            derived.extend(hard_rules.get("rules", {}).get(rule_name, {}).get("requires_any_rule_card", []))
    if risk_class in {"drug_boundary", "withdrawal_mrl_residue"} or scope.intersection({"drug_boundary", "negative_trap"}):
        for rule_name in ("no_source_citation", "unsupported_dose"):
            derived.extend(hard_rules.get("rules", {}).get(rule_name, {}).get("requires_any_rule_card", []))
    if risk_class == "withdrawal_mrl_residue":
        derived.extend(hard_rules.get("rules", {}).get("unsupported_withdrawal_mrl", {}).get("requires_any_rule_card", []))
    if explicit or derived:
        derived.append("RC-CITATION-001")
    return unique(explicit + derived)


def merged_entry(manifest_entry: dict[str, Any], gold_rows: dict[str, dict[str, str]], drug_rows: dict[str, dict[str, str]]) -> dict[str, Any]:
    page_relpath = str(manifest_entry.get("path", ""))
    overlay = gold_rows.get(page_relpath) or drug_rows.get(page_relpath) or {}
    entity_id = manifest_entry.get("page_id") or overlay.get("entity_id") or overlay.get("drug_id") or Path(page_relpath).stem
    usage_scope = split_list(manifest_entry.get("usage_scope")) or split_list(overlay.get("usage_scope"))
    return {
        **overlay,
        "entity_id": entity_id,
        "entity_type": manifest_entry.get("entity_type") or overlay.get("entity_type") or ("drug" if overlay.get("drug_id") else ""),
        "page_relpath": page_relpath,
        "source_trust": manifest_entry.get("source_trust") or overlay.get("source_trust", ""),
        "evidence_coverage": manifest_entry.get("evidence_coverage") or overlay.get("evidence_coverage", ""),
        "usage_scope": usage_scope,
        "authority_level": manifest_entry.get("authority_level") or overlay.get("authority_level", ""),
        "risk_class": manifest_entry.get("risk_class") or overlay.get("risk_class", ""),
        "source_ids": split_list(manifest_entry.get("source_ids")) or split_list(overlay.get("source_ids")),
        "positive_generation_allowed": as_bool(overlay.get("positive_generation_allowed")),
        "negative_trap_allowed": as_bool(overlay.get("negative_trap_allowed")),
        "evaluation_allowed": as_bool(overlay.get("evaluation_allowed")),
        "blocked_question_types": split_list(manifest_entry.get("blocked_question_types")) or split_list(overlay.get("blocked_question_types")),
        "allowed_question_types": split_list(manifest_entry.get("allowed_question_types")) or split_list(overlay.get("allowed_question_types")),
        "rule_card_ids": split_list(overlay.get("rule_card_ids")),
        "requires_rule_cards": split_list(overlay.get("requires_rule_cards")),
        "page_gold_ready": as_bool(overlay.get("page_gold_ready")),
        "evidence_units": to_int(overlay.get("evidence_units"), 0),
    }


def evidence_depth_class(row: dict[str, Any]) -> str:
    source_ids = set(split_list(row.get("source_ids")))
    evidence_units = to_int(row.get("evidence_units"), 0)
    page_gold_ready = as_bool(row.get("page_gold_ready"))
    non_toc_sources = {source_id for source_id in source_ids if source_id and source_id != "SRC-0001"}
    if evidence_units <= 0 or (source_ids and not non_toc_sources):
        return "toc_only"
    if page_gold_ready and evidence_units >= 3 and non_toc_sources:
        return "substantive"
    return "thin"


def training_intent_for_layer(row: dict[str, Any], ability_layer: str) -> str:
    depth = evidence_depth_class(row)
    if ability_layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}:
        return "boundary_sft"
    if ability_layer == "L7_judge_calibration":
        return "eval_only"
    if depth != "substantive":
        return "eval_only"
    return "positive_sft"


def candidate_layers(row: dict[str, Any]) -> list[tuple[str, str, str]]:
    scope = set(split_list(row.get("usage_scope")))
    risk_class = str(row.get("risk_class", ""))
    source_trust = str(row.get("source_trust", ""))
    coverage = str(row.get("evidence_coverage", ""))

    if source_trust == "needs_source_check":
        return [("source_audit", "L7_judge_calibration", "audit_or_eval")]
    if coverage in {"partial", "minimal"}:
        return [("retrieval_gap_check", "L1_retrieval_grounded", "retrieval_gap_or_eval")]

    layers: list[tuple[str, str, str]] = []
    if "retrieval" in scope:
        layers.append(("retrieval_grounded", "L1_retrieval_grounded", "grounded_answer"))
    if "diagnosis_support" in scope:
        layers.append(("diagnosis_support", "L2_diagnosis_support", "diagnostic_boundary_answer"))
    if "differential_support" in scope:
        layers.append(("differential_support", "L3_differential_support", "differential_boundary_answer"))
    if "control_support" in scope:
        layers.append(("control_boundary", "L4_control_boundary", "control_boundary_answer"))
    if scope.intersection({"drug_boundary", "negative_trap"}):
        layers.append(("drug_boundary_negative", "L5_drug_boundary_negative", "boundary_or_refusal"))
    if risk_class == "high_regulatory" or "regulatory_boundary" in scope:
        layers.append(("regulatory_boundary", "L6_regulatory_guardrail", "boundary_or_refusal"))
    return unique_layer_tuples(layers) or [("retrieval_grounded", "L1_retrieval_grounded", "grounded_answer")]


def unique_layer_tuples(layers: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[str] = set()
    result: list[tuple[str, str, str]] = []
    for layer in layers:
        if layer[1] not in seen:
            result.append(layer)
            seen.add(layer[1])
    return result


def positive_allowed_for_layer(row: dict[str, Any], ability_layer: str) -> bool:
    if str(row.get("source_trust")) == "needs_source_check":
        return False
    if str(row.get("evidence_coverage")) in {"partial", "minimal"}:
        return False
    if training_intent_for_layer(row, ability_layer) != "positive_sft":
        return False
    if ability_layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail", "L7_judge_calibration"}:
        return False
    return as_bool(row.get("positive_generation_allowed"))


def build_blueprint(row: dict[str, Any], task_type: str, ability_layer: str) -> dict[str, Any]:
    scope = split_list(row.get("usage_scope"))
    risk_class = str(row.get("risk_class", ""))
    blocked = split_list(row.get("blocked_question_types"))
    depth = evidence_depth_class(row)
    if ability_layer == "L6_regulatory_guardrail":
        intent = "ask_regulatory_action_boundary"
        must_ask_about = ["reporting_boundary", "movement_boundary", "disposal_boundary"]
        must_not_ask_about = ["unsupported_culling_conclusion", "unsupported_quarantine_conclusion"]
    elif ability_layer == "L5_drug_boundary_negative":
        intent = "ask_drug_use_boundary_or_trap"
        must_ask_about = ["dose_course_boundary", "withdrawal_or_mrl_boundary", "label_or_a0_source_check"]
        must_not_ask_about = ["unsupported_dose", "unsupported_withdrawal_mrl"]
    elif ability_layer == "L7_judge_calibration":
        intent = "audit_source_or_generation_boundary"
        must_ask_about = ["source_trust", "evidence_coverage", "runtime_allowlist"]
        must_not_ask_about = ["new_biomedical_fact_generation", "positive_sft_generation"]
    elif task_type == "retrieval_gap_check" or depth != "substantive":
        intent = "ask_retrieval_or_gap_boundary"
        must_ask_about = ["available_source_anchored_summary", "known_gap"]
        must_not_ask_about = ["unsupported_positive_generation", "standalone_prescription", "uncited_differential_detail"]
    else:
        intent = f"ask_{task_type}"
        must_ask_about = scope[:3] or [task_type]
        must_not_ask_about = blocked[:3] or ["unsupported_claims"]

    return {
        "intent": intent,
        "must_ask_about": must_ask_about,
        "must_not_ask_about": must_not_ask_about,
        "risk_boundary": risk_class,
    }


def build_plans(date: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = read_json(RUNTIME_MANIFEST)
    gold_rows = index_by_page(read_csv(GOLD_INDEX))
    drug_rows = index_by_page(read_csv(DRUG_ROLE_INDEX))
    hard_rules = read_json(HARD_BLOCK_RULES)

    manifest_entries = manifest.get("entries", [])
    plans: list[dict[str, Any]] = []
    skipped_forbidden: list[str] = []

    for entry in manifest_entries:
        page_relpath = str(entry.get("path", ""))
        if not page_relpath or forbidden_runtime_path(page_relpath):
            skipped_forbidden.append(page_relpath)
            continue
        if entry.get("path_exists") is False:
            continue

        row = merged_entry(entry, gold_rows, drug_rows)
        rule_cards = derive_rule_cards(row, hard_rules)
        entity_id = str(row["entity_id"])
        depth_class = evidence_depth_class(row)

        for task_type, ability_layer, expected_output_type in candidate_layers(row):
            sequence = len([plan for plan in plans if plan["entity_id"] == entity_id]) + 1
            positive_allowed = positive_allowed_for_layer(row, ability_layer)
            training_intent = training_intent_for_layer(row, ability_layer)
            plan = {
                "plan_id": f"PLAN-{normalize_id(entity_id)}-{sequence:04d}",
                "entity_id": entity_id,
                "entity_type": row["entity_type"],
                "page_relpath": row["page_relpath"],
                "task_type": task_type,
                "ability_layer": ability_layer,
                "source_trust": row["source_trust"],
                "evidence_coverage": row["evidence_coverage"],
                "usage_scope": split_list(row["usage_scope"]),
                "authority_level": row["authority_level"],
                "risk_class": row["risk_class"],
                "expected_output_type": expected_output_type,
                "training_intent": training_intent,
                "evidence_depth_class": depth_class,
                "positive_generation_allowed": positive_allowed,
                "negative_trap_allowed": as_bool(row.get("negative_trap_allowed")),
                "evaluation_allowed": as_bool(row.get("evaluation_allowed")) or ability_layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail", "L7_judge_calibration"},
                "required_rule_cards": rule_cards,
                "question_blueprint": build_blueprint(row, task_type, ability_layer),
                "provenance": {
                    "runtime_manifest": RUNTIME_MANIFEST.relative_to(ROOT).as_posix(),
                    "runtime_page_id": entry.get("page_id"),
                    "source_ids": split_list(row.get("source_ids")),
                    "planner_date": date,
                },
            }
            plans.append(plan)

    summary = summarize(plans, manifest_entries, skipped_forbidden)
    return plans, summary


def summarize(plans: list[dict[str, Any]], manifest_entries: list[dict[str, Any]], skipped_forbidden: list[str]) -> dict[str, Any]:
    missing_fields: list[str] = []
    for plan in plans:
        for field in REQUIRED_PLAN_FIELDS:
            if field not in plan or plan[field] in ("", None):
                missing_fields.append(plan["plan_id"])
                break
    forbidden_paths = [plan["page_relpath"] for plan in plans if forbidden_runtime_path(str(plan["page_relpath"]))]
    high_risk_missing_rule_cards = [
        plan["plan_id"]
        for plan in plans
        if plan.get("risk_class") in {"high_regulatory", "withdrawal_mrl_residue", "drug_boundary"} and not plan.get("required_rule_cards")
    ]
    disallowed_positive = [
        plan["plan_id"]
        for plan in plans
        if plan.get("positive_generation_allowed") is True
        and (plan.get("evidence_coverage") in {"partial", "minimal"} or plan.get("source_trust") == "needs_source_check")
    ]
    toc_or_thin_positive = [
        plan["plan_id"]
        for plan in plans
        if plan.get("training_intent") == "positive_sft"
        and plan.get("evidence_depth_class") != "substantive"
    ]
    runtime_paths = {str(entry.get("path")) for entry in manifest_entries}
    non_runtime_paths = [plan["page_relpath"] for plan in plans if plan["page_relpath"] not in runtime_paths]
    ability_counts = Counter(str(plan["ability_layer"]) for plan in plans)
    intent_counts = Counter(str(plan.get("training_intent") or "") for plan in plans)
    depth_counts = Counter(str(plan.get("evidence_depth_class") or "") for plan in plans)

    acceptance = {
        "all_plans_from_runtime_manifest": not non_runtime_paths,
        "no_forbidden_paths_in_plan": not forbidden_paths,
        "all_plans_have_ability_layer": all(bool(plan.get("ability_layer")) for plan in plans),
        "high_risk_plans_have_required_rule_cards": not high_risk_missing_rule_cards,
        "limited_or_source_check_not_positive": not disallowed_positive,
        "positive_sft_requires_substantive_evidence": not toc_or_thin_positive,
        "passed": not (missing_fields or forbidden_paths or high_risk_missing_rule_cards or disallowed_positive or toc_or_thin_positive or non_runtime_paths),
    }
    return {
        "generated_at": now_iso(),
        "total_manifest_entries": len(manifest_entries),
        "total_plans": len(plans),
        "unique_pages_planned": len({plan["page_relpath"] for plan in plans}),
        "ability_layer_counts": dict(sorted(ability_counts.items())),
        "training_intent_counts": dict(sorted(intent_counts.items())),
        "evidence_depth_counts": dict(sorted(depth_counts.items())),
        "skipped_forbidden_manifest_paths": skipped_forbidden,
        "checks": {
            "missing_required_fields": missing_fields,
            "forbidden_paths": forbidden_paths,
            "high_risk_missing_rule_cards": high_risk_missing_rule_cards,
            "limited_or_source_check_positive": disallowed_positive,
            "toc_or_thin_positive": toc_or_thin_positive,
            "non_runtime_paths": non_runtime_paths,
        },
        "acceptance": acceptance,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_report_md(path: Path, summary: dict[str, Any], plan_relpath: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ability_lines = [f"- {layer}: {count}" for layer, count in summary["ability_layer_counts"].items()]
    intent_lines = [f"- {intent}: {count}" for intent, count in summary.get("training_intent_counts", {}).items()]
    depth_lines = [f"- {depth}: {count}" for depth, count in summary.get("evidence_depth_counts", {}).items()]
    checks = summary["checks"]
    content = [
        "# Phase 12 Wiki Sample Planning Report",
        "",
        f"- Generated at: {summary['generated_at']}",
        f"- Planned samples: {summary['total_plans']}",
        f"- Unique pages: {summary['unique_pages_planned']}",
        f"- Plan output: `{plan_relpath}`",
        f"- Acceptance passed: {summary['acceptance']['passed']}",
        "",
        "## Ability Layers",
        "",
        *(ability_lines or ["- none: 0"]),
        "",
        "## Training Intents",
        "",
        *(intent_lines or ["- none: 0"]),
        "",
        "## Evidence Depth",
        "",
        *(depth_lines or ["- none: 0"]),
        "",
        "## Checks",
        "",
        f"- Missing required fields: {len(checks['missing_required_fields'])}",
        f"- Forbidden paths in plan: {len(checks['forbidden_paths'])}",
        f"- High-risk plans missing rule cards: {len(checks['high_risk_missing_rule_cards'])}",
        f"- Limited/source-check plans incorrectly positive: {len(checks['limited_or_source_check_positive'])}",
        f"- Positive SFT plans without substantive evidence: {len(checks['toc_or_thin_positive'])}",
        f"- Non-runtime paths: {len(checks['non_runtime_paths'])}",
    ]
    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 12: plan wiki-first sample tasks from runtime allowlist.")
    parser.add_argument("--date", default=today_yyyymmdd(), help="Output date stamp in YYYYMMDD format.")
    parser.add_argument("--limit", type=int, default=0, help="Optional maximum number of plans to write for smoke tests.")
    args = parser.parse_args()

    plans, summary = build_plans(args.date)
    if args.limit and args.limit > 0:
        plans = plans[: args.limit]
        summary = summarize(plans, read_json(RUNTIME_MANIFEST).get("entries", []), [])
    plan_path = PLANNED_SAMPLES / f"wiki_sample_plan_{args.date}.jsonl"
    report_json = ISSUES / f"phase12_plan_samples_{args.date}.json"
    report_md = ISSUES / f"phase12_plan_samples_{args.date}.md"

    write_jsonl(plan_path, plans)
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "phase": "phase12_plan_samples_from_wiki",
        "inputs": {
            "runtime_manifest": RUNTIME_MANIFEST.relative_to(ROOT).as_posix(),
            "gold_dataset_readiness_index": GOLD_INDEX.relative_to(ROOT).as_posix(),
            "drug_gold_role_index": DRUG_ROLE_INDEX.relative_to(ROOT).as_posix(),
            "exporter_hard_block_rules": HARD_BLOCK_RULES.relative_to(ROOT).as_posix(),
        },
        "outputs": {
            "planned_samples_file": plan_path.relative_to(ROOT).as_posix(),
            "report_json": report_json.relative_to(ROOT).as_posix(),
            "report_md": report_md.relative_to(ROOT).as_posix(),
        },
        **summary,
    }
    report["passed"] = report["acceptance"]["passed"]
    report["planned_samples"] = report["total_plans"]
    report["output"] = plan_path.relative_to(ROOT).as_posix()
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report_md(report_md, report, plan_path.relative_to(ROOT).as_posix())

    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
