# 2026-05-14 Phase16 问诊字段与主回答导出衔接记录

## 修改背景

生成端新增了用户画像、问题风格、信息完整度、紧急程度、咨询目的、误判类型、可执行性等级和处方支持等级。如果 Phase16 不导出这些字段，后续 CSV 分析、质量汇报和分层抽检无法判断数据质量问题来自哪个场景变量。

同时，原训练 JSONL 的 `messages` 仍可能使用 `question` 和 `stage_2_grounded.answer`。其中 `question` 更接近内部任务问题，`stage_2_grounded.answer` 是审计回答，可能包含锚点，不适合作为主 SFT 对话。

## 修改前代码行为

目标文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase16_export_layered_training_sets.py`

修改前行为：

- `PRODUCTION_CSV_FIELDS` 和 `TRAINING_MAIN_CSV_FIELDS` 未包含新增问诊场景字段。
- `production_metadata()` 未透传 `consultation_generation_contract` 和 `generation_quality_flags`。
- `build_training_sample()` 的 JSONL messages 使用：
  - user: `generated.question`
  - assistant: `stage_2_grounded.answer`
- 这会让训练样本继续偏向知识库任务题和审计答案。

## 本次修改内容

新增 CSV 字段：

- `user_persona`
- `question_style`
- `information_completeness`
- `urgency_level`
- `consultation_intent`
- `misconception_type`
- `actionability_level`
- `prescription_support_level`

新增 metadata 内容：

- `consultation_generation_contract`
- `generation_quality_flags`
- 上述 8 个问诊场景字段

调整训练 JSONL：

- user 消息改为 `query_text_for(generated)`，优先使用 `case_user_query`。
- assistant 消息改为 `answer_text_for(generated)`，优先使用 `stage_2_grounded.clinical_answer`。
- `stage_2_grounded.answer` 继续保留为 `grounded_audit_answer`，不再作为主训练回答优先来源。

更新字段来源说明：

- 在 `training_main_field_source_map()` 中补充新增字段的来源。

## 解决的问题

- 解决 CSV 无法按真实问诊变量追踪质量的问题。
- 避免训练 JSONL 把审计答案作为 assistant 内容。
- 让 Phase16 与 Phase12/13/14/14b 的新字段链路闭合。
- 保留审计字段用于追溯，但主训练视图使用自然问诊问答。

## 预期效果

- 后续汇报可按用户画像、紧急程度、直接问药、处方支持等级分析样本质量。
- `main_sft` 和 `low_weight_sft` 的 messages 更接近真实猪场问诊。
- 对 L5/L6 样本，可以清楚追踪其可执行性和处方支持边界。

## 编码与清理

- CSV 继续使用 `utf-8-sig` 写出，降低 Excel 打开乱码风险。
- JSONL 继续使用 UTF-8 写出。
- 未新增临时脚本。
- 未清理历史导出文件，避免影响既有实验批次。
