---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-048
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0071, SRC-0072, SRC-0088, SRC-0089, SRC-0090]
---

# 猪增生性肠病 / Lawsonia intracellularis

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
- 本轮分析范围：`Chapter 58 Proliferative Enteropathy; raw/md/801-1000.md`；本页保留 18 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：细菌性肠道疾病。

## 病原/定位

- 增生性肠病由 Lawsonia intracellularis 引起，以肠上皮未成熟细胞增殖性病变为核心特征；本批仅覆盖章节开端。`fact_id=LAW-001-pe-definition; source_id=SRC-0071; anchor=Chapter 58 Proliferative Enteropathy; PDF page 922`
- Lawsonia intracellularis 是 Lawsonia 属唯一种，也是增生性肠病唯一病因，为专性细胞内细菌，不能在无细胞培养基中常规培养。`fact_id=LAW-002-sole-species-obligate; source_id=SRC-0071; anchor=Chapter 58 Proliferative Enteropathy; PDF page 922`
- L. intracellularis 体外培养需要分裂中的细胞和特定微需氧条件，培养解释不能按普通细菌培养外推。`fact_id=LAW-003-cell-culture-boundary; source_id=SRC-0071; anchor=Chapter 58 Proliferative Enteropathy; PDF page 923`

## 流行病学/传播边界

- 教材指出尚无 L. intracellularis 感染人的证据，人源炎症性肠病调查未能找到典型 PE 病变或该病原。`fact_id=LAW-004-public-health-no-human-evidence; source_id=SRC-0071; anchor=Chapter 58 Proliferative Enteropathy; PDF page 923`
- 增生性肠病在家猪群中呈地方性存在，也已在全球野猪群中被描述；野猪向商业猪群传播的证据仍需谨慎解释。`fact_id=LAW-005-endemic-domestic-feral; source_id=SRC-0071; anchor=Chapter 58 Proliferative Enteropathy; PDF page 924`
- L. intracellularis 或相似增生性肠病可见于多种动物，但其他动物作为猪感染来源的作用仍不明确。`fact_id=LAW-006-other-species-source-unclear; source_id=SRC-0071; anchor=Chapter 58 Proliferative Enteropathy; PDF page 924`
- 实验感染后约 1 周可开始出现粪便排菌和增生性病变，病变通常先在小肠远端发展。`fact_id=LAW-009-fecal-shedding-timeline; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 925`

## 临床症状

- 增生性肠病可表现为亚临床感染、慢性腹泻/生长受损和急性出血型肠病等不同临床型，不能只按单一腹泻病解释。`fact_id=LAW-011-clinical-forms; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 926-927`
- 部分感染猪即使无明显腹泻，也可因亚临床 PE 病变出现日增重下降等性能损失。`fact_id=LAW-012-subclinical-performance; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 927`

## 剖检变化

- 增生性肠病病变局限于肠上皮，以隐窝上皮细胞增殖、成熟受阻和杯状细胞减少等为核心。`fact_id=LAW-010-lesions-restricted-epithelium; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 926`
- 慢性猪肠腺瘤病样 PE 肉眼病变最常见于回肠末端，也可见于空肠、盲肠或结肠局灶。`fact_id=LAW-013-pia-lesions-terminal-ileum; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 927`

## 实验室诊断

- PE 确诊需要特征性肉眼/显微病变并在病变中证明 L. intracellularis；单靠临床腹泻或生长不良不足以确诊。`fact_id=LAW-014-diagnosis-lesion-organism; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 929`
- 粪便 PCR 可支持群体层面 Lawsonia 评估和排菌水平判断，但检测结果或阈值需结合病变、临床和群体背景解释。`fact_id=LAW-016-fecal-pcr-boundary; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 930`
- Lawsonia 血清学可提示暴露，但不必然代表显著病变或当前临床病；需与临床、PCR、病理或群体资料结合。`fact_id=LAW-017-serology-exposure-not-disease; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 930`

## 鉴别诊断

- PE 临床鉴别需包括猪痢疾、沙门氏菌性肠炎、鞭虫、PCVAD 以及其他肠道病，尤其在腹泻和肛周污染场景中。`fact_id=LAW-015-differential-diarrhea; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 929`

## 防控和用药边界

- 教材指出鼠害控制是控制增生性肠病的重要因素之一，但不能单独替代诊断、清洁消毒、猪流管理和免疫/用药边界。`fact_id=LAW-007-rodent-control; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 925`
- PE 控制需结合清洁消毒、减少粪便污染、猪流管理、昆虫和鼠害控制等措施，而不是单一用药或疫苗动作。`fact_id=LAW-018-disinfection-management; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 931`
- 教材描述抗菌药和活疫苗可减少 PE 病变或排菌，但具体药物、给药、免疫程序、休药期和合规性需本地标签或 A0/A1 来源确认。`fact_id=LAW-019-antibiotic-vaccine-boundary; source_id=SRC-0072; anchor=Chapter 58 Proliferative Enteropathy; PDF page 931-932`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-048-proliferative-enteropathy-lawsonia-intracellularis/001-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-048-proliferative-enteropathy-lawsonia-intracellularis/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-048-proliferative-enteropathy-lawsonia-intracellularis/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: SRC-0090。
