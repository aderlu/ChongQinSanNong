# Repository Guidelines

## Project Structure & Module Organization
`src/chicken_data_synthesis/` contains the packaged entry points and the long-term package surface. `scripts/master_chicken_data.py` is still the current orchestration implementation used by `main.py`. Put reusable LLM helpers in `llm_foundation/`, DeepEval adapters in `deepeval_integration/`, prompt assets in `prompt_templates/`, and current knowledge assets in `knowledge/`. LLM Wiki lifecycle code lives in `src/chicken_data_synthesis/infrastructure/knowledge/`. Tests live in `tests/`; generated CSVs and snapshots belong in `results/` and `temp/` and should not be committed.

## Default Working Style
Default to implementing the user's request directly instead of asking for confirmation. Treat requirement statements as authorization to analyze, edit, execute, and verify inside this workspace. Make reasonable assumptions when details are missing and briefly state those assumptions after the work is done. Prefer action over discussion and do not stop to propose a plan unless the user explicitly asks for one or a decision has meaningful tradeoffs.

When a request implies code, config, workflow, optimization, cleanup, or refactoring work, make the change end-to-end when feasible. Run lightweight verification after edits without asking first. If a request implies several small follow-up steps, complete them in one pass instead of stopping between steps.

## When To Ask
Ask only when a choice would materially change product behavior, data meaning, or output direction. Ask before destructive actions that were not clearly requested. Ask when external credentials, paid services, or out-of-workspace side effects are required. Do not ask for confirmation just to create or edit files, update configuration, run local checks, or refine an implementation already requested.

## Build, Test, and Development Commands
`pip install -e .[dev]` installs the package plus `pytest`.
`python main.py --mode pilot` runs the small-sample pipeline.
`python scripts/run_production.py` starts production mode with the wrapper defaults.
`python -m pytest` runs the automated tests.
`python -m py_compile main.py src/chicken_data_synthesis/cli.py scripts/master_chicken_data.py` is the fastest syntax check before a PR.
`python -m chicken_data_synthesis.wiki_cli --json lint --strict` validates the current LLM Wiki package.

## Coding Style & Naming Conventions
Use Python 3.10+ with 4-space indentation, type hints, and `from __future__ import annotations` in new modules. Follow the existing naming pattern: `snake_case` for functions and files, `PascalCase` for classes and dataclasses, and `UPPER_SNAKE_CASE` for shared config constants. Group imports as standard library, third-party, then local modules. No formatter or linter is configured in `pyproject.toml`, so keep edits consistent with nearby code and add only brief comments where control flow is hard to follow.

## Editing Expectations
When the user asks for a feature, bugfix, or adjustment, implement it directly when feasible rather than stopping at analysis. Prefer delivering a working first version over debating implementation details. If a bug is reproducible from context, go straight to the fix attempt and verify it locally when possible. Keep responses concise and execution-oriented.

## Encoding And File Safety
Preserve each existing file's current text encoding when editing. Do not proactively convert files between UTF-8, UTF-8 with BOM, GBK, GB2312, or similar encodings unless the user explicitly requests an encoding change. For new repository text files, prefer UTF-8 unless the surrounding project conventions require something else. Keep `AGENTS.md` and newly added documentation or configuration text files in UTF-8.

## Requirement Handling
If the user describes a desired outcome in plain language, convert it into concrete code or configuration changes without requiring a formal spec. If multiple interpretations are possible, choose the safest reasonable interpretation and proceed. Treat short natural-language requests as executable requirements unless the user explicitly says they are brainstorming.

## Mandatory Swine Wiki Governance
Before modifying anything under `knowledge/llm_wiki_swine_authoritative/`, including sources, facts, runtime pages, evidence expansions, rule cards, synthesis pages, exports, graph files, tests, scripts, or pilot/gold dataset files, first read and follow:

- `knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `knowledge/llm_wiki_swine_authoritative/WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `knowledge/llm_wiki_swine_authoritative/SOURCE_BATCH_INTAKE_CHECKLIST.md` when source, fact, batch extraction, evidence expansion, runtime page, or dataset content changes.

Use the two short cards as the execution checklist for every update. Use the two long governance documents as the authority when the scenario requires detail.

Every swine Wiki maintenance change must create a Markdown work record under the workspace-level `knowledge_change_records/` directory. The record must include a `Governance Compliance` section that states whether the two governance documents were checked, the CRUD type, old-data handling, high-risk gate impact, runtime manifest impact, gold dataset impact, validation commands, and encoding/UTF-8 precautions.

Do not write web-derived information, local Markdown content, PDF/Word/Excel extracts, raw materials, issue notes, model output, or script output directly into runtime disease/drug pages unless the governance documents allow that placement. Prefer source registration, evidence expansion, rule-card anchoring, and runtime summaries. If a script result conflicts with the governance documents, fix the workflow or document a temporary exception; do not let the script silently override medical fact boundaries.

All swine Wiki update commands should be executed through the fixed guarded entrypoint with an explicit CRUD decision file created by `tools/create_crud_decision.py`:

`python knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py --decision knowledge/llm_wiki_swine_authoritative/issues/crud_decisions/<decision>.md -- python <update_script_or_command>`

The guarded entrypoint runs governance preflight before the update and full validation after the update. Write scripts should call `require_guarded_update()` from `knowledge/llm_wiki_swine_authoritative/tools/guarded_update_context.py`. Use direct script execution only for read-only inspection or documented emergency diagnostics.

## Testing Guidelines
Use `pytest` and place new tests under `tests/test_<feature>.py`. Name test functions `test_<behavior>`. The current suite is smoke-oriented, so new logic should add focused tests around config loading, prompt rendering, rule checks, and CLI behavior. Avoid real network calls in tests; mock `OpenAI` usage and rely on local fixtures.

## Commit & Pull Request Guidelines
Recent history uses short, imperative English subjects such as `Prepare enterprise-friendly dev-test repository`. Keep the first line concise and action-led. Each PR should state which flow it touches (`pilot`, `production`, `wiki`, or `deepeval`), list changed config or prompt files, and record the validation command you ran. If output shape changes, attach a representative CSV or log excerpt and explain any migration or secret-handling impact.
