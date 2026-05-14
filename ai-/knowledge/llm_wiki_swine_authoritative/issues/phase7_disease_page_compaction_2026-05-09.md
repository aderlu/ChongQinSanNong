# Phase 7 Disease Page Compaction / 2026-05-09

Generated: 2026-05-09T14:35:51+08:00

## Summary

- Pages checked: 3
- Pages changed: 3
- Batch evidence blocks moved: 12
- Fact-like rows moved: 106
- Candidate fact mentions moved: 31
- Source anchors moved: 108
- Runtime bytes reduced: 40524

## Changed Pages

- `wiki/diseases/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md`: blocks=5, rows=31, candidate_fact=12, bytes=22916->11432, expansion=`wiki/evidence_expansions/diseases/phase7/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia-phase7-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md`: blocks=4, rows=44, candidate_fact=12, bytes=24330->10704, expansion=`wiki/evidence_expansions/diseases/phase7/DIS-052-swine-dysentery-brachyspira-hyodysenteriae-phase7-evidence-expansion-20260509.md`
- `wiki/diseases/DIS-044-gl-sser-s-disease.md`: blocks=3, rows=31, candidate_fact=7, bytes=26778->11364, expansion=`wiki/evidence_expansions/diseases/phase7/DIS-044-gl-sser-s-disease-phase7-evidence-expansion-20260509.md`

## Runtime Handling

- Target disease pages now keep compact clinical/runtime cores and short moved-evidence placeholders.
- Detailed batch evidence moved to `wiki/evidence_expansions/diseases/phase7/` is not for default retrieval.
- This phase does not add new disease facts; it reorganizes already present evidence to reduce retrieval noise.
- Diagnosis, regulatory action, treatment, and residue-related generation remains gated by disease/drug rule cards.
