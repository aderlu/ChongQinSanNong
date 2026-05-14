# DIS-059 猪隐孢子虫病权威来源补充与知识图谱更新记录

## 本次问题

- DIS-059 原页面为 `evidence_coverage: partial`，证据缺口明确列出传播途径、实验室诊断、鉴别诊断和防控要点等内容。
- 原页面存在旧模板残留：`source_trust: $sourceTrust; legacy_evidence_status=$legacy`，会降低页面可读性和汇报可信度。
- 原有临床症状证据主要是括号式来源锚点，缺少 `fact_id/source_id/anchor` 三件套，因此不能稳定生成 verified 语义关系边。

## 修改前数据与代码状态

- 数据页：`wiki/diseases/DIS-059-cryptosporidiosis-protozoa.md`
- 原 frontmatter 来源：`SRC-0001, SRC-0081`
- 原图谱状态：`wiki/wiki-native-graph.json`
- 构图代码：`tools/build_wiki_native_graph_mvp.py`
- 关系边规则：只有 evidence unit 同时具备 `fact_id/source_id/anchor/evidence_text/supporting_span`，并满足 predicate registry 和 rule card 要求，语义边才可进入 `verified`。

## 本次新增或更新

- 新增来源页：
  - `wiki/sources/A2-MERCK-CRYPTOSPORIDIOSIS-ANIMALS-2026.md`
  - `wiki/sources/A2-CORNELL-AHDC-CRYPTOSPORIDIUM-PARASITOLOGY-2026.md`
  - `wiki/sources/A2-IOWA-STATE-SWINE-PARASITOLOGY-2026.md`
  - `wiki/sources/A2-IOWA-STATE-PARASITOLOGY-SERVICES-2026.md`
- 更新实体页：
  - `wiki/diseases/DIS-059-cryptosporidiosis-protozoa.md`
- 新增 evidence units：
  - 病原与分类
  - 临床症状
  - 传播途径
  - 实验室诊断
  - 鉴别诊断
  - 防控要点
  - 用药/处置边界
- 新增 rule card frontmatter 引用：
  - `RC-CITATION-001`
  - `RC-DX-001`
  - `RC-DRUG-001`
  - `RC-DISEASE-REGULATORY-001`
  - `RC-WITHDRAWAL-MRL-001`

## 解决的问题

- 将“有来源但不能入 verified 语义边”的旧括号来源，升级为可被构图器识别的 `fact_id/source_id/anchor` 证据单元。
- 对诊断类边绑定 `RC-DX-001`，避免实验室检测结果被直接外推为疾病因果结论。
- 用 Iowa State 和 Cornell 的诊断解释规则，补强“阳性不等于病因、单样本不代表猪群、结果不一致需复核”的反幻觉边界。
- 对治疗相关内容只保留支持疗法和标签边界，不生成具体药物处方、剂量、疗程、休药期或 MRL。

## 预计更新效果

- DIS-059 将从 2 个 evidence units 增加到多条 source-anchored evidence units。
- 知识图谱将新增来源节点、证据边、治理边和 DIS-059 相关语义边。
- 新增语义边将可在 HTML 图谱中检索并展开，支持关系追溯到来源、anchor 和 evidence text。

## 乱码防护

- 所有新增和修改文件均按 UTF-8 写入。
- 后续验证需运行 `tools/audit_encoding_integrity.py`，确认没有新增乱码风险。

## 验证结果

- 已执行：`tools/normalize_wiki_entity_status.py`，输出 `normalized_files=0`，说明本次新增状态字段已符合规范。
- 已执行：`tools/build_wiki_native_graph_mvp.py --phase all`，输出 `status=pass`。
- 已执行：`tools/render_wiki_native_graph.py`，重新生成 `wiki/wiki-native-knowledge-graph.html` 与 `wiki/wiki-native-knowledge-graph-audit.html`。
- 已执行：`tools/audit_encoding_integrity.py`，输出 `mojibake_like_content=0`、`runtime_damaged_count=0`；未发现新增运行时乱码损伤。
- 构图前后变化：
  - 节点：5902 -> 5936
  - 边：6240 -> 6279
  - evidence units：2372 -> 2385
  - semantic edges：98 -> 112
  - verified semantic edges：70 -> 84
  - DIS-059 evidence units：2 -> 15
  - DIS-059 semantic edges：0 -> 14，且全部 `status=verified`
- 2026-05-13 补充修正：发现 `wiki-native-knowledge-graph.html` 的“图谱构建日志”只显示总量，不显示本轮新增节点/边。原因是 wiki-native 渲染器没有接入 native 图谱 diff，而旧 `graph_change_diff_last.json` 只针对 legacy `graph-data.json`。
- 已新增 `issues/wiki_native_graph_change_diff_last.json`，并更新 `tools/render_wiki_native_graph.py`，使主图日志能显示本次 DIS-059 的节点、边和 evidence unit 增量。
