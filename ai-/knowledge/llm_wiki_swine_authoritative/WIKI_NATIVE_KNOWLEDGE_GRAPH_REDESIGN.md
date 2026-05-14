# Wiki-Native Knowledge Graph Redesign

本文档定义一套从当前 wiki 数据重新设计知识图谱的规则，并同步记录当前已经落地的 MVP 实现边界。它不以现有 `wiki/graph-data.json` 的 page/source/rule/fact 锚点规则为基础继续叠加，而是把当前 wiki 的真实内容结构作为图谱源头，重新构建一个 wiki-native knowledge graph。

目标：

- 减少历史规则叠加造成的冗余。
- 让疾病、药物、综合页、症候群、比较页、来源页、规则卡都自然体现在图谱中。
- 明确区分结构关系、证据关系、语义事实关系、候选关系。
- 所有高风险语义边必须能追溯到 `fact_id + source_id + anchor`，并且必须明确区分“当前代码已完成的证据链形式校验”和“下一阶段需要补强的 source 原文一致性/医学蕴含校验”。
- 完整解决关系边幻觉：LLM 只能提出关系边提案，验证器通过后才允许标记为 `status=verified`。
- 每次更新都必须产出统一图谱和 build/audit report，记录新增节点、新增边、候选边、拒绝边和失败原因，确保可判断、可回滚、可追溯。

参考吸收：

- Karpathy LLM Wiki: raw sources 不可变、wiki 是维护层、schema 是约束层、log 追加记录。
- Understand-Anything: 先确定性扫描，再合并、去重、端点校验、结构审计。
- WeKnora: 可配置 schema、图检索/Neo4j 形态、ingest/operation 可观测性。
- claude-obsidian: raw/wiki/log/hot/lint 分层，更新过程追加式记录。
- llm-wiki-agent: wikilink 确定性边与 LLM inferred/ambiguous 边分离。

## 0. 落地版目标与取舍

本方案优先采用 MVP 落地模式，而不是一次实现完整重型图谱平台。目标是在当前 wiki 数据基础上，快速构建一个可用于猪病黄金数据集生成、微调和评估的高可信图谱。

第一阶段只保留四个必要组件：

```text
1. wiki evidence unit extractor
2. predicate registry
3. edge validator
4. build/audit report
```

这里的“轻量”只表示实现形态轻量，不表示验证标准降低。第一阶段可以少拆文件、少做平台化、少做图数据库，但不能减少 verified 边的证据门槛。

不可降级的正确性底线：

```text
1. 语义边先 proposal，后 validation，不能在生成阶段直接 verified。
2. 所有 verified semantic edge 必须通过 evidence_support_check。
3. 所有 verified semantic edge 必须能反查 evidence_unit_id、source_id、anchor、evidence_text、supporting_span。
4. 所有 high_risk predicate 在当前 MVP 中必须通过 rule_card_check；`second_validator` 当前以 `pass_rule_card_gated` 形式记录，真正的 source 原文一致性和医学蕴含复核属于下一阶段增强项。
5. 普通 predicate 如果 evidence_text 不直接支持 subject-predicate-object，也只能 candidate。
```

第一阶段只输出三个核心产物：

```text
wiki/wiki-native-graph.json
issues/wiki_native_graph_build_report.json
issues/wiki_native_graph_build_report.md
```

`wiki-native-graph.json` 中同时保存节点、verified edges、candidate edges 和 rejected edges，通过 `status` 字段区分：

```text
verified   可用于黄金数据集正例、SFT 事实支撑、评估标准答案
candidate  可用于缺口发现、人工复核、负例/陷阱候选，不可作为正例事实
rejected   可用于负例、反幻觉训练、禁止连接记录
```

完整模式中的独立 candidate graph、rejected graph、diff report、failed operations 可在第二阶段拆分；第一阶段可以合并到 build report 中，避免流程过重。

核心取舍：

| 目标 | 第一阶段做法 |
|---|---|
| 减少幻觉 | verified 边必须有 evidence unit 和 validation |
| 覆盖全面 | 所有 wiki 页面都建节点，所有可识别证据都进入 graph |
| 不浪费数据 | 证据不足的关系进入 candidate，不丢弃 |
| 可用于黄金数据集 | verified 用正例，candidate/rejected 用困难负例和边界题 |
| 实现可行 | 一个主构建脚本、一个 registry、一个 graph、一个 report |

一句话原则：

```text
图谱可以包含候选和拒绝信息，但只有 verified 边能作为事实真源。
```

### 0.1 当前实际实现边界

截至当前 MVP，核心实现文件为：

```text
tools/build_wiki_native_graph_mvp.py
tools/render_wiki_native_graph.py
config/wiki_native_predicate_registry.json
wiki/wiki-native-graph.json
issues/wiki_native_graph_build_report.json
issues/wiki_native_graph_build_report.md
```

当前代码已经实际完成：

1. 从 `wiki/diseases`、`wiki/drugs`、`wiki/comparisons`、`wiki/syndromes`、`wiki/rule_cards`、`wiki/rules`、`wiki/synthesis`、`wiki/sources`、`wiki/topics` 扫描页面节点。
2. 从 Markdown 标题抽取 `section` 节点，并保留 `line_start/line_end`。
3. 从正文中解析 `fact_id/source_id/anchor`，形成 `evidence_unit`。
4. 依据 `section_title + predicate registry` 生成语义边 proposal。
5. 所有语义边先以 `candidate` 创建，再经过 `validate_semantic_edge` 升级或降级。
6. `verified` 语义边必须具备 `evidence_unit_id/source_id/anchor/evidence_text/supporting_span`，且 `supporting_span` 必须出现在 `evidence_text` 中。
7. 高风险 predicate 必须绑定对应 rule card，例如 `HAS_DRUG_BOUNDARY` 要求 `RC-DRUG-001`。
8. `candidate/rejected` 边默认 `blocked_from_runtime=true`、`gold_dataset_ready=false`，不能作为黄金数据集正例。
9. 最终 `audit_graph` 会检查 verified 边是否缺少必要字段，防止不合格边混入可用正例。
10. HTML 主图采用 `section_group` 投影，完整审计图保留原始 section；主图搜索时通过 `full_index` 展开任意节点的全量关系。

当前代码尚未完全完成：

