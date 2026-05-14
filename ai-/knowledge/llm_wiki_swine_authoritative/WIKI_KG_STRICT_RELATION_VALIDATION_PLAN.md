# Wiki Knowledge Graph Strict Relation Validation Plan

本文档给出一套可落地的关系边严格验证方案，目标是最大可能实现：

```text
节点关系严格真实正确
不是同页共现乱连
不是章节标题误推
不是 LLM 幻觉生成
不是从权威文本中过度抽象出的错误关系
```

## 1. 当前问题判断

当前图谱已经能做到“语义边有形式化证据链”，但还不能完全证明“语义边符合医学事实”。

当前已具备：

```text
edge -> evidence_unit_id
edge -> source_id
edge -> anchor
edge -> evidence_text
edge -> supporting_span
supporting_span in evidence_text
validation_status=accepted
evidence_support_check=pass
audit blockers=0
```

当前缺口：

```text
没有逐条回查 source 原文
没有验证 anchor 是否能定位到原始来源
没有验证 evidence_text 是否被 source 原文支持
没有验证 subject/object 是否都被证据明确落地
没有验证 predicate 是否被医学语义蕴含
高风险边没有真正 second validator
supporting_span 多数仍是整条 evidence_text，不是最小支持片段
```

因此，当前 `verified` 只能解释为：

```text
通过当前代码定义的证据链形式校验。
```

不能解释为：

```text
已经严格证明医学事实成立。
```

## 2. 总体解决思路

把关系边验证从一层 `verified` 升级为六级准入管线：

```text
candidate
  -> schema_validated
  -> provenance_validated
  -> source_aligned
  -> endpoint_grounded
  -> medically_entailed
  -> verified
```

任何一层失败，都不能进入最终 verified。

最终 verified 边必须满足：

```json
{
  "status": "verified",
  "validation_status": "accepted",
  "evidence_support_check": "pass",
  "source_alignment_status": "pass",
  "endpoint_grounding_status": "pass",
  "medical_entailment": "supported",
  "blocked_from_runtime": false,
  "gold_dataset_ready": true
}
```

高风险边还必须额外满足：

```json
{
  "required_rule_card_check": "pass",
  "second_validator": "pass",
  "negation_or_boundary_handled": true,
  "jurisdiction_scope_checked": true
}
```

## 3. 分层方案

### 3.1 Schema Validation

解决的问题：

```text
防止边类型非法、端点类型非法、字段缺失。
```

判断规则：

```text
predicate 必须在 config/wiki_native_predicate_registry.json 中注册。
source node type 必须在 allowed_subject_types 中。
target node type 必须在 allowed_object_types 中。
高风险 predicate 必须标记 high_risk=true。
```

为什么有效：

```text
它能防止疾病页和药物页因为同页出现而被任意连成不合法关系。
```

需要代码实现：

```text
在 validate_semantic_edge 中增加 endpoint type check。
构建 audit report 时输出 schema_validation 统计。
```

### 3.2 Provenance Validation

解决的问题：

```text
防止无来源、无锚点、无证据文本的关系边进入 verified。
```

判断规则：

```text
必须有 evidence_unit_id。
必须有 source_id。
必须有 anchor。
必须有 evidence_text。
必须有 supporting_span。
supporting_span 必须是 evidence_text 的原文子串。
```

为什么有效：

```text
它能防止 LLM 直接生成“看起来合理但没有出处”的边。
```

当前状态：

```text
当前代码已经基本实现这一层。
```

仍需改进：

```text
supporting_span 应从整句 evidence_text 精确裁剪为最小支持片段。
```

### 3.3 Source Alignment Check

解决的问题：

```text
防止 wiki 页面写了 source_id，但 source 原文其实不支持该关系。
```

新增字段：

```json
{
  "source_node_exists": true,
  "source_page_exists": true,
  "anchor_found_in_source": true,
  "evidence_text_supported_by_source": true,
  "source_alignment_status": "pass|candidate|rejected",
  "source_alignment_reason": ""
}
```

判断规则：

```text
source_id 必须对应 source 节点。
source_id 必须能找到 wiki/sources 页面或 source registry 记录。
anchor 必须能在 source 页面、source 索引或本地原文摘录中定位。
evidence_text 必须能被 source anchor 附近文本直接支持。
如果找不到原始 source 文本，只能 candidate，不能 verified。
```

为什么有效：

