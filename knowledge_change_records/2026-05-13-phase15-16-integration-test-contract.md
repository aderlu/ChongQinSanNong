# Phase 15/16 Integration Test Contract Record

## Context

Phase 12/13/14 already had smoke tests for wiki-first sample planning, answer skeletons, and two-stage deterministic sample generation. This update extends the integration verification surface for the downstream Phase 15 evaluator and Phase 16 training-set export steps without changing runtime wiki content or business generation scripts.

## Changes

- Updated `ai-/tests/test_swine_wiki_first_generation_pipeline.py`.
- Added Phase 15 contract tests for gate precedence and evaluated sample fields.
- Added Phase 16 contract tests for layer-based export, SFT accepted-only filtering, preserved `evidence_anchors`, and `messages` role shape.
- Added an end-to-end Phase 12 -> 16 smoke test that runs once Phase 15/16 scripts are present.
- Phase 15/16 tests explicitly skip when the corresponding worker scripts are not yet present in the workspace, preserving the current Phase 12/13/14 regression signal.

## Current Boundary

The current workspace snapshot does not contain:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase15_evaluate_generated_samples.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase16_export_training_sets.py`

The new tests are therefore ready to activate automatically after those scripts land with the expected CLI contract:

- `--wiki-root <path>`
- `--date <stamp>`
- JSON summary on stdout

## Governance Compliance

- Governance documents checked: `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`, `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`, `WIKI_MAINTENANCE_GUIDE.md`, and `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`.
- CRUD type: modify tests; add audit/work record.
- Data layer impacted: test code and workspace-level `knowledge_change_records`; no runtime disease/drug/source/fact/evidence page content changed.
- Old-data handling: no old data removed, overwritten, downgraded, or migrated.
- High-risk gate impact: positive. Tests assert Phase 15 cannot allow a high judge score to override failed fact or hard-gate checks.
- Runtime manifest impact: none. No manifest rebuild required.
- Gold dataset impact: no dataset content changed. Phase 16 tests verify accepted-only SFT export behavior once the exporter exists.
- Validation command: `py -m pytest ai-\tests\test_swine_wiki_first_generation_pipeline.py -q` returned `8 passed, 4 skipped`; skipped tests are Phase 15/16 activation tests because the scripts are not present yet.
- Encoding/UTF-8 precautions: new record written as UTF-8 plain text; tests use UTF-8 JSON/JSONL helpers and do not change existing knowledge encodings.
