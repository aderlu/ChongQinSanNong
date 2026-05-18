# 2026-05-16 LLM-First Phase 3/4 Implementation Record

## Task Scope

This record documents implementation and acceptance for:

- Phase 3: Answer claim extraction and claim schema validation.
- Phase 4: Wiki/rule evidence retrieval and claim-to-evidence matching.

The implementation continues the `llm_first` path from Phase 1/2 and keeps the existing Wiki-first control modules untouched.

## Phase 3: Claim Extraction

### Previous Problem

Before this phase, raw `llm_first` records preserved the raw user query and raw assistant answer, but there was no executable layer that converted the answer into auditable claims. That meant later governance could not reliably tell whether an answer contained:

- clinical signs copied from case context,
- diagnostic reasoning,
- field actions,
- medication class suggestions,
- specific drug claims,
- dosage/course claims,
- withdrawal/residue claims,
- food-safety claims,
- regulatory execution claims,
- safe boundary statements,
- cross-species terminology leakage.

### Code Added

New module:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/extract_consultation_answer_claims.py`

New test:

- `ai-/tests/test_llm_first_phase3_claim_extraction.py`

The module adds deterministic rule-based extraction with:

- required claim schema validation,
- source span preservation,
- allowed `claim_type` normalization,
- `risk_level` classification,
- `needs_evidence` assignment,
- case-context vs authoritative-knowledge separation,
- species profile binding,
- forbidden cross-species term detection.

High-risk claim types are forced to `needs_evidence=true`:

- `specific_drug`
- `dosage_or_course`
- `withdrawal_or_residue`
- `food_safety`
- `regulatory_action`

### Expected Effect

Every raw answer can now be converted into a claim record before governance. This makes unsafe or unsupported answer content visible and reviewable instead of hidden inside free text.

## Phase 4: Claim Evidence Retrieval

### Previous Problem

Before this phase, there was no post-generation retrieval layer scoped to extracted claims. Existing Wiki-first logic expected evidence anchors before generation, while `llm_first` needs evidence after the raw answer exists.

The main risk was that future retrieval could accidentally read evidence from the wrong species runtime or treat weak/cross-species evidence as support.

### Code Added

New module:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/retrieve_wiki_evidence_for_claims.py`

New test:

- `ai-/tests/test_llm_first_phase4_evidence_retrieval.py`

The module reads only the bound species profile runtime files:

- `runtime_core_manifest.json`
- `knowledge_facts.json`
- `drug_gold_role_index.csv`
- `rule_card_index.csv` or selected species rule index
- `source_authority_status_index.csv`

It outputs:

- `wiki_retrieval_id`
- `wiki_retrieval_query`
- `wiki_retrieved_entity_ids`
- `retrieved_evidence`
- `evidence_anchors`
- `wiki_source_trust`
- `wiki_evidence_coverage`
- `wiki_evidence_anchor_count`
- `unsupported_high_risk_claim_count`
- `evidence_support_status`
- `evidence_support_failures`
- species binding fields and isolation status

### Important Design Correction

During dry-run validation, unsupported high-risk claims were initially mixed into `species_isolation_status=failed`. This was corrected.

Final semantics:

- Cross-species/root/path/namespace/provenance problems use `species_isolation_status=failed`.
- Unsupported high-risk claims use `evidence_support_status=failed` and `evidence_support_failures`.

This keeps isolation failures separate from evidence insufficiency, which is important for later Phase 5 governance and Phase 6 remediation.

## Acceptance And Verification

### Unit Tests

Command:

```powershell
py -m pytest ai-/tests/test_llm_first_phase3_claim_extraction.py ai-/tests/test_llm_first_phase4_evidence_retrieval.py -vv
```

Result:

- 6 passed.

Covered acceptance points:

- Claim records include required schema fields.
- Source spans are preserved.
- High-risk medication, dosage/course, withdrawal/residue, and food-safety claims require evidence.
- Forbidden cross-species terms become claim-level isolation violations.
- Evidence anchors are bound to selected species profile, namespace, Wiki root, and provenance hash.
- Cross-species claim violations block retrieval support.
- Unsupported high-risk claims are not silently treated as supported.

