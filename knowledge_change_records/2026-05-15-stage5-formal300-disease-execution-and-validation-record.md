# 2026-05-15 300条疾病问诊正式批次执行与验收留痕

## 执行目标

按照八路并行方式生成 300 条真实猪病问诊数据，随后对最终 CSV 进行完整检查，评估：

- 数据是否有效。
- 覆盖是否完整。
- 是否尽可能覆盖完整病例。

## 执行链路

1. Phase12 规划样本。
2. Phase13 构建回答骨架。
3. Phase14 八路并发真实 API 生成。
4. Phase14b 自然化与审计清洗。
5. Phase15 确定性事实与硬门禁评估。
6. Phase18 双裁判与仲裁。
7. Phase16 导出最终 CSV。

## 本次正式批次

- 批次标识：`20260514_stage5_formal300_disease_v2`
- Phase12 计划数：300
- 生成模式：真实 API
- 并发数：8
- 目标范围：disease / positive_sft / substantive

## 关键结果

### Phase12

- 300 条计划全部为 disease。
- 300 条全部为 positive_sft。
- 300 条全部为 substantive evidence。
- 覆盖 43 个可生成的 substantive 疾病页面。

### Phase13

- 300 条骨架全部生成。
- 无 evidence gap。

### Phase14

- 300 条全部生成成功。
- fallback 样本 3 条。
- API 重试分布最高到 7 次，说明高可用 key 池在工作，但仍有少量不稳定调用。
- 耗时约 15 分 32 秒。

### Phase14b

- 300 条全部通过自然化。
- 未发现需要重写的审计痕迹样本。

### Phase15

- 238 条通过。
- 62 条拒绝。
- 主要拒绝原因：`executive_content_missing_a0_source`。

### Phase18

- 238 条进入双裁判。
- 225 条 accepted。
- 12 条 review。
- 63 条 rejected。
- 触发仲裁 66 条。
- 耗时约 21 分 44 秒。

### Phase16

最终导出结果：

- `swine_wiki_training_dataset_production_20260514_stage5_formal300_disease_v2.csv`：300 行
- `swine_wiki_training_dataset_production_train_ready_20260514_stage5_formal300_disease_v2.csv`：225 行
- `swine_wiki_training_main_20260514_stage5_formal300_disease_v2.csv`：300 行
- `swine_wiki_training_main_train_ready_20260514_stage5_formal300_disease_v2.csv`：225 行

## 覆盖与重复性检查

- 最终 300 条样本覆盖 43 个 disease/entity。
- exact `user_query + assistant_answer` 组合未发现重复组。
- 每个疾病最多分配 8 条样本，说明扩展主要通过同病不同问诊变体完成，而不是靠重复粘贴。

## 有效性判断

### 可以确认的部分

- 产线能够稳定跑完 300 条正式批次。
- 生成、自然化、事实门禁、双裁判、仲裁、导出链路均可执行。
- 最终 train-ready CSV 只保留了高质量可训练样本。

### 仍然存在的边界

- 当前 300 条只覆盖到 43 个可生成的 substantive 疾病页面，尚未覆盖 wiki 中全部疾病页面。
- Phase15/18 的门禁会明显压缩最终可训练样本数量，这对质量是必要的，但会限制规模转化率。
- 少量样本仍需 review，说明仲裁层在边界样本上仍保留人工复核价值。

## 瓶颈观察

- 主要耗时在 Phase14 真实 API 生成与 Phase18 双裁判/仲裁。
- Phase15 非瓶颈，执行快但过滤强。
- 影响覆盖完整性的主要因素不是并发数，而是可用 substantive disease 页面总量。

## 结论

本批次可以确认：

1. 系统支撑八路并行生成 300 条。
2. 最终 CSV 可用，且 train-ready 部分质量较稳。
3. 但它并不能说明已经覆盖了 wiki 中全部猪病病例。
4. 若目标是更完整病例覆盖，下一步仍需继续补强 partial / thin / toc_only 页面，或引入更多高价值疾病页面证据。
