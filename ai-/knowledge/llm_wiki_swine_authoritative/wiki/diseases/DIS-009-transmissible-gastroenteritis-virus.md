---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-009
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-BANNED-DRUG-250-POLICY, A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0008, SRC-0009, SRC-0012, SRC-0036, SRC-0037, SRC-0087, SRC-0088, SRC-0089]
---

# 猪传染性胃肠炎

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime low-risk cleanup / Phase 9

- Runtime role: compact disease page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`.
- Moved fact-like rows: 28; moved candidate facts: 2.
- Detailed evidence moved in Phase 9 is for audit, source lookup, manual review, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Transmissible gastroenteritis virus

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- 处于潜伏期、排毒期或可能携带状态的猪可传播 TGEV；感染猪粪便可经鞋靴、衣物、车辆、饲料等机械传播，冬季尤其需要严格消毒。`fact_id=TGEV-013-biosecurity-carriers-fomites; source_id=SRC-0037; anchor=Chapter 31 Coronaviruses continuation; PDF page 526`

### 临床症状

- 在易感猪群中，流行性 TGE 可快速传播并造成新生仔猪严重腹泻和高死亡风险；成年猪常因免疫状态不同而表现较轻或无症状。`fact_id=TGEV-001-epidemic-pattern; source_id=SRC-0036; anchor=Chapter 31 Coronaviruses opening; PDF page 516-517`
- TGEV 感染对新生仔猪更严重，较大日龄猪相对不易发生同等严重的肠绒毛萎缩和死亡。`fact_id=TGEV-003-age_susceptibility; source_id=SRC-0036; anchor=Chapter 31 Coronaviruses opening; PDF page 520`

### 剖检变化

- 当前事实支持 TGEV 严重度与新生仔猪肠绒毛萎缩和死亡相关；剖检描述应保留为肠绒毛萎缩方向，尚不足以展开完整肉眼病变清单。`fact_id=TGEV-003-age_susceptibility; source_id=SRC-0036; anchor=Chapter 31 Coronaviruses opening; PDF page 520`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-009-transmissible-gastroenteritis-virus/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-009-transmissible-gastroenteritis-virus/002-VTOP_V13_1.md`：VTOP_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-009-transmissible-gastroenteritis-virus/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-009-transmissible-gastroenteritis-virus/004-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-009-transmissible-gastroenteritis-virus/005-B-task.md`：B-task 核心栏目补强；sources: SRC-0036, SRC-0037。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-009-transmissible-gastroenteritis-virus/006-Dataset-QA-Reinforcement-V6.md`：Dataset QA Reinforcement / V6；sources: A0-MOA-BANNED-DRUG-250-POLICY, SRC-0008, SRC-0009, SRC-0012, SRC-0036, SRC-0037。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-009-transmissible-gastroenteritis-virus/007-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026, CMP-001, CMP-001-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-001-。
