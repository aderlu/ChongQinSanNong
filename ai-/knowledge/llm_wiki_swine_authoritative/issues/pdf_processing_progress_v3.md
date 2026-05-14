# Diseases of Swine PDF 分批处理进度 V3

## V3 初始化说明

- 初始化时间：2026-05-07 09:20:00 +08:00。
- V3 继承 V2 截至位置：Formal Batch 020，PDF page 724。
- V3 从 Formal Batch 021 开始记录新的正式构建批次。
- V3 继续使用本地 PDF 解析库 PyMuPDF、pdfplumber、pypdf 进行交叉解析，并按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行候选 facts、交叉审查、正式落库、验证和文档同步。
- V2 文档保留为历史记录，后续增量同步以 V3 文档为准。

---
# Diseases of Swine PDF 分批处理进度 V2

## 更新时间

- V2 初始化时间：2026-05-06。
- V2 继承 V1 截至位置：Formal Batch 007，PDF page 220。
- Formal Batch 008 完成时间：2026-05-06 18:06:12 +08:00。
- Formal Batch 009 完成时间：2026-05-06 19:28:50 +08:00。
- Formal Batch 010 完成时间：2026-05-06 20:35:00 +08:00。
- Formal Batch 015 完成时间：2026-05-06 23:59:00 +08:00。
- Formal Batch 014 完成时间：2026-05-06 23:35:00 +08:00。
- Formal Batch 013 完成时间：2026-05-06 23:25:00 +08:00。
- Formal Batch 012 完成时间：2026-05-06 22:35:00 +08:00。
- Formal Batch 011 完成时间：2026-05-06 21:42:00 +08:00。

## 当前状态

- PDF 总页数：1132。
- 文件：`docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman, Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf`
- V1 已完成批次：Batch 0 至 Formal Batch 007，PDF page 1-220。
- V2 已完成批次：
  - Formal Batch 008：PDF page 221-244，Chapter 12 和 Chapter 13 正式构建。
  - Formal Batch 009：PDF page 245-284，Section II 起始、Chapter 14 和 Chapter 15 前段正式构建。
  - Formal Batch 010：PDF page 285-324，Chapter 16 Immune System 与 Chapter 17 Integumentary System 前段正式构建。
- 当前正式落库：
  - `SRC-0001` 至 `SRC-0019`。
  - `RULE-001` 至 `RULE-113`。
  - `issues/formal_batch_001_candidate_facts.json` 至 `issues/formal_batch_010_candidate_facts.json`。
  - `issues/formal_batch_001_cross_review.md` 至 `issues/formal_batch_010_cross_review.md`。
  - `exports/knowledge_facts.json` 当前共 487 条 facts，其中 341 条为 `HUMAN_REVIEWED` 正式事实，146 条目录级 facts 保持 `NEEDS_REVIEW`。

## Formal Batch 008 实施记录

- 完成时间：2026-05-06 18:06:12 +08:00。
- 处理范围：PDF page 221-244。
- 章节：Chapter 12 Preharvest Food Safety, Zoonotic Diseases, and the Human Health Interface；Chapter 13 Special Considerations for Show and Pet Pigs。
- 新增来源：`SRC-0014`、`SRC-0015`。
- 新增主题页：
  - `wiki/topics/Swine-preharvest-food-safety-zoonotic-human-health.md`
  - `wiki/topics/Swine-show-pig-health-biosecurity-and-ethics.md`
  - `wiki/topics/Swine-pet-pig-care-behavior-and-drug-boundaries.md`
- 新增规则页：`RULE-071` 至 `RULE-085`。
- 新增候选事实：`issues/formal_batch_008_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_008_cross_review.md`。
- 正式落库 facts：48 条 `HUMAN_REVIEWED` facts。
- 所有正式 facts 均锚定 `SRC-0014` 或 `SRC-0015` 及具体 PDF page。
- 明确未落库：具体休药期、药检阈值、召回方案、强制检疫处置、展会合格承诺、具体疫苗/驱虫/用药剂量、手术步骤、中国监管结论。

### Formal Batch 008 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖食品安全危害分类、残留边界、人兽共患风险、抗菌药耐药解释、展览猪/宠物猪特殊管理边界。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。
- 编码复核：通过。新增 batch 008 中文内容已确认可被 query 正常召回。

