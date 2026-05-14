---
page_id: DIS-046
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-046 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- Byte size moved: 1656
- Fact-like rows moved: 3
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 3

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 3 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 53.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0075` 处方1：灭菌花生油或茶油100毫升，土霉素碱25克；用法=用法：混合均匀，按每千克体重 $40\sim 50$ 毫克，在颈、背两侧行深部肌内分点轮流注射，小猪 $1\sim 2$ 毫升，中猪 $3\sim 5$ 毫升，大猪 $5\sim 8$ 毫升，每隔3天1次，5次为一疗程。；注=说明：重症猪可进行 $2\sim 3$ 个疗程，配合卡那霉素注射，效果更好。。`source_id=SRC-0087; page=53; line=2202-2208`
- `HANDBOOK-RX-0076` 处方2：兽用卡那霉素 每千克体重3万～4万单位；用法=用法：肌内注射，每天1次，连续5天为一疗程，必要时进行 $2\sim 3$ 个疗程；但停药后往往复发。；注=。`source_id=SRC-0087; page=53; line=2210-2214`
- `HANDBOOK-RX-0077` 处方3：① 林可霉素按每吨饲料加入200克，连喂3周，或按每千克体重50毫克肌内注射，5天为一疗程，有一定效果。；② 泰乐菌素按每千克体重 $4 \sim 9$ 毫克进行肌内注射，3天为一疗程。；③ 泰妙灵按每千克体重20毫克，掺入饲料饲喂。；④ 治百炎（大观霉素）按每千克体重40毫克，每日肌内注射1次，5天为一疗程，有一定疗效。；用法=；注=。`source_id=SRC-0087; page=53; line=2216-2221`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- Byte size moved: 3048
- Fact-like rows moved: 6
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 6

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Treatment Evidence (SRC-0088, V13.1 batch)

- Batch status: 6 treatment facts linked to this disease page.
- Source pages: 47, 85, 86.
- Full matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`; fact index: `exports/veterinary_treatment_of_pigs_fact_index.csv`.

