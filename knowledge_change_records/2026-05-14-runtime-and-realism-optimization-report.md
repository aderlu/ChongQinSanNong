# 2026-05-14 运行耗时与真实问诊数据质量优化记录

## 背景

上一轮八路并发生成 40 条问诊 CSV 的总耗时达到约 22 分 28 秒。更重要的是，样本中出现了不真实的问答形式：用户问题包含 `DIS-001`、内部知识库问题、`请你按兽医问诊 agent 的方式回答` 等提示词痕迹；助手回答直接暴露 `[source=...]`、`[fact=...]`、`[page=...]` 等审计锚点。这类数据不适合作为真实兽医问诊 agent 的主训练样本。

本次优化同时处理两个问题：
- 降低全链路耗时。
- 让主训练字段更像真实兽医问诊，只把知识库作为约束和审计依据。

## 耗时原因分析

### Phase14 生成阶段

上一轮 Phase14 耗时约 487.80 秒。主要原因：

1. 每条样本调用两次真实模型：stage1 草稿一次，stage2 grounded answer 一次。
2. 40 条样本等价于约 80 次真实模型调用。
3. prompt 中包含完整 skeleton、anchors、required citations、case context 等，输入较长。
4. `max_tokens=3200`，单次输出上限较大。
5. 中转站和模型响应本身存在波动，即使八路并发也会被最慢请求拖尾。

### Phase18 裁判与仲裁阶段

上一轮 Phase18 耗时约 283.99 秒。主要原因：

1. 29 条样本进入双裁判。
2. 每条样本至少调用 Judge A 和 Judge B。
3. 上一轮 29 条全部触发仲裁，额外增加 29 次 arbiter 调用。
4. 因此 Phase18 约等价于 58 次裁判调用 + 29 次仲裁调用。
5. 裁判 prompt 包含样本、审计答案、证据锚点和评分体系，输入也较长。

### Phase13、Phase15、Phase16

这些阶段基本不是瓶颈：
- Phase13 通常小于 2 秒。
- Phase15 通常小于 2 秒。
- Phase16 通常小于 2 秒。

## 已实施的性能优化

### 优化一：Phase14 从双调用改为单调用

修改文件：

`tools/pipeline/phase14_generate_two_stage_samples.py`

修改前：
- 每条样本调用 stage1 LLM。
- 再调用 stage2 LLM。
- 40 条约 80 次生成调用。

修改后：
- stage1 和 grounded audit answer 由确定性骨架提供。
- 真实 LLM 只生成 `clinical_answer`。
- 40 条约 40 次生成调用。

预期效果：
- Phase14 调用次数减少约 50%。
- 烟测 4 条 Phase14 耗时约 12.97 秒。
- 按比例估算，40 条 Phase14 有机会从约 488 秒降到约 130 到 180 秒，实际仍取决于中转站波动。

### 优化二：Phase18 减少无必要仲裁

修改文件：

`tools/pipeline/phase18_dual_judge_and_arbitrate.py`

修改前：
- 大量样本因为轻微分歧或 Phase15 warning 触发仲裁。
- 29 条进入双裁判后，29 条全部仲裁。

修改后：
- 如果 Judge A 和 Judge B 都是 `pass`，无致命风险，分差未超过阈值，且没有硬风险分歧，则跳过仲裁。
- 保留高风险样本、致命风险、标签分歧、明显分差和安全边界分歧的仲裁。

预期效果：
- 降低不必要 arbiter 调用。
- 不牺牲高风险样本的安全兜底。

### 优化三：保留高风险强仲裁

没有为了速度取消 `high_risk_sample` 强制仲裁。原因：
- 猪病问诊涉及用药、调运、上报、扑杀等高风险内容。
- 高风险样本即使两个裁判通过，也应该保留仲裁兜底。
- 该策略牺牲部分速度，但更符合安全和企业级审计要求。

## 已实施的真实性优化

### 问题一：用户问题像知识库检索，不像真实问诊

典型错误：

```text
请你按兽医问诊 agent 的方式回答：围绕DIS-001，猪场现场咨询：围绕猪腺病毒感染，现有资料目前能确认哪些可靠信息...
```

修复文件：

`tools/pipeline/consultation_case_variables.py`

