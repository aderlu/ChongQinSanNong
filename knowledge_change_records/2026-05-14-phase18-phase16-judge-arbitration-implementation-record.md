# 2026-05-14 裁判仲裁流程与CSV字段落地修改记录

## 一、修改目标

根据 `2026-05-14-swine-consultation-judge-arbitration-redesign-plan.md`，对猪病真实问诊数据的裁判、仲裁和最终 CSV 导出字段进行落地修改。

本次修改目标不是单纯调整分数，而是让 Phase18 和 Phase16 能围绕真实兽医问诊数据准入完成闭环：

```text
双裁判独立评分
→ 规则触发仲裁
→ 仲裁输出最终有效性与训练准入
→ Phase16 按 sft_admission 分流导出
```

## 二、修改前存在的问题

### 2.1 裁判维度偏旧

修改前 `wiki_first_judge_prompts.py` 和 `phase18_dual_judge_and_arbitrate.py` 仍主要使用旧维度：

- `evidence_fidelity`
- `clinical_reasoning`
- `safety_boundary`
- `question_resolution`
- `training_utility`
- `risk_control`
- `unsupported_expansion_control`
- `answer_completeness`
- `citation_integrity`
- `language_naturalness`

这些维度能做证据审计，但不能充分判断样本是否像真实猪场问诊，容易出现两个问题：

- 奖励带 `source=`、`fact=`、`page=` 的审计化回答。
- 对真实自然问诊回答的场景感、追问逻辑、可执行性判断不足。

### 2.2 仲裁触发偏窄

原仲裁触发主要依赖标签分歧、较小分差、fatal risk、高风险样本和少量 flag 分歧。它没有完整覆盖：

- 关键维度分歧。
- 60-75 灰区样本。
- 裁判低置信度。
- hard fail 聚合。
- L5/L6 默认仲裁。

这会导致总分接近但有硬伤的样本漏过，或低分但可修复样本无法被区分。

### 2.3 最终标签和导出动作不够细

原流程主要围绕 `pass/review/reject` 和 `accepted/review/rejected`。这会把训练数据治理压缩成二到三类，不能表达：

- 高质量主训练样本。
- 可用但低权重样本。
- 可修复样本。
- 必须拒绝样本。

Phase16 也没有稳定读取 `sft_admission`，因此即使 Phase18 给出更细判断，下游 CSV 和 JSONL 导出也不能真正执行。

## 三、本次修改的代码文件

### 3.1 `wiki_first_judge_prompts.py`

路径：

`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\wiki_first_judge_prompts.py`

主要修改：

- 将 `SCORECARD_VERSION` 更新为 `realistic_swine_consultation_eval_v4`。
- 将双裁判维度统一为 8 个真实问诊维度：
  - `scenario_realism`
  - `consultation_completeness`
  - `medical_correctness`
  - `followup_logic`
  - `triage_boundary`
  - `context_consistency`
  - `actionability`
  - `structure_labelability`
- 将仲裁维度更新为：
  - `medical_correctness`
  - `safety_boundary`
  - `consultation_completeness`
  - `scenario_realism`
  - `context_consistency`
  - `information_sufficiency`
  - `actionability`
  - `communication_naturalness`
- 将标签体系改为：
  - `high_quality_valid`
  - `valid`
  - `repairable`
  - `invalid`
- 在裁判输出合同中加入：
  - `hard_fail_flags`
  - `confidence`
- 在仲裁输出合同中加入：
  - `preferred_judge`
  - `preferred_judge_reason`
  - `hard_fail`
  - `hard_fail_codes`
  - `risk_level`
  - `main_issues`
  - `repair_suggestion`
  - `sft_admission`

解决的问题：

- 让裁判从“证据审计”转为“真实问诊有效性评估”。
- 避免主回答被要求暴露 citation/debug 字段。
- 让裁判模型必须输出可被 Phase18/Phase16 稳定消费的新字段。

### 3.2 `phase18_dual_judge_and_arbitrate.py`

路径：

`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase18_dual_judge_and_arbitrate.py`

主要修改：

- 新增标签归一化：
  - `normalize_label()`
  - `label_is_usable()`
  - `sft_admission_from_label()`
- 新增 hard fail 识别：
  - `hard_fail_flags_for()`
- 新增审计泄漏检测：
  - `AUDIT_LEAK_RE`
- 将 rule fallback 双裁判评分从旧维度改为真实问诊 8 维。
- 将仲裁触发规则扩展为：
  - `score_gap_ge_15`
  - `label_disagreement`
  - `hard_fail_flag`
  - `judge_fatal_risk`
  - `critical_dimension_gap_ge_2`
  - `avg_score_gray_zone_60_75`
  - `judge_low_confidence`
  - `high_risk_sample`
  - `l5_l6_default_arbitration`
  - Phase15 高风险信号
- 仲裁输出新增：
  - `hard_fail`
  - `hard_fail_codes`
  - `risk_level`
  - `sft_admission`
  - `main_issues`
  - `repair_suggestion`
  - `preferred_judge`
  - `preferred_judge_reason`
