---
page_id: DRUG-034-sulfonamides
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase3_drug_evidence_expansion
moved_from: wiki/drugs/DRUG-034-sulfonamides.md
generated: 2026-05-09T11:42:41+08:00
---

# DRUG-034-sulfonamides Evidence Expansion

This file stores detailed batch evidence moved out of the runtime drug page during Phase 3 cleanup.

Runtime rule:

- Do not load this file for default production/evaluation retrieval.
- Load it only for evidence expansion, audit, source lookup, or manual review.
- Dose, route, course, withdrawal period, MRL, residue, and food-safety claims still require current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-034-sulfonamides.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 20

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 24 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 磺胺.
- Source pages: 14, 17, 20, 22, 29, 34, 35, 37, 38, 42, 44, 48, 72, 73, 93, 139, 150, 160, 161.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0007` 流行性乙型脑炎 / 处方1 `source_id=SRC-0087; page=14; line=676-704`
- `HANDBOOK-RX-0018` 猪繁殖与呼吸综合征 / 处方2 `source_id=SRC-0087; page=20; line=901-917`
- `HANDBOOK-RX-0019` 猪流行性腹泻 / 处方1 `source_id=SRC-0087; page=22; line=970-984`
- `HANDBOOK-RX-0023` 仔猪黄痢 / 处方1 `source_id=SRC-0087; page=29; line=1128-1148`
- `HANDBOOK-RX-0031` 仔猪白痢 / 处方2 `source_id=SRC-0087; page=29; line=1210-1230`
- `HANDBOOK-RX-0034` 猪水肿病 / 处方2 `source_id=SRC-0087; page=29; line=1324-1360`
- `HANDBOOK-RX-0037` 副猪嗜血杆菌病或猪多发性浆膜炎与关节炎 / 处方2 `source_id=SRC-0087; page=34; line=1418-1426`
- `HANDBOOK-RX-0040` 仔猪副伤寒或猪沙门菌病 / 处方3 `source_id=SRC-0087; page=35; line=1468-1480`
- `HANDBOOK-RX-0046` 猪传染性萎缩性鼻炎 / 处方1 `source_id=SRC-0087; page=37; line=1568-1580`
- `HANDBOOK-RX-0047` 猪传染性胸膜肺炎 / 处方1 `source_id=SRC-0087; page=38; line=1612-1628`
- `HANDBOOK-RX-0054` 猪肺疫 / 处方1 `source_id=SRC-0087; page=42; line=1748-1758`
- `HANDBOOK-RX-0062` 猪链球菌病 / 处方3 `source_id=SRC-0087; page=44; line=1849-1855`
- `HANDBOOK-RX-0064` 仔猪梭菌性肠炎 / 处方1 `source_id=SRC-0087; page=48; line=1932-1946`
- `HANDBOOK-RX-0149` 弓形虫病 / 处方1 `source_id=SRC-0087; page=72; line=3007-3011`
- `HANDBOOK-RX-0150` 弓形虫病 / 处方2 `source_id=SRC-0087; page=72; line=3013-3023`
- `HANDBOOK-RX-0151` 7克 / 处方3 `source_id=SRC-0087; page=72; line=3025-3029`
- `HANDBOOK-RX-0154` 球虫病 / 处方2 `source_id=SRC-0087; page=73; line=3064-3068`
- `HANDBOOK-RX-0194` 胃肠炎 / 处方1 `source_id=SRC-0087; page=17; line=3554-3590`
- `HANDBOOK-RX-0226` 脑膜脑炎 / 处方1 `source_id=SRC-0087; page=93; line=4015-4019`
- `HANDBOOK-RX-0327` 创伤 / 处方2 `source_id=SRC-0087; page=139; line=5885-5891`
- Additional rows omitted here: 4; see `exports/handbook_prescription_drug_mention_index.csv`.
<!-- HANDBOOK_RX_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-034-sulfonamides.md`
- Candidate facts: 7
- Dose/route/course facts: 11
- Source anchors: 35

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 46 linked drug-use facts.
- Source pages: 3, 13, 14, 19, 22, 31, 45, 55, 61, 73, 74, 75, 78, 79, 82, 86, 120, 151, 152, 172, 188.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0004` candidate_fact / p.3 / 兽药分类: （1）磺胺类药 磺胺嘧啶（SD）、磺胺二甲嘧啶（SM2）、磺胺甲基异噁唑（新诺明、SMZ）、磺胺-5-甲氧嘧啶（磺胺对甲氧嘧啶、SMD）、磺胺-6-甲氧嘧啶（磺胺间甲嘧啶、SMM）、磺胺脒(S克)。 `source_id=SRC-0089; page=3; line=314`
- `SFDUT1-TX-0006` candidate_fact / p.3 / 兽药分类: （2）抗球虫药托曲珠利、地克珠利、甲苯三嗪酮（百球清）、磺胺二甲嘧啶、磺胺氯吡嗪钠。 `source_id=SRC-0089; page=3; line=338`
- `SFDUT1-TX-0027` compliance_or_safety / p.13 / 兽药使用必须遵循的基本原则: 功倍的效果。在此特别提醒要注意药物之间的配伍禁忌。酸性药物与碱性药物合用会使药效降低或丧失，口服活菌制剂时应禁用抗菌药物和吸附剂，磺胺类药物与维生素C合用会产生沉淀，等等。避免使用多种药物或固定剂量的联合用药，因为多种药物治疗极大地增加药物相互作用的概率，也给患畜增加了危险；要慎重使用固定剂量的联合用药，因为它使兽医师失去了根据动物病情变化去调整药物剂量的机会，达不到最佳的用药效果。 `source_id=SRC-0089; page=13; line=584`
- `SFDUT1-TX-0028` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （1） $\beta-$ 内酰胺类 $\beta-$ 内酰胺类（青霉素类、头孢菌素类）与 $\beta-$ 内酰胺酶抑制剂如克拉维酸、舒巴坦钠合用有较好的保护和协同增效作用，青霉素类与氨基糖苷类呈协同作用，但剂量应基本平衡。青霉素类不能与四环素类、氯霉素类、大环内酯类、磺胺类等抗菌药合用。但例外的是治疗脑膜炎时，因青霉素不易透过血脑屏障而采用青霉素与磺胺嘧啶合用，但要分开注射，否则会发生理化性配伍禁忌。青霉素与维生素C、碳酸氢钠等也不能同时使用。头孢菌素类不宜与氨基糖苷类合用，因都有肾毒性。 `source_id=SRC-0089; page=13; line=588`
- `SFDUT1-TX-0029` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （2）氨基糖苷类 氨基糖苷类与 $\beta$ -内酰胺类配伍应用有较好的协同作用。甲氧苄氨嘧啶（TMP）可增强本品的作用。氨基糖苷类可与多黏菌素类合用，但不可与氯霉素类合用。氨基糖苷类药物之间不可联合应用以免增强毒性，与碱性药物联合应用其抗菌效能可能增强，但毒性也会增大。链霉素与四环素合用，能增强对布氏杆菌的治疗作用。链霉素与红霉素合用，对猪链球菌病有较好的疗效。庆大霉素（或卡那霉素）可与喹诺酮药物合用。链霉素与磺胺类药物配伍应用会发生水解失效。硫酸新霉素一般口服给药，与阿托品类药物应用于仔猪腹泻。 `source_id=SRC-0089; page=13; line=589`
- `SFDUT1-TX-0031` treatment_or_prevention / p.13 / 兽药使用必须遵循的基本原则: （4）大环内酯类 大环内酯类与磺胺二甲嘧啶、磺胺嘧啶、磺胺间甲氧嘧啶、TMP的复方可用于治疗呼吸道病。泰乐菌素可与磺胺类合用。红霉素不宜与 $\beta$ -内酰胺类、林可霉素、氯霉素类、 `source_id=SRC-0089; page=13; line=591`
- `SFDUT1-TX-0033` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （9）喹诺酮类 喹诺酮类与杀菌药（青霉素类、氨基糖苷类）及TMP在治疗特定细菌感染方面有协同作用。喹诺酮类药物+林可霉素可用于治疗支原体合并大肠杆菌感染引起的呼吸道和肠道感染。喹诺酮类药物与氯霉素类、大环内酯类（如红霉素）合用有拮抗作用。喹诺酮类药物可与磺胺类药物配伍应用，合用对大肠杆菌和金黄色葡萄球菌有相加作用。喹诺酮类慎与氨茶碱合用。 `source_id=SRC-0089; page=13; line=599`
- `SFDUT1-TX-0034` treatment_or_prevention / p.14 / 兽药使用必须遵循的基本原则: 内服能吸收的药物，可以用于全身感染类疾病。内服不能吸收的药物，如磺胺脒等，只能用于胃肠道细菌感染。一般的抗菌药物很少能进入脑脊液，只有磺胺嘧啶钠可以进入，因此，治疗脑部感染，如猪链球菌性脑炎，应首选磺胺嘧啶钠。 `source_id=SRC-0089; page=14; line=605`
- `SFDUT1-TX-0057` treatment_or_prevention / p.19 / 治疗猪病要选择最适宜的给药方法: 消化道感染应以口服为主。大多数能在胃肠道吸收的药物也可采用口服给药。口服给药的优点是操作方便、安全，缺点是起效慢，剂量较大。此外，胃肠道不易吸收的磺胺脒、新霉素、庆大霉素、吡哌酸、黏杆菌素等也可口服，利用在肠道形成较高浓度的特点，治疗细菌性肠炎、仔猪黄白痢等。若治疗全身性感染疾病，如副猪嗜血杆菌病等以及危急病例，不宜口服而应注射。 `source_id=SRC-0089; page=19; line=713`
- `SFDUT1-TX-0070` treatment_or_prevention / p.22 / 要提前预见药物的疗效和不良反应: 例如，磺胺类药物有其独特的优点：抗菌谱广、价格较低、使用方便等，对大多数革兰阳性菌和部分革兰阴性菌都有效，对衣原体和某些原虫也有效，主要用于各种病菌所致的呼吸道、消化道、泌尿生殖道等全身感染，如猪巴氏杆菌、链球菌病、仔猪水肿病、弓形体病、乳腺炎、子宫炎、败血症、坏死杆菌病、萎缩性鼻炎等，在控制猪感染性疾病中发挥了很大作用，尤其是抗菌增效剂和一些新型磺胺药出现后，有了新的广阔前景，是最常用的防治猪病的药物。首次使用时剂量必须加倍，并要有足够的剂量和疗程，一般应连用 $5 \sim 6$ 天。但同时也有不良反应及毒副作用较多、细菌易产生耐药性、用量大等缺点。在临床上应用必须正确、合理，否则会出现诸多弊端。急性中毒多发生于静脉注射其钠盐时速度过快或剂量过大，主要表现为共济失调、肌无力、呕吐、昏迷、厌食和腹泻等。慢性中毒主要由剂量偏大、用药时间过长而引起，主要表现为精神沉郁、食欲减退或废绝、泌尿系统损伤，出现结晶尿、血尿 `source_id=SRC-0089; page=22; line=762`
- `SFDUT1-TX-0071` vaccination_or_immunization / p.22 / 要提前预见药物的疗效和不良反应: 和蛋白尿、尿少或无尿、体温升高等；抑制胃肠道菌丛，导致消化系统障碍；造血机能破坏，出现溶血性贫血、凝血时间延长和毛细血管渗血；仔猪免疫系统抑制、免疫器官出血及萎缩；增重减慢、毛长无光泽、光吃不长等。在发挥药物治疗作用的同时，应该采取措施减少或预防副作用的发生，如配合等量碳酸氢钠，并增加饮水量。副作用严重时，除及时停药外，还应立即内服或静注碳酸氢钠，以促进磺胺类药的排出，同时进行对症治疗。 `source_id=SRC-0089; page=22; line=764`
- `SFDUT1-TX-0105` drug_interaction / p.31 / 肆霉素类: ④ 本品还与下列药物有配伍禁忌：氨基糖苷类、林可霉素、氟苯尼考、泰妙菌素、土霉素、四环素、金霉素、多黏菌素、红霉素、氯丙嗪、碳酸氢钠、葡萄糖酸钙、氯化钙、肾上腺类、B族维生素、维生素C、磺胺类药物。 `source_id=SRC-0089; page=31; line=916`
- `SFDUT1-TX-0231` treatment_or_prevention / p.45 / 大环内酯类: ④ 磷酸泰乐菌素、磺胺二甲嘧啶预混剂，以泰乐菌素计，混饲，每吨饲料100克，连用 $5 \sim 7$ 天。主要用于防治支原体及敏感 $\mathbf{G}^{+}$ 菌感染，也用于预防猪痢疾。 `source_id=SRC-0089; page=45; line=1468`
- `SFDUT1-TX-0256` candidate_fact / p.61 / 氟苯尼考: （3）本品不能与磺胺嘧啶钠混合肌注。口服或肌注给药时忌与碱性药物合用，以免分解失效。也不宜与盐酸四环素、卡那霉素、庆大霉素、三磷酸腺苷、辅酶A等混合注射，以免发生沉淀和降效。 `source_id=SRC-0089; page=61; line=1558`
- `SFDUT1-TX-0269` dose_route_course / p.55 / 林可霉素: （2）用法与用量 肌注：一次量，每千克体重10毫克，2次/天，连用 $3\sim 5$ 天。注意：不能与磺胺嘧啶钠混合注射；亦不宜与氟苯尼考、大环内酯类、泰妙菌素、氟喹诺酮类抗菌药物联用，呈拮抗作用。 `source_id=SRC-0089; page=55; line=1630`
- `SFDUT1-TX-0312` treatment_or_prevention / p.73 / 磺胺类药物及抗菌增效剂: 磺胺类药物（SAs）是指具有对氨基苯磺酰胺结构的一类用于预防和治疗全身各系统细菌感染的化学合成药物的总称。磺胺类药物作为应用最早的（1935年合成百浪多息）一类人工合成的抗菌药物，有其独特的优点：抗菌谱广、疗效确实、性质稳定、不易变质、使用方便、能大量生产、价格相对低廉。但同时也有抗菌作用较弱、不良反应较多、细菌易产生耐药性、用量大、疗程偏长等缺陷。在发现了甲氧苄啶（TMP）和二甲氧苄啶（DVD）等抗菌增效剂后，把磺胺药和抗菌增效剂联合使用，使抗菌活性和疗效大大增强，甚至从抑菌剂变为杀菌剂，因此，磺胺类药至今仍为猪抗感染治疗中的重要药物之一，在临床上仍广泛应用。除用于治疗的针剂外，主要通过拌料或饮水做脉冲式药物保健。保健时往往配伍使用强力霉素等四环素类药物、枝原净（泰妙菌素）、泰乐菌素或氟苯尼考等。 `source_id=SRC-0089; page=73; line=1843`
- `SFDUT1-TX-0313` candidate_fact / p.73 / 磺胺类药物及抗菌增效剂: 旋体、立克次体、病毒等完全无效。不同的磺胺药抗菌作用强度不同，口服易吸收者，其抗菌作用强度的顺序依次为磺胺间甲氧嘧啶(SMM) $>$ 磺胺氯达嗪钠（SCP） $>$ 磺胺甲噁唑（SMZ） $>$ 磺胺异噁唑（SIZ） $>$ 磺胺嘧啶（SD） $>$ 磺胺二甲嘧啶（ $\mathrm{SM}_2$ ） $>$ 磺胺对甲氧嘧啶（SMD） $>$ 磺胺邻二甲氧嘧啶（SDM，又名磺胺多辛、周效磺胺）。 `source_id=SRC-0089; page=73; line=1851`
- `SFDUT1-TX-0314` treatment_or_prevention / p.74 / 磺胺类药物及抗菌增效剂: 可分为口服肠道易吸收、口服肠道不易吸收及局部外用三类。口服肠道易吸收者用于治疗全身各系统感染；口服肠道不易吸收者仅作为肠道感染的治疗，如磺胺脒（SG）、酞磺噻唑（PST）；局部外用磺胺药作为皮肤黏膜感染的外用药物，如磺胺嘧啶银（烧伤宁，SD-Ag）等。 `source_id=SRC-0089; page=74; line=1859`
- `SFDUT1-TX-0316` treatment_or_prevention / p.75 / 磺胺类药物及抗菌增效剂: （1）合理选药 全身性感染宜选肠道易吸收、作用强而副作用较小的药物，如磺胺间甲氧嘧啶（SMM）、磺胺氯达嗪钠（SCP）、磺胺甲噁唑（SMZ）、磺胺异噁唑（SIZ）、磺胺嘧啶（SD）、磺胺二甲嘧啶（ $\mathrm{SM}_2$ ）、磺胺对甲氧嘧啶（SMD）、磺胺噻唑（ST）、磺胺喹噁啉（SQ）等；肠道感染可选内服肠道不易吸收的药物，如磺胺脒（磺胺胍、SG）、琥磺噻唑（SST）、酞磺噻唑（PST）等；治疗创伤时可选用氨苯磺胺（SN）、磺胺嘧啶银（SD-Ag）等；尿道感染可选用对尿道损伤小、尿中浓度高的SMZ、SIZ等。 `source_id=SRC-0089; page=75; line=1877`
- `SFDUT1-TX-0318` candidate_fact / p.75 / 磺胺类药物及抗菌增效剂: （1）严格掌握适应证，对病毒性疾病及发热病因不明时不宜用磺胺药。 `source_id=SRC-0089; page=75; line=1883`
- `SFDUT1-TX-0320` candidate_fact / p.75 / 磺胺类药物及抗菌增效剂: （5）磺胺类药在体内的代谢产物乙酰磺胺的溶解度低，易在泌尿道中析出结晶，故用药期间应充分饮水，增加尿量，以促进排出。 `source_id=SRC-0089; page=75; line=1888`
- `SFDUT1-TX-0321` compliance_or_safety / p.75 / 磺胺类药物及抗菌增效剂: （6）肾功能受损时，磺胺药排泄缓慢，应慎用。 `source_id=SRC-0089; page=75; line=1889`
- `SFDUT1-TX-0322` treatment_or_prevention / p.75 / 磺胺类药物及抗菌增效剂: （10）治疗创伤时，须将创口中的坏死组织和脓汁消除干净，以免因其含有大量PABP而影响磺胺药的疗效。 `source_id=SRC-0089; page=75; line=1893`
- `SFDUT1-TX-0324` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: ① 磺胺嘧啶片。用于敏感菌引起的感染，亦可用于猪弓形虫病。内服，一次量，每千克体重，首次 $0.14 \sim 0.2$ 克，维持量 $0.07 \sim 0.1$ 克，2次/天，连用 $3 \sim 5$ 天。 `source_id=SRC-0089; page=78; line=1936`
- `SFDUT1-TX-0325` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: ② 复方磺胺嘧啶预混剂，规格：1000克：磺胺嘧啶125克与甲氧嘧啶25克，用于猪的链球菌、葡萄球菌、巴氏杆菌、大肠杆菌、沙门菌和李氏杆菌等感染。以磺胺嘧啶计。混饲，一日量，每千克体重 $15\sim 30$ 毫克，连用5天。 `source_id=SRC-0089; page=78; line=1937`
- `SFDUT1-TX-0326` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: ③ 磺胺嘧啶钠注射液，规格： $10\%$ 、 $20\%$ ，用于敏感菌引起的感染（为脑膜炎的首选药物）及猪弓形虫病。深部肌注、静脉注射，一次量，每千克体重50毫克，2次/天，连用 $2 \sim 3$ 天。注意：本品遇酸可析出结晶，故不宜用 $5\%$ 葡萄糖液稀释；本品不可与四环素、卡那霉素、阿米卡星、林可霉素等配合使用。 `source_id=SRC-0089; page=78; line=1938`
- `SFDUT1-TX-0327` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: ④ $10\%$ 复方磺胺嘧啶钠注射液，规格：10毫升：磺胺嘧啶钠1克和甲氧苄啶0.2克，用于敏感菌及猪弓形虫感染，以磺胺嘧啶计，肌注，一次量，每千克体重 $20\sim 30$ 毫克， $1\sim 2$ 次/天，连用 $2\sim 3$ 天。注意：同③。 `source_id=SRC-0089; page=78; line=1939`
- `SFDUT1-TX-0329` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: ① 磺胺间甲氧嘧啶钠注射液，用于各种敏感菌所引起的呼吸道、消化道、泌尿道感染及球虫病、猪弓形虫病等。静注，一次量，每千克体重50毫克， $1\sim 2$ 次/天，连用 $2\sim 3$ 天。 `source_id=SRC-0089; page=78; line=1946`
- `SFDUT1-TX-0330` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: ② 磺胺间甲氧嘧啶粉（片），内服，一次量，每千克体重，首次量 $50 \sim 100$ 毫克，维持量 $25 \sim 50$ 毫克，一天2次，连用 $3 \sim 5$ 天。 `source_id=SRC-0089; page=78; line=1947`
- `SFDUT1-TX-0331` candidate_fact / p.78 / 磺胺类药物及抗菌增效剂: （1）作用与用途、药物相互作用 同磺胺间甲氧嘧啶。 `source_id=SRC-0089; page=78; line=1951`
- `SFDUT1-TX-0332` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: 敏感菌感染等。以磺胺氯达嗪钠计，内服，一次量，每千克体重 $20\sim 30$ 毫克，连用 $5\sim 10$ 天。 `source_id=SRC-0089; page=78; line=1956`
- `SFDUT1-TX-0333` drug_interaction / p.78 / 磺胺类药物及抗菌增效剂: ② $62.5\%$ 复方磺胺氯达嗪钠粉能有效控制弓形体、萎缩性鼻炎、乳房炎、子宫炎及巴氏杆菌、链球菌、大肠杆菌、胸膜肺炎放线杆菌、沙门菌等感染。每吨饲料添加 $300 \sim 500$ 克“康舒秘”成品，或每吨水添加 $150 \sim 250$ 克“康舒秘”成品，每次连用7天。作为一种慢效抑菌剂，“康舒秘”与快效抑菌剂强力霉素联合具有协同作用，能更有效地控制敏感菌感染。如能使用枝原净十强力霉素十康舒秘的黄金三宝组合，还能有效控制肺炎支原体等感染引起的呼吸道病综合征（PRDC）。因肺炎支原体是引起PRDC的钥匙病原和导火线，控制好支原体也可减轻蓝耳病对机体的损伤。 `source_id=SRC-0089; page=78; line=1958`
- `SFDUT1-TX-0335` dose_route_course / p.79 / 磺胺类药物及抗菌增效剂: ① 磺胺二甲嘧啶粉（片），内服，一次量，每千克体重，首次量 $0.14 \sim 0.2$ 克，维持量 $0.07 \sim 0.1$ 克， $1 \sim 2$ 次/天，连用 $3 \sim 5$ 天。 `source_id=SRC-0089; page=79; line=1966`
- `SFDUT1-TX-0336` dose_route_course / p.79 / 磺胺类药物及抗菌增效剂: ② $10\%$ 磺胺二甲嘧啶钠注射液，静注、肌注，一次量，每千克体重 $50 \sim 100$ 毫克， $1 \sim 2$ 次/天，连用 $2 \sim 3$ 天。 `source_id=SRC-0089; page=79; line=1967`
- `SFDUT1-TX-0337` dose_route_course / p.79 / 磺胺类药物及抗菌增效剂: （2）制剂 磺胺噻唑钠注射液，静注，一次量，每千克体重 $50\sim 100$ 毫克，2次/天，连用 $2\sim 3$ 天。 `source_id=SRC-0089; page=79; line=1972`
- Additional linked rows omitted here: 11; see exported index.
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-034-sulfonamides.md`
- Candidate facts: 8
- Dose/route/course facts: 5
- Source anchors: 23

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 23 linked drug-use facts.
- Source pages: 194, 199, 201, 209, 216, 222, 226, 240, 252, 256, 263, 269, 273, 304, 306, 307.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0017` treatment_or_prevention / p.194 / 猪支原体肺炎: 因猪肺炎支原体没有细胞壁，因此通过干扰细胞壁合成发挥抗菌作用的青霉素、氨苄西林、阿莫西林和头孢菌素对单纯的支原体肺炎治疗无效，其他抗菌药物如甲氧氨苄和磺胺类药物、多黏菌素、链霉素、红霉素对猪支原体肺炎的治疗也不起作用。 `source_id=SRC-0090; page=194; line=65`
- `SFDUT2-TX-0036` candidate_fact / p.199 / 副猪嗜血杆菌病: （2）亚急性型或慢急性型 常由急性型转化而来或由中等毒力毒株引起，主要表现为多发性浆膜炎、关节炎、脑膜炎等。病猪食欲下降、精神沉郁、发抖、扎堆、咳嗽、呼吸困难、被毛粗乱、渐进性消瘦、体表皮肤苍白；行动迟缓僵硬，后肢不协调；四肢无力，不愿站立；关节肿大或跛行。副猪嗜血杆菌性脑膜炎的症状，除共济失调、步伐蹒跚、头向后仰、四肢呈游泳状以外，笔者还观察到一种特殊表现：喜欢向同一侧躺卧，将猪翻过来它又很快便自动翻回去，可反复数次（可用复方磺胺间甲氧嘧啶配合阿莫西林或氨苄西林分别肌注，效果较好）。慢急性型有的可拖10多天后终因衰竭而死。侥幸不死的极度消瘦或生长缓慢。 `source_id=SRC-0090; page=199; line=137`
- `SFDUT2-TX-0049` candidate_fact / p.201 / 副猪嗜血杆菌病: ⑥ 复方磺胺间甲氧嘧啶，首次量0.1克/千克体重，维持量0.05克/千克体重，2次/天，连用 $4\sim 5$ 天。 `source_id=SRC-0090; page=201; line=176`
- `SFDUT2-TX-0066` candidate_fact / p.209 / 猪链球菌病: ② 选择最有效的抗菌药物时必须考虑细菌的敏感性、感染类型。如脑膜炎型要首选磺胺嘧啶钠，再联合使用其他抗菌药物，如青霉素类、头孢霉素等，有条件的要做药敏试验，确定首选药物。 `source_id=SRC-0090; page=209; line=287`
- `SFDUT2-TX-0084` candidate_fact / p.216 / 猪传染性胸膜肺炎: （1）推荐注射用药方案 应选择对革兰阴性菌敏感的药物。首选药物是头孢噻呋（或头孢噻肟）和氟苯尼考。强力霉素、庆大霉素配合阿莫西林、恩诺沙星、磺胺六甲氧、泰妙菌素、阿奇霉素等可酌情选用。 `source_id=SRC-0090; page=216; line=379`
- `SFDUT2-TX-0107` treatment_or_prevention / p.222 / 猪传染性萎缩性鼻炎: ① 母猪和仔猪 为了减少母猪的感染及传播，可在母猪产仔前在饲料中添加药物以达到治疗的目的。可用磺胺二甲基嘧啶或强力霉素拌在饲料中。哺乳仔猪在 $3 \sim 4$ 周龄注射较大剂量的抗菌剂进行治疗。最有效的有增效磺胺、土霉素、青霉素及链霉素。如果仔猪主要由支气管波氏杆菌感染，则磺胺是首选药物。在 $3 \sim 4$ 周龄时，最好每周给 $1 \sim 2$ 次长效药物，如果细菌没有产生耐药性，长效药物应对治疗巴氏杆菌病很有效。试验证明，长效土霉素能降低鼻腔感染的患病率和由多杀性巴氏杆菌引起鼻甲骨萎缩程度。也可使用强力霉素。 `source_id=SRC-0090; page=222; line=464`
- `SFDUT2-TX-0109` treatment_or_prevention / p.222 / 猪传染性萎缩性鼻炎: 磺胺类药物是第一个成功用于控制本病的药物，到目前，此药仍在单用或与其他抗生素以及磺胺增效剂合用。许多猪支气管败血性波氏杆菌的分离物对四环素敏感，这些药物特别是土霉素的长效制剂，对仔猪注射给药，可用于控制本病。新的氟喹诺酮类药物也对猪支气管败血波氏杆菌有效。大多数的抗菌药物可单用也可联合使用，它们既能有效治疗PAR又有助于生长。 `source_id=SRC-0090; page=222; line=468`
- `SFDUT2-TX-0110` dose_route_course / p.222 / 猪传染性萎缩性鼻炎: ③ 个体治疗 肌注，一次量：a. 磺胺类药物配合磺胺增效剂的复方制剂，如复方增效磺胺或复方磺胺嘧啶钠注射液，12.5毫克/千克体重；b. 长效土霉素注射液，20毫克/千克体重；c. 青霉素（4万单位/千克体重）配合卡那霉素（ $20\sim 30$ 毫克/千克体重）或氨苄西林（ $10\sim 20$ 毫克/千克体重）或阿莫西林（ $10\sim 20$ 毫克/千克体重）；d. 氟喹诺酮类注射液， $2.5\sim 5$ 毫克/千克体重；e. 头孢噻呋钠， $5\sim 10$ 毫克/千克体重；f. 仔猪打喷嚏时也可用卡那霉素注射液滴鼻，每天1次，每个鼻孔滴0.5毫升，连用 $2\sim 3$ 天。 `source_id=SRC-0090; page=222; line=470`
- `SFDUT2-TX-0111` candidate_fact / p.222 / 猪传染性萎缩性鼻炎: ④ 混饲给药 每吨饲料中可添加：a. 泰乐菌素 100 克 + 磺胺二甲基嘧啶 100 克；b. 强力霉素 150 克；c. 拜尔“利好”20% 复方磺胺间甲氧嘧啶，首次量 2000 克，维持量 1000 克，连用 7 天。 `source_id=SRC-0090; page=222; line=472`
- `SFDUT2-TX-0121` drug_interaction / p.226 / 猪大肠杆菌病: ④ 药物治疗 丁胺卡那霉素、头孢噻呋、恩诺沙星、吡哌酸、庆大霉素、新霉素、增效磺胺甲基异噁唑、安普霉素、痢菌净等均为敏感药物。但是，由于长期使用上述药物，大肠杆菌对其普遍产生较强的耐药性，有些菌株同时耐受多种药物。因此，为了提高药物治疗效果，应每隔一段时间（一年或半年）进行一次大肠杆菌药敏试验，掌握细菌药敏状态的变化，减少用药的盲目性。治疗时尽量联合用药，或 $2 \sim 3$ 个月轮换用药，既可提高疗效，又能减少耐药菌株的产生。 `source_id=SRC-0090; page=226; line=535`
- `SFDUT2-TX-0151` treatment_or_prevention / p.240 / 仔猪副伤寒（猪沙门菌病）: (1) 个体治疗 注射抗菌药物, 如硫酸阿米卡星、庆大霉素、卡那霉素、氟喹诺酮类药物、复方新诺明、复方磺胺嘧啶钠注射液等。对病重猪可注射地塞米松, 以降低内毒素的作用; 也可灌服氟哌酸。 `source_id=SRC-0090; page=240; line=754`
- `SFDUT2-TX-0152` candidate_fact / p.240 / 仔猪副伤寒（猪沙门菌病）: （2）群体混饲给药可在饲料中添加新霉素、安普霉素或含有TMP的磺胺甲基异噁唑或磺胺嘧啶。 `source_id=SRC-0090; page=240; line=755`
- `SFDUT2-TX-0196` dose_route_course / p.252 / 仔猪渗出性皮炎: ④ 复方磺胺对甲氧嘧啶钠注射液，肌内注射，一次量， $15\sim 20$ 毫克/千克体重， $1\sim 2$ 次/天。 `source_id=SRC-0090; page=252; line=947`
- `SFDUT2-TX-0203` treatment_or_prevention / p.256 / 猪衣原体病: （6）脑炎 各年龄段的猪有时出现神经症状，表现兴奋、尖叫，盲目冲撞或转圈运动，倒地后四肢呈现游泳状划动，不久死亡。青霉素配合磺胺嘧啶钠（不能混合，要分别肌注）和地塞米松治疗有效。 `source_id=SRC-0090; page=256; line=1012`
- `SFDUT2-TX-0215` treatment_or_prevention / p.263 / 8. 综合防治: （4）在常发地区和流行时节，对病猪群饲料中添加四环素类抗生素或砷制剂预防。如每吨饲料中添加 $15\%$ 金霉素预混剂2000克或回盛生物的“附红特乐”（有效成分盐酸多西环素及增效剂）1000克，或强力霉素可溶性粉150克（效价）+磺胺增效剂（TMP）20克，连用 $7\sim 10$ 天；也可每吨饲料中添加阿散酸180克，连用1周，以后改为90克，连用15天。 `source_id=SRC-0090; page=263; line=1136`
- `SFDUT2-TX-0232` dose_route_course / p.269 / 仔猪球虫病: 本病很难根治，而且用于防治的药物并不多。病猪口服“百球清”，每千克体重 $20\sim 30$ 毫克；或托曲珠利溶液（南京金盾“艾美青”），一次1毫升；或口服盐酸氨丙啉，每千克体重 $25\sim 40$ 毫升，每天1次，连用 $5\sim 6$ 天，有一定效果。也可试用口服甲氧苄啶/磺胺二甲嘧啶，每千克体重0.1克，每天1次，连用 $5\sim 7$ 天。 `source_id=SRC-0090; page=269; line=1227`
- `SFDUT2-TX-0234` candidate_fact / p.269 / 仔猪球虫病: （4）虽然母猪体内的球虫不是引起仔猪球虫病的主要原因，但也不能忽视。针对目前猪场存在多种寄生虫危害的实际情况，应选用能同时驱除猪体内外寄生虫的复方驱虫药物，有效地控制猪球虫和其他寄生虫对猪群的危害。猪场技术人员在选择驱虫药物时应考虑以下三个方面的问题：①单纯使用伊维菌素、阿维菌素对疥螨等寄生虫驱除效果较好，但对球虫无效，对猪体内移行期的蛔虫幼虫等效果也较差；②阿苯达唑、芬苯达唑等对蛔虫、鞭虫、结节虫等线虫及移行期的幼虫、虫卵都有较强的驱杀或抑制作用，但对猪球虫无效；③地克珠利、盐酸氨丙啉和一些磺胺类药物对球虫效果 `source_id=SRC-0090; page=269; line=1234`
- `SFDUT2-TX-0235` treatment_or_prevention / p.269 / 仔猪球虫病: （5）在仔猪球虫病发病严重的猪场，在仔猪 $3 \sim 6$ 日龄（5日龄最佳）时使用“百球清”或磺胺二甲氧嘧啶和泰乐菌素复方制剂溶液或 $5\%$ 的三嗪酮悬液，对小猪进行灌服，有一定预防效果。当怀疑仔猪发生球虫病时，用同样方法进行治疗，连用5天，患病仔猪应同时灌服口服补液盐，防止脱水死亡。 `source_id=SRC-0090; page=269; line=1238`
- `SFDUT2-TX-0239` dose_route_course / p.273 / 猪弓形虫病: （1）对全场的病猪使用磺胺-6-甲氧嘧啶，按50毫克/千克体重进行肌内注射，每天1次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=273; line=1286`
- `SFDUT2-TX-0240` dose_route_course / p.273 / 猪弓形虫病: （2）对全场未发病猪可选用拜耳“利好”（ $20\%$ 磺胺间甲氧嘧啶/TMP)，混饲治疗，每吨饲料加本品，首次量2000克，饲喂1天后，改为维持量1000克，再喂6天。也可选用磺胺甲基异噁唑(SMZ)，100毫克/千克体重，每天内服一次，连用 $5 \sim 7$ 天。 `source_id=SRC-0090; page=273; line=1287`
- `SFDUT2-TX-0320` vaccination_or_immunization / p.304 / 猪呼吸道病综合征: ⑤ 免疫抑制因素 已知有许多可致免疫抑制的病原体，尤以病毒为主，如PRRSV、PCV-2、SIV、CFSV等。此外，饲料中的霉菌毒素，某些药物，如长期使用地塞米松、磺胺类药、氟苯尼考、卡那霉素等。 `source_id=SRC-0090; page=304; line=1743`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
- `SFDUT2-TX-0341` candidate_fact / p.307 / 猪呼吸道病综合征: ⑤ 泰乐菌素（效价）100克+磺胺二甲嘧啶100克+磺胺增效剂20克。 `source_id=SRC-0090; page=307; line=1797`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-034-sulfonamides.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-081-DRUG-034-sulfonamides-md-9191` 磺胺类 / 磺胺类 / p.81：目录定位显示 `磺胺类` 属于 `磺胺类`，可作为药物召回、类别边界和联用禁忌复核入口。 `source_id=SRC-0091; page=81`
<!-- RAU_1_200_V14_END -->

## RAU_201_400_V14

- Original marker: `RAU_201_400_V14_START` / `RAU_201_400_V14_END`
- Original runtime page: `wiki/drugs/DRUG-034-sulfonamides.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 2

