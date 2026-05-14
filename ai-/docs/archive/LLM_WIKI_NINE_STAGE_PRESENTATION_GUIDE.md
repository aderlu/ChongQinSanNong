# 鸡病系统 LLM Wiki 九阶段现场演示与工作汇报讲稿

本文档用于现场演示和工作汇报。目标不是只列命令，而是把 LLM Wiki 的完整维护链路串起来：从真实知识需求开始，到 LLM 发现权威数据页，再到白名单校验、真实网页或 PDF 抓取、证据摘要抽取、候选事实落库、分层复核、检索上下文、图谱重建、生成/评估审计字段，最后说明系统如何保证权威性、真实性和可追溯性。

你可以按本文顺序复刻演示，也可以把每个阶段的“汇报话术”直接用于现场讲解。

## 九阶段总览

现场汇报时，建议先把九阶段完整结构讲出来。这样 leader 在后续追问“LLM 到底做了什么、数据到底在哪里、HTML 为什么会变化、正式事实有没有被模型直接写入”时，可以始终回到这条链路。

```text
阶段 1：真实知识需求
  作用：确定本轮维护要解决什么鸡病知识问题，例如诊断标准、监管公告、兽药禁用和休药期。
  产物：维护 query、当前 Wiki 状态、后续 fetch 相关性判断依据。

阶段 2：LLM 使用 web access 发现候选权威数据页，系统同步抓取真实数据
  作用：LLM 只提出候选权威数据页 URL 和为什么要看这个页面；系统负责 URL 去重、默认 fetch、保存网页或 PDF、抽取证据摘要。
  产物：candidate_sources、raw/html 或 raw/pdfs、evidence_excerpt、authority_reports。

阶段 3：authority-discover 校验权威白名单，并决定数据是否允许进入 Wiki
  作用：检查 URL 域名是否在 schema 白名单内，同时过滤重复 URL、抓取失败页面、与知识需求无关的页面。
  产物：accepted/rejected 明细、created_sources、fetched_raw_paths、rejected_candidates。

阶段 4：通过校验的权威来源和权威数据进入 raw/ 与 wiki/sources/
  作用：raw 保存真实原始材料，wiki/sources 保存结构化来源登记卡。两者共同证明“系统维护的是可追溯数据，不是只维护链接”。
  产物：raw/urls、raw/html、raw/pdfs、wiki/sources/SRC-xxxx.md。

阶段 5：基于来源数据生成候选事实 knowledge_facts.candidates.json
  作用：把来源、URL、raw 路径、证据摘要、证据角色写入候选事实池。候选层允许自动维护，正式 facts 不允许 LLM 直接写入。
  产物：exports/knowledge_facts.candidates.json。

阶段 6：分层自动复核，并控制是否进入正式事实 knowledge_facts.json
  作用：程序先做 source/raw/URL/excerpt 硬校验，再按诊断、监管、药品、休药期等风险自动分层。
  产物：review_decision、review_reasons、knowledge_facts.review_report.json；高风险事实不会自动进入正式 facts。

阶段 7：query 构建 LLM 检索上下文
  作用：生成和评估流程需要知识时，不让模型凭记忆回答，而是从 Wiki 中取可追溯事实、来源和证据上下文。
  产物：query 返回的 evidence context、source_ids、context chars。

阶段 8：graph-build 重建 graph-data.json 与 knowledge-graph.html
  作用：把新增、修改、删除后的疾病、药品、规则、来源、候选事实重新投影成图谱数据和 HTML 页面。
  产物：wiki/graph-data.json、wiki/knowledge-graph.html、节点数、边数。

阶段 9：生成/评估流程记录 Wiki 审计字段
  作用：把本次生成/评估使用的 Wiki 目录、事实数量、来源 ID、证据状态写入结果，形成可追溯闭环。
  产物：最终 CSV 或评估结果中的 wiki_* 审计字段。
```

一句话概括：

```text
LLM 负责发现候选权威数据页，系统负责抓取真实数据、抽取证据、校验来源、生成候选、分层复核、重建检索和图谱，正式事实必须受控入库。
```

## 0. 演示前准备

### 从哪里开始

进入项目根目录：

```powershell
cd D:\XF-ChongQin\ai-
```

确认 API key 已经配置为环境变量。注意：API key 不应该写入源码、文档或日志。

```powershell
$env:NONELINEAR_API_KEY=[Environment]::GetEnvironmentVariable("NONELINEAR_API_KEY","User")
if (-not $env:NONELINEAR_API_KEY) { throw "NONELINEAR_API_KEY 未配置" }
```

确认 CLI 可以运行：

```powershell
$env:PYTHONPATH="src;."
python -m chicken_data_synthesis.wiki_cli --help
```

### 为什么要先做准备

LLM Wiki 是一个本地知识库维护系统，既要调用三方 LLM 平台，也要写入本地 Wiki 目录。因此演示前必须确认三件事：

```text
1. 当前目录正确：D:\XF-ChongQin\ai-
2. Python 能找到 src 包：PYTHONPATH=src;.
3. Nonelinear API key 存在：NONELINEAR_API_KEY
```

### 代码依据

CLI 入口：

```text
src/chicken_data_synthesis/wiki_cli.py
src/chicken_data_synthesis/interfaces/cli/wiki.py
```

在 `src/chicken_data_synthesis/interfaces/cli/wiki.py` 中可以看到这些命令：

```text
status
schema-check
authority-discover
query
graph-build
daily-maintain
```

### 汇报话术

> 演示从项目根目录开始。LLM Wiki 的所有维护动作都通过 `python -m chicken_data_synthesis.wiki_cli` 进入，CLI 是统一入口。API key 只放在环境变量中，不写入代码，避免泄漏。

## 阶段 1：真实知识需求

### 从哪里开始

先看当前 Wiki 状态：

```powershell
python -m chicken_data_synthesis.wiki_cli --json status
```

重点看这些字段，并在现场解释它们分别代表什么：

```text
purpose_exists
含义：Wiki 根目录下是否存在 purpose.md。
为什么重要：purpose.md 说明这个 Wiki 的维护目标和边界。现场可以解释为“知识库不是散乱文件，而是有明确用途的鸡病权威知识库”。

schema_exists
含义：Wiki 根目录下是否存在 .wiki-schema.md，同时项目中存在 knowledge/schemas/llm_wiki_schema.yaml。
为什么重要：schema 是维护规则的约束来源，说明目录、来源、候选层、审计字段都不是随意设计的。

graph_data_exists
含义：是否存在 wiki/graph-data.json。
为什么重要：graph-data.json 是 HTML 图谱的数据源。它存在，说明图谱可以根据当前知识库状态渲染。

graph_html_exists
含义：是否存在 wiki/knowledge-graph.html。
为什么重要：这是现场可视化展示页面。它存在，说明知识库变化可以被图谱页面展示出来。

raw_file_count
含义：raw/ 目录下原始材料数量，包括 raw/urls、raw/html、raw/pdfs 等。
为什么重要：raw 是可追溯的原始证据层。数量增加通常说明系统发现或抓取了新的来源材料。

section_counts
含义：各类 Wiki 页面数量，例如 diseases、drugs、rules、sources、topics。
为什么重要：它反映知识库结构规模。比如 sources 增加，说明新增了来源页；diseases/drugs/rules 不变，说明没有随意改动核心疾病、药品、规则页面。

fact_count
含义：exports/knowledge_facts.json 中正式事实的数量。
为什么重要：这是判断 LLM 是否直接写入正式事实库的关键字段。自动维护后如果 fact_count 不变，说明 LLM 只进入候选层，没有污染正式事实。

evidence_status_counts
含义：正式事实按证据状态统计，例如 EXTRACTED、INFERRED。
为什么重要：它说明正式事实是直接抽取自来源，还是基于已有知识推断。现场可以用它解释“系统不仅记录事实数量，也记录事实可信状态”。
```

### 这一步做什么

这一阶段不是让 LLM 随机搜索，而是给出真实知识需求。真实知识需求不能删除，也不应该放到 LLM 搜索之后。原因是：它是 LLM 搜索的任务输入、系统校验的上下文、fetch 后相关性判断的依据。如果先让 LLM 漫无目的地搜索，再事后判断，就会变成“先收集一堆网页，再猜哪些有用”，容易引入大量无关入口页、重复来源和不可解释的候选。

当前默认维护不再固定为三个写死需求。系统会先扫描当前 Wiki，动态生成本轮维护需求。扫描范围包括：

