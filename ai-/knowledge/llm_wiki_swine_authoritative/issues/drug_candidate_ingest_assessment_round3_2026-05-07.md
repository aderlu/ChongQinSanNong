# Drug Candidate Ingest Assessment Round 3 - 2026-05-07

## 本次处理

- 根据 PDF 深度解析子任务，新增 `DRUG-071` 到 `DRUG-076`，共 6 个单列药物页面。
- 新增药物：streptomycin、tildipirosin、erythromycin、amikacin、praziquantel、dichlorvos。
- 更新 `exports/drug_page_index.csv`。

## 入库边界

- 全部为 `NEEDS_REVIEW`。
- `streptomycin`、`amikacin`、`dichlorvos` 标记为高复核。
- `praziquantel` 仅作为 Taenia solium 公共卫生生命周期边界，不从人终宿主治疗外推为猪治疗。
- 未写入 `exports/knowledge_facts.json`。
