# 猪病 LLM Wiki 知识库实施文档

## 目标

在现有鸡病 LLM Wiki 架构上，构建一个同构的猪病知识库 `knowledge/llm_wiki_swine_authoritative`，并接入同一套生成、评估、规则审计和 DeepEval 复核系统。

本轮以本地 PDF `docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman,  Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf` 作为初始教材来源，先完成 Phase 1 和 Phase 2 的可运行骨架。由于 PDF 共 1132 页，正文抽取必须分批进行，每批处理后更新截至页码，避免上下文过长和证据边界混乱。


## Formal Batch 001 完成记录

- 完成时间：2026-05-06 16:34:49 +08:00（UTC 2026-05-06T08:34:49.578542+00:00）
- 更新确认时间：2026-05-06 16:37:16 +08:00
- 处理范围：PDF page 13-40。
- 已落库来源：SRC-0002、SRC-0003。
- 已落库主题页：`wiki/topics/Swine-herd-evaluation-and-field-investigation.md`。
- 已落库规则页：RULE-001 至 RULE-005。
- 已落库正式事实：20 条，均为 `HUMAN_REVIEWED`，均锚定 `SRC-0003; Chapter 1 Herd Evaluation; PDF page xx`。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_001_cross_review.md`。
- 当前截至位置：PDF page 40。下一批从 PDF page 41 开始。

### Formal Batch 001 具体实施说明

1. PDF page 13-24 仅用于来源元数据建档，生成 `SRC-0002`。该范围包含 Contributors、Editors' Note 和 Acknowledgments，不进入疾病、药方、诊断、治疗或监管 facts。
2. PDF page 25-40 用于正式构建 Chapter 1 Herd Evaluation，生成 `SRC-0003`、1 个猪群评估 topic 页、5 个规则页和 20 条正式 facts。
3. 所有正式 facts 先写入 `issues/formal_batch_001_candidate_facts.json`，再通过 `issues/formal_batch_001_cross_review.md` 的三层交叉审查后合并到 `exports/knowledge_facts.json`。
4. 三层交叉审查包括：页码锚点核验、内容边界核验、一致性核验。
5. 本批事实只覆盖猪群评估、记录核验、现场调查、采样选择、干预排序、口腔液样本提交等流程知识；Chapter 1 没有给出具体疾病药方，因此不构建药方或处方规则。
6. 验证命令已运行：`status`、`lint`、`query "猪群评估 急性 未治疗 采样 四圈评估"`、`graph-build`。
7. 验证结果：`fact_count=166`，其中 `HUMAN_REVIEWED=20`、`NEEDS_REVIEW=146`；`rule_count=5`；图谱更新为 `181 nodes / 405 links`；`lint ok=True`，无结构错误。



## Formal Batch 002 完成记录

- 完成时间：2026-05-06 16:45:00 +08:00。
- 处理范围：PDF page 41-65。
- 章节：Section I Veterinary Practice / Chapter 2 Behavior and Welfare。
- 已落库来源：SRC-0004。
- 已落库主题页：`wiki/topics/Swine-behavior-welfare-and-pain-management.md`。
- 已落库规则页：RULE-006 至 RULE-012。
- 已落库正式事实：25 条，均为 `HUMAN_REVIEWED`，均锚定 `SRC-0004; Chapter 2 Behavior and Welfare; PDF page xx`。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_002_cross_review.md`。
- 当前截至位置：PDF page 65。下一批从 PDF page 66 开始。

### Formal Batch 002 具体实施说明

