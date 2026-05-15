# Phase13/Phase14 真实问诊骨架与提示词质量优化记录

## 修改背景

前一轮已经让结果 CSV 具备 `case_context`、`case_user_query` 和 `clinical_answer`，但生成质量仍主要依赖 Phase14 临时构造场景。Phase13 生成的 answer skeleton 只有事实 claim、禁用项和 citation 规则，没有明确告诉下游：

- 这是兽医问诊 agent 的 SFT 样本。
- 场景应该包含哪些病例槽位。
- 主回答应该有哪些训练价值要素。
- 合成病例上下文和 wiki 权威事实之间的边界是什么。

因此模型容易退化成“证据摘要+保守边界”，而不是“真实问诊场景问答”。

## 修改前问题

- `phase13_build_answer_skeletons.py` 输出的 skeleton 缺少问诊场景配置。
- `phase14_generate_two_stage_samples.py` 只能根据 ability layer 写固定场景句，场景多样性和真实感不足。
- Prompt 虽要求自然回答，但没有把“主训练答案 contract”作为结构化输入。
- 兜底回答仍容易回到审计式证据串。

## 本次修改

- 在 Phase13 skeleton 中新增 `case_generation_profile`。
- 在 Phase13 skeleton 中新增 `clinical_answer_contract`。
- `case_generation_profile` 定义场景目标、必备病例槽位、应追问的信息主题和合成上下文边界。
- `clinical_answer_contract` 定义主训练回答字段、风格要求、必须语义覆盖的回答要素和禁止项。
- Phase14 的 `scenario_for()`、`case_user_query_for()`、prompt payload 已读取上述骨架字段。
- Stage2 prompt 明确要求 `clinical_answer` 严格遵守 `clinical_answer_contract`。
- Stage2 prompt 强化“不要一上来堆引用、不要只说不能回答、引用放关键结论或文末证据依据”的质量要求。
- 默认兜底回答改成问诊 agent 风格，包含现场回应、证据边界、补充信息建议和执行性结论边界。

## 修改效果预期

- 新生成 skeleton 自带问诊样本质量契约。
- Phase14 不再只依赖硬编码场景模板，而是根据骨架生成更明确的真实问诊场景。
- CSV 中 `case_user_query` 更像真实用户输入。
- `assistant_answer` 更适合微调兽医问诊 agent，减少机械证据串和过度拒答。
- `grounded_audit_answer` 仍保留，用于审计和裁判追溯。

## 防乱码措施

- 所有新增文档和代码均保持 UTF-8。
- 命令行验证使用 `PYTHONIOENCODING=utf-8` 和 PowerShell UTF-8 输出设置。
- 未使用 ANSI 编码写入中文内容。

