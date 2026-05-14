# Source And Batch Intake Checklist

Use this checklist before adding any new source, batch extraction, evidence enhancement block, or generated evidence file to the swine LLM wiki.

This checklist is mandatory. It must be used together with:

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

No web-derived source, local Markdown/PDF/Word/Excel source, extracted fact, batch enhancement block, runtime edit, evidence expansion file, index rebuild, or pilot/gold dataset sample should be accepted unless the governance and CRUD decisions are explicit.

## 0. Mandatory Governance Gate

- [ ] `WIKI_MAINTENANCE_GUIDE.md` has been read and applied.
- [ ] `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` has been read and applied.
- [ ] `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` has been read and applied.
- [ ] `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` has been read and applied.
- [ ] The update will run through `tools/run_guarded_wiki_update.py`, or the exception is documented.
- [ ] The operation type is identified: create, read/query, update, delete, migrate, archive, downgrade, exclude, rebuild.
- [ ] The input source type is identified: web, local Markdown, PDF, Word, Excel, scanned document, raw file, historical issue, model output, script output, human review.
- [ ] Old data handling is explicit: keep, update, supersede, downgrade, archive, migrate to evidence expansion, exclude from runtime, or delete with justification.
- [ ] If old data is overwritten or removed from runtime, the reason is documented: rule update, obsolete version, source conflict, fact error, encoding damage, duplicate data, page-size compaction, or task-gate change.

## 1. Source Registration

- [ ] A stable `source_id` has been assigned.
- [ ] Source title, author or institution, date, jurisdiction, language, and source type are recorded where available.
- [ ] Authority level is clear:
  - [ ] official/regulatory source,
  - [ ] label or product instruction,
  - [ ] textbook or handbook,
  - [ ] peer-reviewed article,
  - [ ] internal extraction or evaluation artifact,
  - [ ] other source requiring source expansion or authority-level clarification.
- [ ] Source limitations are recorded.
- [ ] The source is not being used beyond its authority level.

## 2. Fact Extraction Requirements

- [ ] Every extracted fact has a `source_id`.
- [ ] Every extracted fact has a stable `fact_id` or equivalent local identifier.
- [ ] Page, table, section, line, URL, or other source anchor is retained where available.
- [ ] Facts with incomplete anchors are marked with `source_status=source_missing` or `fact_validity=insufficient_anchor`.
- [ ] Candidate facts are not promoted to executable recommendations.
- [ ] Missing fields are not guessed.
- [ ] Usability is mapped through `source_status`, `fact_validity`, `authority_level`, `risk_class`, and `task_use_status`, not legacy review states.

## 3. Runtime Placement Decision

- [ ] The extracted material has been classified:
  - [ ] compact runtime summary,
  - [ ] evidence expansion,
  - [ ] rule card,
  - [ ] synthesis/policy page,
  - [ ] issue/audit report only.
- [ ] Large extraction blocks are placed under `wiki/evidence_expansions/`.
- [ ] Runtime pages receive only concise summaries or moved-evidence placeholders.
- [ ] Runtime page size remains below the maintenance threshold where possible.
- [ ] No raw extraction dump is inserted directly into `wiki/diseases/` or `wiki/drugs/`.

## 4. Guardrail Requirements

- [ ] Disease content references `RC-DX-001` where diagnosis is involved.
- [ ] Regulatory, quarantine, culling, reporting, inspection, or movement-control content references `RC-DISEASE-REGULATORY-001` or `RC-REGULATORY-CURRENT-001`.
- [ ] Drug, dose, route, course, compatibility, contraindication, or prescription content references `RC-DRUG-001`.
- [ ] Withdrawal period, MRL, residue, edible product, or food-safety content references `RC-WITHDRAWAL-MRL-001`.
- [ ] Synthesis or evaluation content references `RC-SYNTHESIS-SCOPE-001` and `RC-EVAL-RUBRIC-001`.
- [ ] Partial pages include `RC-PARTIAL-GAP-ROUTING-001`.

## 5. Batch Enhancement Block Requirements

- [ ] Batch block markers use the standard format:

```text
<!-- BATCH_NAME_START -->
...
<!-- BATCH_NAME_END -->
```

- [ ] Batch block names are stable and unique enough for future migration.
- [ ] Large batch blocks are stored in evidence expansion files.
- [ ] Runtime placeholders point to the evidence expansion path.
- [ ] Runtime placeholders state that the block is not default retrieval.
- [ ] Runtime placeholders mention applicable guardrails.

## 6. Audit Requirements

Run the one-command maintenance check after the change:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

If a specific failure needs investigation, run the component commands:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py
```

Required acceptance criteria:

- [ ] `missing_paths` is 0.
- [ ] high-risk count is 0.
- [ ] medium-risk count is 0, or the exception is documented.
- [ ] readiness score is at least 99.
- [ ] no new unbounded runtime page is introduced.
- [ ] governance compliance preflight passes.
- [ ] runtime damaged count is 0.

## 7. Work Record Requirements

- [ ] A change record is added under `knowledge_change_records/`.
- [ ] The record includes landing time to hour and minute.
- [ ] The record explains the before state, code state, changes, verification, expected effects, and remaining issues.
- [ ] Any temporary risk exception is explicitly listed.
