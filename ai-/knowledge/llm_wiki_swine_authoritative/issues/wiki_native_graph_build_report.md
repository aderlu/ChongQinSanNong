# Wiki Native Graph Build Report

- Build ID: `wiki-native-graph:2026-05-14T00:21:24+08:00`
- Build status: `pass`
- Graph path: `wiki/wiki-native-graph.json`
- Report JSON: `issues/wiki_native_graph_build_report.json`
- Encoding: UTF-8 read/write enforced by script

## Coverage

- Evidence units: 2405
- Frontmatter missing: 0
- Uncovered content summary items: 1711
- Node counts: `{"comparison": 17, "disease": 73, "drug": 81, "rule": 450, "rule_card": 21, "section": 4819, "literal_span": 243, "source": 239, "syndrome": 22, "synthesis": 35, "topic": 99}`
- Edge status counts: `{"verified": 6347, "candidate": 95}`

## Semantic Edges

- By predicate: `{"HAS_CONTROL_MEASURE": 27, "HAS_TRANSMISSION_ROUTE": 64, "HAS_CLINICAL_SIGN": 73, "HAS_DIAGNOSTIC_METHOD": 35, "DIFFERENTIAL_DIAGNOSIS": 28, "HAS_DRUG_BOUNDARY": 2, "HAS_PATHOGEN": 18}`
- Candidate reasons: `{"missing_fact_id": 63, "missing_required_rule_card": 32}`
- Rejected reasons: `{}`

## Audit

- Blockers: 0
- Warnings: 0

## Runtime Admission

Only semantic edges with `status=verified`, `validation_status=accepted`, and `evidence_support_check=pass` are eligible for golden dataset positive examples.
Candidate and rejected edges remain in the unified graph for review, gap discovery, and anti-hallucination training.
