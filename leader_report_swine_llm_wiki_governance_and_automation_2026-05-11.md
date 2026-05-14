# 猪病 LLM Wiki 知识库治理与自动化维护机制工作汇报

日期：2026-05-11  
汇报对象：项目 Leader  
范围：`ai-/knowledge/llm_wiki_swine_authoritative`

## 一、总体目标

本轮工作的总目标，是把猪病 LLM Wiki 从“可检索的知识文件集合”升级为“可进入生产、评估、黄金数据集试生产，并且后续更新可持续受控”的知识库体系。

这件事分成两层：

1. 先治理知识库内容本身：清理 runtime 噪声、压缩大页面、迁移长证据、补齐规则卡、建立来源和事实门禁、重建索引图谱、试生产 pilot 数据集。
2. 再治理后续维护流程：把维护指南和 CRUD 治理规范升级为强制规则，新增自动预检、一键验收、固定更新入口和短执行卡，保证后续网页、本地文档、脚本或定时任务更新时，不会绕过规则。

为什么要这么做：

- 猪病 Wiki 涉及医学、兽药、诊断、监管、休药期、MRL、残留、食品安全等高风险内容，不能只追求“能检索”，必须保证来源清楚、事实有效、风险可控。
- 原始知识库中存在历史构建材料、候选事实、旧批处理块、大体量页面、legacy review 字段、chicken/swine 领域漂移等问题。
- 如果只完成一次性清洗，而没有后续维护约束，后续网页资料、本地 Markdown、PDF 抽取或定时任务仍可能再次把无来源、高风险或冗余内容写回 runtime。

最终形成的能力：

- 内容层：runtime 高风险和中风险清零，默认检索只进入 allowlist，长证据进入 evidence expansion。
- 规则层：药物、疾病、监管、引用、评估、synthesis 等页面均有规则卡边界。
- 状态层：source/fact/runtime/gold dataset 用 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status` 判断，而不是依赖 `HUMAN_REVIEWED` 或 `NEEDS_REVIEW`。
- 工程层：有治理预检、一键验收、pytest 回归、固定更新入口。
- 流程层：每次修改都必须在 `knowledge_change_records/` 留痕，方便汇报和审计。

## 二、阶段一：知识库基线冻结与运行时边界治理

本阶段目标，是先明确“当前知识库是什么状态、哪些内容能进 runtime、哪些内容必须排除、后续怎么证明没有引入回归”。

修改前问题：

- 根文档和图谱仍有 chicken/swine 领域漂移。
- runtime manifest 仍偏向 legacy `evidence_status`。
- 缺少稳定的编码完整性审计，难以证明中文 runtime 没有乱码。
- raw、issues、graph、历史构建材料和大矩阵存在被默认检索误召回的风险。

解决方式：

- 冻结 Phase 0 baseline，记录 readiness、runtime manifest、路径状态和已知问题。
- 修正 `purpose.md`、`index.md`、README、schema 等根文档。
- 新增 `audit_encoding_integrity.py`，把 runtime 编码损坏和 raw/issues 历史损坏区分开。
- 更新 `build_runtime_core_manifest.py`，使用 runtime allowlist 和 denylist。
- 将 manifest 主字段切换为来源、事实、权威等级、风险类别和任务用途。

代表性产物：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_encoding_integrity.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_core_manifest.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/exports/runtime_exclude_patterns.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/baseline_phase0_2026-05-09.json`

结果：

- runtime damaged count 为 0。
- manifest missing paths 为 0。
- 默认生产和评估检索明确使用 allowlist。
- raw、issues、graph、evidence expansion、大矩阵和备份文件不进入默认 runtime。

## 三、阶段二：药物、疾病和综合监管页面护栏建设

本阶段目标，是让高风险页面在 runtime 中有清晰、机器可识别的边界，避免模型把知识页当成处方、监管动作或食品安全结论来源。

修改前问题：

- 7 个 high 风险药物页包含大量候选事实、剂量、疗程、休药期、MRL、处方候选等内容。
- 80 个 runtime 药物页中有 63 个缺少药物和休药期/MRL 规则卡锚点。
- 73 个疾病页缺少统一诊断、监管、用药、休药期/MRL 边界。
- synthesis/regulatory 页面中包含监管和药物术语，容易被普通事实页审计规则误判。

解决方式：

