---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-055-external-parasites-mange.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-007-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0080]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-055-external-parasites-mange / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- 猪疥螨病是全球最重要的猪外寄生虫病，可降低生长速度、饲料效率和繁殖母猪受胎/繁殖表现。 ($fact_id=PARA-001-sarcoptic-mange-importance; source=SRC-0080; Chapter 65 External Parasites; PDF page 1029)
- 猪疥螨病由 Sarcoptes scabiei var. suis 引起，虫体宿主适应性强，主要来源为带虫猪。 ($fact_id=PARA-002-sarcoptes-host-specific; source=SRC-0080; Chapter 65 External Parasites; PDF page 1029)
- 雌虫在表皮上部掘隧道产卵，幼虫、若虫和成虫均在皮肤上完成生活史，约 10-15 天形成成虫。 ($fact_id=PARA-003-sarcoptes-life-cycle; source=SRC-0080; Chapter 65 External Parasites; PDF page 1029-1030)

### 临床症状

- 猪疥螨病可表现为螨数量少但过敏反应强的瘙痒型，也可表现为多见于成年猪的角化过度型。 ($fact_id=PARA-004-mange-clinical-forms; source=SRC-0080; Chapter 65 External Parasites; PDF page 1030-1031)
- 猪疥螨病可见瘙痒、丘疹、红斑、结痂和角化过度，成年猪耳部和体侧病变常有提示意义。 ($fact_id=PARA-005-mange-lesions; source=SRC-0080; Chapter 65 External Parasites; PDF page 1030-1031)
- 猪疥螨病通常不致死，但可使生长猪生长速度和饲料效率下降，并导致胴体降级或修割。 ($fact_id=PARA-009-mange-economic-effect; source=SRC-0080; Chapter 65 External Parasites; PDF page 1033)

### 实验室诊断

- 猪疥螨病确诊依赖检出螨或虫卵，但皮肤刮片可能假阴性，需结合群体病史和病变解释。 ($fact_id=PARA-006-mange-diagnosis; source=SRC-0080; Chapter 65 External Parasites; PDF page 1031)

### 防控和用药边界

- 建立无疥螨猪群依赖仔猪出生时无螨、有效杀螨药和防止引入带虫猪的生物安全。 ($fact_id=PARA-007-mange-elimination; source=SRC-0080; Chapter 65 External Parasites; PDF page 1032)
- 教材外寄生虫药物表用于说明标签适应范围，不得直接转写为通用处方、剂量、疗程或中国休药期。 ($fact_id=PARA-008-mange-products-boundary; source=SRC-0080; Chapter 65 External Parasites; PDF page 1032)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-007-skin-pruritus-crusts](../comparisons/CMP-007-skin-pruritus-crusts.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
