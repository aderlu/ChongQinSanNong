---
tags: [synthesis, swine, treatment_candidates, source_first, v11_1]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, matrix_reference]
sources: [SRC-0012, SRC-0058, SRC-0059, SRC-0062, SRC-0063, SRC-0064, SRC-0065, SRC-0069, SRC-0070, SRC-0071, SRC-0072, SRC-0073, SRC-0074, SRC-0075, SRC-0076, SRC-0077, SRC-0080, SRC-0081, SRC-0082, RC-DRUG-001, RC-DRUG-GOLD-ROLE-001]
---

# Swine Treatment Candidate Matrix / 猪病治疗候选矩阵

## 来源和状态

- 本页由 `Diseases of Swine, 11th Edition` 全文候选扫描和后续 V11 标签证据补强汇总而来。
- 教材候选可用于召回疾病-药物关系、生成药敏/标签核验追问和构造评估陷阱。
- 候选命中不等于处方；正向处方需要回到具体标签或等效事实源。

## Source-first 可用边界

- 可用于：治疗候选召回、药物类别归并、病原/药敏/阶段判断、标签复核提示、处方越界识别。
- 可升级为正向处方的条件：猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL/禁停用状态均有清晰来源。
- 来源不限于中国 A0/A1；`A0/A1/A2/SRC/RC/RULE` 均可，但答案必须限定在来源本身的法域和标签范围内。
- `high_review` 药物应优先查禁用/停用/淘汰清单、AMR 审慎来源、药敏证据和产品标签。

## 候选概览

- 候选关系行数：178。
- 高复核药物包括：ceftiofur、cefquinome、fluoroquinolones、colistin、chloramphenicol、carbadox、olaquindox、nitroimidazoles、ractopamine。