### Formal Batch 008 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪肉 食品安全 沙门氏菌 休药期 展览猪 药检 宠物猪 约束" --top-k 8
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=405`，`disease_count=73`，`rule_count=85`。
- 证据状态：`HUMAN_REVIEWED=259`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回食品安全危害分类、沙门氏菌屠前控制、休药期边界、展览猪药检、展览猪生物安全、宠物猪约束和宠物猪用药边界。
- `graph-build`：已重建图谱，`733 nodes / 883 links`。

## 截至位置更新

- 当前已处理至 PDF page 244。
- 下一次应从 PDF page 245 开始。
- 推荐下一批：PDF page 245-284，进入 Section II Body Systems，优先处理 Chapter 14 Diseases of the Cardiovascular System 与相邻系统章节开端。

## Formal Batch 009 实施记录

- 一次处理可行性判断：PDF page 245-448 共 204 页，覆盖 Section II Body Systems 多个系统章节，不适合一次处理；本轮拆分处理 PDF page 245-284。
- 完成时间：2026-05-06 19:28:50 +08:00。
- 处理范围：PDF page 245-284。
- 章节：Section II Body Systems 起始页；Chapter 14 Cardiovascular and Hematopoietic Systems；Chapter 15 Digestive System 正文至参考文献页开端。
- 新增来源：`SRC-0016`、`SRC-0017`。
- 新增主题页：
  - `wiki/topics/Swine-cardiovascular-hematopoietic-system-navigation.md`
  - `wiki/topics/Swine-digestive-system-and-diarrhea-navigation.md`
  - `wiki/topics/Swine-system-based-necropsy-and-clinical-pathology-boundaries.md`
- 新增规则页：`RULE-086` 至 `RULE-099`。
  - `issues/formal_batch_001_candidate_facts.json` 至 `issues/formal_batch_010_candidate_facts.json`。
  - `issues/formal_batch_001_cross_review.md` 至 `issues/formal_batch_010_cross_review.md`。
- 正式落库 facts：34 条 `HUMAN_REVIEWED` facts。
- 所有正式 facts 均锚定 `SRC-0016` 或 `SRC-0017` 及具体 PDF page。
- 明确未落库：具体处方、补液方案、抗菌药方案、手术方案、补硒/维生素方案、中国监管结论。

### Formal Batch 009 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖心血管/造血系统导航、心脏剖检、临床病理解释、消化系统、胃溃疡、腹泻机制和鉴别诊断边界。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。
- 编码复核：通过。新增 batch 009 中文内容已确认可被 query 正常召回。
- 二次严格验证：2026-05-06 复核后确认 PDF page 245-284 已处理完成；`DIG-016` 页码锚点由 `PDF page 280` 收紧为 `PDF page 280-281`，并同步更新候选事实、正式 facts、交叉审查记录和图谱派生数据。

### Formal Batch 009 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "心血管 造血 心脏剖检 桑葚心 胃溃疡 腹泻 新生仔猪 鉴别" --top-k 8
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=439`，`disease_count=73`，`rule_count=99`。
- 证据状态：`HUMAN_REVIEWED=293`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回心血管与造血系统导航、心脏剖检、桑葚心病确认、胃溃疡解释、新生仔猪腹泻和腹泻机制鉴别等新增内容。
- `graph-build`：已重建图谱，`817 nodes / 951 links`。

## 截至位置更新

- 当前已处理至 PDF page 284。
- 下一次应从 PDF page 285 开始。
- 推荐下一批：PDF page 285-324，继续 Section II Body Systems 后续系统章节。

## Formal Batch 010 实施记录

- 完成时间：2026-05-06 20:35:00 +08:00。
- 处理范围：PDF page 285-324。
- 章节边界：PDF page 285-287 为 Chapter 15 参考文献尾页，不生成新事实；PDF page 288-312 为 Chapter 16 Immune System 正文至参考文献开端；PDF page 313-315 为 Chapter 16 参考文献页；PDF page 316-324 为 Chapter 17 Integumentary System: Skin, Hoof, and Claw 前段。
- 新增来源：`SRC-0018`、`SRC-0019`。
- 新增主题页：
  - `wiki/topics/Swine-immune-system-and-vaccination-boundaries.md`
  - `wiki/topics/Swine-neonatal-and-mucosal-immunity.md`
  - `wiki/topics/Swine-integumentary-lesion-differential-and-sampling.md`
- 新增规则页：`RULE-100` 至 `RULE-113`。
- 新增候选事实：`issues/formal_batch_010_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_010_cross_review.md`。
- 正式落库 facts：48 条 `HUMAN_REVIEWED` facts。
- 明确未落库：参考文献列表、具体疫苗免疫程序、攻毒/返饲操作方案、佐剂配方、药物剂量、抗菌药治疗方案、手术/采样麻醉细节、中国监管结论。

### Formal Batch 010 交叉审查

- 页码锚点核验：通过。`SRC-0018` 事实锚定 PDF page 288-312，`SRC-0019` 事实锚定 PDF page 316-324。
- 内容边界核验：通过。参考文献页只作为章节边界，不单独生成事实；Chapter 16 仅抽取免疫机制、黏膜/新生仔猪免疫、疫苗失败边界和免疫管理原则；Chapter 17 仅抽取皮肤功能、病史/病变鉴别、采样和早期皮肤病边界。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。
- 编码复核：通过。新增 batch 010 文件为 UTF-8，无替换字符。
- 二次严格验证：2026-05-06 复核后确认 PDF page 285-324 已处理完成；48 条候选事实与正式 facts 逐字段一致，无重复 `fact_id`，无页码越界；V2 文档中 Batch 010 初始计数已由 43 条修正为 48 条。

