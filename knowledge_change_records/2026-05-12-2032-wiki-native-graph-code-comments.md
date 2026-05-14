# Wiki-Native Graph Code Comments 变更记录

## 1. 落地时间

- 日期：2026-05-12
- 时间：20:32
- 时区：Asia/Shanghai
- 变更类型：核心代码注释补充

## 2. 修改前存在的问题

- 新图谱构建和 HTML 渲染逻辑已经实现，但关键函数缺少解释。
- 后续维护人员不容易快速理解：
  - 为什么不读取旧 `graph-data.json` 作为主输入。
  - evidence_unit 如何产生。
  - semantic edge 如何从 candidate 升级到 verified。
  - 为什么主图隐藏 section，但又能搜索隐藏节点。
  - 节点拖动时为什么边不会断。

## 3. 修改前代码和知识库状态

- 图谱构建脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_wiki_native_graph_mvp.py`
- HTML 渲染脚本：
  - `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py`

两个脚本此前可以运行，但注释偏少，不利于工作交接和代码审计。

## 4. 本次修改内容

- 为 `build_wiki_native_graph_mvp.py` 增加关键注释，覆盖：
  - 输入目录到节点类型映射。
  - 不读取旧 `graph-data.json` 的原因。
  - frontmatter 解析策略。
  - section 节点的作用。
  - inline fact/source/anchor 抽取逻辑。
  - reference 节点类型识别。
  - predicate 选择只是 candidate proposal。
  - evidence_unit 是语义边事实来源。
  - literal_span 语义对象用于降低实体误连风险。
  - semantic edge 准入验证。
  - audit blocker 的作用。
- 为 `render_wiki_native_graph.py` 增加关键注释，覆盖：
  - section_group 是视觉层分组，不是知识层合并。
  - 主图和审计图的区别。
  - full_index 的用途。
  - 搜索 full_index 而非只搜可见节点。
  - 局部聚焦视图如何屏蔽其他节点。
  - 节点拖拽如何重绘主图边和聚焦边。

## 5. 新增或修改文件

- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_wiki_native_graph_mvp.py`
- 修改：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py`
- 重新生成：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html`
- 重新生成：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph-audit.html`

## 6. 解决了什么问题

- 提高代码可读性。
- 降低后续维护和二次开发成本。
- 方便向他人解释新图谱如何防止幻觉边。
- 方便排查 HTML 可视化中 full_index、章节分组、搜索聚焦和拖拽边重绘逻辑。

## 7. 验证结果

运行命令：

```powershell
$env:PYTHONIOENCODING='utf-8'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8
py -m py_compile ai-\knowledge\llm_wiki_swine_authoritative\tools\build_wiki_native_graph_mvp.py ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py
py ai-\knowledge\llm_wiki_swine_authoritative\tools\render_wiki_native_graph.py
py ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

结果：

- Python 编译通过。
- HTML 重新生成成功。
- 主图 nodes: 2164。
- 主图 edges: 2594。
- 审计图 nodes: 5902。
- 审计图 edges: 6234。
- 编码审计：
  - mojibake_like_content: 0
  - runtime_damaged_count: 0

## 8. 预期效果

- 后续继续优化知识图谱时，可以直接从注释理解构建链路。
- 审计关系边是否准确时，可以快速定位 validator 和 evidence_unit 逻辑。
- 维护 HTML 交互时，可以快速定位 full_index、局部聚焦、拖拽和边重绘逻辑。

## 9. 剩余问题

- 注释只覆盖核心逻辑，不是完整开发手册。
- 后续如果继续扩展 second validator 或动态二阶展开，需要继续同步补充注释。

## 10. 结论

本次变更补充了 wiki-native 图谱构建和可视化核心代码注释，不改变功能行为。代码通过编译和编码审计，HTML 已重新生成。

