# LLM-first 鸡病数据链路：Wiki 高效治理与轻量裁判改造落地方案

日期：2026-05-16  
适用项目：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative`  
目标链路：鸡病 `llm-first` 真实生成、Wiki 后验治理、双裁判仲裁、最终 CSV 导出

## 1. 背景与实际问题

当前完整链路已能跑通：

- 主入口：`tools/pipeline/run_llm_first_chicken_parallel40_full_chain.py`
- 语义裁判入口：`tools/pipeline/llm_first_dual_judge_and_arbitrate.py`
- 旧裁判核心：`tools/pipeline/phase18_dual_judge_and_arbitrate.py`
- 裁判 prompt：`tools/pipeline/wiki_first_judge_prompts.py`

最新 8 条真实链路结果：

- Phase 2-8 全部通过。
- Phase 9 双裁判与仲裁全部完成。
- 总耗时：`551.174s`
- Phase 9 耗时：`524.547s`
- Phase 9 占总耗时约 95%。
- 8 条最终语义结果：`review=5`，`rejected=3`，`accepted=0`。
- 最长单条语义评审耗时：`402.236s`。

实际定位结果：

- Judge A/B 输入约 `9562 chars`。
- Arbiter 输入约 `33264 chars`。
- 但最终批量裁判理论上只需要：
  - `disease_field`
  - `question`
  - `final_answer`
  - 少量 Wiki 治理摘要
  - 简短评分规则

当前 Phase 9 慢的主要原因不是没有 API KEY 池，而是：

1. Wiki 后验治理产生的完整审计信息被重复塞入裁判 prompt。
2. Arbiter 又携带 Judge A/B 完整结果，导致输入再次膨胀。
3. fallback 链路过宽，失败后切换模型造成长尾延迟。
4. Phase 9 全量强制仲裁，每条样本至少 3 次真实模型调用。

## 2. 改造目标

本方案目标不是取消 Wiki，而是将 Wiki 从“后段裁判大 prompt”中剥离，保留其作为事实治理引擎的价值。

改造后应满足：

1. Wiki 在 Phase 4-6 深度参与事实治理。
2. Phase 9 默认批量模式不再传完整 Wiki anchors、case_context、stage lineage、hard gate 全量结构。
3. Phase 9 默认只传轻量字段与治理摘要。
4. 完整 Wiki 证据仍保存在 JSONL 审计文件中，供抽样审计和单条 debug 使用。
5. 最终 CSV 只保留样本本体、疾病字段、双裁判评分、仲裁评分、最终质量结论。
6. Phase 9 性能应显著提升，并避免单条 400s 长尾。

## 3. 新的信息分层

将当前 evidence/governance 信息分为三层。

### L1：完整审计层

用途：追溯、问题定位、抽样复核。

保留位置：

- `exports/generated_samples/llm-first-claim-evidence-*.jsonl`
- `exports/evaluated_samples/llm-first-claim-governance-*.jsonl`
- `exports/evaluated_samples/llm-first-remediated-answers-*.jsonl`
- `exports/evaluated_samples/llm-first-remediation-review-*.jsonl`

包含：

- 完整 `claims`
- 完整 `evidence_anchors`
- claim span
- support polarity
- support scope
- claim type coverage
- governance lineage
- remediation lineage

要求：

- 保留，不进入默认 Phase 9 prompt。

### L2：轻量治理摘要层

用途：Phase 9 批量裁判输入。

新增字段名：

```text
compact_governance_summary
```

字段结构：

```json
{
  "wiki_governance_passed": true,
  "unsupported_high_risk_claim_count": 0,
  "contradicted_claim_count": 0,
  "unsafe_claim_count": 0,
  "remaining_high_risk_claim_count": 0,
  "species_isolation_status": "passed",
  "internal_marker_leak": false,
  "removed_claim_count": 0,
  "boundary_rewrite_count": 0,
  "top_risk_codes": []
}
```

生成位置：

- Phase 8 export adapter 内生成并写入最终 export JSONL。
- 文件：`tools/pipeline/export_admitted_training_datasets.py`

同时 `llm_first_dual_judge_and_arbitrate.py` 需要在 `to_phase18_sample()` 中继承该字段。

### L3：最终 CSV 层

用途：训练数据质量结果表。

最终 CSV 只保留：

- 基础样本字段：
  - `sample_id`
  - `species_key`
  - `disease_field`
  - `question`
  - `final_answer`
- 语义终审字段：
  - `semantic_final_decision`
  - `semantic_final_total_score`
  - `semantic_sft_admission`
  - `semantic_main_issues`
- A/B 裁判一致维度评分
- Arbiter 维度评分
- 版本字段

禁止进入最终 CSV：

- `case_context_json`
- `raw_assistant_answer`
- `evidence_anchors`
- `hard_gate_check`
- `stage_1_draft`
- `stage_2_grounded`
- `semantic_route`
- `arbitration_trigger_codes`
- 模型名、key index、耗时、fallback 细节

当前该方向已部分完成，后续需保持。

## 4. 具体修改点

### 4.1 Phase 4：保留完整 evidence，但补充 compact evidence summary

文件：

```text
tools/pipeline/retrieve_wiki_evidence_for_claims.py
```

新增输出字段：

```text
compact_evidence_summary
```

字段：

```json
{
  "evidence_anchor_count": 0,
  "supported_claim_count": 0,
  "contradicted_claim_count": 0,
  "unsupported_high_risk_claim_count": 0,
  "regulatory_risk_count": 0,
  "drug_risk_count": 0,
  "species_mismatch_count": 0,
  "top_risk_codes": []
}
```

实现要求：

- 不删除现有 `evidence_anchors`。
- summary 从现有 anchors 和 claim review 结果聚合。
- summary 必须是稳定结构，缺失值填 0 或空数组。

### 4.2 Phase 5：生成 compact governance summary

文件：

```text
tools/pipeline/evaluate_claim_fact_and_safety_governance.py
```

新增函数：

```python
def build_compact_governance_summary(record: dict[str, Any]) -> dict[str, Any]:
    ...
