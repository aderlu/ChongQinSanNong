---
tags: [evidence_expansion, swine, phase4_runtime_compaction]
source_page: wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md
original_section: "Phase 2 Gold Anchors / V8"
migration_reason: "legacy H2 construction or reinforcement section moved out of default runtime"
source_ids: [CMP-003-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0069]
default_runtime: false
updated: 2026-05-09T20:09:38+08:00
---

# DIS-046-mycoplasmosis-enzootic-pneumonia / Phase 2 Gold Anchors / V8

This evidence expansion preserves original source-anchored material moved out of the compact runtime entity page.
It is retained for audit, source lookup, and targeted evidence expansion, not default production retrieval.

## Original Content

## Phase 2 Gold Anchors / V8

> 2026-05-08 Phase 2 补强块。仅使用 exports/knowledge_facts.json 中 HUMAN_REVIEWED 且带 evidence_source_id 的事实；用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。

### 病原/病型定位

- 猪支原体疾病主要由 M. hyopneumoniae、M. hyorhinis、M. hyosynoviae 和 M. suis 四类覆盖，分别关联地方性肺炎/PRDC、多浆膜炎关节炎、育肥猪关节炎和感染性贫血。 ($fact_id=MYCO-001-major-species; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 887)
- M. hyopneumoniae 是地方性肺炎的必要病因，并可作为 PRDC 的重要原发病原促进其他呼吸道病原造成疾病。 ($fact_id=MHYO-001-ep-prdc-primary; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 887)

### 流行病学和传播边界

- 地方性肺炎通常呈慢性、高发病率、低死亡率，经济影响主要来自日增重下降、料肉比升高和出栏日龄延长。 ($fact_id=MHYO-002-performance-pattern; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 887)
- 多数猪群可为地方性存在，但阴性易感猪群新引入 M. hyopneumoniae 时可出现影响各年龄猪的暴发。 ($fact_id=MHYO-003-naive-herd-epidemic; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 887)
- M. hyopneumoniae 最常经感染猪与易感猪近距离接触传播，传播相对缓慢；定植可持续数月，定植猪可在感染期间持续具有传播风险。 ($fact_id=MHYO-005-contact-slow-persistent; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 888)
- M. hyopneumoniae 可发生空气传播，尤其在利于气溶胶传播的条件下；教材称子宫内传播尚不明确，媒介作用被认为很小。 ($fact_id=MHYO-006-airborne-not-inutero; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 888)
- 母猪可在哺乳期通过鼻分泌物将 M. hyopneumoniae 传播给后代，后备母猪引入和母猪群感染结构会影响群内维持。 ($fact_id=MHYO-007-sow-to-piglet; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 888-889)

### 剖检变化

- M. hyopneumoniae 相关肺部肉眼病变可提示地方性肺炎，但并非特异性，猪流感、PRRSV、PCV2、App、猪腺病毒和伪狂犬病毒等也可产生相似病变。 ($fact_id=MHYO-008-lesions-nonpathognomonic; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 892)

### 实验室诊断

- M. hyopneumoniae 体外培养营养要求高、生长慢，且易受 M. hyorhinis 等过度生长影响，分离常不成功。 ($fact_id=MHYO-004-culture-difficult; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 887-888)
- 地方性肺炎诊断需综合典型临床表现、流行病学、肉眼/显微病变和病变部位中 M. hyopneumoniae 的实验室检测，不能只凭单项结果确认。 ($fact_id=MHYO-009-diagnosis-composite; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 892)

### 防控和用药边界

- 治疗可改善地方性肺炎临床表现，但停药后临床表现和排菌可重新出现，因此不能把治疗等同于清除感染。 ($fact_id=MHYO-010-treatment-shedding-boundary; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 893-894)
- M. hyopneumoniae 疫苗可降低临床症状、肺病变和治疗需求，但不能阻止定植或感染传播，需要结合群体管理解释。 ($fact_id=MHYO-011-vaccine-reduction-not-blocking; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 894-895)
- M. hyopneumoniae 感染可通过严格方案尝试根除，但根除后仍需生物安全和监测以防再感染，不能仅凭教材生成固定清群流程。 ($fact_id=MHYO-012-eradication-biosecurity; source=SRC-0069; Chapter 56 Mycoplasmosis; PDF page 895)

### 黄金集生成边界

- 本页生成病例时应优先联动 [CMP-003-respiratory-disease](../comparisons/CMP-003-respiratory-disease.md)，不得孤立生成单病种确定诊断。
- 中国动物疫病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 与 A0 来源核验。
- 涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 与 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。
