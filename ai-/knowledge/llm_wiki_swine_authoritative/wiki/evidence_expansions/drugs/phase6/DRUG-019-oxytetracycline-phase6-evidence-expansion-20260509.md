---
page_id: DRUG-019-oxytetracycline
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase6_drug_page_compaction
moved_from: wiki/drugs/DRUG-019-oxytetracycline.md
generated: 2026-05-09T14:25:31+08:00
---

# DRUG-019-oxytetracycline Phase 6 Evidence Expansion

This file stores high-density batch evidence moved out of the default runtime drug page during Phase 6.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any treatment parameter, withdrawal-period, MRL, residue, or food-safety conclusion still requires current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-019-oxytetracycline.md`
- Byte size moved: 1243
- Fact-like rows moved: 8
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 8

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 8 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 土霉素.
- Source pages: 27, 29, 35, 53, 74, 139, 150.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0022` 猪圆环病毒2型感染 / 处方1 `source_id=SRC-0087; page=27; line=1092-1100`
- `HANDBOOK-RX-0023` 仔猪黄痢 / 处方1 `source_id=SRC-0087; page=29; line=1128-1148`
- `HANDBOOK-RX-0031` 仔猪白痢 / 处方2 `source_id=SRC-0087; page=29; line=1210-1230`
- `HANDBOOK-RX-0041` 仔猪副伤寒或猪沙门菌病 / 处方4 `source_id=SRC-0087; page=35; line=1482-1490`
- `HANDBOOK-RX-0075` 猪支原体肺炎 / 处方1 `source_id=SRC-0087; page=53; line=2202-2208`
- `HANDBOOK-RX-0157` 小袋纤毛虫病 / 处方1 `source_id=SRC-0087; page=74; line=3099-3103`
- `HANDBOOK-RX-0328` 创伤 / 处方3 `source_id=SRC-0087; page=139; line=5893-5903`
- `HANDBOOK-RX-0346` 腐蹄病 / 处方2 `source_id=SRC-0087; page=150; line=6303-6307`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-019-oxytetracycline.md`
- Byte size moved: 5856
- Fact-like rows moved: 21
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 21

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 15 appendix medicine rows and 6 text treatment mentions linked to this drug page.
- Source pages: 46, 57, 87, 92, 116, 152, 153, 154, 155, 156.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0019` Alamycin 10 (100 mg oxytetracycline/ml): dose=1 ml/11–50 kg im daily; meat_withhold=20 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0020` Alamycin LA (200 mg oxytetracycline/ml): dose=1 ml/10 kg im as a single injection; meat_withhold=18 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0021` Alamycin LA 300 (300 mg oxytetracycline/ml): dose=1 ml/10–15 kg im as a single injection; meat_withhold=14–28 (depending on dosage) days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0038` Cyclosol LA (200 mg oxytetracycline/ml): dose=1 ml/10 kg im every 3 days; meat_withhold=28 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0043` Duphacycline 10% (100 mg oxytetracycline/ml): dose=1 ml/11–50 kg im daily; meat_withhold=20 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0044` Duphacycline LA 20% Solution for Injection (200 mg oxytetracycline/ml): dose=1 ml/10 kg im as a single injection; meat_withhold=18 days. `source_id=SRC-0088; page=152; table=Table A.2.`
- `VTOP-MED-0052` Engemycin 10% (DD) (100 mg oxytetracycline/ml): dose=1 ml/12.5 kg im daily or 1 ml/5 kg im every 60 h; meat_withhold=14 (with daily dose)10 (with 60 h dose) days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0053` Engemycin 10% Farm Pack (100 mg oxytetracycline/ml): dose=1 ml/12.5 kg im daily or 1 ml/5 kg im every 60 h; meat_withhold=14 (with daily dose)10 (with 60 h dose) days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0054` Engemycin LA (200 mg oxytetracycline/ml): dose=1 ml/10 kg im as a single injection; meat_withhold=18 days. `source_id=SRC-0088; page=153; table=Table A.2.`
- `VTOP-MED-0078` Oxycare 10% (100 mg oxytetracycline/ml): dose=1 ml/11–50 kg im daily; meat_withhold=20 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0079` Oxycare 20% LA (200 mg oxytetracycline/ml): dose=1 ml/10 kg im as a single injection; meat_withhold=18 days. `source_id=SRC-0088; page=154; table=Table A.2.`
- `VTOP-MED-0080` Oxytetrin 20 LA (200 mg oxytetracycline/ml): dose=1 ml/10 kg im as a single injection; meat_withhold=70 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0089` Terramycin Q-100 mg/ml Solution for Injection (100 mg oxytetracycline/ml): dose=1 ml/10 kg im daily; meat_withhold=21 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0090` Terramycin/LA 200 mg/ml Solution for Injection (200 mg oxytetracycline/ml): dose=1 ml/10 kg im as a single injection; meat_withhold=36 days. `source_id=SRC-0088; page=155; table=Table A.2.`
- `VTOP-MED-0116` Terramycin Soluble Powder Concentrated 20% (200 g oxytetracycline/kg): dose=10–30 mg/kg in drinking water daily for 3–5 days; meat_withhold=7 days. `source_id=SRC-0088; page=156; table=Table A.3.`
- `VTOP-TX-0071` treatment_candidate / p.57 / Infectious mycoplasma: Acute lameness is caused by Mycoplasma hyorhinitis and Mycoplasma hyosynoviae. These should be treated with tylosin or oxytetracycline by injection; both of these antibiotics can be given as a follow-up by water medication. `source_id=SRC-0088; page=57; line=1667`
- `VTOP-TX-0125` dose_or_route / p.46 / Intestinal haemorrhagic syndrome: intestinal torsion. Treatment has been recommended with oxytetracycline at $2 0 ~ \mathrm { m g / k g }$ given im by injection. The author has not found this to be useful even with injections of NSAIDs. Control is to reduce the amount of whey in the diet. `source_id=SRC-0088; page=46; line=2162`
- `VTOP-TX-0134` vaccination / p.46 / Atrophic rhinitis: amoxicillin, enrofloxacin and oxytetracycline. A good control measure is to treat litters of baby pigs with injections of trimethoprim sulfonamide on days 3, 10 and 21. Sows should be vaccinated twice in pregnancy, ideally 5 and 2 weeks before farrowing. Some vaccines are licensed for piglets to be given at 1 and 3 weeks of age. `source_id=SRC-0088; page=46; line=2248`
- `VTOP-TX-0141` vaccination / p.87 / Pasteurellosis: is fever and a nasal discharge. The lung sounds are loud and breathing laboured, often with mouth breathing. Post-mortem will reveal an acute necrotizing and fibrinous pneumonia. Grey areas of consolidation will be seen in the anterior lobes of the lungs. Culture is important not only for diagnosis but also for typing the organism for sensitivity testing. Aggressive antibiotic treatment should be tried using injectio `source_id=SRC-0088; page=87; line=2296`
- `VTOP-TX-0167` treatment_candidate / p.92 / Nephritis/cystitis complex: If several cases occur in a herd then routine treatment with antibiotics of both boars and sows before service may be justified. The author’s preference is long-acting oxytetracycline given by injection at the appropriate time before service in the boar and after service in the sow. If antibiotics are given in the feed or water to all animals in the service area, the danger of antibiotic resistance is high. `source_id=SRC-0088; page=92; line=2458`
- `VTOP-TX-0235` treatment_candidate / p.116 / Bite wounds: These are common after pig groups have been mixed and they may be severe. They require aggressive antibiotic treatment. They should not be sutured but allowed to heal by secondary intention. Precautions should be taken to avoid fly strike. Oxytetracycline aerosols are useful. `source_id=SRC-0088; page=116; line=3122`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-019-oxytetracycline.md`
- Byte size moved: 6881
- Fact-like rows moved: 15
- Candidate fact mentions moved: 6
- Dose/route/course fact markers moved: 4
- Source anchors moved: 15

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 15 linked drug-use facts.
- Source pages: 10, 13, 31, 32, 34, 35, 42, 48, 49, 120, 151, 188.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0018` candidate_fact / p.10 / 兽药使用必须遵循的基本原则: （1）抗生素、合成抗菌药：头孢哌酮、头孢噻肟、头孢曲松（头孢三嗪）、头孢噻吩、头孢拉啶、头孢唑啉、头孢噻啶、罗红霉素、克拉霉素、阿奇霉素、磷霉素、硫酸奈替米星、氟罗沙星、司帕沙星、甲替沙星、克林霉素（氯林可霉素、氯洁霉素）、妥布霉素、胍哌甲基四环素、盐酸甲烯土霉素（美他环素）、两性霉素、利福霉素等。 `source_id=SRC-0089; page=10; line=525`
- `SFDUT1-TX-0030` drug_interaction / p.13 / 兽药使用必须遵循的基本原则: （3）四环素类 四环素类药物与非同类药物如泰妙菌素、泰乐菌素配伍用于胃肠道和呼吸道感染时有协同作用，可降低使用浓度，缩短治疗时间。四环素类与氯霉素类合用有较好的协同作用。土霉素不能与喹乙醇、北里霉素合用。 `source_id=SRC-0089; page=13; line=590`
- `SFDUT1-TX-0105` drug_interaction / p.31 / 肆霉素类: ④ 本品还与下列药物有配伍禁忌：氨基糖苷类、林可霉素、氟苯尼考、泰妙菌素、土霉素、四环素、金霉素、多黏菌素、红霉素、氯丙嗪、碳酸氢钠、葡萄糖酸钙、氯化钙、肾上腺类、B族维生素、维生素C、磺胺类药物。 `source_id=SRC-0089; page=31; line=916`
- `SFDUT1-TX-0186` candidate_fact / p.48 / 四环素类: 本类药物的盐酸盐水溶液为强酸性，有较强的刺激性，内服后对消化道黏膜有直接刺激，引起厌食、呕吐、腹泻等症状；肌注可引起局部肿胀、疼痛、炎症和坏死；静注可引起静脉炎。这些刺激性，以金霉素最强，土霉素次之，四环素最轻。除土霉素外，本类药物不宜肌注，静脉注射宜用稀溶液，缓慢滴注。不同土霉素制剂对组织的刺激强度相差较大，浓度为 $20\%$ 的长效土霉素对组织的刺激性特别强，其长效作用与其在注射部位缓慢释放有关。 `source_id=SRC-0089; page=48; line=1295`
- `SFDUT1-TX-0190` candidate_fact / p.49 / 四环素类: （5）注意事项：①不宜与碳酸氢钠同服，同服后，吸收减少，活性降低；②不宜与氨茶碱等生物碱混合注射，否则将分解失效；③土霉素不能与喹乙醇合用；④禁与B族维生素混用并应避光保存；⑤不要用林格液稀释粉针，防止与钙离子结合。 `source_id=SRC-0089; page=49; line=1321`
- `SFDUT1-TX-0192` dose_route_course / p.32 / 四环素类: ① 土霉素片（粉），内服，一次量，每千克体重 $10 \sim 20$ 毫克， $2 \sim 3$ 次/天，连用 $3 \sim 5$ 天。 `source_id=SRC-0089; page=32; line=1331`
- `SFDUT1-TX-0193` dose_route_course / p.32 / 四环素类: ② 土霉素注射液，肌注，一次量，每千克体重 $10 \sim 20$ 毫克 `source_id=SRC-0089; page=32; line=1332`
- `SFDUT1-TX-0195` dose_route_course / p.34 / 四环素类: ③ $20\%$ 长效土霉素注射液，肌注，一次量，每千克体重20毫克，一般每2天注射一次，重症每天一次，连用 $3 \sim 5$ 次。 `source_id=SRC-0089; page=34; line=1336`
- `SFDUT1-TX-0196` dose_route_course / p.34 / 四环素类: ④ 注射用盐酸土霉素，静注，一次量，每千克体重 $5 \sim 10$ 毫克，2次/天，连用 $2 \sim 3$ 天。 `source_id=SRC-0089; page=34; line=1337`
- `SFDUT1-TX-0197` treatment_or_prevention / p.34 / 四环素类: ⑤ 盐酸土霉素粉（以有效成分计），每吨饲料添加：促生长 $50 \sim 100$ 克，防病 $100 \sim 200$ 克，治疗 $200 \sim 400$ 克，连用 $7 \sim 10$ 天。 `source_id=SRC-0089; page=34; line=1338`
- `SFDUT1-TX-0198` candidate_fact / p.35 / 四环素类: ⑥ $20\%$ 饲用土霉素钙，混饲，每吨饲料添加 $250 \sim 500$ 克，连用 $7 \sim 10$ 天。 `source_id=SRC-0089; page=35; line=1339`
- `SFDUT1-TX-0204` candidate_fact / p.42 / 四环素类: ② 其他同土霉素的注意事项②、③。 `source_id=SRC-0089; page=42; line=1359`
- `SFDUT1-TX-0542` compliance_or_safety / p.120 / 猪疫苗免疫接种应注意的细节: （3）禁用抗菌和抗病毒药物弱毒苗只有在被免疫猪体内生存并繁殖才有效，因此注射活菌苗之前7天和注射之后10天内，均不应饲喂含有抗菌、抑菌药物（如各种抗生素、磺胺类、氟喹诺酮类等）的饲料和添加剂，或混饮、注射任何抗菌药物。猪气喘病活疫苗注射前15天及注射后2个月内禁用土霉素、卡那霉素等药物及含以上药物的配合饲料，否则疫苗中的活菌会被杀死而影响免疫 `source_id=SRC-0089; page=120; line=2715`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
- `SFDUT1-TX-0722` treatment_or_prevention / p.188 / 猪巴氏杆菌病: 个体治疗可选用第3代头孢菌素类和氟喹诺酮类，这是目前治疗本病最有效的药物。也可酌情选用氨基糖苷类、氨苄西林、阿莫西林、氟苯尼考、长效土霉素、强力霉素、磺胺类药物。预防用药可在饲料中添加选用氟苯尼考、泰乐菌素与磺胺二甲嘧啶联用等都有较好疗效。治疗时一般采用交叉用药，用药前尽可能先做药敏试验而后选用最敏感的药物。 `source_id=SRC-0089; page=188; line=3740`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-019-oxytetracycline.md`
- Byte size moved: 8616
- Fact-like rows moved: 14
- Candidate fact mentions moved: 1
- Dose/route/course fact markers moved: 7
- Source anchors moved: 14

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 14 linked drug-use facts.
- Source pages: 192, 195, 222, 229, 257, 263, 280, 284, 293, 295, 306.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0003` treatment_or_prevention / p.192 / 猪支原体肺炎: 多种喹诺酮类药、抗生素类药如林可霉素、泰妙菌素、泰乐菌素、替米考星、乙酰异戊酰泰乐菌素、四环素、土霉素、强力霉素、金霉素、卡那霉素等对猪支原体肺炎均有较好的治疗作用。 `source_id=SRC-0090; page=192; line=41`
- `SFDUT2-TX-0009` dose_route_course / p.192 / 猪支原体肺炎: ⑤ $20\%$ 长效土霉素注射液（得米仙），1毫克/10千克，三天1次，连用3次。 `source_id=SRC-0090; page=192; line=49`
- `SFDUT2-TX-0031` treatment_or_prevention / p.195 / 猪支原体肺炎: 总之，控制猪气喘病需要采取综合防制的办法。其中重点是要建立健康的种猪群，母猪临产前7天和分娩后7天，用泰乐菌素、泰妙菌素或土霉素拌料饲喂，防止经母猪把疾病传给仔猪。其次是要抓好仔猪的疾病预防控制。搞好环境卫生消毒和一栏或一舍的全进全出。定期检查、立即隔离发病猪；根据猪群具体情况采取定时用药、预防用药策略。只有从总体采取合理的综合防治措施，才能有效地控制猪气喘病的发生和流行。 `source_id=SRC-0090; page=195; line=95`
- `SFDUT2-TX-0107` treatment_or_prevention / p.222 / 猪传染性萎缩性鼻炎: ① 母猪和仔猪 为了减少母猪的感染及传播，可在母猪产仔前在饲料中添加药物以达到治疗的目的。可用磺胺二甲基嘧啶或强力霉素拌在饲料中。哺乳仔猪在 $3 \sim 4$ 周龄注射较大剂量的抗菌剂进行治疗。最有效的有增效磺胺、土霉素、青霉素及链霉素。如果仔猪主要由支气管波氏杆菌感染，则磺胺是首选药物。在 $3 \sim 4$ 周龄时，最好每周给 $1 \sim 2$ 次长效药物，如果细菌没有产生耐药性，长效药物应对治疗巴氏杆菌病很有效。试验证明，长效土霉素能降低鼻腔感染的患病率和由多杀性巴氏杆菌引起鼻甲骨萎缩程度。也可使用强力霉素。 `source_id=SRC-0090; page=222; line=464`
- `SFDUT2-TX-0109` treatment_or_prevention / p.222 / 猪传染性萎缩性鼻炎: 磺胺类药物是第一个成功用于控制本病的药物，到目前，此药仍在单用或与其他抗生素以及磺胺增效剂合用。许多猪支气管败血性波氏杆菌的分离物对四环素敏感，这些药物特别是土霉素的长效制剂，对仔猪注射给药，可用于控制本病。新的氟喹诺酮类药物也对猪支气管败血波氏杆菌有效。大多数的抗菌药物可单用也可联合使用，它们既能有效治疗PAR又有助于生长。 `source_id=SRC-0090; page=222; line=468`
- `SFDUT2-TX-0110` dose_route_course / p.222 / 猪传染性萎缩性鼻炎: ③ 个体治疗 肌注，一次量：a. 磺胺类药物配合磺胺增效剂的复方制剂，如复方增效磺胺或复方磺胺嘧啶钠注射液，12.5毫克/千克体重；b. 长效土霉素注射液，20毫克/千克体重；c. 青霉素（4万单位/千克体重）配合卡那霉素（ $20\sim 30$ 毫克/千克体重）或氨苄西林（ $10\sim 20$ 毫克/千克体重）或阿莫西林（ $10\sim 20$ 毫克/千克体重）；d. 氟喹诺酮类注射液， $2.5\sim 5$ 毫克/千克体重；e. 头孢噻呋钠， $5\sim 10$ 毫克/千克体重；f. 仔猪打喷嚏时也可用卡那霉素注射液滴鼻，每天1次，每个鼻孔滴0.5毫升，连用 $2\sim 3$ 天。 `source_id=SRC-0090; page=222; line=470`
- `SFDUT2-TX-0127` treatment_or_prevention / p.229 / 猪大肠杆菌病: ② 在饲料中添加适当的抗菌药物，如土霉素、新霉素等，有一定预防作用。 `source_id=SRC-0090; page=229; line=574`
- `SFDUT2-TX-0205` dose_route_course / p.257 / 猪衣原体病: 首选四环素类抗生素（强力霉素、金霉素、土霉素）进行预防和治疗。为了完全排除或抑制潜伏性感染，公母猪在配种前 $1 \sim 2$ 周，应按治疗水平通过饮水或混饲，连续给药 $2 \sim 3$ 周，治疗不充分时可引起复发。对怀孕母猪在产前 $2 \sim 3$ 周混饲 $10 \sim 15$ 天以预防新生仔猪感染本病。也可选用青霉素、氟苯尼考、大环内酯类（泰乐菌素、乙酰异戊酰泰乐菌素）等抗菌药物。在流行期，也可每吨饲料添加 $15\%$ 金霉素预混剂2000克或强力霉素150克（效价），母猪群体预防。为了防止出现耐药性，要合理交替用药。对出现临床症状的猪，可肌内注射辉瑞“得米先”（ $20\%$ 长效土霉素注射液），每10千克体重肌注1毫升，每3天1次，连用3次；或土霉素注射液，20毫升/千克体重，每天1次，连续治疗 $5 \sim 7$ 天；或肌注强力霉素注射液，3毫克/千克体重，每天1次，连用5天。 `source_id=SRC-0090; page=257; line=1029`
- `SFDUT2-TX-0213` dose_route_course / p.263 / 8. 综合防治: （2）急性感染时，可肌注烟台绿叶“炎沙”注射液（ $20\%$ 长效土霉素），每千克体重0.1毫升，隔日一次，连用 $2 \sim 3$ 次，重症每天一次；或辉瑞“得米仙”；也可肌注 $5\%$ 强力霉素注射液，每千克体重0.2毫升，每天1次，连用 $3 \sim 5$ 天。 `source_id=SRC-0090; page=263; line=1132`
- `SFDUT2-TX-0249` dose_route_course / p.280 / 产后泌乳障碍综合征: （1）抗菌药物疗法 对有临床症状的，由大肠杆菌等 $\mathbf{G}^{-}$ 菌和葡萄球菌、链球菌等 $\mathbf{G}^{+}$ 菌引起的乳腺炎、膀胱炎、肾盂肾炎、子宫内膜炎、产后败血症等患病母猪，应采用抗生素疗法。有条件的应做药敏试验。也可选用对 $\mathbf{G}^{+}$ 菌敏感的青霉素类、第4代头孢菌素——头孢喹诺、大环内酯类抗生素和对 $\mathbf{G}^{-}$ 菌敏感的氨基糖苷类，采用联合用药方式（如青霉素 $+$ 链霉素或青霉素 $+$ 庆大霉素）或使用广谱抗菌药物，如法国施维雅“新素易康”（长效土霉素）或氟喹诺酮类。每头用量：青霉素400万～600万单位，链霉素 `source_id=SRC-0090; page=280; line=1401`
- `SFDUT2-TX-0273` candidate_fact / p.284 / 产后泌乳障碍综合征: ⑧ 临产前 $15 \sim 30$ 天，给母猪肌注亚硒酸钠维生素E注射液 $10 \sim 15$ 毫升，对内毒素有一定保护作用。患疥螨的，可皮下注射伊能净（ $1\%$ 伊维菌素），3毫升/100千克体重。对有附红细胞体威胁的，产前可注射一次新素易康或长效土霉素，10毫升/头，以减 `source_id=SRC-0090; page=284; line=1461`
- `SFDUT2-TX-0282` dose_route_course / p.293 / 母猪产后泌尿生殖系统疾病: 的氨基糖苷类抗生素，采用联合用药方式（如青霉素G+链霉素或青霉素G+庆大霉素）或使用广谱抗菌药物，如得米先（长效土霉素）或氟喹诺酮类。每头每次肌注用量：青霉素G400万单位，链霉素150万～200万单位， $4\%$ 庆大霉素 $10\sim 20$ 毫升，得米先 $10\sim$ 20毫升， $2.5\%$ 氧氟沙星或 $0.5\%$ 恩诺沙星20毫升，以上药物每天两次， $3\sim 5$ 天为一疗程。 `source_id=SRC-0090; page=293; line=1582`
- `SFDUT2-TX-0294` dose_route_course / p.295 / 母猪产后泌尿生殖系统疾病: ① 产后立即或最迟8小时内，对母猪全身使用抗生素，如肌注青霉素G400万单位+链霉素200万单位，2次/天，连用2天；或一次肌注“易速达”（头孢噻呋）10毫升；或“得米先”（长效土霉素）15毫升，这是目前产房常用的措施。 `source_id=SRC-0090; page=295; line=1618`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-019-oxytetracycline.md`
- Byte size moved: 1500
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-059-DRUG-019-oxytetracycline-md-4872` 土霉素 / 四环素类 / p.59：Oxytetracycline 【药理作用及适应证】又名氧四环素。对革兰阳性菌和革兰阴性菌均有较强抗菌作用；对立克次体、衣原体、支原体、螺旋体、放线菌和某些原虫亦有效。用于大肠杆菌或沙门菌引起的犊牛白痢、羔羊痢疾、仔猪黄痢和白痢、雏鸡白痢；多杀性巴氏杆菌引起的牛出败、猪肺疫、禽霍乱等；支原体引起的牛肺炎、猪气喘病、鸡慢性呼吸道病等；局部用于子宫脓肿、子宫内膜炎等；也用于泰勒焦虫病、放线菌病、钩端螺旋体病。本品内服吸收不完全，抑制反刍动物瘤胃微生物活性，肌注给药吸收迅速；吸收后广泛分布于机体各组织和体液中，易渗入胸腔、腹腔、胎畜及乳汁中，不易透过血脑屏障，主要以原型经肾脏排泄，部分经肝肠循环，胆汁和尿 中浓度高。 `source_id=SRC-0091; page=59`
<!-- RAU_1_200_V14_END -->
