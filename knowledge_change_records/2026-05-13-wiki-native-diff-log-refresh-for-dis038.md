# 2026-05-13 Wiki-Native 最近一次更新日志修复记录

## 变更背景

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\wiki-native-knowledge-graph.html` 已经重建为最新主图谱，但页面顶部“Wiki-Native 图谱构建日志”仍混入旧日志信息和乱码说明。
- 根因不是主图谱没有更新，而是渲染链优先读取 `issues/wiki_native_graph_change_diff_last.json`，该文件被手工补写后存在 UTF-8 中文污染。
- 同时，本次新增的来源页 `A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.md` 也残留了两段乱码中文标题，导致重建后 source section 节点名称异常。

## 修改前的问题

- 顶部 change log 的 `generated_at` 已是最新时间，但 `recent_crud_events.reason` 和 `reasonableness` 显示为乱码问号，无法作为正式汇报证据。
- `A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.md` 中“可支持结论”“不得外推边界”两个章节标题及其正文出现乱码。
- 因来源页标题乱码，`wiki-native-graph.json` 与 `wiki-native-knowledge-graph.html` 中新 source section 节点 ID 也被污染，不利于审计和后续自动化判断。

## 本次修改

### 1. 修复来源页 UTF-8 中文

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\sources\A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.md`
- 修复内容：
  - 将乱码章节名改为“可支持结论”“不得外推边界”
  - 将对应中文说明恢复为可读 UTF-8 文本

### 2. 修复 wiki-native 最近一次变更 diff

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\wiki_native_graph_change_diff_last.json`
- 修复内容：
  - 更正 `added_nodes` 中污染的 source section 节点名称
  - 更正 `added_links` 中对应 section 链接文字
  - 将 `recent_crud_events.reason` 恢复为正式中文说明
  - 将 `reasonableness` 恢复为可审计、可汇报的中文判断结论

## 预期效果

- 重新渲染后，`wiki-native-knowledge-graph.html` 顶部“Wiki-Native 图谱构建日志”会显示最近一次 `DIS-038` 更新，而不是历史日志文案。
- 顶部 change log 可直接作为“最近一次真实更新已进入主图谱”的汇报证据。
- 新增的 CFSPH 来源页及其 section 节点名称恢复正常，避免图谱节点、审计结果和后续 diff 再次出现乱码扩散。

## 审计价值

- 将“主图谱已更新”和“最近一次更新日志已刷新”分开留痕，便于后续工作汇报区分：
  - 主图谱结构是否已变化
  - 页面顶部最近一次更新日志是否同步变化
- 明确指出本次问题属于渲染输入 diff 文件和来源页编码污染，而不是 wiki-native 主图谱构建失败。
