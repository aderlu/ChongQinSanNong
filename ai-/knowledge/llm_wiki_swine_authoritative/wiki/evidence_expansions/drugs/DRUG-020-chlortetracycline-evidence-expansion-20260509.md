---
page_id: DRUG-020-chlortetracycline
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase3_drug_evidence_expansion
moved_from: wiki/drugs/DRUG-020-chlortetracycline.md
generated: 2026-05-09T11:42:41+08:00
---

# DRUG-020-chlortetracycline Evidence Expansion

This file stores detailed batch evidence moved out of the runtime drug page during Phase 3 cleanup.

Runtime rule:

- Do not load this file for default production/evaluation retrieval.
- Load it only for evidence expansion, audit, source lookup, or manual review.
- Dose, route, course, withdrawal period, MRL, residue, and food-safety claims still require current label/regulatory verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-020-chlortetracycline.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 4

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Mentions (SRC-0087, V13.1 batch)

- Batch status: 4 prescription-drug mention rows from `raw/md/猪病诊疗与处方手册.md`.
- Matched mention terms: 金霉素.
- Source pages: 29, 35, 37, 160.
- Full drug mention index: `exports/handbook_prescription_drug_mention_index.csv`; prescription matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0031` 仔猪白痢 / 处方2 `source_id=SRC-0087; page=29; line=1210-1230`
- `HANDBOOK-RX-0038` 仔猪副伤寒或猪沙门菌病 / 处方1 `source_id=SRC-0087; page=35; line=1448-1456`
- `HANDBOOK-RX-0046` 猪传染性萎缩性鼻炎 / 处方1 `source_id=SRC-0087; page=37; line=1568-1580`
- `HANDBOOK-RX-0368` 子宫内膜炎 / 处方1 `source_id=SRC-0087; page=160; line=6782-6802`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-020-chlortetracycline.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 2

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Medicine Evidence (SRC-0088, V13.1 batch)

- Batch status: 1 appendix medicine rows and 1 text treatment mentions linked to this drug page.
- Source pages: 47, 156.
- Medicine index: `exports/veterinary_treatment_of_pigs_medicine_index.csv`; treatment matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`.

