# 猪病 LLM Wiki 知识库实施文档 V2

## 目标

本 V2 文档从 V1 的 Formal Batch 007 之后继续记录猪病 LLM Wiki 知识库构建，避免 `SWINE_LLM_WIKI_IMPLEMENTATION_PLAN.md` 继续膨胀。V1 保留 Batch 0 至 Formal Batch 007 的完整历史；V2 从 Formal Batch 008 开始做增量记录。

知识库路径仍为 `knowledge/llm_wiki_swine_authoritative`。正文抽取继续使用本地 PDF `docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman, Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf`。每批仍需先生成候选事实和交叉审查记录，确认页码锚点、内容边界和一致性无问题后再落库。

## V1 继承状态

- V1 截至批次：Formal Batch 007。
- V1 截至页码：PDF page 220。
- V1 已处理范围：PDF page 1-220。
- V1 当前事实：`fact_count=362`，其中 `HUMAN_REVIEWED=216`、`NEEDS_REVIEW=146`。
- V1 当前来源页：`SRC-0001` 至 `SRC-0013`。
- V1 当前规则页：`RULE-001` 至 `RULE-070`。
- V1 图谱状态：`630 nodes / 797 links`。

## Formal Batch 008 完成记录

- 完成时间：2026-05-06 18:06:12 +08:00。
- 处理范围：PDF page 221-244。
- 章节：Chapter 12 Preharvest Food Safety, Zoonotic Diseases, and the Human Health Interface；Chapter 13 Special Considerations for Show and Pet Pigs。
- 已落库来源：`SRC-0014`、`SRC-0015`。
- 已落库主题页：猪肉屠前食品安全/人兽共患/人类健康接口、展览猪健康/生物安全/药检/伦理边界、宠物猪护理/行为/用药边界。
- 已落库规则页：`RULE-071` 至 `RULE-085`。
- 已落库正式事实：43 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_008_cross_review.md`。
- 明确未生成内容：具体休药期、药检阈值、召回方案、强制检疫处置、展会合格承诺、具体疫苗/驱虫/用药剂量、手术步骤、中国监管结论。
- 验证命令：已运行 `status`、`lint`、`query "猪肉 食品安全 沙门氏菌 休药期 展览猪 药检 宠物猪 约束"`、`graph-build`。
- 验证结果：`fact_count=405`，`disease_count=73`，`rule_count=85`；`HUMAN_REVIEWED=259`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `733 nodes / 883 links`。
- 当前截至位置：PDF page 244。下一批从 PDF page 245 开始。

### Formal Batch 008 具体实施说明

1. PDF page 221-234 用于构建食品安全危害分类、断针物理危害、化学残留边界、食源性/接触型人兽共患风险和抗菌药耐药解释边界。
2. PDF page 235-244 用于构建展览猪流动生物安全、展会人兽共患教育、健康方案、药检规则、伦理边界、宠物猪行为约束、免疫/寄生虫/牙蹄护理和用药边界。
3. 美国监管、展会药检、残留数值、具体操作和治疗用药均只作为风险边界记录，不转成中国场景的生产结论。
4. 食品安全、监管、药检、检疫、人兽共患处置和用药仍需 A0/A1 来源补强后才能进入生产答案约束。

## Formal Batch 009 完成记录

- 一次处理可行性判断：PDF page 245-448 共 204 页，覆盖 Section II Body Systems 多个系统章节，不适合一次处理；本轮拆分处理 PDF page 245-284。
- 完成时间：2026-05-06 19:28:50 +08:00。
- 处理范围：PDF page 245-284。
- 章节：Section II Body Systems 起始页；Chapter 14 Cardiovascular and Hematopoietic Systems；Chapter 15 Digestive System 正文至参考文献页开端。
- 已落库来源：`SRC-0016`、`SRC-0017`。
- 已落库主题页：猪心血管与造血系统导航、猪消化系统与腹泻鉴别导航、猪系统性剖检与临床病理解释边界。
- 已落库规则页：`RULE-086` 至 `RULE-099`。
- 已落库正式事实：34 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_009_cross_review.md`。
- 明确未生成内容：具体处方、补液方案、抗菌药方案、手术方案、补硒/维生素方案、中国监管结论。
- 验证命令：已运行 `status`、`lint`、`query "心血管 造血 心脏剖检 桑葚心 胃溃疡 腹泻 新生仔猪 鉴别"`、`graph-build`。
- 验证结果：`fact_count=439`，`disease_count=73`，`rule_count=99`；`HUMAN_REVIEWED=293`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `817 nodes / 951 links`。
- 二次严格验证：2026-05-06 已复核 PDF 契合度、来源页码、落库一致性和图谱同步；`DIG-016` 已将锚点收紧为 `PDF page 280-281` 并同步派生图谱。
- 当前截至位置：PDF page 284。下一批从 PDF page 285 开始。

