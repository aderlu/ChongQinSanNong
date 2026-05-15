# 2026-05-14 Phase13 问诊 skeleton 合同改造记录

## 修改背景

此前 Phase13 的 skeleton 主要承载 `must_include_claims`、`required_citations`、`hard_gate_profile` 等证据和边界信息。这对审计有用，但不足以指导 Phase14 生成真实猪场问诊。

核心问题是 skeleton 没有明确区分“主回答可以自然表达的事实”和“只供审计追溯的事实”，也没有把用户画像、问题风格、紧急程度、可执行性和处方证据等级固化为生成合同。

## 修改前代码行为

目标文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase13_build_answer_skeletons.py`

修改前行为：

- `must_include_claims` 会整体进入后续生成，容易驱动模型把知识点硬塞进主回答。
- `clinical_answer_contract_for()` 曾要求主回答保留 `source/rule/fact/page` 锚点，不符合真实用户问诊。
- `must_not_include_for()` 主要关注医学和监管边界，未系统禁止审计字段泄漏。
- `case_generation_profile_for()` 未透传 Phase12 新增的问诊变量。

## 本次修改内容

新增和更新：

- 新增 `consultation_generation_contract_for(plan)`，把真实问诊生成要求写入 skeleton：
  - 用户画像
  - 问题风格
  - 信息完整度
  - 紧急程度
  - 咨询目的
  - 误判类型
  - `actionability_level`
  - `prescription_support_level`
  - 必须完成的问诊动作
  - 主回答禁止出现的审计痕迹
- 新增 `split_claims_for_consultation()`，把 claims 拆分为：
  - `main_answer_claims`
  - `audit_only_claims`
  - `boundary_claims`
- 在 skeleton 顶层透传 Phase12 新增字段，便于 Phase14 和后续 CSV 使用。
- 修改 `clinical_answer_contract_for()`，明确主回答不暴露 `source/rule/fact/page`，证据锚点只保留在 `stage_2_answer`、`evidence_anchors` 或审计字段。
- 扩展 `must_not_include_for()`，加入：
  - `source=`
  - `fact=`
  - `page=`
  - `rule=`
  - `DIS-`
  - `知识库`
  - `引用锚点`

## 解决的问题

- 解决 skeleton 只像证据清单、不像问诊合约的问题。
- 降低主回答堆事实、露锚点、模板腔的概率。
- 保留审计追溯能力，同时避免污染 SFT 主训练视图。
- 让 L5/L6 高风险样本明确边界优先，避免为了可执行性越界。

## 预期效果

- Phase14 可依据 `consultation_generation_contract` 生成更接近真实猪场用户的问答。
- 主回答只吸收少量核心事实和边界表达，审计事实仍保留在结构化字段。
- 处方类内容受 `prescription_support_level` 约束，无 P4 证据时不应产生精确剂量、疗程和休药期。

## 编码与清理

- 文件继续使用 UTF-8。
- 未新增临时脚本。
- 未删除历史 skeleton 产物，避免破坏既有实验记录。
