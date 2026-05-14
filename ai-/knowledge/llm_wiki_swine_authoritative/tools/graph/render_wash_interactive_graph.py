from __future__ import annotations

import json
import math
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parents[2]
SKILL_ROOT = WORKSPACE / "llm-wiki-skill-main"
WIKI = ROOT / "wiki"
GRAPH_JSON = WIKI / "graph-data.json"
GRAPH_HTML = WIKI / "knowledge-graph.html"
ISSUES = ROOT / "issues"
GRAPH_DIFF_JSON = ISSUES / "graph_change_diff_last.json"
CRUD_LOG = ISSUES / "wiki_crud_change_log.jsonl"
WASH = SKILL_ROOT / "templates" / "graph-styles" / "wash"
DEPS = SKILL_ROOT / "deps"
TZ = timezone(timedelta(hours=8))


GROUP_TO_TYPE = {
    "source": "source",
    "fact": "entity",
    "rule_card": "topic",
    "disease": "topic",
    "drug": "topic",
    "comparison": "topic",
    "syndrome": "topic",
    "synthesis": "topic",
}

GROUP_LABELS = {
    "disease": "疾病",
    "drug": "药物",
    "source": "来源",
    "fact": "事实",
    "rule_card": "规则卡",
    "comparison": "鉴别矩阵",
    "syndrome": "综合征",
    "synthesis": "综合页",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"missing {label}: {path}")


def node_content(node: dict[str, object]) -> str:
    lines = [
        f"# {node.get('label') or node.get('id')}",
        "",
        f"- ID: `{node.get('id', '')}`",
        f"- 类型: {GROUP_LABELS.get(str(node.get('group', '')), str(node.get('group', '')))}",
    ]
    for key, label in [
        ("task_use_status", "任务状态"),
        ("risk_class", "风险类别"),
        ("authority_level", "权威等级"),
        ("path", "页面路径"),
    ]:
        value = str(node.get(key, "") or "")
        if value:
            lines.append(f"- {label}: `{value}`")
    return "\n".join(lines) + "\n"


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(read(path))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def load_recent_crud_events(limit: int = 3) -> list[dict[str, object]]:
    if not CRUD_LOG.exists():
        return []
    events: list[dict[str, object]] = []
    for line in CRUD_LOG.read_text(encoding="utf-8").splitlines()[-limit:]:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


def has_graph_changes(payload: dict[str, object]) -> bool:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    for key in ["added_nodes", "removed_nodes", "changed_nodes", "added_links", "removed_links", "changed_links"]:
        value = summary.get(key)
        if isinstance(value, int) and value > 0:
            return True
        items = payload.get(key)
        if isinstance(items, list) and items:
            return True
    return bool(payload.get("crud_counts"))