### Formal Batch 009 具体实施说明

1. PDF page 245-246 只作为 Section II Body Systems 起始边界，不生成独立临床事实。
2. PDF page 247-257 用于构建心血管/造血系统功能、临床病理解释、心脏剖检、心包/心肌/心内膜病变、心衰/休克和发绀等系统导航事实。
3. PDF page 258-284 用于构建消化系统功能、口腔/胃/肠道结构性病变、胃溃疡、肠扭转、腹泻机制和年龄阶段性鉴别边界。
4. 教材表格中的参考区间、病原清单和诊断确认项目均未转为单独确诊依据；本批不完善具体病原疾病页正文。

## Formal Batch 010 完成记录

- 完成时间：2026-05-06 20:35:00 +08:00。
- 处理范围：PDF page 285-324。
- 章节：Chapter 15 参考文献尾页；Chapter 16 Immune System 正文；Chapter 17 Integumentary System: Skin, Hoof, and Claw 前段。
- 已落库来源：`SRC-0018`、`SRC-0019`。
- 已落库主题页：猪免疫系统与疫苗边界、新生仔猪与黏膜免疫、猪皮肤/蹄/爪病变鉴别与采样。
- 已落库规则页：`RULE-100` 至 `RULE-113`。
- 已落库正式事实：48 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_010_cross_review.md`。
- 明确未生成内容：具体疫苗免疫程序、返饲或攻毒操作方案、佐剂配方、具体药物剂量、采样麻醉细节、治疗处方、中国监管结论。
- 验证命令：已运行 `status`、`lint`、`query "免疫系统 新生仔猪 初乳 黏膜免疫 疫苗失败 皮肤病变 蹄爪 采样 鉴别"`、`graph-build`。
- 验证结果：`fact_count=487`，`disease_count=73`，`rule_count=113`；`HUMAN_REVIEWED=341`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `929 nodes / 1047 links`。
- 当前截至位置：PDF page 324。下一批从 PDF page 325 开始。

### Formal Batch 010 具体实施说明

1. PDF page 285-287 和 313-315 为参考文献页，只作为章节边界，不单独生成事实。
2. PDF page 288-312 用于构建免疫系统、先天免疫、适应性免疫、黏膜免疫、新生仔猪初乳免疫、应激/营养/共感染免疫调节和疫苗失败边界。
3. PDF page 316-324 用于构建皮肤屏障功能、病史与环境风险、病变形态和部位鉴别、皮肤采样、外渗性表皮炎、耳坏死、丹毒和水疱性疾病监管边界。
4. 本批不把教材中的疫苗、攻毒、治疗、采样技术细节转换为生产处方或监管结论。

## 当前完成状态

- 已处理页码：PDF page 1-524。
- 当前截至位置：下一次从 PDF page 525 开始。
- 已生成疾病/综合征/中毒条目：73 个。
- 已生成目录级事实：146 条，保持 `NEEDS_REVIEW`。
- 已生成正式交叉审查事实：649 条，均为 `HUMAN_REVIEWED`。
- 当前来源页：`SRC-0001` 至 `SRC-0036`。
- 当前规则页：`RULE-001` 至 `RULE-191`。
- 当前图谱状态：已重建，`1639 nodes / 1663 links`。
- 当前 V2 进度记录：`knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress_v2.md`。

注意：目录级病种覆盖仍不能直接当作完整临床知识或处方依据；只有通过候选事实、交叉审查和页码锚点核验的 `HUMAN_REVIEWED` facts 才能进入正式生成/评估约束。

## PDF 分批识别方案

每批处理后必须更新：

- `issues/pdf_processing_progress_v2.md`
- 对应 disease/topic/source 页面
- `exports/knowledge_facts.json`
- 必要时更新 `exports/disease_index.csv` 或 `exports/rule_index.csv`
- 对应 `issues/formal_batch_xxx_candidate_facts.json`
- 对应 `issues/formal_batch_xxx_cross_review.md`

正文抽取继续按 20-40 页分片推进。进入 Section II Body Systems 后，优先构建系统/综合征导航、鉴别诊断边界和采样解释，不提前生成具体疾病处方、剂量或监管结论。

## 质量边界

- 没有 PDF 章节和页码锚点的事实不得落库。
- 药方、剂量、休药期、监管处置、药检合格承诺、强制检疫、召回和扑杀等结论必须等待相应章节和 A0/A1 来源复核。
- 教材中的美国法规、展会规则和国际贸易语境不得直接迁移为中国监管答案。
- 每批先写候选事实和交叉审查记录，通过后再合并到 `exports/knowledge_facts.json`。

## 权威来源补强计划

V2 后续应优先补强：

- 中国动物疫病病种名录、检疫规程和食品安全法规。
- 中国兽药标签、禁限用药、残留限量和休药期文件。
- 展览猪或宠物猪涉及的检疫、运输、用药和公共卫生要求。
- WOAH / FAO 等 A1 来源，用于法定疫病、人兽共患和国际贸易边界。

## 验证命令

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪肉 食品安全 沙门氏菌 休药期 展览猪 药检 宠物猪 约束" --top-k 8
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

## 下一次工作入口

从 `knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress_v2.md` 读取当前截至位置。

当前截至：PDF page 524。

下一批建议处理：PDF page 525-564。

## Formal Batch 011 完成记录

- 完成时间：2026-05-06 21:42:00 +08:00。
- 处理范围：PDF page 325-364。
- 章节：Chapter 17 后段、Chapter 18 Mammary System 正文、Chapter 19 Nervous and Locomotor System 开端。
- 已落库来源：`SRC-0020`、`SRC-0021`、`SRC-0022`。
- 已落库主题页：皮肤真菌/寄生虫/环境/营养性鉴别，蹄爪病变与跛行，乳腺/泌乳/初乳/PDS，神经与运动系统开端导航。
- 已落库规则页：`RULE-114` 至 `RULE-127`。
- 已落库正式事实：47 条，均为 `HUMAN_REVIEWED`，均锚定具体 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_011_cross_review.md`。
- 明确未生成内容：参考文献列表、药物剂量、固定治疗处方、固定催产素/NSAID/抗菌药方案、中国监管结论。
- 当前截至位置：PDF page 364。下一批从 PDF page 365 开始，建议 PDF page 365-404。

