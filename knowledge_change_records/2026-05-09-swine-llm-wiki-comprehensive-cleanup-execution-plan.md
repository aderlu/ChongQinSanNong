# 猪病 LLM Wiki 知识库全面清洗整理执行文档

Date: 2026-05-09

Target knowledge base: `ai-/knowledge/llm_wiki_swine_authoritative`

Related method baseline:

- `llm-wiki-skill-main/README.md`
- `llm-wiki-skill-main/SKILL.md`
- GitHub project: https://github.com/sdyckjq-lab/llm-wiki-skill

## 1. 目标

本次清洗整理的目标不是简单删除或补写页面，而是把当前猪病知识库治理成一个清晰、可审计、可检索、可评估、可用于高质量黄金数据集生产的 LLM Wiki。

最终状态应满足：

1. 符合 `llm-wiki-skill` 的核心结构：`raw/` 保存不可变原始素材，`wiki/` 保存结构化知识页，`sources/` 保存素材摘要和来源锚点，`purpose.md`、`index.md`、`log.md`、`.wiki-schema.md` 保存方向、索引、日志和 schema。
2. 生产和评估默认只加载受控运行时集合，不直接索引 `raw/`、`issues/`、巨大矩阵、graph 导出、会话记录和候选抽取材料。
3. 疾病页、药物页、规则卡、综合页、鉴别页、综合征页都保留稳定 ID、来源锚点、任务用途、不可外推边界和高风险阻断规则。
4. 所有可进入黄金数据集的事实必须能追溯到 `source_id`、`fact_id`、页码、URL、表格、规则卡或等价锚点。
5. 对剂量、疗程、给药途径、休药期、MRL、残留、可食用性、检疫、扑杀、调运、法定报告、官方处置等高风险结论，必须由 A0 或标签级等价来源支持；否则只能作为边界、拒答或后续检索任务。
6. 输出的黄金数据集必须区分 `train_ready`、`eval_ready`、`generation_ready_limited`、`retrieval_only`、`blocked`；可用性不再由“是否复核”决定，而由来源是否清晰、数据是否有效、来源等级是否匹配任务用途决定。
7. 实体页不再按“原始内容、补强块、增强内容、Vxx 批次块”分割同类事实；同一类型条目必须归并到同一节中，去重后保留所有原始来源锚点，尤其适用于 `wiki/diseases/` 和 `wiki/drugs/`。
8. 每一次代码、索引、实体页、来源页、规则卡、导出文件或清洗策略修改，都必须在根目录 `knowledge_change_records/` 新增说明文档，形成可汇报、可追溯的工作留痕。

## 2. 当前基线

本次检查以本地知识库和现有审计脚本为准。

### 2.1 结构和规模

`ai-/knowledge/llm_wiki_swine_authoritative` 当前包含：

- `wiki/`: 疾病、药物、来源、规则、规则卡、综合征、鉴别、综合页、主题页、graph 导出。
- `exports/`: 索引、事实表、运行时 manifest、排除规则、知识 facts。
- `raw/`: PDF、Markdown 转换、网页抓取、附件和爬取元数据。
- `issues/`: 缺口审计、抽取记录、就绪度报告、JSON 问题清单。
- `scripts/` 和 `tools/`: 构建、审计、归一化、manifest 生成和维护脚本。

现有审计脚本输出：

- Readiness score: 99/100.
- Disease pages: 73.
- Drug pages: 81.
- Syndromes: 22.
- Comparisons: 17.
- Rules: 449.
- Rule cards: 18.
- Sources: 219.
- Synthesis pages: 27.
- Missing indexed paths: 0.
- Bad fact tables: 0.
- Missing required rule cards: 0.
- Missing required synthesis pieces: 0.

运行时 manifest 已存在：

- `exports/runtime_core_manifest.json`
- `exports/runtime_exclude_patterns.json`
- `exports/runtime_core_manifest_summary.md`

Manifest summary 显示默认运行时集合包括：

- disease: 73
- drug: 80
- comparison: 14
- rule_card: 15
- syndrome: 12
- synthesis: 4

### 2.2 页面大小和噪声密度

抽样统计显示：

- `wiki/diseases`: 73 个文件，约 900 KB，平均 12.3 KB，4 个页面超过 20 KB。
- `wiki/drugs`: 81 个文件，约 601 KB，平均 7.4 KB，2 个页面超过 20 KB。
- `wiki/synthesis`: 27 个文件，约 922 KB，平均 34.1 KB，8 个页面超过 20 KB。
- 最大合成矩阵包括：
  - `swine_farm_drug_use_1_200_treatment_matrix.md`: 约 312 KB。
  - `swine_farm_drug_use_200_363_treatment_matrix.md`: 约 171 KB。
  - `veterinary_treatment_of_pigs_treatment_matrix.md`: 约 161 KB。
  - `swine_diagnosis_prescription_handbook_prescription_matrix.md`: 约 111 KB。

