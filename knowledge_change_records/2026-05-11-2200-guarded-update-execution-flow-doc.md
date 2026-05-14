# Guarded Wiki Update Execution Flow Documentation

## 1. Change Summary

This change adds a report-ready execution guide for the guarded swine LLM Wiki update process.

New document:

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_GUARDED_UPDATE_EXECUTION_FLOW.md`

The document explains the complete process from update preparation to final data landing, graph rebuild, validation, and evidence output.

## 2. Previous Problem

Before this change, the repository already had governance rules, CRUD decision templates, guarded update code, maintenance checks, and update examples. However, the full execution chain was distributed across several documents and scripts.

This made it difficult to answer the following reporting questions in one place:

- How does a wiki update start?
- Where is the CRUD decision prepared?
- Which code checks the CRUD decision before execution?
- Which code executes the fixed guarded entrypoint?
- Which code runs post-update validation?
- How can we prove that data has fully landed?
- Which evidence files should be used in a work report?

## 3. Related Existing Code Before The Change

The documentation was written by reading and organizing the behavior of the existing implementation:

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_crud_decision.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/run_swine_wiki_maintenance_checks.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/tools/apply_dis026_fmd_authority_web_refresh.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/CRUD_DECISION_TEMPLATE.md`

No runtime data, disease page, source page, fact page, graph export, or gold dataset file was changed by this documentation-only update.

## 4. What Was Added

The new execution guide adds the following content:

- High-level guarded update flow.
- Responsibility split between maintainer or LLM agent, guarded entrypoint, CRUD audit, update script, postcheck runner, and work record.
- Preparation stage and governance basis.
- CRUD decision file creation and required fields.
- Actual `run_guarded_wiki_update.py` call chain.
- Preflight governance and CRUD decision checks.
- Update script responsibilities for source, fact, runtime, export, and graph-affecting files.
- Full post-update validation chain.
- Graph rebuild and graph diff evidence.
- Data fully landed criteria.
- DIS-026 foot-and-mouth disease authority refresh example.
- Common failure points.
- Report-ready wording for explaining the mechanism.

## 5. Problem Solved After The Change

After this change, the guarded update process can be explained as a complete auditable chain:

1. Governance rules provide the operation basis.
2. CRUD decision file records why an operation should happen.
3. `audit_crud_decision.py` checks the decision before data update.
4. `run_guarded_wiki_update.py` fixes the execution order.
5. The update script performs actual data landing.
6. `run_swine_wiki_maintenance_checks.py` runs post-update validation and rebuild tasks.
7. Evidence files prove whether the update completed successfully.
8. The work record preserves human-readable reporting evidence.

This directly supports work reporting around "how the update is judged, executed, validated, and evidenced."

## 6. Expected Effect

The new document should help maintainers:

- Understand the complete update execution and call flow.
- Explain which steps are enforced by code and which steps require maintainer or LLM-agent preparation.
- Use a fixed command pattern for guarded updates.
- Locate the evidence files proving that the update completed.
- Present the CRUD governance mechanism in a concise report format.

## 7. Verification

Verification performed:

- Confirmed the new document exists.
- Confirmed the document contains references to `run_guarded_wiki_update.py`.
- Confirmed the document contains `preflight_crud_decision`.
- Confirmed the document contains `audit_crud_decision.py`.
- Confirmed the document contains the data fully landed criteria section.

## 8. Encoding Precautions

This change was created as a new UTF-8 Markdown file and did not rewrite existing Chinese governance documents. This reduces the risk of introducing encoding damage or mojibake into existing files.
