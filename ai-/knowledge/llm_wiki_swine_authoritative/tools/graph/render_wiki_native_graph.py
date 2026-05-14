from __future__ import annotations

import json
import math
import shutil
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parents[2]
SKILL_ROOT = WORKSPACE / "llm-wiki-skill-main"
WIKI = ROOT / "wiki"
ISSUES = ROOT / "issues"
GRAPH_JSON = WIKI / "wiki-native-graph.json"
GRAPH_HTML = WIKI / "wiki-native-knowledge-graph.html"
GRAPH_AUDIT_HTML = WIKI / "wiki-native-knowledge-graph-audit.html"
REPORT_JSON = ISSUES / "wiki_native_graph_build_report.json"
NATIVE_DIFF_JSON = ISSUES / "wiki_native_graph_change_diff_last.json"
WASH = SKILL_ROOT / "templates" / "graph-styles" / "wash"
DEPS = SKILL_ROOT / "deps"
TZ = timezone(timedelta(hours=8))

# 默认主图不直接绘制原始 section 节点。
# section 仍完整保留在 wiki-native-graph.json 和审计图中；
# 主图用 section_group 代理它们，以降低 HTML 卡顿并保留视觉上的关系桥。
HIDDEN_NODE_TYPES = {"section"}
SECTION_SUMMARY_LIMIT = 24

# 章节分组规则：按标题关键词把细章节投影到大章节。
# 这是“视觉层分组”，不是知识层合并；每个 section_group 仍保留原始 section_id 和行号。
SECTION_GROUP_PATTERNS = [
    ("pathogen", "病原/分类", ["病原", "分类", "教材章节", "英文", "pathogen", "etiology"]),
    ("transmission", "传播/流行", ["传播", "流行", "排毒", "宿主", "阶段", "transmission", "epidemiology"]),
    ("clinical", "临床/表现", ["临床", "症状", "表现", "综合征", "clinical", "sign"]),
    ("lesion", "剖检/病变", ["剖检", "病变", "病理", "lesion", "necropsy"]),
    ("diagnosis", "诊断/检测", ["诊断", "检测", "实验室", "样本", "diagnosis", "diagnostic"]),
    ("differential", "鉴别诊断", ["鉴别", "比较", "矩阵", "differential", "comparison"]),
    ("control", "防控/控制", ["防控", "控制", "预防", "生物安全", "消毒", "control", "prevention"]),
    ("drug_boundary", "用药/处置边界", ["用药", "处方", "治疗", "药物", "标签", "休药", "MRL", "残留", "drug", "treatment"]),
    ("regulatory", "监管/执行边界", ["监管", "执行", "检疫", "报告", "扑杀", "调运", "食品安全", "regulatory", "official"]),
    ("evidence", "来源/证据/可用性", ["来源", "证据", "可用性", "source", "evidence", "anchor", "citation"]),
]


TYPE_TO_WASH_TYPE = {
    "source": "source",
    "evidence_unit": "source",
    "literal_span": "entity",
    "section": "entity",
    "section_summary": "entity",
    "section_group": "entity",
    "fact": "entity",
    "rule_card": "topic",
    "rule": "topic",
    "disease": "topic",
    "drug": "topic",
    "comparison": "topic",
    "syndrome": "topic",
    "synthesis": "topic",
    "topic": "topic",
}

TYPE_LABELS = {
    "disease": "疾病",
    "drug": "药物",
    "source": "来源",
    "rule_card": "规则卡",
    "rule": "规则",
    "comparison": "鉴别矩阵",
    "syndrome": "综合征",
    "synthesis": "综合页",
    "topic": "主题",
    "section": "章节",
    "section_summary": "章节摘要",
    "section_group": "章节分组",
    "literal_span": "语义对象",
}

STATUS_LABELS = {
    "verified": "已验证",
    "candidate": "候选",
    "rejected": "拒绝",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"missing {label}: {path}")


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    payload = json.loads(read(path))
    return payload if isinstance(payload, dict) else {}


def node_content(node: dict[str, object], degree: int) -> str:
    """生成右侧详情抽屉中的 Markdown 内容。

    对 section_group 节点，会列出分组内原始章节和 line_start/line_end，
    保证视觉折叠后仍然可以追溯到具体章节位置。
    """
    node_type = str(node.get("type", "node") or "node")
    lines = [
        f"# {node.get('label') or node.get('id')}",
        "",
        f"- ID: `{node.get('id', '')}`",
        f"- 类型: {TYPE_LABELS.get(node_type, node_type)}",
        f"- 连接数: {degree}",
    ]
    for key, label in [
        ("path", "页面路径"),
        ("section_title", "章节标题"),
        ("section_count", "章节数"),
        ("predicate_context", "关系上下文"),
        ("source_evidence_unit_id", "来源证据单元"),
    ]:
        value = str(node.get(key, "") or "")
        if value:
            lines.append(f"- {label}: `{value}`")
    status = node.get("status")
    if isinstance(status, dict):
        usage_scope = status.get("usage_scope", [])
        if isinstance(usage_scope, list) and usage_scope:
            lines.append(f"- 使用范围: `{', '.join(str(item) for item in usage_scope)}`")
        for key, label in [
            ("source_trust", "来源可信度"),
            ("evidence_coverage", "证据覆盖度"),
        ]:
            value = str(status.get(key, "") or "")
            if value:
                lines.append(f"- {label}: `{value}`")
        legacy = status.get("legacy")
        if isinstance(legacy, dict):
            compact_legacy = {
                key: value
                for key, value in legacy.items()
                if value and key in {"legacy_source_note"}
            }
            if compact_legacy:
                lines.append(f"- 历史状态: `{compact_legacy}`")
    exact = str(node.get("exact_text_span", "") or "")
    if exact:
        lines.extend(["", "## Exact Text Span", "", exact])
    section_titles = node.get("section_titles")
    if isinstance(section_titles, list) and section_titles:
        heading = "## 分组内原始章节" if node_type == "section_group" else "## 折叠章节"
        lines.extend(["", heading, ""])
        for index, title in enumerate(section_titles, start=1):
            lines.append(f"{index}. {title}")
        omitted = int(node.get("section_omitted", 0) or 0)
        if omitted:
            lines.append(f"{len(section_titles) + 1}. ... 另有 {omitted} 个章节未在摘要中列出")
    section_refs = node.get("section_refs")
    if isinstance(section_refs, list) and section_refs:
        lines.extend(["", "## 原始定位", ""])
        for ref in section_refs[:SECTION_SUMMARY_LIMIT]:
            if not isinstance(ref, dict):
                continue
            lines.append(
                f"- `{ref.get('section_id', '')}` · {ref.get('title', '')} · line {ref.get('line_start', '')}-{ref.get('line_end', '')}"
            )
        if len(section_refs) > SECTION_SUMMARY_LIMIT:
            lines.append(f"- ... 另有 {len(section_refs) - SECTION_SUMMARY_LIMIT} 条原始章节定位")
    return "\n".join(lines) + "\n"


