from __future__ import annotations
"""LLM Wiki 自动维护模块。

本模块把三方大模型平台接入到现有 LLM Wiki 的安全维护链路中。它的目标
不是维护某一个固定鸡病，而是先从 Wiki 中扫描疾病、药品、规则和历史候选
欠账，动态生成本轮维护需求；再让大模型发现候选权威数据页，交给系统抓取
真实网页或 PDF、保存 raw 原文、抽取证据摘要、生成候选事实、执行分层复核
并重建图谱。

安全边界：
    - API key 只从环境变量读取，不写入代码和日志。
    - 大模型只能输出候选权威数据页 JSON，不能输出正式事实。
    - 通过白名单、去重和 fetch 相关性校验的数据只进入 raw/source/candidate 层。
    - 候选事实会执行分层自动复核，高风险事实不能由大模型直接写入正式库。
    - 每次维护结束后会重新执行 review、graph-build、schema-check、lint 和 status。
"""

import csv
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .authority import allowed_authority_domains, discover_authority_sources
from .graph import build_graph_data, rebuild_graph
from .operations import build_status_report, lint_wiki
from .review import review_candidate_facts
from .schema import schema_check

DEFAULT_NONELINEAR_BASE_URL = "https://api.nonelinear.com/v1"
DEFAULT_NONELINEAR_MODEL = "gpt-5.4-mini-medium"
DEFAULT_API_KEY_ENV = "NONELINEAR_API_KEY"

DEFAULT_MAINTENANCE_SEED_QUERIES: tuple[str, ...] = (
    "鸡新城疫 诊断标准 实验室确诊 权威来源 更新",
    "禽流感 鸡病 诊断标准 监管公告 WOAH 权威来源 更新",
    "蛋鸡 兽药 禁用 休药期 农业农村部 国家标准 权威来源 更新",
)
"""空 Wiki 或无法扫描缺口时使用的种子维护需求。

这些 query 只作为兜底启动项，不再代表长期自动维护的固定范围。正常情况下，
``run_daily_maintenance`` 会优先调用 ``build_maintenance_queries``，从当前
Wiki 的疾病页、药品页、规则页和候选欠账中动态生成本轮维护需求。
"""

# 兼容旧导入名。含义已经从“固定默认范围”调整为“兜底种子需求”。
DEFAULT_MAINTENANCE_QUERIES = DEFAULT_MAINTENANCE_SEED_QUERIES

DEFAULT_DYNAMIC_QUERY_LIMIT = 8

SWINE_GAP_REVIEW_RELATIVE_PATH = Path("issues") / "swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md"
SWINE_MAINTENANCE_SEED_QUERIES: tuple[str, ...] = (
    "猪病 LLM wiki 缺失内容优先补齐 实验室诊断 鉴别诊断 防控要点 权威来源 更新",
    "猪病 LLM wiki 药物页缺失 靶动物 适应证 给药途径 休药期 MRL 禁停用 官方标签 权威来源 更新",
    "猪病 LLM wiki 低可用率 generation_ready_limited NEEDS_REVIEW partial 优先补齐 来源证据 更新",
)
DEFAULT_PROTOCOL_CONTEXT_CHARS = 6000


@dataclass(frozen=True)
class LlmSourceSuggestion:
    """大模型返回的一条候选权威数据页。

    这里只记录 URL、标题、理由和证据角色，不记录正式事实。后续是否落库由
    ``authority-discover`` 的白名单、去重、fetch 和相关性校验决定。
    """

    url: str
    title: str = ""
    reason: str = ""
    evidence_role: str = ""


@dataclass(frozen=True)
class DailyMaintenanceReport:
    """每日维护执行报告。

    报告会说明调用了哪个模型、处理了哪些 query、哪些来源进入候选层、
    schema/lint/graph 的最终状态是什么。该报告适合 CLI JSON 输出和定时任务
    日志留存。
    """

    wiki_dir: str
    base_url: str
    model: str
    query_count: int
    maintenance_queries: tuple[str, ...]
    maintenance_protocol_path: str
    maintenance_protocol_digest: str
    gap_first_count: int
    accepted_count: int
    rejected_count: int
    candidate_sources: tuple[dict[str, str], ...]
    authority_reports: tuple[dict[str, Any], ...]
    review_report: dict[str, Any]
    graph_report: dict[str, Any]
    graph_change_report: dict[str, Any]
    status_report: dict[str, Any]
    schema_ok: bool
    lint_ok: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class MaintenanceTopic:
    """从 Wiki 缺口中生成的一条维护主题。

    ``kind`` 表示主题来自疾病、药品、规则还是历史候选欠账；``priority``
    越小越优先。维护 query 最终会交给大模型用于发现权威数据页。
    """

    query: str
    kind: str
    name: str
    priority: int
    reason: str


