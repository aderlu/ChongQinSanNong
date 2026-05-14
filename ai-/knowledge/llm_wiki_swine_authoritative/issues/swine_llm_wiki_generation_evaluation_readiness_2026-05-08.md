# Swine LLM Wiki Generation/Evaluation Readiness Audit / 2026-05-08

- Readiness score: 89/100
- Entity counts: diseases=73, drugs=81, syndromes=22, comparisons=17, rules=449, rule_cards=21, sources=239, synthesis=27.
- Disease coverage: {'blank': 73}
- Drug status: {'blank': 4, 'source_anchored_drug_evidence_page': 71, 'regulatory_boundary_page': 1, 'partial_drug_evidence_page': 8}
- Rule cards: 21 total, 11 hard blocks; required missing=[].
- Synthesis required missing: [].

## Fact Table Quality

- `handbook_prescription_fact_index.csv`: rows=394, source_id_rate=1.0, page_rate=1.0, unmapped=0.
- `veterinary_treatment_of_pigs_fact_index.csv`: rows=293, source_id_rate=1.0, page_rate=1.0, unmapped=0.
- `veterinary_treatment_of_pigs_medicine_index.csv`: rows=175, source_id_rate=1.0, page_rate=1.0, unmapped=0.
- `swine_farm_drug_use_1_200_fact_index.csv`: rows=727, source_id_rate=1.0, page_rate=1.0, unmapped=0.
- `swine_farm_drug_use_200_363_fact_index.csv`: rows=366, source_id_rate=1.0, page_rate=1.0, unmapped=0.
- `handbook_prescription_drug_mention_index.csv`: rows=192, source_id_rate=1.0, page_rate=1.0, unmapped=0.
- `swine_farm_drug_use_1_200_drug_mention_index.csv`: rows=538, source_id_rate=1.0, page_rate=1.0, unmapped=0.
- `swine_farm_drug_use_200_363_drug_mention_index.csv`: rows=357, source_id_rate=1.0, page_rate=1.0, unmapped=0.

## Path Integrity

- `disease_index.csv`: rows=73, checked_paths=73, missing_paths=0.
- `drug_page_index.csv`: rows=84, checked_paths=84, missing_paths=0.
- `rule_index.csv`: rows=449, checked_paths=449, missing_paths=0.
- `rule_card_index.csv`: rows=21, checked_paths=21, missing_paths=0.
- `comparison_index.csv`: rows=14, checked_paths=14, missing_paths=0.
- `synthesis_index.csv`: rows=24, checked_paths=24, missing_paths=0.
- `source_index.csv`: rows=235, checked_paths=235, missing_paths=0.

## Entity Readiness

- diseases: pages=73, status_counts={'MISSING': 73}, missing_required_section=73, missing_sources=0, legacy_review_frontmatter=0.
- drugs: pages=81, status_counts={'MISSING': 81}, missing_required_section=1, missing_sources=0, legacy_review_frontmatter=0.

## Deductions

-10: disease pages missing unified availability section
-1: drug pages missing unified availability section

## Conclusion

The wiki is structurally capable of supporting source-first swine disease dataset generation and evaluation. It has entity pages, rule cards, comparison matrices, treatment/prescription fact tables, and source-indexed evidence. Remaining risks are listed above and should be handled as gating constraints rather than blockers for all dataset work.
