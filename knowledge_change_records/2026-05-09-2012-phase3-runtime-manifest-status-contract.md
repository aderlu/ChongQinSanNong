# Phase 3 Runtime Manifest Status Contract

Date: 2026-05-09

## 修改目标和范围

执行猪病 LLM Wiki 清洗整理 Phase 3：强化 runtime allowlist/denylist，并让 runtime manifest 使用新的主状态字段，不再以 legacy `evidence_status` 作为事实可用性门槛。

修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest_summary.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_exclude_patterns.json`

## 修改前存在的问题

修改前 manifest 构建器主要写入：

- `evidence_status`
- `runtime_tier`
- `allowed_use`
- `blocked_use`
- `source_ids`

但执行文档已经要求可用性由来源清晰、数据有效、来源等级匹配任务用途决定。旧 manifest 缺少：

- `source_status`
- `fact_validity`
- `authority_level`
- `risk_class`
- `task_use_status`
- `gold_dataset_role`

同时 `runtime_core_reviewed` 仍带有 review 语义，容易让后续 loader/exporter 继续把复核状态当作门槛。

## 修改前代码状态

`build_runtime_core_manifest.py` 中：

- disease 页按 `coverage_gap_status` 映射为 `runtime_core_reviewed` 或 `runtime_core_partial`。
- drug 页按 `status` 映射为 `runtime_core_reviewed`、`runtime_core_partial` 或 `candidate_or_incomplete`。
- rule_card 和 syndrome 人工写入 `HUMAN_REVIEWED`。
- exclude patterns 未排除 `wiki/phase*/**` 和 `wiki/knowledge-graph.md`。

## 本次更新或新增了什么代码

更新 `build_runtime_core_manifest.py`：

1. 新增状态推断函数：
   - `authority_from_sources`
   - `source_status_for`
   - `fact_validity_for`

2. `add_entry` 新增主字段：
   - `source_status`
   - `fact_validity`
   - `authority_level`
   - `risk_class`
   - `task_use_status`
   - `gold_dataset_role`
   - `legacy_evidence_status`

3. 将 `runtime_core_reviewed` 改为 `runtime_core_source_anchored`。

4. 增加 manifest 顶层 `status_contract`，说明主字段和 legacy 字段。

5. 扩展 denylist：
   - `wiki/knowledge-graph.md`
   - `wiki/phase*/**`

## 本次进行了什么整理工作

重建 runtime manifest：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
```

结果：

- entries: 198。
- missing_paths: 0。
- runtime tier:
  - runtime_core_guardrail: 15。
  - runtime_core_partial: 41。
  - runtime_core_policy: 4。
  - runtime_core_source_anchored: 138。

## 修改后解决了什么

- manifest 明确使用新状态契约。
- legacy `evidence_status` 被保留为兼容字段，但不再是唯一判断依据。
- 生产/评估 runtime allowlist 更清晰。
- denylist 更完整，避免 phase construction 目录和 Markdown graph 被默认检索。

## 预计更新效果

- 后续 runtime loader/exporter 可以直接使用 `source_status + fact_validity + authority_level + risk_class + task_use_status`。
- 减少旧 review 字段误伤来源清晰事实的风险。
- 为 Phase 6 复核状态去门槛化打下代码基础。

## 验证

已运行：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- manifest entries: 198。
- manifest missing_paths: 0。
- hallucination risk high: 0。
- hallucination risk medium: 0。
- readiness_score: 99。

## 残余风险和下一步

本阶段更新了 manifest 生成逻辑，但 runtime loader/exporter 的实际调用侧仍需在 Phase 6 中全面迁移到新状态字段。
