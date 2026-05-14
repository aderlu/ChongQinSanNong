# Phase 8 Rule Card And Exporter Gate Report

Generated: 2026-05-13T00:18:14+08:00

## Summary

- Rule cards indexed: 21
- Hard-block cards: 11
- Missing required cards: []
- Runtime pages requiring rule checks: 156
- Runtime pages missing expected page-level rule anchors: 0

## Exporter Hard Blocks

- `unsupported_dose`: cards=RC-DRUG-001; block_when=No source/fact/rule anchor covers product, species, formulation, route, dose/course and jurisdiction.
- `unsupported_withdrawal_mrl`: cards=RC-WITHDRAWAL-MRL-001; block_when=No A0 or label-level equivalent source covers product, species, tissue/food class and jurisdiction.
- `unsupported_regulatory_action`: cards=RC-DISEASE-REGULATORY-001;RC-REGULATORY-CURRENT-001; block_when=No current official/regulatory source covers the requested jurisdiction and action.
- `single_test_causality_overclaim`: cards=RC-DX-001;RC-EVAL-RUBRIC-001; block_when=Answer asserts definitive causality without sample, method, timing, clinical fit and differential boundary.
- `no_source_citation`: cards=RC-CITATION-001; block_when=Any high-value answer lacks source_id, fact_id, URL/page/table anchor or rule card citation.
- `source_level_mismatch`: cards=RC-EVAL-RUBRIC-001;RC-REGULATORY-CURRENT-001; block_when=SRC/A1/A2 or textbook evidence is used for an A0/label-level regulatory, withdrawal, MRL, residue, food-safety or compulsory-action claim.

## Outputs

- `exports/rule_card_index.csv`
- `exports/exporter_hard_block_rules.json`
