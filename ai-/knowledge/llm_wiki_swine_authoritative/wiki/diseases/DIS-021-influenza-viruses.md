---
tags: [disease, swine, cleaned_v13_2, clinical_evidence_page]
disease_id: DIS-021
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, diagnosis_support, differential_support, control_support, regulatory_boundary, treatment_boundary, gold_candidate]
sources: [A0-MOA-SWINE-FLU-EMERGENCY-2009, A2-MERCK-INFLUENZA-A-SWINE-2024, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001, SRC-0009, SRC-0014, SRC-0042, SRC-0043, SRC-0049, SRC-0058, SRC-0069, SRC-0088, SRC-0089]
---

# 猪流感

## Source citation gate / Phase 8

- RC-CITATION-001: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.
## Runtime disease guardrail anchors / Phase 5

- RC-DX-001: Diagnosis must distinguish clinical suspicion, sample type, test method, pathogen detection, causality, and differential diagnosis.
- RC-DISEASE-REGULATORY-001: Reporting, quarantine, culling, movement control, inspection, and jurisdiction-specific disease-control actions require current official/regulatory sources.
- RC-DRUG-001: Disease pages must not independently generate executable drug prescriptions, dose, route, or course.
- RC-WITHDRAWAL-MRL-001: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
- Missing facets stay unfilled unless a source-anchored expansion is added.
## 英文/教材章节名

- Influenza Viruses

## Evidence-backed optional facets

- Transmission, clinical signs, necropsy findings, laboratory diagnosis, differential diagnosis, and control points are not mandatory entity-page sections; they appear here only when a clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists.
- Missing facets represent source-coverage boundaries and must not be scored as page failures or filled by guesswork.

### 传播途径

- 人类变异型甲型流感病例可与猪接触相关，展会等高接触场景需要人兽共患风险沟通。（SRC-0014; Chapter 12 Preharvest Food Safety, Zoonotic Diseases, and the Human Health Interface; PDF page 229）
- 猪流感在不同地区维持的 H1/H3 谱系和基因组合不同，并持续发生重配；解释流行格局必须结合地区和监测年代。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 605-606）

- IAV-S 复制主要集中在呼吸道，肺组织病毒滴度可较高；临床和传播解释需围绕呼吸道感染。`fact_id=IAV-011-respiratory-replication; source_id=SRC-0043; anchor=Chapter 36 Influenza Viruses continuation; PDF page 607`

### 临床症状

- 猪流感临床表现可从亚临床感染到鼻液、喷嚏、发热和呼吸道症状，严重度受病毒、剂量、免疫和并发感染影响。`fact_id=IAV-012-clinical-range; source_id=SRC-0043; anchor=Chapter 36 Influenza Viruses continuation; PDF page 607-608`

- 猪流感临床表现可从亚临床感染到鼻液、喷嚏、发热和呼吸道症状，严重度受病毒、剂量、免疫和并发感染影响。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 607-608）
- 母源抗体可减少临床病或排毒，但也可能影响仔猪主动免疫应答；解释免疫效果需结合母猪免疫状态和仔猪日龄。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 611）
- App 感染结局和暴发严重度受菌株毒力、M. hyopneumoniae、伪狂犬病病毒和可能的猪流感病毒等共同感染影响。（SRC-0058; Chapter 48 Actinobacillosis; PDF page 778）

### 剖检变化

- IAV-S 复制主要集中在呼吸道，肺组织病毒滴度可较高；临床和病理解释需围绕呼吸道感染。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 607）
- 单纯 IAV-S 病变主要为病毒性肺炎，但病变可轻微、不典型，或被继发/混合感染掩盖。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 608）
- M. hyopneumoniae 相关肺部肉眼病变可提示地方性肺炎，但并非特异性，猪流感、PRRSV、PCV2、App、猪腺病毒和伪狂犬病毒等也可产生相似病变。（SRC-0069; Chapter 56 Mycoplasmosis; PDF page 892）

- 单纯 IAV-S 病变主要为病毒性肺炎，但病变可轻微、不典型，或被继发/混合感染掩盖。`fact_id=IAV-013-lesion-boundary; source_id=SRC-0043; anchor=Chapter 36 Influenza Viruses continuation; PDF page 608`

### 实验室诊断

