---
tags: [comparison, swine, v11]
comparison_id: CMP-009
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [A2-MERCK-LAMENESS-NURSERY-PIGS-2026, A2-MERCK-LAMENESS-BREEDING-PIGS-2026, A2-MERCK-ERYSIPELAS-SWINE-2026, DIS-044, DIS-051]
---

# 跛行/关节炎鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 3-10 周龄保育猪多发跛行、关节肿胀或僵硬，以及后备/母猪跛行、蹄裂、淘汰升高时，必须分年龄和系统性表现。

## syndrome 链接

- 关联 syndrome: `SYN-009-lameness-arthritis`

## 候选病种和支持线索

- 保育猪多发性关节炎：常见 S. suis、Glaesserella parasuis、Mycoplasma hyorhinis 等，应与脑膜炎/败血症一起评估。 (`A2-MERCK-LAMENESS-NURSERY-PIGS-2026`)
- 丹毒：慢性丹毒常导致关节炎和跛行；急性丹毒还可有发热和菱形皮肤病变。 (`V11-DIS-043-clinical`; `A2-MERCK-ERYSIPELAS-SWINE-2026`)
- 后备/母猪结构性跛行：骨软骨病、退行性关节病、腿弱和蹄病需要与感染性关节炎分开。 (`A2-MERCK-LAMENESS-BREEDING-PIGS-2026`)
- 创伤/栏舍因素：湿滑地面、混群打斗、蹄裂和体况问题不能被病原检测掩盖。

## 最小诊断包

- 按日龄分组采关节液、滑膜、脑膜/浆膜、血液和病变蹄部；做细菌培养/PCR、药敏、组织病理和栏舍地面/混群检查。

## 监管、用药和食品安全边界

- 本矩阵只用于鉴别诊断和生成/评估约束；不得生成剂量、疗程、休药期、MRL、残留合格、肉品可食、饲料放行、调运、扑杀、检疫或上报结论，除非另有精确 A0/A1 来源。 (`RC-DISEASE-REGULATORY-001`; `RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)

## 评估陷阱

- 把跛行默认等同于丹毒。
- 未做关节液或滑膜采样就生成抗菌药疗程。
- 忽略后备母猪结构性和蹄部原因。
