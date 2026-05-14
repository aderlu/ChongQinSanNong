# 2026-05-13 Phase18 Dual Judge And Arbitrate

## 旧逻辑问题

- Phase15 在结构检查、事实检查、hard gate 之后，只写入 `judge_check.mode=deterministic_placeholder`，没有真正的双裁判和仲裁。
- 旧弱 Wiki 双裁判契约里有 `total_score`、`fatal_risk`、`structured_pass`、`final_label`、`agreed_with_judge` 这类可复用字段，但没有适配 Wiki-first 的 `fact/anchor/rule_card/page` 语义。
- 高风险样本虽然会在 Phase15 被硬门禁约束，但 Phase18 之前没有单独记录“哪些样本直接跳过语义双裁判、为什么跳过”。
- 缺少仲裁触发规则的代码化定义，`fatal_risk` 优先级也没有在 Wiki-first 样本上被显式固定。

## 当前代码结构

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/wiki_first_judge_prompts.py`
  - 维护 Phase18 的契约常量。
  - 定义 `judge_a` / `judge_b` / `arbiter` 的输入结构。
  - 固定评分阈值、维度、仲裁分差阈值和高风险层定义。
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase18_dual_judge_and_arbitrate.py`
  - 读取 Phase15 的 `fact_evaluated_samples_*.jsonl`。
  - 先做路由：判断样本是进入双裁判还是直接跳过。
  - 对可进入样本执行 `judge_a`、`judge_b`、必要时 `arbiter`。
  - 生成 `semantic_final_metrics`、`semantic_final_decision` 和语义拒绝原因。
  - 输出 JSONL、JSON/CSV/MD 报告。

## 我做了什么

1. 新建 `wiki_first_judge_prompts.py`
   - 复用了旧双裁判常见契约风格：
     - `total_score`
     - `fatal_risk`
     - `structured_pass`
     - `final_label`
     - `agreed_with_judge`
   - 但把 judge 输入改成 Wiki-first 上下文：
     - `question`
     - `stage_2_grounded.answer`
     - `evidence_anchors`
     - `structure_check`
     - `fact_level_check`
     - `hard_gate_check`
     - `phase15 reject_reasons`

2. 新建 `phase18_dual_judge_and_arbitrate.py`
   - 明确了进入双裁判的条件：
     - `structure_check.passed=true`
     - `fact_level_check.passed=true`
     - `hard_gate_check.passed=true`
     - `evidence_anchors` 非空
   - 明确了直接跳过的条件：
     - hard gate 失败 -> `semantic_route=skipped_hard_gate`
     - 结构失败 -> `semantic_route=skipped_phase15_structure`
     - 事实失败 -> `semantic_route=skipped_phase15_fact`
     - 缺少锚点 -> `semantic_route=skipped_missing_anchors`
   - 为跳过样本保留：
     - `semantic_skip_reason`
     - `semantic_skip_codes`
     - `semantic_final_decision=rejected`

3. 实现了真正的双裁判
   - `judge_a`
     - `clinical_correctness`
     - `reasoning_consistency`
     - `wiki_grounding_fidelity`
     - `safety_boundary_clarity`
     - `training_usability`
   - `judge_b`
     - `safety_risk`
     - `unsupported_expansion`
     - `answer_completeness`
     - `language_quality`
     - `dataset_fit`
   - 两个 judge 都输出统一的旧风格字段：
     - `total_score`
     - `fatal_risk`
     - `structured_pass`
     - `final_label`
     - `summary`
     - `strengths`
     - `weaknesses`
     - `flags`

4. 实现了仲裁触发条件
   - `judge_a.final_label != judge_b.final_label`
   - 两裁判总分差 `>= 8`
   - 任一裁判 `fatal_risk=true`
   - L5/L6 或其他高风险样本
   - Phase15 高风险/执行性触发 warning
   - 对 `unsupported_expansion` 或 `boundary_clear` 判断不一致

5. 实现了最终标签合并和 fatal 优先级
   - `fatal_risk` 优先级最高。
   - 有 fatal -> 直接压成 `semantic_final_decision=rejected`
   - 无 fatal 且 `final_label=pass` 且 Phase15 已 accepted -> `semantic_final_decision=accepted`
   - 其余 -> `review` 或 `rejected`
   - hard gate 失败样本不能被 Phase18 改回 accepted

6. 增加了可独立验证能力
   - 在 `phase18_dual_judge_and_arbitrate.py` 内新增 `--self-test`
   - 覆盖了：
     - hard gate 失败直接跳过
     - 高风险边界样本强制触发仲裁
     - unsupported expansion 导致 fatal 并 reject

## 解决了什么

- 补上了 Phase15 之后真实存在的“语义双裁判 + 仲裁”空洞。
- 让 Phase18 不再只是占位逻辑，而是能对 Wiki-first 样本输出稳定的语义评审元数据。
- 把“跳过双裁判”和“为什么跳过”显式化，便于 Phase19/Phase16 后续准入。
- 把 `fatal_risk`、高风险样本、边界/拒答表达、unsupported expansion 的优先级固化成代码。

## 预期效果

- Phase18 会对 Phase15 全通过样本输出：
  - `judge_a_result`
  - `judge_b_result`
  - `arbiter_result`
  - `semantic_final_metrics`
  - `semantic_final_decision`
- Phase15 hard gate 失败样本会被直接标为跳过并拒绝，不会误进入训练准入链路。
- L5/L6 高风险样本会被强制仲裁或保守处理，降低严重误放风险。
- 后续 Phase19 只需要读取 Phase18 产物，就能实现“双通过才准入”的策略。

## 怎么验证

1. 运行内置自检：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase18_dual_judge_and_arbitrate.py --self-test
```

2. 对 Phase15 产物跑 Phase18：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase18_dual_judge_and_arbitrate.py
```

3. 核查输出：
   - `ai-/knowledge/llm_wiki_swine_authoritative/exports/semantic_evaluated_samples/semantic_evaluated_samples_YYYYMMDD.jsonl`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/phase18_semantic_eval_YYYYMMDD.json`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/phase18_semantic_eval_YYYYMMDD.csv`
   - `ai-/knowledge/llm_wiki_swine_authoritative/issues/wiki_first_generation_reports/phase18_semantic_eval_YYYYMMDD.md`

4. 重点人工检查：
   - hard gate 失败样本是否都被 `semantic_route=skipped_hard_gate`
   - L5/L6 样本是否都进入仲裁
   - unsupported executable expansion 是否一定触发 `fatal_risk`
   - `semantic_final_decision=accepted` 的样本是否同时满足：
     - `final_decision=accepted`
     - `hard_gate_check.passed=true`
     - `semantic_final_metrics.fatal_risk=false`

## 备注

- 这次严格没有改动 Phase17/19 文件。
- 由于本轮用户限制了可修改范围，未额外新增 `tests/` 下独立测试文件；改为在 Phase18 脚本内提供独立 `--self-test`，保证可验证性且不越界。
