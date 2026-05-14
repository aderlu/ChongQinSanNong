# 2026-05-13 Wiki-first 目标核查与真实 API 30 条质量分析

## 目标核查结论

当前 Phase 12-16 已达到 Wiki-first MVP 目标：

- Phase 12：从 runtime manifest 与 Wiki 索引规划样本，不随机生成。
- Phase 13：用结构化事实、规则卡和来源形成标准答案骨架。
- Phase 14：支持两段式生成；默认 deterministic dry-run，新增真实 API 30 条试跑脚本。
- Phase 15：评估不只依赖 judge，包含结构检查、事实锚点检查、硬门禁和确定性 judge 占位。
- Phase 16：训练集按 L1-L7 分层导出。
- 高风险内容：药物边界、监管/处置类样本经过硬门禁。
- L5 修复后：药物边界 SFT 只包含通过评估的 accepted 拒答样本。

正式训练集未被真实 API 试跑覆盖，仍保持：

- `sft_l1_retrieval_grounded.jsonl`：40
- `sft_l2_diagnosis_support.jsonl`：39
- `sft_l3_differential_support.jsonl`：39
- `sft_l4_control_boundary.jsonl`：39
- `sft_l5_drug_boundary_negative.jsonl`：71
- `eval_l6_regulatory_guardrail.jsonl`：31
- `eval_l7_judge_calibration.jsonl`：289

## 真实 API 试跑

- API：Nonelinear OpenAI-compatible API
- 模型：`hunyuan-turbos-20250926`
- 样本数：30
- 生成文件：`knowledge/llm_wiki_swine_authoritative/exports/generated_samples/real_api_samples_20260513_30.jsonl`
- 评估文件：`knowledge/llm_wiki_swine_authoritative/exports/evaluated_samples/fact_evaluated_samples_20260513_realapi30.jsonl`
- 质量分析 JSON：`knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/real_api_30_quality_analysis_20260513.json`

初始候选中有 3 个 skeleton 缺少 Phase 14 可用锚点，被跳过并用候补样本补足 30 条：

- `PLAN-DIS-001-0001`
- `PLAN-DIS-003-0001`
- `PLAN-DIS-005-0001`

## 真实 API 30 条质量结果

- generated：30
- evaluated：30
- accepted：22
- rejected：8
- accept rate：73.3%
- anchor preserved：28/30
- anchor preserved rate：93.3%

分层结果：

- L1 retrieval：2/2 accepted
- L2 diagnosis：5/5 accepted
- L3 differential：5/5 accepted
- L4 control：5/5 accepted
- L5 drug boundary：5/5 accepted
- L6 regulatory guardrail：0/4 accepted，4/4 rejected
- L7 judge calibration：0/4 accepted，4/4 rejected

拒绝原因：

- `hard_gate:executive_content_missing_a0_source`：4
- `fact:sample_source_trust_not_authoritative`：4
- `fact:answer_missing_fact_citation`：4
- `judge:deterministic_placeholder_failed`：8

## 质量判断

整体质量可用，但不适合直接全量进入训练集：

- L1-L5 表现稳定，尤其 L5 药物边界 5 条全部通过，说明真实 API 能遵守拒答/边界模板。
- L6 被全部拒绝是预期中的保守结果：样本涉及监管/处置边界，但缺少 A0 权威来源支撑，因此硬门禁拒绝。
- L7 被拒绝主要是校准/审计类规则卡边界样本，含 `source_trust` 或 fact citation 缺口，适合保留作 judge calibration，不应进入 SFT。
- 2 条样本存在锚点保留不完整，需要在真实 API prompt 中进一步强制“逐字保留 citation bracket”。

## 后续修正建议

- 将真实 API 生成脚本继续保留为独立试跑入口，避免覆盖正式 deterministic 产物。
- 若要扩大真实 API 生成，应先改进 prompt：
  - 明确禁止改写 citation bracket。
  - 要求输出前自检每个 `source/rule/fact/page` 是否逐字出现。
  - 对 L6 明确要求“不形成监管执行结论，只做边界拒答”，并优先选择 A0 锚点样本。
- Phase 15 可继续升级为真实 LLM judge，但不能替代 fact/hard gate。

## 验证

- `python -m pytest tests/test_swine_wiki_first_generation_pipeline.py -q`
  - 14 passed
- `python -m pytest tests/test_swine_llm_wiki_runtime.py -q`
  - 12 passed
- 状态词扫描无命中。
- pytest 临时产物无残留。
