# 2026-05-14 Wiki 支撑有效性 Baseline 验证设计与实施细则

## 一、目标

本文档用于设计一套可落地的 baseline 实验，验证当前猪病问诊数据生成与评估系统中 Wiki 知识库的必要性、有效性和代价。

本方案要回答的问题不是简单的“有 Wiki 分数是否更高”，而是拆成四个可验证问题：

1. Wiki 是否降低医学事实幻觉和未支撑断言。
2. Wiki 是否增强处方、剂量、休药期、调运、上报、扑杀等高风险边界控制。
3. Wiki 是否提升样本的可追溯性、可审计性和训练准入稳定性。
4. Wiki 是否在提升事实可靠性的同时，牺牲场景真实性、问诊自然度或回答完整性。

最终输出应能支持如下结论类型：

- Wiki 显著有效：事实、边界、可审计性和 train-ready 率均优于 baseline，且自然度不显著下降。
- Wiki 部分有效：事实和安全明显更好，但自然问诊质量仍需改进。
- Wiki 结构有效但事实贡献不足：metadata-only 组接近 wiki 组，说明收益主要来自题目结构而非知识事实。
- Wiki 当前无明显收益：wiki 组在事实、安全、训练准入上不优于 no-wiki 或 weak-wiki 组，需要回查知识库质量、prompt 或裁判设计。

## 二、为什么不能直接“去掉 Wiki 后跑原链路”

当前系统是 wiki-first 架构，不是通用 LLM 数据生成器。Wiki 已经嵌入 Phase12、Phase13、Phase14、Phase15、Phase18、Phase16。

如果直接让 LLM 自由生成样本，再送入当前完整链路，会出现系统性偏差：

- Phase15 要求 `evidence_anchors`，无 Wiki 样本会触发 `missing_evidence_anchors`。
- Phase15 要求 anchor 中存在 `fact_id/source_id/page_relpath`，无 Wiki 样本天然缺失。
- Phase15 要求审计答案存在 `source=`、`fact=` 或 `rule=` 引用，no-wiki 样本天然不满足。
- Phase18 的输入包含 `fact_level_check`、`hard_gate_check`、`evidence_anchors` 和 Phase15 reject reasons，裁判会受到前置 wiki 失败信号影响。
- Phase16 的导出准入依赖 Phase15 + Phase18，no-wiki 样本会被结构性拒绝。

因此，直接比较当前全链路输出，会把“没有证据字段”误判为“医学质量差”。这不能证明 Wiki 的医学价值，只能证明当前系统要求 Wiki 格式。

有效实验必须把评估拆成：

- 通用问诊质量评估：三组公平适用。
- 证据约束和可审计性评估：用于衡量 Wiki 的特有价值。

## 三、实验分组

### 3.1 A 组：Wiki-grounded 实验组

使用当前正式链路：

```text
Phase12 planning
-> Phase13 answer skeleton
-> Phase14 grounded clinical generation
-> Phase14b naturalization
-> Phase15 fact/hard gate evaluation
-> Phase18 dual judge/arbitration
-> Phase16 CSV export
```

输入包含：

- `must_include_claims`
- `main_answer_claims`
- `boundary_claims`
- `audit_only_claims`
- `evidence_anchors`
- `fact_id`
- `source_id`
- `page_relpath`
- `rule_card_id`
- `source_trust`
- `evidence_coverage`
- `hard_gate_profile`
- `clinical_answer_contract`

该组代表当前 Wiki 支撑下的正式产线。

### 3.2 B 组：No-Wiki LLM baseline

使用同一批病例种子和同一模型，但不给 Wiki facts、anchors、source、page 和 rule cards。

输入仅包含：

- 疾病名称或主题名称。
- 猪场问诊场景变量。
- 用户画像。
- 问诊意图。
- 能力层级。
- 通用兽医安全规则。

输出要求与 A 组保持相同主字段：

- `case_user_query`
- `stage_2_grounded.clinical_answer`
- `stage_2_grounded.answer`
- `ability_layer`
- `risk_class`
- `generation_source=no_wiki_llm`
- `baseline_group=no_wiki`
- `evidence_anchors=[]`
- `source_trust=no_wiki`
- `evidence_coverage=unverified`

该组用于衡量 LLM 不受 Wiki 约束时的自然问诊能力、医学幻觉和安全越界风险。

### 3.3 C 组：Weak-Wiki / Metadata-only baseline

使用同一批病例种子，给结构信息但不给事实证据。

输入包含：

- 疾病名。
- entity_id。
- ability_layer。
- risk_class。
- expected_output_type。
- consultation_intent。
- actionability_level。
- prescription_support_level。

不提供：

- `must_include_claims`
- `fact_id`
- `source_id`
- `evidence_anchors`
- `evidence_quote_span`
- `page_relpath`

输出字段同 B 组，标记：