### Formal Batch 010 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "免疫系统 新生仔猪 初乳 黏膜免疫 疫苗失败 皮肤病变 蹄爪 采样 鉴别" --top-k 8
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=487`，`disease_count=73`，`rule_count=113`。
- 证据状态：`HUMAN_REVIEWED=341`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回免疫系统、初乳与新生仔猪免疫、黏膜免疫、疫苗失败、皮肤病变鉴别、皮肤采样、脓疱/水疱边界等新增内容。
- `graph-build`：已重建图谱，`929 nodes / 1047 links`。

## 截至位置更新

- 当前已处理至 PDF page 324。
- 下一次应从 PDF page 325 开始。
- 推荐下一批：PDF page 325-364，继续 Chapter 17 Integumentary System 后段，并视章节边界进入后续系统章节。

## 质量规则

- 没有 PDF 章节和页码锚点的事实不得落库。
- 食品安全、监管、药检、检疫、休药期、用药、手术和公共卫生处置类内容必须等待 A0/A1 来源复核。
- 每批先写候选事实和交叉审查记录，通过后再合并到 `exports/knowledge_facts.json`。

## Formal Batch 011 实施记录

- 完成时间：2026-05-06 21:42:00 +08:00。
- 处理范围：PDF page 325-364。
- 章节边界：Chapter 17 后段；Chapter 18 Mammary System 正文；Chapter 19 Nervous and Locomotor System 开端。
- 新增来源：`SRC-0020`、`SRC-0021`、`SRC-0022`。
- 新增主题页：皮肤真菌/寄生虫/环境/营养性鉴别、蹄爪病变与跛行、乳腺/泌乳/初乳/PDS、神经与运动系统开端导航。
- 新增规则页：`RULE-114` 至 `RULE-127`。
- 新增候选事实：`issues/formal_batch_011_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_011_cross_review.md`。
- 正式落库 facts：47 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、具体 NSAID/催产素/抗菌药剂量方案、固定治疗处方、场内免疫/淘汰/监管结论、中国本地标签或法规结论。

### Formal Batch 011 交叉审查

- 页码锚点核验：通过。`SRC-0020` 覆盖 PDF page 325-334，`SRC-0021` 覆盖 PDF page 337-355，`SRC-0022` 覆盖 PDF page 363-364。
- 内容边界核验：通过。参考文献页不生成事实；治疗段落仅转化为处方边界规则。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- 编码复核：通过。Batch 011 文件已复核为 UTF-8，无替换问号。

### Formal Batch 011 验证结果

- `status`：`fact_count=534`，`disease_count=73`，`rule_count=127`。
- 证据状态：`HUMAN_REVIEWED=388`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回乳腺/泌乳/初乳/PDS、蹄爪病变与跛行、神经与运动系统开端、PDS 体温边界和癣菌/疥螨等新增内容。
- `graph-build`：已重建图谱，`1039 nodes / 1141 links`。

## 截至位置更新

- 当前已处理至 PDF page 364。
- 下一批应从 PDF page 365 开始。
- 推荐下一批：PDF page 365-404，继续 Chapter 19 Nervous and Locomotor System 正文。

## Formal Batch 012 实施记录

- 完成时间：2026-05-06 22:35:00 +08:00。
- 处理范围：PDF page 365-404。
- 章节边界：Chapter 19 后段；Chapter 19 参考文献；Chapter 20 Diseases of the Reproductive System 开端。
- 新增来源：`SRC-0023`、`SRC-0024`。
- 新增主题页：神经运动系统检查/骨关节肌肉导航，跛行/关节炎/骨软骨病/肌病边界，繁殖系统与猪群繁殖问题诊断开端。
- 新增规则页：`RULE-128` 至 `RULE-143`。
- 新增候选事实：`issues/formal_batch_012_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_012_cross_review.md`。
- 正式落库 facts：49 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、固定治疗处方、固定激素/抗菌药方案、药物剂量、淘汰处置、中国监管结论。

### Formal Batch 012 交叉审查

- 页码锚点核验：通过。`SRC-0023` 覆盖 PDF page 365-390，`SRC-0024` 覆盖 PDF page 397-404。
- 内容边界核验：通过。参考文献页不生成事实；治疗和激素段落仅转化为诊断/处方边界规则。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

### Formal Batch 012 验证结果

- `status`：`fact_count=583`，`disease_count=73`，`rule_count=143`。
- 证据状态：`HUMAN_REVIEWED=437`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回跛行、关节炎、骨软骨病、肌病/PSS、繁殖系统诊断、初情延迟、断奶至发情间隔、受胎率/分娩率等新增内容。
- `graph-build`：已重建图谱，`1155 nodes / 1239 links`。
- 编码复核：通过。Batch 012 候选事实、交叉审查记录、进度文档和实施计划未发现替换问号或字面量换行残留。

## 截至位置更新

- 当前已处理至 PDF page 404。
- 下一批应从 PDF page 405 开始。
- 推荐下一批：PDF page 405-444，继续 Chapter 20 Diseases of the Reproductive System。

## Formal Batch 013 实施记录

- 完成时间：2026-05-06 23:25:00 +08:00。
- 处理范围：PDF page 405-444。
- 章节边界：Chapter 20 后段；Chapter 20 参考文献；Chapter 21 Respiratory System 正文；Chapter 21 参考文献；Chapter 22 Urinary System 开端。
- 新增来源：`SRC-0025`、`SRC-0026`、`SRC-0027`。
- 新增主题页：繁殖系统后段分泌物/难产/公猪/流产诊断，呼吸系统防御/PRDC/病理/控制边界，泌尿系统与肾脏病变鉴别，流产采样/血清学/病原边界。
- 新增规则页：`RULE-144` 至 `RULE-159`。
- 新增候选事实：`issues/formal_batch_013_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_013_cross_review.md`。
- 正式落库 facts：70 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、固定激素/抗菌药/助产方案、药物剂量、免疫程序、淘汰或屠宰判定、中国监管结论。

### Formal Batch 013 交叉审查

- 页码锚点核验：通过。`SRC-0025` 覆盖 PDF page 405-415，`SRC-0026` 覆盖 PDF page 417-429，`SRC-0027` 覆盖 PDF page 432-444。
- 内容边界核验：通过。参考文献页不生成事实；治疗、激素、抗菌药、助产、免疫和处置段落仅转化为诊断/风险/处方边界。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

### Formal Batch 013 验证结果

- `status`：`fact_count=653`，`disease_count=73`，`rule_count=159`。
- 证据状态：`HUMAN_REVIEWED=507`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回母猪外阴分泌物、难产、公猪热应激与精液质量、流产采样、PRDC、呼吸防御、肺炎形态、肾小球肾炎、膀胱炎-肾盂肾炎等新增内容。
- `graph-build`：已重建图谱，`1314 nodes / 1379 links`。
- 编码复核：通过。Batch 013 候选事实、交叉审查记录和正式 facts 未发现替换问号或字面量换行残留。

## 截至位置更新

- 当前已处理至 PDF page 444。
- 下一批应从 PDF page 445 开始。
- 推荐下一批：PDF page 445-484，继续 Chapter 22 Urinary System 后续正文，并视页码边界进入下一章节。

## Formal Batch 014 实施记录

- 完成时间：2026-05-06 23:35:00 +08:00。
- 处理范围：PDF page 445-484。
- 章节边界：Chapter 22 收尾；Chapter 22 参考文献；Section III Viral Diseases 扉页/空页；Chapter 23 Overview of Viruses；Chapter 24 Adenoviruses；Chapter 25 African Swine Fever Virus 开端；Chapter 25 参考文献；Chapter 26 Anelloviruses；Chapter 27 Astroviruses 开端。
- 新增来源：`SRC-0028`、`SRC-0029`、`SRC-0030`、`SRC-0031`、`SRC-0032`。
- 新增主题页：泌尿系统大体鉴别和毒性病变边界，病毒总论分类/检测/因果边界，猪腺病毒疾病和诊断边界，非洲猪瘟病毒教材证据和监管边界，猪 Anellovirus 和星状病毒因果边界。
- 新增规则页：`RULE-160` 至 `RULE-175`。
- 新增候选事实：`issues/formal_batch_014_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_014_cross_review.md`。
- 正式落库 facts：72 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、Section III 扉页、空页、ASF 中国上报/封锁/扑杀/调运/消毒执行结论、固定免疫或治疗方案、公共卫生确定性扩展结论。

### Formal Batch 014 交叉审查

- 页码锚点核验：通过。`SRC-0028` 覆盖 PDF page 445-446，`SRC-0029` 覆盖 PDF page 451-461，`SRC-0030` 覆盖 PDF page 462-466，`SRC-0031` 覆盖 PDF page 467-474，`SRC-0032` 覆盖 PDF page 477-484。
- 内容边界核验：通过。参考文献页、扉页和空页不生成 facts；非洲猪瘟仅落库全球教材事实与监管边界，不生成中国本地处置规则。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

### Formal Batch 014 验证结果

- `status`：`fact_count=725`，`disease_count=73`，`rule_count=175`。
- 证据状态：`HUMAN_REVIEWED=579`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回非洲猪瘟教材证据/监管边界、猪腺病毒、星状病毒、TTSuV、病毒检测和病因边界、肾点状出血鉴别等新增内容。
- `graph-build`：已重建图谱，`1479 nodes / 1523 links`。
- 编码复核：通过。Batch 014 候选事实、交叉审查记录和正式 facts 未发现替换问号或字面量换行残留。

## 截至位置更新

- 当前已处理至 PDF page 484。
- 下一批应从 PDF page 485 开始。
- 推荐下一批：PDF page 485-524，继续 Section III Viral Diseases 后续病毒章节。


## Formal Batch 015 实施记录

- 完成时间：2026-05-06 23:59:00 +08:00。
- 处理范围：PDF page 485-524。
- 章节边界：Chapter 28 Bunyaviruses 正文和参考文献；Chapter 29 Caliciviruses 正文和参考文献；Chapter 30 Circoviruses 正文和参考文献；Chapter 31 Coronaviruses 开端至 TGEV/PRCV 免疫段落开端。
- 新增来源：`SRC-0033`、`SRC-0034`、`SRC-0035`、`SRC-0036`。
- 新增主题页：猪布尼亚病毒媒介/诊断/控制边界，猪杯状病毒水疱病和肠道因果边界，猪圆环病毒 PCV2/PCV3/PDNS 诊断边界，猪冠状病毒 TGEV/PRCV 诊断和免疫边界。
- 新增规则页：`RULE-176` 至 `RULE-191`。
- 新增候选事实：`issues/formal_batch_015_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_015_cross_review.md`。
- 正式落库 facts：70 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、口蹄疫/重大水疱病排除结论、PCV3 确定性病原结论、PCV2 定性 PCR 单独确诊、固定疫苗程序、药物剂量、根除承诺、ASF/CSF/水疱病中国监管处置结论。

### Formal Batch 015 交叉审查

- 页码锚点核验：通过。`SRC-0033` 覆盖 PDF page 485-486；`SRC-0034` 覆盖 PDF page 488-495；`SRC-0035` 覆盖 PDF page 497-507；`SRC-0036` 覆盖 PDF page 512-524。PDF page 487、496、508-511 为参考文献页，未生成 facts。
- 内容边界核验：通过。布尼亚病毒、杯状病毒、圆环病毒和冠状病毒事实均限制在教材证据、诊断/鉴别/免疫边界和因果解释；未生成本地监管或处方结论。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- 编码复核：通过。Batch 015 候选事实、交叉审查记录、topic/rule/source 页面和正式 facts 已二次修复 UTF-8，新增文件未发现替换问号或替换字符。

### Formal Batch 015 验证结果

- `status`：`fact_count=795`，`disease_count=73`，`rule_count=191`。
- 证据状态：`HUMAN_REVIEWED=649`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回布尼亚病毒/Akabane、杯状病毒水疱病、PCV2/PCV3/PDNS、TGEV/PRCV 诊断和免疫边界等新增内容。
- `graph-build`：已重建图谱，`1639 nodes / 1663 links`。

## 截至位置更新

- 当前已处理至 PDF page 524。
- 下一批应从 PDF page 525 开始。
- 推荐下一批：PDF page 525-564，继续 Chapter 31 Coronaviruses 后续正文，并视页码边界进入后续病毒章节。

## 后续待处理阶段

- PDF page 525-766：Section III Viral Diseases。
- PDF page 767-1026：Section IV Bacterial Diseases。
- PDF page 1027-1064：Section V Parasitic Diseases。
- PDF page 1065-1111：Section VI Noninfectious Diseases。
- PDF page 1112-1132：Index。


## Formal Batch 017 实施记录

- 完成时间：2026-05-07 00:35:00 +08:00。
- 处理范围：PDF page 565-604。
- 章节边界：Chapter 33 Flaviviruses 参考文献收尾；Chapter 34 Hepatitis E Virus；Chapter 35 Herpesviruses；Chapter 36 Influenza Viruses 开端。
- 新增来源：`SRC-0040`、`SRC-0041`、`SRC-0042`。
- 新增主题页：猪 HEV 人兽共患和食品安全边界、猪疱疹病毒 PRV/PCMV/PLHV/MCF 诊断和控制边界、猪流感病毒重配/谱系/跨种引入边界。
- 新增规则页：`RULE-209` 至 `RULE-225`。
- 新增候选事实：`issues/formal_batch_017_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_017_cross_review.md`。
- 正式落库 facts：31 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、HEV 食品召回/烹饪温度/人群诊疗结论、PRV 本地根除或监管结论、固定疫苗程序、猪流感亚型本地流行结论和具体防控处方。

### Formal Batch 017 交叉审查

- 页码锚点核验：通过。`SRC-0040` 覆盖 PDF page 568-571，`SRC-0041` 覆盖 PDF page 572-599，`SRC-0042` 覆盖 PDF page 600-604。PDF page 565-567、570-571、595-599 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。HEV、PRV/PCMV/PLHV/MCF、猪流感均只落库教材证据和诊断/公共卫生/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 604。
- 下一批应从 PDF page 605 开始。
- 推荐下一批：PDF page 605-644，继续 Chapter 36 Influenza Viruses 正文。

### Formal Batch 017 验证结果

- `status`：`fact_count=888`，`disease_count=73`，`rule_count=225`，`sources=42`，`topics=54`。
- 证据状态：`HUMAN_REVIEWED=742`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 HEV/戊型肝炎、PRV/伪狂犬病、PCMV、猪 MCF、猪流感重配/谱系/血清学边界等新增内容。
- `graph-build`：已重建图谱，`1865 nodes / 1849 links`。


## Formal Batch 018 实施记录

- 完成时间：2026-05-07 07:20:00 +08:00。
- 处理范围：PDF page 605-644。
- 章节边界：Chapter 36 Influenza Viruses 后段和参考文献；Chapter 37 Paramyxoviruses；Chapter 38 Parvoviruses 开端。
- 新增来源：`SRC-0043`、`SRC-0044`、`SRC-0045`。
- 新增主题页：猪流感诊断/免疫/疫苗边界、猪副黏病毒 Blue eye/Menangle/Nipah/PPIV-1 边界、猪细小病毒 PPV1 繁殖损失和诊断边界。
- 新增规则页：`RULE-226` 至 `RULE-241`。
- 新增候选事实：`issues/formal_batch_018_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_018_cross_review.md`。
- 正式落库 facts：35 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、固定免疫程序、疫苗产品推荐、尼帕病毒现场处置流程、中国监管处置、PPV 固定控制方案和药物/剂量结论。

### Formal Batch 018 交叉审查

- 页码锚点核验：通过。`SRC-0043` 覆盖 PDF page 605-617，`SRC-0044` 覆盖 PDF page 618-634，`SRC-0045` 覆盖 PDF page 635-644。PDF page 613-617、633-634 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。猪流感、蓝眼病、Menangle、Nipah、PPIV-1、PPV 均只落库教材证据和诊断/免疫/公共卫生/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 644。
- 下一批应从 PDF page 645 开始。
- 推荐下一批：PDF page 645-684，继续 Chapter 38 Parvoviruses 后续正文，并视页码边界进入后续病毒章节。

### Formal Batch 018 验证结果

- `status`：`fact_count=923`，`disease_count=73`，`rule_count=241`，`sources=45`，`topics=57`。
- 证据状态：`HUMAN_REVIEWED=777`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回猪流感 PCR/病毒分离、母源抗体、疫苗匹配、VAERD、尼帕病毒、蓝眼病、Menangle、PPIV-1、PPV1/细小病毒繁殖损失和诊断边界等新增内容。
- `graph-build`：已重建图谱，`1954 nodes / 1919 links`。


## 优化执行规范建立记录

- 完成时间：2026-05-07 08:10:00 +08:00。
- 新增执行文档：`docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md`。
- 后续正式批次需按该文档执行：读取 v2 入口、三解析器 PDF 抽取、候选事实、交叉审查、审查通过后落库、同步 v2 文档、运行 status/lint/query/graph-build 并回写验证结果。

## Formal Batch 019 实施记录

- 完成时间：2026-05-07 08:10:00 +08:00。
- 处理范围：PDF page 645-684。
- 章节边界：Chapter 38 Parvoviruses 参考文献收尾；Chapter 39 Pestiviruses；Chapter 40 Picornaviruses 开端。
- 新增来源：`SRC-0046`、`SRC-0047`。
- 新增主题页：猪 Pestivirus/CSFV 诊断和控制边界、猪 Picornavirus/FMD/SVD 水疱病鉴别边界。
- 新增规则页：`RULE-242` 至 `RULE-257`。
- 新增候选事实：`issues/formal_batch_019_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_019_cross_review.md`。
- 正式落库 facts：34 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、CSF/FMD 中国监管处置、固定免疫程序、扑杀/封锁/调运/消毒命令、FMD 疫苗产品推荐、SVDV 完整后续疾病结论。

### Formal Batch 019 交叉审查

- 页码锚点核验：通过。`SRC-0046` 覆盖 PDF page 646-664，`SRC-0047` 覆盖 PDF page 665-684。PDF page 645、662-664 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。CSF/CSFV、FMDV、SVDV、Bungowannah、反刍动物 pestivirus 和 APPV 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 684。
- 下一批应从 PDF page 685 开始。
- 推荐下一批：PDF page 685-724，继续 Chapter 40 Picornaviruses 后续正文。

### Formal Batch 019 验证结果

- `status`：`fact_count=958`，`disease_count=73`，`rule_count=257`，`sources=47`，`topics=59`。
- 证据状态：`HUMAN_REVIEWED=812`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 CSF/经典猪瘟、CSFV/pestivirus 诊断和血清学交叉反应、FMD/口蹄疫气溶胶传播、水疱病鉴别、SVDV 与 FMD 实验室鉴别等新增内容。
- `graph-build`：已重建图谱，`2042 nodes / 1989 links`。


## Formal Batch 020 实施记录

- 完成时间：2026-05-07 09:00:00 +08:00。
- 处理范围：PDF page 685-724。
- 章节边界：Chapter 40 Picornaviruses 后续正文和参考文献；Chapter 41 PRRSV 开端。
- 新增来源：`SRC-0048`、`SRC-0049`。
- 新增主题页：猪 Picornavirus SVD/EMCV/Teschovirus/SVV 边界、PRRSV 传播/诊断/免疫/防控边界。
- 新增规则页：`RULE-258` 至 `RULE-273`。
- 新增候选事实：`issues/formal_batch_020_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_020_cross_review.md`。
- 正式落库 facts：38 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、固定疫苗程序、PRRSV 清群/净化方案、中国监管处置、SVDV/SVV/FMD 监管命令、EMCV 固定控制方案。

### Formal Batch 020 交叉审查

- 页码锚点核验：通过。`SRC-0048` 覆盖 PDF page 685-708，`SRC-0049` 覆盖 PDF page 709-724。PDF page 701-708 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。SVDV、EMCV、teschovirus/sapelovirus、SVV、kobuvirus/pasivirus 和 PRRSV 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

### Formal Batch 020 验证结果

- `status`：`fact_count=996`，`disease_count=73`，`rule_count=273`，`sources=49`，`topics=61`。
- 证据状态：`HUMAN_REVIEWED=850`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 SVDV/EMCV/Teschovirus/Senecavirus A/SVV 水疱病鉴别、PRRSV PCR/ELISA/精液/气溶胶/疫苗/母源抗体边界等新增内容。
- `graph-build`：已重建图谱，`2136 nodes / 2065 links`。

## 截至位置更新

- 当前已处理至 PDF page 724。
- 下一批应从 PDF page 725 开始。
- 推荐下一批：PDF page 725-764，继续 Chapter 41 PRRSV 正文后段和参考文献边界。



## Formal Batch 021 / V3 实施记录

- 完成时间：2026-05-07 09:40:00 +08:00。
- 处理范围：PDF page 725-764。
- 章节边界：Chapter 41 PRRSV 控制和监测尾段；Chapter 42 Swinepox；Chapter 43 Reoviruses；Chapter 44 Retroviruses；Chapter 45 Rhabdoviruses；Chapter 46 Togaviruses 开端。
- 参考文献页处理：PDF page 727-732、738、748-751、756、763 仅作为章节边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0050` 至 `SRC-0055`。
- 新增主题页：PRRSV 控制/净化/监测边界、猪痘诊断/控制边界、轮状病毒/呼肠孤病毒肠道病边界、PERV 异种移植边界、Rhabdovirus 水疱性口炎/狂犬病边界、Togavirus 开端锚点。
- 新增规则页：`RULE-274` 至 `RULE-293`。
- 新增候选事实：`issues/formal_batch_021_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_021_cross_review.md`。
- 正式落库 facts：44 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、PRRSV 固定净化程序、LVI 操作流程、猪痘特异性抗病毒治疗、轮状病毒处方/疫苗程序、PERV 普通猪场处置、VSV/狂犬病本地监管和公共卫生处置细则、Togavirus 后续正文结论。

