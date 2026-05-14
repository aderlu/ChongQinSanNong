---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-044-cefquinome
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-ANNOUNCEMENT-661-CEFQUINOME-2006, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-PRESCRIPTION-2471-2016, SRC-0012, SRC-0089, SRC-0090, SRC-0091]
candidate_source: subagent_pdf_candidate_scan_2026-05-07
---

# Cefquinome / 头孢喹肟

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime guardrail anchors / Phase 4

- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.

## 证据状态

- 使用范围：`boundary_only`。
- 本页来自 Diseases of Swine 11e PDF 二次候选抽取，用于补齐被药物大类吞掉的具体药物名。
- 未完成中国批准产品、禁限用、停用/淘汰、残留限量、说明书和休药期复核前，不得生成处方、剂量、疗程或特定法域合规承诺。

## 药物知识页可用性

- 证据覆盖：source_anchored_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=boundary_only`。
- 可用边界：本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。
- 来源覆盖：A0-MOA-ANNOUNCEMENT-661-CEFQUINOME-2006, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-PRESCRIPTION-2471-2016, SRC-0012, SRC-0089, SRC-0090；页码锚点：7；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：6 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 药物类别

- fourth-generation cephalosporin

## MOA authority enrichment 2026-05-08

- 农业部公告第661号批准硫酸头孢喹肟注射液（2.5%，商品名克百特注射液2.5%）在我国注册，核发进口兽药注册证书，并发布质量标准、标签和说明书；该证据限定于公告所列进口产品和注册期限语境。`source_id=A0-MOA-ANNOUNCEMENT-661-CEFQUINOME-2006; local_text=raw/web/drug_compliance_a0_targeted_20260508/pages_text/592917eeae67_t20060704_641878.htm.html.txt`
- 农业部公告第2471号第二批兽用处方药目录列入“注射用硫酸头孢喹肟”，分类为抗生素类；该证据支持处方药边界提示。`source_id=A0-MOA-PRESCRIPTION-2471-2016`
- 头孢喹肟为高重要性抗菌药候选，本页仍不得从教材敏感性语境生成猪场经验用药；需具体产品标签、病原诊断、药敏和兽医处方复核。`source_id=A0-MOA-LABEL-INSTRUCTION-RULES-2002`

## 教材候选证据

- 候选页码：PDF page 784。
- PDF 语境：胸膜肺炎放线杆菌敏感性语境。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-044-cefquinome/001-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-044-cefquinome/002-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: SRC-0090。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-044-cefquinome/003-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