1. PDF page 41-45 用于构建动物福利定义、评估框架、动物本体指标与资源指标 facts。
2. PDF page 46-49 涉及侵入性操作和疼痛研究；本批仅记录疼痛/证据边界，不落库药方或剂量。
3. PDF page 50-57 用于构建采食饮水、咬尾、belly nosing、跛行、疾病行为、护理栏和混群风险 facts。
4. PDF page 58-59 用于构建安乐死 protocol、失去知觉监测和 CO2 设备边界 facts。
5. PDF page 60-65 为参考文献页，只作为 Chapter 2 参考边界，不单独生成事实。
6. 所有正式 facts 先写入 `issues/formal_batch_002_candidate_facts.json`，通过 `issues/formal_batch_002_cross_review.md` 三层审查后合并到 `exports/knowledge_facts.json`。
7. 本批明确不构建处方、药物剂量、休药期、中国监管处置或具体疾病治疗方案。
8. 验证命令已运行：`status`、`lint`、`query "猪福利 咬尾 病弱猪 护理栏 安乐死"`、`graph-build`。
9. 验证结果：`fact_count=191`，其中 `HUMAN_REVIEWED=45`、`NEEDS_REVIEW=146`；`rule_count=12`；图谱更新为 `226 nodes / 455 links`；`lint ok=True`，无结构错误。



## Formal Batch 003 完成记录

- 完成时间：2026-05-06 16:55:00 +08:00。
- 处理范围：PDF page 66-98。
- 章节：Chapter 3 Genetics and Health；Chapter 4 Effect of Environment on Health；Chapter 5 Differential Diagnosis of Diseases。
- 已落库来源：SRC-0005、SRC-0006、SRC-0007。
- 已落库主题页：遗传健康、环境健康、按系统/年龄鉴别诊断 3 个 topic。
- 已落库规则页：RULE-013 至 RULE-021。
- 已落库正式事实：24 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_003_cross_review.md`。
- 验证命令：已运行 `status`、`lint`、`query "猪病 鉴别诊断 呼吸 繁殖损失 人兽共患"`、`graph-build`。
- 验证结果：`fact_count=215`，`disease_count=73`，`rule_count=21`；`HUMAN_REVIEWED=69`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `282 nodes / 503 links`。
- 当前截至位置：PDF page 98。下一批从 PDF page 99 开始。

### Formal Batch 003 具体实施说明

1. PDF page 66-73 用于构建遗传健康、疾病抵抗/耐受、基因组选择和母猪生产寿命边界。
2. PDF page 74-82 用于构建环境健康前置检查，包括温度、湿度、空间、水料和空气质量。
3. PDF page 83-98 用于构建按系统、年龄和临床表现组织的鉴别诊断导航。
4. 本批不将 Chapter 5 表格直接作为确诊依据，只作为鉴别诊断召回和导航依据。
5. 所有正式 facts 先写入 `issues/formal_batch_003_candidate_facts.json`，通过 `issues/formal_batch_003_cross_review.md` 三层审查后合并到 `exports/knowledge_facts.json`。



## Formal Batch 004 完成记录

- 完成时间：2026-05-06 17:09:00 +08:00。
- 处理范围：PDF page 99-121。
- 章节：Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。
- 已落库来源：SRC-0008。
- 已落库主题页：诊断测试选择与结果解释、实验室方法与性能边界 2 个 topic。
- 已落库规则页：RULE-022 至 RULE-029。
- 已落库正式事实：26 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_004_cross_review.md`。
- 验证命令：已运行 `status`、`lint`、`query "猪病 PCR 药敏 诊断测试 阳性 阴性 解释"`、`graph-build`。
- 验证结果：`fact_count=241`，`disease_count=73`，`rule_count=29`；`HUMAN_REVIEWED=95`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `343 nodes / 555 links`。
- 当前截至位置：PDF page 121。下一批从 PDF page 122 开始。

### Formal Batch 004 具体实施说明

1. PDF page 99-105 用于构建诊断解释总原则、AGID、细菌培养、MALDI-TOF、AST、bioassay、Brucella serology 和 clinical pathology 边界。
2. PDF page 106-110 用于构建 CF、EM、ELISA、FA、FMIA、HI、IHC、IFA/IPMA、MAT 的适用场景和限制。
3. PDF page 111-118 用于构建 ISH、寄生虫鉴定、PCR、qPCR、multiplex PCR、Sanger/NGS/nanopore sequencing 的解释边界。
4. PDF page 119-120 用于构建阴性状态、可疑阳性、复测、换靶标和采样计划的诊断策略。
5. PDF page 121 为参考文献页，只作为 Chapter 6 证据边界，不单独生成事实。



