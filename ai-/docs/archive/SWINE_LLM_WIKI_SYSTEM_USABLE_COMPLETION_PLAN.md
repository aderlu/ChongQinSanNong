# 猪病 LLM Wiki 系统可用型补全方案

## 目标

本文档用于把当前 `knowledge/llm_wiki_swine_authoritative` 从“教材事实抽取型知识库”补全为“系统可用型知识库”，直接服务猪病数据生成、答案评估、风险拦截、鉴别诊断和监管/用药边界控制。

当前 V4 已完成 `Diseases of Swine 11e` 至 PDF page 1064 的正文抽取，已形成 `knowledge_facts.json`、`sources`、`rules` 和部分 `topics`。主要缺口是：

- `diseases/*.md` 仍有大量目录级空壳字段，如传播途径、临床症状、剖检变化、实验室诊断、防控要点。
- `drugs/` 尚未形成教材证据页和中国合规页。
- `rule_cards/` 尚未把长规则转成系统可调用的评估卡片。
- `syndromes/` 尚未形成按临床场景组织的鉴别诊断入口。
- `synthesis/` 尚未形成供数据生成和评估使用的二级总结页。
- 中国监管、法定病种、禁用药、休药期、公共卫生/食品安全执行结论缺少 A0/A1 权威来源。

## 原则

1. 不推翻 V4，新增 V5 补全主线。
2. PDF 教材继续作为 A2 来源，只支持疾病机理、临床、病理、诊断、防控边界。
3. 中国监管、禁用药、休药期、强制处置、检疫、食品安全执行必须由 A0/A1 来源支持。
4. 所有补全文本必须回链 `fact_id`、`source_id`、PDF page 或网页 URL。
5. `diseases` 用于病种知识页面，`syndromes` 用于临床入口，`rule_cards` 用于评估器，`synthesis` 用于生成器和评估器的高层上下文。

## 权威来源池

### A0 中国官方来源

1. 农业农村部公告第 573 号：一、二、三类动物疫病病种名录  
   URL: https://xmsyj.moa.gov.cn/gzdt/202206/t20220629_6403635.htm  
   用途：写入 `regulatory_status`、`notifiable_disease_class`、`China` jurisdiction 规则。该公告列出一类动物疫病包含口蹄疫、猪水疱病、非洲猪瘟等；二类猪病包含猪瘟、猪繁殖与呼吸综合征、猪流行性腹泻；三类猪病包含猪细小病毒感染、猪丹毒、猪传染性胸膜肺炎、猪圆环病毒病、猪流感、猪丁型冠状病毒感染、猪痢疾、猪增生性肠病等。

2. 农业农村部《非洲猪瘟常态化防控技术指南（试行版）》  
   URL: https://www.moa.gov.cn/nybgb/2020/202009/202011/t20201124_6356917.htm  
   用途：补充 ASF 中国防控、生物安全、引种隔离、检测、样品运输、阳性处置、饲料和无害化处理风险点。该指南明确引种前健康评估、隔离观察、入场检测、qPCR/PCR 检测、阳性后报告当地畜牧兽医部门并停止生产相关活动等边界。

3. 农业农村部关于食品动物中禁止使用药品及其他化合物清单的政策说明  
   URL: https://www.moa.gov.cn/xw/zwdt/202001/t20200120_6336378.htm  
   用途：建立禁用药 A0 来源，作为 `drugs/`、`rule_cards/` 和评估器硬阻断依据。该来源说明农业农村部公告第 250 号修订发布禁用清单，禁用清单用于规范养殖用药并保障动物源性食品安全。

4. 农业农村部公告第 250 号原文或官方镜像  
   首选：农业农村部原站或部委公报 PDF；备选：地方农业农村局转载页面、FAOLEX 镜像。  
   用途：抽取禁用药清单具体药物条目。只有确认原文或可信官方镜像后，才能把具体药物升为 `China` jurisdiction 的 `BANNED` 规则。

