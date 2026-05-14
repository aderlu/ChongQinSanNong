---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-008
updated: 2026-05-11T17:25:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-573, A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025, A0-MOA-BANNED-DRUG-250-POLICY, A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0008, SRC-0009, SRC-0012, SRC-0037, SRC-0087, SRC-0088, SRC-0089, A1-WOAH-PED, A1-USDA-APHIS-PED-TECH-NOTE-2023]
---

# 猪流行性腹泻

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime low-risk cleanup / Phase 9

- Runtime role: compact disease page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`.
- Moved fact-like rows: 17; moved candidate facts: 2.
- Detailed evidence moved in Phase 9 is for audit, source lookup, manual review, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Porcine epidemic diarrhea virus

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- PEDV 可通过连续窝仔在断奶时失去泌乳免疫而形成感染循环并地方性存在；野猪检出 PEDV 后，其维持和传播作用仍不明确。`fact_id=PEDV-004-endemic-cycle-lactogenic-immunity; source_id=SRC-0037; anchor=Chapter 31 Coronaviruses continuation; PDF page 529`
- PEDV 高度传染，预防病毒进入需严格卫生和生物安全；控制目标还包括促进母猪群形成泌乳免疫以降低哺乳仔猪风险。`fact_id=PEDV-012-control-biosecurity-sanitation; source_id=SRC-0037; anchor=Chapter 31 Coronaviruses continuation; PDF page 534`

### 临床症状

- PED 与 TGE 共享水样腹泻、呕吐、厌食和沉郁等临床特征，繁殖场各年龄猪均可发病，仔猪发病率可接近 100%。`fact_id=PEDV-007-clinical-pattern; source_id=SRC-0037; anchor=Chapter 31 Coronaviruses continuation; PDF page 532`

### 剖检变化

- PEDV 主要在小肠绒毛上皮细胞胞质内复制，造成肠细胞变性、绒毛高度降低和吸收不良；本条支持小肠绒毛/吸收不良方向，不能外推为全部剖检谱。`fact_id=PEDV-006-villous-enterocyte-tropism; source_id=SRC-0037; anchor=Chapter 31 Coronaviruses continuation; PDF page 530`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## MOA monitoring enrichment 2026-05-09

- 农业农村部 2021—2025 年主要家畜疫病专项调查将猪流行性腹泻纳入猪群主要疫病调查范围，用于了解流行状况和发展趋势，并提出动态预警及相关政策措施建议。`fact_id=MOA-MONITOR-LIVESTOCK-001; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件25 主要家畜疫病专项调查方案`
- 该专项调查包括每季度问卷调查、发病猪场组织/血清样品检测，以及临床健康猪群组织样品病原学检测；本条只支持流调/监测用途，不改变本页药物、处方、休药期或食品安全边界。`fact_id=MOA-MONITOR-LIVESTOCK-002,MOA-MONITOR-LIVESTOCK-003; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件25`

## 病原与分类

- 初始分类：病毒病
- 教材章节：Section III Viral Diseases，Chapter 31
- 正文起始页：PDF page 512

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/002-VTOP_V13_1.md`：VTOP_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/004-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: A0-MOA-573。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/005-B-task.md`：B-task 核心栏目补强；sources: SRC-0037。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/006-Dataset-QA-Reinforcement-V6.md`：Dataset QA Reinforcement / V6；sources: A0-MOA-573, A0-MOA-BANNED-DRUG-250-POLICY, SRC-0008, SRC-0009, SRC-0012, SRC-0037。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/007-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026, CMP-001, CMP-001-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-001-。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/001-Phase-2-Gold-Anchors-V8.md`：Phase 2 Gold Anchors / V8；sources: CMP-001-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0037。

## Web Access authority source ingest / 2026-05-11

### Sources

- `A1-WOAH-PED`: https://www.woah.org/en/disease/porcine-epidemic-diarrhoea/
- `A1-USDA-APHIS-PED-TECH-NOTE-2023`: https://www.aphis.usda.gov/sites/default/files/ped_tech_note.pdf

### Facts

- `DIS008-WEB-001-woah-nonzoonotic-coronavirus`
- `DIS008-WEB-002-woah-age-morbidity-mortality`
- `DIS008-WEB-003-woah-fecal-oral-biosecurity-early-detection`
- `DIS008-WEB-004-woah-clinical-similarity-no-specific-treatment`
- `DIS008-WEB-005-usda-lab-differentiation-from-tge`
- `DIS008-WEB-006-usda-fecal-oral-no-vector-reservoir`

### Governance boundary

- Do not generate China-specific reporting, quarantine, culling, movement-control, vaccination schedule, farm-closure, or market-access conclusions from WOAH or USDA pages alone.
- Do not convert no-treatment or secondary-infection wording into executable prescriptions, antimicrobial choices, dose, route, course, withdrawal period, MRL, residue, or food-safety conclusions.
- Do not diagnose PED from watery diarrhoea alone; clinical similarity to TGE and other porcine gastroenteritis requires laboratory-supported differentiation.

- This update adds source-anchored PED identity, non-zoonotic, susceptible-age, transmission, diagnostic-differential, early-detection, biosecurity, and treatment-boundary facts only.
- It does not add executable prescriptions, antimicrobial choices, dose, route, treatment course, withdrawal period, MRL, residue, food-safety, or China-specific regulatory execution conclusions.
- Detailed evidence is routed to `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-008-porcine-epidemic-diarrhea-virus/008-Web-Access-Authority-Reinforcement-2026-05-11.md`.
