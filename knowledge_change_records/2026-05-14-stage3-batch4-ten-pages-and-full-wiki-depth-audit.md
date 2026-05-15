# 2026-05-14 Stage3 批次4十页补强与完整 Wiki 证据深度审计记录

## 一、任务背景

用户要求继续补强 10 个高价值疾病页面，并全面细致检查完整猪病 wiki 库，严格评估当前知识库是否能够有效解决 Phase12 抽样证据深度过低、生成样本疾病覆盖不足、低证据页面被误用为高质量正向问答样本的问题。

本次执行仍遵守前序阶段原则：

- 不重写历史页面主体，避免扩大既有编码异常。
- 仅追加 UTF-8 的结构化补强块。
- 每条补强都带 `source_id` 或规则卡锚点。
- 不新增药物剂量、疗程、休药期、MRL、扑杀、调运、屠宰或监管执行命令。
- 低证据页面继续保持 partial/gap-routing 定位，不伪装成完整疾病页。

## 二、修改前存在的问题

1. 部分页面虽有来源索引，但默认内容仍偏“目录级/章节级锚点”，不能直接支撑真实兽医问诊。
2. 低频疾病、低频寄生虫和人畜共患风险页面缺少可用于问诊的实际追问点，例如暴露史、日龄、同群传播、剖检线索、采样确认边界。
3. 生成流程容易把 partial 页面误用为单病因正向 SFT，导致回答过度确定、治疗建议过早、疾病覆盖虚假扩展。
4. 部分历史页面存在编码异常，直接整体重写风险较高，容易引入二次乱码或破坏原有证据索引。

## 三、本次补强的 10 个页面

本批次追加统一小节：

`## Web Access 深度补强 / 2026-05-14 批次4`

补强页面如下：

1. `DIS-001-adenoviruses.md`
   - 强化腺病毒作为低频/偶发检出病原的边界。
   - 明确适合检出结果解释、多病原鉴别，不适合作为单病因高置信处置样本。

2. `DIS-016-west-nile-virus-and-other-flaviviruses.md`
   - 强化西尼罗病毒的鸟-蚊循环、死端宿主和蚊媒暴露问诊边界。
   - 防止把猪群非特异性神经症状直接归因于西尼罗病毒。

3. `DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md`
   - 强化 APPV 与新生仔猪先天性震颤、窝内发病背景的关联。
   - 明确成年猪非特异性神经症状不得泛化为 APPV。

4. `DIS-032-rabies-virus.md`
   - 强化狂犬病作为人畜共患和公共卫生风险页面的硬边界。
   - 明确疑似暴露、神经症状、人员接触必须触发官方/公共卫生/现场兽医评估。

5. `DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md`
   - 强化 A. suis 的败血症、多浆膜炎、关节炎、肺炎等多系统问诊线索。
   - 防止被错误写成单一胸膜肺炎模板。

6. `DIS-053-tuberculosis.md`
   - 强化猪结核的病原范围、淋巴结/肝脾病变、屠检和散养暴露线索。
   - 明确不能把牛结核监管条目直接外推为猪结核处置命令。

7. `DIS-054-miscellaneous-bacterial-infections.md`
   - 明确“杂项细菌感染”不是单一疾病标签。
   - 要求按病变系统和定位追问，否则只能进入采样、培养、PCR、鉴别诊断流程。

8. `DIS-062-strongyloides-internal-parasites.md`
   - 强化 Strongyloides ransomi 与哺乳仔猪、母猪乳汁传播、产房潮湿卫生的关系。
   - 明确不能把成年猪阳性自动解释为当前主诉病因。

9. `DIS-063-metastrongylus-lungworms.md`
   - 强化肺虫病与户外/放牧、蚯蚓中间宿主、慢性咳嗽和剖检支气管虫体的关系。
   - 防止仅凭咳嗽诊断肺虫病。

10. `DIS-064-stephanurus-dentatus-kidney-worm.md`
    - 强化猪肾虫与野猪、散养、户外、温暖气候、尿检虫卵和剖检肾周虫体的关系。
    - 明确封闭集约化猪群中通常不是重要问题。

## 四、代码和文档实际变更

新增或修改内容集中在 10 个疾病页面，均为追加式补强：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-001-adenoviruses.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-016-west-nile-virus-and-other-flaviviruses.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-032-rabies-virus.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-053-tuberculosis.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-054-miscellaneous-bacterial-infections.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-062-strongyloides-internal-parasites.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-063-metastrongylus-lungworms.md`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/diseases/DIS-064-stephanurus-dentatus-kidney-worm.md`

新增本留痕文档：

- `knowledge_change_records/2026-05-14-stage3-batch4-ten-pages-and-full-wiki-depth-audit.md`

本次没有清理历史输出 CSV/JSONL/报告文件，原因是这些文件属于前序真实调用与审计留痕，删除会影响追溯。也没有修改 Phase12/Phase14/Phase18 代码。

## 五、验证结果

使用 `rg` 检查批次4标记，确认 10 个页面均写入：

- `DIS-001-adenoviruses.md`
- `DIS-016-west-nile-virus-and-other-flaviviruses.md`
- `DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md`
- `DIS-032-rabies-virus.md`
- `DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md`
- `DIS-053-tuberculosis.md`
- `DIS-054-miscellaneous-bacterial-infections.md`
- `DIS-062-strongyloides-internal-parasites.md`
- `DIS-063-metastrongylus-lungworms.md`
- `DIS-064-stephanurus-dentatus-kidney-worm.md`

