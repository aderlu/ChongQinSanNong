# 2026-05-13 LLM Wiki 全功能健康检查报告

## 检查目标

对当前 `D:\XF-ChongQin\ai-` 项目中的 LLM Wiki 猪病知识库及其相关数据生成、评估、仲裁、治理工具链进行一次全面可用性检查，判断是否达到“功能完全正常可用”的状态，并识别当前阻塞点。

## 检查范围

本次检查覆盖以下能力域：

1. Python 包与主 CLI 入口
2. Wiki CLI 主命令与核心子命令
3. 知识库运行时状态、schema、lint、coverage、query、graph-build
4. Wiki-first 数据生成、评估、仲裁链路
5. Wiki 治理、守护更新、审计与维护脚本
6. 自动化测试与编译级检查

## 检查方法

### 一、自动化检查

- 运行 `pytest`
- 运行 `compileall`
- 检查关键依赖安装状态

### 二、CLI 与运行时烟测

- `main.py --help`
- `python -m chicken_data_synthesis.wiki_cli --help`
- `status`
- `lint --strict`
- `schema-check`
- `coverage`
- `query`
- `graph-build`

### 三、工具链烟测

- phase12 / phase13 / phase14 / phase15 / phase18 入口
- `create_crud_decision.py`
- `run_guarded_wiki_update.py`
- 典型受保护写脚本
- 审计与维护脚本

## 总体结论

**结论：当前项目不处于“所有功能完全正常可用”的状态。**

更准确的判断是：

- 主 CLI 可启动
- Wiki CLI 大部分基础功能可启动
- `status`、`coverage`、`query`、`graph-build` 可用
- phase12、phase13、phase15、phase18 的入口基本可用
- phase18 自检通过
- 但严格健康检查、schema 检查、部分治理维护链路和 phase14 生成链路存在明确故障
- 自动化测试存在 7 项失败

因此当前只能判定为：

**“系统部分可用，但未达到企业级稳定可交付状态。”**

## 关键通过项

### 1. 主 CLI 入口可用

- `main.py --help` 正常
- `python -m chicken_data_synthesis.wiki_cli --help` 正常

说明主包入口和命令注册链路没有整体损坏。

### 2. Wiki 状态查询可用

- `status` 正常返回
- 已识别：
  - `raw_file_count = 865`
  - `fact_count = 2230`
  - `disease_count = 73`
  - `drug_count = 84`
  - `rule_count = 449`

说明知识库基础结构和主数据加载仍然可工作。

### 3. 图谱构建可用

- `graph-build` 成功
- 产出：
  - `graph-data.json`
  - `knowledge-graph.html`
  - `knowledge-graph.md`
- 构建结果：
  - `node_count = 4636`
  - `link_count = 4533`

说明图谱主构建能力仍可运行。

### 4. 检索查询可用

- `query "猪流感 鉴别诊断" --top-k 5` 正常返回上下文与结构化事实

说明 Wiki 检索层与事实命中层可用。

### 5. phase12 / phase13 / phase15 / phase18 入口可用

- `phase12_plan_samples_from_wiki.py` 可运行，烟测通过
- `phase13_build_answer_skeletons.py --help` 正常
- `phase15_fact_level_evaluate_samples.py --help` 正常
- `phase18_dual_judge_and_arbitrate.py --self-test` 正常，返回 `ok = true`

说明数据链路并未整体失效。

### 6. phase19 相关测试通过

- `test_phase19_layered_export_admission.py` 通过

说明 phase16/phase19 的部分兼容与分层路径保持住了。

### 7. 受保护写链部分脚本本体可用

- `create_crud_decision.py --help` 正常
- `apply_dis026_fmd_authority_web_refresh.py` 在直接执行时能正确拒绝并提示必须通过 `run_guarded_wiki_update.py`
- `run_guarded_wiki_update.py --help` 正常

说明守护写入机制的业务脚本本身还在工作。

## 关键失败项

### 1. 自动化测试失败

本次 `pytest` 结果：

- 55 项中 48 项通过
- **7 项失败**

失败集中在两个区域：

1. `tests/test_swine_llm_wiki_runtime.py`
2. `tests/test_swine_wiki_first_generation_pipeline.py`

### 2. 严格 lint 失败

`wiki_cli --json lint --strict` 返回 `ok = false`

主因是大量：

- `fact_missing_evidence_status`

问题规模不是少量边角问题，而是大面积结构性缺失，影响严格治理判定。

### 3. schema-check 失败

`wiki_cli --json schema-check` 返回 `ok = false`

失败原因与 `lint --strict` 高度一致，核心是大量 fact 未设置 `evidence_status`。

### 4. phase14 生成链路失败

测试失败表明：

- `test_phase14_generated_samples_have_two_stages` 失败
- `test_phase14_every_sample_has_evidence_anchors` 失败
- `test_phase12_to_16_end_to_end_smoke_outputs_and_manifest_counts` 因 phase14 失败而失败

从测试断言看，phase14 当前至少存在两类问题：

