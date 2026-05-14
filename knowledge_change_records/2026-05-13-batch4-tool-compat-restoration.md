# 2026-05-13 第四批修复记录：治理与运维工具旧路径兼容恢复

## 本批目标

恢复 `knowledge/llm_wiki_swine_authoritative/tools/` 根层下治理、审计、维护、图谱相关脚本的旧路径兼容入口，修复整理后大量测试和维护总入口因为“找不到脚本”而失败的问题。

## 修改前的问题

1. 真实脚本已按职责迁移到：
   - `tools/audit/`
   - `tools/wiki_ops/`
   - `tools/graph/`
2. 但旧 `tools/*.py` 根层兼容包装没有同步补齐。
3. 导致：
   - `test_swine_llm_wiki_runtime.py` 多项失败
   - `run_swine_wiki_maintenance_checks.py` 无法通过旧路径调用相关脚本
   - `audit_governance_compliance.py` 治理检查失败

## 原有状态概述

项目在结构上已经更清晰，但很多历史测试、自动化命令和维护入口仍默认认为脚本位于 `tools/` 根层。

## 本批采取的动作

1. 为 `audit/` 中脚本补根层兼容包装。
2. 为 `wiki_ops/` 中脚本补根层兼容包装。
3. 为 `graph/` 中脚本补根层兼容包装。
4. 包装方式与现有 phase12-18 兼容层一致，保证：
   - 直接执行
   - 动态导入
   - 旧测试路径
   都继续可用。

## 本批解决了什么

- 修复“脚本真实存在但旧入口失效”的回归。
- 让企业级结构整理与历史自动化链路兼容并存。

## 预计效果

- `test_swine_llm_wiki_runtime.py` 中与旧路径缺失相关的失败项将显著下降。
- 治理、维护、图谱检查总入口恢复可调用状态。
