---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-026
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A1-USDA-APHIS-FMD-NAHLN-2026, A1-USDA-APHIS-FMD-DISEASE-2026, A1-FAO-FMD-DISEASE-2026, A0-MOA-573, A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025, A0-MOA-FMD-CONTROL-GUIDE-2024, A0-MOA-FMD-EMERGENCY-DRAFT-2026, A0-MOA-FMD-REFERENCE-LAB-APPLICATION-2024, A2-MERCK-FMD-ANIMALS-2026, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0047, SRC-0048, SRC-0087, SRC-0088, SRC-0089]
---

# 猪口蹄疫

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime low-risk cleanup / Phase 9

- Runtime role: compact disease page after high/medium-risk cleanup; this page keeps the default retrieval core.
- Phase 9 moved low-risk high-density evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`.
- Moved fact-like rows: 37; moved candidate facts: 2.
- Detailed evidence moved in Phase 9 is for audit, source lookup, manual review, or evidence expansion, not default production retrieval.
- Existing disease, drug, withdrawal/MRL, regulatory, and synthesis guardrails still apply.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Foot-and-mouth disease / Picornaviruses

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- 人员可机械性传播 FMDV，因此人员流动和污染物控制是口蹄疫控制的重要考虑。`fact_id=FMDV-002-people-mechanical; source_id=SRC-0047; anchor=Chapter 40 Picornaviruses opening; PDF page 671-672`
- 猪可通过呼吸排出大量 FMDV 气溶胶，气溶胶传播受气象、距离和病毒云完整性影响。`fact_id=FMDV-004-aerosol-pigs; source_id=SRC-0047; anchor=Chapter 40 Picornaviruses opening; PDF page 673`

### 临床症状

- 猪口蹄疫临床病通常较重，疼痛和水疱性病变可明显影响行动和采食。`fact_id=FMDV-007-pig-clinical-severe; source_id=SRC-0047; anchor=Chapter 40 Picornaviruses opening; PDF page 677`

- 猪口蹄疫临床病通常较重，疼痛和水疱性病变可明显影响行动和采食。（SRC-0047; Chapter 40 Picornaviruses opening; PDF page 677）

### 剖检变化

- 现有事实明确支持疼痛和水疱性病变方向；FMD 临床诊断仍需与猪水疱病、水疱性口炎、Senecavirus A 和 vesivirus 感染等鉴别。`fact_id=FMDV-009-differential; source_id=SRC-0047; anchor=Chapter 40 Picornaviruses opening; PDF page 679`

## Evidence gaps

- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: 实验室诊断、鉴别诊断、防控要点.
- These gaps should route generation to topic pages, rule pages, textbook sources, or explicit requests for additional authority sources.

## MOA monitoring enrichment 2026-05-09

- 农业农村部 2021—2025 年国家动物疫病监测计划将口蹄疫监测对象列为猪、牛、羊、鹿等偶蹄类动物，监测目的包括掌握病原感染与分布、跟踪病毒变异、查找传播风险因素和评估免疫效果。`fact_id=MOA-MONITOR-FMD-001,MOA-MONITOR-FMD-002; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件3 口蹄疫监测计划`
- 发现偶蹄动物或野生动物出现水泡、跛行、烂蹄等类似口蹄疫症状时，应向当地畜牧兽医主管部门或动物疫病预防控制机构报告并采样监测；本条仅支持监测/报告触发边界，不替代正式疫情认定。`fact_id=MOA-MONITOR-FMD-003; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件3`
- 口蹄疫病原检测可对猪颌下淋巴结或扁桃体采用 RT-PCR 或实时 RT-PCR；阳性解释仍需遵守 `RC-DX-001` 和当前官方处置来源。`fact_id=MOA-MONITOR-FMD-004; source_id=A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025; anchor=附件3`

## MOA authority enrichment 2026-05-07

- 中国官方口蹄疫防控指南提示：国家口蹄疫参考实验室发现部分猪群中口蹄疫流行毒株发生变异；中东地区近年来流行的 SAT2 型口蹄疫病毒传入我国风险较高。`source_id=A0-MOA-FMD-CONTROL-GUIDE-2024; source_page=https://xmsyj.moa.gov.cn/zcjd/202404/t20240423_6454217.htm`
- 口蹄疫疫苗免疫是防控有效手段，但 7 个血清型之间无交叉免疫保护，同一血清型不同毒株抗原性也存在差异；当前猪群主要关注 O 型 CATHAY 拓扑型和 O 型 Mya-98 毒株。`source_id=A0-MOA-FMD-CONTROL-GUIDE-2024`
- 口蹄疫免疫群体中的发病畜应重点监测，阳性样品应送国家口蹄疫参考实验室进行病原分析；检测试剂选择需考虑敏感性、特异性和血清型交叉检出问题。`source_id=A0-MOA-FMD-CONTROL-GUIDE-2024`
- 2026 年版应急实施方案征求意见稿规定，发现疑似口蹄疫感染症状应立即报告，并按“可疑疫情-疑似疫情-确诊疫情”程序认定和报告；该条目前为征求意见稿证据，不能替代正式方案。`source_id=A0-MOA-FMD-EMERGENCY-DRAFT-2026; attachment=raw/web/moa_batch_authority_pilot_20260507_v4/attachments/d5ac1f3e6d46_P020260507566304703096.docx`
- 征求意见稿中，国内首次报告的新血清型疫情，以及疫区、受威胁区涉及两个以上省份的疫情，由农业农村部认定；一般受威胁区由疫区边缘向外延伸 10 公里，新血清型疫情可向外延伸 30 公里。`source_id=A0-MOA-FMD-EMERGENCY-DRAFT-2026`
- 国家口蹄疫专业实验室申报材料要求包括有效期内生物安全实验室认可证书及最近一次评审报告复印件；该证据仅用于实验室资质边界。`source_id=A0-MOA-FMD-REFERENCE-LAB-APPLICATION-2024; attachment=raw/web/moa_batch_authority_pilot_20260507_v4/attachments/17f351485d5e_P020241210336254873984.docx`

