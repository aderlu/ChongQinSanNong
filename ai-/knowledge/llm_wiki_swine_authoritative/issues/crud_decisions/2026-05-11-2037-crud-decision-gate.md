# CRUD Decision

- Target object type: other
- Target object id/path: ai-/knowledge/llm_wiki_swine_authoritative CRUD governance tooling
- Intended action: update
- Why this action is needed: Add a lightweight mandatory CRUD decision gate so every future wiki write records the intended action, reason, old-data handling, risk class, runtime impact, and gold dataset impact before guarded execution.
- Input source type: human review
- New evidence/source: user request and existing governance documents
- Old data exists: yes
- Old data handling: keep
- Authority level: not applicable
- Risk class: not applicable
- Source/fact anchor available: not applicable
- Runtime impact: none
- Gold dataset impact: none
- Deletion or replacement safety check: no referenced object will be silently deleted
- Final decision: allowed

## Reasoning Notes

- Replacement reason, if action is replace: not applicable
- Deletion reason, if action is delete: not applicable
- Downgrade/archive/exclude reason, if applicable: not applicable
- Conflict handling, if new and old data disagree: not applicable
- Required follow-up checks: run `tools/audit_crud_decision.py`; run `tools/run_guarded_wiki_update.py --dry-run -- python -c "print('crud gate smoke')"`; inspect for UTF-8 or syntax issues.

