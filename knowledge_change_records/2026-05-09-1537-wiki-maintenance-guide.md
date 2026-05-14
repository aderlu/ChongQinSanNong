# Wiki 维护规范文档新增记录

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：15:37（Asia/Shanghai，精确到时和分）
- 工作类型：新增 wiki 后续维护规范文档

## 2. 修改前存在的问题

Phase 1 到 Phase 9 已经完成知识库主要清洗治理，高风险和中风险已清零。但后续如果继续新增来源、批处理增强块或运行时页面，仍存在复发风险：

1. 新增来源可能直接堆入 runtime 页面，导致页面重新冗长。
2. 批处理增强块可能绕过 evidence expansion，重新增加检索噪声。
3. 新增事实可能缺少 `source_id`、`fact_id`、页码或等效锚点。
4. partial 页面可能被误当作完整知识页使用。
5. 维护人员可能忘记执行 manifest、幻觉风险和 readiness 回归审计。

## 3. 修改前代码和知识库状态

修改前已有清洗脚本、审计脚本和阶段记录，但缺少一份面向后续维护的统一约束文档，用于规定：

- 新来源如何进入知识库。
- 批处理增强块应放在哪里。
- runtime 页面应保持什么体量和结构。
- evidence expansion 与 runtime retrieval 的边界。
- 每次维护后必须执行哪些审计。
- 每次修改必须如何留痕。

## 4. 本次新增内容

新增维护规范文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`

该文档规定了：

1. 新增来源的准入规则。
2. 批处理增强块的放置和标记规则。
3. runtime 页面体量和候选事实密度阈值。
4. 疾病页、药物页、synthesis 页、rule card、evidence expansion 的目录职责。
5. 新来源或批处理导入后的必跑审计流程。
6. 每次维护必须新增 `knowledge_change_records` 工作记录。
7. 禁止事项，包括不得将 raw extraction dump 直接放入 runtime 页面、不得猜测 partial 页面缺口等。

## 5. 修改后解决了什么

新增维护文档后，后续维护有了统一入口和执行标准，可以降低以下风险：

1. 知识库重新变得杂乱和冗长。
2. 新增批处理证据污染默认检索层。
3. 未经锚定的事实进入生产链路。
4. partial 页面被误用为完整知识。
5. 缺少审计和留痕导致工作不可追溯。

## 6. 预计效果

1. 后续新增来源会优先进入 evidence expansion，而不是直接堆入 runtime 页面。
2. 生产链路默认检索将持续保持短、清晰、有边界。
3. 评估链路可以继续依赖 rule-card anchors、manifest 和风险审计。
4. 每次修改都有统一记录格式，便于工作汇报、审计和复盘。

## 7. 后续要求

后续任何新增来源、批处理增强块、runtime 页面、rule card 或审计脚本变更，都应先参考：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`

并在修改后至少执行：

1. `build_runtime_core_manifest.py`
2. `audit_runtime_hallucination_risk.py`
3. `audit_swine_llm_wiki_readiness.py`

同时在 `knowledge_change_records/` 下新增对应工作留痕文档。
