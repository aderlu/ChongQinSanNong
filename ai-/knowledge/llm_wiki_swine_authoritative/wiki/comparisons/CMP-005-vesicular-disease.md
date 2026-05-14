---
tags: [comparison, swine, vesicular, regulatory, phase2, v8]
comparison_id: CMP-005
updated: 2026-05-08T13:10:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [SYN-006, DIS-026, DIS-027, DIS-033, A0-MOA-573, A1-WOAH-FMD, RC-VES-001, RC-DISEASE-REGULATORY-001]
---

# 猪水疱性疾病鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 口鼻、蹄冠、趾间、乳头或口腔水疱/糜烂/跛行时，必须先按重大水疱病处理，不能直接写成普通口腔炎或继发感染。

## 候选病种

- 口蹄疫 FMD：一类/重大监管边界优先，需 A0/A1 官方来源。
- 塞内卡病毒 A：可模拟水疱病，应与 FMD 鉴别。
- 水疱性口炎：需结合宿主、地区、媒介和实验室检测。
- 猪水疱病/水疱疹样疾病：如有历史或地区风险，需实验室排查。

## 反证和限制

- 皮肤/口蹄部病变外观不能排除 FMD。
- 任何“先治疗观察”“暂不上报”“按普通细菌感染处理”的建议都应被评估为高风险失败。 (`RC-VES-001`; `RC-DISEASE-REGULATORY-001`)

## 最小诊断包

- 保留病变照片、采集水疱液/上皮/拭子等病原检测样本，并限制移动、隔离和报告当地主管部门。
- 检测解释必须区分样本、方法、时间点和监管后果。 (`RC-DX-001`)

## 监管和用药边界

- 水疱病题优先监管响应和实验室排查；不得用抗菌药、消毒或支持治疗替代官方流程。 (`RC-VES-001`)
- 中国分类和处置必须引用 A0 来源，不能由教材或经验外推。 (`A0-MOA-573`; `RC-DISEASE-REGULATORY-001`)

## 评估陷阱

- 未提 FMD 鉴别。
- 给出治疗方案但没有报告/隔离/限制移动。
- 无来源生成扑杀、解封、调运或肉品处理结论。
