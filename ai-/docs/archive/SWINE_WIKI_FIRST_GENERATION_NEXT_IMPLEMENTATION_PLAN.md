# 猪病 Wiki-first 数据生成与评估下一步实施方案

生成日期：2026-05-13

## 1. 背景与当前状态

当前猪病数据生成与评估工程已经形成可运行的 Wiki-first 闭环：

```text
Phase12 从 Wiki 运行清单规划样本
  -> Phase13 用结构化事实生成标准答案骨架
  -> Phase14 两段式生成样本并写入证据锚点
  -> Phase15 执行结构、事实、证据锚点和高风险硬门禁评估
  -> Phase16 按能力层导出训练集和评估集
```

已落地能力包括：

- 样本规划来自 `runtime_core_manifest.json`、`gold_dataset_readiness_index.csv`、`drug_gold_role_index.csv`、`exporter_hard_block_rules.json`。
- 标准答案骨架来自 `knowledge_facts_status_index.json` 中的结构化事实。
- 每条样本携带 `evidence_anchors`，包含 `fact_id`、`source_id`、`rule_card_id`、`page_relpath`。
- Phase15 已经能够检查事实链接、来源可信度、证据覆盖、能力范围、引用标记和高风险硬门禁。
- Phase16 已经按 L1-L7 能力层导出数据。

但当前流程仍有两个关键缺口：

- Phase14 主流程仍以 `deterministic_dry_run_mock` 为主，真实 LLM 生成只在旁路脚本中跑过 30 条样本验证。
- Phase15 的 `judge_check` 仍是 `deterministic_placeholder`，尚未接入真实双裁判和仲裁。

因此下一步目标不是重新搭建闭环，而是把当前闭环升级为可规模化生产高质量训练数据的质量闭环。

## 2. 总体目标

下一阶段目标是实现：

```text
Wiki 约束规划
  -> 结构化事实答案骨架
  -> 真实 LLM 两段式生成
  -> 确定性事实/硬门禁评估
  -> 双裁判语义评估
  -> 仲裁
  -> 分层训练集准入
  -> 质量报告与回流修复
```

核心原则：

- Wiki 是生成边界，不是事后参考。
- 结构化事实决定标准答案骨架。
- LLM 负责语言化和问答多样性，不能自由扩写事实。
- 事实校验和硬门禁先于 judge。
- judge 只评估规则无法覆盖的临床语义质量、表达质量和安全边界清晰度。
- 高风险内容必须由硬门禁兜底，不能交给 judge 自由判断。

## 3. 实施阶段

### Phase17：真实 LLM 两段式生成主流程

目标：把真实 API 生成从旁路验证脚本升级为主生产能力。

新增或改造文件：

- `knowledge/llm_wiki_swine_authoritative/tools/phase14_generate_two_stage_samples.py`
- 新增可选模块：`knowledge/llm_wiki_swine_authoritative/tools/wiki_first_llm_client.py`
- 新增报告：`knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/phase17_real_generation_<date>.json`

实现要求：

- 保留当前确定性生成模式，作为 `--mode dry-run`。
- 新增 `--mode real-api`。
- 输入仍为 Phase13 skeleton 和 Phase12 plan。
- 每次 API 调用必须传入：
  - `question_blueprint`
  - `must_include_claims`
  - `must_not_include`
  - `required_citations`
  - `hard_gate_profile`
  - `evidence_anchors`
- 输出必须包含：
  - `stage_1_draft`
  - `stage_2_grounded`
  - `evidence_anchors`
  - `generation_model`
  - `generation_mode`
  - `generation_prompt_version`
  - `raw_generation_ref`

两段式生成定义：

```text
Stage 1：只根据 skeleton 生成临床自然语言草稿，不允许新增事实。
Stage 2：对 Stage 1 做 grounding rewrite，把每个关键结论绑定到 fact/source/rule/page；不能绑定的内容必须删除或改写为证据边界。
```

验收标准：

- 100% 样本保留 `plan_id`、`skeleton_id`、`ability_layer`。
- 100% 样本有 `evidence_anchors`。
- 100% `stage_2_grounded.answer` 含有所需引用标记。
- `dry-run` 与 `real-api` 都能通过现有测试。
- 真实 API 生成 100 条样本后，Phase15 接受率不低于 75%。

### Phase18：双裁判与仲裁接入 Phase15 后置评估

