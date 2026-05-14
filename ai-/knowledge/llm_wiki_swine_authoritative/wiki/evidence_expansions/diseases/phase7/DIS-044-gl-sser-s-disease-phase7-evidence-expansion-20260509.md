---
page_id: DIS-044-gl-sser-s-disease
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase7_disease_page_compaction
moved_from: wiki/diseases/DIS-044-gl-sser-s-disease.md
generated: 2026-05-09T14:35:51+08:00
---

# DIS-044-gl-sser-s-disease Phase 7 Evidence Expansion

This file stores high-density disease evidence moved out of the default runtime disease page during Phase 7.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Diagnosis, regulatory action, treatment, withdrawal-period, MRL, residue, and food-safety conclusions still require rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- Byte size moved: 944
- Fact-like rows moved: 2
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Treatment or prescription markers moved: 1
- Source anchors moved: 2

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 2 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 34.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0036` 处方1：注射用青霉素钠；200万单位；注射用水；5毫升；用法=用法：一次肌内注射，每日2次，连用 $3\sim 5$ 天。；注=。`source_id=SRC-0087; page=34; line=1406-1416`
- `HANDBOOK-RX-0037` 处方2：$①$ 三甲氧苄氨嘧啶 0.5克；$②$ 磺胺嘧啶 5克；用法=用法：按每千克体重10毫克喂服，每日2次，连用 $3\sim 5$ 天。；用法：按每千克体重0.1克（首次0.2克）喂服，每日2次，连用 $3\sim 5$ 天。；注=。`source_id=SRC-0087; page=34; line=1418-1426`
<!-- HANDBOOK_RX_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- Byte size moved: 6053
- Fact-like rows moved: 8
- Candidate fact mentions moved: 2
- Dose/route/course fact markers moved: 0
- Treatment or prescription markers moved: 0
- Source anchors moved: 8

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 8 linked disease-control/treatment facts.
- Source pages: 19, 30, 31, 34, 60, 61, 116, 119.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0057` treatment_or_prevention / p.19 / 治疗猪病要选择最适宜的给药方法: 消化道感染应以口服为主。大多数能在胃肠道吸收的药物也可采用口服给药。口服给药的优点是操作方便、安全，缺点是起效慢，剂量较大。此外，胃肠道不易吸收的磺胺脒、新霉素、庆大霉素、吡哌酸、黏杆菌素等也可口服，利用在肠道形成较高浓度的特点，治疗细菌性肠炎、仔猪黄白痢等。若治疗全身性感染疾病，如副猪嗜血杆菌病等以及危急病例，不宜口服而应注射。 `source_id=SRC-0089; page=19; line=713`
- `SFDUT1-TX-0103` candidate_fact / p.30 / 肆霉素类: （1）作用与用途 用于各种敏感菌引起的全身性感染，如大肠杆菌、沙门菌、巴氏杆菌、嗜血杆菌属、葡萄球菌、链球菌、脑膜炎球菌、化脓性隐秘杆菌等引起的肺部、肠道、尿路感染和败血症、乳腺炎、子宫炎、猪传染性胸膜肺炎、副猪嗜血杆菌病等。 `source_id=SRC-0089; page=30; line=908`
- `SFDUT1-TX-0111` treatment_or_prevention / p.31 / 肆霉素类: （1）作用与用途 主要适用于对青霉素敏感的 $\mathbf{G}^{+}$ 菌和 $\mathbf{G}^{-}$ 敏感菌引起的呼吸道、消化道、泌尿生殖道等感染，如大肠杆菌病、副伤寒、猪肺疫、传染性胸膜肺炎、副猪嗜血杆菌病、萎缩性鼻炎、细菌性肺炎、败血症、链球菌病、葡萄球菌病及多种细菌引起的皮炎和软组织感染均有显著疗效。与地塞米松合用治疗乳房炎、子宫炎、肾盂肾炎及泌乳障碍综合征等疗效极佳。 `source_id=SRC-0089; page=31; line=932`
- `SFDUT1-TX-0119` candidate_fact / p.34 / 头孢菌素类: （1）作用与用途 本品为半合成的第三代动物专用头孢菌素，具有广谱杀菌作用。一些研究者所做的头孢噻呋对兽医临床分离的数千株病原菌的抑菌实验结果表明，本药是抗菌活性最强的药物之一。对 $\mathbf{G}^{+}$ 菌、 $\mathbf{G}^{-}$ 菌（包括产 $\beta$ 内酰胺酶菌）及一些厌氧菌均有效。敏感菌主要有多杀性巴氏杆菌、溶血性巴氏杆菌、胸膜肺炎放线杆菌、副猪嗜血杆菌、大肠杆菌、沙门菌、链球菌、葡萄球菌等，但支气管败血波氏杆菌、某些铜绿假单胞菌、肠球菌、衣原体耐药。本品抗菌活性比氨苄西林强，对链球菌的活性比氟喹诺酮类强。兽医临床主要用于 $\mathbf{G}^{+}$ 和 $\mathbf{G}^{-}$ 菌感染，如猪胸膜肺炎放线杆菌、副猪嗜血杆菌、多杀性巴氏杆菌、大肠杆菌、猪霍乱沙门菌及链球菌等引起的感染及呼吸道病（猪细菌性肺炎）。注射本品后，15分钟内可迅速被吸收，并有消除半衰期长的特点，对传染性胸膜肺炎及副猪嗜血杆菌病的疗效较阿莫西林、林可霉素-大观霉素（利高霉素）显著，建议首选。 `source_id=SRC-0089; page=34; line=974`
- `SFDUT1-TX-0251` treatment_or_prevention / p.60 / 氟苯尼考: （1）主要用于治疗敏感菌所致的各种感染以及多种病因引起的继发感染和并发症，尤其适合于呼吸道疾病。推荐作为巴氏杆菌病（猪肺炎）、猪传染性胸膜肺炎和副猪嗜血杆菌病的首选药物，特别适用于治疗对氟喹诺酮类及其他抗菌药物有耐药性的细菌感染，对中度感染尤其明显。也可用于治疗链球菌（肺炎）、支气管败血波氏杆菌（萎缩性鼻炎）、肺炎支原体（猪气喘病）等引起的呼吸道疾病及嗜血支原体引起的猪附红细胞体病等。病猪表现为体温升高、不食、呼吸急促、咳嗽、气喘；有的张口呼吸，鼻流泡沫状液体，有时混有血液，皮肤有淤血斑块和小出血点；有的表现关节肿胀，耳、鼻发绀（蓝紫色）等。 `source_id=SRC-0089; page=60; line=1537`
- `SFDUT1-TX-0257` treatment_or_prevention / p.61 / 氟苯尼考: （5）传染性胸膜肺炎、副猪嗜血杆菌病、猪肺疫等的治疗：发病初期，患病猪群还有较好的食欲时，混饲给药时可适当提高添加量，每吨饲料可添加氟苯尼考（效价）100克，最好再配合强力霉素（效价）200克，连用7天，有较好效果。对传染性疾病引起的发热、咳嗽、气喘，单独使用抗菌药物即可，无需添加其他解热镇痛、止咳平喘类药物。如果病猪出现高热、不食，则要进行隔离治疗，使用氟苯尼考注射液肌内注射；若体温超过 $41^{\circ}\mathrm{C}$ 时，可配合解热镇痛药及地塞米松使用，效果更佳。 `source_id=SRC-0089; page=61; line=1560`
- `SFDUT1-TX-0512` vaccination_or_immunization / p.116 / 制定和执行科学的免疫程序: （7）其他病毒及细菌性疫病 根据各场的实际情况，酌情选用猪2型圆环病毒灭活疫苗（勃林格、哈兽研维科、普莱柯、成都天邦、海利、福州大北农、南农高科等）、高致病性猪蓝耳病活疫苗或灭活苗、副猪嗜血杆菌病灭活苗（勃林格、海勃莱、科前）等，免疫程序及剂量依厂家说明书。 `source_id=SRC-0089; page=116; line=2660`
- `SFDUT1-TX-0529` vaccination_or_immunization / p.119 / 猪疫苗免疫接种应注意的细节: （4）常用的细菌灭活苗 副猪嗜血杆菌病灭活疫苗、猪链球菌双价灭活疫苗、猪传染性胸膜肺炎三价油乳剂灭活疫苗、猪传染性萎缩性鼻炎二联油乳剂灭活菌苗、猪气喘病灭活疫苗、仔猪大肠杆菌病三价灭活疫苗等。 `source_id=SRC-0089; page=119; line=2693`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-044-gl-sser-s-disease.md`
- Byte size moved: 10941
- Fact-like rows moved: 21
- Candidate fact mentions moved: 5
- Dose/route/course fact markers moved: 5
- Treatment or prescription markers moved: 0
- Source anchors moved: 22

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 增强证据 (SRC-0090, V13.1 batch)

- Batch status: 22 linked disease-control/treatment facts.
- Source pages: 196, 197, 199, 200, 201, 202.
- Matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_200_363_fact_index.csv`.

