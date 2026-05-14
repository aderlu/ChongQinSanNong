# V11 P1 web-first disease reinforcement execution log

- Date: 2026-05-08
- Scope: `wiki/diseases`, `wiki/sources`, `exports/source_index.csv`, `exports/knowledge_facts.json`
- Target entities: DIS-004 porcine astrovirus; DIS-025 atypical porcine pestivirus / APPV; DIS-026 foot-and-mouth disease; DIS-032 rabies virus risk
- Status: partial / source_enriched

## Task scope and required fields

- Entity type: disease pages.
- Required fields: pathogen/form positioning, epidemiology or public-health boundary, clinical signs, laboratory diagnosis, differential diagnosis, control/treatment/regulatory boundary, generation/evaluation boundary.
- High-risk dimensions: China legal disease status, report/escalation, public-health exposure, vesicular-disease handling, drug/dose/withdrawal/MRL/food-chain claims.
- Required authority levels: A0 for China regulatory/FMD catalog and official control guide; A1 for international official/public-health diagnosis and escalation; A2 for non-regulatory clinical background for porcine astrovirus and APPV.

## Web/source search

| Entity | Query | Result | Accepted source_id | Rejected reason |
|---|---|---|---|---|
| DIS-026 | `site:xmsyj.moa.gov.cn 口蹄疫 防控 技术指南 猪` | MOA/XMSYJ 2024 FMD control guide opened and already registered locally | A0-MOA-FMD-CONTROL-GUIDE-2024 | none |
| DIS-026 | `site:woah.org foot and mouth disease swine disease` | WOAH FMD disease page opened/used as international boundary | A1-WOAH-FMD-DISEASE | none |
| DIS-026 / DIS-032 | `site:moa.gov.cn 一类动物疫病 名录 口蹄疫 狂犬病` | MOA Announcement No.573 disease catalog already registered and reused after source check | A0-MOA-573 | none |
| DIS-032 | `CDC rabies veterinarians diagnosis animals official` | CDC veterinarian rabies guidance opened and registered | A1-CDC-RABIES-VETERINARIANS-2025 | none |
| DIS-032 | `CDC rabies diagnostic testing animals laboratory official` | CDC diagnostic testing page registered for laboratory diagnosis boundary | A1-CDC-RABIES-LABORATORY-DIAGNOSIS-2024 | none |
| DIS-004 | `Iowa State SHIC porcine astrovirus factsheet pdf` | SHIC/CFSPH/Iowa State factsheet registered for clinical/diagnostic context | A2-SHIC-CFSPH-PORCINE-ASTROVIRUS-FACTSHEET | A2 only; not used for China regulatory or drug claims |
| DIS-025 | `atypical porcine pestivirus congenital tremor newborn piglets Nature Scientific Reports 2016` | Scientific Reports open article registered for APPV/congenital tremor boundary | A2-NATURE-SCI-REP-APPV-CONGENITAL-TREMOR-2016 | A2 only; not used for China regulatory or drug claims |

## New source pages

- `wiki/sources/A1-CDC-RABIES-VETERINARIANS-2025.md`
- `wiki/sources/A1-CDC-RABIES-LABORATORY-DIAGNOSIS-2024.md`
- `wiki/sources/A2-SHIC-CFSPH-PORCINE-ASTROVIRUS-FACTSHEET.md`
- `wiki/sources/A2-NATURE-SCI-REP-APPV-CONGENITAL-TREMOR-2016.md`

Existing adopted source pages reused after web-first check:

- `wiki/sources/A0-MOA-573.md`
- `wiki/sources/A0-MOA-FMD-CONTROL-GUIDE-2024.md`
- `wiki/sources/A1-WOAH-FMD-DISEASE.md`

## Facts extracted from new/adopted sources

