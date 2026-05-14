from __future__ import annotations
"""鸡病 LLM Wiki 的知识图谱导出与 HTML 渲染模块。

图谱是从 Wiki 和 exports 派生出来的可视化层，主要用于演示、覆盖率检查、
来源追溯和知识结构审查。它不是正式事实库本身；真正的事实来源仍然是
``wiki/`` 页面和 ``exports/`` 下的结构化文件。

设计原则：
    - 每一条正式事实都应该尽量进入图谱，便于证明数据是否全覆盖。
    - 如果某个事实的 subject 或 object 无法映射成疾病、药品、规则、标准，
      不直接丢弃，而是作为 ``concept`` 概念节点保留。
    - 候选事实也会以 ``candidate`` 节点或边展示，方便看到自动维护产生的
      新变化，但不会把候选内容伪装成已复核事实。
"""

import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from .wiki import clear_llm_wiki_cache, load_llm_wiki


@dataclass(frozen=True)
class GraphBuildResult:
    """一次图谱重建产生的路径和数量统计。

    CLI 返回这个对象后，演示者可以直接说明本次生成了哪些文件、节点多少、
    边多少，以及生成时间。
    """
    wiki_dir: str
    graph_data_path: str
    html_path: str
    mermaid_path: str
    node_count: int
    link_count: int
    generated_at: str


def build_graph_data(wiki_dir: str | Path) -> dict[str, Any]:
    """从当前 Wiki 包构建尽量全覆盖的图谱 JSON。

    输入包括：
        - ``exports`` 中的疾病、药品、规则索引。
        - ``wiki/sources`` 中的来源页。
        - ``exports/knowledge_facts.json`` 中的正式事实。
        - ``exports/knowledge_facts.candidates.json`` 中的候选事实。

    输出包括：
        一个可以序列化为 JSON 的对象，包含 ``metadata``、``nodes`` 和
        ``links``。其中 ``metadata`` 会记录 ``facts_in_graph``、
        ``facts_not_in_graph`` 等覆盖率字段，用于证明正式事实是否全部入图。
    """
    root = Path(wiki_dir)
    clear_llm_wiki_cache()
    kb = load_llm_wiki(root)
    nodes: dict[str, dict[str, Any]] = {}
    links: list[dict[str, Any]] = []
    label_index: dict[str, str] = {}

    for row in kb.disease_index:
        disease_id = row.get("disease_id", "").strip() or f"DISEASE:{row.get('page_relpath', '')}"
        label = row.get("disease_name", "").strip() or disease_id
        _add_node(nodes, disease_id, label, "disease", row)
        _index_label(label_index, label, disease_id)
        source_id = row.get("primary_source_id", "").strip()
        if source_id:
            _add_node(nodes, source_id, source_id, "source", {})
            links.append({"source": disease_id, "target": source_id, "type": "primary-source"})

    for row in kb.drug_index:
        relpath = row.get("page_relpath", "").strip()
        label = row.get("drug_name", "").strip() or row.get("title", "").strip() or Path(relpath).stem
        node_id = f"DRUG:{relpath or label}"
        _add_node(nodes, node_id, label, "drug", row)
        _index_label(label_index, label, node_id)

    for row in kb.rule_index:
        relpath = row.get("page_relpath", "").strip()
        label = row.get("title", "").strip() or Path(relpath).stem
        node_id = f"RULE:{relpath or label}"
        _add_node(nodes, node_id, label, "rule", row)
        _index_label(label_index, label, node_id)

    for page in kb.pages:
        if page.section != "sources":
            continue
        source_id = _source_id_from_text(page.text) or _source_id_from_stem(Path(page.relpath).stem)
        _add_node(nodes, source_id, page.title or source_id, "source", {"page_relpath": page.relpath})
        _index_label(label_index, source_id, source_id)

    governance_events = _load_governance_events(root)
    for event in governance_events:
        _add_governance_event_to_graph(nodes, links, event)

    covered_fact_count = 0
    for fact in kb.facts:
        if _add_fact_to_graph(nodes, links, label_index, fact, candidate=False):
            covered_fact_count += 1

    candidate_facts = _load_json_array(root / "exports" / "knowledge_facts.candidates.json")
    covered_candidate_count = 0
    for fact in candidate_facts:
        if _add_fact_to_graph(nodes, links, label_index, fact, candidate=True):
            covered_candidate_count += 1

    final_links = _dedupe_links(links, nodes)
    metadata = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "diseases": len(kb.disease_index),
        "drugs": len(kb.drug_index),
        "rules": len(kb.rule_index),
        "sources": sum(1 for node in nodes.values() if node.get("group") == "source"),
        "facts": len(kb.facts),
        "candidate_facts": len(candidate_facts),
        "governance_events": len(governance_events),
        "facts_in_graph": covered_fact_count,
        "facts_not_in_graph": max(len(kb.facts) - covered_fact_count, 0),
        "candidate_facts_in_graph": covered_candidate_count,
        "node_groups": _count_groups(nodes.values()),
        "link_types": _count_link_types(final_links),
    }
    return {"metadata": metadata, "nodes": list(nodes.values()), "links": final_links}


