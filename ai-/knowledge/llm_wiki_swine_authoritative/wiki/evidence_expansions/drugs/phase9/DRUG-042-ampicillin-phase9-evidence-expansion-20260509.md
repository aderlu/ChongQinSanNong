---
page_id: DRUG-042-ampicillin
entity_type: drug_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/drugs/DRUG-042-ampicillin.md
generated: 2026-05-09T14:56:01+08:00
---

# DRUG-042-ampicillin Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-042-ampicillin.md`
- Byte size moved: 8442
- Fact-like rows moved: 12
- Candidate fact mentions moved: 4
- Dose/route/course fact markers moved: 1
- Source anchors moved: 12

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 用药证据 (SRC-0089, V13.1 batch)

- Batch status: 12 linked drug-use facts.
- Source pages: 11, 22, 28, 31, 34, 36, 41, 63, 152, 188.
- Drug mention index: `exports/swine_farm_drug_use_1_200_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`.

- `SFDUT1-TX-0023` dose_route_course / p.11 / 兽药使用必须遵循的基本原则: 不同的疾病使用不同的药物，同一种疾病也不能长期使用某一种药物治疗。当发生某种疾病时，要根据流行病学、临床症状、解剖变化、实验室检验结果等综合分析，做出准确的诊断，然后有针对性地选择药物，所选药物要安全、可靠、方便、价廉，达到“药半功倍”的效果，彻底杜绝不明病情而滥用药物，特别是抗菌药物。例如对发生传染性胸膜肺炎的猪，选用氟苯尼考、青霉素、氨苄西林、四环素等治疗有良好效果。对于诸如亚硝酸盐中毒可用特效解毒药小剂量美蓝（亚甲蓝）进行解毒，注射 $1\%$ 美蓝溶液，猪 $1\sim 2$ 毫克/千克体重。有机磷中毒可使用阿托品结合解磷定进行解毒。 `source_id=SRC-0089; page=11; line=566`
- `SFDUT1-TX-0073` treatment_or_prevention / p.22 / 要提前预见药物的疗效和不良反应: 药物的作用或效应取决于作用部位的浓度，无论以何种途径给药，药物在动物体内均要发生吸收、分布、生物转化和排泄的动力学过程。每种药物有其特定的药动学特征，如半衰期、生物利用率、表观分布容积等都有所差异。其动力学特征还受疾病类型及过程影响。只有熟悉药物的动力学特征及其影响因素，才能做到正确选药并制定科学、合理的给药方案，达到预期的治疗效果。例如，阿莫西林与氨苄西林的体外抗菌活性很相似，但前者的生物利用率比后者高1倍，血清浓度高 $1.5 \sim 3$ 倍，在治疗全身性感染时，选用阿莫西林的疗效比氨苄西林好；但在胃肠道感染时，因氨苄西林不易吸收，在胃肠道能保持较高的药物浓度，治疗效果较好。 `source_id=SRC-0089; page=22; line=772`
- `SFDUT1-TX-0106` candidate_fact / p.31 / 肆霉素类: （1）作用与用途 同注射用氨苄西林钠，主要用于敏感菌引起的肺部、肠道、尿路感染和败血症。 `source_id=SRC-0089; page=31; line=921`
- `SFDUT1-TX-0108` candidate_fact / p.31 / 肆霉素类: （3）注意事项 同注射用氨苄西林钠。 `source_id=SRC-0089; page=31; line=923`
- `SFDUT1-TX-0114` drug_interaction / p.31 / 肆霉素类: （3）注意事项 阿莫西林与喹诺酮类、氨基糖苷类抗菌药物联合应用，有协同或相加作用。但与四环素类、氟苯尼考、大环内酯类及林可霉素联用，可能发生拮抗作用。其他参见注射用氨苄西林钠。 `source_id=SRC-0089; page=31; line=938`
- `SFDUT1-TX-0116` treatment_or_prevention / p.28 / 头孢菌素类: 第一代头孢菌素的抗菌谱与广谱青霉素（氨苄西林、阿莫西林）相似。虽对青霉素酶稳定，但仍可被多数 $\mathbf{G}^{-}$ 菌产生的 $\beta$ 内酰胺酶所分解。因此，主要用于革兰阳性（ $\mathbf{G}^{+}$ ）菌（链球菌、产酶葡萄球菌等）和少数 $\mathbf{G}^{-}$ 菌（大肠杆菌、嗜血杆菌、沙门菌等）的感染治疗。常用的有注射用头孢噻吩（先锋霉素I）、头孢唑啉（头孢霉素V）以及内服用的头孢氨苄（先锋霉素IV）、头孢拉定（VI）、头孢羟氨苄等，需要注意的是，该类产品对肾脏毒性较大。 `source_id=SRC-0089; page=28; line=948`
- `SFDUT1-TX-0119` candidate_fact / p.34 / 头孢菌素类: （1）作用与用途 本品为半合成的第三代动物专用头孢菌素，具有广谱杀菌作用。一些研究者所做的头孢噻呋对兽医临床分离的数千株病原菌的抑菌实验结果表明，本药是抗菌活性最强的药物之一。对 $\mathbf{G}^{+}$ 菌、 $\mathbf{G}^{-}$ 菌（包括产 $\beta$ 内酰胺酶菌）及一些厌氧菌均有效。敏感菌主要有多杀性巴氏杆菌、溶血性巴氏杆菌、胸膜肺炎放线杆菌、副猪嗜血杆菌、大肠杆菌、沙门菌、链球菌、葡萄球菌等，但支气管败血波氏杆菌、某些铜绿假单胞菌、肠球菌、衣原体耐药。本品抗菌活性比氨苄西林强，对链球菌的活性比氟喹诺酮类强。兽医临床主要用于 $\mathbf{G}^{+}$ 和 $\mathbf{G}^{-}$ 菌感染，如猪胸膜肺炎放线杆菌、副猪嗜血杆菌、多杀性巴氏杆菌、大肠杆菌、猪霍乱沙门菌及链球菌等引起的感染及呼吸道病（猪细菌性肺炎）。注射本品后，15分钟内可迅速被吸收，并有消除半衰期长的特点，对传染性胸膜肺炎及副猪嗜血杆菌病的疗效较阿莫西林、林可霉素-大观霉素（利高霉素）显著，建议首选。 `source_id=SRC-0089; page=34; line=974`
- `SFDUT1-TX-0135` candidate_fact / p.36 / 头孢菌素类: (3) 注意事项 本品不宜与氨基糖苷类、甲硝唑、氨苄西林、氨茶碱置于同一针管混合注射, 因可能发生理化性质相互作用而减效。其他同注射用头孢噻呋钠。 `source_id=SRC-0089; page=36; line=1046`
- `SFDUT1-TX-0147` vaccination_or_immunization / p.41 / 氨基糖苷类: 作为“繁殖期杀菌剂”的青霉素类、头孢菌素类，能破坏细菌细胞壁，有利于“静止期杀菌剂”的氨基糖苷类抗生素进入细胞体内而发挥杀菌作用，是处理混合感染、危重感染、免疫抑制感染以及致病菌不明感染联合用药的常用品种。常用的有：庆大霉素、卡那霉素、链霉素等与青霉素、氨苄西林钠、阿莫西林、头孢噻呋、头孢喹肟等联用，相互协同，增强疗效。如青霉素+庆大霉素+地塞米松治疗猪链球菌病、猪急性乳腺炎以及敏感细菌混合感染的疗效较高；氨基糖苷类与青霉素或氨苄西林联用治疗猪李氏杆菌病，与头孢菌素类联用治疗肺炎杆菌；庆大霉素与阿莫西林联用治疗铜绿假单胞菌等。但用药剂量应基本平衡，过大剂量的青霉素或其他半合成青霉素均可使氨基糖苷类活性降低。另外，本类药物体外与 `source_id=SRC-0089; page=41; line=1144`
- `SFDUT1-TX-0261` drug_interaction / p.63 / 林可霉素: （8）本品不能与卡那霉素、新生霉素混合静注，也不能与氨苄西林、氨茶碱、葡萄糖酸钙合用，否则将发生配伍禁忌。 `source_id=SRC-0089; page=63; line=1606`
- `SFDUT1-TX-0640` vaccination_or_immunization / p.152 / 猪圆环病毒病: 采取病因治疗与对症治疗相结合的“标本兼治”的办法治疗。抗菌药物可选用枝原净、氟苯尼考、氟喹诺酮类、丁胺卡那霉素、庆大霉素、阿莫西林、氨苄西林、头孢类、磺胺类等肌注，并配合使用黄芪多糖、鱼腥草、双黄连等免疫增强剂、抗病毒药物及维生素 $\mathbf{B}_{1}$ 和维生素C等。高热者可配合使用安乃近、复方氨基比林等解热镇痛药。因为PCV-2病毒主要侵害猪的免疫系统，临床上尽可能不使用甲矾霉素、卡那霉素等免疫抑制作用的药物，除发生皮炎及肾病综合征外，也不宜使用地塞米松、氢化可的松等皮质激素类药物。也可采用血清疗法：采本场淘汰母猪血，分离血清， $3\sim 5$ 周龄，腹股沟皮下或腹腔注射5毫升，或 $2\sim 3$ 周龄、5周龄仔猪腹股沟注射 $5\sim 10$ 毫升。也可对发病猪进行治疗，每头病猪注射血清 $10\sim 20$ 毫升，隔日注射一次。 `source_id=SRC-0089; page=152; line=3171`
- `SFDUT1-TX-0722` treatment_or_prevention / p.188 / 猪巴氏杆菌病: 个体治疗可选用第3代头孢菌素类和氟喹诺酮类，这是目前治疗本病最有效的药物。也可酌情选用氨基糖苷类、氨苄西林、阿莫西林、氟苯尼考、长效土霉素、强力霉素、磺胺类药物。预防用药可在饲料中添加选用氟苯尼考、泰乐菌素与磺胺二甲嘧啶联用等都有较好疗效。治疗时一般采用交叉用药，用药前尽可能先做药敏试验而后选用最敏感的药物。 `source_id=SRC-0089; page=188; line=3740`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/drugs/DRUG-042-ampicillin.md`
- Byte size moved: 6826
- Fact-like rows moved: 9
- Candidate fact mentions moved: 1
- Dose/route/course fact markers moved: 6
- Source anchors moved: 9

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 用药证据 (SRC-0090, V13.1 batch)

- Batch status: 9 linked drug-use facts.
- Source pages: 194, 199, 201, 210, 217, 222, 251, 294, 306.
- Drug mention index: `exports/swine_farm_drug_use_200_363_drug_mention_index.csv`; matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`.

