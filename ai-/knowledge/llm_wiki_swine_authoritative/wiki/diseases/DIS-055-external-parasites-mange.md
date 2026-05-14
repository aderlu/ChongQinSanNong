---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-055
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A2-MERCK-MANGE-PIGS-2026, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0020, SRC-0080, SRC-0088, SRC-0089, SRC-0090]
---

# 猪疥螨病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime low-risk cleanup / Phase 9

- Runtime role: compact disease page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`, `RAU_201_400_V14`, `RAU_401_600_V14`.
- Moved fact-like rows: 16; moved candidate facts: 5.
- Detailed evidence moved in Phase 9 is for audit, source lookup, manual review, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- External parasites / mange

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- 猪疥螨病由 Sarcoptes scabiei var. suis 引起，虫体宿主适应性强，主要来源为带虫猪。（SRC-0080; Chapter 65 External Parasites; PDF page 1029）
- 建立无疥螨猪群依赖仔猪出生时无螨、有效杀螨药和防止引入带虫猪的生物安全。（SRC-0080; Chapter 65 External Parasites; PDF page 1032）

### 临床症状

- 猪疥螨病是全球最重要的猪外寄生虫病，可降低生长速度、饲料效率和繁殖母猪受胎/繁殖表现。（SRC-0080; Chapter 65 External Parasites; PDF page 1029）
- 猪疥螨病可表现为螨数量少但过敏反应强的瘙痒型，也可表现为多见于成年猪的角化过度型。（SRC-0080; Chapter 65 External Parasites; PDF page 1030-1031）
- 猪疥螨病通常不致死，但可使生长猪生长速度和饲料效率下降，并导致胴体降级或修割。（SRC-0080; Chapter 65 External Parasites; PDF page 1033）

### 剖检变化

- 疥螨接触后约 3 周先在耳、眼、鼻周形成结痂，随后可在臀部、胁部和腹部出现与超敏反应相关的红色丘疹和瘙痒。（SRC-0020; Chapter 17 Integumentary System; PDF page 326）
- 猪疥螨病可见瘙痒、丘疹、红斑、结痂和角化过度，成年猪耳部和体侧病变常有提示意义。（SRC-0080; Chapter 65 External Parasites; PDF page 1030-1031）

### 实验室诊断

- 猪疥螨病确诊依赖检出螨或虫卵，但皮肤刮片可能假阴性，需结合群体病史和病变解释。（SRC-0080; Chapter 65 External Parasites; PDF page 1031）

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：寄生虫病/皮肤病
- 教材章节：Section V Parasitic Diseases，Chapter 65
- 正文起始页：PDF page 1029

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/001-VTOP_V13_1.md`：VTOP_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/004-RAU_1_200_V14.md`：RAU_1_200_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/005-RAU_201_400_V14.md`：RAU_201_400_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/006-RAU_401_600_V14.md`：RAU_401_600_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/007-Formal-Batch-029-V4.md`：Formal Batch 029 / V4 正文抽取进展；sources: SRC-0080。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/008-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: SRC-0020, SRC-0080。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/009-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A2-MERCK-MANGE-PIGS-2026, CMP-007, CMP-007-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-008-。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-055-external-parasites-mange/001-Phase-2-Gold-Anchors-V8.md`：Phase 2 Gold Anchors / V8；sources: CMP-007-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0080。
