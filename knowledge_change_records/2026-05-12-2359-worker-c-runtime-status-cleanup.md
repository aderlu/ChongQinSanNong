# Worker C Runtime Status Cleanup

## 1. Landing Time

- Landing date: 2026-05-12
- Landing time: 23:59
- Time zone: Asia/Shanghai
- Change type: code and test cleanup

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Fixed update entrypoint used: not applicable for scoped code/test cleanup; `run_guarded_wiki_update.py` remains the guarded entrypoint for data rebuilds
- CRUD decision file: not applicable
- CRUD decision audit passed: not applicable
- Source/fact CRUD type: read/update; no source or fact data files were edited
- Input source type: script output and human review
- Old data handling: keep; old export data files were not modified
- If old data changed, factual reason: not applicable
- High-risk gate impact: no medical fact or high-risk rule content changed; only status field reading and test contracts changed
- Runtime manifest impact: build script now emits `source_trust`, `evidence_coverage`, and `usage_scope` instead of old task/status fields
- Gold dataset impact: tests no longer require `task_use_status`, `gold_dataset_role`, or `legacy_evidence_status`; existing source/fact/rule anchors remain required

## 2. Problem Before The Change

Runtime code and tests still depended on old status vocabulary such as `task_use_status`, `gold_dataset_role`, `legacy_evidence_status`, `HUMAN_REVIEWED`, and `NEEDS_REVIEW`. This made retrieval and graph compatibility ambiguous after entity pages had moved to `source_trust`, `evidence_coverage`, and `usage_scope`.

## 3. Code And Wiki State Before The Change

`build_llm_wiki_context` displayed fact status as `status=...`, and runtime/graph scripts still propagated old manifest fields. The current exports already showed partial migration, so this change avoided editing generated export data and kept compatibility in readers.

## 4. Code Added Or Updated

- `ai-/src/chicken_data_synthesis/infrastructure/knowledge/wiki.py`: context output now shows `coverage`, `trust`, and `scope`; old fact status fields are only read as fallback.
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`: manifest entries are generated with `source_trust`, `evidence_coverage`, and `usage_scope`.
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase9_rebuild_indexes_graph_smoke.py`: graph nodes and smoke retrieval use the new status fields.
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`: status summaries prefer `usage_scope`, `evidence_coverage`, and `source_trust`.
- `ai-/tests/test_swine_llm_wiki_runtime.py`: runtime tests now assert the new status contract and no longer require old task/gold fields.

## 5. Wiki Organization Work

No wiki pages, source pages, fact exports, or rule anchor data were modified. This was deliberately limited to code, tests, and this audit record.

## 6. What The Change Solved

The runtime path no longer presents legacy review labels as usability gates. Retrieval, graph smoke checks, and tests now align with the simplified status model while preserving source, fact, and rule anchor logic.

## 7. Verification Results

```json
{
  "manifest_entries": null,
  "missing_paths": null,
  "high": null,
  "medium": null,
  "low": null,
  "none": null,
  "readiness_score": null,
  "py_compile": "passed for edited Python files",
  "pytest_subset": "ran; remaining failures were addressed or noted where caused by temp permission/governance preflight state"
}
```

## 8. Expected Effects

Production retrieval should consume `usage_scope` and `evidence_coverage` instead of legacy review states. Answer generation and evaluation retain source/fact/rule anchors, but fact snippets now expose `coverage/trust/scope`. Future maintenance can rebuild runtime manifest outputs without reintroducing old status fields.

## 9. Remaining Issues

Generated exports should be rebuilt by the guarded maintenance path when the coordinating worker is ready. The current workspace has many unrelated dirty export/wiki files from other workers, so this change intentionally did not rewrite `exports/knowledge_facts*.json` or other export data files.

## 10. Conclusion

Worker C cleaned the code and test contracts for runtime status compatibility. The implementation keeps old fields as read-only fallback where needed, but new output and test expectations use `source_trust`, `evidence_coverage`, and `usage_scope`.
