# Phase 6 Drug Page Compaction / 2026-05-09

Generated: 2026-05-09T14:25:31+08:00

## Summary

- Pages checked: 6
- Pages changed: 6
- Batch evidence blocks moved: 28
- Fact-like rows moved: 300
- Candidate fact mentions moved: 63
- Source anchors moved: 300
- Runtime bytes reduced: 132094

## Changed Pages

- `wiki/drugs/DRUG-015-tylosin.md`: blocks=4, rows=56, candidate_fact=16, bytes=34086->7670, expansion=`wiki/evidence_expansions/drugs/phase6/DRUG-015-tylosin-phase6-evidence-expansion-20260509.md`
- `wiki/drugs/DRUG-021-doxycycline.md`: blocks=5, rows=45, candidate_fact=12, bytes=26497->8209, expansion=`wiki/evidence_expansions/drugs/phase6/DRUG-021-doxycycline-phase6-evidence-expansion-20260509.md`
- `wiki/drugs/DRUG-013-tiamulin.md`: blocks=5, rows=47, candidate_fact=11, bytes=30086->8265, expansion=`wiki/evidence_expansions/drugs/phase6/DRUG-013-tiamulin-phase6-evidence-expansion-20260509.md`
- `wiki/drugs/DRUG-012-florfenicol.md`: blocks=5, rows=46, candidate_fact=9, bytes=32418->9610, expansion=`wiki/evidence_expansions/drugs/phase6/DRUG-012-florfenicol-phase6-evidence-expansion-20260509.md`
- `wiki/drugs/DRUG-010-amoxicillin.md`: blocks=4, rows=47, candidate_fact=8, bytes=29903->8503, expansion=`wiki/evidence_expansions/drugs/phase6/DRUG-010-amoxicillin-phase6-evidence-expansion-20260509.md`
- `wiki/drugs/DRUG-019-oxytetracycline.md`: blocks=5, rows=59, candidate_fact=7, bytes=29848->8487, expansion=`wiki/evidence_expansions/drugs/phase6/DRUG-019-oxytetracycline-phase6-evidence-expansion-20260509.md`

## Runtime Handling

- Target pages now keep a compact runtime core and short moved-evidence placeholders.
- Detailed batch evidence moved to `wiki/evidence_expansions/drugs/phase6/` is not for default retrieval.
- This phase does not add new drug facts; it reorganizes already present evidence to reduce retrieval noise.
- Drug generation remains gated by `RC-DRUG-001` and `RC-WITHDRAWAL-MRL-001`.
