---
tags: [rule_card, swine, drug, dataset, gold_generation, source_first, v11_1]
card_id: RC-DRUG-GOLD-ROLE-001
updated: 2026-05-08T23:59:00+08:00
severity: critical
jurisdiction: Global
hard_block: true
legacy_evidence_status: HUMAN_REVIEWED
sources: [RC-TRAIN-READY-001, RC-DRUG-001, RC-DRUG-CLASS-001, RC-WITHDRAWAL-MRL-001]
---

# 药物页按黄金集用途分级

## 生成角色

- `positive_label_candidate`: 已有具体标签或等效来源，可核验猪靶动物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 或禁停用状态；可在严格引用下进入正向用药题。
- `boundary_only`: 只能说明需要标签、药敏、兽医处方、来源或法域复核；不得生成执行性处方。
- `negative_trap`: 用于训练和评估错误外推，例如人医语境、公共卫生语境、非猪靶动物、禁用/停用/淘汰药或无标签证据。
- `exclude_from_positive_generation`: 不进入正向黄金答案生成。

## 规则

药物页没有显式 `gold_dataset_use` 时，默认视为 `boundary_only`。药物页若为 `NEEDS_REVIEW`，只能做候选召回或待核验提示，除非答案同时引用了可独立核验的具体标签/事实源。

## 允许响应

- 使用 `positive_label_candidate` 页面在精确来源范围内生成限定性处方边界。
- 使用 `boundary_only` 页面生成拒答、追问、标签核验和来源需求。
- 使用 `negative_trap` 页面生成评估陷阱和反例。

## 禁止响应

- 将 `boundary_only` 或 `negative_trap` 页面转化为正向治疗方案。
- 在没有 `gold_dataset_use` 和精确标签来源时默认认为药物可用于猪。
- 将候选命中、教材页码、处方药目录命中或同类药当成批准适应证。
