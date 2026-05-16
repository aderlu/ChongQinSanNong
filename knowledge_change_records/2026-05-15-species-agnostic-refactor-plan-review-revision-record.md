# 多物种 Wiki Pipeline 可复用改造方案审查修订记录

日期：2026-05-15

关联文档：

- `D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md`

## 一、修改背景

用户要求对原《多物种 Wiki 生成与评估全链路可复用改造方案》进行严格审查，判断它是否完整可落地，而不是停留在架构设想。

审查时对照了当前猪病 pipeline 真实代码，包括：

- `phase12_plan_samples_from_wiki.py`
- `phase13_build_answer_skeletons.py`
- `phase14_generate_two_stage_samples.py`
- `phase15_fact_level_evaluate_samples.py`
- `phase16_export_layered_training_sets.py`
- `phase18_dual_judge_and_arbitrate.py`
- `baseline_validation/baseline_validation_common.py`
- `baseline_validation/run_baseline_experiment.py`
- `baseline_validation/generate_baseline_groups.py`
- `baseline_validation/compare_groups.py`

审查结论是：原方案方向正确，但还不能直接作为执行方案，因为遗漏了现有链路中的部分硬约束。

## 二、之前存在的问题

### 1. Phase 12 没有被纳入核心改造范围

原方案主要覆盖 Phase 13、Phase 14、Phase 18 和 baseline，但当前完整 wiki-grounded 链路实际从 Phase 12 开始。

当前 Phase 12 直接依赖：

- `exports/runtime_core_manifest.json`
- `exports/gold_dataset_readiness_index.csv`
- `exports/drug_gold_role_index.csv`
- `exports/exporter_hard_block_rules.json`

鸡病目前没有这些等价文件。如果只生成 runtime manifest，鸡病仍然不能跑完整 Phase 12。

### 2. Phase 16 导出层遗漏

原方案没有把 Phase 16 列入核心改造文件。当前 Phase 16 仍存在：

- `swine-wiki-*` case_id 命名空间。
- `species = 猪` 的硬编码。
- 输出 metadata 和文件前缀的猪病默认假设。

这会导致鸡病即使前面生成成功，最终导出也可能被标记成猪病。

### 3. 54 字段口径不严谨

原方案写到“54 字段结构不变，只新增或保留 `species_key`、`wiki_root`、`run_id` 三个运行追踪字段”，这与当前代码不一致。

当前口径是：

- 51 个标准样本字段。
- 3 个比较追踪字段：`run_id`、`case_seed_id`、`baseline_group`。

如果再加入 `species_key` 和 `wiki_root`，就不再是 54 字段。

### 4. 路径迁移风险被低估

当前多个脚本使用 `Path(__file__).resolve().parents[...]` 推导 Wiki 根目录。例如：

- pipeline 脚本常用 `parents[2]`
- baseline 脚本常用 `parents[3]`

如果第一阶段直接迁移到新的顶层 `llm_wiki_runtime/`，默认路径会改变，容易破坏猪病既有流程。

### 5. 鸡病字段映射规则过粗

原方案提到把鸡病 `coverage_gap_status` 映射到 `evidence_coverage`、把 `evidence_status` 映射到 `task_use_status`，但没有给出保守降级规则。

如果简单映射，可能把 `INFERRED` 或 `NEEDS_REVIEW` 当成可生成事实，导致高风险处方、休药期或食品安全输出失控。

## 三、本次修改了什么

本次直接修订了：

- `D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md`

新增了本记录文档：

- `D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-refactor-plan-review-revision-record.md`

## 四、具体修订内容

### 1. 明确第一阶段原地抽象，不迁移旧入口

修订后方案明确：

- 第一轮不迁移旧入口脚本。
- 不改变猪病默认输出目录。
- 不改变 2026-05-14 baseline 验收基准。
- 不改变 54 字段比较表口径。
- 先在现有 pipeline 内原地抽象和兼容。

必须保留的旧入口包括：

- `phase12_plan_samples_from_wiki.py`
- `phase13_build_answer_skeletons.py`
- `phase14_generate_two_stage_samples.py`
- `phase15_fact_level_evaluate_samples.py`
- `phase16_export_layered_training_sets.py`
- `phase18_dual_judge_and_arbitrate.py`
- `baseline_validation/run_baseline_experiment.py`

