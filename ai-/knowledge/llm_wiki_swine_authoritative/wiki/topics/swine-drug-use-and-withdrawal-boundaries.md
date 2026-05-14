---
tags: [topic, swine, dataset_quality, v6]
updated: 2026-05-07T04:56:26.230513+00:00
legacy_evidence_status: HUMAN_REVIEWED
sources: [A0-MOA-BANNED-DRUG-250-POLICY, SRC-0012]
---

# Swine Drug Use and Withdrawal Boundaries

用于所有治疗建议样本，强调药物获益风险、培养药敏、治疗失败复核、禁用药来源和不得生成剂量/休药期。

### Reviewed facts

- 任何外源化学药物都可能影响机体稳态；治疗前应确认对动物的潜在获益大于风险和代谢负担。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 182)
- 抗菌治疗目标的理想依据是完整诊断调查中的细菌培养、鉴定和药敏，并确认代表性病例存在与病原一致的病变。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 183)
- 治疗失败可由误诊、感染部位药物活性不足、培养缺失、实验室结果不适用、耐药、慢性感染或采样错误导致；失败时应复核诊断并采样送检。 (SRC-0012; Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; PDF page 190)
- 食品动物禁用药应以农业农村部公告第250号及官方清单为准；未核验具体清单原文前，不得编造禁用药条目。 (A0-MOA-BANNED-DRUG-250-POLICY; 农业农村部政策说明；公告第250号来源入口)

## Dataset use

- 生成问诊答案时必须写明证据锚点，优先使用 source id、PDF page、A0/A1 source page 或 rule card。
- 无法确认中国标签、批准适应证、剂量、疗程或休药期时，只能输出边界说明，不能输出固定处方。
- 重大动物疫病、疑似法定疫病和人兽共患风险必须先写监管/生物安全边界，再写支持性处置。
