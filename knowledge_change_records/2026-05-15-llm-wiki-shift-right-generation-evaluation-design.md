# 2026-05-15 猪病生成与评估系统 Wiki 后移方案思路文档

## 一、背景

当前猪病数据生成系统采用的是 `wiki-first` 架构：

```text
Wiki 页面
-> Phase12 plan
-> Phase13 answer skeleton
-> Phase14 grounded generation
-> Phase15 fact / hard gate
-> Phase18 dual judge
-> Phase16 export
```

这个架构的优点是事实可追溯、边界可控、证据字段完整。但经过多轮数据审查后，暴露出一个关键问题：

**Wiki 过早参与生成，会把 LLM 的回答压成“知识库约束下的安全问答”，而不是一线临床兽医式回答。**

表现包括：

- 用户问题容易被知识库任务牵引，不够像真实养殖户。
- 回答偏“不能确诊、建议补信息、送检、联系兽医”。
- 诊疗和处方内容不够直接，缺少临床处置、支持治疗、处方化治疗框架。
- 为了满足证据锚点，回答会保守、宽泛、模板化。
- 评估得分可能高，但训练价值不一定高。

因此，建议将 Wiki 从“生成前约束”改为“生成后校验、补强和准入判断”。

## 二、核心思路

新架构不再让 Wiki 直接约束 LLM 生成问题、诊疗和处方内容。

改为：

```text
病例任务 / 疾病主题 / 场景变量
-> LLM 生成真实养殖户问题
-> LLM 生成临床式诊疗和处方化回答
-> Wiki 后置检索
-> Wiki 事实校验
-> Wiki 安全边界校验
-> Wiki 支撑度评分
-> 必要时 LLM 基于 Wiki 进行修订
-> 裁判评估
-> 训练准入 / 修复队列 / 拒绝队列
```

也可以理解为：

```text
先让 LLM 像兽医一样回答
再让 Wiki 像审稿人一样审核
```

这和原来的区别是：

```text
原方案：Wiki 先规定 LLM 能说什么
新方案：LLM 先给出自然临床回答，Wiki 再判断哪些能保留、哪些要修正、哪些要拒绝
```

## 三、为什么要后移 Wiki

### 3.1 生成质量由 LLM 的临床表达能力主导

真实问诊数据的核心价值是：

- 用户问题像真实养殖户。
- 回答像真实临床兽医。
- 能直接给出处置方案。
- 能给出处方化治疗框架。
- 能体现经验判断、风险排序、禁忌和升级条件。

这些内容不适合由 Wiki 条目直接拼接出来。

Wiki 更适合提供事实边界，不适合直接决定表达形态。

### 3.2 避免“证据锚点牵引回答”

当前 Wiki 前置后，模型经常为了不越界而写成：

- “目前不能确诊”
- “建议补充检测”
- “请现场兽医评估”
- “不能直接给药”

这些话本身是安全的，但如果每条回答都这样，训练数据会变成保守客服式回答，而不是临床诊疗式回答。

后移 Wiki 后，LLM 可以先完整回答：

- 先判断严重程度。
- 给出可能方向。
- 给出现场处置。
- 给出支持治疗。
- 给出用药类别。
- 给出禁忌。
- 给出升级条件。

再由 Wiki 判断其中哪些事实、药物、边界需要修正。

### 3.3 更适合处方化数据生成

处方和治疗建议天然需要：

- 病情假设。
- 临床分层。
- 猪群阶段。
- 体重/日龄。
- 给药途径。
- 禁忌。
- 标签说明。
- 休药期。
- 现场兽医确认。

这些内容单靠疾病 Wiki 很难在生成阶段完整约束。

更合理的方式是：

1. LLM 先生成一个临床处置方案。
2. Wiki / 药品知识 / 规则卡后置检查：
   - 药物是否适用猪。
   - 是否涉及禁药。
   - 是否超适应症。
   - 是否缺少休药期边界。
   - 是否编造剂量。
   - 是否把疑似病说成确诊。
