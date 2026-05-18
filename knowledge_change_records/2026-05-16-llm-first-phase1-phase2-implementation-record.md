# 2026-05-16 LLM-First Phase 1/2 Implementation Record

## Task Scope

Based on `knowledge_change_records/2026-05-16-llm-first-generation-wiki-posthoc-governance-implementation-spec.md`, this task implemented and accepted:

- Phase 1: Species runtime registry and isolation foundation.
- Phase 2: LLM-first raw consultation generation and prompt isolation.

All code and generated records were written with explicit UTF-8 encoding to reduce mojibake risk on Windows/PowerShell.

## Phase 1: Species Runtime Registry And Isolation

### Previous Problem

The repository already had species-aware display/config concepts and a minimal runtime registry, but the isolation checks were still too shallow for the llm_first gate:

- It could resolve swine/chicken profiles, but did not expose a stable runtime artifact provenance hash.
- Evidence anchor checks mainly compared namespace, profile, root, path, and forbidden terms.
- Manifest membership and provenance mismatch were not executable validation signals.
- Record-level species binding checks were not available as a reusable validator.

This meant a future post-generation evidence step could accidentally accept a path or artifact that looked syntactically plausible but was not proven to belong to the selected species runtime.

### Code Before

Main file:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/common/species_runtime_registry.py`

It provided:

- `SpeciesRuntimeProfile`
- `resolve_species_runtime_profile`
- `validate_runtime_profile`
- `validate_prompt_isolation`
- `validate_path_under_profile`
- `validate_evidence_anchor_isolation`

But it did not validate runtime manifest membership or artifact provenance hash.

### Changes Made

Updated:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/common/species_runtime_registry.py`
- `ai-/tests/test_llm_first_phase1_species_runtime_registry.py`

Added or strengthened:

- `SpeciesRuntimeProfile.runtime_root`
- `artifact_provenance_hash(profile)`
- UTF-8-sig JSON loading for runtime manifests.
- Runtime manifest `knowledge_base`, species, and non-empty entries checks.
- Manifest page path membership validation.
- Generic ID prefix validation for entity/fact/rule/source fields.
- Record-level species binding validator.
- Evidence anchor artifact provenance mismatch detection.
- Combined prompt plus record isolation helper.

### Expected Effect

Every llm_first record and future evidence anchor can now be bound to one explicit species runtime profile. Cross-species roots, mismatched namespaces, missing runtime files, wrong manifest membership, or wrong artifact provenance are surfaced as isolation failures instead of being silently treated as low-confidence evidence.

## Phase 2: LLM-First Raw Generation And Prompt Isolation

### Previous Problem

The current generation path remained Wiki-first:

- It expected skeletons and pre-generation evidence anchors.
- It generated grounded answers with Wiki evidence already injected.
- Raw llm_first records without `skeleton_id`, `stage_2_grounded`, or `evidence_anchors` did not have a dedicated executable path.
- There was no prompt renderer proving that raw generation avoids Wiki facts, IDs, page paths, and cross-species prompt leakage.

### Code Added

New module:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/generate_llm_first_raw_consultations.py`

New test:

- `ai-/tests/test_llm_first_phase2_raw_generation.py`

The module adds:

- `workflow_mode=llm_first`.
- Case seed creation before Wiki evidence injection.
- Species profile binding before prompt rendering.
- Prompt renderer using only selected species profile wording.
- Prompt isolation validation before model calls.
- Deterministic dry-run raw answer generation.
- Real-API hook through the existing `WikiFirstLLMClient`.
- UTF-8 JSONL/report writers.
- Functional kebab-case output artifact names:
  - `llm-first-raw-consultations-20260516-phase1-phase2-acceptance.jsonl`
  - `llm-first-raw-generation-20260516-phase1-phase2-acceptance.md`
  - `llm-first-raw-generation-20260516-phase1-phase2-acceptance.json`

### Expected Effect

The project can now create raw consultation records first, preserve the raw assistant answer lineage, and defer Wiki/rule governance to later post-generation phases. The raw generation prompt is rejected if it contains internal markers such as source/fact/rule/page identifiers, Wiki page paths, generic evidence IDs, or forbidden cross-species terms.

## Acceptance And Verification

### Automated Tests

Command:

```powershell
py -m pytest ai-/tests/test_llm_first_phase1_species_runtime_registry.py ai-/tests/test_llm_first_phase2_raw_generation.py -vv
```

Result:

- 10 passed.

Covered acceptance points:

- Swine and chicken resolve to distinct `species_profile_id`, `species_runtime_namespace`, and `wiki_root`.
- Unknown species fails closed.
- Prompt isolation blocks internal markers and cross-species terms.
- Evidence anchors fail on cross-species namespace/profile/root mismatch.
- Evidence anchors fail on runtime manifest non-membership and artifact provenance mismatch.
- Paths outside the selected Wiki root fail.
- Record species binding mismatch fails.
- Raw llm_first records include required lineage fields.
- Raw llm_first records do not require Wiki-first fields: `skeleton_id`, `stage_2_grounded`, `evidence_anchors`.
- Chicken prompt uses chicken profile wording and does not include swine terms or internal evidence markers.

### Dry-Run Acceptance Artifact

Command:

```powershell
py ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/generate_llm_first_raw_consultations.py --species swine --mode dry-run --limit 2 --run-label phase1-phase2-acceptance
```

Generated:

- `ai-/knowledge/llm_wiki_swine_authoritative/exports/generated_samples/llm-first-raw-consultations-20260516-phase1-phase2-acceptance.jsonl`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/llm-first-raw-generation-20260516-phase1-phase2-acceptance.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/llm-first-raw-generation-20260516-phase1-phase2-acceptance.json`

Result:

- 2 dry-run records generated.
- `workflow_mode=llm_first`.
- `species_isolation_status=passed`.
- Chinese text displayed correctly when read as UTF-8.

### Syntax Check

Command:

```powershell
py -m compileall -q ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/common/species_runtime_registry.py ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/generate_llm_first_raw_consultations.py
```

Result:

- Passed.

## Cleanup

Removed Python `__pycache__` folders produced by this task under:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline`

No unrelated pre-existing working-tree changes or generated historical artifacts were reverted or deleted.

## Remaining Boundary

This completes Phase 1 and Phase 2 only. Claim extraction, post-generation evidence retrieval, claim governance, remediation, cleaning, and export adapter remain later phases under the implementation spec.
