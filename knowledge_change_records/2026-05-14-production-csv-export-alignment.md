# 2026-05-14 生产级 CSV 导出对齐记录

## 本次目标

将当前猪病 LLM Wiki 训练数据链路的最终结果，导出为可直接用于训练和微调的生产级 CSV 文件，并对齐参考模板：

- `D:\XF-ChongQin\ai-\archives\runtime_artifacts\root_results_2026-05-13\chicken_disease_dataset_production_20260506_145945.csv`

同时保留猪病当前链路中的必要字段，不丢失治理、评估、锚点和风格质量信息。

## 修改前的问题

修改前，`Phase16` 只能输出：

- 分层 JSONL 训练集
- manifest JSON
- review / reject 队列 JSONL

问题在于：

1. 虽然适合工程内部流转，但不适合直接作为“最终交付格式”汇报或给训练侧消费。
2. 与历史鸡病、猪病生产数据的 CSV 交付习惯不一致。
3. 当前新增的评估和治理字段没有统一落到一份最终 CSV 中。

## 本次修改

修改文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py`

新增内容：

1. 新增 `PRODUCTION_CSV_FIELDS`
   - 参考鸡病模板主字段
   - 增补当前猪病链路必要字段

2. 新增 CSV 写出函数
   - `write_csv()`
   - 使用 `utf-8-sig`
   - 兼容 Excel / Windows 打开，降低乱码风险

3. 新增生产级 CSV 行构造逻辑
   - `build_production_csv_row()`
   - 将当前样本映射为生产 CSV 格式

4. 新增 metadata 汇总逻辑
   - `production_metadata()`
   - 保留：
     - sample_id / plan_id / skeleton_id
     - ability_layer / risk_class / expected_output_type
     - usage_scope / evidence_anchors
     - training_intent / evidence_depth_class
     - style_flags / style_rewrites
     - phase15 / phase18 关键信号
     - export_bucket / export_decision

5. 在 `Phase16` 主流程中新增双 CSV 输出
   - 全量生产 CSV
   - 仅 train-ready accepted 生产 CSV

## 输出结果

本次基于批次 `20260514_quality_harden_smoke_v2` 已产出：

全量生产 CSV：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\training_sets\swine_wiki_training_dataset_production_20260514_quality_harden_smoke_v2.csv`

训练可用 train-ready 生产 CSV：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\training_sets\swine_wiki_training_dataset_production_train_ready_20260514_quality_harden_smoke_v2.csv`

manifest 已同步记录：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\training_sets\training_set_manifest_20260514_quality_harden_smoke_v2.json`

## 字段对齐策略

### 与鸡病模板对齐的字段

保留鸡病生产 CSV 的主字段风格，包括：

- `case_id`
- `index`
- `disease_name`
- `generator_key`
- `generator_model`
- `success`
- `error`
- `species`
- `user_query`
- `diagnosis`
- `prescription`
- `withdrawal_period`
- `metadata`
- 规则判定字段
- 双裁判/仲裁字段
- 最终分数字段

### 猪病链路额外保留字段

为避免信息损失，额外保留：

- `sample_id`
- `plan_id`
- `ability_layer`
- `entity_id`
- `entity_type`
- `risk_class`
- `expected_output_type`
- `export_bucket`
- `export_decision`
- `phase15_final_decision`
- `phase18_semantic_decision`
- `phase18_judge_status`
- `phase18_judge_a_status`
- `phase18_judge_b_status`
- `phase18_arbiter_status`
- `training_intent`
- `evidence_depth_class`
- `page_gold_ready`
- `evidence_units`
- `source_trust`
- `evidence_coverage`
- `evidence_anchor_count`
- 风格质量字段

## 当前结果验证

已完成验证：

1. `phase16_export_layered_training_sets.py` 通过 `py_compile`
2. 重新运行 `Phase16` 成功
3. 生产 CSV 文件已落盘
4. CSV 表头已对齐鸡病模板风格
5. `train_ready` CSV 当前样本数为 20 条

## 防乱码措施

本次 CSV 导出专门采用：

- `utf-8-sig`
- `newline=""`
- 统一 PowerShell UTF-8 环境变量

这样做的原因是：

- 兼容 Windows / Excel 场景
- 降低中文列头和 JSON metadata 被错误解码的概率

## 预计效果

1. 当前猪病链路已经不只是工程中间结果，而是能直接产出“最终生产级 CSV”。
2. 训练侧和汇报侧都可以直接使用 `train_ready` CSV。
3. 历史鸡病、猪病项目之间的交付格式更统一。
4. 当前新增的治理、风格和评估字段也没有丢失，仍然可追溯。
