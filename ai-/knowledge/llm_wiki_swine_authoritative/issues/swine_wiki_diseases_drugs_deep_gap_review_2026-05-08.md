# Swine LLM Wiki diseases/drugs deep gap review & Entity Reinforcement Protocol

## 0.1 V16 balanced source-use override / 2026-05-08

This section supersedes earlier wording that treats A0/A1 as a universal hard gate for all generation and evaluation. The new rule is: **source level determines allowed task use, not absolute usability**.

Qualified source levels are `A0`, `A1`, `A2`, `SRC`, and `RC/RULE`. A fact or page may support dataset generation if it is anchored to one of these qualified levels and the answer preserves the source boundary. A0/A1 remain preferred for official and executable claims, but they are no longer required for ordinary clinical generation.

`HUMAN_REVIEWED`, `NEEDS_REVIEW`, and `partial` are audit states, not dataset-use statuses. Use these task-use statuses instead:

- `train_ready`: may enter filtered SFT/evaluation data when clinical claims are source-grounded and answer JSON includes standard source IDs.
- `eval_ready`: may be used for evaluation, contrastive cases, and reviewer training even if it is not strong enough for final SFT.
- `generation_ready_limited`: may be used to generate candidate answers, but answers must keep explicit boundaries and avoid unsupported executable conclusions.
- `retrieval_only`: may be used for recall, alias matching, routing, and context, but not for final answer claims.
- `blocked`: insufficient source signal or unsafe conflict.

The following may use `A0/A1/A2/SRC/RC/RULE` when the source is clear and the answer cites it: pathogen or disease positioning, host and production stage, transmission, clinical signs, necropsy findings, laboratory diagnosis methods, sample selection, differential diagnosis, causality limitations, general prevention and management direction, and "do not conclude from a single test" boundaries.

The following remain high-risk executable claims and must cite A0/A1 or a label-level equivalent source: China legal disease class, statutory reporting, quarantine, culling, movement restriction, official testing workflow, mandatory vaccination program, specific dose, course, route, withdrawal period, MRL, residue compliance, slaughter/sale/food-safety decisions, prescription/prohibited/eliminated drug status, and any local regulatory commitment.

Generation and evaluation should prefer broader coverage with standard citations over blocking pages solely because they are not A0/A1 anchored. If an answer contains a high-risk executable claim without authority or label-level support, it must be downgraded to boundary language, `generation_ready_limited`, or rejected by the exporter.

- **Date**: 2026-05-08
- **Scope**: `wiki/diseases`, `wiki/drugs`, and dataset-generation boundary pages
- **Goal**: V11 起改为网页信息源优先：每次执行任务必须先从权威网页检索并获取对应信息源，再从新获取的信息中补充和补足本地知识库；本地既有 facts/source/rule/comparison 只用于写入后的去重、冲突检查、链接和一致性校验，不再作为新内容的优先依据。

---

## 0. V11 web-first source acquisition override / 2026-05-08

**本节覆盖下方旧的 V8/V10 entity-first 和 SRC-first 工作流。** 下方历史规则保留用于审计和追溯，但后续新任务默认不再执行“先查本地、缺口再联网”的流程。

### 核心原则

- 每次 disease/drug/rule/comparison/syndrome/source 补强任务，必须先执行网页检索并获取权威信息源。
- 不再先读取或挖掘本地 `exports/knowledge_facts.json`、`wiki/sources/*`、`wiki/rule_cards/*`、`wiki/rules/*`、`wiki/syndromes/*`、`wiki/comparisons/*` 或旧 execution log 来生成新内容。
- 本地知识库只作为写入目标、ID 注册表、格式参照、去重和冲突校验对象。
- 如果网页检索无法获得可接受来源，任务必须标记为 `blocked_web_source_missing`、`source_enrichment_pending` 或 `partial`；不得用本地旧事实或模型记忆补齐。
- 所有新增事实必须来自本轮新检索并打开核验过的网页、PDF、标准、公告或官方附件。

### 新的固定执行顺序

1. **任务定界**
   - 先列出目标实体和需要补齐的字段。
   - disease 页至少覆盖：病原/病型定位、流行病学或传播边界、临床症状或剖检变化、实验室诊断、鉴别诊断、防控/用药/处置边界。
   - drug 页至少覆盖：批准标签或监管状态、靶动物、剂型/给药途径边界、适应证边界、处方/禁停用状态、休药期/MRL 或明确 Evidence gap。

