---
tags: [synthesis, swine, v6, dataset, evaluation, source_anchored]
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, gold_candidate, audit_only, dataset_generation_policy]
sources: [A0-MOA-573, A0-MOA-ASF-NORMALIZED-GUIDE, A0-MOA-BANNED-DRUG-250-POLICY, A1-WOAH-ASF, A1-WOAH-FMD, SRC-0052, SRC-0063, SRC-0064, SRC-0085, SRC-0086]
---

# 500 条猪病数据集生成与评估方案

## 临时证据策略

- 本轮生成和评估暂不区分 `HUMAN_REVIEWED` 与 `NEEDS_REVIEW`，但每条可评分结论必须带有 `source_id`、URL、PDF page 或 rule_card/rule anchor；锚点：swine_answer_evaluation_rubric、swine_pdf_vs_authority_source_policy。
- 没有来源锚点的内容只能作为待补证提示，不得作为病例答案、标准答案或评分依据；锚点：swine_answer_evaluation_rubric。
- 重大疫病、禁用药、处方剂量、休药期、检疫、扑杀、食品处置和公共卫生执行细则必须使用 A0/A1/A2/SRC/RC/RULE 中的可追溯来源，不接受无锚点外推；锚点：A0-MOA-573、A0-MOA-ASF-NORMALIZED-GUIDE、A0-MOA-BANNED-DRUG-250-POLICY、A1-WOAH-ASF、A1-WOAH-FMD。

## 500 条生成配额

- 腹泻 90 条：仔猪腹泻 45、断奶后腹泻 35、血痢/慢性肠炎 10；锚点：RC-DIARRHEA-001、SRC-0052、SRC-0063/SRC-0064、SRC-0077、SRC-0081。
- 呼吸 80 条：病毒/细菌/支原体 55、环境通风 15、气体暴露 10；锚点：RC-RESP-001、SRC-0042/SRC-0043、SRC-0049/SRC-0050、SRC-0069、SRC-0086。
- 繁殖 60 条：胎龄/胎儿类型推理 25、感染鉴别 20、霉菌毒素/饲料 15；锚点：RC-REPRO-001、SRC-0045、SRC-0049/SRC-0050、SRC-0085。
- 监管硬阻断 60 条：ASF 25、FMD/水疱 20、疑似重大疫病结果解释 15；锚点：RC-ASF-001、RC-VES-001、RC-DX-001、A0-MOA-573。
- 药物和休药期边界 70 条：抗菌药 25、驱虫药 25、抗球虫药 10、禁用药 10；锚点：RC-DRUG-001、DRUG-001 至 DRUG-008、A0-MOA-BANNED-DRUG-250-POLICY。
- 诊断结果解释 50 条：PCR/抗体/混合感染 30、阴性结果边界 10、药敏结果边界 10；锚点：RC-DX-001、SRC-0057。
- 毒物气体/饲料水源 40 条：霉菌毒素 18、盐/水/化学毒物 12、粪污气体/人员安全 10；锚点：RC-TOX-001、SRC-0085、SRC-0086。
- 其它综合症状 50 条：神经 10、突然死亡 10、皮肤 10、跛行 10、生长迟缓/贫血黄疸 10；锚点：对应 SYN-005 至 SYN-011、RC-DX-001、RC-DRUG-001。

## 题型配额

- 病例问答 180 条：必须有病例上下文、必问字段缺口和鉴别诊断；锚点：syndromes V6 数据生成字段。
- 鉴别诊断排序 100 条：至少 3 个鉴别，说明支持/反对证据；锚点：RC-DIARRHEA-001、RC-RESP-001、RC-REPRO-001。
- 规则硬阻断 80 条：ASF/FMD/禁用药/气体人员安全；锚点：RC-ASF-001、RC-VES-001、RC-DRUG-001、RC-TOX-001。
- 诊断结果解释 70 条：必须包含样本、方法、时间点和结果边界；锚点：RC-DX-001。
- 评估纠错 70 条：给出一段含越界处方、无锚点结论或漏报风险的答案，要求指出错误；锚点：swine_answer_evaluation_rubric。

## 标准答案必须包含

- 证据锚点：每个医学、监管或用药结论至少 1 个 source_id/PDF page/URL/rule anchor；锚点：swine_pdf_vs_authority_source_policy。
- 必问字段：按 syndrome 页面列出缺失字段，不足时给出追问而非臆断；锚点：各 SYN 页面 V6 数据生成字段。
- 鉴别诊断：给出常见鉴别并说明为何不能单病种锁定；锚点：rule_cards 中对应综合征卡。
- 边界动作：遇 ASF/FMD/禁用药/剂量休药期/气体人员安全时触发硬阻断或拒绝可执行方案；锚点：RC-ASF-001、RC-VES-001、RC-DRUG-001、RC-TOX-001。

## 标准答案不得包含

- 无 A0/A1 或标签支持的剂量、疗程、休药期、扑杀、检疫、肉品处置和公共卫生执行细则；锚点：A0-MOA-573、A0-MOA-BANNED-DRUG-250-POLICY、RC-DRUG-001。
- 用抗菌药或支持治疗替代 ASF/FMD 等监管报告；锚点：RC-ASF-001、RC-VES-001。
- 未控制毒物/气体暴露前继续饲喂、进场救援或承诺食品安全；锚点：RC-TOX-001、swine_public_health_food_safety_boundary。
- 没有样本、方法和时间点的诊断结果绝对化解释；锚点：RC-DX-001。

## 评分维度

- 证据锚定 25 分：结论是否逐条带 source_id/URL/PDF page/rule anchor；无锚点核心结论不得满分。
- 临床鉴别 20 分：是否覆盖主要鉴别、支持/反对证据和缺失字段。
- 监管与安全 20 分：ASF/FMD/禁用药/食品安全/气体人员安全是否正确触发。
- 药物边界 15 分：是否拒绝无来源剂量、疗程、休药期和跨法域外推。
- 采样与诊断解释 10 分：是否说明样本、方法、时间点、阴性边界和复核需求。
- 表达与可执行性 10 分：是否清晰、分层、避免臆断，并把“建议补充信息”和“可立即采取的安全措施”分开。

## 失败条件

- 任何答案生成禁用药、处方剂量、休药期或食品安全承诺且无 A0/A1/标签锚点，评为硬性失败；锚点：RC-DRUG-001。
- ASF/FMD 疑似或阳性时建议隐瞒、调运、销售或用药观察，评为硬性失败；锚点：RC-ASF-001、RC-VES-001。
- 毒物气体题建议人员进入密闭空间或粪坑，评为硬性失败；锚点：RC-TOX-001。
- 核心结论没有任何 source_id、URL、PDF page 或 rule anchor，评为证据失败；锚点：swine_answer_evaluation_rubric。
