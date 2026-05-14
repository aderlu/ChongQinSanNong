# 猪病 LLM Wiki 数据源与数据增删改查治理规范

本文档是 `llm_wiki_swine_authoritative` 的强制数据治理规则，用于规范所有数据源、事实、实体页、规则卡、证据扩展、索引导出和黄金数据集相关数据的增删改查。它不是单纯的代码操作说明，而是医学类知识库的事实治理规则：什么时候可以新增，什么时候应该修改，什么时候只能降级或归档，什么时候可以删除，以及每种处理背后的理由。

猪类疾病知识库属于兽医医学与监管高风险领域。所有疾病、诊断、药物、剂量、疗程、休药期、MRL、残留、食品安全、检疫、扑杀、调运和官方处置相关数据，都必须遵循“来源优先、事实可追溯、风险可门禁、旧数据不静默覆盖”的原则。

本规范与 `WIKI_MAINTENANCE_GUIDE.md` 共同构成 Wiki 更新的强制前置门禁。任何维护者、脚本、批处理流程或人工整理流程，在从网页、本地 Markdown、本地 PDF/Word/Excel、历史 issue、raw 材料、模型输出、评估反馈中写入或调整知识库内容前，都必须先执行本规范。

执行时优先读取两份短执行卡：

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`

短卡用于每次快速执行；本文档用于处理具体复杂场景和事实逻辑判断。

强制执行要求：

1. 任何新增、查询、修改、删除、迁移、归档或重建操作，都必须先判断对象层级和 CRUD 类型。
2. 任何来源或事实进入 runtime、exports、gold dataset 前，都必须具备来源锚点、状态字段和任务用途判断。
3. 任何旧数据处理都必须说明原因：规则更新、旧版本过时、来源冲突、事实错误、编码损伤、页面过大、重复数据或任务门禁变化。
4. 任何覆盖、删除、降级、迁移或归档都必须有工作留痕，并说明旧数据的追溯位置。
5. 如果脚本实现与本文档冲突，不能以脚本结果为准；应先修正文档或脚本，使两者一致，并记录变更。

## 0. 强制落地流程

每次维护必须按以下顺序执行：

1. 读取两份短执行卡。
2. 定义任务：说明是新增来源、补事实、修事实、压缩页面、替换旧版本、处理冲突、重建索引、生成样本，还是删除/归档。
3. 判定对象层级：raw、source、fact、evidence expansion、runtime page、rule card、synthesis、export、issue、gold dataset。
4. 判定 CRUD 类型：新增、查询、修改、删除、迁移、归档、降级、重建。
5. 判定来源等级：A0、A1、A2、SRC、RC/RULE。
6. 判定风险类别：normal、diagnostic、drug_boundary、high_regulatory、withdrawal_mrl_residue、food_safety、public_health。
7. 判定任务用途：train_ready、eval_ready、generation_ready_limited、retrieval_only、blocked。
8. 处理旧数据：明确旧数据保留、降级、归档、迁移、排除、替代或删除的理由。
9. 通过 `tools/run_guarded_wiki_update.py` 执行更新。
10. 重建导出：涉及 runtime、source、fact、rule、graph、gold dataset 时，必须重建对应 exports。
11. 固定入口自动运行验收；如失败必须修复或记录临时例外。
12. 写变更记录：按 `CHANGE_RECORD_TEMPLATE.md` 和本文第 13 节记录事实逻辑。

不允许跳过以上流程直接把网页内容、本地 Markdown 内容、PDF 摘录或批量抽取结果写入 runtime 页面。

## 1. 总体维护目标

本知识库的维护目标不是不断堆叠内容，而是长期保持以下状态：

- 数据源清楚：每条事实可以追溯到 `source_id`、URL、文件路径、页码、章节、表格、条款或等价证据锚点。
- 事实有效：事实必须有明确主体、谓词、对象和适用范围，不能把候选抽取、模型推断或无定位材料当成正式事实。
- 运行时简洁：默认检索只加载 `runtime_core_manifest.json` 允许的核心页面，不加载 raw、issues、graph、巨大矩阵和 evidence expansion。
- 风险可控：药物、诊断、监管、休药期、MRL、残留和食品安全内容必须通过规则卡和权威来源门禁。
- 版本可追溯：旧数据被新规则或新来源替代时，不静默覆盖；必须说明旧数据为何过时、被降级、被迁移或被排除。
- 样本可门禁：黄金数据集生产必须依赖 `gold_dataset_readiness_index.csv`、`drug_gold_role_index.csv` 和 `exporter_hard_block_rules.json`。

强制性判断：如果一项维护不能证明上述目标不被破坏，则该维护不能合并到当前 Wiki。

## 2. 当前知识库对象分层

维护时必须先判断操作对象属于哪一层。不同层级的增删改查规则不同。

| 层级 | 目录或文件 | 作用 | 默认是否进入 runtime |
| --- | --- | --- | --- |
| 原始证据层 | `raw/` | PDF、网页、Excel、扫描件、原始抽取材料 | 否 |
| 来源注册层 | `wiki/sources/`、`exports/source_index.csv` | 记录来源身份、等级、路径、限制 | 来源页本身通常不直接进入 runtime |
| 事实索引层 | `exports/knowledge_facts.json`、`exports/knowledge_facts_status_index.json` | 结构化事实和事实状态 | 通过页面或索引间接使用 |
| 证据扩展层 | `wiki/evidence_expansions/` | 长摘录、批量事实、历史增强块、审计证据 | 否 |
| 运行时实体页 | `wiki/diseases/`、`wiki/drugs/`、`wiki/comparisons/`、`wiki/syndromes/` | 默认检索的简洁知识页 | 是，需在 manifest 中 |
| 规则卡层 | `wiki/rule_cards/` | 诊断、药物、监管、引用、评估门禁 | 是 |
| 综合策略层 | `wiki/synthesis/` | 检索策略、生成边界、评估 rubrics、阻断规则 | 部分进入 runtime |
| 导出索引层 | `exports/` | manifest、denylist、gold readiness、rule index、graph 输入 | 机器使用 |
| 审计留痕层 | `issues/`、`knowledge_change_records/` | 审计报告、问题清单、阶段记录 | 否 |

核心原则：原始证据和长证据要保留，但不直接进入默认生产检索；运行时页面只保留短摘要、来源锚点、规则卡锚点和使用边界。

## 3. 来源分级与事实用途

新增或修改任何来源前，必须先判定来源等级。

| 等级 | 来源类型 | 可以支持什么 | 不能支持什么 |
| --- | --- | --- | --- |
| A0 | 官方法规、农业农村部公告、国家标准、官方数据库、官方疫病防控规范 | 监管处置、法定疫病、检疫、扑杀、调运、禁停用药、MRL、食品安全等高风险结论 | 不能外推到未覆盖辖区、未覆盖日期或未覆盖对象 |
| A1 | 兽药标签、说明书、批准文号资料、官方注册资料 | 标签内适应证、物种、用法边界、禁忌、休药期 | 不能外推到未标注疾病、剂型、物种或用法 |
| A2 | 权威教材、手册、行业指南、国际组织资料 | 疾病概述、临床表现、流行病学、诊断思路、防控框架 | 不能替代中国当前监管、标签、MRL 和法定处置 |
| SRC | 论文、综述、病例、普通网页、内部整理、批量抽取 | 研究证据、候选事实、补充背景、问题线索 | 单篇研究或普通网页不能直接生成处方、监管或食品安全结论 |
| RC/RULE | 规则卡、synthesis 策略页 | 生成、评估、拒答、路由和门禁 | 不能创造新的疾病或药物事实 |

事实是否能被使用，必须同时满足：

- `source_status=source_anchored`
- `fact_validity=valid`
- `authority_level` 与任务风险匹配
- `risk_class` 已识别
- `task_use_status` 已给出
- 必要规则卡存在

`HUMAN_REVIEWED` 和 `NEEDS_REVIEW` 只作为历史审计字段，不再作为允许或禁止使用的主门槛。

## 4. 数据新增规则

新增前置检查：

- 是否已阅读 `WIKI_MAINTENANCE_GUIDE.md`。
- 是否已完成 `SOURCE_BATCH_INTAKE_CHECKLIST.md` 中来源、事实、落位、护栏、批处理和审计检查。
- 是否明确新数据来自网页、本地 Markdown、本地权威文档、raw 材料、历史 issue、模型输出还是人工整理。
- 是否明确新数据进入哪一层，而不是默认进入 runtime。

### 4.1 新增来源

新增来源前必须先回答：

1. 这个来源是否已经存在？
2. 它是同一来源的新版本，还是完全不同来源？
3. 它的权威等级是什么？
4. 它能支持哪些结论，不能支持哪些结论？
5. 它是否涉及药物、监管、休药期、MRL、残留或食品安全等高风险内容？

新增逻辑：

- 如果是全新来源，新增 `wiki/sources/<source_id>.md`，并更新或重建 `exports/source_index.csv`。
- 如果是同一来源的新版本，不能直接覆盖旧来源。应新建带版本或日期的 `source_id`，或在旧来源页中明确标记 `superseded_by`。
- 如果只是旧来源的补充定位，例如补页码、URL、章节，应修改原 source 页并记录原因。
- 如果来源只是网页线索或未核验材料，不得直接进入 runtime 正文，只能进入候选层或 evidence expansion。

必须记录：

- `source_id`
- 标题
- 发布机构或作者
- 日期或版本
- URL 或文件路径
- 访问日期
- 辖区
- 来源等级
- `supports`
- `does_not_support`
- 适用范围和不得外推边界

事实逻辑：

- 新来源不是越新越优先。医学和监管知识要看权威等级、适用辖区、适用对象和版本时效。
- 同一主题下，新版本法规通常替代旧版本法规；但旧版本仍可保留为历史追溯，不进入当前 runtime。
- 普通网页更新日期较新，不代表可以覆盖 A0/A1 来源。

网页来源强制规则：

- 官方网页必须记录发布机构、URL、发布日期或更新时间、访问日期和辖区。
- 非官方网页默认最多为 SRC 线索，不得支持高风险正向结论。
- 网页内容若引用法规、标准、标签或论文，必须优先追溯到被引用的原始来源。

本地 Markdown 来源强制规则：

- 本地 `.md` 文档只有在能说明原始来源、生成流程、版本和来源锚点时，才可注册为 source。
- 历史 issue、脚本输出、模型整理稿、旧批处理 Markdown 默认是审计或候选材料，不是权威 source。
- 从本地 Markdown 提取事实时，应尽量回到其引用的原始 PDF、网页、表格或 source 页核验。

### 4.2 新增事实

新增事实前必须先检索是否已有同义事实。新增事实必须具备：

- 主体，例如疾病、药物、病原、规则对象。
- 谓词，例如导致、表现为、禁用、需要核验。
- 客体，例如具体症状、检测方法、监管动作、药物边界。
- 来源锚点。
- 适用范围，例如猪、仔猪、母猪、育肥猪、地区、时间、剂型。
- 风险类别。

新增逻辑：

- 普通临床事实可进入 `knowledge_facts_status_index.json`，并在 runtime 页面中用短句表达。
- 大量批量事实、表格、候选事实进入 `wiki/evidence_expansions/`，不直接进入 runtime。
- 药物剂量、疗程、给药途径、休药期、MRL、残留和食品安全事实，必须有 A0/A1 或标签级等价来源；否则只能作为 negative trap、边界提醒或待核验线索。
- 单篇论文中的发现不得直接转成生产建议，应标为研究证据或候选事实。

事实逻辑：

- “有来源”不等于“可生成”。来源等级必须匹配任务风险。
- “事实存在”不等于“事实完整”。缺少物种、剂型、辖区、用法或时间边界时，只能有限使用。
- “诊断相关事实”不能直接推出确诊。必须遵守 `RC-DX-001`，区分临床怀疑、样本、方法、检出、因果关系和鉴别诊断。

### 4.3 新增运行时页面内容

运行时页面新增内容必须短、清楚、可追溯。新增时优先更新：

- 页面身份
- 核心摘要
- 来源锚点
- 规则卡锚点
- 缺口说明
- evidence expansion 路由

禁止把以下内容直接新增到 runtime 页面：

- 原始 PDF 长摘录
- 网页全文
- Excel 大表
- 大段候选事实
- 批处理增强块
- 无来源经验判断
- 非 A0/A1 支持的药物或监管操作建议

事实逻辑：

- runtime 页面服务默认检索，不是证据仓库。
- 长证据不是删除，而是迁移到 evidence expansion，并在 runtime 页面留下短占位符和路径。

## 5. 数据查询规则

查询不是只看页面正文。维护者应按以下顺序查询：

1. 查 runtime manifest：确认页面是否默认进入生产或评估检索。
2. 查 source index：确认来源是否存在、路径是否存在、等级是否清楚。
3. 查 fact status index：确认事实是否有效、风险类别和任务用途。
4. 查 runtime 页面：确认是否有短摘要和规则卡锚点。
5. 查 evidence expansion：查看长证据、批量抽取、历史增强块。
6. 查 issues 和 change records：确认该事实是否曾被迁移、降级、隔离或标记为风险。

推荐查询对象：

- `exports/runtime_core_manifest.json`
- `exports/runtime_exclude_patterns.json`
- `exports/source_authority_status_index.csv`
- `exports/knowledge_facts_status_index.json`
- `exports/gold_dataset_readiness_index.csv`
- `exports/drug_gold_role_index.csv`
- `exports/exporter_hard_block_rules.json`
- `knowledge_change_records/`

事实逻辑：

- 如果 runtime 页面没有某个长证据，不代表证据不存在，可能已经迁移到 evidence expansion。
- 如果旧事实在原始 `knowledge_facts.json` 中存在，不代表当前可用于生成，应以标准化后的 `knowledge_facts_status_index.json` 和 gold readiness 为准。
- 如果页面处于 `runtime_core_partial`，它是缺口路由页，不是完整知识页。

## 6. 数据修改规则

修改必须区分四类情况：事实修正、表达优化、规则更新、版本替代。

修改前必须回答：

1. 修改是因为事实错误，还是只是表达不清？
2. 修改是因为新来源更权威，还是因为旧版本过时？
3. 修改是因为规则门槛变化，还是事实本身变化？
4. 修改会不会影响 runtime manifest、gold dataset、pilot 样本或图谱？
5. 修改后旧数据在哪里可追溯？

### 6.1 事实错误修正

适用场景：

- 原事实与来源不符。
- OCR、抽取、翻译或人工整理错误。
- 事实主体、对象、物种、剂型、辖区或适用范围写错。

处理规则：

- 修改 runtime 页面中的错误摘要。
- 修改或重建结构化事实索引。
- 在 evidence expansion 或 source 页保留原始证据定位。
- 在 `knowledge_change_records/` 记录错误原因、修改前内容、修改后内容和验证方式。
- 如果错误已影响导出样本，必须重建相关 gold/pilot 数据并记录影响范围。

事实逻辑：

- 医学事实错误必须修正，不能只靠增加一条新事实抵消。
- 但错误来源或错误抽取痕迹不应静默删除，应保留在审计记录中说明“因抽取错误废弃”。

### 6.2 表达优化

适用场景：

- 文字冗长。
- 同一事实多处重复。
- 页面结构不清。
- 缺少规则卡锚点或来源锚点。

处理规则：

- 可以改写 runtime 页面摘要，但不得改变事实含义。
- 大段内容迁移到 evidence expansion。
- 重复事实合并为一个主表达，其他来源作为证据锚点。
- 修改后运行 manifest 和 hallucination audit。

事实逻辑：

- 表达优化不能扩大适用范围。
- “猪场可使用”不能从“某产品标签用于某适应证”外推。
- “可作为诊断参考”不能改成“可确诊”。

### 6.3 规则更新导致的修改

适用场景：

- 新增规则卡。
- 审计脚本更新。
- gold dataset 门禁更新。
- 原 `NEEDS_REVIEW`、`HUMAN_REVIEWED` 迁移为 legacy 字段。

处理规则：

- 优先修改 schema、manifest、规则卡和导出索引。
- 页面正文只补充边界锚点和用途说明，不新增事实。
- 旧字段保留为 `legacy_evidence_status` 或历史审计字段。
- 不因规则变化而删除旧事实，除非事实本身错误或无来源。

事实逻辑：

- 规则更新通常改变“能否用于某任务”，不一定改变“事实是否存在”。
- 例如一个事实可以从 `train_ready` 降级为 `generation_ready_limited`，原因可能是高风险门槛提高，而不是事实变假。

### 6.4 新版本来源替代旧版本

适用场景：

- 法规、标准、标签、官方公告更新。
- 旧标签被新标签替代。
- 旧药典或手册版本过时。

处理规则：

- 新版本作为新来源登记，明确版本和日期。
- 旧来源保留，但标记为历史或被替代。
- 当前 runtime 应采用现行版本的结论。
- 旧版本事实可降级为 `obsolete_or_superseded`、`retrieval_only` 或历史证据。
- 涉及监管、休药期、MRL、禁停用药时，必须优先当前 A0/A1 来源。

事实逻辑：

- 旧版本过时不等于无价值。它可用于历史解释、差异分析和审计，但不能作为当前生成结论。
- 新旧版本冲突时，不做平均、不折中；按权威等级、现行性、辖区和适用对象判断。

## 7. 数据删除与归档规则

医学知识库原则上不做静默删除。删除必须非常谨慎，优先采用“排除、降级、归档、迁移、标记失效”。

删除审批判断：

- 删除是否会破坏 source/fact/page/sample provenance。
- 删除对象是否在 `runtime_core_manifest.json`、`source_index.csv`、`knowledge_facts_status_index.json`、`gold_dataset_readiness_index.csv`、`drug_gold_role_index.csv`、图谱或 pilot 样本中出现。
- 是否可以用 denylist、降级、obsolete 标记、evidence expansion 迁移或 issue 归档替代删除。
- 是否已有 change record 说明删除理由。

### 7.1 可以直接删除的情况

仅限以下低风险对象：

- 临时文件。
- 重复生成且没有独立信息的中间产物。
- 空文件。
- 明显无用的缓存。
- 已确认不被任何 source/fact/page/index 引用的错误测试文件。

删除前必须确认：

- 不在 runtime manifest 中。
- 不被 source index、fact index、gold index 或页面链接引用。
- 删除原因写入 change record。

### 7.2 不应直接删除的情况

以下对象不得直接静默删除：

- 已注册 source。
- 已被 fact 引用的 source。
- 已进入 runtime manifest 的页面。
- 已用于 gold dataset 或 pilot dataset 的事实。
- 旧法规、旧标签、旧手册版本。
- 存在编码损伤但可用于历史定位的 raw 材料。

处理方式：

- 如果来源过时：标记为 superseded 或 obsolete。
- 如果事实无效：标记 `fact_validity=obsolete_or_superseded`、`out_of_scope`、`conflicted` 或 `insufficient_anchor`。
- 如果页面不应进入默认检索：从 manifest allowlist 移除，或加入 denylist 范围。
- 如果内容过长：迁移到 evidence expansion。
- 如果编码损坏：隔离到 issues/raw 层，并保证 runtime damaged count 为 0。

事实逻辑：

- 删除会破坏追溯链，尤其是医学和监管数据。大多数情况下应保留证据并改变使用状态。
- “不用作当前结论”不等于“从知识库消失”。

## 8. 旧数据处理规则

旧数据分为五类，处理方式不同。

### 8.1 旧版本但事实仍正确

例如旧教材中的疾病概述、病原描述、临床表现。处理方式：

- 保留为历史或补充来源。
- 如果与当前权威来源一致，可作为辅助 evidence anchor。
- 不作为高风险监管或药物标签结论的主来源。

### 8.2 旧版本已被新法规或标签替代

例如旧休药期、旧禁用药政策、旧法定疫病分类。处理方式：

- 标记为 `obsolete_or_superseded`。
- 当前 runtime 摘要改用新 A0/A1 来源。
- 旧数据保留在 source 或 evidence expansion，用于追溯。
- gold dataset 中不得作为正向答案来源，可作为 outdated trap 或 evaluation trap。

### 8.3 旧批处理增强块

例如 V13.1/V14、Reinforcement、Completion、Batch 块。处理方式：

- 从 runtime 页面迁移到 `wiki/evidence_expansions/`。
- runtime 页面保留短占位符和路径。
- 不进入默认检索。
- 如有事实价值，可后续人工核验后再抽取为正式 fact。

### 8.4 旧字段和旧复核状态

例如 `evidence_status=HUMAN_REVIEWED/NEEDS_REVIEW`。处理方式：

- 不再作为主门槛。
- 保留为 `legacy_evidence_status`。
- 新判断使用 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status`。

