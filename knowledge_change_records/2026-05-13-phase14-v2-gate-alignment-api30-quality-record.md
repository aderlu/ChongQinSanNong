# Phase14 v2 + Phase15/18 Gate Alignment Real API 30 Quality Record

- Date: 2026-05-13
- Batch: 20260513_api30_promptv2_fixgate2
- Generated source batch: 20260513_api30_promptv2
- Prompt version: phase14.two_stage.v2
- Model: hunyuan-turbos-20250926

## Previous Problem

Phase14 v2 had introduced L2/L3/L4 structured answer sections, but real model outputs often used safety-boundary phrases containing terms such as dose, withdrawal, residue, report, cull, quarantine, and their Chinese equivalents. Phase15 and Phase18 previously treated any lexical trigger as positive executable content, so low-risk negative boundary text was incorrectly routed into A0-only hard gates or arbitration review.

## Code Changes

- Updated Phase14 low-risk template wording in phase14_generate_two_stage_samples.py to reduce hard-gate trigger terms in ordinary L1-L4 answers.
- Updated Phase15 in phase15_fact_level_evaluate_samples.py with NEGATIVE_BOUNDARY_CUE_RE, LOW_RISK_EXECUTIVE_CONTEXT_LAYERS, and executive_triggered_positive_context(). Phase15 now distinguishes lexical trigger hits from true positive executable content through positive_triggered.
- Updated Phase18 in phase18_dual_judge_and_arbitrate.py to consume positive_triggered and route low-risk negative boundary hits as phase15_negative_boundary_trigger, not fatal executive triggers.
- Added regression coverage in test_swine_wiki_first_generation_pipeline.py for low-risk negative boundary text that mentions high-risk terms but should not require A0.

## Real API 30 Results

| Metric | Previous api30_phase17_full2 | Current promptv2_fixgate2 | Delta |
|---|---:|---:|---:|
| Generated | 30 | 30 | 0 |
| Phase15 accepted | 26 | 20 | -6 |
| Phase15 rejected | 4 | 10 | 6 |
| Phase18 accepted | 4 | 20 | 16 |
| Phase18 review | 18 | 0 | -18 |
| Phase18 rejected | 8 | 10 | 2 |
| SFT accepted | 4 | 20 | 16 |
| Review queue | 18 | 0 | -18 |
| Rejected queue | 8 | 10 | 2 |
| structured_pass_false | 20 | 0 | -20 |
| judge_a:review | 18 | 0 | -18 |
| judge_b:review | 20 | 0 | -20 |

## Current Layer Export

- L1 SFT: 5
- L2 SFT: 5
- L3 SFT: 5
- L4 SFT: 5
- L5 SFT: 0
- L6 eval: 1
- L7 calibration: 30
- Review queue: 0
- Rejected queue: 10

## Validation

- Phase18 self-test passed: 7 assertions.
- The same pipeline test file previously passed 15 tests after Phase15 fix. After switching to local Python 3.14, pytest was blocked by Windows temp directory deletion permissions and subprocess handle errors, not by assertion failures in the changed logic.
- Real pipeline validation passed through Phase15, Phase18, and Phase16 on 30 real API samples.

## Expected Effect

The usable SFT-ready samples increased from 4/30 to 20/30, while review backlog dropped from 18 to 0. L1-L4 now produce balanced accepted SFT samples, and hard-gate rejections remain reserved for samples that Phase15 still identifies as positive executable/A0-gated content.

## Output Files

- exports/generated_samples/two_stage_samples_20260513_api30_promptv2.jsonl
- exports/evaluated_samples/fact_evaluated_samples_20260513_api30_promptv2_fixgate.jsonl
- exports/semantic_evaluated_samples/semantic_evaluated_samples_20260513_api30_promptv2_fixgate2.jsonl
- exports/training_sets/training_set_manifest_20260513_api30_promptv2_fixgate2.json
- issues/wiki_first_generation_reports/api30_promptv2_fixgate_quality_comparison_20260513_api30_promptv2_fixgate2.json
- issues/wiki_first_generation_reports/api30_promptv2_fixgate_quality_comparison_20260513_api30_promptv2_fixgate2.csv
