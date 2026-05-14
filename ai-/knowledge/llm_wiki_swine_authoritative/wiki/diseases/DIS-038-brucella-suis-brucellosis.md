---
tags: [disease, swine, cleaned_v13_2, partial_evidence_page]
disease_id: DIS-038
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: partial
usage_scope: [retrieval, regulatory_boundary, treatment_boundary, gap_routing]
sources: [A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026, A2-CDC-BRUCELLOSIS, A1-WOAH-BRUCELLOSIS, A0-MOA-BRUCELLOSIS-2022-2026, A0-MOA-BRUCELLOSIS-KEY-POINTS-2023, A1-USDA-APHIS-SWINE-BRUCELLOSIS, RC-CITATION-001, RC-TRAIN-READY-001, SRC-0001, SRC-0060, SRC-0061]
---

# 猪布鲁氏菌病

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
- Brucella suis brucellosis

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 实验室诊断
- 细菌培养是确认猪布鲁氏菌病的确定性方法；淋巴结培养与血清学结合可提高解释质量。（SRC-0061; Chapter 50 Brucellosis; PDF page 809）
## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 传播途径、临床症状、剖检变化、鉴别诊断、防控要点
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## 病原与分类
- 初始分类：细菌病/繁殖障碍/人兽共患风险
- 教材章节：Section IV Bacterial Diseases，Chapter 50
- 正文起始页：PDF page 802

## 监管/执行性处置边界
- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。
## 典型宿主与阶段
- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。
## 用药/处置边界

- 待正文抽取和具体标签/等效来源复核；不以中国兽药来源作为唯一门槛。- 法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。
## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。
## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: retrieval, recall, differential routing, and gap tracking only; absent facets must not be inferred.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/001-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/002-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/003-DOS_1_200_REVIEW_REINFORCEMENT.md`：DOS_1_200_REVIEW_REINFORCEMENT；sources: SRC-0003, SRC-0007, SRC-0008, SRC-0009, SRC-0010, SRC-0011, SRC-0012, SRC-0014。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/004-Formal-Batch-022-V3.md`：Formal Batch 022 / V3 姝ｆ枃鎶藉彇杩涘睍；sources: SRC-0060。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/005-Formal-Batch-023-V3.md`：Formal Batch 023 / V3 姝ｆ枃鎶藉彇杩涘睍；sources: SRC-0061。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/006-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: SRC-0061。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/001-Zoonotic-Authority-Reinforcement-V7.md`：Zoonotic Authority Reinforcement / V7；sources: A1-USDA-APHIS-SWINE-BRUCELLOSIS, RC-CITATION-001, RC-TRAIN-READY-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/002-MOA-A0-Authority-Reinforcement-2026-05-08.md`：MOA A0 Authority Reinforcement / 2026-05-08；sources: A0-MOA-BRUCELLOSIS-2022-2026。

## Authority Web Refresh / 2026-05-12

> This additive refresh was produced through the guarded CRUD decision workflow. It strengthens source/fact anchors for swine brucellosis identity, reproductive signs, wild-swine exposure, zoonotic/public-health risk, WOAH listed-disease framing, and diagnostic/reporting boundaries. It does not replace China A0 animal-disease control sources and does not authorize local culling, movement, vaccination, slaughter, compensation, food-chain, drug, withdrawal-period, or MRL claims.

### Disease identity and swine clinical boundary

- USDA APHIS identifies swine brucellosis as an infectious disease caused by `Brucella suis`; the authority summary supports reproductive-loss patterns such as abortion, infertility and weak piglets, possible joint involvement with lameness, and human-exposure warning. `fact_id=DIS038-WEB-001-aphis-causation-reproductive-zoonotic; source_id=A1-USDA-APHIS-SWINE-BRUCELLOSIS; anchor=Disease Alert: Swine Brucellosis / disease identity and reproductive-loss pattern, accessed 2026-05-12`
- USDA APHIS states the disease was eliminated from US commercial swine in 2011 but remains present in wild swine; pigs exposed to feral swine are at risk. Suspected herd disease routes through an accredited veterinarian and US reportable-disease channels where applicable, not through model-generated execution orders. `fact_id=DIS038-WEB-002-aphis-wild-swine-and-report-routing; source_id=A1-USDA-APHIS-SWINE-BRUCELLOSIS; anchor=Disease Alert: Swine Brucellosis / wild swine reservoir and report-routing language, accessed 2026-05-12`