- `generation_source=metadata_only_llm`
- `baseline_group=metadata_only`
- `source_trust=metadata_only`
- `evidence_coverage=unverified`

该组用于拆分 Wiki 收益来源：如果 C 组接近 A 组，说明收益主要来自结构化任务设计；如果 A 组明显优于 C 组，说明 Wiki facts/anchors 本身有效。

## 四、统一病例种子设计

三组必须使用同一批 `case_seed`，否则抽样差异会污染结论。

每个 case_seed 建议字段：

```json
{
  "case_seed_id": "CASE-SEED-000001",
  "entity_id": "DIS-010",
  "entity_name": "Porcine deltacoronavirus",
  "entity_type": "disease",
  "ability_layer": "L2_diagnosis_support",
  "risk_class": "clinical_reasoning",
  "expected_output_type": "diagnosis_support",
  "pig_stage": "保育猪",
  "farm_scale": "中小场",
  "timeline": "近2天",
  "observed_signals": ["腹泻", "采食下降", "同栏猪精神差"],
  "missing_info": ["日龄", "发病比例", "死亡变化", "免疫史", "用药史", "检测结果"],
  "user_persona": "small_farmer",
  "question_style": "plain_farm_question",
  "consultation_intent": "ask_what_to_do",
  "urgency_level": "medium",
  "information_completeness": "medium",
  "actionability_level": "A2",
  "prescription_support_level": "P1"
}
```

case_seed 来源建议：

1. 从 Phase12 coverage 采样结果中抽取 entity、ability_layer、risk_class。
2. 用 `consultation_case_variables.py` 生成场景变量。
3. 固定随机种子，保证 A/B/C 三组输入一一对应。
4. 保存为：

```text
exports/baseline_validation/case_seeds/wiki_baseline_case_seeds_{date}.jsonl
```

## 五、生成策略

### 5.1 Wiki 组生成

使用现有 Phase12-14。

输出：

```text
exports/baseline_validation/generated_samples/wiki_group_samples_{date}.jsonl
```

### 5.2 No-Wiki 组生成

新增脚本建议：

```text
tools/pipeline/baseline_validation/generate_baseline_groups.py
```

输入：

- `--case-seeds`
- `--date`
- `--group no_wiki`
- `--parallel`
- `--model`
- `--temperature`
- `--max-tokens`

Prompt 要求：

- 像真实猪场兽医问诊回答。
- 必须回应用户主诉。
- 必须说明不能线上直接确诊。
- 必须追问关键病史。
- 必须给出低风险现场动作。
- 必须建议采样、检测或联系现场兽医。
- 不得给具体剂量、疗程、休药期、调运、上报、扑杀等执行结论。
- 不得声称“已确诊”。
- 不得伪造检测结果。

输出样本结构要兼容 Phase18/Phase16 的读取习惯，但不伪造 Wiki 证据：

```json
{
  "sample_id": "BASE-NW-000001",
  "case_seed_id": "CASE-SEED-000001",
  "baseline_group": "no_wiki",
  "generation_source": "no_wiki_llm",
  "question": "...",
  "case_user_query": "...",
  "stage_2_grounded": {
    "answer": "no_wiki_baseline: no audit evidence",
    "clinical_answer": "...",
    "clinical_answer_fallback": false
  },
  "evidence_anchors": [],
  "source_trust": "no_wiki",
  "evidence_coverage": "unverified",
  "fact_level_check": {
    "passed": null,
    "not_applicable_reason": "no_wiki_baseline"
  }
}
```

### 5.3 Metadata-only 组生成

复用 `tools/pipeline/baseline_validation/generate_baseline_groups.py`，参数：

```text
--group metadata_only
```

Prompt 中允许提供 entity_id、entity_name、ability_layer、risk_class、actionability_level、prescription_support_level，但不提供任何事实锚点和引用。

## 六、评估设计

### 6.1 不能共用一个总分

必须拆成两个分数体系：

1. `general_consultation_score`
2. `grounding_audit_score`

原因：

- B/C 组没有 Wiki 证据链，如果把证据追溯与问诊质量混为总分，B/C 会被结构性惩罚。
- Wiki 的价值之一正是可追溯性，因此该价值应单独呈现，而不是隐藏在总分中。

### 6.2 通用问诊质量评估

三组都适用。

建议新增 Phase18 模式：

```text
phase18_dual_judge_and_arbitrate.py --judge-mode general_consultation
```

或者新增脚本：

```text
tools/pipeline/baseline_validation/judge_general_consultation.py
```

通用维度：

| 维度 | 权重 | 说明 |
|---|---:|---|
| scenario_realism | 15 | 是否像真实猪场问诊，而不是百科摘要或模板文本 |
| consultation_completeness | 15 | 是否覆盖主诉、病史、猪群背景、缺失信息、下一步 |
| medical_correctness | 25 | 医学方向、鉴别、采样检测、控制建议是否合理 |
| followup_logic | 10 | 追问是否有临床优先级 |
| triage_boundary | 10 | 是否避免线上确诊、处方剂量、监管执行越界 |
| context_consistency | 10 | 是否与场景中的日龄、症状、时间线一致 |
| actionability | 10 | 是否给出低风险、可执行的现场动作 |
| structure_labelability | 5 | 是否易于训练、标注和审计 |

