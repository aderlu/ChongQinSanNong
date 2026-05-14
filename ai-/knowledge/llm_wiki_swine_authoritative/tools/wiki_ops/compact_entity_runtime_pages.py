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

REPORT_JSON = ISSUES / "entity_runtime_compaction_2026-05-09.json"
REPORT_MD = ISSUES / "entity_runtime_compaction_2026-05-09.md"

MARKED_BLOCK_RE = re.compile(
    r"(?P<block><!--\s*(?P<name>[A-Z0-9_]+)_START\s*-->.*?<!--\s*(?P=name)_END\s*-->)",
    flags=re.DOTALL,
)

SOURCE_ID_RE = re.compile(r"\b(?:A0|A1|A2|SRC|RC|RULE|SYN|CMP)-[A-Z0-9-]+")

LEGACY_HEADING_PATTERNS = [
    "Formal Disease Completion",
    "Targeted Disease Completion",
    "Dataset QA Reinforcement",
    "Low Frequency Virus QA Reinforcement",
    "Authority Web Reinforcement",
    "MOA Suffix Crawl Reinforcement",
    "MOA A0 Authority Reinforcement",
    "Zoonotic Authority Reinforcement",
    "Web Source Reinforcement",
    "Formal Batch",
    "Source-Anchored Completion",
    "Phase 2 Gold Anchors",
    "Dataset Alias",
    "Raw MD textbook evidence",
    "Handbook prescription evidence",
    "Handbook enrichment",
    "生成与评估边界",
    "黄金集用途",
    "B-task 核心栏目补强",
    "补强",
    "增强",
]

RENAME_HEADINGS = {
    "## Source-first 标签证据使用边界 / V11.1": "## 标签/来源使用边界",
}


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return value[:120] or "section"


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :]
    return "", text


def source_ids(text: str) -> list[str]:
    return sorted(set(SOURCE_ID_RE.findall(text)))


def write_expansion(entity_type: str, page: Path, name: str, content: str, reason: str, ordinal: int) -> dict[str, object]:
    out_dir = EXPANSIONS / entity_type / "phase4_runtime_compaction" / page.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    candidate = ordinal
    while True:
        out_path = out_dir / f"{candidate:03d}-{slug(name)}.md"
        if not out_path.exists():
            break
        candidate += 1
    rel_source = page.relative_to(ROOT).as_posix()
    rel_out = out_path.relative_to(ROOT).as_posix()
    ids = source_ids(content)
    title = name.replace("_", " ")
    expansion = [
        "---",
        "tags: [evidence_expansion, swine, phase4_runtime_compaction]",
        f"source_page: {rel_source}",
        f"original_section: {json.dumps(name, ensure_ascii=False)}",
        f"migration_reason: {json.dumps(reason, ensure_ascii=False)}",
        f"source_ids: [{', '.join(ids)}]",
        "default_runtime: false",
        f"updated: {datetime.now(TZ).isoformat(timespec='seconds')}",
        "---",
        "",
        f"# {page.stem} / {title}",
        "",
        "This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.",
        "It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.",
        "",
        "## Original Content",
        "",
        content.strip(),
        "",
    ]
    out_path.write_text("\n".join(expansion), encoding="utf-8")
    return {
        "name": name,
        "reason": reason,
        "path": rel_out,
        "source_ids": ids,
        "bytes": len(content.encode("utf-8")),
    }


def strip_batch_phrase(text: str) -> str:
    text = re.sub(r"；批处理增强块：[^。\n]*。", "；证据扩展：见本页“证据扩展索引”。", text)
    text = re.sub(r"批处理增强块：无批处理增强块", "证据扩展：无迁移扩展块", text)
    return text


def should_move_heading(heading: str) -> bool:
    if heading in RENAME_HEADINGS:
        return False
    return any(pattern in heading for pattern in LEGACY_HEADING_PATTERNS)


