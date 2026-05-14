---
tags: [disease, swine, cleaned_v13_2, partial_evidence_page]
disease_id: DIS-063
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: partial
usage_scope: [retrieval, regulatory_boundary, treatment_boundary, gap_routing]
sources: [SRC-0001, SRC-0082]
---

# 猪后圆线虫病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Partial page gap-routing / Phase 9

- RC-PARTIAL-GAP-ROUTING-001: This page is a controlled partial runtime page for recall, differential routing, and gap tracking.
- Missing facets must not be inferred, completed, or converted into diagnosis, treatment, dose, withdrawal-period, MRL, residue, or regulatory conclusions.
- If a requested answer depends on absent facets, route to higher-evidence disease pages, rule cards, source expansion, or current official/regulatory sources.
## Runtime disease guardrail anchors / Phase 5

- RC-PARTIAL-GAP-ROUTING-001: This page stays in partial retrieval mode for recall, differential routing, and gap tracking.
- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名
- Metastrongylus / lungworms

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 传播途径、临床症状、剖检变化、实验室诊断、鉴别诊断、防控要点
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类
- 初始分类：寄生虫/呼吸道病
- 教材章节：Section V Parasitic Diseases，Chapter 67
- 正文起始页：PDF page 1052

## 监管/执行性处置边界
- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。
## 典型宿主与阶段
- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。
## 用药/处置边界

- 待正文抽取和具体标签/等效来源复核；不以中国兽药来源作为唯一门槛。- 法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。
## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。
## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: retrieval, recall, differential routing, and gap tracking only; absent facets must not be inferred.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-063-metastrongylus-lungworms/001-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-063-metastrongylus-lungworms/002-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-063-metastrongylus-lungworms/003-DOS_1_200_REVIEW_REINFORCEMENT.md`：DOS_1_200_REVIEW_REINFORCEMENT；sources: SRC-0003, SRC-0007, SRC-0008, SRC-0009, SRC-0010, SRC-0011, SRC-0012, SRC-0014。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-063-metastrongylus-lungworms/004-Formal-Batch-029-V4.md`：Formal Batch 029 / V4 姝ｆ枃鎶藉彇杩涘睍；sources: SRC-0082。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-063-metastrongylus-lungworms/005-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: source anchors retained in expansion。
