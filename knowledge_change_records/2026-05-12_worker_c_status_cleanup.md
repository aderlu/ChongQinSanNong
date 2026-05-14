# Worker C 状态清洗留痕

日期：2026-05-12

## 之前问题

- 指定目录内的非疾病/非药物实体页和综合页仍保留 legacy_evidence_status，同时在正文中重复描述 Runtime task use、gold dataset role、Runtime role、legacy audit/legacy review 等历史状态。
- 状态字段与实际可用边界、生成门控、规则锚点混写，容易让检索或生成流程把审计状态误当成可用性门槛。
- 同一类页面的使用角色散落在正文中，不利于按统一简化模型读取。

## 修改范围

仅修改以下三个目录内 Markdown 文件：

- i-/knowledge/llm_wiki_swine_authoritative/wiki/comparisons
- i-/knowledge/llm_wiki_swine_authoritative/wiki/syndromes
- i-/knowledge/llm_wiki_swine_authoritative/wiki/synthesis

未修改疾病页、药物页或其它工作者目录。

## 修改后解决什么

- 将历史状态统一整理为 front matter 三字段：source_trust、evidence_coverage、usage_scope。
- 删除重复的 legacy_evidence_status、runtime role、gold dataset role、legacy audit/review 说明。
- 保留 RC-CITATION-001、RC-SYNTHESIS-SCOPE-001、RC-REGULATORY-CURRENT-001、RC-EVAL-RUBRIC-001、RC-DRUG-001、RC-WITHDRAWAL-MRL-001 等规则锚点和生成/拒答/监管门控内容。
- 综合页的 guardrails 标题统一为 Status model and guardrails，比较页/综合入口保留来源引用门控标题。

## 改了哪些文件或整理类型

共修改 60 个文件：

- comparisons：14 个，统一为 usage_scope: differential_comparison。
- syndromes：22 个；普通综合征入口统一为 usage_scope: syndrome_entrypoint，边界/鉴别页统一为 usage_scope: syndrome_boundary。
- synthesis：24 个；按页面功能整理为 dataset_generation_policy、generation_gate、evaluation_rubric、egulatory_blocking_policy、oundary_policy、matrix_reference、source_digest 等。

## 预计效果

- 状态读取更稳定：下游可直接读取三字段判断来源信任、证据覆盖和使用范围。
- 正文噪声减少：重复历史状态被压缩，鉴别矩阵、规则、来源锚点、生成门控和拒绝条件仍保留。
- 降低误用风险：legacy 审计字段不再与可用性门槛混淆。

## 编码措施

- 所有改动文件使用 .NET UTF8Encoding(false) 写入，即 UTF-8 无 BOM。
- 留痕文件使用 UTF-8 写入。
- 修改后用 g 扫描确认目标目录不再残留 legacy_evidence_status、Runtime task use、gold dataset role、Runtime role:、Legacy audit status、legacy review 等旧状态描述。