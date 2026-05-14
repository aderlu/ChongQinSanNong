# 鸡病系统 LLM Wiki 分阶段演示与工作汇报指南

更新时间：2026-05-05

本文档用于现场演示和工作汇报。结构严格按 LLM Wiki 的维护链路组织，所有内容都归入对应阶段，避免“命令、代码依据、定时任务、图谱、审计”散落在不同地方。

整体链路如下：

```text
演示准备
  -> 阶段 1：真实知识需求
  -> 阶段 2：LLM 使用 web access 搜索权威来源，并只输出候选 URL
  -> 阶段 3：authority-discover 校验权威域名白名单
  -> 阶段 4：通过校验的来源进入 raw/ 与 wiki/sources/
  -> 阶段 5：生成候选事实 knowledge_facts.candidates.json
  -> 阶段 6：复核后进入正式事实 knowledge_facts.json
  -> 阶段 7：query 构建 LLM 检索上下文
  -> 阶段 8：graph-build 重建 graph-data.json 与 knowledge-graph.html
  -> 阶段 9：生成/评估流程记录 Wiki 审计字段
```

核心汇报结论：

```text
LLM 可以自动发现候选来源；
LLM 不能直接写正式事实；
系统通过白名单、schema、候选层、复核、图谱和审计字段保证可追溯。
```

## 演示准备：确认项目、环境、状态

### 演示目标

先证明当前项目里确实存在一个可运行的 LLM Wiki，而不是只停留在文档描述。

### 执行命令

```powershell
cd D:\XF-ChongQin\ai-
$env:PYTHONPATH='src;.'

python -m chicken_data_synthesis.wiki_cli --json status
```

如果不设置 `PYTHONPATH`，会出现：

```text
ModuleNotFoundError: No module named 'chicken_data_synthesis'
```

原因是 CLI 入口位于：

```text
src/chicken_data_synthesis/wiki_cli.py
```

### 当前真实状态摘要

```json
{
  "wiki_dir": "D:\\XF-ChongQin\\ai-\\knowledge\\llm_wiki_chicken_authoritative",
  "purpose_exists": true,
  "schema_exists": true,
  "graph_data_exists": true,
  "graph_html_exists": true,
  "raw_file_count": 124,
  "fact_count": 1748,
  "disease_count": 60,
  "drug_count": 115,
  "rule_count": 30,
  "evidence_status_counts": {
    "EXTRACTED": 1633,
    "INFERRED": 115
  }
}
```

### 字段解释

`purpose_exists`：是否存在 Wiki 用途说明文件。

```text
knowledge/llm_wiki_chicken_authoritative/purpose.md
```

`schema_exists`：是否存在 Wiki 包内部 schema 说明文件。

```text
knowledge/llm_wiki_chicken_authoritative/.wiki-schema.md
```

注意：完整机器约束 schema 是另一个文件：

```text
knowledge/schemas/llm_wiki_schema.yaml
```

`raw_file_count`：`raw/` 目录中的原始证据文件数量，包括 URL 记录、HTML、PDF、文本等。

`section_counts`：`wiki/` 目录下各类 Markdown 页面数量，例如 diseases、drugs、rules、sources。

区别如下：

```text
raw_file_count = 原始材料数量
section_counts = Wiki 页面数量
fact_count = 正式结构化事实数量
```

`fact_count`：正式事实库中的事实数量，来源文件是：

```text
knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.json
```

`evidence_status_counts`：正式事实按证据状态统计。例如：

- `EXTRACTED`：从来源中抽取或整理出的事实。
- `INFERRED`：基于已有知识归纳出的事实，可信边界低于直接抽取事实。
- `NEEDS_REVIEW`：待复核事实，原则上只应停留在候选层。

### 代码依据

- `src/chicken_data_synthesis/wiki_cli.py`
  - CLI 模块入口。
- `src/chicken_data_synthesis/interfaces/cli/wiki.py`
  - 注册 `status`、`daily-maintain`、`authority-discover`、`query`、`graph-build` 等命令。
- `src/chicken_data_synthesis/infrastructure/knowledge/operations.py`
  - `build_status_report()` 生成上述状态字段。