```text
它能解决“引用了权威来源名，但引用位置不匹配或原文不支持”的问题。
```

需要补充的数据：

```text
必须有可检索的 source 原文、PDF OCR 文本、HTML 文本、source 摘录或页码索引。
如果只有 source_id 和书名，没有对应页码文本，则无法仅靠规则严格验证。
```

无法仅靠代码解决的情况：

```text
PDF 没有 OCR 文本。
anchor 只写章节名，没有页码或可定位文本。
source 页面只是目录级来源，没有原文摘录。
```

这类边处理方式：

```text
降级为 candidate_source_unresolved。
进入 source_text_backfill_queue。
不得进入最终黄金训练正例。
```

### 3.4 Endpoint Grounding Check

解决的问题：

```text
防止同一段文字里出现多个疾病、多个药物、多个症状时交叉乱连。
```

新增字段：

```json
{
  "subject_grounded": true,
  "object_grounded": true,
  "object_span_in_evidence": true,
  "endpoint_grounding_status": "pass|candidate|rejected",
  "endpoint_grounding_reason": ""
}
```

判断规则：

```text
subject 必须由当前页面身份、标题、frontmatter id 或 evidence_text 明确指向。
object 必须来自 evidence_text 或 supporting_span。
literal_span target 必须保留 exact_text_span。
药物对象必须能匹配 drug page alias 或原文药名。
疾病对象必须能匹配 disease page alias 或原文疾病名。
如果证据只支持泛称“该病”“本病”，必须能绑定到当前页面 subject。
```

为什么有效：

```text
它能防止“同一页面中出现多个对象，系统随机连接”的问题。
```

需要补充的数据：

```text
疾病别名表。
药物别名表。
中文名/英文名/商品名/类别名映射。
```

无法仅靠规则解决的情况：

```text
原文使用高度省略表达，如“上述药物”“该方案”“前者”“后者”。
```

这类边处理方式：

```text
降级为 candidate_endpoint_ambiguous。
需要人工或 LLM constrained resolver 复核。
```

### 3.5 Predicate Medical Entailment Check

解决的问题：

```text
防止证据文本虽然权威，但不支持当前 predicate。
```

典型错误：

```text
提到药物 -> 被误连成推荐用药。
提到检测方法 -> 被误连成确诊方法。
提到相似疾病 -> 被误连成正式鉴别诊断。
提到禁用/不得使用 -> 被误连成可用治疗。
提到其他动物标签 -> 被误外推为猪用。
```

新增字段：

```json
{
  "medical_entailment": "supported|not_supported|ambiguous",
  "medical_entailment_reason": "",
  "minimal_supporting_span": "",
  "negation_detected": false,
  "boundary_detected": false,
  "extrapolation_detected": false
}
```

判断规则：

```text
HAS_CLINICAL_SIGN 必须表达临床症状、表现、体征或病例表现。
HAS_TRANSMISSION_ROUTE 必须表达传播、感染途径、排毒、流行方式。
HAS_DIAGNOSTIC_METHOD 必须表达检测方法、样本、实验室诊断或确诊路径。
HAS_CONTROL_MEASURE 必须表达防控、生物安全、免疫、隔离、监测或环境控制。
HAS_DRUG_BOUNDARY 必须表达用药限制、处方边界、标签要求、禁用、休药期、MRL 或治疗边界。
DIFFERENTIAL_DIAGNOSIS 必须表达相似疾病、鉴别要点、区别诊断或排除条件。
```

为什么有效：

```text
它把“文本共现”升级为“语义支持”，能真正防止关系边从权威文本中被错误抽象出来。
```

实现方式：

```text
第一阶段：确定性规则 + 关键词/否定词/章节模式。
第二阶段：受约束 LLM entailment validator。
第三阶段：高风险边人工抽样或双模型一致性验证。
```

LLM validator 约束：

```text
只能读取 subject label、predicate definition、object exact_text_span、evidence_text、source anchor。
不得使用外部常识补全。
必须输出 supported/not_supported/ambiguous。
必须给出 minimal_supporting_span。
不能给出 supporting_span 时，不能 accepted。
```

无法仅靠代码解决的情况：

```text
医学语义需要专业判断。
原文表达含糊。
不同权威来源存在冲突。
证据只给出经验性描述，没有明确适用边界。
```

这类边处理方式：

```text
medical_entailment=ambiguous。
status=candidate。
进入 expert_review_queue。
```

