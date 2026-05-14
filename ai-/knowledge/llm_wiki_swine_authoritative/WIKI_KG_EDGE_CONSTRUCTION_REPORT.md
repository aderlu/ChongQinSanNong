# Wiki 知识图谱节点关系边构建汇报

本文档用于汇报当前 Wiki 知识图谱中节点之间的边如何构建、相比优化前有什么改进、目前解决了什么问题、还存在什么问题，以及后续理论上如何解决。

## 1. 当前图谱基本情况

当前主图谱文件：

```text
wiki/wiki-native-graph.json
```

当前可视化文件：

```text
wiki/wiki-native-knowledge-graph.html
wiki/wiki-native-knowledge-graph-audit.html
```

当前构建脚本：

```text
tools/build_wiki_native_graph_mvp.py
tools/render_wiki_native_graph.py
```

当前图谱边总数：

```text
6240
```

四类边数量：

| 边层级 | 数量 | 主要类型 | 当前作用 |
|---|---:|---|---|
| `structural` | 4777 | `HAS_SECTION` | 表示页面包含章节 |
| `evidence` | 1176 | `CITES_SOURCE`、`REFERENCES_ENTITY` | 表示页面引用来源或实体 |
| `governance` | 189 | `GOVERNED_BY_RULE_CARD`、`GOVERNED_BY_RULE` | 表示页面受规则卡或规则约束 |
| `semantic` | 98 | `HAS_CLINICAL_SIGN` 等 | 表示从证据文本抽象出的医学语义关系 |

语义边状态：

```text
verified: 70
candidate: 28
```

语义边类型分布：

| 语义边类型 | 数量 |
|---|---:|
| `HAS_DIAGNOSTIC_METHOD` | 27 |
| `HAS_CONTROL_MEASURE` | 22 |
| `HAS_CLINICAL_SIGN` | 18 |
| `HAS_PATHOGEN` | 16 |
| `HAS_TRANSMISSION_ROUTE` | 14 |
| `HAS_DRUG_BOUNDARY` | 1 |

## 2. 优化前的边是如何构建的

优化前主要依赖旧图谱：

```text
wiki/graph-data.json
```

旧图谱更接近 runtime provenance graph，主要表达：

```text
页面
source
rule
fact anchor
runtime 检索和引用关系
```

旧构建方式的问题：

1. 边更多服务运行时检索和来源路由，而不是严格表达医学语义关系。
2. 页面状态、证据状态、运行时用途混在一起，例如 `HUMAN_REVIEWED`、`NEEDS_REVIEW`、`gold_dataset_use`、`Runtime task use` 等。
3. 图谱中 page/source/rule/fact 锚点关系较多，但缺少清晰的 semantic edge 状态机。
4. LLM 或规则生成的关系和可验证关系边界不够清楚。
5. 候选关系、拒绝关系、正式可用关系没有充分分层。
6. 旧图不适合直接作为猪病黄金数据集正例来源。

因此，优化前可以支持：

```text
检索
来源路由
规则门禁
页面导航
```

但难以回答：

```text
这条疾病-症状关系来自哪段证据？
这条疾病-用药边界是否可作为训练正例？
这条边是 verified、candidate 还是 rejected？
这条边是否有 source_id、anchor、supporting_span？
```

## 3. 当前优化后的边是如何构建的

当前采用 wiki-native 图谱，不再以旧 `graph-data.json` 作为核心输入，而是从 Wiki 页面重新扫描构建。

总体流程：

```text
wiki Markdown 页面
  -> 解析 frontmatter
  -> 创建 page 节点
  -> 解析 Markdown heading
  -> 创建 section 节点
  -> 解析 sources
  -> 创建 source/rule 引用边
  -> 解析正文 fact_id/source_id/anchor
  -> 创建 evidence_unit
  -> 根据 page_type + section_title + predicate registry 生成 semantic edge proposal
  -> validator 校验
  -> 输出 verified/candidate/rejected
```

核心代码位置：

