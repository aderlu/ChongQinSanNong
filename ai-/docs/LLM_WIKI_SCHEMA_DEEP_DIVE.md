# LLM Wiki Schema 设计详解

文件位置：`D:\XF-ChongQin\ai-\knowledge\schemas\llm_wiki_schema.yaml`

更新时间：2026-05-04

## 1. 这个 Schema 是什么

`llm_wiki_schema.yaml` 不是普通意义上的“数据表结构定义”，而是鸡病系统 LLM Wiki 的运行契约。它约束的是整个知识库如何组织、如何导入来源、如何维护候选事实、如何检索、如何审计、如何生成知识图谱。

它解决的问题是：LLM 可以参与知识维护，但不能因为 LLM 会生成文字，就让未验证内容直接污染权威知识库。

因此这个 schema 的核心设计思想是：

```text
原始来源 raw
  -> 来源页 wiki/sources
  -> 候选事实 knowledge_facts.candidates.json
  -> 复核
  -> 正式事实 knowledge_facts.json
  -> 检索上下文
  -> 图谱和 HTML 展示
  -> 生成/评估结果审计
```

## 2. 为什么要这样设计

鸡病诊疗、用药、禁用药、休药期、产蛋鸡用药边界、国家标准和法规属于高风险知识。如果没有 schema 约束，会出现几个问题：

- LLM 可能把未验证内容写成确定结论。
- 来源 URL 可能不是权威来源。
- 知识库文件可能散乱，无法追溯。
- 候选事实和正式事实可能混在一起。
- HTML 图谱可能被误认为事实源。
- 最终生成/评估结果无法说明使用了哪些证据。

所以 schema 把知识库拆成多个层次：

| 层次 | 目录或文件 | 作用 |
| --- | --- | --- |
| 原始来源层 | `raw/` | 保存导入前的原始材料 |
| 来源记录层 | `wiki/sources/` | 记录来源 ID、路径、权威等级、证据状态 |
| 候选层 | `exports/knowledge_facts.candidates.json` | 保存待复核事实 |
| 权威事实层 | `exports/knowledge_facts.json` | 保存可用于生成/评估的正式事实 |
| 领域页面层 | `wiki/diseases`、`wiki/drugs`、`wiki/rules` | 保存可读的领域知识 |
| 检索层 | `query`、`context` | 给 LLM 提供证据上下文 |
| 图谱层 | `graph-data.json`、`knowledge-graph.html` | 可视化展示和审计 |
| 审计层 | CSV audit fields、`log.md` | 记录知识使用痕迹 |

## 3. 完整带注释 Schema

下面是当前 schema 的逐段注释版。注释使用 `#` 表示说明，不建议直接替换原文件，因为原文件保持纯净更利于程序读取。

