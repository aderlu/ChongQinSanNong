# 图谱 HTML 右侧更新日志面板改造说明

## 1. 本次修改目标

本次修改目标是将猪病 LLM Wiki 图谱 HTML 右侧面板从“节点详情/来源详情”调整为“知识图谱更新日志”，用于现场对比更新前后知识图谱的可视化结果，并说明本轮变化部分及其合理性。

用户希望当前三栏式 HTML 中，右侧区域不再主要展示单个节点详情，而是展示每次图谱更新后的审计信息，包括节点、边、事实、CRUD 变化和合理性说明。

## 2. 修改前存在的问题

修改前的 HTML 右侧面板由 `graph-wash.js` 的 `renderDrawer` 和 `renderKnowledgeCard` 控制，主要逻辑是：

- 未选中节点时显示推荐起点或空状态。
- 选中节点时显示节点标题、摘要、正文、相邻节点和来源按钮。
- 右侧内容随当前选中节点变化。

这种设计适合知识阅读，但不适合汇报“图谱更新前后发生了什么变化”。在演示图谱更新时，用户需要看到的是：

- 更新前后节点数量变化。
- 更新前后关系数量变化。
- 本轮新增、删除、修改了哪些节点和边。
- CRUD 统计是什么。
- 变化是否合理，是否来自受控 source/fact 入库。
- 是否存在覆盖或删除旧数据。

原右侧面板不能稳定承载这些信息。

## 3. 本次修改内容

### 3.1 增加图谱更新日志 payload

修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wash_interactive_graph.py`

新增读取来源：

- `issues/graph_change_diff_last.json`
- `issues/wiki_crud_change_log.jsonl`

新增逻辑：

- `load_json`
- `load_recent_crud_events`
- `build_change_log_payload`

新增输出字段：

- `change_log`

`change_log` 包含：

- `generated_at`
- `title`
- `subtitle`
- `summary`
- `crud_counts`
- `added_nodes`
- `added_links`
- `removed_nodes`
- `changed_nodes`
- `recent_crud_events`
- `reasonableness`
- `evidence_files`

### 3.2 改造右侧面板显示逻辑

修改文件：

- `llm-wiki-skill-main/templates/graph-styles/wash/graph-wash.js`

新增逻辑：

- `formatSignedNumber`
- `renderChangeList`
- `renderCrudCounts`
- `renderGraphChangeLog`

调整逻辑：

- `renderDrawer` 固定调用 `renderGraphChangeLog`。
- 右侧标题改为“图谱更新日志”。
- 右侧摘要显示节点、关系前后数量和变化量。
- 正文显示更新前后对比、CRUD 统计、新增节点示例、新增关系示例、合理性说明和证据文件。
- 右侧按钮从“加入学习队列/查看来源”调整为“查看变更日志/打开变化页”。
- “打开变化页”跳转到 `knowledge-graph-changes.html`。

### 3.3 重建猪病图谱 HTML

执行：

- `python ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wash_interactive_graph.py`

生成并更新：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.html`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/graph-wash.js`

当前图谱渲染结果：

- 节点：2569
- 关系：3151

### 3.4 更新 DIS-045 快照

同步更新：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/DIS-045-graph-html-snapshots/graph-wash.js`

新增/刷新：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/DIS-045-graph-html-snapshots/DIS-045-after-knowledge-graph.html`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/DIS-045-graph-html-snapshots/DIS-045-after-knowledge-graph-changes.html`

其中 after HTML 已内嵌 `change_log`，包括 `delta_nodes: 14` 和本轮合理性说明。

## 4. 解决的问题

本次修改解决了以下问题：

- 右侧面板可以直接展示本轮图谱更新日志。
- 用户可以在同一个 HTML 页面中查看图谱可视化和更新原因。
- 更新前后节点、关系数量变化可以直接展示。
- CRUD diff、source/fact 新增和关系新增可以直接展示。
- 合理性说明直接进入 HTML，便于向 leader 解释为什么这些节点和边被新增。
- 点击节点仍会影响中间图谱高亮，但右侧保持更新日志，不会被单个节点详情覆盖。

## 5. 数据合理性说明

当前 `change_log` 显示本轮 DIS-045 更新：

- 节点从 2555 增加到 2569。
- 关系从 3135 增加到 3151。
- 新增节点 14 个。
- 新增关系 16 条。
- CRUD 统计为新增 fact 8 个，新增 source 6 个。
- 没有删除节点、删除关系或修改既有节点。

这些变化来自受控入库后的 source/fact 注册：

- 新增事实节点通过 `fact_anchor` 连接到 `DIS-045` 疾病页。
- 新增事实节点通过 `evidence_source` 连接到来源节点。
- 未出现删除，说明既有知识未被覆盖。

## 6. 本次未修改的内容

本次没有修改知识事实本身，没有新增或删除 source/fact 数据，也没有改变 DIS-045 的医学结论。

本次修改属于图谱 HTML 展示层和渲染 payload 层改造，目标是让已有 diff、CRUD 和图谱变化更适合汇报展示。

## 7. 验证结果

已完成以下验证：

- `render_wash_interactive_graph.py` 通过 `py_compile`。
- `graph-wash.js` 通过 `node --check`。
- 成功重建 `wiki/knowledge-graph.html`。
- 生成结果显示节点 2569、关系 3151。
- `knowledge-graph.html` 中已包含 `change_log`。
- `knowledge-graph.html` 中已包含 `title: 图谱更新日志`、`delta_nodes: 14` 和合理性说明。
- `wiki/graph-wash.js` 中已包含 `renderGraphChangeLog`。
- DIS-045 after 快照已生成，并包含 `change_log`。
- 检查常见乱码信号，未发现异常标记；医学术语中的正常中文字符不作为乱码处理。

## 8. 防乱码措施

本次所有读取、写入和检查均使用 UTF-8。Python 渲染时使用 `ensure_ascii=False`，保持中文更新说明、合理性说明和节点标签可读。
