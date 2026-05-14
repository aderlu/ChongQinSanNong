---
tags: [comparison, swine, sudden_death, septicemia, phase2, v8]
comparison_id: CMP-006
updated: 2026-05-08T13:10:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [SYN-007, DIS-002, DIS-024, DIS-043, DIS-044, DIS-047, DIS-049, DIS-073, SRC-0066, SRC-0070, SRC-0073, RC-DX-001, RC-DISEASE-REGULATORY-001]
---

# 猪突然死亡/败血症鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 猝死、高热、发绀、呼吸困难、神经症状、出血性病变或群体死亡升高时，必须先排除重大疫病、败血症和毒物气体。

## 候选病种和支持线索

- 非洲猪瘟/猪瘟：出血性综合征和高死亡率时必须纳入监管鉴别。
- 格拉瑟病：超急性可突然死亡且无特征性肉眼病变，急性可有高热、呼吸、关节和神经症状。 (`GLASS-007-peracute`; `GLASS-006-clinical`; `SRC-0066`)
- 败血型 P. multocida：突然发生，可有高热、严重呼吸困难、发绀和死亡；诊断需在血液或系统组织中检出 P. multocida。 (`PAST-008-septicemic-clinical`; `PAST-013-septicemic-diagnosis`; `SRC-0070`)
- 败血型沙门氏菌：可表现发热、发绀、呼吸或神经症状和死亡，腹泻并非早期必有。 (`SALM-008-septicemic-clinical`; `SRC-0073`)
- 毒物气体/通风失败：人员安全、通风和暴露控制优先，联动 `SYN-012` 和 `RC-TOX-001`。

## 反证和限制

- 猝死没有特征性肉眼病变不能排除格拉瑟病或毒物气体，也不能排除重大疫病。
- 单个细菌分离结果需结合系统性病变、血液/组织来源和流行病学。
- 正常大小伴广泛点状出血肾脏的鉴别包括细菌败血症、急性病毒血症、电击和部分中毒。 (`URIN-011-normal-size-petechial-kidney-differentials`; `SRC-0028`)

## 最小诊断包

- 先处理人员安全和移动控制；选择新鲜死亡或濒死未用药猪做剖检。
- 采集血液、脾、肝、肺、淋巴结、脑/关节/浆膜病变、固定组织和环境/饲料/气体相关样本。

## 监管和用药边界

- 高死亡率、出血性或水疱性重大疫病疑似必须走 `RC-DISEASE-REGULATORY-001`、`RC-ASF-001` 或 `RC-VES-001`。
- 败血症候选不自动授权抗菌药剂量；药敏、标签和休药期仍走 `RC-DRUG-001`。

## 评估陷阱

- 猝死题只给抗生素方案。
- 未提 ASF/CSF/FMD 等重大疫病排查。
- 忽略毒物气体的人员安全。
