---
tags: [drug, swine, cleaned_v13_2, regulatory_boundary_page]
drug_id: DRUG-008-food-animal-banned-drug-list
updated: 2026-05-08T23:59:00+08:00
jurisdiction: China
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-BANNED-DRUG-250-POLICY]
---

# 食品动物禁用药清单

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

- 监管边界：`china_regulated`。
- `usage_scope=boundary_only` 表示本页可用于候选召回和边界判断；正向处方需另有具体标签或等效来源。
- `jurisdiction` 仅描述来源适用范围；生成答案时应按所引标签或事实源限定法域和产品范围。

## 药物知识页可用性

- 证据覆盖：regulatory_boundary_page；`source_trust=human_reviewed`；`usage_scope=boundary_only`。
- 可用边界：本页主要用于禁用、限用、监管和越界识别；不得作为正向处方来源。
- 来源覆盖：A0-MOA-BANNED-DRUG-250-POLICY；页码锚点：0；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：1 条。
- 本页用于阻断或限制越界用药；正向治疗方案必须转到具体药物页、产品标签、处方规则和当地法规来源。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 已核验证据

- 食品动物禁用药应以农业农村部公告第250号及官方清单为准；未核验具体清单原文前，不得编造禁用药条目。（`AUTH-017-food-animal-banned-drug-policy`; A0-MOA-BANNED-DRUG-250-POLICY; 农业农村部政策说明；公告第250号来源入口）
