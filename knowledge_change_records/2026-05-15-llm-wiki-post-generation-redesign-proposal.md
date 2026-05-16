# 2026-05-15 猪病生成与评估系统 Wiki 后移重构思路文档

## 一、结论先行

当前系统是典型 `wiki-first` 架构：先从 Wiki 页面生成 plan，再生成 answer skeleton，再约束 LLM 生成问题、诊疗回答和处方边界。这种方式事实可控，但已经明显牺牲了真实问诊质量，尤其是：

1. 用户问题容易被知识库结构污染，像“资料缺口清单”而不是养殖户提问。
2. 回答容易变成“不能确诊、建议检测、继续追问”，不像临床兽医直接处置。
3. 处方和治疗建议被前置证据锚点压得过保守，缺少临床式支持治疗和处方化框架。
4. Wiki 约束越强，生成越像审计报告；生成越自然，Phase15/18 又容易因为缺锚点拒绝。

因此建议大改为：

```text
LLM 先生成真实临床问诊样本
-> Wiki 后置检索与证据审计
-> LLM/Wiki 联合修订
-> 双裁判与风险门控
-> 分层导出
```

也就是：**Wiki 不再约束 LLM 如何生成问题、诊疗和处方，而是在生成后承担证据校验、风险识别、修订建议、打标和可追溯增强。**

## 二、为什么要把 Wiki 后移

### 2.1 现有 wiki-first 的优点

当前链路的优点是真实存在的：

- 事实来源清晰。
- 每条样本能挂 `evidence_anchors`。
- Phase15 可以做硬门控。
- Phase18 能参考 fact/hard gate 结果。
- Phase16 可以稳定导出带证据字段的数据。

这适合生成“知识库问答”“事实检索问答”“规则边界问答”。

### 2.2 但它不适合生成真实问诊

猪场问诊数据的核心不是“把 Wiki 内容问出来”，而是模拟：

- 养殖户怎么描述问题。
- 兽医怎么从有限症状给临床判断。
- 兽医怎么直接给现场处置。
- 兽医怎么给处方化治疗框架。
- 兽医怎么控制禁忌、剂量、休药期和重大疫病风险。

这些更接近临床交流，而不是文档检索。

现有 `wiki-first` 把 Wiki 放在生成前，导致模型必须先考虑：

- 哪些 claim 有锚点。
- 哪些 fact 能说。
- 哪些 hard gate 不能碰。
- 哪些 source/rule/page 需要保留。

结果就是：模型的主要注意力从“像兽医回答”转移到“不要违反审计规则”。

### 2.3 最根本的问题

当前系统把两个目标混在了一起：

1. **生成目标**：产出真实、自然、有临床处置价值的问答。
2. **审计目标**：证明回答中的事实、边界和处方建议是否有证据支撑。

wiki-first 的做法是用审计目标支配生成目标。

Wiki 后移的做法是：先让生成目标充分发挥，再用审计目标做后置过滤和修订。

## 三、新架构总览

### 3.1 新主链路

建议新链路命名为：

```text
clinical-first + wiki-audited
```

完整流程：

```text
Phase A: Clinical Case Seed
-> Phase B: LLM Clinical QA Generation
-> Phase C: Claim & Risk Extraction
-> Phase D: Wiki Retrieval
-> Phase E: Evidence Alignment
-> Phase F: Wiki-Audited Revision
-> Phase G: Dual Judge + Arbiter
-> Phase H: Export & Dataset Stratification
```

### 3.2 旧链路到新链路映射

| 旧阶段 | 旧职责 | 新定位 |
|---|---|---|
| Phase12 plan from Wiki | 从 Wiki 页面决定生成任务 | 降级为 coverage/index 参考，不再作为生成主入口 |
| Phase13 skeleton | 把 claims/anchors 固化成生成骨架 | 后移为 evidence audit schema，不再约束初稿生成 |
| Phase14 generation | 在 anchors 约束下生成回答 | 改为 clinical-first 自由生成 |
| Phase14b naturalization | 清理审计腔 | 大幅弱化，生成阶段本身就应自然 |
| Phase15 fact gate | 检查 anchors 和硬门控 | 保留，但改为生成后事实审计 |
| Phase18 dual judge | 语义评估与仲裁 | 保留，并拆分临床质量与证据质量 |
| Phase16 export | 导出训练集 | 保留，但增加证据状态、修订状态、处方风险等级 |

