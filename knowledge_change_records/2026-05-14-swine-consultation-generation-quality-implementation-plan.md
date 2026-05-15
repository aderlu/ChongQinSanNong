# 2026-05-14 猪病真实问诊数据生成质量源头治理落地方案

## 一、目标

当前已完成 Phase18 裁判、仲裁与 Phase16 CSV 准入字段的改造，但这只能更好地识别和隔离坏样本，不能从源头提升问答生成质量。

本方案用于指导下一步生成端改造，目标是让 Phase12、Phase13、Phase14、Phase14b 生成的问答本身更像真实猪病问诊，而不是依赖后置裁判筛掉大量坏样本。

目标链路：

```text
Phase12 规划真实问诊场景
→ Phase13 生成问诊型 skeleton
→ Phase14 生成自然用户问题和主回答
→ Phase14b 清理审计痕迹和模板腔
→ Phase15 事实/安全门控
→ Phase18 新裁判反向评估生成质量
→ Phase16 按 sft_admission 导出
```

## 二、当前生成质量问题

### 2.1 用户问题不像真实问诊

常见问题：

- 问题像知识库检索题。
- 问题过于完整，像技术病例摘要。
- 用户身份单一，缺少养殖户、饲养员、场长、基层技术员差异。
- 缺少焦急、误判、只问“现在怎么办”、直接问药等真实场景。
- 问题中容易出现内部任务口吻或知识库痕迹。

影响：

- 训练数据会让模型学成百科问答，而不是问诊 agent。
- 后续裁判会把大量样本判为 `repairable` 或 `invalid`。

### 2.2 回答像审计文本或模板答案

常见问题：

- 主回答暴露 `source=`、`fact=`、`page=`、`rule=`、`DIS-` 等审计痕迹。
- 回答结构像字段拼接，不像兽医对养殖户说话。
- 开头不回应现场情况，直接列疾病事实。
- 只说“建议送检”，缺少低风险现场动作。
- 追问是机械清单，缺少临床优先级。

影响：

- `scenario_realism` 和 `communication_naturalness` 低。
- 主训练视图不可直接使用。

### 2.3 安全边界与可执行性失衡

常见问题：

- 低风险样本过度保守，只有拒答和送检。
- 高风险样本为了“可执行”越界给药、剂量、休药期、监管动作。
- L5/L6 样本回答趋同，缺少多样化边界表达。

影响：

- 数据真实性下降。
- 容易产生 `hard_fail`。

### 2.4 skeleton 对真实问诊约束不足

常见问题：

- skeleton 主要承载证据和事实，缺少用户画像、信息缺失、紧急程度、误判倾向。
- `must_include_claims` 容易驱动模型把知识点硬塞进主回答。
- 生成器不知道哪些内容应进入主回答，哪些应只进入审计字段。

影响：

- Phase14 即使 prompt 调整，也容易被 skeleton 结构拉回百科/审计风格。

## 三、总体修改原则

### 3.1 知识库只约束，不污染主问答

主回答禁止出现：

- `source=`
- `fact=`
- `page=`
- `rule=`
- `DIS-`
- `引用锚点`
- `知识库`
- `wiki`

证据追溯只允许出现在：

- `grounded_audit_answer`
- `evidence_anchors`
- `metadata`
- 裁判/仲裁报告

原因：

真实用户不需要看到审计字段。主回答泄漏这些字段会让数据不像问诊，也会污染 SFT。

### 3.2 真实问诊优先，但不牺牲安全

回答应具备：

- 现场回应。
- 初步风险判断。
- 可能方向或鉴别思路。
- 2 到 4 个相关低风险动作。
- 关键追问。
- 检测/就医/分诊建议。
- 用药或监管边界。

但禁止：

- 无证据精确诊断。
- 无证据具体药名、剂量、疗程、休药期。
- 在线上问诊中直接给监管执行结论。
- 编造检测、剖检、免疫、药敏结果。

### 3.3 多样性来自场景变量，不来自医学乱编

允许多样：

- 用户身份。
- 语言风格。
- 症状组合。
- 信息完整度。
- 紧急程度。
- 咨询目的。
- 是否误判。
- 是否直接问药。

禁止多样：