```yaml
# Schema 名称。用于说明这是鸡病系统 LLM Wiki 的运行契约。
schema_name: chicken_llm_wiki_operations

# Schema 版本。后续如果目录结构、维护策略或审计字段变化，应提升版本。
version: 1.0.0

# 总体说明：这个 schema 管的是知识库组织、维护、验证、检索和审计。
description: >
  Runtime contract for how the chicken disease LLM Wiki knowledge base is
  organized, maintained, validated, retrieved, and audited.

# 适用范围。
# applies_to 表示该 schema 约束哪些目录和代码模块。
# not_applies_to 表示它不约束最终数据集行结构和评分字段。
scope:
  applies_to:
    - knowledge/llm_wiki_chicken_authoritative
    - chicken_data_synthesis.infrastructure.knowledge
  not_applies_to:
    - generated dataset row shape
    - final evaluation scoring field definitions
  archived_dataset_schema: knowledge/schemas/archive/schema_final_v2.legacy.yaml

# Wiki 根目录约束。
# 这一段定义 Wiki 必须有哪些根文件、目录和导出文件。
wiki_root:
  default_path: knowledge/llm_wiki_chicken_authoritative
  cache_file: .wiki-cache.json
  cache_version: 1

  # 根文件。
  # index.md 是入口。
  # purpose.md 说明知识库用途。
  # .wiki-schema.md 是 Wiki 内部可读 schema 说明。
  # log.md 记录维护动作。
  required_root_files:
    - index.md
    - purpose.md
    - .wiki-schema.md
    - log.md

  # 必须存在的目录。
  # raw 保存原始材料。
  # wiki 保存可读 Markdown 页面。
  # exports 保存结构化事实和索引。
  # issues 保存待处理问题。
  required_directories:
    - raw
    - raw/notes
    - raw/html
    - raw/pdfs
    - raw/urls
    - wiki
    - wiki/diseases
    - wiki/drugs
    - wiki/rules
    - wiki/rule_cards
    - wiki/sources
    - wiki/topics
    - wiki/syndromes
    - wiki/synthesis
    - wiki/synthesis/sessions
    - wiki/comparisons
    - wiki/sessions
    - wiki/queries
    - exports
    - issues

  # 必须存在的导出文件。
  # knowledge_facts.json 是正式事实库。
  # disease_index.csv、rule_index.csv、drug_page_index.csv 是检索和图谱的索引入口。
  required_exports:
    - knowledge_facts.json
    - disease_index.csv
    - rule_index.csv
    - drug_page_index.csv

# 页面组织方式。
# 这部分定义 Wiki 中不同页面类型的含义。
organization:
  page_types:
    disease:
      directory: wiki/diseases
      role: authoritative disease page
    drug:
      directory: wiki/drugs
      role: authoritative drug and medication page
    rule:
      directory: wiki/rules
      role: authoritative safety or regulatory rule
    rule_card:
      directory: wiki/rule_cards
      role: compact executable rule summary
    source:
      directory: wiki/sources
      role: evidence source record
    topic:
      directory: wiki/topics
      role: thematic concept page
    syndrome:
      directory: wiki/syndromes
      role: symptom or syndrome page
    synthesis:
      directory: wiki/synthesis
      role: derived synthesis page
    comparison:
      directory: wiki/comparisons
      role: derived comparison page
    session:
      directory: wiki/sessions
      role: derived working session page
    query:
      directory: wiki/queries
      role: derived saved retrieval answer

  # 权威页面类型。
  # 这些页面可以作为知识库的领域知识主体。
  authoritative_page_types:
    - disease
    - drug
    - rule
    - rule_card
    - source
    - topic
    - syndrome

  # 派生页面类型。
  # LLM 可以生成这些页面，但它们不是一手证据。
  derived_page_types:
    - synthesis
    - comparison
    - session
    - query

  # 命名规则。
  naming:
    source_page_prefix: SRC-
    disease_page_prefix: DIS-
    relation_style: wiki links plus explicit source ids

# 来源页面契约。
# 来源页是保证可追溯性的关键。
source_contract:
  # 每个 source page 必须有这些 frontmatter 字段。
  required_frontmatter_fields:
    - type
    - source_id
    - source_path
    - source_type
    - authority_level
    - evidence_status
    - created
    - updated
    - sources

  # 证据状态。
  # EXTRACTED 表示从来源抽取。
  # INFERRED 表示由已有知识推断。
  # NEEDS_REVIEW 表示待复核。
  # UNVERIFIED 表示未验证。
  evidence_status_enum:
    - EXTRACTED
    - INFERRED
    - NEEDS_REVIEW
    - UNVERIFIED

  # 来源权威等级。
  # 这个等级用于区别官方、指南、教材、论文、现场笔记等来源可信度。
  authority_levels:
    - official
    - guideline
    - textbook
    - paper
    - field_note
    - unknown

  # 支持的来源类型。
  # 每个类型定义输入方式、raw 落库目录、适配器和依赖。
  source_types:
    markdown:
      source_label: Markdown file
      source_category: core_builtin
      input_mode: file
      raw_dir: raw/notes
      adapter_name: builtin
      dependency_name: ""
      extensions:
        - .md
        - .markdown
    text:
      source_label: Text file
      source_category: core_builtin
      input_mode: file
      raw_dir: raw/notes
      adapter_name: builtin
      dependency_name: ""
      extensions:
        - .txt
    html:
      source_label: HTML file
      source_category: core_builtin
      input_mode: file
      raw_dir: raw/html
      adapter_name: builtin
      dependency_name: ""
      extensions:
        - .html
        - .htm
    pdf:
      source_label: PDF file
      source_category: core_builtin
      input_mode: file
      raw_dir: raw/pdfs
      adapter_name: pypdf
      dependency_name: pypdf
      extensions:
        - .pdf
    url:
      source_label: Web URL
      source_category: manual_only
      input_mode: url
      raw_dir: raw/urls
      adapter_name: manual
      dependency_name: ""
      url_pattern: ^https?://
    plain_text:
      source_label: Plain text
      source_category: core_builtin
      input_mode: text
      raw_dir: raw/notes
      adapter_name: builtin
      dependency_name: ""
      extensions: []

  # 适配器状态枚举。
  # 用于说明某个来源导入器是否可用，或是否需要人工 fallback。
  adapter_states:
    - available
    - missing_dependency
    - manual_only
    - failed_retryable
    - failed_manual_fallback

# 维护策略。
# 这是限制 LLM 自动维护边界的核心部分。
maintenance:
  ingest_policy:
    # 必须先保存原始材料。
    raw_first: true

    # 必须先创建来源页，再更新事实。
    create_source_page_before_fact_update: true

    # 导入时只能写候选，不直接写正式事实。
    write_candidate_notes_only: true

    candidate_directory: issues

    # 禁止直接修改权威事实层。
    direct_authoritative_mutation_allowed: false

    # 每个导入来源都要写缓存，避免重复导入。
    cache_every_ingested_source: true

  # 权威来源自动发现策略。
  # LLM 可以找来源，但必须被系统验证。
  authority_discovery:
    supported: true
    llm_may_propose_sources: true
    llm_may_extract_candidate_facts: true

    # URL 必须经过白名单域名校验。
    allowlist_required: true

    # 如果要抽取事实，必须先抓取或保存来源内容。
    fetch_required_for_extraction: true

    # 自动发现只能进入候选层。
    candidate_only: true

    # 禁止 LLM 自动写入正式事实库。
    must_not_write_authoritative_facts: true

    # 被拒绝的来源不能落库。
    rejected_sources_are_not_landed: true

    # 被接受的来源必须有 source page 和 candidate record。
    accepted_sources_require_source_page: true
    accepted_sources_require_candidate_record: true

    # 当前允许的权威域名。
    allowed_domains:
      - moa.gov.cn
      - std.cahec.cn
      - openstd.samr.gov.cn
      - samr.gov.cn
      - woah.org
      - merckvetmanual.com
      - ema.europa.eu
      - fao.org

  # 批量导入策略。
  batch_ingest_policy:
    supported: true
    file_inputs_only: true
    continue_on_single_file_failure: true

  # 删除策略。
  # 默认 dry-run，是为了防止误删被正式事实引用的来源。
  delete_policy:
    supported: true
    dry_run_default: true
    scan_references_before_delete: true
    invalidate_cache_on_apply: true

  # 会话结晶策略。
  # crystallize 只能生成派生页，不能成为一手证据。
  crystallize_policy:
    supported: true
    output_directory: wiki/synthesis/sessions
    derived_only: true

  compatibility_policy:
    inspect_supported: true
    validate_supported: true
    ensure_source_dir_supported: true

  # 缓存结构。
  cache_schema:
    version_field: version
    updated_at_field: updated_at
    entries_field: entries
    entry_required_fields:
      - source_path
      - source_page
      - title
      - created_at
      - updated_at

  # 维护日志要求。
  change_log:
    file: log.md
    required_for:
      - init
      - source-create
      - ingest
      - digest-save
      - query-save

# 验证规则。
validation:
  # 普通 lint 的阻断项和警告项。
  normal_lint:
    blocks:
      - missing root files
      - missing index targets
      - invalid JSON exports
      - facts without evidence_status
    warns:
      - missing exports
      - broken wiki links
      - unresolved evidence source ids
      - NEEDS_REVIEW facts

  # 严格 lint 会阻断未复核和未验证事实。
  strict_lint:
    blocks:
      - NEEDS_REVIEW facts
      - UNVERIFIED facts
      - invalid cache entries
      - missing cache targets

  # 自动修复边界。
  # fix 可以创建目录和清理缓存，但不能编辑权威页面。
  fix_mode:
    may_create_missing_directories: true
    may_prune_invalid_cache_entries: true
    must_not_edit_authoritative_pages: true

  # schema-check 必须检查 schema 与代码契约是否一致。
  schema_check:
    must_match_code_contracts: true
    must_validate_current_wiki_root: true
    command: chicken-wiki schema-check --json

# 检索规则。
retrieval:
  query_sources:
    - markdown wiki pages
    - exports/knowledge_facts.json
    - disease_index.csv
    - rule_index.csv
    - drug_page_index.csv

  # query 返回必须具备这些字段。
  required_result_fields:
    - query
    - hits
    - fact_hits
    - wiki_dir

  # 生成上下文必须包含页面命中和事实命中，并引用 source id。
  generation_context:
    include_page_hits: true
    include_fact_hits: true
    cite_source_ids: true
    target_disease_query_must_include_disease_name: true

  # 派生回答策略。
  derived_answer_policy:
    derived_pages_must_set_derived_true: true
    derived_pages_are_not_primary_evidence: true
    save_locations:
      quick: wiki/synthesis
      report: wiki/synthesis
      comparison: wiki/comparisons
      query: wiki/queries

# 审计要求。
audit:
  # 最终 CSV 必须保留这些 Wiki 审计字段。
  output_csv_fields:
    - wiki_dir
    - wiki_fact_count
    - wiki_page_count
    - wiki_context_query
    - wiki_evidence_status_counts
    - wiki_evidence_source_ids
    - wiki_context_chars
    - target_disease_in_diagnosis
    - target_disease_mismatch
    - final_fatal_risk

  required_checks:
    - knowledge context was retrieved
    - evidence status counts were recorded
    - evidence source ids were recorded when available
    - target disease consistency was checked
    - final fatal risk merged rule and judge outcomes

  retention:
    generated_rows_keep_audit_columns: true
    source_pages_keep_original_source_path: true
    log_records_maintenance_events: true

# 图谱产物。
# 图谱是派生展示层，不是事实源。
graph:
  graph_data_path: wiki/graph-data.json
  graph_html_path: wiki/knowledge-graph.html
  graph_mermaid_path: wiki/knowledge-graph.md
  source_of_truth:
    - wiki pages
    - exports
  derived_only: true
  offline_renderable: true
```

