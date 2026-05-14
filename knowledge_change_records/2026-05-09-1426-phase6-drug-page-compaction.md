# Phase 6 大体量药物页二次结构化与证据迁移记录

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：14:26（Asia/Shanghai，精确到时和分）
- 所属阶段：Phase 6
- 工作类型：高密度药物运行时页面压缩、批量证据迁移、幻觉风险回归审计

## 2. 本阶段执行前存在的问题

Phase 5 完成后，运行时知识库高风险条目已经为 0，但仍有 10 个中风险条目。其中 6 个来自大体量药物页：

- `wiki/drugs/DRUG-015-tylosin.md`
- `wiki/drugs/DRUG-021-doxycycline.md`
- `wiki/drugs/DRUG-013-tiamulin.md`
- `wiki/drugs/DRUG-012-florfenicol.md`
- `wiki/drugs/DRUG-010-amoxicillin.md`
- `wiki/drugs/DRUG-019-oxytetracycline.md`

这些页面的问题不是缺少基础护栏，而是运行时正文仍然过长、事实密度过高：

1. 页面中仍包含 V13.1/V14 批处理增强块。
2. 大量 `candidate_fact`、`dose_route_course`、`source_id`、处方候选、治疗候选、休药期或残留相关事实集中在默认运行时页面中。
3. 生产链路检索时可能一次性召回过多药物事实，导致模型把“证据候选”误当成“可执行用药建议”。
4. 评估链路虽然能看到 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`，但长正文仍会增加定位、判分和错误归因成本。

## 3. 修改前代码状态

修改前已有以下代码能力：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
  - 可生成运行时核心 manifest，并排除非运行时目录。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`
  - 可审计页面体量、候选事实密度、缺失护栏等风险。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase3_move_drug_evidence_expansions.py`
  - 已经能迁移一批早期高风险药物页的 evidence expansion 块。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase4_apply_drug_guardrail_anchors.py`
  - 已经补齐药物页运行时护栏锚点。

但修改前还缺少一个专门面向 Phase 5 后剩余 6 个中风险药物页的二次压缩工具，无法批量完成“运行时核心保留 + 长证据迁移 + 迁移报告生成 + 回归审计”的闭环。

## 4. 本阶段新增或更新的代码

本阶段新增工具：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase6_compact_high_density_drug_pages.py`

该工具完成以下工作：

1. 固定处理 Phase 6 目标药物页。
2. 识别页面中的 `<!-- *_START -->` / `<!-- *_END -->` 批处理增强块。
3. 将完整批处理证据迁移到：
   - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/drugs/phase6/`
