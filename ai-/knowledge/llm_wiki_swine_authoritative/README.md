# Swine Disease LLM Wiki

本知识库是面向猪病生产、评估、仲裁和黄金数据集生产的 source-first LLM Wiki。它遵循 `llm-wiki-skill` 的本地 Markdown 知识库结构：`raw/` 保留原始素材，`wiki/` 保留结构化知识页，`exports/` 保留索引、事实表和运行时 manifest，`issues/` 保留审计与问题清单。

## Mandatory Governance Rules

任何后续 Wiki 更新、来源补充、事实抽取、网页资料整理、本地 Markdown/PDF/Word/Excel 资料整理、runtime 页面改写、证据迁移、索引重建、图谱重建或黄金数据集生成，都必须先遵守以下两份强制规则：

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

执行要求：

- 每次更新先读两份短执行卡；遇到具体场景时，再查两份完整制度文档。
- 所有会修改 Wiki 的更新命令必须通过固定入口执行：`tools/run_guarded_wiki_update.py`。
- 不得绕过这两份文档直接把网页内容、本地 Markdown 内容、PDF 摘录、模型输出或批量抽取结果写入 runtime 页面。
- 新增、修改、删除、降级、归档、迁移、覆盖旧数据或重建派生产物时，必须按 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 说明事实逻辑和旧数据处理方式。
- 每次维护必须使用 `SOURCE_BATCH_INTAKE_CHECKLIST.md` 做执行前检查，并在 `knowledge_change_records/` 中记录治理合规情况。
- 如果脚本输出与治理规则冲突，必须先修正规则或脚本，不得以脚本结果直接覆盖医学事实边界。

## Current Baseline

- 疾病页：73。
- 药物页：81。
- 综合征页：22。
- 鉴别页：17。
- 规则页：449。
- 规则卡：18。
- 来源页：219。
- 综合页：27。
- 2026-05-09 readiness score：99/100。

## Runtime Boundary

生产和评估默认使用：

- allowlist: `exports/runtime_core_manifest.json`
- denylist: `exports/runtime_exclude_patterns.json`

默认运行时不得直接加载 `raw/`、`issues/`、graph 导出、会话记录、备份文件或大型治疗/处方矩阵。需要审计、追溯或证据扩展时，再通过专门流程读取这些材料。

## Usability Rule

知识是否可用不由“是否复核”单独决定。只要来源清晰明确、数据有效、来源等级匹配任务用途，即可进入对应任务流。

核心判断字段：

- `source_status`
- `fact_validity`
- `authority_level`
- `risk_class`
- `task_use_status`

`HUMAN_REVIEWED`、`NEEDS_REVIEW` 等历史字段只作为迁移线索或 legacy audit 信息，不作为直接 allow/block 门槛。

## High-Risk Boundary

剂量、疗程、给药途径、休药期、MRL、残留、食品安全、法定报告、检疫、扑杀、调运、官方处置、兽药标签等高风险结论必须有 A0 或标签级等价来源支持。没有匹配来源时，只能写成边界、拒答、后续检索任务或 `blocked`。

## Maintenance Records

每次清洗、整理、索引重建、脚本修改或状态迁移，都必须在根目录 `knowledge_change_records/` 新增工作留痕文档，说明修改前问题、修改内容、预期效果、验证命令和残余风险。
