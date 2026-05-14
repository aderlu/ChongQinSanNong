# Swine wiki diseases/drugs gap execution log

- Date: 2026-05-08
- Parent review: `issues/swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md`
- Execution scope: first-pass safety and source reinforcement for drug/disease gold-dataset gates.

## Completed

### A0 source pages added or reinforced

- Added `wiki/sources/A0-MOA-PRESCRIPTION-790-2024.md`.
  - Purpose: latest veterinary prescription-drug catalogue workflow and fourth-batch catalogue boundary.
  - Key boundary: prescription catalogue status does not prove pig indication, dose, route, course, withdrawal period, or label approval.
- Added `wiki/sources/A0-MOA-MRL-GB31650-1-2022.md`.
  - Purpose: GB 31650.1-2022 residue-limit source entry.
  - Key boundary: entry page is not a numeric MRL or withdrawal-period source by itself.
- Reinforced `wiki/sources/A0-MOA-THREE-CLASS-ANIMAL-DISEASE-SPECS.md`.
  - Added reviewed facts for report, isolation, movement control, treatment eligibility, legal drug use, withdrawal-period compliance, and 2-year drug-record retention.

### Drug rule cards added

- Added `wiki/rule_cards/RC-DRUG-CLASS-001.md`.
  - Blocks inference from drug class pages to specific China pig products, indications, dose, route, course, or withdrawal period.
- Added `wiki/rule_cards/RC-WITHDRAWAL-MRL-001.md`.
  - Requires exact jurisdiction/product/species/formulation or exact standard terms for withdrawal-period, MRL, residue and meat-safety claims.
- Added `wiki/rule_cards/RC-DRUG-GOLD-ROLE-001.md`.
  - Defines `positive_label_candidate`, `boundary_only`, `negative_trap`, and `exclude_from_positive_generation`.
  - Missing `gold_dataset_use` defaults to `boundary_only`.

### Disease rule card added

- Added `wiki/rule_cards/RC-DISEASE-REGULATORY-001.md`.
  - Blocks China animal-disease category, reporting, treatment, culling, movement-control and immunization claims without current A0 source support.
  - Allows use of the three-class disease prevention specification only after the disease classification is separately confirmed.

### Drug pages normalized

- Added `gold_dataset_use: boundary_only` to 75 drug pages.
- Marked `DRUG-075-praziquantel.md` as `gold_dataset_use: negative_trap`.
  - Purpose: prevent false inference from Taenia solium human definitive-host/public-health context to routine pig treatment.
- Generated `exports/drug_gold_role_index.csv`.
  - Summary: 75 `boundary_only`, 1 `negative_trap`.

### Synthesis gates updated

- Updated `wiki/synthesis/swine_drug_and_withdrawal_boundary.md`.
  - Added V8 drug gold-dataset gates.
  - Added new source/rule anchors.
- Updated `wiki/synthesis/swine_dataset_generation_validity_gate_v7.md`.
  - Positive drug-use answers now require `positive_label_candidate`.
  - Boundary-only, negative-trap, excluded or `NEEDS_REVIEW` drug pages must not become positive treatment sources.

### First disease-page reinforcement batch

Added A0/regulatory non-inference and treatment-boundary anchors to:

- `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- `wiki/diseases/DIS-047-pasteurellosis.md`
- `wiki/diseases/DIS-040-colibacillosis.md`
- `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`

Each page now explicitly says:

- China disease classification and reporting/treatment conclusions require A0 official catalogue verification.
- The three-class disease prevention specification is conditional and may be used only after disease classification is confirmed.
- Treatment-related answers require disease evidence, veterinary diagnosis, antimicrobial susceptibility or label basis, approved product instructions, prescription status, withdrawal/MRL checks, and current China law.

### Export indexes updated

- Appended new A0 sources to `exports/source_index.csv`.
- Appended new rule cards to `exports/rule_card_index.csv`.
- Added `exports/drug_gold_role_index.csv`.

## Remaining work

### Phase 2 disease facts

Phase 2 first execution was completed after the initial safety pass.

Added `## Phase 2 Gold Anchors / V8` blocks to 12 disease pages:

- Glasser's disease
- mycoplasmal pneumonia
- pasteurellosis
- colibacillosis / yellow-white scours
- edema disease
- clostridial enteritis
- salmonellosis
- mange
- leptospirosis
- rotavirus
- PEDV

Validation summary:

- All 12 target disease pages contain a V8 gold-anchor block.
- Each page has at least 8 V8 reviewed fact references; most have 10-15.
- Each page links to at least one comparison matrix.
- Drug/regulatory non-inference boundaries were preserved through `RC-DISEASE-REGULATORY-001`, `RC-DRUG-001`, and `RC-WITHDRAWAL-MRL-001`.

Still not completed in Phase 2:

- toxic gases
- mycotoxins
- vesicular disease page-level enrichment beyond the comparison matrix
- disease-specific China A0 classification confirmation for common production diseases where A0 sources remain generic

### Phase 3 comparison pages

Created comparison pages:

- `wiki/comparisons/CMP-001-neonatal-diarrhea.md`
- `wiki/comparisons/CMP-002-post-weaning-diarrhea.md`
- `wiki/comparisons/CMP-003-respiratory-disease.md`
- `wiki/comparisons/CMP-004-reproductive-failure.md`
- `wiki/comparisons/CMP-005-vesicular-disease.md`
- `wiki/comparisons/CMP-006-sudden-death-septicemia.md`
- `wiki/comparisons/CMP-007-skin-pruritus-crusts.md`

Generated export:

- `exports/comparison_index.csv`

Validation summary:

- 7 comparison pages created.
- Each page includes trigger pattern, candidate diseases, limitations, minimum diagnostic package, safety/regulatory/drug boundary, and evaluation traps.

### Phase 4 positive drug promotion

No drug page was promoted to `positive_label_candidate` in this execution. Promotion should happen only after exact China pig-relevant label/announcement, formulation, target species, indication, prescription status, withdrawal and MRL evidence are verified.
