import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
MANIFEST = EXPORTS / "runtime_core_manifest.json"

DISEASE_EXPANSIONS = WIKI / "evidence_expansions" / "diseases" / "phase9"
DRUG_EXPANSIONS = WIKI / "evidence_expansions" / "drugs" / "phase9"

REPORT_JSON = ISSUES / "phase9_runtime_cleanup_regression_2026-05-09.json"
REPORT_MD = ISSUES / "phase9_runtime_cleanup_regression_2026-05-09.md"

TZ = timezone(timedelta(hours=8))

COMPACTION_TARGET_IDS = {
    "DIS-046",
    "DIS-049",
    "DIS-055",
    "DRUG-042-ampicillin",
    "DIS-041",
    "DIS-040",
    "DIS-051",
    "DIS-008",
    "DIS-009",
    "DIS-024",
    "DIS-026",
}

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


def load_manifest_entries():
    return json.loads(MANIFEST.read_text(encoding="utf-8")).get("entries", [])


def block_stats(text):
    return {
        "bytes": len(text.encode("utf-8")),
        "candidate_fact_mentions": text.count("candidate_fact"),
        "dose_route_course_mentions": text.count("dose_route_course"),
        "source_id_mentions": text.count("source_id="),
        "fact_like_lines": sum(1 for line in text.splitlines() if line.strip().startswith("- `")),
    }


def phase9_runtime_section(entry, blocks):
    page_type = entry.get("entity_type", "runtime")
    moved = ", ".join(f"`{block['name']}`" for block in blocks) or "none"
    rows = sum(block["stats"]["fact_like_lines"] for block in blocks)
    candidates = sum(block["stats"]["candidate_fact_mentions"] for block in blocks)
    return f"""## Runtime low-risk cleanup / Phase 9

- Runtime role: compact {page_type} page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: {moved}.
- Moved fact-like rows: {rows}; moved candidate facts: {candidates}.
- Detailed evidence moved in Phase 9 is for audit, source lookup, human audit, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

"""


def partial_gap_section(entry):
    return f"""## Partial page gap-routing / Phase 9

- `RC-PARTIAL-GAP-ROUTING-001`: This page is a controlled partial runtime page for recall, differential routing, and gap tracking.
- Runtime tier: `{entry.get('runtime_tier', '')}`; legacy audit status: `{entry.get('legacy_evidence_status', '')}`.
- Missing facets must not be inferred, completed, or converted into diagnosis, treatment, dose, withdrawal-period, MRL, residue, or regulatory conclusions.
- If a requested answer depends on absent facets, route to higher-evidence disease pages, rule cards, source expansion, or current official/regulatory sources.

"""


def insert_after_title(text, section, marker):
    if marker in text:
        return text, False
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            new_lines = lines[: i + 1] + ["", section.rstrip(), ""] + lines[i + 1 :]
            return "\n".join(new_lines) + "\n", True
    return section + text, True


def expansion_root(entry):
    if entry.get("entity_type") == "drug":
        return DRUG_EXPANSIONS
    return DISEASE_EXPANSIONS


def expansion_path(entry):
    return expansion_root(entry) / f"{entry['page_id']}-phase9-evidence-expansion-20260509.md"


