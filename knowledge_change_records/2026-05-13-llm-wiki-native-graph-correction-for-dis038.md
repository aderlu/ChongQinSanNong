# 2026-05-13 DIS-038 图谱基准纠偏记录

## 纠偏背景

- 本次 `DIS-038` 猪布鲁氏菌病 CFSPH 数据补充后，最初误将以下链路当成“主知识图谱”进行汇报：
  - `wiki/graph-data.json`
  - `wiki/knowledge-graph.html`
- 用户指出正确基准应严格参考：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`

## 正确的图谱分层

### 1. legacy runtime graph

- 文件：
  - `wiki/graph-data.json`
  - `wiki/knowledge-graph.html`
- 特点：
  - 以 runtime provenance 为核心
  - 主要表达 page/source/rule/fact anchor
  - 用于兼容层、运行时索引、规则门禁和现有维护检查链

### 2. wiki-native 主图谱

- 文件：
  - `wiki/wiki-native-graph.json`
  - `wiki/wiki-native-knowledge-graph.html`
  - `wiki/wiki-native-knowledge-graph-audit.html`
- 特点：
  - 从 wiki 页面正文重新扫描构建
  - 主体是 section、evidence_unit、semantic edge
  - 只有满足 `fact_id + source_id + anchor + evidence_text + supporting_span` 等约束的证据单元，才能形成 verified 语义边
  - 这是当前项目真正的主知识图谱

## 本次误判原因

- `run_guarded_wiki_update.py` 和 `run_swine_wiki_maintenance_checks.py` 默认跑的是 legacy runtime graph 验收链。
- 因此我在第一次汇报中用了：
  - `issues/graph_change_diff_last.json`
  - `wiki/knowledge-graph.html`
  - `wiki/graph-data.json`
- 这些结果说明 runtime 兼容层已经更新成功，但它们不能代表 wiki-native 主图谱已经同步变化。

## 本次纠偏后的真实修复动作

### 修复 1：补齐 DIS-038 页面中 wiki-native 所需的 `anchor=`

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\diseases\DIS-038-brucella-suis-brucellosis.md`
- 补齐对象：
  - `DIS038-WEB-001`
  - `DIS038-WEB-002`
  - `DIS038-WEB-003`
  - `DIS038-WEB-004`
  - `DIS038-WEB-005`
  - `DIS038-WEB-006`
  - `DIS038-WEB-007`
- 原因：
  - wiki-native 图谱不会从 `knowledge_facts.json` 自动投影 semantic edge
  - 它直接扫描 disease 页面正文中的 `fact_id / source_id / anchor`
  - 没有 `anchor=` 的条目不会成为合格的 verified evidence unit

### 修复 2：重建 wiki-native 主图谱

- 执行命令：
  - `tools/build_wiki_native_graph_mvp.py`
  - `tools/render_wiki_native_graph.py`
- 结果文件：
  - `wiki/wiki-native-graph.json`
  - `wiki/wiki-native-knowledge-graph.html`
  - `wiki/wiki-native-knowledge-graph-audit.html`

## 修前修后主图谱差分

### 修前快照

