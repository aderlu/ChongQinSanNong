# 猪病 LLM Wiki 知识库维护指南

本文档是后续维护 `llm_wiki_swine_authoritative` 的强制准入规则。任何来自网页搜索、本地 Markdown/PDF/Word/Excel 文档、批量抽取、人工整理、脚本生成或评估反馈的信息，都必须先按本指南和 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 判断是否可进入知识库、进入哪个层级、如何去重、如何溯源、如何验收。

强制适用范围：

- 新增、修改、删除、迁移或归档任何 source、fact、runtime 页面、evidence expansion、rule card、synthesis 页面、导出索引、图谱或黄金数据集样本。
- 从网页获取来源或事实。
- 从本地 `.md`、PDF、Word、Excel、扫描件、教材、标准、标签资料中抽取来源或事实。
- 运行脚本批量生成、增强、压缩、迁移或重建知识库内容。
- 根据评估反馈、人工审校或规则更新调整已有数据。

强制执行顺序：

1. 先阅读 `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`。
2. 再阅读 `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`。
3. 再按需查阅本文档和 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 的具体章节。
4. 再使用 `SOURCE_BATCH_INTAKE_CHECKLIST.md` 做执行前检查。
5. 所有更新命令通过 `tools/run_guarded_wiki_update.py` 固定入口执行。
6. 修改完成后必须在 `knowledge_change_records/` 记录结果。

如果实际操作与这两份规则冲突，必须停止修改；只有在变更记录中明确说明例外原因、风险、临时范围和补救计划后，才允许保留临时例外。

维护目标是：保持知识库清晰、简洁、可追溯、可审计、可用于生成和评估，同时避免把原始材料、重复证据、无来源结论和高风险建议直接塞进 runtime 页面。

## 1. 核心原则

1. 知识库采用 source-first 原则。
   - 任何新增事实必须能回到 `source_id`、`fact_id` 或等价证据锚点。
   - 网页信息必须记录 URL、访问日期、发布或更新日期、发布机构和页面标题。
   - 本地文档必须记录文件路径、页码、章节、表格、条款或行号等定位信息。

2. runtime 页面必须保持短、清楚、可检索。
   - `wiki/diseases/`、`wiki/drugs/`、`wiki/syndromes/`、`wiki/comparisons/` 只保留核心摘要、边界、来源锚点和规则卡引用。
   - 大段摘录、批量表格、网页全文、PDF 抽取块、模型整理过程必须放到 `wiki/evidence_expansions/`、`raw/` 或 `issues/`，不得直接进入 runtime 页面。

3. 高风险内容必须先门禁再生成。
   - 剂量、疗程、给药途径、休药期、MRL、残留、食品安全、法定报告、检疫、扑杀、调运、官方处置、兽药标签结论，必须有 A0 官方或标签级等价来源。
   - 没有对应权威来源时，只能写成风险边界、拒答规则、待补证据或 `generation_ready_limited`，不得写成正向操作建议。

4. synthesis 页面不是事实源。
   - `wiki/synthesis/` 只能承载路由、策略、评估、拒答、样本生成边界和综合规则。
   - synthesis 页面不得创造新的疾病事实、药物事实、剂量、休药期、MRL、监管处置或食品安全结论。

5. partial 页面必须明确缺口。
   - `runtime_core_partial`、`partial_source_anchored_page` 或 `generation_ready_limited` 页面只能用于检索、提醒和缺口路由。
   - 不得由模型补全缺失的病原、症状、诊断、药物、监管或风险信息。

## 2. 来源分级与准入

新增来源必须先分级，再决定用途。

| 等级 | 来源类型 | 可支持用途 | 限制 |
| --- | --- | --- | --- |
| A0 | 中国官方法规、农业农村部公告、国家标准、药典/兽药典、官方疫病防控技术规范、官方数据库 | 监管、法定疫病、检疫、扑杀、调运、MRL、禁停用药等高风险结论 | 必须记录时效、辖区和条款 |
| A1 | 兽药标签、产品说明书、批准文号资料、官方注册资料 | 药物适应证、用法边界、禁忌、休药期、标签级事实 | 不得外推到未标注物种、疾病或用途 |
| B | 权威教材、手册、行业指南、WOAH/FAO 等国际机构资料 | 疾病概述、流行病学、临床表现、诊断思路、防控框架 | 不得替代中国当前监管和标签结论 |
| C | 同行评议论文、综述、病例报告 | 研究证据、机制、流行趋势、诊断方法参考 | 单篇研究不得直接转成生产建议 |
| D | 网页科普、新闻、企业资料、模型生成材料、未核验内部材料 | 线索、待核验候选事实、问题发现 | 默认不得进入正向训练样本 |

