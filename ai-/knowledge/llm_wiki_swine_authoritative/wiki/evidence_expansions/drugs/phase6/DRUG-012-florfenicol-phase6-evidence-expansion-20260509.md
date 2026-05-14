---
page_id: DRUG-012-florfenicol
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase6_drug_page_compaction
moved_from: wiki/drugs/DRUG-012-florfenicol.md
generated: 2026-05-09T14:25:31+08:00
---

# DRUG-012-florfenicol Phase 6 Evidence Expansion

This file stores high-density batch evidence moved out of the default runtime drug page during Phase 6.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any treatment parameter, withdrawal-period, MRL, residue, or food-safety conclusion still requires current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-012-florfenicol.md`
- Byte size moved: 548
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 1 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 氟苯尼考.
- Source pages: 17.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0194` 胃肠炎 / 处方1 `source_id=SRC-0087; page=17; line=3554-3590`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-012-florfenicol.md`
- Byte size moved: 1985
- Fact-like rows moved: 7
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 7

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 7 appendix medicine rows and 0 text treatment mentions linked to this drug page.
- Source pages: 26, 154, 155, 156.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0061` Fenflor 300 mg/ml Solution for Injection for Pigs (300 mg florfenicol/ml): dose=1 ml/20 kg im every 48 h; meat_withhold=18 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0064` Florkem Fosfomycin (300 mg florfenicol/ml This antibiotic is not licensed for use in pigs in the UK. However in other countries it has been found to be a useful antibiotic in respiratory disease): dose=1 ml/20 kg im every 48 h The dose of calcium fosfomycin is 30 mg/kg; meat_withhold=18 42 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0066` Kefloril 300 mg/ml Lincocin Sterile Solution Lincojet 10% (300 mg florfenicol/ml 100 mg lincomycin/ml 100 mg lincomycin/ml): dose=1 ml/20 kg im every 48 h 1 ml/9–22 kg im daily 1 ml/9–22 kg im daily; meat_withhold=18 3 3 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0077` Nuflor Swine 300 mg/ml Solution for Injection (300 mg florfenicol/ml): dose=1 ml/20 kg im every 48 h; meat_withhold=18 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0086` Selectan (300 mg florfenicol/ml): dose=1 ml/20 kg im every 48 h; meat_withhold=18 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0108` Nuflor Drinking Water Concentrate for Swine (23 mg florfenicol/ml): dose=10 mg/kg in drinking water for 5 days; meat_withhold=20 days. `source_id=SRC-0088; page=26; table=Table A.3.`
- `VTOP-MED-0112` Selectan Oral (23 mg florfenicol/g): dose=10 mg/kg daily for 5 days; meat_withhold=20 days. `source_id=SRC-0088; page=156; table=Table A.3.`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-012-florfenicol.md`
- Byte size moved: 17065
- Fact-like rows moved: 25
- Candidate fact mentions moved: 4
- Dose/route/course fact markers moved: 5
- Source anchors moved: 25

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 25 linked drug-use facts.
- Source pages: 11, 27, 31, 36, 38, 45, 47, 52, 53, 55, 57, 58, 61, 73, 87, 120, 145, 151, 152, 172, 188.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0023` dose_route_course / p.11 / 兽药使用必须遵循的基本原则: 不同的疾病使用不同的药物，同一种疾病也不能长期使用某一种药物治疗。当发生某种疾病时，要根据流行病学、临床症状、解剖变化、实验室检验结果等综合分析，做出准确的诊断，然后有针对性地选择药物，所选药物要安全、可靠、方便、价廉，达到“药半功倍”的效果，彻底杜绝不明病情而滥用药物，特别是抗菌药物。例如对发生传染性胸膜肺炎的猪，选用氟苯尼考、青霉素、氨苄西林、四环素等治疗有良好效果。对于诸如亚硝酸盐中毒可用特效解毒药小剂量美蓝（亚甲蓝）进行解毒，注射 $1\%$ 美蓝溶液，猪 $1\sim 2$ 毫克/千克体重。有机磷中毒可使用阿托品结合解磷定进行解毒。 `source_id=SRC-0089; page=11; line=566`
- `SFDUT1-TX-0092` treatment_or_prevention / p.27 / 肆霉素类: 其作用机理主要是干扰转肽酶、破坏细菌细胞壁的合成而产生杀菌作用。它能抑制细菌细胞壁的基础成分黏肽的合成，造成细胞壁缺损而失去屏障保护作用，使水分渗入细菌胞浆，导致菌体肿胀、变形，最后裂解而死亡。 $\mathrm{G}^{+}$ 菌的细胞壁主要由黏肽（达 $65\% \sim 95\%$ ）组成，而 $\mathrm{G}^{-}$ 菌细胞壁的主要成分是磷脂（黏肽仅占 $1\% \sim 10\%$ ），由于 $\mathrm{G}^{+}$ 菌的细胞壁黏肽含量较 $\mathrm{G}^{-}$ 菌高，故对 $\mathrm{G}^{+}$ 菌作用很强，而对 $\mathrm{G}^{-}$ 菌作用较弱。另外，生长期的敏感菌分裂旺盛，细胞壁处于生物合成期，在青霉素的作用下，黏肽的合成受阻不能形成细胞壁，在渗透压作用下，导致细胞膜破裂而死亡，这一过程发生在细菌细胞的繁殖期，因此，本类药物为繁殖期快效杀菌剂，对已形成细胞壁的或者非生长繁殖的细菌，此时不需要合成细胞壁，则青霉素不起杀菌作用，故临床上应避免将青霉素这类“繁殖期杀菌药”与抑制细菌生长繁殖的“快效抑菌药”（如氟苯尼考、四环素类、红霉素等）合用，尤其是在治疗脑膜炎或需迅 `source_id=SRC-0089; page=27; line=853`
- `SFDUT1-TX-0105` drug_interaction / p.31 / 肆霉素类: ④ 本品还与下列药物有配伍禁忌：氨基糖苷类、林可霉素、氟苯尼考、泰妙菌素、土霉素、四环素、金霉素、多黏菌素、红霉素、氯丙嗪、碳酸氢钠、葡萄糖酸钙、氯化钙、肾上腺类、B族维生素、维生素C、磺胺类药物。 `source_id=SRC-0089; page=31; line=916`
- `SFDUT1-TX-0114` drug_interaction / p.31 / 肆霉素类: （3）注意事项 阿莫西林与喹诺酮类、氨基糖苷类抗菌药物联合应用，有协同或相加作用。但与四环素类、氟苯尼考、大环内酯类及林可霉素联用，可能发生拮抗作用。其他参见注射用氨苄西林钠。 `source_id=SRC-0089; page=31; line=938`
- `SFDUT1-TX-0171` drug_interaction / p.45 / 氨基糖苷类: （5）注意事项 本品不能与氟苯尼考或四环素合用，呈拮抗作用。 `source_id=SRC-0089; page=45; line=1229`
- `SFDUT1-TX-0239` candidate_fact / p.53 / 大环内酯类: ② $5 \%$ 乙酰异戊酰泰乐菌素预混剂（回盛“治嗽静”、伊科“爱乐新”），以本品计，混饲，每吨饲料1000克，连用7天。注意：禁止与泰妙菌素、林可霉素、氟苯尼考及大环内酯类其他药物联用。搅拌配料时，防止与皮肤、眼睛接触。 `source_id=SRC-0089; page=53; line=1490`
- `SFDUT1-TX-0243` compliance_or_safety / p.57 / 氟苯尼考: 因为氯霉素毒性大，能严重抑制动物骨髓造血功能，从而引起白细胞缺乏症及血小板生成减少，或导致不可逆性再生障碍性贫血，并有抑制免疫作用，因此农业部2002年193号公告明确规定氯霉素禁用于所有食品动物。目前氟苯尼考已成为氯霉素禁用后的主要替代品种，在兽医临床上发挥着重要作用。如何正确而合理地使用氟苯尼考，在养猪生产和临床应用上都应注意哪些事项，成为 `source_id=SRC-0089; page=57; line=1505`
- `SFDUT1-TX-0244` candidate_fact / p.58 / 氟苯尼考: 氟苯尼考化学结构与氯霉素相似，是甲砜霉素的单氟衍生物，其抗菌谱、抗菌作用、抗菌机制及适应证与氯霉素相同。由于氯霉素苯环结构上的对位硝基被甲砜基取代，故毒副作用降低，但仍存在剂量相关的可逆性骨髓造血功能抑制作用。其作用机理是与细菌70S核糖体的50S亚基结合，阻断肽酰基转移酶，抑制肽链延伸，从而干扰细菌蛋白质合成而产生抗菌作用。本品属广谱速效抑菌剂，抗菌活性略优于氯霉素与甲砜霉素，耐药性与药物残留低。对多种革兰阳性菌、革兰阴性菌及支原体等有较强的抗菌活性，尤其是对革兰阴性菌的作用优于革兰阳性菌。对溶血性巴氏杆菌、多杀性巴氏杆菌（可引起猪肺炎）、猪胸膜肺炎放线杆菌（可引起传染性胸膜肺炎）高度敏感；对多数革兰阴性肠杆菌科细菌，包括副伤寒杆菌、克雷伯菌、大肠杆菌、沙门菌、布氏杆菌均敏感。敏感的革兰阳性菌有链球菌、化脓性隐秘杆菌、李氏杆菌、肺炎球菌、葡萄球菌等。对钩端螺旋体、衣原体、立克次体有一定作用。也能顺利进入细胞内，对多种细胞内致病原也有效。对各种厌氧菌如破伤风梭菌、放线菌等也有相当作用，但对革兰阳性球菌的作用不如青霉素和四环素。另外，一般剂量的氟苯尼考具抑菌作用，高浓度时或作用于对本品高度敏感的细菌时可呈杀菌作用。细菌对本品可 `source_id=SRC-0089; page=58; line=1513`
- `SFDUT1-TX-0245` candidate_fact / p.58 / 氟苯尼考: 猪内服吸收较完全，生物利用率高，即使在饲喂状况下，仍可吸收 $80\% \sim 90\%$ 。由于氟苯尼考在肝内不与葡萄糖醛酸结合，因此体内抗菌活性较高，比氯霉素强 $2.5 \sim 5$ 倍。内服和肌注吸收迅速，血药浓度高。药物分布广泛，可渗入各种组织与体液，在内脏中也有较高浓度。可顺利通过血脑屏障，腹水、胸腔积液中也可渗入。半衰期长，有效浓度维持时间长。 `source_id=SRC-0089; page=58; line=1517`
- `SFDUT1-TX-0248` drug_interaction / p.36 / 氟苯尼考: （1）本品不宜与大环内酯类（如泰乐菌素、红霉素、替米考星、吉他霉素等）、林可胺类（如林可霉素）及双萜类半合成抗生素——泰妙菌素（枝原净）联合用药，合用时可产生拮抗作用。因为它们的作用机制相同，均是与细菌核糖体50S亚基结合，后三类抗生素可替代或阻止氟苯尼考与细菌核糖体的50S亚基相结合，即由于竞争作用部位而导致减效。 `source_id=SRC-0089; page=36; line=1529`
- `SFDUT1-TX-0252` dose_route_course / p.38 / 氟苯尼考: （1）氟苯尼考注射液（规格：10毫升：1克；100毫升：30克），肌注（以氟苯尼考计），一次量，20毫克/千克体重，每天2次，连用 $3\sim 5$ 天。 `source_id=SRC-0089; page=38; line=1549`
- `SFDUT1-TX-0253` dose_route_course / p.47 / 氟苯尼考: （2）氟苯尼考粉（规格：50克：5克），内服（以氟苯尼考计），一次量 $20\sim 30$ 毫克/千克体重，每天2次，连用 $3\sim 5$ 天。 `source_id=SRC-0089; page=47; line=1551`
- `SFDUT1-TX-0254` treatment_or_prevention / p.52 / 氟苯尼考: （3）氟苯尼考预混剂（规格：100克：20克；100克：10克；100克：5克；100克：2克），混饲，用于治疗敏感菌所致感染，以氟苯尼考计，每吨饲料添加40克，连用7天。 `source_id=SRC-0089; page=52; line=1552`
- `SFDUT1-TX-0255` vaccination_or_immunization / p.61 / 氟苯尼考: （1）虽然氟苯尼考的毒副作用比氯霉素降低，不导致不可逆再生障碍性贫血，但仍有血液系统毒性，亦可引起可逆性细胞生成抑制及白细胞、血小板的减少，且有较氯霉素更强的免疫抑制作用，故应严格掌握适应证，不宜用于轻度感染的选用药，更不应作为感染的预防用药，只宜在某些重症感染或低毒性药物治疗无效时使用。本药治疗时间应持续至治愈，防止复发。但应避免剂量过大或重复疗程使用，防止可逆性骨髓抑制毒性反应发生的可能性。 `source_id=SRC-0089; page=61; line=1556`
- `SFDUT1-TX-0257` treatment_or_prevention / p.61 / 氟苯尼考: （5）传染性胸膜肺炎、副猪嗜血杆菌病、猪肺疫等的治疗：发病初期，患病猪群还有较好的食欲时，混饲给药时可适当提高添加量，每吨饲料可添加氟苯尼考（效价）100克，最好再配合强力霉素（效价）200克，连用7天，有较好效果。对传染性疾病引起的发热、咳嗽、气喘，单独使用抗菌药物即可，无需添加其他解热镇痛、止咳平喘类药物。如果病猪出现高热、不食，则要进行隔离治疗，使用氟苯尼考注射液肌内注射；若体温超过 $41^{\circ}\mathrm{C}$ 时，可配合解热镇痛药及地塞米松使用，效果更佳。 `source_id=SRC-0089; page=61; line=1560`
- `SFDUT1-TX-0258` treatment_or_prevention / p.61 / 氟苯尼考: （6）在防治呼吸道病综合征（PRDC）方面，有的厂家推荐氟苯尼考与阿莫西林或泰乐菌素或泰妙菌素合用，笔者认为此法欠妥。因为从药理学的角度讲，两者不可联用。但氟苯尼考可与四环 `source_id=SRC-0089; page=61; line=1561`
- `SFDUT1-TX-0269` dose_route_course / p.55 / 林可霉素: （2）用法与用量 肌注：一次量，每千克体重10毫克，2次/天，连用 $3\sim 5$ 天。注意：不能与磺胺嘧啶钠混合注射；亦不宜与氟苯尼考、大环内酯类、泰妙菌素、氟喹诺酮类抗菌药物联用，呈拮抗作用。 `source_id=SRC-0089; page=55; line=1630`
- `SFDUT1-TX-0312` treatment_or_prevention / p.73 / 磺胺类药物及抗菌增效剂: 磺胺类药物（SAs）是指具有对氨基苯磺酰胺结构的一类用于预防和治疗全身各系统细菌感染的化学合成药物的总称。磺胺类药物作为应用最早的（1935年合成百浪多息）一类人工合成的抗菌药物，有其独特的优点：抗菌谱广、疗效确实、性质稳定、不易变质、使用方便、能大量生产、价格相对低廉。但同时也有抗菌作用较弱、不良反应较多、细菌易产生耐药性、用量大、疗程偏长等缺陷。在发现了甲氧苄啶（TMP）和二甲氧苄啶（DVD）等抗菌增效剂后，把磺胺药和抗菌增效剂联合使用，使抗菌活性和疗效大大增强，甚至从抑菌剂变为杀菌剂，因此，磺胺类药至今仍为猪抗感染治疗中的重要药物之一，在临床上仍广泛应用。除用于治疗的针剂外，主要通过拌料或饮水做脉冲式药物保健。保健时往往配伍使用强力霉素等四环素类药物、枝原净（泰妙菌素）、泰乐菌素或氟苯尼考等。 `source_id=SRC-0089; page=73; line=1843`
- `SFDUT1-TX-0382` dose_route_course / p.87 / 其他合成抗菌药: ③ 注意事项 禁与氟苯尼考、大环内酯类、四环素类等药物合用。切勿随意加量或加倍使用，防止中毒。中毒症状是咳嗽、喷嚏、发抖、叫唤、后躯瘫痪等。按最小量的5倍，即10毫克/千克体重，就有可能引起轻度中毒。发现中毒，可马上肌注硫酸甲基新斯的明（10毫升：200毫克，即 $2\%$ ）抢救，按 $0.04 \sim 0.1$ 毫克/千克体重。新斯的明中毒，可用阿托品解救。 `source_id=SRC-0089; page=87; line=2145`
- `SFDUT1-TX-0545` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （5）避免使用免疫抑制剂 不论是注射病毒苗还是细菌苗，也不论注射活苗或死苗，在免疫前后 $5 \sim 7$ 天都要避免使用影响疫苗免疫应答的药物和免疫抑制剂，如氟苯尼考、喹乙醇、磺胺类药、氨基糖苷类（如庆大霉素、卡那霉素）、四环素类及地塞米松等糖皮质激素，因它们对抗体的合成有一定抑制作用，或对T淋巴细胞、B淋巴细胞的转化有明显的抑制作用，从而影响免疫效果。 `source_id=SRC-0089; page=120; line=2720`
- `SFDUT1-TX-0627` vaccination_or_immunization / p.145 / 猪繁殖与呼吸障碍综合征: 九是对猪群进行药物预防，控制细菌性继发感染。在发病高峰前，可在饲料中添加对继发性细菌感染敏感的抗菌药物及增强机体非特异性免疫力的药物。如“骏安”（乙酰戊乙酰泰乐菌素——第2代替米考星）、替米考星、加康（10%氟苯尼考）、枝原净、强力霉素、黄芪多糖等。 `source_id=SRC-0089; page=145; line=3091`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
- `SFDUT1-TX-0640` vaccination_or_immunization / p.152 / 猪圆环病毒病: 采取病因治疗与对症治疗相结合的“标本兼治”的办法治疗。抗菌药物可选用枝原净、氟苯尼考、氟喹诺酮类、丁胺卡那霉素、庆大霉素、阿莫西林、氨苄西林、头孢类、磺胺类等肌注，并配合使用黄芪多糖、鱼腥草、双黄连等免疫增强剂、抗病毒药物及维生素 $\mathbf{B}_{1}$ 和维生素C等。高热者可配合使用安乃近、复方氨基比林等解热镇痛药。因为PCV-2病毒主要侵害猪的免疫系统，临床上尽可能不使用甲矾霉素、卡那霉素等免疫抑制作用的药物，除发生皮炎及肾病综合征外，也不宜使用地塞米松、氢化可的松等皮质激素类药物。也可采用血清疗法：采本场淘汰母猪血，分离血清， $3\sim 5$ 周龄，腹股沟皮下或腹腔注射5毫升，或 $2\sim 3$ 周龄、5周龄仔猪腹股沟注射 $5\sim 10$ 毫升。也可对发病猪进行治疗，每头病猪注射血清 $10\sim 20$ 毫升，隔日注射一次。 `source_id=SRC-0089; page=152; line=3171`
- `SFDUT1-TX-0685` treatment_or_prevention / p.172 / 猪流行性感冒: （7）在改善饲养管理基础上，积极做好病猪的治疗工作。发病时一般用柴胡、复方氨基比林、安乃近或对乙酰氨基酚注射液等解热镇痛药对症疗法以减轻症状和使用抗生素或磺胺类药物防控继发感染，如饲料添加阿莫西林、金霉素、氟苯尼考等，也可添加黄芪多糖和电解多维。还可采用中药方剂治疗。治疗人流感常用的抗病毒药物，对猪流感病毒也有较好的良效。在加强护理基础上进行对症治疗，才能收到好的效果。 `source_id=SRC-0089; page=172; line=3509`
- `SFDUT1-TX-0722` treatment_or_prevention / p.188 / 猪巴氏杆菌病: 个体治疗可选用第3代头孢菌素类和氟喹诺酮类，这是目前治疗本病最有效的药物。也可酌情选用氨基糖苷类、氨苄西林、阿莫西林、氟苯尼考、长效土霉素、强力霉素、磺胺类药物。预防用药可在饲料中添加选用氟苯尼考、泰乐菌素与磺胺二甲嘧啶联用等都有较好疗效。治疗时一般采用交叉用药，用药前尽可能先做药敏试验而后选用最敏感的药物。 `source_id=SRC-0089; page=188; line=3740`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-012-florfenicol.md`
- Byte size moved: 5193
- Fact-like rows moved: 12
- Candidate fact mentions moved: 5
- Dose/route/course fact markers moved: 5
- Source anchors moved: 12

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 12 linked drug-use facts.
- Source pages: 201, 202, 210, 216, 217, 235, 257, 294, 304, 306, 307.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0048` dose_route_course / p.201 / 副猪嗜血杆菌病: ⑤ 氟苯尼考注射液，30毫克/千克体重，2次/天，连用 $3\sim 5$ 天（如果按国内厂家使用说明书用量20毫克/千克体重，48小时一次，连用2次，效果不好）。 `source_id=SRC-0090; page=201; line=175`
- `SFDUT2-TX-0055` candidate_fact / p.202 / 副猪嗜血杆菌病: ④ 每吨饲料添加英国伊科“爱乐新”预混料1000克或伊科力康（ $10\%$ 氟苯尼考）1500克，或“氟奇霉素”800克，或“加康”500克，或替米考星200克（效价），连用2周。 `source_id=SRC-0090; page=202; line=196`
- `SFDUT2-TX-0072` dose_route_course / p.210 / 猪链球菌病: c. 氟苯尼考注射液 $20 \sim 40$ 毫克/千克体重， $1 \sim 2$ 次/天，连用 $3 \sim 5$ 天。注意：如按厂家使用说明书48小时一次，连用2次，效果不佳。 `source_id=SRC-0090; page=210; line=300`
- `SFDUT2-TX-0084` candidate_fact / p.216 / 猪传染性胸膜肺炎: （1）推荐注射用药方案 应选择对革兰阴性菌敏感的药物。首选药物是头孢噻呋（或头孢噻肟）和氟苯尼考。强力霉素、庆大霉素配合阿莫西林、恩诺沙星、磺胺六甲氧、泰妙菌素、阿奇霉素等可酌情选用。 `source_id=SRC-0090; page=216; line=379`
- `SFDUT2-TX-0086` dose_route_course / p.216 / 猪传染性胸膜肺炎: ② 氟苯尼考注射液， $20\sim 30$ 毫克/千克体重，每天 $1\sim 2$ 次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=216; line=381`
- `SFDUT2-TX-0093` candidate_fact / p.217 / 猪传染性胸膜肺炎: ① 氟苯尼考100克（效价），连续使用7天，然后将剂量减半，再继续使用2周。 `source_id=SRC-0090; page=217; line=394`
- `SFDUT2-TX-0140` dose_route_course / p.235 / 猪增生性肠炎: ① 诺华公司生产的注射用延胡索泰妙菌素（泰妙灵、枝原净），肌内注射，一次量，15毫克/千克体重，每天1次，连用 $3\sim$ 5天。注意事项：a. 要现配现用，当天用完；b. 不能与泰乐菌素、氟苯尼考、林可霉素联用，否则由于互相竞争作用部位而导致减效。 `source_id=SRC-0090; page=235; line=673`
- `SFDUT2-TX-0205` dose_route_course / p.257 / 猪衣原体病: 首选四环素类抗生素（强力霉素、金霉素、土霉素）进行预防和治疗。为了完全排除或抑制潜伏性感染，公母猪在配种前 $1 \sim 2$ 周，应按治疗水平通过饮水或混饲，连续给药 $2 \sim 3$ 周，治疗不充分时可引起复发。对怀孕母猪在产前 $2 \sim 3$ 周混饲 $10 \sim 15$ 天以预防新生仔猪感染本病。也可选用青霉素、氟苯尼考、大环内酯类（泰乐菌素、乙酰异戊酰泰乐菌素）等抗菌药物。在流行期，也可每吨饲料添加 $15\%$ 金霉素预混剂2000克或强力霉素150克（效价），母猪群体预防。为了防止出现耐药性，要合理交替用药。对出现临床症状的猪，可肌内注射辉瑞“得米先”（ $20\%$ 长效土霉素注射液），每10千克体重肌注1毫升，每3天1次，连用3次；或土霉素注射液，20毫升/千克体重，每天1次，连续治疗 $5 \sim 7$ 天；或肌注强力霉素注射液，3毫克/千克体重，每天1次，连用5天。 `source_id=SRC-0090; page=257; line=1029`
- `SFDUT2-TX-0290` candidate_fact / p.294 / 母猪产后泌尿生殖系统疾病: ② 庆大霉素、青霉素G、头孢菌素类、大环内酯类、四环素类抗生素或氟苯尼考，连续肌注5天，有较好疗效。 `source_id=SRC-0090; page=294; line=1605`
- `SFDUT2-TX-0320` vaccination_or_immunization / p.304 / 猪呼吸道病综合征: ⑤ 免疫抑制因素 已知有许多可致免疫抑制的病原体，尤以病毒为主，如PRRSV、PCV-2、SIV、CFSV等。此外，饲料中的霉菌毒素，某些药物，如长期使用地塞米松、磺胺类药、氟苯尼考、卡那霉素等。 `source_id=SRC-0090; page=304; line=1743`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
- `SFDUT2-TX-0343` candidate_fact / p.307 / 猪呼吸道病综合征: ⑦ $10\%$ 氟苯尼考500克+强力霉素200克+TMP100克。 `source_id=SRC-0090; page=307; line=1799`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-012-florfenicol.md`
- Byte size moved: 730
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-066-DRUG-012-florfenicol-md-7113` 氟苯尼考 / 酰胺醇类 / p.66：目录定位显示 `氟苯尼考` 属于 `酰胺醇类`，可作为药物召回、类别边界和联用禁忌复核入口。 `source_id=SRC-0091; page=66`
<!-- RAU_1_200_V14_END -->