2. **网页检索优先**
   - 在读取本地 facts 前，先检索权威网页来源。
   - 检索词必须包含目标中文名、英文名、病原名或活性成分名，并结合监管/诊断/防控/标签关键词。
   - 涉及中国监管、兽药、残留、饲料/食品安全、检疫、调运、上报、扑杀、官方处置时，优先检索 A0 域名：
     - `moa.gov.cn`
     - `xmsyj.moa.gov.cn`
     - `samr.gov.cn`
     - `nhc.gov.cn`
     - `sac.gov.cn`
     - `openstd.samr.gov.cn`
   - 涉及国际疫病状态、公共卫生、诊断手册、官方动物卫生资料时，检索 A1 域名：
     - `woah.org`
     - `fao.org`
     - `aphis.usda.gov`
     - `cdc.gov`
     - `ema.europa.eu`
     - `efsa.europa.eu`
     - `fda.gov/animal-veterinary`
   - A2 仅用于非监管临床背景补充，例如 `merckvetmanual.com`、有署名兽医作者的大学 extension 页面、可核验的同行评议开放论文。

3. **来源打开和信息捕获**
   - 必须打开候选网页/PDF/标准正文，不能只用搜索结果摘要。
   - 记录标题、URL、发布机构、发布日期或修订日期、访问日期、适用辖区、可用段落/表格/PDF 页码，以及不得外推的边界。
   - 拒绝营销页、经销商页、论坛、问答、短视频、无作者/无出处转载、无法确认发布日期/机构/辖区的页面。

4. **权威等级判定**
   - 先判定来源等级，再抽取事实：
     - `A0`: 中国官方法规、公告、标准、标签、目录、残留限量、动物疫病名录、技术规范。
     - `A1`: 国际官方或准官方动物/公共卫生权威。
     - `A2`: 高质量二级临床或学术支持资料。
   - A1/A2 不能替代 A0 来支持中国监管、药物合法性、休药期、MRL、扑杀、调运、检疫、上报或食品安全结论。

5. **创建/更新 source 页**
   - 任何被采用的网页信息源，必须先创建或更新 `wiki/sources/<SOURCE_ID>.md`。
   - source 页必须包含：`source_id`、`authority_level`、URL、发布机构、发布日期/修订日期、访问日期、辖区、可支持结论、不得外推边界、页码/段落/表格锚点。
   - 新 source 必须同步更新 `exports/source_index.csv`。

6. **从新来源抽取 facts**
   - 从本轮新检索来源中创建或更新 `exports/knowledge_facts.json`。
   - 每条 fact 必须包含稳定 `fact_id`、`evidence_source_id`、`evidence_url`、网页段落/PDF 页码/表格锚点、`evidence_status`、适用物种/阶段/辖区。
   - 只有已经打开正文并核验的事实才能标记 `HUMAN_REVIEWED`。
   - 新检索来源无法支持的字段必须写 `Evidence gap`，不得从本地旧 facts 或模型记忆补齐。

7. **回填本地实体页**
   - source 页和 facts 完成后，再更新 `wiki/diseases`、`wiki/drugs`、`wiki/rule_cards`、`wiki/rules`、`wiki/syndromes`、`wiki/comparisons` 以及相关索引。
   - 每个实体页 bullet 必须带新 `fact_id` 或新 source/rule anchor。
   - disease 页应至少链接 1 个 syndrome 或 comparison 页面。

8. **高风险硬门禁**
   - 剂量、疗程、给药途径、休药期、MRL、残留合格、肉品可食、饲料放行、中国法定状态、上报、扑杀、调运、检疫、固定疫苗程序、处方药/禁停用结论，必须有精确 A0 来源。
   - 无精确 A0 时，只能写边界、拒答或后续检索任务。
   - A2 临床资料不得用于中国监管或食品安全执行结论。

9. **验证**
   - 新实体补强块应使用 `## Web Source Reinforcement / V11`，或包含 `V11` 与 `Web Source Reinforcement` 的任务特定标题。
   - 验证每个 `fact_id` 都存在于 `exports/knowledge_facts.json`，每个 `evidence_source_id` 都能解析到 source 页或已接受 rule card。
   - 验证新增 source 已进入 `exports/source_index.csv`。
   - 验证高风险词只出现在 A0 支持的结论或明确禁止/边界语句中。

10. **执行日志**
   - 每次任务必须新建或更新 execution log，记录：
     - 目标实体
     - 使用的检索式
     - 采用来源和拒绝来源
     - 抽取 facts
     - 创建/更新 source 页
     - 修改实体页
     - 高风险门禁结果
     - 剩余 Evidence gaps
     - 验证统计
   - 如果外部检索失败或来源无法访问，记录失败原因并停止为 `blocked_web_source_missing`；不得改用本地材料宣称完成。

### 新 lookup order

旧顺序 `Existing SRC first -> A0/A1 -> A2` 废止。新顺序为：

1. **A0 web sources first**：中国监管、兽药、残留、饲料/食品安全、疫病名录、检疫、调运、上报、扑杀、标准和官方处置边界。
2. **A1 web sources second**：国际疫病状态、官方诊断手册、公共卫生和跨境参考。
3. **A2 web sources third**：仅补充非监管临床事实。
4. **Local wiki last**：只用于去重、链接、格式一致性和冲突校验。

