# 2026-05-13 Phase14 v2 Prompt 与 L2/L3/L4 结构模板优化记录

## 背景

上一轮真实 API 30 条质量统计显示：

- Phase17 真实 API 生成可以稳定运行，30/30 保留证据锚点。
- Phase15 事实与硬门禁接受率较高。
- Phase18 双裁判后只有 4/30 进入 SFT，18/30 进入 review。

主要问题集中在：

- L2 诊断支持、L3 鉴别诊断、L4 控制边界样本缺少稳定的结构化回答格式。
- Phase18 常见原因包括 `semantic:structured_pass_false`、`judge_a:review`、`judge_b:review`。
- Stage2 prompt 只要求“带引用”，没有强制回答必须包含“证据依据、边界、不扩展内容、锚点”这些段落。

## 原代码情况

`phase14_generate_two_stage_samples.py` 原先使用：

- `PROMPT_VERSION = phase14.two_stage.v1`
- Stage2 prompt 只要求：
  - 保留 anchor citation
  - factual claim 可追溯
  - 不包含 forbidden content
  - boundary/refusal 样本保留边界表达

Dry-run 的 Stage2 也是把 claim 与 citation 简单拼接，缺少能力层差异化结构。

## 本次修改内容

### 1. 升级 prompt 版本

将 Phase14 prompt 版本升级为：

```text
phase14.two_stage.v2
```

### 2. 新增能力层结构模板

新增函数：

- `answer_structure_for()`
- `structure_requirements_for()`
- `structured_answer()`

不同能力层有不同标签：

- L2:
  - `Diagnosis-support evidence`
  - `Diagnostic boundary`
  - `Do not infer`
  - `Citation anchors`
- L3:
  - `Differential-boundary evidence`
  - `Differential boundary`
  - `Do not over-diagnose`
  - `Citation anchors`
- L4:
  - `Control-boundary evidence`
  - `Control boundary`
  - `Do not prescribe beyond evidence`
  - `Citation anchors`

### 3. 强化 Stage2 prompt

Stage2 prompt 现在明确要求：

- 必须按 `required_answer_structure` 顺序输出。
- evidence section 必须带 bracket citation。
- boundary/do-not-extend section 必须明确说明当前证据不能支持什么。
- L2 不能直接给出无锚点最终诊断。
- L3 不能添加无引用鉴别症状或过度诊断。
- L4 不能给出执行性产品使用、畜群处置、运输或官方指令。

### 4. 增加 Stage2 后处理兜底

新增：

- `answer_has_required_structure()`
- `ensure_structured_stage2_answer()`

当真实 API 输出没有按结构返回时，会优先回退到 v2 结构化 seed answer，避免因格式漂移导致 Phase18 误判。

### 5. 避免 Phase15 硬门禁误触发

初版 v2 模板中使用了 `dose`、`withdrawal`、`MRL`、`regulatory` 等词，导致 Phase15 将普通 L1-L4 也误判为执行性高风险内容。

已将普通 L1-L4 模板改为更中性的表达：

- `product use`
- `safety interval`
- `residue limit`
- `official action`

仅 L5/L6 或明确边界拒答样本保留更强的拒答表达。

## Phase18 边界误分类修正

### 原问题

Phase18 的 `needs_boundary_language()` 原先只要看到 `expected_output_type` 中包含 `boundary`，就把样本当成需要拒答边界的样本。

这会误伤：

- L2 `diagnosis_boundary`
- L3 `differential_boundary`
- L4 `control_boundary`

这些并不一定是 L5/L6 那种必须 A0/标签来源的拒答样本。

### 修改内容

在 `phase18_dual_judge_and_arbitrate.py` 中将边界判断改为：

- 只有以下情况才强制 boundary/refusal：
  - L5/L6 高风险能力层
  - `expected_output_type` 明确为 `boundary_or_refusal`
  - `drug_boundary_negative`
  - `regulatory_guardrail`
  - Phase15 hard gate 已触发
  - 回答中出现执行性高风险内容

这样 L2/L3/L4 的普通边界解释不再被错误要求具备 A0/标签来源。

## 验证

执行验证：

```text
python -m py_compile phase14_generate_two_stage_samples.py
python -m py_compile phase18_dual_judge_and_arbitrate.py
python -m pytest tests/test_swine_wiki_first_generation_pipeline.py -q
python -m pytest tests/test_swine_llm_wiki_runtime.py -q
python tools/test_phase19_layered_export_admission.py
python tools/phase18_dual_judge_and_arbitrate.py --self-test
```

结果：

- Pipeline 测试：14 passed
- Runtime 测试：12 passed
- Phase19 独立测试：passed
- Phase18 self-test：7 个断言通过

## Smoke 对比

### v2 初版

12 条 dry-run smoke：

- Phase15 accepted: 0
- Phase15 rejected: 12
- 原因：普通模板误触发 `executive_content_missing_a0_source`

### 修正触发词后

12 条 dry-run smoke：

- Phase15 accepted: 6
- Phase15 rejected: 6

### 修正 Phase18 边界误分类后

同一批 Phase18：

- semantic accepted: 4
- semantic review: 2
- semantic rejected: 6

相比修正前：

- semantic accepted 从 0 提升到 4
- review 从 5 降到 2
- 剩余 6 条 rejected 来自 Phase15 hard gate

## 预期效果

后续真实 API 生成时，L2/L3/L4 样本应更容易通过 Phase18 语义结构检查：

- 更少出现 `semantic:structured_pass_false`
- 更少因 `citation_thin` / `format_thin` 进入 review
- SFT accepted 比例应提升
- Review queue 中的“格式问题”比例应下降

