---
type: issue_report
page_id: wiki_diseases_comparisons_drugs_mojibake_audit_2026_05_08
title: wiki diseases/comparisons/drugs mojibake audit and cleanup
updated: 2026-05-08T23:59:00+08:00
evidence_status: HUMAN_REVIEWED
---

# wiki diseases/comparisons/drugs mojibake audit and cleanup

## Scope

Checked these directories with explicit UTF-8 reads:

- `wiki/diseases`：73 Markdown files
- `wiki/comparisons`：17 Markdown files
- `wiki/drugs`：81 Markdown files

## Findings

- `wiki/comparisons`：no persistent mojibake found after explicit UTF-8 read. Apparent mojibake shown by default PowerShell `Get-Content` was a command decoding artifact.
- `wiki/drugs`：no persistent mojibake found after explicit UTF-8 read. Apparent mojibake shown by default PowerShell `Get-Content` was a command decoding artifact.
- `wiki/diseases`：true mojibake was concentrated in the 32 disease pages that had previously remained `evidence_status: NEEDS_REVIEW`; several already reviewed disease pages also contained isolated imported raw excerpt lines from SFDUT candidate facts.

## Cleanup performed

- Recovered reversible UTF-8-as-GBK mojibake in disease pages, including headings and repeated boundary text such as `英文/教材章节名`, `传播途径`, `临床症状`, `实验室诊断`, `监管/执行性处置边界`, `用药/处置边界`, and `临床知识页可用性`.
- Cleaned common replacement-character fragments (`�?`) where the context was deterministic, for example `诊断`, `分类`, `边界`, `阶段`, `要点`, `来源`, `锚点`, `公告第250号`, and `公告第573号`.
- Preserved all `evidence_status` values; 32 disease pages remain `NEEDS_REVIEW`.
- Normalized files written during cleanup as UTF-8.

## Residual issue lines

Four residual lines remain because they are imported raw handbook/candidate excerpts whose text is not safely recoverable from the stored bytes without returning to the original raw source extraction. They are source-anchored candidate excerpts, not disease-page headings or core disease facts:

- `DIS-009-transmissible-gastroenteritis-virus.md`, line 190, `SFDUT1-TX-0691`, `SRC-0089`, page 176.
- `DIS-026-foot-and-mouth-disease-picornaviruses.md`, line 184, `SFDUT1-TX-0585`, `SRC-0089`, page 134.
- `DIS-040-colibacillosis.md`, line 205, `SFDUT2-TX-0123`, `SRC-0090`, page 227.
- `DIS-044-gl-sser-s-disease.md`, line 157, `SFDUT2-TX-0041`, `SRC-0090`, page 201.

## Recommendation

For the four residual lines, do not attempt blind character replacement. Re-extract those exact raw source pages from `raw/md/猪场兽药使用与猪病防治技术1-200页.md` and `raw/md/猪场兽药使用与猪病防治技术200-363页.md`, or remove the unreadable excerpt text while preserving `fact_id`, `source_id`, page, and line anchors.
