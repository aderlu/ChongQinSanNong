# Encoding Integrity Audit

Generated: 2026-05-14T00:21:28+08:00

## Summary

- Text files scanned: 2532
- Runtime manifest paths loaded: 204
- Encoding OK: 2518
- Decode or replacement damage: 3
- Mojibake-like content: 0
- Minor mojibake signal: 11
- Runtime damaged count: 0

## Damaged Or High-Signal Files

- `issues/phase2_encoding_quarantine_2026-05-09.json`: decode_or_replacement_damage, replacement=1438, mojibake_score=0, runtime=False
- `issues/wiki_diseases_comparisons_drugs_mojibake_audit_2026-05-08.md`: decode_or_replacement_damage, replacement=1, mojibake_score=0, runtime=False
- `raw/md/猪场兽药使用与猪病防治技术200-363页.md`: decode_or_replacement_damage, replacement=1, mojibake_score=0, runtime=False

## Interpretation

- `decode_or_replacement_damage` means UTF-8 decoding failed or replacement characters were found.
- `mojibake_like_content` means text decoded as UTF-8 but contains a high count of common mojibake patterns.
- Runtime manifest paths with damage should be fixed before production retrieval.
- Raw archive damage should be isolated or reprocessed before it is used for new facts.
