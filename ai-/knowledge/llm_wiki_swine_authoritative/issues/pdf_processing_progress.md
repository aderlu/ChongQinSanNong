# Diseases of Swine PDF 分批处理进度

## 更新时间

- 首次目录级建库：2026-05-06，处理 PDF page 1-12。
- Formal Batch 001 完成时间：2026-05-06 16:34:49 +08:00。
- 本进度文档确认更新时间：2026-05-06 16:37:16 +08:00。
- Formal Batch 007 增量更新时间：2026-05-06 17:56:16 +08:00。

## 当前状态

- PDF 总页数：1132
- 文件：`docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman, Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf`
- 已完成批次：
  - Batch 0：PDF page 1-12，目录级覆盖建模。
  - Formal Batch 001：PDF page 13-40，来源元数据与 Chapter 1 Herd Evaluation 正式构建。
  - Formal Batch 002-006：PDF page 41-181，Chapter 2-9 正式构建。
  - Formal Batch 007：PDF page 182-220，Chapter 10-11 正式构建。
- 当前正式落库：
  - `SRC-0001` 至 `SRC-0013`。
  - `wiki/rules/RULE-001` 到 `RULE-070`。
  - `issues/formal_batch_001_candidate_facts.json` 至 `issues/formal_batch_007_candidate_facts.json`。
  - `issues/formal_batch_001_cross_review.md` 至 `issues/formal_batch_007_cross_review.md`。
  - `exports/knowledge_facts.json` 当前共 362 条 facts，其中 216 条为 `HUMAN_REVIEWED` 正式事实，146 条目录级 facts 保持 `NEEDS_REVIEW`。

## Formal Batch 001 实施说明

处理范围：

- PDF page 13-22：Contributors。只记录为来源元数据，不生成疾病事实。
- PDF page 23：Editors' Note。只记录为来源元数据，不生成疾病事实。
- PDF page 24：Acknowledgments。只记录为来源元数据，不生成疾病事实。
- PDF page 25：Section I Veterinary Practice 起始页。
- PDF page 27-40：Chapter 1 Herd Evaluation 正文、表格、采样说明和参考文献。

落库内容：

- `wiki/sources/SRC-0002-diseases-of-swine-11e-contributors-editors-note.md`
- `wiki/sources/SRC-0003-diseases-of-swine-11e-chapter-1-herd-evaluation.md`
- `wiki/topics/Swine-herd-evaluation-and-field-investigation.md`
- `wiki/rules/Swine-herd-evaluation-records-and-reporting.md`
- `wiki/rules/Swine-four-circle-herd-evaluation.md`
- `wiki/rules/Swine-diagnostic-sampling-selection.md`
- `wiki/rules/Swine-intervention-prioritization.md`
- `wiki/rules/Swine-oral-fluid-sample-submission.md`

正式 facts：

- 新增 20 条 `HUMAN_REVIEWED` facts。
- 每条 fact 均包含 `evidence_source_id=SRC-0003`。
- 每条 fact 均包含 `evidence_quote_span=Chapter 1 Herd Evaluation; PDF page xx`。
- 本批 facts 只覆盖猪群评估、记录核验、报告结构、生物安全、四圈评估、流行程度估计、代表性采样、剖检对象选择、开放式访谈、干预优先级和口腔液样本提交。

明确未构建：

- 未构建任何药方。
- 未构建任何药物剂量。
- 未构建任何休药期。
- 未构建任何中国监管处置、扑杀、封锁、上报或调运规则。
- 未完善具体疾病页正文。

## 交叉审查记录

审查文件：`issues/formal_batch_001_cross_review.md`

审查结论：

- 页码锚点核验通过：正式 facts 均锚定 `SRC-0003` 和具体 PDF page。
- 内容边界核验通过：本批不生成药方、剂量、休药期或监管处置结论。
- 一致性核验通过：facts 与 topic/rule 页面一致，`applies_to_species` 均为 `swine`，正式 facts 均为 `HUMAN_REVIEWED`。

## 验证结果

已运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪群评估 急性 未治疗 采样 四圈评估" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

结果：

- `status`：`fact_count=166`，`disease_count=73`，`rule_count=5`。
- evidence status：`HUMAN_REVIEWED=20`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构错误；剩余 warning 全部为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回猪群评估 topic、四圈评估规则、代表性急性未治疗采样规则。
- `graph-build`：图谱已更新为 `181 nodes / 405 links`。

## 截至位置

下一次应从 PDF page 41 开始。

推荐下一批：PDF page 41-65，处理 Chapter 2 Behavior and Welfare。该批应优先生成 welfare/topic/rule facts，不生成药方。

## 质量规则

