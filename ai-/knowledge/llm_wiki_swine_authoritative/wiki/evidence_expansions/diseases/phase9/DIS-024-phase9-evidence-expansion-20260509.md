---
page_id: DIS-024
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-024 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- Byte size moved: 1511
- Fact-like rows moved: 3
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 3

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 3 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 10.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0001` 处方1：抗猪瘟血清；25毫升；庆大小诺霉素注射液；16万～32万单位；用法=用法：一次肌内或静脉注射，每日1次，连用 $2\sim 3$ 次。；注=说明：在猪尚未出现腹泻时应用本方可获得一定疗效。。`source_id=SRC-0087; page=10; line=520-532`
- `HANDBOOK-RX-0002` 处方2 预防：猪瘟兔化弱毒疫苗；2头份；用法=用法：非猪瘟流行区，仔猪 $60\sim 70$ 日龄时接种1次；猪瘟流行区，21日龄第1次接种，65日龄再接种1次，种猪群以后每年加强免疫1次。发病猪群中假定健康猪及其他受威胁的猪只，可用此苗作紧急预防接种。；注=。`source_id=SRC-0087; page=10; line=534-540`
- `HANDBOOK-RX-0003` 处方3 白虎汤加减：生石膏40克（先煎）；知母20克；生山栀10克；板蓝根20克；玄参20克；金银花10克；大黄30克（后下）；炒枳壳20克；鲜竹叶30克；生甘草10克；用法=用法：水煎去渣，候温灌服，每天1剂，连服 $2\sim 3$ 剂。；注=说明：配合西药治疗。。`source_id=SRC-0087; page=10; line=542-566`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- Byte size moved: 944
- Fact-like rows moved: 2
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 2

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Treatment Evidence (SRC-0088, V13.1 batch)

- Batch status: 2 treatment facts linked to this disease page.
- Source pages: 49.
- Full matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`; fact index: `exports/veterinary_treatment_of_pigs_fact_index.csv`.

