---
tags: [drug, swine, emergency, anaphylaxis, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-080-epinephrine
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, evidence_linked_candidate]
sources: [SRC-0090, SRC-0092]
---

# Epinephrine / 肾上腺素

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime guardrail anchors / Phase 4

- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=evidence_linked_candidate`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：SRC-0090；页码锚点：8；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：8 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## Evidence Status

- This page was created to host swine vaccine-anaphylaxis emergency treatment facts extracted from `SRC-0090`.
- Use boundary: emergency dose and route statements must preserve the source page citation and should be checked against current local practice guidance before operational use.

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-080-epinephrine/001-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: SRC-0090。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-080-epinephrine/002-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-080-epinephrine/003-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
