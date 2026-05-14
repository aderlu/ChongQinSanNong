---
type: source
source_id: SRC-0039
source_path: docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman, Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf
source_type: textbook_pdf_chapter
authority_level: textbook
legacy_evidence_status: EXTRACTED
source_status: source_anchored
created: 2026-05-06T15:59:30+00:00
updated: 2026-05-06T15:59:30+00:00
sources: []
---

# Diseases of Swine, 11th Edition - Chapter 33 Flaviviruses opening

- 页码范围：PDF page 554-564。
- 可抽取范围：黄病毒总论、日本脑炎病毒、西尼罗病毒、Murray Valley encephalitis virus、DENV/ZIKV 猪模型和新发黄病毒边界。PDF page 564 后段进入参考文献。
- PDF 抽取：本批使用 PyMuPDF `fitz` 主抽取，pdfplumber 页级字符量核对，pdfminer.six 批量抽取作为第三方对照；详见 `issues/formal_batch_016_pdf_pages_525_564_parser_report.txt`。
- 本来源不直接生成固定药物处方、剂量、免疫程序、根除承诺、扑杀/封锁/调运/消毒命令或中国监管结论。

## 可支持结论

- 支持范围以本页来源摘要、URL/path、页码/章节、表格和已登记 facts 为准。

## 不得外推边界

- 不得超出 `authority_level` 和原文明确支持范围；剂量、疗程、休药期、MRL、残留、食品安全、检疫、扑杀、调运、报告等高风险结论必须另有 A0 或标签级等价来源支持。