- 没有 PDF 章节和页码锚点的事实不得落库。
- 药方、剂量、休药期、监管处置必须等待相应章节和 A0/A1 来源复核。
- 每批先写候选事实和交叉审查记录，通过后再合并到 `exports/knowledge_facts.json`。

## Formal Batch 002 实施记录

- 完成时间：2026-05-06 16:45:00 +08:00。
- 处理范围：PDF page 41-65。
- 章节：Section I Veterinary Practice / Chapter 2 Behavior and Welfare。
- 新增来源：`SRC-0004`。
- 新增主题页：`wiki/topics/Swine-behavior-welfare-and-pain-management.md`。
- 新增规则页：`RULE-006` 至 `RULE-012`。
- 新增候选事实：`issues/formal_batch_002_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_002_cross_review.md`。
- 正式落库 facts：25 条 `HUMAN_REVIEWED` facts。
- 所有正式 facts 均锚定 `SRC-0004; Chapter 2 Behavior and Welfare; PDF page xx`。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 002 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 welfare/behavior/hospital pen/euthanasia protocol facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 002 验证结果

已运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪福利 咬尾 病弱猪 护理栏 安乐死" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

结果：

- `status`：`fact_count=191`，`disease_count=73`，`rule_count=12`。
- evidence status：`HUMAN_REVIEWED=45`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构错误；剩余 warning 全部为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回护理栏转移、福利三域评估、安乐死 protocol、咬尾风险和疾病行为规则。
- `graph-build`：图谱已更新为 `226 nodes / 455 links`。

## 截至位置更新

- 当前已处理至 PDF page 65。
- 下一次应从 PDF page 66 开始。
- 推荐下一批：PDF page 66-73，处理 Chapter 3 Genetics and Health。

## Formal Batch 003 实施记录

- 完成时间：2026-05-06 16:55:00 +08:00。
- 处理范围：PDF page 66-98。
- 章节：Chapter 3 Genetics and Health；Chapter 4 Effect of Environment on Health；Chapter 5 Differential Diagnosis of Diseases。
- 新增来源：`SRC-0005`、`SRC-0006`、`SRC-0007`。
- 新增主题页：遗传健康、环境健康、按系统/年龄鉴别诊断 3 个 topic。
- 新增规则页：`RULE-013` 至 `RULE-021`。
- 新增候选事实：`issues/formal_batch_003_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_003_cross_review.md`。
- 正式落库 facts：24 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 003 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 genetics/environment/differential diagnosis facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 003 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 鉴别诊断 呼吸 繁殖损失 人兽共患" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=215`，`disease_count=73`，`rule_count=21`。
- 证据状态：`HUMAN_REVIEWED=69`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回繁殖损失鉴别诊断、人兽共患风险提示、鉴别诊断 topic 与相关 rule。
- `graph-build`：已重建图谱，`282 nodes / 503 links`。

## 截至位置更新

- 当前已处理至 PDF page 98。
- 下一次应从 PDF page 99 开始。
- 推荐下一批：PDF page 99-121，处理 Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。

## Formal Batch 004 实施记录

- 完成时间：2026-05-06 17:09:00 +08:00。
- 处理范围：PDF page 99-121。
- 章节：Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。
- 新增来源：`SRC-0008`。
- 新增主题页：诊断测试选择与结果解释、实验室方法与性能边界 2 个 topic。
- 新增规则页：`RULE-022` 至 `RULE-029`。
- 新增候选事实：`issues/formal_batch_004_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_004_cross_review.md`。
- 正式落库 facts：26 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 004 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 diagnostic tests/test performance/interpretation facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 004 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 PCR 药敏 诊断测试 阳性 阴性 解释" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=241`，`disease_count=73`，`rule_count=29`。
- 证据状态：`HUMAN_REVIEWED=95`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回诊断测试选择与结果解释 topic，以及单项检测不得直接定病因、PCR 阳性不等于活病原、细菌培养解释边界等 rule。
- `graph-build`：已重建图谱，`343 nodes / 555 links`。

## 截至位置更新

- 当前已处理至 PDF page 121。
- 下一次应从 PDF page 122 开始。
- 推荐下一批：PDF page 122-146，合并处理 Chapter 7 和 Chapter 8。

## Formal Batch 005 实施记录

- 完成时间：2026-05-06 17:14:00 +08:00。
- 处理范围：PDF page 122-146。
- 章节：Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value；Chapter 8 Collecting Evidence and Establishing Causality。
- 新增来源：`SRC-0009`、`SRC-0010`。
- 新增主题页：样本选择采集与提交、证据因果与监测解释 2 个 topic。
- 新增规则页：`RULE-030` 至 `RULE-041`。
- 新增候选事实：`issues/formal_batch_005_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_005_cross_review.md`。
- 正式落库 facts：36 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 005 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 sample selection/submission/evidence/causality/surveillance facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 005 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 样本 采集 送检 因果 监测 阴性" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=277`，`disease_count=73`，`rule_count=41`。
- 证据状态：`HUMAN_REVIEWED=131`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回样本选择采集与提交 topic、证据因果与监测解释 topic，以及全阴性监测解释、因果近因/终因、疾病诊断 vs 监测采样等 rule。
- `graph-build`：已重建图谱，`429 nodes / 627 links`。

