# 2026-05-13 Phase19 layered export admission

## 原来问题

Phase16 的训练集导出只依赖 Phase15 `fact_evaluated_samples` 中的 `final_decision`、`fact_level_check`、`hard_gate_check`。
这带来几个直接问题：

- 正向 SFT 准入没有接入 Phase18 语义复核结果，实际上仍是单阶段放行。
- `accepted/review/rejected` 三分流不存在，review 样本无法单独回流。
- 双裁判与仲裁状态没有进入导出样本 metadata，也没有进入 manifest。
- L6/L7 虽然有评估文件，但没有显式和 Phase18 准入规则绑定。
- reject reason 只保留了 Phase15 理由，无法说明 Phase18 的语义拦截原因。

## 原代码结构

原文件 `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase16_export_layered_training_sets.py` 的主结构如下：

- `read_jsonl` / `write_jsonl`：基础读写。
- `is_accepted`：用 Phase15 `final_decision=accepted` 且 fact/hard gate 通过作为唯一准入条件。
- `build_training_sample`：拼接训练样本，仅在 rejected/calibration 时附带 `reject_reasons`。
- `export_layers`：
  - L1-L4 accepted 进入正向 SFT
  - L5 accepted 进入 boundary negative
  - L6 全量进入 eval
  - 所有样本进入 L7 calibration
- `manifest`：仅统计 accepted/rejected 和各层数量，不记录 Phase18 状态。

也就是说，Phase16 原本是“Phase15 单输入导出器”。

## 修改内容

