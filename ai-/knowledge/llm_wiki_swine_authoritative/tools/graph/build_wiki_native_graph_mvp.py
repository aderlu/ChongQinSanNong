from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
CONFIG = ROOT / "config"
ISSUES = ROOT / "issues"   
REGISTRY_PATH = CONFIG / "wiki_native_predicate_registry.json"
GRAPH_PATH = WIKI / "wiki-native-graph.json"
REPORT_JSON = ISSUES / "wiki_native_graph_build_report.json"
REPORT_MD = ISSUES / "wiki_native_graph_build_report.md"
NATIVE_DIFF_JSON = ISSUES / "wiki_native_graph_change_diff_last.json"
NATIVE_DIFF_MD = ISSUES / "wiki_native_graph_change_diff_last.md"
NATIVE_SNAPSHOT_DIR = ISSUES / "graph_snapshots"
LATEST_NATIVE_SNAPSHOT = NATIVE_SNAPSHOT_DIR / "latest_wiki_native_graph_snapshot.json"
TZ = timezone(timedelta(hours=8))

PAGE_DIR_TYPES = {
    "diseases": "disease",
    "drugs": "drug",
    "comparisons": "comparison",
    "syndromes": "syndrome",
    "rule_cards": "rule_card",
    "rules": "rule",
    "synthesis": "synthesis",
    "sources": "source",
    "topics": "topic",
}

ID_FIELDS = {
    "disease": "disease_id",
    "drug": "drug_id",
    "rule_card": "card_id",
    "source": "source_id",
}

RISK_PREDICATES = {
    "HAS_DRUG_BOUNDARY",
    "HAS_LABEL_BOUNDARY",
    "HAS_WITHDRAWAL_OR_MRL_BOUNDARY",
    "REGULATORY_BOUNDARY",
    "DIFFERENTIAL_DIAGNOSIS",
}

BOUNDARY_TERMS = [
    "不得",
    "不能",
    "不应",
    "不足以",
    "边界",
    "需",
    "必须",
    "疑似",
    "推测",
    "尚不",
    "未提供",
    "不能替代",
    "不得外推",
]

FACT_RE = re.compile(r"fact_id\s*=\s*([^;`]+)")
SOURCE_RE = re.compile(r"source_id\s*=\s*([^;`]+)")
ANCHOR_RE = re.compile(r"anchor\s*=\s*([^`]+)")
INLINE_META_RE = re.compile(r"`([^`]*(?:fact_id|source_id|anchor)\s*=[^`]*)`")
PAREN_SOURCE_RE = re.compile(r"[（(]((?:SRC|A0|A1|A2|RC|RULE)-[^;；)）]+)[;；]\s*([^）)]+)[）)]")


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_id(prefix: str, *parts: str) -> str:
    payload = "\n".join(parts)
    return f"{prefix}:{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(read_text(path))
    return payload if isinstance(payload, dict) else {}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return value.strip("'\"")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}, text
    frontmatter: dict[str, Any] = {}
    for line in lines[1:end_index]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = parse_scalar(value)
    return frontmatter, "\n".join(lines[end_index + 1 :])


def slugify(text: str) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip().lower(), flags=re.UNICODE)
    value = value.strip("-")
    return value or "section"


def get_page_type(path: Path) -> str | None:
    try:
        first = path.relative_to(WIKI).parts[0]
    except ValueError:
        return None
    return PAGE_DIR_TYPES.get(first)


def page_id_for(path: Path, page_type: str, frontmatter: dict[str, Any]) -> str:
    key = ID_FIELDS.get(page_type)
    raw_id = str(frontmatter.get(key, "")).strip() if key else ""
    if not raw_id:
        raw_id = path.stem
    if page_type == "drug" and raw_id.startswith("DRUG-"):
        raw_id = raw_id.split("-", 2)[0] + "-" + raw_id.split("-", 2)[1] if raw_id.count("-") >= 1 else raw_id
    return f"{page_type}:{raw_id}"


def extract_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def section_ranges(body: str, page_id: str) -> list[dict[str, Any]]:
    lines = body.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines, start=1):
        match = re.match(r"^(#{2,4})\s+(.+?)\s*$", line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2).strip()))
    ranges: list[dict[str, Any]] = []
    for pos, (line_start, level, title) in enumerate(headings):
        line_end = len(lines)
        for next_start, next_level, _ in headings[pos + 1 :]:
            if next_level <= level:
                line_end = next_start - 1
                break
        section_id = f"section:{page_id}:{slugify(title)}:{line_start}"
        ranges.append(
            {
                "id": section_id,
                "type": "section",
                "page_id": page_id,
                "section_title": title,
                "level": level,
                "line_start": line_start,
                "line_end": line_end,
            }
        )
    return ranges


def current_section(sections: list[dict[str, Any]], line_no: int) -> dict[str, Any] | None:
    """返回 line_no 所在的最具体 Markdown 章节。

    同一行可能同时落在父级 `##` 和子级 `###` 的范围内。语义边的 predicate
    依赖章节标题，如果返回父章节，就可能把“实验室诊断”下的证据误归到上层
    “病原与分类”。因此这里选择匹配范围中 level 最大、line_start 最新的章节，
    也就是离证据行最近的标题。
    """
    matches = [section for section in sections if section["line_start"] <= line_no <= section["line_end"]]
    if not matches:
        return None
    return max(matches, key=lambda section: (int(section.get("level", 0)), int(section.get("line_start", 0))))


