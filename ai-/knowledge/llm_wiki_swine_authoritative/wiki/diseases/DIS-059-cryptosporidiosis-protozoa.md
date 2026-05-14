---
tags: [disease, swine, cleaned_v13_2, partial_evidence_page]
disease_id: DIS-059
updated: 2026-05-12T23:55:00+08:00
source_trust: authoritative
evidence_coverage: partial
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gap_routing]
sources: [SRC-0001, SRC-0081, A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026, A2-CORNELL-AHDC-CRYPTOSPORIDIUM-PARASITOLOGY-2026, A2-IOWA-STATE-SWINE-PARASITOLOGY-2026, A2-IOWA-STATE-PARASITOLOGY-SERVICES-2026, RC-CITATION-001, RC-DX-001, RC-DRUG-001, RC-DISEASE-REGULATORY-001, RC-WITHDRAWAL-MRL-001]
---

# 猪隐孢子虫病

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
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
- Cryptosporidiosis / protozoa

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

## 病原与分类

- 猪隐孢子虫病属于由 Cryptosporidium spp. 引起的胃肠道原虫性寄生虫病；Merck 将 C. parvum、C. suis 和 C. scrofarum 列为猪中常见报道的种。`fact_id=DIS059-PATHOGEN-001; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Etiology and Epidemiology of Cryptosporidiosis / pigs paragraph, accessed 2026-05-12`
- 既有教材锚点将本病归入 Section V Parasitic Diseases, Chapter 66 Coccidia and Other Protozoa；正文起始页为 PDF page 1039。`fact_id=DIS059-PATHOGEN-002; source_id=SRC-0081; anchor=Chapter 66 Coccidia and Other Protozoa, PDF page 1039`

## 临床症状

- 猪中 C. parvum、C. suis 和 C. scrofarum 可见于 1 周龄至上市年龄；多数感染为亚临床，但可参与哺乳仔猪和断奶后仔猪的吸收不良性腹泻。`fact_id=DIS059-CLIN-001; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Etiology and Epidemiology of Cryptosporidiosis / pigs paragraph, accessed 2026-05-12`
- 隐孢子虫阳性结果不能自动等同于腹泻病因；猪群寄生虫学报告需结合临床问题并排除细菌、病毒、营养等其他鉴别诊断后解释。`fact_id=DIS059-CLIN-002; source_id=A2-IOWA-STATE-SWINE-PARASITOLOGY-2026; anchor=Considerations for interpretation of results, accessed 2026-05-12`

## 传播途径

- 感染来源是随粪便排出的、排出时即已孢子化并具有感染性的卵囊；传播可经直接接触、污染物/人员机械传播、环境污染以及饲料或饮水粪源性污染发生。`fact_id=DIS059-TRANS-001; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Transmission of Cryptosporidiosis, accessed 2026-05-12`
- Cryptosporidium parvum 不严格宿主特异，其他动物来源可通过饲料污染参与感染风险；因此猪场解释阳性结果时应同时核查环境、饲料和混合感染背景。`fact_id=DIS059-TRANS-002; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Transmission of Cryptosporidiosis / C parvum not host specific, accessed 2026-05-12`

## 实验室诊断

- Merck 列出的隐孢子虫检测方法包括抗酸染色粪涂片、粪便漂浮、ELISA、免疫层析侧流、直接免疫荧光和 PCR；这些方法用于检测卵囊、抗原或核酸。`fact_id=DIS059-DX-001; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Diagnosis of Cryptosporidiosis, accessed 2026-05-12`
- Cornell AHDC 将 Cryptosporidium ELISA 描述为粪便抗原检测，并与双离心浓缩漂浮法并行用于检测 Cryptosporidium 卵囊和其他粪便寄生虫。`fact_id=DIS059-DX-002; source_id=A2-CORNELL-AHDC-CRYPTOSPORIDIUM-PARASITOLOGY-2026; anchor=Cryptosporidium ELISA interpretation, accessed 2026-05-12`
- Iowa State 建议疑似 Giardia 或 Cryptosporidium 时同时提交未固定粪便和等量福尔马林固定粪便；粪便样本不得冷冻。`fact_id=DIS059-DX-003; source_id=A2-IOWA-STATE-PARASITOLOGY-SERVICES-2026; anchor=Parasitology Submission Guidelines, accessed 2026-05-12`

## 鉴别解释

