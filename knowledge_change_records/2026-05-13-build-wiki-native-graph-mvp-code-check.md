# build_wiki_native_graph_mvp.py 构图脚本检查与注释补充记录

## 本次问题

- 用户要求检查 `tools/build_wiki_native_graph_mvp.py`。
- 检查发现脚本能通过语法编译，但存在两个需要修正的构图风险：
  - `current_section()` 返回第一个匹配章节，嵌套标题场景下可能返回父章节，导致 semantic predicate 被误判。
  - `predicate_for_section()` 对“鉴别诊断/鉴别解释”可能先命中普通诊断类 predicate，而不是更严格的 `DIFFERENTIAL_DIAGNOSIS`。
- 源码中关于四类边是否由代码规则构建、是否调用 LLM 的解释不够清楚，不利于审计和汇报。

## 修改前代码状态

- 构图脚本：`tools/build_wiki_native_graph_mvp.py`
- 四类边均由代码生成：
  - `structural`：Markdown 章节结构。
  - `evidence`：frontmatter `sources` 中的来源引用。
  - `governance`：frontmatter `sources` 中的规则卡/规则引用。
  - `semantic`：正文 evidence unit 经 predicate registry 和 validator 生成。
- 构建阶段没有调用 LLM。

## 本次修改

- 更新 `current_section()`：
  - 从“返回第一个匹配章节”改为“返回最具体章节”。
  - 避免 `## 病原与分类` 这类父章节覆盖 `## 实验室诊断`、`## 传播途径` 等子/近邻章节语义。
- 更新 `predicate_for_section()`：
  - 对命中“鉴别/differential/comparison/比较”的章节，优先选择 `DIFFERENTIAL_DIAGNOSIS`。
  - 避免高风险鉴别边被普通 `HAS_DIAGNOSTIC_METHOD` 抢先匹配。
- 为以下函数补充中文审计注释：
  - `current_section()`
  - `predicate_for_section()`
  - `build_structural_edges()`
  - `build_evidence_units()`
  - `semantic_object_node()`
  - `validate_semantic_edge()`
  - `build_semantic_edges()`

## 解决的问题

- 让 semantic 边类型更贴近证据所在章节，减少章节层级造成的关系类型误判。
- 让鉴别诊断类边进入更严格的高风险 predicate，保留 rule card 和 second-validator 约束。
- 明确记录：构图阶段不调用 LLM，LLM 只可能在前置 Markdown 证据整理阶段参与。

## 验证结果

- `python -m py_compile tools/build_wiki_native_graph_mvp.py`：通过。
- `python tools/build_wiki_native_graph_mvp.py --phase all`：通过，`build_status=pass`。
- 构图审计：`blockers=[]`，`warnings=[]`。
- DIS-059 复核：
  - `HAS_PATHOGEN`: 2
  - `HAS_DIAGNOSTIC_METHOD`: 3
  - `HAS_TRANSMISSION_ROUTE`: 2
  - `HAS_CLINICAL_SIGN`: 2
  - `HAS_CONTROL_MEASURE`: 2
  - `DIFFERENTIAL_DIAGNOSIS`: 2
  - `HAS_DRUG_BOUNDARY`: 1
  - DIS-059 共 14 条 semantic 边，全部 `verified`。

## 预计影响

- 全图会暴露更多 semantic candidate 边，因为以前未命中最具体章节的证据现在能够进入 predicate 评估。
- candidate 仍然保持 `blocked_from_runtime=true`，不会进入黄金数据集正例。
- verified 边必须继续满足 `fact_id/source_id/anchor/evidence_text/supporting_span/rule_card` 等硬条件。
