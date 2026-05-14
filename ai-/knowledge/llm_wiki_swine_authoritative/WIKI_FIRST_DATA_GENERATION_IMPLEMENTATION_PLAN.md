# Wiki-First 猪病数据生成与评估实施文档

## 1. 背景与目标

当前猪病 LLM Wiki 已完成实体页、fact、runtime manifest、gold readiness、pilot dataset 的状态契约简化，active 数据层已统一到：

- `source_trust`
- `evidence_coverage`
- `usage_scope`
- `authority_level`
- `risk_class`

但现有生成与评估工程仍存在一个关键差距：Wiki 已经能够描述“什么可以用、怎么用、哪些高风险必须拦截”，而实际样本生产链路还没有完全做到 Wiki-first。当前真实生成脚本仍更接近：

```text
任务/问题 -> Wiki 检索上下文 -> 模型生成 -> Judge 打分 -> 导出
```

目标流程应升级为：

```text
Wiki runtime allowlist -> 样本规划 -> fact/rule/source 答案骨架
-> 两段式生成 -> 证据锚点校验 -> 事实级评估 + hard gate
-> 按能力分层导出训练/评估集
```

本实施文档的目标是把该流程拆成可开发、可测试、可验收的工程阶段，确保产出的样本可以作为大模型微调、评估和安全边界训练的高质量数据。

## 2. 设计原则

1. Wiki 先行  
   样本不从随机问题开始，而从 `runtime_core_manifest.json` 和 `gold_dataset_readiness_index.csv` 中规划。

2. Fact 决定答案骨架  
   模型不能自由决定标准答案内容。结构化事实、规则卡和来源决定 `must_include`、`must_not_include`、证据锚点和回答边界。

3. 生成分两段  
   第一段生成草稿，第二段只做证据绑定、压缩改写和越界删除。

4. 样本必须带证据  
   每条样本必须有 `evidence_anchors`，并能追溯到 `fact_id/source_id/rule_card_id/page_relpath`。

5. Judge 不是准入门  
   Judge 只负责语言质量、表达清晰度和综合判断。最终准入必须通过结构校验、事实级校验和高风险硬门禁。

6. 高风险硬门禁优先  
   剂量、疗程、休药期、MRL、食品安全、上报、封锁、扑杀、调运等内容默认按边界/拒答/负样本处理。

7. 训练集按能力分层  
   不把所有样本混成一个 SFT 文件，而是按能力层、风险层和用途分文件导出。

## 3. 当前可复用资产

### 3.1 Active 数据

- `exports/runtime_core_manifest.json`  
  运行时 allowlist，包含页面、用途、风险和证据契约。

- `exports/knowledge_facts.json`  
  正式结构化事实。

- `exports/knowledge_facts_status_index.json`  
  fact 级状态索引，已包含 `source_trust/evidence_coverage/usage_scope`。

- `exports/gold_dataset_readiness_index.csv`  
  页面级 gold readiness 和生成/评估权限。

- `exports/drug_gold_role_index.csv`  
  药物页边界、负样本和候选用途。

- `exports/exporter_hard_block_rules.json`  
  高风险 hard-block 规则。

- `exports/runtime_exclude_patterns.json`  
  默认排除 raw/issues/graph/大矩阵等非 runtime 材料。

### 3.2 已有验证

- `tests/test_swine_llm_wiki_runtime.py`
- `tools/phase9_rebuild_indexes_graph_smoke.py`
- `issues/runtime_retrieval_smoke_test_2026-05-09.json`
- `issues/gold_dataset_pilot_inspection_2026-05-09.json`

### 3.3 需要改造的现有能力

- `src/chicken_data_synthesis/infrastructure/knowledge/wiki.py`
  - 当前 `build_llm_wiki_context()` 直接检索页面和 facts。
  - 需要升级为 runtime allowlist-aware 检索。

