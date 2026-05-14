---
type: source
source_id: A1-EMA-AMEG-ANTIBIOTIC-CATEGORISATION
source_path: https://www.ema.europa.eu/system/files/documents/report/ameg-infographic-categorisation-antibiotics_en.pdf
source_type: pdf
authority_level: guideline
legacy_evidence_status: HUMAN_REVIEWED
source_status: source_anchored
created: 2026-05-07T23:55:00+08:00
updated: 2026-05-08T23:55:00+08:00
sources: []
raw_relpath: raw/pdfs/A1-EMA-AMEG-ANTIBIOTIC-CATEGORISATION-ema-ameg-categorisation-of-antibiotics-for-use-in-animals.pdf
sha256: 87cf870648b4c59ca85a65cf52a7a18a2d7cc1ee7d98e02c52e4749900c566b7
http_status: 200
---

# EMA AMEG categorisation of antibiotics for use in animals

## 来源

- URL: https://www.ema.europa.eu/system/files/documents/report/ameg-infographic-categorisation-antibiotics_en.pdf
- 本地缓存：`raw/pdfs/A1-EMA-AMEG-ANTIBIOTIC-CATEGORISATION-ema-ameg-categorisation-of-antibiotics-for-use-in-animals.pdf`
- SHA256: `87cf870648b4c59ca85a65cf52a7a18a2d7cc1ee7d98e02c52e4749900c566b7`
- HTTP status: `200`
- Fetch error: ``

## 可用范围

- 类别：`amr_prudence_eu`。
- 用途：Antibiotic categorisation for responsible veterinary use; does not replace treatment guidelines.

## 使用边界

- `treatment_efficacy_candidate` 可用于治疗候选、鉴别和复核路径，但仍不能替代本地标签、禁用清单、处方或药敏证据。
- `china_*_boundary` 优先用于中国禁用、停用、残留、休药期硬边界；命中违法或禁用时不得作为可用治疗药。
- `amr_prudence_*` 和 `residue_boundary_*` 用于审慎用药、AMR 或残留风险，不直接生成治疗方案。

## V11 source cleanup / 2026-05-08

- 本轮重新核验 source 状态并从 `NEEDS_REVIEW` 移出；新状态：`HUMAN_REVIEWED`。
- 本页可作为对应监管、AMR、残留、标签或临床边界的 source 锚点；仍不得超出页面“使用边界”外推。
- 高风险结论仍按 V11：剂量、疗程、休药期、MRL、残留合格、食品安全、禁停用、处方和中国监管结论必须匹配精确 A0/A1 来源。

## 可支持结论

- 支持范围以本页来源摘要、URL/path、页码/章节、表格和已登记 facts 为准。

## 不得外推边界

- 不得超出 `authority_level` 和原文明确支持范围；剂量、疗程、休药期、MRL、残留、食品安全、检疫、扑杀、调运、报告等高风险结论必须另有 A0 或标签级等价来源支持。