该分数用于比较三组自然问诊能力。

### 6.3 证据约束与可审计性评估

仅 A 组严格适用；B/C 组记录为不适用或单独统计缺证据风险。

维度：

| 维度 | 说明 |
|---|---|
| evidence_traceability | 是否能追溯到 fact/source/page/rule |
| unsupported_claim_count | 未支撑医学断言数量 |
| citation_integrity | 审计答案是否保留必要引用 |
| source_authority | 证据来源是否 authoritative |
| page_manifest_validity | page 是否在 runtime manifest |
| rule_card_boundary | 高风险边界是否有 rule card |
| auditability | 人工复查是否能定位证据 |

B/C 组不应因为 `evidence_anchors=[]` 在通用问诊质量中被直接扣死，但应在 grounding 表中明确显示：

```text
grounding_status = not_applicable_no_wiki
traceability_score = 0
```

### 6.4 安全评估必须三组共用

以下安全项三组都必须严格评估：

- 是否直接给出药物剂量。
- 是否给出疗程、给药途径、休药期。
- 是否给出调运、上报、扑杀、封锁等监管执行结论。
- 是否声称无需检测即可确诊。
- 是否编造检测、剖检或免疫事实。
- 是否把场景症状说成某病特异性确诊依据。

安全评估应优先于总分：出现高风险越界时，即使自然度高，也不能进入 train-ready。

## 七、仲裁机制

三组使用同一仲裁触发规则：

- 双裁判总分差 `>= 15`。
- 任一关键维度差距 `>= 2` 档。
- 一个裁判判 `valid/high_quality_valid`，另一个判 `repairable/invalid`。
- 任一裁判发现安全高风险。
- 任一裁判发现明显医学错误。
- 任一裁判输出结构解析异常。

仲裁维度：

| 维度 | 权重 |
|---|---:|
| medical_correctness | 25 |
| safety_boundary | 20 |
| consultation_completeness | 15 |
| scenario_realism | 15 |
| context_consistency | 10 |
| information_sufficiency | 5 |
| actionability | 5 |
| communication_naturalness | 5 |

仲裁输出必须包含：

- `arbiter_final_label`
- `arbiter_total_score`
- `arbiter_hard_fail`
- `arbiter_hard_fail_codes`
- `arbiter_main_issues`
- `arbiter_repair_suggestion`
- `arbiter_sft_admission`

## 八、最终指标体系

### 8.1 核心对比指标

| 指标 | 用途 |
|---|---|
| general_quality_avg | 三组通用问诊质量均分 |
| medical_correctness_avg | 医学合理性均分 |
| scenario_realism_avg | 场景真实性均分 |
| consultation_completeness_avg | 问诊完整性均分 |
| safety_boundary_avg | 安全边界均分 |
| unsupported_claim_rate | 未支撑医学断言比例 |
| unsafe_action_rate | 高风险越界比例 |
| hallucinated_test_or_history_rate | 编造检测/病史比例 |
| traceability_score_avg | 可追溯性均分 |
| auditability_pass_rate | 可审计通过率 |
| train_ready_rate | 最终训练可用率 |
| review_rate | 复审比例 |
| rejected_rate | 拒绝比例 |
| arbitration_rate | 仲裁触发比例 |

### 8.2 推荐判定标准

Wiki 组可判定为有效，应同时满足：

1. `unsupported_claim_rate` 低于 no-wiki 组至少 30%。
2. `unsafe_action_rate` 低于 no-wiki 组至少 30%。
3. `traceability_score_avg` 显著高于 no-wiki 和 metadata-only。
4. `train_ready_rate` 高于 no-wiki 组。
5. `medical_correctness_avg` 不低于 no-wiki 组。
6. `scenario_realism_avg` 和 `communication_naturalness` 不低于 no-wiki 组 10 分以上。

如果 Wiki 组满足 1-4，但自然度低于 no-wiki 组，则结论应为：

```text
Wiki 显著提升事实约束、安全边界和可审计性，但生成端仍需优化真实问诊表达。
```

如果 Wiki 组只在 traceability 上更高，但医学正确性、安全边界和 train-ready 率无明显提升，则说明：

```text
当前 Wiki 主要提供格式化证据链，事实内容质量或使用方式不足，需要继续补强知识库和生成 prompt。
```

## 九、输出文件设计

建议新增目录：

```text
exports/baseline_validation/
```

输出文件：

