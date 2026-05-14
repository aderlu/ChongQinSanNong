# 2026-05-13 Wiki-First Data Generation Implementation Plan

## Change

新增完整实施文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_FIRST_DATA_GENERATION_IMPLEMENTATION_PLAN.md`

## Purpose

该文档用于把猪病 LLM Wiki 从“生成时辅助检索材料”升级为数据生成与评估流程的主控来源：

1. 先从 Wiki runtime allowlist 规划样本。
2. 用结构化 fact/rule/source 决定标准答案骨架。
3. 使用两段式生成。
4. 每条样本强制绑定 evidence anchors。
5. 评估不只依赖 judge 打分。
6. 高风险内容走 hard gate。
7. 训练集按能力层导出。

## Proposed Implementation Phases

- `phase12_plan_samples_from_wiki.py`
- `phase13_build_answer_skeletons.py`
- `phase14_generate_two_stage_samples.py`
- `phase15_fact_level_evaluate_samples.py`
- `phase16_export_layered_training_sets.py`

## Expected Outputs

- `exports/planned_samples/wiki_sample_plan_YYYYMMDD.jsonl`
- `exports/answer_skeletons/wiki_answer_skeletons_YYYYMMDD.jsonl`
- `exports/generated_samples/two_stage_samples_YYYYMMDD.jsonl`
- `exports/evaluated_samples/fact_evaluated_samples_YYYYMMDD.jsonl`
- `exports/training_sets/*.jsonl`
- `issues/wiki_first_generation_reports/*.json|*.md`

## Notes

该变更仅新增实施文档和执行蓝图，尚未实现 phase12-phase16 脚本。下一步建议先落地 phase12 和 phase13，因为它们不需要 LLM 调用，可以最快验证 Wiki-first 样本规划与答案骨架是否可行。
