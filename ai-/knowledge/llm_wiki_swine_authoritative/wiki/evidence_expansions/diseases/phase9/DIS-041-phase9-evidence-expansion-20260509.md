---
page_id: DIS-041
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-041 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- Byte size moved: 4046
- Fact-like rows moved: 9
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 9

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 9 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 29.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0023` 处方1：$①$ 阿米卡星（丁胺卡那霉素）注射液 20万单位；$②$ 磺胺嘧啶 0.2\~0.8克 三甲氧苄氨嘧啶 0.4\~0.16克活性炭 0.5克；③ 土霉素 0.2~0.3克；$④$ 磺胺甲基嘧啶与增效剂 0.1\~0.2克；$⑤$ $0.5\%$ 恩诺沙星液 2毫升；用法=用法：一次肌内注射或灌服，每日 $2\sim 3$ 次，连用3天。；用法：混匀分2次喂服，每日2次至愈。；用法：口服，每日3次，连用3天。；用法：口服，每日1次，连用3天。；用法：口服，每日1次，连用3天。药物治疗的同时进行补液。口服补盐液的配方：在1000毫升温水中加入葡萄糖20克、氯化钠3.5克、碳酸氢钠2.5克、氯化钾1.5克，混合溶解后让猪自由饮用；也可腹腔注射 $5\%$ 葡萄糖生理盐水。；注=。`source_id=SRC-0087; page=29; line=1128-1148`
- `HANDBOOK-RX-0024` 处方2：白头翁2克 龙胆末1克；用法=用法：研末，1次喂服，每日3次，连用3天。；注=。`source_id=SRC-0087; page=29; line=1150-1154`
- `HANDBOOK-RX-0025` 处方3：大蒜 100克 $95\%$ 乙醇 100毫升 甘草1克；用法=用法：大蒜用乙醇浸泡15天后取汁1毫升，加甘草末1克，调糊一次喂服，每日2次至愈。；注=。`source_id=SRC-0087; page=29; line=1156-1160`
- `HANDBOOK-RX-0026` 处方2 、【处方3】配合【处方1】应用效果更佳。：说明：【处方2】、【处方3】配合【处方1】应用效果更佳。；用法=；注=。`source_id=SRC-0087; page=29; line=1162-1162`
- `HANDBOOK-RX-0027` 处方4：黄连5克 黄柏20克 黄芩20克 金银花20克 诃子20克 乌梅20克 草豆蔻20克 泽泻15克 茯苓15克 神曲10克 山楂10克 甘草5克；用法=用法：研末，分2次喂母猪，早晚各1次，连用2剂。；注=。`source_id=SRC-0087; page=29; line=1164-1168`
- `HANDBOOK-RX-0028` 处方5：0.1%亚硒酸钠注射液 5毫升；用法=用法：母猪产前两日一次肌内注射，每日1次，连注2天。；注=说明：本方用于缺硒地区有良效。。`source_id=SRC-0087; page=29; line=1170-1176`
- `HANDBOOK-RX-0030` 处方1：a.硫酸庆大小诺霉素注射液 8万～16万单位；$5\%$ 维生素 $\mathbf{B}_1$ 注射液 $2\sim 4$ 毫升；b.黄连素片 $1\sim 2$ 克 硅碳银（矽炭银） $1\sim 2$ 克；用法=用法：肌内注射或后海穴一次注射，也可灌服。每日2次，连用 $2\sim 3$ 天。；用法：一次喂服，每日2次，连用 $1\sim 2$ 天。；注=。`source_id=SRC-0087; page=29; line=1198-1208`
- `HANDBOOK-RX-0031` 处方2：a. 大蒜 500 克, 甘草 120 克, 切碎后加白酒 500 毫升, 浸泡 $5 \sim 7$ 天；b. 调痢生（8501）活菌制剂 50毫克/千克体重；c. 磺胺脒 0.5 克, 苏打 0.5 克, 乳酸钙 0.5 克, 加淀粉和水适量。；d. 土霉素或金霉素糖粉 0.2~0.4克；e. $0.2\%$ 亚硒酸钠溶液 适量；用法=用法：取原液1毫升加水4毫升灌服，每日2次，连服 $2\sim 3$ 天。；用法：口服，每天1次，连用3天。；用法：调匀，一次口服。；用法：口服，每日3次，连用3天。；用法：体重2.5千克以下用1毫升， $2.5\sim 5$ 千克用1.5毫升，7.5千克以上用2毫升肌内注射，对缺硒地区的发病仔猪有一定效果。；注=。`source_id=SRC-0087; page=29; line=1210-1230`
- `HANDBOOK-RX-0032` 处方3：白头翁50克；黄连50克；生地50克；黄柏50克；青皮25克；地榆炭25克；青木香10克；山楂25克；当归25克；赤芍20克；用法=用法：水煎，喂服10只小猪，每日1剂，连用 $1\sim 2$ 剂。；注=。`source_id=SRC-0087; page=29; line=1232-1254`
<!-- HANDBOOK_RX_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- Byte size moved: 5032
- Fact-like rows moved: 12
- Candidate fact mentions moved: 4
- Dose/route/course fact markers moved: 0
- Source anchors moved: 12

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 12 linked disease-control/treatment facts.
- Source pages: 30, 31, 33, 39, 43, 44, 87, 88, 92.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0109` candidate_fact / p.31 / 肆霉素类: （1）作用与用途适用于 $G^{+}$ 菌和 $G^{-}$ 敏感菌所致的呼吸系统、泌尿系统、皮肤及软组织等全身感染。如巴氏杆菌病（猪肺疫）、大肠杆菌病（仔猪黄痢和白痢、仔猪水肿病）、沙门菌病（仔猪副伤寒）、嗜血杆菌、葡萄球菌、链球菌感染等。 `source_id=SRC-0089; page=31; line=927`
- `SFDUT1-TX-0141` treatment_or_prevention / p.39 / 氨基糖苷类: 由于脂溶性差，正常的胃肠道内服很难吸收（但肠炎时可有效地增加吸收），肠道内浓度较高，可作为肠道感染用药。口服庆大霉素或新霉素与阿托品、茛菪碱等药物合用，治疗仔猪白痢及腹泻效果好。 `source_id=SRC-0089; page=39; line=1092`
- `SFDUT1-TX-0153` treatment_or_prevention / p.43 / 氨基糖苷类: （1）作用与用途 内服用于治疗敏感菌所致的肠道感染，如仔猪白痢、仔猪副伤寒等。肌注用于需氧 $\mathbf{G}^{-}$ 菌和耐青霉素的金黄色葡萄球菌等敏感菌所致的各种严重感染，如败血症、呼吸道感染、泌尿生殖道感染、乳腺炎、皮肤和软组织感染等，对猪气喘病及萎缩性鼻炎有改善症状的功效。 `source_id=SRC-0089; page=43; line=1181`
- `SFDUT1-TX-0162` treatment_or_prevention / p.44 / 氨基糖苷类: （1）作用与用途 通常内服或局部给药。内服给药后很少吸收，在肠道内呈现抗菌作用，主要用于治疗 $G^{-}$ 菌所致的胃肠道感染，如仔猪白痢等。局部用药对葡萄球菌和 $G^{-}$ 杆菌引起的皮肤创伤、眼和耳感染及子宫内膜炎等有良好疗效。 `source_id=SRC-0089; page=44; line=1205`
- `SFDUT1-TX-0185` treatment_or_prevention / p.33 / 四环素类: 本类药对葡萄球菌、溶血性链球菌、破伤风梭菌等 $\mathbf{G}^{+}$ 菌作用较强，但不如青霉素类和头孢菌素类；对大肠杆菌、沙门菌、巴氏杆菌和布氏杆菌等 $\mathbf{G}^{-}$ 菌作用较强，但不如氨基糖苷类和氯霉素类。主要用于治疗全身和局部感染，如支原体肺炎（猪气喘病）、猪嗜血支原体病（猪附红细胞体病）、巴氏杆菌病（猪肺疫）、大肠杆菌病（仔猪黄痢、仔猪白痢、水肿病）、急性呼吸道感染、细菌性肠炎、子宫炎、坏死杆菌病等。 `source_id=SRC-0089; page=33; line=1277`
- `SFDUT1-TX-0191` treatment_or_prevention / p.30 / 四环素类: （1）作用与用途可用于防治大肠杆菌引起的仔猪黄痢和白痢、沙门菌引起的仔猪副伤寒、多杀性巴氏杆菌引起的猪肺炎、支原体引起的支原体肺炎（猪气喘病）、猪附红细胞体病及敏感菌引起的急性呼吸道及泌尿道感染。对放线菌病、钩端螺旋体病等也有一定疗效。还可局部用于坏死杆菌所致的坏死、子宫蓄脓、子宫内膜炎等。亦常用作饲料药物添加剂，除可一定程度地防治疫病外，还能改善饲料利用率和促生长。 `source_id=SRC-0089; page=30; line=1327`
- `SFDUT1-TX-0377` candidate_fact / p.87 / 其他合成抗菌药: ① 适应证 主要用于密螺旋体引起的猪痢疾，仔猪黄痢、白痢。 `source_id=SRC-0089; page=87; line=2137`
- `SFDUT1-TX-0380` candidate_fact / p.87 / 其他合成抗菌药: ① 适应证 仔猪黄痢、白痢、副伤寒，尤其对密螺旋体所致猪血痢有独特疗效，且复发率低。 `source_id=SRC-0089; page=87; line=2143`
- `SFDUT1-TX-0383` treatment_or_prevention / p.87 / 其他合成抗菌药: 作为抗菌促生长剂，主要用于猪的促生长。亦用于防治仔猪黄痢、仔猪白痢、仔猪副伤寒等。 `source_id=SRC-0089; page=87; line=2151`
- `SFDUT1-TX-0392` candidate_fact / p.88 / 其他合成抗菌药: ① 适应证 主要用于大肠杆菌引起的仔猪黄痢、白痢。 `source_id=SRC-0089; page=88; line=2189`
- `SFDUT1-TX-0395` treatment_or_prevention / p.88 / 其他合成抗菌药: ② 适应证 用于预防及治疗仔猪大肠杆菌所致的仔猪黄痢、白痢，沙门菌所致的下痢。 `source_id=SRC-0089; page=88; line=2200`
- `SFDUT1-TX-0416` treatment_or_prevention / p.92 / 口服补液盐: 治疗仔猪黄痢、白痢时每袋加水500毫升，使用方便。本人曾使用某兽药厂生产的ORS，每袋250克，其中内含氯化钾的小包，称量仅有 $7.0\sim 8.5$ 克，标准含量应为13.65克，含量明显不足，此种粗制滥造的ORS，使用效果不佳。人用ORS，尽管价格贵一些，但货真价实，效果好。 `source_id=SRC-0089; page=92; line=2285`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- Byte size moved: 1020
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 增强证据 (SRC-0090, V13.1 batch)

