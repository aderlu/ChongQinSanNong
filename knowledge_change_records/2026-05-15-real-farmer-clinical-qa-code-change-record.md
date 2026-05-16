# 2026-05-15 真实养殖户问诊与临床式回答代码整改留痕

## 一、整改范围

本次按执行文档 `2026-05-15-real-farmer-clinical-qa-remediation-runbook.md` 落地代码修改，目标是解决 baseline Wiki 组中 `user_query` 和 `assistant_answer` 质量无效的问题。

涉及代码：

```text
ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/consultation_case_variables.py
ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase13_build_answer_skeletons.py
ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py
ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/baseline_validation/generate_baseline_groups.py
ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/baseline_validation/qa_realism_gate.py
ai-/tests/test_real_farmer_clinical_qa_generation.py
```

## 二、修改一：真实养殖户 user_query 生成

### 之前存在什么问题

`consultation_case_variables.py` 中 `_MISSING_INFO` 和 `_FOLLOWUP_TOPICS` 直接包含专业术语：

```text
日龄和批次记录不全
发病比例和死亡数还没统计清楚
免疫记录一时找不到
还没送实验室检测
还没做剖检
是否做过剖检或检测
```

`build_case_user_query()` 还会固定追加：

```text
还需要我补哪些信息，比如...
```

### 会产生什么结果

生成的用户问题不像真实养殖户，而像问诊采集表或评估模板。旧 500 条 Wiki 表中：

- `还需要我补哪些信息` 命中 100%。
- `剖检` 命中 66.2%。
- `发病比例` 命中 68.0%。
- `实验室检测` 命中 43.6%。

### 修改了什么代码

在 `consultation_case_variables.py` 中：

1. 新增内部专业缺口字段：

```python
_CLINICAL_INFORMATION_GAPS = [
    "age_stage_unknown",
    "affected_count_unknown",
    "mortality_count_unknown",
    "vaccination_history_unknown",
    "recent_medication_unknown",
    "necropsy_not_done",
    "laboratory_test_not_done",
]
```

2. 将用户可见缺失信息改为口语表达：

```python
_FARMER_VISIBLE_UNCERTAINTY = [
    "还没来得及细数到底多少头不对劲",
    "只知道今天比昨天又多了几头",
    "死了几头还没完全弄清楚原因",
    ...
]
```

3. 将 `_FOLLOWUP_TOPICS` 改成养殖户听得懂的问题：

```text
这批猪大概多大
大概几头不对劲、死了几头
最近有没有换料、转栏、降温或新进猪
```

4. 删除固定尾巴：

```text
还需要我补哪些信息，比如...
```

5. 新增自然结尾模板：

```text
这大概是咋回事？现在先咋处理？
这种情况严不严重，会不会越传越多？
我怕是大病，先要不要隔开？
```

### 修改后解决了什么

- 普通养殖户问题不再主动说“实验室检测、剖检、发病比例、检测结果”。
- `clinical_information_gaps` 保留内部专业缺口，不丢失后续临床推理和评估信息。
- `user_query` 更接近真实咨询：现场症状 + 时间变化 + 担心 + 求助。

### 预计更新效果

下一批正式生成中：

- `还需要我补哪些信息` 应降为 0。
- 普通用户问题中专业词泄漏率应低于 12%。
- 问题相似度下降，真实感提升。

## 三、修改二：Phase13 问答骨架改为临床 gold 风格

### 之前存在什么问题

`phase13_build_answer_skeletons.py` 中 required followups 直接使用专业清单：

```text
发病日龄/阶段
发病率和死亡率
采样或实验室检测结果
剖检或检测信息
检测或监管依据
```

`consultation_generation_contract` 要求：

```text
followup_question_count = 3-6
```

### 会产生什么结果

下游 Phase14 会把回答目标理解成“补资料 + 检测 + 送检 + 边界”，导致回答过宽泛，不像临床兽医判断。

### 修改了什么代码

1. 将 `required_followups` 改成口语化临床追问：

```text
这批猪大概多大、哪个阶段
大概几头有症状、死了几头
是突然一片起来还是零星慢慢增多
最近有没有换料、转栏、降温或新进猪
```

2. 将回答契约改为：