### Formal Batch 021 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0050` 覆盖 PDF page 725-726；`SRC-0051` 覆盖 733-738；`SRC-0052` 覆盖 739-751；`SRC-0053` 覆盖 752-756；`SRC-0054` 覆盖 757-763；`SRC-0055` 覆盖 764。
- 内容边界核验：通过。PRRSV、猪痘、轮状病毒/呼肠孤病毒、PERV、VSV/狂犬病和 Togavirus 开端均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 764。
- 下一批应从 PDF page 765 开始。
- 推荐下一批：PDF page 765-804，继续 Chapter 46 Togaviruses 正文。

### Formal Batch 021 / V3 验证结果

- `status`：`fact_count=1040`，`disease_count=73`，`rule_count=293`，`sources=55`，`topics=67`。
- 证据状态：`HUMAN_REVIEWED=894`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 PRRSV LVI/封群/检测剔除/监测、猪痘、轮状病毒、PERV、水疱性口炎、狂犬病和 Togavirus 开端等新增内容。
- `graph-build`：已重建图谱，`2250 nodes / 2153 links`。


## Formal Batch 022 / V3 实施记录

- 完成时间：2026-05-07 10:20:00 +08:00。
- 处理范围：PDF page 765-804。
- 章节边界：Chapter 46 Togaviruses 后续正文；Section IV Bacterial Diseases 分隔页；Chapter 47 Overview of Bacteria；Chapter 48 Actinobacillosis；Chapter 49 Bordetellosis；Chapter 50 Brucellosis 开端。
- 参考文献/分隔页处理：PDF page 767-768、772、788-790、800-801 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0056` 至 `SRC-0060`。
- 新增主题页：Togavirus EEEV/SAGV/RRV 边界、细菌病总论边界、Actinobacillosis App/A. suis 边界、Bordetellosis 边界、Brucellosis 开端传播边界。
- 新增规则页：`RULE-294` 至 `RULE-311`。
- 新增候选事实：`issues/formal_batch_022_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_022_cross_review.md`。
- 正式落库 facts：42 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、抗菌药通用处方、App 固定免疫/净化方案、Bordetella 固定疫苗程序、Brucellosis 中国监管/检疫/扑杀/人暴露处置结论。

### Formal Batch 022 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0056` 覆盖 PDF page 765-766；`SRC-0057` 覆盖 769-772；`SRC-0058` 覆盖 773-790；`SRC-0059` 覆盖 791-801；`SRC-0060` 覆盖 802-804。
- 内容边界核验：通过。Togavirus、细菌总论、Actinobacillosis、Bordetellosis 和 Brucellosis 开端均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 804。
- 下一批应从 PDF page 805 开始。
- 推荐下一批：PDF page 805-844，继续 Chapter 50 Brucellosis 正文，并视章节边界进入后续细菌病章节。

