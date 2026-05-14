# 兽医 LLM Wiki 终端 CRUD 闭环执行手册

本文档给出可在 PowerShell 终端逐步执行的完整代码，用临时演示库模拟猪病 LLM Wiki 的新增、修改、删除、查询与图谱同步。示例不会污染正式库：

`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative`

所有示例写入临时目录：

`D:\XF-ChongQin\ai-\results\wiki_graph_crud_manual_demo\demo_swine_wiki`

## 0. 基础设置

```powershell
Set-Location "D:\XF-ChongQin\ai-"
$env:PYTHONPATH = "src;."
$DemoRoot = "results/wiki_graph_crud_manual_demo"
$DemoWiki = "$DemoRoot/demo_swine_wiki"
```

预期结果：后续所有命令都在项目根目录执行，Python 能导入 `src` 下的项目包。

对应代码：

- CLI 入口：`src/chicken_data_synthesis/wiki_cli.py`
- CLI 参数编排：`src/chicken_data_synthesis/interfaces/cli/wiki.py`

## 1. 构建演示库并生成更新前图谱

```powershell
python scripts/simulate_governed_swine_graph_update_2026_05_08.py `
  --clean `
  --output-dir $DemoRoot
```

这个脚本会做三件事：

- 创建一个最小猪病演示 wiki，包含 `DIS-026 口蹄疫`、`SRC-0001` 和 1 条 `HUMAN_REVIEWED` 基础事实。
- 生成更新前图谱并保存到 `knowledge-graph-before.html`、`graph-before.json`。
- 模拟一次自动权威来源发现，把 WOAH 口蹄疫页面作为候选来源写入候选层，再生成更新后图谱与 diff。

预期输出摘要：

```json
{
  "before_html": "...\knowledge-graph-before.html",
  "after_html": "...\knowledge-graph-after.html",
  "diff_json": "...\graph-update-diff.json",
  "added_nodes": 3,
  "added_links": 2,
  "added_candidate_facts": 1
}
```

对应代码：

- 演示脚本：`scripts/simulate_governed_swine_graph_update_2026_05_08.py`
- 图谱生成：`src/chicken_data_synthesis/infrastructure/knowledge/graph.py::rebuild_graph`
- 新增来源准入：`src/chicken_data_synthesis/infrastructure/knowledge/authority.py::discover_authority_sources`
- 治理审计：`src/chicken_data_synthesis/infrastructure/knowledge/governance.py`

## 2. 查看更新前后图谱和差异

```powershell
Get-ChildItem $DemoRoot -Filter "knowledge-graph-*.html" |
  Select-Object FullName,Length,LastWriteTime

Get-Content "$DemoRoot/graph-update-diff.json" |
  Select-String -Pattern "added_node_count|removed_node_count|added_link_count|removed_link_count|candidate_fact_delta"

Get-Content "$DemoRoot/graph-update-report.md"
```

预期结果：

- `knowledge-graph-before.html` 是新增来源前图谱。
- `knowledge-graph-after.html` 是新增候选来源后的图谱。
- `added_node_count = 3`
- `added_link_count = 2`
- `candidate_fact_delta = 1`
- `removed_node_count = 0`
- `removed_link_count = 0`

新增节点应包含：

- `SRC-0002`：WOAH 口蹄疫候选来源节点。
- 一个 candidate subject 节点：候选来源标题。
- 一个 candidate object 节点：`pending_review`。

新增边应包含：

- candidate subject -> `pending_review`，`type=candidate-fact`。
- candidate subject -> `SRC-0002`，`type=candidate-evidence`。

合理性判断：

- 这是补证据，不是改写正式事实。
- 新增事实只进入 `exports/knowledge_facts.candidates.json`。
- `exports/knowledge_facts.json` 中原有 `HUMAN_REVIEWED` 事实不被覆盖。
- 图谱显示 candidate 节点，避免把待复核内容伪装成正式结论。

## 3. 新增：自动发现权威来源如何闭环

演示脚本内部等价执行了如下新增逻辑：

