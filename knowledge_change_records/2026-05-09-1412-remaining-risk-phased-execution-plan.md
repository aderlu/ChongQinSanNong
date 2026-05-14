# 剩余问题分段执行方案与留痕要求

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：14:12（Asia/Shanghai，精确到时和分）
- 文档类型：Phase 5 后剩余问题的后续分段执行方案
- 适用范围：`ai-/knowledge/llm_wiki_swine_authoritative` 运行时 wiki 知识库
- 记录目录：`knowledge_change_records`

## 2. 当前状态概览

Phase 1 到 Phase 5 已经完成运行时边界收敛、编码损伤隔离、药物证据扩展迁移、药物页护栏锚点补齐、疾病页护栏锚点补齐。当前运行时知识库已经具备较清晰的生产和评估边界。

最新审计结果如下：

```json
{
  "runtime_entries": 198,
  "missing_paths": 0,
  "hallucination_risk_high": 0,
  "hallucination_risk_medium": 10,
  "hallucination_risk_low": 100,
  "hallucination_risk_none": 88,
  "readiness_score": 99
}
```

当前已经解决的问题：

1. 非运行时目录已经从核心 manifest 中排除。
2. 明显编码损伤内容已经隔离。
3. 药物页的大段 batch evidence 扩展内容已经迁移到 `wiki/evidence_expansions/drugs/`。
4. 药物页已经补齐 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001` 等运行时护栏锚点。
5. 疾病页已经补齐 `RC-DX-001`、`RC-DISEASE-REGULATORY-001`、`RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001` 等运行时护栏锚点。

## 3. 当前仍然存在的问题

Phase 5 后，高风险条目已经为 0，但仍有 10 个中风险条目。这些问题不再主要是“缺少基础护栏”，而是进入了更细的结构化治理阶段。

### 3.1 大体量药物页仍然事实密集

中风险药物页包括：

- `wiki/drugs/DRUG-015-tylosin.md`
- `wiki/drugs/DRUG-021-doxycycline.md`
- `wiki/drugs/DRUG-013-tiamulin.md`
- `wiki/drugs/DRUG-012-florfenicol.md`
- `wiki/drugs/DRUG-010-amoxicillin.md`
- `wiki/drugs/DRUG-019-oxytetracycline.md`

主要问题：

1. 页面字节数仍然较大。
2. 候选事实密集，检索后容易一次性带入过多上下文。
3. 同一页面内可能同时包含适应证、限制、标签、残留、剂量、证据摘要等多类信息。
4. 即使已经有护栏锚点，生产链路仍可能在长上下文中混淆“知识背景”和“可执行建议”。

### 3.2 大体量疾病页仍然需要压缩运行时正文

中风险疾病页包括：

- `wiki/diseases/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md`
- `wiki/diseases/DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md`
- `wiki/diseases/DIS-044-gl-sser-s-disease.md`

主要问题：

1. 页面体量偏大，候选事实数量较多。
2. 疾病页虽然已经补齐护栏，但正文仍可能混合临床表现、病原学、诊断、防控、治疗相关背景。
3. 检索阶段如果直接召回整页，可能增加模型过度概括或跨段拼接事实的风险。

### 3.3 综合监管页需要专用锚点和审计规则

中风险综合页：

- `wiki/synthesis/swine_regulatory_blocking_rules_china.md`

主要问题：

1. 该页面属于综合规则/监管阻断类页面，不是普通疾病页或药物页。
2. 现有审计脚本仍会按普通页面检查用药、休药期、监管术语护栏。
3. 页面本身可能需要 synthesis/regulatory 专用锚点，而不是简单套用疾病页或药物页锚点。

### 3.4 低风险页面仍有后续治理空间

低风险页面中仍有部分大页和 `partial` 页面，例如 `DIS-046`、`DIS-049`、`DIS-055`、`DRUG-042`、`swine_case_generation_context`、`swine_answer_evaluation_rubric` 等。它们当前不阻塞生产链路，但适合在中风险条目处理完后继续治理。

## 4. 修改前代码状态

当前已有工具如下：

- `tools/build_runtime_core_manifest.py`
  - 负责生成运行时核心 manifest。

- `tools/audit_runtime_hallucination_risk.py`
  - 负责对 runtime 页面进行幻觉风险审计。

- `tools/quarantine_encoding_damaged_lines.py`
  - 负责隔离编码损伤行。

- `tools/phase3_move_drug_evidence_expansions.py`
  - 负责迁移药物页 batch evidence 扩展块。

- `tools/phase4_apply_drug_guardrail_anchors.py`
  - 负责补齐药物页运行时护栏锚点。

- `tools/phase5_apply_disease_guardrail_anchors.py`
  - 负责补齐疾病页运行时护栏锚点。

当前还缺少的代码能力：

1. 缺少面向剩余大体量药物页的“运行时核心摘要 + 扩展证据迁移 + 事实密度审计”工具。
2. 缺少面向剩余大体量疾病页的“运行时正文压缩 + 非核心证据迁移 + 诊断/防控边界复核”工具。
3. 缺少 synthesis/regulatory 页面专用锚点工具。
4. `audit_runtime_hallucination_risk.py` 对 synthesis/regulatory 页面还没有单独类型判断，容易把综合规则页按普通页面误判。

## 5. 后续分段执行方案

### Phase 6：大体量药物页二次结构化与证据迁移

处理对象：

- `DRUG-015-tylosin`
- `DRUG-021-doxycycline`
- `DRUG-013-tiamulin`
- `DRUG-012-florfenicol`
- `DRUG-010-amoxicillin`
- `DRUG-019-oxytetracycline`

计划新增或更新代码：

- 新增 `tools/phase6_compact_high_density_drug_pages.py`
- 可选新增 `issues/phase6_drug_page_compaction_2026-05-09.json`
- 可选新增 `issues/phase6_drug_page_compaction_2026-05-09.md`

整理动作：

1. 对上述 6 个药物页建立运行时核心区块。
2. 将非运行时证据、长列表、重复来源摘要迁移到 `wiki/evidence_expansions/drugs/phase6/`。
3. 保留页面中的核心身份、用途边界、禁忌/限制、标签核验要求、残留/休药期核验要求。
4. 避免新增未经验证的剂量、疗程、适应证或监管结论。

预期效果：

1. 药物页召回内容更短、更稳定。
2. 候选事实密度下降。
3. 中风险药物页数量下降。
4. 生产链路更不容易把背景知识误转成可执行处方。

验收指标：

1. 高风险仍为 0。
2. 中风险条目少于 10。
3. 6 个目标药物页中至少 4 个不再处于中风险。
4. runtime manifest 缺失路径为 0。

本阶段必须新增留痕文档：

- `knowledge_change_records/2026-05-09-HHMM-phase6-drug-page-compaction.md`

留痕文档必须说明：

1. 修改前药物页存在什么问题。
2. 修改前已有代码能力是什么，缺少什么。
3. 新增或更新了什么脚本。
4. 哪些药物页被整理，哪些内容迁移到了 evidence expansions。
5. 修改后解决了什么。
6. 验证指标和预计效果。

### Phase 7：大体量疾病页运行时正文压缩

处理对象：

- `DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia`
- `DIS-052-swine-dysentery-brachyspira-hyodysenteriae`
- `DIS-044-gl-sser-s-disease`

计划新增或更新代码：

- 新增 `tools/phase7_compact_high_density_disease_pages.py`
- 可选新增 `issues/phase7_disease_page_compaction_2026-05-09.json`
- 可选新增 `issues/phase7_disease_page_compaction_2026-05-09.md`

整理动作：

1. 对 3 个疾病页拆出运行时核心摘要。
2. 将长证据、细碎背景、重复说明迁移到 `wiki/evidence_expansions/diseases/phase7/`。
3. 保留疾病身份、主要综合征、诊断边界、鉴别诊断提醒、防控边界、监管边界。
4. 明确治疗相关内容只能指向兽医诊疗和药物页护栏，不在疾病页生成处方。

预期效果：

1. 疾病页检索更聚焦。
2. 诊断类回答更容易遵循 `RC-DX-001`。
3. 防控和监管处置更容易触发官方来源核验。
4. 中风险疾病页数量下降。

验收指标：

1. 高风险仍为 0。
2. 3 个目标疾病页不再处于中风险，或风险分数明显下降。
3. runtime manifest 缺失路径为 0。
4. readiness score 不低于 99。

本阶段必须新增留痕文档：

- `knowledge_change_records/2026-05-09-HHMM-phase7-disease-page-compaction.md`

留痕文档必须说明：

1. 修改前疾病页为什么仍然偏冗长。
2. 修改前代码是否支持疾病页压缩。
3. 新增或更新了什么脚本。
4. 哪些疾病页被整理，迁移了哪些类型内容。
5. 修改后解决了什么。
6. 验证指标和预计效果。

### Phase 8：综合监管与 synthesis 页面专用护栏

处理对象：

- `wiki/synthesis/swine_regulatory_blocking_rules_china.md`
- 可扩展检查 `wiki/synthesis/swine_case_generation_context.md`
- 可扩展检查 `wiki/synthesis/swine_answer_evaluation_rubric.md`

计划新增或更新代码：

- 新增 `tools/phase8_apply_synthesis_regulatory_guardrails.py`
- 更新 `tools/audit_runtime_hallucination_risk.py`

整理动作：

1. 为 synthesis/regulatory 页面增加专用锚点，例如：
   - `RC-SYNTHESIS-SCOPE-001`：综合页只用于规则路由、评估和阻断，不直接生成新的事实结论。
   - `RC-REGULATORY-CURRENT-001`：监管结论必须核验当前官方来源。
   - `RC-EVAL-RUBRIC-001`：评估规则只用于判分和质量控制，不能被当作事实来源。
2. 在审计脚本中识别 synthesis/regulatory 页面，避免把综合页误判为普通疾病页或药物页。
3. 对仍存在监管、休药期、剂量词的综合页做显式边界标注。

预期效果：

1. 综合监管页不再因为普通页面规则而误报中风险。
2. 评估系统能更清楚地区分“事实知识页”和“规则/评估页”。
3. 生产链路更容易把监管内容路由到官方来源核验，而不是直接生成结论。

验收指标：

1. `swine_regulatory_blocking_rules_china` 不再处于中风险。
2. 高风险仍为 0。
3. 中风险条目继续下降。
4. 审计脚本对 synthesis/regulatory 类型有明确处理逻辑。

本阶段必须新增留痕文档：

- `knowledge_change_records/2026-05-09-HHMM-phase8-synthesis-regulatory-guardrails.md`

留痕文档必须说明：

1. 修改前综合页为什么被误判或仍有风险。
2. 修改前审计代码如何判断该类页面。
3. 修改后新增了哪些 synthesis/regulatory 锚点。
4. 审计代码如何更新。
5. 修改后解决了什么。
6. 验证指标和预计效果。

### Phase 9：低风险页面收尾治理与回归审计

处理对象：

- Phase 6 到 Phase 8 后仍处于 low 或 medium 的页面。
- 优先检查大体量低风险页面和 `partial` 页面。

计划新增或更新代码：

- 新增或更新 `tools/phase9_runtime_cleanup_regression.py`
- 可选更新 `tools/audit_runtime_hallucination_risk.py`
- 生成 `issues/phase9_runtime_cleanup_regression_2026-05-09.{json,md}`

整理动作：

1. 对低风险大页做轻量压缩，不做大规模事实改写。
2. 对 `partial` 页面补充一致的缺口路由说明。
3. 对所有 runtime 页面做最终回归审计。
4. 输出后续维护清单，区分“已处理”“待外部权威源核验”“适合后续人工审校”。

预期效果：

1. 运行时知识库进一步稳定。
2. 生产检索上下文更短、更可控。
3. 评估系统可以使用更清晰的知识边界和规则锚点。

验收指标：

1. 高风险为 0。
2. 中风险尽量降至 0，或仅保留需要外部权威源核验的合理例外。
3. readiness score 不低于 99。
4. runtime manifest 缺失路径为 0。
5. 输出完整回归报告。

本阶段必须新增留痕文档：

- `knowledge_change_records/2026-05-09-HHMM-phase9-runtime-cleanup-regression.md`

留痕文档必须说明：

1. 前几阶段完成后仍剩什么问题。
2. 本阶段是否修改代码、知识页或仅做审计。
3. 处理了哪些低风险页面。
4. 最终风险分布如何。
5. 对生产和评估链路的预计效果。
6. 后续仍需人工核验或外部权威源补充的内容。

## 6. 每次修改的统一留痕规范

后续每一个阶段都必须在 `knowledge_change_records` 下新增一个说明文档。文档命名建议：

```text
YYYY-MM-DD-HHMM-phaseN-short-topic.md
```

每份说明文档必须包含以下内容：

1. 落地时间。
   - 必须精确到时和分。
   - 必须标注时区。

2. 修改前存在的问题。
   - 说明知识库哪里杂乱、冗余或容易诱发幻觉。
   - 说明对生产链路和评估链路的潜在影响。

3. 修改前代码状态。
   - 说明已有工具是什么。
   - 说明缺少什么自动化能力。

4. 本次新增或更新的代码。
   - 列出新增脚本、更新脚本、输出报告路径。
   - 如果没有改代码，也要明确说明“本阶段未修改代码，仅做知识整理或审计”。

5. 本次整理更新工作。
   - 列出处理对象。
   - 说明迁移、压缩、补锚点或审计了什么。

6. 修改后解决了什么。
   - 对应到幻觉风险、召回噪声、事实密度、监管边界、用药边界等问题。

7. 验证结果。
   - 至少包含 manifest、hallucination risk audit、readiness audit。
   - 尽量给出修改前后对比。

8. 预计效果。
   - 面向生产链路。
   - 面向评估链路。
   - 面向后续维护。

9. 仍未解决的问题。
   - 每一阶段完成后都要留下下一阶段的问题清单。

## 7. 后续执行优先级

建议优先级如下：

1. Phase 6：先处理大体量药物页，因为药物页最容易引发剂量、疗程、休药期和残留相关高风险输出。
2. Phase 7：再处理大体量疾病页，重点降低诊断和防控类长上下文误用。
3. Phase 8：随后处理 synthesis/regulatory 页面，让审计规则和页面类型更匹配。
4. Phase 9：最后做低风险页面收尾和全量回归。

## 8. 总结

当前 wiki 已经不再是最初的杂乱状态：运行时边界、药物护栏、疾病护栏都已经建立。但剩余问题说明知识库还没有完全进入“轻量、结构化、低噪声”的最终形态。

后续工作的重点不是继续堆叠事实，而是减少运行时页面中的冗余事实密度，把长证据和扩展材料迁移到 evidence expansions，并让生产链路和评估链路只召回更短、更明确、更有边界的核心知识。

本文件作为 Phase 6 到 Phase 9 的执行依据。后续每一阶段完成后，都必须在 `knowledge_change_records` 下新增单独的工作记录，形成可以用于汇报、审计和回溯的连续留痕。
