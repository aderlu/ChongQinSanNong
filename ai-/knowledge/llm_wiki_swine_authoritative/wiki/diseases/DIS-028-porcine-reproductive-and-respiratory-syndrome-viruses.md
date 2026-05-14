---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-028
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-573, A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025, A0-MOA-PRRS-CSF-GUIDANCE-2017, A2-MERCK-PRRS-2026, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0049, SRC-0050, SRC-0087, SRC-0088, SRC-0089, SRC-0090]
---

# 猪繁殖与呼吸综合征

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Porcine Reproductive and Respiratory Syndrome Viruses

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- PRRSV 感染猪可通过口鼻分泌物、乳汁等排毒，排毒水平和持续时间因毒株和个体而异。`fact_id=PRRSV-004-shedding; source_id=SRC-0049; anchor=Chapter 41 PRRSV opening; PDF page 712`
- PRRSV 可在精液中检出感染性病毒，存在经精液传播风险；公猪/精液监测需结合检测和病程。`fact_id=PRRSV-005-semen; source_id=SRC-0049; anchor=Chapter 41 PRRSV opening; PDF page 712-716`
- PRRSV 气溶胶传播受毒株、环境和距离影响，不能把所有场间传播都归因于空气传播。`fact_id=PRRSV-007-aerosol; source_id=SRC-0049; anchor=Chapter 41 PRRSV opening; PDF page 713-714`

### 临床症状

- PRRSV 临床表现从亚临床到严重暴发不等，受猪群免疫、毒株毒力和共感染影响。`fact_id=PRRSV-010-clinical-variable; source_id=SRC-0049; anchor=Chapter 41 PRRSV opening; PDF page 717-718`

### 剖检变化

- 当前选入事实主要锚定传播和临床变异性，未提供稳定剖检病变清单；本页剖检栏目仍需继续正文抽取，避免用综合征名称替代病理。`fact_id=PRRSV-010-clinical-variable; source_id=SRC-0049; anchor=Chapter 41 PRRSV opening; PDF page 717-718`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## MOA monitoring enrichment 2026-05-09

- 农业农村部 2021—2025 年国家动物疫病监测计划明确高致病性猪蓝耳病监测目的包括掌握流行情况、分析病毒遗传变异、发现传播风险因素和评估免疫效果。`fact_id=MOA-MONITOR-PRRS-001; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件10 高致病性猪蓝耳病监测计划`
- 重点监测对象包括种猪场、中小规模饲养场、交易市场、屠宰场和发生过疫情地区的猪；活体可采全血或扁桃体，屠宰场可采肺脏、扁桃体、颌下淋巴结，采用 RT-PCR 或实时 RT-PCR，血清学检测使用 ELISA。`fact_id=MOA-MONITOR-PRRS-002,MOA-MONITOR-PRRS-003; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件10`
- 病原学阳性解释需排除疫苗免疫阳性，阳性群体判定也需排除疫苗免疫阳性；不得把单次检测结果直接外推为完整因果或处置结论。`fact_id=MOA-MONITOR-PRRS-004; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件10`

## MOA authority enrichment 2026-05-07

- 农业部农医发〔2017〕10号通知依据《国家中长期动物疫病防治规划（2012-2020年）》，印发《国家高致病性猪蓝耳病防治指导意见（2017-2020年）》和《国家猪瘟防治指导意见（2017-2020年）》。`source_id=A0-MOA-PRRS-CSF-GUIDANCE-2017; source_page=https://www.moa.gov.cn/govpublic/SYJ/201703/t20170324_5537806.htm`
- 该通知的官方目标表述为有效控制和消灭高致病性猪蓝耳病、猪瘟；本条为 2017-2020 年阶段性防治指导来源，不能替代当前年度处置方案。`source_id=A0-MOA-PRRS-CSF-GUIDANCE-2017; attachment=raw/web/moa_batch_authority_pilot_20260507_v4/attachments/5fd8bfc17615_P020170324587295840632.ceb`

## 病原与分类

- 初始分类：病毒病
- 教材章节：Section III Viral Diseases，Chapter 41
- 正文起始页：PDF page 709

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/004-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: SRC-0090。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/005-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/006-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/007-Formal-Batch-021-V3.md`：Formal Batch 021 / V3 正文抽取进展；sources: SRC-0050。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/008-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: A0-MOA-573。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/009-B-task.md`：B-task 核心栏目补强；sources: SRC-0049。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses/010-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A2-MERCK-PRRS-2026, CMP-004, CMP-004-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-003-。