## 四、新系统中 Wiki 的具体作用

Wiki 后移不等于不用 Wiki。相反，Wiki 的角色更清晰、更有价值。

### 4.1 Wiki 不再做什么

Wiki 不再负责：

- 生成用户问题。
- 预先规定回答必须包含哪些 claim。
- 强行把回答限制在少量锚点句子里。
- 在生成前决定 LLM 能不能说某个临床处置。
- 让用户问题和回答暴露知识库结构。

### 4.2 Wiki 继续做什么

Wiki 后置负责：

1. **疾病/药物/规则检索**
   - 根据生成问答中的实体、症状、药物、风险词检索相关 Wiki 页面。

2. **事实 claim 对齐**
   - 抽取回答中的医学事实、诊断判断、防控建议、处方建议。
   - 判断每个 claim 是否被 Wiki 支撑、部分支撑、冲突或无证据。

3. **风险边界审计**
   - 检查是否出现：
     - 线上确诊。
     - 明确剂量但无标签证据。
     - 休药期/MRL 无依据。
     - 调运、上报、扑杀、封锁等监管越界。
     - 禁药或不适用于猪的药物。

4. **处方安全审计**
   - 对回答中的用药内容做分层：
     - 支持治疗：通常可保留。
     - 药物类别：可保留但需标边界。
     - 具体药名：需要标签/适应症证据。
     - 精确剂量、疗程、休药期：必须有高可信来源，否则降级或拒绝。

5. **修订建议生成**
   - 对无证据或冲突内容，给出可执行修订：
     - 删除。
     - 降级为“可能方向”。
     - 改为“需现场兽医确认”。
     - 补充禁忌或安全边界。

6. **证据包生成**
   - 不把 evidence 写进主回答，但在后台生成：
     - `evidence_anchors`
     - `supporting_claim_ids`
     - `conflicting_claim_ids`
     - `unsupported_claims`
     - `risk_gate_codes`

7. **训练分层**
   - Wiki 不再决定初稿怎么写，但决定样本进入：
     - main_sft
     - low_weight_sft
     - repair_queue
     - reject_queue
     - eval_only

## 五、推荐新阶段设计

### Phase A: Clinical Case Seed

目标：生成真实猪场病例种子，不依赖 Wiki claim。

输入来源：

- 疾病列表或主题列表。
- 猪群阶段。
- 场景变量。
- 症状组合。
- 时间线。
- 场规模。
- 用户角色。
- 紧急程度。
- 处方支持等级。

注意：疾病名可以来自 Wiki 或疾病目录，但这里只作为“主题标签”，不是事实约束。

输出示例：

```json
{
  "case_seed_id": "CASE-000001",
  "target_topic": "疑似非洲猪瘟方向",
  "pig_stage": "育肥猪",
  "farm_scale": "中小场",
  "timeline": "这两天",
  "observed_signals": ["发热", "吃料下降", "皮肤发红", "死亡增加"],
  "consultation_intent": "ask_what_to_do",
  "prescription_expectation": "needs_practical_plan",
  "risk_profile": "high_consequence_disease_possible"
}
```

### Phase B: LLM Clinical QA Generation

目标：让 LLM 先生成高质量真实问答。

输入：

- case_seed
- 生成风格约束
- 通用安全底线
- 处方化回答模板

不输入：

- Wiki facts
- evidence anchors
- fact_id
- source_id
- page_relpath

回答要求：

- 用户问题必须像养殖户真实提问。
- 助手回答必须直接回应“现在怎么办”。
- 必须给：
  - 临床方向。
  - 严重程度。
  - 鉴别方向。
  - 现场处置。
  - 支持治疗。
  - 处方化治疗框架。
  - 禁忌和升级条件。
- 追问最多 0-2 个，只能放在末尾。

输出：