| 功能 | 代码位置 |
|---|---|
| 页面和章节节点构建 | `tools/build_wiki_native_graph_mvp.py::build_page_nodes` |
| 结构边、来源边、治理边构建 | `tools/build_wiki_native_graph_mvp.py::build_structural_edges` |
| 证据单元抽取 | `tools/build_wiki_native_graph_mvp.py::build_evidence_units` |
| 根据章节标题选择 predicate | `tools/build_wiki_native_graph_mvp.py::predicate_for_section` |
| 语义对象节点构建 | `tools/build_wiki_native_graph_mvp.py::semantic_object_node` |
| 语义边构建 | `tools/build_wiki_native_graph_mvp.py::build_semantic_edges` |
| 语义边验证 | `tools/build_wiki_native_graph_mvp.py::validate_semantic_edge` |
| 最终审计 | `tools/build_wiki_native_graph_mvp.py::audit_graph` |

## 4. 当前四种边的详细说明

### 4.1 structural 结构边

代表：

```text
页面包含某个章节。
```

典型形式：

```text
page -> section
```

真实例子：

```json
{
  "layer": "structural",
  "type": "HAS_SECTION",
  "source": "disease:DIS-008",
  "target": "section:disease:DIS-008:临床症状:36",
  "status": "verified"
}
```

含义：

```text
猪流行性腹泻页面包含“临床症状”章节。
```

建立依据：

```text
Markdown 标题。
```

解决的问题：

```text
让图谱能追踪页面结构和证据所在位置。
```

不能解决的问题：

```text
它不证明章节内的医学事实正确。
```

### 4.2 evidence 来源/证据边

代表：

```text
页面引用某个 source，或页面引用某个实体。
```

典型形式：

```text
page -> source
page -> referenced entity
```

真实例子：

```json
{
  "layer": "evidence",
  "type": "CITES_SOURCE",
  "source": "disease:DIS-008",
  "target": "source:SRC-0087",
  "source_id": "SRC-0087",
  "status": "verified"
}
```

建立依据：

```yaml
sources: [SRC-0087]
```

解决的问题：

```text
让页面和来源之间的引用关系可追溯。
```

不能解决的问题：

```text
page -> source 只表示页面引用了该来源，不表示 source 支持页面中的每一句话。
```

### 4.3 governance 规则治理边

代表：

```text
页面受某个 rule card 或 rule 约束。
```

典型形式：

```text
page -> rule_card
page -> rule
```

真实例子：

```json
{
  "layer": "governance",
  "type": "GOVERNED_BY_RULE_CARD",
  "source": "disease:DIS-008",
  "target": "rule_card:RC-DISEASE-REGULATORY-001",
  "source_id": "RC-DISEASE-REGULATORY-001",
  "status": "verified"
}
```

建立依据：

```yaml
sources: [RC-DISEASE-REGULATORY-001]
```

解决的问题：

```text
把用药、监管、诊断、休药期、MRL 等规则约束显式接入图谱。
```

不能解决的问题：

```text
它不证明某个具体医学事实成立，只表示后续生成和验证必须受该规则约束。
```

### 4.4 semantic 语义事实边

代表：

```text
从证据文本中抽象出的医学语义关系。
```

典型形式：

```text
disease -> HAS_CLINICAL_SIGN -> literal_span
disease -> HAS_TRANSMISSION_ROUTE -> literal_span
disease -> HAS_DIAGNOSTIC_METHOD -> literal_span
disease -> HAS_CONTROL_MEASURE -> literal_span
disease -> HAS_PATHOGEN -> literal_span
disease/drug -> HAS_DRUG_BOUNDARY -> literal_span
```

真实例子：

```json
{
  "layer": "semantic",
  "type": "HAS_TRANSMISSION_ROUTE",
  "source": "disease:DIS-048",
  "target": "semantic_object:29c6251a0b567be6",
  "source_id": "SRC-0072",
  "anchor": "Chapter 58 Proliferative Enteropathy; PDF page 925",
  "evidence_unit_id": "evidence_unit:0feb4ef6067ae806",
  "section_id": "section:disease:DIS-048:流行病学-传播边界:35",
  "status": "verified"
}
```

含义：

```text
猪增生性肠病页面中，有一段来源锚定证据，被当前系统归为传播/流行相关语义。
```

建立依据：

```text
当前页面类型 = disease
当前章节标题 = 流行病学/传播边界
正文有 source_id + anchor + evidence_text
predicate registry 匹配 HAS_TRANSMISSION_ROUTE
validator 检查证据字段完整性
```