- `src/chicken_data_synthesis/infrastructure/knowledge/wiki.py`
  - `resolve_llm_wiki_dir()` 解析默认 Wiki 路径。

### 汇报口径

> 演示前先跑 status，是为了证明当前 Wiki 包真实存在，并且已经有 raw 原始证据、Wiki 页面、正式事实、图谱数据和 HTML 页面。后续每一步都是在这个真实 Wiki 包上运行。

## 阶段 1：真实知识需求

### 演示目标

说明 LLM Wiki 的维护不是无目的地让模型补知识，而是由真实业务问题触发。

示例需求：

```text
新城疫诊断标准是否有权威来源？
当前知识库中是否已有国家标准或 WOAH 手册依据？
如果没有，是否需要让 LLM 搜索新的权威来源？
```

### 执行命令

```powershell
python -m chicken_data_synthesis.wiki_cli --json query "新城疫 WOAH 诊断 标准 实验室" --top-k 3
```

### 当前真实返回示例

`fact_hits` 中可以看到：

```json
[
  {
    "fact_id": "SRC-0012-standard-number",
    "fact_type": "diagnosis_standard",
    "subject": "GB/T 16550-2020 新城疫诊断技术",
    "predicate": "standard_no",
    "object": "GB/T 16550-2020",
    "evidence_source_id": "SRC-0012",
    "evidence_url": "https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=DAA58A6FCC696F91339EED5BF8460CAB",
    "evidence_status": "EXTRACTED",
    "jurisdiction": "CN"
  },
  {
    "fact_id": "DIS-009-diagnosis-standard-anchor",
    "subject": "新城疫",
    "predicate": "diagnosis_standard_anchor",
    "object": "WOAH Terrestrial Manual chapter 3.3.14 Newcastle disease",
    "evidence_source_id": "SRC-0066",
    "evidence_url": "https://www.woah.org/fileadmin/Home/eng/Health_standards/tahm/3.03.14_NEWCASTLE_DIS.pdf",
    "evidence_status": "EXTRACTED",
    "jurisdiction": "WOAH"
  }
]
```

### 过程说明

```text
真实知识问题
  -> query 检索 Wiki 页面
  -> query 检索正式结构化事实
  -> 返回 hits、fact_hits、context
  -> 判断是否需要补充新来源
```

### 代码和数据依据

- `src/chicken_data_synthesis/infrastructure/knowledge/operations.py`
  - `query_wiki()`
- `src/chicken_data_synthesis/infrastructure/knowledge/wiki.py`
  - `build_llm_wiki_context()`
  - `LlmWikiKnowledgeBase.search()`
  - `LlmWikiKnowledgeBase.search_facts()`
- `knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.json`
- `knowledge/llm_wiki_chicken_authoritative/wiki/diseases/DIS-009-新城疫.md`

### 为什么这样做

先 query 的原因是：自动维护前必须判断知识库是否已经有答案。已有权威事实时，不需要重复引入来源；缺少来源或事实时，才进入下一阶段的 LLM 搜索。

### 可验证点

Leader 追问“你怎么知道已有权威来源？”时，可以回答：

> query 返回的结构化事实里有 `evidence_source_id` 和 `evidence_url`。例如新城疫诊断标准对应 `SRC-0012`，URL 是国家标准公开系统；WOAH 诊断锚点对应 `SRC-0066`，URL 是 WOAH 手册 PDF。这些不是 LLM 编写的，而是正式事实库中的结构化事实。

## 阶段 2：LLM 使用 web access 搜索权威来源，并只输出候选 URL

### 演示目标

展示 LLM 可以自动发现新来源，但不能直接输出或落库正式事实。

### 当前实现方式

项目已经新增自动维护入口，接入三方 LLM 平台，并通过 Windows 计划任务设置为每周维护一次：

```text
Base URL: https://api.nonelinear.com/v1
Model: gpt-5.4-mini-medium
API key 环境变量: NONELINEAR_API_KEY
```

相关代码：

- `src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py`
  - `NonelinearAuthorityClient`
  - `run_daily_maintenance()`
- `src/chicken_data_synthesis/interfaces/cli/wiki.py`
  - `daily-maintain` 子命令。

### API key 配置

API key 不能写入代码、文档正文或日志，只能通过环境变量读取：

