# Phase 8/9 规则卡加固、索引图谱重建与检索冒烟测试执行记录

Date: 2026-05-09 20:43

Target: `ai-/knowledge/llm_wiki_swine_authoritative`

## 1. 修改目标和范围

本次执行 Phase 8 和 Phase 9：

- Phase 8：补强高风险规则卡、评估 rubrics 和 exporter hard-block 门禁，确保微调、评估和生成遵守同一套安全边界。
- Phase 9：重建核心索引、runtime manifest、knowledge graph，并完成检索 smoke test，确认默认检索不命中 raw、issues、graph、巨大矩阵。

涉及范围：

- `wiki/rule_cards/`
- `wiki/synthesis/`
- `wiki/diseases/`、`wiki/drugs/`、`wiki/comparisons/`、`wiki/syndromes/` 的页面级 citation gate 锚点
- `exports/`
- `issues/`
- `wiki/graph-data.json`
- `wiki/knowledge-graph.md`
- `wiki/knowledge-graph.html`
- `tools/`

## 2. 修改前存在的问题

修改前主要问题：

- 执行计划要求的 `RC-EVAL-RUBRIC-001` 不存在。
- 现有 synthesis 页面已经引用 `RC-SYNTHESIS-SCOPE-001`、`RC-REGULATORY-CURRENT-001`、`RC-EVAL-RUBRIC-001`，但对应规则卡文件缺失，形成“引用存在、规则卡不存在”的治理缺口。
- `exports/rule_card_index.csv` 只有 18 张左右旧规则卡，不能覆盖 Phase 8 所需核心 rubrics。
- 缺少 exporter/evaluator 的机器可读 hard-block 规则配置。
- 部分 runtime 页面没有显式 `RC-CITATION-001` 页面锚点，不利于后续样本导出统一检查 source/fact/rule provenance。
- `wiki/knowledge-graph.md` 和 `wiki/knowledge-graph.html` 标题仍写 `Chicken Disease LLM Wiki Graph`，图谱 metadata 停在 2026-05-07，存在领域漂移和派生产物过期问题。
- Phase 9 缺少当前 runtime allowlist 视角下的检索 smoke test 报告。

## 3. 修改前相关代码、索引和知识文件状态

修改前：

- `wiki/rule_cards/` 中不存在：
  - `RC-EVAL-RUBRIC-001.md`
  - `RC-SYNTHESIS-SCOPE-001.md`
  - `RC-REGULATORY-CURRENT-001.md`
- `wiki/synthesis/swine_answer_evaluation_rubric.md` 等页面引用了上述规则卡 ID，但只能作为文本引用，无法通过 rule card index 和 manifest 解析为稳定规则页。
- `wiki/graph-data.json` metadata 显示旧统计：diseases 73、drugs 76、sources 145、facts 1465，与当前知识库 sources 219、标准化 facts 2193 不一致。
- `knowledge-graph.md/html` 仍带 Chicken 标题。
- `runtime_core_manifest.json` 上一阶段为 198 条；新增规则卡后需要重新构建。

## 4. 本次更新或新增了什么代码

新增代码：

- `tools/phase8_rule_card_and_exporter_gate.py`
  - 重新扫描 `wiki/rule_cards/*.md` 生成 `exports/rule_card_index.csv`。
  - 生成 `exports/exporter_hard_block_rules.json`。
  - 检查核心规则卡缺失数。
  - 检查 runtime 页面是否缺少必要规则卡锚点。
  - 输出 `issues/phase8_rule_card_exporter_gate_2026-05-09.json/md`。

- `tools/phase8_apply_runtime_citation_anchors.py`
  - 对 disease/drug/comparison/syndrome runtime 页面补入 `RC-CITATION-001` 页面级来源引用门禁。
  - 仅新增规则锚点说明，不改实体事实。
  - 输出 `issues/phase8_runtime_citation_anchors_2026-05-09.json/md`。

- `tools/phase9_rebuild_indexes_graph_smoke.py`
  - 规范化重写核心索引 CSV。
  - 基于 `runtime_core_manifest.json` 和 `knowledge_facts_status_index.json` 重建 runtime graph。
  - 重建 `wiki/graph-data.json`、`wiki/knowledge-graph.md`、`wiki/knowledge-graph.html`。
  - 执行 5 条检索 smoke test。
  - 输出 `issues/phase9_index_graph_rebuild_2026-05-09.json` 和 `issues/runtime_retrieval_smoke_test_2026-05-09.json/md`。