```json
{
  "sample_id": "CLIN-000001",
  "case_seed_id": "CASE-000001",
  "user_query": "...",
  "assistant_answer_draft": "...",
  "generation_source": "clinical_first_llm",
  "wiki_used_in_generation": false
}
```

### Phase C: Claim & Risk Extraction

目标：把回答拆成可审计 claim。

抽取对象：

- 疾病判断 claim。
- 症状-疾病关联 claim。
- 鉴别诊断 claim。
- 现场处置 claim。
- 用药/处方 claim。
- 监管/上报/调运 claim。
- 检测/剖检 claim。

输出示例：

```json
{
  "claims": [
    {
      "claim_id": "C001",
      "claim_text": "发热、采食下降和死亡增加需要警惕非洲猪瘟",
      "claim_type": "diagnostic_risk",
      "risk_level": "high"
    },
    {
      "claim_id": "C002",
      "claim_text": "腹泻脱水明显时可先使用口服补液盐或电解质水",
      "claim_type": "supportive_care",
      "risk_level": "low"
    }
  ]
}
```

### Phase D: Wiki Retrieval

目标：根据 claim 去 Wiki 找证据。

检索粒度：

- 疾病页面。
- 药物页面。
- rule card。
- source fact 表。
- gold readiness index。
- drug label/withdrawal evidence。

检索策略：

1. 用 disease/topic/entity 做粗召回。
2. 用症状、药物、处方词做二次召回。
3. 对高风险 claim 扩展检索 rule cards。
4. 对药物 claim 必须检索 drug/label/source。

输出：

```json
{
  "retrieved_evidence": [
    {
      "claim_id": "C001",
      "entity_id": "DIS-002",
      "page_relpath": "wiki/diseases/...",
      "fact_id": "FACT-...",
      "source_trust": "A1",
      "match_score": 0.82
    }
  ]
}
```

### Phase E: Evidence Alignment

目标：判断 claim 和 Wiki 证据关系。

每个 claim 给一个状态：

- `supported`
- `partially_supported`
- `unsupported`
- `contradicted`
- `not_in_wiki_but_low_risk_common_practice`
- `requires_label_or_local_vet`
- `regulatory_boundary_required`

特别规则：

- 支持治疗可以允许 `not_in_wiki_but_low_risk_common_practice`。
- 药物类别可以允许 `requires_label_or_local_vet`。
- 精确剂量/疗程/休药期必须 `supported`，否则不能进 main_sft。
- 重大疫病确诊和监管动作必须严格证据或拒绝。

输出：

```json
{
  "claim_audit": [
    {
      "claim_id": "C001",
      "support_status": "supported",
      "evidence_anchor_count": 2
    },
    {
      "claim_id": "C003",
      "support_status": "requires_label_or_local_vet",
      "risk_gate": "drug_specific_boundary"
    }
  ]
}
```

### Phase F: Wiki-Audited Revision

目标：不是让 Wiki 生成回答，而是让 Wiki 审计结果修订回答。

修订原则：

- 保留临床自然表达。
- 删除或降级无证据高风险内容。
- 对处方建议加边界。
- 对支持治疗保留实用性。
- 不把 source/fact/page 写进主回答。

输入：

- 原始 `assistant_answer_draft`
- claim audit
- risk gates
- retrieved evidence summary

输出：

```json
{
  "assistant_answer_final": "...",
  "revision_actions": [
    "downgraded_final_diagnosis_to_suspected_direction",
    "added_drug_label_boundary",
    "removed_unsourced_withdrawal_period"
  ],
  "wiki_used_in_revision": true
}
```

### Phase G: Dual Judge + Arbiter

建议拆成两个独立裁判体系。

#### G1 临床质量裁判

只看：

- 用户问题是否真实。
- 回答是否直接解决问题。
- 是否有临床判断。
- 是否有处置方案。
- 是否有处方化治疗框架。
- 是否自然、可训练。

不因为缺 Wiki anchor 扣分。

#### G2 Wiki 证据裁判

只看：

- claim 是否有证据。
- 高风险内容是否被降级或修订。
- 处方、剂量、休药期、监管内容是否合规。
- evidence anchors 是否足够。