```text
wiki/diseases：疾病页，生成诊断标准、临床症状、实验室确诊类权威来源需求。
wiki/drugs：药品页，生成禁用、休药期、官方监管类权威来源需求。
wiki/rules：规则页，生成监管规则、国家标准、官方公告类权威来源需求。
exports/knowledge_facts.candidates.json：历史候选欠账，优先生成补抓取、补元数据需求。
```

动态需求不是简单把某一类缺口全部排在前面。代码会按“候选欠账、疾病、药品、规则”分桶轮询，避免历史候选太多时占满整轮维护。这样每周维护既能补历史证据链，也能持续覆盖疾病诊断、药品监管和规则更新。

如果当前 Wiki 是空库，或者无法扫描到任何维护主题，系统才会退回三条种子级兜底需求：

```text
鸡新城疫 诊断标准 实验室确诊 权威来源 更新
禽流感 鸡病 诊断标准 监管公告 WOAH 权威来源 更新
蛋鸡 兽药 禁用 休药期 农业农村部 国家标准 权威来源 更新
```

注意：这三条现在只是“空库启动种子”，不是长期自动维护的固定范围。

动态生成的需求会覆盖鸡病系统里的三类高价值知识：

```text
1. 疾病诊断标准
2. 疫病监管与国际通报
3. 兽药禁用、休药期和监管规则
```

例如，当前 Wiki 中如果存在 `鸡球虫病`、`传染性支气管炎`、`氨丙啉`、`禁用药规则` 等页面，系统会生成类似下面的维护需求：

```text
鸡球虫病 鸡病 诊断标准 临床症状 实验室确诊 权威来源 更新
传染性支气管炎 鸡病 诊断标准 临床症状 实验室确诊 权威来源 更新
氨丙啉 鸡 兽药 禁用 休药期 官方来源 农业农村部 国家标准 更新
禁用药规则 鸡 兽药 监管规则 禁用 休药期 官方公告 国家标准 更新
```

### 为什么要这么做

LLM Wiki 的维护不是泛泛地“更新知识库”，而是围绕系统的真实业务缺口进行维护。鸡病系统生成病例和评估结果时，最容易出风险的地方是：

```text
诊断依据是否权威
用药规则是否可靠
评估时引用的来源是否可追溯
```

因此第一阶段必须先说明“为什么要维护这些知识”。

现场如果被问“这一阶段能否删除”，回答：

```text
不能删除。
真实知识需求是自动维护的起点，不是事后判断。
但真实知识需求不应该长期写死为某几个病。现在项目中是先扫描 Wiki 缺口，再动态生成本轮维护需求。
它决定 LLM 搜索什么、白名单通过后是否需要 fetch、fetch 摘要是否和任务相关、最终候选事实应该进入哪个复核主题。
没有真实知识需求，LLM Wiki 只是在收集网站；有真实知识需求，LLM Wiki 才是在维护鸡病系统真正需要的权威数据。
```

### 执行结果怎么看

`status` 返回中，每个字段的解释可以这样讲：

```text
fact_count: 正式事实数量。这个数字代表已经进入 knowledge_facts.json 的事实，不包含候选事实。
raw_file_count: raw 原始材料数量。这个数字代表系统保存了多少原始 URL、网页正文或 PDF。
section_counts.sources: source 来源页数量。这个数字代表可追溯来源页数量，新增权威来源后通常会增加。
graph_data_exists / graph_html_exists: 图谱数据和 HTML 页面是否已经生成。
evidence_status_counts: 正式事实证据状态分布，用来说明事实是 EXTRACTED 还是 INFERRED。
```

如果 `fact_count` 没变，而 sources 增加，说明系统新增的是候选来源，不是直接新增正式事实。

### 代码依据

状态统计代码：

```text
src/chicken_data_synthesis/infrastructure/knowledge/operations.py
build_status_report()
```

CLI 分发代码：

```text
src/chicken_data_synthesis/interfaces/cli/wiki.py
args.command == "status"
```

### 汇报话术

> 第一阶段先定义真实知识需求。这里不是让 LLM 随便扩写鸡病知识，而是围绕诊断标准、监管公告、兽药规则三类高风险知识做维护。这样可以保证后续维护和生成/评估流程真正相关。

## 阶段 2：LLM 使用 web access 发现候选权威数据页，系统同步抓取真实数据

### 从哪里开始

执行一次真实 LLM 维护：

```powershell
$env:PYTHONPATH="src;."
python -m chicken_data_synthesis.wiki_cli --json daily-maintain `
  --base-url "https://api.nonelinear.com/v1" `
  --model "gpt-5.4-mini-medium" `
  --max-queries 8
```

这条命令在没有传 `--query` 时，会先调用 `build_maintenance_queries()` 从当前 Wiki 缺口动态生成维护需求，默认最多 8 个。它不会只维护鸡新城疫，也不会长期固定维护三条演示 query。

如果现场想限制本轮动态需求数量，可以加：

```powershell
python -m chicken_data_synthesis.wiki_cli --json daily-maintain `
  --base-url "https://api.nonelinear.com/v1" `
  --model "gpt-5.4-mini-medium" `
  --max-queries 5
```

如果现场想演示指定主题，可以显式传 `--query`。一旦传了 `--query`，系统就按你给出的主题维护，不再使用动态扫描结果：

```powershell
python -m chicken_data_synthesis.wiki_cli --json daily-maintain `
  --base-url "https://api.nonelinear.com/v1" `
  --model "gpt-5.4-mini-medium" `
  --query "鸡球虫病 鸡病 诊断标准 临床症状 实验室确诊 权威来源 更新" `
  --query "氨丙啉 鸡 兽药 禁用 休药期 官方来源 农业农村部 国家标准 更新"
```

这条命令现在会默认 fetch。也就是说，第二阶段不是“只维护 URL”。LLM 负责发现候选权威数据页，系统随后会对通过校验、未重复、具体度较高的 URL 抓取真实网页或 PDF，把原文保存到 `raw/html` 或 `raw/pdfs`，再从抓取内容中抽取 `evidence_excerpt` 写入候选层。如果现场只想演示“发现 URL 但不抓正文”，才加：

```powershell
python -m chicken_data_synthesis.wiki_cli --json daily-maintain `
  --base-url "https://api.nonelinear.com/v1" `
  --model "gpt-5.4-mini-medium" `
  --no-fetch
```

如果要演示“每周自动维护”，展示脚本：

```powershell
.\scripts\register_llm_wiki_weekly_task.ps1 -DayOfWeek "Monday" -At "03:00"
```

每周实际执行脚本：

```text
scripts/run_llm_wiki_weekly_maintenance.ps1
```

### 这一步做什么

这一步调用 Nonelinear 的 `gpt-5.4-mini-medium`，让 LLM 根据真实知识需求提出候选权威数据页面 URL。这里要特别说明：LLM 不是最终数据维护者，它是“权威数据页发现者”；真正的数据维护由系统完成，包括抓取页面、保存原文、抽取证据摘要、写入候选事实池。

当前代码已经不是“只发现来源”，而是“发现具体页面 + 去重 + fetch + 原始数据保存 + 证据摘要 + 候选事实”的链路：

```text
真实知识需求
  -> LLM 优先搜索具体权威页面、公告、标准详情页、疾病手册页或 PDF
  -> LLM 只返回候选数据页 URL、标题、理由和证据角色
  -> 系统进行同批 URL 去重
  -> 系统和已有 source/raw URL 做跨库去重
  -> 通过白名单后默认 fetch 真实网页或 PDF
  -> 将网页保存到 raw/html，或将 PDF 保存到 raw/pdfs
  -> 抽取 evidence_excerpt 证据摘要
  -> 摘要必须和 query/title 有关键词关联
  -> 通过后才进入 raw/、wiki/sources/ 和 candidates