class NonelinearAuthorityClient:
    """面向 Nonelinear OpenAI 兼容接口的最小客户端。

    当前只实现每日维护所需的 chat completions 调用。这样项目不需要在此处
    引入新的 SDK，也便于测试中替换为假客户端。
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_NONELINEAR_BASE_URL,
        model: str = DEFAULT_NONELINEAR_MODEL,
        timeout_seconds: int = 60,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = int(timeout_seconds)

    def suggest_sources(self, query: str, *, max_sources: int = 5, protocol_context: str = "") -> str:
        """让大模型为一个知识需求生成候选权威数据页 JSON。

        返回值保持为原始 JSON 字符串，再由 ``authority-discover`` 继续解析。
        这里不抽取事实，也不直接判断事实真假。
        """

        body = {
            "model": self.model,
            "messages": _build_authority_messages(query, max_sources=max_sources, protocol_context=protocol_context),
            "response_format": {"type": "json_object"},
        }
        payload = self._chat_completion(body)
        return _content_from_chat_completion(payload)

    def _chat_completion(self, body: Mapping[str, Any]) -> Mapping[str, Any]:
        """调用 Nonelinear 的 OpenAI 兼容 chat completions 接口。

        不同三方平台对 OpenAI 参数的支持范围并不完全一致。这里默认不传
        ``temperature``，因为 ``gpt-5.4-mini-medium`` 只接受平台默认值。
        如果平台继续拒绝 ``response_format``，则自动去掉该参数重试一次；
        后续仍会通过 ``_normalize_llm_json`` 校验模型输出是否真的是 JSON。
        """

        try:
            return self._post_chat_completion(dict(body))
        except RuntimeError as exc:
            message = str(exc)
            if "response_format" not in message and "Unsupported parameter" not in message:
                raise
            fallback_body = dict(body)
            fallback_body.pop("response_format", None)
            return self._post_chat_completion(fallback_body)

    def _post_chat_completion(self, body: Mapping[str, Any]) -> Mapping[str, Any]:
        """发送一次 chat completions 请求，并把 HTTP 错误转换为可读异常。"""

        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Nonelinear API 调用失败: HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Nonelinear API 网络错误: {exc.reason}") from exc

        return payload


def build_maintenance_queries(
    wiki_dir: str | Path,
    *,
    limit: int = DEFAULT_DYNAMIC_QUERY_LIMIT,
) -> tuple[str, ...]:
    """根据当前 Wiki 内容动态生成本轮维护需求。

    这个函数是“自动维护整个鸡病知识库”的起点。它不再把维护范围固定为某
    一个疾病，而是扫描当前 Wiki 中的疾病页、药品页、规则页和候选事实欠账，
    生成一批本轮最值得让大模型查找权威数据的 query。

    生成策略：
        1. 优先处理候选事实中需要补抓取或补元数据的历史欠账。
        2. 疾病页生成“诊断标准/临床症状/实验室确诊”类权威来源需求。
        3. 药品页生成“禁用/休药期/官方监管”类权威来源需求。
        4. 规则页生成“监管规则/国家标准/官方公告”类权威来源需求。
        5. 如果 Wiki 为空或无法扫描到主题，才退回种子 query。
    """

    root = Path(wiki_dir)
    max_items = max(1, int(limit))
    candidate_topics: list[MaintenanceTopic] = []
    disease_topics: list[MaintenanceTopic] = []
    drug_topics: list[MaintenanceTopic] = []
    rule_topics: list[MaintenanceTopic] = []
    fact_subjects = _load_fact_subjects(root)

    for index, candidate in enumerate(_load_candidate_items(root)):
        decision = str(candidate.get("review_decision") or "")
        if decision not in {"LEGACY_NEEDS_FETCH", "LEGACY_NEEDS_METADATA"}:
            continue
        subject = _clean_topic_name(
            candidate.get("subject")
            or candidate.get("title")
            or candidate.get("external_url")
            or candidate.get("source_page")
            or "历史候选来源"
        )
        if not subject:
            continue
        reason = "历史候选缺少 raw 原文或来源元数据，需要优先补全证据链"
        candidate_topics.append(
            MaintenanceTopic(
                query=f"{subject} 鸡病 权威来源 原始证据 官方数据 补抓取 更新",
                kind="candidate_gap",
                name=subject,
                priority=10 + index,
                reason=reason,
            )
        )

    for index, name in enumerate(_iter_wiki_titles(root / "wiki" / "diseases")):
        missing_fact = name not in fact_subjects
        priority = 100 + (index if missing_fact else 1000 + index)
        reason = "疾病页缺少正式事实覆盖" if missing_fact else "疾病页需要周期性刷新权威诊断来源"
        disease_topics.append(
            MaintenanceTopic(
                query=f"{name} 鸡病 诊断标准 临床症状 实验室确诊 权威来源 更新",
                kind="disease",
                name=name,
                priority=priority,
                reason=reason,
            )
        )

    for index, name in enumerate(_iter_wiki_titles(root / "wiki" / "drugs")):
        missing_fact = name not in fact_subjects
        priority = 200 + (index if missing_fact else 1000 + index)
        reason = "药品页缺少正式事实覆盖" if missing_fact else "药品页需要周期性刷新禁用和休药期来源"
        drug_topics.append(
            MaintenanceTopic(
                query=f"{name} 鸡 兽药 禁用 休药期 官方来源 农业农村部 国家标准 更新",
                kind="drug",
                name=name,
                priority=priority,
                reason=reason,
            )
        )

    for index, name in enumerate(_iter_wiki_titles(root / "wiki" / "rules")):
        priority = 300 + index
        rule_topics.append(
            MaintenanceTopic(
                query=f"{name} 鸡 兽药 监管规则 禁用 休药期 官方公告 国家标准 更新",
                kind="rule",
                name=name,
                priority=priority,
                reason="规则页需要对齐最新官方公告和国家标准",
            )
        )

    queries = _dedupe_queries(
        topic.query
        for topic in _interleave_topic_buckets(
            (
                sorted(candidate_topics, key=lambda item: item.priority),
                sorted(disease_topics, key=lambda item: item.priority),
                sorted(drug_topics, key=lambda item: item.priority),
                sorted(rule_topics, key=lambda item: item.priority),
            )
        )
    )
    if not queries:
        queries = DEFAULT_MAINTENANCE_SEED_QUERIES
    return tuple(queries[:max_items])


def build_gap_first_maintenance_queries(
    wiki_dir: str | Path,
    *,
    limit: int = DEFAULT_DYNAMIC_QUERY_LIMIT,
    protocol_path: str | Path | None = None,
    gap_first: bool = True,
) -> tuple[str, ...]:
    """Build maintenance queries that start from explicit dataset readiness gaps.

    This wrapper keeps the legacy dynamic scan available, but for the swine wiki
    it first reads the deep gap review plus readiness exports so scheduled
    maintenance spends its first query budget on missing content and low task-use
    pages instead of generic refreshes.
    """

    root = Path(wiki_dir)
    max_items = max(1, int(limit))
    species = _detect_wiki_species(root)
    protocol = _load_maintenance_protocol(root, protocol_path=protocol_path)
    gap_topics: list[MaintenanceTopic] = []
    if gap_first:
        gap_topics.extend(_load_balanced_task_use_gap_topics(root, species=species, protocol=protocol))
        gap_topics.extend(_load_index_gap_topics(root, species=species, protocol=protocol))
        gap_topics.extend(_load_readiness_audit_gap_topics(root, species=species, protocol=protocol))

    gap_queries = _dedupe_queries(topic.query for topic in sorted(gap_topics, key=lambda item: item.priority))
    if len(gap_queries) >= max_items:
        return tuple(gap_queries[:max_items])

    remaining = max_items - len(gap_queries)
    legacy_queries = build_maintenance_queries(root, limit=max(remaining, DEFAULT_DYNAMIC_QUERY_LIMIT))
    if species == "swine":
        legacy_queries = tuple(_rewrite_legacy_query_for_swine(query, protocol=protocol) for query in legacy_queries)
    queries = _dedupe_queries((*gap_queries, *legacy_queries))
    if not queries:
        queries = SWINE_MAINTENANCE_SEED_QUERIES if species == "swine" else DEFAULT_MAINTENANCE_SEED_QUERIES
    return tuple(queries[:max_items])


def run_daily_maintenance(
    wiki_dir: str | Path,
    *,
    api_key: str = "",
    base_url: str = DEFAULT_NONELINEAR_BASE_URL,
    model: str = DEFAULT_NONELINEAR_MODEL,
    queries: Sequence[str] | None = None,
    query_limit: int = DEFAULT_DYNAMIC_QUERY_LIMIT,
    fetch: bool = True,
    max_sources_per_query: int = 5,
    timeout_seconds: int = 60,
    protocol_path: str | Path | None = None,
    gap_first: bool = True,
    client: NonelinearAuthorityClient | None = None,
) -> DailyMaintenanceReport:
    """执行一次完整的 LLM Wiki 自动维护。

    这个函数是“每天一次”的实际工作单元。定时任务只需要每天调用一次该函数
    对应的 CLI 命令即可。

    执行步骤：
        1. 如果调用方没有显式传入 query，先扫描 Wiki 缺口，动态生成维护需求。
        2. 调用三方 LLM，为每个知识需求发现候选权威数据页。
        3. 使用 ``authority-discover`` 校验白名单、抓取 raw 原文并写入候选层。
        4. 执行候选事实分层复核。
        5. 重建 ``graph-data.json`` 和 ``knowledge-graph.html``。
        6. 执行 schema-check、lint、status，形成可追溯报告。
    """

    #1.API key 读取
    root = Path(wiki_dir)
    key = api_key or os.environ.get(DEFAULT_API_KEY_ENV, "")
    if client is None and not key:
        raise RuntimeError(f"缺少 API key。请设置环境变量 {DEFAULT_API_KEY_ENV}。")

    #2. 客户端初始化
    llm_client = client or NonelinearAuthorityClient(
        api_key=key,
        base_url=base_url,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    #3. 累加器初始化
    warnings: list[str] = []
    authority_reports: list[dict[str, Any]] = []
    candidate_sources: list[dict[str, str]] = []
    accepted_total = 0
    rejected_total = 0
    graph_before = _safe_graph_snapshot(root)
    protocol_file, protocol_context = _load_maintenance_protocol_with_path(root, protocol_path=protocol_path)
    protocol_digest = _summarise_protocol(protocol_context)

    #4. Query 决定逻辑
    explicit_queries = tuple(str(query).strip() for query in (queries or ()) if str(query).strip())
    effective_queries = explicit_queries or build_gap_first_maintenance_queries(
        root,
        limit=query_limit,
        protocol_path=protocol_file,
        gap_first=gap_first,
    )
    gap_first_count = _count_gap_first_queries(effective_queries)
    #5. Query 循环
    for query in effective_queries:
        if not str(query).strip():
            continue
        # 1. LLM 建议候选 URL
        try:
            raw_suggestions = llm_client.suggest_sources(
                str(query),
                max_sources=max_sources_per_query,
                protocol_context=protocol_context[:DEFAULT_PROTOCOL_CONTEXT_CHARS],
            )
        except TypeError as exc:
            if "protocol_context" not in str(exc):
                raise
            raw_suggestions = llm_client.suggest_sources(
                str(query),
                max_sources=max_sources_per_query,
            )
        # 2. 规范化 JSON（去掉 markdown code block，验证格式）
        normalized_json = _normalize_llm_json(raw_suggestions, warnings)
        # 3. 提取候选来源摘要（用于报告）
        for item in _extract_candidate_sources(normalized_json):
            candidate_sources.append(item)
        # 4. 白名单校验 + 抓取 + 写入候选层
        report = discover_authority_sources(
            root,
            str(query),
            llm_suggestions_json=normalized_json,
            fetch=fetch,
            timeout_seconds=timeout_seconds,
        )
        # 5. 累加接受/拒绝计数
        accepted_total += report.accepted_count
        rejected_total += report.rejected_count
        # 6. 记录 authority 报告
        authority_reports.append(asdict(report))
        _append_log(
            root,
            _format_task_log_line(
                str(query),
                accepted=report.accepted_count,
                rejected=report.rejected_count,
                created_sources=report.created_sources,
                fetched_raw_paths=report.fetched_raw_paths,
                candidates_path=report.candidates_path,
                rejected_candidates=report.rejected_candidates,
            ),
        )

    review_report = review_candidate_facts(root)   # 候选事实分层复核
    graph_report = rebuild_graph(root)              # 重建图谱 JSON + HTML
    graph_after = _safe_graph_snapshot(root)
    graph_change_report = _diff_graph_snapshots(graph_before, graph_after)
    _append_log(root, _format_graph_diff_log_line(graph_change_report))
    schema_report = schema_check(root)             # Schema 校验
    lint_report = lint_wiki(root)                  # Lint 检查
    status_report = build_status_report(root)      # Wiki 健康快照

    return DailyMaintenanceReport(
        wiki_dir=str(root),
        base_url=base_url,
        model=model,
        query_count=len(tuple(query for query in effective_queries if str(query).strip())),
        maintenance_queries=tuple(query for query in effective_queries if str(query).strip()),
        maintenance_protocol_path=str(protocol_file) if protocol_file else "",
        maintenance_protocol_digest=protocol_digest,
        gap_first_count=gap_first_count,
        accepted_count=accepted_total,
        rejected_count=rejected_total,
        candidate_sources=tuple(candidate_sources),
        authority_reports=tuple(authority_reports),
        review_report=asdict(review_report),
        graph_report=asdict(graph_report),
        graph_change_report=graph_change_report,
        status_report=asdict(status_report),
        schema_ok=schema_report.ok,
        lint_ok=lint_report.ok,
        warnings=tuple(warnings),
    )


def _build_authority_messages(query: str, *, max_sources: int, protocol_context: str = "") -> list[dict[str, str]]:
    """构建给大模型的受控提示词。

    提示词要求模型优先寻找具体权威数据页面，而不是只返回官网首页。
    模型仍然不能输出正式事实、诊断结论或用药建议；事实是否可用由抓取、
    候选层和复核流程决定。
    """

    domains = "\n".join(f"- {domain}" for domain in allowed_authority_domains())
    protocol_note = ""
    if protocol_context:
        protocol_note = (
            "\n维护协议摘要（用于确定来源优先级，不要把摘要改写成事实）：\n"
            f"{protocol_context[:DEFAULT_PROTOCOL_CONTEXT_CHARS]}\n"
        )
    system = (
        "你是鸡病 LLM Wiki 的权威数据发现助手。"
        "你的任务不是写事实，不是总结诊断标准，也不是给用药建议。"
        "你只能基于允许域名寻找候选权威数据页面 URL，并输出 JSON。"
    )
    user = f"""请为下面的真实知识需求寻找候选权威数据页 URL。

