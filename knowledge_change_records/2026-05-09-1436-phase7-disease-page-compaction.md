# Phase 7 大体量疾病页运行时正文压缩记录

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：14:36（Asia/Shanghai，精确到时和分）
- 所属阶段：Phase 7
- 工作类型：高密度疾病运行时页面压缩、疾病证据扩展迁移、幻觉风险回归审计

## 2. 本阶段执行前存在的问题

Phase 6 完成后，药物页高密度问题已经完成主要治理，高风险条目保持 0，中风险条目从 10 降至 4。剩余 4 个中风险条目中，3 个来自大体量疾病页：

- `wiki/diseases/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md`
- `wiki/diseases/DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md`
- `wiki/diseases/DIS-044-gl-sser-s-disease.md`

这些疾病页已经在 Phase 5 补齐疾病运行时护栏，但仍存在以下问题：

1. 页面默认运行时正文仍然较长。
2. 批处理增强块中包含大量 `candidate_fact`、处方候选、治疗候选、用药和防控相关事实。
3. 疾病页容易同时混合临床表现、诊断、剖检、防控、治疗、药物和处方候选，生产检索时上下文噪声较高。
4. 模型可能把疾病页中的治疗候选或处方增强证据直接转写为可执行用药建议。
5. 评估链路虽然可以看到 `RC-DX-001`、`RC-DISEASE-REGULATORY-001`、`RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`，但长证据堆叠仍会增加判分和归因成本。

## 3. 修改前代码状态

修改前已有以下代码能力：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
  - 可生成运行时核心 manifest，并排除非运行时目录。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`
  - 可审计页面体量、候选事实密度、缺失护栏等风险。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase5_apply_disease_guardrail_anchors.py`
  - 已经对疾病页补齐诊断、监管、用药、休药期/MRL 相关护栏锚点。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase6_compact_high_density_drug_pages.py`
  - 已经实现药物页的高密度证据迁移，但只面向药物页。

修改前缺少专门面向疾病页的自动化压缩迁移工具，无法批量完成“疾病运行时核心保留 + 长证据迁移 + 疾病扩展证据报告 + 回归审计”的闭环。

## 4. 本阶段新增或更新的代码

本阶段新增工具：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase7_compact_high_density_disease_pages.py`

该工具完成以下工作：

1. 固定处理 Phase 7 的 3 个目标疾病页。
2. 识别页面中的 `<!-- *_START -->` / `<!-- *_END -->` 批处理增强块。
3. 将完整批处理证据迁移到：
   - `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/diseases/phase7/`