1. 未逐条回查 source 原始页面或 PDF 原文，确认 `anchor` 位置是否能直接支持该 `evidence_text`。
2. 未实现独立医学蕴含模型来判断“证据文本是否医学上支持该 predicate”。
3. 未把 `supporting_span` 精确裁剪到最小支持短语；当前 MVP 多数情况下使用整条 `evidence_text` 作为 `supporting_span`。
4. 未对“处方-用药”“药物标签”“休药期/MRL”“监管执行”等高风险关系做完整的 source alignment + medical entailment 双重验证。

因此，当前 `verified` 的严格含义是：

```text
通过当前代码定义的证据链形式校验、端点校验、rule card 校验和 evidence_support_check。
```

当前 `verified` 还不能被解释为：

```text
已经由 source 原文逐字定位和医学专家级蕴含验证确认绝对正确。
```

对于黄金数据集，当前 MVP 可以先读取 `verified` 边生成候选正例，但药物、处方、标签、MRL、监管等高风险样本在进入最终训练集前，必须再经过 source alignment 和 medical entailment 复核。

## 1. 设计原则

### 1.1 当前旧图不再作为核心模型

旧图谱 `wiki/graph-data.json` 只保留为兼容层，命名为 legacy runtime graph。新的主图谱由 wiki 页面重新扫描构建：

```text
wiki/*.md
  -> frontmatter parser
  -> section parser
  -> inline fact anchor parser
  -> wikilink/source/rule parser
  -> evidence expansion parser
  -> normalized graph
```

### 1.2 wiki 页面就是图谱源头

节点和边不再优先来自 `runtime_core_manifest.json`，而是来自 wiki 目录和页面结构：

| wiki 位置 | 节点类型 |
|---|---|
| `wiki/diseases/*.md` | `disease` |
| `wiki/drugs/*.md` | `drug` |
| `wiki/syndromes/*.md` | `syndrome` |
| `wiki/comparisons/*.md` | `comparison` |
| `wiki/synthesis/*.md` | `synthesis` |
| `wiki/sources/*.md` | `source` |
| `wiki/rule_cards/*.md` | `rule_card` |
| `wiki/topics/*.md` | `topic` |
| `wiki/evidence_expansions/**/*.md` | `evidence_expansion` |

### 1.3 边分四类，不混用

| 边层级 | 作用 | 是否要求证据 |
|---|---|---|
| `structural` | 页面属于目录、页面引用来源、页面包含章节 | 不要求 |
| `governance` | 页面受 rule card 约束 | 不要求原文证据，但要求规则来源明确 |
| `evidence` | fact/source/anchor 证据链 | 要求 `fact_id/source_id/anchor` |
| `semantic` | 疾病-症状、疾病-诊断、药物-边界等事实关系 | 必须由 evidence 边支撑 |

### 1.4 不再把所有内容强制验证后才入图

新图允许不同置信层级共存，但必须清楚标记：

```text
verified     有 fact_id + source_id + anchor
anchored     有 source_id + anchor，但 fact_id 不完整
page_claim   来源页面声明或页面结构声明
candidate    GPT/规则候选，不能用于正式回答
rejected     已确认不成立或验证失败，只进入审计记录
```

高风险关系只能使用 `verified`。

### 1.5 关系边状态机

所有新语义边默认都是 `candidate`，不得直接进入主图。

```text
candidate
  -> accepted / verified
  -> candidate with reason
  -> rejected
```

状态含义：

| 状态 | 含义 | 是否可作为 verified 事实边使用 |
|---|---|---|
| `candidate` | 新提案，未完成验证 | 否 |
| `accepted` / `verified` | 通过 schema、端点、证据、蕴含和一致性验证 | 是 |
| `rejected` | 明确不被证据支持或违反本体规则 | 否 |

硬规则：

```text
不确定不是低置信 accepted，而是 candidate，并写明 reason。
证据不足不是弱关系，而是未获准关系。
LLM 常识不能把 candidate 升级为 verified。
```

## 2. 新图谱文件

第一阶段新图谱不要覆盖旧图，先并行输出一个统一图谱文件：

```text
wiki/wiki-native-graph.json
issues/wiki_native_graph_build_report.md
issues/wiki_native_graph_build_report.json
```

旧图：

```text
wiki/graph-data.json
```

保留但降级为：

```text
legacy_runtime_graph
```

第一阶段不强制拆分多个图文件，而是在统一图中按 `status` 区分：

| status | 含义 | 可否用于黄金数据集 |
|---|---|---|
| `verified` | 证据单元和规则校验通过 | 可用于正例、标准答案、SFT 支撑 |
| `candidate` | 有线索但证据不完整或关系不够明确 | 不可作正例，可用于复核队列、缺口发现 |
| `rejected` | 证据不支持、规则不允许、端点不合法 | 可用于负例和反幻觉训练 |

如后续规模变大，可在第二阶段拆出：

```text
wiki/wiki-native-semantic-graph.json
wiki/wiki-native-candidate-graph.json
wiki/wiki-native-rejected-graph.json
issues/wiki_native_graph_diff_report.md
issues/wiki_native_graph_failed_operations.jsonl
```

正式问答、SFT 正例和黄金数据集标准答案只能读取 `status=verified` 的边。

### 2.1 统一图谱结构

`wiki/wiki-native-graph.json` 第一阶段结构：

```json
{
  "metadata": {
    "graph_kind": "wiki_native_mvp",
    "generated_at": "...",
    "source": "wiki markdown",
    "runtime_compat": "legacy graph-data.json unchanged"
  },
  "nodes": [],
  "edges": [],
  "evidence_units": [],
  "validation_summary": {},
  "gold_dataset_readiness": {}
}
```

其中：

- `nodes`: 全量页面节点、section 节点、source/rule/fact/object 节点。
- `edges`: structural、evidence、semantic、governance 边，均带 `status`。
- `evidence_units`: 页面内可定位证据单元。
- `validation_summary`: 校验统计。
- `gold_dataset_readiness`: 可用于黄金数据集的覆盖率和风险统计。

## 3. 节点设计

### 3.1 Page Node

每个 wiki 页面生成一个 page/entity node：

```json
{
  "id": "disease:DIS-024",
  "type": "disease",
  "label": "Classical Swine Fever",
  "path": "wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md",
  "frontmatter": {
    "disease_id": "DIS-024",
    "sources": ["SRC-0046", "RC-DRUG-001"]
  },
  "status": {
    "source_status": "",
    "fact_validity": "",
    "task_use_status": "",
    "risk_class": ""
  }
}
```

ID 规则：

