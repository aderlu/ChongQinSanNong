# CRUD Decision Template

Prefer creating this file with `tools/create_crud_decision.py` before running any guarded wiki update that changes source, fact, runtime page, evidence expansion, rule card, export, graph, or gold dataset data.

The decision file is intentionally short. It forces the maintainer or LLM agent to state what is being changed, why the change is needed, how old data will be handled, and whether runtime or gold dataset outputs are affected.

## Governance Context

- Decision generated at:
- Governance documents read:
- Governance document hashes JSON:
- CRUD template hash:
- Planned command:

## CRUD Decision

- Target object type: source/fact/runtime_page/evidence_expansion/rule_card/synthesis/export/graph/gold_sample/other
- Target object id/path:
- Intended action: create/read/update/replace/delete/archive/downgrade/exclude/rebuild
- Why this action is needed:
- Input source type: web/local Markdown/PDF/Word/Excel/raw/issue/model output/script output/human review/not applicable
- New evidence/source:
- Old data exists: yes/no/unknown
- Old data handling: keep/update/supersede/downgrade/archive/migrate/exclude/delete/not applicable
- Authority level: A0/A1/A2/SRC/RC-RULE/not applicable
- Risk class: normal/diagnostic/drug_boundary/high_regulatory/withdrawal_mrl_residue/food_safety/not applicable
- Source/fact anchor available: yes/no/not applicable
- Runtime impact: none/add/update/remove/rebuild
- Gold dataset impact: none/add/update/exclude/block/rebuild
- Deletion or replacement safety check: no referenced object will be silently deleted
- Final decision: allowed/blocked/manual_review

## Reasoning Notes

- Replacement reason, if action is replace:
- Deletion reason, if action is delete:
- Downgrade/archive/exclude reason, if applicable:
- Conflict handling, if new and old data disagree:
- Required follow-up checks:
