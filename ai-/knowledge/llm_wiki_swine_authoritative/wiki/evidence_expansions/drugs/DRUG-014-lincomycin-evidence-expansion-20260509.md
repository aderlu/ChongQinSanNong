---
page_id: DRUG-014-lincomycin
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase3_drug_evidence_expansion
moved_from: wiki/drugs/DRUG-014-lincomycin.md
generated: 2026-05-09T11:42:41+08:00
---

# DRUG-014-lincomycin Evidence Expansion

This file stores detailed batch evidence moved out of the runtime drug page during Phase 3 cleanup.

Runtime rule:

- Do not load this file for default production/evaluation retrieval.
- Load it only for evidence expansion, audit, source lookup, or manual review.
- Dose, route, course, withdrawal period, MRL, residue, and food-safety claims still require current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-014-lincomycin.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 1

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 1 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 林可霉素.
- Source pages: 53.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0077` 猪支原体肺炎 / 处方3 `source_id=SRC-0087; page=53; line=2216-2221`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-014-lincomycin.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 4

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 3 appendix medicine rows and 1 text treatment mentions linked to this drug page.
- Source pages: 73, 154, 156.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0066` Kefloril 300 mg/ml Lincocin Sterile Solution Lincojet 10% (300 mg florfenicol/ml 100 mg lincomycin/ml 100 mg lincomycin/ml): dose=1 ml/20 kg im every 48 h 1 ml/9–22 kg im daily 1 ml/9–22 kg im daily; meat_withhold=18 3 3 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0106` Linco-Spectin 100 Soluble Powder (33.3 g lincomycin + 66.7 g spectinomycin per pack): dose=10 mg/kg in drinking water for 7 days; meat_withhold=0 days. `source_id=SRC-0088; page=156; table=Table A.3.`
- `VTOP-MED-0107` Lincocin Soluble Powder (400 g lincomycin/g): dose=4.5 mg/kg in drinking water for a minimum of 5 days; meat_withhold=0 days. `source_id=SRC-0088; page=156; table=Table A.3.`
- `VTOP-TX-0099` dose_or_route / p.73 / Proliferative enteropathy: Treatment of the individual pig is best carried out with long-acting tetracycline by intramuscular injection. Tetracyclines or tylosin are the antibiotics of choice for group therapy in the drinking water. Some authorities favour tiamulin or lincomycin, particularly if there are other enteric pathogens involved. Tetracyclines may be effective given in the feed but levels should be higher than standard, in the region  `source_id=SRC-0088; page=73; line=2014`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-014-lincomycin.md`
- Candidate facts: 8
- Dose/route/course facts: 2
- Source anchors: 22

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 22 linked drug-use facts.
- Source pages: 10, 13, 21, 27, 31, 34, 36, 43, 44, 45, 48, 53, 59, 78, 83, 151.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0018` candidate_fact / p.10 / 兽药使用必须遵循的基本原则: （1）抗生素、合成抗菌药：头孢哌酮、头孢噻肟、头孢曲松（头孢三嗪）、头孢噻吩、头孢拉啶、头孢唑啉、头孢噻啶、罗红霉素、克拉霉素、阿奇霉素、磷霉素、硫酸奈替米星、氟罗沙星、司帕沙星、甲替沙星、克林霉素（氯林可霉素、氯洁霉素）、妥布霉素、胍哌甲基四环素、盐酸甲烯土霉素（美他环素）、两性霉素、利福霉素等。 `source_id=SRC-0089; page=10; line=525`
- `SFDUT1-TX-0031` treatment_or_prevention / p.13 / 兽药使用必须遵循的基本原则: （4）大环内酯类 大环内酯类与磺胺二甲嘧啶、磺胺嘧啶、磺胺间甲氧嘧啶、TMP的复方可用于治疗呼吸道病。泰乐菌素可与磺胺类合用。红霉素不宜与 $\beta$ -内酰胺类、林可霉素、氯霉素类、 `source_id=SRC-0089; page=13; line=591`
- `SFDUT1-TX-0032` treatment_or_prevention / p.13 / 兽药使用必须遵循的基本原则: （6）林可酰胺类 林可霉素可与四环素或氟哌酸配合应用于治疗合并感染，林可霉素可与壮观霉素合用（利高霉素）治疗慢性呼吸道病。此外，林可霉素可与新霉素、恩诺沙星合用。 `source_id=SRC-0089; page=13; line=596`
- `SFDUT1-TX-0033` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （9）喹诺酮类 喹诺酮类与杀菌药（青霉素类、氨基糖苷类）及TMP在治疗特定细菌感染方面有协同作用。喹诺酮类药物+林可霉素可用于治疗支原体合并大肠杆菌感染引起的呼吸道和肠道感染。喹诺酮类药物与氯霉素类、大环内酯类（如红霉素）合用有拮抗作用。喹诺酮类药物可与磺胺类药物配伍应用，合用对大肠杆菌和金黄色葡萄球菌有相加作用。喹诺酮类慎与氨茶碱合用。 `source_id=SRC-0089; page=13; line=599`
- `SFDUT1-TX-0066` treatment_or_prevention / p.21 / 正确处理对因治疗与对症治疗: 针对发生疾病的原因进行的治疗称为对因治疗，目的在于消除疾病的原发致病因子，中医称“治本”。一般情况下，首先要对因治疗，即“治本”，选择使用消除病因的药物。例如，猪场最常见的猪气喘病，病因是感染了肺炎支原体，所以要选用枝原净、泰乐菌素、恩诺沙星、林可霉素等敏感药物肌注，彻底杀灭支原体。对因治疗要彻底，用药量要足，首次可加倍，疗程要够，一般用药 $3\sim 5$ 天；疗程不足或症状改善即停药，一是易复发，二是易诱发耐药性。 `source_id=SRC-0089; page=21; line=746`
- `SFDUT1-TX-0092` treatment_or_prevention / p.27 / 肆霉素类: 其作用机理主要是干扰转肽酶、破坏细菌细胞壁的合成而产生杀菌作用。它能抑制细菌细胞壁的基础成分黏肽的合成，造成细胞壁缺损而失去屏障保护作用，使水分渗入细菌胞浆，导致菌体肿胀、变形，最后裂解而死亡。 $\mathrm{G}^{+}$ 菌的细胞壁主要由黏肽（达 $65\% \sim 95\%$ ）组成，而 $\mathrm{G}^{-}$ 菌细胞壁的主要成分是磷脂（黏肽仅占 $1\% \sim 10\%$ ），由于 $\mathrm{G}^{+}$ 菌的细胞壁黏肽含量较 $\mathrm{G}^{-}$ 菌高，故对 $\mathrm{G}^{+}$ 菌作用很强，而对 $\mathrm{G}^{-}$ 菌作用较弱。另外，生长期的敏感菌分裂旺盛，细胞壁处于生物合成期，在青霉素的作用下，黏肽的合成受阻不能形成细胞壁，在渗透压作用下，导致细胞膜破裂而死亡，这一过程发生在细菌细胞的繁殖期，因此，本类药物为繁殖期快效杀菌剂，对已形成细胞壁的或者非生长繁殖的细菌，此时不需要合成细胞壁，则青霉素不起杀菌作用，故临床上应避免将青霉素这类“繁殖期杀菌药”与抑制细菌生长繁殖的“快效抑菌药”（如氟苯尼考、四环素类、红霉素等）合用，尤其是在治疗脑膜炎或需迅 `source_id=SRC-0089; page=27; line=853`
- `SFDUT1-TX-0105` drug_interaction / p.31 / 肆霉素类: ④ 本品还与下列药物有配伍禁忌：氨基糖苷类、林可霉素、氟苯尼考、泰妙菌素、土霉素、四环素、金霉素、多黏菌素、红霉素、氯丙嗪、碳酸氢钠、葡萄糖酸钙、氯化钙、肾上腺类、B族维生素、维生素C、磺胺类药物。 `source_id=SRC-0089; page=31; line=916`
- `SFDUT1-TX-0114` drug_interaction / p.31 / 肆霉素类: （3）注意事项 阿莫西林与喹诺酮类、氨基糖苷类抗菌药物联合应用，有协同或相加作用。但与四环素类、氟苯尼考、大环内酯类及林可霉素联用，可能发生拮抗作用。其他参见注射用氨苄西林钠。 `source_id=SRC-0089; page=31; line=938`
- `SFDUT1-TX-0119` candidate_fact / p.34 / 头孢菌素类: （1）作用与用途 本品为半合成的第三代动物专用头孢菌素，具有广谱杀菌作用。一些研究者所做的头孢噻呋对兽医临床分离的数千株病原菌的抑菌实验结果表明，本药是抗菌活性最强的药物之一。对 $\mathbf{G}^{+}$ 菌、 $\mathbf{G}^{-}$ 菌（包括产 $\beta$ 内酰胺酶菌）及一些厌氧菌均有效。敏感菌主要有多杀性巴氏杆菌、溶血性巴氏杆菌、胸膜肺炎放线杆菌、副猪嗜血杆菌、大肠杆菌、沙门菌、链球菌、葡萄球菌等，但支气管败血波氏杆菌、某些铜绿假单胞菌、肠球菌、衣原体耐药。本品抗菌活性比氨苄西林强，对链球菌的活性比氟喹诺酮类强。兽医临床主要用于 $\mathbf{G}^{+}$ 和 $\mathbf{G}^{-}$ 菌感染，如猪胸膜肺炎放线杆菌、副猪嗜血杆菌、多杀性巴氏杆菌、大肠杆菌、猪霍乱沙门菌及链球菌等引起的感染及呼吸道病（猪细菌性肺炎）。注射本品后，15分钟内可迅速被吸收，并有消除半衰期长的特点，对传染性胸膜肺炎及副猪嗜血杆菌病的疗效较阿莫西林、林可霉素-大观霉素（利高霉素）显著，建议首选。 `source_id=SRC-0089; page=34; line=974`
- `SFDUT1-TX-0176` candidate_fact / p.45 / 氨基糖苷类: （1）规格 1000克：林可霉素222克与大观霉素444克。 `source_id=SRC-0089; page=45; line=1243`
- `SFDUT1-TX-0177` treatment_or_prevention / p.45 / 氨基糖苷类: （2）作用与用途 林可霉素对革兰阳性菌和支原体有抑制作用，大观霉素对革兰阴性菌和支原体有抑制作用。本品对 $\mathbf{G}^{+}$ 菌和 $\mathbf{G}^{-}$ 菌均有抗菌作用，抗菌活性和范围比单用一种明显扩大和增强，对支原体也有明显效用。用于防治大肠杆菌及沙门菌引起的感染、支原体肺炎、猪呼吸道病综合征（PRDC）和密螺旋体性痢疾等。 `source_id=SRC-0089; page=45; line=1245`
- `SFDUT1-TX-0181` candidate_fact / p.45 / 氨基糖苷类: （1）规格 100 克：林可霉素 2.2 克与大观霉素 2.2 克。 `source_id=SRC-0089; page=45; line=1257`
- `SFDUT1-TX-0182` treatment_or_prevention / p.45 / 氨基糖苷类: (2) 作用与用途 同盐酸林可霉素、硫酸大观霉素可溶性粉,用于防治猪沙门菌及大肠杆菌性肠炎、猪气喘病和密螺旋体性痢疾等, 疗效较泰乐菌素强。 `source_id=SRC-0089; page=45; line=1258`
- `SFDUT1-TX-0239` candidate_fact / p.53 / 大环内酯类: ② $5 \%$ 乙酰异戊酰泰乐菌素预混剂（回盛“治嗽静”、伊科“爱乐新”），以本品计，混饲，每吨饲料1000克，连用7天。注意：禁止与泰妙菌素、林可霉素、氟苯尼考及大环内酯类其他药物联用。搅拌配料时，防止与皮肤、眼睛接触。 `source_id=SRC-0089; page=53; line=1490`
- `SFDUT1-TX-0248` drug_interaction / p.36 / 氟苯尼考: （1）本品不宜与大环内酯类（如泰乐菌素、红霉素、替米考星、吉他霉素等）、林可胺类（如林可霉素）及双萜类半合成抗生素——泰妙菌素（枝原净）联合用药，合用时可产生拮抗作用。因为它们的作用机制相同，均是与细菌核糖体50S亚基结合，后三类抗生素可替代或阻止氟苯尼考与细菌核糖体的50S亚基相结合，即由于竞争作用部位而导致减效。 `source_id=SRC-0089; page=36; line=1529`
- `SFDUT1-TX-0264` dose_route_course / p.43 / 林可霉素: ② 混饮：以林可霉素计（注：1.13克盐酸林可霉素相当于林可霉素1克），每升水 $40\sim 70$ 毫克，连用7天。 `source_id=SRC-0089; page=43; line=1618`
- `SFDUT1-TX-0265` candidate_fact / p.44 / 林可霉素: ③ 混饲：以林可霉素计，每吨饲料添加 $44 \sim 77$ 克，连用 $1 \sim 3$ 周或症状消失为止。孕猪产前7天至产后7天，按55克/吨给药，在产仔数、初生窝重、断奶窝重方面都可获得较好效果，并可减少腹泻。 `source_id=SRC-0089; page=44; line=1619`
- `SFDUT1-TX-0266` treatment_or_prevention / p.48 / 林可霉素: （1）作用与用途 同盐酸林可霉素可溶性粉。当用于治疗时可有效控制由肺炎支原体引起的猪气喘病及呼吸道病综合征(PRDC)、猪痢疾。 `source_id=SRC-0089; page=48; line=1623`
- `SFDUT1-TX-0283` candidate_fact / p.59 / 泰妙菌素与沃尼妙林: （1）适应证及特点 本品是一种新型动物专用抗生素，抗菌谱广，对革兰阳性菌、部分革兰阴性菌和支原体均有作用；对猪痢疾短螺旋体、结肠菌毛样短螺旋体、细胞内劳森菌、葡萄球菌、链球菌、猪肺炎支原体、猪滑液支原体、猪胸膜肺炎放线杆菌等均有较强的抑制作用；对支原体属和螺旋体属高度敏感。对细胞内劳森菌的抑制效果优于金霉素、林可霉素、泰妙菌素、泰乐菌素。 `source_id=SRC-0089; page=59; line=1696`
- `SFDUT1-TX-0326` dose_route_course / p.78 / 磺胺类药物及抗菌增效剂: ③ 磺胺嘧啶钠注射液，规格： $10\%$ 、 $20\%$ ，用于敏感菌引起的感染（为脑膜炎的首选药物）及猪弓形虫病。深部肌注、静脉注射，一次量，每千克体重50毫克，2次/天，连用 $2 \sim 3$ 天。注意：本品遇酸可析出结晶，故不宜用 $5\%$ 葡萄糖液稀释；本品不可与四环素、卡那霉素、阿米卡星、林可霉素等配合使用。 `source_id=SRC-0089; page=78; line=1938`
- `SFDUT1-TX-0354` treatment_or_prevention / p.83 / 氟喹诺酮类药物: （3）氟喹诺酮类与林可霉素联用，对葡萄球菌、链球菌等革兰阳性菌作用增强；可用于治疗猪支原体肺炎（猪气喘病）或肺炎支 `source_id=SRC-0089; page=83; line=2058`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-014-lincomycin.md`
- Candidate facts: 3
- Dose/route/course facts: 5
- Source anchors: 14

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 14 linked drug-use facts.
- Source pages: 192, 210, 235, 244, 246, 251, 252, 306, 307.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0003` treatment_or_prevention / p.192 / 猪支原体肺炎: 多种喹诺酮类药、抗生素类药如林可霉素、泰妙菌素、泰乐菌素、替米考星、乙酰异戊酰泰乐菌素、四环素、土霉素、强力霉素、金霉素、卡那霉素等对猪支原体肺炎均有较好的治疗作用。 `source_id=SRC-0090; page=192; line=41`
- `SFDUT2-TX-0006` dose_route_course / p.192 / 猪支原体肺炎: ② 林可霉素注射液，10毫克/千克，一天1次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=192; line=46`
- `SFDUT2-TX-0075` candidate_fact / p.210 / 猪链球菌病: （3）注意事项 据报道，猪链球菌对四环素、林可霉素、卡那霉素、链霉素均有耐药性。 `source_id=SRC-0090; page=210; line=309`
- `SFDUT2-TX-0138` treatment_or_prevention / p.235 / 猪增生性肠炎: 常用于治疗回肠炎的抗生素有泰妙菌素、泰乐菌素、林可霉素、金霉素、强力霉素等。但治疗时常面临失败的可能，失败的原因可能有：①猪发病期间，采食量下降，因而药物的吸收量不足；②用药途径不合理，急性感染猪不能通过饮水或饲料获得治疗量的药物；③胞内劳氏菌间歇性排菌，故治疗时间难以确定或治疗太晚，在疾病的后期用药效果不理想；④抗生素的耐药性问题；⑤抗生素的有效作用时间有限。为此要根据发病猪的年龄和病的类型采用不同的治疗方法。新引进种猪在混群前，应采用治疗剂量水平的抗菌药物，通过混饲进行口服给药连续治疗14天，以防发生临床症状。治疗处方是每吨饲料中添加 $80\%$ 泰妙菌素预混剂120克、泰乐菌素100克（效价）或林可霉素110克（效价）。 `source_id=SRC-0090; page=235; line=667`
- `SFDUT2-TX-0139` treatment_or_prevention / p.235 / 猪增生性肠炎: （1）急性回肠炎需要采取得力的治疗方法，治疗既包括临床感染的猪，也包括有接触的猪。首选的治疗药物是每吨饲料添加 $80\%$ 泰妙菌素预混剂150克或泰乐菌素100克（效价）或林可霉素110克（效价），可通过预混料口服，连续治疗14天。 `source_id=SRC-0090; page=235; line=669`
- `SFDUT2-TX-0140` dose_route_course / p.235 / 猪增生性肠炎: ① 诺华公司生产的注射用延胡索泰妙菌素（泰妙灵、枝原净），肌内注射，一次量，15毫克/千克体重，每天1次，连用 $3\sim$ 5天。注意事项：a. 要现配现用，当天用完；b. 不能与泰乐菌素、氟苯尼考、林可霉素联用，否则由于互相竞争作用部位而导致减效。 `source_id=SRC-0090; page=235; line=673`
- `SFDUT2-TX-0161` treatment_or_prevention / p.244 / 猪痢疾: （2）猪增生性肠炎（PE）由胞内劳氏菌引起，是 $6\sim 20$ 周龄断奶后的生长肥育猪和后备种猪的一种常见腹泻病，病变主要在小肠。急性型通常发生于4月龄以后的后备种猪及肥育猪，首次观察到的临床症状常常是排出黑色柏油状粪便，皮肤苍白，死亡率高达 $50\%$ ，怀孕母猪可流产。慢性型最常见，一般发生于 $18\sim 36$ 千克体重的猪，临床症状不典型，部分猪出现腹泻时一般都是轻微的，排出正常灰绿色的疏松、稀薄直至水样粪便，出血或黏液粪便并不是慢性增生性肠炎腹泻的特征，主要是影响猪只的生长性能。剖检小肠末端50厘米处及邻近结肠上1/3处，肠壁增厚，有隆起的黏膜，导致肠管变硬，类似胶皮水管样外观。泰妙菌素、大环内酯类、林可霉素治疗有效。而对治疗猪痢疾有特效的痢菌净对本病效果不明显。确诊依赖于粪便PCR试验阳性。 `source_id=SRC-0090; page=244; line=823`
- `SFDUT2-TX-0176` dose_route_course / p.246 / 猪痢疾: ① 盐酸林可霉素注射液，肌注，一次量，10毫克/千克体重，每天2次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=246; line=863`
- `SFDUT2-TX-0177` dose_route_course / p.246 / 猪痢疾: ② 盐酸林可霉素可溶性粉，混饮，8毫克/千克体重，或每升水添加 $40 \sim 70$ 毫克，用药 $5 \sim 7$ 天。 `source_id=SRC-0090; page=246; line=864`
- `SFDUT2-TX-0178` candidate_fact / p.246 / 猪痢疾: ③ 盐酸林可霉素预混剂，混饲，每吨饲料添加100克（效 `source_id=SRC-0090; page=246; line=865`
- `SFDUT2-TX-0194` dose_route_course / p.251 / 仔猪渗出性皮炎: ② 林可霉素注射液，15毫克/千克体重，早晚各肌注一次；中午肌注庆大霉素注射液，8毫克/千克体重；再配合地塞米松磷酸钠注射液，0.2毫克/千克体重，1次/天。 `source_id=SRC-0090; page=251; line=945`
- `SFDUT2-TX-0197` treatment_or_prevention / p.252 / 仔猪渗出性皮炎: （3）局部治疗 可加速康复和防止感染扩散。早期涂擦紫药水，较重者可用温热的消毒剂，如 $0.2\%$ 高锰酸钾或洗必泰、碘伏、百毒杀或双链季铵盐-碘消毒剂等浸泡 $5 \sim 10$ 分钟，待干固的痂皮发软后用毛刷擦洗，去掉痂皮，擦干后涂紫药水。也可涂擦自制的林可霉素软膏（林可霉素粉5克，加入鱼肝油或香油100毫升，混合均匀）或人用红霉素眼膏， $2 \sim 3$ 次/天，至痊愈。 `source_id=SRC-0090; page=252; line=951`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
- `SFDUT2-TX-0340` candidate_fact / p.307 / 猪呼吸道病综合征: ④ 林可霉素 150 克 + 15% 金霉素 2000 克。 `source_id=SRC-0090; page=307; line=1796`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-014-lincomycin.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-073-DRUG-014-lincomycin-md-1070` 林可霉素 / 林可胺类 / p.73：Lincomycin 【药理作用及适应证】又名洁霉素。对革兰阳性菌如葡萄球菌、溶血性链球菌、肺炎球菌、炭疽杆菌等作用较强，但弱于青霉素类和头孢菌素类；对厌氧菌有强大的抑杀作用；对支原体作用与红霉素相似；对猪痢疾密螺旋体有一定作用；对革兰阴性菌无效。与克林霉素完全交叉耐药，与红霉素部分交叉耐药。用于敏感菌感染及猪、鸡的支原体病，猪的密螺旋体血痢等；也作饲料添加剂可促进肉鸡和育肥猪生长，提高饲料利用率。内服吸收不完全，肌注吸收良好。 `source_id=SRC-0091; page=73`
<!-- RAU_1_200_V14_END -->
