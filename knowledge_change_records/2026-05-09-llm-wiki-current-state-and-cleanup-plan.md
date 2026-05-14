# LLM Wiki Knowledge Base Current State And Cleanup Plan

Date: 2026-05-09

## Purpose

This record documents the current state of `ai-/knowledge/llm_wiki_swine_authoritative`, the main risks found during inspection, and a proposed cleanup plan for safer production and evaluation use.

This is the first work-trace document in the new root-level `knowledge_change_records` directory. Future modifications should add one record per change.

## Current Baseline

Inspected path:

`ai-/knowledge/llm_wiki_swine_authoritative`

Existing top-level layout:

- `wiki/`: production-facing knowledge pages, but also contains graph exports, synthesis pages, sessions, sources, rules, topics, and issue-like material.
- `exports/`: generated indexes and structured fact tables.
- `raw/`: source PDFs, converted Markdown, crawled web pages, attachments, and crawl metadata.
- `issues/`: audit reports, gap reviews, extraction notes, and work logs.
- `scripts/` and `tools/`: batch enrichment, cleanup, extraction, validation, and readiness-audit scripts.

Quantitative baseline from the existing readiness audit:

- Disease pages: 73.
- Drug pages: 81.
- Syndromes: 22.
- Comparisons: 17.
- Rules: 449.
- Rule cards: 18.
- Sources: 219.
- Synthesis pages: 27.
- Topics: 99.
- Readiness score from `tools/audit_swine_llm_wiki_readiness.py`: 99/100.
- Missing indexed paths: 0.
- Bad fact tables by the existing audit: 0.
- Remaining audit deduction: 1 drug page missing unified availability section.

Size and density observations:

- `wiki/diseases`: 73 Markdown files, about 1.02 MB total, average about 14 KB, 17 files over 20 KB.
- `wiki/drugs`: 81 Markdown files, about 0.88 MB total, average about 11 KB, 14 files over 20 KB.
- `wiki/synthesis`: 27 Markdown files, about 0.94 MB total, average about 35 KB, 8 files over 20 KB.
- `exports/knowledge_facts.json`: about 1.7 MB.
- `wiki/graph-data.json`: about 1.7 MB.
- `wiki/knowledge-graph.html`: about 1.4 MB.

Encoding/data-quality signal:

