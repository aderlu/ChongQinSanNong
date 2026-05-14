---
page_id: DRUG-066-dexamethasone
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase3_drug_evidence_expansion
moved_from: wiki/drugs/DRUG-066-dexamethasone.md
generated: 2026-05-09T11:42:41+08:00
---

# DRUG-066-dexamethasone Evidence Expansion

This file stores detailed batch evidence moved out of the runtime drug page during Phase 3 cleanup.

Runtime rule:

- Do not load this file for default production/evaluation retrieval.
- Load it only for evidence expansion, audit, source lookup, or manual review.
- Dose, route, course, withdrawal period, MRL, residue, and food-safety claims still require current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-066-dexamethasone.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 7

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 7 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 地塞米松.
- Source pages: 16, 29, 44, 89, 149, 152.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0011` 轮状病毒病 / 处方1 `source_id=SRC-0087; page=16; line=751-777`
- `HANDBOOK-RX-0033` 猪水肿病 / 处方1 `source_id=SRC-0087; page=29; line=1276-1322`
- `HANDBOOK-RX-0059` 猪链球菌病 / 处方1 `source_id=SRC-0087; page=44; line=1829-1835`
- `HANDBOOK-RX-0212` 支气管炎 / 处方1 `source_id=SRC-0087; page=89; line=3843-3849`
- `HANDBOOK-RX-0342` 5%普鲁卡因青霉素5~10毫升 / 处方2 `source_id=SRC-0087; page=149; line=6239-6249`
- `HANDBOOK-RX-0352` 母猪配种过敏症 / 处方2 `source_id=SRC-0087; page=152; line=6423-6427`
- `HANDBOOK-RX-0353` 母猪配种过敏症 / 处方3 `source_id=SRC-0087; page=152; line=6429-6443`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-066-dexamethasone.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 11

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 3 appendix medicine rows and 8 text treatment mentions linked to this drug page.
- Source pages: 88, 97, 107, 109, 116, 117, 127, 134, 151.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0002` Dexadreson (2 mg dexamethasone/ml): dose=1.5 ml/50 kg iv or im once and repeated in 48 h; meat_withhold=2 days. `source_id=SRC-0088; page=151; table=Table A.1 includes the only licensed products which are available in the UK at the time of writing.`
- `VTOP-MED-0012` Rapidexon (2 mg dexamethasone/ml): dose=1.5 ml/50 kg iv or im once and repeated in 48 h; meat_withhold=2 days. `source_id=SRC-0088; page=151; table=Table A.1 includes the only licensed products which are available in the UK at the time of writing.`
- `VTOP-MED-0017` Voren Suspension for Injection, 1 mg/ml (1 mg dexamethazone/ml): dose=2 ml/100 kg im in growing pigs and adults; 1 ml/10 kg im in piglets; meat_withhold=55 days. `source_id=SRC-0088; page=151; table=Table A.1 includes the only licensed products which are available in the UK at the time of writing.`
- `VTOP-TX-0144` dose_or_route / p.88 / Smoke inhalation: Fires are a constant danger on pig farms, particularly on smallholdings and in old, poorly designed buildings. Pigs will die from smoke inhalation. The cause of death can be seen on post-mortem and confirmed by histopathology. If pigs can be removed from the smoke and are still breathing, they should be given dexamethazone at a raised dose of $1 \mathrm { m g } / 5 \mathrm { k g }$ . They should be checked to ascerta `source_id=SRC-0088; page=88; line=2316`
- `VTOP-TX-0188` dose_or_route / p.97 / Farrowing fever complex: practitioners used to give dexamethazone to reduce the inflammation in the mammary gland. With the advent of NSAIDs the author would recommend them rather than dexamethazone. NSAIDs and dexamethazone certainly should not be given at the same time. Oxytocin is a useful drug either if parturition is complete or if there is a likelihood of further pigs being born. In this latter case it should be given as small intramus `source_id=SRC-0088; page=97; line=2610`
- `VTOP-TX-0207` treatment_candidate / p.107 / Streptococcal meningitis: This is one of the most common neurological diseases to affect pigs. It is caused by Streptococcus suis type 1. The most usual condition in the UK occurs in the 8–12 week age group. Pigs may be found dead, but the condition is more commonly seen as pigs which are unable to sit up and are paddling. They will have a raised rectal temperature. Antibiotics, normally penicillin, are very helpful. A small dose of dexametha `source_id=SRC-0088; page=107; line=2877`
- `VTOP-TX-0211` treatment_candidate / p.109 / Heat stroke: This condition will certainly cause neurological signs. They are very similar to water deprivation (salt poisoning). Over-fat Vietnamese Pot Bellied Pigs are very susceptible. Sunburn may complicate the condition in white pigs. Pigs should be cooled rapidly with buckets of cold water or a hose. If they are in extremis, dexamethazone given iv will be helpful. If the pigs have sunburn they will require antibio tics, NS `source_id=SRC-0088; page=109; line=2953`
- `VTOP-TX-0238` euthanasia / p.116 / Pemphigus: Autoimmune diseases are seen in pigs but they are extremely rare. Diagnosis will be achieved by ruling out other causes for the erythematous, pruritic patches on the skin. Diagnosis could be confirmed by histopathology. Treatment is with corticosteroids in pet pigs. Initially dexamethazone can be injected at $2 \mathrm { \ m g } / 2 5 \mathrm { \ k g }$ every $^ { 4 8 \mathrm { ~ h ~ } }$ with antibiotic cover. Then  `source_id=SRC-0088; page=116; line=3148`
- `VTOP-TX-0243` treatment_candidate / p.117 / Uticaria: This is rare in pigs and is called ‘hives’. In theory it could be caused by a contact allergy or even a food allergy but these are unlikely. The likely cause is an allergic reaction to an insect bite, usually a biting fly or a tick. The whole of the pig’s body will be covered in raised plaques. This is a peracute condition. The pig’s temperature will be raised. The re - spiratory rate may be raised. The condition is  `source_id=SRC-0088; page=117; line=3170`
- `VTOP-TX-0263` dose_or_route / p.127 / Old World Screw-worm: Affected pigs should receive an injection of $2 0 0 ~ { \mu \mathrm { g } }$ ivermectin/ $\mathrm { ^ { \prime k g } }$ to kill the maggots. They should also receive antibiotics to combat the secondary infection and dexamethazone to limit the shock. The wound should be dressed with a cream containing acriflavin and BHC. `source_id=SRC-0088; page=127; line=3410`
- `VTOP-TX-0281` dose_or_route / p.134 / Iron toxicity: This can occur from the overdosing of injectable iron in piglets. The piglets will be very depressed and will huddle together. Careful examination will normally reveal physical damage to the muscles at the site of injection where a large dose has been injected. There is no specific antidote. Dexamethazone is suggested at $2 ~ \mathrm { m g }$ per piglet injected im. Death usually occurs within $6 \mathrm { ~ h ~ }$ o `source_id=SRC-0088; page=134; line=3562`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-066-dexamethasone.md`
- Candidate facts: 2
- Dose/route/course facts: 1
- Source anchors: 18

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 18 linked drug-use facts.
- Source pages: 21, 24, 31, 40, 41, 43, 61, 93, 96, 120, 152.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0068` vaccination_or_immunization / p.21 / 正确处理对因治疗与对症治疗: 任何事情都不能千篇一律。对因治疗与对症治疗是相辅相成的，有些情况下则要对因治疗与对症治疗相结合同时进行，例如，当发生急性肺炎，严重的呼吸困难和高热（41.5℃以上）会影响动物的抵抗力，加重病情，甚至引起死亡，此时，则应同时使用对因和对症治疗的药物，如用敏感抗菌药物杀菌，用安乃近或复方氨基比林退烧，用氨茶碱平喘，用地塞米松帮助杀菌药消炎、抗休克。或再配合维生素C以及免疫增强剂和抗病毒的中草药制剂，如黄芪多糖、双黄连、鱼腥草等，这样“标本兼治”可取得最佳疗效。此外，支持性和辅助性治疗也是至关重要的。例如，强心补液，使用抗血清、抗炎药（地塞米松）等可有效地挽救生命。 `source_id=SRC-0089; page=21; line=754`
- `SFDUT1-TX-0076` compliance_or_safety / p.24 / 掌握好妊娠母猪禁用或慎用的药物: 如地塞米松磷酸钠注射液（氟美松）、醋酸泼尼松龙注射液（强的松龙）等，孕育应慎用或禁用。妊娠期间（特别是妊娠早期）使用，可能影响胎儿的发育，甚至导致畸形。妊娠后期大剂量使用会引起流产。 `source_id=SRC-0089; page=24; line=794`
- `SFDUT1-TX-0111` treatment_or_prevention / p.31 / 肆霉素类: （1）作用与用途 主要适用于对青霉素敏感的 $\mathbf{G}^{+}$ 菌和 $\mathbf{G}^{-}$ 敏感菌引起的呼吸道、消化道、泌尿生殖道等感染，如大肠杆菌病、副伤寒、猪肺疫、传染性胸膜肺炎、副猪嗜血杆菌病、萎缩性鼻炎、细菌性肺炎、败血症、链球菌病、葡萄球菌病及多种细菌引起的皮炎和软组织感染均有显著疗效。与地塞米松合用治疗乳房炎、子宫炎、肾盂肾炎及泌乳障碍综合征等疗效极佳。 `source_id=SRC-0089; page=31; line=932`
- `SFDUT1-TX-0146` candidate_fact / p.40 / 氨基糖苷类: 偶尔引起皮疹、血管神经性水肿、发热等，也可引起过敏性休克，尤其是链霉素。一旦发生，应静注钙剂或肌注肾上腺素、地塞米松急救。 `source_id=SRC-0089; page=40; line=1130`
- `SFDUT1-TX-0147` vaccination_or_immunization / p.41 / 氨基糖苷类: 作为“繁殖期杀菌剂”的青霉素类、头孢菌素类，能破坏细菌细胞壁，有利于“静止期杀菌剂”的氨基糖苷类抗生素进入细胞体内而发挥杀菌作用，是处理混合感染、危重感染、免疫抑制感染以及致病菌不明感染联合用药的常用品种。常用的有：庆大霉素、卡那霉素、链霉素等与青霉素、氨苄西林钠、阿莫西林、头孢噻呋、头孢喹肟等联用，相互协同，增强疗效。如青霉素+庆大霉素+地塞米松治疗猪链球菌病、猪急性乳腺炎以及敏感细菌混合感染的疗效较高；氨基糖苷类与青霉素或氨苄西林联用治疗猪李氏杆菌病，与头孢菌素类联用治疗肺炎杆菌；庆大霉素与阿莫西林联用治疗铜绿假单胞菌等。但用药剂量应基本平衡，过大剂量的青霉素或其他半合成青霉素均可使氨基糖苷类活性降低。另外，本类药物体外与 `source_id=SRC-0089; page=41; line=1144`
- `SFDUT1-TX-0156` treatment_or_prevention / p.43 / 氨基糖苷类: （1）作用与用途 用于治疗 $G^{-}$ 菌和 $G^{+}$ 敏感菌引起的败血症、呼吸道感染、胃肠道感染（包括腹膜炎）、泌尿生殖系统感染、乳腺炎、子宫炎及皮肤、软组织等严重感染。内服不吸收，用于肠道感染。主要用于猪巴氏杆菌病（猪肺疫）、仔猪白痢、猪链球菌病等的全身治疗。对于严重全身感染或大肠杆菌性、金黄色葡萄球菌性或链球菌性乳腺炎，本品可与青霉素、头孢菌素、地塞米松等联 `source_id=SRC-0089; page=43; line=1187`
- `SFDUT1-TX-0257` treatment_or_prevention / p.61 / 氟苯尼考: （5）传染性胸膜肺炎、副猪嗜血杆菌病、猪肺疫等的治疗：发病初期，患病猪群还有较好的食欲时，混饲给药时可适当提高添加量，每吨饲料可添加氟苯尼考（效价）100克，最好再配合强力霉素（效价）200克，连用7天，有较好效果。对传染性疾病引起的发热、咳嗽、气喘，单独使用抗菌药物即可，无需添加其他解热镇痛、止咳平喘类药物。如果病猪出现高热、不食，则要进行隔离治疗，使用氟苯尼考注射液肌内注射；若体温超过 $41^{\circ}\mathrm{C}$ 时，可配合解热镇痛药及地塞米松使用，效果更佳。 `source_id=SRC-0089; page=61; line=1560`
- `SFDUT1-TX-0419` treatment_or_prevention / p.93 / 地塞米松: 地塞米松（氟美松）是猪病治疗中常用的人工合成的含氟长效糖皮质激素（又称皮质甾体类激素），在肝内转化为氢化可的松，具有明显的抗炎、抗内毒素、抗过敏、抗休克、影响代谢等多种药理作用，临床上用于严重的细菌感染性疾病、过敏性疾病、休克、局部炎症等的综合治疗。 `source_id=SRC-0089; page=93; line=2297`
- `SFDUT1-TX-0420` treatment_or_prevention / p.93 / 地塞米松: 地塞米松是一把“双刃剑”，如果能够严格掌握适应证，使用得当，有良好疗效；否则，会发生不良反应和并发症。不少人对其药理作用缺乏全面深入了解，在猪病治疗中，将其当作“万金油”和“灵丹妙药”，滥用的现象很普遍，不仅一般感染时用，发热时用，甚至猪不吃食也用。滥用的后果常常干扰了治疗性诊断，使感染扩散、病情恶化、母猪死胎增多甚至流产。所以，要掌握地塞米松的基本知识，注意合理使用，走出滥用的诸多误区。 `source_id=SRC-0089; page=93; line=2299`
- `SFDUT1-TX-0434` dose_route_course / p.96 / 地塞米松: （1）一般常规用法及剂量 肌内或静脉注射：地塞米松磷酸钠注射液，一次量（以下指50千克体重猪的用量）， $4\sim 12$ 毫克，每天1次。疗程依病情而定，一般疗程限于 $3\sim 5$ 天。如果疗程超过5天，在第2个5天内应逐渐减量并停用。 `source_id=SRC-0089; page=96; line=2350`
- `SFDUT1-TX-0438` treatment_or_prevention / p.96 / 地塞米松: 必须与足量有效的抗菌药物配合使用，以免感染扩散和加重。治疗休克时，皮下和肌注吸收慢，应静脉注射给药。要求用 $5 \sim 10$ 倍于正常剂量的给药，治疗才会有效。在治疗与内毒素血症有关的急性乳腺炎时，静注地塞米松有利于抑制毒素在体内的循环及代谢。此外，要密切观察病情变化，在短期用药病情控制后即应迅速减量、停药，用药时间不宜长。 `source_id=SRC-0089; page=96; line=2361`
- `SFDUT1-TX-0439` candidate_fact / p.96 / 地塞米松: (4) 用于过敏性休克时应首选使用肾上腺素, 再合用地塞米松。 `source_id=SRC-0089; page=96; line=2369`
- `SFDUT1-TX-0440` treatment_or_prevention / p.96 / 地塞米松: 因地塞米松起效相对较慢。用于治疗失血和脱水等引起的休克时，只能在血容补充之后才能给予。 `source_id=SRC-0089; page=96; line=2371`
- `SFDUT1-TX-0441` vaccination_or_immunization / p.96 / 地塞米松: （6）在免疫抑制性病毒病普遍存在的今天，应用地塞米松尤要慎重。 `source_id=SRC-0089; page=96; line=2377`
- `SFDUT1-TX-0442` vaccination_or_immunization / p.96 / 地塞米松: 目前，不少猪场均存在着蓝耳病、2型圆环病毒感染、猪流感、猪瘟、猪伪狂犬病等免疫抑制性疾病，使用地塞米松更要慎重，不乏应用后病情恶化的病例。因为地塞米松无抗病毒作用，用后反而可降低抗体的防御能力，使病毒得以复制和增殖，病情反而加重。 `source_id=SRC-0089; page=96; line=2379`
- `SFDUT1-TX-0544` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （4）注射疫苗后必须观察15分钟 个别猪在注射疫苗后可能发生急性过敏反应，表现为不安、发抖、发绀、口吐泡沫、呕吐、呼吸困难、卧地不起等，应立即用肾上腺素、地塞米松等抗过敏药物紧急抢救。 `source_id=SRC-0089; page=120; line=2719`
- `SFDUT1-TX-0545` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （5）避免使用免疫抑制剂 不论是注射病毒苗还是细菌苗，也不论注射活苗或死苗，在免疫前后 $5 \sim 7$ 天都要避免使用影响疫苗免疫应答的药物和免疫抑制剂，如氟苯尼考、喹乙醇、磺胺类药、氨基糖苷类（如庆大霉素、卡那霉素）、四环素类及地塞米松等糖皮质激素，因它们对抗体的合成有一定抑制作用，或对T淋巴细胞、B淋巴细胞的转化有明显的抑制作用，从而影响免疫效果。 `source_id=SRC-0089; page=120; line=2720`
- `SFDUT1-TX-0640` vaccination_or_immunization / p.152 / 猪圆环病毒病: 采取病因治疗与对症治疗相结合的“标本兼治”的办法治疗。抗菌药物可选用枝原净、氟苯尼考、氟喹诺酮类、丁胺卡那霉素、庆大霉素、阿莫西林、氨苄西林、头孢类、磺胺类等肌注，并配合使用黄芪多糖、鱼腥草、双黄连等免疫增强剂、抗病毒药物及维生素 $\mathbf{B}_{1}$ 和维生素C等。高热者可配合使用安乃近、复方氨基比林等解热镇痛药。因为PCV-2病毒主要侵害猪的免疫系统，临床上尽可能不使用甲矾霉素、卡那霉素等免疫抑制作用的药物，除发生皮炎及肾病综合征外，也不宜使用地塞米松、氢化可的松等皮质激素类药物。也可采用血清疗法：采本场淘汰母猪血，分离血清， $3\sim 5$ 周龄，腹股沟皮下或腹腔注射5毫升，或 $2\sim 3$ 周龄、5周龄仔猪腹股沟注射 $5\sim 10$ 毫升。也可对发病猪进行治疗，每头病猪注射血清 $10\sim 20$ 毫升，隔日注射一次。 `source_id=SRC-0089; page=152; line=3171`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-066-dexamethasone.md`
- Candidate facts: 2
- Dose/route/course facts: 8
- Source anchors: 17

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 17 linked drug-use facts.
- Source pages: 201, 209, 210, 217, 240, 251, 256, 281, 282, 293, 294, 304, 306, 311.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0043` vaccination_or_immunization / p.201 / 副猪嗜血杆菌病: （4）本病临床治疗非常困难。在发病初期采用下列抗菌药物进行早期治疗，同时要“标本兼治”，病因疗法与对症疗法相结合，酌情配合解热镇痛药、地塞米松、维生素C、排疫苗、猪转移因子、干扰素以及黄芪多糖、复方柴胡、穿心莲、板蓝根、双黄连、鱼腥草等抗病毒及增强机体免疫力的注射剂等，有一定疗效，治愈率 $60\%$ 左右。如果治疗不及时，则疗效欠佳。 `source_id=SRC-0090; page=201; line=169`
- `SFDUT2-TX-0067` treatment_or_prevention / p.209 / 猪链球菌病: 松等作辅助治疗，效果更佳。地塞米松副作用小，有良好抗炎、抗过敏、抗休克、抗毒素、促进症状缓解及降温作用，临床上用于各种急性严重细菌性感染，以及由猪链球菌引起的脑膜炎等。 `source_id=SRC-0090; page=209; line=290`
- `SFDUT2-TX-0074` dose_route_course / p.210 / 猪链球菌病: 在酌情选用上述抗菌药物的同时，一定要配合使用消炎药地塞米松，5毫克/20千克体重，1次/天，用3天后，逐渐减量，不要骤停。 `source_id=SRC-0090; page=210; line=303`
- `SFDUT2-TX-0091` dose_route_course / p.217 / 猪传染性胸膜肺炎: （2）注意事项 据报道，本病对氨苄西林、链霉素、四环素已产生较强耐药性。在选用上述抗菌药物“治本”的同时，可配合使用地塞米松。地塞米松是控制严重肺炎的有效药物，按0.1毫克/千克体重，急重病例可适当加量，最大量0.2毫克/千克体重，2次/天。以每支1毫升（含5毫克）的地塞米松为例，50千克的猪可用2支，30千克的猪每次可用1支，其他依体重大小酌情增减。注意不可突然停药，用 $2\sim 4$ 天后逐渐减量，第 $5\sim 7$ 天停药。在使用地塞米松时，必须同时配合抗菌药物。如果体温达到 $40.5^{\circ}C$ 以上时，可酌情选用解热药“治标”。 $30\%$ 安乃近可按0.2毫克/千克体重； $10\%$ 复方氨基比林或安痛定，10千克体重可注2毫升；或复方柴胡注射液。为提高机体免疫力和抗病毒能力，可肌注复方黄芪多糖注射液，每10千克体重 $2\sim 3$ 毫升，1次/天，连用 $3\sim 5$ 天；或鱼腥草注射液。选用止咳药，如金蛤蟆咳喘针，0.2毫克/千克体重，1次/天，连用 $2\sim 3$ 天；或冰蟾熊胆注射液、咳嗽1号、强力喘康。平喘药如氨茶碱、麻黄素，或酌情选用板蓝根、双黄连等中药制剂。强心可用 `source_id=SRC-0090; page=217; line=390`
- `SFDUT2-TX-0151` treatment_or_prevention / p.240 / 仔猪副伤寒（猪沙门菌病）: (1) 个体治疗 注射抗菌药物, 如硫酸阿米卡星、庆大霉素、卡那霉素、氟喹诺酮类药物、复方新诺明、复方磺胺嘧啶钠注射液等。对病重猪可注射地塞米松, 以降低内毒素的作用; 也可灌服氟哌酸。 `source_id=SRC-0090; page=240; line=754`
- `SFDUT2-TX-0193` dose_route_course / p.251 / 仔猪渗出性皮炎: ① 肌注大剂量的青霉素类或头孢类药物，如注射用青霉素钠，5万单位/千克体重，2~3次/天；注射用氨苄西林钠，20毫克/千克体重，2~3次/天；注射用舒巴坦钠·氨苄西林钠，10毫克/千克体重，2次/天；阿莫西林·克拉维酸钾注射液，1毫升/10千克体重，1次/天；头孢噻呋钠，10毫克/千克体重，1次/天。如再配合地塞米松磷酸钠注射液，0.2毫克/千克体重，1次/天，效果更好。 `source_id=SRC-0090; page=251; line=944`
- `SFDUT2-TX-0194` dose_route_course / p.251 / 仔猪渗出性皮炎: ② 林可霉素注射液，15毫克/千克体重，早晚各肌注一次；中午肌注庆大霉素注射液，8毫克/千克体重；再配合地塞米松磷酸钠注射液，0.2毫克/千克体重，1次/天。 `source_id=SRC-0090; page=251; line=945`
- `SFDUT2-TX-0203` treatment_or_prevention / p.256 / 猪衣原体病: （6）脑炎 各年龄段的猪有时出现神经症状，表现兴奋、尖叫，盲目冲撞或转圈运动，倒地后四肢呈现游泳状划动，不久死亡。青霉素配合磺胺嘧啶钠（不能混合，要分别肌注）和地塞米松治疗有效。 `source_id=SRC-0090; page=256; line=1012`
- `SFDUT2-TX-0252` dose_route_course / p.281 / 产后泌乳障碍综合征: （3）糖皮质激素抗炎疗法 对严重的感染性疾病，在应用足量、有效抗菌药物的前提下，也可配合使用地塞米松作辅助治疗，肌注，一日量： $15\sim 20$ 毫克，利用其抗炎和抗毒素作用，以迅速缓解病情。使用时要注意，尽量应用较小剂量，病情控制后应减量或停药，用药时间不宜过长。 `source_id=SRC-0090; page=281; line=1407`
- `SFDUT2-TX-0259` treatment_or_prevention / p.282 / 产后泌乳障碍综合征: ① 病因不明时，常用的药物治疗方法为间隔12小时，重复使用抗生素 $+$ 催产素 $+$ 福乃达（或地塞米松）。 `source_id=SRC-0090; page=282; line=1429`
- `SFDUT2-TX-0284` compliance_or_safety / p.293 / 母猪产后泌尿生殖系统疾病: （3）糖皮质激素抗炎疗法 对严重的感染性疾病，在应用足量有效抗菌药物的前提下，也可配合使用地塞米松作辅助治疗，肌注一日量： $15\sim 20$ 毫克，利用其抗炎作用（缓解炎症局部的红肿、热、痛等症状）和抗毒素作用（能提高机体抗应激能力，对抗细菌内毒素对机体的损害，对感染毒血症的高热猪有退热作用），迅速缓解病情，度过危险期。此外，地塞米松对治疗乳房水肿也有效（孕猪禁用）。使用地塞米松时要注意，尽量应用较小剂量，病情控制后应减量或停药，用药时间不宜过长，大剂量连续用药超过1周时，应逐渐减量，缓慢停药，切不可突然停药，以免复发或出现肾上腺皮质机能不足。 `source_id=SRC-0090; page=293; line=1586`
- `SFDUT2-TX-0286` dose_route_course / p.294 / 母猪产后泌尿生殖系统疾病: 200万单位十地塞米松10毫克十催产素20单位，2次/天，连用 $3\sim$ 5天；b.环丙沙星10毫克/千克，1次/天，连用 $3\sim 5$ 天；c.氨苄西林20毫克/千克，2次/天，连用 $3\sim 5$ 天；d.注射用阿莫西林·克拉维酸钾7毫克/千克（以阿莫西林计），2次/天，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=294; line=1596`
- `SFDUT2-TX-0288` dose_route_course / p.294 / 母猪产后泌尿生殖系统疾病: ④ 对症疗法：病情严重有全身症状的，除用抗生素配合地塞米松的病因治疗外，还要强心补液，解除酸中毒、退烧等对症治疗。笔者试用下面验方效果较好： $2.5\%$ 氧氟沙星20毫升，地塞米松25毫克， $5\%$ 葡萄糖氯化钠注射液500毫升，混合静脉滴注，同时，每6小时外阴内侧注射催产素10单位，连用4次，可促使乳中病菌及毒素排出，提高疗效。并经常引导仔猪去拱母猪乳房并吸吮乳头。 `source_id=SRC-0090; page=294; line=1600`
- `SFDUT2-TX-0320` vaccination_or_immunization / p.304 / 猪呼吸道病综合征: ⑤ 免疫抑制因素 已知有许多可致免疫抑制的病原体，尤以病毒为主，如PRRSV、PCV-2、SIV、CFSV等。此外，饲料中的霉菌毒素，某些药物，如长期使用地塞米松、磺胺类药、氟苯尼考、卡那霉素等。 `source_id=SRC-0090; page=304; line=1743`
- `SFDUT2-TX-0330` candidate_fact / p.306 / 猪呼吸道病综合征: （7）必要时可再配合地塞米松、维生素C、维生素B、肌苷、三磷酸腺苷（ATP）、辅酶A等注射液，以增强机体抗毒素、抗休克、抗过敏功能。 `source_id=SRC-0090; page=306; line=1776`
- `SFDUT2-TX-0360` dose_route_course / p.311 / 猪疫苗过敏反应: （2）配合使用地塞米松 地塞米松能增强肾上腺素的作用，对于危重病例，在注射肾上腺素后，再配合肌注地塞米松磷酸钠注射液疗效更佳。每头用量：初生仔猪3毫克，5千克猪5毫克，10千克猪10毫克，25千克猪15毫克，50千克猪20毫克，100千克以上猪及种公、母猪30毫克。 `source_id=SRC-0090; page=311; line=1843`
- `SFDUT2-TX-0363` candidate_fact / p.311 / 猪疫苗过敏反应: （2）肾上腺素和地塞米松宜肌内注射而不要皮下注射，因肌内注射吸收快而完全，作用可立即显现；若皮下注射，因局部血管收缩而吸收较慢， $6\sim 15$ 分钟后才能起效，易错过最佳抢救时机。 `source_id=SRC-0090; page=311; line=1851`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_201_400_V14

- Original marker: `RAU_201_400_V14_START` / `RAU_201_400_V14_END`
- Original runtime page: `wiki/drugs/DRUG-066-dexamethasone.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 1

<!-- RAU_201_400_V14_START -->
## 兽药合理应用与联用手册（201-400页）增强 / SRC-0092

- 证据用途：系统用药、抗原虫/杀虫药、中药配伍、联用禁忌和对症支持边界。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺。

- `RAU2-DRUG-278-9314` 氢化可的松 / 肾上腺皮质激素 / p.278：Hydrocortisone 【药理作用及适应证】本品为天然皮质激素，有抗炎、抗过敏、抗毒素和抗休克等作用，此外也有一定的水钠潴留及排钾作用。静脉注射制剂显效快，可用于治疗严重的中毒性感染或其他危急病症。醋酸氢化可的松注射液（混悬液）肌内注射时吸收很少，作用较弱，因此，主要供关节或腱鞘内注射，治疗关节、腱鞘炎症。局部应用疗效较好，常用于牛乳腺炎、眼科炎症、皮肤过敏性炎症等的治疗。 `source_id=SRC-0092; page=278`
<!-- RAU_201_400_V14_END -->
