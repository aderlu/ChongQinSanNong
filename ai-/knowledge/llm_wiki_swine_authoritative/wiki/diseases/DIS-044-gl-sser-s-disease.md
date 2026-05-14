---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-044
updated: 2026-05-14T10:30:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-573, A0-MOA-THREE-CLASS-ANIMAL-DISEASE-SPECS, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0066, SRC-0087, SRC-0089, SRC-0090]
---

# Glasser's Disease

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime core compaction / Phase 7

- Runtime role: compact disease boundary page for retrieval, differential diagnosis routing, prevention/control framing, and evaluation checks.
- Phase 7 moved high-density batch evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`.
- Moved fact-like rows: 31; moved candidate facts: 7.
- `RC-DX-001`: Diagnosis must remain evidence-routed and distinguish suspicion, sample, method, pathogen detection, causality, and differential diagnosis.
- `RC-DISEASE-REGULATORY-001`: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- `RC-DRUG-001`: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- Expansion files under `wiki/evidence_expansions/diseases/phase7/` are for audit, source lookup, and manual review, not default production retrieval.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.

## English / textbook chapter name

- Glasser's disease

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

## Transmission and epidemiology

- Piglets can be protected during early colonization by maternal IgM and IgG, but that protection mainly reflects the strains to which the sow was previously exposed. `fact_id=GLASS-003-maternal-immunity; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 870`
- Clinical disease is commonly associated with decline of maternal immunity, exposure to new strains, weaning/mixing, introduction of pigs, chilling, crowding, or concurrent stressors. `fact_id=GLASS-004-risk-2aee4f263dad2d98046bb67515e900c0; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 870`
- *H. parasuis* infection is epidemiologically associated with PRRSV, PCV2, swine influenza, and *B. bronchiseptica*; coinfections can intensify or alter disease expression. `fact_id=GLASS-005-coinfection; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 871`

## Clinical signs

- Acute Glasser's disease can present with fever, coughing, abdominal breathing, swollen joints with lameness, recumbency, paddling, tremors, and other CNS-related manifestations. `fact_id=GLASS-006-clinical; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 872`
- Peracute cases may have a short course and can die suddenly without obvious preceding gross lesions. `fact_id=GLASS-007-peracute; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 872`

## Necropsy findings

- Typical pathology is fibrinous to fibrinosuppurative polyserositis, and some cases can also include fibrinous meningitis. `fact_id=GLASS-008-lesions; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 873`

## Laboratory diagnosis

- This runtime page does not independently promote unanchored diagnosis logic; laboratory interpretation must still route through `RC-DX-001`, source anchors, sample context, and differential diagnosis. Existing detailed evidence remains in the linked evidence expansion.

## Differential diagnosis

- Case generation and evaluation for this page should preferentially cross-link to [CMP-003-respiratory-disease](../comparisons/CMP-003-respiratory-disease.md) and [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md); the page must not be used as a stand-alone deterministic diagnosis source.

## Control points

- Maternal immunity can interfere with antibody induction after piglet vaccination against *H. parasuis*; vaccine interpretation should therefore be tied to outbreak context and herd immune status. `fact_id=GLASS-010-vaccine-maternal; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 875`
- Antibiotics are commonly discussed in control settings, but pressure to reduce group-level preventive antimicrobial use reinforces the boundary that control should also emphasize vaccine strategy and management measures. `fact_id=GLASS-011-antibiotic-boundary; source_id=SRC-0066; anchor=Chapter 54 Glasser disease; PDF page 875`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: executable treatment regimen, dose, route, withdrawal period, MRL, residue, jurisdiction-specific movement control, quarantine, culling, and reporting actions.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## Pathogen and classification

- Initial classification: bacterial disease / polyserositis-pattern disease.
- Textbook chapter: Section IV Bacterial Diseases, Chapter 54.
- Primary chapter span: PDF page 868-877.

## Regulatory and execution boundary

- This page follows a source-first evidence policy. Diagnosis, transmission, clinical signs, lesions, and laboratory interpretation may rely on `A0/A1/A2/SRC/RC/RULE` anchors when the anchor is explicit.
- Reporting, quarantine, culling, movement control, inspection, jurisdiction-specific disease-control actions, food handling, and local compliance conclusions must return to the corresponding current official/regulatory sources.
- This disease page summary cannot replace executable official instructions.

## Typical host and stage

- Applies to species: swine.
- Susceptible stage details should be read from the source-anchored facts above and from the linked evidence expansion when more density is needed.

## Treatment and disposition boundary

- This page must not independently generate executable prescriptions, dose, route, course, withdrawal period, or MRL conclusions.
- Treatment-related answers must simultaneously satisfy pathogen/pathology evidence, veterinary diagnosis, susceptibility or label evidence, product labeling, prescription-drug management, withdrawal/MRL requirements, and current China regulatory rules.
- Suspected major regulated animal disease scenarios must not use empiric treatment text from this page to replace diagnosis, reporting, isolation, or official workflow.

## Local evidence

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - local textbook TOC anchor.
- [SRC-0066](../sources/SRC-0066-diseases-of-swine-11e-chapter-54-glassers-disease.md) - local textbook chapter anchor for Chapter 54 Glasser disease.
- [A0-MOA-573](../sources/A0-MOA-573.md) - China animal disease classification entry, used for classification check rather than clinical expansion.
- [A0-MOA-THREE-CLASS-ANIMAL-DISEASE-SPECS](../sources/A0-MOA-THREE-CLASS-ANIMAL-DISEASE-SPECS.md) - three-class animal disease prevention/control specification, used only where A0 classification scope is applicable.
- [RC-DISEASE-REGULATORY-001](../rule_cards/RC-DISEASE-REGULATORY-001.md) - regulatory boundary rule card.

## source_trust / evidence_coverage / usage_scope

- source_trust: authoritative. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: disease recall, evidence lookup, differential prompts, and boundary checks only; do not generate executable treatment, withdrawal-period, MRL, or regulatory conclusions without rule-card and source verification.

## Evidence expansion index

- Historical high-density blocks and build-time supplements were moved out of the default runtime page while preserving original anchors in evidence expansion files.
- Default production retrieval should prefer this compact runtime page; audit, trace-back, and denser source lookup should read the files below.
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-044-gl-sser-s-disease/001-HANDBOOK_RX_V13_1.md`: HANDBOOK_RX_V13_1; sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001.
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-044-gl-sser-s-disease/002-SFDUT_1_200_V13_1.md`: SFDUT_1_200_V13_1; sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001.
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-044-gl-sser-s-disease/003-SFDUT_200_363_V13_1.md`: SFDUT_200_363_V13_1; sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001.
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-044-gl-sser-s-disease/004-Formal-Batch-024-V3.md`: Formal Batch 024 / V3 extraction progress; sources: SRC-0066.
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-044-gl-sser-s-disease/005-Formal-Disease-Completion-V5.md`: Formal Disease Completion / V5; sources retained in the expansion.
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-044-gl-sser-s-disease/001-Phase-2-Gold-Anchors-V8.md`: Phase 2 Gold Anchors / V8; sources: CMP-003-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0066.
