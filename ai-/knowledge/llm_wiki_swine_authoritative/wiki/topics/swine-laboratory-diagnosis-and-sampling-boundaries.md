---
tags: [topic, swine, dataset_quality, v6]
updated: 2026-05-07T04:56:26.230513+00:00
legacy_evidence_status: HUMAN_REVIEWED
sources: [SRC-0008, SRC-0009]
---

# Swine Laboratory Diagnosis and Sampling Boundaries

用于所有猪病问诊样本的实验室诊断、采样数量、采样对象、送检单和样本保存边界。

### Reviewed facts

- 明确诊断问题应决定样本类型、样本数量和最合适的检测项目。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 送检单应包含环境和临床证据、地理位置、年龄、临床症状、用药和免疫史、水料来源、发病率和死亡率等信息。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 122)
- 以诊断临床疾病为目标时，推荐采集急性受影响且未用药动物的样本。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 123)
- 采样计划必须考虑病原生物学；例如 C. difficile 需要大肠和结肠内容物，猪流感检测不适合提交全血或血清 RNA。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 124)
- 新鲜样本应立即冷藏并分袋密封，脑、脊髓、肺、心、肝、脾、肾等应与肠道或胃肠内容物分开。 (SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 125)
- 定量 PCR 测量核酸量，不能单独证明样本中存在感染性或复制性病原。 (SRC-0008; Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation; PDF page 113)

## Dataset use

- 生成问诊答案时必须写明证据锚点，优先使用 source id、PDF page、A0/A1 source page 或 rule card。
- 无法确认中国标签、批准适应证、剂量、疗程或休药期时，只能输出边界说明，不能输出固定处方。
- 重大动物疫病、疑似法定疫病和人兽共患风险必须先写监管/生物安全边界，再写支持性处置。
