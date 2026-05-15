# 2026-05-14 三子智能体并发实施记录：问诊 SFT 约束弱化与字段链路对齐

## 背景

本次工作依据 `2026-05-14-consultation-sft-constraint-relaxation-implementation-plan.md` 执行，目标是把猪病 LLM Wiki 的生成、评估、仲裁和导出链路，从“偏 wiki 审计”调整为“偏真实兽医问诊训练”，同时保持疾病知识仍可追溯到 wiki anchors。

## 原始问题

1. `Phase14` 生成结果偏模板化，`case_user_query` 不够像真实养殖户咨询。
2. `Phase15` hard gate 对合理问诊建议误杀偏多，特别是采样、PCR/ELISA、病程补充、免疫史追问等内容。
3. `Phase18` 裁判和仲裁仍偏审计视角，过于强调逐句 citation，压低了训练可用性。
4. 训练主 CSV 的真实问诊层、审计层、双裁判/仲裁字段链路不够清晰，缺少可汇报的字段来源说明。
5. 过程中存在重复函数、JSON 截断、真实模型输出不稳定和 UTF-8 乱码风险。

## 并发任务分工

### 子智能体 A

写入范围：
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/consultation_case_variables.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase13_build_answer_skeletons.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py`

任务目标：
- 建立通用真实问诊场景变量库。
- 弱化 Phase13/Phase14 过强结构约束。
- 让 `case_context` / `case_user_query` 更贴近真实场景，同时确保疾病事实仍由 wiki anchors 提供。

### 子智能体 B

写入范围：
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase15_fact_level_evaluate_samples.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/wiki_first_judge_prompts.py`

任务目标：
- 放宽合理问诊建议的 hard gate。
- 让双裁判和仲裁围绕 `case_user_query` / `clinical_answer` 评估。
- 将 scorecard 重点调整到 `question_resolution`、`training_utility`、`answer_completeness`、`language_naturalness`。

### 子智能体 C

写入范围：
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase16_export_layered_training_sets.py`
- `knowledge_change_records/` 下本次留痕说明文档

任务目标：
- 将训练主 CSV 的字段链路补齐到可汇报、可追踪。
- 保留 `case_context`、`case_user_query`、`assistant_answer`、`grounded_audit_answer`。
- 补齐双裁判、仲裁和阶段耗时字段的导出。

## 主要修改结果

### 生成侧

- 新增通用问诊变量库 `consultation_case_variables.py`。
- Phase14 接入合成场景变量，生成更真实的猪场咨询上下文。
- `case_context` 只负责描述场景和信息缺口，不再冒充疾病事实。
- `case_user_query` 融合场景、诉求和原始问题，更接近真实问诊表达。
- Phase14 默认 `max_tokens` 提升，降低长样本 JSON 截断风险。
- 清理了重复函数定义，减少维护冲突。

### 评估与仲裁侧

- Phase15 保留处方、剂量、休药期、监管执行等硬风险拦截。
- 新增合理问诊建议白名单，允许补充日龄、发病率、死亡率、病程、免疫史、采样、PCR/ELISA、剖检、联系兽医等内容。
- Phase18 的 prompt 和规则兜底都改为优先评价问诊可用性。
- 双裁判和仲裁对真实问诊结构的权重提升，减少把自然问诊误判成“审计不够严格”的问题。

### 导出侧

- 训练主 CSV 保留并强化：`case_context`、`case_user_query`、`assistant_answer`、`grounded_audit_answer`。
- 补齐双裁判、仲裁和耗时字段，方便做批次分析。
- 增加字段来源链路，便于汇报“每个字段来自哪一阶段”。

## 验证结果

- 关键脚本 `py_compile` 已通过。
- Phase18 self-test 通过，结果稳定。
- 子智能体 B 的内联验证确认：合理问诊建议不再被 A0/rule 误杀，药物剂量和休药期仍保持拒绝。
- 子智能体 A 的烟雾验证确认：`clinical_answer` 更接近真实问诊表达，而不是纯审计摘要。

## 预期效果

1. 训练样本会更像真实兽医问诊 agent 的对话，而不是 wiki 审计记录。
2. accepted 样本比例和训练可用性预计提升。
3. review/rejected 仍可保留高风险边界样本，不会丢失安全约束。
4. CSV 字段链路更完整，便于汇报和后续排查空字段。

## 残余风险

1. 真实 LLM 输出仍可能受上下文长度和中转站稳定性影响。
2. 个别复杂病例仍可能触发保守判定，需要后续批量统计确认。
3. 现有工作区中仍有大量历史产物文件，后续可继续做归档和清理。

## 相关文件

- [consultation_case_variables.py](D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/consultation_case_variables.py)
- [phase13_build_answer_skeletons.py](D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase13_build_answer_skeletons.py)
- [phase14_generate_two_stage_samples.py](D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py)
- [phase15_fact_level_evaluate_samples.py](D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase15_fact_level_evaluate_samples.py)
- [phase16_export_layered_training_sets.py](D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase16_export_layered_training_sets.py)
- [phase18_dual_judge_and_arbitrate.py](D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py)
- [wiki_first_judge_prompts.py](D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/wiki_first_judge_prompts.py)
