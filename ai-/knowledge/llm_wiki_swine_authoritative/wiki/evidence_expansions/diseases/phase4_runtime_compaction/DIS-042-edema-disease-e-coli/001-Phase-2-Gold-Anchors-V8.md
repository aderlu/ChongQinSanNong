---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-042-edema-disease-e-coli.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-002-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0063, SRC-0064]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-042-edema-disease-e-coli / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- 水肿病是 EDEC 在肠道定植后吸收 Stx2e 导致的毒血症，特定部位出现严重水肿。 ($fact_id=ECOLI-017-edema-disease; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 844)

### 流行病学和传播边界

- F18-STEC 与 F4-ETEC 混合感染时，临床上常以 F4-ETEC 腹泻为主，即使组织病理可见水肿病证据。 ($fact_id=ECOLI-004-pwd-mixed; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 834)
- F4ab/ac-ETEC 腹泻易感性与 MUC4 多态性相关，但 MUC4 与 F4 受体表达之间并非绝对对应。 ($fact_id=ECOLI-016-f4-receptor; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 843)

### 剖检变化

- 水肿病相关病变可包括血管内皮肿胀、内皮下纤维蛋白沉积、中膜坏死、血管周围水肿和微血栓。 ($fact_id=ECOLI-019-ed-lesions; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 846)

### 实验室诊断

- 水肿病病程较长时肠道细菌数量可能下降，因此细菌学阴性不能排除水肿病。 ($fact_id=ECOLI-020-ed-negative-culture; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 847)
- 溶血菌落常用于快速推定 ED 和 ETEC PWD，但会漏掉 EPEC 和日益增多的非溶血性 F4-ETEC。 ($fact_id=ECOLI-021-hemolysis-limit; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 847)

### 防控和用药边界

- 断奶舍应按全进全出管理，使用前彻底清除有机物并消毒，水线和供水系统也应消毒。 ($fact_id=ECOLI-022-aiao; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 848)
- 断奶仔猪管理应减少混群、受冷、运输和转栏等环境应激，并维持适宜、无贼风的环境。 ($fact_id=ECOLI-023-stress-temperature; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 848)
- 预防性饲料用抗菌药存在消费者不接受、免疫建立受损和耐药菌选择等严重缺点。 ($fact_id=ECOLI-024-antimicrobial-prophylaxis; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 849)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-002-post-weaning-diarrhea](../comparisons/CMP-002-post-weaning-diarrhea.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
