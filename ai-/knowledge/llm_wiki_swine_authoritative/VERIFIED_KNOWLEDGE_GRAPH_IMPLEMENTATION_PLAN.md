# Verified Knowledge Graph Implementation Plan

本文档用于指导 GPT 或工程执行者分阶段完善当前猪病 LLM Wiki 知识图谱。目标不是把所有 wiki 文本强行连成语义边，而是在保留全文覆盖率的同时，建立可审计、可回溯、可逐步扩展的 evidence-first verified fact graph。

## 0. 总原则

当前主图谱 `wiki/graph-data.json` 是 runtime provenance graph，主要表达：

- runtime 页面挂靠哪些 source；
- runtime 页面受哪些 rule card 约束；
- valid/source_anchored fact 挂靠哪些 source；
- 少量 fact 挂回对应页面。

新方案保留现有主图谱，不直接替换。新增并行图谱层：

| 层级 | 文件 | 作用 | 是否可用于正式生成 |
|---|---|---|---|
| runtime provenance graph | `wiki/graph-data.json` | 页面、source、rule、fact 锚点 | 可用于来源路由和规则门禁 |
| verified fact relations | `exports/verified_fact_relations.jsonl` | 可验证语义事实真源 | 可用于高可信语义关系 |
| rejected/candidate relations | `exports/candidate_fact_relations_rejected.jsonl` | 证据不足或字段不足的候选关系 | 不可直接用于正式回答 |
| verified fact graph | `wiki/verified-fact-graph.json` | fact-centered 语义图 | 可用于检索增强和审计 |
| semantic projection graph | `wiki/semantic-projection-graph.json` | 从 fact 派生的实体-实体展示图 | 仅作为派生视图 |

硬规则：

1. GPT 不得直接创建 runtime 实体-实体语义边。
2. 任何语义关系必须先进入 `verified_fact_relations.jsonl`。
3. 任何 projection edge 必须带 `derived_from_fact_id` 和 `projection_only=true`。
4. 不满足证据要求的关系只能进入 rejected/candidate 文件。
5. 高风险关系必须满足更高 authority 和 rule card 门禁。

## 1. 目标数据模型

### 1.1 Verified Fact Relation

每行 JSONL 记录一个被验证的语义事实关系：

```json
{
  "fact_id": "FACT-DIS-024-CLINICAL-001",
  "source_fact_id": "DIS-024-existing-fact-id",
  "subject_id": "DIS-024",
  "subject_type": "disease",
  "predicate": "HAS_CLINICAL_SIGN",
  "object_id": "clinical_sign:fever",
  "object_text": "fever",
  "object_type": "clinical_sign",
  "polarity": "positive",
  "scope": {
    "species": "swine",
    "stage": "all_stages",
    "jurisdiction": "Global"
  },
  "source_id": "SRC-0046",
  "evidence_locator": "Chapter 42; PDF page 612",
  "evidence_quote": "short source text that directly supports the relation",
  "evidence_hash": "sha256-of-evidence-quote",
  "span_check_status": "full_verified",
  "source_status": "source_anchored",
  "fact_validity": "valid",
  "authority_level": "SRC",
  "risk_class": "diagnostic",
  "task_use_status": "train_ready",
  "rule_card_ids": ["RC-CITATION-001"],
  "review_status": "machine_verified"
}
```

允许的 `span_check_status`：

- `full_verified`: `evidence_quote` 能在登记来源文本中匹配。
- `locator_verified`: 有 source、章节/页码/表格定位，但暂时不能逐字匹配 quote。
- `candidate_only`: 不允许进入 verified 文件，只能进入 rejected/candidate。

### 1.2 Rejected Candidate Relation

无法通过验证的候选关系写入：

`exports/candidate_fact_relations_rejected.jsonl`

字段应包含：

```json
{
  "source_fact_id": "APP-008-clinical",
  "candidate_predicate": "HAS_CLINICAL_SIGN",
  "candidate_subject": "DIS-035",
  "candidate_object_text": "fever",
  "source_id": "SRC-0058",
  "rejected_reason": "missing_subject_id_or_evidence_quote",
  "required_fix": "map subject_id and add evidence quote from source span"
}
```

## 2. 关系本体

新增：

`config/relation_ontology.json`

第一版只覆盖高价值关系，宁可少而准：

