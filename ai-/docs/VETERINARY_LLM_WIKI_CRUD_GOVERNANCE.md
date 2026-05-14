# Veterinary LLM Wiki CRUD Governance

## 中文执行说明

本文件是猪病、鸡病等兽医医学 LLM Wiki 的增删改查治理规范。所有通过项目
CLI / 服务层执行的知识库写入，都必须完成以下闭环：

`变更触发 -> 规则校验 -> 理由归档 -> 数据生效 -> 图谱同步 -> 审计留痕`

核心约束：

- 新增：人工新增来源、URL、文本、批量材料必须提供 `reason` 与
  `evidence`；自动权威来源发现必须通过白名单、去重、抓取相关性等检查。
- 修改：cache 映射等状态变更必须提供 `reason` 与 `evidence`，写入后必须
  执行 schema、strict lint、graph rebuild、status snapshot。
- 删除：默认只 dry-run；真正删除必须提供 `reason` 与 `evidence`，路径必须在
  wiki 根目录内，删除前扫描引用，删除后重建图谱并写审计。
- 查询：查询本身不改变数据，不要求 reason/evidence，但返回上下文必须保留
  evidence source id 与 evidence status，便于训练集和评估集追溯。

对应代码：

- 统一准入和审计：`src/chicken_data_synthesis/infrastructure/knowledge/governance.py`
- 新增/修改入口：`operations.py`
- 删除与批量导入入口：`lifecycle.py`
- 权威来源发现入口：`authority.py`
- 图谱同步：`graph.py::rebuild_graph`
- schema/lint/status 闭环：`schema.py`、`operations.py::lint_wiki`、
  `operations.py::build_status_report`
- 猪病 gap-first 自动维护：`maintenance.py::build_gap_first_maintenance_queries`

审计落点：

- 人类可读日志：`log.md`
- 机器可读闭环审计：`issues/wiki_governance_audit_YYYY-MM-DD.jsonl`

This document defines the mandatory update loop for veterinary LLM Wiki
knowledge bases and their derived knowledge graphs. It applies to swine and
chicken disease domains because both are professional veterinary medicine
systems, and source, entity, fact, and graph changes must be auditable.

## Goal

Every knowledge-base mutation must follow this closed loop:

`change trigger -> rule validation -> reason archive -> data effect -> graph sync -> audit trail`

Manual arbitrary create, update, or delete behavior is not allowed through the
CLI/service entrypoints. Low-level file helpers may still exist for tests and
controlled batch scripts, but production maintenance should enter through the
governed orchestration layer.

## CRUD Rules

### Create

Trigger:

- Add a raw/source/candidate record from a local file, URL, pasted text, batch
  source folder, or authority-source discovery.
- Automated swine maintenance discovers a gap-first authority source.

Admission gates:

- The caller must provide `reason` and `evidence` for manual create operations.
- Authority discovery must pass domain allowlist, duplicate checks, and optional
  fetch relevance checks.
- New factual claims may enter only `exports/knowledge_facts.candidates.json`
  unless a separate review/promote flow explicitly approves them.

Code:

- Governance validation: `src/chicken_data_synthesis/infrastructure/knowledge/governance.py`
- Manual create wrappers: `operations.py::source_create`, `operations.py::ingest_source`,
  `operations.py::ingest_url_source`, `operations.py::ingest_text_source`
- Batch create wrapper: `lifecycle.py::batch_ingest_sources`
- Authority source discovery: `authority.py::discover_authority_sources`

### Update

Trigger:

- Cache mapping changes.
- Scheduled maintenance adds sources/candidates, then refreshes review and graph.
- Future entity/fact update wrappers should call the same governance gate before
  writing formal facts or index rows.

Admission gates:

- Manual update requires `reason` and `evidence`.
- Schema and strict lint must run after write.
- Graph artifacts must be rebuilt from the current wiki state.

Code:

- Cache update wrapper: `operations.py::update_cache`
- Scheduled swine gap-first maintenance: `maintenance.py::run_daily_maintenance`
- Graph sync: `graph.py::rebuild_graph`

### Delete

Trigger:

- Remove an invalid, duplicate, obsolete, or replaced source/raw pair.

Admission gates:

- Default is dry-run.
- Applied delete requires `reason` and `evidence`.
- Paths must resolve inside the wiki root.
- References are scanned before deletion and returned in the report.
- Cache invalidation, schema/lint, graph rebuild, and audit event are mandatory
  after applied deletion.

Code:

- Delete wrapper: `lifecycle.py::delete_source`
- Path containment and reference scan: `lifecycle.py::_resolve_inside`,
  `lifecycle.py::_scan_references`

### Read / Query

Trigger:

- Query wiki context, status, lint, schema, coverage, or graph status.

Admission gates:

- Read operations do not require `reason/evidence` because they do not mutate
  data.
- Query responses must expose evidence source IDs and evidence status so
  generated/evaluation data can trace claims back to the knowledge base.

Code:

- Query: `operations.py::query_wiki`
- Evidence-aware context: `wiki.py::build_llm_wiki_context`
- Audit metadata for generated datasets: `audit.py::build_wiki_audit_metadata`

## Closed-Loop Implementation

The centralized governance layer is:

- `governance.py::validate_change_request`
- `governance.py::classify_change_semantics`
- `governance.py::append_governance_event`

