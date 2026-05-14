# 猪病 LLM Wiki 图谱更新模拟终端执行说明

本文档说明如何在终端逐步执行一次“受治理的猪病知识图谱自动更新模拟”，并查看更新前后图谱、节点/边/事实变化、合理性说明和审计闭环结果。

该流程使用临时演示库：

`D:\XF-ChongQin\ai-\results\wiki_graph_update_simulation\demo_swine_wiki`

不会修改正式猪病知识库：

`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative`

## 1. 进入项目目录

执行：

```powershell
Set-Location "D:\XF-ChongQin\ai-"
```

预期结果：

- 终端当前目录切换到 `D:\XF-ChongQin\ai-`
- 后续命令都从项目根目录执行

## 2. 设置 Python 模块路径

执行：

```powershell
$env:PYTHONPATH = "src;."
```

预期结果：

- Python 可以找到 `chicken_data_synthesis` 包
- 不会打印输出；没有报错即成功

## 3. 编译检查模拟脚本

执行：

```powershell
python -m py_compile scripts/simulate_governed_swine_graph_update_2026_05_08.py
```

预期结果：

- 没有输出即表示语法检查通过
- 如果脚本有语法问题，终端会打印 Python traceback

## 4. 执行完整模拟更新

执行：

```powershell
python scripts/simulate_governed_swine_graph_update_2026_05_08.py `
  --clean `
  --output-dir results/wiki_graph_update_simulation
```

预期输出类似：

```json
{
  "demo_wiki": "D:\\XF-ChongQin\\ai-\\results\\wiki_graph_update_simulation\\demo_swine_wiki",
  "before_html": "D:\\XF-ChongQin\\ai-\\results\\wiki_graph_update_simulation\\knowledge-graph-before.html",
  "after_html": "D:\\XF-ChongQin\\ai-\\results\\wiki_graph_update_simulation\\knowledge-graph-after.html",
  "diff_json": "D:\\XF-ChongQin\\ai-\\results\\wiki_graph_update_simulation\\graph-update-diff.json",
  "report": "D:\\XF-ChongQin\\ai-\\results\\wiki_graph_update_simulation\\graph-update-report.md",
  "reproduce_steps": "D:\\XF-ChongQin\\ai-\\results\\wiki_graph_update_simulation\\reproduce-steps.ps1",
  "added_nodes": 3,
  "added_links": 2,
  "added_candidate_facts": 1
}
```

本步骤实际完成：

- 创建最小猪病演示 wiki
- 生成更新前图谱
- 模拟 `DIS-026 口蹄疫` 的 gap-first 自动更新
- 发现并登记 WOAH 口蹄疫权威来源候选
- 写入 `NEEDS_REVIEW` 候选事实
- 执行 schema-check、strict lint、graph rebuild、status snapshot
- 写入治理审计 JSONL
- 生成更新后图谱
- 生成前后 diff 报告

## 5. 查看生成文件

执行：

```powershell
Get-ChildItem results/wiki_graph_update_simulation |
  Select-Object Name,Length,LastWriteTime
```

预期结果包含：

```text
demo_swine_wiki
graph-before.json
graph-after.json
graph-update-diff.json
graph-update-report.md
knowledge-graph-before.html
knowledge-graph-after.html
knowledge-graph-before.md
knowledge-graph-after.md
reproduce-steps.ps1
```

## 6. 查看更新前后图谱可视化文件

执行：

```powershell
Get-ChildItem results/wiki_graph_update_simulation -Filter "knowledge-graph-*.html" |
  Select-Object FullName,Length,LastWriteTime
```

预期结果：

- `knowledge-graph-before.html`
- `knowledge-graph-after.html`

可在浏览器中打开：

```powershell
Start-Process "D:\XF-ChongQin\ai-\results\wiki_graph_update_simulation\knowledge-graph-before.html"
Start-Process "D:\XF-ChongQin\ai-\results\wiki_graph_update_simulation\knowledge-graph-after.html"
```

预期视觉差异：

- 更新前：只有 `DIS-026 口蹄疫`、基础 source、已复核基础事实相关节点和边
- 更新后：新增 WOAH source 节点、候选事实节点、候选证据边

## 7. 查看结构化 diff 摘要

执行：

```powershell
Get-Content results/wiki_graph_update_simulation/graph-update-diff.json |
  Select-String -Pattern "added_node_count|removed_node_count|added_link_count|removed_link_count|candidate_fact_delta|accepted_count|rejected_count"
```

预期关键结果：

```text
"added_node_count": 3
"removed_node_count": 0
"added_link_count": 2
"removed_link_count": 0
"candidate_fact_delta": 1
"accepted_count": 1
"rejected_count": 0
```

含义：

- 新增 3 个图谱节点
- 新增 2 条图谱边
- 没有删除既有节点或边
- 候选事实增加 1 条
- 权威来源候选接受 1 条、拒绝 0 条

## 8. 查看新增节点详情

执行：

