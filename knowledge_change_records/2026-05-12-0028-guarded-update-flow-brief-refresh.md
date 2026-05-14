# Guarded Update Flow Brief Refresh

## 1. Landing Time

- Landing date: 2026-05-12
- Landing time: 00:28
- Time zone: Asia/Shanghai
- Change type: documentation update

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Fixed update entrypoint used: not applicable for documentation-only update; current fixed entrypoint is `run_guarded_wiki_update.py`
- CRUD decision file: not applicable; documentation reflects the existing bound CRUD flow
- CRUD decision audit passed: not applicable
- Source/fact CRUD type: update
- Input source type: human review
- Old data handling: update
- If old data changed, factual reason: no source or fact data changed
- High-risk gate impact: documents the stricter bound CRUD preflight
- Runtime manifest impact: none
- Gold dataset impact: none

## 2. Problem Before The Change

`WIKI_GUARDED_UPDATE_FLOW_BRIEF_CN.md` still described the older latest-decision workflow and old command format. It did not explain `create_crud_decision.py`, governance document hashes, explicit `--decision`, planned-command binding, or guarded environment variables.

## 3. Code And Wiki State Before The Change

The current code already requires a bound decision file and guarded environment for write scripts, but the brief Chinese flow document was stale and could lead maintainers to use the old command form.

## 4. Code Added Or Updated

- Updated `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_GUARDED_UPDATE_FLOW_BRIEF_CN.md`.
- Added this work record under `knowledge_change_records/`.

## 5. Wiki Organization Work

No runtime page, source, fact, evidence expansion, graph, export, or gold dataset content was changed.

## 6. What The Change Solved

The brief flow document now matches the active implementation: decision generation reads governance documents, the decision file records hashes and planned command, the guarded entrypoint requires `--decision`, CRUD audit checks command binding, and write scripts can reject direct execution.

## 7. Verification Results

Planned verification:

```powershell
python ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py
```

Summary JSON:

```json
{
  "manifest_entries": null,
  "missing_paths": null,
  "high": null,
  "medium": null,
  "low": null,
  "none": null,
  "readiness_score": null
}
```

## 8. Expected Effects

Future maintainers can follow the brief document without accidentally using the obsolete latest-decision workflow. Production retrieval, answer generation, evaluation, and gold dataset behavior are unchanged.

## 9. Remaining Issues

The longer execution-flow documents should be refreshed later so all explanatory documents use the same bound CRUD vocabulary.

## 10. Conclusion

This is a documentation alignment change. It improves audit clarity and reduces the chance of bypassing the current bound CRUD workflow.
