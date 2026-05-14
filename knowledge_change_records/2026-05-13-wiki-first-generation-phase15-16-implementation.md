# 2026-05-13 Wiki-first 数据生成 Phase 15-16 实施记录

## 范围

- Phase 15：基于结构化事实、证据锚点、硬门禁和确定性 judge 占位规则评估两段式生成样本。
- Phase 16：按能力层导出可训练/可评估数据集，并生成 manifest 与报告。
- 集成验证：重新执行 Phase 12 到 Phase 16 正式链路，确认输出未被测试 smoke 数据覆盖。

## 代码变更

- `knowledge/llm_wiki_swine_authoritative/tools/phase15_fact_level_evaluate_samples.py`
  - 新增事实级评估脚本。
  - 输出评估 JSONL、JSON/MD 报告和 reject reason CSV。
  - 每条样本执行结构检查、事实锚点检查、硬门禁检查和确定性 judge 占位检查。
- `knowledge/llm_wiki_swine_authoritative/tools/phase16_export_layered_training_sets.py`
  - 新增训练集分层导出脚本。
  - L1-L4 仅导出 `accepted` 且 fact/hard gate 均通过的正向 SFT 样本。
  - L5 保留被拒绝的药物边界负样本；本次正式输入批次暂无可导出样本。
  - L6 导出监管/高风险硬门禁评估样本。
  - L7 保留全量样本，用于 judge calibration。
  - manifest 同时记录层名 key 与文件名 key 的 `layer_counts`，便于脚本和测试消费。
- `knowledge/llm_wiki_swine_authoritative/tools/phase12_plan_samples_from_wiki.py`
  - 将输出路径字段改为 `outputs.planned_samples_file`。
  - 新增顶层数值字段 `planned_samples`，表示计划样本数量。
- `knowledge/llm_wiki_swine_authoritative/tools/phase14_generate_two_stage_samples.py`
  - 新增 `samples_generated` 兼容字段。
- `tests/test_swine_wiki_first_generation_pipeline.py`
  - 扩展 Phase 15、Phase 16 和 Phase 12-16 端到端 smoke 测试。
  - 明确 L5 负样本、L6 高风险样本和 L7 全量校准集的导出契约。

## 正式链路输出

执行日期：`20260513`

- Phase 12 planned samples：474
- Phase 13 answer skeletons：474
- Phase 14 two-stage generated samples：179
- Phase 15 evaluated samples：179
  - accepted：159
  - rejected：20
  - reject reasons：
    - `hard_gate:executive_content_missing_a0_source`：20
    - `judge:deterministic_placeholder_failed`：20
- Phase 16 layered training/eval sets：
  - `sft_l1_retrieval_grounded.jsonl`：40
  - `sft_l2_diagnosis_support.jsonl`：39
  - `sft_l3_differential_support.jsonl`：39
  - `sft_l4_control_boundary.jsonl`：39
  - `sft_l5_drug_boundary_negative.jsonl`：0
  - `eval_l6_regulatory_guardrail.jsonl`：10
  - `eval_l7_judge_calibration.jsonl`：179

## 验证

- `python -m pytest tests/test_swine_wiki_first_generation_pipeline.py -q`
  - 结果：13 passed
  - 备注：Windows pytest 临时目录清理阶段出现非致命 `PermissionError`，测试退出码为 0。
- `python -m pytest tests/test_swine_llm_wiki_runtime.py -q`
  - 结果：12 passed
- 状态词扫描范围：
  - `exports/planned_samples`
  - `exports/answer_skeletons`
  - `exports/generated_samples`
  - `exports/evaluated_samples`
  - `exports/training_sets`
- 扫描词包括：
  - `HUMAN_REVIEWED`
  - `legacy_evidence_status`
  - `task_use_status`
  - `gold_dataset_use`
  - `gold_dataset_role`
  - `boundary_only`
  - `positive_label_candidate`
  - `NEEDS_REVIEW`
  - `runtime_core_partial`
  - `source_anchored_clinical_page`
  - `evidence_status`
  - `fact_validity`
  - `source_status`
- 结果：未命中。

## 并行执行说明

- Phase 15 子智能体完成评估脚本和测试扩展。
- Phase 16 子智能体完成分层导出脚本和测试扩展。
- 第三个集成验证子智能体因外部服务返回 `403 Forbidden: insufficient balance` 失败；集成验证由主线程继续完成。

## 后续建议

- 将 Phase 14 从确定性 mock 生成升级为真实 LLM 两段式生成，但必须继续使用 Phase 13 skeleton 作为标准答案骨架。
- 将 Phase 15 的 deterministic judge 占位升级为“规则门禁 + 事实覆盖 + LLM judge + 人工抽检”的组合评估。
- 为 L5 药物边界负样本补齐 Phase 14 生成策略，使正式训练集中能稳定产出药物边界拒答/纠偏样本。
