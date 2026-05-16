# 2026-05-15 真实养殖户问诊 + 临床式回答整改执行文档

## 一、背景与当前结论

本文件用于整改 `baseline_comparison_wiki_20260515_baseline500_parallel3_v2.csv` 中 `user_query` 和 `assistant_answer` 质量无效的问题。

当前问题不是 54 字段结构问题，而是问答内容质量问题：

- `user_query` 不像真实养殖户、饲养员或场长咨询，而像审计/质控人员在填写问诊采集表。
- `assistant_answer` 不像临床兽医给现场人员的判断和处置建议，而像安全边界模板：不能确诊、补资料、送检、找兽医。
- 该问题会导致 Wiki 组即使调用真实 LLM，也生成低训练价值样本，无法达到 `D:/ChongQin/鸡病数据合成系统/results/gold_dataset_1000_20260429_173132.csv` 的问答水准。

本轮整改目标是让正式输出变成：

```text
真实养殖户问诊 user_query
+ 临床式兽医回答 assistant_answer
+ 仍保留 Wiki grounding、事实边界和安全约束
+ 可通过自动质量闸门和人工抽检
```

## 二、已确认的问题证据

### 2.1 当前 Wiki 500 条的症状

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/exports/baseline_validation/comparisons/baseline_comparison_wiki_20260515_baseline500_parallel3_v2.csv
```

抽查和统计显示：

| 字段 | 问题词 | 命中情况 |
|---|---:|---:|
| `user_query` | `还需要我补哪些信息` | 500/500，100% |
| `user_query` | `剖检` | 331/500，66.2% |
| `user_query` | `日龄` | 348/500，69.6% |
| `user_query` | `发病比例` | 340/500，68.0% |
| `user_query` | `实验室检测` | 218/500，43.6% |
| `assistant_answer` | `送检` | 410/500，82.0% |
| `assistant_answer` | `剖检` | 352/500，70.4% |
| `assistant_answer` | `实验室检测` | 311/500，62.2% |

这些比例说明专业术语不是偶发，而是被生成链路系统性注入。

### 2.2 典型错误样式

当前错误问题样式：

```text
我们这边是自繁自养场，一批保育猪换栏后一两天开始出现，现在主要是咳嗽、喘气、皮肤发红、走路不稳。
还没送实验室检测、还没做剖检、还没量体温，心里没底，想先判断严不严重。
会不会是非瘟？
麻烦先帮我判断一下主要方向和下一步排查重点。
还需要我补哪些信息，比如是否做过剖检或检测、日龄、发病比例？
```

该问题不符合真实普通养殖户问诊习惯。真实问法更可能是：

```text
兽医老师，我这批保育猪刚换栏两天就开始咳喘，有几头不吃料，身上发红，还有两头走路发晃。
今天早上又多了几头，我有点怕是不是大病。
这种情况严重不严重？现在先咋处理？
```

### 2.3 Gold 数据的目标风格

参考文件：

```text
D:/ChongQin/鸡病数据合成系统/results/gold_dataset_1000_20260429_173132.csv
```

该 gold 数据的典型结构：

- `user_query`：真实养殖场景描述，包括规模、品种、日龄/阶段、症状、死亡、环境变化、用户诉求。
- `diagnosis`：临床判断、病理逻辑、鉴别诊断。
- `prescription`：现场处置、治疗/非治疗边界、管理措施。
- `withdrawal_period`：涉及用药时说明休药期；不适用时说明原因。

本项目最终仍可保留 `assistant_answer` 单字段，但建议内部生成时拆成：

```json
{
  "clinical_judgement": "...",
  "differential_diagnosis": "...",
  "field_actions": "...",
  "drug_or_regulatory_boundary": "...",
  "followup_questions": "..."
}
```

再合成为 `assistant_answer`。

## 三、根因分析

### 3.1 根因一：用户问题模板直接注入专业术语

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/consultation_case_variables.py
```

问题位置：

- `_MISSING_INFO`
- `_FOLLOWUP_TOPICS`
- `build_case_user_query()`

当前逻辑把以下内容直接放进用户问题：

