---
tags: [syndrome, swine, v5]
syndrome_id: SYN-008-skin-pruritus-crusts
updated: 2026-05-07T20:30:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 皮肤瘙痒/结痂

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪疥螨病 -> `wiki/diseases/DIS-055-external-parasites-mange.md`
- 猪虱病 -> `wiki/diseases/DIS-056-external-parasites-lice.md`
- 猪痘 -> `wiki/diseases/DIS-029-swinepox-virus.md`
- 猪葡萄球菌病 -> `wiki/diseases/DIS-050-staphylococcosis-exudative-epidermitis.md`
- 猪丹毒 -> `wiki/diseases/DIS-043-erysipelas.md`

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

- 必问字段：瘙痒程度、结痂部位、耳缘/背部/腹部病变、同群传播、引种、接触性皮炎线索、是否伴发消瘦或继发感染；锚点：SRC-0080（External Parasites; PDF page 1027-1038）、RC-DX-001。
- 常见鉴别：疥螨、虱、皮肤真菌/细菌继发感染、猪痘、营养或环境刺激、药物/消毒剂接触性损伤；锚点：SRC-0080、SRC-0051（PDF page 733-738）。
- 必须包含：皮肤刮片/病料检查、全群管理和环境控制边界、驱虫药标签核验；锚点：SRC-0080、DRUG-001-avermectins、RC-DRUG-001。
- 不得包含：直接给阿维菌素/伊维菌素剂量和休药期，或仅凭瘙痒锁定疥螨；锚点：DRUG-001-avermectins、DRUG-002-ivermectin、RC-DRUG-001。

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 疥癣、湿疹、皮肤湿热、外用杀虫解毒边界（pages=588-600）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