修复内容：
- 重建正常 UTF-8 中文问诊变量库。
- 用户问题只保留养殖户真实表达。
- 不再把 `DIS-001`、内部 question、wiki 检索目标写入 `case_user_query`。
- 用户问题变成类似：

```text
老师您好，我们这边是分区管理的规模场，一批哺乳母猪连续两个批次都有类似情况，现在主要是有个别死亡、精神差、吃料下降。日龄和批次记录不全、发病比例和死亡数还没统计清楚、免疫记录一时找不到，心里没底，想先排一下可能方向。您看我现在应该先从哪些方面排查？
```

### 问题二：助手回答直接暴露审计引用

典型错误：

```text
猪腺病毒感染属于病毒性疾病[source=SRC-0001][rule=RC-CITATION-001]...
```

修复文件：

`tools/pipeline/phase14_generate_two_stage_samples.py`

修复内容：
- `clinical_answer` 不再要求展示 `[source=...]`、`[fact=...]`、`[page=...]`、`[rule=...]`。
- 主训练答案只输出自然问诊回复。
- 证据引用保留在 `grounded_audit_answer`、`evidence_anchors`、Phase15 和 Phase18 审计字段中。
- 新增自然化清理逻辑，防止主回答中残留引用锚点或实体编号。

### 问题三：Phase15 仍要求主回答带 citation

修复文件：

`tools/pipeline/phase15_fact_level_evaluate_samples.py`

修复内容：
- citation 完整性检查改为检查 `stage_2_grounded.answer`，即审计答案。
- 主训练答案 `clinical_answer` 不再因为没有 source/fact/page 而被拒绝。

## 验证结果

### Phase14 真实烟测

批次：`20260514_perf_natural_smoke4_v1`

- 样本数：4
- 并发：4
- 耗时：约 12.97 秒
- fallback：0
- missing anchors：0
- missing grounded citations：0

抽查结果：
- `case_user_query` 无 DIS 编号。
- `case_user_query` 无内部 wiki 检索问题。
- `clinical_answer` 无 source/fact/page/rule 引用。
- `grounded_audit_answer` 保留 citation。

### Phase15/Phase18 烟测

批次：`20260514_perf_natural_smoke4_v2`

- Phase15：4 条全部 accepted。
- Phase18：4 条进入双裁判。
- Phase18 accepted：3
- Phase18 review：1
- Phase18 rejected：0
- Phase18 耗时：约 70.16 秒

说明：
- 自然主回答不再因为缺少 citation 被 Phase15 误拒。
- 高风险上下文仍会触发仲裁，这是安全策略，不是错误。

## 后续可选优化

### 可选一：裁判模型分层

对低风险样本使用更快模型或规则 + 单裁判，对高风险样本继续双裁判 + 仲裁。

预期收益：
- Phase18 调用量可进一步下降。

风险：
- 低风险样本的误放行概率略增，需要抽检验证。

### 可选二：按风险决定是否仲裁

低风险样本在 Judge A/B 都 pass 且分差小于阈值时跳过仲裁；高风险样本保留仲裁。

当前已部分实现。

### 可选三：限制裁判输入长度

Phase18 可只传：
- `case_user_query`
- `clinical_answer`
- `grounded_audit_answer` 摘要
- evidence anchor 摘要
- Phase15 flags

而不是传完整样本对象。

预期收益：
- 降低模型处理时长和超时概率。

### 可选四：40 条正式批次使用 `--max-tokens 1800`

本次烟测使用 `max_tokens=1800` 已能稳定生成自然问诊答案。

预期收益：
- 降低 Phase14 输出耗时。

风险：
- 极少数复杂样本回答可能略短，需要监控 `assistant_answer` 长度。

## 结论

上一轮 22 分 28 秒主要来自真实模型调用次数过多和 Phase18 全量仲裁。当前已经完成两项核心优化：

1. Phase14 从每条两次 LLM 调用降为每条一次 LLM 调用。
2. 主训练问答不再暴露知识库结构和引用锚点，知识库只作为约束、审计和裁判依据。

烟测显示：
- 生成速度明显改善。
- 问诊输入和回答更接近真实兽医场景。
- Phase15/18 链路仍能正常工作。

建议下一步重新跑 40 条正式批次，使用：

```powershell
--parallel 8 --max-tokens 1800
```

并继续输出单一综合 CSV。