def split_fact_ids(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[,，]", value) if item.strip()]


def strip_inline_meta(line: str) -> str:
    text = INLINE_META_RE.sub("", line)
    text = re.sub(r"^\s*[-*]\s+", "", text).strip()
    return text


def parse_inline_meta(line: str) -> list[dict[str, Any]]:
    metas: list[dict[str, Any]] = []
    for raw in INLINE_META_RE.findall(line):
        fact_match = FACT_RE.search(raw)
        source_match = SOURCE_RE.search(raw)
        anchor_match = ANCHOR_RE.search(raw)
        fact_ids = split_fact_ids(fact_match.group(1)) if fact_match else []
        source_id = source_match.group(1).strip() if source_match else ""
        anchor = anchor_match.group(1).strip().rstrip(";") if anchor_match else ""
        if fact_ids:
            for fact_id in fact_ids:
                metas.append({"fact_id": fact_id, "source_id": source_id, "anchor": anchor, "meta_mode": "inline_key_value"})
        elif source_id or anchor:
            metas.append({"fact_id": "", "source_id": source_id, "anchor": anchor, "meta_mode": "inline_key_value"})
    if metas:
        return metas
    for source_id, anchor in PAREN_SOURCE_RE.findall(line):
        metas.append({"fact_id": "", "source_id": source_id.strip(), "anchor": anchor.strip(), "meta_mode": "parenthetical_source"})
    return metas


def source_ids_from_frontmatter(frontmatter: dict[str, Any]) -> list[str]:
    value = frontmatter.get("sources", [])
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in re.split(r"[,，]", value.strip("[]")) if item.strip()]
    return []


def reference_node_type(ref_id: str) -> str:
    if ref_id.startswith("RC-"):
        return "rule_card"
    if ref_id.startswith("RULE-"):
        return "rule"
    if ref_id.startswith("DIS-"):
        return "disease"
    if ref_id.startswith("DRUG-"):
        return "drug"
    if ref_id.startswith("SYN-"):
        return "synthesis"
    return "source"


def reference_node_id(ref_id: str) -> str:
    return f"{reference_node_type(ref_id)}:{ref_id}"


def edge_type_for_reference(ref_id: str) -> str:
    node_type = reference_node_type(ref_id)
    if node_type == "rule_card":
        return "GOVERNED_BY_RULE_CARD"
    if node_type == "rule":
        return "GOVERNED_BY_RULE"
    if node_type in {"disease", "drug", "synthesis"}:
        return "REFERENCES_ENTITY"
    return "CITES_SOURCE"


def load_registry() -> dict[str, Any]:
    return json.loads(read_text(REGISTRY_PATH))


def predicate_for_section(page_type: str, section_title: str, registry: dict[str, Any]) -> str | None:
    """根据页面类型和章节标题确定 semantic 边类型。

    这是纯代码规则，不调用 LLM。输入只有：
    - page_type，例如 disease、drug、comparison；
    - section_title，例如“实验室诊断”“防控要点”“鉴别诊断”；
    - config/wiki_native_predicate_registry.json 中的 allowed_section_patterns。

    重要细节：如果章节标题同时命中普通诊断和鉴别诊断，例如“鉴别诊断”，
    必须优先使用更严格的 high-risk predicate（DIFFERENTIAL_DIAGNOSIS），
    否则会把本应受 RC-DX-001 和 second-validator 约束的鉴别边降级成普通诊断边。
    """
    title = section_title.lower()
    candidates = []
    for predicate, rule in registry["predicates"].items():
        if page_type not in rule.get("allowed_subject_types", []):
            continue
        patterns = [str(item).lower() for item in rule.get("allowed_section_patterns", [])]
        if any(pattern and pattern in title for pattern in patterns):
            candidates.append(predicate)
    if not candidates:
        return None
    if "DIFFERENTIAL_DIAGNOSIS" in candidates and any(token in title for token in ["鉴别", "differential", "comparison", "比较"]):
        return "DIFFERENTIAL_DIAGNOSIS"
    non_risk = [item for item in candidates if item not in RISK_PREDICATES]
    return non_risk[0] if non_risk else candidates[0]


def evidence_level(meta: dict[str, Any]) -> str:
    if meta.get("fact_id") and meta.get("source_id") and meta.get("anchor"):
        return "verified_candidate"
    if meta.get("source_id") and meta.get("anchor"):
        return "anchored"
    if meta.get("source_id"):
        return "source_only"
    return "candidate"


