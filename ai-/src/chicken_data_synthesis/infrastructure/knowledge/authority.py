from __future__ import annotations
"""鸡病 LLM Wiki 的权威来源发现模块。

这个模块位于“LLM 使用 web access 搜索网页”和“项目知识库真正落库”之间，
作用是做安全闸门。LLM 可以提出它搜索到的候选 URL，但这些 URL 在进入
知识库之前不能被默认相信，必须先经过本模块的域名白名单校验。

核心边界：
    本模块绝不能直接写入 ``exports/knowledge_facts.json``。也就是说，
    LLM 搜索到的内容不能绕过复核直接成为正式事实。通过校验的来源只会
    进入 ``raw/``、``wiki/sources/`` 和
    ``exports/knowledge_facts.candidates.json`` 候选层。只有后续复核
    确认来源、证据、事实三者都可靠后，才能把事实提升到正式事实库。
"""

import json
import re
from dataclasses import dataclass
from email.message import Message
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.error import URLError
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

from .cache import cache_update
from .contracts import AUTHORITY_ALLOWED_DOMAINS
from .governance import append_governance_event, validate_change_request
from .ingest import create_source_page, write_candidate_facts
from .rendering import slugify, today_iso


@dataclass(frozen=True)
class AuthorityCandidate:
    """表示一个待校验的权威来源候选。

    ``url`` 是唯一必填字段。其他字段是解释性信息，通常来自 LLM 的
    web access 搜索结果，例如标题、推荐原因、证据角色等。这些字段不会
    被当作正式事实，只是写入 source page，帮助人工复核时理解：
    “为什么 LLM 推荐这个来源，它准备支撑哪类证据”。
    """

    url: str
    title: str = ""
    reason: str = ""
    evidence_role: str = ""
    authority_level: str = ""


@dataclass(frozen=True)
class AuthoritySourceReport:
    """``authority-discover`` 命令返回的机器可读报告。

    报告会明确列出接受和拒绝的候选来源。这样演示和自动化流程都能证明：
    非白名单域名确实被拒绝了；通过校验的来源也只是进入候选层和来源层，
    而不是直接进入正式事实库。
    """

    wiki_dir: str
    query: str
    accepted_count: int
    rejected_count: int
    created_sources: tuple[str, ...]
    fetched_raw_paths: tuple[str, ...]
    candidates_path: str
    warnings: tuple[str, ...]
    rejected_candidates: tuple[dict[str, str], ...]


def allowed_authority_domains() -> tuple[str, ...]:
    """返回运行时使用的权威域名白名单。

    这个函数用于对外暴露代码层面的白名单，方便 CLI、测试、文档和
    schema-check 对齐。它对应 ``contracts.py`` 里的
    ``AUTHORITY_ALLOWED_DOMAINS``。
    """
    return AUTHORITY_ALLOWED_DOMAINS


def is_authoritative_url(url: str) -> bool:
    """判断一个 URL 是否属于允许访问的权威域名。

    这里不仅支持精确域名，也支持子域名后缀匹配。例如：
    ``xmsyj.moa.gov.cn`` 会被接受，因为 ``moa.gov.cn`` 在白名单中。
    这样可以覆盖农业农村部等官方站点的子站，同时仍然阻止无关商业网站、
    论坛、博客或转载页面进入自动维护链路。
    """

    host = _hostname(url)
    return bool(host) and any(host == domain or host.endswith(f".{domain}") for domain in AUTHORITY_ALLOWED_DOMAINS)


def authority_level_for_url(url: str) -> str:
    """根据 URL 域名推断来源权威等级。

    该等级会写入 source page 的 ``authority_level`` 字段，用于复核和展示。
    例如中国政府、国家标准、行业标准站点归为 ``official``；WOAH、FAO、
    EMA 等国际组织归为 ``guideline``；Merck Veterinary Manual 归为
    ``textbook``。这个判断只代表来源类别，不代表其中每个事实已经被复核。
    """
    host = _hostname(url)
    if host.endswith(("moa.gov.cn", "samr.gov.cn", "openstd.samr.gov.cn", "std.cahec.cn")):
        return "official"
    if host.endswith(("woah.org", "fao.org", "ema.europa.eu")):
        return "guideline"
    if host.endswith("merckvetmanual.com"):
        return "textbook"
    return "unknown"