| 页面类型 | ID 来源 |
|---|---|
| disease | frontmatter `disease_id`，否则文件名前缀 `DIS-xxx` |
| drug | frontmatter `drug_id`，否则文件名前缀 `DRUG-xxx` |
| rule_card | frontmatter `card_id`，否则文件名前缀 `RC-xxx` |
| source | frontmatter `source_id`，否则文件名前缀 |
| syndrome/comparison/synthesis/topic | 文件名 stem |

### 3.2 Section Node

每个二级/三级标题生成 section node：

```json
{
  "id": "section:disease:DIS-024:clinical-signs",
  "type": "section",
  "section_title": "临床症状",
  "page_id": "disease:DIS-024",
  "line_start": 42,
  "line_end": 51
}
```

Section 不是装饰节点，它用于决定语义 predicate 的候选类型。

### 3.3 Fact Anchor Node

页面中出现以下模式时生成 fact anchor：

```text
fact_id=CSFV-007-clinical-nonspecific; source_id=SRC-0046; anchor=Chapter 39 Pestiviruses; PDF page 649-651
```

生成：

```json
{
  "id": "fact:CSFV-007-clinical-nonspecific",
  "type": "fact",
  "source_id": "SRC-0046",
  "anchor": "Chapter 39 Pestiviruses; PDF page 649-651",
  "text": "该 bullet 或段落的正文",
  "page_id": "disease:DIS-024",
  "section_id": "section:disease:DIS-024:clinical-signs",
  "confidence_layer": "verified"
}
```

如果只有 `source_id + anchor`，没有 `fact_id`，生成 `evidence_anchor`，置信层为 `anchored`。

### 3.4 Evidence Expansion Node

`wiki/evidence_expansions/**/*.md` 生成 evidence expansion node，并通过路径挂回原实体页：

```json
{
  "id": "evidence_expansion:disease:DIS-024:005-Formal-Batch-019",
  "type": "evidence_expansion",
  "owner_page_id": "disease:DIS-024",
  "path": "wiki/evidence_expansions/diseases/.../005-Formal-Batch-019.md"
}
```

## 4. 边设计

### 4.1 Structural Edges

#### `page_has_section`

来源：Markdown 标题解析。

```text
disease:DIS-024 -> section:disease:DIS-024:clinical-signs
```

用途：支持按章节定位信息。

#### `page_has_source`

来源：frontmatter `sources` 列表。

```text
disease:DIS-024 -> source:SRC-0046
```

注意：这只表示页面声明引用该 source，不表示每条事实都被该 source 支持。

#### `page_has_rule_card`

来源：frontmatter `sources` 中的 `RC-*`、正文中反引号规则卡、rule card 章节。

```text
disease:DIS-024 -> rule_card:RC-DRUG-001
```

#### `page_has_evidence_expansion`

来源：evidence expansion 路径或页面内 evidence expansion index。

```text
disease:DIS-024 -> evidence_expansion:disease:DIS-024:005-Formal-Batch-019
```

### 4.2 Evidence Edges

#### `section_has_fact`

来源：section 内 `fact_id=...`。

```text
section:disease:DIS-024:clinical-signs -> fact:CSFV-007-clinical-nonspecific
```

#### `fact_has_source`

来源：inline `source_id=...`。

```text
fact:CSFV-007-clinical-nonspecific -> source:SRC-0046
```

#### `fact_has_anchor`

来源：inline `anchor=...`。

```text
fact:CSFV-007-clinical-nonspecific -> evidence_anchor:CSFV-007-clinical-nonspecific
```

anchor 可作为 fact 属性，也可建独立节点。第一版建议作为属性，减少节点爆炸；审计需要可视化时再展开为节点。

### 4.3 Semantic Edges

语义边不直接从页面到页面生成，而是从 fact anchor 和 section type 派生。

#### 语义边生成三层

新图谱只允许三类边生成器：

```text
deterministic_edge_builder
  从 frontmatter、wikilink、heading、inline anchor 生成 structural/evidence 边。

anchored_semantic_edge_builder
  只读取 fact anchor 所在 bullet/paragraph，根据 page_type + section_title + predicate registry 生成语义边候选。

implicit_edge_proposer
  只生成 status=candidate 的可能关系，用于人工复核或后续补证；不得直接升级为 status=verified。
```

准入规则：

```text
deterministic structural/evidence edges 可以直接 accepted。
anchored semantic edges 必须经过五级验证。
implicit edges 默认保持 candidate，除非后续绑定 fact_id/source_id/anchor 并重新验证。
```

语义边的 verified 条件必须同时满足：

```text
predicate 来自 registry
subject 节点存在
object 来自 existing node 或 exact_text_span
evidence_unit_id 存在
source_id 和 anchor 存在
evidence_text 中能定位 supporting_span
supporting_span 直接表达该 predicate 的含义
高风险 predicate 通过 rule card 和 second validator
无 verified 冲突边
```

如果只能证明两个概念在同一段出现，但不能证明 predicate 关系成立，必须保持 `status=candidate`。

禁止路径：

```text
page A + page B + LLM 常识
  -> semantic edge
```

允许路径：

```text
fact_id + source_id + anchor + exact_text_span
  -> edge proposal
  -> validator
  -> accepted semantic edge
```

#### 疾病页 predicate 映射

| 章节标题关键词 | predicate | object 来源 |
|---|---|---|
| 病原、分类、pathogen | `HAS_PATHOGEN` | 当前段落或已识别病原实体 |
| 传播 | `HAS_TRANSMISSION_ROUTE` | 当前 bullet 文本 |
| 临床症状 | `HAS_CLINICAL_SIGN` | 当前 bullet 文本 |
| 剖检、病变 | `HAS_LESION` | 当前 bullet 文本 |
| 实验室诊断、诊断 | `HAS_DIAGNOSTIC_METHOD` | 当前 bullet 文本 |
| 鉴别诊断 | `DIFFERENTIAL_DIAGNOSIS` | 链接疾病或当前文本 |
| 防控、控制 | `HAS_CONTROL_MEASURE` | 当前 bullet 文本 |
| 监管、处置 | `REGULATED_BY` 或 `HAS_REGULATORY_BOUNDARY` | 当前 bullet 文本 |
| 用药、处方、治疗边界 | `HAS_DRUG_BOUNDARY` | 当前 bullet 文本 |

#### 药物页 predicate 映射

