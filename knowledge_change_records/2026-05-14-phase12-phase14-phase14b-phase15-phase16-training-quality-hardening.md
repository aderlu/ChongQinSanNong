# 2026-05-14 训练数据质量强化记录

## 本次目标

针对猪病 LLM Wiki 数据生成与评估链路中已经暴露出的两类核心质量问题，执行可落地的工程修复：

1. 少量 accepted 样本呈现出类似字典、键值对、伪 JSON、英文标签模板的痕迹，不适合作为高质量问诊训练数据。
2. 一部分低风险正样本过于保守，答案信息密度不足，更像边界拒答而不是高质量临床问诊回答。

本次修改同时要求：

- 全程使用 UTF-8，避免乱码。
- 每次变更必须留痕，便于汇报。
- 修改后要把代码、输出和队列关系整理得更清晰，符合企业级工程结构。

## 修改前存在的问题

### 1. Phase12 入口筛选过宽

修改前，样本规划阶段对页面证据厚度、页面是否 gold-ready、证据单元数量的利用不足，导致部分 `TOC-only` 或 `thin evidence` 页面仍可能流入正向 SFT 轨道。

这会在下游造成两个问题：

- 即使生成正确，也容易形成训练价值不高的“证据稀薄回答”。
- 低质量页面进入真实生成后，会放大模型输出保守化和模板化的倾向。

### 2. Phase14 生成提示词仍允许“结构化回答腔”

修改前，`Phase14` 虽然要求中文和 grounded answer，但对于以下不自然输出缺乏足够强的显式约束：

- 英文标签分节
- 结构化对象转字符串
- 字典式 `key: value`
- 像任务说明或提示词回显的回答

因此真实 API 在部分样本中会产出“形式上符合要求、训练上不自然”的文本。

### 3. 缺少生成后自然化修复层

修改前，如果 `Phase14` 真实生成产出了半结构化文本，下游评估只能做接收或拒绝，缺少一个“先把明显格式问题自然化再继续评估”的缓冲层。

### 4. Phase15 只重事实，不重训练语料风格质量

修改前，`Phase15` 重点检查：

- 字段结构
- 证据锚点
- 事实链路
- 高风险 hard gate

但对“是否像训练语料”缺少硬门槛，因此某些“事实正确但形式不自然”的样本会漏进 accepted。

### 5. Phase16 训练集分层不够细

修改前，导出主要按能力层和 review/reject 进行拆分，不能很好地区分：

- 高价值正向 SFT
- 边界/拒绝训练集
- 需要格式修复的样本
- 勉强可用但不够优质的 borderline 样本

结果是训练集用途不够清晰，后续数据运营成本高。

## 本次修改的代码与整理动作

### 一、样本规划入口收紧

修改文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase12_plan_samples_from_wiki.py`

新增/强化内容：

- 引入 `training_intent`
- 引入 `evidence_depth_class`
- 引入 `page_gold_ready`
- 引入 `evidence_units`
- 增加 `toc_only / thin / substantive` 证据深度分类
- 禁止低证据深度页面进入 `positive_sft`

解决效果：

- 正样本从入口开始就更偏向 substantive 页面。
- 低价值页面更多被路由到缺口/边界类轨道，而不是主 SFT 轨道。

### 二、Phase14 中文临床表达强化

修改文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14_real_api_generate_30.py`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14_generate_two_stage_samples.py`

更新内容：

- 明确要求输出必须像真实猪场兽医中文问诊交流。
- 禁止字典、键值对、伪 JSON、英文标签分节、对象转字符串式回答。
- 对低风险正样本强调“高训练价值的信息密度”，不能只剩空泛保守表述。
- 将 `answer_structure_for()` 的节标题从英文改为中文。
- 将 `structure_requirements_for()` 改成中文要求。
- Stage1/Stage2 system prompt 与 user prompt 全部强化为中文临床表达约束。
- 兼容中文全角冒号 `：` 的结构识别。

解决效果：

- 从生成源头压制英文模板输出。
- 提升正样本回答的“真实问诊感”和可训练性。

### 三、新增生成后自然化层

新增文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14b_naturalize_grounded_answers.py`

新增能力：

- 检测 dict-like 输出
- 检测英文模板标签
- 对半结构化回答进行自然化重写
- 生成 `style_flags`
- 生成 `style_rewrites`
- 计算 `clinical_conversation_score`

解决效果：

