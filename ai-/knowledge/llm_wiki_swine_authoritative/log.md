# Wiki Log

2026-05-06 init | created or verified standard Wiki structure

2026-05-06 init | domain=swine_disease | force_template_sync=False

2026-05-07 drug-backfill | added 28 evidence_only NEEDS_REVIEW drug candidate pages from Diseases of Swine PDF extraction; updated drug/source indexes; did not mutate authoritative facts.

2026-05-07 drug-backfill-round2 | added 34 additional evidence_only NEEDS_REVIEW drug candidate/boundary pages from second PDF scan; updated indexes only.

2026-05-07 authority-web-fetch | fetched 17 authority web/PDF sources to raw cache; created source pages and updated source index; facts unchanged.

2026-05-07 pdf-treatment-candidate-matrix | generated 178 PDF disease-drug treatment candidate rows with PyMuPDF; added derived synthesis page; facts unchanged.

2026-05-07 drug-backfill-round3 | added 6 additional PDF deep-scan drug pages; updated drug index; facts unchanged.
- 2026-05-07 swine-optimization-v6 | fixed missing rule index targets; added dataset QA reinforcement for sampling, lab diagnosis, differential diagnosis, regulatory and drug-use boundaries. Report: `issues/swine_llm_wiki_optimization_v6_2026-05-07.json`.
- 2026-05-07 low-frequency-virus-v7 | reinforced 7 sparse viral disease pages for QA dataset generation. Report: `issues/swine_low_frequency_viruses_v7_2026-05-07.json`.
## 2026-05-07 - Added pages 1-200 textbook crosscutting digest

- Added `wiki/synthesis/swine_textbook_pages_1_200_crosscutting_digest.md`.
- Added candidate facts in `issues/textbook_1_200_crosscutting_candidate_facts_20260507.json`.
- Updated `exports/synthesis_index.csv` with the new synthesis page.
- Scope: extracted and paraphrased crosscutting rules from `raw/md/1-200.md` for herd evaluation, diagnostic process, sample selection, causality, biosecurity, disease control, drug-use boundaries, and procedure boundaries.
- Limits: this update does not fill individual disease-specific clinical signs, lesions, laboratory tests, China regulatory status, or drug label dosage/withdrawal facts.

## 2026-05-07 - Added pages 201-400 textbook system digest

- Added `wiki/synthesis/swine_textbook_pages_201_400_system_digest.md`.
- Added candidate facts in `issues/textbook_201_400_system_candidate_facts_20260507.json`.
- Updated `exports/synthesis_index.csv` with the new synthesis page.
- Scope: extracted and paraphrased system-level and syndrome-level knowledge from `raw/md/201-400.md`, including food safety, zoonoses, show/pet pig boundaries, cardiovascular/hematopoietic differentials, digestive differential diagnosis, immunity/vaccine failure, skin/hoof/claw diagnosis, mammary/PDS context, neurologic/locomotor localization, and reproductive-system opening.
- Limits: this update improves syndrome and evaluation context but does not replace individual pathogen chapters, China official regulatory sources, product labels, executable drug protocols, or full reproductive/respiratory/urinary system coverage.

## 2026-05-07 - Added pages 401-600 reproductive respiratory urinary and virus digest

- Added `wiki/synthesis/swine_textbook_pages_401_600_repro_respiratory_virus_digest.md`.
- Added candidate facts in `issues/textbook_401_600_repro_respiratory_virus_candidate_facts_20260507.json`.
- Updated `exports/synthesis_index.csv` with the new synthesis page.
- Scope: extracted and paraphrased reproductive sampling/differential rules, PRDC and respiratory monitoring rules, urinary gross-lesion differential rules, viral diagnostic interpretation rules, and disease-specific boundaries for adenoviruses, ASF, circoviruses, coronaviruses, flaviviruses, HEV, herpesviruses, and influenza opening from `raw/md/401-600.md`.
- Limits: this update does not replace Chinese official regulatory sources, product labels, complete influenza chapter, later viral chapters, bacterial chapters, or formal differential-matrix exports.

## 2026-05-07 - Added pages 601-800 viral and early bacterial digest

- Added `wiki/synthesis/swine_textbook_pages_601_800_viral_bacterial_digest.md`.
- Added candidate facts in `issues/textbook_601_800_viral_bacterial_candidate_facts_20260507.json`.
- Updated `exports/synthesis_index.csv` with the new synthesis page.
- Scope: extracted and paraphrased disease-specific boundaries for swine influenza, paramyxoviruses, parvoviruses, pestiviruses, picornaviruses, PRRSV, swinepox, rotavirus/reovirus, retroviruses, rhabdoviruses, togaviruses, bacterial overview, Actinobacillus pleuropneumoniae, Actinobacillus suis, and Bordetella bronchiseptica from `raw/md/601-800.md`.
- Limits: this update does not replace Chinese official reporting/quarantine rules, product labels, antimicrobial dosing/withdrawal facts, bacterial chapters after Bordetellosis, parasite/nutrition/toxin chapters, or formal differential-matrix exports.

## 2026-05-07 - Added pages 801-1000 core bacterial disease digest

- Added `wiki/synthesis/swine_textbook_pages_801_1000_core_bacterial_digest.md`.
- Added candidate facts in `issues/textbook_801_1000_core_bacterial_candidate_facts_20260507.json`.
- Updated `exports/synthesis_index.csv` with the new synthesis page.
- Scope: extracted and paraphrased disease-specific boundaries for brucellosis, clostridial diseases, colibacillosis, erysipelas, Glasser's disease, leptospirosis, mycoplasmosis, pasteurellosis, proliferative enteropathy, salmonellosis, staphylococcosis, streptococcosis, swine dysentery/brachyspiral colitis, and tuberculosis opening from `raw/md/801-1000.md`.
- Limits: this update does not replace Chinese official public-health/regulatory rules, antimicrobial labels, dose/route/course/withdrawal facts, complete post-1000 tuberculosis continuation if present, later miscellaneous bacterial/parasitic/nutrition/toxin chapters, or formal differential-matrix exports.

## 2026-05-08 - Reinforced 32 diseases still marked NEEDS_REVIEW with local Markdown evidence boundaries

- Added `wiki/synthesis/swine_textbook_pages_1_200_chapter_type_analysis.md` from `raw/md/DISEASES OF SWINE1-200.md`, organized by chapter and evidence type.
- Added `DOS_1_200_REVIEW_REINFORCEMENT` blocks to 32 disease pages that remain `evidence_status: NEEDS_REVIEW`.
- Reinforcement scope: diagnostic process, sampling, causality, differential diagnosis, biosecurity/control, drug-use boundaries, and local raw Markdown substitution policy.
- Status policy: did not force any disease page to `HUMAN_REVIEWED`; local `raw/md/` evidence can support retrieval and evaluation when source scope is preserved, but executable drug/regulatory conclusions still require label-level or jurisdictional sources.
- Report: `issues/diseases_needs_review_local_md_reinforcement_2026-05-08.md`.

## 2026-05-08 - Mojibake audit and cleanup for diseases/comparisons/drugs

- Checked `wiki/diseases`, `wiki/comparisons`, and `wiki/drugs` with explicit UTF-8 reads.
- Confirmed `comparisons` and `drugs` are clean; default PowerShell display can show false mojibake if not read as UTF-8.
- Recovered reversible mojibake in disease pages and preserved all evidence statuses.
- Residual unrecoverable text is limited to four source-anchored raw handbook excerpt lines in DIS-009, DIS-026, DIS-040, and DIS-044.
- Report: `issues/wiki_diseases_comparisons_drugs_mojibake_audit_2026-05-08.md`.
