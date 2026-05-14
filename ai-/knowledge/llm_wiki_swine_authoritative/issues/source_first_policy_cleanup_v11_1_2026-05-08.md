# Source-first policy cleanup V11.1 execution log

- Date: 2026-05-08
- Core policy added: `wiki/synthesis/swine_source_first_generation_policy_v11_1.md`
- Synthesis pages rewritten/normalized: 7
- Rule cards rewritten: 5
- Rules covered by source-first adjustment: 448
- Drug pages covered by source-first label boundary: 76
- Disease pages covered by source-first regulatory boundary cleanup: 73
- Latest idempotent run changed rules/drugs/diseases: 0/0/0

## Policy outcome

- `A0/A1/A2/SRC/RC/RULE` are all accepted as evidence families for swine disease generation and evaluation when source anchors are clear and the evidence is not `NEEDS_REVIEW`.
- China-specific regulatory language is no longer the default global gate; it is retained only when the answer claims China/local compliance or execution.
- Drug pages now distinguish positive label candidates from boundary-only pages using source-first label evidence rather than a China-only A0/A1 gate.
- Disease pages had empty V5 placeholder subsections removed while populated V5/V8/V11 evidence blocks were preserved.
