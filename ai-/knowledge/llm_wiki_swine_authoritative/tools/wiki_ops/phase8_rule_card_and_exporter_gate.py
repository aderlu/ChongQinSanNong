from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
RULE_CARDS = WIKI / "rule_cards"
SYNTHESIS = WIKI / "synthesis"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
MANIFEST = EXPORTS / "runtime_core_manifest.json"
RULE_CARD_INDEX = EXPORTS / "rule_card_index.csv"
EXPORTER_RULES = EXPORTS / "exporter_hard_block_rules.json"
REPORT_JSON = ISSUES / "phase8_rule_card_exporter_gate_2026-05-09.json"
REPORT_MD = ISSUES / "phase8_rule_card_exporter_gate_2026-05-09.md"
TZ = timezone(timedelta(hours=8))

REQUIRED_CARDS = [
    "RC-DX-001",
    "RC-DRUG-001",
    "RC-WITHDRAWAL-MRL-001",
    "RC-DISEASE-REGULATORY-001",
    "RC-CITATION-001",
    "RC-TRAIN-READY-001",
    "RC-EVAL-RUBRIC-001",
]

HARD_BLOCK_RULES = {
    "unsupported_dose": {
        "requires_any_rule_card": ["RC-DRUG-001"],
        "trigger_terms": ["剂量", "用量", "疗程", "给药", "dose", "course", "route", "mg/kg", "mL/kg"],
        "block_when": "No source/fact/rule anchor covers product, species, formulation, route, dose/course and jurisdiction.",
    },
    "unsupported_withdrawal_mrl": {
        "requires_any_rule_card": ["RC-WITHDRAWAL-MRL-001"],
        "trigger_terms": ["休药期", "停药期", "MRL", "残留", "屠宰", "可食", "withdrawal", "residue"],
        "block_when": "No A0 or label-level equivalent source covers product, species, tissue/food class and jurisdiction.",
    },
    "unsupported_regulatory_action": {
        "requires_any_rule_card": ["RC-DISEASE-REGULATORY-001", "RC-REGULATORY-CURRENT-001"],
        "trigger_terms": ["上报", "扑杀", "封锁", "检疫", "调运", "无害化", "report", "quarantine", "movement"],
        "block_when": "No current official/regulatory source covers the requested jurisdiction and action.",
    },
    "single_test_causality_overclaim": {
        "requires_any_rule_card": ["RC-DX-001", "RC-EVAL-RUBRIC-001"],
        "trigger_terms": ["PCR", "Ct", "抗体阳性", "抗原阳性", "检出", "阳性", "single test"],
        "block_when": "Answer asserts definitive causality without sample, method, timing, clinical fit and differential boundary.",
    },
    "no_source_citation": {
        "requires_any_rule_card": ["RC-CITATION-001"],
        "trigger_terms": ["诊断", "治疗", "用药", "休药期", "上报", "食品安全", "public health"],
        "block_when": "Any high-value answer lacks source_id, fact_id, URL/page/table anchor or rule card citation.",
    },
    "source_level_mismatch": {
        "requires_any_rule_card": ["RC-EVAL-RUBRIC-001", "RC-REGULATORY-CURRENT-001"],
        "trigger_terms": ["中国", "合规", "标签", "禁用", "休药期", "MRL", "残留", "扑杀"],
        "block_when": "SRC/A1/A2 or textbook evidence is used for an A0/label-level regulatory, withdrawal, MRL, residue, food-safety or compulsory-action claim.",
    },
}


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    front: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            front[key.strip()] = value.strip()
    return front, text[end + 5 :]