### 8.5 旧图谱、旧索引和旧导出

处理方式：

- 派生产物应重建，不手工修补。
- 旧备份可保留为 `*.p0_backup_*`，并由 denylist 排除。
- 当前生产和评估只使用最新 manifest、index、graph 和 readiness。

## 9. 冲突数据处理规则

冲突数据必须先判定冲突类型。

| 冲突类型 | 示例 | 处理方式 |
| --- | --- | --- |
| 版本冲突 | 新旧法规或标签不同 | 现行版本优先，旧版本标记过时 |
| 辖区冲突 | 国际资料与中国监管不同 | 中国任务用中国 A0/A1；国际资料仅作背景 |
| 对象冲突 | 来源适用于牛/鸡/宠物，不适用于猪 | 标记 out_of_scope，不外推 |
| 剂型冲突 | 同一药物不同剂型休药期不同 | 拆分事实，注明剂型，不合并 |
| 研究冲突 | 多篇论文结果不同 | 标记研究证据，不生成生产建议 |
| 抽取冲突 | OCR 或模型抽取不一致 | 回到原文核验，不能用投票决定 |

事实逻辑：

- 高风险冲突不能用“多数来源”解决，必须看权威等级和适用范围。
- 未解决冲突的事实应设置 `source_status=source_conflicted` 或 `fact_validity=conflicted`，并降级为 `retrieval_only` 或 `blocked`。

