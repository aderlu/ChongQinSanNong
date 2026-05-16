# 2026-05-15 三组真实 LLM 全链路 30 条并行运行记录

## 运行目标

按用户要求，使用三个子智能体分别运行三个实验组：

- A 组：Wiki-grounded
- B 组：no_wiki
- C 组：metadata_only

每组要求：

- 30 条数据
- 组内 `parallel=3`
- 必须调用真实 LLM
- 必须完成完整链路
- 最终生成 54 字段 CSV

运行 ID：

- `20260515_real_llm_3groups30_parallel3_v1`

## 基准保持

本次运行未改变 `2026-05-14-wiki-grounded-baseline-validation-design.md` 的对比口径。

最终对比字段仍为：

- 3 个比较键：`run_id`、`case_seed_id`、`baseline_group`
- 51 个样本与评估字段
- 合计 54 字段

最终标准总表检查：

- 行数：90
- 字段数：54
- 结果：通过

## 子智能体分工

### Wiki 组

子智能体：

- `019e29d2-5556-7093-90e4-13d3108c1b20`

执行链路：

```text
Phase12 plan
-> Phase13 skeleton
-> Phase14 real-api grounded generation
-> Phase14b naturalization
-> Phase15 fact/hard gate
-> Phase18 dual judge/arbitration
-> Phase16 export
-> baseline general judge real-api
-> grounding audit
```

说明：

- 初次运行时因缺少同 run id 的 `planned_samples` 和 `answer_skeletons` 上游文件失败。
- 随后补跑 `prepare`，生成 plan/skeleton，并通过 `wiki_anchorable_preflight`。
- 重新运行 Wiki 组后完整成功。

最终行数：

- `wiki_group`: 30
- `wiki_judged`: 30
- `wiki_grounding`: 30

真实 LLM 调用：

- 确认使用 `--mode real-api`
- Phase14 和 baseline general judge 均调用真实 LLM

### no_wiki 组

子智能体：

- `019e29cf-9496-73b2-b566-9d48dd19767c`

执行链路：

```text
baseline no_wiki generation real-api
-> baseline general judge real-api
-> grounding audit
```

最终行数：

- `no_wiki_group`: 30
- `no_wiki_judged`: 30
- `no_wiki_grounding`: 30

真实 LLM 调用：

- 确认使用 `--mode real-api`

### metadata_only 组

子智能体：

- `019e29cf-95a0-7033-8660-7bc37e8579ef`

执行链路：

```text
baseline metadata_only generation real-api
-> baseline general judge real-api
-> grounding audit
```

最终行数：

- `metadata_only_group`: 30
- `metadata_only_judged`: 30
- `metadata_only_grounding`: 30

真实 LLM 调用：

- 确认使用 `--mode real-api`

## 最终 CSV 产物

标准 90 行总表：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_standard_20260515_real_llm_3groups30_parallel3_v1.csv`

三组 54 字段 CSV：

- Wiki：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_wiki_20260515_real_llm_3groups30_parallel3_v1.csv`
- no_wiki：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_no_wiki_20260515_real_llm_3groups30_parallel3_v1.csv`
- metadata_only：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_metadata_only_20260515_real_llm_3groups30_parallel3_v1.csv`

## 对比报告结果

报告文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\reports\baseline_validation_report_20260515_real_llm_3groups30_parallel3_v1.json`

结果：

- `passed`: true
- `rows`: 90
- `comparison_fields_count`: 54
- `standard_fields_count`: 51
- `all_rows_have_standard_fields`: true
- `unique_case_group_rows`: true

通用质量均分：

- Wiki：92.57
- no_wiki：89.53
- metadata_only：89.50

训练可用率：

- Wiki：1.0
- no_wiki：1.0
- metadata_only：1.0

unsafe/hallucination 率：

- Wiki：0.0
- no_wiki：0.0
- metadata_only：0.0

证据锚点：

- Wiki：平均 2.47 个
- no_wiki：0
- metadata_only：0

## QA Gate 结果

### Wiki

报告：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\reports\qa_realism_gate_wiki_20260515_real_llm_3groups30_parallel3_v1.json`

结果：

- `passed`: true
- `rows`: 30
- `query_hard_fail_rate`: 0.0%
- `professional_leakage_rate_user_query`: 0.0%
- `answer_hard_fail_rate`: 3.33%
- `clinical_judgement_rate`: 100.0%
- `differential_rate`: 100.0%
- `field_action_rate`: 100.0%

说明：

- 唯一失败项为 `CASE-SEED-000025`。
- 失败原因是 QA gate 标记 `fabricated_test_or_necropsy_result`。
- 人工复核文本后，回答实际是在说“目前没有明确的病原检测结果”“不能作为确诊”，属于安全边界提示，并未伪造阳性结果、剖检所见或已确诊结论。
- 因此该项更接近 gate 边缘误报，不影响本轮整体通过。

### no_wiki

报告：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\reports\qa_realism_gate_no_wiki_20260515_real_llm_3groups30_parallel3_v1.json`

结果：

- `passed`: true
- `rows`: 30
- `query_hard_fail_rate`: 0.0%
- `professional_leakage_rate_user_query`: 0.0%
- `answer_hard_fail_rate`: 0.0%
- `clinical_judgement_rate`: 100.0%
- `differential_rate`: 100.0%
- `field_action_rate`: 100.0%

### metadata_only

报告：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\reports\qa_realism_gate_metadata_only_20260515_real_llm_3groups30_parallel3_v1.json`

结果：

- `passed`: true
- `rows`: 30
- `query_hard_fail_rate`: 0.0%
- `professional_leakage_rate_user_query`: 0.0%
- `answer_hard_fail_rate`: 0.0%
- `clinical_judgement_rate`: 100.0%
- `differential_rate`: 100.0%
- `field_action_rate`: 100.0%

## 注意事项

1. 本次是 30 条 smoke，不覆盖全部 73 个猪病疾病条目，因此 `coverage` 在 prepare 阶段提示失败是预期行为，不代表三组 30 条链路失败。
2. 初次 Wiki 子智能体运行失败的原因是缺少同 run id 的 plan/skeleton 上游文件；已通过补跑 prepare 修复，并重新完成 Wiki 全链路。
3. 本次没有改动对比字段、分组定义和 baseline 证据边界。

## 结论

三组均已完成真实 LLM 全链路运行，每组 30 条，组内三路并行。最终总表为 90 行、54 字段，三份组内 CSV 均为 30 行、54 字段。QA gate 三组均通过，可作为后续 500 条正式运行前的稳定验证记录。
