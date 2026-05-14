# API 30 Phase17-18-19 Quality Summary

- Batch: `20260513_api30_phase17_full2`
- Generated samples: 30
- Anchor preserved: 30/30 (100.00%)
- Phase15 accepted/rejected: 26/4 (86.67% accepted)
- Phase18 accepted/review/rejected: 4/18/8
- Phase16 accepted/review/rejected: 4/18/8

## Ability Layers

- L1_retrieval_grounded: generated 8, P15 accepted 6, semantic accepted/review/rejected 4/2/2
- L2_diagnosis_support: generated 7, P15 accepted 7, semantic accepted/review/rejected 0/6/1
- L3_differential_support: generated 7, P15 accepted 7, semantic accepted/review/rejected 0/6/1
- L4_control_boundary: generated 7, P15 accepted 6, semantic accepted/review/rejected 0/4/3
- L6_regulatory_guardrail: generated 1, P15 accepted 0, semantic accepted/review/rejected 0/0/1

## Reject Reasons

- Phase15: `{'hard_gate:executive_content_missing_a0_source': 4, 'judge:deterministic_placeholder_failed': 4}`
- Phase18: `{'arbiter:high_risk_sample': 8, 'arbiter:label_disagreement': 6, 'arbiter:phase15_high_risk_class': 8, 'arbiter:phase15_high_risk_context': 8, 'arbiter:score_gap_ge_8': 6, 'judge_a:review': 18, 'arbiter:conservative_high_risk_merge': 4, 'judge_a:reject': 4, 'judge_b:review': 20, 'semantic:structured_pass_false': 20, 'hard_gate:executive_content_missing_a0_source': 4}`

## Outputs

- generated: `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\generated_samples\two_stage_samples_20260513_api30_phase17_full2.jsonl`
- phase15: `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\evaluated_samples\fact_evaluated_samples_20260513_api30_phase17_full2.jsonl`
- phase18: `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\semantic_evaluated_samples\semantic_evaluated_samples_20260513_api30_phase17_full2.jsonl`
- manifest: `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\training_sets\training_set_manifest_20260513_api30_phase17_full2.json`
- summary_json: `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_first_generation_reports\api30_phase17_18_19_quality_summary_20260513_api30_phase17_full2.json`
- sample_csv: `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_first_generation_reports\api30_phase17_18_19_samples_20260513_api30_phase17_full2.csv`