def discover_authority_sources(
    wiki_dir: str | Path,
    query: str,
    *,
    candidate_urls: Sequence[str] = (),
    llm_suggestions_json: str = "",
    fetch: bool = False,
    timeout_seconds: int = 20,
) -> AuthoritySourceReport:
    """保存通过校验的权威来源候选。

    LLM 的输出在这里被视为“不可信的发现线索”，而不是事实本身。

    执行流程：
        1. 合并命令行显式传入的 ``--url`` 和 LLM JSON 中的候选来源。
        2. 拒绝格式错误、协议不合法或不在白名单中的 URL。
        3. 对通过校验的来源，在 ``raw/`` 下记录 URL 或抓取原文。
        4. 为每个通过校验的来源创建 ``wiki/sources/SRC-xxxx`` 来源页。
        5. 向 ``exports/knowledge_facts.candidates.json`` 追加候选事实。

    安全不变量：
        这个函数不会修改 ``exports/knowledge_facts.json``，也不会直接修改
        疾病、药品、规则等正式知识页面。候选事实提升为正式事实必须通过
        后续复核流程完成。
    """

    root = Path(wiki_dir)
    governance_request = validate_change_request(
        operation="create",
        target=f"authority-discover:{query}",
        reason="candidate authority source discovery for wiki gap; candidate_only pending review",
        evidence=query,
        actor="wiki_cli_or_maintenance",
    )
    append_governance_event(root, governance_request, phase="precheck", status="accepted")
    warnings: list[str] = []
    rejected: list[dict[str, str]] = []
    created_sources: list[str] = []
    fetched_raw_paths: list[str] = []
    candidates_path = ""

    existing_urls = _existing_external_urls(root)
    candidates = _dedupe_candidates(
        (
            *[AuthorityCandidate(url=url) for url in candidate_urls],
            *_parse_llm_suggestions(llm_suggestions_json, warnings),
        )
    )
    candidates = _prioritize_specific_candidates(candidates)
    if not candidates:
        warnings.append("no_candidates_provided")

    for candidate in candidates:
        if not candidate.url.startswith(("http://", "https://")):
            rejected.append({"url": candidate.url, "reason": "invalid_url_scheme"})
            continue
        if not is_authoritative_url(candidate.url):
            rejected.append({"url": candidate.url, "reason": "domain_not_allowlisted"})
            continue
        canonical_url = _canonical_url(candidate.url)
        if canonical_url in existing_urls:
            rejected.append({"url": candidate.url, "reason": "duplicate_existing_source"})
            continue

        try:
            raw_path, source_type, excerpt = _materialize_candidate(
                root,
                candidate,
                query=query,
                fetch=fetch,
                timeout_seconds=timeout_seconds,
            )
        except URLError as exc:
            rejected.append({"url": candidate.url, "reason": f"fetch_failed:{exc.reason}"})
            continue
        except OSError as exc:
            rejected.append({"url": candidate.url, "reason": f"fetch_failed:{exc}"})
            continue
        if fetch and source_type == "html" and not _has_relevant_evidence(excerpt, query=query, title=candidate.title):
            rejected.append({"url": candidate.url, "reason": "fetched_content_not_relevant_to_query"})
            _remove_unusable_raw(raw_path)
            continue

        title = candidate.title or _title_from_url(candidate.url)
        authority_level = candidate.authority_level or authority_level_for_url(candidate.url)
        summary_parts = [
            "LLM-assisted authority source candidate.",
            f"Query: {query}",
            f"Authority gate: domain allowlist matched `{_hostname(candidate.url)}`.",
        ]
        if candidate.reason:
            summary_parts.append(f"LLM reason: {candidate.reason}")
        if candidate.evidence_role:
            summary_parts.append(f"Evidence role: {candidate.evidence_role}")
        if not fetch:
            summary_parts.append("Fetch disabled: URL was recorded, but fact extraction still requires fetched/source text review.")
        if fetch and excerpt:
            summary_parts.append(f"Fetched evidence excerpt: {excerpt[:320]}")

        source_page = create_source_page(
            root,
            raw_path,
            title=title,
            source_type=source_type,
            summary=" ".join(summary_parts),
            external_url=candidate.url,
            authority_level=authority_level,
            evidence_status="NEEDS_REVIEW",
            excerpt=excerpt,
            audit_reason="authority_discover_accept_after_allowlist_fetch_and_relevance_checks",
            audit_evidence=f"url={candidate.url}; query={query}",
        )
        cache_update(root, raw_path, source_page, title=title)
        candidates_path = str(
            write_candidate_facts(
                root,
                title=title,
                source_page=source_page,
                external_url=candidate.url,
                evidence_role=candidate.evidence_role,
                evidence_excerpt=excerpt,
            )
        )
        created_sources.append(str(source_page))
        existing_urls.add(canonical_url)
        if fetch:
            fetched_raw_paths.append(str(raw_path))
        _append_log(root, f"{today_iso()} authority-discover | {candidate.url} | {source_page.relative_to(root).as_posix()}")

    report = AuthoritySourceReport(
        wiki_dir=str(root),
        query=query,
        accepted_count=len(created_sources),
        rejected_count=len(rejected),
        created_sources=tuple(created_sources),
        fetched_raw_paths=tuple(fetched_raw_paths),
        candidates_path=candidates_path,
        warnings=tuple(warnings),
        rejected_candidates=tuple(rejected),
    )
    if created_sources:
        _post_authority_closure(root, governance_request, report)
    else:
        append_governance_event(root, governance_request, phase="post_write_closure", status="no_effect", details={"warnings": warnings, "rejected": rejected})
    return report


