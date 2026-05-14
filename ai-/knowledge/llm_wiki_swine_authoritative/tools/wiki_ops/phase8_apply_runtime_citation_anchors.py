from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
MANIFEST = EXPORTS / "runtime_core_manifest.json"
REPORT_JSON = ISSUES / "phase8_runtime_citation_anchors_2026-05-09.json"
REPORT_MD = ISSUES / "phase8_runtime_citation_anchors_2026-05-09.md"
TZ = timezone(timedelta(hours=8))

TARGET_TYPES = {"disease", "drug", "comparison", "syndrome"}


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def load_entries() -> list[dict[str, object]]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = payload.get("entries", [])
    return entries if isinstance(entries, list) else []


def section(entry: dict[str, object]) -> str:
    return f"""## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
- Runtime task use: `{entry.get('task_use_status', '')}`; gold dataset role: `{entry.get('gold_dataset_role', '')}`.
- Legacy audit status, if present, is not a usability gate; use `source_status`, `fact_validity`, `authority_level`, `risk_class`, and `task_use_status`.

"""


def insert_after_title(text: str, addition: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[: idx + 1] + ["", addition.rstrip(), ""] + lines[idx + 1 :]) + "\n"
    return addition + text


def process(entry: dict[str, object]) -> dict[str, object]:
    relpath = str(entry.get("path", ""))
    path = ROOT / relpath
    if entry.get("entity_type") not in TARGET_TYPES:
        return {"page_id": entry.get("page_id", ""), "path": relpath, "changed": False, "reason": "entity_type_not_targeted"}
    if not path.exists():
        return {"page_id": entry.get("page_id", ""), "path": relpath, "changed": False, "reason": "missing_path"}
    text = path.read_text(encoding="utf-8", errors="replace")
    if "RC-CITATION-001" in text:
        return {"page_id": entry.get("page_id", ""), "path": relpath, "changed": False, "reason": "anchor_already_present"}
    updated = insert_after_title(text, section(entry))
    path.write_text(updated, encoding="utf-8")
    return {
        "page_id": entry.get("page_id", ""),
        "path": relpath,
        "entity_type": entry.get("entity_type", ""),
        "changed": True,
        "reason": "citation_gate_added",
        "bytes_before": len(text.encode("utf-8")),
        "bytes_after": len(updated.encode("utf-8")),
    }


def main() -> None:
    records = [process(entry) for entry in load_entries()]
    changed = [record for record in records if record.get("changed")]
    report = {
        "generated_at": now(),
        "purpose": "Phase 8 page-level insertion of RC-CITATION-001 anchors for runtime dataset provenance gates.",
        "target_entity_types": sorted(TARGET_TYPES),
        "records": records,
        "summary": {
            "runtime_entries_checked": len(records),
            "pages_changed": len(changed),
        },
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Phase 8 Runtime Citation Anchors",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Runtime entries checked: {len(records)}",
        f"- Pages changed: {len(changed)}",
        "",
        "## Changed Pages",
        "",
    ]
    if not changed:
        lines.append("- None")
    else:
        for record in changed[:200]:
            lines.append(f"- `{record['page_id']}` `{record['path']}` bytes={record['bytes_before']}->{record['bytes_after']}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"runtime_entries_checked": len(records), "pages_changed": len(changed), "report_json": str(REPORT_JSON.relative_to(ROOT)), "report_md": str(REPORT_MD.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