```text
日龄和批次记录不全
发病比例和死亡数还没统计清楚
免疫记录一时找不到
还没送实验室检测
还没做剖检
是否做过剖检或检测
```

产生结果：

- 用户问题过于专业。
- 每条问题都像在主动配合数据标注。
- 普通养殖户自然表达被专业字段覆盖。

解决方向：

- 专业字段保留在 `case_context` 内部，不直接进入 `user_query`。
- `user_query` 只表达现场看到的症状、变化、担心和求助意图。
- `剖检/实验室检测/发病比例/检测结果` 默认不得出现在普通用户问题中。

### 3.2 根因二：固定追加“还需要我补哪些信息”

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/consultation_case_variables.py
```

问题函数：

```text
build_case_user_query()
```

当前会固定拼接：

```text
还需要我补哪些信息，比如...
```

产生结果：

- 500 条全部出现同一尾巴。
- 问题相似度过高。
- 用户角色从“求助者”变成“问诊数据采集员”。

解决方向：

- 删除该固定尾巴。
- 将补充信息需求转移到 `assistant_answer` 的最多 1-3 个追问中。
- 如果用户身份是 `field_technician`，才允许少量专业补充问题。

### 3.3 根因三：Phase13 骨架把追问主题专业化

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase13_build_answer_skeletons.py
```

当前骨架包含：

```text
发病日龄/阶段
发病率和死亡率
采样或实验室检测结果
剖检或检测信息
检测或监管依据
```

产生结果：

- 下游 Phase14 会把这些项目当成必须覆盖的问诊点。
- LLM 被迫输出“补齐资料、检测、剖检、送检”。
- 回答倾向从临床解释变成审计清单。

解决方向：

- Phase13 保留内部临床目标，但改成口语化/临床化标签。
- 内部字段命名可以专业，展示给用户的追问必须口语。
- 追问数量从 3-6 个降为 1-3 个。

### 3.4 根因四：Phase14 prompt 强化泛化安全回答

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py
```

问题函数：

```text
clinical_generation_user_prompt()
default_clinical_answer()
```

当前提示词要求：

- 必须给 2-4 个低风险动作。
- 必须提出 3-6 个关键追问。
- 示例动作包含“联系兽医采样送检”。
- 缺少体重、日龄、现场兽医确认时不得给精确剂量。

这些安全要求本身合理，但被放在主回答生成目标里后，模型会过度保守。

产生结果：

- 回答缺少倾向诊断。
- 回答缺少病理逻辑和鉴别诊断。
- 回答反复出现“不能确诊、补资料、送检”。
- 具体现场处置不够具体。

解决方向：

- 新 prompt 的主目标改为“临床判断优先，安全边界兜底”。
- 要求回答包含“倾向方向 + 理由 + 鉴别方向 + 现场动作 + 少量追问”。
- 禁止回答只由“不能确诊/送检/补信息”构成。

### 3.5 根因五：质量裁判奖励方向偏差

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/baseline_validation/judge_general_consultation.py
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase18_dual_judge_and_arbitrate.py
```

当前倾向奖励：

- 有追问。
- 有边界。
- 有送检。
- 有低风险动作。

但没有强惩罚：

- 用户问题专业化。
- 用户问题模板化。
- 回答没有临床倾向。
- 回答只有泛化安全建议。

产生结果：

- 低训练价值问答仍可能拿高分。
- 结构验收通过，但内容验收失败。

解决方向：

- 增加 QA realism gate。
- 增加 gold-style score。
- 对专业术语泄漏、模板尾巴、泛化回答设置硬失败。

## 四、整改目标

### 4.1 user_query 目标

`user_query` 应像真实养殖户、饲养员、场长或基层技术员的自然咨询。

必须包含：

- 猪群阶段或大致类别，例如保育猪、育肥猪、母猪、仔猪。
- 现场症状，例如咳喘、拉稀、发热、皮肤发红、精神差、死亡。
- 时间线或变化，例如刚换栏、这两天、今天早上、连续两批。
- 用户诉求，例如“咋回事”“严不严重”“先咋处理”“是不是大病”“能不能先用药”。

普通养殖户问题中默认禁止：

- `还需要我补哪些信息`
- `实验室检测`
- `剖检`
- `发病比例`
- `检测结果`
- `采样送检`
- `是否做过剖检或检测`