解决的问题：

```text
让疾病-症状、疾病-传播、疾病-诊断、防控、病原等语义关系具备 evidence_unit/source_id/anchor。
```

不能解决的问题：

```text
当前 semantic verified 还没有完成 source 原文对齐、端点落地、医学蕴含和高风险二次验证。
```

## 5. 相比优化前的主要改进

### 5.1 从旧 runtime 图谱转为 wiki-native 图谱

优化前：

```text
以 graph-data.json 为核心，更偏 runtime provenance。
```

优化后：

```text
从 wiki 页面、frontmatter、section、inline fact/source/anchor 重新构建。
```

解决的问题：

```text
减少旧规则叠加造成的冗余，让图谱直接反映当前 Wiki 内容结构。
```

### 5.2 明确分成四类边

优化前：

```text
结构、来源、规则、事实关系边界不够清楚。
```

优化后：

```text
structural/evidence/governance/semantic 分层。
```

解决的问题：

```text
避免把“页面引用 source”误解为“source 支持所有医学事实”。
避免把“受规则卡约束”误解为“已经有处方事实”。
```

### 5.3 引入 evidence_unit

优化前：

```text
很多关系只能追到页面或 source，难以追到具体证据文本。
```

优化后：

```text
正文中的 fact_id/source_id/anchor 会形成 evidence_unit。
```

解决的问题：

```text
每条 semantic edge 可以追踪到 evidence_text、source_id、anchor。
```

### 5.4 引入 verified/candidate/rejected 状态

优化前：

```text
候选边、可用边、不可用边不够清楚。
```

优化后：

```text
所有语义边先 candidate，再由 validator 判断是否 verified。
```

解决的问题：

```text
证据不足的边不会直接进入黄金数据集正例。
```

### 5.5 引入统一页面状态

优化前：

```text
HUMAN_REVIEWED、NEEDS_REVIEW、gold_dataset_use、Runtime task use 等状态混乱。
```

优化后：

```text
source_trust
evidence_coverage
usage_scope
```

解决的问题：

```text
页面来源可信、证据覆盖程度、使用范围分开表达，降低系统复杂度。
```

## 6. 当前起到的作用

当前图谱已经可以有效支持：

1. 页面结构追踪。
2. 来源引用追踪。
3. 规则卡约束追踪。
4. 证据单元追踪。
5. 语义关系候选发现。
6. 知识图谱 HTML 可视化。
7. 节点搜索和全量关系展开。
8. 黄金数据集候选来源筛选。
9. 反幻觉训练中的 candidate/rejected 线索保留。

当前能防止的问题：

```text
完全没有 source_id/anchor/evidence_text 的语义边直接 verified。
candidate/rejected 边进入黄金正例。
页面结构、来源、规则、语义关系混在一起。
章节节点过多导致主图不可用。
```

## 7. 当前仍未解决的问题

### 7.1 不能完全证明医学事实严格成立

原因：

```text
当前 semantic edge 主要基于 evidence_unit + 章节标题 + predicate registry。
```

尚未完成：

```text
source 原文对齐
anchor 可定位验证
evidence_text 是否被 source 原文支持
subject/object 是否都在证据中明确落地
predicate 是否被医学语义蕴含
高风险边 second validator
```

### 7.2 supporting_span 还不够精确

当前：

```text
supporting_span 多数等于整条 evidence_text。
```

问题：

```text
它能证明不是凭空生成，但不能证明哪一个最小短语支撑关系。
```

### 7.3 章节标题仍可能误导 predicate

例如章节标题是：

```text
临床症状和病理机制
```

其中某一句可能实际表达病理机制，但因为章节标题包含“临床症状”，被映射为：

```text
HAS_CLINICAL_SIGN
```

问题：

```text
章节标题只能作为候选提示，不能作为最终医学语义判断。
```

### 7.4 高风险边不能直接作为最终训练正例

高风险边包括：

```text
HAS_DRUG_BOUNDARY
HAS_LABEL_BOUNDARY
HAS_WITHDRAWAL_OR_MRL_BOUNDARY
REGULATORY_BOUNDARY
DIFFERENTIAL_DIAGNOSIS
```

当前缺少：

```text
标签一致性
靶动物一致性
法域一致性
禁用/限制判断
休药期/MRL 校验
二次验证结果
```

