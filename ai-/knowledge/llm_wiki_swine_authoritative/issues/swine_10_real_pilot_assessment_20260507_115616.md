# Swine 10 Real Pilot Assessment - 20260507_115616

## Artifacts

- JSON: `results/swine_10_real_pilot/swine_10_real_pilot_20260507_115616.json`
- CSV: `results/swine_10_real_pilot/swine_10_real_pilot_20260507_115616.csv`
- Summary: `results/swine_10_real_pilot/swine_10_real_pilot_summary_20260507_115616.json`

## Timing

- Average elapsed: 40.08 s/case
- P50 elapsed: 37.02 s/case
- P90 elapsed: 49.7 s/case

## Quality

- Average score: 78.4
- Score range: 65.0 - 88.0
- Pass/review/reject: 5 / 4 / 1
- Fatal risk count: 1
- Specific dose count: 0
- Specific withdrawal count: 0
- Average answer anchor count: 3.1

## Problems To Review

- SWINE10-001 非洲猪瘟: label=reject score=65 fatal=True dose=False withdrawal=False weaknesses=未明确提及非洲猪瘟为中国一类动物疫病（A0-MOA-573），未强调必须按中国官方法规和技术规范处置。未明确提及非洲猪瘟不能仅凭临床症状或大体病变诊断（SRC-0031），需依赖实验室检测确诊。未明确提及非洲猪瘟检测阳性时应报告当地畜牧兽医部门并按官方流程处理（A0-MOA-ASF-NORMALIZED-GUIDE），不得生成治疗替代报告。
- SWINE10-003 猪大肠杆菌病: label=review score=70 fatal=False dose=False withdrawal=False weaknesses=['evidence_anchoring: 缺失部分规则引用（如RULE-431, RULE-417未展开说明）。', 'clinical_reasoning: 未提及全群用药可能导致耐药菌选择、肠道菌群紊乱等风险。', 'regulatory_safety: 未引用ASF/FMD相关用药限制（如A1-WOAH-ASF/FMD），未说明禁用药物（如氯霉素、呋喃唑酮）。', 'drug_boundary: 未提供中国批准的猪用抗菌药清单（如《兽药使用指南》）。', 'diagnostic_sampling: 未说明采样方法（如棉拭子、粪便量）和送检时限（建议2小时内冷藏送检）。', 'data_usability: 未提供非抗菌药替代方案（如口服补液盐、锌制剂、益生菌）。']
- SWINE10-004 猪胸膜肺炎: label=review score=79 fatal=False dose=False withdrawal=False weaknesses=['evidence_anchoring（25分）：诊断部分未明确引用急性病变的具体证据（如出血、坏死、纤维素性胸膜炎的教材描述，source=SRC-0058），也未引用三类疫病分类的具体监管来源（A0-MOA-573）在文本中的位置，扣5分。', 'clinical_reasoning（20分）：治疗建议中‘向当地兽医主管部门报告疫情’缺乏直接证据支持（未引用具体规则或教材），扣4分。', 'regulatory_safety（20分）：未明确说明‘替米考星拌料是否属于中国批准用法’，存在潜在误导风险，扣3分。', 'drug_boundary（15分）：未重复强调‘禁止将教材讨论或美国标签迁移为中国用药建议’（RC-DRUG-001），扣3分。', 'diagnostic_sampling（10分）：未提及‘采样对象应代表主要临床表现’（RULE-031，source=SRC-0009），扣2分。', 'data_usability（10分）：整体结构清晰，但部分句子较长（如治疗建议段），影响可读性，扣1分。']
- SWINE10-007 猪球虫病: label=review score=78 fatal=False dose=False withdrawal=False weaknesses=['evidence_anchoring：部分诊断依据（如抗菌药无效、高湿环境）未直接引用结构化事实中的锚点证据，仅依赖教材章节的间接描述，证据锚定强度可加强。', 'clinical_reasoning：未明确说明如何结合肠道病变（如肠道卡他性炎症、出血等）进行综合诊断，临床推理链条不完整。', 'drug_boundary：虽指出托曲珠利需中国批准，但未明确说明当前资料仅为教材候选证据且未经复核，可能误导用户认为托曲珠利是可选药物之一。', 'diagnostic_sampling：未提及需通过粪便漂浮法或饱和盐水漂浮法检测卵囊，或通过肠道刮片检查发育阶段球虫，采样方法描述不足。']
- SWINE10-008 猪霉菌毒素中毒: label=review score=75 fatal=False dose=False withdrawal=False weaknesses=['evidence_anchoring扣分：未引用教材章节页码（textbook_chapter_start_page 1079）作为基础分类依据', 'clinical_reasoning扣分：未解释繁殖异常与ZEA的雌激素样作用机制关联强度', 'regulatory_safety扣分：未明确说明饲料检测需通过CMA认证实验室', 'diagnostic_sampling扣分：未具体说明采样方法（如玉米样本需多点混合取样）']

## Initial Judgment

- 该试跑使用真实模型调用、真实猪病 wiki 检索和真实 judge 评分。
- 若 review/reject 或无来源剂量/休药期比例较高，应先收紧 prompt 和规则卡，再扩到 30/100。
- 若大多数样本有 source anchors 且无硬失败，可进入 30 条 pilot。
