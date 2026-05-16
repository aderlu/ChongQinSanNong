# 多物种 Wiki 生成与评估全链路可复用改造方案

日期：2026-05-15

范围：`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative`、`D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative` 以及后续新增物种 Wiki。

## 一、当前结论

当前猪病系统已经形成了较完整的 Phase 12 规划、Phase 13 骨架、Phase 14 真实 LLM 生成、Phase 14b 自然化、Phase 15 事实门控、Phase 16 导出、Phase 18 双裁判/仲裁、baseline 三组对比和 CSV 导出链路，但这套链路仍然是“猪病专用实现”，不能直接完整复用于鸡病或后续新 Wiki。

鸡病 Wiki 已具备知识内容基础，包括疾病页、药物页、规则页、source、facts 和基础 exports，但缺少猪病链路所需的 runtime manifest、统一字段合同、物种变量配置、评估配置和可执行工具目录。因此，当前不能把鸡病路径简单传入猪病脚本后期望得到同等质量的完整结果。

本阶段暂不执行“LLM Wiki 后移”架构，而是先把现有 wiki-first / wiki-grounded 生成与评估链路改造成可复用框架，保证猪、鸡和后续新 Wiki 都能共用同一套执行流程。

本方案已经过一次基于现有代码的严格审查并修订。修订后的执行原则是：第一轮不迁移旧入口脚本，不改变猪病默认输出目录，不改变 2026-05-14 baseline 验收基准，不改变 54 字段比较表口径；先在现有 pipeline 内原地抽象和兼容，再考虑长期公共包迁移。

## 二、架构决策

### 1. Swine Pipeline 与 Chicken 应用层框架的关系

仓库中已经存在 `D:\XF-ChongQin\ai-\src\chicken_data_synthesis` 应用层框架，包含 application、domain、infrastructure、interfaces 分层，以及 LLM runtime、model fallback、judge normalization、pipeline use case、persistence 和 chicken Wiki CLI 等能力。

因此，本次改造不能把 chicken 当成完全空白系统，也不能在 swine pipeline 旁边再建设一套互不兼容的 chicken runtime。

本阶段采用如下架构决策：

1. **短期执行主干**：以现有 swine wiki-grounded pipeline 为执行主干，先抽出 species-aware 契约，保证 swine 不退化，并让 chicken Wiki 通过 adapter 进入 Phase 12 到 Phase 18 最小闭环。
2. **Chicken 能力复用**：优先复用 `chicken_data_synthesis` 中已经存在的模型路由、LLM runtime、judge normalization、fallback、运行状态和应用层组织经验，不重复实现等价能力。
3. **契约对齐**：swine pipeline 抽出的 `SpeciesConfig`、`RuntimeIndexes`、`ModelRoutingContract`、`JudgeRubric` 和 `RunManifest` 必须设计成可被 `chicken_data_synthesis` 调用或映射，而不是只服务 swine 目录内部脚本。
4. **长期合流方向**：当 swine 默认流程、chicken smoke 和 baseline orchestration 全部稳定后，再评估将公共能力迁入独立 runtime 包，或与 `chicken_data_synthesis` 的 application/infrastructure 分层合并。迁移前不得形成两套并行的 species-aware runtime。

### 1.1 Chicken_Data_Synthesis 复用边界清单

`chicken_data_synthesis` 不是本次多物种 Wiki pipeline 的替代主干；第一阶段只复用其中已经成熟、与物种无强绑定或可通过 adapter 对齐的能力。

第一阶段优先复用：

- `infrastructure.llm`：LLM 调用、key pool、fallback、错误分类、预算估算等运行能力。
- `application.services.review` 与 `infrastructure.evaluation`：judge payload normalization、score normalization、fallback judge 调用组织。
- `application.services.task_planning` 中的模型配置解析经验：用于对齐 `ModelRoutingContract`。
- `infrastructure.persistence` 中的运行快照和进度记录经验：用于 run manifest / runtime snapshot 设计。
- `interfaces.cli` 的 CLI 组织方式：作为未来统一命令入口参考。

第一阶段不直接复用或不直接吸收：

- chicken 现有输出路径、文件名前缀、benchmark/runtime 命名中仍带有旧业务语义或 swine 残留命名的部分。
- chicken 既有数据合成主流程作为多物种 Wiki pipeline 的主入口。
- chicken 现有业务字段作为 54 字段 baseline 合同的替代品。
- 未经审查的持久化目录命名、benchmark 命名、旧 dataset prefix。

第一阶段必须新增一个接口对齐清单：

| 能力 | 复用来源 | 多物种 pipeline 对接方式 | 是否第一阶段使用 |
| --- | --- | --- | --- |
| LLM runtime/fallback | `chicken_data_synthesis.infrastructure.llm` | 通过 `common/model_routing.py` 适配 | 是 |
| Judge normalization | `chicken_data_synthesis.infrastructure.evaluation` | 通过 `common/judge_rubric.py` 或 Phase 18 normalizer 适配 | 是 |
| Pipeline persistence | `chicken_data_synthesis.infrastructure.persistence` | 只参考 run snapshot 结构，不直接替换输出路径 | 部分 |
| Chicken CLI | `chicken_data_synthesis.interfaces.cli` | 作为未来统一 CLI 参考 | 否 |
| Chicken dataset output naming | 现有 chicken 应用层 | 暂不复用，需先清理旧命名 | 否 |

如果 Phase A inventory 发现 `chicken_data_synthesis` 中仍有 `swine_disease_dataset_*` 等命名残留，必须记录在合流风险中，不得在第一阶段直接把这些命名带入多物种 pipeline。

### 2. 第一阶段质量边界

第一阶段目标是“可复用、可运行、不破坏 swine、chicken 保守接入”，不是承诺 chicken 立即达到 swine 同等级数据质量。

第一阶段 chicken 的合理目标：

1. 能从现有 chicken exports 生成 runtime 五件套。
2. 能完成至少 5 条真实 LLM smoke 的 Phase 12 到 Phase 18 闭环，包含 Phase 14b 自然化步骤。
3. 生成和评估结果不出现猪病术语污染。
4. 缺证、高风险药物、休药期、蛋品/肉品安全内容默认保守处理。

第一阶段不承诺：

1. chicken 大规模 500 条结果质量立即达到 swine 成熟水平。
2. chicken 药物和处方样本具备与 swine 相同的正向生成比例。
3. chicken judge rubric 一次性完成充分校准。
4. chicken 原始 Wiki 字段成熟度由 adapter 自动补足。

