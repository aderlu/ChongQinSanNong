# Governed Swine Graph Update Simulation

## Visualization Files

- Before: `D:\XF-ChongQin\ai-\results\wiki_graph_update_simulation\knowledge-graph-before.html`
- After: `D:\XF-ChongQin\ai-\results\wiki_graph_update_simulation\knowledge-graph-after.html`
- Diff JSON: `D:\XF-ChongQin\ai-\results\wiki_graph_update_simulation\graph-update-diff.json`

## Summary

- Added nodes: 3
- Removed nodes: 0
- Added links: 2
- Removed links: 0
- Candidate fact delta: 1

## Added Nodes

- `CANDIDATE:c183a023083ef0` (candidate): pending_review
- `CANDIDATE:ff96a46f354a24` (candidate): 口蹄疫 WOAH disease page
- `SRC-0002` (source): 口蹄疫 WOAH disease page

## Added Links

- `CANDIDATE:ff96a46f354a24` -> `CANDIDATE:c183a023083ef0` type=`candidate-fact` fact_id=`CAND-0001`
- `CANDIDATE:ff96a46f354a24` -> `SRC-0002` type=`candidate-evidence` fact_id=`CAND-0001`

## Reasonableness

- 新增 source 节点来自 WOAH allowlisted domain，属于权威来源候选。
- 新增 candidate 节点/边来自 knowledge_facts.candidates.json，evidence_status=NEEDS_REVIEW，不会冒充正式事实。
- 既有 DIS-026 与 HUMAN_REVIEWED 基础事实未被覆盖或删除，说明更新为增量补证据。
- 图谱更新后 candidate_facts 增加，符合 gap-first 自动维护先补缺失来源再复核的流程。