这说明实体页已经相对压缩，但合成矩阵和证据扩展材料仍必须被运行时排除，否则会显著干扰检索。

### 2.3 证据状态

疾病页：

- `HUMAN_REVIEWED`: 41.
- `NEEDS_REVIEW`: 32.
- `partial_source_anchored_page`: 32.
- `source_anchored_clinical_page`: 41.

药物页：

- `HUMAN_REVIEWED`: 73.
- `NEEDS_REVIEW`: 8.
- `source_anchored_drug_evidence_page`: 71.
- `partial_drug_evidence_page`: 8.
- `regulatory_boundary_page`: 1.
- `blank`: 4.

结论：知识库已经具有较好的来源锚点，但 `HUMAN_REVIEWED`、`NEEDS_REVIEW` 这类复核导向字段不应再决定事实能否使用。它们只能作为历史审计字段或迁移线索；真正的可用性应由 `source_status`、`fact_validity`、`authority_level`、`risk_class` 和 `task_use_status` 共同决定。

## 3. 主要问题

### 3.1 根目标和说明存在领域漂移

`purpose.md` 当前仍写着 chicken disease：

```text
This Wiki stores auditable chicken disease, drug, rule, source, and derived synthesis knowledge...
```

这会污染运行时上下文、测试夹具和自动提示。猪病知识库必须把 species、用途、黄金数据集目标、评估边界写清楚。

### 3.2 `wiki/` 同时承载生产知识和构建产物

`wiki/` 下既有实体页，也有 `graph-data.json`、`knowledge-graph.html`、巨大 synthesis 矩阵和历史阶段目录。`llm-wiki-skill` 允许 graph 和 synthesis 存在，但生产检索不能把它们与疾病、药物、规则卡同权加载。

风险：

- 检索命中巨大矩阵而不是实体页。
- 候选抽取事实被模型误当成最终有效事实。
- 评估模型从历史增强块中抽到过时或不适用结论。

### 3.3 复核状态、证据状态和任务用途尚未完全解耦

页面里已有 `HUMAN_REVIEWED`、`NEEDS_REVIEW`、`partial_source_anchored_page` 等状态，但这些状态混合了“人工流程状态”和“事实可用性”。后续必须去掉“复核”作为可用性门槛，改用数据本身的可追溯性和有效性判断。

新的判断原则：

- 来源清晰明确：存在 `source_id`、`fact_id`、页码、URL、表格、规则卡或等价锚点。
- 数据有效：内容无乱码、无未解释冲突、未超出来源支持范围。
- 来源等级匹配用途：普通临床事实可由 SRC/A1/A2 支持；中国监管、兽药标签、休药期、MRL、食品安全等高风险结论必须由 A0 或标签级等价来源支持。
- 任务用途明确：事实被映射到合适的 task-use 状态，而不是被 `NEEDS_REVIEW` 这类字段阻断。

黄金数据集生产需要的是 task-use 状态：

- `train_ready`
- `eval_ready`
- `generation_ready_limited`
- `retrieval_only`
- `blocked`

缺少这个层会导致三个错误：

- 把证据充分但不适合训练的页面放入 SFT。
- 把临床可用但不支持监管或用药执行结论的页面过度阻断。
- 把来源清晰、数据有效的事实仅因为 `NEEDS_REVIEW` 历史字段而错误排除。

### 3.4 药物和监管高风险边界仍需硬门槛

药物页已经有规则卡锚点，但数据集生产阶段必须再次强制：

- 没有 A0 或标签级等价来源，不得生成正向剂量、疗程、途径、休药期、MRL、残留合格、可销售或可食用结论。
- A1/A2 或教材来源可以支持一般临床、诊断、鉴别、控制思路，但不能替代中国监管、兽药标签、食品安全和强制处置结论。
- `positive_label_candidate` 必须单独审核，不能由普通药物页自动升级。

### 3.5 中文编码和显示链路需要专门治理

UTF-8 replacement character 当前未在核心疾病和药物页中发现，但 PowerShell 默认读取会大量显示乱码。本地还存在约 25 个包含 mojibake-like 高风险字符模式的 Markdown 文件，集中在：

- 部分 `raw/md/*.md` 转换文本。
- `wiki/topics/Swine-integumentary-lesion-differential-and-sampling.md`.
- 若干药物页，如 `DRUG-064-flunixin-meglumine.md`、`DRUG-063-meloxicam.md`、`DRUG-026-spectinomycin.md` 等。

后续需要区分三类情况：

- 文件真实内容正确，只是终端显示编码错误。
- 文件中已固化 mojibake，需要从来源或备份修复。
- 原始 OCR 或 PDF 转换质量不足，只能隔离为来源转换损坏或 `source_status=damaged_source_conversion`，不得用“待复核”模糊表达。

### 3.6 黄金数据集导出门槛需要从知识库侧显式化

