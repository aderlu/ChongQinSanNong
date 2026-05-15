# 2026-05-14 猪病真实问诊数据裁判与仲裁体系重构方案

## 一、目标

当前猪病 Wiki-First 数据生成系统已经具备 Phase15 事实门控、Phase18 双裁判与仲裁、Phase16 分层导出能力。但现有裁判体系仍偏向“证据审计”和“安全拒答”，不足以稳定判断一条样本是否适合进入真实兽医问诊 SFT。

本方案目标是将裁判与仲裁体系改造为：

```text
双裁判独立评分
→ 规则触发仲裁
→ 仲裁模型给出最终有效性结论
→ Phase16 按最终结论导出 main_sft / repair_queue / reject_queue
```

核心原则：

- 双裁判负责广覆盖评分。
- 仲裁负责处理分歧、硬伤和边界样本。
- 仲裁不能只是平均分修正器。
- 医学正确性、安全边界和监管/处方风险必须有一票否决机制。
- 最终判断服务训练数据准入，而不是只服务模型回答好看。

## 二、为什么必须重构

### 2.1 当前裁判流程的主要问题

现有 Phase18 已经具备双裁判和仲裁能力，但它仍存在几个结构性问题：

1. 评价目标偏审计，不完全等同于问诊数据有效性  
   当前评分较重视 evidence fidelity、citation integrity、structured pass 等指标。这些指标对防幻觉有价值，但不能充分判断一条样本是否像真实猪场问诊、是否能训练出可用的问诊 agent。

2. 自然问诊回答容易被误判为证据不足  
   真实问诊回答通常不会在主回答里展示 `source=`、`fact=`、`page=`。如果裁判把主回答 citation 完整性看得过重，就会倾向奖励审计化回答，惩罚自然回答。

3. 有实用性但存在医学硬伤的样本可能拿到中高分  
   一条回答如果语言自然、有现场建议，但存在无证据剂量、错误确诊、监管越界，这类问题不能靠总分抵消。当前如果只看加权分，存在高分带硬伤的准入风险。

4. 低分样本不一定应该丢弃  
   有些样本低分只是因为表达机械、追问不足或场景不自然，并非医学错误。这类样本应进入 repair queue，而不是直接 rejected。

5. 仲裁容易退化为平均分修正  
   如果仲裁只看两个裁判总分差异，再给一个折中分数，它无法回答真正重要的问题：谁判断更可信、是否有一票否决、样本应修复还是丢弃。

6. 高风险样本需要更保守的复核机制  
   L5 药物边界、L6 监管边界、重大疫病场景，即使两个裁判都打高分，也可能隐藏处方或监管越界风险。这类样本应默认进入仲裁。

### 2.2 本方案要解决的问题

本方案通过重构裁判与仲裁流程，解决以下问题：

| 当前问题 | 本方案对应措施 | 预期效果 |
|---|---|---|
| 裁判偏审计，不能判断真实问诊价值 | 增加真实性/场景感、问诊完整性、追问逻辑、可执行性维度 | 更准确识别可训练问诊样本 |
| 自然回答被 citation 维度误伤 | 明确主回答不要求显示 citation，审计字段负责追溯 | 避免奖励审计腔回答 |
| 高分样本可能有医学硬伤 | 设置一票否决项和 hard_fail_flags | 防止危险样本进入主训练集 |
| 低分样本可能可修复 | 输出 `repairable` 和 `repair_suggestion` | 区分修复队列和拒绝队列 |
| 仲裁只做平均分 | 仲裁模型专门处理分歧、硬伤、边界样本 | 提升最终有效性结论可信度 |
| L5/L6 高风险样本漏判 | L5/L6 和高风险 risk_class 默认仲裁 | 降低处方/监管越界风险 |
| Phase16 不知道如何导出 | 新增 `sft_admission` | 直接映射 main_sft / repair_queue / reject_queue |

### 2.3 为什么采用双裁判加仲裁

单一裁判容易形成稳定偏见：

- 偏安全的裁判可能把有用问诊样本打低。
- 偏自然度的裁判可能放过医学边界问题。
- 偏证据的裁判可能奖励审计文本。

双裁判可以让两个视角互相制衡：

- Judge A 重点看医学正确性、安全边界、上下文一致性。
- Judge B 重点看真实场景、问诊完整性、追问逻辑、可执行性。