3. 根据检查结果打标签或要求修订。

## 四、修改后的 LLM Wiki 应该起什么作用

Wiki 后移后，不再是“生成器的手铐”，而是“质量控制和知识增强层”。

具体作用如下。

### 4.1 事实核验器

Wiki 用来检查回答中的医学事实是否成立。

例如：

- 某疾病是否会导致腹泻。
- 某疾病是否常见于哺乳仔猪。
- 某疾病是否可能表现为神经症状。
- 某病是否应列入鉴别方向。
- 某症状组合是否与疾病特征相符。

作用：

- 降低医学幻觉。
- 防止 LLM 编造疾病表现。
- 防止把不相关疾病硬拉进鉴别诊断。

### 4.2 安全边界审稿人

Wiki 和规则卡共同检查高风险内容：

- 是否线上确诊。
- 是否直接下扑杀、封锁、调运、上报结论。
- 是否给出无依据精确剂量。
- 是否忽略重大传染病风险。
- 是否建议危险混药。
- 是否缺少休药期提醒。

作用：

- 保证临床回答有帮助但不越界。
- 保证处方化回答不变成危险处方。

### 4.3 证据覆盖评分器

每条回答生成后，系统从回答中抽取 claim，再到 Wiki 中检索证据。

可将 claim 分为：

- 已支撑事实。
- 部分支撑事实。
- 未支撑但低风险常识。
- 未支撑且高风险。
- 与 Wiki 冲突。

作用：

- 从“有没有证据锚点”升级为“回答内容被证据支撑到什么程度”。
- 不再要求每句话生成时都带锚点，而是在生成后评估支撑度。

### 4.4 回答修订器

当回答存在问题时，Wiki 后移系统可以触发修订：

```text
原始回答
-> claim 抽取
-> Wiki 检索
-> 冲突 / 缺证据 / 越界识别
-> LLM revise
-> 再评估
```

修订方式：

- 删除无依据确诊。
- 把“确定是某病”改成“需要优先怀疑某病”。
- 把精确剂量改成“按产品标签、体重和兽医医嘱执行”。
- 补充重大疫病风险边界。
- 补充休药期提醒。
- 补充检测或上报边界。

作用：

- 保留 LLM 原始回答的自然临床表达。
- 只修正事实和安全问题，而不是把整条回答重写成模板。

### 4.5 训练准入裁判

Wiki 后移后，最终导出不再只看生成阶段是否带证据，而是看后置评估结果。

建议训练准入分层：

- `gold_clinical`: 临床表达好，事实支撑好，安全边界好。
- `silver_revised`: 原始回答有小问题，经 Wiki 修订后可用。
- `repair_queue`: 临床表达好，但存在未支撑事实或边界缺失，需要人工/模型修复。
- `reject`: 重大医学错误、危险用药、伪造检测、线上确诊。

作用：

- 训练集质量更贴近实际用途。
- 不因为缺少生成时锚点就直接拒绝好样本。

### 4.6 对比实验基准

Wiki 后移后，Wiki 的价值可以更公平地衡量。

新的对比问题不是：

```text
有没有 Wiki 约束生成？
```

而是：

```text
LLM 原始回答经过 Wiki 后置校验/修订后，质量提升多少？
```

可比较：

- 原始 LLM 回答。
- Wiki 校验后未修订版本。
- Wiki 修订后版本。
- 人工 gold 对照。

作用：

- 更准确衡量 Wiki 对事实正确性、安全边界和训练准入的贡献。

## 五、新系统建议链路

### Phase A：任务与场景生成

输入：

- 疾病主题或疾病 ID。
- 猪群阶段。
- 场景变量。
- 用户画像。
- 训练目标。

输出：

- `case_seed`
- `user_query`

注意：

