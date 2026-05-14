# Phase 4 Entity Runtime Compaction

Date: 2026-05-09

## 修改目标和范围

执行猪病 LLM Wiki 清洗整理 Phase 4：清理 `wiki/diseases/` 和 `wiki/drugs/` 实体页中的历史批次块、补强块、增强块和构建期分节，迁移到 evidence expansion 层，让 runtime 实体页保持紧凑、清晰、可检索，并保留原始来源追溯。

新增或修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/compact_entity_runtime_pages.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_entity_runtime_compaction.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/entity_runtime_compaction_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/entity_runtime_compaction_2026-05-09.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/entity_runtime_compaction_cumulative_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/entity_runtime_compaction_cumulative_2026-05-09.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/diseases/phase4_runtime_compaction/**`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/drugs/phase4_runtime_compaction/**`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/*.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/drugs/*.md`

## 修改前存在的问题

修改前 disease/drug 页中存在大量历史构建痕迹：

- `Formal Disease Completion / V5`
- `Dataset QA Reinforcement / V6`
- `Web Source Reinforcement / V11`
- `Raw MD textbook evidence / V12`
- `V13.1 batch`
- `RAU_*_V14`
- `DOS_1_200_REVIEW_REINFORCEMENT`
- `_START/_END` 批次块标记

这些内容在构建期有价值，但长期留在 runtime 页会造成：

- 同类事实分散在多个批次块。
- 检索命中旧批次内容而非当前 runtime 摘要。
- 页面冗长、重复、难以审核。
- 黄金数据集可能误采候选抽取或旧增强内容。

## 修改前代码状态

修改前没有专门的实体页压缩迁移工具。只能通过 `rg` 手工查找批次块，无法保证：

- 迁移后来源锚点仍保留。
- 页面统一生成证据扩展索引。
- 后续可以审计剩余旧标题和 `_START/_END` 标记。

## 本次更新或新增了什么代码

新增 `compact_entity_runtime_pages.py`：

- 扫描 `wiki/diseases/` 和 `wiki/drugs/`。
- 识别 `_START/_END` 标记块。
- 识别包含 V 批次、Reinforcement、补强、增强、Completion、Batch 等构建期 H2 标题。
- 将这些内容迁移到 `wiki/evidence_expansions/{diseases,drugs}/phase4_runtime_compaction/<entity>/`。
- 在实体页追加统一的 `## 证据扩展索引`。
- 保留每个迁移块中的 `source_id`、`fact_id`、页码、URL、规则卡等原始追溯信息。
- 可重复运行，保留已有证据扩展索引，避免覆盖前次结果。

新增 `audit_entity_runtime_compaction.py`：

- 统计 disease/drug 页面数量。
- 统计 evidence expansion 文件数量。
- 检查剩余旧 V 批次/补强/增强标题和 `_START/_END` 标记。
- 统计最大 runtime 页面大小。

## 本次进行了什么整理工作

执行实体页压缩迁移：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\compact_entity_runtime_pages.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_entity_runtime_compaction.py
```

累计结果：

- pages_scanned: 154。
- evidence_expansion_files_total: 612。
- disease expansion files: 367。
- drug expansion files: 245。
- pages_with_evidence_expansion_index: 145。
- remaining_legacy_heading_or_marker_pages: 0。
- remaining_legacy_heading_or_marker_hits: 0。
- max_runtime_page_bytes: 13065。

## 修改后解决了什么

- disease/drug runtime 页不再长期保留旧 V 批次/补强/增强标题。
- `_START/_END` 构建期块已迁出默认 runtime。
- 原始来源锚点没有丢弃，而是保存在 evidence expansion 文件中。
- 默认生产/评估检索看到的是紧凑实体页，而不是历史构建堆叠。
- 页面大小显著降低，最大 runtime 页约 13 KB，低于 20 KB 维护阈值。

## 预计更新效果

- 降低检索噪声。
- 降低候选事实和旧批次事实被误采为最终答案的风险。
- 提高 disease/drug 页面可读性。
- 为后续 Phase 6 exporter/loader 状态迁移提供更干净的 runtime 输入。

## 验证

已运行：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\audit_entity_runtime_compaction.py
python knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- remaining_legacy_heading_or_marker_hits: 0。
- manifest missing_paths: 0。
- hallucination risk high: 0。
- hallucination risk medium: 0。
- runtime_damaged_count: 0。
- readiness_score: 99。

## 残余风险和下一步

本阶段迁移了构建期块，但实体页正文中仍可能存在 legacy frontmatter 字段如 `evidence_status=NEEDS_REVIEW/HUMAN_REVIEWED`。这些应在 Phase 6 状态去门槛化中处理。
