# Phase 6/7 复核状态去门槛化与黄金数据集用途分层执行记录

Date: 2026-05-09 20:29

Target: `ai-/knowledge/llm_wiki_swine_authoritative`

## 1. 修改目标和范围

本次执行 Phase 6 和 Phase 7，目标是把 `HUMAN_REVIEWED`、`NEEDS_REVIEW` 等复核状态从可用性门槛降级为历史审计字段，并建立黄金数据集生产前置门禁。

涉及范围：

- runtime manifest 构建逻辑。
- hallucination risk audit 和 readiness audit。
- source/fact 状态标准化脚本。
- Phase 4/5/9 运行时维护脚本的 legacy 字段兼容。
- 黄金数据集 readiness index 和 drug gold role index。
- schema 和维护指南。

## 2. 修改前存在的问题

修改前主要问题：

- `exports/runtime_core_manifest.json` 同时输出 `evidence_status` 和 `legacy_evidence_status`，容易让后续 loader/exporter 误把复核状态继续当主门槛。
- `audit_runtime_hallucination_risk.py` 会把页面正文前部出现 `NEEDS_REVIEW` 或 partial tier 直接计为风险，没有区分来源是否清晰、事实是否有效、是否有 gap-routing。
- `drug_gold_role_index.csv` 已存在，但字段仍以 `evidence_status` 为主，缺少 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status` 等 Phase 6 主判断字段。
- 缺少 `exports/gold_dataset_readiness_index.csv`，无法从 manifest 层明确区分 `train_ready`、`eval_ready`、`generation_ready_limited`、`retrieval_only`、`blocked`。
- 部分维护脚本仍从 manifest 读取 `evidence_status`，在 manifest 去门槛化后可能读不到状态。
- schema 尚未完整写明黄金数据集字段和药物页正向生成门槛。

## 3. 修改前相关代码和数据状态

修改前：

- `tools/build_runtime_core_manifest.py` 根据 disease/drug index 构建运行时 allowlist，但 manifest entry 中仍保留 `evidence_status`。
- `tools/audit_runtime_hallucination_risk.py` 旧逻辑会产生 `partial_or_needs_review` 风险项。
- `exports/drug_gold_role_index.csv` 只有 `drug_id,title,gold_dataset_use,evidence_status,page_relpath` 等窄字段。
- `exports/gold_dataset_readiness_index.csv` 不存在。
- `exports/knowledge_facts_status_index.json` 中仍可能保留原始 `evidence_status` 字段。

## 4. 本次更新或新增的代码

更新代码：

- `tools/build_runtime_core_manifest.py`
  - 新增 `allowed_question_types` 和 `blocked_question_types`。
  - manifest version 更新为 `phase6-phase7-runtime-core-v2`。
  - manifest status contract 明确 legacy 字段只保留 `legacy_evidence_status`。
  - `review` 类监管提示不再直接等同强阻断；只有明确 `regulatory_anchor_required=yes` 且缺少 A0 时才降级为高监管受限用途。
  - comparison/syndrome 派生运行时页补齐 `authority_level=SRC`。

- `tools/phase6_7_review_status_and_gold_dataset.py`
  - 新增脚本，用 manifest 生成 Phase 6 迁移报告和 Phase 7 黄金数据集门禁表。
  - 输出 `exports/gold_dataset_readiness_index.csv`。
  - 重建 `exports/drug_gold_role_index.csv`。
  - 输出 `issues/review_status_migration_2026-05-09.json`。

- `tools/audit_runtime_hallucination_risk.py`
  - 不再因 `NEEDS_REVIEW` 字符串本身扣分。
  - 改为检查 `source_status`、`fact_validity`、高风险无 A0、药物/休药期/监管规则卡缺失等实际风险。

- `tools/audit_swine_llm_wiki_readiness.py`
  - 将 `needs_review_frontmatter` 改为 `legacy_review_frontmatter`，复核字段只作为历史标记统计。

- `tools/standardize_source_fact_status.py`
  - 标准化 fact 状态时将原 `evidence_status` 迁移为 `legacy_evidence_status`。

- `tools/phase4_apply_drug_guardrail_anchors.py`
- `tools/phase5_apply_disease_guardrail_anchors.py`
- `tools/phase9_runtime_cleanup_regression.py`
- `tools/validate_swine_p0_runtime.py`
  - 改为读取或展示 `legacy_evidence_status` / legacy audit status。

- `.wiki-schema.md`
  - 新增 Gold Dataset Contract。
  - 明确药物页 role：`boundary_only`、`negative_trap`、`exclude_from_positive_generation`、`positive_label_candidate`。

- `WIKI_MAINTENANCE_GUIDE.md`
  - 将“无来源事实按 NEEDS_REVIEW 处理”改为 `source_missing` + `fact_validity: insufficient_anchor`。

## 5. 本次进行了什么整理、迁移或索引重建

本次未重写疾病/药物实体正文，主要进行代码、manifest、导出索引和状态契约整理。

重建或新增导出：

- `exports/runtime_core_manifest.json`
- `exports/runtime_exclude_patterns.json`
- `exports/runtime_core_manifest_summary.md`
- `exports/gold_dataset_readiness_index.csv`
- `exports/drug_gold_role_index.csv`
- `exports/knowledge_facts_status_index.json`
- `exports/source_authority_status_index.csv`
- `issues/review_status_migration_2026-05-09.json`
- `issues/runtime_hallucination_risk_audit_2026-05-09.json`
- `issues/runtime_hallucination_risk_audit_2026-05-09.md`
- `issues/source_fact_authority_status_audit_2026-05-09.json`
- `issues/source_fact_authority_status_audit_2026-05-09.md`

## 6. 修改后解决的问题

修改后：

- 运行时 manifest 主判断字段统一为 `source_status + fact_validity + authority_level + risk_class + task_use_status`。
- `evidence_status` 不再作为 manifest 主字段输出，历史状态只保留为 `legacy_evidence_status`。
- readiness audit 不再把 legacy review 字段作为质量失败。
- hallucination risk audit 不再把 `NEEDS_REVIEW` 本身视为风险，而是检查来源缺失、事实无效、高风险无 A0、规则卡缺失。
- 黄金数据集门禁表已经可以直接判断：
  - 是否允许正向生成。
  - 是否允许 negative trap。
  - 是否允许 evaluation。
  - 需要哪些 rule cards。
  - 缺少哪些关键字段。
- 药物页单独生成 `drug_gold_role_index.csv`，未满足 A0/标签级来源的药物页不会被标为正向生成来源。

## 7. 预计更新效果

对生成：

- 普通临床、来源清晰、事实有效、非强监管高风险页面可以进入受控生成。
- 高监管、休药期、MRL、残留、食品安全、药物剂量/疗程等内容会被 rule card 和 A0/标签级来源门槛限制。

对评估：

- `eval_ready` 和 `generation_ready_limited` 页面可进入评估和陷阱样本构建。
- 评估器更容易惩罚无来源、高风险外推和药物越界。

对检索：

- runtime manifest 继续作为 allowlist，raw/issues/graph/巨大矩阵仍由 denylist 排除。
- partial 页面不再因为 legacy review 字段被整体否定，而是用于召回、鉴别路由和缺口处理。

对黄金数据集生产：

- `gold_dataset_readiness_index.csv` 提供统一入口。
- `drug_gold_role_index.csv` 提供药物专用门禁。
- 任一导出样本后续可按 `source_ids`、`rule_card_ids` 和 allowed/blocked question types 做前置检查。

## 8. 验证命令和结果

所有命令均在 PowerShell 下设置 UTF-8 后执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

运行结果：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
```

