# DeepEval Integration

这个目录把当前项目里“手写 G-Eval prompt + JSON 解析”的评估层，整理成了基于 `deepeval` 的独立封装。

## 当前覆盖

- `diagnosis_accuracy`
- `pathology_logic`
- `prescription_safety`
- `data_quality`

## 目录说明

- `config.py`
  读取项目 `config.json`，并把四个评分维度映射为 DeepEval `GEval` metric 定义。
- `llm.py`
  提供 OpenAI-compatible API 到 `DeepEvalBaseLLM` 的适配器。
- `evaluator.py`
  提供 `ChickenCaseDeepEvalEvaluator` 和 `evaluate_case_with_deepeval()`，输出格式尽量对齐当前主流程的裁判结果结构。
- `cli.py`
  单条样本验证入口。

## 最小运行方式

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 准备一个单条样本 JSON，例如：

```json
{
  "species": "鸡",
  "user_query": "我这批 35 日龄肉鸡这两天精神差，呼吸道声音重，还拉黄绿色粪便，应该怎么办？",
  "diagnosis": "初步考虑新城疫并发细菌感染，需要结合死亡率和免疫程序综合判断。",
  "prescription": "建议先隔离病鸡，使用敏感抗菌药物控制继发感染，并补充电解多维。",
  "withdrawal_period": "遵循所用药物说明书的休药期要求。",
  "metadata": {
    "disease_name": "新城疫",
    "severity": "high",
    "scene_tags": ["呼吸道", "腹泻"]
  }
}
```

3. 运行评测

```bash
python -m deepeval_integration.cli --case-file sample_case.json --judge-key judge_a
```

## 与现有主流程的最小对接方式

当前不修改 `master_chicken_data.py`。后续只需要把原来的：

- `build_geval_prompt(...)`
- `evaluate_case(...)`

替换为：

```python
from deepeval_integration import evaluate_case_with_deepeval

judge_result = evaluate_case_with_deepeval(
    case_data=case_data,
    judge_config=judge_config,
    judge_label="judge_a",
    project_config=CONFIG,
)
```

返回结果会继续包含当前主流程所需的这些关键字段：

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
- `judge_model`