## 5. 本次新增或整理的知识文件

新增规则卡：

- `wiki/rule_cards/RC-EVAL-RUBRIC-001.md`
  - 定义 `unsupported_dose`、`unsupported_withdrawal_mrl`、`unsupported_regulatory_action`、`single_test_causality_overclaim`、`no_source_citation`、`source_level_mismatch` 等评估硬失败。

- `wiki/rule_cards/RC-SYNTHESIS-SCOPE-001.md`
  - 明确 synthesis 页面只能作为策略、路由、评估、拒答和来源升级页面，不得创造新的疾病、药物、剂量、休药期、MRL、残留、食品安全或监管事实。

- `wiki/rule_cards/RC-REGULATORY-CURRENT-001.md`
  - 明确中国监管、检疫、扑杀、调运、强制报告、禁停用药、休药期、MRL、残留合格、肉品可食和食品安全结论必须使用当前 A0 官方或标签级来源。

整理 synthesis 页面：

- `wiki/synthesis/swine_case_generation_context.md`
- `wiki/synthesis/swine_regulatory_blocking_rules_china.md`
- `wiki/synthesis/swine_drug_and_withdrawal_boundary.md`

整理内容：

- 将 sources 补齐到相关 rule cards。
- 将旧的 `HUMAN_REVIEWED` / `NEEDS_REVIEW` 正文表达改为 `source_status=source_anchored`、`fact_validity=valid` 和 legacy audit status 表达。
- 明确所有样本必须遵守 `RC-CITATION-001`。

页面级补锚点：

- 对 176 个 runtime disease/drug/comparison/syndrome 页面补入 `Source citation gate / Phase 8` 小节。
- 该小节只声明 `RC-CITATION-001`、task use、gold dataset role 和 legacy 字段不作为门槛，不新增生物医学事实。

## 6. 本次重建或新增的导出文件

新增或重建：

- `exports/rule_card_index.csv`
- `exports/exporter_hard_block_rules.json`
- `exports/runtime_core_manifest.json`
- `exports/runtime_exclude_patterns.json`
- `exports/runtime_core_manifest_summary.md`
- `exports/gold_dataset_readiness_index.csv`
- `exports/drug_gold_role_index.csv`
- `exports/source_authority_status_index.csv`
- `exports/knowledge_facts_status_index.json`
- `wiki/graph-data.json`
- `wiki/knowledge-graph.md`
- `wiki/knowledge-graph.html`
- `issues/phase8_rule_card_exporter_gate_2026-05-09.json`
- `issues/phase8_rule_card_exporter_gate_2026-05-09.md`
- `issues/phase8_runtime_citation_anchors_2026-05-09.json`
- `issues/phase8_runtime_citation_anchors_2026-05-09.md`
- `issues/phase9_index_graph_rebuild_2026-05-09.json`
- `issues/runtime_retrieval_smoke_test_2026-05-09.json`
- `issues/runtime_retrieval_smoke_test_2026-05-09.md`

核心索引规范化重写：

- `source_index.csv`: 219 rows, missing_paths 0
- `disease_index.csv`: 73 rows, missing_paths 0
- `drug_page_index.csv`: 84 rows, missing_paths 0
- `rule_index.csv`: 449 rows, missing_paths 0
- `rule_card_index.csv`: 21 rows, missing_paths 0
- `comparison_index.csv`: 14 rows, missing_paths 0
- `synthesis_index.csv`: 24 rows, missing_paths 0

## 7. 修改后解决了什么问题

修改后：

- Phase 8 要求的核心规则卡全部存在，`missing_required_cards=[]`。
- rule card index 已更新为 21 张规则卡，其中 hard-block cards 为 11。
- runtime 页面必要规则锚点缺失数为 0。
- exporter/evaluator 已有机器可读硬阻断配置：
  - `unsupported_dose`
  - `unsupported_withdrawal_mrl`
  - `unsupported_regulatory_action`
  - `single_test_causality_overclaim`
  - `no_source_citation`
  - `source_level_mismatch`
