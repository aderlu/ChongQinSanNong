# 猪病弱 Wiki 300 条有效数据生产方案

更新时间：2026-05-07

## 目标

在猪病 wiki 尚未完全建设完成的情况下，先生成一批可用于模型初步测试、模型初步校验和弱监督微调流程验证的猪病问答数据。

本方案优先保证：

- 问答场景真实，像养殖户实际提问。
- 诊断与症状相互匹配。
- 处方/处理方向与疾病相互印证。
- 不生成明显错误或危险的治疗建议。
- 输出结构对齐鸡病生产 CSV。
- 生成、评审、过滤、导出流程完整。

本方案暂不追求：

- 每条回答都有权威来源引用。
- 每条回答都有 PDF 页码。
- 中国兽药标签级剂量、疗程和具体休药期。
- 可直接作为临床处方依据。

## 当前验证结论

### 30 条试跑

命令：

```powershell
python scripts\run_swine_weak_wiki_production_2026_05_07.py --limit 30 --parallel 6 --answer-max-tokens 1500 --judge-max-tokens 950
```

结果：

- 生成：30 条
- 有效：22 条
- 有效率：73.3%
- 平均分：84.17
- pass/review/reject：22 / 6 / 2
- fatal risk：2 条
- 具体剂量错误：0 条
- 具体休药期错误：0 条

### 100 条试跑

命令：

```powershell
python scripts\run_swine_weak_wiki_production_2026_05_07.py --limit 100 --parallel 8 --answer-max-tokens 1500 --judge-max-tokens 950
```

输出：

- 全量 CSV：`results/swine_weak_wiki_production/swine_disease_dataset_production_20260507_140257.csv`
- 有效 CSV：`results/swine_weak_wiki_production/swine_disease_dataset_production_20260507_140257_valid.csv`
- 拒绝/复核 CSV：`results/swine_weak_wiki_production/swine_disease_dataset_production_20260507_140257_rejects.csv`
- 质量报告：`results/swine_weak_wiki_production/swine_disease_dataset_production_quality_report_20260507_140257.md`

结果：

- 生成：100 条
- 有效：71 条
- 有效率：71.0%
- 平均分：85.0
- 有效子集平均分：87.08
- pass/review/reject：71 / 11 / 18
- fatal risk：18 条
- 具体剂量错误：0 条
- 具体休药期数字错误：0 条
- 有效子集覆盖疾病：54 种
- 全量覆盖疾病：73 种

判断：弱 wiki 方案有效，可以扩展到 300 条。当前有效率约 71%，因此应超采样生成 450-500 条候选，再取通过评估的 300 条。

## 为什么加入双评审和仲裁

当前 100 条结果里有一个明显现象：部分样本被本地别名规则硬拒绝，但 judge 实际给了 88-92 分；也有部分低频病种被 judge 判为 review，但可能只是目标疾病本身证据稀疏或场景特异性弱。

加入双评审和仲裁可以解决三类问题：

- 减少单 judge 偶然误杀。
- 减少单 judge 对“缺少具体药物/剂量”的偏好影响。
- 对高分但本地规则触发、两个 judge 分歧较大、fatal 判断不一致的样本做最终裁决。

因此推荐从“单评审生产线”升级为：

```text
生成 answer
  -> judge_a 严格评估
  -> judge_b 独立评估
  -> 本地硬规则扫描
  -> 分歧样本进入 arbiter
  -> 生成 final_label
  -> 导出 full / valid / review / reject
```

## 双评审设计

### judge_a

偏临床一致性：

- 症状是否支持目标疾病。
- 诊断是否包含必要鉴别。
- 病理逻辑是否合理。
- 问答场景是否真实。

建议模型：`judge_swine_ernie45_turbo32k`

### judge_b

偏安全和数据可用性：

- 处理方向是否安全。
- 是否有重大疫病普通治疗替代处置。
- 是否有错误剂量、具体休药期或上市承诺。
- 是否适合作为训练/测试数据。

建议模型：`judge_swine_hunyuan_turbos` 或 `judge_swine_hunyuan20_instruct`

### 评审输出字段

每个 judge 必须输出：

```json
{
  "total_score": 88,
  "diagnosis_accuracy": 28,
  "pathology_logic": 20,
  "prescription_safety": 22,
  "data_quality": 18,
  "fatal_risk": false,
  "final_label": "pass",
  "summary": "...",
  "weaknesses": ["..."],
  "improvement_actions": ["..."]
}
```

## 仲裁触发条件

满足任一条件时进入 arbiter：

- `judge_a.final_label != judge_b.final_label`
- `abs(judge_a.total_score - judge_b.total_score) >= 8`
- `judge_a.fatal_risk != judge_b.fatal_risk`
- 本地硬规则触发，但两个 judge 均给出 `pass`
- 两个 judge 均 pass，但任一分项低于 18 分
- 样本涉及非洲猪瘟、口蹄疫、猪瘟、布鲁氏菌病、狂犬病、重大中毒、临近出栏用药等高风险场景

## 仲裁输出字段

arbiter 输出：

```json
{
  "arbiter_final_label": "pass|review|reject",
  "arbiter_final_score": 86,
  "arbiter_fatal_risk": false,
  "arbiter_agreed_with_judge": "a|b|neither",
  "arbiter_reason": "...",
  "required_fix": "..."
}
```

## 最终标签合成规则

### 直接 pass

必须同时满足：

- judge_a = pass
- judge_b = pass
- 两者分数均 >= 80
- 两者 fatal_risk 均为 false
- 本地硬规则无 fatal
- 目标疾病或别名命中诊断
- 不含具体剂量
- 不含具体休药期数字

### 进入 review

满足任一：