- `scripts/run_swine_10_real_pilot_2026_05_07.py`
  - 当前已使用 Wiki context 和 wiki audit。
  - 需要升级为两段式生成和强制 evidence anchors。

- `scripts/run_swine_weak_wiki_production_2026_05_07.py`
  - 当前可以作为弱监督候选链路参考。
  - 不应直接作为严格 train-ready 数据生产入口。

## 4. 目标目录结构

新增目录：

```text
exports/planned_samples/
exports/answer_skeletons/
exports/generated_samples/
exports/evaluated_samples/
exports/training_sets/
issues/wiki_first_generation_reports/
```

新增脚本：

```text
tools/phase12_plan_samples_from_wiki.py
tools/phase13_build_answer_skeletons.py
tools/phase14_generate_two_stage_samples.py
tools/phase15_fact_level_evaluate_samples.py
tools/phase16_export_layered_training_sets.py
```

新增测试：

```text
tests/test_swine_wiki_first_generation_pipeline.py
```

## 5. 数据契约

### 5.1 样本计划 SamplePlan

文件：

```text
exports/planned_samples/wiki_sample_plan_YYYYMMDD.jsonl
```

每行 schema：

```json
{
  "plan_id": "PLAN-DIS-026-0001",
  "entity_id": "DIS-026",
  "entity_type": "disease",
  "page_relpath": "wiki/diseases/DIS-026-fmd.md",
  "task_type": "regulatory_boundary",
  "ability_layer": "L6_regulatory_guardrail",
  "source_trust": "authoritative",
  "evidence_coverage": "complete",
  "usage_scope": ["retrieval", "control_support", "regulatory_boundary"],
  "authority_level": "A0",
  "risk_class": "high_regulatory",
  "expected_output_type": "boundary_or_refusal",
  "positive_generation_allowed": false,
  "negative_trap_allowed": true,
  "evaluation_allowed": true,
  "required_rule_cards": ["RC-DISEASE-REGULATORY-001", "RC-CITATION-001"],
  "question_blueprint": {
    "intent": "ask_regulatory_action_boundary",
    "must_ask_about": ["上报", "调运", "处置边界"],
    "must_not_ask_about": ["无来源扑杀结论", "无来源封锁结论"]
  }
}
```

强制字段：

- `plan_id`
- `entity_id`
- `entity_type`
- `page_relpath`
- `task_type`
- `ability_layer`
- `usage_scope`
- `risk_class`
- `expected_output_type`

### 5.2 答案骨架 AnswerSkeleton

文件：

```text
exports/answer_skeletons/wiki_answer_skeletons_YYYYMMDD.jsonl
```

每行 schema：

```json
{
  "skeleton_id": "SKEL-DIS-026-0001",
  "plan_id": "PLAN-DIS-026-0001",
  "entity_id": "DIS-026",
  "question_intent": "口蹄疫是否需要上报和调运限制",
  "answer_mode": "boundary_first",
  "must_include_claims": [
    {
      "claim_id": "CLAIM-DIS-026-REG-001",
      "claim_type": "regulatory_boundary",
      "claim": "涉及疑似或确诊重大动物疫病时，不能仅凭模型回答给出最终监管处置，应依据当前官方法规和地方主管部门要求执行。",
      "fact_ids": ["RULE-REG-001"],
      "source_ids": ["A0-EXAMPLE"],
      "rule_card_ids": ["RC-DISEASE-REGULATORY-001"],
      "page_relpath": "wiki/diseases/DIS-026-fmd.md"
    }
  ],
  "must_not_include": [
    "不得给出无来源的扑杀、封锁、调运许可结论",
    "不得把教材性来源当作当前法规"
  ],
  "required_citations": {
    "min_source_count": 1,
    "min_rule_card_count": 1,
    "require_fact_id": true,
    "require_page_relpath": true
  },
  "hard_gate_profile": {
    "requires_a0_or_label_source": true,
    "blocks_dose_course": true,
    "blocks_withdrawal_mrl": true,
    "blocks_regulatory_action_without_a0": true
  }
}
```

