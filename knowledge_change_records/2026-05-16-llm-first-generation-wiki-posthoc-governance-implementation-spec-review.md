# 2026-05-16 LLM-First Generation With Wiki Posthoc Governance Implementation Spec Review

## 1. Review Scope

Reviewed document:

- `D:\XF-ChongQin\knowledge_change_records\2026-05-16-llm-first-generation-wiki-posthoc-governance-implementation-spec.md`

Reviewed against current implementation under:

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative`
- `D:\XF-ChongQin\ai-\tests`
- Related change records under `D:\XF-ChongQin\knowledge_change_records`

Review objective:

1. Strictly assess whether the proposed implementation is executable on the current data generation and evaluation system.
2. Assess whether chicken-disease and swine-disease workflows can share one system.
3. Assess whether the proposed workflow can effectively achieve the stated goal: generate more natural LLM-first consultation data while preserving Wiki/rule governance as a real admission gate.

## 2. Executive Conclusion

The document is directionally correct and technically meaningful, but it should be treated as an implementation specification, not as a description of already available system capability.

Current system reality:

- The current production-style chain is still Wiki-first / anchor-first.
- Existing generation depends on Wiki-derived plans, answer skeletons, facts, rule cards, and evidence anchors before generation.
- Existing fact evaluation mostly validates pre-attached anchors and hard-gate rules.
- Existing baseline comparison already has a stable 54-field contract.
- Chicken workflow has recently reached small real-API smoke execution, but this is still the existing Wiki-first chain, not the proposed LLM-first posthoc-governance chain.

Therefore:

- The proposed workflow is executable only after substantial new components are implemented.
- It is not safe to achieve the target merely by relaxing generation prompts.
- Chicken and swine can share the same platform framework, but cannot share the same disease/drug evidence content, species wording, runtime indexes, or regulatory/drug constraints without strict species isolation.

Overall review verdict:

`Conditionally executable, not yet implemented, high value if completed with strict gates.`

## 3. Current System Assessment

### 3.1 Current Generation Model Is Wiki-First

Current Phase 12 creates plans from runtime Wiki metadata and evidence readiness:

- It reads `runtime_core_manifest.json`, `gold_dataset_readiness_index.csv`, `drug_gold_role_index.csv`, and `exporter_hard_block_rules.json`.
- It derives `required_rule_cards`, `source_trust`, `evidence_coverage`, `authority_level`, `risk_class`, and ability layers before generation.
- It filters or routes plans according to evidence depth and risk class.

Current Phase 13 builds answer skeletons before generation:

- It selects facts from `knowledge_facts_status_index.json`.
- It turns facts into `must_include_claims`.
- It creates evidence anchors from fact IDs, source IDs, rule cards, and page paths.
- It embeds generation contracts and hard-gate profiles into the skeleton.

Current Phase 14 generates samples with evidence already attached:

- It builds stage answers from skeletons and plans.
- It outputs `evidence_anchors`.
- It stores `stage_2_grounded.answer` as the audit-grounded answer.
- It stores `stage_2_grounded.clinical_answer` as the user-facing consultation answer.

This means current generation is not LLM-first. The proposed workflow requires raw model output without Wiki evidence injected into the answer prompt.

### 3.2 Current Evaluation Assumes Pre-Existing Anchors

Current Phase 15 checks:

- Required sample fields.
- Presence and completeness of `evidence_anchors`.
- Fact IDs and source IDs against fact index.
- Page paths against runtime manifest.
- Hard safety gates using regex and rule-card/A0 checks.

This is useful, but it is not the same as post-generation claim governance.

Current Phase 15 does not yet:

- Extract claims from raw natural language answers.
- Link each extracted claim to evidence after generation.
- Assign per-claim review labels such as `supported`, `unsupported_high_risk`, `contradicted`, or `unsafe`.
- Compare raw and remediated claims.
- Produce `unsupported_high_risk_claim_count` as an admission invariant.

### 3.3 Current Semantic Review Is Reusable But Not Sufficient

Current Phase 18 provides:

- Dual judge and arbiter logic.
- Semantic quality scoring.
- Safety and fatal-risk routing.
- Species-aware prompt rendering after recent chicken fixes.

This component can be reused in the proposed workflow, but it should remain downstream of deterministic claim governance. It cannot replace claim extraction and evidence matching.

### 3.4 Current Export Layer Is Mature But Needs New Metadata Inputs

Current Phase 16 can export:

- Production CSV.
- Training main CSV.
- Layered training sets.
- Review/repair/rejected queues.

It already supports species output prefix such as `swine_wiki` and `chicken_wiki`.

However, the proposed LLM-first workflow requires new export-layer inputs:

- `raw_assistant_answer`
- `claims`
- `claim_reviews`
- `evidence_matches`
- `remediation_id`
- `revised_assistant_answer`
- `revision_admission_decision`
- `final_assistant_answer`
- lineage hashes

These are not currently produced by the main pipeline.

## 4. Review Of Proposed Workflow

### 4.1 Scenario And Case Seed Creation

Assessment: feasible and partially supported.

Current system already has case variables, scenario context, user persona, information completeness, urgency, consultation intent, observed signals, and missing information.

Required change:

- Case seed creation must be decoupled from authoritative disease facts.
- Case context must remain synthetic user-provided context only.
- Evidence anchors must not be included in the raw-answer generation prompt.

Risk:

- Existing planner starts from Wiki entities and evidence metadata. That is acceptable for selecting topics, but not for injecting answer facts.
- The new system must clearly distinguish topic/entity selection from answer evidence grounding.

Recommendation:

- Reuse existing case-variable machinery.
- Add a new functional module such as `create_consultation_case_seeds.py`.
- Add explicit fields: `case_seed_id`, `scenario_id`, `raw_user_query`, `case_context`, `generation_policy`, `workflow_mode=llm_first`.

### 4.2 LLM Raw Consultation Generation

Assessment: not currently implemented as specified.

The proposed raw generation must:

- Generate without Wiki facts, rule cards, source IDs, page paths, fact IDs, or evidence anchors.
- Preserve raw output exactly.
- Still prohibit precise unsupported dose, withdrawal period, residue, official reporting, culling, quarantine, movement restriction, or enforcement conclusions.

Current Phase 14 is not suitable as-is because it uses skeletons and anchors.

Recommendation:

- Implement a separate raw-generation path.
- Do not modify the existing Wiki-first generator destructively.
- Keep Wiki-first as control baseline.
- Add explicit lineage fields: `generation_model`, `generation_provider`, `generation_prompt_version`, `generation_request_ref`, `generation_response_ref`, `generation_error`.

### 4.3 Answer Claim Extraction

Assessment: required but missing.

This is the most important missing component.

The proposed claim extraction must identify:

- Disease facts.
- Clinical signs.
- Diagnostic reasoning.
- Differential diagnosis.
- Field actions.
- Medication class.
- Specific drug.
- Dosage/course.
- Withdrawal/residue.
- Food safety.
- Regulatory actions.
- Biosecurity.
- Unsupported generalizations.
- Safe boundary statements.

Current regex gates detect some dangerous patterns, but they do not produce auditable claim objects.

Recommendation:

- Implement LLM-assisted claim extraction with strict JSON schema validation.
- Add deterministic detectors for high-risk categories.
- Treat deterministic high-risk hits as claim candidates even if LLM extraction misses them.
- Add tests for dose/course, withdrawal/residue, regulatory execution, food safety, public health, and culling/quarantine/movement claims.

Minimum required output:

- `claim_extraction_id`
- `claim_count`
- `high_risk_claim_count`
- `needs_evidence_claim_count`
- `claims[]`

### 4.4 Wiki And Rule Evidence Retrieval

Assessment: partially reusable, but current matching direction is wrong for the new workflow.

Current system can read:

- Runtime manifest.
- Fact index.
- Drug index.
- Rule-card metadata.
- Evidence coverage and source trust.

But current flow selects facts before generation. The proposed workflow requires retrieving evidence after claims are known.

Recommendation:

- Build a claim-to-evidence matching layer.
- Start with deterministic matching using entity ID, entity name, page path, fact subject/object, usage scope, risk class, source trust, authority level, and rule-card IDs.
- Add conservative fallback: if adequate authority is not found for a high-risk claim, mark it unsupported high risk.

High-risk authority requirements:

- Drug dose/course: label-level or A0/rule-card support.
- Withdrawal/residue/MRL: A0/rule-card support.
- Food safety clearance: A0/rule-card support.
- Regulatory action: current official/rule-card support.
- Disease diagnosis/control facts: authoritative Wiki fact support with adequate evidence coverage.

### 4.5 Claim Fact And Safety Governance

Assessment: conceptually valid, not currently implemented at claim level.

Current Phase 15 can be adapted, but not reused unchanged.

Required change:

- Move from sample-level anchor validation to claim-level review.
- Compute `unsupported_claim_count`, `unsupported_high_risk_claim_count`, `contradicted_claim_count`, `unsafe_claim_count`.
- Admit only when high-risk authoritative claims are supported and unsafe count is zero.

Recommendation:

- Keep current hard gates as a supplemental safety layer.
- Add claim-level deterministic admission invariants.
- Make `unsupported_high_risk_claim_count=0` and `unsafe_claim_count=0` mandatory for all accepted final records.

### 4.6 Evidence-Guided Remediation

Assessment: required and feasible, but currently missing.

The proposed remediation loop is essential because raw LLM-first answers will sometimes contain useful low-risk content mixed with unsafe or unsupported details.

Required behavior:

- Remove or soften unsupported high-risk claims.
- Replace executable claims with safe boundary language.
- Preserve consultation usefulness and tone.
- Avoid exposing internal evidence anchors.

Recommendation:

- Implement remediation as a separate module, not as a hidden mutation inside evaluation.
- Preserve raw answer exactly.
- Store `removed_claims`, `downgraded_claims`, `added_boundary_statements`.

### 4.7 Remediation Re-Evaluation

Assessment: mandatory.

Without re-evaluation, remediation can introduce new unsupported claims and create a false sense of safety.

Required:

- Re-run claim extraction on revised answer.
- Re-run evidence matching for new or changed claims.
- Reject remediation if new unsafe or unsupported high-risk claims appear.

Recommendation:

- Do not admit any remediated answer without `revision_admission_decision=accepted` or equivalent successful review.

### 4.8 Dataset Cleaning And Artifact Standardization

Assessment: valid and necessary.

Current system already has some leakage checks for audit anchors, JSON-like artifacts, and style issues. The proposed cleaning layer is still needed because LLM-first introduces additional leakage risk.

Required checks:

- No `source=`, `fact=`, `rule=`, `page=`, `DIS-`, `RC-` in final user-facing answers.
- No serialized objects.
- No markdown table leakage.
- No internal field names.
- Stable lineage hashes.
- Final answer differs from raw only when remediation was required.

Recommendation:

- Build cleaning as a gate, not a cosmetic postprocessor.
- Rejected and repair-queue records must preserve raw/revised/final lineage.

### 4.9 Final Admission And Training Export

Assessment: current export can be extended.

The allowed final decisions are appropriate:

- `accepted`
- `repair_queue`
- `rejected`
- `review_queue`
- `low_weight_sft`

Recommendation:

- Do not collapse `review_queue` and `repair_queue`.
- Keep raw governance JSONL artifacts separate from stable comparison CSV.
- Add LLM-first training export as new artifact family to avoid destabilizing current Wiki-first outputs.

### 4.10 Baseline Comparison And Monitoring

Assessment: compatible with current system if the 54-field contract is preserved.

Current tests explicitly protect 54-field comparison output:

- `test_baseline_field_contract.py`
- `test_real_farmer_clinical_qa_generation.py`
- `test_swine_wiki_baseline_validation.py`

Recommendation:

- Add `llm_first` as an additional comparison group only through the existing standard comparison mapping.
- Do not add internal governance fields to the comparison CSV.
- Store detailed claim governance in JSONL artifacts and reports.

## 5. Chicken And Swine Shared-System Assessment

### 5.1 Can They Share One System?

Yes, they can share one platform-level system.

The shared system can include:

- Orchestration framework.
- Case seed generation interface.
- Claim extraction schema.
- Evidence retrieval abstraction.
- Claim governance labels.
- Hard safety gate categories.
- Remediation workflow.
- Semantic review and arbitration framework.
- Export and comparison contracts.
- Artifact naming rules.

### 5.2 What Must Not Be Shared Blindly?

The following must remain species-specific:

- Wiki root.
- Runtime manifest.
- Disease fact index.
- Drug fact index.
- Rule cards where species-specific constraints apply.
- A0/label source mappings.
- Withdrawal period and residue constraints.
- Food safety constraints.
- Regulatory boundaries.
- Prompt wording.
- Case variables.
- Judge prompt species lens.
- Export prefix and namespace.

Chicken and swine can share code, but not evidence assumptions.

### 5.3 Current Chicken Status

Recent chicken smoke records show:

- Chicken Wiki pipeline can run Phase 12, 13, 14, 14b, 15, 18, and 16 on small real-API smoke batches.
- Known swine contamination issues were identified and fixed, including swine judge lens, `pig_stage_or_group`, swine wiki root leakage, and missing `assistant_answer`.
- The current validation is still only 5-record and 2-record smoke, not 500-record stability.
- The current output is training export CSV, not yet full 54-field baseline comparison validation.

Conclusion:

- Chicken can use the same pipeline architecture.
- Chicken is not yet proven mature at the same scale as swine.
- Chicken evidence depth may still be thinner, causing higher review rates in larger runs.

## 6. Major Gaps Against The Proposed Spec

### Gap 1: No Executable LLM-First Raw Generation Path

Current generation is still anchored by Wiki skeletons and evidence.

Impact:

- The target workflow cannot be validated yet.
- Relaxing the existing prompt would not equal LLM-first.

Required fix:

- Add a separate `llm_first` raw generation path with no evidence injection.

### Gap 2: No Post-Generation Claim Extraction Module

Current system has hard-gate regex checks but not auditable claims.

Impact:

- Unsupported high-risk claims cannot be counted reliably.
- Claim-level lineage is missing.

Required fix:

- Add schema-validated extraction and deterministic high-risk detectors.

### Gap 3: No Claim-To-Evidence Matching Layer

Current evidence is selected before generation.

Impact:

- The system cannot judge whether raw answer claims are supported after generation.

Required fix:

- Build posthoc retrieval and matching against facts, rule cards, drug constraints, food-safety constraints, and regulatory constraints.

### Gap 4: Existing Fact Evaluation Cannot Be Reused Unchanged

Current Phase 15 validates attached anchors.

Impact:

- It may pass structurally valid anchored samples, but cannot govern arbitrary raw LLM answers.

Required fix:

- Adapt Phase 15 logic to consume `claims[]` and `claim_reviews[]`.

### Gap 5: No Remediation Re-Evaluation Loop

Current system routes repair/review but does not implement the proposed claim-level remediation and re-review loop.

Impact:

- Unsafe generated answers may either be rejected entirely or manually queued; automated repair cannot be safely admitted.

Required fix:

- Add remediation plus mandatory post-remediation extraction/retrieval/governance.

### Gap 6: Artifact Naming And Schema Are Not Yet Implemented

The proposed artifact family names do not exist yet in the executable pipeline.

Impact:

- Acceptance gates cannot be run.

Required fix:

- Add functional module names and artifact names as specified.

## 7. Risk Assessment

### 7.1 Highest Risk: Claim Extraction Misses Dangerous Claims

If extraction misses a precise dose, withdrawal period, regulatory conclusion, or food-safety claim, the system may admit unsafe training data.

Control:

- Combine LLM extraction with deterministic regex detectors.
- Treat detector hits as mandatory claims.
- Make high-risk unknowns fail closed.

### 7.2 High Risk: Evidence Retrieval Misses Valid Evidence

If retrieval fails to find support, useful answers may be over-rejected.

Control:

- Conservative admission is correct for high-risk claims.
- Route unsupported high-risk claims to repair/reject, not accepted.
- Improve retrieval iteratively with reports.

### 7.3 High Risk: Remediation Introduces New Claims

Remediation can create new unsupported details while trying to repair old ones.

Control:

- Mandatory remediation re-evaluation.
- Diff raw claims vs revised claims.
- Reject any remediation with new unsupported high-risk claims.

### 7.4 Medium Risk: Final Answers Become Generic

Over-remediation may remove useful consultation quality.

Control:

- Keep Phase 18 semantic review for naturalness, actionability, responsiveness, and training utility.
- Add metrics for final answer usefulness, not just safety.

### 7.5 Medium Risk: Species Cross-Contamination

Recent chicken smoke records show this risk is real.

Control:

- Require species-aware prompt rendering in every stage.
- Add contamination tests for chicken outputs.
- Keep species-specific wiki roots and runtime manifests.

## 8. Acceptance Gate Review

The proposed acceptance gates are appropriate, but currently not satisfiable because the required modules and artifacts do not exist yet.

Required gates before claiming success:

- 30-record `llm_first` smoke run completes.
- 500-record `llm_first` expanded run completes.
- Existing Wiki-grounded workflow remains runnable as control.
- Stable comparison CSV remains exactly 54 fields.
- Every admitted sample has raw answer lineage, claim review lineage, evidence lineage, and final decision lineage.
- Every remediated admitted sample has successful remediation re-evaluation.
- All admitted records have `unsupported_high_risk_claim_count=0`.
- All admitted records have `unsafe_claim_count=0`.
- Final user-facing answers contain no internal anchors or serialized artifacts.
- Artifact names follow functional enterprise naming.

Additional recommended gates:

- Chicken and swine each pass at least 30-record smoke for LLM-first.
- Chicken and swine each pass species-contamination checks.
- High-risk drug/regulatory samples have separate targeted test packs.
- Claim extraction recall is manually audited on a stratified sample before 500-record run.

## 9. Implementation Recommendation

Recommended implementation sequence:

1. Freeze current Wiki-first workflow as control.
2. Add `llm_first` case seed generation using existing species-aware case variables.
3. Add raw consultation generation with no evidence anchors in prompt.
4. Add claim extraction schema and deterministic high-risk detectors.
5. Add claim-to-evidence retrieval and matching.
6. Adapt fact/hard-gate governance to claim reviews.
7. Add remediation.
8. Add remediation re-evaluation.
9. Add cleaning and artifact standardization.
10. Add LLM-first export and comparison mapping.
11. Run 30-record smoke for swine.
12. Run 30-record smoke for chicken.
13. Run 500-record expanded validation.
14. Compare `llm_first`, `wiki`, `no_wiki`, and `metadata_only`.

Do not:

- Replace current Wiki-first pipeline before LLM-first gates pass.
- Reuse Phase 15 unchanged as proof of LLM-first governance.
- Treat small chicken smoke as scale validation.
- Put detailed governance fields into the stable 54-field comparison CSV.

## 10. Final Review Decision

The reviewed document is acceptable as a target implementation specification with required revisions in interpretation:

- It is not an already executable feature.
- It requires several new core modules.
- It must preserve existing Wiki-first workflow as control.
- It must keep high-risk admission conservative.
- It can support both chicken and swine only through a species-aware shared framework with isolated evidence content and prompts.

Final decision:

`Approved as design direction; not approved as evidence that the current system already satisfies the target.`

Required next action:

Create a concrete implementation plan or engineering ticket set for the missing LLM-first components, starting with raw generation, claim extraction, and claim-to-evidence matching.
