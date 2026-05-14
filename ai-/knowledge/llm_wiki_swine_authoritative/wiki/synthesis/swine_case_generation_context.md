---
tags: [synthesis, swine, v5]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, dataset_generation_policy]
sources: [SRC-0001, A0-MOA-573, A0-MOA-ASF-NORMALIZED-GUIDE, A1-WOAH-ASF, RC-CITATION-001, RC-SYNTHESIS-SCOPE-001, RC-EVAL-RUBRIC-001, RC-REGULATORY-CURRENT-001]
---

# 猪病病例生成上下文

## Status model and guardrails

- `RC-SYNTHESIS-SCOPE-001`: Synthesis pages may combine rules and retrieval policy, but must not create new disease, drug, dose, withdrawal, MRL, residue, or regulatory facts.
- `RC-REGULATORY-CURRENT-001`: Reporting, quarantine, culling, movement control, inspection, banned-drug, withdrawal-period, MRL, residue, edible-product, and jurisdiction-specific compliance conclusions require current official/regulatory sources.
- `RC-EVAL-RUBRIC-001`: Evaluation rubrics and blocking rules are for scoring, routing, refusal, or source escalation; they are not standalone factual evidence.
- `RC-DRUG-001`: Drug, dose, route, course, compatibility, contraindication, or prescription content must be resolved through drug pages, source expansion, and label/regulatory verification.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, and food-safety claims require current label/regulatory verification.

## 系统用途

病例生成必须优先使用 disease 页面、syndrome 页面和 source/fact/rule 锚点清晰的 facts；不得生成无来源处方、休药期、扑杀、检疫或公共卫生执行细则。所有样本必须遵守 `RC-CITATION-001`。

## 强制边界

- 仅使用 `source_status=source_anchored` 且 `fact_validity=valid` 的 facts 和有来源锚点页面。
- 禁用药、剂量、休药期、检疫、扑杀、食品处理和公共卫生暴露处置必须要求可追溯来源；来源可以是 A0/A1/A2/SRC/RC/RULE，涉及特定法域合规时必须使用该法域来源。

## 推荐检索顺序

1. `rule_cards`
2. `syndromes`
3. `diseases`
4. `rules`
5. `sources`
6. `knowledge_facts.json`

## V6 生成/评估临时取用策略

- 本轮按用户要求，生成和评估暂不区分 `HUMAN_REVIEWED` 与 `NEEDS_REVIEW`。
- 可直接使用的最低门槛调整为：事实或页面必须有明确 `evidence_source_id`、来源页、URL 或 PDF page 锚点。
- 没有来源锚点的内容仍不得作为生成或评估结论。
- 处方、剂量、休药期、食品处理、扑杀、检疫和公共卫生执行细则必须有可追溯权威来源；涉及特定法域合规时必须使用对应法域来源。

## 500 条数据生成入口

- 生成器应优先读取 `swine_500_dataset_generation_evaluation_plan` 的主题配额，再进入对应 `rule_cards` 和 `syndromes`；结论锚点：swine_500_dataset_generation_evaluation_plan。
- 每条样本必须保存 `required_fields`、`differentials`、`must_include`、`must_not_include`、`evidence_anchors` 五类元数据；结论锚点：各 SYN 页面 V6 数据生成字段。
- 每条样本至少包含 1 个明确证据锚点；监管、药物和食品安全题必须包含 A0/A1 或 rule_card 锚点；结论锚点：A0-MOA-573、A0-MOA-BANNED-DRUG-250-POLICY、RC-DRUG-001。
- 药物题只生成用途边界、禁用/休药期边界、可用于题型和拒答逻辑，不生成具体处方剂量；结论锚点：DRUG-001 至 DRUG-008、RC-DRUG-001。
