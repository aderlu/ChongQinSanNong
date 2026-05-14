from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


# 渲染函数负责为 Wiki 操作生成稳定的 Markdown 页面。
# 它们不判断临床结论是否正确，只把已经选定的元数据、来源和检索结果渲染成
# 统一格式，保证加载器、lint 和图谱构建器之后还能一致地读回来。

def today_iso() -> str:
    """返回本地日期，用于文件名和日志行。"""
    return datetime.now().astimezone().date().isoformat()


def now_iso() -> str:
    """返回带时区的时间戳，用于缓存和来源元数据。"""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str, *, fallback: str = "item") -> str:
    """把用户可读标题转换成稳定、适合文件名的 slug。"""
    text = str(value or "").strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text, flags=re.UNICODE)
    text = re.sub(r"-{2,}", "-", text).strip("-.")
    return text[:80] or fallback


def render_root_file(name: str, *, domain: str = "chicken_disease") -> str:
    """渲染 ``init_wiki`` 创建的默认根文件。

    这些文件记录 Wiki 目的、schema 期望、索引入口和操作历史。它们让一个
    新 Wiki 在尚未摄取领域证据前也具备基本结构。
    """
    date = today_iso()
    if name == "index.md":
        return f"# Chicken Disease LLM Wiki\n\n- domain: {domain}\n- initialized: {date}\n\n## Sections\n\n- [[Start-here-for-case-triage]]\n"
    if name == "purpose.md":
        return (
            "# Purpose\n\n"
            "This Wiki stores auditable chicken disease, drug, rule, source, and derived synthesis knowledge "
            "for generation, evaluation, arbitration, and rule checks.\n"
        )
    if name == ".wiki-schema.md":
        return (
            "# Wiki Schema\n\n"
            "Core page types: disease, drug, rule, rule_card, source, topic, syndrome, synthesis, comparison, session, query.\n\n"
            "Source pages must include source_id, source_path or external_url, source_type, authority_level, and evidence_status.\n"
        )
    if name == "log.md":
        return f"# Wiki Log\n\n{date} init | created or verified standard Wiki structure\n"
    return ""


def render_source_page(payload: Mapping[str, Any]) -> str:
    """根据来源元数据渲染一个 source Markdown 页面。

    source page 是 LLM Wiki 的追溯锚点。它记录来源来自哪里、权威等级如何、
    是否已复核，以及可选摘录，供人工和 LLM 在复核时查看。
    """
    created = str(payload.get("created") or today_iso())
    updated = str(payload.get("updated") or created)
    title = str(payload.get("title") or payload.get("source_id") or "Untitled source")
    source_id = str(payload.get("source_id") or "")
    source_path = str(payload.get("source_path") or "")
    external_url = str(payload.get("external_url") or "")
    source_type = str(payload.get("source_type") or "unknown")
    authority = str(payload.get("authority_level") or "unclassified")
    status = str(payload.get("evidence_status") or "NEEDS_REVIEW")
    summary = str(payload.get("summary") or "Pending human summary.")
    excerpt = str(payload.get("excerpt") or "").strip()
    url_line = f"external_url: {external_url}\n" if external_url else ""
    excerpt_block = f"\n## Excerpt\n\n{excerpt}\n" if excerpt else ""
    return (
        "---\n"
        "type: source\n"
        f"source_id: {source_id}\n"
        f"source_path: {source_path}\n"
        f"{url_line}"
        f"source_type: {source_type}\n"
        f"authority_level: {authority}\n"
        f"evidence_status: {status}\n"
        f"created: {created}\n"
        f"updated: {updated}\n"
        "sources: []\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Summary\n\n"
        f"{summary}\n\n"
        "## Basic Information\n\n"
        f"- Source ID: {source_id}\n"
        f"- Source type: {source_type}\n"
        f"- Source path: {source_path or external_url or 'manual'}\n"
        f"- Evidence status: {status}\n"
        f"{excerpt_block}"
        "\n## Audit Notes\n\n- Review authority level, source traceability, and clinical/regulatory claims before merging facts.\n"
    )


def render_digest_page(payload: Mapping[str, Any]) -> str:
    """根据 Wiki 页面命中和事实命中渲染派生摘要页面。"""
    title = str(payload.get("title") or payload.get("query") or "Wiki digest")
    query = str(payload.get("query") or title)
    created = str(payload.get("created") or today_iso())
    source_pages = list(payload.get("source_pages") or [])
    facts = list(payload.get("facts") or [])
    answer = str(payload.get("answer") or "")
    source_lines = "\n".join(f"- [[{Path(str(item)).stem}]] ({item})" for item in source_pages) or "- No source pages matched."
    fact_lines = "\n".join(
        f"- {fact.get('subject', '')} | {fact.get('predicate', '')} | {fact.get('object', '')} "
        f"(source={fact.get('evidence_source_id') or fact.get('evidence_source') or 'unknown'}, "
        f"status={fact.get('evidence_status') or 'UNKNOWN'})"
        for fact in facts
        if isinstance(fact, Mapping)
    ) or "- No structured facts matched."
    return (
        "---\n"
        "type: synthesis\n"
        "derived: true\n"
        f"created: {created}\n"
        "evidence_status: INFERRED\n"
        "sources: []\n"
        "---\n\n"
        f"# {title}\n\n"
        f"Query: {query}\n\n"
        "## Synthesis\n\n"
        f"{answer or 'This digest is generated from matching Wiki pages and structured facts. Human review is required before using it as authority.'}\n\n"
        "## Source Pages\n\n"
        f"{source_lines}\n\n"
        "## Structured Evidence\n\n"
        f"{fact_lines}\n"
    )