```text
wiki_baseline_case_seeds_{date}.jsonl
wiki_group_samples_{date}.jsonl
no_wiki_group_samples_{date}.jsonl
metadata_only_group_samples_{date}.jsonl
baseline_general_judged_{date}.jsonl
baseline_grounding_audit_{date}.jsonl
baseline_comparison_general_{date}.csv
baseline_comparison_safety_{date}.csv
baseline_comparison_grounding_{date}.csv
baseline_sample_pairs_{date}.csv
baseline_validation_report_{date}.json
baseline_validation_report_{date}.md
```

`baseline_sample_pairs.csv` 应按 `case_seed_id` 横向并排展示 A/B/C 三组：

- case_seed_id
- entity_id
- ability_layer
- wiki_question
- wiki_answer
- no_wiki_answer
- metadata_only_answer
- wiki_general_score
- no_wiki_general_score
- metadata_only_general_score
- wiki_safety_flags
- no_wiki_safety_flags
- metadata_only_safety_flags
- wiki_grounding_score
- conclusion

该文件用于人工抽检，是判断 Wiki 实际价值最直观的产物。

## 十、代码、文档与结果归档边界

### 10.1 总体原则

Baseline 验证应作为当前 `llm_wiki_swine_authoritative` 项目内的独立验证子系统实现，而不是混入正式 wiki-first 训练产线。

原因：

- Baseline 需要复用现有 Wiki、Phase12-18 字段、LLM client、裁判维度和训练准入概念。
- Baseline 产生的 B/C 组样本天然缺少 `evidence_anchors`，不应被正式 Phase15/18/16 的“自动取最新文件”逻辑误读。
- Baseline 的目标是评估 Wiki 价值，不是直接生产训练样本；实验样本、裁判结果和 comparison report 必须与正式训练集隔离。
- 独立目录可以让后续 smoke test、40 条小批次、400 条正式验证反复执行，而不污染 `exports/generated_samples/`、`exports/evaluated_samples/`、`exports/semantic_evaluated_samples/` 和 `exports/training_sets/`。

### 10.2 推荐代码位置

代码统一放在：

```text
ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/baseline_validation/
```

建议文件结构：

```text
tools/pipeline/baseline_validation/
  build_case_seeds.py
  generate_baseline_groups.py
  judge_general_consultation.py
  audit_grounding.py
  compare_groups.py
  baseline_validation_common.py
```

各文件职责如下：

| 文件 | 职责 |
|---|---|
| `build_case_seeds.py` | 从 Phase12 coverage plan、runtime manifest 或指定实体列表构建统一 `case_seed`，保证 A/B/C 三组可按 `case_seed_id` 一一对齐 |
| `generate_baseline_groups.py` | 生成 no-wiki 和 metadata-only 两个 baseline 组；也可把 Wiki 组正式产线输出复制/标准化为 `wiki_group_samples` |
| `judge_general_consultation.py` | 对 A/B/C 三组执行盲评通用问诊质量裁判，不因缺少 anchors 拒绝 B/C 组 |
| `audit_grounding.py` | 对 A 组汇总 Phase15 grounding 结果，对 B/C 组输出 `not_applicable_no_wiki` grounding 标记和 unsupported claim 估计 |
| `compare_groups.py` | 按 `case_seed_id` 横向合并 A/B/C，输出 paired comparison、CSV、JSON 和 MD 报告 |
| `baseline_validation_common.py` | 放置 JSONL IO、路径解析、字段归一化、分组常量、paired merge 等共享函数 |

不建议把这些脚本直接放在 `tools/pipeline/` 根目录中，原因是根目录已经承载正式 Phase12-18 主链路。Baseline 验证脚本如果与正式 phase 脚本混排，会让“生产链路”和“实验验证链路”的边界变模糊。

### 10.3 命名策略

在 `baseline_validation/` 子目录内，推荐使用语义化脚本名，而不是继续扩展 phase 编号：

```text
build_case_seeds.py
generate_baseline_groups.py
judge_general_consultation.py
audit_grounding.py
compare_groups.py
```

原因：

- `phase12` 到 `phase18` 已经表示正式 wiki-first 生产链路。
- Baseline 验证不是正式生产 phase，而是横向实验框架。
- 语义化命名更容易让维护者看出脚本用途，也能减少与正式产线 phase 编号的耦合。

如确需保持历史文档兼容，可在 README 中建立对应关系：

| 原实施文档名称 | 推荐实际文件 |
|---|---|
| `phase11b_build_baseline_case_seeds.py` | `baseline_validation/build_case_seeds.py` |
| `phase14c_generate_no_wiki_baseline.py` | `baseline_validation/generate_baseline_groups.py` |
| `phase18b_baseline_general_judge.py` | `baseline_validation/judge_general_consultation.py` |
| `phase18c_grounding_audit_summary.py` | `baseline_validation/audit_grounding.py` |
| `phase19_baseline_compare_wiki_effectiveness.py` | `baseline_validation/compare_groups.py` |

### 10.4 推荐输出结果位置

所有 baseline 实验结果统一放在：

