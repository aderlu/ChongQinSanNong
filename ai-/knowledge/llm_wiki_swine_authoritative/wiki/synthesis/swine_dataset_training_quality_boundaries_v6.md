---
tags: [synthesis, swine, dataset, qa, sampling, drug_boundary, regulatory_boundary]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, gold_candidate, audit_only, dataset_generation_policy]
sources: [SRC-0008, SRC-0009, SRC-0012, A0-MOA-573, A0-MOA-BANNED-DRUG-250-POLICY]
---

# Swine Dataset Training Quality Boundaries V6

This page is a retrieval target for dataset generation and judging. It consolidates sampling, laboratory diagnosis, drug boundary, and regulatory boundary facts that should be injected when disease-specific pages are sparse.

### Sampling and lab diagnosis

- 明确诊断问题应决定样本类型、样本数量和最合适的检测项目。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 送检单应包含环境和临床证据、地理位置、年龄、临床症状、用药和免疫史、水料来源、发病率和死亡率等信息。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 以诊断临床疾病为目标时，推荐采集急性受影响且未用药动物的样本。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 123)
- 采样计划必须考虑病原生物学；例如 C. difficile 需要大肠和结肠内容物，猪流感检测不适合提交全血或血清 RNA。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 124)
- 新鲜样本应立即冷藏并分袋密封，脑、脊髓、肺、心、肝、脾、肾等应与肠道或胃肠内容物分开。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 125)
- 定量 PCR 测量核酸量，不能单独证明样本中存在感染性或复制性病原。 (SRC-0008; Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation; PDF page 113)

### Drug and treatment boundary

- 任何外源化学药物都可能影响机体稳态；治疗前应确认对动物的潜在获益大于风险和代谢负担。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 182)
- 抗菌治疗目标的理想依据是完整诊断调查中的细菌培养、鉴定和药敏，并确认代表性病例存在与病原一致的病变。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 183)
- 治疗失败可由误诊、感染部位药物活性不足、培养缺失、实验室结果不适用、耐药、慢性感染或采样错误导致；失败时应复核诊断并采样送检。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 190)
- 食品动物禁用药应以农业农村部公告第250号及官方清单为准；未核验具体清单原文前，不得编造禁用药条目。 (A0-MOA-BANNED-DRUG-250-POLICY; 农业农村部政策说明；公告第250号来源入口)

## Use in generation

- Require at least two source anchors in every answer candidate when the case contains diagnosis, treatment, regulatory action, or sampling advice.
- Prefer acute untreated representative animals for diagnostic sampling; include submission form context and sample handling details.
- If the disease is A0/A1 regulated or zoonotic, include official-reporting and public-health boundaries before treatment language.
- Keep all dose, course and withdrawal-period fields as boundary statements unless a verified local label source is present.
