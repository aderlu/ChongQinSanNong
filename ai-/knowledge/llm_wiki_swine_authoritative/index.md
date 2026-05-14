# Swine Disease LLM Wiki

- domain: swine_disease
- initialized: 2026-05-06
- runtime_manifest: `exports/runtime_core_manifest.json`
- runtime_exclude_patterns: `exports/runtime_exclude_patterns.json`
- baseline_readiness: 99/100 as of 2026-05-09

## Runtime Entry Points

- `wiki/diseases/`: compact disease runtime pages for recall, clinical summaries, differential routing, diagnosis boundaries, prevention/control framing, and evidence gaps.
- `wiki/drugs/`: compact drug runtime pages for recall, label/source boundary checks, negative traps, and generation/evaluation guardrails.
- `wiki/rule_cards/`: hard-block and scoring rules for generation, evaluation, drug safety, diagnosis, citation, and regulatory boundaries.
- `wiki/syndromes/`: syndrome entry points for case generation and differential routing.
- `wiki/comparisons/`: differential diagnosis and contrastive evaluation support.
- `wiki/synthesis/`: selected policy, generation, and evaluation pages. Large treatment or prescription matrices are excluded from default runtime retrieval.
- `wiki/sources/`: source metadata and traceability pages.

## Governance

- Mandatory governance documents:
  - `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
  - `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
  - `WIKI_MAINTENANCE_GUIDE.md`
  - `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- All source intake, web-derived information, local Markdown/PDF/Word/Excel extraction, runtime page edits, evidence migration, index rebuilds, graph rebuilds, and gold dataset generation must follow the two short cards plus the two full governance documents before any wiki content is changed.
- All update commands that can modify this wiki should run through `tools/run_guarded_wiki_update.py`.
- Use `exports/runtime_core_manifest.json` as the positive allowlist for production and evaluation retrieval.
- Do not default-load `raw/`, `issues/`, sessions, graph exports, backup files, or large treatment matrices.
- A fact can be used when its source is clear, its data is valid, and its authority level matches the requested task.
- Legacy review-oriented states such as `HUMAN_REVIEWED` and `NEEDS_REVIEW` must not be used as direct allow/block gates.
