from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any, Mapping

from chicken_data_synthesis.infrastructure.knowledge.authority import discover_authority_sources
from chicken_data_synthesis.infrastructure.knowledge.graph import rebuild_graph
from chicken_data_synthesis.infrastructure.knowledge.governance import append_governance_event, validate_change_request


DEFAULT_OUTPUT = Path("results/wiki_graph_update_simulation")


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate a governed swine LLM Wiki graph update.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--clean", action="store_true", help="Remove previous simulation output first.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    demo_wiki = output_dir / "demo_swine_wiki"
    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    build_demo_wiki(demo_wiki)
    before = rebuild_graph(demo_wiki)
    before_graph = json.loads(Path(before.graph_data_path).read_text(encoding="utf-8"))
    before_copy = output_dir / "graph-before.json"
    before_html = output_dir / "knowledge-graph-before.html"
    before_md = output_dir / "knowledge-graph-before.md"
    shutil.copy2(before.graph_data_path, before_copy)
    shutil.copy2(before.html_path, before_html)
    shutil.copy2(before.mermaid_path, before_md)

    request = validate_change_request(
        operation="create",
        target="authority-source:WOAH foot-and-mouth-disease",
        reason="simulate gap-first swine wiki authority source update for graph diff validation",
        evidence="issues/swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md; WOAH disease page URL",
        actor="simulation",
    )
    append_governance_event(demo_wiki, request, phase="simulation_trigger", status="accepted")

    suggestions = {
        "sources": [
            {
                "url": "https://www.woah.org/en/disease/foot-and-mouth-disease/",
                "title": "口蹄疫 WOAH disease page",
                "reason": "WOAH disease page can support a candidate source for swine foot-and-mouth disease diagnosis and control context.",
                "evidence_role": "clinical_reference",
            }
        ]
    }
    authority_report = discover_authority_sources(
        demo_wiki,
        "GAP-FIRST | 猪病 LLM wiki | DIS-026 口蹄疫 | 补齐国际权威来源候选，候选事实进入 NEEDS_REVIEW，不直接进入正式事实库。",
        llm_suggestions_json=json.dumps(suggestions, ensure_ascii=False),
        fetch=False,
    )

    after = rebuild_graph(demo_wiki)
    after_graph = json.loads(Path(after.graph_data_path).read_text(encoding="utf-8"))
    after_copy = output_dir / "graph-after.json"
    after_html = output_dir / "knowledge-graph-after.html"
    after_md = output_dir / "knowledge-graph-after.md"
    shutil.copy2(after.graph_data_path, after_copy)
    shutil.copy2(after.html_path, after_html)
    shutil.copy2(after.mermaid_path, after_md)

    diff = diff_graphs(before_graph, after_graph)
    diff["authority_report"] = {
        "accepted_count": authority_report.accepted_count,
        "rejected_count": authority_report.rejected_count,
        "created_sources": authority_report.created_sources,
        "candidates_path": authority_report.candidates_path,
    }
    diff_path = output_dir / "graph-update-diff.json"
    diff_path.write_text(json.dumps(diff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = output_dir / "graph-update-report.md"
    report_path.write_text(render_report(output_dir, diff), encoding="utf-8")

    steps_path = output_dir / "reproduce-steps.ps1"
    steps_path.write_text(render_steps(output_dir), encoding="utf-8")

    print(json.dumps(
        {
            "demo_wiki": str(demo_wiki),
            "before_html": str(before_html),
            "after_html": str(after_html),
            "diff_json": str(diff_path),
            "report": str(report_path),
            "reproduce_steps": str(steps_path),
            "added_nodes": diff["added_node_count"],
            "added_links": diff["added_link_count"],
            "added_candidate_facts": diff["candidate_fact_delta"],
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


def build_demo_wiki(root: Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    for rel in (
        "wiki/diseases",
        "wiki/sources",
        "wiki/drugs",
        "wiki/rules",
        "wiki/rule_cards",
        "wiki/topics",
        "wiki/syndromes",
        "wiki/synthesis",
        "wiki/synthesis/sessions",
        "wiki/comparisons",
        "wiki/sessions",
        "wiki/queries",
        "exports",
        "issues",
        "raw/html",
        "raw/urls",
        "raw/notes",
        "raw/pdfs",
    ):
        (root / rel).mkdir(parents=True, exist_ok=True)
    (root / "index.md").write_text("# Swine LLM Wiki Graph Update Demo\n", encoding="utf-8")
    (root / "purpose.md").write_text("# Purpose\n\nGoverned swine graph update simulation.\n", encoding="utf-8")
    (root / ".wiki-schema.md").write_text("# Schema\n\nDemo schema marker.\n", encoding="utf-8")
    (root / "log.md").write_text("# Log\n", encoding="utf-8")
    (root / ".wiki-cache.json").write_text('{"version":1,"entries":{}}\n', encoding="utf-8")

    (root / "wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md").write_text(
        "# 口蹄疫 / Foot-and-mouth disease\n\n"
        "猪可作为口蹄疫易感动物。本演示只保留一个已复核基础事实，后续自动更新仅新增候选来源与候选事实。\n",
        encoding="utf-8",
    )
    (root / "wiki/sources/SRC-0001-baseline-swine-reference.md").write_text(
        "---\n"
        "type: source\n"
        "source_id: SRC-0001\n"
        "source_path: raw/notes/baseline-swine-reference.txt\n"
        "source_type: plain_text\n"
        "authority_level: textbook\n"
        "evidence_status: HUMAN_REVIEWED\n"
        "---\n\n"
        "# Baseline swine reference\n\nDemo baseline source.\n",
        encoding="utf-8",
    )
    (root / "raw/notes/baseline-swine-reference.txt").write_text("Baseline reviewed swine reference.\n", encoding="utf-8")

    write_csv(
        root / "exports/disease_index.csv",
        ["disease_id", "disease_name", "category", "primary_source_id", "page_relpath"],
        [
            {
                "disease_id": "DIS-026",
                "disease_name": "口蹄疫",
                "category": "病毒病",
                "primary_source_id": "SRC-0001",
                "page_relpath": "wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md",
            }
        ],
    )
    write_csv(root / "exports/drug_page_index.csv", ["drug_id", "drug_name", "page_relpath"], [])
    write_csv(root / "exports/rule_index.csv", ["rule_id", "title", "page_relpath"], [])
    facts = [
        {
            "fact_id": "DIS-026-DEMO-001",
            "fact_type": "disease",
            "subject": "口蹄疫",
            "predicate": "diagnosis_standard_anchor",
            "object": "baseline reviewed swine reference",
            "evidence_source_id": "SRC-0001",
            "evidence_status": "HUMAN_REVIEWED",
        }
    ]
    (root / "exports/knowledge_facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "exports/knowledge_facts.candidates.json").write_text("[]\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def diff_graphs(before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]:
    before_nodes = {str(node["id"]): node for node in before.get("nodes", [])}
    after_nodes = {str(node["id"]): node for node in after.get("nodes", [])}
    before_links = {_link_key(link): link for link in before.get("links", [])}
    after_links = {_link_key(link): link for link in after.get("links", [])}
    added_nodes = [after_nodes[key] for key in sorted(set(after_nodes) - set(before_nodes))]
    removed_nodes = [before_nodes[key] for key in sorted(set(before_nodes) - set(after_nodes))]
    added_links = [after_links[key] for key in sorted(set(after_links) - set(before_links))]
    removed_links = [before_links[key] for key in sorted(set(before_links) - set(after_links))]
    return {
        "before_metadata": before.get("metadata", {}),
        "after_metadata": after.get("metadata", {}),
        "added_node_count": len(added_nodes),
        "removed_node_count": len(removed_nodes),
        "added_link_count": len(added_links),
        "removed_link_count": len(removed_links),
        "candidate_fact_delta": int(after.get("metadata", {}).get("candidate_facts", 0)) - int(before.get("metadata", {}).get("candidate_facts", 0)),
        "added_nodes": added_nodes,
        "removed_nodes": removed_nodes,
        "added_links": added_links,
        "removed_links": removed_links,
        "reasonableness": [
            "新增 source 节点来自 WOAH allowlisted domain，属于权威来源候选。",
            "新增 candidate 节点/边来自 knowledge_facts.candidates.json，evidence_status=NEEDS_REVIEW，不会冒充正式事实。",
            "既有 DIS-026 与 HUMAN_REVIEWED 基础事实未被覆盖或删除，说明更新为增量补证据。",
            "图谱更新后 candidate_facts 增加，符合 gap-first 自动维护先补缺失来源再复核的流程。",
        ],
    }


def _link_key(link: Mapping[str, Any]) -> str:
    return "|".join(str(link.get(key, "")) for key in ("source", "target", "type", "predicate", "fact_id"))


def render_report(output_dir: Path, diff: Mapping[str, Any]) -> str:
    added_nodes = "\n".join(f"- `{n.get('id')}` ({n.get('group')}): {n.get('label')}" for n in diff["added_nodes"]) or "- none"
    added_links = "\n".join(
        f"- `{l.get('source')}` -> `{l.get('target')}` type=`{l.get('type')}` fact_id=`{l.get('fact_id', '')}`"
        for l in diff["added_links"]
    ) or "- none"
    reasonableness = "\n".join(f"- {item}" for item in diff["reasonableness"])
    return f"""# Governed Swine Graph Update Simulation

## Visualization Files

- Before: `{output_dir / 'knowledge-graph-before.html'}`
- After: `{output_dir / 'knowledge-graph-after.html'}`
- Diff JSON: `{output_dir / 'graph-update-diff.json'}`

## Summary

- Added nodes: {diff['added_node_count']}
- Removed nodes: {diff['removed_node_count']}
- Added links: {diff['added_link_count']}
- Removed links: {diff['removed_link_count']}
- Candidate fact delta: {diff['candidate_fact_delta']}

## Added Nodes

{added_nodes}

## Added Links

{added_links}

## Reasonableness

{reasonableness}
"""


def render_steps(output_dir: Path) -> str:
    script = Path("scripts/simulate_governed_swine_graph_update_2026_05_08.py")
    return f"""$ErrorActionPreference = "Stop"
Set-Location "D:\\XF-ChongQin\\ai-"
$env:PYTHONPATH = "src;."

# 1. 运行受治理的猪病图谱更新模拟。
python "{script}" --clean --output-dir "{output_dir}"

# 2. 查看更新前/后图谱文件路径。
Get-ChildItem "{output_dir}" -Filter "knowledge-graph-*.html" | Select-Object FullName,Length,LastWriteTime

# 3. 查看节点、边、候选事实变化摘要。
Get-Content "{output_dir / 'graph-update-diff.json'}" | Select-String -Pattern "added_node_count|added_link_count|candidate_fact_delta"

# 4. 查看审计闭环事件。
Get-ChildItem "{output_dir / 'demo_swine_wiki' / 'issues'}" -Filter "wiki_governance_audit_*.jsonl" | ForEach-Object {{ Get-Content $_.FullName }}

# 5. 打开说明报告。
Get-Content "{output_dir / 'graph-update-report.md'}"
"""


if __name__ == "__main__":
    raise SystemExit(main())