- Batch status: 1 linked disease-control/treatment facts.
- Source pages: 266.
- Matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_200_363_fact_index.csv`.

- `SFDUT2-TX-0227` treatment_or_prevention / p.266 / 仔猪球虫病: 猪球虫病是由猪等孢球虫寄生于猪小肠上皮细胞而引起的一种原虫病，呈全球性分布，主要危害集约化猪场 $8 \sim 15$ 日龄仔猪群，以腹泻（排淡黄色糯糊状稀粪）、脱水、体重下降和死亡为主要特征，故又称“十日龄腹泻”。抗生素治疗无效，在临床上易与仔猪黄痢、白痢和轮状病毒等引起的仔猪腹泻相混淆，常造成误诊，延误了治疗时机，影响仔猪群整齐度、断奶体重、断奶成活率、饲料 `source_id=SRC-0090; page=266; line=1189`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- Byte size moved: 611
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用证据增强 / SRC-0091

- 关联场景：仔猪黄白痢。
- 药物/类别候选：磺胺类, 氨基糖苷类, 口服补液。
- 生成边界：仔猪腹泻样病例应先区分病毒性、细菌性、球虫性和管理性因素。
- 本块用于候选召回、鉴别增强和 rule 约束；不得单独输出剂量、疗程、休药期或 MRL。
- 来源：兽药合理应用与联用手册（1-200页），相关药物目录与正文页码见 `exports/veterinary_rational_use_1_200_drug_index.csv`。`source_id=SRC-0091`
<!-- RAU_1_200_V14_END -->

## RAU_201_400_V14

- Original marker: `RAU_201_400_V14_START` / `RAU_201_400_V14_END`
- Original runtime page: `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- Byte size moved: 581
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_201_400_V14_START -->
## 兽药合理应用与联用证据增强（201-400页）/ SRC-0092

