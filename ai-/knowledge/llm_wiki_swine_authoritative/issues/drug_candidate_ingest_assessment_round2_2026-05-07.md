# Drug Candidate Ingest Assessment Round 2 - 2026-05-07

## 本次处理

- 根据并发 PDF 子任务二次抽取结果，新增 `DRUG-037` 到 `DRUG-070`，共 34 个页面。
- 重点补齐被药物大类掩盖的具体药物名、复方组合、历史用药和高风险/禁用边界项。
- 更新 `exports/drug_page_index.csv` 和 `exports/source_index.csv`。

## 高风险边界

- `DRUG-047-chloramphenicol`、`DRUG-048-carbadox`、`DRUG-049-olaquindox`、`DRUG-050-dimetridazole-ronidazole`、`DRUG-070-ractopamine` 标记为 `prohibited_boundary` 或高风险候选。
- 这些页面只用于禁用/停用/风险识别，不作为可用治疗药。

## 解析结论

- PyMuPDF 对正文候选召回效率最高；pdfplumber 对该 PDF 表格线识别有限，适合作为文本 spot check，不适合作为唯一表格来源。
- 建议后续把候选词典拆成：抗菌药、驱虫/外寄生虫、抗球虫、NSAID/支持治疗、繁殖管理药、高风险禁用边界六类。

## 未升级事项

- 未写入 `exports/knowledge_facts.json`。
- 未生成剂量、疗程、给药途径或休药期。
- 未把国外/教材标签外推为中国可用结论。
