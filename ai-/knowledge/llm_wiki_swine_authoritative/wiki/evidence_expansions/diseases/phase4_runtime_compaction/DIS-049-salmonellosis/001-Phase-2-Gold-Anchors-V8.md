---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-049-salmonellosis.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-002-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0073]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-049-salmonellosis / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- S. Choleraesuis 具有猪适应性并常与败血型病相关；S. Typhimurium 和单相变异株等常与肠炎型病相关。 ($fact_id=SALM-004-serovar-host-pattern; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 936-938)
- 沙门氏菌侵袭肠上皮、诱导炎症和分泌反应是肠炎型沙门氏菌病腹泻和肠道病变的重要机制。 ($fact_id=SALM-005-enteric-pathogenesis; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 940-941)
- 败血型沙门氏菌病涉及全身播散、血管损伤和多器官病变，不能仅按普通腹泻病处理。 ($fact_id=SALM-006-septicemic-pathogenesis; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 941-943)

### 流行病学和传播边界

- 非伤寒沙门氏菌病是全球公共卫生问题，猪及猪肉可参与食物链风险，但具体食品安全执行和召回需本地法规来源。 ($fact_id=SALM-001-nontyphoidal-public-health; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 937)
- 猪沙门氏菌病暴发多见于集约化饲养的断奶和生长猪，常与应激、混群、运输、饲料变化或其他疾病背景相关。 ($fact_id=SALM-003-outbreak-intensive; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 938)

### 临床症状

- 肠炎型沙门氏菌病常见发热、沉郁和水样至黏液性或带血腹泻，慢性病例可有消瘦和持续肠道病变。 ($fact_id=SALM-007-clinical-enteric; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 941-942)
- S. Choleraesuis 败血型可表现为发热、发绀、呼吸或神经症状以及死亡，腹泻并非早期必有表现。 ($fact_id=SALM-008-septicemic-clinical; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 941)

### 剖检变化

- 肠炎型沙门氏菌病变常为纤维素坏死性肠炎/结肠炎，盲肠和结肠病变较稳定，可见假膜或纽扣样溃疡。 ($fact_id=SALM-009-enteric-lesions; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 942-944)
- 败血型沙门氏菌病可见脾大、肝大、淋巴结肿大、肺炎和多器官显微病变，需与经典猪瘟等急性败血性疾病鉴别。 ($fact_id=SALM-010-septicemic-lesions; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 943-944)

### 实验室诊断

- 临床表现和病变可支持沙门氏菌病初步诊断，但不足以确诊，需结合病原分离/检测和相符病变。 ($fact_id=SALM-011-presumptive-not-confirmed; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 944)
- 由于沙门氏菌感染和带菌广泛存在，单独从肠内容物或病变培养出沙门氏菌不能可靠诊断疾病，必须有相符病变支持。 ($fact_id=SALM-012-culture-alone-unreliable; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 945)
- PCR 检出沙门氏菌不等同于诊断沙门氏菌病，尤其在个体动物层面需要临床、病变和流行病学背景。 ($fact_id=SALM-013-pcr-detection-not-diagnosis; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 945)

### 防控和用药边界

- 沙门氏菌疫苗可降低疾病表现，但不能可靠防止感染或带菌，不能作为食品安全或清除承诺。 ($fact_id=SALM-014-vaccine-boundary; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 945-946)
- 沙门氏菌暴发控制目标是减少死亡、临床病和排菌，同时结合饲养管理、卫生、生物安全和其他疾病控制。 ($fact_id=SALM-015-control-goals; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 946-947)
- 肠炎型沙门氏菌抗菌药使用常见，但疗效、耐药和带菌影响需谨慎评估；不能生成通用处方。 ($fact_id=SALM-016-antimicrobial-boundary; source=SRC-0073; Chapter 59 Salmonellosis; PDF page 946)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-002-post-weaning-diarrhea](../comparisons/CMP-002-post-weaning-diarrhea.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