- `VTOP-MED-0102` Chlorsol (50% w/w chlortetracycline): dose=20 mg/kg in drinking water for 5 days; meat_withhold=6 days. `source_id=SRC-0088; page=156; table=Table A.3.`
- `VTOP-TX-0127` vaccination / p.47 / Introduction: Prevention is best achieved by keeping a closed herd and by carrying out strict biosecurity. Veterinary surgeons should be mindful of not risking the introduction of disease by their routine visit. Ideally they should be ‘pig free’ for 3 days before a visit to a high health status herd. Vaccination is extremely useful. Good ventilation and temperature control are vital. Antibiotics should be used responsibly. A study `source_id=SRC-0088; page=47; line=2184`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-020-chlortetracycline.md`
- Candidate facts: 5
- Dose/route/course facts: 3
- Source anchors: 12

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 12 linked drug-use facts.
- Source pages: 31, 44, 46, 48, 59, 63, 65, 66, 151, 172.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0105` drug_interaction / p.31 / 肆霉素类: ④ 本品还与下列药物有配伍禁忌：氨基糖苷类、林可霉素、氟苯尼考、泰妙菌素、土霉素、四环素、金霉素、多黏菌素、红霉素、氯丙嗪、碳酸氢钠、葡萄糖酸钙、氯化钙、肾上腺类、B族维生素、维生素C、磺胺类药物。 `source_id=SRC-0089; page=31; line=916`
- `SFDUT1-TX-0186` candidate_fact / p.48 / 四环素类: 本类药物的盐酸盐水溶液为强酸性，有较强的刺激性，内服后对消化道黏膜有直接刺激，引起厌食、呕吐、腹泻等症状；肌注可引起局部肿胀、疼痛、炎症和坏死；静注可引起静脉炎。这些刺激性，以金霉素最强，土霉素次之，四环素最轻。除土霉素外，本类药物不宜肌注，静脉注射宜用稀溶液，缓慢滴注。不同土霉素制剂对组织的刺激强度相差较大，浓度为 $20\%$ 的长效土霉素对组织的刺激性特别强，其长效作用与其在注射部位缓慢释放有关。 `source_id=SRC-0089; page=48; line=1295`
- `SFDUT1-TX-0188` candidate_fact / p.48 / 四环素类: 长期或过量使用（尤其是金霉素）或大剂量静注，可致严重的 `source_id=SRC-0089; page=48; line=1307`
- `SFDUT1-TX-0207` dose_route_course / p.46 / 四环素类: ② 注射用盐酸金霉素，静注，一次量，每千克体重 $5 \sim 10$ 毫克，临用时用专用溶剂（甘氨酸钠）稀释。 `source_id=SRC-0089; page=46; line=1369`
- `SFDUT1-TX-0208` candidate_fact / p.46 / 四环素类: ③ 混饲，4月龄以内猪，每吨饲料添加 $15\%$ 饲料级金霉素预混剂 $200 \sim 500$ 克，用于促生长； $80\%$ 泰妙菌素（枝原净）预混剂 $125$ 克 $+15\%$ 金霉素预混剂 $2000$ 克，于仔猪断奶后饲喂 $10 \sim 14$ 天，有利于控制呼吸道疾病综合征及增生性肠炎等。 `source_id=SRC-0089; page=46; line=1371`
- `SFDUT1-TX-0250` treatment_or_prevention / p.44 / 氟苯尼考: （3）本品可与四环素类（如强力霉素、金霉素等）、黏杆菌素联合使用，呈相加作用，因为作用机制不同，不竞争作用位置。也可与氨基糖苷类联用，治疗需氧及厌氧菌混合感染所致的败血症及 `source_id=SRC-0089; page=44; line=1531`
- `SFDUT1-TX-0272` drug_interaction / p.66 / 泰妙菌素与沃尼妙林: （2）本类药物与金霉素以 $1:4$ 配伍混饲有协同作用，可治疗猪细菌性肠炎、细菌性肺炎、短螺旋体性猪痢疾（血痢），对肺炎支原体、支气管败血波氏杆菌、多杀性巴氏杆菌和胸膜肺炎放线杆菌等混合感染所引起的肺炎疗效显著。 `source_id=SRC-0089; page=66; line=1665`
- `SFDUT1-TX-0283` candidate_fact / p.59 / 泰妙菌素与沃尼妙林: （1）适应证及特点 本品是一种新型动物专用抗生素，抗菌谱广，对革兰阳性菌、部分革兰阴性菌和支原体均有作用；对猪痢疾短螺旋体、结肠菌毛样短螺旋体、细胞内劳森菌、葡萄球菌、链球菌、猪肺炎支原体、猪滑液支原体、猪胸膜肺炎放线杆菌等均有较强的抑制作用；对支原体属和螺旋体属高度敏感。对细胞内劳森菌的抑制效果优于金霉素、林可霉素、泰妙菌素、泰乐菌素。 `source_id=SRC-0089; page=59; line=1696`
- `SFDUT1-TX-0284` dose_route_course / p.63 / 泰妙菌素与沃尼妙林: （2）盐酸沃尼妙林治疗猪混合感染型呼吸道病猪的混合型呼吸道感染具有普遍性，给养猪者造成巨大的经济损失。临床研究表明混合型感染主要为肺炎支原体、多杀性巴氏杆菌、胸膜肺炎放线菌，有时还有大肠杆菌和猪链球菌感染。研究者对猪人工感染肺炎支原体、多杀性巴氏杆菌和胸膜炎放线菌，然后用替米考星300毫克/千克、泰妙菌素100毫克/千克+金霉素400毫克/千克、沃尼 `source_id=SRC-0089; page=63; line=1700`
- `SFDUT1-TX-0285` dose_route_course / p.65 / 泰妙菌素与沃尼妙林: 妙林25毫克/千克+金霉素400毫克/千克、沃尼妙林75毫克/千克+金霉素400毫克/千克进行治疗。结果表明沃尼妙林+金霉素显著优于替米考星组，肺病变最小，饲料转化率和体增重最好，对呼吸道病原体具广谱的治疗作用。其他研究也表明沃尼妙林与金霉素结合对猪呼吸道病原体 $51\%$ 呈协同作用， $49\%$ 呈相加作用。 `source_id=SRC-0089; page=65; line=1702`
- `SFDUT1-TX-0638` candidate_fact / p.151 / 猪圆环病毒病: 如氟甲砜霉素（氟苯尼考）、强力霉素、土霉素、金霉素、枝原净、泰乐菌素、爱乐新、阿莫西林、林可霉素等。因为不同猪场混合或继发感染的细菌不完全一样，单纯使用一种抗生素不能完全覆盖所要控制的细菌，因此必须采用药物组合的方法，既要控制支原体，又要控制链球菌、巴氏杆菌、猪副嗜血杆菌、胸膜肺炎放线杆菌以及沙门菌等。为减少猪肺炎支原体的影响，并控制继发感染，每吨饲料可添加 $80\%$ 枝原净（泰妙菌素）125克 $+15\%$ 金霉素2000克（或强力霉素200克）。具体用药时间为：断奶仔猪，断奶后连续喂14天。保育猪也可添加泰乐菌素100克 $+$ 磺胺二甲基嘧啶220克，或爱乐新1000克，用药时间：断奶后喂2周。如果发现有猪链球菌或副猪嗜血杆菌并发感染，可同时在饲料中添加 $70\%$ 阿莫西林300克或者 $10\%$ 氟苯尼考800克。还可采用“脉冲式”投药方法，即以一定的间隔短期投药，如7天用药、3天停药 `source_id=SRC-0089; page=151; line=3161`
- `SFDUT1-TX-0685` treatment_or_prevention / p.172 / 猪流行性感冒: （7）在改善饲养管理基础上，积极做好病猪的治疗工作。发病时一般用柴胡、复方氨基比林、安乃近或对乙酰氨基酚注射液等解热镇痛药对症疗法以减轻症状和使用抗生素或磺胺类药物防控继发感染，如饲料添加阿莫西林、金霉素、氟苯尼考等，也可添加黄芪多糖和电解多维。还可采用中药方剂治疗。治疗人流感常用的抗病毒药物，对猪流感病毒也有较好的良效。在加强护理基础上进行对症治疗，才能收到好的效果。 `source_id=SRC-0089; page=172; line=3509`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-020-chlortetracycline.md`
- Candidate facts: 8
- Dose/route/course facts: 1
- Source anchors: 12

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 12 linked drug-use facts.
- Source pages: 192, 193, 217, 235, 257, 263, 283, 295, 307.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0003` treatment_or_prevention / p.192 / 猪支原体肺炎: 多种喹诺酮类药、抗生素类药如林可霉素、泰妙菌素、泰乐菌素、替米考星、乙酰异戊酰泰乐菌素、四环素、土霉素、强力霉素、金霉素、卡那霉素等对猪支原体肺炎均有较好的治疗作用。 `source_id=SRC-0090; page=192; line=41`
- `SFDUT2-TX-0014` candidate_fact / p.193 / 猪支原体肺炎: ② $8.8\%$ 磷酸泰乐菌素预混剂200克 $+15\%$ 金霉素预混剂2000克。 `source_id=SRC-0090; page=193; line=61`
- `SFDUT2-TX-0098` candidate_fact / p.217 / 猪传染性胸膜肺炎: ⑥ 其他如爱乐新、泰乐菌素、泰乐菌素十金霉素、泰妙菌素、利高霉素等也可用。混饲最好与抗菌增效剂TMP合用（5:1），以增强疗效。 `source_id=SRC-0090; page=217; line=400`
- `SFDUT2-TX-0138` treatment_or_prevention / p.235 / 猪增生性肠炎: 常用于治疗回肠炎的抗生素有泰妙菌素、泰乐菌素、林可霉素、金霉素、强力霉素等。但治疗时常面临失败的可能，失败的原因可能有：①猪发病期间，采食量下降，因而药物的吸收量不足；②用药途径不合理，急性感染猪不能通过饮水或饲料获得治疗量的药物；③胞内劳氏菌间歇性排菌，故治疗时间难以确定或治疗太晚，在疾病的后期用药效果不理想；④抗生素的耐药性问题；⑤抗生素的有效作用时间有限。为此要根据发病猪的年龄和病的类型采用不同的治疗方法。新引进种猪在混群前，应采用治疗剂量水平的抗菌药物，通过混饲进行口服给药连续治疗14天，以防发生临床症状。治疗处方是每吨饲料中添加 $80\%$ 泰妙菌素预混剂120克、泰乐菌素100克（效价）或林可霉素110克（效价）。 `source_id=SRC-0090; page=235; line=667`
- `SFDUT2-TX-0205` dose_route_course / p.257 / 猪衣原体病: 首选四环素类抗生素（强力霉素、金霉素、土霉素）进行预防和治疗。为了完全排除或抑制潜伏性感染，公母猪在配种前 $1 \sim 2$ 周，应按治疗水平通过饮水或混饲，连续给药 $2 \sim 3$ 周，治疗不充分时可引起复发。对怀孕母猪在产前 $2 \sim 3$ 周混饲 $10 \sim 15$ 天以预防新生仔猪感染本病。也可选用青霉素、氟苯尼考、大环内酯类（泰乐菌素、乙酰异戊酰泰乐菌素）等抗菌药物。在流行期，也可每吨饲料添加 $15\%$ 金霉素预混剂2000克或强力霉素150克（效价），母猪群体预防。为了防止出现耐药性，要合理交替用药。对出现临床症状的猪，可肌内注射辉瑞“得米先”（ $20\%$ 长效土霉素注射液），每10千克体重肌注1毫升，每3天1次，连用3次；或土霉素注射液，20毫升/千克体重，每天1次，连续治疗 $5 \sim 7$ 天；或肌注强力霉素注射液，3毫克/千克体重，每天1次，连用5天。 `source_id=SRC-0090; page=257; line=1029`
- `SFDUT2-TX-0215` treatment_or_prevention / p.263 / 8. 综合防治: （4）在常发地区和流行时节，对病猪群饲料中添加四环素类抗生素或砷制剂预防。如每吨饲料中添加 $15\%$ 金霉素预混剂2000克或回盛生物的“附红特乐”（有效成分盐酸多西环素及增效剂）1000克，或强力霉素可溶性粉150克（效价）+磺胺增效剂（TMP）20克，连用 $7\sim 10$ 天；也可每吨饲料中添加阿散酸180克，连用1周，以后改为90克，连用15天。 `source_id=SRC-0090; page=263; line=1136`
- `SFDUT2-TX-0266` candidate_fact / p.283 / 产后泌乳障碍综合征: ② 产前 $5 \sim 7$ 天至产后7天，每吨饲料中添加如下抗菌药物：辉瑞“利高霉素-44”1.5千克，或“金西林”1.25千克，或加康400克，或 $80\%$ 枝原净（ $80\%$ 泰妙菌素）125克 $+15\%$ 金霉素2000克，或泰乐菌素110克 $+SM_{2}110$ 克，或爱乐新1.5千克。 `source_id=SRC-0090; page=283; line=1445`
- `SFDUT2-TX-0295` candidate_fact / p.295 / 母猪产后泌尿生殖系统疾病: ② 产前5天至产后7天，每吨饲料中添加如下抗菌药物：辉瑞“利高霉素-44”1.5千克，或“金西林”1.25千克，或腾骏“加康”400克，或酒石酸乙酰异戊酰泰乐菌素预混剂（腾骏“骏安”、荷本“万乐福欣”、伊科拜克“爱乐新”） $50\sim 70$ 克（效价），或诺华“枝原净”（ $80\%$ 泰妙菌素）125克 $+15\%$ 金霉素2000克，或泰乐菌素110克。 `source_id=SRC-0090; page=295; line=1619`
- `SFDUT2-TX-0337` candidate_fact / p.307 / 猪呼吸道病综合征: ① $80\%$ 泰妙菌素（枝原净）125克 $+15\%$ 金霉素2000克（或强力霉素150克）。 `source_id=SRC-0090; page=307; line=1793`
- `SFDUT2-TX-0338` candidate_fact / p.307 / 猪呼吸道病综合征: ② $5\%$ 爱乐新1000克+强力霉素150克（或 $15\%$ 金霉素2000克）。 `source_id=SRC-0090; page=307; line=1794`
- `SFDUT2-TX-0340` candidate_fact / p.307 / 猪呼吸道病综合征: ④ 林可霉素 150 克 + 15% 金霉素 2000 克。 `source_id=SRC-0090; page=307; line=1796`
- `SFDUT2-TX-0342` candidate_fact / p.307 / 猪呼吸道病综合征: ⑥ 泰乐菌素（效价）100克 $+15\%$ 金霉素2000克（或强力霉素150克）。 `source_id=SRC-0090; page=307; line=1798`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-020-chlortetracycline.md`
- Candidate facts: 0
- Dose/route/course facts: 0
- Source anchors: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-064-DRUG-020-chlortetracycline-md-7791` 金霉素 / 四环素类 / p.64：目录定位显示 `金霉素` 属于 `四环素类`，可作为药物召回、类别边界和联用禁忌复核入口。 `source_id=SRC-0091; page=64`
<!-- RAU_1_200_V14_END -->
