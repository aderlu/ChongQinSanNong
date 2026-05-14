# Runtime Hallucination Risk Audit / 2026-05-09

Generated: 2026-05-14T00:21:26+08:00
Manifest: `exports\runtime_core_manifest.json`
Entries checked: 204

## Severity Counts

- high: 0
- medium: 0
- low: 16
- none: 188

## Top Risk Pages

- score=9 severity=low `RC-TCM-COMPATIBILITY-RAU-003` `wiki/rule_cards/RC-TCM-COMPATIBILITY-RAU-003.md` findings=dose_or_course_terms_without_expected_guardrail:2; withdrawal_or_mrl_terms_without_expected_guardrail:2; regulatory_or_emergency_terms_without_expected_guardrail:1
- score=9 severity=low `SYN-012-feed-toxin-gas` `wiki/syndromes/SYN-012-feed-toxin-gas.md` findings=dose_or_course_terms_without_expected_guardrail:3; withdrawal_or_mrl_terms_without_expected_guardrail:5; regulatory_or_emergency_terms_without_expected_guardrail:1
- score=6 severity=low `RC-SYNTHESIS-SCOPE-001` `wiki/rule_cards/RC-SYNTHESIS-SCOPE-001.md` findings=dose_or_course_terms_without_expected_guardrail:2; withdrawal_or_mrl_terms_without_expected_guardrail:5
- score=6 severity=low `CMP-014` `wiki/comparisons/CMP-014-handbook-disease-coverage-map.md` findings=dose_or_course_terms_without_expected_guardrail:2; withdrawal_or_mrl_terms_without_expected_guardrail:4
- score=3 severity=low `RC-ALIAS-001` `wiki/rule_cards/RC-ALIAS-001.md` findings=withdrawal_or_mrl_terms_without_expected_guardrail:1
- score=3 severity=low `RC-CITATION-001` `wiki/rule_cards/RC-CITATION-001.md` findings=withdrawal_or_mrl_terms_without_expected_guardrail:2
- score=3 severity=low `CMP-004` `wiki/comparisons/CMP-004-reproductive-failure.md` findings=withdrawal_or_mrl_terms_without_expected_guardrail:2
- score=3 severity=low `CMP-005` `wiki/comparisons/CMP-005-vesicular-disease.md` findings=withdrawal_or_mrl_terms_without_expected_guardrail:2
- score=3 severity=low `SYN-001-piglet-diarrhea` `wiki/syndromes/SYN-001-piglet-diarrhea.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=3 severity=low `SYN-002-post-weaning-diarrhea` `wiki/syndromes/SYN-002-post-weaning-diarrhea.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=3 severity=low `SYN-003-reproductive-failure` `wiki/syndromes/SYN-003-reproductive-failure.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=3 severity=low `SYN-004-respiratory-syndrome` `wiki/syndromes/SYN-004-respiratory-syndrome.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=3 severity=low `SYN-005-neurologic-signs` `wiki/syndromes/SYN-005-neurologic-signs.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=3 severity=low `SYN-008-skin-pruritus-crusts` `wiki/syndromes/SYN-008-skin-pruritus-crusts.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=3 severity=low `SYN-010-anemia-jaundice` `wiki/syndromes/SYN-010-anemia-jaundice.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=3 severity=low `SYN-011-poor-growth-wasting` `wiki/syndromes/SYN-011-poor-growth-wasting.md` findings=regulatory_or_emergency_terms_without_expected_guardrail:1
- score=0 severity=none `DIS-001` `wiki/diseases/DIS-001-adenoviruses.md` findings=none
- score=0 severity=none `DIS-002` `wiki/diseases/DIS-002-african-swine-fever-virus.md` findings=none
- score=0 severity=none `DIS-003` `wiki/diseases/DIS-003-anelloviruses-torque-teno-sus-viruses.md` findings=none
- score=0 severity=none `DIS-004` `wiki/diseases/DIS-004-astroviruses.md` findings=none
- score=0 severity=none `DIS-005` `wiki/diseases/DIS-005-bunyaviruses-akabane-lumbo-oya-tahyna.md` findings=none
- score=0 severity=none `DIS-006` `wiki/diseases/DIS-006-caliciviruses-norovirus-sapovirus-vesicular-exanthema-virus.md` findings=none
- score=0 severity=none `DIS-007` `wiki/diseases/DIS-007-circoviruses-pcvad.md` findings=none
- score=0 severity=none `DIS-008` `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md` findings=none
- score=0 severity=none `DIS-009` `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md` findings=none

## Interpretation

- This audit is a risk triage, not a truth-quality judgment.
- High or medium pages should be reviewed before they are used for unrestricted production retrieval.
- Drug, withdrawal/MRL, and regulatory findings should be handled with rule-card gating and source expansion.
