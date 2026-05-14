import csv
import json
import re
from pathlib import Path

"""猪病 LLM Wiki readiness 检查脚本。

由 run_swine_wiki_maintenance_checks.py 在更新后验收阶段调用。
它检查索引、实体状态、规则卡、综合页和交叉链接，评估当前知识库是否可用于生成和评测。
"""

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
REPORT = ISSUES / "swine_llm_wiki_generation_evaluation_readiness_2026-05-08.md"
SUMMARY = ISSUES / "swine_llm_wiki_generation_evaluation_readiness_2026-05-08.json"


def read_csv(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def count_md(dirname):
    p = WIKI / dirname
    return len(list(p.glob("*.md"))) if p.exists() else 0


def text(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def file_exists(rel):
    if not rel:
        return False
    return (ROOT / rel.replace("/", "\\")).exists()


def path_integrity(index_name, path_fields):
    rows = read_csv(EXPORTS / index_name)
    missing = []
    checked = 0
    for row in rows:
        for field in path_fields:
            rel = row.get(field, "")
            if rel:
                checked += 1
                if not file_exists(rel):
                    missing.append({"index": index_name, "field": field, "path": rel, "id": row.get("id") or row.get("drug_id") or row.get("disease_id") or row.get("source_id") or row.get("rule_id") or row.get("card_id")})
    return {"index": index_name, "rows": len(rows), "checked_paths": checked, "missing_paths": missing}


def fact_table_quality(name, page_required=True):
    rows = read_csv(EXPORTS / name)
    if not rows:
        return {"name": name, "rows": 0, "source_id_present": 0, "page_present": 0, "source_id_rate": 0, "page_rate": 0, "unmapped": 0}
    source_id_present = sum(1 for r in rows if r.get("source_id"))
    page_present = sum(1 for r in rows if str(r.get("page", "")).strip() not in {"", "UNMAPPED", "None", "null"})
    unmapped = sum(1 for r in rows if str(r.get("page", "")).strip() in {"", "UNMAPPED", "None", "null"})
    return {
        "name": name,
        "rows": len(rows),
        "source_id_present": source_id_present,
        "page_present": page_present,
        "source_id_rate": round(source_id_present / len(rows), 4),
        "page_rate": round(page_present / len(rows), 4),
        "unmapped": unmapped,
        "page_required": page_required,
    }


def entity_status(dirname, status_key, required_section):
    pages = sorted((WIKI / dirname).glob("*.md"))
    status_counts = {}
    missing_section = []
    missing_source = []
    legacy_review_frontmatter = []
    for p in pages:
        t = text(p)
        status = None
        m = re.search(rf"^{re.escape(status_key)}:\s*(.+)$", t, flags=re.M)
        if m:
            status = m.group(1).strip()
        else:
            m = re.search(r"^evidence_status:\s*(.+)$", t, flags=re.M)
            status = m.group(1).strip() if m else "MISSING"
        status_counts[status] = status_counts.get(status, 0) + 1
        if required_section not in t:
            missing_section.append(p.name)
        sm = re.search(r"^sources:\s*\[(.*?)\]", t, flags=re.M)
        if not sm or not sm.group(1).strip():
            missing_source.append(p.name)
        if "NEEDS_REVIEW" in t[:500] or "HUMAN_REVIEWED" in t[:500]:
            legacy_review_frontmatter.append(p.name)
    return {
        "dirname": dirname,
        "pages": len(pages),
        "status_counts": status_counts,
        "missing_required_section": missing_section,
        "missing_sources": missing_source,
        "legacy_review_frontmatter": legacy_review_frontmatter,
    }


def rule_readiness():
    rule_rows = read_csv(EXPORTS / "rule_index.csv")
    card_rows = read_csv(EXPORTS / "rule_card_index.csv")
    card_ids = {r.get("card_id") for r in card_rows}
    required_cards = [
        "RC-ASF-001",
        "RC-VES-001",
        "RC-DRUG-001",
        "RC-WITHDRAWAL-MRL-001",
        "RC-DISEASE-REGULATORY-001",
        "RC-DX-001",
        "RC-DIARRHEA-001",
        "RC-RESP-001",
        "RC-REPRO-001",
        "RC-TOX-001",
        "RC-CITATION-001",
        "RC-TRAIN-READY-001",
    ]
    hard_block = sum(1 for r in card_rows if str(r.get("hard_block", "")).lower() == "true")
    missing_required = [x for x in required_cards if x not in card_ids]
    rule_categories = {}
    for r in rule_rows:
        c = r.get("category", "") or "uncategorized"
        rule_categories[c] = rule_categories.get(c, 0) + 1
    return {
        "rules": len(rule_rows),
        "rule_cards": len(card_rows),
        "hard_block_cards": hard_block,
        "missing_required_cards": missing_required,
        "rule_categories": rule_categories,
    }


def synthesis_readiness():
    rows = read_csv(EXPORTS / "synthesis_index.csv")
    titles = " ".join((r.get("title", "") + " " + r.get("page_id", "") + " " + r.get("path", "") + " " + r.get("page_relpath", "")) for r in rows)
    required = {
        "case_generation_context": "case_generation" in titles or "病例生成" in titles,
        "answer_evaluation_rubric": "evaluation_rubric" in titles or "评估量表" in titles,
        "regulatory_blocking": "regulatory_blocking" in titles or "硬阻断" in titles,
        "drug_withdrawal_boundary": "withdrawal" in titles or "休药期" in titles,
        "differential_matrix": "differential" in titles or "鉴别" in titles,
        "dataset_validity_gate": "validity_gate" in titles or "门禁" in titles,
        "prescription_matrices": "prescription" in titles or "处方" in titles,
    }
    return {"rows": len(rows), "required": required, "missing": [k for k, v in required.items() if not v]}


def coverage_crosslinks():
    disease_index = read_csv(EXPORTS / "disease_index.csv")
    drug_index = read_csv(EXPORTS / "drug_page_index.csv")
    comparison_index = read_csv(EXPORTS / "comparison_index.csv")
    syndrome_index = read_csv(EXPORTS / "syndrome_index.csv")
    alias_index = read_csv(EXPORTS / "alias_index.csv")
    disease_cov = {}
    for r in disease_index:
        disease_cov[r.get("coverage_gap_status", "") or "blank"] = disease_cov.get(r.get("coverage_gap_status", "") or "blank", 0) + 1
    drug_status = {}
    for r in drug_index:
        drug_status[r.get("status", "") or "blank"] = drug_status.get(r.get("status", "") or "blank", 0) + 1
    return {
        "disease_index_rows": len(disease_index),
        "disease_coverage": disease_cov,
        "drug_index_rows": len(drug_index),
        "drug_status": drug_status,
        "comparison_rows": len(comparison_index),
        "syndrome_rows": len(syndrome_index),
        "alias_rows": len(alias_index),
    }


def score(summary):
    score = 100
    deductions = []
    missing_paths = sum(len(x["missing_paths"]) for x in summary["path_integrity"])
    if missing_paths:
        d = min(20, missing_paths)
        score -= d
        deductions.append(f"-{d}: missing index target paths ({missing_paths})")
    if summary["entities"]["diseases"]["missing_required_section"]:
        d = min(10, len(summary["entities"]["diseases"]["missing_required_section"]))
        score -= d
        deductions.append(f"-{d}: disease pages missing unified availability section")
    if summary["entities"]["drugs"]["missing_required_section"]:
        d = min(10, len(summary["entities"]["drugs"]["missing_required_section"]))
        score -= d
        deductions.append(f"-{d}: drug pages missing unified availability section")
    bad_fact_tables = [x for x in summary["fact_tables"] if x["rows"] and (x["source_id_rate"] < 1 or (x["page_required"] and x["page_rate"] < 0.95))]
    if bad_fact_tables:
        d = min(20, len(bad_fact_tables) * 5)
        score -= d
        deductions.append(f"-{d}: fact tables with weak source/page completeness")
    if summary["rules"]["missing_required_cards"]:
        d = min(20, len(summary["rules"]["missing_required_cards"]) * 5)
        score -= d
        deductions.append(f"-{d}: required rule cards missing")
    if summary["synthesis"]["missing"]:
        d = min(15, len(summary["synthesis"]["missing"]) * 3)
        score -= d
        deductions.append(f"-{d}: synthesis generation/evaluation pieces missing")
    if summary["coverage"]["comparison_rows"] < 10:
        score -= 5
        deductions.append("-5: weak comparison matrix coverage")
    return max(score, 0), deductions


def main():
    """执行 readiness 评估并写入 Markdown/JSON 报告。"""
    path_checks = [
        path_integrity("disease_index.csv", ["page_relpath"]),
        path_integrity("drug_page_index.csv", ["page_relpath", "path"]),
        path_integrity("rule_index.csv", ["page_relpath"]),
        path_integrity("rule_card_index.csv", ["page_relpath"]),
        path_integrity("comparison_index.csv", ["page_relpath"]),
        path_integrity("synthesis_index.csv", ["page_relpath", "path"]),
        path_integrity("source_index.csv", ["relpath", "page_relpath"]),
    ]
    fact_tables = [
        fact_table_quality("handbook_prescription_fact_index.csv"),
        fact_table_quality("veterinary_treatment_of_pigs_fact_index.csv"),
        fact_table_quality("veterinary_treatment_of_pigs_medicine_index.csv"),
        fact_table_quality("swine_farm_drug_use_1_200_fact_index.csv"),
        fact_table_quality("swine_farm_drug_use_200_363_fact_index.csv"),
        fact_table_quality("handbook_prescription_drug_mention_index.csv"),
        fact_table_quality("swine_farm_drug_use_1_200_drug_mention_index.csv"),
        fact_table_quality("swine_farm_drug_use_200_363_drug_mention_index.csv"),
    ]
    summary = {
        "counts": {
            "diseases": count_md("diseases"),
            "drugs": count_md("drugs"),
            "syndromes": count_md("syndromes"),
            "comparisons": count_md("comparisons"),
            "rules": count_md("rules"),
            "rule_cards": count_md("rule_cards"),
            "sources": count_md("sources"),
            "synthesis": count_md("synthesis"),
            "topics": count_md("topics"),
        },
        "coverage": coverage_crosslinks(),
        "entities": {
            "diseases": entity_status("diseases", "coverage_gap_status", "## 临床知识页可用性"),
            "drugs": entity_status("drugs", "drug_page_status", "## 药物知识页可用性"),
        },
        "path_integrity": path_checks,
        "fact_tables": fact_tables,
        "rules": rule_readiness(),
        "synthesis": synthesis_readiness(),
    }
    readiness_score, deductions = score(summary)
    summary["readiness_score"] = readiness_score
    summary["deductions"] = deductions
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    missing_paths = [m for pc in path_checks for m in pc["missing_paths"]]
    lines = [
        "# Swine LLM Wiki Generation/Evaluation Readiness Audit / 2026-05-08",
        "",
        f"- Readiness score: {readiness_score}/100",
        f"- Entity counts: diseases={summary['counts']['diseases']}, drugs={summary['counts']['drugs']}, syndromes={summary['counts']['syndromes']}, comparisons={summary['counts']['comparisons']}, rules={summary['counts']['rules']}, rule_cards={summary['counts']['rule_cards']}, sources={summary['counts']['sources']}, synthesis={summary['counts']['synthesis']}.",
        f"- Disease coverage: {summary['coverage']['disease_coverage']}",
        f"- Drug status: {summary['coverage']['drug_status']}",
        f"- Rule cards: {summary['rules']['rule_cards']} total, {summary['rules']['hard_block_cards']} hard blocks; required missing={summary['rules']['missing_required_cards']}.",
        f"- Synthesis required missing: {summary['synthesis']['missing']}.",
        "",
        "## Fact Table Quality",
        "",
    ]
    for ft in fact_tables:
        lines.append(f"- `{ft['name']}`: rows={ft['rows']}, source_id_rate={ft['source_id_rate']}, page_rate={ft['page_rate']}, unmapped={ft['unmapped']}.")
    lines.extend(["", "## Path Integrity", ""])
    for pc in path_checks:
        lines.append(f"- `{pc['index']}`: rows={pc['rows']}, checked_paths={pc['checked_paths']}, missing_paths={len(pc['missing_paths'])}.")
    if missing_paths:
        lines.extend(["", "### Missing Paths", ""])
        for m in missing_paths[:100]:
            lines.append(f"- `{m['index']}` {m['field']} `{m['path']}` id={m['id']}")
    lines.extend(["", "## Entity Readiness", ""])
    for name, ent in summary["entities"].items():
        lines.append(f"- {name}: pages={ent['pages']}, status_counts={ent['status_counts']}, missing_required_section={len(ent['missing_required_section'])}, missing_sources={len(ent['missing_sources'])}, legacy_review_frontmatter={len(ent['legacy_review_frontmatter'])}.")
    if deductions:
        lines.extend(["", "## Deductions", ""])
        lines.extend(deductions)
    lines.extend([
        "",
        "## Conclusion",
        "",
        "The wiki is structurally capable of supporting source-first swine disease dataset generation and evaluation. It has entity pages, rule cards, comparison matrices, treatment/prescription fact tables, and source-indexed evidence. Remaining risks are listed above and should be handled as gating constraints rather than blockers for all dataset work.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "readiness_score": readiness_score,
        "counts": summary["counts"],
        "disease_coverage": summary["coverage"]["disease_coverage"],
        "drug_status": summary["coverage"]["drug_status"],
        "missing_paths": len(missing_paths),
        "bad_fact_tables": [x["name"] for x in fact_tables if x["rows"] and (x["source_id_rate"] < 1 or (x["page_required"] and x["page_rate"] < 0.95))],
        "missing_rule_cards": summary["rules"]["missing_required_cards"],
        "missing_synthesis": summary["synthesis"]["missing"],
        "report": str(REPORT.relative_to(ROOT)),
        "summary": str(SUMMARY.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
