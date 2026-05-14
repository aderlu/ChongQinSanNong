---
page_id: DRUG-015-tylosin
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase6_drug_page_compaction
moved_from: wiki/drugs/DRUG-015-tylosin.md
generated: 2026-05-09T14:25:31+08:00
---

# DRUG-015-tylosin Phase 6 Evidence Expansion

This file stores high-density batch evidence moved out of the default runtime drug page during Phase 6.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any treatment parameter, withdrawal-period, MRL, residue, or food-safety conclusion still requires current label/regulatory verification.

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-015-tylosin.md`
- Byte size moved: 3481
- Fact-like rows moved: 9
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 9

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 4 appendix medicine rows and 5 text treatment mentions linked to this drug page.
- Source pages: 26, 57, 70, 73, 75, 87, 154, 155.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0076` Norotyl LA 15% (150 mg tylosin/ml): dose=1 ml/7.5 kg im as a single injection; meat_withhold=7 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0095` Tylan 200 (200 mg tylosin/ml): dose=1 ml/20–100 kg im daily; meat_withhold=9 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0096` Tyluvet 20% w/v, Solution for Injection (200 mg tylosin/ml): dose=1 ml/20 kg im daily; meat_withhold=46 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0110` Pharmasin 100% w/w Water Soluble Granules (110 g tylosin/pot): dose=20 mg/kg for enzootic pneumonia; 5–10 mg/kg for ileitis or porcine intestinal adenomatosis complex (PIA); meat_withhold=1 days. `source_id=SRC-0088; page=26; table=Table A.3.`
- `VTOP-TX-0071` treatment_candidate / p.57 / Infectious mycoplasma: Acute lameness is caused by Mycoplasma hyorhinitis and Mycoplasma hyosynoviae. These should be treated with tylosin or oxytetracycline by injection; both of these antibiotics can be given as a follow-up by water medication. `source_id=SRC-0088; page=57; line=1667`
- `VTOP-TX-0086` vaccination / p.70 / Clostridial diarrhoea: There are other Clostridium spp. which cause enteric problems in pigs. Clostridium difficile has been isolated from pigs and shown to cause acute haemorrhagic diarrhoea or a more chronic scouring. These isolates have been found in North America and France but not in the UK. Both A and B toxins have been found. It must be remembered that the organism is zoonotic. In piglets under 1 week of age it causes abdominal dist `source_id=SRC-0088; page=70; line=1958`
- `VTOP-TX-0099` dose_or_route / p.73 / Proliferative enteropathy: Treatment of the individual pig is best carried out with long-acting tetracycline by intramuscular injection. Tetracyclines or tylosin are the antibiotics of choice for group therapy in the drinking water. Some authorities favour tiamulin or lincomycin, particularly if there are other enteric pathogens involved. Tetracyclines may be effective given in the feed but levels should be higher than standard, in the region  `source_id=SRC-0088; page=73; line=2014`
- `VTOP-TX-0104` treatment_candidate / p.75 / Swine dysentery: Tylosin used to be the drug of choice for treatment either of the individual by injection or for the group in the water. Sadly most isolates are now resistant to tylosin, so tiamulin either as an injection or in the water would now be the drug of choice. `source_id=SRC-0088; page=75; line=2052`
- `VTOP-TX-0140` treatment_candidate / p.87 / Mycoplasma hyosynoviae disease: This is a disease of older growing pigs between 2 and 5 months of age. It is also mainly a disease of the joints but will cause respiratory signs. It occurs worldwide. It occurs mainly after stress. The organism can be regularly cultured from the tonsil of healthy pigs. There may be coughing and various levels of lameness. One or more joints will be swollen. The organism can be cultured from a joint tap in the live p `source_id=SRC-0088; page=87; line=2290`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-015-tylosin.md`
- Byte size moved: 13815
- Fact-like rows moved: 23
- Candidate fact mentions moved: 6
- Dose/route/course fact markers moved: 2
- Source anchors moved: 23

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 23 linked drug-use facts.
- Source pages: 13, 21, 27, 36, 42, 43, 44, 45, 51, 53, 59, 61, 73, 82, 102, 145, 151, 188.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0030` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （3）四环素类 四环素类药物与非同类药物如泰妙菌素、泰乐菌素配伍用于胃肠道和呼吸道感染时有协同作用，可降低使用浓度，缩短治疗时间。四环素类与氯霉素类合用有较好的协同作用。土霉素不能与喹乙醇、北里霉素合用。 `source_id=SRC-0089; page=13; line=590`
- `SFDUT1-TX-0031` treatment_or_prevention / p.13 / 兽药使用必须遵循的基本原则: （4）大环内酯类 大环内酯类与磺胺二甲嘧啶、磺胺嘧啶、磺胺间甲氧嘧啶、TMP的复方可用于治疗呼吸道病。泰乐菌素可与磺胺类合用。红霉素不宜与 $\beta$ -内酰胺类、林可霉素、氯霉素类、 `source_id=SRC-0089; page=13; line=591`
- `SFDUT1-TX-0066` treatment_or_prevention / p.21 / 正确处理对因治疗与对症治疗: 针对发生疾病的原因进行的治疗称为对因治疗，目的在于消除疾病的原发致病因子，中医称“治本”。一般情况下，首先要对因治疗，即“治本”，选择使用消除病因的药物。例如，猪场最常见的猪气喘病，病因是感染了肺炎支原体，所以要选用枝原净、泰乐菌素、恩诺沙星、林可霉素等敏感药物肌注，彻底杀灭支原体。对因治疗要彻底，用药量要足，首次可加倍，疗程要够，一般用药 $3\sim 5$ 天；疗程不足或症状改善即停药，一是易复发，二是易诱发耐药性。 `source_id=SRC-0089; page=21; line=746`
- `SFDUT1-TX-0092` treatment_or_prevention / p.27 / 肆霉素类: 其作用机理主要是干扰转肽酶、破坏细菌细胞壁的合成而产生杀菌作用。它能抑制细菌细胞壁的基础成分黏肽的合成，造成细胞壁缺损而失去屏障保护作用，使水分渗入细菌胞浆，导致菌体肿胀、变形，最后裂解而死亡。 $\mathrm{G}^{+}$ 菌的细胞壁主要由黏肽（达 $65\% \sim 95\%$ ）组成，而 $\mathrm{G}^{-}$ 菌细胞壁的主要成分是磷脂（黏肽仅占 $1\% \sim 10\%$ ），由于 $\mathrm{G}^{+}$ 菌的细胞壁黏肽含量较 $\mathrm{G}^{-}$ 菌高，故对 $\mathrm{G}^{+}$ 菌作用很强，而对 $\mathrm{G}^{-}$ 菌作用较弱。另外，生长期的敏感菌分裂旺盛，细胞壁处于生物合成期，在青霉素的作用下，黏肽的合成受阻不能形成细胞壁，在渗透压作用下，导致细胞膜破裂而死亡，这一过程发生在细菌细胞的繁殖期，因此，本类药物为繁殖期快效杀菌剂，对已形成细胞壁的或者非生长繁殖的细菌，此时不需要合成细胞壁，则青霉素不起杀菌作用，故临床上应避免将青霉素这类“繁殖期杀菌药”与抑制细菌生长繁殖的“快效抑菌药”（如氟苯尼考、四环素类、红霉素等）合用，尤其是在治疗脑膜炎或需迅 `source_id=SRC-0089; page=27; line=853`
- `SFDUT1-TX-0182` treatment_or_prevention / p.45 / 氨基糖苷类: (2) 作用与用途 同盐酸林可霉素、硫酸大观霉素可溶性粉,用于防治猪沙门菌及大肠杆菌性肠炎、猪气喘病和密螺旋体性痢疾等, 疗效较泰乐菌素强。 `source_id=SRC-0089; page=45; line=1258`
- `SFDUT1-TX-0214` candidate_fact / p.51 / 大环内酯类: 大环内酯类是由链霉菌产生或半合成的一类弱碱性抗生素，因具有 $14 \sim 16$ 元环内酯结构，故称大环内酯类抗生素。主要对革兰阳性（ $\mathrm{G}^{+}$ ）菌、某些革兰阴性（ $\mathrm{G}^{-}$ ）球菌及支原体有良好抗菌作用。自1952年发现红霉素以来，已有竹桃霉素、螺旋霉素、吉他霉素、麦迪霉素、交沙霉素及它们的衍生物问世。近年来又开发出罗红霉素、阿奇霉素和克拉霉素等新品种。动物专用品种有泰乐菌素、替米考星、乙酰异戊酰泰乐菌素（又名泰万菌素、万乐霉素）、泰拉霉素等。大环内酯类对很多临床常用抗生素的耐药菌株 `source_id=SRC-0089; page=51; line=1386`
- `SFDUT1-TX-0227` treatment_or_prevention / p.42 / 大环内酯类: （1）作用与用途 酒石酸泰乐菌素胃肠道吸收良好，主要在肠道吸收。其磷酸盐口服吸收较少。皮下或肌内注射吸收迅速。用于支原体及 $\mathbf{G}^{+}$ 菌和螺旋体感染。主要用于防治猪支原体病，如支原体肺炎（猪气喘病）和支原体关节炎，以及敏感革兰阳性菌引起的感染性疾病，如肠炎、肺炎、乳腺炎、子宫炎等，也可用作猪的促生长剂。 `source_id=SRC-0089; page=42; line=1461`
- `SFDUT1-TX-0228` dose_route_course / p.43 / 大环内酯类: ① 泰乐菌素注射液，肌注，一次量，每千克体重10毫克，2次/天，症状消失后继续给药1天，每个注射点不超过5次。主要用于猪气喘病等。 `source_id=SRC-0089; page=43; line=1465`
- `SFDUT1-TX-0229` dose_route_course / p.44 / 大环内酯类: ② 注射用酒石酸泰乐菌素，皮下注射或肌注，每千克体重10毫克，2次/天，连用5天。 `source_id=SRC-0089; page=44; line=1466`
- `SFDUT1-TX-0230` candidate_fact / p.44 / 大环内酯类: ③ $8.8\%$ 磷酸泰乐菌素预混剂，以本品计，混饲，每吨饲料 $400\sim 800$ 克，主要用于猪促生长。 `source_id=SRC-0089; page=44; line=1467`
- `SFDUT1-TX-0231` treatment_or_prevention / p.45 / 大环内酯类: ④ 磷酸泰乐菌素、磺胺二甲嘧啶预混剂，以泰乐菌素计，混饲，每吨饲料100克，连用 $5 \sim 7$ 天。主要用于防治支原体及敏感 $\mathbf{G}^{+}$ 菌感染，也用于预防猪痢疾。 `source_id=SRC-0089; page=45; line=1468`
- `SFDUT1-TX-0232` candidate_fact / p.45 / 大环内酯类: （3）注意事项 仔猪过量服用泰乐菌素，可引起休克和死亡。不建议与其他药物混合注射给药。 `source_id=SRC-0089; page=45; line=1469`
- `SFDUT1-TX-0237` treatment_or_prevention / p.51 / 大环内酯类: ① $20\%$ 乙酰异戊酰泰乐菌素预混剂（腾骏“骏安”），对于保育猪前、中期经常发病，母猪出现繁殖障碍的猪场，可采用如下预防和控制措施，以本品计，混饲，种公、母猪（包括后备母猪）：每月7天，每吨饲料250克，控制支原体及细菌性疾病，防止疾病在母猪群中循环传染给仔猪；怀孕母猪：产前5天至产后7天，每吨饲料250克（也可外加强力霉素200克），切断细菌性疾病的垂直传播；保育猪：断奶当天至断奶后7天，每吨饲料500克，或断奶后8天至转群，每吨饲料250克，防止呼吸道和肠道疾病。 `source_id=SRC-0089; page=51; line=1486`
- `SFDUT1-TX-0239` candidate_fact / p.53 / 大环内酯类: ② $5 \%$ 乙酰异戊酰泰乐菌素预混剂（回盛“治嗽静”、伊科“爱乐新”），以本品计，混饲，每吨饲料1000克，连用7天。注意：禁止与泰妙菌素、林可霉素、氟苯尼考及大环内酯类其他药物联用。搅拌配料时，防止与皮肤、眼睛接触。 `source_id=SRC-0089; page=53; line=1490`
- `SFDUT1-TX-0248` drug_interaction / p.36 / 氟苯尼考: （1）本品不宜与大环内酯类（如泰乐菌素、红霉素、替米考星、吉他霉素等）、林可胺类（如林可霉素）及双萜类半合成抗生素——泰妙菌素（枝原净）联合用药，合用时可产生拮抗作用。因为它们的作用机制相同，均是与细菌核糖体50S亚基结合，后三类抗生素可替代或阻止氟苯尼考与细菌核糖体的50S亚基相结合，即由于竞争作用部位而导致减效。 `source_id=SRC-0089; page=36; line=1529`
- `SFDUT1-TX-0258` treatment_or_prevention / p.61 / 氟苯尼考: （6）在防治呼吸道病综合征（PRDC）方面，有的厂家推荐氟苯尼考与阿莫西林或泰乐菌素或泰妙菌素合用，笔者认为此法欠妥。因为从药理学的角度讲，两者不可联用。但氟苯尼考可与四环 `source_id=SRC-0089; page=61; line=1561`
- `SFDUT1-TX-0283` candidate_fact / p.59 / 泰妙菌素与沃尼妙林: （1）适应证及特点 本品是一种新型动物专用抗生素，抗菌谱广，对革兰阳性菌、部分革兰阴性菌和支原体均有作用；对猪痢疾短螺旋体、结肠菌毛样短螺旋体、细胞内劳森菌、葡萄球菌、链球菌、猪肺炎支原体、猪滑液支原体、猪胸膜肺炎放线杆菌等均有较强的抑制作用；对支原体属和螺旋体属高度敏感。对细胞内劳森菌的抑制效果优于金霉素、林可霉素、泰妙菌素、泰乐菌素。 `source_id=SRC-0089; page=59; line=1696`
- `SFDUT1-TX-0312` treatment_or_prevention / p.73 / 磺胺类药物及抗菌增效剂: 磺胺类药物（SAs）是指具有对氨基苯磺酰胺结构的一类用于预防和治疗全身各系统细菌感染的化学合成药物的总称。磺胺类药物作为应用最早的（1935年合成百浪多息）一类人工合成的抗菌药物，有其独特的优点：抗菌谱广、疗效确实、性质稳定、不易变质、使用方便、能大量生产、价格相对低廉。但同时也有抗菌作用较弱、不良反应较多、细菌易产生耐药性、用量大、疗程偏长等缺陷。在发现了甲氧苄啶（TMP）和二甲氧苄啶（DVD）等抗菌增效剂后，把磺胺药和抗菌增效剂联合使用，使抗菌活性和疗效大大增强，甚至从抑菌剂变为杀菌剂，因此，磺胺类药至今仍为猪抗感染治疗中的重要药物之一，在临床上仍广泛应用。除用于治疗的针剂外，主要通过拌料或饮水做脉冲式药物保健。保健时往往配伍使用强力霉素等四环素类药物、枝原净（泰妙菌素）、泰乐菌素或氟苯尼考等。 `source_id=SRC-0089; page=73; line=1843`
- `SFDUT1-TX-0348` drug_interaction / p.82 / 氟喹诺酮类药物: 这是因为其结构不同于其他抗生素，抗菌作用独特，而且不受质粒传导耐药性影响。因此对某些多重耐药菌株或对其他抗菌药耐药的细菌仍具有较强的良好抗菌活性，也有利于与其他抗菌药物联合用药。对耐甲氧嘧啶/磺胺药的细菌、耐庆大霉素的铜绿假单胞菌、耐泰乐菌素或泰妙菌素的支原体等也有很好的疗效，且可用于支原体、衣原体、军团菌等在细胞内繁殖的病原体。 `source_id=SRC-0089; page=82; line=2022`
- `SFDUT1-TX-0457` treatment_or_prevention / p.102 / 替米考星注射液: 替米考星属于大环内酯类动物专用抗生素，其抗菌作用与泰乐菌素相似，主要对抗革兰阳性菌，对少数革兰阴性菌和支原体也有效。对胸膜肺炎放线杆菌、巴氏杆菌及猪支原体的活性比泰乐菌素强，其口服时临床效果较好。主要用于治疗胸膜肺炎放线杆菌、巴氏杆菌、猪肺炎支原体等感染引起的肺炎。每吨饲料中添加 $200 \sim 400$ 克的替米考星，连用2周，可以防治猪呼吸道病综合征。但替米考星注射液对猪使用时应特别慎重！ `source_id=SRC-0089; page=102; line=2461`
- `SFDUT1-TX-0627` vaccination_or_immunization / p.145 / 猪繁殖与呼吸障碍综合征: 九是对猪群进行药物预防，控制细菌性继发感染。在发病高峰前，可在饲料中添加对继发性细菌感染敏感的抗菌药物及增强机体非特异性免疫力的药物。如“骏安”（乙酰戊乙酰泰乐菌素——第2代替米考星）、替米考星、加康（10%氟苯尼考）、枝原净、强力霉素、黄芪多糖等。 `source_id=SRC-0089; page=145; line=3091`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
- `SFDUT1-TX-0722` treatment_or_prevention / p.188 / 猪巴氏杆菌病: 个体治疗可选用第3代头孢菌素类和氟喹诺酮类，这是目前治疗本病最有效的药物。也可酌情选用氨基糖苷类、氨苄西林、阿莫西林、氟苯尼考、长效土霉素、强力霉素、磺胺类药物。预防用药可在饲料中添加选用氟苯尼考、泰乐菌素与磺胺二甲嘧啶联用等都有较好疗效。治疗时一般采用交叉用药，用药前尽可能先做药敏试验而后选用最敏感的药物。 `source_id=SRC-0089; page=188; line=3740`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-015-tylosin.md`
- Byte size moved: 10173
- Fact-like rows moved: 23
- Candidate fact mentions moved: 10
- Dose/route/course fact markers moved: 6
- Source anchors moved: 23

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 23 linked drug-use facts.
- Source pages: 192, 193, 194, 195, 217, 222, 235, 236, 246, 257, 269, 283, 295, 306, 307.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0003` treatment_or_prevention / p.192 / 猪支原体肺炎: 多种喹诺酮类药、抗生素类药如林可霉素、泰妙菌素、泰乐菌素、替米考星、乙酰异戊酰泰乐菌素、四环素、土霉素、强力霉素、金霉素、卡那霉素等对猪支原体肺炎均有较好的治疗作用。 `source_id=SRC-0090; page=192; line=41`
- `SFDUT2-TX-0008` dose_route_course / p.192 / 猪支原体肺炎: ④ 泰乐菌素注射液，20毫克/千克，一天1次，连用 $3 \sim 5$ 天。 `source_id=SRC-0090; page=192; line=48`
- `SFDUT2-TX-0014` candidate_fact / p.193 / 猪支原体肺炎: ② $8.8\%$ 磷酸泰乐菌素预混剂200克 $+15\%$ 金霉素预混剂2000克。 `source_id=SRC-0090; page=193; line=61`
- `SFDUT2-TX-0016` candidate_fact / p.194 / 猪支原体肺炎: ④ $20\%$ 乙酰异戊酰泰乐菌素（又名泰万菌素、万乐霉素）预混剂400克。 `source_id=SRC-0090; page=194; line=63`
- `SFDUT2-TX-0031` treatment_or_prevention / p.195 / 猪支原体肺炎: 总之，控制猪气喘病需要采取综合防制的办法。其中重点是要建立健康的种猪群，母猪临产前7天和分娩后7天，用泰乐菌素、泰妙菌素或土霉素拌料饲喂，防止经母猪把疾病传给仔猪。其次是要抓好仔猪的疾病预防控制。搞好环境卫生消毒和一栏或一舍的全进全出。定期检查、立即隔离发病猪；根据猪群具体情况采取定时用药、预防用药策略。只有从总体采取合理的综合防治措施，才能有效地控制猪气喘病的发生和流行。 `source_id=SRC-0090; page=195; line=95`
- `SFDUT2-TX-0098` candidate_fact / p.217 / 猪传染性胸膜肺炎: ⑥ 其他如爱乐新、泰乐菌素、泰乐菌素十金霉素、泰妙菌素、利高霉素等也可用。混饲最好与抗菌增效剂TMP合用（5:1），以增强疗效。 `source_id=SRC-0090; page=217; line=400`
- `SFDUT2-TX-0111` candidate_fact / p.222 / 猪传染性萎缩性鼻炎: ④ 混饲给药 每吨饲料中可添加：a. 泰乐菌素 100 克 + 磺胺二甲基嘧啶 100 克；b. 强力霉素 150 克；c. 拜尔“利好”20% 复方磺胺间甲氧嘧啶，首次量 2000 克，维持量 1000 克，连用 7 天。 `source_id=SRC-0090; page=222; line=472`
- `SFDUT2-TX-0138` treatment_or_prevention / p.235 / 猪增生性肠炎: 常用于治疗回肠炎的抗生素有泰妙菌素、泰乐菌素、林可霉素、金霉素、强力霉素等。但治疗时常面临失败的可能，失败的原因可能有：①猪发病期间，采食量下降，因而药物的吸收量不足；②用药途径不合理，急性感染猪不能通过饮水或饲料获得治疗量的药物；③胞内劳氏菌间歇性排菌，故治疗时间难以确定或治疗太晚，在疾病的后期用药效果不理想；④抗生素的耐药性问题；⑤抗生素的有效作用时间有限。为此要根据发病猪的年龄和病的类型采用不同的治疗方法。新引进种猪在混群前，应采用治疗剂量水平的抗菌药物，通过混饲进行口服给药连续治疗14天，以防发生临床症状。治疗处方是每吨饲料中添加 $80\%$ 泰妙菌素预混剂120克、泰乐菌素100克（效价）或林可霉素110克（效价）。 `source_id=SRC-0090; page=235; line=667`
- `SFDUT2-TX-0139` treatment_or_prevention / p.235 / 猪增生性肠炎: （1）急性回肠炎需要采取得力的治疗方法，治疗既包括临床感染的猪，也包括有接触的猪。首选的治疗药物是每吨饲料添加 $80\%$ 泰妙菌素预混剂150克或泰乐菌素100克（效价）或林可霉素110克（效价），可通过预混料口服，连续治疗14天。 `source_id=SRC-0090; page=235; line=669`
- `SFDUT2-TX-0140` dose_route_course / p.235 / 猪增生性肠炎: ① 诺华公司生产的注射用延胡索泰妙菌素（泰妙灵、枝原净），肌内注射，一次量，15毫克/千克体重，每天1次，连用 $3\sim$ 5天。注意事项：a. 要现配现用，当天用完；b. 不能与泰乐菌素、氟苯尼考、林可霉素联用，否则由于互相竞争作用部位而导致减效。 `source_id=SRC-0090; page=235; line=673`
- `SFDUT2-TX-0141` dose_route_course / p.236 / 猪增生性肠炎: ② 泰乐菌素注射液或注射用酒石酸泰乐菌素，10毫克/千克体重，每天2次，连用5天。 `source_id=SRC-0090; page=236; line=674`
- `SFDUT2-TX-0143` vaccination_or_immunization / p.236 / 猪增生性肠炎: （2）严重的慢性回肠炎 对 $6 \sim 10$ 周龄、临床表现为猪体消瘦、有或无坏死性肠炎的病例，在胞内劳氏菌感染高峰刚到之前就将抗菌药物通过预混料给药，能够取得很好的治疗效果。添加抗菌药物的时间不可太迟或过早。太迟不能减轻临床症状；反之，如果添加时间太早，那么“洁净”的猪群没有机会产生对此病的主动免疫，仍维持其原有的易感状态，从而在以后更容易发生严重急性回肠炎。治疗处方是：每吨饲料添加 $80\%$ 泰妙菌素预混剂150克，或每吨饲料添加美国礼来公司 $8.8\%$ 磷酸盐泰乐菌素预混剂250克，连用14天。 `source_id=SRC-0090; page=236; line=679`
- `SFDUT2-TX-0171` dose_route_course / p.246 / 猪痢疾: ① 注射用酒石酸泰乐菌素，肌注，一次量，10毫克/千克体重，每天2次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=246; line=852`
- `SFDUT2-TX-0172` dose_route_course / p.246 / 猪痢疾: ② 酒石酸泰乐菌素可溶性粉，混饮， $5\sim 10$ 毫克/千克体重，或每升水添加50毫克，连用 $5\sim 7$ 天。 `source_id=SRC-0090; page=246; line=853`
- `SFDUT2-TX-0173` candidate_fact / p.246 / 猪痢疾: ③ 磷酸泰乐菌素预混剂，混饲，每吨饲料100克（效价），给药 $2\sim 4$ 周。 `source_id=SRC-0090; page=246; line=854`
- `SFDUT2-TX-0205` dose_route_course / p.257 / 猪衣原体病: 首选四环素类抗生素（强力霉素、金霉素、土霉素）进行预防和治疗。为了完全排除或抑制潜伏性感染，公母猪在配种前 $1 \sim 2$ 周，应按治疗水平通过饮水或混饲，连续给药 $2 \sim 3$ 周，治疗不充分时可引起复发。对怀孕母猪在产前 $2 \sim 3$ 周混饲 $10 \sim 15$ 天以预防新生仔猪感染本病。也可选用青霉素、氟苯尼考、大环内酯类（泰乐菌素、乙酰异戊酰泰乐菌素）等抗菌药物。在流行期，也可每吨饲料添加 $15\%$ 金霉素预混剂2000克或强力霉素150克（效价），母猪群体预防。为了防止出现耐药性，要合理交替用药。对出现临床症状的猪，可肌内注射辉瑞“得米先”（ $20\%$ 长效土霉素注射液），每10千克体重肌注1毫升，每3天1次，连用3次；或土霉素注射液，20毫升/千克体重，每天1次，连续治疗 $5 \sim 7$ 天；或肌注强力霉素注射液，3毫克/千克体重，每天1次，连用5天。 `source_id=SRC-0090; page=257; line=1029`
- `SFDUT2-TX-0235` treatment_or_prevention / p.269 / 仔猪球虫病: （5）在仔猪球虫病发病严重的猪场，在仔猪 $3 \sim 6$ 日龄（5日龄最佳）时使用“百球清”或磺胺二甲氧嘧啶和泰乐菌素复方制剂溶液或 $5\%$ 的三嗪酮悬液，对小猪进行灌服，有一定预防效果。当怀疑仔猪发生球虫病时，用同样方法进行治疗，连用5天，患病仔猪应同时灌服口服补液盐，防止脱水死亡。 `source_id=SRC-0090; page=269; line=1238`
- `SFDUT2-TX-0266` candidate_fact / p.283 / 产后泌乳障碍综合征: ② 产前 $5 \sim 7$ 天至产后7天，每吨饲料中添加如下抗菌药物：辉瑞“利高霉素-44”1.5千克，或“金西林”1.25千克，或加康400克，或 $80\%$ 枝原净（ $80\%$ 泰妙菌素）125克 $+15\%$ 金霉素2000克，或泰乐菌素110克 $+SM_{2}110$ 克，或爱乐新1.5千克。 `source_id=SRC-0090; page=283; line=1445`
- `SFDUT2-TX-0295` candidate_fact / p.295 / 母猪产后泌尿生殖系统疾病: ② 产前5天至产后7天，每吨饲料中添加如下抗菌药物：辉瑞“利高霉素-44”1.5千克，或“金西林”1.25千克，或腾骏“加康”400克，或酒石酸乙酰异戊酰泰乐菌素预混剂（腾骏“骏安”、荷本“万乐福欣”、伊科拜克“爱乐新”） $50\sim 70$ 克（效价），或诺华“枝原净”（ $80\%$ 泰妙菌素）125克 $+15\%$ 金霉素2000克，或泰乐菌素110克。 `source_id=SRC-0090; page=295; line=1619`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
- `SFDUT2-TX-0339` candidate_fact / p.307 / 猪呼吸道病综合征: ③ 骏安（20%第2代替米考星——乙酰异戊酰泰乐菌素）500克+强力霉素（效价）200克。 `source_id=SRC-0090; page=307; line=1795`
- `SFDUT2-TX-0341` candidate_fact / p.307 / 猪呼吸道病综合征: ⑤ 泰乐菌素（效价）100克+磺胺二甲嘧啶100克+磺胺增效剂20克。 `source_id=SRC-0090; page=307; line=1797`
- `SFDUT2-TX-0342` candidate_fact / p.307 / 猪呼吸道病综合征: ⑥ 泰乐菌素（效价）100克 $+15\%$ 金霉素2000克（或强力霉素150克）。 `source_id=SRC-0090; page=307; line=1798`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-015-tylosin.md`
- Byte size moved: 1230
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-070-DRUG-015-tylosin-md-2913` 泰乐菌素 / 大环内酯类 / p.70：Tylosin 【药理作用及适应证】动物专用。抗菌谱同红霉素，对革兰阳性菌作用弱于红霉素，抗支原体作用强，对敏感菌并发支原体感染尤为有效。主要用于防治猪、禽支原体病，如鸡慢性呼吸道病、传染性窦腔炎，猪弧菌性痢疾、传染性胸膜肺炎，牛莫拉菌感染及犬结肠炎等；亦用于浸泡种蛋预防鸡支原体传播。本品内服可吸收，有效血药浓度维持时间短，肌注吸收迅速，组织药物浓度比内服高 $2\sim 3$ 倍，有效浓度维持时间较长；体内分布广泛主要经肾脏和胆汁排泄。 `source_id=SRC-0091; page=70`
<!-- RAU_1_200_V14_END -->
