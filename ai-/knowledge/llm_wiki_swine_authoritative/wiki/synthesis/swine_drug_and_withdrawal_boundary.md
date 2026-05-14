---
tags: [synthesis, swine, drug, withdrawal, source_first, v11_1]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, boundary_policy]
sources: [RC-DRUG-001, RC-WITHDRAWAL-MRL-001, RC-DRUG-GOLD-ROLE-001, RC-CITATION-001, RC-DISEASE-REGULATORY-001, RC-REGULATORY-CURRENT-001, RC-SYNTHESIS-SCOPE-001, RC-EVAL-RUBRIC-001]
---

# 猪病用药和休药期 source-first 边界

## Status model and guardrails

- `RC-SYNTHESIS-SCOPE-001`: Synthesis pages may combine rules and retrieval policy, but must not create new disease, drug, dose, withdrawal, MRL, residue, or regulatory facts.
- `RC-REGULATORY-CURRENT-001`: Reporting, quarantine, culling, movement control, inspection, banned-drug, withdrawal-period, MRL, residue, edible-product, and jurisdiction-specific compliance conclusions require current official/regulatory sources.
- `RC-EVAL-RUBRIC-001`: Evaluation rubrics and blocking rules are for scoring, routing, refusal, or source escalation; they are not standalone factual evidence.
- `RC-DRUG-001`: Drug, dose, route, course, compatibility, contraindication, or prescription content must be resolved through drug pages, source expansion, and label/regulatory verification.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, and food-safety claims require current label/regulatory verification.

## 系统用途

本页定义药物、处方、休药期、MRL、残留和食品安全答案的证据门槛。V11.1 后不再把中国 A0/A1 作为唯一可用来源；任何可追溯且未待审的 `A0/A1/A2/SRC/RC/RULE` 证据，均可用于生成和评估，但不得超出来源自身覆盖的法域、靶动物、产品、剂型、途径和适应证。

## 可用来源

- `A0-*`、`A1-*`、`A2-*`、`SRC-*`、`RC-*`、`RULE-*` 均可作为猪病诊断、治疗候选、处方边界和评估证据。
- 每条可评分结论必须能回到 source page、URL、PDF page、标签页、fact_id 或 rule_card。
- `NEEDS_REVIEW` 仅用于召回和待核验提示，不作为最终处方或休药期结论的唯一来源。

## 处方生成门槛

- 正向处方或治疗方案必须同时核验：猪靶动物、具体药物/产品、剂型、给药途径、适应证、剂量/疗程、处方状态、休药期/MRL/残留边界、禁用/停用状态。
- 药物类别页、教材候选命中、处方药目录命中、同类药、其他动物标签、人医语境或公共卫生语境不能单独升级为执行性处方。
- `positive_label_candidate` 可在其精确来源范围内生成限定性正向答案；`boundary_only` 只能生成追问、拒答、核验路径和风险边界；`negative_trap` 用于评估错误外推。

## 休药期和 MRL

- 休药期、肉品可食、残留合格和 MRL 数值必须精确到具体来源条款；来源可以是 A0/A1/A2/SRC/RC/RULE，但必须覆盖对应产品、动物种属、组织/食品类别和适用条件。
- 如果来源只证明“存在标签候选”或“处方药管理状态”，不得推出休药期、残留合格或可出栏结论。
- 当用户明确询问特定法域合规或本地执行，必须使用该法域的现行官方或等效权威来源；若来源来自其他法域，应标注“仅限所引来源法域”。
