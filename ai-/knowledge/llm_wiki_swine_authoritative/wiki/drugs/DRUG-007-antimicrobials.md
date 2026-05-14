---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-007-antimicrobials
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-BANNED-DRUG-250-POLICY, RULE-HANDBOOK-PRESCRIPTION-001, SRC-0057, SRC-0087, SRC-0092]
---

# Antimicrobials / 抗菌药

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime guardrail anchors / Phase 4

- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.

## 证据状态

- 使用范围：`boundary_only`。
- `usage_scope=boundary_only` 表示本页可用于候选召回和边界判断；正向处方需另有具体标签或等效来源。
- `jurisdiction` 仅描述来源适用范围；生成答案时应按所引标签或事实源限定法域和产品范围。

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=boundary_only`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：A0-MOA-BANNED-DRUG-250-POLICY, RULE-HANDBOOK-PRESCRIPTION-001, SRC-0057, SRC-0087；页码锚点：0；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：0 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 已核验证据

- 当前仅建立药物类别占位页；需后续从教材 facts 或 A0/A1 标签/公告补充。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-007-antimicrobials/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-007-antimicrobials/002-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-007-antimicrobials/003-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-007-antimicrobials/001-Handbook-prescription-evidence-V13.md`：Handbook prescription evidence / V13；sources: RULE-HANDBOOK-PRESCRIPTION-001, SRC-0087。
