# DIS-053 Formal Source/Fact Ingest

- Date: 2026-05-11
- Scope: DIS-053 猪结核病
- guarded_entrypoint: `python knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python knowledge\llm_wiki_swine_authoritative\scripts\ingest_dis053_tuberculosis_web_access_20260511.py`

## Governance Compliance

- 是否遵守: yes
- maintenance_guide: `WIKI_MAINTENANCE_GUIDE.md`
- crud_governance: `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- mandatory_short_card: `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- scenario_short_card: `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- guarded_entrypoint: `run_guarded_wiki_update.py`
- 固定入口: yes
- 短执行卡: followed
- 场景化短执行卡: DIS-053 official-source supplementation

## CRUD

- Create: `A0-SAMR-GBT-18645-2020-ANIMAL-TB-DIAGNOSIS` source page.
- Create/Update: four `DIS053-WEB-*` facts registered in `exports/knowledge_facts.json` and standardized into `exports/knowledge_facts_status_index.json`.
- Update: `wiki/diseases/DIS-053-tuberculosis.md` now links to `A0-MOA-573` and `A0-SAMR-GBT-18645-2020-ANIMAL-TB-DIAGNOSIS`.
- Read: raw JSON kept as audit evidence, not as the formal A0 source node.
- Delete/Archive: none.
- 增删改查: 新增 source/fact，查询 raw/source/fact/runtime，修改 DIS-053 页面和索引，删除为 none。

## Graph Result

- Added nodes: 5.
- Added links: 8.
- Removed nodes: 0.
- Removed links: 0.
- Reasonable change: one new official source node plus four fact nodes, with fact-to-source evidence edges and DIS-053-to-fact anchor edges.

## Old data / Runtime manifest / Gold dataset

- Old data: retained; no existing DIS-053 source/fact was deleted.
- 旧数据: 保留原有 DIS-053 runtime page、`SRC-0001`、`SRC-0078` 和已有来源锚点。
- Runtime manifest: rebuilt by post-update maintenance checks.
- runtime manifest: `exports/runtime_core_manifest.json` refreshed through maintenance postcheck.
- Gold dataset: unchanged.
- gold dataset: unchanged; no 黄金数据集 promotion or demotion.

## Boundary

- No treatment, dose, course, withdrawal period, MRL, food-safety, culling, quarantine, movement-control, or regulatory execution conclusion was added.
- High-risk: treatment, dose, course, withdrawal period, MRL, residue, food-safety, culling, quarantine, movement-control, and regulatory execution claims remain blocked unless an exact A0/label-level source supports them.
- 高风险: 本次只新增来源边界和标准元数据事实，不新增执行性处置或用药结论。