### Formal Batch 022 / V3 验证结果

- `status`：`fact_count=1082`，`disease_count=73`，`rule_count=311`，`sources=60`，`topics=72`。
- 证据状态：`HUMAN_REVIEWED=936`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 EEEV/SAGV/RRV、细菌芽孢/革兰染色、App/ApxIV/A. suis、Bordetella、Brucella suis/布鲁氏菌传播边界等新增内容。
- `graph-build`：已重建图谱，`2357 nodes / 2237 links`。


## Formal Batch 023 / V3 实施记录

- 完成时间：2026-05-07 11:00:00 +08:00。
- 处理范围：PDF page 805-844。
- 章节边界：Chapter 50 Brucellosis 正文后段和参考文献；Chapter 51 Clostridial Diseases 正文和参考文献；Chapter 52 Colibacillosis 开端。
- 参考文献处理：PDF page 813-815、829-830 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0061` 至 `SRC-0063`。
- 新增主题页：猪布鲁氏菌诊断/血清学/疫苗边界、猪梭菌病诊断/毒素/防控边界、猪大肠杆菌病 ETEC/EDEC/ExPEC 边界。
- 新增规则页：`RULE-312` 至 `RULE-328`。
- 新增候选事实：`issues/formal_batch_023_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_023_cross_review.md`。
- 正式落库 facts：43 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、布鲁氏菌中国监管/人暴露处置、梭菌病固定抗毒素/抗菌药/疫苗程序、大肠杆菌病抗菌药通用处方。

### Formal Batch 023 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0061` 覆盖 PDF page 805-815；`SRC-0062` 覆盖 816-830；`SRC-0063` 覆盖 831-844。
- 内容边界核验：通过。Brucellosis、Clostridial diseases 和 Colibacillosis 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 844。
- 下一批应从 PDF page 845 开始。
- 推荐下一批：PDF page 845-884，继续 Chapter 52 Colibacillosis 正文后段和参考文献，并视章节边界进入后续细菌病章节。

