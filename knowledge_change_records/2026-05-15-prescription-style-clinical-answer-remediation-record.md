# 2026-05-15 临床式直接处置与处方化回答修复记录

## 背景问题

用户复核三组 30 条 CSV 后反馈：`assistant_answer` 质量仍不够，主要表现为：

1. 回答偏“风险提示 + 继续追问”，没有像临床兽医一样直接给出处置意见。
2. 缺少处方化治疗思路，只有隔离、通风、观察、送检等泛化建议。
3. 用户问“现在先怎么处理”，回答却把重点放在“还需要补哪些信息”。

这会导致生成数据虽然通过了之前的自然度、鉴别方向、现场动作门禁，但仍达不到实际问诊训练中需要的“真实临床回答”质量。

## 原因分析

排查后发现问题来自多层约束叠加。

### 1. Phase13 合约偏追问

原代码中：

- `required_consultation_moves` 包含 `ask_key_followups`
- `followup_question_count` 为 `1-3`
- `must_include_sections_semantically` 明确要求“最后只追问 1-3 个最关键问题”
- `prescription_policy` 对药名、剂量、疗程、休药期限制较强

结果：

- 模型会把“追问”视为必需动作。
- 回答天然会以“补信息/送检/联系兽医”收尾。
- 临床处置和处方化治疗被压缩为低风险动作。

### 2. Phase14 prompt 把用药边界写得过强

原代码中：

- 系统 prompt 写明“不得编造确诊、处方、剂量、休药期或监管执行结论”
- user prompt 写明“最后只问 1 到 3 个最关键问题”
- 对 L2 要求“只说明诊断支持点、限制和需要补充的问诊/检测信息”
- 对低 `prescription_support_level` 要求不得同时给药名、剂量、疗程或休药期

结果：

- 模型为了安全，倾向不写处方化建议。
- 回答变成“不能确诊 + 继续补信息 + 请兽医”。
- 即使有现场动作，也缺少护理、补液、抗菌药类别、禁忌和升级条件。

### 3. B/C 组 prompt 明确禁止执行性用药

原代码中：

- `generate_baseline_groups.py` 的 system prompt 写明“不得直接给出药物剂量、疗程、休药期...”
- user prompt 要求最后追问 1-3 个关键问题
- fallback 回答也写“不建议直接定药物剂量、疗程、休药期”

结果：

- no_wiki 和 metadata_only 组也不敢给处方化治疗框架。
- B/C 组回答更像保守问诊建议，不像临床处置。

### 4. QA gate 没有检查处方化治疗

原 QA gate 只检查：

- 真实养殖户问题
- 临床判断
- 鉴别方向
- 现场动作

没有检查：

- 是否给出处方化治疗思路
- 是否包含支持治疗、补液、电解质、抗菌药类别、禁忌、剂量/休药期边界
- 是否过早追问、用追问替代处置

结果：

- 低质量的“隔离 + 送检 + 追问”回答也能通过。

## 修改内容

### 1. Phase13：回答合约从“追问完整”改为“处置完整”

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase13_build_answer_skeletons.py`

修改点：

- 将 `ask_key_followups` 改为 `ask_optional_key_followups`
- 新增 `give_direct_clinical_management_plan`
- 新增 `give_prescription_style_plan_with_boundaries`
- 将 `followup_question_count` 从 `1-3` 改为 `0-2`
- 将 farmer visible followup policy 改为“先给完整临床处置方案，追问最多 0-2 个且只能放在末尾补充”
- `clinical_answer_contract_for` 中新增要求：
  - 给出隔离、保温/降温、饮水补液、饲料调整、消毒和观察指标
  - 给出处方化治疗思路
  - 给出支持治疗、疑似细菌继发感染时的抗菌药类别、腹泻/脱水护理、禁用或慎用事项
  - 追问不能替代处置方案

解决效果：

- 生成器不再把追问当作主回答。
- 模型会先输出临床处置方案，再少量补问。

### 2. Phase14：Wiki 组 prompt 增加直接处置和处方化治疗

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\phase14_generate_two_stage_samples.py`

修改点：

- stage2 prompt 从“判断边界、建议补充信息”改为“临床判断、处置方案、处方化治疗思路、风险边界”
- L2 不再只说明“需要补充问诊/检测信息”，而是必须给出现场临床处置、护理和处方化治疗思路
- `clinical_generation_system_prompt` 从禁止“处方”改为：
  - 可以给出处方化治疗框架和药物类别建议
  - 不得编造最终确诊、精确剂量、休药期或监管执行结论
- clinical generation requirements 新增：
  - 必须给现场处理方案
  - 必须给处方化治疗思路
  - 支持治疗、补液/电解质水、保温/降温
  - 疑似细菌继发感染时给抗菌药类别
  - 缺少体重、产品标签和现场确认时不编造精确 mg/kg、疗程或休药期
- fallback `default_clinical_answer` 新增处方化段落：
  - 清洁饮水
  - 口服补液盐/电解质水
  - 保温或降温
  - 现场兽医确认后选择标签允许的抗菌药类别
  - 禁止自行混用多种抗生素、退烧药或激素

解决效果：

- Wiki 组回答从“分诊式建议”转为“临床处置 + 治疗框架”。
- 保持 Wiki 证据边界，不伪造精确剂量和监管结论。

