# 鸡病数据生成与评估系统

这是一个面向鸡病问诊场景的合成数据生成、质量评估、规则拦截和 LLM Wiki 知识库维护项目。当前版本聚焦保留核心主链路，清理旧的 benchmark 外壳、历史知识库目录和临时产物。

## 核心能力

- 鸡病问诊样本生成：支持 pilot 和 production 两种运行模式。
- 双裁判与仲裁评估：生成结果可进入多模型评审和仲裁流程。
- 规则拦截：结合规则库和 LLM Wiki 证据识别禁用药、限制药、待复核风险。
- LLM Wiki 知识库：支持 status、lint、query、digest、ingest、source、cache、graph 等维护命令。

## 当前结构

```text
.
├─ main.py                         # 主流程入口
├─ config.json                     # 默认配置
├─ pyproject.toml                  # 包配置与 console scripts
├─ src/chicken_data_synthesis/     # 主应用包
│  ├─ application/                 # 用例和编排边界
│  ├─ domain/                      # 领域模型
│  ├─ infrastructure/              # 配置、LLM、知识库、规则、持久化适配
│  └─ interfaces/cli/              # CLI 适配层
├─ scripts/                        # 兼容运行脚本
├─ llm_foundation/                 # 兼容 LLM/prompt/rule 工具
├─ deepeval_integration/           # DeepEval 兼容适配
├─ prompt_templates/               # Prompt 模板
├─ knowledge/                      # 当前权威知识库和主数据
├─ docs/                           # 当前知识库和架构文档
├─ configs/                        # 配置约定说明
└─ tests/                          # 核心回归测试
```

更详细的结构说明见 [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)，清理与健康评估见 [docs/LLM_WIKI_SYSTEM_CLEANUP_AND_HEALTH.md](docs/LLM_WIKI_SYSTEM_CLEANUP_AND_HEALTH.md)。
LLM Wiki skill 功能对齐审查见 [docs/LLM_WIKI_SKILL_PARITY_REVIEW.md](docs/LLM_WIKI_SKILL_PARITY_REVIEW.md)。

## 安装

```bash
pip install -e .[dev]
```

也可以临时使用：

```powershell
$env:PYTHONPATH="src;."
```

## 运行

主流程：

```bash
python main.py --help
python main.py --mode pilot
python main.py --mode production --generator-key deepseek_v32
```

安装后：

```bash
chicken-data --mode pilot
chicken-wiki --json status
```

Wiki 维护：

```bash
chicken-wiki --json lint --strict
chicken-wiki --json schema-check
chicken-wiki --json coverage
chicken-wiki query "新城疫 鉴别诊断"
chicken-wiki digest "新城疫 鉴别诊断" --save
chicken-wiki batch-ingest ./materials --recursive
chicken-wiki ingest-url https://example.com/poultry-note --title "Demo URL source"
chicken-wiki crystallize "产蛋下降场景鉴别" --notes "把检索证据沉淀为二级会话结晶"
chicken-wiki source match --input sample.pdf
chicken-wiki graph-build
```

## 验证

```bash
python -m pytest -q
python -m compileall -q src tests
chicken-wiki --json lint --strict
```

## 保留边界

- `knowledge/llm_wiki_chicken_authoritative` 是当前权威 Wiki 包。
- `knowledge/masters` 保留核心主数据 CSV。
- `knowledge/schemas/llm_wiki_schema.yaml` 是当前活动的 LLM Wiki 运行 schema。
- `knowledge/schemas/archive/schema_final_v2.legacy.yaml` 是历史数据集 schema，仅供追溯。
- `knowledge/archive` 保留可追溯来源材料，不进入运行时热路径。
- `benchmarks/` 和旧 `knowledge_base/` 已从当前核心结构中移除。
- `archive/legacy_scripts` 保留旧 Dify 对比脚本，不属于当前主运行链路。
