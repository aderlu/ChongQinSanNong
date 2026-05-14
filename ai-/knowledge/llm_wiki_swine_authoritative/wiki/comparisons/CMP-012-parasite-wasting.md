---
tags: [comparison, swine, v11]
comparison_id: CMP-012
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [A2-MERCK-ASCARIS-SUUM-PIGS-2024, A2-MERCK-COCCIDIOSIS-PIGS-2024, A2-MERCK-MANGE-PIGS-2026, DIS-055, DIS-057, DIS-060, DIS-061, DIS-063, DIS-064]
---

# 寄生虫/消瘦鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 消瘦、生长迟缓、饲料报酬下降、腹泻、咳嗽、肝乳斑、皮肤瘙痒或寄生虫卵检出时，按内外寄生虫、营养和慢性肠病分层。

## syndrome 链接

- 关联 syndrome: `SYN-011-poor-growth-wasting`

## 候选病种和支持线索

- 猪蛔虫：肝乳斑、肺移行病变和成虫影响增重；专利期粪检、未成熟期剖检。 (`V11-DIS-060-diagnosis`; `A2-MERCK-ASCARIS-SUUM-PIGS-2024`)
- 球虫病：仔猪腹泻、抗菌药无效和卵囊/组织学/PCR 支持。 (`V11-DIS-057-diagnosis`; `A2-MERCK-COCCIDIOSIS-PIGS-2024`)
- 疥螨：瘙痒、结痂、耳部病变和母猪至仔猪传播，长期影响生长。 (`V11-DIS-055-etiology`; `A2-MERCK-MANGE-PIGS-2026`)
- 鞭虫/肺虫/肾虫：需结合粪检、剖检部位和户外/垫料暴露史；不能由消瘦直接定因。 (`DIS-061`; `DIS-063`; `DIS-064`)

## 最小诊断包

- 分日龄粪便漂浮/虫卵计数、皮肤刮片、剖检肝肺肠肾、饲料营养审查和慢性肠道病原检测。

## 监管、用药和食品安全边界

- 本矩阵只用于鉴别诊断和生成/评估约束；不得生成剂量、疗程、休药期、MRL、残留合格、肉品可食、饲料放行、调运、扑杀、检疫或上报结论，除非另有精确 A0/A1 来源。 (`RC-DISEASE-REGULATORY-001`; `RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)

## 评估陷阱

- 把一次阴性粪检作为排除未成熟寄生虫感染。
- 生成驱虫药剂量/休药期而无具体标签。
- 忽略营养、慢性肠炎和管理因素。
