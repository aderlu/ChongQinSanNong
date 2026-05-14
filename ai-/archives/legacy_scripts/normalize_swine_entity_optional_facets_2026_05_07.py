from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"

OPTIONAL_FACETS = [
    "\u4f20\u64ad\u9014\u5f84",  # transmission
    "\u4e34\u5e8a\u75c7\u72b6",  # clinical signs
    "\u5256\u68c0\u53d8\u5316",  # necropsy findings
    "\u5b9e\u9a8c\u5ba4\u8bca\u65ad",  # laboratory diagnosis
    "\u9274\u522b\u8bca\u65ad",  # differential diagnosis
    "\u9632\u63a7\u8981\u70b9",  # control points
]
EVIDENCE_RE = re.compile(
    r"(?:source_id=|fact_id=|SRC-\d{4}|A0-[A-Z0-9-]+|A1-[A-Z0-9-]+|A2-[A-Z0-9-]+|RC-[A-Z0-9-]+|https?://|PDF page)"
)
PLACEHOLDER_RE = re.compile(
    r"(?:\u5f85\u6b63\u6587\u62bd\u53d6|\u6682\u65e0\u53ef\u81ea\u52a8\u6620\u5c04|\u4e0d\u5f97\u7f16\u9020|\u4e0d\u53ef\u4f5c\u4e3a\u5b8c\u6574\u4e34\u5e8a\u77e5\u8bc6\u9875|NEEDS_REVIEW)"
)


def split_h2_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.M))
    if not matches:
        return text, []
    prefix = text[: matches[0].start()].rstrip()
    sections: list[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        heading = match.group(1).strip()
        body = text[match.end() : end].strip()
        sections.append((heading, body))
    return prefix, sections


def render_section(heading: str, body: str) -> str:
    body = body.strip()
    return f"## {heading}\n\n{body}" if body else f"## {heading}"


def has_source_anchored_evidence(body: str) -> bool:
    if not EVIDENCE_RE.search(body):
        return False
    non_empty_lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not non_empty_lines:
        return False
    only_placeholder = all(PLACEHOLDER_RE.search(line) for line in non_empty_lines)
    return not only_placeholder


def collect_nested_evidence(text: str) -> dict[str, str]:
    found: dict[str, list[str]] = {heading: [] for heading in OPTIONAL_FACETS}
    for heading in OPTIONAL_FACETS:
        pattern = rf"^###\s+{re.escape(heading)}\s*\n(.*?)(?=\n### |\n## |\Z)"
        for match in re.finditer(pattern, text, flags=re.S | re.M):
            body = match.group(1).strip()
            if has_source_anchored_evidence(body) and body not in found[heading]:
                found[heading].append(body)
    return {heading: "\n\n".join(bodies) for heading, bodies in found.items() if bodies}


def optional_block(evidence: dict[str, str], gaps: list[str]) -> str:
    lines: list[str] = [
        "## Evidence-backed optional facets",
        "",
        "- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/SRC/A0/A1 anchor exists.",
        "- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.",
    ]
    for heading in OPTIONAL_FACETS:
        body = evidence.get(heading, "").strip()
        if body:
            lines.extend(["", f"### {heading}", "", body])
    if gaps:
        lines.extend(
            [
                "",
                "## Evidence gaps",
                "",
                "- Optional facets without attached source-anchored/A0/A1 evidence: "
                + "\u3001".join(gaps)
                + ".",
                "- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.",
            ]
        )
    return "\n".join(lines)


def normalize_page(path: Path) -> bool:
    original = path.read_text(encoding="utf-8-sig", errors="replace")
    prefix, sections = split_h2_sections(original)
    if not sections:
        return False

    nested_evidence = collect_nested_evidence(original)
    filtered: list[tuple[str, str]] = []
    captured: dict[str, str] = dict(nested_evidence)
    gaps: list[str] = []
    changed = False

    for heading, body in sections:
        if heading in {"Evidence-backed optional facets", "Evidence gaps"}:
            changed = True
            continue
        if heading in OPTIONAL_FACETS:
            changed = True
            if has_source_anchored_evidence(body):
                if heading in captured and body not in captured[heading]:
                    captured[heading] = body + "\n\n" + captured[heading]
                else:
                    captured[heading] = body
            else:
                gaps.append(heading)
            continue
        filtered.append((heading, body))

    if not changed:
        return False

    insert_at = 1
    for idx, (heading, _body) in enumerate(filtered):
        if heading in {"\u82f1\u6587/\u6559\u6750\u7ae0\u8282\u540d", "\u82f1\u8bed/\u6559\u6750\u7ae0\u8282\u540d"}:
            insert_at = idx + 1
            break

    final_gaps = [heading for heading in OPTIONAL_FACETS if heading not in captured]
    filtered.insert(insert_at, ("__OPTIONAL_BLOCK__", optional_block(captured, final_gaps)))

    rendered = [prefix] if prefix else []
    for heading, body in filtered:
        if heading == "__OPTIONAL_BLOCK__":
            rendered.append(body.strip())
        else:
            rendered.append(render_section(heading, body))
    new_text = "\n\n".join(part.rstrip() for part in rendered).rstrip() + "\n"
    if new_text != original:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed_pages = []
    for page in sorted((WIKI / "wiki" / "diseases").glob("*.md")):
        if normalize_page(page):
            changed_pages.append(page.name)

    report = WIKI / "issues" / "optional_facets_normalization_2026-05-07.md"
    lines = [
        "# Optional Facets Normalization",
        "",
        "Date: 2026-05-07",
        "",
        "Policy:",
        "- Disease entity pages no longer require fixed H2 sections for transmission, clinical signs, necropsy, laboratory diagnosis, differential diagnosis, or control.",
        "- Source-anchored content from those sections is preserved under `Evidence-backed optional facets`.",
        "- Unsourced placeholders are represented as `Evidence gaps` and must not be treated as generation or evaluation failures.",
        "",
        f"Changed disease pages: {len(changed_pages)}",
        "",
    ]
    lines.extend(f"- `{name}`" for name in changed_pages)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"changed={len(changed_pages)}")


if __name__ == "__main__":
    main()
