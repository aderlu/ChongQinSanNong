---
tags: [syndrome, swine, v5]
syndrome_id: SYN-004-respiratory-syndrome
updated: 2026-05-07T20:30:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
sources: [SRC-0087]
---

# 呼吸道综合征

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪流感 -> `wiki/diseases/DIS-021-influenza-viruses.md`
- 猪支原体肺炎 -> `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- 猪胸膜肺炎 -> `wiki/diseases/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md`
- 猪萎缩性鼻炎 -> `wiki/diseases/DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md`
- 猪多杀性巴氏杆菌病 -> `wiki/diseases/DIS-047-pasteurellosis.md`
- 猪繁殖与呼吸综合征 -> `wiki/diseases/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`
- 猪后圆线虫病 -> `wiki/diseases/DIS-063-metastrongylus-lungworms.md`

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

- 必问字段：猪群阶段、发热比例、咳嗽/喘气模式、死亡率、混群/引种、免疫史、通风、氨味/粪污操作、近期天气和人员安全；锚点：RC-RESP-001、SRC-0042/SRC-0043（PDF page 600-617）、SRC-0049/SRC-0050（PDF page 709-726）、SRC-0086（PDF page 1096-1111）。
- 常见鉴别：流感、PRRS、支原体肺炎、胸膜肺炎、巴氏杆菌、波氏杆菌、Glasser 病、环境性刺激和气体中毒；锚点：RC-RESP-001。
- 必须包含：感染与环境并列鉴别、采样检测、急性气体暴露时人员撤离和通风优先；锚点：RC-RESP-001、RC-TOX-001。
- 不得包含：默认抗菌药方案、无诊断群体投药、让人员进入粪沟/密闭空间；锚点：RC-DRUG-001、RC-TOX-001。

## Handbook enrichment / V13

- 手册呼吸相关鉴别覆盖猪流感 p21、PRRS p20、萎缩性鼻炎 p37、传染性胸膜肺炎 p38、猪肺疫 p42、支原体肺炎 p53、支气管肺炎 p86、纤维素性肺炎 p88 和支气管炎 p89；呼吸综合征生成应并列考虑原发病毒、细菌继发、支原体、胸膜肺炎样病变和普通内科呼吸病。`fact_id=V13-SYN-004-handbook-ddx; source_id=SRC-0087; pages=20,21,37,38,42,53,86,88,89`

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 咳嗽、喘息、寒痰/热痰、肺虚久咳和化痰止咳边界（pages=506-524）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
