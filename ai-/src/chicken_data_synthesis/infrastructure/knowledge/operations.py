from __future__ import annotations
"""LLM Wiki 的高层维护操作模块。

这个模块汇总 CLI 和测试会直接调用的服务函数。更底层的模块分别负责来源
摄取、缓存、图谱构建、schema 校验等具体任务；本模块负责把这些能力组合成
常用维护命令，例如 init、status、lint、query、ingest、coverage 等。

可以把这里理解成“命令层背后的编排层”：它不直接承担所有细节，但负责保证
每个维护动作按照项目定义的安全链路执行。
"""

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from .cache import cache_check, cache_update, ensure_cache
from .contracts import REQUIRED_DIRECTORIES, REQUIRED_EXPORTS, ROOT_MARKDOWN_FILES
from .digest import build_digest
from .governance import append_governance_event, validate_change_request
from .ingest import IngestResult, create_source_page, ingest_file, ingest_text, ingest_url
from .linting import CheckResult, json_loadable_exports, run_strict_checks, source_signal_coverage
from .registry import adapter_state, list_source_types, match_source_input
from .rendering import render_root_file, today_iso
from .wiki import LlmWikiKnowledgeBase, LlmWikiSearchHit, build_llm_wiki_context, load_llm_wiki

_WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


@dataclass(frozen=True)
class LlmWikiLintReport:
    """当前 Wiki 包的 lint 汇总结果。

    其中 ``errors`` 表示必须修复的问题，``warnings`` 表示需要关注但不一定
    阻断演示的问题，``counts`` 和 ``evidence_status_counts`` 用于汇报覆盖率。
    """
    wiki_dir: str
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    counts: dict[str, int]
    evidence_status_counts: dict[str, int]
    checks: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class LlmWikiStatusReport:
    """Wiki 健康状态和内容数量的快照。

    `status` 命令会返回这个对象，用来快速说明当前知识库是否完整、图谱是否
    已生成、raw 文件和正式事实数量是多少。
    """
    wiki_dir: str
    purpose_exists: bool
    schema_exists: bool
    graph_data_exists: bool
    graph_html_exists: bool
    raw_file_count: int
    section_counts: dict[str, int]
    fact_count: int
    disease_count: int
    drug_count: int
    rule_count: int
    evidence_status_counts: dict[str, int]
    log_tail: tuple[str, ...]


@dataclass(frozen=True)
class WikiInitReport:
    """初始化 Wiki 时创建或保留的文件和目录报告。"""
    wiki_dir: str
    created_directories: tuple[str, ...]
    created_files: tuple[str, ...]
    preserved_files: tuple[str, ...]
    cache_path: str


def init_wiki(
    wiki_dir: str | Path,
    *,
    domain: str = "chicken_disease",
    force_template_sync: bool = False,
) -> WikiInitReport:
    """创建标准 Wiki 目录结构和基础导出文件。

    这个函数用于初始化或补齐 Wiki 包。默认不会覆盖已有文件，除非传入
    ``force_template_sync``。这样可以保护人工维护过的 Wiki 内容。
    """
    root = Path(wiki_dir)
    root.mkdir(parents=True, exist_ok=True)
    created_dirs: list[str] = []
    created_files: list[str] = []
    preserved_files: list[str] = []

    for relpath in REQUIRED_DIRECTORIES:
        path = root / relpath
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(relpath)

    for relpath in ROOT_MARKDOWN_FILES:
        path = root / relpath
        if force_template_sync or not path.exists():
            path.write_text(render_root_file(relpath, domain=domain), encoding="utf-8")
            created_files.append(relpath)
        else:
            preserved_files.append(relpath)

    exports_dir = root / "exports"
    for relpath in REQUIRED_EXPORTS:
        path = exports_dir / relpath
        if path.exists():
            preserved_files.append(f"exports/{relpath}")
            continue
        if relpath.endswith(".json"):
            path.write_text("[]\n", encoding="utf-8")
        else:
            path.write_text("\n", encoding="utf-8")
        created_files.append(f"exports/{relpath}")

    cache_path = ensure_cache(root)
    _append_log(root / "log.md", f"{today_iso()} init | domain={domain} | force_template_sync={force_template_sync}")
    return WikiInitReport(
        wiki_dir=str(root),
        created_directories=tuple(created_dirs),
        created_files=tuple(created_files),
        preserved_files=tuple(preserved_files),
        cache_path=str(cache_path),
    )


