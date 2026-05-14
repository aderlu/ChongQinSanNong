import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
MANIFEST = EXPORTS / "runtime_core_manifest.json"

REPORT_JSON = ISSUES / "phase4_drug_guardrail_anchors_2026-05-09.json"
REPORT_MD = ISSUES / "phase4_drug_guardrail_anchors_2026-05-09.md"

TZ = timezone(timedelta(hours=8))


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def load_drug_entries():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return [entry for entry in payload.get("entries", []) if entry.get("entity_type") == "drug"]


def guardrail_section(runtime_tier, legacy_audit_status):
    return f"""## Runtime guardrail anchors / Phase 4

- Runtime tier: `{runtime_tier}`; legacy audit status: `{legacy_audit_status}`.
- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.

"""


def insert_after_title(text, section):
    if "## Runtime guardrail anchors / Phase 4" in text or "## Runtime guardrail anchors / Phase 3" in text:
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
    before = {
        "has_rc_drug": "RC-DRUG-001" in text,
        "has_rc_withdrawal": "RC-WITHDRAWAL-MRL-001" in text,
        "bytes": len(text.encode("utf-8")),
    }
    if before["has_rc_drug"] and before["has_rc_withdrawal"]:
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
        "has_rc_drug": "RC-DRUG-001" in updated,
        "has_rc_withdrawal": "RC-WITHDRAWAL-MRL-001" in updated,
        "bytes": len(updated.encode("utf-8")),
    }
    return {
        "page_id": entry.get("page_id", ""),
        "path": entry.get("path", ""),
        "changed": changed,
        "reason": "guardrail_section_added" if changed else "not_changed",
        "runtime_tier": entry.get("runtime_tier", ""),
        "legacy_evidence_status": entry.get("legacy_evidence_status", ""),
        "before": before,
        "after": after,
    }


def write_reports(records):
    generated = now()
    changed = [record for record in records if record.get("changed")]
    missing_after = [
        record for record in records
        if not record["after"]["has_rc_drug"] or not record["after"]["has_rc_withdrawal"]
    ]
    payload = {
        "generated_at": generated,
        "purpose": "Phase 4 application of explicit drug runtime guardrail anchors.",
        "records": records,
        "summary": {
            "drug_pages_checked": len(records),
            "drug_pages_changed": len(changed),
            "missing_anchor_after": len(missing_after),
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 4 Drug Guardrail Anchor Application / 2026-05-09",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Drug pages checked: {len(records)}",
        f"- Drug pages changed: {len(changed)}",
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
        "- Each changed drug page now has explicit `RC-DRUG-001` and `RC-WITHDRAWAL-MRL-001` anchors.",
        "- These anchors are intended for production gating, evaluation checks, and audit scripts.",
        "- This phase does not add new drug facts or change source evidence; it adds runtime boundary metadata.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    records = [process_entry(entry) for entry in load_drug_entries()]
    write_reports(records)
    print(json.dumps({
        "drug_pages_checked": len(records),
        "drug_pages_changed": sum(1 for record in records if record.get("changed")),
        "missing_anchor_after": sum(
            1 for record in records
            if not record["after"]["has_rc_drug"] or not record["after"]["has_rc_withdrawal"]
        ),
        "report_json": rel(REPORT_JSON),
        "report_md": rel(REPORT_MD),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