def edge_weight(edge: dict[str, object]) -> float:
    status = str(edge.get("status", "") or "")
    layer = str(edge.get("layer", "") or "")
    if status == "verified" and layer == "semantic":
        return 0.86
    if status == "verified":
        return 0.66
    if status == "candidate":
        return 0.38
    return 0.24


def edge_type(edge: dict[str, object]) -> str:
    status = str(edge.get("status", "") or "")
    if status == "verified":
        return "EXTRACTED"
    if status == "candidate":
        return "INFERRED"
    return "LOW_CONFIDENCE"


def compact_full_node(node: dict[str, object]) -> dict[str, object]:
    """为 full_index 压缩节点字段。

    主图默认不画所有节点，但搜索任意节点时仍要能查到它；
    full_index 保留搜索和关系展开所需的最小字段，避免把完整节点对象重复塞进 HTML。
    """
    node_type = str(node.get("type", "node") or "node")
    return {
        "id": str(node.get("id", "")),
        "label": str(node.get("label") or node.get("section_title") or node.get("id", "")),
        "type": node_type,
        "type_label": TYPE_LABELS.get(node_type, node_type),
        "path": str(node.get("path", "") or ""),
        "page_id": str(node.get("page_id", "") or ""),
        "section_title": str(node.get("section_title", "") or ""),
        "line_start": node.get("line_start", ""),
        "line_end": node.get("line_end", ""),
        "exact_text_span": str(node.get("exact_text_span", "") or ""),
        "source_evidence_unit_id": str(node.get("source_evidence_unit_id", "") or ""),
    }


def compact_full_edge(edge: dict[str, object]) -> dict[str, object]:
    """为 full_index 压缩边字段，保留追溯证据所需的关键字段。"""
    return {
        "id": str(edge.get("id", "")),
        "source": str(edge.get("source", "") or ""),
        "target": str(edge.get("target", "") or ""),
        "type": str(edge.get("type", "") or ""),
        "layer": str(edge.get("layer", "") or ""),
        "status": str(edge.get("status", "") or ""),
        "validation_status": str(edge.get("validation_status", "") or ""),
        "evidence_unit_id": str(edge.get("evidence_unit_id", "") or ""),
        "source_id": str(edge.get("source_id", "") or ""),
        "anchor": str(edge.get("anchor", "") or ""),
        "section_id": str(edge.get("section_id", "") or ""),
        "reason": str(edge.get("reason", "") or ""),
    }


def build_full_index(graph: dict[str, object], projection: dict[str, object]) -> dict[str, object]:
    """构建 HTML 内嵌的全量搜索索引。

    这个索引解决“默认主图折叠后搜索不到隐藏节点”的问题。
    搜索时不再只看画布可见节点，而是查 full_index.nodes 和 edges_by_node。
    """
    raw_nodes = graph.get("nodes", [])
    raw_edges = graph.get("edges", [])
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        return {"nodes": {}, "edges_by_node": {}, "projection_map": {}, "visible_node_ids": []}
    full_nodes = {
        str(node.get("id", "")): compact_full_node(node)
        for node in raw_nodes
        if isinstance(node, dict) and node.get("id")
    }
    edges_by_node: dict[str, list[dict[str, object]]] = {}
    for edge in raw_edges:
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("source", "") or "")
        target = str(edge.get("target", "") or "")
        if not source or not target:
            continue
        compact = compact_full_edge(edge)
        edges_by_node.setdefault(source, []).append(compact)
        edges_by_node.setdefault(target, []).append(compact)

    projection_map: dict[str, str] = {}
    for node in raw_nodes:
        if not isinstance(node, dict) or str(node.get("type", "")) != "section":
            continue
        section_id = str(node.get("id", ""))
        page_id = str(node.get("page_id", ""))
        group_id, _label = section_group_for_title(str(node.get("section_title", "")))
        projection_map[section_id] = f"section_group:{page_id}:{group_id}"

    visible_nodes = projection.get("visible_nodes", [])
    visible_node_ids = [
        str(node.get("id", ""))
        for node in visible_nodes
        if isinstance(node, dict) and node.get("id")
    ]
    return {
        "nodes": full_nodes,
        "edges_by_node": edges_by_node,
        "projection_map": projection_map,
        "visible_node_ids": visible_node_ids,
    }


def section_group_for_title(title: str) -> tuple[str, str]:
    """根据章节标题返回视觉分组 ID 和标签。"""
    lowered = title.lower()
    for group_id, label, patterns in SECTION_GROUP_PATTERNS:
        if any(pattern.lower() in lowered for pattern in patterns):
            return group_id, label
    return "other", "其他章节"


