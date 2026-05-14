---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/drugs/DRUG-011-ceftiofur.md
original_section: "Web Source Reinforcement / V11"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024, A0-MOA-LABEL-INSTRUCTION-RULES-2002, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
default_runtime: false
updated: 2026-05-09T20:06:42+08:00
---

# DRUG-011-ceftiofur / Web Source Reinforcement / V11

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Web Source Reinforcement / V11

> 2026-05-08 V11 药物标签证据第一批。`gold_dataset_use` 本轮判定为 `positive_label_candidate`；事实来自本轮打开核验并注册的 source：`A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024`。

### 批准标签和靶动物

- 本轮找到农业农村部公报 PDF 中的注射用头孢噻呋钠说明书；可作为精确制剂标签候选。`fact_id=V11-DRUG-011-label-scope; source_id=A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024; anchor=web page opened 2026-05-08`

### 剂型/途径/适应证边界

- 该说明书为注射用头孢噻呋钠，兽用处方药；标签适应证包括猪细菌性呼吸道感染，猪给药途径为肌内注射。`fact_id=V11-DRUG-011-route-indication; source_id=A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024; anchor=web page opened 2026-05-08`

### 休药期/MRL/残留边界

- 该说明书列明猪休药期为 4 日；MRL 或残留合格结论仍需另查对应标准表，不得由休药期直接推出肉品合格。`fact_id=V11-DRUG-011-withdrawal; source_id=A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024; anchor=web page opened 2026-05-08`

### 生成与评估边界

- 头孢类属于高风险抗菌药；不得由成分类名外推剂量、疗程、休药期、联合用药或非标签适应证。`fact_id=V11-DRUG-011-boundary; source_id=A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024; anchor=web page opened 2026-05-08`

### Evidence gap

- 即使页面升级为 `positive_label_candidate`，也只表示存在可召回的官方标签候选；剂量、疗程、给药途径、休药期、MRL、残留合格和食品安全结论仍必须在具体回答时逐条核对原始标签、标准或等效来源，不得从本页摘要外推。`source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001; source_id=A0-MOA-LABEL-INSTRUCTION-RULES-2002`