允许例外：

- `field_technician` 或 `farm_vet` 身份可以少量出现专业词，但比例必须受控。
- 高风险监管类场景中，用户可问“要不要上报/能不能转猪”，但不能每条都问。

### 4.2 assistant_answer 目标

`assistant_answer` 应像临床兽医给现场人员的回答。

必须包含：

1. 初步临床判断  
   说明“更像哪类问题”或“优先考虑哪些方向”。

2. 判断依据  
   结合用户症状、猪群阶段、时间线、死亡/传播情况。

3. 鉴别方向  
   给出 2-3 个可能方向，并说明为什么需要区分。不得无依据硬确诊。

4. 现场处置  
   给出具体、低风险、可执行步骤。

5. 少量追问  
   只问 1-3 个最关键问题，不能清单化。

6. 安全边界  
   在药物、剂量、休药期、调运、上报、扑杀等高风险内容上保持边界。

禁止：

- 只说“不能确诊、建议送检、联系兽医”。
- 大段审计式免责声明。
- 每条都机械出现“剖检、实验室检测、采样送检”。
- 编造检测阳性、剖检所见、免疫事实、用药事实。

## 五、具体代码修改方案

### 5.1 修改 `consultation_case_variables.py`

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/consultation_case_variables.py
```

#### 5.1.1 拆分内部专业字段和用户表述字段

新增两套变量：

```python
_INTERNAL_MISSING_INFO = [
    "age_stage_unknown",
    "morbidity_unknown",
    "mortality_unknown",
    "vaccination_unknown",
    "medication_unknown",
    "necropsy_not_done",
    "lab_test_not_done",
]

_FARMER_VISIBLE_UNCERTAINTY = [
    "还没来得及细数到底多少头不对劲",
    "只知道今天比昨天多了几头",
    "死了几头还没完全弄清楚原因",
    "疫苗和用药记录还没翻出来",
    "现场只看到这些症状，心里没底",
    "刚发现问题，还没请兽医到场看",
]
```

说明：

- `_INTERNAL_MISSING_INFO` 进入 `case_context`。
- `_FARMER_VISIBLE_UNCERTAINTY` 可进入 `user_query`。
- 不再把“实验室检测、剖检、发病比例”直接放入普通用户问题。

#### 5.1.2 重写 followup topics

当前：

```python
_FOLLOWUP_TOPICS = [
    "日龄",
    "发病比例",
    "死亡变化",
    "免疫记录",
    "近期用药",
    "是否转群或换料",
    "是否做过剖检或检测",
]
```

改为：

```python
_FOLLOWUP_TOPICS = [
    "多大猪",
    "大概几头不对劲",
    "有没有死猪、死了几头",
    "吃料喝水有没有明显下降",
    "最近有没有换料、转栏、降温或引种",
    "最近打过什么苗、用过什么药",
    "有没有同栏或隔壁栏也开始发病",
]
```

#### 5.1.3 重写 `build_case_user_query()`

删除固定拼接：

```python
" 还需要我补哪些信息，比如..."
```

新增按 persona/style 生成的自然问句模板：

```python
_FARMER_QUESTION_ENDINGS = [
    "这大概是咋回事？现在先咋处理？",
    "这种情况严不严重，会不会越传越多？",
    "我怕是大病，先要不要隔开？",
    "能不能先用点药，还是先别乱动？",
    "麻烦帮我判断下主要往哪个方向考虑。",
]
```

目标输出示例：

```text
兽医老师，我这批保育猪刚换栏两天就开始咳喘，有几头不吃料，身上还有点发红。
今天早上又多了几头，现场只看到这些症状，心里没底。
这大概是咋回事？现在先咋处理？
```

验收标准：

- 生成 100 条 smoke 时，`还需要我补哪些信息` 命中 0。
- 普通 persona 中，`实验室检测/剖检/发病比例` 总命中率小于 5%。
- `user_query` 平均长度建议 120-240 字。
- exact duplicate 为 0。

### 5.2 修改 `phase13_build_answer_skeletons.py`

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase13_build_answer_skeletons.py
```

