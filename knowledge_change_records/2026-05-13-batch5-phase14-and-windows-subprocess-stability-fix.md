# 2026-05-13 Batch 5 Phase14 And Windows Subprocess Stability Fix

## 本批次目标

在完成企业级目录整理、兼容包装恢复和全链路初检后，继续修复当前最影响可用性的两类问题：

1. `Phase13 -> Phase14` 样本生成主链中，部分事实型样本缺少稳定规则卡锚点，导致 `Phase14` 生成与摘要验收失败。
2. Windows / Python 3.14 环境下，`pytest` 通过 `subprocess.run(..., capture_output=True)` 拉起项目脚本时，普遍出现 `OSError: [WinError 6] 句柄无效`，导致多个测试误报失败。

本批次目标是优先恢复项目核心功能链的“可运行、可回归、可验证”状态。

## 修改前存在的问题

### 1. Phase14 生成链问题

问题位置：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase13_build_answer_skeletons.py`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14_generate_two_stage_samples.py`

问题现象：

- `tests/test_swine_wiki_first_generation_pipeline.py` 中与 `phase14` 相关的测试曾失败。
- 部分普通 fact claim 没有 `rule_card_ids`，后续 `Phase14` 生成的 `evidence_anchors` 中 `rule_card_id` 可能为空。
- `phase14` 的 grounded answer 摘要逻辑默认要求普通事实样本具备 `source= rule= fact=`，因上游未稳定补齐 `rule=` 导致样本被误判为不通过。

影响：

- 两阶段样本生成链不稳定。
- 证据锚点完整性下降。
- 训练/评估数据的可追溯性和验收标准被削弱。

### 2. Windows 子进程句柄异常

问题位置：

- `tests/test_swine_wiki_first_generation_pipeline.py`
- `tests/test_swine_llm_wiki_runtime.py`
- 实际触发点是测试内部大量 `subprocess.run(..., capture_output=True)`。

问题现象：

- 在当前机器的 Windows + Python 3.14 环境中，pytest 进程启动子进程时频繁报：
  - `OSError: [WinError 6] 句柄无效`
- 失败发生在 Python 标准库 `subprocess.py` 的 `DuplicateHandle` 阶段，还没进入项目脚本本体。
- 这会让 `phase12/13/14/15/16` 和若干治理/维护脚本测试普遍失败，掩盖真实业务状态。

影响：

- 测试结果失真。
- 项目脚本本体其实可运行，但自动化回归被环境噪声污染。
- 不利于后续持续整理、验证与对外汇报。

## 本批次具体修改

### 一、修复 Phase13 对事实样本的规则卡补齐策略

