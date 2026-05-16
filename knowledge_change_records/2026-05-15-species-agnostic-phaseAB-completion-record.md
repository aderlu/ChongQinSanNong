# Phase A And Phase B Completion Record

日期：2026-05-15

关联文档：

- [2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md)
- [2026-05-15-species-agnostic-wiki-pipeline-execution-master-plan.md](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-execution-master-plan.md)
- [2026-05-15-species-agnostic-phaseA-inventory.md](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-phaseA-inventory.md)
- [2026-05-15-species-agnostic-phaseB-contracts-and-compat.md](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-phaseB-contracts-and-compat.md)

## 一、结论

Phase A 与 Phase B 已按“低风险接入、默认保 swine、不改 54 字段契约”的原则直接落地，并完成基础验收。

当前可以进入 Phase C，但前提仍然是继续保持：

1. 不重写主链路核心生成逻辑。
2. 不漂移 `baseline_validation_common.py` 的 54 字段定义。
3. 不跳过默认链路中的 `Phase 14b`。

## 二、Phase A 已完成内容

1. 形成 swine/chicken 当前链路与复用边界盘点文档。
2. 形成 machine-readable inventory JSON。
3. 冻结 baseline 54 字段口径。
4. 冻结 baseline runner 默认顺序：
   `Phase 14 -> Phase 14b -> Phase 15 -> Phase 18`
5. 明确 `Phase 14b` 是主链路步骤，不是可选附属步骤。

## 三、Phase B 已完成内容

1. 新增公共契约层目录：
   `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\common`
2. 新增公共模块：
   `species_config.py`
   `manifest_contract.py`
   `path_context.py`
   `runtime_indexes.py`
   `model_routing.py`
3. 新增 baseline 兼容层：
   `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\baseline_validation\orchestration_compat.py`
4. 新增 species 配置：
   `swine.yaml`
   `chicken.yaml`
5. 为旧入口补入兼容参数：
   `phase12_plan_samples_from_wiki.py`
   `phase14b_naturalize_grounded_answers.py`
   `baseline_validation/run_baseline_experiment.py`
6. 新增基础测试：
   `D:\XF-ChongQin\ai-\tests\test_species_config_loader.py`
   `D:\XF-ChongQin\ai-\tests\test_baseline_field_contract.py`
   `D:\XF-ChongQin\ai-\tests\test_legacy_entrypoint_compatibility.py`

## 四、验收命令

```powershell
C:\Users\admin\AppData\Local\Python\bin\python.exe -m pytest D:\XF-ChongQin\ai-\tests\test_species_config_loader.py D:\XF-ChongQin\ai-\tests\test_baseline_field_contract.py D:\XF-ChongQin\ai-\tests\test_legacy_entrypoint_compatibility.py D:\XF-ChongQin\ai-\tests\test_swine_wiki_baseline_validation.py -q
```

```powershell
C:\Users\admin\AppData\Local\Python\bin\python.exe D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase12_plan_samples_from_wiki.py --help
```

```powershell
C:\Users\admin\AppData\Local\Python\bin\python.exe D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14b_naturalize_grounded_answers.py --help
```

```powershell
C:\Users\admin\AppData\Local\Python\bin\python.exe D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\baseline_validation\run_baseline_experiment.py --help
```

## 五、验收结果

1. `12 passed in 0.13s`
2. `phase12_plan_samples_from_wiki.py` 旧入口可正常解析新增参数。
3. `phase14b_naturalize_grounded_answers.py` 旧入口可正常解析新增参数。
4. `run_baseline_experiment.py` 旧入口可正常解析新增参数。
5. `--species`、`--species-config`、`--wiki-root` 已进入兼容层，不影响默认 swine 行为。

## 六、剩余风险

1. 工作区当前存在大量与本任务无关的脏文件和新增产物，后续阶段不能用覆盖式改写。
2. `phase12_plan_samples_from_wiki.py` 与 `phase14b_naturalize_grounded_answers.py` 在本次落地前就已有较多在研修改，后续继续改这两个文件必须先按现状审读再补改。
3. 当前验证覆盖的是契约层、入口兼容层和 baseline 字段冻结，不等于已经完成 chicken 真实运行闭环。

## 七、阶段结论

1. Phase A：完成，验收通过，允许进入下一阶段。
2. Phase B：完成，验收通过，允许进入下一阶段。
3. 下一阶段应进入 Phase C：先生成 chicken runtime 五件套，再继续后续 species-aware 主链改造。
