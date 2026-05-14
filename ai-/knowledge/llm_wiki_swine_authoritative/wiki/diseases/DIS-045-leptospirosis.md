---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-045
updated: 2026-05-11T12:45:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0008, SRC-0067, SRC-0068, SRC-0087, SRC-0088, A0-DIS045-LEPTO-WEB-01-573, A1-DIS045-LEPTO-WEB-02-LEPTOSPIROSIS-WOAH-WORLD-ORGANISATION-FOR-ANIMAL, A1-DIS045-LEPTO-WEB-03-WOAH-TERRESTRIAL-MANUAL-CHAPTER-LEPTOSPIROSIS, A0-DIS045-LEPTO-WEB-04-GB-T-45106-2024, A0-DIS045-LEPTO-WEB-05-WS-290-2008, A0-DIS045-LEPTO-WEB-06-2008-2]
---

# 猪钩端螺旋体病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Leptospirosis

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 临床症状

- 钩端螺旋体病是繁殖猪群繁殖损失原因之一，地方性猪群可缺乏明显临床病。（SRC-0067; Chapter 55 Leptospirosis; PDF page 878）
- 绝大多数猪钩端螺旋体感染为亚临床，幼龄仔猪和妊娠母猪最可能出现临床感染。（SRC-0067; Chapter 55 Leptospirosis; PDF page 882）

### 实验室诊断

- MAT 是猪钩端螺旋体病血清学参考试验之一，但单次读数诊断价值低，推荐间隔约 2 周的连续检测。（SRC-0008; Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation; PDF page 110）

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 传播途径、剖检变化、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：细菌病/繁殖障碍/人兽共患风险
- 教材章节：Section IV Bacterial Diseases，Chapter 55
- 正文起始页：PDF page 878

## 监管/执行性处置边界

- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。
- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。
- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。

## 典型宿主与阶段

- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。

## 用药/处置边界

- 待正文抽取和具体标签/等效来源复核；不以中国兽药来源作为唯一门槛。
- 法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。

## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: disease recall, evidence lookup, differential prompts, and boundary checks only; do not generate executable treatment, withdrawal-period, MRL, or regulatory conclusions without rule-card and source verification.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/003-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/004-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/005-Formal-Batch-024-V3.md`：Formal Batch 024 / V3 正文抽取进展；sources: SRC-0067。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/006-Formal-Batch-025-V3.md`：Formal Batch 025 / V3 正文抽取进展；sources: SRC-0068。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/007-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: SRC-0008, SRC-0067。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-045-leptospirosis/001-Phase-2-Gold-Anchors-V8.md`：Phase 2 Gold Anchors / V8；sources: CMP-004-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0067, SRC-0068。

## Web Access 官方来源入库 / 2026-05-11

### Sources

- `A0-DIS045-LEPTO-WEB-01-573`: https://www.moa.gov.cn/govpublic/xmsyj/202206/t20220629_6403635.htm
- `A1-DIS045-LEPTO-WEB-02-LEPTOSPIROSIS-WOAH-WORLD-ORGANISATION-FOR-ANIMAL`: https://www.woah.org/en/disease/leptospirosis/
- `A1-DIS045-LEPTO-WEB-03-WOAH-TERRESTRIAL-MANUAL-CHAPTER-LEPTOSPIROSIS`: https://www.woah.org/fileadmin/Home/eng/Health_standards/tahm/3.01.12_LEPTO.pdf
- `A0-DIS045-LEPTO-WEB-04-GB-T-45106-2024`: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=0BFBE42DA04B55D0BDC83933CAB0AD6F
- `A0-DIS045-LEPTO-WEB-05-WS-290-2008`: https://www.nhc.gov.cn/wjw/s9491/200801/38802.shtml
- `A0-DIS045-LEPTO-WEB-06-2008-2`: https://www.nhc.gov.cn/bgt/pw10803/200805/c5e6985f24844fbb9e6d675cdaf8b5d8.shtml

### Facts

- `DIS045-WEB-001-official-source`
- `DIS045-WEB-002-573-2008-1125-2011-1663-2013-1950`
- `DIS045-WEB-003-woah-leptospirosis`
- `DIS045-WEB-004-woah-terrestrial-manual-leptospirosis`
- `DIS045-WEB-005-gb-t-45106-2024-2024-12-31-2025-07-01`
- `DIS045-WEB-006-ws-290-2008-nhc-2008-01-16-2008-08-01`
- `DIS045-WEB-007-2008-2-ws-290-2008-2008-08-01`
- `DIS045-WEB-008-dis-045-mrl-mrl`

### 不得外推边界

- 不要把农业农村部动物疫病分类名录解释为疾病诊断标准、治疗方案或防控操作规范。
- 不要把 WOAH 疾病页面或 Terrestrial Manual 章节中的诊断/病原信息外推为中国法定防控要求。
- 不要把人间钩端螺旋体病诊断、防控资料直接外推为猪群诊断标准或养殖场处置规范。
- 不要从“钩端螺旋体病”疾病名称推断任何兽药 MRL；MRL 必须按药物活性成分、动物种属、组织/产品矩阵和标准版本逐项引用。
- 不要把公开标准检索入口替代为具体标准条款；只有打开并核验具体标准详情或全文后，才可抽取标准编号、发布日期、实施日期和条款。
- 不要将“多种动物共患病”理解为所有动物种属均有相同易感性、临床表现、流行病学意义或管理要求。

- 本次来源不得单独生成猪钩端螺旋体病治疗、剂量、疗程、休药期、MRL、食品安全、检疫、扑杀、调运或执行性监管结论，除非 raw evidence 中存在逐条可核验的官方原文支持。