| 章节标题关键词 | predicate |
|---|---|
| 药物类别 | `BELONGS_TO_DRUG_CLASS` |
| 疾病/用途候选 | `HAS_INDICATION_CANDIDATE` |
| 标签/来源使用边界 | `HAS_LABEL_BOUNDARY` |
| 禁用、禁止、不得 | `HAS_PROHIBITION` |
| 休药期、MRL、残留 | `HAS_WITHDRAWAL_OR_MRL_BOUNDARY` |
| 相互作用、配伍、禁忌 | `HAS_CONTRAINDICATION_OR_INTERACTION` |

#### 语义边必须带出处

```json
{
  "source": "disease:DIS-024",
  "target": "semantic_object:clinical_sign:csfv-clinical-nonspecific",
  "type": "HAS_CLINICAL_SIGN",
  "derived_from_fact_id": "CSFV-007-clinical-nonspecific",
  "source_id": "SRC-0046",
  "anchor": "Chapter 39 Pestiviruses; PDF page 649-651",
  "evidence_text": "CSF 临床表现非特异，不能替代实验室确诊。",
  "supporting_span": "临床表现非特异，不能替代实验室确诊",
  "evidence_text_hash": "sha256:...",
  "source_page_path": "wiki/sources/SRC-0046-....md",
  "section_id": "section:disease:DIS-024:clinical-signs",
  "edge_generation_mode": "anchored_semantic_edge_builder",
  "confidence_layer": "verified",
  "validation_status": "accepted",
  "blocked_from_runtime": false
}
```

如果没有 `fact_id`，语义边只能以 `status=candidate` 保存在统一图谱中：

```json
{
  "confidence_layer": "candidate",
  "blocked_from_runtime": true,
  "reason": "missing_fact_id"
}
```

### 4.4 Predicate Registry

新增硬约束文件：

```text
config/wiki_native_predicate_registry.json
```

每个 predicate 必须注册允许的 subject/object 类型、章节模式、证据要求、风险要求和运行时准入条件。

示例：

```json
{
  "HAS_CLINICAL_SIGN": {
    "allowed_subject_types": ["disease"],
    "allowed_object_types": ["clinical_sign", "literal_span"],
    "allowed_section_patterns": ["临床", "症状", "clinical", "sign"],
    "requires_fact_id": true,
    "requires_source_id": true,
    "requires_anchor": true,
    "requires_evidence_text": true,
    "requires_supporting_span": true,
    "requires_rule_card": false,
    "requires_second_validator": false,
    "high_risk": false,
    "object_must_be_text_span": true,
    "runtime_allowed_confidence": ["verified"]
  },
  "HAS_DRUG_BOUNDARY": {
    "allowed_subject_types": ["disease", "drug"],
    "allowed_object_types": ["drug_boundary", "literal_span"],
    "allowed_section_patterns": ["用药", "处方", "治疗边界", "drug", "treatment"],
    "requires_fact_id": true,
    "requires_source_id": true,
    "requires_anchor": true,
    "requires_evidence_text": true,
    "requires_supporting_span": true,
    "requires_rule_card": true,
    "required_rule_cards": ["RC-DRUG-001"],
    "requires_second_validator": true,
    "high_risk": true,
    "object_must_be_text_span": true,
    "runtime_allowed_confidence": ["verified"]
  }
}
```

规则：

1. predicate 不在 registry 中，候选边必须 rejected。
2. subject/object 类型不匹配，候选边必须 rejected。
3. section title 不匹配 predicate 的 `allowed_section_patterns`，候选边必须保持 candidate 或 rejected。
4. 高风险 predicate 必须有 required rule cards，并通过 second validator。
5. object 若不是已有节点，必须来自 `exact_text_span`，不得由 LLM 凭空标准化。
6. registry 中声明 `requires_supporting_span=true` 的 predicate，缺少 supporting_span 时不得 verified。
7. registry 中声明 `object_must_be_text_span=true` 的 predicate，不允许只使用 LLM 归纳标签作为 object。

第一阶段 predicate registry 只做黄金数据集最需要的关系，不追求全覆盖：

| predicate | 用途 | 黄金数据集角色 |
|---|---|---|
| `HAS_PATHOGEN` | 疾病病原/分类 | 疾病召回、基础问答 |
| `HAS_CLINICAL_SIGN` | 临床表现 | 临床摘要、病例生成 |
| `HAS_TRANSMISSION_ROUTE` | 传播路径 | 流行病学问答 |
| `HAS_DIAGNOSTIC_METHOD` | 检测/诊断方法 | 诊断边界、评估题 |
| `DIFFERENTIAL_DIAGNOSIS` | 鉴别诊断 | case triage、困难负例 |
| `HAS_CONTROL_MEASURE` | 防控措施 | 防控建议、边界题 |
| `HAS_DRUG_BOUNDARY` | 用药边界 | 负例、拒答、越界识别 |
| `HAS_LABEL_BOUNDARY` | 标签/法域边界 | 药物安全、监管边界 |
| `HAS_WITHDRAWAL_OR_MRL_BOUNDARY` | 休药期/MRL/残留边界 | 高风险拒答和规则题 |
| `REGULATORY_BOUNDARY` | 报告、检疫、扑杀、调运等监管边界 | 高风险监管题 |

第一阶段不做过细实体拆分；对象可以先用 `literal_span`，避免强行标准化造成误连。

```text
literal_span 优先，实体标准化后置。
```

这能保证覆盖率，同时减少把不同概念错误合并成同一节点的风险。

### 4.5 Edge Proposal Contract

LLM 只能输出关系边提案，不得直接写入正式图谱。提案格式固定：

```json
{
  "proposal_id": "edge-proposal:<batch_id>:<hash>",
  "subject_id": "disease:DIS-024",
  "predicate": "HAS_CLINICAL_SIGN",
  "object": {
    "mode": "existing_node|new_literal_span",
    "id": "semantic_object:clinical_sign:...",
    "label": "...",
    "exact_text_span": "..."
  },
  "evidence": {
    "fact_id": "CSFV-007-clinical-nonspecific",
    "source_id": "SRC-0046",
    "anchor": "Chapter 39 Pestiviruses; PDF page 649-651",
    "section_id": "section:disease:DIS-024:clinical-signs",
    "quote": "..."
  },
  "reason": "一句话说明为什么该 fact 支持该关系",
  "confidence_layer": "candidate",
  "blocked_from_runtime": true
}
```

硬规则：

