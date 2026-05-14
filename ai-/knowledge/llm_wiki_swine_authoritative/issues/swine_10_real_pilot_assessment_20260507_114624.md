# Swine 10 Real Pilot Assessment - 20260507_114624

## Artifacts

- JSON: `results/swine_10_real_pilot/swine_10_real_pilot_20260507_114624.json`
- CSV: `results/swine_10_real_pilot/swine_10_real_pilot_20260507_114624.csv`
- Summary: `results/swine_10_real_pilot/swine_10_real_pilot_summary_20260507_114624.json`

## Timing

- Average elapsed: 50.6 s/case
- P50 elapsed: 47.53 s/case
- P90 elapsed: 61.49 s/case

## Quality

- Average score: 74.8
- Score range: 0.0 - 90.0
- Pass/review/reject: 7 / 2 / 0
- Fatal risk count: 0
- Specific dose count: 0
- Specific withdrawal count: 0
- Average answer anchor count: 3.7

## Problems To Review

- SWINE10-003 猪大肠杆菌病: label=review score=75 fatal=False dose=False withdrawal=False weaknesses={'evidence_anchoring': ['未引用SRC-0073关于沙门氏菌抗菌药疗效需谨慎评估的来源', '仔猪黄白痢分类标记为NEEDS_REVIEW（DIS-041）仍被引用'], 'clinical_reasoning': ['未提及猪痢疾（Brachyspira）的典型血便特征与当前病例的关联性', '缺少对脱水猪紧急补液方案的建议'], 'regulatory_safety': ['未明确说明两个月出栏与常见抗菌药（如恩诺沙星、阿莫西林）默认休药期的冲突', '未引用A0-MOA-BANNED-DRUG-250-POLICY具体禁用药清单'], 'diagnostic_sampling': ['建议采集病死猪组织但未指定具体部位（如回肠、结肠内容物）', '缺少对新鲜粪便保存条件（如冷藏）的说明']}
- SWINE10-007 猪球虫病: label=review score=75 fatal=False dose=False withdrawal=False weaknesses={'evidence_anchoring': ['未明确引用‘抗菌药治疗无效提示非细菌性腹泻’的间接证据来源（如轮状病毒、冠状病毒等病毒性腹泻对抗菌药无效的教材描述）。'], 'clinical_reasoning': ['未提及球虫病典型肠道病变特征（如小肠黏膜出血性坏死）或粪便性状（如黄色或灰色水样便）的描述，可能影响诊断准确性。'], 'regulatory_safety': ['未明确提示托曲珠利在中国可能未获批用于仔猪球虫病的风险（wiki/drugs/DRUG-027-toltrazuril.md中证据状态为‘NEEDS_REVIEW’且未完成中国监管来源核验）。'], 'drug_boundary': ['未提及托曲珠利在教材中的描述仅为‘抗球虫药活性’，不能外推为具体用药方案（source_id=SRC-0081 / PDF page 1043 & wiki/drugs/DRUG-006-anticoccidials.md）。'], 'diagnostic_sampling': ['未建议具体诊断采样方法（如肠道病变组织采样、粪便卵囊计数等）以支持综合判断。'], 'data_usability': ['未提供用户可操作的下一步建议（如联系兽医进行实验室检测、完善病史记录等）。']}
- SWINE10-009 猪疥螨病: label=None score=None fatal=None dose=False withdrawal=False weaknesses=

## Initial Judgment

- 该试跑使用真实模型调用、真实猪病 wiki 检索和真实 judge 评分。
- 若 review/reject 或无来源剂量/休药期比例较高，应先收紧 prompt 和规则卡，再扩到 30/100。
- 若大多数样本有 source anchors 且无硬失败，可进入 30 条 pilot。
