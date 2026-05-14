# LLM Wiki 受控更新流程简明说明

本文档用于简明说明一次猪病 LLM Wiki 数据更新，从治理规则读取、CRUD 决策生成、门禁、执行、验收到证据输出的完整调用链。

## 1. 总体调用链

```text
create_crud_decision.py
  -> 读取强制治理文档和 CRUD_DECISION_TEMPLATE.md
  -> 写入带治理文档 hash 和 planned command 的 CRUD 决策文件

run_guarded_wiki_update.py --decision <decision-file> -- <update command>
  -> audit_governance_compliance.py
      检查治理文档、入口文档、必要工具和最新工作留痕
  -> audit_crud_decision.py --decision <decision-file> -- <update command>
      检查 CRUD 决策字段、治理文档 hash、高风险门禁和 planned command 绑定
  -> <update command>
      在 guarded 环境变量下执行真实写库命令
  -> run_swine_wiki_maintenance_checks.py
      更新成功后的总验收入口，按固定顺序运行以下检查
      -> audit_governance_compliance.py
          再次确认治理文档、入口、工具和最新留痕仍完整
      -> build_runtime_core_manifest.py
          重建 runtime manifest，确认默认检索页面清单和路径有效
      -> phase9_rebuild_indexes_graph_smoke.py
          重建 source/disease/drug/rule 等索引、图谱数据和检索 smoke test
      -> audit_graph_change_diff.py
          对比图谱前后快照，生成新增/删除/变化节点和边的 diff
      -> audit_runtime_hallucination_risk.py
          检查 runtime 页面是否新增无来源或高风险幻觉信号
      -> audit_swine_llm_wiki_readiness.py
          检查生成/评估 readiness、缺失路径、规则卡和综合页覆盖
      -> audit_encoding_integrity.py
          检查 UTF-8、乱码、替换字符和 runtime damaged count
      -> pytest tests/test_swine_llm_wiki_runtime.py -q
          运行 runtime 回归测试，验证关键检索和边界规则没有被破坏
  -> guarded_wiki_update_last_run.json
      最近一次 guarded update 的机器可读完整报告
  -> guarded_wiki_update_runs.jsonl
      每次 guarded update 的历史流水日志，便于审计追踪
  -> knowledge_change_records/*.md
      人工可读工作留痕，记录本次判断、修改、旧数据处理和验证结果
```

一句话概括：

> 先由 `create_crud_decision.py` 读取治理文档并生成绑定本次命令的 CRUD 决策文件；再由 `run_guarded_wiki_update.py --decision ...` 执行前置门禁；门禁通过后才给写库脚本传入 guarded 环境并运行真实更新；更新成功后自动执行完整验收并写入机器证据，最后形成工作留痕。

## 2. 第一步：生成绑定式 CRUD 决策文件

不要再手写一个“最新决策文件”让门禁自动猜测。本流程要求先调用固定生成器：

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\create_crud_decision.py `
  --topic "<本次更新主题>" `
  --target-object-type "source/fact/runtime_page/evidence_expansion/rule_card/synthesis/export/graph/gold_sample/other" `
  --target-object-id-path "<目标对象路径或 ID>" `
  --intended-action "create/update/replace/delete/archive/downgrade/exclude/rebuild/migrate" `
  --why "<为什么需要本次操作>" `
  --input-source-type "web/local Markdown/PDF/Word/Excel/raw/issue/model output/script output/human review/not applicable" `
  --old-data-exists "yes/no/unknown" `
  --old-data-handling "keep/update/supersede/downgrade/archive/migrate/exclude/delete/not applicable" `
  --authority-level "A0/A1/A2/SRC/RC-RULE/not applicable" `
  --risk-class "normal/diagnostic/drug_boundary/high_regulatory/withdrawal_mrl_residue/food_safety/not applicable" `
  --source-fact-anchor-available "yes/no/not applicable" `
  --runtime-impact "none/add/update/remove/rebuild" `
  --gold-dataset-impact "none/add/update/exclude/block/rebuild" `
  -- python knowledge/llm_wiki_swine_authoritative/tools/<update_script>.py
```

生成器会读取并记录以下文档的 hash：

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `CRUD_DECISION_TEMPLATE.md`

决策文件会落到：

```text
ai-/knowledge/llm_wiki_swine_authoritative/issues/crud_decisions/YYYY-MM-DD-HHMM-<topic>.md
```

关键点：

- 决策文件包含 `Governance documents read` 和 `Governance document hashes JSON`。
- 决策文件包含 `Planned command`。
- 后续固定入口必须显式传入这一个决策文件。
- `audit_crud_decision.py` 会检查该决策文件是否仍匹配当前治理文档和实际命令。

## 3. 第二步：通过固定入口启动更新

执行命令格式：

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py `
  --decision ai-/knowledge/llm_wiki_swine_authoritative/issues/crud_decisions/<decision-file>.md `
  -- python knowledge/llm_wiki_swine_authoritative/tools/<update_script>.py
```

