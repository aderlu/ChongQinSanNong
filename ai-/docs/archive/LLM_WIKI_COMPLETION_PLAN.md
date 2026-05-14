# 鸡病系统 LLM Wiki 能力补完计划

## 目标与边界

本文档用于指导现有鸡病生成与评估系统补齐 `llm-wiki-skill-main` 的核心知识库生命周期能力。当前系统已经可以把 `knowledge/llm_wiki_chicken_authoritative` 作为生成、评估、仲裁和规则拦截的知识底座使用；本计划聚焦“如何把静态知识包升级成可持续维护、可消化新增资料、可审计、可回归验证的知识库系统”。

本计划明确不包含图片、附件、截图、图像下载、图片页面追踪等功能。

## 当前状态

已经实现：

- `LLM Wiki` 检索适配层：加载 `wiki/**/*.md`、`index.md`、`purpose.md`、`.wiki-schema.md`。
- 结构化事实加载：读取 `exports/knowledge_facts.json`、`disease_index.csv`、`rule_index.csv`、`drug_page_index.csv`。
- 生成链路接入：单阶段生成、问诊草稿、盲补全阶段会注入 Wiki 上下文。
- 评估链路接入：双裁判和仲裁提示词会注入 Wiki 上下文。
- 规则底座接入：可以从 Wiki 证据中识别禁用/限制药物、待复核事实等风险。
- 维护 CLI 雏形：`status`、`lint`、`context`、`query`、`query-save`、`step1-validate`、`graph-build`、`graph-watch`。
- 基础图谱构建：可以生成 `wiki/graph-data.json` 和 `wiki/knowledge-graph.html`。

未完整实现：

- 初始化工作流。
- 素材消化和批量消化工作流。
- 来源注册、来源适配器状态和失败分类。
- 缓存、去重和 source 页关联机制。
- 深度综合报告。
- 级联删除和维护。
- 完整 lint 和 source signal coverage。
- 完整离线交互式图谱体验。
- SessionStart 自动上下文注入。
- 对话结晶化。
- 通用页面类型和索引体系。

## 总体架构

建议保留当前鸡病领域定制结构，同时引入 `llm-wiki-skill-main` 的生命周期能力。不要把外部 skill 脚本直接作为运行时硬依赖，而是把稳定契约迁移到 Python 模块中，必要时保留 shell 脚本兼容层。

目标目录结构：

```text
knowledge/llm_wiki_chicken_authoritative/
├─ raw/
├─ wiki/
│  ├─ diseases/
│  ├─ drugs/
│  ├─ rules/
│  ├─ rule_cards/
│  ├─ sources/
│  ├─ topics/
│  ├─ syndromes/
│  ├─ synthesis/
│  ├─ comparisons/
│  ├─ sessions/
│  └─ queries/
├─ exports/
├─ issues/
├─ index.md
├─ purpose.md
├─ log.md
├─ .wiki-schema.md
└─ .wiki-cache.json
```

新增代码建议：

```text
src/chicken_data_synthesis/infrastructure/knowledge/
├─ cache.py
├─ contracts.py
├─ deletion.py
├─ digest.py
├─ graph.py
├─ ingest.py
├─ linting.py
├─ registry.py
├─ rendering.py
├─ session_context.py
├─ wiki.py
└─ operations.py

src/chicken_data_synthesis/interfaces/cli/wiki.py
```

## 实施阶段

### 阶段 0：冻结契约与基线

目标：先把当前能工作的行为固化，避免后续补功能时破坏生成和评估主链路。

任务：

- 为当前 Wiki 包生成基线报告，记录页面数、事实数、疾病数、药物数、规则数、图谱节点数。
- 增加测试 fixture，覆盖当前鸡病 Wiki 的最小真实子集。
- 固化 CLI 参数顺序规范：全局参数必须位于子命令前，例如 `chicken-wiki --json status`。
- 在文档中明确 `pip install -e .` 或 `PYTHONPATH=src;.` 的本地运行方式。
- 把现有 `lint_wiki` 的输出作为基础健康检查契约。

验收标准：

- `python -m pytest -q` 通过。
- `chicken-wiki --json status` 返回稳定字段。
- `chicken-wiki --json lint` 对当前知识包返回 `ok: true`。
- 主流程 `python main.py --help` 正常。

