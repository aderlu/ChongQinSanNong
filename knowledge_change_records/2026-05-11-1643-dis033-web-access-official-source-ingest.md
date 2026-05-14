# DIS-033 Web Access 官方来源补充与图谱更新留痕

## 1. 修改目标

本次更新针对 `DIS-033 猪水疱性口炎` 补充权威网页来源和对应事实锚点。目标是使用 Codex 已配置的 Web Access skill 进入官方来源页面，提取可核验数据，登记 source、fact 和疾病页 runtime 锚点，并通过固定入口自动执行治理预检和完整验收，使知识图谱产生可追踪变化。

## 2. 修改前存在的问题

- `DIS-033` 当前主要依赖教材来源 `SRC-0001`、`SRC-0054`，对官方网页来源的 host range、媒介传播、报告边界和动物调运/贸易影响缺少单独 source/fact 节点。
- 知识图谱虽然已有 `DIS-033`、教材 source、rule card 和部分事实节点，但缺少 USDA APHIS 官方网页节点，无法展示“本次从网页获取来源并驱动图谱变化”的完整链路。
- 高风险监管信息如果没有明确边界，容易被 LLM 外推为中国法域的检疫、扑杀、调运、治疗、剂量、休药期、MRL 或食品安全结论。

## 3. 修改前代码和数据状态

- 疾病页：`ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-033-vesicular-stomatitis-viruses.md`
- 既有来源：`SRC-0001`、`SRC-0054`
- 既有固定入口：`ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py`
- 既有治理依据：
  - `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
  - `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
  - `WIKI_MAINTENANCE_GUIDE.md`
  - `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`

## 4. 本次新增或更新内容

### 新增原始 Web Access 证据

- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/web_access_dis033_vesicular_stomatitis_20260511/SRC-DIS033-VS-WEB-20260511.json`

该 JSON 保存从 USDA APHIS 官方页面提取的来源信息、支持事实和不得外推边界。

### 新增入库脚本

- `ai-/knowledge/llm_wiki_swine_authoritative/scripts/ingest_dis033_vesicular_stomatitis_web_access_20260511.py`

脚本逻辑：

- 校验 raw JSON 必填字段、疾病编号、source_id 和官方域名。
- 登记 `A0-USDA-APHIS-VS-2026` source 页面。
- 更新 `exports/source_index.csv`。
- 向 `exports/knowledge_facts.json` upsert 5 条 source-anchored facts。
- 更新 `DIS-033` 疾病页的 sources 和 Web Access 入库说明。
- 调用 `standardize_source_fact_status.py` 生成事实状态。

## 5. CRUD 类型

- Create：新增 raw Web Access JSON、新增 USDA APHIS source 页面、新增 5 条事实节点。
- Update：更新 `DIS-033` 疾病页、`source_index.csv`、`knowledge_facts.json`、`knowledge_facts_status_index.json`。
- Query：通过 Web Access 查询 USDA APHIS 官方页面。
- Delete：本次不删除旧数据。

## 6. Old data 旧数据处理

- 旧教材来源 `SRC-0001`、`SRC-0054` 保留，不覆盖、不删除。
- 新 APHIS 来源仅作为额外官方网页锚点加入，补充 runtime 可解释性。
- 对旧事实不做替换，避免因单一网页来源覆盖教材证据。
- 如果后续发现更高等级或更新法域来源，应按 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 将旧来源标记为历史、补充或降级，而不是静默删除。

## 7. High-risk 高风险边界

本次涉及报告、动物移动和国际贸易影响，属于 high_regulatory 风险域。处理方式：

- 只记录 APHIS 明确支持的美国官方来源范围。
- 不外推为中国法域的报告、检疫、扑杀、封锁、调运或无害化处理结论。
- 不新增治疗、药物、剂量、疗程、休药期、MRL、残留或食品安全结论。
- 运行时必须继续联动 `RC-DISEASE-REGULATORY-001`、`RC-REGULATORY-CURRENT-001`、`RC-CITATION-001`。

## 8. Governance Compliance

本次更新遵守：

- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- 固定入口 `run_guarded_wiki_update.py`

正式执行必须使用：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python knowledge/llm_wiki_swine_authoritative/scripts/ingest_dis033_vesicular_stomatitis_web_access_20260511.py
```

## 9. Runtime manifest 影响

更新后固定入口会自动执行 `run_swine_wiki_maintenance_checks.py`，其中包括：

- `build_runtime_core_manifest.py`
- `phase9_rebuild_indexes_graph_smoke.py`
- `audit_graph_change_diff.py`

预计 `runtime_core_manifest` 会重新生成，`DIS-033` 的 source_ids 将包含 `A0-USDA-APHIS-VS-2026`。

## 10. Gold dataset 影响

- 本次新增事实可支持 `DIS-033` 的疾病召回、鉴别诊断边界、报告边界和高风险监管边界评估。
- 不直接将 `DIS-033` 升级为无边界生成任务。
- Gold dataset 仍应把治疗、处方、休药期、MRL、食品安全和法域执行动作作为禁止外推项。

## 11. 预计图谱变化

预计新增：

- `source:A0-USDA-APHIS-VS-2026`
- `fact:DIS033-WEB-001-aphis-swine-host-boundary`
- `fact:DIS033-WEB-002-aphis-vector-transmission`
- `fact:DIS033-WEB-003-aphis-lesion-sites`
- `fact:DIS033-WEB-004-aphis-us-reporting-boundary`
- `fact:DIS033-WEB-005-aphis-movement-trade-impact`

预计新增边：

- `disease:DIS-033 -> source:A0-USDA-APHIS-VS-2026`
- `disease:DIS-033 -> fact:*`
- `fact:* -> source:A0-USDA-APHIS-VS-2026`

## 12. UTF-8 和乱码防护

- 新增 JSON、Python、Markdown 均使用 UTF-8 编码。
- Python 写文件统一使用 `encoding="utf-8"` 和 LF 换行。
- 不对已有中文乱码文本做批量重写，避免扩大编码损伤。
- 通过固定入口的 `audit_encoding_integrity.py` 做更新后检查。
