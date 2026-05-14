# 猪病 LLM Wiki 分阶段清洗和整理方案

日期：2026-05-09

## 背景

当前知识库 `ai-/knowledge/llm_wiki_swine_authoritative` 已经具备较好的 source-first 基础：有疾病页、药物页、规则卡、综合页、来源页、结构化 fact index 和 readiness 审计脚本。

但它的问题不是“没有证据”，而是“证据层级和运行时边界不够清楚”。如果生产或评估链路直接索引整个 `wiki/`、`exports/` 或更大范围目录，容易把历史构建材料、候选事实、原始抽取、长矩阵和稳定知识混在一起，从而增加幻觉、证据漂移、过度处方建议、评估不稳定等风险。

## 分阶段目标

### Phase 0：现状基线和工作留痕机制

目标：

- 建立根目录工作留痕文件夹。
- 记录现状、问题、已有代码和知识库结构。
- 不直接改动生产知识页。

已完成：

- 新增 `knowledge_change_records/`。
- 新增 `knowledge_change_records/README.md`。
- 新增现状评估文档 `2026-05-09-llm-wiki-current-state-and-cleanup-plan.md`。

### Phase 1：建立运行时边界和风险审计

目标：

- 生成 production/evaluation 默认可加载的 runtime allowlist。
- 生成默认排除规则，避免 raw、issues、sessions、graph、大型矩阵被无差别检索。
- 新增 hallucination risk audit，量化高风险页面。

核心改动：

- 新增 `tools/build_runtime_core_manifest.py`。
- 新增 `exports/runtime_core_manifest.json`。
- 新增 `exports/runtime_exclude_patterns.json`。
- 新增 `exports/runtime_core_manifest_summary.md`。
- 新增 `tools/audit_runtime_hallucination_risk.py`。
- 新增 `issues/runtime_hallucination_risk_audit_2026-05-09.json`。
- 新增 `issues/runtime_hallucination_risk_audit_2026-05-09.md`。

验收标准：

- runtime manifest 中所有路径存在。
- manifest 不包含 `raw/**`、`issues/**`、`wiki/sessions/**`、graph HTML/JSON、大型 treatment/prescription matrix。
- 风险审计能重复运行，并输出 high/medium/low/none 统计。

### Phase 2：编码损坏和显著脏数据清洗

目标：

- 修复或隔离包含 UTF-8 replacement character 的生产实体页。
- 优先处理会直接影响召回和生成的疾病页。

优先文件：

- `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- `wiki/diseases/DIS-040-colibacillosis.md`
- `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`

执行策略：

- 先从原始 Markdown、fact index 或 source pages 复原损坏事实。
- 不能复原的片段移动到 evidence gap 或标记为不可用于 runtime。
- 每个修复批次生成一份留痕文档，列出修复前问题、修复位置、证据来源、修复后验证结果。

验收标准：

- 生产实体页中 replacement character 计数下降。
- readiness audit 不下降。
- hallucination risk audit 中 encoding findings 减少。

### Phase 3：过长实体页拆分

目标：

- 将实体页改为“运行时核心摘要 + 证据扩展链接”的结构。
- 把 V11/V12/V13/V14 批次增强块、candidate facts、长处方列表迁移到 evidence expansion 层。

优先对象：

- 大于 20 KB 的疾病页。
- 大于 20 KB 的药物页。
- hallucination risk audit 中 high 的药物页。

执行策略：

- 保留实体页中的关键字段：身份、别名、适用边界、核心临床事实、用药/监管硬边界、来源锚点。
- 将大段候选事实、处方列表、药物 mention 列表迁入 `wiki/evidence_expansions/` 或继续由 `exports/*fact_index.csv` 承载。
- 更新 manifest，只让核心页进入 runtime core。

验收标准：

- 大页面数量下降。
- high-risk 药物页数量下降。
- 候选事实不再直接暴露在 runtime core 页中。

### Phase 4：证据状态和规则卡统一

目标：

- 统一 evidence status、runtime tier、allowed use、blocked use。
- 所有高风险用药、休药期、MRL、监管处置内容必须显式连到规则卡。

建议状态：

- `runtime_core_reviewed`
- `runtime_core_partial`
- `runtime_core_guardrail`
- `runtime_core_policy`
- `evidence_expansion`
- `candidate_only`
- `raw_archive`
- `do_not_index`

验收标准：

- manifest 中所有 runtime core 页面都有明确 tier。
- 药物页包含 `RC-DRUG-001` 或等价规则锚点。
- 休药期/MRL 相关页面包含 `RC-WITHDRAWAL-MRL-001` 或等价规则锚点。
- 法定疫病/应急处置页面包含监管规则卡或 A0/A1 来源。

### Phase 5：生产和评估链路接入

目标：

- 生产问答和评估系统默认读取 `runtime_core_manifest.json`。
- 只有证据扩展、审计、溯源场景才读取 `raw/`、`issues/`、大型矩阵和完整 fact index。

验收标准：

- 生产链路有 allowlist loader。
- 评估链路有同样的 allowlist 或明确的测试集专用 manifest。
- 若请求涉及剂量、疗程、休药期、MRL、扑杀、封锁、调运、检疫等内容，系统必须触发规则卡和来源扩展。

## 每次修改的留痕要求

每次修改必须在 `knowledge_change_records/` 新增一份 Markdown 文档，建议包含：

- 修改日期和阶段。
- 修改前存在什么问题。
- 修改前相关代码、索引、知识库结构是什么样。
- 修改了什么文件。
- 新增或更新了什么代码。
- 整理了哪些知识文件或生成了哪些产物。
- 修改后解决了什么风险。
- 验证命令和验证结果。
- 后续遗留问题。

## 当前执行状态

- Phase 0 已完成。
- Phase 1 已执行。
- Phase 2 建议下一步开始。

