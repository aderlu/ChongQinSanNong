# 猪病 LLM Wiki 知识库实施文档 V4

## V4 初始化说明

- 初始化时间：2026-05-07 13:35:00 +08:00。
- V4 继承 V3 截至位置：Formal Batch 025，PDF page 924。
- V4 从 Formal Batch 026 开始作为新的增量同步主线，继续使用本地 PDF 解析库 PyMuPDF、pdfplumber、pypdf 进行逐页交叉解析。
- V4 仍执行 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md`：每批优先处理 40-60 页，先生成候选 facts 与交叉审查记录，确认页码锚点、内容边界、来源一致性和落库一致性后再写入正式知识库。
- V4 文档同步范围：本文件与 `knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress_v4.md` 必须随正式落库同步更新；V3 文件保留为历史版本，不再作为后续主线。

## V3 继承状态

- V3 截至批次：Formal Batch 025。
- V3 截至页码：PDF page 924。
- V3 当前事实：`fact_count=1216`，其中 `HUMAN_REVIEWED=1070`、`NEEDS_REVIEW=146`。
- V3 当前来源页：`SRC-0001` 至 `SRC-0071`。
- V3 当前规则页：`RULE-001` 至 `RULE-361`。
- V3 图谱状态：`2686 nodes / 2505 links`。
- 下一批入口：PDF page 925。

## V4 质量边界

- 没有 PDF 章节和页码锚点的事实不得落库。
- 药方、剂量、休药期、监管处置、药检合格承诺、强制检疫、食品召回、公共卫生暴露处置、免疫程序和扑杀等结论必须等待相应章节和 A0/A1 来源复核。
- 教材中的美国法规、公共卫生语境和国际贸易语境不得直接迁移为中国监管答案。
- 每批先写候选事实和交叉审查记录，通过后再合并到 `exports/knowledge_facts.json`。


## Formal Batch 026 / V4 实施记录

- 完成时间：2026-05-07 13:35:00 +08:00。
- 处理范围：PDF page 925-964。
- 章节边界：Chapter 58 Proliferative Enteropathy 正文后段和参考文献；Chapter 59 Salmonellosis 正文和参考文献；Chapter 60 Staphylococcosis 正文和参考文献；Chapter 61 Streptococcosis 开端。
- 参考文献处理：PDF page 932-935、947-949、956-957 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0072` 至 `SRC-0075`。
- 新增主题页：Lawsonia 增生性肠病诊断/防控/用药/疫苗边界、沙门氏菌肠炎型/败血型/诊断/控制边界、葡萄球菌病/渗出性表皮炎/LA-MRSA 边界、S. suis 人兽共患/脑膜炎/败血症开端边界。
- 新增规则页：`RULE-362` 至 `RULE-378`。
- 新增候选事实：`issues/formal_batch_026_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_026_cross_review.md`。
- 正式落库 facts：47 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、Lawsonia 抗菌药/疫苗固定程序和休药期、沙门氏菌食品安全执行/召回/通用处方、S. hyicus 药物方案、LA-MRSA 公共卫生处置、S. suis 人暴露处置、中国监管结论。

### Formal Batch 026 / V4 交叉审查

- 页码锚点核验：通过。`SRC-0072` 覆盖 PDF page 925-935；`SRC-0073` 覆盖 936-949；`SRC-0074` 覆盖 950-957；`SRC-0075` 覆盖 958-964。
- 内容边界核验：通过。Lawsonia/PE、Salmonellosis、Staphylococcosis 和 Streptococcosis 开端均只落库教材证据和诊断/传播/公共卫生/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- 编码复核：通过。Batch 026 候选事实、交叉审查、规则页和索引为 UTF-8，无成串替换问号残留。

## 截至位置更新

- 当前已处理至 PDF page 964。
- 下一批应从 PDF page 965 开始。
- 推荐下一批：PDF page 965-1004，继续 Chapter 61 Streptococcosis 正文，补充 S. suis 诊断、治疗、防控、疫苗和参考文献边界，并视章节边界进入后续细菌病章节。

### Formal Batch 026 / V4 验证结果

- `status`：`fact_count=1263`，`disease_count=73`，`rule_count=378`，`sources=75`，`topics=87`。
- 证据状态：`HUMAN_REVIEWED=1117`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 Lawsonia/增生性肠病 PCR 和血清学边界、沙门氏菌肠炎型/败血型和诊断边界、渗出性表皮炎/LA-MRSA、S. suis 人兽共患/脑膜炎/败血症开端等新增内容。
- `graph-build`：已重建图谱，`2801 nodes / 2599 links`。

## 后续待处理阶段

- PDF page 965-1026：Section IV Bacterial Diseases 后续章节。
- PDF page 1027-1064：Section V Parasitic Diseases。
- PDF page 1065-1111：Section VI Noninfectious Diseases。
- PDF page 1112-1132：Index。


## Formal Batch 027 / V4 实施记录

- 完成时间：2026-05-07 17:10:00 +08:00。
- 处理范围：PDF page 965-1004。
- 章节边界：Chapter 61 Streptococcosis 正文后段和参考文献；Chapter 62 Swine Dysentery and Brachyspiral Colitis 正文和参考文献；Chapter 63 Tuberculosis 正文前中段和参考文献开端。
- 参考文献处理：PDF page 972-974、991-994、1004 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0076` 至 `SRC-0078`。
- 新增主题页：猪链球菌病诊断/用药/疫苗/控制边界、猪痢疾/Brachyspira 诊断/防控/耐药边界、猪结核 MAC/MTBC 诊断和防控边界。
- 新增规则页：`RULE-379` 至 `RULE-396`。
- 新增候选事实：`issues/formal_batch_027_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_027_cross_review.md`。
- 正式落库 facts：42 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、具体处方/剂量/休药期、固定疫苗程序、美国屠宰法规执行细则和中国监管结论。

### Formal Batch 027 / V4 交叉审查

- 页码锚点核验：通过。`SRC-0076` 覆盖 PDF page 965-974；`SRC-0077` 覆盖 975-994；`SRC-0078` 覆盖 995-1004。
- 内容边界核验：通过。S. suis、Brachyspira/猪痢疾和猪结核均只落库教材证据和诊断/传播/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 1004。
- 下一批应从 PDF page 1005 开始。
- 推荐下一批：PDF page 1005-1026，继续 Chapter 63 Tuberculosis 参考文献后段，并视章节边界进入 Section IV 后续细菌病章节。

### Formal Batch 027 / V4 验证结果

- `status`：`fact_count=1311`，`disease_count=73`，`rule_count=396`，`sources=78`，`topics=90`。
- 证据状态：`HUMAN_REVIEWED=1165`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回猪痢疾/Brachyspira 强 β 溶血确诊、防控/耐药边界、S. suis 诊断/疫苗/用药边界、猪结核 MAH 有机垫料/生物膜风险等新增内容。
- `graph-build`：已重建图谱，`2918 nodes / 2695 links`。


## Formal Batch 028 / V4 实施记录

- 完成时间：2026-05-07 18:25:00 +08:00。
- 处理范围：PDF page 1005-1026。
- 章节边界：Chapter 64 Miscellaneous Bacterial Infections 正文和各小节参考文献；PDF page 1026 仅含页脚/空白边界。
- 解析器：PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six`。
- 参考文献处理：各小节参考文献仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0079`。
- 新增主题页：猪杂项细菌感染诊断和定因边界、猪杂项细菌人兽共患和食品安全边界。
- 新增规则页：`RULE-397` 至 `RULE-414`。
- 新增候选事实：`issues/formal_batch_028_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_028_cross_review.md`。
- 正式落库 facts：46 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、具体处方/剂量/休药期、食品召回/执法、公共卫生暴露处置和中国监管结论。

### Formal Batch 028 / V4 交叉审查

- 页码锚点核验：通过。`SRC-0079` 覆盖 PDF page 1005-1026。
- 内容边界核验：通过。Chapter 64 杂项细菌感染均只落库教材证据和诊断/传播/公共卫生/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 1026。
- 下一批应从 PDF page 1027 开始。
- 推荐下一批：PDF page 1027-1064，进入 Section V Parasitic Diseases，处理外寄生虫和寄生虫病章节。

### Formal Batch 028 / V4 验证结果

- `status`：`fact_count=1357`，`disease_count=73`，`rule_count=414`，`sources=79`，`topics=92`。
- 证据状态：`HUMAN_REVIEWED=1211`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 Chapter 64 杂项细菌感染来源页、A. suis 交配后血尿鉴别、炭疽/类鼻疽/衣原体/李斯特菌/Yersinia/R. equi 等新增边界；`A. suis` 缩写同时召回既有 Actinobacillus suis 条目属预期。
- `graph-build`：已重建图谱，`3029 nodes / 2787 links`。


## Formal Batch 029 / V4 实施记录

- 完成时间：2026-05-07 19:10:00 +08:00。
- 处理范围：PDF page 1027-1064。
- 章节边界：Section V Parasitic Diseases 扉页；Chapter 65 External Parasites 正文和参考文献；Chapter 66 Coccidia and Other Protozoa 正文和参考文献；Chapter 67 Internal Parasites 正文前中段和参考文献开端。
- 解析器：PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six`。
- 参考文献处理：PDF page 1037-1038、1050-1051、1064 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0080` 至 `SRC-0082`。
- 新增主题页：猪外寄生虫诊断和防控边界、猪原虫性腹泻和人兽共患边界、猪内寄生虫诊断和防控边界。
- 新增规则页：`RULE-415` 至 `RULE-432`。
- 新增候选事实：`issues/formal_batch_029_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_029_cross_review.md`。
- 正式落库 facts：48 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、具体驱虫/杀虫/抗球虫处方、剂量、疗程、休药期、食品处理执行细则、公共卫生暴露处置和中国监管结论。

### Formal Batch 029 / V4 交叉审查

- 页码锚点核验：通过。`SRC-0080` 覆盖 PDF page 1027-1038；`SRC-0081` 覆盖 1039-1051；`SRC-0082` 覆盖 1052-1064。
- 内容边界核验：通过。Chapter 65-67 只落库教材证据、诊断/传播/生产影响/防控/公共卫生边界，不生成处方、固定程序、休药期或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 1064。
- 下一批应从 PDF page 1065 开始。
- 推荐下一批：PDF page 1065-1111，进入 Section VI Noninfectious Diseases，处理营养缺乏/过量、霉菌毒素和毒物/气体相关章节。

### Formal Batch 029 / V4 验证结果

- `status`：`fact_count=1405`，`disease_count=73`，`rule_count=432`，`sources=82`，`topics=95`。
- 证据状态：`HUMAN_REVIEWED=1259`，`NEEDS_REVIEW=146`。
- `lint`：非 strict `ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。`lint --strict` 仍会按设计阻断这 146 条目录级待复核 facts。
- `query`：可召回猪疥螨刮片假阴性/净化边界、猪虱诊断、仔猪球虫卵囊定因边界、弓形虫猫源卵囊和食品安全边界、Metastrongylus 虫卵不易漂浮、Ascaris milk spots 鉴别、Stephanurus 肾虫等新增内容。
- `graph-build`：已重建图谱，`3125 nodes / 2883 links`。