### A1 国际权威来源

1. WOAH African swine fever disease page  
   URL: https://www.woah.org/en/disease/african-swine-fever/  
   用途：补充 ASF 国际 disease card、Terrestrial Code/Manual 链接、全球态势、传播和控制措施。WOAH 明确 ASF 是家猪和野猪高度传染性病毒病，死亡率可达 100%，对人无健康危害，但可通过环境、衣物、车辆和猪肉制品等传播，并要求成员及时向 WOAH 通报。

2. WOAH Foot and mouth disease disease page  
   URL: https://www.woah.org/en/disease/foot-and-mouth-disease/  
   用途：补充 FMD 国际权威边界、水疱病鉴别、国际贸易和通报要求。

3. WOAH Codes and Manuals  
   URL: https://www.woah.org/en/what-we-do/standards/codes-and-manuals/  
   用途：作为 WOAH Terrestrial Code 和 Manual 的入口，补充诊断、通报、贸易、无疫区和生物安全相关规则。

4. WOAH WAHIS  
   URL: https://wahis.woah.org  
   用途：真实疫情数据入口。用于生成 `raw/wahis/` 快照和 `synthesis/global_situation_*`，不直接改写中国处置规则。

## 数据层设计

### facts 分层

继续使用 `exports/knowledge_facts.json`，但 V5 开始强制规范 `fact_type`：

- `transmission`：传播途径、媒介、环境存活、垂直/水平传播。
- `clinical_sign`：临床症状、生产性能、阶段特异表现。
- `lesion_pattern`：剖检变化、组织病理、典型病变。
- `diagnostic_method`：检测方法、样本、实验室方法。
- `diagnostic_boundary`：阳性/阴性解释、假阳性、混合感染、定因条件。
- `differential_diagnosis`：鉴别诊断。
- `control_boundary`：生物安全、隔离、环境控制、饲养管理。
- `treatment_boundary`：教材治疗讨论、不得生成处方边界。
- `drug_evidence`：教材或标签中提及药物，但不代表可用处方。
- `drug_regulatory_status`：中国禁用、限用、处方药、休药期等，必须 A0/A1。
- `notifiable_status`：中国一二三类动物疫病或 WOAH listed disease。
- `public_health_boundary`：人兽共患、食品安全、暴露边界。

### disease 页面补全结构

每个 `wiki/diseases/DIS-*.md` 需要由 facts 自动回填：

```markdown
## 传播途径
- ...

## 临床症状
- ...

## 剖检变化
- ...

## 实验室诊断
- ...

## 鉴别诊断
- ...

## 防控要点
- ...

## 用药/处置边界
- ...

## 中国监管状态
- ...

## 本地证据
- SRC-xxxx / PDF page ...
- A0-xxxx / URL ...
```

页面中的每条 bullets 必须包含来源锚点，例如 `（SRC-0031, PDF page 473-474）` 或 `（A0-MOA-573, 2022-06-29）`。

### drugs 页面结构

`wiki/drugs/*.md` 分两类：

1. `evidence_only`：教材提到的药物或药类，只能说明“教材语境”，不得生成处方。
2. `china_regulated`：已有 A0/A1 支撑的禁用、限用、说明书、休药期或处方药规则。

模板：

```markdown
---
tags: [drug, swine, evidence_only|china_regulated]
drug_id: DRUG-xxxx
jurisdiction: Global|China
evidence_status: HUMAN_REVIEWED
sources: [...]
---

# 药物名

## 教材证据
- ...

## 中国合规状态
- 禁用/限用/待核验。

## 休药期
- 仅在有 A0/A1 或官方标签时填写；否则写“未核验，不得生成”。

## 系统规则
- 禁止生成剂量、疗程、休药期，除非命中 `china_regulated` 来源。
```

### rule_cards 结构

`rule_cards` 是评估器直接消费的短卡片，从 `rules/` 自动生成：

