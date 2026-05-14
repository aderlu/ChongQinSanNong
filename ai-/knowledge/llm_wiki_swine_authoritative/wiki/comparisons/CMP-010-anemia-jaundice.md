---
tags: [comparison, swine, v11]
comparison_id: CMP-010
updated: 2026-05-08T23:55:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [A2-MERCK-NUTRITIONAL-DISEASES-PIGS-2026, A2-MERCK-AFLATOXICOSIS-ANIMALS-2025, A2-MERCK-NITRATE-NITRITE-TOXICOSIS-2024, DIS-017, DIS-045, DIS-067]
---

# 贫血/黄疸鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 苍白、黄疸、发绀、血红蛋白下降、生长差、突然死亡或肝脏病变时，先区分营养性贫血、溶血/败血、肝毒性和缺氧性毒物。

## syndrome 链接

- 关联 syndrome: `SYN-010-anemia-jaundice`

## 候选病种和支持线索

- 哺乳仔猪营养性贫血：低 Hb/RBC、苍白黏膜、颈肩水肿、精神差和 thumps 需结合补铁史。 (`A2-MERCK-NUTRITIONAL-DISEASES-PIGS-2026`)
- 黄曲霉毒素：可造成采食下降、生长不良、抑郁、出血、黄疸和死亡；需检测饲料。 (`A2-MERCK-AFLATOXICOSIS-ANIMALS-2025`)
- 亚硝酸盐/硝酸盐：高铁血红蛋白血症可导致发绀、呼吸困难、虚弱和缺氧死亡。 (`A2-MERCK-NITRATE-NITRITE-TOXICOSIS-2024`)
- 钩端螺旋体/败血症/肝炎：需结合发热、尿液、肾肝病变和公共卫生边界。 (`DIS-045`; `DIS-017`)

## 最小诊断包

- 血常规、血涂片/溶血指标、肝肾生化、尿液、水料毒物、饲料霉菌毒素和剖检肝脾肾样本。

## 监管、用药和食品安全边界

- 本矩阵只用于鉴别诊断和生成/评估约束；不得生成剂量、疗程、休药期、MRL、残留合格、肉品可食、饲料放行、调运、扑杀、检疫或上报结论，除非另有精确 A0/A1 来源。 (`RC-DISEASE-REGULATORY-001`; `RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)

## 评估陷阱

- 用黄疸直接诊断单一病原。
- 发现贫血就自动补铁而不查出血、溶血和毒物。
- 未检测饲料/水源就排除毒物。
