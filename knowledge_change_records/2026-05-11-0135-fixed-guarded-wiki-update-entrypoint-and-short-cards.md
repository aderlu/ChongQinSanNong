# 猪病 LLM Wiki 固定更新入口与短执行卡落地记录

## 1. Landing Time

- Landing date: 2026-05-11
- Landing time: 01:35
- Time zone: Asia/Shanghai
- Change type: fixed update entrypoint, short execution cards, governance automation, validation hardening

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: not applicable
- Fixed update entrypoint used: not applicable for creating the entrypoint itself; future updates must use `run_guarded_wiki_update.py`
- Source/fact CRUD type: update governance tooling and documentation
- Input source type: local Markdown governance documents and local Python tooling
- Old data handling: keep existing long governance documents; add short execution cards and fixed guarded entrypoint
- If old data changed, factual reason: no biomedical old data changed; workflow rules were strengthened to reduce LLM omission and manual operation
- High-risk gate impact: strengthens future high-risk gate enforcement; no high-risk fact changed
- Runtime manifest impact: none in this change
- Gold dataset impact: none in this change

## 2. 修改目标

本次目标是把后续猪病 LLM Wiki 的所有更新操作设计为固定入口执行，并新增两份短执行卡，降低 LLM 每次读取长文档时遗漏规则或跑偏的风险。

目标包括：

1. 所有会修改 Wiki 的人工触发、LLM 触发、脚本触发、定时任务触发更新，都通过固定入口执行。
2. 固定入口自动执行治理预检、具体更新命令和完整验收。
3. 新增两份短执行卡，让 LLM 每次先读短卡，遇到具体场景再查长文档。
4. 将短执行卡和固定入口挂入 AGENTS、README、维护指南、CRUD 规范、checklist、change record template 和治理预检脚本。
5. 每次修改继续在 `knowledge_change_records/` 留痕。
6. 保持 UTF-8 和乱码防护要求。

## 3. 修改前存在的问题

修改前已经有：

- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `audit_governance_compliance.py`
- `run_swine_wiki_maintenance_checks.py`

但仍存在以下问题：

1. 没有固定入口包裹实际更新命令。
2. 定时任务或人工脚本仍可能直接调用某个更新脚本，绕过治理预检和完整验收。
3. 两份完整制度文档较长，LLM 每次完整读取时可能抓不住任务最相关的执行项。
4. 没有短执行卡帮助 LLM 快速判断来源类型、CRUD 类型、落位、高风险、旧数据处理和验收要求。
5. 没有自动检查固定入口是否存在，也没有测试固定入口 dry-run 行为。

## 4. 修改前代码状态

修改前相关代码状态：

- `audit_governance_compliance.py`
  - 能检查两份长治理文档、入口文件和最新变更记录。
  - 但不检查短执行卡和固定更新入口。

- `run_swine_wiki_maintenance_checks.py`
  - 能一键执行治理预检、manifest、风险审计、readiness、编码审计和 pytest。
  - 但只用于更新后验收，不能包裹实际更新命令。

- `AGENTS.md`
  - 已要求 LLM 遵守两份长治理文档。
  - 但未要求所有更新命令通过固定入口执行。

- `test_swine_llm_wiki_runtime.py`
  - 已测试治理预检通过。
  - 但未测试固定入口脚本存在和 dry-run 行为。

## 5. 本次新增或更新了什么代码

新增固定入口脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py`

该脚本逻辑：

1. 先运行 `audit_governance_compliance.py`。
2. 如果治理预检失败，直接失败退出。
3. 如果传入 `--dry-run`，只报告将要执行的命令，不执行更新和后置验收。
4. 如果治理预检通过，执行 `--` 后面的具体更新命令。
5. 更新命令成功后，自动运行 `run_swine_wiki_maintenance_checks.py`。
6. 任一步失败，整体任务失败。
7. 将最近一次运行报告写入 `wiki/issues/guarded_wiki_update_last_run.json`。

新增两份短执行卡：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_SCENARIO_SHORT_CARD.md`

