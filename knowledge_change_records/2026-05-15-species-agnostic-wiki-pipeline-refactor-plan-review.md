# 多物种 Wiki Pipeline 改造方案审查文档

日期：2026-05-15

被审查文档：
`D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md`

## 一、审查结论

该方案整体方向正确，抓住了当前问题主轴：

1. 现有 swine pipeline 与物种强绑定，无法直接复用于 chicken 或后续新 Wiki。
2. chicken 侧缺少完整 runtime/gold/eval/hard-block 配套文件，不能直接跑通现有全链路。
3. 54 字段 baseline 比较口径已被现有系统严格依赖，不能随意改动。

但按当前文档写法，不建议直接执行。原因不是方向错误，而是：

1. 低估了现有 swine pipeline 的深度耦合程度。
2. 低估了 baseline runner 的兼容性改造复杂度。
3. 忽略了仓库内已存在的 `chicken_data_synthesis` 应用层框架，存在重复建设风险。
4. 对 model selection / judge routing 的改造顺序安排偏后。

综合判断：

- 可执行性：中等偏低，修正后可提升到中高
- 有效性：方向有效，但第一阶段只能保证“可复用、可运行、不破坏 swine”，不能默认承诺 chicken 立即达到与 swine 同级的数据质量

## 二、有效性评估

这份方案在目标层面是有效的，原因如下：

1. 它正确识别了真正的抽象边界：`species config`、`manifest contract`、`prompt pack`、`judge rubric`、`adapter`。
2. 它明确强调保留 swine 默认行为、旧入口兼容、baseline 口径不变，这与当前仓库的稳定性要求一致。
3. 它没有试图在第一阶段同时完成大规模目录迁移和逻辑迁移，方向上是稳妥的。
4. 它正确要求 chicken 在接入前先补齐 runtime 五件套，而不是直接套跑 swine 脚本。

但它的有效性存在边界：

1. 第一阶段更现实的结果是“chicken 可保守接入并完成 smoke”，而不是“立即得到与 swine 同等级的产出质量”。
2. `ManifestAdapter` 能解决结构兼容问题，但不能自动弥补 chicken 原始字段成熟度不足的问题。
3. 如果不先解决 model routing 和 baseline orchestration 的兼容问题，后续 phases 即使逻辑正确，也会在系统联调时失效。

## 三、当前文档的主要问题

### 1. 低估 swine pipeline 的深度物种绑定

当前耦合并不只是变量名或路径名层面，而是贯穿：

1. case variables
2. 问题模板
3. 生成场景
4. 导出 namespace
5. judge model routing
6. 风险边界正则与裁判逻辑

这意味着该改造不是“加 `--species` 参数”级别，而是跨计划、生成、评估、导出、裁判、baseline runner 的全链路重构。

### 2. 低估 baseline runner 改造成本

当前 baseline runner 直接串联旧脚本文件名、旧输出路径和固定 54 字段校验口径。

如果底层 phase 重命名、路径变更、字段透传变化，而 orchestration 层没有先兼容，baseline runner 会最先失效。因此“保 wrapper”还不够，必须把 runner 的兼容解析层前置。

### 3. 忽略了 chicken 侧已有应用层框架

仓库中已存在 `ai-\src\chicken_data_synthesis` 体系，说明 chicken 并非完全空白。

因此当前文档缺少一项关键架构决策：

1. 以 swine pipeline 为主干吸收 chicken
2. 还是以 chicken 的应用层 runtime 为主干，承接 swine 的 wiki-first 能力

如果不先明确，后续很容易形成两套并行的 species-aware runtime。

### 4. model selection / judge routing 处理顺序偏后

当前 Phase 18 依赖 `swine_runtime_selection` 和 `judge_swine_*` 配置键。

如果只先抽 prompt 和 rubric，而不提前抽象模型选择契约，chicken 在进入双裁判阶段时仍会卡住。因此该项不应放到后期，而应在早期一并抽象。

### 5. 对 chicken 接入后的质量预期偏乐观

从现有数据基础看，chicken 可以生成 runtime 五件套并接入流程，但短期内更可能出现：

1. 大量记录落入 `generation_ready_limited`
2. 药物和高风险条目落入 `boundary_only` 或 `review_only`
3. 可运行不代表可大规模稳定正向生成

因此文档应明确：第一阶段目标是“跑通且保守”，不是“与 swine 对齐到同等质量”。