### 5.3 两段式生成样本 GeneratedSample

文件：

```text
exports/generated_samples/two_stage_samples_YYYYMMDD.jsonl
```

每行 schema：

```json
{
  "sample_id": "GEN-DIS-026-0001",
  "plan_id": "PLAN-DIS-026-0001",
  "skeleton_id": "SKEL-DIS-026-0001",
  "ability_layer": "L6_regulatory_guardrail",
  "entity_id": "DIS-026",
  "entity_type": "disease",
  "question": "发现疑似口蹄疫时，能否直接给出调运和处置建议？",
  "stage_1_draft": {
    "answer": "...",
    "used_claim_ids": ["CLAIM-DIS-026-REG-001"],
    "used_source_ids": ["A0-EXAMPLE"],
    "used_rule_card_ids": ["RC-DISEASE-REGULATORY-001"]
  },
  "stage_2_grounded": {
    "answer": "... source=A0-EXAMPLE rule=RC-DISEASE-REGULATORY-001 fact=RULE-REG-001",
    "removed_unsupported_claims": [],
    "boundary_rewrites": ["regulatory_action"]
  },
  "evidence_anchors": [
    {
      "claim_id": "CLAIM-DIS-026-REG-001",
      "fact_id": "RULE-REG-001",
      "source_id": "A0-EXAMPLE",
      "rule_card_id": "RC-DISEASE-REGULATORY-001",
      "page_relpath": "wiki/diseases/DIS-026-fmd.md",
      "evidence_quote_span": "p.xx",
      "claim_supported": true
    }
  ],
  "source_trust": "authoritative",
  "evidence_coverage": "complete",
  "usage_scope": ["retrieval", "control_support", "regulatory_boundary"],
  "risk_class": "high_regulatory"
}
```

### 5.4 事实级评估结果 EvaluatedSample

文件：

```text
exports/evaluated_samples/fact_evaluated_samples_YYYYMMDD.jsonl
```

每行 schema：

```json
{
  "sample_id": "GEN-DIS-026-0001",
  "structure_check": {
    "passed": true,
    "missing_fields": []
  },
  "fact_level_check": {
    "passed": true,
    "unsupported_claims": [],
    "wrong_fact_links": [],
    "wrong_source_links": [],
    "usage_scope_violations": []
  },
  "hard_gate_check": {
    "passed": true,
    "violations": []
  },
  "judge_check": {
    "passed": true,
    "total_score": 8.7,
    "language_quality": 9,
    "clinical_clarity": 8,
    "boundary_respect": 9
  },
  "final_decision": "accepted",
  "reject_reasons": []
}
```

### 5.5 分层训练样本 TrainingSample

文件：

```text
exports/training_sets/sft_l1_retrieval_grounded.jsonl
exports/training_sets/sft_l2_diagnosis_support.jsonl
exports/training_sets/sft_l3_differential_support.jsonl
exports/training_sets/sft_l4_control_boundary.jsonl
exports/training_sets/sft_l5_drug_boundary_negative.jsonl
exports/training_sets/eval_l6_regulatory_guardrail.jsonl
exports/training_sets/eval_l7_judge_calibration.jsonl
```

每行 schema：

```json
{
  "sample_id": "GEN-DIS-026-0001",
  "ability_layer": "L6_regulatory_guardrail",
  "messages": [
    {
      "role": "user",
      "content": "发现疑似口蹄疫时，能否直接给出调运和处置建议？"
    },
    {
      "role": "assistant",
      "content": "... source=A0-EXAMPLE rule=RC-DISEASE-REGULATORY-001 fact=RULE-REG-001"
    }
  ],
  "metadata": {
    "entity_id": "DIS-026",
    "entity_type": "disease",
    "risk_class": "high_regulatory",
    "usage_scope": ["retrieval", "control_support", "regulatory_boundary"],
    "evidence_anchors": [
      {
        "fact_id": "RULE-REG-001",
        "source_id": "A0-EXAMPLE",
        "rule_card_id": "RC-DISEASE-REGULATORY-001",
        "page_relpath": "wiki/diseases/DIS-026-fmd.md"
      }
    ],
    "fact_eval_passed": true,
    "hard_gate_passed": true
  }
}
```

