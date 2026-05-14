# Wiki Governance Rules Enforcement

## 1. Landing Time

- Landing date: 2026-05-11
- Landing time: 00:00
- Time zone: Asia/Shanghai
- Change type: governance rule enforcement and documentation hardening

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Source/fact CRUD type: update/rebuild governance documentation only
- Input source type: existing local Markdown governance documents
- Old data handling: keep and strengthen existing guidance
- If old data changed, factual reason: existing maintenance guide existed, but CRUD governance was not explicitly wired as a mandatory entry rule across README, schema, index, checklist, and change-record template
- High-risk gate impact: strengthens future high-risk source/fact handling; no biomedical facts changed
- Runtime manifest impact: none
- Gold dataset impact: strengthens future source/rule provenance requirements; no samples changed

## 2. Problem Before The Change

`WIKI_MAINTENANCE_GUIDE.md` already described source-first maintenance rules, and `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` already described detailed CRUD and old-data handling logic. However, the CRUD governance document was not yet explicitly registered across the main entry points as a mandatory rule.

This created a process risk: future maintainers or scripts could read only README, index, schema, or intake checklist and miss the full CRUD requirements for web sources, local Markdown sources, old version handling, overwrite/delete decisions, downgrade/archive logic, and high-risk medical fact gates.

## 3. Code And Wiki State Before The Change

Before this change:

- `README.md` documented runtime boundary and high-risk boundary, but did not explicitly list both governance documents as mandatory pre-change rules.
- `index.md` had a Governance section, but did not mention `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`.
- `.wiki-schema.md` defined source, usability, gold dataset, and runtime contracts, but did not require change records to explain old-data handling.
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked source registration, facts, placement, guardrails, batch blocks, audit, and records, but did not include a mandatory governance gate.
- `CHANGE_RECORD_TEMPLATE.md` did not have a dedicated governance compliance section.

## 4. Code Added Or Updated

Updated documentation:

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/README.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/index.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/.wiki-schema.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/SOURCE_BATCH_INTAKE_CHECKLIST.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/CHANGE_RECORD_TEMPLATE.md`

No Python runtime, source facts, disease pages, drug pages, rule cards, exports, manifest, graph, or gold dataset samples were modified.

## 5. Wiki Organization Work

This change makes the two governance documents mandatory for all future maintenance:

- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

The mandatory rule is now visible in:

- README entry point.
- Wiki index governance section.
- Wiki schema mandatory governance contract.
- Source and batch intake checklist.
- Change record template.

The maintenance guide now explicitly covers:

- Web-derived sources and facts.
- Local Markdown/PDF/Word/Excel extraction.
- Old-data handling through the CRUD governance document.
- Required explanation for overwrite, delete, downgrade, archive, and migration decisions.

The CRUD governance document now explicitly includes:

- Mandatory enforcement statement.
- Required execution flow.
- Exception handling.
- Validation failure handling.
- Governance compliance block for change records.

## 6. What The Change Solved

This change reduces process drift. Future Wiki updates must now prove that source intake, fact extraction, old-data handling, runtime placement, high-risk gates, validation, and change records follow the two governance documents.

It specifically closes the gap where web information or local Markdown information could be written into the Wiki without first deciding:

- whether the source is authoritative,
- whether old data should be kept, superseded, downgraded, archived, migrated, excluded, or deleted,
- whether a fact is valid or only a candidate,
- whether high-risk claims need A0/A1 support,
- whether runtime pages, evidence expansions, exports, graph, or gold dataset samples need to be rebuilt.

## 7. Verification Results

Manual documentation verification:

```json
{
  "mandatory_governance_docs": [
    "WIKI_MAINTENANCE_GUIDE.md",
    "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md"
  ],
  "entry_points_updated": [
    "README.md",
    "index.md",
    ".wiki-schema.md",
    "SOURCE_BATCH_INTAKE_CHECKLIST.md",
    "CHANGE_RECORD_TEMPLATE.md"
  ],
  "biomedical_facts_changed": 0,
  "runtime_manifest_changed": false,
  "gold_dataset_samples_changed": false
}
```

No runtime audit was required because this change only updates governance documentation and does not alter runtime pages, source facts, exports, or manifest inputs.

## 8. Expected Effects

Future maintenance should now follow a stricter chain:

1. Read `WIKI_MAINTENANCE_GUIDE.md`.
2. Read `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`.
3. Use `SOURCE_BATCH_INTAKE_CHECKLIST.md`.
4. Make source/fact/page/export changes.
5. Run required validation.
6. Record governance compliance in `knowledge_change_records/`.

This should make web-source intake, local Markdown extraction, old version handling, high-risk fact gating, and gold dataset preparation more consistent and auditable.

## 9. Remaining Issues

The governance is now documented and linked across entry points. A future improvement could add an automated documentation lint or preflight script to check that every new change record contains the `Governance Compliance` section.

## 10. Conclusion

This phase turns the maintenance guide and CRUD governance document from standalone references into mandatory Wiki update rules. Future source intake, fact changes, local document extraction, web-derived updates, runtime edits, evidence migration, export rebuilds, and dataset generation must follow these documents and record compliance.

