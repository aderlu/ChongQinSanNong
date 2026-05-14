# Swine wiki execution protocol V10 entity-first update

- Date: 2026-05-08
- Updated document: `issues/swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md`
- Reason: execution protocol must prioritize strengthening existing entity pages before broad new-source searching.

## Correction to V9

V9 overcorrected toward mandatory source-first search. That risks spending effort on broad web discovery while existing disease/drug pages remain thin or hard for generation/evaluation systems to retrieve.

V10 changes the priority:

1. Reinforce existing entity pages first.
2. Use existing `HUMAN_REVIEWED` facts, SRC/source pages, rule cards, syndrome pages, comparison pages and synthesis gates first.
3. Trigger external search only for unresolved high-risk gaps or when existing sources cannot support a required entity-page claim.
4. Treat source enrichment as a targeted support action, not the main task.

## New execution status labels

- `entity_reinforced`: existing facts/source/rules have been landed into entity pages with anchors, boundaries and comparison links.
- `source_enrichment_pending`: entity page is usable for generation/evaluation constraints, but disease/drug-specific A0/A1 expansion remains open.
- `source_enriched`: external A0/A1/A2 source search was triggered, accepted sources were created as source pages, indexes were updated, and entity pages were backfilled.
- `partial`: entity page still lacks enough anchored facts or boundaries for reliable use.
- `blocked`: source, parsing or access failure prevents safe update.

## When external search is required

External source search is required only when:

- existing `HUMAN_REVIEWED` facts are fewer than the entity usability threshold;
- China regulatory status, legal reporting, culling, movement control, food safety, public health, MRL or withdrawal period is needed;
- a drug page may be promoted to `positive_label_candidate`;
- the entity belongs to high-risk categories such as ASF/FMD/CSF/PRRS/PED, zoonosis, vesicular disease, sudden death/high mortality, antimicrobial use, banned/stopped drugs, or residue-sensitive products;
- comparison/rule/synthesis pages need authority beyond current sources.

## What still must happen every time

Every execution must still:

- inspect existing pages and exports;
- update the target entity pages directly;
- add explicit Evidence gaps instead of leaving holes for the model;
- update comparison/rule/synthesis pages if the change affects generation or evaluation;
- write an execution log with validation counts.

The task should stop only when the existing entity pages are actually more useful for generation/evaluation, not merely because new sources were found.
