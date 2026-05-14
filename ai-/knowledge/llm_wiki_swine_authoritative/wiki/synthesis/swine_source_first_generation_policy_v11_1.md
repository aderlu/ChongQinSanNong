---
tags: [synthesis, swine, source_first, generation_gate, v11_1]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, gold_candidate, audit_only, generation_gate]
sources: [RC-CITATION-001, RC-DRUG-GOLD-ROLE-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001]
---

# Swine Source-first Generation Policy / V11.1

## 核心原则

- 猪病诊断、鉴别诊断、采样、治疗候选、处方边界和评估结论均以来源可追溯性为第一约束。
- 可用来源范围放宽为：`A0-*`、`A1-*`、`A2-*`、`SRC-*`、`RC-*`、`RULE-*`。只要来源页、事实锚点、URL、PDF page、标签页或规则卡可追溯，且不是 `NEEDS_REVIEW`，即可进入生成和评估。
- `NEEDS_REVIEW` 仍可用于召回、追问、待核验提示和负例构造；不得作为最终诊断、处方、休药期或食品安全结论的唯一依据。

## 诊断和鉴别

- 疾病页、syndrome 页、comparison 页、textbook `SRC-*`、官方/权威网页 `A0/A1/A2-*` 和 rule card 均可支持诊断与鉴别。
- 诊断答案应说明支持证据、反证或缺失字段；不能仅凭单一症状锁定单病种。
- 实验室诊断结论必须绑定样本、检测方法、采样时间和阴性/阳性解释边界。

## 处方和用药

- 可生成处方或正向治疗答案的最低门槛不是“中国来源”，而是“具体标签或等效权威事实源”：必须能核对猪靶动物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL/残留边界和禁停用状态。
- 来源可以是 `A0/A1/A2/SRC/RC/RULE` 中任一类；但答案必须限定在该来源自身覆盖的法域、产品、制剂、动物种属和适应证内。
- `positive_label_candidate` 药物页可进入正向用药黄金题；`boundary_only` 用于追问、拒答、标签核验和风险边界；`negative_trap` 用于错误外推评估。
- 没有精确标签/事实源时，可以给出诊断、采样、药敏和兽医复核路径，但不输出执行性剂量、疗程、休药期或肉品可食承诺。

## 法域和监管表述

- 中国监管来源不再作为猪病生成和评估的默认唯一门槛。
- 只有当问题明确要求“中国合规”“当地执法/报告/检疫/扑杀/出栏/肉品可食”时，才必须回到相应法域的官方来源或明确标注“仅限所引来源法域”。
- 禁用、停用、淘汰、食品安全和公共卫生人员安全仍是硬边界；硬边界的来源可以来自已锚定的官方、权威教材、规则卡或标签源。

## 黄金集评估

- 正确答案优先奖励：来源清晰、事实真实、数据有效、边界限定准确。
- 主要扣分：无来源结论、把候选/类别/非猪标签外推为处方、把一个法域的标签伪装成另一法域合规、遗漏禁停用或人员安全硬边界。

<!-- LOCAL_RAW_MD_SUBSTITUTION_V15_START -->
## Local raw Markdown substitution / V15

- Local Markdown files under raw/md/ are accepted source anchors for pathogen biology, diagnostic reasoning, regulatory-boundary framing, disease-chapter evidence, sampling, differential diagnosis, biosecurity, treatment-objective boundaries, and public-health/food-safety context when they are linked to a specific book/manual, chapter, page range, or registered SRC-* page.
- This substitution is source-first, not status-first: a disease page may remain evidence_status: NEEDS_REVIEW while still retrieving locally anchored textbook/manual evidence for safer generation and evaluation.
- Local Markdown evidence cannot by itself create executable drug dose, course, fixed withdrawal period, MRL, slaughter decision, quarantine order, shipment permission, or jurisdiction-specific legal compliance conclusion. Those still require a product-label, official jurisdictional, or equivalent rule-card source.
- For the 32 disease pages still marked NEEDS_REVIEW, retrieve swine_textbook_pages_1_200_chapter_type_analysis with the target disease page and the relevant syndrome/comparison page before judging the answer as under-supported.
<!-- LOCAL_RAW_MD_SUBSTITUTION_V15_END -->