### 阶段 1：初始化工作流

目标：提供可重复创建标准 Wiki 包的入口，而不是依赖手工拷贝目录。

新增命令：

```bash
chicken-wiki init --wiki-dir knowledge/llm_wiki_chicken_authoritative --domain chicken_disease
chicken-wiki init --force-template-sync
```

实现方案：

- 新增 `contracts.py` 定义必需路径、页面类型、导出文件名和 frontmatter 字段。
- 新增 `rendering.py` 保存模板渲染逻辑，优先使用项目内 Python 模板，避免运行 shell 脚本。
- 初始化时创建 `raw/`、`wiki/sources/`、`wiki/topics/`、`wiki/synthesis/`、`wiki/queries/`、`exports/`、`issues/`。
- 如果 `index.md`、`purpose.md`、`.wiki-schema.md`、`log.md` 不存在，则创建；存在则默认不覆盖。
- 创建 `.wiki-cache.json`，格式包含 `version`、`entries`、`updated_at`。

建议文件：

- `src/chicken_data_synthesis/infrastructure/knowledge/contracts.py`
- `src/chicken_data_synthesis/infrastructure/knowledge/rendering.py`
- `src/chicken_data_synthesis/infrastructure/knowledge/operations.py`
- `src/chicken_data_synthesis/interfaces/cli/wiki.py`

验收标准：

- 对空目录执行 `init` 后，`status` 能识别为有效 Wiki。
- 对当前鸡病 Wiki 执行 `init` 不破坏现有页面。
- 测试覆盖空目录初始化、重复初始化、模板同步三类场景。

### 阶段 2：来源注册与输入路由

目标：实现 `llm-wiki-skill-main` 的来源识别能力，让新增资料能进入统一处理入口。

新增命令：

```bash
chicken-wiki source list
chicken-wiki source match --input "D:/path/file.pdf"
chicken-wiki source match --input "https://example.com/article"
chicken-wiki adapter check --source-id pdf
```

实现方案：

- 新增 `registry.py`，用 Python 数据结构替代 `source-registry.tsv`。
- 来源类型先覆盖本项目需要的核心类型：`markdown`、`text`、`pdf`、`html`、`url`、`plain_text`。
- 每个来源类型定义：
  - `source_id`
  - `source_label`
  - `source_category`
  - `input_mode`
  - `raw_dir`
  - `adapter_name`
  - `dependency_name`
  - `fallback_hint`
- 新增适配器状态分类：`available`、`missing_dependency`、`manual_only`、`failed_retryable`、`failed_manual_fallback`。
- 第一版不需要做复杂外部网页抓取，URL 可先保存为 source record，并要求人工提供正文或 HTML。

验收标准：

- 本地 `.md/.txt/.html/.pdf` 可以被正确匹配到来源类型。
- 未安装 PDF 解析依赖时能返回明确 fallback。
- 所有 source registry 输出都支持 JSON。

### 阶段 3：缓存、去重与 source 页生成

目标：新增资料进入 Wiki 时可去重、可追踪、可重复执行。

新增命令：

```bash
chicken-wiki cache check <raw-file>
chicken-wiki cache update <raw-file> <source-page>
chicken-wiki source-create <raw-file> --title "..." --summary-file summary.md
```

实现方案：

- 新增 `cache.py`。
- 缓存 key 使用文件内容 SHA256；URL 或纯文本输入使用规范化文本 SHA256。
- `.wiki-cache.json` 建议结构：

```json
{
  "version": 1,
  "updated_at": "2026-05-03T00:00:00+08:00",
  "entries": {
    "sha256:...": {
      "source_path": "raw/standards/example.pdf",
      "source_page": "wiki/sources/SRC-0001.md",
      "title": "...",
      "created_at": "...",
      "updated_at": "..."
    }
  }
}
```

- 新增 source 页写入函数，统一生成 frontmatter：
  - `type: source`
  - `source_id`
  - `source_path`
  - `source_type`
  - `authority_level`
  - `evidence_status`
  - `created`
  - `updated`
  - `sources: []`
- 写入 source 页后自动更新 `index.md` 和 `log.md`。

验收标准：

