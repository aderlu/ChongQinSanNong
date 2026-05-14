import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
DRUGS = WIKI / "drugs"
EXPANSIONS = WIKI / "evidence_expansions" / "drugs"
ISSUES = ROOT / "issues"

REPORT_JSON = ISSUES / "phase3_drug_evidence_expansion_2026-05-09.json"
REPORT_MD = ISSUES / "phase3_drug_evidence_expansion_2026-05-09.md"

TZ = timezone(timedelta(hours=8))

TARGETS = [
    "DRUG-034-sulfonamides.md",
    "DRUG-014-lincomycin.md",
    "DRUG-009-penicillin-g.md",
    "DRUG-030-tetracyclines.md",
    "DRUG-023-gentamicin.md",
    "DRUG-020-chlortetracycline.md",
    "DRUG-066-dexamethasone.md",
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
        "source_id_mentions": text.count("source_id="),
    }


def guardrail_section():
    return """## Runtime guardrail anchors / Phase 3

- `RC-DRUG-001`: This runtime page must not be used by itself to generate executable prescriptions, dose, route, course, withdrawal period, MRL, residue, or food-safety claims.
- `RC-WITHDRAWAL-MRL-001`: Any withdrawal-period, MRL, residue, or edible-product conclusion must be checked against current label/regulatory sources and the evidence expansion layer.
- Evidence expansion blocks moved in Phase 3 are audit and source-expansion material, not default runtime retrieval text.

"""


def insert_guardrail(text):
    if "## Runtime guardrail anchors / Phase 3" in text:
        return text, False
    match = re.search(r"^# .+$\n", text, flags=re.M)
    if not match:
        return guardrail_section() + text, True
    pos = match.end()
    return text[:pos] + "\n" + guardrail_section() + text[pos:], True


def expansion_path(page_id):
    return EXPANSIONS / f"{page_id}-evidence-expansion-20260509.md"


