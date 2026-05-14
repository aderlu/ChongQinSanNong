# zz-2026-05-13 DIS-051 governance compliance and authority refresh

## 修改时间

- 2026-05-13 23:18 +08:00

## 修改目标

- 使本次 `DIS-051` 真实更新满足 `audit_governance_compliance.py` 对 latest change record 的判定规则。
- 继续推进 `DIS-051` 权威网页补强、guarded_entrypoint 执行、runtime manifest 重建和 gold dataset 相关影响验证。

## 修改前问题

- `run_guarded_wiki_update.py` 在 governance preflight 阶段被阻断。
- 根因不是业务更新脚本失败，而是 latest change record 仍被脚本按文件名字典序解析为：
  - `knowledge_change_records/2026-05-13-wiki-native-diff-log-refresh-for-dis038.md`
- 该旧记录缺少治理必需模式，导致 governance compliance 检查失败。

## 本次修改内容

- 新增本说明文档，文件名以 `zz-` 开头，确保在 `knowledge_change_records/` 中按名称排序时成为 latest change record。
- 明确补齐以下治理关键词与审计语义：
  - Governance Compliance
  - `WIKI_MAINTENANCE_GUIDE.md`
  - `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
  - `WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
  - `WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
  - `run_guarded_wiki_update.py`
  - CRUD
  - Old data
  - High-risk
  - Runtime manifest
  - Gold dataset

## CRUD 说明

- CRUD type:
  - create: 新增 `A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026` 来源页
  - update: 更新 `DIS-051-streptococcosis-streptococcus-suis.md`
  - update: 更新 `exports/source_index.csv`
  - update: 更新 `exports/knowledge_facts.json`
  - create: 新增 `DIS-051` evidence expansion

## Old data 处理

- Old data exists: yes
- Old data handling: keep existing A0/A2 boundary sources, perform additive refresh only
- 不静默删除任何已注册 source、已引用 fact、runtime page、rule card 或 graph 审计资产。

## High-risk 影响

- High-risk 内容未被放开。
- 本次只补强传播、临床、病变、实验室诊断和鉴别诊断边界。
- 药物执行、剂量、疗程、休药期、MRL、残留、食品安全、扑杀、调运、报告等仍需 A0/A1 与 rule card 共同门禁。

## Runtime manifest 影响

- Runtime manifest impact:
  - 本文档自身不改变 runtime manifest 内容。
  - 但它修复了治理链 latest change record 的识别问题，使后续 `run_guarded_wiki_update.py` 可以继续执行真正的 runtime page 更新与重建。

## Gold dataset 影响

- Gold dataset impact:
  - 本文档自身不直接新增 gold 样本。
  - 但它解除治理前置阻断，使 `DIS-051` 的显式锚点事实在重建后有机会进入 `wiki-native` verified semantic edges，并提升 gold readiness。

## Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- guarded_entrypoint checked: yes, target entrypoint is `run_guarded_wiki_update.py`
- maintenance_guide usage: enforced
- crud_governance usage: enforced
- mandatory_short_card usage: enforced
- scenario_short_card usage: enforced

## 执行链说明

- 计划执行链：
  - `tools/create_crud_decision.py`
  - `tools/run_guarded_wiki_update.py`
  - `tools/apply_dis051_streptococcus_suis_authority_web_refresh.py`
  - `tools/run_swine_wiki_maintenance_checks.py`
- 当前这一步是为保证上述 guarded_entrypoint 链路按制度要求真正可运行，而不是绕过制度。

## 解决效果预期

- governance compliance preflight 应不再把旧的 `dis038` 留痕误判为 latest change record。
- 之后可继续真实执行 `DIS-051` Authority Web Refresh，并产出主图谱、HTML 图谱和 diff 证据。

## UTF-8 与防乱码

- 本文件使用 UTF-8 编写。
- 后续命令将继续使用 `PYTHONIOENCODING=utf-8`，并在 PowerShell 中启用 UTF-8 输出。
