import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
MANIFEST = EXPORTS / "runtime_core_manifest.json"

REPORT_JSON = ISSUES / "phase2_encoding_quarantine_2026-05-09.json"
REPORT_MD = ISSUES / "phase2_encoding_quarantine_2026-05-09.md"

TZ = timezone(timedelta(hours=8))
BAD_CHAR = "\ufffd"


def load_manifest_entries():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return payload.get("entries", [])


def source_anchor(line):
    source_id = ""
    page = ""
    source_line = ""
    fact_id = ""
    fact_match = re.search(r"`([^`]+)`", line)
    if fact_match:
        fact_id = fact_match.group(1)
    source_match = re.search(r"source_id=([^;`\s]+)", line)
    if source_match:
        source_id = source_match.group(1)
    page_match = re.search(r"page=([^;`\s]+)", line)
    if page_match:
        page = page_match.group(1)
    line_match = re.search(r"line=([^;`\s]+)", line)
    if line_match:
        source_line = line_match.group(1)
    return {
        "fact_id": fact_id,
        "source_id": source_id,
        "page": page,
        "line": source_line,
    }


def replacement_line(anchor):
    bits = []
    if anchor["fact_id"]:
        bits.append(f"fact_id={anchor['fact_id']}")
    if anchor["source_id"]:
        bits.append(f"source_id={anchor['source_id']}")
    if anchor["page"]:
        bits.append(f"page={anchor['page']}")
    if anchor["line"]:
        bits.append(f"line={anchor['line']}")
    anchor_text = "; ".join(bits) if bits else "anchor unavailable"
    return (
        "- PHASE2_ENCODING_QUARANTINED: one damaged extracted fact line was removed "
        "from runtime text because it contained UTF-8 replacement characters. "
        f"See `issues/phase2_encoding_quarantine_2026-05-09.md`. Original anchor: {anchor_text}."
    )


def process_entry(entry):
    relpath = entry.get("path", "")
    path = ROOT / relpath
    if not path.exists() or path.suffix.lower() != ".md":
        return []

    text = path.read_text(encoding="utf-8", errors="replace")
    if BAD_CHAR not in text:
        return []

    lines = text.splitlines()
    changed = False
    quarantined = []
    new_lines = []
    for idx, line in enumerate(lines, start=1):
        if BAD_CHAR not in line:
            new_lines.append(line)
            continue
        anchor = source_anchor(line)
        quarantined.append({
            "page_id": entry.get("page_id", ""),
            "path": relpath,
            "line_number": idx,
            "replacement_char_count": line.count(BAD_CHAR),
            "anchor": anchor,
            "original_line": line,
        })
        new_lines.append(replacement_line(anchor))
        changed = True

    if changed:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return quarantined


def write_reports(records):
    generated_at = datetime.now(TZ).isoformat(timespec="seconds")
    payload = {
        "generated_at": generated_at,
        "purpose": "Phase 2 quarantine of runtime Markdown lines containing UTF-8 replacement characters.",
        "records": records,
        "record_count": len(records),
        "files": sorted({record["path"] for record in records}),
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 2 Encoding Quarantine / 2026-05-09",
        "",
        f"Generated: {generated_at}",
        f"Records: {len(records)}",
        "",
        "## Quarantined Runtime Lines",
        "",
    ]
    if not records:
        lines.append("- None")
    for record in records:
        anchor = record["anchor"]
        bits = []
        for key in ["fact_id", "source_id", "page", "line"]:
            if anchor.get(key):
                bits.append(f"{key}={anchor[key]}")
        lines.append(
            f"- `{record['path']}` line {record['line_number']}: "
            f"replacement_chars={record['replacement_char_count']}; "
            f"{'; '.join(bits) if bits else 'anchor unavailable'}"
        )
    lines.extend([
        "",
        "## Runtime Handling",
        "",
        "- The damaged original lines were removed from runtime Markdown pages.",
        "- Each affected page now contains a clean PHASE2_ENCODING_QUARANTINED placeholder with the original source anchor when available.",
        "- Original damaged text is preserved in the JSON report for audit and future re-extraction.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    records = []
    for entry in load_manifest_entries():
        records.extend(process_entry(entry))
    write_reports(records)
    print(json.dumps({
        "quarantined_lines": len(records),
        "files": sorted({record["path"] for record in records}),
        "report_json": str(REPORT_JSON.relative_to(ROOT)),
        "report_md": str(REPORT_MD.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

