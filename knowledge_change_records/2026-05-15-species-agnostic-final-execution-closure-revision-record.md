# 多物种 Wiki Pipeline 可执行版收口修订记录

日期：2026-05-15

关联文档：

- `D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md`

## 一、修改背景

用户进一步指出主方案仍有四个执行关键点缺口：

1. 漏掉真实链路中的 `phase14b_naturalize_grounded_answers.py` 自然化步骤。
2. baseline orchestration 前置了，但缺少对 `baseline_validation_common.py` 公共字段定义层的显式改造承诺。
3. `chicken_data_synthesis` 复用方向正确，但缺少复用边界和接口对齐清单。
4. Phase E 同时承载 Phase 15、16、18 和 baseline orchestration，风险集中度偏高。

本次修订目标是把主方案从“基本合理”进一步收口到“可以执行”。

## 二、之前存在的问题

### 1. Phase 14b 缺失

当前真实链路中，生成后并不是直接从 Phase 14 进入 Phase 15，而是存在 `phase14b_naturalize_grounded_answers.py` 自然化步骤。如果不把 Phase 14b 纳入 species-aware 改造和验收，文档链路会闭环，但实际执行会断链。

### 2. 54 字段公共合同层缺失

54 字段不是只由 runner 校验，而是由 `baseline_validation_common.py` 中的字段常量统一定义。若只改 runner，不改公共字段定义层，species-aware 字段透传和 54 字段冻结之间仍可能脱节。

### 3. Chicken_Data_Synthesis 复用边界不清

主方案此前只说优先复用 `chicken_data_synthesis`，但没有说明复用哪些能力、不复用哪些能力。由于该应用层自身可能存在旧命名或业务路径残留，如果无边界吸收，仍可能导致双轨实现或命名污染。

### 4. Phase E 风险集中

Phase 15、Phase 16、Phase 18 和 baseline runner 都有真实硬编码和路径耦合。如果都放在同一个 Phase E 中执行，联调风险偏高。

## 三、本次修改内容

### 1. Phase 14b 纳入正式链路

主方案已更新：

- 当前结论中加入 Phase 14b。
- Phase D 改为覆盖 Phase 12、13、14、14b。
- 新增 `phase14b_naturalize_grounded_answers.py` -> `naturalize_grounded_answers.py` 的命名迁移建议。
- 明确默认链路顺序为 Phase 14 -> Phase 14b -> Phase 15。
- run manifest 必须记录 Phase 14b 是否执行、输入、输出、species 和 prompt pack 版本。

### 2. Baseline 字段合同层纳入改造

主方案已更新：

- 明确 `baseline_validation_common.py` 是 54 字段公共合同层。
- 将其加入优先改造文件清单。
- 新增 `tests/test_baseline_field_contract.py`。
- 验收标准要求独立测试保护 51 + 3 字段口径。

### 3. Chicken_Data_Synthesis 复用边界清单

主方案已新增：

- `Chicken_Data_Synthesis 复用边界清单`

第一阶段优先复用：

- `infrastructure.llm`
- `application.services.review`
- `infrastructure.evaluation`
- `application.services.task_planning` 的模型解析经验
- `infrastructure.persistence` 的快照设计经验
- `interfaces.cli` 的 CLI 组织方式作为未来参考

第一阶段不直接复用：

- chicken 现有输出路径、文件名前缀、benchmark/runtime 命名中仍有旧业务语义的部分。
- chicken 既有数据合成主流程作为多物种 Wiki pipeline 主入口。
- chicken 现有业务字段作为 54 字段 baseline 合同的替代品。
- 未经审查的持久化目录命名、benchmark 命名、旧 dataset prefix。

### 4. Phase E 拆分

主方案已将 Phase E 拆成：

- Phase E1：事实评估与导出 species-aware 化。
- Phase E2：裁判、仲裁和 baseline orchestration species-aware 化。

这样可以先解决 Phase 15/16 的事实评估和导出污染，再进入 Phase 18 和 baseline orchestration，降低联调风险。

## 四、修改后解决了什么

本轮修订解决了最后一批执行断点：

1. 默认真实链路不会跳过 Phase 14b。
2. 54 字段口径有公共字段定义层保护。
3. `chicken_data_synthesis` 的复用有边界，不会无控制吸收旧命名或旧输出路径。
4. Phase E 风险被拆分，执行顺序更稳。

## 五、预计效果

修订后主方案更适合作为实施依据：

- swine 不退化的保护更完整。
- chicken 最小 smoke 闭环链路更贴近真实执行。
- baseline 54 字段不容易在改造中漂移。
- 文件重命名、自然化、裁判、baseline orchestration 的顺序更可控。

## 六、后续执行注意事项

正式代码修改时必须优先执行：

1. `baseline_validation_common.py` 字段合同测试。
2. Phase 14b 旧入口与新入口兼容测试。
3. runner 默认链路顺序检查。
4. `chicken_data_synthesis` 复用边界 inventory。

未完成这些检查前，不应启动大规模文件重命名或 500 条数据生成。
