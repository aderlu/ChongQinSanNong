---
tags: [comparison, swine, respiratory, prdc, phase2, v8]
comparison_id: CMP-003
updated: 2026-05-08T13:10:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [SYN-004, DIS-021, DIS-028, DIS-035, DIS-044, DIS-046, DIS-047, DIS-037, SRC-0066, SRC-0069, SRC-0070, RC-DX-001, RC-DRUG-001]
---

# 呼吸道疾病鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 咳嗽、喘气、腹式呼吸、发热、死亡、胸膜肺炎样病变或 PRDC 背景时，必须同时考虑原发病原、继发细菌、环境通风和混合感染。

## 候选病种和支持线索

- M. hyopneumoniae：是地方性肺炎必要病因，也是 PRDC 重要原发病原；常呈慢性、高发病率、低死亡率和生产性能下降。 (`MHYO-001-ep-prdc-primary`; `MHYO-002-performance-pattern`; `SRC-0069`)
- P. multocida：肺炎型常作为其他呼吸道疾病后的继发/终末阶段，通常需要呼吸道防御受损或原发病原/环境因素参与。 (`PAST-003-pneumonic-secondary`; `PAST-006-lung-defense-compromise`; `SRC-0070`)
- H. parasuis / Glasser's：可见高热、咳嗽、腹式呼吸、关节肿胀跛行和中枢神经症状，典型病变为纤维素性至纤维素脓性浆膜炎。 (`GLASS-006-clinical`; `GLASS-008-lesions`; `SRC-0066`)
- Bordetella / 萎缩性鼻炎、APP、猪流感、PRRSV、PCV2：作为呼吸道综合征鉴别，不得只凭咳嗽定位。

## 反证和限制

- M. hyopneumoniae 肺部肉眼病变并非特异，猪流感、PRRSV、PCV2、App、猪腺病毒和伪狂犬病毒等可产生相似病变。 (`MHYO-008-lesions-nonpathognomonic`; `SRC-0069`)
- P. multocida 定植和肺病变本身不能证明其为原发病因。 (`PAST-004-epidemiology-uncertain`; `PAST-012-lung-not-pathognomonic`; `SRC-0070`)
- H. parasuis 与 PRRSV、PCV2、猪流感和 B. bronchiseptica 有共同感染关联，需解释混合感染。 (`GLASS-005-coinfection`; `SRC-0066`)

## 最小诊断包

- 结合临床、流行病学、肺/浆膜病变、组织病理和病原检测。
- M. hyopneumoniae 培养困难且慢，诊断应综合临床、流行病学、病变和病变部位检测。 (`MHYO-004-culture-difficult`; `MHYO-009-diagnosis-composite`; `SRC-0069`)

## 监管和用药边界

- 抗菌药治疗可改善部分细菌性或混合感染表现，但不得替代病原诊断、药敏、标签和休药期核验。 (`RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)
- M. hyopneumoniae 治疗后仍可能复现症状和排菌，不能把治疗等同于清除感染。 (`MHYO-010-treatment-shedding-boundary`; `SRC-0069`)

## 评估陷阱

- 把 P. multocida 检出写成原发诊断。
- 把支原体样肺病变当作 M. hyopneumoniae 确诊。
- 用抗菌药方案替代 PRRS/流感/重大疫病鉴别。