## 1. Entity-first reinforcement protocol (实体页优先补强规程)

> **Superseded by V11 web-first source acquisition override.** This historical section is retained for audit context only and must not be used as the default workflow for new tasks.

核心原则：**先让现有 disease/drug/syndrome/comparison/rule 实体页可用，再考虑搜索新数据。** 搜索不是任务本身，搜索只服务于实体页缺口、监管/药物硬边界和黄金数据集验收。

### Authority source taxonomy (A0/A1/A2/SRC)

所有事实进入实体页前，必须先判断来源等级。来源等级决定它能支持什么结论，也决定模型应该去哪些网址检索。

| Level | 定义 | 首选网址/入口 | 可支持内容 | 不可支持内容 |
|---|---|---|---|---|
| A0 | 中国官方、现行或可追溯的法规/公告/标准/技术规范 | `https://www.moa.gov.cn/`, `https://xmsyj.moa.gov.cn/`, `https://www.samr.gov.cn/`, `https://www.nhc.gov.cn/`, `https://www.sac.gov.cn/`, `https://openstd.samr.gov.cn/`, `https://www.pkulaw.com/` only if official text is cross-checkable | 中国动物疫病分类、报告义务、官方处置边界、兽药标签/注册公告、处方药目录、禁停用/淘汰、MRL/休药期、国家标准 | 不得从标题或入口页外推具体剂量、疗程、扑杀、调运、食品处理；必须核验正文或附件 |
| A1 | 国际官方或准官方动物卫生/公共卫生权威 | `https://www.woah.org/`, `https://www.fao.org/`, `https://www.aphis.usda.gov/`, `https://www.cdc.gov/`, `https://www.ema.europa.eu/`, `https://www.efsa.europa.eu/`, `https://www.fda.gov/animal-veterinary` | 国际疾病状态、WOAH listed disease、Terrestrial Code/Manual、公共卫生边界、国际药物重要性、非中国参考边界 | 不得替代中国法规、不得把境外标签外推为中国猪用 |
| A2 | 高质量二级权威或专业参考 | `https://www.merckvetmanual.com/`, university extension pages with named veterinary authors, peer-reviewed review pages when source is clear | 辅助临床背景、鉴别诊断、采样建议、疾病解释 | 不得支持中国监管、具体处方、休药期、MRL、食品安全执行 |
| SRC | 本地项目内已登记来源，通常为教材 PDF、已审 facts、内部 source/rule/synthesis | `wiki/sources/`, `exports/knowledge_facts.json`, `wiki/rule_cards/`, `wiki/syndromes/`, `wiki/comparisons/`, `wiki/synthesis/` | 教材临床事实、病理、诊断、鉴别、生成/评估约束 | 不得直接外推中国法定处置、剂量、休药期、MRL 或当地监管执行 |

#### Fixed source lookup order

执行任何补强任务时，按以下顺序查找来源：

1. **Existing SRC first**: `exports/knowledge_facts.json`、`exports/source_index.csv`、现有 `wiki/sources/*`、`rule_cards`、`syndromes`、`comparisons`、`synthesis`。
2. **A0 when China/regulatory/drug/food-safety is involved**: 优先 `moa.gov.cn` 和 `xmsyj.moa.gov.cn`；涉及国家标准、MRL 或食品安全时再查 `samr.gov.cn`、`nhc.gov.cn`、`sac.gov.cn`、`openstd.samr.gov.cn`。
3. **A1 when disease status/manual/public health is involved**: 优先 WOAH disease pages、WOAH Terrestrial Code/Manual；再查 FAO、USDA APHIS、CDC、EMA/EFSA/FDA 动物药资料。
4. **A2 only for support**: Merck Veterinary Manual 或大学 extension 仅作临床辅助，不作为高风险执行依据。

#### Which source level to use

| Task question | Required level | Notes |
|---|---|---|
| 中国是否法定报告、几类动物疫病、是否限制移动/扑杀/检疫 | A0 | 优先 MOA/畜牧兽医局；A1/SRC 不能替代 |
| 猪病临床表现、病理、发病机制、鉴别诊断 | SRC first, then A1/A2 | 优先本地 `HUMAN_REVIEWED` textbook facts；不足时用 WOAH/Merck 等补充 |
| 诊断方法、采样、检测结果解释 | SRC/A1/A2; A0 if China official standard exists | 单次 PCR/培养/抗体阳性不得直接定因 |
| 药物能否中国猪用、标签、靶动物、剂型、适应证 | A0 only for positive-use | 处方药目录只能证明管理属性，不能证明适应证 |
| 剂量、疗程、给药途径、休药期、MRL、残留合格 | A0 exact label/standard only | 无精确来源必须拒绝或边界化 |
| 禁用、停用、淘汰、人药兽用、非法添加 | A0 | 不得用延长休药期规避 |
| 人兽共患、职业暴露、公共卫生 | A0 for China execution; A1/A2 for general risk | CDC/WOAH/FAO 可做国际边界，不能替代中国处置 |
| 黄金数据集生成/评估硬门禁 | RC/SYN/CMP + A0/A1/SRC | 必须引用 rule_card/synthesis/comparison 和实体页事实 |

