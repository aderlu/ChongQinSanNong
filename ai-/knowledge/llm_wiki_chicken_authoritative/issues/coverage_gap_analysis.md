# Coverage Expansion Analysis

## Why earlier page counts were too low

- Disease coverage was previously constrained by a small seed universe and weak derivation rules.
- Standards and sources were previously represented as separate page layers even when they referred to the same evidence item.
- Rule pages were anchored mainly to top-level regulatory notices instead of one-page-per-anchor patterns.
- Drug issues were counted per ingredient rule, which made one unresolved bulletin look like dozens of separate root causes.

## What changed in this rebuild

- Expanded authoritative source inventory to 121 local originals.
- Normalized all sources into a harder evidence pyramid using `authority_level + evidence_role + jurisdiction + primary_or_secondary`.
- Added more directly downloadable standards and PDFs from `std.cahec.cn` where public download was available.
- Expanded disease pages to 60 after adding new disease reference pages and stricter de-duplication.
- Folded standards into the source layer so one authoritative item now maps to one primary source page.
- Collapsed unresolved work into 4 grouped root-cause buckets for easier manual follow-up.

## Remaining blockers

- The previously image-based CAHEC and MOA PDFs now have local OCR text, but some pages may still need manual QA if downstream use requires publication-grade text fidelity.
- Product-level veterinary labels are not all publicly bulk-downloadable; many drug rows still point to bulletin-level evidence and need manual label capture.
- OpenSTD full-text flows with captcha or off-site redirects still require manual intervention when no direct public PDF is exposed.