## Formal Batch 005 完成记录

- 完成时间：2026-05-06 17:14:00 +08:00。
- 处理范围：PDF page 122-146。
- 章节：Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value；Chapter 8 Collecting Evidence and Establishing Causality。
- 已落库来源：SRC-0009、SRC-0010。
- 已落库主题页：样本选择采集与提交、证据因果与监测解释 2 个 topic。
- 已落库规则页：RULE-030 至 RULE-041。
- 已落库正式事实：36 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_005_cross_review.md`。
- 验证命令：已运行 `status`、`lint`、`query "猪病 样本 采集 送检 因果 监测 阴性"`、`graph-build`。
- 验证结果：`fact_count=277`，`disease_count=73`，`rule_count=41`；`HUMAN_REVIEWED=131`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `429 nodes / 627 links`。
- 当前截至位置：PDF page 146。下一批从 PDF page 147 开始。

### Formal Batch 005 具体实施说明

1. PDF page 122-125 用于构建诊断问题、送检单信息、代表性动物选择、病程阶段和死前样本解释边界。
2. PDF page 125-135 用于构建尸检、组织固定、呼吸/败血症/腹泻/流产/CNS/关节采样和尸检安全边界。
3. PDF page 136-142 用于构建近因/终因、疾病诊断 vs 监测/监视、诊断流程、敏感性/特异性和串联/并联检测规则。
4. PDF page 143-146 用于构建全阴性监测解释、rule of three、cutoff、时间维度和过程改进边界。
5. 所有正式 facts 先写入 `issues/formal_batch_005_candidate_facts.json`，通过 `issues/formal_batch_005_cross_review.md` 三层审查后合并到 `exports/knowledge_facts.json`。



## Formal Batch 006 完成记录

- 完成时间：2026-05-06 17:21:00 +08:00。
- 处理范围：PDF page 147-181。
- 章节：Chapter 9 Disease Control, Prevention, and Elimination。
- 已落库来源：SRC-0011。
- 已落库主题页：疾病生态传播与控制框架、生物安全与风险管理 2 个 topic。
- 已落库规则页：RULE-042 至 RULE-055。
- 已落库正式事实：40 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、扑杀补偿、具体法定疫病处置方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_006_cross_review.md`。
- 验证命令：已运行 `status`、`lint`、`query "猪病 生物安全 传播 清除 引种 隔离 饲料 运输"`、`graph-build`。
- 验证结果：`fact_count=317`，`disease_count=73`，`rule_count=55`；`HUMAN_REVIEWED=171`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `523 nodes / 707 links`。
- 当前截至位置：PDF page 181。下一批从 PDF page 182 开始。

### Formal Batch 006 具体实施说明

1. PDF page 147-152 用于构建疾病生态、传播/暴露区别、疾病发生测量和疾病模式 facts。
2. PDF page 153-158 用于构建 vector-borne、short-cycle、long-cycle、resistant、commensal 病原控制边界。
3. PDF page 160-165 用于构建 BRM、HACCP、OIE 风险分析和跨层级生物安全框架。
4. PDF page 166-178 用于构建活体动物、隔离适应、运输、饲料、人流和循证生物安全原则。
5. PDF page 179-181 为参考文献页，只作为 Chapter 9 证据边界，不单独生成事实。

## Formal Batch 007 完成记录

