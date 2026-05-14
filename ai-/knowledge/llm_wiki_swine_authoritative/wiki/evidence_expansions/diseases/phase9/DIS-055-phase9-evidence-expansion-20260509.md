---
page_id: DIS-055
entity_type: disease_evidence_expansion
runtime_tier: evidence_expansion
default_runtime_retrieval: false
phase: phase9_runtime_cleanup_regression
moved_from: wiki/diseases/DIS-055-external-parasites-mange.md
generated: 2026-05-09T14:56:01+08:00
---

# DIS-055 Phase 9 Evidence Expansion

This file stores low-risk high-density evidence moved out of default runtime retrieval during Phase 9.

Runtime handling:

- Do not load this file for default production or evaluation retrieval.
- Load it only for audit, source lookup, evidence expansion, or manual review.
- Any diagnosis, treatment, regulatory, withdrawal-period, MRL, residue, or food-safety conclusion still requires rule-card gating and current source verification.

## VTOP_V13_1

- Original marker: `VTOP_V13_1_START` / `VTOP_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-055-external-parasites-mange.md`
- Byte size moved: 3208
- Fact-like rows moved: 6
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 6

<!-- VTOP_V13_1_START -->
## Veterinary Treatment of Pigs Treatment Evidence (SRC-0088, V13.1 batch)

- Batch status: 6 treatment facts linked to this disease page.
- Source pages: 56, 107, 113, 114, 115.
- Full matrix: `wiki/synthesis/veterinary_treatment_of_pigs_treatment_matrix.md`; fact index: `exports/veterinary_treatment_of_pigs_fact_index.csv`.

- `VTOP-TX-0070` treatment_candidate / p.56 / Haematomas: These normally occur in the ears of lop-eared breeds as a result of continuous shaking of the head, which is caused by mange mites. It is very important that the underlying cause, i.e. the mange, should be treated with injectable ivermectins. Pigs with haematomas should receive injectable antibiotics which can be continued with water medication and injectable NSAIDs, which also can be continued with water medication. `source_id=SRC-0088; page=56; line=1613`
- `VTOP-TX-0206` treatment_candidate / p.107 / Middle-ear infection: The main sign will be shaking of the head. This will result in the formation of aural haematomas in adult lop-eared breeds. The infection is likely to follow mange. Treatment must involve treating the sarcoptic mange as well as the secondary infection. Obvious aural haematomas may be treated as in dogs under a GA in a variety of surgical ways. In view of the dangers of anaesthetics in adult pigs, this procedure canno `source_id=SRC-0088; page=107; line=2867`
- `VTOP-TX-0225` treatment_candidate / p.113 / Demodectic mange: This is caused by Demodex phylloides. These mites will be found in normal hair follicles. If they occur in very large numbers they will cause small pustular lesions on the body. Normally only when pustules are seen on the face, which when incised will reveal a thick caseous pus containing thousands of mites, is a diagnosis of demodectic mange made. These mites are easily seen without staining under the high power on  `source_id=SRC-0088; page=113; line=3054`
- `VTOP-TX-0229` treatment_candidate / p.114 / Sarcoptic mange: sample is the ear margins and inside the pinnae towards the canal. Often the mites can be seen without any preparation just spread on a microscope slide and examined under low power. However many authorities suggest dissolving the crusts in warm $1 0 \%$ w/v potassium hydroxide. This is a fairly lengthy process. The prepatent period can be as short as 10 days but it is normally 2 weeks. The normal picture of an infec `source_id=SRC-0088; page=114; line=3074`
- `VTOP-TX-0230` treatment_candidate / p.114 / Sarcoptic mange: Control should be carried out by 6-monthly oral medication of ivermectins in the food. `source_id=SRC-0088; page=114; line=3082`
- `VTOP-TX-0234` treatment_candidate / p.115 / Aural haematoma: These are normally caused by violent head shaking caused by pruritic parasitic conditions. Normally the swelling is on the median aspect of the ear between the cartilage and the skin. The condition is usually restricted to lop-eared animals. The underlying cause must be treated, i.e. a doramectin injection to kill the mange mites, and if the swollen ear is left it will result in permanent scarring called a ‘cauliflow `source_id=SRC-0088; page=115; line=3116`
<!-- VTOP_V13_1_END -->

## SFDUT_1_200_V13_1