这里的关键是：

- `--decision` 必填。
- `--decision` 指向本次由 `create_crud_decision.py` 生成的决策文件。
- `--` 后面的内容会进入 `args.command`，也就是实际更新命令。
- `audit_crud_decision.py` 会比较决策文件中的 `Planned command` 和实际 `args.command`。
- 两者不一致时，更新会在 preflight 阶段停止。

## 4. 第三步：固定入口执行更新前门禁

`run_guarded_wiki_update.py` 当前按固定顺序执行两个 preflight：

```text
run_guarded_wiki_update.py
  -> audit_governance_compliance.py
  -> audit_crud_decision.py --decision <decision-file> -- <update command>
```

治理合规检查负责确认：

- 强制治理文档存在；
- README、index、schema、checklist、AGENTS 等入口仍指向治理规则；
- 必要治理工具存在；
- 最新 `knowledge_change_records/*.md` 仍包含治理合规、旧数据、高风险、runtime manifest 和 gold dataset 留痕。

CRUD 决策检查负责确认：

- 决策文件存在且字段完整；
- `Final decision` 必须是 `allowed`；
- 高风险内容必须有匹配的 authority gate；
- create/update/replace 不能缺少 source/fact anchor；
- replace/delete 必须说明旧数据和引用安全；
- governance 文档 hash 必须和当前文档一致；
- `Planned command` 必须和本次真实命令一致。

任一门禁失败时：

- 固定入口写入失败原因；
- 真实更新命令不会执行；
- Wiki 数据不会被写入。

## 5. 第四步：门禁通过后执行真实更新命令

门禁通过后，固定入口会给更新命令注入 guarded 环境：

```text
SWINE_WIKI_GUARDED_UPDATE=1
SWINE_WIKI_CRUD_DECISION=<decision-file>
```

真实更新命令在这个环境下执行：

```text
run_guarded_wiki_update.py
  -> <update command>
```

会修改 Wiki 数据的脚本应调用：

```python
from guarded_update_context import require_guarded_update

def main() -> None:
    require_guarded_update()
    ...
```

这样脚本直接运行时会失败，只有通过 `run_guarded_wiki_update.py --decision ...` 才能执行写库逻辑。

这一环节负责真正修改数据，例如：

- 新增或修改 `wiki/sources/*.md`；
- 新增或修改 facts/index/export；
- 更新 `wiki/diseases/*.md`、`wiki/drugs/*.md` 等 runtime 页面；
- 写入 evidence expansion；
- 更新图谱或 gold dataset 相关输入。

## 6. 第五步：更新成功后执行完整验收

真实更新命令返回 0 后，固定入口调用总验收入口：

```text
run_guarded_wiki_update.py
  -> run_swine_wiki_maintenance_checks.py
```

`run_swine_wiki_maintenance_checks.py` 再按 `CHECKS` 顺序执行：

```python
CHECKS = [
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py"],
    ["knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py"],
    ["knowledge/llm_wiki_swine_authoritative/tools/phase9_rebuild_indexes_graph_smoke.py"],
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_graph_change_diff.py"],
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py"],
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_swine_llm_wiki_readiness.py"],
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_encoding_integrity.py"],
    ["-m", "pytest", "tests/test_swine_llm_wiki_runtime.py", "-q"],
]
```

验收含义：

- manifest 重建确认生产检索 allowlist 可用；
- index/graph smoke 重建索引和知识图谱；
- graph diff 记录图谱变化；
- hallucination risk 检查 runtime 风险；
- readiness 检查知识库是否仍满足生成、评估和 gold dataset 边界；
- encoding audit 检查运行时文件是否出现乱码或损坏；
- pytest 做运行时回归测试。

任一验收失败时：

- 固定入口写入 `post_update_checks_failed`；
- 数据可能已经落盘，但不能视为完成；
- 必须修复后重新通过验收，或在 change record 中记录临时例外、影响范围和后续修复计划。

## 7. 第六步：写入机器运行证据

无论成功还是失败，`run_guarded_wiki_update.py` 都会汇总 `steps` 并写入：

