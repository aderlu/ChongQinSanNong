# 猪病 Wiki 更新强制短执行卡

本卡是每次更新前必须优先读取的短执行规则。完整制度以 `WIKI_MAINTENANCE_GUIDE.md` 和 `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` 为准；遇到具体场景再查长文档对应章节。

## 1. 固定入口

所有人工触发、LLM 触发、脚本触发、定时任务触发的 Wiki 更新，都必须通过固定入口执行：

```powershell
python .\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py -- python <你的更新脚本或命令>
```

该入口会自动执行：

1. 治理预检。
2. 具体更新命令。
3. 完整验收检查。

禁止绕过该入口直接运行会修改 Wiki 的更新脚本。紧急诊断例外必须写入 `knowledge_change_records/`。

## 2. 修改前 8 问

每次更新前必须回答：

1. 输入来源是什么：网页、本地 Markdown、PDF、Word、Excel、raw、issue、脚本输出、模型输出、人工审校？
2. 操作类型是什么：新增、查询、修改、删除、迁移、归档、降级、排除、重建？
3. 数据落在哪层：source、fact、evidence expansion、runtime page、rule card、synthesis、exports、gold dataset？
4. 是否涉及高风险：诊断、药物、剂量、疗程、休药期、MRL、残留、食品安全、监管处置？
5. 来源等级是什么：A0、A1、A2、SRC、RC/RULE？
6. 是否有 source_id、fact_id、URL、页码、表格、条款或规则卡锚点？
7. 旧数据怎么处理：保留、替代、降级、归档、迁移、排除、删除？
8. 是否需要重建 manifest、index、graph、gold readiness 或 pilot/gold dataset？

## 3. Runtime 写入红线

runtime 页面只允许写：

- 短摘要。
- source/fact 锚点。
- rule-card 锚点。
- evidence expansion 路由。
- 缺口和边界说明。

不得直接写入：

- 网页全文。
- PDF/Word/Excel 长摘录。
- 本地 Markdown 中未核验的内容。
- 批处理增强块。
- 候选事实堆叠。
- 无 A0/A1 或标签级来源支持的剂量、疗程、休药期、MRL、残留、食品安全或监管结论。

## 4. 必须留痕

每次修改必须在 `knowledge_change_records/` 新增说明文档，并包含：

- 修改前问题。
- 修改前代码或知识库状态。
- 新增或更新了什么代码/文档/数据。
- 进行了什么整理、迁移、降级、归档、删除或重建。
- 修改后解决了什么。
- 预计影响。
- 验证命令和结果。
- Governance Compliance。
- UTF-8 和乱码防护措施。

