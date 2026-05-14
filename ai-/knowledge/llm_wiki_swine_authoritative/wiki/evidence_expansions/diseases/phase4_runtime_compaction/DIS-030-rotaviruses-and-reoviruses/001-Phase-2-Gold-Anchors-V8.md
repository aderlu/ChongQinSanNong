---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-030-rotaviruses-and-reoviruses.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-001-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0052]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-030-rotaviruses-and-reoviruses / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- 轮状病毒属于 Reoviridae，具分节段双链 RNA，猪相关轮状病毒需按种和基因型解释，不能用单一血清型概括全部风险。 ($fact_id=ROTA-001-taxonomy; source=SRC-0052; Chapter 43 Reoviruses; PDF page 739-741)

### 流行病学和传播边界

- 轮状病毒环境稳定性高，完全干燥不能灭活所有病毒颗粒；清洁消毒策略需考虑环境持续污染。 ($fact_id=ROTA-002-environment; source=SRC-0052; Chapter 43 Reoviruses; PDF page 742)
- 卤素/氯类、酚类和戊二醛等消毒剂可帮助控制轮状病毒传播，但效果依赖持续、正确使用和有机物清除。 ($fact_id=ROTA-003-disinfection; source=SRC-0052; Chapter 43 Reoviruses; PDF page 742)

### 临床症状

- 轮状病毒腹泻的公认机制包括绒毛损失、吸收不足和吸收不良性腹泻，其他分泌性机制也可能参与。 ($fact_id=ROTA-004-pathogenesis; source=SRC-0052; Chapter 43 Reoviruses; PDF page 743)
- 轮状病毒主要影响新生仔猪，临床表现与其他肠道病原重叠，不能仅凭腹泻确诊。 ($fact_id=ROTA-005-clinical; source=SRC-0052; Chapter 43 Reoviruses; PDF page 744)

### 实验室诊断

- 轮状病毒诊断必须依赖实验室检测，临床症状和日龄只能提示纳入鉴别诊断。 ($fact_id=ROTA-006-diagnosis; source=SRC-0052; Chapter 43 Reoviruses; PDF page 744)

### 防控和用药边界

- 轮状病毒血清中和抗体水平并不是保护性免疫的良好指标，局部肠道免疫和母源免疫需要单独解释。 ($fact_id=ROTA-007-immunity; source=SRC-0052; Chapter 43 Reoviruses; PDF page 745)
- 轮状病毒腹泻治疗以支持疗法和减少脱水/继发问题为主，不得生成特异性抗病毒处方。 ($fact_id=ROTA-008-treatment; source=SRC-0052; Chapter 43 Reoviruses; PDF page 746)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-001-neonatal-diarrhea](../comparisons/CMP-001-neonatal-diarrhea.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
