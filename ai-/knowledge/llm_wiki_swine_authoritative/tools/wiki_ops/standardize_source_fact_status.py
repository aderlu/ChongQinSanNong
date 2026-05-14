from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
TZ = timezone(timedelta(hours=8))

SOURCE_STATUS_CSV = EXPORTS / "source_authority_status_index.csv"
FACT_STATUS_JSON = EXPORTS / "knowledge_facts_status_index.json"
REPORT_JSON = ISSUES / "source_fact_authority_status_audit_2026-05-09.json"
REPORT_MD = ISSUES / "source_fact_authority_status_audit_2026-05-09.md"

HIGH_RISK_PATTERNS = {
    "withdrawal_mrl_residue": ["休药期", "MRL", "残留", "withdrawal", "residue"],
    "food_safety": ["食品安全", "肉品", "可食", "屠宰", "edible", "food safety"],
    "high_regulatory": ["扑杀", "检疫", "调运", "报告", "封锁", "一类动物疫病", "二类动物疫病", "movement", "quarantine"],
    "drug_boundary": ["剂量", "用量", "疗程", "给药", "处方", "dose", "course", "route"],
}


def read_csv(name: str) -> list[dict[str, str]]:
    path = EXPORTS / name
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def authority_from_source_id(source_id: str) -> str:
    if source_id.startswith("A0-"):
        return "A0"
    if source_id.startswith("A1-"):
        return "A1"
    if source_id.startswith("A2-"):
        return "A2"
    if source_id.startswith("SRC-"):
        return "SRC"
    if source_id.startswith("RC-"):
        return "RC"
    if source_id.startswith("RULE-"):
        return "RULE"
    return ""


def legacy_status(row: dict[str, object]) -> str:
    return str(row.get("legacy_evidence_status", "") or row.get("evidence_status", ""))


