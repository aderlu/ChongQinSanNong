# Gold Dataset Pilot Inspection / 2026-05-09

Generated: 2026-05-13T00:18:21+08:00

## Outputs

- `pilot_train`: `exports/pilot_gold_dataset/pilot_train_20260509.jsonl`
- `pilot_eval`: `exports/pilot_gold_dataset/pilot_eval_20260509.jsonl`
- `pilot_negative_trap`: `exports/pilot_gold_dataset/pilot_negative_trap_20260509.jsonl`
- `pilot_limited`: `exports/pilot_gold_dataset/pilot_limited_20260509.jsonl`

## Inspection

- Total samples: 24
- Group counts: {'pilot_train': 8, 'pilot_eval': 8, 'pilot_negative_trap': 8, 'pilot_limited': 0}
- Provenance complete rate: 1.0
- Missing provenance: []
- High-risk overreach: []
- Incomplete JSON: []
- Passed: True

## Manual Inspection Notes

- This pilot is a gate-validation dataset, not a final training release.
- Samples preserve source/rule provenance and avoid unsupported dose, withdrawal/MRL, food-safety, and regulatory positive claims.
- Batch production should continue only after a domain reviewer approves representative sample wording.