## 4. 代码如何校验这个 Schema

项目中的校验代码位于：

`src/chicken_data_synthesis/infrastructure/knowledge/schema.py`

核心逻辑如下：

```python
def schema_check(
    wiki_dir: str | Path,
    *,
    schema_path: str | Path | None = None,
) -> LlmWikiSchemaCheckReport:
    """Validate the declarative Wiki operations schema against code and disk."""

    schema_file = Path(schema_path) if schema_path else DEFAULT_SCHEMA_PATH
    root = Path(wiki_dir)
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    # 1. schema 文件必须存在。
    if not schema_file.is_file():
        return LlmWikiSchemaCheckReport(
            schema_path=str(schema_file),
            wiki_dir=str(root),
            ok=False,
            declared_version="",
            errors=(f"schema_file_missing:{schema_file}",),
            warnings=(),
            checks=(),
        )

    # 2. 读取 YAML。
    schema = _load_yaml_mapping(schema_file)
    declared_version = str(schema.get("version") or "")

    # 3. 检查 schema 中声明的目录和代码常量是否完全一致。
    _check_exact_list(schema, "wiki_root.required_root_files", ROOT_MARKDOWN_FILES, errors, checks)
    _check_exact_list(schema, "wiki_root.required_directories", REQUIRED_DIRECTORIES, errors, checks)
    _check_exact_list(schema, "wiki_root.required_exports", REQUIRED_EXPORTS, errors, checks)

    # 4. 检查缓存文件名和版本。
    _check_value(schema, "wiki_root.cache_file", CACHE_FILE_NAME, errors, checks)
    _check_value(schema, "wiki_root.cache_version", CACHE_VERSION, errors, checks)

    # 5. 检查页面类型和 source frontmatter 字段。
    _check_mapping_keys(schema, "organization.page_types", PAGE_TYPES, errors, checks)
    _check_contains_list(
        schema,
        "source_contract.required_frontmatter_fields",
        SOURCE_FRONTMATTER_FIELDS,
        errors,
        checks,
    )

    # 6. 检查 source registry 中的来源类型是否都写入 schema。
    _check_mapping_keys(
        schema,
        "source_contract.source_types",
        tuple(item.source_id for item in list_source_types()),
        errors,
        checks,
    )

    # 7. 检查权威来源发现的安全约束。
    _check_exact_list(
        schema,
        "maintenance.authority_discovery.allowed_domains",
        AUTHORITY_ALLOWED_DOMAINS,
        errors,
        checks,
    )
    _check_value(schema, "maintenance.authority_discovery.llm_may_propose_sources", True, errors, checks)
    _check_value(schema, "maintenance.authority_discovery.allowlist_required", True, errors, checks)
    _check_value(schema, "maintenance.authority_discovery.candidate_only", True, errors, checks)
    _check_value(schema, "maintenance.authority_discovery.must_not_write_authoritative_facts", True, errors, checks)

    # 8. 检查审计字段是否包含代码要求的字段。
    _check_contains_list(schema, "audit.output_csv_fields", REQUIRED_AUDIT_FIELDS, errors, checks)

    # 9. 同时验证当前 Wiki 目录的 JSON 和严格检查项。
    for check in (*json_loadable_exports(root), *run_strict_checks(root, fix=False)):
        payload = check.to_dict()
        checks.append(payload)
        if check.severity == "error":
            errors.append(f"wiki:{check.code}:{check.path or check.message}")
        else:
            warnings.append(f"wiki:{check.code}:{check.path or check.message}")

    return LlmWikiSchemaCheckReport(
        schema_path=str(schema_file),
        wiki_dir=str(root),
        ok=not errors,
        declared_version=declared_version,
        errors=tuple(errors),
        warnings=tuple(warnings),
        checks=tuple(checks),
    )
```

