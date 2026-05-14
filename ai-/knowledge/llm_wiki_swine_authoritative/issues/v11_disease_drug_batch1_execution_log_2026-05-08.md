# V11 disease/drug batch 1 execution log

- Date: 2026-05-08
- Scope: Disease V11 first batch + Drug V11 label evidence first batch
- Target entities: DIS-008-porcine-epidemic-diarrhea-virus, DIS-009-transmissible-gastroenteritis-virus, DIS-010-porcine-deltacoronavirus, DIS-018-pseudorabies-aujeszky-disease, DIS-021-influenza-viruses, DIS-024-classical-swine-fever-pestiviruses, DIS-026-foot-and-mouth-disease-picornaviruses, DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses, DIS-030-rotaviruses-and-reoviruses, DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia, DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis, DIS-040-colibacillosis, DIS-042-edema-disease-e-coli, DIS-043-erysipelas, DIS-046-mycoplasmosis-enzootic-pneumonia, DIS-049-salmonellosis, DIS-052-swine-dysentery-brachyspira-hyodysenteriae, DIS-055-external-parasites-mange, DIS-057-coccidia-and-other-protozoa, DIS-060-ascaris-suum-internal-parasites; DRUG-010-amoxicillin, DRUG-011-ceftiofur, DRUG-012-florfenicol, DRUG-013-tiamulin, DRUG-015-tylosin, DRUG-018-enrofloxacin, DRUG-019-oxytetracycline, DRUG-021-doxycycline, DRUG-002-ivermectin, DRUG-027-toltrazuril
- Status: partial

## Task scope and required fields

- Entity type: disease + drug
- Required fields: disease diagnosis, differential, transmission/control boundaries, comparison/syndrome links; drug target species, label source, formulation/route/indication boundary, prescription/prohibited/withdrawal/MRL boundary.
- High-risk dimensions: China regulatory status, drug use, withdrawal/MRL, residue, food safety, report/cull/movement/quarantine.
- Required authority levels: A2 accepted for disease clinical/diagnostic reinforcement; A0 required for drug positive label candidates and high-risk China drug claims.

## Web/source search

Web search was executed first under V11. Representative accepted queries included:

| Entity | Query | Result | Accepted source_id | Rejected reason |
|---|---|---|---|---|
| enteric coronaviruses | Merck Veterinary Manual coronaviral enteritis in pigs PED TGE PDCoV | accepted Merck clinical page | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | commercial/secondary snippets rejected |
| respiratory diseases | Merck Veterinary Manual influenza/PRRS/mycoplasmal pneumonia/atrophic rhinitis in pigs | accepted Merck clinical pages | A2-MERCK-INFLUENZA-A-SWINE-2024 and related A2 sources | non-authoritative reposts rejected |
| vesicular disease | Merck Veterinary Manual foot-and-mouth disease pigs vesicular disease | accepted Merck clinical page | A2-MERCK-FMD-ANIMALS-2026 | non-official summaries rejected |
| enteric bacterial/parasitic disease | Merck Veterinary Manual colibacillosis, edema disease, dysentery, coccidiosis, ascaris in pigs | accepted Merck clinical pages | multiple A2-MERCK sources | forums/marketing pages rejected |
| 阿莫西林/头孢噻呋/氟苯尼考/恩诺沙星/托曲珠利 | site:moa.gov.cn active ingredient 兽药 说明书 猪 休药期 | accepted MOA announcements/PDFs when exact label source was opened | A0-MOA-* label sources | source-mismatched or incomplete snippets rejected |
| 泰妙菌素/泰乐菌素/土霉素/多西环素/伊维菌素 | site:moa.gov.cn active ingredient 兽药 说明书 猪 休药期 | exact page-level label not fully registered in this batch | A0-MOA-LABEL-INSTRUCTION-RULES-2002 as hard boundary | not upgraded; exact A0 label still pending |

## New source pages