```powershell
setx NONELINEAR_API_KEY "你的 API key"
```

当前 PowerShell 会话临时配置：

```powershell
$env:NONELINEAR_API_KEY="你的 API key"
```

### 手动执行一次 LLM 自动维护

```powershell
python -m chicken_data_synthesis.wiki_cli --json daily-maintain `
  --base-url "https://api.nonelinear.com/v1" `
  --model "gpt-5.4-mini-medium"
```

也可以指定知识需求：

```powershell
python -m chicken_data_synthesis.wiki_cli --json daily-maintain `
  --base-url "https://api.nonelinear.com/v1" `
  --model "gpt-5.4-mini-medium" `
  --query "新城疫 诊断标准 实验室确诊 权威来源" `
  --query "蛋鸡 兽药 禁用 休药期 农业农村部 权威来源"
```

### 注册每周维护一次

项目提供 Windows 任务计划注册脚本：

```powershell
.\scripts\register_llm_wiki_weekly_task.ps1 -DayOfWeek "Monday" -At "03:00"
```

默认任务名：

```text
ChickenDiseaseLLMWikiWeeklyMaintenance
```

每周执行脚本：

```text
scripts/run_llm_wiki_weekly_maintenance.ps1
```

维护日志输出：

```text
results/llm_wiki_maintenance/weekly-maintain-*.json
```

### LLM 的受控提示词逻辑

代码中由 `_build_authority_messages()` 构建提示词，核心要求是：

```text
1. 只允许在白名单域名中找来源。
2. 只输出候选 URL JSON。
3. 不输出正式事实。
4. 不总结诊断标准。
5. 不给用药建议。
```

输出 JSON 结构：

```json
{
  "sources": [
    {
      "url": "https://...",
      "title": "来源标题",
      "reason": "为什么这个来源可能有用",
      "evidence_role": "diagnosis_standard | regulation | clinical_reference | drug_rule"
    }
  ]
}
```

### 权威域名白名单

```text
moa.gov.cn
std.cahec.cn
openstd.samr.gov.cn
samr.gov.cn
woah.org
merckvetmanual.com
ema.europa.eu
fao.org
```

代码和 schema 依据：

- `src/chicken_data_synthesis/infrastructure/knowledge/contracts.py`
  - `AUTHORITY_ALLOWED_DOMAINS`
- `knowledge/schemas/llm_wiki_schema.yaml`
  - `maintenance.authority_discovery.allowed_domains`

### 为什么 LLM 只能输出候选 URL

原因：

- 搜索结果可能过期、重复或来自转载页面。
- LLM 可能误读网页内容。
- 鸡病诊断、兽药使用、监管边界属于高风险知识。
- schema 明确要求 `candidate_only: true`。
- schema 明确要求 `must_not_write_authoritative_facts: true`。

schema 依据：

```yaml
maintenance:
  authority_discovery:
    llm_may_propose_sources: true
    llm_may_extract_candidate_facts: true
    candidate_only: true
    must_not_write_authoritative_facts: true
```

### 汇报口径

> 当前已经不是每次都必须人工手写提示词。项目新增了 `daily-maintain` 作为“执行一次维护”的 CLI 入口，并通过 `register_llm_wiki_weekly_task.ps1` 注册为每周自动运行一次。它会调用 Nonelinear 的 `gpt-5.4-mini-medium`，使用代码内置的受控提示词，让 LLM 自动发现候选权威 URL。但自动化只到候选来源层，LLM 不能直接写正式事实。

## 阶段 3：authority-discover 校验权威域名白名单

### 演示目标

证明系统不会无条件相信 LLM 输出的 URL，而是通过白名单校验。

### 执行方式一：接收 LLM 自动维护结果

`daily-maintain` 内部会自动调用：

```text
run_daily_maintenance()
  -> NonelinearAuthorityClient.suggest_sources()
  -> discover_authority_sources()
```

### 执行方式二：手动传入候选 URL

```powershell
python -m chicken_data_synthesis.wiki_cli --json authority-discover `
  "新城疫诊断标准权威来源" `
  --url "https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=DAA58A6FCC696F91339EED5BF8460CAB" `
  --url "https://www.woah.org/fileadmin/Home/eng/Health_standards/tahm/3.03.14_NEWCASTLE_DIS.pdf"
