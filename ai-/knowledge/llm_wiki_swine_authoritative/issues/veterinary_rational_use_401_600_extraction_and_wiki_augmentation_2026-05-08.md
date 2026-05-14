# 兽药合理应用与联用手册（401-600页） 批处理增强报告

## 处理范围

- 源文件：`raw/md/兽药合理应用与联用手册401-600页.md`
- 已切片章节：14 个，覆盖 p.401-600。
- 抽取中药/联用条目：229 个。
- 写入结构化 facts：421 条。

## 写入内容

- 来源页：`wiki/sources/SRC-0093-veterinary-rational-use-combination-manual-401-600.md`
- 新增 drug 实体页：`wiki/drugs/DRUG-081-traditional-chinese-veterinary-medicines.md`
- 更新既有 drug 页：7 个。
- 更新 disease 页：21 个。
- 新增 syndrome 页：4 个；增强既有 syndrome 页：9 个。
- 新增 rule card：`wiki/rule_cards/RC-TCM-COMPATIBILITY-RAU-003.md`
- 新增 synthesis 矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`
- 新增 comparison 矩阵：`wiki/comparisons/veterinary_rational_use_401_600_tcm_symptom_differential_matrix.md`
- 导出索引：`exports/veterinary_rational_use_401_600_fact_index.csv`、`exports/veterinary_rational_use_401_600_drug_index.csv`

## 质量与边界

- 本批主要补强中药类兽药、症候支持、联用禁忌、毒性注意和鉴别边界。
- 本批不会把仍缺现代标签证据的药物强行改为可执行处方来源；剩余 `NEEDS_REVIEW` 药物若未被本来源覆盖，应继续用标签/法规/药典来源补足。
- 原始 Markdown 未保留显式分页符；本批按 401-600 页段、章节起点和条目行号建立页码锚点，并保留 `line=` 供复核。