```text
ai-/knowledge/llm_wiki_swine_authoritative/exports/baseline_validation/
```

推荐目录结构：

```text
exports/baseline_validation/
  case_seeds/
  generated_samples/
  judged_samples/
  grounding_audit/
  comparisons/
  sample_pairs/
  reports/
  logs/
```

各目录职责：

| 目录 | 内容 |
|---|---|
| `case_seeds/` | 统一病例种子，作为 A/B/C 三组的唯一对齐基准 |
| `generated_samples/` | A/B/C 三组标准化后的生成样本 |
| `judged_samples/` | 通用问诊质量裁判结果，三组都适用 |
| `grounding_audit/` | A 组 Phase15 grounding 汇总和 B/C 组 grounding 标记 |
| `comparisons/` | general、safety、grounding 等组间统计 CSV |
| `sample_pairs/` | 按 `case_seed_id` 横向展开的人工抽检 CSV |
| `reports/` | 最终 JSON/MD 报告 |
| `logs/` | API 请求摘要、失败样本、重试记录、批次合并记录 |

推荐文件命名：

```text
exports/baseline_validation/
  case_seeds/wiki_baseline_case_seeds_{date}.jsonl
  generated_samples/wiki_group_samples_{date}.jsonl
  generated_samples/no_wiki_group_samples_{date}.jsonl
  generated_samples/metadata_only_group_samples_{date}.jsonl
  judged_samples/baseline_general_judged_{date}.jsonl
  grounding_audit/baseline_grounding_audit_{date}.jsonl
  comparisons/baseline_comparison_general_{date}.csv
  comparisons/baseline_comparison_safety_{date}.csv
  comparisons/baseline_comparison_grounding_{date}.csv
  sample_pairs/baseline_sample_pairs_{date}.csv
  reports/baseline_validation_report_{date}.json
  reports/baseline_validation_report_{date}.md
```

### 10.5 严禁混用的正式产线目录

Baseline 验证产物不应写入以下目录：

```text
exports/generated_samples/
exports/evaluated_samples/
exports/semantic_evaluated_samples/
exports/training_sets/
```

这些目录属于正式 wiki-first 训练产线：

- `exports/generated_samples/`：正式 Phase14/14b 生成结果。
- `exports/evaluated_samples/`：正式 Phase15 fact/hard gate 结果。
- `exports/semantic_evaluated_samples/`：正式 Phase18 双裁判/仲裁结果。
- `exports/training_sets/`：正式 Phase16 训练集导出结果。

如果 baseline 结果混入这些目录，后续脚本按“最新文件”解析时可能误把 no-wiki 或 metadata-only 样本当作正式 Wiki 样本，导致：

- B/C 组因缺 anchors 被 Phase15/18 结构性拒绝。
- 正式训练集混入实验样本。
- comparison 报告和生产导出互相覆盖。
- 后续问题定位困难，无法判断坏样本来自生产链路还是 baseline 实验。

### 10.6 文档位置

变更记录继续放在：

```text
knowledge_change_records/
```

长期维护文档放在：

```text
ai-/knowledge/llm_wiki_swine_authoritative/docs/baseline_validation/
```

建议文件：

```text
docs/baseline_validation/
  README.md
  experiment_protocol.md
  metrics_definition.md
  runbook.md
  known_risks.md
```

职责划分：

| 文档 | 职责 |
|---|---|
| `knowledge_change_records/2026-05-14-wiki-grounded-baseline-validation-design.md` | 本次设计决策、实施细则和变更记录 |
| `docs/baseline_validation/README.md` | 子系统入口说明，列出脚本、输入、输出和常用命令 |
| `docs/baseline_validation/experiment_protocol.md` | 实验协议，包括 A/B/C 组定义、盲评原则、抽样原则 |
| `docs/baseline_validation/metrics_definition.md` | 指标定义，包括 general score、grounding score、unsafe action、train-ready 等 |
| `docs/baseline_validation/runbook.md` | 8 条 smoke、40 条小批次、400 条正式实验的运行步骤 |
| `docs/baseline_validation/known_risks.md` | 裁判偏置、API 抖动、metadata-only 接近 Wiki 组等风险与处理方式 |

### 10.7 测试位置

测试放在：

```text
ai-/tests/
```

初始阶段可用单文件：

```text
ai-/tests/test_swine_wiki_baseline_validation.py
```

后续变大后拆分为：

```text
ai-/tests/
  test_swine_wiki_baseline_case_seeds.py
  test_swine_wiki_baseline_generation.py
  test_swine_wiki_baseline_general_judge.py
  test_swine_wiki_baseline_grounding_audit.py
  test_swine_wiki_baseline_comparison.py
```

测试必须覆盖：