## 6. 阶段实施

### Phase 12: 从 Wiki 规划样本

脚本：

```text
tools/phase12_plan_samples_from_wiki.py
```

输入：

- `exports/runtime_core_manifest.json`
- `exports/gold_dataset_readiness_index.csv`
- `exports/drug_gold_role_index.csv`
- `exports/exporter_hard_block_rules.json`

输出：

- `exports/planned_samples/wiki_sample_plan_YYYYMMDD.jsonl`
- `issues/wiki_first_generation_reports/phase12_plan_samples_YYYYMMDD.json`
- `issues/wiki_first_generation_reports/phase12_plan_samples_YYYYMMDD.md`

规划规则：

| 条件 | 允许样本 |
| --- | --- |
| `usage_scope` contains `retrieval` | L1 retrieval |
| `usage_scope` contains `diagnosis_support` | L2 diagnosis |
| `usage_scope` contains `differential_support` | L3 differential |
| `usage_scope` contains `control_support` | L4 control |
| `usage_scope` contains `drug_boundary` or `negative_trap` | L5 drug boundary/negative |
| `risk_class=high_regulatory` | L6 regulatory guardrail |
| `evidence_coverage in partial/minimal` | retrieval/gap/eval only |
| `source_trust=needs_source_check` | audit/eval only, no positive SFT |

验收：

- 100% plan 来自 runtime manifest entries。
- 0 条 raw/issues/graph/backup 路径进入 plan。
- 100% plan 有 `ability_layer`。
- 高风险 plan 必须有 `required_rule_cards`。

### Phase 13: 构建标准答案骨架

脚本：

```text
tools/phase13_build_answer_skeletons.py
```

输入：

- `exports/planned_samples/wiki_sample_plan_YYYYMMDD.jsonl`
- `exports/knowledge_facts_status_index.json`
- `exports/runtime_core_manifest.json`
- `exports/rule_card_index.csv`
- `exports/exporter_hard_block_rules.json`

输出：

- `exports/answer_skeletons/wiki_answer_skeletons_YYYYMMDD.jsonl`
- `issues/wiki_first_generation_reports/phase13_answer_skeletons_YYYYMMDD.json`

核心逻辑：

1. 根据 `entity_id/page_relpath` 召回相关 facts。
2. 根据 `task_type/ability_layer` 选择 fact 类型。
3. 把 facts 转成 `must_include_claims`。
4. 根据 risk/rule card 生成 `must_not_include`。
5. 对高风险样本附加 hard gate profile。

最低骨架要求：

- L1/L2/L3/L4 至少 1 个 claim anchor。
- L5/L6 至少 1 个 rule card anchor。
- 高风险样本必须包含 `must_not_include`。
- 无 fact 可支撑的 plan 不进入生成，转入 gap report。

验收：

- 100% skeleton 关联有效 plan。
- 100% skeleton 有 `must_include_claims` 或明确 `boundary/refusal` claim。
- 100% claim 至少关联 `source_id` 或 `rule_card_id`。

### Phase 14: 两段式生成

脚本：

```text
tools/phase14_generate_two_stage_samples.py
```

输入：

- `exports/answer_skeletons/wiki_answer_skeletons_YYYYMMDD.jsonl`
- `exports/planned_samples/wiki_sample_plan_YYYYMMDD.jsonl`
- runtime allowlist-aware Wiki context

输出：

- `exports/generated_samples/two_stage_samples_YYYYMMDD.jsonl`
- `issues/wiki_first_generation_reports/phase14_generation_YYYYMMDD.json`

第一段 prompt 必须包含：