本次仅修改了：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase16_export_layered_training_sets.py`
- 新增独立测试 `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\test_phase19_layered_export_admission.py`
- 本留痕文档

没有修改 Phase17/18 文件。

### 集成复核补充

主线集成复核时发现一个字段兼容问题：

- Phase18 的实际输出字段为 `semantic_final_decision`，并且最终指标同时写在 `semantic_final_metrics.semantic_final_decision` 中。
- Phase19 初版优先识别 `semantic_decision`、`phase18_semantic_decision`、`final_semantic_decision` 等字段。
- 当 Phase16 显式接入真实 Phase18 JSONL 时，初版会退回读取 Phase15 的 `final_decision`，导致 Phase18 的 `review/rejected` 被误统计为 `accepted`。

修复方式：

- 在 `extract_phase18_fields()` 中新增对 `semantic_final_decision` 的优先识别。
- 同时兼容 `semantic_final_metrics.semantic_final_decision`。
- 补充读取 `judge_a_result.final_label`、`judge_b_result.final_label`、`arbiter_result.arbiter_final_label`，让 manifest 中的裁判状态不再为空。

修复效果：

- 修复前，小批次 Phase18 报告为 `accepted=1, review=3, rejected=4`，但 Phase16 误统计为 `accepted=7, rejected=1`。
- 修复后，Phase16 正确统计为 `accepted=1, review=3, rejected=4`。
- 正向 SFT 只接收 Phase15 与 Phase18 双通过样本，review/rejected 样本进入对应队列。

### 1. 接入 Phase18 结果

新增 Phase18 输入解析能力：

- 支持 `--phase18` 显式传入 Phase18 JSONL。
- 如果未显式传入，会在 `exports/` 下尝试搜索常见 Phase18/semantic review 文件名。
- 如果仍未找到，会尝试读取 `evaluated` 行内是否已被其他流程注入 Phase18 字段。
- 如果外部文件和行内字段都缺失，直接报错，避免继续导出“假双通过”数据。

### 2. 改为 Phase15 + Phase18 双阶段准入

新增组合准入逻辑：

- Phase15 通过条件：`final_decision=accepted` 且 `fact_level_check.passed=true` 且 `hard_gate_check.passed=true`
- Phase18 通过条件：`semantic_decision=accepted`
- 只有二者都通过，L1-L5 才能进入正向 SFT

对应硬要求落实：

- SFT 训练集只能接收 Phase15 + Phase18 都通过的样本。
- Phase18 `review` 样本不会进入正向 SFT。
- Phase18 `rejected` 样本不会进入正向 SFT。

### 3. 增加 review / reject 队列

在原有导出结构基础上保留主层文件，同时新增：

- `exports/training_sets/training_set_review_queue.jsonl`
- `exports/training_sets/training_set_rejected_queue.jsonl`

规则：

- Phase15 通过但 Phase18 为 `review` -> review queue
- Phase15 未通过 -> rejected queue
- Phase15 通过但 Phase18 为 `rejected` -> rejected queue

每条队列样本都保留原因字段，方便后续回流修复。

### 4. L6/L7 严格分流

保留原有层文件，但调整语义：

- L6 只进入评估/校准导出，不属于正向 SFT 准入。
- L7 全量作为 calibration/eval 样本导出，不属于正向 SFT。

这次实现中，L6 仍写入 `eval_l6_regulatory_guardrail.jsonl`，L7 仍写入 `eval_l7_judge_calibration.jsonl`，但正向 SFT 只限 L1-L5 且必须双通过。

### 5. 扩展 metadata / manifest

每条导出样本 metadata 新增：

- `export_bucket`
- `export_decision`
- `phase15.passed`
- `phase15.final_decision`
- `phase15.reject_reasons`
- `phase18.semantic_decision`
- `phase18.judge_status`
- `phase18.judge_a_status`
- `phase18.judge_b_status`
- `phase18.arbiter_status`

review/reject 样本继续保留：

- `reject_reasons`
- `review_reasons`

manifest 新增/更新：

- `review`
- `accept_review_reject_counts`
- `phase15_decision_counts`
- `phase18_semantic_decision_counts`
- `phase18_judge_status_counts`
- `phase18_judge_a_status_counts`
- `phase18_judge_b_status_counts`
- `phase18_arbiter_status_counts`
- `phase18.source_mode`
- `input_files.phase18`
- `input_file_hashes.phase18_sha256`

这样 manifest 能直接说明样本到底是被 Phase15 拦下、被 Phase18 送 review、还是经双裁判/仲裁后通过。

## 解决效果

修改后 Phase16 不再把 Phase15 accepted 直接当成 SFT 准入，而是执行：

1. 先检查 Phase15 事实/硬门禁是否通过
2. 再检查 Phase18 语义裁决是否 accepted
3. 决定进入 SFT、review queue、rejected queue 或 eval/calibration

因此达成了以下效果：

- 正向 SFT 只含双通过样本
- review/reject 队列可单独回流
- L6/L7 与正向 SFT 显式隔离
- 导出样本和 manifest 均保留 Phase18 语义裁决、双裁判、仲裁状态

## 预期更新结果

在存在 Phase18 输入时，重新运行 Phase16 后，预期会看到：

- L1-L5 正向 SFT 数量下降到“Phase15 accepted 且 Phase18 accepted”的交集
- `training_set_review_queue.jsonl` 出现需要复核的样本
- `training_set_rejected_queue.jsonl` 出现被 Phase15 或 Phase18 拒绝的样本
- `training_set_manifest_*.json` 中出现 review 计数和 Phase18 统计字段
- 导出样本 metadata 中能追溯语义裁决和仲裁状态

如果当前批次没有可识别的 Phase18 结果，脚本会直接报错，防止误导出。

## 验证方法

### 静态检查

执行：

```powershell
py -3.14 -m py_compile D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase16_export_layered_training_sets.py
py -3.14 -m py_compile D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\test_phase19_layered_export_admission.py
```

结果：通过。

### 独立测试

执行：

```powershell
py -3.14 D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\test_phase19_layered_export_admission.py
```

结果：

```json
{"passed": true}
```

### 测试覆盖点

独立测试验证了：

- Phase15 accepted + Phase18 accepted 才进入正向 SFT
- Phase18 review 进入 review queue，不进正向 SFT
- L6 保留在 eval，不进入正向 SFT
- L7 进入 calibration
- rejected queue 保留 rejected 样本
- manifest 记录 accept/review/reject 和 Phase18 arbiter 计数
- 缺失 Phase18 信号时会抛出错误，阻止误导出
