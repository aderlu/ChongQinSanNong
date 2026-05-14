# 2026-05-13 Wiki-first Phase 14-16 边界样本补强记录

## 背景

Phase 12/13 已能规划并构建 L5 药物边界负样本骨架，但 Phase 14 早期只接受 `fact_id + source_id + rule_card_id` 三者齐全的事实锚点，导致只有规则卡约束的 L5 边界样本被跳过，Phase 16 的 `sft_l5_drug_boundary_negative.jsonl` 在正式批次中为空。

本次补强目标是让规则卡边界锚点成为高风险拒答/边界样本的合法证据形态，同时不把这类样本混入 L1-L4 正向 SFT。

## 代码变更

- `knowledge/llm_wiki_swine_authoritative/tools/phase14_generate_two_stage_samples.py`
  - 新增 `anchor_type`：
    - `fact`：包含事实、来源和规则卡。
    - `rule_card_boundary`：包含规则卡和 Wiki 页面锚点，用于边界/拒答样本。
  - L5/L6/L7 或 `boundary_or_refusal` 样本允许使用规则卡边界锚点。
  - L1-L4 正向样本仍要求事实级锚点；仅有规则卡边界锚点时会被跳过。
  - citation 检查改为按锚点类型判断：
    - fact 锚点要求 `source=`、`rule=`、`fact=`。
    - rule-card boundary 锚点要求 `rule=`、`page=`。
- `knowledge/llm_wiki_swine_authoritative/tools/phase15_fact_level_evaluate_samples.py`
  - 新增边界锚点结构规则：规则卡边界锚点只强制 `rule_card_id` 和 `page_relpath`。
  - 新增 `boundary_policy_check`：
    - L5 样本必须体现拒答、边界或标签/官方来源检查。
    - 直接给出剂量、疗程、给药途径、休药期、MRL 等执行性建议且没有拒答语义时硬门禁失败。
  - L5 的 `RC-DRUG-*` / `RC-WITHDRAWAL-*` 规则卡视为标签/边界来源约束，不再因缺少 A0 fact 自动全部失败。
- `knowledge/llm_wiki_swine_authoritative/tools/phase16_export_layered_training_sets.py`
  - 恢复并确认 L5 分支：`final_decision != accepted` 的药物边界样本进入 `sft_l5_drug_boundary_negative.jsonl`。
- `tests/test_swine_wiki_first_generation_pipeline.py`
  - 测试契约同步支持 fact 锚点与 rule-card boundary 锚点两种证据形态。

## 正式输出变化

执行日期：`20260513`

- Phase 13 skeletons：474
- Phase 14 generated samples：289
  - L1：46
  - L2：41
  - L3：41
  - L4：41
  - L5：71
  - L6：31
  - L7：18
- Phase 15 evaluated samples：289
  - accepted：220
  - rejected：69
  - reject reasons：
    - `fact:answer_missing_fact_citation`：18
    - `fact:sample_source_trust_not_authoritative`：18
    - `hard_gate:executive_content_missing_a0_source`：51
    - `judge:deterministic_placeholder_failed`：69
- Phase 16 layered outputs：
  - `sft_l1_retrieval_grounded.jsonl`：40
  - `sft_l2_diagnosis_support.jsonl`：39
  - `sft_l3_differential_support.jsonl`：39
  - `sft_l4_control_boundary.jsonl`：39
  - `sft_l5_drug_boundary_negative.jsonl`：10
  - `eval_l6_regulatory_guardrail.jsonl`：31
  - `eval_l7_judge_calibration.jsonl`：289

## 验证

- `python -m pytest tests/test_swine_wiki_first_generation_pipeline.py -q`
  - 结果：13 passed
  - 备注：Windows pytest 临时目录清理阶段仍有非致命 `PermissionError`。
- `python -m pytest tests/test_swine_llm_wiki_runtime.py -q`
  - 结果：12 passed
- 状态词扫描：
  - 范围：planned samples、answer skeletons、generated samples、evaluated samples、training sets。
  - 结果：未命中旧状态词。

## 结论

L5 药物边界负样本已从 Wiki 规划、规则卡骨架、两段式生成、事实/硬门禁评估到训练集导出全链路接通。当前正式批次中 L5 已有 10 条可用于边界拒答训练的数据，L7 校准集同步扩大到 289 条。
