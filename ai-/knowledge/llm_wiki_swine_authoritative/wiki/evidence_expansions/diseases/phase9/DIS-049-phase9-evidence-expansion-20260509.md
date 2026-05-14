---
page_id: DIS-049
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-049-salmonellosis.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-049 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-049-salmonellosis.md`
- Byte size moved: 2900
- Fact-like rows moved: 8
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 8

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 8 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 35.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0038` 处方1 预防用：（1）仔猪副伤寒弱毒冻干苗 1头份；(2）金霉素 100克；用法=用法：断奶前后1次喂服或肌内注射。；用法：混饲，加入1000千克饲料中。；注=。`source_id=SRC-0087; page=35; line=1448-1456`
- `HANDBOOK-RX-0039` 处方2：（1）阿米卡星（丁胺卡那霉素）注射液 20万～40万单位；（2）大蒜 20克；用法=用法：1次肌内注射，每日 $2\sim 3$ 次至愈。；用法：捣汁后1次灌服，每日1次，连用 $2\sim 3$ 次。；注=。`source_id=SRC-0087; page=35; line=1458-1466`
- `HANDBOOK-RX-0040` 处方3：（1）磺胺嘧啶 0.2～0.8克；三甲氧苄氨嘧啶 0.4～0.16克；(2） $10\%$ 磺胺嘧啶钠注射液 25毫升；$25\%$ 葡萄糖注射液 $40\sim 60$ 毫升；用法=用法：混合后分2次喂服，按每千克体重磺胺嘧啶 $20\sim 40$ 毫克、三甲氧苄氨嘧啶 $4\sim$ 8毫克用药，连用1周。；用法：一次静脉注射，磺胺嘧啶钠按10千克体重5毫升用药。；注=。`source_id=SRC-0087; page=35; line=1468-1480`
- `HANDBOOK-RX-0041` 处方4：(1) $1\%$ 盐酸强力霉素注射液 3～10毫升；(2）盐酸土霉素 0.6～2克；用法=用法：一次肌内注射，按1千克体重 $0.3\sim 0.5$ 毫升用药。每日1次，连用 $3\sim 5$ 天。；用法：分 $2\sim 3$ 次喂服，按1千克体重 $60\sim 100$ 毫克用药。；注=。`source_id=SRC-0087; page=35; line=1482-1490`
- `HANDBOOK-RX-0042` 处方5：青木香10克 苍术6克 黄连10克 地榆炭15克；炒白芍15克 白头翁10克 车前子10克 烧大枣5枚（为引）；用法=用法：研末，1次喂服，每日1剂，连用 $2\sim 3$ 剂。；注=。`source_id=SRC-0087; page=35; line=1492-1498`
- `HANDBOOK-RX-0043` 处方6：黄连15克；木香15克；白芍20克；槟榔10克；茯苓20克；滑石25克；甘草10克；用法=用法：水煎，分3次服完，每日2次，连用 $2\sim 3$ 剂。；注=。`source_id=SRC-0087; page=35; line=1500-1516`
- `HANDBOOK-RX-0044` 处方7：黄芩6克；陈皮6克；莱菔子9克；神曲9克；柴胡9克；连翘6克；金银花9克；槐木炭6克；苦参9克；用法=用法：水煎，分2次喂服，每日1剂，连用 $2\sim 3$ 剂。；注=。`source_id=SRC-0087; page=35; line=1518-1538`
- `HANDBOOK-RX-0045` 处方8 针灸：穴位：后三里、后海、脾俞、尾尖，配百会、苏气、血印等穴。；针法：白针或血针。；用法=；注=。`source_id=SRC-0087; page=35; line=1540-1544`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-049-salmonellosis.md`
- Byte size moved: 1396
- Fact-like rows moved: 2
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 2

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Treatment Evidence (SRC-0088, V13.1 batch)

- Batch status: 2 treatment facts linked to this disease page.
- Source pages: 74.
- Full matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`; fact index: `exports/veterinary_treatment_of_pigs_fact_index.csv`.

- `VTOP-TX-0101` euthanasia / p.74 / Salmonellosis: Cases of less acute salmonellosis do not cause septicaemia. Diarrhoea is, however, always a feature. Cases will occur in a wide variety of age ranges even in unweaned piglets. The diarrhoea is normally creamy. Dysentery is rarely seen but some necrotic sloughing of the mucosa may occur. Some clinicians maintain that pigs suffering from this less acute salmonellosis have a distinct smell but this has not been the auth `source_id=SRC-0088; page=74; line=2032`
- `VTOP-TX-0102` treatment_candidate / p.74 / Salmonellosis: Sick animals can be treated with many types of antibiotic injections on a daily basis. This can be followed up with water medication. However every effort should be made to grow the specific salmonella and test for resistance. Then the correct antibiotic can be given in adequate doses to avoid the build-up of antibiotic-resistant bacteria. Practitioners in the UK should remember that nitrofurazone, furazolidone and c `source_id=SRC-0088; page=74; line=2040`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-049-salmonellosis.md`
- Byte size moved: 1387
- Fact-like rows moved: 3
- Candidate fact mentions moved: 1
- Dose/route/course fact markers moved: 0
- Source anchors moved: 3

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 3 linked disease-control/treatment facts.
- Source pages: 49, 78, 119.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0363` candidate_fact / p.49 / 氟喹诺酮类药物: （1）适应证 本品适用于敏感细菌及支原体所致的呼吸道、尿道、消化道等各种感染性疾病。主要用于仔猪黄白痢、猪气喘病、仔猪副伤寒、猪丹毒等。 `source_id=SRC-0089; page=49; line=2090`
- `SFDUT1-TX-0372` treatment_or_prevention / p.78 / 氟喹诺酮类药物: （1）适应证 本品适用于治疗敏感细菌及支原体所致的各种感染性疾病，如仔猪黄白痢、仔猪副伤寒等，对不明原因引起的久泻不止疗效显著。 `source_id=SRC-0089; page=78; line=2116`
- `SFDUT1-TX-0527` vaccination_or_immunization / p.119 / 猪疫苗免疫接种应注意的细节: （2）常用的细菌活菌苗 多杀性巴氏杆菌病活疫苗，败血性链球菌病活疫苗，仔猪副伤寒活疫苗，肺炎支原体病活疫苗，仔猪大肠杆菌K88、K99双价基因工程活疫苗，猪布鲁杆菌病活菌苗等。 `source_id=SRC-0089; page=119; line=2691`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-049-salmonellosis.md`
- Byte size moved: 4528
- Fact-like rows moved: 9
- Candidate fact mentions moved: 4
- Dose/route/course fact markers moved: 0
- Source anchors moved: 9

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 增强证据 (SRC-0090, V13.1 batch)

- Batch status: 9 linked disease-control/treatment facts.
- Source pages: 237, 238, 239, 240.
- Matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_200_363_fact_index.csv`.

- `SFDUT2-TX-0146` candidate_fact / p.237 / 仔猪副伤寒（猪沙门菌病）: （1）易感性 本病主要引起 $1 \sim 2$ 月龄（ $10 \sim 15$ 千克体重）小猪发病，常呈散发，有时呈地方流行，在不良因素作用下，发病猪增多。 `source_id=SRC-0090; page=237; line=705`
- `SFDUT2-TX-0147` candidate_fact / p.238 / 仔猪副伤寒（猪沙门菌病）: (2) 传染源及传染途径 病猪及某些健康带菌猪是主要的传染来源。病菌存在于肠道中, 通过粪便排泄到外界环境中, 污染饲料、饮水、猪圈、食槽及周围环境, 通过消化道感染健康猪。其暴发主要通过介质以及饲养人员的传播, 从一个猪栏传播到另一个猪 `source_id=SRC-0090; page=238; line=706`
- `SFDUT2-TX-0148` candidate_fact / p.238 / 仔猪副伤寒（猪沙门菌病）: （2）内毒素 败血性沙门菌病的全身症状和病变，是因为沙门菌细胞壁中内毒素（脂多糖）也是一种毒力因素，作用于白细胞而引发炎症、高烧、黏膜出血、败血症等，最后因休克死亡。 `source_id=SRC-0090; page=238; line=718`
- `SFDUT2-TX-0149` vaccination_or_immunization / p.239 / 仔猪副伤寒（猪沙门菌病）: 酶联免疫吸附试验（ELISA）。 `source_id=SRC-0090; page=239; line=728`
- `SFDUT2-TX-0150` treatment_or_prevention / p.239 / 仔猪副伤寒（猪沙门菌病）: ① 临床症状 病猪食欲丧失、嗜睡，体温升高至 $40.5 \sim 41.6^{\circ} \mathrm{C}$ ，怕冷、扎堆，可能伴有湿性咳嗽及轻微呼吸困难、黄疸。发病的最初症状可见猪只不爱活动，此时病猪衰弱、弓背弯腰、行走不稳或蜷缩于猪栏的拐角内，甚至死亡。耳部、鼻端、颈部、四肢末端及腹部发绀，出现弥漫性紫红色。一般不见有腹泻发生，直到发病后三四天才出现水样、浅黄色粪便或稀粪。此病暴发时，死亡率很高；发病率不同，但一般在 $10\%$ 以下。此病的暴发往往与应激因素有关。每次流行时，猪的病程以及每次发病时间及严重程度是无法预测的，如不进行有效的治疗，病程会变长。疾病传播可通过摄食了污染的粪便和鼻咽分泌物，潜伏期为2天至数周。幸存下来的猪可继续带菌，粪便排菌至少达12周。 `source_id=SRC-0090; page=239; line=732`
- `SFDUT2-TX-0151` treatment_or_prevention / p.240 / 仔猪副伤寒（猪沙门菌病）: (1) 个体治疗 注射抗菌药物, 如硫酸阿米卡星、庆大霉素、卡那霉素、氟喹诺酮类药物、复方新诺明、复方磺胺嘧啶钠注射液等。对病重猪可注射地塞米松, 以降低内毒素的作用; 也可灌服氟哌酸。 `source_id=SRC-0090; page=240; line=754`
- `SFDUT2-TX-0152` candidate_fact / p.240 / 仔猪副伤寒（猪沙门菌病）: （2）群体混饲给药可在饲料中添加新霉素、安普霉素或含有TMP的磺胺甲基异噁唑或磺胺嘧啶。 `source_id=SRC-0090; page=240; line=755`
- `SFDUT2-TX-0153` vaccination_or_immunization / p.240 / 仔猪副伤寒（猪沙门菌病）: 认真执行预防为主的办法，改善饲养管理和卫生条件，避免和消除引起发病的多种应激因素，增强仔猪抵抗力。在本病常发地区，可对1月龄以上哺乳或断奶仔猪，用仔猪副伤寒冻干弱毒活疫苗（中牧生物）预防，用 $20\%$ 氢氧化铝生理盐水稀释，肌内注射1毫升，免疫期为9个月。口服时，按瓶签说明，服前用冷开水稀释成每头份 $5\sim 10$ 毫升，掺入少量新鲜冷饲料中，让猪自行采食。或将每1头份疫苗稀释于 $5\sim 10$ 毫升冷开水中给猪灌服。注意阅读疫苗使用说明书。 `source_id=SRC-0090; page=240; line=759`
- `SFDUT2-TX-0154` treatment_or_prevention / p.240 / 仔猪副伤寒（猪沙门菌病）: 发病后的措施：①隔离病猪，及时治疗；②圈舍彻底清扫、消毒，特别是饲槽要刷洗干净，粪便堆积发酵后利用；③病死猪应深埋，决不能食用，防止人发生食物中毒事故。 `source_id=SRC-0090; page=240; line=761`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/diseases/DIS-049-salmonellosis.md`
- Byte size moved: 605
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用证据增强 / SRC-0091

- 关联场景：沙门氏菌病。
- 药物/类别候选：氨苄西林, 磺胺嘧啶, 氟苯尼考。
- 生成边界：应强调药敏、耐药和公共卫生边界，避免经验性滥用抗菌药。
- 本块用于候选召回、鉴别增强和 rule 约束；不得单独输出剂量、疗程、休药期或 MRL。
- 来源：兽药合理应用与联用手册（1-200页），相关药物目录与正文页码见 `exports/veterinary_rational_use_1_200_drug_index.csv`。`source_id=SRC-0091`
<!-- RAU_1_200_V14_END -->

## RAU_201_400_V14

- Original marker: `RAU_201_400_V14_START` / `RAU_201_400_V14_END`
- Original runtime page: `wiki/diseases/DIS-049-salmonellosis.md`
- Byte size moved: 568
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_201_400_V14_START -->
## 兽药合理应用与联用证据增强（201-400页）/ SRC-0092

- 关联场景：沙门氏菌/公共卫生腹泻。
- 药物/类别候选：补液, NSAID 对症, 抗菌药候选。
- 生成边界：需保留人兽共患和食品安全边界。
- 用途：症状入口、候选召回、鉴别诊断、对症支持和 drug-rule 约束。
- 不得单独输出剂量、疗程、休药期、MRL 或出栏可食用承诺。
- 来源：兽药合理应用与联用手册（201-400页）。`source_id=SRC-0092`
<!-- RAU_201_400_V14_END -->

## RAU_401_600_V14

- Original marker: `RAU_401_600_V14_START` / `RAU_401_600_V14_END`
- Original runtime page: `wiki/diseases/DIS-049-salmonellosis.md`
- Byte size moved: 592
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 0

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）症候支持边界 / SRC-0093

- 下痢/败血症鉴别：止泻支持不能替代沙门菌公共卫生、采样和抗菌药边界。
- 证据用途：中药联用、禁忌、用药注意、症候支持和鉴别增强；不是病原确诊、报告处置、抗菌药剂量、休药期、MRL 或食品安全承诺来源。
- 索引：`exports/veterinary_rational_use_401_600_fact_index.csv`；矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`。
<!-- RAU_401_600_V14_END -->