- UTF-8 replacement characters were detected in 6 text-like files.
- Affected production-facing disease pages include:
  - `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
  - `wiki/diseases/DIS-044-gl-sser-s-disease.md`
  - `wiki/diseases/DIS-040-colibacillosis.md`
  - `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`
- The largest observed replacement-character count was in `DIS-026`, so it should be treated as a priority cleanup target.

## Main Problems Found

### 1. Production knowledge and construction artifacts are mixed

The repository has useful source-first structure, but `wiki/` is doing too many jobs at once. It contains stable entity pages, graph exports, synthesis matrices, rules, topics, source pages, sessions, and issue-like material.

Impact:

- Retrieval may pull historical notes, giant matrices, graph exports, or construction scaffolding together with production knowledge.
- Evaluation may reward answers that cite noisy enrichment blocks instead of stable source-backed sections.
- The production chain has no clear "load only this curated subset" boundary.

### 2. Entity pages are becoming too long

Several disease and drug pages include multiple appended batch sections, for example V11, V12, V13.1, V14, local Markdown reinforcement, handbook facts, treatment matrix facts, and raw extraction snippets.

Impact:

- Long pages increase chunking noise.
- Duplicate or near-duplicate facts can compete during retrieval.
- Older candidate facts may be retrieved beside reviewed facts.
- The model may overfit to verbose treatment snippets and generate executable dosage or treatment advice beyond the intended boundary.

### 3. Evidence status exists, but retrieval tiers are not explicit enough

Pages use statuses such as `HUMAN_REVIEWED`, `NEEDS_REVIEW`, `partial_source_anchored_page`, `source_anchored_clinical_page`, and `source_anchored_drug_evidence_page`. This is good, but the current file layout does not enforce tier-based loading.

Impact:

- A downstream system that simply indexes all Markdown under `wiki/` may treat partial pages, synthesis pages, and reviewed pages as equivalent.
- This can increase hallucination risk, especially in drug, withdrawal-period, MRL, diagnosis, regulatory, and emergency disease workflows.

### 4. Some text has encoding damage or extraction artifacts

The inspection found replacement characters in several files. The console also showed many Chinese sections as mojibake during direct reads, so the ingestion/display pipeline should be checked carefully.

Impact:

- Broken text reduces embedding quality.
- It can cause entity names, disease names, drug names, or instructions to be incorrectly chunked.
- It makes evidence review and report generation harder.

### 5. Raw and generated evidence are valuable but too close to runtime use

The `raw/` and `exports/` layers contain important traceability, but they should not be directly mixed with production retrieval unless the caller explicitly needs audit evidence or source reconstruction.

Impact:

- Production prompts can become overloaded.
- Evaluation can become unstable if large generated matrices dominate retrieval.
- The system may cite extraction artifacts rather than concise curated knowledge.

## Will This Affect Production Or Evaluation?

Yes, if the production or evaluation chain indexes the whole knowledge tree without a curated allowlist.

The current knowledge base is not unusable. The existing audit score is high, paths resolve, fact tables are source-linked, and rule cards exist. The main risk is not "no evidence"; the risk is "too much mixed evidence with weak runtime boundaries."

High-risk scenarios:

- Asking for treatment, dose, route, course, withdrawal period, MRL, slaughter, movement control, vaccination schedule, or regulatory action.
- Asking about diseases with both `NEEDS_REVIEW` and appended enrichment blocks.
- Retrieval over all Markdown files under `wiki/`, including `synthesis`, `sessions`, graph files, and issue-like pages.
- Evaluation tasks where candidate facts are treated as gold facts.

Expected failure modes:

- Hallucinated certainty from partial pages.
- Over-specific dosage or treatment suggestions copied from non-current or non-label sources.
- Conflicting answers caused by duplicate facts from multiple appended batches.
- Citation drift, where an answer cites a source id but the retrieved chunk was an extraction matrix or reinforcement note.
- Lower evaluator consistency because the same query may retrieve different large appended blocks.

## Recommended Cleanup Architecture

### Layer 1: Runtime Core

Create a curated production subset for generation and evaluation:

- Reviewed disease pages.
- Reviewed drug pages with strict use boundaries.
- Rule cards and hard-block rules.
- Syndrome and comparison pages.
- Minimal source metadata.

Runtime core should exclude:

- `raw/`
- `issues/`
- `sessions/`
- giant synthesis matrices
- graph HTML/JSON
- candidate extraction dumps
- batch construction notes

### Layer 2: Evidence Store

Keep structured fact indexes and source anchors here:

- `exports/*fact_index.csv`
- `exports/knowledge_facts.json`
- source pages
- page/line/source id mappings

This layer supports audit, citation lookup, and evidence expansion, but should not be blindly chunked into normal answer generation.

### Layer 3: Raw Archive

Keep original PDFs, converted Markdown, crawled pages, attachments, and crawl metadata.

This layer is for traceability and reprocessing only.

### Layer 4: Work Records

Use the new root-level `knowledge_change_records/` directory for management-facing change records and work traces.

This is separate from `ai-/knowledge/.../issues` because it records repository-level maintenance decisions and is easier to use for work reporting.

## Recommended File/Index Changes

1. Add a production allowlist manifest.

Suggested path:

`ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest.json`

It should list exactly which pages are allowed for production retrieval, with fields such as:

- `page_id`
- `path`
- `entity_type`
- `evidence_status`
- `runtime_tier`
- `allowed_use`
- `blocked_use`
- `source_ids`
- `last_verified`

2. Add a retrieval denylist.

Suggested path:

`ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_exclude_patterns.json`

Initial denylist:

- `raw/**`
- `issues/**`
- `wiki/sessions/**`
- `wiki/exports/**`
- `wiki/knowledge-graph.html`
- `wiki/graph-data.json`
- large synthesis matrices unless explicitly requested

3. Split oversized entity pages.

Keep entity pages concise:

- identity
- aliases
- clinical summary
- risk boundaries
- source-backed key facts
- explicit do-not-generate constraints
- links to evidence expansion files

Move appended batch facts into evidence expansion files or structured indexes.

4. Normalize status names.

Recommended runtime tiers:

- `runtime_core_reviewed`
- `runtime_core_partial`
- `evidence_expansion`
- `candidate_only`
- `raw_archive`
- `do_not_index`

5. Add a hallucination-risk audit script.

Suggested checks:

- files over size threshold
- replacement characters
- pages with `NEEDS_REVIEW`
- pages containing dose/withdrawal/MRL terms without explicit rule-card links
- duplicated fact ids
- candidate facts in runtime pages
- missing source/page anchors

6. Add a pre-production validation command.

The production chain should fail or warn when:

- a runtime manifest includes `raw`, `issues`, `sessions`, graph exports, or candidate dumps
- a retrieved chunk has no source anchor
- drug advice is requested without rule-card and label/regulatory evidence
- emergency disease handling is requested without A0/A1 regulatory sources

## Work Done In This Change

Added root-level work-trace directory:

- `knowledge_change_records/`

Added documentation:

- `knowledge_change_records/README.md`
- `knowledge_change_records/2026-05-09-llm-wiki-current-state-and-cleanup-plan.md`

No production knowledge pages were modified in this change.

No extraction, graph, index, or audit code was modified in this change.

## Verification Run

Command:

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py`

Result:

- readiness score: 99/100
- missing indexed paths: 0
- bad fact tables: 0
- missing rule cards: 0
- missing synthesis pieces: 0
- deduction: 1 drug page missing unified availability section

Additional inspection:

- counted file types and major directories
- sampled disease and drug pages
- checked largest files
- checked UTF-8 replacement-character occurrences in text-like knowledge files

## Next Recommended Steps

1. Build `runtime_core_manifest.json` and `runtime_exclude_patterns.json`.
2. Add a hallucination-risk audit script and wire it into the production/evaluation precheck.
3. Repair the disease pages with replacement characters, starting with `DIS-026`, `DIS-044`, `DIS-040`, and `DIS-009`.
4. Refactor the largest disease/drug pages so appended evidence batches live in structured evidence expansion files.
5. Update the production and evaluation chain to load only the runtime manifest, not the full wiki tree.