- 对药物页补齐 `RC-DRUG-001` 和 `RC-WITHDRAWAL-MRL-001`。
- 对疾病页补齐 `RC-DX-001`、`RC-DISEASE-REGULATORY-001`、`RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`。
- 对 synthesis/regulatory 页面补齐 `RC-SYNTHESIS-SCOPE-001`、`RC-REGULATORY-CURRENT-001`、`RC-EVAL-RUBRIC-001`。
- 更新幻觉风险审计逻辑，使其能按页面类型识别风险。

代表性产物：

- `tools/phase4_apply_drug_guardrail_anchors.py`
- `tools/phase5_apply_disease_guardrail_anchors.py`
- `tools/phase8_apply_synthesis_regulatory_guardrails.py`
- `tools/audit_runtime_hallucination_risk.py`
- `wiki/rule_cards/RC-EVAL-RUBRIC-001.md`
- `wiki/rule_cards/RC-SYNTHESIS-SCOPE-001.md`
- `wiki/rule_cards/RC-REGULATORY-CURRENT-001.md`

结果：

- 药物页缺失规则卡锚点数从 63 降为 0。
- 疾病页 73 个全部补齐运行时护栏。
- synthesis/policy 页面核心锚点缺失数为 0。
- high 风险从 7 降为 0，medium 风险最终降为 0。

## 四、阶段三：实体页压缩与证据扩展层拆分

本阶段目标，是把 disease/drug runtime 页从“事实堆叠页”整理成“短核心边界页 + evidence expansion 路由页”。

修改前问题：

- 多个药物页超过 20 KB，个别超过 45 KB。
- 页面正文中有 `candidate_fact`、`dose_route_course`、V13.1/V14 批处理增强块、旧补强块。
- 疾病页中混合临床表现、诊断、防控、治疗候选、药物候选，检索噪声高。
- 历史构建痕迹长期留在 runtime，容易被模型误采为最终答案。

解决方式：

- 将高风险药物页的大段证据迁移到 `wiki/evidence_expansions/drugs/`。
- 对大体量药物页、疾病页、低风险大页继续压缩。
- 新增通用实体页压缩工具，清理 `wiki/diseases/` 和 `wiki/drugs/` 中旧批处理标题和 `_START/_END` 标记。
- runtime 页面只保留短摘要、规则锚点和 evidence expansion 路由。

代表性产物：

- `tools/phase3_move_drug_evidence_expansions.py`
- `tools/phase6_compact_high_density_drug_pages.py`
- `tools/phase7_compact_high_density_disease_pages.py`
- `tools/phase9_runtime_cleanup_regression.py`
- `tools/compact_entity_runtime_pages.py`
- `wiki/evidence_expansions/diseases/`
- `wiki/evidence_expansions/drugs/`

结果：

- 首批 7 个高风险药物页迁移 33 个证据块。
- 6 个大体量药物页迁移 28 个证据块，减少 132094 bytes。
- 3 个大体量疾病页迁移 12 个证据块，减少 40524 bytes。
- 11 个低风险大页迁移 50 个证据块，减少 155100 bytes。
- 通用实体压缩累计生成 612 个 evidence expansion 文件。
- 旧批次标题和 `_START/_END` 标记剩余命中为 0。

## 五、阶段四：来源、事实和黄金数据集门禁标准化

本阶段目标，是把“哪些内容能训练、评估、有限生成、检索路由或阻断”变成机器可读的门禁。

修改前问题：

- source/fact 主要依赖 legacy review 字段，缺少统一状态契约。
- `drug_gold_role_index.csv` 字段不足，无法稳定判断药物页是否允许正向生成。
- 缺少统一 `gold_dataset_readiness_index.csv`。
- exporter/evaluator 缺少机器可读 hard-block 配置。

解决方式：

- 新增 `standardize_source_fact_status.py`，为 source 和 facts 生成新状态索引。
- 新增 `phase6_7_review_status_and_gold_dataset.py`，生成黄金数据集门禁表。
- 新增 `exporter_hard_block_rules.json`。
- 对 runtime 页面补齐 `RC-CITATION-001` 页面级来源引用门禁。

代表性产物：

- `exports/source_authority_status_index.csv`
- `exports/knowledge_facts_status_index.json`
- `exports/gold_dataset_readiness_index.csv`
- `exports/drug_gold_role_index.csv`
- `exports/exporter_hard_block_rules.json`
- `tools/standardize_source_fact_status.py`
- `tools/phase6_7_review_status_and_gold_dataset.py`
- `tools/phase8_rule_card_and_exporter_gate.py`
- `tools/phase8_apply_runtime_citation_anchors.py`

结果：