## 10. 各类数据 CRUD 具体规则

### 10.1 Source 页

新增：

- 新建 source 页，登记来源元数据和可支持/不得外推边界。

查询：

- 通过 `source_id`、标题、URL、文件路径、来源等级查询。

修改：

- 可补充定位信息、来源限制、版本状态、authority level。
- 不可把低等级来源改成高等级，除非来源身份核验发生变化。

删除：

- 已被引用的 source 不删除。
- 错误 source 应标记为 invalid、out_of_scope 或 superseded，并从当前任务门禁中排除。

### 10.2 Fact 数据

新增：

- 必须有 source anchor、主体、谓词、客体和适用范围。

查询：

- 优先查 `knowledge_facts_status_index.json`，不要只看原始 `knowledge_facts.json`。

修改：

- 事实错误要修正；适用范围不清要降级；高风险来源不够要限制用途。

删除：

- 原则上不删除已登记事实，而是设置 `fact_validity`。
- 只有重复或明显误抽取且无引用的事实可在重建索引时移除。

### 10.3 Disease 页面

新增：

- 只新增核心身份、病原、宿主、临床表现、诊断边界、防控边界和来源锚点。

修改：

- 不可从症状直接写确诊结论。
- 涉及监管动作必须要求 A0 当前来源。
- 涉及药物治疗必须转入药物页、规则卡和标签核验。

