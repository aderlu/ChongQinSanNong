# Swine Wiki Authority + PDF Enrichment Summary - 2026-05-07

## 已完成

- 下载/缓存 17 个权威网页或 PDF 来源到 `raw/urls` 与 `raw/pdfs`，并建立 source pages。
- 生成权威来源 manifest：`issues/authority_web_fetch_manifest_2026-05-07.json`。
- 生成 PDF 疾病-药物候选矩阵：`issues/swine_pdf_treatment_candidate_matrix_2026-05-07.csv`，共 178 行。
- 新增 derived synthesis：`wiki/synthesis/swine_treatment_candidate_matrix_v7.md`。
- 本轮新增 6 个药物页，使 drug 页面总数达到 76。

## 下载状态说明

- 成功缓存正文或 PDF：MOA 第250号、第2292号、喹乙醇等停用政策入口、GB31650 新闻入口、WOAH swine AMR TRD PDF、WOAH 抗微生物药重要性页面、EMA AMEG PDF、EMA MRL 页面。
- 未成功缓存全文但保留 source page 和失败状态：Merck 页面返回 403，FDA 页面本地下载路径遇到 SSL/404，农业部第278号旧链接返回 404。
- 未成功缓存的来源不得作为已抓取原文使用；后续需通过浏览器手动保存、官方 API、替代官方链接或人工下载补原文。

## 重要质量边界

- MOA/中国政府来源用于中国禁用、停用、标签、残留、休药期和说明书规则边界。
- Merck/EMA/FDA/WOAH/FAO 可用于治疗候选、产品证据、AMR 审慎或国际对照，但不能替代中国禁用/合规判断。
- 本轮未把候选写入正式 `knowledge_facts.json`。

## 后续建议

- 对 Merck 403 页面用浏览器/人工保存或官方可下载版本补原文快照。
- 对 FDA Green Book 使用 `animaldrugsatfda.fda.gov` 的查询/API 或人工导出补充产品级标签。
- 将 PDF 候选矩阵按疾病页批量回填为 `NEEDS_REVIEW` 候选小节，人工复核后再升级事实。
