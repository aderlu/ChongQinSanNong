# 图谱右侧更新日志不随最新 diff 刷新的修复留痕

## 1. 修改目标

本次修复 `knowledge-graph.html` 右侧“图谱更新日志”没有跟随最新知识库更新变化的问题。目标是保证每次图谱 diff 生成后，主图谱页面也同步嵌入最新 `graph_change_diff_last.json`，从而让右侧日志展示最近一次更新的 CRUD 结果。

## 2. 修改前存在的问题

- 用户在浏览器中打开 `knowledge-graph.html` 后，右侧仍显示 DIS-045 的旧更新日志。
- 最新 diff 文件 `issues/graph_change_diff_last.json` 已经正确记录 DIS-033 更新，但主 HTML 中内嵌的 `change_log` 仍是上一轮数据。
- 原因是执行顺序为：`phase9_rebuild_indexes_graph_smoke.py` 先渲染主图谱 HTML，随后 `audit_graph_change_diff.py` 才生成最新 diff；diff 生成后没有再次渲染主图谱。

## 3. 修改前代码状态

- 主图谱渲染脚本：`ai-/knowledge/llm_wiki_swine_authoritative/tools/render_wash_interactive_graph.py`
- diff 脚本：`ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_graph_change_diff.py`
- 验收链路：`ai-/knowledge/llm_wiki_swine_authoritative/tools/run_swine_wiki_maintenance_checks.py`

修改前 `audit_graph_change_diff.py` 只生成：

- `issues/graph_change_diff_last.json`
- `issues/graph_change_diff_last.md`
- `wiki/knowledge-graph-changes.html`
- `issues/wiki_crud_change_log.jsonl`

但不会刷新 `wiki/knowledge-graph.html`。

## 4. 本次新增或更新内容

### 更新代码

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_graph_change_diff.py`

新增逻辑：

- 在 diff 写入完成后调用 `render_wash_interactive_graph.py`。
- 让主图谱 HTML 重新读取最新 `graph_change_diff_last.json` 并重建内嵌 `change_log`。
- 新增 `--skip-main-html-refresh` 参数，保留诊断场景下跳过主 HTML 刷新的能力。
- 如果主 HTML 刷新失败，diff 脚本返回失败，避免验收显示通过但页面仍是旧日志。

## 5. CRUD 类型

- Update：修改图谱 diff 脚本的执行逻辑。
- Rebuild：重新生成 `knowledge-graph.html`，使右侧日志读取最新 diff。
- Query：检查 `knowledge-graph.html`、`graph_change_diff_last.json` 与 `knowledge-graph-changes.html` 的内容一致性。
- Delete：本次不删除旧数据。

## 6. Old data 旧数据处理

- 不删除旧的 DIS-045 diff 记录，历史记录仍保留在 `issues/wiki_crud_change_log.jsonl`。
- 主图谱右侧只展示最近一次 diff，旧数据作为历史审计日志保留。
- 这样既避免覆盖审计历史，也保证当前演示页面展示最新更新结果。

## 7. High-risk 高风险边界

本次修改只影响图谱 HTML 展示和 diff 刷新流程，不新增医学事实、药物、剂量、疗程、休药期、MRL、食品安全或监管执行结论。

## 8. Governance Compliance

本次更新遵守：

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- 固定入口 `run_guarded_wiki_update.py`

后续完整验收仍通过：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

## 9. Runtime manifest 影响

- 本次不改变 runtime manifest 的实体纳入范围。
- 只保证 `audit_graph_change_diff.py` 之后的主图谱 HTML 使用最新 diff。
- `runtime_core_manifest` 的 missing_paths、实体数量和图谱结构应保持由既有构建脚本控制。

## 10. Gold dataset 影响

- 本次不改变 gold dataset 事实、样本或评估边界。
- 仅提升演示页面对最新 CRUD 变化的可见性，方便汇报和验收。

## 11. 预计更新效果

- `knowledge-graph.html` 右侧“图谱更新日志”将显示 DIS-033 本次新增的 `source:A0-USDA-APHIS-VS-2026` 和 5 个 `DIS033-WEB-*` fact。
- 右侧统计应显示新增节点 6、边 10，而不是旧的 DIS-045 更新。
- `knowledge-graph-changes.html` 与主图谱右侧日志保持一致。

## 12. UTF-8 和乱码防护

- 新增和修改文件均使用 UTF-8。
- Python 写入 JSON、HTML、Markdown 继续使用 `encoding="utf-8"`。
- 不批量重写历史中文乱码内容，避免扩大编码损伤。
