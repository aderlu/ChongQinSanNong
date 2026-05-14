---
tags: [comparison, swine, v11]
comparison_id: CMP-011
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [A2-MERCK-MYCOTOXICOSES-OVERVIEW-2025, A2-MERCK-AFLATOXICOSIS-ANIMALS-2025, A2-FDA-CHEMICAL-CONTAMINANTS-ANIMAL-FOOD-2026, A2-ISU-SWINE-TOXICOSES-2026, DIS-066, DIS-067, DIS-068, DIS-069, DIS-070, DIS-073]
---

# 毒物/饲料/气体中毒鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 同栏或多栏突然采食下降、呕吐、繁殖异常、肺水肿、神经症状、死亡或粪沟/通风事件时，先按饲料批次、水源和环境暴露追踪。

## syndrome 链接

- 关联 syndrome: `SYN-012-feed-toxin-gas`

## 候选病种和支持线索

- DON/呕吐毒素：采食下降和呕吐更突出；常规吸附剂不应默认有效。 (`A2-MERCK-MYCOTOXICOSES-OVERVIEW-2025`; `DIS-068`)
- 玉米赤霉烯酮：雌激素样表现和母猪/后备繁殖异常突出。 (`A2-MERCK-MYCOTOXICOSES-OVERVIEW-2025`; `DIS-069`)
- 富马毒素：FDA 动物食品资料将猪肺水肿列为相关危害方向。 (`A2-FDA-CHEMICAL-CONTAMINANTS-ANIMAL-FOOD-2026`; `DIS-070`)
- 硫化氢/通风失败：粪沟搅动、密闭空间和人员风险是首要边界，应先撤离人员和动物。 (`A2-ISU-SWINE-TOXICOSES-2026`; `RC-TOX-001`)

## 最小诊断包

- 保留同批饲料、水样、原料、死猪组织、肺/肝/胃内容物和环境事件时间线；做毒素谱、硝酸盐/亚硝酸盐、气体和霉菌检测。

## 监管、用药和食品安全边界

- 本矩阵只用于鉴别诊断和生成/评估约束；不得生成剂量、疗程、休药期、MRL、残留合格、肉品可食、饲料放行、调运、扑杀、检疫或上报结论，除非另有精确 A0/A1 来源。 (`RC-DISEASE-REGULATORY-001`; `RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)

## 评估陷阱

- 把所有霉菌毒素统一写成一种治疗或吸附剂方案。
- 在气体事件中让人员先进入粪沟救猪。
- 未检测饲料就宣称肉品、饲料或猪只可安全放行。
