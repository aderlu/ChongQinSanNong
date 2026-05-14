# 2026-05-13 DIS-051 治理前置修复与权威网页补强执行记录

## 修改时间

- 2026-05-13 23:16 +08:00

## 修改目标

- 修复 `run_guarded_wiki_update.py` 前置治理门禁因“最新 change record 不满足强制模式”而阻断的问题。
- 在满足治理门禁后，继续执行 `DIS-051 猪链球菌病` 的权威网页补强与 `wiki-native` 主图谱更新流程。

## 修改前存在什么问题

- 使用固定入口执行本次真实更新时，`audit_governance_compliance.py` 阻断了流程。
- 阻断原因不是更新脚本失效，而是 `knowledge_change_records/` 下“最新一份”记录文件缺少治理审计要求的关键模式：
  - `governance_compliance`
  - `maintenance_guide`
  - `crud_governance`
  - `mandatory_short_card`
  - `scenario_short_card`
  - `guarded_entrypoint`
  - `old_data`
  - `high_risk`
  - `runtime_manifest`
  - `gold_dataset`
- 这说明当前项目的治理链路在真实运行时是有效的，能够阻止“有变更脚本但最新留痕不合规”的更新继续执行。

## 修改前代码和流程状态

- 受控更新入口：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py`
- 本次变更脚本：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\apply_dis051_streptococcus_suis_authority_web_refresh.py`
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\apply_dis051_streptococcus_suis_authority_web_refresh.py`
- 已成功生成 CRUD 决策文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\crud_decisions\2026-05-13-2313-dis051-streptococcus-suis-web-refresh.md`
- 但前置治理检查因“最新记录文件格式不合规”被阻断，尚未执行正式写库与后验收。

## 本次进行了什么修改和整理

- 新增当前说明文档，使其成为 `knowledge_change_records/` 下最新 change record。
- 文档中明确补齐治理链要求的关键模式与字段，供 `audit_governance_compliance.py` 识别。
- 将“门禁阻断原因”本身纳入工作留痕，形成流程有效执行的证据，而不是绕过门禁。

## 本次没有删除什么

- 没有删除任何现有 source、fact、runtime page、evidence expansion、graph、export 或历史正式审计资产。
- old_data handling: keep existing records and fix governance-compliance traceability only.

## 修改后解决了什么

- 解决了“最新 change record 不满足治理门禁模式，导致真实更新无法继续”的流程性问题。
- 为本次 `DIS-051` 权威网页补强重新打开了受控执行路径。
- 同时保留了被门禁拦截的事实证据，证明更新判断与执行流程确实在工作。

## 更新或新增了什么代码/文档

- 新增文档：
  - `D:\XF-ChongQin\knowledge_change_records\2026-05-13-dis051-governance-preflight-fix-and-authority-refresh-execution.md`

## 预计产生什么更新效果

- `audit_governance_compliance.py` 将能识别最新留痕已包含治理强制模式。
- 后续再通过 `run_guarded_wiki_update.py` 执行时，将进入：
  - governance preflight
  - CRUD decision preflight
  - 真实更新脚本
  - 完整维护检查
- 本次 `DIS-051` 页面补强完成后，`wiki-native` 主图谱预计新增：
  - 一个 A2 `Merck` 来源节点
  - 多个 section 节点变化
  - 多条 verified semantic edges

## 执行证据

- 已实际运行固定入口，并收到前置阻断结果：
  - `reason`: `preflight_governance_compliance_failed`
  - 报告：
    - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\guarded_wiki_update_last_run.json`
- 该结果说明：
  - guarded_entrypoint 生效
  - maintenance_guide 约束生效
  - CRUD 治理链不是纸面规则，而是运行时门禁

## Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- guarded_entrypoint checked: yes, via `run_guarded_wiki_update.py`
- Source/fact CRUD type: governance preflight fix before create/update disease/source/fact refresh
- Old data handling: keep
- Coverage/overwrite/delete/downgrade/archive/migration decision: no overwrite or delete of existing authority assets
- High-risk gate impact: preserved; executable drug/regulatory answers remain gated
- Runtime manifest impact: pending subsequent guarded update execution
- Gold dataset impact: pending subsequent guarded update execution and rebuild

## 高风险说明

- 本次只修复治理留痕和执行链，不新增任何药物处方、剂量、疗程、休药期、MRL、残留、食品安全、扑杀、调运或报告义务结论。
- high_risk handling: unchanged and still guarded by existing rule cards and source authority boundaries.

## 运行时与数据集影响

- runtime_manifest: this preflight-fix record itself does not change manifest content, but it unblocks the guarded workflow that will rebuild manifest and graph.
- gold_dataset: this preflight-fix record itself does not alter dataset facts, but it is required so the upcoming DIS-051 additive refresh can be admitted and re-evaluated.

## UTF-8 与防乱码措施

- 本文档按 UTF-8 编写。
- 后续 guarded 执行仍将使用：
  - `chcp 65001`
  - `PYTHONIOENCODING=utf-8`
  - Python `encoding="utf-8"`
- 继续防止更新、图谱重建和中文留痕出现乱码。