- 完成时间：2026-05-06 17:56:16 +08:00。
- 处理范围：PDF page 182-220。
- 章节：Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis；Chapter 11 Anesthesia and Surgical Procedures in Swine。
- 已落库来源：SRC-0012、SRC-0013。
- 已落库主题页：猪用药治疗与抗菌药审慎使用、猪麻醉镇痛与手术决策边界；并将既有“猪用药合规、食品安全与休药期边界”升级为正式引用页。
- 已落库规则页：RULE-056 至 RULE-070。
- 已落库正式事实：45 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：具体药方、剂量、麻醉方案、手术步骤、具体休药期、禁限用药清单、中国监管处置。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_007_cross_review.md`。
- 验证命令：已运行 `status`、`lint`、`query "抗菌药 药敏 CLSI 休药期 恶性高热 CO2 去势 镇痛"`、`graph-build`。
- 验证结果：`fact_count=362`，`disease_count=73`，`rule_count=70`；`HUMAN_REVIEWED=216`，`NEEDS_REVIEW=146`；`lint ok=True`；图谱 `630 nodes / 797 links`。
- 当前截至位置：PDF page 220。下一批从 PDF page 221 开始。

### Formal Batch 007 具体实施说明

1. PDF page 182-194 用于构建猪用药治疗原则、抗菌药选择、药敏解释、给药路线、预防性抗菌用药、休药期边界、耐药风险和治疗失败复核 facts。
2. PDF page 195-220 用于构建猪麻醉镇痛边界、恶性高热风险、静脉通路、吸入麻醉监测、区域麻醉、仔猪处理疼痛管理和常见手术决策边界 facts。
3. 教材表格中的具体剂量、麻醉组合、手术步骤、美国法规和具体休药期均未转为可执行处方或操作规则。
4. 中国监管、禁限用药、批准标签、处方权限和休药期仍需 A0/A1 来源补强后才能进入生产答案约束。

## 当前完成状态

- 已创建猪病 Wiki 包：`knowledge/llm_wiki_swine_authoritative`
- 已完成 PDF 基础识别：总页数 1132，未加密，包含可读取书签目录
- 已处理页码：PDF page 1-220
- 当前截至位置：下一次从 PDF page 221 开始
- 已生成疾病/综合征/中毒条目：73 个
- 已生成目录级事实：146 条
- 已生成正式交叉审查事实：216 条
- 当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；216 条 Chapter 1-11 正式 facts 为 `HUMAN_REVIEWED`
- 当前来源页：`SRC-0001` 至 `SRC-0013`
- 当前规则页：`RULE-001` 至 `RULE-070`
- 当前图谱状态：已重建，`630 nodes / 797 links`
- 当前进度记录：`knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress.md`

注意：目录级病种覆盖仍不能直接当作完整临床知识或处方依据；只有通过候选事实、交叉审查和页码锚点核验的 `HUMAN_REVIEWED` facts 才能进入正式生成/评估约束。

## 现有鸡病架构复用点

猪病库复用以下鸡病 Wiki 能力：

- `init_wiki`：创建标准目录、根文件和 exports 文件
- `load_llm_wiki`：加载 Markdown 页面、facts、疾病索引、药物索引、规则索引
- `build_llm_wiki_context`：为生成和评估拼接 prompt-ready 证据上下文
- `build_wiki_audit_metadata`：输出 CSV 可追踪审计字段
- `lint_wiki`：检查必需文件、索引目标、证据状态、source id、wiki 双链
- `query_wiki`：按问诊问题召回相关 disease/topic/source/fact
- `rebuild_graph`：重建 `graph-data.json` 和 `knowledge-graph.html`
- `review_candidate_facts`：候选事实复核入口
- `run_daily_maintenance`：后续可用于自动发现权威来源，但正式事实仍需人工/规则复核

## Phase 1：知识库包初始化

已执行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative init --domain swine_disease
```

生成目录：

```text
knowledge/llm_wiki_swine_authoritative/
  index.md
  purpose.md
  .wiki-schema.md
  log.md
  raw/
  wiki/
    diseases/
    drugs/
    rules/
    rule_cards/
    sources/
    topics/
    syndromes/
    synthesis/
    comparisons/
    sessions/
    queries/
  exports/
    knowledge_facts.json
    disease_index.csv
    rule_index.csv
    drug_page_index.csv
  issues/
```

Phase 1 验收标准：

- `status` 能正常返回 wiki_dir、fact_count、disease_count
- `lint` 至少能完成结构检查
- `query` 能在无正式事实时保守返回

## Phase 2：目录级覆盖蓝图

本轮使用 PDF 书签和 Contents 页建立初始覆盖范围。处理范围：

- page 1：封面
- page 6：版权页
- page 7-12：目录页

已生成：

