---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-060
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0082, SRC-0087, SRC-0088]
---

# 猪蛔虫病 / Ascaris suum

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
- 本轮分析范围：`Chapter 67 Internal Parasites; raw/md/1000-1132.md`；本页保留 7 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：内寄生虫病。

## 病原/定位

- 内寄生虫是全球猪生产常见问题，尽管有驱虫药，Ascaris suum 仍是最普遍的猪寄生虫之一。`fact_id=PARA-029-internal-parasites-common; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1052`
- Ascaris suum 因虫卵广泛存在而常见，成虫在剖检小肠中容易观察。`fact_id=PARA-032-ascaris-ubiquitous; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1055`

## 剖检/免疫影响

- 猪蛔虫病可由成虫或虫卵支持诊断，但肝脏 milk spots 需与肾虫移行相关纤维化等鉴别。`fact_id=PARA-033-ascaris-diagnosis; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1056`
- Ascaris 感染可能降低宿主对免疫或其他感染的反应，需作为生产性能和免疫反应解释的边界。`fact_id=PARA-034-ascaris-immune-effect; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1056`

## 实验室诊断

- 猪蛔虫病可由成虫或虫卵支持诊断，但肝脏 milk spots 需与肾虫移行相关纤维化等鉴别。`fact_id=PARA-033-ascaris-diagnosis; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1056`

## 防控和用药边界

- 在混凝土地面饲养可减少猪接触部分中间宿主和土壤传播寄生虫，从而降低多类内寄生虫感染。`fact_id=PARA-043-internal-control-concrete; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1062`
- 教材中驱虫药标签适应虫种和美国休药期信息不得跨法域泛化为中国处方或休药期。`fact_id=PARA-046-anthelmintic-boundary; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1063-1064`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-060-ascaris-suum-internal-parasites/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-060-ascaris-suum-internal-parasites/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-060-ascaris-suum-internal-parasites/003-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-060-ascaris-suum-internal-parasites/004-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
