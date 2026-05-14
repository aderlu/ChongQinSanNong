# Wiki 实体页状态简化与清洗总记录

时间：2026-05-12

## 一、修改前存在的问题

Wiki 实体页中长期累积了多套状态描述，包括 `legacy_evidence_status`、`gold_dataset_use`、`Runtime task use`、`gold dataset role`、`页面状态`、`可用边界`、`boundary_only`、`positive_label_candidate` 等。由于所有数据来源理论上均来自权威官网、权威文献和权威书籍，这些状态不应继续混合表达“来源是否可信”“页面覆盖是否完整”“任务能否使用”等不同含义。

主要问题：

1. 状态字段过多，含义重叠。
2. 页面正文中重复出现运行时说明，降低实体页可读性。
3. 构建图谱时只能展示旧状态，无法形成统一的使用范围判断。
4. 药物、处方、MRL、监管等高风险边界需要保留，但不应和普通页面状态混在一起。

## 二、修改前代码状态

构建脚本 `tools/build_wiki_native_graph_mvp.py` 原先只读取：

- `legacy_evidence_status`
- `task_use_status`
- `gold_dataset_use`
- `risk_class`

可视化脚本 `tools/render_wiki_native_graph.py` 也主要展示这些旧状态字段。

## 三、本次修改内容

### 1. 三个子智能体并行清洗

- Worker A：负责 `wiki/diseases` 疾病实体页。
- Worker B：负责 `wiki/drugs` 药物实体页。
- Worker C：负责 `wiki/comparisons`、`wiki/syndromes`、`wiki/synthesis`。

对应子任务留痕：

- `knowledge_change_records/2026-05-12-disease-status-cleanup-worker-a.md`
- `knowledge_change_records/2026-05-12-worker-b-drugs-status-cleanup.md`
- `knowledge_change_records/2026-05-12_worker_c_status_cleanup.md`

### 2. 新增统一状态配置

新增文件：

- `config/wiki_entity_usage_schema.json`

统一模型：

```yaml
source_trust: authoritative | needs_source_check
evidence_coverage: complete | partial | minimal
usage_scope: [retrieval, diagnosis_support, differential_support, drug_boundary, gold_candidate, gap_routing, audit_only, ...]
```

### 3. 新增确定性规范化脚本

新增文件：

- `tools/normalize_wiki_entity_status.py`

作用：

1. 为实体页补齐 `source_trust/evidence_coverage/usage_scope`。
2. 将旧状态值映射为固定枚举。
3. 删除或压缩重复的运行时状态模板行。
4. 不删除事实证据、source/fact/anchor、药物禁用、剂量、休药期、MRL、监管边界等医学安全内容。

### 4. 更新图谱构建脚本

修改文件：

- `tools/build_wiki_native_graph_mvp.py`

新增能力：

1. 读取 `config/wiki_entity_usage_schema.json`。
2. 兼容旧字段并统一输出新状态模型。
3. 即使页面仍有历史字段，也能规范化为 `source_trust/evidence_coverage/usage_scope`。
4. 保留 legacy 子字段用于追溯，但不作为主要显示字段。

### 5. 更新可视化脚本

修改文件：

- `tools/render_wiki_native_graph.py`

新增能力：

1. 节点详情优先展示 `usage_scope`、`source_trust`、`evidence_coverage`。
2. 旧状态只以 compact legacy 形式保留，降低视觉噪声。

### 6. 补齐无 frontmatter 矩阵页

为 6 个矩阵页补充最小 frontmatter：

- `wiki/comparisons/veterinary_rational_use_1_200_antimicrobial_combination_matrix.md`
- `wiki/comparisons/veterinary_rational_use_201_400_symptomatic_drug_boundary_matrix.md`
- `wiki/comparisons/veterinary_rational_use_401_600_tcm_symptom_differential_matrix.md`
- `wiki/synthesis/veterinary_rational_use_1_200_drug_disease_rule_matrix.md`
- `wiki/synthesis/veterinary_rational_use_201_400_system_drug_disease_rule_matrix.md`
- `wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`

## 四、修改后解决的问题

1. 页面状态从多套历史标签收敛为三个统一字段。
2. 所有目标实体页和矩阵页均具备统一状态字段。
3. 来源权威性不再反复用 `HUMAN_REVIEWED` 等历史字段表达，默认统一为 `source_trust: authoritative`。
4. 页面覆盖程度统一为 `evidence_coverage: complete|partial`。
5. 页面任务用途统一由 `usage_scope` 表达。
6. 高风险医学边界仍保留在正文中，不因简化状态而丢失。
7. 图谱构建和 HTML 可视化均已适配新状态模型。

## 五、清洗覆盖结果

最终核查：

- 疾病页：73 个
- 药物页：81 个
- 比较页：17 个
- 综合征页：22 个
- 综合页：27 个
- 合计：220 个目标页面

字段覆盖：

- `source_trust`：220/220
- `evidence_coverage`：220/220
- `usage_scope`：220/220

最终状态分布：

- `source_trust=authoritative`：220
- `evidence_coverage=complete`：180
- `evidence_coverage=partial`：40

## 六、验证结果

已执行：

```powershell
py -m py_compile tools/build_wiki_native_graph_mvp.py tools/render_wiki_native_graph.py tools/normalize_wiki_entity_status.py
py tools/build_wiki_native_graph_mvp.py --phase all
py tools/render_wiki_native_graph.py
py tools/audit_encoding_integrity.py
```

结果：

- Python 编译通过。
- 图谱构建通过，`status=pass`。
- HTML 主图和完整审计图重新生成通过。
- 编码审计通过，`mojibake_like_content=0`，`runtime_damaged_count=0`。

当前图谱输出：

- `wiki/wiki-native-graph.json`
- `wiki/wiki-native-knowledge-graph.html`
- `wiki/wiki-native-knowledge-graph-audit.html`

## 七、预计效果

1. GPT 后续读取实体页时，状态判断更简单，减少误解。
2. 图谱节点详情更清晰，减少历史状态噪声。
3. 页面来源可信、证据覆盖、使用范围三者分离，系统复杂度下降。
4. 高风险关系仍由边级证据链、rule card、source alignment 和后续 medical entailment 保证严谨性。
5. 后续新增页面只需要填写三字段，降低维护成本。

## 八、编码措施

本次所有脚本和文档均使用 UTF-8 读写。PowerShell 执行前设置：

```powershell
$env:PYTHONIOENCODING='utf-8'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8
```

未引入新的乱码问题。