- 一个 judge pass，另一个 judge review
- 两个 judge 都 review
- 平均分 >= 75，但存在轻微逻辑不足
- 低频疾病特异性不足，但处理方向安全
- 场景真实，但鉴别诊断不够完整

### 直接 reject

满足任一：

- 任一 judge 判定 fatal_risk=true，且 arbiter 同意
- 目标疾病明显跑偏
- 处方与疾病相冲突
- 重大疫病建议普通治疗观察
- 出现具体剂量或具体休药期承诺
- 物种错误
- user_query 不像真实养殖户提问

## 本地硬规则

脚本应自动识别并拒绝或触发仲裁：

- 物种不是猪。
- 诊断未命中目标疾病或别名。
- 出现具体剂量，例如 `10mg/kg`、`5g/L`。
- 出现具体休药期数字。
- 非洲猪瘟、口蹄疫、猪瘟、水疱病、布鲁氏菌病等被建议普通治疗观察。
- 临近出栏场景中出现“可以直接卖”“不用管休药期”等表述。
- 中毒类场景中建议继续饲喂可疑饲料。
- 人兽共患病场景中完全忽略人员防护、隔离或送检边界。

## 生产 300 条的推荐参数

### 单评审版本

根据 100 条试跑的 71% 有效率，建议生成 500 条：

```powershell
python scripts\run_swine_weak_wiki_production_2026_05_07.py --limit 500 --parallel 8 --answer-max-tokens 1500 --judge-max-tokens 950
```

预期有效：

```text
500 * 0.71 = 355 条
```

### 双评审 + 仲裁版本

双评审会更严格，有效率预计下降到 55%-65%，但质量更高。

建议生成 600 条候选：

```powershell
python scripts\run_swine_weak_wiki_production_2026_05_07.py --limit 600 --parallel 8 --answer-max-tokens 1500 --judge-max-tokens 950 --dual-judge --arbiter
```

预期有效：

```text
600 * 0.55 = 330 条
600 * 0.65 = 390 条
```

如果脚本暂未实现 `--dual-judge --arbiter` 参数，则先使用单评审生产 500 条，再对 `*_valid.csv` 和高风险 `*_rejects.csv` 做二次复评。

## 输出文件建议

生产脚本应输出：

```text
swine_disease_dataset_production_YYYYMMDD_HHMMSS.csv
swine_disease_dataset_production_YYYYMMDD_HHMMSS_valid.csv
swine_disease_dataset_production_YYYYMMDD_HHMMSS_review.csv
swine_disease_dataset_production_YYYYMMDD_HHMMSS_rejects.csv
swine_disease_dataset_production_summary_YYYYMMDD_HHMMSS.json
swine_disease_dataset_production_quality_report_YYYYMMDD_HHMMSS.md
```

CSV 字段继续对齐鸡病生产结果：

- `judge_a_*`
- `judge_b_*`
- `needed_arbitration`
- `arbiter_*`
- `final_*`

## 有效样本判定标准

样本进入 `*_valid.csv` 必须满足：

- `species = 猪`
- `final_label = pass`
- `final_total_score >= 80`
- `final_fatal_risk = False`
- 目标疾病或别名在诊断中命中
- 不包含具体剂量
- 不包含具体休药期数字
- 重大疫病不得生成普通治疗替代处置
- 处方/处理方向与疾病类型一致

第一批数据不要求药品剂量，所以处方建议写成：

```text
治疗方向 + 管理措施 + 采样送检 + 禁忌边界 + 休药期边界说明
```

## 是否可用于训练和微调

### 可用于

- 模型初步测试。
- Prompt 回归测试。
- 诊断-处理方向一致性评估。
- 弱监督 SFT 流程验证。
- 小规模初步微调实验。

### 不建议直接用于

- 高可信正式医疗/兽医模型微调。
- 真实临床处方生成能力训练。
- 剂量、疗程、休药期能力训练。
- 无人审的生产级知识注入。

原因：

- 当前是弱 wiki 背景，不是逐条权威证据锚定。
- 没有中国兽药标签级处方来源。
- 处方字段训练的是安全处理方向，而非可执行处方。
- 仍需抽样人工复核。

## 质量抽查建议

生成 500-600 条候选后，建议人工抽查：

- 从 `*_valid.csv` 随机抽 30 条。
- 从 `*_review.csv` 抽 20 条。
- 从 `*_rejects.csv` 抽 20 条，确认过滤原因是否合理。

重点看：

- 非洲猪瘟、口蹄疫、猪瘟是否没有普通治疗建议。
- 布鲁氏菌病是否有人兽共患和暂停配种边界。
- 腹泻病是否能区分病毒性、细菌性、寄生虫性方向。
- 呼吸道病是否避免无依据全群乱用药。
- 休药期是否没有具体承诺。
- 低频病毒病是否被过度诊断。

## 后续升级路径

第一阶段：弱 wiki + 单评审，生成 300 条测试数据。

第二阶段：弱 wiki + 双评审 + 仲裁，生成 300 条更高质量测试/弱监督数据。

第三阶段：补齐猪病 wiki 的诊断、鉴别诊断、采样、用药边界。

第四阶段：重新跑 source-aware 版本，增加引用和更严格的证据门禁。

第五阶段：加入人工复核，生成可用于正式微调的高可信版本。

## 结论

可以加入双评审和仲裁，而且建议加入。  

基于当前 30 条和 100 条试跑结果，弱 wiki 方案本身有效。若保持单评审，建议生成 500 条候选并取 300 条 valid；若加入双评审和仲裁，建议生成 600 条候选并取 300 条 valid。双评审版本成本更高、速度更慢，但流程更完整，误杀和漏判都会更少，更适合作为后续正式微调流程的过渡版本。