1. 生成结果 `summary["passed"]` 为 `false`
2. 部分 `evidence_anchors` 中 `rule_card_id` 为空，不满足测试契约

这说明 phase14 并非只是入口可启动，而是输出结构已经与预期契约不一致。

### 5. 治理/维护脚本旧路径兼容中断

以下测试和工具失败，根因都是**清理整理后旧路径文件不存在**：

- `audit_governance_compliance.py`
- `audit_graph_change_diff.py`
- `run_swine_wiki_maintenance_checks.py`
- `run_guarded_wiki_update.py` 间接引用的旧路径链
- `build_runtime_core_manifest.py`
- `phase9_rebuild_indexes_graph_smoke.py`
- `audit_runtime_hallucination_risk.py`
- `audit_swine_llm_wiki_readiness.py`
- `audit_encoding_integrity.py`
- `create_crud_decision.py` 的旧测试路径引用
- `apply_dis026_fmd_authority_web_refresh.py` 的旧测试路径引用

需要强调：

这些并不全是“脚本本体坏了”，而是**测试和维护入口仍写死在 `tools/` 根层旧路径**，而整理后真实实现被移入了 `tools/audit/`、`tools/wiki_ops/`、`tools/graph/` 等子目录，但尚未像 phase12/13/14/15/16/18 那样补齐兼容包装。

### 6. 治理合规预检失败

直接运行新位置的 `audit/audit_governance_compliance.py` 时，返回：

- `passed = false`

原因是它要求的若干治理工具仍期望位于旧路径：

- `tools/audit_governance_compliance.py`
- `tools/audit_graph_change_diff.py`
- `tools/run_swine_wiki_maintenance_checks.py`
- `tools/run_guarded_wiki_update.py`

因此该治理预检目前也未恢复到“完全正常”。

## 根因分类

### A. 知识库内容治理问题

这类问题来自知识库内容本身，不是整理动作导致：

1. 大量 fact 缺失 `evidence_status`
2. `RC-TOX-001` 存在 source unresolved 警告
3. 严格 lint 与 schema-check 无法通过

这代表知识库数据治理层还没有闭环。

### B. 数据生成链路契约问题

这类问题来自 phase14 输出与测试契约不一致：

1. phase14 `passed = false`
2. 部分 anchor 的 `rule_card_id` 为空
3. 进而影响 phase12-16 端到端烟测

这代表 Wiki-first 数据生成链路没有完全稳定。

### C. 结构整理后的旧路径兼容缺口

这类问题主要是本轮结构优化后遗留的兼容问题：

1. `audit/`、`wiki_ops/`、`graph/` 真实脚本已迁移
2. 但旧 `tools/*.py` 根路径包装未补齐
3. 测试和维护脚本仍调用旧路径

这导致治理链大量报“找不到文件”。

## 风险等级

### P0

- `lint --strict` 失败
- `schema-check` 失败
- phase14 主生成链失败

这三项意味着项目不能被认定为“全功能稳定可用”。

### P1

- 治理维护工具旧路径大量失效
- `test_swine_llm_wiki_runtime.py` 关键治理测试失败

这会影响企业级运维、审计和更新流程。

### P2

- pytest 清理阶段存在 Windows 权限噪音
- 某些帮助命令和路径检查仍依赖旧布局

这类问题次要，但会影响日常体验和自动化环境稳定性。

## 当前可用性判断

### 可以认为“可用”的部分

- 主 CLI 启动
- Wiki CLI 帮助和基础命令
- status
- coverage
- query
- graph-build
- phase12
- phase13 入口
- phase15 入口
- phase18 自检
- 部分受保护更新脚本本体

### 不能认为“完全正常”的部分

- strict lint
- schema-check
- phase14 生成链
- phase12-16 端到端烟测
- 治理合规预检
- 维护检查总入口
- 多个旧路径治理工具入口

## 建议整改顺序

### 第一优先级

1. 补齐 `tools/` 根层对 `audit/`、`wiki_ops/`、`graph/` 的兼容包装
2. 修复 `run_swine_wiki_maintenance_checks.py` 中对旧路径的调用
3. 修复 `audit_governance_compliance.py` 的工具路径清单

### 第二优先级

1. 修复 phase14 anchor 生成契约
2. 让 phase14 的 `summary["passed"]` 恢复为通过
3. 重新跑 phase12-16 端到端测试

### 第三优先级

1. 系统性补齐 `fact.evidence_status`
2. 清理 unresolved source
3. 让 `lint --strict` 和 `schema-check` 全量通过

## 最终结论

当前 LLM Wiki 猪病知识库**不是“所有功能完全正常可用”**。

更准确的结论是：

- 核心知识加载、检索、图谱、部分数据链和部分守护更新机制仍可运行
- 但严格治理检查、schema 健康度、phase14 数据生成链、以及整理后旧路径治理入口存在明显故障
- 项目目前处于**“部分可用、但未通过全面健康验收”**状态

后续如要达到“企业级全功能可用”，应按本报告中的 P0/P1/P2 顺序继续修复。
