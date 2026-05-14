---
tags: [syndrome, swine, v5]
syndrome_id: SYN-006-vesicular-disease
updated: 2026-05-07T20:30:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 水疱/口蹄部病变

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪口蹄疫 -> `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- 塞内卡病毒A感染 -> `wiki/diseases/DIS-027-senecavirus-a-picornaviruses.md`
- 猪水疱性口炎 -> `wiki/diseases/DIS-033-vesicular-stomatitis-viruses.md`
- 猪水疱病 -> 待 disease_index 补充

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

- 必问字段：水疱部位、蹄冠/口腔病变、跛行、发热、流涎、传播速度、调运/引种、是否已有实验室结果；锚点：RC-VES-001、A1-WOAH-FMD（URL https://www.woah.org/en/disease/foot-and-mouth-disease/）、A0-MOA-573。
- 常见鉴别：口蹄疫、猪水疱病、水疱性口炎、塞内卡病毒相关病变和非水疱性口炎/创伤；锚点：RC-VES-001。
- 必须包含：限制移动、采样检测、FMD 等一类病鉴别和监管来源引用；锚点：RC-VES-001、A0-MOA-573。
- 不得包含：按普通口炎治疗、不检测直接用药、忽略调运和报告风险；锚点：RC-VES-001、RC-DRUG-001。
