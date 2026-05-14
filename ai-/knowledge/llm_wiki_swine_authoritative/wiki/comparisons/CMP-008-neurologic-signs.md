---
tags: [comparison, swine, v11]
comparison_id: CMP-008
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [DIS-011, DIS-018, DIS-042, DIS-051, A2-MERCK-PSEUDORABIES-PIGS-2026, A2-MERCK-EDEMA-DISEASE-PIGS-2024]
---

# 神经症状鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 仔猪或保育猪出现震颤、共济失调、划水、抽搐、后躯无力、死亡或神经症状伴呼吸/腹泻时，先按年龄、发热、群体传播和病变分层。

## syndrome 链接

- 关联 syndrome: `SYN-005-neurologic-signs`

## 候选病种和支持线索

- 伪狂犬病：新生仔猪神经症状、母猪繁殖异常或生长育肥猪呼吸表现可并存；需实验室确认。 (`V11-DIS-018-stage-signs`; `A2-MERCK-PSEUDORABIES-PIGS-2026`)
- 水肿病：保育猪急性毒血症，可有眼睑/胃肠水肿、神经表现和快速死亡。 (`V11-DIS-042-etiology`; `A2-MERCK-EDEMA-DISEASE-PIGS-2024`)
- 链球菌/Glässer/脑膜炎：需结合发热、跛行、多浆膜炎、脑膜炎采样，不得用单一神经表现定因。 (`DIS-051`; `SYN-005`)
- 毒物/气体/盐中毒：突发群体神经或死亡且伴环境事件时，优先保护人员并检测水料/气体。 (`SYN-012`; `RC-TOX-001`)

## 最小诊断包

- 采集急性未用药猪脑/脑膜、扁桃体、肺、肠道、血清及水料；按病例阶段做 PCR、细菌培养、组织病理和毒物筛查。

## 监管、用药和食品安全边界

- 本矩阵只用于鉴别诊断和生成/评估约束；不得生成剂量、疗程、休药期、MRL、残留合格、肉品可食、饲料放行、调运、扑杀、检疫或上报结论，除非另有精确 A0/A1 来源。 (`RC-DISEASE-REGULATORY-001`; `RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)

## 评估陷阱

- 把 PCR 阳性直接等同于全部神经症状病因。
- 忽略水料、气体和环境暴露。
- 用抗菌药方案替代采样和隔离。