| fact_id | entity | evidence_source_id | page/span/table | evidence_status |
|---|---|---|---|---|
| V11-DIS-026-A0-fmd-catalog-class1 | DIS-026 | A0-MOA-573 | 一二三类动物疫病病种名录; 一类动物疫病; 口蹄疫 | HUMAN_REVIEWED |
| V11-DIS-026-A0-fmd-current-guide | DIS-026 | A0-MOA-FMD-CONTROL-GUIDE-2024 | 家畜口蹄疫防控技术指南; 2024-04-23 | HUMAN_REVIEWED |
| V11-DIS-026-A1-woah-fmd-vesicular-disease | DIS-026 | A1-WOAH-FMD-DISEASE | WOAH FMD disease page | HUMAN_REVIEWED |
| V11-DIS-032-A0-rabies-catalog-class2 | DIS-032 | A0-MOA-573 | 一二三类动物疫病病种名录; 狂犬病 | HUMAN_REVIEWED |
| V11-DIS-032-A1-cdc-rabies-veterinary-escalation | DIS-032 | A1-CDC-RABIES-VETERINARIANS-2025 | CDC veterinarian rabies guidance | HUMAN_REVIEWED |
| V11-DIS-032-A1-cdc-rabies-lab-diagnosis | DIS-032 | A1-CDC-RABIES-LABORATORY-DIAGNOSIS-2024 | CDC rabies diagnostic testing | HUMAN_REVIEWED |
| V11-DIS-004-A2-astrovirus-causality-caution | DIS-004 | A2-SHIC-CFSPH-PORCINE-ASTROVIRUS-FACTSHEET | factsheet clinical/diagnosis boundary | HUMAN_REVIEWED |
| V11-DIS-004-A2-astrovirus-enteric-differential | DIS-004 | A2-SHIC-CFSPH-PORCINE-ASTROVIRUS-FACTSHEET | factsheet enteric differential context | HUMAN_REVIEWED |
| V11-DIS-025-A2-appv-congenital-tremor | DIS-025 | A2-NATURE-SCI-REP-APPV-CONGENITAL-TREMOR-2016 | congenital tremor type A-II | HUMAN_REVIEWED |
| V11-DIS-025-A2-appv-diagnosis-boundary | DIS-025 | A2-NATURE-SCI-REP-APPV-CONGENITAL-TREMOR-2016 | APPV possible cause / differential caution | HUMAN_REVIEWED |

## Entity pages changed

- `wiki/diseases/DIS-004-astroviruses.md`
- `wiki/diseases/DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md`
- `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `wiki/diseases/DIS-032-rabies-virus.md`

## Comparison/rule/synthesis pages changed

- No comparison/rule page body changed in this pass.
- Disease pages now link to existing syndrome/comparison anchors:
  - DIS-004 -> SYN-001, SYN-002, CMP-001, CMP-002
  - DIS-025 -> SYN-005, CMP-008
  - DIS-026 -> SYN-006, CMP-005
  - DIS-032 -> SYN-005, CMP-008

## Validation

- source pages added: 4
- source index updated: yes; total rows 219
- facts added/updated: 10; total facts 2193
- entity pages with new anchors: 4
- comparison links: present on all 4 pages
- high-risk gate result: pass; unsupported dose/course/withdrawal/MRL/food-safety/culling/movement claims are explicitly blocked or routed to A0 evidence.
- unresolved gaps: APPV and astrovirus remain A2-supported clinical entities only; rabies China execution details require A0/locally applicable official procedure; FMD page does not provide local on-site implementation details beyond A0 catalog/control-guide boundary.

## Stop-condition check

- Web search executed first: yes
- Adopted web sources opened and classified: yes
- Source pages created/indexed before entity claims: yes
- Facts extracted from new/adopted web sources: yes
- Entity pages updated: yes
- Remaining gaps recorded: yes
- High-risk unsupported claims blocked: yes

Status remains `partial / source_enriched` because this batch resolves the P1 disease-page fields for four selected high-priority/open-tab entities, but does not claim all 73 disease pages or all drug pages are complete.
