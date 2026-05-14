# Phase 9 低风险页面收尾治理与回归审计记录

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：14:56（Asia/Shanghai，精确到时和分）
- 所属阶段：Phase 9
- 工作类型：低风险大页收尾压缩、partial 页面缺口路由标注、最终回归审计

## 2. 本阶段执行前存在的问题

Phase 8 完成后，高风险和中风险已经清零，运行时知识库已经完成主要高风险治理闭环。但仍存在 97 个低风险条目。

低风险问题主要分为两类：

1. 低风险大体量页面仍有少量候选事实。
   - 代表页面包括 `DIS-046`、`DIS-049`、`DIS-055`、`DRUG-042-ampicillin`、`DIS-041`、`DIS-040`、`DIS-051`、`DIS-008`、`DIS-009`、`DIS-024`、`DIS-026`。
   - 这些页面虽然不再构成高/中风险，但默认运行时正文仍包含批处理增强块，可能带来检索噪声。

2. `runtime_core_partial` 页面仍作为低风险项出现。
   - partial 页面本意是召回、鉴别诊断路由和缺口追踪。
   - 如果没有统一说明，生产链路和评估链路可能误把 partial 页面当作完整知识页，进而补全缺失事实。

## 3. 修改前代码状态

修改前已有以下代码能力：

- `tools/build_runtime_core_manifest.py`
  - 负责生成运行时核心 manifest。

- `tools/audit_runtime_hallucination_risk.py`
  - 负责输出高、中、低、无风险分布。

- `tools/phase6_compact_high_density_drug_pages.py`
  - 已处理高密度药物页。

- `tools/phase7_compact_high_density_disease_pages.py`
  - 已处理高密度疾病页。

- `tools/phase8_apply_synthesis_regulatory_guardrails.py`
  - 已处理 synthesis/regulatory 页面专用护栏。

修改前缺少一个统一收尾脚本，用于：

1. 对低风险大页做轻量证据迁移。
2. 对 partial 页面补充统一缺口路由说明。
3. 输出最终回归报告。
4. 让审计脚本识别已受控的 partial 页面，避免把“已标注的缺口页”当成未治理风险。

## 4. 本阶段新增或更新的代码

本阶段新增工具：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase9_runtime_cleanup_regression.py`

该工具完成以下工作：

1. 对 11 个低风险大体量页面迁移批处理增强证据块。
2. 将迁移内容写入：
   - `wiki/evidence_expansions/diseases/phase9/`
   - `wiki/evidence_expansions/drugs/phase9/`
3. 在原运行时页面中保留短占位符，指向 evidence expansion 文件。
4. 在被压缩页面中加入 `Runtime low-risk cleanup / Phase 9` 区块。
5. 对所有 `runtime_core_partial` 页面加入 `Partial page gap-routing / Phase 9` 区块。
6. 输出报告：
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase9_runtime_cleanup_regression_2026-05-09.json`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase9_runtime_cleanup_regression_2026-05-09.md`

本阶段更新审计脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`

更新内容：

1. 新增 `RC-PARTIAL-GAP-ROUTING-001` 识别逻辑。
2. 对已经标注缺口路由的 partial 页面，不再按“未治理 partial”计入风险分。
3. 保留对其他候选事实、页面体量、监管/用药术语的审计能力。

## 5. 本阶段进行了哪些整理更新工作

本阶段实际处理结果如下：

- 低风险大页检查：11 个
- 低风险大页修改：11 个
- 迁移证据块：50 个
- 迁移 fact-like rows：336 行
- 迁移 `candidate_fact`：39 个
- 迁移 source anchors：347 个
- 运行时页面总字节减少：155100 bytes
- partial 页面检查：41 个
- partial 页面新增缺口路由说明：41 个

被压缩的页面：

- `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`
- `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `wiki/diseases/DIS-040-colibacillosis.md`
- `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- `wiki/diseases/DIS-049-salmonellosis.md`
- `wiki/diseases/DIS-051-streptococcosis-streptococcus-suis.md`
- `wiki/diseases/DIS-055-external-parasites-mange.md`
- `wiki/drugs/DRUG-042-ampicillin.md`

本阶段没有新增未经验证的疾病、药物、剂量、休药期、MRL、残留或监管事实。所有操作都是运行时结构整理、证据扩展迁移和缺口页边界标注。

## 6. 修改后解决了什么问题

本阶段解决了以下问题：

1. 低风险大页的批处理增强证据不再默认暴露在运行时检索层。
2. 11 个页面的运行时上下文更短，默认召回噪声降低。
3. partial 页面统一标注为受控缺口路由页，缺失字段不得由模型猜测补全。
4. 评估链路可以明确区分“知识缺失但已标注”和“未治理风险”。
5. 低风险条目从 97 降至 45，进一步降低生产和评估链路的噪声。

## 7. 验证结果

执行 Phase 9 工具后得到结果：

```json
{
  "compaction_pages_checked": 11,
  "compaction_pages_changed": 11,
  "blocks_moved": 50,
  "candidate_fact_mentions_moved": 39,
  "bytes_reduced": 155100,
  "partial_pages_checked": 41,
  "partial_pages_changed": 41,
  "report_json": "issues/phase9_runtime_cleanup_regression_2026-05-09.json",
  "report_md": "issues/phase9_runtime_cleanup_regression_2026-05-09.md"
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
  "medium": 0,
  "low": 45,
  "none": 153
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

1. 生产链路默认检索上下文更短，候选事实噪声更低。
2. partial 页面不会被误读为完整知识页，减少模型补全缺失事实的风险。
3. 评估系统可以更稳定地区分页面类型、证据扩展层和缺口路由页。
4. evidence expansion 层保留详细证据，便于人工复核、审计和后续外部权威源补充。
5. 前九阶段形成完整治理闭环：高风险和中风险清零，低风险显著下降。

## 9. 当前仍未完全处理的问题

Phase 9 完成后仍有 45 个低风险条目，主要包括：

1. 个别药物页仍有少量 `candidate_fact`，例如 `DRUG-002-ivermectin`、`DRUG-024-neomycin`、`DRUG-045-tilmicosin`、`DRUG-052-colistin`。
2. 个别疾病页仍因页面体量略大或少量候选事实处于低风险，例如 `DIS-018`、`DIS-028`。
3. 少量 rule card、comparison、syndrome 页面中包含监管、休药期或剂量术语，被审计脚本作为低风险提示保留。
4. 这些低风险项当前不阻塞生产链路，但适合后续按人工审校或外部权威源补充计划继续治理。

建议后续维护方式：

1. 每次新增来源或批处理增强块后，先运行 runtime manifest 和 hallucination risk audit。
2. 新增大段证据默认进入 evidence expansion，不直接放入运行时核心页。
3. partial 页面只有在完成事实补齐和人工审核后，才从缺口路由页升级为完整临床页。
4. 涉及药物、剂量、疗程、休药期、MRL、残留和监管动作的内容，继续强制执行 rule-card gating 和当前标签/监管核验。

## 10. 本阶段结论

Phase 9 已完成低风险页面收尾治理和全量回归审计。最终结果为高风险 0、中风险 0、低风险 45、无风险 153，readiness score 保持 99。

本阶段的核心价值是把前八阶段后的剩余低风险噪声进一步压低，并把 partial 页面统一纳入受控缺口路由体系。至此，当前 wiki 知识库已经从最初的杂乱、冗余和高事实密度状态，整理为运行时核心页、证据扩展层、规则护栏和工作留痕文档并存的可维护结构。