## 三、之前存在的问题

### 1. 代码与物种强绑定

当前猪病链路中大量逻辑写死了猪病语境：

- `consultation_case_variables.py` 写死保育猪、育肥猪、母猪、仔猪等阶段。
- `phase13_build_answer_skeletons.py` 使用 `pig_stage_or_group`、猪群、猪场等字段和措辞。
- `phase14_generate_two_stage_samples.py` 写死 `species = 猪`、猪场问诊、猪舍处理、猪用药边界。
- `phase18_dual_judge_and_arbitrate.py` 使用 `judge_swine_*` 和 `swine_runtime_selection`。
- `baseline_validation/generate_baseline_groups.py` 写死猪场 baseline 问答提示词。
- 部分导出文件名、case_id、scorecard 名称、质量门控说明均带有 swine/pig 语义。

结果：

- 鸡病无法直接运行完整链路。
- 后续新增牛、羊、水禽等 Wiki 时会继续复制并改写脚本，代码膨胀。
- 每个物种独立维护 prompt、字段、裁判、导出逻辑，容易产生版本漂移。
- baseline 对比不稳定，因为不同物种可能不是同一套流程生成。

### 2. Runtime 合同不统一

猪病已有 `exports/runtime_core_manifest.json` 和 `exports/runtime_exclude_patterns.json`，作为默认生成和评估上下文入口。

鸡病目前只有 `portable_manifest.json` 和基础索引，没有同等 runtime allowlist / denylist。

此外，当前 Phase 12 不只依赖 `runtime_core_manifest.json`，还依赖：

- `exports/gold_dataset_readiness_index.csv`
- `exports/drug_gold_role_index.csv`
- `exports/exporter_hard_block_rules.json`

鸡病目前也没有这些等价文件。如果只生成 runtime manifest，Phase 12 仍然不能完整运行。

字段差异包括：

- 猪病 `disease_index.csv` 使用 `evidence_coverage`，鸡病使用 `coverage_gap_status`。
- 猪病 facts 有 `source_trust`、`usage_scope`，鸡病 facts 主要使用 `evidence_status`。
- 猪病 drug/rule 索引包含较强的生成与评估字段，鸡病 drug/rule 索引偏摘要。

结果：

- 同一个 phase 读取不同 Wiki 时无法稳定得到相同含义的字段。
- 证据覆盖、可信等级、训练用途、风险等级等 54 字段比较表无法可靠填充。
- 评估链路容易把“字段缺失”误判为“知识不可用”。

### 3. Prompt 与评估标准没有物种适配层

当前 prompt 同时包含通用任务逻辑和猪病领域语言。例如“真实猪场咨询”“猪群阶段”“猪舍温度”“猪用药标签”。

结果：

- 直接迁移到鸡病会出现不自然问法，如把鸡场说成猪场，或遗漏产蛋率、采食量、饮水量、粪便、免疫程序等鸡病关键线索。
- 裁判会按猪病问诊标准评分鸡病样本，导致评分不公平。
- 处方边界可能错误，例如鸡病必须关注蛋鸡/肉鸡差异、产蛋期禁用、弃蛋期、休药期和食品安全边界。

### 4. 文档和代码留痕分散

猪病已有较多知识库治理文档和 change records，但 pipeline 改造、运行经验、smoke 结果和字段合同仍分散在多个记录中。

结果：

- 后续汇报时难以说明“为什么改、改了什么、预期效果是什么”。
- 新物种接入时无法按固定 checklist 执行。
- 清理冗余脚本和中间文件时风险较高。

### 5. 导出层仍存在猪病硬编码

Phase 16 是最终训练集、比较表字段和生产 metadata 的关键层。当前导出代码仍存在 `swine-wiki-*` case_id 命名空间和 `species = 猪` 等硬编码。

结果：

- 即使前置生成阶段接入鸡病，最终导出仍可能被标记成猪病。
- 54 字段比较表中的物种上下文和 case_id 追踪会失真。
- 后续训练集混合时难以追溯样本来源。

### 6. 54 字段口径容易被误改

现有 baseline 比较表口径是：

- 51 个标准样本字段。
- 3 个比较追踪字段：`run_id`、`case_seed_id`、`baseline_group`。

合计 54 字段。`species_key`、`wiki_root`、`run_manifest` 等运行追踪信息不应直接加入比较 CSV，否则字段数会从 54 变成 56 或更多，破坏既定验收口径。

### 7. Model Selection / Judge Routing 与 Swine 强绑定

当前 Phase 18 和部分 baseline 评审链路依赖 `swine_runtime_selection`、`judge_swine_*` 等配置键和裁判模型命名。`chicken_data_synthesis` 中已经存在模型选择、fallback chain、judge normalization 等能力。如果不尽早抽象统一的 model routing contract，后续即使 Phase 12/14 能运行，进入双裁判和 baseline orchestration 时仍会卡住。

结果：

- chicken 无法稳定选择 generator、judge_a、judge_b、arbiter。
- baseline runner 在不同物种上使用的模型路由不可追溯。
- 可能重复实现一套与 `chicken_data_synthesis` 现有 LLM runtime 冲突的模型选择逻辑。

### 8. Baseline Runner Orchestration 改造成本被低估

当前 baseline runner 直接串联旧脚本文件名、旧输出路径和固定 54 字段校验口径。如果底层 phase 重命名、路径变更、字段透传变化，而 orchestration 层没有先兼容，baseline runner 会最先失效。

同时，54 字段不是只由 runner 临时拼接，而是由 `baseline_validation_common.py` 中的 `STANDARD_SAMPLE_FIELDS`、`COMPARISON_KEY_FIELDS` 和 `STANDARD_COMPARISON_FIELDS` 统一定义。runner 只是再做运行时硬校验。因此 baseline contract 改造必须显式包含 `baseline_validation_common.py`，不能只改 `run_baseline_experiment.py`。

结果：

- 只保留 wrapper 不足以保证三组实验可运行。
- 必须先让 runner 具备旧入口/新入口映射、species 参数透传、run manifest 记录和 54 字段校验能力。
- 必须把 `baseline_validation_common.py` 作为公共字段定义层冻结和测试。
- 文件命名规范化必须排在 orchestration 兼容层之后，不能先大规模重命名。

## 四、改造目标

### 总目标