```json
{
  "HAS_PATHOGEN": {
    "subject_types": ["disease"],
    "object_types": ["pathogen"],
    "required_fields": ["fact_id", "subject_id", "object_id", "source_id", "evidence_locator"],
    "required_rule_cards": ["RC-CITATION-001"],
    "min_authority_level": "SRC",
    "allowed_risk_classes": ["diagnostic", "normal_clinical", "high_regulatory"]
  },
  "HAS_CLINICAL_SIGN": {
    "subject_types": ["disease"],
    "object_types": ["clinical_sign"],
    "required_fields": ["fact_id", "subject_id", "object_text", "source_id", "evidence_locator"],
    "required_rule_cards": ["RC-CITATION-001"],
    "min_authority_level": "SRC",
    "allowed_risk_classes": ["diagnostic", "normal_clinical"]
  },
  "HAS_DIAGNOSTIC_METHOD": {
    "subject_types": ["disease"],
    "object_types": ["diagnostic_method"],
    "required_fields": ["fact_id", "subject_id", "object_text", "source_id", "evidence_locator"],
    "required_rule_cards": ["RC-CITATION-001"],
    "min_authority_level": "SRC",
    "allowed_risk_classes": ["diagnostic", "high_regulatory"]
  },
  "DIFFERENTIAL_DIAGNOSIS": {
    "subject_types": ["disease", "syndrome"],
    "object_types": ["disease"],
    "required_fields": ["fact_id", "subject_id", "object_id", "source_id", "evidence_locator"],
    "required_rule_cards": ["RC-CITATION-001"],
    "min_authority_level": "SRC",
    "allowed_risk_classes": ["diagnostic", "high_regulatory"]
  },
  "HAS_CONTROL_MEASURE": {
    "subject_types": ["disease"],
    "object_types": ["control_measure"],
    "required_fields": ["fact_id", "subject_id", "object_text", "source_id", "evidence_locator"],
    "required_rule_cards": ["RC-CITATION-001"],
    "min_authority_level": "SRC",
    "allowed_risk_classes": ["normal_clinical", "high_regulatory", "food_safety"]
  },
  "HAS_DRUG_BOUNDARY": {
    "subject_types": ["disease", "drug"],
    "object_types": ["drug_boundary", "treatment_boundary"],
    "required_fields": ["fact_id", "subject_id", "object_text", "source_id", "evidence_locator"],
    "required_rule_cards": ["RC-CITATION-001", "RC-DRUG-001"],
    "min_authority_level": "SRC",
    "allowed_risk_classes": ["drug_boundary", "high_regulatory"]
  },
  "HAS_WITHDRAWAL_PERIOD": {
    "subject_types": ["drug"],
    "object_types": ["withdrawal_period"],
    "required_fields": ["fact_id", "subject_id", "object_text", "source_id", "evidence_locator", "scope"],
    "required_rule_cards": ["RC-WITHDRAWAL-MRL-001"],
    "min_authority_level": "A0",
    "allowed_risk_classes": ["withdrawal_mrl_residue", "food_safety"]
  },
  "REGULATED_BY": {
    "subject_types": ["disease", "drug"],
    "object_types": ["regulation", "standard"],
    "required_fields": ["fact_id", "subject_id", "object_text", "source_id", "evidence_locator", "scope"],
    "required_rule_cards": ["RC-REGULATORY-CURRENT-001"],
    "min_authority_level": "A0",
    "allowed_risk_classes": ["high_regulatory", "food_safety", "withdrawal_mrl_residue"]
  }
}
```

## 3. 分阶段执行计划

### Phase 1: 基线冻结与目录准备

目标：不破坏现有图谱，建立新增文件和报告位置。

执行：

1. 确认现有文件存在：
   - `exports/runtime_core_manifest.json`
   - `exports/knowledge_facts_status_index.json`
   - `wiki/graph-data.json`
2. 新建目录：
   - `config/`
3. 新建 relation ontology。
4. 生成基线报告：
   - `issues/verified_fact_graph_phase1_baseline.md`

验收：

- 现有 `wiki/graph-data.json` 未被修改。
- `config/relation_ontology.json` 存在且 JSON 可解析。
- 基线报告包含当前 runtime entries、fact 数、link type 统计。

失败处理：

- 如果任一输入文件缺失，停止执行，不进入 Phase 2。

### Phase 2: 候选关系抽取

目标：从现有 `knowledge_facts_status_index.json` 生成候选关系，不直接进入 verified。

新增脚本：

