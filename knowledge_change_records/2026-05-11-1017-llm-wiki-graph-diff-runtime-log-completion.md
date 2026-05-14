# 猪病 LLM Wiki 图谱变化展示与运行日志补齐记录

## 1. Landing Time

- Landing date: 2026-05-11
- Landing time: 10:17
- Time zone: Asia/Shanghai
- Change type: graph diff, CRUD log, runtime run log, HTML change view, validation pipeline enhancement

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Fixed update entrypoint used: not applicable for adding graph/log infrastructure; dry-run verified
- Source/fact CRUD type: update graph/log tooling and derived graph artifacts
- Input source type: local graph JSON, runtime manifest, fact status index, local Python tooling
- Old data handling: keep existing graph files; add diff snapshot, CRUD JSONL log, and change HTML
- If old data changed, factual reason: graph HTML previously showed only current state and did not expose data-change diff or append-only run history
- High-risk gate impact: none to facts; validation pipeline now preserves graph and CRUD visibility after updates
- Runtime manifest impact: manifest was rebuilt during graph rebuild; missing paths remained 0
- Gold dataset impact: none to samples

## 2. 修改目标

参考 `llm-wiki-skill` 项目的 LLM Wiki 图谱思路，本次目标是补齐当前猪病 Wiki 在完整知识图谱功能展示上的缺口：

1. 每次验收自动重建 graph JSON、Markdown 和 HTML。
2. 数据变化后生成图谱 diff。
3. 记录节点和边的新增、删除、更新变化。
4. 生成可查看变化的 HTML 页面。
5. 维护 CRUD 追加日志。
6. 固定入口追加运行历史日志，而不是只保留 last run。

## 3. 修改前存在的问题

修改前已有：

- `wiki/graph-data.json`
- `wiki/knowledge-graph.md`
- `wiki/knowledge-graph.html`
- `tools/phase9_rebuild_indexes_graph_smoke.py`
- `issues/runtime_retrieval_smoke_test_2026-05-09.json`
- `issues/guarded_wiki_update_last_run.json`

但仍存在以下问题：

1. `knowledge-graph.html` 只展示当前图谱，不展示本次新增、删除、修改了哪些节点和边。
2. 数据变化后，HTML 是否刷新依赖人工是否运行图谱重建脚本。
3. 一键验收脚本没有自动调用 `phase9_rebuild_indexes_graph_smoke.py`。
4. 没有图谱快照和 diff 机制。
5. 没有机器可读的 CRUD 追加日志。
6. 固定入口只写 `guarded_wiki_update_last_run.json`，没有追加式运行历史。

## 4. 修改前代码状态

修改前：

- `run_swine_wiki_maintenance_checks.py`
  - 执行治理预检、manifest、风险审计、readiness、编码审计、pytest。
  - 不重建 graph/html。
  - 不生成 graph diff。

- `run_guarded_wiki_update.py`
  - 固定入口可执行治理预检、更新命令和完整验收。
  - 只写最近一次运行报告。

- `test_swine_llm_wiki_runtime.py`
  - 检查 runtime、denylist、gold readiness、hard-block、pilot provenance、治理预检和固定入口 dry-run。
  - 不检查图谱 diff 工具。

## 5. 本次新增或更新了什么代码