- source rows: 219，source missing: 0。
- facts: 2193，invalid facts: 0。
- gold dataset readiness 中 missing critical fields 为 0。
- 非 A0 药物页正向生成允许数为 0。
- rule card count: 21，hard block count: 11。
- runtime 页面必要规则锚点缺失数为 0。

## 六、阶段五：索引图谱重建、检索冒烟测试和 pilot 数据集

本阶段目标，是把前面治理结果落到可验证工程闭环。

修改前问题：

- 图谱标题和 metadata 仍有 Chicken Disease 遗留。
- 图谱统计与当前 source/fact 不一致。
- 缺少 runtime allowlist 视角的检索 smoke test。
- 缺少猪病 runtime 专用 pytest。
- 尚未进行小批量黄金数据集试生产。

解决方式：

- 重建核心索引、runtime graph、`knowledge-graph.md/html`。
- 新增检索 smoke test，确认默认检索不命中 raw、issues、graph、大矩阵。
- 新增猪病 runtime pytest。
- 新增 Phase 11 pilot 脚本，试生产 train/eval/negative_trap/limited 四类样本。

代表性产物：

- `tools/phase9_rebuild_indexes_graph_smoke.py`
- `tools/phase11_pilot_gold_dataset.py`
- `tests/test_swine_llm_wiki_runtime.py`
- `wiki/graph-data.json`
- `wiki/knowledge-graph.md`
- `wiki/knowledge-graph.html`
- `exports/pilot_gold_dataset/`
- `issues/gold_dataset_pilot_inspection_2026-05-09.md`

结果：

- runtime manifest entries: 204，missing paths: 0。
- graph nodes: 2550，graph links: 3127，facts in graph: 2193。
- retrieval smoke test passed: true。
- pilot total samples: 32。
- provenance complete rate: 1.0。
- high risk overreach: 0。
- manual inspection pass rate: 1.0。

## 七、阶段六：治理规则强制落地

本阶段目标，是防止后续维护时只完成一次性清洗，却没有稳定执行规则。

修改前问题：

- `WIKI_MAINTENANCE_GUIDE.md` 已经有 source-first 维护规则。
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 已经有 CRUD 和旧数据处理逻辑。
- 但 CRUD 治理规范还没有被 README、index、schema、checklist、change record template 明确挂成强制规则。
- 后续维护者可能只看 README 或 checklist，忽略旧数据处理、覆盖/删除/降级/归档、高风险门禁等规则。

解决方式：

- 将两份治理文档升级为 mandatory governance rules。
- 更新 README、index、schema、SOURCE_BATCH_INTAKE_CHECKLIST、CHANGE_RECORD_TEMPLATE。
- 在变更模板中新增 `Governance Compliance` 区块。
- 要求每次修改说明 CRUD 类型、旧数据处理、高风险门禁、runtime manifest、gold dataset 影响。

代表性产物：

- `WIKI_MAINTENANCE_GUIDE.md`
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
- `SOURCE_BATCH_INTAKE_CHECKLIST.md`
- `CHANGE_RECORD_TEMPLATE.md`
- `knowledge_change_records/2026-05-11-0000-wiki-governance-rules-enforcement.md`

结果：

- 两份治理文档从参考文档变成强制更新规则。
- web source、本地 Markdown、本地文档抽取、旧版本处理、冲突事实处理都有固定依据。
- 每次修改必须形成可汇报、可审计的工作留痕。

## 八、阶段七：治理自动化、预检和一键验收

本阶段目标，是减少人工提醒，让 LLM 和维护者在更新 Wiki 时自动受到约束。

修改前问题：

- 每次需要人工提醒 LLM 先读两份治理文档。
- 每次验收要记住多条命令。
- 没有自动检查 README、index、schema、checklist、change record template 是否仍挂着治理规则。
- 如果最新变更记录漏写治理合规，主要靠人工发现。

解决方式：

- 更新 `ai-/AGENTS.md`，加入 `Mandatory Swine Wiki Governance`。
- 新增 `audit_governance_compliance.py`，自动检查治理文档、入口文件、最新变更记录和乱码信号。
- 新增 `run_swine_wiki_maintenance_checks.py`，一键执行治理预检、manifest、风险审计、readiness、编码审计和 pytest。
- 将治理预检接入 `tests/test_swine_llm_wiki_runtime.py`。

代表性产物：

- `ai-/AGENTS.md`
- `tools/audit_governance_compliance.py`
- `tools/run_swine_wiki_maintenance_checks.py`
- `tests/test_swine_llm_wiki_runtime.py`
- `knowledge_change_records/2026-05-11-0124-swine-wiki-governance-automation.md`

