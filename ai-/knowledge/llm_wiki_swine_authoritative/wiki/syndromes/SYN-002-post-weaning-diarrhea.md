---
tags: [syndrome, swine, v5]
syndrome_id: SYN-002-post-weaning-diarrhea
updated: 2026-05-07T20:30:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
sources: [SRC-0087]
---

# 断奶后腹泻

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 仔猪黄白痢 -> `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- 仔猪水肿病 -> `wiki/diseases/DIS-042-edema-disease-e-coli.md`
- 猪沙门氏菌病 -> `wiki/diseases/DIS-049-salmonellosis.md`
- 猪痢疾 -> `wiki/diseases/DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md`
- 猪增生性肠炎 -> `wiki/diseases/DIS-048-proliferative-enteropathy-lawsonia-intracellularis.md`
- 猪鞭虫病 -> `wiki/diseases/DIS-061-trichuris-suis-internal-parasites.md`

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

- 必问字段：断奶日龄、断奶后第几天、采食量、饲料更换、混群/转栏、粪便是否带血或黏液、发热和死亡率；锚点：RC-DIARRHEA-001、SRC-0063/SRC-0064（PDF page 831-858）、SRC-0071/SRC-0072（PDF page 922-935）、SRC-0077（PDF page 975-994）。
- 常见鉴别：断奶后大肠杆菌病、沙门氏菌、增生性肠病、猪痢疾、球虫/寄生虫、饲料或水质问题；锚点：RC-DIARRHEA-001。
- 必须包含：按病程和粪便性状提出鉴别，建议粪便/肠道样本和必要时药敏，不把药敏结果自动转为剂量；锚点：RC-DX-001、RC-DRUG-001。
- 不得包含：群体经验性投药、固定促生长或抗菌方案、无来源的休药期；锚点：RC-DRUG-001。

## Handbook enrichment / V13

- 手册腹泻相关鉴别覆盖轮状病毒病 p16、传染性胃肠炎 p17、流行性腹泻 p22、大肠杆菌病 p29、沙门氏菌病 p35、增生性肠炎 p46、梭菌性肠炎 p48、寄生虫病 p57-78、胃肠炎 p82 和中毒病 p116-138；断奶后腹泻问诊应同时覆盖日龄、断奶、饲料/水源、发热、血便/黏液和群体用药史。`fact_id=V13-SYN-002-handbook-ddx; source_id=SRC-0087; pages=16-138`

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 断奶后腹泻应并列病原、饲料、应激和寄生虫；中药消导/收涩只能作为支持候选（pages=407,426,588）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