#### Disallowed sources

以下来源不得作为实体页事实依据：

- 兽药营销页、经销商网页、厂家宣传页，除非引用的是可核验官方批准标签附件；
- 论坛、问答、公众号二次转载、短视频、无作者无出处博客；
- 仅有摘要没有正文或附件的搜索结果；
- 无法确认发布日期、发布机构或适用辖区的网页；
- 与猪、目标药物、目标病种或中国辖区不匹配的页面。

#### Source ID naming

新增 source 页必须使用稳定 ID：

- 中国官方：`A0-MOA-...`, `A0-SAMR-...`, `A0-NHC-...`, `A0-GB-...`
- 国际官方：`A1-WOAH-...`, `A1-FAO-...`, `A1-USDA-APHIS-...`, `A1-CDC-...`, `A1-EMA-...`
- 二级权威：`A2-MERCK-...`, `A2-UNIV-...`
- 本地教材/内部：`SRC-....`, `RC-....`, `SYN-....`, `CMP-....`

每个 source 页必须写明：`source_id`、`authority_level`、URL、本地路径或附件、发布机构、发布日期/访问日期、可用边界、不得外推边界。

### Mandatory entity-first workflow / V10

任何 disease/drug/entity 补强任务都必须以现有实体页为中心执行。优先使用项目内已经存在的 `HUMAN_REVIEWED` facts、SRC/source 页、rule cards、syndrome 页、comparison 页和 synthesis 门禁，把实体页补到可检索、可约束、可评估的状态。只有当关键字段没有可用来源，或涉及中国监管、禁用药、休药期、MRL、食品安全、公共卫生、法定报告等高风险结论时，才触发外部检索。

每个实体必须按以下顺序执行：

1. **Local baseline scan**
   - 读取现有实体页、`exports/knowledge_facts.json`、`exports/source_index.csv`、相关 `syndromes`、`rule_cards`、`synthesis` 和 `issues`。
   - 输出当前缺口：缺 A0/A1、缺诊断、缺鉴别、缺用药边界、缺休药/MRL、缺公共卫生、缺监管状态。
2. **Existing evidence consolidation**
   - 优先从 `HUMAN_REVIEWED` facts、已有 source 页、syndrome/comparison/rule/synthesis 页抽取可落地内容。
   - 先补实体页的核心栏目：病原/分类、宿主阶段、传播/流行病学、临床症状、剖检变化、实验室诊断、鉴别诊断、防控和用药/处置边界。
   - 每条事实必须带 `fact_id`、`source_id`、PDF page/URL/rule anchor。
3. **Gap-triggered external search**
   - 仅当现有来源不足以支撑关键缺口时，才使用 web-access/联网检索。
   - 必须检索的触发条件：A0/A1 中国监管状态未知却要生成监管边界；drug 需要正向用药、标签、靶动物、处方药、禁停用、休药期或 MRL；公共卫生/食品安全/重大疫病/水疱病/高死亡率问题缺权威来源；现有事实少于最低实体页可用阈值。
   - 外部检索必须是“缺什么查什么”，不得为了凑数量进行泛搜。
4. **Source triage**
   - 候选来源按 A0/A1/A2/SRC 分级。
   - A0/A1 优先，A2 只能辅助，商业网页、论坛、营销材料、无出处转载不得作为事实来源。
   - 每个采用来源必须记录 URL、标题、发布机构、发布日期/访问日期、适用辖区、可用边界和不得外推边界。
5. **Source page creation**
   - 对所有被采用的新来源创建 `wiki/sources/<SOURCE_ID>.md`。
   - 同步更新 `exports/source_index.csv`。
   - 未创建 source 页的网页不得直接写入 disease/drug 页事实。
6. **Entity-page reinforcement**
   - 只把已经落到 source 页或 `HUMAN_REVIEWED` fact 的内容写入实体页。
   - 每条事实必须带 source/fact anchor。
   - 对仍未找到来源的维度，写成 `Evidence gap`，不得补推测。
7. **Comparison/rule update**
   - 如果新增来源影响鉴别、监管、用药、休药期、公共卫生或食品安全，必须同步更新相应 comparison/rule_card/synthesis 页。
8. **Execution log**
   - 每次任务必须新增或更新 execution log，列出：实体页基线、已使用本地 facts/source、是否触发外部检索、采用来源、拒绝来源、修改页面、未解决缺口、下一步。
   - 未满足停止条件时，不能写“完成”，只能写“partial / blocked / needs source follow-up”。

