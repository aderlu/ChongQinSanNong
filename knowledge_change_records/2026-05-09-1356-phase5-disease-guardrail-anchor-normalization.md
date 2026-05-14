# Phase 5 疾病页运行时护栏锚点归一化记录

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：13:56（Asia/Shanghai，精确到时和分）
- 所属阶段：Phase 5
- 工作类型：疾病类 runtime wiki 页面护栏锚点补齐、审计指标复核、变更留痕

## 2. 本阶段执行前存在的问题

前四个阶段已经完成了运行时边界收敛、编码损伤隔离、药物证据扩展块迁移、药物页护栏锚点补齐，整体幻觉风险已经明显下降。但 Phase 4 后仍存在以下问题：

1. 疾病类页面缺少统一的运行时护栏锚点。
   - 疾病页中包含诊断、病原检测、临床表现、鉴别诊断、防控、监管处置、可能治疗相关内容。
   - 如果没有统一锚点，生产链路和评估链路在检索后较难稳定识别哪些内容只能作为知识背景，哪些内容必须转入官方法规、检测标准、兽医处方或标签核验。

2. `partial` 或 `NEEDS_REVIEW` 疾病页容易被误当成完整知识页。
   - 这类页面本意是缺口定位和检索路由，但如果没有明确标识，模型可能补全缺失环节，增加事实编造和过度推断风险。

3. Phase 4 后仍有中风险运行时条目。
   - 最新审计中高风险已经为 0，但中风险仍为 40。
   - 其中一部分来自疾病页缺少诊断、监管、用药边界提示，导致页面虽然可用，但对生产和评估链路仍不够“可控”。

## 3. 修改前代码与知识库状态

修改前已有以下代码和机制：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
  - 用于生成运行时核心知识清单。
  - 会排除 `raw/**`、`issues/**`、`wiki/sessions/**`、`wiki/exports/**`、`wiki/evidence_expansions/**` 等非运行时目录。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`
  - 用于检查运行时知识页是否存在幻觉诱发风险。
  - 会输出高、中、低、无风险分布。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase4_apply_drug_guardrail_anchors.py`
  - 已经对药物页补齐 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001` 等锚点。

但修改前还没有一个专门面向疾病页的批量护栏锚点归一化工具。疾病页仍缺少统一的诊断边界、监管边界、疾病页不得生成处方边界、休药期和残留核验边界。

## 4. 本阶段新增或更新的代码

本阶段新增工具：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase5_apply_disease_guardrail_anchors.py`

该工具的作用：

1. 读取 `exports/runtime_core_manifest.json`，只处理 `entity_type == disease` 的运行时疾病页。
2. 在疾病页 H1 标题后插入统一的运行时疾病护栏锚点区块。
3. 对所有疾病页补齐以下锚点：
   - `RC-DX-001`：诊断必须区分临床怀疑、样本类型、检测方法、病原检出、因果关系和鉴别诊断。
   - `RC-DISEASE-REGULATORY-001`：报告、隔离、扑杀、移动控制、检疫和监管处置必须依赖当前官方或监管来源。
   - `RC-DRUG-001`：疾病页不得独立生成可执行用药处方、剂量、给药途径或疗程。
   - `RC-WITHDRAWAL-MRL-001`：休药期、MRL、残留、可食组织和食品安全相关结论必须进行当前标签或监管核验。
4. 对 `partial` 或 `NEEDS_REVIEW` 页面增加说明：这类页面只能作为检索和缺口路由页，缺失内容不得由模型猜测补全。
5. 输出本阶段机器可读和人工可读报告：
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase5_disease_guardrail_anchors_2026-05-09.json`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase5_disease_guardrail_anchors_2026-05-09.md`

## 5. 本阶段进行了哪些整理更新工作

本阶段实际处理结果如下：

- 检查疾病页：73 个
- 修改疾病页：73 个
- 其中 `partial` 疾病页修改：32 个
- 修改后仍缺失疾病护栏锚点的页面：0 个

