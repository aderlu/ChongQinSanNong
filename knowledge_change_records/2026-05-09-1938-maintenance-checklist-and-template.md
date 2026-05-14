# Wiki 维护检查清单与留痕模板新增记录

## 1. 落地时间

- 落地日期：2026-05-09
- 落地时间：19:38（Asia/Shanghai，精确到时和分）
- 工作类型：维护规范落地化，新增准入检查清单和工作留痕模板

## 2. 修改前存在的问题

此前已经新增 `WIKI_MAINTENANCE_GUIDE.md`，明确了后续维护原则。但该文档偏规范说明，后续维护人员在实际新增来源、导入批处理增强块、迁移 evidence expansion 或写工作记录时，还缺少两个可直接复用的执行工具：

1. 新增来源和批处理增强块前的准入检查清单。
2. 每次修改后可复制使用的工作留痕模板。

如果没有这些模板，后续维护仍可能出现执行口径不一致、漏跑审计、漏写来源锚点、漏写工作记录等问题。

## 3. 修改前代码和知识库状态

修改前已有：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- Phase 1 到 Phase 9 的清洗脚本和审计脚本
- `knowledge_change_records/` 下的阶段性留痕文档

但知识库根目录下没有专门的 source/batch intake checklist，也没有统一的 change record template。

## 4. 本次新增或更新的内容

新增文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/SOURCE_BATCH_INTAKE_CHECKLIST.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/CHANGE_RECORD_TEMPLATE.md`

更新文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`

更新方式：

1. 在维护指南的新增来源/批处理工作流中引用 `SOURCE_BATCH_INTAKE_CHECKLIST.md`。
2. 在维护指南的工作留痕章节中引用 `CHANGE_RECORD_TEMPLATE.md`。

## 5. 本次整理更新工作

`SOURCE_BATCH_INTAKE_CHECKLIST.md` 覆盖：

- 来源注册要求
- 事实抽取要求
- runtime 与 evidence expansion 放置决策
- guardrail 要求
- batch block 标记要求
- 审计要求
- 工作留痕要求

`CHANGE_RECORD_TEMPLATE.md` 覆盖：

- 落地时间
- 修改前问题
- 修改前代码和知识库状态
- 新增或更新代码
- wiki 整理工作
- 解决的问题
- 验证结果
- 预计效果
- 剩余问题
- 结论

## 6. 修改后解决了什么

本次修改解决了维护规范难以直接执行的问题。后续维护人员可以：

1. 在新增来源前按 checklist 检查来源、事实锚点和放置位置。
2. 在新增批处理增强块前确认是否应进入 evidence expansion。
3. 在修改后按模板写工作记录。
4. 按固定命令执行 manifest、幻觉风险和 readiness 审计。
5. 降低因为人为遗漏导致知识库重新变得冗长、混乱或不可追溯的风险。

## 7. 验证结果

本次为文档维护工作，未修改运行时知识页正文，未新增事实，未变更生产检索内容。

已确认新增文件存在：

```text
ai-/knowledge/llm_wiki_swine_authoritative/SOURCE_BATCH_INTAKE_CHECKLIST.md
ai-/knowledge/llm_wiki_swine_authoritative/CHANGE_RECORD_TEMPLATE.md
```

已确认维护指南完成引用更新：

```text
ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md
```

## 8. 预计效果

1. 后续新增来源和批处理增强块会有统一准入标准。
2. 后续工作留痕格式会更稳定，便于汇报和审计。
3. 维护人员更容易遵守“runtime 保持精简、长证据进入 expansion、每次修改必审计”的规则。
4. 降低知识库治理成果回退的风险。

## 9. 剩余问题

后续仍需在实际新增来源或批处理增强块时严格执行该清单和模板。模板本身不能替代审计脚本，任何实质性内容变更仍必须运行：

- `build_runtime_core_manifest.py`
- `audit_runtime_hallucination_risk.py`
- `audit_swine_llm_wiki_readiness.py`

## 10. 结论

本次继续任务完成了维护规范的落地化补充。知识库现在不仅有维护原则，还有新增来源/批处理前的检查清单，以及每次修改后的工作记录模板，可用于长期保持 wiki 清晰、有效和可审计。
