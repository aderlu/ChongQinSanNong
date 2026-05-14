# 严格关系边验证方案文档新增记录

时间：2026-05-12

## 一、修改前存在的问题

当前 wiki-native 知识图谱已经能够保证语义边具备形式化证据链，例如 `evidence_unit_id/source_id/anchor/evidence_text/supporting_span`。但是这只能证明边不是完全凭空生成，不能完全证明节点之间的关系符合医学事实。

主要缺口包括：

1. 没有逐条回查 source 原文。
2. 没有验证 anchor 是否能定位。
3. 没有验证 evidence_text 是否被 source 原文支持。
4. 没有验证 subject/object 是否都被证据明确落地。
5. 没有验证 predicate 是否被医学语义蕴含。
6. 高风险边没有真正的 second validator。
7. supporting_span 多数仍是整条 evidence_text，不是最小支持片段。

## 二、本次新增内容

新增文档：

- `WIKI_KG_STRICT_RELATION_VALIDATION_PLAN.md`

文档提出六级关系边准入管线：

```text
candidate
  -> schema_validated
  -> provenance_validated
  -> source_aligned
  -> endpoint_grounded
  -> medically_entailed
  -> verified
```

并明确最终 verified 边必须满足：

```text
schema_validation=pass
provenance_validation=pass
source_alignment_status=pass
endpoint_grounding_status=pass
medical_entailment=supported
evidence_support_check=pass
validation_status=accepted
```

高风险边还必须满足：

```text
required_rule_card_check=pass
second_validator=pass
jurisdiction_scope_checked=true
negative_or_boundary_handled=true
```

## 三、每部分解决的问题

1. Schema Validation：解决边类型非法、端点类型非法、字段缺失问题。
2. Provenance Validation：解决无 source、无 anchor、无 evidence_text 的幻觉边问题。
3. Source Alignment Check：解决 source_id 存在但 source 原文不支持的问题。
4. Endpoint Grounding Check：解决同页多实体共现导致交叉乱连的问题。
5. Predicate Medical Entailment Check：解决章节标题误推、文本共现误连、否定/禁用误判为正向关系的问题。
6. High-Risk Second Validator：解决药物、处方、MRL、监管、鉴别诊断等高风险边错误进入训练正例的问题。
7. Expert Review Queue：解决规则和模型都无法确定的问题，防止不确定关系被强行 verified。

## 四、无法仅靠规则和代码解决的问题

文档明确列出必须补充数据或人工/专家复核的问题：

- source 原文缺失。
- anchor 不可定位。
- 疾病别名或药物别名缺失。
- 具体产品标签缺失。
- 法域上下文缺失。
- 不同权威来源冲突。
- 医学语义存在争议。

这些情况不能通过修改规则直接变成 verified，只能进入 candidate、source_text_backfill_queue 或 expert_review_queue。

## 五、预期效果

该方案实施后，知识图谱关系边会从“有形式证据链”升级为“source 原文对齐 + 端点落地 + 医学蕴含成立 + 高风险二次验证”。

预期能最大程度防止：

- 同页共现乱连。
- 章节标题误推。
- LLM 幻觉生成关系。
- 权威文本被错误抽象成错误关系。
- 药物/监管/鉴别等高风险边直接进入黄金数据集。

## 六、验证

已执行编码审计：

```powershell
py tools/audit_encoding_integrity.py
```

结果：

- `mojibake_like_content=0`
- `runtime_damaged_count=0`

未引入新的乱码问题。
