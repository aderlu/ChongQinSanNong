---
tags: [topic, swine, dataset_quality, v6]
updated: 2026-05-07T04:56:26.230513+00:00
legacy_evidence_status: HUMAN_REVIEWED
sources: [SRC-0008, SRC-0009, SRC-0035, SRC-0036, SRC-0037]
---

# Swine Differential Diagnosis Boundaries

用于阻断单一症状、单一阳性检测或单一病名直接定因，要求结合临床、病变、群体和实验室证据。

### Reviewed facts

- 诊断测试应围绕明确问题设计，样本选择和采样时机可能比检测方法选择更关键。 (SRC-0008; Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation; PDF page 119)
- 现场信息收集应先于诊断问题和病因假设构建，否则可能引入确认偏倚或选择偏倚。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 地方性或常在菌群中的病原被检出不必然表示临床疾病，只提示可能诊断。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 124)
- 由于 PCV2 普遍存在，定性 PCR 不应单独用于诊断 PCV2-SD，需结合病毒量、病变和病原定位。 (SRC-0035; Chapter 30 Circoviruses; PDF page 504)
- PRCV/TGEV 可通过针对 PRCV S 基因缺失区域的 PCR 引物鉴别；多重 RT-PCR 或实时 RT-PCR 可同时检测多种猪腹泻相关病毒。 (SRC-0036; Chapter 31 Coronaviruses opening; PDF page 523)
- PHEV 可通过病毒分离、IHC 或 RT-PCR 诊断，并需与伪狂犬、猪捷申病、狂犬病、Teschen/Talfan 病和盐中毒等鉴别。 (SRC-0037; Chapter 31 Coronaviruses continuation; PDF page 539)

## Dataset use

- 生成问诊答案时必须写明证据锚点，优先使用 source id、PDF page、A0/A1 source page 或 rule card。
- 无法确认中国标签、批准适应证、剂量、疗程或休药期时，只能输出边界说明，不能输出固定处方。
- 重大动物疫病、疑似法定疫病和人兽共患风险必须先写监管/生物安全边界，再写支持性处置。
