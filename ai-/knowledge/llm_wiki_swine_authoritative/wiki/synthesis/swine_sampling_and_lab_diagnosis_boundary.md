---
tags: [synthesis, swine, v5]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, boundary_policy]
sources: [SRC-0001, A0-MOA-573, A0-MOA-ASF-NORMALIZED-GUIDE, A1-WOAH-ASF]
---

# 采样和实验室诊断边界

## 系统用途

采样、PCR、培养、血清学、粪检、剖检等必须结合疾病阶段和假阳性/假阴性边界解释。

## 强制边界

- 仅使用 `HUMAN_REVIEWED` facts 和有来源锚点页面。
- `NEEDS_REVIEW` 只能提示“待复核”，不得作为最终结论。
- 禁用药、剂量、休药期、检疫、扑杀、食品处理和公共卫生暴露处置必须要求可追溯来源；来源可以是 A0/A1/A2/SRC/RC/RULE，涉及特定法域合规时必须使用该法域来源。

## 推荐检索顺序

1. `rule_cards`
2. `syndromes`
3. `diseases`
4. `rules`
5. `sources`
6. `knowledge_facts.json`