1. `subject_id` 必须来自 node registry。
2. `predicate` 必须来自 Predicate Registry。
3. `quote` 必须能在 fact text 中原文匹配。
4. 所有 LLM proposal 初始都是 candidate。
5. validator 通过后才可提升为 verified semantic edge。

第一阶段可不调用 LLM 生成 proposal。优先使用确定性规则：

```text
page_type + section_title + inline fact/source/anchor
  -> candidate edge
  -> validator
  -> verified/candidate/rejected
```

只有以下场景才允许 LLM proposal：

1. comparison 页面中需要识别鉴别诊断方向；
2. syndrome 页面中需要从列表提取候选疾病；
3. drug 页面中需要区分“用途候选”和“可执行处方”；
4. evidence unit 文本较长，需要抽出 object literal span。

即使使用 LLM，输出仍必须是 candidate proposal。

## 5. 新构建流水线

第一阶段只实现一个主脚本：

```text
tools/build_wiki_native_graph_mvp.py
```

该脚本内部完成扫描、证据单元抽取、候选边生成、必要校验和报告输出。文档仍按 Phase A-F 描述职责，但实现上不拆多个脚本，避免落地过重。

### Phase A: Wiki 结构扫描

脚本：

```text
tools/build_wiki_native_graph_mvp.py --phase scan
```

职责：

1. 遍历 `wiki/` 下允许目录。
2. 解析 frontmatter。
3. 根据目录和 ID 字段创建 page nodes。
4. 解析 headings 创建 section nodes。
5. 解析 `sources` 创建 source/rule edges。
6. 解析 evidence expansion index 创建 expansion edges。

输出：

```text
wiki/wiki-native-graph.json
issues/wiki_native_graph_build_report.md
```

### Phase B: Fact Anchor 抽取

脚本：

```text
tools/build_wiki_native_graph_mvp.py --phase evidence
```

职责：

1. 在正文中识别 `fact_id=...; source_id=...; anchor=...`。
2. 将所在 bullet/paragraph 作为 fact text。
3. 挂到当前 page 和 section。
4. 如果 `fact_id/source_id/anchor` 不完整，进入 `candidate_fact_anchor`。

输出：

```text
wiki/wiki-native-graph.json
issues/wiki_native_graph_build_report.json
issues/wiki_native_graph_build_report.md
```

### Phase C: Wiki-Native Semantic Edge Proposal

脚本：

```text
tools/build_wiki_native_graph_mvp.py --phase semantic
```

职责：

1. 读取统一图谱中的 `evidence_units`。
2. 根据 page type + section title 映射 predicate。
3. 生成 semantic object nodes。
4. 生成 `status=candidate` 的 semantic edge proposals。
5. 无法映射 predicate 的 fact 保留为 evidence fact，不生成语义边。

Phase C 不允许直接生成 verified semantic edge。它只能生成候选边，verified 只能由 Phase D validator 写入。

输出：

```text
wiki/wiki-native-graph.json
issues/wiki_native_graph_build_report.json
issues/wiki_native_graph_build_report.md
```

### Phase D: 关系边验证

脚本：

```text
tools/build_wiki_native_graph_mvp.py --phase validate
```

输入：

```text
wiki/wiki-native-graph.json
config/wiki_native_predicate_registry.json
```

第一阶段采用“全量确定性验证 + 高风险 rule card 门控”。完整 LLM entailment validator 和 source 原文一致性复核暂不视为当前 MVP 已完成能力，而是下一阶段必须补强的增强校验。所有语义边当前都必须经过 evidence_support_check：

```text
V1 Schema Validation
  字段完整、JSON 合法、predicate 合法、类型合法。

V2 Endpoint Validation
  source/target 节点存在；新 object 节点必须有 exact_text_span。

V3 Provenance Validation
  当前 MVP 检查 fact_id/source_id/anchor 是否存在，并把它们写入 edge/evidence_unit；
  下一阶段需要继续检查 source page 或 source registry 记录是否存在、anchor 是否可解析、
  evidence_text 是否能被 source 原文支持。

V4 Graph Consistency Validation
  查重、冲突、反向边一致性、高风险 rule card、候选边隔离。

V5 Evidence Support Check
  对每条 semantic edge proposal 检查 evidence_text/supporting_span 是否直接支持该 predicate；
  不允许仅因同段共现、同页共现、标题相近或常识推断而 accepted。
```

当前 MVP 中 V5 的实际实现边界：

```text
已实现：
1. verified 边必须有 evidence_text。
2. verified 边必须有 supporting_span。
3. supporting_span 必须是 evidence_text 的原文子串。
4. object 必须有 exact_text_span。
5. 高风险 predicate 必须有 required rule card。

尚未完全实现：
1. 没有逐条验证 evidence_text 是否来自 source 原文 anchor。
2. 没有独立判断 supporting_span 是否“医学语义上”支持 subject-predicate-object。
3. 没有完整识别处方、禁用、标签外使用、休药期、MRL、监管边界中的否定/限制/冲突关系。
```

验证失败处理：

```text
V1/V2 失败：rejected
V3 失败：candidate，reason=missing_or_unresolvable_provenance
V4 冲突：candidate，reason=conflicts_with_existing_verified_edge
V5 无 supporting_span：candidate
V5 supporting_span 与 predicate 不匹配：rejected 或 candidate
高风险 entailment not_supported：rejected
高风险 entailment ambiguous：candidate
```

Evidence Support Check 是非可选项。它可以先用确定性规则实现，不必一开始接入复杂模型，但必须清楚区分“当前已落地检查”和“后续增强检查”：

```text
1. supporting_span 必须是 evidence_text 的原文子串。
2. object label 或 exact_text_span 必须能在 supporting_span 或同一 evidence unit 中定位。
3. predicate 必须与 section_title 和 predicate registry 的 allowed_section_patterns 匹配。
4. 否定、禁用、疑似、待证实、不能替代确诊等边界词必须触发 predicate 降级或进入 candidate。当前代码只保留了边界词表和高风险门控，尚未完成完整语义降级。
5. 药物、休药期、MRL、监管、处方相关边必须进入 second validator。当前 MVP 中 `second_validator=pass_rule_card_gated` 只表示已通过 rule card 门控，不等同于完整医学复核。
```

Entailment Validator 判断边界：

```text
只能看 subject label、predicate definition、object label/exact_text_span、
evidence_text、source_id、anchor metadata。
不得使用外部常识补全关系。
```