def build_status_report(wiki_dir: str | Path) -> LlmWikiStatusReport:
    """返回当前 Wiki 包的数量统计和健康标记。"""
    root = Path(wiki_dir)
    kb = load_llm_wiki(root)
    section_counts: Counter[str] = Counter(page.section for page in kb.pages)
    evidence_counts = _evidence_status_counts(kb)
    return LlmWikiStatusReport(
        wiki_dir=str(root),
        purpose_exists=(root / "purpose.md").is_file(),
        schema_exists=(root / ".wiki-schema.md").is_file(),
        graph_data_exists=(root / "wiki" / "graph-data.json").is_file(),
        graph_html_exists=(root / "wiki" / "knowledge-graph.html").is_file(),
        raw_file_count=_count_files(root / "raw"),
        section_counts=dict(sorted(section_counts.items())),
        fact_count=len(kb.facts),
        disease_count=len(kb.disease_index),
        drug_count=len(kb.drug_index),
        rule_count=len(kb.rule_index),
        evidence_status_counts=evidence_counts,
        log_tail=tuple(_tail_nonempty_lines(root / "log.md", limit=5)),
    )


def lint_wiki(wiki_dir: str | Path, *, strict: bool = False, fix: bool = False) -> LlmWikiLintReport:
    """检查 Wiki 的结构、索引、链接、来源和证据状态。

    普通模式用于发现问题；严格模式会把未复核事实等风险提升为错误；``fix``
    会尝试修复可自动处理的问题，例如缺失目录或过期缓存。
    """
    root = Path(wiki_dir)
    kb = load_llm_wiki(root)
    errors: list[str] = []
    warnings: list[str] = []

    for required in ("index.md", ".wiki-schema.md", "purpose.md", "wiki", "exports"):
        if not (root / required).exists():
            errors.append(f"missing_required_path:{required}")

    existing_targets = _build_wikilink_targets(root)
    for page in kb.pages:
        for target in _WIKILINK_PATTERN.findall(page.text):
            if _normalize_wikilink_target(target) not in existing_targets:
                warnings.append(f"broken_wikilink:{page.relpath}->[[{target}]]")

    for row in (*kb.disease_index, *kb.rule_index, *kb.drug_index):
        relpath = row.get("page_relpath", "").strip()
        if relpath and not (root / relpath).is_file():
            errors.append(f"missing_index_target:{relpath}")

    source_ids = {_source_id_from_stem(path.stem) for path in (root / "wiki" / "sources").glob("*.md") if path.is_file()}
    for fact in kb.facts:
        status = str(fact.get("evidence_status") or "").strip()
        if not status:
            errors.append(f"fact_missing_evidence_status:{fact.get('fact_id', '<unknown>')}")
        if status == "NEEDS_REVIEW":
            warnings.append(f"fact_needs_review:{fact.get('fact_id', '<unknown>')}")
        source_id = str(fact.get("evidence_source_id") or "").strip()
        if source_id and source_ids and source_id not in source_ids:
            warnings.append(f"fact_source_not_found:{fact.get('fact_id', '<unknown>')}->{source_id}")

    checks: list[CheckResult] = []
    checks.extend(json_loadable_exports(root))
    if strict or fix:
        checks.extend(run_strict_checks(root, fix=fix))
    for check in checks:
        payload = f"{check.code}:{check.path or check.message}"
        if check.severity == "error":
            errors.append(payload)
        else:
            warnings.append(payload)

    counts = {
        "pages": len(kb.pages),
        "facts": len(kb.facts),
        "diseases": len(kb.disease_index),
        "drugs": len(kb.drug_index),
        "rules": len(kb.rule_index),
        "broken_wikilinks": sum(1 for item in warnings if item.startswith("broken_wikilink:")),
        "missing_index_targets": sum(1 for item in errors if item.startswith("missing_index_target:")),
        "needs_review_facts": sum(1 for item in warnings if item.startswith("fact_needs_review:")),
    }
    return LlmWikiLintReport(
        wiki_dir=str(root),
        ok=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        counts=counts,
        evidence_status_counts=_evidence_status_counts(kb),
        checks=tuple(check.to_dict() for check in checks),
    )


