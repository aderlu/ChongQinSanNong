---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-067
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0085]
---

# 黄曲霉毒素中毒 / Aflatoxicosis

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
- 本轮分析范围：`Chapter 69 Mycotoxins in Grains and Feeds; raw/md/1000-1132.md`；本页保留 4 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：霉菌毒素/肝毒性。

## 病因和暴露

- 多数猪霉菌毒素问题与受毒素产生真菌污染的饲料谷物有关，风险可发生在收获、储存或运输环节。`fact_id=NINF-009-mycotoxin-feed-grains; source_id=SRC-0085; anchor=Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1079-1080`

## 临床症状和剖检

- 黄曲霉毒素中毒可见肝脏相关病变，急性至亚急性病例可出现沉郁和肝毒性表现。`fact_id=NINF-012-aflatoxin-liver-lesions; source_id=SRC-0085; anchor=Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1082-1083`

## 实验室诊断

- 谷物或饲料霉菌毒素检测可支持暴露判断，但应与采食量、批次、临床表现、病变和其他疾病鉴别一起解释。`fact_id=NINF-011-mycotoxin-testing-feed; source_id=SRC-0085; anchor=Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1082`

## 防控/用药边界

- 教材关于霉菌毒素吸附剂或预防性添加剂的讨论不能直接生成通用治疗方案、剂量或中国合规结论。`fact_id=NINF-013-aflatoxin-additives-boundary; source_id=SRC-0085; anchor=Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1084`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。