```python
"followup_question_count": "1-3"
"answer_style": "clinical_gold_style"
"must_include_clinical_judgement": True
"must_include_differential_directions": True
"avoid_generic_testing_boilerplate": True
```

3. 将 required moves 从单纯不确定性声明改为：

```text
give_initial_clinical_direction
explain_reasoning_from_user_scene
give_differential_directions
ask_key_followups
give_low_risk_next_steps
triage_or_testing_boundary
```

### 修改后解决了什么

- 骨架不再驱动模型机械罗列专业追问。
- 回答主目标从“审计安全”转为“临床判断 + 鉴别 + 现场动作”。
- 追问数量降低到 1-3 个，更符合真实兽医问诊。

### 预计更新效果

- `assistant_answer` 中“只补资料/送检”的泛化回答减少。
- `clinical_judgement_rate` 和 `differential_rate` 提升。

## 四、修改三：Phase14 生成提示词和 fallback 重写

### 之前存在什么问题

`phase14_generate_two_stage_samples.py` 中 prompt 要求：

```text
必须给出 2 到 4 个低风险动作，例如联系兽医采样送检
必须提出 3 到 6 个关键追问
```

`default_clinical_answer()` 固定包含：

```text
记录日龄、发病头数、死亡变化
剖检、采样和实验室检测
```

### 会产生什么结果

即使 LLM 没有故意写坏，prompt 和 fallback 也会把回答拉回旧模板：

- 不能确诊。
- 补齐资料。
- 联系兽医。
- 采样送检。
- 缺少具体临床倾向和鉴别诊断。

### 修改了什么代码

1. `question_for()` 改掉审计式内部问题，避免出现：

```text
现有资料能确认哪些可靠信息
还需要补哪些关键资料
哪些事需要等检测或现场兽医确认
```

改为：

```text
现在先怎么稳住，病弱猪要不要隔开？
会不会传得很快，先做哪几件事？
```

2. `known_limitations` 改为自然表达：

```text
用户只提供了现场观察和部分背景，很多细节还没有完全说清。
```

3. `clinical_generation_user_prompt()` 新增强约束：

```text
先给初步临床方向和严重程度
解释依据
给 2 到 3 个鉴别方向
给现场动作
最后只问 1 到 3 个最关键问题
不得只写“无法确诊、建议送检、补齐资料、联系当地兽医”
```

4. `default_clinical_answer()` 改为临床式 fallback：

```text
从你说的症状来看，先按猪群里可能继续扩散的情况处理。
更像感染性疾病、环境应激或饲料饮水问题叠在一起。
鉴别上优先把呼吸道/消化道感染、转群或温差应激、饲料饮水异常分开。
现场先隔开病弱猪、检查通风温度饮水饲料、观察采食饮水和死亡变化。
```

### 修改后解决了什么

- fallback 不再把每条回答拖回“剖检、采样、实验室检测”模板。
- 主 prompt 明确要求临床判断和鉴别方向。
- 检测/兽医介入被保留为必要时的边界和后续动作，而不是所有回答的主干。

### 预计更新效果

- 回答会更接近 gold 数据的 `diagnosis + prescription` 风格。
- 泛化模板率下降。
- 回答更适合训练问诊 agent。

## 五、修改四：B/C baseline 组生成同步整改

### 之前存在什么问题

`baseline_validation/generate_baseline_groups.py` 的 `low_risk_answer()` 同样使用旧模板：

```text
补齐日龄、发病比例、死亡变化、免疫史、用药史和检测结果
尽快联系现场兽医或检测机构，按症状采集合适样本做实验室检测
```

### 会产生什么结果

B/C 组即使真实调用 LLM，也可能因为 fallback 和 prompt 目标不当生成宽泛答案，导致三组比较不公平。

### 修改了什么代码

1. `low_risk_answer()` 改为临床式 baseline fallback：

- 初步判断为群体性异常。
- 说明如果担心某病，应看是否成片增多、死亡加快、采食饮水下降。
- 鉴别感染性疾病、转群/温差应激、饲料饮水问题。
- 给出隔开病弱猪、检查通风饮水饲料、观察变化、现场兽医介入。
- 最多追问两点。

2. `build_prompt()` 增加要求：

