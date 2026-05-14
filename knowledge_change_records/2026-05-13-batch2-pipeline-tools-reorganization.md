# 2026-05-13 第二批清洗记录：Wiki-first 数据生成与评估工具链重组

## 本批目标

将猪病 Wiki-first 数据生成、评估、仲裁相关脚本从 `tools/` 根层整理到更清晰的 `pipeline/` 分组下，同时保留旧路径兼容入口，避免测试和人工运行脚本失效。

## 修改前的问题

1. `knowledge/llm_wiki_swine_authoritative/tools/` 根目录中同时混放了：
   - Wiki 维护脚本
   - 审计脚本
   - 图谱脚本
   - 数据生成脚本
   - 评估与仲裁脚本
2. phase12、13、14、15、16、18 与 `wiki_first_llm_client.py`、`wiki_first_judge_prompts.py` 属于同一数据链路，但文件名和位置没有体现职责分组。
3. 现有测试通过“按文件路径动态加载”的方式引用脚本，若直接移动文件会导致测试和人工命令断裂。

## 原有结构概述

原有相关文件全部位于：

- `knowledge/llm_wiki_swine_authoritative/tools/phase12_plan_samples_from_wiki.py`
- `knowledge/llm_wiki_swine_authoritative/tools/phase13_build_answer_skeletons.py`
- `knowledge/llm_wiki_swine_authoritative/tools/phase14_generate_two_stage_samples.py`
- `knowledge/llm_wiki_swine_authoritative/tools/phase14_real_api_generate_30.py`
- `knowledge/llm_wiki_swine_authoritative/tools/phase14_real_api_generate_40_parallel.py`
- `knowledge/llm_wiki_swine_authoritative/tools/phase15_fact_level_evaluate_samples.py`
- `knowledge/llm_wiki_swine_authoritative/tools/phase16_export_layered_training_sets.py`
- `knowledge/llm_wiki_swine_authoritative/tools/phase18_dual_judge_and_arbitrate.py`
- `knowledge/llm_wiki_swine_authoritative/tools/wiki_first_llm_client.py`
- `knowledge/llm_wiki_swine_authoritative/tools/wiki_first_judge_prompts.py`
- `knowledge/llm_wiki_swine_authoritative/tools/test_phase19_layered_export_admission.py`

## 本批采取的动作

1. 将上述主链脚本迁移到 `tools/pipeline/`。
2. 在原路径保留兼容包装文件。
3. 兼容包装文件通过动态加载真实实现模块并转发执行，保证：
   - `python old_path.py`
   - 按旧路径 `importlib` 加载
   - 测试中按旧路径引用模块
   仍能工作。
4. 对 `phase18` 所需的 `wiki_first_judge_prompts.py`、对 `phase14` 所需的 `wiki_first_llm_client.py` 一并纳入同一职责层。

## 本批解决了什么

- 让“数据生成、评估、仲裁”成为一个明确的工具子域，而不是散落在 `tools` 根层。
- 给后续继续拆分为企业级 package/module 奠定目录基础。
- 在不破坏现有调用链的情况下，实现结构升级。

## 更新或新增了什么

- 新增 `tools/pipeline/` 中的真实实现位置
- 新增原路径兼容包装脚本
- 更新 `tools/README.md` 的职责说明

## 预计效果

- 后续排查真实 API 调用链、数据生成流程、评估与仲裁逻辑时，定位路径更直接
- 项目目录更符合企业级“按职责分组”的组织方式
- 为第三阶段继续清理 `wiki_ops/`、`audit/`、`graph/` 链路提供模板
