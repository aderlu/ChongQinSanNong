# 2026-05-14 猪病问诊数据生成产线质量问题分阶段修复方案

## 一、文档目标

本方案用于修复当前真实全链路执行中暴露出的三个核心问题：

1. 40 条生成数据重复高、多样性差、覆盖范围窄。
2. Phase12 当前抽样证据深度过低，大量样本来自 `toc_only`。
3. Phase18 裁判/仲裁结构化输出和 Phase16 准入映射存在缺陷。

本方案只基于当前项目中已经存在的链路和文件落地，不设计脱离当前代码结构的新系统。

目标链路：

```text
Phase12 规划与抽样
→ Phase13 skeleton 合同
→ Phase14 真实生成
→ Phase14b 主回答清理
→ Phase15 事实与安全门控
→ Phase18 双裁判与仲裁
→ Phase16 CSV/训练集导出
```

## 二、当前问题与实际证据

本方案依据批次：

`20260514_parallel8_real40_quality_audit_v1`

### 2.1 重复高、覆盖窄

本批 40 条只覆盖 `DIS-001` 到 `DIS-017`，没有有效覆盖 wiki 全范围。

重复情况：

- `DIS-002` 出现 5 次。
- `DIS-004` 出现 4 次。
- `DIS-007` 出现 4 次。
- `DIS-008` 出现 4 次。
- `DIS-009` 出现 4 次。
- `DIS-015` 出现 5 次。

直接原因：

- Phase12 按 runtime manifest 顺序遍历。
- 同一 entity 会因多个 ability layer 生成多条 plan。
- `--limit 40` 只是截取前 40 条 plan，没有按 page/entity 做批次级覆盖控制。

### 2.2 证据深度过低

本批 Phase12 规划 80 条：

- `toc_only`: 80
- `substantive`: 0
- `positive_sft`: 0
- `eval_only`: 74
- `boundary_sft`: 6

全局粗略估算：

- runtime manifest 页面：204
- substantive 页面：约 7
- toc_only 页面：约 197

直接原因：

- 当前 wiki 大量页面只有目录级事实，如疾病类别、教材页码。
- Phase12 允许 `toc_only` 进入正式生成链路。
- Phase14 在证据不足时只能生成边界/缺口回答，甚至 fallback 时退化为字段拼接。

### 2.3 Phase18/Phase16 准入结构缺陷

本批发现：

- 15 条 `semantic_decision=accepted`，但 `final_label=repairable`。
- 这 15 条又被映射为 `sft_admission=main_sft`。
- 部分 `main_issues` 被拆成单字符列表。
- 多条 judge/arbiter 分数为 `0.0`，但结论仍是 `repairable` 或被 accepted。

直接原因：

- Phase18 中对 `main_issues` 使用 `list(value)`，当 value 是字符串时会拆成字符。
- Phase18/Phase16 过度信任模型返回的 `sft_admission`。
- Phase16 中只要 `sft_admission in {"main_sft", "low_weight_sft"}` 就 accepted。
- 没有把 `zero_score_non_invalid` 当作结构化解析失败。

## 三、总体修复原则

### 3.1 先修准入，再扩大生成

原因：

如果 Phase18/Phase16 准入错误未修复，即使生成质量提升，也可能把 `repairable` 或结构异常数据错误导入主训练集。

所以第一阶段必须先修裁判/仲裁归一化和导出准入。

### 3.2 正式 SFT 只使用足够证据

原因：

真实兽医问诊回答需要症状、病程、诊断边界、鉴别、采样、检测、防控等证据支撑。目录级事实只能支撑“资料不足”的检索缺口样本，不能支撑高质量问诊 SFT。

### 3.3 多样性来自抽样设计，不靠模型随机

原因：

如果 Phase12 输入本身集中在前几个疾病，即使 prompt 再好，Phase14 也只能围绕少数疾病生成。多样性应在 Phase12 批次规划中解决。

