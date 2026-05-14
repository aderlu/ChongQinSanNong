# DIS-038 Brucellosis Authority Web Refresh / 2026-05-12

## Scope

This evidence expansion records the web-access authority refresh for `DIS-038-brucella-suis-brucellosis`.

## Web Access Acquisition

- Tool path used: `C:/Users/admin/.codex/skills/web-access/SKILL.md`.
- Dependency precheck: `node C:/Users/admin/.codex/skills/web-access/scripts/check-deps.mjs` passed with Node, Chrome and proxy ready.
- Acquisition method: Chrome CDP proxy opened official source pages and extracted rendered page text on 2026-05-12.

## Sources Updated

- `A1-USDA-APHIS-SWINE-BRUCELLOSIS`: USDA APHIS swine brucellosis page, last modified 2025-07-30.
- `A1-WOAH-BRUCELLOSIS`: WOAH brucellosis disease page.
- `A2-CDC-BRUCELLOSIS`: CDC About Brucellosis page, dated 2024-05-02.

## Facts Added

- `DIS038-WEB-001-aphis-causation-reproductive-zoonotic`
- `DIS038-WEB-002-aphis-wild-swine-and-report-routing`
- `DIS038-WEB-003-woah-listed-transmission-diagnostic`
- `DIS038-WEB-004-cdc-occupational-public-health-boundary`

## Governance Boundary

- This refresh is additive.
- Existing source and fact records are kept; no source, fact, runtime page, rule card or gold sample is deleted.
- A1/A2 sources do not replace China A0 official control rules.
- Runtime additions remain short source/fact-routed summaries; full web pages are not copied into runtime.
