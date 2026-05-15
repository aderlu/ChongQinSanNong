# 2026-05-14 阶段五 40 条正式批次执行与验收记录

## 一、执行背景

在阶段五小批次 `20260514_stage5_small10_fix3` 抽查后，发现 8 条 review 的主因不是生成质量整体不足，而是 Phase18 对 LLM 裁判/仲裁输出结构的归一化不足。

已完成修复：

- 支持中文/别名维度名读取。
- 支持从 `scores/dimensions/顶层字段` 提取分数。
- 缺少总分时用维度分本地重算。
- 缺少 `structured_pass` 时，在无 hard fail 且有有效分数的情况下推断通过。
- 仲裁无硬伤但缺分时，回退到双裁判保守分，避免误判为 0 分。

修复后小批次复判 `20260514_stage5_small10_fix3_rejudge2`：

- accepted: 8
- review: 0
- rejected: 2

因此继续执行 40 条正式批次。

## 二、正式批次信息

批次号：

`20260514_stage5_formal40_v1`

执行参数：

- `limit=40`
- `parallel=8`
- `sampling-mode=coverage`
- `max-plans-per-entity=2`
- `prefer-depth=substantive,thin,toc_only`

## 三、阶段执行结果

### Phase12 规划

输出：

- `exports/planned_samples/wiki_sample_plan_20260514_stage5_formal40_v1.jsonl`

结果：

- planned: 40
- unique entities: 40
- unique pages: 40
- max samples per entity: 1
- substantive ratio: 1.0
- toc_only ratio: 0.0
- training_intent: positive_sft 40

说明：

Phase12 已有效解决历史上样本集中于前几个疾病、CMP 页、toc_only 页的问题。

### Phase13 skeleton

输出：

- `exports/answer_skeletons/wiki_answer_skeletons_20260514_stage5_formal40_v1.jsonl`

结果：

- skeletons: 40
- gaps: 0

### Phase14 真实生成

输出：

- `exports/generated_samples/two_stage_samples_20260514_stage5_formal40_v1.jsonl`

结果：

- generated: 40
- fallback: 1
- missing anchors: 0
- missing grounded citations: 0
- API attempts:
  - 1 次成功：26
  - 2 次成功：7
  - 4 次成功：5
  - 5 次成功：1

说明：

API 调用存在明显重试，但 fallback 仅 1 条，说明 keypool/重试机制在正式批次中有效。

### Phase14b 主回答清理

输出：

- `exports/generated_samples/naturalized_samples_20260514_stage5_formal40_v1.jsonl`

结果：

- samples: 40
- rewritten: 0
- clinical_answer_audit_artifact_samples: 0

说明：

主回答未发现 `source=/fact=/page=/rule=` 等审计字段泄漏。

### Phase15 事实与硬门控

输出：

- `exports/evaluated_samples/fact_evaluated_samples_20260514_stage5_formal40_v1.jsonl`

结果：

- accepted: 30
- rejected: 10

拒绝原因：

- `hard_gate:executive_content_missing_a0_source`: 10
- `judge:deterministic_placeholder_failed`: 10

说明：

拒绝主要集中在高风险/监管或执行性内容缺少 A0 级支撑，属于安全门控结果，不建议直接放宽。

### Phase18 双裁判与仲裁

输出：

- `exports/semantic_evaluated_samples/semantic_evaluated_samples_20260514_stage5_formal40_v1.jsonl`

结果：

- dual judged: 30
- needed arbitration: 11
- semantic accepted: 26
- semantic review: 3
- semantic rejected: 11
- fatal risk count: 10

仲裁触发主要原因：

- `score_gap_ge_15`: 7
- `label_disagreement`: 6
- `phase15_negative_boundary_trigger`: 6
- `critical_dimension_gap_ge_2`: 5
- `synthetic_context_misuse`: 4
- `hard_fail_flag`: 3
- `high_risk_sample`: 3

说明：

Phase18 不再出现大规模 0 分误伤。剩余 review/rejected 主要来自真实分歧、高风险样本和合成语境使用风险。

### Phase16 导出

输出：

- `exports/training_sets/swine_wiki_training_dataset_production_20260514_stage5_formal40_v1.csv`
- `exports/training_sets/swine_wiki_training_dataset_production_train_ready_20260514_stage5_formal40_v1.csv`
- `exports/training_sets/swine_wiki_training_main_20260514_stage5_formal40_v1.csv`
- `exports/training_sets/swine_wiki_training_main_train_ready_20260514_stage5_formal40_v1.csv`
- `exports/training_sets/training_set_manifest_20260514_stage5_formal40_v1.json`

结果：

- accepted: 26
- review: 3
- rejected: 11
- `sft_l1_retrieval_grounded.jsonl`: 26
- `sft_l1_l4_borderline.jsonl`: 26
- `training_set_review_queue.jsonl`: 3
- `training_set_repair_queue.jsonl`: 3
- `training_set_rejected_queue.jsonl`: 11
- `training_set_low_weight_sft.jsonl`: 1

## 四、验收指标

| 指标 | 目标 | 实测 | 结论 |
|---|---:|---:|---|
| fallback | <= 2 | 1 | 通过 |
| unique entity | >= 30 | 40 | 通过 |
| single entity count | <= 2 | 1 | 通过 |
| substantive ratio | >= 60% | 100% | 通过 |
| toc_only ratio | <= 10% | 0% | 通过 |
| train-ready / accepted | >= 25 | 26 | 通过 |
| invalid / rejected | >= 10 | 11 | 通过 |
| repairable_main_sft_count | 0 | 0 | 通过 |
| main_issues_char_split_count | 0 | 0 | 通过 |
| zero_score_non_invalid_count | 0 | 0 | 通过 |
| audit leak | 0 | 0 | 通过 |

## 五、耗时与瓶颈

| 阶段 | 约耗时 |
|---|---:|
| Phase12 | 约 1 秒 |
| Phase13 | 约 1 秒 |
| Phase14 | 约 151 秒 |
| Phase14b | 约 1 秒 |
| Phase15 | 约 1 秒 |
| Phase18 | 约 171 秒 |
| Phase16 | 约 1 秒 |

主要瓶颈：

1. Phase18 双裁判/仲裁最耗时。
2. Phase14 真实 API 生成次之，且存在多次重试。
3. Phase12/13/14b/15/16 本地阶段耗时很低。

## 六、结论

阶段五目标已完整实现：

- 先完成 8 条 review 样本抽查。
- 确认主要问题来自 Phase18 结构归一化，而不是生成质量整体不足。
- 修复 Phase18 后，小批次复判通过。
- 继续执行 40 条正式批次，最终产出 26 条 accepted/train-ready、3 条 review、11 条 rejected。

当前产线已经具备继续扩大批量验证的基础，但后续仍建议持续监控：

- Phase15 高风险硬门控拒绝比例。
- Phase18 仲裁触发比例。
- Synthetic context misuse 触发样本。
- API 重试次数与 fallback 样本。