### Formal Batch 023 / V3 验证结果

- `status`：`fact_count=1125`，`disease_count=73`，`rule_count=328`，`sources=63`，`topics=75`。
- 证据状态：`HUMAN_REVIEWED=979`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 Brucella biovar/血清学假阳性/Yersinia O:9/疫苗边界、C. perfringens/C. difficile/肉毒中毒、ETEC/EDEC/水肿病/Stx2e 等新增内容。
- `graph-build`：已重建图谱，`2463 nodes / 2323 links`。


## Formal Batch 024 / V3 实施记录

- 完成时间：2026-05-07 11:45:00 +08:00。
- 处理范围：PDF page 845-884。
- 章节边界：Chapter 52 Colibacillosis 正文后段和参考文献；Chapter 53 Erysipelas；Chapter 54 Glasser disease；Chapter 55 Leptospirosis 开端。
- 参考文献处理：PDF page 857-858、866-867、876-877 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0064` 至 `SRC-0067`。
- 新增主题页：Colibacillosis PWD/ED/系统感染/乳房炎/UTI 边界、猪丹毒鉴别/公共卫生边界、格拉瑟病免疫/共同感染/诊断边界、猪钩端螺旋体 serovar/人兽共患/传播边界。
- 新增规则页：`RULE-329` 至 `RULE-344`。
- 新增候选事实：`issues/formal_batch_024_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_024_cross_review.md`。
- 正式落库 facts：44 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、大肠杆菌抗菌药通用处方、猪丹毒治疗/疫苗程序、格拉瑟病群体固定预防用药、钩端螺旋体公共卫生和中国监管处置结论。

### Formal Batch 024 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0064` 覆盖 PDF page 845-858；`SRC-0065` 覆盖 859-867；`SRC-0066` 覆盖 868-877；`SRC-0067` 覆盖 878-884。
- 内容边界核验：通过。Colibacillosis、Erysipelas、Glasser disease 和 Leptospirosis 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 884。
- 下一批应从 PDF page 885 开始。
- 推荐下一批：PDF page 885-924，继续 Chapter 55 Leptospirosis 正文后段和参考文献，并视章节边界进入后续细菌病章节。