- 编造疾病事实。
- 编造检测结果。
- 编造用药依据。
- 随机给处方。

## 四、Phase12 修改要求：样本规划阶段

目标文件：

`ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase12_plan_samples_from_wiki.py`

### 4.1 新增规划字段

建议在 sample plan 中新增或稳定输出：

| 字段 | 取值示例 | 用途 |
|---|---|---|
| `user_persona` | `small_farmer` / `keeper` / `farm_owner` / `field_technician` / `anxious_misdiagnosis` | 控制用户口吻 |
| `information_completeness` | `low` / `medium` / `high` | 控制问题是否完整 |
| `urgency_level` | `low` / `medium` / `high` | 控制分诊强度 |
| `consultation_intent` | `ask_disease` / `ask_what_to_do` / `ask_drug` / `ask_sampling` / `ask_risk` | 控制问题目的 |
| `misconception_type` | `none` / `suspect_asf` / `want_injection` / `confuse_feed_issue` | 控制真实误判 |
| `question_style` | `oral_short` / `farm_note` / `technical_brief` / `urgent_call` | 控制表达风格 |
| `actionability_level` | `A0` / `A1` / `A2` / `A3` | 控制允许的可执行程度 |
| `prescription_support_level` | `P0` / `P1` / `P2` / `P3` / `P4` | 控制药物建议边界 |

原因：

如果 Phase12 不规划这些变量，Phase14 只能靠 prompt 临场发挥，生成结果容易回到单一模板。

### 4.2 推荐分布

建议小批次中保持如下分布：

| 变量 | 推荐比例 |
|---|---:|
| 普通养殖户/小散户 | 35%-45% |
| 饲养员 | 20%-30% |
| 猪场老板 | 10%-20% |
| 基层技术员 | 10%-20% |
| 焦急误判用户 | 5%-10% |
| 信息不完整问题 | 45%-60% |
| 直接问“现在怎么办” | 25%-35% |
| 直接问药 | 10%-20%，其中多数应边界化处理 |
| 高紧急度 | 15%-25% |

验收：

- 40 条样本中不得超过 25% 使用同一用户画像。
- 至少 40% 的问题应存在合理信息缺失。
- 至少 20% 的问题应只问现场处置或风险，而不是直接问疾病定义。

## 五、Phase13 修改要求：skeleton 阶段

目标文件：

`ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase13_build_answer_skeletons.py`

### 5.1 skeleton 新增问诊合同

建议新增 `consultation_generation_contract`：

```json
{
  "user_persona": "small_farmer",
  "question_style": "oral_short",
  "information_completeness": "low",
  "urgency_level": "medium",
  "consultation_intent": "ask_what_to_do",
  "required_consultation_moves": [
    "respond_to_scene",
    "state_uncertainty",
    "ask_key_followups",
    "give_low_risk_next_steps",
    "triage_or_testing_boundary"
  ],
  "forbidden_main_answer_artifacts": [
    "source=",
    "fact=",
    "page=",
    "rule=",
    "DIS-",
    "知识库",
    "引用锚点"
  ]
}
```

原因：

skeleton 应告诉 Phase14 怎样构造真实问诊，而不是只告诉它哪些事实必须包含。

### 5.2 将证据事实分为主回答事实和审计事实

建议把 claims 分为：

| 字段 | 说明 |
|---|---|
| `main_answer_claims` | 可自然写入主回答的少量关键结论 |
| `audit_only_claims` | 只用于追溯，不应写入主回答 |
| `boundary_claims` | 用于说明不能确诊、不能开药、需要检测/兽医现场判断 |

原因：

当前 `must_include_claims` 容易导致回答堆事实。真实问诊主回答只需要少量关键结论，其余证据放到审计字段。

验收：

- 每个 skeleton 至少有 1 个 `boundary_claims` 或明确的边界规则。
- 主回答事实不应超过 3 到 5 个核心点。
- 审计字段可以完整，但主回答必须自然。

## 六、Phase14 修改要求：生成阶段

目标文件：

`ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14_generate_two_stage_samples.py`

### 6.1 修改问题生成逻辑

重点函数：

- `question_for()`
- `scenario_for()`
- `case_user_query_for()`
- `clinical_generation_user_prompt()`