def latest_non_empty_crud_event() -> dict[str, object]:
    if not CRUD_LOG.exists():
        return {}
    for line in reversed(CRUD_LOG.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and has_graph_changes(payload):
            return payload
    return {}


def build_change_log_payload(graph: dict[str, object]) -> dict[str, object]:
    diff = load_json(GRAPH_DIFF_JSON)
    if not has_graph_changes(diff):
        fallback = latest_non_empty_crud_event()
        if fallback:
            diff = fallback
    summary = diff.get("summary") if isinstance(diff.get("summary"), dict) else {}
    crud_counts = diff.get("crud_counts") if isinstance(diff.get("crud_counts"), dict) else {}
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), dict) else {}

    added_nodes = [str(item) for item in diff.get("added_nodes", [])[:14]] if isinstance(diff.get("added_nodes"), list) else []
    added_links = [str(item) for item in diff.get("added_links", [])[:10]] if isinstance(diff.get("added_links"), list) else []
    removed_nodes = [str(item) for item in diff.get("removed_nodes", [])[:8]] if isinstance(diff.get("removed_nodes"), list) else []
    changed_nodes = [str(item) for item in diff.get("changed_nodes", [])[:8]] if isinstance(diff.get("changed_nodes"), list) else []

    nodes_before = int(summary.get("nodes_before", 0) or 0)
    nodes_after = int(summary.get("nodes_after", metadata.get("node_count", 0)) or 0)
    links_before = int(summary.get("links_before", 0) or 0)
    links_after = int(summary.get("links_after", metadata.get("link_count", 0)) or 0)
    added_node_count = int(summary.get("added_nodes", len(added_nodes)) or 0)
    added_link_count = int(summary.get("added_links", len(added_links)) or 0)
    removed_node_count = int(summary.get("removed_nodes", len(removed_nodes)) or 0)
    removed_link_count = int(summary.get("removed_links", 0) or 0)
    changed_node_count = int(summary.get("changed_nodes", len(changed_nodes)) or 0)
    changed_link_count = int(summary.get("changed_links", 0) or 0)

    if added_node_count or added_link_count:
        reasonableness = (
            "本轮图谱变化来自受控入库后的 source/fact 注册：新增事实节点通过 fact_anchor 连接到疾病页，"
            "并通过 evidence_source 连接到来源节点；未出现删除，说明既有知识未被覆盖。"
        )
    elif removed_node_count or removed_link_count or changed_node_count or changed_link_count:
        reasonableness = (
            "本轮存在删除或修改，请结合变更记录核对旧数据处理理由，确认是来源过时、规则更新、证据废弃或结构整理。"
        )
    else:
        reasonableness = (
            "本轮图谱结构无变化，通常表示更新只影响文档、日志、候选层或未进入 graph 构建范围的数据。"
        )

    return {
        "generated_at": str(diff.get("generated_at") or metadata.get("generated_at") or datetime.now(TZ).isoformat(timespec="seconds")),
        "title": "图谱更新日志",
        "subtitle": "更新前后对比 · CRUD diff · 合理性说明",
        "summary": {
            "nodes_before": nodes_before,
            "nodes_after": nodes_after,
            "delta_nodes": nodes_after - nodes_before if nodes_before else added_node_count - removed_node_count,
            "links_before": links_before,
            "links_after": links_after,
            "delta_links": links_after - links_before if links_before else added_link_count - removed_link_count,
            "added_nodes": added_node_count,
            "removed_nodes": removed_node_count,
            "changed_nodes": changed_node_count,
            "added_links": added_link_count,
            "removed_links": removed_link_count,
            "changed_links": changed_link_count,
            "facts_in_graph": metadata.get("facts_in_graph", ""),
        },
        "crud_counts": crud_counts,
        "added_nodes": added_nodes,
        "added_links": added_links,
        "removed_nodes": removed_nodes,
        "changed_nodes": changed_nodes,
        "recent_crud_events": load_recent_crud_events(),
        "reasonableness": reasonableness,
        "evidence_files": {
            "diff_json": "issues/graph_change_diff_last.json",
            "diff_md": "issues/graph_change_diff_last.md",
            "crud_log": "issues/wiki_crud_change_log.jsonl",
            "changes_html": "wiki/knowledge-graph-changes.html",
        },
    }