- 同一文件重复消化时命中缓存，不重复生成 source 页。
- 删除缓存条目后可重新生成。
- source 页生成后 `lint` 能检查缓存和文件一致性。

### 阶段 4：素材消化 ingest 与 batch-ingest

目标：把新资料从 raw/source 层转成可检索、可审计的 Wiki 页面和结构化事实。

新增命令：

```bash
chicken-wiki ingest <file-or-url> --title "..."
chicken-wiki ingest-text --title "..." --text-file input.txt
chicken-wiki batch-ingest raw/new_materials --glob "*.md"
```

实现方案：

- 新增 `ingest.py`。
- 第一版采用“确定性骨架 + LLM 可选补全”的双层模式：
  - 不依赖 LLM 时，生成 source 页、摘要、关键词、来源元数据。
  - 启用 LLM 时，生成实体、主题、关系、结构化事实候选。
- 复用现有 `validate_step1_analysis` 校验实体、主题、关系结构。
- 对鸡病领域新增事实候选导出为 `exports/knowledge_facts.candidates.json`，人工审核后再合并到 `knowledge_facts.json`。
- 不直接让 ingest 修改疾病主页面；先生成候选 patch 或 issue 页面，降低污染权威知识库的风险。

推荐流程：

```text
input -> source match -> raw copy -> cache check -> extract text
      -> source page -> step1 analysis -> validate
      -> candidates -> issue/audit page -> optional merge
```

验收标准：

- `.md/.txt/.html` 能完整 ingest。
- `.pdf` 在依赖可用时提取文本，不可用时给出人工 fallback。
- batch-ingest 支持跳过缓存命中的文件。
- 所有候选事实带来源 ID 和 evidence_status。

### 阶段 5：深度综合 digest

目标：补齐跨页面综合分析能力，用于生成诊断专题、用药合规专题、疾病鉴别专题。

新增命令：

```bash
chicken-wiki digest "新城疫与禽流感鉴别诊断" --save
chicken-wiki digest "产蛋下降相关疾病和合规用药" --format report
```

实现方案：

- 新增 `digest.py`。
- 输入 query 后先调用现有 `query_wiki` 找到候选页面和事实。
- 按页面类型分组：疾病、药物、规则、来源、专题、综合页。
- 生成三类输出：
  - `quick`: 简短回答。
  - `report`: 带证据引用的综合报告。
  - `comparison`: 对比表。
- 保存到 `wiki/synthesis/` 或 `wiki/comparisons/`。
- digest 页面必须标记 `derived: true`，并记录使用的 source 页面列表。

验收标准：

- digest 输出中每个关键结论都有 source/fact 引用。
- 保存页面后 `index.md` 和 `log.md` 更新。
- digest 页面不会被当作一手证据，只作为二级综合材料。

### 阶段 6：级联删除与维护

目标：删除素材或页面时自动发现影响范围，避免断链和缓存残留。

新增命令：

```bash
chicken-wiki delete source wiki/sources/SRC-0001.md --dry-run
chicken-wiki delete source wiki/sources/SRC-0001.md --apply
chicken-wiki delete raw raw/standards/example.pdf --dry-run
```

实现方案：

- 新增 `deletion.py`。
- dry-run 默认输出：
  - 将删除的 raw 文件。
  - 将删除或保留的 source 页。
  - 受影响的 wikilinks。
  - 受影响的 cache entries。
  - 受影响的 exports 候选项。
- apply 模式必须只操作 Wiki 根目录内文件。
- 删除后运行 lint，并把删除记录追加到 `log.md`。

验收标准：

- dry-run 不修改任何文件。
- apply 后无 broken wikilink、无 dangling cache entry。
- 删除操作有日志记录。

### 阶段 7：增强 lint 与质量门

目标：把当前基础 lint 升级成 CI 可用的知识库健康检查。

新增命令：

```bash
chicken-wiki lint --strict
chicken-wiki lint --fix
chicken-wiki coverage --json
```

增强检查项：

- 必需路径存在。
- index/log/purpose/schema 存在且可读。
- 所有索引 `page_relpath` 指向真实文件。
- 所有 wikilink 可解析。
- 所有事实有 `evidence_status`。
- 所有事实的 source id 指向 source 页面。
- 所有 source 页有 `source_path` 或明确 `external_url`。
- cache entry 指向真实 raw/source 文件。
- `derived: true` 页面不得作为一手证据。
- `NEEDS_REVIEW` 或 `UNVERIFIED` 事实在 strict 模式下阻断。
- `exports/*.csv/json` 可解析。
- 图谱数据和 exports 计数一致。

