# Wiki-Native Graph Section Group Traceability 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：19:43
- 时区：Asia/Shanghai
- 变更类型：章节分组可追溯视图优化

## 2. 修改前存在的问题

- 完整章节节点直接展示会造成图谱卡顿。
- 简单章节摘要虽然变轻，但只是页面级摘要，不能充分表达“具体语义关系属于哪类大章节”。
- 用户需要在视觉层看到完整关系桥，同时仍能定位到原始章节标题和行号。

## 3. 修改前代码和知识库状态

- 渲染脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`
- 主视图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph.html`
- 审计视图：
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/wiki-native-knowledge-graph-audit.html`

修改前主视图使用 `section_summary` 作为页面级章节摘要，能减少卡顿，但语义分组和具体定位能力不足。

## 4. 本次修改内容

- 将 `section_summary` 升级为 `section_group`。
- 按章节标题语义把原始章节分到固定大类：
  - 病原/分类
  - 传播/流行
  - 临床/表现
  - 剖检/病变
  - 诊断/检测
  - 鉴别诊断
  - 防控/控制
  - 用药/处置边界
  - 监管/执行边界
  - 来源/证据/可用性
  - 其他章节
- 每个 `section_group` 节点保留：
  - `section_count`
  - `section_titles`
  - `section_refs`
  - 原始 `section_id`
  - `line_start`
  - `line_end`
- 增加视觉边：
  - `页面 -> HAS_SECTION_GROUP -> 章节分组`
  - `章节分组 -> SECTION_GROUP_SUPPORTS_SEMANTIC_OBJECT -> 语义对象`

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`
- 更新：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph-audit.html`

## 6. 解决了什么问题

- 主视图不再只是隐藏或简单摘要章节，而是保留语义大类桥接。
- 点击章节分组节点可以看到原始章节标题和行号定位。
- 语义对象可通过视觉边回连到对应章节分组，关系路径更完整。
- 知识层仍保留全部原始章节节点，不做破坏性合并。

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

- 主干章节分组视图：
  - HTML: `wiki/wiki-native-knowledge-graph.html`
  - nodes: 2164
  - edges: 2594
- 完整章节审计视图：
  - HTML: `wiki/wiki-native-knowledge-graph-audit.html`
  - nodes: 5902
  - edges: 6234

编码审计结果：

- mojibake_like_content: 0
- runtime_damaged_count: 0

## 8. 预期效果

- 日常查看时，用户能看到页面、章节分组、语义对象之间的完整关系桥。
- 章节分组节点比 4777 个原始章节轻很多，页面仍可流畅打开。
- 需要审计时可通过章节分组中的 `section_refs` 定位到原始章节和行号。
- 完整章节审计视图仍保留全部原始章节节点。

## 9. 剩余问题

- 当前章节分组基于标题关键词，部分非标准标题可能进入“其他章节”。
- 后续可根据 predicate registry 进一步优化章节分组映射。
- 当前仍是两个 HTML 文件，尚未做同页动态展开。

## 10. 结论

本次优化采用“知识层保留原始章节、视觉层展示章节分组”的方案。它不是破坏性合并章节，而是在视觉层建立可追溯的大章节节点，兼顾可读性、性能和关系追溯完整性。

