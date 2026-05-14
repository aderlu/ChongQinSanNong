# 基于终端 Walkthrough 重构 PowerShell 更新演示文档说明

## 1. 本次修改目标

本次修改目标是参考 `ai-/docs/SWINE_GRAPH_UPDATE_TERMINAL_WALKTHROUGH.md`，重新构建 `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`，使演示文档尽量以 PowerShell 命令行为主，能够逐步展示猪病 LLM Wiki 的图谱更新、图谱前后对比、节点/边/事实变化、运行日志和治理闭环。

## 2. 修改前存在的问题

修改前的 `WIKI_UPDATE_POWERSHELL_DEMO.md` 已经包含真实 API、固定入口、日志、图谱和留痕要求，但整体更偏说明型文档，存在以下不足：

- 命令行步骤不够像可现场执行的终端 walkthrough。
- 对“预期输出”和“结果含义”的拆解不够细。
- 安全模拟演示和正式 Wiki 更新流程混在一起，不利于区分“展示效果”和“真实落地”。
- 向 leader 演示图谱变化时，缺少类似参考文档中“更新前 HTML、更新后 HTML、diff JSON、候选事实、审计闭环”的清晰演示节奏。

## 3. 本次修改内容

重构文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`

新版文档拆分为两条主线：

- A 线：安全模拟演示。使用 `scripts/simulate_governed_swine_graph_update_2026_05_08.py` 生成临时演示库，不修改正式猪病知识库，用于展示图谱更新前后可视化差异。
- B 线：正式 Wiki 受控更新。使用 `knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py` 作为唯一固定入口，用于真实更新任务。

新版文档新增或强化了以下命令行内容：

- PowerShell UTF-8 编码设置。
- 进入项目目录和设置 `PYTHONPATH`。
- 编译检查模拟脚本。
- 执行完整模拟更新。
- 查看模拟输出文件。
- 打开更新前后 HTML 图谱。
- 查看结构化 diff 摘要。
- 查看新增节点和新增边详情。
- 查看候选事实文件。
- 验证正式事实未被污染。
- 查看治理审计闭环事件。
- 查看人类可读报告。
- 使用 `reproduce-steps.ps1` 一键复现模拟。
- 正式 Wiki 更新前快照。
- 调用真实 NCBI PubMed API 获取来源线索。
- 使用固定入口 dry-run。
- 使用固定入口执行正式更新命令。
- 查看正式运行日志、图谱 diff、CRUD 日志。
- 对比正式更新前后节点和边数量。
- 强制要求每次真实更新新增 `knowledge_change_records` 工作留痕。
- 汇报时建议展示的命令和证据。

## 4. 解决的问题

本次重构后，演示文档从“说明文档”变成“可执行命令行演示手册”，解决了以下问题：

- 维护人员可以按步骤复制命令执行，不需要自行拼接脚本。
- leader 汇报时可以先用安全模拟线展示图谱前后变化，不影响正式知识库。
- 真实更新时可以切换到正式受控更新线，确保不会绕过治理预检和完整验收。
- 图谱节点、边、候选事实、正式事实、HTML 页面和审计日志都有对应查看命令。
- 明确了候选事实不会直接污染正式事实层，符合兽医医学知识库的严谨性要求。
- 明确了 Windows PowerShell 下 UTF-8 设置，降低中文乱码风险。

## 5. 本次未修改的内容

本次只重构演示文档，没有修改正式疾病、药物、来源、事实或图谱运行时数据。

本次没有执行真实 Wiki 数据写入，也没有改变 `graph-data.json`、`knowledge-graph.html`、`knowledge-graph-changes.html` 的内容。文档中的正式更新命令仍要求后续真实维护时通过固定入口执行。

## 6. 预计效果

后续进行演示或培训时，可以直接按新版文档操作：

- 先跑安全模拟线，展示更新前后图谱 HTML 和 diff。
- 再讲正式更新线，说明真实 Wiki 如何通过固定入口执行。
- 用日志和 CRUD diff 证明每次更新可追溯。
- 用工作留痕要求保证每次变更都能支撑汇报。

该文档将降低后续维护人员的操作门槛，并减少漏跑预检、漏看 diff、漏写留痕、误把候选事实当正式事实的风险。

## 7. 防乱码措施

新版文档保留并前置 PowerShell UTF-8 设置：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

同时要求所有中文 Markdown 和 JSON 查看命令显式使用 `-Encoding UTF8`，并提醒 Python 写 JSON 时使用 UTF-8 和 `ensure_ascii=False`。

## 8. 验证结果

已完成以下验证：

- 使用 UTF-8 读取新版 `WIKI_UPDATE_POWERSHELL_DEMO.md`，中文显示正常。
- 使用 `Select-String` 检查章节标题，确认文档包含 0 到 27 的完整步骤。
- 检查常见乱码信号，未发现异常标记。
- 确认参考的模拟脚本 `ai-/scripts/simulate_governed_swine_graph_update_2026_05_08.py` 存在。
- 确认正式固定入口 `ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py` 存在。