- `wiki/sources/A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026.md`
- `wiki/sources/A2-MERCK-PSEUDORABIES-PIGS-2026.md`
- `wiki/sources/A2-MERCK-INFLUENZA-A-SWINE-2024.md`
- `wiki/sources/A2-MERCK-CLASSICAL-SWINE-FEVER-2026.md`
- `wiki/sources/A2-MERCK-FMD-ANIMALS-2026.md`
- `wiki/sources/A2-MERCK-PRRS-2026.md`
- `wiki/sources/A2-MERCK-ROTAVIRAL-ENTERITIS-PIGS-2024.md`
- `wiki/sources/A2-MERCK-ACTINOBACILLOSIS-PIGS-2025.md`
- `wiki/sources/A2-MERCK-ATROPHIC-RHINITIS-PIGS-2026.md`
- `wiki/sources/A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS-2024.md`
- `wiki/sources/A2-MERCK-EDEMA-DISEASE-PIGS-2024.md`
- `wiki/sources/A2-MERCK-ERYSIPELAS-SWINE-2026.md`
- `wiki/sources/A2-MERCK-MYCOPLASMAL-PNEUMONIA-PIGS-2024.md`
- `wiki/sources/A2-MERCK-SALMONELLOSIS-ANIMALS-2026.md`
- `wiki/sources/A2-MERCK-SWINE-DYSENTERY-2026.md`
- `wiki/sources/A2-MERCK-MANGE-PIGS-2026.md`
- `wiki/sources/A2-MERCK-COCCIDIOSIS-PIGS-2024.md`
- `wiki/sources/A2-MERCK-ASCARIS-SUUM-PIGS-2024.md`
- `wiki/sources/A0-MOA-AMOXICILLIN-INJECTION-332-2020.md`
- `wiki/sources/A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024.md`
- `wiki/sources/A0-MOA-FLORFENICOL-INJECTION-219-2019.md`
- `wiki/sources/A0-MOA-ENROFLOXACIN-SOLUTION-55-2018.md`
- `wiki/sources/A0-MOA-TOLTRAZURIL-SUSPENSION-216-2019.md`

## Facts extracted from new sources

