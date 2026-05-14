# 知识图谱关系边构建汇报文档新增记录

时间：2026-05-12

## 一、修改前存在的问题

用户需要一份可用于工作汇报的文档，系统说明当前知识图谱中节点之间的边如何构建、优化前如何构建、优化后解决了什么问题、当前起到什么作用，以及仍未解决的问题和理论解决路径。

此前相关信息分散在多个设计文档、构建脚本和对话解释中，不便于直接汇报。

## 二、本次新增内容

新增文档：

- `WIKI_KG_EDGE_CONSTRUCTION_REPORT.md`

文档内容包括：

1. 当前图谱基本统计。
2. 四类边数量：structural、evidence、governance、semantic。
3. 优化前基于 legacy `wiki/graph-data.json` 的构建方式和问题。
4. 当前 wiki-native 图谱构建流程。
5. 四类边的详细解释、真实示例、建立依据和代码位置。
6. 相比优化前的主要改进。
7. 当前图谱起到的作用。
8. 尚未解决的问题。
9. 阻碍原因。
10. 理论解决路径，包括 source_alignment、endpoint_grounding、medical_entailment、high_risk_second_validator。

## 三、修改后解决的问题

- 将分散说明整理为单独汇报文档。
- 便于说明当前图谱不是随意乱连，而是基于 Wiki 结构、来源标记、规则卡和 evidence_unit 构建。
- 同时明确指出当前 semantic edge 仍未完成严格医学事实验证，避免过度承诺。

## 四、预计效果

该文档可用于向项目相关人员说明：

- 当前边是怎么来的。
- 当前优化相比旧图谱改进在哪里。
- 为什么当前图谱已经提升了可追溯性。
- 为什么仍需继续补 source 原文对齐和医学蕴含验证。

## 五、编码与验证

已执行编码审计：

```powershell
python tools/audit_encoding_integrity.py
```

结果：

- `mojibake_like_content=0`
- `runtime_damaged_count=0`

未引入新的乱码问题。
