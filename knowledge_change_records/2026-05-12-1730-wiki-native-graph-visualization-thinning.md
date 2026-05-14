# Wiki-Native Graph Visualization Thinning 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：17:30
- 时区：Asia/Shanghai
- 变更类型：知识图谱可视化瘦身优化

## 2. 修改前存在的问题

- 新版 wiki-native 图谱中章节节点约 4777 个，整体图谱 HTML 首屏渲染和交互明显卡顿。
- 虽然章节节点对关系判定有用，但在默认可视化里并不需要全部同时展示。
- 若直接删除章节节点，会影响图谱正确性、证据追溯和后续审计，因此不能做知识层削减。

## 3. 修改前代码和知识库状态

- 可视化脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`
- 可视化 HTML：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph.html`
- 新图谱数据：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-graph.json`

原先默认可视化直接渲染全部 nodes 和 edges，章节节点、章节边全部进入默认视图，导致节点数和边数过大。

## 4. 本次修改内容

- 保留 wiki-native 图谱 JSON 的完整章节节点和章节边，不改知识层。
- 修改 `render_wiki_native_graph.py`，在可视化层默认隐藏 `section` 节点和 `HAS_SECTION` 边。
- 仍然保留章节信息在节点内容与构建报告中，确保需要时可追溯。
- 将默认可视化视图减少为疾病、药物、来源、规则卡、综合页、语义对象等主干节点。
- 可视化 HTML 仍复用原有 wash 风格和静态资源，不重写整套前端。

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`

## 6. 解决了什么问题

- 默认可视化节点数从 5902 降至 1125。
- 默认可视化边数从 6234 降至 1457。
- 页面首屏与交互流畅性显著改善。
- 不牺牲知识图谱正确性，因为章节节点仍保留在 JSON 中，不影响验证、追溯和黄金数据集准入。

## 7. 验证结果

运行命令：

```powershell
$env:PYTHONIOENCODING='utf-8'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8
py ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py
py -m py_compile ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py
```

结果：

- HTML 输出成功：`wiki/wiki-native-knowledge-graph.html`
- 默认可视化节点数：1125
- 默认可视化边数：1457
- 仍保持 HTML 中的中文展示和 wash 风格

编码检查：

- 本次修改未引入可见乱码。

## 8. 预期效果

- 新图谱 HTML 打开和拖拽会明显更顺。
- 工作汇报和人工审阅时，先看主干节点和 verified/candidate/rejected 边，不会被章节节点淹没。
- 若后续需要章节级审计，可以在图中再逐步展开，而不是默认全量展示。

## 9. 剩余问题

- 默认视图仍保留较多主干节点，极端低性能设备上仍可能偏重。
- 章节节点虽被隐藏，但仍在 HTML 数据里；如果后续要做更轻量页面，可进一步拆分为“主视图”和“审计视图”。

## 10. 结论

本次优化属于展示层瘦身，不改变知识层正确性。章节节点仍完整保留在 wiki-native 图谱中，但默认 HTML 不再直接渲染全部章节节点和章节边，从而显著缓解卡顿。

