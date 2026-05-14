# Archives

This directory stores historical materials that should remain traceable but should not stay mixed with the active runtime, tooling, and delivery paths.

## Layout

- `history_docs/`: archived plans, walkthroughs, presentations, and superseded implementation notes
- `legacy_scripts/`: one-off dated scripts, batch jobs, backfills, and historical runners
- `runtime_artifacts/`: root-level exports, issues, and generated outputs that are not part of the active source tree
- `issue_records/`: historical issue collections that are kept for audit, not active runtime

## Rules

1. Active runtime code should not depend on files under `archives/`.
2. Historical files should be moved here instead of deleted when they may still be useful for audit or reporting.
3. New archive moves should be documented in `D:\XF-ChongQin\knowledge_change_records`.
