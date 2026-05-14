---
page_id: DRUG-023-gentamicin
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase3_drug_evidence_expansion
moved_from: wiki/drugs/DRUG-023-gentamicin.md
generated: 2026-05-09T11:42:41+08:00
---

# DRUG-023-gentamicin Evidence Expansion

This file stores detailed batch evidence moved out of the runtime drug page during Phase 3 cleanup.

Runtime rule:

- Do not load this file for default production/evaluation retrieval.
- Load it only for evidence expansion, audit, source lookup, or manual review.
- Dose, route, course, withdrawal period, MRL, residue, and food-safety claims still require current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-023-gentamicin.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 3

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 3 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 庆大霉素.
- Source pages: 29, 40, 89.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0034` 猪水肿病 / 处方2 `source_id=SRC-0087; page=29; line=1324-1360`
- `HANDBOOK-RX-0048` 猪丹毒 / 处方1 `source_id=SRC-0087; page=40; line=1664-1674`
- `HANDBOOK-RX-0212` 支气管炎 / 处方1 `source_id=SRC-0087; page=89; line=3843-3849`
<!-- HANDBOOK_RX_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-023-gentamicin.md`
- Candidate facts: 3
- Dose/route/course facts: 1
- Source anchors: 16

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 16 linked drug-use facts.
- Source pages: 13, 19, 37, 39, 40, 41, 43, 61, 82, 92, 120, 152.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0029` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （2）氨基糖苷类 氨基糖苷类与 $\beta$ -内酰胺类配伍应用有较好的协同作用。甲氧苄氨嘧啶（TMP）可增强本品的作用。氨基糖苷类可与多黏菌素类合用，但不可与氯霉素类合用。氨基糖苷类药物之间不可联合应用以免增强毒性，与碱性药物联合应用其抗菌效能可能增强，但毒性也会增大。链霉素与四环素合用，能增强对布氏杆菌的治疗作用。链霉素与红霉素合用，对猪链球菌病有较好的疗效。庆大霉素（或卡那霉素）可与喹诺酮药物合用。链霉素与磺胺类药物配伍应用会发生水解失效。硫酸新霉素一般口服给药，与阿托品类药物应用于仔猪腹泻。 `source_id=SRC-0089; page=13; line=589`
- `SFDUT1-TX-0057` treatment_or_prevention / p.19 / 治疗猪病要选择最适宜的给药方法: 消化道感染应以口服为主。大多数能在胃肠道吸收的药物也可采用口服给药。口服给药的优点是操作方便、安全，缺点是起效慢，剂量较大。此外，胃肠道不易吸收的磺胺脒、新霉素、庆大霉素、吡哌酸、黏杆菌素等也可口服，利用在肠道形成较高浓度的特点，治疗细菌性肠炎、仔猪黄白痢等。若治疗全身性感染疾病，如副猪嗜血杆菌病等以及危急病例，不宜口服而应注射。 `source_id=SRC-0089; page=19; line=713`
- `SFDUT1-TX-0136` treatment_or_prevention / p.37 / 氨基糖苷类: 氨基糖苷类（氨基环醇类）曾称氨基糖甙类，是由链霉菌或小单孢菌产生或经半合成制得的一类水溶性的碱性抗生素。由链霉菌产生的有链霉素、新霉素、卡那霉素等，由小单孢菌产生的有庆大霉素、小诺霉素等，半合成品有阿米卡星（丁胺卡那霉素）等。它们在化学结构、抗菌活性、药理特点和毒性方面具有共性。由于抗菌活性强，至今仍是对革兰阴性（ $\mathrm{G}^{-}$ ）菌严重感染唯一有效和不可缺少的药物，在兽医临床上被广泛使用，在防治猪传染病方面发挥了重要作用。 `source_id=SRC-0089; page=37; line=1050`
- `SFDUT1-TX-0141` treatment_or_prevention / p.39 / 氨基糖苷类: 由于脂溶性差，正常的胃肠道内服很难吸收（但肠炎时可有效地增加吸收），肠道内浓度较高，可作为肠道感染用药。口服庆大霉素或新霉素与阿托品、茛菪碱等药物合用，治疗仔猪白痢及腹泻效果好。 `source_id=SRC-0089; page=39; line=1092`
- `SFDUT1-TX-0144` candidate_fact / p.40 / 氨基糖苷类: 本类抗生素主要经肾排泄，肾皮质药物浓度可超过血药浓度 $10 \sim 50$ 倍，肾皮质内药物蓄积浓度越高，对肾毒性越大，其损害程度与剂量大小及疗程长短呈正比。主要损害近曲小管上皮细胞，表现为蛋白尿、血尿、尿频，严重时出现肾功能减退甚至无尿，肾毒性的早期变化或证据能在 $3 \sim 5$ 天内被发现，更明显的体征要在 $7 \sim 10$ 天内才能出现。为此，应尽量避免与肾毒性药物（如本类药物之间及多黏菌素、杆菌肽等）合用，同时应给病猪足量饮水。常用剂量下，各类损害发生率依次为：新霉素 $>$ 卡那霉素 $>$ 庆大霉素 $=$ 阿米卡星 $>$ 链霉素 $>$ 小诺霉素。 `source_id=SRC-0089; page=40; line=1116`
- `SFDUT1-TX-0147` vaccination_or_immunization / p.41 / 氨基糖苷类: 作为“繁殖期杀菌剂”的青霉素类、头孢菌素类，能破坏细菌细胞壁，有利于“静止期杀菌剂”的氨基糖苷类抗生素进入细胞体内而发挥杀菌作用，是处理混合感染、危重感染、免疫抑制感染以及致病菌不明感染联合用药的常用品种。常用的有：庆大霉素、卡那霉素、链霉素等与青霉素、氨苄西林钠、阿莫西林、头孢噻呋、头孢喹肟等联用，相互协同，增强疗效。如青霉素+庆大霉素+地塞米松治疗猪链球菌病、猪急性乳腺炎以及敏感细菌混合感染的疗效较高；氨基糖苷类与青霉素或氨苄西林联用治疗猪李氏杆菌病，与头孢菌素类联用治疗肺炎杆菌；庆大霉素与阿莫西林联用治疗铜绿假单胞菌等。但用药剂量应基本平衡，过大剂量的青霉素或其他半合成青霉素均可使氨基糖苷类活性降低。另外，本类药物体外与 `source_id=SRC-0089; page=41; line=1144`
- `SFDUT1-TX-0148` candidate_fact / p.41 / 氨基糖苷类: $\beta$ -内酰胺类抗生素配伍时可使前者灭活，因此不宜与含有青霉素类、头孢菌素类抗生素的溶液混合应用。切记，联用不等于可以混合注射，如庆大霉素在静脉输液中与阿莫西林混合，则会使庆大霉素血浓度显著降低而减效，尤其是对肾病严重的病猪，这可能是因为氨基糖苷类的氨基与 $\beta$ -内酰胺环之间形成无生物活性的酰胺，使庆大霉素被灭活。可分别肌注，或庆大霉素肌注，阿莫西林静注。 `source_id=SRC-0089; page=41; line=1146`
- `SFDUT1-TX-0149` drug_interaction / p.41 / 氨基糖苷类: TMP抗菌谱较广，抗菌作用较强，对多数 $\mathbf{G}^{+}$ 菌和 $\mathbf{G}^{-}$ 菌均有抗菌作用，以 $1:5$ 与某些抗生素配伍合用，如 $\mathrm{TMP}+$ 庆大霉素、 $\mathrm{TMP}+$ 阿米卡星有明显协同作用，既可拓展抗菌谱，减少耐药菌株产生，又可降低两者用量，提高疗效。 `source_id=SRC-0089; page=41; line=1150`
- `SFDUT1-TX-0150` drug_interaction / p.41 / 氨基糖苷类: 本类抗生素对肾脏及第8对脑神经都具有不同程度的毒性及神经肌内阻滞作用。如果用庆大霉素，就不能再同时联用卡那霉素或阿米卡星或链霉素等，只能用本类抗生素中的一种，但可以与没有药理性配伍禁忌的其他类抗生素或抗菌药联用。 `source_id=SRC-0089; page=41; line=1158`
- `SFDUT1-TX-0157` dose_route_course / p.43 / 氨基糖苷类: （2）制剂及用法用量 硫酸庆大霉素可溶性粉（片）、硫酸庆大霉素注射液。本品效价以质量计算，1克（1000毫克）等于100万单位，1毫克 $= 0.1$ 万单位。内服，一次量，每千克体重仔猪5毫克，2次/天。肌注，一次量，每千克体重 $2\sim 4$ 毫克（0.2万～0.4万单位），2次/天；或每千克体重 $4\sim 8$ 毫克，1次/天，连用 $2\sim 3$ 天。 `source_id=SRC-0089; page=43; line=1191`
- `SFDUT1-TX-0160` treatment_or_prevention / p.43 / 氨基糖苷类: （1）作用与用途 主要用于各种敏感菌引起的菌血症、败血症、呼吸道感染、腹膜炎以及各种感染。尤其适用于 $\mathbf{G}^{-}$ 杆菌中对卡那霉素、庆大霉素或其他氨基糖苷类耐药菌株所引起的感染。也可子宫灌注，治疗子宫内膜炎和子宫蓄脓。 `source_id=SRC-0089; page=43; line=1200`
- `SFDUT1-TX-0256` candidate_fact / p.61 / 氟苯尼考: （3）本品不能与磺胺嘧啶钠混合肌注。口服或肌注给药时忌与碱性药物合用，以免分解失效。也不宜与盐酸四环素、卡那霉素、庆大霉素、三磷酸腺苷、辅酶A等混合注射，以免发生沉淀和降效。 `source_id=SRC-0089; page=61; line=1558`
- `SFDUT1-TX-0348` drug_interaction / p.82 / 氟喹诺酮类药物: 这是因为其结构不同于其他抗生素，抗菌作用独特，而且不受质粒传导耐药性影响。因此对某些多重耐药菌株或对其他抗菌药耐药的细菌仍具有较强的良好抗菌活性，也有利于与其他抗菌药物联合用药。对耐甲氧嘧啶/磺胺药的细菌、耐庆大霉素的铜绿假单胞菌、耐泰乐菌素或泰妙菌素的支原体等也有很好的疗效，且可用于支原体、衣原体、军团菌等在细胞内繁殖的病原体。 `source_id=SRC-0089; page=82; line=2022`
- `SFDUT1-TX-0417` treatment_or_prevention / p.92 / 口服补液盐: 对于由大肠杆菌、沙门菌、螺旋体等引起的腹泻，在使用口服补液盐对症疗法治“标”，赢得时间的同时，还要及时用庆大霉素、新霉素、痢菌净等抗菌药物治疗原发病，不要顾此失彼。 `source_id=SRC-0089; page=92; line=2289`
- `SFDUT1-TX-0545` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （5）避免使用免疫抑制剂 不论是注射病毒苗还是细菌苗，也不论注射活苗或死苗，在免疫前后 $5 \sim 7$ 天都要避免使用影响疫苗免疫应答的药物和免疫抑制剂，如氟苯尼考、喹乙醇、磺胺类药、氨基糖苷类（如庆大霉素、卡那霉素）、四环素类及地塞米松等糖皮质激素，因它们对抗体的合成有一定抑制作用，或对T淋巴细胞、B淋巴细胞的转化有明显的抑制作用，从而影响免疫效果。 `source_id=SRC-0089; page=120; line=2720`
- `SFDUT1-TX-0640` vaccination_or_immunization / p.152 / 猪圆环病毒病: 采取病因治疗与对症治疗相结合的“标本兼治”的办法治疗。抗菌药物可选用枝原净、氟苯尼考、氟喹诺酮类、丁胺卡那霉素、庆大霉素、阿莫西林、氨苄西林、头孢类、磺胺类等肌注，并配合使用黄芪多糖、鱼腥草、双黄连等免疫增强剂、抗病毒药物及维生素 $\mathbf{B}_{1}$ 和维生素C等。高热者可配合使用安乃近、复方氨基比林等解热镇痛药。因为PCV-2病毒主要侵害猪的免疫系统，临床上尽可能不使用甲矾霉素、卡那霉素等免疫抑制作用的药物，除发生皮炎及肾病综合征外，也不宜使用地塞米松、氢化可的松等皮质激素类药物。也可采用血清疗法：采本场淘汰母猪血，分离血清， $3\sim 5$ 周龄，腹股沟皮下或腹腔注射5毫升，或 $2\sim 3$ 周龄、5周龄仔猪腹股沟注射 $5\sim 10$ 毫升。也可对发病猪进行治疗，每头病猪注射血清 $10\sim 20$ 毫升，隔日注射一次。 `source_id=SRC-0089; page=152; line=3171`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-023-gentamicin.md`
- Candidate facts: 2
- Dose/route/course facts: 7
- Source anchors: 12

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 12 linked drug-use facts.
- Source pages: 201, 210, 216, 226, 240, 251, 280, 293, 294, 306.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0045` dose_route_course / p.201 / 副猪嗜血杆菌病: ② 庆大霉素注射液，4毫克/千克体重，2次/天；同时配合左氧氟沙星5毫克/千克体重，2次/天（或甲磺酸达氟沙星2.5毫克/千克体重，1次/天），连用 $4\sim 5$ 天。 `source_id=SRC-0090; page=201; line=171`
- `SFDUT2-TX-0070` dose_route_course / p.210 / 猪链球菌病: a. 早期可用大剂量青霉素类抗生素类，因大多数分离菌株对青霉素敏感。如青霉素5万～8万单位/千克体重，每天2～3次，连用3～5天；或氨苄西林10～15毫克/千克体重，2次/天，连用3～5天；或阿莫西林15～20毫克/千克体重，每天2次，连用3～5天。如果再联合应用庆大霉素4～5毫克/千克体重，2次/天，或丁胺卡那霉素（阿米卡星）10毫克/千克体重，2次/天，效果更佳。注意，不能用庆大霉素等稀释青霉素类，要分别肌注。 `source_id=SRC-0090; page=210; line=298`
- `SFDUT2-TX-0084` candidate_fact / p.216 / 猪传染性胸膜肺炎: （1）推荐注射用药方案 应选择对革兰阴性菌敏感的药物。首选药物是头孢噻呋（或头孢噻肟）和氟苯尼考。强力霉素、庆大霉素配合阿莫西林、恩诺沙星、磺胺六甲氧、泰妙菌素、阿奇霉素等可酌情选用。 `source_id=SRC-0090; page=216; line=379`
- `SFDUT2-TX-0088` dose_route_course / p.216 / 猪传染性胸膜肺炎: ④ 复方庆大霉素注射液（加有抗菌增效剂TMP)，4毫克/千克体重，2次/天，连用 $3\sim 5$ 天；同时配合阿莫西林，15毫克/千克体重，2次/天，连用 $3\sim 5$ 天。但不能用庆大霉素稀释阿莫西林，否则庆大霉素将减效。阿莫西林·克拉维酸亦可。 `source_id=SRC-0090; page=216; line=383`
- `SFDUT2-TX-0121` drug_interaction / p.226 / 猪大肠杆菌病: ④ 药物治疗 丁胺卡那霉素、头孢噻呋、恩诺沙星、吡哌酸、庆大霉素、新霉素、增效磺胺甲基异噁唑、安普霉素、痢菌净等均为敏感药物。但是，由于长期使用上述药物，大肠杆菌对其普遍产生较强的耐药性，有些菌株同时耐受多种药物。因此，为了提高药物治疗效果，应每隔一段时间（一年或半年）进行一次大肠杆菌药敏试验，掌握细菌药敏状态的变化，减少用药的盲目性。治疗时尽量联合用药，或 $2 \sim 3$ 个月轮换用药，既可提高疗效，又能减少耐药菌株的产生。 `source_id=SRC-0090; page=226; line=535`
- `SFDUT2-TX-0151` treatment_or_prevention / p.240 / 仔猪副伤寒（猪沙门菌病）: (1) 个体治疗 注射抗菌药物, 如硫酸阿米卡星、庆大霉素、卡那霉素、氟喹诺酮类药物、复方新诺明、复方磺胺嘧啶钠注射液等。对病重猪可注射地塞米松, 以降低内毒素的作用; 也可灌服氟哌酸。 `source_id=SRC-0090; page=240; line=754`
- `SFDUT2-TX-0194` dose_route_course / p.251 / 仔猪渗出性皮炎: ② 林可霉素注射液，15毫克/千克体重，早晚各肌注一次；中午肌注庆大霉素注射液，8毫克/千克体重；再配合地塞米松磷酸钠注射液，0.2毫克/千克体重，1次/天。 `source_id=SRC-0090; page=251; line=945`
- `SFDUT2-TX-0249` dose_route_course / p.280 / 产后泌乳障碍综合征: （1）抗菌药物疗法 对有临床症状的，由大肠杆菌等 $\mathbf{G}^{-}$ 菌和葡萄球菌、链球菌等 $\mathbf{G}^{+}$ 菌引起的乳腺炎、膀胱炎、肾盂肾炎、子宫内膜炎、产后败血症等患病母猪，应采用抗生素疗法。有条件的应做药敏试验。也可选用对 $\mathbf{G}^{+}$ 菌敏感的青霉素类、第4代头孢菌素——头孢喹诺、大环内酯类抗生素和对 $\mathbf{G}^{-}$ 菌敏感的氨基糖苷类，采用联合用药方式（如青霉素 $+$ 链霉素或青霉素 $+$ 庆大霉素）或使用广谱抗菌药物，如法国施维雅“新素易康”（长效土霉素）或氟喹诺酮类。每头用量：青霉素400万～600万单位，链霉素 `source_id=SRC-0090; page=280; line=1401`
- `SFDUT2-TX-0250` dose_route_course / p.280 / 产后泌乳障碍综合征: 200万～300万单位，法国施美芬（2.5%头孢喹诺）10～15毫升，4%庆大霉素10～20毫升，新素易康10～20毫升。氧氟沙星或恩诺沙星20毫升。对无明显临床症状的亚临床感染者，多由G-菌产生的内毒素引起，应首选庆大霉素。以上药物3～5天为一疗程。 `source_id=SRC-0090; page=280; line=1403`
- `SFDUT2-TX-0282` dose_route_course / p.293 / 母猪产后泌尿生殖系统疾病: 的氨基糖苷类抗生素，采用联合用药方式（如青霉素G+链霉素或青霉素G+庆大霉素）或使用广谱抗菌药物，如得米先（长效土霉素）或氟喹诺酮类。每头每次肌注用量：青霉素G400万单位，链霉素150万～200万单位， $4\%$ 庆大霉素 $10\sim 20$ 毫升，得米先 $10\sim$ 20毫升， $2.5\%$ 氧氟沙星或 $0.5\%$ 恩诺沙星20毫升，以上药物每天两次， $3\sim 5$ 天为一疗程。 `source_id=SRC-0090; page=293; line=1582`
- `SFDUT2-TX-0290` candidate_fact / p.294 / 母猪产后泌尿生殖系统疾病: ② 庆大霉素、青霉素G、头孢菌素类、大环内酯类、四环素类抗生素或氟苯尼考，连续肌注5天，有较好疗效。 `source_id=SRC-0090; page=294; line=1605`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-023-gentamicin.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-054-DRUG-023-gentamicin-md-1207` 庆大霉素 / 氨基糖苷类 / p.54：Gentamycin 【药理作用及适应证】体外抗菌活性在本类药物中最强，对大多数需氧革兰阴性菌均有较强杀菌作用，革兰阳性菌中对耐药金葡菌也有较强作用，对耐药的溶血性链球菌、炭疽杆菌等也有效果；对支原体有一定作用；对结核杆菌、真菌、阿米巴原虫无效。主要用于敏感菌所致呼吸道、肠道、泌尿道感染和败血症等。细菌耐药性维持时间较短，停药后易恢复敏感。本品内服和子宫灌注极少吸收；肌内注射吸收迅速而完全；皮下注射血药浓度达峰较肌注慢；局部冲洗经体表吸收一定量；新生仔畜及肾功能障碍患畜排泄显著减慢。发热使本品血药浓度降低，贫血使血药浓度升高。 `source_id=SRC-0091; page=54`
<!-- RAU_1_200_V14_END -->
