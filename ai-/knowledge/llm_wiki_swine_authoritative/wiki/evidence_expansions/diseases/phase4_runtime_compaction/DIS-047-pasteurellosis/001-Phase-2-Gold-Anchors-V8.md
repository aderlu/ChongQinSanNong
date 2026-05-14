---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-047-pasteurellosis.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-003-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0070]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-047-pasteurellosis / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- P. multocida 在猪中主要与进行性萎缩性鼻炎、肺炎型巴氏杆菌病和败血型巴氏杆菌病相关，临床解释需区分病型。 ($fact_id=PAST-001-disease-forms; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 908-909)

### 流行病学和传播边界

- 肺炎型 P. multocida 常作为其他呼吸道病原或综合征后的继发/终末阶段出现，单独检出不能自动解释为原发病因。 ($fact_id=PAST-003-pneumonic-secondary; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 909-912)
- 猪 P. multocida 流行病学尚不完全清楚，鼻腔/扁桃体定植与疾病发生之间需要结合宿主、环境和共同感染解释。 ($fact_id=PAST-004-epidemiology-uncertain; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 909-910)
- 肺炎型 P. multocida 通常需呼吸道防御受损或原发病原/环境因素参与，例如 M. hyopneumoniae、PRRSV、PCV2 或通风等背景。 ($fact_id=PAST-006-lung-defense-compromise; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 912)

### 临床症状

- 进行性萎缩性鼻炎临床表现可变，常围绕鼻腔病变、喷嚏/鼻部改变和生产性能影响解释，而非单一症状确诊。 ($fact_id=PAST-007-par-clinical; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 912-913)
- 败血型巴氏杆菌病通常突然发生，可表现为高热、严重呼吸困难、发绀和死亡等急性全身性表现。 ($fact_id=PAST-008-septicemic-clinical; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 913)

### 剖检变化

- 进行性萎缩性鼻炎肉眼病变主要限于鼻腔，可见鼻甲萎缩、鼻中隔偏曲或鼻腔改变，需与其他鼻炎原因鉴别。 ($fact_id=PAST-009-par-lesions; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 913-914)
- 肺炎型巴氏杆菌病可见前腹侧肺实变，常伴化脓性支气管肺炎，部分病例可有脓肿或胸膜炎。 ($fact_id=PAST-010-pneumonic-lesions; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 915)

### 实验室诊断

- 进行性萎缩性鼻炎确诊依赖临床/病理表现与产毒 P. multocida 的分离或确认，单靠典型临床模式只能作初步判断。 ($fact_id=PAST-011-par-definitive-diagnosis; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 916)
- P. multocida 相关肺病变并非特异性，需结合暴发史、组织病理、细菌培养和其他检测确认。 ($fact_id=PAST-012-lung-not-pathognomonic; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 916-917)
- 败血型巴氏杆菌病诊断依赖在血液或系统性组织中检出 P. multocida，并结合急性全身性病变解释。 ($fact_id=PAST-013-septicemic-diagnosis; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 917)

### 防控和用药边界

- 针对 PMT/产毒 P. multocida 的免疫可减轻或避免 PAR 相关病变，但具体产品和程序必须依赖本地标签与猪群背景。 ($fact_id=PAST-014-par-vaccine-protection; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 917-918)
- 教材认为猪肺炎型巴氏杆菌病疫苗控制效果总体存疑，不能把疫苗作为单独可靠控制承诺。 ($fact_id=PAST-015-pneumonic-vaccine-questionable; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 918)
- 肺炎型 P. multocida 常是其他呼吸道疾病的后续阶段，因此控制 M. hyopneumoniae 等原发病原通常是更有效的控制路径。 ($fact_id=PAST-016-control-primary-pathogens; source=SRC-0070; Chapter 57 Pasteurellosis; PDF page 919)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-003-respiratory-disease](../comparisons/CMP-003-respiratory-disease.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