### 3.6 High-Risk Second Validator

高风险边包括：

```text
HAS_DRUG_BOUNDARY
HAS_LABEL_BOUNDARY
HAS_WITHDRAWAL_OR_MRL_BOUNDARY
REGULATORY_BOUNDARY
DIFFERENTIAL_DIAGNOSIS
```

解决的问题：

```text
这些边一旦错误，会影响处方、食品安全、监管执行、诊断判断和训练数据质量。
```

高风险边必须额外检查：

```text
是否有 required rule_card。
是否存在否定词、禁用词、限制词。
是否涉及法域。
是否涉及靶动物。
是否涉及产品/剂型/给药途径。
是否涉及剂量、疗程、休药期、MRL。
是否从其他动物、人医、实验研究或其他法域外推。
```

新增字段：

```json
{
  "second_validator": "pass|failed|ambiguous",
  "risk_validation": {
    "required_rule_card_check": "pass",
    "target_species_check": "pass|not_applicable|failed",
    "jurisdiction_scope_check": "pass|not_applicable|failed",
    "label_scope_check": "pass|not_applicable|failed",
    "withdrawal_mrl_check": "pass|not_applicable|failed",
    "negative_or_boundary_handled": true
  }
}
```

为什么有效：

```text
它把普通医学事实和高风险执行性事实分开处理，防止“能检索到”被误当成“能处方/能执行”。
```

无法仅靠规则解决的情况：

```text
缺少当前有效标签。
缺少当地法规。
source 已过期。
不同法域标签不一致。
```

这类边处理方式：

```text
不得 verified。
不得 gold_dataset_ready=true。
只能用于边界题、拒答题、复核队列。
```

## 4. 数据结构改造

### 4.1 Edge 字段

每条 semantic edge 增加：

```json
{
  "schema_validation": "pass|failed",
  "provenance_validation": "pass|candidate|failed",
  "source_alignment_status": "pass|candidate|rejected",
  "endpoint_grounding_status": "pass|candidate|rejected",
  "medical_entailment": "supported|ambiguous|not_supported",
  "risk_validation_status": "pass|not_required|candidate|failed",
  "minimal_supporting_span": "",
  "final_verification_level": "candidate|source_aligned|grounded|medically_supported|verified"
}
```

### 4.2 Report 字段

构建报告增加：

```json
{
  "strict_validation_summary": {
    "source_alignment_pass": 0,
    "source_alignment_candidate": 0,
    "endpoint_grounding_pass": 0,
    "medical_entailment_supported": 0,
    "high_risk_second_validator_pass": 0
  },
  "strict_validation_blockers": [],
  "source_text_backfill_queue": [],
  "expert_review_queue": []
}
```

## 5. 状态准入规则

### 5.1 verified

只有同时满足以下条件，才能 verified：

```text
schema_validation=pass
provenance_validation=pass
source_alignment_status=pass
endpoint_grounding_status=pass
medical_entailment=supported
evidence_support_check=pass
validation_status=accepted
```

### 5.2 candidate

任一情况进入 candidate：

```text
source 原文无法定位
端点绑定不明确
医学蕴含 ambiguous
supporting_span 过长或无法裁剪
缺少高风险二次验证
缺少别名表导致实体无法确定
```

### 5.3 rejected

任一情况进入 rejected：

```text
source 原文明确不支持
supporting_span 不在 evidence_text 中
predicate 与证据语义相反
证据表达禁用但边被建成正向可用
端点类型不合法
高风险边违反 rule card
```

## 6. 实施阶段

### Phase 1：确定性严格校验

目标：

```text
不引入 LLM，先用规则把明显不合格边降级。
```

任务：

```text
1. 增加 source_alignment_check.py。
2. 增加 endpoint_grounding_check.py。
3. 在 build_wiki_native_graph_mvp.py 中接入两个 check。
4. 报告 unresolved source、ambiguous endpoint、missing alias。
```

可解决：

```text
无 source 原文定位的边。
source 节点不存在的边。
object 不在 evidence_text 中的边。
端点类型明显错误的边。
```

不能解决：

```text
复杂医学语义是否蕴含。
含糊表达。
跨句指代。
source 冲突。
```

### Phase 2：医学蕴含验证

目标：

```text
判断 evidence_text 是否真的支持 predicate。
```

任务：

