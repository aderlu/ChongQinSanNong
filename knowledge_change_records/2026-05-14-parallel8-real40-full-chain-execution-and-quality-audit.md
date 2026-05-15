# 2026-05-14 八路并发真实 40 条全链路执行与质量审查报告

## 一、执行目标

本次按用户要求执行八路并发真实调用全链路流程，生成 40 条真实 CSV 数据，并检查：

- 结果问答字段是否有效。
- Phase15 事实/安全门控结果。
- Phase18 双裁判与仲裁流程是否有效。
- 每个阶段耗时和瓶颈。
- 执行过程中暴露的问题。

批次标识：

`20260514_parallel8_real40_quality_audit_v1`

## 二、执行链路

执行顺序：

```text
Phase12 样本规划
→ Phase13 skeleton 构建
→ Phase14 八路并发真实 API 生成 40 条
→ Phase14b 主回答自然化/审计痕迹清理
→ Phase15 事实与安全门控
→ Phase18 双裁判独立评分 + 仲裁
→ Phase16 CSV 与训练集导出
```

执行过程中发现并修复 1 个运行时阻塞问题：

- Phase14 通过根兼容脚本运行时无法导入 `consultation_case_variables.py`。
- 已新增运行时导入路径修复。
- 留痕文档：`knowledge_change_records/2026-05-14-phase14-runtime-import-path-fix.md`

## 三、输出文件

主要输出：

- 规划文件：`ai-/knowledge/llm_wiki_swine_authoritative/exports/planned_samples/wiki_sample_plan_20260514_parallel8_real40_quality_audit_v1.jsonl`
- Skeleton：`ai-/knowledge/llm_wiki_swine_authoritative/exports/answer_skeletons/wiki_answer_skeletons_20260514_parallel8_real40_quality_audit_v1.jsonl`
- 原始生成：`ai-/knowledge/llm_wiki_swine_authoritative/exports/generated_samples/two_stage_samples_20260514_parallel8_real40_quality_audit_v1.jsonl`
- 自然化生成：`ai-/knowledge/llm_wiki_swine_authoritative/exports/generated_samples/naturalized_samples_20260514_parallel8_real40_quality_audit_v1.jsonl`
- Phase15 结果：`ai-/knowledge/llm_wiki_swine_authoritative/exports/evaluated_samples/fact_evaluated_samples_20260514_parallel8_real40_quality_audit_v1.jsonl`
- Phase18 结果：`ai-/knowledge/llm_wiki_swine_authoritative/exports/semantic_evaluated_samples/semantic_evaluated_samples_20260514_parallel8_real40_quality_audit_v1.jsonl`
- 生产 CSV：`ai-/knowledge/llm_wiki_swine_authoritative/exports/training_sets/swine_wiki_training_dataset_production_20260514_parallel8_real40_quality_audit_v1.csv`
- Train-ready CSV：`ai-/knowledge/llm_wiki_swine_authoritative/exports/training_sets/swine_wiki_training_dataset_production_train_ready_20260514_parallel8_real40_quality_audit_v1.csv`
- 主训练 CSV：`ai-/knowledge/llm_wiki_swine_authoritative/exports/training_sets/swine_wiki_training_main_20260514_parallel8_real40_quality_audit_v1.csv`
- 主训练 train-ready CSV：`ai-/knowledge/llm_wiki_swine_authoritative/exports/training_sets/swine_wiki_training_main_train_ready_20260514_parallel8_real40_quality_audit_v1.csv`

辅助分析 JSON：

- `knowledge_change_records/2026-05-14-20260514_parallel8_real40_quality_audit_v1-analysis.json`
- `knowledge_change_records/2026-05-14-20260514_parallel8_real40_quality_audit_v1-phase18-admission-analysis.json`

## 四、阶段耗时

| 阶段 | 耗时秒 | 说明 |
|---|---:|---|
| Phase12 | 0.58 | 规划 80 条 |
| Phase13 | 0.62 | 生成 80 个 skeleton |
| Phase14 | 52.36 | 八路并发真实 API 生成 40 条 |
| Phase14b | 0.33 | 主回答清理 |
| Phase15 | 0.24 | 事实/安全门控 |
| Phase18 | 231.91 | 双裁判 + 仲裁 |
| Phase16 | 0.38 | CSV/训练集导出 |

