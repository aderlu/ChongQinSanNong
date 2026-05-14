from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.M)
    return match.group(1).strip() if match else ""


def title_from_page(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return match.group(1).strip() if match else fallback


def merge_authority_source_index() -> None:
    canonical = WIKI / "exports" / "source_index.csv"
    sidecar = WIKI / "wiki" / "exports" / "source_index.csv"
    rows = read_csv(canonical)
    existing = {row.get("source_id", "") for row in rows}
    fields = ["source_id", "title", "pages", "evidence_status", "relpath"]

    for side in read_csv(sidecar):
        source_id = side.get("source_id", "")
        if not source_id or source_id in existing:
            continue
        file_value = side.get("file", "")
        relpath = file_value if file_value.startswith("wiki/") else f"wiki/{file_value}"
        page = WIKI / relpath
        text = page.read_text(encoding="utf-8", errors="replace") if page.exists() else ""
        rows.append({
            "source_id": source_id,
            "title": title_from_page(text, source_id),
            "pages": side.get("url", "") or frontmatter_value(text, "url") or "accessed 2026-05-07",
            "evidence_status": frontmatter_value(text, "evidence_status") or "HUMAN_REVIEWED",
            "relpath": relpath,
        })
        existing.add(source_id)

    write_csv(canonical, fields, rows)

    side_report = WIKI / "wiki" / "issues" / "authority_source_registry_report.md"
    if side_report.exists():
        target = WIKI / "issues" / "authority_source_registry_report.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(side_report, target)


def section_body(text: str, heading: str, level: str = "##") -> str:
    pattern = rf"{re.escape(level)} {re.escape(heading)}\n(.*?)(?=\n{re.escape(level)} |\Z)"
    match = re.search(pattern, text, flags=re.S)
    return match.group(1).strip() if match else ""


def replace_canonical_section(text: str, heading: str, body: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return text
    body_start = start + len(marker)
    next_start = text.find("\n## ", body_start)
    if next_start < 0:
        next_start = len(text)
    return text[:body_start].rstrip() + "\n\n" + body.rstrip() + "\n" + text[next_start:]


def normalize_b_task_disease_sections() -> None:
    report_rows: list[str] = ["# Parallel B-task Canonical Section Normalization", ""]
    for page in sorted((WIKI / "wiki" / "diseases").glob("*.md")):
        text = page.read_text(encoding="utf-8", errors="replace")
        marker = "## B-task 核心栏目补强"
        if marker not in text:
            continue
        block = text[text.find(marker):]
        changed_sections: list[str] = []
        for heading in ["传播途径", "临床症状", "剖检变化"]:
            match = re.search(rf"### {re.escape(heading)}\n(.*?)(?=\n### |\n## |\Z)", block, flags=re.S)
            body = match.group(1).strip() if match else ""
            if body and "source_id=" in body and "PDF page" in body:
                text = replace_canonical_section(text, heading, body)
                changed_sections.append(heading)
        if changed_sections:
            page.write_text(text, encoding="utf-8", newline="\n")
            report_rows.append(f"- `{page.name}`: {', '.join(changed_sections)}")
    (WIKI / "issues" / "parallel_b_task_canonical_section_normalization.md").write_text(
        "\n".join(report_rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    merge_authority_source_index()
    # Disease clinical facets are now evidence-driven optional dimensions.
    # Do not repopulate canonical H2 sections such as 传播途径/剖检变化 from
    # sidecar batches; sourced facts remain available in batch sections and can
    # be surfaced by the optional-facet normalizer when needed.


if __name__ == "__main__":
    main()
