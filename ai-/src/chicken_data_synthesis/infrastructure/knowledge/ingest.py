from __future__ import annotations
"""鸡病 LLM Wiki 的来源摄取模块。

摄取流程始终遵循“原始证据优先”的模式：
    1. 先把原始材料保存到 ``raw/``，保证证据可回看。
    2. 再创建可追溯的 ``wiki/sources/SRC-xxxx`` 来源页。
    3. 最后写入一条候选事实，等待复核。

这个模块有一个非常重要的边界：它不会直接修改正式事实库
``knowledge_facts.json``。无论输入来自 LLM、人工粘贴、URL 还是本地文件，
都必须先进入候选层，避免未复核信息污染生成和评估流程。
"""

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .cache import cache_check, cache_update
from .registry import adapter_state, match_source_input
from .rendering import render_source_page, slugify, today_iso


@dataclass(frozen=True)
class IngestResult:
    """文件、文本或 URL 摄取命令的返回结果。

    该结果记录 raw 文件路径、source page 路径、候选事实文件路径和 warning，
    方便 CLI 展示“这次摄取到底落到了哪里”。
    """
    wiki_dir: str
    input: str
    source_type: str
    cache_hit: bool
    raw_path: str
    source_page: str
    candidates_path: str
    warnings: tuple[str, ...]


def ingest_file(
    wiki_dir: str | Path,
    input_path: str | Path,
    *,
    title: str = "",
    summary: str = "",
) -> IngestResult:
    """把一个本地支持文件摄取到 raw、source 和 candidate 三层。

    例如 Markdown、TXT、HTML、PDF 等文件会先复制到对应的 ``raw/`` 子目录，
    然后生成来源页，最后追加候选事实。这样即使后续复核发现内容不合格，
    也能保留摄取过程和原始材料。
    """
    root = Path(wiki_dir)
    source = Path(input_path)
    if not source.is_file():
        raise FileNotFoundError(str(source))
    source_type = match_source_input(str(source))
    state = adapter_state(source_type.source_id)
    warnings: list[str] = []
    if state["state"] == "missing_dependency":
        warnings.append(f"adapter_missing_dependency:{source_type.source_id}:{state['fallback_hint']}")

    raw_dir = root / source_type.raw_dir
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = _unique_path(raw_dir / source.name)
    if source.resolve() != raw_path.resolve():
        shutil.copy2(source, raw_path)

    source_page = create_source_page(
        root,
        raw_path,
        title=title or source.stem,
        source_type=source_type.source_id,
        summary=summary,
    )
    check = cache_check(root, raw_path)
    if not check["hit"]:
        cache_update(root, raw_path, source_page, title=title or source.stem)
    candidates_path = write_candidate_facts(root, title=title or source.stem, source_page=source_page)
    _append_log(root, f"{today_iso()} ingest | {raw_path.relative_to(root).as_posix()} | {source_page.relative_to(root).as_posix()}")
    return IngestResult(
        wiki_dir=str(root),
        input=str(source),
        source_type=source_type.source_id,
        cache_hit=bool(check["hit"]),
        raw_path=str(raw_path),
        source_page=str(source_page),
        candidates_path=str(candidates_path),
        warnings=tuple(warnings),
    )


def ingest_url(
    wiki_dir: str | Path,
    url: str,
    *,
    title: str = "",
    summary: str = "",
) -> IngestResult:
    """把 URL 记录为需要人工处理的来源候选。

    这个函数不会抓取网页正文，也不会抽取事实。它只把 URL 保存到
    ``raw/urls``，并创建一个 ``NEEDS_REVIEW`` 的来源页，表示后续需要人工
    或受控抓取流程补充正文和复核。
    """
    root = Path(wiki_dir)
    text = str(url or "").strip()
    if not text.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")
    raw_dir = root / "raw" / "urls"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = _unique_path(raw_dir / f"{slugify(title or text, fallback='url')}.url.txt")
    raw_path.write_text(text + "\n", encoding="utf-8")
    page = create_source_page(
        root,
        raw_path,
        title=title or text,
        source_type="url",
        summary=summary or "URL source record. Provide extracted article text manually before merging facts.",
        external_url=text,
    )
    cache_update(root, raw_path, page, title=title or text)
    candidates_path = write_candidate_facts(root, title=title or text, source_page=page)
    _append_log(root, f"{today_iso()} ingest-url | {text} | {page.relative_to(root).as_posix()}")
    return IngestResult(str(root), text, "url", False, str(raw_path), str(page), str(candidates_path), ("manual_extraction_required:url",))


