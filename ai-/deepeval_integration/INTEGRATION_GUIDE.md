# DeepEval 最小对接说明

这份说明只回答一件事：如果后续要把 `deepeval_integration` 接到当前主流程，最小需要改哪些调用点、字段如何映射、哪些地方必须先做 smoke test 校准。

当前不修改主流程文件，只说明最小改法。

## 1. 最小需要改的调用点

主流程文件当前在：

- [master_chicken_data.py](C:\Users\admin\Desktop\每日内容\ai兽医问诊\鸡病数据合成系统\scripts\master_chicken_data.py)

如果只做最小接入，真正需要动的点只有 2 个。

### 调用点 A：替换评估入口

当前入口：

- `evaluate_case(case_data, judge_label, judge_config)`

当前内部依赖：

- `build_geval_prompt(case_data)`
- `call_api_with_backoff(...)`
- `extract_json_from_response(...)`
- `normalize_judge_result(...)`

最小替换方式：

1. 保留函数签名不变。
2. 在函数内部改为调用：

```python
from deepeval_integration import evaluate_case_with_deepeval

def evaluate_case(case_data, judge_label, judge_config):
    started_at = time.perf_counter()
    result = evaluate_case_with_deepeval(
        case_data=case_data,
        judge_config=judge_config,
        judge_label=judge_label,
        project_config=CONFIG,
    )
    elapsed = time.perf_counter() - started_at
    return result, elapsed
```

这样做的好处是：

- `process_single_case(...)` 不需要改调用姿势
- `judge_a_seconds` / `judge_b_seconds` 逻辑不需要改
- 其他 worker 正在改的批处理、日志、并发部分也不容易冲突

### 调用点 B：确认仲裁逻辑还吃得下新输出

当前仲裁触发依赖这几个字段：

- `total_score`
- `fatal_risk`

当前最终聚合依赖这几个字段：

- `diagnosis_accuracy`
- `pathology_logic`
- `prescription_safety`
- `data_quality`
- `total_score`
- `fatal_risk`

`deepeval_integration.evaluate_case_with_deepeval()` 已经直接输出这些字段，所以：

- `process_single_case(...)` 可以继续复用
- `select_final_metrics(...)` 可以继续复用
- `arbitrate_case(...)` 可以继续复用

也就是说，最小接入时通常 **不需要改仲裁函数本身**。

## 2. 可以先不动的调用点

以下逻辑可以保持不变：

- `generate_case(...)`
- `arbitrate_case(...)`
- `select_final_metrics(...)`
- `process_single_case(...)`
- CSV 写盘逻辑
- pilot / production 的任务调度逻辑

另外，这几个旧函数在最小接入阶段可以先保留，即使不再主用：

- `build_geval_prompt(...)`
- `normalize_judge_result(...)`

原因是这样更利于回滚，也不会和其他 worker 的改动打架。

## 3. 输入字段映射

`deepeval_integration` 目前假设的输入样本结构，和主流程生成结果一致：

```json
{
  "species": "鸡",
  "user_query": "...",
  "diagnosis": "...",
  "prescription": "...",
  "withdrawal_period": "...",
  "metadata": {
    "disease_name": "...",
    "severity": "low|medium|high",
    "scene_tags": ["..."]
  }
}
```

对应关系如下：

- `user_query`
  映射到 `LLMTestCase.input`
- `diagnosis + prescription + withdrawal_period + metadata`
  组合后映射到 `LLMTestCase.actual_output`
- `species`
  不直接参与 DeepEval 参数，但会保留在输出序列化文本中

## 4. 输出字段映射

`evaluate_case_with_deepeval()` 的目标是尽量兼容当前主流程裁判结果结构。

### 直接兼容的字段

- `judge_label`
- `judge_model`
- `diagnosis_accuracy`
- `pathology_logic`
- `prescription_safety`
- `data_quality`
- `total_score`
- `fatal_risk`
- `structured_pass`
- `summary`
- `strengths`
- `weaknesses`
- `final_label`

### 新增但主流程当前可忽略的字段

- `metric_reasoning`
  记录每个维度的文字理由，便于后续调试和人工复核。
- `avg_metric_score`
  便于做整体评分分布分析。

### 和旧实现的差别

旧实现是：

- 单次 prompt 直接返回一整个 JSON

新实现是：

