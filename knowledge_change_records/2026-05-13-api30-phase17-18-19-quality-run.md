# 2026-05-13 API 30 Phase17-18-19 质量运行记录

## 背景

本次任务是在 Phase17、Phase18、Phase19 完成后，使用真实 API 构建 30 条新数据，并通过完整 Wiki-first 质量链路统计结果：

```text
Phase13 skeleton
  -> Phase17 real-api two-stage generation
  -> Phase15 fact/hard-gate evaluation
  -> Phase18 dual judge and arbitration
  -> Phase19 layered training admission
```

## 执行过程

### 1. API 与输入检查

- 环境中存在 `NONELINEAR_API_KEY`，未打印密钥。
- 初次运行时 Phase14 自动选择了最近的 `pytest_e2e` 小批次 plan/skeleton，只生成 9 条。
- 发现 `wiki_answer_skeletons_20260513.jsonl` 曾被测试流程覆盖为 12 条 skeleton，而正式 plan 仍为 474 条。

处理方式：

- 使用正式 `wiki_sample_plan_20260513.jsonl` 重新生成独立 skeleton：
  - `exports/answer_skeletons/wiki_answer_skeletons_20260513_api30_source.jsonl`
  - skeleton 数量：474

### 2. Phase17 真实 API 生成

命令使用 `real-api` 模式、模型 `hunyuan-turbos-20250926`，限制 30 条。

输出：

- `exports/generated_samples/two_stage_samples_20260513_api30_phase17_full2.jsonl`

结果：

- 生成样本：30
- 生成模式：`real-api`
- 模型：`hunyuan-turbos-20250926`
- fallback 样本：0
- evidence anchor 保留：30/30
- 缺失 grounded citation：0

### 3. Phase15 事实与硬门禁评估

输出：

- `exports/evaluated_samples/fact_evaluated_samples_20260513_api30_phase17_full2.jsonl`

结果：

- 样本数：30
- accepted：26
- rejected：4
- Phase15 通过率：86.67%

拒绝原因：

- `hard_gate:executive_content_missing_a0_source`: 4
- `judge:deterministic_placeholder_failed`: 4

说明：

- 4 条被拒绝样本主要是高风险执行性内容缺少 A0/标签级来源。
- Phase15 硬门禁正常生效。

### 4. Phase18 双裁判与仲裁

输出：

- `exports/semantic_evaluated_samples/semantic_evaluated_samples_20260513_api30_phase17_full2.jsonl`

结果：

- 样本数：30
- 进入双裁判：26
- hard gate 跳过：4
- 需要仲裁：8
- fatal risk：4
- semantic accepted：4
- semantic review：18
- semantic rejected：8

仲裁触发：

- `high_risk_sample`: 8
- `label_disagreement`: 6
- `phase15_high_risk_class`: 8
- `phase15_high_risk_context`: 8
- `score_gap_ge_8`: 6

主要语义拒绝/复核原因：

- `semantic:structured_pass_false`: 20
- `judge_a:review`: 18
- `judge_b:review`: 20
- `arbiter:conservative_high_risk_merge`: 4
- `hard_gate:executive_content_missing_a0_source`: 4

说明：

- Phase18 明显比 Phase15 更严格。
- 大量样本进入 review，说明真实 API 输出虽然证据锚点完整，但临床表达、结构完整性或高风险边界表达仍需要优化。

### 5. Phase19 分层准入导出

输出：

- `exports/training_sets/training_set_manifest_20260513_api30_phase17_full2.json`
- `exports/training_sets/training_set_review_queue.jsonl`
- `exports/training_sets/training_set_rejected_queue.jsonl`

结果：

- accepted：4
- review：18
- rejected：8

分层导出：

- `sft_l1_retrieval_grounded.jsonl`: 4
- `sft_l2_diagnosis_support.jsonl`: 0
- `sft_l3_differential_support.jsonl`: 0
- `sft_l4_control_boundary.jsonl`: 0
- `sft_l5_drug_boundary_negative.jsonl`: 0
- `eval_l6_regulatory_guardrail.jsonl`: 1
- `eval_l7_judge_calibration.jsonl`: 30
- `training_set_review_queue.jsonl`: 18
- `training_set_rejected_queue.jsonl`: 8

## 能力层统计

- L1 retrieval grounded
  - generated: 8
  - Phase15 accepted: 6
  - semantic accepted/review/rejected: 4/2/2
- L2 diagnosis support
  - generated: 7
  - Phase15 accepted: 7
  - semantic accepted/review/rejected: 0/6/1
- L3 differential support
  - generated: 7
  - Phase15 accepted: 7
  - semantic accepted/review/rejected: 0/6/1
- L4 control boundary
  - generated: 7
  - Phase15 accepted: 6
  - semantic accepted/review/rejected: 0/4/3
- L6 regulatory guardrail
  - generated: 1
  - Phase15 accepted: 0
  - semantic accepted/review/rejected: 0/0/1

## 质量判断

当前新链路有效：

- 真实 API 生成可运行。
- 30 条样本全部保留证据锚点。
- Phase15 能拦截缺少 A0/标签来源的高风险样本。
- Phase18 能进一步将临床语义和边界表达不足的样本分流到 review/rejected。
- Phase19 能只把双通过样本导入 SFT，并保留 review/rejected 队列。

但当前批次还不适合直接扩大作为正式 SFT 主数据：

- Phase18 最终 accepted 仅 4/30，接受率 13.33%。
- L2/L3/L4 的样本多进入 review，说明真实生成提示词对诊断支持、鉴别诊断、控制边界的结构化表达约束还不够。
- `semantic:structured_pass_false` 过高，说明 Phase18 的结构准入标准与 Phase14 真实输出之间还需要进一步对齐。

## 输出报告

- JSON 汇总：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_first_generation_reports\api30_phase17_18_19_quality_summary_20260513_api30_phase17_full2.json`
- Markdown 汇总：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_first_generation_reports\api30_phase17_18_19_quality_summary_20260513_api30_phase17_full2.md`
- CSV 明细：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_first_generation_reports\api30_phase17_18_19_samples_20260513_api30_phase17_full2.csv`

## 后续建议

1. 优先分析 18 条 review 样本，确认是 Phase14 输出结构不足，还是 Phase18 规则过严。
2. 优化 Phase14 stage2 prompt，明确要求输出结构性段落，例如：
   - 事实依据
   - 可回答边界
   - 不可扩展内容
   - 证据锚点
3. 对 L2/L3/L4 增加更明确的回答模板或 skeleton claim 分组。
4. 对 L6/L5 高风险样本单独构建边界型 prompt，不与普通正向样本混跑。
5. 下一轮建议跑 30 条“按层均衡抽样”，避免前 30 条主要集中在 L1-L4。

