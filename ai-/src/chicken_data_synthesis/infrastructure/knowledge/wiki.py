from __future__ import annotations
"""鸡病 LLM Wiki 的加载与检索模块。

这个模块负责把磁盘上的 Wiki 文件包加载成运行时可检索的知识库，并把检索
结果整理成可直接交给 LLM 的上下文。生成病例、评估病例、规则检查、CLI
查询和图谱构建都会依赖这里。

设计重点：
    检索时同时使用 Markdown 页面和结构化事实。Markdown 页面适合给 LLM
    提供可读背景；结构化事实适合提供精确的 subject/predicate/object、
    source id 和 evidence status。两者结合后，LLM 输出更容易被追溯和审计。
"""

import csv
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from chicken_data_synthesis.paths import PROJECT_ROOT

DEFAULT_LLM_WIKI_CONTEXT = "当前未检索到 LLM Wiki 证据，请优先输出保守、可复核、合规的结论。"
_TOKEN_PATTERN = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)
_SEARCH_EXCLUDED_RELPATHS = {
    "wiki/knowledge-graph.md",
}


@dataclass(frozen=True)
class LlmWikiPage:
    """从 Wiki 目录中加载出来的一页 Markdown 文档。

    它保存页面标题、相对路径、所属栏目和正文文本，是页面级检索的基本单元。
    """
    title: str
    relpath: str
    section: str
    text: str


@dataclass(frozen=True)
class LlmWikiSearchHit:
    """一次页面检索命中的结果。

    ``score`` 表示该页面和查询的相关度，``excerpt`` 是围绕命中词生成的
    摘要片段，方便 CLI 或 LLM 快速判断为什么这页被召回。
    """
    title: str
    relpath: str
    section: str
    score: float
    excerpt: str


@dataclass(frozen=True)
class LlmWikiKnowledgeBase:
    """Wiki 知识库的内存视图。

    这个对象把页面、正式结构化事实、疾病索引、规则索引、药品索引放在一起，
    使上层查询不需要反复读取磁盘文件。
    """
    root: Path
    pages: tuple[LlmWikiPage, ...]
    facts: tuple[dict[str, Any], ...]
    disease_index: tuple[dict[str, str], ...]
    rule_index: tuple[dict[str, str], ...]
    drug_index: tuple[dict[str, str], ...]

    def disease_names(self) -> tuple[str, ...]:
        """从疾病索引中返回去重后的疾病名称。

        该方法常用于判断生成或评估结果是否命中了项目内已知疾病。
        """
        names = [
            row.get("disease_name", "").strip()
            for row in self.disease_index
            if row.get("disease_name", "").strip()
        ]
        return tuple(dict.fromkeys(names))

    def search(self, query: str, *, top_k: int = 6) -> tuple[LlmWikiSearchHit, ...]:
        """使用确定性的词项打分检索 Markdown 页面。

        这里没有调用外部向量库，目的是让演示和测试结果稳定可复现。查询词会
        和页面标题、路径、正文进行匹配，并按分数返回最相关的页面。
        """
        tokens = _tokenize(query)
        if not tokens:
            return ()

        hits: list[LlmWikiSearchHit] = []
        for page in self.pages:
            searchable = f"{page.title}\n{page.relpath}\n{page.text}".lower()
            score = _score_page(page, searchable, tokens)
            if score <= 0:
                continue
            hits.append(
                LlmWikiSearchHit(
                    title=page.title,
                    relpath=page.relpath,
                    section=page.section,
                    score=score,
                    excerpt=_excerpt(page.text, tokens),
                )
            )

        hits.sort(key=lambda item: item.score, reverse=True)
        return tuple(hits[: max(int(top_k), 1)])

    def search_facts(self, query: str, *, top_k: int = 8) -> tuple[dict[str, Any], ...]:
        """检索正式结构化事实，返回带来源依据的证据片段。

        这些事实来自 ``exports/knowledge_facts.json``，通常包含
        ``evidence_source_id``、``evidence_url`` 和 source trust / evidence coverage / usage scope，
        是生成和评估时最重要的可追溯依据。
        """
        tokens = _tokenize(query)
        if not tokens:
            return ()

        scored: list[tuple[float, dict[str, Any]]] = []
        for fact in self.facts:
            text = json.dumps(fact, ensure_ascii=False).lower()
            score = _score_fact(fact, text, tokens)
            if score > 0:
                scored.append((score, fact))
        scored.sort(key=lambda item: item[0], reverse=True)
        return tuple(dict(fact) for _, fact in scored[: max(int(top_k), 1)])