- 这里可以使用疾病名/主题，但不使用 Wiki facts 约束问题生成。
- 用户问题要像真实养殖户，不出现“实验室检测、剖检、发病比例”等专业化模板。

### Phase B：LLM 原始临床回答

LLM 生成：

- 临床判断。
- 严重程度。
- 鉴别方向。
- 现场处置。
- 处方化治疗框架。
- 禁忌。
- 升级条件。
- 少量必要追问。

输出：

- `raw_user_query`
- `raw_assistant_answer`
- `generation_model`
- `generation_prompt_version`

### Phase C：Claim 抽取

从回答中抽取 claim：

- 疾病表现 claim。
- 鉴别诊断 claim。
- 防控 claim。
- 治疗 claim。
- 药物/处方 claim。
- 监管/上报 claim。

输出：

```json
{
  "claim_id": "...",
  "claim_text": "...",
  "claim_type": "symptom|diagnosis|differential|treatment|drug|regulatory",
  "risk_level": "low|medium|high",
  "needs_evidence": true
}
```

### Phase D：Wiki / 药品 / 规则检索

根据 claim 检索：

- 疾病 Wiki。
- 药品知识库。
- 规则卡。
- 禁药/休药期/监管边界。

输出：

- `retrieved_evidence`
- `evidence_anchors`
- `source_trust`
- `evidence_coverage`

### Phase E：事实与边界评估

对每个 claim 给出判断：

- `supported`
- `partially_supported`
- `unsupported_low_risk`
- `unsupported_high_risk`
- `contradicted`
- `unsafe`

输出：

- `wiki_fact_score`
- `wiki_safety_score`
- `unsupported_claims`
- `contradicted_claims`
- `unsafe_claims`

### Phase F：必要时修订

触发条件：

- 高风险 unsupported。
- contradicted。
- unsafe。
- 伪造检测/剖检。
- 精确剂量无依据。
- 线上确诊。

修订要求：

- 尽量保留原回答自然表达。
- 只修事实、边界和危险建议。
- 不把回答重写成知识库摘要。

输出：

- `revised_assistant_answer`
- `revision_reasons`
- `removed_claims`
- `downgraded_claims`
- `added_safety_boundaries`

### Phase G：最终评估与导出

评估维度：

- 场景真实度。
- 临床直接性。
- 处方化完整性。
- 医学正确性。
- Wiki 支撑度。
- 安全边界。
- 表达自然度。

导出字段建议保留：

- `raw_assistant_answer`
- `revised_assistant_answer`
- `final_assistant_answer`
- `wiki_evidence_coverage`
- `wiki_fact_score`
- `wiki_safety_score`
- `revision_needed`
- `revision_type`
- `unsupported_claim_count`
- `unsafe_claim_count`
- `final_export_decision`

## 六、修改后 Wiki 能提升什么

### 6.1 提升事实正确性

LLM 先生成可能会有幻觉，Wiki 后置可以发现：

- 疾病症状不匹配。
- 鉴别方向不合理。
- 把少见表现写成典型表现。
- 把不相关疾病纳入主要怀疑。

提升点：

- 医学正确性。
- 鉴别诊断可靠性。
- 疾病知识一致性。

### 6.2 提升安全边界

Wiki + 规则卡可以拦截：

- 危险处方。
- 无依据精确剂量。
- 错误休药期。
- 监管越界。
- 线上确诊。
- 忽视重大疫病。

提升点：

- 处方安全。
- 合规性。
- 高风险样本拒绝能力。

### 6.3 提升训练数据可用性

相比 Wiki 前置，新方案可以保留更自然、更像真实临床的回答。

Wiki 只修问题，不压制表达。

提升点：

- 回答自然度。
- 临床可操作性。
- 训练模型的实用性。
- 减少“客服式拒答”。

### 6.4 提升评估解释性

每条回答可以解释：

- 哪些 claim 被支持。
- 哪些 claim 未支撑。
- 哪些 claim 被修订。
- 为什么拒绝。

