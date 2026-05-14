# 猪病 LLM Wiki 治理规则强制落地与维护留痕机制更新记录

## 1. 修改时间

- 日期：2026-05-11
- 时间：01:17
- 时区：Asia/Shanghai
- 修改类型：知识库维护规则强制落地、文档优化、工作留痕机制完善、乱码防护强化

## 2. 本次修改目标

本次修改的目标，是把以下两份文档从“维护参考文档”升级为后续猪病 LLM Wiki 更新必须遵守的强制规则：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

同时要求后续每一次 Wiki 知识库修改，都必须在根目录 `knowledge_change_records/` 下新增修改说明文档，作为工作留痕和汇报依据。

本次规则重点覆盖：

- 从网页获取的信息源和事实。
- 从本地 Markdown、PDF、Word、Excel、扫描件、教材、标准、标签资料中获得的信息源和事实。
- source、fact、runtime 页面、evidence expansion、rule card、synthesis、exports、graph、gold dataset 的增删改查。
- 旧数据处理逻辑，包括过时、冲突、覆盖、降级、归档、迁移、删除。
- 高风险医学与监管内容的来源门禁和规则卡门禁。
- 中文文档更新过程中的 UTF-8 编码和乱码防护。

## 3. 修改前存在的问题

修改前已经存在 `WIKI_MAINTENANCE_GUIDE.md`，其中说明了 source-first、runtime 简洁、高风险门禁、修改留痕和编码防护等规则；也已经新增了 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`，说明数据源与数据增删改查治理逻辑。

但仍存在以下问题：

1. `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 尚未被 README、index、schema、checklist、change record template 明确挂为强制规则。
2. 后续维护者如果只看 README 或 intake checklist，可能不知道必须先执行 CRUD 治理规范。
3. 网页信息、本地 Markdown 信息、本地文档抽取信息进入知识库前，缺少统一的强制执行入口。
4. 旧数据如何处理虽然已有说明，但尚未在维护指南、schema 和变更模板中形成固定留痕字段。
5. 修改记录模板缺少专门的 `Governance Compliance` 区块，无法强制说明：
   - 是否检查维护指南。
   - 是否检查 CRUD 治理规范。
   - 本次是新增、查询、修改、删除、迁移、归档、降级、排除还是重建。
   - 旧数据是否被覆盖、删除、降级、归档或迁移。
   - 高风险门禁、runtime manifest、gold dataset 是否受影响。
6. 中文知识库维护过程中，仍需要明确要求所有后续操作使用 UTF-8，避免 PowerShell、Python、CSV、JSON 或复制粘贴导致乱码。

## 4. 修改前代码和文档状态

修改前关键文档状态如下：

- `WIKI_MAINTENANCE_GUIDE.md`
  - 已有维护准入规则。
  - 已有编码与乱码防护章节。
  - 但尚未明确声明必须同时执行 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`。

- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
  - 已有数据源和数据增删改查规则。
  - 已有旧数据处理、冲突处理、高风险门禁、验收和留痕规则。
  - 但尚未被其他入口文档明确列为强制规则。

- `README.md`
  - 已说明 runtime boundary 和 high-risk boundary。
  - 但未把两份治理文档列为后续维护的 mandatory governance rules。

- `index.md`
  - 已有 Governance 小节。
  - 但未列出两份强制治理文档。

- `.wiki-schema.md`
  - 已有 Source Contract、Usability Contract、Gold Dataset Contract 和 Runtime Boundary。
  - 但未定义 Mandatory Governance Contract。

- `SOURCE_BATCH_INTAKE_CHECKLIST.md`
  - 已有 source、fact、runtime placement、guardrail、batch block、audit、work record 检查项。
  - 但缺少最前置的 mandatory governance gate。

- `CHANGE_RECORD_TEMPLATE.md`
  - 已有常规修改记录模板。
  - 但缺少治理合规声明区块。

## 5. 本次更新或新增了什么文档

本次更新了以下文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/README.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/index.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/.wiki-schema.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/SOURCE_BATCH_INTAKE_CHECKLIST.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/CHANGE_RECORD_TEMPLATE.md`

新增了以下留痕文档：

- `knowledge_change_records/2026-05-11-0000-wiki-governance-rules-enforcement.md`
- `knowledge_change_records/2026-05-11-0117-wiki-governance-docs-enforcement-summary.md`

