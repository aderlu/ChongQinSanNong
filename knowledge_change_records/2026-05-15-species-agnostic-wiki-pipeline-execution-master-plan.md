# 多物种 Wiki Pipeline 改造执行主控文档

日期：2026-05-15

主控对象：
[2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md)

适用范围：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative`
- `D:\XF-ChongQin\ai-\src\chicken_data_synthesis`

## 一、文档用途

本文件作为“多物种 Wiki 生成与评估链路改造”的执行主控文档，用于：

1. 固定实施顺序
2. 明确每阶段执行项
3. 明确每阶段验收项
4. 记录是否允许进入下一阶段
5. 作为后续逐阶段 change record 的总索引

本文件不是设计草案，而是实施控制文档。后续任何实际改造都应以本文件阶段顺序和验收门槛为准。

## 二、执行总原则

### 1. 阶段顺序不可跳

必须严格按以下顺序执行：

1. Phase A：基线冻结与实施准备
2. Phase B：契约层与兼容层落地
3. Phase C：chicken runtime 五件套生成
4. Phase D：生成链 species-aware 化
5. Phase E1：事实评估与导出 species-aware 化
6. Phase E2：双裁判、仲裁与 baseline runner species-aware 化
7. Phase F：全链路回归与小批量验证

任何阶段未完成验收，不允许进入下一阶段。

### 2. 每阶段必须同时做三类验收

每阶段结束时必须完成：

1. 代码结构验收
2. 数据产物验收
3. 回归验收

### 3. 默认先保 swine，再扩展 chicken

所有改造先保证：

1. 不破坏 `swine` 默认行为
2. 不破坏 `2026-05-14` baseline 口径
3. 不破坏 `54` 字段 comparison CSV 契约

然后再让 `chicken` 保守接入。

### 4. 关键冻结项不得在中途漂移

以下内容在第一阶段完成前后都必须冻结：

1. `baseline_validation_common.py` 的 `54` 字段定义
2. `swine` 默认入口行为
3. baseline runner 默认链路顺序：
   `Phase 14 -> Phase 14b -> Phase 15 -> Phase 18`
4. 旧入口兼容性要求

### 5. 每阶段必须新增一份 change record

每阶段结束后，必须在 `knowledge_change_records` 下新增一份记录文档，记录：

1. 修改背景
2. 修改文件
3. 新增文件
4. 删除或迁移内容
5. 验证命令
6. 验证结果
7. 剩余风险
8. 是否允许进入下一阶段

## 三、阶段主控总表

| 阶段 | 目标 | 是否完成 | 是否通过验收 | 是否允许进入下一阶段 |
| --- | --- | --- | --- | --- |
| Phase A | 基线冻结与实施准备 | [x] | [x] | [x] |
| Phase B | 契约层与兼容层落地 | [x] | [x] | [x] |
| Phase C | chicken runtime 五件套生成 | [x] | [x] | [x] |
| Phase D | 生成链 species-aware 化 | [ ] | [ ] | [ ] |
| Phase E1 | 事实评估与导出 species-aware 化 | [ ] | [ ] | [ ] |
| Phase E2 | 双裁判、仲裁与 baseline runner species-aware 化 | [ ] | [ ] | [ ] |
| Phase F | 全链路回归与小批量验证 | [ ] | [ ] | [ ] |

## 四、Phase A：基线冻结与实施准备

### 目标

在不修改业务逻辑的前提下，冻结当前系统基线、依赖关系、字段口径和真实执行链路。

### 执行项

- [x] 盘点当前 swine 全链路真实入口、输入输出文件、字段定义、默认命名
- [x] 盘点 chicken 现有 exports、缺失文件、可复用能力
- [x] 盘点 `chicken_data_synthesis` 可复用边界
- [x] 冻结 `54` 字段定义
- [x] 冻结 baseline runner 默认链路顺序
- [x] 明确 `Phase 14b` 是正式主链路步骤
- [x] 生成 inventory 文档
- [x] 生成 machine-readable inventory JSON
- [x] 建立本次迁移总控 change record

### 强制检查点

- [x] 明确记录 `baseline_validation_common.py` 是 `54` 字段公共契约层
- [x] 明确记录 `run_baseline_experiment.py` 当前真实串联关系
- [x] 明确记录 `phase14b_naturalize_grounded_answers.py` 当前在默认链路中存在
- [x] 明确记录 `chicken_data_synthesis` 中可复用与不可直接复用模块

### 验收标准

- [x] 未修改任何业务逻辑代码
- [x] 形成 inventory 文档
- [x] 形成 inventory JSON
- [x] 形成基线字段冻结说明
- [x] `swine` 最小 smoke 运行成功一次
- [x] 记录当前关键输入输出路径与样本产物

### 阶段输出

- [x] `knowledge_change_records/YYYY-MM-DD-species-agnostic-phaseA-inventory.md`
- [x] machine-readable inventory JSON

### 是否允许进入下一阶段

- [x] 允许

## 五、Phase B：契约层与兼容层落地

### 目标

先搭建 species-aware 公共契约层与 orchestration 兼容层，不先改写核心生成行为。

### 执行项

- [x] 新增 `species_config.py`
- [x] 新增 `manifest_contract.py`
- [x] 新增 `path_context.py`
- [x] 新增 `runtime_indexes.py`
- [x] 新增 `model_routing.py`
- [x] 新增 baseline orchestration compatibility 层
- [x] 新增 `swine.yaml`
- [x] 新增 `chicken.yaml`
- [x] 旧入口支持 `--species`
- [x] 旧入口支持 `--species-config`
- [x] 旧入口支持 `--wiki-root`
- [x] 默认 `--species swine`

### 强制检查点

- [x] `swine_runtime_selection` 可被统一映射到 `model_routing`
- [x] baseline runner 能记录 species、入口映射和 run manifest
- [x] 不改动当前 `54` 字段定义
- [x] 不改变旧命令默认行为

### 验收标准

- [x] 旧命令不传参仍可运行
- [x] `--species swine` 与旧行为一致
- [x] `model_routing` 能兼容旧 `swine` 配置键
- [x] runner 识别 species、旧入口、新入口
- [x] `54` 字段常量未变化
- [x] 所有新增契约层有基础测试

### 建议测试

- [x] `tests/test_species_config_loader.py`
- [x] `tests/test_baseline_field_contract.py`
- [x] legacy entrypoint compatibility test

### 阶段输出

- [x] `knowledge_change_records/YYYY-MM-DD-species-agnostic-phaseB-contracts-and-compat.md`

### 是否允许进入下一阶段

- [x] 允许

## 六、Phase C：chicken runtime 五件套生成

### 目标

让 chicken 在不重写 wiki 页面、不调用 LLM 的前提下具备运行所需输入契约。

### 执行项

- [x] 实现或扩展 `build_runtime_manifest.py`
- [x] 生成 `runtime_core_manifest.json`
- [x] 生成 `runtime_exclude_patterns.json`
- [x] 生成 `gold_dataset_readiness_index.csv`
- [x] 生成 `drug_gold_role_index.csv`
- [x] 生成 `exporter_hard_block_rules.json`
- [x] 输出 `runtime_manifest_validation_report.md`
- [x] 对缺失字段做显式保守降级

### 强制检查点

- [x] 不调用 LLM
- [x] 不允许缺失字段静默留空
- [x] 药物、休药期、食品安全相关记录默认保守
- [x] validation report 明确展示保守降级比例

### 验收标准

- [x] chicken exports 下出现完整五件套
- [x] 每条记录有明确 `task_use_status`
- [x] 高风险记录不会错误进入正向可生成状态
- [x] 索引生成在断网条件下可运行
- [x] validation report 明确统计：
  `generation_ready_limited`
  `retrieval_only`
  `boundary_only`
  `blocked`

### 建议测试

- [x] `tests/test_manifest_contract_mapping.py`
- [x] `tests/test_runtime_index_generation.py`

### 阶段输出

- [x] `knowledge_change_records/YYYY-MM-DD-species-agnostic-phaseC-chicken-runtime-indexes.md`

### 是否允许进入下一阶段

- [x] 允许

## 七、Phase D：生成链 species-aware 化

### 目标

将 case variables、Phase 12、13、14、14b 改造为 species-aware，同时不破坏 swine 默认生成质量。

### 执行项

- [ ] 改造 `consultation_case_variables.py`
- [ ] 主字段统一为 `production_stage`
- [ ] 保留 `pig_stage` 作为 swine 兼容字段
- [ ] 改造 Phase 12
- [ ] 改造 Phase 13
- [ ] 改造 Phase 14
- [ ] 改造 Phase 14b
- [ ] species prompt pack 接入生成链
- [ ] species prompt pack 接入自然化链
- [ ] runner 显式记录 `14 -> 14b -> 15` 顺序

### 强制检查点

- [ ] chicken 样本中不得出现猪病术语污染
- [ ] `Phase 14b` 必须纳入 run manifest
- [ ] `Phase 14b` 新旧入口都必须可解释对齐
- [ ] swine 默认生成效果不得明显退化

### 验收标准

- [ ] `swine` 生成 smoke 不退化
- [ ] `chicken` 生成样本自然、无猪病污染
- [ ] `Phase 14b` 旧入口仍可跑
- [ ] `Phase 14b` 新入口输出一致或差异可解释
- [ ] chicken 至少完成 `30` 条 smoke
- [ ] run manifest 明确记录 Phase 14b 是否执行、输入输出文件、species、prompt pack 版本

### 建议测试

- [ ] `tests/test_multispecies_case_variables.py`
- [ ] `tests/test_phase14b_species_naturalization.py`

### 阶段输出

- [ ] `knowledge_change_records/YYYY-MM-DD-species-agnostic-phaseD-generation-chain.md`

### 是否允许进入下一阶段

- [ ] 允许

## 八、Phase E1：事实评估与导出 species-aware 化

### 目标

先稳定事实门控与训练集导出层，不在此阶段同时处理双裁判复杂逻辑。

### 执行项

- [ ] 改造 Phase 15
- [ ] 改造 Phase 16
- [ ] 由 species 配置驱动 `case_id namespace`
- [ ] 由 species 配置驱动 `species`
- [ ] 由 species 配置驱动输出前缀
- [ ] 由 species 配置驱动 metadata
- [ ] 比较表仍固定 `54` 字段

### 强制检查点

- [ ] `swine` 文件名与字段保持兼容
- [ ] `chicken` 导出中不得出现 `swine-wiki-*`
- [ ] 运行追踪只写入 run manifest，不写入 comparison CSV

### 验收标准

- [ ] `swine` 导出兼容
- [ ] `chicken` 导出 namespace 正确
- [ ] `chicken` 导出 `species` 正确
- [ ] `54` 字段数量与字段名不变
- [ ] run manifest 记录 species、模型、输入输出路径

### 建议测试

- [ ] `tests/test_phase16_species_export.py`

### 阶段输出

- [ ] `knowledge_change_records/YYYY-MM-DD-species-agnostic-phaseE1-fact-eval-and-export.md`

### 是否允许进入下一阶段

- [ ] 允许

## 九、Phase E2：双裁判、仲裁与 baseline runner species-aware 化

### 目标

最后处理最复杂、最容易破坏基线的裁判链与 baseline orchestration。

### 执行项

- [ ] 改造 Phase 18
- [ ] 接入 `ModelRoutingContract`
- [ ] 接入 `JudgeRubric`
- [ ] `swine_runtime_selection` 迁移到统一 `model_routing`
- [ ] 保留 swine adapter 对旧键兼容
- [ ] 冻结并测试 `baseline_validation_common.py`
- [ ] 改造 `build_case_seeds.py`
- [ ] 改造 `generate_baseline_groups.py`
- [ ] 改造 `judge_general_consultation.py`
- [ ] 改造 `audit_grounding.py`
- [ ] 改造 `compare_groups.py`
- [ ] 改造 `run_baseline_experiment.py`
- [ ] runner 显式串联：
  `Phase 14 -> Phase 14b -> Phase 15 -> Phase 18 -> compare/export`

### 强制检查点

- [ ] 模型路由失败时必须明确报错
- [ ] 不允许静默 fallback 到 swine judge
- [ ] `STANDARD_SAMPLE_FIELDS` 不变
- [ ] `STANDARD_COMPARISON_FIELDS` 仍为 `54` 字段

### 验收标准

- [ ] `swine` 三组 baseline 可复现
- [ ] `chicken` 三组 baseline 可产出
- [ ] `Phase 18` 不再依赖单一 `swine_runtime_selection` 键名
- [ ] `baseline_validation_common.py` 有独立契约测试
- [ ] `54` 字段口径稳定
- [ ] runner 默认顺序未绕过 `Phase 14b`

### 建议测试

- [ ] `tests/test_swine_wiki_baseline_validation.py`
- [ ] baseline contract tests for `baseline_validation_common.py`

### 阶段输出

- [ ] `knowledge_change_records/YYYY-MM-DD-species-agnostic-phaseE2-judge-and-baseline.md`

### 是否允许进入下一阶段

- [ ] 允许

## 十、Phase F：全链路回归与小批量验证

### 目标

确认整个改造不是“代码能跑”，而是“修改有效、质量受控、目标达成”。

### 执行项

- [ ] `swine` 全链路回归
- [ ] `chicken` 全链路真实 smoke
- [ ] `chicken` 质量 smoke
- [ ] 如资源允许，执行 `chicken` 小批量验证
- [ ] 汇总所有阶段验证结果

### 强制检查点

- [ ] `swine` 对齐 `2026-05-14` 基线
- [ ] `chicken` 无猪病术语污染
- [ ] `54` 字段完整率必须 `100%`
- [ ] 高风险边界必须保守

### 验收标准

- [ ] `swine` 与既有验收基准一致
- [ ] `chicken` 至少完成 `5` 条真实 LLM 全链路 smoke
- [ ] `chicken` 完成 `30` 条质量 smoke
- [ ] `Phase 14b` 包含在 chicken 默认链路中
- [ ] comparison CSV `54` 字段完整率 `100%`
- [ ] 第一阶段只要求 chicken 结果“可审查、无猪病污染、边界保守”，不要求达到 swine 成熟质量

### 阶段输出

- [ ] `knowledge_change_records/YYYY-MM-DD-species-agnostic-phaseF-regression-and-smoke.md`
- [ ] 最终总结文档

### 是否允许判定项目第一阶段完成

- [ ] 允许

## 十一、每阶段统一验收模板

每个阶段的阶段记录文档必须包含以下固定模板：

### 1. 背景

- 本阶段为什么做

### 2. 修改前状态

- 修改前代码/数据/入口状态是什么

### 3. 本阶段修改内容

- 修改了哪些文件
- 新增了哪些文件
- 删除或迁移了哪些内容

### 4. 验证命令

- 列出所有执行过的验证命令

### 5. 验证结果

- 通过项
- 未通过项
- 差异说明

### 6. 风险与未完成项

- 还剩哪些风险
- 为什么当前仍允许进入下一阶段，或为什么不允许

### 7. 结论

- 是否通过本阶段验收
- 是否允许进入下一阶段

## 十二、开工前最终检查

正式开始执行前，必须再勾选以下三项：

- [ ] 已确认本主控文档是当前唯一实施顺序依据
- [ ] 已确认 `54` 字段口径冻结
- [ ] 已确认 `Phase 14b` 和 `baseline_validation_common.py` 均纳入正式改造范围

## 十三、最终完成判定

当且仅当以下条件同时满足，才可判定本轮第一阶段改造完成：

- [ ] swine 默认命令、默认路径、默认 baseline 行为未被破坏
- [ ] chicken runtime 五件套完整生成
- [ ] chicken 至少完成 `5` 条真实全链路 smoke
- [ ] chicken 至少完成 `30` 条质量 smoke
- [ ] `54` 字段 comparison CSV 契约稳定
- [ ] `Phase 14b` 已纳入默认主链路
- [ ] `baseline_validation_common.py` 已冻结并有测试保护
- [ ] model routing 已脱离单一 `swine_runtime_selection`
- [ ] baseline runner 已支持 species-aware orchestration
- [ ] 所有阶段均有对应 change record