将当前猪病专用全链路升级为“多物种 Wiki 生成与评估框架”，实现：

1. 猪病、鸡病、后续新 Wiki 共用同一套 phase 执行流程。
2. 物种差异通过配置和 adapter 表达，不复制整套脚本。
3. 统一 runtime manifest 合同，保证生成、评估和 54 字段对比表稳定。
4. 保持当前猪病 baseline 基准和验收要求不变。
5. 每次修改都有独立工作留痕文档，便于汇报和回溯。
6. 全流程使用 UTF-8，无乱码、无 BOM 混乱、无中间文件污染。
7. 保留旧入口脚本和默认 swine 行为，避免已有命令、脚本和验收流程失效。
8. 鸡病接入前必须补齐或生成 Phase 12 所需的 runtime/gold/drug/hard-block 等价运行文件。
9. 对应文件和目录名称必须同步规范化、合理化，避免公共流程继续使用带有单一物种或过期阶段含义的名称。
10. Model selection / judge routing 必须前置抽象，不能留到双裁判阶段末尾才处理。
11. 明确与 `chicken_data_synthesis` 的合流关系，避免重复建设第二套鸡病应用层 runtime。
12. Phase 14b 自然化步骤必须纳入正式链路改造与验收，不能只覆盖 Phase 14 到 Phase 15。
13. `baseline_validation_common.py` 必须作为 54 字段公共合同层纳入显式改造和回归测试。

### 非目标

本阶段不做：

- 不执行 LLM Wiki 后移。
- 不重写全部知识库页面。
- 不改变 2026-05-14 baseline 验收基准。
- 不删除用户已有结果文件。
- 不把鸡病强行套用猪病 prompt。
- 不在第一阶段迁移旧入口脚本到新顶层包。
- 不向 54 字段比较表随意增加 `species_key`、`wiki_root` 等新列。
- 不在没有兼容 wrapper 和回归验证前直接删除旧文件名或旧命令入口。
- 不承诺第一阶段 chicken 质量、药物正向处方比例、judge 校准程度达到 swine 成熟水平。
- 不重复建设 `chicken_data_synthesis` 已有的模型 fallback、judge normalization 和应用层 runtime 能力。
- 不绕过 Phase 14b 自然化直接进入 Phase 15，除非 run manifest 明确记录该 run 是特殊实验模式。
- 不在未冻结 `baseline_validation_common.py` 字段合同前修改 baseline runner 输出字段。

## 五、目标架构

长期建议形成如下结构：

```text
llm_wiki_runtime/
  common/
    io/
    llm/
    manifest/
    generation/
    evaluation/
    baseline/
    export/
    validation/
  species/
    swine/
      species_config.yaml
      prompt_pack.yaml
      judge_rubric.yaml
      field_mapping.yaml
    chicken/
      species_config.yaml
      prompt_pack.yaml
      judge_rubric.yaml
      field_mapping.yaml
  tools/
    run_pipeline.py
    build_runtime_manifest.py
    validate_species_config.py
    run_baseline_groups.py
```

但第一轮落地不直接迁移到该顶层包。现有代码大量使用 `Path(__file__).resolve().parents[...]` 推导 Wiki 根目录，直接移动脚本会改变默认路径，容易破坏已稳定的猪病流程。

第一轮采用“原地抽象、旧入口兼容”的结构：

```text
llm_wiki_swine_authoritative/tools/pipeline/
  common/
    species_config.py
    manifest_contract.py
    runtime_indexes.py
    prompt_pack.py
    judge_rubric.py
    path_context.py
    model_routing.py
    orchestration_compat.py
  species_configs/
    swine.yaml
    chicken.yaml
  species_adapters/
    swine_adapter.py
    chicken_adapter.py
```

旧入口脚本继续保留：

- `phase12_plan_samples_from_wiki.py`
- `phase13_build_answer_skeletons.py`
- `phase14_generate_two_stage_samples.py`
- `phase15_fact_level_evaluate_samples.py`
- `phase16_export_layered_training_sets.py`
- `phase18_dual_judge_and_arbitrate.py`
- `baseline_validation/run_baseline_experiment.py`

这些脚本第一阶段只新增 `--species`、`--species-config`、`--wiki-root` 等参数，并默认 `--species swine`，保证旧命令不变。

Baseline orchestration 层必须前置兼容。也就是说，在底层 phase 文件大规模重命名或迁移之前，先让 `run_baseline_experiment.py` 或其新入口具备如下能力：

- 同时识别旧入口和新入口。
- 解析 species config、wiki root、model routing 和 run manifest。
- 验证 54 字段口径。
- 记录实际调用的新旧入口映射。
- 对 swine 使用原输出路径，对 chicken 使用隔离输出路径。

同时建立规范化文件名。旧文件名作为兼容 wrapper 或 compatibility entrypoint 保留一个迁移周期，真正逻辑迁入通用命名文件。

建议命名迁移如下：

| 当前文件 | 规范化目标文件 | 处理方式 |
| --- | --- | --- |
| `phase12_plan_samples_from_wiki.py` | `plan_samples_from_runtime_manifest.py` | 旧文件保留 wrapper，调用新文件主逻辑 |
| `phase13_build_answer_skeletons.py` | `build_answer_skeletons.py` | 旧文件保留 wrapper |
| `phase14_generate_two_stage_samples.py` | `generate_grounded_samples.py` | 旧文件保留 wrapper |
| `phase14b_naturalize_grounded_answers.py` | `naturalize_grounded_answers.py` | 旧文件保留 wrapper |
| `phase15_fact_level_evaluate_samples.py` | `evaluate_fact_grounding.py` | 旧文件保留 wrapper |
| `phase16_export_layered_training_sets.py` | `export_layered_training_sets.py` | 旧文件保留 wrapper |
| `phase18_dual_judge_and_arbitrate.py` | `judge_and_arbitrate_samples.py` | 旧文件保留 wrapper |
| `wiki_first_judge_prompts.py` | `judge_prompt_pack.py` | 迁入 prompt pack，旧文件保留导入兼容 |
| `wiki_first_llm_client.py` | `llm_client.py` | 迁入 common，旧文件保留导入兼容 |
| `baseline_validation/generate_baseline_groups.py` | `baseline_validation/generate_comparison_groups.py` | 旧文件保留 wrapper |
| `baseline_validation/judge_general_consultation.py` | `baseline_validation/judge_consultation_samples.py` | 旧文件保留 wrapper |
| `baseline_validation/audit_grounding.py` | `baseline_validation/audit_sample_grounding.py` | 旧文件保留 wrapper |
| `baseline_validation/compare_groups.py` | `baseline_validation/build_comparison_table.py` | 旧文件保留 wrapper |
| `baseline_validation/run_baseline_experiment.py` | `baseline_validation/run_comparison_experiment.py` | 旧文件保留 wrapper |

