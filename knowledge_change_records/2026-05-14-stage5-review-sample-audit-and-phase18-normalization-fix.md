# 2026-05-14 阶段五 review 样本抽查与 Phase18 归一化修复记录

## 一、任务背景

阶段五小批次 `20260514_stage5_small10_fix3` 首次完成后，Phase16 结果为：

- accepted: 0
- review: 8
- rejected: 2

因此按要求先抽查 8 条 review 样本，判断问题来自生成质量不足，还是裁判/仲裁阈值或结构解析问题。

## 二、抽查结论

抽查 8 条 review 后发现：

- 多数主回答具备真实问诊风格，能回应用户场景、说明不确定性、追问关键信息、给出低风险现场建议，并避免剂量/疗程/休药期等线上越界内容。
- Judge B 多条给出 78.5、87.5、93、97 等高分，并在文字评价中明确认为样本可训练或高质量。
- Judge A 或 Arbiter 多条出现 `total_score=0.0`、`structured_pass=false`，但无 fatal risk、无 hard fail。
- 多条仲裁结果的 `main_issues` 为“无”或轻微表达问题，却仍被归为 repairable。

因此主要问题不是生成质量整体不足，也不是单纯阈值过严，而是 Phase18 对 LLM 裁判/仲裁输出结构的兼容和归一化不足。

## 三、发现的具体代码问题

目标文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`

问题表现：

1. 裁判模型有时把分数写在 `scores`、`dimensions`、中文维度名或顶层字段中，而原代码只读取 `dimension_scores` 的英文键。
2. 裁判模型有时省略 `weighted_total_score/total_score`，但给出了各维度分；原代码没有本地重算总分。
3. 裁判模型有时省略 `structured_pass`，原代码默认 `False`，导致高分样本被强制降为 repairable。
4. 仲裁模型有时给出明确文字结论和轻微问题，但没有返回可解析总分；原代码按 0 分处理，导致样本被误判为 repairable。

## 四、本次修改

### 4.1 增强维度分归一化

新增：

- `DIMENSION_ALIASES`
- `_numeric()`
- `_normalized_key()`
- `_score_from_mapping()`
- `_candidate_score_mappings()`

支持从以下形式读取维度分：

- `dimension_scores`
- `scores`
- `score`
- `dimensions`
- `dimension_score`
- 顶层字段
- 中文维度名，如“医学正确性”“问诊完整性”“上下文一致性”等

### 4.2 本地重算总分

新增：

- `score_payload_total()`

逻辑：

- 优先读取模型返回的 `weighted_total_score/final_total_score/total_score/score`
- 如果缺失，则用归一化后的维度分本地求和

### 4.3 推断 structured_pass

新增：

- `infer_structured_pass()`

逻辑：

- 模型显式返回 `structured_pass` 时尊重模型输出
- 未返回时，如果无 hard fail、总分大于 0、且维度分存在，则推断为 `True`
- 避免高分但缺字段的样本被默认判为结构失败

### 4.4 仲裁缺分保护

修改 `normalize_llm_arbiter_payload()`：

- 当仲裁无硬伤、无有效分数、但双裁判分数可用时，用双裁判的保守分作为仲裁分。
- 这不是放宽安全标准，而是防止仲裁输出结构缺字段时被误当成 0 分样本。

## 五、复判结果

### rejudge1

批次：

`20260514_stage5_small10_fix3_rejudge1`

结果：

- accepted: 5
- review: 3
- rejected: 2

说明裁判维度归一化修复后，原 8 条 review 中已有 5 条恢复为 accepted。

### rejudge2

批次：

`20260514_stage5_small10_fix3_rejudge2`

结果：

- accepted: 8
- review: 0
- rejected: 2

Phase16 导出结果：

- accepted: 8
- review: 0
- rejected: 2
- `sft_l1_retrieval_grounded.jsonl`: 8
- `sft_l1_l4_borderline.jsonl`: 8
- `training_set_rejected_queue.jsonl`: 2

## 六、判断结论

本次抽查结论：

1. 8 条 review 样本多数生成质量可用。
2. 原先全部进入 review 的主因是 Phase18 裁判/仲裁输出归一化缺陷。
3. 修复后 8 条 Phase15 accepted 样本全部进入 Phase18 accepted。
4. 2 条 rejected 是 Phase15 对高风险/监管边界样本的硬门控拒绝，属于真实安全门控，不建议放宽。

因此可以进入 40 条正式批次，但应继续监控：

- Phase15 高风险样本拒绝比例
- Phase18 仲裁触发比例
- accepted/train-ready 占比
- 是否再次出现 0 分非 invalid、main_issues 字符拆分、repairable 进入 main_sft

## 七、后续动作

基于 rejudge2 的结果，继续执行 40 条正式批次验证。
