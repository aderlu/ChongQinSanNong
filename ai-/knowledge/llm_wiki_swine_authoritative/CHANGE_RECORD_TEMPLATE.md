# Change Record Template

Copy this template into `knowledge_change_records/YYYY-MM-DD-HHMM-short-topic.md` for every future wiki maintenance change.

## 1. Landing Time

- Landing date:
- Landing time:
- Time zone:
- Change type:

## 1A. Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes/no
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes/no
- `WIKI_UPDATE_MANDATORY_SHORT_CARD.md` checked: yes/no
- `WIKI_UPDATE_SCENARIO_SHORT_CARD.md` checked: yes/no
- `SOURCE_BATCH_INTAKE_CHECKLIST.md` checked, if source/fact/batch data changed: yes/no/not applicable
- Fixed update entrypoint used: yes/no/not applicable
- CRUD decision file:
- CRUD decision audit passed: yes/no/not applicable
- Source/fact CRUD type: create/read/update/delete/migrate/archive/downgrade/exclude/rebuild
- Input source type: web/local Markdown/PDF/Word/Excel/raw/issue/model output/script output/human review/not applicable
- Old data handling: keep/update/supersede/downgrade/archive/migrate/exclude/delete/not applicable
- If old data changed, factual reason:
- High-risk gate impact:
- Runtime manifest impact:
- Gold dataset impact:

## 2. Problem Before The Change

Describe what was messy, redundant, incomplete, hallucination-prone, or difficult for production/evaluation retrieval.

Include:

- affected pages or directories,
- risk type,
- production-chain impact,
- evaluation-chain impact.

## 3. Code And Wiki State Before The Change

Describe:

- existing scripts or tools,
- existing wiki structure,
- missing automation,
- missing guardrails or source anchors,
- relevant prior audit metrics.

## 4. Code Added Or Updated

List files added or updated.

For each file, explain:

- purpose,
- input,
- output,
- whether it changes runtime pages,
- whether it only audits or reports.

## 5. Wiki Organization Work

List pages or directories changed.

Describe:

- evidence moved,
- sections compacted,
- guardrails added,
- partial pages annotated,
- reports generated.

## 6. What The Change Solved

Explain how the change reduces:

- hallucination risk,
- retrieval noise,
- fact density,
- unsupported drug or regulatory claims,
- partial-page misuse,
- evaluation ambiguity.

## 7. Verification Results

Include command outputs or summarized JSON:

```json
{
  "manifest_entries": null,
  "missing_paths": null,
  "high": null,
  "medium": null,
  "low": null,
  "none": null,
  "readiness_score": null
}
```

Also include any phase-specific report paths.

## 8. Expected Effects

Describe expected effects for:

- production retrieval,
- answer generation,
- evaluation and scoring,
- audit, source expansion, and validity checks,
- future maintenance.

## 9. Remaining Issues

List:

- unresolved low-risk items,
- pages or facts needing source expansion, conflict resolution, or authority-level clarification,
- external authority sources needed,
- future phase or maintenance recommendations.

## 10. Conclusion

Summarize the outcome in 2 to 5 sentences.