def resolve_llm_wiki_dir(config: Mapping[str, Any] | None = None, repo_root: str | Path | None = None) -> Path:
    """解析 LLM Wiki 目录。

    如果配置里提供了 ``rule_base.llm_wiki_dir``，就优先使用配置值；如果是
    相对路径，则按项目根目录解析。没有配置时，默认使用
    ``knowledge/llm_wiki_chicken_authoritative``。这样 CLI、工具函数和测试
    都能指向同一个默认知识库。
    """
    root = Path(repo_root).resolve() if repo_root is not None else PROJECT_ROOT
    rule_config = config.get("rule_base", {}) if isinstance(config, Mapping) else {}
    configured = ""
    if isinstance(rule_config, Mapping):
        configured = str(rule_config.get("llm_wiki_dir") or "").strip()
    if not configured:
        configured = "knowledge/llm_wiki_chicken_authoritative"

    candidate = Path(configured)
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def load_llm_wiki(wiki_dir: str | Path) -> LlmWikiKnowledgeBase:
    """加载 Wiki 页面、正式事实和索引，并使用进程内缓存。

    缓存可以减少一次生成/评估过程中反复读取同一批文件的开销。
    """
    return _load_llm_wiki_cached(str(Path(wiki_dir).resolve()))


def clear_llm_wiki_cache() -> None:
    """清理 Wiki 加载缓存。

    当图谱重建、测试或知识库文件刚刚发生变化时，需要清理缓存，确保下一次
    读取的是磁盘上的最新内容。
    """
    _load_llm_wiki_cached.cache_clear()


def build_llm_wiki_context(
    query: str,
    *,
    wiki_dir: str | Path,
    top_k_pages: int = 5,
    top_k_facts: int = 8,
    max_chars: int = 4200,
) -> str:
    """为 LLM 生成或评估构建可直接使用的检索上下文。

    返回文本会明确提醒 LLM：不能编造没有上下文支持的监管或用药结论。
    同时上下文会包含页面命中和事实命中，并带上 source id 与 coverage/trust/scope，
    这样后续生成结果可以被审计到具体来源。
    """
    kb = load_llm_wiki(wiki_dir)
    hits = kb.search(query, top_k=top_k_pages)
    facts = kb.search_facts(query, top_k=top_k_facts)
    if not hits and not facts:
        return DEFAULT_LLM_WIKI_CONTEXT

    lines: list[str] = [
        "LLM Wiki 知识上下文（用于生成与评估，不能编造未被上下文支持的监管/用药结论）："
    ]
    if hits:
        lines.append("相关 Wiki 页：")
        for index, hit in enumerate(hits, start=1):
            lines.append(
                f"{index}. [{hit.section}] {hit.title} ({hit.relpath}) score={hit.score:.1f}\n"
                f"   摘要: {hit.excerpt}"
            )
    if facts:
        lines.append("相关结构化事实：")
        for index, fact in enumerate(facts, start=1):
            source = fact.get("evidence_source_id") or fact.get("evidence_source") or "unknown_source"
            trust, coverage, scope = _fact_status_fields(fact)
            lines.append(
                f"{index}. {fact.get('subject', '')} | {fact.get('predicate', '')} | "
                f"{fact.get('object', '')} | source={source} | "
                f"coverage={coverage} | trust={trust} | scope={scope}"
            )

    context = "\n".join(lines)
    if len(context) <= max_chars:
        return context
    return context[: max(int(max_chars), 500)].rstrip() + "\n...（LLM Wiki 上下文已截断）"


@lru_cache(maxsize=4)
def _load_llm_wiki_cached(wiki_dir: str) -> LlmWikiKnowledgeBase:
    """从磁盘加载 Wiki 包的缓存实现。"""
    root = Path(wiki_dir)
    if not root.is_dir():
        return LlmWikiKnowledgeBase(root=root, pages=(), facts=(), disease_index=(), rule_index=(), drug_index=())

    return LlmWikiKnowledgeBase(
        root=root,
        pages=tuple(_load_pages(root)),
        facts=tuple(_load_json_array(root / "exports" / "knowledge_facts.json")),
        disease_index=tuple(_load_csv(root / "exports" / "disease_index.csv")),
        rule_index=tuple(_load_csv(root / "exports" / "rule_index.csv")),
        drug_index=tuple(_load_csv(root / "exports" / "drug_page_index.csv")),
    )


def _load_pages(root: Path) -> Iterable[LlmWikiPage]:
    """加载 Wiki 中的 Markdown 页面，并排除自动生成的图谱说明文件。

    图谱说明文件是派生产物，不应该参与普通检索，否则 query 可能召回一堆
    图谱元信息，而不是疾病、药品、规则等实际知识页面。
    """
    for path in sorted((root / "wiki").rglob("*.md")):
        relpath = path.relative_to(root).as_posix()
        if relpath in _SEARCH_EXCLUDED_RELPATHS:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        section = path.parent.name
        title = _title_from_markdown(text) or path.stem
        yield LlmWikiPage(title=title, relpath=relpath, section=section, text=_compact(text))

    for path in (root / "index.md", root / "purpose.md", root / ".wiki-schema.md"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8-sig")
        yield LlmWikiPage(
            title=_title_from_markdown(text) or path.stem,
            relpath=path.relative_to(root).as_posix(),
            section="root",
            text=_compact(text),
        )


def _load_csv(path: Path) -> list[dict[str, str]]:
    """把 CSV 索引文件读取为字典列表。"""
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _load_json_array(path: Path) -> list[dict[str, Any]]:
    """读取 JSON 数组导出文件；文件不存在或格式不合法时返回空列表。

    这样可以避免某个导出文件缺失时整个查询流程崩溃。
    """
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, list):
        return []
    return [dict(item) for item in payload if isinstance(item, Mapping)]