仲裁只在必要时介入，处理两个裁判无法直接合并的问题。这样既能减少 API 成本，也能避免对所有样本重复深度评审。

### 2.4 为什么仲裁不能只是平均分

兽医问诊数据中，分数平均并不可靠：

- A 给 90、B 给 55，可能是 B 发现了医学硬伤，也可能只是 B 对表达不满意。
- A 给 75、B 给 76，仍可能共同漏掉无证据剂量。
- 两个裁判都给低分，但一个认为医学错误，一个认为语言不自然，处理方式完全不同。

因此仲裁必须输出：

- 分歧原因。
- 是否存在一票否决。
- 更可信的裁判或独立判断。
- 最终有效性标签。
- 修复建议或拒绝原因。

这比平均分更适合训练数据治理。

## 三、适用范围

落地文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/wiki_first_judge_prompts.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase16_export_layered_training_sets.py`

输入样本字段至少应包含：

- `case_user_query`
- `assistant_answer`
- `grounded_audit_answer`
- `evidence_anchors`
- `ability_layer`
- `risk_class`
- `source_trust`
- `evidence_coverage`
- `phase15_final_decision`
- `phase15_reject_reasons`

## 四、双裁判评分维度

Judge A 和 Judge B 使用同一套维度，便于校准和比较；但提示词中赋予不同审查重点。

### 4.1 评分维度和权重

满分 100。

| 维度 | 权重 | 评分重点 |
|---|---:|---|
| 真实性/场景感 | 15 | 用户问题是否像养殖户、饲养员、场长或猪场技术员真实咨询，而不是知识库检索题 |
| 问诊完整性 | 15 | 是否回应主诉、症状、时间线、群体情况、缺失信息和用户诉求 |
| 医学正确性 | 25 | 疾病方向、鉴别、检测、处置建议是否符合猪病知识和证据边界 |
| 追问逻辑 | 10 | 追问是否有优先级，是否围绕日龄、发病率、死亡率、免疫、用药、剖检、检测展开 |
| 边界与分诊 | 10 | 是否区分轻重急缓，避免线上确诊、危险用药和监管越界 |
| 上下文一致性 | 10 | 是否紧扣用户给出的猪只阶段、症状、场景，不编造病历、检测、剖检或免疫结果 |
| 可执行性 | 10 | 是否给出安全、低风险、现场可做的下一步 |
| 结构化与可标注性 | 5 | 是否清晰、可拆分、可标注，适合训练和复核 |

### 4.2 为什么这样设置权重

权重设计的理由如下：

- 医学正确性占 25%，因为这是猪病问诊数据能否使用的核心。如果医学方向错误，真实感和语言自然度再高也不能进入主训练集。
- 真实性/场景感占 15%，因为当前数据的主要缺陷之一是用户问题像知识库任务，不像猪场咨询。
- 问诊完整性占 15%，因为模型必须学会围绕主诉、病程、群体信息和缺失信息完成问诊，而不是只给结论。
- 追问逻辑占 10%，用于区分“机械罗列问题”和“按临床优先级追问”。
- 边界与分诊占 10%，用于约束线上问诊不能确诊、不能乱开药、不能下监管结论。
- 上下文一致性占 10%，用于防止模型编造检测结果、剖检结果、免疫史或把猪只阶段搞错。
- 可执行性占 10%，用于避免回答只有“补充信息/送检”，没有任何低风险现场动作。
- 结构化与可标注性占 5%，用于训练数据工程，不让格式凌驾于医学和问诊质量之上。

这套权重把医学安全放在第一位，同时补足当前系统对真实问诊体验和训练价值评估不足的问题。

### 4.3 Judge A 侧重点

Judge A 偏医学和安全：

- 医学正确性。
- 边界与分诊。
- 上下文一致性。
- 证据是否足以支撑回答。
- 是否存在一票否决问题。

这样设计 Judge A，是为了防止自然流畅但医学错误的回答被误收。

### 4.4 Judge B 侧重点

Judge B 偏问诊数据质量：

- 真实性/场景感。
- 问诊完整性。
- 追问逻辑。
- 可执行性。
- 语言自然度和训练可用性。

这样设计 Judge B，是为了防止系统继续偏向审计文本，而忽略真实用户体验和 SFT 可用性。

### 4.5 双裁判输出结构

每个裁判必须输出结构化结果：

```json
{
  "judge_id": "judge_a",
  "score": 82,
  "validity_label": "valid",
  "confidence": 0.82,
  "dimension_scores": {
    "scenario_realism": 4,
    "consultation_completeness": 4,
    "medical_correctness": 4,
    "followup_logic": 3,
    "triage_boundary": 4,
    "context_consistency": 5,
    "actionability": 4,
    "structure_labelability": 4
  },
  "hard_fail_flags": [],
  "main_issues": [
    "追问免疫记录和死亡变化仍可更具体"
  ],
  "summary": "样本整体可用，医学边界清楚，问诊自然度较好。"
}
```

`validity_label` 只允许：

- `high_quality_valid`
- `valid`
- `repairable`
- `invalid`

## 五、一票否决项

以下问题不能被总分抵消。命中后应进入仲裁，且严重问题最终只能判为 `invalid`。

| 一票否决项 | 默认处理 |
|---|---|
| 无证据给具体药名 + 剂量/疗程/休药期 | invalid |
| 缺少体重、日龄、药品规格、标签依据仍给精确剂量 | invalid |
| 对疑似重大疫病给出扑杀、封锁、调运、上报等监管执行结论 | invalid |
| 对线上问诊直接确诊某病，且可能延误处置 | invalid 或 repairable |
| 把合成病例症状写成疾病典型事实 | invalid 或 repairable |
| 高死亡、急性传播、疑似重大疫病样本没有任何分诊升级或送检建议 | repairable 或 invalid |
| 猪只阶段混乱，如把哺乳仔猪按妊娠母猪处理 | invalid |
| 明显编造检测结果、剖检结果、免疫史、药敏结果 | invalid |
| 主回答泄漏 `source=`、`fact=`、`page=`、`rule=`、`DIS-` 等审计痕迹 | repairable，严重时 invalid |
| 回答根本不是问诊，如只输出分类字段残片 | invalid |

一票否决项应在 Phase18 中形成 `hard_fail_flags`，同时传入仲裁模型。

### 5.1 为什么需要一票否决

一票否决用于解决“总分掩盖硬伤”的问题。

例如：

- 回答很自然，也给了现场建议，但无证据给出剂量和休药期。
- 回答结构完整，但对疑似重大疫病给出扑杀或调运结论。
- 回答语气专业，但编造了检测结果。

这些样本不能因为真实性、完整性或可执行性得分较高而进入训练集。一票否决把医学安全和监管边界放在加权分之上，避免模型学到危险行为。

## 六、仲裁触发规则

仲裁分为强制仲裁和条件仲裁。

### 6.1 强制仲裁

命中任一条即进入仲裁：

| 触发条件 | 阈值 |
|---|---:|
| 两个裁判总分差异过大 | `abs(score_A - score_B) >= 15` |
| 一个判有效、一个判无效 | 例如 `A >= 75` 且 `B < 60` |
| 任一裁判标记严重医学错误 | 直接仲裁 |
| 任一裁判标记严重安全风险 | 直接仲裁 |
| 任一裁判标记非真实问诊场景 | 直接仲裁 |
| 任一裁判标记关键字段缺失 | 直接仲裁 |
| 任一裁判置信度低 | `confidence < 0.6` |
| 任一关键维度分歧过大 | 单项 5 分制下差异 `>= 2` |
| 样本属于 L5 药物边界或 L6 监管边界 | 默认仲裁 |
| 疑似非洲猪瘟、口蹄疫等重大疫病边界样本 | 默认仲裁 |

关键维度包括：

- `medical_correctness`
- `consultation_completeness`
- `scenario_realism`
- `triage_boundary`
- `context_consistency`

### 6.2 条件仲裁

总分差不大，但存在结构性风险时进入仲裁：

| 条件 | 说明 |
|---|---|
| 均分处于灰区 | `avg_score >= 60 and avg_score <= 75` |
| 高分但存在硬伤标签 | 例如总分 82，但缺少体重仍给剂量 |
| 低分但分歧集中在表达质量 | 可能只是语言自然度差，可修复 |
| 双方都有效但关键项低 | 例如总分 > 75，但医学正确性 < 3/5 |
| 双方都无效但原因不同 | 需要确认丢弃还是修复 |

### 6.3 为什么要区分强制仲裁和条件仲裁

强制仲裁解决高风险和明显分歧问题；条件仲裁解决灰区样本治理问题。

如果只看总分差，会漏掉这些情况：

- 两个裁判总分接近，但都忽略了高风险药物边界。
- 两个裁判都给低分，但样本只是表达差，可以修复。
- 一个裁判因为自然度打高分，另一个因为医学边界打低分。

区分强制与条件仲裁，可以让仲裁资源集中在最需要复核的样本上，同时减少无意义的全量仲裁。

### 6.4 决策逻辑

```python
def need_arbitration(judge_a, judge_b, sample):
    if sample.hard_fail_flags:
        return True
    if abs(judge_a.score - judge_b.score) >= 15:
        return True
    if judge_a.validity_label != judge_b.validity_label:
        return True
    if critical_dimension_gap(judge_a, judge_b) >= 2:
        return True
    avg_score = (judge_a.score + judge_b.score) / 2
    if 60 <= avg_score <= 75:
        return True
    if min(judge_a.confidence, judge_b.confidence) < 0.6:
        return True
    if sample.ability_layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}:
        return True
    if sample.risk_class in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"}:
        return True
    return False
