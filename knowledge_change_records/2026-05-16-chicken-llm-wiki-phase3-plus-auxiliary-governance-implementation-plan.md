# 鸡病 LLM Wiki 融入 Phase 3+ 辅助治理实施方案

日期：2026-05-16

适用项目：

- `D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline`
- `D:/XF-ChongQin/ai-/knowledge/llm_wiki_chicken_authoritative`

## 1. 目标

本方案用于改造当前 LLM-first 鸡病数据生成链路，使鸡病 LLM Wiki 在 Phase 3 及后续阶段中更有效地发挥辅助作用。

核心目标：

- 生成阶段仍由大模型自主生成自然问诊，不注入 Wiki 长文本，不加入生成期安全治理约束。
- Phase 3 及后续阶段使用鸡病 LLM Wiki 做结构化事实校验、安全边界判断和最小修复。
- 最终 CSV 仍由 Phase 9 双裁判和必要仲裁判断 `accepted/rejected`。
- Wiki 的定位是辅助，不允许显著削弱全链路执行效率。

## 2. 当前链路

当前主链路：

```text
Phase 1  样本规划
Phase 2  真实 API 大模型生成
Phase 3  claim extraction
Phase 4  Wiki evidence retrieval
Phase 5  claim fact and safety governance
Phase 6  span-based remediation
Phase 6b remediation reevaluation
Phase 7  cleaning and standardization
Phase 8  export adapter
Phase 9  dual judge and selective arbitration
```

当前关键文件：

```text
run_llm_first_chicken_parallel40_full_chain.py
extract_consultation_answer_claims.py
retrieve_wiki_evidence_for_claims.py
evaluate_claim_fact_and_safety_governance.py
remediate_answers_with_wiki_evidence.py
review_remediated_answers.py
clean_and_standardize_training_candidates.py
export_admitted_training_datasets.py
llm_first_dual_judge_and_arbitrate.py
llm_first_compact_judge_prompts.py
common/species_runtime_registry.py
common/compact_governance.py
```

## 3. 当前问题

### 3.1 Phase 3 claim 过细

最近一次 16 条链路中，Phase 3 抽出约 993 个 claim，平均每条约 62 个。大量细碎 claim 会直接放大 Phase 4 的检索量。

问题表现：

- 同一药物方案被拆成药物名、剂量、频次、疗程、休药期、注意事项等多个 claim。
- 同一诊断段被拆成过多低价值事实 claim。
- Phase 4 必须为大量 claim 扫描 Wiki facts/drug index。

### 3.2 Phase 4 Wiki 检索效率受 claim 数拖累

Phase 4 当前使用本地结构化 Wiki 产物，不调用大模型，但 claim 数过多时仍然慢。

现有 Wiki 产物：

```text
runtime_core_manifest.json
knowledge_facts.json
drug_gold_role_index.csv
rule_index.csv
source_authority_status_index.csv
exporter_hard_block_rules.json
```

### 3.3 Phase 5 的 Wiki 作用需要更清晰地传递给后续阶段

Phase 5 已能基于 `support_polarity`、`support_scope`、`claim_type_coverage` 判断支持、反证、缺证和 unsafe，但后续 Phase 9 主要消费 compact summary。

如果 compact summary 过弱，裁判难以感知 Wiki 的实际贡献。

### 3.4 Phase 6b 和 Phase 9 有部分重复

Phase 6b 做 remediation 复评，Phase 9 再做大模型裁判。如果 Phase 6b 重跑过多逻辑，会拖慢链路。

## 4. 总体原则

### 4.1 Wiki 不进入 Phase 2

Phase 2 保持：

- 不注入 Wiki 原文。
- 不要求引用 Wiki。
- 不加入生成期安全治理约束。
- 只让大模型生成自然的用户问题、诊断、处方和处理建议。

原因：

- 保持问答自然。
- 避免生成变成百科式回答。
- 避免 token 和延迟显著增加。

### 4.2 Wiki 只以结构化方式进入 Phase 3+

允许使用：

- Wiki fact index
- drug index
- rule index
- source authority index
- hard block rules
- compact governance summary

禁止引入：

- 大段 Wiki Markdown 原文
- 完整 Wiki evidence anchors 进入 Phase 9 prompt
- Phase 2 生成阶段的 Wiki 证据注入

