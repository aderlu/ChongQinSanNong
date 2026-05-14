---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-043
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0065, SRC-0087, SRC-0088]
---

# 猪丹毒 / Erysipelas

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
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
- 本轮分析范围：`Chapter 53 Erysipelas; raw/md/801-1000.md`；本页保留 8 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：细菌性败血症/皮肤/关节心内膜病。

## 病原/定位

- 猪丹毒在猪群中散发，但更严重和更普遍的暴发可按约十年间隔反复出现。`fact_id=ERYS-001-relevance; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 859`
- Erysipelothrix 人感染常为职业性皮肤感染 erysipeloid，不应与由链球菌引起的人丹毒混淆。`fact_id=ERYS-002-public-health; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 860`

## 传播和发病机制

- 猪丹毒杆菌可经皮肤擦伤或昆虫叮咬等机械媒介进入；无有效免疫应答时可在 24 小时内出现菌血症。`fact_id=ERYS-003-entry; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 861`
- 急性败血型猪丹毒早期可损伤毛细血管和小静脉，形成休克样全身性凝血病。`fact_id=ERYS-004-coagulopathy; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 861`

## 临床/剖检变化

- 急性猪丹毒近乎特征性的肉眼病变为多灶粉红至紫色、菱形、稍隆起皮肤病变。`fact_id=ERYS-005-rhomboid-lesions; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 862`
- 慢性或相关猪丹毒可见瓣膜性心内膜炎，表现为心瓣膜上增生性颗粒状赘生物，以二尖瓣常见。`fact_id=ERYS-006-endocarditis; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 863`

## 实验室诊断

- Erysipelothrix 分型可用血清型、RAPD、PFGE 等方法，但依赖特定抗血清、方法和实验室能力。`fact_id=ERYS-008-typing; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 865`

## 鉴别诊断

- 急性猪丹毒需与 Salmonella Choleraesuis、A. suis、App、H. parasuis、S. suis、CSFV、PDNS 等鉴别。`fact_id=ERYS-007-differential; source_id=SRC-0065; anchor=Chapter 53 Erysipelas; PDF page 864`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-043-erysipelas/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-043-erysipelas/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-043-erysipelas/003-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
