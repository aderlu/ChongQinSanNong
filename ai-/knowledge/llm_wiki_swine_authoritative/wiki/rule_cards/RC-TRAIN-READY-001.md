---
card_id: RC-TRAIN-READY-001
severity: critical
jurisdiction: Global
hard_block: true
legacy_evidence_status: HUMAN_REVIEWED
updated: 2026-05-08T23:59:00+08:00
sources: [RC-CITATION-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
---

# 训练可用样本门禁

## Rule

训练可用样本必须 pass、无 fatal risk、目标疾病别名命中诊断、回答标准引用不少于 3 个，且不得包含无来源剂量、无来源疗程、无来源具体休药期或无来源食品安全承诺。

## Source-first adjustment

可接受来源包括 `A0/A1/A2/SRC/RC/RULE`。中国来源不再是默认唯一门槛；但任何法域合规承诺、处方、休药期、MRL 或肉品可食结论都必须精确到对应来源自身覆盖范围。

## Enforcement

- Candidate generation: inject this card whenever a case asks for diagnosis, treatment, sampling, regulation, sale, withdrawal period, or public-health boundary.
- CSV conversion: compute local flags from normalized aliases and standard citations.
- Train-ready export: reject records that violate this card.