结果：

- 治理预检通过：`passed=true`。
- 猪病 runtime 测试从 8 项扩展到 9 项。
- 后续可通过一键命令完成治理链路和 runtime 质量检查。

## 九、阶段八：固定更新入口与短执行卡

本阶段目标，是进一步把“推荐遵守规则”升级为“所有更新通过固定入口执行”，并降低 LLM 每次读取长文档时遗漏规则的风险。

修改前问题：

- 治理文档较长，LLM 每次完整读取时可能抓不住本次任务最关键的执行项。
- 虽然有一键验收，但还没有固定入口包裹实际更新命令。
- 定时任务或人工脚本仍可能直接调用某个更新脚本，绕过预检和验收。

解决方式：

- 新增固定入口 `run_guarded_wiki_update.py`。
- 新增两份短执行卡：
  - `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
  - `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- 更新 AGENTS、README、index、schema、维护指南、CRUD 规范、checklist、模板和治理预检脚本。
- 新增 pytest，验证固定入口 dry-run 行为。

代表性产物：

- `tools/run_guarded_wiki_update.py`
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- `tools/audit_governance_compliance.py`
- `tests/test_swine_llm_wiki_runtime.py`
- `knowledge_change_records/2026-05-11-0135-fixed-guarded-wiki-update-entrypoint-and-short-cards.md`

固定入口执行方式：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python <你的更新脚本或命令>
```

固定入口会自动执行：

1. 治理预检。
2. 具体更新命令。
3. 完整验收检查。

结果：

- 治理预检通过。
- 固定入口 dry-run 通过。
- 猪病 runtime 测试扩展到 10 项并全部通过。
- 新增短执行卡和固定入口脚本均无明显乱码信号。

## 十、当前整体成果

当前猪病 LLM Wiki 已形成两条闭环。

内容治理闭环：

- runtime allowlist / denylist。
- source/fact 状态契约。
- disease/drug/synthesis 规则卡护栏。
- evidence expansion 分层。
- gold dataset readiness。
- runtime graph 和 retrieval smoke test。
- pilot dataset 自动抽检。

维护治理闭环：

- 两份完整制度文档。
- 两份短执行卡。
- 项目级 AGENTS 约束。
- SOURCE_BATCH_INTAKE_CHECKLIST。
- CHANGE_RECORD_TEMPLATE。
- governance compliance preflight。
- fixed guarded update entrypoint。
- one-command maintenance checks。
- pytest 回归。
- knowledge_change_records 工作留痕。

关键验证结果：

- runtime manifest missing paths: 0。
- hallucination risk high: 0。
- hallucination risk medium: 0。
- runtime damaged count: 0。
- readiness score: 99。
- pilot provenance complete rate: 1.0。
- high risk overreach: 0。
- governance preflight: passed。
- guarded update dry-run: passed。
- swine runtime pytest: 10 passed。

## 十一、后续使用方式

后续所有人工、LLM、脚本或定时任务触发的 Wiki 修改，都建议走以下流程：

1. 先读：
   - `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
   - `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
2. 复杂场景再查：
   - `WIKI_MAINTENANCE_GUIDE.md`
   - `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
3. 执行更新时使用固定入口：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python <实际更新脚本>
```

4. 每次修改都在 `knowledge_change_records/` 新增说明文档。
5. 如果只做全量验收，可运行：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py
```

## 十二、仍需关注

1. 固定入口已经完成，但如果存在外部 Windows 计划任务或其他调度器，还需要把调度命令改成调用 `run_guarded_wiki_update.py`。
2. Phase 11 pilot 仍是 gate-validation pilot，不是最终正式训练集，扩大生产前仍需领域专家抽查。
3. 非 runtime 历史材料仍可能存在少量编码损伤信号，但 runtime damaged count 为 0。
4. 后续如果新增更新脚本，应在脚本说明和 change record 中明确必须由固定入口调用。

## 十三、总结

本轮工作完成了从“知识库内容治理”到“后续维护机制治理”的连续升级。5 月 9 日完成了 runtime、实体页、来源事实、规则卡、图谱、检索和 pilot 数据集治理；5 月 11 日进一步把维护规则、自动预检、一键验收、固定入口和短执行卡落地。

现在猪病 LLM Wiki 不只是一次性清洗完成，而是具备了持续更新的安全机制：后续任何网页来源、本地文档、脚本批处理或定时任务更新，都有明确规则、固定入口、自动验收和工作留痕，能够更稳定地支撑生产问答、评估和黄金数据集建设。