```

注意：LLM 在这里仍然不输出正式事实。它输出的是“应该去哪里拿权威数据”；真实数据由系统 fetch 获取，证据摘要由系统从抓取内容中抽取，候选事实由系统写入 `knowledge_facts.candidates.json`，正式 facts 仍然必须复核后才能写入。

典型返回结构：

```json
{
  "sources": [
    {
      "url": "https://www.woah.org/",
      "title": "WOAH 官方站点",
      "reason": "用于检索动物卫生与相关国际参考资料入口",
      "evidence_role": "clinical_reference"
    }
  ]
}
```

### 为什么要这么做

LLM 有搜索和总结能力，但不能天然保证真实性。鸡病诊断、兽药、监管规则属于高风险知识，所以系统把 LLM 的权限限制在“发现候选权威数据页面”，把真实数据获取交给系统的 fetch 流程：

```text
LLM 可以找 URL
LLM 可以说明为什么这个 URL 可能有用
系统负责抓取网页、公告或 PDF
系统负责抽取证据摘要
系统负责判断抓取内容是否和知识需求相关
LLM 不能直接写正式事实
LLM 不能绕过白名单
LLM 不能把总结当作权威结论
```

这是一条权限分离链路：

```text
LLM 的权限：发现候选权威数据页。
系统的权限：抓取真实页面或 PDF、保存 raw、抽取 evidence_excerpt、做白名单和相关性校验。
复核层的权限：决定候选能否继续提升。
正式事实库的权限：只能接收复核后确认的事实，不接收 LLM 直接输出。
```

如果被问“为什么第二阶段不是直接输出事实”，回答：

```text
因为 LLM 输出的事实可能误读网页、混淆版本或夹带推断。
所以第二阶段只允许 LLM 给出权威数据页面 URL，不允许它直接给结论。
但系统不会停在 URL，会默认 fetch URL，拿到真实网页/PDF，保存 raw，并抽取 evidence_excerpt。
这样进入流程的是权威来源、权威原文和可复核证据摘要，而不是 LLM 自己编写的事实。
```

### 执行结果怎么看

重点看 `daily-maintain` 返回。不要只读数字，要把每个字段和维护链路对应起来：

```text
wiki_dir
含义：本次维护写入的 Wiki 目录。
解释口径：它证明本轮维护作用在鸡病权威 Wiki，而不是临时目录或其他知识库。

base_url / model
含义：本次调用的三方 LLM 平台地址和模型。
解释口径：这里展示的是 Nonelinear 的 https://api.nonelinear.com/v1 和 gpt-5.4-mini-medium，说明是一次真实模型调用。

query_count
含义：本轮维护执行了多少个知识需求。
解释口径：现在默认不是固定 3 个，而是由 `build_maintenance_queries()` 从当前 Wiki 缺口动态生成，默认最多 8 个。现场要看 `maintenance_queries` 才能知道本轮实际维护了哪些疾病、药品、规则或候选欠账。

maintenance_queries
含义：本轮实际执行的维护需求列表。
解释口径：这个字段是判断“是否只维护鸡新城疫”的关键依据。如果列表里来自多种 disease、drug、rule 和 candidate gap，就说明系统在维护整个鸡病知识库，而不是固定维护某一个疾病。

accepted_count
含义：通过白名单、去重、fetch 相关性等准入检查的候选数据页总数。
解释口径：accepted 现在代表“域名权威、没有与已有知识库重复、fetch 后内容与知识需求相关，并允许进入候选层”。它仍然不代表里面的事实已经被确认为正式事实。

rejected_count
含义：被白名单、URL 合法性、去重、fetch 或相关性校验拒绝的候选数据页总数。
解释口径：如果出现 rejected，可能是非白名单域名、已有重复来源、fetch 失败，或抓取内容和知识需求不相关。这不是错误，而是安全过滤结果。

candidate_sources
含义：LLM 输出的候选来源列表，包含 url、title、reason、evidence_role。
解释口径：这是 LLM 的输出结果，但它仍然只是“候选数据页清单”。真实数据是否进入 Wiki，要看后续 authority_reports 里的 fetch 和校验结果。

authority_reports
含义：每个知识需求经过 authority-discover 后的落库报告。
解释口径：它能看到每个 query 创建了哪些 source 页面，哪些 URL 被拒绝，是否执行了 fetch，抓取后的 raw 文件在哪里，以及为什么被拒绝。

graph_report
含义：本轮维护后图谱重建结果，包括 graph-data.json、knowledge-graph.html、节点数、边数。
解释口径：它证明 HTML 图谱会跟随知识库变化重建。

graph_change_report
含义：本轮维护前后图谱的差异报告，包括维护前后节点数、边数、新增节点、删除节点、新增边、删除边。
解释口径：它不是只说“图谱重建了”，而是说明图谱具体变了什么。新增 source/candidate 会体现为 added_nodes 或 added_links；删除 source/fact/candidate 后会体现为 removed_nodes 或 removed_links。

status_report
含义：维护结束后的 Wiki 总体状态。
解释口径：它用来确认 raw、sources、facts、graph 等最终数量是否符合预期。

schema_ok
含义：维护结束后是否仍符合 llm_wiki_schema.yaml。
解释口径：true 说明目录结构、白名单策略、候选层约束、审计字段没有被破坏。

lint_ok
含义：维护结束后 Wiki 内部一致性是否通过检查。
解释口径：true 说明没有明显断链、索引缺失、证据状态异常等问题。

warnings
含义：维护过程中的非致命警告。
解释口径：空列表说明 LLM JSON 解析、降级重试、候选处理等过程没有出现需要关注的问题。
```

同时查看 `log_tail` 或 `log.md` 时，要重点找四类日志：

```text
maintenance-task
含义：每个 query 的处理摘要。
说明：记录 query、accepted、rejected、created_sources、fetched_raw、candidates、rejected_reasons、reason、evidence。

source-create
含义：新增 source 来源页。
说明：现在会记录 reason、evidence、external_url，证明新增来源不是随意写入。

candidate-create
含义：新增候选事实。
说明：记录 fact_id、source、reason、evidence、evidence_status=NEEDS_REVIEW，证明候选仍在待复核层。

candidate-review
含义：候选事实分层复核写回。
说明：记录 total、decisions、reason=layered_program_review、evidence=knowledge_facts.review_report.json。

graph-diff
含义：维护前后图谱变化摘要。
说明：记录 nodes 前后数量、links 前后数量、新增/删除节点数、新增/删除边数，以及 graph-data.json 和 HTML 作为证据。
```

还要重点看 `authority_reports[].fetched_raw_paths` 和 `exports/knowledge_facts.candidates.json`：

```text
fetched_raw_paths
含义：系统真实抓取后落到 raw/html 或 raw/pdfs 的文件路径。
解释口径：这个字段能直接证明系统维护了真实数据。如果为空，需要看是否使用了 --no-fetch、URL 是否重复、页面是否抓取失败，或是否因为内容不相关被拒绝。

knowledge_facts.candidates.json
含义：候选事实池，里面会保存 source_page、external_url、evidence_role、evidence_excerpt、review_decision 等字段。
解释口径：这说明 URL 后面的数据已经被转成可复核候选，而不是停留在链接层。
```

当前增强后常见的 rejected 原因：

```text
duplicate_existing_source
含义：该 URL 已经存在于 wiki/sources 或 raw/urls 中。
说明：系统不会重复创建 source，避免知识图谱和候选事实膨胀。

domain_not_allowlisted
含义：URL 不属于 schema 白名单里的权威域名。
说明：系统拒绝非权威来源。

fetch_failed:...
含义：URL 通过了白名单，但网页/PDF 抓取失败。
说明：没有真实数据进入 raw，因此不会创建候选 source。

fetched_content_not_relevant_to_query
含义：URL 能抓取，但正文摘要和当前知识需求或标题没有明显关联。
说明：系统拒绝“权威网站上的无关入口页”，保证进入流程的是权威数据，而不仅是权威域名。
```

示例结果说明：

```text
query_count=3
表示系统执行了三个真实维护主题。

accepted_count=15
表示 LLM 给出的 15 个 URL 都通过了权威域名白名单。但要强调：通过白名单只说明来源入口可信，不说明页面中的具体事实已经被正式采用。

rejected_count=0
表示没有 URL 被白名单拒绝。

