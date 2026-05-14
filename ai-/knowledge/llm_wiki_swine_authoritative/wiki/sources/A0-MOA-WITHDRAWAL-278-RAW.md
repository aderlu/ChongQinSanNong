---
type: source
source_id: A0-MOA-WITHDRAWAL-278-RAW
source_path: https://www.moa.gov.cn/gk/tzgg_1/gg/200306/t20030611_90514.htm
source_type: html
authority_level: official
legacy_evidence_status: PROCESSED_SOURCE_ANCHORED
source_status: source_anchored
created: 2026-05-07T23:55:00+08:00
updated: 2026-05-08T23:55:00+08:00
sources: []
raw_relpath: raw/urls/A0-MOA-WITHDRAWAL-278-RAW-moa-notice-no-278-withdrawal-period-provisions.html
sha256: 55f7d9e99b8e2d4e0e193b2f0275501e6d9c1ebd29cadbea6a0da48a8587e3e0
http_status: 404
---

# MOA Notice No. 278 withdrawal period provisions

## 来源

- URL: https://www.moa.gov.cn/gk/tzgg_1/gg/200306/t20030611_90514.htm
- 本地缓存：`raw/urls/A0-MOA-WITHDRAWAL-278-RAW-moa-notice-no-278-withdrawal-period-provisions.html`
- SHA256: `55f7d9e99b8e2d4e0e193b2f0275501e6d9c1ebd29cadbea6a0da48a8587e3e0`
- HTTP status: `404`
- Fetch error: `HTTP Error 404: Not Found`

## 可用范围

- 类别：`china_withdrawal_boundary`。
- 用途：Chinese withdrawal-period source entry; lower priority than current product labels and later notices.

## 使用边界

- `treatment_efficacy_candidate` 可用于治疗候选、鉴别和复核路径，但仍不能替代本地标签、禁用清单、处方或药敏证据。
- `china_*_boundary` 优先用于中国禁用、停用、残留、休药期硬边界；命中违法或禁用时不得作为可用治疗药。
- `amr_prudence_*` 和 `residue_boundary_*` 用于审慎用药、AMR 或残留风险，不直接生成治疗方案。

## V11 source cleanup / 2026-05-08

- 本轮重新核验 source 状态并从 `NEEDS_REVIEW` 移出；新状态：`PROCESSED_SOURCE_ANCHORED`。
- 本页作为 `A0-MOA-WITHDRAWAL-278` 的原始抓取/重复入口保留，用于审计和去重；实体页生成应优先引用 canonical source。
- 高风险结论仍按 V11：剂量、疗程、休药期、MRL、残留合格、食品安全、禁停用、处方和中国监管结论必须匹配精确 A0/A1 来源。

## 可支持结论

- 支持范围以本页来源摘要、URL/path、页码/章节、表格和已登记 facts 为准。

## 不得外推边界

- 不得超出 `authority_level` 和原文明确支持范围；剂量、疗程、休药期、MRL、残留、食品安全、检疫、扑杀、调运、报告等高风险结论必须另有 A0 或标签级等价来源支持。
