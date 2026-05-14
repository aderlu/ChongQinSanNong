# Worker B 药物实体页状态清洗留痕

- 日期：2026-05-12
- 范围：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\drugs` 下 81 个药物实体 Markdown 页。

## 之前问题

历史状态同时分散在 `legacy_evidence_status`、`gold_dataset_use`、`drug_page_status`、正文“页面类型/页面状态/黄金集用途”和个别标签中；`boundary_only`、`positive_label_candidate`、`negative_trap`、排除正向生成等语义不在同一字段下，容易让召回、正向生成、负例评估和合规边界混用。

## 修改范围

仅修改 Worker B 指定的 drugs 目录药物实体页，并新建本留痕文件。未修改其他 wiki 目录、证据扩展目录或其他工作者负责目录。

## 修改后解决什么

将历史状态归并为简化模型：`source_trust` 表示人工复核/待复核可信度，`evidence_coverage` 表示页面证据覆盖形态，`usage_scope` 表示运行时/黄金集使用范围。旧的 `gold_dataset_use=` 正文引用同步改为 `usage_scope=`，`negative_trap` 和排除正向生成语义统一收敛到 `usage_scope=negative_trap`。

## 改了哪些文件或整理类型

- 批量替换 front matter：`legacy_evidence_status` -> `source_trust`，`drug_page_status` -> `evidence_coverage`，`gold_dataset_use` -> `usage_scope`。
- 批量替换正文状态表述：页面状态/页面类型/黄金集用途改写为 `source_trust`、`evidence_coverage`、`usage_scope` 语义。
- 保留 `sources`、`source_id`、`fact_id`、页码锚点、证据扩展索引、适应症、靶动物、休药期、MRL、禁用限制等高风险边界文本。
- 对 `DRUG-075-praziquantel.md` 的历史 `negative_trap` 标签和正文排除正向生成说法做归并，明确落到 `usage_scope=negative_trap`。

## 预计效果

检索和生成链路可以直接读取三字段判断来源可信度、证据覆盖和使用范围，减少 boundary-only 页面被误当正向处方页、positive label 候选被跨法域外推、negative trap 被混入正向生成的风险。

## 编码措施

所有被写入的 Markdown 文件均使用 UTF-8 写回；未使用 ANSI/本地代码页写入。修改后用 `rg` 复核旧字段名残留，并抽查关键页面确认来源和事实锚点仍在。

## 修改数量

- 药物实体页：81 个。
- 留痕文件：`D:\XF-ChongQin\knowledge_change_records\2026-05-12-worker-b-drugs-status-cleanup.md`。