要求：

- `case_user_query` 必须由 `user_persona`、`information_completeness`、`urgency_level`、`consultation_intent` 共同决定。
- 不允许直接把 disease/entity 名称机械塞进问题。
- 普通养殖户问题允许口语、不完整、焦急。
- 技术员问题可以更专业，但不能像知识库检索。

示例：

```text
老师，我这边保育猪这两天有几头不吃料，还有点喘，有一头早上死了。我怕传开，现在先咋处理？要不要马上打针？
```

不合格示例：

```text
请根据猪繁殖与呼吸综合征的知识库事实，说明该病的诊断和防控措施。
```

### 6.2 修改主回答生成 prompt

`clinical_answer` 必须遵守：

- 第一段回应用户现场情况。
- 不能直接确诊。
- 给出 2 到 4 个与场景相关的低风险动作。
- 追问 3 到 6 个关键问题，按优先级排列。
- 高风险场景必须提示尽快联系兽医或送检。
- 直接问药时，优先说明不能线上给具体剂量；可给条件性、类别级、需现场兽医确认的边界表达。
- 禁止主回答出现审计字段。

建议 prompt 明确：

```text
clinical_answer 是给真实养殖户/猪场人员看的，不是审计报告。
不要输出 source=、fact=、page=、rule=、DIS-、引用锚点、知识库。
证据追溯写入 stage_2_answer 或 evidence_anchors，不写入 clinical_answer。
```

### 6.3 加入 actionability 矩阵

| 能力层 | 允许的可执行性 | 禁止项 |
|---|---|---|
| L1 | 解释、信息补充、低风险观察 | 诊断确定、处方 |
| L2 | 初步方向、关键追问、送检建议 | 精确诊断、剂量 |
| L3 | 鉴别思路、检测路径 | 无证据治疗方案 |
| L4 | 防控边界、隔离观察、减少应激 | 监管执行结论 |
| L5 | 药物边界、拒绝无证据处方 | 具体剂量/疗程/休药期，除非 P4 |
| L6 | 监管边界、建议依法联系机构 | 扑杀/封锁/调运/上报等执行结论 |

原因：

这样可以保证回答有帮助，但不会为了可执行性越界。

### 6.4 加入 prescription_support_level

| 等级 | 含义 | 允许内容 |
|---|---|---|
| P0 | 无药物支持 | 不给药物建议 |
| P1 | 支持护理 | 补水、电解质、保温、减少应激等 |
| P2 | 类别级建议 | “需兽医判断是否使用抗菌药/退热药” |
| P3 | 有药名但无完整处方依据 | 可提药名边界，但不能给剂量/疗程/休药期 |
| P4 | 有标签/权威证据完整支持 | 才允许药名、剂量、疗程、休药期 |

要求：

- 默认不得生成 P4，除非 skeleton 明确具备标签或 A0/A1 证据。
- `clinical_answer` 里如出现具体药名、剂量、疗程、休药期，必须在审计字段中说明证据来源。
- 无体重、日龄、药品规格时不得给精确剂量。

验收：

- 直接问药样本中，80% 以上应能体现边界而不是简单拒答。
- 无 P4 证据时，不得出现精确剂量、疗程、休药期。

## 七、Phase14b 修改要求：自然化与清理阶段

目标文件：

`ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14b_naturalize_grounded_answers.py`

### 7.1 新增主回答清理规则

必须清理：

- `source=...`
- `fact=...`
- `page=...`
- `rule=...`
- `DIS-...`
- JSON/字典残片。
- 英文模板标签。
- “根据知识库”“引用锚点”等审计话术。

### 7.2 新增自然度修复

应修复：

- 开头过硬，缺少现场回应。
- 只列知识点，缺少“现在先做什么”。
- 追问清单过长。
- 高风险样本只有拒答，没有安全动作。

修复后仍必须保留：

- 不确诊边界。
- 检测/兽医现场判断建议。
- 事实证据约束。

验收：

- `clinical_answer` 不得包含审计字段。
- 回答长度建议控制在 180 到 500 中文字，复杂技术员问题可适当更长。
- 追问不超过 6 个，且应有优先级。

