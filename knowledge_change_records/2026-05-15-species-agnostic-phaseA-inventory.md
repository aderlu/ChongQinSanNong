# Phase A Inventory And Baseline Freeze

日期：2026-05-15

## 目标

冻结当前 swine/chicken 真实链路、54 字段契约、Phase 14b 主链路地位，以及 `chicken_data_synthesis` 的可复用边界。

## 当前真实结论

1. swine 当前正式链路包含 `Phase 14b`，不是可选步骤。
2. baseline `54` 字段由 `tools/pipeline/baseline_validation/baseline_validation_common.py` 统一定义。
3. `run_baseline_experiment.py` 当前真实默认顺序包含：
   `Phase 14 -> Phase 14b -> Phase 15 -> Phase 18`
4. chicken wiki 当前缺少 runtime 五件套。
5. `chicken_data_synthesis` 可复用 `llm runtime`、`evaluation normalizers`、`snapshot persistence`，但其部分命名仍带 swine 历史残留。

## 冻结项

1. `STANDARD_SAMPLE_FIELDS = 51`
2. `COMPARISON_KEY_FIELDS = 3`
3. `STANDARD_COMPARISON_FIELDS = 54`
4. `Phase 14b` 不允许在默认链路中被跳过
5. `swine` 仍为默认行为

## 机器可读清单

对应 JSON：

[2026-05-15-species-agnostic-phaseA-inventory.json](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-phaseA-inventory.json)

## 是否允许进入 Phase B

允许。