def build_change_log_payload(graph: dict[str, object], report: dict[str, object]) -> dict[str, object]:
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), dict) else {}
    readiness = graph.get("gold_dataset_readiness") if isinstance(graph.get("gold_dataset_readiness"), dict) else {}
    validation = graph.get("validation_summary") if isinstance(graph.get("validation_summary"), dict) else {}
    coverage = report.get("coverage") if isinstance(report.get("coverage"), dict) else {}
    semantic = report.get("semantic") if isinstance(report.get("semantic"), dict) else {}
    payload = {
        "generated_at": str(metadata.get("generated_at") or datetime.now(TZ).isoformat(timespec="seconds")),
        "title": "Wiki-Native 图谱构建日志",
        "subtitle": "统一图谱 · verified/candidate/rejected · 证据准入",
        "summary": {
            "nodes_after": len(graph.get("nodes", [])) if isinstance(graph.get("nodes"), list) else 0,
            "links_after": len(graph.get("edges", [])) if isinstance(graph.get("edges"), list) else 0,
            "facts_in_graph": coverage.get("evidence_unit_count", len(graph.get("evidence_units", [])) if isinstance(graph.get("evidence_units"), list) else 0),
            "verified_semantic_edges": readiness.get("verified_semantic_edges", 0),
            "candidate_semantic_edges": readiness.get("candidate_semantic_edges", 0),
            "audit_blockers": validation.get("audit_blockers", 0),
            "audit_warnings": validation.get("audit_warnings", 0),
        },
        "crud_counts": {},
        "added_nodes": [],
        "added_links": [],
        "removed_nodes": [],
        "changed_nodes": [],
        "recent_crud_events": [],
        "reasonableness": (
            "该可视化来自 wiki-native unified graph。语义边只有在 evidence_unit、source_id、anchor、"
            "evidence_text、supporting_span 和 evidence_support_check 均通过时才可作为 verified 事实边。"
        ),
        "semantic_by_predicate": semantic.get("semantic_by_predicate", {}),
        "candidate_reasons": semantic.get("candidate_reasons", {}),
        "evidence_files": {
            "graph_json": "wiki/wiki-native-graph.json",
            "build_report_json": "issues/wiki_native_graph_build_report.json",
            "build_report_md": "issues/wiki_native_graph_build_report.md",
            "native_diff_json": "issues/wiki_native_graph_change_diff_last.json",
            "legacy_graph_json": "wiki/graph-data.json",
        },
    }
    diff = load_json(NATIVE_DIFF_JSON)
    if diff:
        payload["generated_at"] = str(diff.get("generated_at") or payload["generated_at"])
        payload["summary"].update(diff.get("summary", {}))
        payload["crud_counts"] = diff.get("crud_counts", {})
        payload["added_nodes"] = diff.get("added_nodes", [])
        payload["added_links"] = diff.get("added_links", [])
        payload["removed_nodes"] = diff.get("removed_nodes", [])
        payload["changed_nodes"] = diff.get("changed_nodes", [])
        payload["recent_crud_events"] = diff.get("recent_crud_events", [])
        if diff.get("reasonableness"):
            payload["reasonableness"] = str(diff["reasonableness"])
    return payload


def project_visual_graph(graph: dict[str, object], include_sections: bool = False) -> dict[str, object]:
    """把完整图谱投影成 HTML 视图。

    include_sections=False: 主图，隐藏原始 section，生成 section_group 和视觉支撑边。
    include_sections=True: 审计图，保留全部原始 section 和 HAS_SECTION 边。
    """
    raw_nodes = graph.get("nodes", [])
    raw_edges = graph.get("edges", [])
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        raise ValueError("wiki-native-graph.json must contain nodes and edges arrays")

    if include_sections:
        return {
            "visible_nodes": [node for node in raw_nodes if isinstance(node, dict) and node.get("id")],
            "visible_edges": [edge for edge in raw_edges if isinstance(edge, dict)],
            "hidden_counts": {
                "hidden_node_types": {},
                "hidden_node_total": 0,
                "hidden_edge_total": 0,
                "summary_node_total": 0,
            },
        }

    page_nodes = {
        str(node.get("id", "")): node
        for node in raw_nodes
        if isinstance(node, dict) and node.get("id") and str(node.get("type", "")) != "section"
    }
    section_groups: dict[str, list[dict[str, object]]] = {}
    for node in raw_nodes:
        if not isinstance(node, dict) or str(node.get("type", "")) != "section":
            continue
        page_id = str(node.get("page_id", ""))
        if not page_id:
            continue
        section_groups.setdefault(page_id, []).append(node)
    for items in section_groups.values():
        items.sort(key=lambda item: (int(item.get("level", 0) or 0), int(item.get("line_start", 0) or 0), str(item.get("section_title", ""))))

    summary_page_types = {"disease", "drug", "comparison", "syndrome", "synthesis", "rule_card", "topic"}
    group_nodes: list[dict[str, object]] = []
    group_edges: list[dict[str, object]] = []
    section_to_group: dict[str, str] = {}
    for page_id, sections in section_groups.items():
        page_node = page_nodes.get(page_id)
        if not page_node or str(page_node.get("type", "")) not in summary_page_types:
            continue
        grouped: dict[str, dict[str, object]] = {}
        for section in sections:
            # 这里不是删除或合并知识层 section，而是为视觉层建立分组代理。
            title = str(section.get("section_title", ""))
            group_id, group_label = section_group_for_title(title)
            group = grouped.setdefault(
                group_id,
                {
                    "label": group_label,
                    "sections": [],
                },
            )
            group["sections"].append(section)
        for group_id, payload in grouped.items():
            group_sections = payload["sections"] if isinstance(payload.get("sections"), list) else []
            group_label = str(payload.get("label", group_id))
            titles = [str(section.get("section_title", "")) for section in group_sections[:SECTION_SUMMARY_LIMIT] if str(section.get("section_title", ""))]
            section_refs = [
                {
                    "section_id": str(section.get("id", "")),
                    "title": str(section.get("section_title", "")),
                    "line_start": section.get("line_start", ""),
                    "line_end": section.get("line_end", ""),
                }
                for section in group_sections
            ]
            summary_id = f"section_group:{page_id}:{group_id}"
            for ref in section_refs:
                if ref["section_id"]:
                    section_to_group[ref["section_id"]] = summary_id
            group_nodes.append(
                {
                    "id": summary_id,
                    "type": "section_group",
                    "label": f"{group_label} · {str(page_node.get('label', page_id))}",
                    "path": str(page_node.get("path", "")),
                    "section_group_id": group_id,
                    "section_group_label": group_label,
                    "section_count": len(group_sections),
                    "section_titles": titles,
                    "section_refs": section_refs,
                    "section_omitted": max(0, len(group_sections) - len(titles)),
                    "page_id": page_id,
                    "placeholder": True,
                    "summary_of_sections": True,
                }
            )
            group_edges.append(
                {
                    "id": f"edge-section-group:{page_id}:{group_id}",
                    "source": page_id,
                    "target": summary_id,
                    "type": "HAS_SECTION_GROUP",
                    "layer": "structural",
                    "status": "verified",
                    "validation_status": "accepted",
                    "blocked_from_runtime": False,
                    "gold_dataset_ready": False,
                }
            )

    visible_nodes = [
        node
        for node in raw_nodes
        if isinstance(node, dict) and node.get("id") and str(node.get("type", "") or "") not in HIDDEN_NODE_TYPES
    ]
    visible_nodes.extend(group_nodes)
    visible_node_ids = {str(node["id"]) for node in visible_nodes}
    visible_edges = [
        edge
        for edge in raw_edges
        if isinstance(edge, dict)
        and str(edge.get("source", "") or "") in visible_node_ids
        and str(edge.get("target", "") or "") in visible_node_ids
        and str(edge.get("type", "") or "") != "HAS_SECTION"
    ]
    visible_edges.extend(group_edges)
    existing_visual_edge_ids = {str(edge.get("id", "")) for edge in visible_edges if isinstance(edge, dict)}
    for edge in raw_edges:
        # 语义边原本是 page -> semantic_object。
        # 为了让视觉上看到“章节分组参与了这条关系”，额外添加：
        # section_group -> semantic_object 的投影边。
        if not isinstance(edge, dict) or str(edge.get("layer", "")) != "semantic":
            continue
        group_id = section_to_group.get(str(edge.get("section_id", "")))
        target = str(edge.get("target", ""))
        if not group_id or target not in visible_node_ids:
            continue
        visual_edge_id = f"edge-section-group-semantic:{group_id}:{target}"
        if visual_edge_id in existing_visual_edge_ids:
            continue
        existing_visual_edge_ids.add(visual_edge_id)
        visible_edges.append(
            {
                "id": visual_edge_id,
                "source": group_id,
                "target": target,
                "type": "SECTION_GROUP_SUPPORTS_SEMANTIC_OBJECT",
                "layer": "visual_projection",
                "status": str(edge.get("status", "candidate")),
                "validation_status": str(edge.get("validation_status", "")),
                "evidence_unit_id": str(edge.get("evidence_unit_id", "")),
                "source_id": str(edge.get("source_id", "")),
                "anchor": str(edge.get("anchor", "")),
                "reason": str(edge.get("reason", "")),
                "section_id": str(edge.get("section_id", "")),
                "blocked_from_runtime": edge.get("blocked_from_runtime", True),
                "gold_dataset_ready": edge.get("gold_dataset_ready", False),
            }
        )
    return {
        "visible_nodes": visible_nodes,
        "visible_edges": visible_edges,
        "hidden_counts": {
            "hidden_node_types": {node_type: sum(1 for node in raw_nodes if isinstance(node, dict) and str(node.get("type", "") or "") == node_type) for node_type in sorted(HIDDEN_NODE_TYPES)},
            "hidden_node_total": sum(1 for node in raw_nodes if isinstance(node, dict) and str(node.get("type", "") or "") in HIDDEN_NODE_TYPES),
            "hidden_edge_total": sum(1 for edge in raw_edges if isinstance(edge, dict) and str(edge.get("type", "") or "") == "HAS_SECTION"),
            "summary_node_total": len(group_nodes),
        },
    }