### Phase 1-4 Regression Set

Command:

```powershell
py -m pytest ai-/tests/test_llm_first_phase1_species_runtime_registry.py ai-/tests/test_llm_first_phase2_raw_generation.py ai-/tests/test_llm_first_phase3_claim_extraction.py ai-/tests/test_llm_first_phase4_evidence_retrieval.py -q
```

Result:

- 16 passed.

### Small Chain Dry Run

Phase 3 command:

```powershell
py ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/extract_consultation_answer_claims.py --input ai-/knowledge/llm_wiki_swine_authoritative/exports/generated_samples/llm-first-raw-consultations-20260516-phase1-phase2-acceptance.jsonl --run-label phase3-phase4-acceptance
```

Generated:

- `ai-/knowledge/llm_wiki_swine_authoritative/exports/generated_samples/llm-first-claims-20260516-phase3-phase4-acceptance.jsonl`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/llm-first-claim-extraction-20260516-phase3-phase4-acceptance.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/llm-first-claim-extraction-20260516-phase3-phase4-acceptance.json`

Result summary:

- record_count: 2
- claim_count: 46
- high_risk_claim_count: 6
- isolation_violation_claim_count: 0

Phase 4 command:

```powershell
py ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/retrieve_wiki_evidence_for_claims.py --input ai-/knowledge/llm_wiki_swine_authoritative/exports/generated_samples/llm-first-claims-20260516-phase3-phase4-acceptance.jsonl --run-label phase3-phase4-acceptance-v2
```

Generated:

- `ai-/knowledge/llm_wiki_swine_authoritative/exports/generated_samples/llm-first-claim-evidence-20260516-phase3-phase4-acceptance-v2.jsonl`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/llm-first-claim-evidence-retrieval-20260516-phase3-phase4-acceptance-v2.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/llm-first-claim-evidence-retrieval-20260516-phase3-phase4-acceptance-v2.json`

Result summary:

- record_count: 2
- evidence_anchor_count: 22
- unsupported_high_risk_claim_count: 4
- species_isolation_failed_records: 0

Interpretation:

- The chain ran effectively from raw answers to claims to claim-scoped evidence.
- No cross-species isolation failure was found in the two-record dry run.
- Four high-risk claims remain unsupported and must be handled by Phase 5 governance and later remediation/rejection.

## Encoding And Cleanup

All new code uses explicit UTF-8 or UTF-8-sig reads and UTF-8 writes.

Cleaned:

- Python `__pycache__` folders created during this task under `tools/pipeline`.
- The first Phase 4 trial artifact without the corrected evidence-support/isolation separation:
  - `llm-first-claim-evidence-20260516-phase3-phase4-acceptance.jsonl`
  - `llm-first-claim-evidence-retrieval-20260516-phase3-phase4-acceptance.md`
  - `llm-first-claim-evidence-retrieval-20260516-phase3-phase4-acceptance.json`

Retained final acceptance artifacts:

- Phase 3 claim extraction artifacts.
- Phase 4 corrected `phase3-phase4-acceptance-v2` artifacts.

## Clear Main Chain Recommendation

Keep as active main-chain modules:

- `generate_llm_first_raw_consultations.py`
- `extract_consultation_answer_claims.py`
- `retrieve_wiki_evidence_for_claims.py`
- `common/species_runtime_registry.py`

Keep as active acceptance tests:

- `test_llm_first_phase1_species_runtime_registry.py`
- `test_llm_first_phase2_raw_generation.py`
- `test_llm_first_phase3_claim_extraction.py`
- `test_llm_first_phase4_evidence_retrieval.py`

Candidates for future archival after Phase 5/6 stabilize:

- Older exploratory `llm-first-*acceptance` artifacts can be moved under an archive subfolder once a newer smoke run covers Phase 1-6 end to end.
- Historical Wiki-first phase reports should remain as control evidence, but should not be mixed with new `llm_first` generated artifacts in the main execution path.

Do not remove yet:

- Phase 1/2 acceptance raw records, because Phase 3/4 currently use them as a small reproducible fixture.
- Phase 3/4 acceptance artifacts, because they prove this handoff into Phase 5.
