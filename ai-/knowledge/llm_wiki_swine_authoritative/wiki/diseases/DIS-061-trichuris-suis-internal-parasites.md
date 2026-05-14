---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-061
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0082, SRC-0087, SRC-0088]
---

# 猪鞭虫病 / Trichuris suis

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
- 本轮分析范围：`Chapter 67 Internal Parasites; raw/md/1000-1132.md`；本页保留 5 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：内寄生虫性大肠炎。

## 病原/定位

- 猪鞭虫 Trichuris suis 寄生于盲肠和结肠，重度感染可导致结肠炎和腹泻。`fact_id=PARA-035-trichuris-colon; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1058-1059`

## 临床/剖检边界

- 猪鞭虫 Trichuris suis 寄生于盲肠和结肠，重度感染可导致结肠炎和腹泻。`fact_id=PARA-035-trichuris-colon; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1058-1059`

## 实验室诊断

- 发现成虫或典型虫卵可支持猪鞭虫病诊断，但低虫体负荷可能病变轻微，需结合临床。`fact_id=PARA-036-trichuris-diagnosis; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1059`

## 防控和用药边界

- 教材中驱虫药标签适应虫种和美国休药期信息不得跨法域泛化为中国处方或休药期。`fact_id=PARA-046-anthelmintic-boundary; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1063-1064`
- 教材称芬苯达唑被认为是少数对 Trichuris 有效的驱虫药之一，但本批不生成剂量、疗程或休药期。`fact_id=PARA-047-fenbendazole-trichuris; source_id=SRC-0082; anchor=Chapter 67 Internal Parasites; PDF page 1064`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-061-trichuris-suis-internal-parasites/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-061-trichuris-suis-internal-parasites/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-061-trichuris-suis-internal-parasites/003-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-061-trichuris-suis-internal-parasites/004-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
