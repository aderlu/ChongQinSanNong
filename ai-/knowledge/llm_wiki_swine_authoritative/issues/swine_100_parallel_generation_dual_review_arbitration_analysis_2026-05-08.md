# 100 条猪病数据集八路并行生成-双评审-仲裁执行分析 / 2026-05-08

## 运行结论

- 已真实调用模型链路完成 100 条一阶段生成与 Judge A 初评。
- 双评审脚本按一评 pass 候选进入 Judge B，因此实际二评 72 条；其中 71 条触发仲裁。
- 双评审/仲裁后最终通过 50 条，平均分 87.97。
- 严格 train-ready 导出为 0 条，主要原因是当前弱监督链路输出没有标准 source 引用写入答案正文，也没有 `answer_json` 字段。
- 因此，本次产物适合作弱监督候选、评估样本和链路压测；不适合直接作为严格微调训练 JSONL。

## 执行时间

- 一阶段生成 + Judge A 墙钟时间：374.1 秒。
- 二评 + 仲裁墙钟时间：182.7 秒。
- train-ready 导出时间：0.8 秒。
- 全链路墙钟总计：557.6 秒。
- 单条一阶段平均：28.63 秒；P50=28.45 秒；P90=33.2 秒。
- 单条回答生成平均：10.15 秒；Judge A 平均：18.48 秒。
- Judge B 平均：18.89 秒；仲裁平均：None 秒。

## Wiki 参与度

- 100/100 条均记录了 wiki_dir 和 wiki_audit。
- 平均上下文字符数：2197.96。
- 平均可检索 wiki fact count：1595.0；平均 page count：980.0。
- 本次检索用到唯一 evidence source：127 个。
- Top evidence sources: {'SRC-0001': 92, 'RC-WITHDRAWAL-MRL-001': 49, 'RC-DRUG-001': 46, 'SRC-0087': 41, 'SRC-0088': 41, 'RC-DISEASE-REGULATORY-001': 38, 'SRC-0009': 36, 'SRC-0089': 36, 'SRC-0008': 33, 'SRC-0012': 32, 'SRC-0090': 26, 'A0-MOA-573': 22, 'SRC-0037': 15, 'RC-TRAIN-READY-001': 12, 'SRC-0032': 11, 'A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026': 10, 'SRC-0085': 10, 'SRC-0033': 10, 'SRC-0063': 9, 'SRC-0064': 9}

## 质量结果

- 一阶段标签：{'pass': 72, 'reject': 18, 'review': 10}。
- 双评审最终标签：{'pass': 50, 'review': 22}。
- 最终选中标签：{'pass': 50}。
- 一阶段 Judge A 平均分：85.36；范围 65.0 - 95.0。
- 最终选中平均分：87.97；范围 81.0 - 95.0。
- 一阶段无具体剂量条数风险：specific_dose_count=0；specific_withdrawal_count=0。

## Train-ready 门禁

- 输入最终候选：50 + 0 条。
- 通过严格训练导出：0 条。
- 拒绝原因计数：{'too_few_standard_citations': 50, 'missing_answer_json': 50, 'internal_anchor_without_source_id': 24, 'target_disease_alias_not_in_diagnosis': 1, 'fatal_risk': 5, 'score_below_min': 7}。

## 文件

- production_csv: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_164033.csv`
- production_raw_json: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_weak_wiki_production_raw_20260508_164033.json`
- dual_reviewed_csv: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_164033_dual_reviewed_20260508_164705.csv`
- dual_final_csv: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_164033_dual_final100_20260508_164705.csv`
- dual_rejects_csv: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_164033_dual_rejects_20260508_164705.csv`
- dual_raw_json: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260508_164033_dual_review_raw_20260508_164705.json`
- train_ready_jsonl: `D:\XF-ChongQin\ai-\results\swine_qa_dataset\swine_train_ready_20260508_165018.jsonl`
- train_ready_rejects_csv: `D:\XF-ChongQin\ai-\results\swine_qa_dataset\swine_train_ready_rejects_20260508_165018.csv`

## 判断

本次运行有效使用了猪病 LLM wiki 参与生成阶段和 Judge A 阶段：每条样本均有 wiki_audit、wiki_context_chars、wiki_evidence_source_ids 等记录。但现有弱监督脚本没有把 source_id/fact_id/page 标准引用强制写入最终答案字段，导致 train-ready 严格导出全拒。要生产大模型微调数据，应把 V11.1 source-first 约束前移到生成 prompt 和 CSV schema：输出 answer_json、evidence_anchors、must_include、must_not_include，并在答案正文保留至少 3 个标准 source/rule 引用。
