---
page_id: DIS-040
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-040-colibacillosis.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-040 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## HANDBOOK_RX_V13_1

- Original marker: `HANDBOOK_RX_V13_1_START` / `HANDBOOK_RX_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-040-colibacillosis.md`
- Byte size moved: 638
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- HANDBOOK_RX_V13_1_START -->
## Handbook Prescription Facts (SRC-0087, V13.1 batch)

- Batch status: 1 prescription facts from `raw/md/猪病诊疗与处方手册.md`.
- Source pages: 29.
- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md`.

- `HANDBOOK-RX-0029` 处方6：调痢生（8501）活菌制剂 适量；用法=用法：按50毫克/千克体重口服，每天1次，连用3天。；注=说明：该处方不能与抗生素同时应用。。`source_id=SRC-0087; page=29; line=1178-1184`
<!-- HANDBOOK_RX_V13_1_END -->

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-040-colibacillosis.md`
- Byte size moved: 5808
- Fact-like rows moved: 11
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 11

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Treatment Evidence (SRC-0088, V13.1 batch)

- Batch status: 11 treatment facts linked to this disease page.
- Source pages: 72, 97.
- Full matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`; fact index: `exports/veterinary_treatment_of_pigs_fact_index.csv`.

- `VTOP-TX-0090` vaccination / p.72 / Escherichia coli diarrhoea: This is a disease of the neonatal piglet. It normally starts with diarrhoea but quickly progresses to a septicaemia and death if there is no treatment. Escherichia coli will cause disease conditions in older pre- and post-weaned piglets. These will be described separately. In the neonatal piglet there are certain specific strains of E. coli involved, particularly those with the $^ \prime \mathrm { O ^ { \prime } }$ , `source_id=SRC-0088; page=72; line=1974`
- `VTOP-TX-0091` vaccination / p.72 / Escherichia coli diarrhoea: to suck. Death will occur in $^ { 4 8 \mathrm { ~ h ~ } }$ . However some may recover and regain condition. Electrolytes as well as antibiotics are vital for treatment. The outbreak will continue until the sows and gilts coming to the farrowing quarters have been vaccinated. There will be lateral spread from neighbouring litters. The infection will follow inadequately cleaned farrowing pens. Post-mortem will reveal a `source_id=SRC-0088; page=72; line=1978`
- `VTOP-TX-0092` treatment_candidate / p.72 / Escherichia coli diarrhoea: Treatment with oral antibiotics, namely spectromycin, neomycin or enrofloxacin, which are prepared in a special pump form, may be adequate or may have to be supplemented by a parenteral injection initially. `source_id=SRC-0088; page=72; line=1980`
- `VTOP-TX-0093` vaccination / p.72 / Escherichia coli diarrhoea: Control should be based on good hygiene and an ‘all-in all-out’ system in the whole farrowing shed. Although the condition is not nearly so common in outdoor pigs, a strict ‘turn and burn’ should be used with the farrowing huts. There are a wide variety of vaccines available which need to be given to the pregnant sow to provide passive immunity in the colostrum. It is vital that the vaccine contains the correct antig `source_id=SRC-0088; page=72; line=1982`
- `VTOP-TX-0094` vaccination / p.72 / Escherichia coli diarrhoea: E. coli may cause diarrhoea any time up until weaning. The faeces are often grey or white and hence the name ‘white scour’. The disease is much more common in piglets fed replacement diets. It may also occur if the temperature in the creep area of the farrowing house is too cold. In these cases often the pigs do not receive sufficient colostrum. Piglets will also not receive sufficient colostrum if the sow is ill wit `source_id=SRC-0088; page=72; line=1984`
- `VTOP-TX-0095` treatment_candidate / p.72 / Escherichia coli diarrhoea: E. coli may affect pigs in the post- weaning period but in the author’s experience it very rarely has a high mortality. It nearly always occurs after mixing batches of pigs after weaning. Diagnosis relies on growing pure growths of $\beta$ -haemolytic strains. These are not actually easy to grow from the faeces. They are only grown from the gut contents of a pig at post-mortem. They will not be found in any other org `source_id=SRC-0088; page=72; line=1986`
- `VTOP-TX-0096` vaccination / p.72 / Escherichia coli diarrhoea: Sow vaccination in post-weaning infections is not helpful. Rigid attention to detail to the environment of newly weaned pigs is vital. They should be warm and not subjected to draughts. Groups should be mixed as little as possible. The creep feed should initially be the same in the post-weaning period as the creep fed while the piglets were with the sow. All changes to the feed should be made very gradually. Various  `source_id=SRC-0088; page=72; line=1988`
- `VTOP-TX-0097` treatment_candidate / p.72 / Escherichia coli diarrhoea: Once pigs show neurological signs, there is little hope of recovery. Antibiotics such as amoxicillin will help, if given promptly prior to neurological signs. The remaining pigs should be given a less nutritious diet. `source_id=SRC-0088; page=72; line=1998`
- `VTOP-TX-0183` treatment_candidate / p.97 / Farrowing fever complex: A full clinical examination should be performed. The rectal temperature will normally be raised initially but this will often drop to a subnormal temperature as the disease progresses. Palpation of the udder will often reveal a hot, swollen, hard mammary gland. This indication of an acute mastitis will be shown in the majority of cases but is not an invariable sign. A vaginal examination may reveal piglets which will `source_id=SRC-0088; page=97; line=2596`
- `VTOP-TX-0186` treatment_candidate / p.97 / Farrowing fever complex: MMA is normally the result of an E. coli infection that affects the mammary gland and the uterus soon after parturition. It is normally associated with a slow farrowing. A streptococcal or staphylococcal metritis may also be involved, particularly after human intervention. In many cases the condition can be prevented by prompt treatment with a penicillin/streptomycin mixture being given im for 3 days following any hu `source_id=SRC-0088; page=97; line=2604`
- `VTOP-TX-0187` treatment_candidate / p.97 / Farrowing fever complex: For treatment of MMA a suitable antibiotic together with an NSAID should be injected. The choice of antibiotic has been given considerable debate: if the main organism is a Streptococcus sp., penicillin is the drug of choice, particularly as it gives high levels in the uterus. If a Staphylococcus sp. (and particularly a penicillin-resistant Staphy lococcus sp.) is involved, synthetic penicillins with or without clavu `source_id=SRC-0088; page=97; line=2608`
<!-- VTOP_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-040-colibacillosis.md`
- Byte size moved: 11524
- Fact-like rows moved: 21
- Candidate fact mentions moved: 3
- Dose/route/course fact markers moved: 1
- Source anchors moved: 22

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 增强证据 (SRC-0090, V13.1 batch)

