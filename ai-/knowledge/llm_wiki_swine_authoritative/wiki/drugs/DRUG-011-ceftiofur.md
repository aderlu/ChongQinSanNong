---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-011-ceftiofur
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, positive_drug_candidate, gap_routing, positive_label_candidate]
sources: [A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0059, SRC-0063, SRC-0070, SRC-0074, SRC-0075, SRC-0088, SRC-0089, SRC-0090, SRC-0091]
candidate_source: issues/drug_pdf_candidate_extraction_2026-05-07.md
---

# Ceftiofur / 头孢噻呋

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 证据状态

- 使用范围：`positive_label_candidate`。
- 本页来自教材 PDF 候选抽取和有限权威来源入口整理，用于扩大 drug 检索覆盖面。
- 未完成具体标签、靶动物、剂型/途径、适应证、禁停用和药敏证据逐项复核前，不得生成执行性处方、剂量、疗程、休药期或法域合规承诺。

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=positive_label_candidate`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0059, SRC-0063, SRC-0070, SRC-0074, SRC-0075, SRC-0088, SRC-0089, SRC-0090；页码锚点：17；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：24 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=positive_label_candidate`，表示已存在可召回的具体标签或等效权威事实源；可用于正向用药答案，但只能限定在该来源覆盖的猪靶动物、制剂、途径、适应证、剂量/疗程、处方状态和休药期/MRL 范围内。
- 生成处方或评估答案时，可接受 `A0/A1/A2/SRC/RC/RULE` 任一类已锚定来源；不再要求必须是中国 A0/A1，但不得把一个法域、产品或制剂的证据外推到另一个法域、产品或制剂。
- 如果问题明确要求中国合规、当地出栏、残留合格或肉品可食，必须回到中国现行标签/标准/公告；否则应标注“仅限所引来源范围”。

## 药物类别

- third-generation cephalosporin

## 教材候选证据

- 教材候选表在放线杆菌病、支气管败血波氏杆菌混合呼吸道病、大肠杆菌耐药、巴氏杆菌肺炎、葡萄球菌病和链球菌病语境中命中 ceftiofur。
- 候选页码：PDF page 184, 187, 188, 190, 784, 787, 798, 836, 840, 847, 918, 919, 946, 954, 966, 967。

## 疾病/用途候选

- 呼吸道和系统性细菌病抗菌候选；因第三代头孢公共卫生重要性，生成答案必须优先提示诊断、药敏和合规复核。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-011-ceftiofur/001-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-011-ceftiofur/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-011-ceftiofur/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: SRC-0090。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-011-ceftiofur/004-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-011-ceftiofur/005-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
