# 2026-05-14 Wiki 真实乱码标题修复与 partial 页面 fact_id 深度补强记录

## 一、修改背景

用户要求：

1. 修复 `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-027-senecavirus-a-picornaviruses.md:11` 的真实乱码标题。
2. 对 `partial 且 fact_id < 3` 的页面继续补强，优先补临床症状、传播/暴露、实验室诊断、鉴别、问诊追问点。

此前库级审查显示：

- 疾病页面总数为 73。
- partial 页面为 32。
- 所有页面都能按 UTF-8 解码，说明不是全库编码损坏。
- `DIS-027-senecavirus-a-picornaviruses.md` 存在真实标题乱码。
- 有一批 partial 页面虽然有 `source_id` 或规则卡锚点，但缺少可被 Phase12/Phase14/裁判稳定识别的 `fact_id` 事实单元。

## 二、修改前问题

### 1. DIS-027 标题乱码

修改前标题为：

```md
# 濉炲唴鍗＄梾姣扐鎰熸煋
```

该问题会影响：

- 疾病实体可读性。
- CSV 样本中的 disease/title 展示。
- 抽样、审查和人工汇报时的识别。

### 2. partial 页面事实单元不足

命中条件为：

```text
partial 页面且 fact_id < 3
```

这类页面虽然已有来源锚点，但生成器和裁判难以稳定识别其可用事实边界，容易产生：

- 低证据页面被误用为确定诊断样本。
- 问诊缺少追问点。
- 回答过早进入处方、剂量或处置。
- 裁判难以依据具体事实单元判定是否过度外推。

## 三、实际修改内容

### 1. 修复真实乱码标题

文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-027-senecavirus-a-picornaviruses.md`

修改后标题：

```md
# 塞内卡病毒A感染
```

### 2. 对 partial 且 fact_id < 3 页面追加 fact_id 补强块

统一追加小节：

```md
## fact_id 补强 / 2026-05-14
```

每个页面至少追加 3 条结构化 fact 单元，覆盖以下类型：

- 疾病/页面使用定位。
- 真实问诊应追问的信息。
- 诊断、鉴别、实验室确认或暴露史边界。
- 不得生成处方、剂量、疗程、休药期、MRL 或监管执行结论的限制。

本次补强页面包括：

- `DIS-001-adenoviruses.md`
- `DIS-003-anelloviruses-torque-teno-sus-viruses.md`
- `DIS-005-bunyaviruses-akabane-lumbo-oya-tahyna.md`
- `DIS-006-caliciviruses-norovirus-sapovirus-vesicular-exanthema-virus.md`
- `DIS-014-filoviruses-reston-ebolavirus-zaire-ebolavirus.md`
- `DIS-016-west-nile-virus-and-other-flaviviruses.md`
- `DIS-017-hepatitis-e-virus.md`
- `DIS-019-porcine-cytomegalovirus.md`
- `DIS-020-malignant-catarrhal-fever-ovine-herpesvirus-2.md`
- `DIS-022-paramyxoviruses.md`
- `DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md`
- `DIS-029-swinepox-virus.md`
- `DIS-031-retroviruses.md`
- `DIS-032-rabies-virus.md`
- `DIS-034-togaviruses-getah-sagiyama-ross-river-eee.md`
- `DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md`
- `DIS-054-miscellaneous-bacterial-infections.md`
- `DIS-062-strongyloides-internal-parasites.md`
- `DIS-063-metastrongylus-lungworms.md`
- `DIS-064-stephanurus-dentatus-kidney-worm.md`
- `DIS-065-nutrient-deficiencies-and-excesses.md`
- `DIS-069-zearalenone-toxicosis.md`
- `DIS-070-fumonisin-toxicosis.md`
- `DIS-071-toxic-minerals-chemicals-plants-and-gases.md`
- `DIS-072-nitrite-toxicosis.md`

## 四、修改原则

本次修改采取保守追加策略：

- 不重写历史主体内容。
- 不删除旧证据索引。
- 不修改 Phase12/Phase14/Phase18 代码。
- 不新增药物剂量、疗程、休药期、MRL。
- 不新增扑杀、检疫、调运、食用安全等执行性监管命令。
- 所有新增事实均保留 `fact_id` 与 `source_id` 或规则卡锚点。

这样做的原因是：当前目标不是把 partial 页面伪装成 complete 页面，而是让 partial 页面更适合作为“追问、鉴别、边界、采样、低置信解释”样本来源。

## 五、验收结果

已执行检查：

```text
remaining_partial_fact_lt3=0
```

含义：

- 当前已经不存在 `partial 且 fact_id < 3` 的疾病页面。

DIS-027 标题复核结果：

```md
# 塞内卡病毒A感染
```

## 六、预期效果

1. Phase12 抽样时，partial 页面拥有更稳定的 fact 单元，可用于深度排序和样本类型区分。
2. Phase14 生成时，低频页面更容易生成真实问诊风格：先追问、再鉴别、再采样/转诊，而不是直接确诊和处方。
3. Phase18 裁判/仲裁可依据 `fact_id` 判定回答是否过度外推、是否缺少关键信息、是否触碰处方或监管边界。
4. CSV 结果中的疾病标题可读性提高，DIS-027 不再因乱码影响人工审查和汇报。

## 七、剩余风险

1. `fact_id >= 3` 代表结构化事实单元达标，不等于页面已变为 complete。
2. partial 页面仍应限制用途，不能直接作为高质量正向处置型 SFT 的主来源。
3. 若后续目标是继续提升正向问诊样本比例，还需要补充更强的临床症状、剖检、实验室诊断和防控证据，并更新 readiness index 或 Phase12 分层规则。
