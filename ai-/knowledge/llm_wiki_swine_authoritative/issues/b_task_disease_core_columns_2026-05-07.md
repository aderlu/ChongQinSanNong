# B-task disease core columns backfill - 2026-05-07

Scope: appended `## B-task 核心栏目补强` blocks under `wiki/diseases` only.

Columns covered in each touched disease page:
- `传播途径`
- `临床症状`
- `剖检变化`

Evidence rule used: only existing `exports/knowledge_facts.json` facts with explicit `fact_id`, `source_id`, and `PDF page` anchors were used. Boundary-only evidence was written as boundary text rather than complete pathology or transmission claims.

Updated disease pages:
- DIS-004 猪星状病毒感染
- DIS-007 猪圆环病毒相关疾病
- DIS-008 猪流行性腹泻
- DIS-009 猪传染性胃肠炎
- DIS-010 猪δ冠状病毒感染
- DIS-011 猪血凝性脑脊髓炎
- DIS-012 猪呼吸道冠状病毒感染
- DIS-013 猪托罗病毒感染
- DIS-015 猪乙型脑炎
- DIS-018 猪伪狂犬病
- DIS-021 猪流感
- DIS-023 猪细小病毒病
- DIS-024 猪瘟
- DIS-026 猪口蹄疫
- DIS-027 塞内卡病毒A感染
- DIS-028 猪繁殖与呼吸综合征
- DIS-030 猪轮状病毒病
- DIS-033 猪水疱性口炎
- DIS-035 猪胸膜肺炎
- DIS-037 猪萎缩性鼻炎 / Bordetella bronchiseptica
- DIS-039 仔猪梭菌性肠炎
- DIS-041 仔猪黄白痢 / 断奶后大肠杆菌病
- DIS-049 猪沙门氏菌病
- DIS-052 猪痢疾

Validation performed:
- Confirmed 24 disease pages contain the B-task block.
- Confirmed each block contains all three target headings.
- Confirmed each block contains at least one `source_id=` and `PDF page` anchor.

Suggested follow-up validation:
- Run a repository-level link/render check for Markdown pages.
- Review pages where `剖检变化` is intentionally boundary-only: DIS-004, DIS-011, DIS-012, DIS-013, DIS-015, DIS-018, DIS-023, DIS-024, DIS-027, DIS-028, DIS-039.
- In a later pass, map these facts into the canonical non-B-task sections if the project wants to remove duplicate placeholder/V5 areas.
