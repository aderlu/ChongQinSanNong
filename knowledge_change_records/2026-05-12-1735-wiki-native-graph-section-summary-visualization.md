# Wiki-Native Graph Section Summary Visualization 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：17:35
- 时区：Asia/Shanghai
- 变更类型：知识图谱视觉层结构优化

## 2. 修改前存在的问题

- 章节节点数量太多，直接全量展示会让 HTML 图谱页面卡顿。
- 如果简单隐藏章节节点，视觉上会让“页面 -> 章节 -> 证据 -> 语义边”的桥断掉，用户会感觉图谱关系变弱。
- 但如果真的删除章节节点，又会影响知识层正确性和证据追溯。

## 3. 修改前代码和知识库状态

- 可视化脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`
- 可视化输出：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph.html`
- 新图谱 JSON：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-graph.json`

原方案是隐藏 `section` 节点和 `HAS_SECTION` 边，虽然能减轻卡顿，但会弱化视觉上的章节桥接感。

## 4. 本次修改内容

- 保留章节节点在 `wiki-native-graph.json` 中完整存在，不改知识层。
- 在视觉层把大量 `section` 节点折叠为 `section_summary` 节点。
- 为每个页面生成一个章节摘要节点，记录该页面章节数和前几个章节标题。
- 增加 `HAS_SECTION_SUMMARY` 边，把页面连接到章节摘要节点，保留视觉上的章节桥接。
- 默认视图中不再展示 4777 个原始章节节点，而是展示更少的摘要节点。

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 更新：`D:\XF-ChongQin\ai-knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`

## 6. 解决了什么问题

- 默认图谱节点从 1125 增加到 1460，但保留了章节桥接结构，不再是纯隐藏。
- 默认图谱边从 1457 增加到 1792，但仍远低于 6234 的全量展示规模。
- 视觉上保留“页面-章节-证据-语义边”的关系感，避免用户感觉两个有联系的节点被断开。
- 仍然不影响图谱的正确性，因为原始章节节点和章节边都保留在 JSON 中。

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
- 默认视觉节点数：1460
- 默认视觉边数：1792
- HTML 仍保持 wash 风格

## 8. 预期效果

- 页面比全量章节展示更流畅。
- 视觉上比纯隐藏章节更自然，不会把知识桥切断。
- 需要审计时仍可回到 `wiki-native-graph.json` 查看完整章节节点。

## 9. 剩余问题

- 摘要节点仍然是折叠层，不等同于完整章节逐条展开。
- 如果后续要进一步提升性能，可以按页面类型或边状态再做二级过滤。

## 10. 结论

本次优化在知识层不变的前提下，对章节节点做了视觉折叠。它比“纯隐藏章节”更能保留关系桥，比“全量章节展示”更流畅，适合作为新图谱的默认展示方式。