网页搜索得到的信息默认不高于 C/D 级，除非页面来自明确的官方机构、法规库、标准库、药品标签库或权威国际组织。

## 3. 网页搜索信息维护流程

通过网页搜索补充信息时，必须按以下流程处理：

1. 先判定搜索目的。
   - 补权威法规或标准。
   - 补疾病事实。
   - 补药物标签。
   - 补诊断、流行病学或鉴别诊断。
   - 补评估规则或负样本陷阱。

2. 记录搜索来源。
   - 查询词。
   - 搜索日期。
   - 页面 URL。
   - 页面标题。
   - 发布机构。
   - 发布日期或更新时间。
   - 访问日期。
   - 是否为官方/标签/教材/论文/网页线索。

3. 不直接复制网页全文到 runtime 页面。
   - 原始网页材料或摘录放入 `raw/` 或 `wiki/evidence_expansions/`。
   - runtime 页面只写 3 到 8 行以内的 source-routed 摘要。

4. 必须进行去重。
   - 先检索 `wiki/sources/` 是否已有同一来源。
   - 再检索 disease/drug/syndrome/comparison 页面是否已有同一事实。
   - 同一事实只能保留一个主表达，其他来源作为 evidence anchors 合并。

5. 高风险网页信息不得直接进入正向结论。
   - 非官方网页提到剂量、疗程、休药期、MRL、残留或监管措施时，只能作为线索。
   - 需要 A0/A1 来源复核后，才能进入生产或训练用途。

6. 必须执行 CRUD 判断。
   - 新网页来源是否新建 source，按 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 第 4 节执行。
   - 与旧来源冲突时，按第 8、9 节处理，不得用网页内容静默覆盖旧权威来源。
   - 如果只是补充已有事实，不新增 runtime 正文，只补 evidence anchor 或 evidence expansion。

## 4. 本地权威文档维护流程

从本地 Markdown、PDF、Word、Excel、扫描件、教材、标准或标签资料补充信息时，必须按以下流程处理：

1. 注册来源。
   - 在 `wiki/sources/` 或对应来源索引中登记 `source_id`。
   - 记录文件路径、标题、机构、版本、日期、语言、辖区、来源等级。

2. 保留证据定位。
   - PDF 使用页码、章节、表号、图号或条款。
   - Excel 使用文件名、工作表名、行号、列名。
   - Word 使用章节标题、页码或段落锚点。
   - 扫描件必须标记 OCR 可靠性。

3. 分层落位。
   - 原始文件保留在 `raw/` 或项目指定来源目录。
   - 抽取表、长摘录、批量事实放入 `wiki/evidence_expansions/`。
   - runtime 页面只保留结论摘要和来源锚点。

4. 不允许无定位摘录。
   - 无页码、无表号、无 URL、无章节定位的事实，最多进入候选层。
   - 候选层事实必须标记 `fact_validity=insufficient_anchor` 或等价状态。

5. 本地 `.md` 文档不能因为已经在仓库内就默认可信。
   - 必须追溯该 Markdown 的原始来源、生成时间、作者或脚本、是否为历史批处理产物。
   - 如果 Markdown 是旧批处理、旧导出、历史 issue 或模型生成材料，只能作为线索或 evidence expansion，不得直接当成权威 source。
   - 如果 Markdown 引用了外部来源，必须回到外部来源或原始文件核验关键事实。

## 5. 去重与落位规则

新增信息前必须回答三个问题：是否已有、是否权威、是否应该进 runtime。

