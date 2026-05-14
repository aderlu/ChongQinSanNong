# DIS-050 Web Access 权威来源补充与图谱更新留痕

## 1. 修改目标

本次更新针对 `DIS-050 猪葡萄球菌病/渗出性表皮炎` 补充权威网页来源和对应事实锚点。目标是使用 Codex 已配置的 Web Access skill 进入 Merck Veterinary Manual 权威兽医手册页面，提取可核验数据，登记 source、fact 和疾病页 runtime 锚点，并通过固定入口自动执行治理预检和完整验收，使知识图谱产生可追踪变化。

## 2. 修改前存在的问题

- `DIS-050` 主要依赖本地教材和本地资料来源，页面仍列出传播/风险、临床症状、剖检变化、实验室诊断、鉴别诊断和防控要点等 evidence gaps。
- 虽然已有教材事实锚点，但缺少可演示“网页权威来源获取 -> source/fact 入库 -> 图谱变化”的外部权威网页节点。
- 页面包含治疗候选相关内容，如果缺少边界，LLM 容易把抗菌药信息外推成处方、剂量、疗程、休药期、MRL 或食品安全结论。

## 3. 修改前代码和数据状态

- 疾病页：`ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-050-staphylococcosis-exudative-epidermitis.md`
- 既有来源：`SRC-0001`、`SRC-0074`、`SRC-0089`、`SRC-0090`
- 既有固定入口：`ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py`
- 既有治理依据：
  - `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
  - `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
  - `WIKI_MAINTENANCE_GUIDE.md`
  - `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

## 4. 本次新增或更新内容

### 新增原始 Web Access 证据

- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/web_access_dis050_exudative_epidermitis_20260511/SRC-DIS050-EE-WEB-20260511.json`

该 JSON 保存从 Merck Veterinary Manual 页面提取的来源信息、支持事实和不得外推边界。

### 新增入库脚本

- `ai-/knowledge/llm_wiki_swine_authoritative/scripts/ingest_dis050_exudative_epidermitis_web_access_20260511.py`

脚本逻辑：

- 校验 raw JSON 必填字段、疾病编号、source_id 和权威域名。
- 登记 `A2-MERCK-EXUDATIVE-EPIDERMITIS-PIGS-2026` source 页面。
- 更新 `exports/source_index.csv`。
- 向 `exports/knowledge_facts.json` upsert 7 条 source-anchored facts。
- 更新 `DIS-050` 疾病页的 sources 和 Web Access 入库说明。
- 调用 `standardize_source_fact_status.py` 生成事实状态。

## 5. CRUD 类型

- Create：新增 raw Web Access JSON、新增 Merck source 页面、新增 7 条事实节点。
- Update：更新 `DIS-050` 疾病页、`source_index.csv`、`knowledge_facts.json`、`knowledge_facts_status_index.json`。
- Query：通过 Web Access 查询 Merck Veterinary Manual 权威网页。
- Delete：本次不删除旧数据。

## 6. Old data 旧数据处理

- 旧教材和本地资料来源 `SRC-0001`、`SRC-0074`、`SRC-0089`、`SRC-0090` 保留，不覆盖、不删除。
- 新 Merck 来源仅作为额外权威网页锚点加入，补充 runtime 可解释性。
- 对旧事实不做替换，避免因单一网页来源覆盖教材证据。
- 如果后续发现更高等级或更新法域来源，应按 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 将旧来源标记为历史、补充或降级，而不是静默删除。

## 7. High-risk 高风险边界

本次涉及诊断和抗菌药治疗边界，属于 diagnostic / drug_boundary 风险域。处理方式：

- 只记录 Merck 明确支持的临床、诊断、鉴别和治疗边界事实。
- 不把抗菌药示例外推为可执行处方、剂量、给药途径、疗程、休药期、MRL、残留或食品安全结论。
- 不外推为中国法域的监管、检疫、调运、报告或处置结论。
- 运行时必须继续联动 `RC-DX-001`、`RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-CITATION-001`。

## 8. Governance Compliance

本次更新遵守：

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- 固定入口 `run_guarded_wiki_update.py`

正式执行必须使用：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python knowledge/llm_wiki_swine_authoritative/scripts/ingest_dis050_exudative_epidermitis_web_access_20260511.py
```

## 9. Runtime manifest 影响

更新后固定入口会自动执行 `run_swine_wiki_maintenance_checks.py`，其中包括：

- `build_runtime_core_manifest.py`
- `phase9_rebuild_indexes_graph_smoke.py`
- `audit_graph_change_diff.py`

预计 `runtime_core_manifest` 会重新生成，`DIS-050` 的 source_ids 将包含 `A2-MERCK-EXUDATIVE-EPIDERMITIS-PIGS-2026`。

## 10. Gold dataset 影响

- 本次新增事实可支持 `DIS-050` 的疾病召回、临床识别、诊断边界、鉴别诊断和治疗边界评估。
- 不直接将 `DIS-050` 升级为无边界处方生成任务。
- Gold dataset 仍应把处方、剂量、疗程、给药途径、休药期、MRL、食品安全和法域执行动作作为禁止外推项。

## 11. 预计图谱变化

预计新增：

- `source:A2-MERCK-EXUDATIVE-EPIDERMITIS-PIGS-2026`
- `fact:DIS050-WEB-001-merck-etiology-shyicus`
- `fact:DIS050-WEB-002-merck-age-stage`
- `fact:DIS050-WEB-003-merck-clinical-lesions`
- `fact:DIS050-WEB-004-merck-predisposing-factors`
- `fact:DIS050-WEB-005-merck-diagnosis-culture-boundary`
- `fact:DIS050-WEB-006-merck-differentials`
- `fact:DIS050-WEB-007-merck-antimicrobial-boundary`

预计新增边：

- `disease:DIS-050 -> source:A2-MERCK-EXUDATIVE-EPIDERMITIS-PIGS-2026`
- `disease:DIS-050 -> fact:*`
- `fact:* -> source:A2-MERCK-EXUDATIVE-EPIDERMITIS-PIGS-2026`

## 12. UTF-8 和乱码防护

- 新增 JSON、Python、Markdown 均使用 UTF-8 编码。
- Python 写文件统一使用 `encoding="utf-8"` 和 LF 换行。
- 不对已有中文乱码文本做批量重写，避免扩大编码损伤。
- 通过固定入口的 `audit_encoding_integrity.py` 做更新后检查。
