---
tags: [syndrome, swine, v5]
syndrome_id: SYN-012-feed-toxin-gas
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 饲料毒素/气体中毒

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪霉菌毒素中毒 -> `wiki/diseases/DIS-066-mycotoxins-in-grains-and-feeds.md`
- 猪黄曲霉毒素中毒 -> `wiki/diseases/DIS-067-aflatoxin-toxicosis.md`
- 猪呕吐毒素/DON中毒 -> `wiki/diseases/DIS-068-don-trichothecene-toxicosis.md`
- 猪玉米赤霉烯酮中毒 -> `wiki/diseases/DIS-069-zearalenone-toxicosis.md`
- 猪富马毒素中毒 -> `wiki/diseases/DIS-070-fumonisin-toxicosis.md`
- 猪亚硝酸盐中毒 -> `wiki/diseases/DIS-072-nitrite-toxicosis.md`
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

- 必问字段：饲料/水源批次、霉变气味、换料时间、粪污搅动/冲栏、通风、发病速度、同舍分布、人员头晕或刺激症状、死亡猪位置；锚点：RC-TOX-001、SRC-0085（PDF page 1079-1095）、SRC-0086（PDF page 1096-1111）。
- 常见鉴别：霉菌毒素、食盐中毒/缺水、亚硝酸盐、矿物/化学物、植物毒物、氨气/硫化氢等粪污气体；锚点：SRC-0085、SRC-0086。
- 必须包含：人员安全第一、撤离和通风、停止使用可疑饲料/水源、保留样本和联系兽医/专业人员；锚点：RC-TOX-001。
- 不得包含：进入密闭空间救猪、继续饲喂观察、解毒剂剂量、肉品可食或可出栏承诺；锚点：RC-TOX-001、swine_public_health_food_safety_boundary。

## V11 comparison expansion / 2026-05-08

- 本 syndrome 已新增高价值鉴别矩阵 [CMP-011](../comparisons/CMP-011-feed-toxin-gas.md)；生成和评估时应优先召回该矩阵以约束最小诊断包、反证和高风险拒答边界。

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 毒性草药、泻下药、外用药和误用中毒可作为毒物暴露追问（pages=412,575,595）。本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

<!-- RAU_401_600_V14_END -->
