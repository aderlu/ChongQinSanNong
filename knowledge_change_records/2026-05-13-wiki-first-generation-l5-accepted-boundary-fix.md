# 2026-05-13 Wiki-first L5 accepted 边界训练修复记录

## 修复目标

严格检查后发现两处不完整：

1. `sft_l5_drug_boundary_negative.jsonl` 只导出了 rejected L5 样本，违反实施文档中“训练样本来自 accepted evaluated sample”的要求。
2. Phase 15 的中文高风险/药物边界正则存在乱码文本，中文剂量、休药期和拒答表达可能无法被稳定识别。

本次修复目标是让 L5 训练集导出通过评估的合格药物边界拒答样本，并让中文硬门禁检测可验证、可回归。

## 代码修复

- `knowledge/llm_wiki_swine_authoritative/tools/phase16_export_layered_training_sets.py`
  - L5 导出条件由 `final_decision != accepted` 改为 `is_accepted(eval_row)`。
  - rejected L5 不再进入 SFT 主训练层，仍保留在 L7 judge calibration 全量集中。
- `knowledge/llm_wiki_swine_authoritative/tools/phase14_generate_two_stage_samples.py`
  - `rule_card_boundary` 锚点优先选择 `RC-DRUG-*`、`RC-WITHDRAWAL-*`、`RC-DISEASE-REGULATORY-*`。
  - 普通 fact 锚点恢复使用原始首个规则卡，避免 L1-L4 因误用监管规则卡而触发硬门禁。
- `knowledge/llm_wiki_swine_authoritative/tools/phase15_fact_level_evaluate_samples.py`
  - 使用 Unicode escape 覆盖乱码正则，修复中文高风险触发、药物执行性内容和拒答边界表达检测。
  - 已验证中文 `剂量`、`休药期`、`上报`、`扑杀`、`不能直接提供`、`边界` 可被对应规则识别。
- `tests/test_swine_wiki_first_generation_pipeline.py`
  - 新增中文药物边界门禁回归测试。
  - Phase 16 测试契约改为：L5 accepted 边界拒答进入 SFT；L6 rejected 高风险样本进入 eval；L7 保留全量。

## 正式链路输出

执行日期：`20260513`

- Phase 13 skeletons：474
- Phase 14 generated samples：289
- Phase 15 evaluated samples：289
  - accepted：230
  - rejected：59
- Phase 16 layered outputs：
  - `sft_l1_retrieval_grounded.jsonl`：40
  - `sft_l2_diagnosis_support.jsonl`：39
  - `sft_l3_differential_support.jsonl`：39
  - `sft_l4_control_boundary.jsonl`：39
  - `sft_l5_drug_boundary_negative.jsonl`：71
  - `eval_l6_regulatory_guardrail.jsonl`：31
  - `eval_l7_judge_calibration.jsonl`：289

## L5 修复后验收

- L5 训练集行数：71
- `final_decision`：全部为 `accepted`
- `hard_gate_passed`：全部为 `true`
- `reject_reasons` metadata：0 条
- L5 规则卡锚点：`RC-DRUG-001`

## 验证

- `python -m pytest tests/test_swine_wiki_first_generation_pipeline.py -q`
  - 结果：14 passed
  - 备注：Windows pytest 临时目录清理阶段仍有非致命 `PermissionError`。
- `python -m pytest tests/test_swine_llm_wiki_runtime.py -q`
  - 结果：12 passed
- 旧状态词扫描：
  - planned samples、answer skeletons、generated samples、evaluated samples、training sets 均未命中。

## 结论

L5 药物边界负样本现在符合“accepted evaluated sample 进入训练集”的目标。训练集中不再混入被 Phase 15 判定失败的 L5 样本；失败样本仍保留在 L7 校准集中，用于评估器校准和误差分析。
