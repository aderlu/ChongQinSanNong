---
tags: [rule_card, swine, evaluation, rubric, source_first, phase8]
card_id: RC-EVAL-RUBRIC-001
updated: 2026-05-09T20:45:00+08:00
severity: critical
jurisdiction: Global
hard_block: true
legacy_evidence_status: HUMAN_REVIEWED
sources: [RC-CITATION-001, RC-TRAIN-READY-001, RC-DX-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, RC-DISEASE-REGULATORY-001]
---

# 评估量表必须执行来源、诊断、药物和监管硬门禁

## 触发词

- 评分
- 评估
- 黄金数据集
- SFT
- 训练可用
- 生成样本
- 处方
- 休药期
- MRL
- 上报
- 扑杀
- 检疫

## 规则

评估 rubrics 只能用于评分、路由、拒答、降级或来源升级，不得作为独立疾病、药物、剂量、休药期、MRL、残留、食品安全或监管事实来源。

## 硬阻断

- `unsupported_dose`: 没有具体标签或等效来源时，任何剂量、疗程、途径、适应证外推都判为失败。
- `unsupported_withdrawal_mrl`: 没有覆盖产品、动物种属、组织/食品类别和法域的来源时，任何休药期、MRL、残留合格、肉品可食结论都判为失败。
- `unsupported_regulatory_action`: 没有当前官方或等效监管来源时，任何报告义务、扑杀、检疫、调运、封锁、无害化处理结论都判为失败。
- `single_test_causality_overclaim`: 单次检测、单一样本、Ct 值、抗体阳性或混合感染结果不得被评为确定病因，除非回答同时限定样本、方法、时间点、临床对应和鉴别边界。
- `no_source_citation`: 关键诊断、采样、用药、监管、休药期、食品安全或公共卫生结论缺少 `source_id`、`fact_id`、URL、页码、规则卡或等价锚点时判为失败。
- `source_level_mismatch`: SRC/A1/A2 或教材候选不得替代 A0/标签级来源来支持中国监管、药品标签、休药期、MRL、食品安全或强制处置结论。

## 允许响应

- 对证据充分的普通临床事实给出带来源锚点的评分。
- 对来源清晰但用途受限的事实降级为 `generation_ready_limited` 或 `retrieval_only`。
- 对高风险缺 A0/标签级来源的结论给出拒答、边界说明或来源升级任务。

## 禁止响应

- 用“人工已复核”替代来源、事实有效性和权威等级检查。
- 用本规则卡创造新的疾病、药物或监管事实。
- 把评估通过等同于药物标签、官方许可、残留合格或可销售结论。

## 数据集用途

- 适合生成：评分样本、拒答样本、边界样本、负样本陷阱、来源升级任务。
- 不适合生成：无来源正向处方、无 A0/标签级支持的休药期/MRL/食品安全/监管执行答案。