4. 在原运行时疾病页中保留短占位符，指向对应 evidence expansion 文件。
5. 在每个目标疾病页标题后新增 `Runtime core compaction / Phase 7` 区块，说明：
   - 页面是疾病运行时边界页，不是完整证据堆叠页。
   - 被迁移的证据块不参与默认生产检索。
   - 诊断必须遵守 `RC-DX-001`。
   - 监管处置必须遵守 `RC-DISEASE-REGULATORY-001`。
   - 疾病页不得独立生成可执行处方，仍需遵守 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`。
6. 输出机器可读和人工可读报告：
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase7_disease_page_compaction_2026-05-09.json`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase7_disease_page_compaction_2026-05-09.md`

## 5. 本阶段进行了哪些整理更新工作

本阶段实际处理结果如下：

- 检查疾病页：3 个
- 修改疾病页：3 个
- 迁移批处理证据块：12 个
- 迁移 fact-like rows：106 行
- 迁移 `candidate_fact` 提及：31 个
- 迁移 source anchors：108 个
- 默认运行时页面总字节减少：40524 bytes

具体页面变化：

- `DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia`：5 个证据块迁移，页面从 22916 bytes 降至 11432 bytes。
- `DIS-052-swine-dysentery-brachyspira-hyodysenteriae`：4 个证据块迁移，页面从 24330 bytes 降至 10704 bytes。
- `DIS-044-gl-sser-s-disease`：3 个证据块迁移，页面从 26778 bytes 降至 11364 bytes。

新增 disease evidence expansion 文件：

- `wiki/evidence_expansions/diseases/phase7/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia-phase7-evidence-expansion-20260509.md`
- `wiki/evidence_expansions/diseases/phase7/DIS-052-swine-dysentery-brachyspira-hyodysenteriae-phase7-evidence-expansion-20260509.md`
- `wiki/evidence_expansions/diseases/phase7/DIS-044-gl-sser-s-disease-phase7-evidence-expansion-20260509.md`

本阶段没有新增未经验证的疾病事实，也没有改写诊断、用药、处方、休药期、MRL 或监管结论。所有操作都是运行时结构整理和检索层降噪。

## 6. 修改后解决了什么问题

本阶段解决了以下问题：

1. 3 个大体量疾病页不再把批处理增强证据直接暴露在默认运行时检索层。
2. 疾病页中的 `candidate_fact` 和治疗/处方候选从默认运行时正文迁出。
3. 疾病页从“核心临床知识 + 大量增强证据堆叠”调整为“核心疾病边界页 + evidence expansion 路由”。
4. 生产链路更不容易从疾病页直接生成处方、剂量、疗程或监管执行结论。
5. 评估链路可以更清楚地区分：
   - 默认检索层：疾病身份、诊断边界、防控边界、监管边界。
   - 扩展证据层：仅用于审计、来源查找、人工复核和 evidence expansion。

## 7. 验证结果

执行 Phase 7 工具后得到结果：

```json
{
  "pages_checked": 3,
  "pages_changed": 3,
  "blocks_moved": 12,
  "fact_like_rows_moved": 106,
  "candidate_fact_mentions_moved": 31,
  "bytes_reduced": 40524,
  "report_json": "issues/phase7_disease_page_compaction_2026-05-09.json",
  "report_md": "issues/phase7_disease_page_compaction_2026-05-09.md"
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
  "medium": 1,
  "low": 100,
  "none": 97
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

3 个目标疾病页在最新风险 JSON 中均已降为：

```json
{
  "risk_score": 0,
  "findings": []
}
```

## 8. 预计产生的效果

1. 生产链路默认检索疾病页时，上下文更短、更聚焦。
2. 疾病类回答更容易遵守 `RC-DX-001`，避免从症状或候选证据直接下诊断结论。
3. 涉及隔离、报告、检疫、扑杀、移动控制等内容时，更容易触发 `RC-DISEASE-REGULATORY-001`。
4. 涉及治疗候选、剂量、疗程、休药期、MRL、残留和食品安全时，更容易转向药物页和外部标签/监管核验。
5. 中风险条目从 4 降至 1，说明大体量疾病页高密度问题已经完成主要治理。

## 9. 当前仍未完全处理的问题

Phase 7 完成后仍有 1 个中风险条目：

- `wiki/synthesis/swine_regulatory_blocking_rules_china.md`

该页面属于综合监管/synthesis 页面，问题不再是疾病页或药物页正文冗余，而是：

1. 综合监管页缺少 synthesis/regulatory 专用锚点。
2. 当前审计脚本仍会按普通页面逻辑检查其中的剂量、休药期、监管术语。
3. 需要在 Phase 8 中增加综合页专用护栏，并更新审计脚本对 synthesis/regulatory 页面的识别逻辑。

## 10. 本阶段结论

Phase 7 已完成大体量疾病页运行时正文压缩。3 个目标疾病页全部退出中风险，运行时页面总计减少 40524 bytes，迁移 12 个批处理证据块和 108 个 source anchors。修改后高风险保持 0，中风险从 4 降至 1，readiness score 保持 99。

本阶段的核心价值是把疾病页从“默认检索中暴露大量诊疗和候选处方事实”调整为“默认检索只保留核心疾病边界，详细证据进入扩展层”，从而降低生产和评估链路中的诊断、治疗、处方、监管和残留类幻觉风险。