知识需求：
{query}
{protocol_note}

只允许以下域名：
{domains}

要求：
1. 如果你具备 web access，请优先访问上述域名搜索最新权威来源。
2. 优先返回具体数据页面、公告详情页、标准详情页、疾病手册页、PDF 页面或可直接下载的 PDF URL。
3. 不要优先返回官网首页；只有确实找不到具体页面时，才返回官网首页作为入口。
4. 如果无法访问网页，只能返回你能确认属于上述域名的候选入口，不要编造 URL。
5. 只输出 JSON，不要输出解释文本。
6. 不要输出任何正式事实、诊断结论、用药结论或监管结论。
7. 最多输出 {max_sources} 个来源。

JSON 格式：
{{
  "sources": [
    {{
      "url": "https://...",
      "title": "来源标题",
      "reason": "为什么这个来源可能有用",
      "evidence_role": "diagnosis_standard | regulation | clinical_reference | drug_rule"
    }}
  ]
}}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def _detect_wiki_species(root: Path) -> str:
    path_text = str(root).lower()
    if "swine" in path_text or "porcine" in path_text or "pig" in path_text:
        return "swine"
    if (root / SWINE_GAP_REVIEW_RELATIVE_PATH).is_file():
        return "swine"
    return "chicken"


def _load_maintenance_protocol_with_path(
    root: Path,
    *,
    protocol_path: str | Path | None = None,
) -> tuple[Path | None, str]:
    candidates: list[Path] = []
    if protocol_path:
        candidates.append(Path(protocol_path))
    if _detect_wiki_species(root) == "swine":
        candidates.append(root / SWINE_GAP_REVIEW_RELATIVE_PATH)
    for path in candidates:
        resolved = path if path.is_absolute() else (root / path)
        try:
            text = resolved.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        return resolved, text
    return None, ""


