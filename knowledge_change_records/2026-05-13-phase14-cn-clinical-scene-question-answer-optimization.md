# Phase14 中文真实问诊场景问答优化记录

- 日期：2026-05-13
- 目标：将 Wiki-first 样本生成中的问题与回答，从“系统任务句/翻译腔”改为更符合中国猪场真实咨询场景的规范中文表述。

## 之前存在的问题

此前 Phase14 的 `question_for()` 直接生成诸如：

- `Summarize core knowledge for DIS-002 using registered Wiki evidence.`
- `Explain the diagnosis-support points and limits for DIS-007 using registered Wiki evidence.`

这类句子更像内部任务描述，不像中国猪场里场长、技术员、驻场兽医或咨询兽医之间的真实问答场景。

同时，Stage1/Stage2 提示词没有明确要求“必须生成中国猪场咨询语境下的自然中文回复”，因此真实 API 生成结果容易出现：

- 系统任务句口吻
- 翻译腔
- 机械复述实体 ID
- 不够像真实现场问诊/咨询表达

## 本次修改

### 1. 修改 Phase14 问题生成逻辑

文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase14_generate_two_stage_samples.py`

更新内容：

- `PROMPT_VERSION` 从 `phase14.two_stage.v2` 升级到 `phase14.two_stage.v3_cn_clinical`
- 新增 `entity_name_for()`，优先从结构化 claim 中提取中文实体名，而不是直接用 `DIS-xxx`
- 重写 `question_for()`，将问题改写成真实中文猪场咨询场景，例如：
  - 猪场现场咨询
  - 如果怀疑某病
  - 现有资料能支持哪些判断
  - 哪些内容还不能直接下结论

### 2. 修改 Stage1/Stage2 提示词

同文件中同步更新：

- `stage_1_system_prompt()`
- `stage_1_user_prompt()`
- `stage_2_system_prompt()`
- `stage_2_user_prompt()`

新增约束：

- 输出必须像中国大陆猪场真实咨询回复
- 不得写成任务说明句、翻译练习句、系统摘要句
- 除结构化引用字段外，正文应使用自然、规范、专业中文
- 避免 `Summarize core knowledge`、`using registered Wiki evidence` 等系统化表述

### 3. 修改默认结构化回答的边界表述

同文件中同步将 `structured_answer()` 的默认边界句改成更接近真实中文咨询答复的表述，减少英文任务腔。

### 4. 补充测试

文件：

- `D:\XF-ChongQin\ai-\tests\test_swine_wiki_first_generation_pipeline.py`

新增与更新内容：

- 断言 prompt version 为 `phase14.two_stage.v3_cn_clinical`
- 断言生成问题中不再包含：
  - `Summarize core knowledge`
  - `using registered Wiki evidence`
- 断言问题中包含更像真实咨询场景的中文提示词
- 新增 `test_phase14_question_for_uses_realistic_cn_clinical_scene()`

## 预期效果

- 样本问题将更像中国猪场真实问诊/咨询问题
- 回答更接近驻场兽医、咨询兽医对养殖场的规范回复口吻
- 更适合作为中文兽医问答 SFT 数据
- 降低“系统任务句”和“翻译腔”对训练样本质量的负面影响

## 后续建议

- 基于新 prompt 重新生成一批真实 API 样本
- 重点抽查 L2/L3/L4 的中文问答真实性
- 如果需要，可继续把不同能力层的问题模板细化为：
  - 场长提问
  - 技术员提问
  - 驻场兽医会诊
  - 监管咨询边界场景
