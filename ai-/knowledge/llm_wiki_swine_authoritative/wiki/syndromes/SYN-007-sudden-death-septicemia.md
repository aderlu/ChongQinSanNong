---
tags: [syndrome, swine, v5]
syndrome_id: SYN-007-sudden-death-septicemia
updated: 2026-05-07T20:30:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 突然死亡/败血症

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 非洲猪瘟 -> `wiki/diseases/DIS-002-african-swine-fever-virus.md`
- 猪瘟 -> `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- 猪丹毒 -> `wiki/diseases/DIS-043-erysipelas.md`
- 猪链球菌病 -> `wiki/diseases/DIS-051-streptococcosis-streptococcus-suis.md`
- 猪沙门氏菌病 -> `wiki/diseases/DIS-049-salmonellosis.md`
- 猪放线杆菌败血症 -> `wiki/diseases/DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md`
- 猪胸膜肺炎 -> `wiki/diseases/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md`

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

- 必问字段：死亡速度、体温、皮肤发绀/出血、同群发病率、剖检所见、近期调运、饲料/水源、粪污操作和是否伴随人员不适；锚点：RC-ASF-001、RC-TOX-001、SRC-0065（PDF page 859-867）、SRC-0073（PDF page 936-949）、SRC-0086（PDF page 1096-1111）。
- 常见鉴别：ASF、猪丹毒、沙门氏菌败血症、链球菌、胸膜肺炎急性死亡、毒物/气体暴露；锚点：RC-ASF-001、RC-TOX-001。
- 必须包含：高死亡率/高热/ASF 线索硬触发报告，急性气体暴露先保护人员，建议剖检和实验室送检；锚点：RC-ASF-001、RC-TOX-001、RC-DX-001。
- 不得包含：用抗生素治疗替代 ASF 报告，或让人员进入疑似有毒气体现场；锚点：RC-ASF-001、RC-DRUG-001、RC-TOX-001。
