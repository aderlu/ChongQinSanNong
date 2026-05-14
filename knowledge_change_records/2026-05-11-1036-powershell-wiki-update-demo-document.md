# PowerShell Wiki 更新演示文档建设说明

## 1. 本次修改目标

本次修改的目标是为猪病 LLM Wiki 知识库补充一份可直接用于演示和培训的 PowerShell 操作文档，说明如何从真实 API 获取来源线索，并通过固定更新入口完成受控更新、治理预检、图谱重建、CRUD diff、运行日志查看和 HTML 可视化对比。

该文档用于解决“规则已经存在，但向 leader 或维护人员展示时缺少逐步演示材料”的问题，使后续知识库更新不只停留在制度约束上，也能用一套清晰命令证明更新流程、图谱变化和日志留痕是可落地的。

## 2. 修改前存在的问题

修改前，知识库已经具备以下支撑：

- 固定更新入口：`ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py`
- 一键验收脚本：`ai-/knowledge/llm_wiki_swine_authoritative/tools/run_swine_wiki_maintenance_checks.py`
- 治理预检脚本：`ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py`
- 图谱变更 diff 脚本：`ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_graph_change_diff.py`
- 短执行卡与完整治理文档。

但仍存在一个汇报和交接层面的缺口：

- 缺少一份从 PowerShell 视角出发的逐步演示文档。
- 缺少“真实 API 来源 -> 固定入口执行 -> 日志查看 -> 图谱 HTML 对比 -> CRUD 变更说明”的完整串联示例。
- 维护人员需要自己拼接多个脚本命令，容易漏掉编码设置、dry-run、日志检查、图谱 diff、变更记录等关键步骤。
- 中文知识库在 Windows PowerShell 场景下存在默认编码导致显示乱码的风险，需要在演示命令中明确 UTF-8 设置。

## 3. 本次新增内容

新增文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`

该文档覆盖以下内容：

- 演示前必须读取的短执行卡和完整治理文档。
- PowerShell UTF-8 编码设置。
- 更新前图谱、HTML 页面、diff 和运行日志快照。
- 使用 NCBI E-utilities 公共 API 作为真实 API 示例获取 PubMed 来源线索。
- 构建演示更新脚本的命令示例。
- 通过固定入口执行 dry-run。
- 通过固定入口执行正式受控更新。
- 查看 `guarded_wiki_update_last_run.json` 和 `guarded_wiki_update_runs.jsonl`。
- 查看更新后来源、证据和候选材料。
- 打开 `knowledge-graph.html` 和 `knowledge-graph-changes.html` 对比图谱变化。
- 展示节点、边、事实变更的判断逻辑。
- 查看 `wiki_crud_change_log.jsonl`。
- 手动对比更新前后节点数、边数、事实数。
- 要求每次真实更新都补充 `knowledge_change_records` 工作留痕。
- 提供演示数据回滚或清理说明。

## 4. 解决的问题

本次新增文档解决了以下问题：

- 将分散的治理规则、执行入口、验收脚本、图谱页面和运行日志串成一条可演示流程。
- 让维护人员可以按步骤手动复现一次真实 API 来源更新，不需要临时理解多个脚本之间的关系。
- 强化了“所有更新必须通过固定入口执行”的操作习惯。
- 将图谱变化、HTML 页面变化、CRUD 日志和工作留痕纳入演示过程。
- 对医学知识库的高风险内容给出边界提醒：API 来源默认作为研究线索或候选来源，不能直接外推为药物、剂量、休药期、MRL、残留、食品安全或监管正向结论。
- 明确 Windows PowerShell 下的 UTF-8 设置，降低中文内容乱码风险。

## 5. 本次未修改的内容

本次只新增演示文档，没有直接修改疾病、药物、来源、事实或图谱运行时数据。

本次没有新增或删除医学事实，没有改变现有图谱节点、边、事实内容，也没有改动 HTML 构建逻辑。文档中涉及的 API 更新脚本是演示用命令，真实执行时仍必须经过固定入口和完整验收。

## 6. 预计效果

后续向 leader 汇报或进行维护交接时，可以直接使用该文档演示：

- 更新前如何确认图谱和日志状态。
- 如何从真实 API 获取来源线索。
- 如何通过固定入口执行 Wiki 更新。
- 如何自动触发治理预检和验收。
- 如何查看更新后的图谱 HTML 和图谱变更页面。
- 如何查看每次运行的日志记录和 CRUD 变更记录。
- 如何补充每次更新的工作留痕。

该文档可以降低后续维护成本，减少漏跑脚本、漏写日志、漏做图谱对比、漏做变更说明的风险。

## 7. 防乱码措施

演示文档中明确要求每次维护前在 PowerShell 中执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

文档中的 JSON 写入示例要求使用 UTF-8，并在 Python 中使用 `ensure_ascii=False`，避免中文标题、来源名、疾病名、药物名在写入和展示时发生乱码。

## 8. 验证结果

已完成以下轻量验证：

- 确认 `WIKI_UPDATE_POWERSHELL_DEMO.md` 文件已创建。
- 使用 `Select-String` 检查文档章节标题，确认演示步骤完整。
- 使用 UTF-8 方式读取文档开头内容，中文显示正常。
- 检查常见乱码信号，未发现异常标记。

注意：PowerShell 默认编码读取中文文件时可能出现显示乱码，因此后续查看中文 Markdown 文档时应显式使用 `-Encoding UTF8`，并先完成 UTF-8 控制台设置。