- Batch status: 22 linked disease-control/treatment facts.
- Source pages: 224, 225, 226, 227, 228, 229, 230.
- Matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_200_363_fact_index.csv`.

- `SFDUT2-TX-0115` candidate_fact / p.224 / 猪大肠杆菌病: （4）内毒素 以水肿病菌株的内毒素注射给猪，可引起内毒素血症，主要表现为血压急剧下降、呕吐、里急后重、血管内凝血和白细胞先减少后增多等现象，最后导致内毒素性休克。 `source_id=SRC-0090; page=224; line=501`
- `SFDUT2-TX-0116` vaccination_or_immunization / p.224 / 猪大肠杆菌病: 仔猪黄痢又称早发性大肠杆菌病或新生仔猪腹泻，是发生在出生后几小时到1周以内的一种仔猪急性高度致死性传染病，以剧烈腹泻、排出黄色或黄白色水样粪便以及迅速脱水为特征。腹泻程度与大肠杆菌毒力、仔猪日龄和免疫状况有关。严重时临床表现为脱水、代谢性酸中毒及死亡。有些情况下，特别是日龄小的猪常常在没有出现腹泻时就已死亡。 `source_id=SRC-0090; page=224; line=506`
- `SFDUT2-TX-0117` treatment_or_prevention / p.225 / 猪大肠杆菌病: （3）临床症状 仔猪在出生时体况正常，最早可在出生后 $2 \sim 3$ 小时发病，一窝仔猪突然有 $1 \sim 2$ 头表现全身衰弱、很快死亡，以后其他仔猪相应发生腹泻，粪便颜色不一，从清亮到白色稍带程度不一的棕色，或是黄色浆状，含有凝乳小片。捕捉仔猪时，在挣扎和鸣叫中常由肛门冒出稀粪，粪便也可能仅从肛门滴落到会阴部，须仔细检查会阴部才可见到。在较严重流行时，少量病猪可能呕吐，由于体液流进肠管可迅速消瘦，体重下降 $30\% \sim 40\%$ ，并伴发脱水症状，腹肌松弛、无力，精神沉郁、迟钝，眼睛无光，皮肤蓝灰色、干燥无光泽。若为慢性或不很严重，猪的肛门和会阴部可能由于与碱性粪便接触而发炎，脱水不严重的病猪可能还饮水，治疗及时可以恢复。 `source_id=SRC-0090; page=225; line=522`
- `SFDUT2-TX-0118` candidate_fact / p.226 / 猪大肠杆菌病: 色、黄白色稀薄内容物，有时混有血液、凝乳块和气泡，其他肠段也出现气体，黏膜上皮脱落，绒毛袒露，肠系膜淋巴结肿大、充血，切面多汁。在并发休克的ETEC感染时，其特征性病变是小肠壁和胃壁显著充血及血性肠内容物。 `source_id=SRC-0090; page=226; line=526`
- `SFDUT2-TX-0119` vaccination_or_immunization / p.226 / 猪大肠杆菌病: ② 疫苗预防 选用大肠杆菌 K88 K99 987PF41 四价苗，初产母猪产前 4 周、2 周各接种一次，经产母猪于产前 2 周接种一次。或选用仔猪腹泻基因工程 K88、K99 双价灭活菌苗，于母猪产前 21 天接种一次，要用专用稀释液。 `source_id=SRC-0090; page=226; line=533`
- `SFDUT2-TX-0120` treatment_or_prevention / p.226 / 猪大肠杆菌病: ③ 微生态制剂疗法 最常用的是乳酸杆菌和双歧杆菌制剂，如调痢生（8501）、促菌生等，仔猪在吃奶前喂服，有益菌迅速在肠道内定殖，消耗氧气，促进厌氧菌增殖，有利于肠道正常菌群的建立与恢复，有效防治腹泻，但不能与抗生素同时使用。 `source_id=SRC-0090; page=226; line=534`
- `SFDUT2-TX-0121` drug_interaction / p.226 / 猪大肠杆菌病: ④ 药物治疗 丁胺卡那霉素、头孢噻呋、恩诺沙星、吡哌酸、庆大霉素、新霉素、增效磺胺甲基异噁唑、安普霉素、痢菌净等均为敏感药物。但是，由于长期使用上述药物，大肠杆菌对其普遍产生较强的耐药性，有些菌株同时耐受多种药物。因此，为了提高药物治疗效果，应每隔一段时间（一年或半年）进行一次大肠杆菌药敏试验，掌握细菌药敏状态的变化，减少用药的盲目性。治疗时尽量联合用药，或 $2 \sim 3$ 个月轮换用药，既可提高疗效，又能减少耐药菌株的产生。 `source_id=SRC-0090; page=226; line=535`
- `SFDUT2-TX-0122` treatment_or_prevention / p.226 / 猪大肠杆菌病: ⑤ 补液 可灌服“口服补液盐（ORS）”或腹腔注射 $5\%$ 葡萄糖生理盐水。防脱水的好办法是采用世界卫生组织在人医推广的口服补液盐，给仔猪口服补液，可有效地预防和治疗腹泻脱水，显著 `source_id=SRC-0090; page=226; line=536`
- PHASE2_ENCODING_QUARANTINED: one damaged extracted fact line was removed from runtime text because it contained UTF-8 replacement characters. See `issues/phase2_encoding_quarantine_2026-05-09.md`. Original anchor: fact_id=SFDUT2-TX-0123; source_id=SRC-0090; page=227; line=538.
- `SFDUT2-TX-0124` treatment_or_prevention / p.227 / 猪大肠杆菌病: （6）防治 与仔猪黄痢相似，治疗的同时可以用收敛剂，抗生素可交巢穴（又称后海穴）注射。 `source_id=SRC-0090; page=227; line=550`
- `SFDUT2-TX-0125` candidate_fact / p.228 / 猪大肠杆菌病: ③ 传播途径 病猪由粪便排出病菌，污染环境、饮水和饲料，通过消化道感染健康仔猪。 `source_id=SRC-0090; page=228; line=560`
- `SFDUT2-TX-0126` vaccination_or_immunization / p.228 / 猪大肠杆菌病: ⑤ 诱因 断奶、分群、运输、免疫注射、驱虫、环境及饲料与饲养条件改变、气候突变等各种应激因素，硒与维生素E缺乏以及集约化饲养免疫亚健康状态和其他感染因素的存在。 `source_id=SRC-0090; page=228; line=562`
- `SFDUT2-TX-0127` treatment_or_prevention / p.229 / 猪大肠杆菌病: ② 在饲料中添加适当的抗菌药物，如土霉素、新霉素等，有一定预防作用。 `source_id=SRC-0090; page=229; line=574`
- `SFDUT2-TX-0128` treatment_or_prevention / p.229 / 猪大肠杆菌病: ③ 本病无特效的药物治疗方法，报刊介绍的治疗方法不少，但疗效都不确实。一般可使用一些敏感的抗菌药物治疗或用葡萄糖、氯化钙、甘露醇等静脉注射，亚硒酸钠-维生素E肌注，安钠咖皮下注射，利尿素口服等对症治疗，对较慢性病例有一定疗效。 `source_id=SRC-0090; page=229; line=575`
- `SFDUT2-TX-0129` vaccination_or_immunization / p.230 / 猪大肠杆菌病: 利用抗血清防治大肠杆菌腹泻由来已久，是防治本病最有效的方法。老母猪血清或用大肠杆菌全菌免疫制备的血清含有针对各种菌体成分的抗体，可与黏附抗原结合，防止大肠杆菌黏附至肠黏膜上大量增殖，也可中和肠毒素和细菌裂解后释放的内毒素，终止其致病作用。血清作为异体蛋白质，还可非特异性地提高机体的抵抗力，在发病初期通常一次注射 $5 \sim 10$ 毫升就能使仔猪在4天内康复。 `source_id=SRC-0090; page=230; line=579`
- `SFDUT2-TX-0130` vaccination_or_immunization / p.230 / 猪大肠杆菌病: 抗血清的来源很广，各个猪场可用淘汰的老母猪制备。用本场常见血清型的大肠杆菌制成灭活菌苗后，每隔 $1\sim 2$ 周给母猪肌内注射一次，用量逐渐加大。最后一次免疫10天后无菌采血，分离 `source_id=SRC-0090; page=230; line=581`
- `SFDUT2-TX-0131` treatment_or_prevention / p.230 / 猪大肠杆菌病: 感染肠毒素性大肠杆菌是发生本病的先决条件，但饲养管理和环境因素对本病的发生及严重程度有着重要影响。因此，预防本病还应该从搞好饲养管理、环境卫生着手，尽可能降低环境中的细菌数量（特别是仔猪初生期），使仔猪有充足的营养、舒适的生活环境，尽可能减少应激，使仔猪有较强的抵抗能力。首先分娩栏的设计要合理，最好能随母猪的大小而调节，配合使用漏缝地板并及时清洁，减少母猪粪便的污染强度和范围。其次要保持舍内通风、干燥、温暖。三是给母猪提供营养丰富而易消化的饲料，加强母猪乳房的保健，使母猪有旺盛泌乳能力。四是减少应激，体热散失过多（含温过低）、室温突然改变、转栏、混群、密度过高等各种应激会诱发本病。 `source_id=SRC-0090; page=230; line=587`
- `SFDUT2-TX-0132` vaccination_or_immunization / p.230 / 猪大肠杆菌病: ① 购买的大肠杆菌疫苗，由于血清型可能与本场菌猪不同，免疫效果欠佳。一是可采用人工感染的方法，即对怀孕母猪在分娩前2周，用仔猪黄痢的粪便或死亡小猪的肠内容物拌料喂母猪，进行人工感染，母猪不发病；但能刺激母猪产生抗体，通过初乳保护仔猪。 `source_id=SRC-0090; page=230; line=591`
- `SFDUT2-TX-0133` vaccination_or_immunization / p.230 / 猪大肠杆菌病: ② 一定要吃好吃足初乳。众所周知，人类胎儿是通过母体胎盘获得免疫球蛋白（一种抗病蛋白）。母体血液循环系统中的抗体能自由穿过胎膜进入胎儿体内，保护出生的胎儿。而猪的胎盘（6层）是上皮绒毛膜型的，这种胎盘阻止母猪抗体通过胎盘直接传递给胎儿，新生仔猪出生时没有抵抗病原体的免疫力。所有初生仔猪最初的免疫力是出生后从母猪初乳获得的，称为被动免疫。仔猪出生后必须尽快吃到初乳（最迟不得晚于2小时），并令其在出生后12小时内尽可能多地吃到母源抗体含量丰富的初乳，尤其是头6小时内更重要，因为此时初乳中不仅母源抗体水平高（免疫球蛋白多，在4～6小时后很快下降），而且此时的免疫球蛋白不必经过消化就能完全地被消化道吸收到血液中。仔猪出生后对免疫球蛋白的完全吸收能力仅可持续12～18小时，18小时后，免疫球蛋白必须 `source_id=SRC-0090; page=230; line=592`
- `SFDUT2-TX-0134` vaccination_or_immunization / p.230 / 猪大肠杆菌病: 分解后才能吸收进血液，所以要尽快吃初乳。饲喂初乳6次可使仔猪获得充分的免疫保护。 `source_id=SRC-0090; page=230; line=594`
- `SFDUT2-TX-0135` dose_route_course / p.230 / 猪大肠杆菌病: ③ 收集好初乳。在分娩时和分娩后1小时内，初乳很容易排出。为保护吃不到初乳的仔猪，应在分娩过程中用人用的“吸奶器”立即收集母猪的初乳（每个乳头收集的奶不应超过5毫升），每头母猪可收集到60毫升，足够供 $3\sim 4$ 头仔猪使用（每千克体重15毫升）。初乳可冷冻保存，需要时取出，在 $37^{\circ}C$ 温水（不要热水）中解冻。初生仔猪只要能进食 $40\sim 60$ 毫升初乳（每小时灌一次，每次灌 $10\sim 20$ 毫升，连灌 $3\sim 4$ 次），将能提供足够的免疫球蛋白（如果有条件连灌 $5\sim 6$ 次更好）。收集初乳的工作目前仍被很多猪场所忽视，不吃初乳的仔猪仅靠吃牛奶是难养活的。 `source_id=SRC-0090; page=230; line=596`
- `SFDUT2-TX-0136` vaccination_or_immunization / p.230 / 猪大肠杆菌病: 总之，大肠杆菌病的防治是一个复杂的问题，必须综合考虑，多方面去控制（如在应用药物疫苗进行防治的时候，还得考虑营养代谢问题、补铁补硒的应用等）。 `source_id=SRC-0090; page=230; line=598`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/diseases/DIS-040-colibacillosis.md`
- Byte size moved: 658
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用证据增强 / SRC-0091

