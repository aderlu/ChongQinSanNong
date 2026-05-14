# Wiki-Native Graph Draggable Nodes 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：20:16
- 时区：Asia/Shanghai
- 变更类型：HTML 节点拖拽交互增强

## 2. 修改前存在的问题

- 图谱节点较多时，部分节点会互相遮挡。
- 用户无法把被遮住的节点拖出来检查。
- 如果只移动节点而不重绘边，会导致视觉上关系边断开或指向旧位置。

## 3. 修改前代码和知识库状态

- 渲染脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`
- 主图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph.html`
- 审计图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph-audit.html`

修改前已有搜索聚焦视图和全量关系面板，但节点不可手动拖拽。

## 4. 本次修改内容

- 在主图 HTML 注入通用节点拖拽脚本。
- 默认主图节点 `.node` 支持拖动。
- 搜索聚焦后生成的 `.full-index-overlay-node` 也支持拖动。
- 拖动默认主图节点时，实时重算并更新与该节点相关的主图边路径。
- 拖动搜索聚焦节点时，实时重算并更新对应聚焦关系边路径。
- 拖动过程中节点增加 `is-dragging` 样式，提升可见性和交互反馈。

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph-audit.html`

## 6. 解决了什么问题

- 被遮挡的节点可以被拖出查看。
- 拖动节点时，关联边会同步更新，不会出现视觉断边。
- 搜索聚焦视图中的局部关系网络也可手动整理。
- 不改变底层 wiki-native 图谱数据，只增强 HTML 交互。

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

HTML 检查：

- 已注入 `makeNodeDraggable`。
- 已注入 `updateMainGraphEdgesForNode`。
- 已注入 `updateOverlayEdgesForNode`。
- 已注入 `data-drag-enabled` 和 `is-dragging` 样式。

编码审计结果：

- mojibake_like_content: 0
- runtime_damaged_count: 0

## 8. 预期效果

- 用户可以在主图中拖动任意可见节点，整理重叠区域。
- 用户可以在搜索聚焦视图中拖动命中节点和相关节点，检查被遮挡的局部关系。
- 拖动过程中相关边保持连接，提高视觉核查体验。

## 9. 剩余问题

- 拖动位置目前只存在于当前浏览会话，没有保存回文件。
- 审计全图节点较多，虽然也具备拖拽脚本，但打开和操作仍会比主图重。
- 后续可考虑增加“保存布局”或“重置布局”按钮。

## 10. 结论

本次优化为 wiki-native HTML 图谱增加了节点拖拽能力，并保证拖动时相关关系边同步重绘。它解决了节点遮挡导致难以检查的问题，同时保持底层知识图谱不变。

