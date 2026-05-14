# Swine wiki execution protocol V9 update

- Date: 2026-05-08
- Updated document: `issues/swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md`
- Reason: prior Phase 2 execution reorganized local `HUMAN_REVIEWED` facts effectively, but did not perform enough web/source acquisition to qualify as complete source enrichment.

## What changed

Added a mandatory source-first workflow:

- local baseline scan;
- external authority search;
- source triage;
- source page creation;
- entity-page reinforcement;
- comparison/rule/synthesis update;
- execution-log recording.

Added minimum source coverage thresholds:

- disease pages require clinical/pathology/diagnosis sources, regulatory/public-health boundary sources, diagnosis/sampling sources, differential anchors, and at least 5 logged search queries;
- drug pages require China official label/register/quality/prescription/MRL/withdrawal/banned-status searches and at least 6 logged search queries.

Added explicit stop conditions:

- source pages must be created and indexed before external-source facts are used;
- entity pages must receive source-anchored facts or explicit evidence gaps;
- execution logs must include queries, accepted sources, rejected sources, modified pages and unresolved gaps;
- a task cannot be marked complete if it only reorganizes local facts, only adds rule cards, only finds entry pages, or only searches without creating source pages.

## Status correction

The previous Phase 2 disease work should be interpreted as:

- `clinical_anchor_partial`: complete for local reviewed-fact anchoring and comparison matrix creation;
- not yet `source-enriched`: disease-specific A0/A1/A2 web source searches were not sufficiently executed or logged for every entity.

## Required next task

Run `Phase 2-A0/A1 Source Enrichment` for the 12 reinforced diseases:

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

For each disease:

- execute the Disease query checklist;
- create source pages for accepted A0/A1/A2 sources;
- update `exports/source_index.csv`;
- update disease `sources:` and China regulatory/public-health boundary sections;
- record unresolved no-hit findings instead of inventing facts.
