# LLM Wiki 运行 Schema 说明

## 结论

`knowledge/schemas/llm_wiki_schema.yaml` 是鸡病 LLM Wiki 知识库的运行约束 schema。它约束的是知识库如何组织、维护、校验、检索和审计，不是最终生成数据集的字段定义。

旧文件 `knowledge/schemas/schema_final_v2.yaml` 已归档到 `knowledge/schemas/archive/schema_final_v2.legacy.yaml`。它更像历史生成样本、评估结果、导出字段的业务数据 schema，不再作为当前系统的活动 schema。

- `llm_wiki_schema.yaml`：当前活动 schema，约束知识库运行方式。
- `archive/schema_final_v2.legacy.yaml`：历史数据集 schema，仅供追溯旧字段和旧质量门槛。

## 约束范围

新的运行 schema 覆盖以下内容：

- 组织：Wiki 根目录、必需根文件、必需目录、必需导出文件、页面类型与页面职责。
- 维护：来源先入库、生成候选笔记、缓存登记、维护日志、禁止导入过程直接改权威事实页。
- 校验：普通 lint、严格 lint、cache 校验、导出 JSON 校验、schema 与代码契约一致性校验。
- 检索：检索来源、返回字段、生成上下文必须包含页面命中和事实命中、目标疾病查询必须包含疾病名。
- 审计：生成 CSV 必须保留 Wiki 目录、事实数、页面数、检索 query、证据状态统计、证据 source id、目标疾病一致性和最终致命风险字段。
- 图谱：`wiki/graph-data.json` 与 `wiki/knowledge-graph.html` 是由 Wiki 页面和 exports 派生的离线可渲染结果。

## 与 llm-wiki-skill-main 的关系

`D:\XF-ChongQin\llm-wiki-skill-main` 中的 schema 不是传统数据库 schema，而是一套 Wiki 运行规则，通常体现在 `.wiki-schema.md`、source record contract、source registry 和模板约定中。它定义页面放在哪里、来源怎么登记、frontmatter 怎么写、哪些内容可以作为证据、查询和 lint 如何工作。

本项目新增的 `llm_wiki_schema.yaml` 承担类似职责，但更贴合鸡病生成评估系统：

- 明确鸡病 Wiki 的目录和页面类型。
- 明确来源类型、证据状态、缓存结构。
- 明确生成评估流程需要记录的 Wiki 审计字段。
- 可以被 `chicken-wiki schema-check` 实际校验。

## 使用方式

运行 schema 校验：

```powershell
python -m chicken_data_synthesis.wiki_cli --json schema-check
```

指定 Wiki 根目录：

```powershell
python -m chicken_data_synthesis.wiki_cli --wiki-dir D:\XF-ChongQin\ai-\knowledge\llm_wiki_chicken_authoritative --json schema-check
```

指定 schema 文件：

```powershell
python -m chicken_data_synthesis.wiki_cli --json schema-check --schema-file D:\XF-ChongQin\ai-\knowledge\schemas\llm_wiki_schema.yaml
```

校验会同时检查：

- schema 声明是否与代码中的 Wiki 契约一致。
- 当前 Wiki 根目录是否满足严格运行要求。
- exports 中 JSON 是否可解析。
- cache、source、evidence_status 是否满足严格约束。

## 修改建议

后续如果要修改知识库运行方式，应优先修改 `llm_wiki_schema.yaml`，再同步调整代码常量和校验逻辑。不要只改 `.wiki-schema.md` 或只改代码，否则容易出现“文档说一套、程序跑另一套”的问题。

`archive/schema_final_v2.legacy.yaml` 不应再改造成 LLM Wiki 运行指导。它可以用于追溯旧数据集字段，但不承担目录、来源、检索和维护规则。