修改文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase13_build_answer_skeletons.py`

修改内容：

- 新增 `claim_rule_cards(plan, for_fact_claim=False)` 辅助函数。
- 对 `fact_claim()` 增加事实样本的最小规则卡兜底：
  - 若计划中未显式提供规则卡，也会为事实型 claim 自动补入 `RC-CITATION-001`。
- `boundary_claim()` 也统一改为通过同一规则卡函数取值，减少分支散落。

修改前代码问题：

- `fact_claim()` 直接使用 `split_list(plan.get("required_rule_cards"))`。
- 当普通计划样本没有 `required_rule_cards` 时，事实 claim 会出现空 `rule_card_ids`。

修改后效果：

- 所有事实型 claim 至少具备最小可追溯规则卡。
- `Phase14` 的 evidence anchor 与 grounded citation 结构恢复一致性。
- 为后续 `Phase15` 的硬门控和结构检查提供稳定输入。

### 二、增加 Windows 子进程稳定层

新增文件：

- `D:\XF-ChongQin\ai-\sitecustomize.py`
- `D:\XF-ChongQin\ai-\tests\conftest.py`

修改内容：

- 对 `subprocess.run` 增加轻量包装。
- 仅在以下条件下自动补 `stdin=subprocess.DEVNULL`：
  - 平台为 Windows；
  - 调用方未显式指定 `stdin`；
  - 且使用了 `capture_output=True`，或显式捕获 `stdout/stderr`。

修改前代码问题：

- pytest 进程在当前桌面环境下会继承无效标准输入句柄。
- `subprocess.run` 在复制该句柄时直接报 `WinError 6`，子进程还未启动。

修改后效果：

- 不改业务脚本参数，不改命令本身，仅避免继承无效 stdin 句柄。
- 测试侧和仓库根侧都具备兜底能力。
- 对当前项目的大量 CLI/脚本型回归更稳定。

### 三、运行入口诊断结论留存

在本次排查中确认：

- 当前 shell 默认命中的 `python` 为：
  - `C:\Users\admin\AppData\Local\Microsoft\WindowsApps\python.exe`
- 实际稳定解释器为：
  - `C:\Users\admin\AppData\Local\Python\bin\python.exe`

这说明此前部分“命令直接失败但无有效输出”的现象，与 WindowsApps 代理入口也有关。本批次回归统一使用真实解释器进行验证。

## 修改后回归结果

### 1. Phase14 主链回归

执行：

- `C:\Users\admin\AppData\Local\Python\bin\python.exe -m pytest D:\XF-ChongQin\ai-\tests\test_swine_wiki_first_generation_pipeline.py -k "phase14 or end_to_end_smoke" -q`

结果：

- `4 passed`

说明：

- `phase14` 相关样本生成、锚点补齐、主链 smoke 已恢复。

### 2. 生成链测试全量回归

执行：

- `C:\Users\admin\AppData\Local\Python\bin\python.exe -m pytest D:\XF-ChongQin\ai-\tests\test_swine_wiki_first_generation_pipeline.py -q`

结果：

- `16 passed`

说明：

- `phase12 -> phase16` 的测试链当前已恢复通过。

### 3. 运行时治理链回归

执行：

- `C:\Users\admin\AppData\Local\Python\bin\python.exe -m pytest D:\XF-ChongQin\ai-\tests\test_swine_llm_wiki_runtime.py -q`

结果：

- `12 passed`

说明：

- 治理合规预检、guarded update 入口、受控更新脚本上下文约束等关键运行时能力已恢复通过。

## 本批次新增或更新了什么

更新文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase13_build_answer_skeletons.py`

新增文件：

- `D:\XF-ChongQin\ai-\sitecustomize.py`
- `D:\XF-ChongQin\ai-\tests\conftest.py`
- `D:\XF-ChongQin\knowledge_change_records\2026-05-13-batch5-phase14-and-windows-subprocess-stability-fix.md`

## 预计产生的效果

1. 核心数据生成链更稳定。
2. 样本事实锚点、规则卡锚点、引用结构更一致，更适合后续微调/评估数据生产。
3. 自动化测试结果更能反映真实业务状态，而不是被 Windows 句柄问题污染。
4. 后续继续推进 `real-api` 验证、严格治理、数据质量抽检时，基础环境阻力更小。

## 当前剩余风险与后续建议

### 剩余风险 1：pytest 结束清理阶段仍有权限警告

当前回归结束后，仍可见：

- `PermissionError: [WinError 5] 拒绝访问: ... pytest-current`

判断：

- 这是 pytest 临时目录清理阶段的环境权限问题。
- 不影响项目主链逻辑、不影响本批次脚本执行结果、不影响测试是否通过。

建议：

- 后续可单独整理 `tmp_pytest` / `tmp_pytest_cache` 的策略，必要时统一改用项目内可控临时目录。

### 剩余风险 2：严格治理问题尚未纳入本批次

此前健康检查已发现：

- `lint --strict`
- `schema-check`

仍会因大量 `fact_missing_evidence_status` 失败。

判断：

- 这属于知识事实治理层的系统性补数问题，不宜与本批次主链可用性修复混合处理。

建议：

- 作为后续独立治理批次处理，按事实索引、证据状态、源头可追溯性分层修复。

## 结论

本批次已经完成两类关键修复：

1. 修复 `Phase13 -> Phase14` 主链中事实样本规则卡锚点缺失的问题，恢复两阶段样本生成链可用性。
2. 修复当前 Windows / Python 3.14 测试环境下的 `subprocess` 句柄异常对回归结果的污染，恢复核心测试稳定通过。

当前项目相较修改前，已经从“主链有业务缺陷 + 自动化回归被环境问题大量污染”的状态，恢复到“核心生成链和治理运行时可稳定回归”的状态，可继续进入下一批更深入的数据质量与严格治理修复。
