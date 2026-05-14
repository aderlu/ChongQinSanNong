# 兽药合理应用与联用手册（1-200页）抽取与 Wiki 补强报告 / 2026-05-08

## 抽取范围

- 原始文件：`raw/md/兽药合理应用与联用手册1-200页.md`
- source_id：`SRC-0091`
- 覆盖章节：第 1 章合理用药/联用禁忌基础知识；第 2 章抗菌药合理应用及联用禁忌；第 3 章消毒防腐药；第 4 章抗寄生虫药合理应用及联用禁忌（至约 p.200）。

## 分种类抽取统计

- β-内酰胺/头孢菌素类: 2
- β-内酰胺/青霉素类: 4
- 其他驱线虫药: 1
- 咪唑并噻唑类驱虫药: 1
- 喹噁啉类: 2
- 喹诺酮类: 3
- 四氢嘧啶类驱虫药: 1
- 四环素类: 4
- 多肽类: 3
- 大环内酯类: 4
- 截短侧耳素/其他抗生素: 2
- 抗球虫药: 2
- 抗绦虫药: 1
- 拟除虫菊酯类杀虫药: 2
- 有机磷杀虫药: 1
- 林可胺类: 1
- 氨基糖苷类: 6
- 硝基咪唑类: 4
- 磺胺类/增效剂: 6
- 苯并咪唑类驱虫药: 2
- 酰胺醇类: 1
- 阿维菌素类: 4

## 写入结果

- drug 页面增强：56 页。
- disease 页面增强：15 页。
- 新增/刷新 facts：82 条。
- 新增疾病别名索引：43 条，写入 `exports/alias_index.csv`，用于降低 `target_disease_alias_not_in_diagnosis` 风险。
- 新增 rule card：`wiki/rule_cards/RC-DRUG-COMBINATION-RAU-001.md`。
- 新增 synthesis 矩阵：`wiki/synthesis/veterinary_rational_use_1_200_drug_disease_rule_matrix.md`。
- 新增 comparison 矩阵：`wiki/comparisons/veterinary_rational_use_1_200_antimicrobial_combination_matrix.md`。
- 新增 syndrome 入口：3 页。
- 新增索引：`exports/veterinary_rational_use_1_200_fact_index.csv`、`exports/veterinary_rational_use_1_200_drug_index.csv`。

## 约束结论

- 本轮补强显著增加了 drug/disease/rule 三方映射和联用禁忌约束。
- 本来源可作为候选和边界增强；具体剂量、疗程、休药期、MRL 或合规结论仍必须叠加当前标签/A0/A1 来源。
- drug 页 `NEEDS_REVIEW` 显式残留由 45 页降至 10 页；剩余主要是本书 1-200 页未覆盖或页码超过本批范围的药物，如 tulathromycin、tildipirosin、amitraz、ponazuril、ractopamine 等。
- disease 页 `NEEDS_REVIEW` 仍为 32 页，本批来源不是疾病专著，未对未覆盖的病毒性/罕见病页面作状态升级；但已对 15 个与抗菌药、抗寄生虫药直接相关的疾病页补充 drug-rule 边界。