<!-- RAU_201_400_V14_START -->
## 兽药合理应用与联用手册（201-400页）增强 / SRC-0092

- 证据用途：系统用药、抗原虫/杀虫药、中药配伍、联用禁忌和对症支持边界。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺。

- `RAU2-DRUG-249-8022` 碳酸氢钠 / 酸碱平衡/磺胺安全边界 / p.249：`碳酸氢钠` 在本批来源中定位为 `酸碱平衡/磺胺安全边界`。 `source_id=SRC-0092; page=249`
- `RAU2-DRUG-282-0748` 维生素C / 维生素/配伍边界 / p.282：Vitamin C 【药理作用及适应证】又名抗坏血酸，广泛参与机体的多种生化反应。参加体内氧化还原反应，促进细胞间质的合成，保持细胞间质的完整，增加毛细血管壁致密度，降低其通透性及脆性；参与解毒功能；维生素C具有强还原性，保护酶系的巯基以避免被毒物破坏；参与体内活性物质和组织代谢，如胶原蛋白合成；增强机体抗病能力，可提高白细胞和吞噬细胞功能等。主要用于防治维生素C缺乏症，铅、汞、砷、苯等的慢性中毒，以及风湿性疾病、药疹和高铁血红蛋白血症等；辅助治疗急慢性感染、各种贫血、肝胆疾病、心源性和感染性休克等；还可促进创伤愈合等。 `source_id=SRC-0092; page=282`
<!-- RAU_201_400_V14_END -->

## RAU_401_600_V14

- Original marker: `RAU_401_600_V14_START` / `RAU_401_600_V14_END`
- Original runtime page: `wiki/drugs/DRUG-034-sulfonamides.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 0

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）中药联用边界 / SRC-0093

- 本批来源补充中药类兽药的联用、禁忌、用药注意和症候支持边界；乌梅、五味子等酸化尿液时可增强磺胺类结晶尿/血尿/尿闭风险；需作为禁忌/监测提示。 完整事实见 `exports/veterinary_rational_use_401_600_fact_index.csv`。
- 使用门禁：不得据此单独生成现代兽药可执行剂量、疗程、休药期、MRL 或合规承诺；抗菌药、驱虫药、激素、急救药等仍需标签/法规/药敏或等效来源。
<!-- RAU_401_600_V14_END -->
