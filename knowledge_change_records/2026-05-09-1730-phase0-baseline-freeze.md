# Phase 0 Baseline Freeze

Date: 2026-05-09

## 修改目标和范围

执行猪病 LLM Wiki 清洗整理的 Phase 0：冻结当前基线，记录清洗前状态，避免后续 Phase 1/2/后续阶段无法追溯变化来源。

涉及新增文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/baseline_phase0_2026-05-09.json`

未修改实体页、索引、运行时代码或事实表。

## 修改前存在的问题

清洗执行前虽然已经有 readiness 审计脚本和 runtime manifest，但缺少本轮 Phase 0 专用基线记录。后续如果修改根元数据、schema、编码脚本或实体页，难以直接说明：

- 修改前 readiness 是多少。
- 清洗前 disease/drug/source/rule 等数量是多少。
- runtime manifest 当前默认加载哪些类型页面。
- 已知的清洗前问题有哪些。

## 修改前代码和知识库状态

执行前 `ai-` 工作树为 clean。

执行 readiness 审计：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- readiness_score: 99。
- diseases: 73。
- drugs: 81。
- syndromes: 22。
- comparisons: 17。
- rules: 449。
- rule_cards: 18。
- sources: 219。
- synthesis: 27。
- topics: 99。
- missing_paths: 0。
- bad_fact_tables: []。
- missing_rule_cards: []。
- missing_synthesis: []。

runtime manifest summary：

- comparison: 14。
- disease: 73。
- drug: 80。
- rule_card: 15。
- syndrome: 12。
- synthesis: 4。
- missing paths: 0。

## 本次更新或新增了什么

新增 `baseline_phase0_2026-05-09.json`，记录：

- Phase 0 目的。
- git 状态。
- readiness 审计结果。
- runtime manifest summary。
- 已知清洗前问题。

## 本次整理工作

本阶段没有整理 disease/drug 实体页，只做基线冻结。

已记录的清洗前问题包括：

- `purpose.md` 仍将知识库描述为 chicken disease。
- `index.md` 标题仍为 Chicken Disease LLM Wiki。
- `README.md` 仍描述为 Phase 1/2 初始建设阶段。
- legacy review 状态尚未迁移到 `source_status`、`fact_validity`、`task_use_status`。
- 尚未有可重复运行的编码完整性审计脚本。

## 修改后解决了什么

本次新增了可追溯基线。后续所有 Phase 1/2 改动都可以与该 JSON 对照，判断是否引入路径缺失、事实表异常或 runtime manifest 变化。

## 预计更新效果

- 支持阶段性工作汇报。
- 支持后续回滚和差异解释。
- 为 Phase 1 根元数据修正和 Phase 2 编码审计提供基准。

## 验证

已运行：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

验证结果：

- readiness_score: 99。
- missing_paths: 0。
- bad_fact_tables: []。

## 残余风险和下一步

Phase 0 不修复问题，只冻结问题。下一步继续执行 Phase 1 根元数据修正和 Phase 2 编码完整性审计。