### 4.2.1 现有代码兼容硬约束

本方案必须以当前 pipeline 的真实字段契约为迁移起点，不能只替换文档中的概念名。

当前代码已经稳定消费的 canonical claim types 为：

```text
disease_fact
clinical_sign
diagnostic_reasoning
differential_diagnosis
field_action
medication_class
specific_drug
dosage_or_course
withdrawal_or_residue
food_safety
regulatory_action
biosecurity
unsupported_generalization
safe_boundary_statement
```

因此，Phase 3 的“合并式 claim 类型”不得直接替换 `claim_type`，除非同时完成 Phase 4/5/6/6b/测试的全链路迁移。

推荐落地方式：

```text
claim_type             保持现有 canonical 类型，供下游代码稳定消费
claim_group_type       新增合并式分组类型，如 drug_execution_claim
claim_granularity      merged | atomic
evidence_intent        新增检索意图
```

如果后续确实要把 `claim_type` 改成新命名，必须在同一 Stage 内完成以下改动：

```text
extract_consultation_answer_claims.py
retrieve_wiki_evidence_for_claims.py
evaluate_claim_fact_and_safety_governance.py
remediate_answers_with_wiki_evidence.py
review_remediated_answers.py
tests/test_llm_first_phase3_claim_extraction.py
```

并增加新旧类型映射回归测试，证明高风险 claim、药物检索、治理判断和 span 修复没有降级。

### 4.3 性能硬约束

建议设置：

```text
每条样本 max_claims = 35
每条样本 max_needs_evidence_claims = 25
每条样本 max_evidence_anchors = 50
每个 claim max_anchors = 3
Phase 4 fact candidates top_k = 2-3
Phase 4 drug candidates top_k = 2
Phase 9 不传完整 evidence_anchors
```

## 5. 目标链路

改造后的目标链路：

```text
Phase 2
大模型自主生成自然问诊
        ↓
Phase 3
Wiki-aware merged claim extraction，但不查 Wiki
        ↓
Phase 4
轻量结构化 Wiki evidence retrieval
        ↓
Phase 5
Wiki-supported governance and compact summary
        ↓
Phase 6
Wiki-guided span-based minimal remediation
        ↓
Phase 6b
lightweight remediation reevaluation
        ↓
Phase 7
cleaning and standardization
        ↓
Phase 8
thin export adapter
        ↓
Phase 9
dual judge + selective arbitration
```

## 6. Phase 3 实施方案

文件：

```text
extract_consultation_answer_claims.py
tests/test_llm_first_phase3_claim_extraction.py
```

### 6.1 目标

Phase 3 不直接查 Wiki，但需要抽取更适合 Wiki 检索的合并式 claim。

目标指标：

```text
每条样本 claim_count: 15-30
每条样本 needs_evidence_count: 10-20
每条样本 high_risk_claim_count: 3-8
```

### 6.2 新 claim 类型

建议引入或映射到以下合并式 claim group 类型。

落地时优先新增 `claim_group_type`，不要直接替换现有 `claim_type`：

```text
claim_group_type             canonical claim_type
diagnosis_claim              diagnostic_reasoning | disease_fact | clinical_sign
differential_claim           differential_diagnosis
drug_execution_claim         specific_drug | dosage_or_course
withdrawal_claim             withdrawal_or_residue
regulatory_claim             regulatory_action | food_safety
biosecurity_claim            biosecurity
management_claim             field_action
supportive_care_claim        field_action | unsupported_generalization
case_context_claim           原 claim_type 保持不变，is_case_context_claim=true
safe_boundary_claim          safe_boundary_statement
```

兼容原则：

```text
Phase 4/5/6 在完成全链路迁移前继续读取 canonical claim_type
新增 claim_group_type 只用于统计、合并策略、检索路由辅助和可读审计
HIGH_RISK_TYPES 继续覆盖 specific_drug/dosage_or_course/withdrawal_or_residue/food_safety/regulatory_action
drug_execution_claim 不能让 specific_drug 与 dosage_or_course 的高风险语义消失
```

### 6.3 药物 claim 合并

当前不应把同一个药物方案拆成多个 claim。建议合并为：

