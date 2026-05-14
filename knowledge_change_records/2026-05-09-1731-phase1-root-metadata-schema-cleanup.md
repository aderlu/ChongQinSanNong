# Phase 1 Root Metadata And Schema Cleanup

Date: 2026-05-09

## 修改目标和范围

执行猪病 LLM Wiki 清洗整理的 Phase 1：修正根元数据和项目方向，消除 chicken/swine 领域漂移，明确运行时边界、可用性规则和高风险来源门槛。

修改文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/purpose.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/.wiki-schema.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/index.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/README.md`

## 修改前存在的问题

根元数据中存在明显历史漂移：

- `purpose.md` 写的是 chicken disease，而实际知识库是 swine disease。
- `index.md` 标题是 Chicken Disease LLM Wiki。
- `README.md` 仍描述为 Phase 1/2 初始建设阶段，不符合当前 99/100 readiness 和 runtime manifest 已存在的状态。
- `.wiki-schema.md` 只包含很简略的 page type 和 source 字段要求，没有体现 `source_status`、`fact_validity`、`task_use_status`、runtime manifest、复核状态去门槛化等新治理原则。

这些问题会污染运行时上下文、自动提示、汇报文档和后续 exporter/loader 的设计依据。

## 修改前代码和文件状态

修改前：

- `purpose.md` 描述为 “auditable chicken disease...”。
- `index.md` 第一行是 `# Chicken Disease LLM Wiki`。
- `.wiki-schema.md` 只有核心页面类型和 source 页字段要求。
- `README.md` 仍写当前处于 Phase 1/2 初始建设阶段。

## 本次更新或新增了什么代码

本次未新增 Python 或业务代码。

## 本次进行了什么整理工作

1. 更新 `purpose.md`：
   - 明确本库是 swine disease/drug/rule/source/comparison/syndrome/synthesis knowledge base。
   - 明确服务于 case generation、answer evaluation、arbitration、retrieval routing、golden dataset production。
   - 明确可用性不由复核状态决定，而由来源清晰、数据有效、来源等级匹配任务用途决定。
   - 明确高风险结论必须有 A0 或标签级等价来源。

2. 更新 `.wiki-schema.md`：
   - 明确 domain 为 swine。
   - 扩展 core page types。
   - 增加 source contract。
   - 增加 usability contract。
   - 增加 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status`。
   - 明确 `HUMAN_REVIEWED` 和 `NEEDS_REVIEW` 是迁移线索，不是 allow/block 决策。
   - 明确 runtime allowlist/denylist。

3. 更新 `index.md`：
   - 标题改为 Swine Disease LLM Wiki。
   - 增加 runtime manifest、exclude patterns、baseline readiness。
   - 增加各 runtime entry point 的职责说明。
   - 增加 governance 规则。

4. 更新 `README.md`：
   - 改为当前 swine source-first LLM Wiki 描述。
   - 增加当前 baseline counts。
   - 增加 runtime boundary、usability rule、high-risk boundary 和 maintenance records。

## 修改后解决了什么

- 根元数据不再把猪病库描述为鸡病库。
- schema 能支持后续 Phase 6 复核状态去门槛化。
- README 和 index 可以作为当前运行时知识库入口，而不是过时的初始建设说明。
- 后续生产/评估/黄金数据集逻辑有了明确的 source-first 和 task-aware 依据。

## 预计更新效果

- 降低运行时上下文误导。
- 降低后续维护者误用 `NEEDS_REVIEW` / `HUMAN_REVIEWED` 的风险。
- 让项目汇报能直接说明当前知识库状态和边界。
- 为后续 manifest、exporter、audit 代码优化提供 schema 依据。

## 验证

已运行：

```powershell
rg -n "chicken|Chicken|鸡病|NEEDS_REVIEW|HUMAN_REVIEWED|source_status|fact_validity" knowledge\llm_wiki_swine_authoritative\purpose.md knowledge\llm_wiki_swine_authoritative\.wiki-schema.md knowledge\llm_wiki_swine_authoritative\index.md knowledge\llm_wiki_swine_authoritative\README.md
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- 根元数据中未再出现 chicken/Chicken/鸡病。
- 新 schema 字段 `source_status` 和 `fact_validity` 已出现。
- readiness_score 仍为 99。
- missing_paths 仍为 0。

## 残余风险和下一步

本阶段只修正根元数据和 schema，不修改具体实体页，也不修改 exporter/loader 代码。后续需按 Phase 6 迁移 legacy review 状态，并按 Phase 4 清理 disease/drug 页面内的历史增强块。
