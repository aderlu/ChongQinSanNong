# 2026-05-14 300条疾病问诊批次 Phase12 规划过滤与变体扩展留痕

## 背景问题

用户要求采用八路并行生成300条真实猪病问诊CSV数据，并尽可能覆盖完整病例。首次按通用 coverage 方式规划 `20260514_stage5_formal300_v1` 时，虽然达到300条，但计划混入了 drug、rule_card 和大量 toc_only 页面：

- disease 194 条、drug 85 条、rule_card 21 条。
- substantive 181 条、thin 9 条、toc_only 110 条。

该规划不适合作为正式生成输入。原因是 drug/rule_card/toc_only 不能稳定支撑真实疾病问诊样本，容易造成病例覆盖被稀释、问答依据不足、数据真实性下降。

## 修改前代码状态

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase12_plan_samples_from_wiki.py` 原本主要依赖采样模式和 readiness 索引进行覆盖规划，缺少正式批次需要的硬过滤能力：

- 不能在命令行层面限定只选 disease。
- 不能在命令行层面限定只选 positive_sft。
- 不能在命令行层面限定只选 substantive。
- 当高质量疾病页面数量不足以直接达到300条时，缺少受控的问诊变体扩展机制。

## 本次修改

新增并启用以下能力：

- 新增 `filter_plans(...)`：按 entity_type、training_intent、evidence_depth 对 Phase12 候选计划做硬过滤。
- 新增 `apply_plan_variant(...)`：为同一疾病计划构造不同问诊变体，改变 user_persona、consultation_intent、urgency_level、ability_layer 等字段。
- 新增 `expand_plans_with_variants(...)`：在不引入低质量页面的前提下扩展样本数。
- 新增 CLI 参数：
  - `--entity-types`
  - `--training-intents`
  - `--evidence-depths`
  - `--max-variants-per-plan`

## 正式规划命令

```powershell
& 'C:\Users\admin\AppData\Local\Python\bin\python.exe' 'D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase12_plan_samples_from_wiki.py' --date 20260514_stage5_formal300_disease_v2 --limit 300 --sampling-mode coverage --max-plans-per-entity 6 --prefer-depth substantive --entity-types disease --training-intents positive_sft --evidence-depths substantive --max-variants-per-plan 3
```

## 修改后结果

输出计划：

`ai-/knowledge/llm_wiki_swine_authoritative/exports/planned_samples/wiki_sample_plan_20260514_stage5_formal300_disease_v2.jsonl`

Phase12 报告显示：

- planned_samples: 300
- entity_type: disease only
- training_intent: positive_sft only
- evidence_depth: substantive only
- unique_entities: 43
- unique_pages: 43
- substantive_plan_ratio: 1.0
- toc_only_plan_ratio: 0.0
- passed: true

能力层分布：

- L1_retrieval_grounded: 86
- L2_diagnosis_support: 72
- L3_differential_support: 72
- L4_control_boundary: 70

问诊意图分布：

- ask_disease: 62
- ask_drug: 67
- ask_risk: 66
- ask_sampling: 51
- ask_what_to_do: 54

## 解决的问题

本次修改解决了正式300条生成中的三个核心问题：

1. 防止低证据页面进入生成链路，减少无依据问答和模板化回答。
2. 保证样本主体集中在真实猪病病例，而不是药物说明或规则卡片。
3. 在当前仅43个实质疾病页面可用的约束下，通过问诊变体扩展达到300条，同时保持每条数据仍绑定疾病页面证据。

## 预期效果

- 正式批次的疾病覆盖更集中、更清晰。
- 后续 Phase14 生成不会被 toc_only 或非疾病页面拖低质量。
- CSV 中疾病分布应显著优于此前40条批次，不再只覆盖少数几个疾病。
- 最终验收时应同时检查通过率、疾病覆盖、重复度、字段结构、裁判/仲裁有效性。

## 边界说明

当前计划覆盖的是现有 wiki 中可用于生成的43个 substantive 疾病页面，不等同于覆盖全部73个疾病页面。未进入正式生成的页面主要因为证据深度不足或不适合直接生成 positive_sft 问诊数据。后续若继续补强 partial/thin/toc_only 页面，Phase12 可在同样过滤策略下扩展到更完整的疾病覆盖。