命名原则：

- 公共文件名不出现 `swine`、`pig`、`chicken` 等物种词，物种差异放入 species config 或 adapter。
- 文件名描述职责，不描述历史阶段号；phase 编号可保留在报告、run manifest 和兼容入口中。
- 若文件仍为物种专用，必须放入 `species_adapters/<species>/` 或 `species_configs/<species>/`。
- 重命名必须配套更新测试、文档、运行脚本、change record 和 run manifest 中的入口记录。
- 每次重命名必须提供旧命令兼容验证，避免破坏已有自动化和验收命令。
- 第一阶段先完成兼容性抽象和 orchestration 适配，再推进大规模文件重命名；命名规范化不能早于 runner 兼容层。

长期可在所有测试稳定后，把 `common/` 与 `species_adapters/` 迁出到独立 `llm_wiki_runtime/` 包。迁移前必须先完成路径上下文封装，不能再让业务代码直接依赖 `parents[2]` 或 `parents[3]`。

## 六、核心设计

### 1. SpeciesConfig

新增统一物种配置，代替代码中的硬编码。

必需字段：

```yaml
species_key: swine
species_cn: 猪
species_en: swine
farm_context_cn: 猪场
animal_group_label: 猪群
case_stage_field: production_stage
output_prefix: swine_wiki
runtime_selection_key: swine_runtime_selection
required_runtime_files:
  - runtime_core_manifest.json
  - runtime_exclude_patterns.json
  - gold_dataset_readiness_index.csv
  - drug_gold_role_index.csv
  - exporter_hard_block_rules.json
```

鸡病示例：

```yaml
species_key: chicken
species_cn: 鸡
species_en: chicken
farm_context_cn: 鸡场
animal_group_label: 鸡群
case_stage_field: production_stage
output_prefix: chicken_wiki
runtime_selection_key: chicken_runtime_selection
required_runtime_files:
  - runtime_core_manifest.json
  - runtime_exclude_patterns.json
  - gold_dataset_readiness_index.csv
  - drug_gold_role_index.csv
  - exporter_hard_block_rules.json
```

还应包含：

- 生产阶段：雏鸡、育成鸡、蛋鸡、肉鸡、种鸡。
- 场景线索：采食量、饮水量、精神、粪便、呼吸音、产蛋率、死淘、免疫史。
- 普通养殖户语言限制：避免过多“剖检、实验室检测、流调”等专业术语。
- 临床式回答要求：直接判断、现场处理、用药边界、观察指标、何时升级。
- 高风险边界：法定疫病、食品安全、禁用药、休药期、蛋品处理。
- 输出命名：case_id namespace、文件前缀、报告前缀。
- 旧字段兼容：猪病保留 `pig_stage`，主字段统一使用 `production_stage`。

### 2. ManifestAdapter

新增 runtime manifest 与 Phase 12 运行索引标准合同。

统一后的 manifest record 至少包括：

```json
{
  "entity_id": "",
  "entity_type": "disease|drug|rule|source|syndrome",
  "entity_name": "",
  "species_key": "",
  "page_relpath": "",
  "source_trust": "",
  "evidence_coverage": "",
  "evidence_anchor_count": 0,
  "risk_class": "",
  "task_use_status": "",
  "gold_dataset_role": "",
  "allowed_question_types": [],
  "blocked_question_types": [],
  "facts": []
}
```

猪病 adapter 负责从现有字段直接映射。

鸡病 adapter 负责把：

- `coverage_gap_status` 映射到 `evidence_coverage`
- `evidence_status` 映射到 `task_use_status` 候选值
- 缺失的 `source_trust` 用 source governance 或默认规则补齐
- drug/rule 简表扩展成统一实体记录

注意：上述映射不是简单改名，必须按风险和证据级别做保守降级。建议转换规则如下：

| 鸡病字段状态 | 默认 runtime 角色 | 默认训练用途 | 说明 |
| --- | --- | --- | --- |
| `HUMAN_REVIEWED` 且有 A0/A1/A2/SRC 来源锚点 | `eval_ready` 或 `generation_ready_limited` | 可进入评估或低风险生成 | 仍需按风险类型判断是否可正向处方 |
| `EXTRACTED` 且 source 可追溯 | `generation_ready_limited` | 可生成带边界的候选 | 不得默认输出高风险处方、休药期、监管结论 |
| `INFERRED` | `retrieval_only` | 只用于召回和上下文 | 不作为事实裁判硬依据 |
| `NEEDS_REVIEW` | `blocked` 或 `review_only` | 不进入正向生成 | 可用于负样本、拒答、缺证训练 |
| 药物/休药期/食品安全缺少标签级证据 | `blocked` 或 `boundary_only` | 不进入 positive prescription | 只能输出边界提醒或建议线下兽医核查 |

缺失字段不能静默为空，必须写入：

- `field_missing`
- `defaulted_by_adapter`
- `needs_review`

这样评估时能区分“没有证据”和“旧 schema 暂未迁移”。

ManifestAdapter 还必须生成 Phase 12 依赖的等价文件：

1. `runtime_core_manifest.json`：统一 allowlist。
2. `runtime_exclude_patterns.json`：默认 denylist，可从通用模板和物种规则合成。
3. `gold_dataset_readiness_index.csv`：从 manifest record 派生，字段不足时显式标记 `blocked` 或 `generation_ready_limited`。
4. `drug_gold_role_index.csv`：药物页默认保守，缺少标签证据时标为 `boundary_only`、`negative_trap` 或 `exclude_from_positive_generation`。
5. `exporter_hard_block_rules.json`：由通用高风险规则和物种药残/食品安全规则合成。

没有这些文件，不能宣布该物种已经接入完整链路。

### 3. CaseVariableProvider

把 `consultation_case_variables.py` 改成通用变量生成器。

原始问题：

```python
_PIG_STAGES = ["保育猪", "育肥猪", ...]
pig_stage = ...
```

目标形态：

```python
provider = CaseVariableProvider(species_config)
scenario = provider.build(entity_record, seed)
```