### Minimum entity usability thresholds / V10

#### Disease entity threshold

每个 disease 页在宣布“实体页补强完成”前，至少满足：

- 至少 5 条疾病特异 `HUMAN_REVIEWED` facts，或明确写出该实体目前 facts 不足；
- 至少覆盖病原/病型定位、临床或病变、诊断、鉴别/因果限制、防控或用药边界中的 4 类；
- 至少 1 个 diagnosis/sampling/test interpretation 来源；
- 至少 1 个 differential/comparison anchor；
- 对 treatment/control/vaccine/public-health 至少有明确 source-backed boundary；
- 中国监管状态若无疾病特异 A0/A1，可先使用通用 A0/rule 门禁，但必须写明“疾病特异 A0 未确认”；
- 对仍缺的栏目写入 `Evidence gap` 或 `黄金集生成边界`，不能留给模型自由补全。

只有在以下情况下，disease 才必须执行外部检索：

- 现有 `HUMAN_REVIEWED` facts 少于 5 条；
- 需要生成中国监管、法定报告、扑杀、调运、检疫、公共卫生或食品安全结论；
- 疾病为 ASF/FMD/CSF/PRRS/PED/zoonosis/vesicular/sudden death/high mortality/public health 相关，且现有 A0/A1 不足；
- comparison/rule/synthesis 页需要新增权威边界。

#### Drug entity threshold

每个 drug 页在宣布“实体页补强完成”前，至少满足：

- 明确 `gold_dataset_use`：`boundary_only`、`negative_trap`、`exclude_from_positive_generation` 或 `positive_label_candidate`；
- 明确药物类别、候选用途边界、不可生成内容；
- 明确是否已有中国标签/靶动物/剂型/适应证/处方药/禁停用/休药期/MRL 来源；
- 若没有精确猪用证据，必须写入 `boundary_only` 或 `negative_trap`，并说明需要哪些来源才能升级；
- 对 dose/course/route/withdrawal/MRL/residue/food-safety 必须有 rule-card 门禁。

只有在以下情况下，drug 才必须执行外部检索：

- 准备将页面提升为 `positive_label_candidate`；
- 用户任务要求具体药物中国猪用标签、适应证、剂量、疗程、休药期、MRL、残留或处方药状态；
- 页面缺少禁用/停用/淘汰或处方药边界，且该药可能进入生成答案；
- 药物属于高风险类别：抗菌药、人医关键药、禁停用历史药、促生长剂、有机磷/杀虫剂、激素、生殖调控药、食品安全高风险药。

没有精确中国猪用标签、靶动物、剂型、适应证、休药期/MRL 支持时，不得将任何 drug 页提升为 `positive_label_candidate`。

### Stop conditions / V10

实体补强任务只有在满足以下全部条件后才可停止：

- 目标实体页已写入来源锚定事实、生成边界或明确 Evidence gaps；
- 优先使用的本地 facts/source 已在 execution log 中列明；
- 若触发外部检索，新来源已创建 source 页并进入 `exports/source_index.csv`；
- 若未触发外部检索，execution log 必须写明原因，例如“现有 HUMAN_REVIEWED facts 已满足本轮实体页可用阈值，剩余为 A0 source enrichment 后续任务”；
- comparison/rule_card/synthesis 受影响页面已同步更新；
- execution log 已记录实体页改动、使用来源、是否检索、采用/拒绝来源和剩余缺口；
- 至少有一个验证统计证明页面中 source/fact anchors、comparison links 或 `gold_dataset_use` 等门禁字段存在；
- 若检索不足、网页受阻、官方来源无法访问或没有疾病/药物特异来源，必须在 execution log 写明阻塞原因和下一步查询策略。

禁止用以下情况作为停止理由：

- 只完成本地 facts 重排但没有写入实体页可检索栏目、生成边界或 comparison links；
- 只新增 rule_card 但未补 source；
- 只找到入口页但未确认可用边界；
- 只做了网页搜索但未创建 source 页；
- 只补了中文或英文一个名称，未补实体页核心字段。

允许作为本轮停止理由：

- 已经把现有 `HUMAN_REVIEWED` facts 和已有 source/rule/comparison 充分落地到实体页；
- 高风险缺口已被 rule cards 明确阻断；
- 外部检索被记录为后续 source-enrichment 任务，且不会影响当前实体页对生成/评估的约束能力。