def list_sources() -> tuple[dict[str, object], ...]:
    """向 CLI 暴露当前注册的来源类型。"""
    return tuple(item.to_dict() for item in list_source_types())


def match_source(value: str) -> dict[str, object]:
    """根据输入值匹配应该使用的来源适配器。

    输入可能是本地文件路径、URL 或纯文本。匹配结果会告诉 CLI 该走哪个 raw
    子目录，以及适配器是否可用。
    """
    source_type = match_source_input(value)
    payload = source_type.to_dict()
    payload["adapter"] = adapter_state(source_type.source_id)
    return payload


def check_adapter(source_id: str) -> dict[str, str]:
    """返回某个来源适配器在当前环境中的可用状态。"""
    return adapter_state(source_id)


def check_cache(wiki_dir: str | Path, raw_file: str | Path) -> dict[str, Any]:
    """检查某个 raw 文件是否已经有缓存记录。"""
    return cache_check(wiki_dir, _resolve_wiki_path(wiki_dir, raw_file))


def update_cache(
    wiki_dir: str | Path,
    raw_file: str | Path,
    source_page: str | Path,
    *,
    reason: str = "",
    evidence: str = "",
) -> dict[str, Any]:
    """新增或刷新 raw 文件与 source page 的缓存映射。"""
    request = validate_change_request(
        operation="update",
        target=f"cache:{raw_file}->{source_page}",
        reason=reason,
        evidence=evidence,
        actor="wiki_cli",
    )
    append_governance_event(wiki_dir, request, phase="precheck", status="accepted")
    raw_path = _resolve_wiki_path(wiki_dir, raw_file)
    source_path = _resolve_wiki_path(wiki_dir, source_page)
    result = cache_update(wiki_dir, raw_path, source_path)
    _post_write_closure(wiki_dir, request, details=result)
    return result


def source_create(
    wiki_dir: str | Path,
    raw_file: str | Path,
    *,
    title: str = "",
    summary: str = "",
    reason: str = "",
    evidence: str = "",
) -> Path:
    """为已有 raw 文件创建 source page，并同步写入缓存。"""
    audit_reason = reason or "compat_source_create_from_existing_raw"
    audit_evidence = evidence or f"raw_file:{raw_file}"
    request = validate_change_request(
        operation="create",
        target=f"source:{raw_file}",
        reason=audit_reason,
        evidence=audit_evidence,
        actor="wiki_cli",
    )
    append_governance_event(wiki_dir, request, phase="precheck", status="accepted")
    page = create_source_page(wiki_dir, raw_file, title=title, summary=summary, audit_reason=audit_reason, audit_evidence=audit_evidence)
    cache_update(wiki_dir, raw_file, page, title=title or Path(raw_file).stem)
    _post_write_closure(wiki_dir, request, details={"source_page": str(page)})
    return page


