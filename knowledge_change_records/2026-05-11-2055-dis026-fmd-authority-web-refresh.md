# DIS-026 FMD Authority Web Refresh Change Record

## 1. Landing Time

- Landing date: 2026-05-11
- Landing time: 20:55
- Time zone: Asia/Shanghai
- Change type: source/fact/runtime/graph update

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: yes
- Fixed update entrypoint used: yes
- CRUD decision file: `ai-/knowledge/llm_wiki_swine_authoritative/issues/crud_decisions/2026-05-11-2055-dis026-fmd-authority-web-refresh.md`
- CRUD decision audit passed: yes
- Source/fact CRUD type: create/update
- Input source type: web
- Old data handling: keep
- If old data changed, factual reason: old data is retained; this is additive source/fact enrichment
- High-risk gate impact: strengthens high-regulatory FMD boundary; A1 sources do not replace China A0 execution sources
- Runtime manifest impact: update after rebuild
- Gold dataset impact: update after rebuilt fact status/readiness indexes

## 2. Problem Before The Change

`DIS-026` already had China A0 and textbook anchors, but several international authority boundaries were still better represented as compact, source-routed facts: FAO disease impact/control framing, USDA APHIS species/subtype/reporting framing, and USDA NAHLN diagnostic-preparedness framing.

The page needed an update that both supplements authority sources and demonstrates the new CRUD decision workflow: decision file, preflight audit, guarded execution, post-update checks, graph diff, and work record.

## 3. Code And Wiki State Before The Change

Before the change, the guarded update entrypoint already executed both governance compliance and CRUD decision preflights. `DIS-026` included existing source anchors such as `A0-MOA-FMD-CONTROL-GUIDE-2024`, `A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025`, and `A1-WOAH-FMD-DISEASE`, but did not yet include the new FAO/APHiS/NAHLN source IDs in its source list or new facts.

## 4. Code Added Or Updated

- Added `tools/apply_dis026_fmd_authority_web_refresh.py`.
  - Purpose: write new source pages, update `source_index.csv`, add knowledge facts, append a compact runtime block, and write an execution report.
  - Input: verified web-access authority sources.
  - Output: new source pages, knowledge facts, runtime page block, evidence expansion, issue report.

- Added CRUD decision file for this update.
- Added this change record.

## 5. Wiki Organization Work

The update is additive. It creates source pages for FAO, USDA APHIS disease, and USDA APHIS NAHLN preparedness, registers three facts, updates the FMD disease page, and writes a dedicated evidence expansion.

No old source, fact, runtime page, graph node, or gold sample is deleted or replaced.

## 6. What The Change Solved

The update strengthens FMD generation and evaluation boundaries:

- FMD as international transboundary disease affecting pigs and other cloven-hoofed animals.
- FMD impact on food security, livelihoods, and trade.
- Type/subtype boundary and why generic immunity/vaccine claims must be constrained.
- Reporting and diagnostic-preparedness boundaries.
- Clear separation between A1 international/US official references and China A0 execution rules.

## 7. Verification Results

Verification was performed through the guarded update command:

```powershell
$env:PYTHONIOENCODING='utf-8'
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python knowledge/llm_wiki_swine_authoritative/tools/apply_dis026_fmd_authority_web_refresh.py
```

Observed evidence:

- `preflight_governance_compliance`: passed
- `preflight_crud_decision`: passed
- `update_command`: passed
- `post_update_full_checks`: passed
- `phase9_rebuild_indexes_graph_smoke.py`: graph rebuilt with 2597 nodes, 3193 links, 2226 facts in graph
- `audit_graph_change_diff.py`: added 6 nodes and 6 links; removed 0 nodes and 0 links
- `audit_runtime_hallucination_risk.py`: high 0, medium 0
- `audit_swine_llm_wiki_readiness.py`: readiness score 99
- `audit_encoding_integrity.py`: runtime damaged count 0
- `pytest tests/test_swine_llm_wiki_runtime.py -q`: 11 passed

Graph diff summary:

```json
{
  "nodes_before": 2591,
  "nodes_after": 2597,
  "links_before": 3187,
  "links_after": 3193,
  "added_nodes": 6,
  "removed_nodes": 0,
  "added_links": 6,
  "removed_links": 0,
  "crud_counts": {
    "create": {
      "fact": 3,
      "source": 3
    }
  }
}
```

Added graph nodes:

- `source:A1-FAO-FMD-DISEASE-2026`
- `source:A1-USDA-APHIS-FMD-DISEASE-2026`
- `source:A1-USDA-APHIS-FMD-NAHLN-2026`
- `fact:DIS026-WEB-001-fao-fmd-impact-control`
- `fact:DIS026-WEB-002-usda-aphis-species-subtype-report`
- `fact:DIS026-WEB-003-usda-nahln-fmd-preparedness`

## 8. Expected Effects

The knowledge graph should gain three source nodes, three fact nodes, evidence-source links, and disease-fact links for `DIS-026`. Runtime retrieval should surface clearer FMD international authority and diagnostic/reporting boundaries, while still routing China-specific execution details to A0 sources.

## 9. Remaining Issues

The update does not add China-specific new execution details beyond existing A0 anchors. Local quarantine, culling, vaccination program, slaughter, compensation, food-chain, drug, withdrawal-period, and MRL claims still require current A0 or label-level sources.

## 10. Encoding Protection Measures

- New script and Markdown files were written with UTF-8 through `apply_patch`.
- The update script writes JSON and Markdown using `encoding="utf-8"`.
- CSV output uses `utf-8-sig` to protect spreadsheet compatibility.
- The guarded entrypoint sets `PYTHONIOENCODING=utf-8`.
