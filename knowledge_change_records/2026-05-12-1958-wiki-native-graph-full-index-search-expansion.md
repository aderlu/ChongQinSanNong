# Wiki-Native Graph Full Index Search Expansion 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：19:58
- 时区：Asia/Shanghai
- 变更类型：HTML 全量关系搜索与局部展开增强

## 2. 修改前存在的问题

- 主图为了性能采用章节分组投影，默认画布不直接显示全部原始章节节点。
- 原 wash 搜索只搜索可见节点集合，因此搜索隐藏章节节点时不会命中。
- 用户需要在视觉层搜索任意节点时，都能看到它所有相关节点和对应关系边。

## 3. 修改前代码和知识库状态

- 渲染脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`
- 主图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph.html`
- 审计图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph-audit.html`

修改前主图只画可见投影节点和边，隐藏节点关系需要打开审计图查看。

## 4. 本次修改内容

- 在主图 HTML payload 中新增 `full_index`。
- `full_index` 包含：
  - `nodes`: 全量节点索引。
  - `edges_by_node`: 任意节点的一阶全量关系边。
  - `projection_map`: 隐藏章节节点到主图章节分组节点的映射。
  - `visible_node_ids`: 当前默认画布可见节点集合。
- 向主图 HTML 注入搜索增强脚本。
- 当搜索任意节点时，底部弹出“全量关系展开”面板，显示：
  - 命中节点。
  - 该节点的一阶相关节点。
  - 对应关系边。
  - 如果命中的是隐藏章节，显示它在主图中的章节分组投影。

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph-audit.html`

## 6. 解决了什么问题

- 主图默认仍然只画轻量投影视图，不会回到全量章节卡顿状态。
- 搜索任意节点时，不再受默认可见节点限制。
- 隐藏章节节点也可以被搜索命中，并展示相关边和主图投影位置。
- 用户可以在主图中获得全量关系信息，不必一开始打开完整审计图。

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

输出结果：

- 主图：
  - visible nodes: 2164
  - visible edges: 2594
  - full_index nodes: 5902
  - hidden sections indexed: 4777
- 审计图：
  - nodes: 5902
  - edges: 6234
- 抽样隐藏章节：
  - `section:comparison:CMP-001-neonatal-diarrhea:source-citation-gate-phase-8:4`
  - sample_edges: 1
  - sample_projection: `section_group:comparison:CMP-001-neonatal-diarrhea:evidence`

编码审计结果：

- mojibake_like_content: 0
- runtime_damaged_count: 0

## 8. 预期效果

- 默认页面仍保持主图投影，打开和浏览不会像完整图那么卡。
- 搜索任意节点时，能获得该节点的完整一阶关系。
- 搜索隐藏章节时，能看到它属于哪个章节分组，并看到对应的边。
- 审计图仍保留，作为完整逐节点逐边视图。

## 9. 剩余问题

- 当前增强以底部关系面板展示全量邻居和边，尚未把隐藏节点动态注入画布绘制。
- 主图 HTML 因内嵌 full_index 变大，约 13 MB；如果后续需要更轻，可拆成外部 JSON 索引文件。
- 当前展示一阶邻居，二阶展开可作为后续增强。

## 10. 结论

本次优化实现了“默认轻量投影 + 搜索全量关系展开”。它满足主图不卡和任意节点可查全量关系两个目标，同时不改变底层 wiki-native graph 的正确性。

