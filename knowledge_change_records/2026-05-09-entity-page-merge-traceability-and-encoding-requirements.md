# Entity Page Merge, Traceability, And Encoding Requirements Update

Date: 2026-05-09

## 修改目标和范围

本次修改只更新执行文档：

`knowledge_change_records/2026-05-09-swine-llm-wiki-comprehensive-cleanup-execution-plan.md`

没有修改 `wiki/diseases/`、`wiki/drugs/`、索引、脚本或运行时代码。

## 修改前存在的问题

原执行文档已经提出实体页压缩、证据扩展迁移、运行时 allowlist、黄金数据集门禁和编码治理，但还缺少三个明确约束：

1. 没有明确要求 disease/drug 实体页取消“原始内容、补强块、增强内容、Vxx 批次块”的长期分层。
2. 没有明确要求同类事实直接归并到同一章节，并在去重时保留全部原始来源。
3. 对每次修改必须新增工作留痕文档的要求不够具体，不能直接满足阶段性工作汇报需要。

## 修改前相关文件状态

执行文档中 Phase 4 原本主要表达为：

- 定义 disease/drug 固定结构。
- 复核超过 20 KB 的 runtime 页面。
- 将长批次增强块移入 `wiki/evidence_expansions/`。
- Runtime 页保留短占位符。

这能降低页面长度，但还可能保留“补强块”和“原始内容”并列的历史构建痕迹，无法彻底减少实体页冗余。

## 本次更新或新增的内容

本次未新增代码。

本次更新了执行文档中的以下要求：

1. 在目标章节新增实体页组织原则：
   - 实体页不再按“原始内容、补强块、增强内容、Vxx 批次块”分割同类事实。
   - 同一类型条目必须归并到同一节中。
   - 去重后必须保留所有原始来源锚点。

2. 新增问题章节：
   - `3.7 实体页存在批次块堆叠和同类条目分散问题`
   - 说明批次块堆叠会带来检索噪声、人工审核困难和黄金数据集误采风险。

3. 强化 Phase 4：
   - 改为“实体页规范化、同类条目归并和证据扩展迁移”。
   - 明确 disease/drug 页面按知识类型整理。
   - 要求合并重复事实时保留 `source_id`、`fact_id`、页码、URL、表格、规则卡或等价锚点。
   - 要求冲突事实不得静默合并，必须保留来源等级、适用范围和待复核状态。
   - 要求无来源条目不得保留为结论。

4. 新增每次修改的留痕要求：
   - 每次修改都必须在根目录 `knowledge_change_records/` 新增 Markdown 说明。
   - 说明文档必须写清楚修改前问题、修改前状态、本次更新内容、解决了什么、预计效果、验证命令和残余风险。

5. 新增防乱码要求：
   - PowerShell 执行维护前设置 UTF-8。
   - Python 读写显式使用 UTF-8。
   - JSON 使用 `ensure_ascii=False`。
   - CSV 优先使用 `utf-8-sig`。
   - 批量覆盖前必须检查 replacement character 和 mojibake-like 模式。

## 修改后解决的问题

本次更新让后续清洗执行有了更明确的实体页整理规则：

- disease/drug 页面不再靠历史补强块堆叠表达知识。
- 同类事实归并后，页面更清晰，检索更稳定。
- 去重不会牺牲来源追溯。
- 每次修改都有可汇报的工作记录。
- 后续批量整理前有明确防乱码措施。

## 预计更新效果

后续执行 Phase 4 时，预计会减少：

- disease/drug 页面内的重复段落。
- 检索命中旧批次块的概率。
- 黄金数据集误采候选事实或旧增强内容的风险。
- 人工审核时定位最终事实的成本。
- Windows/PowerShell 环境下中文内容被误写成乱码的风险。

## 验证

本次修改后已计划执行：

```powershell
rg "补强块|增强内容|原始内容|每次修改|防乱码|source_id" knowledge_change_records\2026-05-09-swine-llm-wiki-comprehensive-cleanup-execution-plan.md
```

并重新运行现有 readiness 审计，确认本次文档修改不影响知识库现有结构审计。

## 残余风险和下一步

本次只是更新执行要求，尚未实际清洗 disease/drug 实体页。

下一步应按执行文档进入 Phase 1 到 Phase 4，优先处理：

- 根元数据 swine/chicken 领域漂移。
- 编码完整性扫描。
- runtime manifest 字段增强。
- disease/drug 页面批次块归并和来源锚点去重。