- 每个维度分别通过一个 `GEval` metric 去评分
- 再在适配层汇总出主流程兼容字段

所以主流程看到的结果结构尽量不变，但评分来源已经切成了标准化的 `GEval` metric。

## 5. 必须先做 3 到 5 条 smoke test 的地方

正式替换前，至少要做一轮 3 到 5 条 smoke test，不建议直接切到 1000 条。

### 校准点 A：分数区间是否和当前逻辑对齐

风险原因：

- 不同版本的 `deepeval` / `GEval` 可能返回 `0-1`、`0-10` 或别的区间
- 当前适配器里已经做了分数归一化，但必须用真实模型输出确认一次

要检查：

- `diagnosis_accuracy` 是否稳定落在 `0-30`
- `pathology_logic` 是否稳定落在 `0-20`
- `prescription_safety` 是否稳定落在 `0-30`
- `data_quality` 是否稳定落在 `0-20`
- `total_score` 是否基本等于四维分数之和

### 校准点 B：`fatal_risk` 是否过松或过严

风险原因：

- 当前 `fatal_risk` 不是 DeepEval 原生字段，是适配层根据处方安全得分、理由文本、休药期缺失做的规则推断

要检查：

- 明显安全问题样本是否会被标记为 `True`
- 正常样本是否不会被误伤

建议：

- smoke test 里至少放 1 条明显高风险样本
- 至少放 1 条正常高质量样本

### 校准点 C：`structured_pass` 是否和现有黄金集标准一致

风险原因：

- 当前 `structured_pass` 也是适配层规则判断，不是直接由 `GEval` 给出

要检查：

- 字段齐全的样本是否稳定为 `True`
- 缺失 `withdrawal_period`、`metadata.disease_name`、`metadata.severity` 的样本是否会被打成 `False`

### 校准点 D：仲裁触发率是否异常变化

风险原因：

- 主流程仲裁阈值依赖 `total_score` 差值
- 如果 DeepEval 版本下分数分布更集中或更发散，仲裁率会变化

要检查：

- 与当前手写版本相比，3 到 5 条 smoke test 是否出现明显更高的仲裁率
- 若仲裁率异常，需要再看 `CONFIG["scoring"]["arbitration_threshold"]` 是否要调

### 校准点 E：耗时是否显著上升

风险原因：

- 新实现是 4 个维度分别调用 `GEval`
- 单次裁判耗时通常会高于当前“一次 prompt 返回整包 JSON”的方式

要检查：

- `judge_a_seconds`
- `judge_b_seconds`
- 在 pilot 小样本下的平均裁判耗时

如果耗时明显升高，建议先在 pilot 模式验证，再决定是否直接用于 production。

## 6. 推荐的 smoke test 样本组成

建议最少 3 条，最好 5 条。

### 样本 1：高质量标准样本

目标：

- 验证总分是否高
- 验证 `fatal_risk=False`
- 验证 `structured_pass=True`

### 样本 2：诊断逻辑一般但结构完整

目标：

- 验证 `pathology_logic` 会明显低于其他维度

### 样本 3：存在处方安全问题

目标：

- 验证 `prescription_safety` 拉低
- 验证 `fatal_risk=True`

### 样本 4：字段缺失样本

目标：

- 验证 `structured_pass=False`

### 样本 5：接近仲裁阈值的边界样本

目标：

- 验证两位裁判分差和仲裁触发逻辑是否合理

## 7. 建议的实际接入顺序

最稳妥的顺序是：

1. 先安装依赖并跑单条 CLI

```powershell
python -m deepeval_integration.cli --case-file sample_case.json --judge-key judge_a
```

2. 再把主流程里的 `evaluate_case(...)` 替换为 `evaluate_case_with_deepeval(...)`

3. 先跑 3 到 5 条 smoke test

建议：

- 用 `pilot` 模式
- 并发先降到 `1` 或 `2`

4. 确认字段、分数、仲裁率、耗时都正常后，再扩大到 10 到 30 条 pilot

5. 最后再考虑切 production

## 8. 一句话总结

如果只做最小对接，核心只需要替换主流程里的 `evaluate_case(...)` 实现，其他生成、仲裁、聚合、写盘逻辑都可以先不动；但正式切换前，必须先用 3 到 5 条真实样本做分数区间、风险标记、结构化通过率、仲裁率和耗时的 smoke test 校准。
