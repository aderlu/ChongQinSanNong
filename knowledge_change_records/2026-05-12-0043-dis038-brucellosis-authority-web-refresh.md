# DIS-038 Brucellosis Authority Web Refresh

## 1. Landing Time

- Landing date: 2026-05-12
- Landing time: 00:43
- Time zone: Asia/Shanghai
- Change type: guarded source/fact/runtime/evidence refresh

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: yes
- Fixed update entrypoint used: yes
- CRUD decision file: `ai-/knowledge/llm_wiki_swine_authoritative/issues/crud_decisions/2026-05-12-0042-dis038-brucellosis-authority-web-refresh-a1-gated-cwd.md`
- CRUD decision audit passed: yes
- Source/fact CRUD type: update source metadata; create fact anchors; update runtime page; create evidence expansion; rebuild exports/graph/readiness
- Input source type: web
- Old data handling: keep
- If old data changed, factual reason: existing source/fact/runtime/evidence records were retained; no referenced object was deleted, replaced, downgraded, archived, migrated, or excluded.
- High-risk gate impact: high_regulatory decision was allowed only after A1 was stated as the controlling authority level; CDC A2 was limited to public-health exposure boundary and cannot authorize animal-control execution.
- Runtime manifest impact: rebuilt through guarded post-update checks; missing paths remained 0.
- Gold dataset impact: rebuilt fact status/readiness indexes; readiness score remained 99.

## 2. Problem Before The Change

`wiki/diseases/DIS-038-brucella-suis-brucellosis.md` was still a partial source-anchored page. It had older anchors and local textbook-derived facts, but the runtime page did not compactly expose current authority web evidence for B. suis causation, reproductive-loss signs, wild-swine exposure, WOAH listed-disease framing, diagnostic confirmation boundary, and human-exposure risk.

The risk was high_regulatory/public_health: model answers could overuse partial content or under-route execution questions to current official/regulatory sources.

## 3. Code And Wiki State Before The Change

The guarded CRUD flow already existed: `create_crud_decision.py`, `audit_crud_decision.py`, `run_guarded_wiki_update.py`, and `guarded_update_context.py`.

DIS-038 had existing source anchors including MOA, USDA APHIS, WOAH, CDC, and Diseases of Swine sources. It remained `partial_source_anchored_page` and `generation_ready_limited`, which is appropriate for bounded generation but needs clear source/fact anchors.

## 4. Code Added Or Updated

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/apply_dis038_brucellosis_authority_web_refresh.py`
  - Purpose: guarded DIS-038 authority web refresh.
  - Input: rendered authoritative web text acquired with web-access/CDP from USDA APHIS, WOAH, and CDC.
  - Output: updated source pages, four fact anchors, runtime authority refresh block, evidence expansion, execution report, and refreshed fact status.
  - Runtime impact: updates DIS-038 with a short source/fact-routed block.
  - Guardrail: calls `require_guarded_update()` and fails when run outside `run_guarded_wiki_update.py`.

## 5. Wiki Organization Work

- Updated source metadata:
  - `wiki/sources/A1-USDA-APHIS-SWINE-BRUCELLOSIS.md`
  - `wiki/sources/A1-WOAH-BRUCELLOSIS.md`
  - `wiki/sources/A2-CDC-BRUCELLOSIS.md`
- Added fact anchors:
  - `DIS038-WEB-001-aphis-causation-reproductive-zoonotic`
  - `DIS038-WEB-002-aphis-wild-swine-and-report-routing`
  - `DIS038-WEB-003-woah-listed-transmission-diagnostic`
  - `DIS038-WEB-004-cdc-occupational-public-health-boundary`
- Updated runtime page:
  - `wiki/diseases/DIS-038-brucella-suis-brucellosis.md`
- Added evidence expansion:
  - `wiki/evidence_expansions/diseases/phase4_runtime_compaction/DIS-038-brucella-suis-brucellosis/003-Authority-Web-Refresh-2026-05-12.md`
- Added execution report:
  - `issues/dis038_brucellosis_authority_web_refresh_2026-05-12.json`

## 6. What The Change Solved

The page now has compact, source-routed authority anchors for the specific missing boundaries most likely to affect retrieval and generation. The update reduces partial-page misuse by explicitly saying that A1/A2 sources do not authorize China-specific culling, movement, vaccination, slaughter, compensation, food-chain, drug, withdrawal-period, or MRL claims.

The graph changed in the intended direction: DIS-038 now links to four new fact nodes, and those facts link back to the refreshed authority source nodes.

## 7. Verification Results

```json
{
  "guarded_update_passed": true,
  "preflight_governance_compliance": true,
  "preflight_crud_decision": true,
  "update_command": true,
  "post_update_full_checks": true,
  "manifest_missing_paths": 0,
  "graph_nodes_before": 2597,
  "graph_nodes_after": 2604,
  "graph_links_before": 3193,
  "graph_links_after": 3201,
  "graph_added_nodes": 7,
  "graph_added_links": 8,
  "hallucination_high": 0,
  "hallucination_medium": 0,
  "readiness_score": 99,
  "runtime_damaged_count": 0,
  "pytest": "12 passed"
}
```

Important report paths:

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/guarded_wiki_update_last_run.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/graph_change_diff_last.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph.html`
- `ai-/knowledge/llm_wiki_swine_authoritative/wiki/knowledge-graph-changes.html`

Negative/guard evidence:

- Direct execution of `apply_dis038_brucellosis_authority_web_refresh.py` failed with the guarded-entrypoint error.
- An initial CRUD decision using `authority_level=A1/A2` with `risk_class=high_regulatory` failed preflight.
- A second attempt with the wrong command path passed preflight but failed before content changes due to command path mismatch.
- The final decision used `authority_level=A1`, a cwd-correct planned command, and passed the full guarded flow.

## 8. Expected Effects

Production retrieval should now find DIS-038 authority anchors more directly for swine brucellosis identity, reproductive signs, wild-swine exposure, WOAH listed-disease framing, diagnostic confirmation boundaries, and public-health exposure boundaries.

Answer generation should remain bounded: local execution questions still route to current China A0/A1 official sources and rule cards. Evaluation and scoring can use the new fact IDs as explicit provenance anchors.

## 9. Remaining Issues

DIS-038 should remain a partial/gap-routing page until additional jurisdiction-specific and source-complete facets are reviewed. CDC material must remain public-health exposure support only. China-specific execution claims still require current China A0/A1 sources.

## 10. Conclusion

This change completed one full guarded web-source update cycle for DIS-038. It updated authority source metadata, added four source-anchored facts, changed the runtime page, rebuilt graph/readiness artifacts, and preserved high-risk regulatory boundaries. The flow proved effective because invalid decisions and direct execution were blocked before the final valid guarded run succeeded.