def build_wash_payload(graph: dict[str, object], report: dict[str, object], *, include_sections: bool = False) -> dict[str, object]:
    """把 wiki-native 图谱转换为 wash HTML 模板需要的 payload。"""
    projection = project_visual_graph(graph, include_sections=include_sections)
    raw_nodes = projection["visible_nodes"]
    raw_edges = projection["visible_edges"]

    node_ids = {str(node.get("id", "")) for node in raw_nodes if isinstance(node, dict)}
    degree: dict[str, int] = {}
    for edge in raw_edges:
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("source", "") or "")
        target = str(edge.get("target", "") or "")
        if source in node_ids and target in node_ids:
            degree[source] = degree.get(source, 0) + 1
            degree[target] = degree.get(target, 0) + 1

    ranked = sorted(
        [node for node in raw_nodes if isinstance(node, dict) and node.get("id")],
        key=lambda item: (degree.get(str(item.get("id", "")), 0), str(item.get("type", "")) in {"disease", "drug", "comparison"}),
        reverse=True,
    )
    initial_view = [str(node["id"]) for node in ranked[:72]]

    wash_nodes = []
    for index, node in enumerate(raw_nodes):
        if not isinstance(node, dict) or not node.get("id"):
            continue
        node_id = str(node["id"])
        node_type = str(node.get("type", "node") or "node")
        angle = index * 2.399963229728653
        radius = 11 + math.sqrt(index + 1) * 4.2
        x = max(5, min(95, 50 + math.cos(angle) * radius))
        y = max(5, min(95, 50 + math.sin(angle) * radius * 0.72))
        status = node.get("status") if isinstance(node.get("status"), dict) else {}
        summary_tail = ""
        if isinstance(status, dict):
            usage_scope = status.get("usage_scope", [])
            if isinstance(usage_scope, list):
                summary_tail = ", ".join(str(item) for item in usage_scope if str(item))
            else:
                summary_tail = str(usage_scope or status.get("evidence_coverage") or status.get("source_trust") or "")
        if node_type in {"section_summary", "section_group"}:
            titles = node.get("section_titles") if isinstance(node.get("section_titles"), list) else []
            section_count = int(node.get("section_count", 0) or 0)
            summary_tail = f"{section_count} 个章节" if section_count else "章节摘要"
        wash_nodes.append(
            {
                "id": node_id,
                "label": str(node.get("label") or node_id),
                "type": TYPE_TO_WASH_TYPE.get(node_type, "entity"),
                "community": node_type,
                "summary": f"{TYPE_LABELS.get(node_type, node_type)} · {summary_tail or 'wiki-native'}",
                "content": node_content(node, degree.get(node_id, 0)),
                "source_path": str(node.get("path", "") or ""),
                "confidence": "EXTRACTED" if not node.get("placeholder") else "INFERRED",
                "weight": min(100, 30 + degree.get(node_id, 0) * 4),
                "x": round(x, 2),
                "y": round(y, 2),
            }
        )

    wash_edges = []
    for index, edge in enumerate(raw_edges):
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("source", "") or "")
        target = str(edge.get("target", "") or "")
        if source not in node_ids or target not in node_ids:
            continue
        status = str(edge.get("status", "") or "")
        label = str(edge.get("type", "EDGE") or "EDGE")
        wash_edges.append(
            {
                "id": str(edge.get("id") or f"edge-{index}"),
                "from": source,
                "to": target,
                "source": source,
                "target": target,
                "type": edge_type(edge),
                "label": f"{label} · {STATUS_LABELS.get(status, status)}" if status else label,
                "weight": edge_weight(edge),
                "signals": {
                    "wiki_native_type": label,
                    "layer": str(edge.get("layer", "")),
                    "status": status,
                    "validation_status": str(edge.get("validation_status", "")),
                    "evidence_unit_id": str(edge.get("evidence_unit_id", "")),
                    "source_id": str(edge.get("source_id", "")),
                    "anchor": str(edge.get("anchor", "")),
                    "reason": str(edge.get("reason", "")),
                },
                "source_signal_available": bool(edge.get("evidence_unit_id") or edge.get("source_id")),
            }
        )

    communities = []
    for idx, community in enumerate(sorted({node["community"] for node in wash_nodes})):
        group_nodes = [node for node in wash_nodes if node["community"] == community]
        if not group_nodes:
            continue
        best = max(group_nodes, key=lambda item: degree.get(str(item["id"]), 0))
        communities.append(
            {
                "id": community,
                "label": TYPE_LABELS.get(community, community),
                "node_count": len(group_nodes),
                "source_count": sum(1 for node in group_nodes if node["type"] == "source"),
                "is_primary": idx == 0,
                "recommended_start_node_id": best["id"],
            }
        )

    generated_at = str(graph.get("metadata", {}).get("generated_at") or datetime.now(TZ).isoformat(timespec="seconds"))
    status_counts = Counter(str(edge.get("status", "") or "") for edge in raw_edges if isinstance(edge, dict))
    mode_label = "章节审计视图" if include_sections else "主干摘要视图"
    payload = {
        "meta": {
            "build_date": generated_at,
            "wiki_title": f"猪病 LLM Wiki · Wiki-Native Knowledge Graph · {mode_label}",
            "total_nodes": len(wash_nodes),
            "total_edges": len(wash_edges),
            "full_nodes": len(graph.get("nodes", [])) if isinstance(graph.get("nodes"), list) else 0,
            "full_edges": len(graph.get("edges", [])) if isinstance(graph.get("edges"), list) else 0,
            "hidden_nodes": projection["hidden_counts"]["hidden_node_total"],
            "hidden_edges": projection["hidden_counts"]["hidden_edge_total"],
            "visual_mode": "audit_full_sections" if include_sections else "main_section_summary",
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
            "summary": (
                "由 wiki/wiki-native-graph.json 适配为 wash 图谱格式；"
                f"当前为{mode_label}。"
                f"隐藏节点数 {projection['hidden_counts']['hidden_node_total']}、隐藏边数 {projection['hidden_counts']['hidden_edge_total']}、"
                f"章节摘要节点数 {projection['hidden_counts'].get('summary_node_total', 0)}。"
                f"边状态统计：{dict(status_counts)}。verified 语义边可用于黄金数据集正例，candidate/rejected 仅用于复核和反幻觉训练。"
            ),
        },
        "change_log": build_change_log_payload(graph, report),
    }
    if not include_sections:
        # 主图需要 full_index 才能在搜索时展开隐藏节点和隐藏边。
        # 审计图本身已经全量展示，不需要再嵌入一份 full_index。
        payload["full_index"] = build_full_index(graph, projection)
    return payload