def _load_maintenance_protocol(root: Path, *, protocol_path: str | Path | None = None) -> str:
    return _load_maintenance_protocol_with_path(root, protocol_path=protocol_path)[1]


def _summarise_protocol(text: str) -> str:
    if not text:
        return ""
    useful_lines: list[str] = []
    needles = (
        "V16",
        "balanced",
        "五级",
        "A0/A1",
        "train_ready",
        "generation_ready_limited",
        "缺失",
        "优先",
        "HUMAN_REVIEWED",
        "NEEDS_REVIEW",
        "partial",
    )
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and any(needle in stripped for needle in needles):
            useful_lines.append(stripped)
        if len(useful_lines) >= 12:
            break
    return "\n".join(useful_lines)[:1200]


def _maintenance_query(subject: str, *, kind: str, species: str, protocol: str, focus: str) -> str:
    domain = "猪病 LLM wiki" if species == "swine" else "LLM wiki"
    protocol_name = SWINE_GAP_REVIEW_RELATIVE_PATH.name if species == "swine" else "maintenance protocol"
    policy = (
        "按 V16 balanced source-use：弱化中国标签事实和 A0/A1 作为通用门槛；五级合格来源可用于 bounded generation；"
        "只有剂量、休药期、MRL、禁停用、扑杀、调运、食品安全等高风险可执行事实需要官方/标签/标准来源。"
        if species == "swine"
        else "按来源分级和候选复核策略补齐缺失证据。"
    )
    return (
        f"GAP-FIRST | {domain} | {kind} | {subject} | 基于 {protocol_name} 优先补缺。"
        f"{focus} {policy} 只寻找候选权威来源 URL，不输出事实结论。"
    )


