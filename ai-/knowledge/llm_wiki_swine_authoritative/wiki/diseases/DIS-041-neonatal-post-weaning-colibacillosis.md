---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-041
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-573, A0-MOA-THREE-CLASS-ANIMAL-DISEASE-SPECS, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0063, SRC-0064, SRC-0087, SRC-0089, SRC-0090]
---

# 仔猪黄白痢

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime low-risk cleanup / Phase 9

- Runtime role: compact disease page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`, `RAU_201_400_V14`, `RAU_401_600_V14`.
- Moved fact-like rows: 22; moved candidate facts: 4.
- Detailed evidence moved in Phase 9 is for audit, source lookup, manual review, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Neonatal/post-weaning colibacillosis

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- 猪大肠杆菌感染在商业养猪国家普遍存在，包括新生仔猪腹泻、断奶后腹泻、水肿病、系统感染、膀胱炎和尿路感染；传播栏目需结合不同致病型和日龄解释。`fact_id=ECOLI-007-epidemiology; source_id=SRC-0063; anchor=Chapter 52 Colibacillosis; PDF page 836`

### 临床症状

- ETEC 是猪中最重要的大肠杆菌致病型，可产生一种或多种肠毒素导致分泌性腹泻。`fact_id=ECOLI-003-etec; source_id=SRC-0063; anchor=Chapter 52 Colibacillosis; PDF page 833`

### 剖检变化

- E. coli 断奶后腹泻死亡猪常严重脱水、眼窝凹陷，胃可因干料扩张，小肠扩张、轻度水肿和充血。`fact_id=ECOLI-018-pwd-lesions; source_id=SRC-0064; anchor=Chapter 52 Colibacillosis; PDF page 845`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：细菌病/腹泻病
- 教材章节：Section IV Bacterial Diseases，Chapter 52
- 正文起始页：PDF page 831

## 监管/执行性处置边界

- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。
- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。
- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。

## 典型宿主与阶段

- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。

## 用药/处置边界

- 待正文抽取和具体标签/等效来源复核；不以中国兽药来源作为唯一门槛。
- 治疗相关回答必须同时满足病原/病变证据、兽医诊断、药敏或标签依据、具体产品说明书、处方药管理、休药期/MRL 和中国现行法规；不得从疾病页直接生成剂量、疗程或休药期。
- 法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。
- [A0-MOA-573](../sources/A0-MOA-573.md) - 中国一二三类动物疫病病种名录入口；用于分类核验，不得外推具体处置。
- [A0-MOA-THREE-CLASS-ANIMAL-DISEASE-SPECS](../sources/A0-MOA-THREE-CLASS-ANIMAL-DISEASE-SPECS.md) - 三类动物疫病防治规范；仅在疾病分类已被 A0 来源确认时用于报告、诊治和合规用药边界。
- [RC-DISEASE-REGULATORY-001](../rule_cards/RC-DISEASE-REGULATORY-001.md) - 中国动物疫病分类和处置不得外推。

## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: disease recall, evidence lookup, differential prompts, and boundary checks only; do not generate executable treatment, withdrawal-period, MRL, or regulatory conclusions without rule-card and source verification.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/004-RAU_1_200_V14.md`：RAU_1_200_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/005-RAU_201_400_V14.md`：RAU_201_400_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/006-RAU_401_600_V14.md`：RAU_401_600_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/007-Formal-Batch-023-V3.md`：Formal Batch 023 / V3 正文抽取进展；sources: SRC-0063。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/008-Formal-Batch-024-V3.md`：Formal Batch 024 / V3 正文抽取进展；sources: SRC-0064。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/009-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/010-B-task.md`：B-task 核心栏目补强；sources: SRC-0063, SRC-0064。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-041-neonatal-post-weaning-colibacillosis/001-Phase-2-Gold-Anchors-V8.md`：Phase 2 Gold Anchors / V8；sources: CMP-001-, CMP-002-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0063, SRC-0064。
