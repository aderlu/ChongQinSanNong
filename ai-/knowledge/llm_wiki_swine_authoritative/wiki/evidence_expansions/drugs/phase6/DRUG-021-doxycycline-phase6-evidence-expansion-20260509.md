---
page_id: DRUG-021-doxycycline
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase6_drug_page_compaction
moved_from: wiki/drugs/DRUG-021-doxycycline.md
generated: 2026-05-09T14:25:31+08:00
---

# DRUG-021-doxycycline Phase 6 Evidence Expansion

This file stores high-density batch evidence moved out of the default runtime drug page during Phase 6.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any treatment parameter, withdrawal-period, MRL, residue, or food-safety conclusion still requires current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-021-doxycycline.md`
- Byte size moved: 770
- Fact-like rows moved: 3
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 3

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 3 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 强力霉素.
- Source pages: 27, 35, 42.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0022` 猪圆环病毒2型感染 / 处方1 `source_id=SRC-0087; page=27; line=1092-1100`
- `HANDBOOK-RX-0041` 仔猪副伤寒或猪沙门菌病 / 处方4 `source_id=SRC-0087; page=35; line=1482-1490`
- `HANDBOOK-RX-0055` 猪肺疫 / 处方2 `source_id=SRC-0087; page=42; line=1760-1768`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-021-doxycycline.md`
- Byte size moved: 1720
- Fact-like rows moved: 5
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 5

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 4 appendix medicine rows and 1 text treatment mentions linked to this drug page.
- Source pages: 26, 116, 156.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0105` HydroDoxx (500 mg doxycycline/g): dose=10 mg doxycycline/kg in drinking water for 5 days; meat_withhold=6 days. `source_id=SRC-0088; page=156; table=Table A.3.`
- `VTOP-MED-0111` Pulmodox Granules for Oral Solution (500 mg doxycycline/g): dose=12.5 mg/kg in drinking water for 4 days; meat_withhold=4 days. `source_id=SRC-0088; page=156; table=Table A.3.`
- `VTOP-MED-0113` Soludox 500 mg/g Water Soluble Powder for Pigs (500 mg doxycycline/g): dose=20 mg/kg in drinking water for 5 days; meat_withhold=4 days. `source_id=SRC-0088; page=26; table=Table A.3.`
- `VTOP-MED-0114` Soludox 500 mg/g Water Soluble Powder for Pigs and Chickens (500 mg doxycycline/g): dose=20 mg/kg in drinking water for 5 days; meat_withhold=4 days. `source_id=SRC-0088; page=26; table=Table A.3.`
- `VTOP-TX-0238` euthanasia / p.116 / Pemphigus: Autoimmune diseases are seen in pigs but they are extremely rare. Diagnosis will be achieved by ruling out other causes for the erythematous, pruritic patches on the skin. Diagnosis could be confirmed by histopathology. Treatment is with corticosteroids in pet pigs. Initially dexamethazone can be injected at $2 \mathrm { \ m g } / 2 5 \mathrm { \ k g }$ every $^ { 4 8 \mathrm { ~ h ~ } }$ with antibiotic cover. Then  `source_id=SRC-0088; page=116; line=3148`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-021-doxycycline.md`
- Byte size moved: 8041
- Fact-like rows moved: 14
- Candidate fact mentions moved: 1
- Dose/route/course fact markers moved: 3
- Source anchors moved: 14

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 14 linked drug-use facts.
- Source pages: 25, 44, 49, 50, 51, 61, 73, 78, 145, 151, 188.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0087` compliance_or_safety / p.25 / 掌握好妊娠母猪禁用或慎用的药物: 13. 慎用强力霉素（多西环素） `source_id=SRC-0089; page=25; line=824`
- `SFDUT1-TX-0087` compliance_or_safety / p.25 / 掌握好妊娠母猪禁用或慎用的药物: 13. 慎用强力霉素（多西环素） `source_id=SRC-0089; page=25; line=824`
- `SFDUT1-TX-0210` dose_route_course / p.49 / 四环素类: ① 盐酸多西环素片，内服，一次量，每千克体重 $3 \sim 5$ 毫克，1次/天，连用 $3 \sim 5$ 天。 `source_id=SRC-0089; page=49; line=1379`
- `SFDUT1-TX-0211` dose_route_course / p.50 / 四环素类: ② 注射用盐酸强力霉素粉针，静注，一次量，每千克体重5毫克，用 $5\%$ 葡萄糖注射液配制成 $0.1\%$ 以下浓度，缓慢注入，不可漏于皮下，1次/天，连用 $3\sim 5$ 天。 `source_id=SRC-0089; page=50; line=1380`
- `SFDUT1-TX-0212` dose_route_course / p.50 / 四环素类: ③ 长效盐酸多西环素注射液，肌注，一次量，每千克体重10毫克，1次/天，连用 $3 \sim 5$ 天。 `source_id=SRC-0089; page=50; line=1381`
- `SFDUT1-TX-0213` drug_interaction / p.50 / 四环素类: ④ 混饲，盐酸强力霉素粉（以有效成分计），每吨饲料添加 $150 \sim 200$ 克，连用 $5 \sim 7$ 天。或与有协同作用的其他抗生素联用。 `source_id=SRC-0089; page=50; line=1382`
- `SFDUT1-TX-0237` treatment_or_prevention / p.51 / 大环内酯类: ① $20\%$ 乙酰异戊酰泰乐菌素预混剂（腾骏“骏安”），对于保育猪前、中期经常发病，母猪出现繁殖障碍的猪场，可采用如下预防和控制措施，以本品计，混饲，种公、母猪（包括后备母猪）：每月7天，每吨饲料250克，控制支原体及细菌性疾病，防止疾病在母猪群中循环传染给仔猪；怀孕母猪：产前5天至产后7天，每吨饲料250克（也可外加强力霉素200克），切断细菌性疾病的垂直传播；保育猪：断奶当天至断奶后7天，每吨饲料500克，或断奶后8天至转群，每吨饲料250克，防止呼吸道和肠道疾病。 `source_id=SRC-0089; page=51; line=1486`
- `SFDUT1-TX-0250` treatment_or_prevention / p.44 / 氟苯尼考: （3）本品可与四环素类（如强力霉素、金霉素等）、黏杆菌素联合使用，呈相加作用，因为作用机制不同，不竞争作用位置。也可与氨基糖苷类联用，治疗需氧及厌氧菌混合感染所致的败血症及 `source_id=SRC-0089; page=44; line=1531`
- `SFDUT1-TX-0257` treatment_or_prevention / p.61 / 氟苯尼考: （5）传染性胸膜肺炎、副猪嗜血杆菌病、猪肺疫等的治疗：发病初期，患病猪群还有较好的食欲时，混饲给药时可适当提高添加量，每吨饲料可添加氟苯尼考（效价）100克，最好再配合强力霉素（效价）200克，连用7天，有较好效果。对传染性疾病引起的发热、咳嗽、气喘，单独使用抗菌药物即可，无需添加其他解热镇痛、止咳平喘类药物。如果病猪出现高热、不食，则要进行隔离治疗，使用氟苯尼考注射液肌内注射；若体温超过 $41^{\circ}\mathrm{C}$ 时，可配合解热镇痛药及地塞米松使用，效果更佳。 `source_id=SRC-0089; page=61; line=1560`
- `SFDUT1-TX-0312` treatment_or_prevention / p.73 / 磺胺类药物及抗菌增效剂: 磺胺类药物（SAs）是指具有对氨基苯磺酰胺结构的一类用于预防和治疗全身各系统细菌感染的化学合成药物的总称。磺胺类药物作为应用最早的（1935年合成百浪多息）一类人工合成的抗菌药物，有其独特的优点：抗菌谱广、疗效确实、性质稳定、不易变质、使用方便、能大量生产、价格相对低廉。但同时也有抗菌作用较弱、不良反应较多、细菌易产生耐药性、用量大、疗程偏长等缺陷。在发现了甲氧苄啶（TMP）和二甲氧苄啶（DVD）等抗菌增效剂后，把磺胺药和抗菌增效剂联合使用，使抗菌活性和疗效大大增强，甚至从抑菌剂变为杀菌剂，因此，磺胺类药至今仍为猪抗感染治疗中的重要药物之一，在临床上仍广泛应用。除用于治疗的针剂外，主要通过拌料或饮水做脉冲式药物保健。保健时往往配伍使用强力霉素等四环素类药物、枝原净（泰妙菌素）、泰乐菌素或氟苯尼考等。 `source_id=SRC-0089; page=73; line=1843`
- `SFDUT1-TX-0333` drug_interaction / p.78 / 磺胺类药物及抗菌增效剂: ② $62.5\%$ 复方磺胺氯达嗪钠粉能有效控制弓形体、萎缩性鼻炎、乳房炎、子宫炎及巴氏杆菌、链球菌、大肠杆菌、胸膜肺炎放线杆菌、沙门菌等感染。每吨饲料添加 $300 \sim 500$ 克“康舒秘”成品，或每吨水添加 $150 \sim 250$ 克“康舒秘”成品，每次连用7天。作为一种慢效抑菌剂，“康舒秘”与快效抑菌剂强力霉素联合具有协同作用，能更有效地控制敏感菌感染。如能使用枝原净十强力霉素十康舒秘的黄金三宝组合，还能有效控制肺炎支原体等感染引起的呼吸道病综合征（PRDC）。因肺炎支原体是引起PRDC的钥匙病原和导火线，控制好支原体也可减轻蓝耳病对机体的损伤。 `source_id=SRC-0089; page=78; line=1958`
- `SFDUT1-TX-0627` vaccination_or_immunization / p.145 / 猪繁殖与呼吸障碍综合征: 九是对猪群进行药物预防，控制细菌性继发感染。在发病高峰前，可在饲料中添加对继发性细菌感染敏感的抗菌药物及增强机体非特异性免疫力的药物。如“骏安”（乙酰戊乙酰泰乐菌素——第2代替米考星）、替米考星、加康（10%氟苯尼考）、枝原净、强力霉素、黄芪多糖等。 `source_id=SRC-0089; page=145; line=3091`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
- `SFDUT1-TX-0722` treatment_or_prevention / p.188 / 猪巴氏杆菌病: 个体治疗可选用第3代头孢菌素类和氟喹诺酮类，这是目前治疗本病最有效的药物。也可酌情选用氨基糖苷类、氨苄西林、阿莫西林、氟苯尼考、长效土霉素、强力霉素、磺胺类药物。预防用药可在饲料中添加选用氟苯尼考、泰乐菌素与磺胺二甲嘧啶联用等都有较好疗效。治疗时一般采用交叉用药，用药前尽可能先做药敏试验而后选用最敏感的药物。 `source_id=SRC-0089; page=188; line=3740`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-021-doxycycline.md`
- Byte size moved: 9740
- Fact-like rows moved: 22
- Candidate fact mentions moved: 11
- Dose/route/course fact markers moved: 4
- Source anchors moved: 22

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 22 linked drug-use facts.
- Source pages: 192, 193, 202, 216, 217, 218, 222, 235, 257, 259, 263, 306, 307.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0003` treatment_or_prevention / p.192 / 猪支原体肺炎: 多种喹诺酮类药、抗生素类药如林可霉素、泰妙菌素、泰乐菌素、替米考星、乙酰异戊酰泰乐菌素、四环素、土霉素、强力霉素、金霉素、卡那霉素等对猪支原体肺炎均有较好的治疗作用。 `source_id=SRC-0090; page=192; line=41`
- `SFDUT2-TX-0013` candidate_fact / p.193 / 猪支原体肺炎: ① $80\%$ 泰妙菌素预混剂（枝原净）125克 $+10\%$ 盐酸多西环素预混剂1000克。 `source_id=SRC-0090; page=193; line=60`
- `SFDUT2-TX-0054` treatment_or_prevention / p.202 / 副猪嗜血杆菌病: （6）在日粮或饮水中添加药物进行预防，并要科学用药 本病在严重暴发时，使用药物预防可能无效。为此，应摸清本病在本场的发病规律，应在发病前3周提前对整个猪群进行药物预防。有条件的最好能做药敏测验，采用敏感药物，但用药量不可过少，防止产生耐药性，或在全群的饮水中添加阿莫西林或强力霉素。 `source_id=SRC-0090; page=202; line=191`
- `SFDUT2-TX-0084` candidate_fact / p.216 / 猪传染性胸膜肺炎: （1）推荐注射用药方案 应选择对革兰阴性菌敏感的药物。首选药物是头孢噻呋（或头孢噻肟）和氟苯尼考。强力霉素、庆大霉素配合阿莫西林、恩诺沙星、磺胺六甲氧、泰妙菌素、阿奇霉素等可酌情选用。 `source_id=SRC-0090; page=216; line=379`
- `SFDUT2-TX-0087` dose_route_course / p.216 / 猪传染性胸膜肺炎: ③ 复方盐酸多西环素（强力霉素）注射液，2.5毫克/千克体重，1次/天，连用 $3 \sim 5$ 天。 `source_id=SRC-0090; page=216; line=382`
- `SFDUT2-TX-0087` dose_route_course / p.216 / 猪传染性胸膜肺炎: ③ 复方盐酸多西环素（强力霉素）注射液，2.5毫克/千克体重，1次/天，连用 $3 \sim 5$ 天。 `source_id=SRC-0090; page=216; line=382`
- `SFDUT2-TX-0096` candidate_fact / p.217 / 猪传染性胸膜肺炎: ④ 强力霉素300克（效价），连用2周。 `source_id=SRC-0090; page=217; line=398`
- `SFDUT2-TX-0100` candidate_fact / p.218 / 猪传染性胸膜肺炎: ① 每100升饮水中添加强力霉素15克，连续混饮5天，同时添加可溶性多维添加剂。 `source_id=SRC-0090; page=218; line=404`
- `SFDUT2-TX-0107` treatment_or_prevention / p.222 / 猪传染性萎缩性鼻炎: ① 母猪和仔猪 为了减少母猪的感染及传播，可在母猪产仔前在饲料中添加药物以达到治疗的目的。可用磺胺二甲基嘧啶或强力霉素拌在饲料中。哺乳仔猪在 $3 \sim 4$ 周龄注射较大剂量的抗菌剂进行治疗。最有效的有增效磺胺、土霉素、青霉素及链霉素。如果仔猪主要由支气管波氏杆菌感染，则磺胺是首选药物。在 $3 \sim 4$ 周龄时，最好每周给 $1 \sim 2$ 次长效药物，如果细菌没有产生耐药性，长效药物应对治疗巴氏杆菌病很有效。试验证明，长效土霉素能降低鼻腔感染的患病率和由多杀性巴氏杆菌引起鼻甲骨萎缩程度。也可使用强力霉素。 `source_id=SRC-0090; page=222; line=464`
- `SFDUT2-TX-0111` candidate_fact / p.222 / 猪传染性萎缩性鼻炎: ④ 混饲给药 每吨饲料中可添加：a. 泰乐菌素 100 克 + 磺胺二甲基嘧啶 100 克；b. 强力霉素 150 克；c. 拜尔“利好”20% 复方磺胺间甲氧嘧啶，首次量 2000 克，维持量 1000 克，连用 7 天。 `source_id=SRC-0090; page=222; line=472`
- `SFDUT2-TX-0138` treatment_or_prevention / p.235 / 猪增生性肠炎: 常用于治疗回肠炎的抗生素有泰妙菌素、泰乐菌素、林可霉素、金霉素、强力霉素等。但治疗时常面临失败的可能，失败的原因可能有：①猪发病期间，采食量下降，因而药物的吸收量不足；②用药途径不合理，急性感染猪不能通过饮水或饲料获得治疗量的药物；③胞内劳氏菌间歇性排菌，故治疗时间难以确定或治疗太晚，在疾病的后期用药效果不理想；④抗生素的耐药性问题；⑤抗生素的有效作用时间有限。为此要根据发病猪的年龄和病的类型采用不同的治疗方法。新引进种猪在混群前，应采用治疗剂量水平的抗菌药物，通过混饲进行口服给药连续治疗14天，以防发生临床症状。治疗处方是每吨饲料中添加 $80\%$ 泰妙菌素预混剂120克、泰乐菌素100克（效价）或林可霉素110克（效价）。 `source_id=SRC-0090; page=235; line=667`
- `SFDUT2-TX-0205` dose_route_course / p.257 / 猪衣原体病: 首选四环素类抗生素（强力霉素、金霉素、土霉素）进行预防和治疗。为了完全排除或抑制潜伏性感染，公母猪在配种前 $1 \sim 2$ 周，应按治疗水平通过饮水或混饲，连续给药 $2 \sim 3$ 周，治疗不充分时可引起复发。对怀孕母猪在产前 $2 \sim 3$ 周混饲 $10 \sim 15$ 天以预防新生仔猪感染本病。也可选用青霉素、氟苯尼考、大环内酯类（泰乐菌素、乙酰异戊酰泰乐菌素）等抗菌药物。在流行期，也可每吨饲料添加 $15\%$ 金霉素预混剂2000克或强力霉素150克（效价），母猪群体预防。为了防止出现耐药性，要合理交替用药。对出现临床症状的猪，可肌内注射辉瑞“得米先”（ $20\%$ 长效土霉素注射液），每10千克体重肌注1毫升，每3天1次，连用3次；或土霉素注射液，20毫升/千克体重，每天1次，连续治疗 $5 \sim 7$ 天；或肌注强力霉素注射液，3毫克/千克体重，每天1次，连用5天。 `source_id=SRC-0090; page=257; line=1029`
- `SFDUT2-TX-0209` candidate_fact / p.259 / 1. 病原学: 过去曾将猪附红细胞体列为立克次体目、无浆体科、附红细胞体属。但近几年，对病原的基因测序与种系遗传分析认为附红细胞体与支原体相似，无细胞壁，无鞭毛，对青霉素类不敏感，而对强力霉素等四环素类抗生素敏感，故将其更名为猪嗜血支原体。 `source_id=SRC-0090; page=259; line=1063`
- `SFDUT2-TX-0213` dose_route_course / p.263 / 8. 综合防治: （2）急性感染时，可肌注烟台绿叶“炎沙”注射液（ $20\%$ 长效土霉素），每千克体重0.1毫升，隔日一次，连用 $2 \sim 3$ 次，重症每天一次；或辉瑞“得米仙”；也可肌注 $5\%$ 强力霉素注射液，每千克体重0.2毫升，每天1次，连用 $3 \sim 5$ 天。 `source_id=SRC-0090; page=263; line=1132`
- `SFDUT2-TX-0215` treatment_or_prevention / p.263 / 8. 综合防治: （4）在常发地区和流行时节，对病猪群饲料中添加四环素类抗生素或砷制剂预防。如每吨饲料中添加 $15\%$ 金霉素预混剂2000克或回盛生物的“附红特乐”（有效成分盐酸多西环素及增效剂）1000克，或强力霉素可溶性粉150克（效价）+磺胺增效剂（TMP）20克，连用 $7\sim 10$ 天；也可每吨饲料中添加阿散酸180克，连用1周，以后改为90克，连用15天。 `source_id=SRC-0090; page=263; line=1136`
- `SFDUT2-TX-0215` treatment_or_prevention / p.263 / 8. 综合防治: （4）在常发地区和流行时节，对病猪群饲料中添加四环素类抗生素或砷制剂预防。如每吨饲料中添加 $15\%$ 金霉素预混剂2000克或回盛生物的“附红特乐”（有效成分盐酸多西环素及增效剂）1000克，或强力霉素可溶性粉150克（效价）+磺胺增效剂（TMP）20克，连用 $7\sim 10$ 天；也可每吨饲料中添加阿散酸180克，连用1周，以后改为90克，连用15天。 `source_id=SRC-0090; page=263; line=1136`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
- `SFDUT2-TX-0337` candidate_fact / p.307 / 猪呼吸道病综合征: ① $80\%$ 泰妙菌素（枝原净）125克 $+15\%$ 金霉素2000克（或强力霉素150克）。 `source_id=SRC-0090; page=307; line=1793`
- `SFDUT2-TX-0338` candidate_fact / p.307 / 猪呼吸道病综合征: ② $5\%$ 爱乐新1000克+强力霉素150克（或 $15\%$ 金霉素2000克）。 `source_id=SRC-0090; page=307; line=1794`
- `SFDUT2-TX-0339` candidate_fact / p.307 / 猪呼吸道病综合征: ③ 骏安（20%第2代替米考星——乙酰异戊酰泰乐菌素）500克+强力霉素（效价）200克。 `source_id=SRC-0090; page=307; line=1795`
- `SFDUT2-TX-0342` candidate_fact / p.307 / 猪呼吸道病综合征: ⑥ 泰乐菌素（效价）100克 $+15\%$ 金霉素2000克（或强力霉素150克）。 `source_id=SRC-0090; page=307; line=1798`
- `SFDUT2-TX-0343` candidate_fact / p.307 / 猪呼吸道病综合征: ⑦ $10\%$ 氟苯尼考500克+强力霉素200克+TMP100克。 `source_id=SRC-0090; page=307; line=1799`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-021-doxycycline.md`
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

- `RAU1-DRUG-063-DRUG-021-doxycycline-md-9259` 多西环素 / 四环素类 / p.63：目录定位显示 `多西环素` 属于 `四环素类`，可作为药物召回、类别边界和联用禁忌复核入口。 `source_id=SRC-0091; page=63`
<!-- RAU_1_200_V14_END -->
