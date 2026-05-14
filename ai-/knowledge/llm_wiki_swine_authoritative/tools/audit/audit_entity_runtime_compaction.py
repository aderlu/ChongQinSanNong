from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
ISSUES = ROOT / "issues"
EXPANSIONS = WIKI / "evidence_expansions"
TZ = timezone(timedelta(hours=8))

REPORT_JSON = ISSUES / "entity_runtime_compaction_cumulative_2026-05-09.json"
REPORT_MD = ISSUES / "entity_runtime_compaction_cumulative_2026-05-09.md"

LEGACY_RE = re.compile(
    r"^## .*?(?:V[0-9]|Reinforcement|补强|增强|Completion|Batch)|<!-- .*_START|<!-- .*_END",
    flags=re.MULTILINE,
)


def scan_pages() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    records = []
    legacy_hits = []
    for entity_type, dirname in [("diseases", "diseases"), ("drugs", "drugs")]:
        for path in sorted((WIKI / dirname).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            hits = LEGACY_RE.findall(text)
            item = {
                "path": rel,
                "entity_type": entity_type,
                "bytes": path.stat().st_size,
                "has_evidence_expansion_index": "## 证据扩展索引" in text,
                "legacy_heading_or_marker_hits": len(hits),
            }
            records.append(item)
            if hits:
                legacy_hits.append({"path": rel, "hits": hits})
    return records, legacy_hits


def count_expansions() -> dict[str, int]:
    counts = {"diseases": 0, "drugs": 0}
    for entity_type in counts:
        root = EXPANSIONS / entity_type / "phase4_runtime_compaction"
        counts[entity_type] = len(list(root.rglob("*.md"))) if root.exists() else 0
    return counts


def main() -> None:
    pages, legacy_hits = scan_pages()
    expansion_counts = count_expansions()
    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "pages_scanned": len(pages),
        "pages_with_evidence_expansion_index": sum(1 for p in pages if p["has_evidence_expansion_index"]),
        "remaining_legacy_heading_or_marker_pages": len(legacy_hits),
        "remaining_legacy_heading_or_marker_hits": sum(len(item["hits"]) for item in legacy_hits),
        "evidence_expansion_files": expansion_counts,
        "evidence_expansion_files_total": sum(expansion_counts.values()),
        "max_runtime_page_bytes": max((p["bytes"] for p in pages), default=0),
    }
    REPORT_JSON.write_text(
        json.dumps({"summary": summary, "remaining_legacy_hits": legacy_hits, "pages": pages}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# Entity Runtime Compaction Cumulative Audit / Phase 4",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Pages scanned: {summary['pages_scanned']}",
        f"- Pages with evidence expansion index: {summary['pages_with_evidence_expansion_index']}",
        f"- Remaining legacy heading or marker pages: {summary['remaining_legacy_heading_or_marker_pages']}",
        f"- Remaining legacy heading or marker hits: {summary['remaining_legacy_heading_or_marker_hits']}",
        f"- Disease expansion files: {expansion_counts['diseases']}",
        f"- Drug expansion files: {expansion_counts['drugs']}",
        f"- Evidence expansion files total: {summary['evidence_expansion_files_total']}",
        f"- Max runtime page bytes: {summary['max_runtime_page_bytes']}",
        "",
    ]
    if legacy_hits:
        lines.extend(["## Remaining Legacy Hits", ""])
        for item in legacy_hits:
            lines.append(f"- `{item['path']}`: {len(item['hits'])}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
