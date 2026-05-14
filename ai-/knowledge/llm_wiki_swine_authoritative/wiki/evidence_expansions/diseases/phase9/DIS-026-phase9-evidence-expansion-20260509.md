---
page_id: DIS-026
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-026 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- Byte size moved: 1428
- Fact-like rows moved: 3
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 3

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 3 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 11.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0004` 处方1：$①$ 抗口蹄疫血清 25毫升；$②$ $0.1\%$ 高锰酸钾溶液 适量；碘酊甘油（碘7克、碘化钾5克、酒精100毫升，溶解后加入甘油10毫升） 适量；碘甘油或 $1\% \sim 2\%$ 龙胆紫液 适量；用法=用法：一次肌内或静脉注射，按每千克体重0.5毫升用药。；用法：先以 $0.1\%$ 高锰酸钾溶液冲洗患部，再涂以碘酊甘油或龙胆紫溶液。；注=。`source_id=SRC-0087; page=11; line=618-630`
- `HANDBOOK-RX-0005` 处方2 冰硼散加减：冰片15克 硼砂150克 芒硝18克；用法=用法：患部以消毒水洗净后，研末撒布。；注=。`source_id=SRC-0087; page=11; line=632-636`
- `HANDBOOK-RX-0006` 处方3 贯众散：贯众15克 桔梗12克 山豆根15克 连翘12克；大黄12克 赤芍9克 生地9克 花粉9克；荆芥9克 木通9克 甘草9克 绿豆粉30克；用法=用法：共研末加蜂蜜100克为引，开水冲服，每日1剂，连用 $2\sim 3$ 剂。；注=。`source_id=SRC-0087; page=11; line=638-646`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- Byte size moved: 1082
- Fact-like rows moved: 2
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 2

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Treatment Evidence (SRC-0088, V13.1 batch)

- Batch status: 2 treatment facts linked to this disease page.
- Source pages: 49.
- Full matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`; fact index: `exports/veterinary_treatment_of_pigs_fact_index.csv`.