- `VTOP-TX-0045` vaccination / p.49 / Classical swine fever: There are inactivated and live vaccines to CSF available but none of them are licensed in the UK. `source_id=SRC-0088; page=49; line=1463`
- `VTOP-TX-0251` vaccination / p.49 / Classical Swine Fever: from other pestiviruses. There is no treatment and most countries adopt a slaughter policy. In countries where the disease is endemic there is a vaccine which may be used. If wild boar are involved there is a live vaccine, which can be put in bait to attempt to control the disease. `source_id=SRC-0088; page=49; line=3240`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- Byte size moved: 21387
- Fact-like rows moved: 40
- Candidate fact mentions moved: 2
- Dose/route/course fact markers moved: 2
- Source anchors moved: 40

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 43 linked disease-control/treatment facts.
- Source pages: 6, 96, 111, 113, 117, 119, 120, 124, 125, 126, 127, 129, 130, 131, 132, 145, 152, 153, 159.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0007` vaccination_or_immunization / p.6 / 兽药分类: （1）病毒疫苗 猪瘟活疫苗（I）、猪瘟活疫苗（Ⅱ）、猪口蹄 `source_id=SRC-0089; page=6; line=444`
- `SFDUT1-TX-0442` vaccination_or_immunization / p.96 / 地塞米松: 目前，不少猪场均存在着蓝耳病、2型圆环病毒感染、猪流感、猪瘟、猪伪狂犬病等免疫抑制性疾病，使用地塞米松更要慎重，不乏应用后病情恶化的病例。因为地塞米松无抗病毒作用，用后反而可降低抗体的防御能力，使病毒得以复制和增殖，病情反而加重。 `source_id=SRC-0089; page=96; line=2379`
- `SFDUT1-TX-0474` vaccination_or_immunization / p.111 / 中、小型集约化养猪场兽医防疫工作规程: （4）要坚持自繁自养的原则，必需引进猪只前必须调查产地是否为非疫区，并有产地检疫；猪只在装运及运输过程中没有接触过其他偶蹄动物，运输车辆应做过清洗消毒，猪只引入后至少隔离饲养30天，在此期间进行观察、检疫，确认为健康者方可并群饲养，及时注射猪瘟等疫苗。 `source_id=SRC-0089; page=111; line=2568`
- `SFDUT1-TX-0477` treatment_or_prevention / p.111 / 中、小型集约化养猪场兽医防疫工作规程: ① 驻场兽医应及时进行诊断，调查疫源，向当地畜牧兽医行政管理部门报告疫情，根据各类疫病的特点做好封锁、隔离、消毒、紧急防疫、治疗和淘汰等工作，做到早发现、早确诊、早处理，把疫情控制在最小范围内；确诊发生口蹄疫、猪水疱病时，养猪场应配合当地畜牧兽医管理部门对猪群实施严格的隔离、扑杀措施；发生猪瘟、伪狂犬病、猪蓝耳病、布鲁菌病时，应对猪群实施清群和净化措施；全场进行彻底的清洗消毒，病死或淘汰猪的尸体进行无害化处理。 `source_id=SRC-0089; page=111; line=2591`
- `SFDUT1-TX-0480` vaccination_or_immunization / p.113 / 制定和执行科学的免疫程序: （1）猪瘟 选用普通的猪瘟活疫苗（Ⅱ）（细胞源），又称犊牛睾丸细胞疫苗，通用名猪瘟细胞苗，国家标准为每头份抗原含量不低于750个兔体感染量（RID）。生产厂家：永顺、中牧、维科、齐鲁、南京天邦等。 `source_id=SRC-0089; page=113; line=2603`
- `SFDUT1-TX-0485` vaccination_or_immunization / p.113 / 制定和执行科学的免疫程序: 提示：①使用前要认真查看说明书。现在的猪瘟细胞苗广告宣传和说明书上多数都标有每头份抗原含量是多少个兔体感染量，抗原含量参差不齐（有的标称每头份 $\geqslant 20000$ 个RID）。凡含量只标示每头份含细胞毒液不少于0.015毫升而没有标示含多少个兔体感染量的，其实就是那种抗原含量不少于750个RID的普通猪瘟细胞苗，可适当加大剂量。而政府采购专用高效价猪瘟活疫苗（细胞源）质量标准中明确规定每头份抗原含量不少于7500个RID，使用时就不要再增加剂量，1头份即可，但要使用专用稀释液。②政府采购专用猪瘟活疫苗（I），又称猪瘟牌淋苗，剂量 $1\sim 2$ 头份即可，使用时参照产品说明书。③不要使用猪瘟、猪丹毒、猪多杀性巴氏杆菌病三联活疫苗。 `source_id=SRC-0089; page=113; line=2610`
- `SFDUT1-TX-0513` vaccination_or_immunization / p.117 / 制定和执行科学的免疫程序: （1）后备种公、母猪（5月龄转入后备种猪舍）160日龄，乙型脑炎、细小病毒首免（乙型脑炎仅 $4\sim 9$ 月蚊虫季节免疫）；170日龄，伪狂犬首免；180日龄，乙型脑炎、细小病毒二免（乙脑仅 $4\sim 9$ 月蚊虫季节免疫）；190日龄，口蹄疫；200日龄，伪狂犬二免；210日龄，猪瘟。225日龄，可以配种。 `source_id=SRC-0089; page=117; line=2664`
- `SFDUT1-TX-0514` vaccination_or_immunization / p.117 / 制定和执行科学的免疫程序: （3）种公猪 3月1日、9月1日，猪瘟；3月10日～20日，7月10日～20日，11月10日～20日，口蹄疫（不要在同一天全部免疫，防止影响精液品质及准胎率）；4月1日、10月1日，猪细小病毒（2周岁以上的不必免疫）；2月15日、6月15日、10月15日，伪狂犬病；4月初至9月底，乙脑（只免2周岁以内的）。 `source_id=SRC-0089; page=117; line=2666`
- `SFDUT1-TX-0515` vaccination_or_immunization / p.117 / 制定和执行科学的免疫程序: （4）免疫母猪所产仔猪 $25\sim 30$ 日龄，猪瘟首免；断奶后7天内，病毒性腹泻（每年10月至次年3月寒冷季节免疫）；45日 `source_id=SRC-0089; page=117; line=2667`
- `SFDUT1-TX-0526` vaccination_or_immunization / p.119 / 猪疫苗免疫接种应注意的细节: （1）常用的病毒弱毒苗猪瘟活疫苗（I）（俗称脾淋苗）、猪瘟活疫苗（Ⅱ）（俗称细胞苗）、繁殖与呼吸综合征活疫苗（俗称蓝耳病活疫苗）、伪狂犬病活疫苗、伪狂犬病基因缺失活疫苗、猪传染性胃肠炎-猪流行性腹泻二联活疫苗、乙型脑炎活疫苗。 `source_id=SRC-0089; page=119; line=2690`
- `SFDUT1-TX-0538` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （8）选对稀释液 每种活疫苗都有专门的稀释配方，适合于一种疫苗的稀释液也许会灭活另一种疫苗。乙脑活疫苗、猪伪狂犬病活疫苗等带有专用稀释液，必须用专用稀释液而不能用生理盐水或注射用水稀释。猪瘟活疫苗必须用生理盐水而不能用注射用水、凉开水或矿泉水稀释，猪链球菌活疫苗必须用 $20\%$ 铝胶盐水稀释。 `source_id=SRC-0089; page=120; line=2708`
- `SFDUT1-TX-0540` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （1）有针对性地选用疫苗 要掌握本地区及本场传染病的流行情况，有针对性、有选择地进行免疫预防。免疫接种应遵循病毒性疾病免疫为先的原则，猪瘟、口蹄疫、伪狂犬病、圆环病毒、乙脑、细小病毒病等没有争议的病毒病疫苗必须免疫。细菌苗要依据本场具体情况有选择性地使用，疫苗使用不是越多越好，可用可不用的疫苗不要使用，一些疾病可通过添加药物预防，从未发生过猪肺疫、猪丹毒、链球菌病等的猪场也可不接种这几种病的菌苗。 `source_id=SRC-0089; page=120; line=2713`
- `SFDUT1-TX-0546` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （6）避免两种或两种以上疫苗同时注射，以免互相干扰影响抗体产生猪瘟活疫苗、蓝耳病弱毒苗、伪狂犬病弱毒苗等病毒活疫苗之间，必须间隔7天以上。猪口蹄疫O型灭活苗更不能与猪瘟活疫苗混合注射，要先免疫好猪瘟，后接种口蹄疫疫苗。 `source_id=SRC-0089; page=120; line=2721`
- `SFDUT1-TX-0554` vaccination_or_immunization / p.124 / 猪瘟: 猪瘟（CSF）是由猪瘟病毒（CSFV）引起猪的一种急性、热性、高度接触性传染病。它传染性强、流行广泛、发病率和死亡率甚高，危害极大。世界动物卫生组织（OIE）将其列为A类动物疫病，我国也将其列为一类动物疫病。我国多年来实行以免疫预防为主的防制策略，猪瘟急性暴发式流行已得到有效控制，但并未被扑灭，仍在我国范围内不间断地小规模散发流行，其流行特点出现了新变化。不仅典型的猪瘟时有暴发，非典型猪瘟更是频繁发生，并出现持续感染（临床隐性感染）、胎盘垂直感染（仔猪先天性感染）、妊娠母猪带毒综合征（母猪繁殖障碍）及新生仔猪的免疫耐受等。这些带毒猪的存在，成为猪瘟发生的祸根，尤其是亚临床感染猪，依靠常规方法很难确诊并剔除此类病猪，从而给猪瘟防制工作带来新的困难。在出现这些流行特点的地区和猪场，往往还伴随有多种原因引起的免疫失败，严重威胁养猪业的健康发展。 `source_id=SRC-0089; page=124; line=2766`
- `SFDUT1-TX-0555` vaccination_or_immunization / p.125 / 猪瘟: 性和可变性。病毒可通过精液（人工授精）及交配方式感染母猪，经垂直传播的猪瘟病毒可使仔猪成为免疫麻痹的猪瘟带毒猪。人工感染的带毒母猪可无临床症状持续带毒750天以上，无临床症状的带毒猪体内的病毒可经垂直或水平方式传播。疫苗弱毒对猪瘟带毒猪无免疫保护作用。 `source_id=SRC-0089; page=125; line=2774`
- `SFDUT1-TX-0556` vaccination_or_immunization / p.125 / 猪瘟: 猪瘟病毒与牛病毒性腹泻病毒（BVDV）有高度同源性，可存在交叉反应。牛病毒性腹泻病毒感染妊娠母猪可引起繁殖障碍，病毒可经胎盘传染胎儿，导致畸胎形成或使所产仔猪造成亚临床感染。用牛病毒性腹泻病毒污染的猪瘟细胞苗（污染主要来源是小牛血清）免疫母猪后，仔猪发生类似先天性猪瘟感染的症状与病理变化，死亡率增加，因此给生产造成很大损失。此外，BVDV会干扰猪瘟疫苗的免疫效果。 `source_id=SRC-0089; page=125; line=2776`
- `SFDUT1-TX-0557` vaccination_or_immunization / p.125 / 猪瘟: （1）易感动物 在自然情况下，只是猪和野猪感染发病，任何年龄、品种、性别的猪在任何季节都可发病。免疫母猪所生仔猪因哺乳可获得一定的被动免疫保护，对该病有一定的短期抵抗力。没有或不按期进行预防注射的地区，或者免疫程序不科学，疫苗质量差和保管、运输不当等，都可使猪群发病。一旦发病，短期内可造成较大范围的流行，发病和死亡率都较高。在常发地区或预防注射密度不很高的地区，可呈零星散发。 `source_id=SRC-0089; page=125; line=2782`
- `SFDUT1-TX-0558` candidate_fact / p.126 / 猪瘟: 病毒传播主要通过直接或间接与病猪接触经口鼻传播。传染途径主要是消化道，食入污染的饮料或饮水，就能被传染；也可通过 `source_id=SRC-0089; page=126; line=2786`
- `SFDUT1-TX-0559` vaccination_or_immunization / p.126 / 猪瘟: 瘟。感染弱毒株可造成中等程度疫病或亚临床感染，但这些弱毒株可引起迟发性猪瘟，其症状轻微或亚临床形式，导致胎儿死亡和新生仔猪死亡。以下分型不要绝对分开，因为临床症状也取决于猪日龄、免疫状态、营养和饲养情况、健康状况以及是否与其他病毒、细菌混合感染等。仔猪表现的临床症状比成年猪明显。典型猪瘟可分为4型，此外，还有非典型型及繁殖障碍型猪瘟。 `source_id=SRC-0089; page=126; line=2800`
- `SFDUT1-TX-0560` candidate_fact / p.127 / 猪瘟: （1）最急性型较少见，在新疫区发病初期可见。病猪除体温升高外，常无明显症状，往往在 $1\sim 2$ 天内因循环障碍和休克而突然死亡。 `source_id=SRC-0089; page=127; line=2802`
- `SFDUT1-TX-0561` vaccination_or_immunization / p.127 / 猪瘟: （6）繁殖障碍型（又称“带毒母猪综合征”）近些年来，猪瘟还有一种新的临床动态，系母猪妊娠期感染弱毒株经胎盘感染所致。妊娠母猪主要表现为早产或流产，产木乃伊胎、死胎（占每窝仔猪 $33\% \sim 50\%$ ）、畸形胎或弱仔，弱仔多在产后数天内死亡。一般情况下，母猪妊娠早期在40日龄感染猪瘟病毒多数会发生流产、产死胎和木乃伊胎；妊娠70日龄感染病毒可产下弱仔猪，表现为先天性震颤，俗称“抖抖病”，病后约2周内死亡；妊娠 $80\sim 90$ 日龄感染病毒时产出的仔猪，除少数仔猪发病死亡外，多数仔猪能成活，这些仔猪并不表现症状，对猪瘟疫苗的免疫不产生免疫应答，表现出先天性免疫耐受，有的因疫苗免疫失败而死亡，也有不发病的感染仔猪终身向外排毒而成为最危险的传染源。这些持续性感染的带毒仔猪，如果作后备种猪培育，则会形成新的带毒种猪群，使猪瘟在猪群中传播下去，是猪瘟防制中必须解决的重要问题之一。而母猪和配种公猪一般经疫苗免疫过有一定免疫力，则不表现症状。此型要注意与其他病毒性流产相区别。 `source_id=SRC-0089; page=127; line=2810`
- `SFDUT1-TX-0562` vaccination_or_immunization / p.129 / 猪瘟: （1）免疫荧光抗体测验（FAT）检测病原。具有简单、快速（2小时内可得出结果）和可靠的特点。 `source_id=SRC-0089; page=129; line=2830`
- `SFDUT1-TX-0563` vaccination_or_immunization / p.129 / 猪瘟: （2）动物接种试验。将病料接种易感家兔，进行兔体免疫交叉试验。 `source_id=SRC-0089; page=129; line=2831`
- `SFDUT1-TX-0564` vaccination_or_immunization / p.129 / 猪瘟: （3）酶联免疫吸附试验（ELISA）检测强毒特异性抗体。此法可用于区分强毒感染抗体和疫苗免疫抗体。 `source_id=SRC-0089; page=129; line=2832`
- `SFDUT1-TX-0565` treatment_or_prevention / p.129 / 猪瘟: （1）强化猪瘟防控意识，将猪瘟防控放在第一位 要按照《动物防疫法》的要求，认真贯彻“预防为主，防重于治”和综合防制的方针，克服“重治轻防，只治不防”的消极错误认识，千方百计要把猪瘟预防好，尽管有高致病性蓝耳病的肆虐，但猪瘟至今仍是“第一杀手”。 `source_id=SRC-0089; page=129; line=2837`
- `SFDUT1-TX-0566` dose_route_course / p.129 / 猪瘟: 则，其中心思想是严格的隔离、消毒和防疫，防止所有的病原进入猪群。关键控制点在于对人和环境的控制，建立起防止病原入侵的多层屏障，使猪只生长在最佳状态的生产环境中。通过实施生物安全措施，对防制猪传染病的发生，获得较好的经济效益都是十分重要的。我国目前广大养猪单位不同程度地执行了有关生物安全措施，但共同的缺点是执行不彻底、不完全、不持久，因而使某些传染病有可乘之机。要搞好养猪工作，必须推行生物安全技术。 `source_id=SRC-0089; page=129; line=2840`
- `SFDUT1-TX-0567` vaccination_or_immunization / p.129 / 猪瘟: （3）坚持预防接种制度，建立科学、合理的免疫程序 用猪瘟疫苗给猪只接种，能使猪体产生特异性的抵抗力，在一定时间内能使猪只不感染猪瘟，这是预防猪瘟的有效手段，养猪者一定要坚持做好。在安排免疫接种时，应重视以下几方面的工作：①要使用货真价实的高质量的疫苗，这是获得免疫成功的物质基础；②免疫程序一定要科学合理；③要避免和克服免疫注射全过程中的失误（如疫苗稀释、注射方法、更换针头等）影响免疫效果，造成免疫失败。 `source_id=SRC-0089; page=129; line=2842`
- `SFDUT1-TX-0568` vaccination_or_immunization / p.130 / 猪瘟: 科学、合理的免疫程序是根据猪瘟的流行特点、猪只年龄、母源抗体水平等确定，并需根据监测的结果调整免疫程序，没有一个适合全国所有养猪场的统一的免疫程序。农业部《2011年国家动物疫病强制免疫计划》中要求对所有猪进行猪瘟强制免疫。规模养猪场免疫程序：商品猪， $25\sim 30$ 日龄初免， $60\sim 70$ 日龄加强免疫一次；种猪， $25\sim 30$ 日龄初免， $60\sim 70$ 日龄加强免疫一次，以后每 $4\sim 6$ 个月免疫一次。发生疫情时对疫区和受威胁地区所有健康猪进行一次强化免疫。最近1个月内已免疫的猪可不进行强化免疫。各种疫苗免疫接种方法及剂量按相关产品说明书规定操作。免疫21天，进行免疫效果监测。猪瘟抗体阻断ELISA检测试验抗体阳性判定为合格，猪瘟抗体正向间接血凝试验抗体效价 $\geqslant 25$ 判定为合格。存栏猪抗体合格率 $\geqslant 70\%$ 判定为合格。 `source_id=SRC-0089; page=130; line=2844`
- `SFDUT1-TX-0569` vaccination_or_immunization / p.130 / 猪瘟: 现推荐一个大多数规模化猪场采用的免疫程序，仅供参考。疫苗可选用常规猪瘟细胞苗（通用名），常用名是猪瘟活疫苗（Ⅱ）（细胞源），又称犊牛睾丸细胞疫苗［俗称细胞苗，国家标准效价指标： $\geqslant 750$ 个兔体感染量（RID)/头份]。猪瘟细胞苗必须无菌、无支原体、无牛病毒性黏膜病毒污染。 `source_id=SRC-0089; page=130; line=2846`
- `SFDUT1-TX-0570` vaccination_or_immunization / p.130 / 猪瘟: 种公猪：每年3月、9月各免疫1次，细胞苗8头份。 `source_id=SRC-0089; page=130; line=2848`
- `SFDUT1-TX-0571` vaccination_or_immunization / p.130 / 猪瘟: 种母猪：每次产后 $25 \sim 30$ 天免疫1次（空怀母猪要及时补免），细胞苗8头份。 `source_id=SRC-0089; page=130; line=2850`
- `SFDUT1-TX-0572` vaccination_or_immunization / p.130 / 猪瘟: 后备种公、母猪：按仔猪免疫程序，至 $6\sim 7$ 月龄配种前再加强一次免疫，细胞苗8头份，以后按种猪免疫程序进行。 `source_id=SRC-0089; page=130; line=2854`
- `SFDUT1-TX-0573` vaccination_or_immunization / p.130 / 猪瘟: 政府采购的猪瘟脾淋苗（常用名），通用名是猪瘟活疫苗（I）（兔源、脾淋组织），或政府采购的高效价猪瘟细胞苗[效价指标： $\geqslant 7500$ 个兔体感染量（RID)/头份]的使用剂量可参照生产厂家的使用说明书。 `source_id=SRC-0089; page=130; line=2856`
- `SFDUT1-TX-0574` vaccination_or_immunization / p.130 / 猪瘟: 要正确采用“乳前免疫”。乳前免疫又称“超前免疫”或“零时免疫”，即在仔猪出生后未吸初乳前立即注射猪瘟疫苗，注射疫苗后隔1小时再吮吸初乳。该方法在我国应用已20多年，在某些大、中型规模化养猪场应用，证明是切实可行的。 `source_id=SRC-0089; page=130; line=2858`
- `SFDUT1-TX-0575` vaccination_or_immunization / p.131 / 猪瘟: 在养猪生产实际中，要做好仔猪乳前免疫是一件不容易的事情，母猪大多在夜间分娩，负责值班的人员（或接生员）稍有睡意，待出生仔猪吸吮初乳后注射就失去免疫的效果，一定要有忠于职守的专人守护，对出生后尚未吸初乳的仔猪逐头注射猪瘟疫苗，经一小时后再让出生仔猪吸吮初乳，否则造成免疫失败。免疫剂量最多2头份为宜。 `source_id=SRC-0089; page=131; line=2860`
- `SFDUT1-TX-0576` vaccination_or_immunization / p.131 / 猪瘟: “乳前免疫”目前有争议，可密切关注今后的研究成果及推广使用动态。 `source_id=SRC-0089; page=131; line=2862`
- `SFDUT1-TX-0577` vaccination_or_immunization / p.131 / 猪瘟: （6）实施疫苗接种效果的监测 常用的是ELISA检测。猪场要评价疫苗质量的优劣，应该监测抗体。疫苗免疫3周后测猪群的抗体，阳性率达到 $95\%$ 以上，就是合格的。 `source_id=SRC-0089; page=131; line=2872`
- `SFDUT1-TX-0578` dose_route_course / p.131 / 猪瘟: 对病猪及可疑病猪，立即隔离饲养，特别是贵重的种猪，在备有抗猪瘟血清的单位，可用于猪瘟早期的治疗，对中后期的猪瘟无效；对发病猪场及附近尚没发病的猪只，立即全部用猪瘟兔化弱毒疫苗进行紧急注射，可有效地制止新的病猪出现，缩短流行过程，减少部分损失；发病猪舍、运动场、饲养管理用具及环境，用消毒药液进行消毒；粪、尿及垫草等污物，堆积发酵后作肥料利用；死猪深埋或销毁、化制。 `source_id=SRC-0089; page=131; line=2878`
- `SFDUT1-TX-0579` vaccination_or_immunization / p.132 / 猪口蹄疫: 畜传染病之一。因其具有高度传染性和对畜牧业生产、肉食品供应及其产品对国际贸易造成的重大影响，世界动物卫生组织（OIE）将口蹄疫列为A类传染病之首，我国也将其列为一类动物疫病（17种）的第一位。《2012年国家动物疫病强制免疫计划》也将口蹄疫列为猪的3大强制免疫计划（口蹄疫、高致病性蓝耳病、猪瘟）之首，要求对所有猪进行O型口蹄疫强制免疫。 `source_id=SRC-0089; page=132; line=2884`
- `SFDUT1-TX-0625` vaccination_or_immunization / p.145 / 猪繁殖与呼吸障碍综合征: 六是做好猪瘟、猪伪狂犬病、口蹄疫、2型圆环病毒病、猪细小病毒病等病毒性疾病和副猪嗜血杆菌病、猪链球菌病等细菌性疾病的疫苗免疫工作，防止与猪蓝耳病的混合感染。 `source_id=SRC-0089; page=145; line=3083`
- Additional linked rows omitted here: 3; see `exports/swine_farm_drug_use_1_200_fact_index.csv`.
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- Byte size moved: 6997
- Fact-like rows moved: 11
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 11

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 增强证据 (SRC-0090, V13.1 batch)

- Batch status: 11 linked disease-control/treatment facts.
- Source pages: 198, 202, 205, 218, 262, 284, 290, 307, 308, 309.
- Matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_200_363_fact_index.csv`.

