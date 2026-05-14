# 2026-05-14 v2 Scorecard 校准与训练主版本字段体系说明

## 一、修改背景

本次任务目标是把 `wiki_first_g_eval_v2` 评分卡校准到真实批次中能够产生合理的 `accepted / review / rejected` 分布，并补充一份专门说明文档，解释训练主版本 CSV 的完整字段结构、评分体系来源、字段与数据生成/评估流程的对应关系。

修改前主要存在以下问题：

1. `Phase18` v2 scorecard 的总分聚合逻辑存在“重复加权”风险。各维度分数本身已经按 100 分点数预算给出，如果再乘以权重，会导致总分异常偏低，使真实样本被普遍打为 `rejected`，无法体现真实批次的质量分层。
2. 训练主版本 CSV 已经需要承载双裁判与仲裁结果，但字段体系需要更明确地解释：哪些字段来自生成阶段、哪些来自事实评估、哪些来自 Phase18 双裁判、哪些来自仲裁与导出路由。
3. `wiki_first_judge_prompts.py` 中历史中文 rubric 文本存在 Windows 控制台写入造成的乱码痕迹，虽然当前 deterministic scorer 不直接依赖这些中文说明，但会影响后续真实 LLM 裁判提示词组装、代码审计与工作汇报。
4. 需要通过真实批次验证：校准后不能出现全部 accepted 或全部 rejected，而应在小批量真实数据中产生符合质量判断的分布。

## 二、本次更新内容

### 1. v2 scorecard 总分校准

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase18_dual_judge_and_arbitrate.py`

核心逻辑：

```python
def weighted_total(dimension_scores, dimension_weights):
    # Scores are stored on the same point budget as their weights, so the
    # weighted total is the sum of earned points across all dimensions.
    total = 0.0
    for key in dimension_weights:
        total += float(dimension_scores.get(key, 0.0) or 0.0)
    return round2(total)
```

校准理由：

- `JUDGE_A_DIMENSIONS`、`JUDGE_B_DIMENSIONS`、`ARBITER_DIMENSIONS` 每组权重合计均为 100。
- 当前每个维度的实际得分已经是该维度点数预算下的 earned points，例如 `evidence_fidelity` 最高 28 分。
- 因此最终 `weighted_total_score` 应为各维度 earned points 的求和，而不是再乘一次权重。
- 该修复可以避免“高质量样本因重复加权被系统性压低分数”的问题。

### 2. v2 双裁判与仲裁维度固定为 100 分制

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\wiki_first_judge_prompts.py`

当前评分卡版本：

- `SCORECARD_VERSION = "wiki_first_g_eval_v2"`

Judge A：偏证据一致性与临床推理，总分 100。

| 字段 | 权重 | 含义 |
|---|---:|---|
| `evidence_fidelity` | 28 | 是否严格基于 wiki 证据、source、rule、page anchor，不虚构、不越界。 |
| `clinical_reasoning` | 22 | 是否在证据边界内给出合理诊断支持、鉴别或控制逻辑。 |
| `safety_boundary` | 20 | 是否对高风险、监管、药物等边界场景保持安全约束。 |
| `question_resolution` | 15 | 是否真正回应用户问诊问题，而不是只堆叠资料。 |
| `training_utility` | 15 | 是否清晰、自然、具备微调训练价值。 |

Judge B：偏风险控制与训练可用性，总分 100。

| 字段 | 权重 | 含义 |
|---|---:|---|
| `risk_control` | 30 | 是否降低错误执行、违规用药、错误监管建议等风险。 |
| `unsupported_expansion_control` | 20 | 是否避免补充证据不支持的事实、处置、剂量、监管动作。 |
| `answer_completeness` | 20 | 在允许边界内是否完整、不空泛。 |
| `citation_integrity` | 15 | 关键结论是否有 citation 和 evidence anchor 支撑。 |
| `language_naturalness` | 15 | 语言是否自然、专业，避免对象串/模板感。 |

Arbiter：偏最终路由与冲突裁决，总分 100。

| 字段 | 权重 | 含义 |
|---|---:|---|
| `consensus_reliability` | 25 | 两位裁判共识是否稳定，是否有明显分歧。 |
| `safety_override` | 30 | 安全风险与训练价值冲突时是否优先安全。 |
| `evidence_sufficiency` | 20 | 最终结论是否匹配当前证据充分性。 |
| `training_value` | 15 | 是否适合训练，或应进入 review / reject / repair 队列。 |
| `calibration_consistency` | 10 | 是否与 hard gate、Phase15、Phase18 信号一致。 |

