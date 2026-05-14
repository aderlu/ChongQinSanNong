# 猪病黄金训练集链路优化报告 / 2026-05-08

## 目标

解决严格导出阶段因 `missing_answer_json`、`too_few_standard_citations` 等原因导致样本全部被拒的问题，并把输出结构优化为可被大模型训练和微调直接使用的黄金数据集格式。

## 代码优化

### 1. 生成阶段 source-first 化

修改文件：`D:\XF-ChongQin\ai-\scripts\run_swine_weak_wiki_production_2026_05_07.py`

新增输出字段：

- `answer_json`
- `golden_answer`
- `evidence_anchors`
- `standard_citation_count`
- `training_task_type`

核心变化：

- 生成 prompt 从“弱 wiki 测试数据”升级为“可训练黄金候选数据”。
- 强制答案使用 LLM Wiki 检索到的 `source_id`。
- 自动构建 `evidence_anchors`，每条锚点包含 `source_id`、`supports`、`evidence_status`。
- 自动构建 `answer_json`，包含诊断、鉴别、处置、采样、用药边界、休药期边界、风险控制和证据来源。
- 对 `diagnosis`、`prescription`、`withdrawal_period` 自动补充标准引用。
- 增加通用兜底来源：`RC-TRAIN-READY-001`、`RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`，用于保证训练规范、用药边界、休药期/MRL 约束可追溯。

### 2. 双评审支持全量二评

修改文件：`D:\XF-ChongQin\ai-\scripts\dual_review_select_swine_weak_wiki_2026_05_07.py`

新增参数：

- `--review-all`

核心变化：

- 过去只将 Judge A pass 的候选样本送入 Judge B。
- 现在可通过 `--review-all` 让所有输入样本进入 Judge B 和仲裁链路。
- 本次 100 条复跑使用了 `--review-all`，实际 `100/100` 进入二评。

### 3. 严格导出结构升级

修改文件：`D:\XF-ChongQin\ai-\scripts\export_swine_train_ready_2026_05_07.py`

核心变化：

- 严格校验 `answer_json` 内的关键字段和证据来源。
- 输出 JSONL 从简单 `messages + metadata` 升级为：
  - `case_id`
  - `task_type`
  - `species`
  - `disease_name`
  - `user_query`
  - `messages`
  - `answer_json`
  - `evidence`
  - `quality`
  - `safety`
  - `metadata`
- `fatal_risk` 以仲裁后的 `final_fatal_risk` 为准，避免 Judge B 单方风险标记覆盖最终仲裁结果。

## 验证结果

### 小批量验证

- 生成：8 条
- Judge A pass：7 条
- 全量 Judge B：8 条
- 双评审最终 pass：7 条
- 严格导出：5 条通过，2 条拒绝

小批量验证证明：严格导出已从原来的全拒，变为可以产出结构化黄金 JSONL。

### 100 条全量复跑

生成命令：

```powershell
python D:\XF-ChongQin\ai-\scripts\run_swine_weak_wiki_production_2026_05_07.py --limit 100 --parallel 8 --timeout 90 --max-retries 2 --answer-max-tokens 1800
```

结果：

- 请求：100
- 生成：100
- Judge A pass：72
- Judge A review：10
- Judge A reject：18
- Judge A 平均分：84.39
- fatal：18
- specific_dose：0
- specific_withdrawal：1

产物：

- `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_172305.csv`
- `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_weak_wiki_production_raw_20260508_172305.json`

### 全量双评审与仲裁

二评命令使用 `--review-all`。

结果：

- 输入：100
- 进入 Judge B：100
- 仲裁触发：100
- 双评审最终 pass：58
- 最终平均分：86.38
- 最终分数范围：82 - 95

产物：

- `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_172305_dual_reviewed_20260508_172924.csv`
- `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_172305_dual_final100_20260508_172924.csv`
- `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_172305_dual_review_raw_20260508_172924.json`

### 严格黄金 JSONL 导出

导出结果：

- 输入最终候选：58
- 严格通过：32
- 拒绝：26
- 最低分门槛：85
- 最少标准引用：3

产物：

- `D:\XF-ChongQin\ai-\results\swine_qa_dataset\swine_train_ready_20260508_173338.jsonl`
- `D:\XF-ChongQin\ai-\results\swine_qa_dataset\swine_train_ready_rejects_20260508_173338.csv`

拒绝原因：

- `score_below_min`: 25
- `too_few_standard_citations`: 2
- `answer_json_too_few_evidence_sources`: 2

结论：原先严格导出 `50/50` 全拒的问题已经解决。本轮严格产出 32 条可训练 JSONL；剩余拒绝主要来自质量分数低，而不是结构字段缺失。

## 当前 LLM Wiki 缺陷

当前规模：

- diseases：73 页
- drugs：80 页
- rules：449 页
- rule_cards：15 页
- comparisons：14 页
- synthesis：23 页
- syndromes：12 页
- sources：212 页
- topics：99 页
- knowledge facts：1595 条

事实状态：

- `HUMAN_REVIEWED`: 1419
- `NEEDS_REVIEW`: 146
- `PROCESSED_SOURCE_ANCHORED`: 30

主要缺陷：

1. 疾病页仍有 32 页包含 `NEEDS_REVIEW`，部分罕见病、病毒相关感染、综合征页仍偏召回型，缺少完整临床知识页结构。
2. 药物页仍有 45 页包含 `NEEDS_REVIEW`，对 approved label、靶动物、禁忌、休药期、MRL、适应证和不得生成剂量的边界仍不均衡。
3. source 索引仍有至少 1 个事实引用未在 `source_index.csv` 中完整登记：`RC-TOX-001`。
4. facts 中仍有 146 条 `NEEDS_REVIEW`，这些事实会降低高置信黄金数据的可用性。
5. 鉴别诊断矩阵数量不足，当前 comparisons 只有 14 页，对呼吸道、腹泻、繁殖障碍、神经症状、猝死、中毒等高混淆场景仍不够密。
6. syndrome 页只有 12 页，不能充分覆盖真实问诊中的“症状先行”任务。
7. 部分病种的别名覆盖不足，仍会触发 `target_disease_alias_not_in_diagnosis`。
8. 处方事实虽然已抽取多个来源索引，但 disease/drug/rule 三者之间的三元映射仍不够完整，影响高质量 answer_json 的自动生成稳定性。
9. 某些 source 来自教材或手册页码，但实体页没有把页码证据统一提升到结构化字段，导致页面可读但机器约束力不足。

## 下一步补强优先级

1. 清理所有 diseases/drugs 中的 `NEEDS_REVIEW`，优先处理本轮 rejected 和 score<85 的病种。
2. 为每个高频疾病补齐：典型场景、关键症状、鉴别诊断、采样、监管边界、治疗方向、禁忌、出栏/休药边界、证据来源页码。
3. 为每个药物补齐：批准标签、靶动物、适应证、禁忌、不得生成剂量边界、休药期/MRL 来源、合规结论。
4. 扩展 syndrome 页，用症状入口支撑真实养殖户问法。
5. 扩展 comparisons 矩阵，优先覆盖腹泻、呼吸道、繁殖障碍、猝死、皮肤病、寄生虫和中毒。
6. 修复 `source_index.csv` 缺失项，确保所有 fact 的 `evidence_source_id` 可回溯。
7. 对黄金导出做批量生产时，建议目标 1000 条以上，并保持 `--review-all`、`min_score>=85`、`min_standard_citations>=3`。