- 采样计划必须考虑病原生物学；例如 C. difficile 需要大肠和结肠内容物，猪流感检测不适合提交全血或血清 RNA。（SRC-0009; Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value; PDF page 124）
- 猪流感血清学可能难以清楚区分人源、猪源或重配谱系，解释需结合病毒分离、PCR 和测序。（SRC-0042; Chapter 36 Influenza Viruses; PDF page 602）
- 猪流感病毒分离样本应尽快检测，低温保存和样本质量会影响病毒分离成功率；PCR 阳性不等于获得感染性病毒分离株。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 609）
- 猪流感核酸检测可筛查临床样本，但核酸检出不等同病毒分离，可能反映降解或非感染性病毒材料。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 609）
- 猪流感血清学解释需结合亚型、毒株和抗原交叉反应，不能单靠抗体结果精确定义感染来源。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 610）

### 鉴别诊断

- H1N1pdm09 实验感染研究未在猪肉或肌肉组织中检出病毒；该事实仅用于教材食品暴露边界，不生成食品安全监管或消费结论。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 607）
- 猪流感疫苗相关增强呼吸道疾病 VAERD 是特定灭活疫苗与攻击毒株不匹配语境下的风险边界，不得泛化为所有免疫均会加重疾病。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 608）
- 猪流感减毒活疫苗可用于诱导黏膜免疫的研究和部分场景，但不能据此生成固定免疫程序或本地可用性结论。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 612）
- PRRSV 鉴别诊断可包括 CSFV、PCMV、PHEV、钩端螺旋体、细小病毒、PCV2、PRV、猪流感和 teschovirus 等。（SRC-0049; Chapter 41 PRRSV opening; PDF page 720）

### 防控要点

- 疫苗接种是猪流感预防的重要手段，但效果受疫苗毒株匹配、群体免疫、母源抗体和流行毒株影响。（SRC-0043; Chapter 36 Influenza Viruses continuation; PDF page 611-612）

## 病原与分类

- 初始分类：病毒病/呼吸道病
- 教材章节：Section III Viral Diseases，Chapter 36
- 正文起始页：PDF page 600

## 监管/执行性处置边界

- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。
- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。
- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。

## 典型宿主与阶段

- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。

## 用药/处置边界

- 待正文抽取和具体标签/等效来源复核；不以中国兽药来源作为唯一门槛。
- 法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。

## source_trust / evidence_coverage / usage_scope

- source_trust: $sourceTrust; legacy_evidence_status=$legacy. Preserve source/fact/page anchors and rule-card boundaries.
- evidence_coverage: retained source/fact/page anchors and explicit gaps stay in the evidence sections above.
- usage_scope: disease recall, evidence lookup, differential prompts, and boundary checks only; do not generate executable treatment, withdrawal-period, MRL, or regulatory conclusions without rule-card and source verification.
## 证据扩展索引

- 以下历史批次块、增强块或构建期补充内容已移出默认 runtime 页面；原始来源锚点完整保留在对应 evidence expansion 文件中。
- 默认生产/评估检索应优先使用本实体页的归并后 runtime 内容；需要审计、追溯或证据扩展时再定向读取下列文件。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/001-VTOP_V13_1.md`：VTOP_V13_1；sources: SRC-0088。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/002-SFDUT_1_200_V13_1.md`：SFDUT_1_200_V13_1；sources: SRC-0089。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/003-Formal-Batch-017.md`：Formal Batch 017 正文抽取进展；sources: SRC-0042。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/004-Formal-Batch-018.md`：Formal Batch 018 正文抽取进展；sources: SRC-0043。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/005-Formal-Disease-Completion-V5.md`：Formal Disease Completion / V5；sources: SRC-0009, SRC-0014, SRC-0042, SRC-0043, SRC-0049, SRC-0058, SRC-0069。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/006-B-task.md`：B-task 核心栏目补强；sources: SRC-0043。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/007-Web-Source-Reinforcement-V11.md`：Web Source Reinforcement / V11；sources: A2-MERCK-INFLUENZA-A-SWINE-2024, CMP-003, CMP-003-, RC-DISEASE-REGULATORY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SYN-004-。
- `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-021-influenza-viruses/001-MOA-A0-Authority-Reinforcement-2026-05-08.md`：MOA A0 Authority Reinforcement / 2026-05-08；sources: A0-MOA-SWINE-FLU-EMERGENCY-2009。
