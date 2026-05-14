# Phase 8 综合监管与 synthesis 页面专用护栏记录

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：14:44（Asia/Shanghai，精确到时和分）
- 所属阶段：Phase 8
- 工作类型：synthesis/regulatory 页面专用护栏补齐、审计脚本类型识别更新、幻觉风险回归审计

## 2. 本阶段执行前存在的问题

Phase 7 完成后，高风险条目保持 0，中风险条目从 4 降至 1。剩余唯一中风险条目是：

- `wiki/synthesis/swine_regulatory_blocking_rules_china.md`

该页面属于综合监管/阻断规则页，不是普通疾病页或药物页。它的作用是用于生产链路和评估链路中的规则路由、阻断、拒答、权威源升级，而不是提供新的疾病、药物、剂量、休药期或监管事实。

修改前主要问题：

1. 综合监管页中包含“禁用药、剂量、休药期、检疫、扑杀、食品处理”等高风险术语。
2. 审计脚本按普通页面逻辑扫描这些术语，导致 synthesis/policy 页面被判为中风险。
3. synthesis 页面缺少统一的专用锚点，不能明确说明“这是规则/路由/评估页，不是事实来源页”。
4. `swine_case_generation_context`、`swine_answer_evaluation_rubric`、`swine_drug_and_withdrawal_boundary` 等同类页面也需要统一的 synthesis/regulatory 护栏，以避免后续再次被普通页面规则误判。

## 3. 修改前代码状态

修改前已有以下代码能力：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
  - 可识别 `entity_type=synthesis`、`runtime_tier=runtime_core_policy` 等 manifest 信息。

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`
  - 可审计页面体量、候选事实密度、缺失药物/疾病护栏等风险。

- Phase 4 和 Phase 5 已分别补齐药物页、疾病页护栏。

但修改前审计脚本仍缺少 synthesis/policy 类型的专门处理逻辑。它会把综合规则页中的监管、用药、休药期术语当作普通事实页风险，而不是识别为“规则页本身用于阻断和源升级”。

## 4. 本阶段新增或更新的代码

本阶段新增工具：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase8_apply_synthesis_regulatory_guardrails.py`

该工具完成以下工作：

1. 对 synthesis/regulatory 目标页面插入 `Synthesis/regulatory runtime guardrails / Phase 8` 区块。
2. 补齐以下专用锚点：
   - `RC-SYNTHESIS-SCOPE-001`：综合页只能用于规则组合、检索策略、阻断和评估，不得生成新的疾病、药物、剂量、休药期、MRL、残留或监管事实。
   - `RC-REGULATORY-CURRENT-001`：报告、隔离、扑杀、移动控制、检疫、禁用药、休药期、MRL、残留和法域合规结论必须核验当前官方/监管来源。
   - `RC-EVAL-RUBRIC-001`：评估规则和阻断规则只用于评分、路由、拒答或源升级，不是独立事实证据。
   - `RC-DRUG-001`：药物、剂量、给药途径、疗程、配伍、禁忌或处方内容必须通过药物页、证据扩展和标签/监管核验。
   - `RC-WITHDRAWAL-MRL-001`：休药期、MRL、残留和食品安全结论必须进行当前标签/监管核验。
3. 输出报告：
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase8_synthesis_regulatory_guardrails_2026-05-09.json`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase8_synthesis_regulatory_guardrails_2026-05-09.md`

