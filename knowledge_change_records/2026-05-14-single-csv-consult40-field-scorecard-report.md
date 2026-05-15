# 2026-05-14 单一 CSV 问诊数据生成、字段与评分体系说明

## 本次目标

本次重新使用真实模型和八路并发生成 40 条猪病问诊数据，并将最终结果收敛为一份单一 CSV。该 CSV 同时包含好样本、待复核样本和坏样本，不再拆分“全量版”和“可直接训练版”，而是用标签字段标记每条数据的用途和缺陷。

批次编号：`20260514_parallel8_consult40_singlecsv_v1`

最终 CSV：

`exports/training_sets/swine_wiki_consultation_sft_scored_single_20260514_parallel8_consult40_singlecsv_v1.csv`

## 防乱码措施

所有运行命令均使用 UTF-8 环境：

```powershell
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

最终检查结果：
- 乱码命中数：0
- `assistant_answer` 中对象串痕迹：0
- 核心字段空值：0

## 全流程运行结果

### Phase13

- 功能：从 plan 生成回答骨架和生成约束。
- 数量：40
- 耗时：约 0.66 秒
- 结果：通过

### Phase14

- 功能：八路并发调用真实模型，生成问诊场景、用户问题、主训练答案和审计答案。
- 模型：`hunyuan-turbos-20250926`
- 数量：40
- fallback：0
- missing anchors：0
- missing grounded citations：0
- 耗时：约 487.80 秒
- 结果：通过

### Phase15

- 功能：事实级门控与硬风险检查。
- accepted：29
- rejected：11
- 耗时：约 0.71 秒
- 主要拒绝原因：`hard_gate:executive_content_missing_a0_source`

### Phase18

- 功能：真实 LLM 双裁判与仲裁。
- 输入：40
- 双裁判：29
- Phase15 硬门控跳过：11
- accepted：23
- review：6
- rejected：11
- 耗时：约 283.99 秒

### Phase16 与单 CSV 收敛

Phase16 先按既有导出逻辑生成中间 CSV，随后收敛为一份最终 CSV：

- 好样本：23
- 待复核样本：6
- 坏样本/安全对照：11

清理措施：
- 删除本批次自动生成的 `training_main`、`training_main_train_ready`、`production`、`production_train_ready` 四份多余 CSV。
- 保留最终单一 CSV。
- 保留 JSONL、manifest 和阶段报告作为审计证据。

## 最终 CSV 的核心标记字段

### `sample_quality_tag`

表示样本总体质量标签。

- `good_train_candidate`：可作为正向 SFT 训练候选。
- `needs_review_or_repair`：需要人工复核或二次修复。
- `bad_or_unsafe_contrast`：坏样本或安全对照样本，可用于缺陷识别、判别器或评估训练。

### `defect_tag`

表示缺陷来源。

- `none`：当前未发现影响训练使用的主要缺陷。
- `phase15_hard_gate_executive_content_or_missing_a0`：Phase15 发现执行性内容或缺少 A0 权威来源，作为坏样本/安全对照。
- `phase18_quality_or_judge_disagreement_review`：Phase18 多维裁判或仲裁认为需要复核，通常来自质量边界、裁判分歧或训练价值不足。

### `training_use_tag`

表示建议用途。

- `sft_positive`：正向问诊 SFT 样本。
- `repair_or_human_review`：修复队列或人工复核。
- `negative_contrast_or_defect_analysis`：负例对照、缺陷分析或评估器训练。

## 最终 CSV 主要字段含义

### 基础标识字段

- `sample_id`：样本编号。
- `plan_id`：样本规划阶段的 plan 编号。
- `ability_layer`：能力层级，例如检索型回答、诊断支持、鉴别支持、防控边界、监管边界。
- `entity_id`：疾病或实体编号。
- `entity_type`：实体类型。
- `risk_class`：风险等级。
- `expected_output_type`：规划阶段期望输出类型。

### 问诊训练字段

- `case_context`：合成的真实问诊场景上下文，只表示用户描述，不作为疾病事实来源。
- `case_user_query`：真实感用户问诊输入，是后续 SFT 的主要 user 内容。
- `user_query`：兼容字段，当前与 `case_user_query` 对齐。
- `assistant_answer`：主训练答案，是兽医问诊 agent 的回答。
- `grounded_audit_answer`：审计答案，保留更多证据锚点和边界说明。

### 证据字段

- `source_trust`：来源可信等级。
- `evidence_coverage`：证据覆盖程度。
- `evidence_anchor_count`：证据锚点数量。
- `evidence_units`：证据单元内容。
- `page_gold_ready`：页面或事实是否达到 gold-ready 条件。

### Phase15 字段

- `phase15_final_decision`：Phase15 的事实门控结论。
- `phase15_fact_passed`：事实检查是否通过。
- `phase15_hard_gate_passed`：硬风险门控是否通过。

### Phase18 总体字段

- `phase18_semantic_decision`：Phase18 双裁判与仲裁后的语义结论。
- `phase18_judge_status`：总体裁判状态。
- `phase18_judge_a_status`：裁判 A 状态。
- `phase18_judge_b_status`：裁判 B 状态。
- `phase18_arbiter_status`：仲裁状态。
- `needed_arbitration`：是否触发仲裁。

### 最终导出字段

- `export_decision`：最终导出决策，取值为 `accepted`、`review`、`rejected`。
- `final_label`：最终标签，通常为 `pass`、`review`、`reject`。
- `final_total_score`：最终总分。
- `final_weighted_total_score`：最终加权总分。
- `final_fatal_risk`：是否存在致命风险。
- `final_structured_pass`：结构化检查是否通过。
- `final_score_source`：最终分数来源。

### 裁判 A 字段

- `judge_a_model`：裁判 A 使用模型。
- `judge_a_total_score`：裁判 A 总分。
- `judge_a_weighted_total_score`：裁判 A 加权总分。
- `judge_a_final_label`：裁判 A 标签。
- `judge_a_fatal_risk`：裁判 A 是否发现致命风险。
- `judge_a_structured_pass`：裁判 A 结构化输出是否通过。
- `judge_a_seconds`：裁判 A 耗时。
- `judge_a_summary`：裁判 A 总结。
- `judge_a_evidence_fidelity`：证据忠实度评分。
- `judge_a_clinical_reasoning`：临床推理评分。
- `judge_a_safety_boundary`：安全边界评分。
- `judge_a_question_resolution`：问题解决度评分。
- `judge_a_training_utility`：训练价值评分。

### 裁判 B 字段

- `judge_b_model`：裁判 B 使用模型。
- `judge_b_total_score`：裁判 B 总分。
- `judge_b_weighted_total_score`：裁判 B 加权总分。
- `judge_b_final_label`：裁判 B 标签。
- `judge_b_fatal_risk`：裁判 B 是否发现致命风险。
- `judge_b_structured_pass`：裁判 B 结构化输出是否通过。
- `judge_b_seconds`：裁判 B 耗时。
- `judge_b_summary`：裁判 B 总结。
- `judge_b_risk_control`：风险控制评分。
- `judge_b_unsupported_expansion_control`：无依据扩展控制评分。
- `judge_b_answer_completeness`：回答完整性评分。
- `judge_b_citation_integrity`：引用完整性评分。
- `judge_b_language_naturalness`：语言自然度评分。

### 仲裁字段

- `arbiter_model`：仲裁模型。
- `arbiter_seconds`：仲裁耗时。
- `arbiter_reason`：仲裁理由。
- `arbiter_agreed_with_judge`：仲裁更接近哪位裁判。
- `arbiter_final_total_score`：仲裁最终总分。
- `arbiter_weighted_total_score`：仲裁加权总分。
- `arbiter_final_label`：仲裁最终标签。
- `arbiter_fatal_risk`：仲裁是否发现致命风险。
- `arbiter_structured_pass`：仲裁结构化输出是否通过。
- `arbiter_consensus_reliability`：裁判一致性评分。
- `arbiter_safety_override`：安全覆盖优先评分。
- `arbiter_evidence_sufficiency`：证据充分性评分。
- `arbiter_training_value`：训练价值评分。
- `arbiter_calibration_consistency`：校准一致性评分。

### 风格字段

- `style_clinical_conversation_score`：临床对话风格评分。
- `style_dict_like_detected`：是否检测到字典/对象串痕迹。
- `style_english_template_label_detected`：是否检测到英文模板标签。
- `style_naturalized`：是否自然化。

### 来源字段

- `field_source_map`：字段来源映射，说明字段来自 Phase14、Phase15、Phase18 或 Phase16。
- `metadata`：样本元数据。

## 裁判是否多维度评估

是。当前裁判体系位于：

`tools/pipeline/wiki_first_judge_prompts.py`

评分体系版本：

`consultation_sft_g_eval_v3`

阈值：
- `PASS_THRESHOLD = 80.0`
- `REVIEW_THRESHOLD = 60.0`

也就是说：
- 总分大于等于 80 通常为 pass。
- 总分 60 到 80 通常为 review。
- 低于 60 或存在致命风险时通常 reject。

## 裁判 A 评分维度与权重

裁判 A 更偏“证据忠实 + 临床推理 + 训练价值”。

- `evidence_fidelity`，权重 22：疾病结论是否严格受 evidence anchors 约束。
- `clinical_reasoning`，权重 18：是否像猪病兽医一样在证据边界内推理。
- `safety_boundary`，权重 18：是否避免无依据确诊、处方、剂量、休药期和监管动作。
- `question_resolution`，权重 22：是否真正解决用户问诊问题，而不是只复述引用。
- `training_utility`，权重 20：是否适合作为兽医问诊 SFT 样本。

## 裁判 B 评分维度与权重

裁判 B 更偏“风险控制 + 表达完整 + 自然度”。

- `risk_control`，权重 24：是否控制治疗执行、处方、剂量、调运、上报、扑杀等风险。
- `unsupported_expansion_control`，权重 18：是否避免把合成场景误写成疾病事实。
- `answer_completeness`，权重 22：是否包含场景回应、证据判断、边界、不确定性、后续建议。
- `citation_integrity`，权重 14：关键疾病结论是否可追溯到引用锚点。
- `language_naturalness`，权重 22：语言是否自然、专业、像真实问诊 agent。

## 仲裁是否多维度评估

是。仲裁同样进行多维度评分，位于：

`tools/pipeline/wiki_first_judge_prompts.py`

仲裁触发条件包括：
- 两位裁判标签不一致。
- 两位裁判分差大于等于 8。
- 存在风险冲突。
- Phase15 提供负向边界信号。

## 仲裁维度与权重

- `consensus_reliability`，权重 20：两位裁判在标签、分数、致命风险和主要缺陷上是否一致。
- `safety_override`，权重 25：安全优先，如果训练价值和安全冲突，优先安全。
- `evidence_sufficiency`，权重 18：accepted 样本是否有足够证据支撑关键疾病结论。
- `training_value`，权重 25：样本是否应进入 SFT、修复队列或拒绝队列。
- `calibration_consistency`，权重 12：仲裁是否与 Phase15 和 v3 scorecard 保持一致。

## 本批次结果分布

最终单 CSV 共 40 行：

- `good_train_candidate`: 23
- `needs_review_or_repair`: 6
- `bad_or_unsafe_contrast`: 11

缺陷标签分布：

- `none`: 23
- `phase15_hard_gate_executive_content_or_missing_a0`: 11
- `phase18_quality_or_judge_disagreement_review`: 6

## 结论

本次最终只保留一份综合 CSV，满足同时包含好数据和坏数据的要求。好样本可用于问诊 SFT 正样本，坏样本可用于缺陷对照、判别器训练或评估体系校准，review 样本可进入人工复核或自动修复队列。

本批次的裁判与仲裁均基于多维度评分，并且所有维度、权重、阈值和评分标准均可在 `wiki_first_judge_prompts.py` 中追溯。
