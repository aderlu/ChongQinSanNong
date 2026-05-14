# 猪病 Wiki 场景化短执行卡

本卡是强制短执行卡，用于帮助 LLM 在具体更新场景中快速选择规则。完整依据仍为 `WIKI_MAINTENANCE_GUIDE.md` 和 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`。

任何使用本卡执行的更新，都必须在 `knowledge_change_records/` 中保留工作留痕，并说明治理合规、旧数据处理、高风险门禁、runtime manifest 和 gold dataset 影响。

## 1. 网页来源

- 官方法规、公告、标准、数据库：可登记为 A0，但必须记录 URL、机构、日期、访问日期、辖区和条款。
- 兽药标签、说明书、注册资料：可登记为 A1，但不得外推到未标注物种、剂型、疾病或用法。
- 普通网页、新闻、企业资料：默认只是 SRC 线索，不能支持高风险正向结论。
- 网页引用了法规、标准、标签或论文时，优先追溯原始来源。

## 2. 本地 Markdown

- 本地 Markdown 不等于权威来源。
- 必须判断它是 source 页、人工审校稿、历史 issue、脚本输出、模型整理稿还是旧批处理产物。
- 旧 issue、脚本输出、模型整理稿默认进入 evidence expansion 或候选层，不直接写 runtime。
- 关键事实尽量回到原始 PDF、网页、表格、标签或 source 页核验。

## 3. 本地 PDF/Word/Excel/扫描件

- 先登记 source。
- 保留页码、章节、表格、行列、条款或 OCR 可靠性。
- 长摘录和批量表格进入 `wiki/evidence_expansions/`。
- runtime 只写短摘要和锚点。

## 4. 旧数据处理

- 旧数据默认不静默删除。
- 新法规/标签替代旧版本：当前 runtime 用新版本，旧版本标记历史或 superseded。
- 抽取错误：修正事实，并在 change record 说明错误原因。
- 页面过大或批处理块过长：迁移到 evidence expansion。
- 来源等级不匹配：降级 `task_use_status`，不要硬写成正向答案。
- 冲突未解决：标记 conflicted，降级为 retrieval_only 或 blocked。

## 5. 高风险内容

以下内容必须检查规则卡和 A0/A1 或标签级来源：

- 药物、剂量、疗程、给药途径、处方。
- 休药期、MRL、残留、屠宰、可食组织、食品安全。
- 上报、扑杀、封锁、检疫、调运、无害化处理。
- PCR、Ct、抗体阳性、抗原阳性直接推出确诊或因果关系。

必要规则卡：

- `RC-DX-001`
- `RC-DRUG-001`
- `RC-WITHDRAWAL-MRL-001`
- `RC-DISEASE-REGULATORY-001`
- `RC-REGULATORY-CURRENT-001`
- `RC-CITATION-001`
- `RC-EVAL-RUBRIC-001`
- `RC-SYNTHESIS-SCOPE-001`
- `RC-PARTIAL-GAP-ROUTING-001`

## 6. 更新后验收

普通维护只需要运行固定入口；入口会自动跑完整验收。

如果只做治理链路检查：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_governance_compliance.py
```

如果需要完整验收但没有更新命令：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

完整验收必须满足：

- governance preflight 通过。
- manifest missing_paths 为 0。
- hallucination high/medium 为 0，或有明确例外。
- readiness 不低于 99。
- runtime damaged count 为 0。
- pytest 通过。