提升点：

- 审查透明度。
- 汇报可解释性。
- 后续人工修复效率。

### 6.5 提升实验公平性

原来 Wiki 组天然有结构优势，no-wiki 组天然缺证据字段。

后移后，可以比较：

- LLM 原始回答质量。
- Wiki 审核带来的增益。
- Wiki 修订带来的增益。

提升点：

- 更公平评估 Wiki 价值。
- 更容易判断问题来自 LLM、Wiki、prompt 还是裁判。

## 七、建议的新字段

在原 54 字段之外，建议新增一组后置 Wiki 字段。

### 原始与修订字段

- `raw_user_query`
- `raw_assistant_answer`
- `revised_assistant_answer`
- `final_assistant_answer`
- `revision_needed`
- `revision_type`
- `revision_reason`

### Wiki 后置证据字段

- `wiki_retrieval_query`
- `wiki_retrieved_entity_ids`
- `wiki_evidence_anchor_count`
- `wiki_evidence_coverage`
- `wiki_source_trust`

### Claim 级评估字段

- `claim_count`
- `supported_claim_count`
- `partially_supported_claim_count`
- `unsupported_low_risk_claim_count`
- `unsupported_high_risk_claim_count`
- `contradicted_claim_count`
- `unsafe_claim_count`

### 分数与准入字段

- `wiki_fact_score`
- `wiki_safety_score`
- `clinical_directness_score`
- `prescription_actionability_score`
- `final_export_decision`
- `final_training_use_tag`

## 八、阶段性实施建议

### 第一步：保留旧链路，新增后置 Wiki 实验链路

不要立刻删除 `wiki-first`。

新增：

```text
llm_first_generation
-> claim_extraction
-> wiki_retrieval
-> wiki_posthoc_evaluation
-> wiki_revision
-> final_compare
```

这样可以与旧链路并行比较。

### 第二步：先跑 30 条 smoke

比较：

- 旧 Wiki-first 结果。
- 新 LLM-first raw 结果。
- 新 Wiki-posthoc revised 结果。

重点看：

- 回答是否更像临床兽医。
- 处方化内容是否更完整。
- Wiki 是否能拦住事实错误和危险用药。

### 第三步：再跑 500 条

如果 30 条通过，再扩大到 500 条。

重点看：

- unsupported claim 率。
- revision rate。
- unsafe claim 率。
- final train-ready rate。
- 与 gold_dataset 的风格接近度。

## 九、主要风险

### 风险 1：LLM 原始回答幻觉增加

解决：

- 强化 posthoc claim 抽取和 Wiki 评估。
- 高风险 claim 必须有证据，否则修订或拒绝。

### 风险 2：处方化回答越界

解决：

- 精确剂量、疗程、休药期必须有药品标签或规则卡支撑。
- 无支撑时只能给类别和边界。

### 风险 3：Wiki 检索召回不足

解决：

- 同时用疾病名、症状、英文名、别名、实体 ID 检索。
- 支持多跳检索：疾病 -> 症状 -> 药物 -> 监管规则。

### 风险 4：修订后又变模板化

解决：

- 修订 prompt 要求保留原回答结构和语气。
- 只改错，不重写。

## 十、结论

建议将 Wiki 从“生成前硬约束”后移为“生成后事实核验、安全审稿、证据评分、必要修订和训练准入”。

这样做的核心收益是：

1. 让 LLM 先发挥临床表达和处方化组织能力。
2. 让 Wiki 专注做事实和安全边界控制。
3. 同时提升回答自然度、临床可操作性和医学可靠性。
4. 避免生成结果变成知识库摘要或保守拒答。
5. 更公平地衡量 Wiki 对数据质量的真实增益。

一句话概括：

**新方案不是让 Wiki 指挥 LLM 怎么说，而是让 Wiki 审核 LLM 说得对不对、安不安全、能不能进训练集。**
