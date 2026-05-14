---
page_id: DIS-008
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-008 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- Byte size moved: 1060
- Fact-like rows moved: 2
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 2

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 2 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 22.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0019` 处方1：① 阿米卡星（丁胺卡那霉素）注射液 60万～120万单位；② 氯化钠3.5克 氯化钾1.5克 碳酸氢钠2.5克 葡萄糖20克；温开水1000毫升；③ 磺胺脒4克 次硝酸铋4克 小苏打2克；用法=用法：一次肌内注射，每日2次，连用 $3\sim 5$ 天。；用法：混合自由饮用。；用法：混合一次喂服，每日2次，连用 $2\sim 3$ 天。；注=。`source_id=SRC-0087; page=22; line=970-984`
- `HANDBOOK-RX-0020` 处方2 针灸：穴位：后三里、交巢、带脉，配蹄叉、百会等穴。；针法：白针或血针。；用法=；注=。`source_id=SRC-0087; page=22; line=986-990`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- Byte size moved: 918
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Treatment Evidence (SRC-0088, V13.1 batch)

- Batch status: 1 treatment facts linked to this disease page.
- Source pages: 110.
- Full matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`; fact index: `exports/veterinary_treatment_of_pigs_fact_index.csv`.

- `VTOP-TX-0080` vaccination / p.110 / Enteric Diseases Caused by Viruses and Their Treatment: This is caused by a coronavirus. The disease is also called porcine epidemic diarrhoea (PED). It shows clinical signs very similar to TGE (see below). Both conditions are now rare but TGE was common in the UK in the 1960s. Epidemic diarrhoea was first recorded in the UK in 1972. Historically it was less common than TGE. There are two forms of the disease. Both have a high morbidity like TGE but a reduced mortality. O `source_id=SRC-0088; page=110; line=1922`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- Byte size moved: 8977
- Fact-like rows moved: 14
- Candidate fact mentions moved: 2
- Dose/route/course fact markers moved: 0
- Source anchors moved: 14

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 14 linked disease-control/treatment facts.
- Source pages: 179, 181, 182, 183, 184.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0703` vaccination_or_immunization / p.179 / 猪流行性腹泻: 20世纪90年代，韩国、日本等亚洲国家暴发严重的哺乳仔猪高死亡率猪流行性腹泻，这些暴发是急性的，而且非常严重，以至于在临床上很难与典型的急性传染性胃肠炎相区别。在日本，哺乳仔猪的死亡率平均为 $70\%$ （ $30\% \sim 100\%$ ），在流行期间，成年猪只表现短暂的食欲不振和母猪奶量减少。在韩国，导致所有日龄猪腹泻，10日龄内仔猪死亡率高达 $90\%$ 。研究表明：亚洲区域的流行性腹泻在部分免疫母猪群中呈地方性流行。我国从2010年12月起，急性暴发席卷全国的导致所有日龄猪腹泻和新生仔猪高死亡率的疫情，而且用传统的TP二联灭活疫苗免疫效果很差，病因众说纷纭。据杨汉春教授报道：通过对北京、河北、山东、河南、浙江等地区12个发病猪场的临床粪便和肠道组织样本的病原学检测结果表明，引起猪只腹泻的主要病原是猪流行性腹泻病毒。对毒株的全基因组序测定表明，是一种新的变异的毒株，其S基因与韩国的流行毒株同源性最高。其特点是发生于哺乳仔猪，大多 $3 \sim 10$ 日龄以内发病最严重，呈现高发病率和高死亡率，导致整窝发病整窝死亡。发病率 $100\%$ ，病死率 $80\% \sim 100\%$ 。其他阶段的猪和母猪很 `source_id=SRC-0089; page=179; line=3595`
- `SFDUT1-TX-0704` candidate_fact / p.179 / 猪流行性腹泻: （2）传染源和传播途径 病猪和带毒猪以及污染物（运猪车辆、靴子等）是本病的主要传染源，粪便-口腔传播是主要的但并不是唯一的传染途径。病毒随粪便排出污染体表、周围环境、饲料、饮水、饲养管理用具、衣鞋和运输车辆等，易感猪摄入被污染的饲料、饮水或污染物等，通过消化道感染发病。同时，发病15天以内的母猪乳汁中也带毒，可感染哺乳仔猪。 `source_id=SRC-0089; page=179; line=3603`
- `SFDUT1-TX-0706` candidate_fact / p.181 / 猪流行性腹泻: 期，流行性腹泻感染引起的疾病比传染性胃肠炎引起的更为严重，体重迅速减轻（快出栏的肥育猪因腹泻体重可减轻15千克），但通常具有一过性特点，大多数经 $4\sim 7$ 天后不治自愈，仅有 $1\% \sim 3\%$ 的猪急性死亡。 `source_id=SRC-0089; page=181; line=3624`
- `SFDUT1-TX-0708` treatment_or_prevention / p.182 / 猪流行性腹泻: 目前本病尚无特效的治疗方法，抗菌药物治疗也无效（但可防止继发细菌感染），只能靠加强护理、提供充足饮水和采取对症疗法，可防止哺乳仔猪脱水和酸中毒，减少死亡，促进康复。 `source_id=SRC-0089; page=182; line=3640`
- `SFDUT1-TX-0710` vaccination_or_immunization / p.182 / 猪流行性腹泻: 苗（弱毒活疫苗优于灭活苗），也可选用传染性胃肠炎-流行性腹泻-轮状病毒三联弱毒活疫苗。肌内注射无效，必须采用后海穴（又名交巢穴，即尾根与肛门中间凹陷的小窝部位）注射，进针角度为与脊背平行稍上扬 $5^{\circ} \sim 10^{\circ}$ 角，不能平行进针，否则针头会穿透直肠将药液打进直肠而失去效果。 `source_id=SRC-0089; page=182; line=3646`
- `SFDUT1-TX-0711` vaccination_or_immunization / p.183 / 猪流行性腹泻: ① 生产母猪：9 月底或 10 月初，先首免 1 次，然后于产前 $20 \sim 25$ 天加强免疫 1 次，可通过母乳使仔猪获得被动免疫，防止相关病毒性腹泻的发生。 `source_id=SRC-0089; page=183; line=3650`
- `SFDUT1-TX-0712` vaccination_or_immunization / p.183 / 猪流行性腹泻: ② 后备母猪群：9月和10月普免2次，然后在产前 $20\sim 25$ 天再加强免疫1次，提高初乳中抗体水平，为哺乳仔猪提供更长期的被动免疫，并要保证仔猪吃足初乳。同时，对初产母猪还要接种仔猪大肠杆菌病多价基因工程疫苗，以减少细菌性因素的危害。 `source_id=SRC-0089; page=183; line=3652`
- `SFDUT1-TX-0713` vaccination_or_immunization / p.183 / 猪流行性腹泻: ④ 仔猪：9月底或10月初，对全场所有的越冬仔猪普遍免疫1次（11月底能出栏的肥育猪可不免），间隔 $3\sim 4$ 周再加强免疫1次。 `source_id=SRC-0089; page=183; line=3656`
- `SFDUT1-TX-0714` vaccination_or_immunization / p.183 / 猪流行性腹泻: （2）加强各项生物安全措施 任何疫病的发生必须有传染源、传播途径和易感动物三个环节，通过疫苗接种只能减少易感猪群的数量，不能过于倚重疫苗，把疫苗当作万能的，免疫过后就万事大吉。还必须严格封闭猪场，禁止车辆及闲杂人员进入猪场范围内，并做好灭鼠、除蝇、驱鸟等工作，要防止猫、狗等进入猪场。加强平时的清洁卫生、严格消毒，切断传染源和传播途径。坚持自繁自养，严防从发病猪场引进处于潜伏期或排毒、带毒的种猪，引种后至少隔离饲养1个月后无病方可混群。 `source_id=SRC-0089; page=183; line=3658`
- `SFDUT1-TX-0715` vaccination_or_immunization / p.184 / 猪流行性腹泻: （3）加强饲养管理和环境控制 小猪出生后6小时内要吃足初乳，以提供母源抗体保护。尽量实施“全进全出”的生产模式，至少保证产房和保育舍“全进全出”。寒冷季节要做好防寒保暖，1周龄仔猪要确保保暖箱温度达到 $32^{\circ} \mathrm{C}$ ，舍温要达到 $25 \sim 28^{\circ} \mathrm{C}$ ，同时要保持干燥。严把饲料原料采购关，不饲喂发霉饲料，饲料中应添加霉消安、耐而菲、畜安生、霉卫宝等脱霉剂或按 $0.2\% \sim 0.3\%$ 的比例添加能增强机体非特异性免疫力的天然植物制品——保力胺。 `source_id=SRC-0089; page=184; line=3664`
- `SFDUT1-TX-0716` vaccination_or_immunization / p.184 / 猪流行性腹泻: ① 对已发病的猪场，可选用传染性胃肠炎-流行性腹泻二联弱毒活疫苗或传染性胃肠炎-流行性腹泻-轮状病毒三联弱毒活疫苗，对临产前20天以上的未腹泻的怀孕母猪进行紧急预防接种，必须后海穴注射。 `source_id=SRC-0089; page=184; line=3668`
- `SFDUT1-TX-0717` vaccination_or_immunization / p.184 / 猪流行性腹泻: ② 对已发病猪场，对初生仔猪实行“乳前免疫”，即没吃初乳前先免疫，分别口服和注射传染性胃肠炎-流行性腹泻-轮状病毒三联弱毒活疫苗，或传染性胃肠炎-流行性腹泻二联活疫苗0.1头份（稀释好的疫苗要在1小时内用完），1小时后再吃奶；对 $2\sim 3$ 日龄仔猪可分别口服和后海穴注射0.2头份。可有效减少腹泻造成的损失，即使出现腹泻，症状也较轻微。 `source_id=SRC-0089; page=184; line=3669`
- `SFDUT1-TX-0718` vaccination_or_immunization / p.184 / 猪流行性腹泻: ④ 人工感染妊娠母猪。对于流行性腹泻变异株、嗜病毒、杯状病毒、牛病毒性腹泻病毒等引起的病毒性腹泻，目前尚无商品化疫苗。对于因未免疫或者免疫失败造成病毒性腹泻急性暴发的猪场，为将哺乳仔猪死亡率降到最低，可对11月至次年3月份期间分娩的、临产前半个月以上的怀孕母猪或空怀母猪进行强毒人工感染——“返饲法”：将含有病毒的病猪的粪便或采集 $2\sim 5$ 日龄发病症状典型的小猪的小肠（包括内容物）剪碎后（发病24小时内采集的病料最佳）拌在饲料里饲喂空怀或怀孕母猪，或将发病小猪的小肠结扎后连同肠内容物加适量的生理盐水，用不能加热至沸的普 `source_id=SRC-0089; page=184; line=3671`
- `SFDUT1-TX-0719` vaccination_or_immunization / p.184 / 猪流行性腹泻: 通豆浆机制成匀浆饲喂母猪（1头仔猪的肠管可返饲3头母猪），连续饲喂 $2\sim 3$ 天，间隔3周后再返饲一次。母猪经感染后15天便能激发产生抗体和乳汁免疫力，并通过初乳传递给哺乳仔猪，仔猪经被动免疫后可持续到断奶而不发病，并能缩短本病的流行时间。对临产15天的怀孕母猪只能返饲1次。“返饲法”有一定散毒风险，可使得强毒持续存在，成为重要的传染源，这是一种“亡羊补牢”、不得已而求其次的办法。提示注意：临产15天以内不能采用此法，因感染后15天内的乳汁带毒。 `source_id=SRC-0089; page=184; line=3673`
<!-- SFDUT_1_200_V13_1_END -->
