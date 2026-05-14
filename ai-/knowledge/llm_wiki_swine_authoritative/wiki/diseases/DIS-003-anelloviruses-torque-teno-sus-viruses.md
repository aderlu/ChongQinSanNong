---
tags: [disease, swine, cleaned_v13_2, partial_evidence_page]
disease_id: DIS-003
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: partial
usage_scope: [retrieval, regulatory_boundary, treatment_boundary, gap_routing]
sources: [A0-MOA-BANNED-DRUG-250-POLICY, RC-ALIAS-001, RC-CITATION-001, RC-TRAIN-READY-001, SRC-0001, SRC-0008, SRC-0009, SRC-0012, SRC-0032, SRC-0083]
---

# 猪环曲病毒托克特诺病毒感染

## Partial page gap-routing / Phase 9

- RC-PARTIAL-GAP-ROUTING-001: This page is a controlled partial runtime page for recall, differential routing, and gap tracking.
- Missing facets must not be inferred, completed, or converted into diagnosis, treatment, dose, withdrawal-period, MRL, residue, or regulatory conclusions.
- If a requested answer depends on absent facets, route to higher-evidence disease pages, rule cards, source expansion, or current official/regulatory sources.
## Runtime disease guardrail anchors / Phase 5

- RC-PARTIAL-GAP-ROUTING-001: This page stays in partial retrieval mode for recall, differential routing, and gap tracking.
- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Anelloviruses / Torque teno sus viruses

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- TTSuV 可在组织、血液、精液、初乳、鼻腔和粪便样本中检出，提示存在水平和垂直传播可能（`SRC-0083`, PDF page 478）。
- TTSuV 在血清和鼻腔排出物中的检出率随日龄增加，提示传播效率较高（`SRC-0083`, PDF page 478）。

### 临床症状

- 目前没有特异性临床症状可归因于 TTSuV 感染，健康猪中也可高比例检出（`SRC-0083`, PDF page 478-479）。
- TTSuV 与 PCV2 系统性疾病、PDNS 样病变、增重下降和肺炎等关联仍具争议，不能把 TTSuV 单独检出作为定因（`SRC-0083`, PDF page 479）。

### 剖检变化

- 无菌 TTSuV1 组织匀浆接种试验可见轻度间质性肺炎、短暂胸腺萎缩、膜性肾小球肾病和轻度肝淋巴细胞/组织细胞浸润；但常规猪临床病理实验资料缺乏（`SRC-0083`, PDF page 479）。

### 实验室诊断

- TTSuV 尚无已描述的病毒分离方案，诊断主要基于病毒 DNA 或抗体检测（`SRC-0083`, PDF page 479）。
- PCR/qPCR 与 ELISA 方法主要用于研究，教材称无商业化检测方法可用（`SRC-0083`, PDF page 479）。

### 鉴别诊断

- TTSuV 是否作为 PCV2 系统性疾病的协同因子仍未确定，需要与 PCV2 相关疾病和共感染解释分开（`SRC-0083`, PDF page 479）。

### 防控要点

- TTSuV 感染对猪群健康的影响和防控后果尚未建立，不能生成固定免疫、净化或用药程序（`SRC-0083`, PDF page 479）。

## 病原与分类

- 初始分类：病毒病
- 教材章节：Section III Viral Diseases，Chapter 26
- 正文起始页：PDF page 477

## 监管/执行性处置边界

- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。
- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。
- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。

## 典型宿主与阶段

- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。

## 用药/处置边界

- 本页无教材支持的特异治疗方案。
- 不得将 TTSuV 检出生成抗菌药、抗病毒药、固定免疫、净化、扑杀、封锁或跨区调运结论。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。
- [SRC-0083](../sources/SRC-0083-diseases-of-swine-11e-chapter-26-anelloviruses.md) - Chapter 26 Anelloviruses 正文补全，PDF page 478-479）

## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: retrieval, recall, differential routing, and gap tracking only; absent facets must not be inferred.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-003-anelloviruses-torque-teno-sus-viruses/001-DOS_1_200_REVIEW_REINFORCEMENT.md`：DOS_1_200_REVIEW_REINFORCEMENT；sources: SRC-0003, SRC-0007, SRC-0008, SRC-0009, SRC-0010, SRC-0011, SRC-0012, SRC-0014。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-003-anelloviruses-torque-teno-sus-viruses/002-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-003-anelloviruses-torque-teno-sus-viruses/003-Low-Frequency-Virus-QA-Reinforcement-V7.md`：Low Frequency Virus QA Reinforcement / V7；sources: A0-MOA-BANNED-DRUG-250-POLICY, SRC-0008, SRC-0009, SRC-0012, SRC-0032。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-003-anelloviruses-torque-teno-sus-viruses/001-Dataset-Alias-and-Causality-Boundary-V7.md`：Dataset Alias and Causality Boundary / V7；sources: RC-ALIAS-001, RC-CITATION-001, RC-TRAIN-READY-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-003-anelloviruses-torque-teno-sus-viruses/001-Targeted-Disease-Completion-V5---Chapter-26-Anelloviruses.md`：Targeted Disease Completion / V5 - Chapter 26 Anelloviruses；sources: SRC-0083。
