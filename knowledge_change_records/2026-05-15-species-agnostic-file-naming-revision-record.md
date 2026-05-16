# 多物种 Pipeline 文件命名规范补充修订记录

日期：2026-05-15

关联文档：

- `D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md`

## 一、修改背景

用户要求在多物种 Wiki 生成与评估全链路可复用改造方案中，加入“同时修改对应文件名称，规范化、合理化”的要求。

原方案已经覆盖了配置化、manifest、Phase 12/16、54 字段、路径上下文和旧入口兼容，但没有明确要求把现有带历史阶段号、`wiki_first` 或物种专用语义的文件名同步整理。

## 二、之前存在的问题

当前文件名存在三类问题：

1. 部分文件名带历史阶段号，例如 `phase14_generate_two_stage_samples.py`。阶段号有助于追溯，但不适合作为长期公共能力文件名。
2. 部分文件名带 `wiki_first`，而本阶段目标是可复用 wiki-grounded 流程，后续也可能接入不同知识库，继续使用该名称会让职责含义不清。
3. 部分文件虽然未来要承载多物种流程，但文件名、变量或输出仍会让人误以为是猪病专用。

如果只改代码内部逻辑、不改文件命名，会产生以下问题：

- 新物种接入时入口含义不清。
- 文档、run manifest 和实际命令不一致。
- 后续清理和迁移公共包时难以判断哪些是通用能力，哪些是兼容入口。
- 容易继续复制旧脚本，而不是复用公共模块。

## 三、本次修改了什么

已修订主方案，新增以下要求：

1. 对应文件和目录名称必须同步规范化、合理化。
2. 第一阶段不直接删除旧文件名。
3. 旧文件名作为 wrapper 或 compatibility entrypoint 保留一个迁移周期。
4. 真正业务逻辑迁入通用命名文件。
5. 重命名必须配套更新测试、文档、运行脚本、change record 和 run manifest。

## 四、补充的命名迁移建议

主方案中新增了命名迁移表，核心包括：

- `phase12_plan_samples_from_wiki.py` -> `plan_samples_from_runtime_manifest.py`
- `phase13_build_answer_skeletons.py` -> `build_answer_skeletons.py`
- `phase14_generate_two_stage_samples.py` -> `generate_grounded_samples.py`
- `phase15_fact_level_evaluate_samples.py` -> `evaluate_fact_grounding.py`
- `phase16_export_layered_training_sets.py` -> `export_layered_training_sets.py`
- `phase18_dual_judge_and_arbitrate.py` -> `judge_and_arbitrate_samples.py`
- `wiki_first_judge_prompts.py` -> `judge_prompt_pack.py`
- `wiki_first_llm_client.py` -> `common/llm_client.py`
- `baseline_validation/generate_baseline_groups.py` -> `baseline_validation/generate_comparison_groups.py`
- `baseline_validation/compare_groups.py` -> `baseline_validation/build_comparison_table.py`
- `baseline_validation/run_baseline_experiment.py` -> `baseline_validation/run_comparison_experiment.py`

## 五、修改后解决了什么

这次补充解决的是工程可维护性问题：

- 公共流程不再长期挂着猪病或历史阶段含义的名称。
- 旧命令仍可运行，不破坏已有自动化。
- 新命名表达真实职责，方便后续鸡病和新 Wiki 接入。
- 后续公共包迁移时，能清楚区分“真实逻辑文件”和“兼容入口文件”。

## 六、预计效果

执行该补充要求后，最终代码结构会更清晰：

- 通用能力使用职责型文件名。
- 物种差异进入 config/adapter。
- 历史 phase 入口保留兼容，但不再承载主要业务逻辑。
- 每次重命名都有替代命令和验证记录，便于工作汇报和后续清理。

## 七、验证要求

正式执行文件重命名时，每个旧入口至少要验证：

1. 旧命令仍能运行。
2. 新命令能运行。
3. 两者在同一输入下输出一致或差异可解释。
4. run manifest 记录实际调用的新入口文件。
5. change record 记录旧文件名、新文件名、兼容策略和清理计划。
