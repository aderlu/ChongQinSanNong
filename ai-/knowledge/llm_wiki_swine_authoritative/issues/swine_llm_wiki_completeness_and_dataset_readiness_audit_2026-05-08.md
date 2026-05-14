# 猪病 LLM Wiki 生成与评估数据集支撑能力审计（2026-05-08）

## 结论

当前 `llm_wiki_swine_authoritative` 已经具备较强的“猪病证据库雏形”：疾病、药物、规则、来源、综合分析和鉴别页面数量充足，能支撑受控的候选样本生成、疾病召回、症候鉴别、监管边界检查和弱监督评估。

但它尚不能被视为可无人值守生产高质量训练/微调数据集的完整知识库。主要原因不是资料完全缺失，而是“机器可消费层”仍不稳定：项目配置仍指向鸡病知识库，核心 `exports/knowledge_facts.json` 当前不是合法 JSON 且有乱码，疾病页关键诊断/鉴别/防控字段覆盖不足，综合和症候页面多为人读叙述而非生成器可直接执行的 schema。

## 当前资产盘点

- diseases: 73 页
- comparisons: 17 页
- drugs: 81 页
- rules: 449 页
- rule_cards: 18 页
- sources: 215 页
- syndromes: 22 页
- synthesis: 27 页
- topics: 99 页

导出层已存在：`alias_index.csv`、`comparison_index.csv`、`disease_index.csv`、`drug_page_index.csv`、`rule_index.csv`、`rule_card_index.csv`、`source_index.csv`、多类 fact index，以及 `knowledge_facts.json`。

## 证据状态

- diseases: HUMAN_REVIEWED 41，NEEDS_REVIEW 32
- drugs: HUMAN_REVIEWED 73，NEEDS_REVIEW 8
- comparisons: HUMAN_REVIEWED 14，缺少 evidence_status 3
- syndromes: HUMAN_REVIEWED 22
- rules: HUMAN_REVIEWED 433，PROCESSED_SOURCE_ANCHORED 16
- rule_cards: HUMAN_REVIEWED 11，缺少 evidence_status 7
- sources: HUMAN_REVIEWED 168，EXTRACTED 39，PROCESSED_SOURCE_ANCHORED 8
- synthesis: HUMAN_REVIEWED 22，PROCESSED_SOURCE_ANCHORED 2，缺少 evidence_status 3
- topics: HUMAN_REVIEWED 94，NEEDS_REVIEW 5

含义：页面层证据基础较强，但仍有一批疾病页和药物页不能直接作为最终结论金标准。若用于训练集，必须把 HUMAN_REVIEWED、NEEDS_REVIEW、PROCESSED_SOURCE_ANCHORED 的使用边界写入生成和评估规则。

## 疾病页结构覆盖

在 73 个疾病页面中，关键章节覆盖大致如下：

- 传播途径: 30/73
- 临床症状: 40/73
- 剖检变化: 33/73
- 实验室诊断: 32/73
- 鉴别诊断: 18/73
- 防控要点: 4/73
- 用药/处置边界: 61/73
- 监管/执行性处置边界: 61/73
- 本地证据: 61/73

含义：知识库目前更强的是“边界、规则、证据链接”，弱项是完整疾病专章字段，尤其是鉴别诊断、防控要点、实验室确诊路径。它适合做证据约束和风险拦截，不适合直接当完整疾病百科金标。

## 症候与比较页可用性

22 个 syndrome 页面基本能提供人读的临床鉴别框架，多数包含采样和鉴别信息。但未发现统一的机器字段，例如 `required_fields`、`differentials`、`must_include`、`must_not_include`、`evidence_anchors`、`sampling_plan`。

17 个 comparison 页面中，核心疾病鉴别比较较有价值，但 3 个兽药合理使用矩阵缺少 evidence_status。

含义：症候页和比较页能帮助人审和 prompt 设计，但还不能稳定驱动生成器产出结构一致的训练样本。

## 药物页可用性

81 个 drug 页面中：

- `boundary_only`: 约 71 页
- `evidence_linked_candidate`: 约 48 页
- `positive_label_candidate`: 约 11 页
- `negative_trap`: 约 1 页

含义：药物库适合做禁忌、边界、撤药期、误用风险、不能替代病原诊断等规则检查；不适合大规模生成“明确剂量/疗程/适应证”的正例，除非补齐官方标签和法规证据。

## 直接阻断训练数据生产的硬缺陷

1. 项目配置仍指向鸡病知识库

`D:\XF-ChongQin\ai-\config.json` 的 `rule_base` 仍使用：

- `knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.json`
- `knowledge/llm_wiki_chicken_authoritative/index.md`
- `knowledge/llm_wiki_chicken_authoritative/exports/disease_index.csv`
- `knowledge/llm_wiki_chicken_authoritative`

如果生成/评估系统读取此配置，猪病知识库不会真正参与主流程，或会产生鸡病证据混入猪病任务的风险。

2. `exports/knowledge_facts.json` 当前无效

`D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\knowledge_facts.json` 无法通过 JSON 解析，并且内容中存在严重乱码/损坏片段。任何依赖该文件的检索、证据绑定、规则评分、训练样本导出都会失败或产生污染样本。

3. 既有 100 并发生成评估结果显示严格 train-ready 为 0

既有分析报告显示：100 条生成中，最终通过 50，均分约 87.97，但严格训练集导出为 0。主要拒绝原因包括：

- `too_few_standard_citations`
- `missing_answer_json`
- `internal_anchor_without_source_id`
- `fatal_risk`
- `score_below_min`

