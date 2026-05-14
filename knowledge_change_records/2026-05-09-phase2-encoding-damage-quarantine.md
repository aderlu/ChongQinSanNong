# Phase 2 编码损坏清洗与隔离执行记录

日期：2026-05-09

## 本阶段目标

按照 `2026-05-09-wiki-phased-cleanup-plan.md` 的 Phase 2，优先处理生产运行时页面中的编码损坏和明显脏数据。

本阶段采取“隔离而不猜测修复”的策略：

- 不凭模型猜测损坏文本原意。
- 将含 UTF-8 replacement character 的抽取行从 runtime Markdown 正文中移除。
- 在原位置留下干净的 `PHASE2_ENCODING_QUARANTINED` 占位行。
- 将原始损坏行保存到 `issues/phase2_encoding_quarantine_2026-05-09.json`，保留事实编号和来源锚点，方便后续从原始材料重新抽取。

## 修改前存在的问题

Phase 1 的幻觉风险审计发现 4 个 runtime 疾病页存在编码损坏：

- `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- `wiki/diseases/DIS-040-colibacillosis.md`
- `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`

这些页面中的损坏不是整页损坏，而是各有 1 条 SFDUT 批次抽取事实行发生严重乱码或 replacement character 问题。

修改前风险：

- 损坏行会进入 runtime retrieval，污染 embedding 和召回。
- 损坏文本中仍带有剂量、补液、治疗或防控相关片段，可能诱发模型基于乱码生成不可靠结论。
- 如果直接删除，后续无法追踪原始 fact id 和 source anchor。
- 如果猜测性修复，可能引入未经来源验证的新错误。

## 修改前相关代码和知识库状态

已有代码：

- `tools/build_runtime_core_manifest.py`：Phase 1 新增，用于生成 runtime allowlist。
- `tools/audit_runtime_hallucination_risk.py`：Phase 1 新增，用于审计幻觉风险。
- `tools/audit_swine_llm_wiki_readiness.py`：原有 readiness 审计脚本。

修改前审计基线：

- runtime manifest entries: 198
- runtime hallucination risk audit:
  - high: 9
  - medium: 103
  - low: 47
  - none: 39
- readiness score: 99/100

修改前 4 个优先疾病页 replacement character 分布：

- `DIS-026-foot-and-mouth-disease-picornaviruses.md`: 570
- `DIS-044-gl-sser-s-disease.md`: 347
- `DIS-040-colibacillosis.md`: 332
- `DIS-009-transmissible-gastroenteritis-virus.md`: 189

## 本阶段新增或更新的代码

新增脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/quarantine_encoding_damaged_lines.py`

脚本功能：

- 读取 `exports/runtime_core_manifest.json`。
- 只处理 runtime manifest 中的 Markdown 页面。
- 查找包含 UTF-8 replacement character 的行。
- 提取可用的 fact id、source_id、page、line 锚点。
- 将损坏行替换为干净的 `PHASE2_ENCODING_QUARANTINED` 占位说明。
- 将原始损坏行写入隔离 JSON 和 Markdown 报告。

## 本阶段整理或修改的知识文件

以下 4 个疾病页被修改，各隔离 1 条损坏行：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-040-colibacillosis.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-044-gl-sser-s-disease.md`

新增隔离记录：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase2_encoding_quarantine_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase2_encoding_quarantine_2026-05-09.md`

隔离的原始事实锚点：

- `SFDUT1-TX-0691`; `SRC-0089`; page 176; line 3556
- `SFDUT1-TX-0585`; `SRC-0089`; page 134; line 2918
- `SFDUT2-TX-0123`; `SRC-0090`; page 227; line 538
- `SFDUT2-TX-0041`; `SRC-0090`; page 201; line 167

## 修改后解决了什么

### 1. runtime 页面不再包含这些 replacement character

修改后 4 个优先疾病页检查结果：

- `DIS-026-foot-and-mouth-disease-picornaviruses.md`: replacement character 0; quarantine placeholder 1
- `DIS-044-gl-sser-s-disease.md`: replacement character 0; quarantine placeholder 1
- `DIS-040-colibacillosis.md`: replacement character 0; quarantine placeholder 1
- `DIS-009-transmissible-gastroenteritis-virus.md`: replacement character 0; quarantine placeholder 1

### 2. 原始损坏证据没有丢失

损坏原文保存在：

- `issues/phase2_encoding_quarantine_2026-05-09.json`

管理汇报和人工审查可读摘要保存在：

- `issues/phase2_encoding_quarantine_2026-05-09.md`

### 3. 幻觉风险审计结果改善

修改前：

- high: 9
- medium: 103
- low: 47
- none: 39

修改后：

- high: 7
- medium: 102
- low: 50
- none: 39

说明：

- 原先因 encoding damage 进入 high 的疾病页已从 high 风险列表中移出。
- 当前 high 风险主要转移到大型药物页和含候选事实、剂量、休药期/MRL词的药物页。

## 验证命令和结果

执行编码损坏隔离：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\quarantine_encoding_damaged_lines.py`

结果：

- quarantined_lines: 4
- files: 4

重新生成 runtime manifest：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py`

结果：

- entries: 198
- missing_paths: 0

运行 hallucination risk audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py`

结果：

- entries_checked: 198
- high: 7
- medium: 102

运行原 readiness audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py`

结果：

- readiness_score: 99
- missing_paths: 0
- bad_fact_tables: 0
- missing_rule_cards: 0
- missing_synthesis: 0

## 后续遗留问题

Phase 2 已完成优先编码损坏隔离，但仍有两类问题需要后续阶段处理：

1. 当前 high 风险主要集中在药物页，例如 `DRUG-034-sulfonamides`、`DRUG-014-lincomycin`、`DRUG-009-penicillin-g`、`DRUG-030-tetracyclines` 等。
2. 很多药物页含 candidate facts、剂量/疗程/休药期/MRL 相关词，但 runtime 正文中缺少显式规则卡锚点，建议进入 Phase 3/4 处理。

下一步建议：

- Phase 3 优先拆分高风险大型药物页，把处方/剂量/候选事实迁移到 evidence expansion 层。
- Phase 4 为药物页补强 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001` 等规则卡锚点。

