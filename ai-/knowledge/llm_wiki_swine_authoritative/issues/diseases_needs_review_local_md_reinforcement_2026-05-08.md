---
type: issue_report
page_id: diseases_needs_review_local_md_reinforcement_2026_05_08
title: diseases NEEDS_REVIEW local-md reinforcement execution
updated: 2026-05-08T23:59:00+08:00
evidence_status: HUMAN_REVIEWED
sources:
  - SRC-0003
  - SRC-0007
  - SRC-0008
  - SRC-0009
  - SRC-0010
  - SRC-0011
  - SRC-0012
  - SRC-0014
  - swine_textbook_pages_1_200_chapter_type_analysis
---

# diseases NEEDS_REVIEW local-md reinforcement execution

## Problem

The disease namespace still contained 32 pages with `evidence_status: NEEDS_REVIEW`. Some had already received symptom or differential-boundary enrichment, but the status was intentionally not forced to `HUMAN_REVIEWED`.

## Action

1. Read and structured `raw/md/DISEASES OF SWINE1-200.md` by section, chapter, and usable evidence type.
2. Added `wiki/synthesis/swine_textbook_pages_1_200_chapter_type_analysis.md` as a detailed source-intake and retrieval page.
3. Added one bounded reinforcement block to each of the 32 `NEEDS_REVIEW` disease pages, marked by `DOS_1_200_REVIEW_REINFORCEMENT`.
4. Updated source-first generation policy with `Local raw Markdown substitution / V15`.

## Reinforced groups

- Viral diseases: DIS-001, DIS-003, DIS-005, DIS-006, DIS-010, DIS-012, DIS-013, DIS-014, DIS-016, DIS-017, DIS-019, DIS-020, DIS-022, DIS-025, DIS-027, DIS-029, DIS-031, DIS-032, DIS-034.
- Bacterial and zoonotic diseases: DIS-036, DIS-038, DIS-053, DIS-054.
- Parasitic diseases: DIS-059, DIS-062, DIS-063, DIS-064.
- Nutritional, mycotoxin, and toxic disease pages: DIS-065, DIS-069, DIS-070, DIS-071, DIS-072.

## Evidence use rule

Local Markdown documents under `raw/md/` may substitute for pathogen, diagnosis, regulatory-boundary, and disease-chapter evidence when the source is cited by book/manual, chapter, page range, or registered `SRC-*` anchor. They do not by themselves authorize executable drug doses, fixed withdrawal periods, MRL claims, slaughter/transport decisions, quarantine orders, shipment permissions, or jurisdiction-specific legal conclusions.

## Status rule

No disease page was changed from `NEEDS_REVIEW` to `HUMAN_REVIEWED`. The reinforcement is retrieval and evaluation support only.