- 已保留修前主图谱快照：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\graph_snapshots\wiki-native-graph-before-dis038-20260513-2238.json`

### 修后结果摘要

- 主图谱节点：
  - `6054 -> 6067`
- 主图谱边：
  - `6397 -> 6410`
- 新增节点：
  - `13`
- 新增边：
  - `16`
- 变更节点：
  - `3`

## DIS-038 在 wiki-native 主图谱中的真实变化

### 新增节点

- 新增 disease section 节点：
  - `section:disease:DIS-038:authority-web-refresh-2026-05-13:87`
  - `section:disease:DIS-038:transmission-and-exposure-boundary:91`
  - `section:disease:DIS-038:clinical-pattern-boundary:95`
  - `section:disease:DIS-038:zoonotic-public-health-boundary:99`
  - `section:disease:DIS-038:enforcement-boundary:103`
- 新增 source 节点：
  - `source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`
- 新增 source section 节点：
  - `section:source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026:source:4`
  - `section:source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026:usable-boundary:13`
  - `section:source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026:do-not-extrapolate-boundary:18`
  - `section:source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026:可支持结论:23`
  - `section:source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026:不得外推边界:27`
- 新增 semantic object：
  - `semantic_object:222c13b49a52f4f6`
  - `semantic_object:ce45dbdbb5e050fc`

### 新增 verified 语义边

- `DIS038-WEB-005` 成功进入主图谱：
  - `disease:DIS-038 -> semantic_object:ce45dbdbb5e050fc`
  - predicate: `HAS_TRANSMISSION_ROUTE`
  - status: `verified`
  - source: `A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`
- `DIS038-WEB-006` 成功进入主图谱：
  - `disease:DIS-038 -> semantic_object:222c13b49a52f4f6`
  - predicate: `HAS_CLINICAL_SIGN`
  - status: `verified`
  - source: `A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`

### 新增 source 引用边

- `disease:DIS-038 -> source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`
  - predicate: `CITES_SOURCE`
  - status: `verified`

## DIS-038 当前仍未成为 verified 的部分

### DIS038-WEB-007

- 该条是公共卫生暴露边界，但当前 predicate registry 中没有专门的“public-health exposure boundary” predicate。
- 因此本次不会自动生成对应 verified semantic edge。
- 这不代表数据无效，而是说明当前 wiki-native predicate registry 的覆盖范围尚未扩到这一类边。

### DIS038-WEB-003

- 该条被识别为 `HAS_DIAGNOSTIC_METHOD`
- 当前状态：`candidate`
- 原因：`missing_required_rule_card`
- 说明：
  - wiki-native 图谱对诊断类 semantic edge 要求 `RC-DX-001`
  - 当前 `DIS-038` frontmatter sources 中没有该规则卡
  - 因此该边不能升级为 verified

### 教材诊断 bullet

- 当前也存在 1 条 `HAS_DIAGNOSTIC_METHOD` candidate
- 原因：`missing_fact_id`
- 说明：
  - 该条正文已有 source 与 anchor，但没有结构化 `fact_id`
  - 所以只能留在 candidate

## 纠偏后的结论

- 之前关于“图谱已经变化”的说法，如果指的是 legacy runtime graph，是成立的。
- 但如果严格指向项目主知识图谱 `wiki-native-knowledge-graph.html`，之前的表达不准确。
- 纠偏并重建后，可以确认：
  - `DIS-038` 的 CFSPH 补充已经真实进入 wiki-native 主图谱
  - 至少新增了 1 个 source 节点、5 个 disease section 节点、5 个 source section 节点、2 个 semantic object
  - 至少新增了 2 条 verified 语义边：
    - 传播边界
    - 临床表现边界

## 这次纠偏的意义

- 澄清了企业级项目中两套图谱链的职责边界：
  - legacy runtime graph 负责兼容层与运行时 provenance
  - wiki-native graph 才是主知识图谱
- 修正了 `DIS-038` 页面与 wiki-native semantic edge 契约不一致的问题
- 让后续所有“知识图谱是否变化”的判断都能回到正确基准

## 后续建议

- 若希望 `DIS038-WEB-007` 这类公共卫生暴露边界进入主图谱 verified semantic edge：
  - 需要扩展 `config/wiki_native_predicate_registry.json`
  - 新增适用于 public-health / zoonotic exposure 的 predicate
- 若希望 `DIS038-WEB-003` 的诊断边界升级为 verified：
  - 需要将 `RC-DX-001` 纳入 `DIS-038` 的 frontmatter sources
- 若希望主图谱更新也像 legacy 图谱一样自动纳入维护检查：
  - 需要把 native build/render/diff 检查纳入受控更新后的 post-check 链
