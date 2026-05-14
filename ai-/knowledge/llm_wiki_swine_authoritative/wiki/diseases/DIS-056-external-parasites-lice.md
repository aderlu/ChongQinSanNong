---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-056
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0080, SRC-0087, SRC-0088]
---

# 猪虱病 / Haematopinus suis

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
- 本轮分析范围：`Chapter 65 External Parasites; raw/md/1000-1132.md`；本页保留 4 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：外寄生虫病。

## 病原/定位

- 猪虱 Haematopinus suis 为专性寄生虫，离开宿主通常只能存活 2-3 天，主要经直接接触传播。`fact_id=PARA-011-lice-obligate; source_id=SRC-0080; anchor=Chapter 65 External Parasites; PDF page 1033-1034`

## 传播和诊断

- 猪虱 Haematopinus suis 为专性寄生虫，离开宿主通常只能存活 2-3 天，主要经直接接触传播。`fact_id=PARA-011-lice-obligate; source_id=SRC-0080; anchor=Chapter 65 External Parasites; PDF page 1033-1034`
- 猪虱病诊断依靠在猪体发现虱或黏附在毛上的虫卵，需纳入瘙痒和皮肤损伤鉴别。`fact_id=PARA-012-lice-diagnosis; source_id=SRC-0080; anchor=Chapter 65 External Parasites; PDF page 1034`

## 防控和用药边界

- 教材外寄生虫药物表用于说明标签适应范围，不得直接转写为通用处方、剂量、疗程或中国休药期。`fact_id=PARA-008-mange-products-boundary; source_id=SRC-0080; anchor=Chapter 65 External Parasites; PDF page 1032`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-056-external-parasites-lice/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-056-external-parasites-lice/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-056-external-parasites-lice/003-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-056-external-parasites-lice/004-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-056-external-parasites-lice/005-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
