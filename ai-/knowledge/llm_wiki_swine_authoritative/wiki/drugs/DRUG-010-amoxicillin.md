---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-010-amoxicillin
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, positive_drug_candidate, gap_routing, positive_label_candidate]
sources: [A0-MOA-AMOXICILLIN-INJECTION-332-2020, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-PRESCRIPTION-2471-2016, A0-MOA-WITHDRAWAL-278, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0062, SRC-0063, SRC-0075, SRC-0088, SRC-0089, SRC-0090, SRC-0091]
candidate_source: issues/drug_pdf_candidate_extraction_2026-05-07.md
---

# Amoxicillin / 阿莫西林

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime core compaction / Phase 6

- Runtime role: compact drug boundary page for retrieval, source routing, and evaluation checks.
- Phase 6 moved high-density batch evidence blocks out of default retrieval: `VTOP_V13_1`, `SFDUT_1_200_V13_1`, `SFDUT_200_363_V13_1`, `RAU_1_200_V14`.
- Moved fact-like rows: 47; moved source anchors: 47.
- `RC-DRUG-001`: Keep this page as a boundary and routing page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Expansion files under `wiki/evidence_expansions/drugs/phase6/` are for audit, source lookup, and manual review, not default production retrieval.

## 证据状态

- 使用范围：`positive_label_candidate`。
- 本页来自教材 PDF 候选抽取和有限权威来源入口整理，用于扩大 drug 检索覆盖面。
- 未完成具体标签、靶动物、剂型/途径、适应证、禁停用和药敏证据逐项复核前，不得生成执行性处方、剂量、疗程、休药期或法域合规承诺。

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=positive_label_candidate`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：A0-MOA-AMOXICILLIN-INJECTION-332-2020, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-PRESCRIPTION-2471-2016, A0-MOA-WITHDRAWAL-278, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0012, SRC-0062, SRC-0063, SRC-0075, SRC-0088, SRC-0089, SRC-0090；页码锚点：34；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：46 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=positive_label_candidate`，表示已存在可召回的具体标签或等效权威事实源；可用于正向用药答案，但只能限定在该来源覆盖的猪靶动物、制剂、途径、适应证、剂量/疗程、处方状态和休药期/MRL 范围内。
- 生成处方或评估答案时，可接受 `A0/A1/A2/SRC/RC/RULE` 任一类已锚定来源；不再要求必须是中国 A0/A1，但不得把一个法域、产品或制剂的证据外推到另一个法域、产品或制剂。
- 如果问题明确要求中国合规、当地出栏、残留合格或肉品可食，必须回到中国现行标签/标准/公告；否则应标注“仅限所引来源范围”。

## 药物类别

- beta-lactam / aminopenicillin

## MOA authority enrichment 2026-05-08

- 农业部公告第278号《兽药国家标准和专业标准中部分品种停药期规定》列有“阿莫西林可溶性粉”，但该条靶动物为鸡，停药期为7日，产蛋鸡禁用；不得外推为猪用阿莫西林休药期。`source_id=A0-MOA-WITHDRAWAL-278; local_text=raw/web/drug_compliance_a0_targeted_20260508/pages_text/0deb27262333_t20030611_90514.htm.html.txt`
- 农业部公告第2471号《兽用处方药品种目录（第二批）》列入“复方阿莫西林粉”，分类为抗生素类；该证据仅确认对应复方粉剂进入兽用处方药目录，不证明猪用适应证、剂量或休药期。`source_id=A0-MOA-PRESCRIPTION-2471-2016`
- 兽药标签和说明书编写细则要求适应症按法定质量标准或兽药管理部门批准内容书写，不得擅自扩大应用范围；本页生成答案时应要求提供具体产品批准标签。`source_id=A0-MOA-LABEL-INSTRUCTION-RULES-2002`

## 教材候选证据

- 教材候选表在 Chapter 10、梭菌性肠炎预防、放线杆菌敏感性、大肠杆菌病和链球菌病语境中命中 amoxicillin。
- 候选页码：PDF page 184, 187, 190, 784, 820, 847, 967。

## 疾病/用途候选

- 氨基青霉素类抗菌候选；不得从教材直接生成执行性处方、给水用药方案或休药期。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-010-amoxicillin/001-VTOP_V13_1.md`：VTOP_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-010-amoxicillin/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-010-amoxicillin/003-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-010-amoxicillin/004-RAU_1_200_V14.md`：RAU_1_200_V14；sources: RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-010-amoxicillin/005-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A0-MOA-AMOXICILLIN-INJECTION-332-2020, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001。
