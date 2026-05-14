# Phase 9 Runtime Cleanup Regression / 2026-05-09

Generated: 2026-05-09T14:56:01+08:00

## Summary

- Compaction pages checked: 11
- Compaction pages changed: 11
- Evidence blocks moved: 50
- Fact-like rows moved: 336
- Candidate fact mentions moved: 39
- Source anchors moved: 347
- Runtime bytes reduced: 155100
- Partial pages checked: 41
- Partial pages changed: 41

## Compacted Pages

- `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`: blocks=3, candidate_fact=2, bytes=27440->18390, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-008-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`: blocks=3, candidate_fact=2, bytes=26872->14459, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-009-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`: blocks=4, candidate_fact=2, bytes=39849->11396, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-024-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`: blocks=3, candidate_fact=2, bytes=33055->15634, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-026-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-040-colibacillosis.md`: blocks=5, candidate_fact=3, bytes=32244->15854, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-040-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`: blocks=6, candidate_fact=4, bytes=23278->14703, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-041-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`: blocks=5, candidate_fact=6, bytes=34477->15350, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-046-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-049-salmonellosis.md`: blocks=7, candidate_fact=5, bytes=26218->18005, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-049-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-051-streptococcosis-streptococcus-suis.md`: blocks=5, candidate_fact=3, bytes=23638->8455, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-051-phase9-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-055-external-parasites-mange.md`: blocks=6, candidate_fact=5, bytes=22848->16647, expansion=`wiki/evidence_expansions/diseases/phase9/DIS-055-phase9-evidence-expansion-20260509.md`
- `wiki/drugs/DRUG-042-ampicillin.md`: blocks=3, candidate_fact=5, bytes=20352->6278, expansion=`wiki/evidence_expansions/drugs/phase9/DRUG-042-ampicillin-phase9-evidence-expansion-20260509.md`

## Partial Gap Routing

- Controlled partial pages annotated: 41
- Partial pages are retained as recall and gap-routing entries; missing facets must not be guessed.

## Runtime Handling

- Phase 9 does not add new biomedical facts.
- It moves low-risk dense evidence to expansion files and marks partial pages as controlled gap-routing pages.
- Final regression should be read together with `runtime_hallucination_risk_audit_2026-05-09` and readiness outputs.
