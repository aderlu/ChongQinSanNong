# A0 农业农村部动物疫病监测计划来源补充执行记录

Date: 2026-05-09 22:42

Target: `ai-/knowledge/llm_wiki_swine_authoritative`

## 1. 修改目标

本次按照以下维护文档执行第一批白名单网页来源补充：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_SUPPLEMENTATION_BLUEPRINT.md`
- `knowledge_change_records/2026-05-09-2115-wiki-maintenance-guide-and-supplementation-blueprint.md`

目标是从 A0 官方来源补充猪病监测、流行病学调查、采样、检测方法和判定边界，并确保：

- 原始网页和附件进入 `raw/`。
- 长证据进入 `wiki/evidence_expansions/`。
- runtime 疾病页只增加短摘要和 source/fact/rule 锚点。
- 不新增药物剂量、疗程、休药期、MRL、残留、食品安全或监管处置越界结论。

## 2. 联网与白名单来源获取情况

本次使用项目可用的 web access skill 进行联网来源发现。CDP 前置检查结果显示：

- Node.js 版本为 v18.20.8，低于建议的 22+。
- Chrome remote debugging 未连接。

因此本次没有操作用户浏览器标签，改用公开网页搜索、网页下载和附件下载方式获取公开 A0 来源。

白名单来源：

- 发布机构：农业农村部
- 来源名称：《国家动物疫病监测与流行病学调查计划（2021—2025年）》
- 文号：农牧发〔2021〕11号
- 政府信息公开页：`https://www.moa.gov.cn/govpublic/xmsyj/202104/t20210425_6366570.htm`
- 农业农村部公报全文页：`https://www.moa.gov.cn/nybgb/2021/202105/202110/t20211021_6380181.htm`
- 附件：`P020210425538815292389.ofd`
- PDF 镜像：`P020250625342607377668.pdf`

## 3. 修改前存在的问题

修改前主要问题：

- 猪病知识库已有较多疾病临床和部分监管来源，但缺少一个统一的 2021—2025 年中国官方动物疫病监测与流行病学调查 A0 锚点。
- 非洲猪瘟、口蹄疫、高致病性猪蓝耳病、猪瘟、猪伪狂犬病、猪流行性腹泻等页面已有临床事实，但对“官方监测对象、采样场景、检测方法、监测阳性/确诊阳性边界、专项调查范围”的当前官方来源补充不足。
- 直接从网页或附件摘录长文本会造成 runtime 页面冗余，因此需要按维护指南分层落位。

## 4. 修改前代码和知识库状态

修改前：

- `wiki/sources/` 中不存在 `A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025.md`。
- `wiki/evidence_expansions/regulatory/` 中不存在该计划的结构化证据扩展。
- `exports/source_index.csv` 中没有该 source_id。
- 以下疾病页未引用该统一监测计划来源：
  - `DIS-002-african-swine-fever-virus.md`
  - `DIS-026-foot-and-mouth-disease-picornaviruses.md`
  - `DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`
  - `DIS-024-classical-swine-fever-pestiviruses.md`
  - `DIS-018-pseudorabies-aujeszky-disease.md`
  - `DIS-008-porcine-epidemic-diarrhea-virus.md`

## 5. 本次新增或更新了什么文件

新增原始来源文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/moa_animal_disease_monitoring_2021_2025_20260509/source_page_2021_notice.html`
- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/moa_animal_disease_monitoring_2021_2025_20260509/source_page_2025_pdf_entry.html`
- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/moa_animal_disease_monitoring_2021_2025_20260509/official_bulletin_full_text.html`
- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/moa_animal_disease_monitoring_2021_2025_20260509/official_bulletin_full_text.txt`
- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/moa_animal_disease_monitoring_2021_2025_20260509/P020210425538815292389.ofd`
- `ai-/knowledge/llm_wiki_swine_authoritative/raw/web/moa_animal_disease_monitoring_2021_2025_20260509/P020250625342607377668.pdf`

新增 source 页：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/sources/A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025.md`

新增 evidence expansion：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/regulatory/moa_animal_disease_monitoring_2021_2025_20260509.md`

更新 runtime 疾病页：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-002-african-swine-fever-virus.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-018-pseudorabies-aujeszky-disease.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`

更新导出索引和派生产物：

- `ai-/knowledge/llm_wiki_swine_authoritative/exports/source_index.csv`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/source_authority_status_index.csv`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts_status_index.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest_summary.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/graph-data.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.html`

## 6. 本次进行了什么整理工作

来源登记：

- 新增 `source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025`。
- 标记 `authority_level=A0`、`source_status=source_anchored`、`fact_validity=valid`。
- 记录官方页面、附件路径、访问日期、发布机构、文号和使用边界。

附件分析：

- 保存官方 OFD 附件原件。
- 保存农业农村部公报 PDF 镜像。
- PDF 为图片型，直接文本抽取信息量有限。
- OFD 为压缩结构，直接文本解析不稳定。
- 使用农业农村部公报全文 HTML 作为结构化事实抽取基础，同时保留 OFD/PDF 作为原始附件证据。