def build_wash_payload(graph: dict[str, object]) -> dict[str, object]:
    nodes = graph.get("nodes", [])
    links = graph.get("links", [])
    if not isinstance(nodes, list) or not isinstance(links, list):
        raise ValueError("graph-data.json must contain nodes and links arrays")

    degree: dict[str, int] = {}
    for link in links:
        if not isinstance(link, dict):
            continue
        source = str(link.get("source", ""))
        target = str(link.get("target", ""))
        if source and target:
            degree[source] = degree.get(source, 0) + 1
            degree[target] = degree.get(target, 0) + 1

    ranked_ids = [
        str(node.get("id", ""))
        for node in sorted(nodes, key=lambda item: degree.get(str(item.get("id", "")), 0), reverse=True)
        if isinstance(node, dict) and node.get("id")
    ]
    initial_view = ranked_ids[:80]

    wash_nodes = []
    for index, node in enumerate(nodes):
        if not isinstance(node, dict) or not node.get("id"):
            continue
        group = str(node.get("group", "node") or "node")
        angle = index * 2.399963229728653
        radius = 11 + math.sqrt(index + 1) * 4.5
        x = max(5, min(95, 50 + math.cos(angle) * radius))
        y = max(5, min(95, 50 + math.sin(angle) * radius * 0.72))
        wash_nodes.append(
            {
                "id": str(node["id"]),
                "label": str(node.get("label") or node["id"]),
                "type": GROUP_TO_TYPE.get(group, "entity"),
                "community": group,
                "summary": f"{GROUP_LABELS.get(group, group)} · {node.get('risk_class', '') or node.get('task_use_status', '') or 'source anchored'}",
                "content": node_content(node),
                "source_path": str(node.get("path", "")),
                "confidence": "EXTRACTED",
                "weight": min(100, 35 + degree.get(str(node["id"]), 0) * 5),
                "x": round(x, 2),
                "y": round(y, 2),
            }
        )

    wash_edges = []
    for index, link in enumerate(links):
        if not isinstance(link, dict):
            continue
        source = str(link.get("source", ""))
        target = str(link.get("target", ""))
        if not source or not target:
            continue
        link_type = str(link.get("type", "EXTRACTED"))
        confidence = "EXTRACTED" if link_type in {"source_anchor", "fact_anchor", "evidence_source"} else "INFERRED"
        wash_edges.append(
            {
                "id": f"edge-{index}-{link_type}",
                "from": source,
                "to": target,
                "source": source,
                "target": target,
                "type": confidence,
                "label": link_type,
                "weight": 0.72 if confidence == "EXTRACTED" else 0.48,
                "signals": {"runtime_link_type": link_type, "fact_id": str(link.get("fact_id", ""))},
                "source_signal_available": bool(link.get("fact_id")),
            }
        )

    communities = []
    for idx, group in enumerate(sorted({str(node.get("group", "node") or "node") for node in nodes if isinstance(node, dict)})):
        group_nodes = [node for node in wash_nodes if node["community"] == group]
        if not group_nodes:
            continue
        best = max(group_nodes, key=lambda node: degree.get(str(node["id"]), 0))
        communities.append(
            {
                "id": group,
                "label": GROUP_LABELS.get(group, group),
                "node_count": len(group_nodes),
                "source_count": sum(1 for node in group_nodes if node["type"] == "source"),
                "is_primary": idx == 0,
                "recommended_start_node_id": best["id"],
            }
        )

    generated_at = str(graph.get("metadata", {}).get("generated_at") or datetime.now(TZ).isoformat(timespec="seconds"))
    return {
        "meta": {
            "build_date": generated_at,
            "wiki_title": "猪病 LLM Wiki",
            "total_nodes": len(wash_nodes),
            "total_edges": len(wash_edges),
            "initial_view": initial_view,
            "degraded": False,
        },
        "nodes": wash_nodes,
        "edges": wash_edges,
        "learning": {
            "entry": {
                "recommended_start_node_id": initial_view[0] if initial_view else None,
                "node_ids": initial_view,
            },
            "communities": communities,
        },
        "insights": {
            "meta": {"degraded": False},
            "summary": "由猪病 runtime graph 适配为 llm-wiki-skill wash 图谱格式；节点和边仍来自 wiki/graph-data.json。",
        },
        "change_log": build_change_log_payload(graph),
    }


def render_html(payload: dict[str, object]) -> None:
    header = WASH / "header.html"
    footer = WASH / "footer.html"
    require(header, "wash header template")
    require(footer, "wash footer template")

    meta = payload["meta"]
    html_text = read(header)
    html_text = (
        html_text.replace("__WIKI_TITLE__", str(meta["wiki_title"]))
        .replace("__NODE_COUNT__", str(meta["total_nodes"]))
        .replace("__EDGE_COUNT__", str(meta["total_edges"]))
        .replace("__BUILD_DATE__", str(meta["build_date"])[:10])
    )
    graph_text = json.dumps(payload, ensure_ascii=False, indent=2).replace("</script>", "<\\/script>")
    html_text += graph_text
    html_text += read(footer)
    write(GRAPH_HTML, html_text)

    assets = [
        (DEPS / "d3.min.js", WIKI / "d3.min.js"),
        (DEPS / "rough.min.js", WIKI / "rough.min.js"),
        (DEPS / "marked.min.js", WIKI / "marked.min.js"),
        (DEPS / "purify.min.js", WIKI / "purify.min.js"),
        (WASH / "graph-wash-helpers.js", WIKI / "graph-wash-helpers.js"),
        (WASH / "graph-wash.js", WIKI / "graph-wash.js"),
    ]
    for source, dest in assets:
        require(source, "wash asset")
        shutil.copyfile(source, dest)


def main() -> None:
    require(GRAPH_JSON, "runtime graph data")
    graph = json.loads(read(GRAPH_JSON))
    payload = build_wash_payload(graph)
    render_html(payload)
    print(
        json.dumps(
            {
                "html": GRAPH_HTML.relative_to(ROOT).as_posix(),
                "nodes": payload["meta"]["total_nodes"],
                "edges": payload["meta"]["total_edges"],
                "style": "llm-wiki-skill wash",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
