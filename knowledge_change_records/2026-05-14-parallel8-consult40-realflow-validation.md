# 2026-05-14 八路并发 40 条真实问诊 CSV 生成与全流程验证记录

## 本次目标

本次执行目标是重新使用真实大模型，以八路并发方式生成 40 条猪病问诊 CSV 数据，并完整验证 Phase13、Phase14、Phase15、Phase18、Phase16 的运行链路、字段完整性、数据质量、耗时表现和产物清理情况。

批次编号：`20260514_parallel8_consult40_v1`

## 防乱码措施

所有 PowerShell 命令执行前均设置：

```powershell
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

同时修复了 `consultation_case_variables.py` 的历史乱码内容，并用正常中文重新写入问诊场景变量库。

## 运行前发现并修复的问题

### 问题一：Phase14 缺失 `scenario_for`

第一次执行 Phase14 时失败，错误为：

```text
NameError: name 'scenario_for' is not defined
```

原因是前一轮清理重复函数时，将 Phase14 仍在调用的唯一包装入口也清理掉了。

修复措施：
- 在 `phase14_generate_two_stage_samples.py` 中恢复唯一的 `scenario_for` 和 `case_user_query_for` 包装函数。
- 函数内部统一调用 `consultation_case_variables.py`，避免多套场景逻辑重复存在。

### 问题二：问诊变量库存在乱码

检查发现 `consultation_case_variables.py` 中大量中文字符串已经乱码。该问题会直接污染 `case_context` 和 `case_user_query`。

修复措施：
- 删除旧文件并用 UTF-8 正常中文重建。
- 增加抽检，确认生成文本没有乱码。
- 顺手修复“出现异常出现异常”的拼接重复问题。

## 全流程执行结果

### Phase13：构建回答骨架

- 输入 plan：`exports/planned_samples/wiki_sample_plan_20260514_fullflow40_keypool.jsonl`
- 输出：`exports/answer_skeletons/wiki_answer_skeletons_20260514_parallel8_consult40_v1.jsonl`
- 生成数量：40
- 耗时：约 1.22 秒
- 结果：通过

层级分布：
- `L1_retrieval_grounded`: 17
- `L2_diagnosis_support`: 7
- `L3_differential_support`: 7
- `L4_control_boundary`: 7
- `L6_regulatory_guardrail`: 2

### Phase14：八路真实模型生成

- 模式：`real-api`
- 并发：8
- 模型：`hunyuan-turbos-20250926`
- 输出：`exports/generated_samples/two_stage_samples_20260514_parallel8_consult40_v1.jsonl`
- 生成数量：40/40
- fallback 数量：0
- missing anchors：0
- missing grounded citations：0
- 耗时：约 202.50 秒
- 结果：通过

### Phase15：事实门控与硬风险检查

- 输出：`exports/evaluated_samples/fact_evaluated_samples_20260514_parallel8_consult40_v1.jsonl`
- 样本数：40
- accepted：29
- rejected：11
- 耗时：约 1.33 秒
- 结果：通过

拒绝原因集中为：
- `hard_gate:executive_content_missing_a0_source`: 11
- `judge:deterministic_placeholder_failed`: 11

这说明仍有 11 条回答触碰到执行性内容边界。该拒绝不是 API 或字段失败，而是 Phase15 安全策略生效。

### Phase18：八路真实双裁判与仲裁

- 模式：真实 LLM 双裁判 + 仲裁
- 并发：8
- 输出：`exports/semantic_evaluated_samples/semantic_evaluated_samples_20260514_parallel8_consult40_v1.jsonl`
- 样本数：40
- 双裁判数量：29
- Phase15 硬门控跳过：11
- semantic accepted：23
- semantic review：6
- semantic rejected：11
- 耗时：约 297.51 秒
- 结果：通过

说明：
- 11 条 rejected 是 Phase15 硬门控失败后按设计跳过双裁判。
- 29 条进入双裁判的样本均完成真实裁判和仲裁。

### Phase16：导出训练 CSV

输出文件：
- `exports/training_sets/swine_wiki_training_main_20260514_parallel8_consult40_v1.csv`
- `exports/training_sets/swine_wiki_training_main_train_ready_20260514_parallel8_consult40_v1.csv`
- `exports/training_sets/swine_wiki_training_dataset_production_20260514_parallel8_consult40_v1.csv`
- `exports/training_sets/swine_wiki_training_dataset_production_train_ready_20260514_parallel8_consult40_v1.csv`
- `exports/training_sets/training_set_manifest_20260514_parallel8_consult40_v1.json`

导出结果：
- 全量训练主 CSV：40 行
- train-ready CSV：23 行
- accepted：23
- review：6
- rejected：11
- 耗时：约 1.40 秒
- 结果：通过

## 字段完整性检查

训练主 CSV 关键字段检查结果：

- `sample_id`: 0 个空值
- `case_context`: 0 个空值
- `case_user_query`: 0 个空值
- `user_query`: 0 个空值
- `assistant_answer`: 0 个空值
- `grounded_audit_answer`: 0 个空值
- `phase15_final_decision`: 0 个空值
- `phase18_semantic_decision`: 0 个空值
- `export_decision`: 0 个空值
- `final_label`: 0 个空值
- `final_total_score`: 0 个空值
- `field_source_map`: 0 个空值

accepted 样本中，双裁判和仲裁字段均完整：
- `judge_a_total_score`: 0 个空值
- `judge_b_total_score`: 0 个空值
- `arbiter_final_label`: 0 个空值

全量 CSV 中有 11 行的 `judge_a_total_score`、`judge_b_total_score`、`arbiter_final_label` 为空，这是因为这些样本在 Phase15 硬门控阶段已经拒绝，Phase18 按设计跳过双裁判，不属于字段生成失败。

## 数据质量检查

质量统计：
- 乱码命中数：0
- `assistant_answer` 对象串痕迹：0
- `case_user_query` 长度：最短 226，最长 289，平均 250.2 字符
- `assistant_answer` 长度：最短 381，最长 1163，平均 748.6 字符
- `grounded_audit_answer` 长度：最短 504，最长 2237，平均 819.9 字符
- 最终分数：最低 0，最高 93.6，平均 60.93

质量判断：
- `case_user_query` 已明显具备真实问诊场景，包含猪群阶段、场景规模、病程/时间线、症状、缺失信息和用户诉求。
- `assistant_answer` 更像兽医问诊 agent 的自然回答，能够回应现场情况、说明证据边界、提出补充信息和检测建议。
- `grounded_audit_answer` 保留审计追溯信息，有助于证明回答不是完全自由生成。
- accepted 样本整体可用于问诊 SFT 训练。
- review 样本适合进入人工复核或二次修复队列。
- rejected 样本主要是安全边界触发，应保留在审计或负例队列，不建议直接进入主训练集。

## 本次清理工作

已删除：
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/__pycache__`

保留：
- 本批次所有 CSV、JSONL、manifest 和阶段报告。这些产物是本次真实跑批和质量审查的证据，不应删除。

遍历产物时遇到历史目录 `issues/pytest_tmp` 权限拒绝，该目录与本批次结果无关，未强行处理，避免破坏未知历史测试环境。

## 结论

本次 40 条真实问诊 CSV 全流程已经跑通。Phase14 和 Phase18 均使用真实模型，八路并发有效。最终获得：

- 全量训练主 CSV：40 条
- 可直接训练的 train-ready CSV：23 条
- 需要复核：6 条
- 安全拒绝：11 条

字段完整性方面，核心训练字段和 accepted 样本的裁判/仲裁字段均完整有效。数据质量方面，未发现乱码、对象串痕迹或核心问诊字段缺失。当前主要问题不是 API 失效，而是仍有部分样本触发执行性内容硬门控，后续可进一步细分 Phase15 的执行性内容识别规则，降低合理问诊建议被误判的概率。
