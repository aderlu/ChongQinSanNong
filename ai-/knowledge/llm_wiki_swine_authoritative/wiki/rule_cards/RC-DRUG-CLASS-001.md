---
tags: [rule_card, swine, drug, label, non_inference, v8]
card_id: RC-DRUG-CLASS-001
updated: 2026-05-08T12:00:00+08:00
severity: critical
jurisdiction: China
hard_block: true
legacy_evidence_status: HUMAN_REVIEWED
sources: [A0-MOA-LABEL-INSTRUCTION-RULES-2002, A0-MOA-PRESCRIPTION-790-2024, RC-DRUG-001]
---

# 药物类别不得外推为具体猪用产品

## 触发词

- 某类药
- 同类药
- 可以替代
- 猪用剂量
- 猪用休药期
- 批准用于猪
- 按同类药使用

## 规则

药物类别页只能支持类别识别、风险提醒、药敏/诊断优先级和合规核验路径。类别页不得证明某个具体活性成分、剂型、靶动物、适应证、剂量、疗程或休药期在中国猪场可用。

## 允许响应

- 说明该药属于哪一类。
- 提醒需要核验具体产品标签、批准文号、说明书、处方药目录、MRL 和休药期。
- 对无标签或无来源的用药请求转为兽医处方和官方来源核验。

## 禁止响应

- 从药物类别直接生成具体剂量、疗程、给药途径或休药期。
- 从牛、羊、禽、宠物、人医或境外标签外推为中国猪用。
- 从同类药或复方制剂外推到单方制剂。
- 从处方药目录命中外推为具体疾病适应证。

## 来源

- `A0-MOA-LABEL-INSTRUCTION-RULES-2002`
- `A0-MOA-PRESCRIPTION-790-2024`
- `RC-DRUG-001`