### WOAH and diagnostic boundary

- WOAH frames `B. suis` in swine as a listed brucellosis disease, describes reproductive failure/abortion with shedding in birth fluids and environmental persistence under cool moist conditions, and keeps confirmation tied to serology plus prescribed laboratory tests to isolate and identify the bacteria. `fact_id=DIS038-WEB-003-woah-listed-transmission-diagnostic; source_id=A1-WOAH-BRUCELLOSIS; anchor=WOAH Brucellosis / listed disease, transmission and diagnostic confirmation boundary, accessed 2026-05-12`

### Public-health exposure boundary

- CDC supports human-exposure boundaries for infected animals or contaminated animal products, including pigs and wild hogs, occupational animal/body-fluid exposure, hunting/meat-hide preparation, animal-vaccine accidents, and laboratory sample work. This source must not be used as the primary swine herd-control protocol. `fact_id=DIS038-WEB-004-cdc-occupational-public-health-boundary; source_id=A2-CDC-BRUCELLOSIS; anchor=About Brucellosis | CDC / exposure routes and occupational-hunting-laboratory boundary, accessed 2026-05-12`

### Enforcement boundary

- These A1/A2 authority sources strengthen retrieval, differential, diagnostic-boundary, report-routing, and public-health exposure answers only. China-specific reporting, quarantine, culling, movement, vaccination program, slaughter, compensation, food-chain release, drug dose, withdrawal period, and MRL claims must still route to current China A0/A1 sources and rule cards.

## Authority Web Refresh / 2026-05-13

> This additive refresh was produced through the guarded CRUD decision workflow using a source-anchored CFSPH factsheet PDF downloaded through the web-access workflow. It strengthens transmission, clinical-pattern, and zoonotic/public-health boundaries for swine brucellosis. It does not replace China A0 animal-disease control sources and does not authorize local reporting, culling, movement, vaccination, slaughter, compensation, food-chain, drug, withdrawal-period, or MRL claims.

### Transmission and exposure boundary

- The Iowa State CFSPH Brucella suis factsheet describes transmission through infected reproductive discharges, aborted fetuses, semen, contaminated environments, and exposure to feral or wild swine. This strengthens source-anchored transmission routing but does not create jurisdiction-free control orders. `fact_id=DIS038-WEB-005-cfsph-transmission-exposure; source_id=A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026; anchor=CFSPH Brucella suis factsheet PDF page 2-3 transmission and exposure section, accessed 2026-05-13`

### Clinical-pattern boundary

- The same factsheet supports a reproductive-loss pattern including abortion, infertility, stillbirth, weak piglets, and possible lameness/paralysis involvement, while keeping clinical suspicion separate from confirmation. `fact_id=DIS038-WEB-006-cfsph-clinical-pattern; source_id=A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026; anchor=CFSPH Brucella suis factsheet PDF page 3-4 clinical signs section, accessed 2026-05-13`

### Zoonotic/public-health boundary

- CFSPH also supports zoonotic risk from pigs and feral swine, including occupational and hunting-related exposure. This is a public-health exposure boundary, not a standalone herd-control, treatment, or local regulatory protocol. `fact_id=DIS038-WEB-007-cfsph-zoonotic-boundary; source_id=A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026; anchor=CFSPH Brucella suis factsheet PDF page 1-2 and 4-5 zoonotic and public-health sections, accessed 2026-05-13`

### Enforcement boundary

- These A2 facts strengthen retrieval, differential, clinical-boundary, and public-health exposure answers only. China-specific reporting, quarantine, culling, movement, vaccination program, slaughter, compensation, food-chain release, drug dose, withdrawal period, and MRL claims must still route to current China A0/A1 sources and rule cards.
