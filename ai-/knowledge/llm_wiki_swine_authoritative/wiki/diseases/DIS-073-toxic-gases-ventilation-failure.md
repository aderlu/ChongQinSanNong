---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-073
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0086]
---

# 猪舍有毒气体与通风失败损伤

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
- 本轮分析范围：`Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; raw/md/1000-1132.md`；本页保留 9 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：非感染性疾病/环境毒物。

## 病因和暴露

- 毒物相关病例评估必须追问饲料、水源、环境、工业污染、药物/添加剂、杀虫剂、垫料和群体暴露史。`fact_id=NINF-019-toxic-agent-history; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1096`
- 粪污分解可释放氨、硫化氢等有害气体；通风失败、搅动粪池或封闭空间可增加毒性暴露风险。`fact_id=NINF-028-toxic-gases-manure; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1108`

## 临床和现场边界

- 有机磷或氨基甲酸酯中毒可见流泪、缩瞳、呼吸困难、发绀、呼吸道分泌物增多和支气管收缩等胆碱能相关表现。`fact_id=NINF-024-op-carbamate-signs; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1101`
- 急性亚硝酸盐中毒可快速出现全身性缺氧相关表现，需结合水源/饲料暴露和实验室证据。`fact_id=NINF-026-nitrite-acute-signs; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1105`
- 教材称动物设施中低于 10 ppm 的常见氨浓度通常无毒，但呼吸道刺激、通风和混合气体暴露仍需结合现场判断。`fact_id=NINF-029-ammonia-low-level; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1109`

## 实验室/鉴别诊断

- 毒物相关病例评估必须追问饲料、水源、环境、工业污染、药物/添加剂、杀虫剂、垫料和群体暴露史。`fact_id=NINF-019-toxic-agent-history; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1096`
- 钠离子中毒诊断需结合饮水剥夺或盐摄入史、神经表现、病理组织学和鉴别诊断。`fact_id=NINF-027-sodium-ion-histology; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1107`

## 人员安全和防控

- 怀疑离子载体中毒时，防止进一步中毒的核心是停止相关给药或饲料暴露并核查混料错误。`fact_id=NINF-023-ionophore-stop-exposure; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1100`
- 粪污分解可释放氨、硫化氢等有害气体；通风失败、搅动粪池或封闭空间可增加毒性暴露风险。`fact_id=NINF-028-toxic-gases-manure; source_id=SRC-0086; anchor=Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1108`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-073-toxic-gases-ventilation-failure/001-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
