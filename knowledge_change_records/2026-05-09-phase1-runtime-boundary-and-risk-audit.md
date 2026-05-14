# Phase 1 运行时边界和幻觉风险审计执行记录

日期：2026-05-09

## 本阶段目标

本阶段目标是先不改动生产实体页内容，而是建立生产和评估链路的运行时边界：

- 明确哪些页面可以默认进入 production/evaluation retrieval。
- 明确哪些目录和文件默认不应被无差别索引。
- 增加一个可重复运行的 hallucination risk audit，用于发现过长页面、编码损坏、候选事实、高风险用药/监管词等问题。

## 修改前存在的问题

### 1. 缺少 runtime allowlist

修改前，知识库已有：

- `exports/disease_index.csv`
- `exports/drug_page_index.csv`
- `exports/rule_card_index.csv`
- `exports/comparison_index.csv`
- `exports/syndrome_index.csv`
- `exports/synthesis_index.csv`

但没有一个专门告诉生产链路“只加载这些页面”的清单。

风险：

- 如果生产链路直接索引 `wiki/`，会混入图谱、会话、综合矩阵、构建痕迹等内容。
- 如果直接索引 `exports/`，会混入 fact index 和 mention index 这类证据扩展表。

### 2. 缺少默认排除规则

修改前，`raw/`、`issues/`、`wiki/sessions/`、`wiki/knowledge-graph.html`、`wiki/graph-data.json` 和大型 treatment/prescription matrix 没有统一的 runtime denylist。

风险：

- 检索召回过大，噪声增加。
- 候选事实或历史抽取内容可能被模型当成稳定结论。

### 3. 缺少面向幻觉风险的专项审计

已有 readiness audit 能验证结构完整性，但它不会专门检查：

- 页面是否过大。
- 是否有 UTF-8 replacement character。
- 是否包含 `candidate_fact`。
- 是否有剂量、疗程、休药期、MRL、扑杀、封锁、调运等高风险词。
- 高风险词是否缺少规则卡锚点。

## 本阶段新增或更新的代码

新增：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`

更新：

- `build_runtime_core_manifest.py` 首次运行时发现 `drug_page_index.csv` 里有 4 个非药物实体页的 evidence index CSV 路径。
- 已收紧脚本逻辑：药物实体只允许 `wiki/drugs/*.md` 进入 runtime manifest。

## 本阶段新增或更新的知识库产物

新增/生成：

- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_exclude_patterns.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest_summary.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/runtime_hallucination_risk_audit_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/runtime_hallucination_risk_audit_2026-05-09.md`

## 修改后解决了什么

### 1. 明确了生产默认加载边界

`runtime_core_manifest.json` 当前包含 198 个条目，且路径全部存在。

条目类型包括：

- disease
- drug
- rule_card
- comparison
- syndrome
- synthesis policy

### 2. 排除了明显不适合默认运行时检索的内容

`runtime_exclude_patterns.json` 默认排除：

- `raw/**`
- `issues/**`
- `wiki/sessions/**`
- `wiki/exports/**`
- `wiki/knowledge-graph.html`
- `wiki/graph-data.json`
- `wiki/synthesis/*treatment_matrix.md`
- `wiki/synthesis/*prescription_matrix.md`
- `exports/*.p0_backup_*`

### 3. 建立了幻觉风险基线

`audit_runtime_hallucination_risk.py` 对 runtime manifest 中的 198 个条目进行风险扫描。

当前结果：

- high: 9
- medium: 103
- low: 47
- none: 39

高风险页面主要集中在：

- 大型药物页。
- 包含候选事实的药物页。
- 包含剂量、疗程、休药期、MRL 等词但缺少显式规则卡锚点的页面。
- 存在 replacement character 的疾病页。

优先清洗对象：

- `wiki/drugs/DRUG-034-sulfonamides.md`
- `wiki/drugs/DRUG-014-lincomycin.md`
- `wiki/drugs/DRUG-009-penicillin-g.md`
- `wiki/drugs/DRUG-030-tetracyclines.md`
- `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `wiki/diseases/DIS-040-colibacillosis.md`
- `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`

## 验证命令和结果

生成 runtime manifest：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py`

结果：

- entries: 198
- missing_paths: 0

运行 hallucination risk audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py`

结果：

- entries_checked: 198
- high: 9
- medium: 103
- 输出报告：
  - `issues/runtime_hallucination_risk_audit_2026-05-09.json`
  - `issues/runtime_hallucination_risk_audit_2026-05-09.md`

运行原 readiness audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py`

结果：

- readiness_score: 99
- missing_paths: 0
- bad_fact_tables: 0
- missing_rule_cards: 0
- missing_synthesis: 0

## 后续建议

下一阶段进入 Phase 2：

- 先修复或隔离包含 replacement character 的疾病页。
- 优先处理 `DIS-026`、`DIS-044`、`DIS-040`、`DIS-009`。
- 修复后重新运行 hallucination risk audit，观察 encoding findings 是否下降。
