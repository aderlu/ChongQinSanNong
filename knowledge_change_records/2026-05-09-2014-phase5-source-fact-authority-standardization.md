# Phase 5 Source And Fact Authority Standardization

Date: 2026-05-09

## 修改目标和范围

执行猪病 LLM Wiki 清洗整理 Phase 5：标准化 source 和 fact 的来源状态、有效性、权威等级、风险类别和任务用途，生成可供后续 exporter、runtime loader 和审计工具使用的新状态索引。

新增或修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/standardize_source_fact_status.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/source_authority_status_index.csv`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts_status_index.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/source_fact_authority_status_audit_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/source_fact_authority_status_audit_2026-05-09.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/sources/*.md`

## 修改前存在的问题

修改前 `source_index.csv` 和 `knowledge_facts.json` 主要依赖：

- `evidence_status`
- `evidence_source_id`
- source id 前缀隐含权威等级

缺少显式的新状态字段：

- `source_status`
- `fact_validity`
- `authority_level`
- `risk_class`
- `task_use_status`

source 页也没有统一的 `source_status` frontmatter 和标准 “可支持结论 / 不得外推边界” 章节。

## 修改前代码状态

没有独立工具将 source/fact 映射到新状态契约。后续 exporter 或 loader 若直接读取旧 facts，仍可能误用 `HUMAN_REVIEWED` / `NEEDS_REVIEW`。

## 本次更新或新增了什么代码

新增 `standardize_source_fact_status.py`：

- 读取 `exports/source_index.csv`。
- 为 source 推断 `authority_level`。
- 为 source 页补充 `source_status: source_anchored`。
- 为 source 页补充标准章节：
  - `## 可支持结论`
  - `## 不得外推边界`
- 生成 `exports/source_authority_status_index.csv`。
- 读取 `exports/knowledge_facts.json`。
- 为每条 fact 增加：
  - `source_status`
  - `fact_validity`
  - `authority_level`
  - `risk_class`
  - `task_use_status`
  - `legacy_evidence_status`
- 生成 `exports/knowledge_facts_status_index.json`。

## 本次进行了什么整理工作

执行：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\standardize_source_fact_status.py
```

结果：

- source_rows: 219。
- source_pages_changed: 219。
- source_missing: 0。
- facts: 2193。
- invalid_facts: 0。
- task_use_counts:
  - train_ready: 2015。
  - generation_ready_limited: 154。
  - eval_ready: 24。

## 修改后解决了什么

- source/fact 可用性不再依赖 legacy review 字段。
- 所有 source 页都有显式 `source_status`。
- 所有 facts 都有新状态字段。
- 高风险事实可通过 `risk_class` 和 `authority_level` 识别。
- 普通来源清晰、数据有效的事实可直接进入对应任务流。

## 预计更新效果

- 为 Phase 6 exporter/loader 迁移提供可直接读取的新索引。
- 提高黄金数据集生产前的筛选精度。
- 降低来源等级不匹配造成的监管、用药、休药期、MRL 和食品安全越界风险。
- 让后续审计可以按 `source_status/fact_validity/task_use_status` 统计，而不是按复核状态统计。

## 验证

已运行：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\standardize_source_fact_status.py
python knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- source_missing: 0。
- invalid_facts: 0。
- manifest missing_paths: 0。
- hallucination risk high: 0。
- hallucination risk medium: 0。
- runtime_damaged_count: 0。
- readiness_score: 99。

## 残余风险和下一步

本阶段生成了新状态索引，但还没有把 exporter、runtime loader、评估器全部切换到这些新索引。该工作应在 Phase 6 中完成。