def rebuild_graph(wiki_dir: str | Path) -> GraphBuildResult:
    """根据当前 Wiki 重建图谱 JSON、Mermaid 文档和 HTML 页面。

    这是 `graph-build` 命令最终调用的核心函数。知识新增、修改或删除后，
    执行它即可让 ``graph-data.json`` 和 ``knowledge-graph.html`` 跟随变化。
    """
    root = Path(wiki_dir)
    graph = build_graph_data(root)
    graph_data_path = root / "wiki" / "graph-data.json"
    html_path = root / "wiki" / "knowledge-graph.html"
    mermaid_path = root / "wiki" / "knowledge-graph.md"
    graph_data_path.parent.mkdir(parents=True, exist_ok=True)
    graph_data_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    html_path.write_text(render_graph_html(graph), encoding="utf-8")
    mermaid_path.write_text(render_mermaid_graph(graph), encoding="utf-8")
    return GraphBuildResult(
        wiki_dir=str(root),
        graph_data_path=str(graph_data_path),
        html_path=str(html_path),
        mermaid_path=str(mermaid_path),
        node_count=len(graph["nodes"]),
        link_count=len(graph["links"]),
        generated_at=str(graph["metadata"]["generated_at"]),
    )


def watch_graph(wiki_dir: str | Path, *, interval_seconds: float = 2.0, once: bool = False) -> GraphBuildResult:
    """监控 Wiki 和 exports 文件变化，并在变化时重建图谱。

    ``once=True`` 时只重建一次，适合测试或 CLI 快速验证；持续监控模式适合
    本地演示时边改知识库边刷新图谱。
    """
    root = Path(wiki_dir)
    last_signature = ""
    result = rebuild_graph(root)
    if once:
        return result
    while True:
        signature = _wiki_signature(root)
        if signature != last_signature:
            result = rebuild_graph(root)
            last_signature = signature
        time.sleep(max(float(interval_seconds), 0.5))


