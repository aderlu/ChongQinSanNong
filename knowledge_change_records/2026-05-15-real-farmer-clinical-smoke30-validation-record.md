# 2026-05-15 真实养殖户问诊整改后 30 条 smoke 验证记录

## 一、运行目标

本次 smoke 用于验证 `user_query` 和 `assistant_answer` 整改后的真实问诊质量，不作为正式 500 条验收。

Run ID：

```text
20260515_real_farmer_clinical_smoke30_v1
```

运行规模：

```text
wiki: 30 条
no_wiki: 30 条
metadata_only: 30 条
standard comparison: 90 条
```

## 二、运行说明

首次直接运行：

```text
run_baseline_experiment.py --run-id 20260515_real_farmer_clinical_smoke30_v1 --limit 30 --parallel 3 --stage all
```

出现一个 smoke 特有流程问题：

- `limit=30` 无法覆盖 runtime manifest 中全部 73 个疾病。
- `prepare()` 触发 coverage failed。
- 因 coverage failed，`case_seeds` 未生成。
- 后续 `wiki_group` 和 `no_wiki_group` 初次标准化/生成出现 0 行。

处理方式：

- 手动补跑 `build_case_seeds.py`，生成 30 条 case seeds。
- 使用已有的 30 条 Wiki naturalized 输出重新标准化 Wiki group。
- 顺序补跑 `no_wiki`、`metadata_only`、`wiki_baseline` 和 `compare`。

该问题不影响本次内容质量判断，但说明 smoke 流程需要单独支持“非全疾病覆盖的小批量验证”，不能套用正式 500/全覆盖逻辑。

## 三、结构结果

最终产物：

```text
exports/baseline_validation/comparisons/baseline_comparison_standard_20260515_real_farmer_clinical_smoke30_v1.csv
exports/baseline_validation/comparisons/baseline_comparison_wiki_20260515_real_farmer_clinical_smoke30_v1.csv
exports/baseline_validation/comparisons/baseline_comparison_no_wiki_20260515_real_farmer_clinical_smoke30_v1.csv
exports/baseline_validation/comparisons/baseline_comparison_metadata_only_20260515_real_farmer_clinical_smoke30_v1.csv
```

结构检查：

```text
standard comparison: 90 rows, 54 fields, passed
wiki: 30 rows
no_wiki: 30 rows
metadata_only: 30 rows
```

注意：`compare_groups.py` 原生只输出 standard 总表。本次为便于 QA gate 分组检查，从 standard 表按 `baseline_group` 拆出了三份 group CSV。

## 四、QA realism gate 结果

报告文件：

```text
exports/baseline_validation/reports/qa_realism_gate_wiki_20260515_real_farmer_clinical_smoke30_v1.json
exports/baseline_validation/reports/qa_realism_gate_no_wiki_20260515_real_farmer_clinical_smoke30_v1.json
exports/baseline_validation/reports/qa_realism_gate_metadata_only_20260515_real_farmer_clinical_smoke30_v1.json
```

### 4.1 Wiki 组

```text
passed = false
rows = 30
query_hard_fail_rate = 0.0%
professional_leakage_rate_user_query = 0.0%
answer_hard_fail_rate = 36.67%
generic_answer_rate = 0.0%
clinical_judgement_rate = 96.67%
differential_rate = 63.33%
field_action_rate = 100.0%
duplicate_user_query_extra_count = 0
duplicate_assistant_answer_extra_count = 0
user_query_length_avg = 137.87
assistant_answer_length_avg = 516.43
```

结论：

- `user_query` 整改有效，旧问题基本清除。
- `assistant_answer` 明显改善，已有临床判断和现场动作。
- 未通过主要因为 `differential_rate` 只有 63.33%，部分回答没有明确写出 2-3 个鉴别方向。

### 4.2 No-Wiki 组

```text
passed = false
rows = 30
query_hard_fail_rate = 0.0%
professional_leakage_rate_user_query = 0.0%
answer_hard_fail_rate = 93.33%
generic_answer_rate = 0.0%
clinical_judgement_rate = 10.0%
differential_rate = 50.0%
field_action_rate = 100.0%
duplicate_user_query_extra_count = 0
duplicate_assistant_answer_extra_count = 0
user_query_length_avg = 75.87
assistant_answer_length_avg = 412.57
```