```

### 执行方式三：传入 LLM JSON 文件

```powershell
python -m chicken_data_synthesis.wiki_cli --json authority-discover `
  "新城疫诊断标准权威来源" `
  --llm-suggestions-file .\llm_sources_newcastle.json
```

### 过程说明

```text
候选 URL JSON
  -> _parse_llm_suggestions()
  -> _dedupe_candidates()
  -> is_authoritative_url()
  -> authority_level_for_url()
  -> accepted 或 rejected
```

### 代码依据

- `src/chicken_data_synthesis/interfaces/cli/wiki.py`
  - `authority-discover`
  - `daily-maintain`
- `src/chicken_data_synthesis/infrastructure/knowledge/authority.py`
  - `discover_authority_sources()`
  - `is_authoritative_url()`
  - `authority_level_for_url()`
- `src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py`
  - `run_daily_maintenance()`

### 为什么这样做

这一步是自动化与真实性之间的边界：

```text
LLM 提出 URL
  -> 系统校验 URL
  -> 非白名单拒绝
  -> 白名单通过但仍然只是候选来源
```

### 可验证点

维护报告中重点看：

```text
accepted_count
rejected_count
rejected_candidates
authority_reports
```

如果某个 URL 不在白名单，应出现在 `rejected_candidates`，原因通常为：

```text
domain_not_allowlisted
```

### 汇报口径

> authority-discover 是 LLM Wiki 的安全闸门。LLM 可以发现 URL，但系统必须用代码白名单和 schema 白名单校验。只有通过白名单的来源才能进入 raw 和 source page。

## 阶段 4：通过校验的来源进入 raw/ 与 wiki/sources/

### 演示目标

展示通过白名单的来源如何落到可追溯的文件结构中。

### 落库位置

如果不加 `--fetch`，只记录 URL：

```text
knowledge/llm_wiki_chicken_authoritative/raw/urls/
```

如果加 `--fetch`，抓取网页或 PDF：

```text
knowledge/llm_wiki_chicken_authoritative/raw/html/
knowledge/llm_wiki_chicken_authoritative/raw/pdfs/
```

来源页保存到：

```text
knowledge/llm_wiki_chicken_authoritative/wiki/sources/
```

### 当前真实来源页示例

```text
knowledge/llm_wiki_chicken_authoritative/wiki/sources/SRC-0122-demo-newcastle-layer-note.md
```

内容摘要：

```yaml
---
type: source
source_id: SRC-0122
source_path: raw/notes/demo-newcastle-layer-note.txt
source_type: plain_text
authority_level: unclassified
evidence_status: NEEDS_REVIEW
created: 2026-05-05
updated: 2026-05-05
sources: []
---
```

### 过程说明

```text
accepted URL
  -> _materialize_candidate()
  -> raw/urls 或 raw/html/raw/pdfs
  -> create_source_page()
  -> wiki/sources/SRC-xxxx.md
  -> cache_update()
  -> log.md
```

### 代码依据

- `src/chicken_data_synthesis/infrastructure/knowledge/authority.py`
  - `_materialize_candidate()`
- `src/chicken_data_synthesis/infrastructure/knowledge/ingest.py`
  - `create_source_page()`
- `src/chicken_data_synthesis/infrastructure/knowledge/rendering.py`
  - `render_source_page()`
- `src/chicken_data_synthesis/infrastructure/knowledge/cache.py`
  - `cache_update()`

### 为什么这样做

`raw/` 和 `wiki/sources/` 分层的原因：

- `raw/` 保留原始证据。
- `wiki/sources/` 提供可读来源页。
- 事实可以稳定引用 `SRC-xxxx`。
- 删除或更新来源时可以检查引用。

### 汇报口径

> 来源落库不是直接变成事实，而是先形成 raw 原始证据和 source page。source page 是后续事实追溯的锚点。

## 阶段 5：生成候选事实 knowledge_facts.candidates.json

### 演示目标

展示自动维护产生的新增来源会进入候选事实层，而不是正式事实层。

候选事实文件：

```text
knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.candidates.json
```

### 当前真实候选事实

```json
{
  "fact_id": "CAND-0001",
  "subject": "demo-newcastle-layer-note",
  "predicate": "source_imported",
  "object": "pending_review",
  "evidence_source_id": "SRC-0122",
  "source_page": "wiki/sources/SRC-0122-demo-newcastle-layer-note.md",
  "evidence_status": "NEEDS_REVIEW"
}
```

### 执行验证

```powershell
Get-Content .\knowledge\llm_wiki_chicken_authoritative\exports\knowledge_facts.candidates.json
```

也可以通过图谱元数据验证：

```json
{
  "candidate_facts": 1,
  "candidate_facts_in_graph": 1
}
```

### 过程说明

```text
source page 创建完成
  -> write_candidate_facts()
  -> 追加 CAND-xxxx
  -> evidence_status=NEEDS_REVIEW