- 猪群层面解释寄生虫检测结果时，必须先排除与当前临床症状相关的其他鉴别诊断；单个或少数个体的粪检不适合代表整个猪群状态。`fact_id=DIS059-DIFF-001; source_id=A2-IOWA-STATE-SWINE-PARASITOLOGY-2026; anchor=Considerations for interpretation of results, accessed 2026-05-12`
- Cornell AHDC 对 ELISA 与漂浮法结果不一致时要求按低水平排卵囊、假阳性或假阴性等可能性解释，并建议追加第二份样本复核。`fact_id=DIS059-DIFF-002; source_id=A2-CORNELL-AHDC-CRYPTOSPORIDIUM-PARASITOLOGY-2026; anchor=Cryptosporidium ELISA Positive/Flotation Negative and ELISA Negative/Flotation Positive interpretations, accessed 2026-05-12`

## 防控要点

- Merck 将严格卫生作为预防感染的核心措施，控制目标是消除或减少环境中 Cryptosporidium 卵囊污染。`fact_id=DIS059-CTRL-001; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Control / Key Points, accessed 2026-05-12`
- 隐孢子虫卵囊对多数消毒剂有抵抗力，可在凉爽潮湿环境中存活数月；控制方案不能只依赖普通消毒结论，需结合干燥、卫生、样本复核和环境污染管理。`fact_id=DIS059-CTRL-002; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Transmission of Cryptosporidiosis / oocyst resistance, accessed 2026-05-12`

## Evidence gaps

- 剖检变化仍未在本页形成 verified 语义边；如需用于剖检型黄金问答，应继续补充教材原文页码或诊断实验室病例资料。
- 本页已补充病原、临床症状、传播途径、实验室诊断、鉴别解释和防控要点的 source-anchored evidence units；缺失 facet 不得由模型自行补全。

## 监管/执行性处置边界

- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。
- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。
- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。

## 典型宿主与阶段

- Applies to species: swine
- 易感/检出阶段：Merck 明确列出猪从 1 周龄至上市年龄均有报道；临床相关性重点放在哺乳仔猪和断奶后仔猪腹泻背景中解释。`fact_id=DIS059-HOST-001; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Etiology and Epidemiology of Cryptosporidiosis / pigs paragraph, accessed 2026-05-12`

## 用药/处置边界

- Merck 对隐孢子虫病治疗的概括是支持疗法；本页不得生成具体药物、剂量、疗程、休药期或 MRL 结论。`fact_id=DIS059-DRUG-BOUNDARY-001; source_id=A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026; anchor=Treatment / Key Points, accessed 2026-05-12`
- 具体标签/等效来源仍需复核；法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。
- [SRC-0081](../sources/SRC-0081-diseases-of-swine-11e-chapter-66-coccidia-and-other-protozoa.md) - Diseases of Swine 11e, Chapter 66 Coccidia and Other Protozoa。
- [A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026](../sources/A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026.md) - Merck Veterinary Manual: Cryptosporidiosis in Animals。
- [A2-CORNELL-AHDC-CRYPTOSPORIDIUM-PARASITOLOGY-2026](../sources/A2-CORNELL-AHDC-CRYPTOSPORIDIUM-PARASITOLOGY-2026.md) - Cornell AHDC parasitology interpretation。
- [A2-IOWA-STATE-SWINE-PARASITOLOGY-2026](../sources/A2-IOWA-STATE-SWINE-PARASITOLOGY-2026.md) - Iowa State VDL swine parasitology interpretation。
- [A2-IOWA-STATE-PARASITOLOGY-SERVICES-2026](../sources/A2-IOWA-STATE-PARASITOLOGY-SERVICES-2026.md) - Iowa State parasitology sample submission guidance。

## source_trust / evidence_coverage / usage_scope

- source_trust: authoritative；本页新增来源均为兽医手册、大学兽医诊断实验室或兽医病理服务页面。
- evidence_coverage: partial；核心诊断、传播、防控和解释边界已补齐，但剖检变化仍需继续补充精确来源。
- usage_scope: retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gap_routing；黄金数据集只能使用 verified 且 source-anchored 的边。
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-059-cryptosporidiosis-protozoa/001-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-059-cryptosporidiosis-protozoa/002-DOS_1_200_REVIEW_REINFORCEMENT.md`：DOS_1_200_REVIEW_REINFORCEMENT；sources: SRC-0003, SRC-0007, SRC-0008, SRC-0009, SRC-0010, SRC-0011, SRC-0012, SRC-0014。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-059-cryptosporidiosis-protozoa/003-Formal-Batch-029-V4.md`：Formal Batch 029 / V4 姝ｆ枃鎶藉彇杩涘睍；sources: SRC-0081。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-059-cryptosporidiosis-protozoa/004-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: SRC-0081。