新增：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_graph_change_diff.py`

该脚本完成：

1. 读取 `wiki/graph-data.json`。
2. 与 `issues/graph_snapshots/latest_graph_snapshot.json` 对比。
3. 生成节点和边的新增、删除、更新列表。
4. 生成 CRUD 统计。
5. 输出：
   - `issues/graph_change_diff_last.json`
   - `issues/graph_change_diff_last.md`
   - `wiki/knowledge-graph-changes.html`
   - `issues/wiki_crud_change_log.jsonl`
   - `issues/graph_snapshots/latest_graph_snapshot.json`

更新：

- `tools/run_swine_wiki_maintenance_checks.py`
  - 加入 `phase9_rebuild_indexes_graph_smoke.py`。
  - 加入 `audit_graph_change_diff.py`。

- `tools/run_guarded_wiki_update.py`
  - 新增追加式运行日志 `issues/guarded_wiki_update_runs.jsonl`。
  - 保留 `issues/guarded_wiki_update_last_run.json` 作为最近一次报告。

- `tools/audit_governance_compliance.py`
  - 将 `audit_graph_change_diff.py` 纳入 required governance tools。

- `tests/test_swine_llm_wiki_runtime.py`
  - 新增图谱变化工具和图谱产物存在性测试。

- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
  - 更新验收说明，明确完整验收会重建 graph/html 并生成 graph diff、CRUD log 和 change HTML。

## 6. 本次整理或生成了什么图谱与日志产物

已生成或更新：

- `wiki/knowledge-graph.html`
- `wiki/knowledge-graph.md`
- `wiki/graph-data.json`
- `wiki/knowledge-graph-changes.html`
- `issues/graph_change_diff_last.json`
- `issues/graph_change_diff_last.md`
- `issues/wiki_crud_change_log.jsonl`
- `issues/graph_snapshots/latest_graph_snapshot.json`
- `issues/guarded_wiki_update_last_run.json`
- `issues/guarded_wiki_update_runs.jsonl`

当前图谱：

- nodes: 2550
- links: 3127
- facts_in_graph: 2193

首次 diff 初始化结果：

```json
{
  "baseline_initialized": true,
  "added_nodes": 0,
  "removed_nodes": 0,
  "changed_nodes": 0,
  "added_links": 0,
  "removed_links": 0,
  "changed_links": 0
}
```

说明：本次是首次建立 graph snapshot，因此以当前图谱作为 baseline，没有实际新增/删除/修改差异。

## 7. 修改后解决了什么问题

修改后，当前猪病 Wiki 在图谱功能上补齐了以下能力：

1. 完整验收会自动重建图谱 JSON、Markdown 和 HTML。
2. 数据变化后会自动生成图谱 diff。
3. CRUD 变化会进入 `wiki_crud_change_log.jsonl`。
4. 图谱变化可以通过 `knowledge-graph-changes.html` 查看。
5. 固定入口的运行历史会追加到 `guarded_wiki_update_runs.jsonl`。
6. pytest 会检查图谱变化工具和图谱产物存在。

现在可以更清楚地区分：

- 当前图谱展示：`knowledge-graph.html`
- 图谱变化展示：`knowledge-graph-changes.html`
- 机器可读变化：`graph_change_diff_last.json`
- 长期 CRUD 日志：`wiki_crud_change_log.jsonl`
- 最近一次固定入口运行：`guarded_wiki_update_last_run.json`
- 固定入口运行历史：`guarded_wiki_update_runs.jsonl`

## 8. 预计更新效果

对后续数据更新：

- source/fact/runtime/rule/gold 相关变化后，图谱会在完整验收中自动刷新。
- HTML 页面可以展示当前图谱和最新变化。
- CRUD 变化可以长期追踪。

对定时任务：

- 只要定时任务通过 `run_guarded_wiki_update.py` 执行，就会自动触发完整验收和图谱变化记录。

对工作汇报：

- 可以直接引用 `graph_change_diff_last.md/json` 和 `wiki_crud_change_log.jsonl` 说明本次新增、删除、修改了哪些节点和关系。

## 9. 验证命令和结果

已运行：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase9_rebuild_indexes_graph_smoke.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_graph_change_diff.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py
python -m pytest .\tests\test_swine_llm_wiki_runtime.py -q
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py --dry-run -- python -c "print('noop')"
```

结果：

```json
{
  "graph_rebuild": "passed",
  "graph_nodes": 2550,
  "graph_links": 3127,
  "facts_in_graph": 2193,
  "graph_diff": "passed",
  "governance_preflight": "passed",
  "pytest": "11 passed",
  "guarded_update_dry_run": "passed"
}
```

## 10. 防乱码措施

本次新增脚本和文档均使用 UTF-8。

新增 JSON/HTML/Markdown 输出均使用 UTF-8 写入。

图谱 diff 的 JSON 输出使用 `ensure_ascii=False`。

已检查新增脚本、变更记录和图谱变化 HTML 的明显乱码信号。

## 11. 残余风险和下一步

当前能力已经覆盖当前图谱展示、变化 HTML、CRUD JSONL 和固定入口运行历史。

后续仍建议：

1. 外部定时任务必须改为调用 `run_guarded_wiki_update.py`。
2. 如果需要更复杂的可视化，可以在 `knowledge-graph-changes.html` 中加入节点分组过滤、风险等级过滤和时间线过滤。
3. 如果需要跨多版本对比，可保留按时间戳命名的 graph snapshot，而不仅是 latest snapshot。

## 12. 结论

本次补齐了猪病 LLM Wiki 的图谱变化展示和运行日志能力。现在知识库不仅可以展示当前图谱，还能在完整验收中自动重建 HTML、生成 graph diff、记录 CRUD 日志，并为固定入口保留追加式运行历史，更接近完整 LLM Wiki 知识图谱维护体验。