| 信息类型 | 首选落位 | runtime 是否收录 | 说明 |
| --- | --- | --- | --- |
| 原始 PDF、网页全文、Excel 原表 | `raw/` | 否 | 只作证据底座 |
| 大段抽取事实、批量表格 | `wiki/evidence_expansions/` | 否 | 供审计和证据扩展 |
| 疾病核心身份、病原、宿主、临床表现 | `wiki/diseases/` | 是，短摘要 | 必须有来源锚点 |
| 药物标签、禁忌、风险边界 | `wiki/drugs/` | 是，短摘要 | 高风险结论需 A1/A0 |
| 鉴别诊断矩阵 | `wiki/comparisons/` | 是，短摘要 | 避免大表直接进 runtime |
| 症候群路由 | `wiki/syndromes/` | 是，短摘要 | 用于召回和分诊 |
| 规则、拒答、评估标准 | `wiki/rule_cards/` 或 `wiki/synthesis/` | 是 | 规则卡要短且稳定 |
| 审计报告、问题清单、试生产报告 | `issues/` | 否 | 不进入默认检索 |

去重要求：

1. 同一来源不得重复注册多个 `source_id`，除非是不同版本。
2. 同一事实不得在多个 runtime 页面中长篇重复。
3. 跨页面复用事实时，使用链接、source anchor 或 comparison/syndrome 页面承接。
4. 新增信息如果只是证明已有事实，不新增正文，只补来源锚点或 evidence expansion。

旧数据处理要求：

1. 旧来源、旧事实、旧批处理块、旧索引和旧图谱的处理必须遵守 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 第 7、8、9 节。
2. 默认不静默删除已注册来源、已引用事实或已进入 runtime manifest 的页面。
3. 因规则更新或版本过时导致的数据调整，应优先采用降级、归档、迁移、标记 `obsolete_or_superseded`、移出 runtime 或加入 denylist，而不是直接覆盖或删除。

## 6. runtime 页面写作规范

runtime 页面应优先包含：

1. 页面身份：疾病、药物、症候或对比对象。
2. 适用范围：猪种、年龄阶段、生产场景、辖区或任务用途。
3. 核心事实：短句、分点、不过度展开。
4. 证据锚点：source_id、fact_id、页码、条款或 URL。
5. 规则卡锚点：诊断、药物、监管、休药期、MRL、引用门禁。
6. 缺口说明：哪些信息不能生成、需要进一步核验。

runtime 页面不应包含：

1. 原始文档长摘录。
2. 多页表格。
3. 大量候选事实。
4. 无来源经验性判断。
5. 未经 A0/A1 支持的剂量、休药期、MRL、食品安全或监管结论。

页面大小建议：

1. 超过 20 KB：必须检查是否可迁移到 evidence expansion。
2. 超过 50 KB：默认视为过大，不应作为常规 runtime 页面。
3. 单页超过 5 个 `candidate_fact` 或同类候选块：应迁移或拆分。

## 7. 规则卡与高风险门禁

新增或修改以下内容时，必须检查规则卡：

| 内容 | 必要规则 |
| --- | --- |
| 诊断、检测解释、PCR/Ct 值、阳性结果解释 | `RC-DX-001` |
| 法定报告、检疫、扑杀、封锁、调运、官方处置 | `RC-DISEASE-REGULATORY-001`、`RC-REGULATORY-CURRENT-001` |
| 药物、处方、剂量、疗程、给药途径、配伍、禁忌 | `RC-DRUG-001` |
| 休药期、MRL、残留、肉品可食、食品安全 | `RC-WITHDRAWAL-MRL-001` |
| 来源引用和事实锚定 | `RC-CITATION-001` |
| 综合页、样本生成上下文、评估说明 | `RC-SYNTHESIS-SCOPE-001`、`RC-EVAL-RUBRIC-001` |
| partial 页面和缺口路由 | `RC-PARTIAL-GAP-ROUTING-001` |

如果新增内容触发高风险规则，但缺少来源或规则卡锚点，必须阻断进入生产和训练用途。

## 8. 黄金数据集维护要求

知识库补充必须服务于黄金数据集生产，但不能为了生成样本牺牲溯源和边界。

进入训练或评估样本前，页面或事实应具备：

1. `source_status=source_anchored` 或等价状态。
2. `fact_validity=valid` 或明确可用状态。
3. 与任务匹配的 `authority_level`。
4. 明确 `risk_class`。
5. 明确 `task_use_status`。
6. source/rule provenance 完整。
7. 高风险内容具备 A0/A1 来源。

样本生产时必须保留：