`tools/extract_candidate_fact_relations.py`

输入：

- `exports/knowledge_facts_status_index.json`
- `exports/runtime_core_manifest.json`
- `config/relation_ontology.json`

输出：

- `exports/candidate_fact_relations.jsonl`
- `exports/candidate_fact_relations_rejected.jsonl`
- `issues/candidate_fact_relations_extraction_report.md`

候选筛选条件：

1. `fact_validity == "valid"`
2. `source_status == "source_anchored"`
3. 有 `evidence_source_id` 或 `source_id`
4. 有可映射的 `predicate`

第一版 predicate 映射采用保守规则：

| 原始字段特征 | 候选 predicate |
|---|---|
| `fact_type` 或 `predicate` 包含 `clinical`、`sign`、`fever`、`diarrhea`、`respiratory` | `HAS_CLINICAL_SIGN` |
| 包含 `diagnos`、`pcr`、`serology`、`isolation` | `HAS_DIAGNOSTIC_METHOD` |
| 包含 `differential`、`confused_with` | `DIFFERENTIAL_DIAGNOSIS` |
| 包含 `control`、`biosecurity`、`disinfection`、`vaccin` | `HAS_CONTROL_MEASURE` |
| 包含 `treatment_boundary`、`drug_boundary`、`antimicrobial` | `HAS_DRUG_BOUNDARY` |
| 包含 `withdrawal`、`mrl`、`residue` | `HAS_WITHDRAWAL_PERIOD` |
| 包含 `regulatory`、`regulated`、`standard` | `REGULATED_BY` |

拒绝条件：

- 无法映射 predicate；
- 无法确定 subject_id；
- 无 source_id；
- 无 evidence locator；
- 高风险关系 authority 不足；
- object 为空。

验收：

- 所有候选和拒绝项都有 `source_fact_id`。
- 拒绝项必须有 `rejected_reason`。
- Phase 2 不写入 `verified_fact_relations.jsonl`。

### Phase 3: 证据与本体验证

目标：把候选关系提升为 verified 或明确拒绝。

新增脚本：

- `tools/audit_relation_ontology.py`
- `tools/audit_fact_evidence_span.py`
- `tools/promote_verified_fact_relations.py`

输入：

- `exports/candidate_fact_relations.jsonl`
- `config/relation_ontology.json`

输出：

- `exports/verified_fact_relations.jsonl`
- `exports/candidate_fact_relations_rejected.jsonl`
- `issues/relation_ontology_audit_report.md`
- `issues/fact_evidence_span_audit_report.md`

验证规则：

1. predicate 必须在 ontology 中。
2. `subject_type` 必须在允许范围。
3. `object_type` 必须在允许范围。
4. required fields 必须非空。
5. required rule cards 必须存在。
6. risk class 必须允许。
7. authority 必须满足最低要求。
8. `evidence_locator` 必须非空。
9. 如果能访问原始来源文本，则 `evidence_quote` 必须能匹配原文；否则只允许标记 `locator_verified`。

提升规则：

- `full_verified` 和 `locator_verified` 可进入 `verified_fact_relations.jsonl`。
- 高风险关系必须 `full_verified`，否则拒绝。
- `candidate_only` 不得进入 verified。

验收：

- verified 文件中无空 `fact_id`、`source_id`、`predicate`、`subject_id`。
- 所有 verified relation 均通过 ontology audit。
- 高风险 verified relation 必须具备 required rule cards。

### Phase 4: 构建 verified fact graph

目标：从 verified facts 构建 fact-centered 图。

新增脚本：

`tools/build_verified_fact_graph.py`

输入：

- `exports/verified_fact_relations.jsonl`

输出：

- `wiki/verified-fact-graph.json`
- `wiki/verified-fact-graph.md`
- `issues/verified_fact_graph_build_report.md`

节点类型：

- `entity`
- `fact`
- `source`
- `rule_card`

边类型：

```text
subject_to_fact
fact_to_object
fact_to_source
fact_to_rule_card
```

示例：

```json
{
  "source": "entity:disease:DIS-024",
  "target": "fact:FACT-DIS-024-CLINICAL-001",
  "type": "subject_to_fact",
  "fact_id": "FACT-DIS-024-CLINICAL-001"
}
```

验收：

- 每个 fact 节点至少有：
  - 1 条 `subject_to_fact`
  - 1 条 `fact_to_object`
  - 1 条 `fact_to_source`
