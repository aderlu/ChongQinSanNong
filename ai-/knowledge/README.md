# Knowledge 目录说明

本目录现在分成两条主线：

- `authoritative/`：证据真源层。用于存放真实落库的 raw 文件、来源清单、evidence registry 和 coverage 资产。
- `llm_wiki_chicken_authoritative/`：LLM Wiki 成品层。用于存放自包含、可迁移、可直接被其他项目复用的鸡病 Wiki 包。

## 主要区域

- `authoritative/`：当前鸡病权威知识库的证据底座
- `llm_wiki_chicken_authoritative/`：参考 Karpathy / `llm-wiki-skill` 方法构建的鸡病 LLM Wiki 包
- `masters/`：项目运行使用的结构化主表
- `schemas/`：模式定义
- `references/`：工作参考材料，不直接视为权威证据库
- `archive/`：旧版下载包和历史材料，保留以便追溯

## 使用建议

- 要补采、核验、追溯来源时，优先进入 `authoritative/`
- 要查询、迁移、复制到其他项目时，优先进入 `llm_wiki_chicken_authoritative/`
- 如果后续扩展到其他畜禽或其他垂直领域，建议复用 LLM Wiki 的结构，而不是直接复用当前病种内容

## 清理原则

- 明显无价值的临时锁文件会移除
- 空的 review 目录会移除
- 旧版来源包优先归档，而不是直接静默删除