### 3.4 fallback 不能污染主回答

原因：

API 不稳定时可以保留样本记录，但 fallback 的审计事实拼接不能进入 `clinical_answer`，否则会被 Phase15 拒绝，也会污染 CSV。

## 四、阶段一：修复 Phase18/Phase16 准入结构

### 4.1 目标文件

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase16_export_layered_training_sets.py`

### 4.2 修改内容

#### 4.2.1 新增安全列表归一化

新增函数：

```python
def normalize_string_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]
```

替换所有类似：

```python
list(payload.get("main_issues") or [])
```

原因：

字符串直接 `list()` 会被拆成字符，导致 `["T", "h", "e"]` 这种错误结构。

能够解决：

- `main_issues` 单字符拆分。
- `hard_fail_codes`、`repair_suggestion` 等字段类型不稳定。

#### 4.2.2 不再信任模型返回的 sft_admission

Phase18 中：

```python
sft_admission = sft_admission_from_label(final_label, hard_fail=hard_fail, risk_level=risk_level)
```

不要使用：

```python
payload.get("sft_admission")
```

除非仅作为 `raw_model_sft_admission` 保存。

原因：

模型可能输出 `repairable + main_sft` 这种自相矛盾结果。最终准入必须由本地规则统一计算。

能够解决：

- `repairable -> main_sft` 错误。
- 模型输出覆盖本地安全准入规则的问题。

#### 4.2.3 增加结构化失败检测

新增检测：

```python
zero_score_non_invalid = total_score == 0 and final_label != "invalid"
all_dimensions_zero = all(score == 0 for score in dimension_scores.values())
label_score_conflict = final_label in {"valid", "high_quality_valid"} and total_score < PASS_THRESHOLD
```

处理策略：

- 标记 `structured_parse_failed=True`。
- `final_label` 最高只能是 `repairable`。
- 严重时进入 `repair_queue` 或 `reject_queue`。

原因：

0 分但 accepted/repairable 本质上是解析失败或模型输出不可信。

能够解决：

- 裁判结果自相矛盾。
- Phase18 高分/低分尺度失真。

#### 4.2.4 Phase16 二次硬约束

在 `combined_decision()` 中增加：

```python
if final_label == "repairable":
    export_decision = "review"
elif final_label == "invalid":
    export_decision = "rejected"
elif final_label == "valid":
    export_decision = "accepted" only if sft_admission == "low_weight_sft"
elif final_label == "high_quality_valid":
    export_decision = "accepted" only if sft_admission == "main_sft"
```

原因：

Phase16 是最后一道导出门，不能只看 `sft_admission` 字符串。

能够解决：

- repairable 数据进入 train-ready。
- 主训练 CSV 混入待修复样本。

### 4.3 验收标准

- `repairable_main_sft_count = 0`
- `main_issues_char_split_count = 0`
- `zero_score_non_invalid_count = 0`
- `final_label=repairable` 的样本进入 review/repair queue，不进入 train-ready。
- Phase16 train-ready 中只允许 `high_quality_valid` 和 `valid`。

## 五、阶段二：修复 Phase12 覆盖与抽样策略

### 5.1 目标文件

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase12_plan_samples_from_wiki.py`

### 5.2 修改内容

#### 5.2.1 新增正式批次抽样模式

新增参数：

```text
--sampling-mode coverage
--max-plans-per-entity 2
--prefer-depth substantive,thin,toc_only
--min-substantive-ratio 0.6
```

默认保留当前行为，避免破坏已有测试和历史流程。

原因：

当前 `--limit` 是简单截断，导致前 40 条集中在前几个 disease 页面。

能够解决：

- 覆盖范围窄。
- 同一疾病多能力层重复。
- 批次只覆盖前几个 wiki 页面。

#### 5.2.2 批次级去重与分层抽样

实现逻辑：