```

输出字段：

```text
compact_governance_summary
```

聚合来源：

- `unsupported_high_risk_claim_count`
- `unsafe_claim_count`
- `contradicted_claim_count`
- `species_isolation_status`
- high-risk claim review results
- regulatory/drug hard detector results

必须保留的判断：

```text
wiki_governance_passed =
  unsupported_high_risk_claim_count == 0
  and unsafe_claim_count == 0
  and contradicted_claim_count == 0
  and species_isolation_status == "passed"
```

### 4.3 Phase 6：修复后更新 compact summary

文件：

```text
tools/pipeline/remediate_answers_with_wiki_evidence.py
```

新增或更新字段：

```json
{
  "removed_claim_count": 0,
  "boundary_rewrite_count": 0
}
```

要求：

- span-based remediation 不再只写 lineage，还要回写轻量计数。
- 删除 claim 后，`remaining_high_risk_claim_count` 应在复评阶段归零或保留实际剩余值。

### 4.4 Phase 6 Reevaluation：输出最终 compact summary

文件：

```text
tools/pipeline/review_remediated_answers.py
```

输出字段：

```text
compact_governance_summary
```

该字段是 Phase 9 默认使用的最终治理摘要。

必须包含：

```json
{
  "wiki_governance_passed": true,
  "remaining_high_risk_claim_count": 0,
  "unsupported_high_risk_claim_count": 0,
  "unsafe_claim_count": 0,
  "contradicted_claim_count": 0,
  "species_isolation_status": "passed",
  "internal_marker_leak": false,
  "removed_claim_count": 0,
  "boundary_rewrite_count": 0,
  "top_risk_codes": []
}
```

### 4.5 Phase 8：正式 export adapter 继承 compact summary

文件：

```text
tools/pipeline/export_admitted_training_datasets.py
```

修改：

- export record 必须保留 `compact_governance_summary`。
- 如果上游缺失，应从现有 lineage 重建一个最小 summary。
- 最小 summary 不允许为空。

验收：

- Phase 8 JSONL 每条都有 `compact_governance_summary`。

### 4.6 Phase 9：新增 compact judge 模式

文件：

```text
tools/pipeline/llm_first_dual_judge_and_arbitrate.py
```

新增 CLI 参数：

```text
--judge-input-mode compact|full_audit
```

默认：

```text
compact
```

`compact` 模式只向裁判传：

```json
{
  "disease_field": "呼吸道方向",
  "species_key": "chicken",
  "question": "...",
  "final_answer": "...",
  "compact_governance_summary": {...},
  "scorecard": {
    "dimensions": {...},
    "label_policy": "..."
  }
}
```

`full_audit` 模式保留当前重 prompt，用于抽样审计或 debug。

### 4.7 Phase 9 prompt 构造不要复用重型 wiki-first prompt

当前重 prompt 来源：

```text
tools/pipeline/wiki_first_judge_prompts.py
```

新增轻量 prompt 文件：

```text
tools/pipeline/llm_first_compact_judge_prompts.py
```

新增函数：

```python
def build_compact_judge_a_messages(sample: Mapping[str, Any]) -> list[dict[str, str]]:
    ...