- `VTOP-TX-0036` vaccination / p.47 / Mycoplasma hyopneumoniae: A single injection to be given between 3 and 10 weeks of age. Certain vaccines can be given as early as 7 days, but the majority of these require two doses 2–4 weeks apart. `source_id=SRC-0088; page=47; line=1418`
- `VTOP-TX-0127` vaccination / p.47 / Introduction: Prevention is best achieved by keeping a closed herd and by carrying out strict biosecurity. Veterinary surgeons should be mindful of not risking the introduction of disease by their routine visit. Ideally they should be ‘pig free’ for 3 days before a visit to a high health status herd. Vaccination is extremely useful. Good ventilation and temperature control are vital. Antibiotics should be used responsibly. A study `source_id=SRC-0088; page=47; line=2184`
- `VTOP-TX-0136` treatment_candidate / p.85 / Enzootic pneumonia: Treatment of enzootic pneumonia is in some ways easy as there are many antibiotics which will treat the disease apparently successfully, but none of them will ever entirely eliminate the organism so that the disease will always return. The use of antibiotics will take time to reduce the lung lesions and restore growth rates but in the end production targets may be met. `source_id=SRC-0088; page=85; line=2264`
- `VTOP-TX-0137` treatment_candidate / p.85 / Enzootic pneumonia: There are better methods of control. The well-tried ‘all-in all-out’ system with treatment on entry will be helpful on a house basis. It will be much more helpful on a whole unit basis. An early weaning system – where the pigs are weaned and moved with treatment to a clean site and reared for 4 weeks, then moved to a grower site for a further 4 weeks before being moved to a clean finisher site – also has merits. Low  `source_id=SRC-0088; page=85; line=2266`
- `VTOP-TX-0138` euthanasia / p.86 / Glasser’s disease: This is an infectious disease caused by Haemophilus parasuis, which is often fatal in growing pigs. The disease is found throughout the world. It is caused by a Gram-negative coccobacillus. It is non-haemolytic and is hard to culture on blood agar. The agar has to be streaked with a Staphylococcus spp. first and then the H. parasuis will grow on the edge of the streak as very small clear colonies. The main clinical s `source_id=SRC-0088; page=86; line=2274`
- `VTOP-TX-0139` treatment_candidate / p.86 / Mycoplasma hyorhinis disease: Treatment is the same as for enzootic pneumonia, with oxytetracyclines, tiamulin and tylosine being most commonly used. In the author’s experience the injectable route is more effective, particularly if NSAIDs are also injected. `source_id=SRC-0088; page=86; line=2286`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- Byte size moved: 5906
- Fact-like rows moved: 10
- Candidate fact mentions moved: 1
- Dose/route/course fact markers moved: 0
- Source anchors moved: 10

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 10 linked disease-control/treatment facts.
- Source pages: 27, 33, 36, 39, 48, 53, 66, 83, 189.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0092` treatment_or_prevention / p.27 / 肆霉素类: 其作用机理主要是干扰转肽酶、破坏细菌细胞壁的合成而产生杀菌作用。它能抑制细菌细胞壁的基础成分黏肽的合成，造成细胞壁缺损而失去屏障保护作用，使水分渗入细菌胞浆，导致菌体肿胀、变形，最后裂解而死亡。 $\mathrm{G}^{+}$ 菌的细胞壁主要由黏肽（达 $65\% \sim 95\%$ ）组成，而 $\mathrm{G}^{-}$ 菌细胞壁的主要成分是磷脂（黏肽仅占 $1\% \sim 10\%$ ），由于 $\mathrm{G}^{+}$ 菌的细胞壁黏肽含量较 $\mathrm{G}^{-}$ 菌高，故对 $\mathrm{G}^{+}$ 菌作用很强，而对 $\mathrm{G}^{-}$ 菌作用较弱。另外，生长期的敏感菌分裂旺盛，细胞壁处于生物合成期，在青霉素的作用下，黏肽的合成受阻不能形成细胞壁，在渗透压作用下，导致细胞膜破裂而死亡，这一过程发生在细菌细胞的繁殖期，因此，本类药物为繁殖期快效杀菌剂，对已形成细胞壁的或者非生长繁殖的细菌，此时不需要合成细胞壁，则青霉素不起杀菌作用，故临床上应避免将青霉素这类“繁殖期杀菌药”与抑制细菌生长繁殖的“快效抑菌药”（如氟苯尼考、四环素类、红霉素等）合用，尤其是在治疗脑膜炎或需迅 `source_id=SRC-0089; page=27; line=853`
- `SFDUT1-TX-0209` treatment_or_prevention / p.48 / 四环素类: （1）作用与用途 用于治疗 $G^{+}$ 、 $G^{-}$ 菌和支原体引起的感染性疾病，如巴氏杆菌病、布氏杆菌病、大肠杆菌病、沙门菌病、猪螺旋体病、猪支原体肺炎、猪附红细胞体病等。本品对呼吸道感染除有抗菌作用外，还有一定祛痰、镇咳、平喘等对症治疗作用。 `source_id=SRC-0089; page=48; line=1375`
- `SFDUT1-TX-0221` treatment_or_prevention / p.36 / 大环内酯类: （1）作用与用途 主要用于治疗对青霉素耐药的金黄色葡萄球菌和其他敏感菌导致的各种感染，如肺炎、败血症、子宫炎、乳腺炎等。对猪支原体肺炎也有一定疗效。红霉素还用作青霉素过敏者的替代品或其他抗生素无效的微生物感染。 `source_id=SRC-0089; page=36; line=1444`
- `SFDUT1-TX-0268` treatment_or_prevention / p.53 / 林可霉素: （1）作用与用途 主要用于由链球菌属、葡萄球菌属及厌氧菌等敏感菌所致的各种感染，如肺炎、败血症、蜂窝织炎、骨关节炎和乳腺炎、子宫炎等。对猪支原体肺炎（猪气喘病）、猪密螺旋体痢疾（血痢）等也有防治功效。 `source_id=SRC-0089; page=53; line=1628`
- `SFDUT1-TX-0270` treatment_or_prevention / p.66 / 泰妙菌素与沃尼妙林: 猪内服吸收良好，血药浓度达峰时间在 $2\sim 4$ 小时，生物利用度 $85\%$ 以上。吸收后在体内广泛分布，肺中浓度最高。主要用于防治猪支原体肺炎、放线菌性胸膜肺炎和短螺旋体性痢疾、由胞内劳氏菌感染引起的猪增生性肠病（回肠炎）和由结肠菌毛样短螺旋体感染引起的猪结肠螺旋体病（结肠炎）等。低剂量作为猪的饲料药物添加剂可促进增重，提高饲料利用率。 `source_id=SRC-0089; page=66; line=1656`
- `SFDUT1-TX-0273` treatment_or_prevention / p.33 / 泰妙菌素与沃尼妙林: （1）适应证 主要用于防治猪支原体肺炎和放线菌性胸膜肺炎，也可用于短螺旋体性痢疾、猪增生性肠炎。 `source_id=SRC-0089; page=33; line=1671`
- `SFDUT1-TX-0354` treatment_or_prevention / p.83 / 氟喹诺酮类药物: （3）氟喹诺酮类与林可霉素联用，对葡萄球菌、链球菌等革兰阳性菌作用增强；可用于治疗猪支原体肺炎（猪气喘病）或肺炎支 `source_id=SRC-0089; page=83; line=2058`
- `SFDUT1-TX-0360` candidate_fact / p.39 / 氟喹诺酮类药物: （1）适应证 本品主要用于细菌性疾病和支原体感染，如猪支原体肺炎（猪气喘病）、猪嗜血支原体病（猪附红细胞体病）、多杀性巴氏杆菌病（猪肺疫）、大肠杆菌病（仔猪黄白痢、仔猪水肿病）、沙门菌病（仔猪副伤寒）、猪链球菌病、传染性胸膜肺炎、副猪嗜血杆菌病、猪萎缩性鼻炎、乳腺炎、子宫炎、泌乳障碍综合征、尿道炎、膀胱炎等。 `source_id=SRC-0089; page=39; line=2081`
- `SFDUT1-TX-0726` treatment_or_prevention / p.189 / 猪支原体肺炎: （2）传染源 猪肺炎支原体存在于感染猪鼻腔中，患病母猪尤其是初产母猪是最重要的传染源，母猪将病原体传给仔猪，造成猪肺炎支原体在猪群中长期存在。症状消失但未完全康复的猪或用药物治疗但未完全治愈的猪体内仍然带菌，也可造成同圈断奶仔猪之间相互传染。 `source_id=SRC-0089; page=189; line=3766`
- `SFDUT1-TX-0727` treatment_or_prevention / p.189 / 猪支原体肺炎: （4）流行特点 本病一年四季均可发生，以冬春寒冷季节多发。本病的发生与饲养管理、气候与环境的变化有很密切的关系。猪群过分拥挤、饲料营养水平不够、猪舍阴暗潮湿、通风不良、环境卫生条件差的猪场常易发生本病。环境的突然改变，如仔猪断奶、运输等各种应激造成猪过度疲劳，易使本病加重，也为继发或并发感染创造了条件。用一般药物治疗后，症状暂时消退以后又能复发。 `source_id=SRC-0089; page=189; line=3770`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- Byte size moved: 10777
- Fact-like rows moved: 31
- Candidate fact mentions moved: 5
- Dose/route/course fact markers moved: 6
- Source anchors moved: 31

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 增强证据 (SRC-0090, V13.1 batch)

- Batch status: 31 linked disease-control/treatment facts.
- Source pages: 189, 191, 192, 193, 194, 195.
- Matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_200_363_fact_index.csv`.