本阶段并未扩写疾病正文，也没有新增未经验证的医学、兽医或法规事实。整理重点是给已有疾病知识页增加运行时边界，使其更适合被生产链路和评估链路安全调用。

## 6. 修改后解决了什么问题

本阶段完成后，疾病页的关键边界被显式化：

1. 降低诊断幻觉风险。
   - 模型在引用疾病页时会看到诊断不能只凭症状直接下结论，需要区分检测、样本、病原检出和鉴别诊断。

2. 降低监管处置幻觉风险。
   - 涉及报告、隔离、扑杀、移动控制、检疫等内容时，疾病页会明确要求转向当前官方或监管来源。

3. 降低疾病页越权生成处方的风险。
   - 疾病页明确不能独立生成剂量、给药途径、疗程等可执行用药方案。

4. 降低休药期、MRL、残留和食品安全相关幻觉风险。
   - 这些高风险结论必须经标签或监管来源核验，不能由疾病页直接推断。

5. 让 `partial` / `NEEDS_REVIEW` 页面从“可能被误读为完整知识”变为“明确的缺口路由页”。
   - 有助于评估系统识别知识不完整状态，减少模型补全缺失事实。

## 7. 验证结果

执行 Phase 5 工具后得到结果：

```json
{
  "disease_pages_checked": 73,
  "disease_pages_changed": 73,
  "partial_disease_pages_changed": 32,
  "missing_anchor_after": 0,
  "report_json": "issues/phase5_disease_guardrail_anchors_2026-05-09.json",
  "report_md": "issues/phase5_disease_guardrail_anchors_2026-05-09.md"
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
  "medium": 10
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

## 8. 预计产生的效果

1. 生产链路检索疾病页时，会更容易识别疾病知识的使用边界。
2. 评估链路可以把疾病类回答中的诊断、监管、用药、残留相关断言映射到明确的 rule-card 锚点。
3. 疾病页和药物页的高风险边界开始形成一致结构，减少不同页面之间的提示风格漂移。
4. 对 `partial` 疾病页的使用会更谨慎，减少模型将缺口页面当成完整权威页使用。
5. 幻觉风险审计指标继续下降：高风险保持 0，中风险从 Phase 4 后的 40 降至 10。

## 9. 当前仍未完全处理的问题

Phase 5 完成后，运行时知识库仍存在一些后续需要处理的问题：

1. 仍有 10 个中风险条目。
   - 主要原因不再是缺少疾病护栏锚点，而是页面体量较大、候选事实密集、药物或疾病页面仍含较多需要进一步结构化的事实。

2. 部分大体量药物页仍需要继续拆分或事实表结构化。
   - 代表页面包括 `DRUG-015-tylosin`、`DRUG-021-doxycycline`、`DRUG-013-tiamulin`、`DRUG-012-florfenicol`、`DRUG-010-amoxicillin`、`DRUG-019-oxytetracycline`。

3. 部分大体量疾病页仍需要继续压缩运行时正文或迁移扩展证据。
   - 代表页面包括 `DIS-035`、`DIS-052`、`DIS-044`。

4. `swine_regulatory_blocking_rules_china` 仍被审计脚本识别为中风险。
   - 原因是该页面属于综合规则/监管阻断类页面，内容中包含政策和阻断术语，但目前审计规则仍按普通页面的护栏锚点进行判断。
   - 后续可以在 Phase 6 中补充 synthesis/regulatory 页面专用锚点，或调整审计脚本对综合规则页的判定逻辑。

## 10. 本阶段结论

Phase 5 已完成疾病页运行时护栏锚点归一化。该阶段没有增加新的未经验证事实，而是对 73 个疾病运行时页面补齐诊断、监管、用药、休药期和残留相关边界提示。修改后疾病页缺失护栏锚点数量为 0，高风险条目保持 0，中风险条目从 40 降至 10。

当前知识库已经比 Phase 1 前更适合进入生产和评估链路，但仍建议继续执行下一阶段：对剩余中风险的大体量药物页、疾病页和综合监管页做结构化压缩、证据迁移或专用规则锚点处理。
