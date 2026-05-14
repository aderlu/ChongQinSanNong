---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-001-, CMP-002-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0063, SRC-0064]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-041-neonatal-post-weaning-colibacillosis / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- ETEC 是猪中最重要的大肠杆菌致病型，可产生一种或多种肠毒素导致分泌性腹泻。 ($fact_id=ECOLI-003-etec; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 833)
- 断奶后腹泻最常由 ETEC 引起，也可由不具备经典 PWD/ED 毒力因子的 EPEC 引起。 ($fact_id=ECOLI-015-pwd; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 842)

### 流行病学和传播边界

- 环境温度低于 25°C 时，仔猪肠蠕动减弱，细菌和保护性抗体通过肠道延迟，可加重大肠杆菌腹泻。 ($fact_id=ECOLI-009-cold-stress; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 838)
- 肠道 E. coli 感染免疫主要为体液免疫，早期依赖母源初乳和乳源抗体，随后依赖局部肠道主动免疫。 ($fact_id=ECOLI-013-immunity; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 840)
- F4ab/ac-ETEC 腹泻易感性与 MUC4 多态性相关，但 MUC4 与 F4 受体表达之间并非绝对对应。 ($fact_id=ECOLI-016-f4-receptor; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 843)

### 临床症状

- F18-STEC 与 F4-ETEC 混合感染时，临床上常以 F4-ETEC 腹泻为主，即使组织病理可见水肿病证据。 ($fact_id=ECOLI-004-pwd-mixed; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 834)

### 剖检变化

- E. coli 断奶后腹泻死亡猪常严重脱水、眼窝凹陷，胃可因干料扩张，小肠扩张、轻度水肿和充血。 ($fact_id=ECOLI-018-pwd-lesions; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 845)

### 实验室诊断

- 溶血菌落常用于快速推定 ED 和 ETEC PWD，但会漏掉 EPEC 和日益增多的非溶血性 F4-ETEC。 ($fact_id=ECOLI-021-hemolysis-limit; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 847)

### 鉴别诊断

- 新生仔猪 ETEC 腹泻需与 C. difficile、C. perfringens A/C、TGEV、PEDV、轮状病毒、PRRSV 和较大日龄仔猪的 Isospora suis 鉴别。 ($fact_id=ECOLI-010-neonatal-differential; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 839)
- ETEC 通常产生碱性粪便，而 TGEV、PEDV、轮状病毒等吸收不良性腹泻产生酸性粪便；pH 只能辅助鉴别。 ($fact_id=ECOLI-011-fecal-ph; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 839)

### 防控和用药边界

- 断奶舍应按全进全出管理，使用前彻底清除有机物并消毒，水线和供水系统也应消毒。 ($fact_id=ECOLI-022-aiao; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 848)
- 断奶仔猪管理应减少混群、受冷、运输和转栏等环境应激，并维持适宜、无贼风的环境。 ($fact_id=ECOLI-023-stress-temperature; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 848)
- 预防性饲料用抗菌药存在消费者不接受、免疫建立受损和耐药菌选择等严重缺点。 ($fact_id=ECOLI-024-antimicrobial-prophylaxis; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 849)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-001-neonatal-diarrhea](../comparisons/CMP-001-neonatal-diarrhea.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-002-post-weaning-diarrhea](../comparisons/CMP-002-post-weaning-diarrhea.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
