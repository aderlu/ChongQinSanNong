# 猪病 LLM Wiki 批处理构建执行规范

## 目标

本规范用于指导 `knowledge/llm_wiki_swine_authoritative` 后续所有正式批次构建，确保构建速度提升的同时，保持数据正确性、有效性和来源正确性。

主教材来源：

`docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman,  Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf`

进度文档：

- `docs/SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V2.md`
- `knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress_v2.md`

## 批次范围

- 常规正文批次：每批处理 40-60 PDF pages。
- 表格、图注、参考文献或跨章密集区：可缩小到 20-40 PDF pages。
- 参考文献页、扉页、空白页、目录页只记录边界，默认不生成 standalone facts。
- 下一批起点必须以 `pdf_processing_progress_v2.md` 的“当前已处理至 PDF page”作为准入依据。

## 标准流水线

每个正式批次必须按以下顺序执行：

1. 读取 v2 进度，确认起止页和上一批验证结果。
2. 使用三解析器抽取 PDF 文本：
   - 主解析：PyMuPDF `fitz`
   - 二次核对：`pdfplumber`
   - 三次异常检查：`pypdf`
3. 生成页级抽取文件和解析报告：
   - `issues/formal_batch_XXX_pdf_pages_A_B_extract.txt`
   - `issues/formal_batch_XXX_pdf_pages_A_B_parser_report.txt`
4. 识别章节边界、参考文献页和不得落库内容。
5. 先生成候选事实：
   - `issues/formal_batch_XXX_candidate_facts.json`
6. 生成交叉审查记录：
   - `issues/formal_batch_XXX_cross_review.md`
7. 交叉审查通过后，才允许写入正式库：
   - `exports/knowledge_facts.json`
   - `wiki/sources/`
   - `wiki/topics/`
   - `wiki/rules/`
   - 必要时更新 `wiki/diseases/`
   - 必要时更新 `exports/rule_index.csv`、`exports/source_index.csv`
8. 同步追加两个 v2 进度文档。
9. 运行验证命令并将结果写回两个 v2 文档。

## 每条事实的最低要求

正式落库 facts 必须满足：

- `fact_id` 全库唯一。
- `evidence_source` 为 `Diseases of Swine 11e` 或明确权威来源。
- `evidence_source_id` 指向已存在的 `SRC-XXXX` source 页面。
- `evidence_quote_span` 包含章节名和 PDF page。
- `evidence_status` 为 `HUMAN_REVIEWED`。
- `applies_to_species` 为 `swine`。
- `jurisdiction` 默认使用 `Global`；除非有中国官方或 A0/A1 来源，不得写成 `China`。

## 来源分级

- A0：中国官方法规、农业农村部、国家标准、检疫规程。
- A1：WOAH、FAO、国际标准、同行评议综述。
- A2：权威教材，本 PDF 属于 A2 textbook。
- B：协会或行业指南。
- C：普通网页、博客、非权威材料。

本 PDF 只能支撑全球教材事实和边界。以下内容不得仅凭本 PDF 生成中国本地结论：

- 强制上报、封锁、扑杀、调运、消毒命令。
- 疫苗产品推荐和固定免疫程序。
- 药物剂量、固定治疗处方、休药期。
- 食品召回、人群诊疗、公共卫生执行命令。
- 中国监管、检疫和贸易合规结论。

## 交叉审查要求

每批 `cross_review.md` 必须包含：

- 处理范围和章节边界。
- PDF 解析交叉检查结论。
- 候选事实数量、规则页数量、来源页数量、主题页数量。
- 页码锚点核验。
- 内容边界核验。
- 一致性核验。
- 明确未落库内容。
- 保留问题和下一批入口。

没有通过交叉审查的候选 facts 不得写入正式库。

## 自动验证命令

每批落库后必须运行：

```powershell
$env:PYTHONPATH='src'
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "<本批核心关键词>" --top-k 10
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

验证结果必须同步写入：

- `docs/SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V2.md`
- `knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress_v2.md`

## 完成标准

一个批次只有同时满足以下条件才算完成：

- 页级 PDF 抽取和解析报告存在。
- 候选事实文件存在。
- 交叉审查文件存在。
- 正式 facts、source、topic、rule 页面已同步。
- v2 进度文档已同步。
- `lint ok=True`。
- 查询可以召回本批新增核心内容。
- 图谱已重建。

## 当前入口

截至 Formal Batch 018：

- 已处理至 PDF page 644。
- 下一批从 PDF page 645 开始。
- 推荐下一批：PDF page 645-684，继续 Chapter 38 Parvoviruses 后续正文，并视页码边界进入后续病毒章节。
