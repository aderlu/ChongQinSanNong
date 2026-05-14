# 真实 API Wiki 更新演示文档重构说明

## 1. 本次修改目标

本次修改目标是根据最新要求，重构 `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`，将演示流程从“模拟图谱更新”调整为“直接调用真实 API 做实际更新演示”。

新版文档要求维护人员在 PowerShell 中直接调用 NCBI PubMed E-utilities API，并通过正式 Wiki 的固定入口完成一次可审计的实际更新，展示真实 API 来源如何进入知识库、如何产生图谱变化、如何记录运行日志和 CRUD diff。

## 2. 修改前存在的问题

修改前的演示文档采用“两条线”结构：

- A 线：使用临时演示库做安全模拟，不修改正式猪病知识库。
- B 线：正式 Wiki 受控更新。

这种方式适合安全展示图谱变化，但与当前要求存在偏差：

- 用户希望直接调用真实 API 做实际演示，不需要模拟。
- 模拟库虽然安全，但不能完全证明正式 Wiki 的真实写入链路。
- leader 汇报时需要展示真实 API 来源、正式知识库写入、图谱 diff、HTML 更新和日志闭环，而不是临时演示库的结果。

## 3. 本次修改内容

重构文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`

新版文档移除了模拟演示主线，改为真实 API 实操流程，核心步骤包括：

- 设置 PowerShell UTF-8，防止中文乱码。
- 进入 `D:\XF-ChongQin\ai-` 项目目录。
- 读取两份短执行卡和两份完整治理文档。
- 记录正式 Wiki 更新前图谱、HTML、运行日志和 diff 状态。
- 使用 PowerShell `Invoke-RestMethod` 直接调用 NCBI PubMed E-utilities API。
- 获取真实 PMID、文献标题、期刊名和发布日期。
- 通过 PowerShell 生成 `demo_real_api_pubmed_source_update.py` 更新脚本。
- 更新脚本再次调用真实 PubMed API。
- 更新脚本写入正式 Wiki 的 raw API JSON、source markdown、source index、source authority status index 和一条 provenance fact。
- 使用 `run_guarded_wiki_update.py --dry-run` 做固定入口预演。
- 使用 `run_guarded_wiki_update.py -- python ...` 正式执行真实 API 更新。
- 查看固定入口运行日志。
- 查看 raw API 原始落盘数据。
- 查看新增来源页。
- 查看新增来源索引。
- 查看新增 provenance fact。
- 查看图谱 diff 和 HTML 图谱页面。
- 对比更新前后节点、边、事实数量。
- 查看 CRUD 日志。
- 单独执行一键完整验收。
- 要求真实演示后新增 `knowledge_change_records` 工作留痕。
- 提供通过固定入口清理演示数据的命令。
- 给出 leader 汇报时建议展示的命令证据。

## 4. 数据治理边界

新版文档明确限制本次真实 API 演示的事实边界：

- PubMed 文献只作为 `SRC` 级研究来源线索。
- 新增 fact 类型为 provenance-only，只表示“真实 API 来源已登记并可追溯”。
- 不新增药物剂量、休药期、MRL、残留、食品安全、检疫处置、扑杀、治疗方案或监管结论。
- 不覆盖、不删除既有非洲猪瘟页面或既有正式医学事实。
- 如果后续要将文献内容晋级为正式医学事实，必须经过证据分级、交叉来源核验和人工复核。

## 5. 解决的问题

本次重构解决了以下问题：

- 使演示流程完全基于真实 API 和正式 Wiki，不再依赖模拟库。
- 能够展示真实 API 数据如何落盘为 raw evidence。
- 能够展示来源页、来源索引、权威状态索引和 provenance fact 如何被写入。
- 能够展示固定入口如何自动执行治理预检、更新命令和完整验收。
- 能够展示数据变化后图谱 diff、HTML 页面、CRUD 日志和运行日志如何支撑汇报。
- 通过 provenance-only 设计避免真实 API 演示污染高风险医学事实层。

## 6. 本次未执行的内容

本次只修改演示文档，没有实际调用 PubMed API，也没有实际执行正式 Wiki 更新。

本次没有写入 raw API JSON、source markdown、source index、source authority status index 或 knowledge facts。真实演示需要维护人员按文档命令执行，并通过固定入口完成。

## 7. 防乱码措施

新版文档继续前置 UTF-8 设置：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

并要求所有中文 Markdown、JSON、JSONL、CSV 读取命令显式使用 `-Encoding UTF8`。文档中的 Python 写入逻辑使用 UTF-8 和 `ensure_ascii=False`，用于降低中文来源标题和日志内容乱码风险。

## 8. 验证结果

已完成以下验证：

- 使用 UTF-8 读取新版 `WIKI_UPDATE_POWERSHELL_DEMO.md`，中文显示正常。
- 使用 `Select-String` 检查章节标题，确认文档包含 0 到 22 的完整真实 API 演示步骤。
- 检查常见乱码信号，未发现异常标记。
- 确认文档主线已从模拟演示调整为真实 PubMed API 与正式固定入口。