def _parse_llm_suggestions(raw: str, warnings: list[str]) -> tuple[AuthorityCandidate, ...]:
    """把 LLM 输出的 JSON 解析为来源候选列表。

    支持的 JSON 形态：
        - ``[{"url": "..."}]``
        - ``{"sources": [...]}``
        - ``{"candidates": [...]}``
        - ``{"urls": ["https://..."]}``

    如果 JSON 无效或某一项缺少 URL，函数不会直接抛异常中断整批任务，
    而是把问题记录到 ``warnings``。这样一次发现任务可以同时报告多个
    问题，方便演示和批量维护。
    """
    text = str(raw or "").strip()
    if not text:
        return ()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        warnings.append(f"llm_suggestions_json_invalid:{exc.msg}")
        return ()
    if isinstance(payload, Mapping):
        values = payload.get("sources") or payload.get("candidates") or payload.get("urls") or []
    else:
        values = payload
    if not isinstance(values, list):
        warnings.append("llm_suggestions_json_no_list")
        return ()
    parsed: list[AuthorityCandidate] = []
    for index, item in enumerate(values):
        if isinstance(item, str):
            parsed.append(AuthorityCandidate(url=item.strip()))
            continue
        if isinstance(item, Mapping):
            url = str(item.get("url") or "").strip()
            if not url:
                warnings.append(f"llm_suggestion_missing_url:{index}")
                continue
            parsed.append(
                AuthorityCandidate(
                    url=url,
                    title=str(item.get("title") or "").strip(),
                    reason=str(item.get("reason") or "").strip(),
                    evidence_role=str(item.get("evidence_role") or item.get("role") or "").strip(),
                    authority_level=str(item.get("authority_level") or "").strip(),
                )
            )
            continue
        warnings.append(f"llm_suggestion_invalid_item:{index}")
    return tuple(parsed)


def _dedupe_candidates(candidates: Iterable[AuthorityCandidate]) -> tuple[AuthorityCandidate, ...]:
    """按 URL 去重，并保留第一次出现时携带的解释信息。

    LLM 搜索和人工补充可能同时给出同一个 URL。去重可以避免重复创建
    source page，也避免候选事实被重复追加。
    """
    seen: set[str] = set()
    result: list[AuthorityCandidate] = []
    for candidate in candidates:
        normalized = _canonical_url(candidate.url.strip())
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(AuthorityCandidate(candidate.url.strip(), candidate.title, candidate.reason, candidate.evidence_role, candidate.authority_level))
    return tuple(result)


def _prioritize_specific_candidates(candidates: Iterable[AuthorityCandidate]) -> tuple[AuthorityCandidate, ...]:
    """优先处理具体页面、公告页、PDF 或疾病手册页，降低官网首页的优先级。

    这不是把首页直接判定为非法，而是让同一批候选中更有证据价值的页面先落库。
    如果一轮里只有官网首页，首页仍然可以作为入口进入候选层；如果同时存在具体页面，
    具体页面会排在前面，减少“只新增入口页”的情况。
    """

    return tuple(sorted(candidates, key=lambda item: _specificity_score(item.url), reverse=True))