- entries: 198
- missing_paths: 0

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase6_7_review_status_and_gold_dataset.py
```

- entries: 198
- drug_entries: 80
- task_use_counts:
  - generation_ready_limited: 113
  - train_ready: 31
  - eval_ready: 46
  - retrieval_only: 8
- blocked_reason_counts: 0

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
```

- entries_checked: 198
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

- text_files_scanned: 2296
- runtime_manifest_paths_loaded: 198
- encoding_ok: 2284
- decode_or_replacement_damage: 3
- mojibake_like_content: 0
- minor_mojibake_signal: 9
- runtime_damaged_count: 0

额外检查：

- `runtime_core_manifest.json` 不再输出 `"evidence_status"` 主字段，只保留 `"legacy_evidence_status"`。
- `gold_dataset_readiness_index.csv` 中 `missing_critical_fields` 为 0。
- 非 A0 药物页 `positive_generation_allowed=true` 数量为 0。

## 9. 仍然存在的风险和下一步待办

仍然存在：

- 历史批处理脚本、旧导出、实体页 frontmatter 和历史记录中仍可见 `HUMAN_REVIEWED`、`NEEDS_REVIEW`、`evidence_status`，但本次已将当前 runtime manifest、fact status index 和黄金数据集门禁迁移到主状态字段。
- `knowledge_facts.json` 作为历史事实原表仍保留原始 `evidence_status`，当前标准化产物 `knowledge_facts_status_index.json` 已迁移为 `legacy_evidence_status`。
- 编码审计显示 runtime_damaged_count=0，但非 runtime 文件仍有少量 decode/replacement damage 和 minor signal，后续 Phase 9/10 前建议继续隔离 raw/历史材料。

下一步建议：

- Phase 8 加固 rule cards 与 exporter hard-block checks。
- Phase 9 重建索引/图谱并做检索 smoke test。
- Phase 10 增加猪病专用测试，覆盖 `gold_dataset_readiness_index.csv`、`drug_gold_role_index.csv` 和高风险 A0 门禁。