#### 5.2.1 required_followups 内部化

将专业追问改成临床内部目标：

```python
required_followups = [
    "clarify_pig_stage_or_rough_age",
    "clarify_affected_and_dead_count",
    "clarify_onset_and_spread_speed",
    "clarify_feed_transfer_weather_or_introduction_change",
    "clarify_recent_vaccine_or_drug_if_relevant",
]
```

再增加用户可见追问表达：

```python
farmer_followup_phrases = [
    "这批猪大概多大、哪个阶段？",
    "现在大概几头有症状，死了几头？",
    "是突然一片起来，还是零星慢慢多？",
    "最近有没有换料、转栏、降温或新进猪？",
    "最近打过什么苗、用过什么药？",
]
```

#### 5.2.2 consultation_generation_contract 调整

当前：

```text
followup_question_count = 3-6
low_risk_action_count = 2-4
```

改为：

```text
followup_question_count = 1-3
low_risk_action_count = 2-4
answer_style = clinical_gold_style
must_include_clinical_judgement = true
must_include_differential_directions = true
avoid_generic_testing_boilerplate = true
```

### 5.3 修改 `phase14_generate_two_stage_samples.py`

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py
```

#### 5.3.1 修改 `clinical_generation_user_prompt()`

新增核心要求：

```text
clinical_answer 必须采用真实兽医临床问诊回答风格，不是审计摘要。

回答结构：
1. 先给出初步临床方向：更像哪类疾病或问题，严重程度如何。
2. 说明判断依据：必须引用用户提供的症状、阶段、时间线。
3. 给出 2-3 个鉴别方向：说明为什么要区分，不能硬确诊。
4. 给出现场可执行步骤：隔离、保温通风、饮水采食、病弱猪处理、避免混群、记录死亡变化等。
5. 最后只问 1-3 个最关键追问。
6. 药物、剂量、休药期、调运、上报、扑杀等高风险内容必须有边界。

禁止：
- 不得只写“无法确诊、建议送检、补齐资料”。
- 不得把回答写成 Wiki 审计、证据摘要或检测清单。
- 不得在普通养殖户问题中复述“剖检、实验室检测、发病比例”等专业缺失项。
- 不得编造检测结果、剖检结果、免疫事实或用药事实。
```

#### 5.3.2 修改 `default_clinical_answer()`

当前 fallback 是固定泛化模板。必须改成使用：

- `case_user_query`
- `target_disease`
- `pig_stage`
- `observed_signals`
- `risk_class`
- `evidence_anchors`

生成至少包含：

```text
从你说的症状看，首先要把它当成群体性疾病风险处理...
目前更需要优先区分的是...
现场先做三件事...
我还需要确认两点...
```

fallback 不得固定写：

```text
记录日龄、栏舍、发病头数、死亡变化、剖检、采样和实验室检测
```

#### 5.3.3 增加 structured clinical answer 字段

建议 Stage14 输出增加：

```json
"stage_2_grounded": {
  "clinical_answer": "...",
  "clinical_judgement": "...",
  "differential_diagnosis": "...",
  "field_actions": "...",
  "followup_questions": ["...", "..."],
  "safety_boundary": "...",
  "grounded_audit_answer": "..."
}
```

`assistant_answer` 继续使用 `clinical_answer`，`grounded_audit_answer` 只用于审计，不进入主训练问答。

### 5.4 修改 baseline B/C 组生成

文件：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/baseline_validation/generate_baseline_groups.py
```

当前 B/C 组也会使用同一套模板和 fallback，因此同样会产生泛化回答。

修改要求：

- B/C 组必须使用同一个自然 `case_user_query`。
- B/C 组 prompt 也采用 gold-style clinical answer。
- 不允许 fallback 写“补齐日龄、发病比例、检测结果”。
- B/C 组可以没有 Wiki facts，但仍必须生成临床式回答，方便和 Wiki 组比较。

### 5.5 新增 QA 质量闸门

新增脚本：

```text
D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/baseline_validation/qa_realism_gate.py
```

输入：

