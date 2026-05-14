# 猪病 LLM Wiki 知识库治理与黄金数据集准备工作汇报

日期：2026-05-09  
汇报对象：项目 Leader  
范围：`ai-/knowledge/llm_wiki_swine_authoritative`

## 一、总体目标

本轮工作的总目标，是把猪病 LLM Wiki 从“可检索的知识文件集合”治理为“可进入生产、评估和黄金数据集试生产的受控知识库”。

具体来说，我们在做一件事：围绕猪病、药物、规则卡、来源、事实、综合监管页面，建立一套可审计、可回归、可门禁的运行时知识体系。目标不是单纯增加内容，而是解决 LLM 使用知识库时最容易出问题的几个核心风险：

1. 检索层混入历史构建材料、raw 文档、issues、图谱和大矩阵，导致模型召回噪声。
2. 药物页和疾病页正文过长，包含候选事实、剂量、疗程、休药期、MRL、处方候选等高风险内容，容易被模型误当成可执行建议。
3. `HUMAN_REVIEWED`、`NEEDS_REVIEW` 等历史复核字段被误当作可用性门槛，真正应该判断的来源状态、事实有效性、权威等级和任务用途不够明确。
4. 部分根文档仍存在 chicken/swine 领域漂移，schema、README、图谱、维护指南不能准确反映当前猪病知识库状态。
5. 黄金数据集生产前缺少统一门禁，无法稳定判断哪些页面能训练、哪些只能评估、哪些只能做 negative trap 或检索路由。

本轮解决思路是：先冻结基线，再建立运行时契约；先把高风险内容从默认检索层迁出，再用规则卡和状态字段约束生成、评估和导出；最后用索引、图谱、冒烟测试、pytest 和小批量 pilot 数据集验证整套链路。

最终结果：

- runtime manifest 从 198 条扩展到 204 条，缺失路径始终为 0。
- runtime 编码损坏数保持为 0。
- 幻觉风险审计最终为 high: 0、medium: 0。
- readiness score 保持 99。
- rule cards 增至 21 张，其中 hard-block cards 11 张。
- 图谱重建为 2550 个节点、3127 条边，事实数 2193。
- 猪病 runtime 专用测试 8 passed，历史兼容测试 27 passed。
- 试生产黄金数据集 pilot 32 条，provenance 完整率 1.0，高风险越界 0。

## 二、阶段一：基线冻结与运行时治理契约建立

本阶段目标，是先回答“现在知识库是什么状态、哪些内容能进 runtime、用什么字段判断可用性”。为什么要先做这一步，是因为后续会批量修改实体页、schema、manifest 和导出文件，如果没有基线和状态契约，后续无法证明修改是否引入路径缺失、乱码、事实表异常或运行时边界漂移。

原来存在的问题包括：

- `purpose.md`、`index.md`、README、图谱等根文档仍残留 chicken disease 表述。
- `.wiki-schema.md` 对 source、fact、runtime、gold dataset 的状态字段定义不足。
- 缺少可重复运行的编码完整性审计，无法稳定说明 runtime 是否存在中文乱码。
- runtime manifest 仍偏向 legacy `evidence_status`，缺少 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status` 等主字段。

解决方式：

- 新增 Phase 0 baseline，记录 readiness、manifest、已知问题和清洗前状态。
- 修正根文档，把项目方向统一为 swine disease LLM Wiki。
- 建立 UTF-8 编码完整性审计脚本，区分 runtime 损坏和 raw/issues 历史材料损坏。
- 更新 runtime manifest 生成逻辑，建立新的 status contract，让 legacy review 字段退为历史审计字段。

代表性修改：

- `ai-/knowledge/llm_wiki_swine_authoritative/purpose.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/.wiki-schema.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/index.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/README.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_encoding_integrity.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/baseline_phase0_2026-05-09.json`

阶段结果：

- 根文档不再把猪病库描述为鸡病库。
- runtime damaged count 为 0。
- manifest missing paths 为 0。
- manifest 主状态字段切换为来源、事实、权威等级、风险等级和任务用途。

## 三、阶段二：药物、疾病和综合监管页面的运行时护栏统一

本阶段目标，是让所有高风险页面在默认检索时都有明确边界：哪些内容只能作为知识背景，哪些必须触发规则卡、官方来源、标签核验或拒答/升级。

为什么要做：猪病知识库里最容易产生安全风险的是药物、诊断、监管处置、休药期、MRL、残留、食品安全等内容。原来页面虽然有来源和正文说明，但机器审计和生产链路不一定能稳定识别这些边界。

原来存在的问题：

- Phase 3 前仍有 7 个 high 风险药物页。
- Phase 4 后还有 102 个 medium 风险项，其中大量来自药物页缺少规则卡字面锚点。
- 疾病页缺少统一诊断、监管、用药、休药期/MRL 边界。
- synthesis/regulatory 页面含有大量监管和药物术语，容易被普通事实页规则误判。

解决方式：

- 药物页统一补齐 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`。
- 疾病页统一补齐 `RC-DX-001`、`RC-DISEASE-REGULATORY-001`、`RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`。
- synthesis/regulatory 页面新增 `RC-SYNTHESIS-SCOPE-001`、`RC-REGULATORY-CURRENT-001`、`RC-EVAL-RUBRIC-001` 等专用锚点。
- 更新幻觉风险审计脚本，让它按页面类型识别风险，而不是只按关键词误报。