```text
ai-/knowledge/llm_wiki_swine_authoritative/issues/guarded_wiki_update_last_run.json
ai-/knowledge/llm_wiki_swine_authoritative/issues/guarded_wiki_update_runs.jsonl
```

这些文件记录：

- 本次使用的 decision file；
- governance preflight 是否通过；
- CRUD decision preflight 是否通过；
- 真实更新命令是否执行；
- postcheck 是否通过；
- 每一步的 returncode、stdout_tail、stderr_tail；
- 失败原因。

## 8. 第七步：形成工作留痕

最后必须在根目录写入人工可读工作说明：

```text
knowledge_change_records/*.md
```

工作留痕至少应说明：

- 修改前问题；
- 本次为什么修改；
- CRUD 决策文件路径；
- CRUD decision audit 是否通过；
- 旧数据如何处理；
- 高风险门禁影响；
- runtime manifest 影响；
- gold dataset 影响；
- 验证命令和结果；
- 仍然存在的问题和下一步计划。

机器证据来自 `issues/*.json` 和 `issues/*.jsonl`，人工说明来自 `knowledge_change_records/*.md`。两者共同支撑审计、复盘和工作汇报。

## 9. 完整流程连接表

| 环节 | 连接方式 |
|---|---|
| 读取治理文档 | `create_crud_decision.py` 读取 4 份强制治理文档并计算 hash |
| 创建 CRUD 决策 | 生成到 `issues/crud_decisions/*.md` |
| 决策绑定命令 | 决策文件写入 `Planned command` |
| 固定入口启动 | `run_guarded_wiki_update.py --decision <file> -- <update command>` |
| 治理门禁 | `audit_governance_compliance.py` |
| CRUD 门禁 | `audit_crud_decision.py --decision <file> -- <update command>` |
| 防绕过执行 | 固定入口注入 `SWINE_WIKI_GUARDED_UPDATE=1` |
| 写库脚本自检 | 写库脚本调用 `require_guarded_update()` |
| 更新后验收 | `run_swine_wiki_maintenance_checks.py` 调用完整 `CHECKS` |
| 运行证据 | `write_report(payload)` 写入 JSON 和 JSONL |
| 工作留痕 | 写入 `knowledge_change_records/*.md` |

## 10. 汇报用简短表述

当前猪病 LLM Wiki 更新流程采用绑定式受控执行。更新前先由 `create_crud_decision.py` 读取强制治理文档并生成 CRUD 决策文件，决策文件记录治理文档 hash、目标对象、操作类型、旧数据处理、高风险门禁、runtime/gold 影响和 planned command。执行时必须通过 `run_guarded_wiki_update.py --decision <file> -- <update command>` 启动，入口先运行治理合规检查，再运行 CRUD 决策检查，并确认决策文件与实际命令一致。门禁通过后，入口给更新脚本注入 guarded 环境变量，写库脚本可通过 `require_guarded_update()` 阻止直接绕过执行。更新成功后，入口自动运行 manifest、图谱、graph diff、风险、readiness、编码和 pytest 验收，并写入 JSON/JSONL 机器证据。最后在 `knowledge_change_records` 中形成可读工作留痕。

## 11. 关键脚本职责

| 脚本 | 职责 |
|---|---|
| `tools/create_crud_decision.py` | 读取治理文档和模板，生成带 hash 与 planned command 的 CRUD 决策文件 |
| `tools/run_guarded_wiki_update.py` | 固定入口，要求 `--decision`，调度 preflight、真实更新、postcheck 和运行证据 |
| `tools/audit_governance_compliance.py` | 检查治理文档、入口文档、必要工具和最新工作留痕 |
| `tools/audit_crud_decision.py` | 检查 CRUD 决策字段、治理 hash、高风险门禁和命令绑定 |
| `tools/guarded_update_context.py` | 提供 `require_guarded_update()`，供写库脚本防止直接绕过执行 |
| `tools/run_swine_wiki_maintenance_checks.py` | 更新后总验收入口 |
| `tools/build_runtime_core_manifest.py` | 重建 runtime manifest |
| `tools/phase9_rebuild_indexes_graph_smoke.py` | 重建索引和知识图谱，并执行 smoke 检查 |
| `tools/audit_graph_change_diff.py` | 输出图谱变化 diff 和相关证据 |
| `tools/audit_runtime_hallucination_risk.py` | 检查 runtime 幻觉和护栏风险 |
| `tools/audit_swine_llm_wiki_readiness.py` | 检查知识库生成、评估和 gold dataset readiness |
| `tools/audit_encoding_integrity.py` | 检查编码完整性和 runtime 乱码风险 |
