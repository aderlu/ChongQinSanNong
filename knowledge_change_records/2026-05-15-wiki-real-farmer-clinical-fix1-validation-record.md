# 2026-05-15 Wiki 组真实养殖户问诊质量修复与验证记录

## 背景问题

上一轮 30 条 smoke 验证显示，Wiki 组的 `user_query` 已经基本摆脱“实验室检测、剖检、发病比例”等专业术语泄漏，但 `assistant_answer` 仍存在两个需要继续收紧的问题：

1. 部分回答的鉴别诊断表达不够显性，自动门禁难以稳定识别“临床判断 + 鉴别方向”。
2. 个别用户问题里可能出现“心里没底”语义重复，影响真实养殖户问诊自然度。

如果不处理，会导致后续 500 条批量生成时出现两类风险：

1. 回答看起来仍偏模板化，虽然有建议，但不像一线兽医的临床式判断。
2. QA gate 报告无法准确区分“真实质量问题”和“规则未覆盖的自然表达”，影响验收判断。

## 本轮修改

### 1. Wiki 生成链路提示词增强

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14_generate_two_stage_samples.py`

调整内容：

- 要求 Wiki 组回答必须明确包含临床鉴别表达，例如“鉴别上”或“需要优先区分的是”。
- 强化回答结构：先给主要临床方向，再给依据、2-3 个鉴别方向、现场低风险动作、1-3 个关键追问。

预期效果：

- 减少“建议送检、联系兽医”式宽泛回答。
- 提高 `assistant_answer` 的临床判断密度和可用性。

### 2. 问诊变量自然度修正

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\consultation_case_variables.py`

调整内容：

- 将可见不确定描述从“现场只看到这些症状，心里没底”改为“现场只看到这些症状”。
- 保留外层模板中的自然表达“心里没底”，避免一句话里重复出现。

预期效果：

- 用户问题更像真实养殖户临时咨询，不再机械堆叠焦虑表达。

### 3. QA gate 临床表达识别补充

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\baseline_validation\qa_realism_gate.py`

调整内容：

- 将 `CLINICAL_JUDGEMENT_RE` 从只识别“首先考虑、倾向、需要警惕”等表达，补充为可识别“首先需要考虑、可能性较大、更倾向”等自然临床表达。

原因说明：

- Wiki fix1 smoke 中有一条回答使用了“首先需要考虑一些病毒性感染的风险，尤其是……可能性较大”，语义上是明确临床判断，但旧规则没有命中。
- 本次不是降低质量标准，而是让规则覆盖真实临床回答常见句式。

## 本轮运行

运行 ID：

- `20260515_real_farmer_clinical_smoke30_wiki_fix1`

真实链路：

- Phase12/13/14/14b/15/18/16 已完成 Wiki 组生成与评估。
- baseline general judge 已完成。
- grounding audit 已完成。

产物：

- Wiki 54 字段 CSV：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_wiki_20260515_real_farmer_clinical_smoke30_wiki_fix1.csv`
- QA gate 报告：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\reports\qa_realism_gate_wiki_20260515_real_farmer_clinical_smoke30_wiki_fix1.json`

CSV 汇总情况：

- 行数：30
- 字段数：54
- 缺失 judge：0
- 缺失 grounding：0

## 验证结果

QA gate 结果：

- `passed`: true
- `rows`: 30
- `query_hard_fail_rate`: 0.0%
- `professional_leakage_rate_user_query`: 0.0%
- `answer_hard_fail_rate`: 0.0%
- `generic_answer_rate`: 0.0%
- `clinical_judgement_rate`: 100.0%
- `differential_rate`: 100.0%
- `field_action_rate`: 100.0%
- `duplicate_user_query_extra_count`: 0
- `duplicate_assistant_answer_extra_count`: 0
- `user_query_length_avg`: 136.2
- `assistant_answer_length_avg`: 543.93

代码验证：

- `py -m pytest ai-\tests\test_real_farmer_clinical_qa_generation.py -q`
  - 结果：6 passed
- `py -m py_compile tools\pipeline\baseline_validation\qa_realism_gate.py`
  - 结果：通过

## 结论

Wiki 组本轮 30 条 smoke 已达到“真实养殖户问诊 + 临床式回答”的基本质量目标：

1. `user_query` 不再出现“实验室检测、剖检、采样送检、发病比例”等不符合普通养殖户表达的专业术语泄漏。
2. `assistant_answer` 能稳定给出临床方向、鉴别方向和现场可执行动作。
3. 54 字段 CSV 可以正常构建，并且 judge 与 grounding 字段没有缺失。

注意：

- 30 条 smoke 不能覆盖全部 73 个猪病知识库疾病；全量 500 条运行前，仍建议增加 `--allow-partial-coverage` 或明确 smoke 模式，避免覆盖率验收逻辑把小样本测试误判为失败。
- B/C 组在上一轮仍有 dict/list 内容泄漏风险，本轮按用户要求重点修复 Wiki 组，后续正式三组对比前应继续修复 B/C 组 fallback/prompt 输出格式。