当前 exports 已经有大量事实表和 role index，但黄金数据集生产还需要明确：

- 哪些疾病或药物能出正向病例。
- 哪些只能出鉴别诊断、拒答、边界、负样本或评估陷阱。
- 每条 QA 或 case 的 answer 必须引用哪些 source/fact/rule。
- 哪些字段缺失时 exporter 必须降级或拒绝导出。

### 3.7 实体页存在批次块堆叠和同类条目分散问题

当前许多 disease/drug 页面仍带有历史构建痕迹，例如 `Formal Disease Completion / V5`、`V11`、`V13`、`V15`、local-md review reinforcement、web source reinforcement 等批次块。它们在构建期有价值，但进入长期运行时后会造成同类事实被拆散在多个章节里。

风险：

- 同一类事实在“原始内容、补强块、增强内容、批次块”之间重复出现，增加检索噪声。
- 旧批次和新批次可能同时被检索，导致模型看到重复、冲突或不同证据等级的表述。
- 维护者难以判断最终可用事实在哪里。
- 黄金数据集生产可能把历史候选块误当作最终实体页结论。

治理要求：

- 实体页最终只按知识类型组织，不按构建批次组织。
- 同类条例、事实、边界、规则、来源说明直接放在同一节中。
- 内容去重时不得丢弃原始来源，必须把多个来源锚点合并保留。
- 批次块标记只允许临时存在于迁移过程中；迁移完成后 runtime 页不应保留大段增强块。

### 3.8 测试夹具存在历史鸡病乱码文本

`ai-/tests/test_llm_wiki_knowledge.py` 中的夹具文本仍是鸡病语料，而且读取时显示为 mojibake。它可能是兼容测试，但不应成为猪病知识库质量判断的唯一依据。需要新增猪病专用 regression，而不是直接替换所有历史鸡病测试。

## 4. 清洗后的目标架构

### 4.1 四层知识结构

#### Layer A: Runtime Core

默认生产与评估加载层，只允许 manifest 中列出的短页进入。

包括：

- source-clear and validity-passed disease pages
- source-clear and boundary-safe drug pages
- rule cards
- key syndrome pages
- key comparison pages
- small generation/evaluation policy synthesis pages
- minimal source metadata

不包括：

- `raw/**`
- `issues/**`
- `wiki/sessions/**`
- graph HTML/JSON
- huge treatment or prescription matrices
- candidate extraction dumps
- phase construction directories

#### Layer B: Evidence Store

审计和证据扩展层。

包括：

- `exports/knowledge_facts.json`
- fact indexes
- source index
- evidence expansion files
- source pages
- page, table, URL, section anchors

该层可被专门的 evidence expansion workflow 读取，但不进入默认问答上下文。

#### Layer C: Raw Archive

不可变来源层。

包括：

- PDFs
- converted Markdown
- crawled HTML/text
- official attachments
- crawl metadata

仅用于追溯、重抽取、有效性检查和来源重建，不参与默认检索。

#### Layer D: Governance Records

维护和变更记录层。

包括：

- root-level `knowledge_change_records/`
- knowledge base `issues/`
- audit JSON
- execution logs

该层记录为什么改、改了什么、如何验收。

### 4.2 页面职责

疾病页：

- 支持疾病召回、临床摘要、鉴别路由、诊断边界、防控框架、评估约束。
- 不生成独立处方、剂量、休药期、MRL 或法定监管结论。

药物页：

- 支持药物召回、合法性/标签/风险边界、负样本和规则检查。
- 不作为独立处方来源。

规则卡：

- 保存硬阻断和评估规则。
- 必须短、稳定、可直接被 exporter 引用。

综合页：

- 保存生成策略、评估 rubrics、任务边界、鉴别总览。
- 不直接创造新的生物医学事实。

来源页：

- 保存来源元数据、权威等级、可支持结论、不可外推边界。

## 5. 分阶段执行计划

### Phase 0: 冻结基线和建立回滚点

目标：清洗前固化当前状态，避免后续无法判断改动来源。

动作：

1. 记录 `git status --short`。
2. 保存当前审计输出。
3. 保存 runtime manifest 和 exclude patterns 的摘要。
4. 生成文件数量、大小、状态、来源锚点、疑似编码损坏清单。

产出：

- `knowledge_change_records/YYYY-MM-DD-phase0-baseline.md`
- `issues/baseline_audit_YYYY-MM-DD.json`

验收：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

通过标准：

- readiness score >= 99.
- missing indexed paths = 0.
- bad fact tables = 0.

阻断条件：

- 发现索引缺失路径。
- 发现 facts 无法解析到 source。
- 当前工作树有未知改动且会与清洗脚本冲突。

### Phase 1: 修正根元数据和项目方向

目标：消除 chicken/swine 领域漂移，让运行时上下文准确描述猪病知识库。

动作：

