---
tags: [drug, swine, cleaned_v13_2, partial_drug_evidence_page]
drug_id: DRUG-017-tulathromycin
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: partial
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-BANNED-DRUG-250-NOTICE, SRC-0012, SRC-0059, SRC-0070, SRC-0088]
candidate_source: issues/drug_pdf_candidate_extraction_2026-05-07.md
---

# Tulathromycin / 泰拉霉素

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Partial page gap-routing / Phase 9

- `RC-PARTIAL-GAP-ROUTING-001`: This page is a controlled partial runtime page for recall, differential routing, and gap tracking.
- Missing facets must not be inferred, completed, or converted into diagnosis, treatment, dose, withdrawal-period, MRL, residue, or regulatory conclusions.
- If a requested answer depends on absent facets, route to higher-evidence disease pages, rule cards, source expansion, or current official/regulatory sources.

## Runtime guardrail anchors / Phase 4

- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.

## 证据状态

- 使用范围：`boundary_only`。
- 本页来自教材 PDF 候选抽取和有限权威来源入口整理，用于扩大 drug 检索覆盖面。
- 未完成具体标签、靶动物、剂型/途径、适应证、禁停用和药敏证据逐项复核前，不得生成执行性处方、剂量、疗程、休药期或法域合规承诺。

## 药物知识页可用性

- 证据覆盖：partial_drug_evidence_page；`source_trust=needs_review`；`usage_scope=boundary_only`。
- 可用边界：本页只有部分来源锚定证据，可用于药物召回、边界提示和后续标签核验任务规划。
- 来源覆盖：A0-MOA-BANNED-DRUG-250-NOTICE, SRC-0012, SRC-0059, SRC-0070, SRC-0088；页码锚点：1；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：1 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 药物类别

- macrolide

## 教材候选证据

- 教材候选表在放线杆菌病、波氏杆菌/巴氏杆菌混合呼吸道病和巴氏杆菌肺炎语境中命中 tulathromycin。
- 候选页码：PDF page 185, 190, 784, 798, 918, 919。

## 疾病/用途候选

- 呼吸道病大环内酯候选；不得将美国标签直接转写为中国适应证。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-017-tulathromycin/001-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-017-tulathromycin/001-Raw-MD-textbook-evidence-V12.md`：Raw MD textbook evidence / V12；sources: SRC-0012。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-017-tulathromycin/002-V12.md`：V12 生成与评估边界；sources: source anchors retained in expansion。
