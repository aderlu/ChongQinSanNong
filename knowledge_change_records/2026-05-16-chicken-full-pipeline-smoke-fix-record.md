# 鸡病 Wiki 全链路真实 API Smoke 阻断点修复记录

日期：2026-05-16

## 一、修改背景

真实 API 运行鸡病 Wiki 5 条 smoke 后，Phase 12、13、14、14b、15、18、16 均能产出文件，但不能判定为可验收全流程。

暴露的问题：

1. 鸡病 case variables 出现“哺乳仔鸡”等猪病阶段污染。
2. Phase 18 arbiter prompt 仍出现 `realistic swine consultation SFT lens`。
3. Phase 16 production CSV 中 `assistant_answer` 缺失，真实回答留在 `stage_2_grounded.clinical_answer`。
4. Phase 18 模型路由虽然入口支持 `--species chicken`，但内部仍按 swine 路由解析。

## 二、修改前代码状态

### 1. `consultation_case_variables.py`

鸡病阶段池中包含：

- `哺乳仔鸡`
- `育成鸡群`
- `商品鸡`

这些表达不适合作为鸡病问诊阶段，尤其 `哺乳仔鸡` 是明显物种污染。

### 2. `wiki_first_judge_prompts.py`

裁判 prompt 和 rubric 仍有大量 swine 表达，包括：

- `realistic swine consultation`
- `swine veterinary knowledge`
- `pig stage`
- `swine consultation tone`

### 3. `phase18_dual_judge_and_arbitrate.py`

入口已有 `--species`，但 `model_config_for()` 和 `model_chain()` 内部仍使用 `resolve_model_routing(config, species="swine")`。

fallback 的中文 dimension reasons 仍写死猪场、猪群、猪只阶段。

### 4. `phase16_export_layered_training_sets.py`

`answer_text_for()` 已能读取 `stage_2_grounded.clinical_answer`，但 `PRODUCTION_CSV_FIELDS` 中没有 `assistant_answer`，production CSV 只把回答写入 `diagnosis`，导致审查时 `assistant_answer` 为空。

## 三、本次修改文件

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\consultation_case_variables.py`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\wiki_first_judge_prompts.py`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase18_dual_judge_and_arbitrate.py`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py`

## 四、修改内容

### 1. 修复鸡病阶段和现场线索

将鸡病阶段调整为：

- `雏鸡`
- `育雏鸡`
- `育成鸡`
- `后备鸡`
- `产蛋鸡`
- `肉鸡`
- `种鸡`

同时把鸡病现场线索改为更符合鸡场问诊：

- `饮水变化`
- `冠脸发紫或发白`
- `产蛋率下降`
- `采食和饮水有没有明显变化`
- `粪便颜色和稀稠有没有变化`

### 2. Phase 18 prompt 按物种渲染

新增 prompt 渲染逻辑：

- 从 sample 读取 `species`、`species_cn`、`farm_context_cn`、`animal_group_label`、`production_stage`。
- chicken 样本将 swine/pig/herd 等表达替换为 chicken/flock/鸡场/鸡群等语义。
- arbiter prompt 不再出现 swine lens。

### 3. Phase 18 模型路由使用当前 species

新增运行期 species 上下文：

- `RUN_SPECIES`
- `set_run_species(args.species)`
- `current_species()`

`model_config_for()` 和 `model_chain()` 改为使用当前 species 调用 `resolve_model_routing()`，不再固定 swine。

### 4. Phase 18 fallback 中文原因按 chicken 渲染

当 `--species chicken` 时：

- `judge_a_dimension_reasons()`
- `judge_b_dimension_reasons()`
- `arbiter_dimension_reasons()`

返回鸡场/鸡群/日龄用途/采食饮水/粪便/休药期/弃蛋期等语境。

### 5. Phase 16 production CSV 增加 `assistant_answer`

在 `PRODUCTION_CSV_FIELDS` 中新增 `assistant_answer`，并将其填充为：

- `stage_2_grounded.clinical_answer`
- fallback 到 `stage_2_grounded.answer`

## 五、预计效果

修复后预期：

1. 鸡病问诊场景不再出现“哺乳仔鸡”等猪病污染。
2. Phase 18 arbiter 和 judge prompt 不再以 swine consultation lens 评估 chicken。
3. Phase 18 模型路由能够读取 chicken runtime selection。
4. production CSV 中可直接审查 `assistant_answer`。
5. 鸡病全链路 smoke 的可用性判断更接近真实状态。

## 六、已执行的本地检查

已执行 Python 语法检查：

```text
py -m py_compile consultation_case_variables.py wiki_first_judge_prompts.py phase18_dual_judge_and_arbitrate.py phase16_export_layered_training_sets.py
```

已执行结构检查：

- chicken case variables 不再生成 `哺乳仔鸡`。
- chicken arbiter prompt 中不再包含 `swine`。

## 七、后续验证

已重新运行鸡病真实 API 全链路：

1. Phase 12
2. Phase 13
3. Phase 14 real-api
4. Phase 14b
5. Phase 15
6. Phase 18 real judges
7. Phase 16 export