最终由 arbiter 合并。

### Phase H: Export & Stratification

导出时每条样本至少有三层文本：

1. `assistant_answer_draft`
   - LLM 原始临床回答。

2. `assistant_answer_final`
   - Wiki 审计修订后的训练回答。

3. `audit_explanation`
   - 不进训练主回答，但供审查。

## 六、字段设计建议

建议保留原 54 字段作为 baseline comparison 兼容层，同时新增后移架构字段。

### 6.1 新增核心字段

| 字段 | 含义 |
|---|---|
| generation_mode | clinical_first_llm |
| wiki_used_in_generation | 是否生成时使用 Wiki，默认 false |
| wiki_used_in_audit | 是否审计时使用 Wiki |
| assistant_answer_draft | 原始 LLM 回答 |
| assistant_answer_final | Wiki 审计修订后的最终回答 |
| claim_count | 抽取 claim 数 |
| supported_claim_count | Wiki 支撑 claim 数 |
| unsupported_claim_count | 未支撑 claim 数 |
| contradicted_claim_count | 冲突 claim 数 |
| prescription_claim_count | 处方相关 claim 数 |
| prescription_boundary_status | 处方边界状态 |
| revision_required | 是否需要修订 |
| revision_action_count | 修订动作数量 |
| revision_actions | 修订动作 JSON |
| wiki_audit_decision | accepted/review/rejected |
| clinical_quality_decision | accepted/review/rejected |
| final_export_decision | main_sft/low_weight_sft/repair/reject |

### 6.2 证据字段保留但语义改变

旧字段：

- `evidence_anchor_count`
- `source_trust`
- `evidence_coverage`
- `phase15_final_decision`

新语义：

- 不再表示“生成时用了多少证据”。
- 改为表示“生成后审计找到了多少证据”。

例如：

```text
evidence_coverage = post_generation_supported
source_trust = post_generation_wiki_audit_A1
```

## 七、样本分层策略

### 7.1 main_sft

进入条件：

- 临床质量高。
- 处方化回答完整。
- 高风险 claim 均 supported 或已安全降级。
- 没有 contradicted claim。
- 无监管越界。

### 7.2 low_weight_sft

进入条件：

- 临床质量好。
- 少量 unsupported 低风险 claim。
- 处方只有类别级建议，无精确剂量。
- Wiki 审计建议 review，但无 fatal risk。

### 7.3 repair_queue

进入条件：

- 问答自然，但存在：
  - 无证据疾病断言。
  - 用药边界不清。
  - 支持治疗可保留但诊断需要降级。

### 7.4 reject_queue

进入条件：

- 编造检测结果。
- 线上确诊重大疫病。
- 编造剂量/休药期。
- 给出调运、扑杀、封锁等监管执行结论。
- 与 Wiki 高可信证据冲突且未修订。

## 八、与当前系统的落地迁移路径

### 阶段 1：保留现有系统，新增 clinical-first 分支

新增脚本建议：

```text
tools/pipeline/clinical_first/generate_clinical_cases.py
tools/pipeline/clinical_first/generate_clinical_qa.py
tools/pipeline/clinical_first/extract_claims.py
tools/pipeline/clinical_first/wiki_retrieve_for_claims.py
tools/pipeline/clinical_first/wiki_audit_claims.py
tools/pipeline/clinical_first/revise_with_wiki_audit.py
tools/pipeline/clinical_first/export_clinical_first_dataset.py
```

不要立即删除 Phase12-16。

### 阶段 2：双轨对比

同时跑：

1. 旧 wiki-first。
2. 新 clinical-first + wiki-audited。

对比指标：

- 用户问题自然度。
- 临床处置完整度。
- 处方化治疗覆盖率。
- unsupported claim 率。
- 高风险越界率。
- 修订后 train-ready 率。
- 人工抽审通过率。

### 阶段 3：迁移评估体系

把当前 Phase15 改造成：

```text
post_generation_wiki_audit
```

把当前 Phase18 拆成：

```text
clinical_quality_judge
wiki_evidence_judge
arbiter
```