目标：在确定性事实/硬门禁评估之后，增加真实语义质量评估。

新增文件：

- `knowledge/llm_wiki_swine_authoritative/tools/phase18_dual_judge_and_arbitrate.py`
- `knowledge/llm_wiki_swine_authoritative/tools/wiki_first_judge_prompts.py`

复用参考：

- `scripts/dual_review_select_swine_weak_wiki_2026_05_07.py`
- `scripts/run_swine_weak_wiki_production_2026_05_07.py`

执行位置：

```text
Phase15 输出 evaluated_samples
  -> 只对 hard_gate_passed 且 fact_level_check passed 的样本执行 judge
  -> judge_a
  -> judge_b
  -> 必要时 arbiter
  -> 输出 semantic_evaluated_samples
```

Judge A 评估维度：

```text
clinical_correctness 30
reasoning_consistency 20
wiki_grounding_fidelity 20
safety_boundary_clarity 20
training_usability 10
```

Judge B 评估维度：

```text
safety_risk 30
unsupported_expansion 25
answer_completeness 20
language_quality 15
dataset_fit 10
```

仲裁触发条件：

- `judge_a.final_label != judge_b.final_label`
- 两个裁判分差 `>= 8`
- 任一裁判标记 `fatal_risk=true`
- L5/L6 高风险样本
- Phase15 存在非致命 warning
- judge 对 `unsupported_expansion` 或 `safety_boundary` 判断不一致

最终标签：

```text
accepted：Phase15 全通过，双裁判均 pass，且无 fatal
review：Phase15 通过，但 judge 分歧或轻微质量问题
rejected：Phase15 未通过，或任一硬门禁失败，或仲裁判定不可用
```

硬规则：

- Phase15 hard gate 失败的样本不得被 judge 或 arbiter 改为 accepted。
- 缺少证据锚点的样本不得进入 judge。
- L5/L6 样本即使 judge 通过，也必须保留边界/拒答表达。

验收标准：

- Phase18 输出每条样本的 `judge_a_result`、`judge_b_result`、`arbiter_result`、`semantic_final_decision`。
- 所有进入训练集的样本必须同时满足：
  - `final_decision=accepted`
  - `semantic_final_decision=accepted`
  - `hard_gate_check.passed=true`
- 对 100 条真实生成样本执行评估，人工抽检 20 条，严重误放率为 0。

### Phase19：训练集准入策略升级

目标：让 Phase16 不再只看 Phase15 的 deterministic accepted，而是同时看 Phase18 的语义评估。

改造文件：

- `knowledge/llm_wiki_swine_authoritative/tools/phase16_export_layered_training_sets.py`

准入条件：

```text
SFT 训练集：
  Phase15 accepted
  Phase18 accepted
  no reject_reasons
  no fatal_risk
  ability_layer in L1-L5

评估集：
  Phase15 accepted 或 review
  Phase18 accepted 或 review
  ability_layer in L6-L7

拒绝样本池：
  Phase15 rejected 或 Phase18 rejected
  保留 reject_reasons、judge weaknesses、arbiter reason
```

导出目标：

- `sft_l1_retrieval_grounded.jsonl`
- `sft_l2_diagnosis_support.jsonl`
- `sft_l3_differential_support.jsonl`
- `sft_l4_control_boundary.jsonl`
- `sft_l5_drug_boundary_negative.jsonl`
- `eval_l6_regulatory_guardrail.jsonl`
- `eval_l7_judge_calibration.jsonl`
- `rejected_with_reasons.jsonl`
- `review_queue.jsonl`

验收标准：

- L5 训练集不得包含 rejected 样本。
- L6 默认进入 eval，不直接进入 SFT。
- 每条导出样本保留完整 provenance。
- 每个导出文件生成对应 summary，统计来源、能力层、风险层、拒绝原因。

### Phase20：质量回流与 Wiki 缺口修复队列

目标：把生成/评估失败原因转化为 Wiki 修复任务，而不是只丢弃样本。

新增文件：

- `knowledge/llm_wiki_swine_authoritative/tools/phase20_build_quality_feedback_queue.py`

输入：

- Phase15 reject reasons
- Phase18 judge weaknesses
- Phase18 arbiter required_fix
- real API quality analysis report

输出：