```powershell
$Suggestions = @{
  sources = @(
    @{
      url = "https://www.woah.org/en/disease/foot-and-mouth-disease/"
      title = "口蹄疫 WOAH disease page"
      reason = "WOAH disease page can support a candidate source for swine foot-and-mouth disease diagnosis and control context."
      evidence_role = "clinical_reference"
    }
  )
} | ConvertTo-Json -Depth 5
```

实际新增由 Python 函数执行，不建议手工拼写 JSON 文件后绕过流程。核心闭环是：

1. `discover_authority_sources(...)` 收到候选 URL。
2. `is_authoritative_url(...)` 检查域名白名单，WOAH 域名通过。
3. `_existing_external_urls(...)` 检查去重，避免重复来源。
4. `create_source_page(...)` 创建 `wiki/sources/SRC-0002-...md`。
5. `write_candidate_facts(...)` 只写候选事实，不写正式事实。
6. `_post_authority_closure(...)` 执行 schema、strict lint、graph rebuild、status。
7. `append_governance_event(...)` 写入 JSONL 审计。

事实层面的生命周期语义：

- 本示例不是“覆盖旧来源”，而是 `candidate_only`。
- 原因是新来源只写入候选层，`evidence_status=NEEDS_REVIEW`。
- 旧的 `SRC-0001` 和 `DIS-026-DEMO-001` 仍然保留。
- 图谱会额外出现 `governance` 节点，标签类似
  `create:candidate_only:closed`，并通过 `governance-create` 边指向
  `SRC-0002`。

验证命令：

```powershell
Get-Content "$DemoWiki/exports/knowledge_facts.candidates.json"

Get-ChildItem "$DemoWiki/wiki/sources" -Filter "SRC-0002-*.md" |
  Select-Object FullName,Length,LastWriteTime

Get-ChildItem "$DemoWiki/issues" -Filter "wiki_governance_audit_*.jsonl" |
  ForEach-Object { Get-Content $_.FullName } |
  Select-String -Pattern "candidate_only|post_write_closure|schema_ok|lint_ok|accepted_count"

Get-Content "$DemoWiki/wiki/graph-data.json" |
  Select-String -Pattern "governance_events|governance-create|semantic_action|candidate_only"
```

预期结果：

- `knowledge_facts.candidates.json` 增加 `CAND-0001`。
- `CAND-0001.evidence_status = NEEDS_REVIEW`。
- source page `SRC-0002` 存在。
- 审计中 `accepted_count = 1`。
- 审计中 `schema_ok = true`、`lint_ok = true`、`status = closed`。
- 图谱 metadata 中 `governance_events` 大于 0。
- 图谱 links 中出现 `governance-create`，表示本次新增的事实生命周期已进入图谱。

为什么新增合理：

- 触发理由是 gap-first 补齐 DIS-026 权威来源缺口。
- WOAH 是允许域名。
- 新增内容只进入候选层，需要后续 review 才能成为正式事实。
- 图谱增量只增加 candidate/source 节点和 candidate 边。

## 4. 修改：cache 映射更新如何闭环

修改示例：修复或补齐 raw 文件与 source page 的 cache 映射。

触发条件：

- raw 文件已经存在。
- source page 已经存在。
- `.wiki-cache.json` 缺少映射，或映射需要与审计后的 source page 对齐。

执行代码：

```powershell
python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir $DemoWiki `
  --json `
  cache update `
  raw/notes/baseline-swine-reference.txt `
  wiki/sources/SRC-0001-baseline-swine-reference.md `
  --reason "repair cache mapping after audited source reconciliation" `
  --evidence "source page SRC-0001 points to raw/notes/baseline-swine-reference.txt"
```

预期输出：

```json
{
  "key": "sha256:...",
  "entry": {
    "source_path": "raw/notes/baseline-swine-reference.txt",
    "source_page": "wiki/sources/SRC-0001-baseline-swine-reference.md",
    "title": "baseline-swine-reference",
    "created_at": "...",
    "updated_at": "..."
  }
}
```

验证命令：

