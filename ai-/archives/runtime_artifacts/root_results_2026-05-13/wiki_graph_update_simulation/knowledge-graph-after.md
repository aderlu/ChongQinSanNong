# Chicken Disease LLM Wiki Graph (Mermaid)

> Derived from wiki/graph-data.json. Open wiki/knowledge-graph.html for the interactive full-coverage view.

```mermaid
graph LR
  DIS_026["口蹄疫"] -->|primary-source| SRC_0001["SRC-0001"]
  DIS_026["口蹄疫"] -->|diagnosis_standard_anchor| STANDARD_78c7b3214edf7a["baseline reviewed swine reference"]
  DIS_026["口蹄疫"] -->|evidence| SRC_0001["SRC-0001"]
  STANDARD_78c7b3214edf7a["baseline reviewed swine reference"] -->|described-by| SRC_0001["SRC-0001"]
  CANDIDATE_ff96a46f354a24["口蹄疫 WOAH disease page"] -->|candidate-fact| CANDIDATE_c183a023083ef0["pending_review"]
  CANDIDATE_ff96a46f354a24["口蹄疫 WOAH disease page"] -->|candidate-evidence| SRC_0002["口蹄疫 WOAH disease page"]
```
