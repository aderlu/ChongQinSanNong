# 2026-05-14 全链路 API Key 池高可用改造记录

## 一、修改背景

项目 `config.json` 中已经配置了多 key 池，例如 `api.models.generator.api_keys`，并带有 `rotation_strategy`、`cooldown_seconds`、`max_consecutive_failures` 等高可用意图字段。

但真实 40 条八路并发执行中，Phase14 出现 17 条 fallback，错误包括：

- `APIConnectionError: Connection error.`
- `JSONDecodeError: Invalid control character`

说明此前代码虽然读取了 key 池，但没有真正做到失败后换 key、冷却、熔断和重试恢复。

## 二、修改前代码行为

### 2.1 Phase14 生成链路

文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/wiki_first_llm_client.py`

修改前行为：

- 读取 `api.models.generator.api_keys`。
- 使用 `RoundRobinKeyPool.next()` 做轮询。
- 每次请求只选择一个 key。
- 如果 `response_format` 报错，会去掉 `response_format` 再用同一个 key 重试一次。
- 如果连接失败、限流、超时、JSON 解析失败，不会换 key。
- 失败后 Phase14 外层直接 fallback。

实际效果：

- key 池只是负载分摊，不是高可用。

### 2.2 Phase18 裁判/仲裁链路

文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`

修改前行为：

- `llm_json_call()` 有 3 次 attempt。
- 每次 attempt 会轮询下一个 key。
- 但没有 key 冷却、失败计数、错误类型记录。
- 没有完整记录尝试过哪些 key。

实际效果：

- Phase18 比 Phase14 更接近高可用，但仍缺少健康状态和可观测性。

## 三、本次修改内容

### 3.1 共享 LLM 客户端高可用

修改文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/wiki_first_llm_client.py`

新增能力：

- 新增 `load_model_config()`，读取模型配置中的高可用参数。
- `RoundRobinKeyPool` 增加：
  - 连续失败计数。
  - key 冷却时间。
  - 跳过冷却中的 key。
  - `mark_success()`。
  - `mark_failure()`。
- `WikiFirstLLMClient.generate_json()` 增加：
  - 多次重试。
  - 每次失败后切换 key。
  - 失败 key 进入冷却。
  - 成功 key 清空失败状态。
  - 记录 `attempts`。
  - 记录 `api_key_indices_tried`。
  - 记录 `error_types`。
- 默认重试次数：
  - 如果配置 `max_retries`，使用配置值。
  - 否则使用 `max(3, min(key_pool_size, 8))`。

### 3.2 Phase14 生成链路可观测性

修改文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py`

新增输出字段：

- `api_call_attempts`
- `api_key_indices_tried`
- `api_error_types`

报告新增统计：

- `generation_error_type_counts`
- `api_attempt_counts`

效果：

- 后续可以直接从 Phase14 report 判断失败是否被重试恢复。
- 可以定位是否存在某些 key 频繁失败。

### 3.3 Phase18 裁判/仲裁链路高可用

修改文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`

新增能力：

- `_KEY_POOL_FAILURES`
- `_KEY_POOL_COOLDOWN_UNTIL`
- `mark_api_key_success()`
- `mark_api_key_failure()`
- `exception_type()`
- `next_api_key()` 跳过冷却中的 key。
- `llm_json_call()` 使用 key 池大小动态决定重试次数。
- 默认重试次数：
  - 若配置 `max_retries`，使用配置值。
  - 否则 `max(3, min(key_pool_size, 8))`。

新增 judge/arbiter 元数据：

- `judge_total_seconds`
- `arbiter_total_seconds`
- `api_key_indices_tried`
- `api_error_types`

## 四、解决的问题

本次改造解决：

- 单 key 失败后直接 fallback 的问题。
- key 池只轮询不容错的问题。
- 失败 key 反复被选中的问题。
- 生成链路和裁判链路缺少 key 尝试记录的问题。
- Phase14 与 Phase18 高可用能力不一致的问题。

## 五、预计效果

预期在下一次 8 并发真实调用中：

- `APIConnectionError` 不会立刻导致样本 fallback，而会换 key 重试。
- 单个坏 key 会进入冷却，避免短时间反复失败。
- Phase14 fallback 数量应明显下降。
- Phase18 裁判/仲裁调用稳定性应提升。
- 报告中可以看到每条样本实际尝试次数和 key 索引。

## 六、未解决风险

仍需注意：

- 如果上游服务整体不可用，多 key 也无法恢复。
- 如果所有 key 共享同一服务侧限流，多 key 效果有限。
- JSON 内容质量错误可以重试，但不能保证模型每次都输出合格 JSON。
- 目前没有持久化 key 健康状态，冷却状态只在当前进程有效。
- 没有单独的 key 健康巡检报告，后续可增加。

## 七、验证结果

已执行编译检查：

```text
python -m py_compile wiki_first_llm_client.py phase14_generate_two_stage_samples.py phase18_dual_judge_and_arbitrate.py
```

结果：

```text
通过，无语法错误。
```

## 八、后续建议

建议下一步重新跑一个小批次，例如 8 并发 10 条，检查：

- fallback 是否下降。
- `api_attempt_counts` 是否出现 2 次或更多重试恢复。
- `api_key_indices_tried` 是否覆盖多个 key。
- Phase18 是否仍存在大量 0 分和结构化解析异常。

只有小批次确认高可用有效后，再继续执行 40 条或更大批次。
