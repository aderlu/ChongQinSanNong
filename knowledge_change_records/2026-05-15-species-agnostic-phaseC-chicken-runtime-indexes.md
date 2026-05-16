# Phase C Chicken Runtime Indexes

日期：2026-05-15

关联文档：

- [2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-refactor-plan.md)
- [2026-05-15-species-agnostic-wiki-pipeline-execution-master-plan.md](D:\XF-ChongQin\knowledge_change_records\2026-05-15-species-agnostic-wiki-pipeline-execution-master-plan.md)

## 一、阶段目标

为 chicken Wiki 生成 Phase 12 可消费的 runtime 五件套，在不调用 LLM、不改主生成链路脚本的前提下，补齐最小运行底座。

## 二、本阶段落地内容

1. 新增独立构建脚本：
   [build_species_runtime_indexes.py](D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\build_species_runtime_indexes.py)
2. 新增测试：
   [test_manifest_contract_mapping.py](D:\XF-ChongQin\ai-\tests\test_manifest_contract_mapping.py)
   [test_runtime_index_generation.py](D:\XF-ChongQin\ai-\tests\test_runtime_index_generation.py)
3. 生成 chicken runtime 五件套：
   [runtime_core_manifest.json](D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\runtime_core_manifest.json)
   [runtime_exclude_patterns.json](D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\runtime_exclude_patterns.json)
   [gold_dataset_readiness_index.csv](D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\gold_dataset_readiness_index.csv)
   [drug_gold_role_index.csv](D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\drug_gold_role_index.csv)
   [exporter_hard_block_rules.json](D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\exporter_hard_block_rules.json)
4. 生成验证报告：
   [runtime_manifest_validation_report.md](D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative\exports\runtime_manifest_validation_report.md)

## 三、实现原则

1. 不修改 `phase12_plan_samples_from_wiki.py`。
2. 不修改 `phase14b_naturalize_grounded_answers.py`。
3. 仅复用现有 `common/` 契约层和 chicken 现有 `exports/*.csv/json`。
4. 对弱证据、缺字段和高风险主题采用显式保守降级。

## 四、验证命令

```powershell
C:\Users\admin\AppData\Local\Python\bin\python.exe D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\build_species_runtime_indexes.py --wiki-root D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative --species chicken
```

```powershell
C:\Users\admin\AppData\Local\Python\bin\python.exe -m pytest D:\XF-ChongQin\ai-\tests\test_manifest_contract_mapping.py D:\XF-ChongQin\ai-\tests\test_runtime_index_generation.py -q
```

## 五、验证结果

构建输出摘要：

```json
{
  "species": "chicken",
  "wiki_root": "D:\\XF-ChongQin\\ai-\\knowledge\\llm_wiki_chicken_authoritative",
  "entries": 137,
  "gold_rows": 60,
  "drug_gold_rows": 44,
  "status_counts": {
    "blocked": 60,
    "generation_ready_limited": 42,
    "boundary_only": 7,
    "eval_ready": 25,
    "retrieval_only": 3
  }
}
```

测试结果：

- `3 passed in 0.17s`

验证报告中的关键统计：

- `generation_ready_limited: 42`
- `retrieval_only: 3`
- `boundary_only: 7`
- `blocked: 60`

## 六、有效性判断

本阶段已经达成 Phase C 的既定目标：

1. chicken `exports` 下已经具备完整 runtime 五件套。
2. 每条 manifest 记录都具备明确 `task_use_status`。
3. 高风险药物、休药期、残留、监管动作仍默认保守，不会被误提升为正向可生成。
4. 整个过程只消费本地索引，不依赖联网或 LLM。

## 七、剩余风险

1. 当前保守降级较强，许多 chicken disease 页仍被压在 `blocked` 或 `retrieval_only`，这说明后续要进入 Phase D/E 前，不能假设 chicken 已具备 swine 同等级生成成熟度。
2. `eval_ready` 当前主要存在于 rule 或边界类条目，不代表 chicken 已具备完整正向训练集导出条件。
3. pytest 结束时出现了 Windows 临时目录清理权限警告，但不影响测试通过和本阶段产物有效性。

## 八、阶段结论

1. Phase C：完成，验收通过。
2. 允许进入下一阶段。
3. 下一阶段应进入 Phase D，在继续保持不覆盖现有主流程在研改动的前提下，开始做生成链 species-aware 化。
