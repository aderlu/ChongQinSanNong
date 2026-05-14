from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


WIKI_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = WIKI_ROOT.parents[1]
REPORT_JSON = WIKI_ROOT / "issues" / "swine_p0_runtime_validation_2026-05-08.json"
REPORT_MD = WIKI_ROOT / "issues" / "swine_p0_runtime_validation_2026-05-08.md"

EXPECTED_RULE_PATHS = {
    "knowledge_base_file": "knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts.json",
    "references_file": "knowledge/llm_wiki_swine_authoritative/index.md",
    "llm_wiki_index_file": "knowledge/llm_wiki_swine_authoritative/exports/disease_index.csv",
    "llm_wiki_dir": "knowledge/llm_wiki_swine_authoritative",
}
REQUIRED_FINAL_FIELDS = {"answer_json", "evidence_anchors"}
REQUIRED_TEMPLATE_TOKENS = {
    "answer_json",
    "evidence_anchors",
    "source=SRC",
    "source=RC",
}
SOURCE_RE = re.compile(r"\b(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+)\b")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check_config() -> dict[str, Any]:
    config_path = PROJECT_ROOT / "config.json"
    config = load_json(config_path)
    rule_base = config.get("rule_base", {})
    output = config.get("output", {})
    mismatches = {
        key: {"expected": expected, "actual": rule_base.get(key)}
        for key, expected in EXPECTED_RULE_PATHS.items()
        if rule_base.get(key) != expected
    }
    result_csv = str(output.get("result_csv", ""))
    return {
        "config_path": str(config_path),
        "rule_base_ok": not mismatches,
        "rule_base_mismatches": mismatches,
        "result_csv": result_csv,
        "result_csv_ok": "swine" in result_csv and "chicken" not in result_csv,
    }


def check_facts() -> dict[str, Any]:
    facts_path = WIKI_ROOT / "exports" / "knowledge_facts.json"
    facts = load_json(facts_path)
    if not isinstance(facts, list):
        return {"facts_path": str(facts_path), "json_ok": False, "error": "top_level_not_list"}
    bad_questionmark = []
    missing_source = []
    legacy_status_counts: dict[str, int] = {}
    source_ids: set[str] = set()
    for fact in facts:
        if not isinstance(fact, dict):
            continue
        legacy_status = str(fact.get("legacy_evidence_status") or fact.get("evidence_status") or "MISSING")
        legacy_status_counts[legacy_status] = legacy_status_counts.get(legacy_status, 0) + 1
        source = str(fact.get("evidence_source_id") or fact.get("evidence_source") or "")
        if source:
            source_ids.add(source)
        else:
            missing_source.append(str(fact.get("fact_id") or ""))
        payload = json.dumps(fact, ensure_ascii=False)
        if "???" in payload or payload.count("?") >= 5:
            bad_questionmark.append(str(fact.get("fact_id") or ""))
    return {
        "facts_path": str(facts_path),
        "json_ok": True,
        "fact_count": len(facts),
        "bad_questionmark_facts": bad_questionmark,
        "bad_questionmark_count": len(bad_questionmark),
        "missing_source_count": len(missing_source),
        "missing_source_sample": missing_source[:20],
        "legacy_evidence_status_counts": legacy_status_counts,
        "source_id_count": len(source_ids),
    }


def check_templates() -> dict[str, Any]:
    template_dir = PROJECT_ROOT / "prompt_templates"
    texts = {
        path.name: path.read_text(encoding="utf-8")
        for path in template_dir.glob("*.j2")
    }
    joined = "\n".join(texts.values())
    missing_tokens = sorted(token for token in REQUIRED_TEMPLATE_TOKENS if token not in joined)
    chicken_mentions = {
        name: [line for line in text.splitlines() if "鸡病" in line or "关于鸡" in line]
        for name, text in texts.items()
    }
    chicken_mentions = {name: lines for name, lines in chicken_mentions.items() if lines}
    return {
        "template_dir": str(template_dir),
        "required_tokens_ok": not missing_tokens,
        "missing_required_tokens": missing_tokens,
        "chicken_mentions": chicken_mentions,
    }


def check_code_contract() -> dict[str, Any]:
    csv_path = PROJECT_ROOT / "src" / "chicken_data_synthesis" / "infrastructure" / "persistence" / "csv_artifacts.py"
    generation_path = PROJECT_ROOT / "src" / "chicken_data_synthesis" / "application" / "services" / "generation.py"
    csv_text = csv_path.read_text(encoding="utf-8")
    generation_text = generation_path.read_text(encoding="utf-8")
    return {
        "final_fields_ok": all(field in csv_text for field in REQUIRED_FINAL_FIELDS),
        "generation_preserves_answer_json": "payload.get(\"answer_json\"" in generation_text,
        "generation_preserves_evidence_anchors": "payload.get(\"evidence_anchors\"" in generation_text,
        "default_species_swine": "payload.get(\"species\", \"猪\")" in generation_text,
    }


def build_summary() -> dict[str, Any]:
    checks = {
        "config": check_config(),
        "facts": check_facts(),
        "templates": check_templates(),
        "code_contract": check_code_contract(),
    }
    errors: list[str] = []
    if not checks["config"]["rule_base_ok"]:
        errors.append("config_rule_base_not_swine")
    if not checks["config"]["result_csv_ok"]:
        errors.append("config_result_csv_not_swine")
    if not checks["facts"]["json_ok"]:
        errors.append("knowledge_facts_json_invalid")
    if checks["facts"].get("bad_questionmark_count"):
        errors.append("knowledge_facts_questionmark_pollution")
    if not checks["templates"]["required_tokens_ok"]:
        errors.append("generation_templates_missing_p0_tokens")
    if checks["templates"]["chicken_mentions"]:
        errors.append("prompt_templates_still_mention_chicken")
    for key, value in checks["code_contract"].items():
        if not value:
            errors.append(f"code_contract_failed:{key}")
    checks["ok"] = not errors
    checks["errors"] = errors
    return checks


def write_reports(summary: dict[str, Any]) -> None:
    REPORT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Swine P0 runtime validation",
        "",
        f"- ok: {summary['ok']}",
        f"- errors: {', '.join(summary['errors']) if summary['errors'] else 'none'}",
        f"- rule_base_ok: {summary['config']['rule_base_ok']}",
        f"- result_csv: `{summary['config']['result_csv']}`",
        f"- knowledge_facts_json_ok: {summary['facts']['json_ok']}",
        f"- fact_count: {summary['facts'].get('fact_count', 0)}",
        f"- bad_questionmark_count: {summary['facts'].get('bad_questionmark_count', 0)}",
        f"- template_required_tokens_ok: {summary['templates']['required_tokens_ok']}",
        f"- prompt_chicken_mentions: {len(summary['templates']['chicken_mentions'])}",
        f"- final_fields_ok: {summary['code_contract']['final_fields_ok']}",
        f"- generation_preserves_answer_json: {summary['code_contract']['generation_preserves_answer_json']}",
        f"- generation_preserves_evidence_anchors: {summary['code_contract']['generation_preserves_evidence_anchors']}",
        "",
        "This report verifies the P0 runtime contract for swine dataset generation: swine wiki routing, loadable facts, source-first schema tokens, and CSV preservation of structured answer/evidence fields.",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary = build_summary()
    write_reports(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    raise SystemExit(0 if summary["ok"] else 1)


if __name__ == "__main__":
    main()
