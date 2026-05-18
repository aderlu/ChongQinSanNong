# 2026-05-16 LLM-First Generation With Wiki Posthoc Governance Implementation Spec

## 1. Objective

Build an executable `llm_first` data generation and governance workflow:

1. Generate realistic farmer/veterinary consultation data before Wiki factual constraints are injected.
2. Extract factual, clinical, medication, food-safety, and regulatory claims from the raw answer.
3. Retrieve Wiki/rule evidence after generation and evaluate each claim against authoritative anchors.
4. Remediate risky or unsupported answers without losing the raw answer lineage.
5. Clean, normalize, and organize records before final training admission.
6. Enforce strict species-aware runtime isolation and evidence isolation.
7. Keep the existing Wiki-grounded workflow available as a control baseline.

The target is not to weaken Wiki governance. The target is to move Wiki from a generation-time constraint to a post-generation admission gate.

## 2. Current System Reality

The current implementation already has useful building blocks:

- Wiki-grounded sample planning and answer skeleton generation.
- Evidence anchors, rule cards, source-trust fields, and evidence-coverage fields.
- Deterministic fact checks, hard safety gates, semantic review, arbitration, and layered exports.
- Baseline comparison groups including `wiki`, `no_wiki`, and `metadata_only`.
- A stable 51 sample fields + 3 comparison keys contract for baseline comparison.

The current implementation is not yet a complete or directly runnable `llm_first` workflow because generated samples are still expected to carry evidence anchors before fact evaluation. Therefore, this spec requires new post-generation claim extraction, species runtime registry, claim-to-evidence matching, claim governance, remediation review, and export-adapter capabilities before any 30-record `llm_first` smoke run can be considered valid.

Implementation evidence that must be considered during delivery:

- Current generation creates Wiki-derived plans, answer skeletons, audit answers, user-facing clinical answers, and `evidence_anchors` before fact evaluation.
- Current fact governance requires `sample_id`, `plan_id`, `skeleton_id`, `question`, `stage_2_grounded`, `evidence_anchors`, `ability_layer`, `risk_class`, `source_trust`, and `evidence_coverage` before it can pass structure checks.
- Current export combines a coarse export decision with a separate training admission tag. The implementation already treats `accepted`, `review`, and `rejected` as export decisions, while `main_sft`, `low_weight_sft`, `repair_queue`, and `reject_queue` are training-use or routing tags.
- Current baseline comparison contract is 51 standardized sample fields plus 3 comparison keys. Detailed governance fields must not be added directly to this comparison CSV.
- Current multi-species execution risk is real: swine and chicken can share orchestration code, but must not share runtime evidence roots, source indexes, drug constraints, rule cards, species wording, or judge lens assumptions.
- Current species configuration is species-aware but not yet species-isolated. Existing configuration covers display/runtime selection concepts such as `species_key`, `species_cn`, `species_en`, `farm_context_cn`, `animal_group_label`, `case_stage_field`, `output_prefix`, `runtime_selection_key`, and `required_runtime_files`; it does not yet provide the runtime registry fields needed to prove Wiki-root, evidence, entity, rule-card, drug, and terminology isolation.
- Current Wiki-first tests protect skeleton `must_include_claims` and pre-generation `evidence_anchors`. They remain valuable for the control workflow, but they do not prove the `llm_first` posthoc-governance target.

Implementation status statement:

- This document is an implementation target, not a statement that the current repository can already run this workflow.
- The design is ready to implement only after the runtime registry/schema, claim extraction, claim evidence retrieval, claim governance, remediation review, and `llm_first` export adapter are built.
- The existing Wiki-first workflow and Phase15/Phase16 modules may be used as reference behavior, but they must not be treated as drop-in execution layers for `llm_first`.

## 3. Non-Negotiable Principles

- Raw generation must be preserved exactly as produced by the model.
- Wiki/rule governance must remain an admission gate, not a decorative report.
- No unsupported high-risk clinical, medication, withdrawal-period, residue, food-safety, or regulatory claim may enter training output.
- Remediated answers must be evaluated again before admission.
- The system must preserve raw answer, extracted claims, evidence matches, remediation traces, final answer, and final admission decision.
- Baseline comparison fields must remain stable unless a separate migration is approved.
- Historical compatibility entrypoints may remain as wrappers, but new records, reports, module names, and output artifact names must use functional enterprise naming instead of ordinal lifecycle naming.
- Export decision, training-use tag, and queue routing must remain separate concepts.
- Species-aware runtime isolation and evidence isolation are hard admission requirements, not optional quality improvements.
- A sample may use shared orchestration code, but every evidence lookup, prompt, claim review, remediation, and export decision must be bound to one explicit species profile.
- Cross-species evidence, rule-card, drug-constraint, Wiki-root, prompt-lens, or terminology leakage must route the sample to rejection or repair, never direct admission.

## 4. Functional Workflow

```text
Scenario and Case Seed Creation
-> Species Runtime and Evidence Isolation Binding
-> LLM Raw Consultation Generation
-> Answer Claim Extraction
-> Wiki and Rule Evidence Retrieval
-> Claim Fact and Safety Governance
-> Evidence-Guided Answer Remediation
-> Remediation Re-Evaluation
-> Dataset Cleaning and Artifact Standardization
-> Final Admission and Training Export
-> Baseline Comparison and Monitoring
```

## 5. Functional Components

### 5.1 Scenario and Case Seed Creation

Purpose: create realistic consultation prompts without forcing the answer to follow Wiki facts.

Inputs:

- `entity_id`
- `entity_name`
- `entity_type`
- `species`
- `farm_context`
- `production_stage`
- `user_persona`
- `consultation_intent`
- `urgency_level`
- `information_completeness`
- `observed_signals`
- `missing_info`
- `risk_class`
- `expected_output_type`