def full_index_enhancement_script() -> str:
    """返回注入到主图 HTML 的交互增强脚本。

    该脚本不修改共享 wash 模板，而是在当前 HTML 中额外提供：
    1. 搜索 full_index，而不是只搜索可见节点。
    2. 底部“全量关系展开”面板。
    3. 画布局部聚焦视图，临时屏蔽其他节点和边。
    4. 节点拖拽，并在拖动时重绘关联边。
    """
    return r'''
<style>
  body.full-index-focus-active .node,
  body.full-index-focus-active .edge {
    opacity: .08 !important;
    pointer-events: none;
  }
  .full-index-overlay-node {
    position: absolute;
    z-index: 38;
    width: 172px;
    min-height: 64px;
    transform: translate(-50%, -50%);
    border: 1px solid rgba(139, 46, 36, .42);
    background: rgba(255, 253, 247, .98);
    box-shadow: 0 12px 28px rgba(36, 31, 26, .18);
    border-radius: 8px;
    padding: 8px 9px;
    color: var(--ink, #241f1a);
    text-align: left;
    font-family: var(--font-ui, sans-serif);
    cursor: grab;
    user-select: none;
  }
  .full-index-overlay-node.is-dragging,
  .node.is-dragging {
    cursor: grabbing !important;
    z-index: 90 !important;
  }
  .node {
    touch-action: none;
  }
  .node[data-drag-enabled="1"] {
    cursor: grab;
  }
  .full-index-overlay-node[data-focus="1"] {
    border-color: rgba(139, 46, 36, .92);
    background: #fff8ec;
    box-shadow: 0 18px 38px rgba(139, 46, 36, .22);
  }
  .full-index-overlay-node small {
    display: block;
    color: var(--muted, #6f6559);
    font-size: 10px;
    margin-bottom: 3px;
  }
  .full-index-overlay-node strong {
    display: block;
    font-size: 12px;
    line-height: 1.25;
    max-height: 32px;
    overflow: hidden;
  }
  .full-index-overlay-node code {
    display: block;
    margin-top: 5px;
    font-size: 10px;
    color: var(--cinnabar, #8b2e24);
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .full-index-overlay-edge {
    opacity: .78;
    stroke: #8b2e24;
    stroke-linecap: round;
    fill: none;
    pointer-events: none;
  }
  .full-index-overlay-edge[data-status="candidate"] {
    stroke: #b7791f;
    stroke-dasharray: 7 5;
  }
  .full-index-overlay-edge[data-status="rejected"] {
    stroke: #8b8b8b;
    stroke-dasharray: 3 5;
  }
  .full-index-panel {
    position: fixed;
    left: 24px;
    right: 24px;
    bottom: 24px;
    z-index: 80;
    max-height: 38vh;
    overflow: auto;
    border: 1px solid rgba(104, 88, 66, .26);
    background: rgba(255, 253, 247, .96);
    box-shadow: 0 18px 36px rgba(36, 31, 26, .16);
    border-radius: 10px;
    padding: 14px 16px;
    font-family: var(--font-ui, sans-serif);
    color: var(--ink, #241f1a);
  }
  .full-index-panel[hidden] { display: none; }
  .full-index-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 10px;
  }
  .full-index-head strong { display: block; font-size: 15px; }
  .full-index-head span { display: block; color: var(--muted, #6f6559); font-size: 12px; margin-top: 2px; }
  .full-index-close {
    border: 1px solid var(--rule, #d8cdbb);
    background: var(--surface-2, #f8f1e4);
    color: var(--ink, #241f1a);
    border-radius: 6px;
    padding: 5px 9px;
    cursor: pointer;
  }
  .full-index-grid {
    display: grid;
    grid-template-columns: minmax(220px, .75fr) minmax(280px, 1fr) minmax(320px, 1.35fr);
    gap: 12px;
  }
  .full-index-card {
    border: 1px solid rgba(216, 205, 187, .9);
    background: rgba(248, 241, 228, .72);
    border-radius: 8px;
    padding: 10px;
  }
  .full-index-card h3 {
    margin: 0 0 8px;
    font-size: 13px;
    color: var(--cinnabar, #8b2e24);
  }
  .full-index-card ul { margin: 0; padding-left: 18px; }
  .full-index-card li { margin: 5px 0; font-size: 12px; line-height: 1.45; }
  .full-index-card code { font-family: var(--font-mono, monospace); font-size: 11px; }
  @media (max-width: 960px) {
    .full-index-panel { left: 10px; right: 10px; bottom: 10px; max-height: 50vh; }
    .full-index-grid { grid-template-columns: 1fr; }
  }
</style>
<script>
(function () {
  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }
  function escapeHtml(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch];
    });
  }
  function normalize(value) {
    return String(value || "").trim().toLowerCase();
  }
  function labelOf(index, id) {
    const node = index.nodes && index.nodes[id];
    return node ? (node.label || id) : id;
  }
  function nodeMeta(node) {
    if (!node) return "";
    const parts = [];
    if (node.type_label) parts.push(node.type_label);
    if (node.path) parts.push(node.path);
    if (node.line_start || node.line_end) parts.push("line " + (node.line_start || "") + "-" + (node.line_end || ""));
    return parts.join(" · ");
  }
  function clearFocusOverlay() {
    document.body.classList.remove("full-index-focus-active");
    document.querySelectorAll(".full-index-overlay-node").forEach((item) => item.remove());
    const svg = document.querySelector(".graph-svg");
    if (svg) svg.querySelectorAll(".full-index-overlay-edge").forEach((item) => item.remove());
  }
  function parsePercent(value, fallback) {
    const n = parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  function elementPoint(el) {
    return {
      x: parsePercent(el.style.left, 50),
      y: parsePercent(el.style.top, 50)
    };
  }
  function overlayPath(p1, p2) {
    const x1 = p1.x * 10;
    const y1 = p1.y * 6.8;
    const x2 = p2.x * 10;
    const y2 = p2.y * 6.8;
    const mx = (x1 + x2) / 2;
    const my = (y1 + y2) / 2 - 18;
    return `M${x1.toFixed(1)},${y1.toFixed(1)} Q${mx.toFixed(1)},${my.toFixed(1)} ${x2.toFixed(1)},${y2.toFixed(1)}`;
  }
  function updateMainGraphEdgesForNode(id) {
    // 主图节点被拖动后，重算与该节点相连的 SVG path，避免边停留在旧位置。
    const atlas = document.getElementById("atlas");
    if (!atlas) return;
    const sourceEl = atlas.querySelector('.node[data-id="' + CSS.escape(id) + '"]');
    if (!sourceEl) return;
    document.querySelectorAll('.edge[data-from="' + CSS.escape(id) + '"], .edge[data-to="' + CSS.escape(id) + '"]').forEach((edgeEl) => {
      const from = edgeEl.getAttribute("data-from");
      const to = edgeEl.getAttribute("data-to");
      const fromEl = atlas.querySelector('.node[data-id="' + CSS.escape(from) + '"]');
      const toEl = atlas.querySelector('.node[data-id="' + CSS.escape(to) + '"]');
      if (!fromEl || !toEl) return;
      edgeEl.setAttribute("d", overlayPath(elementPoint(fromEl), elementPoint(toEl)));
    });
  }
  function updateOverlayEdgesForNode(id) {
    // 搜索聚焦视图中的临时节点被拖动后，重算临时关系边。
    const atlas = document.getElementById("atlas");
    if (!atlas) return;
    document.querySelectorAll('.full-index-overlay-edge[data-from="' + CSS.escape(id) + '"], .full-index-overlay-edge[data-to="' + CSS.escape(id) + '"]').forEach((edgeEl) => {
      const from = edgeEl.getAttribute("data-from");
      const to = edgeEl.getAttribute("data-to");
      const fromEl = atlas.querySelector('.full-index-overlay-node[data-id="' + CSS.escape(from) + '"]');
      const toEl = atlas.querySelector('.full-index-overlay-node[data-id="' + CSS.escape(to) + '"]');
      if (!fromEl || !toEl) return;
      edgeEl.setAttribute("d", overlayPath(elementPoint(fromEl), elementPoint(toEl)));
    });
  }
  function makeNodeDraggable(el, options) {
    // 为普通主图节点和搜索聚焦节点统一绑定拖拽。
    // 拖动只影响当前 HTML 会话，不写回图谱 JSON。
    if (!el || el.dataset.dragEnabled === "1") return;
    el.dataset.dragEnabled = "1";
    el.addEventListener("pointerdown", function (event) {
      if (event.button !== 0) return;
      event.stopPropagation();
      const atlas = document.getElementById("atlas");
      if (!atlas) return;
      const rect = atlas.getBoundingClientRect();
      const startLeft = parsePercent(el.style.left, 50);
      const startTop = parsePercent(el.style.top, 50);
      const startX = event.clientX;
      const startY = event.clientY;
      const nodeId = el.dataset.id;
      el.classList.add("is-dragging");
      if (el.setPointerCapture) el.setPointerCapture(event.pointerId);
      function move(moveEvent) {
        const dx = (moveEvent.clientX - startX) / Math.max(1, rect.width) * 100;
        const dy = (moveEvent.clientY - startY) / Math.max(1, rect.height) * 100;
        const nextLeft = Math.max(3, Math.min(97, startLeft + dx));
        const nextTop = Math.max(3, Math.min(97, startTop + dy));
        el.style.left = nextLeft + "%";
        el.style.top = nextTop + "%";
        if (options && options.overlay) updateOverlayEdgesForNode(nodeId);
        else updateMainGraphEdgesForNode(nodeId);
      }
      function up(upEvent) {
        el.classList.remove("is-dragging");
        if (el.releasePointerCapture) {
          try { el.releasePointerCapture(upEvent.pointerId); } catch (_err) {}
        }
        window.removeEventListener("pointermove", move, true);
        window.removeEventListener("pointerup", up, true);
        window.removeEventListener("pointercancel", up, true);
      }
      window.addEventListener("pointermove", move, true);
      window.addEventListener("pointerup", up, true);
      window.addEventListener("pointercancel", up, true);
      event.preventDefault();
    });
  }
  function enableMainNodeDragging() {
    document.querySelectorAll(".node").forEach((nodeEl) => makeNodeDraggable(nodeEl, { overlay: false }));
  }
  function pointFor(index, id, order, total) {
    const visible = document.querySelector('.node[data-id="' + CSS.escape(id) + '"]');
    if (visible) {
      return {
        x: parseFloat(visible.style.left || "50"),
        y: parseFloat(visible.style.top || "50")
      };
    }
    const projection = index.projection_map && index.projection_map[id];
    if (projection) {
      const projected = document.querySelector('.node[data-id="' + CSS.escape(projection) + '"]');
      if (projected) {
        const baseX = parseFloat(projected.style.left || "50");
        const baseY = parseFloat(projected.style.top || "50");
        const angle = order * 2.399963229728653;
        return {
          x: Math.max(7, Math.min(93, baseX + Math.cos(angle) * 10)),
          y: Math.max(7, Math.min(93, baseY + Math.sin(angle) * 7))
        };
      }
    }
    const angle = order * 2 * Math.PI / Math.max(total, 1);
    const radius = id && index.nodes[id] && index.nodes[id].type === "section" ? 25 : 31;
    return {
      x: Math.max(7, Math.min(93, 50 + Math.cos(angle) * radius)),
      y: Math.max(7, Math.min(93, 50 + Math.sin(angle) * radius * .72))
    };
  }
  function drawFocusOverlay(index, nodeId, neighbors, edges) {
    // 搜索命中后，把命中节点、一阶邻居和对应边画到覆盖层。
    // 同时弱化原主图，使用户只关注当前节点的全量一阶关系。
    clearFocusOverlay();
    const atlas = document.getElementById("atlas");
    const svg = document.querySelector(".graph-svg");
    if (!atlas || !svg || !nodeId) return;
    document.body.classList.add("full-index-focus-active");
    const nodeOrder = [nodeId].concat(neighbors.map((item) => item.id));
    const unique = [];
    const seen = new Set();
    nodeOrder.forEach((id) => {
      if (!id || seen.has(id) || !index.nodes[id]) return;
      seen.add(id);
      unique.push(id);
    });
    const points = {};
    unique.forEach((id, order) => {
      points[id] = id === nodeId ? { x: 50, y: 50 } : pointFor(index, id, order, unique.length);
    });
    edges.forEach((edge) => {
      const p1 = points[edge.source];
      const p2 = points[edge.target];
      if (!p1 || !p2) return;
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      const x1 = p1.x * 10;
      const y1 = p1.y * 6.8;
      const x2 = p2.x * 10;
      const y2 = p2.y * 6.8;
      const mx = (x1 + x2) / 2;
      const my = (y1 + y2) / 2 - 18;
      path.setAttribute("d", `M${x1.toFixed(1)},${y1.toFixed(1)} Q${mx.toFixed(1)},${my.toFixed(1)} ${x2.toFixed(1)},${y2.toFixed(1)}`);
      path.setAttribute("class", "full-index-overlay-edge");
      path.setAttribute("data-status", edge.status || "");
      path.setAttribute("data-from", edge.source);
      path.setAttribute("data-to", edge.target);
      path.setAttribute("stroke-width", edge.status === "verified" ? "2.8" : "2");
      svg.appendChild(path);
    });
    unique.forEach((id) => {
      const node = index.nodes[id];
      const p = points[id];
      const el = document.createElement("button");
      el.type = "button";
      el.className = "full-index-overlay-node";
      el.dataset.id = id;
      el.dataset.focus = id === nodeId ? "1" : "0";
      el.style.left = p.x + "%";
      el.style.top = p.y + "%";
      el.title = id;
      el.innerHTML = `<small>${escapeHtml(node.type_label || node.type || "node")}</small><strong>${escapeHtml(node.label || id)}</strong><code>${escapeHtml(id)}</code>`;
      atlas.appendChild(el);
      makeNodeDraggable(el, { overlay: true });
    });
  }
  function findBestMatch(index, query) {
    const q = normalize(query);
    if (!q || !index.nodes) return null;
    if (index.nodes[query]) return query;
    let contains = null;
    for (const id of Object.keys(index.nodes)) {
      const node = index.nodes[id];
      const hay = normalize([id, node.label, node.type, node.path, node.section_title, node.exact_text_span].join(" "));
      if (normalize(id) === q || normalize(node.label) === q) return id;
      if (!contains && hay.includes(q)) contains = id;
    }
    return contains;
  }
  function renderPanel(index, nodeId, query) {
    // 底部审计面板：列出命中节点、相关节点、对应关系边和隐藏章节的投影位置。
    let panel = document.getElementById("full-index-panel");
    if (!panel) {
      panel = document.createElement("aside");
      panel.id = "full-index-panel";
      panel.className = "full-index-panel";
      panel.hidden = true;
      document.body.appendChild(panel);
    }
    if (!nodeId) {
      panel.hidden = true;
      return;
    }
    const node = index.nodes[nodeId];
    const edges = (index.edges_by_node && index.edges_by_node[nodeId]) || [];
    const projection = index.projection_map && index.projection_map[nodeId];
    const neighbors = [];
    const seen = new Set();
    edges.forEach((edge) => {
      const other = edge.source === nodeId ? edge.target : edge.source;
      if (!other || seen.has(other)) return;
      seen.add(other);
      neighbors.push({ id: other, node: index.nodes[other], via: edge });
    });
    const visibleSet = new Set(index.visible_node_ids || []);
    const hiddenCount = neighbors.filter((item) => !visibleSet.has(item.id)).length;
    const edgeItems = edges.slice(0, 80).map((edge) => {
      return `<li><code>${escapeHtml(edge.type)}</code> · <code>${escapeHtml(edge.source)}</code> -> <code>${escapeHtml(edge.target)}</code>${edge.status ? " · " + escapeHtml(edge.status) : ""}${edge.evidence_unit_id ? " · evidence " + escapeHtml(edge.evidence_unit_id) : ""}${edge.anchor ? "<br><span>" + escapeHtml(edge.anchor) + "</span>" : ""}</li>`;
    }).join("");
    const neighborItems = neighbors.slice(0, 80).map((item) => {
      return `<li><strong>${escapeHtml(labelOf(index, item.id))}</strong><br><code>${escapeHtml(item.id)}</code><br><span>${escapeHtml(nodeMeta(item.node))}</span></li>`;
    }).join("");
    panel.innerHTML = `
      <div class="full-index-head">
        <div>
          <strong>全量关系展开：${escapeHtml(node ? node.label || nodeId : nodeId)}</strong>
          <span>搜索词：${escapeHtml(query)} · 一阶邻居 ${neighbors.length} 个，其中默认视图隐藏 ${hiddenCount} 个 · 关系边 ${edges.length} 条</span>
        </div>
        <button class="full-index-close" type="button">收起</button>
      </div>
      <div class="full-index-grid">
        <section class="full-index-card">
          <h3>命中节点</h3>
          <ul>
            <li><code>${escapeHtml(nodeId)}</code></li>
            <li>${escapeHtml(nodeMeta(node)) || "无额外元数据"}</li>
            ${projection ? `<li>主图投影：<code>${escapeHtml(projection)}</code><br>${escapeHtml(labelOf(index, projection))}</li>` : ""}
          </ul>
        </section>
        <section class="full-index-card">
          <h3>相关节点</h3>
          <ul>${neighborItems || "<li>未找到一阶邻居</li>"}</ul>
        </section>
        <section class="full-index-card">
          <h3>对应关系边</h3>
          <ul>${edgeItems || "<li>未找到关系边</li>"}</ul>
        </section>
      </div>`;
    panel.querySelector(".full-index-close").addEventListener("click", () => { panel.hidden = true; });
    panel.hidden = false;
    drawFocusOverlay(index, nodeId, neighbors, edges.slice(0, 120));
  }
  ready(function () {
    const dataEl = document.getElementById("graph-data");
    const input = document.getElementById("search");
    if (!dataEl || !input) return;
    enableMainNodeDragging();
    const observer = new MutationObserver(() => enableMainNodeDragging());
    const atlas = document.getElementById("atlas");
    if (atlas) observer.observe(atlas, { childList: true, subtree: true });
    let graph;
    try { graph = JSON.parse(dataEl.textContent || "{}"); } catch (_err) { return; }
    const index = graph.full_index;
    if (!index || !index.nodes || !index.edges_by_node) return;
    function runSearch() {
      const query = input.value.trim();
      if (!query) {
        renderPanel(index, null, query);
        clearFocusOverlay();
        return;
      }
      const nodeId = findBestMatch(index, query);
      renderPanel(index, nodeId, query);
    }
    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        window.setTimeout(runSearch, 0);
      }
    });
    let timer = null;
    input.addEventListener("input", function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(runSearch, 450);
    });
    const fitButton = document.getElementById("fit-view");
    if (fitButton) fitButton.addEventListener("click", clearFocusOverlay);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        renderPanel(index, null, "");
        clearFocusOverlay();
      }
    });
  });
})();
</script>
'''


