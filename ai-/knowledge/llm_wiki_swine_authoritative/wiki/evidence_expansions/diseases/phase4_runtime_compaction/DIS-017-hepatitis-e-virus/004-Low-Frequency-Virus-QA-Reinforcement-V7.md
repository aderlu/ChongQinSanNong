---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-017-hepatitis-e-virus.md
original_section: "Low Frequency Virus QA Reinforcement / V7"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [A0-MOA-BANNED-DRUG-250-POLICY, SRC-0008, SRC-0009, SRC-0012, SRC-0040]
default_runtime: false
updated: 2026-05-09T20:06:42+08:00
---

# DIS-017-hepatitis-e-virus / Low Frequency Virus QA Reinforcement / V7

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Low Frequency Virus QA Reinforcement / V7

> 2026-05-07T05:05:11.588451+00:00 added for swine QA dataset generation. This block uses Diseases of Swine 11e HUMAN_REVIEWED facts and does not create dose, withdrawal-period, culling, quarantine or public-health execution instructions.

### 病原、临床和因果边界

- HEV 是人类戊型肝炎病原，猪 HEV 与人类感染具有公共卫生关联；猪场知识库只能生成风险边界，不能替代食品安全或公共卫生处置规范。（SRC-0040; Chapter 34 Hepatitis E Virus; PDF page 568)
- HEV 以粪口传播为核心，污染的水、食物和猪源产品暴露可构成风险；解释时需区分养殖场传播与食品消费暴露。（SRC-0040; Chapter 34 Hepatitis E Virus; PDF page 568-569)
- 猪感染 HEV 可出现肝脏复制和显微肝炎，但常无明显临床病；不得将 HEV 检出直接写成猪群明显临床肝炎诊断。（SRC-0040; Chapter 34 Hepatitis E Virus; PDF page 568-569)
- HEV 感染后可出现短期病毒血症和较长粪便排毒窗口；采样解释需结合感染阶段和样本类型。（SRC-0040; Chapter 34 Hepatitis E Virus; PDF page 569)
- 急性戊肝病例与猪肝或猪源产品暴露有关；本事实只用于风险提示，不生成烹饪温度、召回或中国监管结论。(SRC-0040; Chapter 34 Hepatitis E Virus; PDF page 569)
- HEV 诊断涉及核酸、血清学和病理解释；猪群检出需结合感染阶段、排毒和公共卫生语境，不能单凭单项结果扩展为场内处置结论。(SRC-0040; Chapter 34 Hepatitis E Virus; PDF page 568-570)

### 实验室诊断与采样边界

- 明确诊断问题应决定样本类型、样本数量和最合适的检测项目。（SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 送检单应包含环境和临床证据、地理位置、年龄、临床症状、用药和免疫史、水料来源、发病率和死亡率等信息。（SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 以诊断临床疾病为目标时，推荐采集急性受影响且未用药动物的样本。（SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 123)
- 采样计划必须考虑病原生物学；例如 C. difficile 需要大肠和结肠内容物，猪流感检测不适合提交全血或血液 RNA。（SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 124)
- 新鲜样本应立即冷藏并分袋密封，脑、脊髓、肺、心、肝、脾、肾等应与肠道或胃肠内容物分开。（SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 125)
- 定量 PCR 测量核酸量，不能单独证明样本中存在感染性或复制性病原。（SRC-0008; Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation; PDF page 113)

### 防控与用药边界

- 任何外源化学药物都可能影响机体稳态；治疗前应确认对动物的潜在获益大于风险和代谢负担。（SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 182)
- 食品动物禁用药应以农业农村部公告第250号及官方清单为准；未核验具体清单原文前，不得编造禁用药条目。（A0-MOA-BANNED-DRUG-250-POLICY; 农业农村部政策说明；公告第250号来源入口。

### 问答生成注意事项

- 低频病毒病不得用单项检出直接定因；应写成“疑似/需鉴别/需结合共感染和病变”。
- 对人兽共患或公共卫生内容，只能提示风险边界，不能生成食品召回、暴露后处置或监管执行命令。
- 无商业化疫苗、无特异治疗或诊断试剂不成熟时，应转向采样、隔离观察、支持性管理和权威实验室确认。
