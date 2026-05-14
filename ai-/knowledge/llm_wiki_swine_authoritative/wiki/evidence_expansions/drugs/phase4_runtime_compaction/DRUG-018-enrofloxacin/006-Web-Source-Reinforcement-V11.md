---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/drugs/DRUG-018-enrofloxacin.md
original_section: "Web Source Reinforcement / V11"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [A0-MOA-ENROFLOXACIN-SOLUTION-55-2018, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
default_runtime: false
updated: 2026-05-09T20:06:42+08:00
---

# DRUG-018-enrofloxacin / Web Source Reinforcement / V11

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Web Source Reinforcement / V11

> 2026-05-08 V11 药物标签证据第一批。`gold_dataset_use` 本轮判定为 `positive_label_candidate`；事实来自本轮打开核验并注册的 source：`A0-MOA-ENROFLOXACIN-SOLUTION-55-2018`。

### 批准标签和靶动物

- 本轮找到农业农村部公告中的恩诺沙星溶液说明书；可作为匹配制剂和靶动物范围内的标签候选。`fact_id=V11-DRUG-018-label-scope; source_id=A0-MOA-ENROFLOXACIN-SOLUTION-55-2018; anchor=web page opened 2026-05-08`

### 剂型/途径/适应证边界

- 该说明书为恩诺沙星溶液，适应证为治疗猪大肠杆菌所致的胃肠道疾病，标签给药途径为内服。`fact_id=V11-DRUG-018-route-indication; source_id=A0-MOA-ENROFLOXACIN-SOLUTION-55-2018; anchor=web page opened 2026-05-08`

### 休药期/MRL/残留边界

- 该说明书列明猪休药期为 5 日；标签还要求尽可能根据药敏试验使用氟喹诺酮类药物，并提示偏离说明书可增加耐药风险。`fact_id=V11-DRUG-018-withdrawal; source_id=A0-MOA-ENROFLOXACIN-SOLUTION-55-2018; anchor=web page opened 2026-05-08`

### 生成与评估边界

- 氟喹诺酮类高风险；不得把恩诺沙星溶液标签外推到其他剂型、其他喹诺酮或无诊断群体用药。`fact_id=V11-DRUG-018-boundary; source_id=A0-MOA-ENROFLOXACIN-SOLUTION-55-2018; anchor=web page opened 2026-05-08`

### Evidence gap

- 即使页面升级为 `positive_label_candidate`，也只表示存在可召回的官方标签候选；剂量、疗程、给药途径、休药期、MRL、残留合格和食品安全结论仍必须在具体回答时逐条核对原始标签、标准或等效来源，不得从本页摘要外推。`source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001; source_id=A0-MOA-LABEL-INSTRUCTION-RULES-2002`
