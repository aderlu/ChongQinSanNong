# Swine LLM Wiki gap audit

- Date: 2026-05-08
- Scope: wiki/diseases and wiki/drugs
- Detail CSV: `issues\swine_wiki_gap_audit_2026-05-08.csv`

## Summary

- disease_has_a0_moa: 27
- disease_has_raw_moa_saved: 11
- disease_needs_review: 73
- disease_pages: 73
- drug_has_a0_moa: 69
- drug_has_raw_moa_saved: 14
- drug_needs_review: 68
- drug_pages: 76

## Highest priority gaps

- severity=6 | drug | Praziquantel / 吡喹酮 | `wiki\drugs\DRUG-075-praziquantel.md` | drug_needs_review;drug_a0_moa_missing
- severity=3 | drug | Altrenogest / 烯丙孕素 | `wiki\drugs\DRUG-068-altrenogest.md` | drug_needs_review
- severity=3 | drug | Amikacin / 阿米卡星 | `wiki\drugs\DRUG-074-amikacin.md` | drug_needs_review
- severity=3 | drug | Aminoglycosides / 氨基糖苷类 | `wiki\drugs\DRUG-033-aminoglycosides.md` | drug_needs_review
- severity=3 | drug | Amitraz / 双甲脒 | `wiki\drugs\DRUG-058-amitraz.md` | drug_needs_review
- severity=3 | drug | Amoxicillin / 阿莫西林 | `wiki\drugs\DRUG-010-amoxicillin.md` | drug_needs_review
- severity=3 | drug | Amoxicillin/clavulanic acid / 阿莫西林克拉维酸 | `wiki\drugs\DRUG-043-amoxicillin-clavulanic-acid.md` | drug_needs_review
- severity=3 | drug | Ampicillin / 氨苄西林 | `wiki\drugs\DRUG-042-ampicillin.md` | drug_needs_review
- severity=3 | drug | Amprolium HCl / 盐酸氨丙啉 | `wiki\drugs\DRUG-062-amprolium.md` | drug_needs_review
- severity=3 | drug | Anticoccidials / 抗球虫药 | `wiki\drugs\DRUG-006-anticoccidials.md` | drug_a0_moa_missing
- severity=3 | drug | Apramycin / 安普霉素 | `wiki\drugs\DRUG-025-apramycin.md` | drug_needs_review
- severity=3 | drug | Avermectins / 阿维菌素类 | `wiki\drugs\DRUG-001-avermectins.md` | drug_a0_moa_missing
- severity=3 | drug | Bacitracin methylene disalicylate / 亚甲基双水杨酸杆菌肽 | `wiki\drugs\DRUG-053-bacitracin-methylene-disalicylate.md` | drug_needs_review
- severity=3 | drug | Benzimidazoles / 苯并咪唑类 | `wiki\drugs\DRUG-005-benzimidazoles.md` | drug_a0_moa_missing
- severity=3 | drug | Beta-lactams / β-内酰胺类 | `wiki\drugs\DRUG-035-beta-lactams.md` | drug_needs_review
- severity=3 | drug | Cefquinome / 头孢喹肟 | `wiki\drugs\DRUG-044-cefquinome.md` | drug_needs_review
- severity=3 | drug | Ceftiofur / 头孢噻呋 | `wiki\drugs\DRUG-011-ceftiofur.md` | drug_needs_review
- severity=3 | drug | Danofloxacin / Marbofloxacin / 达氟沙星/马波沙星 | `wiki\drugs\DRUG-051-danofloxacin-marbofloxacin.md` | drug_needs_review
- severity=3 | drug | Dexamethasone / 地塞米松 | `wiki\drugs\DRUG-066-dexamethasone.md` | drug_needs_review
- severity=3 | drug | Dichlorvos / 敌敌畏 | `wiki\drugs\DRUG-076-dichlorvos.md` | drug_needs_review
- severity=3 | drug | Doramectin / 多拉菌素 | `wiki\drugs\DRUG-003-doramectin.md` | drug_a0_moa_missing
- severity=3 | drug | Erythromycin / 红霉素 | `wiki\drugs\DRUG-073-erythromycin.md` | drug_needs_review
- severity=3 | drug | Fenbendazole / 芬苯达唑 | `wiki\drugs\DRUG-004-fenbendazole.md` | drug_a0_moa_missing
- severity=3 | drug | Flunixin meglumine / 氟尼辛葡甲胺 | `wiki\drugs\DRUG-064-flunixin-meglumine.md` | drug_needs_review
- severity=3 | drug | Gentamicin / 庆大霉素 | `wiki\drugs\DRUG-023-gentamicin.md` | drug_needs_review
- severity=3 | drug | Iron dextran / 右旋糖酐铁 | `wiki\drugs\DRUG-028-iron-dextran.md` | drug_needs_review
- severity=3 | drug | Ivermectin / 伊维菌素 | `wiki\drugs\DRUG-002-ivermectin.md` | drug_a0_moa_missing
- severity=3 | drug | Ketoprofen / Sodium salicylate / Indomethacin / 酮洛芬/水杨酸钠/吲哚美辛 | `wiki\drugs\DRUG-065-ketoprofen-sodium-salicylate-indomethacin.md` | drug_needs_review
- severity=3 | drug | Levamisole / 左旋咪唑 | `wiki\drugs\DRUG-056-levamisole.md` | drug_needs_review
- severity=3 | drug | Lincomycin / 林可霉素 | `wiki\drugs\DRUG-014-lincomycin.md` | drug_needs_review
- severity=3 | drug | Lincosamides / 林可酰胺类 | `wiki\drugs\DRUG-036-lincosamides.md` | drug_needs_review
- severity=3 | drug | Macrolides / 大环内酯类 | `wiki\drugs\DRUG-031-macrolides.md` | drug_needs_review
- severity=3 | drug | Meloxicam / 美洛昔康 | `wiki\drugs\DRUG-063-meloxicam.md` | drug_needs_review
- severity=3 | drug | Moxidectin / 莫昔克丁 | `wiki\drugs\DRUG-055-moxidectin.md` | drug_needs_review
- severity=3 | drug | NSAIDs / 非甾体抗炎药 | `wiki\drugs\DRUG-029-nsaids.md` | drug_needs_review

## Conclusions

- Disease pages are broadly present, but many still need China-context A0 regulatory or control anchors at the page level.
- Drug pages remain the largest weakness: most are NEEDS_REVIEW and need specific China compliance anchors for banned/stopped use, residues, withdrawal periods, quality standards, labels, and monitoring boundaries.
- Existing MOA raw/web batches already contain useful official pages; the highest-yield path during API blocking is to convert saved official pages into source pages and page-level boundaries.
- MOA search discovery is currently blocked by code=-101 on api.so-gov.cn; continue with known official URLs and candidate rescoring until the search endpoint is available again.
