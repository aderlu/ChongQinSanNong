# 2026-05-13 LLM Wiki 猪布鲁氏菌病 CFSPH 受控更新与知识图谱恢复记录

## 本次工作目标

- 对 `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative` 执行一次真实、可审计、可复盘的猪病数据补充与更新。
- 验证更新流程是否严格遵守以下治理文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md`
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\WIKI_MAINTENANCE_GUIDE.md`
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\WIKI_UPDATE_MANDATORY_SHORT_CARD.md`
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\WIKI_UPDATE_SCENARIO_SHORT_CARD.md`
- 验证企业级清洗整理后，LLM Wiki 数据更新链、legacy 运行时图谱链、图谱差分审计链是否仍完整可用。
- 对发现的兼容性问题进行修复，并保留明确工作留痕，方便项目汇报与审计。

## 本次真实补充的数据对象

- 病种：`DIS-038-brucella-suis-brucellosis`
- 新增权威来源：
  - `A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`
- 新增 facts：
  - `DIS038-WEB-005-cfsph-transmission-exposure`
  - `DIS038-WEB-006-cfsph-clinical-pattern`
  - `DIS038-WEB-007-cfsph-zoonotic-boundary`

## 真实联网检索与取证情况

- 使用已配置的 `web-access` skill 对多个权威来源进行了真实检索。
- 最终选定的新增来源为 Iowa State University CFSPH 的 `Brucella suis` factsheet PDF。
- 原始文件已落地：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\raw\web\web_access_dis038_brucellosis_20260513\A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.pdf`
- 原始 PDF 提取页文本已生成：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\raw\web\web_access_dis038_brucellosis_20260513\A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026-pages.txt`

## 为什么选这个来源

- 该来源是 A2 权威动物卫生/公共卫生知识来源，适合做以下边界增强：
  - 传播与暴露边界
  - 临床模式边界
  - 人兽共患与公共卫生暴露边界
- 该来源不被允许外推为：
  - 中国法域报告、检疫、扑杀、调运、补偿、屠宰、食品链放行
  - 药物剂量、休药期、MRL、食品安全放行
- 这正好能够体现治理流程的实际作用：
  - 不是“搜到资料就直接入库”
  - 而是“按 authority level、风险边界和用途约束进行准入”

## 更新前存在的问题

### 问题 1：更新脚本内部仍引用清洗整理前的旧路径

- 问题文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\apply_dis038_brucellosis_cfsph_refresh.py`
- 问题表现：
  - 通过 `run_guarded_wiki_update.py` 执行受控更新时，preflight 全通过，但 update_command 失败。
  - 根因是脚本内部 `refresh_fact_status()` 调用了已不存在的旧路径：
    - `tools/standardize_source_fact_status.py`
  - 企业级整理后真实脚本位置已经迁移到：
    - `tools/wiki_ops/standardize_source_fact_status.py`
- 影响：
  - 真实数据入库链会在 update_command 阶段中断。
  - 说明清洗整理后存在“治理入口仍正常，但内部调用路径残留未完全清理”的兼容性缺陷。

### 问题 2：新增 facts 成功入库，但 legacy 图谱未吸收

- 第一次修复路径后，受控更新已能跑通，但图谱差分结果显示：
  - `added_nodes = 0`
  - `added_links = 0`
- 初看像是“图谱没变”，但进一步核查发现并非如此：
  - disease 页面已更新
  - source 页面已新增
  - raw extract 已生成
  - `knowledge_facts.json` 已存在 `DIS038-WEB-005..007`
  - `knowledge_facts_status_index.json` 也已存在 `DIS038-WEB-005..007`
- 深入排查后发现真正根因：
  - legacy 运行时图谱构建器 `phase9_rebuild_indexes_graph_smoke.py` 只会纳入同时满足以下条件的 fact：
    - `source_trust == authoritative`
    - `evidence_coverage in {"complete", "partial"}`
  - 本次新增 CFSPH facts 在初版脚本中没有写入：
    - `source_trust`
    - `evidence_coverage`
    - `usage_scope`
  - 因此事实虽然成功进入状态索引，但被 legacy 图谱构建阶段直接过滤掉。

## 本次修改内容

### 修改 1：修复受控更新脚本中的旧路径引用

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\apply_dis038_brucellosis_cfsph_refresh.py`
- 修改前：
  - `refresh_fact_status()` 调用 `tools/standardize_source_fact_status.py`