- `SFDUT2-TX-0032` vaccination_or_immunization / p.196 / 副猪嗜血杆菌病: 吸道病综合征等因素的存在，使得本病危害日渐严重，在世界各地广为流传，成为断奶前后和保育猪头号杀手。特别在有繁殖与呼吸障碍综合征（俗称蓝耳病，PRRS）和2型圆环病毒（PCV-2）感染这两种免疫抑制性疾病存在的猪场，本病更容易趁机暴发，且发病很快，确诊和治疗都有困难，死淘率大幅度上升，损失惨重。如果再与肺炎支原体（MHP）、胸膜肺炎放线杆菌（APP）、多杀性巴氏杆菌（PM）、猪链球菌（SS）等混合感染，便会发生所谓的呼吸道病综合征（PRDC）。本病是日益严重PRDC的首要细菌病，目前不少人缺乏对它应有的认识，而更多的人则经常将其与胸膜肺炎、链球菌病及猪附红细胞体病混淆而忽视其存在，造成不必要的灾难性的损失，应引起高度重视，严加防范。 `source_id=SRC-0090; page=196; line=103`
- `SFDUT2-TX-0033` treatment_or_prevention / p.197 / 副猪嗜血杆菌病: 目前，我国已确认的副猪嗜血杆菌的血清型有15种，还有 $12.1\%$ 的分离株不能分型，不同血清型的发病特点、交叉保护，甚至治疗用药都可能不同。其中以4型和5型最为流行，其次为13、14和12型。不同的血清型致病力差异很大，1、5、10、12、13和14型毒力最强，患猪归于死亡或处于濒死状态；2、4、8和15型为中等毒力，患病猪死亡率相对较低，但可能出现败血症状，生长迟缓；其他型毒力较低，没有明显临床症状。同一猪场可能同时存在不同菌株。一些最新研究报道指出，HPS也可以从患有严重胸膜肺炎的肺脏中分离出，这也可能是导致此类肺部损伤的原发病原。 `source_id=SRC-0090; page=197; line=109`
- `SFDUT2-TX-0035` candidate_fact / p.199 / 副猪嗜血杆菌病: 喘；疼痛（可由尖叫推断）；跗、腕关节肿胀，严重的会瘸腿；有的出现颤抖，共济失调，耳尖发紫，眼睑发乌肿胀以及中枢神经系统症状等。病情严重者随之可能死亡。临死前侧卧或四肢呈划水样。通常发病后 $2\sim 5$ 天死亡（通常由败血性休克或内毒素休克所致，在不出现典型的多发性浆膜炎时就出现发绀、皮下水肿及肺水肿，乃至死亡）。最急性的个别猪可能不表现任何症状而突然猝死。耐过急性发病的猪可转为亚急性型或慢急性型。 `source_id=SRC-0090; page=199; line=135`
- `SFDUT2-TX-0036` candidate_fact / p.199 / 副猪嗜血杆菌病: （2）亚急性型或慢急性型 常由急性型转化而来或由中等毒力毒株引起，主要表现为多发性浆膜炎、关节炎、脑膜炎等。病猪食欲下降、精神沉郁、发抖、扎堆、咳嗽、呼吸困难、被毛粗乱、渐进性消瘦、体表皮肤苍白；行动迟缓僵硬，后肢不协调；四肢无力，不愿站立；关节肿大或跛行。副猪嗜血杆菌性脑膜炎的症状，除共济失调、步伐蹒跚、头向后仰、四肢呈游泳状以外，笔者还观察到一种特殊表现：喜欢向同一侧躺卧，将猪翻过来它又很快便自动翻回去，可反复数次（可用复方磺胺间甲氧嘧啶配合阿莫西林或氨苄西林分别肌注，效果较好）。慢急性型有的可拖10多天后终因衰竭而死。侥幸不死的极度消瘦或生长缓慢。 `source_id=SRC-0090; page=199; line=137`
- `SFDUT2-TX-0037` treatment_or_prevention / p.200 / 副猪嗜血杆菌病: 笔者总结了治疗 HPS 的几条原则和体会，如下。 `source_id=SRC-0090; page=200; line=159`
- `SFDUT2-TX-0038` treatment_or_prevention / p.200 / 副猪嗜血杆菌病: （1）治疗应在暴发早期，必须早发现、早确诊、早治疗、越快越好。 `source_id=SRC-0090; page=200; line=161`
- `SFDUT2-TX-0039` treatment_or_prevention / p.201 / 副猪嗜血杆菌病: 要在整个猪群大量发病之前 $1 \sim 2$ 天就能发现病猪。此病传染性很强，一定要对病猪进行隔离治疗，同时要对整个猪群采取严格的控制措施。 `source_id=SRC-0090; page=201; line=163`
- `SFDUT2-TX-0040` treatment_or_prevention / p.201 / 副猪嗜血杆菌病: （2）一旦临床症状已经出现，一是应立即采用肌注或静注用药的方式，不能采用口服用药。二是必须应用大剂量的敏感抗菌药物对同栏的所有猪（感染猪或非感染猪）进行治疗，才可能有部分效果，而不仅仅只是对那些表现出症状的猪用药。此条被临床实践证 `source_id=SRC-0090; page=201; line=165`
- PHASE2_ENCODING_QUARANTINED: one damaged extracted fact line was removed from runtime text because it contained UTF-8 replacement characters. See `issues/phase2_encoding_quarantine_2026-05-09.md`. Original anchor: fact_id=SFDUT2-TX-0041; source_id=SRC-0090; page=201; line=167.
- `SFDUT2-TX-0042` candidate_fact / p.201 / 副猪嗜血杆菌病: （3）很多慢性病例都是由于长期不吃食，饥饿衰竭而死。为此，要“3分治7分养”，加强护理。可在饮水中加电解多维、口服葡萄糖、黄芪多糖等，增加营养，提高自身恢复能力。 `source_id=SRC-0090; page=201; line=168`
- `SFDUT2-TX-0043` vaccination_or_immunization / p.201 / 副猪嗜血杆菌病: （4）本病临床治疗非常困难。在发病初期采用下列抗菌药物进行早期治疗，同时要“标本兼治”，病因疗法与对症疗法相结合，酌情配合解热镇痛药、地塞米松、维生素C、排疫苗、猪转移因子、干扰素以及黄芪多糖、复方柴胡、穿心莲、板蓝根、双黄连、鱼腥草等抗病毒及增强机体免疫力的注射剂等，有一定疗效，治愈率 $60\%$ 左右。如果治疗不及时，则疗效欠佳。 `source_id=SRC-0090; page=201; line=169`
- `SFDUT2-TX-0044` dose_route_course / p.201 / 副猪嗜血杆菌病: ① 头孢噻呋钠，5毫克/千克体重，1次/天，连用 $4 \sim 5$ 天。或头孢拉定，30毫克/千克体重，每 $6 \sim 8$ 小时1次。 `source_id=SRC-0090; page=201; line=170`
- `SFDUT2-TX-0045` dose_route_course / p.201 / 副猪嗜血杆菌病: ② 庆大霉素注射液，4毫克/千克体重，2次/天；同时配合左氧氟沙星5毫克/千克体重，2次/天（或甲磺酸达氟沙星2.5毫克/千克体重，1次/天），连用 $4\sim 5$ 天。 `source_id=SRC-0090; page=201; line=171`
- `SFDUT2-TX-0046` dose_route_course / p.201 / 副猪嗜血杆菌病: ③ 阿莫西林，15毫克/千克体重，2次/天，连用 $4 \sim 5$ 天（也可选用：氨苄西林/舒巴坦，20毫克/千克体重，2次/天，连用 $4 \sim 5$ 天；或青霉素G，5万单位/千克体重， $2 \sim 3$ 次/天，连用 $4 \sim 5$ 天）。或氨苄西林 $10 \sim 20$ 毫克/千克体重， $2 \sim 3$ 次/天，连用 $2 \sim 3$ 天。 `source_id=SRC-0090; page=201; line=172`
- `SFDUT2-TX-0047` dose_route_course / p.201 / 副猪嗜血杆菌病: ④ 纽弗罗注射液，20毫克/千克体重，1次/天，连用 $3\sim$ 5天。 `source_id=SRC-0090; page=201; line=173`
- `SFDUT2-TX-0048` dose_route_course / p.201 / 副猪嗜血杆菌病: ⑤ 氟苯尼考注射液，30毫克/千克体重，2次/天，连用 $3\sim 5$ 天（如果按国内厂家使用说明书用量20毫克/千克体重，48小时一次，连用2次，效果不好）。 `source_id=SRC-0090; page=201; line=175`
- `SFDUT2-TX-0049` candidate_fact / p.201 / 副猪嗜血杆菌病: ⑥ 复方磺胺间甲氧嘧啶，首次量0.1克/千克体重，维持量0.05克/千克体重，2次/天，连用 $4\sim 5$ 天。 `source_id=SRC-0090; page=201; line=176`
- `SFDUT2-TX-0050` treatment_or_prevention / p.202 / 副猪嗜血杆菌病: 副猪嗜血杆菌病作为一种新的传染病，其流行与严重程度日益增加，尤其是大型养猪场，应加深对其潜在危害性的认识。由于本病治疗效果不好，要遵循“养重于防，防重于治”的原则，以预防为主，采取综合防控措施。 `source_id=SRC-0090; page=202; line=181`
- `SFDUT2-TX-0052` vaccination_or_immunization / p.202 / 副猪嗜血杆菌病: （5）疫苗免疫预防 有条件的猪场，最好的办法是从脑分离菌株制作自家灭活疫苗。所谓的自家苗是指从本场发病猪分离致病毒力菌株，经实验室分离培养鉴定，大规模制备、灭活，添加免疫佐剂，并经初步试验后供本场使用的疫苗。因为血清型符合本场的实际，使用效果较好。无条件的可选用进口灭活疫苗（西班牙海博莱或勃林格）免疫母猪，初产母猪产前40天首免，产前20天二免；经产母猪产前30天免疫一次即可，一般情况下 $2\sim 3$ 周后产生保护 `source_id=SRC-0090; page=202; line=187`
- `SFDUT2-TX-0053` vaccination_or_immunization / p.202 / 副猪嗜血杆菌病: 力，母猪抗体可保护 $6 \sim 7$ 周龄的仔猪；如果仔猪在8周龄以后发病，则需要在仔猪 $2 \sim 3$ 周龄首免， $2 \sim 3$ 周后二免，使其产生主动免疫力。也可选用国产疫苗（武汉科前），母猪接种后可对4周龄仔猪提供保护。再用含有相同血清型的灭活苗接种小猪，对断奶仔猪产生主动保护性免疫力。由于HPS具有明显的地方性特征，血清型多，不同血清型之间无交叉保护力，目前还没有一种灭活苗同时对猪所有的致病株产生交叉保护力，商品疫苗效果有时不确定。也可试用常规的本场的病变组织匀浆制成的自家组织灭活苗。 `source_id=SRC-0090; page=202; line=189`
- `SFDUT2-TX-0054` treatment_or_prevention / p.202 / 副猪嗜血杆菌病: （6）在日粮或饮水中添加药物进行预防，并要科学用药 本病在严重暴发时，使用药物预防可能无效。为此，应摸清本病在本场的发病规律，应在发病前3周提前对整个猪群进行药物预防。有条件的最好能做药敏测验，采用敏感药物，但用药量不可过少，防止产生耐药性，或在全群的饮水中添加阿莫西林或强力霉素。 `source_id=SRC-0090; page=202; line=191`
- `SFDUT2-TX-0055` candidate_fact / p.202 / 副猪嗜血杆菌病: ④ 每吨饲料添加英国伊科“爱乐新”预混料1000克或伊科力康（ $10\%$ 氟苯尼考）1500克，或“氟奇霉素”800克，或“加康”500克，或替米考星200克（效价），连用2周。 `source_id=SRC-0090; page=202; line=196`
<!-- SFDUT_200_363_V13_1_END -->
