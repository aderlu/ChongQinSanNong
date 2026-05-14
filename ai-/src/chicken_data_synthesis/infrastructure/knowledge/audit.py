from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from .wiki import load_llm_wiki

_SOURCE_ID_PATTERN = re.compile(r"\b(?:SRC-\d{3,4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+)\b")
_STATUS_PATTERN = re.compile(r"status=([A-Z_]+)")


# 审计函数负责把 Wiki 来源信息附加到生成/评估结果中。
# 它们不会重新检索知识库，而是统计已经传给 LLM 的那段上下文。这样后续 CSV
# 和报告就能回答：“这次生成或评估到底依赖了哪些 Wiki 证据？”

def build_wiki_audit_metadata(
    *,
    wiki_dir: str | Path,
    knowledge_context: str = "",
    query: str = "",
) -> dict[str, Any]:
    """为一次基于 Wiki 的操作构建简洁来源审计元数据。"""
    kb = load_llm_wiki(wiki_dir)
    source_ids = sorted(set(_SOURCE_ID_PATTERN.findall(str(knowledge_context or ""))))
    evidence_statuses = Counter(_STATUS_PATTERN.findall(str(knowledge_context or "")))
    return {
        "wiki_dir": str(Path(wiki_dir)),
        "wiki_fact_count": len(kb.facts),
        "wiki_page_count": len(kb.pages),
        "wiki_context_query": str(query or ""),
        "wiki_evidence_status_counts": dict(sorted(evidence_statuses.items())),
        "wiki_evidence_source_ids": source_ids,
        "wiki_context_chars": len(str(knowledge_context or "")),
    }


def compact_wiki_audit_for_csv(value: Mapping[str, Any] | None) -> dict[str, Any]:
    """把 Wiki 审计元数据展平成适合写入 CSV 的标量字段。"""
    data = dict(value or {})
    return {
        "wiki_dir": data.get("wiki_dir", ""),
        "wiki_fact_count": data.get("wiki_fact_count", ""),
        "wiki_page_count": data.get("wiki_page_count", ""),
        "wiki_context_query": data.get("wiki_context_query", ""),
        "wiki_evidence_status_counts": json.dumps(data.get("wiki_evidence_status_counts", {}), ensure_ascii=False),
        "wiki_evidence_source_ids": "|".join(data.get("wiki_evidence_source_ids", []) or []),
        "wiki_context_chars": data.get("wiki_context_chars", ""),
    }
