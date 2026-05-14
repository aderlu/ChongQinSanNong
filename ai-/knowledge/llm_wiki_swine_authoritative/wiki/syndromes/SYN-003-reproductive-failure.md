---
tags: [syndrome, swine, v5]
syndrome_id: SYN-003-reproductive-failure
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, syndrome_entrypoint]
---

# 繁殖障碍/流产

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 关联病种

- 猪繁殖与呼吸综合征 -> `wiki/diseases/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`
- 猪伪狂犬病 -> `wiki/diseases/DIS-018-pseudorabies-aujeszky-disease.md`
- 猪细小病毒病 -> `wiki/diseases/DIS-023-parvoviruses.md`
- 猪乙型脑炎 -> `wiki/diseases/DIS-015-japanese-encephalitis-virus.md`
- 猪布鲁氏菌病 -> `wiki/diseases/DIS-038-brucella-suis-brucellosis.md`
- 猪钩端螺旋体病 -> `wiki/diseases/DIS-045-leptospirosis.md`
- 猪玉米赤霉烯酮中毒 -> `wiki/diseases/DIS-069-zearalenone-toxicosis.md`

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

- 必问字段：妊娠日龄、流产/死胎/木乃伊胎/弱仔组合、母猪发热、胎次、批次分布、配种记录、疫苗史、引种、饲料霉变和样本保存；锚点：RC-REPRO-001、SRC-0045（PDF page 635-644）、SRC-0049/SRC-0050（PDF page 709-726）、SRC-0085（PDF page 1079-1095）。
- 常见鉴别：PRRS、细小病毒、伪狂犬/疱疹病毒相关鉴别、猪瘟/瘟病毒鉴别、布鲁氏菌、钩端螺旋体、霉菌毒素和管理应激；锚点：RC-REPRO-001。
- 必须包含：胎龄和胎儿类型推理、胎儿/胎盘/血清/饲料样本建议、公共卫生或监管线索触发；锚点：RC-REPRO-001、RC-DX-001、A0-MOA-573。
- 不得包含：保胎药、激素、抗菌药剂量，或只凭“流产”锁定单一病原；锚点：RC-DRUG-001、RC-REPRO-001。

## V11 comparison expansion / 2026-05-08

- 本 syndrome 已新增高价值鉴别矩阵 [CMP-013](../comparisons/CMP-013-sow-reproductive-lactation.md)；生成和评估时应优先召回该矩阵以约束最小诊断包、反证和高风险拒答边界。