## 八、字段与CSV影响

生成样本建议新增字段：

| 字段 | 来源 | 说明 |
|---|---|---|
| `user_persona` | Phase12/13/14 | 用户画像 |
| `question_style` | Phase12/13/14 | 问题表达风格 |
| `information_completeness` | Phase12/13/14 | 信息完整度 |
| `urgency_level` | Phase12/13/14 | 紧急程度 |
| `consultation_intent` | Phase12/13/14 | 咨询目的 |
| `misconception_type` | Phase12/13/14 | 误判类型 |
| `actionability_level` | Phase13/14 | 可执行性上限 |
| `prescription_support_level` | Phase13/14 | 药物建议证据等级 |
| `main_answer_claims` | Phase13 | 主回答可用事实 |
| `audit_only_claims` | Phase13 | 审计专用事实 |
| `boundary_claims` | Phase13 | 边界/拒答依据 |
| `generation_quality_flags` | Phase14/14b | 生成端质量标记 |

Phase16 CSV 建议后续同步加入上述字段，便于按用户画像、紧急程度、处方支持等级分析质量。

## 九、验收流程

### 9.1 10条校准批次

先生成 10 条，要求覆盖：

- 普通养殖户。
- 饲养员。
- 场长/老板。
- 技术员。
- 焦急误判用户。
- 直接问药。
- 高死亡/传播风险。
- 信息很少的问题。
- L5 药物边界。
- L6 监管边界。

验收阈值：

- `scenario_realism` 平均不低于 11/15。
- `consultation_completeness` 平均不低于 11/15。
- `medical_correctness` 平均不低于 18/25。
- `triage_boundary` 不得低于 7/10。
- 主回答审计字段泄漏为 0。
- `hard_fail` 为 0。

### 9.2 40条正式批次

通过 10 条校准后再跑 40 条。

验收阈值：

- `high_quality_valid + valid` 不低于 70%。
- `invalid` 不高于 10%。
- `repairable` 不高于 25%。
- `scenario_realism` 低于 8/15 的样本不超过 10%。
- `main_sft + low_weight_sft` 中不得出现审计字段泄漏。
- L5/L6 样本必须全部进入仲裁，且不得因无证据处方进入主训练。

### 9.3 失败回滚规则

如果出现以下情况，应停止扩大生成：

- `hard_fail` 超过 5%。
- 审计字段泄漏超过 0。
- 直接问药样本出现无证据剂量。
- L6 样本出现监管执行结论。
- 大量问题仍像知识库检索题。

## 十、实施顺序

建议分四步落地：

1. 修改 Phase12，先让计划中有真实问诊变量。
2. 修改 Phase13，把问诊合同写进 skeleton。
3. 修改 Phase14，重写问题生成和主回答 prompt。
4. 修改 Phase14b，做审计泄漏清理和自然度修复。

每一步都应新增一份工作留痕文档，记录：

- 修改前问题。
- 修改文件。
- 新增字段。
- 修改逻辑。
- 预期效果。
- 验证结果。
- 未解决风险。

## 十一、与当前 Phase18/Phase16 的衔接

当前 Phase18 已经能评估：

- 真实性/场景感。
- 问诊完整性。
- 医学正确性。
- 追问逻辑。
- 边界与分诊。
- 上下文一致性。
- 可执行性。
- 结构化与可标注性。

因此生成端改造后，应直接用 Phase18 作为反向质量仪表盘：

```text
Phase14/14b 生成
→ Phase15 门控
→ Phase18 新裁判评分
→ 按低分维度回改 Phase12/13/14
```

这能形成闭环，而不是只靠人工抽检。

## 十二、结论

生成质量问题不能只靠裁判解决。真正的源头治理必须改：

- Phase12 的场景规划。
- Phase13 的问诊 skeleton。
- Phase14 的问题和主回答生成 prompt。
- Phase14b 的自然化与审计清理。

本方案的核心是让生成器先知道“真实问诊长什么样”，再让新 Phase18 裁判判断是否达标。

只有完成这条链路，当前问答数据中“知识库题、审计腔、模板腔、追问机械、可执行性失衡、药物边界不稳”的问题才有可能被系统性解决。