### 药品类精准查询 (Drug Precision Query)
针对药品实体，通过限定政务关键词，确立官方核准的使用边界：
* **查询公式**：`site:<A0/A1 domain> [中文通用名/英文通用名/活性成分] + [监管关键词]`
* **A0 首选入口**：`moa.gov.cn`、`xmsyj.moa.gov.cn`、`samr.gov.cn`、`nhc.gov.cn`、`openstd.samr.gov.cn`
* **推荐关键词**：`质量标准`、`说明书`、`标签`、`注册公告`、`处方药目录`、`禁用`、`停用`、`淘汰`、`残留限量`、`休药期`、`停药期`、`GB 31650`
* **指令示例**：
    > "调用 `eze-is/web-access` 模块，检索并同步 **[阿莫西林]** 的官方政务信息。重点提取：质量标准、说明书全文、处方药分类以及最新的休药期规定。确保数据来源于 moa.gov.cn 或其下属政务门户。"

#### Drug gap-triggered query checklist / V10

当 drug 页触发外部检索条件时，按以下查询组合执行，并保留命中或未命中记录。若本轮仅做 `boundary_only`、`negative_trap` 或本地实体页补强，可不执行全部查询，但必须在 execution log 中说明未检索原因。

- `site:moa.gov.cn [中文通用名] 兽药 说明书`
- `site:xmsyj.moa.gov.cn [中文通用名] 兽药 说明书`
- `site:moa.gov.cn [中文通用名] 质量标准`
- `site:moa.gov.cn [中文通用名] 注册公告`
- `site:moa.gov.cn [中文通用名] 处方药目录`
- `site:moa.gov.cn [中文通用名] 休药期 OR 停药期`
- `site:moa.gov.cn [中文通用名] 最大残留限量 OR GB 31650`
- `site:openstd.samr.gov.cn [中文通用名] GB 31650`
- `site:samr.gov.cn [中文通用名] 食品安全国家标准`
- `[English active ingredient] swine label withdrawal MRL official`
- `[中文通用名] 禁用 OR 停用 OR 淘汰 兽药`

采用来源时必须区分：

- active ingredient vs formulation；
- single ingredient vs compound product；
- pig vs poultry/cattle/aquaculture/pet/human；
- China label vs foreign label；
- prescription status vs approved indication；
- MRL vs withdrawal period。

### 疾病类精准查询 (Disease Precision Query)
针对疾病实体，侧重于同步现行监管要求与处置规范：
* **查询公式**：`site:<A0/A1 domain> [中文病名/英文病名/病原名] + [疾病关键词]`
* **A0 首选入口**：`moa.gov.cn`、`xmsyj.moa.gov.cn`
* **A1 首选入口**：`woah.org`、`fao.org`、`aphis.usda.gov`、`cdc.gov`
* **推荐关键词**：`防控方案`、`监测计划`、`应急处置指南`、`法定报告义务`、`诊断规范`、`技术指南`、`动物疫病名录`、`Terrestrial Manual`、`Terrestrial Code`
* **指令示例**：
    > "调用 `eze-is/web-access` 模块，同步官方关于 **[猪瘟]** 的防控与监管要求。重点检索：现行防控方案、法定报告义务等级、以及最新的监测与应急处置指南。优先采集 A0 级政务公告。"

#### Disease gap-triggered query checklist / V10

当 disease 页触发外部检索条件时，按以下查询组合执行，并保留命中或未命中记录。若本轮现有 `HUMAN_REVIEWED` facts 已足够补齐临床、诊断、鉴别和生成边界，可先完成实体页补强，把疾病特异 A0/A1 扩源列为后续任务。

- `site:moa.gov.cn [中文病名] 防控 技术指南`
- `site:xmsyj.moa.gov.cn [中文病名] 防控 技术指南`
- `site:moa.gov.cn [中文病名] 监测 计划`
- `site:moa.gov.cn [中文病名] 应急 实施方案`
- `site:moa.gov.cn [中文病名] 诊断 规范`
- `site:moa.gov.cn [中文病名] 动物疫病 名录`
- `site:woah.org [English disease name] swine disease`
- `site:woah.org [pathogen name] Terrestrial Manual`
- `site:woah.org [English disease name] Terrestrial Code`
- `site:fao.org [English disease name] swine`
- `site:aphis.usda.gov [English disease name] swine`
- `site:cdc.gov [English disease name] swine zoonosis`
- `[English disease name] swine diagnosis control official`
- `[病原名中文] 猪 诊断 防控 官方`

采用来源时必须区分：

- disease page vs source entry page；
- diagnosis method vs disease causality；
- global textbook fact vs China regulatory action；
- prevention/control guidance vs execution-level legal instruction；
- current version vs obsolete/archived version。

---

## 2. Disease Task Selection Framework

This document does not define a fixed disease priority list. Target diseases, page IDs, expected output scope, and minimum count are supplied by the current user task or execution ticket.

When a task includes disease entities, use the **Disease Precision Query** protocol and V11 web-first workflow to decide what must be searched, extracted, and written. Prioritize within the provided target set using the following general risk order:

1. diseases or syndromes that affect dataset safety, public-health boundaries, China regulatory interpretation, movement/quarantine/reporting/culling, or food-chain decisions;
2. diseases that commonly appear in generated cases and need stable diagnosis, differential diagnosis, or causality boundaries;
3. diseases with incomplete A0/A1/A2 source coverage for current task fields;
4. diseases whose pages have too few reviewed, newly sourced facts to support generation and evaluation;
5. diseases linked to comparison matrices or syndrome pages that are likely to become evaluation traps.

For each target disease, the executor must determine the information gaps from the task requirements, not from a hard-coded disease list in this document.

---

## 3. Drug Task Selection Framework

This document does not define a fixed drug priority list. Target drugs, ingredients, formulations, jurisdictions, and output fields are supplied by the current user task or execution ticket.

When a task includes drug entities, use the **Drug Precision Query** protocol and V11 web-first workflow to verify only the fields required by the task. Drug work must prioritize safety and legality over page completeness.

Required evidence depends on the requested claim:

- positive pig-use claim: exact approved label or official registration source for pigs;
- target species claim: source must explicitly include pigs/swine and must not be inferred from another species;
- formulation or route claim: source must match the active ingredient, formulation, and route;
- withdrawal period or MRL claim: exact A0 label/standard/table required;
- prescription, prohibited, stopped, eliminated, or restricted-use claim: exact A0 source required;
- food-safety or residue compliance claim: exact A0 source required.

If exact evidence is missing, mark the page or claim as `boundary_only`, `negative_trap`, `source_enrichment_pending`, or `blocked_web_source_missing`; do not promote it into positive generation.

---

## 4. Generic Reinforcement Sequence

Use this sequence for any task, regardless of entity type. The specific pages, source targets, and required fields must come from the current conversation or task ticket.

### Step 1: Scope and risk classification

- Identify target entity type: disease, drug, rule, syndrome, comparison, source, or mixed.
- Identify required output: page reinforcement, source enrichment, fact extraction, rule update, comparison matrix, index update, or execution-log-only audit.
- Identify high-risk dimensions: China regulatory status, legal handling, public health, drug use, withdrawal/MRL, residue, feed/food safety, quarantine, movement, culling, reporting, or fixed vaccine program.
- Decide required authority level for each claim before searching.

### Step 2: Web source acquisition

- Execute V11 web-first search before using local facts as content.
- Search A0/A1/A2 sources according to the claim type.
- Open and inspect sources, including PDF pages or official attachments when applicable.
- Reject unsupported, commercial, outdated, inaccessible, or jurisdiction-mismatched sources.

### Step 3: Source-page creation and indexing

- Create or update `wiki/sources/<SOURCE_ID>.md` for every adopted web source.
- Record authority level, URL, publisher, date, access date, usable claims, non-extrapolation boundaries, and page/span/table anchors.
- Update `exports/source_index.csv` for new source pages.

### Step 4: Fact extraction

- Extract facts only from adopted sources.
- Add or update `exports/knowledge_facts.json` with stable `fact_id`, `evidence_source_id`, `evidence_url`, source span, evidence status, species, stage, and jurisdiction.
- Mark `HUMAN_REVIEWED` only after checking the opened source text or PDF page.
- If the source does not support a required field, write `Evidence gap`.

### Step 5: Entity-page reinforcement

New entity-page reinforcement should use:

```md
## Web Source Reinforcement / V11
```

Use subsections relevant to the entity type and task. For disease pages, common subsections are:

- `### 病原/病型定位`
- `### 流行病学或传播边界`
- `### 临床症状或剖检变化`
- `### 实验室诊断`
- `### 鉴别诊断`
- `### 防控/用药/处置边界`
- `### 生成与评估边界`
- `### Evidence gap`

For drug pages, common subsections are:

- `### 药物/成分定位`
- `### 批准标签和靶动物`
- `### 剂型/途径/适应证边界`
- `### 处方药/禁停用/限制状态`
- `### 休药期/MRL/残留边界`
- `### 生成与评估边界`
- `### Evidence gap`

Rules:

- Every factual bullet must cite `fact_id`, `source_id`, and page/span/table/URL anchor.
- Every rule or boundary bullet must cite rule/source IDs.
- Do not replace older V5/V6/V8 blocks unless the task explicitly asks for cleanup; append or add V11 so retrieval can prefer newer anchors.
- Do not promote `evidence_status` to `HUMAN_REVIEWED` while the source text has not been opened and checked.
- Do not generate dose, course, withdrawal period, vaccine schedule, culling, movement, quarantine, reporting, edible-meat, feed-release, or food-safety claims without exact source support.

### Step 6: Comparison, syndrome, and rule updates

Create or update comparison/syndrome/rule pages only when the current task requires them or when new sources change generation/evaluation boundaries.

Comparison pages should generally include:

- syndrome or trigger pattern;
- candidate entities;
- support clues;
- against/limitation clues;
- minimum diagnostic or verification package;
- regulatory/drug/food-safety boundary;
- evaluation traps that should fail.

Comparison and syndrome pages may synthesize across cited facts and sources, but must not introduce uncited clinical or regulatory claims.

### Step 7: Status assignment

Use these statuses consistently:

- `entity_reinforced`: required fields for the current task are supported by accepted sources and written to the entity page.
- `source_enriched`: new A0/A1/A2 source pages were created or attached, indexes updated, and the entity distinguishes source-backed clinical facts from regulatory boundaries.
- `source_enrichment_pending`: entity page is usable for the current task, but additional A0/A1/A2 detail remains unresolved.
- `partial`: some required fields are missing, facts are fewer than the task threshold, or links/indexes are incomplete.
- `blocked_web_source_missing`: web search did not find acceptable sources or sources were inaccessible.
- `blocked_high_risk_evidence_missing`: the task requires a high-risk conclusion but exact A0/A1 evidence is unavailable.

### Step 8: Acceptance criteria

A disease entity update is acceptable when:

- it covers the task-required disease fields, or explicitly records Evidence gaps;
- it includes diagnosis/sampling/test-interpretation support when diagnosis is in scope;
- it includes differential diagnosis or causality limitation when generation/evaluation is in scope;
- it includes drug/regulatory/public-health/food-safety non-inference boundaries when relevant;
- it links to at least one syndrome or comparison page when cases or evaluation traps are in scope;
- it records web searches, adopted sources, rejected sources, and remaining gaps.

A drug entity update is acceptable when:

- target species, formulation, route, and indication claims are matched to exact source scope;
- positive pig-use claims have exact A0 label/registration support;
- prescription, prohibited, stopped, eliminated, withdrawal, MRL, residue, and food-safety claims have exact A0 support;
- unsupported drug claims are marked `boundary_only`, `negative_trap`, `source_enrichment_pending`, or blocked;
- no dose/course/withdrawal/MRL is inferred from non-A0 or non-matching sources.

A comparison or syndrome update is acceptable when:

- it covers the candidate set requested by the task;
- it cites entity pages, source pages, fact IDs, or rule cards for every substantive claim;
- it has explicit "do not conclude from" traps;
- it avoids dose, withdrawal, food-safety, culling, movement, quarantine, reporting, or legal-status claims unless exact A0/A1 support is present.

---

## 5. Train-Ready Decision Standard

Train-ready status is task-scoped. A page or dataset component is train-ready only when it satisfies the current task requirements and the following general standards:

- source-backed: every factual claim has a resolvable source/fact/rule anchor;
- web-first: new content is derived from newly retrieved and logged web sources, not from local facts alone;
- scope-aware: source jurisdiction, species, stage, formulation, disease form, and date are compatible with the claim;
- high-risk safe: dose, course, withdrawal/MRL, residue, food safety, legal handling, quarantine, movement, culling, reporting, and vaccine-program claims are exact-source backed or explicitly blocked;
- evaluation-ready: generation boundaries, refusal boundaries, and "do not conclude from" traps are visible where relevant;
- logged: searches, accepted/rejected sources, changed pages, indexes, unresolved gaps, and validation results are recorded.

If any required high-risk evidence is missing, the result cannot be train-ready; mark it `partial`, `source_enrichment_pending`, or blocked according to the status definitions.

## 6. Mandatory execution-log template / V11

Every execution should append a report using this shape:

```md
# <task name> execution log

- Date:
- Scope:
- Target entities:
- Status: complete | partial | blocked

## Task scope and required fields

- Entity type:
- Required fields:
- High-risk dimensions:
- Required authority levels:

## Web/source search

Web search is mandatory for new content under V11. Record all material queries and source decisions.

| Entity | Query | Result | Accepted source_id | Rejected reason |
|---|---|---|---|---|

## New source pages

- `wiki/sources/...`

## Facts extracted from new sources

| fact_id | entity | evidence_source_id | page/span/table | evidence_status |
|---|---|---|---|---|

## Entity pages changed

- `wiki/diseases/...`
- `wiki/drugs/...`

## Comparison/rule/synthesis pages changed

- `wiki/comparisons/...`
- `wiki/rule_cards/...`
- `wiki/synthesis/...`

## Validation

- source pages added:
- source index updated:
- facts added/updated:
- entity pages with new anchors:
- comparison links:
- high-risk gate result:
- unresolved gaps:

## Stop-condition check

- Web search executed first: yes/no
- Adopted web sources opened and classified: yes/no
- Source pages created/indexed before entity claims: yes/no
- Facts extracted from new sources: yes/no
- Entity pages updated: yes/no
- Remaining gaps recorded: yes/no
- High-risk unsupported claims blocked: yes/no
- If any answer is no, status must be partial or blocked.
```
