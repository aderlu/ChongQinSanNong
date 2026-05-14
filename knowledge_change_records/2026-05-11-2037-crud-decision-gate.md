# CRUD Decision Gate Change Record

## 1. Landing Time

- Landing date: 2026-05-11
- Landing time: 20:37
- Time zone: Asia/Shanghai
- Change type: governance tooling update

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Fixed update entrypoint used: not applicable for this code edit; guarded dry-run verification was performed after the edit
- CRUD decision file: `ai-/knowledge/llm_wiki_swine_authoritative/issues/crud_decisions/2026-05-11-2037-crud-decision-gate.md`
- CRUD decision audit passed: pending verification at authoring time
- Source/fact CRUD type: update
- Input source type: human review
- Old data handling: keep
- If old data changed, factual reason: no source, fact, runtime page, evidence expansion, rule card, or gold sample was replaced or deleted
- High-risk gate impact: adds a preflight blocker for unsafe high-risk CRUD decisions
- Runtime manifest impact: none
- Gold dataset impact: none

## 2. Problem Before The Change

The wiki already had strong governance documents and a guarded update entrypoint, but the execution path did not require a compact, machine-checkable CRUD decision file before a write. That meant a maintainer or LLM agent could describe the change in prose after the fact, while the preflight could not directly verify whether the intended action, reason, old-data handling, replacement/delete safety, runtime impact, and gold dataset impact had been judged before execution.

This was especially risky for operations such as replace, delete, downgrade, archive, and high-risk veterinary facts. The rules existed, but the runtime gate did not yet force an explicit decision record for every update.

## 3. Code And Wiki State Before The Change

Before this change, `tools/run_guarded_wiki_update.py` ran only `audit_governance_compliance.py` as preflight. That script checked required governance documents, entrypoints, required tools, and the latest change record, but it did not parse an operation-specific CRUD decision.

The change record template already asked for CRUD type and old-data handling, but that was a reporting artifact rather than a pre-execution gate.

## 4. Code Added Or Updated

- Added `ai-/knowledge/llm_wiki_swine_authoritative/CRUD_DECISION_TEMPLATE.md`.
  - Purpose: provide a short required decision form for every real write.
  - Input: maintainer or LLM-filled CRUD judgment.
  - Output: a Markdown decision file under `issues/crud_decisions/`.
  - Runtime impact: none.
  - Audit/report only: yes.

- Added `ai-/knowledge/llm_wiki_swine_authoritative/CRUD_DECISION_GATE.md`.
  - Purpose: document the lightweight gate and simple CRUD rules in stable UTF-8/ASCII text.
  - Runtime impact: none.
  - Audit/report only: yes.

- Added `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_crud_decision.py`.
  - Purpose: parse the latest CRUD decision file and block unsafe or incomplete decisions.
  - Checks: required fields, blank fields, final decision, replace/delete old-data handling, reference safety statement, high-risk authority gate, source/fact anchor availability, runtime/gold impact assessment.
  - Runtime impact: none.
  - Audit/report only: yes.

- Updated `ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py`.
  - Purpose: run both governance compliance and CRUD decision preflights before any update command.
  - Runtime impact: none by itself; it blocks unsafe future writes.

- Updated `ai-/knowledge/llm_wiki_swine_authoritative/CHANGE_RECORD_TEMPLATE.md`.
  - Purpose: require future work reports to point to the CRUD decision file and state whether the CRUD decision audit passed.

- Added `ai-/knowledge/llm_wiki_swine_authoritative/issues/crud_decisions/2026-05-11-2037-crud-decision-gate.md`.
  - Purpose: decision record for this governance tooling update.

## 5. Wiki Organization Work

No source, fact, runtime, evidence expansion, rule card, synthesis, graph, or gold dataset content was reorganized. This change only adds a pre-execution decision layer and reporting artifacts.

The existing mandatory short card appears to contain pre-existing mojibake in the current terminal view. To avoid worsening encoding damage, this change did not rewrite that file. Instead, a separate `CRUD_DECISION_GATE.md` was added in stable ASCII/UTF-8, and the main change template was updated safely.

## 6. What The Change Solved

The update path now requires a concrete answer to these questions before future writes:

- What object is being changed?
- Is the action create, update, replace, delete, archive, downgrade, exclude, or rebuild?
- Why is the action needed?
- Does old data exist?
- Will old data be kept, superseded, downgraded, archived, migrated, excluded, or deleted?
- Does the action affect runtime output?
- Does the action affect gold dataset output?
- Is a high-risk claim backed by an adequate authority level?
- Is a delete or replace operation protected against silent removal of referenced data?

This converts CRUD governance from a prose-only expectation into a small executable preflight gate.

## 7. Verification Results

Verification commands to run:

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'

python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_crud_decision.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py --dry-run -- python -c "print('crud gate smoke')"
```

Initial expected result:

```json
{
  "crud_decision_audit": "passed",
  "guarded_dry_run": "passed",
  "runtime_manifest_impact": "none",
  "gold_dataset_impact": "none"
}
```

## 8. Expected Effects

Future production updates should become easier to audit because every write has a pre-execution decision file. Replacement and deletion will be harder to perform accidentally. High-risk veterinary facts will have an additional preflight check before positive runtime or gold dataset use.

The expected operational cost is low: maintainers only fill one compact Markdown decision file before running the existing guarded entrypoint.

## 9. Remaining Issues

The current mandatory short card displays mojibake in the terminal. That appears to be pre-existing encoding damage or terminal decoding mismatch. A separate cleanup should decide whether to repair or regenerate the affected Chinese governance documents from a known-good source.

The CRUD decision audit is intentionally lightweight. It does not yet perform deep graph reference analysis. A later enhancement could connect it to graph/source/fact indexes so delete and replace operations are verified against actual references, not only the decision statement.

## 10. Encoding Protection Measures

- New files were written as UTF-8 through `apply_patch`.
- New governance gate files use mostly ASCII text to minimize encoding ambiguity.
- Python scripts read and write with `encoding="utf-8"`.
- `run_guarded_wiki_update.py` already sets `PYTHONIOENCODING=utf-8` for subprocesses.
- The pre-existing mojibake short card was not rewritten during this change.

