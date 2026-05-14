# Web Access 官方网页来源更新演示文档重构说明

## 1. 本次修改目标

本次修改目标是继续重构 `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`，将演示流程从“直接调用 PubMed API”调整为“调用 Codex 并使用已安装的 Web Access skill 进入权威官方来源链接获取信息源和数据，再更新 LLM Wiki 和知识图谱”。

新版文档用于演示：Codex 如何通过 Web Access skill 获取官方网页来源，如何将来源证据落盘为 raw evidence JSON，如何通过固定入口写入正式 Wiki，并如何通过图谱 diff、HTML 页面、CRUD 日志和运行日志完成审计闭环。

## 2. 修改前存在的问题

上一版 `WIKI_UPDATE_POWERSHELL_DEMO.md` 使用 NCBI PubMed E-utilities API 作为真实 API 示例，能够演示真实 API 数据进入 Wiki，但仍存在以下问题：

- 演示入口是 API，不是用户当前要求的 Web Access skill。
- 不能展示 Codex 如何进入官方网页链接、读取页面原文并保存来源证据。
- 对动态网页、官方网页结构、浏览器 CDP 模式和 Web Access skill 的操作说明不足。
- 用户希望演示的是“LLM 使用 Codex + Web Access 获取官方来源后更新 Wiki 和知识图谱”的完整链路。

## 3. 本次修改内容

重构文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`

新版文档的核心演示来源改为：

- `https://www.woah.org/en/disease/african-swine-fever/`

新版流程包括：

- 设置 PowerShell UTF-8。
- 进入 `D:\XF-ChongQin\ai-` 项目目录。
- 读取两份短执行卡和两份完整治理文档。
- 检查 Web Access skill 可用性。
- 提示浏览器自动化风险。
- 记录正式 Wiki 更新前图谱和运行日志状态。
- 准备给 Codex 的 Web Access 获取任务。
- 要求 Codex 必须加载 `web-access` skill。
- 要求 Codex 进入 WOAH 官方非洲猪瘟页面。
- 要求 Codex 提取页面标题、URL、访问时间、发布机构、疾病名称、页面明示摘要、来源等级建议、证据状态建议、使用边界和不得外推边界。
- 要求 Codex 将 raw evidence 保存为 UTF-8 JSON。
- 提供 Web Access CDP 命令行执行参考。
- 检查 Web Access 证据文件。
- 生成 `demo_web_access_official_source_update.py` 更新脚本。
- 更新脚本读取 raw evidence JSON，不再联网。
- 更新脚本写入 source markdown、source index、source authority status index 和 provenance fact。
- 通过固定入口执行 dry-run。
- 通过固定入口正式执行官方网页来源更新。
- 查看固定入口运行日志。
- 查看新增来源页。
- 查看索引是否新增来源。
- 查看新增 provenance fact。
- 查看图谱 diff。
- 打开更新后 HTML 图谱。
- 对比更新前后节点、边、事实数量。
- 查看 CRUD 日志。
- 单独执行一键完整验收。
- 要求本次演示必须补充工作留痕。
- 提供通过固定入口清理演示数据的命令。
- 给出向 leader 汇报时展示的命令证据。

## 4. 数据治理边界

新版文档明确了 Web Access 官方网页来源的使用边界：

- Web Access 只负责进入权威官方来源页面、读取页面内容、保存证据摘要和来源元数据。
- 官方网页来源必须进入治理判断，不能直接外推高风险医学或监管结论。
- 新增 fact 是 provenance-only，只表示“官方网页来源已登记并关联到非洲猪瘟页面”。
- 不新增药物剂量、休药期、MRL、残留、食品安全、检疫处置、扑杀、治疗方案或监管结论。
- 不覆盖、不删除既有非洲猪瘟事实。
- 是否晋级为正式医学事实，必须按治理文档进行证据分级、交叉来源核验和人工复核。

## 5. 解决的问题

本次重构解决了以下问题：

- 将演示流程对齐为 Codex + Web Access skill 的官方网页来源获取方式。
- 明确区分“联网获取 raw evidence”和“固定入口正式写入 Wiki”两个阶段，便于审计。
- 使官方网页来源获取、证据落盘、Wiki 写入、图谱重建、CRUD diff、HTML 页面和运行日志形成完整闭环。
- 保留 provenance-only 事实设计，避免 Web Access 提取内容直接污染医学事实层。
- 强化了固定入口约束，所有写入动作仍必须通过 `run_guarded_wiki_update.py`。

## 6. 本次未执行的内容

本次只修改演示文档，没有实际调用 Web Access skill 访问 WOAH 页面，也没有写入 raw evidence JSON。

本次没有实际执行 `demo_web_access_official_source_update.py`，也没有写入 source markdown、source index、source authority status index 或 knowledge facts。真实演示需要维护人员按文档命令执行，并通过固定入口完成。

## 7. 防乱码措施

新版文档继续前置 UTF-8 设置：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

并要求所有中文 Markdown、JSON、JSONL、CSV 读取命令显式使用 `-Encoding UTF8`。文档中的 Python 写入逻辑使用 UTF-8 和 `ensure_ascii=False`，用于降低中文来源标题、证据摘要和日志内容乱码风险。

## 8. 验证结果

已完成以下验证：

- 使用 UTF-8 读取新版 `WIKI_UPDATE_POWERSHELL_DEMO.md`，中文显示正常。
- 使用 `Select-String` 检查章节标题，确认文档包含 0 到 24 的完整 Web Access 官方网页来源演示步骤。
- 检查常见乱码信号，未发现异常标记。
- 确认文档包含 Web Access skill、WOAH 官方来源、固定入口、演示更新脚本、source id、fact id、graph diff 和 CRUD 日志等关键命令与标识。
