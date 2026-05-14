---
tags: [comparison, swine, handbook, differential, executable_source, v13_1]
comparison_id: CMP-014
updated: 2026-05-08T23:58:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [SRC-0087, SYN-002, SYN-004, SYN-011, RULE-HANDBOOK-PRESCRIPTION-001]
---

# 手册疾病覆盖与鉴别入口

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## Viral Infectious Disease Entry

- 高热、出血、繁殖异常或群体急性传播时，优先从猪瘟 p10、口蹄疫 p11、乙型脑炎 p14、PRRS p20、猪流感 p21、伪狂犬病 p24、细小病毒病 p25 和 PCV2 感染 p27 建立传染病鉴别清单。`fact_id=HANDBOOK-CMP-001-viral; source_id=SRC-0087; pages=10-28`

## Diarrhea Entry

- 新生、断奶后或群体腹泻病例不应只按大肠杆菌处理；手册同时覆盖轮状病毒 p16、传染性胃肠炎 p17、流行性腹泻 p22、大肠杆菌病 p29、沙门氏菌病 p35、增生性肠炎 p46、梭菌性肠炎 p48、寄生虫 p57-78、胃肠炎 p82 和中毒 p116-138。`fact_id=HANDBOOK-CMP-002-diarrhea; source_id=SRC-0087; pages=16-138`

## Respiratory Entry

- 咳嗽、喘气、腹式呼吸、肺炎或胸膜肺炎样病变时，手册覆盖猪流感 p21、PRRS p20、萎缩性鼻炎 p37、传染性胸膜肺炎 p38、猪肺疫 p42、支原体肺炎 p53、支气管肺炎 p86、纤维素性肺炎 p88 和支气管炎 p89；应并列考虑感染、继发感染、环境和内科因素。`fact_id=HANDBOOK-CMP-003-respiratory; source_id=SRC-0087; pages=20-89`

## Wasting And Poor Growth Entry

- 消瘦、增重下降或慢性群体问题应同时召回 PCV2 感染 p27、寄生虫病 p57-78、胃肠溃疡/胃肠炎 p82-84、维生素/矿物质缺乏 p96-115、霉菌毒素和其他中毒 p116-138。`fact_id=HANDBOOK-CMP-004-wasting; source_id=SRC-0087; pages=27-138`

## Prescription Execution

- 该矩阵既用于候选召回和问诊组织，也可导向手册中的可执行处方、剂量、疗程、休药期、MRL 和合规事实；处方输出必须保留 `RULE-HANDBOOK-PRESCRIPTION-001` 与 `SRC-0087` 页码。`fact_id=HANDBOOK-CMP-005-executable; source_id=SRC-0087; pages=4,8`