- `VTOP-TX-0047` vaccination / p.49 / Foot and mouth disease: There are inactivated vaccines available for pigs but they are not licensed in the UK. `source_id=SRC-0088; page=49; line=1471`
- `VTOP-TX-0253` licensing_or_cascade / p.49 / Foot and Mouth Disease: Clinical signs are seen in all ages of pig. They are very marked and unlikely to be missed by observant practitioners. There will be a sudden onset of severe lameness in the whole herd. Piglets and growing pigs will actually squeal if made to move. All ages will have hunched backs and be reluctant to move. They should have their feet washed with water, ideally from a hose, to clean off any debris and then the small r `source_id=SRC-0088; page=49; line=3258`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- Byte size moved: 16816
- Fact-like rows moved: 32
- Candidate fact mentions moved: 2
- Dose/route/course fact markers moved: 0
- Source anchors moved: 33

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 33 linked disease-control/treatment facts.
- Source pages: 6, 20, 113, 114, 119, 120, 133, 134, 135, 136, 137, 138, 147.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0008` vaccination_or_immunization / p.6 / 兽药分类: 疫O型合成肽疫苗、猪口蹄疫O型灭活疫苗、猪高致病性蓝耳病活疫苗、猪高致病性蓝耳病灭活苗、猪圆环病毒2型灭活疫苗、猪伪狂犬病基因缺失弱毒苗、猪伪狂犬病灭活疫苗、猪传染性胃肠炎、流行性腹泻二联灭活苗、猪乙型脑炎活疫苗、猪细小病毒病灭活疫苗、猪衣原体流产油佐剂灭活苗、猪传染性胃肠炎-流行性腹泻-轮状病毒三联弱毒活疫苗。 `source_id=SRC-0089; page=6; line=446`
- `SFDUT1-TX-0061` vaccination_or_immunization / p.20 / 治疗猪病要选择最适宜的给药方法: （5）后海穴注射 后海穴，又称交巢穴，位于尾根与肛门之间凹陷处。后海穴注射药物治疗腹泻，效果比肌注好，因同时有穴位针灸作用。母猪后海穴注射口蹄疫疫苗比肌注产生的抗体多。而有的疫苗，如传染性胃肠炎与流行性腹泻二联苗必须后海穴注射，肌注无效。 `source_id=SRC-0089; page=20; line=723`
- `SFDUT1-TX-0486` vaccination_or_immunization / p.113 / 制定和执行科学的免疫程序: （2）口蹄疫 选用进口206佐剂猪口蹄疫O型灭活疫苗（缅甸98谱系2010毒株即O/MyA98/BY、OZK/93株 $+\mathrm{OS} / 99$ 株或OZK/93株等)，后海穴注射效果更佳。生产厂家：中农威特、中 `source_id=SRC-0089; page=113; line=2612`
- `SFDUT1-TX-0492` vaccination_or_immunization / p.114 / 制定和执行科学的免疫程序: 提示：也可选用猪口蹄疫O型合成肽疫苗（双抗原），剂量 $1\sim 2$ 头份。种公猪每年接种3次；后备种公、母猪：配种前4周接种一次；怀孕母猪：产前 $30\sim 45$ 天接种一次；免疫母猪所产仔猪： $45\sim 50$ 日龄首免，80日龄加强免疫一次；非免疫母猪所产仔猪：仔猪断奶时首免， $20\sim 30$ 天后加强免疫一次，100日龄3免。 `source_id=SRC-0089; page=114; line=2622`
- `SFDUT1-TX-0528` vaccination_or_immunization / p.119 / 猪疫苗免疫接种应注意的细节: （3）常用的病毒灭活苗 猪口蹄疫O型高效灭活疫苗、猪口蹄疫O型合成肽疫苗、菌格发猪圆环病毒疫苗、细小病毒病灭活疫苗、伪狂犬病灭活疫苗、传染性胃肠炎-流行性腹泻二联灭活疫苗、蓝耳病灭活疫苗等。 `source_id=SRC-0089; page=119; line=2692`
- `SFDUT1-TX-0536` vaccination_or_immunization / p.120 / 猪疫苗免疫接种应注意的细节: （6）选择好注射方法和部位 猪传染性胃肠炎-流行性腹泻二联活疫苗或灭活苗，必须后海穴（尾根下肛门上之间的凹陷处，又称交巢穴）注射，进针深度3日龄仔猪为0.5厘米，随猪龄增大而加深，成年猪为4厘米，肌内注射无效。猪口蹄疫O型灭活苗最好也后海穴注射，因为这里是穴位，产生的抗体多。猪气喘病活疫苗必须肺内注射。伪狂犬病基因缺失活疫苗对仔猪采用滴鼻效果更好。猪布氏杆菌病活疫苗要皮下注射，而且只限于非怀孕猪，怀孕猪注射会引起流产。凡肌内接种的疫苗，注射部位有耳根后颈部、臀部和后腿内侧等几处供选择，要求轮换选点，不要在同一部位重复注射。已经肿了的地方不能注射，否则疫苗不吸收。 `source_id=SRC-0089; page=120; line=2705`
- `SFDUT1-TX-0580` vaccination_or_immunization / p.133 / 猪口蹄疫: 在人和动物医学的所有疾病里，口蹄疫的传播性和致病毒力是最强的。其感染率之高、传播速度之快、对社会危害之大，均居众多种疫病之首。未经预防免疫的猪场，只要有1头猪感染或混进1头病猪，不过数日便会传染给全群、全场的猪引起发病，再好的隔离条件也难以幸免。由于该病传播快，发病率高达 $100\%$ ，生长育肥猪掉膘、育肥时间长、母猪流产、仔猪成窝死亡，不仅给养猪业造成巨大经济损失，而且直接关系到菜篮子工程，影响畜产品出口贸易和国际声誉。为扑灭口蹄疫和防止疫情扩大蔓延，对疫区要采取封锁措施、阻断交通、关闭交易市场和屠宰加工厂；扑杀病猪、销毁或无害化处理动物尸体，消毒处理污染物、畜舍及车辆工具；以及大面积的紧急免疫预防等各方面均要耗费大量的人力、物力、财力等。更为严重的是，如果彻底拔除疫点保证疫情不再发生，需要花费比扑灭口蹄疫更大的气力。如果不彻底根除疫源，给环境造成的污染会在很长时间内造成隐患。 `source_id=SRC-0089; page=133; line=2890`
- `SFDUT1-TX-0581` candidate_fact / p.133 / 猪口蹄疫: 病毒的传染性和感染致病毒力很强。据试验，采取病猪水疱皮，测其含毒量和感染力，对猪可达 $10^{-4} \sim 10^{-5}$ ，即1克蹄水疱皮可使1万至10万头猪感染发病。加上粪尿、口腔和呼吸道大量排毒，健康猪与其接触，便难以逃脱受其感染。 `source_id=SRC-0089; page=133; line=2896`
- `SFDUT1-TX-0582` vaccination_or_immunization / p.133 / 猪口蹄疫: 系，可将此病毒分为O、A、C、亚洲I型及南非I、Ⅱ、Ⅲ型共7个不同的血清型，型与型之间无交叉保护。亚洲最流行的血清型是O、A和亚洲I型，注射O型口蹄疫苗不能保护A型和亚洲I型口蹄疫。每个血清型又有若干亚型，目前已有80多个亚型，其中O型有10个亚型，病毒亚型间仅有一个有限的保护水平，意味着即使注射了猪口蹄疫O型疫苗，如果流行毒株发生变异，与疫苗毒株的亚型不同，也不能完全获得免疫保护，使防制口蹄疫的工作难度进一步加大。为此，还要加强平时的生物安全、兽医防疫等综合防控措施，才能防患于未然。 `source_id=SRC-0089; page=133; line=2900`
- `SFDUT1-TX-0583` candidate_fact / p.134 / 猪口蹄疫: （2）传染源 潜伏期感染、临床发病动物及病愈带毒猪为主要传染源。病猪破裂水疱的渗出物、呼出的气体、分泌物、唾液、粪尿、奶、精液及肉和副产品均可排出比牛羊等其他感染动物更多的病毒。故有绵羊是“储存器”（它们保持病毒，常常没有症状），猪是“放大器”（它能将致病力弱的毒株增强为致病力强的毒株），牛是“指示器”（牛对口蹄疫最容易感染）之说。此外，被病毒污染的饲料、饮水、空气、车辆、用具等也是重要传染源。通过悬浮微粒病毒可随风散播到相当远的地方。 `source_id=SRC-0089; page=134; line=2907`
- `SFDUT1-TX-0584` vaccination_or_immunization / p.134 / 猪口蹄疫: 潜伏期很短，通常为 $2 \sim 3$ 天，长的可达 $7 \sim 10$ 天。已经免疫而保护力不足的猪，潜伏期通常延长。且记，成年猪和仔猪的临床症状不一样。成年猪主要表现为发生水疱和跛行，而小猪经常呈心肌炎、瘫痪而猝死。要保持高度警惕，每天观察猪群，及早发现，防止蔓延。 `source_id=SRC-0089; page=134; line=2916`
- PHASE2_ENCODING_QUARANTINED: one damaged extracted fact line was removed from runtime text because it contained UTF-8 replacement characters. See `issues/phase2_encoding_quarantine_2026-05-09.md`. Original anchor: fact_id=SFDUT1-TX-0585; source_id=SRC-0089; page=134; line=2918.
- `SFDUT1-TX-0586` vaccination_or_immunization / p.135 / 猪口蹄疫: 根据流行病学特点（传播速度极快，发病率极高，猪、牛、羊等偶蹄动物患病等）、临诊症状（成年猪主要是口、鼻、蹄、乳房等部位出现水疱和跛行、卧地不起、死亡率低；哺乳仔猪因急性心肌炎常突然死亡，且死亡率极高，常成窝死亡）和剖检变化（仔猪可见心肌炎，心肌表面出现灰白色条纹，酷似虎斑），一般可做出初步诊断，定为疑似猪口蹄疫病例，但因水疱病变与“猪水疱病”(SVD，仅猪患病，牛、羊不发病)、猪水疱性口炎（VS，通常感染牛、马，很少感染猪）极相似，不易区分，确诊必须依靠实验室。病原学检测可应用间接夹心酶联免疫吸附试验（I-ELISA）和分子生物学检测技术（如RT-PCR）等，互相佐证，进行快速鉴定，确定血清型和不同亚型。疑似口蹄疫病例，在不能获得病原学检测样本的情况下，未免疫猪血清抗体检测阳性或免疫猪非结构蛋白抗体ELISA检测阳性，可判定为确诊口蹄疫病例。 `source_id=SRC-0089; page=135; line=2930`
- `SFDUT1-TX-0587` treatment_or_prevention / p.135 / 猪口蹄疫: （1）严格执行《动物防疫法》和《口蹄疫防治技术规范》。 `source_id=SRC-0089; page=135; line=2934`
- `SFDUT1-TX-0588` vaccination_or_immunization / p.135 / 猪口蹄疫: 坚持预防为主的方针，采取强制免疫预防为主及扑杀结合的综合防控措施，控制疫情发生。 `source_id=SRC-0089; page=135; line=2936`
- `SFDUT1-TX-0589` vaccination_or_immunization / p.136 / 猪口蹄疫: 接种疫苗是国际上公认的防制口蹄疫的有效措施，要认真落实 `source_id=SRC-0089; page=136; line=2940`
- `SFDUT1-TX-0590` vaccination_or_immunization / p.136 / 猪口蹄疫: 好农业部《2012年国家动物强制免疫计划》，在尚未发生口蹄疫之前，定期有计划地对所有健康猪群进行O型口蹄疫强制预防性免疫接种（经过 $2\sim 4$ 周可使其在免疫期内产生免疫力）。我国现用的是猪O型口蹄疫灭活疫苗和口蹄疫O型合成肽疫苗（双抗原）。免疫28天后要进行免疫效果监测，存栏猪免疫抗体合格率 $\geqslant 70\%$ 判定为合格，否则要查找原因及时补免。发生疫情时，对疫区、受威胁区全部易感家畜进行一次强化免疫。 `source_id=SRC-0089; page=136; line=2942`
- `SFDUT1-TX-0591` vaccination_or_immunization / p.136 / 猪口蹄疫: 笔者自1996年以来，广泛听取国内多名知名专家、学者及同行的建议与指导，参考全国防制牲畜口蹄疫总指挥部办公室（1998）13号文印发的免疫程序，不断总结经验，逐步探索出一套比较科学、行之有效的免疫方法和程序，并推荐给许多猪场实施，均取得良好预防效果，现介绍如下。 `source_id=SRC-0089; page=136; line=2944`
- `SFDUT1-TX-0592` vaccination_or_immunization / p.136 / 猪口蹄疫: ① 疫苗选择。选用中牧兰州生物药厂或中农威特生物科技公司采用进口206佐剂生产的猪口蹄疫O型灭活疫苗（Ⅱ），俗称高效浓缩苗，注射后15天产生免疫力，免疫期为6个月。 `source_id=SRC-0089; page=136; line=2946`
- `SFDUT1-TX-0593` vaccination_or_immunization / p.136 / 猪口蹄疫: a. 后备种公、母猪：仔猪二免后，配种前免疫一次；如果仔猪未经二次免疫，应在配种前间隔1个月免疫2次。 `source_id=SRC-0089; page=136; line=2952`
- `SFDUT1-TX-0594` vaccination_or_immunization / p.136 / 猪口蹄疫: b. 经产母猪：每次产前45天免疫一次，4毫升/头，以确保产后乳汁中有较高水平的母源抗体，使哺乳仔猪和保育仔猪有足够的被动免疫保护。空怀母猪要及时补免，必须保证一年至少免疫2次。 `source_id=SRC-0089; page=136; line=2954`
- `SFDUT1-TX-0595` vaccination_or_immunization / p.137 / 猪口蹄疫: c. 种公猪：每 4 个月免疫一次，4 毫升/头。 `source_id=SRC-0089; page=137; line=2956`
- `SFDUT1-TX-0596` vaccination_or_immunization / p.137 / 猪口蹄疫: d. 免疫母猪所生断奶仔猪： $65 \sim 75$ 日龄首免，2毫升/头；1月后加强免疫1次，3毫升/头。 `source_id=SRC-0089; page=137; line=2958`
- `SFDUT1-TX-0597` vaccination_or_immunization / p.137 / 猪口蹄疫: e. 未免疫母猪所产仔猪： $28\sim 35$ 日龄首免，1个月后强化免疫1次。 `source_id=SRC-0089; page=137; line=2960`
- `SFDUT1-TX-0598` compliance_or_safety / p.137 / 猪口蹄疫: a. 严格执行生物制品使用规范和操作技术，本疫苗仅用于接种健康猪，临产前1个月的母猪、未断奶的仔猪禁用。 `source_id=SRC-0089; page=137; line=2964`
- `SFDUT1-TX-0599` vaccination_or_immunization / p.137 / 猪口蹄疫: c. 破乳或分层超过规定量（水相超过1/10）的疫苗不能使用。 `source_id=SRC-0089; page=137; line=2966`
- `SFDUT1-TX-0600` vaccination_or_immunization / p.137 / 猪口蹄疫: d. 疫苗应在 $2 \sim 8^{\circ} \mathrm{C}$ 下冷藏运输。 `source_id=SRC-0089; page=137; line=2967`
- `SFDUT1-TX-0601` vaccination_or_immunization / p.137 / 猪口蹄疫: e. 疫苗不可冻结，一旦开封，应在当日用完。 `source_id=SRC-0089; page=137; line=2968`
- `SFDUT1-TX-0602` vaccination_or_immunization / p.137 / 猪口蹄疫: 不注射疫苗是万万不能的，但注射疫苗也不是万能的。因为口蹄疫有7个血清型，注射猪的口蹄疫O型高效灭活苗后，仍不能防控A型或亚洲I型口蹄疫。 `source_id=SRC-0089; page=137; line=2971`
- `SFDUT1-TX-0603` vaccination_or_immunization / p.138 / 猪口蹄疫: 严密监视疫情动态，切实加强各项生物安全和兽医防疫措施，严防各种渠道传入疫情，一旦发生和传入疫情，必须按照“早、快、严、小”的原则，采取紧急措施及时就地消灭，严格封锁，防止疫情扩大蔓延。扑杀、销毁病猪及同群猪，进行无害化处理；对污染的猪舍、场所、用具等应彻底消毒；对受威胁区所有易感猪紧急免疫接种，或用口蹄疫高免血清或康复动物血清进行被动免疫。在发生疫情的猪舍内，最好能对尚未出现临床症状的猪群接种口蹄疫康复血清（发病 $21\sim 60$ 天内的康复猪采血）， $5\sim 8$ 毫升/头，按种后12小时即可起到被动免疫作用，并可维持20天。仔猪治疗量是1毫升/千克体重。血清要在冰箱保鲜层（ $4\sim 8^{\circ}\mathrm{C}$ ）存放，切忌冰冻。发现口蹄疫后，应迅速报告疫情。 `source_id=SRC-0089; page=138; line=2975`
- `SFDUT1-TX-0604` drug_interaction / p.138 / 猪口蹄疫: 要做好养猪场消毒池、装猪台、运载工具、用具、场地、人员等的预防性常规消毒，每周圈舍全面消毒一次，每月全场彻底消毒一次。发生疫情时要加大消毒力度和消毒药的浓度（1～2倍），增加消毒次数（每天2次），并认真对人畜体表及其接触过的器具消毒。并注意不同类别的消毒剂切勿混用，酸碱类药物不得同时使用，以免发生拮抗和中和作用，降低药效。切勿频繁交替使用不同类型的消毒剂，以免降低消毒效能，绝不能使用对病毒无效的杀菌消毒药品，如来苏尔、新洁而灭等或去污剂。 `source_id=SRC-0089; page=138; line=2992`
- `SFDUT1-TX-0605` vaccination_or_immunization / p.138 / 猪口蹄疫: 最后强调指出：猪水疱病（SVD，也是一类动物疫病，仅猪发病，牛、羊不发病），在临床症状上与猪口蹄疫很难区别，注射猪O型口蹄疫疫苗预防不了猪水疱病，也要采取与猪口蹄疫相同的综合防制措施，严加防范。 `source_id=SRC-0089; page=138; line=2994`
- `SFDUT1-TX-0631` vaccination_or_immunization / p.147 / 猪圆环病毒病: PCV常与PRRSV、PPV、PRV等其他病毒及肺炎支原体、副猪嗜血杆菌、猪链球菌、巴氏杆菌等混合感染，引发许多附加症状，使该病的诊断趋于复杂化和多样化，更加剧了该病的危害性， $5\sim$ 12周龄的仔猪感染后多表现为PMWS；b.免疫刺激，如油乳剂灭活疫苗（如支原体、传染性胸膜肺炎、口蹄疫、蓝耳病灭活疫苗等）、佐剂，均可刺激病毒在猪体内的复制；c.环境因素，如氨气、内毒素等；d.应激因素，如运输、混群等。②PCV-2母源抗体可通过初乳从母猪传到仔猪，可有效预防仔猪免于发生PMWS，所以仔猪一定要吃足初乳。没有从母猪得到母源抗体的仔猪感染PCV-2后容易发生PMWS。③PCV-2相关疾病暴发与流行的原因：a.集约化养猪的出现，导致管理、操作的改变；b.宿主遗传的改变与世界范围内的流动；c.早先出现的PRRS、PR、PP等病原体的混合感染。 `source_id=SRC-0089; page=147; line=3113`
<!-- SFDUT_1_200_V13_1_END -->
