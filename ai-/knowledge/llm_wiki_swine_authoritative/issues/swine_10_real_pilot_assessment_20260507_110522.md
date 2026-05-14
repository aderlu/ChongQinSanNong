# Swine 10 Real Pilot Assessment - 20260507_110522

## Artifacts

- JSON: `results/swine_10_real_pilot/swine_10_real_pilot_20260507_110522.json`
- CSV: `results/swine_10_real_pilot/swine_10_real_pilot_20260507_110522.csv`
- Summary: `results/swine_10_real_pilot/swine_10_real_pilot_summary_20260507_110522.json`

## Timing

- Average elapsed: 146.42 s/case
- P50 elapsed: 6.6 s/case
- P90 elapsed: 286.24 s/case

## Quality

- Average score: 0.0
- Score range: 0.0 - 0.0
- Pass/review/reject: 0 / 0 / 0
- Fatal risk count: 0
- Specific dose count: 0
- Specific withdrawal count: 0
- Average answer anchor count: 0

## Problems To Review

- SWINE10-001 非洲猪瘟: label=None score=None fatal=None dose=False withdrawal=False weaknesses=
- SWINE10-002 猪流行性腹泻: label=None score=None fatal=None dose=False withdrawal=False weaknesses=

## Initial Judgment

- 该试跑使用真实模型调用、真实猪病 wiki 检索和真实 judge 评分。
- 若 review/reject 或无来源剂量/休药期比例较高，应先收紧 prompt 和规则卡，再扩到 30/100。
- 若大多数样本有 source anchors 且无硬失败，可进入 30 条 pilot。
