# 2026-05-14 阶段四 fallback 质量修复执行记录

## 一、任务来源

依据 `knowledge_change_records/2026-05-14-swine-consultation-pipeline-quality-staged-remediation-plan.md` 中“阶段四：修复 fallback 质量”的要求，检查并补齐当前项目中 fallback 质量控制。

阶段四目标：

- fallback 不得使用审计事实拼接做 `clinical_answer`。
- fallback 的主回答必须使用固定安全问诊模板。
- fallback 样本默认不进入主训练集。
- 降低 Phase15 中 placeholder、too_short、audit leak 等拒绝问题。

## 二、检查结论

检查时发现：

1. `phase14_generate_two_stage_samples.py` 已经存在安全 fallback 模板 `default_clinical_answer()`。
2. `phase14b_naturalize_grounded_answers.py` 已经存在 `fallback_clinical_answer()`，会在主回答为空时生成安全问诊模板。
3. Phase14/Phase14b 已经会写入：
   - `generation_fallback`
   - `fallback_default_review`
   - `stage_2_grounded.clinical_answer_fallback`
4. 但后续准入链路对这些 fallback 标记消费不够硬：
   - Phase15 未把 fallback 标记暴露为质量标记。
   - Phase18 未强制将 fallback 样本降级到 review/repair。
   - Phase16 导出阶段仍可能只看 `final_label` 和 `sft_admission`，存在 fallback 进入 accepted/train-ready 的风险。

因此，阶段四在“生成安全模板”层面基本已实现，但在“默认不进入主训练”层面尚未完全闭环。

## 三、本次修改内容

### 1. Phase15 增加 fallback 标记透传

文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase15_fact_level_evaluate_samples.py`

修改：

- 在 `style_quality_check()` 中识别：
  - `generation_fallback`
  - `fallback_default_review`
  - `stage_2_grounded.clinical_answer_fallback`
- 输出 `fallback_default_review` 标记。

目的：

- 让 Phase15 质量检查能显式保留 fallback 状态。
- 不把安全 fallback 模板直接判为失败，但为后续 review/repair 准入提供依据。

### 2. Phase18 将 fallback 样本默认降级

文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py`

修改：

- `phase15_warning_codes()` 新增：

```text
phase14_generation_fallback_default_review
```

- `merge_semantic_result()` 中，如果命中 fallback warning：
  - `sft_admission = repair_queue`
  - 如果原本是 `valid` 或 `high_quality_valid`，降级为 `repairable`
  - `reasons` 增加 `phase14:generation_fallback_default_review`

目的：

- 防止 fallback 样本仅凭模型评分进入 `main_sft` 或 `low_weight_sft`。
- 满足“fallback 样本默认不进入主训练”的阶段四要求。

### 3. Phase16 最终导出门再次拦截 fallback

文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase16_export_layered_training_sets.py`

修改：

- `combined_decision()` 识别：
  - `generation_fallback`
  - `fallback_default_review`
  - `stage_2_grounded.clinical_answer_fallback`
- 若命中 fallback：
  - `export_decision = review`
  - `sft_admission = repair_queue`
  - `export_reasons` 增加 `phase14:generation_fallback_default_review`

目的：

- 即使 Phase18 结果异常偏宽，Phase16 作为最后导出门也会阻止 fallback 进入 train-ready。

## 四、已满足的阶段四验收项

| 验收项 | 当前状态 |
|---|---|
| fallback 样本主回答长度 >= 120 | 已满足，Phase14 安全模板约 298 字符，Phase14b 模板也超过 120 字符 |
| fallback 样本审计泄漏 = 0 | 已满足模板层面要求，模板不含 `source=`、`fact=`、`rule=`、`page=`、`category`、`textbook_chapter` 等审计字段 |
| fallback 样本默认不进入 main_sft | 本次已补齐，Phase18 降级为 `repair_queue`，Phase16 导出为 `review` |
| Phase15 placeholder/too_short 降低 | 模板长度和问诊结构已满足降低风险的条件，需后续小批次运行验证具体数量 |

## 五、验证情况

已完成静态验证：

- 检索确认 Phase14 安全模板存在。
- 检索确认 Phase14b 安全模板存在。
- 检索确认 fallback 标记在 Phase15/Phase18/Phase16 中均可被识别。
- 检查 Phase14 默认模板不含审计字段片段。

本次未完成 Python `py_compile`，原因：

- 当前 shell 环境中未找到可用的 `python`、`py` 或历史记录中的 Python 路径。
- 因此未执行字节码编译检查。

后续若 Python 环境恢复，建议执行：

```powershell
python -m py_compile `
  ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py `
  ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14b_naturalize_grounded_answers.py `
  ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase15_fact_level_evaluate_samples.py `
  ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase16_export_layered_training_sets.py `
  ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py
```

## 六、预期效果

本次修改后，API 不稳定或模型未返回 `clinical_answer` 时：

1. Phase14/Phase14b 会生成安全问诊模板，而不是审计事实拼接。
2. 样本会保留 `generation_fallback` 或 `fallback_default_review`。
3. Phase18 会把该样本降级为 `repair_queue/review`。
4. Phase16 会最终阻止该样本进入 train-ready 主训练集。

这能解决阶段四最核心的问题：fallback 可以留痕和复核，但不能污染主训练数据。