def build_compact_judge_b_messages(sample: Mapping[str, Any]) -> list[dict[str, str]]:
    ...

def build_compact_arbiter_messages(
    sample: Mapping[str, Any],
    judge_a_result: Mapping[str, Any],
    judge_b_result: Mapping[str, Any],
    trigger_codes: list[str],
) -> list[dict[str, str]]:
    ...
```

compact judge 输入不得包含：

- `evidence_anchors`
- `case_context`
- `stage_1_draft`
- `stage_2_grounded`
- `hard_gate_check`
- `fact_level_check`
- `structure_check`
- `judge_input`
- `arbiter_input`

compact arbiter 输入只包含：

```json
{
  "disease_field": "...",
  "species_key": "chicken",
  "question": "...",
  "final_answer": "...",
  "compact_governance_summary": {...},
  "judge_a": {
    "total_score": 0,
    "weighted_total_score": 0,
    "final_label": "...",
    "dimension_scores": {...},
    "main_issues": []
  },
  "judge_b": {
    "total_score": 0,
    "weighted_total_score": 0,
    "final_label": "...",
    "dimension_scores": {...},
    "main_issues": []
  },
  "trigger_codes": []
}
```

## 5. Phase 9 高可用与效率控制

### 5.1 API KEY 池保留

继续使用现有：

- `WikiFirstLLMClient.RoundRobinKeyPool`
- `phase18_dual_judge_and_arbitrate.next_api_key`
- `mark_api_key_success`
- `mark_api_key_failure`

### 5.2 限制 model fallback

文件：

```text
tools/pipeline/phase18_dual_judge_and_arbitrate.py
```

新增配置读取：

```json
{
  "compact_judge": {
    "max_model_fallbacks": 1,
    "max_key_attempts_per_model": 2,
    "single_sample_timeout_seconds": 120,
    "json_value_error_fast_fail": true,
    "allowed_arbiter_models": [
      "ERNIE-4.5-Turbo-32K",
      "hunyuan-2.0-instruct-20251111"
    ]
  }
}
```

配置位置：

```text
ai-/config.json
```

要求：

- compact 模式禁止 fallback 到 `deepseek-v4-flash`。
- `ValueError` JSON 结构错误最多重试一次。
- 单条样本超过 `120s` 标记为 `review` 或 `repair_queue`，不能拖垮整批。

### 5.3 主 runner 参数

文件：

```text
tools/pipeline/run_llm_first_chicken_parallel40_full_chain.py
```

新增或确认参数：

```text
--semantic-parallel 4
--judge-input-mode compact
--semantic-timeout 120
--semantic-limit 0
--skip-semantic
```

默认：

```text
--judge-input-mode compact
--semantic-parallel 4
```

## 6. 最终 CSV 字段策略

最终 CSV 路径：

```text
exports/training_sets/llm-first-final-semantic-scored-{TODAY}-{label}.csv
```

字段保留策略：

### 基础字段

```text
sample_id
species_key
disease_field
question
final_answer
```

### 最终语义字段

```text
semantic_final_decision
semantic_final_total_score
semantic_sft_admission
semantic_main_issues
```

### A/B 裁判摘要

```text
judge_a_total_score
judge_a_weighted_total_score
judge_a_final_label
judge_b_total_score
judge_b_weighted_total_score
judge_b_final_label
judge_score_gap_abs
judge_average_total_score
```

### A/B 共同维度

每个维度：

```text
judge_<dimension>_weight
judge_<dimension>_a_score
judge_<dimension>_b_score
judge_<dimension>_score_gap
```

维度：

```text
scenario_realism
consultation_completeness
medical_correctness
followup_logic
triage_boundary
context_consistency
actionability
structure_labelability
```

### 仲裁字段

```text
arbiter_final_total_score
arbiter_weighted_total_score
arbiter_final_label
arbiter_sft_admission
arbiter_preferred_judge
arbiter_main_issues
arbiter_repair_suggestion
```

### 仲裁维度

每个维度：

```text
arbiter_<dimension>_weight
arbiter_<dimension>_score
```

维度：

```text
medical_correctness
safety_boundary
consultation_completeness
scenario_realism
context_consistency
information_sufficiency
actionability
communication_naturalness
```

### 版本字段

```text
scorecard_version
semantic_adapter_version
```

禁止字段：

```text
case_context_json
raw_assistant_answer
evidence_anchors
hard_gate_check
stage_1_draft
stage_2_grounded
semantic_route
arbitration_trigger_codes
api_key_index
api_key_indices_tried
judge_model
arbiter_model
elapsed_seconds
```

## 7. 测试方案

### 7.1 单元测试

新增或修改：

```text
ai-/tests/test_llm_first_compact_governance_summary.py
ai-/tests/test_llm_first_dual_judge_adapter.py
```

测试点：

1. Phase 5 生成 `compact_governance_summary`。
2. Phase 6 修复后更新 removed/boundary 计数。
3. Phase 8 export 每条都有 `compact_governance_summary`。
4. compact judge prompt 不包含：
   - `evidence_anchors`
   - `case_context`
   - `stage_1_draft`
   - `hard_gate_check`
5. A/B 维度 schema 必须一致。
6. 最终 CSV 不含中间状态字段。

### 7.2 回归测试

运行：

```powershell
py -m pytest ai-/tests/test_llm_first_dual_judge_adapter.py -q
py -m pytest ai-/tests/test_llm_first_phase5_phase6_governance_remediation.py ai-/tests/test_llm_first_phase8_export_adapter.py ai-/tests/test_llm_first_end_to_end_and_failure_regressions.py -q
```

### 7.3 真实链路验收

先跑轻量：

```powershell
py D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\run_llm_first_chicken_parallel40_full_chain.py `
  --limit 8 `
  --parallel 8 `
  --species chicken `
  --run-label chicken-real8-compact-judge-v1 `
  --semantic-parallel 4 `
  --judge-input-mode compact
