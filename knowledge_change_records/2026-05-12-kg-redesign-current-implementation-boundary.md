# WIKI_NATIVE_KNOWLEDGE_GRAPH_REDESIGN 当前实现边界更新说明

时间：2026-05-12

## 一、修改前存在的问题

原设计文档中部分表述偏向完整目标方案，容易让后续执行者误以为当前 MVP 已经完成了完整的 source 原文一致性校验和医学蕴含校验。尤其是高风险关系边，如处方、用药、标签、MRL、监管、鉴别诊断等，当前代码已经做了证据链形式校验和 rule card 门控，但尚未逐条回查 source 原文，也尚未引入独立医学蕴含验证器。

## 二、修改前代码/文档状态

当前代码主要实现于：

- `tools/build_wiki_native_graph_mvp.py`
- `tools/render_wiki_native_graph.py`
- `config/wiki_native_predicate_registry.json`

当前构建脚本已经能保证：

- 语义边先 candidate，再验证升级。
- verified 边必须有 evidence_unit_id、source_id、anchor、evidence_text、supporting_span。
- supporting_span 必须是 evidence_text 的原文子串。
- 高风险 predicate 必须有 required rule card。
- candidate/rejected 不允许进入黄金数据集正例。
- audit_graph 会拦截缺少必要字段的 verified 边。

但当前代码尚未完成：

- source 原文 anchor 定位校验。
- evidence_text 与 source 原文一致性校验。
- 处方/用药等医学语义蕴含校验。
- 否定、禁用、标签外使用、MRL、监管边界的完整语义降级。

## 三、本次修改内容

更新文档：

- `WIKI_NATIVE_KNOWLEDGE_GRAPH_REDESIGN.md`

新增和调整内容：

1. 增加“当前实际实现边界”章节，明确当前 MVP 已实现能力和未实现能力。
2. 修正 `verified` 的解释：当前表示通过项目当前代码定义的证据链形式校验、端点校验、rule card 校验和 evidence_support_check，不等同于已经完成 source 原文逐字定位和医学专家级验证。
3. 修正 Phase D 关系验证说明，将“高风险语义复核”改为“高风险 rule card 门控”，避免过度承诺。
4. 增加下一阶段 `source_alignment_check` 输出格式。
5. 明确高风险边进入最终黄金数据集前，必须额外满足 `source_alignment_status=pass` 和 `medical_entailment=supported`。
6. 调整最终可接受标准：第一阶段图谱可用于黄金数据集候选生成和复核，不应把高风险医学关系直接视为最终训练正例。

## 四、修改后解决的问题

- 防止后续 GPT 或开发者误把当前 verified 边理解为“医学事实绝对正确”。
- 明确区分当前已落地校验与下一阶段必须补强的 source alignment / medical entailment。
- 让文档与当前实际代码一致，减少执行过程中的错误预期。
- 为后续实现高风险边严格验证提供明确接口和准入标准。

## 五、预计更新效果

后续基于该文档继续执行时，将会：

- 更谨慎地处理处方、用药、标签、MRL、监管、鉴别诊断等高风险边。
- 不会把 candidate/rejected 或未经 source/医学复核的高风险边直接作为黄金数据集正例。
- 能按 `source_alignment_check` 和 `medical_entailment` 方向继续补强代码。

## 六、编码与验证

本次使用 UTF-8 读写文档，未使用 ANSI/GBK 编码。修改后需继续执行编码审计，确认未引入乱码。
