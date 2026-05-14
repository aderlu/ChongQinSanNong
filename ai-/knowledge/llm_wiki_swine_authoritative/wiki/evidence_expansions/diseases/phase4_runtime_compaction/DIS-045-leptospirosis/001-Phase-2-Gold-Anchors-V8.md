---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-045-leptospirosis.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-004-, CMP-006-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0067, SRC-0068]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-045-leptospirosis / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- 钩端螺旋体病是繁殖猪群繁殖损失原因之一，地方性猪群可缺乏明显临床病。 ($fact_id=LEPTO-001-relevance; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 878)
- serovar 分类仍广泛用于血清诊断、流行病学和流行率研究，serogroup 用于选择血清学交叉反应株。 ($fact_id=LEPTO-002-serovar; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 879)

### 流行病学和传播边界

- 在猪群感染常见地区，钩端螺旋体病是养猪者、兽医等接触猪人员的潜在职业性人兽共患病。 ($fact_id=LEPTO-003-zoonosis; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 879)
- Pomona 进入猪群后可建立高感染率，若直接接触受阻，受污染粪污、水或土壤在潮湿条件下仍可传播。 ($fact_id=LEPTO-004-pomona; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 880)
- 感染猪可经尿液排出 Canicola 至少 90 天，提示同种内传播可能。 ($fact_id=LEPTO-005-canicola; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 881)
- Icterohemorrhagiae/Copenhageni 可能经褐家鼠尿液污染环境引入易感猪群。 ($fact_id=LEPTO-006-rat; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 881)
- Bratislava 感染可在非妊娠母猪输卵管/子宫和公猪精囊、尿道球腺、前列腺、睾丸中持续存在。 ($fact_id=LEPTO-007-bratislava; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 882)

### 临床症状

- 绝大多数猪钩端螺旋体感染为亚临床，幼龄仔猪和妊娠母猪最可能出现临床感染。 ($fact_id=LEPTO-008-clinical; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 882)

### 剖检变化

- 慢性钩端螺旋体病肉眼病变局限于肾脏，显微镜下可见进行性多灶性间质性肾炎。 ($fact_id=LEPTO-009-kidney-lesions; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 883)

### 实验室诊断

- 钩端螺旋体临床材料培养困难且耗时，应由专门实验室完成；肾脏带菌动物培养对流行病学研究有用。 ($fact_id=LEPTO-010-culture; source=SRC-0067; Chapter 55 Leptospirosis; PDF page 884)

### 防控和用药边界

- 教材将人工授精列为控制 Bratislava 感染的重要工具；该事实不等同于固定净化程序或监管处置命令。 ($fact_id=LEPTO-011-bratislava-ai-control; source=SRC-0068; Chapter 55 Leptospirosis; PDF page 885)
- 教材讨论免疫和饲料给药作为控制选项，但具体剂量、程序、休药期和中国合规结论必须另由本地标签或 A0/A1/A2/SRC/RC/RULE 来源确认。 ($fact_id=LEPTO-012-vaccine-medication-boundary; source=SRC-0068; Chapter 55 Leptospirosis; PDF page 885)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-004-reproductive-failure](../comparisons/CMP-004-reproductive-failure.md)，不得孤立生成单病种确定诊断。
- 本页生成病例时应优先联动 [CMP-006-sudden-death-septicemia](../comparisons/CMP-006-sudden-death-septicemia.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
