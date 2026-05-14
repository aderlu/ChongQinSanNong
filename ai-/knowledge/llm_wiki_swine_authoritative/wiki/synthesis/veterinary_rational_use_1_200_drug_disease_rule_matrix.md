---
tags: [synthesis, swine, rational_drug_use, rule_matrix]
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, drug_boundary, audit_only]
sources: [SRC-0091]
---

# 兽药合理应用与联用手册（1-200页）药物-疾病-rule 矩阵

- 来源：`SRC-0091` / 兽药合理应用与联用手册（1-200页）
- 用途：补强 drug、disease、rule 三方映射，服务黄金数据生成、评估和拒答边界。

## 药物目录抽取

| 药物/类别 | 页码 | 类别 | Wiki 目标页 | 用途 |
|---|---:|---|---|---|
| 青霉素 | 35 | β-内酰胺/青霉素类 | `wiki/drugs/DRUG-009-penicillin-g.md` | individual_drug |
| 普鲁卡因青霉素 | 38 | β-内酰胺/青霉素类 | `wiki/drugs/DRUG-009-penicillin-g.md` | individual_drug |
| 氨苄西林 | 40 | β-内酰胺/青霉素类 | `wiki/drugs/DRUG-042-ampicillin.md` | individual_drug |
| 阿莫西林 | 42 | β-内酰胺/青霉素类 | `wiki/drugs/DRUG-010-amoxicillin.md` | individual_drug |
| 头孢噻呋 | 46 | β-内酰胺/头孢菌素类 | `wiki/drugs/DRUG-011-ceftiofur.md` | individual_drug |
| 头孢喹肟 | 47 | β-内酰胺/头孢菌素类 | `wiki/drugs/DRUG-044-cefquinome.md` | individual_drug |
| 链霉素 | 51 | 氨基糖苷类 | `wiki/drugs/DRUG-071-streptomycin.md` | individual_drug |
| 庆大霉素 | 54 | 氨基糖苷类 | `wiki/drugs/DRUG-023-gentamicin.md` | individual_drug |
| 安普霉素 | 56 | 氨基糖苷类 | `wiki/drugs/DRUG-025-apramycin.md` | individual_drug |
| 大观霉素 | 57 | 氨基糖苷类 | `wiki/drugs/DRUG-026-spectinomycin.md` | individual_drug |
| 新霉素 | 57 | 氨基糖苷类 | `wiki/drugs/DRUG-024-neomycin.md` | individual_drug |
| 阿米卡星 | 58 | 氨基糖苷类 | `wiki/drugs/DRUG-074-amikacin.md` | individual_drug |
| 土霉素 | 59 | 四环素类 | `wiki/drugs/DRUG-019-oxytetracycline.md` | individual_drug |
| 四环素 | 62 | 四环素类 | `wiki/drugs/DRUG-030-tetracyclines.md` | class_or_drug |
| 多西环素 | 63 | 四环素类 | `wiki/drugs/DRUG-021-doxycycline.md` | individual_drug |
| 金霉素 | 64 | 四环素类 | `wiki/drugs/DRUG-020-chlortetracycline.md` | individual_drug |
| 氟苯尼考 | 66 | 酰胺醇类 | `wiki/drugs/DRUG-012-florfenicol.md` | individual_drug |
| 红霉素 | 67 | 大环内酯类 | `wiki/drugs/DRUG-073-erythromycin.md` | individual_drug |
| 泰乐菌素 | 70 | 大环内酯类 | `wiki/drugs/DRUG-015-tylosin.md` | individual_drug |
| 替米考星 | 71 | 大环内酯类 | `wiki/drugs/DRUG-045-tilmicosin.md` | individual_drug |
| 林可霉素 | 73 | 林可胺类 | `wiki/drugs/DRUG-014-lincomycin.md` | individual_drug |
| 泰万菌素 | 73 | 大环内酯类 | `wiki/drugs/DRUG-016-tylvalosin.md` | individual_drug |
| 多黏菌素E | 76 | 多肽类 | `wiki/drugs/DRUG-052-colistin.md` | individual_drug |
| 杆菌肽 | 78 | 多肽类 | `wiki/drugs/DRUG-053-bacitracin-methylene-disalicylate.md` | individual_drug |
| 泰妙菌素 | 79 | 截短侧耳素/其他抗生素 | `wiki/drugs/DRUG-013-tiamulin.md` | individual_drug |
| 维吉尼霉素 | 79 | 多肽类 | `wiki/drugs/DRUG-054-virginiamycin.md` | individual_drug |
| 沃尼妙林 | 80 | 截短侧耳素/其他抗生素 | `wiki/drugs/DRUG-046-valnemulin.md` | individual_drug |
| 磺胺嘧啶 | 83 | 磺胺类/增效剂 | `wiki/drugs/DRUG-038-trimethoprim-sulfadiazine.md` | individual_drug |
| 磺胺二甲嘧啶 | 87 | 磺胺类/增效剂 | `wiki/drugs/DRUG-037-sulfamethazine.md` | individual_drug |
| 磺胺甲噁唑 | 88 | 磺胺类/增效剂 | `wiki/drugs/DRUG-040-trimethoprim-sulfamethoxazole.md` | individual_drug |
| 磺胺间甲氧嘧啶 | 90 | 磺胺类/增效剂 | `wiki/drugs/DRUG-039-sulfadimethoxine.md` | individual_drug |
| 甲氧苄啶 | 93 | 磺胺类/增效剂 | `wiki/drugs/DRUG-022-sulfonamide-trimethoprim.md` | synergy_agent |
| 恩诺沙星 | 97 | 喹诺酮类 | `wiki/drugs/DRUG-018-enrofloxacin.md` | individual_drug |
| 达氟沙星 | 99 | 喹诺酮类 | `wiki/drugs/DRUG-051-danofloxacin-marbofloxacin.md` | individual_drug |
| 马波沙星 | 101 | 喹诺酮类 | `wiki/drugs/DRUG-051-danofloxacin-marbofloxacin.md` | individual_drug |
| 甲硝唑 | 107 | 硝基咪唑类 | `wiki/drugs/DRUG-050-dimetridazole-ronidazole.md` | class_or_drug |
| 地美硝唑 | 109 | 硝基咪唑类 | `wiki/drugs/DRUG-050-dimetridazole-ronidazole.md` | individual_drug |
| 喹乙醇 | 110 | 喹噁啉类 | `wiki/drugs/DRUG-049-olaquindox.md` | individual_drug |
| 卡巴多司 | 111 | 喹噁啉类 | `wiki/drugs/DRUG-048-carbadox.md` | individual_drug |
| 阿苯达唑 | 145 | 苯并咪唑类驱虫药 | `wiki/drugs/DRUG-005-benzimidazoles.md` | individual_drug |
| 芬苯达唑 | 146 | 苯并咪唑类驱虫药 | `wiki/drugs/DRUG-004-fenbendazole.md` | individual_drug |
| 左旋咪唑 | 148 | 咪唑并噻唑类驱虫药 | `wiki/drugs/DRUG-056-levamisole.md` | individual_drug |
| 噻嘧啶 | 153 | 四氢嘧啶类驱虫药 | `wiki/drugs/DRUG-057-piperazine-pyrantel.md` | individual_drug |
| 伊维菌素 | 156 | 阿维菌素类 | `wiki/drugs/DRUG-002-ivermectin.md` | individual_drug |
| 莫西菌素 | 158 | 阿维菌素类 | `wiki/drugs/DRUG-055-moxidectin.md` | individual_drug |
| 多拉菌素 | 159 | 阿维菌素类 | `wiki/drugs/DRUG-003-doramectin.md` | individual_drug |
| 阿维菌素 | 159 | 阿维菌素类 | `wiki/drugs/DRUG-001-avermectins.md` | class_or_drug |
| 哌嗪 | 160 | 其他驱线虫药 | `wiki/drugs/DRUG-057-piperazine-pyrantel.md` | individual_drug |
| 吡喹酮 | 163 | 抗绦虫药 | `wiki/drugs/DRUG-075-praziquantel.md` | individual_drug |
| 磺胺二甲嘧啶 | 177 | 磺胺类/增效剂 | `wiki/drugs/DRUG-037-sulfamethazine.md` | individual_drug |
| 妥曲珠利 | 180 | 抗球虫药 | `wiki/drugs/DRUG-027-toltrazuril.md` | individual_drug |
| 氨丙啉 | 182 | 抗球虫药 | `wiki/drugs/DRUG-062-amprolium.md` | individual_drug |
| 甲硝唑 | 188 | 硝基咪唑类 | `wiki/drugs/DRUG-050-dimetridazole-ronidazole.md` | class_or_drug |
| 地美硝唑 | 191 | 硝基咪唑类 | `wiki/drugs/DRUG-050-dimetridazole-ronidazole.md` | individual_drug |
| 敌敌畏 | 196 | 有机磷杀虫药 | `wiki/drugs/DRUG-076-dichlorvos.md` | individual_drug |
| 溴氰菊酯 | 199 | 拟除虫菊酯类杀虫药 | `wiki/drugs/DRUG-060-permethrin-deltamethrin.md` | individual_drug |
| 氰戊菊酯 | 200 | 拟除虫菊酯类杀虫药 | `wiki/drugs/DRUG-060-permethrin-deltamethrin.md` | individual_drug |