```text
--input exports/baseline_validation/comparisons/baseline_comparison_wiki_{run_id}.csv
--gold-reference D:/ChongQin/鸡病数据合成系统/results/gold_dataset_1000_20260429_173132.csv
--output exports/baseline_validation/reports/qa_realism_gate_{group}_{run_id}.json
```

#### 5.5.1 user_query 硬失败规则

任一命中即失败：

```text
还需要我补哪些信息
是否做过剖检或检测
请基于现有资料
猪场兽医咨询：
现有资料能确认
证据不足
Wiki
source=
fact=
rule=
DIS-
```

普通 persona 中以下词受控：

```text
实验室检测
剖检
发病比例
检测结果
采样送检
```

阈值：

```text
普通 persona user_query 中每个专业词命中率 <= 5%
全部专业词合并命中率 <= 12%
```

#### 5.5.2 assistant_answer 硬失败规则

任一命中即失败：

```text
只包含边界声明，没有临床倾向
只说补资料/送检/联系兽医，没有现场处置
编造检测阳性
编造剖检可见
给出无依据确诊
给出具体药物 + 剂量 + 疗程 + 休药期，但证据等级不支持
```

#### 5.5.3 assistant_answer 质量正向规则

每条回答至少满足：

- 有初步方向：命中“首先考虑/优先考虑/更像/需要警惕/高度怀疑/倾向于”等表达之一。
- 有判断依据：回答中引用至少 2 个用户症状或上下文变量。
- 有鉴别方向：至少出现 2 个疾病/病因方向，或明确说明“需要和 X、Y 区分”。
- 有现场动作：至少 2 个具体动作。
- 追问不超过 3 个。

#### 5.5.4 批量验收阈值

500 条正式输出必须满足：

```text
user_query_hard_fail_rate = 0
assistant_answer_hard_fail_rate <= 2%
professional_leakage_rate_user_query <= 12%
generic_answer_rate <= 8%
exact_duplicate_user_query = 0
exact_duplicate_assistant_answer = 0
gold_style_pass_rate >= 85%
```

## 六、执行流程

### 6.1 开发顺序

1. 修改 `consultation_case_variables.py`。
2. 修改 `phase13_build_answer_skeletons.py`。
3. 修改 `phase14_generate_two_stage_samples.py`。
4. 修改 `generate_baseline_groups.py`。
5. 新增 `qa_realism_gate.py`。
6. 增加测试。
7. 跑 30 条 smoke。
8. 人工抽检。
9. 跑 500 条正式。
10. 跑最终验收。

### 6.2 单元测试建议

新增或扩展测试文件：

```text
D:/XF-ChongQin/ai-/tests/test_real_farmer_clinical_qa_generation.py
```

测试点：

```python
def test_farmer_query_has_no_fixed_followup_tail():
    assert "还需要我补哪些信息" not in query

def test_farmer_query_avoids_professional_terms_for_small_farmer():
    forbidden = ["实验室检测", "剖检", "发病比例", "检测结果"]
    assert not any(term in query for term in forbidden)

def test_clinical_answer_has_judgement_and_actions():
    assert has_clinical_judgement(answer)
    assert has_field_actions(answer)

def test_qa_realism_gate_rejects_old_template():
    assert gate(old_template_sample)["passed"] is False
```

### 6.3 Smoke 运行

建议 run_id：

```text
20260515_real_farmer_clinical_smoke30_v1
```

命令：

```powershell
cd D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative

python tools\pipeline\baseline_validation\run_baseline_experiment.py `
  --date 20260515_real_farmer_clinical_smoke30_v1 `
  --limit 30 `
  --parallel 3 `
  --groups wiki,no_wiki,metadata_only `
  --mode real-api
```

如果当前 `run_baseline_experiment.py` 参数不支持 `--groups` 或 `--mode`，则按现有脚本参数执行，但必须保证：

- Wiki 组走真实 Phase12-18 链路。
- B/C 组调用真实 LLM。
- 三组使用同一批 case seeds。

运行 QA gate：

```powershell
python tools\pipeline\baseline_validation\qa_realism_gate.py `
  --input exports\baseline_validation\comparisons\baseline_comparison_wiki_20260515_real_farmer_clinical_smoke30_v1.csv `
  --group wiki `
  --run-id 20260515_real_farmer_clinical_smoke30_v1 `
  --gold-reference "D:\ChongQin\鸡病数据合成系统\results\gold_dataset_1000_20260429_173132.csv"
