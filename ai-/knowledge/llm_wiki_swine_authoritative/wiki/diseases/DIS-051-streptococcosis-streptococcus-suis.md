---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-051
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026, A0-MOA-STREP-SUIS-CONTROL-2005, SRC-0001, SRC-0075, SRC-0076, SRC-0087, SRC-0088, SRC-0089, SRC-0090]
---

# 猪链球菌病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime low-risk cleanup / Phase 9

- Runtime role: compact disease page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`.
- Moved fact-like rows: 33; moved candidate facts: 3.
- Detailed evidence moved in Phase 9 is for audit, source lookup, manual review, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Streptococcosis / Streptococcus suis

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 传播途径、临床症状、剖检变化、实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：细菌病/脑膜炎/败血症
- 教材章节：Section IV Bacterial Diseases，Chapter 61
- 正文起始页：PDF page 958

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

## Authority Web Refresh / 2026-05-13

- This additive refresh supplements the existing local textbook and China A0 boundary sources with a Merck Veterinary Manual A2 page, using explicit `fact_id/source_id/anchor` metadata so the update can be audited and admitted into the `wiki-native` 主图谱.
- The refresh is limited to epidemiology, transmission, clinical pattern, lesion, diagnosis, differential diagnosis, and control boundaries. It does not authorize executable antimicrobial regimen, dose, route, withdrawal period, MRL, culling, movement-control, or jurisdiction-specific regulatory actions.

## 传播途径

- 临床健康猪可带有多个血清型的 `S. suis`，其上呼吸道尤其扁桃体可作为自然生态位。`fact_id=SSUIS-101-carrier-tonsil-and-colonization; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Epidemiology and Transmission`
- 仔猪可在分娩和哺乳过程中获得定植，保育期混群时亚临床带菌猪可成为同栏感染来源。`fact_id=SSUIS-102-transmission-colonization-mixing; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Epidemiology and Transmission`
- 猪群间传播可通过健康带菌猪的调运和混群发生；高毒力菌株进入易感猪群后可在断奶猪中引发临床病。`fact_id=SSUIS-103-herd-to-herd-carrier-movement; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Epidemiology and Transmission`

## 临床症状

- 猪链球菌病主要表现为败血症、猝死、脑膜炎、多发性关节炎和心内膜炎，最常见于断奶后仔猪。`fact_id=SSUIS-104-clinical-septicemia-meningitis-arthritis; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Clinical Findings`
- 早期可见发热、食欲下降、沉郁和游走性跛行；急性败血型病例可在缺乏明显前驱症状时死亡。`fact_id=SSUIS-105-early-clinical-signs-and-age-window; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Clinical Findings`

## 剖检变化

- 主要病变可见脑膜炎、关节炎、心内膜炎、纤维素性浆膜炎，以及脾大和点状出血等败血症表现。`fact_id=SSUIS-106-lesions-meningitis-serositis-septicemia; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Lesions`

## 实验室诊断

- 初步诊断应结合病史、临床表现、年龄和肉眼病变；确诊需有病原分离、分型，必要时辅以显微病理。`fact_id=SSUIS-107-diagnosis-history-culture-serotyping; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Diagnosis`
- 由于扁桃体和鼻腔是常见定植部位，单独从这些部位检出毒力株不能直接证明其为致病原因；相关分离株需 PCR 等方法确认真实 `S. suis` 身份。`fact_id=SSUIS-108-diagnosis-tonsil-nasal-boundary; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Diagnosis`

## 鉴别诊断

- 脑膜炎、败血症和多发性关节炎场景需与格拉瑟氏病、放线杆菌败血症、大肠杆菌、猪丹毒、沙门氏菌病及其他化脓性关节炎病原区分。`fact_id=SSUIS-109-differential-glaesser-actinobacillus-others; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Diagnosis`

## 防控要点

- 本次 A2 补充支持病例识别、鉴别诊断排序、实验室解释和评估打分；若问题进入药物执行、休药期、MRL、扑杀、报告、调运、屠宰和食品安全，仍必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应 A0/A1 来源。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。

## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: disease recall, evidence lookup, differential prompts, and boundary checks only; do not generate executable treatment, withdrawal-period, MRL, or regulatory conclusions without rule-card and source verification.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/002-VTOP_V13_1.md`：VTOP_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/004-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/005-RAU_1_200_V14.md`：RAU_1_200_V14；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/006-Formal-Batch-026-V4.md`：Formal Batch 026 / V4 正文抽取进展；sources: SRC-0075。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/007-Formal-Batch-027-V4.md`：Formal Batch 027 / V4 正文抽取进展；sources: SRC-0076。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/008-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-051-streptococcosis-streptococcus-suis/001-MOA-A0-Authority-Reinforcement-2026-05-08.md`：MOA A0 Authority Reinforcement / 2026-05-08；sources: A0-MOA-STREP-SUIS-CONTROL-2005。
