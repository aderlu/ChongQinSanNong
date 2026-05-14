# 2026-05-13 Phase17 Real LLM Two-Stage Generation

## 背景与原问题

Phase14 原脚本 `phase14_generate_two_stage_samples.py` 只支持 deterministic mock 生成：

- Stage 1 直接把 `must_include_claims` 串接成草稿答案。
- Stage 2 直接把 claim 与 citation 锚点拼接成 grounded answer。
- `summary.mode` 固定写死为 `deterministic_dry_run_mock`。
- 样本中没有 `generation_mode`、`generation_model`、`prompt_version`、`request_ref`、`response_ref` 等可追踪字段。

这会带来两个问题：

- 无法切换到真实 LLM 两段式主流程，Phase14 只能做模板拼接，不能验证真实提示词和真实生成链路。
- 即使后续接入真实 API，也缺少请求级追踪信息，难以审计某条样本由哪个模式、哪个模型、哪次请求生成。

## 原代码怎样

原始 Phase14 的主逻辑是：

1. 读取 Phase13 skeleton 与 Phase12 plan。
2. `build_stage_answers()` 根据 `must_include_claims` 构造 deterministic 的 `stage_1_draft` 和 `stage_2_grounded`。
3. 输出 `two_stage_samples_YYYYMMDD.jsonl`。
4. 写出 Phase14 summary/report。

原实现优点是稳定，但它没有真实 LLM 模式，也没有请求追踪能力。

## 本次修改内容

本次仅修改了允许范围内的文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase14_generate_two_stage_samples.py`
- 新增 `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_first_llm_client.py`

### 1. 为 Phase14 增加模式切换

新增命令行参数：

```bash
--mode dry-run|real-api
```

行为如下：

- `dry-run`：保留原 deterministic mock 逻辑，作为默认模式。
- `real-api`：调用真实 LLM 两段式生成；若单条请求失败，则自动回退到 deterministic seed，避免破坏既有输出结构。

### 2. 保留并继续使用 Phase13 skeleton 约束

真实生成提示词中显式注入并继续依赖以下字段：

- `must_include_claims`
- `must_not_include`
- `required_citations`
- `hard_gate_profile`
- `evidence_anchors`

也就是说，real-api 不是绕开 Phase13，而是把 Phase13 的 skeleton 当作真实生成的硬边界输入。

### 3. 引入两段式真实 LLM 包装

新增 `wiki_first_llm_client.py`，负责：

- 解析 API Key（支持 `WIKI_FIRST_API_KEY`、`NONELINEAR_API_KEY`、`OPENAI_API_KEY`）
- 调用 OpenAI 兼容 `chat.completions`
- 提取 JSON 响应
- 返回不含密钥的请求追踪信息

Phase14 主脚本只负责：

- 组装 prompt
- 调用 stage 1 / stage 2
- 把返回值与 deterministic seed 做契约对齐
- 在失败时保底回退

### 4. 为样本增加追踪字段

每条生成样本新增：

- `generation_mode`
- `generation_model`
- `prompt_version`
- `request_ref`
- `response_ref`

说明：

- 不写出 API key 或任何密钥。
- `request_ref` / `response_ref` 采用 stage 维度对象结构，便于追踪两段式调用。
- dry-run 模式也会产出可识别的 dryrun ref，保证字段齐全。

### 5. 保持上下游契约不变

保留了 Phase15/16 已依赖的核心字段与结构：

- `sample_id`
- `plan_id`
- `skeleton_id`
- `question`
- `stage_1_draft`
- `stage_2_grounded`
- `evidence_anchors`
- `ability_layer`
- `risk_class`
- `source_trust`
- `evidence_coverage`

因此 Phase15/16 可以继续直接消费，不需要修改它们的脚本。

### 6. 全部使用 UTF-8

新增/修改文件均以 UTF-8 写入，避免默认编码带来的乱码问题。

## 解决了什么

这次改动解决了以下问题：

- 让 Phase14 从“只能 deterministic mock”升级为“dry-run / real-api 可切换”的两段式主流程。
- 让真实生成继续被 Phase13 skeleton 严格约束，避免放飞模型。
- 让每条样本具备生成模式、模型、提示词版本、请求引用、响应引用等可审计能力。
- 让真实模式失败时仍能保底输出 deterministic seed，不至于破坏批处理稳定性。

## 预期效果

预期运行效果：

1. 默认执行仍是 dry-run，兼容当前流水线。
2. 指定 `--mode real-api` 后，Phase14 会改为真实两段式生成。
3. 无论 dry-run 还是 real-api，输出结构都保持 Phase15/16 可消费。
4. 真实模式中每条样本都能追踪生成模式、模型、prompt 版本和两段请求引用。
5. 不会在输出中泄露任何密钥。

## 如何验证

本次已执行的最小验证：

### 1. 语法检查

```bash
py -m py_compile D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase14_generate_two_stage_samples.py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_first_llm_client.py
```

结果：通过。

### 2. Dry-run 回归

```bash
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase14_generate_two_stage_samples.py --wiki-root D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative --mode dry-run --limit 3 --date 20260513
```

结果：

- 成功生成 3 条样本
- `mode = dry-run`
- `generation_model = deterministic-mock`
- `missing_anchors = []`
- `missing_grounded_citations = []`

### 3. Phase15 兼容性验证

```bash
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase15_fact_level_evaluate_samples.py --wiki-root D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative --generated D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\generated_samples\two_stage_samples_20260513.jsonl --limit 3 --date 20260513
```

结果：3/3 accepted，说明新增字段未破坏 Phase15 契约。

### 4. Phase16 兼容性验证

```bash
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase16_export_layered_training_sets.py --wiki-root D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative --generated D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\generated_samples\two_stage_samples_20260513.jsonl --evaluated D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\evaluated_samples\fact_evaluated_samples_20260513.jsonl --date 20260513
```

结果：成功导出分层训练集，说明 Phase16 契约未受影响。

## 后续使用建议

真实模式可用示例：

```bash
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase14_generate_two_stage_samples.py --wiki-root D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative --mode real-api --model hunyuan-turbos-20250926 --date 20260513
```

运行前需要配置任一 API Key 环境变量：

- `WIKI_FIRST_API_KEY`
- `NONELINEAR_API_KEY`
- `OPENAI_API_KEY`

本次不涉及 Phase18/19，也未修改它们的任何文件。
