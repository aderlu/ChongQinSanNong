# 调用链中文注释与行号映射补充记录

## 1. 修改概述

本次对 LLM Wiki 受控更新调用链的关键代码补充了中文注释，并在精简汇报文档中加入函数与行号位置表，方便汇报时直接引用代码位置。

## 2. 修改前存在的问题

原来的文档虽然已经说明了完整流程，但在汇报时还缺少两类信息：

- 调用链关键函数具体位于哪个脚本、哪一行。
- 代码里哪些位置负责门禁、调度、验收和证据输出。

同时，部分脚本虽然已有中文注释，但没有明确说明它们在整条调用链中的职责。

## 3. 本次新增内容

本次补充了以下内容：

- `run_guarded_wiki_update.py` 增加了模块级说明和关键函数中文 docstring。
- `audit_crud_decision.py` 增加了模块级说明和关键函数中文 docstring。
- `run_swine_wiki_maintenance_checks.py` 增加了模块级说明和关键函数中文 docstring。
- `audit_governance_compliance.py` 增加了模块级说明和关键函数中文 docstring。
- `build_runtime_core_manifest.py`、`phase9_rebuild_indexes_graph_smoke.py`、`audit_graph_change_diff.py`、`audit_runtime_hallucination_risk.py`、`audit_swine_llm_wiki_readiness.py` 增加了模块级说明和主入口说明。
- 精简汇报文档 `WIKI_GUARDED_UPDATE_FLOW_BRIEF_CN.md` 增加了“函数与行号位置”表。

## 4. 修改后解决的问题

现在在汇报时可以直接说清楚：

- 固定入口在什么位置。
- 哪个函数负责解析命令。
- 哪个函数负责执行子进程。
- 哪个函数负责写运行证据。
- 哪个函数负责 CRUD 门禁。
- 哪个函数负责更新后验收。
- 哪个函数负责图谱、风险、readiness 和编码检查。

## 5. 预计效果

这次补充能让汇报材料更像“可定位的工程说明”，而不是只停留在流程描述：

- 既能讲清楚流程。
- 也能讲清楚代码位置。
- 还能快速把说明和源代码对应起来。

## 6. 编码保护措施

本次采取局部中文注释和局部文档增补方式，尽量不重写原文件主体，以降低乱码和回归风险。