本次没有修改疾病事实、药物事实、source facts、runtime manifest、gold dataset 样本或图谱数据。

## 6. 本次进行了什么整理和规则落地工作

### 6.1 将维护指南升级为强制准入规则

在 `WIKI_MAINTENANCE_GUIDE.md` 中明确：

- 任何来自网页搜索、本地 Markdown/PDF/Word/Excel、批量抽取、人工整理、脚本生成或评估反馈的信息，都必须先按维护指南和 CRUD 治理规范判断是否可进入知识库。
- 强制执行顺序为：
  1. 阅读并遵守 `WIKI_MAINTENANCE_GUIDE.md`。
  2. 阅读并遵守 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`。
  3. 使用 `SOURCE_BATCH_INTAKE_CHECKLIST.md` 做执行前检查。
  4. 修改后运行验收命令。
  5. 在 `knowledge_change_records/` 记录结果。

### 6.2 强化网页来源和本地 Markdown 来源规则

维护指南中新增或强化：

- 网页来源必须判断是否新建 source、是否只是补 evidence anchor、是否会与旧来源冲突。
- 非官方网页涉及剂量、疗程、休药期、MRL、残留或监管措施时，只能作为线索，不能直接进入正向结论。
- 本地 `.md` 文档不能因为已经在仓库内就默认可信。
- 本地 Markdown 必须追溯原始来源、生成时间、作者或脚本、是否为历史批处理产物。
- 历史 issue、脚本输出、模型整理稿、旧批处理 Markdown 默认是审计或候选材料，不是权威 source。

### 6.3 将 CRUD 治理规范升级为强制数据治理规则

在 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 中新增：

- 强制执行声明。
- 强制落地流程。
- 脚本与治理规则冲突时的处理原则。
- 新增前置检查。
- 网页来源强制规则。
- 本地 Markdown 来源强制规则。
- 修改前必须回答的问题。
- 删除审批判断。
- 验收失败处理。
- 变更记录必须包含的治理合规声明。

### 6.4 将强制规则挂入所有入口文档

在 `README.md` 中新增 `Mandatory Governance Rules`，明确后续所有 Wiki 更新必须遵守两份文档。

在 `index.md` 的 Governance 小节中列出：

- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

在 `.wiki-schema.md` 中新增 `Mandatory Governance Contract`，要求所有 source intake、web-derived information、本地文档抽取、fact changes、runtime page edits、evidence expansion migration、rule card changes、export/index/graph rebuilds 和 gold dataset generation 都遵守这两份文档。

### 6.5 强化 intake checklist 和修改记录模板

在 `SOURCE_BATCH_INTAKE_CHECKLIST.md` 中新增 `Mandatory Governance Gate`，后续新增 source、fact、batch extraction、runtime edit、evidence expansion、index rebuild 或 pilot/gold dataset sample 前，必须先勾选治理规则。

在 `CHANGE_RECORD_TEMPLATE.md` 中新增 `Governance Compliance` 区块，后续每份修改记录都必须说明：

- 是否检查维护指南。
- 是否检查 CRUD 治理规范。
- 是否检查 intake checklist。
- CRUD 类型。
- 输入来源类型。
- 旧数据处理方式。
- 高风险门禁影响。
- runtime manifest 影响。
- gold dataset 影响。

## 7. 修改后解决了什么问题

本次修改后，两个核心治理文档已经不再只是参考文档，而是成为后续猪病 LLM Wiki 更新的强制前置门禁。

解决的问题包括：

1. 后续从网页获取的信息源和事实，不能绕过来源等级、事实有效性、旧数据处理和高风险门禁。
2. 后续从本地 Markdown 或其他本地文档中抽取的信息，不能因为“文件已经在仓库里”就直接当作权威事实。
3. 后续对旧数据进行覆盖、删除、降级、归档、迁移或排除时，必须说明事实逻辑和原因。
4. 后续每次修改都必须有 `knowledge_change_records/` 留痕，便于工作汇报和审计。
5. 后续变更记录模板已经固定加入治理合规项，减少遗漏。
6. 中文文档维护中的 UTF-8、Python 写入、JSON/CSV 输出、PowerShell 编码设置等防乱码要求被再次明确。

## 8. 预计产生的更新效果

对知识库维护：

- 后续新增、修改、删除、迁移和归档操作会更稳定。
- 维护者可以按统一流程判断网页来源、本地文档来源、旧版本数据和冲突事实。
- 不同阶段的工作记录更容易汇总成 leader 汇报材料。

对生产检索：

- runtime 页面仍会保持简洁，避免网页全文、本地 Markdown 长摘录、PDF 长摘录或批处理块直接进入默认检索。
- raw、issues、evidence expansion、graph 和大型矩阵仍保持非默认 runtime。

对医学事实严谨性：

- 高风险内容必须继续满足 A0/A1 或标签级来源要求。
- 诊断、药物、监管、休药期、MRL、残留和食品安全相关事实不会因普通网页或旧 Markdown 直接变成正向答案。

对黄金数据集：

- 后续样本生成必须保留 source/rule provenance。
- 如果来源、规则或事实状态变更，样本必须重建或重新验收。

## 9. 防乱码措施

本次明确要求后续中文知识库维护采取以下防乱码措施：

1. PowerShell 执行前设置 UTF-8：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

2. PowerShell 读取文件时使用：

```powershell
Get-Content -Encoding UTF8
```

3. Python 脚本读写文件时显式指定：

```python
encoding="utf-8"
```

4. JSON 输出使用：

```python
ensure_ascii=False
```

5. CSV 输出使用 UTF-8，必要时使用 `utf-8-sig` 供 Excel 查看。

6. 修改后运行：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

7. 禁止用未知编码复制粘贴覆盖 runtime 页面、source 页面或治理文档。

本次修改后已检查核心文档和新增留痕文档，没有发现 replacement character 或常见 mojibake 字符串等明显乱码信号。

## 10. 验证

本次属于治理文档和留痕机制更新，没有改动 runtime 页面、source facts、manifest 输入、图谱或 gold dataset 样本，因此没有重建 runtime manifest。

已完成的验证：

- 检查 README、index、schema、intake checklist、change record template 是否引用强制治理文档。
- 检查 `WIKI_MAINTENANCE_GUIDE.md` 和 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 是否包含强制执行要求。
- 检查核心文档和新增留痕文档是否存在明显乱码信号。

关键验证结果：

```json
{
  "mandatory_documents": [
    "WIKI_MAINTENANCE_GUIDE.md",
    "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md"
  ],
  "mandatory_entry_points_updated": [
    "README.md",
    "index.md",
    ".wiki-schema.md",
    "SOURCE_BATCH_INTAKE_CHECKLIST.md",
    "CHANGE_RECORD_TEMPLATE.md"
  ],
  "runtime_pages_changed": 0,
  "source_facts_changed": 0,
  "gold_dataset_samples_changed": 0,
  "encoding_damage_signal_in_touched_governance_docs": 0
}
```

## 11. 后续维护要求

之后每一次对猪病 LLM Wiki 的修改，都必须在 `knowledge_change_records/` 下新增说明文档。

说明文档必须包括：

1. 修改时间。
2. 本次目标。
3. 修改前存在的问题。
4. 修改前代码、索引、页面或知识库状态。
5. 新增或更新了什么代码或文档。
6. 进行了什么整理、迁移、降级、归档、删除、覆盖或重建。
7. 修改后解决了什么问题。
8. 预计对生产检索、回答生成、评估、审计和黄金数据集的影响。
9. 验证命令和结果。
10. 是否存在残余风险。
11. 是否遵守 `WIKI_MAINTENANCE_GUIDE.md`。
12. 是否遵守 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`。
13. 是否采取 UTF-8 和编码完整性检查措施。

如果修改涉及医学事实、药物、诊断、监管、休药期、MRL、残留、食品安全或黄金数据集，必须额外说明 source/rule provenance 和高风险门禁结果。

## 12. 结论

本次更新把猪病 LLM Wiki 的维护指南和数据源 CRUD 治理规范正式落地为强制规则，并将该规则挂入 README、index、schema、intake checklist 和 change record template。后续所有网页来源、本地文档来源、事实更新、runtime 页面整理、证据迁移、索引重建和黄金数据集生成，都必须按这两份文档执行，并在 `knowledge_change_records/` 中形成工作留痕。

本次未改变任何医学事实和 runtime 数据，只强化了维护制度、执行入口、留痕模板和乱码防护要求。