def write_expansion(entry, source_rel, blocks):
    root = expansion_root(entry)
    root.mkdir(parents=True, exist_ok=True)
    path = expansion_path(entry)
    if path.exists():
        existing = path.read_text(encoding="utf-8", errors="replace")
        if "phase9_runtime_cleanup_regression" in existing:
            return path, False

    lines = [
        "---",
        f"page_id: {entry['page_id']}",
        f"entity_type: {entry.get('entity_type', '')}_evidence_expansion",
        "runtime_tier: evidence_expansion",
        "default_runtime_retrieval: false",
        "phase: phase9_runtime_cleanup_regression",
        f"moved_from: {source_rel}",
        f"generated: {now()}",
        "---",
        "",
        f"# {entry['page_id']} Phase 9 Evidence Expansion",
        "",
        "This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.",
        "",
        "Runtime handling:",
        "",
        "- Do not load this file for default production or evaluation retrieval.",
        "- Load it only for audit, source lookup, evidence expansion, or manual review.",
        "- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.",
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
        f"> PHASE9_EVIDENCE_EXPANSION_MOVED: Detailed `{block_name}` evidence was moved to "
        f"`{expansion_rel}`. Moved rows={stats['fact_like_lines']}; candidate facts={stats['candidate_fact_mentions']}; "
        f"source anchors={stats['source_id_mentions']}. Load only for audit/source expansion; default runtime generation "
        "must follow the applicable disease, drug, regulatory, withdrawal/MRL, and citation guardrails.\n"
        f"<!-- {block_name}_END -->"
    )


def compact_entry(entry):
    path = ROOT / entry["path"]
    text = path.read_text(encoding="utf-8", errors="replace")
    if "PHASE9_EVIDENCE_EXPANSION_MOVED" in text:
        return {"page": entry["path"], "changed": False, "reason": "already_compacted"}

    matches = list(BLOCK_RE.finditer(text))
    blocks = [
        {
            "name": match.group("name"),
            "body": match.group("body"),
            "stats": block_stats(match.group(0)),
        }
        for match in matches
    ]
    before_bytes = len(text.encode("utf-8"))
    expansion, expansion_created = write_expansion(entry, entry["path"], blocks) if blocks else (None, False)
    expansion_rel = rel(expansion) if expansion else ""

    updated = text
    for block in blocks:
        pattern = re.compile(
            r"<!-- "
            + re.escape(block["name"])
            + r"_START -->\n.*?<!-- "
            + re.escape(block["name"])
            + r"_END -->",
            flags=re.S,
        )
        updated = pattern.sub(placeholder(block["name"], expansion_rel, block["stats"]), updated, count=1)
    updated, core_added = insert_after_title(
        updated,
        phase9_runtime_section(entry, blocks),
        "## Runtime low-risk cleanup / Phase 9",
    )
    path.write_text(updated, encoding="utf-8")
    after_bytes = len(updated.encode("utf-8"))
    return {
        "page": entry["path"],
        "changed": True,
        "blocks_moved": len(blocks),
        "fact_like_rows_moved": sum(block["stats"]["fact_like_lines"] for block in blocks),
        "candidate_fact_mentions_moved": sum(block["stats"]["candidate_fact_mentions"] for block in blocks),
        "source_id_mentions_moved": sum(block["stats"]["source_id_mentions"] for block in blocks),
        "bytes_before": before_bytes,
        "bytes_after": after_bytes,
        "bytes_reduced": before_bytes - after_bytes,
        "expansion": expansion_rel,
        "expansion_created": expansion_created,
        "runtime_section_added": core_added,
    }


def annotate_partial_entry(entry):
    path = ROOT / entry["path"]
    text = path.read_text(encoding="utf-8", errors="replace")
    updated, changed = insert_after_title(
        text,
        partial_gap_section(entry),
        "## Partial page gap-routing / Phase 9",
    )
    if changed:
        path.write_text(updated, encoding="utf-8")
    return {
        "page": entry["path"],
        "changed": changed,
        "bytes_before": len(text.encode("utf-8")),
        "bytes_after": len(updated.encode("utf-8")),
    }