输出字段统一：

```json
{
  "species_key": "chicken",
  "production_stage": "产蛋鸡",
  "farm_scale": "几千只的蛋鸡场",
  "observed_signs": ["采食下降", "产蛋率下降", "拉黄绿色稀粪"],
  "timeline": "这两天",
  "farmer_intent": "想先判断严重不严重，现场怎么处理"
}
```

### 4. PromptPack

把 prompt 拆成三层：

1. 通用任务 prompt：JSON 输出、字段要求、不要编造、必须临床式回答。
2. 物种 prompt：猪场/鸡场语境、阶段、普通用户表达、处方边界。
3. 风险 prompt：法定疫病、禁用药、休药期、食品安全、公共卫生。

这样 Phase 14 不再直接写死“猪场兽医问诊 agent”，而是读取：

```python
prompt_pack.render("two_stage_generation", species_config, entity_record, scenario)
```

### 5. JudgeRubric

把双裁判与仲裁评分标准配置化。

通用维度保持不变：

- scenario_realism
- consultation_completeness
- medical_correctness
- followup_logic
- triage_boundary
- context_consistency
- actionability
- structure_labelability

物种化描述单独配置。

猪病：

- 是否像真实猪场问诊。
- 是否结合猪群阶段、症状、病程、死淘、混群。
- 是否遵守猪用药、休药期和监管边界。

鸡病：

- 是否像真实鸡场问诊。
- 是否结合日龄/用途、采食、饮水、粪便、呼吸、产蛋率、死亡变化。
- 是否区分蛋鸡/肉鸡/种鸡用药和食品安全边界。

### 6. BaselineGroupRunner

三组实验 A/B/C 应使用统一 runner：

```text
run_baseline_groups.py
  --species swine
  --wiki-root ...
  --limit 500
  --parallel 3
```

```text
run_baseline_groups.py
  --species chicken
  --wiki-root ...
  --limit 500
  --parallel 3
```

输出文件统一：

```text
exports/baseline_validation/{species_key}/
  group_a_full.csv
  group_b_full.csv
  group_c_full.csv
  comparison_54_fields.csv
  run_manifest.json
  validation_report.md
```

54 字段结构不变，严格定义为：

- 51 个标准样本字段。
- 3 个比较追踪字段：`run_id`、`case_seed_id`、`baseline_group`。

`species_key`、`species_config_path`、`wiki_root`、`run_manifest_path`、模型配置、并发数、输入输出路径等运行信息写入伴随 `run_manifest.json` 和 `validation_report.md`，不进入 54 字段比较表。若后续确需把 `species_key` 加入 CSV，必须另立版本并改称 55/56 字段比较表，不能继续沿用 54 字段验收口径。

### 7. PathContext

新增路径上下文封装，替代业务逻辑散落使用 `parents[2]`、`parents[3]`。

目标形态：

```python
context = PathContext.from_args(
    script_file=__file__,
    wiki_root=args.wiki_root,
    species_key=args.species,
)
exports = context.exports_dir
baseline_exports = context.baseline_exports_dir
```

第一阶段旧脚本中的 `ROOT = Path(__file__).resolve().parents[...]` 可以暂时保留作为默认值，但读写输出前必须通过 `PathContext` 解析。这样后续迁移公共包时不会再次大面积修改路径逻辑。

### 8. ModelRoutingContract

新增模型路由契约，前置于 Phase 18 改造。

目标：

- 不再让生成、双裁判、仲裁、baseline judge 直接依赖 `swine_runtime_selection` 或 `judge_swine_*`。
- 支持从统一配置解析 generator、judge_a、judge_b、arbiter、baseline_judge、fallback chain、并发、超时和模型成本信息。
- 能与 `chicken_data_synthesis` 已有 LLM runtime 和 model fallback 结构对齐。

建议结构：

```yaml
model_routing:
  generator:
    primary: generator_default
    fallbacks: []
  judge_a:
    primary: judge_a_default
    fallbacks: []
  judge_b:
    primary: judge_b_default
    fallbacks: []
  arbiter:
    primary: arbiter_default
    fallbacks: []
  baseline_judge:
    primary: baseline_judge_default
    fallbacks: []
```

swine adapter 可以继续读取旧 `swine_runtime_selection` 并转换成统一结构。chicken adapter 应优先检查 `chicken_data_synthesis` 现有配置能力，避免重复维护模型池。

验收要求：

- swine 旧配置键仍可用，但 run manifest 记录为统一 `model_routing`。
- chicken 能解析 generator、judge_a、judge_b、arbiter。
- 模型选择失败时输出明确错误，不允许静默 fallback 到 swine judge。
- baseline runner 使用同一模型路由契约。

## 七、分阶段执行方案

### Phase A：冻结基线、依赖图和架构决策

目标：

- 不改变猪病现有 baseline 验收基准。
- 明确当前代码、字段、输出、测试状态。
- 明确 swine pipeline 与 `chicken_data_synthesis` 的合流关系。

动作：

1. 生成当前猪病 pipeline 文件清单。
2. 生成鸡病 exports 字段盘点。
3. 记录 Phase 12 到 Phase 18 的真实入口、参数、输入、输出。
4. 锁定 54 字段当前定义：51 个样本字段 + `run_id`、`case_seed_id`、`baseline_group`。
5. 记录 Phase 12 硬依赖文件：runtime manifest、gold readiness、drug role、hard block rules。
6. 记录 Phase 16 的导出硬编码点：case_id namespace、species、文件前缀、metadata。
7. 盘点 `chicken_data_synthesis` 中可复用能力：LLM runtime、model fallback、judge normalization、persistence、CLI。
8. 建立本次迁移总控记录文档。

验收：

- 有 `knowledge_change_records/YYYY-MM-DD-species-agnostic-phase0-inventory.md`
- 文档说明当前问题、涉及文件、未修改代码。
- 有机器可读的 inventory JSON，记录脚本入口、输入输出文件、字段常量、硬编码扫描结果。
- 文档明确：短期以 swine wiki-grounded pipeline 为执行主干，chicken 通过 adapter 最小闭环接入；长期再评估公共 runtime 与 `chicken_data_synthesis` 合流。

### Phase B：抽出基础契约与 Orchestration 兼容层

目标：

- 建立 `SpeciesConfig`、`FieldMapping`、`RuntimeManifestContract`、`PathContext`、`RuntimeIndexes`、`ModelRoutingContract`。
- 在底层 phase 重命名前，先让 baseline runner 能识别 species、旧入口、新入口和 run manifest。

