from __future__ import annotations

import importlib.util
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal


# 注册表是 LLM Wiki 的来源适配器契约。它告诉摄取代码：支持哪些输入形式、
# 原始证据应该保存到哪个 raw 子目录、是否需要额外依赖、依赖缺失时如何
# 人工兜底。这样来源获取过程是明确的、可审计的。

AdapterState = Literal[
    "available",
    "missing_dependency",
    "manual_only",
    "failed_retryable",
    "failed_manual_fallback",
]


@dataclass(frozen=True)
class SourceType:
    """描述一种受支持的证据输入类型。

    ``raw_dir`` 是契约的一部分，保证不同证据类型进入固定 raw 子目录。
    ``fallback_hint`` 用来告诉 CLI 和文档：当适配器不可用时，人工应该如何
    补充材料。
    """

    source_id: str
    source_label: str
    source_category: str
    input_mode: str
    raw_dir: str
    adapter_name: str
    dependency_name: str
    fallback_hint: str
    extensions: tuple[str, ...] = ()
    url_pattern: str = ""

    def to_dict(self) -> dict[str, object]:
        """把适配器契约转换成字典，供 CLI 状态输出使用。"""
        return asdict(self)


SOURCE_TYPES: tuple[SourceType, ...] = (
    # 内置类型使用 Python 标准库处理，或只做简单文件复制。
    SourceType("markdown", "Markdown file", "core_builtin", "file", "raw/notes", "builtin", "", "Copy the markdown file into raw/notes.", (".md", ".markdown")),
    SourceType("text", "Text file", "core_builtin", "file", "raw/notes", "builtin", "", "Copy the text file into raw/notes.", (".txt",)),
    SourceType("html", "HTML file", "core_builtin", "file", "raw/html", "builtin", "", "Copy the HTML file into raw/html.", (".html", ".htm")),
    SourceType("pdf", "PDF file", "core_builtin", "file", "raw/pdfs", "pypdf", "pypdf", "Install pypdf or provide extracted text/markdown manually.", (".pdf",)),
    # 网址先作为来源元数据记录；正文需要由受控网页访问或搜索流程抓取，
    # 或由人工保存为 HTML/text 后再摄取。
    SourceType("url", "Web URL", "manual_only", "url", "raw/urls", "manual", "", "Save URL as a source record and provide article text or HTML manually.", (), r"^https?://"),
    SourceType("plain_text", "Plain text", "core_builtin", "text", "raw/notes", "builtin", "", "Use ingest-text or provide a text file.", ()),
)


def list_source_types() -> tuple[SourceType, ...]:
    """按稳定顺序返回全部已注册来源适配器。"""
    return SOURCE_TYPES


def source_type_by_id(source_id: str) -> SourceType | None:
    """根据稳定 ID 查找一个来源适配器。"""
    wanted = str(source_id or "").strip().lower()
    for source_type in SOURCE_TYPES:
        if source_type.source_id == wanted:
            return source_type
    return None


def match_source_input(value: str) -> SourceType:
    """根据用户输入推断应该使用哪个来源适配器。"""
    text = str(value or "").strip()
    if re.match(r"^https?://", text, flags=re.IGNORECASE):
        return source_type_by_id("url") or SOURCE_TYPES[-2]
    suffix = Path(text).suffix.lower()
    for source_type in SOURCE_TYPES:
        if suffix and suffix in source_type.extensions:
            return source_type
    return source_type_by_id("plain_text") or SOURCE_TYPES[-1]


def adapter_state(source_id: str) -> dict[str, str]:
    """报告某个适配器在当前环境中是否可用。"""
    source_type = source_type_by_id(source_id)
    if source_type is None:
        return {
            "source_id": source_id,
            "state": "failed_manual_fallback",
            "adapter_name": "",
            "dependency_name": "",
            "fallback_hint": "Unknown source type.",
        }
    if source_type.source_category == "manual_only":
        state: AdapterState = "manual_only"
    elif not source_type.dependency_name or source_type.dependency_name == "builtin":
        state = "available"
    elif importlib.util.find_spec(source_type.dependency_name) is None:
        state = "missing_dependency"
    else:
        state = "available"
    return {
        "source_id": source_type.source_id,
        "state": state,
        "adapter_name": source_type.adapter_name,
        "dependency_name": source_type.dependency_name,
        "fallback_hint": source_type.fallback_hint,
    }
