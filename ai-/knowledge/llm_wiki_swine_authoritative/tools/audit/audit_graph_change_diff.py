from __future__ import annotations

import argparse
import hashlib
import html
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

"""知识图谱变化审计脚本。

由 run_swine_wiki_maintenance_checks.py 在图谱重建后调用。
它读取最新 graph-data.json，与上一份图谱快照对比，输出 graph_change_diff_last.json/md。
"""

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
ISSUES = ROOT / "issues"
GRAPH_JSON = WIKI / "graph-data.json"
CHANGE_HTML = WIKI / "knowledge-graph-changes.html"
SNAPSHOT_DIR = ISSUES / "graph_snapshots"
LATEST_SNAPSHOT = SNAPSHOT_DIR / "latest_graph_snapshot.json"
DIFF_JSON = ISSUES / "graph_change_diff_last.json"
DIFF_MD = ISSUES / "graph_change_diff_last.md"
CRUD_LOG = ISSUES / "wiki_crud_change_log.jsonl"
TZ = timezone(timedelta(hours=8))


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def link_key(link: dict[str, Any]) -> str:
    source = str(link.get("source", ""))
    target = str(link.get("target", ""))
    link_type = str(link.get("type", ""))
    fact_id = str(link.get("fact_id", ""))
    return f"{source}|{target}|{link_type}|{fact_id}"