```text
1. 定义 predicate definition。
2. 增加 deterministic entailment rules。
3. 对 ambiguous 边调用 constrained LLM validator。
4. 要求输出 minimal_supporting_span。
```

可解决：

```text
共现误连。
章节标题误推。
否定误判。
边界条件丢失。
```

不能解决：

```text
source 本身过期。
法域法规变化。
需要专家裁决的医学争议。
```

### Phase 3：高风险二次验证

目标：

```text
药物、处方、MRL、监管、鉴别诊断边不得仅凭普通验证进入训练正例。
```

任务：

```text
1. 建立 high_risk_second_validator.py。
2. 对高风险边检查 rule card、标签、靶动物、法域、禁用、休药期、MRL。
3. 输出 risk_validation_status。
4. 不通过则 candidate 或 rejected。
```

可解决：

```text
处方边界误用。
药物标签外推。
休药期/MRL 错用。
监管命令误生成。
鉴别诊断过度扩展。
```

不能解决：

```text
缺少最新法规源。
缺少具体产品标签。
缺少法域上下文。
```

### Phase 4：人工/专家复核队列

目标：

```text
把规则和模型都无法严格判断的边显式进入队列，而不是强行 verified。
```

输出：

```text
issues/source_text_backfill_queue.md
issues/expert_review_queue.md
issues/high_risk_edge_review_queue.md
```

可解决：

```text
让不确定性可见、可管理、可追踪。
```

不能解决：

```text
没有数据、没有 source、没有专家判断时，不能凭空把关系变成事实。
```

## 7. 最终验收标准

图谱可称为“严格关系可信”时，必须满足：

```text
1. 所有 verified semantic edge 均 source_alignment_status=pass。
2. 所有 verified semantic edge 均 endpoint_grounding_status=pass。
3. 所有 verified semantic edge 均 medical_entailment=supported。
4. 所有 high_risk verified edge 均 second_validator=pass。
5. 所有 high_risk verified edge 均有 required rule card。
6. 所有 candidate/rejected edge 均 blocked_from_runtime=true。
7. 所有 gold_dataset_ready=true 的边均满足 verified 最终准入规则。
8. build report 中 strict_validation_blockers=0。
9. source_text_backfill_queue 和 expert_review_queue 中的边不得进入黄金正例。
```

## 8. 黄金数据集准入规则

黄金数据集正例只能读取：

```text
status=verified
validation_status=accepted
evidence_support_check=pass
source_alignment_status=pass
endpoint_grounding_status=pass
medical_entailment=supported
gold_dataset_ready=true
```

高风险正例还必须读取：

```text
second_validator=pass
risk_validation_status=pass
```

不得读取：

```text
candidate
rejected
source_alignment_status!=pass
medical_entailment!=supported
second_validator!=pass 的高风险边
```

## 9. 需要补充的数据清单

以下问题不能仅靠规则和代码完全解决，必须补数据：

| 缺口 | 影响 | 处理 |
|---|---|---|
| source 原文缺失 | 无法验证 evidence_text 是否真实来自 source | 补 OCR/PDF text/HTML text |
| anchor 不可定位 | 无法确认引用位置 | 补页码、章节、原文摘录 |
| 疾病别名缺失 | subject/object grounding 不稳定 | 补 alias index |
| 药物别名/商品名缺失 | 药物边可能错连 | 补 drug alias index |
| 产品标签缺失 | 无法验证正向处方/剂量/休药期 | 补具体标签或法规 |
| 法域上下文缺失 | 监管/标签边无法最终 verified | 补 jurisdiction 字段 |
| 来源冲突 | 无法自动判断哪条为准 | 建 conflict review queue |

## 10. 结论

本方案能解决的问题：

```text
无证据链边
source 名义引用但无法对齐的边
同页共现乱连
章节标题误推
object 不在证据中的边
否定/禁用被误判为正向关系
高风险药物、MRL、监管、鉴别边直接进入训练正例
```

本方案不能仅靠规则和代码解决的问题：

```text
source 原文不存在
anchor 无法定位
缺少药物标签或法规
医学语义存在争议
不同权威来源冲突
需要专家判断的复杂病例
```

最终原则：

```text
没有 source 原文对齐，不 verified。
端点没有证据落地，不 verified。
predicate 没有医学蕴含，不 verified。
高风险边没有二次验证，不进入黄金正例。
不确定不是低置信事实，而是 candidate。
```