## 四、当前文档中判断正确的部分

以下判断经核对，方向正确，建议保留：

1. swine 侧已经具备完整 runtime/gold/eval/baseline 链路。
2. chicken 侧当前缺少 `runtime_core_manifest.json`、`gold_dataset_readiness_index.csv`、`drug_gold_role_index.csv`、`exporter_hard_block_rules.json`。
3. 54 字段 comparison CSV 口径确实被现有系统严格依赖，不应直接新增 `species_key`、`wiki_root` 等列。
4. 旧入口脚本与默认 swine 行为必须保留，否则会破坏现有命令与验收流程。
5. 第一阶段不宜直接做大规模目录迁移，应优先做原地抽象和兼容层。

## 五、建议修正后的执行原则

### 原则 1：先做兼容性抽象，再做命名规范化

第一阶段只处理：

1. species config
2. runtime contract
3. adapter
4. 路径上下文
5. baseline runner 兼容层
6. model routing contract

不建议第一阶段就同步推进大规模重命名与公共包迁移。

### 原则 2：先保证 swine 不退化，再让 chicken 最小闭环可运行

第一阶段的成功标准应是：

1. swine 结果与既有 baseline 口径不退化
2. chicken 能补齐 runtime 五件套
3. chicken 能完成最小 smoke 闭环

而不是一开始就要求 chicken 达到 swine 同等级质量。

### 原则 3：54 字段比较表保持冻结

运行追踪信息应写入 run manifest、report、metadata，不应写入 comparison CSV。

### 原则 4：架构合流决策必须前置

必须先明确 swine pipeline 与 `chicken_data_synthesis` 的关系，避免重复建设。

## 六、建议补充到原方案的必改项

1. 在文档开头新增“架构决策”章节，明确 swine pipeline 与 `chicken_data_synthesis` 的主从关系。
2. 将 model selection contract 前移到 Phase 1。
3. 将 baseline runner 的兼容层改造前移，在底层 phase 重命名前先完成 orchestration 适配。
4. 将 chicken 第一阶段目标收紧为“生成五类 runtime 文件并完成至少 5 条真实 smoke”。
5. 新增“第一阶段不解决的问题”章节，明确数据成熟度、judge 校准和大规模质量稳定性暂不承诺。

## 七、建议重排后的实施顺序

### Phase A：冻结基线与架构决策

目标：

1. 冻结 swine 当前 baseline、路径、54 字段口径
2. 明确 swine pipeline 与 `chicken_data_synthesis` 的关系
3. 输出 inventory 与依赖图

### Phase B：抽象基础契约

目标：

1. `SpeciesConfig`
2. `ManifestContract`
3. `PathContext`
4. `RuntimeIndexes`
5. model routing contract

### Phase C：chicken runtime 五件套生成

目标：

1. 基于现有 chicken exports 生成运行所需等价文件
2. 明确缺失字段的保守降级规则
3. 输出 validation report

### Phase D：生成链 species-aware 化

目标：

1. case variables
2. Phase 12/13/14
3. prompt pack
4. skeleton 渲染

### Phase E：评估与导出 species-aware 化

目标：

1. Phase 15
2. Phase 16
3. Phase 18
4. baseline runner orchestration

### Phase F：回归与 smoke

目标：

1. swine 回归
2. chicken smoke
3. 小批量验证

## 八、建议验收标准

### 代码验收

1. swine 默认命令不变
2. 旧入口仍可执行
3. Phase 12-18 全部支持 species-aware
4. model selection 不再依赖 `swine_runtime_selection` 单一键名

### 数据验收

1. swine comparison CSV 仍为 54 字段
2. chicken 能生成 runtime 五件套
3. chicken 全链路至少完成 5 条真实 smoke
4. 缺失字段必须显式标记，不能无解释留空

### 质量验收

1. swine 不退化
2. chicken 问答不出现猪病术语污染
3. 高风险药物、休药期、食品安全相关内容维持保守边界

## 九、最终判断

这份方案不是无效方案，而是“方向正确但执行设计偏理想化”的方案。

最终建议如下：

1. 不建议按当前版本直接开工。
2. 建议先按本审查文档修订为“兼容优先、分阶段落地”的执行版。
3. 修订后，该方案有较高概率实现既定目标。
4. 若不修订直接推进，中途出现范围失控、双轨系统并存、回归成本暴涨的概率较高。
