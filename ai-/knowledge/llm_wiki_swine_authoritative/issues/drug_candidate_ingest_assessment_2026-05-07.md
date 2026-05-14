# Drug Candidate Ingest Assessment - 2026-05-07

## 本次处理

- 从 `issues/drug_pdf_candidate_extraction_2026-05-07.md` 中评估并落地药物候选页。
- 新增 drug 页面：28 个，范围为 `DRUG-009` 到 `DRUG-036`。
- 更新索引：`exports/drug_page_index.csv`。
- 新增官方来源入口：`A0-MOA-BANNED-DRUG-250-NOTICE`、`A0-MOA-WITHDRAWAL-278`。

## 解析库评估

- 现有候选表已经使用 PyMuPDF 全量扫描，并用 pdfplumber/pdfminer 对关键页做 spot check。
- 三个解析器在 Chapter 10、Chapter 62、Chapter 65-67 的关键药物词命中一致，说明用已有 PDF 解析库可显著提升效率和可复核性。
- 当前中文名出现 mojibake 的候选表不应直接作为中文实体来源；本次中文药名按常用兽药译名人工校正，并保留 `NEEDS_REVIEW`。

## 入库边界

- 新页面全部为 `evidence_only + NEEDS_REVIEW`，用于检索覆盖和后续人工复核。
- 未写入 `exports/knowledge_facts.json`，避免把候选抽取误升级为正式事实。
- 任何剂量、疗程、给药途径、休药期、中国可用性结论，均需中国现行标签/公告/批准文号或兽医处方依据。

## 权威来源入口

- 农业农村部公告第250号：食品动物禁用药清单原文入口。
- 农业部公告第278号：部分兽药停药期规定入口，需核验现行有效性和具体产品标签。
- 教材来源：`Diseases of Swine, 11th Edition` Chapter 10、49-62、65-67 的候选页码。

## 后续复核建议

- 第一优先级：把 `DRUG-009` 到 `DRUG-036` 按中国批准产品、说明书、禁限用状态、休药期来源逐项核验。
- 第二优先级：对 ceftiofur、enrofloxacin、aminoglycosides 等公共卫生重要抗菌药增加硬边界规则卡。
- 第三优先级：把 PDF 页码候选转为结构化 candidate facts，但保持 `NEEDS_REVIEW`，通过人工复核后再升级。