warnings=[]
表示 LLM 输出 JSON 可以被解析，维护过程没有降级问题。
```

### 代码依据

LLM 客户端：

```text
src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py
NonelinearAuthorityClient
```

自动维护主流程：

```text
src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py
run_daily_maintenance()
```

动态维护需求生成：

```text
src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py
build_maintenance_queries()
```

这段代码会扫描 `wiki/diseases`、`wiki/drugs`、`wiki/rules` 和 `exports/knowledge_facts.candidates.json`，优先维护候选欠账，再覆盖疾病、药品和规则页面。

CLI 参数入口：

```text
src/chicken_data_synthesis/interfaces/cli/wiki.py
daily-maintain
```

受控提示词位置：

```text
src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py
_build_authority_messages()
```

### 现场可讲代码

讲 `NonelinearAuthorityClient`：

```text
它只调用 /chat/completions。
它不把 API key 写死，而是由 run_daily_maintenance 从 NONELINEAR_API_KEY 读取。
它不传 temperature=0，因为 gpt-5.4-mini-medium 只支持默认 temperature。
它要求模型输出 JSON，但如果三方平台不支持 response_format，会自动降级重试。
```

讲 `_build_authority_messages()`：

```text
提示词明确告诉 LLM：
只找候选权威数据页 URL；
只允许白名单域名；
不要输出诊断结论；
不要输出用药建议；
不要输出正式事实。
```

### 汇报话术

> 第二阶段是真实调用 LLM。这里的 LLM 不是直接维护正式知识，而是作为“权威数据页发现助手”。它只负责提出应该访问哪些权威页面、公告、标准详情页或 PDF；系统会继续做去重、白名单校验、默认 fetch、raw 原文保存、证据摘要抽取和候选事实写入。所以这一阶段维护的不是单纯 URL，而是从 URL 入口开始，把权威原始数据带入 LLM Wiki 的候选链路。

## 阶段 3：authority-discover 校验权威白名单，并决定数据是否允许进入 Wiki

### 从哪里开始

`daily-maintain` 内部会自动调用：

```text
run_daily_maintenance()
  -> discover_authority_sources()
```

也可以手动演示一条 URL：

```powershell
python -m chicken_data_synthesis.wiki_cli --json authority-discover `
  "真实 fetch 测试：新城疫 WOAH 权威页面" `
  --url "https://www.woah.org/en/disease/newcastle-disease/"
```

如果要展示真实网页抓取，加 `--fetch`：

```powershell
python -m chicken_data_synthesis.wiki_cli --json authority-discover `
  "真实 fetch 测试：新城疫 WOAH 权威页面" `
  --url "https://www.woah.org/en/disease/newcastle-disease/" `
  --fetch `
  --timeout 60
```

### 这一步做什么

系统接收 LLM 输出的候选数据页 URL，然后判断这个 URL 后面的数据是否允许进入 Wiki。这里不是简单判断“链接是不是权威域名”，而是连续做五件事：

```text
1. URL 格式校验
   只接受 http/https 的合法 URL，拒绝空 URL、错误协议和无法解析的地址。

2. 权威域名白名单校验
   只接受 schema 中允许的官方或权威兽医来源域名。

3. 跨库去重
   检查这个 URL 是否已经存在于 wiki/sources 或 raw/urls，避免重复创建来源和候选。

4. 默认 fetch 真实数据
   对通过校验的具体页面抓取 HTML 或 PDF，保存到 raw/html 或 raw/pdfs。

5. 抓取后相关性校验
   从正文中抽取 evidence_excerpt，并检查摘要是否与 query/title 相关。权威网站上的无关首页或导航页也会被拒绝。
```

当前白名单来自 schema：

```text
moa.gov.cn
std.cahec.cn
openstd.samr.gov.cn
samr.gov.cn
woah.org
merckvetmanual.com
ema.europa.eu
fao.org
```

### 为什么要这么做

LLM 可能返回博客、转载页、商业推广页、不存在的 URL，也可能返回权威网站首页但不是具体数据页。第三阶段的目的，是把“LLM 发现的候选页面”变成“系统确认可以进入 Wiki 的权威数据材料”。

白名单是自动维护的第一道硬边界：

```text
白名单内：进入候选来源层
白名单外：拒绝，不落库
```

但只有白名单还不够，所以代码又增加了去重、fetch、证据摘要和相关性校验。这一步保证“自动化”不会变成“不受控写入”，也不会变成“只收集权威网站首页”。

### 执行结果怎么看

看 `authority_reports` 中每个主题。这个对象是“候选数据页被系统处理后的审计记录”，字段含义如下：

```text
wiki_dir
含义：本次 authority-discover 写入的 Wiki 目录。
为什么重要：证明来源落库发生在当前鸡病权威 Wiki 中。

query
含义：触发本次来源发现的知识需求。
为什么重要：可以把“为什么新增这个来源”追溯回具体业务问题。

accepted_count
含义：通过白名单、去重和 fetch 相关性校验，并进入候选来源层的数据页数量。
为什么重要：它说明有多少候选数据页被系统允许落库。

rejected_count
含义：被拒绝的 URL 数量。
为什么重要：如果 LLM 返回了非权威站点、错误协议或不合法 URL，这里会体现出来。

