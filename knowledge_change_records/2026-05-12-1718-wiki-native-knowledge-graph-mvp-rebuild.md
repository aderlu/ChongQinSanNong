# Wiki-Native Knowledge Graph MVP Rebuild 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：17:18
- 时区：Asia/Shanghai
- 变更类型：知识图谱重构、构建脚本新增、UTF-8 防乱码治理

## 2. 修改前存在的问题

- 旧主图谱 `wiki/graph-data.json` 是 legacy runtime graph，主要由 runtime manifest、索引和事实状态表构建，不是从全部 wiki 页面原生扫描得到。
- 旧图谱更强调 page/source/rule/fact 锚点和 runtime 检索，不足以严格表达 `verified/candidate/rejected` 三层语义关系状态。
- 关系边缺少统一的 evidence support gate，难以清楚回答每条语义边是否由 `evidence_text/supporting_span/source_id/anchor` 直接支持。
- 数据更新时缺少 wiki-native 统一构建报告，无法一次性汇报新增节点、新增边、候选边、覆盖率、阻塞项和黄金数据集可用性。
- Windows PowerShell 默认编码容易造成中文显示乱码，新增脚本和报告必须显式 UTF-8 读写。

## 3. 修改前代码和知识库状态

- 旧图谱产物：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/graph-data.json`
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.md`
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.html`
- 旧构建入口主要是：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase9_rebuild_indexes_graph_smoke.py`
- 旧图谱不覆盖本次新增的 wiki-native 图谱；本次保留旧图作为 `legacy_runtime_graph`。
- 根目录此前没有 `.editorconfig`，不同编辑器或脚本写入中文文件时存在编码不一致风险。

## 4. 本次修改内容

- 新增 UTF-8 编辑约束，统一 Markdown、JSON、Python 等文本文件编码。
- 新增 wiki-native predicate registry，明确第一阶段可验证 predicate、subject/object 类型、章节模式、证据字段、rule card 和 second validator 要求。
- 新增 `build_wiki_native_graph_mvp.py`，从 wiki 页面、frontmatter、section heading、inline `fact_id/source_id/anchor` 构建统一图谱。
- 构建器输出一个统一图谱，所有关系边按 `status=verified|candidate|rejected` 区分。
- Phase C 只生成 candidate proposal，verified 只能由 validator 写入。
- 所有 verified semantic edge 必须通过 `evidence_support_check=pass`，并保留 `evidence_unit_id/source_id/anchor/evidence_text/supporting_span`。
- 对 frontmatter `sources` 中混合出现的 `SRC-* / A0-* / RC-* / RULE-* / DIS-* / SYN-*` 做引用类型识别，避免错误全部建成 `source:*`。
- 对缺页引用生成 placeholder 节点，保证图谱端点完整并保留缺页状态。

## 5. 新增文件

- `D:\XF-ChongQin\.editorconfig`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\config\wiki_native_predicate_registry.json`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_wiki_native_graph_mvp.py`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-graph.json`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_native_graph_build_report.json`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_native_graph_build_report.md`

## 6. 解决了什么问题

- 解决了旧图谱无法从全量 wiki 页面原生构建的问题。
- 解决了关系边准入缺少统一 verified/candidate/rejected 状态的问题。
- 解决了语义边无法强制绑定 evidence unit 和 supporting span 的问题。
- 解决了 candidate/rejected 数据容易丢失的问题：现在它们保留在统一图谱中，但阻止进入 runtime 和黄金数据集正例。
- 解决了 frontmatter 混合引用被误建为 source 节点导致审计 blocker 的问题。
- 增加了可用于工作汇报的构建报告，包含覆盖率、语义边统计、candidate 原因、审计结果和运行时准入规则。

## 7. 验证结果

运行命令：

```powershell
$env:PYTHONIOENCODING='utf-8'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8
py ai-\knowledge\llm_wiki_swine_authoritative\tools\build_wiki_native_graph_mvp.py --phase all
py -m py_compile ai-\knowledge\llm_wiki_swine_authoritative\tools\build_wiki_native_graph_mvp.py
py ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

构建结果：

- build_status: `pass`
- nodes: 5894
- edges: 6234
- evidence_units: 2372
- semantic edges:
  - `HAS_PATHOGEN`: 16
  - `HAS_TRANSMISSION_ROUTE`: 14
  - `HAS_CLINICAL_SIGN`: 18
  - `HAS_DIAGNOSTIC_METHOD`: 27
  - `HAS_CONTROL_MEASURE`: 22
  - `HAS_DRUG_BOUNDARY`: 1
- edge status:
  - verified: 6206
  - candidate: 28
- audit blockers: 0
- audit warnings: 0
- failed_operations: 0

编码审计结果：

- text_files_scanned: 2294
- encoding_ok: 2282
- decode_or_replacement_damage: 3
- mojibake_like_content: 0
- runtime_damaged_count: 0

说明：现有 3 个历史 decode/replacement damage 不属于本次新增 runtime 损坏；本次新增文件均使用 UTF-8 读写。

## 8. 预期效果

- 后续知识图谱更新可以通过统一图谱判断每条关系边是否真实、有效、可追溯。
- 黄金数据集正例只读取 `status=verified`、`validation_status=accepted`、`evidence_support_check=pass` 的语义边，降低幻觉边进入训练集的风险。
- 证据不足、缺 rule card 或缺 fact_id 的关系不会丢失，而是进入 candidate，用于补证、人工复核、困难题和反幻觉训练。
- 构建报告可直接用于阶段性工作汇报，说明覆盖率、缺口和下一步补证方向。

## 9. 剩余问题

- 当前语义边主要来自 section heading 与 inline evidence 的确定性映射，暂未接入复杂 LLM entailment validator。
- `uncovered_content_summary_count=1743`，说明仍有大量页面段落未形成 evidence unit，需要后续按优先级补证或增强解析。
- candidate 中有 27 条因为缺少 required rule card 未进入 verified，后续应检查页面 rule card 绑定是否需要补强。
- 目前新图谱还未接入维护总入口 `run_swine_wiki_maintenance_checks.py`，后续可作为第二阶段纳入。

## 10. 结论

本次完成 wiki-native knowledge graph 第一阶段 MVP 重构。方案保持工程轻量，一个 registry、一个构建脚本、一个统一图谱、一个构建报告；同时保持关系边正确性门槛，不允许语义边绕过 evidence support validation 直接进入 verified。旧 `wiki/graph-data.json` 未被覆盖。