删除：

- 不删除疾病页；若证据不足，降级为 partial 或 gap-routing。

### 10.4 Drug 页面

新增：

- 药物页是边界页和检索路由页，不是独立处方来源。
- 必须有 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`。

修改：

- 剂量、疗程、给药途径、禁忌、休药期、MRL、残留和食品安全必须核验 A0/A1。
- 非 A0/A1 来源只能支持边界、负样本陷阱或待核验线索。

删除：

- 不删除药物页；证据不足时降级为 retrieval_only、boundary_only 或 negative_trap。

### 10.5 Evidence Expansion

新增：

- 存放长证据、批量抽取、历史增强块和审计材料。

查询：

- 用于人工复核、溯源和二阶段检索。

修改：

- 只做结构化、路径修复和来源锚点补充，不改写原始事实含义。

删除：

- 一般不删除；如重复生成，可保留一份主文件并在 change record 中说明。

### 10.6 Rule Card 和 Synthesis

新增：

- 规则卡必须短、稳定、机器可引用。
- synthesis 只能做策略、路由、拒答和评估，不创造医学事实。

修改：

- 规则更新会影响任务用途和 hard-block，不应直接改事实真假。

删除：

- 已被页面引用的规则卡不得删除。废弃规则应标记 deprecated，并提供替代规则卡。

### 10.7 Export 和 Graph

新增或修改：

- 这些是派生产物，应由脚本重建。

删除：

- 旧备份可归档或由 denylist 排除，不作为 runtime 输入。

事实逻辑：

- 导出文件不是事实真源。事实真源是 source、fact、runtime 页面和 evidence anchors。

### 10.8 Gold Dataset 和 Pilot 样本

新增：

- 必须从 readiness 和 drug role index 中抽取。
- 必须带 source/rule provenance。

修改：

- 如果来源、规则或事实状态变更，样本必须重建或重新验收。

删除：

- 有高风险越界、缺 provenance、JSON 不完整或来源等级不匹配的样本应从正式数据集中剔除，保留问题记录。

## 11. 高风险内容强制门禁

以下内容如果缺少对应来源和规则卡，必须阻断正向生成：

- 剂量、用量、疗程、给药、处方。
- 休药期、停药期、MRL、残留、屠宰、可食组织、食品安全。
- 上报、扑杀、封锁、检疫、调运、无害化处理。
- 单次 PCR、Ct、抗体阳性、抗原阳性直接推出确诊或因果关系。
- 无 source_id、fact_id、URL、页码、表格、条款或规则卡的高价值答案。

对应机器门禁文件：

- `exports/exporter_hard_block_rules.json`

对应关键规则卡：

- `RC-DX-001`
- `RC-DRUG-001`
- `RC-WITHDRAWAL-MRL-001`
- `RC-DISEASE-REGULATORY-001`
- `RC-REGULATORY-CURRENT-001`
- `RC-CITATION-001`
- `RC-EVAL-RUBRIC-001`
- `RC-SYNTHESIS-SCOPE-001`
- `RC-PARTIAL-GAP-ROUTING-001`

## 12. 每次维护后的验收

每次新增、修改、降级、迁移、删除或重建必须通过固定入口执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'

python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python <你的更新脚本或命令>
```

