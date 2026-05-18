# Chicken Pharmacopoeia Part 3 Markdown Intake And Entity Anchor Supplement

Date: 2026-05-16

## Goal

Use `ai-\knowledge\llm_wiki_chicken_authoritative\raw\md\中国兽药典三部1-200页.md` to supplement the chicken disease LLM wiki with source-backed biologic and diagnostic-product standard anchors while keeping entity pages compact.

## Source Read

- Source file: `ai-\knowledge\llm_wiki_chicken_authoritative\raw\md\中国兽药典三部1-200页.md`
- Scope: 《中华人民共和国兽药典》2015 年版三部, local Markdown pages 1-200.
- Read strategy: title and table-of-contents scan, poultry/chicken keyword expansion, entry-boundary slicing, candidate-fact extraction, entity alignment.
- New source page: `ai-\knowledge\llm_wiki_chicken_authoritative\wiki\sources\SRC-0166-中国兽药典2015年版三部1-200页.md`

## Candidate Facts

Created:

- `ai-\knowledge\llm_wiki_chicken_authoritative\issues\pharmacopoeia_2015_part3_chicken_candidate_facts_2026-05-16.json`

Candidate coverage:

- 22 chicken/poultry-related candidate anchors.
- Covered inactivated vaccines, live vaccines, diagnostic antigens, positive sera, negative sera, avian tuberculin, and chlamydiosis diagnostic products.
- High-risk clinical claims such as field immunization schedules, dosing, diagnosis interpretation, regulatory action, culling, treatment, and withdrawal/MRL claims were not generated from this source.

## Entity Pages Updated

Added compact pharmacopoeia anchor sections and `SRC-0166` links to:

- `DIS-001-鸡白痢.md`
- `DIS-002-鸡球虫病.md`
- `DIS-003-传染性支气管炎.md`
- `DIS-008-禽流感.md`
- `DIS-009-新城疫.md`
- `DIS-010-传染性法氏囊病.md`
- `DIS-011-马立克病.md`
- `DIS-012-传染性喉气管炎.md`
- `DIS-013-鸡支原体病.md`
- `DIS-014-禽霍乱.md`
- `DIS-015-传染性鼻炎.md`
- `DIS-016-禽痘.md`
- `DIS-019-肉毒梭菌中毒.md`
- `DIS-029-鸡伤寒.md`
- `DIS-054-禽结核病.md`
- `DIS-055-鸡产蛋下降综合征.md`
- `DIS-059-禽衣原体病.md`

## Index Updates

- Updated chicken wiki source count in `ai-\knowledge\llm_wiki_chicken_authoritative\index.md` from 121 to 122.

## Boundaries

- Entity pages received only short standard-anchor summaries.
- Full item detail remains in the source page and candidate JSON.
- No new full disease entity was created.
- No vaccine schedule, dose, treatment, official reporting, culling, movement-control, food-safety, withdrawal-period, or MRL recommendation was generated from the pharmacopoeia source alone.

## Validation

Completed checks:

- Candidate JSON parsed successfully with Node.js: 22 records, from `PHARMA2015P3-CHICKEN-0001` to `PHARMA2015P3-CHICKEN-0022`.
- `SRC-0166` source page exists.
- 17 disease pages contain `SRC-0166` links.
- Sampled edited source/disease pages for common mojibake markers; no new marker was found in the checked files.

Not run:

- `python scripts/lint_chicken_wiki.py` could not be run because the script path referenced by `.wiki-schema.md` does not exist in the current workspace.

## Remaining Work

- Rebuild source/disease indexes and graph data if the project requires machine export synchronization.
- Promote selected candidate facts into `exports/knowledge_facts.json` only after confirming the current fact-export contract and avoiding duplicate fact IDs.
- Consider a future `wiki/biologics/` or `wiki/vaccines/` layer if vaccine anchors grow beyond compact disease-page summaries.
