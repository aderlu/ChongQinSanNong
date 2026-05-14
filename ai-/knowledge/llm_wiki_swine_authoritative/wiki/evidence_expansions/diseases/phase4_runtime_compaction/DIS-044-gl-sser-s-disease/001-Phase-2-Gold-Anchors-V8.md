---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-044-gl-sser-s-disease.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-003-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0066]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-044-gl-sser-s-disease / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- H. parasuis 引起的格拉瑟病以纤维素性多浆膜炎和关节炎为特征。 ($fact_id=GLASS-001-relevance; source=SRC-0066; Chapter 54 Glasser disease; PDF page 868)
- H. parasuis 基因型和血清型之间没有直接关联，基因分型不能替代血清型解释。 ($fact_id=GLASS-002-genotype-serovar; source=SRC-0066; Chapter 54 Glasser disease; PDF page 869)

### 流行病学和传播边界

- 仔猪鼻黏膜定植时可受母源 IgM/IgG 保护，但保护主要针对母猪接触过的菌株。 ($fact_id=GLASS-003-maternal-immunity; source=SRC-0066; Chapter 54 Glasser disease; PDF page 870)
- 格拉瑟病可在母源免疫衰减、接触新菌株、断奶混群、引种、受冷、拥挤或共同感染时发生。 ($fact_id=GLASS-004-risk-2aee4f263dad2d98046bb67515e900c0; source=SRC-0066; Chapter 54 Glasser disease; PDF page 870)
- H. parasuis 感染与 PRRSV、PCV2、猪流感和 B. bronchiseptica 有流行病学或实验关联，可加重或改变疾病表现。 ($fact_id=GLASS-005-coinfection; source=SRC-0066; Chapter 54 Glasser disease; PDF page 871)

### 临床症状

- 急性格拉瑟病可见高热、咳嗽、腹式呼吸、关节肿胀跛行和侧卧、划水、震颤等中枢神经症状。 ($fact_id=GLASS-006-clinical; source=SRC-0066; Chapter 54 Glasser disease; PDF page 872)
- 超急性格拉瑟病病程短，可突然死亡且无特征性肉眼病变。 ($fact_id=GLASS-007-peracute; source=SRC-0066; Chapter 54 Glasser disease; PDF page 872)

### 剖检变化

- 典型格拉瑟病病理为纤维素性至纤维素脓性浆膜炎，可伴纤维素脓性脑膜炎。 ($fact_id=GLASS-008-lesions; source=SRC-0066; Chapter 54 Glasser disease; PDF page 873)

### 防控和用药边界

- 母源免疫可干扰仔猪 H. parasuis 疫苗接种后的抗体诱导，疫苗效果解释需结合暴发和免疫状态。 ($fact_id=GLASS-010-vaccine-maternal; source=SRC-0066; Chapter 54 Glasser disease; PDF page 875)
- H. parasuis 病常用抗生素防控，但减少群体性预防用药压力增加，应强调疫苗和管理策略边界。 ($fact_id=GLASS-011-antibiotic-boundary; source=SRC-0066; Chapter 54 Glasser disease; PDF page 875)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-003-respiratory-disease](../comparisons/CMP-003-respiratory-disease.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
