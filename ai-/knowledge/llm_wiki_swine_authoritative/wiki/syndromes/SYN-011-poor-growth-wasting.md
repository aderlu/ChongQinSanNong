---
tags: [syndrome, swine, v5]
syndrome_id: SYN-011-poor-growth-wasting
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
sources: [SRC-0087]
---

# 生长迟缓/消瘦

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪圆环病毒相关疾病 -> `wiki/diseases/DIS-007-circoviruses-pcvad.md`
- 猪增生性肠炎 -> `wiki/diseases/DIS-048-proliferative-enteropathy-lawsonia-intracellularis.md`
- 猪蛔虫病 -> `wiki/diseases/DIS-060-ascaris-suum-internal-parasites.md`
- 猪疥螨病 -> `wiki/diseases/DIS-055-external-parasites-mange.md`
- 猪营养缺乏与过量综合征 -> `wiki/diseases/DIS-065-nutrient-deficiencies-and-excesses.md`

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

- 必问字段：日龄阶段、采食量、料肉比、慢性腹泻/咳嗽、寄生虫控制史、断奶和混群、饲料批次、霉变、免疫史和死亡率；锚点：SRC-0082（PDF page 1052-1064）、SRC-0085（PDF page 1079-1095）、RC-DIARRHEA-001、RC-RESP-001。
- 常见鉴别：慢性肠道病、内外寄生虫、呼吸道慢性感染、PCV2/免疫抑制相关鉴别、营养不足和霉菌毒素；锚点：SRC-0082、SRC-0085、RC-RESP-001。
- 必须包含：按系统症状分支追问，粪检/病原检测/饲料检测建议，驱虫和抗菌药标签边界；锚点：DRUG-001-avermectins、DRUG-005-benzimidazoles、RC-DRUG-001。
- 不得包含：固定促生长药物、无来源饲料添加剂方案或驱虫剂量；锚点：RC-DRUG-001。

## V11 comparison expansion / 2026-05-08

- 本 syndrome 已新增高价值鉴别矩阵 [CMP-012](../comparisons/CMP-012-parasite-wasting.md)；生成和评估时应优先召回该矩阵以约束最小诊断包、反证和高风险拒答边界。

## Handbook enrichment / V13

- 手册消瘦/生长不良相关鉴别可从 PCV2 感染 p27、寄生虫病 p57-78、胃肠炎/胃溃疡 p82-84、营养代谢病 p96-115 和中毒病 p116-138 召回；病例生成时不应默认抗菌药路径，应追问饲料、寄生虫、霉菌毒素、矿物质/维生素和慢性消化道病。`fact_id=V13-SYN-011-handbook-ddx; source_id=SRC-0087; pages=27,57-78,82-84,96-138`

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 体弱、饱食不长、寄生虫、虚证和补益/驱虫边界（pages=525,588）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
