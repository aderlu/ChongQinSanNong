# DIS-051 Streptococcus suis Authority Web Refresh / 2026-05-13

## Scope

This evidence expansion records the real authority-source refresh for `DIS-051-streptococcosis-streptococcus-suis`.

## Source Added

- `A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026`

## Why This Refresh Was Needed

- Before this refresh, the runtime page still declared evidence gaps for transmission, clinical signs, lesions, laboratory diagnosis, differential diagnosis, and control points.
- The page existed in the wiki but had `evidence_units=0` and `page_gold_ready=false` in the current `wiki-native` build report, which meant the main graph could not admit verified semantic edges from this page.

## Facts Added

- `SSUIS-101-carrier-tonsil-and-colonization`
- `SSUIS-102-transmission-colonization-mixing`
- `SSUIS-103-herd-to-herd-carrier-movement`
- `SSUIS-104-clinical-septicemia-meningitis-arthritis`
- `SSUIS-105-early-clinical-signs-and-age-window`
- `SSUIS-106-lesions-meningitis-serositis-septicemia`
- `SSUIS-107-diagnosis-history-culture-serotyping`
- `SSUIS-108-diagnosis-tonsil-nasal-boundary`
- `SSUIS-109-differential-glaesser-actinobacillus-others`

## Governance Boundary

- This refresh is additive and does not silently delete existing textbook or A0 regulatory evidence.
- China official outbreak/control handling still routes to `A0-MOA-STREP-SUIS-CONTROL-2005` and rule cards.
- Merck A2 evidence is used here for disease facts, differential diagnosis, and laboratory interpretation boundaries, not for executable drug or regulatory conclusions.