```json
{
  "claim_id": "CLAIM-0001",
  "claim_type": "dosage_or_course",
  "claim_group_type": "drug_execution_claim",
  "claim_text": "...",
  "source_span": {"start": 120, "end": 260},
  "drug_names": ["盐酸多西环素"],
  "dose_mentions": ["每1L水添加0.05g"],
  "course_mentions": ["连用5天"],
  "route_mentions": ["混饮"],
  "withdrawal_mentions": [],
  "risk_level": "high",
  "needs_evidence": true,
  "evidence_intent": ["drug_label", "dose_boundary", "species_allowed"],
  "species_key": "chicken"
}
```

休药期兼容要求：

```text
如果同一药物方案中出现休药期、弃蛋期、上市/出栏残留边界，必须保留独立 canonical claim_type=withdrawal_or_residue claim。
或者在合并 claim 中增加 canonical_claim_types=["dosage_or_course","withdrawal_or_residue"]，并将 evidence_intent 加入 withdrawal_residue。
Phase 4 必须根据 withdrawal_or_residue 或 evidence_intent=withdrawal_residue 补查 withdrawal/MRL rule cards，不能只走 drug label/dose 路由。
不得因为 drug_execution_claim 合并而跳过休药期、弃蛋期、残留或 MRL 的高风险治理。
```

推荐字段：

```json
{
  "canonical_claim_types": ["specific_drug", "dosage_or_course"],
  "evidence_intent": ["drug_label", "dose_boundary", "species_allowed"]
}
```

如果包含休药期或残留边界，必须额外形成独立 claim 或等价的检索意图：

```json
{
  "claim_type": "withdrawal_or_residue",
  "claim_group_type": "withdrawal_claim",
  "canonical_claim_types": ["withdrawal_or_residue"],
  "withdrawal_mentions": ["休药期7天"],
  "evidence_intent": ["withdrawal_residue", "mrl_rule", "product_label"]
}
```

### 6.4 诊断 claim 合并

诊断段建议合并为：

```json
{
  "claim_id": "CLAIM-0002",
  "claim_type": "diagnostic_reasoning",
  "claim_group_type": "diagnosis_claim",
  "disease_field": "鸡新城疫",
  "diagnosis_certainty": "suspected",
  "symptom_basis": ["突然死亡", "神经症状", "产蛋下降"],
  "source_span": {"start": 20, "end": 110},
  "risk_level": "medium",
  "needs_evidence": true,
  "evidence_intent": ["clinical_fact", "disease_symptom_match"]
}
```

### 6.5 高风险优先规则

必须保留并测试：

```text
只要 claim_type 属于高风险类型，即使该句同时包含 case context，也必须 needs_evidence=true。
```

### 6.6 Phase 3 输出新增统计

每条 claim record 增加：

```json
{
  "claim_granularity": "merged",
  "claim_count_by_group_type": {
    "diagnosis_claim": 1,
    "drug_execution_claim": 3
  },
  "claim_count_by_canonical_type": {
    "diagnostic_reasoning": 1,
    "dosage_or_course": 3,
    "withdrawal_or_residue": 1
  },
  "needs_evidence_count": 18,
  "high_risk_claim_count": 6
}
```

字段约束：

```text
claim_count_by_group_type 统计 claim_group_type。
claim_count_by_canonical_type 统计现有 claim_type。
如果只保留一个统计字段，字段名必须显式包含 group 或 canonical，避免 Phase 4/5/6 下游误读。
```

### 6.7 验收

命令：

```powershell
py -m pytest D:\XF-ChongQin\ai-\tests\test_llm_first_phase3_claim_extraction.py -q
```

验收标准：

```text
16 条样本 claim 总数下降 50% 以上
source_span 仍可准确切回原文
高风险 claim 全部 needs_evidence=true
真实 UTF-8 中文 fixtures 通过
```

## 7. Phase 4 实施方案

文件：

```text
retrieve_wiki_evidence_for_claims.py
common/species_runtime_registry.py
```

### 7.1 目标

Phase 4 是 Wiki 直接发挥作用的主要阶段。目标是轻量、高精度、可审计。

