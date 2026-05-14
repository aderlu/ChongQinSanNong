---
tags: [disease, swine, raw_md_cleaned, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-037
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0059, SRC-0087, SRC-0088, SRC-0090]
---

# 猪支气管败血波氏杆菌病 / Bordetellosis

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
- 本轮分析范围：`Chapter 49 Bordetellosis; raw/md/601-800.md`；本页保留 10 条可追溯 fact anchors。
- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。

## 病原与分类

- 分类：细菌性呼吸道疾病。

## 病原/定位

- 支气管败血波氏杆菌在猪群中广泛存在，在非进行性萎缩性鼻炎和呼吸道病复合体中可发挥多种作用。`fact_id=BOR-001-role; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 791`
- B. bronchiseptica 引起人病少见但有报道，公共卫生解释需结合免疫状态、接触史和权威指南。`fact_id=BOR-002-public-health; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 792`

## 传播途径

- B. bronchiseptica 传染性强，可通过直接接触或气溶胶快速传播，通常高发病率、低死亡率。`fact_id=BOR-007-transmission; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 795`

## 临床症状和病理机制

- B. bronchiseptica 发病机制依赖黏附素、毒素等毒力因子的协调表达，多数毒力基因表达需要 BvgAS 系统。`fact_id=BOR-004-bvgas; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 793`
- B. bronchiseptica III 型分泌系统可增强肺炎病变严重度，并有助于肺部持续感染。`fact_id=BOR-005-t3ss; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 794`
- B. bronchiseptica 与其他病原共同感染时可出现更强、更持久的促炎细胞因子反应，加重肺部病变。`fact_id=BOR-006-coinfection; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 795`

## 剖检变化

- 哺乳仔猪原发性 B. bronchiseptica 支气管肺炎急性时可呈坏死出血性，慢性时可硬化、白色和纤维化。`fact_id=BOR-008-lesions; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 796`

## 实验室诊断

- 猪肺炎可由多种病原引起，B. bronchiseptica 常存在于混合感染中，分离结果需结合病变和共同感染解释。`fact_id=BOR-009-diagnosis; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 797`

## 防控边界

- B. bronchiseptica 对多种适合农场使用的化学消毒剂敏感，但消毒效果仍取决于清洁、有机物和执行质量。`fact_id=BOR-003-disinfection; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 793`
- 针对 pertactin 的免疫应答可降低疾病严重度，但 pertactin 基因异质性和母源抗体干扰会影响疫苗效果解释。`fact_id=BOR-010-vaccine-boundary; source_id=SRC-0059; anchor=Chapter 49 Bordetellosis; PDF page 798-799`

## 生成和评估边界

- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。
- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。
- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: SRC-0087。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis/002-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: SRC-0090。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis/004-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