瓶颈判断：

- 最大瓶颈是 Phase18，占总耗时约 81%。
- 第二瓶颈是 Phase14，占总耗时约 18%。
- 其他阶段均不是性能瓶颈。

## 五、生成结果概况

| 指标 | 数量 |
|---|---:|
| 原始真实生成样本 | 40 |
| 自然化样本 | 40 |
| 生产 CSV 行数 | 40 |
| Train-ready CSV 行数 | 15 |
| 主训练 CSV 行数 | 40 |
| 主训练 train-ready 行数 | 15 |

Phase14 能力层分布：

| 能力层 | 数量 |
|---|---:|
| L1_retrieval_grounded | 17 |
| L2_diagnosis_support | 7 |
| L3_differential_support | 7 |
| L4_control_boundary | 7 |
| L6_regulatory_guardrail | 2 |

## 六、问答字段有效性检查

检查结果：

| 检查项 | 结果 |
|---|---:|
| 空问题或空回答 | 0 |
| 主回答审计字段泄漏 | 0 |
| 弱问题/知识库式问题 | 0 |
| 回答短于 120 字 | 16 |
| Phase14 fallback 样本 | 17 |
| 生成错误样本 | 17 |

结论：

- CSV 问答字段完整性通过：没有空问题、空回答。
- 主回答清洁度通过：没有发现 `source=`、`fact=`、`page=`、`rule=`、`DIS-`、`RC-`、`知识库`、`引用锚点` 泄漏。
- 真实问诊问题有效性基本通过：未发现明显知识库式用户问题。
- 回答有效性不足：16 条回答过短，17 条由 fallback 生成，训练价值较低。

典型短回答问题：

```text
猪腺病毒感染；category；病毒病; 猪腺病毒感染；textbook_chapter_start_page；462
非洲猪瘟；category；病毒病; 非洲猪瘟；textbook_chapter_start_page；467
```

这些内容来自 fallback 的审计事实拼接，不符合真实兽医问诊回答风格。

## 七、Phase15 门控结果

| 结果 | 数量 |
|---|---:|
| accepted | 23 |
| rejected | 17 |

拒绝原因：

| 原因 | 数量 |
|---|---:|
| `answer_too_short_for_training` | 11 |
| `information_density_too_low` | 11 |
| `executive_content_missing_a0_source` | 6 |
| `deterministic_placeholder_failed` | 17 |

判断：

- Phase15 有效识别了 fallback 导致的短回答、低信息密度和占位式回答。
- Phase15 对质量问题的拦截是有效的。
- 17 条 rejected 与 Phase14 fallback 数量一致，说明生成阶段 API 失败是主要上游问题。

## 八、Phase18 双裁判与仲裁有效性

Phase18 汇总：

| 指标 | 数量 |
|---|---:|
| 样本总数 | 40 |
| 双裁判样本 | 23 |
| Phase15 硬门控跳过 | 17 |
| 需要仲裁 | 23 |
| semantic accepted | 15 |
| semantic rejected | 25 |
| fatal risk | 22 |

仲裁触发统计：

| 触发原因 | 数量 |
|---|---:|
| score_gap_ge_15 | 16 |
| critical_dimension_gap_ge_2 | 11 |
| phase15_negative_boundary_trigger | 12 |
| hard_fail_flag | 5 |
| high_risk_sample | 5 |
| label_disagreement | 3 |
| synthetic_context_misuse | 2 |

双裁判分歧：

| 指标 | 数值 |
|---|---:|
| 有分数差样本 | 23 |
| 平均分差 | 55.41 |
| 最大分差 | 97.0 |
| 分差 >= 15 | 16 |

有效性判断：

- 仲裁触发机制有效：分差、标签分歧、关键维度分歧和硬伤均能触发仲裁。
- Phase15 hard gate 失败的 17 条没有继续浪费双裁判资源，这一策略合理。
- 但双裁判本身稳定性不足：平均分差 55.41，说明两个裁判的评分尺度严重不一致。
- 仲裁结构化输出和最终准入映射存在严重问题。

