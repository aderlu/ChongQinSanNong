# Phase14 真实问诊场景 SFT 字段改造记录

## 修改背景

此前生成链路的主要结果是 wiki 证据边界问答。CSV 中虽然有 `user_query` 和 `assistant_answer`，但 `user_query` 只是“猪场现场咨询/猪场兽医咨询”模板句，缺少真实问诊场景；`assistant_answer` 主要来自 `stage_2_grounded.answer`，容易变成证据锚点拼接文本，不像兽医问诊 agent 对养殖户的回答。

这会导致两个问题：

- 训练主样本不符合“用户提供具体病例场景，兽医问诊 agent 给出正确有效回答”的目标。
- Phase15、Phase18 裁判和仲裁围绕证据摘要打分，而不是围绕真实问诊回答打分。

## 修改前代码行为

- `phase14_generate_two_stage_samples.py` 只生成 `question`、`stage_1_draft.answer`、`stage_2_grounded.answer`。
- `question_for()` 使用固定模板生成简短问题，没有猪场背景、临床表现、用户诉求和信息缺口字段。
- `phase15_fact_level_evaluate_samples.py` 直接读取 `stage_2_grounded.answer` 做结构、事实、硬门控和风格检查。
- `phase18_dual_judge_and_arbitrate.py` 通过 `answer_for()` 读取 `stage_2_grounded.answer`，双裁判和仲裁没有看到真实场景回答。
- `phase16_export_layered_training_sets.py` 将 `question` 导出为 `user_query`，将 `stage_2_grounded.answer` 导出为 `assistant_answer` 或 `diagnosis`。

## 本次修改

- 在 `phase14_generate_two_stage_samples.py` 新增 `case_context`、`case_user_query`、`stage_2_grounded.clinical_answer`。
- 将 prompt 版本升级为 `phase14.two_stage.v4_cn_clinical_case`。
- Stage2 prompt 要求模型同时输出审计用 grounded answer 和主训练用 clinical answer。
- `case_context` 被定义为合成真实问诊上下文，只能提供病例场景和信息缺口，不能作为新增疾病事实来源。
- `clinical_answer` 被定义为主训练结果，要求像兽医问诊 agent 回答真实猪场用户，包含场景回应、判断边界、补充问诊/检测建议、风险提醒和证据依据。
- 在 `phase15_fact_level_evaluate_samples.py` 中新增 `answer_for()` 和 `query_for()`，优先评估 `clinical_answer` 与 `case_user_query`。
- 在 `phase18_dual_judge_and_arbitrate.py` 中让双裁判和仲裁优先读取 `clinical_answer`，并围绕 `case_user_query` 判断风险触发。
- 在 `wiki_first_judge_prompts.py` 中将裁判角色从 wiki 摘要评估调整为 veterinary consultation SFT sample review。
- 在 `phase16_export_layered_training_sets.py` 中新增导出字段 `case_context`、`case_user_query`、`grounded_audit_answer`，并让 `user_query`、`assistant_answer` 使用真实问诊主链路字段。

## 约束调整

本次不是取消 wiki 约束，而是区分两类信息：

- `case_context`：合成病例上下文，用于构造真实问诊语境和用户诉求。
- `clinical_answer` 中的疾病知识结论：仍必须回到 evidence anchors，保留 source/rule/fact/page 引用。

这样可以缓解“约束过强导致回答只剩证据串”的问题，同时避免模型借合成场景杜撰疾病事实、用药方案或监管动作。

## 预期效果

- 新批次 CSV 会包含真实问诊场景字段。
- 训练主版本的 `user_query` 会变成完整场景咨询，而不是一句模板问题。
- 训练主版本的 `assistant_answer` 会变成兽医问诊 agent 风格回答，而不是单纯审计答案。
- Phase15、Phase18、仲裁会围绕真实问诊回答进行质量判断。
- `grounded_audit_answer` 仍保留，方便追溯 wiki 证据边界和审计。

## 防乱码措施

- 所有修改文件保持 UTF-8 编码。
- JSON/CSV 写入继续使用 `encoding="utf-8"` 或 UTF-8 兼容读取。
- 本次留痕文档使用 UTF-8 中文直接写入，避免 Windows ANSI 编码。

