---
tags: [synthesis, swine, v5]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, regulatory_blocking_policy]
sources: [SRC-0001, A0-MOA-573, A0-MOA-ASF-NORMALIZED-GUIDE, A1-WOAH-ASF, RC-CITATION-001, RC-DISEASE-REGULATORY-001, RC-REGULATORY-CURRENT-001, RC-SYNTHESIS-SCOPE-001, RC-EVAL-RUBRIC-001]
---

# 中国监管硬阻断规则

## Status model and guardrails

- `RC-SYNTHESIS-SCOPE-001`: Synthesis pages may combine rules and retrieval policy, but must not create new disease, drug, dose, withdrawal, MRL, residue, or regulatory facts.
- `RC-REGULATORY-CURRENT-001`: Reporting, quarantine, culling, movement control, inspection, banned-drug, withdrawal-period, MRL, residue, edible-product, and jurisdiction-specific compliance conclusions require current official/regulatory sources.
- `RC-EVAL-RUBRIC-001`: Evaluation rubrics and blocking rules are for scoring, routing, refusal, or source escalation; they are not standalone factual evidence.
- `RC-DRUG-001`: Drug, dose, route, course, compatibility, contraindication, or prescription content must be resolved through drug pages, source expansion, and label/regulatory verification.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, and food-safety claims require current label/regulatory verification.

## 系统用途

一类动物疫病、水疱病变、ASF 阳性、禁用药和无 A0/标签级等价来源的休药期、MRL、残留、食品安全或监管执行结论必须触发硬阻断或要求权威来源。所有判断必须保留 `RC-CITATION-001` 要求的 source/fact/rule 锚点。

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