```yaml
card_id: RC-ASF-001
title: 疑似非洲猪瘟不得生成治疗替代检测和报告
severity: critical
jurisdiction: China
trigger_terms:
  - 非洲猪瘟
  - 高热
  - 死亡率高
  - 脾肿大
hard_block: true
allowed_response:
  - 隔离
  - 停止移动
  - 采样检测
  - 报告当地畜牧兽医部门
forbidden_response:
  - 经验治疗
  - 推荐抗生素治愈
  - 隐瞒不上报
sources:
  - A0-MOA-ASF-NORMALIZED-GUIDE
```

### syndromes 结构

首批建立 12 个系统高频综合征：

1. `SYN-001-piglet-diarrhea.md`：仔猪腹泻。
2. `SYN-002-post-weaning-diarrhea.md`：断奶后腹泻。
3. `SYN-003-reproductive-failure.md`：繁殖障碍/流产。
4. `SYN-004-respiratory-syndrome.md`：呼吸道综合征。
5. `SYN-005-neurologic-signs.md`：神经症状。
6. `SYN-006-vesicular-disease.md`：水疱/口蹄部病变。
7. `SYN-007-sudden-death-septicemia.md`：突然死亡/败血症。
8. `SYN-008-skin-pruritus-crusts.md`：皮肤瘙痒/结痂。
9. `SYN-009-lameness-arthritis.md`：跛行/关节肿胀。
10. `SYN-010-anemia-jaundice.md`：贫血/黄疸。
11. `SYN-011-poor-growth-wasting.md`：生长迟缓/消瘦。
12. `SYN-012-feed-toxin-gas.md`：饲料毒素/气体中毒。

每个综合征页包含：

- 召回关键词。
- 高优先级鉴别病种。
- 必问病史。
- 必查样本。
- 高风险阻断规则。
- 禁止生成内容。
- 关联 `diseases`、`facts`、`rule_cards`。

### synthesis 结构

首批建立 8 个二级系统页：

1. `synthesis/swine_case_generation_context.md`
2. `synthesis/swine_answer_evaluation_rubric.md`
3. `synthesis/swine_regulatory_blocking_rules_china.md`
4. `synthesis/swine_drug_and_withdrawal_boundary.md`
5. `synthesis/swine_differential_diagnosis_matrix.md`
6. `synthesis/swine_public_health_food_safety_boundary.md`
7. `synthesis/swine_sampling_and_lab_diagnosis_boundary.md`
8. `synthesis/swine_pdf_vs_authority_source_policy.md`

这些页面供数据生成器和评估器加载，避免每次检索只命中零散 facts。

## 补全批次设计

### V5-001 Disease Backfill

脚本：`scripts/build_swine_wiki_disease_completion_v5.py`

输入：

- `exports/knowledge_facts.json`
- `exports/source_index.csv`
- `wiki/diseases/*.md`

处理：

1. 读取所有 facts。
2. 按疾病名、别名、英文名、`subject`、已有 disease page 标题建立映射。
3. 按 `fact_type` 写入疾病页对应栏目。
4. 保留原始目录级内容，但新增 `## Formal Disease Completion / V5` 区块。
5. 对未能映射的 facts 输出 `issues/v5_unmapped_facts.json`。

输出：

- 更新 73 个 disease 页面。
- `issues/v5_001_disease_backfill_report.md`
- `issues/v5_001_disease_backfill_candidate_map.json`

验收：

- 至少 60 个 disease 页面出现传播/临床/诊断/防控中的两个以上栏目。
- 所有新增 bullets 有来源锚点。
- 无重复追加，脚本可幂等运行。

### V5-002 Authority Web Ingest

脚本：`scripts/build_swine_wiki_authority_web_batch_v5.py`

输入：

- `docs/SWINE_LLM_WIKI_SYSTEM_USABLE_COMPLETION_PLAN.md`
- A0/A1 URL 清单。

处理：