继续使用鸡病 Wiki runtime artifacts：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_chicken_authoritative/exports/runtime_core_manifest.json
D:/XF-ChongQin/ai-/knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.json
D:/XF-ChongQin/ai-/knowledge/llm_wiki_chicken_authoritative/exports/drug_gold_role_index.csv
D:/XF-ChongQin/ai-/knowledge/llm_wiki_chicken_authoritative/exports/rule_index.csv
D:/XF-ChongQin/ai-/knowledge/llm_wiki_chicken_authoritative/exports/source_authority_status_index.csv
D:/XF-ChongQin/ai-/knowledge/llm_wiki_chicken_authoritative/exports/exporter_hard_block_rules.json
```

### 7.2 按 claim_type 路由检索

检索路由分两层实现。

第一层必须支持当前 canonical `claim_type`：

```text
diagnostic_reasoning  -> disease facts
disease_fact          -> disease facts
clinical_sign         -> disease/symptom facts
differential_diagnosis -> disease/symptom facts
specific_drug         -> drug index + drug rule cards
dosage_or_course      -> drug index + drug rule cards
withdrawal_or_residue -> withdrawal/MRL rule cards
food_safety           -> regulatory rule cards
regulatory_action     -> regulatory rule cards
biosecurity           -> management/biosecurity facts
field_action          -> management facts
safe_boundary_statement -> rule boundary cards
```

第二层可选支持 `claim_group_type`，用于合并式 claim 的增强路由：

```text
diagnosis_claim       -> disease facts
differential_claim    -> disease/symptom facts
drug_execution_claim  -> drug index + drug rule cards
withdrawal_claim      -> withdrawal/MRL rule cards
regulatory_claim      -> regulatory rule cards
biosecurity_claim     -> management/biosecurity facts
management_claim      -> management facts
safe_boundary_claim   -> rule boundary cards
```

落地要求：

```text
如果 claim_group_type 存在，Phase 4 可优先用它缩小候选集
如果 claim_group_type 缺失，Phase 4 必须退回 canonical claim_type
不得出现新 claim_group_type 导致 drug index 不检索的情况
如果 evidence_intent 包含 withdrawal_residue/mrl_rule/product_label，必须触发 withdrawal/MRL rule cards 检索
```

### 7.3 Anchor 数限制

建议限制：

```text
diagnosis_claim:      max 2 fact anchors
drug_execution_claim: max 2 drug anchors + 1 rule anchor
withdrawal_claim:     max 1 drug/rule anchor
regulatory_claim:     max 1-2 rule anchors
management_claim:     max 1 fact/rule anchor
biosecurity_claim:    max 1 fact/rule anchor
```

全局限制：

```text
每个 claim max_anchors = 3
每条样本 max_evidence_anchors = 50
```

### 7.4 Claim signature 缓存

新增批次内存缓存：

```text
species_key + disease_field + claim_type + claim_group_type + normalized_subject + normalized_object + normalized_drug_names + normalized_dose_mentions
```

建议函数：

```python
def claim_signature(claim: dict[str, Any], profile: SpeciesRuntimeProfile) -> str:
    ...
```

可选落盘缓存：

```text
exports/cache/wiki_evidence_cache_chicken.jsonl
```

缓存记录：

```json
{
  "claim_signature": "...",
  "species_key": "chicken",
  "artifact_provenance_hash": "...",
  "anchors": []
}
```

缓存失效条件：

```text
artifact_provenance_hash 不一致
species_key 不一致
```

缓存命中后的强制处理：

```text
缓存命中后必须 deep copy anchors。
必须将每个 anchor.claim_id 重写为当前 claim.claim_id。
artifact_provenance_hash、fact_id、rule_card_id、source_id 可以复用。
claim_id 不可复用，否则 Phase 5 会按旧 claim_id 分组，导致当前 claim 被误判为 unsupported。
```

### 7.5 Disease field 优先绑定

Phase 4 检索时优先使用：

```text
claim.disease_field
case_context.target_entity
raw_record.entity_name
```

用于提高疾病相关 facts 的召回精度。

### 7.6 保留结构化 support 字段

必须继续输出：

```text
support_polarity
support_scope
claim_type_coverage
authority_level
source_trust
rule_card_id
fact_id
match_confidence
evidence_quote_span
```

字段含义：

```text
support_polarity:
  positive  正向支持
  negative  反证、禁用、禁止
  boundary  标签、兽医、监管或边界要求

