# 多物种 Wiki Pipeline 方案按审查文档二次修订记录

日期：2026-05-15

关联文档：

- 主方案：`D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md`
- 审查文档：`D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan-review.md`

## 一、修改背景

用户提供了正式审查文档，指出主方案方向正确，但仍存在执行设计偏理想化的问题，尤其是：

1. 低估 swine pipeline 的深度耦合。
2. 低估 baseline runner orchestration 的兼容成本。
3. 忽略仓库中已存在的 `ai-\src\chicken_data_synthesis` 应用层框架。
4. model selection / judge routing 抽象顺序偏后。
5. 对 chicken 第一阶段质量预期偏乐观。

本次修订基于该审查文档，对主方案做进一步收紧和优化。

## 二、之前存在的问题

### 1. 缺少架构合流决策

原主方案没有明确 swine pipeline 与 `chicken_data_synthesis` 的关系，存在重复建设第二套 chicken runtime 的风险。

### 2. Model Routing 前置不足

原主方案虽然提到 Phase 18 要配置化，但没有把 model selection contract 前置到基础契约阶段。

### 3. Baseline Orchestration 前置不足

原主方案要求旧入口 wrapper，但没有明确 baseline runner 必须先能识别旧入口、新入口、species、run manifest 和 54 字段口径。

### 4. Chicken 质量目标过宽

原主方案容易让人理解为 chicken 接入后可以立即与 swine 同等级产出。审查文档指出这不现实，应先以保守 smoke 闭环为目标。

## 三、本次修改了什么

本次修订了主方案：

- `D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md`

并新增本留痕记录：

- `D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-plan-review-driven-revision-record.md`

## 四、具体修订内容

### 1. 新增“架构决策”章节

明确：

- 仓库已有 `D:\XF-ChongQin\ai-\src\chicken_data_synthesis`。
- 短期以 swine wiki-grounded pipeline 为执行主干。
- chicken 通过 adapter 进入最小闭环。
- 优先复用 chicken_data_synthesis 里的 LLM runtime、model fallback、judge normalization、persistence 和应用层组织能力。
- 长期再评估公共 runtime 与 chicken_data_synthesis 合流。

### 2. 新增“第一阶段质量边界”

明确第一阶段目标是：

- 可复用。
- 可运行。
- 不破坏 swine。
- chicken 保守接入。

不承诺：

- chicken 500 条结果立即达到 swine 成熟质量。
- chicken 药物正向处方比例与 swine 对齐。
- chicken judge rubric 一次性充分校准。
- adapter 自动弥补原始 Wiki 字段成熟度不足。

### 3. 新增 ModelRoutingContract

将 model selection / judge routing 前置为基础契约，要求统一解析：

- generator
- judge_a
- judge_b
- arbiter
- baseline_judge
- fallback chain
- 并发、超时和模型成本信息

并要求 swine 旧 `swine_runtime_selection` 只作为兼容输入，不能继续作为唯一模型路由契约。

### 4. Baseline Orchestration 前置

在目标架构和 Phase B 中新增 orchestration compatibility 层，要求在底层 phase 重命名前先具备：

- 旧入口/新入口映射。
- species 参数透传。
- run manifest 记录。
- 54 字段校验。
- swine 原路径与 chicken 隔离路径策略。

### 5. 重排实施顺序

将原 Phase 0-7 调整为：

1. Phase A：冻结基线、依赖图和架构决策。
2. Phase B：抽出基础契约与 orchestration 兼容层。
3. Phase C：鸡病运行索引生成器。
4. Phase D：生成链 species-aware 化。
5. Phase E：评估、导出、裁判和 baseline orchestration species-aware 化。
6. Phase F：猪病回归、鸡病 smoke、小批量验证。

### 6. 修订验收标准

新增：

- model selection 不再依赖 `swine_runtime_selection` 单一键名。
- baseline runner 在底层 phase 重命名前已经具备旧/新入口映射和 species-aware orchestration。
- chicken validation report 必须报告保守降级比例。
- 第一阶段 chicken 质量验收以真实 smoke 可审查、无猪病污染、边界保守为准。

## 五、修改后解决了什么

本次修订后，主方案进一步从“架构可行”变为“执行顺序更稳妥”：

- 避免重复建设 chicken runtime。
- 避免后期才发现 judge/model routing 卡住。
- 避免底层文件先重命名导致 baseline runner 失效。
- 避免将 chicken 的结构可运行误判为质量成熟。
- 更符合“先不破坏 swine，再保守接入 chicken”的现实节奏。

## 六、预计效果

执行修订后的方案，第一阶段预期结果应收敛为：

- swine 默认流程不退化。
- 54 字段 comparison CSV 不变。
- chicken 能生成 runtime 五件套。
- chicken 能完成至少 5 条真实 LLM smoke。
- chicken 结果无猪病术语污染。
- 高风险内容保守边界明确。
- 后续再通过小批量验证推进质量提升，而不是一次性承诺 swine 同级成熟度。

## 七、未解决风险

1. `chicken_data_synthesis` 与 swine pipeline 的最终合并方式仍需在 Phase A inventory 中具体决策。
2. chicken 原始 Wiki 的证据成熟度不足，仍可能限制可正向生成样本比例。
3. model routing 与现有 config.json、chicken 应用层配置之间的映射需要在代码阶段验证。
4. baseline runner 兼容层需要重点测试，避免旧入口和新入口同时存在时出现路径混乱。
