# Maintenance Helper Docs Status Contract Alignment

Date: 2026-05-09

## 修改目标和范围

本次补充处理 Phase 0-2 收尾检查中出现的维护辅助文档，使它们与本轮根元数据和 schema 的新状态契约保持一致。

涉及文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_MAINTENANCE_GUIDE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/CHANGE_RECORD_TEMPLATE.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/SOURCE_BATCH_INTAKE_CHECKLIST.md`

## 修改前存在的问题

收尾检查发现工作区中已有两个新增辅助文档，并且 `WIKI_MAINTENANCE_GUIDE.md` 已引用它们：

- `CHANGE_RECORD_TEMPLATE.md`
- `SOURCE_BATCH_INTAKE_CHECKLIST.md`

这两个文档有助于后续留痕和批次接入，但其中部分措辞仍沿用旧的 review/NEEDS_REVIEW 语义，和 Phase 1 更新后的原则不完全一致。

## 修改前代码和文件状态

`SOURCE_BATCH_INTAKE_CHECKLIST.md` 中曾写：

- other source requiring human review
- Facts with incomplete anchors are marked as `NEEDS_REVIEW`

`CHANGE_RECORD_TEMPLATE.md` 中曾写：

- audit and human review
- pages needing human review

这些表述容易把“复核”重新变成可用性门槛。

## 本次更新或新增了什么代码

本次未新增 Python 或运行时代码。

本次更新了两个维护辅助文档：

1. `SOURCE_BATCH_INTAKE_CHECKLIST.md`
   - 将 `human review` 改为 source expansion or authority-level clarification。
   - 将 `NEEDS_REVIEW` 改为 `source_status=source_missing` 或 `fact_validity=insufficient_anchor`。
   - 增加状态映射要求：使用 `source_status`、`fact_validity`、`authority_level`、`risk_class`、`task_use_status`，不使用 legacy review states 作为门槛。

2. `CHANGE_RECORD_TEMPLATE.md`
   - 将 `audit and human review` 改为 audit, source expansion, and validity checks。
   - 将 `pages needing human review` 改为 pages or facts needing source expansion, conflict resolution, or authority-level clarification。

## 本次进行了什么整理工作

本次没有整理实体页或索引，只整理维护辅助说明，确保后续新增来源、批次和工作记录时，不会继续使用“待复核”作为模糊状态。

## 修改后解决了什么

- 维护辅助文档与 Phase 1 schema 契约一致。
- 避免 `NEEDS_REVIEW` 在后续接入清单中被继续当作默认状态。
- 工作记录模板更符合“来源清晰、数据有效、来源等级匹配用途即可使用”的治理方向。

## 预计更新效果

- 后续维护者填写接入清单时会直接使用新状态字段。
- 工作汇报模板能更准确说明来源扩展、冲突解决和有效性检查，而不是笼统写人工复核。
- 为 Phase 6 复核状态去门槛化减少文档层阻力。

## 验证

已运行收尾验证：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
python knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- runtime_damaged_count: 0。
- runtime manifest entries: 198。
- manifest missing_paths: 0。
- hallucination risk high: 0。
- hallucination risk medium: 0。
- readiness_score: 99。

## 残余风险和下一步

本次只对维护辅助文档做状态契约对齐。后续 Phase 6 仍需真正修改 manifest builder、exporter、runtime loader、audit 脚本和实体页状态字段。