def ingest_source(
    wiki_dir: str | Path,
    input_path: str | Path,
    *,
    title: str = "",
    summary: str = "",
    reason: str = "",
    evidence: str = "",
) -> IngestResult:
    """摄取一个本地来源文件。"""
    audit_reason = reason or "compat_ingest_source_file"
    audit_evidence = evidence or f"input_path:{input_path}"
    request = validate_change_request(
        operation="create",
        target=f"ingest:{input_path}",
        reason=audit_reason,
        evidence=audit_evidence,
        actor="wiki_cli",
    )
    append_governance_event(wiki_dir, request, phase="precheck", status="accepted")
    result = ingest_file(wiki_dir, input_path, title=title, summary=summary)
    _post_write_closure(wiki_dir, request, details={"source_page": result.source_page, "candidates_path": result.candidates_path})
    return result


def ingest_url_source(
    wiki_dir: str | Path,
    url: str,
    *,
    title: str = "",
    summary: str = "",
    reason: str = "",
    evidence: str = "",
) -> IngestResult:
    """记录一个 URL 来源候选，不直接抽取正式事实。"""
    audit_reason = reason or "compat_ingest_url_source"
    audit_evidence = evidence or url
    request = validate_change_request(
        operation="create",
        target=f"ingest-url:{url}",
        reason=audit_reason,
        evidence=audit_evidence,
        actor="wiki_cli",
    )
    append_governance_event(wiki_dir, request, phase="precheck", status="accepted")
    result = ingest_url(wiki_dir, url, title=title, summary=summary)
    _post_write_closure(wiki_dir, request, details={"source_page": result.source_page, "candidates_path": result.candidates_path})
    return result


def ingest_text_source(
    wiki_dir: str | Path,
    text: str,
    *,
    title: str = "pasted-text",
    summary: str = "",
    reason: str = "",
    evidence: str = "",
) -> IngestResult:
    """把粘贴文本摄取为候选来源。"""
    audit_reason = reason or "compat_ingest_text_source"
    audit_evidence = evidence or f"title:{title}"
    request = validate_change_request(
        operation="create",
        target=f"ingest-text:{title}",
        reason=audit_reason,
        evidence=audit_evidence,
        actor="wiki_cli",
    )
    append_governance_event(wiki_dir, request, phase="precheck", status="accepted")
    result = ingest_text(wiki_dir, text, title=title, summary=summary)
    _post_write_closure(wiki_dir, request, details={"source_page": result.source_page, "candidates_path": result.candidates_path})
    return result


def digest_wiki(
    wiki_dir: str | Path,
    query: str,
    *,
    output_format: str = "quick",
    save: bool = False,
) -> Any:
    """根据当前 Wiki 检索结果生成派生摘要。

    派生摘要用于汇总或对比，不等同于正式事实，不能替代复核流程。
    """
    return build_digest(wiki_dir, query, output_format=output_format, save=save)


def coverage_report(wiki_dir: str | Path) -> dict[str, object]:
    """返回页面和事实的来源信号覆盖率。"""
    return source_signal_coverage(wiki_dir)


def validate_step1_analysis(payload: Mapping[str, Any]) -> tuple[bool, tuple[str, ...], tuple[str, ...]]:
    """在 Step1 分析结果进入 Wiki 使用前校验其结构。

    这里检查 entities、topics、connections 是否存在，以及实体和连接是否带有
    名称、置信度和证据。目的是防止没有证据的抽取结果直接进入后续链路。
    """
    errors: list[str] = []
    warnings: list[str] = []
    for field in ("entities", "topics", "connections"):
        if not isinstance(payload.get(field), list):
            errors.append(f"missing_or_invalid_list:{field}")

    for index, entity in enumerate(payload.get("entities", []) or []):
        if not isinstance(entity, Mapping):
            errors.append(f"invalid_entity:{index}")
            continue
        if not entity.get("name"):
            errors.append(f"entity_missing_name:{index}")
        if not entity.get("confidence"):
            errors.append(f"entity_missing_confidence:{entity.get('name', index)}")
        if entity.get("confidence") in {"EXTRACTED", "INFERRED"} and not entity.get("evidence"):
            warnings.append(f"entity_missing_evidence:{entity.get('name', index)}")

    for index, connection in enumerate(payload.get("connections", []) or []):
        if not isinstance(connection, Mapping):
            errors.append(f"invalid_connection:{index}")
            continue
        if not connection.get("from") or not connection.get("to"):
            errors.append(f"connection_missing_endpoint:{index}")
        if not connection.get("confidence"):
            errors.append(f"connection_missing_confidence:{index}")
        if connection.get("confidence") in {"EXTRACTED", "INFERRED"} and not connection.get("evidence"):
            warnings.append(f"connection_missing_evidence:{index}")

    return not errors, tuple(errors), tuple(warnings)