```

验收指标：

```text
Phase 2-8 passed = true
Phase 9 passed = true
final CSV exists = true
final CSV field_count <= 80
Phase 9 total elapsed <= 240s for 8 samples
single semantic sample elapsed <= 120s
fallback to deepseek-v4-flash = 0
```

再跑抽样 full audit：

```powershell
py tools/pipeline/llm_first_dual_judge_and_arbitrate.py `
  --export <phase8_export_jsonl> `
  --raw <raw_jsonl> `
  --evidence <evidence_jsonl> `
  --governance <governance_jsonl> `
  --limit 2 `
  --parallel 1 `
  --judge-input-mode full_audit
```

用途：验证 compact 裁判与 full audit 裁判分歧是否可接受。

## 8. 预期收益

当前实际：

```text
8 samples Phase 9: 524.547s
max single sample: 402.236s
arbiter input: ~33k chars
```

改造后目标：

```text
Judge input: 2k-4k chars
Arbiter input: 4k-7k chars
8 samples Phase 9: <= 240s
max single sample: <= 120s
fallback long-tail: controlled
```

更重要的是：

- Wiki 治理能力不丢。
- 批量裁判不再重复消化 Wiki 审计材料。
- 最终 CSV 更干净。
- 审计 JSONL 仍可追溯。
- 生产链路更可用。

## 9. 实施顺序

建议按以下顺序实施，避免一次大改不可控：

1. Phase 5/6/6b/8 增加 `compact_governance_summary`。
2. 新增 `llm_first_compact_judge_prompts.py`。
3. `llm_first_dual_judge_and_arbitrate.py` 增加 `--judge-input-mode compact|full_audit`。
4. compact 模式接入 A/B judge 和 arbiter。
5. 主 runner 默认使用 compact。
6. 加测试。
7. 跑 8 条真实链路验收。
8. 再跑 20 条真实链路。

## 10. 成功标准

本次改造完成后，必须满足：

```text
1. Phase 2-8 仍完整使用 Wiki 做事实治理。
2. Phase 9 默认不再传完整 Wiki anchors 和审计 lineage。
3. 最终 CSV 只含样本本体和质量评分结果。
4. 8 条真实链路 Phase 9 不再超过 240s。
5. 单条语义评审不再出现 400s 级长尾。
6. fallback 到非白名单模型次数为 0。
7. 所有 llm-first 关键测试通过。
```