- `issues/wiki_first_generation_reports/wiki_quality_feedback_queue_<date>.jsonl`
- `issues/wiki_first_generation_reports/wiki_quality_feedback_summary_<date>.md`

回流类别：

```text
missing_fact_anchor
missing_a0_source
source_trust_not_authoritative
evidence_coverage_partial
usage_scope_mismatch
rule_card_missing
entity_page_needs_fact_expansion
prompt_generation_drift
judge_disagreement
```

验收标准：

- 每个 rejected 样本至少归因到一个可行动问题。
- 能区分 Wiki 数据缺口、生成模型问题、评估规则问题。
- 支持按实体页聚合修复优先级。

## 4. 推荐执行顺序

第一轮实施：

```text
Phase17 real-api 主流程
Phase18 双裁判仲裁
Phase19 训练集准入升级
```

第二轮实施：

```text
Phase20 质量回流
真实 API 100 条验证
人工抽检 20 条
修复 Wiki 缺口
真实 API 300 条验证
```

原因：

- Phase17 先解决样本自然语言质量和多样性。
- Phase18 再补临床语义质量判断。
- Phase19 把评估结果真正接到训练集准入。
- Phase20 最后把失败样本变成 Wiki 改进任务。

## 5. 测试计划

新增测试：

- `tests/test_swine_wiki_first_real_generation.py`
- `tests/test_swine_wiki_first_dual_judge.py`
- `tests/test_swine_wiki_first_training_admission.py`

必须覆盖：

- dry-run 兼容性。
- real-api 输出结构完整性。
- 缺失 evidence anchor 的样本被拒绝。
- Phase15 hard gate 失败不能被 Phase18 改为 accepted。
- judge 分歧触发 arbiter。
- L5/L6 高风险样本强制仲裁或保守准入。
- Phase16 只导出 Phase15 和 Phase18 双通过样本。

命令：

```powershell
python -m pytest tests/test_swine_wiki_first_generation_pipeline.py -q
python -m pytest tests/test_swine_llm_wiki_runtime.py -q
python -m pytest tests/test_swine_wiki_first_dual_judge.py -q
```

## 6. 质量指标

短期门槛：

```text
真实 API 100 条：
  anchor_preserved_rate >= 95%
  phase15_accept_rate >= 75%
  phase18_accept_rate >= 65%
  high_risk_false_accept = 0
  missing_citation_rate = 0
```

中期门槛：

```text
真实 API 300 条：
  phase15_accept_rate >= 80%
  phase18_accept_rate >= 70%
  manual_serious_error_rate <= 2%
  l5_l6_boundary_violation = 0
```

训练集准入门槛：

```text
SFT:
  只允许 Phase15 accepted + Phase18 accepted

Eval:
  允许 accepted/review，但必须保留 judge 和 arbiter 元数据

Reject:
  不进入 SFT，不删除，进入质量回流队列
```

## 7. 风险与回退

风险一：真实 API 生成发散。

回退：

- 启用 `--mode dry-run`。
- 降低 temperature。
- 强制 Stage2 删除无锚点内容。
- 对 L5/L6 使用更严格边界模板。

风险二：双裁判成本高。

回退：

- 只对 Phase15 accepted 样本执行 judge。
- L1 可抽样 judge。
- L2-L6 全量 judge。
- L7 作为 judge calibration 专用集。

风险三：judge 与硬规则冲突。

回退：

- 硬门禁优先。
- Arbiter 不能覆盖 Phase15 hard gate failure。
- 所有冲突样本进入 review queue。

风险四：Wiki 数据不足导致正样本少。

回退：

- 增加边界/拒答样本比例。
- 生成 Wiki 缺口修复队列。
- 优先补 A0 来源、药物标签、法定疫病边界、鉴别诊断事实。

## 8. 最终完成定义

本阶段完成的判定标准：

- Phase17、Phase18、Phase19、Phase20 脚本全部存在并有测试覆盖。
- 可用一条命令或 runbook 跑通真实 API 100 条生产验证。
- 输出包含：
  - generated samples
  - Phase15 evaluated samples
  - Phase18 semantic evaluated samples
  - Phase16 layered training sets
  - review queue
  - rejected with reasons
  - Wiki quality feedback queue
- 高风险样本没有硬门禁漏放。
- SFT 导出集中没有 rejected 样本。
- 每条可训练样本都有 Wiki provenance、fact/source/rule/page 证据链。