```

### 代码依据

- `src/chicken_data_synthesis/infrastructure/knowledge/ingest.py`
  - `write_candidate_facts()`
- `src/chicken_data_synthesis/infrastructure/knowledge/authority.py`
  - `discover_authority_sources()`
- `src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py`
  - `run_daily_maintenance()`

### 为什么这样做

候选事实只表达：

```text
有一个来源被发现并导入，等待复核。
```

它不表达：

```text
该来源中的诊断、用药、监管事实已经被确认。
```

### 汇报口径

> candidates 文件是 LLM Wiki 的安全缓冲区。每周自动维护产生的结果先进入这里，只有复核后才可能进入正式 facts。

## 阶段 6：复核后进入正式事实 knowledge_facts.json

### 演示目标

说明正式事实库是生成、评估、图谱的权威数据层，不能由 LLM 直接写入。

正式事实文件：

```text
knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.json
```

### 当前真实规模

```json
{
  "fact_count": 1748,
  "evidence_status_counts": {
    "EXTRACTED": 1633,
    "INFERRED": 115
  }
}
```

来源覆盖率：

```json
{
  "source_page_count": 123,
  "fact_count": 1748,
  "facts_with_source_count": 1608,
  "unresolved_source_count": 0,
  "page_source_signal_summary": {
    "applicable_total": 215,
    "ok": 215,
    "missing_sources": 0,
    "empty_sources": 0,
    "invalid_sources": 0
  }
}
```

### 复核检查项

候选事实进入正式事实前，需要检查：

- URL 是否在白名单。
- source page 是否存在。
- 原始证据是否可追溯。
- `evidence_status` 是否允许进入正式层。
- `subject/predicate/object` 是否符合鸡病领域语义。
- 物种、阶段、司法辖区、休药期、禁用信息是否明确。
- 诊断、用药、监管结论是否有来源支撑。

### schema 校验

```powershell
python -m chicken_data_synthesis.wiki_cli --json schema-check
```

当前真实结果：

```json
{
  "schema_path": "D:\\XF-ChongQin\\ai-\\knowledge\\schemas\\llm_wiki_schema.yaml",
  "ok": true,
  "declared_version": "1.0.0",
  "errors": [],
  "warnings": []
}
```

### 代码依据

- `knowledge/schemas/llm_wiki_schema.yaml`
- `src/chicken_data_synthesis/infrastructure/knowledge/schema.py`
  - `schema_check()`
- `src/chicken_data_synthesis/infrastructure/knowledge/wiki.py`
  - `load_llm_wiki()`
  - `_load_json_array()`

### 为什么这样做

如果 LLM 可以直接写正式事实，就无法保证真实性，也无法解释每条事实的来源和复核状态。

### 汇报口径

> LLM Wiki 自动化维护不是自动写正式 facts，而是自动发现候选、自动准备复核材料。正式事实仍然需要经过来源和语义复核。

## 阶段 7：query 构建 LLM 检索上下文

### 演示目标

展示生成或评估时，系统不是让 LLM 自由发挥，而是先从 Wiki 构建上下文。

### 执行命令

```powershell
python -m chicken_data_synthesis.wiki_cli --json query "新城疫 WOAH 诊断 标准 实验室" --top-k 3
```

### 返回字段

```json
{
  "query": "...",
  "context": "...",
  "wiki_dir": "...",
  "hits": [],
  "fact_hits": []
}
```

其中：

- `hits`：相关 Wiki 页面。
- `fact_hits`：正式结构化事实。
- `context`：给 LLM 的最终检索上下文。

### 当前真实 context 摘要

```text
LLM Wiki 知识上下文（用于生成与评估，不能编造未被上下文支持的监管/用药结论）：
相关 Wiki 页：
1. [diseases] 新城疫 ...
相关结构化事实：
1. GB/T 16550-2020 新城疫诊断技术 | standard_no | GB/T 16550-2020 | source=SRC-0012 | status=EXTRACTED
2. 新城疫 | diagnosis_standard_anchor | WOAH Terrestrial Manual chapter 3.3.14 Newcastle disease | source=SRC-0066 | status=EXTRACTED
```

### 代码依据

- `src/chicken_data_synthesis/infrastructure/knowledge/operations.py`
  - `query_wiki()`
- `src/chicken_data_synthesis/infrastructure/knowledge/wiki.py`
  - `build_llm_wiki_context()`
  - `LlmWikiKnowledgeBase.search()`
  - `LlmWikiKnowledgeBase.search_facts()`

### 为什么这样做

query 的作用：

- 限制 LLM 只能基于检索到的 Wiki 上下文输出。
- 同时提供页面证据和结构化事实。
- 把 source id 和 evidence status 带入后续审计。

### 汇报口径

> query 是生成和评估前的上下文构建器。它返回的 context 明确要求不能编造未被上下文支持的监管或用药结论，并把 source 和 status 带给 LLM。

## 阶段 8：graph-build 重建 graph-data.json 与 knowledge-graph.html

### 演示目标

展示知识库发生新增、修改、删除后，图谱数据和 HTML 页面会跟随重建。

### 执行命令

```powershell
python -m chicken_data_synthesis.wiki_cli --json graph-build
```

生成或更新：

```text
knowledge/llm_wiki_chicken_authoritative/wiki/graph-data.json
knowledge/llm_wiki_chicken_authoritative/wiki/knowledge-graph.md
knowledge/llm_wiki_chicken_authoritative/wiki/knowledge-graph.html
```

每周维护也会自动执行图谱重建：

```text
daily-maintain
  -> run_daily_maintenance()
  -> rebuild_graph()
