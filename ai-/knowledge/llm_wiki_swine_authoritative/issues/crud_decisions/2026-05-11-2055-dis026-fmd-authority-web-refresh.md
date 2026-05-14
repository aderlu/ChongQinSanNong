# CRUD Decision

- Target object type: source
- Target object id/path: DIS-026 foot-and-mouth disease authority web refresh
- Intended action: create
- Why this action is needed: DIS-026 already has China A0 and textbook anchors, but the runtime page still benefits from explicit international authority anchors for FAO disease impact/control framing, USDA APHIS animal-owner reporting and subtype/vaccine-boundary framing, and USDA NAHLN foreign animal disease testing preparedness. The update will add source pages, source-index rows, source-anchored facts, and a compact runtime enrichment block without replacing old data.
- Input source type: web
- New evidence/source: FAO foot-and-mouth disease official page; USDA APHIS Foot-and-Mouth Disease page; USDA APHIS NAHLN Surveillance and Preparedness page
- Old data exists: yes
- Old data handling: keep
- Authority level: A1
- Risk class: high_regulatory
- Source/fact anchor available: yes
- Runtime impact: update
- Gold dataset impact: update
- Deletion or replacement safety check: no referenced object will be silently deleted
- Final decision: allowed

## Reasoning Notes

- Replacement reason, if action is replace: not applicable; this is an additive source/fact enrichment.
- Deletion reason, if action is delete: not applicable.
- Downgrade/archive/exclude reason, if applicable: not applicable.
- Conflict handling, if new and old data disagree: no conflict found; international A1/A2-style source boundaries remain subordinate to China A0 execution rules for China-specific reporting, culling, movement, vaccination program, and food-chain claims.
- Required follow-up checks: run guarded update; rebuild source/fact status, runtime manifest, graph, graph diff, readiness, encoding audit, and tests through `run_guarded_wiki_update.py`.

