---
tags: [comparison, swine, v11]
comparison_id: CMP-013
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [A2-MERCK-ABORTION-PIGS-2026, A2-MERCK-PDS-MASTITIS-SOWS-2026, A2-MERCK-PRRS-2026, DIS-015, DIS-023, DIS-028, DIS-045, DIS-069]
---

# 母猪繁殖/泌乳异常鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 返情、流产、死胎、木乃伊胎、弱仔、产后无乳/少乳、母猪发热或仔猪饥饿叫时，先按妊娠阶段、胎儿谱和产后泌乳状态分流。

## syndrome 链接

- 关联 syndrome: `SYN-003-reproductive-failure`

## 候选病种和支持线索

- PRRS：繁殖失败可伴死胎、木乃伊胎、早产和弱仔，并与呼吸综合征并行。 (`V11-DIS-028-clinical`; `A2-MERCK-PRRS-2026`)
- PPV/JEV/钩端螺旋体：按妊娠阶段、胎儿谱、母猪临床表现和血清学/病原检测区分。 (`DIS-015`; `DIS-023`; `DIS-045`)
- 玉米赤霉烯酮：雌激素样繁殖异常需结合饲料批次和毒素检测。 (`CMP-011`; `DIS-069`)
- 产后泌乳障碍/PDS：需区分真正乳房炎、子宫炎、膀胱炎、发热性疾病、仔猪吮乳不足和管理/水料问题。 (`A2-MERCK-PDS-MASTITIS-SOWS-2026`)

## 最小诊断包

- 记录配种日期、妊娠日龄、胎儿谱、母猪体温/乳房/阴门分泌物、仔猪胃乳充盈；采胎儿/胎盘、血清、乳汁/乳房样本、尿液和饲料。

## 监管、用药和食品安全边界

- 本矩阵只用于鉴别诊断和生成/评估约束；不得生成剂量、疗程、休药期、MRL、残留合格、肉品可食、饲料放行、调运、扑杀、检疫或上报结论，除非另有精确 A0/A1 来源。 (`RC-DISEASE-REGULATORY-001`; `RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)

## 评估陷阱

- 把流产默认归因 PRRS。
- 把少乳直接写成乳房炎并生成抗菌药。
- 未按妊娠阶段解释死胎、木乃伊胎和返情。