- 关联场景：大肠杆菌病。
- 药物/类别候选：磺胺类, 庆大霉素, 安普霉素, 新霉素。
- 生成边界：肠道感染应优先结合脱水、毒血症和药敏判断；氨基糖苷类全身治疗需注意吸收和肾毒性边界。
- 本块用于候选召回、鉴别增强和 rule 约束；不得单独输出剂量、疗程、休药期或 MRL。
- 来源：兽药合理应用与联用手册（1-200页），相关药物目录与正文页码见 `exports/veterinary_rational_use_1_200_drug_index.csv`。`source_id=SRC-0091`
<!-- RAU_1_200_V14_END -->

## RAU_401_600_V14

- Original marker: `RAU_401_600_V14_START` / `RAU_401_600_V14_END`
- Original runtime page: `wiki/diseases/DIS-040-colibacillosis.md`
- Byte size moved: 595
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 0

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）症候支持边界 / SRC-0093

- 腹泻/肠炎鉴别：收涩止泻证据不得掩盖大肠杆菌病、脱水和抗菌药标签复核。
- 证据用途：中药联用、禁忌、用药注意、症候支持和鉴别增强；不是病原确诊、报告处置、抗菌药剂量、休药期、MRL 或食品安全承诺来源。
- 索引：`exports/veterinary_rational_use_401_600_fact_index.csv`；矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`。
<!-- RAU_401_600_V14_END -->
