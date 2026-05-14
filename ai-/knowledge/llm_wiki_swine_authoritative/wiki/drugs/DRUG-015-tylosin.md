---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-015-tylosin
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0059, SRC-0069, SRC-0071, SRC-0077, SRC-0088, SRC-0089, SRC-0090, SRC-0091]
candidate_source: issues/drug_pdf_candidate_extraction_2026-05-07.md
---

# Tylosin / 泰乐菌素

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime core compaction / Phase 6

- Runtime role: compact drug boundary page for retrieval, source routing, and evaluation checks.
- Phase 6 moved high-density batch evidence blocks out of default retrieval: `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`.
- Moved fact-like rows: 56; moved source anchors: 56.
- `RC-DRUG-001`: Keep this page as a boundary and routing page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Expansion files under `wiki/evidence_expansions/drugs/phase6/` are for audit, source lookup, and manual review, not default production retrieval.

## 证据状态

- 使用范围：`boundary_only`。
- 本页来自教材 PDF 候选抽取和有限权威来源入口整理，用于扩大 drug 检索覆盖面。
- 未完成具体标签、靶动物、剂型/途径、适应证、禁停用和药敏证据逐项复核前，不得生成执行性处方、剂量、疗程、休药期或法域合规承诺。

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=boundary_only`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0059, SRC-0069, SRC-0071, SRC-0077, SRC-0088, SRC-0089, SRC-0090；页码锚点：52；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：55 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 药物类别

- macrolide

## 教材候选证据

- 教材候选表在增生性肠炎、猪痢疾、Brachyspira 结肠炎、支原体病、萎缩性鼻炎和钩端螺旋体语境中命中 tylosin。
- 候选页码：PDF page 185, 784, 823, 884, 893, 931, 983, 984, 990, 1084, 1100。

## 疾病/用途候选

- 大环内酯类候选；必须保留耐药和标签复核边界。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-015-tylosin/001-VTOP_V13_1.md`：VTOP_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-015-tylosin/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-015-tylosin/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-015-tylosin/004-RAU_1_200_V14.md`：RAU_1_200_V14；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-015-tylosin/005-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-015-tylosin/001-Raw-MD-textbook-evidence-V12.md`：Raw MD textbook evidence / V12；sources: SRC-0012。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-015-tylosin/002-V12.md`：V12 生成与评估边界；sources: source anchors retained in expansion。
