# 2026-05-13 DIS-051 猪链球菌病权威网页补强与 wiki-native 主图谱入图

## 修改时间

- 2026-05-13 23:35 +08:00

## 修改目标

- 针对 `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\diseases\DIS-051-streptococcosis-streptococcus-suis.md` 执行一次真实的权威来源搜索、数据补充和受控更新。
- 让本页从“声明存在 evidence gaps 但 `wiki-native` 主图谱 `evidence_units=0`”的状态，进入“具备显式 `fact_id/source_id/anchor` 证据锚点并可生成 verified semantic edges”的状态。

## 修改前存在的问题

- `DIS-051` 页面虽然存在本地教材锚点和 A0 边界来源，但传播途径、临床症状、剖检变化、实验室诊断、鉴别诊断、防控要点仍是显式缺口。
- `issues/wiki_native_graph_build_report.json` 中该页在本次修改前为：
  - `path`: `wiki/diseases/DIS-051-streptococcosis-streptococcus-suis.md`
  - `evidence_units`: `0`
  - `page_gold_ready`: `false`
- 这意味着页面文本还没有按 `wiki-native` 语义构建器要求，写成可被解析的显式锚点格式；图谱层无法把这些事实纳入 verified semantic edges。

## 修改前代码与数据状态

- 疾病页只有 gap 说明，没有真正可入图的显式事实锚点块。
- 项目中已有 `A0-MOA-STREP-SUIS-CONTROL-2005` 和 `A2-GOVUK-STREPTOCOCCUS-SUIS`：
  - 前者偏中国官方疫情防控动态边界；
  - 后者偏英国公共卫生/人畜共患边界；
  - 两者都不适合作为本页传播、临床、病变和实验室诊断事实的主要补强来源。

## 本次新增与修改内容

- 新增来源页：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\sources\A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026.md`
- 新增受控更新脚本：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\apply_dis051_streptococcus_suis_authority_web_refresh.py`
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\apply_dis051_streptococcus_suis_authority_web_refresh.py`
- 更新疾病页：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\diseases\DIS-051-streptococcosis-streptococcus-suis.md`
- 新增证据扩展页：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\evidence_expansions\diseases\phase4_runtime_compaction\DIS-051-streptococcosis-streptococcus-suis\009-Authority-Web-Refresh-2026-05-13.md`
- 更新索引与事实：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\source_index.csv`
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\knowledge_facts.json`

## 进行了什么整理和补充

- 使用已配置的 `web-access` skill 进行了真实联网搜索，并实际打开权威页面。
- 本次主要采用的新增权威来源是：
  - `Merck Veterinary Manual`
  - URL: `https://www.merckvetmanual.com/generalized-conditions/streptococcal-infections-in-pigs/streptococcus-suis-infection-in-pigs`
  - 访问日期：2026-05-13
- 从该页抽取并落库的事实覆盖：
  - 带菌与扁桃体自然生态位
  - 分娩/哺乳/混群相关传播
  - 群间经健康带菌猪调运传播
  - 败血症/脑膜炎/关节炎/猝死等临床模式
  - 早期症状与断奶后易感年龄窗
  - 典型病变
  - 初步诊断与确诊边界
  - 扁桃体/鼻腔检出不能直接定因的实验室解释边界
  - 与格拉瑟氏病、放线杆菌败血症等的鉴别诊断
- 所有写入疾病页的新事实都采用了 `fact_id=...; source_id=...; anchor=...` 的显式格式，以满足 `wiki-native` 主图谱构建器要求。

## 修改后解决了什么问题

- 解决了 `DIS-051` 页面对外看起来“有知识”，但对 `wiki-native` 主图谱来说“没有可用 evidence unit”的问题。
- 解决了来源层级错配的问题：
  - A0 中国动态页继续保留监管与执行边界；
  - A2 Merck 补充疾病事实和实验室解释边界；
  - 不再混用人公共卫生边界来源去填猪病页核心事实。
- 让本次更新能被受控入口、治理审计和图谱差异链路完整追踪。

## 预计产生的更新效果

- `DIS-051` 在 `wiki-native` 图谱里应新增：
  - 来源节点
  - 章节相关 section 节点变化
  - 多条 verified semantic edges
- 页面有望从 `page_gold_ready=false` 转为 `page_gold_ready=true`。
- 更新后的主图谱 HTML 预计会体现该病页传播、临床、诊断与鉴别边的增加。

## 数据更新与执行流程证据

- 真实联网检索与打开的来源包括：
  - Bing 搜索结果页
  - Merck Veterinary Manual `Streptococcus suis Infection in Pigs`
  - GOV.UK 相关页（本轮用于边界核查，未作为猪病核心事实主来源）
- 已按项目治理要求构建受控更新脚本，并准备通过：
  - `tools/create_crud_decision.py`
  - `tools/run_guarded_wiki_update.py`
  执行完整流程。

## Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- Source/fact CRUD type: create source + update disease page + add evidence expansion + append facts
- Old data handling: keep existing A0/A2 boundary sources; additive refresh only
- Coverage/overwrite/delete/downgrade/archive/migration decision: no silent deletion or overwrite of existing authority sources
- High-risk gate impact: disease facts strengthened; executable drug/withdrawal/MRL/regulatory generation remains blocked behind rule cards and A0/A1 sources
- Runtime manifest impact: disease page content updated; downstream manifest/graph rebuild required
- Gold dataset impact: `DIS-051` may become graph-admitted and gold-candidate-ready after rebuild

## UTF-8 与防乱码措施

- 新增和修改文件统一按 UTF-8 写入。
- 受控更新脚本中显式使用 `encoding="utf-8"`。
- CSV 写回继续使用 `utf-8-sig` 以兼容既有工程输出。
- 后续将通过固定入口联动编码审计，防止图谱、日志或中文页面再次出现乱码。