def _load_balanced_task_use_gap_topics(root: Path, *, species: str, protocol: str) -> list[MaintenanceTopic]:
    path = root / "exports" / "balanced_task_use_index.csv"
    topics: list[MaintenanceTopic] = []
    for index, row in enumerate(_read_csv_rows(path)):
        task_use = str(row.get("task_use") or "")
        evidence_status = str(row.get("evidence_status") or "")
        reason = str(row.get("reason") or "")
        if task_use == "train_ready" and evidence_status == "HUMAN_REVIEWED":
            continue
        title = _query_title(row, fallback=row.get("entity_id") or row.get("page_relpath") or "")
        entity_type = str(row.get("entity_type") or "entity")
        focus = (
            f"当前 task_use={task_use or 'unknown'} evidence_status={evidence_status or 'unknown'}；"
            f"优先补齐导致低可用率的缺失来源：{reason or 'source/facet gap'}。"
        )
        topics.append(
            MaintenanceTopic(
                query=_maintenance_query(title, kind=f"{entity_type}_task_use_gap", species=species, protocol=protocol, focus=focus),
                kind="balanced_task_use_gap",
                name=title,
                priority=_priority_for_task_use(task_use, evidence_status) + index,
                reason=focus,
            )
        )
    return topics


def _load_index_gap_topics(root: Path, *, species: str, protocol: str) -> list[MaintenanceTopic]:
    topics: list[MaintenanceTopic] = []
    disease_path = root / "exports" / "disease_index.csv"
    for index, row in enumerate(_read_csv_rows(disease_path)):
        status = str(row.get("coverage_gap_status") or "")
        if "partial" not in status.lower():
            continue
        title = _query_title(row, fallback=row.get("disease_id") or row.get("page_relpath") or "")
        topics.append(
            MaintenanceTopic(
                query=_maintenance_query(
                    title,
                    kind="disease_partial_gap",
                    species=species,
                    protocol=protocol,
                    focus=(
                        f"coverage_gap_status={status}；优先补齐疾病页缺失字段，尤其是实验室诊断、鉴别诊断、防控要点和来源锚点。"
                    ),
                ),
                kind="disease_partial_gap",
                name=title,
                priority=1200 + index,
                reason=status,
            )
        )

    drug_path = root / "exports" / "drug_gold_role_index.csv"
    for index, row in enumerate(_read_csv_rows(drug_path)):
        evidence_status = str(row.get("evidence_status") or "")
        gold_use = str(row.get("gold_dataset_use") or "")
        if evidence_status == "HUMAN_REVIEWED" and gold_use != "boundary_only":
            continue
        title = _query_title(row, fallback=row.get("drug_id") or row.get("page_relpath") or "")
        topics.append(
            MaintenanceTopic(
                query=_maintenance_query(
                    title,
                    kind="drug_review_gap",
                    species=species,
                    protocol=protocol,
                    focus=(
                        f"drug evidence_status={evidence_status or 'unknown'} gold_dataset_use={gold_use or 'unknown'}；"
                        "优先补齐标签、适应证、靶动物、禁停用、MRL/休药期和边界来源。"
                    ),
                ),
                kind="drug_review_gap",
                name=title,
                priority=1300 + index,
                reason=f"{evidence_status}/{gold_use}",
            )
        )
    return topics