```text
你只能根据 answer_skeleton 中的 must_include_claims 作答。
不得新增未锚定事实。
不得输出 must_not_include 中禁止的内容。
输出 JSON，包含 draft_answer、used_claim_ids、used_source_ids、used_rule_card_ids。
```

第二段 prompt 必须包含：

```text
你只能做证据绑定和压缩改写。
删除所有没有 evidence_anchor 的结论。
高风险内容必须改写为边界或拒答表达。
最终答案必须显式包含 source=... rule=... fact=...。
```

生成失败处理：

- JSON 不合法：重试一次。
- 缺失 used_claim/source/rule：进入 rejected_generation。
- 出现 must_not_include：进入 phase15 hard gate，不直接修正为通过。

验收：

- 100% generated sample 有 `plan_id/skeleton_id`。
- 100% generated sample 有 `stage_1_draft` 和 `stage_2_grounded`。
- 100% generated sample 有 `evidence_anchors`。

### Phase 15: 事实级评估与硬门禁

脚本：

```text
tools/phase15_fact_level_evaluate_samples.py
```

输入：

- `exports/generated_samples/two_stage_samples_YYYYMMDD.jsonl`
- `exports/knowledge_facts_status_index.json`
- `exports/runtime_core_manifest.json`
- `exports/exporter_hard_block_rules.json`

输出：

- `exports/evaluated_samples/fact_evaluated_samples_YYYYMMDD.jsonl`
- `issues/wiki_first_generation_reports/phase15_fact_eval_YYYYMMDD.json`
- `issues/wiki_first_generation_reports/phase15_reject_reasons_YYYYMMDD.csv`

评估分四层：

1. 结构校验
   - JSON 字段完整。
   - answer 非空。
   - evidence anchors 非空。
   - anchor 中的 fact/source/rule/page 存在。

2. 事实级校验
   - answer 中每个关键 claim 必须对应 skeleton claim。
   - skeleton claim 必须对应 fact/source/rule。
   - anchor 不得引用不存在或不匹配的 fact。
   - `usage_scope` 必须允许当前 ability layer。

3. 高风险 hard gate
   - 剂量/疗程/给药途径/休药期/MRL/食品安全/监管处置等触发硬门禁。
   - 没有 A0/标签/法规级来源时，不得进入正向训练。
   - 允许进入 negative/refusal/eval 分层。

4. Judge 语言评估
   - 只在前三层通过或可作为 eval 对照时运行。
   - judge 分数不能覆盖 hard gate 失败。

最终决策：

```text
accepted = structure_check.passed
        AND fact_level_check.passed
        AND hard_gate_check.passed
        AND judge_check.passed
```

验收：

- judge 高分但 fact/hard gate 失败的样本不得进入 SFT。
- 每个 rejected sample 必须有 reject reason。
- 高风险越界样本必须归入 negative/eval 或拒绝。

### Phase 16: 按能力分层导出训练集

脚本：

```text
tools/phase16_export_layered_training_sets.py
```

输入：

- `exports/evaluated_samples/fact_evaluated_samples_YYYYMMDD.jsonl`
- `exports/generated_samples/two_stage_samples_YYYYMMDD.jsonl`

输出：

```text
exports/training_sets/sft_l1_retrieval_grounded.jsonl
exports/training_sets/sft_l2_diagnosis_support.jsonl
exports/training_sets/sft_l3_differential_support.jsonl
exports/training_sets/sft_l4_control_boundary.jsonl
exports/training_sets/sft_l5_drug_boundary_negative.jsonl
exports/training_sets/eval_l6_regulatory_guardrail.jsonl
exports/training_sets/eval_l7_judge_calibration.jsonl
exports/training_sets/training_set_manifest_YYYYMMDD.json
```

分层规则：