```powershell
$diff = Get-Content results/wiki_graph_update_simulation/graph-update-diff.json -Raw | ConvertFrom-Json
$diff.added_nodes | Format-Table id,group,label,evidence_status -AutoSize
```

预期结果类似：

```text
id                         group     label                      evidence_status
--                         -----     -----                      ---------------
CANDIDATE:c183a023083ef0   candidate pending_review
CANDIDATE:ff96a46f354a24   candidate 口蹄疫 WOAH disease page
SRC-0002                   source    口蹄疫 WOAH disease page   NEEDS_REVIEW
```

解释：

- `SRC-0002` 是新增权威来源候选节点
- `candidate` 节点表示候选事实层，不等同于正式已复核事实
- `NEEDS_REVIEW` 表示仍需后续专业复核

## 9. 查看新增边详情

执行：

```powershell
$diff.added_links | Format-Table source,target,type,fact_id -AutoSize
```

预期结果类似：

```text
source                     target                    type               fact_id
------                     ------                    ----               -------
CANDIDATE:ff96a46f354a24   CANDIDATE:c183a023083ef0  candidate-fact     CAND-0001
CANDIDATE:ff96a46f354a24   SRC-0002                  candidate-evidence CAND-0001
```

解释：

- `candidate-fact`：新增候选事实关系
- `candidate-evidence`：候选事实可追溯到新增 source
- `fact_id=CAND-0001` 表示仍在候选事实层

## 10. 查看候选事实文件

执行：

```powershell
Get-Content results/wiki_graph_update_simulation/demo_swine_wiki/exports/knowledge_facts.candidates.json
```

预期结果包含：

```json
{
  "fact_id": "CAND-0001",
  "subject": "口蹄疫 WOAH disease page",
  "predicate": "source_imported",
  "object": "pending_review",
  "evidence_source_id": "SRC-0002",
  "external_url": "https://www.woah.org/en/disease/foot-and-mouth-disease/",
  "evidence_role": "clinical_reference",
  "evidence_status": "NEEDS_REVIEW"
}
```

合理性：

- 自动更新只新增候选事实
- 不直接进入 `exports/knowledge_facts.json`
- 不会污染训练/评估使用的正式已复核事实层

## 11. 查看正式事实是否未被污染

执行：

```powershell
Get-Content results/wiki_graph_update_simulation/demo_swine_wiki/exports/knowledge_facts.json
```

预期结果仍只有演示库原始正式事实：

```json
{
  "fact_id": "DIS-026-DEMO-001",
  "fact_type": "disease",
  "subject": "口蹄疫",
  "predicate": "diagnosis_standard_anchor",
  "object": "baseline reviewed swine reference",
  "evidence_source_id": "SRC-0001",
  "evidence_status": "HUMAN_REVIEWED"
}
```

合理性：

- 既有 `HUMAN_REVIEWED` 正式事实未被覆盖
- 新增来源只进入候选层
- 符合兽医医学知识库的严谨更新边界

## 12. 查看审计闭环事件

执行：

```powershell
Get-ChildItem results/wiki_graph_update_simulation/demo_swine_wiki/issues -Filter "wiki_governance_audit_*.jsonl" |
  ForEach-Object { Get-Content $_.FullName }
```

预期至少包含 3 类事件：

```text
phase=simulation_trigger
phase=precheck
phase=post_write_closure
```

其中 `post_write_closure` 应包含：

```json
"status": "closed",
"schema_ok": true,
"lint_ok": true,
"accepted_count": 1,
"rejected_count": 0,
"graph_node_count": 6,
"graph_link_count": 6
```

含义：

- 变更触发已记录
- 写入前准入校验已通过
- 写入后 schema、lint、graph rebuild、status snapshot 已完成
- 本次闭环状态为 `closed`

## 13. 查看人类可读报告

执行：

```powershell
Get-Content results/wiki_graph_update_simulation/graph-update-report.md
```

预期报告包含：

- Visualization Files
- Summary
- Added Nodes
- Added Links
- Reasonableness

重点看：

```text
Added nodes: 3
Removed nodes: 0
Added links: 2
Removed links: 0
Candidate fact delta: 1
```

## 14. 一键复现脚本

上面的命令也会生成：

`results/wiki_graph_update_simulation/reproduce-steps.ps1`

执行：

```powershell
.\results\wiki_graph_update_simulation\reproduce-steps.ps1
```

预期结果：

- 自动重新运行完整模拟
- 打印 HTML 图谱文件列表
- 打印 diff 摘要
- 打印治理审计事件
- 打印 Markdown 报告

## 15. 本示例说明了什么

本示例展示了猪病知识图谱自动更新的一条合规路径：

1. 先保留更新前图谱快照。
2. 通过治理请求触发更新。
3. 来源必须通过权威域名白名单。
4. 新增事实只能进入候选层。
5. 写入后必须执行 schema-check、strict lint、graph rebuild。
6. 生成更新后图谱。
7. 输出前后 diff。
8. 写入机器可读审计日志。

因此，它支持对比更新前后的可视化结果，也能解释变化是否合理。

