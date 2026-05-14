---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-040-colibacillosis.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-001-, CMP-002-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0063, SRC-0064]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-040-colibacillosis / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- 猪大肠杆菌病长期存在，母猪疫苗可控制新生仔猪腹泻的一部分，但不能保护断奶后腹泻和水肿病。 ($fact_id=ECOLI-001-relevance; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 831)
- ETEC 是猪中最重要的大肠杆菌致病型，可产生一种或多种肠毒素导致分泌性腹泻。 ($fact_id=ECOLI-003-etec; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 833)
- ExPEC 正常栖息于肠道，但可侵入、造成菌血症、败血症或脑膜炎/关节炎等局部肠外感染。 ($fact_id=ECOLI-005-expec; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 835)

### 流行病学和传播边界

- 猪大肠杆菌感染在商业养猪国家普遍存在，包括新生仔猪腹泻、断奶后腹泻、水肿病、系统感染、膀胱炎和尿路感染。 ($fact_id=ECOLI-007-epidemiology; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 836)
- 并非所有猪都有 F4 上皮细胞受体，因此部分猪对 F4-ETEC 感染有遗传抗性。 ($fact_id=ECOLI-008-f4-genetic; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 837)
- 肠道 E. coli 感染免疫主要为体液免疫，早期依赖母源初乳和乳源抗体，随后依赖局部肠道主动免疫。 ($fact_id=ECOLI-013-immunity; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 840)

### 实验室诊断

- PCR 可用于在福尔马林固定、石蜡包埋组织中检测致病性 E. coli。 ($fact_id=ECOLI-012-pcr-in-situ; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 840)
- 溶血菌落常用于快速推定 ED 和 ETEC PWD，但会漏掉 EPEC 和日益增多的非溶血性 F4-ETEC。 ($fact_id=ECOLI-021-hemolysis-limit; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 847)
- 诊断大肠杆菌菌血症需要阳性血培养证据，采血应无菌并接种需氧和厌氧血培养瓶。 ($fact_id=ECOLI-029-blood-culture; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 852)

### 鉴别诊断

- 新生仔猪 ETEC 腹泻需与 C. difficile、C. perfringens A/C、TGEV、PEDV、轮状病毒、PRRSV 和较大日龄仔猪的 Isospora suis 鉴别。 ($fact_id=ECOLI-010-neonatal-differential; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 839)
- ETEC 通常产生碱性粪便，而 TGEV、PEDV、轮状病毒等吸收不良性腹泻产生酸性粪便；pH 只能辅助鉴别。 ($fact_id=ECOLI-011-fecal-ph; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 839)

### 防控和用药边界

- 常用母猪疫苗含 F4/F5/F6/F41 等抗原并用于新生仔猪腹泻控制，但不能覆盖所有断奶后腹泻或水肿病风险。 ($fact_id=ECOLI-014-vaccine-boundary; source=SRC-0063; Chapter 52 Colibacillosis; PDF page 841)
- 预防性饲料用抗菌药存在消费者不接受、免疫建立受损和耐药菌选择等严重缺点。 ($fact_id=ECOLI-024-antimicrobial-prophylaxis; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 849)
- 猪源大肠杆菌黏菌素耐药近年在全球多地增加，相关用药和公共卫生解释需谨慎。 ($fact_id=ECOLI-025-colistin; source=SRC-0064; Chapter 52 Colibacillosis; PDF page 849)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-001-neonatal-diarrhea](../comparisons/CMP-001-neonatal-diarrhea.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-002-post-weaning-diarrhea](../comparisons/CMP-002-post-weaning-diarrhea.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