```

### 当前真实图谱元数据

```json
{
  "generated_at": "2026-05-05T00:42:56",
  "diseases": 60,
  "drugs": 115,
  "rules": 30,
  "sources": 126,
  "facts": 1748,
  "candidate_facts": 1,
  "facts_in_graph": 1748,
  "facts_not_in_graph": 0,
  "candidate_facts_in_graph": 1,
  "node_groups": {
    "candidate": 2,
    "concept": 1024,
    "disease": 60,
    "drug": 115,
    "rule": 41,
    "source": 126,
    "standard": 18
  }
}
```

### 节点类型解释

- `Disease`：疾病实体，例如新城疫、禽流感。
- `Drug`：药品或药物规则对象。
- `Standard`：国家标准、行业标准、WOAH 手册章节等标准锚点。
- `Rule`：监管规则、禁用规则、休药期规则、公告规则。
- `Source`：来源页，对应 `SRC-xxxx`。
- `Concept`：症状、剖检变化、传播途径、诊断方法等概念节点。
- `Candidate`：候选事实或候选来源，表示待复核内容。

### HTML 为什么会变化

```text
信息新增/修改/删除
  -> Wiki 页面或 exports 文件发生变化
  -> graph-build 重新加载 Wiki 和 facts
  -> 重新生成 graph-data.json
  -> knowledge-graph.html 读取新图谱数据