- `merge_semantic_result()` 改为优先使用仲裁最终结论，并产出：
  - `final_label`
  - `sft_admission`
  - `hard_fail`
  - `risk_level`
  - `main_issues`
  - `repair_suggestion`
- Phase18 简版 CSV 和 detailed CSV 均新增新字段。

解决的问题：

- 避免仲裁退化为平均分修正。
- 防止高分但有医学硬伤的样本进入主训练集。
- 让 L5/L6、食品安全、监管边界样本默认进入更保守复核。
- 让修复型样本带着明确问题和修复建议进入后续队列。

### 3.3 `phase16_export_layered_training_sets.py`

路径：

`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py`

主要修改：

- 新增导出队列：
  - `training_set_repair_queue.jsonl`
  - `training_set_low_weight_sft.jsonl`
- 新增 Phase18 最终字段读取：
  - `sft_admission`
  - `risk_level`
  - `hard_fail`
  - `hard_fail_codes`
  - `main_issues`
  - `repair_suggestion`
- `combined_decision()` 优先按 `sft_admission` 分流：
  - `main_sft` / `low_weight_sft` → accepted
  - `repair_queue` → review
  - `reject_queue` → rejected
- 训练主 CSV 新增真实问诊维度字段：
  - `judge_a_scenario_realism`
  - `judge_a_consultation_completeness`
  - `judge_a_medical_correctness`
  - `judge_a_followup_logic`
  - `judge_a_triage_boundary`
  - `judge_a_context_consistency`
  - `judge_a_actionability`
  - `judge_a_structure_labelability`
  - Judge B 同名字段
  - Arbiter 新维度字段
- 生产 CSV 新增准入字段：
  - `sft_admission`
  - `risk_level`
  - `hard_fail`
  - `hard_fail_codes`
  - `main_issues`
  - `repair_suggestion`

解决的问题：

- Phase18 的精细判断现在能真正影响 Phase16 导出。
- 主训练 CSV 能直接看到最终准入原因和仲裁风险。
- 可修复样本不再只能混在普通 review 队列里。

## 四、防乱码措施

本次修改采取以下措施降低乱码风险：

- 所有人工编辑均通过 `apply_patch` 完成，避免 PowerShell 重定向造成默认编码变化。
- 文档新增为 UTF-8 Markdown。
- 代码中已有 JSON/报告写入继续使用 `encoding="utf-8"` 和 `ensure_ascii=False`。
- 未使用批量字符串重写脚本改写中文内容。

## 五、预计更新效果

预期效果如下：

- 裁判更关注真实问诊数据有效性，而不是只看证据格式。
- 仲裁能识别分歧来源、硬伤和高风险边界样本。
- 高风险药物/监管样本默认更保守，减少危险样本进入训练集。
- 最终 CSV 可直接用于质量汇报和样本筛选。
- Phase16 可以按 `sft_admission` 形成主训、低权重、修复、拒绝四类输出。

## 六、验证情况

已完成的静态检查：

- 确认 `realistic_swine_consultation_eval_v4` 已写入 prompt 合同。
- 确认双裁判 8 维字段已在 prompt、Phase18 评分、Phase18 detailed CSV、Phase16 training main CSV 中出现。
- 确认仲裁触发码包含 `score_gap_ge_15`、`critical_dimension_gap_ge_2`、`l5_l6_default_arbitration`。
- 确认 Phase16 已新增 `repair_queue` 和 `low_weight_sft` 输出。
- 确认最终 CSV 字段包含 `sft_admission`、`risk_level`、`hard_fail_codes`、`main_issues`、`repair_suggestion`。

未完成的运行验证：

- 当前会话中历史 Python 路径均不可用：
  - `C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
  - `C:\Users\admin\AppData\Local\Python\bin\python.exe`
  - `C:\Users\admin\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- 因此未能执行 `py_compile` 和 Phase18 `--self-test`。

后续建议在 Python 环境恢复后立即执行：

```powershell
python -m py_compile `
  D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\wiki_first_judge_prompts.py `
  D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase18_dual_judge_and_arbitrate.py `
  D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py
```

并执行：

```powershell
python D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase18_dual_judge_and_arbitrate.py --self-test
```

## 七、残余风险

- 本次修改较大，尤其 Phase18 rule fallback 评分逻辑已从旧维度切到新维度，需要用真实小批次校准阈值。
- Phase16 保留了部分旧生产 CSV 映射字段，如 `final_diagnosis_accuracy`、`final_pathology_logic`，用于兼容既有报表；新分析应优先看新增真实问诊维度字段。
- 未完成运行级语法验证，需在 Python 恢复后补跑。

## 八、结论

本次已经完成裁判、仲裁和最终 CSV 字段的主体落地修改。

修改后，流程从旧的 `pass/review/reject` 审计式评价，升级为以真实猪病问诊数据准入为核心的：

```text
8维双裁判
→ hard fail 与分歧触发仲裁
→ 四档有效性标签
→ sft_admission 导出分流
```

这能更直接解决当前裁判和仲裁流程中“高分带硬伤”“自然回答被误伤”“可修复样本被丢弃”“仲裁无法指导导出”的问题。