- 关联场景：仔猪腹泻。
- 药物/类别候选：抗球虫药, 止泻/补液支持。
- 生成边界：腹泻处理需先区分病因，避免用止泻药掩盖脱水或感染进展。
- 用途：症状入口、候选召回、鉴别诊断、对症支持和 drug-rule 约束。
- 不得单独输出剂量、疗程、休药期、MRL 或出栏可食用承诺。
- 来源：兽药合理应用与联用手册（201-400页）。`source_id=SRC-0092`
<!-- RAU_201_400_V14_END -->

## RAU_401_600_V14

- Original marker: `RAU_401_600_V14_START` / `RAU_401_600_V14_END`
- Original runtime page: `wiki/diseases/DIS-041-neonatal-post-weaning-colibacillosis.md`
- Byte size moved: 607
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 0

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）症候支持边界 / SRC-0093

- 仔猪腹泻/水肿病鉴别：消导、收涩、利湿只能作症候支持，不得替代病原检测和药敏。
- 证据用途：中药联用、禁忌、用药注意、症候支持和鉴别增强；不是病原确诊、报告处置、抗菌药剂量、休药期、MRL 或食品安全承诺来源。
- 索引：`exports/veterinary_rational_use_401_600_fact_index.csv`；矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`。
<!-- RAU_401_600_V14_END -->