- 有 required rule cards 的 fact 必须有 `fact_to_rule_card`。
- 不允许直接 `entity -> entity` 语义边。

### Phase 5: 构建 semantic projection graph

目标：从 verified fact graph 派生实体-实体展示图。

新增脚本：

`tools/build_semantic_projection_graph.py`

输入：

- `exports/verified_fact_relations.jsonl`

输出：

- `wiki/semantic-projection-graph.json`
- `wiki/semantic-projection-graph.md`
- `issues/semantic_projection_graph_build_report.md`

projection edge 示例：

```json
{
  "source": "entity:disease:DIS-024",
  "target": "entity:clinical_sign:fever",
  "type": "HAS_CLINICAL_SIGN",
  "derived_from_fact_id": "FACT-DIS-024-CLINICAL-001",
  "projection_only": true,
  "confidence_layer": "full_verified",
  "source_id": "SRC-0046",
  "risk_class": "diagnostic"
}
```

验收：

- 所有 projection edge 必须有 `derived_from_fact_id`。
- 所有 projection edge 必须有 `projection_only=true`。
- 所有 `derived_from_fact_id` 必须存在于 verified facts。
- 不允许 projection 反向写入 `wiki/graph-data.json`。

### Phase 6: 总审计与 readiness report

目标：给出是否可合入运行流程的明确判断。

新增脚本：

`tools/audit_verified_fact_graph.py`

输出：

- `issues/verified_fact_graph_readiness_report.md`
- `issues/verified_fact_graph_readiness_report.json`

必须检查：

1. verified facts 总数。
2. rejected candidates 总数。
3. 各 predicate 数量。
4. 各 `span_check_status` 数量。
5. 高风险 facts 是否全部 full verified。
6. 是否存在缺失 source/rule/fact_id 的边。
7. projection 是否全部可追溯到 verified fact。
8. 是否存在直接实体-实体 runtime 边。

readiness 判定：

- `ready_for_parallel_runtime`: 可并行进入检索增强，但不替换现有主图。
- `needs_more_evidence`: verified 数量不足或 locator_only 比例过高。
- `blocked`: 高风险关系存在验证失败或 projection 不可追溯。

## 4. GPT 执行指令模板

后续可直接把下面指令交给 GPT 执行：

```text
请在 D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative 中按 VERIFIED_KNOWLEDGE_GRAPH_IMPLEMENTATION_PLAN.md 执行下一阶段。

执行约束：
1. 不要修改 wiki/graph-data.json，除非计划文档明确要求。
2. 不要创建直接 runtime 实体-实体语义边。
3. 所有语义关系必须先进入 candidate，再通过 ontology/evidence audit 后进入 verified。
4. 无法验证的关系写入 candidate_fact_relations_rejected.jsonl，并说明 rejected_reason。
5. 每完成一个 Phase，生成对应 issues 报告。
6. 如果审计失败，停止进入下一阶段并报告失败原因。
```

## 5. 有效性保障

本方案用五道门保证有效性：

1. 字段门：没有 fact/source/evidence/risk/rule 字段，不入 verified。
2. 本体门：predicate、subject_type、object_type 必须匹配 ontology。
3. 证据门：必须有 evidence locator；高风险必须 full verified。
4. 派生门：实体-实体边只能从 verified facts 派生。
5. 变更门：所有新增图谱并行输出，主图不被直接污染。

## 6. 覆盖率策略

未进入 verified graph 的 wiki 内容仍然可用：

- 继续保留在 wiki 全文检索中；
- 继续保留在 runtime provenance graph 中；
- 可进入 candidate graph 用于缺口发现；
- 回答时必须按验证等级保守表达。

推荐使用等级：

| 等级 | 可用方式 |
|---|---|
| `full_verified` | 可用于正式语义推理和生成 |
| `locator_verified` | 可用于检索增强，回答时需保守引用 |
| `candidate_only` | 仅用于提示复核和补证，不用于正式回答 |

## 7. 最小可行交付

第一轮实施不追求覆盖全部 wiki。最小可行目标：

- 建立 ontology；
- 从现有 fact 中抽取并验证 50 到 100 条低风险关系；
- 构建 verified fact graph；
- 构建 projection graph；
- 生成 readiness report；
- 保持现有主图谱不变。

当第一轮审计通过后，再按疾病类别、药物类别、监管类别分批扩大覆盖。