本阶段更新审计脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`

更新内容：

1. 新增 synthesis policy 识别逻辑。
2. 对 `entity_type=synthesis` 且 `runtime_tier=runtime_core_policy` 或 `runtime_core_context` 的页面，识别为 synthesis policy 页面。
3. 对已具备 `RC-SYNTHESIS-SCOPE-001`、`RC-REGULATORY-CURRENT-001`、`RC-EVAL-RUBRIC-001` 的页面，不再按普通疾病/药物事实页口径计算“监管术语缺少护栏”风险。
4. 若 synthesis policy 页面缺少 Phase 8 锚点，则输出 `synthesis_policy_without_phase8_guardrails`。

## 5. 本阶段进行了哪些整理更新工作

本阶段为以下页面建立或补齐 synthesis/regulatory 专用护栏：

- `wiki/synthesis/swine_regulatory_blocking_rules_china.md`
- `wiki/synthesis/swine_drug_and_withdrawal_boundary.md`
- `wiki/synthesis/swine_case_generation_context.md`
- `wiki/synthesis/swine_answer_evaluation_rubric.md`

执行过程说明：

1. 第一次执行时，对 3 个 synthesis 页面补齐专用锚点。
2. 回归审计发现同类页面 `swine_drug_and_withdrawal_boundary` 仍被识别为缺少 Phase 8 护栏。
3. 随后将该页面加入 Phase 8 目标列表并再次执行。
4. 最终 4 个 synthesis/policy 页面均具备核心专用锚点，缺失数量为 0。

最终报告显示：

```json
{
  "pages_checked": 4,
  "pages_changed": 1,
  "missing_core_synthesis_anchors_after": 0
}
```

说明：最终报告是第二次幂等执行结果，其中前 3 个页面已在第一次执行时完成变更，因此第二次只新增修改了 `swine_drug_and_withdrawal_boundary`。

本阶段没有新增疾病、药物、剂量、休药期、MRL 或监管事实，只补充页面类型边界和审计识别逻辑。

## 6. 修改后解决了什么问题

本阶段解决了以下问题：

1. synthesis/regulatory 页面不再被当作普通事实页误判。
2. 综合监管页中的高风险术语被明确限定为“阻断、路由、源升级和评估规则”，而非可直接生成的事实。
3. 生产链路可以更清楚地区分：
   - 疾病页：用于临床知识检索和诊断边界。
   - 药物页：用于药物边界和标签核验路由。
   - synthesis/policy 页：用于阻断、拒答、源升级和评估。
4. 评估链路可以用 `RC-SYNTHESIS-SCOPE-001`、`RC-REGULATORY-CURRENT-001`、`RC-EVAL-RUBRIC-001` 判断综合规则页是否被误用为事实来源。
5. 剩余中风险条目被清零。

## 7. 验证结果

执行 Phase 8 工具后得到最终结果：

```json
{
  "pages_checked": 4,
  "pages_changed": 1,
  "missing_core_synthesis_anchors_after": 0,
  "report_json": "issues/phase8_synthesis_regulatory_guardrails_2026-05-09.json",
  "report_md": "issues/phase8_synthesis_regulatory_guardrails_2026-05-09.md"
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
  "low": 97,
  "none": 101
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

4 个目标 synthesis/policy 页面在最新风险 JSON 中均已降为：

```json
{
  "risk_score": 0,
  "findings": []
}
```

## 8. 预计产生的效果

1. 生产链路在遇到监管、禁用药、休药期、MRL、残留、扑杀、检疫等高风险话题时，更容易触发阻断或官方源升级。
2. synthesis 页面不会再被误用为新的事实生成来源。
3. 评估系统能更稳定地区分“知识事实错误”和“规则页正确触发阻断/拒答”。
4. 审计脚本对页面类型的理解更精细，后续误报会减少。
5. 高风险和中风险均清零，说明前八阶段的运行时高风险治理已经完成主要闭环。

## 9. 当前仍未完全处理的问题

Phase 8 完成后，高风险和中风险已经为 0，但仍有 97 个低风险条目。低风险主要来自：

1. 部分疾病页体量仍较大，例如 `DIS-046`、`DIS-049`、`DIS-055`、`DIS-041`、`DIS-040`、`DIS-051`。
2. 部分页面仍为 `partial` 或 `NEEDS_REVIEW`，适合作为缺口路由页，但不应被当作完整知识页。
3. 个别药物页如 `DRUG-042-ampicillin` 仍有页面体量和候选事实密度问题，但目前处于低风险，不阻塞生产链路。

建议下一步执行 Phase 9：低风险页面收尾治理与全量回归审计。

## 10. 本阶段结论

Phase 8 已完成 synthesis/regulatory 页面专用护栏建设，并更新了幻觉风险审计脚本的页面类型识别逻辑。最终高风险为 0，中风险为 0，readiness score 保持 99。

本阶段的核心价值是让综合监管、药物边界、case generation 和 evaluation rubric 页面从“可能被普通事实页规则误判”转为“明确的策略、阻断、评估和源升级页面”，从而降低生产和评估链路在监管、处方、休药期、MRL 和残留问题上的误用风险。
