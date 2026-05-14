# Swine P0 runtime validation

- ok: True
- errors: none
- rule_base_ok: True
- result_csv: `results/swine_disease_dataset_{timestamp}.csv`
- knowledge_facts_json_ok: True
- fact_count: 2193
- bad_questionmark_count: 0
- template_required_tokens_ok: True
- prompt_chicken_mentions: 0
- final_fields_ok: True
- generation_preserves_answer_json: True
- generation_preserves_evidence_anchors: True

This report verifies the P0 runtime contract for swine dataset generation: swine wiki routing, loadable facts, source-first schema tokens, and CSV preservation of structured answer/evidence fields.