def render_html(payload: dict[str, object], output_path: Path) -> None:
    """渲染 HTML，并复制 wash 模板依赖的静态资源。"""
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
    if payload.get("full_index"):
        html_text = html_text.replace("</body>", full_index_enhancement_script() + "\n</body>")
    write(output_path, html_text)

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
    """同时生成主图和完整章节审计图。"""
    require(GRAPH_JSON, "wiki-native graph data")
    graph = load_json(GRAPH_JSON)
    report = load_json(REPORT_JSON)
    payload = build_wash_payload(graph, report, include_sections=False)
    render_html(payload, GRAPH_HTML)
    audit_payload = build_wash_payload(graph, report, include_sections=True)
    render_html(audit_payload, GRAPH_AUDIT_HTML)
    print(
        json.dumps(
            {
                "html": GRAPH_HTML.relative_to(ROOT).as_posix(),
                "audit_html": GRAPH_AUDIT_HTML.relative_to(ROOT).as_posix(),
                "nodes": payload["meta"]["total_nodes"],
                "edges": payload["meta"]["total_edges"],
                "audit_nodes": audit_payload["meta"]["total_nodes"],
                "audit_edges": audit_payload["meta"]["total_edges"],
                "style": "llm-wiki-skill wash",
                "source": GRAPH_JSON.relative_to(ROOT).as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