实现方案：

- 新增 `linting.py`，把当前 `operations.lint_wiki` 迁移为可组合检查器。
- 每个检查器返回 `CheckResult`：`code`、`severity`、`message`、`path`、`line`、`fixable`。
- `--fix` 只处理安全修复：补目录、排序 index、移除空 cache entry；不自动修改医学事实。

验收标准：

- 普通 lint 对当前 Wiki 通过。
- strict lint 能按配置阻断高风险问题。
- lint JSON 输出适合 CI 读取。

### 阶段 8：完整离线图谱体验

目标：保留当前 `graph-data.json` 生成逻辑，同时把 HTML 升级为离线可用、交互更完整的版本。

新增或增强：

```bash
chicken-wiki graph-build --style simple
chicken-wiki graph-build --style atlas
```

实现方案：

- 去掉 CDN 依赖，把 D3 或图谱运行时代码 vendored 到项目内，或直接内嵌到 HTML。
- `simple` 保留当前轻量版本。
- `atlas` 对齐 `llm-wiki-skill-main/templates/graph-styles/wash/` 的核心体验：
  - 搜索。
  - 分组过滤。
  - 节点详情面板。
  - 邻居节点列表。
  - 统计摘要。
  - 小地图或缩放定位。
  - 推荐起点。
- 图谱数据继续从 `disease_index`、`drug_page_index`、`rule_index`、`knowledge_facts` 构建。

验收标准：

- 双击 HTML 在无网络环境下可打开。
- 搜索、过滤、节点详情可用。
- `graph-data.json` 更新后重新 build 能反映变化。

### 阶段 9：SessionStart 上下文注入

目标：让运行环境自动感知 Wiki 状态，而不是依赖人工执行 `context`。

实现方案：

- 保留 `chicken-wiki context` 作为标准输出入口。
- 新增 `session_context.py`，负责生成短上下文和长上下文。
- 为 Codex/Claude 等环境生成可选 hook 文档或脚本，但不强制安装。
- 对本项目内部主流程，在启动日志中写入 Wiki 状态摘要。
- 在生成/评估输出结果 metadata 中记录 `wiki_dir`、`wiki_fact_count`、`wiki_context_version`。

验收标准：

- 每次生产任务日志包含 Wiki 状态摘要。
- 生成结果 CSV 可追溯使用的知识库版本。
- `context` 输出少于配置的最大字符数。

### 阶段 10：对话结晶化 crystallize

目标：把人工审核、专家讨论、模型评估中有价值的结论沉淀为 Wiki 派生页面。

新增命令：

```bash
chicken-wiki crystallize --title "新城疫用药合规审核记录" --input review.md
chicken-wiki crystallize --title "产蛋下降鉴别讨论" --stdin
```

实现方案：

- 输出到 `wiki/sessions/` 或 `wiki/synthesis/`。
- 页面必须 `derived: true`。
- 必须声明来源：人工讨论、模型评估、运行结果、外部资料。
- 若内容包含医学或监管结论但没有一手 source，标记 `evidence_status: INFERRED` 或 `NEEDS_REVIEW`。
- 不直接写入 `knowledge_facts.json`；先进入候选事实。

验收标准：

- 可从文本生成结晶化页面。
- 页面能被 query 检索到。
- lint 能识别 derived 页面证据等级。

## 主链路适配方案

补完知识库生命周期后，需要把主链路从“只消费静态 Wiki”升级成“消费带版本和审计状态的 Wiki”。

生成阶段：

- `resolve_generation_diseases()` 继续优先读取 `disease_index.csv`。
- prompt 上下文增加 `wiki_version`、`evidence_status_counts`。
- 若目标疾病 coverage 状态为 `needs_audit`，生成 metadata 加 `wiki_coverage_warning`。

评估阶段：

- 双裁判 prompt 明确区分一手事实和派生综合页。
- 对 `NEEDS_REVIEW`、`UNVERIFIED` 事实降低确定性评分。
- 评分输出增加 `wiki_evidence_used` 字段。