### 阶段 4：正式切换

当新链路满足：

- 真实问诊质量明显优于 wiki-first。
- 高风险越界不高于 wiki-first。
- 修订后 train-ready 率稳定。
- 人工审查通过。

再将默认生成入口切到 clinical-first。

## 九、新旧方案对比

| 维度 | 旧 wiki-first | 新 wiki-post-generation |
|---|---|---|
| 用户问题 | 容易受 Wiki 缺口污染 | 由临床场景生成，更像养殖户 |
| 回答风格 | 容易审计腔、追问腔 | 先临床处置，再少量补问 |
| 处方能力 | 前置压制，偏拒答 | 给处方化框架，后置审计 |
| 事实可靠性 | 生成时强约束 | 生成后 claim 审计和修订 |
| 证据字段 | 生成输入的一部分 | 审计输出的一部分 |
| 训练可用性 | 稳但不自然 | 自然度高，需后置过滤 |
| 风险控制 | 强但保守 | 分层控制，更接近真实临床 |

## 十、关键风险与防护

### 风险 1：LLM 初稿幻觉更多

防护：

- claim extraction 必须细。
- 高风险 claim 必须 Wiki 审计。
- 不支持的高风险内容必须修订或拒绝。

### 风险 2：处方建议失控

防护：

- 精确剂量/疗程/休药期必须有标签级证据。
- 无证据只能给药物类别和现场兽医确认边界。
- 禁药、超范围用药、重大疫病盲目用药直接 hard fail。

### 风险 3：修订后回答变回审计腔

防护：

- 修订 prompt 禁止 source/fact/page 出现在主回答。
- 保留 `audit_explanation` 单独字段。
- 临床质量裁判必须独立评分自然度。

### 风险 4：Wiki 检索召回不足

防护：

- 疾病、症状、药物、风险词多路召回。
- 高风险 claim 扩展到 rule cards 和 drug labels。
- 检索不到不等于通过，而是 `unsupported` 或 `requires_review`。

## 十一、建议的新验收指标

### 生成质量指标

- farmer_query_realism_rate
- direct_answer_rate
- prescription_style_rate
- followup_overuse_rate
- clinical_actionability_rate

### Wiki 审计指标

- claim_extraction_success_rate
- supported_claim_rate
- unsupported_high_risk_claim_rate
- contradicted_claim_rate
- prescription_boundary_pass_rate
- regulatory_boundary_pass_rate

### 修订指标

- revision_required_rate
- revision_success_rate
- post_revision_hard_fail_rate
- post_revision_train_ready_rate

### 人工抽审指标

- clinician_acceptance_rate
- farmer_language_acceptance_rate
- unsafe_prescription_escape_count

## 十二、推荐优先实施的最小闭环

第一版不要直接全量重写，建议先做 30 条最小闭环：

```text
1. 从现有 case_seed 生成 clinical-first QA
2. 抽取 answer claims
3. 对 claim 做 Wiki 检索
4. 做 Wiki audit
5. 对有问题回答做一次 revision
6. 导出 draft/final/audit 三份字段
7. 人工审查 30 条
```

最小闭环输出：

```text
exports/clinical_first/generated_samples/clinical_first_samples_{run_id}.jsonl
exports/clinical_first/claim_audit/claim_audit_{run_id}.jsonl
exports/clinical_first/revised_samples/revised_samples_{run_id}.jsonl
exports/clinical_first/comparisons/clinical_first_comparison_{run_id}.csv
```

## 十三、最终建议

推荐把系统定位改成：

```text
LLM 负责临床表达和真实问诊生成。
Wiki 负责证据审计、风险边界、修订和训练准入。
```

不要再让 Wiki 在生成前决定 LLM “能不能说什么”，而是让 Wiki 在生成后回答：

1. 这句话有没有证据？
2. 这句话有没有风险？
3. 这句话该保留、降级、修订还是拒绝？
4. 修订后能不能进入训练集？

这样既能保留真实临床问答的质量，又能保留 Wiki 体系的最大价值：可信、可追溯、可审计、可治理。
