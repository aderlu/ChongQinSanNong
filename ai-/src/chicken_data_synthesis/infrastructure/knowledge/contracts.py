from __future__ import annotations

from dataclasses import dataclass


# 这里集中定义 init、lint、ingest、graph 和 CLI 共同使用的静态契约。
# 这些常量让 LLM Wiki 的目录结构保持稳定，使自动维护流程能够明确知道：
# 原始证据、来源页、导出文件、问题记录和派生页面分别应该放在哪里。

CACHE_FILE_NAME = ".wiki-cache.json"
CACHE_VERSION = 1

# 根目录 Markdown 文件是 Wiki 最小的人类可读入口。
ROOT_MARKDOWN_FILES: tuple[str, ...] = (
    "index.md",
    "purpose.md",
    ".wiki-schema.md",
    "log.md",
)

# 必需目录把 raw 原始证据、Wiki 页面和机器导出文件明确分层。
REQUIRED_DIRECTORIES: tuple[str, ...] = (
    "raw",
    "raw/notes",
    "raw/html",
    "raw/pdfs",
    "raw/urls",
    "wiki",
    "wiki/diseases",
    "wiki/drugs",
    "wiki/rules",
    "wiki/rule_cards",
    "wiki/sources",
    "wiki/topics",
    "wiki/syndromes",
    "wiki/synthesis",
    "wiki/synthesis/sessions",
    "wiki/comparisons",
    "wiki/sessions",
    "wiki/queries",
    "exports",
    "issues",
)

# 必需导出文件会被检索、lint、图谱构建和演示命令读取。
REQUIRED_EXPORTS: tuple[str, ...] = (
    "knowledge_facts.json",
    "disease_index.csv",
    "rule_index.csv",
    "drug_page_index.csv",
)

# 权威来源发现允许访问的域名白名单。域名检查不能替代临床或监管复核，
# 但可以防止任意网页、论坛、博客、转载页面进入证据候选层。
AUTHORITY_ALLOWED_DOMAINS: tuple[str, ...] = (
    "moa.gov.cn", #农业农村部
    "std.cahec.cn", #中国动物卫生与流行病学中心 / 农业标准相关平台
    "openstd.samr.gov.cn", #国家标准全文公开系统
    "samr.gov.cn", #国家市场监督管理总局
    "woah.org", #世界动物卫生组织
    "merckvetmanual.com", #Merck Veterinary Manual 默克兽医手册，权威经典参考书
    "ema.europa.eu", #欧洲药品管理局
    "fao.org", #联合国粮农组织
)


@dataclass(frozen=True)
class WikiPaths:
    """高层 Wiki 操作使用的标准相对路径集合。"""

    cache: str = CACHE_FILE_NAME
    raw: str = "raw"
    wiki: str = "wiki"
    exports: str = "exports"
    issues: str = "issues"
    sources: str = "wiki/sources"
    synthesis: str = "wiki/synthesis"
    comparisons: str = "wiki/comparisons"
    sessions: str = "wiki/sessions"
    queries: str = "wiki/queries"


PAGE_TYPES: tuple[str, ...] = (
    # 领域知识和权威知识页面。
    "disease",
    "drug",
    "rule",
    "rule_card",
    "source",
    "topic",
    "syndrome",
    "synthesis",
    "comparison",
    "session",
    "query",
)

# 来源页必须包含的页头字段。这些字段保证自动摄取或网页发现后，
# 来源仍然可以被追溯、检查和复核。
SOURCE_FRONTMATTER_FIELDS: tuple[str, ...] = (
    "type",
    "source_id",
    "source_path",
    "source_type",
    "authority_level",
    "evidence_status",
    "created",
    "updated",
    "sources",
)