def _specificity_score(url: str) -> int:
    """计算 URL 的证据具体度分数，用于让公告、PDF、标准详情页优先。"""

    parsed = urlparse(url)
    path = parsed.path.strip("/")
    score = 0
    if path:
        score += min(path.count("/") + 1, 6) * 10
    lowered = url.lower()
    for marker in ("pdf", "manual", "standard", "disease", "newcastle", "avian-influenza", "notice", "公告", "标准", "诊断"):
        if marker in lowered:
            score += 12
    if not path or path in {"en", "zh", "zh-cn"}:
        score -= 30
    if parsed.query:
        score += 8
    return score


def _existing_external_urls(root: Path) -> set[str]:
    """读取现有 source 页和 raw/urls，形成跨知识库 URL 去重集合。"""

    urls: set[str] = set()
    for source_page in (root / "wiki" / "sources").glob("*.md"):
        text = source_page.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"^external_url:\s*(.+?)\s*$", text, flags=re.MULTILINE):
            value = match.group(1).strip().strip('"').strip("'")
            if value:
                urls.add(_canonical_url(value))
    for raw_url in (root / "raw" / "urls").glob("*.url.txt"):
        value = raw_url.read_text(encoding="utf-8", errors="replace").strip()
        if value:
            urls.add(_canonical_url(value))
    return urls