下一阶段 `source_alignment_check` 必须输出：

```json
{
  "edge_id": "...",
  "source_id": "SRC-xxxx",
  "source_node_exists": true,
  "source_page_exists": true,
  "anchor_found_in_source": true,
  "evidence_text_supported_by_source": true,
  "connected_subject_mentioned": true,
  "connected_object_mentioned": true,
  "predicate_semantics_supported": true,
  "negation_or_boundary_detected": false,
  "source_alignment_status": "pass|candidate|rejected"
}
```

对 `HAS_DRUG_BOUNDARY`、`HAS_LABEL_BOUNDARY`、`HAS_WITHDRAWAL_OR_MRL_BOUNDARY`、`REGULATORY_BOUNDARY` 和 `DIFFERENTIAL_DIAGNOSIS`，只有 `source_alignment_status=pass` 且医学蕴含为 `supported`，才能进入最终黄金数据集正例。

输出：

```text
wiki/wiki-native-graph.json
issues/wiki_native_graph_build_report.json
issues/wiki_native_graph_build_report.md
```

验证输出格式：

```json
{
  "edge_id": "...",
  "entailment": "supported|not_supported|ambiguous",
  "supporting_span": "...",
  "failure_reason": "",
  "validation_status": "accepted|candidate|rejected"
}
```

如果 `supporting_span` 为空，不允许 accepted。

### Phase E: Report 与变更账本

脚本：

```text
tools/build_wiki_native_graph_mvp.py --phase report
```

每次构建必须产生 build manifest，并合并写入 build report；第一阶段不强制拆出独立 diff report：

```json
{
  "build_id": "wiki-native-graph:2026-05-12T...",
  "input_snapshot": {
    "wiki_commit": "",
    "source_file_hashes": {},
    "schema_hash": "",
    "predicate_registry_hash": ""
  },
  "outputs": {
    "graph_path": "wiki/wiki-native-graph.json",
    "audit_report": "issues/wiki_native_graph_build_report.md"
  }
}
```

新增节点分为：

```text
accepted_new_nodes
candidate_new_nodes
rejected_new_nodes
```

新增边分为：

```text
accepted_new_edges
candidate_new_edges
rejected_new_edges
deleted_edges
changed_edges
unchanged_edges
```

每条新增语义边必须带审计结论。结构边和证据边只要求 schema、endpoint、provenance 检查通过：

```json
{
  "edge_id": "...",
  "diff_action": "created",
  "decision": "verified|candidate|rejected",
  "validation_summary": {
    "schema": "pass",
    "endpoint": "pass",
    "provenance": "pass",
    "entailment": "supported",
    "graph_consistency": "pass"
  },
  "human_review_required": false
}
```

同时追加写入 `log.md` 或专用变更账本。第一阶段可以把账本摘要合并到 `issues/wiki_native_graph_build_report.md`，后续规模变大后再拆成独立日志：

```text
输入来源
新增节点
新增边
升级边
拒绝边
冲突边
变更原因
校验结果
来源 checksum/hash
```

`log.md` 只能追加，不能改写历史。

失败操作不得静默丢失。任何 LLM proposal 解析失败、validator 崩溃、edge 写入失败，都必须记录。第一阶段可以写入 build report 的 `failed_operations` 字段；第二阶段再拆出：

```text
issues/wiki_native_graph_failed_operations.jsonl
```

构建完成条件不是“脚本跑完”，而是 `failed_operations` 为空，或每条失败都有人工可读 reason。存在失败时，仍可输出图谱，但必须在报告中标记 `build_status=partial`，且失败影响到的边不得标为 `verified`。

### Phase F: 审计

脚本：

```text
tools/build_wiki_native_graph_mvp.py --phase audit
```

必须检查：

1. 每个 `status=verified` semantic edge 是否有 evidence unit。
2. 每个 `status=verified` semantic edge 是否有 `source_id`、`anchor` 和 `evidence_text`。
3. 高风险 predicate 是否有对应 rule card。
4. source 节点是否存在对应 source page 或 source registry 记录。
5. rule_card 节点是否存在对应 rule card page。
6. candidate 边是否全部标记 `blocked_from_runtime=true`。
7. 是否存在未带 provenance 的实体-实体边。
8. `status=verified` 的 semantic edges 是否只包含 `validation_status=accepted` 的边。
9. 高风险 predicate 是否通过 second validator。
10. 每条新增语义边是否有 `diff_action` 和 `validation_summary`。

输出：

```text
issues/wiki_native_graph_build_report.json
issues/wiki_native_graph_build_report.md
```

## 6. 废弃与兼容策略

### 6.1 不再使用旧规则作为新图核心

以下旧逻辑不再作为主图谱构建依据：

- runtime manifest 决定全部页面节点；
- risk_class 自动推导所有 rule card；
- `knowledge_facts_status_index.json` 决定所有 fact 节点；
- page -> fact -> source 作为唯一 fact 图结构。

这些可以保留为 legacy audit 输入，但不能决定新图核心边。

### 6.2 新图优先级

```text
wiki inline fact anchor
  > wiki section + source anchor
  > frontmatter source declaration
  > runtime manifest legacy status
```

也就是说，页面正文里的 `fact_id/source_id/anchor` 是最高优先级证据。

## 7. 为什么这样更简洁

旧方案的问题是把多个历史产物叠在一起：

```text
manifest -> fact status index -> graph -> verified layer -> projection layer
```

新方案直接从 wiki 内容结构出发：

```text
wiki page -> section -> fact anchor -> semantic edge
```

这样更贴近当前数据实际形态，也更容易让 GPT 执行：

1. 先读页面。
2. 找标题。
3. 找 fact/source/anchor。
4. 按章节映射关系。
5. 没证据就进 candidate。

## 8. 最小可行重构

第一轮不需要覆盖全部关系，只做 3 类页面：

```text
wiki/diseases
wiki/drugs
wiki/rule_cards
```

第一轮只支持 8 个 predicate：

```text
HAS_CLINICAL_SIGN
HAS_TRANSMISSION_ROUTE
HAS_DIAGNOSTIC_METHOD
HAS_CONTROL_MEASURE
HAS_DRUG_BOUNDARY
HAS_LABEL_BOUNDARY
HAS_WITHDRAWAL_OR_MRL_BOUNDARY
HAS_CONTRAINDICATION_OR_INTERACTION
```

第一轮验收标准：

