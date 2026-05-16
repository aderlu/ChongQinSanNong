# Phase B Contracts And Compatibility

日期：2026-05-15

## 目标

在不重写核心生成逻辑的前提下，落地 Phase B 的最小可执行版本：

1. 公共契约模块
2. swine/chicken species 配置
3. baseline orchestration compatibility 壳
4. 基础测试

## 本阶段落地内容

1. 新增 `tools/pipeline/common/`
2. 新增 `species_config.py`
3. 新增 `manifest_contract.py`
4. 新增 `path_context.py`
5. 新增 `runtime_indexes.py`
6. 新增 `model_routing.py`
7. 新增 `tools/pipeline/baseline_validation/orchestration_compat.py`
8. 新增 `species_configs/swine.yaml`
9. 新增 `species_configs/chicken.yaml`
10. 新增基础测试：
   - `test_species_config_loader.py`
   - `test_baseline_field_contract.py`
   - `test_legacy_entrypoint_compatibility.py`

## 本阶段策略

本阶段不直接重写 Phase 12/14b/baseline runner 主体逻辑，只先补齐不打断现有流程的兼容层与契约层。

## 核心约束

1. 默认 species 仍为 `swine`
2. `54` 字段契约不变
3. 旧入口不删除
4. `swine_runtime_selection` 仍可通过兼容方式映射到统一 `model_routing`

## 验收预期

1. species 配置可加载
2. baseline 字段契约有测试保护
3. run manifest 兼容层可以记录 species、入口别名、model routing 来源

## 是否允许继续进入后续 Phase B 代码接线

允许。
