---
tags: [drug, swine, v8, cleaned_v13_2, source_anchored_drug_evidence_page]
drug_id: DRUG-075-praziquantel
updated: 2026-05-08T23:59:00+08:00
jurisdiction: Global
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, gap_routing, negative_trap]
sources: [A1-WOAH-PORCINE-CYSTICERCOSIS, RC-DRUG-CLASS-001, RC-DRUG-GOLD-ROLE-001, RC-WITHDRAWAL-MRL-001, SRC-0082, SRC-0091, SRC-0092]
candidate_source: subagent_pdf_deep_scan_2026-05-07
---

# Praziquantel / 吡喹酮

## Source citation gate / Phase 8

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Runtime guardrail anchors / Phase 4

- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.

## 证据状态

- 证据覆盖：`source_anchored_evidence`。
- 使用范围：`negative_trap`。本页用于阻断“从人终宿主/公共卫生语境外推为猪治疗”的错误生成。
- 本页来自 Diseases of Swine 11e PDF 深度解析，用于补齐治疗候选矩阵中缺少的单列药物。
- 本页不是处方页；未完成标签、禁限用、药敏和休药期复核前，不得生成剂量、疗程或特定法域合规承诺。

## 药物知识页可用性

- 证据覆盖：partial_drug_evidence_page；`source_trust=human_reviewed`；`usage_scope=negative_trap`。
- 可用边界：本页只有部分来源锚定证据，可用于药物召回、边界提示和后续标签核验任务规划。
- 来源覆盖：A1-WOAH-PORCINE-CYSTICERCOSIS, RC-DRUG-CLASS-001, RC-DRUG-GOLD-ROLE-001, RC-WITHDRAWAL-MRL-001, SRC-0082；页码锚点：1；证据扩展：见本页“证据扩展索引”。
- 已识别事实锚点：0 条。
- 页面不具备可执行处方条件；不得从药物名、类别或教材候选外推出剂量、疗程、休药期、MRL 或食品安全结论。
- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。

## 标签/来源使用边界

- 本页 `usage_scope=negative_trap`，主要用于训练和评估错误外推。
- 可用来构造拒答、纠错、禁停用或非猪标签陷阱；不得用于正向处方、休药期、MRL 或食品安全答案。
- 若后续发现具体猪用标签或等效来源，必须先更新本页角色和来源索引，再进入正向生成。

## 药物类别

- anthelmintic / cestocide

## 教材候选证据

- 候选页码：PDF page 1062。
- PDF 语境：Taenia solium public-health lifecycle context; treatment of human definitive hosts, not routine treatment of infected pigs.

## 合规和安全边界

- Do not infer pig treatment from human definitive-host treatment; use as zoonotic/public-health boundary.
- 不得把 Taenia solium 公共卫生生命周期中的人终宿主治疗语境，外推为感染猪或特定法域猪场的常规治疗方案。
- 未找到并核验中国猪用吡喹酮具体批准标签、靶动物、剂型、适应证和休药期前，本页不得进入正向用药黄金答案。
- 命中高风险/人医关键药/有机磷/人用公共卫生语境时，必须优先做禁用、停用、淘汰、残留、标签和兽医处方复核。

## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-075-praziquantel/001-RAU_1_200_V14.md`：RAU_1_200_V14；sources: SRC-0091。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-075-praziquantel/002-RAU_201_400_V14.md`：RAU_201_400_V14；sources: SRC-0092。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-075-praziquantel/003-RAU_401_600_V14.md`：RAU_401_600_V14；sources: SRC-0093。
- `wiki/evidence_expansions/drugs/phase4_runtime_compaction/DRUG-075-praziquantel/001-V8.md`：V8 黄金集用途；sources: source anchors retained in expansion。