- `SFDUT2-TX-0001` vaccination_or_immunization / p.189 / 猪支原体肺炎: 猪肺炎支原体可以改变表面抗原而造成免疫逃逸，导致免疫力减弱。还诱导免疫反应和疾病相关炎症反应，其产生的致炎因子加剧了肺脏的炎症反应，更易引起肺组织的损伤和疾病的发展。使肺巨噬细胞的吞噬功能降低，造成严重的免疫抑制作用。在急性期这种感染属于免疫抑制。免疫反应参与病变的发展进程，感染后17周的病肺组织中仍会有大量有活性的支原体，足以使易感猪发生肺炎。 `source_id=SRC-0090; page=189; line=3`
- `SFDUT2-TX-0002` treatment_or_prevention / p.191 / 猪支原体肺炎: 猪肺疫：多表现为急性传染病的特征，急性病例呈败血症和纤维素性胸膜炎症状，全身症状较重，突然发病，体温升高到 $41^{\circ} \mathrm{C}$ 以上，食欲废绝，呼吸困难，哮喘、张口露舌、口鼻流出泡沫或清液，颈部咽喉区高度红肿，病程较短，如不及时治疗很快就死亡。散发型多表现体温升高到 $40 \sim 41^{\circ} \mathrm{C}$ ，呼吸困难，间有咳嗽，后期鼻孔流出黏稠的渗出物，可拖至 $1 \sim 2$ 周才死。如果转为慢性，高度消瘦，病程可达 $3 \sim 5$ 周以上。剖检时见败血症和纤维素性胸膜肺炎变化，出现不同程度的肝变区，可见大小不一的化脓灶或坏死灶，病原是巴氏杆菌。而气喘病的体温和食欲无大变化，肺有肝变区，但无败血症和胸膜炎的变化。 `source_id=SRC-0090; page=191; line=31`
- `SFDUT2-TX-0003` treatment_or_prevention / p.192 / 猪支原体肺炎: 多种喹诺酮类药、抗生素类药如林可霉素、泰妙菌素、泰乐菌素、替米考星、乙酰异戊酰泰乐菌素、四环素、土霉素、强力霉素、金霉素、卡那霉素等对猪支原体肺炎均有较好的治疗作用。 `source_id=SRC-0090; page=192; line=41`
- `SFDUT2-TX-0004` treatment_or_prevention / p.192 / 猪支原体肺炎: （1）个体注射治疗 肌内注射，以体重计一次量。 `source_id=SRC-0090; page=192; line=43`
- `SFDUT2-TX-0005` dose_route_course / p.192 / 猪支原体肺炎: ① 恩诺沙星注射液，5毫克/千克，一天1次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=192; line=45`
- `SFDUT2-TX-0006` dose_route_course / p.192 / 猪支原体肺炎: ② 林可霉素注射液，10毫克/千克，一天1次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=192; line=46`
- `SFDUT2-TX-0007` dose_route_course / p.192 / 猪支原体肺炎: ③ 泰妙菌素注射液，20毫克/千克，一天1次，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=192; line=47`
- `SFDUT2-TX-0008` dose_route_course / p.192 / 猪支原体肺炎: ④ 泰乐菌素注射液，20毫克/千克，一天1次，连用 $3 \sim 5$ 天。 `source_id=SRC-0090; page=192; line=48`
- `SFDUT2-TX-0009` dose_route_course / p.192 / 猪支原体肺炎: ⑤ $20\%$ 长效土霉素注射液（得米仙），1毫克/10千克，三天1次，连用3次。 `source_id=SRC-0090; page=192; line=49`
- `SFDUT2-TX-0010` dose_route_course / p.193 / 猪支原体肺炎: ⑥ 卡那霉素注射液，40毫克/千克，一天1次，连用 $3 \sim 5$ 天。 `source_id=SRC-0090; page=193; line=50`
- `SFDUT2-TX-0011` candidate_fact / p.193 / 猪支原体肺炎: （2）群体混饲给药 可采用如下策略。 `source_id=SRC-0090; page=193; line=52`
- `SFDUT2-TX-0012` treatment_or_prevention / p.193 / 猪支原体肺炎: ③ 脉冲式给药：通过短期的治疗量给药，以尽快杀灭病原体，降低肺病变指数，治疗量添加给药通常为 $3 \sim 5$ 天，停药 $2 \sim 3$ 天后再给药 $3 \sim 5$ 天。 `source_id=SRC-0090; page=193; line=56`
- `SFDUT2-TX-0013` candidate_fact / p.193 / 猪支原体肺炎: ① $80\%$ 泰妙菌素预混剂（枝原净）125克 $+10\%$ 盐酸多西环素预混剂1000克。 `source_id=SRC-0090; page=193; line=60`
- `SFDUT2-TX-0014` candidate_fact / p.193 / 猪支原体肺炎: ② $8.8\%$ 磷酸泰乐菌素预混剂200克 $+15\%$ 金霉素预混剂2000克。 `source_id=SRC-0090; page=193; line=61`
- `SFDUT2-TX-0015` candidate_fact / p.193 / 猪支原体肺炎: ③ 替米考星预混剂（效价） $200 \sim 400$ 克。 `source_id=SRC-0090; page=193; line=62`
- `SFDUT2-TX-0016` candidate_fact / p.194 / 猪支原体肺炎: ④ $20\%$ 乙酰异戊酰泰乐菌素（又名泰万菌素、万乐霉素）预混剂400克。 `source_id=SRC-0090; page=194; line=63`
- `SFDUT2-TX-0017` treatment_or_prevention / p.194 / 猪支原体肺炎: 因猪肺炎支原体没有细胞壁，因此通过干扰细胞壁合成发挥抗菌作用的青霉素、氨苄西林、阿莫西林和头孢菌素对单纯的支原体肺炎治疗无效，其他抗菌药物如甲氧氨苄和磺胺类药物、多黏菌素、链霉素、红霉素对猪支原体肺炎的治疗也不起作用。 `source_id=SRC-0090; page=194; line=65`
- `SFDUT2-TX-0018` vaccination_or_immunization / p.194 / 猪支原体肺炎: 高感染率种猪场仍以药物防治为主，免疫和生物风险管理措施配合，进行综合防控，同时要改善饲养管理和圈舍条件。 `source_id=SRC-0090; page=194; line=69`
- `SFDUT2-TX-0019` vaccination_or_immunization / p.194 / 猪支原体肺炎: （1）弱毒活疫苗 中国兽医药品监察所研制出肺炎支原体兔化 `source_id=SRC-0090; page=194; line=71`
- `SFDUT2-TX-0020` vaccination_or_immunization / p.194 / 猪支原体肺炎: 弱毒活疫苗（培养基疫苗），采用鼻腔深部接种的方法，操作方便，免疫效果确实。可对种公、母猪及断奶前后的仔猪进行免疫，免疫保护率可达 $75\%$ 以上，免疫期可达半年以上。 `source_id=SRC-0090; page=194; line=73`
- `SFDUT2-TX-0021` vaccination_or_immunization / p.194 / 猪支原体肺炎: 南京天邦生产的全球首个猪支原体肺炎克隆弱毒活疫苗（1687猪），采用12号短针头肺内注射方法，剂量：2毫升，一次免疫保护可达 $80\%$ 以上，免疫期6个月以上。免疫程序：在 $6\sim 10$ 周龄一次性免疫（在咳嗽前4周）。 `source_id=SRC-0090; page=194; line=75`
- `SFDUT2-TX-0022` vaccination_or_immunization / p.195 / 猪支原体肺炎: （2）灭活疫苗 美国辉瑞、普泰克、先灵葆雅、梅里亚、海勃莱、荷兰英特威等多家公司通过浓缩猪肺炎支原体培养物先后研制成功猪肺炎支原体灭活苗并已销售。该苗可以用于哺乳仔猪、怀孕母猪和种公猪。肌内接种，免疫接种两次，对猪安全，无副作用。 `source_id=SRC-0090; page=195; line=77`
- `SFDUT2-TX-0023` vaccination_or_immunization / p.195 / 猪支原体肺炎: 疫苗免疫能有效降低临床疾病的发生率，包括肺炎和咳嗽等，但不能阻止病原菌在宿主体内的移行。为此要抓好四项工作：一要净化种猪；二要创造理想的通风、保温、密度等环境条件；三要疫苗免疫；四要药物预防和治疗。 `source_id=SRC-0090; page=195; line=79`
- `SFDUT2-TX-0024` vaccination_or_immunization / p.195 / 猪支原体肺炎: 如果母猪已经怀孕，病猪及早挑出集中隔离饲养，要在接种疫苗的同时，在产仔前2周还要进行药物治疗，减少猪体内的猪肺炎支原体，以防哺乳期间传给仔猪。 `source_id=SRC-0090; page=195; line=84`
- `SFDUT2-TX-0025` vaccination_or_immunization / p.195 / 猪支原体肺炎: （2）新生仔猪 $5\sim 7$ 日龄接种猪气喘病弱毒冻干疫苗，仔猪进行二次免疫可以提高猪群免疫力， $5\sim 7$ 日龄首免， $60\sim 80$ 日龄二免。也可接种进口的猪气喘病灭活苗。 `source_id=SRC-0090; page=195; line=85`
- `SFDUT2-TX-0026` vaccination_or_immunization / p.195 / 猪支原体肺炎: （3）后备母猪连续免疫疫苗2年，可以控制猪气喘病。仔猪从哺乳期到架子猪都未出现气喘症状，通过疫苗接种，仔猪亦未发现气喘病的病变，可以定为健康猪群。 `source_id=SRC-0090; page=195; line=86`
- `SFDUT2-TX-0027` vaccination_or_immunization / p.195 / 猪支原体肺炎: （4）从集市购买的苗猪或架子猪，临诊上如无咳嗽，又无气喘症状，体温正常（ $40^{\circ}\mathrm{C}$ 以下），可以立即接种弱毒疫苗或灭活疫苗。 `source_id=SRC-0090; page=195; line=87`
- `SFDUT2-TX-0028` treatment_or_prevention / p.195 / 猪支原体肺炎: 在暴发此病猪场进行紧急预防，可以降低发病率。 `source_id=SRC-0090; page=195; line=89`
- `SFDUT2-TX-0029` vaccination_or_immunization / p.195 / 猪支原体肺炎: 对国外引进的纯种猪, 严格隔离饲养, 对其仔猪 21 天断奶可有效防止猪气喘病的发生, 但引进猪如与有猪气喘病的其他猪混群, 在混群前则须进行疫苗防疫, 并适当配合用药。引进猪由于生长速度快, 抗应激能力差, 对饲养管理和生物安全标准要求较高。多地生产已得到推广, 其中有两地生产, 即配种、怀孕、分娩和哺乳在一地, 保育、生长和育成在另一地。另一种是三地生产模式, 即配种、怀孕、分娩和哺乳在一地, 然后集中在一起保育, 生长及育肥在另一地。三地生产模式应用较多。 `source_id=SRC-0090; page=195; line=91`
- `SFDUT2-TX-0030` vaccination_or_immunization / p.195 / 猪支原体肺炎: 康复母猪一般带菌不排菌。康复母猪单个隔离饲养、人工授精、疫苗接种和辅以适当治疗，亦可育成后备健康猪群，利用康复母猪建立健康猪群在我国当前情况下是可行的。 `source_id=SRC-0090; page=195; line=93`
- `SFDUT2-TX-0031` treatment_or_prevention / p.195 / 猪支原体肺炎: 总之，控制猪气喘病需要采取综合防制的办法。其中重点是要建立健康的种猪群，母猪临产前7天和分娩后7天，用泰乐菌素、泰妙菌素或土霉素拌料饲喂，防止经母猪把疾病传给仔猪。其次是要抓好仔猪的疾病预防控制。搞好环境卫生消毒和一栏或一舍的全进全出。定期检查、立即隔离发病猪；根据猪群具体情况采取定时用药、预防用药策略。只有从总体采取合理的综合防治措施，才能有效地控制猪气喘病的发生和流行。 `source_id=SRC-0090; page=195; line=95`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_401_600_V14

- Original marker: `RAU_401_600_V14_START` / `RAU_401_600_V14_END`
- Original runtime page: `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- Byte size moved: 589
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 0

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）症候支持边界 / SRC-0093

- 咳嗽/喘息：化痰止咳药只作症候支持，不得替代支原体诊断和治疗边界。
- 证据用途：中药联用、禁忌、用药注意、症候支持和鉴别增强；不是病原确诊、报告处置、抗菌药剂量、休药期、MRL 或食品安全承诺来源。
- 索引：`exports/veterinary_rational_use_401_600_fact_index.csv`；矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`。
<!-- RAU_401_600_V14_END -->
