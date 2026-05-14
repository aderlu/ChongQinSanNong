# Phase 4 药物页规则卡锚点统一执行记录

落地时间：2026-05-09 13:46 +08:00

## 本阶段目标

按照 `2026-05-09-wiki-phased-cleanup-plan.md` 的 Phase 4，统一 runtime 药物页的规则卡边界锚点。

核心目标：

- 所有 runtime 药物页都显式包含 `RC-DRUG-001`。
- 所有 runtime 药物页都显式包含 `RC-WITHDRAWAL-MRL-001`。
- 让生产链路、评估链路和审计脚本能稳定识别药物页的使用边界。
- 不新增药物事实，不改变来源事实，只补充 runtime guardrail metadata。

## 修改前存在的问题

Phase 3 后，high 风险已经清零，但仍有 102 个 medium 风险项。

其中主要问题之一是：

- 80 个 runtime 药物页中，有 63 个缺少 `RC-DRUG-001` 或 `RC-WITHDRAWAL-MRL-001` 字面锚点。

修改前风险：

- 药物页虽然有边界说明，但机器审计和生产链路不一定能稳定识别。
- 当页面含有剂量、疗程、休药期、MRL、残留、食品安全等词时，审计脚本会继续标记为缺少规则卡锚点。
- 评估系统可能把药物页当作直接处方依据，而不是边界页或召回入口。

## 修改前相关代码和知识库状态

已有代码：

- `tools/build_runtime_core_manifest.py`：生成 runtime manifest 和 exclude patterns。
- `tools/audit_runtime_hallucination_risk.py`：检查 runtime 幻觉风险。
- `tools/phase3_move_drug_evidence_expansions.py`：迁移 high 风险药物页的大型证据块。

修改前审计状态：

- runtime manifest entries: 198
- runtime missing paths: 0
- hallucination risk audit:
  - high: 0
  - medium: 102
  - low: 50
  - none: 46
- drug pages missing any required anchor: 63
- readiness score: 99/100

## 本阶段新增或更新的代码

新增脚本：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase4_apply_drug_guardrail_anchors.py`

脚本功能：

- 读取 `exports/runtime_core_manifest.json`。
- 只处理 `entity_type=drug` 的 runtime 药物页。
- 检查每个药物页是否包含：
  - `RC-DRUG-001`
  - `RC-WITHDRAWAL-MRL-001`
- 对缺失锚点的药物页，在 H1 标题下插入统一的 `Runtime guardrail anchors / Phase 4` 小节。
- 小节中写入 runtime tier、evidence status 和规则卡边界。
- 生成 JSON 和 Markdown 执行报告。

## 本阶段整理或更新的知识库内容

批量更新：

- 检查 runtime 药物页：80 个。
- 修改 runtime 药物页：63 个。
- 修改后缺失锚点：0 个。

新增执行报告：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase4_drug_guardrail_anchors_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/phase4_drug_guardrail_anchors_2026-05-09.md`

被更新的页面类型：

- `runtime_core_reviewed` 药物页。
- `runtime_core_partial` 药物页。
- `regulatory_boundary_page` 药物页。

新增小节示例：

```md
## Runtime guardrail anchors / Phase 4

- Runtime tier: `runtime_core_reviewed`; evidence status: `source_anchored_drug_evidence_page`.
- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Dose, route, course, compatibility, contraindication, withdrawal, MRL, and jurisdiction-specific compliance answers must use source expansion and rule-card gating.
```

## 修改后解决了什么

### 1. 药物页规则卡锚点统一

修改后：

- drug pages missing anchor: 0
- 所有 runtime 药物页都有 `RC-DRUG-001`
- 所有 runtime 药物页都有 `RC-WITHDRAWAL-MRL-001`

预期效果：

- 生产链路可以稳定识别“药物页不是独立处方源”。
- 评估链路可以把剂量、疗程、休药期、MRL 等内容纳入规则卡检查。
- 审计脚本不再把药物页大量误判为“缺少规则卡锚点”。

### 2. hallucination risk audit 明显下降

修改前：

- high: 0
- medium: 102
- low: 50
- none: 46

修改后：

- high: 0
- medium: 40
- low: 75
- none: 83

预期效果：

- 药物页的默认运行时风险显著下降。
- 剩余 medium 风险更集中，便于后续阶段继续定向处理。

### 3. 没有改变原始药物事实

本阶段没有新增药物适应证、剂量、疗程、休药期或 MRL 事实。

预期效果：

- 保持知识库事实层稳定。
- 将修改限定在 runtime 元数据和边界提示层。

## 验证命令和结果

执行 Phase 4 锚点补齐：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase4_apply_drug_guardrail_anchors.py`

结果：

- drug_pages_checked: 80
- drug_pages_changed: 63
- missing_anchor_after: 0

重新生成 runtime manifest：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py`

结果：

- entries: 198
- missing_paths: 0

运行 hallucination risk audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py`

结果：

- entries_checked: 198
- high: 0
- medium: 40

运行原 readiness audit：

`python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py`

结果：

- readiness_score: 99
- missing_paths: 0
- bad_fact_tables: 0
- missing_rule_cards: 0
- missing_synthesis: 0

额外核验：

- runtime 药物页缺失规则卡锚点数量：0

## 后续遗留问题

Phase 4 后，medium 风险从 102 降到 40。剩余 medium 风险主要来自：

- 少数仍然较大的药物页，例如 `DRUG-015-tylosin`、`DRUG-021-doxycycline`。
- 部分疾病页仍含候选事实、药物/休药期/监管词，且疾病页尚未做类似的规则卡锚点统一。

下一步建议：

- Phase 5 处理疾病页 runtime guardrail，尤其是 `NEEDS_REVIEW` 疾病页和含药物/监管词的疾病页。
- 对仍较大的 medium 药物页继续做 evidence expansion 迁移。
- 将生产链路接入 `runtime_core_manifest.json`，并基于规则卡锚点做回答前 gating。