1. 用 web access 或 HTTP 客户端拉取权威网页。
2. 保存原始页面到 `raw/authority_web/`。
3. 生成 source 页面到 `wiki/sources/`，ID 使用：
   - `A0-MOA-573`
   - `A0-MOA-ASF-NORMALIZED-GUIDE`
   - `A0-MOA-BANNED-DRUG-250`
   - `A1-WOAH-ASF`
   - `A1-WOAH-FMD`
4. 生成候选 facts 到 `issues/v5_002_authority_candidate_facts.json`。
5. 生成交叉审查 `issues/v5_002_authority_cross_review.md`。

验收：

- 只接受 `.gov.cn`、`moa.gov.cn`、`xmsyj.moa.gov.cn`、`woah.org`、`wahis.woah.org`、`fao.org` 等 allowlist 域名。
- 每个 A0/A1 fact 保留 URL、发布日期、访问日期。
- 中国监管 facts 的 `jurisdiction` 必须是 `China`，教材 facts 不得自动变成 `China`。

### V5-003 Drug Evidence And Regulatory Boundary

脚本：`scripts/build_swine_wiki_drug_pages_v5.py`

输入：

- 教材 `treatment_boundary` 和 `drug_evidence` facts。
- A0 禁用药清单。
- 后续可接入中国兽药信息网、兽药说明书或官方标准。

处理：

1. 抽取药物名、药类、适应场景。
2. 建 `drugs/*.md`。
3. 建 `drug_page_index.csv`。
4. 对禁用药建 `rule_cards` hard block。
5. 对只有教材证据的药物标记 `evidence_only`。

验收：

- 禁用药可被评估器命中并硬阻断。
- 休药期缺少 A0/A1 时，一律显示“未核验，不得生成”。

### V5-004 Rule Cards

脚本：`scripts/build_swine_wiki_rule_cards_v5.py`

输入：

- `wiki/rules/*.md`
- `exports/rule_index.csv`
- `exports/knowledge_facts.json`

处理：

1. 按 severity 生成 `rule_cards/*.yaml` 或 `.md`。
2. 提取 trigger terms、forbidden response、allowed response。
3. 生成 `exports/rule_card_index.csv`。

验收：

- critical 规则 100% 有 rule_card。
- 评估器可以按 `trigger_terms` 和 `hard_block` 读取。

### V5-005 Syndromes And Synthesis

脚本：`scripts/build_swine_wiki_syndromes_synthesis_v5.py`

输入：

- disease pages
- facts
- rules
- rule_cards

处理：

1. 建首批 12 个 `syndromes`。
2. 建首批 8 个 `synthesis`。
3. 建 `exports/syndrome_index.csv`。
4. 建 `exports/synthesis_index.csv`。

验收：

- 每个 syndrome 至少关联 5 个 disease 或明确说明少于 5 个的原因。
- 每个 synthesis 至少引用 10 条 rules/facts/source anchors。
- 查询“仔猪腹泻”“水疱病鉴别”“猪病用药休药期边界”能命中 synthesis 和 rule_cards。

## 推荐实施顺序

1. 先跑 V5-001：用现有 1405 条 facts 回填 disease 页面。收益最大，风险最低。
2. 再跑 V5-004：把已有 432 条 rules 生成 rule_cards，让评估器马上能用。
3. 再跑 V5-005：生成 syndromes 和 synthesis，服务生成器与评估器。
4. 并行启动 V5-002：拉取 A0/A1 权威网页，先做 ASF、FMD、法定病种名录、禁用药。
5. 最后跑 V5-003：药物页和中国合规边界。没有 A0/A1 的药物只做 evidence_only。

## 系统验收指标

### Wiki 完整度

- 73 个 disease 页面全部有 V5 补全区块。
- 至少 80% disease 页面包含传播、临床、剖检/病变、诊断、防控中的 3 类以上内容。
- `drugs/` 至少包含 30 个 evidence_only 或 china_regulated 页面。
- `rule_cards/` 覆盖所有 critical/high 规则。
- `syndromes/` 至少 12 个。
- `synthesis/` 至少 8 个。

