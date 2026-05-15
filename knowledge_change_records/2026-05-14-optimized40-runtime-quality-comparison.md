# 2026-05-14 优化后 40 条正式批次运行与质量对比报告

## 执行目标

按照要求，使用：

```powershell
--parallel 8 --max-tokens 1800
```

重新运行 40 条真实问诊数据生成与评估流程，继续输出单一综合 CSV，并对比优化前后：
- 全链路耗时是否改善。
- 数据真实性是否改善。
- 字段是否完整。
- 各裁判维度评分趋势是变好还是变坏。
- accepted/review/rejected 分布变化及原因。

## 批次信息

优化前对照批次：

`20260514_parallel8_consult40_singlecsv_v1`

优化后正式批次：

`20260514_parallel8_consult40_optimized_v1`

优化后最终单一 CSV：

`exports/training_sets/swine_wiki_consultation_sft_scored_single_20260514_parallel8_consult40_optimized_v1.csv`

## 全链路耗时对比

### 优化前

- Phase13：约 0.66 秒
- Phase14：约 487.80 秒
- Phase15：约 0.71 秒
- Phase18：约 283.99 秒
- Phase16：约 0.93 秒

### 优化后

- Phase13：约 0.91 秒
- Phase14：约 54.97 秒
- Phase15：约 1.16 秒
- Phase18：约 442.71 秒
- Phase16：约 0.99 秒

## 耗时结论

### Phase14 明显变快

Phase14 从约 487.80 秒下降到约 54.97 秒，速度提升约 8.9 倍。

原因：
- 优化前每条样本需要 stage1 + stage2 两次真实模型调用，40 条约 80 次生成调用。
- 优化后每条样本只调用一次真实模型生成 `clinical_answer`，40 条约 40 次生成调用。
- `max_tokens` 从 3200 降到 1800。

### Phase18 反而变慢

Phase18 从约 283.99 秒上升到约 442.71 秒。

原因：
- Phase15 accepted 从 29 增加到 32，因此进入双裁判的样本变多。
- 虽然仲裁数量从 29 降到 22，但双裁判样本数增加，且本轮中转站/裁判模型响应明显波动。
- 自然化回答减少了显式引用，Judge B 和仲裁更容易把部分样本打到 review，需要更多仲裁处理。

## 分布对比

### 优化前

- accepted：23
- review：6
- rejected：11

### 优化后

- accepted：20
- review：12
- rejected：8

## 分布变化结论

优化后：
- rejected 从 11 降到 8，说明 Phase15 硬门控误杀有所减少。
- review 从 6 增到 12，说明更多样本进入“可用但需复核/修复”区间。
- accepted 从 23 降到 20，说明自然化后部分样本虽然更真实，但在证据完整性、回答完整度或裁判一致性上被降级。

整体判断：
- 数据真实性显著变好。
- 安全拒绝减少。
- 直接可训练样本数量略降。
- 可修复样本数量增加。

## 字段完整性检查

优化后单一 CSV 共 40 行，关键字段空值为 0：

- `sample_quality_tag`
- `defect_tag`
- `training_use_tag`
- `sample_id`
- `case_context`
- `case_user_query`
- `assistant_answer`
- `grounded_audit_answer`
- `phase15_final_decision`
- `phase18_semantic_decision`
- `export_decision`
- `final_label`
- `final_total_score`
- `field_source_map`

乱码命中数：0

主回答中 source/fact/page/rule/DIS 编号痕迹：
- 优化前：40/40
- 优化后：0/40

## 数据真实性变化

### 优化前问题

用户问题类似：

```text
请你按兽医问诊 agent 的方式回答：围绕DIS-001，猪场现场咨询：围绕猪腺病毒感染，现有资料目前能确认哪些可靠信息...
```

助手回答包含：

```text
[source=SRC-0001][rule=RC-CITATION-001][fact=...][page=...]
```

这种样本更像知识库审计，不像真实兽医问诊。

### 优化后效果

用户问题变成：

```text
老师您好，我们这边是分区管理的规模场，一批哺乳母猪连续两个批次都有类似情况，现在主要是有个别死亡、精神差、吃料下降。日龄和批次记录不全、发病比例和死亡数还没统计清楚、免疫记录一时找不到，心里没底，想先排一下可能方向。您看我现在应该先从哪些方面排查？
```

助手回答不再直接显示引用编号，而是像兽医问诊回复：

