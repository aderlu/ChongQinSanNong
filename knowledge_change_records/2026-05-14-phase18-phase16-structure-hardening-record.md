# 2026-05-14 Phase18/Phase16 结构硬化修复记录

## 1. 本次修改目标

修复裁判/仲裁输出结构和 CSV 准入链路中的三类问题：

1. `main_issues`、`hard_fail_codes` 等字段被误当作字符串迭代，导致单字符拆分。
2. Phase18 仍然过度信任模型返回的 `sft_admission`，会把 `repairable` 误放进 `main_sft`。
3. Phase16 导出只看准入字符串，不足以拦截零分但非无效、标签与分数冲突等结构异常样本。

## 2. 修改前的问题

### 2.1 字段结构不稳定

Phase18 的归一化逻辑直接对 `main_issues`、`hard_fail_codes` 做 `list(...)` 处理。  
如果模型返回的是字符串，就会被拆成字符列表，造成后续 CSV 字段污染。

### 2.2 准入判断信任模型输出

Phase18/Phase16 之前允许模型直接返回 `sft_admission`，本地规则只是补充。  
这会导致语义上已经判为 `repairable` 的样本，仍被导入 `main_sft`。

### 2.3 异常分数样本缺少硬约束

存在总分为 0、所有维度为 0、或标签与分数明显冲突的样本，但导出层没有强制降级到 review。

## 3. 本次修改内容

### 3.1 Phase18 增加字符串列表归一化

新增 `normalize_string_list()`，统一处理：

- `list`
- `tuple`
- 单字符串
- 空值

并将 `hard_fail_flags`、`hard_fail_codes`、`main_issues` 等字段全部改为安全归一化输出。

### 3.2 Phase18 重新计算准入

Phase18 不再直接采用模型返回的 `sft_admission`，而是按本地规则重新计算：

- `high_quality_valid` -> `main_sft`
- `valid` -> `low_weight_sft`
- `repairable` -> `repair_queue`
- `invalid` -> `reject_queue`

同时新增结构失败标记：

- `zero_score_non_invalid`
- `all_dimensions_zero`
- `label_score_conflict`

一旦命中，就强制降级到 `repair_queue`。

### 3.3 Phase16 增加二次硬约束

导出层新增收口：

- 只有 `final_label=high_quality_valid` 且 `sft_admission=main_sft` 才能进入主 accepted。
- 只有 `final_label=valid` 且 `sft_admission=low_weight_sft` 才能进入 accepted。
- `repairable` 和结构失败样本统一进入 `review`。

## 4. 为什么这样能解决问题

1. 归一化修复了单字符拆分，避免结构字段污染 CSV。
2. 准入重算把最终控制权收回到本地规则，避免模型自相矛盾输出直接穿透。
3. 导出二次硬约束可阻断零分样本、结构失败样本进入训练集。

## 5. 预期效果

- `repairable -> main_sft` 现象消失。
- `main_issues` 不再出现字符拆分。
- `zero_score_non_invalid` 样本不会进入 train-ready。
- CSV 的语义一致性更高，审计留痕更清楚。

## 6. 验收标准

- `repairable_main_sft_count = 0`
- `main_issues_char_split_count = 0`
- `zero_score_non_invalid_count = 0`
- `label_score_conflict_count = 0`

