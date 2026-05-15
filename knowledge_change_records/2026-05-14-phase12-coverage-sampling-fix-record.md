# 2026-05-14 Phase12 覆盖抽样修复记录

## 1. 本次修改目标

修复 Phase12 规划阶段的两个问题：

1. 正式批次仍以简单 `limit` 截断，容易把前几个疾病反复抽到。
2. 计划摘要缺少覆盖和深度指标，无法在规划阶段发现抽样失衡。

## 2. 修改前的问题

### 2.1 抽样方式过于机械

Phase12 之前只是在最后对 `plans[:limit]` 截断。  
这会让前序实体和前序页面占满批次，导致 40 条样本覆盖面很窄。

### 2.2 没有覆盖导向选择

虽然已经有 `evidence_depth_class`，但没有在抽样阶段明确：

- 优先 substantive
- 限制每个实体重复数
- 在正式批次中避免 TOC-only 过量

### 2.3 缺少可验收的覆盖统计

如果不输出 unique entity / unique page / depth ratio，后面只能等生成完毕才发现重复。

## 3. 本次修改内容

### 3.1 新增 coverage 抽样模式

新增 CLI 参数：

- `--sampling-mode default|coverage`
- `--max-plans-per-entity`
- `--prefer-depth`

在 `coverage` 模式下：

- 先按证据深度排序
- 再按实体限额选取
- 再回填剩余名额

### 3.2 新增覆盖统计

Phase12 报告新增：

- `unique_entities_planned`
- `unique_pages_planned`
- `max_samples_per_entity`
- `substantive_plan_ratio`
- `toc_only_plan_ratio`
- `coverage_*` 验收项

### 3.3 保持默认行为兼容

默认仍保留原有 `limit` 行为，避免影响已有脚本。  
只有显式启用 `coverage` 才切换到新抽样模式。

## 4. 为什么这样能解决问题

1. coverage 模式把“多样性”前移到规划阶段，而不是指望生成模型随机分散。
2. 实体限额能直接压低重复率。
3. 深度优先抽样能提升正式批次中的 substantive 占比。
4. 报告字段让问题在 Phase12 就可见，不必等到 CSV 导出后再回头排查。

## 5. 预期效果

- 40 条正式批次不再集中在少数疾病。
- 单实体重复数下降。
- substantive 占比提升。
- TOC-only 不再主导正式正样本。

## 6. 验收标准

- `unique_entities_planned >= 30`
- `unique_pages_planned >= 30`
- `max_samples_per_entity <= 2`
- `substantive_plan_ratio >= 0.6`
- `toc_only_plan_ratio <= 0.1`