代表性修改：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase4_apply_drug_guardrail_anchors.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase5_apply_disease_guardrail_anchors.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase8_apply_synthesis_regulatory_guardrails.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/synthesis/swine_regulatory_blocking_rules_china.md`

核心页面示例：

```md
## Runtime guardrail anchors / Phase 4

- `RC-DRUG-001`: This drug page is a retrieval and boundary page, not a standalone executable prescription source.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, edible-product, and food-safety claims require current label/regulatory verification.
```

阶段结果：

- 药物页缺失规则卡锚点数从 63 降为 0。
- 疾病页 73 个全部补齐运行时护栏。
- synthesis/policy 页面核心锚点缺失数为 0。
- high 风险清零，medium 风险最终清零。

## 四、阶段三：实体页压缩与证据扩展层拆分

本阶段目标，是把 disease/drug runtime 页面从“事实堆叠页”整理成“短核心边界页 + evidence expansion 路由页”。为什么要做：默认运行时检索不应该直接召回大段批处理增强块、候选事实、处方候选和历史构建内容；这些内容需要保留，但应该进入审计、追溯和人工复核层。

原来存在的问题：

- 多个药物页超过 20 KB，个别页面超过 45 KB。
- 页面正文包含 `candidate_fact`、`dose_route_course`、V13.1/V14 批处理增强块、旧补强块。
- 疾病页混合临床表现、诊断、防控、治疗候选和药物候选，检索噪声高。
- 历史构建痕迹长期留在 runtime 页，容易被模型误采为最终答案。

解决方式：

- 高风险药物页先迁移 evidence expansion，保留 runtime 占位说明。
- 对大体量药物页、疾病页和低风险大页继续做批量压缩。
- 新增通用实体页压缩工具，把历史构建期分节迁出 disease/drug runtime 页。
- evidence expansion 默认被 runtime denylist 排除，但保留来源锚点、fact id、页码、URL 和规则卡信息。

代表性修改：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase3_move_drug_evidence_expansions.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase6_compact_high_density_drug_pages.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase7_compact_high_density_disease_pages.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase9_runtime_cleanup_regression.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/compact_entity_runtime_pages.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/diseases/`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/evidence_expansions/drugs/`

阶段结果：

- 首批 7 个高风险药物页迁移 33 个证据块，high 从 7 降为 0。
- 6 个大体量药物页迁移 28 个证据块，减少 132094 bytes。
- 3 个大体量疾病页迁移 12 个证据块，减少 40524 bytes。
- 11 个低风险大页迁移 50 个证据块，减少 155100 bytes。
- 通用实体页压缩累计生成 612 个 evidence expansion 文件，旧批次标题和 `_START/_END` 标记剩余命中为 0。

## 五、阶段四：来源、事实与黄金数据集门禁标准化

本阶段目标，是把“哪些内容可以训练、评估、有限生成、检索路由或阻断”变成机器可读的门禁，而不是靠人工记忆或 legacy review 字段。

为什么要做：黄金数据集生产和评估链路不能只看页面是否 `HUMAN_REVIEWED` 或 `NEEDS_REVIEW`，而应看来源是否清晰、事实是否有效、权威等级是否满足高风险任务、规则卡是否齐全。

原来存在的问题：

- source/fact 缺少统一 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status`。
- `drug_gold_role_index.csv` 字段较窄，不能稳定判断药物页是否允许正向生成。
- 缺少 `gold_dataset_readiness_index.csv`。
- exporter/evaluator 缺少机器可读 hard-block rules。

解决方式：

- 新增 source/fact 状态标准化脚本，为 219 个 source 页面和 2193 条 fact 生成新状态索引。
- 新增 Phase 6/7 review 状态迁移和 gold dataset 门禁脚本。
- 新增核心规则卡和 exporter hard-block 配置。
- 对 runtime 页面补齐 `RC-CITATION-001` 页面级引用门禁。