1. 更新 `purpose.md`，明确本库是 swine disease, drug, rule, source, synthesis knowledge base。
2. 更新 `.wiki-schema.md`，补充 task-use statuses、authority levels、runtime tiers、gold dataset roles。
3. 更新 `index.md`，列出关键目录、runtime manifest、审计入口和高风险规则入口。
4. 更新 README 中过时的 Phase 1/2 描述，改为当前结构化运行时知识库说明。

产出：

- 更新后的 `purpose.md`
- 更新后的 `.wiki-schema.md`
- 更新后的 `index.md`
- 更新后的 `README.md`

验收：

```powershell
rg "chicken|Chicken|鸡病|产蛋鸡" .\ai-\knowledge\llm_wiki_swine_authoritative\purpose.md .\ai-\knowledge\llm_wiki_swine_authoritative\.wiki-schema.md .\ai-\knowledge\llm_wiki_swine_authoritative\index.md
```

通过标准：

- 根元数据不再把猪病库描述成鸡病库。
- schema 明确运行时分层和黄金数据集用途状态。

### Phase 2: 编码和文本完整性清洗

目标：确认哪些文件是显示问题，哪些文件是真实 mojibake 或 OCR/转换损坏。

动作：

1. 建立疑似编码损坏扫描脚本，扫描：
   - replacement character `�`
   - mojibake-like tokens
   - 异常高比例 CJK 罕见字
   - 混杂的 GBK 解码痕迹
2. 对核心 runtime manifest 内文件逐一标记：
   - `encoding_ok`
   - `display_only_issue`
   - `content_mojibake`
   - `source_conversion_damaged`
3. 对 `content_mojibake` 文件，从原始来源、备份、PDF 转换结果或人工修订恢复。
4. 对无法恢复的 raw/md 文件保留在 Raw Archive，并从默认 runtime 和 evidence expansion 中隔离。

优先文件：

- `wiki/topics/Swine-integumentary-lesion-differential-and-sampling.md`
- `wiki/drugs/DRUG-064-flunixin-meglumine.md`
- `wiki/drugs/DRUG-063-meloxicam.md`
- `wiki/drugs/DRUG-026-spectinomycin.md`
- `wiki/drugs/DRUG-024-neomycin.md`
- `raw/md/DISEASES OF SWINE1-200.md`
- `raw/md/DISEASES OF SWINE401-600.md`

产出：

- `issues/encoding_integrity_audit_YYYY-MM-DD.json`
- `knowledge_change_records/YYYY-MM-DD-phase2-encoding-cleanup.md`

验收：

- runtime manifest 内文件 `content_mojibake = 0`。
- 核心疾病、药物、规则卡、comparison、syndrome 页面可被 UTF-8 正常读取。
- PowerShell 维护命令明确设置 UTF-8：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

### Phase 3: 运行时 allowlist 和 denylist 强化

目标：确保生产与评估默认只加载 curated runtime core。

动作：

1. 检查 `exports/runtime_core_manifest.json` 每条记录字段：
   - `page_id`
   - `path`
   - `entity_type`
   - `runtime_tier`
   - `source_status`
   - `fact_validity`
   - `authority_level`
   - `risk_class`
   - `task_use_status`
   - `gold_dataset_role`
   - `allowed_use`
   - `blocked_use`
   - `source_ids`
   - `rule_card_ids`
   - `last_verified`
2. 补齐 `task_use_status` 和 `gold_dataset_role`。
3. 确认 `runtime_exclude_patterns.json` 覆盖：
   - `raw/**`
   - `issues/**`
   - `wiki/sessions/**`
   - graph exports
   - treatment/prescription matrices
   - backup files
   - phase construction directories
4. 更新项目中的 runtime loader，使其默认读取 allowlist 而不是遍历整个 `wiki/`。

产出：

- 更新后的 `runtime_core_manifest.json`
- 更新后的 `runtime_exclude_patterns.json`
- loader 或测试更新

验收：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

通过标准：

- manifest missing paths = 0.
- high-risk runtime page count = 0.
- readiness score >= 99.
- 默认 loader 不加载巨大矩阵、raw、issues、graph。

### Phase 4: 实体页规范化、同类条目归并和证据扩展迁移

目标：让疾病页和药物页保持短、稳定、可检索；取消“补强块/增强块/原始块”的长期分层，把同类事实归并到统一章节中；把长证据块迁移到 evidence expansion，同时保留所有来源锚点。

动作：

1. 为疾病页定义固定结构：
   - frontmatter
   - identity and aliases
   - runtime tier and task use
   - source-backed clinical summary
   - pathogen/classification
   - host/stage
   - transmission or epidemiology
   - clinical signs and lesions
   - diagnosis and sampling boundary
   - differential links
   - prevention/control boundary
   - drug/regulatory guardrails
   - evidence gaps
   - source anchors
2. 为药物页定义固定结构：
   - frontmatter
   - active ingredient/class
   - runtime tier and task use
   - gold dataset role
   - China label/regulatory status if A0 supported
   - species/form/route boundary if source-backed
   - prohibited/withdrawal/MRL/residue boundary
   - non-generable claims
   - source anchors
   - evidence gaps
