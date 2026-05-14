---
card_id: RC-CITATION-001
severity: high
jurisdiction: Global
hard_block: false
legacy_evidence_status: HUMAN_REVIEWED
updated: 2026-05-08T23:59:00+08:00
---

# 标准证据引用门禁

## Rule

所有诊断、采样、监管、用药、休药期和食品安全结论必须使用标准来源锚点：`source=A0-...`、`source=A1-...`、`source=A2-...`、`source=SRC-...`、`source=RC-...` 或 `source=RULE-...`。内部 anchor key、裸页面路径、无来源摘要不能作为训练可用引用。

## Enforcement

- Candidate generation: inject this card whenever a case asks for diagnosis, treatment, sampling, regulation, sale, withdrawal period, or public-health boundary.
- CSV conversion: compute local flags from normalized aliases and standard citations.
- Train-ready export: reject records that violate this card.
