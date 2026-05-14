---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-023
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-573, SRC-0001, SRC-0045, SRC-0089]
---

# 猪细小病毒病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Parvoviruses

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- PPV1 致病机制与到达并跨越胎盘屏障、感染胚胎/胎儿有关；传播栏目应突出繁殖/胎盘感染边界，并结合妊娠阶段解释。`fact_id=PPV-005-pathogenesis; source_id=SRC-0045; anchor=Chapter 38 Parvoviruses opening; PDF page 638-640`

### 临床症状

- PPV1 是猪繁殖损失的明确病因之一，典型问题集中在胚胎和胎儿感染相关损失。`fact_id=PPV-002-ppv1-reproductive; source_id=SRC-0045; anchor=Chapter 38 Parvoviruses opening; PDF page 635 and 639`
- PPV1 通常不导致成年猪明显临床症状，除繁殖损失外不得把成年猪非特异症状直接归因于 PPV1。`fact_id=PPV-006-adult-clinical-boundary; source_id=SRC-0045; anchor=Chapter 38 Parvoviruses opening; PDF page 639-641`

### 剖检变化

- 当前可用事实支持胚胎/胎儿感染相关损失这一方向，但未提供足够稳定的剖检病变清单；需结合妊娠阶段继续抽取。`fact_id=PPV-005-pathogenesis; source_id=SRC-0045; anchor=Chapter 38 Parvoviruses opening; PDF page 638-640`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：病毒病/繁殖障碍
- 教材章节：Section III Viral Diseases，Chapter 38
- 正文起始页：PDF page 635

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-023-parvoviruses/001-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-023-parvoviruses/002-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-023-parvoviruses/003-Formal-Batch-018.md`：Formal Batch 018 正文抽取进展；sources: SRC-0045。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-023-parvoviruses/004-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: A0-MOA-573。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-023-parvoviruses/005-B-task.md`：B-task 核心栏目补强；sources: SRC-0045。