Manual and automated write entrypoints use this sequence:

1. `validate_change_request(...)`
2. `append_governance_event(..., phase="precheck", status="accepted")`
3. Perform the actual write.
4. Run schema check.
5. Run strict lint.
6. Rebuild graph.
7. Build status snapshot.
8. `append_governance_event(..., phase="post_write_closure", status=...)`

## Factual Lifecycle Semantics

CRUD is not enough for veterinary knowledge governance. Every write event is
also classified into a factual lifecycle category:

- `additive_evidence`: a new source or fact signal supplements existing
  knowledge and does not replace older evidence.
- `candidate_only`: a new source/fact enters only the candidate layer and must
  not be treated as formal reviewed knowledge.
- `supersedes_previous`: a new source or fact replaces a previous source/fact;
  the old item should be retained as deprecated/replaced unless an explicit
  later cleanup is justified.
- `deprecated_obsolete`: a source/fact is obsolete, expired, revoked, or no
  longer valid for current use.
- `orphan_cleanup`: a source/raw pair is not referenced by wiki pages, exports,
  formal facts, candidate facts, or index rows, and can be removed after dry-run
  proves `references=[]`.
- `accidental_or_invalid`: cleanup for duplicate, irrelevant, invalid, or
  accidentally added material.
- `cache_reconciliation`: technical correction of raw/source cache mapping
  without changing domain facts.

The graph builder reads `issues/wiki_governance_audit_*.jsonl` and turns these
events into `governance` nodes plus edges such as `governance-create`,
`governance-delete`, and `governance-replacement`. This makes fact/source
lifecycle visible in `wiki/graph-data.json` and `wiki/knowledge-graph.html`
instead of leaving it hidden in imperative code.

Code:

- Semantic inference: `governance.py::classify_change_semantics`
- Governance graph nodes/edges: `graph.py::_load_governance_events`,
  `graph.py::_add_governance_event_to_graph`
- Delete reference protection: `lifecycle.py::_scan_references`

## LLM-Assisted Judgment

LLMs may assist factual lifecycle judgment, but they must not be the authority
that directly mutates the wiki. The correct role split is:

- LLM may propose: whether a new source appears to supersede, supplement,
  deprecate, or duplicate an old source, and which old source IDs may be
  affected.
- Code must enforce: allowlist, path containment, duplicate checks, reference
  scans, reason/evidence presence, schema/lint, graph rebuild, and audit.
- Human/domain review is required for high-risk veterinary claims and for
  promoting candidate facts into formal facts.
- If LLM judgment is used, store it as advisory evidence in the governance
  event details, with `semantic_confidence` separate from formal review status.

Audit files:

- Human log: `log.md`
- Machine audit trail: `issues/wiki_governance_audit_YYYY-MM-DD.jsonl`

Closure status:

- `closed`: schema and strict lint both passed.
- `closed_with_findings`: data was written and graph was synced, but schema or
  lint still reports findings requiring follow-up.
- `no_effect`: a governed operation ran but created no accepted source.

## Swine Maintenance Policy

The swine scheduled maintenance runner is configured to update:

`knowledge/llm_wiki_swine_authoritative`

It uses:

`knowledge/llm_wiki_swine_authoritative/issues/swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md`

The maintenance query generator starts from:

- `exports/balanced_task_use_index.csv`
- `exports/disease_index.csv`
- `exports/drug_gold_role_index.csv`
- `issues/dataset_readiness_audit.json`

This means maintenance first targets missing content and low-usable pages such
as `generation_ready_limited`, `NEEDS_REVIEW`, and `partial` pages before doing
generic refreshes.

The source-use policy is balanced:

- Qualified sources across the five accepted levels may support bounded disease
  or clinical generation.
- A0/A1 and official-label anchoring are required only for executable
  high-risk claims such as dose, withdrawal period, MRL, banned/prohibited drug,
  culling, animal movement, food safety, or regulatory enforcement.

Code:

- Gap-first query generation: `maintenance.py::build_gap_first_maintenance_queries`
- Scheduled runner: `scripts/run_llm_wiki_weekly_maintenance.ps1`
- Task registration: `scripts/register_llm_wiki_weekly_task.ps1`

## CLI Behavior

The following commands now require auditable fields:

- `source-create --reason --evidence`
- `ingest --reason --evidence`
- `ingest-url --reason [--evidence]`
- `ingest-text --reason --evidence`
- `batch-ingest --reason --evidence`
- `cache update --reason --evidence`
- `delete-source --apply --reason --evidence`

Example:

```powershell
python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative `
  ingest-url "https://www.woah.org/..." `
  --reason "fill swine disease diagnostic source gap from 2026-05-08 review" `
  --evidence "issues/swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md"
```

## Current Known Boundary

The governance layer controls project service and CLI entrypoints. It cannot
prevent direct filesystem edits performed outside the application. Those should
be caught by review, git diff, lint/schema checks, and the absence of matching
`wiki_governance_audit_*.jsonl` events.

## Terminal Runbook

For step-by-step PowerShell commands, expected outputs, and create/update/delete
reasonableness checks, see:

`docs/VETERINARY_LLM_WIKI_TERMINAL_CRUD_RUNBOOK.md`
