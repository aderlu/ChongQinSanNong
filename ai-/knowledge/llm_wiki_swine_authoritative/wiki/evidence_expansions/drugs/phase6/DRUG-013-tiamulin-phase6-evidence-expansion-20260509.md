---
page_id: DRUG-013-tiamulin
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase6_drug_page_compaction
moved_from: wiki/drugs/DRUG-013-tiamulin.md
generated: 2026-05-09T14:25:31+08:00
---

# DRUG-013-tiamulin Phase 6 Evidence Expansion

This file stores high-density batch evidence moved out of the default runtime drug page during Phase 6.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any treatment parameter, withdrawal-period, MRL, residue, or food-safety conclusion still requires current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-013-tiamulin.md`
- Byte size moved: 564
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 1 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 泰妙菌素.
- Source pages: 27.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0022` 猪圆环病毒2型感染 / 处方1 `source_id=SRC-0087; page=27; line=1092-1100`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-013-tiamulin.md`
- Byte size moved: 4794
- Fact-like rows moved: 14
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 14

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 8 appendix medicine rows and 6 text treatment mentions linked to this drug page.
- Source pages: 26, 73, 75, 86, 87, 101, 136, 152, 155.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0039` Denagard 200 Solution for Injection (200 mg tiamulin/ml): dose=3 ml/40 kg im daily; meat_withhold=14 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0091` Tiamutin 200 Injection (200 mg tiamulin/ml): dose=3 ml/40 kg im daily; meat_withhold=14 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0098` Vetmulin 162 mg/ml Solution for Injection for Pigs (162 mg tiamulin/ml): dose=1 ml/20 kg im daily; meat_withhold=5 days. `source_id=SRC-0088; page=136; table=Table A.2.`
- `VTOP-MED-0104` Denagard 12.5% Oral Solution (125 mg tiamulin/ml): dose=8.8 mg/kg daily in drinking water for 3–5 days; meat_withhold=2 days. `source_id=SRC-0088; page=136; table=Table A.3.`
- `VTOP-MED-0118` Tiamutin 12.5% Solution (125 mg tiamulin/ml): dose=8.8 mg/kg daily in drinking water for 3–5 days; meat_withhold=2 days. `source_id=SRC-0088; page=136; table=Table A.3.`
- `VTOP-MED-0119` Tiamvet 12.5% Solution (125 mg tiamulin/ml): dose=8.8 mg/kg daily in drinking water for 3–5 days; meat_withhold=2 days. `source_id=SRC-0088; page=136; table=Table A.3.`
- `VTOP-MED-0123` Vetmulin 125 mg/ml Oral Solution (125 mg tiamulin/ml): dose=7 ml/100 kg daily for 5 days for the treatment of swine dysentery; 12–16 ml/110 kg daily for 5 days for the treatment of enzootic pneumonia; meat_withhold=5 days. `source_id=SRC-0088; page=136; table=Table A.3.`
- `VTOP-MED-0124` Vetmulin 450 mg/g Granules for Use in Drinking Water for Pigs (450 mg tiamulin hydrogen fumarate/g): dose=8.8 mg/kg daily for 5 days to treat swine dysentery; 15–20 mg/kg daily for 5 days to treat enzootic pneumonia; meat_withhold=5 days. `source_id=SRC-0088; page=26; table=Table A.3.`
- `VTOP-TX-0099` dose_or_route / p.73 / Proliferative enteropathy: Treatment of the individual pig is best carried out with long-acting tetracycline by intramuscular injection. Tetracyclines or tylosin are the antibiotics of choice for group therapy in the drinking water. Some authorities favour tiamulin or lincomycin, particularly if there are other enteric pathogens involved. Tetracyclines may be effective given in the feed but levels should be higher than standard, in the region  `source_id=SRC-0088; page=73; line=2014`
- `VTOP-TX-0104` treatment_candidate / p.75 / Swine dysentery: Tylosin used to be the drug of choice for treatment either of the individual by injection or for the group in the water. Sadly most isolates are now resistant to tylosin, so tiamulin either as an injection or in the water would now be the drug of choice. `source_id=SRC-0088; page=75; line=2052`
- `VTOP-TX-0139` treatment_candidate / p.86 / Mycoplasma hyorhinis disease: Treatment is the same as for enzootic pneumonia, with oxytetracyclines, tiamulin and tylosine being most commonly used. In the author’s experience the injectable route is more effective, particularly if NSAIDs are also injected. `source_id=SRC-0088; page=86; line=2286`
- `VTOP-TX-0140` treatment_candidate / p.87 / Mycoplasma hyosynoviae disease: This is a disease of older growing pigs between 2 and 5 months of age. It is also mainly a disease of the joints but will cause respiratory signs. It occurs worldwide. It occurs mainly after stress. The organism can be regularly cultured from the tonsil of healthy pigs. There may be coughing and various levels of lameness. One or more joints will be swollen. The organism can be cultured from a joint tap in the live p `source_id=SRC-0088; page=87; line=2290`
- `VTOP-TX-0197` vaccination / p.101 / Leptospirosis: Treatment of ill piglets should be injections of combinations of penicillin/streptomycin. Tiamulin can be used in the water. Abortions may be prevented by a single dose of streptomycin at $2 5 \mathrm { \ m g / k g }$ . This can be used as a long-term preventative. Sows should be injected 1 week before service and again 2 weeks before farrowing. If animals are not infected they should be vaccinated with a killed vacc `source_id=SRC-0088; page=101; line=2711`
- `VTOP-TX-0288` treatment_candidate / p.136 / Tiamulin: Rarely tiamulin, if fed at standard therapeutic levels for the treatment of swine dysentery, will cause adverse reactions. These may be just a slight reddening or in extremely rare cases death will occur. In these cases haemorrhages will be seen in the myocardium. `source_id=SRC-0088; page=136; line=3618`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-013-tiamulin.md`
- Byte size moved: 9618
- Fact-like rows moved: 16
- Candidate fact mentions moved: 5
- Dose/route/course fact markers moved: 4
- Source anchors moved: 16

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 16 linked drug-use facts.
- Source pages: 13, 27, 31, 34, 36, 39, 42, 46, 53, 55, 59, 61, 63, 73, 82, 151.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0030` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （3）四环素类 四环素类药物与非同类药物如泰妙菌素、泰乐菌素配伍用于胃肠道和呼吸道感染时有协同作用，可降低使用浓度，缩短治疗时间。四环素类与氯霉素类合用有较好的协同作用。土霉素不能与喹乙醇、北里霉素合用。 `source_id=SRC-0089; page=13; line=590`
- `SFDUT1-TX-0092` treatment_or_prevention / p.27 / 肆霉素类: 其作用机理主要是干扰转肽酶、破坏细菌细胞壁的合成而产生杀菌作用。它能抑制细菌细胞壁的基础成分黏肽的合成，造成细胞壁缺损而失去屏障保护作用，使水分渗入细菌胞浆，导致菌体肿胀、变形，最后裂解而死亡。 $\mathrm{G}^{+}$ 菌的细胞壁主要由黏肽（达 $65\% \sim 95\%$ ）组成，而 $\mathrm{G}^{-}$ 菌细胞壁的主要成分是磷脂（黏肽仅占 $1\% \sim 10\%$ ），由于 $\mathrm{G}^{+}$ 菌的细胞壁黏肽含量较 $\mathrm{G}^{-}$ 菌高，故对 $\mathrm{G}^{+}$ 菌作用很强，而对 $\mathrm{G}^{-}$ 菌作用较弱。另外，生长期的敏感菌分裂旺盛，细胞壁处于生物合成期，在青霉素的作用下，黏肽的合成受阻不能形成细胞壁，在渗透压作用下，导致细胞膜破裂而死亡，这一过程发生在细菌细胞的繁殖期，因此，本类药物为繁殖期快效杀菌剂，对已形成细胞壁的或者非生长繁殖的细菌，此时不需要合成细胞壁，则青霉素不起杀菌作用，故临床上应避免将青霉素这类“繁殖期杀菌药”与抑制细菌生长繁殖的“快效抑菌药”（如氟苯尼考、四环素类、红霉素等）合用，尤其是在治疗脑膜炎或需迅 `source_id=SRC-0089; page=27; line=853`
- `SFDUT1-TX-0105` drug_interaction / p.31 / 肆霉素类: ④ 本品还与下列药物有配伍禁忌：氨基糖苷类、林可霉素、氟苯尼考、泰妙菌素、土霉素、四环素、金霉素、多黏菌素、红霉素、氯丙嗪、碳酸氢钠、葡萄糖酸钙、氯化钙、肾上腺类、B族维生素、维生素C、磺胺类药物。 `source_id=SRC-0089; page=31; line=916`
- `SFDUT1-TX-0208` candidate_fact / p.46 / 四环素类: ③ 混饲，4月龄以内猪，每吨饲料添加 $15\%$ 饲料级金霉素预混剂 $200 \sim 500$ 克，用于促生长； $80\%$ 泰妙菌素（枝原净）预混剂 $125$ 克 $+15\%$ 金霉素预混剂 $2000$ 克，于仔猪断奶后饲喂 $10 \sim 14$ 天，有利于控制呼吸道疾病综合征及增生性肠炎等。 `source_id=SRC-0089; page=46; line=1371`
- `SFDUT1-TX-0239` candidate_fact / p.53 / 大环内酯类: ② $5 \%$ 乙酰异戊酰泰乐菌素预混剂（回盛“治嗽静”、伊科“爱乐新”），以本品计，混饲，每吨饲料1000克，连用7天。注意：禁止与泰妙菌素、林可霉素、氟苯尼考及大环内酯类其他药物联用。搅拌配料时，防止与皮肤、眼睛接触。 `source_id=SRC-0089; page=53; line=1490`
- `SFDUT1-TX-0248` drug_interaction / p.36 / 氟苯尼考: （1）本品不宜与大环内酯类（如泰乐菌素、红霉素、替米考星、吉他霉素等）、林可胺类（如林可霉素）及双萜类半合成抗生素——泰妙菌素（枝原净）联合用药，合用时可产生拮抗作用。因为它们的作用机制相同，均是与细菌核糖体50S亚基结合，后三类抗生素可替代或阻止氟苯尼考与细菌核糖体的50S亚基相结合，即由于竞争作用部位而导致减效。 `source_id=SRC-0089; page=36; line=1529`
- `SFDUT1-TX-0258` treatment_or_prevention / p.61 / 氟苯尼考: （6）在防治呼吸道病综合征（PRDC）方面，有的厂家推荐氟苯尼考与阿莫西林或泰乐菌素或泰妙菌素合用，笔者认为此法欠妥。因为从药理学的角度讲，两者不可联用。但氟苯尼考可与四环 `source_id=SRC-0089; page=61; line=1561`
- `SFDUT1-TX-0269` dose_route_course / p.55 / 林可霉素: （2）用法与用量 肌注：一次量，每千克体重10毫克，2次/天，连用 $3\sim 5$ 天。注意：不能与磺胺嘧啶钠混合注射；亦不宜与氟苯尼考、大环内酯类、泰妙菌素、氟喹诺酮类抗菌药物联用，呈拮抗作用。 `source_id=SRC-0089; page=55; line=1630`
- `SFDUT1-TX-0274` dose_route_course / p.34 / 泰妙菌素与沃尼妙林: （2）用法与用量 以泰妙菌素计，混饮，每升水，猪 $45\sim 60$ 毫克，临床用溶液应当天配制，连用5天。 `source_id=SRC-0089; page=34; line=1672`
- `SFDUT1-TX-0277` candidate_fact / p.39 / 泰妙菌素与沃尼妙林: （1）适应证 同“延胡索酸泰妙菌素可溶性粉”。 `source_id=SRC-0089; page=39; line=1677`
- `SFDUT1-TX-0279` dose_route_course / p.42 / 泰妙菌素与沃尼妙林: （3）用法与用量 以泰妙菌素计，混饲，每吨饲料，猪100克，连用 $5\sim 10$ 天。 `source_id=SRC-0089; page=42; line=1680`
- `SFDUT1-TX-0283` candidate_fact / p.59 / 泰妙菌素与沃尼妙林: （1）适应证及特点 本品是一种新型动物专用抗生素，抗菌谱广，对革兰阳性菌、部分革兰阴性菌和支原体均有作用；对猪痢疾短螺旋体、结肠菌毛样短螺旋体、细胞内劳森菌、葡萄球菌、链球菌、猪肺炎支原体、猪滑液支原体、猪胸膜肺炎放线杆菌等均有较强的抑制作用；对支原体属和螺旋体属高度敏感。对细胞内劳森菌的抑制效果优于金霉素、林可霉素、泰妙菌素、泰乐菌素。 `source_id=SRC-0089; page=59; line=1696`
- `SFDUT1-TX-0284` dose_route_course / p.63 / 泰妙菌素与沃尼妙林: （2）盐酸沃尼妙林治疗猪混合感染型呼吸道病猪的混合型呼吸道感染具有普遍性，给养猪者造成巨大的经济损失。临床研究表明混合型感染主要为肺炎支原体、多杀性巴氏杆菌、胸膜肺炎放线菌，有时还有大肠杆菌和猪链球菌感染。研究者对猪人工感染肺炎支原体、多杀性巴氏杆菌和胸膜炎放线菌，然后用替米考星300毫克/千克、泰妙菌素100毫克/千克+金霉素400毫克/千克、沃尼 `source_id=SRC-0089; page=63; line=1700`
- `SFDUT1-TX-0312` treatment_or_prevention / p.73 / 磺胺类药物及抗菌增效剂: 磺胺类药物（SAs）是指具有对氨基苯磺酰胺结构的一类用于预防和治疗全身各系统细菌感染的化学合成药物的总称。磺胺类药物作为应用最早的（1935年合成百浪多息）一类人工合成的抗菌药物，有其独特的优点：抗菌谱广、疗效确实、性质稳定、不易变质、使用方便、能大量生产、价格相对低廉。但同时也有抗菌作用较弱、不良反应较多、细菌易产生耐药性、用量大、疗程偏长等缺陷。在发现了甲氧苄啶（TMP）和二甲氧苄啶（DVD）等抗菌增效剂后，把磺胺药和抗菌增效剂联合使用，使抗菌活性和疗效大大增强，甚至从抑菌剂变为杀菌剂，因此，磺胺类药至今仍为猪抗感染治疗中的重要药物之一，在临床上仍广泛应用。除用于治疗的针剂外，主要通过拌料或饮水做脉冲式药物保健。保健时往往配伍使用强力霉素等四环素类药物、枝原净（泰妙菌素）、泰乐菌素或氟苯尼考等。 `source_id=SRC-0089; page=73; line=1843`
- `SFDUT1-TX-0348` drug_interaction / p.82 / 氟喹诺酮类药物: 这是因为其结构不同于其他抗生素，抗菌作用独特，而且不受质粒传导耐药性影响。因此对某些多重耐药菌株或对其他抗菌药耐药的细菌仍具有较强的良好抗菌活性，也有利于与其他抗菌药物联合用药。对耐甲氧嘧啶/磺胺药的细菌、耐庆大霉素的铜绿假单胞菌、耐泰乐菌素或泰妙菌素的支原体等也有很好的疗效，且可用于支原体、衣原体、军团菌等在细胞内繁殖的病原体。 `source_id=SRC-0089; page=82; line=2022`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-013-tiamulin.md`
- Byte size moved: 8180
- Fact-like rows moved: 15
- Candidate fact mentions moved: 6
- Dose/route/course fact markers moved: 2
- Source anchors moved: 15

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 15 linked drug-use facts.
- Source pages: 192, 193, 195, 216, 217, 235, 236, 244, 283, 295, 306, 307.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0003` treatment_or_prevention / p.192 / 猪支原体肺炎: 多种喹诺酮类药、抗生素类药如林可霉素、泰妙菌素、泰乐菌素、替米考星、乙酰异戊酰泰乐菌素、四环素、土霉素、强力霉素、金霉素、卡那霉素等对猪支原体肺炎均有较好的治疗作用。 `source_id=SRC-0090; page=192; line=41`
- `SFDUT2-TX-0007` dose_route_course / p.192 / 猪支原体肺炎: ③ 泰妙菌素注射液，20毫克/千克，一天1次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=192; line=47`
- `SFDUT2-TX-0013` candidate_fact / p.193 / 猪支原体肺炎: ① $80\%$ 泰妙菌素预混剂（枝原净）125克 $+10\%$ 盐酸多西环素预混剂1000克。 `source_id=SRC-0090; page=193; line=60`
- `SFDUT2-TX-0031` treatment_or_prevention / p.195 / 猪支原体肺炎: 总之，控制猪气喘病需要采取综合防制的办法。其中重点是要建立健康的种猪群，母猪临产前7天和分娩后7天，用泰乐菌素、泰妙菌素或土霉素拌料饲喂，防止经母猪把疾病传给仔猪。其次是要抓好仔猪的疾病预防控制。搞好环境卫生消毒和一栏或一舍的全进全出。定期检查、立即隔离发病猪；根据猪群具体情况采取定时用药、预防用药策略。只有从总体采取合理的综合防治措施，才能有效地控制猪气喘病的发生和流行。 `source_id=SRC-0090; page=195; line=95`
- `SFDUT2-TX-0084` candidate_fact / p.216 / 猪传染性胸膜肺炎: （1）推荐注射用药方案 应选择对革兰阴性菌敏感的药物。首选药物是头孢噻呋（或头孢噻肟）和氟苯尼考。强力霉素、庆大霉素配合阿莫西林、恩诺沙星、磺胺六甲氧、泰妙菌素、阿奇霉素等可酌情选用。 `source_id=SRC-0090; page=216; line=379`
- `SFDUT2-TX-0098` candidate_fact / p.217 / 猪传染性胸膜肺炎: ⑥ 其他如爱乐新、泰乐菌素、泰乐菌素十金霉素、泰妙菌素、利高霉素等也可用。混饲最好与抗菌增效剂TMP合用（5:1），以增强疗效。 `source_id=SRC-0090; page=217; line=400`
- `SFDUT2-TX-0138` treatment_or_prevention / p.235 / 猪增生性肠炎: 常用于治疗回肠炎的抗生素有泰妙菌素、泰乐菌素、林可霉素、金霉素、强力霉素等。但治疗时常面临失败的可能，失败的原因可能有：①猪发病期间，采食量下降，因而药物的吸收量不足；②用药途径不合理，急性感染猪不能通过饮水或饲料获得治疗量的药物；③胞内劳氏菌间歇性排菌，故治疗时间难以确定或治疗太晚，在疾病的后期用药效果不理想；④抗生素的耐药性问题；⑤抗生素的有效作用时间有限。为此要根据发病猪的年龄和病的类型采用不同的治疗方法。新引进种猪在混群前，应采用治疗剂量水平的抗菌药物，通过混饲进行口服给药连续治疗14天，以防发生临床症状。治疗处方是每吨饲料中添加 $80\%$ 泰妙菌素预混剂120克、泰乐菌素100克（效价）或林可霉素110克（效价）。 `source_id=SRC-0090; page=235; line=667`
- `SFDUT2-TX-0139` treatment_or_prevention / p.235 / 猪增生性肠炎: （1）急性回肠炎需要采取得力的治疗方法，治疗既包括临床感染的猪，也包括有接触的猪。首选的治疗药物是每吨饲料添加 $80\%$ 泰妙菌素预混剂150克或泰乐菌素100克（效价）或林可霉素110克（效价），可通过预混料口服，连续治疗14天。 `source_id=SRC-0090; page=235; line=669`
- `SFDUT2-TX-0140` dose_route_course / p.235 / 猪增生性肠炎: ① 诺华公司生产的注射用延胡索泰妙菌素（泰妙灵、枝原净），肌内注射，一次量，15毫克/千克体重，每天1次，连用 $3\sim$ 5天。注意事项：a. 要现配现用，当天用完；b. 不能与泰乐菌素、氟苯尼考、林可霉素联用，否则由于互相竞争作用部位而导致减效。 `source_id=SRC-0090; page=235; line=673`
- `SFDUT2-TX-0143` vaccination_or_immunization / p.236 / 猪增生性肠炎: （2）严重的慢性回肠炎 对 $6 \sim 10$ 周龄、临床表现为猪体消瘦、有或无坏死性肠炎的病例，在胞内劳氏菌感染高峰刚到之前就将抗菌药物通过预混料给药，能够取得很好的治疗效果。添加抗菌药物的时间不可太迟或过早。太迟不能减轻临床症状；反之，如果添加时间太早，那么“洁净”的猪群没有机会产生对此病的主动免疫，仍维持其原有的易感状态，从而在以后更容易发生严重急性回肠炎。治疗处方是：每吨饲料添加 $80\%$ 泰妙菌素预混剂150克，或每吨饲料添加美国礼来公司 $8.8\%$ 磷酸盐泰乐菌素预混剂250克，连用14天。 `source_id=SRC-0090; page=236; line=679`
- `SFDUT2-TX-0161` treatment_or_prevention / p.244 / 猪痢疾: （2）猪增生性肠炎（PE）由胞内劳氏菌引起，是 $6\sim 20$ 周龄断奶后的生长肥育猪和后备种猪的一种常见腹泻病，病变主要在小肠。急性型通常发生于4月龄以后的后备种猪及肥育猪，首次观察到的临床症状常常是排出黑色柏油状粪便，皮肤苍白，死亡率高达 $50\%$ ，怀孕母猪可流产。慢性型最常见，一般发生于 $18\sim 36$ 千克体重的猪，临床症状不典型，部分猪出现腹泻时一般都是轻微的，排出正常灰绿色的疏松、稀薄直至水样粪便，出血或黏液粪便并不是慢性增生性肠炎腹泻的特征，主要是影响猪只的生长性能。剖检小肠末端50厘米处及邻近结肠上1/3处，肠壁增厚，有隆起的黏膜，导致肠管变硬，类似胶皮水管样外观。泰妙菌素、大环内酯类、林可霉素治疗有效。而对治疗猪痢疾有特效的痢菌净对本病效果不明显。确诊依赖于粪便PCR试验阳性。 `source_id=SRC-0090; page=244; line=823`
- `SFDUT2-TX-0266` candidate_fact / p.283 / 产后泌乳障碍综合征: ② 产前 $5 \sim 7$ 天至产后7天，每吨饲料中添加如下抗菌药物：辉瑞“利高霉素-44”1.5千克，或“金西林”1.25千克，或加康400克，或 $80\%$ 枝原净（ $80\%$ 泰妙菌素）125克 $+15\%$ 金霉素2000克，或泰乐菌素110克 $+SM_{2}110$ 克，或爱乐新1.5千克。 `source_id=SRC-0090; page=283; line=1445`
- `SFDUT2-TX-0295` candidate_fact / p.295 / 母猪产后泌尿生殖系统疾病: ② 产前5天至产后7天，每吨饲料中添加如下抗菌药物：辉瑞“利高霉素-44”1.5千克，或“金西林”1.25千克，或腾骏“加康”400克，或酒石酸乙酰异戊酰泰乐菌素预混剂（腾骏“骏安”、荷本“万乐福欣”、伊科拜克“爱乐新”） $50\sim 70$ 克（效价），或诺华“枝原净”（ $80\%$ 泰妙菌素）125克 $+15\%$ 金霉素2000克，或泰乐菌素110克。 `source_id=SRC-0090; page=295; line=1619`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
- `SFDUT2-TX-0337` candidate_fact / p.307 / 猪呼吸道病综合征: ① $80\%$ 泰妙菌素（枝原净）125克 $+15\%$ 金霉素2000克（或强力霉素150克）。 `source_id=SRC-0090; page=307; line=1793`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-013-tiamulin.md`
- Byte size moved: 1365
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-079-DRUG-013-tiamulin-md-9712` 泰妙菌素 / 截短侧耳素/其他抗生素 / p.79：Tiamulin 【药理作用及适应证】又名泰妙灵、支原净。广谱抑菌剂，对革兰阳性菌（如金黄色葡萄球菌、链球菌等）、胸膜肺炎放线杆菌、支原体、密螺旋体等有较强作用；对支原体作用强于大环内酯类； 但对革兰阴性菌尤其是肠道菌作用弱。其通过与细菌核糖体50S亚基结合，抑制蛋白质合成而抑菌。临床用于猪肺炎、血痢；鸡慢性呼吸道病、葡萄球菌滑膜炎；低剂量促生长，提高饲料利用率。本品单胃动物内服，生物利用度高，体内分布广，组织和乳中浓度是血清的几倍，代谢为20多种代谢物，部分有抗菌活性，代谢物主要从胆汁排泄，约 $20\%$ 从尿排出。 `source_id=SRC-0091; page=79`
<!-- RAU_1_200_V14_END -->
