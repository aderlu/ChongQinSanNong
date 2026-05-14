import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
DISEASES = WIKI / "diseases"
EXPANSIONS = WIKI / "evidence_expansions" / "diseases" / "phase7"
ISSUES = ROOT / "issues"

REPORT_JSON = ISSUES / "phase7_disease_page_compaction_2026-05-09.json"
REPORT_MD = ISSUES / "phase7_disease_page_compaction_2026-05-09.md"

TZ = timezone(timedelta(hours=8))

TARGETS = [
    "DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md",
    "DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md",
    "DIS-044-gl-sser-s-disease.md",
]

BLOCK_RE = re.compile(
    r"<!-- (?P<name>[A-Z0-9_]+(?:_[A-Z0-9]+)*)_START -->\n"
    r"(?P<body>.*?)"
    r"<!-- (?P=name)_END -->",
    flags=re.S,
)


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def page_id_from_name(name):
    return name.removesuffix(".md")


def block_stats(text):
    return {
        "bytes": len(text.encode("utf-8")),
        "candidate_fact_mentions": text.count("candidate_fact"),
        "dose_route_course_mentions": text.count("dose_route_course"),
        "treatment_mentions": text.count("treatment_candidate") + text.count("Prescription"),
        "source_id_mentions": text.count("source_id="),
        "fact_like_lines": sum(1 for line in text.splitlines() if line.strip().startswith("- `")),
    }


def runtime_core_section(records):
    block_names = ", ".join(f"`{record['name']}`" for record in records) or "none"
    moved_facts = sum(record["stats"]["fact_like_lines"] for record in records)
    moved_candidates = sum(record["stats"]["candidate_fact_mentions"] for record in records)
    return f"""## Runtime core compaction / Phase 7

- Runtime role: compact disease boundary page for retrieval, differential diagnosis routing, prevention/control framing, and evaluation checks.
- Phase 7 moved high-density batch evidence blocks out of default retrieval: {block_names}.
- Moved fact-like rows: {moved_facts}; moved candidate facts: {moved_candidates}.
- `RC-DX-001`: Diagnosis must remain evidence-routed and distinguish suspicion, sample, method, pathogen detection, causality, and differential diagnosis.
- `RC-DISEASE-REGULATORY-001`: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- `RC-DRUG-001`: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- Expansion files under `wiki/evidence_expansions/diseases/phase7/` are for audit, source lookup, and manual review, not default production retrieval.

"""


def insert_runtime_core(text, records):
    marker = "## Runtime core compaction / Phase 7"
    if marker in text:
        return text, False
    lines = text.splitlines()
    section = runtime_core_section(records).rstrip()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            new_lines = lines[: i + 1] + ["", section, ""] + lines[i + 1 :]
            return "\n".join(new_lines) + "\n", True
    return section + "\n\n" + text, True


def expansion_path(page_id):
    return EXPANSIONS / f"{page_id}-phase7-evidence-expansion-20260509.md"