动作：

1. 新增 species 配置目录。
2. 新增 swine 配置，内容从现有硬编码迁移。
3. 新增 chicken 配置，按鸡病问诊语境补齐。
4. 新增 manifest 合同说明文档。
5. 新增 model routing 合同。
6. 新增 baseline orchestration compatibility 层。
7. 对接或映射 `chicken_data_synthesis` 现有模型选择/fallback 能力。

涉及代码：

- 新增 `species_config_loader.py`
- 新增 `manifest_contract.py`
- 新增 `path_context.py`
- 新增 `runtime_indexes.py`
- 新增 `model_routing.py`
- 新增 `baseline_validation/orchestration_compat.py`
- 新增 `species_configs/swine.yaml`
- 新增 `species_configs/chicken.yaml`

验收：

- 猪病配置加载结果与原硬编码含义一致。
- 鸡病配置能通过 schema 校验。
- 暂不改变生成结果。
- `--species` 默认值为 `swine`，旧命令不传参数仍能运行。
- 54 字段常量没有变化。
- model routing 能把旧 `swine_runtime_selection` 转换为统一结构。
- baseline runner 能在不改底层 phase 的情况下记录 species、入口映射和 run manifest。

### Phase C：补齐鸡病运行索引生成器

目标：

- 在不重写鸡病 Wiki 页面、不执行 LLM Wiki 后移的前提下，从现有鸡病 exports 生成完整运行所需索引。

动作：

1. 新增或扩展 `build_runtime_manifest.py`，支持 `--species chicken --wiki-root <chicken_root>`。
2. 从鸡病 `knowledge_facts.json`、`disease_index.csv`、`drug_page_index.csv`、`rule_index.csv`、`source_index.csv` 生成统一 runtime manifest。
3. 生成 `runtime_exclude_patterns.json`。
4. 生成 `gold_dataset_readiness_index.csv`。
5. 生成 `drug_gold_role_index.csv`。
6. 生成 `exporter_hard_block_rules.json`。
7. 输出 `runtime_manifest_validation_report.md`。

验收：

- 鸡病 exports 下出现 Phase 12 必需的 5 个运行文件。
- 每个 record 都有 `task_use_status`，不允许无解释空值。
- 药物和食品安全相关条目默认保守，缺少标签证据时不得标为 `positive_label_candidate`。
- 运行索引生成不调用 LLM，断网可运行。
- validation report 明确统计 `generation_ready_limited`、`retrieval_only`、`blocked`、`boundary_only` 比例，不能把结构接入误写成质量已成熟。

### Phase D：生成链 Species-Aware 化

目标：

- 将 case variables、Phase 12、Phase 13、Phase 14、Phase 14b 改成 species-aware。

动作：

1. 保留旧函数作为兼容包装。
2. 新增 `build_case_variables(species_config, entity_record, seed)`。
3. 将 `pig_stage` 改为 `production_stage`。
4. 输出中保留兼容字段：猪病可以同时输出 `pig_stage`，但主字段改为 `production_stage`。
5. Phase 12 增加 `--species`，读取该物种的 runtime/gold/drug/hard-block 文件。
6. Phase 12 输出计划时写入 `species_key` 到内部 metadata，但不改变 54 字段 CSV。
7. 把 answer skeleton 中的物种术语替换为配置渲染。
8. 把 Phase 14 的系统 prompt、生成 prompt、fallback answer 改成模板。
9. 将 `phase14b_naturalize_grounded_answers.py` 纳入正式链路，增加 `--species`、`--wiki-root`、`--run-id` 和 run manifest 记录。
10. Phase 14b 的自然化 prompt、质量门控和 fallback 文案从 species config / prompt pack 渲染，不能继续写死猪场语境。
11. baseline runner 调用顺序必须明确记录为 Phase 14 -> Phase 14b -> Phase 15，不得在默认链路中跳过 Phase 14b。
12. 增加鸡病 prompt pack。
13. 保留猪病 prompt 输出效果，避免 baseline 漂移。
14. 新增鸡病变量生成测试。

验收：

- 猪病 Phase 12 旧命令仍可运行。
- 猪病 smoke 生成不退化。
- 鸡病能生成自然鸡场问诊变量。
- 鸡病样本不得出现猪场、猪群、猪舍、仔猪、母猪等污染词。
- 输出主字段使用 `production_stage`，猪病兼容字段 `pig_stage` 只作为向后兼容存在。
- 鸡病 30 条 smoke 中问题像真实养殖户问诊。
- 回答必须有临床判断、现场处理、用药边界和升级条件。
- Phase 14b 旧命令仍可运行，新入口 `naturalize_grounded_answers.py` 输出与旧入口一致或差异可解释。
- run manifest 记录 Phase 14b 是否执行、输入文件、输出文件、species 和 prompt pack 版本。

### Phase E1：事实评估与导出 Species-Aware 化

目标：

- 猪病和鸡病都能进入事实门控与训练集/比较表导出，且导出层无物种污染。

动作：

1. Phase 15 从 `PathContext` 读取该物种 runtime manifest。
2. Phase 15 对缺证、弱证和高风险条目做保守判定，不把 adapter 补齐字段误当强证据。
3. Phase 16 增加 `--species`。
4. Phase 16 的 case_id namespace 从配置读取，例如 `swine-wiki-*`、`chicken-wiki-*`。
5. Phase 16 的 `species`、输出前缀、metadata、报告标题从配置读取。
6. 54 字段导出不新增列，运行追踪写入 run manifest。

验收：

- 猪病导出字段和文件名保持兼容。
- 鸡病导出不出现猪病 case_id namespace。
- 鸡病导出 `species` 为鸡，且 metadata 可追溯到 chicken config。
- 54 字段字段数和字段名不变。

### Phase E2：裁判、仲裁和 Baseline Orchestration Species-Aware 化

目标：

- Phase 18、baseline 三组实验和 54 字段比较表在多物种下稳定运行，且不破坏 swine 既有基准。

动作：