4. 在原运行时药物页中保留短占位符，指向对应 evidence expansion 文件。
5. 在每个目标药物页标题后新增 `Runtime core compaction / Phase 6` 区块，说明：
   - 页面是运行时边界页，不是独立处方来源。
   - 被迁移的证据块不参与默认生产检索。
   - 仍必须遵守 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`。
6. 输出机器可读和人工可读报告：
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase6_drug_page_compaction_2026-05-09.json`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase6_drug_page_compaction_2026-05-09.md`

## 5. 本阶段进行了哪些整理更新工作

本阶段实际处理结果如下：

- 检查药物页：6 个
- 修改药物页：6 个
- 迁移批处理证据块：28 个
- 迁移 fact-like rows：300 行
- 迁移 `candidate_fact` 提及：63 个
- 迁移 source anchors：300 个
- 默认运行时页面总字节减少：132094 bytes

具体页面变化：

- `DRUG-015-tylosin`：4 个证据块迁移，页面从 34086 bytes 降至 7670 bytes。
- `DRUG-021-doxycycline`：5 个证据块迁移，页面从 26497 bytes 降至 8209 bytes。
- `DRUG-013-tiamulin`：5 个证据块迁移，页面从 30086 bytes 降至 8265 bytes。
- `DRUG-012-florfenicol`：5 个证据块迁移，页面从 32418 bytes 降至 9610 bytes。
- `DRUG-010-amoxicillin`：4 个证据块迁移，页面从 29903 bytes 降至 8503 bytes。
- `DRUG-019-oxytetracycline`：5 个证据块迁移，页面从 29848 bytes 降至 8487 bytes。

新增 evidence expansion 文件：

- `wiki/evidence_expansions/drugs/phase6/DRUG-015-tylosin-phase6-evidence-expansion-20260509.md`
- `wiki/evidence_expansions/drugs/phase6/DRUG-021-doxycycline-phase6-evidence-expansion-20260509.md`
- `wiki/evidence_expansions/drugs/phase6/DRUG-013-tiamulin-phase6-evidence-expansion-20260509.md`
- `wiki/evidence_expansions/drugs/phase6/DRUG-012-florfenicol-phase6-evidence-expansion-20260509.md`
- `wiki/evidence_expansions/drugs/phase6/DRUG-010-amoxicillin-phase6-evidence-expansion-20260509.md`
- `wiki/evidence_expansions/drugs/phase6/DRUG-019-oxytetracycline-phase6-evidence-expansion-20260509.md`

本阶段没有新增未经验证的药物事实，也没有改写剂量、疗程、适应证、休药期、MRL 或监管结论。所有操作都是结构整理和检索层降噪。

## 6. 修改后解决了什么问题

本阶段解决了以下问题：

1. 大体量药物页不再把批处理证据直接暴露在默认运行时检索层。
2. 6 个目标药物页的 `candidate_fact` 密度被清出默认运行时正文。
3. 运行时页面从“事实堆叠页”转为“边界页 + source expansion 路由页”。
4. 生产链路更不容易把候选证据误用成可执行处方。
5. 评估链路可以更清楚地区分：
   - 默认检索层：短核心边界和规则锚点。
   - 扩展证据层：仅用于审计、来源查找、人工复核和 evidence expansion。

## 7. 验证结果

执行 Phase 6 工具后得到结果：

```json
{
  "pages_checked": 6,
  "pages_changed": 6,
  "blocks_moved": 28,
  "fact_like_rows_moved": 300,
  "candidate_fact_mentions_moved": 63,
  "bytes_reduced": 132094,
  "report_json": "issues/phase6_drug_page_compaction_2026-05-09.json",
  "report_md": "issues/phase6_drug_page_compaction_2026-05-09.md"
}
```

重新构建运行时核心清单：

```json
{
  "entries": 198,
  "missing_paths": 0
}
```

重新执行幻觉风险审计：

```json
{
  "entries_checked": 198,
  "high": 0,
  "medium": 4,
  "low": 100,
  "none": 94
}
```

重新执行 wiki readiness 审计：

```json
{
  "readiness_score": 99,
  "missing_paths": 0,
  "bad_fact_tables": 0,
  "missing_rule_cards": 0,
  "missing_synthesis": 0
}
```

6 个目标药物页在最新风险 JSON 中均已降为：

```json
{
  "risk_score": 0,
  "findings": []
}
```

## 8. 预计产生的效果

1. 生产链路默认检索药物页时，上下文更短、更稳定。
2. 药物类回答更容易遵守 `RC-DRUG-001`，避免从候选证据直接生成处方。
3. 休药期、MRL、残留和食品安全相关内容更容易被强制路由到标签或监管核验。
4. 评估系统可以更准确地区分“页面缺少证据”和“证据已迁移到扩展层”。
5. 中风险条目从 10 降至 4，说明药物页高密度问题已经完成主要治理。

## 9. 当前仍未完全处理的问题

Phase 6 完成后仍有 4 个中风险条目：

- `DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia`
- `DIS-052-swine-dysentery-brachyspira-hyodysenteriae`
- `DIS-044-gl-sser-s-disease`
- `swine_regulatory_blocking_rules_china`

剩余问题已经从“大体量药物页”转移到：

1. 大体量疾病页运行时正文压缩。
2. 综合监管/synthesis 页面专用护栏和审计规则。

建议下一步执行 Phase 7，优先处理 3 个仍处于中风险的疾病页。

## 10. 本阶段结论

Phase 6 已完成大体量药物页二次结构化和证据迁移。6 个目标药物页全部退出中风险，运行时页面总计减少 132094 bytes，迁移 28 个批处理证据块和 300 个 source anchors。修改后高风险保持 0，中风险从 10 降至 4，readiness score 保持 99。

本阶段的核心价值是把药物页从“默认检索中直接暴露大量候选事实”调整为“默认检索只保留核心边界，详细证据进入扩展层”，从而降低生产和评估链路中的药物处方、剂量、休药期和残留类幻觉风险。