- `SFDUT2-TX-0034` vaccination_or_immunization / p.198 / 副猪嗜血杆菌病: 单纯性感染较少。猪瘟、支原体肺炎、萎缩性鼻炎、猪伪狂犬病等原发病的流行为本病的继发和混合感染提供了可乘之机。特别是随着圆环病毒病和蓝耳病这两种所谓的“猪的艾滋病”的流行，使机体免疫功能下降，更易乘机暴发本病。本病往往是这两种病的影子。临床实践证明，保育舍内暴发蓝耳病后，HPS的存在和继发感染可加剧病情并使临床表现复杂化，是造成10周龄以前仔猪死亡率升高的重要的细菌性致病因子。反过来HPS的严重感染又成为蓝耳病存在的“指示病”。 `source_id=SRC-0090; page=198; line=125`
- `SFDUT2-TX-0051` vaccination_or_immunization / p.202 / 副猪嗜血杆菌病: （2）加强生物安全 严格兽医卫生，杜绝外来病原菌，特别要防止引种时引入病原；要按科学合理的免疫程序做好猪瘟、伪狂犬、蓝耳病、支原体肺炎等防疫工作；搞好舍内外环境卫生及经常化的隔离、消毒（每周带猪消毒 $1\sim 2$ 次），防控好圆环病毒病及其他病毒性疾病，消除其他呼吸道病原。 `source_id=SRC-0090; page=202; line=184`
- `SFDUT2-TX-0059` vaccination_or_immunization / p.205 / 猪链球菌病: 型圆环病毒、猪瘟、伪狂犬病等病毒混合感染，或饲喂霉变饲料，导致免疫抑制，均可加重猪链球菌引起的临床症状。 `source_id=SRC-0090; page=205; line=224`
- `SFDUT2-TX-0103` vaccination_or_immunization / p.218 / 猪传染性胸膜肺炎: （1）坚持预防为主、养重于防、防重于治、防治结合的原则做好猪伪狂犬病、猪瘟、传染性胸膜肺炎、气喘病、蓝耳病、副猪嗜血杆菌病等有关疫病的免疫接种，搞好综合防制。 `source_id=SRC-0090; page=218; line=412`
- `SFDUT2-TX-0212` treatment_or_prevention / p.262 / 7. 诊断: 应注意与温和型猪瘟、猪蓝耳病、链球菌病、猪流行性感冒、黄曲霉中毒、弓形体病、硒-维生素E缺乏症以及其他引起繁殖障碍和泌乳障碍的疾病等进行鉴别诊断。日龄较大的病猪，症状与猪流感相似，但猪流感用一般抗生素和退热药治疗有较好疗效，而附红细胞体病使用以上药物无效。附红细胞体病发病后期易与猪瘟相混淆，但猪瘟无贫血和黄疸症状，且表现为多发性败血症变化。附红细胞体病血液稀薄，有伤口会流血不止，且血液呈淡红色或水 `source_id=SRC-0090; page=262; line=1122`
- `SFDUT2-TX-0275` vaccination_or_immunization / p.284 / 产后泌乳障碍综合征: (6) 加强兽医卫生和生物安全 选用杜邦卫可、农福、先灵宝雅 “安灭杀” 等消毒剂定期消毒, 特别抓好配种前和分娩前后的消毒工作, 防止有关疾病的发生。认真做好猪瘟、伪狂犬、传染性胃肠炎、蓝耳病、口蹄疫等几种主要传染病的免疫接种。 `source_id=SRC-0090; page=284; line=1475`
- `SFDUT2-TX-0277` vaccination_or_immunization / p.290 / 母猪繁殖障碍性疾病: （1）切实做好必须免疫疫苗的接种 对于预防繁殖障碍性疫病免疫效果好、没有争议的疫苗，尤其是猪瘟、猪伪狂犬病病毒、细小病毒、乙脑疫苗，一定要按合理的、规范化的免疫程序，使用质量过关的疫苗，把接种做扎实。而且要注意细节及操作规程。对于后备母猪一定要在配种前做好这四种疫苗的注射。此外不要在妊娠期接种猪瘟疫苗，失真空或接近失效期的疫苗不能用。乙脑要选弱毒苗，用专用稀释液稀释，而不要使用灭活苗，两胎以上可不接种。细小病毒尽可能使用灭活苗。这两种苗首免要在150日龄以上，间隔 $2\sim 3$ 周，加强免疫一次效果更佳。商品猪场伪狂犬病可使用全病毒灭活苗，种猪场可选用基因缺失弱毒苗。 `source_id=SRC-0090; page=290; line=1550`
- `SFDUT2-TX-0279` vaccination_or_immunization / p.290 / 母猪繁殖障碍性疾病: （3）搞好种群净化 要搞好疫病监测，坚决淘汰阳性种猪，最好每半年对种公、母猪病毒性繁殖障碍性疫病的免疫抗体水平进行一次检测，淘汰和消除亚临床感染或隐性感染猪。对于猪瘟和伪狂犬病，有条件的可采取活体猪扁桃体荧光抗体试验，检查出阳性（带毒）猪，一律立即淘汰，每6个月进行一次，大约 $3\sim 4$ 次净化后，猪瘟、伪狂犬病可得到完全控制。伪狂犬病还可通过种猪接种基因缺失弱毒苗后，配合使用鉴别诊断ELISA试剂盒，定期对种猪群进行监测，野病毒感染阳性者做淘汰处理。 `source_id=SRC-0090; page=290; line=1552`
- `SFDUT2-TX-0344` vaccination_or_immunization / p.307 / 猪呼吸道病综合征: (6) 做好猪瘟、猪伪狂犬病和猪气喘病的免疫注射。 `source_id=SRC-0090; page=307; line=1801`
- `SFDUT2-TX-0348` vaccination_or_immunization / p.308 / 猪疫苗过敏反应: 猪疫苗过敏反应是抗原-抗体反应所致的一种急性疾病，是变态反应（可分为4个类型）的一种，又称I型变态反应或速发型超敏反应。在临床上，以注射猪瘟活疫苗、猪口蹄疫O型灭活疫苗最容易引起过敏反应，其次为猪伪狂犬病疫苗和仔猪副伤寒疫苗等，应引起特别关注。 `source_id=SRC-0090; page=308; line=1811`
- `SFDUT2-TX-0350` vaccination_or_immunization / p.309 / 猪疫苗过敏反应: 过敏反应是抗原与循环抗体或结合的细胞抗体相互作用与反应的结果。疫苗能与体内蛋白质结合形成变应原，这些变应原能刺激机体产生一种特异类型的反应素抗体 IGE，过敏抗体可通过初乳传递，这也是为什么有的初生仔猪用猪瘟细胞苗进行“乳前免疫”时会发生过敏反应的原因。它对于肥大细胞具有特殊的亲和力，能牢固地结合在这些细胞的表面，使机体处于致敏状态。当上述变应原再次进入致敏动物体内时，使与靶细胞表面 IGE 的 Fab 片段结合，释放多种活性介质，如组胺、前列腺素、激肽、过敏毒素等。它们作用于相应的效应器官，导致平滑肌收缩、毛细血管扩张及通透性增强、血压下降和腺体分泌增多等免疫病理反应即过敏反应。猪主要表现为肺的反应，引起肺充血、水肿和气肿，常因呼吸困难缺氧而死亡。 `source_id=SRC-0090; page=309; line=1817`
<!-- SFDUT_200_363_V13_1_END -->