```text
从你描述的情况来看，哺乳母猪连续两批出现个别死亡、精神沉郁、采食量下降，这种跨批次的表现提示可能存在某种共通风险因素...
```

证据锚点仍保留在：
- `grounded_audit_answer`
- `evidence_anchors`
- Phase15 字段
- Phase18 裁判与仲裁字段

## 维度评分变化

以下为优化前后全量均分对比：

| 维度 | 优化前 | 优化后 | 变化 |
|---|---:|---:|---:|
| `final_total_score` | 61.98 | 66.74 | +4.76 |
| `judge_a_evidence_fidelity` | 56.74 | 56.02 | -0.72 |
| `judge_a_clinical_reasoning` | 54.39 | 55.51 | +1.12 |
| `judge_a_safety_boundary` | 59.76 | 60.84 | +1.08 |
| `judge_a_question_resolution` | 57.47 | 58.93 | +1.46 |
| `judge_a_training_utility` | 55.55 | 56.34 | +0.79 |
| `judge_b_risk_control` | 23.93 | 23.94 | +0.01 |
| `judge_b_unsupported_expansion_control` | 17.31 | 16.94 | -0.37 |
| `judge_b_answer_completeness` | 21.03 | 20.56 | -0.47 |
| `judge_b_citation_integrity` | 13.17 | 12.25 | -0.92 |
| `judge_b_language_naturalness` | 20.93 | 20.41 | -0.52 |
| `arbiter_consensus_reliability` | 37.74 | 52.73 | +14.99 |
| `arbiter_safety_override` | 46.26 | 61.23 | +14.97 |
| `arbiter_evidence_sufficiency` | 39.93 | 52.16 | +12.23 |
| `arbiter_training_value` | 42.13 | 54.85 | +12.72 |
| `arbiter_calibration_consistency` | 35.89 | 50.70 | +14.81 |

## 评分变化解释

### 变好的维度

`final_total_score` 上升 4.76，说明整体质量和仲裁后的综合判断改善。

Judge A 的：
- `clinical_reasoning`
- `safety_boundary`
- `question_resolution`
- `training_utility`

均有小幅上升。原因是主回答更像真实问诊，能更自然地回应用户场景和下一步排查。

仲裁维度大幅上升。原因是：
- Phase15 rejected 减少。
- 主回答不再像审计字段堆砌。
- 好样本与待复核样本的边界更清楚。

### 变差的维度

Judge B 的：
- `citation_integrity`
- `answer_completeness`
- `language_naturalness`

略有下降。

原因：
- 主回答不再显示 source/fact/page，虽然审计字段保留引用，但 Judge B 仍会对主回答的直接可追溯性略扣分。
- `max_tokens=1800` 和单调用策略让部分回答更短，完整度略降。
- 有 3 条 Phase14 fallback，可能拉低部分自然度和训练价值。

## 数据质量判断

整体变好：
- 真实感明显提升。
- 主训练字段不再混入知识库审计格式。
- Phase15 拒绝数减少。
- 最终平均分上升。
- 仲裁维度显著改善。

局部变差：
- accepted 数从 23 降到 20。
- review 数从 6 增到 12。
- Judge B 对完整性、引用完整性和自然度略降。

原因不是生成失效，而是优化后回答更短、更自然，减少了显式引用和审计型表达；这提高了真实感，但也让部分裁判维度更保守。

## 后续建议

1. 保留当前“主回答自然化 + 审计字段保留锚点”的方向，这是正确方向。
2. 下一轮可把 `max_tokens` 从 1800 调到 2200，提升回答完整度，同时仍明显快于 3200。
3. 调整 Judge B prompt，明确 `citation_integrity` 应主要检查 `grounded_audit_answer/evidence_anchors`，不应要求 `assistant_answer` 暴露 citation。
4. 对 Phase14 fallback 的 3 条样本增加重试，而不是直接保留确定性短回答。
5. Phase18 可继续优化低风险样本的仲裁策略，但高风险样本建议继续保留强仲裁。

## 结论

本次优化有效。

从运行效率看：
- Phase14 从约 488 秒降到约 55 秒，效果非常明显。

从数据质量看：
- 主训练问答真实性显著变好。
- 知识库从“直接插入训练回答”变成“约束和审计依据”，方向正确。
- 平均最终分数提升。

需要继续优化的是：
- Phase18 仍是主要耗时瓶颈。
- 自然化后 review 增加，需要通过 prompt 和裁判校准减少过度保守。
