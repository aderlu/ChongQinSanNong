import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
MANIFEST = EXPORTS / "runtime_core_manifest.json"

REPORT_JSON = ISSUES / "phase5_disease_guardrail_anchors_2026-05-09.json"
REPORT_MD = ISSUES / "phase5_disease_guardrail_anchors_2026-05-09.md"

TZ = timezone(timedelta(hours=8))


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def load_disease_entries():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return [entry for entry in payload.get("entries", []) if entry.get("entity_type") == "disease"]


def guardrail_section(runtime_tier, legacy_audit_status):
    return f"""## Runtime disease guardrail anchors / Phase 5

- Runtime tier: `{runtime_tier}`; legacy audit status: `{legacy_audit_status}`.
- `RC-DX-001`: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- `RC-DISEASE-REGULATORY-001`: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- `RC-DRUG-001`: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Partial pages and pages with `source_missing`, `source_level_mismatch`, or `insufficient_anchor` are retrieval and gap-routing pages; missing facets must not be filled by guesswork.

"""


def insert_after_title(text, section):
    if "## Runtime disease guardrail anchors / Phase 5" in text:
        return text, False
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            new_lines = lines[: i + 1] + ["", section.rstrip(), ""] + lines[i + 1 :]
            return "\n".join(new_lines) + "\n", True
    return section + text, True


def process_entry(entry):
    path = ROOT / entry["path"]
    text = path.read_text(encoding="utf-8", errors="replace")
    required = ["RC-DX-001", "RC-DISEASE-REGULATORY-001", "RC-DRUG-001", "RC-WITHDRAWAL-MRL-001"]
    before = {
        "bytes": len(text.encode("utf-8")),
        "missing": [item for item in required if item not in text],
        "legacy_review_marker": "NEEDS_REVIEW" in text[:800] or "HUMAN_REVIEWED" in text[:800],
    }
    if not before["missing"] and "## Runtime disease guardrail anchors / Phase 5" in text:
        return {
            "page_id": entry.get("page_id", ""),
            "path": entry.get("path", ""),
            "changed": False,
            "reason": "anchors_already_present",
            "before": before,
            "after": before,
        }

    section = guardrail_section(entry.get("runtime_tier", ""), entry.get("legacy_evidence_status", ""))
    updated, changed = insert_after_title(text, section)
    if changed:
        path.write_text(updated, encoding="utf-8")
    after = {
        "bytes": len(updated.encode("utf-8")),
        "missing": [item for item in required if item not in updated],
        "legacy_review_marker": "NEEDS_REVIEW" in updated[:1200] or "HUMAN_REVIEWED" in updated[:1200],
    }
    return {
        "page_id": entry.get("page_id", ""),
        "path": entry.get("path", ""),
        "changed": changed,
        "reason": "disease_guardrail_section_added" if changed else "not_changed",
        "runtime_tier": entry.get("runtime_tier", ""),
        "legacy_evidence_status": entry.get("legacy_evidence_status", ""),
        "before": before,
        "after": after,
    }


def write_reports(records):
    generated = now()
    changed = [record for record in records if record.get("changed")]
    missing_after = [record for record in records if record["after"]["missing"]]
    partial_changed = [record for record in changed if record.get("runtime_tier") == "runtime_core_partial"]
    payload = {
        "generated_at": generated,
        "purpose": "Phase 5 application of explicit disease runtime guardrail anchors.",
        "records": records,
        "summary": {
            "disease_pages_checked": len(records),
            "disease_pages_changed": len(changed),
            "partial_disease_pages_changed": len(partial_changed),
            "missing_anchor_after": len(missing_after),
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 5 Disease Guardrail Anchor Application / 2026-05-09",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Disease pages checked: {len(records)}",
        f"- Disease pages changed: {len(changed)}",
        f"- Partial disease pages changed: {len(partial_changed)}",
        f"- Missing anchors after change: {len(missing_after)}",
        "",
        "## Changed Pages",
        "",
    ]
    if not changed:
        lines.append("- None")
    for record in changed:
        lines.append(
            f"- `{record['path']}`: tier={record.get('runtime_tier', '')}, "
            f"legacy_status={record.get('legacy_evidence_status', '')}, "
            f"bytes={record['before']['bytes']}->{record['after']['bytes']}"
        )
    lines.extend([
        "",
        "## Runtime Handling",
        "",
        "- Each changed disease page now has explicit diagnosis, regulatory, drug, and withdrawal/MRL guardrail anchors.",
        "- These anchors are intended for production gating, evaluation checks, and audit scripts.",
        "- This phase does not add new disease facts or change source evidence; it adds runtime boundary metadata.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    records = [process_entry(entry) for entry in load_disease_entries()]
    write_reports(records)
    print(json.dumps({
        "disease_pages_checked": len(records),
        "disease_pages_changed": sum(1 for record in records if record.get("changed")),
        "partial_disease_pages_changed": sum(
            1 for record in records if record.get("changed") and record.get("runtime_tier") == "runtime_core_partial"
        ),
        "missing_anchor_after": sum(1 for record in records if record["after"]["missing"]),
        "report_json": rel(REPORT_JSON),
        "report_md": rel(REPORT_MD),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