3. 对超过 20 KB 的 runtime 页面进行结构检查和来源有效性检查。
4. 对疾病页和药物页执行同类条目归并：
   - 不再按 `V5`、`V11`、`V13`、`V15`、`补强块`、`增强内容`、`原始内容` 等构建来源分节保存长期 runtime 内容。
   - 将同一类型的事实、边界、诊断要点、鉴别点、用药边界、监管边界、防控要点、Evidence gaps 放入各自统一章节。
   - 对语义重复条目去重；如果多个来源支持同一事实，合并为一个条目并保留全部 `source_id`、`fact_id`、页码、URL、表格、规则卡或等价锚点。
   - 对冲突事实不得简单合并，必须保留差异、来源等级、适用范围和冲突原因。
   - 对无来源条目不得保留为结论，只能转为 `Evidence gap`、`source_missing` 或迁移到 evidence expansion 待补源区。
5. 将长批次增强块移入 `wiki/evidence_expansions/`。
6. Runtime 页只保留短占位符，指向 evidence expansion 文件、来源数量和使用边界。
7. 删除或改写迁移完成后的批次块标题，避免默认检索看到“增强块”和“原始内容”并列的历史构建痕迹。

优先疾病页：

- `DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`
- `DIS-002-african-swine-fever-virus.md`
- `DIS-018-pseudorabies-aujeszky-disease.md`
- `DIS-021-influenza-viruses.md`

优先药物页：

- `DRUG-081-traditional-chinese-veterinary-medicines.md`
- `DRUG-018-enrofloxacin.md`

产出：

- compact runtime pages
- evidence expansion files
- migration map
- per-entity deduplication notes
- preserved-source anchor map

验收：

- runtime disease/drug 页面原则上小于 20 KB，超过者必须有 justification。
- 页面内每条事实有 source/fact/rule anchor。
- disease/drug 页面不再长期保留同类事实的 `Vxx`、`补强块`、`增强内容`、`原始内容` 并列分区。
- 去重后的合并条目仍保留全部原始来源锚点。
- 冲突事实被标记为冲突、来源等级不匹配或适用范围不一致，而不是静默合并。
- 迁移后 manifest 仍可解析所有路径。

### Phase 5: 来源、事实和权威等级标准化

目标：让所有事实进入统一来源等级和可支持结论体系。

动作：

1. 统一 source authority levels：
   - `A0`: 中国官方、法规、标准、标签、公告、限量、目录。
   - `A1`: 国际官方或准官方动物卫生、公共卫生、药品监管来源。
   - `A2`: 高质量二级临床或学术支持来源。
   - `SRC`: 本地教材、内部已登记来源。
   - `RC/RULE`: 规则卡和硬门槛。
2. 检查 `wiki/sources/*.md` 是否包含：
   - `source_id`
   - `authority_level`
   - `source_type`
   - `title`
   - `source_path` or `external_url`
   - `publisher`
   - `date`
   - `jurisdiction`
   - `supports`
   - `does_not_support`
   - `source_status`
   - `evidence_status` as legacy optional field
3. 对缺字段 source 页补齐元数据。
4. 对 facts 增加或校验：
   - `fact_id`
   - `subject`
   - `predicate`
   - `object`
   - `evidence_source_id`
   - `evidence_anchor`
   - `source_status`
   - `fact_validity`
   - `evidence_status` as legacy optional field
   - `task_use_status`
   - `risk_class`

产出：

- source page metadata cleanup
- source index refresh
- facts schema enhancement report
- legacy review-status migration report

验收：

- source index rows 与 source pages 一致。
- 事实表 source_id completeness = 100%。
- 需要页码的 fact table page completeness >= 95%。
- facts 不再依赖 `HUMAN_REVIEWED` 或 `NEEDS_REVIEW` 判断可用性。
- 来源清晰、数据有效、来源等级匹配用途的 fact 能被映射到合适的 `task_use_status`。

### Phase 6: 复核相关状态去门槛化和相关代码优化

目标：全面优化知识库中所有复核相关状态和相关代码，把“是否复核”从可用性门槛降级为历史审计信息；确认只要来源清晰明确、数据有效、来源等级匹配用途，数据即可直接进入对应任务流。

核心原则：