Outputs:

- `case_seed_id`
- `scenario_id`
- `raw_user_query`
- `case_context`
- `generation_policy`

Required behavior:

- Keep synthetic case context separate from authoritative disease facts.
- Allow weak or incomplete user information because real consultations are incomplete.
- Include enough metadata for posthoc retrieval, but do not provide evidence anchors to the generation prompt.

### 5.2 Species Runtime and Evidence Isolation Binding

Purpose: bind every sample to exactly one species profile before generation, retrieval, evaluation, remediation, and export.

Inputs:

- `species`
- `entity_id`
- `entity_name`
- `entity_type`
- `case_seed_id`
- `workflow_mode`
- configured species runtime registry

Minimum species runtime registry fields:

- `species_profile_id`
- `species_key`
- `species_cn`
- `species_en`
- `species_runtime_namespace`
- `wiki_root`
- `runtime_manifest_path`
- `fact_index_path`
- `drug_index_path`
- `rule_card_index_path`
- `source_authority_index_path`
- `hard_block_rule_path`
- `allowed_entity_id_prefixes`
- `allowed_fact_id_prefixes`
- `allowed_rule_card_id_prefixes`
- `allowed_source_id_prefixes`
- `forbidden_species_terms`
- `forbidden_wiki_roots`
- `prompt_lens`
- `drug_constraint_namespace`
- `regulatory_rule_namespace`

The registry may be implemented as `species_runtime_registry.py` or as an extension of the existing species configuration schema, but it must be validated independently from display-only species metadata.

Outputs:

- `species_profile_id`
- `species_key`
- `species_cn`
- `species_runtime_namespace`
- `wiki_root`
- `runtime_manifest_path`
- `fact_index_path`
- `drug_index_path`
- `rule_card_index_path`
- `source_authority_index_path`
- `allowed_entity_id_prefixes`
- `forbidden_species_terms`
- `forbidden_wiki_roots`
- `species_isolation_status`
- `species_isolation_violations`

Required behavior:

- Each record must bind to exactly one species profile before any LLM prompt or evidence retrieval is built.
- Runtime paths must resolve under the selected species Wiki root only.
- Evidence retrieval must only read the selected species runtime manifest, fact index, drug index, rule cards, source authority index, and hard-block rules.
- Prompt rendering must use the selected species lens for animal group wording, production-stage wording, disease context, drug-boundary wording, and judge instructions.
- Claim extraction and remediation prompts must include the selected species profile and must not include another species' Wiki root, disease examples, drug constraints, or rule-card assumptions.
- Entity IDs, fact IDs, rule-card IDs, page paths, and source IDs must be validated against the selected species namespace.
- Prefix checks alone are insufficient because swine and chicken runtimes may share generic IDs such as `DIS-*`, `DRUG-*`, `RC-*`, or `SRC-*`.
- Species-isolation validation must also verify resolved absolute Wiki root, manifest membership, page path under selected root, fact-index source file, drug-index source file, rule-card-index source file, source-authority-index source file, runtime namespace, and artifact provenance hash.
- If any evidence anchor points to another species root, forbidden entity prefix, forbidden species term, or incompatible rule/drug constraint, set `species_isolation_status=failed`.
- Samples with failed species isolation must use `final_export_decision=rejected` or `final_export_decision=review` with `queue_routing=repair_queue`.
- No failed species-isolation sample may enter `main_sft`, `low_weight_sft`, or `boundary_refusal_train`.

### 5.3 LLM Raw Consultation Generation

Purpose: generate natural, diverse, clinically useful answers without Wiki-first answer skeleton constraints.

Inputs:

- `raw_user_query`
- `case_context`
- `generation_policy`
- `risk_class`
- `expected_output_type`

Outputs:

- `raw_user_query`
- `raw_assistant_answer`
- `generation_model`
- `generation_provider`
- `generation_prompt_version`
- `generation_request_ref`
- `generation_response_ref`
- `generation_error`

Required behavior:

- The prompt must ask for realistic veterinary consultation style.
- The prompt may allow clinical reasoning, field actions, and treatment framework.
- The prompt must still prohibit precise unsupported dosage, withdrawal-period, residue, reporting, culling, movement-control, or official enforcement conclusions.
- No Wiki source, fact, page, rule, entity identifier, or evidence anchor may be injected into the raw answer prompt.
- The prompt must be rendered from the bound species profile and must include only that species' animal group wording, production-stage wording, and consultation context.
- The prompt must not contain another species' common names, species-specific disease examples, Wiki root, evidence paths, rule-card assumptions, or drug-use constraints.

### 5.4 Answer Claim Extraction

Purpose: convert the raw answer into auditable claims.

Inputs:

- `raw_user_query`
- `raw_assistant_answer`
- `case_context`
- `entity_id`
- `entity_name`
- `species`
- `risk_class`

Outputs:

- `claim_extraction_id`
- `claim_count`
- `claims[]`

Each claim must include:

- `claim_id`
- `claim_text`
- `claim_type`
- `clinical_domain`
- `risk_level`
- `needs_evidence`
- `source_span`
- `normalized_subject`
- `normalized_predicate`
- `normalized_object`
- `is_case_context_claim`
- `is_authoritative_knowledge_claim`

Allowed `claim_type` values:

- `disease_fact`
- `clinical_sign`
- `diagnostic_reasoning`
- `differential_diagnosis`
- `field_action`
- `medication_class`
- `specific_drug`
- `dosage_or_course`
- `withdrawal_or_residue`
- `food_safety`
- `regulatory_action`
- `biosecurity`
- `unsupported_generalization`
- `safe_boundary_statement`

Required behavior:

- Separate case-context observations from authoritative knowledge claims.
- Treat dosage, course, withdrawal period, residue, food-safety, official reporting, culling, quarantine, movement restriction, and disposal claims as high risk by default.
- Mark vague but potentially harmful claims as `needs_evidence=true`.
- Extraction must be deterministic enough for repeatable audits. LLM extraction may be used, but the result must be validated by schema and rule checks.
- Extraction must tag every claim with `species_key` and `species_profile_id`.
- Any claim containing forbidden cross-species terminology must be marked with `species_isolation_violation=true`.

### 5.5 Wiki and Rule Evidence Retrieval

Purpose: retrieve evidence after claims are known.

Inputs:

- `claims[]`
- `entity_id`
- `entity_name`
- `species`
- `risk_class`
- `expected_output_type`

Outputs:

- `wiki_retrieval_id`
- `wiki_retrieval_query`
- `wiki_retrieved_entity_ids`
- `retrieved_evidence[]`
- `evidence_anchors[]`
- `wiki_source_trust`
- `wiki_evidence_coverage`
- `wiki_evidence_anchor_count`

Each evidence anchor must include:

- `claim_id`
- `anchor_type`
- `fact_id`
- `source_id`
- `rule_card_id`
- `page_relpath`
- `authority_level`
- `source_trust`
- `evidence_coverage`
- `usage_scope`
- `match_confidence`
- `evidence_quote_span`

Required behavior:

- Retrieval must search disease facts, drug constraints, rule cards, withdrawal/residue constraints, food-safety boundaries, and regulatory boundaries.
- High-risk claims require rule-card or A0/label-level evidence, depending on claim type.
- If retrieval cannot find adequate authority for a high-risk claim, the claim must be treated as unsupported high risk.
- Retrieval must be scoped to the bound `wiki_root`, runtime manifest, fact index, drug index, rule-card index, and source authority index.
- Retrieval must reject candidate evidence if its page path, source path, entity ID, fact ID, rule-card ID, or runtime namespace belongs to another species.
- Evidence anchors must include `species_key`, `species_profile_id`, `wiki_root`, and `runtime_namespace`.
- Evidence anchors must include `species_key`, `species_profile_id`, `wiki_root`, and `species_runtime_namespace`.
- Cross-species evidence must not be downgraded to low confidence; it must be treated as an isolation failure.

### 5.6 Claim Fact and Safety Governance

Purpose: score every extracted claim and decide whether the raw answer can be admitted, remediated, or rejected.

Implementation boundary:

- This must be a new claim-governance phase, not a direct invocation of the existing Wiki-first Phase15 structure checker.
- Recommended module name: `evaluate_claim_fact_and_safety_governance.py`.
- Inputs are raw records, extracted claims, retrieved evidence, and species-runtime binding.
- Outputs are claim reviews, raw-answer admission decisions, and claim-level failure reasons.
- Existing Phase15 behavior remains the control path for Wiki-first samples that already contain skeletons and pre-generation `evidence_anchors`.
- A raw `llm_first` record must not be rejected merely because it lacks `skeleton_id`, `stage_2_grounded`, or pre-existing `evidence_anchors`; those fields belong to the Wiki-first control contract.

Inputs:

- `raw_assistant_answer`
- `claims[]`
- `evidence_anchors[]`
- `retrieved_evidence[]`
- `case_context`

Outputs:

- `claim_review_id`
- `claim_reviews[]`
- `wiki_fact_score`
- `wiki_safety_score`
- `unsupported_claim_count`
- `unsupported_high_risk_claim_count`
- `contradicted_claim_count`
- `unsafe_claim_count`
- `raw_answer_admission_decision`
- `raw_answer_reject_reasons`

Allowed per-claim review labels:

- `supported`
- `partially_supported`
- `unsupported_low_risk`
- `unsupported_high_risk`
- `contradicted`
- `unsafe`
- `case_context_only`
- `safe_boundary_supported`

Raw answer admission rules:

- Admit only if all authoritative high-risk claims are supported and no unsafe claim exists.
- Send to remediation if unsupported claims are removable or boundary-correctable.
- Reject if the answer contains unsafe advice, contradicted high-risk advice, fabricated regulatory execution, fabricated precise dosage, fabricated withdrawal period, or unrepairable clinical misinformation.
- Reject or repair any sample with `species_isolation_status=failed`.
- Do not count cross-species evidence as supporting evidence for any claim.

### 5.7 Evidence-Guided Answer Remediation

Purpose: revise only the unsafe, unsupported, contradicted, or over-specific parts of the raw answer.

Inputs:

- `raw_user_query`
- `raw_assistant_answer`
- `claim_reviews[]`
- `evidence_anchors[]`
- `raw_answer_reject_reasons`

Outputs:

- `remediation_id`
- `revision_needed`
- `revised_assistant_answer`
- `revision_type`
- `revision_reasons`
- `removed_claims`
- `downgraded_claims`
- `added_boundary_statements`
- `remediation_model`
- `remediation_prompt_version`

Required behavior:

- Preserve original tone, structure, and consultation usefulness where safe.
- Remove or soften unsupported high-risk claims.
- Replace unsupported execution claims with safe boundary language and professional verification requirements.
- Do not turn the answer into a generic template, evidence report, or Wiki summary.
- Do not expose internal evidence anchors in the final user-facing answer.
- Remediation must use the same species profile as the raw answer.
- Remediation must remove cross-species terminology, evidence assumptions, and drug/regulatory constraints unless they are valid for the bound species.

### 5.8 Remediation Re-Evaluation

Purpose: prevent remediation from introducing new unsupported claims.

Inputs:

- `revised_assistant_answer`
- `raw_assistant_answer`
- `claim_reviews[]`
- `evidence_anchors[]`

Outputs:

- `remediation_review_id`
- `revised_claims[]`
- `revised_claim_reviews[]`
- `revision_fact_score`
- `revision_safety_score`
- `revision_admission_decision`
- `revision_reject_reasons`