```

三组都要运行。

### 6.4 Smoke 人工抽检

人工抽检每组 10 条，重点看：

- 用户是否像真实养殖户。
- 是否还有固定尾巴。
- 是否还主动说剖检/实验室检测/发病比例。
- 回答是否有倾向判断。
- 回答是否有鉴别诊断。
- 回答是否有可执行现场动作。
- 是否安全但不过度拒答。

Smoke 必须达到：

```text
30 条中至少 27 条可接受
固定尾巴 0 条
明显审计式 user_query 0 条
泛化模板 assistant_answer <= 2 条
```

### 6.5 正式 500 条运行

建议 run_id：

```text
20260515_real_farmer_clinical_baseline500_v1
```

命令：

```powershell
cd D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative

python tools\pipeline\baseline_validation\run_baseline_experiment.py `
  --date 20260515_real_farmer_clinical_baseline500_v1 `
  --limit 500 `
  --parallel 3 `
  --groups wiki,no_wiki,metadata_only `
  --mode real-api
```

正式输出：

```text
exports/baseline_validation/comparisons/baseline_comparison_wiki_20260515_real_farmer_clinical_baseline500_v1.csv
exports/baseline_validation/comparisons/baseline_comparison_no_wiki_20260515_real_farmer_clinical_baseline500_v1.csv
exports/baseline_validation/comparisons/baseline_comparison_metadata_only_20260515_real_farmer_clinical_baseline500_v1.csv
exports/baseline_validation/comparisons/baseline_comparison_standard_20260515_real_farmer_clinical_baseline500_v1.csv
```

## 七、最终验收标准

### 7.1 结构验收

每组 CSV：

- 500 行。
- 54 字段。
- `user_query` 非空。
- `assistant_answer` 非空。
- 覆盖猪病知识库全部疾病。
- 三组 `case_seed_id` 一一对应。

### 7.2 user_query 质量验收

必须满足：

```text
还需要我补哪些信息 = 0
普通用户问题中 实验室检测 <= 5%
普通用户问题中 剖检 <= 5%
普通用户问题中 发病比例 <= 5%
普通用户问题中 检测结果 <= 5%
审计式开头 = 0
exact duplicate = 0
平均长度 120-240 字为宜
```

人工抽检标准：

- 看起来像养殖户/场长/饲养员在问。
- 能看到具体场景和症状。
- 不像在背问诊表。

### 7.3 assistant_answer 质量验收

必须满足：

```text
generic_answer_rate <= 8%
只说送检/补资料/不能确诊的回答 <= 5%
含临床倾向判断 >= 90%
含鉴别方向 >= 85%
含具体现场动作 >= 90%
编造检测/剖检/免疫/用药事实 = 0
高风险越界 = 0
```

人工抽检标准：

- 像兽医在答，不像审计报告。
- 有明确“优先考虑/需要警惕/更像”的判断。
- 能解释为什么这样判断。
- 能告诉现场先做什么。
- 边界清楚，但不过度泛化。

### 7.4 与 gold 的对齐验收

对齐目标不是复制鸡病 gold 内容，而是对齐风格：

| 维度 | Gold 风格 | 猪病整改后目标 |
|---|---|---|
| 用户问题 | 规模、品种/阶段、症状、死亡、环境、诉求 | 规模、猪群阶段、症状、死亡/传播、近期变化、诉求 |
| 诊断回答 | 临床症状 + 流行病学 + 疾病倾向 | 症状 + 阶段 + 时间线 + 疾病/病因方向 |
| 鉴别诊断 | 明确列出相似病 | 明确列出 2-3 个需区分方向 |
| 处置方案 | 立即行动、上报、治疗或非治疗边界 | 隔离、护理、观察、兽医介入、检测/监管边界 |
| 休药期/边界 | 适用时说明 | 涉药时说明，不支持时明确边界 |

## 八、为什么该方案能够解决问题

1. 从源头移除专业术语注入  
   `user_query` 的专业污染来自模板和变量，不是 LLM 随机生成。删除模板注入后，问题自然度会立刻改善。