- `SFDUT2-TX-0017` treatment_or_prevention / p.194 / 猪支原体肺炎: 因猪肺炎支原体没有细胞壁，因此通过干扰细胞壁合成发挥抗菌作用的青霉素、氨苄西林、阿莫西林和头孢菌素对单纯的支原体肺炎治疗无效，其他抗菌药物如甲氧氨苄和磺胺类药物、多黏菌素、链霉素、红霉素对猪支原体肺炎的治疗也不起作用。 `source_id=SRC-0090; page=194; line=65`
- `SFDUT2-TX-0036` candidate_fact / p.199 / 副猪嗜血杆菌病: （2）亚急性型或慢急性型 常由急性型转化而来或由中等毒力毒株引起，主要表现为多发性浆膜炎、关节炎、脑膜炎等。病猪食欲下降、精神沉郁、发抖、扎堆、咳嗽、呼吸困难、被毛粗乱、渐进性消瘦、体表皮肤苍白；行动迟缓僵硬，后肢不协调；四肢无力，不愿站立；关节肿大或跛行。副猪嗜血杆菌性脑膜炎的症状，除共济失调、步伐蹒跚、头向后仰、四肢呈游泳状以外，笔者还观察到一种特殊表现：喜欢向同一侧躺卧，将猪翻过来它又很快便自动翻回去，可反复数次（可用复方磺胺间甲氧嘧啶配合阿莫西林或氨苄西林分别肌注，效果较好）。慢急性型有的可拖10多天后终因衰竭而死。侥幸不死的极度消瘦或生长缓慢。 `source_id=SRC-0090; page=199; line=137`
- `SFDUT2-TX-0046` dose_route_course / p.201 / 副猪嗜血杆菌病: ③ 阿莫西林，15毫克/千克体重，2次/天，连用 $4 \sim 5$ 天（也可选用：氨苄西林/舒巴坦，20毫克/千克体重，2次/天，连用 $4 \sim 5$ 天；或青霉素G，5万单位/千克体重， $2 \sim 3$ 次/天，连用 $4 \sim 5$ 天）。或氨苄西林 $10 \sim 20$ 毫克/千克体重， $2 \sim 3$ 次/天，连用 $2 \sim 3$ 天。 `source_id=SRC-0090; page=201; line=172`
- `SFDUT2-TX-0070` dose_route_course / p.210 / 猪链球菌病: a. 早期可用大剂量青霉素类抗生素类，因大多数分离菌株对青霉素敏感。如青霉素5万～8万单位/千克体重，每天2～3次，连用3～5天；或氨苄西林10～15毫克/千克体重，2次/天，连用3～5天；或阿莫西林15～20毫克/千克体重，每天2次，连用3～5天。如果再联合应用庆大霉素4～5毫克/千克体重，2次/天，或丁胺卡那霉素（阿米卡星）10毫克/千克体重，2次/天，效果更佳。注意，不能用庆大霉素等稀释青霉素类，要分别肌注。 `source_id=SRC-0090; page=210; line=298`
- `SFDUT2-TX-0091` dose_route_course / p.217 / 猪传染性胸膜肺炎: （2）注意事项 据报道，本病对氨苄西林、链霉素、四环素已产生较强耐药性。在选用上述抗菌药物“治本”的同时，可配合使用地塞米松。地塞米松是控制严重肺炎的有效药物，按0.1毫克/千克体重，急重病例可适当加量，最大量0.2毫克/千克体重，2次/天。以每支1毫升（含5毫克）的地塞米松为例，50千克的猪可用2支，30千克的猪每次可用1支，其他依体重大小酌情增减。注意不可突然停药，用 $2\sim 4$ 天后逐渐减量，第 $5\sim 7$ 天停药。在使用地塞米松时，必须同时配合抗菌药物。如果体温达到 $40.5^{\circ}C$ 以上时，可酌情选用解热药“治标”。 $30\%$ 安乃近可按0.2毫克/千克体重； $10\%$ 复方氨基比林或安痛定，10千克体重可注2毫升；或复方柴胡注射液。为提高机体免疫力和抗病毒能力，可肌注复方黄芪多糖注射液，每10千克体重 $2\sim 3$ 毫升，1次/天，连用 $3\sim 5$ 天；或鱼腥草注射液。选用止咳药，如金蛤蟆咳喘针，0.2毫克/千克体重，1次/天，连用 $2\sim 3$ 天；或冰蟾熊胆注射液、咳嗽1号、强力喘康。平喘药如氨茶碱、麻黄素，或酌情选用板蓝根、双黄连等中药制剂。强心可用 `source_id=SRC-0090; page=217; line=390`
- `SFDUT2-TX-0110` dose_route_course / p.222 / 猪传染性萎缩性鼻炎: ③ 个体治疗 肌注，一次量：a. 磺胺类药物配合磺胺增效剂的复方制剂，如复方增效磺胺或复方磺胺嘧啶钠注射液，12.5毫克/千克体重；b. 长效土霉素注射液，20毫克/千克体重；c. 青霉素（4万单位/千克体重）配合卡那霉素（ $20\sim 30$ 毫克/千克体重）或氨苄西林（ $10\sim 20$ 毫克/千克体重）或阿莫西林（ $10\sim 20$ 毫克/千克体重）；d. 氟喹诺酮类注射液， $2.5\sim 5$ 毫克/千克体重；e. 头孢噻呋钠， $5\sim 10$ 毫克/千克体重；f. 仔猪打喷嚏时也可用卡那霉素注射液滴鼻，每天1次，每个鼻孔滴0.5毫升，连用 $2\sim 3$ 天。 `source_id=SRC-0090; page=222; line=470`
- `SFDUT2-TX-0193` dose_route_course / p.251 / 仔猪渗出性皮炎: ① 肌注大剂量的青霉素类或头孢类药物，如注射用青霉素钠，5万单位/千克体重，2~3次/天；注射用氨苄西林钠，20毫克/千克体重，2~3次/天；注射用舒巴坦钠·氨苄西林钠，10毫克/千克体重，2次/天；阿莫西林·克拉维酸钾注射液，1毫升/10千克体重，1次/天；头孢噻呋钠，10毫克/千克体重，1次/天。如再配合地塞米松磷酸钠注射液，0.2毫克/千克体重，1次/天，效果更好。 `source_id=SRC-0090; page=251; line=944`
- `SFDUT2-TX-0286` dose_route_course / p.294 / 母猪产后泌尿生殖系统疾病: 200万单位十地塞米松10毫克十催产素20单位，2次/天，连用 $3\sim$ 5天；b.环丙沙星10毫克/千克，1次/天，连用 $3\sim 5$ 天；c.氨苄西林20毫克/千克，2次/天，连用 $3\sim 5$ 天；d.注射用阿莫西林·克拉维酸钾7毫克/千克（以阿莫西林计），2次/天，连用 $3\sim 5$ 天。 `source_id=SRC-0090; page=294; line=1596`
- `SFDUT2-TX-0326` treatment_or_prevention / p.306 / 猪呼吸道病综合征: （3）采取病因疗法与对症疗法相结合的治疗原则。通过药敏试验，有针对性选择广谱抗菌药物，通过注射途径给予治疗。比较有效和常用的抗菌消炎药物有：头孢噻呋、氟苯尼考、阿莫西林、氨苄西林、青霉素G钠、氟喹诺酮类、林可霉素、长效土霉素、强力霉素、泰妙菌素、泰乐菌素、丁胺卡那霉素、庆大霉素、复方磺胺嘧啶钠、复方磺胺间甲氧嘧啶等。 `source_id=SRC-0090; page=306; line=1772`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/drugs/DRUG-042-ampicillin.md`
- Byte size moved: 755
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用手册（1-200页）增强 / SRC-0091

- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。
- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。
- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。

- `RAU1-DRUG-040-DRUG-042-ampicillin-md-8898` 氨苄西林 / β-内酰胺/青霉素类 / p.40：目录定位显示 `氨苄西林` 属于 `β-内酰胺/青霉素类`，可作为药物召回、类别边界和联用禁忌复核入口。 `source_id=SRC-0091; page=40`
<!-- RAU_1_200_V14_END -->
