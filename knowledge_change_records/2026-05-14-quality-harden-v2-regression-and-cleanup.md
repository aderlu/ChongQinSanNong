# 2026-05-14 质量强化回归修复与清理记录

## 本次工作背景

在完成训练数据质量强化后，使用真实 30 条批次做回归时发现：

- 自然化重写已经生效
- 但部分样本仍被 `Phase15` 当作格式脏样本拒绝

这说明链路中存在“修复后状态没有正确传递到评估层”的问题。

## 修改前的问题

文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14b_naturalize_grounded_answers.py`

问题表现：

1. `Phase14b` 对答案做了自然化改写。
2. 但 `style_flags.dict_like_detected` 和 `style_flags.english_label_detected` 仍使用“改写前原答案”计算。
3. 导致 `Phase15` 继续按旧脏标记拒绝这些样本。
4. `Phase16` 又把它们继续送入 `format_repair_queue`。

这属于典型的“修复成功但状态同步失败”问题。

## 本次修改内容

修改文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14b_naturalize_grounded_answers.py`

具体修改：

1. `style_flags` 改为基于 `new_answer` 重新计算，不再沿用旧答案结果。
2. 扩展英文模板标签替换规则，兼容如下变体：
   - `Control - boundary evidence:`
   - `Diagnosis - support evidence:`
   - 含空格、连字符、大小写变化的标签形式

## 修改后解决了什么

1. 已被自然化修复的样本，不会再因为旧标签残留而被误拒。
2. `Phase15` 与 `Phase16` 终于能识别“已经修好的答案”。
3. `format_repair_queue` 只保留真正还需要处理的样本。

## 回归验证证据

### 第一轮

批次：

- `20260514_quality_harden_smoke`

结果：

- `Phase15 accepted=15 rejected=13`
- 拒绝原因中仍有大量 `dict_like_output` / `english_template_label_output`

结论：

- 说明自然化后状态没有正确传递

### 第二轮

批次：

- `20260514_quality_harden_smoke_v2`

结果：

- `Phase14b` 重写 12 条
- `Phase15 accepted=21 rejected=7`
- `Phase16 accepted=20 review=1 rejected=7`
- `format_repair_queue=5`

结论：

- 误拒问题已明显收敛
- 训练集与修复队列分流恢复正常

## 本次清理与整理动作

为了保证目录清晰，本次仅清理“已被 v2 明确替代的中间验证产物”，不删除正式批次和最新有效结果。

计划清理对象：

- `exports/generated_samples/naturalized_samples_20260514_quality_harden_smoke.jsonl`
- `exports/evaluated_samples/fact_evaluated_samples_20260514_quality_harden_smoke.jsonl`
- `exports/training_sets/training_set_manifest_20260514_quality_harden_smoke.json`
- `issues/wiki_first_generation_reports/phase14b_naturalize_20260514_quality_harden_smoke.json`
- `issues/wiki_first_generation_reports/phase14b_naturalize_20260514_quality_harden_smoke.md`
- `issues/wiki_first_generation_reports/phase15_fact_eval_20260514_quality_harden_smoke.json`
- `issues/wiki_first_generation_reports/phase15_fact_eval_20260514_quality_harden_smoke.md`
- `issues/wiki_first_generation_reports/phase15_reject_reasons_20260514_quality_harden_smoke.csv`
- `issues/wiki_first_generation_reports/phase16_training_export_20260514_quality_harden_smoke.json`
- `issues/wiki_first_generation_reports/phase16_training_export_20260514_quality_harden_smoke.md`

保留对象：

- 所有 `*_v2` 最新验证产物
- `real30_audit` 正式真实批次
- 更早的正式阶段性批次与治理修复记录

## 预计效果

1. 目录中不会同时保留同一回归批次的失效版和修正版，减少误读。
2. 训练数据质量回归链的最新有效证据更集中。
3. 汇报时可以明确说明：
   - 第一轮发现了状态传递 bug
   - 第二轮已修复并通过回归