这段代码说明 schema 不是摆设。它会真实检查：

- schema 声明的目录是否和代码一致。
- schema 声明的导出文件是否和代码一致。
- schema 声明的页面类型是否和代码一致。
- schema 声明的来源类型是否和 source registry 一致。
- 权威来源白名单是否和代码一致。
- LLM 自动发现是否仍保持候选层限制。
- 当前 Wiki 是否存在无效 JSON、未复核事实、无效缓存等问题。

## 5. 代码常量如何支撑 Schema

代码常量位于：

`src/chicken_data_synthesis/infrastructure/knowledge/contracts.py`

示例：

```python
CACHE_FILE_NAME = ".wiki-cache.json"
CACHE_VERSION = 1

ROOT_MARKDOWN_FILES = (
    "index.md",
    "purpose.md",
    ".wiki-schema.md",
    "log.md",
)

REQUIRED_EXPORTS = (
    "knowledge_facts.json",
    "disease_index.csv",
    "rule_index.csv",
    "drug_page_index.csv",
)

AUTHORITY_ALLOWED_DOMAINS = (
    "moa.gov.cn",
    "std.cahec.cn",
    "openstd.samr.gov.cn",
    "samr.gov.cn",
    "woah.org",
    "merckvetmanual.com",
    "ema.europa.eu",
    "fao.org",
)
```

