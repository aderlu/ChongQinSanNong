# Review Status Degating Execution Plan Update

Date: 2026-05-09

## 修改目标和范围

本次修改更新执行文档：

`knowledge_change_records/2026-05-09-swine-llm-wiki-comprehensive-cleanup-execution-plan.md`

目标是把“复核状态”从事实可用性门槛中移除，明确后续清洗和代码优化应按以下原则执行：

只要来源清晰明确、数据有效、来源等级匹配任务用途，数据就能够直接进入对应任务流。

## 修改前存在的问题

原执行文档已经提出 `HUMAN_REVIEWED`、`NEEDS_REVIEW` 不等于训练用途状态，但仍有若干表述容易让后续执行误解为：

- `NEEDS_REVIEW` 天然不可用。
- `HUMAN_REVIEWED` 才是可用事实。
- “复核”是导出、生成、评估前的必要门槛。
- `evidence_status` 可以继续作为 runtime loader、exporter、audit 的主判断字段。

这会导致来源清晰、数据有效的事实被错误阻断，尤其影响疾病临床事实、教材来源事实、已登记 source/fact/rule 锚点事实进入训练和评估流程。

## 修改前相关状态

执行文档中已有统计：

- 疾病页中 `HUMAN_REVIEWED`: 41，`NEEDS_REVIEW`: 32。
- 药物页中 `HUMAN_REVIEWED`: 73，`NEEDS_REVIEW`: 8。

这些字段应被视为历史审计字段或迁移线索，而不是事实能否使用的最终判断。

## 本次更新或新增了什么

本次未修改业务代码、实体页、索引或导出文件。

本次更新了执行文档：

1. 修改目标条款：
   - 明确可用性不再由“是否复核”决定。
   - 改为由来源是否清晰、数据是否有效、来源等级是否匹配任务用途决定。

2. 强化问题分析：
   - 将 `3.3` 改为“复核状态、证据状态和任务用途尚未完全解耦”。
   - 增加新的判断原则：来源清晰、数据有效、来源等级匹配用途、任务用途明确。

3. 新增 Phase 6：
   - `Phase 6: 复核相关状态去门槛化和相关代码优化`
   - 明确全库检索和迁移 `NEEDS_REVIEW`、`HUMAN_REVIEWED`、`reviewed`、`review`、`待复核`、`人工复核`、`evidence_status`。
   - 要求优化 entity pages、source pages、exports、manifest builder、readiness audit、hallucination risk audit、exporter、runtime loader 和 tests。

4. 新增主判断字段：
   - `source_status`
   - `fact_validity`
   - `authority_level`
   - `risk_class`
   - `task_use_status`

5. 调整后续阶段编号：
   - 黄金数据集用途分层改为 Phase 7。
   - 高风险规则卡加固改为 Phase 8。
   - 索引图谱重建改为 Phase 9。
   - 猪病测试改为 Phase 10。
   - 黄金数据集试生产改为 Phase 11。

## 修改后解决了什么

本次更新明确了后续执行方向：

- 不再用 `NEEDS_REVIEW` 表示不可用。
- 不再用 `HUMAN_REVIEWED` 表示唯一可用。
- 不再用“待复核”作为事实、页面、导出样本的默认阻断理由。
- `evidence_status` 可以作为 legacy audit field 保留，但不得作为主判断字段。
- 来源清晰、数据有效、来源等级匹配用途的数据可以直接使用。

## 预计更新效果

后续执行后预计会带来：

- 提高可用事实覆盖率，避免来源清晰事实被历史复核字段误伤。
- 提高黄金数据集生产效率。
- 让 exporter 和 runtime loader 判断更加稳定、透明、可解释。
- 保留高风险来源等级门槛，避免取消复核门槛后误放开监管、药物、休药期、MRL、食品安全等高风险结论。

## 验证

本次修改后执行：

```powershell
rg -n "Phase 6|source_status|fact_validity|NEEDS_REVIEW|HUMAN_REVIEWED|复核相关状态去门槛化" knowledge_change_records\2026-05-09-swine-llm-wiki-comprehensive-cleanup-execution-plan.md
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

预期：

- 文档能检索到新增 Phase 6 和新字段。
- readiness 仍保持 99。
- missing paths 仍为 0。

## 残余风险和下一步

本次只是修改执行文档，尚未真正修改代码和实体页。

下一步需要按 Phase 6 执行实际迁移：

- 修改 schema 和 manifest builder。
- 修改 exporter、runtime loader、readiness audit、hallucination risk audit。
- 为 facts 和 manifest 增加 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status`。
- 生成 `issues/review_status_migration_YYYY-MM-DD.json`。
- 对仍然 blocked 的事实写清楚具体阻断原因，而不是写“待复核”。