### 3. B/C：baseline 组 prompt 与兜底逻辑增加处方化框架

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\baseline_validation\generate_baseline_groups.py`

修改点：

- 新增 `BASELINE_PRESCRIPTION_STYLE_RE`
- `low_risk_answer` 新增：
  - 支持治疗
  - 口服补液盐/电解质水
  - 保温/降温
  - 细菌继发感染时使用对猪适用、标签允许的抗菌药类别
  - 剂量、疗程、休药期按产品标签、体重和现场兽医医嘱执行
  - 避免自行混用抗生素、退烧药或激素
- `ensure_baseline_answer_quality` 新增处方化兜底句：
  - 若回答缺少处方化治疗关键词，则补充支持治疗和抗菌药类别边界
- prompt 从“不得直接给出药物剂量、疗程...”改为：
  - 必须给出处方化处理框架
  - 不得编造精确剂量、休药期和监管执行结论
- user prompt 新增处方化要求：
  - 支持治疗
  - 补液/电解质水
  - 保温/降温
  - 疑似细菌继发感染时的抗菌药类别
  - 禁忌和升级条件

解决效果：

- no_wiki 和 metadata_only 不再只是问诊建议，也能直接给临床处置框架。
- 仍保持 baseline 定位：不伪造 Wiki anchors，不伪造检测/剖检事实。

### 4. QA gate：新增处方化回答验收

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\baseline_validation\qa_realism_gate.py`

修改点：

- 新增 `PRESCRIPTION_STYLE_RE`
- 新增 failure：
  - `missing_prescription_style_plan`
  - `followup_before_direct_plan`
- 新增指标：
  - `prescription_style_count`
  - `prescription_style_rate`
- 新增阈值：
  - strict: 90%
  - non-strict: 60%

解决效果：

- 以后只“隔离/观察/追问”的回答会被拦截。
- 必须包含支持治疗、补液、电解质、抗菌药类别、标签/剂量/疗程/休药期边界等处方化处理元素。

### 5. 测试更新

涉及文件：

- `D:\XF-ChongQin\ai-\tests\test_real_farmer_clinical_qa_generation.py`

新增/更新测试：

- Phase13 合约要求 `followup_question_count == "0-2"`
- fallback clinical answer 必须包含处方化元素
- B/C answer fallback 必须补充处方化处理
- QA gate 必须拒绝“只有追问、无处方化处理”的回答
- QA gate 必须接受“临床判断 + 鉴别 + 现场动作 + 处方化处理”的回答

测试结果：

- `10 passed`

## 验证结果

### 编译检查

命令：

```powershell
py -m py_compile phase13_build_answer_skeletons.py phase14_generate_two_stage_samples.py generate_baseline_groups.py qa_realism_gate.py
```

结果：

- 通过

### 真实 LLM smoke

运行 ID：

- `20260515_prescription_style_smoke5_v1`

执行内容：

- Wiki 组完整真实链路：Phase13/14/14b/15/18/16 + baseline general judge + grounding
- no_wiki 组真实生成 + 真实通用裁判 + grounding
- metadata_only 组真实生成 + 真实通用裁判 + grounding

行数：

- Wiki：5
- no_wiki：5
- metadata_only：5
- 标准对比表：15 行 x 54 字段

CSV 产物：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_standard_20260515_prescription_style_smoke5_v1.csv`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_wiki_20260515_prescription_style_smoke5_v1.csv`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_no_wiki_20260515_prescription_style_smoke5_v1.csv`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_metadata_only_20260515_prescription_style_smoke5_v1.csv`

### 新 QA gate 结果

Wiki：

- `passed`: true
- `answer_hard_fail_rate`: 0.0%
- `clinical_judgement_rate`: 100.0%
- `differential_rate`: 100.0%
- `field_action_rate`: 100.0%
- `prescription_style_rate`: 100.0%

no_wiki：

- `passed`: true
- `answer_hard_fail_rate`: 0.0%
- `clinical_judgement_rate`: 100.0%
- `differential_rate`: 100.0%
- `field_action_rate`: 100.0%
- `prescription_style_rate`: 100.0%

metadata_only：

- `passed`: true
- `answer_hard_fail_rate`: 0.0%
- `clinical_judgement_rate`: 100.0%
- `differential_rate`: 100.0%
- `field_action_rate`: 100.0%
- `prescription_style_rate`: 100.0%

## 抽样观察

Wiki 组样本已出现以下临床式内容：

- “现场现在可以先做的措施包括”
- “保证清洁饮水，可添加适量电解质水”
- “暂停投喂精料，改为易消化的稀粥或青绿饲料”
- “在治疗思路上，现阶段以支持和对症为主”
- “若后续有细菌感染迹象，可在现场兽医确认后选用适用于猪、且标签允许的广谱抗菌药物类别”
- “不能给出具体的剂量、疗程和休药期，必须由现场兽医根据情况决定”

B/C 组样本已出现：

- “支持治疗”
- “电解质水”
- “广谱抗生素类制剂”
- “严格按标签要求操作”
- “避免使用可能加重肝肾负担的药物”

## 仍需注意

1. 本次不编造精确 mg/kg、疗程和休药期，因为当前样本没有体重、产品标签、现场诊断和药品说明书证据。
2. 新目标是“处方化治疗框架”，不是无依据精确处方。
3. 个别 B/C 组回答可能仍出现兜底句位置略生硬，例如“追问后追加鉴别句”，后续正式 30/500 条前可继续优化句子插入位置。
4. 5 条 smoke 不能代表全量稳定性，建议下一步跑 30 条新口径三组 CSV 复核。

## 清理与乱码防护

- 本次清理了测试/编译产生的 `__pycache__` 临时目录。
- 未删除任何 CSV、JSONL、报告或正式产物。
- 新增/修改文件均使用 UTF-8，无 BOM。
- 测试中保留了常见乱码 token 检查。

## 结论

本次修复已把回答目标从“问诊追问/风险提示”升级为“临床式直接处置 + 处方化治疗框架 + 安全边界”。真实 LLM 5 条 smoke 显示三组均能产出处方化回答，并通过新增 QA gate 的 `prescription_style_rate` 检查。
