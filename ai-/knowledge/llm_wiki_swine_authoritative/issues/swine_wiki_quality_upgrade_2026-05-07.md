# Swine Wiki Quality Upgrade - 2026-05-07

## Outputs

- alias_index: `knowledge/llm_wiki_swine_authoritative/exports/alias_index.csv`
- source_index: `knowledge/llm_wiki_swine_authoritative/exports/source_index.csv`
- authority_source_dir: `knowledge/llm_wiki_swine_authoritative/wiki/sources`
- rule_cards: `['knowledge/llm_wiki_swine_authoritative/wiki/rule_cards/RC-CITATION-001.md', 'knowledge/llm_wiki_swine_authoritative/wiki/rule_cards/RC-TRAIN-READY-001.md', 'knowledge/llm_wiki_swine_authoritative/wiki/rule_cards/RC-ALIAS-001.md']`
- generation_gate_page: `knowledge/llm_wiki_swine_authoritative/wiki/synthesis/swine_dataset_generation_validity_gate_v7.md`
- reinforced_disease_pages: `[]`
- pdf_hit_manifest: `knowledge/llm_wiki_swine_authoritative/issues/swine_pdf_priority_page_hits_2026-05-07.json`

## Policy

- PDF extraction is limited to page-hit manifests for human review; no automatic dose, withdrawal-period, or regulatory action facts are promoted.
- Web authority pages are registered as retrieval anchors and must be paired with jurisdiction-specific sources for local regulatory instructions.
- Dataset generation should use alias normalization and train-ready gates before exporting SFT data.