```

## 七、仲裁模型职责

仲裁模型不应重复普通裁判完整打分。它需要重点回答：

1. 两个裁判谁的判断更可靠。
2. 样本是否存在一票否决问题。
3. 分歧来自医学事实、问诊流程、场景真实性、安全边界，还是主观表达偏好。
4. 样本最终应进入主训练集、低权重训练集、修复队列，还是拒绝队列。

仲裁模型输入必须包括：

- 原始 `case_user_query`
- 原始 `assistant_answer`
- `grounded_audit_answer`
- `evidence_anchors`
- `ability_layer`
- `risk_class`
- Phase15 结论和 reject reasons
- Judge A 维度分、总分、理由
- Judge B 维度分、总分、理由
- 仲裁触发原因

### 7.1 仲裁解决什么问题

仲裁需要解决的是训练数据准入问题，而不是再做一次普通评分。

它应明确回答：

- 这条样本能不能进入主 SFT。
- 如果不能，是可修复还是必须丢弃。
- 两个裁判的分歧是否来自医学事实、安全边界、场景真实性，还是表达偏好。
- 是否存在任何不能被加权分抵消的风险。

因此，仲裁输出必须包含 `sft_admission`，直接服务 Phase16 导出。

## 八、仲裁评分维度

仲裁满分 100。

| 仲裁维度 | 权重 | 说明 |
|---|---:|---|
| 医学正确性 | 25 | 疾病判断、检查建议、处置建议是否符合猪病临床常识和证据 |
| 安全边界与分诊 | 20 | 是否识别高风险场景，避免线上确诊、危险用药、监管越界 |
| 问诊流程完整性 | 15 | 是否覆盖主诉、病史、基础信息、关键追问和下一步 |
| 真实猪场问诊场景符合度 | 15 | 是否像真实养殖户/饲养员/场长/技术员咨询 |
| 上下文一致性 | 10 | 猪只阶段、症状、病程、建议前后是否一致 |
| 信息充分性 | 5 | 是否有足够信息支撑建议，是否明确缺失信息 |
| 可执行性 | 5 | 建议是否安全、具体、现场可做 |
| 语言与沟通自然度 | 5 | 专业但可理解，符合兽医问诊口吻 |

### 8.1 为什么仲裁权重不同于双裁判

仲裁不是普通裁判的重复，因此权重更强调：

- 医学正确性。
- 安全边界与分诊。
- 真实猪场问诊价值。
- 上下文一致性。

可执行性和语言自然度在仲裁中权重较低，是因为它们不能覆盖医学硬伤。一个样本可以因为表达不够自然进入修复队列，但不能因为表达自然而绕过处方或监管风险。

## 九、仲裁输出结构

仲裁模型必须输出 JSON：

```json
{
  "need_arbitration_reason": [
    "judge_score_gap",
    "critical_dimension_disagreement"
  ],
  "final_score": 78,
  "final_label": "valid",
  "hard_fail": false,
  "hard_fail_codes": [],
  "risk_level": "none",
  "preferred_judge": "judge_A",
  "preferred_judge_reason": "Judge A correctly identified missing vaccination history as a moderate issue, while Judge B over-penalized it as invalid.",
  "dimension_scores": {
    "medical_correctness": 4,
    "safety_boundary": 4,
    "consultation_completeness": 3,
    "scenario_realism": 4,
    "context_consistency": 5,
    "information_sufficiency": 3,
    "actionability": 4,
    "communication_naturalness": 4
  },
  "main_issues": [
    "缺少体重信息，但未给精确剂量，因此不构成严重风险",
    "追问免疫和死亡变化不足"
  ],
  "repair_suggestion": "补充免疫史、发病比例、死亡变化和是否做过剖检的追问。",
  "sft_admission": "main_sft"
}
```

字段取值约束：

- `final_label`: `high_quality_valid | valid | repairable | invalid`
- `risk_level`: `none | minor | moderate | severe`
- `preferred_judge`: `judge_A | judge_B | blend | independent`
- `sft_admission`: `main_sft | low_weight_sft | repair_queue | reject_queue`

### 9.1 为什么输出 `sft_admission`

仅输出 `final_score` 和 `final_label` 不足以指导训练集导出。

例如：

- `valid` 样本可以进入主训练集。
- `repairable` 样本应进入修复队列。
- `invalid` 样本应进入拒绝队列或负例分析。
- 某些 `valid` 但非高质量样本可进入低权重训练集。

`sft_admission` 直接把裁判结论转换为 Phase16 的导出动作，减少人工解释空间。

## 十、最终有效性判定

### 10.1 无仲裁样本

```python
final_score = weighted_average(score_A, score_B)
final_label = label_by_threshold(final_score)
```

默认阈值：

| 分数 | 标签 | 导出建议 |
|---:|---|---|
| >= 85 | `high_quality_valid` | `main_sft` |
| 75-84 | `valid` | `main_sft` 或 `low_weight_sft` |
| 60-74 | `repairable` | `repair_queue` |
| < 60 | `invalid` | `reject_queue` |

### 10.2 仲裁样本

```python
final_score = arbitration.final_score
final_label = arbitration.final_label
sft_admission = arbitration.sft_admission
```

如果 `hard_fail=true`：

| 风险等级 | 最高标签 |
|---|---|
| severe | `invalid` |
| moderate | `repairable` |
| minor | `valid` |

### 10.3 这套判定解决什么问题

四档标签解决二分类过粗的问题：

- `high_quality_valid`：可作为高质量 SFT 样本。
- `valid`：可用但需抽检或低权重。
- `repairable`：不应丢弃，应进入修复队列。
- `invalid`：存在严重问题，应拒绝。

这能避免把所有非完美样本都丢弃，也能避免把可疑样本混入主训练集。

## 十一、Phase18 落地要求

### 11.1 `wiki_first_judge_prompts.py`

需要修改：

- Judge A system prompt。
- Judge B system prompt。
- Arbiter system prompt。
- Judge A/B output schema。
- Arbiter output schema。

必须明确：

- 主回答不要求显示 citation。
- citation 和 evidence anchors 在审计字段中检查。
- 问诊真实感和可执行性要评分。
- 医学正确性和安全边界仍是硬门禁。

原因：

- 当前 judge prompt 已经有问诊 SFT 倾向，但维度仍不足以表达“真实场景”和“可执行性”。
- 如果不修改 prompt，仅修改后处理逻辑，裁判模型仍会按旧标准输出，无法稳定产生新字段。

### 11.2 `phase18_dual_judge_and_arbitrate.py`

需要修改：

- `normalize_llm_judge_payload()` 支持新字段。
- `normalize_llm_arbiter_payload()` 支持新字段。
- 新增 `need_arbitration()`。
- 新增 `critical_dimension_gap()`。
- 新增 `hard_fail_flags` 汇总。
- `merge_semantic_result()` 改为优先采用仲裁最终结论。
- CSV/JSON 报告输出新增维度分、触发原因、sft_admission。

原因：

- 仲裁触发不能只靠模型主观判断，必须由程序规则稳定执行。
- `hard_fail_flags` 必须在进入仲裁前汇总，避免模型忽略硬伤。
- `merge_semantic_result()` 必须优先采用仲裁结论，否则仲裁仍会退化为附属信息。

## 十二、Phase16 导出要求

`phase16_export_layered_training_sets.py` 必须读取 Phase18 最终字段：

- `final_score`
- `final_label`
- `hard_fail`
- `hard_fail_codes`
- `risk_level`
- `sft_admission`
- `main_issues`
- `repair_suggestion`

导出策略：

| `sft_admission` | 导出位置 |
|---|---|
| `main_sft` | 主 SFT CSV/JSONL |
| `low_weight_sft` | 可选低权重训练集 |
| `repair_queue` | 修复队列 |
| `reject_queue` | 拒绝队列 |

如果 Phase18 没有输出 `sft_admission`，Phase16 必须保守处理为：

- `high_quality_valid` / `valid` → accepted
- `repairable` → review
- `invalid` → rejected

原因：

- 当前导出更关注 accepted/review/rejected，但不足以表达高质量、低权重、可修复、拒绝四类训练用途。
- 如果 Phase16 不读取 `sft_admission`，Phase18 的精细判断不会真正影响训练集。
- 导出层必须成为最终准入执行点。

## 十三、改动理由与问题闭环

本节用于把“要改什么”和“为什么改”绑定起来，避免后续实现只改字段、不改判断逻辑。

| 改动项 | 为什么要这样做 | 解决当前什么问题 | 落地验收点 |
|---|---|---|---|
| 将裁判维度改为真实性/场景感、问诊完整性、医学正确性、追问逻辑、边界与分诊、上下文一致性、可执行性、结构化与可标注性 | 当前样本的目标是训练真实猪病问诊能力，而不是只证明回答引用了知识库证据 | 解决裁判偏 evidence audit、不能识别“像不像真实问诊”的问题 | Judge A/B 输出必须包含 8 个维度分；报告中能看到每个维度的分值和理由 |
| 医学正确性设为最高权重 | 猪病问诊数据一旦医学方向错误，会直接训练出错误处置倾向 | 解决语言自然但医学错误的样本被误收问题 | 医学正确性低于阈值时，即使总分较高也不得进入 `main_sft` |
| 增加真实性/场景感与问诊完整性 | 现有问题中有大量“知识库问答”“标签片段”“模板总结”，不符合养殖户真实咨询 | 解决数据训练后模型只会答百科、不像兽医问诊的问题 | 抽检样本的问题和回答应呈现主诉、场景、病程、猪群信息或合理缺失追问 |
| 增加追问逻辑 | 真实问诊不是罗列所有问题，而是按急重程度和诊断价值追问 | 解决追问机械、无优先级、不能推动诊断流程的问题 | 追问应优先覆盖日龄、发病率、死亡率、病程、免疫、用药、粪便/呼吸/神经症状、剖检/检测等关键线索 |
| 增加边界与分诊 | 线上问诊不能替代现场诊断，重大疫病、急性传播、高死亡场景必须升级处理 | 解决高风险样本没有就医/送检/隔离/上报边界提示的问题 | 高风险样本若无分诊升级，必须进入仲裁，严重时判 `invalid` |
| 明确主回答不要求显示 citation | 真实给养殖户的回答不应暴露 `source=`、`fact=`、`page=` 等审计痕迹 | 解决裁判奖励审计腔、惩罚自然问诊回答的问题 | 主训练视图不得包含审计字段；证据追溯只保留在 audit/debug 字段 |
| 设置一票否决项 | 加权分不能覆盖危险用药、监管越界、编造检测、物种/阶段错误等硬伤 | 解决高分样本带严重医学或安全风险进入训练集的问题 | 命中 hard fail 的样本不得进入 `main_sft`；严重风险最高只能 `invalid` |
| L5/L6 和高风险 risk_class 默认仲裁 | 药物、休药期、残留、监管边界的错误成本高，双裁判都高分也不能默认安全 | 解决处方/监管边界样本漏判问题 | 所有 L5/L6、高监管、高食品安全风险样本必须有仲裁记录 |
| 区分强制仲裁与条件仲裁 | 并非所有样本都需要仲裁，但硬伤、分歧和灰区必须复核 | 解决全量仲裁成本高、只看总分差又漏掉灰区风险的问题 | 报告中必须记录 `need_arbitration_reason`，且触发原因可复现 |
| 仲裁不做平均分修正 | 双裁判分歧可能来自医学事实、安全边界或表达偏好，平均分无法解释准入决策 | 解决仲裁退化为“折中打分”，无法判断谁更可靠的问题 | 仲裁输出必须包含 `preferred_judge`、`preferred_judge_reason`、`main_issues`、`repair_suggestion` |
| 输出四档最终标签 | 二分类有效/无效过粗，不能区分高质量、可用、可修复和必须丢弃 | 解决低分可修复样本被丢弃、高风险可疑样本被混入主集的问题 | `final_label` 只允许 `high_quality_valid/valid/repairable/invalid` |
| 增加 `sft_admission` | 分数和标签不能直接告诉 Phase16 应该导到哪里 | 解决 Phase18 精细判断无法转化为训练集准入动作的问题 | Phase16 必须按 `main_sft/low_weight_sft/repair_queue/reject_queue` 分流 |
| 保留 `main_issues` 和 `repair_suggestion` | 可修复样本如果只有低分，没有可操作原因，无法进入下一轮修复 | 解决 review 队列不可用、人工无法快速定位问题的问题 | `repairable` 样本必须有明确问题和修复建议 |
| 自测样本覆盖典型失败模式 | 没有固定回归样本，后续 prompt 或代码改动会反复引入旧问题 | 解决流程修改不可验证、质量回退难发现的问题 | 自测至少覆盖高质量、证据不足、无证据剂量、重大疫病边界、审计泄漏、分类残片、裁判分歧、L5/L6 |

如果只修改评分权重、不增加 hard fail 和仲裁触发规则，仍会出现“总分好看但医学危险”的样本。

如果只增加仲裁、不修改 Phase16 导出，仲裁结论不会真正影响最终训练集。

如果只修改 Phase16、不修改 Judge/Arbiter schema，导出层拿不到足够字段，只能继续依赖粗粒度 accepted/review/rejected。

因此，本方案必须按“Prompt schema → Phase18 规则执行 → Arbiter 最终结论 → Phase16 分流导出 → 自测验收”整链路实施。

## 十四、验收标准

### 14.1 自测样本

至少构造以下样本：

1. 高质量真实问诊样本，应判 `high_quality_valid`。
2. 自然但证据不足样本，应判 `repairable`。
3. 无证据剂量样本，应判 `invalid`。
4. 疑似重大疫病但无分诊升级样本，应判 `repairable` 或 `invalid`。
5. 审计字段泄漏到主回答，应判 `repairable`。
6. 只输出分类残片，应判 `invalid`。
7. 两裁判分歧大样本，应触发仲裁。
8. L5/L6 样本，应默认触发仲裁。

这些自测样本覆盖当前最常见失败模式：

- 高质量样本被误杀。
- 自然但证据不足样本被误收。
- 无证据剂量样本漏判。
- 高风险边界样本未升级。
- 审计字段泄漏到训练视图。
- 分类残片进入训练集。
- 双裁判分歧没有被处理。

### 14.2 批次验收

10 条校准批次：

- 仲裁触发原因必须可解释。
- 所有 L5/L6 样本进入仲裁。
- 一票否决样本不得进入 `main_sft`。
- `repairable` 样本必须有 `main_issues` 和 `repair_suggestion`。

40 条正式批次：

- `high_quality_valid + valid` 进入主训练视图。
- `repairable` 进入修复队列。
- `invalid` 进入拒绝队列。
- 主训练样本不得包含 `source=`、`fact=`、`page=`、`rule=`、`DIS-`。
- 所有最终结论必须能追溯到 Judge A/B 或 Arbiter 的理由。

## 十五、残余风险

- 裁判模型可能偏好更长回答，需用长度惩罚或结构化评分控制。
- 可执行性加权过高时，可能鼓励模型给出过度处置建议。
- 医学正确性如果只依赖 LLM judge，仍可能漏掉事实错误，因此 Phase15 hard gate 不能弱化。
- L5/L6 默认仲裁会增加 API 成本，但能降低高风险样本漏判。
- `valid` 不等于一定能进入所有训练集；训练集导出仍应按用途区分 main SFT、评估集、修复队列和负例分析。

## 十六、结论

本方案建议采用三层流程：

```text
Judge A/B 独立评分
→ 规则判断是否仲裁
→ Arbiter 输出最终有效性和训练准入
```

核心改动不是调平均分，而是让仲裁专门处理：

- 医学硬伤。
- 安全边界。
- 问诊真实性分歧。
- 高风险 L5/L6 样本。
- 修复与丢弃决策。

该方案能够更准确判断猪病问诊样本是否真实、有效、可训练，并能降低“高分但有医学硬伤”和“低分但只是表达问题”两类错误准入风险。
