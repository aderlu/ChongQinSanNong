---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-001-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0037]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-008-porcine-epidemic-diarrhea-virus / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- PEDV 只感染猪，教材指出其没有已知公共卫生作用。 ($fact_id=PEDV-001-public-health; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 529)
- PEDV S INDEL 与非 S INDEL 毒株在田间和实验攻毒中可分别表现较轻或较重疾病；S 蛋白变化与致病性和交叉中和有关，但教材仍认为只有一个 PEDV 血清型。 ($fact_id=PEDV-002-s-indel-virulence-boundary; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 528-529)
- PEDV 与 TGEV 或 PDCoV 之间没有交叉中和；仅可见低度交叉反应性，不能把 TGEV/PDCoV 抗体解释为 PEDV 保护。 ($fact_id=PEDV-003-no-cross-neutralization; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 529)

### 流行病学和传播边界

- PEDV 可通过连续窝仔在断奶时失去泌乳免疫而形成感染循环并地方性存在；野猪检出 PEDV 后，其维持和传播作用仍不明确。 ($fact_id=PEDV-004-endemic-cycle-lactogenic-immunity; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 529)
- PED 的致病过程受感染日龄、病毒株毒力、接种途径和剂量影响。 ($fact_id=PEDV-005-pathogenesis-age-strain-route-dose; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 529)

### 临床症状

- PEDV 主要在小肠绒毛上皮细胞胞质内复制，造成肠细胞变性、绒毛高度降低和吸收不良。 ($fact_id=PEDV-006-villous-enterocyte-tropism; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 530)
- PED 与 TGE 共享水样腹泻、呕吐、厌食和沉郁等临床特征，繁殖场各年龄猪均可发病，仔猪发病率可接近 100%。 ($fact_id=PEDV-007-clinical-pattern; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 532)

### 实验室诊断

- PEDV 诊断应同时基于临床表现和实验室检测病毒 RNA、病毒抗原或抗体升高；RT-PCR/实时 RT-PCR 是常用 RNA 检测方法。 ($fact_id=PEDV-008-diagnosis-combined-clinical-lab; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 532)
- 使用 IF 或 IHC 直接示证 PEDV 抗原时，应优先选取腹泻初期、肠细胞脱落前急性处死猪的小肠组织。 ($fact_id=PEDV-009-acute-small-intestine-sampling; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 532)

### 防控和用药边界

- PEDV 编码多种干扰素拮抗蛋白；保护性免疫与肠黏膜分泌型 IgA 存在有关，但免疫可能并不持久。 ($fact_id=PEDV-010-ifn-evasion-and-siga; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 533)
- 母猪肠道免疫可诱导泌乳免疫，初乳/乳汁抗体对保护哺乳仔猪至关重要；所有猪只暴露于 PEDV 并不保证已形成保护性泌乳免疫。 ($fact_id=PEDV-011-lactogenic-immunity; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 533-534)
- PEDV 高度传染，预防病毒进入需严格卫生和生物安全；控制目标还包括促进母猪群形成泌乳免疫以降低哺乳仔猪风险。 ($fact_id=PEDV-012-control-biosecurity-sanitation; source=SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 534)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-001-neonatal-diarrhea](../comparisons/CMP-001-neonatal-diarrhea.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
