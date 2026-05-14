# LLM Wiki 生成评估链路修复说明

## 背景

真实 API 运行 10 条 production 样本后，确认主流程已经调用 LLM Wiki，但暴露出三个生产审计问题：

1. CSV 没有持久化 Wiki 证据字段，必须依赖快照反查。
2. 个别样本目标疾病与 `diagnosis` 主诊断不一致，仍被评估为 `pass`。
3. `rule_fatal_risk`、裁判 `fatal_risk` 和日志汇总的致命风险口径不统一。

## 修复内容

### 1. Wiki 审计字段持久化

新增 `src/chicken_data_synthesis/infrastructure/knowledge/audit.py`，从每次注入的 `llm_wiki_context` 中提取：

- `wiki_dir`
- `wiki_fact_count`
- `wiki_page_count`
- `wiki_context_query`
- `wiki_evidence_status_counts`
- `wiki_evidence_source_ids`
- `wiki_context_chars`

`src/chicken_data_synthesis/infrastructure/persistence/csv_artifacts.py` 已将这些字段写入最终 CSV。

### 2. 目标疾病一致性门禁

`src/chicken_data_synthesis/infrastructure/prompts/builders.py` 为生成阶段追加“目标疾病一致性约束”：

- `diagnosis` 的主要诊断必须显式写出目标疾病；
- 如果使用同义名、旧称或更具体分类，必须说明与目标疾病的关系；
- 如果症状更像其他疾病，目标疾病必须进入鉴别诊断并解释原因。

`src/chicken_data_synthesis/application/services/case_processing.py` 增加最终质量门禁：

- `target_disease_in_diagnosis`
- `target_disease_mismatch`

若目标疾病未在诊断中出现，最终 `final_label` 自动降为 `review`，诊断准确性分数上限收紧为 20。

### 3. 致命风险口径统一

最终指标新增：

- `fatal_risk`
- `rule_fatal_risk`

最终风险由以下任一来源触发：

- 规则层 `rule_base_result.fatal_risk`
- 裁判 A `fatal_risk`
- 裁判 B `fatal_risk`

如果最终风险为真且原标签为 `pass`，标签自动降为 `review`。进度汇总和 CSV 均改用统一后的最终风险口径。

### 4. Wiki 检索 query 加强

`scripts/master_chicken_data.py` 新增 `build_wiki_query()`，确保生成、评估、仲裁、规则检查的 Wiki 检索 query 都包含目标疾病名，降低检索偏移。

## 验证

已通过：

```bash
python -m pytest -q
python -m compileall -q main.py src scripts llm_foundation deepeval_integration tests
chicken-wiki --json lint --strict
```

基于真实 API 旧快照重算 CSV 行后：

- Wiki 审计字段已出现；
- 目标疾病不一致样本被标记为 `review`；
- 规则/裁判风险进入 `final_fatal_risk`；
- `pass` 标签不会覆盖目标不一致或致命风险。

## 后续建议

后续再次运行真实 API 时，建议使用：

```bash
python main.py --mode production --samples 10 --parallel 2 --evaluation-mode legacy
```

运行后检查最终 CSV 中以下字段：

- `target_disease_in_diagnosis`
- `target_disease_mismatch`
- `final_fatal_risk`
- `wiki_evidence_source_ids`
- `wiki_evidence_status_counts`

这些字段应作为生产数据入库前的审计门。