### 3. 修复评分提示词 rubric 中文可读性

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\wiki_first_judge_prompts.py`

处理方式：

- 在原有历史 rubric 定义后增加一组干净 UTF-8 中文常量重声明。
- 不直接大范围删除历史乱码块，避免不可见字符导致误删或扩大改动面。
- 运行时后定义的 `JUDGE_A_RUBRIC`、`JUDGE_B_RUBRIC`、`ARBITER_RUBRIC` 会覆盖前面的历史定义，后续 LLM judge prompt assembly 将使用干净中文说明。

预期效果：

- 提升后续接入真实 LLM 裁判时的提示词质量。
- 降低工作汇报、代码审查时因乱码造成的误解。
- 保持当前 deterministic scoring 逻辑兼容。

## 三、训练主版本 CSV 完整字段结构

训练主版本文件：

- 全量主版本：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\training_sets\swine_wiki_training_main_20260514_realflow_audit10_v2score_calibrated.csv`
- 可训练主版本：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\training_sets\swine_wiki_training_main_train_ready_20260514_realflow_audit10_v2score_calibrated.csv`

字段结构如下。

### 1. 样本基础信息

| 字段 | 含义 |
|---|---|
| `sample_id` | 样本唯一编号。 |
| `plan_id` | 上游生成计划编号。 |
| `ability_layer` | 能力层级，例如检索型、诊断支持、鉴别支持、监管边界等。 |
| `entity_id` | wiki 实体编号。 |
| `entity_type` | 实体类型，例如 disease、pathogen、control 等。 |
| `risk_class` | 风险类别，用于安全边界和 hard gate 判断。 |
| `expected_output_type` | 期望回答类型。 |
| `user_query` | 训练样本中的用户问题。 |
| `assistant_answer` | 训练样本中的助手回答。 |

### 2. wiki 证据与知识库锚定信息

| 字段 | 含义 |
|---|---|
| `source_trust` | 来源可信度等级或来源质量信号。 |
| `evidence_coverage` | 证据覆盖度。 |
| `evidence_anchor_count` | 证据锚点数量。 |
| `training_intent` | 样本训练意图，例如问诊、诊断支持、边界拒答等。 |
| `evidence_depth_class` | 证据深度分类。 |
| `page_gold_ready` | wiki 页面是否达到 gold-ready 状态。 |
| `evidence_units` | 证据单元的结构化摘要，保留可追溯依据。 |

### 3. Phase15 / Phase18 / 导出路由字段

| 字段 | 含义 |
|---|---|
| `phase15_final_decision` | 事实一致性、格式、硬约束等前置评估后的最终决策。 |
| `phase18_semantic_decision` | 语义双裁判与仲裁后的最终语义决策。 |
| `phase18_judge_status` | Phase18 汇总状态。 |
| `phase18_judge_a_status` | Judge A 状态。 |
| `phase18_judge_b_status` | Judge B 状态。 |
| `phase18_arbiter_status` | Arbiter 状态，未触发仲裁时可为空。 |
| `export_bucket` | 样本导出层级或队列，例如 `L1_L4_borderline`、`rejected_queue`。 |
| `export_decision` | 最终导出决策：`accepted`、`review`、`rejected`。 |

### 4. 最终分数与总标签

| 字段 | 含义 |
|---|---|
| `final_label` | 最终标签，例如 pass / review / reject。 |
| `final_total_score` | 最终总分。无仲裁时通常来自双裁判汇总，有仲裁时来自仲裁。 |
| `final_weighted_total_score` | 最终加权总分，当前为各维度 earned points 求和。 |
| `final_fatal_risk` | 是否存在致命风险。 |
| `final_structured_pass` | 结构化检查是否通过。 |

### 5. Judge A 明细字段

| 字段 | 含义 |
|---|---|
| `judge_a_total_score` | Judge A 总分。 |
| `judge_a_weighted_total_score` | Judge A 加权总分。 |
| `judge_a_final_label` | Judge A 标签。 |
| `judge_a_fatal_risk` | Judge A 是否识别致命风险。 |
| `judge_a_structured_pass` | Judge A 结构化检查是否通过。 |
| `judge_a_evidence_fidelity` | 证据忠实度得分。 |
| `judge_a_clinical_reasoning` | 临床推理得分。 |
| `judge_a_safety_boundary` | 安全边界得分。 |
| `judge_a_question_resolution` | 问题回应得分。 |
| `judge_a_training_utility` | 训练价值得分。 |

### 6. Judge B 明细字段

| 字段 | 含义 |
|---|---|
| `judge_b_total_score` | Judge B 总分。 |
| `judge_b_weighted_total_score` | Judge B 加权总分。 |
| `judge_b_final_label` | Judge B 标签。 |
| `judge_b_fatal_risk` | Judge B 是否识别致命风险。 |
| `judge_b_structured_pass` | Judge B 结构化检查是否通过。 |
| `judge_b_risk_control` | 风险控制得分。 |
| `judge_b_unsupported_expansion_control` | 未支持扩展控制得分。 |
| `judge_b_answer_completeness` | 回答完整性得分。 |
| `judge_b_citation_integrity` | 引用完整性得分。 |
| `judge_b_language_naturalness` | 语言自然度得分。 |

### 7. 仲裁字段

| 字段 | 含义 |
|---|---|
| `needed_arbitration` | 是否触发仲裁。 |
| `arbiter_final_total_score` | 仲裁最终总分。未触发仲裁时为空。 |
| `arbiter_weighted_total_score` | 仲裁加权总分。未触发仲裁时为空。 |
| `arbiter_final_label` | 仲裁标签。 |
| `arbiter_fatal_risk` | 仲裁是否识别致命风险。 |
| `arbiter_structured_pass` | 仲裁结构化检查是否通过。 |
| `arbiter_consensus_reliability` | 共识可靠性得分。 |
| `arbiter_safety_override` | 安全优先裁决得分。 |
| `arbiter_evidence_sufficiency` | 证据充分性得分。 |
| `arbiter_training_value` | 训练价值得分。 |
| `arbiter_calibration_consistency` | 校准一致性得分。 |

### 8. 语言自然度与元数据字段

| 字段 | 含义 |
|---|---|
| `style_clinical_conversation_score` | 临床问诊自然度评分。 |
| `style_dict_like_detected` | 是否检测到对象串/字典串痕迹。 |
| `style_english_template_label_detected` | 是否检测到英文模板标签。 |
| `style_naturalized` | 是否完成自然化处理。 |
| `metadata` | 汇总元数据，包含阶段来源、hash、风险、证据等审计信息。 |

## 四、真实批次校准验证结果

验证批次：

- `20260514_realflow_audit10_v2score_calibrated`

输入文件：

- `exports/generated_samples/naturalized_samples_20260514_realflow_audit10.jsonl`
- `exports/evaluated_samples/fact_evaluated_samples_20260514_realflow_audit10.jsonl`
- `exports/semantic_evaluated_samples/semantic_evaluated_samples_20260514_realflow_audit10_v2score_calibrated.jsonl`

Phase16 manifest 结果：

| 指标 | 数值 |
|---|---:|
| input_samples | 10 |
| accepted | 8 |
| review | 0 |
| rejected | 2 |
| Phase18 semantic accepted | 8 |
| Phase18 semantic rejected | 2 |
| Judge A passed | 8 |
| Judge B passed | 8 |
| Arbiter passed | 3 |

验证结论：

- 小批量真实数据没有出现“全部 rejected”的异常，说明重复加权导致的系统性压分问题已被校准。
- 当前 10 条真实批次的分布为 `accepted=8 / review=0 / rejected=2`，对小样本烟测是合理的：可训练样本进入 train-ready，低质量或风险样本进入 rejected queue。
- 本批次未出现 review，不代表 review 机制无效，只代表这 10 条样本没有落入当前阈值和分歧条件下的中间区间。后续 30/100 条批次可继续观察 review 占比。

## 五、验证命令与结果

为防止乱码，本次检查均使用 UTF-8 终端与 Python IO 设置：

```powershell
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'
```

编译验证：

```powershell
py -3 -m py_compile `
  D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\wiki_first_judge_prompts.py `
  D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase18_dual_judge_and_arbitrate.py `
  D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py
```