结论：

- `user_query` 无旧模板和专业泄漏，但平均偏短。
- 回答有现场动作，但临床判断触发率很低。
- 部分 LLM 输出了 JSON/dict 风格内容，`assistant_answer` 未被规范化成自然语言。

### 4.3 Metadata-only 组

```text
passed = false
rows = 30
query_hard_fail_rate = 0.0%
professional_leakage_rate_user_query = 0.0%
answer_hard_fail_rate = 100.0%
generic_answer_rate = 0.0%
clinical_judgement_rate = 3.33%
differential_rate = 60.0%
field_action_rate = 100.0%
duplicate_user_query_extra_count = 0
duplicate_assistant_answer_extra_count = 0
user_query_length_avg = 73.9
assistant_answer_length_avg = 393.63
```

结论：

- `user_query` 无旧模板和专业泄漏，但平均偏短。
- 回答未稳定命中“临床判断”规则。
- 部分回答包含编号清单或 JSON/dict 风格，尚未达到主训练回答标准。

## 五、质量变化判断

### 已解决

1. 用户问题中的旧模板污染已消除。

本次三组：

```text
query_hard_fail_rate = 0.0%
professional_leakage_rate_user_query = 0.0%
```

说明“还需要我补哪些信息、实验室检测、剖检、发病比例、检测结果”等问题已经从 `user_query` 中清除。

2. Wiki 组回答质量明显优于旧表。

旧 500 条 Wiki 表：

```text
clinical_judgement_rate = 2.2%
professional_leakage_rate_user_query = 100.0%
```

新 smoke Wiki 组：

```text
clinical_judgement_rate = 96.67%
professional_leakage_rate_user_query = 0.0%
```

### 尚未解决

1. Wiki 组鉴别方向不足。

部分回答虽然有临床判断和现场动作，但没有稳定写出“需要和哪些病因方向区分”。

2. B/C 组回答自然语言规范化不足。

发现：

```text
no_wiki dict_like_answers = 13/30
metadata_only dict_like_answers = 6/30
metadata_only numbered_answers = 6/30
```

这说明 `generate_baseline_groups.py` 的 `normalize_llm_payload()` 对 LLM 返回的结构化字段处理不够，直接把 dict/list 字符串写入了 `assistant_answer`。

3. B/C 组问题偏短。

`user_query_length_avg` 约 74-76 字，虽然自然，但比目标 gold 风格略短，场景信息不足。

## 六、下一步修复建议

### 6.1 修复 B/C 组结构化回答泄漏

修改：

```text
tools/pipeline/baseline_validation/generate_baseline_groups.py
```

重点：

- `normalize_llm_payload()` 如果收到 dict/list，应把：
  - preliminary_assessment
  - basis
  - differential_directions
  - on_site_actions
  - follow_up_questions
  合成为自然中文段落。
- 禁止把 Python dict 字符串直接写入 `clinical_answer`。

### 6.2 强化 B/C 组 prompt

要求 LLM 只返回：

```json
{
  "question": "...",
  "clinical_answer": "自然中文完整回答"
}
```

如果返回结构化对象，后处理必须合成自然语言。

### 6.3 强化 Wiki 组鉴别方向

修改：

```text
phase14_generate_two_stage_samples.py
clinical_generation_user_prompt()
```

增加硬要求：

```text
clinical_answer 必须显式包含“鉴别上/需要和/优先区分”之一，并给出 2-3 个方向。
```

### 6.4 Smoke 流程修复

修改：

```text
run_baseline_experiment.py
```

增加 smoke 模式或参数：

```text
--allow-partial-coverage
```

用于 30 条/小批量验证时跳过 73 疾病全覆盖硬检查，但正式 500 仍保持全覆盖。

## 七、最终结论

本次 30 条 smoke 结论：

```text
结构跑通：通过
user_query 质量整改：通过
assistant_answer 质量整改：部分通过
三组 QA realism gate：未通过
是否可以直接跑 500 条：不建议
```

建议先修复 B/C 组 dict 泄漏、Wiki 组鉴别方向不足、smoke partial coverage 流程，再跑第二轮 30 条 smoke。
