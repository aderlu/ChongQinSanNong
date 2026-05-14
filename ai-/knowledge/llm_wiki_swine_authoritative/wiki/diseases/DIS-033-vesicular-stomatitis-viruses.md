---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-033
updated: 2026-05-11T16:45:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [SRC-0001, SRC-0054, A0-USDA-APHIS-VS-2026]
---

# 猪水疱性口炎

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Vesicular stomatitis viruses

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- VSV 可通过动物间直接接触以及昆虫媒介的生物性或机械性传播；传播解释需结合病灶、媒介和地区流行情况。`fact_id=VS-004-transmission; source_id=SRC-0054; anchor=Chapter 45 Rhabdoviruses; PDF page 758`

### 临床症状

- 猪水疱性口炎临床上类似 FMD、SVD、猪水疱疹和 SVV，必须进行实验室鉴别。`fact_id=VS-001-differential; source_id=SRC-0054; anchor=Chapter 45 Rhabdoviruses; PDF page 757`

- 猪水疱性口炎临床上无法与 FMD、SVD、VES 或 SVV 区分，必须采集并提交诊断样本做实验室评估。（SRC-0054; Chapter 45 Rhabdoviruses; PDF page 759）

### 剖检变化

- 水疱性口炎水疱可见于口腔黏膜、鼻镜、乳头和蹄冠带，并可在形成后 1-2 天破裂，释放富含病毒的渗出物。`fact_id=VS-006-lesions; source_id=SRC-0054; anchor=Chapter 45 Rhabdoviruses; PDF page 759`

### 鉴别诊断

- 猪水疱性口炎临床上类似 FMD、SVD、猪水疱疹和 SVV，必须进行实验室鉴别。（SRC-0054; Chapter 45 Rhabdoviruses; PDF page 757）

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：病毒病/水疱病鉴别
- 教材章节：Section III Viral Diseases，Chapter 45
- 正文起始页：PDF page 757

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-033-vesicular-stomatitis-viruses/001-Formal-Batch-021-V3.md`：Formal Batch 021 / V3 正文抽取进展；sources: SRC-0054。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-033-vesicular-stomatitis-viruses/002-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: SRC-0054。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-033-vesicular-stomatitis-viruses/003-B-task.md`：B-task 核心栏目补强；sources: SRC-0054。

## Web Access official source ingest / 2026-05-11

### Source

- `A0-USDA-APHIS-VS-2026`: https://www.aphis.usda.gov/livestock-poultry-disease/cattle/vesicular-stomatitis
- Authority: USDA APHIS official disease alert; official domain confirmed through Web Access.
- Last modified on source page: 2026-05-08

### Facts

- `DIS033-WEB-001-aphis-swine-host-boundary`
- `DIS033-WEB-002-aphis-vector-transmission`
- `DIS033-WEB-003-aphis-lesion-sites`
- `DIS033-WEB-004-aphis-us-reporting-boundary`
- `DIS033-WEB-005-aphis-movement-trade-impact`

### Governance boundary

- Do not convert APHIS U.S. reporting language into China-specific regulatory action.
- Do not generate treatment, dose, course, withdrawal period, MRL, residue, or food-safety conclusions from this source.
- Do not treat the page as laboratory-confirmation guidance or a substitute for veterinary diagnosis.

- This update adds source-anchored host, transmission, lesion, U.S. reporting-boundary, and movement/trade impact facts only.
- It does not add treatment, dose, course, withdrawal period, MRL, residue, food-safety, China-specific reporting, quarantine, culling, or movement-control conclusions.