def move_legacy_h2_sections(body: str, entity_type: str, page: Path, moved: list[dict[str, object]]) -> str:
    lines = body.splitlines(keepends=True)
    h2_positions = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if not h2_positions:
        return body
    h2_positions.append(len(lines))
    remove_ranges = []
    for idx in range(len(h2_positions) - 1):
        start = h2_positions[idx]
        end = h2_positions[idx + 1]
        heading = lines[start].strip()
        if should_move_heading(heading):
            section = "".join(lines[start:end])
            moved.append(
                write_expansion(
                    entity_type=entity_type,
                    page=page,
                    name=heading.lstrip("# ").strip(),
                    content=section,
                    reason="legacy H2 construction or reinforcement section moved out of default runtime",
                    ordinal=len(moved) + 1,
                )
            )
            remove_ranges.append((start, end))
    if not remove_ranges:
        return body
    kept = []
    cursor = 0
    for start, end in remove_ranges:
        kept.extend(lines[cursor:start])
        cursor = end
    kept.extend(lines[cursor:])
    return "".join(kept)


def replace_marked_blocks(body: str, entity_type: str, page: Path, moved: list[dict[str, object]]) -> str:
    def repl(match: re.Match[str]) -> str:
        name = match.group("name")
        block = match.group("block")
        moved.append(
            write_expansion(
                entity_type=entity_type,
                page=page,
                name=name,
                content=block,
                reason="marked batch evidence block moved out of default runtime",
                ordinal=len(moved) + 1,
            )
        )
        return "\n"

    return MARKED_BLOCK_RE.sub(repl, body)


def remove_existing_index(body: str) -> tuple[str, list[str]]:
    existing: list[str] = []

    def capture(match: re.Match[str]) -> str:
        section = match.group(0)
        existing.extend(
            line for line in section.splitlines()
            if line.startswith("- `wiki/evidence_expansions/")
        )
        return "\n"

    pattern = re.compile(r"\n## 证据扩展索引\n\n.*?(?=\n## |\Z)", flags=re.DOTALL)
    return pattern.sub(capture, body), existing


def append_index(body: str, moved: list[dict[str, object]], existing_entries: list[str]) -> str:
    if not moved and not existing_entries:
        return body
    lines = [
        "",
        "## 证据扩展索引",
        "",
        "- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。",
        "- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。",
    ]
    seen = set()
    for line in existing_entries:
        if line not in seen:
            lines.append(line)
            seen.add(line)
    for item in moved:
        ids = ", ".join(item["source_ids"]) if item["source_ids"] else "source anchors retained in expansion"
        line = f"- `{item['path']}`：{item['name']}；sources: {ids}。"
        if line not in seen:
            lines.append(line)
            seen.add(line)
    lines.append("")
    return body.rstrip() + "\n" + "\n".join(lines)


def normalize_page(path: Path, entity_type: str) -> dict[str, object]:
    original = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(original)
    body = strip_batch_phrase(body)
    for old, new in RENAME_HEADINGS.items():
        body = body.replace(old, new)
    body, existing_index_entries = remove_existing_index(body)
    moved: list[dict[str, object]] = []
    body = replace_marked_blocks(body, entity_type, path, moved)
    body = move_legacy_h2_sections(body, entity_type, path, moved)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = append_index(body, moved, existing_index_entries)
    updated = frontmatter + body
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "entity_type": entity_type,
        "changed": changed,
        "moved_sections": moved,
        "moved_count": len(moved),
        "bytes_before": len(original.encode("utf-8")),
        "bytes_after": len(updated.encode("utf-8")),
    }


def main() -> None:
    results = []
    for entity_type, dirname in [("diseases", "diseases"), ("drugs", "drugs")]:
        for path in sorted((WIKI / dirname).glob("*.md")):
            results.append(normalize_page(path, entity_type))
    changed = [r for r in results if r["changed"]]
    moved_count = sum(r["moved_count"] for r in results)
    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "pages_scanned": len(results),
        "pages_changed": len(changed),
        "moved_sections": moved_count,
        "evidence_expansion_root": (EXPANSIONS / "{diseases,drugs}" / "phase4_runtime_compaction").as_posix(),
    }
    payload = {"summary": summary, "results": results}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Entity Runtime Compaction / Phase 4",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Pages scanned: {summary['pages_scanned']}",
        f"- Pages changed: {summary['pages_changed']}",
        f"- Moved sections: {summary['moved_sections']}",
        "",
        "## Changed Pages",
        "",
    ]
    for item in changed[:200]:
        lines.append(
            f"- `{item['path']}` moved={item['moved_count']} bytes_before={item['bytes_before']} bytes_after={item['bytes_after']}"
        )
    if not changed:
        lines.append("- None")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
