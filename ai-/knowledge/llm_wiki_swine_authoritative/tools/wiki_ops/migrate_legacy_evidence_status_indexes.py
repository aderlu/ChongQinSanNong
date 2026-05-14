from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
REPORT = ISSUES / "legacy_evidence_status_index_migration_2026-05-12.json"
TZ = timezone(timedelta(hours=8))

TARGETS = [
    "balanced_task_use_index.csv",
    "comparison_index.csv",
    "rule_index.csv",
    "source_index.csv",
    "synthesis_index.csv",
]


def migrate_csv(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"path": path.relative_to(ROOT).as_posix(), "changed": False, "reason": "missing"}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if "evidence_status" not in fieldnames:
        return {"path": path.relative_to(ROOT).as_posix(), "changed": False, "reason": "already_migrated"}
    if "legacy_evidence_status" in fieldnames:
        raise ValueError(f"Both evidence_status and legacy_evidence_status exist in {path}")

    new_fieldnames = ["legacy_evidence_status" if name == "evidence_status" else name for name in fieldnames]
    migrated_rows = []
    for row in rows:
        migrated = {}
        for name in fieldnames:
            target = "legacy_evidence_status" if name == "evidence_status" else name
            migrated[target] = row.get(name, "")
        migrated_rows.append(migrated)

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(migrated_rows)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "changed": True,
        "rows": len(migrated_rows),
        "old_field": "evidence_status",
        "new_field": "legacy_evidence_status",
    }


def main() -> int:
    records = [migrate_csv(EXPORTS / name) for name in TARGETS]
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "scope": "selected derived CSV indexes",
        "reason": "Keep legacy review state explicit and separate from primary usability gates.",
        "records": records,
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