设计理由：

- schema 是声明层，方便人读、LLM 读、文档展示。
- contracts.py 是代码运行层，方便程序引用。
- schema-check 把两者对齐，防止“文档说一套，代码跑一套”。

## 6. 每个模块的作用总结

| 模块 | 设计理由 | 作用 |
| --- | --- | --- |
| `scope` | 明确边界 | 防止 schema 管错对象 |
| `wiki_root` | 固定文件结构 | 保证知识库可初始化、可检查、可迁移 |
| `organization` | 区分权威页和派生页 | 防止 LLM 派生内容冒充权威证据 |
| `source_contract` | 来源可追溯 | 每条知识能追到 source、raw 和 evidence status |
| `source_types` | 统一导入入口 | 支持 md/txt/html/pdf/url/plain_text |
| `maintenance.ingest_policy` | raw first、candidate first | 防止导入时直接污染正式事实库 |
| `authority_discovery` | LLM 自动发现的安全边界 | 允许自动找来源，但必须白名单和候选落库 |
| `validation` | 自动健康检查 | 阻断未复核事实、断链、无效缓存 |
| `retrieval` | 约束 LLM 上下文来源 | 防止 LLM 脱离 Wiki 证据回答 |
| `audit` | 记录知识使用痕迹 | 支撑最终生成/评估结果可追溯 |
| `graph` | 图谱派生展示 | 展示知识覆盖和证据关系，但不作为事实源 |