完整疾病库稳定统计如下：

| 指标 | 当前结果 | 严格解释 |
|---|---:|---|
| 疾病页面总数 | 73 | 全库规模未变 |
| partial 页面 | 32 | 仍有较大比例页面不能作为完整正向 SFT 主来源 |
| complete 或非 partial 页面 | 41 | 可优先用于正向疾病问诊样本 |
| 含 Web Access 标记页面 | 42 | 已超过 30 页下限目标 |
| 本批次写入页面 | 10 | 符合“本次最少10种”要求 |
| source 锚点数 >= 5 页面 | 73 | 检索锚点覆盖已经全库达标 |

注意：部分旧页面存在历史编码异常，PowerShell 中文 heading 正则统计不稳定，因此本次不把“中文 facet heading 匹配数”作为唯一验收依据。更可靠的验收依据是页面是否含 Web Access 补强块、是否含 source/rule 锚点、是否补入问诊追问点和使用边界。

## 六、严格评估：是否已经有效解决 wiki 证据深度问题

结论：已经明显缓解，但尚未完全解决。

已经解决或明显改善的部分：

1. 对 Phase12 抽样深度过低的问题有直接帮助。
   - 新增补强块提供了可被检索的问诊线索、暴露史、采样确认、鉴别边界。
   - 覆盖了低频病毒、人畜共患风险、低频细菌、寄生虫等之前容易被生成器写空或写错的页面。

2. 对生成重复和疾病覆盖不足有帮助。
   - 含 Web Access 标记页面已达到 42/73。
   - 已超过前序目标中的 30 页下限，能够给 Phase12 coverage sampling 提供更多候选实体。

3. 对回答安全性和真实性有帮助。
   - 本批次明确约束低证据页面不得直接生成确诊、处方、剂量、休药期和监管处置命令。
   - 对狂犬病、结核、西尼罗病毒等高边界疾病补入了公共卫生/监管边界。

尚未完全解决的部分：

1. partial 页面仍有 32/73。
   - 这些页面可以支持边界问诊、缺口路由、鉴别提示，但不能全部用于高质量正向 SFT。

2. 仍有页面只有边界强化，没有完整临床 facet。
   - 对低频病原这是合理状态，但对生成“丰富、多样、可执行”的问答来说，仍需要 Phase12/Phase14 明确区分 positive SFT 与 boundary/refusal/gap-routing 样本。

3. 证据深度不能只靠页面补字数解决。
   - 必须配合 Phase12 的 coverage sampling、prefer-depth、max-plans-per-entity 和 readiness index。
   - 否则生成器仍可能抽到大量 partial 页面，造成问答单薄或过度保守。

## 七、当前可落地使用建议

建议 Phase12/Phase14 使用如下硬约束：

1. 正向疾病问诊 SFT：
   - 优先选择 complete 或 verified clinical facets 较多的页面。
   - 每 40 条样本中 unique_entities 应不低于 30。
   - 单一 disease_id 的样本数不超过 2，除非用户显式要求专题数据。

2. partial 页面：
   - 仅用于检出结果解释、鉴别诊断、追问、采样、风险提示、边界/拒答/人工复核样本。
   - 不允许生成确定诊断、药物剂量、疗程、休药期、MRL 或监管执行结论。

3. 裁判/仲裁：
   - 对“低证据页面给确定诊断或处方”的样本设置一票否决或强制仲裁。
   - 对“缺少体重、日龄、暴露史、实验室依据仍给执行性方案”的样本强制降分。

## 八、预计效果

本次补强预计能产生以下效果：

1. 40 条生成样本的疾病覆盖范围更容易扩大，不再只集中于少数高频疾病。
2. 对低频疾病的回答会更像真实问诊：先追问、再鉴别、再建议采样/现场兽医，而不是模板化科普。
3. 裁判更容易识别“证据不足却过度处置”的危险样本。
4. Phase12 的 readiness index 和 coverage sampling 有更多页面可作为有效候选。

## 九、剩余目标

前序阶段目标为补齐 30-50 个高价值页面。当前含 Web Access 标记页面为 42 个，已经达到 30 页下限，距离 50 页上限还差约 8 个页面。

建议下一批优先处理仍处于 partial 且低问诊 facet 的页面：

- `DIS-005-bunyaviruses-akabane-lumbo-oya-tahyna.md`
- `DIS-006-caliciviruses-norovirus-sapovirus-vesicular-exanthema-virus.md`
- `DIS-014-filoviruses-reston-ebolavirus-zaire-ebolavirus.md`
- `DIS-019-porcine-cytomegalovirus.md`
- `DIS-020-malignant-catarrhal-fever-ovine-herpesvirus-2.md`
- `DIS-022-paramyxoviruses.md`
- `DIS-031-retroviruses.md`
- `DIS-034-togaviruses-getah-sagiyama-ross-river-eee.md`

这些页面多为低频病毒或边界性病原，下一步不应强行写成完整治疗页，而应继续补“真实问诊能追问什么、不能推断什么、何时需要实验室/官方来源”的证据块。