结果：

- 编译通过。

scorecard 导入验证：

```powershell
$env:PYTHONPATH='D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline'
py -3 -c "import wiki_first_judge_prompts as p; print(p.SCORECARD_VERSION); print(p.JUDGE_A_RUBRIC['evidence_fidelity']); print(sum(p.JUDGE_A_DIMENSIONS.values()), sum(p.JUDGE_B_DIMENSIONS.values()), sum(p.ARBITER_DIMENSIONS.values()))"
```

结果：

```text
wiki_first_g_eval_v2
是否严格基于已给出的 fact/source/rule/page 锚点回答，不虚构、不越界。
100 100 100
```

训练主版本 CSV 抽检：

- `swine_wiki_training_main_20260514_realflow_audit10_v2score_calibrated.csv`：10 行。
- `swine_wiki_training_main_train_ready_20260514_realflow_audit10_v2score_calibrated.csv`：8 行。
- 分布：`accepted=8`、`rejected=2`、`review=0`。

## 六、当前边界与后续建议

1. 当前 Phase18 的双裁判与仲裁实现仍是 deterministic rubric scorer，并非已经调用外部 LLM judge。它的字段结构、prompt contract 和 scorecard 设计已经为后续真实 LLM judge 接入预留。
2. 建议下一步用 30 条或 100 条真实批次继续观察分布，目标不是固定比例，而是避免长期出现全 accept、全 reject 或 review 永远不可达。
3. 如果后续接入真实 LLM judge，应保留当前字段结构不变，仅替换 Judge A / Judge B / Arbiter 的评分来源，这样训练主 CSV、manifest、审计链路可以保持兼容。
4. 若希望 review 更常出现，可在更大样本验证后再微调 `PASS_THRESHOLD`、`REVIEW_THRESHOLD`、`ARBITRATION_SCORE_GAP`，不建议只基于 10 条样本立即强行制造 review 比例。