- Original marker: `SFDUT_1_200_V13_1_START` / `SFDUT_1_200_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-055-external-parasites-mange.md`
- Byte size moved: 693
- Fact-like rows moved: 1
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- SFDUT_1_200_V13_1_START -->
## 猪场兽药使用与猪病防治技术（1-200页） 增强证据 (SRC-0089, V13.1 batch)

- Batch status: 1 linked disease-control/treatment facts.
- Source pages: 123.
- Matrix: `wiki/synthesis/swine_farm_drug_use_1_200_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_1_200_fact_index.csv`.

- `SFDUT1-TX-0553` treatment_or_prevention / p.123 / 集约化猪场寄生虫病的防治措施及控制程序: 个体治疗猪疥螨病、猪蛔虫可选用辉瑞“通灭”（1%多拉菌素注射液）或 $1\%$ 伊维菌素注射液，每10千克体重注射0.3毫升。 `source_id=SRC-0089; page=123; line=2758`
<!-- SFDUT_1_200_V13_1_END -->

## SFDUT_200_363_V13_1

- Original marker: `SFDUT_200_363_V13_1_START` / `SFDUT_200_363_V13_1_END`
- Original runtime page: `wiki/diseases/DIS-055-external-parasites-mange.md`
- Byte size moved: 3748
- Fact-like rows moved: 9
- Candidate fact mentions moved: 5
- Dose/route/course fact markers moved: 0
- Source anchors moved: 9

<!-- SFDUT_200_363_V13_1_START -->
## 猪场兽药使用与猪病防治技术（200-363页） 增强证据 (SRC-0090, V13.1 batch)

- Batch status: 9 linked disease-control/treatment facts.
- Source pages: 265.
- Matrix: `wiki/synthesis/swine_farm_drug_use_200_363_treatment_matrix.md`; fact index: `exports/swine_farm_drug_use_200_363_fact_index.csv`.

- `SFDUT2-TX-0218` candidate_fact / p.265 / 猪疥螨病: ① 皮下注射杀螨制剂，选用法国施维雅“伊能净”（1%伊维菌素注射液），或美国辉瑞“通灭”（1%多拉菌素注射液），每10千克体重0.3毫升。 `source_id=SRC-0090; page=265; line=1158`
- `SFDUT2-TX-0219` treatment_or_prevention / p.265 / 猪疥螨病: ② 药浴或喷洒疗法， $20\%$ 杀灭菊酯（速灭杀丁）乳油，300倍稀释，全身药浴或喷雾治疗。注意：必须全身都喷到，并用该药液喷洒圈舍地面、猪栏及近地面之墙壁，以消灭散落的虫体。药浴或喷雾治疗后，再在耳廓内侧涂擦自配软膏（杀灭菊酯与凡士林，按1:100的比例配制）。因此药无杀卵作用，根据疥螨的生活发育史，在第一次用药后 $7 \sim 10$ 天要接着进行第2次同样的治疗，以消灭孵化出的螨虫。 `source_id=SRC-0090; page=265; line=1160`
- `SFDUT2-TX-0220` candidate_fact / p.265 / 猪疥螨病: ③ 饲料中添加 $0.6\%$ 伊维菌素预混剂（中美合资中佳大地、诺华生产），每吨饲料添加本品300克，连用7天。或每吨饲料添加大北农“帝诺玢”（ $0.2\%$ 伊维菌素预混剂）1000克，连用7天。 `source_id=SRC-0090; page=265; line=1162`
- `SFDUT2-TX-0221` treatment_or_prevention / p.265 / 猪疥螨病: 猪疥螨病是一种具有高度接触传染性的外寄生虫病，患病公猪通过交配传给母猪，患病母猪又将其传给哺乳仔猪，转群后断奶仔猪之间又互相接触传染。如此，形成恶性循环，永无休止。此外，病猪搔痒脱落在外界环境中的疥螨虫体和虫卵污染的栏舍、用具等也是重要传染源。因此简单地用药治疗患病个体，不能从根本上解 `source_id=SRC-0090; page=265; line=1170`
- `SFDUT2-TX-0222` treatment_or_prevention / p.265 / 猪疥螨病: 决问题。另外，疥螨病在多数猪场得不到很好控制的主要原因，在于对其危害性认识不足，在某种程度上，由于对该病的隐性感染和流行病学缺乏了解，饲养人员缺乏对猪耳损伤的检查，又常把生长猪过敏反应型螨病所致瘙痒这一主要症状，当作一种正常现象而不以为然，既忽视治疗，又忽视防控和净化，从而难以控制本病的发生和流行。 `source_id=SRC-0090; page=265; line=1172`
- `SFDUT2-TX-0223` treatment_or_prevention / p.265 / 猪疥螨病: 本病比较有效的控制方法和措施是：病猪隔离治疗与全场猪只预防结合起来，治疗预防与环境杀虫结合起来，才能收到事半功倍的效果。 `source_id=SRC-0090; page=265; line=1174`
- `SFDUT2-TX-0224` candidate_fact / p.265 / 猪疥螨病: (1) 皮下注射“伊能净” `source_id=SRC-0090; page=265; line=1176`
- `SFDUT2-TX-0225` candidate_fact / p.265 / 猪疥螨病: ① 妊娠母猪分娩前 $10 \sim 15$ 天皮下注射一次，种公猪必须每年至少注射两次，或全场一年两次全面注射（种公、母猪，春秋各一次）。 `source_id=SRC-0090; page=265; line=1177`
- `SFDUT2-TX-0226` candidate_fact / p.265 / 猪疥螨病: (2) 饲料中添加“伊力坦”（0.6%伊维菌素预混剂）每吨饲料添加本品300克，连用7天。适用于上述各阶段猪。优点是使用方便，无应激。 `source_id=SRC-0090; page=265; line=1182`
<!-- SFDUT_200_363_V13_1_END -->

