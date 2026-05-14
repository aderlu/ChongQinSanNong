---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-034-sulfonamides
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-ANNOUNCEMENT-183-SULFADIAZINE-2019, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-MRL-GB31650-2019, A0-MOA-PRESCRIPTION-2471-2016, A0-MOA-WITHDRAWAL-278, SRC-0012, SRC-0059, SRC-0063, SRC-0070, SRC-0074, SRC-0075, SRC-0087, SRC-0089, SRC-0090, SRC-0091, SRC-0092]
candidate_source: issues/drug_pdf_candidate_extraction_2026-05-07.md
---

# Sulfonamides / 磺胺类

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime guardrail anchors / Phase 3

- `RC-DRUG-001`: This runtime page must not be used by itself to generate executable prescriptions, dose, route, course, withdrawal period, MRL, residue, or food-safety claims.
- `RC-WITHDRAWAL-MRL-001`: Any withdrawal-period, MRL, residue, or edible-product conclusion must be checked against current label/regulatory sources and the evidence expansion layer.
- Evidence expansion blocks moved in Phase 3 are audit and source-expansion material, not default runtime retrieval text.

## 证据状态

- 使用范围：`boundary_only`。
- 本页来自教材 PDF 候选抽取和有限权威来源入口整理，用于扩大 drug 检索覆盖面。
- 未完成具体标签、靶动物、剂型/途径、适应证、禁停用和药敏证据逐项复核前，不得生成执行性处方、剂量、疗程、休药期或法域合规承诺。

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=boundary_only`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：A0-MOA-ANNOUNCEMENT-183-SULFADIAZINE-2019, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-MRL-GB31650-2019, A0-MOA-PRESCRIPTION-2471-2016, A0-MOA-WITHDRAWAL-278, SRC-0012, SRC-0059, SRC-0063, SRC-0070, SRC-0074, SRC-0075, SRC-0087, SRC-0089, SRC-0090；页码锚点：59；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：78 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 药物类别

- antimicrobial class

## MOA authority enrichment 2026-05-08

- 农业部公告第278号列入多种磺胺类及复方磺胺品种的停药期，例如复方磺胺氯哒嗪钠粉列猪4日、复方磺胺嘧啶钠注射液列猪20日，磺胺二甲嘧啶片列猪15日；这些是具体品种/剂型边界，不能概括为所有磺胺类统一休药期。`source_id=A0-MOA-WITHDRAWAL-278`
- 农业部公告第2471号第二批兽用处方药目录列入多项磺胺类复方产品；可用于处方药边界提示，但不能证明具体猪用适应证或剂量。`source_id=A0-MOA-PRESCRIPTION-2471-2016`
- GB 31650-2019 官方入口作为食品中兽药最大残留限量检索锚点；残留限量只约束食品安全合规，不能反推出批准使用或治疗方案。`source_id=A0-MOA-MRL-GB31650-2019`
- 农业农村部公告第183号发布复方磺胺嘧啶混悬液质量标准、说明书、标签和磺胺嘧啶/甲氧苄啶残留检测方法，但该产品说明书靶动物为鸡；不得外推为猪用磺胺类标签。`source_id=A0-MOA-ANNOUNCEMENT-183-SULFADIAZINE-2019`

## 教材候选证据

- 教材候选表将 sulfonamides 和 trimethoprim-sulfonamide combinations 纳入急性呼吸道、大肠杆菌、放线杆菌、葡萄球菌、链球菌和沙门氏菌语境。
- 候选页码：PDF page 184, 186, 192, 784, 787, 798, 840, 847, 854, 918, 923, 946, 954, 955, 966, 967, 1022。

## 疾病/用途候选

- 药物类别页；具体成分、组合比例和产品标签需复核。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-034-sulfonamides/001-HANDBOOK_RX_V13_1.md`：HANDBOOK_RX_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-034-sulfonamides/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-034-sulfonamides/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-034-sulfonamides/004-RAU_1_200_V14.md`：RAU_1_200_V14；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-034-sulfonamides/005-RAU_201_400_V14.md`：RAU_201_400_V14；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-034-sulfonamides/006-RAU_401_600_V14.md`：RAU_401_600_V14；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
