---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-049
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A2-MERCK-SALMONELLOSIS-ANIMALS-2026, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0073, SRC-0087, SRC-0088, SRC-0089, SRC-0090]
---

# 猪沙门氏菌病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime low-risk cleanup / Phase 9

- Runtime role: compact disease page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`, `RAU_201_400_V14`, `RAU_401_600_V14`.
- Moved fact-like rows: 22; moved candidate facts: 5.
- Detailed evidence moved in Phase 9 is for audit, source lookup, manual review, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Salmonellosis

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- 猪沙门氏菌病暴发多见于集约化饲养的断奶和生长猪，常与应激、混群、运输、饲料变化或其他疾病背景相关。（SRC-0073; Chapter 59 Salmonellosis; PDF page 938）

- 猪沙门氏菌病暴发多见于集约化饲养的断奶和生长猪，常与应激、混群、运输、饲料变化或其他疾病背景相关。`fact_id=SALM-003-outbreak-intensive; source_id=SRC-0073; anchor=Chapter 59 Salmonellosis; PDF page 938`

### 临床症状

- 肠炎型沙门氏菌病常见发热、沉郁和水样至黏液性或带血腹泻，慢性病例可有消瘦和持续肠道病变。`fact_id=SALM-007-clinical-enteric; source_id=SRC-0073; anchor=Chapter 59 Salmonellosis; PDF page 941-942`
- S. Choleraesuis 败血型可表现为发热、发绀、呼吸或神经症状以及死亡，腹泻并非早期必有表现。`fact_id=SALM-008-septicemic-clinical; source_id=SRC-0073; anchor=Chapter 59 Salmonellosis; PDF page 941`

### 剖检变化

- 肠炎型沙门氏菌病变常为纤维素坏死性肠炎/结肠炎，盲肠和结肠病变较稳定，可见假膜或纽扣样溃疡。`fact_id=SALM-009-enteric-lesions; source_id=SRC-0073; anchor=Chapter 59 Salmonellosis; PDF page 942-944`
- 败血型沙门氏菌病可见脾大、肝大、淋巴结肿大、肺炎和多器官显微病变，需与经典猪瘟等急性败血性疾病鉴别。`fact_id=SALM-010-septicemic-lesions; source_id=SRC-0073; anchor=Chapter 59 Salmonellosis; PDF page 943-944`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：细菌病/肠道病/败血症
- 教材章节：Section IV Bacterial Diseases，Chapter 59
- 正文起始页：PDF page 936

## 监管/执行性处置边界

- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。
- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。
- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。

## 典型宿主与阶段

- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。

## 用药/处置边界

- 待正文抽取和具体标签/等效来源复核；不以中国兽药来源作为唯一门槛。
- 法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。

## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: disease recall, evidence lookup, differential prompts, and boundary checks only; do not generate executable treatment, withdrawal-period, MRL, or regulatory conclusions without rule-card and source verification.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/002-VTOP_V13_1.md`：VTOP_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/004-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/005-RAU_1_200_V14.md`：RAU_1_200_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/006-RAU_201_400_V14.md`：RAU_201_400_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/007-RAU_401_600_V14.md`：RAU_401_600_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/008-Formal-Batch-026-V4.md`：Formal Batch 026 / V4 正文抽取进展；sources: SRC-0073。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/009-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: SRC-0073。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/010-B-task.md`：B-task 核心栏目补强；sources: SRC-0073。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/011-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A2-MERCK-SALMONELLOSIS-ANIMALS-2026, CMP-002, CMP-002-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-002-。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-049-salmonellosis/001-Phase-2-Gold-Anchors-V8.md`：Phase 2 Gold Anchors / V8；sources: CMP-002-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0073。
