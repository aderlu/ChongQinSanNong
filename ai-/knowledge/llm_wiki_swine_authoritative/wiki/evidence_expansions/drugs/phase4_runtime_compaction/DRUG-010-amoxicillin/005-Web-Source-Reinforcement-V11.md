---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/drugs/DRUG-010-amoxicillin.md
original_section: "Web Source Reinforcement / V11"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [A0-MOA-AMOXICILLIN-INJECTION-332-2020, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
default_runtime: false
updated: 2026-05-09T20:06:42+08:00
---

# DRUG-010-amoxicillin / Web Source Reinforcement / V11

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Web Source Reinforcement / V11

> 2026-05-08 V11 药物标签证据第一批。`gold_dataset_use` 本轮判定为 `positive_label_candidate`；事实来自本轮打开核验并注册的 source：`A0-MOA-AMOXICILLIN-INJECTION-332-2020`。

### 批准标签和靶动物

- 本轮找到农业农村部公告中的阿莫西林注射液说明书；页面可升级为 `positive_label_candidate`，但仅限该注射液标签范围。`fact_id=V11-DRUG-010-label-scope; source_id=A0-MOA-AMOXICILLIN-INJECTION-332-2020; anchor=web page opened 2026-05-08`

### 剂型/途径/适应证边界

- 该说明书为阿莫西林注射液，猪的标签适应证为治疗对阿莫西林敏感的感染性疾病；牛和猪给药途径为肌内注射。`fact_id=V11-DRUG-010-route-indication; source_id=A0-MOA-AMOXICILLIN-INJECTION-332-2020; anchor=web page opened 2026-05-08`

### 处方药/禁停用/限制状态

- 该标签区标注为兽用处方药，并列明猪休药期为 21 日；未检出本来源支持其他阿莫西林制剂的休药期。`fact_id=V11-DRUG-010-prescription-withdrawal; source_id=A0-MOA-AMOXICILLIN-INJECTION-332-2020; anchor=web page opened 2026-05-08`

### 生成与评估边界

- 不得把阿莫西林注射液标签外推到可溶性粉、复方制剂、给水群体用药或其他适应证；剂量和休药期回答必须逐字核对原标签。`fact_id=V11-DRUG-010-boundary; source_id=A0-MOA-AMOXICILLIN-INJECTION-332-2020; anchor=web page opened 2026-05-08`

### Evidence gap

- 即使页面升级为 `positive_label_candidate`，也只表示存在可召回的官方标签候选；剂量、疗程、给药途径、休药期、MRL、残留合格和食品安全结论仍必须在具体回答时逐条核对原始标签、标准或等效来源，不得从本页摘要外推。`source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001; source_id=A0-MOA-LABEL-INSTRUCTION-RULES-2002`