Required behavior:

- Run claim extraction again on the revised answer.
- Run evidence retrieval/matching again when new claims appear.
- Compare removed, downgraded, preserved, and newly introduced claims.
- Reject remediation if it introduces new unsafe or unsupported high-risk claims.
- Re-run species-isolation validation after remediation.
- Reject remediation if it introduces any cross-species terminology, evidence anchor, runtime path, rule-card reference, or drug/regulatory assumption.

### 5.9 Dataset Cleaning and Artifact Standardization

Purpose: clean records, normalize schema, repair filenames, and prepare enterprise-grade outputs.

Inputs:

- Raw generated records.
- Extracted claim records.
- Evidence retrieval records.
- Governance review records.
- Remediation records.
- Remediation re-evaluation records.

Outputs:

- `cleaned_training_candidates`
- `cleaning_report`
- `schema_validation_report`
- `artifact_inventory`
- `filename_migration_report`

Cleaning rules:

- Normalize all text encoding to UTF-8 without mojibake.
- Strip leaked audit anchors from user-facing answers.
- Remove serialized object fragments, JSON leakage, markdown tables, and internal field names from final answers.
- Normalize whitespace, line breaks, punctuation, and empty-string/null behavior.
- Deduplicate records by `case_seed_id`, `raw_user_query`, and normalized final answer hash.
- Enforce required lineage fields before export.
- Validate that final answer differs from raw answer only when remediation was required.
- Validate that rejected and repair-queue records still preserve raw/revised/final answer lineage.
- Validate that final user-facing answers do not contain forbidden cross-species terms.
- Validate that all lineage paths and evidence anchors belong to the bound species namespace.

Filename and artifact naming rules:

- New files must use functional names, not ordinal lifecycle names.
- Executable module names must be lowercase ASCII snake_case.
- Data artifacts and reports must be lowercase ASCII kebab-case.
- New filenames must include dataset family, workflow mode, functional component, run date, and optional run label.
- Do not introduce new filenames containing ordinal lifecycle wording or numeric lifecycle prefixes.
- Historical files may remain for compatibility, but new reports must use the functional names below.

Recommended executable module names:

- `create_consultation_case_seeds.py`
- `generate_llm_first_raw_consultations.py`
- `extract_consultation_answer_claims.py`
- `retrieve_wiki_evidence_for_claims.py`
- `evaluate_claim_fact_and_safety_governance.py`
- `remediate_answers_with_wiki_evidence.py`
- `review_remediated_answers.py`
- `clean_and_standardize_training_candidates.py`
- `export_admitted_training_datasets.py`
- `compare_generation_governance_workflows.py`

Recommended output artifact names:

- `llm-first-case-seeds-{run_date}-{run_label}.jsonl`
- `llm-first-raw-consultations-{run_date}-{run_label}.jsonl`
- `llm-first-extracted-claims-{run_date}-{run_label}.jsonl`
- `llm-first-wiki-evidence-matches-{run_date}-{run_label}.jsonl`
- `llm-first-claim-governance-reviews-{run_date}-{run_label}.jsonl`
- `llm-first-remediated-answers-{run_date}-{run_label}.jsonl`
- `llm-first-remediation-reviews-{run_date}-{run_label}.jsonl`
- `llm-first-cleaned-training-candidates-{run_date}-{run_label}.jsonl`
- `llm-first-admitted-training-dataset-{run_date}-{run_label}.jsonl`
- `llm-first-repair-queue-{run_date}-{run_label}.jsonl`
- `llm-first-rejected-samples-{run_date}-{run_label}.jsonl`
- `llm-first-governance-report-{run_date}-{run_label}.json`
- `llm-first-governance-report-{run_date}-{run_label}.md`
- `llm-first-artifact-inventory-{run_date}-{run_label}.json`
- `workflow-comparison-standard-{run_date}-{run_label}.csv`

### 5.10 Final Admission and Training Export

Purpose: produce train-ready outputs only after governance and cleaning pass.

Implementation boundary:

- This layer must include a `llm_first` export adapter even if it reuses existing export utilities internally.
- The adapter must normalize legacy export fields into the spec fields without mixing decision, training-use, and queue-routing semantics.
- `export_decision` may map to `final_export_decision`.
- `sft_admission` may map to `final_training_use_tag` only when its value is a training-use tag.
- Queue values such as `repair_queue`, `review_queue`, `reject_queue`, or `rejected_queue` must be written only to `queue_routing`.
- Legacy Phase16 behavior remains available for Wiki-first/control artifacts, but `llm_first` artifacts must emit the normalized fields below.

Inputs:

- `cleaned_training_candidates`
- Raw governance decision.
- Remediation governance decision.
- Semantic quality review.
- Arbitration result when needed.

Outputs:

- `final_assistant_answer`
- `final_export_decision`
- `final_training_use_tag`
- `queue_routing`
- `sft_admission` only as a legacy compatibility mirror when required by downstream readers
- `risk_level`
- `hard_fail`
- `hard_fail_codes`
- `main_issues`
- `repair_suggestion`
- `species_isolation_status`
- `species_isolation_violations`

Allowed `final_export_decision` values:

- `accepted`
- `rejected`
- `review`

Allowed `final_training_use_tag` values:

- `main_sft`
- `low_weight_sft`
- `boundary_refusal_train`
- `evaluation_only`
- `do_not_train`

Allowed `queue_routing` values:

- `none`
- `repair_queue`
- `review_queue`
- `rejected_queue`

Admission rules:

- `final_export_decision=accepted`: fact governance passed, safety governance passed, cleaning passed, and semantic quality is train-usable.
- `final_export_decision=review`: the sample is not train-ready and must be routed to `repair_queue` or `review_queue`.
- `final_export_decision=rejected`: unsafe, contradicted, untraceable high-risk, structurally invalid, or not recoverable.
- `final_training_use_tag=main_sft`: accepted for primary supervised fine-tuning.
- `final_training_use_tag=low_weight_sft`: accepted but lower training weight due to weaker utility.
- `final_training_use_tag=boundary_refusal_train`: accepted for safe-boundary or refusal training.
- `final_training_use_tag=evaluation_only`: safe enough for evaluation/calibration but not for training.
- `final_training_use_tag=do_not_train`: not allowed in training output.
- `queue_routing=none`: no queue routing is needed.
- `queue_routing=repair_queue`: repairable, not admitted until a successful remediation re-evaluation exists.
- `queue_routing=review_queue`: requires human review due to ambiguity.
- `queue_routing=rejected_queue`: retained only for audit, regression, or negative examples if explicitly allowed outside training.
- `species_isolation_status=passed` is required for `final_export_decision=accepted`.
- `species_isolation_status=failed` requires `final_export_decision=rejected` or `final_export_decision=review` with `queue_routing=repair_queue`.

### 5.11 Baseline Comparison and Monitoring

Purpose: compare `llm_first`, existing Wiki-grounded workflow, no-Wiki baseline, and metadata-only baseline.

Inputs:

- Standardized outputs from all workflows.
- General consultation judge results.
- Grounding audit results.
- Final admission decisions.

Outputs:

- `workflow-comparison-standard-{run_date}-{run_label}.csv`
- `workflow-comparison-summary-{run_date}-{run_label}.json`
- `workflow-comparison-report-{run_date}-{run_label}.md`

Required behavior:

- Preserve the existing 51 sample fields + 3 comparison keys baseline contract.
- Do not overload the 54-field comparison contract with internal governance fields.
- Store detailed governance fields in JSONL artifacts and metadata, not in the stable comparison CSV.
- Report acceptance rate, repair rate, rejection rate, unsafe claim rate, unsupported high-risk claim rate, semantic quality, naturalness score, and traceability score.

## 6. Required Schema Additions

Raw generation layer:

- `workflow_mode`
- `species_profile_id`
- `species_key`
- `species_cn`
- `species_runtime_namespace`
- `wiki_root`
- `runtime_manifest_path`
- `fact_index_path`
- `drug_index_path`
- `rule_card_index_path`
- `source_authority_index_path`
- `species_isolation_status`
- `species_isolation_violations`
- `case_seed_id`
- `raw_user_query`
- `raw_assistant_answer`
- `generation_model`
- `generation_provider`
- `generation_prompt_version`
- `generation_request_ref`
- `generation_response_ref`

Claim layer:

- `claim_extraction_id`
- `species_profile_id`
- `species_key`
- `claims`
- `claim_count`
- `high_risk_claim_count`
- `needs_evidence_claim_count`
- `cross_species_claim_count`

Evidence layer:

- `wiki_retrieval_id`
- `species_profile_id`
- `species_key`
- `species_runtime_namespace`
- `wiki_root`
- `wiki_retrieval_query`
- `wiki_retrieved_entity_ids`
- `retrieved_evidence`
- `evidence_anchors`
- `wiki_evidence_anchor_count`
- `wiki_evidence_coverage`
- `wiki_source_trust`
- `cross_species_evidence_count`

Governance layer:

- `claim_reviews`
- `wiki_fact_score`
- `wiki_safety_score`
- `unsupported_claim_count`
- `unsupported_high_risk_claim_count`
- `contradicted_claim_count`
- `unsafe_claim_count`
- `cross_species_violation_count`
- `raw_answer_admission_decision`
- `raw_answer_reject_reasons`

Remediation layer:

- `revision_needed`
- `revised_assistant_answer`
- `revision_type`
- `revision_reasons`
- `removed_claims`
- `downgraded_claims`
- `added_boundary_statements`
- `revision_admission_decision`
- `revision_reject_reasons`

Cleaning layer:

- `cleaning_status`
- `cleaning_actions`
- `schema_validation_status`
- `species_isolation_validation_status`
- `artifact_name`
- `artifact_family`
- `lineage_hash`
- `raw_answer_hash`
- `final_answer_hash`

Export layer:

- `final_assistant_answer`
- `final_export_decision`
- `final_training_use_tag`
- `queue_routing`
- `sft_admission` only as a legacy compatibility mirror when required by downstream readers
- `species_profile_id`
- `species_key`
- `species_isolation_status`
- `species_isolation_violations`
- `risk_level`
- `hard_fail`
- `hard_fail_codes`
- `main_issues`
- `repair_suggestion`

## 7. Phased Execution Plan

This plan is intentionally staged. A later phase must not begin until the previous phase has passed its acceptance gate, except for harmless documentation or test scaffolding. Each phase must leave the existing Wiki-first workflow runnable as a control.

### 7.1 Phase 0: Baseline Lock and Compatibility Inventory

Purpose: freeze the current behavior before new `llm_first` work begins.

Scope:

- Identify the current Wiki-first entrypoints, Phase15 fact-evaluation entrypoints, Phase16 export entrypoints, species configuration files, and baseline comparison writers.
- Record the current required fields for Wiki-first samples, including `skeleton_id`, `stage_2_grounded`, `evidence_anchors`, `source_trust`, and `evidence_coverage`.
- Record the current 51 sample fields + 3 comparison keys contract.
- Mark existing Wiki-first tests for `must_include_claims` and pre-generation `evidence_anchors` as control-workflow tests.

Deliverables:

- Baseline inventory note or test fixture documenting current Wiki-first contracts.
- Regression test command list for Wiki-first control workflow.
- Compatibility decision that Phase15 and Phase16 remain available for Wiki-first/control artifacts.

Acceptance gate:

- Existing Wiki-first tests still pass without requiring any `llm_first` fields.
- The 54-field comparison CSV contract is documented and protected by a test.
- No `llm_first` implementation has changed Wiki-first required input schema.
- Phase15 is explicitly classified as Wiki-first/control unless invoked through a future adapter.
- Phase16 is explicitly classified as legacy export/control unless invoked through a future normalized export adapter.

Blockers:

- Do not proceed if the current control workflow cannot run or its comparison-field contract is unknown.
- Do not proceed if new `llm_first` fields are required by Wiki-first tests.

### 7.2 Phase 1: Species Runtime Registry and Isolation Foundation

Purpose: make species isolation executable before any new raw generation or retrieval work.

Scope:

- Add `species_runtime_registry.py` or extend the existing species schema with independently validated runtime fields.
- Add `species_profile_id`, `species_runtime_namespace`, `wiki_root`, `runtime_manifest_path`, `fact_index_path`, `drug_index_path`, `rule_card_index_path`, `source_authority_index_path`, `hard_block_rule_path`, allowed ID prefixes, forbidden species terms, forbidden Wiki roots, prompt lens, drug namespace, and regulatory namespace.
- Add path-resolution checks that require runtime files to live under the selected species runtime root.
- Add isolation validators for prompts, evidence anchors, page paths, manifest membership, source index files, rule-card index files, drug index files, runtime namespace, and artifact provenance hash.

Deliverables:

- Species runtime registry.
- Species profile resolver.
- Species isolation validator.
- Unit tests for swine and chicken profiles.

Acceptance gate:

- Registry resolves every supported species to exactly one runtime profile.
- Unknown species and missing runtime files fail closed.
- Swine and chicken profiles resolve to different `species_profile_id`, `species_runtime_namespace`, and `wiki_root`.
- Cross-species Wiki roots, forbidden terms, page paths, rule cards, source paths, or drug constraints produce `species_isolation_status=failed`.
- Validation does not rely only on generic ID prefixes such as `DIS-*`, `DRUG-*`, `RC-*`, or `SRC-*`.

Blockers:

- Do not proceed if any species can run without a profile.
- Do not proceed if evidence or prompt validation can pass with another species' Wiki root or runtime namespace.

### 7.3 Phase 2: LLM-First Raw Generation and Prompt Isolation

Purpose: produce raw consultation records without Wiki-first evidence injection.

Scope:

- Add `workflow_mode=llm_first`.
- Bind every case seed to one `species_profile_id` before prompt rendering.
- Add `generate_llm_first_raw_consultations.py`.
- Generate raw user query, case context, generation policy, and raw assistant answer.
- Validate prompts before every model call.

Deliverables:

- Raw generation module.
- Prompt renderer bound to species profile.
- Prompt isolation tests.
- Small deterministic fixture set for raw records.

Acceptance gate:

- Raw generation prompts contain no `source=`, `fact=`, `rule=`, `page=`, `DIS-`, `DRUG-`, `RC-`, `SRC-`, Wiki page path, or evidence-anchor identifier.
- Raw records include `workflow_mode=llm_first`, `species_profile_id`, `species_key`, `species_runtime_namespace`, `case_seed_id`, `raw_user_query`, and `raw_assistant_answer`.
- Prompt rendering uses only the selected species profile and rejects forbidden cross-species terms.
- Raw records are not required to contain `skeleton_id`, `stage_2_grounded`, or pre-existing `evidence_anchors`.
- Wiki-first generation still produces its existing skeleton and evidence-anchor outputs.

Blockers:

- Do not proceed if any raw-generation prompt includes Wiki facts, source IDs, page paths, rule-card IDs, or another species' prompt lens.
- Do not proceed if raw records cannot preserve the original model answer unchanged.

### 7.4 Phase 3: Claim Extraction and Claim Schema Validation

Purpose: convert raw answers into auditable claim records.

Scope:

- Add `extract_consultation_answer_claims.py`.
- Extract `claims[]` with claim type, risk level, evidence need, source span, normalized subject/predicate/object, case-context flag, authoritative-knowledge flag, `species_key`, and `species_profile_id`.
- Combine LLM extraction with deterministic detectors for dosage, course, withdrawal, residue, regulatory action, food safety, specific drug, and public health claims.
- Mark forbidden cross-species terminology as claim-level species-isolation violation.

Deliverables:

- Claim extraction module.
- Claim schema validator.
- High-risk claim classifier.
- Unit tests for clinical, medication, food-safety, regulatory, and safe-boundary claims.

Acceptance gate:

- Claim extraction validates schema for every raw record.
- Dosage/course, withdrawal/residue, regulatory action, food-safety, specific-drug, and public-health claims are detected as high risk by default.
- Case-context observations are separated from authoritative knowledge claims.
- Forbidden cross-species terms produce claim-level isolation violation.
- Extraction output is deterministic enough for repeated fixture tests.

Blockers:

- Do not proceed if high-risk claims can bypass `needs_evidence=true`.
- Do not proceed if extraction cannot preserve source spans from the raw answer.

### 7.5 Phase 4: Claim Evidence Retrieval and Matching

Purpose: retrieve Wiki/rule evidence after claims are known and only from the selected species runtime.

Scope:

- Add `retrieve_wiki_evidence_for_claims.py`.
- Search disease facts, drug constraints, rule cards, withdrawal/residue constraints, food-safety boundaries, and regulatory boundaries.
- Match evidence to claim IDs.
- Validate every candidate evidence item against the selected species runtime.

Deliverables:

- Claim-scoped evidence retrieval module.
- Claim-to-evidence matcher.
- Evidence anchor schema.
- Cross-species evidence rejection tests.

Acceptance gate:

- Retrieval reads only the bound `wiki_root`, runtime manifest, fact index, drug index, rule-card index, and source authority index.
- Every evidence anchor includes `claim_id`, `species_key`, `species_profile_id`, `wiki_root`, `species_runtime_namespace`, source/fact/rule identifiers, page path, authority level, trust, coverage, and usage scope.
- Cross-species evidence is recorded as isolation failure, not low-confidence support.
- High-risk claims without adequate A0, label-level, or rule-card evidence remain unsupported.
- Prefix, path, manifest, namespace, index-source, and provenance checks are all exercised by tests.

Blockers:

- Do not proceed if retrieval can read another species' Wiki root or rule-card index.
- Do not proceed if unsupported high-risk claims are silently downgraded.

### 7.6 Phase 5: Claim Fact and Safety Governance

Purpose: decide whether the raw answer can be admitted, remediated, or rejected.

Scope:

- Add `evaluate_claim_fact_and_safety_governance.py`.
- Consume raw records, extracted claims, retrieved evidence, and species-runtime binding.
- Produce `claim_reviews[]`, scores, unsupported counts, unsafe counts, raw-answer admission decision, and reject reasons.
- Keep existing Phase15 for Wiki-first control; do not route raw `llm_first` records through Phase15's pre-anchored schema.

Deliverables:

- Claim governance module.
- Per-claim review labels.
- Raw-answer admission decision logic.
- Unit tests for supported, unsupported, contradicted, unsafe, and case-context-only claims.

Acceptance gate:

- Raw `llm_first` records pass governance without `skeleton_id`, `stage_2_grounded`, or pre-existing `evidence_anchors`.
- Unsupported high-risk claims are rejected or routed to repair, never admitted.
- Unsafe advice, contradicted high-risk advice, fabricated dosage, fabricated withdrawal period, and fabricated regulatory execution are rejected or routed to repair.
- Cross-species evidence never supports a claim.
- Wiki-first Phase15 tests still pass as control tests.

Blockers:

- Do not proceed if any unsupported high-risk claim can produce raw admission.
- Do not proceed if species-isolation failure can produce direct training admission.

### 7.7 Phase 6: Remediation and Remediation Re-Evaluation

Purpose: repair only safe and repairable answers, then re-run governance.

Scope:

- Add `remediate_answers_with_wiki_evidence.py`.
- Add `review_remediated_answers.py`.
- Remove, soften, or boundary-correct unsafe or unsupported claims.
- Re-run claim extraction, evidence retrieval, claim governance, and species-isolation validation on revised answers.

Deliverables:

- Remediation module.
- Remediation re-evaluation module.
- Revision lineage fields.
- Tests for removed claims, downgraded claims, added boundary statements, and newly introduced claim blocking.

Acceptance gate:

- Remediated answers preserve raw answer lineage and revision reasons.
- Re-evaluation catches any new unsupported high-risk claim introduced by remediation.
- Remediated final answers do not expose internal evidence anchors, IDs, page paths, or serialized audit fragments.
- Remediation cannot change species profile.
- Remediation introducing cross-species terminology, evidence, runtime path, rule-card reference, or drug/regulatory assumption is rejected.

Blockers:

- Do not proceed if remediation can be admitted without re-extraction and re-governance.
- Do not proceed if raw lineage is overwritten or lost.

### 7.8 Phase 7: Cleaning, Artifact Standardization, and Filename Validation

Purpose: normalize records and enforce new artifact naming before export.

Scope:

- Add `clean_and_standardize_training_candidates.py`.
- Add artifact writer for `llm_first` outputs.
- Add filename validator for lowercase ASCII kebab-case data artifacts and reports.
- Strip leaked audit anchors, object fragments, JSON leakage, markdown tables, internal field names, and forbidden cross-species terms from final user-facing answers.

Deliverables:

- Cleaning module.
- Artifact writer.
- Filename validator.
- Artifact inventory report.
- Schema validation report.

Acceptance gate:

- New `llm_first` artifacts use functional kebab-case names.
- New executable modules use lowercase ASCII snake_case names.
- Historical snake_case artifacts remain read-only compatibility inputs only.
- Final answers contain no `source=`, `fact=`, `rule=`, `page=`, `DIS-`, `RC-`, serialized object fragments, or internal audit labels.
- Rejected and repair-queue records still preserve raw, revised, final, and decision lineage.

Blockers:

- Do not proceed if new `llm_first` writers emit ordinal lifecycle names or snake_case data artifact names.
- Do not proceed if cleaning removes governance lineage needed for audit.

### 7.9 Phase 8: Final Admission and Export Adapter

Purpose: produce train-ready outputs with separated decision, training-use, and queue-routing semantics.

Scope:

- Add `export_admitted_training_datasets.py` or a `llm_first` export adapter around existing export utilities.
- Normalize legacy fields into `final_export_decision`, `final_training_use_tag`, and `queue_routing`.
- Keep `sft_admission` only as a legacy compatibility mirror when required by downstream readers.

Deliverables:

- LLM-first export adapter.
- Final admission decision tests.
- Export schema tests.
- Queue routing tests.

Acceptance gate:

- `final_export_decision` contains only `accepted`, `review`, or `rejected`.
- `final_training_use_tag` contains only `main_sft`, `low_weight_sft`, `boundary_refusal_train`, `evaluation_only`, or `do_not_train`.
- `queue_routing` contains only `none`, `repair_queue`, `review_queue`, or `rejected_queue`.
- Queue values never appear in `final_export_decision` or `final_training_use_tag`.
- Accepted records have `species_isolation_status=passed`, `unsupported_high_risk_claim_count=0`, `unsafe_claim_count=0`, and complete raw/claim/evidence/final decision lineage.
- Records with `species_isolation_status=failed` are rejected or routed to repair, never admitted to training.

Blockers:

- Do not proceed if `sft_admission` still carries queue semantics in `llm_first` exports.
- Do not proceed if accepted outputs include unsupported high-risk, unsafe, or cross-species violations.

### 7.10 Phase 9: Smoke Runs and Per-Species Validation

Purpose: prove the new pipeline works at small scale before expanded runs.

Scope:

- Run 30-record `llm_first` smoke for each supported species.
- Run 30-record Wiki-first control.
- Validate schema, artifacts, species isolation, final answer cleaning, and export semantics.

Deliverables:

- Per-species smoke artifacts.
- Smoke governance report.
- Smoke artifact inventory.
- Smoke comparison summary.

Acceptance gate:

- 30-record `llm_first` smoke completes independently for each supported species.
- 30-record Wiki-first control still completes.
- No admitted sample contains forbidden cross-species terms.
- No admitted evidence anchor references another species Wiki root, runtime namespace, page path, rule card, fact ID, source ID, or drug constraint.
- High-risk samples are rejected or safely remediated before admission.
- Raw `llm_first` records pass through claim extraction and governance without Wiki-first skeleton fields.
- All new smoke artifacts pass filename validation.

Blockers:

- Do not proceed to expanded runs if any admitted record has species-isolation failure.
- Do not proceed if the Wiki-first control fails after `llm_first` additions.

### 7.11 Phase 10: Expanded Validation and Workflow Comparison

Purpose: validate scale, schema stability, and comparison behavior.

Scope:

- Run 500-record `llm_first` expanded validation.
- Run or reuse matched Wiki-grounded, no-Wiki, and metadata-only controls.
- Generate stable comparison CSV and detailed governance reports separately.

Deliverables:

- 500-record expanded artifacts.
- `workflow-comparison-standard-{run_date}-{run_label}.csv`.
- Workflow comparison summary/report.
- Species-isolation pass/fail metrics by species.
- Final acceptance report.

Acceptance gate:

- 500-record `llm_first` run completes without schema drift.
- Stable comparison CSV keeps exactly 54 fields.
- Detailed governance fields remain in JSONL/report artifacts, not in the comparison CSV.
- All admitted records have raw answer lineage, claim review lineage, evidence lineage, and final decision lineage.
- `cross_species_claim_count=0`, `cross_species_evidence_count=0`, and `cross_species_violation_count=0` for all admitted records.
- Every remediated admitted sample has a successful remediation re-evaluation record.
- Acceptance, repair, rejection, unsafe-claim, unsupported-high-risk, semantic-quality, naturalness, and traceability metrics are reported.

Blockers:

- Do not declare implementation complete if the 54-field comparison contract changes without a separate approved migration.
- Do not declare implementation complete if any admitted record violates species isolation, high-risk evidence support, export semantics, or lineage requirements.

## 8. Cross-Phase Acceptance Matrix

The implementation is acceptable only if all phase gates and the final matrix pass:

- Existing Wiki-first workflow remains runnable as a control through all phases.
- Every `llm_first` record binds to exactly one `species_profile_id`.
- Every admitted sample has `species_profile_id`, `species_key`, `species_runtime_namespace`, and `species_isolation_status=passed`.
- Every admitted evidence anchor belongs to the same `species_profile_id` and `species_runtime_namespace` as the sample.
- Cross-species evidence, rule-card, drug constraint, Wiki root, prompt lens, or terminology leakage never produces direct admission.
- `unsupported_high_risk_claim_count=0` for all admitted records.
- `unsafe_claim_count=0` for all admitted records.
- Final user-facing answers contain no internal evidence markers or serialized governance artifacts.
- New artifact names follow functional lowercase ASCII kebab-case.
- `final_export_decision`, `final_training_use_tag`, and `queue_routing` remain separate concepts in all new exports.
- Stable comparison CSV keeps exactly 54 fields unless a separate migration is approved.

## 9. Risk Controls by Phase

Phase 0 risk: baseline behavior becomes ambiguous.

Control: freeze control contracts and keep Wiki-first tests separate from `llm_first` tests.

Phase 1 risk: species configuration remains display-only.

Control: require runtime registry fields and fail closed on missing profile, missing runtime files, or cross-species runtime references.

Phase 2 risk: raw generation accidentally becomes Wiki-first again.

Control: prompt isolation rejects source IDs, fact IDs, rule IDs, page paths, evidence anchors, and forbidden species terms.

Phase 3 risk: claim extraction misses dangerous claims.

Control: combine LLM extraction with deterministic detectors for dosage, withdrawal, residue, regulatory execution, food safety, specific drugs, and public health.

Phase 4 risk: evidence retrieval crosses species boundaries.

Control: validate root, path, namespace, manifest membership, index source, and provenance; fail as isolation error rather than low confidence.

Phase 5 risk: governance admits unsupported high-risk content.

Control: high-risk support is mandatory; unsupported or contradicted high-risk claims route to repair or rejection.

Phase 6 risk: remediation introduces new unsupported claims.

Control: re-run extraction, retrieval, governance, and species-isolation validation after remediation.

Phase 7 risk: artifacts and schemas drift.

Control: enforce artifact writer, filename validator, schema validation report, and artifact inventory.

Phase 8 risk: export semantics mix admission, training use, and queues.

Control: export adapter writes `final_export_decision`, `final_training_use_tag`, and `queue_routing` independently.

Phase 9 and 10 risk: small tests pass but scale or comparison fails.

Control: require per-species smoke, Wiki-first control, 500-record expanded validation, and stable comparison CSV validation.

## 10. Final Execution Rule

This workflow must be delivered as a staged `llm_first` system running beside the existing Wiki-first control. A phase is complete only when its deliverables exist, its tests pass, and its acceptance gate is satisfied. The implementation is not complete until Phase 10 passes and the cross-phase acceptance matrix remains true.
