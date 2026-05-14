---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-007
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-573, SRC-0001, SRC-0035, SRC-0087, SRC-0088, SRC-0089]
---

# 猪圆环病毒相关疾病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Circoviruses / PCVAD

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- PCV1 和 PCV2 在家猪和野猪中普遍存在，野猪和家猪来源毒株可高度相似；该事实提示宿主群间生态联系，但不能单独替代具体传播链证据。`fact_id=PCV-009-ubiquity; source_id=SRC-0035; anchor=Chapter 30 Circoviruses; PDF page 499`

### 临床症状

- PCV2 普遍存在且多数感染为亚临床，现场中仅部分感染猪发展为 PCV2-SD，常见于约 2-4 月龄阶段。`fact_id=PCV-012-subclinical-common; source_id=SRC-0035; anchor=Chapter 30 Circoviruses; PDF page 502`
- PCV2-SD 临床受影响猪可表现消瘦、生长不良、苍白、呼吸或消化症状，并常伴淋巴结改变。`fact_id=PCV-013-pcv2-sd-clinical-signs; source_id=SRC-0035; anchor=Chapter 30 Circoviruses; PDF page 502`

### 剖检变化

- PCV2-SD 主要病变位于淋巴组织，早期可见淋巴结肿大，后期可见正常大小或萎缩淋巴结，组织学上需关注淋巴细胞减少和组织细胞浸润。`fact_id=PCV-015-pcv2-sd-lymphoid-lesions; source_id=SRC-0035; anchor=Chapter 30 Circoviruses; PDF page 502-503`
- PDNS 通常同时有皮肤和肾脏病变，急性死亡猪可见双侧肾肿大、皮质细小红点和肾盂水肿，组织学可见纤维素坏死性肾小球炎和系统性血管炎。`fact_id=PCV-020-pdns-lesions; source_id=SRC-0035; anchor=Chapter 30 Circoviruses; PDF page 505`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：病毒病
- 教材章节：Section III Viral Diseases，Chapter 30
- 正文起始页：PDF page 497

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-007-circoviruses-pcvad/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-007-circoviruses-pcvad/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-007-circoviruses-pcvad/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-007-circoviruses-pcvad/004-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: A0-MOA-573。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-007-circoviruses-pcvad/005-B-task.md`：B-task 核心栏目补强；sources: SRC-0035。
