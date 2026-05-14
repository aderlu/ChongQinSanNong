---
tags: [comparison, swine, diarrhea, post_weaning, phase2, v8]
comparison_id: CMP-002
updated: 2026-05-08T13:10:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [SYN-002, DIS-040, DIS-041, DIS-042, DIS-048, DIS-049, DIS-052, DIS-061, SRC-0063, SRC-0073, RC-DX-001, RC-DRUG-001]
---

# 断奶后腹泻鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 断奶后腹泻、消瘦、生长停滞、突然死亡或神经症状时，优先区分 ETEC/PWD、水肿病、沙门氏菌、Lawsonia、猪痢疾和鞭虫。

## 候选病种和支持线索

- ETEC/PWD：断奶后腹泻最常由 ETEC 引起，也可由 EPEC 引起；低温、混群、运输、新栏和断奶应激是管理风险。 (`ECOLI-015-pwd`; `ECOLI-023-stress-temperature`; `SRC-0063`)
- 水肿病：Stx2e 毒血症发生于肠道 EDEC 定植后；病变包括血管肿胀、纤维蛋白沉积、中膜坏死和微血栓。 (`ECOLI-017-edema-disease`; `ECOLI-019-ed-lesions`; `SRC-0063`)
- 沙门氏菌：多见于集约化断奶和生长猪，可有发热、沉郁、水样至黏液性或带血腹泻；败血型可有发绀、呼吸/神经症状和死亡。 (`SALM-003-outbreak-intensive`; `SALM-007-clinical-enteric`; `SALM-008-septicemic-clinical`; `SRC-0073`)
- Lawsonia：增生性肠病可呈亚临床、慢性或急性出血型；确诊需特征性病变和病变内 Lawsonia 示证。 (`LAW-011-clinical-forms`; `LAW-014-diagnosis-lesion-organism`; `SRC-0071`)
- 猪痢疾/Brachyspira：确诊需典型病例中检出强 β 溶血 Brachyspira，培养慢且需选择性厌氧条件。 (`BRACH-002-sd-definitive`; `BRACH-004-culture-slow`; `SRC-0077`)

## 反证和限制

- 水肿病病程较长时细菌培养阴性不能排除。 (`ECOLI-020-ed-negative-culture`; `SRC-0063`)
- 沙门氏菌 PCR 检出不等于沙门氏菌病诊断，培养也需相符病变支持。 (`SALM-012-culture-alone-unreliable`; `SALM-013-pcr-detection-not-diagnosis`; `SRC-0073`)
- P. Lawsonia、Brachyspira、Salmonella 和 ETEC 可在腹泻综合征中重叠，应避免单检测定因。

## 最小诊断包

- 分层采样：急性腹泻猪、死亡猪、慢性消瘦猪分别采肠道、肠内容物、固定病变肠段和粪便。
- 对水肿病关注血管病变和 Stx2e 相关证据；对沙门氏菌关注盲肠/结肠病变、败血型组织和病原检测。

## 监管和用药边界

- 抗菌药只能在兽医诊断、药敏/标签和中国法规框架下讨论；不得从本矩阵生成剂量、疗程或休药期。 (`RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)
- 预防性饲料用药存在耐药选择和消费者接受度问题，不能作为默认黄金答案。 (`ECOLI-024-antimicrobial-prophylaxis`; `SRC-0063`)

## 评估陷阱

- 把断奶后腹泻默认等同于 ETEC。
- 用 PCR 阳性直接确诊沙门氏菌病。
- 对水肿病培养阴性作排除结论。
