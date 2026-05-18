# 2026-05-16 Chicken Pharmacopoeia Part 1 Split 1-2 Supplement

## Scope

- Read local Markdown:
  - `ai-/knowledge/llm_wiki_chicken_authoritative/raw/md/中国兽药典一部1.md`
  - `ai-/knowledge/llm_wiki_chicken_authoritative/raw/md/中国兽药典一部2.md`
- Added compact source pages, formal facts and candidate mirrors for Phase3+ retrieval.

## Changes

- Added `SRC-0174` for 一部1: pharmacopoeia general monograph semantics and chicken/poultry-relevant monograph anchors.
- Added `SRC-0175` for 一部2: chicken/poultry-relevant monograph anchors.
- Added 15 formal facts with prefix `PHARM-2015-P1-1-2-` and 15 candidate mirrors with prefix `CAND-PHARM-2015-P1-1-2-`.
- Added concise disease-page anchors to DIS-002 鸡球虫病, DIS-006 大肠杆菌病, DIS-013 鸡支原体病, DIS-021 鸡蛔虫病 and DIS-022 鸡绦虫病.

## Runtime Intent

The new facts are deliberately structured for downstream retrieval:

- chicken coccidiosis can hit 二硝托胺、马度米星铵、地克珠利、癸氧喹酯、氨丙啉复方和盐霉素钠 label anchors;
- bacterial and gram-negative intestinal infection retrieval can hit 阿莫西林、恩诺沙星 and 硫酸安普霉素 label anchors;
- mycoplasma/chronic respiratory disease retrieval can hit 泰妙菌素、替米考星、硫氰酸红霉素 and 恩诺沙星 label anchors;
- helminth retrieval can hit 芬苯达唑 and 阿苯达唑 label anchors;
- organophosphate poisoning retrieval can hit 硫酸阿托品注射液 label anchors.

## Boundary

The supplement preserves pharmacopoeia monograph evidence as authoritative label/quality-standard evidence. It does not convert all pharmacopoeia content into unlimited field diagnosis, withdrawal-period, food-safety, regulatory-disposal or clinical-prescription authority.
