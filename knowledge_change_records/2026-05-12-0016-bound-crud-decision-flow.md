# Bound CRUD Decision Flow

## 1. Landing Time

- Landing date: 2026-05-12
- Landing time: 00:16
- Time zone: Asia/Shanghai
- Change type: governance tooling update

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Fixed update entrypoint used: not applicable for editing the entrypoint itself
- CRUD decision file: not applicable; this change repairs the CRUD decision workflow
- CRUD decision audit passed: pending verification
- Source/fact CRUD type: update
- Input source type: human review
- Old data handling: update
- If old data changed, factual reason: no source or fact content changed
- High-risk gate impact: strengthens preflight binding and prevents unbound high-risk update execution
- Runtime manifest impact: none
- Gold dataset impact: none

## 2. Problem Before The Change

The previous CRUD gate checked the latest decision file after it already existed. It did not prove that governance documents were read before decision creation, did not bind the decision to the update command, and allowed write scripts to be run directly outside the guarded entrypoint.

## 3. Code And Wiki State Before The Change

`audit_crud_decision.py` parsed the latest Markdown file under `issues/crud_decisions/`. `run_guarded_wiki_update.py` invoked that audit without passing a specific decision file or actual command. Write scripts had no shared guarded-context check.

## 4. Code Added Or Updated

- `tools/create_crud_decision.py`: reads required governance documents, records hashes, and writes a bound decision file.
- `tools/audit_crud_decision.py`: validates governance hashes and planned-command binding.
- `tools/run_guarded_wiki_update.py`: requires `--decision`, audits that file against the actual command, and passes guarded environment variables to update scripts.
- `tools/guarded_update_context.py`: provides `require_guarded_update()` for write scripts.
- `tools/apply_dis026_fmd_authority_web_refresh.py` and `tools/apply_v11_p1_batch2.py`: now require guarded context.
- `CRUD_DECISION_TEMPLATE.md`, `CRUD_DECISION_GATE.md`, `AGENTS.md`, and runtime tests were updated for the bound flow.

## 5. Wiki Organization Work

No source, fact, runtime page, evidence expansion, graph, or dataset content was changed. The change only updates governance tooling and documentation.

## 6. What The Change Solved

The flow now records which governance document versions were read before a decision was generated. The guarded entrypoint no longer accepts an implicit latest decision file. The CRUD audit can reject mismatched planned and actual commands, and guarded write scripts can reject direct execution.

## 7. Verification Results

Verification commands:

```powershell
python -m py_compile ai-/knowledge/llm_wiki_swine_authoritative/tools/create_crud_decision.py ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_crud_decision.py ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py ai-/knowledge/llm_wiki_swine_authoritative/tools/guarded_update_context.py
python ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py
python -m pytest ai-/tests/test_swine_llm_wiki_runtime.py -q
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

Production retrieval and answer generation are unchanged. Future maintenance is safer because CRUD decisions are created from a documented governance context and checked against the exact update command.

## 9. Remaining Issues

Additional write scripts should gradually adopt `require_guarded_update()` when they are next touched. A later enhancement can compare the decision target path with the actual filesystem diff after execution.

## 10. Conclusion

This update changes the CRUD flow from latest-file inference to explicit decision binding. It improves auditability without changing medical knowledge content, runtime retrieval content, or gold dataset semantics.
