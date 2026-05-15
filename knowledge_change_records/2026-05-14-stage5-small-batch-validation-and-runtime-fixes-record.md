# 2026-05-14 阶段五小批次验证与运行时修复记录

## 一、任务目标

根据 `2026-05-14-swine-consultation-pipeline-quality-staged-remediation-plan.md` 的阶段五要求，重新执行 10 条小批次验证：

- `parallel=8`
- `limit=10`
- `sampling-mode=coverage`
- 验收指标：`fallback <= 1`、`audit leak = 0`、`unique entity >= 8`、`repairable_main_sft_count = 0`、`main_issues_char_split_count = 0`、`zero_score_non_invalid_count = 0`

## 二、执行前发现的问题

第一次阶段五小批次使用 `20260514_stage5_small10` 跑通了技术链路，但没有达到质量验证目标：

- Phase12 选中了 `CMP-001` 到 `CMP-010` 比较页。
- 10 条均为 `L7_judge_calibration`、`eval_only`、`toc_only`。
- Phase15 全部拒绝，原因集中在 `answer_missing_fact_citation`、`sample_source_trust_not_authoritative`、`deterministic_placeholder_failed`。

这说明链路不是 API 或 Phase14 fallback 失败，而是 Phase12 coverage 抽样没有优先选择真实问诊生成可用的疾病页。

## 三、本次代码修改

### 3.1 Phase12 coverage 抽样优先级修复

修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase12_plan_samples_from_wiki.py`

修改内容：

- 新增 `coverage_plan_rank()`，在 coverage 模式下优先选择：
  - `entity_type=disease`
  - `wiki/diseases/` 路径
  - `source_trust=authoritative`
  - 非 `eval_only`
  - 非 `L7_judge_calibration`
- 修改 coverage 选择逻辑，先每个实体取 1 条，再按 `max_plans_per_entity` 补第二条，避免 10 条样本只覆盖 5 个实体。

解决的问题：

- 避免小批次被 CMP/审计页占满。
- 避免同一疾病因多个能力层重复占用样本额度。
- 让小批次验证真正覆盖疾病问诊生成，而不是评测校准样本。

### 3.2 gold readiness 索引补充证据深度字段

修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/wiki_ops/phase6_7_review_status_and_gold_dataset.py`

修改内容：

- 从 `issues/wiki_native_graph_build_report.json` 的 `page_gold_readiness` 读取：
  - `page_gold_ready`
  - `evidence_units`
- 写入：
  - `exports/gold_dataset_readiness_index.csv`
  - `exports/drug_gold_role_index.csv`

解决的问题：

- wiki 页已有事实锚点，但 Phase12 读取不到 `evidence_units/page_gold_ready`，导致所有候选都被判为 `toc_only`。
- 修复后 Phase12 能正确识别 `substantive` 页面。

### 3.3 Phase18 运行时缺陷修复

修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`

修改内容：

- 新增 `first_nonempty()`，修复 `merge_semantic_result()` 中未定义函数导致 Phase18 并发执行中断的问题。
- 修复 `arbitrate()` 中误引用不存在变量 `arbiter` 的问题。
- 更新 Phase18 self-test 的安全高风险样本，使其不再在主回答中包含 `source=/rule=/page=` 审计标记，与阶段四/五的审计泄漏约束保持一致。

解决的问题：

- Phase18 真实执行不再因 `NameError` 中断。
- self-test 与当前“主回答不得泄漏审计字段”的质量约束一致。

## 四、实际执行批次

最终有效批次：

`20260514_stage5_small10_fix3`

主要输出：

- Phase12 plan：`exports/planned_samples/wiki_sample_plan_20260514_stage5_small10_fix3.jsonl`
- Phase13 skeleton：`exports/answer_skeletons/wiki_answer_skeletons_20260514_stage5_small10_fix3.jsonl`
- Phase14 generated：`exports/generated_samples/two_stage_samples_20260514_stage5_small10_fix3.jsonl`
- Phase14b naturalized：`exports/generated_samples/naturalized_samples_20260514_stage5_small10_fix3.jsonl`
- Phase15 evaluated：`exports/evaluated_samples/fact_evaluated_samples_20260514_stage5_small10_fix3.jsonl`
- Phase18 semantic：`exports/semantic_evaluated_samples/semantic_evaluated_samples_20260514_stage5_small10_fix3.jsonl`
- Phase16 CSV：`exports/training_sets/swine_wiki_training_dataset_production_20260514_stage5_small10_fix3.csv`

## 五、阶段结果

| 阶段 | 结果 |
|---|---:|
| Phase12 planned | 10 |
| Phase12 unique entities | 10 |
| Phase12 unique pages | 10 |
| Phase12 substantive ratio | 1.0 |
| Phase12 toc_only ratio | 0.0 |
| Phase13 skeletons | 10 |
| Phase14 generated | 10 |
| Phase14 fallback | 0 |
| Phase14 API attempts | 1次: 7条；2次: 1条；3次: 2条 |
| Phase14b audit leak | 0 |
| Phase15 accepted | 8 |
| Phase15 rejected | 2 |
| Phase18 dual judged | 8 |
| Phase18 semantic review | 8 |
| Phase18 semantic rejected | 2 |
| Phase16 accepted | 0 |
| Phase16 review | 8 |
| Phase16 rejected | 2 |

## 六、阶段五验收

| 验收项 | 阈值 | 实测 | 结论 |
|---|---:|---:|---|
| fallback | <= 1 | 0 | 通过 |
| audit leak | 0 | 0 | 通过 |
| unique entity | >= 8 | 10 | 通过 |
| repairable_main_sft_count | 0 | 0 | 通过 |
| main_issues_char_split_count | 0 | 0 | 通过 |
| zero_score_non_invalid_count | 0 | 0 | 通过 |

## 七、耗时与瓶颈

| 阶段 | 约耗时 |
|---|---:|
| Phase12 fix3 | 约 1 秒 |
| Phase13 | 约 1 秒 |
| Phase14 | 约 40 秒 |
| Phase14b | 约 1 秒 |
| Phase15 | 约 1 秒 |
| Phase18 最终成功执行 | 约 113 秒 |
| Phase16 | 约 1 秒 |

主要瓶颈：

- Phase18 双裁判/仲裁耗时最高。
- Phase14 有 3 条发生重试，但 fallback 为 0，说明 keypool/重试机制有效。
- Phase15 对高风险/监管类样本仍较严格，导致 2 条直接拒绝。

## 八、剩余风险与后续建议

本次阶段五小批次验收通过，但有两个需要继续关注的问题：

1. Phase16 train-ready 为 0。原因是 Phase18 对 8 条通过 Phase15 的样本全部判为 `repairable/review`，说明当前裁判准入较保守，适合作为安全验证结果，但还不能证明已产出可直接主训练的高质量样本。
2. 部分 wiki 页面内容在控制台显示为乱码，虽然本次链路可以运行，但后续若要提升主训练样本质量，应继续治理 wiki 正文编码和事实锚点质量。

建议下一步不要直接扩大 40 条，而是先抽查 `review_queue` 中 8 条样本的具体问题，判断是生成回答确实不足，还是 Phase18 评分/仲裁过严；然后再执行 40 条正式验证。