2. 专业信息不丢失，只是不暴露给用户话术  
   `case_context` 仍保留内部临床字段，模型仍可据此判断，但用户表述更真实。

3. 回答目标从“审计安全”改成“临床判断”  
   新 prompt 要求倾向判断、鉴别诊断和现场动作，因此答案不会停留在“不能确诊、送检”。

4. fallback 不再拖后腿  
   旧 fallback 会把所有失败样本拉回泛化模板。新 fallback 即使没有完美 LLM 输出，也能保持临床结构。

5. QA gate 防止旧问题回流  
   如果旧模板再次出现，自动闸门会阻止进入正式 CSV。

6. Gold-style 拆分提高可控性  
   先生成临床判断、鉴别、处置、边界，再合成回答，比直接生成大段回答更容易稳定达到 gold 风格。

## 九、风险与处理

### 9.1 风险：回答变得过于肯定

处理：

- 允许“倾向/优先考虑/需要警惕”，禁止无依据“确诊”。
- Phase15/Phase18 保持事实和安全边界。

### 9.2 风险：过度压制检测建议

处理：

- 不是禁止助手提检测，而是禁止用户每条主动说检测。
- 助手在严重、高死亡、疑似重大疫病场景中仍应建议联系兽医或检测。

### 9.3 风险：B/C 组因为没有 Wiki facts 产生幻觉

处理：

- B/C prompt 必须要求“不编造检测结果、剖检结果、免疫事实”。
- QA gate 和裁判对 unsupported claim 加强惩罚。

### 9.4 风险：强行 gold-style 导致猪病监管边界不够

处理：

- 对非瘟等重大疫病，回答应保持“高度警惕 + 不自行处置 + 联系兽医/主管部门”的边界。
- 但仍要解释临床风险，而不是只说不能判断。

## 十、交付物清单

### 10.1 代码交付

```text
tools/pipeline/consultation_case_variables.py
tools/pipeline/phase13_build_answer_skeletons.py
tools/pipeline/phase14_generate_two_stage_samples.py
tools/pipeline/baseline_validation/generate_baseline_groups.py
tools/pipeline/baseline_validation/qa_realism_gate.py
ai-/tests/test_real_farmer_clinical_qa_generation.py
```

### 10.2 数据交付

```text
exports/baseline_validation/comparisons/baseline_comparison_wiki_{run_id}.csv
exports/baseline_validation/comparisons/baseline_comparison_no_wiki_{run_id}.csv
exports/baseline_validation/comparisons/baseline_comparison_metadata_only_{run_id}.csv
exports/baseline_validation/comparisons/baseline_comparison_standard_{run_id}.csv
```

### 10.3 报告交付

```text
exports/baseline_validation/reports/qa_realism_gate_wiki_{run_id}.json
exports/baseline_validation/reports/qa_realism_gate_no_wiki_{run_id}.json
exports/baseline_validation/reports/qa_realism_gate_metadata_only_{run_id}.json
exports/baseline_validation/reports/real_farmer_clinical_qa_acceptance_{run_id}.md
```

## 十一、最终决策规则

正式 500 条运行后：

- 如果结构验收通过，但 QA realism gate 不通过：不得验收。
- 如果 Wiki 组质量通过，但 B/C 组质量不通过：可以比较 Wiki 组，但不能声称三组公平对比完成。
- 如果三组都通过 QA realism gate，再进行 baseline 有效性比较。
- 如果 Wiki 组事实和边界显著更好，同时自然度不低于 B/C 组，则说明 Wiki 对真实问诊样本有效。
- 如果 Wiki 组自然度仍明显低于 B/C 组，则继续调整 Wiki prompt，不应直接进入正式训练集。

## 十二、下一步执行建议

第一步不要直接跑 500 条。应先完成代码整改并跑 30 条 smoke。

推荐最小闭环：

```text
改 query 模板
-> 改 answer prompt
-> 改 fallback
-> 加 QA gate
-> 跑 30 条
-> 人工抽检 10 条
-> 自动报告
-> 再跑 500 条
```

只有当 30 条 smoke 能明显接近 gold 风格时，才允许进入 500 条正式实验。
