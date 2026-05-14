---
tags: [syndrome, swine, v5]
syndrome_id: SYN-010-anemia-jaundice
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 贫血/黄疸

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪钩端螺旋体病 -> `wiki/diseases/DIS-045-leptospirosis.md`
- 猪霉菌毒素中毒 -> `wiki/diseases/DIS-066-mycotoxins-in-grains-and-feeds.md`
- 猪矿物质与化学物中毒 -> `wiki/diseases/DIS-071-toxic-minerals-chemicals-plants-and-gases.md`
- 猪有毒气体与通风失败损伤 -> `wiki/diseases/DIS-073-toxic-gases-ventilation-failure.md`

## 必问病史

- 日龄/阶段、发病率、死亡率、免疫史、引种/混群、饲料或环境变化。
- 是否存在高风险监管触发词：高死亡率、水疱、神经症状、繁殖障碍、人兽共患暴露。

## 必查证据

- 优先从 `diseases`、`rules`、`rule_cards`、`sources` 检索 HUMAN_REVIEWED 内容。
- 未命中 A0/A1 中国监管或药物来源时，不得生成监管处置、剂量、疗程或休药期。

## 系统评估要点

- 生成答案应列鉴别诊断和采样/检测边界。
- 涉及一类动物疫病、禁用药、食品安全和公共卫生时，必须触发 rule_cards。

## V6 数据生成字段

- 必问字段：日龄、贫血/黄疸出现速度、血尿/黑便、寄生虫暴露、饲料霉变、铁补充史、死亡率和剖检所见；锚点：SRC-0082（PDF page 1052-1064）、SRC-0085（PDF page 1079-1095）、SRC-0086（PDF page 1096-1111）。
- 常见鉴别：营养性贫血、寄生虫、溶血/中毒、肝炎相关鉴别、败血症和饲料毒素；锚点：SRC-0040（PDF page 568-571）、SRC-0082、SRC-0085、SRC-0086。
- 必须包含：血液/粪便/饲料水源样本建议，食品安全和药物残留边界；锚点：RC-DX-001、swine_public_health_food_safety_boundary、RC-DRUG-001。
- 不得包含：无诊断铁剂/驱虫/抗菌药剂量，或承诺肉品安全；锚点：RC-DRUG-001、RC-TOX-001。

## V11 comparison expansion / 2026-05-08

- 本 syndrome 已新增高价值鉴别矩阵 [CMP-010](../comparisons/CMP-010-anemia-jaundice.md)；生成和评估时应优先召回该矩阵以约束最小诊断包、反证和高风险拒答边界。

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 出血、血虚、止血和补血边界；不得跳过病因检查（pages=466,525）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
