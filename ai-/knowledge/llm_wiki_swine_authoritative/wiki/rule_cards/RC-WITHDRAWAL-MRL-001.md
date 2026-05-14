---
tags: [rule_card, swine, drug, withdrawal, mrl, residue, food_safety, source_first, v11_1]
card_id: RC-WITHDRAWAL-MRL-001
updated: 2026-05-08T23:59:00+08:00
severity: critical
jurisdiction: Global
hard_block: true
legacy_evidence_status: HUMAN_REVIEWED
sources: [RC-DRUG-001, RC-CITATION-001]
---

# 休药期和残留合格必须精确到来源

## 触发词

- 休药期
- 停药期
- 出栏
- 屠宰
- 肉能不能吃
- 残留
- MRL
- 最大残留限量
- 食品安全

## 规则

休药期、肉品可食、残留合格和 MRL 结论必须精确到具体来源条款。来源可以是 `A0/A1/A2/SRC/RC/RULE`，但必须覆盖对应产品、药物、动物种属、剂型、组织/食品类别、适用条件和法域。

## 允许响应

- 引用具体标签、标准或权威来源给出限定性结论。
- 来源不足时回答“不能确认，需要具体标签/标准/残留检测依据复核”。
- 对禁用、停用或淘汰药物触发硬阻断。

## 禁止响应

- 编造休药期天数或 MRL 数值。
- 把其他动物、其他制剂、其他法域、人医语境或教材候选外推为猪。
- 把入口公告、目录命中或摘要页当作具体数值来源。
- 用“延长休药期”规避禁用药、停用药或无批准标签用药。