1. Phase 18 使用 `ModelRoutingContract` 和 `JudgeRubric`。
2. 将 `swine_runtime_selection` 改成通用 `model_routing`，旧键由 swine adapter 兼容。
3. 裁判名称、scorecard 名称配置化。
4. `wiki_first_judge_prompts.py` 中的猪病 rubric 保留为 swine prompt pack，不直接删除。
5. baseline runner orchestration 使用前置兼容层，统一调用旧入口或新入口。
6. 将 `baseline_validation_common.py` 作为 54 字段公共合同层显式冻结和测试。
7. 将 `build_case_seeds.py`、`generate_baseline_groups.py`、`judge_general_consultation.py`、`audit_grounding.py`、`compare_groups.py`、`run_baseline_experiment.py` 改成 species-aware。
8. runner 必须显式串联 Phase 14 -> Phase 14b -> Phase 15 -> Phase 18 -> compare/export 的默认顺序。

验收：

- 猪病原有双裁判/仲裁字段不变。
- 鸡病能输出完整裁判字段。
- 评分说明符合鸡病临床语境。
- 鸡病裁判不按“真实猪场问诊”评分。
- `--species swine` 能复现猪病流程。
- `--species chicken` 能产出鸡病三组 CSV。
- 断网或 LLM 失败时不崩溃，记录失败状态，不写坏 CSV。
- `STANDARD_SAMPLE_FIELDS` 不变，`STANDARD_COMPARISON_FIELDS` 仍为 54 字段。
- `baseline_validation_common.py` 有独立测试验证 51 + 3 字段口径。

### Phase F：测试、回归与 Smoke

目标：

- 保证重构没有破坏猪病基准，并验证鸡病可运行。

测试分层：

1. 单元测试：配置加载、manifest 映射、case variables。
2. 离线测试：无网络、无 LLM mock，保证流程不崩。
3. 运行索引测试：鸡病必须生成 Phase 12 所需 5 个文件。
4. LLM smoke：每物种每组 5 条。
5. 质量 smoke：每物种每组 30 条。
6. 正式小批量：每物种每组 500 条。

验收：

- 猪病结果与 2026-05-14 验收标准一致。
- 鸡病结果没有猪病术语污染。
- 54 字段完整率达到 100%。
- `user_query` 和 `assistant_answer` 通过真实性门控。
- 鸡病 Phase 12 到 Phase 18 全链路至少完成 5 条真实 LLM smoke，且链路包含 Phase 14b。
- 第一阶段只要求 chicken smoke 闭环质量可审查、边界保守，不要求大规模结果达到 swine 成熟质量。

## 七、建议修改文件清单

优先改造：

- `tools/pipeline/phase12_plan_samples_from_wiki.py`
- `tools/pipeline/consultation_case_variables.py`
- `tools/pipeline/phase13_build_answer_skeletons.py`
- `tools/pipeline/phase14_generate_two_stage_samples.py`
- `tools/pipeline/phase14b_naturalize_grounded_answers.py`
- `tools/pipeline/phase15_fact_level_evaluate_samples.py`
- `tools/pipeline/phase16_export_layered_training_sets.py`
- `tools/pipeline/phase18_dual_judge_and_arbitrate.py`
- `tools/pipeline/wiki_first_judge_prompts.py`
- `tools/pipeline/baseline_validation/build_case_seeds.py`
- `tools/pipeline/baseline_validation/baseline_validation_common.py`
- `tools/pipeline/baseline_validation/generate_baseline_groups.py`
- `tools/pipeline/baseline_validation/judge_general_consultation.py`
- `tools/pipeline/baseline_validation/audit_grounding.py`
- `tools/pipeline/baseline_validation/compare_groups.py`
- `tools/pipeline/baseline_validation/run_baseline_experiment.py`
- `tools/pipeline/baseline_validation/qa_realism_gate.py`

建议新增：

- `tools/pipeline/plan_samples_from_runtime_manifest.py`
- `tools/pipeline/build_answer_skeletons.py`
- `tools/pipeline/generate_grounded_samples.py`
- `tools/pipeline/naturalize_grounded_answers.py`
- `tools/pipeline/evaluate_fact_grounding.py`
- `tools/pipeline/export_layered_training_sets.py`
- `tools/pipeline/judge_and_arbitrate_samples.py`
- `tools/pipeline/common/species_config.py`
- `tools/pipeline/common/manifest_contract.py`
- `tools/pipeline/common/path_context.py`
- `tools/pipeline/common/runtime_indexes.py`
- `tools/pipeline/common/model_routing.py`
- `tools/pipeline/common/prompt_pack.py`
- `tools/pipeline/common/judge_rubric.py`
- `tools/pipeline/common/species_runtime_adapter.py`
- `tools/pipeline/common/llm_client.py`
- `tools/pipeline/common/entrypoint_compat.py`
- `tools/pipeline/species_configs/swine.yaml`
- `tools/pipeline/species_configs/chicken.yaml`
- `tools/pipeline/species_adapters/swine_adapter.py`
- `tools/pipeline/species_adapters/chicken_adapter.py`
- `tools/pipeline/build_runtime_manifest.py`
- `tools/pipeline/baseline_validation/generate_comparison_groups.py`
- `tools/pipeline/baseline_validation/judge_consultation_samples.py`
- `tools/pipeline/baseline_validation/audit_sample_grounding.py`
- `tools/pipeline/baseline_validation/build_comparison_table.py`
- `tools/pipeline/baseline_validation/run_comparison_experiment.py`
- `tools/pipeline/baseline_validation/orchestration_compat.py`
- `tests/test_species_config_loader.py`
- `tests/test_manifest_contract_mapping.py`
- `tests/test_runtime_index_generation.py`
- `tests/test_baseline_field_contract.py`
- `tests/test_multispecies_case_variables.py`
- `tests/test_phase14b_species_naturalization.py`
- `tests/test_phase16_species_export.py`
- `tests/test_legacy_entrypoint_compatibility.py`
- `tests/test_chicken_pipeline_smoke.py`

建议迁移或整理：

- 把猪病专用 prompt 文本移入 `species_configs/swine/`。
- 把通用 JSON/CSV/LLM 调用逻辑移入 `common/`。
- 把旧的猪病脚本保留为 thin wrapper，避免已有命令失效。
- 第一阶段不移动旧入口脚本，不移动旧输出目录。
- 待回归稳定后，再评估是否把 `common/` 迁出到独立公共包。
- 对名称不规范、职责已迁移的旧文件，在完成兼容期和回归验证后统一归档或删除；删除前必须有 change record 和替代入口说明。

## 八、文档留痕规范

每一次实际代码修改必须新增一份记录到：

`D:\XF-ChongQin\knowledge_change_records`

命名建议：