## 疾病-药物-rule 映射

| 疾病页 | 场景 | 药物/类别候选 | rule 约束 | 来源 |
|---|---|---|---|---|
| `wiki/diseases/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md` | 胸膜肺炎 | 氨苄西林, 氟苯尼考, 头孢噻呋 | 抗菌治疗候选必须建立在药敏、标签和休药期复核之上；不得仅凭手册候选生成执行剂量。 | `SRC-0091` |
| `wiki/diseases/DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md` | 萎缩性鼻炎/支气管败血波氏杆菌相关 | 磺胺类, 四环素类, 青霉素, 链霉素 | 抗菌药选择需结合病原、药敏和猪场阶段，避免长期单一药物导致耐药。 | `SRC-0091` |
| `wiki/diseases/DIS-040-colibacillosis.md` | 大肠杆菌病 | 磺胺类, 庆大霉素, 安普霉素, 新霉素 | 肠道感染应优先结合脱水、毒血症和药敏判断；氨基糖苷类全身治疗需注意吸收和肾毒性边界。 | `SRC-0091` |
| `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md` | 仔猪黄白痢 | 磺胺类, 氨基糖苷类, 口服补液 | 仔猪腹泻样病例应先区分病毒性、细菌性、球虫性和管理性因素。 | `SRC-0091` |
| `wiki/diseases/DIS-042-edema-disease-e-coli.md` | 仔猪水肿病 | 磺胺嘧啶, 磺胺二甲嘧啶 | 作为敏感菌候选和鉴别增强，不得替代毒素型大肠杆菌的综合处置。 | `SRC-0091` |
| `wiki/diseases/DIS-043-erysipelas.md` | 猪丹毒 | 青霉素 | 青霉素为敏感革兰阳性菌候选；执行处方仍需标签、药敏和休药期。 | `SRC-0091` |
| `wiki/diseases/DIS-045-leptospirosis.md` | 钩端螺旋体病 | 青霉素, 四环素类 | 钩端螺旋体病属于人兽共患风险场景，需保留防护、送检和监管边界。 | `SRC-0091` |
| `wiki/diseases/DIS-049-salmonellosis.md` | 沙门氏菌病 | 氨苄西林, 磺胺嘧啶, 氟苯尼考 | 应强调药敏、耐药和公共卫生边界，避免经验性滥用抗菌药。 | `SRC-0091` |
| `wiki/diseases/DIS-051-streptococcosis-streptococcus-suis.md` | 猪链球菌病 | 青霉素, 磺胺类, 头孢菌素类 | 脑膜炎型等高风险病例需区分中枢渗透、分开注射和人兽共患防护。 | `SRC-0091` |
| `wiki/diseases/DIS-055-external-parasites-mange.md` | 疥螨/外寄生虫 | 伊维菌素, 阿维菌素类, 双甲脒, 拟除虫菊酯类 | 外寄生虫病例需结合群体处理、环境清理和复查，不得只生成单次用药。 | `SRC-0091` |
| `wiki/diseases/DIS-056-external-parasites-lice.md` | 猪虱病 | 伊维菌素, 有机磷杀虫药, 拟除虫菊酯类 | 外寄生虫处理必须同时约束安全、环境和肉品休药期复核。 | `SRC-0091` |
| `wiki/diseases/DIS-057-coccidia-and-other-protozoa.md` | 球虫/原虫性腹泻 | 妥曲珠利, 氨丙啉, 磺胺类 | 腹泻综合征中需与病毒性腹泻和大肠杆菌病鉴别。 | `SRC-0091` |
| `wiki/diseases/DIS-058-toxoplasmosis-protozoa.md` | 弓形虫病 | 磺胺类, TMP | 弓形虫病处方候选需保留人兽共患和妊娠风险边界。 | `SRC-0091` |
| `wiki/diseases/DIS-060-ascaris-suum-internal-parasites.md` | 蛔虫病 | 芬苯达唑, 左旋咪唑, 哌嗪 | 驱虫策略应结合虫卵检查、群体程序和环境控制。 | `SRC-0091` |
| `wiki/diseases/DIS-061-trichuris-suis-internal-parasites.md` | 鞭虫病 | 苯并咪唑类, 伊维菌素 | 慢性腹泻/消瘦需纳入鞭虫鉴别。 | `SRC-0091` |
