---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-032-rabies-virus.md
original_section: "Web Source Reinforcement / V11 P1"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [A0-MOA-573, A1-CDC-RABIES-LABORATORY-DIAGNOSIS-2024, A1-CDC-RABIES-VETERINARIANS-2025, CMP-008, CMP-008-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-005-]
default_runtime: false
updated: 2026-05-09T20:06:42+08:00
---

# DIS-032-rabies-virus / Web Source Reinforcement / V11 P1

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Web Source Reinforcement / V11 P1

> 2026-05-08 web-first P1补强。新增或采用来源：`A0-MOA-573`、`A1-CDC-RABIES-VETERINARIANS-2025`、`A1-CDC-RABIES-LABORATORY-DIAGNOSIS-2024`。本区块用于公共卫生、诊断和生成安全边界；不把CDC内容外推为中国属地执法命令。

### 病原/病型定位

- 猪狂犬病页应作为“溢出感染/人兽共患暴露风险”实体使用，而非普通可经验治疗的猪病；暴露史、神经症状、犬/野生动物接触和人员接触风险是生成时的必问背景。`fact_id=V11-DIS-032-A1-cdc-rabies-veterinary-escalation; source_id=A1-CDC-RABIES-VETERINARIANS-2025; anchor=CDC rabies information for veterinarians`

### 监管/公共卫生边界

- 农业农村部公告第573号动物疫病名录列明狂犬病属于中国动物疫病名录管理对象；涉及中国上报、隔离、处置、调运或无害化时，必须回到A0文本和属地主管部门要求。`fact_id=V11-DIS-032-A0-rabies-catalog-class2; source_id=A0-MOA-573; anchor=一二三类动物疫病病种名录; 狂犬病`
- 疑似狂犬病动物涉及人兽共患和暴露风险，回答应要求联系公共卫生或动物卫生主管机构，不应建议非专业人员自行处置、采样、治疗或屠宰。`fact_id=V11-DIS-032-A1-cdc-rabies-veterinary-escalation; source_id=A1-CDC-RABIES-VETERINARIANS-2025`

### 实验室诊断

- 动物狂犬病不能凭临床表现确诊；确证需要由合格实验室对适当神经组织等样本进行狂犬病检测。`fact_id=V11-DIS-032-A1-cdc-rabies-lab-diagnosis; source_id=A1-CDC-RABIES-LABORATORY-DIAGNOSIS-2024; anchor=CDC rabies diagnostic testing`

### 鉴别诊断

- 神经症状病例应链接 [SYN-005-neurologic-signs](../syndromes/SYN-005-neurologic-signs.md) 和 [CMP-008](../comparisons/CMP-008-neurologic-signs.md)，并与伪狂犬病、脑炎、毒物、创伤、李斯特菌/链球菌脑膜炎等鉴别；有人暴露或犬/野生动物接触时，狂犬病风险必须升级处理。`fact_id=V11-DIS-032-A1-cdc-rabies-veterinary-escalation; source_id=A1-CDC-RABIES-VETERINARIANS-2025`

### 防控/用药/处置边界

- 本页不得生成抗菌药、镇静、疫苗或“观察后可上市/可屠宰”等执行性结论来替代公共卫生和动物卫生程序；疑似狂犬病的处置应先保护人员安全并联系主管机构。`source_id=A1-CDC-RABIES-VETERINARIANS-2025; source_id=RC-DISEASE-REGULATORY-001; source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001`

### Evidence gap

- 本轮未取得中国狂犬病动物处置细则或地方程序全文；中国执行层面的隔离、扑杀、检测流程、补偿、运输和食品链决定仍需A0/属地官方来源。
