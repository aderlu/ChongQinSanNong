# 2026-05-16 Chicken Pharmacopoeia Part 1 Split 3-4 Supplement

## Scope

- Read local Markdown:
  - `ai-/knowledge/llm_wiki_chicken_authoritative/raw/md/中国兽药典一部3.md`
  - `ai-/knowledge/llm_wiki_chicken_authoritative/raw/md/中国兽药典一部4.md`
- Added compact source pages, formal facts, candidate mirrors and disease-page retrieval anchors for Phase3+ retrieval.

## Changes

- Added `SRC-0176` for 中国兽药典 2015 年版一部 3.
- Added `SRC-0177` for 中国兽药典 2015 年版一部 4.
- Added 12 formal facts with prefix `PHARM-2015-P1-3-4-` and 12 candidate mirrors with prefix `CAND-PHARM-2015-P1-3-4-`.
- Updated disease pages: DIS-002 鸡球虫病, DIS-006 大肠杆菌病, DIS-007 坏死性肠炎, DIS-013 鸡支原体病, DIS-021 鸡蛔虫病 and DIS-022 鸡绦虫病.
- Synchronized new formal facts into both `exports/knowledge_facts.json` and `exports/knowledge_facts.csv` so downstream Phase3 runtime builders can retrieve them.

## Runtime Intent

- Chicken coccidiosis retrieval can hit 氯羟吡啶、磺胺氯吡嗪钠、磺胺喹噁啉二甲氧苄啶预混剂 and 磺胺喹噁啉钠 label anchors.
- Gram-negative intestinal infection / 大肠埃希菌 retrieval can hit 硫酸新霉素、硫酸粘菌素 and 复方磺胺氯哒嗪钠 label anchors.
- Chicken mycoplasma and necrotic enteritis retrieval can hit 磷酸泰乐菌素预混剂 label anchors.
- Chicken ascarid and tapeworm retrieval can hit 磷酸哌嗪片 and 氯硝柳胺片 label anchors.
- Excipient-quality retrieval can hit 蛋黄卵磷脂 and 蛋黄卵磷脂（供注射用） quality-standard anchors.

## Boundary

The supplement preserves pharmacopoeia monograph and quality-standard evidence as authoritative label evidence. It does not convert all pharmacopoeia content into unlimited field diagnosis, withdrawal-period, food-safety, regulatory-disposal or clinical-prescription authority.