证据扩展：

- 在 `wiki/evidence_expansions/regulatory/` 中整理以下事实组：
  - 总体要求和流行病学调查触发条件。
  - 非洲猪瘟监测计划。
  - 口蹄疫监测计划。
  - 高致病性猪蓝耳病监测计划。
  - 猪瘟监测计划。
  - 主要家畜疫病专项调查方案。

runtime 页面短摘要：

- 非洲猪瘟页补充监测对象、重点猪群、PCR/实时 PCR 阳性与省级确诊边界。
- 口蹄疫页补充偶蹄动物监测对象、类似症状报告触发、猪颌下淋巴结/扁桃体 RT-PCR 检测边界。
- PRRS 页补充重点监测场景、采样组织、RT-PCR/ELISA、疫苗免疫阳性排除边界。
- 猪瘟页补充重点监测场景、疑似病料、RT-nPCR/实时 RT-PCR/免疫荧光抗体试验、国家参考实验室确认边界。
- 猪伪狂犬病和猪流行性腹泻页补充主要家畜疫病专项调查中的官方流调/采样边界。

## 7. 修改后解决了什么问题

修改后：

- 知识库新增 1 个中国官方 A0 监测/流调来源，source 总数从 219 增加到 220。
- 6 个重点猪病页面获得统一官方监测计划锚点。
- 监测阳性、确诊阳性、采样场景、检测方法、流调范围等事实有了 source_id/fact_id/anchor。
- 长文本没有进入 runtime 页面，符合维护指南中 compact runtime 和 evidence expansion 分层要求。
- 新增内容没有引入用药、剂量、休药期、MRL、残留、食品安全或监管处置越界结论。

## 8. 预计更新效果

对生成：

- 可更稳定回答“哪些场景应监测、采什么样本、用什么检测方法、阳性结果如何边界化解释”。
- 避免把 PCR 阳性直接外推成完整处置结论。

对评估：

- 可构造诊断检测解释、监测阳性/确诊阳性区分、单次检测过度外推等评估样本。

对黄金数据集：

- 新增 A0 监测事实可作为 eval、limited、negative trap 和部分低风险训练样本来源。
- 每条事实保留 `fact_id=MOA-MONITOR-*` 和 source anchor，便于后续升级到 fact 级溯源样本。

对检索和图谱：

- 疾病页可以通过 source_id 关联到统一 A0 监测计划来源。
- 图谱和索引已重建，source_index rows=220，missing_index_paths=0。

## 9. 验证命令和结果

所有命令均在 PowerShell 下设置 UTF-8 后执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

重建 runtime manifest：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
```

结果：

- entries: 204
- missing_paths: 0

标准化 source/fact 状态：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\standardize_source_fact_status.py
```

结果：

- source_rows: 220
- source_pages_changed: 0
- source_missing: 0
- facts: 2193
- invalid_facts: 0

重建索引、图谱和检索 smoke test：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase9_rebuild_indexes_graph_smoke.py
```

结果：

- source_index.csv rows: 220
- missing_index_paths: 0
- graph nodes: 2550
- graph links: 3127
- facts_in_graph: 2193
- smoke_test passed: true

readiness 审计：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- readiness_score: 99
- sources: 220
- missing_paths: 0
- bad_fact_tables: []
- missing_rule_cards: []
- missing_synthesis: []

幻觉风险审计：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
```

结果：

- entries_checked: 204
- high: 0
- medium: 0

编码审计：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

结果：

- text_files_scanned: 2318
- encoding_ok: 2306
- decode_or_replacement_damage: 3
- mojibake_like_content: 0
- minor_mojibake_signal: 9
- runtime_damaged_count: 0

猪病 runtime pytest：

```powershell
python -m pytest .\ai-\tests\test_swine_llm_wiki_runtime.py -q
```

结果：

- 8 passed

## 10. 仍然存在的问题和下一步

仍然存在：

- PDF 附件为图片型，直接文本抽取有限；后续如需页码级逐页证据，可引入 OCR 流程。
- OFD 附件已经保存，但直接解析文本不稳定；本次以官方公报全文 HTML 作为结构化事实基础。
- 本批只补充 1 个 A0 监测计划来源，尚未覆盖兽药标签、MRL、禁停用药和更多当前年度应急方案。
- 新增事实还没有写入 `knowledge_facts_status_index.json` 作为独立 fact 表记录，目前以 evidence expansion 和 runtime 页面 `fact_id` 锚点形式存在。

下一步建议：

- 第二批优先补 A1 兽药标签/说明书来源，用于药物页和休药期/MRL 边界。
- 第三批补当前有效的病种专项应急方案和防治技术规范，重点是非洲猪瘟、口蹄疫、猪瘟、PRRS。
- 后续黄金数据集导出时，将 `MOA-MONITOR-*` fact_id 纳入样本 provenance。