- 图谱派生产物已经从 Chicken 标题修正为 Swine runtime graph。
- 新图谱基于当前 runtime manifest 和标准化 fact status index，避免使用旧图谱噪声。
- 检索 smoke test 确认默认运行时检索不命中 raw、issues、graph、treatment_matrix 或 prescription_matrix。

## 8. 预计更新效果

对生成：

- 无来源处方、无来源剂量/疗程、无来源休药期/MRL、无来源监管处置会被 hard-block 规则拦截。
- synthesis 页面只能用于策略和路由，不会被误当作事实源。

对评估：

- 评估器可以用 `RC-EVAL-RUBRIC-001` 统一判断无来源、过度外推、单次检测因果过度解释、来源等级不匹配。
- 黄金数据集评估样本更容易覆盖药物越界、监管越界和引用缺失陷阱。

对检索：

- runtime graph 和 smoke test 都基于 manifest allowlist，不把 raw、issues、graph、巨大矩阵放入默认检索。
- 症状、疾病、药物、监管和诊断解释类查询都能召回相应 disease/drug/rule_card/comparison/syndrome 页面。

对黄金数据集生产：

- `exporter_hard_block_rules.json` 可作为导出前门禁配置。
- `rule_card_index.csv` 可直接用于检查每条样本是否引用了必要规则卡。
- `gold_dataset_readiness_index.csv` 和 `drug_gold_role_index.csv` 延续 Phase 6/7 分层，并已随 manifest 重新生成。

## 9. 验证命令和结果

所有命令均在 PowerShell 下设置 UTF-8 后执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
```

Phase 8：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase8_apply_synthesis_regulatory_guardrails.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase8_apply_runtime_citation_anchors.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase8_rule_card_and_exporter_gate.py
```

结果：

- rule_card_count: 21
- hard_block_count: 11
- missing_required_cards: []
- runtime_pages_missing_rule_anchors: 0
- synthesis core anchors missing: 0

Phase 9：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase6_7_review_status_and_gold_dataset.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\standardize_source_fact_status.py
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase9_rebuild_indexes_graph_smoke.py
```

结果：

- runtime manifest entries: 204
- manifest missing_paths: 0
- index missing paths: 0
- graph nodes: 2550
- graph links: 3127
- facts_in_graph: 2193
- retrieval smoke test passed: true

通用验收：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
```

- entries_checked: 204
- high: 0
- medium: 0

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

- readiness_score: 99
- missing_paths: 0
- bad_fact_tables: []
- missing_rule_cards: []
- missing_synthesis: []

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

- text_files_scanned: 2310
- runtime_manifest_paths_loaded: 204
- encoding_ok: 2298
- decode_or_replacement_damage: 3
- mojibake_like_content: 0
- minor_mojibake_signal: 9
- runtime_damaged_count: 0

额外检查：

- 图谱文件 `graph-data.json`、`knowledge-graph.md`、`knowledge-graph.html` 中不再出现 `Chicken Disease`、`chicken disease`、`鸡病`、`产蛋鸡`。
- `runtime_core_manifest.json` 中 `"evidence_status"` 主字段计数为 0。
- `gold_dataset_readiness_index.csv` 中 `missing_critical_fields` 计数为 0。
- 非 A0 药物页 `positive_generation_allowed=true` 计数为 0。

## 10. 仍然存在的风险和下一步待办

仍然存在：

- 非 runtime 文件仍有 3 个 decode/replacement damage 和 9 个 minor mojibake signal；runtime_damaged_count=0，本次未处理 raw/历史材料。
- `knowledge_facts.json` 原始事实表仍保留历史字段，当前用于门禁和图谱的是标准化后的 `knowledge_facts_status_index.json`。
- 部分旧批处理脚本仍包含 `HUMAN_REVIEWED`、`NEEDS_REVIEW` 字符串作为历史构建逻辑，当前运行时和 exporter 门禁已不依赖这些字段。

下一步建议：

- Phase 10 增加猪病专用 pytest，覆盖 runtime manifest、denylist、gold_dataset_readiness_index、drug_gold_role_index、exporter_hard_block_rules 和检索 smoke test。
- Phase 11 开始小批量黄金数据集试生产，并用 `RC-EVAL-RUBRIC-001` 和 `exporter_hard_block_rules.json` 做人工抽检前置过滤。
