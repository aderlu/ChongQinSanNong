# 基于 LLM Wiki 的鸡病生成与评估系统

## 架构分析

当前项目已经具备清晰的四层结构：

- `scripts/master_chicken_data.py`：生产流水线编排入口，负责任务拆分、生成、规则拦截、双裁判、仲裁、快照和 CSV 输出。
- `src/chicken_data_synthesis/application/`：应用层用例与服务，封装生成策略、评审策略、批处理、任务规划和结果归一化。
- `src/chicken_data_synthesis/infrastructure/`：基础设施层，负责配置、LLM 调用、Prompt、评估适配、持久化和规则。
- `knowledge/llm_wiki_chicken_authoritative/`：已经按 LLM Wiki 方法编译完成的鸡病知识包，包含 `raw/`、`wiki/`、`exports/`、`issues/`、`index.md`、`.wiki-schema.md` 和可视化图谱。

这与 `llm-wiki-skill` 的关键模式一致：先把权威资料编译成可读、可维护、可检索的 Markdown Wiki，再通过机器索引和事实导出支撑 LLM 工作流。区别是本项目原先只把 `knowledge` 放在旁路，没有成为生成和评估的强依赖。

## 新增知识底座适配层

新增 `src/chicken_data_synthesis/infrastructure/knowledge/`：

- 加载 `wiki/**/*.md`、`index.md`、`purpose.md`、`.wiki-schema.md`。
- 加载 `exports/knowledge_facts.json`、`disease_index.csv`、`rule_index.csv`、`drug_page_index.csv`。
- 提供轻量检索、事实检索、疾病名导出和 Prompt-ready 上下文拼装。
- 使用 `lru_cache` 缓存知识包，避免每个样本重复扫描 Wiki。

## 对齐 llm-wiki-skill 的工具链能力

参考 `llm-wiki-skill` 的完整实现后，项目补齐了维护型能力，而不只是 RAG 式召回：

- Status：统计 raw、wiki sections、疾病/药物/规则、事实量、证据状态、图谱资产和日志尾部。
- Lint：检查必需文件、索引目标、Wiki 双链、事实 `evidence_status`、`NEEDS_REVIEW` 和 source id 可追踪性。
- Runtime Context：生成类似 SessionStart 的运行时上下文，让 LLM 会话先知道知识包边界和约束。
- Query：按问题召回 Wiki 页面与事实上下文。
- Query Save：把高价值查询沉淀为 `wiki/queries/*.md` 派生页，并写入 `log.md`。
- Step1 Validate：验证实体、主题、连接 JSON 是否包含置信度和证据字段，用于后续资料入库前的结构门。

命令入口：

```bash
chicken-wiki status
chicken-wiki lint
chicken-wiki context
chicken-wiki query "新城疫 呼吸道 休药期"
chicken-wiki query-save "新城疫如何鉴别" "需结合呼吸道、神经症状与实验室检测。"
chicken-wiki step1-validate step1.json
```

## HTML 图谱与动态同步

本项目现在已经实现与 `llm-wiki-skill` 类似的知识库 HTML 可视化闭环：

- `chicken-wiki graph-build` 会从 `exports/disease_index.csv`、`exports/drug_page_index.csv`、`exports/rule_index.csv`、`exports/knowledge_facts.json` 重建图谱。
- 输出文件为：
  - `knowledge/llm_wiki_chicken_authoritative/wiki/graph-data.json`
  - `knowledge/llm_wiki_chicken_authoritative/wiki/knowledge-graph.html`
- HTML 页面内嵌一份构建时图谱，同时会尝试从旁边的 `graph-data.json` 读取最新数据。
- 如果通过本地 HTTP 服务打开页面，点击“刷新图谱数据”即可读取最新 `graph-data.json`。
- 如果直接双击 HTML，浏览器可能因本地文件安全策略阻止 `fetch('graph-data.json')`，此时仍会显示内嵌数据；需要重新运行 `graph-build` 并刷新页面才能看到更新。

推荐查看方式：

```bash
chicken-wiki graph-build
cd knowledge/llm_wiki_chicken_authoritative/wiki
python -m http.server 8765
```

然后打开：

```text
http://127.0.0.1:8765/knowledge-graph.html
```

自动观察变化：

```bash
chicken-wiki graph-watch --interval 2
```

当 `wiki/` 或 `exports/` 下文件变化时，`graph-watch` 会自动重建 `graph-data.json` 与 `knowledge-graph.html`。浏览器页面点击“刷新图谱数据”即可看到新节点和新关系；如果需要完全自动刷新浏览器，可在后续增加前端定时刷新开关。

演示验证方式：

1. 运行 `chicken-wiki graph-build`，记录 `node_count`。
2. 向 `exports/disease_index.csv` 增加一行疾病，并在 `wiki/diseases/` 增加对应页面。
3. 再运行 `chicken-wiki graph-build`。
4. 检查 `graph-data.json` 和 `knowledge-graph.html` 是否都包含新疾病名。

已用临时 Wiki 验证：加入 `HTML同步演示病` 后，节点数从 337 增加到 339，`graph-data.json` 与 `knowledge-graph.html` 均包含该新节点。

## 运行链路

1. 任务规划优先从 Wiki `disease_index.csv` 获取疾病实体，避免配置里的疾病名与知识库不一致。
2. 问诊草稿生成按疾病名检索 Wiki，生成真实养殖户问题。
3. 盲补全阶段按 `user_query + metadata` 检索 Wiki，在不泄露目标病名的前提下提供疾病、规则和药物事实。
4. 双裁判评估按完整病例检索 Wiki，用知识底座检查诊断、鉴别诊断、用药合规和休药期。
5. 仲裁阶段按病例和两名裁判摘要检索 Wiki，减少分歧裁决时的幻觉。
6. 规则层读取同一 Wiki 上下文，遇到禁用/限制证据、`NEEDS_REVIEW` 事实时输出可追踪风险码。

## 配置入口

`config.json` 的 `rule_base` 已指向当前知识包：

- `knowledge_base_file`: `knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.json`
- `references_file`: `knowledge/llm_wiki_chicken_authoritative/index.md`
- `llm_wiki_index_file`: `knowledge/llm_wiki_chicken_authoritative/exports/disease_index.csv`
- `llm_wiki_dir`: `knowledge/llm_wiki_chicken_authoritative`

## 质量控制

当前系统使用三道门：

- 结构门：生成结果必须包含 `species/user_query/diagnosis/prescription/withdrawal_period/metadata`。
- 规则门：缺字段、禁用药、休药期冲突、证据不足、Wiki 待复核事实会进入风险码。
- 评审门：双裁判与仲裁使用同一 Wiki 上下文评分，最终结果落入 CSV。

建议后续继续补充 Wiki lint 脚本，把 `.wiki-schema.md` 中的坏链、来源缺失、`NEEDS_REVIEW` 阻断规则自动化。