- 真实 API 的非理想输出不再只能“硬拒绝”。
- 给下游评估提供风格质量信号和修复痕迹。

### 四、Phase15 新增风格质量硬门槛

修改文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase15_fact_level_evaluate_samples.py`

新增内容：

- `DICT_LIKE_OUTPUT_RE`
- `ENGLISH_TEMPLATE_LABEL_RE`
- `style_quality_check(sample)`
- 在 `hard_gate_check()` 中并入 style violations
- 在 `judge_check()` 中把 style pass 纳入 accepted 必要条件

新增拦截项包括：

- `dict_like_output`
- `english_template_label_output`
- `clinical_conversation_score_too_low`
- `information_density_too_low`
- `boundary_dominates_low_risk_answer`
- `answer_too_short_for_training`

解决效果：

- “事实对但不适合训练”的样本会被挡在主训练集之外。
- 低风险样本如果只剩边界拒答，会被识别为信息密度不足。

### 五、Phase16 训练集分层导出细化

修改文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase16_export_layered_training_sets.py`

新增导出桶：

- `L1_L4_high_value`
- `L1_L4_borderline`
- `boundary_refusal_train`
- `format_repair_queue`

新增 metadata：

- `training_intent`
- `evidence_depth_class`
- `page_gold_ready`
- `evidence_units`
- `style_flags`
- `style_rewrites`

新增路由逻辑：

- 高风格质量 + substantive + positive_sft 的样本优先进入高价值桶
- 风格存在问题的样本进入 `format_repair_queue`
- 高风险边界型样本可进入 `boundary_refusal_train`
- 其余可接受正样本进入 `L1_L4_borderline`

解决效果：

- 训练集、边界集、修复集、校准集的职责分开。
- 便于后续做增量运营、人工修复和定向再训练。

## 过程中发现并修复的附加问题

### Phase14b 状态传递错误

初版 `Phase14b` 在完成自然化重写后，`style_flags` 仍然按照“改写前原答案”打标，导致：

- 已被修复的样本仍被 `Phase15` 当成脏样本拒绝
- `Phase16` 误把这些样本继续送进修复队列

后续已在同日继续修复：

- `dict_like_detected`
- `english_label_detected`

改为按“改写后的答案”重新计算。

同时增强了英文模板标签的正则替换覆盖，兼容 `Control - boundary evidence:` 这一类带空格和连字符变体。

## 回归验证结果

### 第一轮回归

批次：

- `20260514_quality_harden_smoke`

结果：

- `Phase14b` 重写 12 条
- `Phase15` accepted 15，rejected 13
- 问题暴露：已自然化样本仍因旧标记被误拒

### 第二轮回归

批次：

- `20260514_quality_harden_smoke_v2`

输入基线：

- 使用真实 30 条批次中的 28 条真实生成样本
- 复用已有 `Phase18` 语义评审结果

结果：

- `Phase14b` 重写 12 条
- `Phase15` accepted 21，rejected 7
- `Phase16` 最终 accepted 20，review 1，rejected 7
- `format_repair_queue` 缩减到 5 条
- `L1_L4_borderline` 形成 20 条可用样本

说明：

- “已修复成功的结构化回答”已能重新回到可用训练轨道。
- 剩余 5 条风格问题样本被正确隔离到修复队列。
- 2 条高风险样本因 `A0/rule card` 约束不足被继续拦截，符合治理要求。

## 防乱码措施

本次修改与验证过程中统一采用以下约束：

- PowerShell 执行前设置 `chcp 65001`
- 设置 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
- 设置 `$OutputEncoding = [System.Text.Encoding]::UTF8`
- 设置 `$env:PYTHONIOENCODING='utf-8'`
- Python 文件读写统一使用 `encoding='utf-8'`
- JSONL 输出统一使用 `newline="\\n"`

额外经验：

- Windows 下内联 Python 偶发出现 `U+FEFF` 注入，说明 BOM 风险真实存在。
- 这也是后续必须继续坚持 UTF-8 无 BOM 和统一 I/O 编码策略的原因。

## 预计产生的效果

1. 主训练集中的“对象串化”“英文模板标签化”样本会显著减少。
2. 低风险正样本的信息密度和问诊训练价值会提升。
3. 高风险边界样本与正向 SFT 样本会被更清晰地拆分。
4. 修复队列会更聚焦，便于后续人工或自动再加工。
5. 整条链路从入口规划、真实生成、自然化修复、事实门控、双裁判后导出，都更接近企业级可运营状态。
