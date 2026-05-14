from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
ISSUES = ROOT / "issues"
REPORT = ISSUES / "legacy_evidence_status_migration_2026-05-12.json"
TZ = timezone(timedelta(hours=8))


def split_frontmatter(text: str) -> tuple[list[str], str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end].splitlines(), text[end + 5 :]


def render(frontmatter: list[str], body: str) -> str:
    return "---\n" + "\n".join(frontmatter).rstrip() + "\n---\n" + body


def migrate_file(path: Path) -> dict[str, object] | None:
    text = path.read_text(encoding="utf-8")
    split = split_frontmatter(text)
    if split is None:
        return None
    frontmatter, body = split

    old_status = ""
    has_legacy = False
    migrated: list[str] = []
    changed = False
    for line in frontmatter:
        if line.startswith("legacy_evidence_status:"):
            has_legacy = True
            migrated.append(line)
        elif line.startswith("evidence_status:"):
            old_status = line.split(":", 1)[1].strip()
            if not has_legacy:
                migrated.append(f"legacy_evidence_status: {old_status}")
            changed = True
        else:
            migrated.append(line)

    if not changed:
        return None

    path.write_text(render(migrated, body), encoding="utf-8")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "old_field": "evidence_status",
        "new_field": "legacy_evidence_status" if not has_legacy else "existing_legacy_evidence_status",
        "value": old_status,
    }


def main() -> int:
    records = []
    for path in sorted(WIKI.rglob("*.md")):
        record = migrate_file(path)
        if record:
            records.append(record)

    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "scope": "wiki markdown front matter only",
        "reason": "evidence_status is a legacy audit field; current usability gates use source_status, fact_validity, authority_level, risk_class, and task_use_status.",
        "changed_files": len(records),
        "records": records,
    }
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
