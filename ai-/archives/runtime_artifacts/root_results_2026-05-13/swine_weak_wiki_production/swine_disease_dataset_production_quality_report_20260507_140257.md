# Swine Weak-Wiki 100 Dataset Quality Report

Generated at: 2026-05-07 14:02:57

## Artifacts

- Full CSV: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260507_140257.csv`
- Valid CSV: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260507_140257_valid.csv`
- Reject/review CSV: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_20260507_140257_rejects.csv`
- Raw JSON: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_weak_wiki_production_raw_20260507_140257.json`
- Summary JSON: `D:\XF-ChongQin\ai-\results\swine_weak_wiki_production\swine_disease_dataset_production_summary_20260507_140257.json`

## Summary

- Requested/generated: 100 / 100
- Valid pass rows: 71
- Review rows: 11
- Reject rows: 18
- Valid rate: 71.0%
- Average score: 85.0
- Valid subset average score: 87.08
- Valid subset score range: 82-95
- Fatal risk rows: 18
- Specific dose hits: 0
- Specific withdrawal-period numeric hits: 0
- Duplicate user queries: 0
- Duplicate diagnoses: 0
- Duplicate prescriptions: 0
- Valid disease coverage: 54 distinct disease names
- Full disease coverage: 73 distinct disease names

## Quality Judgment

The full 100-row file should not be used directly for fine-tuning because it contains 29 non-pass rows, including 18 hard rejects. Most hard rejects were triggered by conservative target-disease alias matching, but the correct operational choice is still to keep them out of train-ready data.

The 71-row valid subset is suitable as preliminary model-testing data and can be used as a weakly supervised fine-tuning pilot only if it is clearly labeled as synthetic, weak-wiki, non-authoritative data.

It is not yet suitable as a high-confidence production medical fine-tuning corpus because:

- Wiki evidence is intentionally weak, not authoritative per answer.
- There is only one LLM judge and no arbiter.
- No human clinical review has been performed.
- Drug directions avoid dose and exact withdrawal periods, so the corpus trains safe treatment direction rather than executable prescriptions.

## Recommendation

Use the 71 valid rows for:

- Model smoke tests.
- Prompt regression tests.
- Preliminary SFT pipeline validation.
- Diagnosis-treatment consistency checks.

Do not use the full 100 rows directly. For a 300-row pilot training set, generate 450-500 candidates and use only the generated `*_valid.csv` rows.

Recommended production command:

```powershell
python scripts\run_swine_weak_wiki_production_2026_05_07.py --limit 500 --parallel 8 --answer-max-tokens 1500 --judge-max-tokens 950
```

Expected valid rows at the observed 71% pass rate:

```text
500 * 0.71 = 355 valid rows
```

Then take 300 valid rows for the preliminary SFT/test set.
