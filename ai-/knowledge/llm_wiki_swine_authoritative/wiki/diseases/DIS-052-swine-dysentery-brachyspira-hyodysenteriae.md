---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-052
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0077, SRC-0087, SRC-0088, SRC-0089, SRC-0090]
---

# 猪痢疾 / Brachyspira hyodysenteriae

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime core compaction / Phase 7

- Runtime role: compact disease boundary page for retrieval, differential diagnosis routing, prevention/control framing, and evaluation checks.
- Phase 7 moved high-density batch evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`.
- Moved fact-like rows: 44; moved candidate facts: 12.
- `RC-DX-001`: Diagnosis must remain evidence-routed and distinguish suspicion, sample, method, pathogen detection, causality, and differential diagnosis.
- `RC-DISEASE-REGULATORY-001`: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- `RC-DRUG-001`: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- Expansion files under `wiki/evidence_expansions/diseases/phase7/` are for audit, source lookup, and manual review, not default production retrieval.

## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: disease recall, evidence lookup, differential prompts, and boundary checks only; do not generate executable treatment, withdrawal-period, MRL, or regulatory conclusions without rule-card and source verification.
## Raw MD cleanup / 2026-05-09

- 本页由 `raw/md` 中《Diseases of Swine, 11th Edition》对应章节重新整理，替换旧页面中的 mojibake/乱码补强块。
- 本轮分析范围：`Chapter 62 Swine Dysentery and Brachyspiral Colitis; raw/md/801-1000.md`；本页保留 17 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：细菌性大肠炎/腹泻。

## 病原/定位

- 猪 Brachyspira 相关疾病包括强溶血种导致的严重黏液出血性猪痢疾，以及弱溶血种导致的较轻 Brachyspira 结肠炎。`fact_id=BRACH-001-overview; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 975`
- 猪痢疾不仅由 B. hyodysenteriae 引起，强 β 溶血的 B. hampsonii 和 B. suanatina 也可致病。`fact_id=SD-001-strong-hemolysis; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 977`
- 7 个 Brachyspira 种可定植猪，其中 B. hyodysenteriae、B. hampsonii 和 B. pilosicoli 是常见致病种。`fact_id=BRACH-003-seven-species; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 975`

## 传播途径

- 猪痢疾在感染猪场主要通过摄入含螺旋体的粪便传播，连续流和生物安全差会增加风险。`fact_id=SD-003-fecal-oral; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 979`
- 猪痢疾康复的无症状猪可向易感猪传播至少 70 天。`fact_id=SD-004-carrier-70-days; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 979`
- B. hyodysenteriae 在湿粪中相对耐受，干燥可迅速杀灭，环境控制需重视湿粪和有机物。`fact_id=SD-005-moist-survival; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 979`

## 临床症状

- 猪痢疾主要发生于生长育肥猪，表现为软便进展到含血、黏液和黏液纤维素渗出物的水样痢疾。`fact_id=SD-007-clinical; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 980`

## 剖检变化

- 猪痢疾病变局限于盲肠、结肠和直肠，急性期可见大肠壁充血水肿、黏液、纤维素和血液。`fact_id=SD-008-large-intestine-lesions; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 980`

## 实验室诊断

- 猪痢疾确诊需在典型痢疾和/或病变猪的结肠黏膜或粪便中确认强 β 溶血 Brachyspira spp.。`fact_id=BRACH-002-sd-definitive; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 975`
- Brachyspira 为生长缓慢的厌氧菌，容易被其他肠道厌氧菌覆盖，培养需选择性培养基。`fact_id=BRACH-004-culture-slow; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 976`
- 选择性厌氧培养可检出已知猪痢疾病原并提供溶血表型，应仍为猪痢疾检测、诊断和监测的重要组成。`fact_id=SD-009-culture-integral; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 982`

## 鉴别诊断

- 猪痢疾需与增生性肠病、沙门氏菌病、鞭虫病、胃溃疡/其他出血性疾病及 PIS/PCS 鉴别。`fact_id=SD-010-differential; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 982`
- 猪肠道螺旋体病/猪结肠螺旋体病（PIS/PCS）是由弱 β 溶血 B. pilosicoli 引起的 Brachyspira 结肠炎。`fact_id=PIS-001-definition; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 985`
- 临床正常猪也可排出 B. pilosicoli，粪便阳性本身不能确诊 PIS/PCS，需结合临床、病变和完整诊断。`fact_id=PIS-003-fecal-only-limit; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 989`

## 防控和用药边界

- 猪痢疾有效抗菌药选择有限，重要药物如 pleuromutilins 的耐药性正在增加，用药需基于 MIC 和法规标签。`fact_id=SD-011-amr; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 983`
- 全进全出、批次间清洁消毒、感染垫料处置、靴刷/脚浴、设备清洁和换防护服可降低猪痢疾再感染和传播。`fact_id=SD-012-aiao-cleaning; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 984`
- 鼠类可作为猪痢疾病原潜在储存宿主，鸟类、水禽和其他野生动物可机械传播感染材料。`fact_id=SD-013-rodent-wildlife; source_id=SRC-0077; anchor=Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 984`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-052-swine-dysentery-brachyspira-hyodysenteriae/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-052-swine-dysentery-brachyspira-hyodysenteriae/002-VTOP_V13_1.md`：VTOP_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-052-swine-dysentery-brachyspira-hyodysenteriae/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-052-swine-dysentery-brachyspira-hyodysenteriae/004-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