## 九、发现的严重问题

### 9.1 Phase14 真实 API 调用不稳定

17 条样本出现 `generation_error` 并进入 fallback。

典型错误：

- `APIConnectionError: Connection error.`
- `JSONDecodeError: Invalid control character`

影响：

- 直接导致 16 条短回答。
- Phase15 拦截 17 条。
- 40 条最终只有 15 条进入 train-ready。

### 9.2 Phase12 当前抽样证据深度过低

Phase12 规划的 80 条中：

- `evidence_depth_class = toc_only` 为 80 条。
- `positive_sft = 0`。
- `eval_only = 74`，`boundary_sft = 6`。

影响：

- 生成器缺少实质医学证据，只能生成边界/缺口型回答。
- 很难生成高质量有效的真实问诊 SFT。
- 这会压低医学正确性、信息充分性和可执行性。

### 9.3 Phase18 裁判/仲裁输出结构存在缺陷

发现异常：

- 15 条 `semantic_decision=accepted`，但 `final_label=repairable`。
- 这 15 条却被映射为 `sft_admission=main_sft`。
- 部分 `main_issues` 被拆成单字符列表，例如英文句子变成 `["T","h","e",...]`。
- 多条 judge 或 arbiter 分数为 `0.0`，但结论却是 `repairable` 或 accepted。

影响：

- 当前 Phase18 仲裁触发有效，但最终结构化解析与准入映射不可靠。
- `repairable` 不应直接进入 `main_sft`。
- 如果不修复，会导致并不完全合格的数据进入主训练集。

### 9.4 Phase16 准入结果偏宽

Phase16 导出结果：

- accepted 15
- rejected 25
- review 0

问题：

- `repairable` 样本没有进入 repair queue，而是进入 main_sft。
- 这与此前设计的四档结论不一致。

## 十、结论

本次全链路成功执行，真实生成了 40 条生产 CSV 数据。但从严格质量角度看，本批数据不能认为已经达到可直接批量训练标准。

可接受部分：

- 全链路可以跑通。
- 8 并发 Phase14 可以生成 40 条。
- CSV 字段完整，新增问诊字段已经进入 CSV。
- 主回答审计泄漏为 0。
- Phase15 对低质量 fallback 有效拦截。
- Phase18 仲裁触发规则有效。

不可接受部分：

- 生成阶段 fallback 比例过高：17/40。
- 训练可用比例偏低：15/40。
- Phase12 抽样全为 `toc_only`，知识支撑不足。
- Phase18 输出结构和 Phase16 准入映射存在严重逻辑问题。
- 双裁判评分尺度差异过大，平均分差 55.41。

## 十一、建议后续修复优先级

优先级 1：

- 修复 Phase18 `main_issues` 字符串被拆成单字符列表的问题。
- 修复 `repairable -> main_sft` 的错误映射，`repairable` 应进入 `repair_queue` 或低权重复核队列。
- 修复 judge/arbiter 分数为 0 但结论 accepted/repairable 的结构化解析问题。

优先级 2：

- Phase12 规划时优先抽取 `substantive` 证据样本，避免 40 条正式批次全部来自 `toc_only`。
- 生成正式 SFT 批次时应过滤 `eval_only/toc_only`，或单独作为边界/检索缺口数据。

优先级 3：

- Phase14 增加 API 重试和 JSON 修复策略，降低 `APIConnectionError` 与 `JSONDecodeError` 导致的 fallback。
- fallback 回答不应使用审计事实拼接作为 `clinical_answer`，应生成安全但自然的兜底问诊回答。

优先级 4：

- Phase18 双裁判 prompt 或解析规则需要统一评分尺度，降低不合理分差。
- 对双裁判评分为 0 的情况增加解析失败标记，而不是进入普通仲裁。

## 十二、最终判断

本次执行链路已完成，CSV 已生成；但本批 40 条中只有 15 条进入 train-ready，且准入映射存在问题。因此该批数据适合作为“全链路压力测试与问题定位批次”，不建议直接作为正式高质量训练集使用。
