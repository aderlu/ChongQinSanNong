# 猪病 LLM Wiki 问题分类审计与后续优化清单

更新时间：2026-05-07

本文档汇总了前几轮围绕猪病 LLM Wiki、弱 wiki 数据生成、双评审仲裁、300 条猪病数据质量核查、以及猪病专属 schema 建设的讨论结论。目标是把当前知识库仍存在的问题分类沉淀下来，方便后续按模块继续补充、增强和验收。

## 1. 当前结论摘要

当前猪病 LLM Wiki 已经具备可运行基础：

- 已存在完整目录：`raw/`、`wiki/`、`exports/`、`issues/`。
- 已存在 73 个疾病页、76 个药物页、448 个规则页、153 个来源页、12 个症候群页、11 个规则卡、99 个主题页。
- 已导出 `knowledge_facts.json`、`disease_index.csv`、`rule_index.csv`、`drug_page_index.csv`、`source_index.csv`、`alias_index.csv` 等核心索引。
- 当前 facts 数量为 1465 条，其中大部分已有 source id 或 evidence status。
- 基于当前弱 wiki 和 LLM 能力，已经可以生成初步可用的猪病问答数据。

但它还没有达到“完全支撑正式训练/微调数据生产”的标准。核心问题是：知识库数量上已经成型，但疾病页正文、鉴别诊断、实验室诊断、药物边界、中国法规锚点和评估专用规则仍然不足。

因此当前定位应为：

- 可用于模型测试、流程验证、弱监督初步 SFT。
- 不宜直接作为权威兽医处方训练知识库。
- 不宜训练具体剂量、具体疗程、具体休药期。
- 若要稳定产出正式训练数据，需要继续补齐疾病页和评估规则。

## 2. 前几轮工作与讨论回顾

### 2.1 早期数据质量评估

最初检查了 `swine_qa_dataset_20260507_130918_usable_candidates.csv`，发现当前猪病 wiki 尚未完全建立，对生成结果的约束偏弱。结论是：原始候选数据不适合直接作为训练集，需要改成“生成 + 严格评估 + 过滤”的流程。

### 2.2 弱 wiki 快速生产方案

为了尽快得到初步 300 条有效猪病数据，讨论并确认了一个过渡方案：

- 不过度依赖尚未完整的猪病 wiki。
- 允许 LLM 用通用猪病知识生成真实场景。
- wiki 主要提供疾病名、边界、规则和部分背景。
- 评审流程负责把明显错误、危险建议、疾病不匹配、具体剂量、具体休药期过滤掉。

形成了 `SWINE_WEAK_WIKI_300_DATA_PLAN.md`。

### 2.3 30 条与 100 条试跑

试跑结果显示：

- 30 条试跑：有效率约 73.3%。
- 100 条试跑：有效率约 71.0%，有效子集平均分约 87.08。
- 说明弱 wiki 方案可以工作，但需要超采样。

### 2.4 双评审与仲裁

为了减少单一 judge 偏差，方案升级为：

```text
生成 answer
  -> judge_a 临床一致性评审
  -> judge_b 安全与数据可用性评审
  -> 本地规则扫描
  -> 高风险/分歧样本进入 arbiter
  -> final_label / final_score
  -> 导出 valid / rejects / raw audit
```

后续实现了二审和仲裁脚本，并修正了一个布尔解析问题：模型返回 `"False"` 字符串时不能被 Python 直接当作真值，否则会把大量合格样本误判为 fatal。

### 2.5 300 条数据生产与严格核查

最终流程：

- 先生成 500 条候选，一审通过 322 条。
- 二审仲裁后重算得到 204 条有效。
- 再补充生成 300 条候选，一审通过 203 条。
- 第二批二审仲裁后得到 113 条有效。
- 合并两批有效候选，共 317 条，最终取最高质量 300 条。

严格评估结果：

- 300 条均为 `final_label=pass`。
- 300 条均为 `final_fatal_risk=False`。
- 覆盖 66 种疾病。
- `case_id` 无重复。
- `user_query` 无重复。
- 问题 + 诊断 + 处方组合无重复。
- 具体剂量为 0 条。
- 有 2 条出现具体休药/观察时间数字，需要剔除或改写。

结论：300 条数据可用于模型测试和初步弱监督 SFT；若按严格 train-ready 口径，建议先处理 2 条 `withdrawal_period` 风险样本，得到 298 条更干净数据。

### 2.6 Schema 讨论

原有 `knowledge/schemas/llm_wiki_schema.yaml` 是鸡病 schema，不建议直接修改。更合理的做法是：

- 保留原 schema。
- 新增猪病专属 schema。
- 生成猪病数据时显式切换 schema。

已新增：

`knowledge/schemas/swine_llm_wiki_schema.yaml`

该 schema 专门约束猪病 wiki、疾病页、药物页、规则卡、生成契约、评估契约和审计字段。

## 3. 当前知识库资产盘点

### 3.1 目录与页面数量

当前 `knowledge/llm_wiki_swine_authoritative` 下主要内容：

| 类型 | 数量 | 说明 |
|---|---:|---|
| 疾病页 | 73 | 覆盖主要猪病，但大量页面仍偏短 |
| 药物页 | 76 | 主要为 evidence-only 安全边界页 |
| 规则页 | 448 | 数量较多，是当前强项 |
| 来源页 | 153 | 存在，但 frontmatter 规范不完全一致 |
| 主题页 | 99 | 多数较短，可作为检索辅助 |
| 症候群页 | 12 | 已有基础症候群导航 |
| 规则卡 | 11 | 数量不足，需要扩展 |
| synthesis 页 | 12 | 可辅助生成，但不是一手证据 |
| facts | 1465 | 已可用，但疾病级事实密度不足 |

### 3.2 导出物

当前 exports 已存在：

- `knowledge_facts.json`
- `disease_index.csv`
- `drug_page_index.csv`
- `rule_index.csv`
- `source_index.csv`
- `alias_index.csv`
- `syndrome_index.csv`
- `rule_card_index.csv`
- `synthesis_index.csv`

这说明检索与生成流程有基础数据入口。

## 4. 问题分类总览

当前问题可以分为 9 类：

1. Schema 与运行契约问题
2. 疾病页正文完整性问题
3. 疾病级事实密度问题
4. 实验室诊断与采样建议不足
5. 鉴别诊断体系不足
6. 防控、上报、禁售、禁运边界不足
7. 药物页与食品安全边界不足
8. 来源页和证据状态规范不足
9. 数据生成与评估流程仍需更强知识约束

下面逐类说明。

## 5. Schema 与运行契约问题

### 5.1 现有问题

原始 `llm_wiki_schema.yaml` 是鸡病 schema：

- `schema_name` 仍为 chicken。
- `default_path` 指向鸡病 wiki。
- `scope.applies_to` 指向鸡病目录和鸡病代码模块。

如果猪病生成流程继续复用该 schema，会出现几个问题：

- 运行契约和实际 wiki 根目录不一致。
- 猪病特有重大疫病、出栏用药、人兽共患等规则没有 schema 级约束。
- 评审字段和生成字段虽能复用，但缺乏猪病专属 hard block。
- 后续维护人员可能误以为猪病 wiki 已被鸡病 schema 充分约束。

### 5.2 当前进展

已新增：

`knowledge/schemas/swine_llm_wiki_schema.yaml`

该文件不修改原 schema，而是专门约束猪病 wiki。

### 5.3 后续需要做

- 在生成脚本中增加 `--schema knowledge/schemas/swine_llm_wiki_schema.yaml` 参数。
- 在检索和审计代码中读取 schema 的 `wiki_root.default_path`。
- 在评估脚本中读取 schema 的 hard blocks、rule cards、dataset_generation_contract。
- 增加 schema-check 脚本，至少校验：
  - 必需目录存在。
  - 必需 exports 存在。
  - 疾病页是否缺核心栏目。
  - train-ready 数据是否含具体剂量或具体休药期。

## 6. 疾病页正文完整性问题

### 6.1 当前问题

疾病页数量已有 73 个，但正文质量不均衡。

审计结果显示：

- 疾病页长度中位数约 2354 字。
- 38 个疾病页低于 2500 字。
- 很多页面仍是骨架页或半骨架页。
- 多数页面缺少可直接支撑生成和评估的细节。

核心栏目覆盖情况：

| 栏目 | 有来源化内容 | placeholder/缺口 |
|---|---:|---:|
| 传播途径 | 28 | 45 |
| 临床症状 | 31 | 42 |
| 剖检变化 | 26 | 47 |
| 实验室诊断 | 4 | 69 |
| 鉴别诊断 | 6 | 67 |
| 防控要点 | 3 | 70 |

这说明疾病页最影响生成质量的栏目仍然严重不足。

### 6.2 最短和最缺的疾病页

以下页面在审计中属于最短、缺口最多的一批，应优先补：