```powershell
python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir $DemoWiki `
  --json `
  cache check raw/notes/baseline-swine-reference.txt

Get-ChildItem "$DemoWiki/issues" -Filter "wiki_governance_audit_*.jsonl" |
  ForEach-Object { Get-Content $_.FullName } |
  Select-String -Pattern "cache:|repair cache mapping|post_write_closure|schema_ok|lint_ok"
```

预期验证：

- `cache check` 返回 `hit: true`。
- `entry.source_path` 与输入 raw 路径一致。
- `entry.source_page` 与输入 source page 一致。
- 审计包含 `operation=update`。
- 审计包含 `phase=precheck` 和 `phase=post_write_closure`。
- post closure 中 `schema_ok=true`、`lint_ok=true`。

为什么修改合理：

- 修改对象不是事实内容，而是 raw/source 的索引映射。
- reason 说明为什么要修复映射。
- evidence 指向 source page 与 raw path 的对应关系。
- 写入后重建图谱，确保可视化与 cache 状态一致。
- 事实生命周期语义为 `cache_reconciliation`，表示这是技术对账，不表示某条兽医事实被覆盖。
- 如果未来发生“同类型新数据覆盖旧数据源”，不能用本命令表达，应使用
  `supersedes_previous` 的治理语义：新来源先作为候选来源加入，旧来源保留，
  审计和图谱记录替代关系，待 review 后再决定是否废止旧来源。

对应代码：

- `operations.py::update_cache`
- `cache.py::cache_update`
- `operations.py::_post_write_closure`
- `governance.py::validate_change_request`
- `governance.py::append_governance_event`

## 5. 删除前置验证：引用中的来源必须阻断删除

删除风险最大，因此必须先 dry-run。示例删除刚刚自动新增的 `SRC-0002`。

执行 dry-run：

```powershell
$Src0002 = (Get-ChildItem "$DemoWiki/wiki/sources" -Filter "SRC-0002-*.md" |
  Select-Object -First 1).FullName

python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir $DemoWiki `
  --json `
  delete-source `
  --source-page $Src0002
```

预期输出：

```json
{
  "dry_run": true,
  "deleted_paths": [],
  "references": [
    "exports/knowledge_facts.candidates.json"
  ],
  "warnings": []
}
```

含义：

- `deleted_paths` 为空，说明 dry-run 不删除任何文件。
- `references` 非空，说明该 source 仍被候选事实引用。
- 这种情况下不允许 apply 删除。

尝试真正删除：

```powershell
python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir $DemoWiki `
  --json `
  delete-source `
  --source-page $Src0002 `
  --reason "remove referenced candidate source should be blocked" `
  --evidence "delete safety demonstration" `
  --apply
```

预期结果：命令失败，并出现类似错误：

```text
ValueError: Refusing to delete a source that is still referenced.
references=('exports/knowledge_facts.candidates.json',).
Update or remove references first
```

为什么这是合理删除逻辑：

- 删除被触发的理由不足以覆盖事实引用风险。
- `_scan_references(...)` 会扫描 `wiki/` 与 `exports/` 下的 `.md/.json/.jsonl/.csv/.txt` 文件。
- 被 `knowledge_facts.candidates.json` 引用的来源不能删除，否则会产生悬空 evidence source。
- CLI 不暴露 `allow_referenced_delete`，因此人工终端路径无法强制删除仍被引用的来源。
- 事实生命周期语义即使能被推断，也不能绕过引用保护。语义只说明“为什么想删”，
  引用扫描决定“是否允许删”。

对应代码：

- `lifecycle.py::delete_source`
- `lifecycle.py::_resolve_inside`
- `lifecycle.py::_scan_references`

## 6. 删除成功示例：只删除无引用的遗留孤儿来源

为了演示成功删除，先构造一个只存在于临时演示库里的“遗留孤儿来源”。这个来源不被任何事实、候选事实、索引或 wiki 页面引用。

创建演示用孤儿来源：

```powershell
$RawOrphan = Join-Path $DemoWiki "raw/notes/legacy-orphan-source.txt"
$SrcOrphan = Join-Path $DemoWiki "wiki/sources/SRC-0099-legacy-orphan-source.md"

