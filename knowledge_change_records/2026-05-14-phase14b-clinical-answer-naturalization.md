# 2026-05-14 Phase14b 主回答自然化与审计痕迹清理记录

## 修改背景

Phase12、Phase13、Phase14 已经开始生成真实问诊变量和主回答 `clinical_answer`，但 Phase14b 仍主要处理 `stage_2_grounded.answer`。该字段本质上是 grounded 审计回答，需要保留 `source=`、`fact=`、`page=`、`rule=` 等锚点，不能直接作为主训练回答。

如果 Phase14b 继续把审计 answer 当自然化对象，会造成两个问题：

- 主训练字段 `clinical_answer` 中的审计痕迹得不到兜底清理。
- 自然度评分错误地把 `[source=]` 缺失当作扣分，不符合“主回答禁止审计字段”的新规则。

## 修改前代码行为

目标文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14b_naturalize_grounded_answers.py`

修改前行为：

- `naturalness_score()` 会因为文本没有 `[source=]` 扣分。
- `process_rows()` 只改写 `stage_2_grounded.answer`，不处理 `stage_2_grounded.clinical_answer`。
- 清理规则主要处理英文标题、字典残片和部分标签，不系统清除：
  - `[source=...]`
  - `source=...`
  - `fact=...`
  - `page=...`
  - `rule=...`
  - `DIS-...`
  - `RC-...`
  - `知识库`
  - `引用锚点`

## 本次修改内容

新增规则：

- `INLINE_AUDIT_RE`：识别方括号审计引用。
- `BARE_AUDIT_RE`：识别裸露审计字段。
- `ENTITY_OR_RULE_ID_RE`：识别 `DIS-`、`RC-` 类编号。
- `AUDIT_WORD_RE`：识别知识库、Wiki、引用锚点、证据锚点等审计话术。

新增函数：

- `has_audit_artifact(answer)`
- `clean_clinical_answer(answer)`
- `fallback_clinical_answer(row, audit_answer)`

调整逻辑：

- `stage_2_grounded.answer` 继续作为审计回答保留锚点，只做轻量自然化。
- `stage_2_grounded.clinical_answer` 作为主训练回答，执行审计痕迹清理。
- 若 `clinical_answer` 为空，则基于问诊场景生成兜底主回答。
- `style_flags` 新增：
  - `audit_artifact_detected`
  - `clinical_answer_cleaned`
  - `audit_answer_naturalized`
- 报告新增 `clinical_answer_audit_artifact_samples`。
- JSONL 读取改为 `utf-8-sig`，兼容 BOM。

## 解决的问题

- 纠正“主回答需要引用锚点”的旧评分逻辑。
- 防止审计字段污染 SFT 主训练回答。
- 保留审计 answer 的事实追溯能力，不破坏 Phase15/Phase18。
- 对空主回答提供兜底问诊式回答，降低导出空值风险。

## 预期效果

- `clinical_answer` 中审计字段泄漏显著降低，目标为 0。
- `style_clinical_conversation_score` 更符合真实问诊主回答的质量。
- Phase16 导出的训练样本更适合直接用于问诊 SFT。

## 编码与清理

- 所有读写保持 UTF-8 或 UTF-8-SIG 兼容。
- 未新增临时脚本。
- 未删除历史 Phase14b 输出，避免破坏已有实验留痕。
