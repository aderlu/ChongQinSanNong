---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-039-clostridial-diseases.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-001-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0062]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-039-clostridial-diseases / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- 猪梭菌病主要涉及 C. perfringens type C、C. difficile、C. septicum、C. perfringens type A、C. tetani、C. botulinum 等。 ($fact_id=CLOST-001-agents; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 816)
- CPB 毒素被确认为 C. perfringens type C 的主要毒力因子，且对胰蛋白酶敏感。 ($fact_id=CLOST-003-typec-cpb; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 818)

### 流行病学和传播边界

- 当母猪形成免疫并通过乳汁提供保护性免疫后，C. perfringens type C 可转为地方性，非免疫母猪窝仔猪风险最高。 ($fact_id=CLOST-002-typec-endemic; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 817)
- 新生动物肠道胰蛋白酶水平低和/或摄入胰蛋白酶抑制物是 type C 疾病发病的重要基础。 ($fact_id=CLOST-004-typec-neonatal-risk; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 818)
- C. difficile 可在出生后很早出现在仔猪肠内容物中，到产后 3 天可全部阳性，随日龄增长流行率下降。 ($fact_id=CLOST-008-cdifficile-colonization; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 822)

### 实验室诊断

- 培养后用多重 PCR 检测主要毒素基因几乎是判定 C. perfringens 类型的通用方法。 ($fact_id=CLOST-005-typec-genotyping; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 820)
- C. difficile TcdA/TcdB 检出必须结合相容临床表现和剖检结果解释，因为正常仔猪肠道也可不一致检出毒素。 ($fact_id=CLOST-009-cdifficile-diagnosis; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 823)
- 由于健康仔猪肠道中 C. difficile 流行率较高，单纯培养诊断意义有限。 ($fact_id=CLOST-010-cdifficile-culture; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 823)

### 防控和用药边界

- C. perfringens type C 出现临床症状后治疗价值有限，预防优先；不得把抗毒素或抗菌药写成通用救治保证。 ($fact_id=CLOST-006-typec-treatment; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 820)
- 破伤风和肉毒中毒属于神经毒性梭菌病，教材指出两者均非人兽共患病。 ($fact_id=CLOST-013-neurotoxigenic; source=SRC-0062; Chapter 51 Clostridial Diseases; PDF page 826)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-001-neonatal-diarrhea](../comparisons/CMP-001-neonatal-diarrhea.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