def title_from_body(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def read_rule_cards() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(RULE_CARDS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        front, body = split_frontmatter(text)
        card_id = front.get("card_id") or path.stem
        rows.append(
            {
                "card_id": card_id,
                "title": title_from_body(body) or card_id,
                "severity": front.get("severity", ""),
                "jurisdiction": front.get("jurisdiction", ""),
                "hard_block": front.get("hard_block", ""),
                "page_relpath": path.relative_to(ROOT).as_posix(),
            }
        )
    return rows


def write_rule_card_index(rows: list[dict[str, str]]) -> None:
    with RULE_CARD_INDEX.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["card_id", "title", "severity", "jurisdiction", "hard_block", "page_relpath"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def manifest_entries() -> list[dict[str, object]]:
    if not MANIFEST.exists():
        return []
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = payload.get("entries", [])
    return entries if isinstance(entries, list) else []


def pages_requiring_rules(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    records = []
    for entry in entries:
        entity_type = str(entry.get("entity_type", ""))
        if entity_type == "rule_card":
            continue
        path = ROOT / str(entry.get("path", ""))
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        required: set[str] = set()
        if entity_type == "drug":
            required.add("RC-DRUG-001")
        if entry.get("risk_class") in {"withdrawal_mrl_residue", "food_safety"}:
            required.add("RC-WITHDRAWAL-MRL-001")
        if entry.get("risk_class") == "high_regulatory":
            required.add("RC-DISEASE-REGULATORY-001")
        usage_scope = set(entry.get("usage_scope", []) or [])
        if usage_scope.intersection({"gold_candidate", "diagnosis_support", "differential_support", "control_support"}):
            required.add("RC-CITATION-001")
        missing = sorted(card for card in required if card not in text and card not in str(entry.get("rule_card_ids", "")))
        if required:
            records.append(
                {
                    "page_id": entry.get("page_id", ""),
                    "path": entry.get("path", ""),
                    "entity_type": entry.get("entity_type", ""),
                    "risk_class": entry.get("risk_class", ""),
                    "required": sorted(required),
                    "missing": missing,
                }
            )
    return records


def write_exporter_rules() -> None:
    payload = {
        "generated_at": now(),
        "purpose": "Phase 8 exporter/evaluator hard-block checks for swine LLM wiki dataset production.",
        "primary_gate_fields": ["source_trust", "evidence_coverage", "usage_scope", "authority_level", "risk_class"],
        "rules": HARD_BLOCK_RULES,
    }
    EXPORTER_RULES.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    rule_rows = read_rule_cards()
    write_rule_card_index(rule_rows)
    write_exporter_rules()
    card_ids = {row["card_id"] for row in rule_rows}
    missing_required_cards = [card for card in REQUIRED_CARDS if card not in card_ids]
    page_records = pages_requiring_rules(manifest_entries())
    missing_page_anchors = [record for record in page_records if record["missing"]]
    synthesis_targets = [
        "swine_answer_evaluation_rubric.md",
        "swine_case_generation_context.md",
        "swine_regulatory_blocking_rules_china.md",
        "swine_drug_and_withdrawal_boundary.md",
    ]
    synthesis_anchor_records = []
    for name in synthesis_targets:
        path = SYNTHESIS / name
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        synthesis_anchor_records.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "exists": path.exists(),
                "has_eval_rubric": "RC-EVAL-RUBRIC-001" in text,
                "has_synthesis_scope": "RC-SYNTHESIS-SCOPE-001" in text,
                "has_regulatory_current": "RC-REGULATORY-CURRENT-001" in text,
            }
        )
    report = {
        "generated_at": now(),
        "required_cards": REQUIRED_CARDS,
        "rule_card_count": len(rule_rows),
        "hard_block_count": sum(1 for row in rule_rows if row.get("hard_block", "").lower() == "true"),
        "missing_required_cards": missing_required_cards,
        "runtime_pages_requiring_rules": len(page_records),
        "runtime_pages_missing_rule_anchors": len(missing_page_anchors),
        "missing_rule_anchor_sample": missing_page_anchors[:30],
        "synthesis_anchor_records": synthesis_anchor_records,
        "outputs": {
            "rule_card_index": RULE_CARD_INDEX.relative_to(ROOT).as_posix(),
            "exporter_hard_block_rules": EXPORTER_RULES.relative_to(ROOT).as_posix(),
        },
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Phase 8 Rule Card And Exporter Gate Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Rule cards indexed: {report['rule_card_count']}",
        f"- Hard-block cards: {report['hard_block_count']}",
        f"- Missing required cards: {report['missing_required_cards']}",
        f"- Runtime pages requiring rule checks: {report['runtime_pages_requiring_rules']}",
        f"- Runtime pages missing expected page-level rule anchors: {report['runtime_pages_missing_rule_anchors']}",
        "",
        "## Exporter Hard Blocks",
        "",
    ]
    for rule_id, rule in HARD_BLOCK_RULES.items():
        lines.append(f"- `{rule_id}`: cards={';'.join(rule['requires_any_rule_card'])}; block_when={rule['block_when']}")
    lines.extend(["", "## Outputs", "", f"- `{report['outputs']['rule_card_index']}`", f"- `{report['outputs']['exporter_hard_block_rules']}`", ""])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
