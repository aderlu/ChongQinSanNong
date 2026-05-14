# 猪病 LLM Wiki 治理规则自动化约束优化记录

## 1. Landing Time

- Landing date: 2026-05-11
- Landing time: 01:24
- Time zone: Asia/Shanghai
- Change type: governance automation, preflight checks, project-level LLM instruction, one-command validation

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Source/fact CRUD type: update/rebuild governance automation only
- Input source type: local Markdown governance documents and local test/tooling files
- Old data handling: keep existing governance documents; add automation and entry-point constraints
- If old data changed, factual reason: no biomedical old data changed; validation workflow was optimized to reduce manual reminders
- High-risk gate impact: strengthens future enforcement; no high-risk fact changed
- Runtime manifest impact: none in this change
- Gold dataset impact: none in this change

## 2. 修改目标

本次目标是降低后续维护时的人工操作成本，让 LLM 在更新猪病 Wiki 时更自动地基于以下两份文档执行：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

优化方向是建立三层约束：

1. 项目级指令约束：LLM 进入仓库时自动看到必须遵守的 Wiki 治理规则。
2. 自动预检约束：用脚本检查治理文档、入口文件和最新变更记录是否仍形成强制链路。
3. 一键验收约束：把治理预检、manifest、风险审计、readiness、编码审计和 pytest 串成一个命令。

## 3. 修改前存在的问题

虽然两份治理文档已经被升级为强制规则，但后续维护仍可能存在操作成本：

- 每次都需要人工提醒 LLM 先读两份治理文档。
- 每次验收需要记住多条命令。
- 没有自动脚本检查 README、index、schema、checklist、change record template 是否仍引用两份治理文档。
- 没有测试保证治理预检脚本长期通过。
- 如果最新变更记录漏写治理合规区块，只能靠人工发现。

## 4. 修改前代码和文档状态

修改前已有：

- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `SOURCE_BATCH_INTAKE_CHECKLIST.md`
- `CHANGE_RECORD_TEMPLATE.md`
- `tests/test_swine_llm_wiki_runtime.py`

但缺少：

- 项目级 `AGENTS.md` 中的猪病 Wiki 专用强制治理说明。
- `audit_governance_compliance.py` 治理预检脚本。
- `run_swine_wiki_maintenance_checks.py` 一键验收脚本。
- pytest 中的治理预检回归测试。

## 5. 本次新增或更新了什么代码和文档

新增代码：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py`
  - 检查两份治理文档是否存在。
  - 检查 README、index、schema、checklist、change record template、AGENTS 是否引用两份治理文档。
  - 检查最新 change record 是否包含治理合规、CRUD、旧数据处理、高风险、runtime manifest、gold dataset 等要素。
  - 检查核心治理文档和最新记录是否有明显乱码信号。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/run_swine_wiki_maintenance_checks.py`
  - 一键运行治理预检、runtime manifest 重建、幻觉风险审计、readiness 审计、编码审计和猪病 runtime pytest。

更新文档：

- `ai-/AGENTS.md`
  - 新增 `Mandatory Swine Wiki Governance` 小节。
  - 明确修改 `knowledge/llm_wiki_swine_authoritative/` 前必须先遵守两份治理文档。
  - 明确必须在 `knowledge_change_records/` 写工作记录。

- `WIKI_MAINTENANCE_GUIDE.md`
  - 新增一键验收命令。
  - 将 `audit_governance_compliance.py` 纳入必跑验收。

- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
  - 新增一键验收命令。
  - 将治理预检纳入验收标准。

- `SOURCE_BATCH_INTAKE_CHECKLIST.md`
  - 新增一键维护检查命令。
  - 增加 governance compliance preflight 和 runtime damaged count 验收项。

更新测试：

- `ai-/tests/test_swine_llm_wiki_runtime.py`
  - 新增 `test_swine_wiki_governance_compliance_preflight_passes`。

## 6. 修改后解决了什么问题

修改后，后续维护不再完全依赖人工提醒。

LLM 自动约束链路变为：

1. `AGENTS.md` 在项目级提示 LLM 修改猪病 Wiki 前必须遵守两份文档。
2. `audit_governance_compliance.py` 自动检查治理链路是否完整。
3. `run_swine_wiki_maintenance_checks.py` 提供一键验收。
4. pytest 将治理预检纳入猪病 runtime 回归测试。
5. 最新 change record 若缺治理合规信息，治理预检会失败。

这样可以降低以下风险：

- 忘记阅读两份治理文档。
- 忘记写 `knowledge_change_records/` 留痕。
- 入口文档后续被改坏，导致治理规则脱钩。
- 中文文档乱码或 mojibake 信号进入核心治理文件。
- 维护者只跑部分审计，遗漏治理预检。

## 7. 验证命令和结果

已运行治理预检：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py
```

结果：

```json
{
  "passed": true,
  "issues": []
}
```

已运行语法检查：

```powershell
python -m py_compile .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

结果：通过。

已运行猪病 runtime 测试：

```powershell
python -m pytest .\tests\test_swine_llm_wiki_runtime.py -q
```

结果：

```text
9 passed
```

说明：第一次 pytest 命令因工作目录和路径重复写成 `ai-\tests`，导致 pytest 未找到文件；随后已用正确路径 `.\tests\test_swine_llm_wiki_runtime.py` 重跑并通过。

## 8. 预计更新效果

对后续 LLM 维护：

- LLM 进入仓库时会通过 `AGENTS.md` 自动看到猪病 Wiki 强制治理规则。
- 修改后只需优先运行一个命令：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

- 如果只需要轻量检查治理链路，可运行：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py
```

对质量控制：

- 入口文档、变更模板和最新修改记录会被自动检查。
- 后续漏写治理合规记录更容易被发现。
- 猪病 runtime pytest 会同时覆盖数据门禁和治理预检。

对工作汇报：

- 每次修改都能自然形成变更记录。
- 汇报时可以直接引用 `knowledge_change_records/` 中的记录。

## 9. 防乱码措施

本次新增脚本和文档均使用 UTF-8 文本。

新增预检脚本会检查核心治理文档、入口文档和最新 change record 中是否存在 replacement character 或常见 mojibake 字符串。

后续维护仍建议先设置：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

## 10. 残余风险和下一步

当前自动化已经覆盖项目级指令、治理预检和 pytest 回归，但仍有一个可选增强方向：

- 后续可以把 `run_swine_wiki_maintenance_checks.py` 接入 CI 或 pre-commit，使治理检查从“推荐运行”升级为“提交前强制运行”。

本次未修改任何医学事实、source fact、runtime manifest 输入、图谱或 gold dataset 样本。

## 11. 结论

本次优化让猪病 Wiki 后续更新从“人工提醒 LLM 看两份文档”升级为“项目级指令自动提示 + 脚本自动预检 + 一键验收 + pytest 回归”。这样后续维护时操作更少，也更不容易绕过 `WIKI_MAINTENANCE_GUIDE.md` 和 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`。