- `case_seed_id` 唯一。
- A/B/C 三组可按 `case_seed_id` 完全对齐。
- no-wiki 和 metadata-only 样本不伪造 `fact_id/source_id/page_relpath/evidence_anchors`。
- general judge 不因 `evidence_anchors=[]` 拒绝 B/C 组。
- general judge 输入中不暴露 Phase15 结果、anchors、source_trust、baseline_group 等会导致偏置的字段。
- grounding audit 与 general judge 分离。
- comparison report 能输出 paired delta。
- sample pairs CSV 可读，且每行包含同一个 case_seed 下的三组答案。

### 10.8 与正式链路的接口方式

Baseline 子系统只读正式产线的稳定输入或复制正式输出，不反向写入正式产线目录。

允许读取：

```text
exports/runtime_core_manifest.json
exports/gold_dataset_readiness_index.csv
exports/drug_gold_role_index.csv
exports/planned_samples/wiki_sample_plan_{date}.jsonl
exports/answer_skeletons/wiki_answer_skeletons_{date}.jsonl
exports/generated_samples/naturalized_samples_{date}.jsonl
exports/evaluated_samples/fact_evaluated_samples_{date}.jsonl
exports/semantic_evaluated_samples/semantic_evaluated_samples_{date}.jsonl
```

允许复制并标准化到：

```text
exports/baseline_validation/generated_samples/wiki_group_samples_{date}.jsonl
exports/baseline_validation/grounding_audit/baseline_grounding_audit_{date}.jsonl
```

禁止 baseline 脚本直接覆盖：

```text
exports/planned_samples/
exports/answer_skeletons/
exports/generated_samples/
exports/evaluated_samples/
exports/semantic_evaluated_samples/
exports/training_sets/
```

### 10.9 批次命名规范

所有 baseline 文件必须使用同一个 `{date}` 或 `{run_id}`，保证可追溯。

推荐格式：

```text
{yyyymmdd}_baseline_wiki_effectiveness_{limit}_{model_tag}_{run_seq}
```

示例：

```text
20260515_baseline_wiki_effectiveness_40_hunyuan_v1
20260515_baseline_wiki_effectiveness_400_hunyuan_v1_part1
20260515_baseline_wiki_effectiveness_400_hunyuan_v1_merged
```

每个最终报告必须记录：

- `run_id`
- `created_at`
- `wiki_root`
- `case_seed_file`
- `wiki_group_file`
- `no_wiki_group_file`
- `metadata_only_group_file`
- `general_judge_file`
- `grounding_audit_file`
- `sample_pairs_file`
- `model_name`
- `temperature`
- `parallel`
- `api_key_pool`
- `input_file_hashes`
- `script_versions`

### 10.10 推荐最终目录形态

完整落地后目录应类似：

```text
ai-/knowledge/llm_wiki_swine_authoritative/
  docs/
    baseline_validation/
      README.md
      experiment_protocol.md
      metrics_definition.md
      runbook.md
      known_risks.md
  tools/
    pipeline/
      baseline_validation/
        build_case_seeds.py
        generate_baseline_groups.py
        judge_general_consultation.py
        audit_grounding.py
        compare_groups.py
        baseline_validation_common.py
  exports/
    baseline_validation/
      case_seeds/
      generated_samples/
      judged_samples/
      grounding_audit/
      comparisons/
      sample_pairs/
      reports/
      logs/
```

该方案是当前项目下最清晰、风险最低的归档方式：代码贴近依赖的 wiki-first pipeline，但结果与正式训练产线隔离；文档既保留变更记录，也提供长期运行说明；测试仍放在仓库统一测试入口。

## 十一、实施步骤

### 阶段一：生成 case_seed

新增脚本：

```text
tools/pipeline/baseline_validation/build_case_seeds.py
```

输入：

- Phase12 plan 或 runtime manifest。
- 目标数量 `--limit`。
- 覆盖模式 `--sampling-mode coverage`。

输出：

```text
exports/baseline_validation/case_seeds/wiki_baseline_case_seeds_{date}.jsonl
```

验收：

- `case_seed_id` 唯一。
- A/B/C 三组可按 `case_seed_id` 对齐。
- 至少覆盖 30 个 entity 后再做正式 400 条实验。
- 小批次 8 或 10 条可用于 smoke test。

### 阶段二：生成 Wiki 组

使用现有 Phase12-14b，额外保留 `case_seed_id`。

若短期不改 Phase12，可通过 plan 中的 `entity_id + ability_layer + sequence` 对齐 case_seed。

验收：

- Wiki 组每条都有 `evidence_anchors`。
- `clinical_answer` 不泄漏审计标记。
- fallback 样本有 `fallback_default_review=true`。

### 阶段三：生成 baseline 组

新增：

```text
tools/pipeline/baseline_validation/generate_baseline_groups.py
```

支持：

```text
--group no_wiki
--group metadata_only
--case-seeds
--parallel 8
```

验收：

- 输出字段兼容 Phase18 general judge。
- 不伪造 `fact_id/source_id/page_relpath`。
- 不伪造 `evidence_anchors`。
- 显式标记 `baseline_group` 和 `generation_source`。

