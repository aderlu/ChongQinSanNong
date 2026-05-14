# Phase 3 药物页证据扩展迁移执行记录

落地时间：2026-05-09 11:43 +08:00

## 本阶段目标

按照 `2026-05-09-wiki-phased-cleanup-plan.md` 的 Phase 3，处理高风险大型药物页。

核心目标：

- 保留药物页作为 runtime core 的精简边界页。
- 将大段批次增强证据、候选事实、剂量/疗程事实迁移到非默认运行时的 evidence expansion 层。
- 在 runtime 药物页中补充明确规则卡锚点，避免生产和评估链路把药物页当作可直接生成处方、剂量、疗程、休药期或 MRL 的依据。

## 修改前存在的问题

Phase 2 后，runtime hallucination risk audit 仍有 7 个 high 风险页，全部是药物页：

- `DRUG-034-sulfonamides`
- `DRUG-014-lincomycin`
- `DRUG-009-penicillin-g`
- `DRUG-030-tetracyclines`
- `DRUG-023-gentamicin`
- `DRUG-020-chlortetracycline`
- `DRUG-066-dexamethasone`

这些页面的共同问题：

- 页面过大，部分超过 20 KB，`DRUG-009` 超过 45 KB。
- runtime 正文中直接包含 `candidate_fact`、`dose_route_course`、处方/混饲/肌注/疗程等长证据。
- 部分页面包含休药期、MRL、残留等高风险词。
- 虽然页面已有边界说明，但 runtime 正文缺少可被审计脚本和生产链路稳定识别的 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001` 字面锚点。

影响：

- 生产检索容易把证据扩展块作为默认回答依据。
- 模型可能从候选事实或旧手册事实外推可执行处方。
- 评估链路可能把长证据块当成答案充分性的主要依据，降低评估稳定性。

## 修改前相关代码和知识库状态

已有代码：

- `tools/build_runtime_core_manifest.py`：生成 runtime allowlist 和 exclude patterns。
- `tools/audit_runtime_hallucination_risk.py`：检查 runtime 页风险。
- `tools/quarantine_encoding_damaged_lines.py`：Phase 2 编码损坏隔离脚本。

修改前审计状态：

- runtime manifest entries: 198
- runtime missing paths: 0
- hallucination risk audit:
  - high: 7
  - medium: 102
  - low: 50
  - none: 39
- readiness score: 99/100

修改前目标页面体积和风险信号：

- `DRUG-034-sulfonamides.md`: 39086 bytes, candidate facts 15, dose_route_course 16
- `DRUG-014-lincomycin.md`: 26389 bytes, candidate facts 11, dose_route_course 7
- `DRUG-009-penicillin-g.md`: 45618 bytes, candidate facts 8, dose_route_course 14
- `DRUG-030-tetracyclines.md`: 24142 bytes, candidate facts 8, dose_route_course 7
- `DRUG-023-gentamicin.md`: 23180 bytes, candidate facts 5, dose_route_course 8
- `DRUG-020-chlortetracycline.md`: 19405 bytes, candidate facts 13, dose_route_course 4
- `DRUG-066-dexamethasone.md`: 29935 bytes, candidate facts 4, dose_route_course 9

## 本阶段新增或更新的代码

新增脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase3_move_drug_evidence_expansions.py`

脚本功能：

- 针对 7 个 high 风险药物页执行批次块迁移。
- 识别 `<!-- XXX_START --> ... <!-- XXX_END -->` 形式的批次增强块。
- 将原始增强块完整写入 `wiki/evidence_expansions/drugs/` 下的证据扩展文件。
- 在 runtime 药物页原位置保留 `PHASE3_EVIDENCE_EXPANSION_MOVED` 占位说明。
- 在 runtime 药物页标题下新增 `Runtime guardrail anchors / Phase 3`，显式写入：
  - `RC-DRUG-001`
  - `RC-WITHDRAWAL-MRL-001`
- 生成 Phase 3 迁移报告。

