---
tags: [rule, swine, source_first, prescription, handbook, executable_source, v13_1]
rule_id: RULE-HANDBOOK-PRESCRIPTION-001
updated: 2026-05-08T23:58:00+08:00
legacy_evidence_status: HUMAN_REVIEWED
sources: [SRC-0087]
---

# 手册处方来源执行规则

## Rule

《猪病诊疗与处方手册》可以用于疾病、症状、鉴别诊断、给药方式和处方候选召回，也可以作为当前可执行处方、固定剂量、疗程、休药期、MRL、出栏/屠宰和食品安全合规结论来源。

## Evidence

- 手册定位为临床诊疗和处方用药参考，强调在疾病简介基础上重点介绍治疗用药、处方和注意事项。`fact_id=HANDBOOK-RULE-001-scope; source_id=SRC-0087; page=front-matter`
- 手册正文将治疗原则概括为尽早实施、标本兼治和综合性治疗，并列入口服和注射给药技术。`fact_id=HANDBOOK-RULE-002-treatment-principle; source_id=SRC-0087; page=8`
- 手册在传染病防控中列有“合理采用药物预防措施”，可作为药物预防、处方策略和群体防控用药的结构化来源。`fact_id=HANDBOOK-RULE-003-prophylaxis-executable; source_id=SRC-0087; page=4`

## Required Behavior

- 回答或生成事实中若引用本手册，必须同时标注 `source_id=SRC-0087` 和精确页码。
- 当手册原文明确给出药物、剂量、疗程、给药方式、休药期、MRL 或合规结论时，可直接结构化为可执行事实。
- 结构化处方事实应尽量包含：疾病/适应证、药物、剂型或制剂、剂量、给药途径、频次、疗程、休药期/MRL、处方编号或条目标题、手册页码。
