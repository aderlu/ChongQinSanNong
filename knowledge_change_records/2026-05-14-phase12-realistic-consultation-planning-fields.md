# 2026-05-14 Phase12 真实问诊规划字段改造记录

## 修改背景

此前 Phase12 主要按知识库页面、能力层、证据覆盖和风险类型规划样本，能够控制事实来源和边界层级，但缺少真实问诊所需的用户画像、信息完整度、紧急程度、咨询目的、误判倾向、问题风格、可执行性上限和处方支持等级。

这会导致后续 Phase14 只能靠 prompt 临场生成问诊场景，容易退化成知识库检索题、百科问答或单一模板问题。

## 修改前代码行为

目标文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase12_plan_samples_from_wiki.py`

修改前后续补丁中已经加入部分问诊变量，但存在两个需要修正的问题：

- `_stable_pick()` 使用 Python 内置 `hash()`，该值默认受进程随机盐影响，不同运行之间可能不稳定。
- `build_plans()` 对同一条 plan 重复调用 `build_blueprint()` 多次，逻辑冗余，也增加未来维护风险。
- Phase12 Markdown 报告只展示能力层、训练意图、证据深度，不能观察问诊画像分布。

## 本次修改内容

更新内容：

- 新增 `hashlib`，将 `_stable_pick()` 改为基于 `hashlib.blake2b` 的稳定哈希。
- 在 `build_plans()` 中每条 plan 只计算一次 `question_blueprint`，再从中透传新增问诊字段。
- 在 `write_report_md()` 中新增以下分布报告：
  - `user_persona_counts`
  - `urgency_level_counts`
  - `consultation_intent_counts`

涉及字段：

- `user_persona`
- `information_completeness`
- `urgency_level`
- `consultation_intent`
- `misconception_type`
- `question_style`
- `actionability_level`
- `prescription_support_level`

## 解决的问题

- 让同一知识库输入在重复运行时生成稳定的问诊变量，便于复现和对比。
- 让 Phase12 的计划结果从“知识任务规划”升级为“真实问诊样本规划”。
- 让报告层可以检查用户画像、紧急程度、咨询目的是否过度集中，便于后续调参。

## 预期效果

- Phase13 可以直接读取稳定的问诊变量并写入 skeleton 合同。
- Phase14 不再需要完全依赖 prompt 随机发挥，而是按计划生成多样但受控的真实问诊。
- 后续 10 条/40 条校准批次可以按画像和意图做质量分析。

## 编码与清理

- 文件继续使用 UTF-8 读写。
- 未新增临时脚本或冗余中间文件。
- 未清理历史实验产物，避免误删既有批次输出。
