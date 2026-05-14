---
tags: [comparison, swine, diarrhea, neonatal, phase2, v8]
comparison_id: CMP-001
updated: 2026-05-08T13:10:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [SYN-001, DIS-008, DIS-009, DIS-030, DIS-039, DIS-040, DIS-041, DIS-057, DIS-059, SRC-0063, SRC-0064, SRC-0052, RC-DX-001, RC-DRUG-001]
---

# 新生仔猪腹泻鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 7 日龄内或哺乳期仔猪水样腹泻、脱水、呕吐、窝内快速扩散或死亡升高时，必须按年龄、病程、窝内分布、母猪免疫/泌乳状态和病变部位分层。

## 候选病种和支持线索

- PEDV：水样腹泻、呕吐、厌食和沉郁可与 TGE 相似，繁殖场各年龄猪均可发病，仔猪发病率可接近 100%；诊断需结合临床与 RT-PCR/抗原/抗体证据。 (`PEDV-007-clinical-pattern`; `PEDV-008-diagnosis-combined-clinical-lab`; `SRC-0062`)
- TGEV：新生仔猪更严重，地方性或流行性模式受母源和群体免疫影响；尚无特异抗病毒治疗。 (`TGEV-001-epidemic-pattern`; `TGEV-003-age_susceptibility`; `TGEV-011-no-antiviral-treatment`; `SRC-0062`)
- 轮状病毒：主要影响新生仔猪，临床症状与其他肠道病原重叠，必须依赖实验室检测。 (`ROTA-005-clinical`; `ROTA-006-diagnosis`; `SRC-0052`)
- ETEC：ETEC 是猪最重要的大肠杆菌致病型，可产生肠毒素导致分泌性腹泻；新生仔猪 ETEC 需与梭菌、TGEV、PEDV、轮状病毒、PRRSV 和球虫鉴别。 (`ECOLI-003-etec`; `ECOLI-010-neonatal-differential`; `SRC-0063`)
- C. perfringens type C / C. difficile：type C 疾病与 CPB 毒素和新生仔猪低胰蛋白酶环境有关；C. difficile 毒素结果必须与临床和剖检相符，培养阳性本身诊断意义有限。 (`CLOST-003-typec-cpb`; `CLOST-004-typec-neonatal-risk`; `CLOST-009-cdifficile-diagnosis`; `CLOST-010-cdifficile-culture`; `SRC-0062`)
- 球虫/隐孢子虫：应作为哺乳期持续腹泻鉴别，不能用单一卵囊或环境检出直接定因；需联动 `SYN-001` 和寄生虫页面。

## 反证和限制

- 单次 PCR 阳性、抗原阳性或培养阳性不等于病因诊断；必须结合日龄、病程、病变、采样质量和群体模式。 (`RC-DX-001`)
- PEDV、TGEV 和轮状病毒的临床表现高度重叠，不能凭水样腹泻或呕吐单独区分。 (`PEDV-007-clinical-pattern`; `ROTA-005-clinical`)
- 大肠杆菌溶血菌落只能作为快速提示，可能漏掉 EPEC 或非溶血 F4-ETEC。 (`ECOLI-021-hemolysis-limit`; `SRC-0063`)

## 最小诊断包

- 选择急性腹泻、未治疗或刚发病仔猪；采集新鲜小肠/结肠内容物、固定肠段和粪便。
- 病毒性腹泻需核酸或抗原检测；PEDV IF/IHC 应优先选择腹泻初期、肠细胞脱落前急性处死猪小肠。 (`PEDV-009-acute-small-intestine-sampling`; `SRC-0062`)
- 大肠杆菌/梭菌需把病原检测与毒素、病变和日龄对应，不能只交付培养结果。

## 监管和用药边界

- 不得生成抗菌药剂量、疗程或休药期；需 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`。
- 高死亡率或疑似重大疫病背景不得用经验性治疗替代报告、隔离、限制移动或官方复核；需 `RC-DISEASE-REGULATORY-001`。

## 评估陷阱

- 把“PEDV/TGEV/轮状病毒水样腹泻”写成单病确诊。
- 把 C. difficile 培养阳性或 E. coli 培养阳性单独当作病因。
- 在无标签来源时给出抗菌药剂量或休药期。