def render_graph_html(graph: Mapping[str, Any]) -> str:
    """渲染一个自包含的 D3 交互式 HTML 图谱页面。

    HTML 内部会嵌入一份图谱数据，因此可以直接双击离线打开；如果在浏览器
    或本地服务环境中打开，它也会尝试重新加载旁边的 ``graph-data.json``。
    这样既支持简单文件演示，也支持本地开发服务器演示。
    """
    embedded = json.dumps(graph, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chicken Disease LLM Wiki Graph</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <style>
    body {{ font-family: "Segoe UI", Arial, sans-serif; margin: 0; background: #f6f7f2; color: #17212b; overflow: hidden; }}
    header {{ padding: 12px 18px 8px; border-bottom: 1px solid #d9dfd2; background: #fbfcf8; }}
    h1 {{ margin: 0 0 6px; font-size: 24px; }}
    .meta {{ color: #56636f; font-size: 13px; display: flex; gap: 14px; flex-wrap: wrap; }}
    .toolbar {{ padding: 10px 18px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; background: #f6f7f2; }}
    input {{ min-width: 300px; padding: 7px 9px; border: 1px solid #b8c3b3; border-radius: 4px; font-size: 14px; }}
    button {{ padding: 7px 10px; border: 1px solid #9aa98f; background: #fff; border-radius: 4px; cursor: pointer; }}
    label {{ display: inline-flex; align-items: center; gap: 5px; font-size: 13px; color: #394650; }}
    .legend {{ display: flex; gap: 12px; padding: 0 18px 9px; flex-wrap: wrap; background: #f6f7f2; }}
    .legend span {{ display: inline-flex; align-items: center; gap: 6px; font-size: 13px; }}
    .dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
    #graph {{ width: 100%; height: calc(100vh - 150px); display: block; background: #fbfcf8; border-top: 1px solid #e2e6dc; }}
    .node-label {{ font-size: 10px; fill: #27323b; paint-order: stroke; stroke: #fbfcf8; stroke-width: 3px; stroke-linejoin: round; pointer-events: none; }}
    .tooltip {{ position: fixed; pointer-events: none; background: rgba(23,33,43,.92); color: #fff; padding: 8px 10px; border-radius: 6px; font-size: 12px; opacity: 0; max-width: 420px; }}
  </style>
</head>
<body>
  <header>
    <h1>Chicken Disease LLM Wiki Graph</h1>
    <div class="meta">
      <span id="generatedAt"></span>
      <span id="counts"></span>
      <span id="coverage"></span>
      <span>数据源: graph-data.json，刷新或打开页面时同步。</span>
    </div>
  </header>
  <div class="toolbar">
    <input id="search" placeholder="搜索疾病、药物、规则、来源、事实对象">
    <button id="reload">刷新图谱数据</button>
    <button id="fit">适配视图</button>
    <button id="clear">清除筛选</button>
    <label><input id="showLabels" type="checkbox">显示标签</label>
    <label><input id="hideCandidates" type="checkbox">隐藏候选</label>
  </div>
  <div class="legend">
    <span><i class="dot" style="background:#c8553d"></i>Disease</span>
    <span><i class="dot" style="background:#5a9b62"></i>Drug</span>
    <span><i class="dot" style="background:#3d6f96"></i>Standard</span>
    <span><i class="dot" style="background:#8b5ca8"></i>Rule</span>
    <span><i class="dot" style="background:#7b7f83"></i>Source</span>
    <span><i class="dot" style="background:#b8892d"></i>Concept</span>
    <span><i class="dot" style="background:#d07aa7"></i>Candidate</span>
  </div>
  <svg id="graph"></svg>
  <div class="tooltip" id="tooltip"></div>
  <script>
    const embeddedGraph = {embedded};
    let currentGraph = embeddedGraph;

    async function loadGraph() {{
      try {{
        const response = await fetch('graph-data.json?ts=' + Date.now(), {{ cache: 'no-store' }});
        if (response.ok) currentGraph = await response.json();
      }} catch (error) {{
        currentGraph = embeddedGraph;
      }}
      render(currentGraph);
    }}

    function color(group) {{
      return {{ disease: '#c8553d', drug: '#5a9b62', standard: '#3d6f96', rule: '#8b5ca8', source: '#7b7f83', concept: '#b8892d', candidate: '#d07aa7' }}[group] || '#555';
    }}

    function radius(group) {{
      return {{ disease: 8, drug: 6, standard: 6, rule: 6, source: 4, concept: 4, candidate: 4 }}[group] || 4;
    }}

    function render(graph) {{
      const svg = d3.select('#graph');
      svg.selectAll('*').remove();
      const width = window.innerWidth;
      const height = Math.max(560, window.innerHeight - 150);
      svg.attr('viewBox', [0, 0, width, height]);
      const tooltip = d3.select('#tooltip');
      const metadata = graph.metadata || {{}};
      document.getElementById('generatedAt').textContent = '生成时间: ' + (metadata.generated_at || 'unknown');
      document.getElementById('counts').textContent = `节点 ${{graph.nodes.length}} / 连线 ${{graph.links.length}} / 疾病 ${{metadata.diseases || 0}} / 药物 ${{metadata.drugs || 0}} / 规则 ${{metadata.rules || 0}} / 来源 ${{metadata.sources || 0}}`;
      document.getElementById('coverage').textContent = `正式事实入图 ${{metadata.facts_in_graph || 0}}/${{metadata.facts || 0}}，候选 ${{metadata.candidate_facts_in_graph || 0}}/${{metadata.candidate_facts || 0}}`;

      const nodes = graph.nodes.map((d, i) => {{
        const angle = (i / Math.max(graph.nodes.length, 1)) * Math.PI * 2;
        const ring = 80 + (i % 13) * 26;
        return {{ ...d, x: width / 2 + Math.cos(angle) * ring, y: height / 2 + Math.sin(angle) * ring }};
      }});
      const links = graph.links.map(d => ({{ ...d }}));
      const sim = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(d => d.type === 'evidence' ? 32 : 46).strength(0.28))
        .force('charge', d3.forceManyBody().strength(-34))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('x', d3.forceX(width / 2).strength(0.02))
        .force('y', d3.forceY(height / 2).strength(0.02))
        .force('collision', d3.forceCollide().radius(d => radius(d.group) + 5));

      const zoomLayer = svg.append('g');
      const link = zoomLayer.append('g').attr('stroke', '#aeb8bd').attr('stroke-opacity', 0.42)
        .selectAll('line').data(links).join('line').attr('stroke-width', d => d.type === 'candidate-fact' ? 0.8 : 1);
      const node = zoomLayer.append('g').attr('stroke', '#fff').attr('stroke-width', 1.1)
        .selectAll('circle').data(nodes).join('circle')
        .attr('r', d => radius(d.group)).attr('fill', d => color(d.group))
        .call(d3.drag()
          .on('start', (event, d) => {{ if (!event.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }})
          .on('drag', (event, d) => {{ d.fx = event.x; d.fy = event.y; }})
          .on('end', (event, d) => {{ if (!event.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }}));
      const label = zoomLayer.append('g').selectAll('text').data(nodes).join('text')
        .attr('class', 'node-label').attr('dy', -9).text(d => String(d.label || d.id).slice(0, 28)).style('display', 'none');

      node.on('mousemove', (event, d) => tooltip.style('opacity', 1).style('left', `${{event.clientX + 12}}px`).style('top', `${{event.clientY + 12}}px`).html(`<b>${{d.label}}</b><br>${{d.group}}<br>${{d.id}}<br>${{d.relpath || ''}}`))
        .on('mouseleave', () => tooltip.style('opacity', 0));

      sim.on('tick', () => {{
        nodes.forEach(d => {{ d.x = Math.max(18, Math.min(width - 18, d.x)); d.y = Math.max(18, Math.min(height - 18, d.y)); }});
        link.attr('x1', d => d.source.x).attr('y1', d => d.source.y).attr('x2', d => d.target.x).attr('y2', d => d.target.y);
        node.attr('cx', d => d.x).attr('cy', d => d.y);
        label.attr('x', d => d.x).attr('y', d => d.y);
      }});

      const zoom = d3.zoom().scaleExtent([0.25, 6]).on('zoom', event => zoomLayer.attr('transform', event.transform));
      svg.call(zoom);
      function applyFilters() {{
        const q = document.getElementById('search').value.trim().toLowerCase();
        const hideCandidates = document.getElementById('hideCandidates').checked;
        const showLabels = document.getElementById('showLabels').checked;
        const match = d => (!q || String(d.label || '').toLowerCase().includes(q) || String(d.id || '').toLowerCase().includes(q) || String(d.relpath || '').toLowerCase().includes(q)) && !(hideCandidates && d.group === 'candidate');
        node.attr('opacity', d => match(d) ? 1 : 0.08);
        label.style('display', d => showLabels && match(d) ? 'block' : 'none').attr('opacity', d => match(d) ? 1 : 0.08);
        link.attr('opacity', d => !q && !hideCandidates ? 0.42 : 0.08);
      }}
      document.getElementById('search').oninput = applyFilters;
      document.getElementById('showLabels').onchange = applyFilters;
      document.getElementById('hideCandidates').onchange = applyFilters;
      document.getElementById('fit').onclick = () => svg.transition().duration(350).call(zoom.transform, d3.zoomIdentity);
    }}

    document.getElementById('reload').onclick = loadGraph;
    document.getElementById('clear').onclick = () => {{ document.getElementById('search').value = ''; document.getElementById('hideCandidates').checked = false; render(currentGraph); }};
    loadGraph();
  </script>
</body>
</html>
"""


def render_mermaid_graph(graph: Mapping[str, Any], *, max_edges: int = 160) -> str:
    """渲染一份精简 Mermaid 图，用于文档或快速审查。

    Mermaid 版本不会展示全部大图细节，只保留有限数量的边，避免文档过长。
    真正完整的交互式展示应打开 ``knowledge-graph.html``。
    """
    nodes = list(graph.get("nodes") or [])
    links = list(graph.get("links") or [])
    labels = {str(node.get("id")): str(node.get("label") or node.get("id")) for node in nodes if isinstance(node, Mapping)}
    lines = [
        "# Chicken Disease LLM Wiki Graph (Mermaid)",
        "",
        "> Derived from wiki/graph-data.json. Open wiki/knowledge-graph.html for the interactive full-coverage view.",
        "",
        "```mermaid",
        "graph LR",
    ]
    used = False
    for link in links[: max(int(max_edges), 1)]:
        if not isinstance(link, Mapping):
            continue
        source = str(link.get("source") or "")
        target = str(link.get("target") or "")
        if not source or not target:
            continue
        used = True
        relation = str(link.get("type") or "related")
        lines.append(
            f'  {_mermaid_id(source)}["{_escape_mermaid_label(labels.get(source, source))}"] '
            f'-->|{_escape_mermaid_label(relation)}| '
            f'{_mermaid_id(target)}["{_escape_mermaid_label(labels.get(target, target))}"]'
        )
    if not used:
        for node in nodes[:80]:
            if isinstance(node, Mapping):
                node_id = str(node.get("id") or "node")
                label = str(node.get("label") or node_id)
                lines.append(f'  {_mermaid_id(node_id)}["{_escape_mermaid_label(label)}"]')
    if len(links) > max_edges:
        lines.append(f'  omitted["{len(links) - max_edges} more links omitted; open knowledge-graph.html"]')
    lines.extend(["```", ""])
    return "\n".join(lines)


def _add_fact_to_graph(
    nodes: dict[str, dict[str, Any]],
    links: list[dict[str, Any]],
    label_index: dict[str, str],
    fact: Mapping[str, Any],
    *,
    candidate: bool,
) -> bool:
    """把一条正式事实或候选事实加入图谱节点和边。

    处理逻辑：
    - subject 一定会映射成一个节点。
    - object 如果存在，也会映射成一个节点，并通过 predicate 边连接。
    - evidence_source_id 会额外生成一条 evidence 边，表示该事实可追溯到
      哪个来源。
    - candidate=True 时，边类型会标记为候选，避免和正式事实混淆。
    """
    subject = str(fact.get("subject") or "").strip()
    predicate = str(fact.get("predicate") or "related_to").strip() or "related_to"
    obj = str(fact.get("object") or "").strip()
    if not subject:
        return False

    subject_id = _node_for_value(nodes, label_index, subject, _group_for_subject(fact, candidate), fact)
    if obj:
        object_group = "candidate" if candidate else _group_for_object(predicate, obj, fact)
        object_id = _node_for_value(nodes, label_index, obj, object_group, fact)
        links.append(
            {
                "source": subject_id,
                "target": object_id,
                "type": "candidate-fact" if candidate else predicate,
                "predicate": predicate,
                "fact_id": str(fact.get("fact_id") or ""),
                "evidence_status": str(fact.get("evidence_status") or ""),
            }
        )
    else:
        object_id = ""

    source_id = str(fact.get("evidence_source_id") or fact.get("evidence_source") or "").strip()
    if source_id:
        _add_node(nodes, source_id, source_id, "source", {})
        links.append(
            {
                "source": subject_id,
                "target": source_id,
                "type": "candidate-evidence" if candidate else "evidence",
                "fact_id": str(fact.get("fact_id") or ""),
            }
        )
        if object_id and predicate == "diagnosis_standard_anchor":
            links.append({"source": object_id, "target": source_id, "type": "described-by"})
    return True


def _node_for_value(
    nodes: dict[str, dict[str, Any]],
    label_index: dict[str, str],
    value: str,
    group: str,
    payload: Mapping[str, Any],
) -> str:
    """根据文本值寻找已有节点，找不到时创建一个指定类型的新节点。

    这样可以让同名疾病、药品、标准等尽量复用同一个节点，减少图谱重复。
    """
    normalized = _normalize_label(value)
    existing = label_index.get(normalized)
    if existing:
        return existing
    node_id = f"{group.upper()}:{_hash(value)}"
    _add_node(nodes, node_id, _short_label(value), group, payload)
    _index_label(label_index, value, node_id)
    return node_id


def _group_for_subject(fact: Mapping[str, Any], candidate: bool) -> str:
    """根据事实类型推断 subject 节点所属分组。"""
    if candidate:
        return "candidate"
    fact_type = str(fact.get("fact_type") or "").lower()
    if "drug" in fact_type:
        return "drug"
    if "rule" in fact_type or "regulatory" in fact_type:
        return "rule"
    if "disease" in fact_type or str(fact.get("fact_id") or "").startswith("DIS-"):
        return "disease"
    return "concept"


def _group_for_object(predicate: str, value: str, fact: Mapping[str, Any]) -> str:
    """根据 predicate、object 值和 fact_type 推断 object 节点分组。"""
    lower_predicate = predicate.lower()
    if "standard" in lower_predicate:
        return "standard"
    if "drug" in lower_predicate:
        return "drug"
    if "rule" in lower_predicate or "regulatory" in lower_predicate or "prohibited" in lower_predicate:
        return "rule"
    if "disease" in lower_predicate or str(value).startswith("DIS-"):
        return "disease"
    fact_type = str(fact.get("fact_type") or "").lower()
    if "standard" in fact_type:
        return "standard"
    return "concept"


def _add_node(nodes: dict[str, dict[str, Any]], node_id: str, label: str, group: str, payload: Mapping[str, Any]) -> None:
    """插入节点，并尽量保留已存在节点中更完整的元数据。

    如果节点已经存在，只在缺少 relpath 且新数据有 relpath 时补充路径，不会
    覆盖已有的标签和分组。
    """
    if not node_id:
        return
    existing = nodes.get(node_id)
    if existing:
        if not existing.get("relpath") and payload.get("page_relpath"):
            existing["relpath"] = payload.get("page_relpath", "")
        return
    nodes[node_id] = {
        "id": node_id,
        "label": label or node_id,
        "group": group,
        "relpath": payload.get("page_relpath", ""),
        "evidence_status": payload.get("evidence_status", ""),
        "semantic_action": payload.get("semantic_action", ""),
    }


def _add_governance_event_to_graph(nodes: dict[str, dict[str, Any]], links: list[dict[str, Any]], event: Mapping[str, Any]) -> None:
    event_id = str(event.get("event_id") or "")
    if not event_id:
        return
    operation = str(event.get("operation") or "")
    semantic_action = str(event.get("semantic_action") or "unknown")
    status = str(event.get("status") or "")
    label = f"{operation}:{semantic_action}:{status}"
    _add_node(
        nodes,
        event_id,
        label,
        "governance",
        {"evidence_status": status, "semantic_action": semantic_action},
    )
    for source_id in _source_ids_from_governance_event(event):
        _add_node(nodes, source_id, source_id, "source", {})
        links.append(
            {
                "source": event_id,
                "target": source_id,
                "type": f"governance-{operation or 'change'}",
                "semantic_action": semantic_action,
                "fact_id": event_id,
            }
        )
    replacement = str((event.get("details") or {}).get("replacement_source") or "")
    if replacement:
        replacement_id = _source_id_from_stem(Path(replacement).stem)
        if replacement_id:
            _add_node(nodes, replacement_id, replacement_id, "source", {})
            links.append(
                {
                    "source": event_id,
                    "target": replacement_id,
                    "type": "governance-replacement",
                    "semantic_action": semantic_action,
                    "fact_id": event_id,
                }
            )


def _index_label(label_index: dict[str, str], label: str, node_id: str) -> None:
    """建立“可读标签 -> 节点 ID”的索引，供后续精确匹配使用。"""
    normalized = _normalize_label(label)
    if normalized and normalized not in label_index:
        label_index[normalized] = node_id


def _dedupe_links(links: list[dict[str, Any]], nodes: Mapping[str, Any]) -> list[dict[str, Any]]:
    """去除重复边和悬空边。

    悬空边是指 source 或 target 节点不存在的边，这类边会导致前端图谱异常，
    所以在写入 graph-data.json 前统一过滤。
    """
    seen: set[tuple[str, str, str, str]] = set()
    result: list[dict[str, Any]] = []
    for link in links:
        source = str(link.get("source") or "")
        target = str(link.get("target") or "")
        link_type = str(link.get("type") or "")
        fact_id = str(link.get("fact_id") or "")
        if not source or not target or source not in nodes or target not in nodes:
            continue
        key = (source, target, link_type, fact_id)
        if key in seen:
            continue
        seen.add(key)
        result.append(dict(link))
    return result


def _load_json_array(path: Path) -> list[dict[str, Any]]:
    """防御性读取 JSON 数组导出文件。"""
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, list):
        return []
    return [dict(item) for item in payload if isinstance(item, Mapping)]


def _load_governance_events(root: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    issues_dir = root / "issues"
    if not issues_dir.is_dir():
        return events
    for path in sorted(issues_dir.glob("wiki_governance_audit_*.jsonl")):
        try:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        except OSError:
            continue
        for line in lines:
            text = line.strip()
            if not text:
                continue
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, Mapping):
                events.append(dict(payload))
    return events


def _source_ids_from_governance_event(event: Mapping[str, Any]) -> tuple[str, ...]:
    values: list[str] = []
    target = str(event.get("target") or "")
    values.extend(re.findall(r"SRC-\d+", target))
    details = event.get("details") if isinstance(event.get("details"), Mapping) else {}
    for key in ("created_sources", "deleted_paths"):
        value = details.get(key)
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        elif value:
            values.append(str(value))
    for key in ("source_page", "replacement_source", "graph_data_path"):
        value = details.get(key)
        if value:
            values.append(str(value))
    source_ids: list[str] = []
    for value in values:
        source_ids.extend(re.findall(r"SRC-\d+", value))
        if "SRC-" in value:
            source_ids.append(_source_id_from_stem(Path(value).stem))
    return tuple(dict.fromkeys(source_id for source_id in source_ids if source_id))


def _source_id_from_text(text: str) -> str:
    """从来源页 frontmatter 或文本中提取 ``source_id``。"""
    match = re.search(r"(?m)^source_id:\s*([A-Za-z]+-\d+)\s*$", text)
    return match.group(1) if match else ""


def _source_id_from_stem(stem: str) -> str:
    """从来源页文件名中提取 ``SRC-xxxx``。"""
    parts = stem.split("-")
    if len(parts) >= 2 and parts[0] == "SRC" and parts[1].isdigit():
        return f"{parts[0]}-{parts[1]}"
    return stem


def _normalize_label(value: str) -> str:
    """规范化标签文本，用于图谱节点的精确匹配。"""
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _short_label(value: str, *, limit: int = 72) -> str:
    """把过长的事实对象截短，避免图谱 UI 标签过长。"""
    text = re.sub(r"\s+", " ", str(value or "").strip())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _hash(value: str) -> str:
    """为 concept 或 candidate 节点生成稳定的短 ID。"""
    return hashlib.sha1(str(value).encode("utf-8")).hexdigest()[:14]


def _count_groups(nodes: Any) -> dict[str, int]:
    """统计各类节点数量，写入图谱 metadata。"""
    counts: dict[str, int] = {}
    for node in nodes:
        group = str(node.get("group") or "unknown")
        counts[group] = counts.get(group, 0) + 1
    return dict(sorted(counts.items()))


def _count_link_types(links: Any) -> dict[str, int]:
    """统计各类边数量，写入图谱 metadata。"""
    counts: dict[str, int] = {}
    for link in links:
        link_type = str(link.get("type") or "unknown")
        counts[link_type] = counts.get(link_type, 0) + 1
    return dict(sorted(counts.items()))


def _mermaid_id(value: str) -> str:
    """把任意图谱 ID 转成 Mermaid 可接受的节点标识。"""
    safe = "".join(ch if ch.isalnum() else "_" for ch in str(value or ""))
    if not safe or safe[0].isdigit():
        safe = f"n_{safe}"
    return safe[:80]


def _escape_mermaid_label(value: str) -> str:
    """转义 Mermaid 标签，避免引号或换行破坏图语法。"""
    return str(value or "").replace('"', "'").replace("\n", " ")[:90]


def _wiki_signature(root: Path) -> str:
    """为 graph-watch 构建轻量级变化签名。

    签名由文件数量和最新修改时间组成。它不读取全部文件内容，性能开销低，
    足以判断是否需要重新构建图谱。
    """
    newest = 0
    count = 0
    for base in (root / "wiki", root / "exports"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.name not in {"graph-data.json", "knowledge-graph.html", "knowledge-graph.md"}:
                stat = path.stat()
                newest = max(newest, int(stat.st_mtime_ns))
                count += 1
    return f"{count}:{newest}"