```text
question 要像真实养殖户咨询
不要出现“还需要我补哪些信息”
不要主动说实验室检测、剖检、发病比例、检测结果
clinical_answer 必须先给初步方向和严重程度，再说明依据，再给鉴别方向和现场动作
```

### 修改后解决了什么

- B/C 组与 Wiki 组使用同一质量目标。
- baseline 不再天然被旧模板污染。
- 后续三组比较更公平。

## 六、修改五：新增 QA realism gate

### 新增文件

```text
ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/baseline_validation/qa_realism_gate.py
```

### 为什么新增

之前只有结构验收，缺少内容质量闸门。旧 500 条虽然 54 字段齐全，但问答质量明显无效。

### 新增能力

脚本可读取比较 CSV，输出 JSON 报告，检查：

1. `user_query` 硬失败：

```text
还需要我补哪些信息
是否做过剖检或检测
猪场兽医咨询：
现有资料能确认
source=
fact=
rule=
DIS-
```

2. 普通问题专业词泄漏：

```text
实验室检测
剖检
发病比例
检测结果
采样送检
```

3. `assistant_answer` 质量：

- 是否有临床判断。
- 是否有鉴别方向。
- 是否有现场动作。
- 是否编造检测阳性或剖检结果。
- 是否追问过多。

4. 批量指标：

```text
query_hard_fail_rate
answer_hard_fail_rate
professional_leakage_rate_user_query
generic_answer_rate
clinical_judgement_rate
differential_rate
field_action_rate
duplicate_user_query_extra_count
duplicate_assistant_answer_extra_count
```

### 旧表验证结果

使用该脚本验证旧 500 条：

```text
qa_realism_gate_wiki_old_v2_quality_probe.json
```

关键结果：

```text
passed = false
query_hard_fail_rate = 100.0%
professional_leakage_rate_user_query = 100.0%
answer_hard_fail_rate = 98.8%
clinical_judgement_rate = 2.2%
differential_rate = 50.0%
field_action_rate = 87.8%
```

该结果证明新 gate 能识别旧问题。

## 七、修改六：新增测试

### 新增文件

```text
ai-/tests/test_real_farmer_clinical_qa_generation.py
```

### 覆盖内容

1. `user_query` 不再出现固定尾巴和专业词。
2. 内部 `clinical_information_gaps` 不泄漏到用户问题。
3. Phase13 contract 使用 `clinical_gold_style`，追问数量为 1-3。
4. Phase14 fallback 包含临床判断、鉴别方向和现场动作。
5. QA gate 能拒绝旧模板，能识别临床式样本。
6. 修改文件业务文本不包含常见乱码 token。

### 验证结果

```text
py -m pytest ai-/tests/test_real_farmer_clinical_qa_generation.py -q
6 passed
```

编译检查：

```text
py -m py_compile consultation_case_variables.py phase13_build_answer_skeletons.py phase14_generate_two_stage_samples.py generate_baseline_groups.py qa_realism_gate.py
passed
```

## 八、防乱码措施

本次采取措施：

- 所有文件使用 `apply_patch` 修改，避免 PowerShell 重定向写中文文件。
- 验证时使用 `py`，避免 WindowsApps `python.exe` 占位入口导致无输出失败。
- 新增测试检查业务文本中的常见乱码 token。
- 保留原有 `MOJIBAKE_RE` 检测器，不把检测器自身的乱码 token 当作正文污染。

## 九、冗余清理说明

本次没有删除历史 exports、issues、baseline_validation 产物，因为工作区已有大量未跟踪和已修改文件，无法确认归属，直接删除会有误伤风险。

本次新增的验证报告位于：

```text
ai-/knowledge/llm_wiki_swine_authoritative/exports/baseline_validation/reports/qa_realism_gate_wiki_old_v2_quality_probe.json
```

该报告用于证明旧 500 条确实不通过内容质量闸门，属于本次任务有效证据，不作为冗余删除。

## 十、下一步建议

1. 跑 30 条 smoke：

```text
20260515_real_farmer_clinical_smoke30_v1
```

2. 对三组分别运行 `qa_realism_gate.py`。
3. 人工抽检每组 10 条。
4. smoke 通过后再跑 500 条正式实验。
5. 正式验收必须同时看结构字段、疾病覆盖和 QA realism gate，不再只看 54 字段完整性。
