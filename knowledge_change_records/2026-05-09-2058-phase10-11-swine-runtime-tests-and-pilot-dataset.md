# Phase 10/11 猪病专用测试、CI 化约束与黄金数据集试生产执行记录

Date: 2026-05-09 20:58

Target: `ai-/knowledge/llm_wiki_swine_authoritative`

## 1. 修改目标和范围

本次执行 Phase 10 和 Phase 11：

- Phase 10：新增猪病 LLM Wiki 专用 regression tests，把 runtime manifest、denylist、黄金数据集门禁、药物高风险门槛、partial 页面路由、编码完整性和试生产样本 provenance 变成可重复验证的工程约束。
- Phase 11：从清洗后的知识库中试生产小批量黄金数据集样本，并做自动抽检，确认 source/fact/rule provenance、JSON 字段和高风险边界。

涉及范围：

- `ai-/tests/`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/`
- 兼容性修复涉及 `src/chicken_data_synthesis/infrastructure/knowledge/`

## 2. 修改前存在的问题

修改前主要问题：

- 只有历史 `test_llm_wiki_knowledge.py`，测试 fixture 仍是鸡病兼容场景，没有猪病 runtime 专用测试。
- Phase 6-9 生成的 runtime manifest、gold dataset readiness、drug gold role、hard-block rules、检索 smoke test、编码审计和 pilot dataset 没有统一 pytest 约束。
- 尚未从 `train_ready`、`eval_ready`、drug `negative_trap`、`generation_ready_limited` 四类任务流生成小批量试生产样本。
- 没有 `issues/gold_dataset_pilot_inspection_2026-05-09.md/json` 报告用于汇报 provenance 完整率和高风险越界率。
- 历史兼容测试暴露出既有治理接口变更后的兼容问题：
  - `source_create`、`ingest_source`、`ingest_url_source`、`ingest_text_source`、`batch_ingest_sources` 在旧调用方式下没有传 reason，会被新治理校验阻断。
  - `run_daily_maintenance` 的 fake client 旧签名不支持 `protocol_context` 参数。
  - `delete_source` 把 `exports/knowledge_facts.candidates.json` 候选暂存文件也当作正式强引用，导致旧工作流删除测试失败。

## 3. 修改前相关代码和数据状态

修改前：

- `ai-/tests/test_llm_wiki_knowledge.py` 仍保留鸡病测试，用于历史兼容。
- 不存在 `ai-/tests/test_swine_llm_wiki_runtime.py`。
- 不存在 `tools/phase11_pilot_gold_dataset.py`。
- 不存在 pilot JSONL：
  - `exports/pilot_gold_dataset/pilot_train_20260509.jsonl`
  - `exports/pilot_gold_dataset/pilot_eval_20260509.jsonl`
  - `exports/pilot_gold_dataset/pilot_negative_trap_20260509.jsonl`
  - `exports/pilot_gold_dataset/pilot_limited_20260509.jsonl`
- 不存在 `issues/gold_dataset_pilot_inspection_2026-05-09.md/json`。

## 4. 本次更新或新增了什么代码

新增测试：

- `ai-/tests/test_swine_llm_wiki_runtime.py`

覆盖内容：

- load swine runtime manifest。
- denylist excludes raw/issues/graph/matrices。
- `task_use_status` 控制 exporter 允许/禁止。
- drug high-risk claims require A0/label-level source。
- partial pages route to gap handling。
- exporter hard-block rules 覆盖 Phase 8 所需失败类型。
- encoding integrity report 和 runtime retrieval smoke test 通过。
- Phase 11 pilot samples 全部带 source/rule provenance。

新增试生产脚本：

- `tools/phase11_pilot_gold_dataset.py`

脚本功能：

- 从 `exports/gold_dataset_readiness_index.csv` 抽取 `train_ready` 样本。
- 从 `eval_ready` 的 comparison/syndrome/rule/synthesis 样本生成评估集。
- 从 `exports/drug_gold_role_index.csv` 抽取 drug `negative_trap` 样本。
- 从 `generation_ready_limited` 抽取带边界候选样本。
- 输出 JSONL 和自动抽检报告。

兼容性修复：

- `src/chicken_data_synthesis/infrastructure/knowledge/operations.py`
  - `source_create`、`ingest_source`、`ingest_url_source`、`ingest_text_source` 在旧调用方式下自动补入默认审计 reason/evidence。
  - 删除等危险操作仍保持显式 reason 要求。

- `src/chicken_data_synthesis/infrastructure/knowledge/lifecycle.py`
  - `batch_ingest_sources` 在旧调用方式下自动补入默认审计 reason/evidence。
  - 删除引用扫描时排除 `knowledge_facts.candidates.json` 候选暂存文件，避免把候选层误当正式强引用。

- `src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py`
  - `run_daily_maintenance` 兼容旧 fake client 签名；当 client 不接受 `protocol_context` 时自动降级为旧参数调用。

## 5. 本次进行了什么知识整理、样本生成或索引重建

本次未重写实体页事实内容，主要完成测试化、试生产和验收报告整理。

生成试生产样本：

- `exports/pilot_gold_dataset/pilot_train_20260509.jsonl`: 8 条
- `exports/pilot_gold_dataset/pilot_eval_20260509.jsonl`: 8 条
- `exports/pilot_gold_dataset/pilot_negative_trap_20260509.jsonl`: 8 条
- `exports/pilot_gold_dataset/pilot_limited_20260509.jsonl`: 8 条

生成抽检报告：

- `issues/gold_dataset_pilot_inspection_2026-05-09.json`
- `issues/gold_dataset_pilot_inspection_2026-05-09.md`

试生产总计：

- total_samples: 32
- group_counts:
  - pilot_train: 8
  - pilot_eval: 8
  - pilot_negative_trap: 8
  - pilot_limited: 8

## 6. 修改后解决了什么问题

修改后：

- 猪病 runtime 质量不再只靠人工查看报告，而是有独立 pytest 文件约束。
- 历史鸡病兼容测试未被替换，仍可运行并通过。
- 试生产样本全部保留 source/rule provenance。
- 药物负样本陷阱明确拒绝非 A0/标签级来源下的正向剂量、疗程、休药期输出。
- 高风险正向生成门槛和 Phase 8 hard-block rules 已进入测试。
- 旧治理接口兼容恢复，同时不放松删除来源时的显式 reason 要求。

## 7. 预计更新效果

对生成：

- 后续批量生成前可以先跑 `test_swine_llm_wiki_runtime.py`，确认 runtime allowlist、denylist 和 task-use 门禁没有回退。
- `pilot_train` 只提供来源锚定的受控临床摘要样本，不生成独立处方、剂量、休药期、MRL 或监管执行结论。

对评估：

- `pilot_eval` 和 hard-block rule tests 能检查无来源、过度外推、单次检测因果过度解释、来源等级不匹配等失败模式。

对检索：

- 测试固定检查 runtime retrieval smoke test，不允许 raw、issues、graph 和巨大矩阵进入默认检索。

对黄金数据集生产：

- 试生产样本分为 `pilot_train`、`pilot_eval`、`pilot_negative_trap`、`pilot_limited`，可作为后续人工抽检和批量生产的模板。
- `gold_dataset_pilot_inspection` 明确 provenance 完整率、高风险越界率、JSON 完整性和是否通过。

## 8. 验证命令和结果

所有命令均在 PowerShell 下设置 UTF-8 后执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

试生产：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase6_7_review_status_and_gold_dataset.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase11_pilot_gold_dataset.py
```