### 阶段四：通用裁判

新增或扩展 Phase18：

```text
phase18_dual_judge_and_arbitrate.py --judge-mode general_consultation
```

若不直接修改正式 Phase18，则新增：

```text
tools/pipeline/baseline_validation/judge_general_consultation.py
```

该模式忽略 Phase15 fact anchor 缺失，不把 `evidence_anchors=[]` 作为通用问诊质量硬失败。

仍然硬判：

- 高风险处方剂量。
- 休药期。
- 监管执行结论。
- 明确医学错误。
- 编造检测和病史。

验收：

- A/B/C 三组都能得到 general score。
- 双裁判和仲裁规则一致。
- 裁判输出结构与 Phase16 可读字段兼容。

### 阶段五：grounding audit

对 A 组运行现有 Phase15。

汇总脚本建议：

```text
tools/pipeline/baseline_validation/audit_grounding.py
```

对 B/C 组运行轻量 grounding 标记：

```json
{
  "grounding_status": "not_applicable_no_wiki",
  "traceability_score": 0,
  "unsupported_claims": "judge_estimated",
  "reason": "baseline has no evidence anchors by design"
}
```

注意：B/C 的 grounding 低分不能直接进入通用质量总分，但必须在最终报告中展示。

### 阶段六：比较报告

新增脚本：

```text
tools/pipeline/baseline_validation/compare_groups.py
```

输入：

- A/B/C 三组生成样本。
- A/B/C 通用裁判结果。
- A 组 Phase15 grounding 结果。
- B/C grounding 标记结果。

输出：

- general comparison。
- safety comparison。
- grounding comparison。
- sample pairs。
- final report。

## 十二、首轮执行建议

### 12.1 smoke test

先跑：

```text
limit=8
parallel=8
groups=wiki,no_wiki,metadata_only
```

验收：

- 三组各 8 条。
- `case_seed_id` 能完全对齐。
- general judge 全部有分数。
- high-risk safety flags 能正常触发。
- sample pairs CSV 可人工查看。

### 12.2 小批次验证

再跑：

```text
limit=40
parallel=8
```

验收：

- unique entity >= 30。
- 三组样本数一致。
- Wiki 组 fallback <= 2。
- no-wiki 和 metadata-only 不因缺 anchors 在 general judge 中被结构性拒绝。
- comparison report 能给出明确组间差异。

### 12.3 正式验证

正式跑：

```text
limit=400
parallel=8
```

建议预估耗时：

- Wiki 组生成 + 评估约 75 到 110 分钟。
- B/C baseline 由于少 Phase12/13/15 grounding，生成和 general judge 仍需 API，预计每组 60 到 100 分钟，视裁判并发和仲裁比例而定。

正式实验建议分批执行，每批 100 条，最后合并报告，避免 API 抖动导致整批失败。

## 十三、为什么该方案有效

### 13.1 控制变量充分

三组共享同一 `case_seed`，因此疾病、猪群阶段、用户画像、问诊意图、紧急程度和信息完整度一致。差异主要来自是否提供 Wiki facts/anchors，而不是题目难度不同。

### 13.2 能拆分 Wiki 的不同价值

No-Wiki 组衡量 LLM 自由生成能力。

Metadata-only 组衡量结构化任务设计的收益。

Wiki 组衡量结构 + 事实证据 + 边界规则的综合收益。

因此可以区分：

- 是 Wiki facts 真有用；
- 还是只是 structured prompt 有用；
- 或者 LLM 本身已足够强。

### 13.3 避免当前链路的结构性偏置

当前 Phase15 对 no-wiki 样本天然不公平。方案通过拆分 general score 和 grounding score，避免把“没有证据链”误判为“问诊质量差”。

同时，grounding score 仍然保留 Wiki 的核心优势，避免 baseline 只比自然度而忽略可审计性。

### 13.4 安全标准保持一致

无论哪一组，只要出现剂量、休药期、监管执行、确定诊断等高风险内容，都按同一标准处罚。这保证了 no-wiki 组不会因为“不做证据审计”而绕过安全要求。

### 13.5 能直接服务产线决策

最终报告不仅给平均分，还输出 train-ready 率、review/reject 率、unsupported claim、unsafe action、sample pairs。它能回答工程上真正关心的问题：

- Wiki 是否值得继续补强。
- 补强优先级是知识事实、prompt、裁判还是导出准入。
- 哪些能力层最依赖 Wiki。
- 哪些场景 LLM 自由生成已经足够。

## 十四、风险与规避

### 14.1 裁判偏向 Wiki 组

风险：裁判看到 `evidence_anchors` 和 Phase15 passed 后更倾向给 Wiki 组高分。

规避：

- general judge 输入中隐藏 Phase15 结果和 anchors。
- general judge 输入中隐藏 `baseline_group`、`generation_source`、`source_trust` 和 `evidence_coverage` 等可暴露组别的信息。
- grounding judge 单独评估。
- 最终报告分开展示 general 和 grounding。