def _load_readiness_audit_gap_topics(root: Path, *, species: str, protocol: str) -> list[MaintenanceTopic]:
    path = root / "issues" / "dataset_readiness_audit.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return []
    topics: list[MaintenanceTopic] = []
    for index, item in enumerate(payload.get("worst_disease_core_gaps") or []):
        if not isinstance(item, Mapping):
            continue
        page = str(item.get("page") or "").strip()
        if not page:
            continue
        title = _clean_topic_name(Path(page).stem)
        topics.append(
            MaintenanceTopic(
                query=_maintenance_query(
                    title,
                    kind="short_or_core_gap_disease",
                    species=species,
                    protocol=protocol,
                    focus=f"dataset_readiness_audit 标记为短页/核心缺口页 page={page}；优先补齐缺失内容和来源证据。",
                ),
                kind="readiness_audit_gap",
                name=title,
                priority=1400 + index,
                reason=f"dataset_readiness_audit:{page}",
            )
        )
    return topics


def _read_csv_rows(path: Path) -> tuple[dict[str, str], ...]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return tuple(dict(row) for row in csv.DictReader(handle))
    except OSError:
        return ()


def _query_title(row: Mapping[str, Any], *, fallback: Any = "") -> str:
    for key in ("title", "disease_name", "name", "entity_id", "disease_id", "drug_id", "page_relpath"):
        value = _clean_topic_name(row.get(key))
        if value:
            return value
    return _clean_topic_name(fallback)


def _priority_for_task_use(task_use: str, evidence_status: str) -> int:
    if task_use == "blocked":
        return 100
    if task_use == "retrieval_only":
        return 200
    if evidence_status == "NEEDS_REVIEW":
        return 300
    if task_use == "generation_ready_limited":
        return 400
    if "partial" in task_use:
        return 500
    return 900


def _rewrite_legacy_query_for_swine(query: str, *, protocol: str) -> str:
    text = str(query or "").strip()
    if not text:
        return text
    text = text.replace("鸡病", "猪病").replace("蛋鸡", "猪").replace("鸡", "猪")
    return _maintenance_query(
        text,
        kind="legacy_dynamic_gap",
        species="swine",
        protocol=protocol,
        focus="来自 wiki 动态扫描的补缺/刷新需求；按猪病知识库缺失内容优先维护。",
    )


def _count_gap_first_queries(queries: Sequence[str]) -> int:
    return sum(1 for query in queries if str(query).startswith("GAP-FIRST"))


def _iter_wiki_titles(directory: Path) -> tuple[str, ...]:
    """读取某个 Wiki 分区下的页面标题。

    优先读取 Markdown 一级标题；如果没有标题，则使用文件名去掉编号和后缀后
    作为维护主题。这样维护任务来自 Wiki 当前内容，而不是写死在代码里。
    """

    if not directory.is_dir():
        return ()
    names: list[str] = []
    for path in sorted(directory.glob("*.md")):
        if path.name.startswith("."):
            continue
        title = _read_markdown_title(path) or _title_from_filename(path)
        title = _clean_topic_name(title)
        if title:
            names.append(title)
    return tuple(dict.fromkeys(names))


def _read_markdown_title(path: Path) -> str:
    """读取 Markdown 文件的第一个一级标题。"""

    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    except OSError:
        return ""
    return ""


def _title_from_filename(path: Path) -> str:
    """从文件名推导页面主题名。"""

    stem = path.stem
    stem = re.sub(r"^(DIS|DRUG|RULE|SRC)-\d+[-_]*", "", stem, flags=re.IGNORECASE)
    stem = stem.replace("-", " ").replace("_", " ").strip()
    return stem