- 73 个 `wiki/diseases/DIS-xxx-*.md` 初始页
- 1 个 source 页：`SRC-0001-diseases-of-swine-11e-toc.md`
- 5 个 topic 初始工作流页
- `exports/disease_index.csv`
- `exports/knowledge_facts.json`
- `issues/pdf_processing_progress.md`

病种覆盖包括：

- 病毒病：非洲猪瘟、猪瘟、猪口蹄疫、猪繁殖与呼吸综合征、猪伪狂犬病、猪圆环病毒相关疾病、猪流行性腹泻、猪传染性胃肠炎、猪流感、猪细小病毒病、猪乙型脑炎、猪轮状病毒病、猪水疱性口炎等
- 细菌病：猪胸膜肺炎、猪萎缩性鼻炎、猪布鲁氏菌病、仔猪梭菌性肠炎、猪大肠杆菌病、仔猪黄白痢、仔猪水肿病、猪丹毒、副猪嗜血杆菌病、猪支原体肺炎、猪沙门氏菌病、猪链球菌病、猪痢疾等
- 寄生虫病：猪疥螨病、猪虱病、猪球虫病、猪弓形虫病、猪隐孢子虫病、猪蛔虫病、猪鞭虫病、猪后圆线虫病等
- 非感染性疾病：营养缺乏与过量、霉菌毒素中毒、黄曲霉毒素中毒、DON 中毒、玉米赤霉烯酮中毒、富马毒素中毒、矿物质与化学物中毒、有毒气体与通风失败损伤等

Phase 2 质量边界：

- 目录只能证明“章节存在、分类、起始页”，不能证明临床症状、诊断标准、治疗建议或休药期
- 所有目录级 facts 必须保持 `NEEDS_REVIEW`
- 法定疫病、重大动物疫病、强制扑杀/上报/封锁等内容必须补 A0/A1 来源

## PDF 分批识别方案

每批处理后必须更新：

- `issues/pdf_processing_progress.md`
- 对应 disease/topic/source 页面
- `exports/knowledge_facts.json`
- 必要时更新 `exports/disease_index.csv`

推荐批次：

```text
Batch 0: page 1-12
状态：已完成。用于目录级覆盖建模。

Batch 1: page 13-24
目标：贡献者、编辑说明、致谢。只记录来源元数据，不进入疾病事实。

Batch 2: page 25-244
目标：Veterinary Practice。
产物：采样、诊断测试、群体评估、疾病控制、药理、食品安全、人兽共患风险 topic/rule 页。

Batch 3: page 245-448
目标：Body Systems。
产物：消化、呼吸、繁殖、神经、皮肤、泌尿等 syndrome/topic 导航页。

Batch 4: page 449-766
目标：Viral Diseases。
产物：完善所有病毒病 disease 页，优先 core 病种。

Batch 5: page 767-1026
目标：Bacterial Diseases。
产物：完善所有细菌病 disease 页，补鉴别诊断和实验室确认。

Batch 6: page 1027-1064
目标：Parasitic Diseases。
产物：完善寄生虫 disease 页和驱虫规则候选页。

Batch 7: page 1065-1111
目标：Noninfectious Diseases。
产物：完善营养、中毒、环境管理 disease/syndrome 页。

Batch 8: page 1112-1132
目标：Index。
产物：补充英文别名、缩写、病原名、同义词和交叉引用。
```

正文抽取时建议每批再按 20-40 页分片，尤其是病毒病和细菌病章节。每个分片输出：

```json
{
  "pdf_page_start": 449,
  "pdf_page_end": 488,
  "chapters": ["Overview of Viruses", "Adenoviruses", "African Swine Fever Virus"],
  "updated_pages": [],
  "new_facts": [],
  "needs_review": [],
  "next_page": 489
}
```

## 疾病页正文抽取模板

每个 disease 页最终应补齐：

```markdown
## 病原与分类
## 中国监管状态
## 典型宿主与阶段
## 传播途径
## 临床症状
## 剖检变化
## 实验室诊断
## 鉴别诊断
## 防控要点
## 用药/处置边界
## 本地证据
## 当前可用性边界
```

每条可用于生成金标答案的事实必须有：

