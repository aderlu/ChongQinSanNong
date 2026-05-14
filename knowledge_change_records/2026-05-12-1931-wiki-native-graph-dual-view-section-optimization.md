# Wiki-Native Graph Dual View Section Optimization 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：19:31
- 时区：Asia/Shanghai
- 变更类型：知识图谱 HTML 双视图与章节摘要增强

## 2. 修改前存在的问题

- 原始章节节点数量为 4777，直接全量展示会造成 HTML 图谱卡顿。
- 单纯隐藏章节节点会让用户在视觉层面感觉关系桥断开。
- 章节摘要节点已经能缓解问题，但摘要内容不够充分，且没有单独的完整章节审计视图。

## 3. 修改前代码和知识库状态

- 渲染脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`
- 默认 HTML：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph.html`
- 数据源：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-graph.json`

修改前只有一个默认 HTML，章节采用摘要节点表达，但无法同时满足“默认流畅查看”和“完整章节审计”两个需求。

## 4. 本次修改内容

- 将 HTML 输出拆成两个视图：
  - 主干摘要视图：`wiki/wiki-native-knowledge-graph.html`
  - 完整章节审计视图：`wiki/wiki-native-knowledge-graph-audit.html`
- 主干摘要视图继续折叠章节节点，只展示 `section_summary` 节点。
- 审计视图展示完整 `section` 节点和 `HAS_SECTION` 边，用于逐章追溯。
- 增强 `section_summary` 内容：
  - 记录页面章节总数。
  - 展示最多 24 个章节标题。
  - 如果还有更多章节，显示省略数量。
- HTML metadata 增加 `visual_mode`、`full_nodes`、`full_edges`、`hidden_nodes`、`hidden_edges`。

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`
- 新增：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph-audit.html`

## 6. 解决了什么问题

- 默认查看不再被 4777 个章节节点拖慢。
- 视觉层仍保留章节摘要桥，避免关系看起来被切断。
- 需要完整审计时，可以打开审计视图查看全部章节节点。
- 不改变 `wiki-native-graph.json`，因此知识层正确性和证据追溯不受影响。

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

- 主干摘要视图：
  - HTML: `wiki/wiki-native-knowledge-graph.html`
  - nodes: 1460
  - edges: 1792
- 完整章节审计视图：
  - HTML: `wiki/wiki-native-knowledge-graph-audit.html`
  - nodes: 5902
  - edges: 6234

编码审计结果：

- mojibake_like_content: 0
- runtime_damaged_count: 0

## 8. 预期效果

- 日常查看使用主干摘要视图，页面更流畅。
- 汇报时可说明默认视图是性能优化后的摘要图。
- 审计或排查关系路径时打开完整章节审计视图，保留全部章节细节。
- 章节摘要节点能直接展示页面章节结构，不再只是空代理。

## 9. 剩余问题

- 两个视图目前是两个 HTML 文件，不是在同一页面内按钮切换。
- 审计视图仍然较大，打开时会比主干摘要视图慢。
- 后续可以进一步按节点类型、边状态或单个页面做局部展开。

## 10. 结论

本次优化把章节展示从单一折叠方案升级为双视图方案。默认主图解决性能和可读性，审计图保留完整章节结构，兼顾“知识图谱拿来看”和“知识图谱要可验证”两个目标。