## RAU_1_200_V14

- Original marker: `RAU_1_200_V14_START` / `RAU_1_200_V14_END`
- Original runtime page: `wiki/diseases/DIS-055-external-parasites-mange.md`
- Byte size moved: 644
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_1_200_V14_START -->
## 兽药合理应用与联用证据增强 / SRC-0091

- 关联场景：疥螨/外寄生虫。
- 药物/类别候选：伊维菌素, 阿维菌素类, 双甲脒, 拟除虫菊酯类。
- 生成边界：外寄生虫病例需结合群体处理、环境清理和复查，不得只生成单次用药。
- 本块用于候选召回、鉴别增强和 rule 约束；不得单独输出剂量、疗程、休药期或 MRL。
- 来源：兽药合理应用与联用手册（1-200页），相关药物目录与正文页码见 `exports/veterinary_rational_use_1_200_drug_index.csv`。`source_id=SRC-0091`
<!-- RAU_1_200_V14_END -->

## RAU_201_400_V14

- Original marker: `RAU_201_400_V14_START` / `RAU_201_400_V14_END`
- Original runtime page: `wiki/diseases/DIS-055-external-parasites-mange.md`
- Byte size moved: 600
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 1

<!-- RAU_201_400_V14_START -->
## 兽药合理应用与联用证据增强（201-400页）/ SRC-0092

- 关联场景：疥螨/外寄生虫。
- 药物/类别候选：双甲脒, 溴氰菊酯, 氰戊菊酯, 敌敌畏。
- 生成边界：杀虫药需要群体处理、环境控制、人员防护和休药期复核。
- 用途：症状入口、候选召回、鉴别诊断、对症支持和 drug-rule 约束。
- 不得单独输出剂量、疗程、休药期、MRL 或出栏可食用承诺。
- 来源：兽药合理应用与联用手册（201-400页）。`source_id=SRC-0092`
<!-- RAU_201_400_V14_END -->

## RAU_401_600_V14

- Original marker: `RAU_401_600_V14_START` / `RAU_401_600_V14_END`
- Original runtime page: `wiki/diseases/DIS-055-external-parasites-mange.md`
- Byte size moved: 600
- Fact-like rows moved: 0
- Candidate fact mentions moved: 0
- Dose/route/course fact markers moved: 0
- Source anchors moved: 0

<!-- RAU_401_600_V14_START -->
## 兽药合理应用与联用手册（401-600页）症候支持边界 / SRC-0093

- 疥癣瘙痒：蛇床子、硫黄等外用杀虫线索可召回，但需外寄生虫确诊和安全用药。
- 证据用途：中药联用、禁忌、用药注意、症候支持和鉴别增强；不是病原确诊、报告处置、抗菌药剂量、休药期、MRL 或食品安全承诺来源。
- 索引：`exports/veterinary_rational_use_401_600_fact_index.csv`；矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`。
<!-- RAU_401_600_V14_END -->