def write_expansion(page_id, source_rel, blocks):
    EXPANSIONS.mkdir(parents=True, exist_ok=True)
    path = expansion_path(page_id)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if "phase3_drug_evidence_expansion" in existing:
            return path, False

    lines = [
        "---",
        f"page_id: {page_id}",
        "entity_type: drug_evidence_expansion",
        "runtime_tier: evidence_expansion",
        "default_runtime_retrieval: false",
        "phase: phase3_drug_evidence_expansion",
        f"moved_from: {source_rel}",
        f"generated: {now()}",
        "---",
        "",
        f"# {page_id} Evidence Expansion",
        "",
        "This file stores detailed batch evidence moved out of the runtime drug page during Phase 3 cleanup.",
        "",
        "Runtime rule:",
        "",
        "- Do not load this file for default production/evaluation retrieval.",
        "- Load it only for evidence expansion, audit, source lookup, or manual review.",
        "- Dose, route, course, withdrawal period, MRL, residue, and food-safety claims still require current label/regulatory verification.",
        "",
    ]
    for block in blocks:
        lines.extend([
            f"## {block['name']}",
            "",
            f"- Original marker: `{block['name']}_START` / `{block['name']}_END`",
            f"- Original runtime page: `{source_rel}`",
            f"- Candidate facts: {block['stats']['candidate_fact_mentions']}",
            f"- Dose/route/course facts: {block['stats']['dose_route_course_mentions']}",
            f"- Source anchors: {block['stats']['source_id_mentions']}",
            "",
            f"<!-- {block['name']}_START -->",
            block["body"].strip(),
            f"<!-- {block['name']}_END -->",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path, True


def placeholder(block_name, expansion_rel):
    return (
        f"<!-- {block_name}_START -->\n"
        f"> PHASE3_EVIDENCE_EXPANSION_MOVED: Detailed `{block_name}` evidence was moved to "
        f"`{expansion_rel}`. Load it only for audit/source expansion. Runtime generation must follow "
        "`RC-DRUG-001` and `RC-WITHDRAWAL-MRL-001`.\n"
        f"<!-- {block_name}_END -->"
    )


def process_page(path):
    original = path.read_text(encoding="utf-8", errors="replace")
    if "PHASE3_EVIDENCE_EXPANSION_MOVED" in original:
        return {
            "page": rel(path),
            "skipped": True,
            "reason": "already_migrated",
        }

    matches = list(BLOCK_RE.finditer(original))
    if not matches:
        text, guardrail_added = insert_guardrail(original)
        if guardrail_added:
            path.write_text(text, encoding="utf-8")
        return {
            "page": rel(path),
            "skipped": False,
            "blocks_moved": 0,
            "guardrail_added": guardrail_added,
        }

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
    expansion, expansion_created = write_expansion(page_id, source_rel, blocks)
    expansion_rel = rel(expansion)

    migrated = original
    for block in blocks:
        pattern = re.compile(
            r"<!-- " + re.escape(block["name"]) + r"_START -->\n.*?<!-- " + re.escape(block["name"]) + r"_END -->",
            flags=re.S,
        )
        migrated = pattern.sub(placeholder(block["name"], expansion_rel), migrated, count=1)
    migrated, guardrail_added = insert_guardrail(migrated)
    path.write_text(migrated, encoding="utf-8")

    return {
        "page": source_rel,
        "skipped": False,
        "blocks_moved": len(blocks),
        "block_names": [block["name"] for block in blocks],
        "candidate_fact_mentions_moved": sum(block["stats"]["candidate_fact_mentions"] for block in blocks),
        "dose_route_course_mentions_moved": sum(block["stats"]["dose_route_course_mentions"] for block in blocks),
        "source_id_mentions_moved": sum(block["stats"]["source_id_mentions"] for block in blocks),
        "bytes_before": len(original.encode("utf-8")),
        "bytes_after": len(migrated.encode("utf-8")),
        "expansion": expansion_rel,
        "expansion_created": expansion_created,
        "guardrail_added": guardrail_added,
    }


def write_report(records):
    generated = now()
    payload = {
        "generated_at": generated,
        "purpose": "Phase 3 migration of large drug batch evidence blocks to non-runtime evidence expansion files.",
        "targets": TARGETS,
        "records": records,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 3 Drug Evidence Expansion Migration / 2026-05-09",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
    ]
    changed = [r for r in records if not r.get("skipped")]
    lines.extend([
        f"- Pages processed: {len(records)}",
        f"- Pages changed: {len(changed)}",
        f"- Blocks moved: {sum(r.get('blocks_moved', 0) for r in changed)}",
        f"- Candidate fact mentions moved: {sum(r.get('candidate_fact_mentions_moved', 0) for r in changed)}",
        f"- Dose/route/course mentions moved: {sum(r.get('dose_route_course_mentions_moved', 0) for r in changed)}",
        "",
        "## Page Records",
        "",
    ])
    for record in records:
        if record.get("skipped"):
            lines.append(f"- `{record['page']}` skipped: {record.get('reason', '')}")
            continue
        lines.append(
            f"- `{record['page']}`: blocks_moved={record.get('blocks_moved', 0)}, "
            f"bytes_before={record.get('bytes_before', '')}, bytes_after={record.get('bytes_after', '')}, "
            f"expansion=`{record.get('expansion', '')}`"
        )
    lines.extend([
        "",
        "## Runtime Handling",
        "",
        "- Runtime drug pages now retain concise placeholders and rule-card anchors.",
        "- Detailed batch evidence is preserved under `wiki/evidence_expansions/drugs/`.",
        "- Evidence expansion files are not part of the runtime manifest and should be loaded only for audit/source expansion.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    records = []
    for target in TARGETS:
        records.append(process_page(DRUGS / target))
    write_report(records)
    print(json.dumps({
        "processed": len(records),
        "changed": sum(1 for r in records if not r.get("skipped")),
        "blocks_moved": sum(r.get("blocks_moved", 0) for r in records),
        "report_json": rel(REPORT_JSON),
        "report_md": rel(REPORT_MD),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
