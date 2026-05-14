---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-002-african-swine-fever-virus.md
original_section: "Dataset QA Reinforcement / V6"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [A0-MOA-573, A0-MOA-ASF-NORMALIZED-GUIDE, A0-MOA-BANNED-DRUG-250-POLICY, A1-WOAH-ASF, SRC-0008, SRC-0009, SRC-0012, SRC-0031]
default_runtime: false
updated: 2026-05-09T20:06:42+08:00
---

# DIS-002-african-swine-fever-virus / Dataset QA Reinforcement / V6

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Dataset QA Reinforcement / V6

> 2026-05-07 V6 数据集训练补强块。仅使用 HUMAN_REVIEWED 或 A0/A1 锚定事实，目标是减少微调样本中的零锚点、泛化采样建议、经验性用药和重大疫病监管外推。

### 实验室诊断与采样规范

- 明确诊断问题应决定样本类型、样本数量和最合适的检测项目。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 送检单应包含环境和临床证据、地理位置、年龄、临床症状、用药和免疫史、水料来源、发病率和死亡率等信息。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 以诊断临床疾病为目标时，推荐采集急性受影响且未用药动物的样本。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 123)
- 采样计划必须考虑病原生物学；例如 C. difficile 需要大肠和结肠内容物，猪流感检测不适合提交全血或血清 RNA。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 124)
- 新鲜样本应立即冷藏并分袋密封，脑、脊髓、肺、心、肝、脾、肾等应与肠道或胃肠内容物分开。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 125)
- 定量 PCR 测量核酸量，不能单独证明样本中存在感染性或复制性病原。 (SRC-0008; Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation; PDF page 113)

### 本病种特异锚点

- 非洲猪瘟列入中国一类动物疫病名录，相关处置必须依据中国官方法规和技术规范。 (A0-MOA-573; 公告第573号；一类动物疫病名录)
- 非洲猪瘟常态化防控指南要求，检测阳性时应报告当地畜牧兽医部门并按官方流程处理，不能生成治疗替代报告的建议。 (A0-MOA-ASF-NORMALIZED-GUIDE; 非洲猪瘟常态化防控技术指南；检测阳性处置边界)
- WOAH 将非洲猪瘟描述为家猪和野猪高度传染性病毒病，但对人类健康无危害。 (A1-WOAH-ASF; WOAH ASF disease page)
- PCR 和血吸附试验是检测识别非洲猪瘟病毒常用方法；血吸附试验为参考标准，但少数野毒株可不诱导血吸附，需要 PCR 或直接免疫荧光识别。 (SRC-0031; Chapter 25 African Swine Fever Virus; PDF page 472-473)
- 家猪和欧洲野猪感染非洲猪瘟可表现从急性到慢性的广泛临床谱，并可能类似经典猪瘟、丹毒等疾病。 (SRC-0031; Chapter 25 African Swine Fever Virus; PDF page 470)

### 鉴别诊断、防控和药物边界

- 任何外源化学药物都可能影响机体稳态；治疗前应确认对动物的潜在获益大于风险和代谢负担。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 182)
- 抗菌治疗目标的理想依据是完整诊断调查中的细菌培养、鉴定和药敏，并确认代表性病例存在与病原一致的病变。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 183)
- 治疗失败可由误诊、感染部位药物活性不足、培养缺失、实验室结果不适用、耐药、慢性感染或采样错误导致；失败时应复核诊断并采样送检。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 190)
- 食品动物禁用药应以农业农村部公告第250号及官方清单为准；未核验具体清单原文前，不得编造禁用药条目。 (A0-MOA-BANNED-DRUG-250-POLICY; 农业农村部政策说明；公告第250号来源入口)

### 生成训练样本时的硬边界

- 不得把单一 PCR/qPCR 阳性、抗体阳性或卵囊检出直接写成定因结论；必须结合日龄、病程、病变、群体流行病学和采样质量。
- 不得从教材页码直接外推中国上报、封锁、扑杀、调运或固定免疫程序；中国监管结论必须引用 A0/A1/A2/SRC/RC/RULE 来源。
- 不得生成具体剂量、疗程或休药期；需要用药时只能提示按兽医处方、批准标签、药敏和本地法规复核。
