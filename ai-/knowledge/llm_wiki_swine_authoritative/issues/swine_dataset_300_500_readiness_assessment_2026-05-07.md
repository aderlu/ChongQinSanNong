# Swine Dataset 300-500 Readiness Assessment - 2026-05-07

## 结论

当前系统可以基于猪病 LLM Wiki 先构建约 300 条可审计、可用于训练/微调候选的数据。

不建议直接生成 500 条高质量金标数据。原因不是生成框架不够，而是疾病页核心栏目覆盖仍不均衡：诊断、鉴别诊断、防控要点的 source-anchored 覆盖偏低，直接扩到 500 会增加无证据推断、弱病例和重复模板化样本。

## 当前可支撑内容

- disease pages: 73
- drug pages: 76
- sources: 106
- rule cards: 8
- syndromes: 12
- knowledge facts: 1465
- source-anchored facts: 1319
- PDF treatment candidate matrix: 178 rows
- high-review treatment/drug-risk rows: 30

## 生成与评估系统依据

系统已有以下能力：

- `build_llm_wiki_context()` 同时检索 Markdown 页面与 `knowledge_facts.json` 结构化事实。
- 生成 prompt 会附加 LLM Wiki 上下文，要求禁用药、休药期、报告/隔离等高风险内容在上下文不足时保守回答。
- 评估 prompt 同样可附加 Wiki 上下文。
- `build_wiki_audit_metadata()` 会记录 wiki_dir、fact/page 数、source_ids、evidence_status_counts、context chars。
- `swine_500_dataset_generation_evaluation_plan.md` 已定义 500 条配额、题型配额、评分维度和硬失败条件。

## 主要短板

readiness audit 显示：

- disease median length: 2069 chars
- disease pages under 2500 chars: 45 / 73
- 实验室诊断 sourced: 4 / 73
- 鉴别诊断 sourced: 6 / 73
- 防控要点 sourced: 3 / 73

这意味着系统能生成病例问答和规则硬阻断题，但若大量生成“诊断结果解释、鉴别诊断排序、防控方案、药物治疗方案”，不少页面会依赖综合页或候选矩阵，而不是疾病页本身的成熟证据。

## 推荐第一阶段：300 条

安全可落地配额：

- 腹泻综合征：55
- 呼吸综合征：45
- 繁殖障碍：35
- 监管硬阻断：45
- 药物/禁用/休药期边界：45
- 诊断结果解释：30
- 毒物/饲料/气体：25
- 其它综合征：20

题型比例：

- 病例问答：100
- 鉴别诊断排序：55
- 规则硬阻断：55
- 诊断结果解释：35
- 评估纠错：55

第一阶段每条样本必须保留：

- wiki_context_query
- wiki_evidence_source_ids
- wiki_evidence_status_counts
- target disease / syndrome
- required anchors
- hard-fail flags
- generation model and judge model metadata

## 500 条前置补强

若要稳定扩到 500，建议先补：

1. 疾病页回填

- 优先补 20 个高频/高价值疾病页的 `实验室诊断`、`鉴别诊断`、`防控要点`。
- 优先疾病：colibacillosis、edema disease、erysipelas、Glasser disease、leptospirosis、mycoplasmosis、pasteurellosis、proliferative enteropathy、salmonellosis、staphylococcosis、streptococcosis、swine dysentery、mange、coccidiosis、internal parasites、ASF、FMD、PRRS、PED、CSF。

2. 候选矩阵转候选事实

- 将 `swine_pdf_treatment_candidate_matrix_2026-05-07.csv` 中 `treatment_or_control_candidate` 与 `susceptibility_candidate` 行转成 `issues/*candidate_facts.json`。
- 保持 `NEEDS_REVIEW`，不直接写入 `knowledge_facts.json`。

3. 规则卡扩充

- 增加 ceftiofur/cefquinome/fluoroquinolones/colistin 高重要抗菌药审慎规则。
- 增加 tiamulin/valnemulin 与 ionophore 致死相互作用规则。
- 增加 carbadox/olaquindox/nitroimidazole/chloramphenicol/ractopamine 禁用或高风险阻断规则。

4. 来源缓存补全

- Merck 页面当前普通下载器返回 403，需用浏览器或人工保存正文快照。
- FDA Green Book 需使用 Animal Drugs @ FDA 查询/API 或人工导出产品标签。
- 第278号旧链接 404，需找官方可访问替代入口或保留为失效来源。

## 可执行流程

1. 运行 readiness audit：

```powershell
python D:\XF-ChongQin\ai-\scripts\audit_swine_wiki_dataset_readiness.py
```

2. 建立 swine 专用 config：

- `rule_base.llm_wiki_dir = knowledge/llm_wiki_swine_authoritative`
- `knowledge_base_file = knowledge/llm_wiki_swine_authoritative/exports/knowledge_facts.json`
- `species = 猪`
- 输出文件改为 `results/swine_disease_dataset_{timestamp}.csv`

3. 先跑 30 条 pilot：

- 覆盖 8 类配额。
- 要求每条至少 2 个 source/rule anchors。
- 自动剔除无 source_id、无鉴别、越界剂量/休药期、禁用药误推荐样本。

4. 人工抽审 30 条：

- 通过率 >= 80% 后扩到 100。
- 100 条通过率 >= 85% 后扩到 300。
- 300 条稳定后再补知识库，扩到 500。

5. 500 条放行条件：

- disease pages under 2500 chars 降到 <= 20。
- 实验室诊断 sourced >= 35 / 73。
- 鉴别诊断 sourced >= 35 / 73。
- 防控要点 sourced >= 30 / 73。
- 规则卡 >= 14。
- 药物高风险规则覆盖 cephalosporins、fluoroquinolones、colistin、pleuromutilin-ionophore、banned/stopped drugs。

## 最终建议

- 现在可以启动 300 条“候选训练集/微调集”生产，但必须带审计字段和硬失败过滤。
- 500 条金标级数据集需要先补疾病页诊断/鉴别/防控栏目，以及药物高风险规则卡。
