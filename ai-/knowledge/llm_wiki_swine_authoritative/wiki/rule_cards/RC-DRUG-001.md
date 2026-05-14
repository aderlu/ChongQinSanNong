---
tags: [rule_card, swine, drug, prescription, source_first, v11_1]
card_id: RC-DRUG-001
updated: 2026-05-08T23:59:00+08:00
severity: critical
jurisdiction: Global
hard_block: true
legacy_evidence_status: HUMAN_REVIEWED
sources: [RC-CITATION-001, RC-DRUG-GOLD-ROLE-001, RC-WITHDRAWAL-MRL-001]
---

# 猪病处方必须有具体标签或等效来源

## 触发词

- 用药
- 剂量
- 休药期
- 处方
- 治疗方案
- 抗菌药
- 驱虫药
- 抗球虫药

## 规则

不得把“中国 A0/A1”作为唯一可用来源；但任何正向处方都必须有具体标签或等效事实源。可用来源包括 `A0/A1/A2/SRC/RC/RULE`，前提是能核验猪靶动物、药物/产品、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。

## 允许响应

- 在精确来源覆盖范围内生成限定性处方或治疗建议。
- 在来源不足时提供诊断、采样、药敏、兽医复核和标签核验路径。
- 标注来源法域和产品范围，避免跨法域或跨制剂外推。

## 禁止响应

- 编造剂量、疗程、给药途径或休药期。
- 把药物类别页、教材候选、处方药目录、其他动物标签或人医语境当作猪用处方。
- 把一个法域的标签伪装成另一个法域的合规结论。
- 用“延长休药期”规避禁用、停用、淘汰或无标签用药。
