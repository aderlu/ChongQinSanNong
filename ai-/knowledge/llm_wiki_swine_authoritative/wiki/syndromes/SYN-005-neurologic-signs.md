---
tags: [syndrome, swine, v5]
syndrome_id: SYN-005-neurologic-signs
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 神经症状

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪伪狂犬病 -> `wiki/diseases/DIS-018-pseudorabies-aujeszky-disease.md`
- 猪乙型脑炎 -> `wiki/diseases/DIS-015-japanese-encephalitis-virus.md`
- 猪血凝性脑脊髓炎 -> `wiki/diseases/DIS-011-hemagglutinating-encephalomyelitis-virus.md`
- 仔猪水肿病 -> `wiki/diseases/DIS-042-edema-disease-e-coli.md`
- 猪链球菌病 -> `wiki/diseases/DIS-051-streptococcosis-streptococcus-suis.md`
- 猪狂犬病风险 -> `wiki/diseases/DIS-032-rabies-virus.md`

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

- 必问字段：日龄、发热、抽搐/转圈/共济失调、死亡速度、同窝/同舍分布、饮水中断、饲料/盐分变化、毒物暴露和人畜共患风险；锚点：SRC-0075/SRC-0076（PDF page 958-974）、SRC-0086（PDF page 1096-1111）、RC-DX-001。
- 常见鉴别：链球菌脑膜炎、Glasser 病、伪狂犬/疱疹病毒相关鉴别、猪瘟/瘟病毒鉴别、食盐中毒/缺水、霉菌毒素或化学毒物；锚点：RC-DX-001、RC-TOX-001。
- 必须包含：神经症状与毒物/水盐问题并列鉴别，建议保留脑组织/血清/饲料水样并由兽医送检；锚点：SRC-0086、RC-DX-001。
- 不得包含：仅凭神经症状给抗菌药或镇静药剂量，或忽略饮水/盐分和毒物线索；锚点：RC-DRUG-001、RC-TOX-001。

## V11 comparison expansion / 2026-05-08

- 本 syndrome 已新增高价值鉴别矩阵 [CMP-008](../comparisons/CMP-008-neurologic-signs.md)；生成和评估时应优先召回该矩阵以约束最小诊断包、反证和高风险拒答边界。

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 惊厥、抽搐、神昏和开窍/息风药只能作为鉴别提示，不能替代感染/中毒/缺氧排查（pages=562-587）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
