# LLM Wiki Skill Parity Review

## Scope

Reviewed against `D:\XF-ChongQin\llm-wiki-skill-main`, excluding image download/localization/rendering features. The chicken disease system is domain-specific, so generic `entities/` pages are mapped to disease, drug, rule, syndrome, topic, source, synthesis, comparison, session, and query pages.

## Parity Matrix

| llm-wiki-skill-main capability | Chicken system status | Implementation |
| --- | --- | --- |
| init wiki layout | Complete | `chicken-wiki init` |
| purpose/schema/log/cache files | Complete | `knowledge/llm_wiki_chicken_authoritative` plus `schema-check` |
| source registry | Complete | `chicken-wiki source list/match` |
| adapter state model | Complete | `chicken-wiki adapter check` |
| local file ingest | Complete | `chicken-wiki ingest` |
| URL ingest fallback | Complete | `chicken-wiki ingest-url` creates manual source record |
| pasted text ingest | Complete | `chicken-wiki ingest-text` |
| batch ingest | Complete | `chicken-wiki batch-ingest` |
| cache check/update/invalidate | Complete | `cache check/update`, delete invalidates cache on apply |
| source-create write-through | Complete | `source-create` updates cache |
| query | Complete | `chicken-wiki query`, returns page hits, fact hits, context |
| query-save | Complete | `chicken-wiki query-save` |
| digest | Complete | `chicken-wiki digest --save` |
| comparison digest | Complete | `chicken-wiki digest --format comparison --save` |
| crystallize/session synthesis | Complete | `chicken-wiki crystallize` |
| lint | Complete | `chicken-wiki lint --strict` |
| status/runtime context | Complete | `status`, `context` |
| source signal coverage | Complete | `coverage`, includes fact source and page source signal summary |
| schema/runtime contract check | Complete | `schema-check` |
| legacy compatibility inspect/validate | Complete | `compat inspect/validate/ensure-source-dir` |
| delete source workflow | Complete | `delete-source`, dry-run by default |
| graph data | Complete | `graph-build` creates `wiki/graph-data.json` |
| interactive graph HTML | Complete | `graph-build` creates `wiki/knowledge-graph.html` |
| static Mermaid graph | Complete | `graph-build` creates `wiki/knowledge-graph.md` |
| graph watch | Complete | `graph-watch --once` or continuous watch |
| Step 1 JSON validation | Complete | `step1-validate` |
| image tracking/localization | Excluded | Out of this review by request |

## Domain-Specific Differences

- Generic `wiki/entities/` is intentionally replaced by chicken disease domain sections: `wiki/diseases`, `wiki/drugs`, `wiki/rules`, `wiki/rule_cards`, `wiki/syndromes`, and `wiki/topics`.
- URL ingest does not pretend to fetch and extract article text automatically. It creates a traceable manual source record, matching the adapter fallback model.
- Generated facts are not directly merged into authoritative exports during ingest. They are written as candidates until reviewed.
- Derived query, digest, comparison, and crystallize pages are explicitly secondary evidence and carry `derived: true`.

## Current Health

Verified current authoritative Wiki:

- `schema-check`: ok
- `lint --strict`: ok
- Pages: 340
- Structured facts: 1748
- Diseases/drugs/rules: 60 / 115 / 30
- Source pages: 122
- Facts with source: 1608
- Unresolved source ids: 0
- Page source signal: 215 / 215 applicable pages ok
- Graph build: 337 nodes, 228 links

## Demonstration Steps

Run these from `D:\XF-ChongQin\ai-`.

1. Confirm the Wiki is the active runtime contract:

```powershell
$env:PYTHONPATH='D:\XF-ChongQin\ai-\src'
python -m chicken_data_synthesis.wiki_cli --json schema-check
python -m chicken_data_synthesis.wiki_cli --json lint --strict
```

2. Show knowledge retrieval for generation/evaluation:

```powershell
python -m chicken_data_synthesis.wiki_cli --json query 鸡白痢 --top-k 3
```

Expected display value: `hits` shows disease/source pages, `fact_hits` shows structured evidence with `evidence_source_id` and `evidence_status`, and `context` is prompt-ready.

3. Show compliance/rule evidence:

```powershell
python -m chicken_data_synthesis.wiki_cli --json query "产蛋鸡 氯霉素 禁用药" --top-k 5
```

Expected display value: drug/rule/source evidence appears and can explain why final quality gates should block or review unsafe prescriptions.

4. Show source traceability:

```powershell
python -m chicken_data_synthesis.wiki_cli --json coverage
python -m chicken_data_synthesis.wiki_cli --json source list
python -m chicken_data_synthesis.wiki_cli --json adapter check --source-id pdf
```

Expected display value: source coverage, source type registry, and adapter state are visible.

5. Show graph views:

```powershell
python -m chicken_data_synthesis.wiki_cli --json graph-build
```

Open:

- `knowledge/llm_wiki_chicken_authoritative/wiki/knowledge-graph.html`
- `knowledge/llm_wiki_chicken_authoritative/wiki/knowledge-graph.md`

6. Show derived synthesis:

```powershell
python -m chicken_data_synthesis.wiki_cli --json digest "新城疫 鉴别诊断" --save
python -m chicken_data_synthesis.wiki_cli --json digest "新城疫 传染性支气管炎 鉴别" --format comparison --save
python -m chicken_data_synthesis.wiki_cli --json crystallize "产蛋下降场景的鉴别诊断" --notes "演示：把检索证据沉淀为二级会话结晶。"
```

7. Show ingest lifecycle without damaging the authority set:

```powershell
python -m chicken_data_synthesis.wiki_cli --json ingest-url https://example.com/poultry-note --title "Demo URL source"
python -m chicken_data_synthesis.wiki_cli --json delete-source --source-page wiki/sources/<created-source-page>.md
```

`delete-source` defaults to dry-run. Add `--apply` only when intentionally deleting.

8. Show the generation/evaluation integration:

```powershell
python main.py --mode production --total-samples 10
```

Expected display value in generated CSV: Wiki audit columns such as `wiki_fact_count`, `wiki_page_count`, `wiki_context_query`, `wiki_evidence_status_counts`, `wiki_evidence_source_ids`, `target_disease_mismatch`, and `final_fatal_risk`.
