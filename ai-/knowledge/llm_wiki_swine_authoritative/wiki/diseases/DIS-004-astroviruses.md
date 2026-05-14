---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-004
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-BANNED-DRUG-250-POLICY, RC-ALIAS-001, RC-CITATION-001, RC-TRAIN-READY-001, SRC-0001, SRC-0008, SRC-0009, SRC-0012, SRC-0032]
---

# 猪星状病毒感染

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Astroviruses

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- 猪星状病毒推测以粪口传播为主，但也曾在鼻拭子、血样和脑组织中检出，提示可能有肠外相关性；该条为边界性证据，不应写成已完整阐明的传播模型。`fact_id=PASTV-006-transmission-and-extraintestinal-detection; source_id=SRC-0032; anchor=Chapter 26 Anelloviruses and Chapter 27 Astroviruses opening; PDF page 482`

### 临床症状

- 猪星状病毒最初在腹泻粪便中通过电镜识别，并被推测可导致轻度自限性腹泻，但其在肠道或其他疾病中的因果作用仍不清楚。`fact_id=PASTV-001-causal-role-obscure; source_id=SRC-0032; anchor=Chapter 26 Anelloviruses and Chapter 27 Astroviruses opening; PDF page 481`
- 猪星状病毒与轻度腹泻和近年神经侵袭性疾病报告相关，但病原因果关系需结合共感染、组织病变和检测背景谨慎判断。`fact_id=PASTV-007-pathogenesis-complexity; source_id=SRC-0032; anchor=Chapter 26 Anelloviruses and Chapter 27 Astroviruses opening; PDF page 482`

### 剖检变化

- 当前可用事实仅支持“需结合组织病变和共感染背景判断”的边界描述，尚不足以生成本病固定剖检病变谱。`fact_id=PASTV-007-pathogenesis-complexity; source_id=SRC-0032; anchor=Chapter 26 Anelloviruses and Chapter 27 Astroviruses opening; PDF page 482`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类

- 初始分类：病毒病
- 教材章节：Section III Viral Diseases，Chapter 27
- 正文起始页：PDF page 481

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-004-astroviruses/001-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-004-astroviruses/002-B-task.md`：B-task 核心栏目补强；sources: SRC-0032。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-004-astroviruses/003-Low-Frequency-Virus-QA-Reinforcement-V7.md`：Low Frequency Virus QA Reinforcement / V7；sources: A0-MOA-BANNED-DRUG-250-POLICY, SRC-0008, SRC-0009, SRC-0012, SRC-0032。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-004-astroviruses/004-Web-Source-Reinforcement-V11-P1.md`：Web Source Reinforcement / V11 P1；sources: A2-SHIC-CFSPH-PORCINE-ASTROVIRUS-FACTSHEET, CMP-001, CMP-001-, CMP-002, CMP-002-, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-001-, SYN-002-。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-004-astroviruses/001-Dataset-Alias-and-Enteric-Differential-Boundary-V7.md`：Dataset Alias and Enteric Differential Boundary / V7；sources: RC-ALIAS-001, RC-CITATION-001, RC-TRAIN-READY-001。