更新治理预检脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py`

新增检查：

- 两份短执行卡是否存在。
- 固定入口脚本是否存在。
- README、index、schema、checklist、template、AGENTS 是否引用短卡和长文档。
- 最新 change record 是否包含短卡和固定入口相关信息。

更新测试：

- `ai-/tests/test_swine_llm_wiki_runtime.py`

新增测试：

- `test_swine_wiki_guarded_update_entrypoint_exists_and_supports_dry_run`

## 6. 本次更新或整理了什么文档

更新：

- `ai-/AGENTS.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/README.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/SOURCE_BATCH_INTAKE_CHECKLIST.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/CHANGE_RECORD_TEMPLATE.md`

整理结果：

- 后续 LLM 每次更新前先读两份短执行卡。
- 复杂场景再查两份完整制度文档。
- 所有更新命令必须通过 `run_guarded_wiki_update.py` 固定入口。
- checklist 和模板中加入短卡、固定入口检查项。

## 7. 修改后解决了什么问题

修改后解决的问题：

1. 后续更新不再需要人工记住先跑预检再跑验收，固定入口会自动串起来。
2. 后续定时任务可以统一调用固定入口，避免直接运行更新脚本。
3. LLM 不必每次从两份长文档中重新提炼所有规则，先读短卡即可掌握关键动作。
4. 复杂场景仍有完整制度文档作为权威依据。
5. 治理预检会检查短卡、固定入口和最新变更记录，减少治理链路断裂。
6. pytest 会检查固定入口 dry-run 行为，避免脚本被破坏而无人发现。

## 8. 固定入口使用方式

以后所有修改 Wiki 的命令，都应使用：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python <你的更新脚本或命令>
```

示例：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\some_future_update.py
```

只检查将执行什么，不真正执行更新：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py --dry-run -- python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\some_future_update.py
```

## 9. 预计更新效果

对 LLM 执行：

- 先读短卡，减少规则遗漏。
- 通过固定入口自动执行预检和验收，减少人工步骤。

对定时任务：

- 定时任务只需要调用固定入口，而不是直接调用更新脚本。
- 如果治理预检或验收失败，定时任务会失败退出，避免坏数据静默进入 Wiki。

对知识库质量：

- 更难绕过来源、事实、旧数据处理、高风险门禁、编码和留痕要求。
- 所有更新更容易形成可汇报、可追溯的记录。

## 10. 防乱码措施

本次新增的短执行卡、固定入口脚本和变更记录均使用 UTF-8。

固定入口运行时会设置 `PYTHONIOENCODING=utf-8`。

后续仍建议维护前设置：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

治理预检脚本会检查核心治理文件和最新变更记录是否存在 replacement character 或常见 mojibake 字符串。

## 11. 验证

已运行验证命令：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py
python -m py_compile .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py
python -m pytest .\tests\test_swine_llm_wiki_runtime.py -q
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py --dry-run -- python -c "print('noop')"
```

结果：

```json
{
  "governance_preflight": "passed",
  "py_compile": "passed",
  "pytest": "10 passed",
  "guarded_update_dry_run": "passed"
}
```

本次未修改医学事实、source fact、runtime manifest 输入、图谱或 gold dataset 样本。

## 12. 残余风险和下一步

固定入口已经完成，但要让定时任务真正强制走该入口，需要后续把 Windows 计划任务或其他调度器的命令改为调用：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python <实际更新脚本>
```

如果未来新增新的更新脚本，也应在脚本说明和 change record 中声明必须由固定入口调用。

## 13. 结论

本次将猪病 Wiki 更新流程升级为“短执行卡优先读取 + 固定入口执行更新 + 自动预检 + 自动验收 + 工作留痕”的闭环。后续人工、LLM 或定时任务触发的更新，都可以通过 `run_guarded_wiki_update.py` 统一执行，从流程上减少绕过两份治理文档的风险。