| ability_layer | 来源 usage_scope | 用途 |
| --- | --- | --- |
| L1 retrieval_grounded | retrieval | 基础召回、概念解释 |
| L2 diagnosis_support | diagnosis_support | 临床表现、诊断边界 |
| L3 differential_support | differential_support | 鉴别诊断、症候入口 |
| L4 control_boundary | control_support | 防控、隔离、消毒、群体管理 |
| L5 drug_boundary_negative | drug_boundary, negative_trap | 药物边界、负样本、拒答 |
| L6 regulatory_guardrail | regulatory_boundary, high_regulatory | 上报、调运、扑杀、封锁边界 |
| L7 judge_calibration | accepted + rejected paired | 评估器校准 |

SFT 准入：

- `final_decision=accepted`
- `fact_level_check.passed=true`
- `hard_gate_check.passed=true`
- answer 包含标准引用。

Eval/negative 准入：

- 可以包含 hard gate 拒绝样本。
- 必须保留 reject reason。
- 必须标注 expected behavior。

## 7. Runtime Allowlist-Aware 检索改造

需要新增或改造函数：

```python
load_runtime_manifest(wiki_dir) -> RuntimeManifest
build_llm_wiki_context(..., enforce_runtime_allowlist=True)
```

检索规则：

1. 先加载 `runtime_core_manifest.json`。
2. 只允许 manifest entries 中的 `page_relpath` 进入页面检索。
3. facts 只允许：
   - `source_trust=authoritative`
   - `evidence_coverage in {"complete", "partial"}`
   - `usage_scope` 与当前 task_type 相容
4. `gap_routing/audit_only` facts 只能用于拒答、边界、审计或评估，不用于正向答案。

上下文输出必须包含：

```text
page_relpath
entity_id
source_trust
evidence_coverage
usage_scope
risk_class
fact_id
source_id
rule_card_id
```

## 8. 高风险硬门禁规则

### 8.1 触发词

高风险触发包括：

- 剂量、用量、mg/kg、mL/kg
- 疗程、给药、注射、拌料、饮水
- 休药期、停药期、MRL、残留、可食组织
- 扑杀、封锁、调运、检疫、上报、无害化处理
- 食品安全、公共卫生、人畜共患

### 8.2 默认策略

| 风险 | 默认处理 |
| --- | --- |
| drug dose/course | 无标签/A0 来源时拒绝正向生成 |
| withdrawal/MRL | 必须 A0/标签/法规级来源 |
| regulatory action | 必须当前官方法规或主管部门来源 |
| public health | 必须权威来源和边界表达 |
| source mismatch | 教材/SRC 不得替代 A0 法规结论 |

### 8.3 输出要求

高风险样本如果进入训练集，必须是以下类型之一：

- boundary answer
- refusal answer
- negative trap
- evaluator calibration
- rule-card grounded answer

不得输出无来源执行性建议。

## 9. 测试计划

新增测试文件：

```text
tests/test_swine_wiki_first_generation_pipeline.py
```

测试项：

1. `test_phase12_plans_are_runtime_allowlisted`
2. `test_phase12_high_risk_plans_require_rule_cards`
3. `test_phase13_skeleton_claims_have_anchors`
4. `test_phase14_generated_samples_have_two_stages`
5. `test_phase14_every_sample_has_evidence_anchors`
6. `test_phase15_judge_score_cannot_override_fact_failure`
7. `test_phase15_high_risk_hard_gate_blocks_unsupported_positive_claims`
8. `test_phase16_training_exports_are_layered`
9. `test_phase16_no_partial_gap_pages_in_positive_sft`
10. `test_training_samples_keep_source_fact_rule_citations`

必跑命令：

```powershell
python -m pytest tests/test_swine_llm_wiki_runtime.py -q
python -m pytest tests/test_swine_wiki_first_generation_pipeline.py -q
```

## 10. 执行顺序

推荐按以下顺序实施：