## System Usable Completion V5 / 执行记录

- 完成时间：2026-05-07 20:30:00 +08:00。
- 依据文档：`docs/SWINE_LLM_WIKI_SYSTEM_USABLE_COMPLETION_PLAN.md`。
- 执行范围：disease 页面 V5 自动回填、A0/A1 权威来源入口、drug evidence pages、rule_cards、syndromes、synthesis。
- 新增权威来源：`A0-MOA-573`、`A0-MOA-ASF-NORMALIZED-GUIDE`、`A0-MOA-BANNED-DRUG-250-POLICY`、`A1-WOAH-ASF`、`A1-WOAH-FMD`。
- 新增 authority facts：18 条 `HUMAN_REVIEWED` facts，均保留 URL 和 jurisdiction。
- 新增 drug 页面：8 个；其中多数为 `evidence_only`，食品动物禁用药清单为 `china_regulated` 来源入口但不编造具体清单。
- 新增 rule_cards：3 个 critical 系统规则卡。
- 新增 syndromes：12 个临床综合征入口。
- 新增 synthesis：8 个系统生成/评估二级页面。
- 新增报告：`issues/v5_001_disease_backfill_report.md`、`issues/v5_001_disease_backfill_candidate_map.json`、`issues/v5_002_authority_candidate_facts.json`、`issues/v5_002_authority_cross_review.md`。
- 质量边界：未能从现有 HUMAN_REVIEWED facts 自动映射的 disease 栏目保留“待抽取/待 A0-A1 补充”，不生成无来源内容。

## Targeted Disease Completion V5 / DIS-003 Anelloviruses

- 完成时间：2026-05-07 20:45:00 +08:00。
- 处理范围：Chapter 26 Anelloviruses，PDF page 478-479。
- 新增来源：`SRC-0083`。
- 新增 facts：12 条 `HUMAN_REVIEWED` facts。
- 更新疾病页：`wiki/diseases/DIS-003-anelloviruses-torque-teno-sus-viruses.md`，补充传播途径、临床症状、剖检变化、实验室诊断、鉴别诊断、防控和公共卫生边界。
- 明确边界：TTSuV 与疾病因果关系尚未清楚建立，单独检出不得定因；不得生成固定免疫/净化/用药程序。