Set-Content `
  -Path $RawOrphan `
  -Encoding UTF8 `
  -Value "Legacy orphan source created only for delete governance simulation."

@'
---
type: source
source_id: SRC-0099
source_path: raw/notes/legacy-orphan-source.txt
source_type: plain_text
authority_level: unclassified
evidence_status: NEEDS_REVIEW
---

# Legacy orphan source

This source is not referenced by exports or wiki pages except its own frontmatter.
'@ | Set-Content -Path $SrcOrphan -Encoding UTF8
```

先 dry-run：

```powershell
python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir $DemoWiki `
  --json `
  delete-source `
  --raw-file raw/notes/legacy-orphan-source.txt `
  --source-page wiki/sources/SRC-0099-legacy-orphan-source.md
```

预期输出：

```json
{
  "dry_run": true,
  "deleted_paths": [],
  "references": [],
  "warnings": []
}
```

只有当 `references` 为空，才允许真正删除：

```powershell
python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir $DemoWiki `
  --json `
  delete-source `
  --raw-file raw/notes/legacy-orphan-source.txt `
  --source-page wiki/sources/SRC-0099-legacy-orphan-source.md `
  --reason "delete legacy orphan source not referenced by any wiki/export fact" `
  --evidence "dry-run references empty; created for deletion governance simulation" `
  --apply
```

预期输出：

```json
{
  "dry_run": false,
  "deleted_paths": [
    "wiki/sources/SRC-0099-legacy-orphan-source.md",
    "raw/notes/legacy-orphan-source.txt"
  ],
  "references": [],
  "warnings": []
}
```

验证确实删除、没有多删：

```powershell
Test-Path "$DemoWiki/wiki/sources/SRC-0099-legacy-orphan-source.md"
Test-Path "$DemoWiki/raw/notes/legacy-orphan-source.txt"

Get-ChildItem "$DemoWiki/wiki/sources" |
  Select-Object Name
```

预期结果：

```text
False
False
```

并且 `SRC-0001`、`SRC-0002` 仍在，说明只删除了指定 orphan source/raw，没有多删。

验证闭环审计：

```powershell
Get-ChildItem "$DemoWiki/issues" -Filter "wiki_governance_audit_*.jsonl" |
  ForEach-Object { Get-Content $_.FullName } |
  Select-String -Pattern "delete legacy orphan|deleted_paths|post_write_closure|schema_ok|lint_ok"
```

预期审计包含：

- `operation = delete`
- `phase = precheck`
- `phase = post_write_closure`
- `deleted_paths` 只包含 orphan source page 与 orphan raw file
- `schema_ok = true`
- `lint_ok = true`
- `status = closed`

为什么不会多删：

- `_resolve_inside(...)` 要求传入路径必须在 wiki 根目录内。
- `delete_source(...)` 只对 `page_path` 与 `raw_path` 两个解析后的路径执行 `unlink()`。
- `deleted_paths` 明确返回实际删除列表，终端可验证。

为什么不会漏删：

- 同时传入 `--raw-file` 与 `--source-page`，函数会删除这两个配对文件。
- 如果只传 raw，函数会通过 cache 或 source page 扫描寻找对应 source page。
- 删除后执行 `cache_invalidate(...)`，避免 cache 指向已删除文件。
- 删除后执行 `rebuild_graph(...)`，图谱从当前文件系统重建，不保留已删除节点。

为什么不会造成悬空引用：

- 真删前 `_scan_references(...)` 扫描 `wiki/` 和 `exports/`。
- 若任何正式事实、候选事实、索引、页面仍引用该 source id、source page 或 raw path，`--apply` 会失败。
- 本成功示例中 `references=[]`，所以删除合理。

事实层面的删除分类：

- 本示例 reason 包含 `orphan` 和 `not referenced`，治理层归类为 `orphan_cleanup`。
- 如果 reason 是 `obsolete/deprecated/expired`，归类为 `deprecated_obsolete`，仍需 dry-run
  证明没有事实依赖，或先完成替代来源和事实迁移。
- 如果 reason 是 `replaced/superseded`，归类为 `supersedes_previous`，旧来源不应立即删除；
  更合理的流程是先保留旧来源、记录 replacement，再由 review 决定是否进入废弃或孤儿清理。
- 如果 reason 是 `duplicate/invalid/irrelevant/accidental`，归类为 `accidental_or_invalid`，
  仍需证明没有事实或候选事实引用。

查看语义审计和图谱边：

```powershell
Get-ChildItem "$DemoWiki/issues" -Filter "wiki_governance_audit_*.jsonl" |
  ForEach-Object { Get-Content $_.FullName } |
  Select-String -Pattern "semantic_action|orphan_cleanup|delete legacy orphan"

