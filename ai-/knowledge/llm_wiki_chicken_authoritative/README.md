# Chicken Disease Authoritative LLM Wiki

This package is a self-contained chicken-disease LLM Wiki built around immutable raw evidence, concise AI-written wiki pages, and a small set of searchable indexes.

## What is inside

- `raw/`: local HTML, PDF, and DOCX originals copied from the authoritative evidence layer
- `wiki/sources/`: one source page per evidence item, including standards anchors
- `wiki/diseases/`: disease pages
- `wiki/syndromes/`: scenario and syndrome pages that are intentionally not disease entities
- `wiki/rules/`: regulatory and rule-anchor pages
- `wiki/drugs/`: drug summaries and rule cards
- `wiki/topics/`: navigation and synthesis pages
- `wiki/graph-data.json`: graph export
- `wiki/knowledge-graph.html`: local graph viewer
- `exports/`: compact machine-readable indexes and fact exports
- `purpose.md`: package-level research scope and usage target
- `.wiki-schema.md`: maintenance conventions for future LLM sessions
- `log.md`: append-only rebuild log
- `issues/manual_fetch_queue.*`: unresolved full text or manual pull queue

## Current package stats

- Source pages: 121
- Extractable text sources: 121
- Non-extractable text sources: 0
- Disease pages: 60
- Syndrome/scenario pages: 3
- Drug pages: 115
- Standards anchors: 34
- Rule pages: 30
- Topic pages: 7
- Unresolved issue groups: 4



raw/：从权威证据层复制的本地 HTML、PDF、DOCX 原始文件
wiki/sources/：每条证据对应一个来源词条页，含标准锚点
wiki/diseases/：鸡病词条页面
wiki/syndromes/：场景与综合征词条页，不作为独立病种实体
wiki/rules/：法规及规则锚点页面
wiki/drugs/：药物概要与规则卡片
wiki/topics/：导航页与知识聚合汇总页
wiki/graph-data.json：知识图谱导出文件
wiki/knowledge-graph.html：本地图谱查看器
exports/：精简机器可读索引与事实数据导出文件
purpose.md：整体项目研究范围与使用目标说明.
wiki-schema.md：供后续大模型会话使用的知识库维护规范
log.md：仅追加写入的重构日志
issues/manual_fetch_queue.*：未完成全文抓取或人工拉取任务队列
当前项目统计数据
来源词条页：121 个
可提取文本来源：121 个
不可提取文本来源：0 个
病种词条页：60 个
综合征 / 场景词条页：3 个
药物词条页：115 个
标准锚点：34 个
规则词条页：30 个
主题导航页：7 个
未解决问题分组：4 个
