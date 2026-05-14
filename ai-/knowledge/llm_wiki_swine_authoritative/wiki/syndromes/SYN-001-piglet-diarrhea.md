---
tags: [syndrome, swine, v5]
syndrome_id: SYN-001-piglet-diarrhea
updated: 2026-05-07T20:30:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 仔猪腹泻

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪流行性腹泻 -> `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- 猪传染性胃肠炎 -> `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`
- 猪δ冠状病毒感染 -> `wiki/diseases/DIS-010-porcine-deltacoronavirus.md`
- 猪轮状病毒病 -> `wiki/diseases/DIS-030-rotaviruses-and-reoviruses.md`
- 仔猪黄白痢 -> `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- 仔猪梭菌性肠炎 -> `wiki/diseases/DIS-039-clostridial-diseases.md`
- 猪球虫病 -> `wiki/diseases/DIS-057-coccidia-and-other-protozoa.md`
- 猪隐孢子虫病 -> `wiki/diseases/DIS-059-cryptosporidiosis-protozoa.md`
- 猪类圆线虫病 -> `wiki/diseases/DIS-062-strongyloides-internal-parasites.md`

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

- 必问字段：日龄、窝/舍发病率、死亡率、粪便性状、呕吐和脱水、母猪免疫/泌乳、保温和卫生、近期换料或寄养；锚点：RC-DIARRHEA-001、SRC-0052（PDF page 739-751）、SRC-0063/SRC-0064（PDF page 831-858）、SRC-0081（PDF page 1039-1051）。
- 常见鉴别：PED/TGE/轮状病毒、大肠杆菌、梭菌性肠炎、球虫、隐孢子虫、低温和管理性腹泻；锚点：RC-DIARRHEA-001。
- 必须包含：分层鉴别、支持护理和采样检测建议、药物剂量拒答边界；锚点：RC-DIARRHEA-001、RC-DRUG-001。
- 不得包含：固定抗菌药/抗球虫药剂量、未核验休药期、单凭水样腹泻锁定单一病原；锚点：RC-DRUG-001、DRUG-006-anticoccidials。

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 腹泻/久泻/久痢/食积/收涩与清热燥湿边界（pages=407,426,438,506）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
