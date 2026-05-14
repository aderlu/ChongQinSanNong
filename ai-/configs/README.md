# 配置说明

当前项目保留一个核心默认配置文件：

- `config.json`：提交到仓库的默认配置，描述模型候选、生成参数、规则库、LLM Wiki 路径和输出约定。
- `config.local.json`：本地私有覆盖文件，可放 API Key、调试参数和机器差异配置，不提交仓库。

运行入口会从项目根目录读取 `config.json`，并在支持的位置合并本地配置。当前精简版不再保留独立 benchmark 配置目录。

建议：

- 把密钥放入环境变量或 `config.local.json`。
- 保持 `rule_base.llm_wiki_dir` 指向 `knowledge/llm_wiki_chicken_authoritative`。
- 新增模型候选时同步验证 `python main.py --help` 和一次小样本 `pilot`。
