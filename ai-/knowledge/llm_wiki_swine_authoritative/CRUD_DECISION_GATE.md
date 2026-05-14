# CRUD Decision Gate

This gate is mandatory for every real write to the swine authoritative LLM Wiki.

Before running `tools/run_guarded_wiki_update.py`, create a decision file with `tools/create_crud_decision.py` under `issues/crud_decisions/`.

The decision file must be passed explicitly to `tools/run_guarded_wiki_update.py` with `--decision`. `tools/audit_crud_decision.py` checks that the decision file contains governance document hashes and that its planned command matches the actual update command. The update is blocked when any required decision field is missing, blank, unsafe, stale, unbound, or inconsistent with high-risk source rules.

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py --decision issues/crud_decisions/<decision>.md -- python knowledge/llm_wiki_swine_authoritative/tools/<update_script>.py
```

## Required Judgment

Each decision file must state:

- what object is being changed,
- what CRUD action is intended,
- why the action is needed,
- whether old data exists,
- how old data will be handled,
- which authority level supports the action,
- which risk class applies,
- whether source or fact anchors exist,
- whether runtime outputs are affected,
- whether gold dataset outputs are affected,
- whether deletion or replacement can occur without silently deleting referenced data,
- whether the final decision is allowed, blocked, or manual review.

## Simple Rules

- Create: allowed only when the object is not already represented and the source or fact anchor is sufficient.
- Update: allowed when the old data is incomplete, unsafe, stale, poorly anchored, oversized, or affected by a rule change.
- Replace: allowed only when old data handling is explicitly supersede, downgrade, archive, migrate, or exclude.
- Delete: allowed only when old data handling is explicitly archive, exclude, delete, or migrate, and the decision states that no referenced object will be silently deleted.
- High-risk data: drug, regulatory, withdrawal, MRL, residue, food safety, and similar high-risk claims require A0/A1 or rule-card authority before positive generation use.