结果：

- runtime manifest entries: 204
- manifest missing_paths: 0
- pilot total_samples: 32
- provenance_complete_rate: 1.0
- missing_provenance: []
- high_risk_overreach: []
- incomplete_json: []
- manual_inspection_pass_rate: 1.0
- acceptance passed: true

Phase 10 猪病专用测试：

```powershell
python -m pytest .\ai-\tests\test_swine_llm_wiki_runtime.py -q
```

结果：

- 8 passed

历史兼容测试：

```powershell
python -m pytest .\ai-\tests\test_llm_wiki_knowledge.py -q
```

结果：

- 27 passed
- 2 warnings 来自第三方 `deepeval` 的 Python 3.14 deprecation warning。
- pytest session finish 后出现 Windows 临时目录清理 PermissionError，但测试结果为通过；该问题是测试框架清理临时目录的系统权限提示，不影响断言结果。

通用审计：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
```

- entries_checked: 204
- high: 0
- medium: 0

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

- readiness_score: 99
- missing_paths: 0
- bad_fact_tables: []
- missing_rule_cards: []
- missing_synthesis: []

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

- text_files_scanned: 2313
- runtime_manifest_paths_loaded: 204
- encoding_ok: 2301
- decode_or_replacement_damage: 3
- mojibake_like_content: 0
- minor_mojibake_signal: 9
- runtime_damaged_count: 0

## 9. 仍然存在的风险和下一步待办

仍然存在：

- Phase 11 试生产样本是 gate-validation pilot，不是最终可直接投产训练集；仍需领域专家抽查代表性措辞和问题覆盖。
- 非 runtime 文件仍存在 3 个 decode/replacement damage 和 9 个 minor mojibake signal；runtime_damaged_count=0，本次没有扩大处理 raw/历史材料。
- 第三方 `deepeval` 在 Python 3.14 下有 deprecation warning，当前不影响测试通过。
- pytest 结束时偶发 Windows 临时目录清理权限提示，当前不影响测试结论。

下一步建议：

- 进入 Phase 11 后续人工抽检：抽查 32 条 pilot 样本的问题表达、答案边界和来源锚点是否满足项目口径。
- 扩展 pilot 到更大批量前，先把 `phase11_pilot_gold_dataset.py` 的样本生成模板改为项目最终 QA schema。
- 将 `python -m pytest .\ai-\tests\test_swine_llm_wiki_runtime.py -q` 加入后续 CI 或批处理验收命令。
