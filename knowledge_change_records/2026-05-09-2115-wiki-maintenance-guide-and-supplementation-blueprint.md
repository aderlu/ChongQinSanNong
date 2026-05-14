# Wiki 维护指南优化与补充建设说明执行记录

Date: 2026-05-09 21:15

Target: `ai-/knowledge/llm_wiki_swine_authoritative`

## 1. 修改目标

本次修改目标：

- 新增一份猪病 LLM Wiki 后续补充建设说明，明确还需要补充哪些来源、事实、图谱关系、规则卡和黄金数据集样本。
- 优化 `WIKI_MAINTENANCE_GUIDE.md`，把网页搜索信息和本地权威文档的维护流程写成可执行准入规则。
- 明确去重、落位、source-first、runtime 简洁、高风险门禁、编码防乱码和工作留痕要求，防止后续补充造成知识库冗余和混乱。

## 2. 修改前存在的问题

修改前 `WIKI_MAINTENANCE_GUIDE.md` 已经有基础维护原则，但存在以下不足：

- 对网页搜索得到的信息如何登记、分级、去重和落位说明不够细。
- 对本地 PDF、Word、Excel、扫描件、标签和法规等权威文档的证据锚点要求不够具体。
- 对哪些内容进入 `raw/`、`wiki/evidence_expansions/`、`wiki/diseases/`、`wiki/drugs/`、`wiki/rule_cards/`、`issues/` 的决策规则还不够表格化。
- 对黄金数据集正式训练样本需要 fact 级锚点、source/rule provenance 和高风险边界的要求还不够集中。
- 缺少单独的“补充建设说明”文档，不能直接用于规划后续补源和补事实工作。

## 3. 修改前文档状态

修改前：

- `WIKI_MAINTENANCE_GUIDE.md` 为英文为主的维护说明，覆盖 runtime compact、source-routed、guardrails、partial routing、audit 和 change record。
- 不存在 `WIKI_SUPPLEMENTATION_BLUEPRINT.md`。
- 维护指南没有把“网页搜索信息”和“本地权威文档”作为两个独立流程展开。

## 4. 本次新增或更新的文档

更新：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`

新增：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_SUPPLEMENTATION_BLUEPRINT.md`
- `knowledge_change_records/2026-05-09-2115-wiki-maintenance-guide-and-supplementation-blueprint.md`

## 5. 本次整理了什么内容

维护指南新增或强化：

- 来源分级与准入：A0、A1、B、C、D。
- 网页搜索信息维护流程：搜索目的、URL、访问日期、发布机构、去重、禁止直接写入 runtime。
- 本地权威文档维护流程：文件路径、页码、章节、表号、条款、OCR 可靠性。
- 去重与落位规则：明确不同信息类型应进入 raw、sources、evidence_expansions、runtime、rule_cards 或 issues。
- runtime 页面写作规范：短摘要、source anchor、规则卡锚点、缺口说明。
- 高风险门禁：诊断、监管、药物、休药期/MRL、引用和 partial 页面对应规则卡。
- 黄金数据集维护要求：sample_id、page_id、source_ids、fact_ids/evidence anchors、rule_card_ids、allowed/blocked claim scope。
- 必跑验收命令：manifest、幻觉风险审计、readiness 审计、编码审计、猪病 runtime pytest。
- 编码与乱码防护：PowerShell UTF-8、Python UTF-8、JSON `ensure_ascii=False`、CSV UTF-8、修改后编码审计。

补充建设说明新增：

- 中国官方监管和法规来源补充。
- 兽药标签和批准资料补充。
- 权威教材、手册和国际组织资料补充。
- 同行评议研究和流行病学资料补充。
- 疾病知识模块补齐。
- 药物知识模块补齐。
- 规则卡和评估体系补充。
- 知识图谱语义关系补充。
- 黄金数据集正向、评估、负样本、limited 样本补充。
- 后续补充优先级和每批交付物。

## 6. 修改后解决了什么问题

修改后：

- 后续通过网页搜索获取的信息，不会直接进入 runtime 页面，而是先进行来源分级、登记、去重和证据落位。
- 本地权威文档补充有了明确证据锚点要求，避免无页码、无表号、无章节定位的事实进入生产知识。
- 维护人员可以根据表格判断信息应该进入 raw、evidence expansion、runtime 页面、规则卡还是 issues。
- 黄金数据集补充有了更明确的 source/fact/rule provenance 要求。
- 维护指南明确了防乱码流程，降低中文资料维护中的编码风险。

## 7. 预计更新效果

对知识库维护：

- 减少重复来源、重复事实和长 runtime 页面。
- 保持 wiki 知识库清晰简洁。
- 提升后续补源和补事实的一致性。

对生成：

- 生成链路默认只使用 compact runtime 和 allowlist。
- 高风险内容继续由 A0/A1 来源和规则卡门禁控制。

对评估：

- 评估器可以按 source/fact/rule provenance 和 hard-block 规则判断答案是否越界。

对黄金数据集：

- 后续样本生产将更容易区分正式训练样本、评估样本、负样本和 limited 样本。
- fact 级锚点要求有助于提升训练样本可信度。

## 8. 验证方式和结果

本次主要修改维护文档，不改变 runtime 事实内容、manifest 构建逻辑或图谱数据。已执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

结果：

- generated_at: 2026-05-09T22:05:36+08:00
- text_files_scanned: 2314
- runtime_manifest_paths_loaded: 204
- encoding_ok: 2302
- decode_or_replacement_damage: 3
- mojibake_like_content: 0
- minor_mojibake_signal: 9
- runtime_damaged_count: 0

验收结论：

- 新增和更新 Markdown 文件可用 UTF-8 正常读取。
- 未发现新增中文乱码。
- runtime damaged count 保持 0。
- 非 runtime 历史文件中仍有既有 decode/replacement damage 和 minor mojibake signal，本次未扩大处理范围。

## 9. 仍然存在的问题和下一步

仍需继续推进：

- 按 `WIKI_SUPPLEMENTATION_BLUEPRINT.md` 分批补 A0/A1 权威来源。
- 把未来黄金数据集样本逐步升级到 fact_id 或 evidence anchor 级溯源。
- 把图谱关系从 runtime 溯源图进一步增强为带语义关系的疾病-药物-规则-来源图。
- 将维护指南中的验收命令固定进后续批处理或 CI 流程。
