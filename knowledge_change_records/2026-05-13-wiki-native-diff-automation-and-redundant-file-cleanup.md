# 2026-05-13 Wiki-Native Diff 自动化与冗余文件清理记录

## 本次目标

- 删除确认冗余且会干扰项目整洁性的文件。
- 将 `wiki-native` 最近一次更新日志改为自动生成，避免再次出现手工补写 diff、编码污染和“最近一次更新不是最新”的问题。

## 修改前问题

- `wiki_native_graph_change_diff_last.json` 之前依赖人工补写，容易出现 UTF-8 乱码、内容与主图谱不同步、最近一次更新显示错误。
- `run_swine_wiki_maintenance_checks.py` 默认只重建 legacy runtime 图谱，不会自动重建 `wiki-native` 主图谱与其最近一次 diff。
- 项目中存在明确冗余文件：
  - `D:\XF-ChongQin\knowledge_change_records\zz-2026-05-12-worker-c-runtime-status-cleanup.md`
    - 与正式留痕 `2026-05-12-2359-worker-c-runtime-status-cleanup.md` 重复。
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\handbook_reinforcement_v13_2026-05-08.md`
    - 为空文件，无审计价值。

## 本次修改

### 1. 删除冗余文件

- 已删除重复留痕：
  - `D:\XF-ChongQin\knowledge_change_records\zz-2026-05-12-worker-c-runtime-status-cleanup.md`
- 已删除空文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\handbook_reinforcement_v13_2026-05-08.md`

### 2. 自动生成 wiki-native 最近一次变更日志

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\graph\build_wiki_native_graph_mvp.py`
- 新增能力：
  - 自动维护 `issues/graph_snapshots/latest_wiki_native_graph_snapshot.json`
  - 自动生成 `issues/wiki_native_graph_change_diff_last.json`
  - 自动生成 `issues/wiki_native_graph_change_diff_last.md`
  - 自动计算：
    - `added_nodes`
    - `removed_nodes`
    - `changed_nodes`
    - `added_links`
    - `removed_links`
    - `changed_links`
    - `verified_semantic_edges_before/after`
    - `recent_crud_events`
    - `reasonableness`

### 3. 将 wiki-native 重建纳入统一维护检查链

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\run_swine_wiki_maintenance_checks.py`
- 新增检查步骤：
  - `build_wiki_native_graph_mvp.py`
  - `render_wiki_native_graph.py`

## 解决效果

- 以后执行统一维护检查时，`wiki-native` 主图谱、页面和最近一次 diff 会一起重建，不再需要手工补写。
- `wiki-native-knowledge-graph.html` 顶部日志会优先读取自动生成的最新 diff，降低再次显示旧日志或乱码的风险。
- 项目目录进一步收敛，避免重复留痕和无内容文件继续留在核心目录中。

## 风险控制说明

- 本次没有删除正式审计快照、正式 build report、正式主图谱页面或用户可能用于追溯的历史记录。
- 删除动作仅限：
  - 明确重复的留痕文件
  - 明确为空的无效文件

## 预期长期收益

- `wiki-native` 主图谱从“人工修补可视化日志”转为“构建链自动生成日志”。
- 后续再出现主图谱更新时，最近一次日志与主图谱结构变化会同步刷新，降低误判和乱码回归概率。
