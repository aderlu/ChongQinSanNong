---
page_id: DRUG-010-amoxicillin
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase6_drug_page_compaction
moved_from: wiki/drugs/DRUG-010-amoxicillin.md
generated: 2026-05-09T14:25:31+08:00
---

# DRUG-010-amoxicillin Phase 6 Evidence Expansion

This file stores high-density batch evidence moved out of the default runtime drug page during Phase 6.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any treatment parameter, withdrawal-period, MRL, residue, or food-safety conclusion still requires current label/regulatory verification.

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-010-amoxicillin.md`
- Byte size moved: 4749
- Fact-like rows moved: 18
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 18

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 13 appendix medicine rows and 5 text treatment mentions linked to this drug page.
- Source pages: 46, 72, 107, 112, 123, 152, 153, 154, 155, 156.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0023` Aloxycare Injection (150 mg amoxicillin/ml): dose=1 ml/21 kg im daily; meat_withhold=16 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0024` Aloxycare LA Injection (150 mg amoxicillin/ml): dose=1 ml/10 kg im every 2 days; meat_withhold=16 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0025` Aloxypen Injection (150 mg amoxicillin/ml): dose=1 ml/20 kg im daily; meat_withhold=16 days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0026` Aloxypen LA (150 mg amoxicillin/ml): dose=1 ml/10 kg im daily; meat_withhold=16 days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0030` Betamox Injection (150 mg amoxicillin/ml): dose=1 ml/21 kg im daily; meat_withhold=16 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0031` Betamox LA (150 mg amoxicillin/ml): dose=1 ml/10 kg im every 2 days; meat_withhold=16 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0035` Clamoxyl Ready-to-Use Injection (150 mg amoxicillin/ml): dose=1 ml/20 kg im daily; meat_withhold=47 days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0045` Duphamox (150 mg amoxicillin/ml): dose=1 ml/21 kg im daily; meat_withhold=16 days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0046` Duphamox LA (150 mg amoxicillin/ml): dose=1 ml/10 kg im as a single injection; meat_withhold=21 days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0088` Synulox Ready-To-Use Suspension for Injection (35 mg clavulanic acid + 140 mg amoxicillin per ml): dose=1 ml/20 kg im daily; meat_withhold=31 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0100` Amoxinsol 50 (50% w/w amoxicillin trihydrate): dose=20 mg/kg in drinking water for 5 days; meat_withhold=2 days. `source_id=SRC-0088; page=156; table=Table A.3.`
- `VTOP-MED-0109` Octacillin 697 mg/g Powder for Use in Pigs (697 mg amoxicillin/g): dose=14 mg/kg in drinking water for 3–5 days; meat_withhold=2 days. `source_id=SRC-0088; page=155; table=Table A.3.`
- `VTOP-MED-0115` Stabox 50% Oral Soluble Powder for Pigs (500 mg amoxicillin/g): dose=20 mg/kg in liquid feed for 5 days; meat_withhold=14 days. `source_id=SRC-0088; page=155; table=Table A.3.`
- `VTOP-TX-0097` treatment_candidate / p.72 / Escherichia coli diarrhoea: Once pigs show neurological signs, there is little hope of recovery. Antibiotics such as amoxicillin will help, if given promptly prior to neurological signs. The remaining pigs should be given a less nutritious diet. `source_id=SRC-0088; page=72; line=1998`
- `VTOP-TX-0134` vaccination / p.46 / Atrophic rhinitis: amoxicillin, enrofloxacin and oxytetracycline. A good control measure is to treat litters of baby pigs with injections of trimethoprim sulfonamide on days 3, 10 and 21. Sows should be vaccinated twice in pregnancy, ideally 5 and 2 weeks before farrowing. Some vaccines are licensed for piglets to be given at 1 and 3 weeks of age. `source_id=SRC-0088; page=46; line=2248`
- `VTOP-TX-0209` dose_or_route / p.107 / Streptococcal meningitis: after weaning; in fact at any stage if the disease is a problem. If water medication is required in pigs after weaning the author’s preference is amoxicillin. Other authorities advise tilmicosin. This antibiotic can also be given in-feed. The author’s preference for in-feed medication is procaine penicillin at $3 0 0 \mathrm { g / t }$ . `source_id=SRC-0088; page=107; line=2885`
- `VTOP-TX-0220` treatment_candidate / p.112 / Greasy pig disease: tips. The organism may be grown in pure culture from swabs taken before treatment. Parenteral antibiotics with topical disinfectant washes are effective treatment. Normally clinicians use amoxicillin with or without clavulinic acid. Dilute chlorohexidine or dilute povidone iodine solutions may be made up into clean plastic dustbins. Piglets may then be totally dipped in the solution before being put on clean shavings `source_id=SRC-0088; page=112; line=3022`
- `VTOP-TX-0261` vaccination / p.123 / Swine Erysipelas: In acute outbreaks of erysipelas in growing pigs the recommended preventive treatment is amoxicillin in the water. This should only be used as an emergency treatment while vaccination is being carried out. `source_id=SRC-0088; page=123; line=3313`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-010-amoxicillin.md`
- Byte size moved: 9739
- Fact-like rows moved: 12
- Candidate fact mentions moved: 3
- Dose/route/course fact markers moved: 1
- Source anchors moved: 12

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 12 linked drug-use facts.
- Source pages: 22, 28, 31, 34, 41, 61, 151, 152, 172, 188.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0073` treatment_or_prevention / p.22 / 要提前预见药物的疗效和不良反应: 药物的作用或效应取决于作用部位的浓度，无论以何种途径给药，药物在动物体内均要发生吸收、分布、生物转化和排泄的动力学过程。每种药物有其特定的药动学特征，如半衰期、生物利用率、表观分布容积等都有所差异。其动力学特征还受疾病类型及过程影响。只有熟悉药物的动力学特征及其影响因素，才能做到正确选药并制定科学、合理的给药方案，达到预期的治疗效果。例如，阿莫西林与氨苄西林的体外抗菌活性很相似，但前者的生物利用率比后者高1倍，血清浓度高 $1.5 \sim 3$ 倍，在治疗全身性感染时，选用阿莫西林的疗效比氨苄西林好；但在胃肠道感染时，因氨苄西林不易吸收，在胃肠道能保持较高的药物浓度，治疗效果较好。 `source_id=SRC-0089; page=22; line=772`
- `SFDUT1-TX-0110` dose_route_course / p.31 / 肆霉素类: （2）用法与用量 以阿莫西林计。内服，一次量，每千克体重20毫克，2次/天，连用5天。猪混饲，每吨饲料 $200\sim 300$ 克，连续用药 $5\sim 10$ 天。 `source_id=SRC-0089; page=31; line=928`
- `SFDUT1-TX-0114` drug_interaction / p.31 / 肆霉素类: （3）注意事项 阿莫西林与喹诺酮类、氨基糖苷类抗菌药物联合应用，有协同或相加作用。但与四环素类、氟苯尼考、大环内酯类及林可霉素联用，可能发生拮抗作用。其他参见注射用氨苄西林钠。 `source_id=SRC-0089; page=31; line=938`
- `SFDUT1-TX-0116` treatment_or_prevention / p.28 / 头孢菌素类: 第一代头孢菌素的抗菌谱与广谱青霉素（氨苄西林、阿莫西林）相似。虽对青霉素酶稳定，但仍可被多数 $\mathbf{G}^{-}$ 菌产生的 $\beta$ 内酰胺酶所分解。因此，主要用于革兰阳性（ $\mathbf{G}^{+}$ ）菌（链球菌、产酶葡萄球菌等）和少数 $\mathbf{G}^{-}$ 菌（大肠杆菌、嗜血杆菌、沙门菌等）的感染治疗。常用的有注射用头孢噻吩（先锋霉素I）、头孢唑啉（头孢霉素V）以及内服用的头孢氨苄（先锋霉素IV）、头孢拉定（VI）、头孢羟氨苄等，需要注意的是，该类产品对肾脏毒性较大。 `source_id=SRC-0089; page=28; line=948`
- `SFDUT1-TX-0119` candidate_fact / p.34 / 头孢菌素类: （1）作用与用途 本品为半合成的第三代动物专用头孢菌素，具有广谱杀菌作用。一些研究者所做的头孢噻呋对兽医临床分离的数千株病原菌的抑菌实验结果表明，本药是抗菌活性最强的药物之一。对 $\mathbf{G}^{+}$ 菌、 $\mathbf{G}^{-}$ 菌（包括产 $\beta$ 内酰胺酶菌）及一些厌氧菌均有效。敏感菌主要有多杀性巴氏杆菌、溶血性巴氏杆菌、胸膜肺炎放线杆菌、副猪嗜血杆菌、大肠杆菌、沙门菌、链球菌、葡萄球菌等，但支气管败血波氏杆菌、某些铜绿假单胞菌、肠球菌、衣原体耐药。本品抗菌活性比氨苄西林强，对链球菌的活性比氟喹诺酮类强。兽医临床主要用于 $\mathbf{G}^{+}$ 和 $\mathbf{G}^{-}$ 菌感染，如猪胸膜肺炎放线杆菌、副猪嗜血杆菌、多杀性巴氏杆菌、大肠杆菌、猪霍乱沙门菌及链球菌等引起的感染及呼吸道病（猪细菌性肺炎）。注射本品后，15分钟内可迅速被吸收，并有消除半衰期长的特点，对传染性胸膜肺炎及副猪嗜血杆菌病的疗效较阿莫西林、林可霉素-大观霉素（利高霉素）显著，建议首选。 `source_id=SRC-0089; page=34; line=974`
- `SFDUT1-TX-0147` vaccination_or_immunization / p.41 / 氨基糖苷类: 作为“繁殖期杀菌剂”的青霉素类、头孢菌素类，能破坏细菌细胞壁，有利于“静止期杀菌剂”的氨基糖苷类抗生素进入细胞体内而发挥杀菌作用，是处理混合感染、危重感染、免疫抑制感染以及致病菌不明感染联合用药的常用品种。常用的有：庆大霉素、卡那霉素、链霉素等与青霉素、氨苄西林钠、阿莫西林、头孢噻呋、头孢喹肟等联用，相互协同，增强疗效。如青霉素+庆大霉素+地塞米松治疗猪链球菌病、猪急性乳腺炎以及敏感细菌混合感染的疗效较高；氨基糖苷类与青霉素或氨苄西林联用治疗猪李氏杆菌病，与头孢菌素类联用治疗肺炎杆菌；庆大霉素与阿莫西林联用治疗铜绿假单胞菌等。但用药剂量应基本平衡，过大剂量的青霉素或其他半合成青霉素均可使氨基糖苷类活性降低。另外，本类药物体外与 `source_id=SRC-0089; page=41; line=1144`
- `SFDUT1-TX-0148` candidate_fact / p.41 / 氨基糖苷类: $\beta$ -内酰胺类抗生素配伍时可使前者灭活，因此不宜与含有青霉素类、头孢菌素类抗生素的溶液混合应用。切记，联用不等于可以混合注射，如庆大霉素在静脉输液中与阿莫西林混合，则会使庆大霉素血浓度显著降低而减效，尤其是对肾病严重的病猪，这可能是因为氨基糖苷类的氨基与 $\beta$ -内酰胺环之间形成无生物活性的酰胺，使庆大霉素被灭活。可分别肌注，或庆大霉素肌注，阿莫西林静注。 `source_id=SRC-0089; page=41; line=1146`
- `SFDUT1-TX-0258` treatment_or_prevention / p.61 / 氟苯尼考: （6）在防治呼吸道病综合征（PRDC）方面，有的厂家推荐氟苯尼考与阿莫西林或泰乐菌素或泰妙菌素合用，笔者认为此法欠妥。因为从药理学的角度讲，两者不可联用。但氟苯尼考可与四环 `source_id=SRC-0089; page=61; line=1561`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
- `SFDUT1-TX-0640` vaccination_or_immunization / p.152 / 猪圆环病毒病: 采取病因治疗与对症治疗相结合的“标本兼治”的办法治疗。抗菌药物可选用枝原净、氟苯尼考、氟喹诺酮类、丁胺卡那霉素、庆大霉素、阿莫西林、氨苄西林、头孢类、磺胺类等肌注，并配合使用黄芪多糖、鱼腥草、双黄连等免疫增强剂、抗病毒药物及维生素 $\mathbf{B}_{1}$ 和维生素C等。高热者可配合使用安乃近、复方氨基比林等解热镇痛药。因为PCV-2病毒主要侵害猪的免疫系统，临床上尽可能不使用甲矾霉素、卡那霉素等免疫抑制作用的药物，除发生皮炎及肾病综合征外，也不宜使用地塞米松、氢化可的松等皮质激素类药物。也可采用血清疗法：采本场淘汰母猪血，分离血清， $3\sim 5$ 周龄，腹股沟皮下或腹腔注射5毫升，或 $2\sim 3$ 周龄、5周龄仔猪腹股沟注射 $5\sim 10$ 毫升。也可对发病猪进行治疗，每头病猪注射血清 $10\sim 20$ 毫升，隔日注射一次。 `source_id=SRC-0089; page=152; line=3171`
- `SFDUT1-TX-0685` treatment_or_prevention / p.172 / 猪流行性感冒: （7）在改善饲养管理基础上，积极做好病猪的治疗工作。发病时一般用柴胡、复方氨基比林、安乃近或对乙酰氨基酚注射液等解热镇痛药对症疗法以减轻症状和使用抗生素或磺胺类药物防控继发感染，如饲料添加阿莫西林、金霉素、氟苯尼考等，也可添加黄芪多糖和电解多维。还可采用中药方剂治疗。治疗人流感常用的抗病毒药物，对猪流感病毒也有较好的良效。在加强护理基础上进行对症治疗，才能收到好的效果。 `source_id=SRC-0089; page=172; line=3509`
- `SFDUT1-TX-0722` treatment_or_prevention / p.188 / 猪巴氏杆菌病: 个体治疗可选用第3代头孢菌素类和氟喹诺酮类，这是目前治疗本病最有效的药物。也可酌情选用氨基糖苷类、氨苄西林、阿莫西林、氟苯尼考、长效土霉素、强力霉素、磺胺类药物。预防用药可在饲料中添加选用氟苯尼考、泰乐菌素与磺胺二甲嘧啶联用等都有较好疗效。治疗时一般采用交叉用药，用药前尽可能先做药敏试验而后选用最敏感的药物。 `source_id=SRC-0089; page=188; line=3740`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-010-amoxicillin.md`
- Byte size moved: 8457
- Fact-like rows moved: 16
- Candidate fact mentions moved: 5
- Dose/route/course fact markers moved: 8
- Source anchors moved: 16

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 16 linked drug-use facts.
- Source pages: 194, 199, 201, 202, 210, 216, 217, 218, 222, 251, 294, 295, 306.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0017` treatment_or_prevention / p.194 / 猪支原体肺炎: 因猪肺炎支原体没有细胞壁，因此通过干扰细胞壁合成发挥抗菌作用的青霉素、氨苄西林、阿莫西林和头孢菌素对单纯的支原体肺炎治疗无效，其他抗菌药物如甲氧氨苄和磺胺类药物、多黏菌素、链霉素、红霉素对猪支原体肺炎的治疗也不起作用。 `source_id=SRC-0090; page=194; line=65`
- `SFDUT2-TX-0036` candidate_fact / p.199 / 副猪嗜血杆菌病: （2）亚急性型或慢急性型 常由急性型转化而来或由中等毒力毒株引起，主要表现为多发性浆膜炎、关节炎、脑膜炎等。病猪食欲下降、精神沉郁、发抖、扎堆、咳嗽、呼吸困难、被毛粗乱、渐进性消瘦、体表皮肤苍白；行动迟缓僵硬，后肢不协调；四肢无力，不愿站立；关节肿大或跛行。副猪嗜血杆菌性脑膜炎的症状，除共济失调、步伐蹒跚、头向后仰、四肢呈游泳状以外，笔者还观察到一种特殊表现：喜欢向同一侧躺卧，将猪翻过来它又很快便自动翻回去，可反复数次（可用复方磺胺间甲氧嘧啶配合阿莫西林或氨苄西林分别肌注，效果较好）。慢急性型有的可拖10多天后终因衰竭而死。侥幸不死的极度消瘦或生长缓慢。 `source_id=SRC-0090; page=199; line=137`
- `SFDUT2-TX-0046` dose_route_course / p.201 / 副猪嗜血杆菌病: ③ 阿莫西林，15毫克/千克体重，2次/天，连用 $4 \sim 5$ 天（也可选用：氨苄西林/舒巴坦，20毫克/千克体重，2次/天，连用 $4 \sim 5$ 天；或青霉素G，5万单位/千克体重， $2 \sim 3$ 次/天，连用 $4 \sim 5$ 天）。或氨苄西林 $10 \sim 20$ 毫克/千克体重， $2 \sim 3$ 次/天，连用 $2 \sim 3$ 天。 `source_id=SRC-0090; page=201; line=172`
- `SFDUT2-TX-0054` treatment_or_prevention / p.202 / 副猪嗜血杆菌病: （6）在日粮或饮水中添加药物进行预防，并要科学用药 本病在严重暴发时，使用药物预防可能无效。为此，应摸清本病在本场的发病规律，应在发病前3周提前对整个猪群进行药物预防。有条件的最好能做药敏测验，采用敏感药物，但用药量不可过少，防止产生耐药性，或在全群的饮水中添加阿莫西林或强力霉素。 `source_id=SRC-0090; page=202; line=191`
- `SFDUT2-TX-0070` dose_route_course / p.210 / 猪链球菌病: a. 早期可用大剂量青霉素类抗生素类，因大多数分离菌株对青霉素敏感。如青霉素5万～8万单位/千克体重，每天2～3次，连用3～5天；或氨苄西林10～15毫克/千克体重，2次/天，连用3～5天；或阿莫西林15～20毫克/千克体重，每天2次，连用3～5天。如果再联合应用庆大霉素4～5毫克/千克体重，2次/天，或丁胺卡那霉素（阿米卡星）10毫克/千克体重，2次/天，效果更佳。注意，不能用庆大霉素等稀释青霉素类，要分别肌注。 `source_id=SRC-0090; page=210; line=298`
- `SFDUT2-TX-0077` dose_route_course / p.210 / 猪链球菌病: （4）策略式使用抗菌药物 从断奶至断奶后6周的时间段内，确定暴发时间，在此之前 $2\sim 3$ 天通过饲料或饮水进行预防性用药，可在每吨饲料中添加 $70\%$ 阿莫西林300克，或在每升饮水中添加200毫克，连用 $7\sim 10$ 天。在有蓝耳病等病毒病的猪场，更应做好链球菌的防控。同时要妥善处理脓汁，防止污染环境，扩大传播。 `source_id=SRC-0090; page=210; line=316`
- `SFDUT2-TX-0084` candidate_fact / p.216 / 猪传染性胸膜肺炎: （1）推荐注射用药方案 应选择对革兰阴性菌敏感的药物。首选药物是头孢噻呋（或头孢噻肟）和氟苯尼考。强力霉素、庆大霉素配合阿莫西林、恩诺沙星、磺胺六甲氧、泰妙菌素、阿奇霉素等可酌情选用。 `source_id=SRC-0090; page=216; line=379`
- `SFDUT2-TX-0088` dose_route_course / p.216 / 猪传染性胸膜肺炎: ④ 复方庆大霉素注射液（加有抗菌增效剂TMP)，4毫克/千克体重，2次/天，连用 $3\sim 5$ 天；同时配合阿莫西林，15毫克/千克体重，2次/天，连用 $3\sim 5$ 天。但不能用庆大霉素稀释阿莫西林，否则庆大霉素将减效。阿莫西林·克拉维酸亦可。 `source_id=SRC-0090; page=216; line=383`
- `SFDUT2-TX-0095` candidate_fact / p.217 / 猪传染性胸膜肺炎: ③ 阿莫西林 $200 \sim 300$ 克（效价），连续使用7天，然后将剂量减半，再继续使用2周。 `source_id=SRC-0090; page=217; line=396`
- `SFDUT2-TX-0101` candidate_fact / p.218 / 猪传染性胸膜肺炎: ② 每100升饮水中添加阿莫西林（效价）15克，连续混饮5天。 `source_id=SRC-0090; page=218; line=405`
- `SFDUT2-TX-0110` dose_route_course / p.222 / 猪传染性萎缩性鼻炎: ③ 个体治疗 肌注，一次量：a. 磺胺类药物配合磺胺增效剂的复方制剂，如复方增效磺胺或复方磺胺嘧啶钠注射液，12.5毫克/千克体重；b. 长效土霉素注射液，20毫克/千克体重；c. 青霉素（4万单位/千克体重）配合卡那霉素（ $20\sim 30$ 毫克/千克体重）或氨苄西林（ $10\sim 20$ 毫克/千克体重）或阿莫西林（ $10\sim 20$ 毫克/千克体重）；d. 氟喹诺酮类注射液， $2.5\sim 5$ 毫克/千克体重；e. 头孢噻呋钠， $5\sim 10$ 毫克/千克体重；f. 仔猪打喷嚏时也可用卡那霉素注射液滴鼻，每天1次，每个鼻孔滴0.5毫升，连用 $2\sim 3$ 天。 `source_id=SRC-0090; page=222; line=470`
- `SFDUT2-TX-0192` candidate_fact / p.251 / 仔猪渗出性皮炎: ④ 对群发且症状较重的断奶仔猪，也可隔离集中饲养，局部进行外科处理，在料中加喂 $70\%$ 阿莫西林300克/吨，连用1周。 `source_id=SRC-0090; page=251; line=940`
- `SFDUT2-TX-0193` dose_route_course / p.251 / 仔猪渗出性皮炎: ① 肌注大剂量的青霉素类或头孢类药物，如注射用青霉素钠，5万单位/千克体重，2~3次/天；注射用氨苄西林钠，20毫克/千克体重，2~3次/天；注射用舒巴坦钠·氨苄西林钠，10毫克/千克体重，2次/天；阿莫西林·克拉维酸钾注射液，1毫升/10千克体重，1次/天；头孢噻呋钠，10毫克/千克体重，1次/天。如再配合地塞米松磷酸钠注射液，0.2毫克/千克体重，1次/天，效果更好。 `source_id=SRC-0090; page=251; line=944`
- `SFDUT2-TX-0286` dose_route_course / p.294 / 母猪产后泌尿生殖系统疾病: 200万单位十地塞米松10毫克十催产素20单位，2次/天，连用 $3\sim$ 5天；b.环丙沙星10毫克/千克，1次/天，连用 $3\sim 5$ 天；c.氨苄西林20毫克/千克，2次/天，连用 $3\sim 5$ 天；d.注射用阿莫西林·克拉维酸钾7毫克/千克（以阿莫西林计），2次/天，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=294; line=1596`
- `SFDUT2-TX-0291` dose_route_course / p.295 / 母猪产后泌尿生殖系统疾病: ② $5\%$ 碘酊 $5 \sim 10$ 毫升溶于 500 毫升生理盐水后灌入子宫冲洗（不要用高锰酸钾），冲洗后及时注射催产素 $20 \sim 30$ 单位，促进子宫炎性分泌物排出，最后用 $20 \sim 40$ 毫升注射用水稀释青霉素 G、链霉素各 200 万单位或强效阿莫西林 2 克，灌入子宫。 `source_id=SRC-0090; page=295; line=1609`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-010-amoxicillin.md`
- Byte size moved: 756
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-042-DRUG-010-amoxicillin-md-6946` 阿莫西林 / β-内酰胺/青霉素类 / p.42：目录定位显示 `阿莫西林` 属于 `β-内酰胺/青霉素类`，可作为药物召回、类别边界和联用禁忌复核入口。 `source_id=SRC-0091; page=42`
<!-- RAU_1_200_V14_END -->