1. 先生成全量候选 plans。
2. 按 `evidence_depth_class` 分桶。
3. 按 `entity_id/page_relpath` 控制重复。
4. round-robin 从不同页面取样。
5. 每个 entity 默认最多 2 条。
6. 优先抽 `substantive`，其次 `thin`，最后 `toc_only`。

原因：

多样性必须在计划阶段控制，不能交给 Phase14 生成模型随机解决。

能够解决：

- 40 条只覆盖 17 个 disease。
- 某些疾病出现 4 到 5 次。

#### 5.2.3 toc_only 限制

正式 SFT 批次中：

- `toc_only` 默认不进入 L2/L3/L4 正样本。
- `toc_only` 只允许进入：
  - `retrieval_gap_check`
  - `eval_only`
  - `L7_judge_calibration`

原因：

toc_only 只知道“是什么类别/在第几页”，不能支撑真实问诊。

能够解决：

- 目录事实拼接成回答。
- 医学信息不足导致的低质量回答。

#### 5.2.4 新增覆盖报告字段

Phase12 report 增加：

- `unique_entity_count`
- `unique_page_count`
- `max_samples_per_entity`
- `substantive_ratio`
- `toc_only_ratio`
- `coverage_passed`
- `coverage_violations`

原因：

如果不在 Phase12 报告中暴露覆盖情况，后续只能等 CSV 出来才发现重复。

能够解决：

- 批次质量不可见。
- 规划阶段无法提前中断低质量批次。

### 5.3 验收标准

40 条正式批次：

- unique page ≥ 30。
- unique entity ≥ 30。
- 单 entity ≤ 2。
- `substantive_ratio >= 60%`。
- `toc_only_ratio <= 10%`。
- 若当前 wiki 无法满足，则 Phase12 明确失败，不进入 Phase14 正式生成。

## 六、阶段三：补强 wiki 证据深度

### 6.1 目标文件/目录

核心目录：

`ai-/knowledge/llm_wiki_swine_authoritative`

相关导出：

- `exports/knowledge_facts_status_index.json`
- `exports/runtime_core_manifest.json`
- wiki disease/control/drug 页面

### 6.2 修改内容

#### 6.2.1 建立“可生成疾病白名单”

新增或导出：

```text
exports/consultation_generation_readiness_index.csv
```

字段：

- `entity_id`
- `page_relpath`
- `evidence_depth_class`
- `main_answer_fact_count`
- `boundary_fact_count`
- `diagnosis_support_fact_count`
- `differential_fact_count`
- `control_fact_count`
- `drug_boundary_fact_count`
- `generation_ready`

原因：

当前 Phase12 只能粗略判断 `toc_only/substantive`，不能判断某页是否能生成真实问诊。

能够解决：

- 有事实但不适合问诊的页面误入生成。
- 正式批次缺少可生成白名单。

#### 6.2.2 优先补 30 到 50 个高价值疾病页面

每个疾病至少补齐：

- 主诉/临床表现事实。
- 易感阶段/猪群背景事实。
- 关键追问事实。
- 采样/检测建议事实。
- 鉴别诊断边界事实。
- 防控边界事实。
- 高风险用药/监管边界事实。

原因：

只有 7 个 substantive 页面无法支撑 40 条高质量 SFT。

能够解决：

- Phase12 无法抽到足够 substantive。
- Phase14 只能生成“资料不足”。

### 6.3 验收标准

- 至少 40 个页面达到 generation_ready。
- 每页至少 3 个非 TOC facts。
- 每页至少 1 个 boundary fact。
- 40 条正式批次中 positive_sft 不为 0。

## 七、阶段四：修复 fallback 质量