def build_runtime_context(wiki_dir: str | Path, *, max_chars: int = 2400) -> str:
    """构建简短的运行时 Wiki 状态上下文。

    该上下文可在会话开始时提醒系统当前 Wiki 路径、页面数量、事实数量、
    图谱状态和最近日志，帮助生成/评估流程了解知识库状态。
    """
    status = build_status_report(wiki_dir)
    lines = [
        "鸡病 LLM Wiki 运行时上下文",
        f"- 路径: {status.wiki_dir}",
        f"- Wiki 页面: {sum(status.section_counts.values())}",
        f"- 疾病/药物/规则: {status.disease_count}/{status.drug_count}/{status.rule_count}",
        f"- 结构化事实: {status.fact_count}",
        f"- 证据状态: {json.dumps(status.evidence_status_counts, ensure_ascii=False)}",
        f"- 图谱: graph-data={'yes' if status.graph_data_exists else 'no'}, html={'yes' if status.graph_html_exists else 'no'}",
        "- 使用约束: 生成、评估、规则拦截必须优先使用 Wiki 编译知识；NEEDS_REVIEW 事实只作为复核提示，不能作为确定监管结论。",
    ]
    if status.log_tail:
        lines.append("- 最近日志:")
        lines.extend(f"  - {line}" for line in status.log_tail)
    context = "\n".join(lines)
    return context[:max_chars]


