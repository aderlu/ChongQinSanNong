# 2026-05-15 B/C Baseline 组真实问诊质量修复记录

## 基准不变声明

本次修复没有修改 `2026-05-14-wiki-grounded-baseline-validation-design.md` 定义的实验分组、比较口径和字段基准。

对比表字段仍保持：

- 3 个比较键：`run_id`、`case_seed_id`、`baseline_group`
- 51 个样本与评估字段
- 总字段数：54

代码中已增加单测锁定该契约：

- `STANDARD_SAMPLE_FIELDS == 51`
- `COMPARISON_KEY_FIELDS == ["run_id", "case_seed_id", "baseline_group"]`
- `STANDARD_COMPARISON_FIELDS == 54`

## 原问题

上一轮 B/C 组存在两个主要问题：

1. LLM 偶发返回数组、对象或分字段结构，代码端没有充分清洗，导致 `assistant_answer` 中泄漏 dict/list 风格文本。
2. B/C 回答虽然有临床含义，但经常使用“提示可能存在、重点考虑、不能排除、常见于”等自然表达，旧 QA gate 对这些表达识别不足，导致临床判断或鉴别方向误判偏高。

这些问题会造成：

1. 最终 CSV 的 `assistant_answer` 不像真实兽医自然回答，影响与 Wiki 组公平比较。
2. 自动验收报告把合格临床表达误判为失败，或者放过结构化文本泄漏。
3. 正式 500 条批量运行时，少量异常输出会污染整体统计。

## 修改内容

### 1. B/C prompt 约束增强

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\baseline_validation\generate_baseline_groups.py`

调整内容：

- 明确要求 `question` 必须是普通字符串。
- 明确要求 `clinical_answer` 必须是完整自然段字符串。
- 禁止返回数组、对象、Markdown 表格或分字段清单。
- 要求回答开头给出明确临床判断，例如“首先需要考虑/需要重点警惕”。

预期效果：

- 降低 B/C 组 dict/list 风格泄漏。
- 让 no-wiki 和 metadata-only 组也具备“真实养殖户问诊 + 临床式回答”的最低质量。

### 2. LLM payload 文本规范化

新增/更新函数：

- `compact_text`
- `normalize_text_value`
- `first_present`

处理逻辑：

- 如果 LLM 返回字符串，直接压缩空白。
- 如果返回 list，递归拼接成自然文本。
- 如果返回 dict，优先抽取 `clinical_answer`、`answer`、`text`、`initial_direction`、`differential`、`field_actions`、`followup_questions` 等文本字段，再拼接。
- 如果仍检测到结构化泄漏，则回退到安全 fallback。

解决的问题：

- 防止 Python/JSON 对象字符串直接进入 `assistant_answer`。
- 保证 B/C 的最终 CSV 字段仍是自然语言，而不是结构化残片。

### 3. B/C 回答质量兜底

新增函数：

- `ensure_baseline_answer_quality`

处理逻辑：

- 若回答缺少显性鉴别方向，则补充“鉴别上还要把感染性疾病、转群或温差应激、饲料饮水问题这几类分开看。”
- 若回答缺少现场动作，则补充“现场先把明显病弱猪隔开，检查通风、温度、饮水和饲料变化，连续观察采食和死亡变化。”
- 兜底补充会插入在追问前，避免出现“？。鉴别上……”这类不自然拼接。

注意：

- 该兜底只补通用临床排查和低风险现场动作。
- 不新增 Wiki anchors。
- 不伪造 fact/source/page/rule。
- 不改变 B/C 组 `source_trust` 和 `evidence_coverage=unverified` 的实验定位。

### 4. QA gate 表达识别补充

涉及文件：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\pipeline\baseline_validation\qa_realism_gate.py`

调整内容：

- 临床判断识别新增：`重点考虑`、`需要重点警惕`、`提示可能`、`不能排除`、`风险较高`。
- 鉴别方向识别新增：`同时要考虑`、`常见于`、`与...鉴别`、`不排除`。
- 现场动作识别新增：`检查.*通风`。

原因：

- 这些是兽医临床回答中常见的自然表达，不应被误判为缺少临床判断或鉴别方向。

## 测试与验证

### 单元测试

命令：

```powershell
py -m pytest ai-\tests\test_real_farmer_clinical_qa_generation.py -q
```

结果：

- 9 passed

新增测试覆盖：

- 54 字段对比契约不变。
- B/C dict/list payload 会被规范化为自然文本。
- B/C 缺鉴别/现场动作时会自动补充低风险临床兜底句。

### 编译检查

命令：

```powershell
py -m py_compile tools\pipeline\baseline_validation\generate_baseline_groups.py tools\pipeline\baseline_validation\qa_realism_gate.py
```

结果：

- 通过

### B/C 30 条真实 LLM smoke

运行 ID：

- `20260515_real_farmer_clinical_bc_fix2_30_v1`

产物：

- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\generated_samples\no_wiki_group_samples_20260515_real_farmer_clinical_bc_fix2_30_v1.jsonl`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\generated_samples\metadata_only_group_samples_20260515_real_farmer_clinical_bc_fix2_30_v1.jsonl`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_no_wiki_20260515_real_farmer_clinical_bc_fix2_30_v1.csv`
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\exports\baseline_validation\comparisons\baseline_comparison_metadata_only_20260515_real_farmer_clinical_bc_fix2_30_v1.csv`

生成层检查：

- no_wiki：30 rows，passed=true，结构化文本泄漏 0，假 evidence anchors 0，fact/source/page 泄漏 0
- metadata_only：30 rows，passed=true，结构化文本泄漏 0，假 evidence anchors 0，fact/source/page 泄漏 0

QA gate：

- no_wiki：passed=true
  - `query_hard_fail_rate`: 0.0%
  - `professional_leakage_rate_user_query`: 0.0%
  - `answer_hard_fail_rate`: 0.0%
  - `clinical_judgement_rate`: 100.0%
  - `differential_rate`: 100.0%
  - `field_action_rate`: 100.0%
- metadata_only：passed=true
  - `query_hard_fail_rate`: 0.0%
  - `professional_leakage_rate_user_query`: 0.0%
  - `answer_hard_fail_rate`: 0.0%
  - `clinical_judgement_rate`: 100.0%
  - `differential_rate`: 100.0%
  - `field_action_rate`: 100.0%

### B/C final10 拼接自然度复核

运行 ID：

- `20260515_real_farmer_clinical_bc_final10_v1`

检查结果：

- no_wiki：10 rows，QA gate passed=true，`answer_hard_fail_rate=0.0%`
- metadata_only：10 rows，QA gate passed=true，`answer_hard_fail_rate=0.0%`
- 未发现“？。鉴别上”这类不自然拼接。

## 结论

B/C 组本次修复后：

1. 保持 2026-05-14 设计文档的分组逻辑和 54 字段对比基准不变。
2. 真实 LLM 输出不会再把 dict/list 结构泄漏进 `assistant_answer`。
3. no_wiki 与 metadata_only 均能稳定产出真实养殖户问题和临床式回答。
4. B/C 仍然不伪造 Wiki 证据，`evidence_anchors=[]`、`evidence_coverage=unverified` 的 baseline 定位保持不变。

后续正式 500 条三组对比时，可以继续使用该生成逻辑；正式比较仍应走设计文档规定的通用问诊质量评估、grounding 审计和标准 54 字段 CSV 汇总。