## 7. 为什么它对 LLM Wiki 很重要

没有这个 schema，LLM Wiki 容易变成“LLM 写 Markdown 的文件夹”。有了它，LLM Wiki 才能成为受控知识系统：

- LLM 可以自动找资料，但必须过来源白名单。
- LLM 可以抽取事实，但只能先进入候选层。
- 正式事实必须有来源和证据状态。
- 检索上下文必须来自 Wiki 和 facts。
- 图谱只是展示层，不能反向作为权威事实。
- 生成/评估结果必须保留 Wiki 审计字段。

这正是鸡病系统需要的能力：既使用 LLM 自动化，又不牺牲权威性、真实性和可追溯性。

## 8. 推荐演示方式

可以用以下命令展示 schema 的作用：

```powershell
cd D:\XF-ChongQin\ai-
$env:PYTHONPATH='src;.'

# 检查 schema 与代码契约、当前 Wiki 状态是否一致
python -m chicken_data_synthesis.wiki_cli --json schema-check

# 检查 Wiki 健康状态
python -m chicken_data_synthesis.wiki_cli --json lint --strict

# 展示权威来源自动发现仍受 schema 约束
python -m chicken_data_synthesis.wiki_cli --json authority-discover "新城疫 诊断标准" --url "https://www.moa.gov.cn/demo.html" --url "https://example.com/demo.html"

# 重建图谱，证明 schema 约束下的正式事实和来源可展示
python -m chicken_data_synthesis.wiki_cli --json graph-build
```

演示重点：

- `schema-check` 证明 schema 和代码一致。
- `authority-discover` 证明 LLM 或用户提交的 URL 必须白名单校验。
- 非权威域名会被拒绝。
- 接受来源只进入 source/candidate，不直接进入正式事实。
- `graph-build` 证明正式事实和来源最终可以被可视化追溯。

