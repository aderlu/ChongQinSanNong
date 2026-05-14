# 2026-05-13 第三批清洗记录：兼容入口修复与路径基准校正

## 本批目标

在完成 `tools/` 分层后，修复由于脚本迁移到子目录导致的运行路径基准问题，并验证旧路径兼容入口是否仍可被动态加载和执行。

## 修改前的问题

1. 原始脚本大量使用 `Path(__file__).resolve().parents[1]` 作为 Wiki 根目录基准。
2. 在脚本迁移到 `pipeline/`、`wiki_ops/`、`audit/`、`graph/` 后，这个层级不再正确，会把 `tools/` 误判为 Wiki 根目录。
3. 旧路径兼容包装在被 `importlib.util.spec_from_file_location` 直接加载时，无法自动找到 `_compat_loader.py`。

## 原有状态概述

- 原脚本全部位于 `tools/` 根层时，`parents[1]` 仍然成立。
- 分层之后，真实实现脚本位于 `tools/<group>/...`，目录深度增加。
- 测试与人工脚本存在“按旧文件路径直接动态导入”的场景。

## 本批采取的动作

1. 将迁移后的真实实现脚本中的 `ROOT/WIKI_ROOT` 基准统一从 `parents[1]` 校正为 `parents[2]`。
2. 为旧路径兼容包装脚本增加本目录 `sys.path` 自举逻辑，确保 `_compat_loader.py` 可以被动态加载场景找到。
3. 对关键兼容入口进行了快速验证：
   - `phase12_plan_samples_from_wiki.py --help`
   - `test_phase19_layered_export_admission.py`
   - 旧路径动态导入 `phase15_fact_level_evaluate_samples.py`
   - 旧路径动态导入 `phase18_dual_judge_and_arbitrate.py`

## 本批解决了什么

- 解决了工具链分层后最关键的运行路径失真问题。
- 解决了旧路径动态导入兼容失败的问题。
- 让“结构更清晰”和“运行仍稳定”同时成立。

## 更新或新增了什么

- 更新：分层后的 `pipeline/`、`wiki_ops/`、`audit/`、`graph/` 真实实现脚本中的路径基准
- 更新：旧路径兼容包装脚本的加载自举逻辑
- 新增：本验证修复记录文档

## 验证结果

1. `phase12` 旧路径入口帮助信息可正常输出。
2. `phase19` 相关测试通过。
3. `phase15` 旧路径动态导入后，`boundary_policy_check` 与 `main` 可见。
4. `phase18` 旧路径动态导入后，`evaluate_samples` 与 `main` 可见。

## 预计效果

- 后续继续整理 `tools` 其他子域时，可以复用同样的“真实实现迁移 + 兼容入口保留 + 路径基准校正”模式。
- 项目结构已经具备企业级分层雏形，同时保住了当前主链的基本可运行性与可验证性。