规则阶段：

- 禁用药和限制药优先读取结构化事实，而不是仅靠文本命中。
- `fatal_block_codes` 增加可配置项：`banned_drug_wiki_evidence`。
- 对证据不足的高风险结论输出人工复核标记。

持久化阶段：

- CSV 增加：
  - `wiki_dir`
  - `wiki_fact_count`
  - `wiki_context_query`
  - `wiki_evidence_status_counts`
  - `wiki_risk_codes`

## 推荐任务拆分

第一批，低风险高收益：

- 阶段 0：冻结契约与基线。
- 阶段 1：初始化工作流。
- 阶段 3：缓存、去重与 source 页生成。
- 阶段 7：增强 lint。

第二批，形成闭环：

- 阶段 2：来源注册与输入路由。
- 阶段 4：素材消化与批量消化。
- 阶段 5：深度综合报告。
- 阶段 6：级联删除。

第三批，体验增强：

- 阶段 8：完整离线图谱体验。
- 阶段 9：SessionStart 上下文注入。
- 阶段 10：对话结晶化。

## 测试策略

单元测试：

- `cache.py`：hash、命中、miss、自愈、损坏 JSON。
- `registry.py`：文件类型匹配、URL 匹配、fallback 状态。
- `ingest.py`：source 页生成、候选事实生成、缓存跳过。
- `linting.py`：每类错误都有 fixture。
- `deletion.py`：dry-run、apply、安全路径。
- `digest.py`：引用完整性和 derived 标记。
- `graph.py`：节点数、链接数、离线 HTML 包含内嵌依赖。

集成测试：

```bash
python -m pytest -q
chicken-wiki --json status
chicken-wiki --json lint
chicken-wiki ingest tests/fixtures/wiki/raw/sample.md
chicken-wiki digest "新城疫 鉴别诊断" --save
chicken-wiki graph-build --style atlas
```

回归测试：

- 当前 7 个 LLM Wiki 测试必须持续通过。
- 主流程 help 和最小 dry-run 入口必须可执行。
- 对真实鸡病 Wiki 的 `status/lint/query/graph-build` 必须可执行。

## 风险与控制

医学事实污染风险：

- ingest 不直接写入权威事实表，先写候选事实。
- `derived` 页面不得作为一手证据。
- strict lint 阻断缺来源的监管和用药结论。

脚本依赖风险：

- 不把 `llm-wiki-skill-main` shell 脚本作为核心运行依赖。
- 稳定能力迁移到 Python，shell 只作为参考或兼容层。

中文编码风险：

- 所有文件读写统一 `utf-8-sig` 兼容读取、`utf-8` 写入。
- Windows 文档明确设置 `PYTHONIOENCODING=utf-8`。

工作区迁移风险：

- 当前仓库已有大量删除和新增，补完功能时避免混入无关回滚。
- 每阶段单独提交，文档、代码、测试同步推进。

性能风险：

- Wiki 加载继续使用缓存。
- ingest 和 lint 对大目录采用增量签名。
- graph-build 可先只用 exports，不每次扫描全部页面正文。

## 里程碑验收

M1：维护基础可用

- `init/cache/source-create/lint --strict` 可用。
- 当前 Wiki 包 lint 通过。
- source 页和 cache 能闭环。

M2：新增资料可入库

- `ingest/batch-ingest` 可用。
- 候选事实可生成、可验证、可审计。
- 不污染正式 `knowledge_facts.json`。

M3：知识库可持续演进

- `digest/delete/coverage` 可用。
- index/log/cache/source/facts 一致性可由 lint 检查。
- 生成和评估结果可追溯 Wiki 版本。

M4：体验和自动上下文完善

- 离线 atlas 图谱可用。
- Session context 可自动或半自动注入。
- crystallize 可把审核讨论沉淀为派生页面。

## 最小可落地版本

如果只做一个最小版本，建议实现以下 6 个功能：

1. `init`
2. `.wiki-cache.json`
3. `source-create`
4. `ingest` 的 `.md/.txt/.html` 版本
5. `lint --strict`
6. `digest --save`

这 6 个功能可以让当前系统从“静态知识包消费者”升级为“可维护知识库系统”，同时不会触碰图片功能，也不会大规模重写生成和评估主链路。