- 不再用 `NEEDS_REVIEW` 表示“不可用”。
- 不再用 `HUMAN_REVIEWED` 表示“唯一可用”。
- 不再用“待复核”作为事实、页面、导出样本的默认阻断理由。
- `evidence_status` 可以作为 legacy 字段保留一段时间，但不得作为 exporter、runtime loader、评估器、manifest 构建器的主判断字段。
- 主判断字段改为：
  - `source_status`: `source_anchored`, `source_missing`, `source_conflicted`, `source_damaged`, `source_level_mismatch`
  - `fact_validity`: `valid`, `conflicted`, `out_of_scope`, `encoding_damaged`, `obsolete_or_superseded`, `insufficient_anchor`
  - `authority_level`: `A0`, `A1`, `A2`, `SRC`, `RC`, `RULE`
  - `risk_class`: `normal_clinical`, `diagnostic`, `drug_boundary`, `high_regulatory`, `withdrawal_mrl_residue`, `food_safety`, `public_health`
  - `task_use_status`: `train_ready`, `eval_ready`, `generation_ready_limited`, `retrieval_only`, `blocked`

动作：

1. 全库检索复核相关字段和逻辑：
   - `NEEDS_REVIEW`
   - `HUMAN_REVIEWED`
   - `reviewed`
   - `review`
   - `待复核`
   - `人工复核`
   - `evidence_status`
2. 梳理受影响对象：
   - entity pages
   - source pages
   - `exports/*.csv`
   - `exports/knowledge_facts.json`
   - runtime manifest builder
   - readiness audit
   - hallucination risk audit
   - exporter
   - runtime loader
   - tests