def write_expansion(page_id, source_rel, blocks):
    EXPANSIONS.mkdir(parents=True, exist_ok=True)
    path = expansion_path(page_id)
    if path.exists():
        existing = path.read_text(encoding="utf-8", errors="replace")
        if "phase7_disease_page_compaction" in existing:
            return path, False

    lines = [
        "---",
        f"page_id: {page_id}",
        "entity_type: disease_evidence_expansion",
        "runtime_tier: evidence_expansion",
        "default_runtime_retrieval: false",
        "phase: phase7_disease_page_compaction",
        f"moved_from: {source_rel}",
        f"generated: {now()}",
        "---",
        "",
        f"# {page_id} Phase 7 Evidence Expansion",
        "",
        "This file stores high-density disease evidence moved out of the default runtime disease page during Phase 7.",
        "",
        "Runtime handling:",
        "",
        "- Do not load this file for default production or evaluation retrieval.",
        "- Load it only for audit, source lookup, evidence expansion, or manual review.",
        "- Diagnosis, regulatory action, treatment, withdrawal-period, MRL, residue, and food-safety conclusions still require rule-card gating and current source verification.",
        "",
    ]
    for block in blocks:
        lines.extend([
            f"## {block['name']}",
            "",
            f"- Original marker: `{block['name']}_START` / `{block['name']}_END`",
            f"- Original runtime page: `{source_rel}`",
            f"- Byte size moved: {block['stats']['bytes']}",
            f"- Fact-like rows moved: {block['stats']['fact_like_lines']}",
            f"- Candidate fact mentions moved: {block['stats']['candidate_fact_mentions']}",
            f"- Dose/route/course fact markers moved: {block['stats']['dose_route_course_mentions']}",
            f"- Treatment or prescription markers moved: {block['stats']['treatment_mentions']}",
            f"- Source anchors moved: {block['stats']['source_id_mentions']}",
            "",
            f"<!-- {block['name']}_START -->",
            block["body"].strip(),
            f"<!-- {block['name']}_END -->",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path, True


def placeholder(block_name, expansion_rel, stats):
    return (
        f"<!-- {block_name}_START -->\n"
        f"> PHASE7_EVIDENCE_EXPANSION_MOVED: Detailed `{block_name}` disease evidence was moved to "
        f"`{expansion_rel}`. Moved rows={stats['fact_like_lines']}; candidate facts={stats['candidate_fact_mentions']}; "
        f"source anchors={stats['source_id_mentions']}. Load only for audit/source expansion. Runtime diagnosis, "
        "regulatory, and treatment generation must follow `RC-DX-001`, `RC-DISEASE-REGULATORY-001`, "
        "`RC-DRUG-001`, and `RC-WITHDRAWAL-MRL-001`.\n"
        f"<!-- {block_name}_END -->"
    )


def process_page(path):
    original = path.read_text(encoding="utf-8", errors="replace")
    if "PHASE7_EVIDENCE_EXPANSION_MOVED" in original:
        return {
            "page": rel(path),
            "skipped": True,
            "reason": "already_compacted",
            "bytes_before": len(original.encode("utf-8")),
            "bytes_after": len(original.encode("utf-8")),
        }

    matches = list(BLOCK_RE.finditer(original))
    blocks = []
    for match in matches:
        full = match.group(0)
        blocks.append({
            "name": match.group("name"),
            "body": match.group("body"),
            "stats": block_stats(full),
        })

    page_id = page_id_from_name(path.name)
    source_rel = rel(path)
    expansion, expansion_created = write_expansion(page_id, source_rel, blocks) if blocks else (None, False)
    expansion_rel = rel(expansion) if expansion else ""

    migrated = original
    for block in blocks:
        pattern = re.compile(
            r"<!-- "
            + re.escape(block["name"])
            + r"_START -->\n.*?<!-- "
            + re.escape(block["name"])
            + r"_END -->",
            flags=re.S,
        )
        migrated = pattern.sub(placeholder(block["name"], expansion_rel, block["stats"]), migrated, count=1)

    migrated, core_added = insert_runtime_core(migrated, blocks)
    path.write_text(migrated, encoding="utf-8")

    return {
        "page": source_rel,
        "skipped": False,
        "blocks_moved": len(blocks),
        "block_names": [block["name"] for block in blocks],
        "fact_like_rows_moved": sum(block["stats"]["fact_like_lines"] for block in blocks),
        "candidate_fact_mentions_moved": sum(block["stats"]["candidate_fact_mentions"] for block in blocks),
        "dose_route_course_mentions_moved": sum(block["stats"]["dose_route_course_mentions"] for block in blocks),
        "treatment_mentions_moved": sum(block["stats"]["treatment_mentions"] for block in blocks),
        "source_id_mentions_moved": sum(block["stats"]["source_id_mentions"] for block in blocks),
        "bytes_before": len(original.encode("utf-8")),
        "bytes_after": len(migrated.encode("utf-8")),
        "bytes_reduced": len(original.encode("utf-8")) - len(migrated.encode("utf-8")),
        "expansion": expansion_rel,
        "expansion_created": expansion_created,
        "runtime_core_section_added": core_added,
    }


def write_reports(records):
    generated = now()
    changed = [record for record in records if not record.get("skipped")]
    payload = {
        "generated_at": generated,
        "purpose": "Phase 7 compaction of high-density runtime disease pages by moving batch evidence to evidence expansions.",
        "targets": TARGETS,
        "records": records,
        "summary": {
            "pages_checked": len(records),
            "pages_changed": len(changed),
            "blocks_moved": sum(record.get("blocks_moved", 0) for record in changed),
            "fact_like_rows_moved": sum(record.get("fact_like_rows_moved", 0) for record in changed),
            "candidate_fact_mentions_moved": sum(record.get("candidate_fact_mentions_moved", 0) for record in changed),
            "source_id_mentions_moved": sum(record.get("source_id_mentions_moved", 0) for record in changed),
            "bytes_reduced": sum(record.get("bytes_reduced", 0) for record in changed),
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 7 Disease Page Compaction / 2026-05-09",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Pages checked: {payload['summary']['pages_checked']}",
        f"- Pages changed: {payload['summary']['pages_changed']}",
        f"- Batch evidence blocks moved: {payload['summary']['blocks_moved']}",
        f"- Fact-like rows moved: {payload['summary']['fact_like_rows_moved']}",
        f"- Candidate fact mentions moved: {payload['summary']['candidate_fact_mentions_moved']}",
        f"- Source anchors moved: {payload['summary']['source_id_mentions_moved']}",
        f"- Runtime bytes reduced: {payload['summary']['bytes_reduced']}",
        "",
        "## Changed Pages",
        "",
    ]
    for record in changed:
        lines.append(
            f"- `{record['page']}`: blocks={record['blocks_moved']}, "
            f"rows={record['fact_like_rows_moved']}, "
            f"candidate_fact={record['candidate_fact_mentions_moved']}, "
            f"bytes={record['bytes_before']}->{record['bytes_after']}, "
            f"expansion=`{record['expansion']}`"
        )
    lines.extend([
        "",
        "## Runtime Handling",
        "",
        "- Target disease pages now keep compact clinical/runtime cores and short moved-evidence placeholders.",
        "- Detailed batch evidence moved to `wiki/evidence_expansions/diseases/phase7/` is not for default retrieval.",
        "- This phase does not add new disease facts; it reorganizes already present evidence to reduce retrieval noise.",
        "- Diagnosis, regulatory action, treatment, and residue-related generation remains gated by disease/drug rule cards.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    records = []
    for name in TARGETS:
        path = DISEASES / name
        if not path.exists():
            records.append({"page": rel(path), "skipped": True, "reason": "missing"})
            continue
        records.append(process_page(path))
    write_reports(records)
    print(json.dumps({
        "pages_checked": len(records),
        "pages_changed": sum(1 for record in records if not record.get("skipped")),
        "blocks_moved": sum(record.get("blocks_moved", 0) for record in records),
        "fact_like_rows_moved": sum(record.get("fact_like_rows_moved", 0) for record in records),
        "candidate_fact_mentions_moved": sum(record.get("candidate_fact_mentions_moved", 0) for record in records),
        "bytes_reduced": sum(record.get("bytes_reduced", 0) for record in records),
        "report_json": rel(REPORT_JSON),
        "report_md": rel(REPORT_MD),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