def _load_fact_subjects(root: Path) -> set[str]:
    """读取正式事实中的 subject，用于判断哪些页面缺少事实覆盖。"""

    facts_path = root / "exports" / "knowledge_facts.json"
    try:
        payload = json.loads(facts_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    if not isinstance(payload, list):
        return set()
    subjects: set[str] = set()
    for item in payload:
        if not isinstance(item, Mapping):
            continue
        subject = _clean_topic_name(item.get("subject"))
        if subject:
            subjects.add(subject)
    return subjects


def _load_candidate_items(root: Path) -> tuple[Mapping[str, Any], ...]:
    """读取候选事实，用于优先生成补抓取、补元数据维护任务。"""

    candidates_path = root / "exports" / "knowledge_facts.candidates.json"
    try:
        payload = json.loads(candidates_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ()
    if not isinstance(payload, list):
        return ()
    return tuple(item for item in payload if isinstance(item, Mapping))


def _clean_topic_name(value: Any) -> str:
    """清理从 Wiki 文件、事实或候选记录中读取到的主题名。"""

    text = str(value or "").strip()
    text = re.sub(r"\s+", " ", text)
    text = text.strip("#:：-—,，。；; ")
    return text[:80]


def _dedupe_queries(values: Iterable[str]) -> tuple[str, ...]:
    """按顺序去重维护 query。"""

    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        query = str(value or "").strip()
        if not query or query in seen:
            continue
        seen.add(query)
        result.append(query)
    return tuple(result)


def _safe_graph_snapshot(root: Path) -> dict[str, Any]:
    """生成图谱快照，供维护前后对比使用。

    快照只保留节点、边和关键 metadata，不写任何文件。失败时返回空快照并
    让主流程继续，因为图谱对比不能阻断权威来源维护。
    """

    try:
        graph = build_graph_data(root)
    except Exception as exc:
        return {"error": str(exc), "nodes": {}, "links": set(), "metadata": {}}
    nodes: dict[str, str] = {}
    for node in graph.get("nodes") or []:
        if isinstance(node, Mapping):
            node_id = str(node.get("id") or "")
            if node_id:
                nodes[node_id] = str(node.get("label") or node_id)
    links: set[tuple[str, str, str, str, str]] = set()
    for link in graph.get("links") or []:
        if isinstance(link, Mapping):
            source = str(link.get("source") or "")
            target = str(link.get("target") or "")
            link_type = str(link.get("type") or "")
            predicate = str(link.get("predicate") or "")
            fact_id = str(link.get("fact_id") or "")
            if source and target:
                links.add((source, target, link_type, predicate, fact_id))
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), Mapping) else {}
    return {"nodes": nodes, "links": links, "metadata": dict(metadata)}


def _diff_graph_snapshots(before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]:
    """对比维护前后图谱快照，给报告和日志提供可解释变化。"""

    before_nodes = before.get("nodes") if isinstance(before.get("nodes"), Mapping) else {}
    after_nodes = after.get("nodes") if isinstance(after.get("nodes"), Mapping) else {}
    before_links = before.get("links") if isinstance(before.get("links"), set) else set()
    after_links = after.get("links") if isinstance(after.get("links"), set) else set()
    added_node_ids = sorted(set(after_nodes) - set(before_nodes))
    removed_node_ids = sorted(set(before_nodes) - set(after_nodes))
    added_links = sorted(after_links - before_links)
    removed_links = sorted(before_links - after_links)
    return {
        "before_node_count": len(before_nodes),
        "after_node_count": len(after_nodes),
        "before_link_count": len(before_links),
        "after_link_count": len(after_links),
        "added_node_count": len(added_node_ids),
        "removed_node_count": len(removed_node_ids),
        "added_link_count": len(added_links),
        "removed_link_count": len(removed_links),
        "added_nodes": tuple({"id": node_id, "label": str(after_nodes.get(node_id) or node_id)} for node_id in added_node_ids[:20]),
        "removed_nodes": tuple({"id": node_id, "label": str(before_nodes.get(node_id) or node_id)} for node_id in removed_node_ids[:20]),
        "added_links": tuple(
            {"source": source, "target": target, "type": link_type, "predicate": predicate, "fact_id": fact_id}
            for source, target, link_type, predicate, fact_id in added_links[:20]
        ),
        "removed_links": tuple(
            {"source": source, "target": target, "type": link_type, "predicate": predicate, "fact_id": fact_id}
            for source, target, link_type, predicate, fact_id in removed_links[:20]
        ),
        "reason": "graph_rebuilt_from_current_wiki_files_after_maintenance",
        "evidence": "wiki/graph-data.json; wiki/knowledge-graph.html",
        "before_error": str(before.get("error") or ""),
        "after_error": str(after.get("error") or ""),
    }


def _format_task_log_line(
    query: str,
    *,
    accepted: int,
    rejected: int,
    created_sources: Sequence[str],
    fetched_raw_paths: Sequence[str],
    candidates_path: str,
    rejected_candidates: Sequence[Mapping[str, str]],
) -> str:
    """生成单个维护任务的审计日志行。"""

    rejected_reasons = _count_rejected_reasons(rejected_candidates)
    return (
        f"{_today_iso()} maintenance-task"
        f" | query={_compact_log_value(query)}"
        f" | accepted={accepted}"
        f" | rejected={rejected}"
        f" | created_sources={_compact_sequence(created_sources)}"
        f" | fetched_raw={_compact_sequence(fetched_raw_paths)}"
        f" | candidates={_compact_log_value(candidates_path)}"
        f" | rejected_reasons={json.dumps(rejected_reasons, ensure_ascii=False, sort_keys=True)}"
        f" | reason=authority_discovery_task_completed"
        f" | evidence=authority_reports"
    )