- `DIS-001-adenoviruses.md`
- `DIS-019-porcine-cytomegalovirus.md`
- `DIS-029-swinepox-virus.md`
- `DIS-031-retroviruses.md`
- `DIS-022-paramyxoviruses.md`
- `DIS-020-malignant-catarrhal-fever-ovine-herpesvirus-2.md`
- `DIS-044-gl-sser-s-disease.md`
- `DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md`
- `DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md`
- `DIS-063-metastrongylus-lungworms.md`
- `DIS-062-strongyloides-internal-parasites.md`
- `DIS-064-stephanurus-dentatus-kidney-worm.md`
- `DIS-050-staphylococcosis-exudative-epidermitis.md`
- `DIS-032-rabies-virus.md`
- `DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- `DIS-047-pasteurellosis.md`
- `DIS-053-tuberculosis.md`
- `DIS-042-edema-disease-e-coli.md`
- `DIS-056-external-parasites-lice.md`
- `DIS-061-trichuris-suis-internal-parasites.md`
- `DIS-060-ascaris-suum-internal-parasites.md`
- `DIS-054-miscellaneous-bacterial-infections.md`
- `DIS-034-togaviruses-getah-sagiyama-ross-river-eee.md`
- `DIS-040-colibacillosis.md`
- `DIS-051-streptococcosis-streptococcus-suis.md`

### 6.3 对生成数据的影响

疾病页正文不足会导致：

- 生成的用户问题容易模板化。
- 诊断理由容易只写常识，不够具体。
- 相似疾病容易混淆。
- 处置建议容易泛化为“隔离、送检、消毒”。
- judge 缺少疾病专属标准，只能用通用安全逻辑评分。
- 低频疾病更容易被误判为 review 或生成偏题。

### 6.4 修复标准

每个疾病页应补齐以下栏目：

- 概述
- 病原/病因
- 易感阶段和真实场景
- 传播途径与风险因素
- 临床症状
- 剖检变化
- 实验室诊断
- 鉴别诊断
- 治疗方向
- 防控要点
- 禁止边界
- 数据生成指导
- 评估 checklist
- evidence/source ids

建议验收标准：

- 每页最低 4000 字。
- 高频/高风险疾病页建议 6000 字以上。
- 每个疾病至少 20 条结构化 facts。
- 正式 train-ready 阶段建议每个疾病 40 条以上 facts。
- 核心栏目不能再是 placeholder。

## 7. 疾病级事实密度问题

### 7.1 当前问题

当前 `knowledge_facts.json` 有 1465 条 facts。数量看起来不少，但很多 facts 是：

- 规则类事实
- 主题类事实
- 诊断流程类事实
- 来源锚点
- 疾病目录属性

真正按疾病聚合、能支撑病例生成和评估的事实密度仍然不足。

典型问题：

- 每个疾病的 clinical facts 不均衡。
- 大量 predicate 只出现一次，不利于稳定检索。
- 诊断、采样、鉴别、防控 facts 数量明显不足。
- 中国法规 facts 只有少量疾病覆盖。

### 7.2 对生成数据的影响

事实密度不足会导致：

- 生成上下文命中弱相关 facts。
- 疾病页命中后缺少具体症状、样本、鉴别、处置边界。
- 评估无法用 facts 验证“诊断与处方是否相互印证”。
- 训练数据虽然看起来合理，但不能声明逐条来源锚定。

### 7.3 修复标准

建议每个疾病至少建立这些 fact 类型：

- disease_attribute
- causative_agent
- host_stage
- clinical_sign
- lesion
- transmission
- risk_factor
- diagnostic_sample
- diagnostic_test
- differential_diagnosis
- treatment_boundary
- control_measure
- reporting_boundary
- food_safety_boundary
- dataset_generation_guidance
- evaluation_rule

每个高频疾病建议：

- 40-80 条 facts。
- 至少 3 个 source ids。
- 至少 5 个鉴别诊断关系。
- 至少 3 个真实场景模板。

## 8. 实验室诊断与采样建议不足

### 8.1 当前问题

实验室诊断是当前最大缺口之一：

- 73 个疾病页中，仅约 4 个有来源化实验室诊断内容。
- 大多数疾病页缺少推荐样本。
- 缺少检测方法与结果解释。
- 缺少采样时机和送检对象。
- 缺少“检测阳性不等于致病”的解释边界。

### 8.2 对生成和评估的影响

没有实验室诊断细节时，生成结果会泛化为：

```text
采样送实验室检测。
```

这对初步安全数据可以接受，但对高质量训练数据不够。正式训练数据需要知道：

- 采血还是采粪？
- 采鼻拭子还是肺组织？
- 采流产胎儿还是母猪血清？
- 做 PCR、病毒分离、细菌培养、药敏、ELISA 还是病理？
- 单次阳性如何解释？
- 是否需要成对血清？

### 8.3 修复方向

按疾病补齐：

- 推荐样本类型。
- 推荐检测方法。
- 采样时机。
- 采样对象。
- 保存和送检边界。
- 结果解释限制。
- 与鉴别诊断对应的检测组合。

示例结构：

```yaml
laboratory_diagnosis:
  recommended_samples:
    - nasal swab
    - lung tissue
  recommended_tests:
    - RT-PCR
    - bacterial culture when secondary infection suspected
  interpretation_limits:
    - clinical signs alone are not sufficient
    - detection must be interpreted with stage and lesions