def graph_maps(graph: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    nodes = {
        str(node.get("id", "")): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    }
    links = {
        link_key(link): link
        for link in graph.get("links", [])
        if isinstance(link, dict) and link.get("source") and link.get("target")
    }
    return nodes, links


def classify_node_change(node_id: str) -> str:
    if node_id.startswith("source:"):
        return "source"
    if node_id.startswith("fact:"):
        return "fact"
    if node_id.startswith("rule_card:"):
        return "rule_card"
    if ":" in node_id:
        return node_id.split(":", 1)[0]
    return "node"


def diff_graph(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    prev_nodes, prev_links = graph_maps(previous)
    curr_nodes, curr_links = graph_maps(current)

    added_nodes = sorted(set(curr_nodes) - set(prev_nodes))
    removed_nodes = sorted(set(prev_nodes) - set(curr_nodes))
    common_nodes = sorted(set(curr_nodes) & set(prev_nodes))
    changed_nodes = [
        node_id
        for node_id in common_nodes
        if digest(curr_nodes[node_id]) != digest(prev_nodes[node_id])
    ]

    added_links = sorted(set(curr_links) - set(prev_links))
    removed_links = sorted(set(prev_links) - set(curr_links))
    common_links = sorted(set(curr_links) & set(prev_links))
    changed_links = [
        key
        for key in common_links
        if digest(curr_links[key]) != digest(prev_links[key])
    ]

    crud_counts: dict[str, dict[str, int]] = {}
    for operation, node_ids in {
        "create": added_nodes,
        "delete_or_exclude": removed_nodes,
        "update": changed_nodes,
    }.items():
        for node_id in node_ids:
            entity_type = classify_node_change(node_id)
            crud_counts.setdefault(operation, {})
            crud_counts[operation][entity_type] = crud_counts[operation].get(entity_type, 0) + 1

    return {
        "added_nodes": added_nodes,
        "removed_nodes": removed_nodes,
        "changed_nodes": changed_nodes,
        "added_links": added_links,
        "removed_links": removed_links,
        "changed_links": changed_links,
        "crud_counts": crud_counts,
        "summary": {
            "nodes_before": len(prev_nodes),
            "nodes_after": len(curr_nodes),
            "links_before": len(prev_links),
            "links_after": len(curr_links),
            "added_nodes": len(added_nodes),
            "removed_nodes": len(removed_nodes),
            "changed_nodes": len(changed_nodes),
            "added_links": len(added_links),
            "removed_links": len(removed_links),
            "changed_links": len(changed_links),
        },
    }


def render_md(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Swine Wiki Graph Change Diff",
        "",
        f"Generated: {payload['generated_at']}",
        f"Baseline initialized: {str(payload['baseline_initialized']).lower()}",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## CRUD Counts", ""])
    crud_counts = payload.get("crud_counts", {})
    if crud_counts:
        for operation, counts in crud_counts.items():
            detail = ", ".join(f"{key}: {value}" for key, value in sorted(counts.items()))
            lines.append(f"- {operation}: {detail}")
    else:
        lines.append("- No node-level CRUD changes detected.")
    lines.extend(["", "## Examples", ""])
    for field in ["added_nodes", "removed_nodes", "changed_nodes", "added_links", "removed_links", "changed_links"]:
        values = payload.get(field, [])[:20]
        lines.append(f"### {field}")
        lines.append("")
        if values:
            lines.extend(f"- `{value}`" for value in values)
        else:
            lines.append("- None")
        lines.append("")
    return "\n".join(lines)


def render_html(payload: dict[str, Any]) -> str:
    graph = load_json(GRAPH_JSON)
    summary = payload["summary"]
    payload_text = json.dumps(payload, ensure_ascii=False)
    nodes_text = json.dumps(graph.get("nodes", []), ensure_ascii=False)
    rows = "\n".join(
        f"<tr><th>{html.escape(str(key))}</th><td>{html.escape(str(value))}</td></tr>"
        for key, value in summary.items()
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Swine Wiki Graph Changes</title>
  <style>
    body {{ font-family: "Segoe UI", Arial, sans-serif; margin: 24px; color: #1f2a2e; background: #fbfcf8; }}
    h1, h2 {{ margin-bottom: 8px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0 24px; }}
    th, td {{ border-bottom: 1px solid #d8dfd5; padding: 7px 9px; text-align: left; font-size: 13px; }}
    th {{ width: 220px; color: #42524a; }}
    input {{ width: min(760px, 92vw); padding: 8px; border: 1px solid #9aa8a0; border-radius: 4px; }}
    .pill {{ display: inline-block; padding: 2px 7px; border: 1px solid #9aa8a0; border-radius: 999px; margin: 2px 4px 2px 0; }}
    .muted {{ color: #5b6961; }}
    pre {{ white-space: pre-wrap; background: #f0f3ee; padding: 12px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Swine Wiki Graph Changes</h1>
  <p class="muted">Generated: {html.escape(str(payload['generated_at']))}</p>
  <h2>Change Summary</h2>
  <table>{rows}</table>
  <h2>CRUD Counts</h2>
  <div id="crud"></div>
  <h2>Changed Items</h2>
  <input id="q" placeholder="搜索 added / removed / changed 节点或边">
  <table><thead><tr><th>Type</th><th>ID</th></tr></thead><tbody id="rows"></tbody></table>
  <h2>Current Graph Nodes</h2>
  <p class="muted">用于确认 HTML 已随最新 graph-data.json 生成。</p>
  <table><thead><tr><th>ID</th><th>Label</th><th>Group</th><th>Risk</th><th>Task Use</th></tr></thead><tbody id="nodes"></tbody></table>
  <script>
    const diff = {payload_text};
    const nodes = {nodes_text};
    const crud = document.getElementById('crud');
    crud.innerHTML = Object.entries(diff.crud_counts || {{}})
      .map(([op, counts]) => `<div><strong>${{op}}</strong>: ` + Object.entries(counts).map(([k,v]) => `<span class="pill">${{k}}: ${{v}}</span>`).join('') + `</div>`)
      .join('') || '<p class="muted">No node-level CRUD changes detected.</p>';
    const changeRows = [];
    for (const field of ['added_nodes','removed_nodes','changed_nodes','added_links','removed_links','changed_links']) {{
      for (const value of diff[field] || []) changeRows.push({{type: field, id: value}});
    }}
    const q = document.getElementById('q');
    const rows = document.getElementById('rows');
    function renderChanges() {{
      const needle = q.value.toLowerCase();
      rows.innerHTML = changeRows
        .filter(row => !needle || JSON.stringify(row).toLowerCase().includes(needle))
        .slice(0, 800)
        .map(row => `<tr><td>${{row.type}}</td><td>${{row.id}}</td></tr>`)
        .join('');
    }}
    q.addEventListener('input', renderChanges);
    renderChanges();
    document.getElementById('nodes').innerHTML = nodes.slice(0, 300).map(n =>
      `<tr><td>${{n.id}}</td><td>${{n.label || ''}}</td><td>${{n.group || ''}}</td><td>${{n.risk_class || ''}}</td><td>${{n.task_use_status || ''}}</td></tr>`
    ).join('');
  </script>
</body>
</html>
"""


def append_jsonl(path: Path, item: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def refresh_main_graph_html() -> dict[str, Any]:
    renderer = ROOT / "tools" / "render_wash_interactive_graph.py"
    if not renderer.exists():
        return {"passed": False, "reason": "missing_renderer", "path": renderer.relative_to(ROOT).as_posix()}
    result = subprocess.run(
        [sys.executable, str(renderer)],
        cwd=ROOT.parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "passed": result.returncode == 0,
        "command": " ".join([sys.executable, str(renderer)]),
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute graph CRUD/diff report for the swine LLM Wiki.")
    parser.add_argument("--no-update-snapshot", action="store_true", help="Do not replace the latest graph snapshot.")
    parser.add_argument("--skip-main-html-refresh", action="store_true", help="Do not rerender knowledge-graph.html after diff generation.")
    return parser.parse_args()


def main() -> int:
    """生成图谱变化 diff、刷新快照，并输出审计结果。"""
    args = parse_args()
    if not GRAPH_JSON.exists():
        print(json.dumps({"passed": False, "reason": "missing_graph_data", "path": GRAPH_JSON.as_posix()}, ensure_ascii=False, indent=2))
        return 1

    current = load_json(GRAPH_JSON)
    previous = load_json(LATEST_SNAPSHOT)
    baseline_initialized = not bool(previous)
    if baseline_initialized:
        previous = current

    diff = diff_graph(previous, current)
    payload = {
        "generated_at": now(),
        "baseline_initialized": baseline_initialized,
        "graph_path": GRAPH_JSON.relative_to(ROOT).as_posix(),
        **diff,
    }

    ISSUES.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    DIFF_MD.write_text(render_md(payload), encoding="utf-8")
    CHANGE_HTML.write_text(render_html(payload), encoding="utf-8")
    append_jsonl(CRUD_LOG, payload)
    if not args.no_update_snapshot:
        LATEST_SNAPSHOT.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")

    refresh = {"passed": True, "skipped": True}
    if not args.skip_main_html_refresh:
        refresh = refresh_main_graph_html()
        if not refresh["passed"]:
            print(json.dumps({
                "passed": False,
                "reason": "main_graph_html_refresh_failed",
                "diff_json": DIFF_JSON.relative_to(ROOT).as_posix(),
                "refresh": refresh,
            }, ensure_ascii=False, indent=2))
            return 1

    print(json.dumps({
        "passed": True,
        "baseline_initialized": baseline_initialized,
        "summary": payload["summary"],
        "diff_json": DIFF_JSON.relative_to(ROOT).as_posix(),
        "diff_md": DIFF_MD.relative_to(ROOT).as_posix(),
        "change_html": CHANGE_HTML.relative_to(ROOT).as_posix(),
        "crud_log": CRUD_LOG.relative_to(ROOT).as_posix(),
        "snapshot": LATEST_SNAPSHOT.relative_to(ROOT).as_posix(),
        "main_graph_html_refresh": refresh,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