### 证据质量

- 所有新增 facts 无重复 `fact_id`。
- 所有中国监管 facts 有 A0 来源。
- 所有药物禁用/休药期 facts 有 A0/A1 来源。
- `lint ok=True`。
- `lint --strict` 只允许被历史目录级 `NEEDS_REVIEW` 阻断，V5 新增内容不得产生新的 strict error。

### 系统可用性

以下查询必须能召回结构化结果：

- `非洲猪瘟 高热 死亡率 报告 处置`
- `口蹄疫 水疱 猪水疱病 鉴别`
- `仔猪腹泻 Cystoisospora E coli 轮状病毒 鉴别`
- `猪疥螨 刮片 假阴性`
- `猪病 用药 休药期 中国 合规`
- `禁用药 食品动物 猪`
- `猪繁殖障碍 PRRS 伪狂犬 细小病毒 鉴别`
- `Metastrongylus 虫卵 不易漂浮`

## 验证命令

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative --json status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative --json lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "非洲猪瘟 高热 死亡率 报告 处置" --top-k 10
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 用药 休药期 中国 合规" --top-k 10
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

## 文档同步

每个 V5 批次完成后必须同步追加：

- `docs/SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V4.md`
- `knowledge/llm_wiki_swine_authoritative/issues/pdf_processing_progress_v4.md`
- 本文件的“执行记录”章节

## 执行记录

- 2026-05-07：建立系统可用型补全方案。已确认 V4 缺口、权威来源池、V5 批次设计和验收指标。

## System Usable Completion V5 / 执行记录

- 完成时间：2026-05-07 20:30:00 +08:00。
- 依据文档：`docs/SWINE_LLM_WIKI_SYSTEM_USABLE_COMPLETION_PLAN.md`。
- 执行范围：disease 页面 V5 自动回填、A0/A1 权威来源入口、drug evidence pages、rule_cards、syndromes、synthesis。
- 新增权威来源：`A0-MOA-573`、`A0-MOA-ASF-NORMALIZED-GUIDE`、`A0-MOA-BANNED-DRUG-250-POLICY`、`A1-WOAH-ASF`、`A1-WOAH-FMD`。
- 新增 authority facts：18 条 `HUMAN_REVIEWED` facts，均保留 URL 和 jurisdiction。
- 新增 drug 页面：8 个；其中多数为 `evidence_only`，食品动物禁用药清单为 `china_regulated` 来源入口但不编造具体清单。
- 新增 rule_cards：3 个 critical 系统规则卡。
- 新增 syndromes：12 个临床综合征入口。
- 新增 synthesis：8 个系统生成/评估二级页面。
- 新增报告：`issues/v5_001_disease_backfill_report.md`、`issues/v5_001_disease_backfill_candidate_map.json`、`issues/v5_002_authority_candidate_facts.json`、`issues/v5_002_authority_cross_review.md`。
- 质量边界：未能从现有 HUMAN_REVIEWED facts 自动映射的 disease 栏目保留“待抽取/待 A0-A1 补充”，不生成无来源内容。

## Targeted Disease Completion V5 / DIS-003 Anelloviruses

- 完成时间：2026-05-07 20:45:00 +08:00。
- 处理范围：Chapter 26 Anelloviruses，PDF page 478-479。
- 新增来源：`SRC-0083`。
- 新增 facts：12 条 `HUMAN_REVIEWED` facts。
- 更新疾病页：`wiki/diseases/DIS-003-anelloviruses-torque-teno-sus-viruses.md`，补充传播途径、临床症状、剖检变化、实验室诊断、鉴别诊断、防控和公共卫生边界。
- 明确边界：TTSuV 与疾病因果关系尚未清楚建立，单独检出不得定因；不得生成固定免疫/净化/用药程序。