def build_page_nodes(registry: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    nodes: dict[str, Any] = {}
    report: dict[str, Any] = {
        "frontmatter_missing": [],
        "read_errors": [],
        "page_counts": Counter(),
        "source_ids_seen": set(),
    }
    for dirname, page_type in PAGE_DIR_TYPES.items():
        folder = WIKI / dirname
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            try:
                text = read_text(path)
            except UnicodeDecodeError as exc:
                report["read_errors"].append({"path": rel(path), "error": str(exc)})
                continue
            frontmatter, body = parse_frontmatter(text)
            page_id = page_id_for(path, page_type, frontmatter)
            title = extract_title(body, path.stem)
            if not frontmatter:
                report["frontmatter_missing"].append(rel(path))
            sources = source_ids_from_frontmatter(frontmatter)
            report["source_ids_seen"].update(sources)
            nodes[page_id] = {
                "id": page_id,
                "type": page_type,
                "label": title,
                "path": rel(path),
                "frontmatter": frontmatter,
                "source_ids": sources,
                "status": {
                    "legacy_evidence_status": frontmatter.get("legacy_evidence_status", ""),
                    "task_use_status": frontmatter.get("task_use_status", ""),
                    "gold_dataset_use": frontmatter.get("gold_dataset_use", ""),
                    "risk_class": frontmatter.get("risk_class", ""),
                },
            }
            report["page_counts"][page_type] += 1
            for section in section_ranges(body, page_id):
                nodes[section["id"]] = section
    report["page_counts"] = dict(report["page_counts"])
    report["source_ids_seen"] = sorted(report["source_ids_seen"])
    return nodes, report


def build_structural_edges(nodes: dict[str, Any]) -> list[dict[str, Any]]:
    """创建结构边、证据引用边和治理边。

    这一阶段完全由代码规则生成边，不调用 LLM：
    - structural：由 Markdown 标题解析出的 section 节点生成 HAS_SECTION。
    - evidence：由 frontmatter.sources 中的 SRC/A0/A1/A2 等来源生成 CITES_SOURCE。
    - governance：由 frontmatter.sources 中的 RC/RULE 生成 GOVERNED_BY_RULE_CARD/RULE。

    这些边表示“页面结构、引用来源、受规则约束”，不直接表达医学事实；
    因此即使 status=verified，也不会作为黄金数据集医学事实正例。
    """
    edges: list[dict[str, Any]] = []
    for node in nodes.values():
        if node["type"] == "section":
            # 结构边：只说明章节属于某个页面。
            # 例：disease:DIS-059 --HAS_SECTION--> section:disease:DIS-059:实验室诊断:43
            edge_id = stable_id("edge", node["page_id"], node["id"], "HAS_SECTION")
            edges.append(
                {
                    "id": edge_id,
                    "layer": "structural",
                    "type": "HAS_SECTION",
                    "source": node["page_id"],
                    "target": node["id"],
                    "status": "verified",
                    "validation_status": "accepted",
                    "blocked_from_runtime": False,
                    "gold_dataset_ready": False,
                }
            )
        elif node["type"] in {"disease", "drug", "comparison", "syndrome", "synthesis", "topic"}:
            for source_id in node.get("source_ids", []):
                # frontmatter 显式引用边：
                # - 来源 ID 进入 evidence layer；
                # - 规则卡/规则 ID 进入 governance layer。
                # 这里不推断“医学上有关”，只记录“本页声明引用/受约束”。
                target = reference_node_id(source_id)
                edge_type = edge_type_for_reference(source_id)
                layer = "governance" if edge_type.startswith("GOVERNED_BY") else "evidence"
                edge_id = stable_id("edge", node["id"], target, edge_type)
                edges.append(
                    {
                        "id": edge_id,
                        "layer": layer,
                        "type": edge_type,
                        "source": node["id"],
                        "target": target,
                        "source_id": source_id,
                        "status": "verified",
                        "validation_status": "accepted",
                        "blocked_from_runtime": False,
                        "gold_dataset_ready": False,
                    }
                )
    return edges


def ensure_reference_nodes(nodes: dict[str, Any]) -> None:
    refs: set[str] = set()
    for node in nodes.values():
        for ref_id in node.get("source_ids", []):
            refs.add(ref_id)
    for ref_id in sorted(refs):
        node_id = reference_node_id(ref_id)
        if node_id in nodes:
            continue
        nodes[node_id] = {
            "id": node_id,
            "type": reference_node_type(ref_id),
            "label": ref_id,
            "path": "",
            "placeholder": True,
            "source_page_missing": reference_node_type(ref_id) == "source",
            "created_by": "wiki_native_reference_placeholder",
        }


def build_evidence_units(nodes: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """从正文 bullet 抽取 evidence_unit。

    evidence_unit 是 semantic 语义事实边的证据来源。脚本只读取 Markdown 中显式
    写出的元数据：`fact_id=...; source_id=...; anchor=...`。

    没有这些结构化锚点的正文不会直接生成 verified 语义事实边；即使文字里出现
    SRC/A2/RC 等来源样式，也只进入 uncovered_content_summary 供人工补锚点。
    """
    evidence_units: list[dict[str, Any]] = []
    report = {
        "evidence_by_page": Counter(),
        "uncovered_content_summary": [],
        "read_errors": [],
    }
    page_nodes = [node for node in nodes.values() if node["type"] in PAGE_DIR_TYPES.values() and node["type"] != "section"]
    for node in page_nodes:
        path = ROOT / node["path"]
        if not path.exists() or path.suffix.lower() != ".md":
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError as exc:
            report["read_errors"].append({"path": node["path"], "error": str(exc)})
            continue
        _frontmatter, body = parse_frontmatter(text)
        sections = [item for item in nodes.values() if item.get("type") == "section" and item.get("page_id") == node["id"]]
        for line_no, line in enumerate(body.splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith(("-", "*")):
                continue
            evidence_text = strip_inline_meta(stripped)
            metas = parse_inline_meta(stripped)
            if not metas:
                # 反幻觉保护：像来源、但缺少可解析 fact/source/anchor 的句子不入 verified。
                if len(evidence_text) >= 30 and any(marker in evidence_text for marker in ["SRC-", "A0-", "A1-", "A2-", "RC-"]):
                    report["uncovered_content_summary"].append(
                        {
                            "page_id": node["id"],
                            "path": node["path"],
                            "line": line_no,
                            "reason": "source_like_bullet_without_parseable_anchor",
                            "text_preview": evidence_text[:180],
                        }
                    )
                continue
            section = current_section(sections, line_no)
            for meta in metas:
                unit_id = stable_id("evidence_unit", node["id"], str(line_no), evidence_text, meta.get("fact_id", ""), meta.get("source_id", ""))
                unit = {
                    "id": unit_id,
                    "type": "evidence_unit",
                    "page_id": node["id"],
                    "page_type": node["type"],
                    "page_path": node["path"],
                    "line_start": line_no,
                    "line_end": line_no,
                    "section_id": section["id"] if section else "",
                    "section_title": section["section_title"] if section else "",
                    "fact_id": meta.get("fact_id", ""),
                    "fact_id_generated": not bool(meta.get("fact_id")),
                    "source_id": meta.get("source_id", ""),
                    "anchor": meta.get("anchor", ""),
                    "evidence_text": evidence_text,
                    "evidence_text_hash": sha256_text(evidence_text),
                    "evidence_level": evidence_level(meta),
                    "meta_mode": meta.get("meta_mode", ""),
                }
                evidence_units.append(unit)
                report["evidence_by_page"][node["id"]] += 1
    report["evidence_by_page"] = dict(report["evidence_by_page"])
    return evidence_units, report


def semantic_object_node(unit: dict[str, Any], predicate: str) -> dict[str, Any]:
    """把 evidence_text 原文片段转成 literal_span 节点。

    MVP 阶段不把证据句激进拆成多个标准实体，避免把两个并无直接关系的标准节点
    误连。semantic 边的 target 因此是“可追溯原文事实片段”。
    """
    exact_text = unit["evidence_text"]
    object_id = stable_id("semantic_object", predicate, exact_text)
    return {
        "id": object_id,
        "type": "literal_span",
        "label": exact_text[:120],
        "predicate_context": predicate,
        "exact_text_span": exact_text,
        "source_evidence_unit_id": unit["id"],
    }


def has_required_rule_card(page_node: dict[str, Any], predicate_rule: dict[str, Any]) -> bool:
    required = set(predicate_rule.get("required_rule_cards", []))
    if not required:
        return True
    sources = set(page_node.get("source_ids", []))
    text_fields = json.dumps(page_node.get("frontmatter", {}), ensure_ascii=False)
    return bool(required & sources) or any(card in text_fields for card in required)


def validate_semantic_edge(edge: dict[str, Any], unit: dict[str, Any], page_node: dict[str, Any], predicate_rule: dict[str, Any]) -> tuple[str, str, dict[str, str]]:
    """验证 semantic 语义事实边能否从 candidate 升级为 verified。

    这里仍然不调用 LLM。校验条件来自 predicate registry：
    - 是否有 fact_id/source_id/anchor/evidence_text；
    - 是否有 supporting_span，且 supporting_span 必须出现在 evidence_text 中；
    - object 是否是精确文本片段；
    - 高风险或诊断类 predicate 是否绑定必要 rule card。

    不满足条件的边只能保持 candidate 或 rejected，并被 blocked_from_runtime，
    不能进入黄金数据集正例。
    """
    summary = {
        "schema": "pass",
        "endpoint": "pass",
        "provenance": "pass",
        "graph_consistency": "pass",
        "evidence_support_check": "pass",
        "second_validator": "not_required",
    }
    if predicate_rule.get("requires_fact_id") and not unit.get("fact_id"):
        summary["provenance"] = "candidate"
        return "candidate", "missing_fact_id", summary
    for field in ["source_id", "anchor", "evidence_text"]:
        if predicate_rule.get(f"requires_{field}") and not unit.get(field):
            summary["provenance"] = "candidate"
            return "candidate", f"missing_{field}", summary
    supporting_span = edge.get("supporting_span", "")
    if predicate_rule.get("requires_supporting_span") and not supporting_span:
        summary["evidence_support_check"] = "candidate"
        return "candidate", "missing_supporting_span", summary
    if supporting_span and supporting_span not in unit.get("evidence_text", ""):
        summary["evidence_support_check"] = "fail"
        return "rejected", "supporting_span_not_in_evidence_text", summary
    if predicate_rule.get("object_must_be_text_span") and not edge.get("exact_text_span"):
        summary["endpoint"] = "fail"
        return "rejected", "missing_exact_text_span", summary
    if predicate_rule.get("requires_rule_card") and not has_required_rule_card(page_node, predicate_rule):
        summary["graph_consistency"] = "candidate"
        return "candidate", "missing_required_rule_card", summary
    if predicate_rule.get("requires_second_validator"):
        summary["second_validator"] = "pass_rule_card_gated"
    return "verified", "validated", summary


def build_semantic_edges(nodes: dict[str, Any], evidence_units: list[dict[str, Any]], registry: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    """从 evidence_unit 生成 semantic 语义事实边。

    流程是确定性的：
    1. predicate_for_section() 根据页面类型和章节标题选择候选 predicate；
    2. semantic_object_node() 把证据文本保存为 literal_span 节点；
    3. 先生成 status=candidate 的 semantic 边；
    4. validate_semantic_edge() 校验通过后才改为 verified。

    因此构图阶段不会让 LLM 或“节点相似度”直接连出 verified 医学事实边。
    """
    semantic_nodes: dict[str, Any] = {}
    edges: list[dict[str, Any]] = []
    report = {"semantic_by_predicate": Counter(), "candidate_reasons": Counter(), "rejected_reasons": Counter()}
    page_nodes = {node["id"]: node for node in nodes.values() if node.get("type") != "section"}
    for unit in evidence_units:
        page_node = page_nodes.get(unit["page_id"], {})
        # 类型选择只依赖规则配置和章节标题，不依赖 LLM。
        predicate = predicate_for_section(unit["page_type"], unit.get("section_title", ""), registry)
        if not predicate:
            continue
        predicate_rule = registry["predicates"][predicate]
        # target 使用证据原文片段，保证关系边可以追溯到 supporting_span。
        object_node = semantic_object_node(unit, predicate)
        semantic_nodes[object_node["id"]] = object_node
        edge_id = stable_id("edge", unit["page_id"], predicate, object_node["id"], unit["id"])
        edge = {
            "id": edge_id,
            "layer": "semantic",
            "type": predicate,
            "source": unit["page_id"],
            "target": object_node["id"],
            "evidence_unit_id": unit["id"],
            "derived_from_fact_id": unit.get("fact_id", ""),
            "source_id": unit.get("source_id", ""),
            "anchor": unit.get("anchor", ""),
            "evidence_text": unit.get("evidence_text", ""),
            "supporting_span": unit.get("evidence_text", ""),
            "exact_text_span": unit.get("evidence_text", ""),
            "evidence_text_hash": unit.get("evidence_text_hash", ""),
            "section_id": unit.get("section_id", ""),
            "section_title": unit.get("section_title", ""),
            "edge_generation_mode": "anchored_semantic_edge_builder",
            # 所有 semantic 边初始都必须是 candidate。
            # 只有验证函数显式返回 verified，才解除 runtime 阻断并允许进入黄金数据集正例。
            "status": "candidate",
            "validation_status": "candidate",
            "blocked_from_runtime": True,
            "gold_dataset_ready": False,
        }
        status, reason, validation_summary = validate_semantic_edge(edge, unit, page_node, predicate_rule)
        edge["status"] = status
        edge["validation_status"] = "accepted" if status == "verified" else status
        edge["validation_summary"] = validation_summary
        edge["evidence_support_check"] = validation_summary["evidence_support_check"]
        edge["reason"] = reason
        if status == "verified":
            edge["blocked_from_runtime"] = False
            edge["gold_dataset_ready"] = True
        elif status == "candidate":
            report["candidate_reasons"][reason] += 1
        else:
            report["rejected_reasons"][reason] += 1
        report["semantic_by_predicate"][predicate] += 1
        edges.append(edge)
    report["semantic_by_predicate"] = dict(report["semantic_by_predicate"])
    report["candidate_reasons"] = dict(report["candidate_reasons"])
    report["rejected_reasons"] = dict(report["rejected_reasons"])
    return semantic_nodes, edges, report


def audit_graph(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {node["id"]: node for node in graph["nodes"]}
    evidence = {unit["id"]: unit for unit in graph["evidence_units"]}
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for edge in graph["edges"]:
        source = edge.get("source")
        target = edge.get("target")
        if source and source not in nodes:
            blockers.append({"edge_id": edge.get("id"), "reason": "missing_source_node", "source": source})
        if target and target not in nodes:
            blockers.append({"edge_id": edge.get("id"), "reason": "missing_target_node", "target": target})
        if edge.get("layer") != "semantic":
            continue
        status = edge.get("status")
        if status == "verified":
            unit_id = edge.get("evidence_unit_id")
            if not unit_id or unit_id not in evidence:
                blockers.append({"edge_id": edge.get("id"), "reason": "verified_missing_evidence_unit"})
            for field in ["source_id", "anchor", "evidence_text", "supporting_span"]:
                if not edge.get(field):
                    blockers.append({"edge_id": edge.get("id"), "reason": f"verified_missing_{field}"})
            if edge.get("supporting_span") and edge.get("supporting_span") not in edge.get("evidence_text", ""):
                blockers.append({"edge_id": edge.get("id"), "reason": "supporting_span_not_in_evidence_text"})
            if edge.get("evidence_support_check") != "pass":
                blockers.append({"edge_id": edge.get("id"), "reason": "verified_without_evidence_support_check_pass"})
            if edge.get("validation_status") != "accepted":
                blockers.append({"edge_id": edge.get("id"), "reason": "verified_without_accepted_validation_status"})
        if status in {"candidate", "rejected"}:
            if edge.get("blocked_from_runtime") is not True:
                blockers.append({"edge_id": edge.get("id"), "reason": "candidate_or_rejected_not_blocked"})
            if edge.get("gold_dataset_ready") is True:
                blockers.append({"edge_id": edge.get("id"), "reason": "candidate_or_rejected_gold_ready"})
        if not edge.get("reason") and status != "verified":
            warnings.append({"edge_id": edge.get("id"), "reason": "non_verified_edge_missing_reason"})
    return {"blockers": blockers, "warnings": warnings}


def build_graph() -> tuple[dict[str, Any], dict[str, Any]]:
    registry = load_registry()
    nodes, page_report = build_page_nodes(registry)
    ensure_reference_nodes(nodes)
    structural_edges = build_structural_edges(nodes)
    evidence_units, evidence_report = build_evidence_units(nodes)
    semantic_nodes, semantic_edges, semantic_report = build_semantic_edges(nodes, evidence_units, registry)
    nodes.update(semantic_nodes)
    graph = {
        "metadata": {
            "graph_kind": "wiki_native_mvp",
            "generated_at": now_iso(),
            "source": "wiki markdown",
            "predicate_registry": rel(REGISTRY_PATH),
            "runtime_compat": "legacy wiki/graph-data.json unchanged",
            "encoding": "utf-8",
        },
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": sorted(structural_edges + semantic_edges, key=lambda item: item["id"]),
        "evidence_units": sorted(evidence_units, key=lambda item: item["id"]),
        "validation_summary": {},
        "gold_dataset_readiness": {},
    }
    audit = audit_graph(graph)
    node_counts = Counter(node["type"] for node in graph["nodes"])
    edge_counts = Counter(edge.get("status", "") for edge in graph["edges"])
    semantic_status_counts = Counter(edge.get("status", "") for edge in graph["edges"] if edge.get("layer") == "semantic")
    page_gold_ready = {}
    for node in graph["nodes"]:
        if node["type"] not in {"disease", "drug"}:
            continue
        count = evidence_report["evidence_by_page"].get(node["id"], 0)
        page_gold_ready[node["id"]] = {
            "path": node.get("path", ""),
            "evidence_units": count,
            "page_gold_ready": count > 0,
        }
    graph["validation_summary"] = {
        "audit_blockers": len(audit["blockers"]),
        "audit_warnings": len(audit["warnings"]),
        "semantic_status_counts": dict(semantic_status_counts),
    }
    graph["gold_dataset_readiness"] = {
        "verified_semantic_edges": semantic_status_counts.get("verified", 0),
        "candidate_semantic_edges": semantic_status_counts.get("candidate", 0),
        "rejected_semantic_edges": semantic_status_counts.get("rejected", 0),
        "page_gold_ready_count": sum(1 for item in page_gold_ready.values() if item["page_gold_ready"]),
        "page_gold_not_ready_count": sum(1 for item in page_gold_ready.values() if not item["page_gold_ready"]),
    }
    report = {
        "build_id": "wiki-native-graph:" + now_iso(),
        "build_status": "pass" if not audit["blockers"] else "partial",
        "outputs": {"graph_path": rel(GRAPH_PATH), "report_json": rel(REPORT_JSON), "report_md": rel(REPORT_MD)},
        "input_snapshot": {"predicate_registry_hash": sha256_text(read_text(REGISTRY_PATH))},
        "coverage": {
            "node_counts": dict(node_counts),
            "edge_status_counts": dict(edge_counts),
            "evidence_unit_count": len(evidence_units),
            "page_counts": page_report["page_counts"],
            "frontmatter_missing_count": len(page_report["frontmatter_missing"]),
            "uncovered_content_summary_count": len(evidence_report["uncovered_content_summary"]),
        },
        "semantic": semantic_report,
        "audit": audit,
        "frontmatter_missing": page_report["frontmatter_missing"][:100],
        "uncovered_content_summary": evidence_report["uncovered_content_summary"][:200],
        "page_gold_readiness": page_gold_ready,
        "failed_operations": page_report["read_errors"] + evidence_report["read_errors"],
    }
    return graph, report


def render_report_md(report: dict[str, Any]) -> str:
    coverage = report["coverage"]
    semantic = report["semantic"]
    audit = report["audit"]
    lines = [
        "# Wiki Native Graph Build Report",
        "",
        f"- Build ID: `{report['build_id']}`",
        f"- Build status: `{report['build_status']}`",
        f"- Graph path: `{report['outputs']['graph_path']}`",
        f"- Report JSON: `{report['outputs']['report_json']}`",
        "- Encoding: UTF-8 read/write enforced by script",
        "",
        "## Coverage",
        "",
        f"- Evidence units: {coverage['evidence_unit_count']}",
        f"- Frontmatter missing: {coverage['frontmatter_missing_count']}",
        f"- Uncovered content summary items: {coverage['uncovered_content_summary_count']}",
        f"- Node counts: `{json.dumps(coverage['node_counts'], ensure_ascii=False)}`",
        f"- Edge status counts: `{json.dumps(coverage['edge_status_counts'], ensure_ascii=False)}`",
        "",
        "## Semantic Edges",
        "",
        f"- By predicate: `{json.dumps(semantic['semantic_by_predicate'], ensure_ascii=False)}`",
        f"- Candidate reasons: `{json.dumps(semantic['candidate_reasons'], ensure_ascii=False)}`",
        f"- Rejected reasons: `{json.dumps(semantic['rejected_reasons'], ensure_ascii=False)}`",
        "",
        "## Audit",
        "",
        f"- Blockers: {len(audit['blockers'])}",
        f"- Warnings: {len(audit['warnings'])}",
        "",
    ]
    if audit["blockers"]:
        lines.extend(["### Blockers", ""])
        for item in audit["blockers"][:50]:
            lines.append(f"- `{json.dumps(item, ensure_ascii=False)}`")
        lines.append("")
    if report["failed_operations"]:
        lines.extend(["## Failed Operations", ""])
        for item in report["failed_operations"][:50]:
            lines.append(f"- `{json.dumps(item, ensure_ascii=False)}`")
        lines.append("")
    lines.extend(
        [
            "## Runtime Admission",
            "",
            "Only semantic edges with `status=verified`, `validation_status=accepted`, and `evidence_support_check=pass` are eligible for golden dataset positive examples.",
            "Candidate and rejected edges remain in the unified graph for review, gap discovery, and anti-hallucination training.",
            "",
        ]
    )
    return "\n".join(lines)


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def edge_key(edge: dict[str, Any]) -> str:
    return "|".join(
        [
            str(edge.get("source", "")),
            str(edge.get("target", "")),
            str(edge.get("type", "")),
            str(edge.get("layer", "")),
            str(edge.get("evidence_unit_id", "")),
            str(edge.get("derived_from_fact_id", "")),
        ]
    )


def graph_maps(graph: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    nodes = {
        str(node.get("id", "")): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    }
    edges = {
        edge_key(edge): edge
        for edge in graph.get("edges", [])
        if isinstance(edge, dict) and edge.get("source") and edge.get("target")
    }
    return nodes, edges


def classify_native_node_change(node_id: str) -> str:
    if node_id.startswith("section:"):
        return "section"
    if node_id.startswith("semantic_object:"):
        return "semantic_object"
    if node_id.startswith("source:"):
        return "source"
    if node_id.startswith("disease:"):
        return "disease"
    if node_id.startswith("drug:"):
        return "drug"
    if ":" in node_id:
        return node_id.split(":", 1)[0]
    return "node"


def native_diff_graph(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    prev_nodes, prev_edges = graph_maps(previous)
    curr_nodes, curr_edges = graph_maps(current)

    added_nodes = sorted(set(curr_nodes) - set(prev_nodes))
    removed_nodes = sorted(set(prev_nodes) - set(curr_nodes))
    common_nodes = sorted(set(curr_nodes) & set(prev_nodes))
    changed_nodes = [node_id for node_id in common_nodes if digest(curr_nodes[node_id]) != digest(prev_nodes[node_id])]

    added_edge_keys = sorted(set(curr_edges) - set(prev_edges))
    removed_edge_keys = sorted(set(prev_edges) - set(curr_edges))
    common_edge_keys = sorted(set(curr_edges) & set(prev_edges))
    changed_edge_keys = [key for key in common_edge_keys if digest(curr_edges[key]) != digest(prev_edges[key])]

    added_links = [describe_native_edge(curr_edges[key]) for key in added_edge_keys]
    removed_links = [describe_native_edge(prev_edges[key]) for key in removed_edge_keys]
    changed_links = [describe_native_edge(curr_edges[key]) for key in changed_edge_keys]

    crud_counts: dict[str, dict[str, int]] = {}
    for operation, node_ids in {
        "create": added_nodes,
        "delete_or_exclude": removed_nodes,
        "update": changed_nodes,
    }.items():
        for node_id in node_ids:
            entity_type = classify_native_node_change(node_id)
            crud_counts.setdefault(operation, {})
            crud_counts[operation][entity_type] = crud_counts[operation].get(entity_type, 0) + 1

    prev_verified = sum(
        1
        for edge in prev_edges.values()
        if edge.get("layer") == "semantic" and edge.get("status") == "verified"
    )
    curr_verified = sum(
        1
        for edge in curr_edges.values()
        if edge.get("layer") == "semantic" and edge.get("status") == "verified"
    )

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
            "delta_nodes": len(curr_nodes) - len(prev_nodes),
            "links_before": len(prev_edges),
            "links_after": len(curr_edges),
            "delta_links": len(curr_edges) - len(prev_edges),
            "facts_in_graph": len(current.get("evidence_units", [])) if isinstance(current.get("evidence_units"), list) else 0,
            "added_nodes": len(added_nodes),
            "removed_nodes": len(removed_nodes),
            "changed_nodes": len(changed_nodes),
            "added_links": len(added_links),
            "removed_links": len(removed_links),
            "changed_links": len(changed_links),
            "verified_semantic_edges_before": prev_verified,
            "verified_semantic_edges_after": curr_verified,
            "delta_verified_semantic_edges": curr_verified - prev_verified,
        },
    }


def describe_native_edge(edge: dict[str, Any]) -> str:
    edge_type = str(edge.get("type", "") or "")
    status = str(edge.get("status", "") or "")
    return f"{edge.get('source', '')} -> {edge.get('target', '')} [{edge_type}, {status}]"


def recent_native_crud_events(current: dict[str, Any], diff: dict[str, Any]) -> list[dict[str, str]]:
    events: list[dict[str, str]] = []
    nodes = {
        str(node.get("id", "")): node
        for node in current.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    }
    changed_disease_nodes = [node_id for node_id in diff.get("changed_nodes", []) if str(node_id).startswith("disease:")]
    for node_id in changed_disease_nodes[:3]:
        node = nodes.get(node_id, {})
        path = str(node.get("path", "") or "")
        label = str(node.get("label", "") or node_id)
        events.append(
            {
                "operation": "update",
                "target": path or node_id,
                "reason": f"页面 {label} 发生结构或证据锚点更新，并重新参与 wiki-native 主图谱构建。"
            }
        )
    added_source_nodes = [node_id for node_id in diff.get("added_nodes", []) if str(node_id).startswith("source:")]
    for node_id in added_source_nodes[:3]:
        node = nodes.get(node_id, {})
        path = str(node.get("path", "") or "")
        label = str(node.get("label", "") or node_id)
        events.append(
            {
                "operation": "create",
                "target": path or node_id,
                "reason": f"新增来源页 {label}，并纳入 wiki-native 来源节点与章节节点。"
            }
        )
    return events


def native_reasonableness(diff: dict[str, Any]) -> str:
    summary = diff.get("summary", {}) if isinstance(diff.get("summary"), dict) else {}
    return (
        "该变更日志由 wiki-native 图谱构建脚本自动生成。"
        f"本次节点净变化 {summary.get('delta_nodes', 0)}，边净变化 {summary.get('delta_links', 0)}，"
        f"verified semantic edges 净变化 {summary.get('delta_verified_semantic_edges', 0)}。"
        "最近一次更新说明来自当前主图谱与上一份 wiki-native 快照的结构化对比，不再依赖手工编辑 diff 文件。"
    )


def render_native_diff_md(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    lines = [
        "# Wiki-Native Graph Change Diff",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## CRUD Counts", ""])
    crud_counts = payload.get("crud_counts", {})
    if isinstance(crud_counts, dict) and crud_counts:
        for operation, counts in crud_counts.items():
            if not isinstance(counts, dict):
                continue
            detail = ", ".join(f"{key}: {value}" for key, value in sorted(counts.items()))
            lines.append(f"- {operation}: {detail}")
    else:
        lines.append("- No node-level CRUD changes detected.")
    lines.extend(["", "## Recent CRUD Events", ""])
    events = payload.get("recent_crud_events", [])
    if isinstance(events, list) and events:
        for item in events:
            if not isinstance(item, dict):
                continue
            lines.append(f"- {item.get('operation', '')}: `{item.get('target', '')}` - {item.get('reason', '')}")
    else:
        lines.append("- None")
    lines.extend(["", "## Reasonableness", "", str(payload.get("reasonableness", "")), ""])
    return "\n".join(lines)


def write_native_diff(current_graph: dict[str, Any]) -> None:
    previous_graph = load_json(LATEST_NATIVE_SNAPSHOT)
    if not previous_graph:
        previous_graph = current_graph
    diff = native_diff_graph(previous_graph, current_graph)
    payload = {
        "generated_at": str(current_graph.get("metadata", {}).get("generated_at") or now_iso()),
        "graph_path": rel(GRAPH_PATH),
        **diff,
        "recent_crud_events": recent_native_crud_events(current_graph, diff),
        "reasonableness": native_reasonableness(diff),
    }
    write_json(NATIVE_DIFF_JSON, payload)
    write_text(NATIVE_DIFF_MD, render_native_diff_md(payload))
    write_json(LATEST_NATIVE_SNAPSHOT, current_graph)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build wiki-native knowledge graph MVP.")
    parser.add_argument("--phase", choices=["scan", "evidence", "semantic", "validate", "report", "audit", "all"], default="all")
    args = parser.parse_args()
    if args.phase != "all":
        # MVP keeps one deterministic build path while preserving the documented phase CLI.
        print(f"Running full MVP build for requested phase: {args.phase}")
    graph, report = build_graph()
    write_json(GRAPH_PATH, graph)
    write_json(REPORT_JSON, report)
    write_text(REPORT_MD, render_report_md(report))
    write_native_diff(graph)
    print(json.dumps({"graph": rel(GRAPH_PATH), "report": rel(REPORT_JSON), "status": report["build_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