```

## 9. 鉴别诊断体系不足

### 9.1 当前问题

鉴别诊断覆盖严重不足：

- 73 个疾病页中，仅约 6 个有来源化鉴别诊断内容。
- 12 个症候群页已有基础，但较短。
- 还缺少可执行的 differential matrix。

### 9.2 高风险混淆组

必须建立矩阵的混淆组：

1. 腹泻类
   - PED
   - TGE
   - 轮状病毒
   - 大肠杆菌
   - 球虫
   - 沙门氏菌
   - 猪痢疾
   - 增生性肠炎
   - 梭菌性肠炎

2. 呼吸道类
   - PRRS
   - 猪流感
   - 支原体肺炎
   - 胸膜肺炎
   - 巴氏杆菌病
   - 副猪嗜血杆菌病

3. 繁殖障碍类
   - PRRS
   - 猪细小病毒病
   - 猪伪狂犬病
   - 猪瘟
   - 乙型脑炎
   - 布鲁氏菌病
   - 钩端螺旋体病

4. 神经症状类
   - 猪伪狂犬病
   - 链球菌病
   - 水肿病
   - 乙型脑炎
   - 狂犬病
   - 盐中毒/水中毒

5. 水疱病类
   - 口蹄疫
   - 塞内卡病毒 A
   - 水疱性口炎
   - 猪水疱病
   - 外伤

6. 急死/败血类
   - 非洲猪瘟
   - 猪瘟
   - 猪丹毒
   - 沙门氏菌病
   - 链球菌病
   - 猪胸膜肺炎
   - 中毒

### 9.3 修复标准

应新增：

- `exports/differential_matrix.csv`
- `exports/differential_matrix.json`
- `wiki/comparisons/*.md` 或 `wiki/synthesis/*differential*.md`

每条矩阵至少包含：

- syndrome
- target_disease
- differential_disease
- shared_signs
- distinguishing_signs
- recommended_samples
- recommended_tests
- fatal_or_report_boundary
- source_ids

## 10. 防控、上报、禁售、禁运边界不足

### 10.1 当前问题

规则页数量较多，是当前强项，但疾病页中“防控要点”缺口极大：

- 73 个疾病页中约 70 个防控要点仍为 placeholder 或不足。
- 规则卡只有 11 张，不足以覆盖主要高风险场景。
- 中国法规锚点还不完整。

### 10.2 高风险边界必须覆盖

以下场景必须有硬规则或强 review 规则：

- 非洲猪瘟疑似或阳性。
- 猪瘟疑似或阳性。
- 口蹄疫或水疱病未排除。
- 布鲁氏菌病、狂犬病、乙型脑炎、结核、钩端等人兽共患风险。
- 急性高热、发绀、血便、急死。
- 临近出栏且存在用药或病情未明。
- 疑似霉菌毒素、亚硝酸盐、有毒气体等中毒。
- 重大繁殖障碍暴发。
- 未排除重大疫病却建议销售、转运、屠宰。

### 10.3 修复标准

规则卡建议从 11 张扩展到 30-50 张。至少新增：

- ASF hard block
- CSF hard block
- FMD/vesicular disease hard block
- zoonotic disease protection rule
- near-market drug/sale rule
- specific dose block
- specific withdrawal period block
- antimicrobial stewardship rule
- feed toxin rule
- sudden death high fever rule
- reproductive failure sampling rule
- no sale/no transport before exclusion rule

## 11. 药物页与食品安全边界不足

### 11.1 当前问题

当前 76 个药物页多数较短：

- median length 约 928 字。
- 最短约 776 字。
- 多数为 evidence-only 页面。
- 可用于提醒“不要乱给剂量/休药期”，但不足以支持正式处方训练。

### 11.2 对训练数据的影响

当前阶段不应训练：

- 具体药物剂量。
- 固定疗程。
- 具体休药期。
- 不同国家/地区标签泛化。
- 临近出栏下的简单用药建议。

如果训练集中出现这些内容，会造成高风险：

- 模型学会无来源处方。
- 模型混用不同地区休药期。
- 模型在食品动物场景给出不安全上市建议。
- 模型把“管理方向”误学成“可执行处方”。

### 11.3 修复标准

药物页至少补：

- 药物类别。
- 猪用适用边界。
- 不适用/禁忌场景。
- 食品动物残留风险。
- 抗菌药耐药风险。
- 中国标签/法规来源。
- 休药期是否可引用。
- 是否允许训练具体剂量。
- dataset_generation_boundary。

没有权威标签来源时，schema 和生成器必须禁止输出具体剂量和具体休药期。

## 12. 来源页和证据状态规范不足

### 12.1 当前问题

来源页数量较多，但格式不完全一致：

- 部分 source page 缺少 `authority_level`。
- 部分 source page 缺少 `source_type`。
- evidence_status 中仍有 `NEEDS_REVIEW`。
- 疾病页中引用 source id 的方式还不完全稳定。

此前统计显示：

- source 页约 153 个。
- source evidence 中有 `HUMAN_REVIEWED`、`EXTRACTED`、`NEEDS_REVIEW`、`PROCESSED_SOURCE_ANCHORED` 等多种状态。
- `authority_level` 与 `source_type` 有缺失。

### 12.2 风险

来源规范不足会导致：

- 无法判断某个事实是否可用于训练。
- 无法区分教材、官方、网页、人工推断。
- 无法在生成结果中稳定记录 source ids。
- 严格审计时难以追踪每条事实来源。

### 12.3 修复标准

每个 source page 必须有：

- `source_id`
- `title`
- `source_path` 或 `url`
- `source_type`
- `authority_level`
- `evidence_status`
- `jurisdiction`
- `created`
- `updated`
- `used_by`

每条 fact 必须有：

- `fact_id`
- `fact_type`
- `subject`
- `predicate`
- `object`
- `fact_confidence`
- `evidence_source_id`
- `evidence_status`
- `applies_to_species`
- `applies_to_stage`
- `jurisdiction`

## 13. 中国法规锚点不足

### 13.1 当前问题

`disease_index.csv` 中：

- 大量疾病 `official_china_status` 为“未在本轮目录级处理中确认”。
- 部分为“待中国官方来源复核”。
- 58 个疾病仍标记为 `needs_body_extraction`。
- 15 个疾病为 `needs_cn_regulatory_anchor`。

### 13.2 对生成数据的影响

中国养殖场场景中，经常涉及：

- 是否需要上报。
- 是否能转运。
- 是否能出栏。
- 是否能销售。
- 是否能自行处置。
- 是否属于重大动物疫病。
- 是否涉及人兽共患风险。

若中国法规锚点不足，生成器只能写泛化安全话术，无法稳定判断具体疾病边界。

### 13.3 修复标准

至少补齐：

- 农业农村部一二三类动物疫病名录。
- 重大动物疫情应急处置相关规则。
- 非洲猪瘟、口蹄疫、猪瘟等关键疫病官方防控要求。
- 人兽共患病人员防护和报告边界。
- 临近出栏和食品安全相关通用边界。

## 14. 数据生成流程仍存在的问题

### 14.1 当前问题

现有 300 条数据已达到初步测试可用，但暴露出流程问题：

- 生成时仍可能出现具体休药/观察数字。
- `index` 在多批次合并后重复，不能作为主键。
- 检索上下文虽存在，但并非每条都能证明来源权威。
- 低频疾病和骨架页疾病更依赖 LLM 常识。
- 生成器未完全利用症候群、鉴别矩阵、规则卡、药物边界联合检索。

### 14.2 具体案例

严格评估发现 2 条应剔除或改写：

1. 猪细小病毒病：
   - `case_id=63c130c0-c739-50aa-aaac-a7a8726fb117`
   - `withdrawal_period` 中出现“约150天以上”

2. 猪营养缺乏与过量综合征：
   - `case_id=8411d9bc-c170-5db9-8d90-bb5291043f84`
   - `withdrawal_period` 中出现“至少观察14天”

这说明本地规则对 `withdrawal_period` 中具体时间数字的扫描仍需加强。

### 14.3 修复标准

生成脚本应增强：

- `--schema` 参数。
- 按 schema 加载 hard blocks。
- 检索疾病页 + 症候群页 + 鉴别矩阵 + 规则卡 + 药物边界页。
- 明确禁止具体剂量和具体休药/观察数字。
- 合并时使用 `case_id` 作为唯一主键。
- 输出 rejects 中必须包含具体拒绝原因。
- 每批生成后自动生成 wiki gap feedback。

## 15. 评估流程仍存在的问题

### 15.1 当前问题

双评审和仲裁已经有效提升了数据质量，但仍有优化空间：

- judge 主要基于通用评分，而不是每个疾病专属 checklist。
- arbiter 耗时字段未完整回填。
- 对 `withdrawal_period` 中“观察 14 天”这类具体时间没有完全拦截。
- 高风险疾病虽然进入仲裁，但规则卡数量不足。
- 当前仲裁通过率依赖模型判断，仍需要更强本地规则兜底。

### 15.2 修复标准

评估脚本应增加：

- disease-specific checklist。
- syndrome-specific checklist。
- differential matrix consistency check。
- hard rule pre-filter。
- final post-filter。
- exact rejection code。
- arbiter elapsed seconds 回填。
- source evidence sufficiency score。

建议新增评估维度：

- diagnosis_source_support
- differential_completeness
- sampling_specificity
- food_safety_boundary
- regulatory_boundary
- drug_safety_boundary
- train_ready_safety

## 16. 症候群页和主题页偏薄

### 16.1 当前问题

症候群页 12 个，主题页 99 个，但多数较短：

- 症候群页 median length 约 1239 字。
- 主题页 median length 约 350 字。

这些页面目前能做检索辅助，但不足以支撑系统级鉴别诊断。

### 16.2 需要增强的症候群页

优先增强：

- 仔猪腹泻
- 断奶后腹泻
- 呼吸道综合征
- 繁殖障碍
- 神经症状
- 水疱病
- 急死/败血症
- 皮肤瘙痒结痂
- 跛行/关节炎
- 贫血/黄疸
- 生长不良/消瘦
- 饲料中毒/有毒气体

每个症候群页应包含：

- 常见疾病列表。
- 年龄/阶段分布。
- 关键区分点。
- 推荐采样。
- 高风险红旗。
- 禁售/上报边界。
- 对应规则卡。

## 17. 规则页数量多但可执行规则卡不足

### 17.1 当前问题

规则页有 448 个，但规则卡只有 11 个。长规则适合阅读和检索，但生成/评估脚本更需要短小、可执行、可 hard block 的规则卡。

### 17.2 修复方向

将 448 个规则页归纳为：

- hard_block cards
- review_trigger cards
- generation_guardrail cards
- scoring_penalty cards
- regulatory_boundary cards

规则卡字段建议：

```yaml
card_id:
title:
severity:
jurisdiction:
hard_block:
trigger_terms:
applies_to_diseases:
applies_to_scenarios:
reject_if:
review_if:
required_safe_response:
evidence_source_id:
```

## 18. 别名和疾病命中仍需增强

### 18.1 当前状态

`alias_index.csv` 有 184 行，覆盖 73 个疾病，基础可用。

### 18.2 潜在问题

猪病真实场景常用俗称：

- 蓝耳
- 伪狂
- 副猪
- 圆环
- 回肠炎
- 黄白痢
- 水肿病
- 喘气病
- 五号病
- 非瘟

如果别名不足，会导致：

- 检索命中不稳定。
- `target_disease_in_diagnosis` 误判。
- 本地 mismatch 规则误杀。
- 生成问题不够真实。

### 18.3 修复标准

每个疾病至少有：

- 中文规范名。
- 英文名。
- 常见缩写。
- 养殖户俗称。
- 病原名。
- 旧称或相关综合征名。

## 19. 训练数据质量问题总结

当前 300 条数据验证结论：

| 项目 | 结果 |
|---|---:|
| 总行数 | 300 |
| 字段数 | 60 |
| final_label=pass | 300 |
| final_fatal_risk=False | 300 |
| 疾病覆盖 | 66 |
| case_id 重复 | 0 |
| user_query 重复 | 0 |
| 问题+诊断+处方重复 | 0 |
| 具体剂量 | 0 |
| 具体休药/观察数字 | 2 |
| 高风险疾病缺安全边界 | 0 |

结论：

- 作为模型测试数据：可用。
- 作为初步弱监督 SFT：基本可用，建议剔除 2 条风险行。
- 作为正式权威兽医训练数据：暂不建议。

主要限制：

- 不是每条都权威来源逐条锚定。
- wiki 还有 placeholder。
- 药物页不足以训练具体处方。
- 中国法规锚点不完整。
- 鉴别诊断矩阵未成型。

## 20. 优化优先级

### P0：立即修复

1. 生成脚本接入 `swine_llm_wiki_schema.yaml`。
2. 加强具体休药/观察时间数字扫描。
3. 合并数据时使用 `case_id` 作为主键，不再依赖 `index`。
4. 剔除或改写当前 2 条 `specific_withdrawal` 样本。
5. 生成后自动输出 strict eval report。

### P1：高价值补强

1. 补齐 20 个高频/高风险疾病页。
2. 建立腹泻、呼吸道、繁殖障碍、神经、水疱、急死败血 6 个鉴别矩阵。
3. 规则卡从 11 张扩展到至少 30 张。
4. 补齐重大动物疫病和人兽共患病中国法规锚点。
5. 每个高风险疾病页补 `forbidden_boundaries` 和 `evaluation_checklist`。

### P2：正式训练集准备

1. 73 个疾病页全部达到 4000 字以上或等效结构化 facts。
2. facts 从 1465 增至 4000-6000。
3. 每个疾病至少 20 条 facts，高频疾病至少 40 条。
4. `NEEDS_REVIEW` facts 比例降到 10% 以下。
5. 所有核心栏目 placeholder 清零。
6. 每批数据进行人工抽检并回写 issues。

### P3：权威处方能力

1. 系统接入中国兽药标签和法规来源。
2. 药物页补适应证、禁忌、食品安全和休药期来源。
3. 建立 jurisdiction-aware 的剂量/休药期规则。
4. 无权威来源时继续禁止具体剂量和具体休药期。

## 21. 建议新增的任务文档和产物

建议后续新增：

- `SWINE_WIKI_COMPLETION_BACKLOG.md`
- `SWINE_DISEASE_PAGE_TEMPLATE.md`
- `SWINE_DIFFERENTIAL_MATRIX_SPEC.md`
- `SWINE_RULE_CARD_BACKLOG.md`
- `SWINE_DRUG_PAGE_COMPLETION_PLAN.md`
- `SWINE_CN_REGULATORY_ANCHOR_PLAN.md`
- `SWINE_DATASET_STRICT_EVAL_SPEC.md`

建议新增 exports：

- `differential_matrix.csv`
- `differential_matrix.json`
- `generation_checklist.json`
- `evaluation_checklist.json`
- `high_risk_rule_cards.json`
- `disease_completeness_report.json`
- `source_completeness_report.json`

## 22. 最终判断

当前猪病 LLM Wiki 的基础是可用的，已经可以支撑弱监督数据生成和初步模型验证。但要达到“完整有效的训练/微调数据生产知识库”，还需要从“有页面、有规则、有 facts”升级为“每个疾病都有完整可生成、可鉴别、可评估、可审计的知识单元”。

最短路径是：

1. 用猪病专属 schema 约束生成与评估。
2. 先补高频和高风险疾病。
3. 建鉴别诊断矩阵。
4. 扩展规则卡。
5. 强化药物和食品安全边界。
6. 持续用生成数据的错误反馈反哺 wiki。

只要这几块补齐，后续生成 1000 条以上更稳定的猪病训练/微调数据会更可靠，人工复核成本也会明显下降。

## 23. 2026-05-07 增量更新：基于 `raw/md/1-200.md` 的总论知识补充

### 23.1 本次分析对象

本次分析文件：

`knowledge/llm_wiki_swine_authoritative/raw/md/1-200.md`

该文件是 *Diseases of Swine, 11th Edition* 前 200 页的 Markdown 转换文本。经章节识别，该文件主要覆盖：

- 版权、目录、编者、贡献者信息
- Section I Veterinary Practice
- Herd Evaluation
- Behavior and Welfare
- Diagnostic Tests
- Optimizing Sample Selection, Collection, and Submission
- Collecting Evidence and Establishing Causality
- Disease Control, Prevention, and Elimination
- Drug Pharmacology, Therapy, and Prophylaxis
- Anti-inflammatory drugs
- Anesthesia and Surgical Procedures in Swine 的开头部分

因此，这 200 页主要是猪病总论、诊断、采样、防控、用药原则和实践框架，而不是具体单病章节。

### 23.2 对当前 wiki 缺口的解决能力评估

该文件可以显著补强以下问题：

1. 采样和实验室诊断边界不足
   - 可补充“采样必须围绕诊断问题、症候群、病变分布、代表性动物”的原则。
   - 可补充“不能只写送检，应该说明样本类型和采样对象”的评估要求。

2. 诊断过程过于单点判断
   - 可补充“诊断应结合病史、临床、剖检、实验室和流行病学”的原则。
   - 可约束生成结果不能把一个症状或一个检测结果直接等同于确诊。

3. 因果判断不足
   - 可补充“检出病原不等于证明致病”的评估边界。
   - 可要求 judge 检查临床表现、病变、时序、鉴别诊断是否支持最终判断。

4. 防控和生物安全建议过于泛化
   - 可补充场内、场间、跨境传播路线。
   - 可强化活猪、死猪、车辆、饲料、人员、衣物鞋靴、工具等传播路径。

5. 药物使用和休药期边界不足
   - 可补充治疗目标、生产物流、法规、残留责任、耐药风险、疗效复核等原则。
   - 支持继续禁止无来源具体剂量和具体休药期。

6. 生成和评估 rubric 不够细
   - 可增强 user_query 的真实场景要求。
   - 可增强评估时对采样、因果、防控和药物边界的检查。

该文件不能单独解决以下问题：

1. 73 个具体疾病页的临床症状缺口。
2. 73 个具体疾病页的剖检变化缺口。
3. 每个疾病的实验室检测方法和推荐样本清单。
4. 每个疾病的鉴别诊断矩阵。
5. 每个疾病的中国官方法规锚点。
6. 药物的中国标签、剂量、疗程、休药期。
7. 单病层面的具体处置和防控策略。

### 23.3 本次已新增或修改的 wiki 内容

本次新增：

`knowledge/llm_wiki_swine_authoritative/wiki/synthesis/swine_textbook_pages_1_200_crosscutting_digest.md`

用途：

- 作为前 200 页总论内容的派生消化页。
- 支撑猪病生成与评估中的通用规则。
- 强化诊断、采样、因果判断、防控、生物安全、用药边界。
- 供检索流程在目标疾病页之外额外召回。

本次新增候选 facts：

`knowledge/llm_wiki_swine_authoritative/issues/textbook_1_200_crosscutting_candidate_facts_20260507.json`

说明：

- 候选 facts 是对原文内容的提炼和改写，不是大段复制。
- 当前放在 `issues/` 下，作为候选层。
- 后续人工复核后再决定是否进入 `exports/knowledge_facts.json`。

本次更新：

`knowledge/llm_wiki_swine_authoritative/exports/synthesis_index.csv`

新增了 `swine_textbook_pages_1_200_crosscutting_digest` 条目。

本次更新：

`knowledge/llm_wiki_swine_authoritative/log.md`

记录了本次增量维护动作。

### 23.4 本次实际解决的问题

本次部分解决了以下章节中的问题：

#### 对第 8 节“实验室诊断与采样建议不足”的改善

新增 digest 明确了：

- 样本选择应服务于诊断问题。
- 应选择能代表当前疾病过程的动物。
- 采样需结合症候群、病变分布和检测目的。
- 急死、呼吸道、消化道、繁殖障碍、神经症状、跛行等不同场景应有不同采样思路。

仍未解决：

- 每个具体疾病的推荐样本清单。
- 每个具体疾病的检测方法。
- 每个疾病的样本保存、送检时机、结果解释。

#### 对第 10 节“防控、上报、禁售、禁运边界不足”的改善

新增 digest 明确了：

- 防控应从宿主、病原、环境三个方面考虑。
- 生物安全应覆盖活猪、死猪、车辆、饲料、人员、衣物鞋靴、设备工具等路线。
- 高风险病例生成时不能只写“消毒隔离”，还应考虑传播路线和移动限制。

仍未解决：

- 中国特定法规下的疾病级上报边界。
- 每个疾病是否属于一二三类动物疫病的最终确认。
- 具体官方处置流程。

#### 对第 11 节“药物页与食品安全边界不足”的改善

新增 digest 明确了：

- 药物治疗需要先明确治疗目标。
- 猪场用药要考虑生产物流和法规。
- 休药期、残留责任、耐药风险不能被忽略。
- 全群用药或预防用药不应自动推荐。
- 没有标签级来源时，不应生成具体剂量和具体休药期。

仍未解决：

- 每种药物在中国猪用标签下的适应证。
- 药物剂量、疗程、休药期的权威来源。
- 禁用药、限用药与市场合规细则。

#### 对第 14 节“数据生成流程仍存在的问题”的改善

新增 digest 可以作为生成上下文补充：

- 让 user_query 更像真实猪场问题。
- 让 diagnosis 更强调证据链和不确定性。
- 让 prescription 更强调管理、采样、送检、防控和禁止边界。
- 强化无来源时不生成具体剂量和具体休药数字。

仍未解决：

- 生成脚本尚未自动检索这个新 digest。
- 生成脚本尚未接入 `swine_llm_wiki_schema.yaml` 的所有 hard blocks。
- 具体休药/观察数字扫描仍需增强。

#### 对第 15 节“评估流程仍存在的问题”的改善

新增 digest 可作为 judge 和 arbiter 的补充依据：

- 检查回答是否考虑猪群层面信息。
- 检查是否把单一症状或单一检测结果过度解释。
- 检查采样建议是否和症候群匹配。
- 检查防控建议是否覆盖传播路径。
- 检查用药建议是否有治疗目标和监管边界。

仍未解决：

- judge 还没有按该 digest 自动生成 checklist。
- arbiter 还没有逐条引用该 digest 的 source ids。
- disease-specific checklist 仍不足。

### 23.5 本次不能解决的核心问题

本次基于 1-200 页的补充无法替代后续单病章节抽取。仍需继续处理：

- `201-400.md`
- `401-600.md`
- 后续疾病章节 md 或 PDF 分段

尤其需要补：

- 病毒病单病章节
- 细菌病单病章节
- 寄生虫病章节
- 非感染性疾病和中毒章节
- 食品安全、人兽共患和法规章节

### 23.6 后续建议

下一步建议优先做两件事：

1. 更新生成/评估脚本的检索策略

   生成猪病数据时，除目标疾病页外，额外检索：

   - `swine_textbook_pages_1_200_crosscutting_digest.md`
   - `swine_sampling_and_lab_diagnosis_boundary.md`
   - `swine_drug_and_withdrawal_boundary.md`
   - `swine_differential_diagnosis_matrix.md`
   - 相关 syndrome 页
   - 相关 rule_card 页

2. 继续处理 `201-400.md` 和 `401-600.md`

   这两段更可能包含具体系统和疾病章节，对解决疾病页临床症状、剖检变化、鉴别诊断和实验室诊断缺口更关键。

### 23.7 本次增量后的问题状态变化

| 问题类别 | 本次变化 | 剩余状态 |
|---|---|---|
| 采样/实验室诊断通用原则 | 部分改善 | 单病样本和检测仍缺 |
| 诊断过程/因果判断 | 明显改善 | 需接入评估脚本 |
| 防控/生物安全通用原则 | 部分改善 | 中国法规和单病边界仍缺 |
| 药物/休药期安全边界 | 部分改善 | 标签级药物信息仍缺 |
| 生成真实场景要求 | 部分改善 | 需脚本检索新 digest |
| disease-specific 临床和剖检 | 未解决 | 需继续抽取疾病章节 |
| 鉴别诊断矩阵 | 未解决 | 需专门构建 matrix |
| 中国法规锚点 | 未解决 | 需官方来源补充 |

## 24. 2026-05-07 增量更新：基于 `raw/md/201-400.md` 的系统章节知识补充

### 24.1 本次分析对象

本次分析文件：

`knowledge/llm_wiki_swine_authoritative/raw/md/201-400.md`

该文件是 *Diseases of Swine, 11th Edition* 第 201-400 页的 Markdown 转换文本。经章节识别，该段并不是完整的单病章节集合，而是从第 11 章后段延续到第 20 章开端，主要覆盖：

- 麻醉、镇痛、外科、阉割、疝、脱垂、胃溃疡、关节炎和外科并发症边界。
- Chapter 12：屠前食品安全、人兽共患病和人类健康接口。
- Chapter 13：展览猪和宠物猪的生物安全、健康管理、用药和伦理边界。
- Chapter 14：心血管与造血系统，含急死、贫血、休克、水肿、心包/心肌/心内膜病变、桑葚心病等鉴别线索。
- Chapter 15：消化系统，含腹泻机制、年龄阶段鉴别、剖检/组织病理/实验室确认、胃肠道病变、肝脏和腹膜病变。
- Chapter 16：免疫系统，含初乳、母源抗体、黏膜免疫、群体免疫、疫苗失败、自家苗和 planned exposure 边界。
- Chapter 17：皮肤、蹄和爪，含皮肤病史、原发/继发病变、皮肤采样、细菌/病毒/真菌/寄生虫/环境/营养鉴别。
- Chapter 18：乳腺系统，含初乳、泌乳、乳房炎和产后泌乳障碍综合征 PDS。
- Chapter 19：神经与运动系统开端，含神经定位、采样、先天性/感染性/中毒性/营养性神经和跛行鉴别。
- Chapter 20：繁殖系统开端，含猪群繁殖问题诊断框架、个体母猪/后备母猪检查和早期繁殖指标排查。

### 24.2 对当前 wiki 缺口的解决能力评估

该文件可以显著补强以下问题：

1. 鉴别诊断体系不足
   - 消化系统章节提供了腹泻按年龄、机制、剖检病变和实验室确认进行鉴别的框架。
   - 心血管/造血、皮肤、神经运动、乳腺和繁殖系统章节可以补充“症候群入口”而不是只按病原检索。
2. 实验室诊断和采样建议不足
   - 消化道疾病可补充“病变 + 组织病理 + PCR/培养/毒素/IHC/ISH”等组合确认边界。
   - 皮肤病可补充 biopsy、scraping/direct examination、culture、PCR 的选择边界。
   - 神经/运动系统可补充按定位和安全风险选择生前/死后样本。
3. 正文事实密度不足
   - 可补充腹泻、出血性肠炎、胃溃疡、肠扭转、贫血、急死、皮肤病变、跛行、弱仔和 PDS 的系统性 facts。
   - 尤其对 `SYN-001-piglet-diarrhea.md`、`SYN-002-post-weaning-diarrhea.md`、`SYN-005-neurologic-signs.md`、`SYN-008-skin-pruritus-crusts.md`、`SYN-009-lameness-arthritis.md`、`SYN-003-reproductive-failure.md` 有直接价值。
4. 药物、食品安全和人兽共患边界不足
   - Chapter 12 明确了屠前食品安全、残留、断针、食品源性与非食品源性人兽共患、AMR 的边界。
   - Chapter 13 对展览猪/宠物猪的移动、混群、药检、伦理和人群接触风险提供了场景化约束。
5. 评估规则不够细
   - 可要求 judge 检查腹泻回答是否匹配年龄、病变和检测。
   - 可要求 judge 检查常在/地方性肠道病原 PCR 或培养阳性是否被过度解释为因果。
   - 可要求 judge 检查皮肤、神经、跛行、PDS、弱仔和繁殖问题是否有症候群级证据链。

该文件不能单独解决以下问题：

1. 73 个具体单病页面仍需要后续病原章节补齐。
2. 中国一二三类动物疫病、强制报告、检疫、禁运、无害化处置仍必须依赖 A0/A1 官方来源。
3. 中国兽药标签、剂量、疗程、休药期、最大残留限量不能由该教材段落直接生成。
4. 繁殖系统仅覆盖开端，完整繁殖章节需要继续处理 `401-600.md`。
5. 呼吸系统、泌尿系统和后续病毒/细菌/寄生虫单病章节仍需继续抽取。

### 24.3 本次已新增或修改的 wiki 内容

本次新增：

`knowledge/llm_wiki_swine_authoritative/wiki/synthesis/swine_textbook_pages_201_400_system_digest.md`

用途：

- 作为 201-400 页系统章节内容的派生消化页。
- 支撑腹泻、急死、贫血、皮肤、神经、跛行、弱仔、PDS、繁殖问题和食品安全场景的生成与评估。
- 与 `swine_textbook_pages_1_200_crosscutting_digest.md` 互补：前者偏总论方法，本文偏系统病理、症候群鉴别和食品安全/公共卫生边界。

本次新增候选 facts：

`knowledge/llm_wiki_swine_authoritative/issues/textbook_201_400_system_candidate_facts_20260507.json`

说明：

- 候选 facts 为对教材内容的提炼和改写，不是大段复制。
- 当前放在 `issues/` 下作为候选层，避免未经复核直接污染 `exports/knowledge_facts.json`。
- 后续可按 disease/syndrome/fact_type 人工复核后分批进入正式 facts。

本次更新：

`knowledge/llm_wiki_swine_authoritative/exports/synthesis_index.csv`

新增了 `swine_textbook_pages_201_400_system_digest` 条目。

本次更新：

`knowledge/llm_wiki_swine_authoritative/log.md`

记录了本次增量维护动作。

### 24.4 本次实际解决的问题

#### 对第 8 节“实验室诊断与采样建议不足”的改善

新增 digest 明确了：

- 腹泻不能只写“PCR/培养”，需要结合年龄、临床、剖检、组织病理和病原定位。
- 常在或地方性肠道病原被 PCR、培养或宏基因组检出，不等于已经证明因果。
- 皮肤病应描述病变类型、分布和病程，并选择皮肤活检、刮片/直接检查、培养或 PCR。
- 神经和跛行病例应先定位，再选择生前/死后样本和安全边界。

仍未解决：

- 每个单病的推荐样本清单仍未全部结构化。
- 每个单病的检测方法、保存运输、阳性/阴性解释仍需病原章节和实验室来源补齐。

#### 对第 9 节“鉴别诊断体系不足”的改善

新增 digest 明确了：

- 腹泻可按仔猪日龄、断奶后、育肥/成年、出血性/黏液性/水样、剖检病变和检测组合建立 matrix。
- 急死/发绀/苍白/腹水/水肿应纳入心血管和造血系统鉴别，不能自动归入 ASF、CSF 或败血症。
- 皮肤病应纳入细菌、病毒、真菌、寄生虫、环境、营养、先天性、蹄爪和监管性水疱/出血性疾病鉴别。
- 神经症状应先做定位，再区分病毒、细菌、中毒、营养、缺氧、低血糖、盐中毒/缺水等原因。
- 跛行应区分骨、关节、肌肉、蹄爪、骨折、骨软骨病、感染性关节炎、多发性关节炎和营养性肌病。

仍未解决：

- `exports/differential_matrix.csv/json` 仍未正式生成。
- 每条鉴别关系还需要按 source id、shared_signs、distinguishing_signs、samples、tests 结构化。

#### 对第 10 节“防控、上报、禁售、禁运边界不足”的改善

新增 digest 明确了：

- 腹泻或出血性肠道病变中若不能排除 CSF/ASF，应进入上报和快速调查边界，而不是常规腹泻治疗。
- 展览猪具有移动、混群、运输、展会压力和人群接触风险，生成时应有独立场景约束。
- 食品链猪涉及断针、残留、药检、人兽共患和 AMR 风险。

仍未解决：

- 中国官方上报、检疫、禁运和无害化处置仍需 A0/A1 来源。
- 展会/流通/屠宰场景的中国本地法规仍未完全结构化。

#### 对第 11 节“药物页与食品安全边界不足”的改善

新增 digest 明确了：

- 市场猪、展览猪、宠物猪和食品链动物的用药回答必须考虑残留、检测、伦理、食品安全和合规边界。
- 断针、化学危害、生物危害、AMR 都应作为屠前食品安全风险进入评估。
- 外科、镇痛、抗菌药、激素、抗炎药相关内容不得转化为固定处方、剂量或休药期。

仍未解决：

- 中国标签级药物适应证、剂量、疗程和休药期仍缺。
- 食品安全阈值、药检规则、市场准入和合规结论仍需官方来源。

#### 对第 16 节“症候群页和主题页偏薄”的改善

新增 digest 可增强以下症候群页：

- 仔猪腹泻
- 断奶后腹泻
- 急死/败血症
- 贫血/黄疸
- 皮肤瘙痒/结痂/坏死
- 跛行/关节炎
- 神经症状
- 弱仔/初乳不足
- PDS/乳房炎
- 繁殖障碍

仍未解决：

- 症候群页尚未自动合并这些候选 facts。
- 部分主题页仍只起导航作用，缺少结构化 matrix。

### 24.5 本次增量后的问题状态变化

| 问题类别 | 本次变化 | 剩余状态 |
|---|---|---|
| 采样/实验室诊断 | 明显改善 | 单病样本、保存运输、检测解释仍需继续抽取 |
| 鉴别诊断 | 明显改善 | 需生成正式 differential matrix |
| 疾病页正文完整性 | 部分改善 | 主要改善系统/症候群，不等于 73 个单病页完成 |
| 食品安全/人兽共患/AMR | 明显改善 | 中国法规、MRL、休药期和药检规则仍缺 |
| 药物/外科/麻醉边界 | 部分改善 | 仍需标签级来源和评估器 hard block |
| 症候群页 | 部分改善 | 需把候选 facts 回填到 syndrome 页面 |
| 生成/评估 rubric | 部分改善 | 脚本尚未自动检索新 digest |
| 中国法规锚点 | 未解决 | 必须继续补 A0/A1 官方来源 |

### 24.6 后续建议

下一步建议：

1. 将生成/评估检索策略加入：
   - `swine_textbook_pages_201_400_system_digest.md`
   - `swine_textbook_pages_1_200_crosscutting_digest.md`
   - 相关 syndrome 页
   - `swine_sampling_and_lab_diagnosis_boundary.md`
   - `swine_public_health_food_safety_boundary.md`
   - `swine_drug_and_withdrawal_boundary.md`
2. 优先把 `textbook_201_400_system_candidate_facts_20260507.json` 中的腹泻、皮肤、神经、乳腺、食品安全 facts 回填到 syndrome 页。
3. 基于本次 digest 先构建腹泻 differential matrix 的第一版。
4. 继续处理 `401-600.md`，重点补完整繁殖系统、呼吸系统、泌尿系统以及后续病毒病单病章节。

## 25. 2026-05-07 增量更新：基于 `raw/md/401-600.md` 的繁殖、呼吸、泌尿和病毒章节补充

### 25.1 本次分析对象

本次分析文件：

`knowledge/llm_wiki_swine_authoritative/raw/md/401-600.md`

该文件是 *Diseases of Swine, 11th Edition* 第 401-600 页的 Markdown 转换文本。经章节识别，该段比 `1-200.md` 和 `201-400.md` 更接近当前 wiki 最缺的 disease-specific 内容。它主要覆盖：

- Chapter 20 繁殖系统后续：断奶至发情间隔、受胎率/分娩率、外阴分泌物、分娩问题、公猪繁殖、精液质量、AI 传播、流产诊断、胎儿采样、血清学、病毒性/细菌性/真菌性/毒素性流产。
- Chapter 21 呼吸系统：呼吸防御、PRDC、环境/管理风险、原发和继发病原、肺炎类型、胸膜炎、空气传播、猪群流动、生物安全、疫苗、诊断和监测。
- Chapter 22 泌尿系统：尿液解释、肾衰竭、肾出血/梗死/肾小球肾炎/肾小管和间质病变、膀胱炎-肾盂肾炎、尿石症、肾积水、肾虫和肾脏大体病变鉴别。
- Chapter 23 病毒总论：病毒分类、培养、抗原检测、核酸检测、抗体检测、测序、定量和病毒因果解释边界。
- Chapter 24-36 开端：腺病毒、非洲猪瘟病毒、环状病毒、冠状病毒、丝状病毒、黄病毒、戊型肝炎病毒、疱疹病毒和流感病毒开端等。

### 25.2 对当前 wiki 缺口的解决能力评估

该文件可以显著补强以下问题：

1. 单病页面正文和事实密度不足
   - 直接提供 ASF、PCV2、TGE/PRCV/PED/PDCoV、PRV、JEV、HEV、腺病毒等章节的病原、传播、临床、病变、诊断、免疫和防控边界。
   - 对 `DIS-001-adenoviruses.md`、`DIS-002-african-swine-fever-virus.md`、`DIS-007-circoviruses-pcvad.md`、`DIS-008/009/010/011/012/013` 冠状病毒相关页、`DIS-015-japanese-encephalitis-virus.md`、`DIS-017-hepatitis-e-virus.md`、`DIS-018-pseudorabies-aujeszky-disease.md`、`DIS-019-porcine-cytomegalovirus.md`、`DIS-020-malignant-catarrhal-fever-ovine-herpesvirus-2.md`、`DIS-021-influenza-viruses.md` 有直接价值。
2. 实验室诊断和采样建议不足
   - 流产章节明确了母猪样本、胎儿样本、胎盘、胎儿胸腔液、胎儿胃内容物、成对血清等选择逻辑。
   - ASF 章节明确了淋巴结、肾、脾、肺、血液、血清，野猪骨髓等样本。
   - PRV 章节明确了三叉神经节、嗅神经节、扁桃体、肺、脾、肝、肾、淋巴结和胎儿组织等样本选择。
   - 呼吸系统章节补充了鼻拭子、口腔液、血清学、剖检、组织病理、屠宰检查和监测计划。
3. 鉴别诊断体系不足
   - 流产可按母猪是否发病、胎儿感染/母体全身病、胎龄、胎儿病变、病原和毒素进行矩阵化。
   - 呼吸病可按 PRDC、原发/继发病原、环境管理风险和肺炎类型进行矩阵化。
   - 肾脏病变可按肾出血、肾皮质点状出血、间质性肾炎、肾盂肾炎、肾小球肾炎、肾积水、肾肿瘤等进行矩阵化。
   - ASF 与 CSF、丹毒、败血性沙门氏菌病、PDNS 等高风险混淆组更清晰。
4. 评估流程 disease-specific checklist 不足
   - PCV2-SD 不能只凭 qPCR，应满足临床消瘦/生长停滞、淋巴组织病理和病变中 PCV2 高载量。
   - PCV2-RD 应看晚期流产/死胎、胎儿心肌病变和心肌病变中 PCV2。
   - PDNS 应看皮肤/肾脏病变和系统性坏死性血管炎/纤维素性坏死性肾小球肾炎。
   - TGE/PED/PDCoV 需结合年龄、绒毛萎缩、腹泻模式和差异检测。
5. 高风险规则和监管边界
   - ASF 疑似时必须限制移动并立即检测；不得生成常规经验治疗、销售、调运或隐瞒建议。
   - 但中国本地的上报、封锁、扑杀、无害化和补偿规则仍不能由教材替代。

该文件不能单独解决以下问题：

1. 中国 A0/A1 官方法规、疫情处置和动物疫病分类。
2. 中国兽药标签、剂量、疗程、休药期和 MRL。
3. 完整流感章节，因为 `401-600.md` 仅进入 Chapter 36 开端。
4. 后续病毒章节仍未覆盖完整，例如副黏病毒、细小病毒、瘟病毒、微 RNA 病毒、PRRSV、猪痘、轮状/呼肠孤病毒、逆转录病毒、弹状病毒、披膜病毒等。
5. 细菌病章节仍需后续 `601-800.md`、`801-1000.md` 等继续抽取。

### 25.3 本次已新增或修改的 wiki 内容

本次新增：

`knowledge/llm_wiki_swine_authoritative/wiki/synthesis/swine_textbook_pages_401_600_repro_respiratory_virus_digest.md`

用途：

- 作为 401-600 页繁殖、呼吸、泌尿和病毒章节内容的派生消化页。
- 支撑繁殖障碍、呼吸道综合征、泌尿/肾脏病变、ASF、PCV2、冠状病毒、PRV、JEV、HEV、流感开端等场景的生成与评估。
- 与 `1-200` 和 `201-400` digest 互补：前者偏总论方法，中段偏系统鉴别，本段开始补 disease-specific 病毒章节。

本次新增候选 facts：

`knowledge/llm_wiki_swine_authoritative/issues/textbook_401_600_repro_respiratory_virus_candidate_facts_20260507.json`

说明：

- 候选 facts 是对教材内容的提炼和改写，不是大段复制。
- 当前仍放在 `issues/` 下作为候选层，等待人工复核后再进入 `exports/knowledge_facts.json`。
- 候选 facts 覆盖 reproductive_sampling、diagnostic_boundary、respiratory_control、renal_differential、ASF、PCV2、TGE、PRV、HEV、JEV、IAV 等。

本次更新：

`knowledge/llm_wiki_swine_authoritative/exports/synthesis_index.csv`

新增了 `swine_textbook_pages_401_600_repro_respiratory_virus_digest` 条目。

本次更新：

`knowledge/llm_wiki_swine_authoritative/log.md`

记录了本次增量维护动作。

### 25.4 本次实际解决的问题

#### 对第 8 节“实验室诊断与采样建议不足”的改善

新增 digest 明确了：

- 流产诊断要按“母体全身病”还是“胎儿/胎盘感染”选择不同样本。
- 若母猪在流产前后有发热、咳嗽、厌食等全身病，应同时采母猪和胎儿样本。
- 若怀疑胎儿感染，应采多头胎儿、多窝材料，避免只采少数胎儿导致漏检。
- 胎儿采样应包括固定和新鲜/冷藏的脑、心、肺、肝、脾、肾、胎盘、骨骼肌、胎儿胸腔液、胎儿胃内容物和母猪血清等。
- IAV 诱发流产不能依赖胎儿样本确认，应从患病母猪鼻拭子、支气管拭子、肺、口腔液或成对血清寻找证据。
- ASF 和 PRV 的推荐组织样本更清晰。

仍未解决：

- 所有单病页面尚未逐一回填完整样本清单。
- 中国官方实验室送检规范和监管样本要求仍需 A0/A1 来源。

#### 对第 9 节“鉴别诊断体系不足”的改善

新增 digest 明确了：

- 繁殖障碍鉴别应覆盖 PRRSV、PCV2、PPV、PRV、IAV、EMCV、肠病毒/捷申病毒、CSF、ASF、非典型瘟病毒、JEV、PCMV、rubulavirus、Menangle virus、钩端螺旋体、猪布鲁氏菌、衣原体、一氧化碳和玉米赤霉烯酮。
- PRDC 不是单一病原病，常由病毒、细菌、环境、管理、遗传和免疫状态共同决定。
- 肾皮质点状出血不是 ASF/CSF 特异病变，也可见于细菌败血症、巨细胞病毒、电击、中毒、急性肾小球肾炎等。
- PCV2-SD、PCV2-RD 和 PDNS 必须区分，不能统一写成“圆环病毒病”。
- TGE、PED、PDCoV、轮状病毒、大肠杆菌、球虫等应按年龄、绒毛萎缩和检测结果鉴别。

仍未解决：

- `exports/differential_matrix.csv/json` 仍未正式生成。
- 每个疾病对的 shared_signs、distinguishing_signs、recommended_samples、recommended_tests 仍需结构化。

#### 对第 6、7 节“疾病页正文完整性和事实密度不足”的改善

新增 digest 可直接服务以下 disease 页：

- `DIS-001-adenoviruses.md`
- `DIS-002-african-swine-fever-virus.md`
- `DIS-007-circoviruses-pcvad.md`
- `DIS-008-porcine-epidemic-diarrhea-virus.md`
- `DIS-009-transmissible-gastroenteritis-virus.md`
- `DIS-010-porcine-deltacoronavirus.md`
- `DIS-011-hemagglutinating-encephalomyelitis-virus.md`
- `DIS-012-porcine-respiratory-coronavirus.md`
- `DIS-013-porcine-torovirus.md`
- `DIS-015-japanese-encephalitis-virus.md`
- `DIS-017-hepatitis-e-virus.md`
- `DIS-018-pseudorabies-aujeszky-disease.md`
- `DIS-019-porcine-cytomegalovirus.md`
- `DIS-020-malignant-catarrhal-fever-ovine-herpesvirus-2.md`
- `DIS-021-influenza-viruses.md`

仍未解决：

- 本次没有直接逐页改写 disease 页面，而是先建立可检索 digest 和候选 facts。
- disease 页面回填还需要下一步按疾病分批处理，避免把候选事实未经复核直接写入正式页面。

#### 对第 10 节“防控、上报、禁售、禁运边界不足”的改善

新增 digest 明确了：

- ASF 疑似时应限制猪只移动并立即检测。
- 低毒力 ASF 可能缺乏明显症状或病变，不能因为不典型就排除。
- PRV、JEV、HEV、IAV 等涉及野生动物、人兽共患、公共卫生或跨物种传播边界。
- 呼吸病控制应从病原负荷、呼吸防御损伤、宿主抵抗力、环境、猪群流动、生物安全和疫苗策略综合考虑。

仍未解决：

- 中国监管处置边界仍必须由农业农村部、海关、WOAH 或相关官方文件补齐。
- 教材中的国际/通用控制原则不能直接替代中国现场执法规则。

#### 对第 15 节“评估流程仍存在的问题”的改善

新增 digest 可支持 judge 检查：

- 流产回答是否按母猪/胎儿/胎盘机制选样。
- 是否错误用胎儿样本确诊 IAV 诱发流产。
- 呼吸道回答是否忽略环境、猪群流动和混合感染。
- 肾点状出血是否被过度解释为单一疾病。
- PCV2 是否被 qPCR 单点阳性过度诊断。
- ASF 是否被写成可常规治疗疾病。
- TGE/PED/PDCoV 是否按年龄、绒毛萎缩和乳源免疫鉴别。

仍未解决：

- 评估脚本尚未自动加载本次 digest。
- disease-specific checklist 尚未由这些候选 facts 自动生成。

### 25.5 本次增量后的问题状态变化

| 问题类别 | 本次变化 | 剩余状态 |
|---|---|---|
| 采样/实验室诊断 | 明显改善 | 需回填到具体疾病页和 syndrome 页 |
| 鉴别诊断矩阵 | 明显改善 | 需生成正式 matrix exports |
| disease-specific 病毒内容 | 明显改善 | 后续病毒章节和细菌章节仍缺 |
| ASF 高风险边界 | 明显改善 | 中国官方处置仍需 A0/A1 |
| PCV2/PDNS 诊断边界 | 明显改善 | 需写入 DIS-007 和皮肤/肾脏 syndrome |
| 冠状病毒腹泻鉴别 | 明显改善 | 需回填 PED/TGE/PDCoV/PRCV 页面 |
| 呼吸道综合征 | 明显改善 | 具体呼吸病病原章节仍需继续处理 |
| 泌尿/肾脏鉴别 | 部分改善 | 需要后续疾病页/症候群页结构化 |
| 药物/休药期 | 未直接解决 | 仍需标签和官方来源 |
| 中国法规锚点 | 未解决 | 仍需官方来源补充 |

### 25.6 后续建议

下一步建议：

1. 将生成/评估检索策略加入：
   - `swine_textbook_pages_401_600_repro_respiratory_virus_digest.md`
   - `swine_textbook_pages_201_400_system_digest.md`
   - `swine_textbook_pages_1_200_crosscutting_digest.md`
2. 优先把 `textbook_401_600_repro_respiratory_virus_candidate_facts_20260507.json` 中的 ASF、PCV2、TGE/PRCV、PRV、流产采样和 PRDC facts 回填到 disease/syndrome 页面。
3. 先构建三张 matrix：
   - 繁殖障碍/流产 matrix
   - 呼吸道 PRDC matrix
   - 腹泻冠状病毒/轮状病毒/大肠杆菌/球虫 matrix
4. 继续处理 `601-800.md`，预计将覆盖更多病毒章节和后续单病内容，是解决 disease-specific 页面缺口的下一块关键材料。

## 26. 2026-05-07 增量更新：基于 `raw/md/601-800.md` 的病毒病和早期细菌病章节补充

### 26.1 本次分析对象

本次分析文件：

`knowledge/llm_wiki_swine_authoritative/raw/md/601-800.md`

该文件是 *Diseases of Swine, 11th Edition* 第 601-800 页的 Markdown 转换文本。经章节识别，该段继续并完成流感病毒章节，随后覆盖副黏病毒、细小病毒、瘟病毒、微 RNA 病毒、PRRSV、猪痘、轮状/呼肠病毒、逆转录病毒、弹状病毒、披膜病毒、细菌总论、放线杆菌病和波氏杆菌病开端。相比 `401-600.md`，本段更集中解决当前 wiki 中 disease-specific 单病页事实密度不足的问题，并且对高风险鉴别诊断、采样、检测解释和防控边界有直接价值。

### 26.2 对当前 wiki 缺口的解决能力评估

该文件可以显著补强以下问题：

1. 单病页面正文和事实密度不足
   - 可直接服务 `DIS-021-influenza-viruses.md`、`DIS-022-paramyxoviruses.md`、`DIS-023-parvoviruses.md`、`DIS-024-classical-swine-fever-pestiviruses.md`、`DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md`、`DIS-026-foot-and-mouth-disease-picornaviruses.md`、`DIS-027-senecavirus-a-picornaviruses.md`、`DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`、`DIS-029-swinepox-virus.md`、`DIS-030-rotaviruses-and-reoviruses.md`、`DIS-031-retroviruses.md`、`DIS-032-rabies-virus.md`、`DIS-033-vesicular-stomatitis-viruses.md`、`DIS-034-togaviruses-getah-sagiyama-ross-river-eee.md`、`DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md`、`DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md`、`DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md`。
2. 高风险鉴别诊断不足
   - 本段明确了口蹄疫、猪水疱病、Senecavirus A、水疱性口炎、水疱疹等水疱性疾病不能凭肉眼区分，必须实验室确认。
   - CSF 不能因临床不典型而排除，应与 ASF、败血性细菌病、PRRSV、PDNS、丹毒、沙门氏菌病等鉴别。
   - PRRSV 不能只靠 ORF5/RFLP 标签判断毒力、保护力或完整遗传关系。
3. 实验室诊断和采样建议不足
   - IAV-S 补充了发热急性期鼻/咽拭子、气管、肺、BAL、口腔液等样本边界，以及口腔液更适合群体筛查、分离和测序成功率相对较低的限制。
   - PRRSV 补充了血清、口腔液、processing fluids、组织、BAL、胎儿组织和繁殖材料应按诊断问题选择。
   - App 补充了临床爆发、剖检病变、培养/PCR/分型和带菌猪检测的组合逻辑。
   - Bordetella 补充了鼻拭子、死后肺冲洗、活检、选择培养、PCR 和鼻甲评分。
4. 生成/评估流程 disease-specific checklist 不足
   - 水疱病变回答如果未触发 FMD/SVD/SVA/VS/VES 鉴别和官方检测边界，应判为高风险。
   - IAV-S 回答如果只凭发热咳嗽确诊，或忽略采样时间窗，应判为不足。
   - PRRSV 回答如果把 PCR 阳性等同于单病因，或把 RFLP 当作毒力/保护结论，应判为不足。
   - App 回答如果把抗菌治疗写成清除带菌或根除猪群感染，应判为不足。
   - Bordetella 回答如果把严重进行性萎缩性鼻炎单独归因于 Bordetella，而不提产毒 Pasteurella multocida，应判为不足。
5. 呼吸道、繁殖障碍、腹泻和败血症综合征不足
   - 本段强化了 IAV-S/PRRSV/App/Bordetella 在 PRDC 中的角色。
   - PPV、Menangle、PRRSV、CSF、APPV 等加强了繁殖障碍矩阵。
   - 轮状病毒章节补充了新生/断奶前后腹泻中的绒毛损伤、乳源免疫和混合感染边界。
   - Actinobacillus suis 补充了败血症、猝死、肺炎、胸膜炎、关节炎、脑膜炎、心内膜炎和繁殖问题鉴别。

该文件不能单独解决以下问题：

1. 中国官方动物疫病分类、上报、封锁、扑杀、移动控制、检疫和补偿规则。
2. 中国境内疫苗可及性、兽药标签、剂量、疗程、给药途径、休药期和 MRL。
3. Brucellosis 之后的大量细菌章节、寄生虫、营养缺乏/过量、霉菌毒素和中毒章节。
4. 正式 `exports/differential_matrix.csv/json` 仍未生成。
5. 本次新增 facts 仍是候选层，未直接进入正式 `exports/knowledge_facts.json`。

### 26.3 本次已新增或修改的 wiki 内容

本次新增：

`knowledge/llm_wiki_swine_authoritative/wiki/synthesis/swine_textbook_pages_601_800_viral_bacterial_digest.md`

用途：

- 作为 601-800 页病毒病和早期细菌病章节的派生消化页。
- 支撑单病页回填、病例生成检索、答案评估 checklist 和后续 differential matrix 构建。
- 与前面三个 digest 形成连续链条：`1-200` 偏总论方法，`201-400` 偏系统鉴别，`401-600` 开始进入病毒单病，`601-800` 则补全更多关键病毒病并开始进入细菌性呼吸病。

本次新增候选 facts：

`knowledge/llm_wiki_swine_authoritative/issues/textbook_601_800_viral_bacterial_candidate_facts_20260507.json`

说明：

- 候选 facts 是对教材内容的提炼和改写，不是大段复制。
- 当前仍放在 `issues/` 下作为候选层，等待人工复核后再进入正式 facts。
- 候选 facts 覆盖 IAV-S、蓝眼病、Menangle、Nipah、PPV、CSF、APPV、FMD、Senecavirus A、EMCV、teschovirus、PRRSV、猪痘、轮状病毒、PERV、水疱性口炎、狂犬病、App、A. suis 和 Bordetella。

本次更新：

`knowledge/llm_wiki_swine_authoritative/exports/synthesis_index.csv`

新增了 `swine_textbook_pages_601_800_viral_bacterial_digest` 条目。

本次更新：

`knowledge/llm_wiki_swine_authoritative/log.md`

记录了本次增量维护动作。

### 26.4 本次实际解决的问题

#### 对第 6、7 节“疾病页正文完整性和事实密度不足”的改善

新增 digest 可直接服务 17 个 disease 页面，尤其是 `DIS-021` 至 `DIS-037` 这一批低频病毒和早期细菌病页面。它补充了各病的临床表现、病变、传播、诊断样本、检测边界、免疫/疫苗限制和防控思路，避免这些页面只有目录式描述。

仍未解决：

- 本次没有直接逐页改写 disease 页面，而是先建立可检索 digest 和候选 facts。
- 需要下一步按疾病逐页回填并人工复核证据锚点。

#### 对第 8 节“实验室诊断与采样建议不足”的改善

新增 digest 明确了：

- IAV-S 应在发热急性期采呼吸道样本；口腔液适合群体筛查，但分离和测序成功率不如个体急性呼吸道样本。
- PRRSV 样本选择必须服务于具体问题：急性感染、暴露、监测、繁殖损失或毒株追踪。
- 水疱性疾病必须实验室确认，不能靠肉眼判断 FMD、SVD、SVA、VS 或 VES。
- App 需要结合爆发模式、剖检病变、培养/PCR/分型和带菌猪检测。
- Bordetella 需要把鼻炎、肺炎、鼻甲萎缩和混合感染分开评估。

仍未解决：

- 中国官方送检流程、法定检测机构和监管采样要求仍需 A0/A1 来源补齐。

#### 对第 9 节“鉴别诊断体系不足”的改善

新增 digest 明确了几组高价值鉴别：

- 水疱病变：FMD、SVD、Senecavirus A、水疱性口炎、水疱疹、创伤和化学刺激。
- 繁殖障碍：PPV、PRRSV、PCV2、PRV、JEV、CSF、Menangle、rubulavirus、EMCV、钩端螺旋体、布鲁氏菌和毒素。
- 呼吸道：IAV-S、PRRSV、PRCV、支原体、App、Pasteurella、Bordetella、S. suis、Glasser's disease。
- 新生/断奶腹泻：轮状病毒 A/B/C、PED、TGE、PDCoV、ETEC、梭菌、球虫、沙门氏菌和隐孢子虫。
- 败血症/猝死：A. suis、App、S. suis、Glasser's disease、丹毒、沙门氏菌病等。

仍未解决：

- 正式 matrix export 仍未生成。
- 每个疾病对的 shared signs、distinguishing signs、recommended samples、tests 和 regulatory boundary 仍需结构化。

#### 对第 10 节“防控、上报、禁售、禁运边界不足”的改善

新增 digest 明确了：

- FMD、CSF、水疱性疾病、狂犬病、Nipah 等必须触发高风险边界，不能输出常规治疗、销售或调运建议。
- App 抗菌治疗只是在早期降低死亡和损失，不能清除带菌或根除猪群感染。
- PRRSV 控制是猪群程序问题，需要生物安全、驯化、封群、监测、疫苗决策、test-and-removal 或清除计划，而不是单猪治疗。

仍未解决：

- 中国本地法定处置规则仍必须由官方来源补齐。
- 教材的通用防控原则不能替代中国现场监管流程。

#### 对第 15 节“评估流程仍存在的问题”的改善

新增 digest 可支持 judge 检查：

- 是否错误从临床表现直接确诊 IAV-S、CSF、FMD、PRRSV、App 或 Bordetella。
- 是否在水疱病变中遗漏 FMD/SVD/SVA/VS/VES 鉴别。
- 是否把 PRRSV PCR 阳性直接等同于单一病因。
- 是否把 App 药物治疗写成清除带菌。
- 是否将 Bordetella 单独解释为严重进行性萎缩性鼻炎。
- 是否在药物建议中绕过中国标签、休药期和审慎用药约束。

仍未解决：

- 评估脚本尚未自动加载本次 digest。
- disease-specific checklist 尚未由候选 facts 自动生成。

### 26.5 本次增量后的问题状态变化

| 问题类别 | 本次变化 | 剩余状态 |
|---|---|---|
| disease-specific 病毒内容 | 明显改善 | 需逐页回填 DIS-021 至 DIS-034 |
| PRRSV 内容 | 明显改善 | 需写入 DIS-028 和繁殖/呼吸 syndrome |
| 水疱病高风险鉴别 | 明显改善 | 中国官方处置仍需 A0/A1 |
| IAV-S 采样/检测 | 明显改善 | 需回填 DIS-021 和 PRDC matrix |
| PPV/繁殖障碍 | 明显改善 | 需回填 DIS-023 和繁殖 matrix |
| 轮状病毒腹泻 | 明显改善 | 需回填 DIS-030 和腹泻 matrix |
| App/Bordetella 细菌性呼吸病 | 明显改善 | 需回填 DIS-035 至 DIS-037 |
| 药物/休药期 | 未直接解决 | 仍需标签和官方来源 |
| 中国法规锚点 | 未解决 | 仍需官方来源补充 |
| 正式鉴别矩阵 exports | 未完成 | 需单独生成和校验 |

### 26.6 后续建议

下一步建议：

1. 将生成/评估检索策略加入：
   - `swine_textbook_pages_601_800_viral_bacterial_digest.md`
   - `swine_textbook_pages_401_600_repro_respiratory_virus_digest.md`
   - `swine_textbook_pages_201_400_system_digest.md`
   - `swine_textbook_pages_1_200_crosscutting_digest.md`
2. 优先把 `textbook_601_800_viral_bacterial_candidate_facts_20260507.json` 中的 IAV-S、FMD/SVA/VS、PRRSV、PPV、App 和 Bordetella facts 回填到 disease/syndrome 页面。
3. 优先构建三张高风险 matrix：
   - 水疱性疾病 matrix
   - PRRSV/IAV-S/App/Bordetella 呼吸病 matrix
   - PPV/PRRSV/CSF/JEV/Menangle/PRV 繁殖障碍 matrix
4. 继续处理 `801-1000.md`，重点补齐 Brucellosis 之后的大量细菌病章节，特别是梭菌、大肠杆菌、丹毒、Glasser's disease、钩端螺旋体、支原体、巴氏杆菌、Lawsonia、沙门氏菌、葡萄球菌和链球菌。

## 27. 2026-05-07 增量更新：基于 `raw/md/801-1000.md` 的核心细菌病章节补充

### 27.1 本次分析对象

本次分析文件：

`knowledge/llm_wiki_swine_authoritative/raw/md/801-1000.md`

该文件是 *Diseases of Swine, 11th Edition* 第 801-1000 页的 Markdown 转换文本。该段覆盖猪病 wiki 当前非常缺的细菌病主体内容，包括布鲁氏菌病、梭菌病、大肠杆菌病、丹毒、Glässer's disease、钩端螺旋体病、支原体病、巴氏杆菌病、增生性肠病、沙门氏菌病、葡萄球菌病、链球菌病、猪痢疾/螺旋体性结肠炎，以及结核病开端。

### 27.2 对当前 wiki 缺口的解决能力评估

该文件可以显著补强以下问题：

1. 细菌性单病页面事实密度不足
   - 可直接服务 `DIS-038` 至 `DIS-053`，尤其是布鲁氏菌、梭菌、大肠杆菌、丹毒、Glässer、钩端螺旋体、支原体、巴氏杆菌、Lawsonia、沙门氏菌、葡萄球菌、链球菌、猪痢疾和结核病页面。
2. 腹泻鉴别不足
   - 新生仔猪腹泻可加入 ETEC、C. perfringens type C、C. difficile、轮状病毒、PED/TGE/PDCoV、球虫等。
   - 断奶后腹泻/水肿病可区分 ETEC、EDEC/STEC、Lawsonia、Salmonella、Brachyspira、日粮和寄生虫。
   - 育肥猪大肠性腹泻可区分猪痢疾、B. pilosicoli 结肠炎、增生性肠病、沙门氏菌病、鞭虫和饲料因素。
3. 呼吸道/PRDC 鉴别不足
   - M. hyopneumoniae、Pasteurella multocida、Glässer、S. suis、App、IAV-S、PRRSV、Bordetella 等之间的关系更清楚。
4. 繁殖障碍和公共卫生边界不足
   - Brucella suis、Leptospira、Salmonella、S. suis、S. aureus/MRSA、Mycobacteria 的人兽共患或食品安全边界得到补充。
   - 布鲁氏菌病和钩端螺旋体病可补强流产、返情、不孕、精液/AI、尿液/肾脏和职业暴露框架。
5. 实验室诊断和采样不足
   - 布鲁氏菌补充了培养样本、个体血清学局限和生物安全边界。
   - Glässer 和 S. suis 补充了“上呼吸道携带不等于发病”，需要无菌部位/病变部位样本。
   - E. coli 补充了不能只靠普通培养，要看 pathotype、毒力因子、年龄、病变和综合征。
   - Brachyspira/B. pilosicoli 补充了粪便阳性不能单独确认疾病。
6. 评估流程 disease-specific checklist 不足
   - 可以新增“检测阳性不等于病因”的细菌病评估项。
   - 可以新增“抗菌药不得从教材直接生成剂量/疗程/休药期”的硬边界项。

该文件不能单独解决以下问题：

1. 中国官方布鲁氏菌、结核病、食品安全、职业暴露和动物疫病处置要求。
2. 中国兽药标签、适应证、剂量、疗程、给药途径、休药期和 MRL。
3. 1000 页之后如果还有结核病后续、杂项细菌病、寄生虫、营养、霉菌毒素和中毒章节，仍未覆盖。
4. 正式 differential matrix exports 尚未生成。
5. 本次新增 facts 仍为候选层，未进入正式 `exports/knowledge_facts.json`。

### 27.3 本次已新增或修改的 wiki 内容

本次新增：

`knowledge/llm_wiki_swine_authoritative/wiki/synthesis/swine_textbook_pages_801_1000_core_bacterial_digest.md`

用途：

- 作为 801-1000 页核心细菌病章节的派生消化页。
- 支撑细菌性单病页面回填、病例生成、答案评估 checklist 和后续矩阵构建。
- 与前四个 digest 连续衔接：`1-200` 偏总论，`201-400` 偏系统鉴别，`401-600` 和 `601-800` 偏病毒/早期细菌病，本段进入细菌病主体。

本次新增候选 facts：

`knowledge/llm_wiki_swine_authoritative/issues/textbook_801_1000_core_bacterial_candidate_facts_20260507.json`

说明：

- 候选 facts 是对教材内容的提炼和改写，不是大段复制。
- 当前仍放在 `issues/` 下作为候选层，等待人工复核后再进入正式 facts。
- 候选 facts 覆盖 Brucella suis、C. perfringens type C、E. coli pathotypes、edema disease、erysipelas、Glässer、Leptospira、M. hyopneumoniae、M. suis、P. multocida、Lawsonia、Salmonella、Staphylococcus、S. suis、Brachyspira 和 tuberculosis opening。

本次更新：

`knowledge/llm_wiki_swine_authoritative/exports/synthesis_index.csv`

新增了 `swine_textbook_pages_801_1000_core_bacterial_digest` 条目。

本次更新：

`knowledge/llm_wiki_swine_authoritative/log.md`

记录了本次增量维护动作。

### 27.4 本次实际解决的问题

#### 对第 6、7 节“疾病页正文完整性和事实密度不足”的改善

新增 digest 可直接服务 `DIS-038` 至 `DIS-053`。它补充了细菌性疾病的病原、传播、临床、病变、诊断样本、检测边界、免疫/疫苗限制、防控思路、公共卫生和食品安全边界。

仍未解决：

- 本次没有直接逐页改写 disease 页面，而是先建立可检索 digest 和候选 facts。
- 需要下一步按疾病逐页回填并人工复核证据锚点。

#### 对第 8 节“实验室诊断与采样建议不足”的改善

新增 digest 明确了：

- 布鲁氏菌病文化确诊样本包括阴道分泌物、乳、精液、胎膜、流产胎儿胃内容物/脾/肺、淋巴结、生殖器官等；血清学更适合猪群层面。
- E. coli 诊断应看 pathotype、毒力因子、年龄、病变和综合征，不能靠普通分离直接归因。
- Glässer 和 S. suis 应优先采无菌部位或病变部位；上呼吸道携带不等于系统性疾病。
- Leptospira 应按时相和问题选择血清学、尿液、肾脏、胎盘、胎儿组织或繁殖材料。
- Lawsonia、Brachyspira 和 Salmonella 的粪便/PCR/培养阳性要结合病变和群体背景解释。

仍未解决：

- 中国官方采样、送检和实验室确认程序仍需官方来源补齐。

#### 对第 9 节“鉴别诊断体系不足”的改善

新增 digest 明确了几组高价值鉴别：

- 新生仔猪腹泻：ETEC、C. perfringens type C、C. difficile、轮状病毒、PED/TGE/PDCoV、球虫。
- 断奶后腹泻/水肿病：ETEC、EDEC/STEC、Lawsonia、Salmonella、Brachyspira、日粮、寄生虫。
- 育肥猪血样/黏液样腹泻：猪痢疾、B. pilosicoli 结肠炎、增生性肠病、沙门氏菌、鞭虫和饲料因素。
- 呼吸道：M. hyopneumoniae、Pasteurella、Glässer、App、IAV-S、PRRSV、Bordetella、S. suis。
- 神经/败血症/关节炎：S. suis、Glässer、丹毒、沙门氏菌、E. coli 败血症、水肿病、PRV、盐中毒。
- 繁殖障碍：Brucella、Leptospira、PPV、PRRSV、PCV2、PRV、JEV、CSF 和毒素。

仍未解决：

- 正式 matrix export 仍未生成。
- shared signs、distinguishing signs、recommended samples、tests、regulatory boundary 仍需结构化。

#### 对第 10 节“防控、上报、禁售、禁运边界不足”的改善

新增 digest 明确了：

- Brucella suis、Leptospira、Salmonella、S. suis、MRSA 和 mycobacteria 具有公共卫生或职业暴露边界。
- 抗菌治疗必须受药敏、标签、休药期、MRL、审慎用药和中国法规约束，不能从教材讨论直接生成处方。
- 对携带状态常见的病原，清除/根除不能被简单写成“用药即可解决”。

仍未解决：

- 中国本地法定处置规则仍必须由官方来源补齐。

#### 对第 15 节“评估流程仍存在的问题”的改善

新增 digest 可支持 judge 检查：

- 是否把普通培养/PCR 阳性直接等同于病因。
- 是否忽略无菌部位采样和病变部位采样。
- 是否把 E. coli、Pasteurella、Bordetella、Glässer、S. suis、Brachyspira 等常见携带/机会病原过度归因。
- 是否遗漏布鲁氏菌、钩端螺旋体、沙门氏菌、S. suis、MRSA、结核等公共卫生边界。
- 是否绕过中国标签和休药期生成抗菌药剂量/疗程。

仍未解决：

- 评估脚本尚未自动加载本次 digest。
- disease-specific checklist 尚未由候选 facts 自动生成。

### 27.5 本次增量后的问题状态变化

| 问题类别 | 本次变化 | 剩余状态 |
|---|---|---|
| 细菌性单病内容 | 明显改善 | 需逐页回填 DIS-038 至 DIS-053 |
| 腹泻鉴别 | 明显改善 | 需生成正式 diarrhea matrix |
| 呼吸道/PRDC 细菌鉴别 | 明显改善 | 需回填 syndrome 和 DIS-046/047 |
| 繁殖障碍细菌鉴别 | 明显改善 | 需回填 Brucella/Leptospira 和繁殖 matrix |
| 公共卫生边界 | 明显改善 | 中国官方职业/食品安全规则仍需补 |
| 检测阳性不等于病因 | 明显改善 | 需写入评估脚本和 disease checklist |
| 药物/休药期 | 未直接解决 | 仍需标签和官方来源 |
| 中国法规锚点 | 未解决 | 仍需官方来源补充 |
| 正式鉴别矩阵 exports | 未完成 | 需单独生成和校验 |

### 27.6 后续建议

下一步建议：

1. 将生成/评估检索策略加入：
   - `swine_textbook_pages_801_1000_core_bacterial_digest.md`
   - `swine_textbook_pages_601_800_viral_bacterial_digest.md`
   - `swine_textbook_pages_401_600_repro_respiratory_virus_digest.md`
   - `swine_textbook_pages_201_400_system_digest.md`
   - `swine_textbook_pages_1_200_crosscutting_digest.md`
2. 优先把 `textbook_801_1000_core_bacterial_candidate_facts_20260507.json` 中的 E. coli、Glässer、S. suis、Lawsonia、Brachyspira、Salmonella、Brucella 和 Leptospira facts 回填到 disease/syndrome 页面。
3. 优先构建四张 matrix：
   - 新生仔猪腹泻 matrix
   - 断奶后腹泻/水肿病 matrix
   - 育肥猪大肠性腹泻 matrix
   - 神经/败血症/关节炎 matrix
4. 继续处理 `1001-1200.md`，重点确认结核病是否有后续，并继续补齐杂项细菌病、寄生虫和后续系统章节。