- 能从疾病页抽取 inline fact anchors。
- 能从药物页抽取 boundary facts。
- 所有 semantic edges 都有 `derived_from_fact_id/source_id/anchor`。
- candidate/rejected edges 进入统一图谱，但必须设置 `blocked_from_runtime=true` 和 `gold_dataset_ready=false`。
- 旧 `wiki/graph-data.json` 不被覆盖。
- 每次构建都有 `wiki/wiki-native-graph.json` 和 `issues/wiki_native_graph_build_report.json/md`，报告中包含 build manifest、diff summary、audit summary、failed_operations。
- 高风险 predicate 不通过 second validator 时不能 accepted。
- 新 object 节点必须来自 exact_text_span。

## 9. Runtime Admission Rule

正式问答和运行时图谱只能读取：

```text
wiki/wiki-native-graph.json
```

并且只允许使用满足以下条件的边：

```text
status = verified
confidence_layer = verified
validation_status = accepted
blocked_from_runtime != true
```

统一图谱中 `status=candidate` 的边只用于：

```text
1. 后续证据补强
2. 人工审核
3. 提醒缺失关系
4. lint 报告
```

统一图谱中 `status=rejected` 的边只用于：

```text
1. 审计
2. 防止重复提出已拒绝关系
3. 解释为何某些节点不应相连
```

强规则：

```text
没有可解析 provenance 的关系边，不是低置信关系，而是未获准关系。
它可以被记录，但不得参与正式知识图谱推理。
```

完整性规则：

```text
图谱完整性不靠放宽 verified 标准实现，而靠 status 分层实现。
页面、section、source、rule_card、evidence_unit、candidate edge、rejected edge 都进入统一图谱。
只有 status=verified 且 validation_status=accepted 的 semantic edge 能作为事实边服务问答、黄金数据集和 SFT。
```

## 9.1 黄金数据集使用规则

wiki-native graph 的最终目标是服务猪病黄金数据集、SFT、评估和反幻觉训练。不同状态的数据用途必须分开：

| 图谱元素 | 可用于 | 不可用于 |
|---|---|---|
| `status=verified` semantic edge | 正例、标准答案、SFT 事实支撑、评估 expected answer | 无来源自由发挥 |
| `status=candidate` edge | 缺口发现、人工复核、困难题候选、需要查证的问题 | 正例答案、确定性结论 |
| `status=rejected` edge | 负例、反幻觉训练、陷阱题、禁止连接说明 | 正例、事实支撑 |
| structural/evidence edge | 检索路由、引用链、证据解释 | 直接替代语义事实 |
| rule/governance edge | 拒答、边界、评分规则、越界检测 | 生成新的事实关系 |

### 正例样本

正例样本只能从 verified semantic edge 生成：

```json
{
  "question_type": "clinical_summary",
  "subject": "disease:DIS-024",
  "expected_fact_edges": ["edge:..."],
  "required_citations": ["SRC-0046"],
  "required_anchors": ["Chapter 39; PDF page 649-651"],
  "answer_boundary": "must cite evidence unit; no unsupported treatment"
}
```

### 负例和陷阱样本

负例优先来自：

```text
status=rejected
status=candidate 且 blocked_from_runtime=true
high_risk predicate 缺少 rule card
药物页中的 boundary_only 信息
```

负例目标：

```text
训练模型不要把候选、共现、边界提示、禁用信息误写成正向事实。
```

### 评估样本

评估样本必须同时保存：

```text
expected_edge_ids
forbidden_edge_ids
required_source_ids
required_rule_cards
risk_class
```

这样可以自动判断模型是否：

1. 命中正确 verified 边；
2. 引用了必要 source；
3. 避免了 rejected/candidate 边；
4. 遵守高风险 rule card；
5. 没有生成 unsupported prescription、withdrawal、MRL 或监管结论。

## 10. Lint 与验收清单

每次 wiki-native graph 构建后必须执行强制 lint。自动修复前必须先出报告，不能静默修改。

必须检查：

- 孤儿页。
- 死链。
- 缺失反向链接；第一阶段只 warning，不阻塞。
- 未绑定 source 的边。
- 未绑定 fact/anchor 的语义边。
- candidate/rejected 边是否被错误设置为 `blocked_from_runtime=false`。
- candidate/rejected 边是否被错误设置为 `gold_dataset_ready=true`。
- 同名实体是否误连。
- 冲突边是否已标注。
- 高风险边是否有 rule card 和 second validator 记录。
- 候选边是否长期未审。
- LLM proposal 是否全部有解析结果；第一阶段如果不启用 LLM proposal，可跳过。
- failed operations 是否为空或均有 reason；第一阶段合并记录在 build report 中。

推荐输出：

```text
issues/wiki_native_graph_lint_report.json
issues/wiki_native_graph_lint_report.md
```

第一阶段阻塞项只包括：

```text
1. verified semantic edge 缺少 evidence unit。
2. verified semantic edge 缺少 source_id、anchor、evidence_text 或 supporting_span。
3. predicate 不在 registry 中却被标为 verified。
4. candidate/rejected 边被用于 gold_dataset_ready=true。
5. 高风险 verified 边缺少 required rule card。
6. Phase C 直接生成 verified semantic edge，而不是 candidate proposal。
7. verified semantic edge 的 supporting_span 不是 evidence_text 原文子串。
8. 普通 verified semantic edge 未通过 evidence_support_check。
```

其他问题先作为 warning，避免实施成本过高。

## 11. 关系冲突与降级规则

冲突不能覆盖式改写，必须显式记录。

规则：

1. 新 verified edge 与既有 verified edge 冲突时，新边先保持 candidate，并记录 reason=conflicts_with_existing_verified_edge。
2. 除非新证据 authority 更高且 validator 明确 supported，否则不能删除旧边。
3. 冲突双方都要记录 `conflicts_with_edge_id`。
4. rejected 边保留在统一图谱中，并设置 `status=rejected`，用于防止后续重复生成。
5. 方向不确定时，不能强行生成 directed edge；只能进入 candidate。
6. 关系类型不确定时，不能硬指定细粒度 predicate；进入 candidate 或 gap。

## 12. GPT 执行指令

