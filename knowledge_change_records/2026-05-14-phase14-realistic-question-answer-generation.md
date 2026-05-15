# 2026-05-14 Phase14 真实问诊问题与主回答生成改造记录

## 修改背景

此前 Phase14 已能生成两阶段回答，但用户问题和主回答仍容易受知识库审计结构影响，表现为问题像检索题、回答像证据报告、主回答泄露 `source=`、`fact=`、`page=`、`rule=` 或实体编号。

这类数据即使事实正确，也不严格符合真实兽医问诊场景，会拉低 Phase18 中的真实性、问诊完整性、追问逻辑、可执行性和结构化可标注性。

## 修改前代码行为

目标文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py`

关联文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/consultation_case_variables.py`

修改前行为：

- `question_for()` 主要按能力层拼接知识型问题，用户真实身份、紧急程度和咨询目的影响不足。
- `stage_2_user_prompt()` 曾要求 `clinical_answer` 保留 `source/rule/fact/page` 锚点。
- `clinical_generation_user_prompt()` 禁止审计字段，但没有充分使用 Phase13 的问诊合同、可执行性等级和处方证据等级。
- `naturalize_clinical_answer()` 对裸露的审计字段和 `DIS-`、`RC-` 类编号清理不够完整。
- 输出样本未在顶层透传新增问诊变量，不便于 Phase16/Phase18 分析。

## 本次修改内容

更新内容：

- 将 `PROMPT_VERSION` 升级为 `phase14.two_stage.v5_realistic_consultation_contract`。
- `question_for()` 读取 `user_persona`、`consultation_intent`、`question_style`、`urgency_level`，优先生成问诊型问题。
- `scenario_for()` 输出新增问诊字段：
  - `user_persona`
  - `information_completeness`
  - `urgency_level`
  - `consultation_intent`
  - `misconception_type`
  - `question_style`
  - `actionability_level`
  - `prescription_support_level`
- `prompt_header()` 和 `stage_2_user_prompt()` 加入：
  - `consultation_generation_contract`
  - `main_answer_claims`
  - `audit_only_claims`
  - `boundary_claims`
- 修改 `stage_2_user_prompt()`，明确 `clinical_answer` 必须能追溯证据，但不得保留审计锚点；锚点只允许在 `stage_2_answer` 或 `evidence_anchors`。
- 强化 `clinical_generation_user_prompt()`：
  - 要求 2 到 4 个低风险现场动作。
  - 要求 3 到 6 个关键追问。
  - L5/L6 或 `boundary_or_refusal` 边界优先。
  - `prescription_support_level < P4` 时不得同时给出具体药名、剂量、疗程或休药期。
- 增强 `naturalize_clinical_answer()`，清理：
  - 方括号审计引用
  - 裸露 `source=`、`fact=`、`page=`、`rule=`、`anchor=`
  - `DIS-`、`RC-` 编号
  - `知识库`、`Wiki`、`目录页`、`证据锚点` 等审计话术
- 输出 sample 顶层新增问诊字段和 `generation_quality_flags`，方便后续 CSV 和质量分析。
- `consultation_case_variables.py` 改为优先使用 Phase12/Phase13 已规划的变量，缺失时才稳定回退生成。

## 解决的问题

- 解决问题生成过度知识库化的问题。
- 解决主回答和审计回答混淆的问题。
- 保留 `stage_2_answer` 的事实锚点，避免破坏 Phase15/Phase18 审计链路。
- 提高主回答作为 SFT 训练字段的自然度、问诊完整性和可执行性。
- 通过 `actionability_level` 和 `prescription_support_level` 控制低风险帮助与高风险边界之间的平衡。

## 预期效果

- `case_user_query` 更像养殖户、饲养员、场长或基层技术员的真实咨询。
- `clinical_answer` 更像兽医对猪场人员的回复，而不是知识库摘要。
- 审计字段泄漏应显著下降，理想目标为 0。
- 直接问药样本应体现“有帮助但不越界”的边界表达，而不是简单拒答或无证据处方。

## 编码与清理

- 所有修改文件继续使用 UTF-8。
- 未新增临时调试脚本。
- 未删除历史生成样本、评估报告或训练集文件，避免误伤既有工作留痕。