| fact_id | entity | evidence_source_id | page/span/table | evidence_status |
|---|---|---|---|---|
| V11-DIS-008-etiology | 猪流行性腹泻 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-008-transmission | 猪流行性腹泻 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-008-diagnosis | 猪流行性腹泻 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-009-etiology | 猪传染性胃肠炎 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-009-lesion | 猪传染性胃肠炎 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-009-diagnosis | 猪传染性胃肠炎 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-010-etiology | 猪δ冠状病毒感染 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-010-transmission | 猪δ冠状病毒感染 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-010-diagnosis | 猪δ冠状病毒感染 | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-018-stage-signs | 猪伪狂犬病 | A2-MERCK-PSEUDORABIES-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-018-diagnosis | 猪伪狂犬病 | A2-MERCK-PSEUDORABIES-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-018-boundary | 猪伪狂犬病 | A2-MERCK-PSEUDORABIES-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-021-etiology | 猪流感 | A2-MERCK-INFLUENZA-A-SWINE-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-021-diagnosis | 猪流感 | A2-MERCK-INFLUENZA-A-SWINE-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-021-treatment-boundary | 猪流感 | A2-MERCK-INFLUENZA-A-SWINE-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-024-etiology | 猪瘟 | A2-MERCK-CLASSICAL-SWINE-FEVER-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-024-differential | 猪瘟 | A2-MERCK-CLASSICAL-SWINE-FEVER-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-024-regulatory-boundary | 猪瘟 | A2-MERCK-CLASSICAL-SWINE-FEVER-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-026-etiology | 猪口蹄疫 | A2-MERCK-FMD-ANIMALS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-026-diagnosis | 猪口蹄疫 | A2-MERCK-FMD-ANIMALS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-026-control-boundary | 猪口蹄疫 | A2-MERCK-FMD-ANIMALS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-028-clinical | 猪繁殖与呼吸综合征 | A2-MERCK-PRRS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-028-differential | 猪繁殖与呼吸综合征 | A2-MERCK-PRRS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-028-boundary | 猪繁殖与呼吸综合征 | A2-MERCK-PRRS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-030-etiology | 猪轮状病毒病 | A2-MERCK-ROTAVIRAL-ENTERITIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-030-diagnosis | 猪轮状病毒病 | A2-MERCK-ROTAVIRAL-ENTERITIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-030-differential | 猪轮状病毒病 | A2-MERCK-ROTAVIRAL-ENTERITIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-035-etiology | 猪胸膜肺炎 | A2-MERCK-ACTINOBACILLOSIS-PIGS-2025 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-035-stage-risk | 猪胸膜肺炎 | A2-MERCK-ACTINOBACILLOSIS-PIGS-2025 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-035-drug-boundary | 猪胸膜肺炎 | A2-MERCK-ACTINOBACILLOSIS-PIGS-2025 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-037-etiology | 猪萎缩性鼻炎 | A2-MERCK-ATROPHIC-RHINITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-037-differential | 猪萎缩性鼻炎 | A2-MERCK-ATROPHIC-RHINITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-037-boundary | 猪萎缩性鼻炎 | A2-MERCK-ATROPHIC-RHINITIS-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-040-etiology | 猪大肠杆菌病 | A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-040-diagnosis | 猪大肠杆菌病 | A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-040-drug-boundary | 猪大肠杆菌病 | A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-042-etiology | 仔猪水肿病 | A2-MERCK-EDEMA-DISEASE-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-042-clinical | 仔猪水肿病 | A2-MERCK-EDEMA-DISEASE-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-042-control-boundary | 仔猪水肿病 | A2-MERCK-EDEMA-DISEASE-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-043-clinical | 猪丹毒 | A2-MERCK-ERYSIPELAS-SWINE-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-043-differential | 猪丹毒 | A2-MERCK-ERYSIPELAS-SWINE-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-043-diagnosis | 猪丹毒 | A2-MERCK-ERYSIPELAS-SWINE-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-046-etiology | 猪支原体肺炎 | A2-MERCK-MYCOPLASMAL-PNEUMONIA-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-046-diagnosis | 猪支原体肺炎 | A2-MERCK-MYCOPLASMAL-PNEUMONIA-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-046-control-boundary | 猪支原体肺炎 | A2-MERCK-MYCOPLASMAL-PNEUMONIA-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-049-diagnosis | 猪沙门氏菌病 | A2-MERCK-SALMONELLOSIS-ANIMALS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-049-drug-boundary | 猪沙门氏菌病 | A2-MERCK-SALMONELLOSIS-ANIMALS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-049-food-safety | 猪沙门氏菌病 | A2-MERCK-SALMONELLOSIS-ANIMALS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-052-clinical | 猪痢疾 | A2-MERCK-SWINE-DYSENTERY-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-052-diagnosis | 猪痢疾 | A2-MERCK-SWINE-DYSENTERY-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-052-differential | 猪痢疾 | A2-MERCK-SWINE-DYSENTERY-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-055-etiology | 猪疥螨病 | A2-MERCK-MANGE-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-055-transmission | 猪疥螨病 | A2-MERCK-MANGE-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-055-drug-boundary | 猪疥螨病 | A2-MERCK-MANGE-PIGS-2026 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-057-etiology | 猪球虫病 | A2-MERCK-COCCIDIOSIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-057-diagnosis | 猪球虫病 | A2-MERCK-COCCIDIOSIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-057-drug-boundary | 猪球虫病 | A2-MERCK-COCCIDIOSIS-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-060-etiology | 猪蛔虫病 | A2-MERCK-ASCARIS-SUUM-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-060-diagnosis | 猪蛔虫病 | A2-MERCK-ASCARIS-SUUM-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DIS-060-control-boundary | 猪蛔虫病 | A2-MERCK-ASCARIS-SUUM-PIGS-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-010-label-scope | Amoxicillin / 阿莫西林 | A0-MOA-AMOXICILLIN-INJECTION-332-2020 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-010-route-indication | Amoxicillin / 阿莫西林 | A0-MOA-AMOXICILLIN-INJECTION-332-2020 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-010-prescription-withdrawal | Amoxicillin / 阿莫西林 | A0-MOA-AMOXICILLIN-INJECTION-332-2020 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-010-boundary | Amoxicillin / 阿莫西林 | A0-MOA-AMOXICILLIN-INJECTION-332-2020 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-011-label-scope | Ceftiofur / 头孢噻呋 | A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-011-route-indication | Ceftiofur / 头孢噻呋 | A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-011-withdrawal | Ceftiofur / 头孢噻呋 | A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-011-boundary | Ceftiofur / 头孢噻呋 | A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-012-label-scope | Florfenicol / 氟苯尼考 | A0-MOA-FLORFENICOL-INJECTION-219-2019 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-012-route-indication | Florfenicol / 氟苯尼考 | A0-MOA-FLORFENICOL-INJECTION-219-2019 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-012-withdrawal | Florfenicol / 氟苯尼考 | A0-MOA-FLORFENICOL-INJECTION-219-2019 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-012-boundary | Florfenicol / 氟苯尼考 | A0-MOA-FLORFENICOL-INJECTION-219-2019 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-013-label-gap | Tiamulin / 泰妙菌素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-013-boundary | Tiamulin / 泰妙菌素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-015-label-gap | Tylosin / 泰乐菌素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-015-boundary | Tylosin / 泰乐菌素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-018-label-scope | Enrofloxacin / 恩诺沙星 | A0-MOA-ENROFLOXACIN-SOLUTION-55-2018 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-018-route-indication | Enrofloxacin / 恩诺沙星 | A0-MOA-ENROFLOXACIN-SOLUTION-55-2018 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-018-withdrawal | Enrofloxacin / 恩诺沙星 | A0-MOA-ENROFLOXACIN-SOLUTION-55-2018 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-018-boundary | Enrofloxacin / 恩诺沙星 | A0-MOA-ENROFLOXACIN-SOLUTION-55-2018 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-019-label-gap | Oxytetracycline / 土霉素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-019-boundary | Oxytetracycline / 土霉素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-021-label-gap | Doxycycline / 多西环素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-021-boundary | Doxycycline / 多西环素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-002-label-gap | Ivermectin / 伊维菌素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-002-boundary | Ivermectin / 伊维菌素 | A0-MOA-LABEL-INSTRUCTION-RULES-2002 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-027-label-scope | Toltrazuril / 托曲珠利 | A0-MOA-TOLTRAZURIL-SUSPENSION-216-2019 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-027-route-indication | Toltrazuril / 托曲珠利 | A0-MOA-TOLTRAZURIL-SUSPENSION-216-2019 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-027-withdrawal | Toltrazuril / 托曲珠利 | A0-MOA-TOLTRAZURIL-SUSPENSION-216-2019 | source page usable claims | HUMAN_REVIEWED |
| V11-DRUG-027-boundary | Toltrazuril / 托曲珠利 | A0-MOA-TOLTRAZURIL-SUSPENSION-216-2019 | source page usable claims | HUMAN_REVIEWED |

