---
tags: [syndrome, swine, v5]
syndrome_id: SYN-009-lameness-arthritis
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 跛行/关节肿胀

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪丹毒 -> `wiki/diseases/DIS-043-erysipelas.md`
- 猪链球菌病 -> `wiki/diseases/DIS-051-streptococcosis-streptococcus-suis.md`
- 副猪嗜血杆菌病 -> `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- 猪支原体肺炎 -> `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- 猪杂项细菌感染 -> `wiki/diseases/DIS-054-miscellaneous-bacterial-infections.md`

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

- 必问字段：日龄、关节肿胀/热痛、跛行部位、外伤/地面、发热、同窝同栏分布、蹄冠或水疱病变、近期断尾/阉割/注射；锚点：SRC-0066（PDF page 868-877）、SRC-0075/SRC-0076（PDF page 958-974）、RC-VES-001。
- 常见鉴别：链球菌、Glasser 病、猪丹毒、外伤/蹄病、营养或地面问题、水疱性疾病；锚点：RC-VES-001、SRC-0065、SRC-0066、SRC-0075/SRC-0076。
- 必须包含：检查是否有水疱/蹄冠病变，采样和培养/药敏边界，药物剂量拒答；锚点：RC-VES-001、RC-DX-001、RC-DRUG-001。
- 不得包含：未排除 FMD 等水疱病即按普通关节炎处理，或生成抗菌药剂量；锚点：RC-VES-001、RC-DRUG-001。

## V11 comparison expansion / 2026-05-08

- 本 syndrome 已新增高价值鉴别矩阵 [CMP-009](../comparisons/CMP-009-lameness-arthritis.md)；生成和评估时应优先召回该矩阵以约束最小诊断包、反证和高风险拒答边界。

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 风寒湿痹、关节肿胀、跛行与细菌性关节炎/外伤鉴别（pages=448,482）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