def write_reports(compaction_records, partial_records):
    generated = now()
    compacted = [r for r in compaction_records if r.get("changed")]
    partial_changed = [r for r in partial_records if r.get("changed")]
    payload = {
        "generated_at": generated,
        "purpose": "Phase 9 low-risk runtime cleanup and regression readiness closure.",
        "compaction_targets": sorted(COMPACTION_TARGET_IDS),
        "compaction_records": compaction_records,
        "partial_gap_routing_records": partial_records,
        "summary": {
            "compaction_pages_checked": len(compaction_records),
            "compaction_pages_changed": len(compacted),
            "blocks_moved": sum(r.get("blocks_moved", 0) for r in compacted),
            "fact_like_rows_moved": sum(r.get("fact_like_rows_moved", 0) for r in compacted),
            "candidate_fact_mentions_moved": sum(r.get("candidate_fact_mentions_moved", 0) for r in compacted),
            "source_id_mentions_moved": sum(r.get("source_id_mentions_moved", 0) for r in compacted),
            "bytes_reduced": sum(r.get("bytes_reduced", 0) for r in compacted),
            "partial_pages_checked": len(partial_records),
            "partial_pages_changed": len(partial_changed),
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 9 Runtime Cleanup Regression / 2026-05-09",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Compaction pages checked: {payload['summary']['compaction_pages_checked']}",
        f"- Compaction pages changed: {payload['summary']['compaction_pages_changed']}",
        f"- Evidence blocks moved: {payload['summary']['blocks_moved']}",
        f"- Fact-like rows moved: {payload['summary']['fact_like_rows_moved']}",
        f"- Candidate fact mentions moved: {payload['summary']['candidate_fact_mentions_moved']}",
        f"- Source anchors moved: {payload['summary']['source_id_mentions_moved']}",
        f"- Runtime bytes reduced: {payload['summary']['bytes_reduced']}",
        f"- Partial pages checked: {payload['summary']['partial_pages_checked']}",
        f"- Partial pages changed: {payload['summary']['partial_pages_changed']}",
        "",
        "## Compacted Pages",
        "",
    ]
    for record in compacted:
        lines.append(
            f"- `{record['page']}`: blocks={record['blocks_moved']}, "
            f"candidate_fact={record['candidate_fact_mentions_moved']}, "
            f"bytes={record['bytes_before']}->{record['bytes_after']}, "
            f"expansion=`{record['expansion']}`"
        )
    lines.extend([
        "",
        "## Partial Gap Routing",
        "",
        f"- Controlled partial pages annotated: {len(partial_changed)}",
        "- Partial pages are retained as recall and gap-routing entries; missing facets must not be guessed.",
        "",
        "## Runtime Handling",
        "",
        "- Phase 9 does not add new biomedical facts.",
        "- It moves low-risk dense evidence to expansion files and marks partial pages as controlled gap-routing pages.",
        "- Final regression should be read together with `runtime_hallucination_risk_audit_2026-05-09` and readiness outputs.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    entries = load_manifest_entries()
    by_id = {entry.get("page_id"): entry for entry in entries}
    compaction_records = [
        compact_entry(by_id[page_id])
        for page_id in sorted(COMPACTION_TARGET_IDS)
        if page_id in by_id and (ROOT / by_id[page_id]["path"]).exists()
    ]
    partial_entries = [
        entry for entry in entries
        if entry.get("runtime_tier") == "runtime_core_partial" and (ROOT / entry["path"]).exists()
    ]
    partial_records = [annotate_partial_entry(entry) for entry in partial_entries]
    write_reports(compaction_records, partial_records)
    print(json.dumps({
        "compaction_pages_checked": len(compaction_records),
        "compaction_pages_changed": sum(1 for r in compaction_records if r.get("changed")),
        "blocks_moved": sum(r.get("blocks_moved", 0) for r in compaction_records),
        "candidate_fact_mentions_moved": sum(r.get("candidate_fact_mentions_moved", 0) for r in compaction_records),
        "bytes_reduced": sum(r.get("bytes_reduced", 0) for r in compaction_records),
        "partial_pages_checked": len(partial_records),
        "partial_pages_changed": sum(1 for r in partial_records if r.get("changed")),
        "report_json": rel(REPORT_JSON),
        "report_md": rel(REPORT_MD),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
