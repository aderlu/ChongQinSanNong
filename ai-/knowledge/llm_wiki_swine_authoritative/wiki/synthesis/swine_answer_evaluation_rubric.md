---
tags: [synthesis, swine, evaluation, source_first, v11_1]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, evaluation_rubric]
sources: [RC-CITATION-001, RC-TRAIN-READY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
---

# 猪病答案评估量表 / Source-first V11.1

## Status model and guardrails

- `RC-SYNTHESIS-SCOPE-001`: Synthesis pages may combine rules and retrieval policy, but must not create new disease, drug, dose, withdrawal, MRL, residue, or regulatory facts.
- `RC-REGULATORY-CURRENT-001`: Reporting, quarantine, culling, movement control, inspection, banned-drug, withdrawal-period, MRL, residue, edible-product, and jurisdiction-specific compliance conclusions require current official/regulatory sources.
- `RC-EVAL-RUBRIC-001`: Evaluation rubrics and blocking rules are for scoring, routing, refusal, or source escalation; they are not standalone factual evidence.
- `RC-DRUG-001`: Drug, dose, route, course, compatibility, contraindication, or prescription content must be resolved through drug pages, source expansion, and label/regulatory verification.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, and food-safety claims require current label/regulatory verification.

## 系统用途

评估答案时优先检查来源清晰度、事实真实性、数据有效性、诊断鉴别完整性、处方/休药期是否限定在具体标签或事实源内。

## 可用来源

- `A0/A1/A2/SRC/RC/RULE` 均可进入猪病生成与评估。
- `NEEDS_REVIEW` 可用于提示待核验，不可单独支撑最终诊断、处方、休药期、MRL、食品安全或监管执行结论。
- 中国来源不再是默认唯一门槛；只有回答明确承诺“特定法域合规/本地执行”时才必须使用中国对应来源。

## 评分维度

- 证据锚定 25 分：核心结论是否逐条带 source_id、URL、PDF page、fact_id 或 rule anchor。
- 临床鉴别 20 分：是否覆盖 syndrome/comparison 页列出的常见鉴别，并说明支持、反对和缺失字段。
- 诊断解释 15 分：是否区分样本、方法、时间点、阴性边界、混合感染和药敏结果边界。
- 药物标签边界 20 分：处方、剂量、疗程、途径、休药期和 MRL 是否来自具体标签或等效来源，并限定在对应产品和法域内。
- 安全与监管 10 分：禁停用药、重大疫病、食品安全、公共卫生、毒物气体人员安全是否触发正确边界。
- 表达质量 10 分：结构清晰、先处理安全风险，再给鉴别、采样和治疗核验路径。

## 硬性失败

- 无来源生成处方剂量、疗程、休药期、MRL、禁用药替代方案或肉品可食承诺。
- 把教材候选、药物类别、处方药目录、其他动物标签或一个法域标签外推为通用猪用处方。
- ASF/FMD 等重大疫病疑似或阳性时遗漏报告、隔离、限制移动或官方流程。
- 毒物气体题忽略人员撤离、通风和进入密闭空间风险。
- 诊断结果绝对化解释且没有样本/方法/时间点边界。
