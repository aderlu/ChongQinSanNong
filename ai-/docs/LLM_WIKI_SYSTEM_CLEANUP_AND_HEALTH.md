# LLM Wiki 系统清理与健康评估

## 本次清理

- `knowledge/schemas/schema_final_v2.yaml` 已归档为 `knowledge/schemas/archive/schema_final_v2.legacy.yaml`。
- 当前活动 schema 统一为 `knowledge/schemas/llm_wiki_schema.yaml`。
- 旧 Dify 对比脚本已移到 `archive/legacy_scripts/`，不再作为当前主链路入口。
- `results/`、`temp/` 中的运行产物已清空，目录保留给后续运行输出。
- `query_wiki()` 已补齐 `wiki_dir` 与 `fact_hits` 字段，和运行 schema 的检索契约保持一致。

## 当前核心架构

```text
main.py
src/chicken_data_synthesis/
├─ application/                 # 生成、评估和质量门控
├─ infrastructure/
│  ├─ knowledge/                # LLM Wiki 加载、检索、lint、schema-check、审计、ingest、digest、graph
│  ├─ persistence/              # CSV 与 snapshot 输出
│  └─ prompts/                  # 生成/评估 prompt 构造
└─ interfaces/cli/              # chicken-data 与 chicken-wiki CLI

knowledge/
├─ llm_wiki_chicken_authoritative/  # 当前权威知识库
├─ schemas/llm_wiki_schema.yaml     # 当前活动运行 schema
└─ schemas/archive/                 # 历史 schema
```

## 有效性检查

当前 LLM Wiki 知识库状态：

- 页面数：340
- 结构化事实数：1748
- 疾病索引：60
- 药物索引：115
- 规则索引：30
- 证据状态：`EXTRACTED=1633`，`INFERRED=115`
- 严格 lint：通过
- schema-check：通过

检索链路验证：

- `query_wiki()` 返回 `query`、`wiki_dir`、`hits`、`fact_hits`、`context`。
- 典型查询可同时命中 Wiki 页面和结构化事实。
- 生成上下文包含来源页面、证据 source id 和 evidence status。

## 效率评估

本地测得：

- Wiki 冷加载：约 88-106 ms。
- 单次查询：约 42-67 ms。
- 每次查询返回 5 个页面命中和 5 个结构化事实命中。
- 生成上下文长度约 3400-4200 字符，适合放入生成/评估 prompt。

结论：当前规模下，LLM Wiki 检索不是系统瓶颈。主要耗时仍会来自外部 LLM API 调用；知识库本地加载和检索足够高效。

## 后续边界

- 不再把 `schema_final_v2.yaml` 当作活动 schema。
- 不再把旧 Dify 对比脚本放在 `scripts/` 主入口中。
- 后续新增知识库规则时，优先更新 `llm_wiki_schema.yaml`，再同步代码校验逻辑。
- 后续真实 API 运行产物继续进入 `results/` 和 `temp/`，不进入核心架构。