## 八、真实 API 验证结果

### 1. 5 条 smoke：`20260516_chicken_smoke_realapi_5_fix1`

运行结果：

- Phase 12、13、14、14b、15、18、16 均完成。
- Phase 15：5/5 通过硬门控。
- Phase 18：`accepted=1`，`review=3`，`rejected=1`。
- Phase 16：生成 production/main/train_ready 等训练集文件。
- production CSV 已包含 `assistant_answer`，且回答非空。

主要产物：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\generated_samples\naturalized_samples_20260516_chicken_smoke_realapi_5_fix1.jsonl`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\semantic_evaluated_samples\semantic_evaluated_samples_20260516_chicken_smoke_realapi_5_fix1.jsonl`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\training_sets\chicken_wiki_training_dataset_production_20260516_chicken_smoke_realapi_5_fix1.csv`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\training_sets\chicken_wiki_training_main_20260516_chicken_smoke_realapi_5_fix1.csv`

该轮发现新的隐性问题：

- generated sample 的 `run_manifest.wiki_root` 仍指向 swine wiki 根目录。
- skeleton 的 `required_case_slots` 仍包含 `pig_stage_or_group`。

这两个问题不会一定出现在用户可见回答里，但会污染审计字段和后续多物种复用判断，因此继续修复 Phase 13/14。

### 2. 隐性污染修复

新增修复：

- `phase13_build_answer_skeletons.py`
  - 增加 `--species` 和 `--species-config`。
  - `case_generation_profile_for()` 按物种生成 case slots。
  - chicken 使用 `production_stage_or_group`，不再使用 `pig_stage_or_group`。
- `phase14_generate_two_stage_samples.py`
  - `generate_sample()`、`generate_samples()` 显式透传 `wiki_root`。
  - `run_manifest["wiki_root"]` 使用当前 chicken wiki 根目录，不再写入 swine 根目录。

### 3. 2 条回归 smoke：`20260516_chicken_smoke_realapi_2_fix2`

运行结果：

- Phase 12、13、14、14b、15、18、16 均完成。
- Phase 18：`accepted=1`，`review=1`，`rejected=0`。
- Phase 16：`accepted=1`，`review=1`，`rejected=0`。
- production CSV：2 行，103 个字段，包含 `assistant_answer`，2/2 非空。
- main CSV：2 行，115 个字段，包含 `assistant_answer`，2/2 非空。

污染检查结果：

- production CSV 未检出：`猪场`、`猪群`、`猪舍`、`仔猪`、`母猪`、`保育猪`、`育肥猪`、`pig_stage_or_group`、`llm_wiki_swine_authoritative`、`realistic swine`。
- main CSV 未检出上述污染词。
- semantic JSONL 未检出上述污染词。
- naturalized JSONL 未检出上述污染词。

主要产物：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\generated_samples\naturalized_samples_20260516_chicken_smoke_realapi_2_fix2.jsonl`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\semantic_evaluated_samples\semantic_evaluated_samples_20260516_chicken_smoke_realapi_2_fix2.jsonl`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\training_sets\chicken_wiki_training_dataset_production_20260516_chicken_smoke_realapi_2_fix2.csv`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\training_sets\chicken_wiki_training_main_20260516_chicken_smoke_realapi_2_fix2.csv`

## 九、最终检查

已执行 Python 编译检查，覆盖本次修改文件：

```text
py -m py_compile consultation_case_variables.py phase13_build_answer_skeletons.py phase14_generate_two_stage_samples.py phase16_export_layered_training_sets.py phase18_dual_judge_and_arbitrate.py wiki_first_judge_prompts.py
```

结果：通过。

已执行 UTF-8/乱码标记检查：

- 未发现新增文档或产物乱码。
- 命中的乱码形态字符串来自 `MOJIBAKE_RE` 防护正则，是用于检测乱码的主动规则，不是实际内容污染。

## 十、当前结论

鸡病 Wiki 当前已经可以基于真实 API 跑通生成、自然化、硬门控、双裁判/仲裁评估、训练集导出的完整 smoke 链路。

本次修复后，阻断全流程验收的关键问题已解决：

1. 鸡病 case variables 不再使用猪病阶段。
2. Phase 18 不再用 swine lens 评估 chicken。
3. Phase 18 模型路由按 `--species chicken` 解析。
4. Phase 16 production CSV 可以直接审查 `assistant_answer`。
5. Phase 13/14 审计字段中的 swine wiki root 和 `pig_stage_or_group` 隐性污染已修复。

剩余边界：

1. 当前验证是 5 条和 2 条真实 API smoke，不代表 500 条规模稳定性已经完成。
2. 当前产物是训练集导出 CSV，不是 54 字段 baseline comparison CSV；54 字段对比表仍属于 baseline runner 的验收范围。
3. 鸡病证据深度仍可能偏薄，较大规模运行时 review 比例可能偏高，需要后续结合鸡病 wiki 覆盖度和裁判结果继续调优。
