---
tags: [drug, swine, cleaned_v13_2, drug_evidence_page]
drug_id: DRUG-045-tilmicosin
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, audit_only, boundary_only]
sources: [A0-MOA-ANNOUNCEMENT-70-TILMICOSIN-2018, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, SRC-0012, SRC-0089, SRC-0090, SRC-0091]
candidate_source: subagent_pdf_candidate_scan_2026-05-07
---

# Tilmicosin / 替米考星

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
- 来源覆盖：A0-MOA-ANNOUNCEMENT-70-TILMICOSIN-2018, A0-MOA-BANNED-DRUG-250-NOTICE, A0-MOA-LABEL-INSTRUCTION-RULES-2002, SRC-0012, SRC-0089, SRC-0090；页码锚点：22；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：21 条。
- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。

## 药物类别

- macrolide

## MOA authority enrichment 2026-05-08

- 农业农村部公告第70号批准替米考星预混剂（20%，商品名泰勇/Pulmotil）再注册并发布修订后的质量标准、说明书和标签；说明书/标签列明适应证为治疗猪胸膜肺炎放线杆菌、巴氏杆菌及支原体引起的感染。`source_id=A0-MOA-ANNOUNCEMENT-70-TILMICOSIN-2018; local_text=raw/web/drug_compliance_a0_targeted_20260508/pages_text/a3cf24c30c8b_t20190102_6165919.htm.html.txt`
- 同一说明书/标签限定用法为混饲，以替米考星计每1000kg饲料猪200-400g，连用15日，休药期猪21日；该结论仅适用于公告对应进口预混剂产品，不外推至注射剂、其他企业产品或所有呼吸道病场景。`source_id=A0-MOA-ANNOUNCEMENT-70-TILMICOSIN-2018`
- 公告文本还列有禁用于马属动物、注意人员接触防护、建议根据药敏试验合理使用等风险边界；答案应避免把替米考星写成无条件经验首选药。`source_id=A0-MOA-ANNOUNCEMENT-70-TILMICOSIN-2018`

## 教材候选证据

- 候选页码：PDF page 185, 186, 784, 918。
- PDF 语境：胸膜肺炎放线杆菌/巴氏杆菌等呼吸道候选语境，教材提示注射安全风险。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-045-tilmicosin/001-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-045-tilmicosin/002-SFDUT_200_363_V13_1.md`：SFDUT_200_363_V13_1；sources: SRC-0090。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-045-tilmicosin/003-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