```

### 代码依据

- `src/chicken_data_synthesis/infrastructure/knowledge/graph.py`
  - `build_graph_data()`
  - `rebuild_graph()`
  - `render_graph_html()`
  - `_add_fact_to_graph()`
- `src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py`
  - `run_daily_maintenance()` 调用 `rebuild_graph()`。

### 可验证点

当前正式事实全量入图：

```text
facts: 1748
facts_in_graph: 1748
facts_not_in_graph: 0
```

候选事实也进入图谱展示：

```text
candidate_facts: 1
candidate_facts_in_graph: 1
```

### 关于 Disease 为什么不直接大量连接 Drug

原因：

```text
Disease -> 诊断、症状、病原、传播、标准、来源
Drug -> 监管规则、禁用、休药期、适用阶段、来源
```

药品在本系统中首先是合规对象，不应简单表达成“某疾病推荐某药”。直接建立大量 Disease-Drug 关系，可能让 LLM 误以为某病可以用某药治疗，存在安全风险。

### 汇报口径

> 图谱不是把疾病和药品粗暴相连，而是把疾病知识、药品合规、监管规则和来源证据分层表达。这样既能展示知识覆盖，也能避免错误用药暗示。

## 阶段 9：生成/评估流程记录 Wiki 审计字段

### 演示目标

展示 LLM Wiki 不只服务于文档和图谱，还会进入生成/评估结果的审计字段。

### 审计字段

schema 要求 CSV 输出字段包括：

```yaml
audit:
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
```

### 审计过程

```text
生成/评估任务开始
  -> query 构建 Wiki context
  -> LLM 基于 context 生成或评估
  -> build_wiki_audit_metadata() 统计 context 中出现的 SRC-xxxx 和 status
  -> compact_wiki_audit_for_csv() 展平成 CSV 字段
  -> 输出结果保留 Wiki 使用痕迹
```

### 代码依据

- `src/chicken_data_synthesis/infrastructure/knowledge/audit.py`
  - `build_wiki_audit_metadata()`
  - `compact_wiki_audit_for_csv()`
- `src/chicken_data_synthesis/infrastructure/persistence/csv_artifacts.py`
  - 写入 `wiki_fact_count`
  - 写入 `wiki_page_count`
  - 写入 `wiki_evidence_status_counts`
  - 写入 `wiki_evidence_source_ids`
  - 写入 `wiki_context_chars`
- `llm_foundation/tools.py`
  - 规则检查工具可携带 Wiki 审计结果。

### 为什么这样做

没有审计字段，就无法回答：

- 用了哪个 Wiki？
- 当时 Wiki 有多少事实？
- 本次上下文包含哪些 source？
- 证据状态是什么？
- LLM 是否引用了足够上下文？

### 可验证命令

```powershell
Get-Content .\src\chicken_data_synthesis\infrastructure\knowledge\audit.py
Get-Content .\src\chicken_data_synthesis\infrastructure\persistence\csv_artifacts.py
```

### 汇报口径

> LLM Wiki 的有效性不仅体现在 HTML 图谱，还体现在生成/评估结果的可追溯性。审计字段会把 Wiki 使用情况写入 CSV，后续可以复查每一次生成或评估依赖了哪些 source 和 evidence status。

## 最终汇报结论

可以直接使用下面这段作为工作汇报总结：

> 当前鸡病系统的 LLM Wiki 已经围绕鸡病合成与评估系统完成适配。系统以真实知识需求为触发点，允许 LLM 通过 Nonelinear `gpt-5.4-mini-medium` 和 web access 能力自动搜索权威来源，但 LLM 只能输出候选 URL。系统通过 `authority-discover` 使用代码白名单和 schema 白名单校验来源，通过的来源进入 `raw/` 和 `wiki/sources/`，并生成 `knowledge_facts.candidates.json` 候选事实。候选事实经过复核后才能进入正式 `knowledge_facts.json`。生成和评估时，`query` 构建 LLM 检索上下文，`graph-build` 重建 `graph-data.json` 和 `knowledge-graph.html`，最终生成/评估流程记录 Wiki 审计字段，保证结果可追溯。

当前真实状态：

```text
Wiki 路径: knowledge/llm_wiki_chicken_authoritative
raw 文件: 124
疾病: 60
药品: 115
规则: 30
来源页: 123
正式事实: 1748
正式事实入图: 1748
未入图正式事实: 0
候选事实: 1
schema-check: ok=true
coverage unresolved_source_count: 0
```

最终一句话：

```text
LLM Wiki 的价值不是让 LLM 无约束生成知识，
而是把 LLM 的发现能力限制在候选来源和候选事实层，
再通过白名单、schema、复核、query、graph-build 和 audit
形成可执行、可追问、可验证、可追溯的知识库维护闭环。
```
