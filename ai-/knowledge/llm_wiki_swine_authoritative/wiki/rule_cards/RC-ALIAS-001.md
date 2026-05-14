---
card_id: RC-ALIAS-001
severity: high
jurisdiction: Global
hard_block: false
legacy_evidence_status: HUMAN_REVIEWED
updated: 2026-05-07T05:40:41.303569+00:00
---

# 疾病别名归一化门禁

## Rule

疾病命中、证据检索和评审必须使用 exports/alias_index.csv，不得只用原始 target 字符串做硬匹配。

## Enforcement

- Candidate generation: inject this card whenever a case asks for diagnosis, treatment, sampling, regulation, sale, withdrawal period, or public-health boundary.
- CSV conversion: compute local flags from normalized aliases and standard citations.
- Train-ready export: reject records that violate this card.
