---
tags: [drug, swine, cleaned_v13_2, source_anchored_drug_evidence_page]
drug_id: DRUG-038-trimethoprim-sulfadiazine
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-BANNED-DRUG-250-NOTICE, SRC-0012, SRC-0091]
candidate_source: subagent_pdf_candidate_scan_2026-05-07
---

# Trimethoprim + sulfadiazine / 甲氧苄啶-磺胺嘧啶

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime guardrail anchors / Phase 4

- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.

## 证据状态

- 使用范围：`boundary_only`。
- 本页来自 Diseases of Swine 11e PDF 二次候选抽取，用于补齐被药物大类吞掉的具体药物名。
- 未完成中国批准产品、禁限用、停用/淘汰、残留限量、说明书和休药期复核前，不得生成处方、剂量、疗程或特定法域合规承诺。

## 药物知识页可用性

- 证据覆盖：partial_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=boundary_only`。
- 可用边界：本页只有部分来源锚定证据，可用于药物召回、边界提示和后续标签核验任务规划。
- 来源覆盖：A0-MOA-BANNED-DRUG-250-NOTICE, SRC-0012；页码锚点：1；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：0 条。
- 页面不具备可执行处方条件；不得从药物名、类别或教材候选外推出剂量、疗程、休药期、MRL 或食品安全结论。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 药物类别

- potentiated sulfonamide

## 教材候选证据

- 候选页码：PDF page 787, 947。
- PDF 语境：Actinobacillus suis 和沙门氏菌病参考语境。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-038-trimethoprim-sulfadiazine/001-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