def _format_graph_diff_log_line(report: Mapping[str, Any]) -> str:
    """生成图谱变化审计日志行。"""

    return (
        f"{_today_iso()} graph-diff"
        f" | nodes={report.get('before_node_count', 0)}->{report.get('after_node_count', 0)}"
        f" | links={report.get('before_link_count', 0)}->{report.get('after_link_count', 0)}"
        f" | added_nodes={report.get('added_node_count', 0)}"
        f" | removed_nodes={report.get('removed_node_count', 0)}"
        f" | added_links={report.get('added_link_count', 0)}"
        f" | removed_links={report.get('removed_link_count', 0)}"
        f" | reason={report.get('reason', '')}"
        f" | evidence={report.get('evidence', '')}"
    )


def _count_rejected_reasons(items: Sequence[Mapping[str, str]]) -> dict[str, int]:
    """统计一个维护任务中各类拒绝原因。"""

    result: dict[str, int] = {}
    for item in items:
        reason = str(item.get("reason") or "unknown")
        reason_key = reason.split(":", 1)[0]
        result[reason_key] = result.get(reason_key, 0) + 1
    return result


def _compact_sequence(values: Sequence[Any], *, limit: int = 3) -> str:
    """把路径列表压缩为日志友好的短文本。"""

    items = [_compact_log_value(value) for value in values[:limit]]
    suffix = f";+{len(values) - limit}" if len(values) > limit else ""
    return ",".join(items) + suffix


def _compact_log_value(value: Any, *, limit: int = 180) -> str:
    """压缩单个日志字段，避免日志行过长。"""

    text = str(value or "").replace("\n", " ").strip()
    return text[:limit]


def _today_iso() -> str:
    """返回本地日期字符串，供维护日志使用。"""

    from datetime import date

    return date.today().isoformat()


def _append_log(root: Path, line: str) -> None:
    """追加一次维护过程审计日志。"""

    log_path = root / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{line}\n")


def _interleave_topic_buckets(buckets: Sequence[Sequence[MaintenanceTopic]]) -> tuple[MaintenanceTopic, ...]:
    """按类别轮询维护主题，避免某一类缺口占满整轮维护。

    候选欠账仍然排在第一桶，能优先补 raw 和元数据；但疾病、药品、规则也会
    持续进入队列，保证定时维护面向整个鸡病知识库，而不是只处理单一类型。
    """

    result: list[MaintenanceTopic] = []
    max_len = max((len(bucket) for bucket in buckets), default=0)
    for index in range(max_len):
        for bucket in buckets:
            if index < len(bucket):
                result.append(bucket[index])
    return tuple(result)


def _content_from_chat_completion(payload: Mapping[str, Any]) -> str:
    """从 OpenAI 兼容 chat completion 响应中提取文本内容。"""

    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("Nonelinear API 响应缺少 choices。")
    first = choices[0]
    if not isinstance(first, Mapping):
        raise RuntimeError("Nonelinear API 响应 choices[0] 格式不正确。")
    message = first.get("message")
    if not isinstance(message, Mapping):
        raise RuntimeError("Nonelinear API 响应缺少 message。")
    content = str(message.get("content") or "").strip()
    if not content:
        raise RuntimeError("Nonelinear API 响应 content 为空。")
    return content


def _normalize_llm_json(raw: str, warnings: list[str]) -> str:
    """把模型输出规范化为 JSON 字符串。

    部分模型会把 JSON 包在 Markdown 代码块里，这里会去掉代码块并验证格式。
    格式不合法时返回空 sources，避免后续流程崩溃。
    """

    text = str(raw or "").strip()
    match = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(1).strip()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        warnings.append(f"llm_json_invalid:{exc.msg}")
        return '{"sources":[]}'
    if isinstance(payload, list):
        payload = {"sources": payload}
    if not isinstance(payload, Mapping):
        warnings.append("llm_json_not_object")
        return '{"sources":[]}'
    return json.dumps(payload, ensure_ascii=False)


def _extract_candidate_sources(raw_json: str) -> tuple[dict[str, str], ...]:
    """从规范化后的 JSON 中提取候选来源摘要，供维护报告展示。"""

    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError:
        return ()
    values = payload.get("sources") if isinstance(payload, Mapping) else []
    if not isinstance(values, list):
        return ()
    result: list[dict[str, str]] = []
    for item in values:
        if isinstance(item, str):
            result.append({"url": item, "title": "", "reason": "", "evidence_role": ""})
            continue
        if isinstance(item, Mapping):
            result.append(
                {
                    "url": str(item.get("url") or ""),
                    "title": str(item.get("title") or ""),
                    "reason": str(item.get("reason") or ""),
                    "evidence_role": str(item.get("evidence_role") or item.get("role") or ""),
                }
            )
    return tuple(result)


__all__ = [
    "DEFAULT_API_KEY_ENV",
    "DEFAULT_MAINTENANCE_QUERIES",
    "DEFAULT_NONELINEAR_BASE_URL",
    "DEFAULT_NONELINEAR_MODEL",
    "DailyMaintenanceReport",
    "LlmSourceSuggestion",
    "MaintenanceTopic",
    "NonelinearAuthorityClient",
    "build_maintenance_queries",
    "run_daily_maintenance",
]