support_scope:
  clinical_fact
  drug_label_or_rule
  withdrawal_residue
  food_safety_regulatory
  field_management
  rule_boundary

claim_type_coverage:
  exact
  partial
  broader_boundary
  unmatched
```

### 7.7 验收

验收标准：

```text
Phase 4 不读取 Wiki markdown 全文
16 条 Phase 4 耗时目标 15-25s
单条样本 evidence_anchor_count <= 50
高风险 claim 严格要求 A0/positive/exact
跨物种 evidence 被 species isolation 拦截
```

## 8. Phase 5 实施方案

文件：

```text
evaluate_claim_fact_and_safety_governance.py
common/compact_governance.py
```

### 8.1 目标

Phase 5 是 Wiki 治理判断层，不做大模型评分。

职责：

```text
claim + evidence anchors -> supported / contradicted / unsafe / unsupported
```

### 8.2 高风险支持条件

高风险 claim 必须满足：

```text
source_trust == authoritative
authority_level == A0
support_polarity == positive
claim_type_coverage == exact
```

否则不能判为 supported。

### 8.3 非高风险支持条件

非高风险 claim 可接受：

```text
source_trust == authoritative
support_polarity in {positive, boundary}
claim_type_coverage in {exact, partial, broader_boundary}
```

### 8.4 新增 reason codes

建议增加：

```text
unsupported_precise_dose
unsupported_withdrawal_period
negative_trap_evidence
drug_not_species_supported
regulatory_execution_without_rule_support
clinical_diagnosis_weak_support
field_management_partially_supported
cross_species_evidence_blocked
```

### 8.5 增强 compact governance summary

建议输出：

```json
{
  "compact_governance_summary": {
    "wiki_governance_passed": false,
    "wiki_fact_score": 0.82,
    "wiki_safety_score": 0.5,
    "supported_claim_count": 18,
    "unsupported_high_risk_claim_count": 3,
    "contradicted_claim_count": 0,
    "unsafe_claim_count": 1,
    "negative_anchor_count": 0,
    "boundary_anchor_count": 8,
    "drug_execution_claim_count": 5,
    "drug_execution_supported_count": 2,
    "regulatory_claim_count": 1,
    "regulatory_supported_count": 1,
    "top_wiki_governance_reasons": [
      "unsupported_precise_dose",
      "drug_execution_requires_label_or_veterinarian_boundary"
    ]
  }
}
```

### 8.6 验收

```text
Phase 5 16 条 <3s
每条样本都有 compact_governance_summary
summary 能表达 Wiki 支持、缺证、反证和 unsafe
Phase 9 不需要读取完整 evidence anchors
```

## 9. Phase 6 实施方案

文件：

```text
remediate_answers_with_wiki_evidence.py
```

### 9.1 目标

Phase 6 使用 Phase 5 的 Wiki governance 结果做最小 span 修复，不整篇重写。

### 9.2 修复规则

#### unsupported precise dose

原文示例：

```text
每1L水添加0.05g，连用5天
```

修复为：

```text
具体用量和疗程按产品标签及现场兽医处方执行
```

#### unsupported withdrawal period

原文示例：

```text
休药期7天
```

修复为：

```text
休药期按产品标签和当地监管要求执行
```

#### regulatory execution risk

原文示例：

```text
立即扑杀
```

修复为：

```text
立即隔离并联系当地兽医或主管部门，按官方要求处置
```

#### negative-trap evidence

如果 anchor `support_polarity=negative`，对应 span 应删除或改为禁用提醒。

#### cross-species term

如果鸡病回答出现猪病术语，替换或删除。

### 9.3 Lineage

每个修复动作记录：

```json
{
  "claim_id": "CLAIM-0004",
  "source_span": {"start": 120, "end": 160},
  "reason_code": "unsupported_precise_dose",
  "before": "...",
  "after": "...",
  "evidence_basis": ["DRUG-...", "RC-..."]
}
```

### 9.4 验收

```text
Phase 6 16 条 <2s
不整篇重写
unsupported_high_risk/unsafe 数量下降
final_answer 自然度不明显下降
```

## 10. Phase 6b 实施方案

文件：

```text
review_remediated_answers.py
```

### 10.1 目标

Phase 6b 改为轻量 delta review，不重复完整 evidence retrieval。

当前 `review_remediated_answers.py` 会重新执行 claim extraction、evidence retrieval 和 governance evaluation。该行为与本节目标不一致，因此 Phase 6b 轻量化必须作为显式代码改造项，而不能视为现状。

推荐迁移路径：

```text
第一步：保留当前 full reevaluation 模式，新增 --review-mode full|delta，CLI 默认 full
第二步：实现 delta 模式，只读取 remediation_lineage、原 governance summary、final_answer 和清理检查结果
第三步：smoke 通过后，把全链路 runner 的 Phase 6b 调用切换为 --review-mode delta
第四步：保留 full 模式作为 debug/抽检入口，不走默认主链路
```

### 10.2 检查项

只检查：

```text
unsupported_high_risk_claim_count 是否下降
unsafe_claim_count 是否为 0
contradicted_claim_count 是否为 0
species_isolation_status 是否 passed
internal_marker 是否清除
case_context/generation_policy/species binding 是否继承
```

delta 模式允许使用的输入：

```text
Phase 5 compact_governance_summary
Phase 6 remediation_lineage
Phase 6 revised_assistant_answer/final_answer
原始 case_context/generation_policy/species metadata
内部 marker/跨物种禁词本地正则检查
```

delta 模式禁止：

```text
调用 retrieve_wiki_evidence_for_claims.retrieve_for_claim_record
扫描 knowledge_facts/drug index/rule index
生成新的 evidence_anchors
新增事实支持判断
```

能力边界：

```text
delta 模式只验证既有治理问题是否被处理，以及本地硬规则问题是否清除。
delta 模式不能声明新增事实安全证明。
如需重新证明事实支持、发现新增事实错误或重新生成 evidence anchors，必须使用 full reevaluation 或抽检模式。
```

### 10.3 验收

```text
Phase 6b 16 条 <10s
仍输出复评结论
不重复 Phase 4 完整检索
```

## 11. Phase 7 和 Phase 8 实施方案

文件：

```text
clean_and_standardize_training_candidates.py
export_admitted_training_datasets.py
```

### 11.1 Phase 7

只做：

```text
清理空白和异常字符
清除内部 marker
统一 question/final_answer
保留 compact_governance_summary
保留 claim/remediation lineage
```

不做：

```text
不查 Wiki
不做新的事实判断
不输出最终训练队列
```

注意：当前 Phase 7 内部仍使用 `candidate_route` 表示中间清洗路由，例如 `candidate_pool`、`repair_queue`、`rejected_queue`。本方案不要求在 Stage 1 立即删除该中间字段。

边界定义：

```text
Phase 7 中间 JSONL 可暂时保留 candidate_route/candidate_cleaning_status
Phase 7 不得恢复 main_sft/low_weight_sft/sft_admission 等训练用途字段
Phase 8 之后面向 Phase 9 和最终 CSV 的记录不得暴露 repair_queue 作为训练队列字段
```

### 11.2 Phase 8

只做正式 export adapter。

保留字段：

```text
sample_id
species_key
disease_field
question/final_answer 所需字段
final_export_decision
final_export_reasons
compact_governance_summary
```

禁止输出：

```text
main_sft
low_weight_sft
repair_queue 作为最终训练队列字段
queue_routing
sft_admission
```

如果 Phase 7 仍输出 `candidate_route=repair_queue`，Phase 8 必须将其折叠为：

```text
final_export_decision = rejected
final_export_reasons 包含 needs_review_or_repair
```

最终 CSV 只允许出现：

```text
quality_decision = accepted | rejected
rejection_reason = accepted 时为空，rejected 时必须非空
```

### 11.3 验收

```text
Phase 7 + Phase 8 合计 <2s
最终 CSV 不出现训练队列字段
Phase 9 可读取 compact governance summary
```

## 12. Phase 9 实施方案

文件：

```text
llm_first_dual_judge_and_arbitrate.py
llm_first_compact_judge_prompts.py
```

### 12.1 输入原则

Phase 9 不查 Wiki，compact judge prompt 不传完整 anchors。

当前 `llm_first_dual_judge_and_arbitrate.py` 的 semantic sample 仍包含 `evidence_anchors`，并且结构检查会在 anchors 缺失时记录 `missing_evidence_anchors`。因此 Stage 6 必须同步修改 compact sample adapter 和 structure_check，否则本节目标不能成立。

边界说明：

```text
semantic JSONL 或 full_audit/debug 产物可以保留完整 evidence_anchors 用于审计。
默认 --judge-input-mode compact 的 judge_input 和 arbiter_input 不得包含完整 evidence_anchors。
本文中“Phase 9 不传完整 anchors”特指不传给默认 compact judge/arbiter prompt，不禁止审计产物保存 anchors。
```

只传：

```json
{
  "disease_field": "鸡新城疫",
  "question": "...",
  "final_answer": "...",
  "compact_governance_summary": {
    "wiki_governance_passed": true,
    "wiki_fact_score": 0.92,
    "wiki_safety_score": 1.0,
    "unsupported_high_risk_claim_count": 0,
    "unsafe_claim_count": 0,
    "contradicted_claim_count": 0,
    "top_wiki_governance_reasons": []
  }
}
```

### 12.2 裁判要求

裁判提示词应说明：

```text
把 compact_governance_summary 当作 Wiki 事实治理信号。
如果 unsupported_high_risk/unsafe/contradicted 非零，应在医学正确性、安全边界、可执行性中扣分。
不要要求完整 Wiki 引文。
不要重新审查隐藏 Wiki anchors。
```

实现要求：

```text
compact prompt 输入只包含 question/final_answer/disease_field/species_key/compact_governance_summary
judge_input 中不得出现 evidence_anchors
full_audit/debug 模式可以保留 anchors，但不得作为默认 --judge-input-mode compact 的输入
structure_check 不再把 compact 模式下缺少 anchors 判为错误
hard_gate 读取 compact_governance_summary 或 claim_review_lineage，不依赖完整 anchors
semantic JSONL/debug 产物即使保留 evidence_anchors，也不得被 compact prompt 直接消费
```

### 12.3 仲裁

继续保持当前 7 条仲裁准入，不扩大仲裁范围：

```text
policy forced
label disagreement
score gap >= 15
avg score gray zone 60-75
critical dimension gap >= 2
low confidence
judge fatal risk
```

输出仍为：

```text
quality_decision = accepted | rejected
rejection_reason = accepted 时为空，rejected 时必须非空
```

如果不需要仲裁：

```text
quality_decision = accepted
```

### 12.4 验收

```text
Phase 9 token 不显著增加
仲裁比例不因 Wiki 增强而显著上升
CSV 拒绝原因能体现 Wiki 支持/缺证/反证
compact judge_input 中不存在 evidence_anchors
compact 模式下 missing_evidence_anchors 不再触发结构错误
semantic JSONL/debug 产物如保留 evidence_anchors，不得被 compact prompt 直接消费
```

## 13. 实施顺序

### Stage 0：契约兼容和测试门禁

改动文件：

```text
extract_consultation_answer_claims.py
retrieve_wiki_evidence_for_claims.py
evaluate_claim_fact_and_safety_governance.py
remediate_answers_with_wiki_evidence.py
llm_first_dual_judge_and_arbitrate.py
tests/test_llm_first_phase3_claim_extraction.py
```

目标：

```text
明确 canonical claim_type 与 claim_group_type 的关系
保留现有 HIGH_RISK_TYPES 语义
补齐新旧类型映射测试
确认 Phase 4/5/6 消费端不会因新增 claim_group_type 降级
```

验收：

```powershell
py -m pytest D:\XF-ChongQin\ai-\tests\test_llm_first_phase3_claim_extraction.py -q
```

### Stage 1：Phase 3 claim 合并

改动文件：

```text
extract_consultation_answer_claims.py
tests/test_llm_first_phase3_claim_extraction.py
```

验收：

```powershell
py -m pytest D:\XF-ChongQin\ai-\tests\test_llm_first_phase3_claim_extraction.py -q
```

### Stage 2：Phase 4 检索路由和缓存

改动文件：

```text
retrieve_wiki_evidence_for_claims.py
```

验收：

```text
16 条 Phase 4 耗时下降到 15-25s
anchor 数受控
高风险证据严格
输出 phase4_cache_hit_count/phase4_cache_miss_count
缓存命中时 rewritten_anchor_claim_id_count 等于复用 anchor 数
```

### Stage 3：Phase 5 compact summary 强化

改动文件：

```text
evaluate_claim_fact_and_safety_governance.py
common/compact_governance.py
```

验收：

```text
Phase 5 <3s
summary 能解释 Wiki 治理结果
```

### Stage 4：Phase 6 span 修复增强

改动文件：

```text
remediate_answers_with_wiki_evidence.py
```

验收：

```text
Phase 6 <2s
修复 lineage 完整
```

### Stage 5：Phase 6b 轻量化

改动文件：

```text
review_remediated_answers.py
```

验收：

```text
Phase 6b 16 条 <10s
默认 runner 使用 delta 模式
full reevaluation 仅作为 debug/抽检模式保留
delta 模式不调用 retrieve_for_claim_record
```

### Stage 6：Phase 9 prompt 接入 Wiki summary

改动文件：

```text
llm_first_dual_judge_and_arbitrate.py
llm_first_compact_judge_prompts.py
```

验收：

```text
Phase 9 不传完整 anchors
compact judge_input 不含 evidence_anchors
structure_check 不再要求 compact 模式必须有 anchors
debug/full_audit 审计产物可保留 evidence_anchors，但 compact prompt 不读取
最终 CSV accepted/rejected 正常
```

## 14. 压测方案

### 14.1 16 条 smoke

```powershell
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\run_llm_first_chicken_parallel40_full_chain.py --limit 16 --parallel 8 --species chicken --run-label chicken-wiki-aux-phase3plus-smoke16 --semantic-parallel 8 --judge-input-mode compact --arbitration-policy selective
```

### 14.2 40 条验证

```powershell
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\run_llm_first_chicken_parallel40_full_chain.py --limit 40 --parallel 8 --species chicken --run-label chicken-wiki-aux-phase3plus-40 --semantic-parallel 8 --judge-input-mode compact --arbitration-policy selective
```

### 14.3 100 条性能估算

```powershell
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\run_llm_first_chicken_parallel40_full_chain.py --limit 100 --parallel 8 --species chicken --run-label chicken-wiki-aux-phase3plus-100 --semantic-parallel 8 --judge-input-mode compact --arbitration-policy selective
```

## 15. 最终验收指标

16 条目标：

```text
Phase 2: 60-90s，取决于 API
Phase 3: <1s
Phase 4: 15-25s
Phase 5: <3s
Phase 6: <2s
Phase 6b: <10s
Phase 7: <1s
Phase 8: <1s
Phase 9: 不高于当前，最好下降
```

质量目标：

```text
disease_field 是明确疾病
question 口语化、非专业表格化
final_answer 诊断和处方具体、自然、合规
Wiki governance summary 能解释事实支持、缺证、反证
最终 CSV 只有 accepted/rejected
rejected 必须有 rejection_reason
```

## 16. 风险和边界

### 16.1 不能做的事

```text
不能在 Phase 2 注入 Wiki 长文本
不能把完整 evidence_anchors 传给默认 compact judge/arbiter prompt
debug/full_audit 审计产物可保留完整 evidence_anchors
不能让 Phase 7/8 做复杂治理
不能在最终导出或最终 CSV 恢复 repair_queue/main_sft/low_weight_sft 字段
不能让 Wiki 检索成为大模型调用
```

### 16.2 可接受的权衡

```text
Phase 4 可使用本地索引多做一点结构化判断
Phase 5 可输出更丰富 summary
Phase 6 可做更多 span 级安全边界修复
Phase 9 只通过 compact summary 感知 Wiki
```

## 17. 结论

本方案的核心是：

```text
Phase 3 控制 claim 粒度
Phase 4 用鸡病 Wiki 结构化检索
Phase 5 产出强 compact governance summary
Phase 6 做最小 span 修复
Phase 9 只用 summary 做质量裁判
```

这样鸡病 LLM Wiki 的作用会更清晰：

- 它不是生成器。
- 它不是裁判 prompt 的长文本材料。
- 它是事实、安全边界、药物和监管约束的结构化辅助系统。

同时，全链路不会因为 Wiki 的接入而显著降低执行效率。
