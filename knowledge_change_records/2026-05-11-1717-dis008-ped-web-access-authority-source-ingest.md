# DIS-008 PED Web Access Authority Source Ingest

## 1. Update Target

This update supplements `DIS-008` porcine epidemic diarrhoea / PED with web-access-discovered authority sources from WOAH and USDA APHIS. The goal was to run a complete source-first update flow: authority source discovery, raw evidence registration, source/fact ingest, disease-page anchoring, evidence expansion routing, guarded validation, and graph rebuild.

## 2. Before State

- Disease page: `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- Existing page already had textbook/MOA/Merck anchors, but the explicit `Evidence gaps` section still listed laboratory diagnosis, differential diagnosis, and control points as remaining source-coverage gaps.
- Existing source `A1-WOAH-PED` was present, but this run refreshed its web-access reinforcement and added a new USDA APHIS technical-note source node.

## 3. Files Added Or Updated

- Added raw Web Access JSON:
  - `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/web_access_dis008_ped_authority_20260511/SRC-DIS008-PED-WEB-20260511.json`
- Added ingest script:
  - `ai-/knowledge/llm_wiki_swine_authoritative/scripts/ingest_dis008_ped_web_access_20260511.py`
- Added source page:
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/sources/A1-USDA-APHIS-PED-TECH-NOTE-2023.md`
- Updated source page:
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/sources/A1-WOAH-PED.md`
- Updated disease page:
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- Added evidence expansion:
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/008-Web-Access-Authority-Reinforcement-2026-05-11.md`
- Updated generated exports and graph artifacts through guarded postcheck:
  - `exports/source_index.csv`
  - `exports/knowledge_facts.json`
  - `exports/knowledge_facts_status_index.json`
  - `exports/runtime_core_manifest.json`
  - `wiki/graph-data.json`
  - `wiki/knowledge-graph.html`
  - `wiki/knowledge-graph.md`
  - `wiki/knowledge-graph-changes.html`

## 4. CRUD Type

- Create: one raw Web Access JSON, one USDA APHIS source page, six fact nodes, one evidence expansion, graph-diff artifacts.
- Update: WOAH PED source page, DIS-008 disease page, source/fact/status indexes, runtime manifest, graph JSON/HTML.
- Query: authority-source web discovery and URL verification through configured web-access workflow.
- Delete: no deletion.

## 5. Old Data Handling

Existing textbook, MOA, Merck, and WOAH data were retained. No previous source or fact was overwritten for medical meaning. Existing `A1-WOAH-PED` was updated only with a dated Web Access reinforcement section and kept as the same source identity.

## 6. High-Risk Gate

This update touches diagnostic and control-boundary information. It does not add executable prescriptions, antimicrobial choices, dose, route, treatment course, withdrawal period, MRL, residue, food-safety, quarantine, culling, movement-control, farm-closure, vaccination schedule, or China-specific regulatory execution conclusions.

Applicable guardrails remain:

- `RC-DX-001`
- `RC-DISEASE-REGULATORY-001`
- `RC-DRUG-001`
- `RC-WITHDRAWAL-MRL-001`
- `RC-CITATION-001`

## 7. Runtime Manifest Impact

The guarded postcheck rebuilt the runtime manifest successfully. `missing_paths` remained `0`; no runtime-damaged file was introduced.

## 8. Gold Dataset Impact

The new facts improve retrieval and evaluation support for PED identity, non-zoonotic boundary, neonatal severity, fecal-oral transmission, biosecurity / early detection, and laboratory differentiation from TGE. They do not upgrade DIS-008 into an unbounded treatment, drug, withdrawal/MRL, food-safety, or jurisdiction-specific regulatory execution source.

## 9. Graph Change

Graph rebuild succeeded and produced a visible change:

- Nodes: `2583 -> 2591`
- Links: `3175 -> 3187`
- Added nodes: 8
- Added links: 12

Added nodes:

- `source:A1-WOAH-PED`
- `source:A1-USDA-APHIS-PED-TECH-NOTE-2023`
- `fact:DIS008-WEB-001-woah-nonzoonotic-coronavirus`
- `fact:DIS008-WEB-002-woah-age-morbidity-mortality`
- `fact:DIS008-WEB-003-woah-fecal-oral-biosecurity-early-detection`
- `fact:DIS008-WEB-004-woah-clinical-similarity-no-specific-treatment`
- `fact:DIS008-WEB-005-usda-lab-differentiation-from-tge`
- `fact:DIS008-WEB-006-usda-fecal-oral-no-vector-reservoir`

## 10. Validation

Commands run:

```powershell
python -m py_compile knowledge/llm_wiki_swine_authoritative/scripts/ingest_dis008_ped_web_access_20260511.py
python knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py -- python knowledge/llm_wiki_swine_authoritative/scripts/ingest_dis008_ped_web_access_20260511.py
```

Guarded update result:

- Governance preflight: passed.
- Update command: passed; facts changed: 6.
- Full post-update checks: passed.
- Hallucination audit: high `0`, medium `0`.
- Readiness score: `99`.
- Encoding audit: runtime damaged count `0`.
- Pytest: `11 passed`.

## 11. Governance Compliance

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`: checked and applied.
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`: checked and applied.
- `WIKI_MAINTENANCE_GUIDE.md`: checked and applied.
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`: checked and applied.
- `SOURCE_BATCH_INTAKE_CHECKLIST.md`: checked and applied for source/fact/evidence-expansion placement.
- Fixed guarded entrypoint was used.
- Old-data handling: keep/update only; no deletion or silent overwrite.
- Runtime manifest impact: rebuilt and validated.
- Gold dataset impact: limited to source-anchored retrieval/evaluation support.

## 12. UTF-8 Precautions

New JSON, Python, Markdown, and change-record files were written as UTF-8. The update avoided bulk rewriting existing Chinese runtime text and used the repository validation chain, including `audit_encoding_integrity.py`, after the guarded update.