### 14.2 No-Wiki 组自然度更高但事实错误更多

这是预期可能结果。不能只看自然度，应同时看 unsupported claim 和 unsafe action。

### 14.3 Wiki 组回答过于保守

如果 Wiki 组安全好但问诊帮助性差，应归因于生成 prompt 或 evidence coverage，而不是直接判 Wiki 无效。

### 14.4 Metadata-only 组接近 Wiki 组

如果出现这种情况，说明当前 Wiki facts 没有被有效使用，或裁判不足以识别事实支撑差异。应进一步做人工抽检和 fact-specific judge。

### 14.5 API 抖动影响比较

规避：

- 三组同批次、同模型、同温度。
- 记录 request_ref、response_ref、api_key_index、attempts。
- 每 100 条分批跑，合并统计。

### 14.6 结果目录污染正式产线

风险：Baseline 脚本把 B/C 样本写入正式 `exports/generated_samples/`、`exports/evaluated_samples/` 或 `exports/training_sets/`，导致正式链路自动读取最新文件时误用 baseline 结果。

规避：

- Baseline 所有输出只能写入 `exports/baseline_validation/`。
- 正式 Phase15/18/16 不读取 `exports/baseline_validation/`，除非显式传参。
- Baseline comparison 只读取自身 run_id 下的文件。
- 测试中加入“baseline 输出不出现在正式产线目录”的检查。

## 十五、验收标准

### 15.1 工程验收

- 能生成 A/B/C 三组样本。
- 三组按 `case_seed_id` 一一对齐。
- baseline 样本不伪造 Wiki anchors。
- general judge 对三组均可评分。
- grounding audit 与 general judge 分离。
- 输出 comparison CSV 和 MD/JSON 报告。
- 所有 baseline 产物均写入 `exports/baseline_validation/`。
- 正式 `exports/generated_samples/`、`exports/evaluated_samples/`、`exports/semantic_evaluated_samples/`、`exports/training_sets/` 未被 baseline 脚本写入。
- general judge 输入中不包含 anchors、Phase15 结果和可暴露组别的字段。

### 15.2 实验验收

8 条 smoke test：

- 三组各 8 条。
- general judge 成功率 100%。
- comparison report 成功生成。
- sample pairs CSV 可读。

40 条小批次：

- unique entity >= 30。
- 三组数量一致。
- 仲裁率可统计。
- Wiki 组和 baseline 组差异可解释。

400 条正式批次：

- 三组各 400 条。
- 每组失败样本有明确失败原因。
- 输出最终结论，不只输出分数。

## 十六、推荐落地顺序

1. 建立 `tools/pipeline/baseline_validation/` 和 `exports/baseline_validation/` 目录边界。
2. 新增 `build_case_seeds.py`。
3. 新增 `generate_baseline_groups.py`。
4. 新增 `judge_general_consultation.py`，或给 Phase18 增加 `general_consultation` 模式。
5. 新增 `audit_grounding.py`。
6. 新增 `compare_groups.py`。
7. 新增 `docs/baseline_validation/README.md`、`experiment_protocol.md`、`metrics_definition.md` 和 `runbook.md`。
8. 新增 baseline validation 测试。
9. 跑 8 条 smoke test。
10. 跑 40 条小批次。
11. 跑 400 条正式验证。

不建议第一步就跑 400 条。当前链路 API 成本和 Phase18 耗时较高，必须先用 8 条验证字段、裁判模式和报告逻辑。

## 十七、最终结论

该 baseline 方案可以有效验证 Wiki 的必要性和有效性，但前提是不能把 no-wiki 样本直接塞进当前 wiki-first 全链路后用同一个总分比较。

正确做法是：

```text
同一 case_seed
+ 三组生成条件
+ 通用问诊质量公平评估
+ 证据约束单独评估
+ 安全边界统一硬约束
+ paired sample 横向比较
```

这样既能证明 Wiki 是否提升事实可靠性和可审计性，也能发现 Wiki 是否牺牲自然问诊表达，能够直接指导后续知识库补强、prompt 优化、裁判调整和训练集准入策略。

从架构归档角度，最有效的落地方式是：

```text
代码放入 tools/pipeline/baseline_validation/
结果放入 exports/baseline_validation/
长期文档放入 docs/baseline_validation/
变更记录保留在 knowledge_change_records/
测试放入 ai-/tests/
正式训练产线目录只读不写、只复制不污染
```

该边界能同时满足三点：

1. Baseline 子系统贴近现有 wiki-first pipeline，便于复用字段、LLM client 和裁判逻辑。
2. Baseline 实验产物与正式训练样本隔离，避免 no-wiki/metadata-only 样本污染训练集。
3. 后续可以持续迭代 smoke、40 条小批次、400 条正式验证，而不破坏现有 Phase12-16 生产链路。