## Entity pages changed

- `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`
- `wiki/diseases/DIS-010-porcine-deltacoronavirus.md`
- `wiki/diseases/DIS-018-pseudorabies-aujeszky-disease.md`
- `wiki/diseases/DIS-021-influenza-viruses.md`
- `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- `wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md`
- `wiki/diseases/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`
- `wiki/diseases/DIS-030-rotaviruses-and-reoviruses.md`
- `wiki/diseases/DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md`
- `wiki/diseases/DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md`
- `wiki/diseases/DIS-040-colibacillosis.md`
- `wiki/diseases/DIS-042-edema-disease-e-coli.md`
- `wiki/diseases/DIS-043-erysipelas.md`
- `wiki/diseases/DIS-046-mycoplasmosis-enzootic-pneumonia.md`
- `wiki/diseases/DIS-049-salmonellosis.md`
- `wiki/diseases/DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md`
- `wiki/diseases/DIS-055-external-parasites-mange.md`
- `wiki/diseases/DIS-057-coccidia-and-other-protozoa.md`
- `wiki/diseases/DIS-060-ascaris-suum-internal-parasites.md`
- `wiki/drugs/DRUG-010-amoxicillin.md`
- `wiki/drugs/DRUG-011-ceftiofur.md`
- `wiki/drugs/DRUG-012-florfenicol.md`
- `wiki/drugs/DRUG-013-tiamulin.md`
- `wiki/drugs/DRUG-015-tylosin.md`
- `wiki/drugs/DRUG-018-enrofloxacin.md`
- `wiki/drugs/DRUG-019-oxytetracycline.md`
- `wiki/drugs/DRUG-021-doxycycline.md`
- `wiki/drugs/DRUG-002-ivermectin.md`
- `wiki/drugs/DRUG-027-toltrazuril.md`

## Comparison/rule/synthesis pages changed

- None. Existing comparison/syndrome/rule anchors were linked from V11 entity sections; no matrix claims were changed.

## Validation

- source pages added/updated: 23
- source index updated: yes
- facts added/updated: 90
- disease entity pages with new anchors: 20
- drug entity pages with new anchors: 10
- comparison links: each disease V11 block links at least one syndrome and one comparison
- high-risk gate result: unsupported China regulatory, dose, course, withdrawal/MRL, residue and food-safety claims remain blocked unless exact A0 is present
- drug promotions: DRUG-010-amoxicillin, DRUG-011-ceftiofur, DRUG-012-florfenicol, DRUG-018-enrofloxacin, DRUG-027-toltrazuril
- drug pages kept boundary_only: DRUG-013-tiamulin, DRUG-015-tylosin, DRUG-019-oxytetracycline, DRUG-021-doxycycline, DRUG-002-ivermectin
- unresolved gaps: disease-specific China A0 status remains pending for many non-statutory pages; drug pages kept boundary_only require exact product label/registration/MRL confirmation before upgrade

## Stop-condition check

- Web search executed first: yes
- Adopted web sources opened and classified: yes
- Source pages created/indexed before entity claims: yes
- Facts extracted from new sources: yes
- Entity pages updated: yes
- Remaining gaps recorded: yes
- High-risk unsupported claims blocked: yes
- Status note: partial because this is the first batch, not full-coverage completion.
