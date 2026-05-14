# DIS-038 Brucellosis CFSPH Authority Refresh / 2026-05-13

## Scope

This evidence expansion records the web-access acquisition and controlled refresh for `DIS-038-brucella-suis-brucellosis`.

## Web Access Acquisition

- Skill path: `C:/Users/admin/.codex/skills/web-access/SKILL.md`
- Dependency precheck: `node C:/Users/admin/.codex/skills/web-access/scripts/check-deps.mjs`
- Browser/CDP proxy confirmed available through `http://localhost:3456/targets`
- Authority source discovered from CFSPH technical factsheet index and downloaded as raw PDF through the governance workflow

## Raw Evidence

- `raw/web/web_access_dis038_brucellosis_20260513/A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.pdf`
- `raw/web/web_access_dis038_brucellosis_20260513/A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026-pages.txt`

## Source Added

- `A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`

## Facts Added

- `DIS038-WEB-005-cfsph-transmission-exposure`
- `DIS038-WEB-006-cfsph-clinical-pattern`
- `DIS038-WEB-007-cfsph-zoonotic-boundary`

## Governance Boundary

- This refresh is additive and keeps all existing A0/A1/A2 source and fact records.
- The new source is A2, not A0 or A1.
- The new source cannot replace China-specific reporting, quarantine, culling, movement, compensation, slaughter, food-chain release, vaccination, dose, withdrawal-period, or MRL rules.
- Runtime additions remain short source/fact-routed summaries. Full PDF text stays outside runtime.