def _fact_status_fields(fact: Mapping[str, Any]) -> tuple[str, str, str]:
    """Return normalized fact status fields without exposing legacy review labels."""
    trust = str(fact.get("source_trust") or "").strip()
    coverage = str(fact.get("evidence_coverage") or "").strip()
    raw_scope = fact.get("usage_scope") or fact.get("scope") or ""
    if isinstance(raw_scope, (list, tuple, set)):
        scope_items = [str(item).strip() for item in raw_scope if str(item).strip()]
    else:
        scope_items = [item.strip() for item in str(raw_scope).replace(";", ",").split(",") if item.strip()]

    if not trust or not coverage or not scope_items:
        legacy = str(fact.get("legacy_evidence_status") or fact.get("evidence_status") or "").strip()
        if legacy in {"HUMAN_REVIEWED", "EXTRACTED", "PROCESSED_SOURCE_ANCHORED"}:
            trust = trust or "authoritative"
            coverage = coverage or "complete"
            scope_items = scope_items or ["retrieval", "generation_context", "evaluation"]
        elif legacy in {"NEEDS_REVIEW", "UNVERIFIED"}:
            trust = trust or "needs_source_check"
            coverage = coverage or "partial"
            scope_items = scope_items or ["retrieval", "gap_routing", "audit_only"]

    return trust or "unknown", coverage or "unknown", ",".join(scope_items) or "retrieval"


def _title_from_markdown(text: str) -> str:
    """提取 Markdown 第一层标题作为页面标题。"""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def _tokenize(text: str) -> tuple[str, ...]:
    """对英文和中文文本分词，并为中文补充二字片段以提高召回。

    中文没有天然空格，如果只按整段匹配，很多短查询会召回不足。加入二字片段
    后，例如“新城疫”也能产生“新城”“城疫”等匹配信号。
    """
    raw_tokens = _TOKEN_PATTERN.findall(str(text or "").lower())
    tokens: list[str] = []
    for token in raw_tokens:
        if len(token) <= 1 and not ("\u4e00" <= token <= "\u9fff"):
            continue
        tokens.append(token)
        if _contains_cjk(token) and len(token) > 2:
            tokens.extend(token[index : index + 2] for index in range(len(token) - 1))
    return tuple(dict.fromkeys(tokens))


def _score_text(text: str, tokens: Sequence[str]) -> float:
    """根据查询词是否出现在文本中计算基础分数。"""
    score = 0.0
    for token in tokens:
        if token in text:
            score += 4.0 if len(token) >= 3 else 1.0
    return score


def _score_page(page: LlmWikiPage, searchable: str, tokens: Sequence[str]) -> float:
    """计算单个页面和查询之间的相关度分数。

    标题命中的权重最高，路径命中次之，正文命中作为基础分。疾病、药品、
    规则等核心栏目会略微加权，使业务知识页面优先于一般说明页。
    """
    score = _score_text(searchable, tokens)
    title = page.title.lower()
    relpath = page.relpath.lower()
    for token in tokens:
        if token in title:
            score += 10.0
        if token in relpath:
            score += 3.0
    if page.section in {"diseases", "drugs", "rules", "rule_cards", "syndromes"}:
        score += 1.5
    return score


def _score_fact(fact: Mapping[str, Any], text: str, tokens: Sequence[str]) -> float:
    """计算单条结构化事实和查询之间的相关度分数。

    ``subject`` 和 ``predicate`` 的命中权重较高，因为它们直接说明事实对象
    和事实关系。涉及禁用、监管、诊断标准等高价值谓词时会额外加权。
    """
    score = _score_text(text, tokens)
    subject = str(fact.get("subject") or "").lower()
    predicate = str(fact.get("predicate") or "").lower()
    fact_type = str(fact.get("fact_type") or "").lower()
    for token in tokens:
        if token in subject:
            score += 12.0
        if token in predicate:
            score += 5.0
    if any(marker in predicate for marker in ("prohibited", "restriction", "ban", "regulatory")):
        score += 6.0
    if any(marker in fact_type for marker in ("drug", "rule", "diagnosis_standard")):
        score += 2.0
    return score


def _excerpt(text: str, tokens: Sequence[str], *, max_chars: int = 420) -> str:
    """围绕第一个命中词生成简短摘要。"""
    compact = _compact(text)
    lower_text = compact.lower()
    match_positions = [lower_text.find(token) for token in tokens if token in lower_text]
    start = min([position for position in match_positions if position >= 0], default=0)
    start = max(start - 80, 0)
    excerpt = compact[start : start + max_chars].strip()
    return excerpt.replace("\n", " ")


def _compact(text: str) -> str:
    """规范化空白字符，方便检索和拼接提示词片段。"""
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _contains_cjk(text: str) -> bool:
    """判断文本中是否包含中文、日文或韩文字符。"""
    return any("\u4e00" <= char <= "\u9fff" for char in text)
