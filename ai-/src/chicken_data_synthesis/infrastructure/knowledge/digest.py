from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .rendering import render_digest_page, slugify, today_iso
from .wiki import load_llm_wiki


# 摘要生成功能用于展示“LLM Wiki 作为可维护知识库”的模式。
# 它会检索页面和事实，渲染派生总结，并可选择保存到 ``wiki/synthesis`` 或
# ``wiki/comparisons``。注意：摘要是派生产物，不会被提升为正式事实。

@dataclass(frozen=True)
class DigestResult:
    """已保存摘要页面的结果摘要。"""

    wiki_dir: str
    query: str
    format: str
    saved_path: str
    source_count: int
    fact_count: int


def build_digest(
    wiki_dir: str | Path,
    query: str,
    *,
    output_format: str = "quick",
    save: bool = False,
) -> DigestResult | dict[str, object]:
    """根据当前 Wiki 检索结果创建派生摘要。

    ``save=False`` 时只返回预览内容，供 CLI 或 UI 展示；``save=True`` 时会
    写入页面并追加日志。无论是否保存，摘要都只是二次综合，不会修改正式
    事实导出文件。
    """
    root = Path(wiki_dir)
    kb = load_llm_wiki(root)
    hits = kb.search(query, top_k=8)
    facts = kb.search_facts(query, top_k=10)
    source_pages = [hit.relpath for hit in hits]
    answer_lines = [
        "This digest is derived from Wiki search results and structured facts.",
        "Use it as secondary synthesis only; verify source pages before final clinical or regulatory conclusions.",
    ]
    if hits:
        answer_lines.append("Top matching pages: " + ", ".join(hit.title for hit in hits[:5]))
    if facts:
        answer_lines.append(f"Matching structured facts: {len(facts)}")
    payload = {
        "query": query,
        "title": query,
        "source_pages": source_pages,
        "facts": facts,
        "answer": "\n\n".join(answer_lines),
    }
    if not save:
        return {
            "wiki_dir": str(root),
            "query": query,
            "format": output_format,
            "source_pages": source_pages,
            "facts": list(facts),
            "content": render_digest_page(payload),
        }

    target_dir = root / "wiki" / ("comparisons" if output_format == "comparison" else "synthesis")
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{today_iso()}-{slugify(query, fallback='digest')}.md"
    path.write_text(render_digest_page(payload), encoding="utf-8")
    _append_log(root, f"{today_iso()} digest | {query} | {path.relative_to(root).as_posix()}")
    return DigestResult(
        wiki_dir=str(root),
        query=query,
        format=output_format,
        saved_path=str(path),
        source_count=len(source_pages),
        fact_count=len(facts),
    )


def _append_log(root: Path, line: str) -> None:
    """向 Wiki 操作日志追加一条摘要创建记录。"""
    with (root / "log.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n{line}\n")
