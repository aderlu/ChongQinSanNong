# 2026-05-14 DIS-044 Runtime Anchor Admission And Native Graph Fix

## Background

- Target page: `DIS-044-gl-sser-s-disease`.
- Current `wiki-native` build report showed `evidence_units=0` and `page_gold_ready=false`.
- The page already had usable authority anchors in local source `SRC-0066` and in evidence expansion `001-Phase-2-Gold-Anchors-V8.md`, but the runtime page itself was still dominated by mojibake and non-admitted content.
- Result: the page looked populated to a human reader, but the current native graph pipeline could not reliably admit it as evidence-bearing runtime content.

## Problems Before This Change

- Runtime page content contained heavy mojibake, which reduced maintainability and created a high risk of future parsing mistakes.
- The key `fact_id/source_id/anchor` lines needed by the `wiki-native` graph were not present in a clean, compact, runtime-admissible form.
- Existing evidence lived mainly in expansion files, so the graph report continued to show `evidence_units=0`.
- The page structure mixed old compaction traces, damaged text, and incomplete runtime sections, which made governance review and downstream use harder.

## What Was Changed

- Rebuilt `wiki/diseases/DIS-044-gl-sser-s-disease.md` as a clean UTF-8 runtime page.
- Preserved the existing source set and kept the update additive with respect to already registered authority sources and expansions.
- Admitted the following source-anchored facts from `SRC-0066` directly into the runtime page:
  - `GLASS-003-maternal-immunity`
  - `GLASS-004-risk-2aee4f263dad2d98046bb67515e900c0`
  - `GLASS-005-coinfection`
  - `GLASS-006-clinical`
  - `GLASS-007-peracute`
  - `GLASS-008-lesions`
  - `GLASS-010-vaccine-maternal`
  - `GLASS-011-antibiotic-boundary`
- Added a guarded-update implementation:
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\wiki_ops\apply_dis044_glasser_runtime_anchor_admission.py`
  - `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\apply_dis044_glasser_runtime_anchor_admission.py`
- Added an execution report output file path under `issues/` for auditable run evidence.

## Why This Solves The Problem

- The runtime page is now compact, readable, and encoded in UTF-8 with normalized line endings.
- The admitted facts are written in the same `fact_id/source_id/anchor` style already used by pages that the `wiki-native` graph successfully counts.
- The update does not invent new authority sources or bypass governance; it promotes already existing local authority evidence into the correct runtime layer.
- This specifically targets the earlier mismatch of “expansion has evidence but runtime page still scores zero”.

## Governance Compliance

- `WIKI_MAINTENANCE_GUIDE.md` checked: yes
- `WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md` checked: yes
- Source/fact CRUD type: runtime page update using existing local authority source anchors
- Old data handling: replace mojibake runtime rendering; keep existing evidence expansions and source registry
- Coverage/overwrite/delete/downgrade/archive/migration decision: overwrite damaged runtime page only; no source deletion; no expansion deletion
- High-risk gate impact: none added; drug/regulatory high-risk boundaries remain blocked to rule cards and official sources
- Runtime manifest impact: same disease page path, higher expected native-graph admissibility
- Gold dataset impact: expected promotion from not-ready toward graph-admitted page, subject to rebuild checks

## UTF-8 And Anti-Mojibake Measures

- All newly added and rewritten files were written explicitly as UTF-8.
- New runtime structure uses mostly ASCII section names and stable inline anchors to reduce future encoding risk.
- No shell redirection overwrite was used for content editing; file edits were prepared as controlled patch changes.

## Expected Effect

- `DIS-044` should stop appearing as a false-empty page in the `wiki-native` build report.
- The native graph should be able to count admitted evidence units from the runtime page.
- Downstream sample planning, retrieval, evaluation, and governance audit should operate on a cleaner page with lower maintenance risk.

## Verification Plan

1. Create a bound CRUD decision for the `DIS-044` runtime-anchor admission update.
2. Execute the update through `run_guarded_wiki_update.py`.
3. Rebuild native graph outputs and inspect:
   - `issues/guarded_wiki_update_last_run.json`
   - `issues/wiki_native_graph_build_report.json`
   - `issues/wiki_native_graph_change_diff_last.json`
   - `wiki/wiki-native-graph.json`
   - `wiki/wiki-native-knowledge-graph.html`
4. Confirm `DIS-044` no longer shows `evidence_units=0`.