- `fact_id`
- `fact_type`
- `subject`
- `predicate`
- `object`
- `fact_confidence`
- `evidence_source_id`
- `evidence_status`
- `applies_to_species: swine`
- `jurisdiction`

## 权威来源补强计划

教材不是监管来源。以下类别必须额外补来源：

- 中国动物疫病病种名录
- 非洲猪瘟、口蹄疫、猪瘟、布鲁氏菌病、狂犬病、钩端螺旋体病等监管/人兽共患边界
- 中国国家标准、行业标准、诊断技术规范
- 农业农村部防控、净化、疫情处置文件
- WOAH disease pages、Terrestrial Manual、Terrestrial Code
- 兽药典、兽药标签、禁限用药、休药期文件

来源等级建议：

```text
A0: 中国官方法律法规、公告、国家标准、行业标准
A1: WOAH / FAO / 官方国际组织
A2: 教材、Merck Veterinary Manual、大学兽医学院资料
A3: 论文、综述、现场笔记
```

监管和用药相关 facts 只有 A0/A1 支撑时才能进入生产答案约束。

## 接入生成和评估系统

最小接入方式：新增 `config.local.json` 覆盖 Wiki 路径。

```json
{
  "project_name": "猪病问诊黄金数据集构建系统",
  "rule_base": {
    "enabled": true,
    "knowledge_base_file": "knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts.json",
    "references_file": "knowledge/llm_wiki_swine_authoritative/index.md",
    "llm_wiki_index_file": "knowledge/llm_wiki_swine_authoritative/exports/disease_index.csv",
    "llm_wiki_dir": "knowledge/llm_wiki_swine_authoritative"
  },
  "output": {
    "result_csv": "results/swine_disease_dataset_{timestamp}.csv",
    "pilot_summary_csv": "results/swine_pilot_model_comparison_{timestamp}.csv"
  }
}
```

建议后续把当前代码中的鸡病命名泛化：

- `common_chicken_diseases` 增加兼容别名 `common_diseases`
- 默认 `species: 鸡` 改成配置项 `domain.species_zh`
- 输出文件前缀改成配置项 `output.dataset_prefix`
- CLI 标题从 chicken 改为 veterinary/swine 可配置
- DeepEval prompt 中的“鸡病专家”改成领域配置

## 验证命令

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "非洲猪瘟 高热 出血 PCR 鉴别诊断" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

接入后小样本验证：

```powershell
python main.py --mode pilot --samples 10 --parallel 2 --evaluation-mode legacy
python main.py --mode pilot --samples 30 --parallel 4 --evaluation-mode legacy
python main.py --mode production --samples 100 --parallel 4 --evaluation-mode legacy
```

## 验收标准

Phase 1/2：

- `disease_count >= 70`
- `fact_count >= 140`
- `wiki/sources/SRC-0001...` 存在
- `issues/pdf_processing_progress.md` 记录当前截至 page 12
- query 能召回猪病页面

正文抽取完成后：

- core 病种均有病原、症状、剖检、实验室诊断、鉴别诊断、防控边界
- 法定疫病均有 A0/A1 监管来源
- 禁限用药、休药期、食品安全风险均有规则页
- `lint --strict` 仅保留可解释的 `NEEDS_REVIEW` 警告
- 生成样本 CSV 中 `wiki_evidence_source_ids` 非空
- 目标病种一致性门禁通过

## 下一次工作入口

从 `knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress.md` 读取当前截至位置。

当前截至：PDF page 220。

下一批建议处理：PDF page 221-244。

## 后续待处理阶段

- PDF page 221-234：Chapter 12 Preharvest Food Safety, Zoonotic Diseases, and the Human Health Interface。
- PDF page 235-244：Chapter 13 Special Considerations for Show and Pet Pigs。
- PDF page 245-448：Section II Body Systems。
- PDF page 449-766：Section III Viral Diseases。
- PDF page 767-1026：Section IV Bacterial Diseases。
- PDF page 1027-1064：Section V Parasitic Diseases。
- PDF page 1065-1111：Section VI Noninfectious Diseases。
- PDF page 1112-1132：Index。