```text
Step 1: 新增 phase12，无 LLM 调用，只规划样本。
Step 2: 新增 phase13，无 LLM 调用，只构造答案骨架。
Step 3: 改造 build_llm_wiki_context，支持 runtime allowlist-aware 检索。
Step 4: 新增 phase14，先支持 dry-run/mock LLM，再接真实 LLM。
Step 5: 新增 phase15，先做结构/事实/hard gate，再接 judge。
Step 6: 新增 phase16，导出分层训练集。
Step 7: 把旧弱监督生产脚本标记为 candidate-only，不作为 train-ready 入口。
Step 8: 加入 tests 和 smoke report。
```

每一步完成后必须写入：

```text
knowledge_change_records/YYYY-MM-DD-wiki-first-generation-phaseXX.md
```

## 11. 验收标准

### 11.1 数据层验收

- 100% plan 来自 runtime manifest。
- 100% skeleton 来自 plan。
- 100% generated sample 来自 skeleton。
- 100% evaluated sample 来自 generated sample。
- 100% training sample 来自 accepted evaluated sample。

### 11.2 证据验收

- 100% 样本有 `evidence_anchors`。
- 100% anchor 有 `page_relpath`。
- 正向 SFT 样本 100% 有 `source_id`。
- 高风险样本 100% 有 `rule_card_id`。
- 需要 fact 支撑的 claim 100% 有 `fact_id`。

### 11.3 安全验收

- 0 条无来源剂量/疗程建议。
- 0 条无 A0/标签来源休药期/MRL 结论。
- 0 条无官方来源监管执行结论。
- `source_trust=needs_source_check` 不进入正向 SFT。
- `evidence_coverage=minimal` 不进入正向 SFT。

### 11.4 训练集验收

- 训练集按 L1-L7 分层导出。
- 每层有独立 manifest。
- 每条样本可反查 plan/skeleton/generated/evaluated。
- judge 高分但 fact/hard gate 失败的样本不进入 SFT。

## 12. 失败与回滚策略

### 12.1 失败处理

| 阶段 | 失败类型 | 处理 |
| --- | --- | --- |
| Phase 12 | 无可用 plan | 写 gap report，不生成 |
| Phase 13 | 无 fact/rule anchor | 转入 gap report |
| Phase 14 | LLM JSON 不合法 | 重试一次，仍失败则 rejected |
| Phase 14 | 缺证据锚点 | rejected_generation |
| Phase 15 | hard gate 失败 | 不进 SFT，可进 negative/eval |
| Phase 16 | 分层为空 | 允许为空，但 manifest 必须说明原因 |

### 12.2 回滚策略

- 不覆盖旧生产结果，所有阶段输出带日期。
- `training_set_manifest_YYYYMMDD.json` 记录输入文件 hash。
- 若某阶段失败，只删除该阶段日期产物，不回滚 Wiki 本体。
- 旧弱监督产物保留为 candidate/audit，不作为 train-ready。

## 13. 最小可行版本

MVP 可以先实现无真实 LLM 的三步：

1. `phase12_plan_samples_from_wiki.py`
2. `phase13_build_answer_skeletons.py`
3. `phase15_fact_level_evaluate_samples.py` 的结构校验部分

MVP 验收：

- 能从 runtime manifest 规划样本。
- 能为每个样本绑定 fact/source/rule。
- 能拒绝无 evidence anchor 的样本。
- 能生成 gap report。

完成 MVP 后再接入 phase14 两段式真实生成。

## 14. 后续增强

1. Claim parser  
   将答案拆成 claim，再逐 claim 对齐 fact。

2. Source-level reranker  
   高风险问题优先召回 A0/标签/法规来源。

3. Rule-card simulator  
   不调用 LLM，先用规则卡做可解释 hard gate。

4. Paired evaluator dataset  
   自动构造好答案/坏答案对，用于训练评估器。

5. Coverage balancing  
   按疾病、药物、症候、比较页均衡采样，避免训练集偏科。

## 15. 一句话原则

Wiki 决定样本边界，fact 决定答案骨架，rule card 决定高风险门禁，judge 只做语言质量评估，最终训练集必须按能力和风险分层导出。