更新脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`

更新点：

- `runtime_exclude_patterns.json` 新增默认排除项：`wiki/evidence_expansions/**`

原因：

- evidence expansion 文件只用于审计、溯源和证据扩展，不应进入默认 production/evaluation retrieval。

## 本阶段整理或新增的知识库内容

新增 evidence expansion 目录：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/drugs/`

新增证据扩展文件：

- `DRUG-034-sulfonamides-evidence-expansion-20260509.md`
- `DRUG-014-lincomycin-evidence-expansion-20260509.md`
- `DRUG-009-penicillin-g-evidence-expansion-20260509.md`
- `DRUG-030-tetracyclines-evidence-expansion-20260509.md`
- `DRUG-023-gentamicin-evidence-expansion-20260509.md`
- `DRUG-020-chlortetracycline-evidence-expansion-20260509.md`
- `DRUG-066-dexamethasone-evidence-expansion-20260509.md`

被精简的 runtime 药物页：

- `wiki/drugs/DRUG-034-sulfonamides.md`
- `wiki/drugs/DRUG-014-lincomycin.md`
- `wiki/drugs/DRUG-009-penicillin-g.md`
- `wiki/drugs/DRUG-030-tetracyclines.md`
- `wiki/drugs/DRUG-023-gentamicin.md`
- `wiki/drugs/DRUG-020-chlortetracycline.md`
- `wiki/drugs/DRUG-066-dexamethasone.md`

新增执行报告：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase3_drug_evidence_expansion_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase3_drug_evidence_expansion_2026-05-09.md`

## 本阶段迁移结果

总计：

- 处理页面：7
- 修改页面：7
- 迁移批次证据块：33
- 迁移 candidate_fact mentions：64
- 迁移 dose_route_course mentions：65

单页结果：

- `DRUG-034-sulfonamides.md`: 6 blocks moved, 39086 -> 7113 bytes
- `DRUG-014-lincomycin.md`: 5 blocks moved, 26389 -> 6455 bytes
- `DRUG-009-penicillin-g.md`: 5 blocks moved, 45618 -> 6655 bytes
- `DRUG-030-tetracyclines.md`: 3 blocks moved, 24142 -> 4660 bytes
- `DRUG-023-gentamicin.md`: 4 blocks moved, 23180 -> 6131 bytes
- `DRUG-020-chlortetracycline.md`: 5 blocks moved, 19405 -> 6539 bytes
- `DRUG-066-dexamethasone.md`: 5 blocks moved, 29935 -> 4972 bytes

修改后 7 个 runtime 药物页：

- `candidate_fact` mentions: 0
- `dose_route_course` mentions: 0
- 均包含 `PHASE3_EVIDENCE_EXPANSION_MOVED`
- 均包含 `RC-DRUG-001`
- 均包含 `RC-WITHDRAWAL-MRL-001`

## 修改后解决了什么

### 1. 默认 runtime 检索更干净

大段候选事实、剂量、疗程、处方和批次增强块不再直接位于 runtime 药物页正文中。

预期效果：

- 减少检索 chunk 噪声。
- 降低模型直接复制旧手册剂量或候选事实的概率。
- 让药物页更像“边界页”和“召回入口”，而不是“处方答案库”。

### 2. 证据没有丢失

迁移出的原始证据保存在 `wiki/evidence_expansions/drugs/`。

预期效果：

- 需要审计、溯源、人工复核或证据扩展时仍能访问完整批次证据。
- 生产链路可以采用“两阶段检索”：先 runtime core，必要时按规则加载 evidence expansion。

### 3. 规则卡锚点更明确

7 个药物 runtime 页均补充 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`。

预期效果：

- 审计脚本能识别药物页已有硬边界。
- 生产和评估系统可以基于规则卡锚点触发拒答、追问、证据扩展或标签复核。

### 4. high 风险清零

Phase 3 后 hallucination risk audit 结果：

- high: 0
- medium: 102
- low: 50
- none: 46

相较 Phase 2 后：

- high: 7 -> 0
- none: 39 -> 46

## 验证命令和结果

执行 Phase 3 迁移：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase3_move_drug_evidence_expansions.py`

结果：

- processed: 7
- changed: 7
- blocks_moved: 33

重新生成 runtime manifest：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py`

结果：

- entries: 198
- missing_paths: 0
- `runtime_exclude_patterns.json` 已包含 `wiki/evidence_expansions/**`

运行 hallucination risk audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py`

结果：

- entries_checked: 198
- high: 0
- medium: 102

运行原 readiness audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py`

结果：

- readiness_score: 99
- missing_paths: 0
- bad_fact_tables: 0
- missing_rule_cards: 0
- missing_synthesis: 0

## 后续遗留问题

当前 high 风险已经清零，但 medium 风险仍有 102 个，主要集中在：

- partial drug pages。
- 仍含剂量、疗程、休药期、MRL 词但尚未显式补规则卡锚点的药物页。
- 仍比较大的药物页，如 `DRUG-015-tylosin`。

下一步建议进入 Phase 4：

- 批量补齐药物页规则卡锚点。
- 统一 `runtime_tier`、`allowed_use`、`blocked_use`。
- 对仍然较大的 medium 药物页继续迁移 evidence expansion。