def split_frontmatter(text: str) -> tuple[list[str], str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            front = text[4:end].splitlines()
            return front, text[end + 5 :]
    return [], text


def render_frontmatter(front: list[str], body: str) -> str:
    if not front:
        return body
    return "---\n" + "\n".join(front).rstrip() + "\n---\n" + body


def front_has(front: list[str], key: str) -> bool:
    prefix = f"{key}:"
    return any(line.startswith(prefix) for line in front)


def insert_after(front: list[str], after_key: str, new_line: str) -> list[str]:
    if not front:
        return [new_line]
    for idx, line in enumerate(front):
        if line.startswith(f"{after_key}:"):
            return front[: idx + 1] + [new_line] + front[idx + 1 :]
    return front + [new_line]


def ensure_source_page_contract(path: Path, source_id: str, authority_level: str) -> bool:
    text = path.read_text(encoding="utf-8")
    front, body = split_frontmatter(text)
    changed = False
    if front:
        if not front_has(front, "source_status"):
            front = insert_after(front, "evidence_status", "source_status: source_anchored")
            changed = True
        if authority_level and not front_has(front, "authority_level"):
            front = insert_after(front, "source_status", f"authority_level: {authority_level}")
            changed = True
    if "## 可支持结论" not in body:
        body = body.rstrip() + "\n\n## 可支持结论\n\n- 支持范围以本页来源摘要、URL/path、页码/章节、表格和已登记 facts 为准。\n"
        changed = True
    if "## 不得外推边界" not in body:
        body = body.rstrip() + "\n\n## 不得外推边界\n\n- 不得超出 `authority_level` 和原文明确支持范围；剂量、疗程、休药期、MRL、残留、食品安全、检疫、扑杀、调运、报告等高风险结论必须另有 A0 或标签级等价来源支持。\n"
        changed = True
    if changed:
        path.write_text(render_frontmatter(front, body), encoding="utf-8")
    return changed


def risk_class_for_fact(fact: dict[str, object]) -> str:
    text = " ".join(str(fact.get(key, "")) for key in ["predicate", "object", "fact_type"])
    for risk, patterns in HIGH_RISK_PATTERNS.items():
        if any(pattern.lower() in text.lower() for pattern in patterns):
            return risk
    if "diagnos" in text.lower() or "检测" in text or "诊断" in text:
        return "diagnostic"
    return "normal_clinical"


def task_use_for(source_status: str, fact_validity: str, authority_level: str, risk_class: str) -> str:
    if source_status != "source_anchored" or fact_validity != "valid":
        return "blocked"
    if risk_class in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"}:
        return "eval_ready" if authority_level == "A0" else "generation_ready_limited"
    if risk_class == "drug_boundary":
        return "generation_ready_limited"
    return "train_ready"


def source_trust_for(source_status: str, authority_level: str) -> str:
    if source_status != "source_anchored":
        return "untrusted"
    if authority_level in {"A0", "A1", "A2", "SRC"}:
        return "authoritative"
    if authority_level in {"RC", "RULE"}:
        return "governance"
    return "authoritative"


def evidence_coverage_for(source_status: str, fact_validity: str, fact: dict[str, object]) -> str:
    if source_status != "source_anchored" or fact_validity != "valid":
        return "gap"
    if str(fact.get("target_page", "")).startswith("wiki/"):
        return "complete"
    return "partial"


def usage_scope_for(task_use_status: str) -> list[str]:
    if task_use_status == "blocked":
        return ["audit_only"]
    if task_use_status == "eval_ready":
        return ["retrieval", "evaluation_only"]
    if task_use_status == "generation_ready_limited":
        return ["retrieval", "bounded_generation"]
    return ["retrieval", "gold_candidate"]


def fact_validity_for(fact: dict[str, object], source_status: str) -> str:
    subject = str(fact.get("subject", ""))
    obj = str(fact.get("object", ""))
    if "\ufffd" in subject or "\ufffd" in obj:
        return "encoding_damaged"
    if not subject or not obj:
        return "insufficient_anchor"
    if source_status != "source_anchored":
        return "insufficient_anchor"
    return "valid"


def normalize_facts(source_authority: dict[str, str], source_paths: set[str]) -> tuple[list[dict[str, object]], dict[str, int]]:
    facts_path = EXPORTS / "knowledge_facts.json"
    facts = json.loads(facts_path.read_text(encoding="utf-8")) if facts_path.exists() else []
    normalized = []
    counts: dict[str, int] = {}
    for fact in facts:
        source_id = str(fact.get("evidence_source_id") or fact.get("source_id") or "")
        authority_level = source_authority.get(source_id) or authority_from_source_id(source_id)
        source_status = "source_anchored" if source_id and (source_id in source_authority or source_id.startswith(("RC-", "RULE-"))) else "source_missing"
        fact_validity = fact_validity_for(fact, source_status)
        risk_class = risk_class_for_fact(fact)
        task_use_status = task_use_for(source_status, fact_validity, authority_level, risk_class)
        source_trust = str(fact.get("source_trust") or source_trust_for(source_status, authority_level))
        evidence_coverage = str(fact.get("evidence_coverage") or evidence_coverage_for(source_status, fact_validity, fact))
        usage_scope = fact.get("usage_scope")
        if not isinstance(usage_scope, list) or not usage_scope:
            usage_scope = usage_scope_for(task_use_status)
        item = dict(fact)
        legacy_evidence_status = item.pop("evidence_status", "")
        item.update(
            {
                "source_trust": source_trust,
                "evidence_coverage": evidence_coverage,
                "usage_scope": usage_scope,
                "source_status": source_status,
                "fact_validity": fact_validity,
                "authority_level": authority_level,
                "risk_class": risk_class,
                "task_use_status": task_use_status,
                "legacy_evidence_status": legacy_evidence_status,
            }
        )
        normalized.append(item)
        counts[task_use_status] = counts.get(task_use_status, 0) + 1
    FACT_STATUS_JSON.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    return normalized, counts


def main() -> None:
    source_rows = read_csv("source_index.csv")
    status_rows = []
    source_authority: dict[str, str] = {}
    changed_pages = 0
    for row in source_rows:
        source_id = row.get("source_id", "")
        relpath = row.get("relpath") or row.get("page_relpath", "")
        path = ROOT / relpath if relpath else Path()
        authority_level = authority_from_source_id(source_id)
        path_exists = bool(relpath and path.exists())
        source_status = "source_anchored" if path_exists and source_id else "source_missing"
        if source_id:
            source_authority[source_id] = authority_level or "SRC"
        if path_exists and path.suffix.lower() == ".md":
            if ensure_source_page_contract(path, source_id, authority_level or "SRC"):
                changed_pages += 1
        status_rows.append(
            {
                "source_id": source_id,
                "title": row.get("title", ""),
                "authority_level": authority_level or "SRC",
                "source_status": source_status,
                "fact_validity": "valid" if source_status == "source_anchored" else "insufficient_anchor",
                "legacy_evidence_status": legacy_status(row),
                "relpath": relpath,
                "path_exists": str(path_exists).lower(),
            }
        )
    write_csv(
        SOURCE_STATUS_CSV,
        status_rows,
        [
            "source_id",
            "title",
            "authority_level",
            "source_status",
            "fact_validity",
            "legacy_evidence_status",
            "relpath",
            "path_exists",
        ],
    )
    normalized_facts, task_counts = normalize_facts(source_authority, {r["source_id"] for r in status_rows})
    missing_sources = sum(1 for r in status_rows if r["source_status"] != "source_anchored")
    invalid_facts = sum(1 for f in normalized_facts if f["fact_validity"] != "valid")
    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "source_rows": len(status_rows),
        "source_pages_changed": changed_pages,
        "source_missing": missing_sources,
        "facts": len(normalized_facts),
        "invalid_facts": invalid_facts,
        "task_use_counts": task_counts,
        "outputs": {
            "source_status_csv": SOURCE_STATUS_CSV.relative_to(ROOT).as_posix(),
            "fact_status_json": FACT_STATUS_JSON.relative_to(ROOT).as_posix(),
        },
    }
    REPORT_JSON.write_text(json.dumps({"summary": summary}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Source And Fact Authority Status Audit / Phase 5",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Source rows: {summary['source_rows']}",
        f"- Source pages changed: {summary['source_pages_changed']}",
        f"- Source missing: {summary['source_missing']}",
        f"- Facts: {summary['facts']}",
        f"- Invalid facts: {summary['invalid_facts']}",
        "",
        "## Task Use Counts",
        "",
    ]
    for key in sorted(task_counts):
        lines.append(f"- {key}: {task_counts[key]}")
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- `{summary['outputs']['source_status_csv']}`",
            f"- `{summary['outputs']['fact_status_json']}`",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
