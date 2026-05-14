---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-035
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, RULE-HANDBOOK-PRESCRIPTION-001, SRC-0058, SRC-0087, SRC-0088, SRC-0089, SRC-0090]
---

# 猪传染性胸膜肺炎 / Actinobacillus pleuropneumoniae

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime core compaction / Phase 7

- Runtime role: compact disease boundary page for retrieval, differential diagnosis routing, prevention/control framing, and evaluation checks.
- Phase 7 moved high-density batch evidence blocks out of default retrieval: `HANDBOOK_RX_V13_1`, `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`.
- Moved fact-like rows: 31; moved candidate facts: 12.
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
- 本轮分析范围：`Chapter 48 Actinobacillosis; raw/md/601-800.md`；本页保留 16 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：细菌性呼吸道疾病。

## 病原/定位

- 胸膜肺炎放线杆菌 App 是猪传染性胸膜肺炎的病原，NAD 依赖性和非依赖性生物型均需正确鉴别。`fact_id=APP-001-agent; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 773`
- App 血清型流行优势可随地区和年份显著变化，不能用单一地区血清型分布替代本地监测。`fact_id=APP-003-serotype-prevalence; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 775`

## 传播途径

- App 可在短距离经气溶胶传播，邻近猪舍间空气传播可能但不常见或依赖场景；不能泛化解释所有引入事件。`fact_id=APP-004-aerosol; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 776`
- 引入带菌猪是 App 进入猪群的重要风险，尤其在高健康状态或阴性种猪群中需重点防控。`fact_id=APP-005-carriers; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 776`

## 临床症状

- App 感染结局和暴发严重度受菌株毒力、M. hyopneumoniae、伪狂犬病病毒和可能的猪流感病毒等共同感染影响。`fact_id=APP-007-severity; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 778`
- App 急性病例可见发热、呼吸困难、咳嗽和张口呼吸；慢性病例可表现为间歇性咳嗽、采食下降和增重下降。`fact_id=APP-008-clinical; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 779`

## 剖检变化

- App 急性病变包括出血、坏死、易碎肺组织和纤维素性胸膜炎，慢性病例可形成胸膜粘连。`fact_id=APP-009-lesions; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 780`

## 实验室诊断

- App 与其他猪上呼吸道 Actinobacillus 种或 A. suis 可混淆，必要时需 species-specific PCR 或完整生化鉴定。`fact_id=APP-002-identification; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 774`
- 尿素酶阴性、非典型、肺内意外分离或不可分型 App 分离株需 species-specific PCR 或完整鉴定确认。`fact_id=APP-010-diagnosis-atypical; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 781`
- 临床健康扁桃体带菌猪检测复杂，在阴性猪群引种和可疑血清结果场景下尤其重要。`fact_id=APP-011-carrier-detection; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 782`
- ApxIV 血清学解释需考虑仅扁桃体带菌时抗体水平可能不高，以及部分菌株可能因插入序列不产生 ApxIV。`fact_id=APP-012-serology-boundary; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 783`

## 防控和用药边界

- 教材列举 App 体外敏感性资料，但不能转化为通用处方；治疗需结合药敏、法规、兽医诊断和给药场景。`fact_id=APP-013-treatment-boundary; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 784`
- 自然或疫苗诱导抗体不能消除动物扁桃体带菌状态；疫苗保护不能等同于清除携带。`fact_id=APP-014-vaccine-carrier; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 786`
- App 区域或育种金字塔控制涉及无胸膜肺炎猪群方案、血清监测、屠宰监测和病死猪剖检等组合措施。`fact_id=APP-015-eradication; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 786`

## 鉴别诊断

- A. suis 可在成年猪引起急性败血症，表现为沉郁、厌食、发热和类似猪丹毒的红色菱形皮肤病变。`fact_id=ASUIS-001-clinical; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 787`
- A. suis 败血症特别是在出现皮肤病变时可与猪丹毒混淆，需实验室鉴别。`fact_id=ASUIS-002-differential; source_id=SRC-0058; anchor=Chapter 48 Actinobacillosis; PDF page 787`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia/002-VTOP_V13_1.md`：VTOP_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia/003-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia/004-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia/005-RAU_1_200_V14.md`：RAU_1_200_V14；sources: RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-DX-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia/001-Handbook-enrichment-V13.md`：Handbook enrichment / V13；sources: RULE-HANDBOOK-PRESCRIPTION-001, SRC-0087。