Get-Content "$DemoWiki/wiki/graph-data.json" |
  Select-String -Pattern "governance-delete|orphan_cleanup|GOV-"
```

预期结果：

- 审计中删除事件包含 `semantic_action=orphan_cleanup`。
- 图谱中出现 governance delete 事件节点，表达“为什么删除”，而不只是文件消失。

## 6.1 同类型新数据进入时，旧数据源如何处理

同类型新数据进入时，不能默认覆盖旧数据源。推荐流程如下：

1. 新来源先以 `candidate_only` 或 `additive_evidence` 进入候选层。
2. 如果新来源声称替代旧来源，reason 必须写明 `superseded/replaced`，并在 evidence
   中写明旧来源 ID、替代依据、发布时间或标准版本。
3. 旧来源保留，不立即删除；图谱通过 governance 节点和 replacement 语义体现替代关系。
4. 只有当 review 证明旧来源不再被正式事实/候选事实/索引引用，且 dry-run 返回
   `references=[]`，才能执行 `deprecated_obsolete` 或 `orphan_cleanup` 删除。
5. 如果旧来源仍被引用，应先进行事实迁移或候选事实重审，而不是删除源文件。

LLM 可辅助判断：

- LLM 可以读取新旧来源标题、摘要、版本号、发布日期，建议其关系是“补充、替代、废止、重复、无关”。
- LLM 输出只能进入 `reason/evidence` 或治理事件 details，作为辅助线索。
- 真正是否生效仍由代码门槛、来源白名单、引用扫描、schema/lint、图谱同步和人工/domain review 决定。

## 7. 查询：读操作如何保留证据链

查询不改变数据，所以不要求 reason/evidence。

```powershell
python -m chicken_data_synthesis.wiki_cli `
  --wiki-dir $DemoWiki `
  --json `
  query "口蹄疫 WOAH 来源"
```

预期结果：

- 返回 `hits`，包含相关 wiki/source 页面。
- 返回 `fact_hits`，事实命中里带有 `evidence_source_id` 与 `evidence_status`。
- 查询不会写入 `wiki_governance_audit_*.jsonl`，因为它不是变更。

对应代码：

- `operations.py::query_wiki`
- `wiki.py::build_llm_wiki_context`
- `audit.py::build_wiki_audit_metadata`

## 8. 总结：增改删的闭环判定标准

新增成功必须同时满足：

- 有触发理由。
- 有 evidence。
- 来源通过白名单/去重/相关性或人工准入。
- 新事实先进入候选层。
- 图谱出现 candidate/source 增量。
- 审计中 `schema_ok=true`、`lint_ok=true`。

修改成功必须同时满足：

- 修改对象明确。
- reason/evidence 指向本次修改依据。
- 修改后可用查询命令验证状态确实变化。
- 图谱、schema、lint、status 已同步。
- 审计中记录 update 的 precheck 与 post closure。

删除成功必须同时满足：

- dry-run 显示 `references=[]`。
- apply 时 reason/evidence 具体。
- `deleted_paths` 只包含目标 raw/source。
- `Test-Path` 验证目标不存在。
- 其他 source 仍存在。
- 审计闭环 `status=closed`。

删除必须失败的情况：

- `references` 非空。
- 路径不在 wiki 根目录内。
- 缺少 reason/evidence。
- source page 或 raw file 缺失且无法明确解析目标。