### Formal Batch 024 / V3 验证结果

- `status`：`fact_count=1169`，`disease_count=73`，`rule_count=344`，`sources=67`，`topics=79`。
- 证据状态：`HUMAN_REVIEWED=1023`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回 PWD/ED 溶血和水肿病诊断边界、母猪 UTI、猪丹毒菱形皮损和 erysipeloid、Glasser/H. parasuis 母源免疫、Leptospirosis Pomona/Bratislava/Canicola 等新增内容。
- `graph-build`：已重建图谱，`2571 nodes / 2411 links`。

## Formal Batch 025 / V3 实施记录

- 完成时间：2026-05-07 12:35:00 +08:00。
- 处理范围：PDF page 885-924。
- 章节边界：Chapter 55 Leptospirosis 控制尾段和参考文献；Chapter 56 Mycoplasmosis 正文和参考文献；Chapter 57 Pasteurellosis 正文和参考文献；Chapter 58 Proliferative Enteropathy 开端。
- 参考文献处理：PDF page 886、902-907、919-921 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0068` 至 `SRC-0071`。
- 新增主题页：猪钩端螺旋体控制/免疫/给药/人工授精边界、猪支原体四类主要致病种边界、猪多杀性巴氏杆菌病 PAR/肺炎型/败血型边界、猪 Lawsonia 增生性肠病开端边界。
- 新增规则页：`RULE-345` 至 `RULE-361`。
- 新增候选事实：`issues/formal_batch_025_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_025_cross_review.md`。
- 正式落库 facts：47 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、钩端螺旋体固定给药剂量/免疫程序/休药期、M. hyopneumoniae 固定根除方案、支原体/巴氏杆菌抗菌药处方、疫苗产品推荐、Lawsonia 完整临床/诊断/防控结论、中国监管或公共卫生处置结论。

### Formal Batch 025 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0068` 覆盖 PDF page 885-886；`SRC-0069` 覆盖 887-907；`SRC-0070` 覆盖 908-921；`SRC-0071` 覆盖 922-924。
- 内容边界核验：通过。Leptospirosis、Mycoplasmosis、Pasteurellosis 和 Proliferative Enteropathy 开端均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- 编码复核：通过。Batch 025 候选事实、交叉审查、规则页和索引已修复为 UTF-8，无成串替换问号残留。

## 截至位置更新

- 当前已处理至 PDF page 924。
- 下一批应从 PDF page 925 开始。
- 推荐下一批：PDF page 925-964，继续 Chapter 58 Proliferative Enteropathy 正文，补充 Lawsonia 传播、临床型、诊断、治疗和防控边界，并视章节边界进入后续细菌病章节。

### Formal Batch 025 / V3 验证结果

- `status`：`fact_count=1216`，`disease_count=73`，`rule_count=361`，`sources=71`，`topics=83`。
- 证据状态：`HUMAN_REVIEWED=1070`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为既有目录级 `NEEDS_REVIEW` facts。
- `query`：可召回猪支原体/M. hyopneumoniae 地方性肺炎诊断和疫苗边界、P. multocida/PAR/肺炎型/败血型巴氏杆菌病边界、Lawsonia/增生性肠病开端等新增内容。
- `graph-build`：已重建图谱，`2686 nodes / 2505 links`。