代表性修改：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/standardize_source_fact_status.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase6_7_review_status_and_gold_dataset.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase8_rule_card_and_exporter_gate.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase8_apply_runtime_citation_anchors.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/source_authority_status_index.csv`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts_status_index.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/gold_dataset_readiness_index.csv`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/drug_gold_role_index.csv`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/exporter_hard_block_rules.json`

阶段结果：

- source rows: 219，source missing: 0。
- facts: 2193，invalid facts: 0。
- gold dataset readiness 中 missing critical fields 为 0。
- 非 A0 药物页正向生成允许数为 0。
- rule card count: 21，hard block count: 11。
- runtime 页面必要规则锚点缺失数为 0。

## 六、阶段五：索引图谱重建、检索冒烟测试、回归测试与 pilot 数据集

本阶段目标，是把前面所有治理结果落到可验证的工程闭环：索引要能重建，图谱要基于当前 runtime，检索不能命中 denylist，测试要能防回退，pilot 数据集要能证明 provenance 和边界控制有效。

原来存在的问题：

- 图谱 metadata 和标题仍残留 Chicken Disease。
- 旧图谱统计和当前 source/fact 数量不一致。
- 缺少 runtime allowlist 视角的检索 smoke test。
- 猪病 runtime 没有专用 pytest。
- 尚未基于门禁表试生产小批量黄金数据集。

解决方式：

- 重建核心索引、runtime graph、`knowledge-graph.md/html`。
- 新增检索 smoke test，确认默认检索不命中 raw、issues、graph、treatment_matrix、prescription_matrix。
- 新增猪病 runtime pytest，覆盖 manifest、denylist、gold dataset readiness、drug role、hard-block rules、编码完整性和 pilot provenance。
- 新增 Phase 11 pilot 脚本，试生产 train/eval/negative_trap/limited 四类样本。

代表性修改：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase9_rebuild_indexes_graph_smoke.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/phase11_pilot_gold_dataset.py`
- `ai-/tests/test_swine_llm_wiki_runtime.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/graph-data.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.html`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/pilot_gold_dataset/`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/gold_dataset_pilot_inspection_2026-05-09.md`

阶段结果：

- runtime manifest entries: 204，missing paths: 0。
- graph nodes: 2550，graph links: 3127，facts in graph: 2193。
- retrieval smoke test passed: true。
- `python -m pytest .\ai-\tests\test_swine_llm_wiki_runtime.py -q`：8 passed。
- `python -m pytest .\ai-\tests\test_llm_wiki_knowledge.py -q`：27 passed。
- pilot total samples: 32。
- provenance complete rate: 1.0。
- high risk overreach: 0。
- manual inspection pass rate: 1.0。

## 七、整体收益

本轮治理完成后，知识库的价值不只是“内容更多”，而是“使用边界更清楚、检索更干净、生成更可控、评估更可追溯、数据集生产更可门禁”。

对生产链路：

- 默认检索只进入 runtime allowlist。
- raw、issues、graph、巨大矩阵、evidence expansion 默认不进入生产检索。
- 药物、剂量、疗程、休药期、MRL、残留和监管处置必须触发规则卡和来源核验。

对评估链路：

- 有 `RC-EVAL-RUBRIC-001` 和 hard-block rules 约束无来源、过度外推、来源等级不匹配等失败模式。
- 可以区分事实错误、来源缺失、页面类型误用、规则页误用和 partial 缺口。

对黄金数据集生产：

- `gold_dataset_readiness_index.csv` 提供统一门禁。
- `drug_gold_role_index.csv` 防止非 A0/标签级药物页进入正向药物生成。
- pilot 数据集证明 4 类任务流可以带 provenance 生成，并通过自动抽检。

## 八、仍需关注的事项

1. Phase 11 pilot 是 gate-validation pilot，不是最终训练集，扩大生产前仍需领域专家抽查题目表达、答案边界和来源引用。
2. 非 runtime 文件仍有少量编码损伤信号，但 runtime damaged count 为 0，当前不影响生产检索。
3. 历史脚本和旧导出中仍可见 `HUMAN_REVIEWED`、`NEEDS_REVIEW`、`evidence_status`，但当前 runtime manifest、fact status index 和黄金数据集门禁已不依赖这些字段。
4. 后续建议把猪病 runtime 专用 pytest 加入 CI 或固定验收命令，避免后续新增来源、批处理增强或图谱重建时发生回退。