3. 更新 schema 和 manifest：
   - 新增或补齐 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status`。
   - 将 `evidence_status` 标记为 legacy audit field。
   - 对旧 `HUMAN_REVIEWED`、`NEEDS_REVIEW` 建立一次性映射，但不再作为最终状态。
4. 更新判断逻辑：
   - 来源清晰且数据有效的普通临床事实，可进入 `train_ready` 或 `eval_ready`。
   - 来源清晰但用途受限的事实，进入 `generation_ready_limited`。
   - 来源清晰但只适合召回、别名、路由的页面，进入 `retrieval_only`。
   - 来源缺失、冲突未解释、乱码损坏、来源等级不匹配高风险用途的事实，进入 `blocked`。
5. 更新代码：
   - manifest 构建器不得因 `NEEDS_REVIEW` 自动降级为不可用。
   - exporter 不得以“未复核”作为拒绝导出的主因。
   - readiness audit 不再把 `NEEDS_REVIEW` 计为质量失败；只检查来源、有效性、风险和用途映射。
   - hallucination risk audit 重点检查 `source_missing`、`source_level_mismatch`、`fact_validity != valid` 和高风险无 A0。
   - tests 改为断言新字段和新规则。
6. 更新实体页：
   - 保留旧字段时只作迁移兼容，不作为页面正文判断依据。
   - 正文不再写“待复核所以不可用”，改写为具体原因，例如 `source_missing`、`source_level_mismatch`、`encoding_damaged`、`conflicted`。
7. 生成迁移报告：
   - 统计仍包含 legacy review 字段的文件。
   - 统计已完成新状态映射的页面和 facts。
   - 列出仍被 `blocked` 的具体原因。

产出：

- updated schema/status contract
- updated runtime manifest fields
- updated audit/exporter/loader logic
- `issues/review_status_migration_YYYY-MM-DD.json`
- `knowledge_change_records/YYYY-MM-DD-HHMM-review-status-migration.md`

验收：

- `rg "NEEDS_REVIEW|HUMAN_REVIEWED|待复核|人工复核" ai-/knowledge/llm_wiki_swine_authoritative` 的结果只允许出现在历史记录、迁移报告或 legacy 字段说明中。
- runtime manifest 主字段不再依赖 `evidence_status` 判断可用性。
- exporter 以 `source_status + fact_validity + authority_level + risk_class + task_use_status` 判断导出。
- 来源清晰、数据有效、来源等级匹配用途的数据能够直接使用。
- 高风险结论仍必须满足 A0 或标签级等价来源，不因取消复核门槛而放宽。

### Phase 7: 黄金数据集用途分层

目标：把知识库事实转化为可控的数据集生产输入。

动作：

1. 为 disease/drug/comparison/syndrome/rule_card/synthesis manifest 记录写入：
   - `task_use_status`
   - `gold_dataset_role`
   - `allowed_question_types`
   - `blocked_question_types`
2. 生成 `exports/gold_dataset_readiness_index.csv`，至少包含：
   - `entity_id`
   - `entity_type`
   - `page_relpath`
   - `task_use_status`
   - `gold_dataset_role`
   - `positive_generation_allowed`
   - `negative_trap_allowed`
   - `evaluation_allowed`
   - `requires_rule_cards`
   - `source_ids`
   - `missing_critical_fields`
3. 定义 exporter 门禁：
   - `train_ready`: 可进入 SFT，但答案必须带 source/fact/rule。
   - `eval_ready`: 可进入评估、对比、裁判训练。
   - `generation_ready_limited`: 可生成候选，但必须保留边界。
   - `retrieval_only`: 只用于召回、别名、路由。
   - `blocked`: 不进入生成或评估。
4. 对药物页单独生成 `drug_gold_role_index`：
   - `boundary_only`
   - `negative_trap`
   - `exclude_from_positive_generation`
   - `positive_label_candidate`

产出：

- `exports/gold_dataset_readiness_index.csv`
- 更新后的 exporter 规则
- QA/case 生成前置门禁

验收：

- 任一导出样本都能追溯 source/fact/rule。
- 高风险问题无 A0 或标签级来源时自动降级或拒绝导出。
- `retrieval_only` 和 `blocked` 不进入正向 SFT。

### Phase 8: 高风险规则卡和评估 rubrics 加固

目标：让模型微调和评估阶段都遵守同一套安全边界。

动作：

1. 检查并补强核心 rule cards：
   - `RC-DX-001`
   - `RC-DRUG-001`
   - `RC-WITHDRAWAL-MRL-001`
   - `RC-DISEASE-REGULATORY-001`
   - `RC-CITATION-001`
   - `RC-TRAIN-READY-001`
   - `RC-EVAL-RUBRIC-001`
2. 确保 disease/drug 页面引用相关 rule cards。
3. 确保 synthesis 中评估 rubrics 与 rule cards 一致。
4. 为 exporter 增加 hard-block checks：
   - unsupported dose
   - unsupported withdrawal/MRL
   - unsupported regulatory action
   - single-test causality overclaim
   - no source citation
   - source level mismatch

产出：

- 更新后的 rule cards
- `exports/rule_card_index.csv`
- evaluator/exporter rule integration report

验收：

- 所有高风险样本必须被 rule card 约束。
- hard-block rule cards 缺失数 = 0。
- evaluator 能识别无来源结论、过度外推和监管越界。

### Phase 9: 索引、图谱和检索质量重建

目标：清洗后重建所有可派生产物，不保留旧图谱和旧索引噪声。

动作：

1. 重建 source index、disease index、drug index、rule index、comparison index、synthesis index。
2. 重建 knowledge graph。
3. 重建 runtime manifest。
4. 重建 `knowledge_facts.json` 或至少生成 integrity report。
5. 对检索进行抽样：
   - 症状到疾病召回。
   - 疾病到鉴别页。
   - 疾病到规则卡。
   - 药物到边界页。
   - 监管问题到拒答或官方来源要求。

产出：

- rebuilt indexes
- rebuilt graph
- retrieval smoke test report

验收：

- missing paths = 0.
- graph build succeeds.
- runtime loader 使用 manifest。
- 抽样查询不命中 raw、issues、huge matrices。

### Phase 10: 猪病专用测试和 CI 化

目标：把清洗质量变成可重复验证的工程约束。

动作：

1. 新增猪病 wiki fixture，不替换历史鸡病兼容测试。
2. 增加测试：
   - load swine runtime manifest
   - denylist excludes raw/issues/graph/matrices
   - task_use_status controls exporter
   - drug high-risk claims require A0/label-level source
   - partial pages route to gap handling
   - all exported cases contain source/fact/rule citations
3. 增加编码完整性测试。
4. 增加黄金数据集导出 smoke test。

产出：

- pytest tests
- audit scripts
- CI/runbook commands

验收：

```powershell
pytest .\ai-\tests\test_llm_wiki_knowledge.py
pytest .\ai-\tests\test_swine_llm_wiki_runtime.py
```

通过标准：

- 猪病 runtime 测试全部通过。
- 历史兼容测试不被破坏。
- 新导出的样本均有 source/fact/rule provenance。

### Phase 11: 黄金数据集试生产和人工抽检

目标：验证清洗后的知识库能稳定支撑高质量训练与评估数据。

动作：

1. 从 `train_ready` 生成小批量 SFT 样本。
2. 从 `eval_ready` 生成评估样本。
3. 从 drug `negative_trap` 生成安全陷阱样本。
4. 从 `generation_ready_limited` 生成带边界的候选样本。
5. 人工抽检：
   - source/fact/rule 是否存在。
   - 答案是否过度外推。
   - 高风险结论是否有 A0 或标签级支持。
   - JSON 字段是否完整。
   - 问题和答案是否适合微调。

产出：

- pilot train dataset
- pilot eval dataset
- rejection report
- manual inspection notes

验收：

- 样本 provenance 完整率 = 100%。
- 高风险越界率 = 0。
- 抽检通过率达到项目设定阈值后，才能进入批量生产。

## 6. 推荐执行顺序

优先级 P0：

1. Phase 0 baseline.
2. Phase 1 root metadata.
3. Phase 2 encoding integrity.
4. Phase 3 runtime allowlist/denylist.

优先级 P1：

1. Phase 4 entity compaction.
2. Phase 5 source/fact authority normalization.
3. Phase 6 review-status migration and code optimization.
4. Phase 7 gold dataset readiness index.
5. Phase 8 rule-card hard gates.

优先级 P2：

1. Phase 9 index/graph rebuild.
2. Phase 10 swine-specific tests.
3. Phase 11 pilot dataset production.

## 7. 不建议立即做的事

1. 不建议一次性重写所有疾病和药物页。当前 readiness 高，应该以 manifest 和高风险页为主线逐步清洗。
2. 不建议删除 raw 和 issues。它们是审计和追溯资产，只应从默认检索中隔离。
3. 不建议把 synthesis 巨大矩阵直接压缩进实体页。应迁移或保留为 evidence expansion。
4. 不建议用模型记忆补齐缺口。所有新增事实必须有 source/fact/rule anchor。
5. 不建议把 A1/A2 或教材来源外推为中国监管、兽药标签、休药期、MRL 或食品安全结论。

## 8. 每阶段通用验收门槛

每次清洗后至少运行：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

必须满足：

- readiness score >= 99.
- missing indexed paths = 0.
- bad fact tables = 0.
- high-risk runtime page count = 0.
- runtime manifest 可解析。
- 默认检索不加载 raw、issues、graph、huge matrices。
- 新增事实都有 source/fact/rule anchor。
- 新增高风险结论有 A0 或标签级等价来源。
- diseases/drugs 实体页同类条目已归并去重，且来源锚点未丢失。

### 8.1 每次修改的工作留痕要求

每一次修改都必须在根目录 `knowledge_change_records/` 新增 Markdown 说明文档。文件名建议：

```text
YYYY-MM-DD-HHMM-short-topic.md
```

说明文档必须包含：

1. 修改目标和范围。
2. 修改前存在的问题。
3. 修改前相关代码、脚本、索引、实体页或知识文件的状态。
4. 本次更新或新增了什么代码。
5. 本次进行了什么知识整理、页面归并、去重、迁移或索引重建。
6. 修改后解决了什么问题。
7. 预计会产生什么更新效果，包括对生成、评估、检索、黄金数据集生产的影响。
8. 运行了哪些验证命令，结果是什么。
9. 仍然存在的风险和下一步待办。

如果本次没有改代码，只做知识库整理，也必须明确写出“未改代码，仅整理知识文件/索引/文档”。

### 8.2 防乱码要求

所有清洗、读取、写入、脚本输出和审计过程必须按 UTF-8 执行，防止中文实体名、疾病名、药物名、来源标题和证据锚点在更新过程中被乱码污染。

Windows PowerShell 执行维护命令前应设置：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

脚本要求：

- Python 读写文本必须显式使用 `encoding="utf-8"` 或 `encoding="utf-8-sig"`。
- JSON 输出必须使用 `ensure_ascii=False`，并用 UTF-8 写入。
- CSV 读写优先使用 `utf-8-sig`，便于 Excel 和中文字段兼容。
- 修改前后运行编码完整性扫描，检查 replacement character `�` 和 mojibake-like 字符模式。
- 发现疑似乱码时不得继续批量覆盖文件，必须先隔离、记录并从原始来源或备份恢复。

## 9. 交付物清单

最终清洗完成后应至少交付：

1. `purpose.md`: swine-specific purpose.
2. `.wiki-schema.md`: swine wiki schema and task-use contract.
3. `README.md`: current state and operating guide.
4. `exports/runtime_core_manifest.json`: production/evaluation allowlist.
5. `exports/runtime_exclude_patterns.json`: denylist.
6. `exports/gold_dataset_readiness_index.csv`: dataset production gate.
7. `exports/drug_gold_role_index.csv`: drug page dataset role gate.
8. `issues/encoding_integrity_audit_YYYY-MM-DD.json`.
9. `issues/runtime_retrieval_smoke_test_YYYY-MM-DD.md`.
10. `issues/gold_dataset_pilot_inspection_YYYY-MM-DD.md`.
11. Updated tests for swine runtime and exporter gates.
12. One `knowledge_change_records/` document per cleanup batch.
13. Per-change work-trace records for code, index, entity-page, source-page, rule-card, export, or cleanup-strategy updates.

## 10. 成功定义

清洗整理完成不是指页面数量更多，而是指：

- 任何生产或评估调用都知道该加载哪些页、排除哪些页。
- 任何训练样本都能追溯到 source/fact/rule。
- 任何高风险结论都被来源等级和规则卡约束。
- 部分页只用于召回和缺口路由，不被误当完整答案依据。
- 药物页不会单独生成处方、剂量、疗程、休药期、MRL 或食品安全结论。
- 评估集能稳定惩罚无来源、过度外推、监管越界和药物越界。
- 新增来源和新增批次都有日志、审计、manifest、索引和回滚记录。
- diseases/drugs 实体页不再靠历史补强块堆叠表达知识，而是按知识类型清晰归并、去重并保留完整来源追溯。
- 每次修改都有 `knowledge_change_records/` 留痕，可直接用于阶段性工作汇报。
- 清洗过程不会把中文内容、来源标题、实体名称或证据锚点写成乱码。

这才是能支撑猪病生产与评估项目持续生产高质量黄金数据集的知识库状态。