def _canonical_url(url: str) -> str:
    """规范化 URL，用于判断候选是否已经存在。

    规范化会统一协议和域名大小写，去掉默认首页尾部斜杠，排序 query 参数。
    这样 ``https://www.woah.org`` 和 ``https://www.woah.org/`` 会被视为同一个来源。
    """

    parsed = urlparse(str(url or "").strip())
    if not parsed.scheme or not parsed.netloc:
        return str(url or "").strip()
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = re.sub(r"/+", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = urlencode(sorted(parse_qsl(parsed.query, keep_blank_values=True)))
    return urlunparse((scheme, netloc, path, "", query, ""))


def _materialize_candidate(
    root: Path,
    candidate: AuthorityCandidate,
    *,
    query: str,
    fetch: bool,
    timeout_seconds: int,
) -> tuple[Path, str, str]:
    """把已通过白名单校验的来源保存到 ``raw/``。

    当 ``fetch=False`` 时，只在 ``raw/urls`` 记录 URL。这种方式不依赖网络
    抓取结果，适合稳定演示，也能保留“来源已发现但尚未抽取正文”的状态。

    当 ``fetch=True`` 时，会从通过校验的 URL 下载最多 2 MB 内容。PDF 保存
    到 ``raw/pdfs``，其他响应保存为 UTF-8 文本到 ``raw/html``，并生成一段
    简短摘录，方便后续人工复核。
    """

    if not fetch:
        raw_dir = root / "raw" / "urls"
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = _unique_path(raw_dir / f"{slugify(candidate.title or candidate.url, fallback='authority-url')}.url.txt")
        raw_path.write_text(candidate.url + "\n", encoding="utf-8")
        return raw_path, "url", ""

    request = Request(candidate.url, headers={"User-Agent": "ChickenLLMWikiAuthorityBot/1.0"})
    with urlopen(request, timeout=timeout_seconds) as response:
        content_type = response.headers.get_content_type()
        body = response.read(2_000_000)
        suffix = _suffix_for_response(candidate.url, response.headers, content_type)
        source_type = "pdf" if suffix == ".pdf" else "html"
        raw_dir = root / ("raw/pdfs" if source_type == "pdf" else "raw/html")
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = _unique_path(raw_dir / f"{slugify(candidate.title or query or candidate.url, fallback='authority-source')}{suffix}")
        if source_type == "pdf":
            raw_path.write_bytes(body)
            excerpt = ""
        else:
            charset = response.headers.get_content_charset() or "utf-8"
            text = body.decode(charset, errors="replace")
            raw_path.write_text(text, encoding="utf-8")
            excerpt = _excerpt(text)
    return raw_path, source_type, excerpt


def _suffix_for_response(url: str, _headers: Message, content_type: str) -> str:
    """根据响应类型和 URL 路径选择稳定的文件后缀。"""
    if content_type == "application/pdf" or urlparse(url).path.lower().endswith(".pdf"):
        return ".pdf"
    return ".html"


def _excerpt(text: str) -> str:
    """从抓取到的 HTML 或文本中生成简短复核摘录。"""
    without_scripts = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    compact = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", without_scripts)).strip()
    return compact[:700]


def _has_relevant_evidence(excerpt: str, *, query: str, title: str) -> bool:
    """判断抓取摘要是否和本次知识需求或来源标题有明显关联。

    这一步避免把“权威网站首页、检索入口页、无关脚本页”当作可用权威数据落库。
    它不是事实判断，只是最低限度的相关性闸门；正式事实仍然需要后续复核。
    """

    text = str(excerpt or "").lower()
    if not text:
        return False
    terms = _evidence_terms(f"{query} {title}")
    if not terms:
        return True
    return any(term in text for term in terms)


def _evidence_terms(text: str) -> tuple[str, ...]:
    """从 query 和 title 中抽取用于相关性校验的关键词。"""

    lowered = str(text or "").lower()
    terms: set[str] = set()
    for token in re.findall(r"[a-z][a-z0-9-]{3,}", lowered):
        terms.add(token)
    for token in re.findall(r"[\u4e00-\u9fff]{2,}", lowered):
        if token not in {"权威来源", "更新", "官网", "官方", "国家标准"}:
            terms.add(token)
    aliases = {
        "新城疫": ("newcastle", "newcastle disease"),
        "禽流感": ("avian influenza", "influenza"),
        "兽药": ("veterinary", "drug", "residue"),
        "休药期": ("withdrawal", "withdrawal period"),
        "禁用": ("prohibited", "ban", "banned"),
        "诊断": ("diagnosis", "diagnostic"),
        "标准": ("standard", "manual"),
    }
    for cn, values in aliases.items():
        if cn in text:
            terms.update(values)
    return tuple(sorted(terms, key=len, reverse=True))


def _remove_unusable_raw(raw_path: Path) -> None:
    """删除未通过相关性校验的临时 raw 文件，避免无关抓取物进入知识库。"""

    try:
        raw_path.unlink(missing_ok=True)
    except OSError:
        pass


def _title_from_url(url: str) -> str:
    """当 LLM 没有提供标题时，从 URL 路径推导一个可读标题。"""
    parsed = urlparse(url)
    tail = Path(parsed.path).name or parsed.hostname or "authority-source"
    return tail.replace("-", " ").replace("_", " ").strip() or url


def _hostname(url: str) -> str:
    """规范化域名，供白名单匹配使用。"""
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def _unique_path(path: Path) -> Path:
    """分配一个不会覆盖已有文件的 raw 路径。"""
    if not path.exists():
        return path
    for index in range(2, 10000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not allocate unique path for {path}")


def _append_log(root: Path, line: str) -> None:
    """向 Wiki 维护日志追加一条审计记录。"""
    log_path = root / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{line}\n")


def _post_authority_closure(root: Path, request: Any, report: AuthoritySourceReport) -> None:
    """Synchronize graph and audit state after authority source discovery."""

    from .graph import rebuild_graph
    from .operations import build_status_report, lint_wiki
    from .schema import schema_check

    schema_report = schema_check(root)
    lint_report = lint_wiki(root, strict=True)
    graph_report = rebuild_graph(root)
    status_report = build_status_report(root)
    details = {
        "accepted_count": report.accepted_count,
        "rejected_count": report.rejected_count,
        "created_sources": report.created_sources,
        "candidates_path": report.candidates_path,
        "schema_ok": schema_report.ok,
        "lint_ok": lint_report.ok,
        "graph_data_path": graph_report.graph_data_path,
        "graph_node_count": graph_report.node_count,
        "graph_link_count": graph_report.link_count,
        "fact_count": status_report.fact_count,
        "evidence_status_counts": status_report.evidence_status_counts,
    }
    status = "closed" if schema_report.ok and lint_report.ok else "closed_with_findings"
    append_governance_event(root, request, phase="post_write_closure", status=status, details=details)


__all__ = [
    "AuthorityCandidate",
    "AuthoritySourceReport",
    "allowed_authority_domains",
    "authority_level_for_url",
    "discover_authority_sources",
    "is_authoritative_url",
]
