---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-012-florfenicol
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, positive_drug_candidate, gap_routing, positive_label_candidate]
sources: [A0-MOA-ANNOUNCEMENT-1738-VET-DRUG-CANCELLATION-2012, A0-MOA-ANNOUNCEMENT-995-FLORFENICOL-2026, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-FLORFENICOL-INJECTION-219-2019, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-VET-DRUG-SUPERVISION-2026, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0069, SRC-0073, SRC-0075, SRC-0087, SRC-0088, SRC-0089, SRC-0090, SRC-0091]
candidate_source: issues/drug_pdf_candidate_extraction_2026-05-07.md
---

# Florfenicol / 氟苯尼考

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime core compaction / Phase 6

- Runtime role: compact drug boundary page for retrieval, source routing, and evaluation checks.
- Phase 6 moved high-density batch evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`.
- Moved fact-like rows: 46; moved source anchors: 46.
- `RC-DRUG-001`: Keep this page as a boundary and routing page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Expansion files under `wiki/evidence_expansions/drugs/phase6/` are for audit, source lookup, and manual review, not default production retrieval.

## 证据状态

- 使用范围：`positive_label_candidate`。
- 本页来自教材 PDF 候选抽取和有限权威来源入口整理，用于扩大 drug 检索覆盖面。
- 未完成具体标签、靶动物、剂型/途径、适应证、禁停用和药敏证据逐项复核前，不得生成执行性处方、剂量、疗程、休药期或法域合规承诺。

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=positive_label_candidate`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：A0-MOA-ANNOUNCEMENT-1738-VET-DRUG-CANCELLATION-2012, A0-MOA-ANNOUNCEMENT-995-FLORFENICOL-2026, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-FLORFENICOL-INJECTION-219-2019, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-VET-DRUG-SUPERVISION-2026, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0069, SRC-0073, SRC-0075, SRC-0087, SRC-0088, SRC-0089, SRC-0090；页码锚点：38；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：45 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=positive_label_candidate`，表示已存在可召回的具体标签或等效权威事实源；可用于正向用药答案，但只能限定在该来源覆盖的猪靶动物、制剂、途径、适应证、剂量/疗程、处方状态和休药期/MRL 范围内。
- 生成处方或评估答案时，可接受 `A0/A1/A2/SRC/RC/RULE` 任一类已锚定来源；不再要求必须是中国 A0/A1，但不得把一个法域、产品或制剂的证据外推到另一个法域、产品或制剂。
- 如果问题明确要求中国合规、当地出栏、残留合格或肉品可食，必须回到中国现行标签/标准/公告；否则应标注“仅限所引来源范围”。

## 药物类别

- phenicol

## MOA authority enrichment 2026-05-07

- 2026 年兽药质量监督抽检和风险监测计划将鸡蛋中酰胺醇类残留监测纳入附录，列明氟苯尼考 10 μg/kg，并按“氟苯尼考与氟苯尼考胺之和”判定；该来源用于残留监测边界，不提供猪用剂量或休药期。`source_id=A0-MOA-VET-DRUG-SUPERVISION-2026; attachment=raw/web/moa_batch_authority_pilot_20260507_v4/attachments/e7e51a2841db_P020260318598272942969.ofd`
- 同一计划的耐药性监测任务包括链球菌对氟苯尼考等 13 种抗菌药的耐药性监测；问答应优先提示病原诊断、药敏和合规标签复核。`source_id=A0-MOA-VET-DRUG-SUPERVISION-2026`
- 农业农村部公告第995号批准 TriRx 医药有限公司法国生产厂生产的氟苯尼考注射液在我国变更注册，并发布修订后的质量标准、说明书和标签；此前发布的该兽药质量标准、说明书和标签同时废止。`source_id=A0-MOA-ANNOUNCEMENT-995-FLORFENICOL-2026; attachment=raw/web/moa_batch_authority_pilot_20260507_v4/attachments/88a10c056e18_P020260330510774656990.ofd`
- 农业部公告第1738号注销部分企业兽药产品批准文号，官方发布页和附件可抽取到氟苯尼考粉注销记录；该证据仅用于注销记录边界，不代表所有同名产品当前状态。`source_id=A0-MOA-ANNOUNCEMENT-1738-VET-DRUG-CANCELLATION-2012; attachments=raw/web/moa_batch_authority_pilot_20260507_v4/attachments/3278b89cbaa1_P020120417395042903284.ceb;raw/web/moa_batch_authority_pilot_20260507_v4/attachments/fef330bef90c_P020120417395042435269.xls`

## 教材候选证据

- 教材候选表在 Chapter 10、放线杆菌病、支原体病、链球菌病和沙门氏菌病语境中命中 florfenicol。
- 候选页码：PDF page 185, 784, 893, 966。

## 疾病/用途候选

- 酰胺醇类抗菌候选；需要与氯霉素禁用边界区分，不能混同为同一合规状态。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-012-florfenicol/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-012-florfenicol/002-VTOP_V13_1.md`：VTOP_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-012-florfenicol/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-012-florfenicol/004-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-012-florfenicol/005-RAU_1_200_V14.md`：RAU_1_200_V14；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-012-florfenicol/006-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A0-MOA-FLORFENICOL-INJECTION-219-2019, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