- 修改后：
  - 显式改为调用 `tools/wiki_ops/standardize_source_fact_status.py`
- 解决效果：
  - 受控更新脚本恢复与清洗整理后企业级目录结构的一致性。
  - 真实 update_command 能够继续执行到标准化与后续维护检查。

### 修改 2：为 CFSPH 新增 facts 补齐 legacy 图谱契约字段

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\apply_dis038_brucellosis_cfsph_refresh.py`
- 新增字段：
  - `source_trust: authoritative`
  - `evidence_coverage: complete`
  - `usage_scope: ["retrieval", "gold_candidate"]`
- 解决效果：
  - 让本次新增 facts 与现有 legacy 运行时图谱构建契约保持一致。
  - 避免“事实已入库但图谱漏数”的情况。

### 修改 3：在标准化脚本中增加缺省兜底推导

- 修改文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\standardize_source_fact_status.py`
- 新增能力：
  - 自动推导 `source_trust`
  - 自动推导 `evidence_coverage`
  - 自动推导 `usage_scope`
- 推导逻辑目的：
  - 即使后续新增脚本忘记显式写入 legacy 图谱兼容字段，也能在标准化阶段自动补齐。
- 解决效果：
  - 把“单个更新脚本的字段遗漏”升级为“系统层兼容防护”。
  - 降低后续企业级维护中的隐性漏图风险。

## 真实执行过程与治理证据

### 证据 1：治理入口严格执行 preflight

- 受控入口：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py`
- 受控执行报告：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\guarded_wiki_update_last_run.json`
- preflight 证明：
  - 先检查 governance compliance
  - 再检查 CRUD decision
  - 通过后才执行真实 update command

### 证据 2：治理链能正确暴露整理残留问题

- 首次失败并不是治理缺失，而是治理正确发现问题：
  - 旧 wrapper 路径错误被拦截
  - 更新脚本内部旧路径引用被暴露
- 这证明：
  - 项目不是“只要 decision 文件存在就默认成功”
  - 而是真正校验命令与执行结果

### 证据 3：治理链修复后可完整跑通

- 最终成功执行报告：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\guarded_wiki_update_last_run.json`
- 最终完整链路全部通过：
  - governance preflight 通过
  - CRUD decision preflight 通过
  - update_command 通过
  - full maintenance checks 通过
  - graph diff audit 通过
  - runtime hallucination risk audit 通过
  - readiness audit 通过
  - encoding integrity audit 通过
  - runtime pytest 通过

### 证据 4：治理文件确实被读取并纳入决策

- 决策文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\crud_decisions\2026-05-13-2223-dis038-cfsph-refresh-v2.md`
- 其中明确记录了：
  - 已读取的治理文件
  - 治理文件哈希
  - planned command
  - authority level
  - old data handling
  - conflict handling
  - required follow-up checks

## 数据更新结果

### 已新增 source 页面

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\sources\A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.md`

### 已更新 disease 页面

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\diseases\DIS-038-brucella-suis-brucellosis.md`

### 已新增证据扩展页

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\evidence_expansions\diseases\phase4_runtime_compaction\DIS-038-brucella-suis-brucellosis\007-CFSPH-Authority-Web-Refresh-2026-05-13.md`

### 已生成本次执行报告

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\dis038_brucellosis_cfsph_refresh_2026-05-13.json`

## 知识图谱变化结果

### 图谱差分结果