```text
YYYY-MM-DD-species-agnostic-phaseN-short-title.md
```

每份文档必须包含：

1. 修改背景。
2. 之前存在什么问题。
3. 修改前代码是什么状态。
4. 本次改了哪些文件。
5. 新增了哪些代码或配置。
6. 删除、迁移、整理了哪些冗余内容。
7. 修改后解决了什么。
8. 预计产生什么效果。
9. 验证命令和验证结果。
10. 未解决风险。
11. 如果涉及重命名，必须列出旧文件名、新文件名、兼容 wrapper、替代命令、验证结果和计划清理时间。

禁止只写“优化完成”“修复完成”。

## 九、乱码防护措施

所有新增和修改文件执行以下约束：

1. Markdown、YAML、JSON、Python 均使用 UTF-8。
2. 不使用 GBK 写文件。
3. PowerShell 读取中文文件时使用显式编码。
4. Python 文件读写统一使用 `encoding="utf-8"` 或 `encoding="utf-8-sig"` 读取 CSV。
5. CSV 输出使用 `utf-8-sig`，方便 Excel 打开。
6. 每次修改后运行 mojibake 检查，扫描：
   - `锟`
   - `�`
   - `Ã`
   - `Â`
7. 不用 shell 重定向写入大段中文文档，优先使用补丁或 Python UTF-8 写入。

## 十、冗余代码与文档清理原则

本次架构改造不应直接删除旧结果。

可清理对象：

- 临时 smoke 输出。
- 空目录。
- 重复的临时脚本。
- 已迁移且有 wrapper 替代的测试性脚本。

不可清理对象：

- 用户审查用 CSV。
- baseline 正式结果。
- 2026-05-14 验收基准相关文档。
- 未确认归属的旧生成结果。
- 用户未要求删除的知识页面或 raw source。

清理动作必须在 change record 中写清楚：

- 清理了什么。
- 为什么可以清理。
- 是否影响复现。
- 是否有替代入口。

## 十一、推荐执行顺序

最稳妥的执行顺序：

1. Phase A：冻结基线、依赖图和架构决策。
2. Phase B：抽出基础契约与 orchestration 兼容层。
3. Phase C：鸡病运行索引生成器。
4. Phase D：生成链 species-aware 化。
5. Phase E1：事实评估与导出 species-aware 化。
6. Phase E2：裁判、仲裁和 baseline orchestration species-aware 化。
7. Phase F：猪病回归、鸡病 smoke、小批量验证。

不建议一上来同时修改 Phase 14、Phase 18 和文件命名。应先保证配置、路径上下文、模型路由、baseline orchestration、运行索引和 54 字段合同稳定，否则后续错误会难以定位。

## 十二、最终验收标准

### 代码验收

- 猪病不再依赖散落硬编码完成主流程，硬编码集中到 swine config。
- 鸡病通过 chicken config 接入同一 runner。
- 新物种只需要新增 Wiki exports、species config、field mapping、prompt pack、judge rubric，即可进入 smoke。
- 旧入口脚本保持可用，默认行为仍是 swine。
- Phase 12 到 Phase 18 均支持 species-aware，不只支持 Phase 13/14/18。
- Phase 14b 自然化是默认链路的一部分，并支持 species-aware。
- 公共文件名已经规范化，不再把通用流程命名为 swine/pig/wiki_first 专用逻辑。
- 旧文件名有 wrapper 兼容测试，且 run manifest 能记录实际调用的新入口。
- model selection 不再依赖 `swine_runtime_selection` 单一键名；旧键只作为 swine adapter 兼容输入。
- baseline runner 在底层 phase 重命名前已经具备旧/新入口映射和 species-aware orchestration。
- `baseline_validation_common.py` 是 54 字段公共合同层，有独立测试保护。

### 数据验收

- 猪病、鸡病都能输出三组完整 CSV。
- 最终比较表固定 54 字段：51 标准样本字段 + `run_id`、`case_seed_id`、`baseline_group`。
- `sample_id`、`entity_id`、`entity_type`、`risk_class`、`case_context`、`user_query`、`assistant_answer`、双裁判、仲裁字段完整。
- 字段缺失必须有明确状态，不允许无解释空值。
- `species_key`、`wiki_root`、模型、并发、输入输出文件写入 run manifest，不写入 54 字段 CSV。
- 鸡病必须有 Phase 12 必需运行文件：runtime manifest、exclude patterns、gold readiness、drug role、hard block rules。
- chicken validation report 必须报告保守降级比例，避免把“结构可运行”误写成“质量已成熟”。

### 质量验收

- `user_query` 像真实养殖户，不主动堆砌实验室检测、剖检等专业术语。
- `assistant_answer` 是临床式回答，不以继续追问替代回答。
- 鸡病回答必须体现鸡病场景，不能出现猪场术语污染。
- 高风险诊疗、处方、休药期、禁用药、监管处置必须有证据边界。
- 鸡病药物、休药期、蛋品/肉品安全缺少标签级证据时不得正向处方化输出。
- 第一阶段 chicken 质量验收以“真实 smoke 可审查、无猪病污染、边界保守”为准，不以 swine 成熟质量作为硬性同级目标。

### 可维护性验收

- 新物种接入不复制整套 phase 文件。
- 每次修改有 change record。
- 所有运行有 run manifest。
- 所有输出路径按 species 和 run_id 隔离。
- 第一阶段不通过搬目录制造大规模路径风险；公共包迁移必须在回归通过后单独执行。
- 文件命名、目录命名、入口命令和文档引用保持一致；任何重命名都有兼容层和清理计划。

## 十三、预期效果

完成后，系统将从“猪病专用链路”升级为“多物种 Wiki 生成与评估平台”。

直接收益：

- 猪病原有 baseline 和验收标准可继续保留。
- 鸡病可以接入完整生成与评估链路。
- 后续新 Wiki 不需要复制猪病代码，只需补齐配置和 manifest 映射。
- 54 字段比较表具备跨物种稳定性。
- 运行失败、字段缺失、证据不足都能被显式记录，便于审查。

质量收益：

- 问题更像对应物种真实养殖户问诊。
- 回答更符合对应物种临床处置逻辑。
- 裁判评分更加公平，不再用猪病标准评估鸡病。
- 处方和食品安全边界更稳，减少跨物种错误外推。

工程收益：

- 公共代码收敛。
- 物种差异清晰。
- 文档留痕完整。
- 后续扩展成本明显下降。