```text
请在 D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative 中按 WIKI_NATIVE_KNOWLEDGE_GRAPH_REDESIGN.md 实施 wiki-native 图谱重构。

要求：
1. 不要沿用旧 graph-data.json 的构图规则作为核心。
2. 不要修改旧 graph-data.json。
3. 新图谱从 wiki 页面、frontmatter、section heading、inline fact_id/source_id/anchor 构建。
4. 第一阶段只输出一个统一图谱文件：wiki/wiki-native-graph.json。
5. 所有边都必须带 status=verified|candidate|rejected。
6. LLM 只能输出 edge proposal，不能直接写入 status=verified；验证器通过后才允许升级。
7. 没有 source_id/anchor/evidence_text/supporting_span 的语义关系不得标为 status=verified；缺 fact_id 时默认 candidate，除非 registry 明确允许 source_id+anchor 作为最低证据。
8. candidate 边必须设置 blocked_from_runtime=true、gold_dataset_ready=false，并记录 reason。
9. rejected 边必须保存在统一图谱中，设置 blocked_from_runtime=true、gold_dataset_ready=false，并记录 rejected_reason。
10. 每次构建必须生成 issues/wiki_native_graph_build_report.json/md，报告中包含 build manifest、coverage、diff summary、audit summary、failed_operations。
11. 审计失败不删除图谱，但失败影响到的边不得 verified；报告必须标记 build_status=partial 或 failed。
12. 高风险 predicate 当前第一阶段必须通过 rule card；药物、MRL、监管、处方边在最终进入训练集前必须补做 source alignment 和 medical entailment。当前 MVP 中 `second_validator=pass_rule_card_gated` 不能视为完整医学复核。
13. 不确定关系进入 candidate，不得 accepted/verified。
14. 黄金数据集、SFT 正例和标准答案只能读取 `status=verified`、`validation_status=accepted` 且 `evidence_support_check=pass` 的 semantic edge；其中药物、处方、标签、MRL、监管、鉴别诊断等高风险边还必须额外满足后续 `source_alignment_status=pass` 和 `medical_entailment=supported`，才能进入最终训练正例。
```

## 13. 最终可接受标准

第一阶段满足以下条件，wiki-native graph 就可以视为可用于并行黄金数据集候选生成和人工/程序复核；对于高风险医学关系，不能直接视为最终训练集：

1. 每条 verified semantic edge 都能反查到 evidence unit，且包含 `source_id/anchor/evidence_text/supporting_span`；有 `fact_id` 时必须记录。
2. 每条 verified semantic edge 都有 `validation_status=accepted`。
3. 每条 edge 的 subject 和 object 都存在于 node registry；新 object 优先来自 exact_text_span。
4. 每条 verified edge 都有 `validation_summary`。
5. 每次构建都有 `issues/wiki_native_graph_build_report.json/md`。
6. candidate edge 永远 `blocked_from_runtime=true`。
7. rejected edge 不可设置 `gold_dataset_ready=true`。
8. 高风险 predicate 必须有 required rule card；当前第一阶段只实现 rule card 门控式 second validator 标记，下一阶段必须补齐真正的 source alignment 和 medical entailment。
9. 如果新增边无法证明由 evidence unit 支持，则 rejected 或 candidate，不允许 verified。
10. 旧 `wiki/graph-data.json` 没有被覆盖。
11. 每条 verified semantic edge 都有 `evidence_support_check=pass`。
12. 高风险边如果尚未具备 `source_alignment_status=pass` 和 `medical_entailment=supported`，只能作为黄金数据集候选正例，不得直接进入最终训练正例。

第一阶段覆盖率目标：

```text
1. wiki/diseases、wiki/drugs、wiki/comparisons、wiki/syndromes、wiki/rule_cards、wiki/synthesis 均建 page nodes。
2. diseases/drugs 页面中可识别的 inline fact/source/anchor 至少 90% 进入 evidence_units。
3. 所有 rule_cards 进入治理节点。
4. 所有 source_ids 至少生成 source nodes，即使 source 页面暂缺也要标记 source_page_missing。
5. verified/candidate/rejected 均计入报告，避免因证据不足而“消失”。
6. 未进入 evidence_units 的页面段落必须计入 uncovered_content_summary，不能静默丢弃。
7. 每个 disease/drug 页面必须报告 evidence coverage；低于阈值的页面不得标记 page_gold_ready=true。
```

覆盖率不足的处理原则：

```text
覆盖率不足不是放宽 verified 标准的理由。
覆盖率不足只会降低 page_gold_ready 或 graph_gold_readiness，并进入补证队列。
```

## 14. MVP 实施清单

第一阶段按以下顺序实施，保证方案可落地、不过重：

```text
1. 新建 config/wiki_native_predicate_registry.json
   - 只注册第一阶段 predicate、允许的 subject/object type、required_evidence、risk_level、required_rule_card。

2. 新建 tools/build_wiki_native_graph_mvp.py
   - 一个脚本支持 scan/evidence/semantic/validate/report/audit 六个 phase。
   - 不拆多个构建脚本，避免流程发散。

3. scan phase
   - 扫描 wiki/diseases、wiki/drugs、wiki/comparisons、wiki/syndromes、wiki/rule_cards、wiki/synthesis、wiki/sources。
   - 生成 page、section、source、rule_card 节点。

4. evidence phase
   - 从页面正文抽取 fact_id/source_id/anchor/evidence_text。
   - 没有 fact_id 但有 source_id+anchor 的内容也进入 evidence_units，并标记 evidence_level=anchored。

5. semantic phase
   - 只从 evidence unit 和 section_title 映射生成 semantic edge proposal。
   - object 优先使用 exact_text_span，不做激进实体合并。

6. validate phase
   - schema、endpoint、provenance、graph consistency 全量检查。
   - entailment/second validator 只检查高风险边和 LLM proposal 边。

7. report/audit phase
   - 输出 wiki/wiki-native-graph.json。
   - 输出 issues/wiki_native_graph_build_report.json/md。
   - 报告 coverage、uncovered_content_summary、verified/candidate/rejected 数量、failed_operations、gold_dataset_readiness。

8. 黄金数据集生成
   - 正例只读取 status=verified、validation_status=accepted、evidence_support_check=pass、gold_dataset_ready=true 的 semantic edge。
   - candidate/rejected 只进入困难题、负例、反幻觉训练和人工复核队列。
```

最小闭环判断：

```text
只要一个疾病页或药物页新增/更新后，新脚本能明确回答：
1. 新增了哪些节点？
2. 新增了哪些关系？
3. 每条关系来自哪段 evidence_text？
4. 为什么它是 verified/candidate/rejected？
5. 它能否进入黄金数据集？

则该轮构建有效。
```