def ingest_text(
    wiki_dir: str | Path,
    text: str,
    *,
    title: str = "pasted-text",
    summary: str = "",
) -> IngestResult:
    """把粘贴文本保存为 raw note，并创建候选来源。

    该入口适合演示或人工临时补充材料。由于粘贴文本不一定来自权威网页，
    默认仍然进入 ``NEEDS_REVIEW``，不能直接作为正式事实。
    """
    root = Path(wiki_dir)
    content = str(text or "").strip()
    if not content:
        raise ValueError("text must not be empty")
    raw_dir = root / "raw" / "notes"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = _unique_path(raw_dir / f"{slugify(title, fallback='pasted-text')}.txt")
    raw_path.write_text(content + "\n", encoding="utf-8")
    page = create_source_page(root, raw_path, title=title, source_type="plain_text", summary=summary or "Pasted text source. Pending domain review.")
    cache_update(root, raw_path, page, title=title)
    candidates_path = write_candidate_facts(root, title=title, source_page=page)
    _append_log(root, f"{today_iso()} ingest-text | {raw_path.relative_to(root).as_posix()} | {page.relative_to(root).as_posix()}")
    return IngestResult(str(root), "<text>", "plain_text", False, str(raw_path), str(page), str(candidates_path), ())


def create_source_page(
    wiki_dir: str | Path,
    raw_file: str | Path,
    *,
    title: str = "",
    source_type: str = "",
    summary: str = "",
    external_url: str = "",
    authority_level: str = "unclassified",
    evidence_status: str = "NEEDS_REVIEW",
    excerpt: str = "",
    audit_reason: str = "",
    audit_evidence: str = "",
) -> Path:
    """为一个 raw 文件或 URL 记录创建可追溯来源页。

    source page 是 raw 原始材料和正式/候选事实之间的审计桥梁。它会记录
    ``source_id``、``source_path``、``source_type``、``authority_level``、
    ``evidence_status``、外部 URL 和摘要。后续每条事实都应该能追溯到这类
    来源页或来源 ID。
    """
    root = Path(wiki_dir)
    raw_path = Path(raw_file)
    sources_dir = root / "wiki" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    next_id = _next_source_id(sources_dir)
    title_value = title or raw_path.stem
    page_path = sources_dir / f"{next_id}-{slugify(title_value)}.md"
    rel_raw = _relpath(root, raw_path)
    page_path.write_text(
        render_source_page(
            {
                "source_id": next_id,
                "title": title_value,
                "source_path": rel_raw,
                "source_type": source_type or match_source_input(str(raw_path)).source_id,
                "authority_level": authority_level,
                "evidence_status": evidence_status,
                "summary": summary or "Imported source. Pending domain review.",
                "external_url": external_url,
                "excerpt": excerpt,
            }
        ),
        encoding="utf-8",
    )
    reason = _source_create_reason(
        audit_reason,
        external_url=external_url,
        excerpt=excerpt,
        source_type=source_type or match_source_input(str(raw_path)).source_id,
    )
    evidence = _source_create_evidence(audit_evidence, external_url=external_url, raw_path=rel_raw)
    _append_log(
        root,
        (
            f"{today_iso()} source-create | {rel_raw} | {page_path.relative_to(root).as_posix()}"
            f" | reason={reason}"
            f" | evidence={evidence}"
            f" | external_url={external_url}"
        ),
    )
    return page_path


