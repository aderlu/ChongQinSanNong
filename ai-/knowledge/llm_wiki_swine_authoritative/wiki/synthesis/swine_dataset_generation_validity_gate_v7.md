---
tags: [synthesis, swine, dataset, qa, evidence_gate, generation_gate, source_first, v11_1]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, gold_candidate, audit_only, generation_gate]
sources: [RC-CITATION-001, RC-TRAIN-READY-001, RC-DRUG-GOLD-ROLE-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
---

# Swine Dataset Generation Validity Gate V11.1

## Purpose

This page defines the minimum source-first evidence package for swine QA dataset generation, draft answers, judging and export.

## Required Evidence Package

- Disease identity must be normalized through `exports/alias_index.csv`.
- Standard anchors may be `source=A0-...`, `source=A1-...`, `source=A2-...`, `source=SRC-...`, `source=RC-...`, or `source=RULE-...`.
- Diagnosis requires at least one disease-specific source and one differential, syndrome, sampling or laboratory source.
- Treatment language requires a drug page or rule card plus a specific label/fact source when the answer gives executable dose, route, course, indication, withdrawal period or MRL.
- Regulated, zoonotic, toxic, food-safety or public-health cases must include the applicable rule/source before management language.
- Positive drug-use answers require the referenced drug page to be `positive_label_candidate` or an equivalent exact label/fact source. Missing `gold_dataset_use` defaults to `boundary_only`.
- Drug-class pages cannot support specific product, dose, route, course, indication, withdrawal period, MRL or lawfulness.

## Train-ready Reject Reasons

- `final_label` is not `pass`.
- `target_disease_mismatch` is true after alias normalization.
- Standard citation count is less than 3.
- The answer contains a specific dose, course, route, withdrawal period, MRL or meat-edibility conclusion without an exact label/fact source.
- The answer treats a `boundary_only`, `negative_trap`, `exclude_from_positive_generation`, or `NEEDS_REVIEW` drug page as a positive treatment source.
- The answer infers pig use from a drug class page, candidate PDF hit, human-public-health context, other animal species, or unrelated label.
- The answer hides source jurisdiction and presents one jurisdiction's label as another jurisdiction's compliance conclusion.
- Any judge marks `fatal_risk=true`.
