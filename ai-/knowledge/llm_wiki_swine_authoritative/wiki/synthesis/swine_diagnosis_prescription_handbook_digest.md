---
tags: [synthesis, swine, handbook, prescription, diagnosis, executable_source, v13_1]
updated: 2026-05-08T23:58:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, source_digest]
sources: [SRC-0087, RULE-HANDBOOK-PRESCRIPTION-001]
---

# 《猪病诊疗与处方手册》知识增强摘要

## Cross-cutting Facts

- 手册强调传染病防控应围绕控制传染源、切断传播途径和保护易感猪群三环节展开，且应从以治疗为主转向预防、保健和综合管理优先。`fact_id=HANDBOOK-CTRL-001; source_id=SRC-0087; page=1`
- 猪场选址和布局应考虑干燥、通风、水源、排污、与道路/集市/居民点及其他畜牧场距离，并将生活管理区与生产区分开；这是病例评估中环境和生物安全字段的来源。`fact_id=HANDBOOK-BIOSEC-001; source_id=SRC-0087; page=1`
- 疫苗程序应依据当地流行情况、母源抗体、上次免疫残余抗体、猪体免疫应答、疫苗性质、接种途径、疫苗配合和对生产性能影响综合制定。`fact_id=HANDBOOK-VACC-001; source_id=SRC-0087; page=3`
- 治疗原则为尽早实施、标本兼治，并采用综合性治疗措施；常用给药方式包括经口给药和注射给药。`fact_id=HANDBOOK-TX-001; source_id=SRC-0087; page=8`
- 饲料混饲给药应先称量药物并用梯度混合法混匀，再拌入日粮；该事实可支持给药方式识别、处方执行和用药操作结构化。`fact_id=HANDBOOK-DRUG-ROUTE-001; source_id=SRC-0087; page=8`
- 注射给药包括皮下、肌内、静脉、腹腔、胸腔和皮内等方式，需依据药液性质、数量和疾病情况选择，并要求器具和注射部位消毒。`fact_id=HANDBOOK-DRUG-ROUTE-002; source_id=SRC-0087; page=8`

## Disease Coverage Map

- 病毒性疾病覆盖：猪瘟 p10、口蹄疫 p11、乙型脑炎 p14、轮状病毒病 p16、传染性胃肠炎 p17、PRRS p20、猪流感 p21、流行性腹泻 p22、伪狂犬病 p24、细小病毒病 p25、PCV2 感染 p27。`fact_id=HANDBOOK-VIRAL-MAP-001; source_id=SRC-0087; pages=10-28`
- 细菌性/其他传染病覆盖：大肠杆菌病 p29、副猪嗜血杆菌病 p34、沙门氏菌病 p35、萎缩性鼻炎 p37、传染性胸膜肺炎 p38、猪丹毒 p40、猪肺疫 p42、链球菌病 p44、增生性肠炎 p46、梭菌性肠炎 p48、钩端螺旋体病 p49、附红细胞体病 p51、弓形虫病 p52、支原体肺炎 p53。`fact_id=HANDBOOK-BACT-MAP-001; source_id=SRC-0087; pages=29-56`
- 寄生虫覆盖：诊断和综合防制 p57-58；蛔虫、鞭虫、结节虫、姜片吸虫、华枝睾吸虫、类圆线虫、后圆线虫、毛首线虫、疥螨、蠕形螨和虱等 p58-78。`fact_id=HANDBOOK-PARASITE-MAP-001; source_id=SRC-0087; pages=57-78`
- 内科、营养代谢和中毒覆盖：普通内科 p80-95，营养代谢 p96-115，中毒 p116-138；可补强非感染性鉴别诊断和对应处方/处置事实。`fact_id=HANDBOOK-NONINFECTIOUS-MAP-001; source_id=SRC-0087; pages=80-138`

## Executable Source Policy

- 来自本手册的处方、药物、剂量、疗程、给药方式、休药期、MRL 和合规结论可作为可执行结构化事实；事实必须保留手册页码。`fact_id=HANDBOOK-EXEC-001; source_id=SRC-0087; pages=4,8; rule=RULE-HANDBOOK-PRESCRIPTION-001`
- 手册目录覆盖大量传染病、寄生虫病、内科病和中毒病，因此病例生成或问答评估不得把腹泻、呼吸、消瘦、神经、繁殖或皮肤问题默认收敛到感染病；必须保留环境、营养、毒物、寄生虫和管理因素。`fact_id=HANDBOOK-DDX-001; source_id=SRC-0087; pages=10-138`
