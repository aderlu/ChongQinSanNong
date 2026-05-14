# 项目结构

## 核心入口

- `main.py`：主流程入口，委托到 `chicken_data_synthesis.cli`。
- `src/chicken_data_synthesis/wiki_cli.py`：`chicken-wiki` 入口。
- `scripts/master_chicken_data.py`：当前生产/试跑编排脚本，仍作为主流程兼容桥接保留。

## 主包分层

```text
src/chicken_data_synthesis/
├─ application/        # 用例、服务和运行计划
├─ domain/             # 领域模型
├─ infrastructure/     # 外部能力适配
├─ interfaces/cli/     # 命令行适配
└─ shared/             # 共享基础空间
```

`infrastructure/knowledge/` 是 LLM Wiki 生命周期能力所在位置，包含加载、检索、状态、lint、缓存、ingest、digest、图谱等能力。

## 运行时知识

```text
knowledge/
├─ llm_wiki_chicken_authoritative/  # 当前权威 Wiki 包
├─ masters/                         # 主数据 CSV
├─ authoritative/                   # 权威资料加工区
├─ archive/                         # 来源归档
├─ references/                      # 外部参考文件
└─ schemas/                         # LLM Wiki 运行 schema 与历史 schema 归档
```

热路径优先使用 `knowledge/llm_wiki_chicken_authoritative`。`knowledge/masters` 仅作为兼容主数据保留；归档和参考目录用于追溯，不应被主流程频繁扫描。

当前活动 schema 是 `knowledge/schemas/llm_wiki_schema.yaml`。旧 `schema_final_v2.yaml` 已归档为 `knowledge/schemas/archive/schema_final_v2.legacy.yaml`，不再指导 LLM Wiki 运行。

## 保留的兼容层

- `llm_foundation/`：prompt 渲染和规则工具仍被当前主包引用。
- `deepeval_integration/`：DeepEval adapter 仍通过 `infrastructure/evaluation/deepeval_adapter.py` 引用。
- `scripts/`：保留主流程兼容脚本。

## 已移出核心的内容

- 旧 `benchmarks/` CLI 和配置。
- 旧 `knowledge_base/` 文档式知识库。
- 旧 Dify 对比脚本，已移动到 `archive/legacy_scripts/`。
- Python 缓存、pytest 缓存、临时 `.tmp` 文件和未跟踪的大型 PDF。
