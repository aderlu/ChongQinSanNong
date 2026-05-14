# 2026-05-12 Fact/Export Status Simplification Record

## Scope

本次清理承接实体页状态简化工作，将猪病 LLM wiki 的 fact、active exports、runtime manifest、gold readiness、pilot dataset 与图谱生成链路统一到新版状态契约：

- `source_trust`: `authoritative` / `needs_source_check`
- `evidence_coverage`: `complete` / `partial` / `minimal`
- `usage_scope`: `retrieval`, `diagnosis_support`, `differential_support`, `control_support`, `regulatory_boundary`, `treatment_boundary`, `drug_boundary`, `positive_drug_candidate`, `gold_candidate`, `gap_routing`, `audit_only`, `negative_trap`

## Data Changes

- `ai-/knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts.json`
  - 2230 facts retained.
  - Added/normalized `source_trust`, `evidence_coverage`, `usage_scope`.
  - Removed old review/status fields such as `evidence_status`, `legacy_evidence_status`, `task_use_status`, `source_status`, `fact_validity`.

- `ai-/knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts_status_index.json`
  - 2230 facts retained.
  - Uses the same simplified contract as the primary facts export.

- Active derived exports rebuilt or normalized:
  - `runtime_core_manifest.json`
  - `runtime_core_manifest_summary.md`
  - `runtime_exclude_patterns.json`
  - `gold_dataset_readiness_index.csv`
  - `drug_gold_role_index.csv`
  - `exporter_hard_block_rules.json`
  - `source_authority_status_index.csv`
  - `wiki/graph-data.json`
  - `wiki/knowledge-graph.md`
  - `wiki/knowledge-graph.html`
  - `exports/pilot_gold_dataset/*.jsonl`

## Code Changes

- `build_runtime_core_manifest.py`
  - Runtime manifest entries now expose `source_trust`, `evidence_coverage`, `usage_scope`, `authority_level`, and `risk_class` as the primary status contract.
  - Removed generated `source_status` and `fact_validity` from manifest entries.

- `phase6_7_review_status_and_gold_dataset.py`
  - Gold readiness and drug role exports now derive generation/evaluation decisions from `usage_scope` plus evidence/trust/risk fields.
  - Removed `task_use_status`, `gold_dataset_role`, `drug_gold_role`, and legacy review counters from active outputs.

- `phase8_rule_card_and_exporter_gate.py`
  - Exporter hard-block rules now advertise the simplified primary gate fields.

- `phase9_rebuild_indexes_graph_smoke.py`
  - Fact graph inclusion now uses `source_trust` and `evidence_coverage`.

- `phase11_pilot_gold_dataset.py`
  - Pilot JSONL samples now use `sample_usage_scope`.

- `tests/test_swine_llm_wiki_runtime.py`
  - Runtime tests updated to reject legacy status fields in active runtime entries.

## Regeneration Results

- Runtime manifest entries: 204
- Missing runtime paths: 0
- Fact nodes included in graph: 2230
- Graph nodes: 2604
- Graph links: 2980
- Pilot samples: 24
  - train: 8
  - eval: 8
  - negative trap: 8
  - limited/gap: 0 under current conservative gate

## Validation

- JSON/CSV parse check passed for primary fact, fact status, runtime manifest, gold readiness, drug role, and source authority exports.
- `phase9_rebuild_indexes_graph_smoke.py` passed and wrote a passing retrieval smoke report.
- `tests/test_swine_llm_wiki_runtime.py` passed after tests were aligned with the simplified contract.

## Remaining Historical Artifacts

- `exports/knowledge_facts.json.p0_backup_20260508` is an explicit historical backup and still contains old `evidence_status` values. It is excluded by `runtime_exclude_patterns.json` and is not active runtime/export data.
- Several old one-off augmentation/migration scripts under `tools/` still contain historical status vocabulary because they document or reproduce earlier migration batches. They should not be used as active regeneration entrypoints without first porting them to the simplified contract.