这说明瓶颈已从“有没有知识”转为“生成输出没有按训练数据 schema 和证据引用规范落地”。

4. 疾病页关键字段缺口影响诊断类数据

鉴别诊断仅 18/73，防控要点仅 4/73，实验室诊断 32/73。对猪病生成与评估系统来说，这会导致：

- 诊断题缺少标准鉴别边界
- 问诊/采样题缺少必问字段
- 检测路径题缺少阴阳性解释和复检策略
- 防控题容易生成泛泛而谈的答案
- 评估器难以区分“正确但不完整”和“危险遗漏”

5. NEEDS_REVIEW 页面仍需拆分可用粒度

32 个疾病页仍为 NEEDS_REVIEW。部分已补强症候/鉴别边界，但没有强行改为 HUMAN_REVIEWED 是正确做法。下一步应拆分成可机器使用的事实粒度：哪些事实可作为 hard evidence，哪些只能作为 candidate/background。

6. 残余乱码仍需源文重抽

疾病页中仍有少量不可逆乱码残留，集中在原始摘录/候选证据行，应从本地 raw md 或来源页重新抽取，而不是凭空修复。

## 当前能支撑的任务

可以较好支撑：

- 猪病候选问答生成
- 症候到疾病的初步鉴别
- ASF、FMD 等重大疫病风险拦截
- 药物边界、禁忌、撤药期、不能替代诊断等规则判断
- 多证据引用式评估
- 人审前的弱监督样本池构建

不建议直接支撑：

- 无人值守的最终微调训练集生产
- 大规模剂量/疗程/用药正例生成
- 没有证据锚点的疾病确诊结论生成
- 监管处置自动化建议的最终答案
- 将 NEEDS_REVIEW 页面作为最终金标来源

## 补强优先级

### P0：先让系统能正确吃到猪病知识库

1. 将项目生成/评估配置切到 swine wiki，或建立独立 swine profile。
2. 重建 `exports/knowledge_facts.json`，保证合法 JSON、UTF-8、无乱码、可被解析。
3. 生成器输出强制包含：`answer_json`、`evidence_anchors`、`source_id`、`fact_id`、`page`、`rule_id`、`must_include`、`must_not_include`、`final_label`、`fatal_risk`。
4. 评估器拒绝没有标准来源引用、没有结构化答案、没有 evidence anchors 的样本。
5. 更新 readiness audit：把 JSON 可解析性、配置路径、citation/schema 覆盖、NEEDS_REVIEW 使用边界纳入硬门槛。

### P1：补齐疾病诊断与鉴别核心字段

优先补 73 个疾病页中缺失的：

- 流行病学/传播途径
- 临床症状，按日龄/阶段区分
- 剖检变化
- 实验室诊断：样本、检测方法、阳性解释、阴性复核
- 鉴别诊断：至少列出高混淆疾病和排除依据
- 防控要点：隔离、消毒、免疫、淘汰、上报、禁运等
- 监管边界：何时必须上报、何时不得经验性治疗替代诊断

### P2：把 syndrome/comparison 页面结构化

为每个 syndrome 增加机器字段：

- `required_fields`
- `differentials`
- `must_include`
- `must_not_include`
- `sampling_plan`
- `evidence_anchors`
- `hard_blocks`
- `evaluation_rubric`

为 comparison 页面补齐 `evidence_status`，并增加“生成负例/陷阱点”：例如 ASF vs CSF、FMD vs SVD/vesicular diseases、TGE vs PED vs PDCoV、PCVAD vs PRRS 等。

### P3：补齐药物与监管正源

1. 为常用兽药补官方标签、适应证、禁忌、撤药期、食品动物限制。
2. 区分 `positive_label_candidate`、`boundary_only`、`negative_trap` 的生成用途。
3. 增加中国语境下的官方监管来源：一、二、三类动物疫病，强制报告、扑杀、无害化、运输限制、产地检疫、屠宰检疫。
4. 不要用边界页生成正向处方训练样本。

### P4：文档与质量门禁

1. 更新 README/purpose，移除旧的鸡病或阶段性表述。
2. 增加 CI 或本地 audit 脚本，检查：UTF-8、JSON parse、front matter、source_id 链接、disease facet coverage、schema coverage。
3. 训练集导出前强制跑 sample-level validator。
4. 建立“可训练事实”和“背景事实”的分层导出，而不是把 markdown 全量混入训练。

## 建议的目标状态

达到以下条件后，可认为知识库可以支撑有效训练/微调数据集生产：

- 项目配置确认读取 swine wiki，而非 chicken wiki。
- 所有 exports 可解析，尤其 `knowledge_facts.json`。
- HUMAN_REVIEWED 和 NEEDS_REVIEW 的事实级使用边界明确。
- 每个高频疾病至少有完整诊断、鉴别、采样、防控、监管字段。
- 每个症候页都有统一机器 schema。
- 生成答案强制包含结构化 `answer_json` 和标准证据引用。
- 严格 train-ready 通过率从 0 提升到可接受阈值，例如首轮目标 60% 以上，再逐步提升。
- 评估器能识别 citation 缺失、风险遗漏、错误用药、未上报重大疫病、把疑似诊断说成确诊等错误。

## 总体判断

当前知识库的页面层资料价值较高，但工程消费层尚未闭环。它可以作为猪病生成与评估系统的证据基础和弱监督来源；若目标是为大模型提供可训练、可微调、可追溯的数据集，必须先完成配置切换、facts 导出修复、schema 化、疾病字段补齐和训练样本验证门禁。