1. `sample_id`。
2. `page_id` 或实体 ID。
3. `source_ids`。
4. `fact_ids` 或 evidence anchors。
5. `rule_card_ids`。
6. `task_type`。
7. `allowed_claim_scope`。
8. `blocked_claim_scope`。

没有 fact 级锚点的样本，只能作为 pilot、评估、负样本或待复核样本，不建议直接进入正式微调训练集。

## 9. 必跑验收命令

每次新增来源、整理 runtime 页面、修改规则卡、更新图谱或生成样本后，必须运行验收。

推荐使用一键验收命令：

如果有具体更新命令，必须使用固定入口：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'

python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python <你的更新脚本或命令>
```

如果只是做全量验收而不执行更新命令，可运行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'

python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

该命令会依次执行治理预检、runtime manifest 重建、幻觉风险审计、readiness 审计、编码审计和猪病 runtime pytest。
同时会重建 runtime graph/HTML，生成图谱变化 diff、CRUD 追加日志和图谱变化 HTML 页面。

如需分步排查，可运行：

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

必要验收标准：

1. `runtime_core_manifest.json` 可成功重建。
2. `missing_paths` 为 0。
3. hallucination high-risk 为 0。
4. medium-risk 为 0，或在修改记录中解释临时例外。
5. readiness score 不低于当前基线。
6. runtime damaged count 为 0。
7. 不新增无边界的大 runtime 页面。
8. 不新增无来源的高风险结论。
9. governance compliance preflight 通过。

## 10. 修改留痕要求

每次维护必须在根目录 `knowledge_change_records/` 下新增修改说明文档。说明文档至少包括：

1. 修改时间。
2. 修改目标。
3. 修改前存在的问题。
4. 修改前代码、索引或知识文件状态。
5. 新增或修改了哪些文件。
6. 做了哪些整理、迁移、补充或删除。
7. 修改后解决了什么问题。
8. 预计对生成、评估、检索、黄金数据集的影响。
9. 验证命令和结果。
10. 仍然存在的问题和下一步计划。

还必须说明：

11. 本次是否遵守 `WIKI_MAINTENANCE_GUIDE.md`。
12. 本次是否遵守 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`。
13. 是否处理旧数据；若处理，说明是版本过时、规则更新、事实错误、来源冲突、编码损坏、页面过大还是重复数据。
14. 是否发生覆盖、删除、降级、归档或迁移；若发生，说明理由和追溯位置。

## 11. 编码与乱码防护

维护中文知识库时必须防止乱码：

1. PowerShell 运行前设置 UTF-8，使用本指南第 9 节命令。
2. 读取文件时使用 `-Encoding UTF8`。
3. Python 脚本写文件时显式使用 `encoding="utf-8"`。
4. JSON 输出使用 `ensure_ascii=False`。
5. CSV 输出使用 UTF-8，必要时使用 `utf-8-sig` 供 Excel 查看。
6. 不用未知编码的复制粘贴覆盖 runtime 页面。
7. 修改后运行 `audit_encoding_integrity.py`。

## 12. 禁止事项

禁止：

1. 把网页搜索结果直接写成权威事实。
2. 把原始 PDF、网页全文、Excel 大表直接塞进疾病或药物页。
3. 重复注册同一来源。
4. 重复粘贴同一事实到多个页面。
5. 用 synthesis 页面制造新的医学事实。
6. 用非 A0/A1 来源生成剂量、休药期、MRL、残留合格或监管处置结论。
7. 将 partial 页面当作完整知识页。
8. 跳过 manifest、审计、编码和测试验收。
9. 修改后不写工作留痕。
10. 未阅读或未执行 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 就从网页或本地文档写入来源和事实。
11. 因为本地 Markdown 已存在就直接把其中内容当作权威事实。
12. 因为网页更新日期较新就覆盖 A0/A1 或更高权威等级来源。

## 13. 维护目标形态

本知识库应长期保持以下形态：

```text
raw 原始证据
+ sources 来源注册
+ evidence_expansions 长证据和批量抽取
+ compact runtime pages 简洁运行时页面
+ rule_cards 规则和门禁
+ exports manifest/index/graph
+ issues 审计与问题清单
+ knowledge_change_records 工作留痕
```

只要新增信息都按这个结构落位，知识库就能持续保持高可用、清晰简洁、低冗余，并稳定支撑猪病生成、评估和黄金数据集生产。