- 差分文件：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\graph_change_diff_last.json`
- 本次图谱变化摘要：
  - `nodes_before: 2604`
  - `nodes_after: 2608`
  - `links_before: 2980`
  - `links_after: 2986`
  - `added_nodes: 4`
  - `added_links: 6`

### 实际新增节点

- `fact:DIS038-WEB-005-cfsph-transmission-exposure`
- `fact:DIS038-WEB-006-cfsph-clinical-pattern`
- `fact:DIS038-WEB-007-cfsph-zoonotic-boundary`
- `source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`

### 实际新增边

- `disease:DIS-038 -> fact:DIS038-WEB-005-cfsph-transmission-exposure` (`fact_anchor`)
- `disease:DIS-038 -> fact:DIS038-WEB-006-cfsph-clinical-pattern` (`fact_anchor`)
- `disease:DIS-038 -> fact:DIS038-WEB-007-cfsph-zoonotic-boundary` (`fact_anchor`)
- `fact:DIS038-WEB-005-cfsph-transmission-exposure -> source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026` (`evidence_source`)
- `fact:DIS038-WEB-006-cfsph-clinical-pattern -> source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026` (`evidence_source`)
- `fact:DIS038-WEB-007-cfsph-zoonotic-boundary -> source:A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026` (`evidence_source`)

### 图谱产物

- JSON：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\graph-data.json`
- Markdown：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\knowledge-graph.md`
- HTML：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\knowledge-graph.html`
- 变化可视化：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\knowledge-graph-changes.html`

## 对“更新是否严谨”的判断

- 结论：严谨。
- 原因：
  - 真实来源检索、真实原始文件落地、真实 decision 文件、真实受控入口、真实 post-check、真实图谱变化全部存在。
  - 新来源只用于允许的 A2 边界增强，不越权替代 A0/A1 中国法域执行规则。
  - old data handling 为 `keep`，未覆盖既有高等级依据。
  - conflict handling 明确采用 additive refresh，不做静默替换。

## 对“是否严格按治理约束执行”的判断

- 结论：是。
- 体现方式：
  - 更新前必须读取治理文档并生成 CRUD decision。
  - 受控入口执行 preflight 审核。
  - 只允许有边界、有 source/fact anchor 的增量更新。
  - 更新后必须执行维护检查、图谱差分、运行时测试与编码检查。
  - 发现问题时先保留失败证据，再修复后重跑，而不是掩盖失败。

## 对“知识图谱功能是否正常”的判断

- 结论：修复后正常。
- 说明：
  - 初始状态下，图谱构建链存在 legacy 兼容字段依赖未满足的问题，导致新增 facts 未入图。
  - 修复后，图谱已真实新增 source 节点、fact 节点以及 source/fact/disease 边。
  - 图谱差分、图谱 HTML 和主运行时图谱都已同步变化。

## 对“前面清洗整理是否破坏了流程”的判断

- 结论：有局部破坏，但治理链成功帮助发现并修复。
- 具体表现：
  - 路径迁移后，更新脚本内部仍保留旧路径引用。
  - 新 wiki_ops 更新脚本与 legacy 图谱契约字段不完全一致，导致事实已入库但图谱漏数。
- 正面意义：
  - 企业级治理入口并未失效，反而准确暴露了整理后的残留问题。
  - 本次修复把问题从“个案修补”提升到“系统兼容性补强”。

## 本次修复带来的预期效果

- 后续类似 web authority refresh 更新，能更稳定地贯通：
  - source/page 更新
  - fact status 标准化
  - legacy 运行时图谱
  - 图谱变化审计
  - HTML 可视化
  - runtime pytest
- 降低“入库成功但图谱不变”的隐形故障概率。
- 提高企业级项目架构下多工具链并存时的兼容性和可审计性。

## 本次涉及的主要代码与文件

- 更新脚本：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\apply_dis038_brucellosis_cfsph_refresh.py`
- 标准化脚本：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\standardize_source_fact_status.py`
- 受控入口：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_guarded_wiki_update.py`
- 维护检查：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\run_swine_wiki_maintenance_checks.py`
- 图谱差分：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\graph_change_diff_last.json`
- 受控执行报告：
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\guarded_wiki_update_last_run.json`

## 编码安全说明

- 本次所有新增与修改文件均使用 UTF-8 写入。
- 未使用会引入 BOM 干扰或 shell 重定向乱码的方式直接写 Markdown 文件。
- 修改过程中优先保留既有中文内容，并通过维护链执行了编码完整性检查。