created_sources
含义：系统为通过校验的 URL 创建的 wiki/sources/*.md 文件。
为什么重要：这是可追溯来源页，后续事实抽取、复核和图谱展示都要依赖它。

fetched_raw_paths
含义：真实抓取并保存的 raw/html 或 raw/pdfs 文件。
为什么重要：这是“维护数据”的直接证据。如果这里有文件，说明系统已经把网页正文或 PDF 原文落到了 raw 原始证据层；如果为空，需要结合 rejected_candidates 和 warnings 判断是重复、抓取失败、使用 --no-fetch，还是内容不相关。

evidence_excerpt
含义：系统从 fetch 到的网页正文中抽取的证据摘要，会写入 source page 和候选事实。
为什么重要：它证明系统不只是保存 URL，还保存了可复核的实际数据片段。

candidates_path
含义：候选事实文件路径，通常是 exports/knowledge_facts.candidates.json。
为什么重要：说明自动维护结果进入了候选层，而不是正式 facts。

warnings
含义：本次 authority-discover 的非致命警告。
为什么重要：用于发现 URL 重复、解析异常、fetch 降级等问题。

rejected_candidates
含义：被拒绝候选数据页的明细和拒绝原因。
为什么重要：可以向 leader 展示系统不是无条件相信 LLM，而是会明确拒绝不合规来源、重复来源、抓取失败来源和权威网站上的无关页面。
```

增强后的 authority-discover 不只做白名单，还做三类质量控制：

```text
1. 跨库 URL 去重
已有 source/raw URL 不再重复落库，避免 source 和 graph 膨胀。

2. fetch 后证据抽取
默认抓取 HTML 或 PDF，HTML 会生成 evidence_excerpt。

3. fetch 后相关性校验
如果抓取摘要和 query/title 没有关键词关联，会以 fetched_content_not_relevant_to_query 拒绝。
```

示例：

```text
accepted_count: 5
rejected_count: 0
created_sources:
  wiki/sources/SRC-0136-woah-世界动物卫生组织.md
  wiki/sources/SRC-0137-fao-联合国粮农组织.md
```

如果执行 `--fetch`，会看到：

```text
fetched_raw_paths:
  raw/html/真实-fetch-测试-新城疫-woah-权威页面.html
```

### 代码依据

白名单和来源发现：

```text
src/chicken_data_synthesis/infrastructure/knowledge/authority.py
discover_authority_sources()
```

权威域名配置：

```text
src/chicken_data_synthesis/infrastructure/knowledge/contracts.py
AUTHORITY_ALLOWED_DOMAINS
```

schema 约束：

```text
knowledge/schemas/llm_wiki_schema.yaml
maintenance.authority_discovery.allowed_domains
maintenance.authority_discovery.candidate_only
maintenance.authority_discovery.must_not_write_authoritative_facts
```

### 汇报话术

> 第三阶段是权威数据准入。LLM 输出候选数据页后，系统不会直接相信它，而是先用 schema 的 allowed_domains 做白名单校验，再做 URL 去重、默认 fetch、证据摘要抽取和相关性过滤。只有通过这些检查的页面，才会把真实网页或 PDF 放入 raw，把来源登记放入 wiki/sources，把候选事实放入 candidates。被拒绝的来源和数据不会落库。

## 阶段 4：通过校验的权威来源和权威数据进入 raw/ 与 wiki/sources/

### 从哪里开始

查看新增 source 文件：

```powershell
Get-ChildItem knowledge\llm_wiki_chicken_authoritative\wiki\sources |
  Select-Object -Last 10 Name
```

这条命令的作用是查看最近创建的来源页。`wiki/sources` 不是原始网页正文，而是来源登记卡，里面记录来源标题、URL、来源类型、权威等级、摘要和证据角色。现场可以解释为：“source 页是把外部权威来源纳入 Wiki 管理的入口”。

查看 raw URL 记录：

```powershell
Get-ChildItem knowledge\llm_wiki_chicken_authoritative\raw\urls |
  Select-Object -Last 10 Name
```

这条命令查看的是 URL 入口记录。它说明系统已经发现并保存了来源入口。注意：在默认 `daily-maintain` 中，系统会继续抓取正文；只有显式 `--no-fetch` 时，才会只停留在 URL 入口层。

注意：当前 `daily-maintain` 已经默认 fetch。只有显式使用 `--no-fetch` 时，才会只记录 URL 而不抓取 raw/html 或 raw/pdfs。

查看 fetch 后的 raw HTML：

```powershell
Get-ChildItem knowledge\llm_wiki_chicken_authoritative\raw\html |
  Select-Object -Last 5 Name
```

这条命令查看真实网页抓取结果。默认 `daily-maintain` 会尝试抓取真实权威数据，所以常规每周维护会在 `raw/html` 或 `raw/pdfs` 里保存正文文件。现场可以解释为：“raw/html 和 raw/pdfs 是后续事实抽取与复核的原始证据，不是 LLM 生成内容”。

### 这一步做什么

通过白名单、去重和 fetch 相关性校验的数据会进入三类位置：

```text
raw/urls/
记录 URL 本身，说明系统发现了这个权威入口。

raw/html/ 或 raw/pdfs/
保存真实网页正文或 PDF。它是事实抽取和复核的原始数据层。

wiki/sources/
为每个来源创建可读的 source 页面，记录标题、URL、来源类型、权威等级、摘要、证据角色、证据摘录和 raw 路径。
```

### 为什么要这么做

LLM Wiki 不只要“知道来源”，还要“保存数据并可追溯”。`raw` 保存外部权威页面或 PDF 的原始材料，`wiki/sources` 保存结构化来源元数据和证据摘要，两者共同保证后续事实抽取可以追踪到原始依据。

现场可以这样区分：

```text
raw/urls：我从哪里发现这个来源。
raw/html 或 raw/pdfs：我实际抓到了什么权威原文。
wiki/sources：我把这个权威原文登记成哪个 Wiki 来源。
knowledge_facts.candidates.json：我基于这个来源形成了哪些待复核候选。
```

### 执行结果怎么看

本次真实维护结果中，新增 source 示例：

```text
SRC-0136-woah-世界动物卫生组织.md
SRC-0137-fao-联合国粮农组织.md
SRC-0138-merck-veterinary-manual.md
SRC-0139-全国标准信息公共服务平台.md
SRC-0140-中国动物卫生与流行病学中心标准平台.md
```

这些文件名中的 `SRC-0136`、`SRC-0137` 是来源 ID。来源 ID 的作用是把后续候选事实、检索上下文、图谱节点和审计字段串起来。也就是说，后续如果生成或评估结果引用了某个知识点，就可以追溯到对应的 `SRC-xxxx` 来源页。

真实 fetch 示例：

```text
raw/html/真实-fetch-测试-新城疫-woah-权威页面.html
wiki/sources/SRC-0135-newcastle-disease.md
```

这组结果说明两件事：第一，网页正文已经真实保存到 `raw/html`；第二，系统为它创建了 `wiki/sources/SRC-0135-newcastle-disease.md` 来源页。raw 文件偏原始证据，source 文件偏结构化登记，两者共同完成可追溯落库。

### 代码依据

来源落库：

```text
src/chicken_data_synthesis/infrastructure/knowledge/authority.py
_materialize_candidate()
discover_authority_sources()
```

source 页面创建：

```text
src/chicken_data_synthesis/infrastructure/knowledge/registry.py
create_source_page()
```

cache 更新：

```text
src/chicken_data_synthesis/infrastructure/knowledge/cache.py
cache_update()
```

### 汇报话术

> 第四阶段是权威来源和权威数据落库。通过校验的 URL 不会直接变成正式事实，而是先形成 raw 原始材料和 source 来源页。raw 保存真实网页或 PDF，source 保存结构化来源登记和证据摘要。这样每个候选数据都有文件、有路径、有元数据，后续复核可以追到具体页面和具体原文。

## 阶段 5：基于来源数据生成候选事实 knowledge_facts.candidates.json

### 从哪里开始

查看候选事实文件：

```powershell
Get-Content knowledge\llm_wiki_chicken_authoritative\exports\knowledge_facts.candidates.json -Tail 80
```

这条命令不是查看正式事实库，而是查看候选事实池。现场要强调：`knowledge_facts.candidates.json` 是“待复核区”，它允许自动维护写入；`knowledge_facts.json` 是“正式事实区”，不能由 LLM 自动写入。

### 这一步做什么

系统会把通过校验的权威来源和抓取到的证据数据写入候选事实文件：

```text
knowledge/llm_wiki_chicken_authoritative/exports/knowledge_facts.candidates.json
```

这里的候选事实不是正式事实，而是等待复核的中间层。它不是单纯保存 URL，而是把“来源登记 + 外部 URL + raw 原文路径 + evidence_excerpt + 证据角色 + 复核状态”组合成可治理的候选记录。

候选事实通常需要关注这些信息：

```text
candidate id
含义：候选事实自身的编号。
作用：用于后续复核、去重和提升为正式事实时定位候选记录。

title / subject
含义：候选来源或候选事实涉及的主题。
作用：帮助复核人员快速判断它对应哪类疾病、规则、药品或标准。

source_page / source_id
含义：候选事实关联的 source 页面或来源 ID。
作用：保证候选事实不是孤立文本，而是能追溯到具体来源。

external_url
含义：候选事实对应的外部权威页面或 PDF URL。
作用：用于复核时回到原始网站，也用于后续去重，避免同一个数据页重复进入 Wiki。

raw_path / fetched_raw_path
含义：系统抓取后保存到 raw/html 或 raw/pdfs 的本地原始材料路径。
作用：证明候选不是 LLM 自己写的，而是有本地保存的原始证据。

evidence_excerpt
含义：系统从抓取正文中抽取的证据摘要。
作用：复核时可以先看摘要判断是否相关，再回到 raw 原文或外部 URL 做确认。

evidence_role
含义：这个来源在证据链中的角色，例如 diagnosis_standard、clinical_reference、regulation、drug_rule。
作用：帮助系统和复核人员判断它属于诊断标准、临床参考、监管规则还是药品规则。

evidence_status
含义：候选证据状态，通常处于 NEEDS_REVIEW 或类似待复核状态。
作用：提醒系统和人员它还不能当作正式事实使用。

created_at / updated_at
含义：候选记录产生或更新的时间。
作用：用于审计和判断候选是否过期。
```

### 为什么要这么做

这是 LLM Wiki 的安全缓冲区。LLM 可以提出候选数据页，系统可以抓取数据并生成候选，但不能越过复核直接进入正式事实库。

安全边界是：

```text
knowledge_facts.candidates.json
  可以由自动维护追加

knowledge_facts.json
  不能由 LLM 自动写入
  必须经过复核后才能更新
```

### 执行结果怎么看

如果 `daily-maintain` 运行后：

```text
sources 增加
raw_file_count 增加
knowledge_facts.candidates.json 更新
fact_count 不变
```

这说明系统行为正确：自动维护抓到了数据、登记了来源、生成了候选，但没有污染正式事实库。

现场可以打开候选文件，重点讲这些字段之间的关系：

```text
source_page
说明候选来自哪个 Wiki 来源页。

external_url
说明这个来源页对应哪个外部权威网页或 PDF。

raw_path 或 fetched_raw_path
说明系统是否已经把外部数据抓到了本地 raw。

evidence_excerpt
说明系统从真实抓取内容中抽到了什么可复核片段。

review_decision
说明第六阶段自动复核后，这条候选属于自动通过来源候选、需要补抓取、需要补元数据、需要人工确认，还是被拒绝。
```

本次结果中：

```text
fact_count: 1748
evidence_status_counts:
  EXTRACTED: 1633
  INFERRED: 115
```

`fact_count` 没变，说明 LLM 没有直接新增正式事实。

这里的 `EXTRACTED` 表示正式事实是从来源材料中抽取得到，可信度和可追溯性更强；`INFERRED` 表示事实来自系统已有知识之间的推断或整理，现场要说明它仍然需要保留来源链路和审计字段。候选事实不应该混入这两个正式状态，否则会让“待复核”和“已复核”的边界变模糊。

### 代码依据

候选事实写入：

```text
src/chicken_data_synthesis/infrastructure/knowledge/authority.py
discover_authority_sources()
write_candidate_facts()
```

schema 安全约束：

```text
knowledge/schemas/llm_wiki_schema.yaml
candidate_only: true
must_not_write_authoritative_facts: true
```

### 汇报话术

> 第五阶段是候选事实层。自动维护的结果不是只保存 URL，而是把 source、external_url、raw 原文路径、证据摘要、证据角色和复核状态写入 `knowledge_facts.candidates.json`。这个文件相当于待审池。正式事实库 `knowledge_facts.json` 没有被 LLM 直接改写，所以系统可以自动维护真实数据，同时控制真实性风险。

## 阶段 6：分层自动复核，并控制是否进入正式事实 knowledge_facts.json

### 从哪里开始

先执行候选事实分层自动复核：

```powershell
python -m chicken_data_synthesis.wiki_cli --json review-candidates
```

这条命令会读取 `exports/knowledge_facts.candidates.json`，对候选事实执行程序硬校验和风险分层，并把结果写回候选文件，同时生成：

```text
exports/knowledge_facts.review_report.json
```

在完整自动维护中，`daily-maintain` 会自动调用这个复核步骤。因此现场可以说：第六阶段不是口头上的“等人工复核”，而是已经实现了可执行的分层自动复核。

再查看正式事实数量：

```powershell
python -m chicken_data_synthesis.wiki_cli --json status
```

这条命令通过 `fact_count` 间接查看正式事实规模。它适合现场对比：自动维护前后如果 `sources` 增加但 `fact_count` 不变，说明自动维护没有越权写入正式事实。

查看正式事实文件：

```powershell
Get-Item knowledge\llm_wiki_chicken_authoritative\exports\knowledge_facts.json
```

这条命令确认正式事实文件存在。正式事实文件是生成和评估流程真正可以依赖的结构化事实库，不等同于候选事实文件。

### 这一步做什么

这一阶段做两件事。

第一，自动复核候选事实：

```text
knowledge_facts.candidates.json
  -> review_candidate_facts()
  -> 程序硬校验 source/raw/URL/excerpt
  -> 风险分层
  -> 写入 review_decision / review_tier / review_reasons
  -> 生成 knowledge_facts.review_report.json
```

第二，继续控制正式事实库：

```text
exports/knowledge_facts.json
```

当前自动维护会完成分层复核，但不会让 LLM 或程序无条件把高风险候选写入正式 facts。低风险来源记录可以进入 `AUTO_READY_SOURCE`，高风险诊断、监管、兽药、休药期内容会进入 `HUMAN_REQUIRED`。历史候选如果只有 URL 或 source、缺少 raw 原文和证据摘要，会进入 `LEGACY_NEEDS_FETCH` 或 `LEGACY_NEEDS_METADATA`，成为后续自动补全队列。

### 为什么要这么做

鸡病诊断和兽药规则不能由 LLM 自行判断后直接入库。现在采用的是分层自动化复核：

```text
程序硬校验层
  检查 source_page 是否存在、raw 文件是否存在、external_url 是否在白名单内、evidence_excerpt 是否存在。

规则风险层
  根据 evidence_role、subject、evidence_excerpt 判断是否涉及诊断、监管、兽药、休药期、标准等高风险主题。

自动决策层
  AUTO_READY_SOURCE：低风险来源记录已具备追溯条件，可以作为来源候选继续流转。
  HUMAN_REQUIRED：高风险候选需要人工确认后才能提升为正式事实。
  LEGACY_NEEDS_FETCH：历史候选已有 source/URL，但缺少正文摘要，需要补 fetch。
  LEGACY_NEEDS_METADATA：历史候选有 source 页面，但缺少 external_url 等元数据，需要补齐登记信息。
  REJECTED：source/raw/URL/证据摘要不完整或不合规，不能进入后续事实提升。
```

正式事实必须满足：

```text
1. 来源在权威白名单内。
2. 有 raw 原文、网页正文或 PDF。
3. source 页面记录完整。
4. 候选事实和来源内容一致。
5. 自动复核不是 REJECTED。
6. 高风险事实经过人工确认。
7. 能被 schema-check 和 lint 验证。
```

### 执行结果怎么看

复核结果重点看：

```text
total_count
含义：候选事实总数。

auto_ready_count
含义：低风险、来源追溯完整、可自动进入“来源就绪”状态的候选数量。

human_required_count
含义：涉及诊断、监管、兽药、休药期等高风险内容，需要人工最终确认的候选数量。

needs_fetch_count
含义：历史候选中已有来源记录，但缺少 raw/html、raw/pdfs 或 evidence_excerpt，需要后续自动补抓取的数量。

needs_metadata_count
含义：历史候选中 source 页面存在，但外部 URL、证据角色等元数据不完整，需要补齐登记信息的数量。

rejected_count
含义：source/raw/URL/证据摘要等硬条件不满足，被自动拒绝的候选数量。

decision_counts
含义：按 AUTO_READY_SOURCE、HUMAN_REQUIRED、LEGACY_NEEDS_FETCH、LEGACY_NEEDS_METADATA、REJECTED 汇总的决策分布。
```

正式事实数量仍然看：

```text
fact_count: 1748
```

说明正式 facts 没有因为 LLM 维护而被无约束增加。这是符合设计的。

现场可以继续解释：正式 facts 不增加，并不表示 LLM Wiki 没有更新。它表示更新停留在更安全的候选层和来源层。也就是说：

```text
source 增加
表示系统发现了更多可追溯来源。

raw_file_count 增加
表示系统记录或抓取了更多原始材料。

candidate 文件更新
表示系统产生了待复核候选。

fact_count 不变
表示正式知识没有被 LLM 自动污染。
```

如果 leader 问“复核是不是必须人工”，回答：

```text
不是必须全部人工。
项目现在已经实现分层自动复核：程序先做硬校验，规则再做风险分层，低风险来源记录可自动进入 AUTO_READY_SOURCE；历史欠账会进入 LEGACY_NEEDS_FETCH 或 LEGACY_NEEDS_METADATA，形成自动治理队列。
但诊断标准、兽药规则、监管公告解释等高风险正式事实，仍然需要人工最终确认。
所以系统不是人工阻塞，也不是 LLM 无约束自动写事实，而是“自动复核 + 风险分流 + 高风险人工确认”。
```

这里要强调“分层自动化”不是“全部自动写正式 facts”：

```text
低风险来源完整性检查：可以自动完成。
历史候选补抓取、补元数据：可以自动形成治理队列。
高风险事实判断：可以自动识别风险，但最终进入正式 facts 前仍需要确认。
不合规候选：可以自动拒绝。
```

### 代码依据

分层自动复核代码：

```text
src/chicken_data_synthesis/infrastructure/knowledge/review.py
review_candidate_facts()
```

自动维护中调用复核：

```text
src/chicken_data_synthesis/infrastructure/knowledge/maintenance.py
run_daily_maintenance()
```

正式事实读取和检索：

```text
src/chicken_data_synthesis/infrastructure/knowledge/wiki.py
load_llm_wiki()
build_llm_wiki_context()
```

lint 对事实状态的检查：

```text
src/chicken_data_synthesis/infrastructure/knowledge/operations.py
lint_wiki()
```

最终 CSV 审计字段：

```text
knowledge/schemas/llm_wiki_schema.yaml
audit.output_csv_fields
```

### 汇报话术

> 第六阶段是分层自动复核。系统会检查候选是否有 source、external_url、raw 原文和 evidence_excerpt，再按诊断、监管、药品、休药期等风险分层。低风险来源候选可以自动进入可用候选队列，历史欠账会自动进入补抓取或补元数据队列，高风险正式事实仍需确认。可以看到 `fact_count` 没有被 LLM 直接增加，这说明系统不是让模型直接写事实，而是把真实性控制在候选复核之后。

## 阶段 7：query 构建 LLM 检索上下文

### 从哪里开始

执行一次检索：

```powershell
python -m chicken_data_synthesis.wiki_cli --json query "新城疫 诊断 实验室确诊" --top-k 5
```

这条命令模拟生成/评估流程在需要知识时如何向 LLM Wiki 要上下文。`--top-k 5` 表示最多返回 5 个相关命中，现场可以解释为“不是把整个知识库塞给模型，而是按问题检索最相关证据”。

### 这一步做什么

`query` 会从当前 Wiki 中检索相关页面、来源、候选证据和正式事实，构建给生成/评估 LLM 使用的上下文。

它不是让 LLM 直接凭空回答，而是先从 LLM Wiki 中拿证据。这个证据来自正式 facts、source 页面、候选层中已经登记的来源数据，以及关联的证据状态：

```text
用户问题或病例主题
  -> query_wiki()
  -> build_llm_wiki_context()
  -> 返回 source/fact/page/candidate 相关上下文
  -> 生成或评估流程引用这些上下文
```

### 为什么要这么做

生成病例和评估诊断时，模型不能只依赖自身参数记忆。query 阶段把当前知识库中可追溯的事实、来源、证据摘要和页面组织成上下文，降低幻觉风险。

这里要强调：第二到第六阶段维护进来的数据，会在第七阶段变成 LLM 可使用的检索上下文。也就是说，raw/source/candidates 不是孤立文件，它们最终服务于生成和评估。

### 执行结果怎么看

重点看 query 返回，并解释每个字段如何服务生成/评估：

```text
query
含义：本次检索问题。
作用：用于审计“当时模型到底按什么问题检索知识”。

hits
含义：命中的页面、事实或来源摘要。
作用：展示系统为什么认为这些内容和当前问题相关。

context
含义：组装后的 LLM 上下文文本。
作用：生成/评估模型真正会读取的是这个上下文，而不是直接读取整个 Wiki。

source_ids
含义：本次上下文涉及的来源 ID。
作用：如果后续结果有争议，可以通过 source_ids 追溯到 wiki/sources/SRC-xxxx.md，再从 source 页追到 raw 原文和外部权威 URL。

top_k
含义：最多返回多少个相关命中。
作用：控制上下文规模，避免无关信息过多影响生成和评估。

context_chars
含义：上下文字符数。
作用：用于判断上下文是否过长或过短，也会进入审计字段。
```

如果新增 source 后重建了图谱和索引，相关来源会更容易进入检索上下文。

现场要注意：query 命中不等于正式采用事实。query 只是构建上下文，最终生成/评估还要结合质量门控和审计字段。这样可以避免“检索到了”被误解成“已经证明了”。

### 代码依据

CLI：

```text
src/chicken_data_synthesis/interfaces/cli/wiki.py
args.command == "query"
```

检索载荷：

```text
src/chicken_data_synthesis/infrastructure/knowledge/operations.py
query_wiki()
```

上下文构建：

```text
src/chicken_data_synthesis/infrastructure/knowledge/wiki.py
build_llm_wiki_context()
```

### 汇报话术

> 第七阶段是检索上下文。LLM Wiki 的作用不是只生成 HTML 图谱，也不是只保存 URL，而是给生成和评估流程提供可追溯上下文。query 命令会把知识库中的正式事实、来源页、候选证据和证据状态组织成 LLM 可使用的 evidence context。

## 阶段 8：graph-build 重建 graph-data.json 与 knowledge-graph.html

### 从哪里开始

执行图谱重建：

```powershell
python -m chicken_data_synthesis.wiki_cli --json graph-build
```

打开 HTML：

```text
knowledge/llm_wiki_chicken_authoritative/wiki/knowledge-graph.html
```

查看图谱数据：

```text
knowledge/llm_wiki_chicken_authoritative/wiki/graph-data.json
```

### 这一步做什么

图谱重建会扫描当前 Wiki，生成：

```text
wiki/graph-data.json
wiki/knowledge-graph.html
wiki/knowledge-graph.md
```

图谱里展示的节点包括：

```text
Disease: 疾病
Drug: 药品
Standard: 标准
Rule: 规则
Source: 来源
Concept: 概念
Candidate: 候选事实
```

第二到第六阶段维护进来的数据，在图谱里通常会体现为：

```text
新增 Source 节点：说明新的权威来源页进入 wiki/sources。
新增 Candidate 节点：说明新的候选事实进入 candidates。
新增 Source-Candidate 连线：说明候选事实能追溯到来源。
新增 Candidate-Concept/Disease/Rule 连线：说明候选事实和疾病、规则、概念产生关联。
节点和连线数量变化：说明 HTML 图谱跟随知识库数据重建，而不是固定静态页面。
```

### 为什么要这么做

图谱是给现场演示和知识库治理看的。它可以直观看到：

```text
新增来源是否进入 Wiki
候选事实是否进入图谱
疾病、药品、规则、来源之间是否有联系
HTML 页面是否跟随知识库变化
```

### 执行结果怎么看

本次真实重建结果：

```text
node_count: 1438
link_count: 3593
generated_at: 2026-05-05T18:44:14
```

后来执行真实 fetch 并重建后：

```text
node_count: 1412
link_count: 3563
```

现场讲解时不需要死背具体数字，重点讲变化逻辑：

```text
新增 source 或 candidate
  -> graph-data.json 节点和边发生变化
  -> knowledge-graph.html 刷新后展示新节点
```

现在 `daily-maintain` 会同时返回 `graph_change_report`。这个字段用于对比维护前后的可视化变化：

```text
before_node_count / after_node_count
含义：维护前后图谱节点数量。
说明：如果新增 source 或 candidate，after 通常会增加；如果删除 source 或候选事实，after 可能减少。

before_link_count / after_link_count
含义：维护前后图谱连线数量。
说明：新增候选事实、证据来源关系、事实关系会让连线增加；删除 source/fact/candidate 会让连线减少。

added_nodes
含义：本轮新增节点样例，包含 id 和 label。
说明：用于现场指出“本轮新增了哪些 source、candidate、concept”。

removed_nodes
含义：本轮删除节点样例。
说明：如果执行 delete-source 或删除候选/事实后重建图谱，这里能看到受影响节点。

added_links / removed_links
含义：本轮新增或删除的关系边样例。
说明：用于解释新增来源与候选事实、候选事实与概念、事实与来源之间的关系变化。

reason
含义：图谱变化原因。
固定为 graph_rebuilt_from_current_wiki_files_after_maintenance，说明图谱是由当前 Wiki 文件重建得到。

evidence
含义：图谱变化证据文件。
固定指向 wiki/graph-data.json 和 wiki/knowledge-graph.html。
```

现场讲图谱变化时，不要只说“HTML 更新了”，要按下面三句话讲：

```text
第一，变化来源于底层 Wiki 文件新增、修改或删除，不是手工改 HTML。
第二，graph_change_report 记录了节点和边的前后差异。
第三，最终证据文件是 graph-data.json 和 knowledge-graph.html，可以现场打开验证。
```

如果现场有人问“为什么 HTML 页面能说明 LLM Wiki 有效”，回答：

```text
因为 HTML 读取的是 graph-data.json。
graph-data.json 是 graph-build 根据当前 Wiki 文件重新生成的。
当 raw/source/candidates/facts 发生新增、修改、删除后，graph-build 会重新扫描这些文件。
所以 HTML 展示的是当前知识库状态，而不是手工画出来的示意图。
```

### 为什么很多 Disease 不直接连接 Drug

这是图谱设计问题，不是单纯的数据缺失。系统没有把疾病和药品强行直连，而是通过更安全的中间结构表达：

```text
Disease
  -> Rule / Standard / Source / Concept
  -> Drug 或 drug_rule
```

原因是鸡病治疗和兽药使用存在禁用药、适应证、休药期、蛋鸡限制等监管约束。直接画成“疾病 -> 药品”容易被误解为推荐用药。

### 代码依据

图谱构建：

```text
src/chicken_data_synthesis/infrastructure/knowledge/graph.py
rebuild_graph()
```

CLI：

```text
src/chicken_data_synthesis/interfaces/cli/wiki.py
args.command == "graph-build"
```

HTML 输出：

```text
knowledge/llm_wiki_chicken_authoritative/wiki/knowledge-graph.html
```

### 汇报话术

> 第八阶段是图谱重建。每次新增、修改、删除来源、raw 数据或候选事实后，都可以重建 graph-data.json 和 HTML。HTML 不是静态展示图，而是当前 Wiki 数据状态的可视化投影。新增权威数据页、抓取原文、生成候选、复核分层之后，图谱中的 source、candidate、concept 及其连线都会跟随变化。

## 阶段 9：生成/评估流程记录 Wiki 审计字段

### 从哪里开始

查看 schema 中要求的审计字段：

```powershell
Select-String -Path knowledge\schemas\llm_wiki_schema.yaml -Pattern "output_csv_fields" -Context 0,20
```

运行测试确认最终 CSV 包含审计字段：

```powershell
python -m pytest -q tests\test_llm_wiki_knowledge.py
```

### 这一步做什么

生成和评估流程最终会记录 Wiki 审计字段，例如：

```text
wiki_dir
wiki_fact_count
wiki_page_count
wiki_context_query
wiki_evidence_status_counts
wiki_evidence_source_ids
wiki_context_chars
```

这些字段用于回答：

```text
这次生成/评估用了哪个 Wiki？
当时有多少事实？
引用了哪些来源？
上下文长度是多少？
证据状态是什么？
```

### 为什么要这么做

如果评估结果有争议，不能只看模型输出，还要能追溯当时引用了哪些知识、哪些来源、证据状态是什么、上下文来自哪个 Wiki。审计字段就是把知识库状态和生成/评估结果绑定起来。

这一步把前八个阶段形成闭环：

```text
阶段 1 的需求决定维护主题。
阶段 2-4 把权威数据抓进 raw 和 sources。
阶段 5-6 把数据变成候选并完成分层复核。
阶段 7 把可追溯数据取出来给 LLM 使用。
阶段 8 把当前知识状态展示到 HTML 图谱。
阶段 9 把使用过的 Wiki 状态写入生成/评估结果。
```

### 代码依据

CSV 行构建：

```text
src/chicken_data_synthesis/infrastructure/persistence/csv_artifacts.py
build_final_result_row()
```

质量门控：

```text
src/chicken_data_synthesis/application/services.py
apply_final_quality_gates()
```

测试依据：

```text
tests/test_llm_wiki_knowledge.py
test_final_csv_contains_wiki_audit_fields()
```

schema 依据：

```text
knowledge/schemas/llm_wiki_schema.yaml
audit.output_csv_fields
```

### 汇报话术

> 第九阶段是审计闭环。LLM Wiki 不只是前端图谱，也不是单独知识库，它会把生成/评估使用到的 Wiki 状态、来源 ID、证据状态和上下文长度写入最终结果。这样 leader 如果问某条病例或评估依据来自哪里，我们可以追溯到 query 上下文、候选事实、source 页面、raw 原文和外部权威 URL。

## 完整现场演示顺序

按下面顺序演示即可：

```powershell
cd D:\XF-ChongQin\ai-
$env:PYTHONPATH="src;."
$env:NONELINEAR_API_KEY=[Environment]::GetEnvironmentVariable("NONELINEAR_API_KEY","User")

python -m chicken_data_synthesis.wiki_cli --json status

python -m chicken_data_synthesis.wiki_cli --json daily-maintain `
  --base-url "https://api.nonelinear.com/v1" `
  --model "gpt-5.4-mini-medium"

# daily-maintain 已经自动执行 review-candidates。
# 如需现场单独展示第六阶段，可以再执行一次：
python -m chicken_data_synthesis.wiki_cli --json review-candidates

python -m chicken_data_synthesis.wiki_cli --json authority-discover `
  "真实 fetch 测试：新城疫 WOAH 权威页面" `
  --url "https://www.woah.org/en/disease/newcastle-disease/" `
  --fetch `
  --timeout 60

python -m chicken_data_synthesis.wiki_cli --json query "新城疫 诊断 实验室确诊" --top-k 5

python -m chicken_data_synthesis.wiki_cli --json graph-build

python -m chicken_data_synthesis.wiki_cli --json schema-check
python -m chicken_data_synthesis.wiki_cli --json lint
python -m pytest -q
```

如果需要现场单独演示删除、修改、新增都有明确审计依据，按下面补充演示：

```powershell
# 1. 新增：手动登记一个 raw 来源时必须写明原因和依据。
python -m chicken_data_synthesis.wiki_cli --json source-create `
  "knowledge\llm_wiki_chicken_authoritative\raw\html\coccidiosis-in-poultry.html" `
  --title "Manual audited source demo" `
  --reason "manual_authority_review" `
  --evidence "review-ticket:AUTH-DEMO-001"

# 2. 修改：候选复核写回会生成 review_report，并写 candidate-review 日志。
python -m chicken_data_synthesis.wiki_cli --json review-candidates

# 3. 删除预演：先 dry-run，看会影响哪些 raw/source 和 references。
python -m chicken_data_synthesis.wiki_cli --json delete-source `
  --source-page "wiki/sources/SRC-xxxx-demo.md"

# 4. 删除执行：真正删除必须给出 reason；建议同时给 evidence 和 replacement-source。
python -m chicken_data_synthesis.wiki_cli --json delete-source `
  --source-page "wiki/sources/SRC-xxxx-demo.md" `
  --raw-file "raw/html/xxxx-demo.html" `
  --reason "source_replaced_by_more_specific_page" `
  --evidence "review:旧来源未提供可抽取证据，已由更具体权威页面替代" `
  --replacement-source "wiki/sources/SRC-yyyy-replacement.md" `
  --apply

# 5. 删除或修改后重建图谱，观察 graph_change_report 或 graph-diff 日志。
python -m chicken_data_synthesis.wiki_cli --json graph-build
```

注意：现场不要随便删除真实权威来源。删除演示应使用演示 source，或先执行 dry-run。专业知识库里，删除必须有明确原因、证据和替代链路；没有 reason 的 `--apply` 会被代码拒绝。

## 完整汇报结论

可以直接按下面这段总结：

> 本项目中的 LLM Wiki 已经不是静态文档，而是一套受控的知识库自动维护链路。系统不是固定维护鸡新城疫，而是先调用 `build_maintenance_queries()` 扫描当前 Wiki 的疾病页、药品页、规则页和候选欠账，动态生成本轮维护需求；然后调用 Nonelinear 的 `gpt-5.4-mini-medium` 发现候选权威数据页，但 LLM 只允许输出候选页面 URL、标题、理由和证据角色，不能直接写正式事实。候选数据页会经过 schema 中的权威域名白名单校验、跨库去重、默认 fetch、raw 原文保存、证据摘要抽取和相关性过滤，通过后进入 raw、wiki/sources 和 candidates 候选层。第六阶段已经实现分层自动复核：程序先做 source/raw/URL/excerpt 硬校验，规则再识别诊断、监管、兽药、休药期等高风险项，低风险进入 `AUTO_READY_SOURCE`，高风险进入 `HUMAN_REQUIRED`，历史欠账进入 `LEGACY_NEEDS_FETCH` 或 `LEGACY_NEEDS_METADATA`，不合格才进入 `REJECTED`。正式 facts 不会被 LLM 无约束改写，只有复核通过的事实才能进入 `knowledge_facts.json`。随后系统通过 query 构建生成/评估所需的检索上下文，通过 graph-build 重建 `graph-data.json` 和 `knowledge-graph.html`，最终在生成/评估结果中记录 Wiki 审计字段。这样既提高了自动化程度，又保证了全库覆盖、来源权威、原始数据可查、事实隔离、风险分层和过程可追溯。

## 当前结果的讲解重点

当 leader 看到类似结果时：

```text
query_count: 8
maintenance_queries: [...]
accepted_count: 15
rejected_count: 0
fact_count: 1748
schema_ok: true
lint_ok: true
graph_data_exists: true
graph_html_exists: true
```

解释如下：

```text
query_count
表示本轮执行了多少个真实维护主题。旧版本常见是 3；现在默认由动态扫描决定，通常最多 8 个，具体以返回的 query_count 为准。

maintenance_queries=[...]
表示本轮实际维护的问题清单。现场重点看这里是否覆盖多个疾病、药品、规则和候选欠账。它是证明系统面向整个鸡病知识库自动维护的核心字段。

accepted_count=15
表示 LLM 输出的 15 个候选数据页通过了权威准入链路。现场要补充：accepted 不等于正式事实被采用，它表示来源和数据可以进入候选层。

rejected_count=0
表示本轮没有白名单外 URL。

fact_count=1748
表示正式事实库没有被 LLM 直接改写，这是安全设计。

schema_ok=true
表示 Wiki 目录结构、白名单策略、候选层约束、审计字段都符合 schema。

lint_ok=true
表示 Wiki 内部链接、索引、证据状态没有破坏。

graph_data_exists=true / graph_html_exists=true
表示图谱数据和 HTML 页面已经跟随维护结果重建。
```

也要主动说明当前优化方向：

```text
1. 当前已经增强 URL 幂等去重，已有 source/raw URL 不会重复落库。
2. 当前已经提高具体页面优先级，优先寻找公告、标准详情页、疾病手册页和 PDF，减少只返回官网首页。
3. 当前 daily-maintain 已经默认 fetch，让权威页面正文进入 raw/html 或 raw/pdfs；如果只想记录 URL，才使用 --no-fetch。
4. 当前已经增加 fetch 后 evidence_excerpt 抽取和相关性校验，保证进入流程的是权威数据，而不只是权威域名。
5. 候选事实会自动执行 review-candidates 分层复核，但高风险正式事实仍需确认，保证不虚构、不误读、不越权。
```

## 最终一句话

> LLM Wiki 的核心价值不是让 LLM 自动编知识，而是让 LLM 自动发现权威数据页，让系统抓取真实原文、抽取证据、校验来源、生成候选、分层复核，并用 schema、白名单、候选层、图谱和审计字段把知识维护过程管住、留痕、可复核。