### 7.1 目标文件

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14b_naturalize_grounded_answers.py`

### 7.2 修改内容

#### 7.2.1 fallback 不得使用审计事实拼接做 clinical_answer

当前问题样例：

```text
非洲猪瘟；category；病毒病; 非洲猪瘟；textbook_chapter_start_page；467
```

修复策略：

- fallback 的 `clinical_answer` 必须使用固定安全问诊模板。
- 模板包含：
  - 现场回应。
  - 不能直接确诊。
  - 需要补充信息。
  - 采样/检测/联系兽医建议。
  - 不给处方/剂量/监管结论。

原因：

API 失败不可避免，但 fallback 不能污染主回答字段。

能够解决：

- Phase15 中 `answer_too_short_for_training`。
- `information_density_too_low`。
- `deterministic_placeholder_failed`。

#### 7.2.2 fallback 样本默认不进入主训练

新增规则：

- `generation_fallback` 存在时，默认进入 `review_queue`。
- 除非 Phase18 明确判定为 valid/high_quality_valid 且回答长度、结构、医学边界均通过。

原因：

fallback 是异常路径，不应和真实模型生成样本同等准入。

能够解决：

- API 异常样本进入 train-ready。

### 7.3 验收标准

- fallback 样本主回答长度 ≥ 120。
- fallback 样本审计泄漏 = 0。
- fallback 样本默认不进入 `main_sft`。
- Phase15 因 placeholder/too_short 拒绝数量显著下降。

## 八、阶段五：重新执行小批次验证

### 8.1 推荐批次

先跑 10 条：

```text
parallel=8
limit=10
sampling-mode=coverage
```

通过后再跑 40 条。

### 8.2 验收指标

10 条小批次：

- fallback ≤ 1。
- audit leak = 0。
- unique entity ≥ 8。
- `repairable_main_sft_count = 0`。
- `main_issues_char_split_count = 0`。
- `zero_score_non_invalid_count = 0`。

40 条正式批次：

- fallback ≤ 2。
- unique entity ≥ 30。
- single entity count ≤ 2。
- train-ready ≥ 25。
- invalid ≤ 10。
- repairable 不进入 train-ready。
- Phase18 平均双裁判分差 < 20。

## 九、实施顺序

建议按以下顺序执行：

1. 修 Phase18/Phase16 准入结构。
2. 修 Phase12 覆盖抽样。
3. 修 fallback 主回答。
4. 增加 consultation generation readiness index。
5. 补 wiki substantive facts。
6. 先跑 10 条小批次。
7. 再跑 40 条正式批次。

原因：

- 如果先补 wiki 但准入仍错误，坏数据仍可能进入主训练。
- 如果先跑大批次但抽样仍按前 N 截断，仍会重复。
- 如果 fallback 不修，API 波动仍会污染数据。

## 十、预期效果

完成上述修复后，应产生以下改善：

- 40 条批次覆盖更广，不再集中在前 10 到 20 个疾病。
- 同一疾病重复显著减少。
- `toc_only` 样本不再主导正式 SFT。
- 主回答不再出现目录字段拼接。
- `repairable` 不再进入 `main_sft`。
- Phase18 输出结构更稳定。
- CSV 可以更真实反映可训练数据质量。

## 十一、不建议做的事

不建议：

- 只改 prompt 解决重复问题。
- 在 wiki 证据不足时强行生成 40 条高质量 SFT。
- 把 `toc_only` 样本包装成真实问诊正样本。
- 信任模型直接输出的 `sft_admission`。
- 把 fallback 样本直接放入 train-ready。

这些做法短期看能增加样本数，但会降低训练集真实性和医学可靠性。

## 十二、最终结论

当前问题不是单纯生成模型能力问题，而是：

```text
Phase12 抽样无覆盖控制
+ wiki substantive 证据不足
+ Phase18 结构归一化不严
+ Phase16 准入映射偏宽
+ fallback 质量不足
```

因此必须分阶段修复。最先修准入，其次修抽样，再补证据，最后扩大生成。该路径符合当前项目结构，修改范围明确，可逐步验证，不依赖额外新系统，具备实际落地性。