## Formal Batch 012 完成记录

- 完成时间：2026-05-06 22:35:00 +08:00。
- 处理范围：PDF page 365-404。
- 章节：Chapter 19 后段、Chapter 20 Diseases of the Reproductive System 开端。
- 已落库来源：`SRC-0023`、`SRC-0024`。
- 已落库主题页：神经运动系统检查/骨关节肌肉导航，跛行/关节炎/骨软骨病/肌病边界，繁殖系统与猪群繁殖问题诊断开端。
- 已落库规则页：`RULE-128` 至 `RULE-143`。
- 已落库正式事实：49 条，均为 `HUMAN_REVIEWED`，均锚定具体 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_012_cross_review.md`。
- 明确未生成内容：参考文献列表、药物剂量、固定治疗处方、固定激素/抗菌药方案、中国监管结论。
- 验证结果：`status`、`lint`、主题检索和 `graph-build` 均通过；当前 `fact_count=583`，`HUMAN_REVIEWED=437`，图谱为 `1155 nodes / 1239 links`。
- 当前截至位置：PDF page 404。下一批从 PDF page 405 开始，建议 PDF page 405-444。

## Formal Batch 013 完成记录

- 完成时间：2026-05-06 23:25:00 +08:00。
- 处理范围：PDF page 405-444。
- 章节：Chapter 20 后段、Chapter 21 Respiratory System 正文、Chapter 22 Urinary System 开端；参考文献页只作边界。
- 已落库来源：`SRC-0025`、`SRC-0026`、`SRC-0027`。
- 已落库主题页：繁殖系统后段分泌物/难产/公猪/流产诊断，呼吸系统防御/PRDC/病理/控制边界，泌尿系统与肾脏病变鉴别，流产采样/血清学/病原边界。
- 已落库规则页：`RULE-144` 至 `RULE-159`。
- 已落库正式事实：70 条，均为 `HUMAN_REVIEWED`，均锚定具体 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_013_cross_review.md`。
- 明确未生成内容：参考文献列表、固定激素/抗菌药/助产方案、药物剂量、免疫程序、淘汰或屠宰判定、中国监管结论。
- 验证结果：`status`、`lint`、主题检索和 `graph-build` 均通过；当前 `fact_count=653`，`HUMAN_REVIEWED=507`，图谱为 `1314 nodes / 1379 links`。
- 当前截至位置：PDF page 444。下一批从 PDF page 445 开始，建议 PDF page 445-484。


