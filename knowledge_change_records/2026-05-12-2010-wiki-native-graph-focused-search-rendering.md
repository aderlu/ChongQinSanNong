# Wiki-Native Graph Focused Search Rendering 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：20:10
- 时区：Asia/Shanghai
- 变更类型：HTML 搜索聚焦渲染增强

## 2. 修改前存在的问题

- 上一版搜索能弹出“全量关系展开”面板，但画布本身仍显示默认主图投影。
- 用户希望搜索任意节点后，不只是看到文字面板，还要在渲染页面中展示命中节点、相关节点和对应边。
- 用户还希望搜索聚焦时屏蔽其他节点和边，避免局部关系被主图背景干扰。

## 3. 修改前代码和知识库状态

- 渲染脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`
- 主图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph.html`
- 审计图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph-audit.html`

修改前已有 `full_index` 和底部关系面板，但没有在画布层动态绘制搜索命中的全量一阶关系。

## 4. 本次修改内容

- 在主图 HTML 注入聚焦渲染增强脚本。
- 搜索命中节点后：
  - 原主图节点和边临时弱化并屏蔽交互。
  - 画布中央绘制命中节点。
  - 围绕命中节点绘制全量一阶相关节点。
  - 绘制这些节点之间的对应关系边。
  - 如果命中隐藏章节，优先参考它的章节分组投影进行定位。
- 底部“全量关系展开”面板继续保留，展示详细节点和边清单。
- 点击“收起”、清空搜索、点击适配视图或按 Escape 可恢复主图。

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph-audit.html`

## 6. 解决了什么问题

- 搜索结果不再只是文字面板，而是在画布中形成局部关系图。
- 搜索聚焦时会弱化其他节点和边，避免视觉干扰。
- 隐藏章节也能通过 full_index 命中，并在画布上作为聚焦节点展示。
- 保留主图轻量投影，不需要默认全量渲染 5902 个节点。

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
- 审计图：
  - nodes: 5902
  - edges: 6234

HTML 检查：

- 已注入 `full-index-overlay-node`。
- 已注入 `full-index-overlay-edge`。
- 已注入 `drawFocusOverlay`。
- 已注入 `full-index-focus-active` 视觉屏蔽样式。

编码审计结果：

- mojibake_like_content: 0
- runtime_damaged_count: 0

## 8. 预期效果

- 搜索任意节点后，用户可以直接在画布上看到该节点的一阶全量关系。
- 其他节点和边被临时屏蔽，局部关系更清晰。
- 底部面板提供文字审计信息，画布提供视觉关系。
- 默认图仍保持轻量，不回退到全量渲染导致卡顿。

## 9. 剩余问题

- 当前聚焦渲染展示一阶关系，二阶关系仍需后续增强。
- 当前聚焦节点布局为脚本生成的局部布局，不参与原 D3/rough 完整布局。
- 如果某个节点一阶邻居过多，当前最多绘制前 120 条边，避免再次卡顿。

## 10. 结论

本次优化实现了“搜索即局部全量可视化”。用户搜索任意节点后，主图会临时切换为局部关系视图，展示命中节点、相关节点和对应边，并屏蔽其他节点和边，从而兼顾全量关系可见性和默认页面性能。