### 2. 新增 PathContext 设计

修订后增加 `PathContext`，用于封装路径解析，逐步替代业务逻辑中散落的 `parents[2]`、`parents[3]`。

目标是降低未来公共包迁移风险，避免目录一变就全链路崩溃。

### 3. 补入 Phase 12 改造要求

修订后明确 Phase 12 必须 species-aware，并且鸡病接入前必须生成 Phase 12 所需的 5 个运行文件：

- `runtime_core_manifest.json`
- `runtime_exclude_patterns.json`
- `gold_dataset_readiness_index.csv`
- `drug_gold_role_index.csv`
- `exporter_hard_block_rules.json`

没有这些文件，不能宣布该物种接入完整链路。

### 4. 补入 Phase 16 改造要求

修订后把 `phase16_export_layered_training_sets.py` 加入优先改造清单，并明确：

- case_id namespace 从 species config 读取。
- `species` 从 species config 读取。
- 输出前缀、metadata、报告标题从 species config 读取。
- 54 字段不新增列。

### 5. 修正 54 字段定义

修订后严格定义：

- 54 字段 = 51 个标准样本字段 + `run_id`、`case_seed_id`、`baseline_group`。
- `species_key`、`wiki_root`、模型、并发、输入输出路径写入 `run_manifest.json` 和 `validation_report.md`。
- 如果未来要把 `species_key` 加入 CSV，必须另立字段版本，不能继续叫 54 字段。

### 6. 增加鸡病 conservative mapping 规则

修订后增加鸡病 evidence/runtime 映射表：

- `HUMAN_REVIEWED` 且有权威来源：可进入 `eval_ready` 或 `generation_ready_limited`。
- `EXTRACTED` 且 source 可追溯：可进入带边界候选。
- `INFERRED`：默认 `retrieval_only`。
- `NEEDS_REVIEW`：默认 `blocked` 或 `review_only`。
- 药物、休药期、食品安全缺少标签级证据：默认 `blocked` 或 `boundary_only`。

### 7. 扩展 baseline runner 改造范围

修订后不只修改 `generate_baseline_groups.py`，还必须同步修改：

- `build_case_seeds.py`
- `judge_general_consultation.py`
- `audit_grounding.py`
- `compare_groups.py`
- `run_baseline_experiment.py`

否则 baseline 三组实验仍不能完整 species-aware。

## 五、修改后解决了什么

修订后方案从“架构方向”升级为“可执行迁移方案”。

解决的问题：

1. 避免只改 Phase 13/14/18，却在 Phase 12 卡住。
2. 避免鸡病结果在 Phase 16 被导出成猪病。
3. 避免 54 字段验收口径被无意破坏。
4. 避免第一阶段搬目录导致路径推导失效。
5. 避免鸡病弱证据被错误升级为可生成事实。
6. 避免 baseline 只改单个脚本，其他脚本仍写死猪病。

## 六、预计更新效果

执行修订后的方案，预期可以实现：

- 猪病旧流程继续可运行。
- 鸡病可以在补齐运行索引后接入完整 Phase 12 到 Phase 18 链路。
- baseline 三组实验可以按 `--species swine/chicken` 运行。
- 54 字段比较表保持稳定。
- 新物种接入时只需补 species config、adapter、prompt pack、judge rubric 和运行索引映射，不需要复制整套 phase 脚本。

## 七、验证与检查

本次是文档修订，没有修改业务代码。

已完成：

- 对原方案进行代码级审查。
- 修订原方案中的落地缺口。
- 新增本次修订记录。

后续正式代码修改时，仍需每个 Phase 单独新增 change record，并附验证命令和运行结果。

## 八、未解决风险

1. 鸡病现有 source/fact/drug/rule schema 与猪病差异较大，adapter 规则需要在 Phase 1b 中用真实数据校验。
2. 猪病 Phase 14 和 Phase 18 文件较大，抽 prompt/rubric 时必须小步提交，避免破坏当前生成质量。
3. 真实 LLM 调用稳定性仍取决于配置、网络、供应商状态和并发限流。
4. 鸡病药物、休药期、蛋品安全证据如果不足，短期内可能只能生成边界型或低风险样本，不能强行生成正向处方样本。
