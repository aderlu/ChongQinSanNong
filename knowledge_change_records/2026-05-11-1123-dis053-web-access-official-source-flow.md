# DIS-053 猪结核病 Web Access 官方来源流程记录

## Time

- Updated at: 2026-05-11 11:23:02 +08:00

## Goal

- 针对 `DIS-053 猪结核病`，加载并遵循 `web-access` skill。
- 使用疾病名加 `通知`、`公告`、`技术指南`、`通报`、`实施方案` 等后缀定位权威官方来源。
- 将真实检索到的官方来源整理为 raw evidence JSON。
- 根据真实执行流程修改 `WIKI_UPDATE_POWERSHELL_DEMO.md`，删除旧 ASF/WOAH 演示语境，改为 DIS-053 当前流程说明。

## Before

- `DIS-053-tuberculosis.md` 当前为 partial/gap-routing 页面。
- 项目中没有发现“任意 Web Access raw JSON -> source/fact/runtime 正式入库”的通用现成脚本。
- `web-access` CDP 前置检查真实结果为 Chrome 端口存在但 proxy 连接超时；该失败分支已记录。

## Changes

- 新增 raw evidence:
  - `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/web_access_dis053_tuberculosis_20260511/SRC-DIS053-TB-WEB-20260511.json`
- 修改流程文档:
  - `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`
- 未修改:
  - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-053-tuberculosis.md`
  - `exports/source_index.csv`
  - `exports/knowledge_facts_status_index.json`
  - runtime manifest / graph / gold dataset

## Official Sources Found

- `GB/T 18645-2020 动物结核病诊断技术`
  - URL: `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=05248DA1409774CDD6057CDCF09B3F90`
  - 支持：标准号、现行状态、发布/实施日期、主管/归口部门。
- `中华人民共和国农业农村部公告 第574号：种用动物健康标准`
  - URL: `https://xmsyj.moa.gov.cn/gzdt/202206/t20220629_6403636.htm`
  - 支持：种用动物健康标准适用范围；结核病检测方法引用 `GB/T 18645` 和 `GB/T 27639`。
- `农业农村部关于印发《全国畜间人兽共患病防治规划（2022—2030年）》的通知`
  - URL: `https://app.www.gov.cn/govdata/gov/202209/21/489892/article.html`
  - 支持：官方规划通知和实施背景。
- 农业农村部畜牧兽医局负责人就规划答记者问
  - URL: `https://www.moa.gov.cn/gk/zcjd/202209/t20220926_6411695.htm`
  - 支持：牛结核病规划解读边界；不得外推为猪结核病处置细则。

## Risk Boundary

- 本次来源可作为诊断标准存在性、官方检测方法锚点、种用动物健康标准语境和规划边界的来源。
- 本次未发现可作为猪结核病当前可执行剂量、疗程、休药期或 MRL 的官方来源。
- 不得从牛结核病措施外推猪结核病检疫、扑杀、调运、无害化处理或监管处置细则。
- 不得从标准信息页外推具体检测步骤、样本类型、阈值或确诊结论。

## Validation

- web-access skill file checked: yes
- CDP preflight: attempted; proxy connection timed out, recorded as real execution branch
- Official-source web retrieval: completed through live official-domain search/open
- raw JSON created: yes
- Runtime page modified: no
- Source/fact index modified: no
- dry-run: not executed for DIS-053 because no existing official DIS-053 raw JSON ingestion script was found
- guarded update: not executed for DIS-053 content ingestion
- postcheck: should be run after this documentation/raw evidence change if the repository policy requires full validation

## Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- governance_compliance: this record includes the required Governance Compliance section
- maintenance_guide: checked before changing the flow document
- crud_governance: source/fact CRUD decision recorded; raw evidence only
- scenario_short_card: checked as required pre-update guidance
- guarded_entrypoint: no DIS-053 content ingestion was run because no existing guarded entrypoint script covers this raw Web Access JSON; any future promotion must use `tools/run_guarded_wiki_update.py`
- Source/fact CRUD type: add raw evidence; modify process documentation; no runtime fact promotion
- old_data: existing DIS-053 runtime page and existing source/fact indexes retained unchanged
- Coverage/overwrite/delete/downgrade/archive/migration decision: no overwrite, no delete, no downgrade, no migration
- High-risk gate impact: reinforces blocking of treatment, drug, dose, course, withdrawal period, MRL, food safety, and regulatory extrapolation
- runtime_manifest: no runtime manifest change
- gold_dataset: no gold dataset change
