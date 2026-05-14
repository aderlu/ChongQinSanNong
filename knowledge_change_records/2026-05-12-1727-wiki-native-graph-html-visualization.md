# Wiki-Native Graph HTML Visualization 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：17:27
- 时区：Asia/Shanghai
- 变更类型：知识图谱可视化 HTML 新增

## 2. 修改前存在的问题

- 旧可视化 `wiki/knowledge-graph.html` 只读取 legacy runtime graph，即 `wiki/graph-data.json`。
- 新增的 wiki-native 图谱 `wiki/wiki-native-graph.json` 还没有对应 HTML 可视化，无法直观看到 `verified/candidate/rejected` 边、证据单元、语义对象和新图节点。
- 若直接覆盖旧 HTML，会混淆 legacy runtime graph 和 wiki-native graph 的用途边界。

## 3. 修改前代码和知识库状态

- 旧 HTML 渲染脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wash_interactive_graph.py`
- 旧 HTML 输出：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.html`
- 新图谱已有：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-graph.json`
  - `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_native_graph_build_report.json`

旧渲染脚本依赖 `llm-wiki-skill-main/templates/graph-styles/wash` 的 header/footer 模板和 `graph-wash.js` 等静态资源。新可视化沿用该格式，保证风格和交互一致。

## 4. 本次修改内容

- 新增 `render_wiki_native_graph.py`，专门把 `wiki-native-graph.json` 映射为现有 wash HTML 格式。
- 新 HTML 输出为 `wiki/wiki-native-knowledge-graph.html`，不覆盖旧 `wiki/knowledge-graph.html`。
- 节点映射：
  - disease/drug/comparison/syndrome/synthesis/rule_card/rule/topic 映射为 topic。
  - source/evidence_unit 映射为 source。
  - literal_span/section/fact 映射为 entity。
- 边映射：
  - `status=verified` 映射为 EXTRACTED。
  - `status=candidate` 映射为 INFERRED。
  - `status=rejected` 映射为 LOW_CONFIDENCE。
- HTML 内嵌 change_log，说明新图谱来源、证据准入规则、semantic_by_predicate 和 candidate_reasons。

## 5. 新增文件

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`

## 6. 解决了什么问题

- 解决了新 wiki-native 图谱无法可视化的问题。
- 解决了旧图和新图展示混用的问题：旧图继续使用 `knowledge-graph.html`，新图使用 `wiki-native-knowledge-graph.html`。
- 让工作汇报可以直观看到新图谱节点、边、状态、证据来源和候选原因。
- 可视化保留了原有 HTML 的整体风格、布局、交互脚本和静态资源。

## 7. 验证结果

运行命令：

```powershell
$env:PYTHONIOENCODING='utf-8'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8
py ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py
py -m py_compile ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py
py ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

生成结果：

- HTML: `wiki/wiki-native-knowledge-graph.html`
- nodes: 5902
- edges: 6234
- style: `llm-wiki-skill wash`
- source: `wiki/wiki-native-graph.json`

HTML 文件检查：

- 文件大小约 8.1 MB。
- 标题包含 `猪病 LLM Wiki · Wiki-Native Knowledge Graph`。
- HTML 内含中文节点内容，例如药物、疾病和证据相关说明。
- HTML 内含 `verified/candidate` 等边状态信号。

编码审计结果：

- text_files_scanned: 2295
- encoding_ok: 2283
- decode_or_replacement_damage: 3
- mojibake_like_content: 0
- runtime_damaged_count: 0

说明：本次新增 HTML 和脚本未引入乱码；现存 3 个 decode/replacement damage 是历史文件，且不属于 runtime damaged。

## 8. 预期效果

- 可以直接打开 `wiki/wiki-native-knowledge-graph.html` 查看新图谱。
- 汇报时可以同时说明旧图和新图：旧图服务 legacy runtime，新图服务证据可验证的 wiki-native graph。
- 后续如果 wiki-native graph 更新，只需重新运行 `render_wiki_native_graph.py` 即可刷新 HTML。

## 9. 剩余问题

- 当前 HTML 复用原 wash 交互组件，尚未针对 `verified/candidate/rejected` 增加专门筛选按钮。
- 当前 HTML 内嵌全量图谱数据，文件较大；后续如需要可增加按节点类型或状态裁剪的轻量视图。
- 当前布局使用确定性螺旋初始坐标，后续可按社区或边类型做更细的初始分区。

## 10. 结论

本次完成 wiki-native graph 的新 HTML 可视化构建。它保留旧 HTML 的视觉和交互格式，但数据源切换为 `wiki/wiki-native-graph.json`，并独立输出为 `wiki/wiki-native-knowledge-graph.html`，不会影响 legacy runtime graph 的展示。

