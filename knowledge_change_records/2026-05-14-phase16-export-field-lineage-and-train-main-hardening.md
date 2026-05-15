# Phase16 导出字段与留痕加固说明

## 背景问题
之前的 Phase16 导出虽然已经开始保留 `case_context`、`case_user_query`、`assistant_answer`、`grounded_audit_answer`，但仍存在三类问题：

1. 训练主 CSV 的“真实问诊字段”与“审计字段”还不够清晰。
2. `final_*`、裁判模型、裁判耗时、仲裁原因等字段虽然部分可导出，但缺少明确的字段来源说明，不利于汇报和追溯。
3. 若上游 Phase18 结构略有差异，部分最终分数字段可能依赖单一路径，导致导出结果不够稳健。

## 本次修改

### 1. 强化训练主 CSV 的字段覆盖
训练主 CSV 继续保留并明确输出以下核心问诊字段：

- `case_context`
- `case_user_query`
- `user_query`
- `assistant_answer`
- `grounded_audit_answer`

同时补充 Phase15 / Phase18 / 双裁判 / 仲裁的完整链路字段：

- `phase15_fact_passed`
- `phase15_hard_gate_passed`
- `phase18_semantic_decision`
- `phase18_judge_status`
- `phase18_judge_a_status`
- `phase18_judge_b_status`
- `phase18_arbiter_status`
- `judge_a_*`
- `judge_b_*`
- `arbiter_*`
- `final_*`

### 2. 增加最终分数字段的容错来源
新增 `final_metrics_from_phase18()`，使最终分数按以下顺序回退：

1. `semantic_final_metrics`
2. `arbiter_result`
3. 双裁判保守回退值

这样可避免某些样本因 Phase18 结构差异而导出空分。

### 3. 增加字段来源说明
新增 `field_source_map`，明确说明主训练 CSV 各类字段来源于哪个阶段，方便审查、汇报和后续排障。

## 解决了什么

- 让主训练 CSV 变成“真实问诊样本 + 证据审计 + 双裁判仲裁”一体化结果，而不是仅有问答文本。
- 降低因上游字段结构变化导致的空字段风险。
- 让每个字段的来源链路更容易汇报和核验。

## 预期效果

- 更容易确认哪些样本可以直接用于微调，哪些样本属于 review / audit / rejected。
- 更方便对外说明 CSV 中每个分数字段来自 Phase15、Phase18 的哪一环。
- 训练主 CSV 的可追溯性更强，适合企业级归档和后续复盘。

## 验证建议

建议运行：

```powershell
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
py -3 -m py_compile D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py
py -3 D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py --wiki-root D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative --date 20260514_check --evaluated <Phase15结果> --generated <Phase14结果> --phase18 <Phase18结果>
```

重点核对：

- CSV 中 `case_context/case_user_query/assistant_answer/grounded_audit_answer` 非空。
- `judge_a_*`、`judge_b_*`、`arbiter_*` 分数字段非空且和 Phase18 对应。
- `final_*` 分数和标签可追溯到 Phase18 或保守回退。
- `field_source_map` 存在，便于汇报。
