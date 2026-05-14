from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .cache import cache_invalidate
from .governance import append_governance_event, validate_change_request
from .ingest import IngestResult, ingest_file
from .registry import list_source_types, source_type_by_id
from .rendering import slugify, today_iso


# 生命周期操作位于“单文件摄取”之上。它们用于演示和维护场景，例如批量摄取、
# 安全删除来源、检查 Wiki 兼容性、把一次会话沉淀为派生笔记。这里的操作
# 仍然遵守安全边界：不会直接把未复核内容写入正式事实库。

@dataclass(frozen=True)
class BatchIngestReport:
    """批量导入一个目录后返回的结果。"""

    wiki_dir: str
    input_dir: str
    recursive: bool
    processed_count: int
    skipped_count: int
    results: tuple[dict[str, Any], ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class DeleteSourceReport:
    """删除 raw/source 配对时的预演或执行报告。"""

    wiki_dir: str
    raw_file: str
    source_page: str
    reason: str
    evidence: str
    replacement_source: str
    dry_run: bool
    deleted_paths: tuple[str, ...]
    references: tuple[str, ...]
    cache_removed_count: int
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class WikiCompatReport:
    """Wiki 新旧目录结构兼容性检查报告。"""

    wiki_dir: str
    ok: bool
    schema_version: str
    language: str
    legacy_mode: bool
    migration_required: bool
    missing_required_paths: tuple[str, ...]
    missing_optional_raw_dirs: tuple[str, ...]
    ensured_path: str = ""


@dataclass(frozen=True)
class CrystallizeResult:
    """保存派生会话总结后的路径和数量统计。"""

    wiki_dir: str
    topic: str
    saved_path: str
    source_count: int
    fact_count: int


def batch_ingest_sources(
    wiki_dir: str | Path,
    input_dir: str | Path,
    *,
    recursive: bool = False,
    reason: str = "",
    evidence: str = "",
) -> BatchIngestReport:
    """把目录中所有支持的文件摄取到 Wiki 暂存流程。

    每个文件都会复用 ``ingest_file``，因此 raw 文件、source page、候选事实、
    缓存和日志的行为保持一致。单个文件失败不会中断整批任务，而是记录为
    warning，这适合真实维护时处理质量参差不齐的来源目录。
    """
    root = Path(wiki_dir)
    source_dir = Path(input_dir)
    audit_reason = reason or "compat_batch_ingest_sources"
    audit_evidence = evidence or f"input_dir:{source_dir}"
    governance_request = validate_change_request(
        operation="create",
        target=f"batch-ingest:{source_dir}",
        reason=audit_reason,
        evidence=audit_evidence,
        actor="wiki_cli",
    )
    append_governance_event(root, governance_request, phase="precheck", status="accepted")
    if not source_dir.is_dir():
        raise NotADirectoryError(str(source_dir))
    results: list[dict[str, Any]] = []
    warnings: list[str] = []
    skipped = 0
    for path in _iter_supported_files(source_dir, recursive=recursive):
        try:
            result = ingest_file(root, path)
            results.append(_ingest_result_to_dict(result))
        except Exception as exc:  # 单个文件失败时继续处理后续文件，并把失败原因放入报告。
            skipped += 1
            warnings.append(f"ingest_failed:{path}:{exc}")
    report = BatchIngestReport(
        wiki_dir=str(root),
        input_dir=str(source_dir),
        recursive=recursive,
        processed_count=len(results),
        skipped_count=skipped,
        results=tuple(results),
        warnings=tuple(warnings),
    )
    _post_delete_closure(root, governance_request, details={"processed_count": report.processed_count, "skipped_count": report.skipped_count})
    return report


def delete_source(
    wiki_dir: str | Path,
    *,
    raw_file: str | Path = "",
    source_page: str | Path = "",
    reason: str = "",
    evidence: str = "",
    replacement_source: str | Path = "",
    allow_referenced_delete: bool = False,
    dry_run: bool = True,
) -> DeleteSourceReport:
    """在解析引用后删除 source page 和 raw 文件配对。

    默认 ``dry_run=True``，因为删除来源会影响事实、派生页面和图谱节点的
    可追溯性。函数会先确认路径在 Wiki 根目录内，再扫描引用，只有明确关闭
    dry-run 时才真正删除文件和缓存。

    真正删除时必须提供 ``reason``。原因要写明可审计依据，例如：
    ``source_replaced_by_more_specific_page``、``fetched_content_irrelevant``、
    ``duplicate_source``、``source_url_obsolete``。如果有替代来源或外部依据，
    应通过 ``replacement_source`` 或 ``evidence`` 一并记录。这样删除日志不
    只是“删了什么”，还会说明“为什么删、依据是什么、用什么替代”。
    """
    root = Path(wiki_dir)
    raw_path = _resolve_inside(root, raw_file) if raw_file else None
    page_path = _resolve_inside(root, source_page) if source_page else None
    replacement_path = _resolve_inside(root, replacement_source) if replacement_source else None
    reason_text = str(reason or "").strip()
    evidence_text = str(evidence or "").strip()
    warnings: list[str] = []
    deleted: list[str] = []
    if raw_path is None and page_path is None:
        raise ValueError("raw_file or source_page is required.")
    governance_request = None
    if not dry_run:
        governance_request = validate_change_request(
            operation="delete",
            target=f"source:{source_page or raw_file}",
            reason=reason_text,
            evidence=evidence_text,
            actor="wiki_cli",
        )
        append_governance_event(root, governance_request, phase="precheck", status="accepted")
    if page_path is None and raw_path is not None:
        page_path = _source_page_from_cache_or_scan(root, raw_path)
    if page_path is not None and not page_path.is_file():
        warnings.append(f"source_page_missing:{page_path}")
    if raw_path is not None and not raw_path.is_file():
        warnings.append(f"raw_file_missing:{raw_path}")
    if replacement_path is not None and not replacement_path.exists():
        warnings.append(f"replacement_source_missing:{replacement_path}")
    references = _scan_references(root, page_path, raw_path)
    if not dry_run and references and not allow_referenced_delete:
        raise ValueError(
            "Refusing to delete a source that is still referenced. "
            f"references={references}. Update or remove references first, or pass allow_referenced_delete=True only for a documented migration."
        )
    cache_result = {"removed_count": 0}
    if not dry_run:
        if page_path is not None and page_path.is_file():
            page_path.unlink()
            deleted.append(_relpath(root, page_path))
        if raw_path is not None and raw_path.is_file():
            raw_path.unlink()
            deleted.append(_relpath(root, raw_path))
        cache_result = cache_invalidate(root, raw_path or "", source_page=page_path or "")
        _append_log(
            root,
            (
                f"{today_iso()} delete | raw={_relpath(root, raw_path) if raw_path else ''}"
                f" | source={_relpath(root, page_path) if page_path else ''}"
                f" | reason={reason_text}"
                f" | evidence={evidence_text}"
                f" | replacement={_relpath(root, replacement_path) if replacement_path else ''}"
            ),
        )
        _post_delete_closure(
            root,
            governance_request,
            details={
                "deleted_paths": tuple(deleted),
                "cache": cache_result,
                "references": references,
                "replacement_source": _relpath(root, replacement_path) if replacement_path else "",
            },
        )
    return DeleteSourceReport(
        wiki_dir=str(root),
        raw_file=str(raw_path or ""),
        source_page=str(page_path or ""),
        reason=reason_text,
        evidence=evidence_text,
        replacement_source=str(replacement_path or ""),
        dry_run=dry_run,
        deleted_paths=tuple(deleted),
        references=references,
        cache_removed_count=int(cache_result.get("removed_count") or 0),
        warnings=tuple(warnings),
    )


def inspect_compat(wiki_dir: str | Path, *, ensure_source_id: str = "") -> WikiCompatReport:
    """检查一个目录是否具备 LLM Wiki 所需结构。

    ``ensure_source_id`` 用于演示或初始化脚本：它只创建某个来源类型需要的
    raw 目录，不会迁移或重写已有 Wiki 内容。
    """
    root = Path(wiki_dir)
    missing_required = tuple(rel for rel in _compat_required_paths() if not (root / rel).exists())
    optional_missing = tuple(
        dict.fromkeys(
            source.raw_dir
            for source in list_source_types()
            if source.raw_dir and not (root / source.raw_dir).is_dir()
        )
    )
    ensured_path = ""
    if ensure_source_id:
        source_type = source_type_by_id(ensure_source_id)
        if source_type is None:
            raise ValueError(f"Unknown source type: {ensure_source_id}")
        ensured = root / source_type.raw_dir
        ensured.mkdir(parents=True, exist_ok=True)
        ensured_path = str(ensured)
        optional_missing = tuple(item for item in optional_missing if item != source_type.raw_dir)
    legacy_mode = bool(optional_missing or not (root / "purpose.md").is_file() or not (root / ".wiki-cache.json").is_file())
    return WikiCompatReport(
        wiki_dir=str(root),
        ok=not missing_required,
        schema_version="1.0" if legacy_mode else "1.0.0",
        language="zh",
        legacy_mode=legacy_mode,
        migration_required=False,
        missing_required_paths=missing_required,
        missing_optional_raw_dirs=optional_missing,
        ensured_path=ensured_path,
    )


def crystallize_session(
    wiki_dir: str | Path,
    topic: str,
    *,
    notes: str = "",
) -> CrystallizeResult:
    """保存一份基于当前 Wiki 检索结果的会话级派生总结。

    该页面会被标记为 ``derived: true`` 和 ``INFERRED``。这表示它只是基于
    Wiki 检索结果形成的二次总结，可以用于汇报和回顾，但不能等同于正式、
    已复核的权威事实。
    """
    from .wiki import load_llm_wiki

    root = Path(wiki_dir)
    kb = load_llm_wiki(root)
    hits = kb.search(topic, top_k=8)
    facts = kb.search_facts(topic, top_k=12)
    target = root / "wiki" / "synthesis" / "sessions" / f"{today_iso()}-{slugify(topic, fallback='session')}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    source_lines = "\n".join(f"- [[{Path(hit.relpath).stem}]] ({hit.relpath}) score={hit.score:.1f}" for hit in hits) or "- No matching pages."
    fact_lines = "\n".join(
        f"- {fact.get('subject', '')} | {fact.get('predicate', '')} | {fact.get('object', '')} "
        f"(source={fact.get('evidence_source_id') or fact.get('evidence_source') or 'unknown'}, status={fact.get('evidence_status') or 'UNKNOWN'})"
        for fact in facts
    ) or "- No matching structured facts."
    target.write_text(
        "\n".join(
            [
                "---",
                "type: session",
                "derived: true",
                "evidence_status: INFERRED",
                f"created: {today_iso()}",
                "sources: []",
                "---",
                "",
                f"# {topic} crystallized session",
                "",
                "## Core Insights",
                "",
                notes.strip() or "This session crystallizes matching Wiki pages and structured facts. Treat as secondary synthesis.",
                "",
                "## Source Pages",
                "",
                source_lines,
                "",
                "## Structured Evidence",
                "",
                fact_lines,
                "",
                "## Follow Up",
                "",
                "- Verify source pages before using conclusions in generation, evaluation, or regulatory blocking.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _append_log(root, f"{today_iso()} crystallize | {topic} | {target.relative_to(root).as_posix()}")
    return CrystallizeResult(str(root), topic, str(target), len(hits), len(facts))


def _iter_supported_files(root: Path, *, recursive: bool) -> Iterable[Path]:
    """遍历后缀被已注册来源适配器接受的文件。"""
    patterns = {suffix for source in list_source_types() for suffix in source.extensions}
    iterator = root.rglob("*") if recursive else root.glob("*")
    for path in sorted(iterator):
        if path.is_file() and (not patterns or path.suffix.lower() in patterns):
            yield path


def _ingest_result_to_dict(result: IngestResult) -> dict[str, Any]:
    """把不可变的摄取结果转换成适合 JSON 和 CLI 输出的字典。"""
    return {
        "input": result.input,
        "source_type": result.source_type,
        "cache_hit": result.cache_hit,
        "raw_path": result.raw_path,
        "source_page": result.source_page,
        "candidates_path": result.candidates_path,
        "warnings": list(result.warnings),
    }


def _resolve_inside(root: Path, value: str | Path) -> Path:
    """解析用户传入路径，并要求最终路径必须位于 Wiki 根目录内。"""
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    if not str(resolved).startswith(str(root.resolve())):
        raise ValueError(f"Path must stay inside wiki root: {value}")
    return resolved


def _source_page_from_cache_or_scan(root: Path, raw_path: Path) -> Path | None:
    """查找 raw 文件对应的 source page；优先查缓存，缓存缺失时扫描文件。"""
    from .cache import cache_check, read_cache

    check = cache_check(root, raw_path) if raw_path.is_file() else {"entry": None}
    entry = check.get("entry")
    if isinstance(entry, dict) and entry.get("source_page"):
        return root / str(entry["source_page"])
    raw_name = raw_path.name
    for path in (root / "wiki" / "sources").glob("*.md"):
        try:
            if raw_name in path.read_text(encoding="utf-8-sig"):
                return path
        except UnicodeDecodeError:
            continue
    cache = read_cache(root)
    for item in dict(cache.get("entries") or {}).values():
        if isinstance(item, dict) and item.get("source_path") == _relpath(root, raw_path) and item.get("source_page"):
            return root / str(item["source_page"])
    return None


def _scan_references(root: Path, page_path: Path | None, raw_path: Path | None) -> tuple[str, ...]:
    return _scan_references_strict(root, page_path, raw_path)


def _scan_references_strict(root: Path, page_path: Path | None, raw_path: Path | None) -> tuple[str, ...]:
    """Find wiki/export files that still reference a source page, raw path, or source id."""
    needles = {
        item
        for item in (
            _relpath(root, page_path) if page_path else "",
            _relpath(root, raw_path) if raw_path else "",
            _source_id_from_stem(page_path.stem) if page_path else "",
            page_path.name if page_path else "",
            raw_path.name if raw_path else "",
        )
        if item
    }
    refs: set[str] = set()
    for base in (root / "wiki", root / "exports"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path == page_path or path == raw_path:
                continue
            rel = _relpath(root, path)
            if rel in {"wiki/graph-data.json", "wiki/knowledge-graph.md", "wiki/knowledge-graph.html"}:
                continue
            if rel.endswith("knowledge_facts.candidates.json"):
                continue
            if path.suffix.lower() not in {".md", ".json", ".jsonl", ".csv", ".txt"}:
                continue
            try:
                text = path.read_text(encoding="utf-8-sig", errors="replace")
            except OSError:
                continue
            if any(needle in text for needle in needles):
                refs.add(rel)
    return tuple(sorted(refs))


def _scan_references_legacy(root: Path, page_path: Path | None, raw_path: Path | None) -> tuple[str, ...]:
    """查找仍然引用某个 source page 或 raw 文件路径的 Wiki 页面。"""
    needles = {item for item in (_relpath(root, page_path) if page_path else "", _relpath(root, raw_path) if raw_path else "") if item}
    refs: set[str] = set()
    for path in (root / "wiki").rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        if any(needle in text for needle in needles):
            refs.add(_relpath(root, path))
    return tuple(sorted(refs))


def _compat_required_paths() -> tuple[str, ...]:
    """返回一个目录要作为 LLM Wiki 运行所需的最小路径集合。"""
    return (".wiki-schema.md", "index.md", "log.md", "raw", "wiki", "wiki/sources", "wiki/synthesis")


def _relpath(root: Path, path: Path | None) -> str:
    """尽量把路径显示为相对于 Wiki 根目录的形式。"""
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _append_log(root: Path, line: str) -> None:
    """向 ``log.md`` 追加一条生命周期操作审计日志。"""
    with (root / "log.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n{line}\n")


def _source_id_from_stem(stem: str) -> str:
    parts = str(stem or "").split("-")
    if len(parts) >= 2 and parts[0] == "SRC" and parts[1].isdigit():
        return f"{parts[0]}-{parts[1]}"
    return str(stem or "")


def _post_delete_closure(root: Path, request: Any, *, details: dict[str, Any]) -> None:
    """Run schema/lint/graph/status closure after an applied delete."""

    from .graph import rebuild_graph
    from .operations import build_status_report, lint_wiki
    from .schema import schema_check

    schema_report = schema_check(root)
    lint_report = lint_wiki(root, strict=True)
    graph_report = rebuild_graph(root)
    status_report = build_status_report(root)
    payload = dict(details)
    payload.update(
        {
            "schema_ok": schema_report.ok,
            "lint_ok": lint_report.ok,
            "graph_data_path": graph_report.graph_data_path,
            "graph_node_count": graph_report.node_count,
            "graph_link_count": graph_report.link_count,
            "fact_count": status_report.fact_count,
            "evidence_status_counts": status_report.evidence_status_counts,
        }
    )
    status = "closed" if schema_report.ok and lint_report.ok else "closed_with_findings"
    append_governance_event(root, request, phase="post_write_closure", status=status, details=payload)


__all__ = [
    "BatchIngestReport",
    "CrystallizeResult",
    "DeleteSourceReport",
    "WikiCompatReport",
    "batch_ingest_sources",
    "crystallize_session",
    "delete_source",
    "inspect_compat",
]