## 截至位置更新

- 当前已处理至 PDF page 146。
- 下一次应从 PDF page 147 开始。
- 推荐下一批：PDF page 147-181，处理 Chapter 9 Disease Control, Prevention, and Elimination。


## Formal Batch 006 实施记录

- 完成时间：2026-05-06 17:21:00 +08:00。
- 处理范围：PDF page 147-181。
- 章节：Chapter 9 Disease Control, Prevention, and Elimination。
- 新增来源：`SRC-0011`。
- 新增主题页：疾病生态传播与控制框架、生物安全与风险管理 2 个 topic。
- 新增规则页：`RULE-042` 至 `RULE-055`。
- 新增候选事实：`issues/formal_batch_006_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_006_cross_review.md`。
- 正式落库 facts：40 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、扑杀补偿、具体法定疫病处置方案。

### Formal Batch 006 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 disease ecology/transmission/control/biosecurity/risk management facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 006 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 生物安全 传播 清除 引种 隔离 饲料 运输" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=317`，`disease_count=73`，`rule_count=55`。
- 证据状态：`HUMAN_REVIEWED=171`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回生物安全与风险管理 topic，以及饲料、运输、人员、HACCP、引种隔离和风险管理相关 rule。
- `graph-build`：已重建图谱，`523 nodes / 707 links`。

## 截至位置更新

- 当前已处理至 PDF page 181。
- 下一次应从 PDF page 182 开始。
- 推荐下一批：PDF page 182-220，合并处理 Chapter 10 和 Chapter 11。

## Formal Batch 007 实施记录

- 完成时间：2026-05-06 17:56:16 +08:00。
- 处理范围：PDF page 182-220。
- 章节：Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis；Chapter 11 Anesthesia and Surgical Procedures in Swine。
- 新增来源：`SRC-0012`、`SRC-0013`。
- 新增主题页：`wiki/topics/Swine-drug-therapy-antimicrobial-stewardship.md`、`wiki/topics/Swine-anesthesia-analgesia-and-surgery-boundaries.md`。
- 更新主题页：`wiki/topics/Swine-medication-legality-and-withdrawal.md`。
- 新增规则页：`RULE-056` 至 `RULE-070`。
- 新增候选事实：`issues/formal_batch_007_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_007_cross_review.md`。
- 正式落库 facts：45 条 `HUMAN_REVIEWED` facts。
- 所有正式 facts 均锚定 `SRC-0012` 或 `SRC-0013` 及具体 PDF page。
- 明确未落库：具体药方、药物剂量、麻醉方案、手术步骤、具体休药期、禁限用药清单、中国监管处置。

### Formal Batch 007 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖用药原则、抗菌药审慎使用、药敏解释、麻醉镇痛风险、监测支持、疼痛管理和手术决策边界。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。
- 编码复核：通过。新增 batch 007 中文内容已确认可被 query 正常召回。

### Formal Batch 007 验证结果

已完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "抗菌药 药敏 CLSI 休药期 恶性高热 CO2 去势 镇痛" --top-k 8
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

- `status`：`fact_count=362`，`disease_count=73`，`rule_count=70`。
- 证据状态：`HUMAN_REVIEWED=216`，`NEEDS_REVIEW=146`。
- `lint`：`ok=True`，无结构性错误；剩余 warnings 均为目录级 `NEEDS_REVIEW` facts。
- `query`：可召回恶性高热风险、抗菌药预防用药、猪用药治疗与抗菌药审慎使用、休药期标签/法规边界、药敏解释边界等新增内容。
- `graph-build`：已重建图谱，`630 nodes / 797 links`。

## 截至位置更新

- 当前已处理至 PDF page 220。
- 下一次应从 PDF page 221 开始。
- 推荐下一批：PDF page 221-244，合并处理 Chapter 12 和 Chapter 13。

## 后续待处理阶段

- PDF page 221-234：Chapter 12 Preharvest Food Safety, Zoonotic Diseases, and the Human Health Interface。
- PDF page 235-244：Chapter 13 Special Considerations for Show and Pet Pigs。
- PDF page 245-448：Section II Body Systems。
- PDF page 449-766：Section III Viral Diseases。
- PDF page 767-1026：Section IV Bacterial Diseases。
- PDF page 1027-1064：Section V Parasitic Diseases。
- PDF page 1065-1111：Section VI Noninfectious Diseases。
- PDF page 1112-1132：Index。