def write_candidate_facts(
    wiki_dir: str | Path,
    *,
    title: str,
    source_page: str | Path,
    external_url: str = "",
    evidence_role: str = "",
    evidence_excerpt: str = "",
) -> Path:
    """为新导入来源追加一条最小候选事实。

    这条候选事实只表达“某个来源已导入，等待复核”，并不表达疾病诊断、
    药品用法或监管结论。这样既能让图谱展示新增来源，又不会把未复核内容
    当作正式知识使用。
    """
    root = Path(wiki_dir)
    exports_dir = root / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    path = exports_dir / "knowledge_facts.candidates.json"
    existing: list[dict[str, Any]] = []
    if path.is_file():
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
            if isinstance(payload, list):
                existing = [dict(item) for item in payload if isinstance(item, dict)]
        except json.JSONDecodeError:
            existing = []
    rel_source = _relpath(root, Path(source_page))
    candidate = {
        "fact_id": f"CAND-{len(existing) + 1:04d}",
        "subject": title,
        "predicate": "source_imported",
        "object": "pending_review",
        "evidence_source_id": _source_id_from_stem(Path(source_page).stem),
        "source_page": rel_source,
        "external_url": external_url,
        "evidence_role": evidence_role,
        "evidence_excerpt": evidence_excerpt,
        "evidence_status": "NEEDS_REVIEW",
    }
    existing.append(candidate)
    path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _append_log(
        root,
        (
            f"{today_iso()} candidate-create | {candidate['fact_id']}"
            f" | source={rel_source}"
            f" | reason=source_imported_pending_review"
            f" | evidence={external_url or rel_source}"
            f" | evidence_status=NEEDS_REVIEW"
        ),
    )
    return path


def _next_source_id(sources_dir: Path) -> str:
    """分配下一个顺序递增的 ``SRC-xxxx`` 来源 ID。"""
    max_id = 0
    for path in sources_dir.glob("SRC-*.md"):
        prefix = path.stem.split("-")
        if len(prefix) >= 2 and prefix[0] == "SRC" and prefix[1].isdigit():
            max_id = max(max_id, int(prefix[1]))
    return f"SRC-{max_id + 1:04d}"


def _unique_path(path: Path) -> Path:
    """为 raw 文件分配不冲突的路径，避免覆盖已有证据。"""
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 10000):
        candidate = path.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not allocate unique path for {path}")


def _relpath(root: Path, path: Path) -> str:
    """尽量返回相对于 Wiki 根目录的路径，便于页面和日志引用。"""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _append_log(root: Path, line: str) -> None:
    """向 Wiki 日志追加一条维护事件。"""
    log_path = root / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{line}\n")


def _source_create_reason(explicit: str, *, external_url: str, excerpt: str, source_type: str) -> str:
    """生成 source-create 审计原因，确保新增来源有可解释依据。"""

    if explicit.strip():
        return explicit.strip()
    if external_url and excerpt:
        return "authority_url_fetched_with_evidence_excerpt"
    if external_url:
        return "external_url_recorded_pending_fetch_or_review"
    if source_type == "plain_text":
        return "manual_text_source_pending_review"
    return "raw_source_registered_pending_review"


def _source_create_evidence(explicit: str, *, external_url: str, raw_path: str) -> str:
    """生成 source-create 审计依据，优先使用外部 URL，其次使用 raw 路径。"""

    if explicit.strip():
        return explicit.strip()
    return external_url or raw_path


def _source_id_from_stem(stem: str) -> str:
    """从来源页文件名中提取 ``SRC-xxxx``。"""
    parts = stem.split("-")
    if len(parts) >= 2 and parts[0] == "SRC" and parts[1].isdigit():
        return f"{parts[0]}-{parts[1]}"
    return stem