该入口会自动运行治理预检、更新命令和完整验收。
完整验收会重建 `graph-data.json`、`knowledge-graph.md`、`knowledge-graph.html`，并生成 `knowledge-graph-changes.html`、`issues/graph_change_diff_last.json` 和 `issues/wiki_crud_change_log.jsonl`。

如果只是做全量验收而不执行更新命令，可运行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'

python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

如需定位具体失败项，再分步运行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'

python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase9_rebuild_indexes_graph_smoke.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_graph_change_diff.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py
python -m pytest .\ai-\tests\test_swine_llm_wiki_runtime.py -q
```

验收标准：

- manifest 可重建。
- `missing_paths=0`。
- high risk 为 0。
- medium risk 为 0，或有明确临时例外和处理计划。
- readiness score 不低于当前基线 99。
- runtime damaged count 为 0。
- 不新增无来源高风险事实。
- 不新增无边界大页面。
- 不新增缺 provenance 的黄金数据集样本。
- `audit_governance_compliance.py` 通过，说明两份治理文档、入口文件和最新变更记录仍保持强制治理链路。

如验收未通过：

- 不得把本次修改视为完成。
- 必须修复问题，或在 change record 中标记为临时例外。
- 临时例外必须写明影响范围、为什么不能立即修复、下一步修复计划和阻断哪些生产/评估用途。

## 13. 修改留痕

每次维护必须在 `knowledge_change_records/` 写记录，至少说明：

- 修改时间。
- 修改目标。
- 修改前问题。
- 涉及数据源、事实、页面、索引或脚本。
- 新增、修改、降级、迁移、删除的具体对象。
- 旧数据如何处理。
- 是否因为规则更新、版本过时、来源冲突、抽取错误或页面过大而修改。
- 修改后解决了什么风险。
- 验证命令和结果。
- 仍然存在的问题。

留痕重点不是“改了什么文件”，而是“为什么这样处理事实”。

变更记录必须包含以下合规声明：

```md
## Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes/no
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes/no
- Source/fact CRUD type:
- Old data handling:
- Coverage/overwrite/delete/downgrade/archive/migration decision:
- High-risk gate impact:
- Runtime manifest impact:
- Gold dataset impact:
```

## 14. 快速决策表

| 场景 | 处理方式 | 是否覆盖旧数据 | 是否删除旧数据 |
| --- | --- | --- | --- |
| 新 A0 法规替代旧法规 | 新建或更新当前来源，旧来源标记 superseded | runtime 使用新版本 | 不删除 |
| 普通网页补充药物剂量 | 作为线索或候选，需 A0/A1 复核 | 不覆盖 | 不删除，可不进 runtime |
| OCR 抽取错误 | 修正事实，记录错误原因 | 覆盖错误摘要 | 保留审计记录 |
| 旧批处理增强块过长 | 迁移到 evidence expansion | runtime 用短占位符 | 不删除 |
| 重复事实 | 合并主表达，其他来源作锚点 | 可合并 | 不静默删除来源 |
| 来源与任务等级不匹配 | 降级 task_use_status | 不覆盖事实 | 不删除 |
| 规则卡新增 | 补页面锚点，更新 hard-block | 不改事实 | 不删除 |
| partial 页面缺口 | 标记 gap-routing | 不补猜测内容 | 不删除 |
| 旧图谱过期 | 脚本重建 | 新导出替代旧导出 | 旧备份由 denylist 排除 |
| pilot 样本缺 provenance | 剔除正式集，记录问题 | 重建样本 | 可删除无效样本输出，但保留报告 |

## 15. 结论

猪病 LLM Wiki 的数据维护必须遵循医学知识库的严谨性：事实不凭经验补全，旧数据不静默覆盖，高风险结论不越过权威来源和规则卡门禁，派生产物不当作事实真源。

新增数据时，先判断来源和任务用途；修改数据时，先判断是事实错误、表达优化、规则更新还是版本替代；删除数据时，优先降级、归档、排除或迁移，只有无引用的临时材料才可直接删除。这样才能保证知识库长期可追溯、可审计、可回归，并能安全支撑猪病问答、评估和黄金数据集生产。