## 8. 阻碍是什么

### 8.1 source 原文数据不一定完整

如果只有 source_id 和章节名，没有 OCR 文本、PDF 页文本或 HTML 原文，就无法严格验证：

```text
evidence_text 是否真的来自 source 原文。
```

### 8.2 anchor 粒度不统一

当前 anchor 可能是：

```text
章节名
PDF page
网页标题
法规附件
本地文本路径
```

如果 anchor 不能稳定定位，就无法自动 source alignment。

### 8.3 别名表不完整

疾病、药物、商品名、英文名、简称、类别名不完整时，容易出现：

```text
实体无法落地
object 错连
同义词漏连
类别名误当具体药物
```

### 8.4 医学语义需要专业判断

一些文本不是规则能完全判断的，例如：

```text
经验性治疗
实验研究
其他动物标签
其他法域标签
复方药
禁用与例外情况
冲突来源
```

这些需要受约束 LLM、专家复核或补充结构化标签数据。

## 9. 理论上如何解决

### 9.1 增加 source alignment

目标：

```text
验证 source_id、anchor、evidence_text 与 source 原文一致。
```

新增字段：

```text
source_alignment_status=pass|candidate|rejected
anchor_found_in_source=true|false
evidence_text_supported_by_source=true|false
```

能解决：

```text
引用了 source_id 但原文不支持的问题。
```

需要补充：

```text
PDF OCR 文本
HTML 原文
source 摘录
页码索引
```

### 9.2 增加 endpoint grounding

目标：

```text
验证 subject 和 object 都被证据明确指向。
```

新增字段：

```text
subject_grounded=true|false
object_grounded=true|false
endpoint_grounding_status=pass|candidate|rejected
```

能解决：

```text
同页多个实体共现导致的交叉乱连。
```

需要补充：

```text
疾病别名表
药物别名表
商品名/通用名/类别名映射
```

### 9.3 增加 medical entailment

目标：

```text
验证 evidence_text 是否医学语义上支持 predicate。
```

新增字段：

```text
medical_entailment=supported|ambiguous|not_supported
minimal_supporting_span=...
```

能解决：

```text
共现误连
章节标题误推
否定/禁用误判
边界条件丢失
```

实现方式：

```text
确定性规则
受约束 LLM validator
高风险人工抽样复核
```

### 9.4 增加 high-risk second validator

目标：

```text
药物、处方、MRL、监管、鉴别诊断不得只靠普通验证进入训练正例。
```

检查：

```text
rule card
靶动物
剂型/途径
适应症
禁用
休药期
MRL
法域
标签来源
```

能解决：

```text
高风险医学关系进入黄金数据集造成训练污染。
```

## 10. 最终建议

当前图谱应按分层使用：

| 层级 | 用途 | 是否要求最严格验证 |
|---|---|---|
| 结构层 | 导航、章节定位 | 否 |
| 来源层 | 证据追溯、source 路由 | 否 |
| 治理层 | 规则门控、风险约束 | 否 |
| 语义候选层 | 关系发现、复核队列 | 部分 |
| 严格事实层 | 问答事实支撑 | 是 |
| 黄金训练层 | SFT/评估正例 | 最严格 |

最终原则：

```text
图谱覆盖可以尽量全。
事实层准入必须严格。
训练层准入必须最严格。
不确定关系保留为 candidate，不得强行 verified。
```

## 11. 结论

当前优化已经解决：

```text
旧图谱规则叠加混乱
页面结构和来源关系不可分
候选边与正式边不分
缺少 evidence_unit
缺少 build/audit report
可视化关系追溯不足
页面状态字段复杂混乱
```

当前还没有完全解决：

```text
source 原文对齐
医学语义蕴含验证
高风险二次验证
最小 supporting_span
别名落地和实体消歧
冲突来源处理
```

理论解决路径：

```text
source_alignment_check
endpoint_grounding_check
medical_entailment_check
high_risk_second_validator
expert_review_queue
source_text_backfill_queue
```

这意味着：当前关系边已经不是随意乱连，而是有 Wiki 结构、来源标记和证据单元支撑的规则构建边；但要成为严格医学事实边，还必须继续补齐 source 原文对齐、端点落地、医学蕴含和高风险二次验证。