## Formal Batch 014 完成记录

- 完成时间：2026-05-06 23:35:00 +08:00。
- 处理范围：PDF page 445-484。
- 章节：Chapter 22 收尾、Chapter 23 Overview of Viruses、Chapter 24 Adenoviruses、Chapter 25 African Swine Fever Virus 开端、Chapter 26 Anelloviruses、Chapter 27 Astroviruses 开端。
- 已落库来源：`SRC-0028` 至 `SRC-0032`。
- 已落库主题页：泌尿系统大体鉴别和毒性病变边界，病毒总论分类/检测/因果边界，猪腺病毒疾病和诊断边界，非洲猪瘟病毒教材证据和监管边界，猪 Anellovirus 和星状病毒因果边界。
- 已落库规则页：`RULE-160` 至 `RULE-175`。
- 已落库正式事实：72 条，均为 `HUMAN_REVIEWED`，均锚定具体 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_014_cross_review.md`。
- 验证结果：`status`、`lint`、主题检索和 `graph-build` 均通过；当前 `fact_count=725`，`HUMAN_REVIEWED=579`，图谱为 `1479 nodes / 1523 links`。
- 当前截至位置：PDF page 484。下一批从 PDF page 485 开始。

## Formal Batch 015 完成记录

- 完成时间：2026-05-06 23:59:00 +08:00。
- 处理范围：PDF page 485-524。
- 章节：Chapter 28 Bunyaviruses、Chapter 29 Caliciviruses、Chapter 30 Circoviruses、Chapter 31 Coronaviruses 开端。
- 已落库来源：`SRC-0033` 至 `SRC-0036`。
- 已落库主题页：猪布尼亚病毒媒介/诊断/控制边界，猪杯状病毒水疱病和肠道因果边界，猪圆环病毒 PCV2/PCV3/PDNS 诊断边界，猪冠状病毒 TGEV/PRCV 诊断和免疫边界。
- 已落库规则页：`RULE-176` 至 `RULE-191`。
- 已落库正式事实：70 条，均为 `HUMAN_REVIEWED`，均锚定具体 PDF page。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_015_cross_review.md`。
- 明确未生成内容：参考文献列表、重大水疱病排除/监管处置、PCV3 确定性病原结论、PCV2 定性 PCR 单独确诊、固定疫苗程序、药物剂量、根除承诺、中国监管结论。
- 验证结果：`status`、`lint`、主题检索和 `graph-build` 均通过；当前 `fact_count=795`，`HUMAN_REVIEWED=649`，图谱为 `1639 nodes / 1663 links`。
- 当前截至位置：PDF page 524。下一批从 PDF page 525 开始，建议 PDF page 525-564。

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