## 病原与分类

- 初始分类：病毒病
- 教材章节：Section III Viral Diseases，Chapter 40
- 正文起始页：PDF page 665

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
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/002-VTOP_V13_1.md`：VTOP_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: source anchors retained in expansion。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/004-Formal-Batch-019.md`：Formal Batch 019 正文抽取进展；sources: SRC-0047。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/005-Formal-Batch-020.md`：Formal Batch 020 正文抽取进展；sources: SRC-0048。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/006-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: A0-MOA-573, SRC-0047。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/007-B-task.md`：B-task 核心栏目补强；sources: SRC-0047。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/008-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A2-MERCK-FMD-ANIMALS-2026, CMP-005, CMP-005-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-006-。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-026-foot-and-mouth-disease-picornaviruses/009-Web-Source-Reinforcement-V11-P1-A0-A1-Refresh.md`：Web Source Reinforcement / V11 P1 A0/A1 Refresh；sources: A0-MOA-573, A0-MOA-FMD-CONTROL-GUIDE-2024, A1-WOAH-FMD-DISEASE, CMP-005, CMP-005-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, SYN-006-。

## Authority Web Refresh / 2026-05-11

> This additive refresh was produced through the guarded CRUD decision workflow. It adds international authority anchors for FMD impact, reporting, and diagnostic-preparedness boundaries. It does not replace China A0 control rules and does not authorize local culling, movement, vaccination, slaughter, food-chain, drug, withdrawal-period, or MRL claims.

### International disease and impact boundary

- FAO frames FMD as a highly contagious disease of cloven-hoofed animals including pigs; it is not a human-health threat but can severely affect food security, livelihoods, and trade. Broad control concepts include vaccination, movement controls, and biosecurity, but China-specific execution still requires A0 sources. `fact_id=DIS026-WEB-001-fao-fmd-impact-control; source_id=A1-FAO-FMD-DISEASE-2026`

### Reporting and subtype boundary

- USDA APHIS identifies pigs among FMD-affected cloven-hoofed animals, notes multiple virus types/subtypes with type-specific immunity, and directs suspected or diagnosed reportable animal diseases to animal-health officials. This supports reporting-boundary prompts, not jurisdiction-free execution orders. `fact_id=DIS026-WEB-002-usda-aphis-species-subtype-report; source_id=A1-USDA-APHIS-FMD-DISEASE-2026`

### Laboratory preparedness boundary

- USDA APHIS NAHLN states that there is not an active national FMD surveillance program in NAHLN laboratories, but FMD-approved laboratories maintain training and proficiency for preparedness; during a foreign animal disease investigation, duplicate samples may support preliminary screening while confirmatory testing follows official channels. `fact_id=DIS026-WEB-003-usda-nahln-fmd-preparedness; source_id=A1-USDA-APHIS-FMD-NAHLN-2026`

### Enforcement boundary

- These A1 sources strengthen international retrieval and diagnostic/reporting boundaries only. China-specific reporting, quarantine, culling, movement, vaccination program, slaughter, compensation, food-chain release, drug dose, withdrawal period, and MRL claims must still route to `A0-MOA-573`, `A0-MOA-FMD-CONTROL-GUIDE-2024`, `A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025`, current official implementation documents, and rule cards.