def save_query_result(
    query: str,
    answer: str,
    *,
    wiki_dir: str | Path,
    source_hits: Sequence[LlmWikiSearchHit] | None = None,
) -> Path:
    """把一次基于 Wiki 的查询回答保存为可审计的派生页面。

    LLM Wiki 不只在运行时提供检索上下文，也要记录知识是如何被使用的。
    保存的 query 页面会记录用户问题、LLM 或应用层生成的回答，以及支撑回答
    的来源页。页面存放在 ``wiki/queries``，并标记为 ``derived: true``，
    让后续 lint 和图谱导出可以区分“派生回答”和“正式事实”。
    """
    root = Path(wiki_dir)
    queries_dir = root / "wiki" / "queries"
    queries_dir.mkdir(parents=True, exist_ok=True)
    # 查询哈希让文件名稳定且不会过长；完整问题仍然会写在页面正文里。
    today = datetime.now().strftime("%Y-%m-%d")
    digest = hashlib.sha256(str(query).encode("utf-8")).hexdigest()[:10]
    path = queries_dir / f"{today}-{digest}.md"
    source_lines = [
        f"- [[{Path(hit.relpath).stem}]] ({hit.relpath}) score={hit.score:.1f}"
        for hit in (source_hits or ())
    ]
    path.write_text(
        "\n".join(
            [
                "---",
                "type: query",
                "derived: true",
                f"date: {today}",
                f"query_hash: {digest}",
                "---",
                "",
                f"# 查询：{query}",
                "",
                "## 回答",
                "",
                answer.strip(),
                "",
                "## 来源页面",
                "",
                *(source_lines or ["- 暂无显式来源页面"]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    _append_log(root / "log.md", f"{today} query | {query} | {path.relative_to(root).as_posix()}")
    return path


def query_wiki(query: str, *, wiki_dir: str | Path, top_k: int = 5, max_chars: int = 4200) -> dict[str, Any]:
    """返回 CLI 演示和报告使用的完整检索载荷。

    返回内容同时包含 Markdown 页面命中和结构化事实命中。页面命中解释 LLM
    可以阅读的文本证据   ；事实命中提供 subject/predicate/object、source 和
    evidence status，用于图谱重建、覆盖率检查、生成约束和评估规则。
    """
    kb = load_llm_wiki(wiki_dir)
    hits = kb.search(query, top_k=top_k)
    fact_hits = kb.search_facts(query, top_k=top_k)
    return {
        "query": query,
        "context": build_llm_wiki_context(query, wiki_dir=wiki_dir, top_k_pages=top_k, max_chars=max_chars),
        "wiki_dir": str(Path(wiki_dir)),
        "hits": [
            {
                "title": hit.title,
                "relpath": hit.relpath,
                "section": hit.section,
                "score": hit.score,
                "excerpt": hit.excerpt,
            }
            for hit in hits
        ],
        "fact_hits": list(fact_hits),
    }


def _evidence_status_counts(kb: LlmWikiKnowledgeBase) -> dict[str, int]:
    """统计结构化事实中的证据状态数量。"""
    counter: Counter[str] = Counter(str(fact.get("evidence_status") or "UNKNOWN") for fact in kb.facts)
    return dict(sorted(counter.items()))


def _count_files(path: Path) -> int:
    """统计目录树中的文件数量；目录不存在时返回 0。"""
    if not path.is_dir():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def _tail_nonempty_lines(path: Path, *, limit: int) -> list[str]:
    """读取最近的非空日志行，用于 status 和运行时上下文。"""
    if not path.is_file():
        return []
    lines = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return lines[-limit:]


def _build_wikilink_targets(root: Path) -> set[str]:
    """从文件名和标题中构建合法 Wiki 链接目标集合。

    Wiki 页面可能按文件名链接，也可能按页面标题链接。lint 同时接受这两种
    写法，既方便人工编辑，又能发现真正断掉的链接。
    """
    targets: set[str] = set()
    for path in (root / "wiki").rglob("*.md"):
        targets.add(_normalize_wikilink_target(path.stem))
    for path in (root / "wiki").rglob("*.md"):
        try:
            first_heading = next(
                (
                    line.lstrip("#").strip()
                    for line in path.read_text(encoding="utf-8-sig").splitlines()
                    if line.strip().startswith("#")
                ),
                "",
            )
        except UnicodeDecodeError:
            first_heading = ""
        if first_heading:
            targets.add(_normalize_wikilink_target(first_heading))
    return targets


def _normalize_wikilink_target(value: str) -> str:
    """比较 Wiki 链接目标前先统一大小写和空白。"""
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def _append_log(path: Path, line: str) -> None:
    """追加一条操作审计日志，并在需要时创建父目录。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{line}\n")


def _resolve_wiki_path(wiki_dir: str | Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = Path(wiki_dir) / path
    return path


def _post_write_closure(wiki_dir: str | Path, request: Any, *, details: Mapping[str, Any] | None = None) -> None:
    """Run the mandatory post-write closure: schema, lint, graph, status, audit."""

    from .graph import rebuild_graph
    from .schema import schema_check

    closure_details: dict[str, Any] = {"write_result": dict(details or {})}
    schema_report = schema_check(wiki_dir)
    lint_report = lint_wiki(wiki_dir, strict=True)
    graph_report = rebuild_graph(wiki_dir)
    status_report = build_status_report(wiki_dir)
    closure_details.update(
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
    append_governance_event(wiki_dir, request, phase="post_write_closure", status=status, details=closure_details)


def _source_id_from_stem(stem: str) -> str:
    """从来源页文件名中提取稳定的 ``SRC-0001`` 风格 ID。"""
    match = re.match(r"^(SRC-\d+)", stem)
    return match.group(1) if match else stem
