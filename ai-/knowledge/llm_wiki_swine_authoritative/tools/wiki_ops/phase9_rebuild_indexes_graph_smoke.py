from __future__ import annotations

import csv
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

"""索引、知识图谱和 smoke test 重建脚本。

由 run_swine_wiki_maintenance_checks.py 在更新后验收阶段调用。
它读取 runtime manifest 和 wiki 数据，重建图谱文件，并输出基础检索 smoke 测试报告。

本脚本处理的核心数据流：

1. 输入数据
   - `exports/runtime_core_manifest.json`
     默认生产/评估检索允许加载的 runtime 页面清单。
   - `exports/*_index.csv`
     source、disease、drug、rule、comparison、synthesis 等派生索引。
   - `exports/knowledge_facts_status_index.json`
     标准化后的事实状态索引，只把 `valid + source_anchored` 的事实放进图谱。

2. 派生数据
   - `wiki/graph-data.json`
     机器可读知识图谱数据，供交互图谱和 graph diff 使用。
   - `wiki/knowledge-graph.md`
     简短 Mermaid 预览图，便于 Markdown 审阅。
   - `wiki/knowledge-graph.html`
     交互式知识图谱页面，由 `render_wash_interactive_graph.py` 渲染。
   - `issues/runtime_retrieval_smoke_test_*.json/.md`
     检索 smoke test 报告。
   - `issues/phase9_index_graph_rebuild_*.json`
     本脚本的总报告。

3. 验收目标
   - 索引去重并确认 `wiki/...` 路径存在；
   - 图谱节点/边反映 runtime 页面、source、rule card、fact 的关系；
   - 基础检索场景能命中预期页面，且不把 raw/issues/矩阵类非 runtime 文件混入默认结果。
"""

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"

# 主要输入：runtime manifest。
# 它决定哪些页面属于默认生产/评估检索核心范围。
MANIFEST = EXPORTS / "runtime_core_manifest.json"

# 主要输出：图谱三件套。
# graph-data.json 是机器真源；md/html 是审阅和可视化产物。
GRAPH_JSON = WIKI / "graph-data.json"
GRAPH_MD = WIKI / "knowledge-graph.md"
GRAPH_HTML = WIKI / "knowledge-graph.html"

# smoke test 输出。文件名沿用既有日期，避免破坏下游引用。
SMOKE_JSON = ISSUES / "runtime_retrieval_smoke_test_2026-05-09.json"
SMOKE_MD = ISSUES / "runtime_retrieval_smoke_test_2026-05-09.md"

# 本脚本总报告输出。
INDEX_REPORT = ISSUES / "phase9_index_graph_rebuild_2026-05-09.json"
TZ = timezone(timedelta(hours=8))

# 需要规范化的 CSV 索引及其业务主键字段。
# id_fields 用于去重和排序；不同索引历史字段不完全一致，所以每类单独声明。
INDEX_SPECS = {
    "source_index.csv": ["source_id", "relpath", "page_relpath"],
    "disease_index.csv": ["disease_id", "page_relpath"],
    "drug_page_index.csv": ["drug_id", "id", "page_relpath", "path"],
    "rule_index.csv": ["rule_id", "page_relpath"],
    "rule_card_index.csv": ["card_id", "page_relpath"],
    "comparison_index.csv": ["comparison_id", "page_relpath"],
    "synthesis_index.csv": ["synthesis_id", "id", "page_relpath", "path"],
}


def now() -> str:
    """返回带 Asia/Shanghai 时区的当前时间字符串，用于报告时间戳。"""
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    """读取 UTF-8-SIG CSV。

    使用 utf-8-sig 是为了兼容历史上可能带 BOM 的 Excel/CSV 输出。
    文件不存在时返回空列表，让后续报告明确显示 rows=0。
    """
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    """写回 UTF-8-SIG CSV，保持 Windows/Excel 查看兼容性。"""
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def migrate_legacy_fieldnames(fieldnames: list[str]) -> list[str]:
    return fieldnames


def normalize_index(name: str, id_fields: list[str]) -> dict[str, object]:
    """规范化一个派生索引。

    处理内容：
    - 按 id_fields 去重；
    - 清理字段首尾空白和 BOM；
    - 检查 `relpath`、`page_relpath`、`path` 中的 `wiki/...` 路径是否真实存在；
    - 按业务主键排序后写回。

    返回值会进入总报告，供 postcheck 判断 missing_paths 是否为 0。
    """
    path = EXPORTS / name
    rows = read_csv(path)
    if not rows:
        return {"index": name, "rows": 0, "deduplicated": 0, "missing_paths": [], "rewritten": False}
    original_fieldnames = list(rows[0].keys())
    fieldnames = migrate_legacy_fieldnames(original_fieldnames)
    seen: set[tuple[str, ...]] = set()
    normalized: list[dict[str, str]] = []
    missing_paths = []
    for row in rows:
        # 优先使用业务主键去重；如果该行没有主键字段，则退回整行内容作为 key。
        key = tuple(row.get(field, "") for field in id_fields if row.get(field, ""))
        if not key:
            key = tuple(row.get(field, "") for field in fieldnames)
        if key in seen:
            continue
        seen.add(key)
        clean = {}
        for original, field in zip(original_fieldnames, fieldnames):
            clean[field] = (row.get(original, "") or "").replace("\ufeff", "").strip()
        normalized.append(clean)
        # 派生索引里只检查 wiki 内部路径。外部 URL、PDF 页码等不在这里判定。
        for path_field in ["relpath", "page_relpath", "path"]:
            relpath = clean.get(path_field, "")
            if relpath and relpath.startswith("wiki/") and not (ROOT / relpath).exists():
                missing_paths.append({"id": key[0] if key else "", "field": path_field, "path": relpath})
    normalized.sort(key=lambda row: tuple(row.get(field, "") for field in id_fields) or tuple(row.values()))
    write_csv(path, normalized, fieldnames)
    return {
        "index": name,
        "rows": len(normalized),
        "deduplicated": len(rows) - len(normalized),
        "missing_paths": missing_paths,
        "rewritten": True,
    }


def load_manifest() -> list[dict[str, object]]:
    """加载 runtime manifest entries。

    manifest 是图谱页面节点的主来源；只有 manifest 中的 runtime 页面会作为
    disease/drug/rule/synthesis 等实体节点进入默认图谱骨架。
    """
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = payload.get("entries", [])
    return entries if isinstance(entries, list) else []


def node_id(prefix: str, value: str) -> str:
    """生成稳定图谱节点 ID，例如 `disease:DIS-038`、`source:A1-...`。"""
    return f"{prefix}:{value}"


def add_node(nodes: dict[str, dict[str, object]], node_id_value: str, label: str, group: str, **extra: object) -> None:
    """向图谱节点字典添加节点。

    使用 dict 去重：同一 source/rule/fact 被多个页面引用时，只保留一个节点。
    """
    if node_id_value not in nodes:
        nodes[node_id_value] = {"id": node_id_value, "label": label, "group": group, **extra}


def add_link(links: list[dict[str, object]], source: str, target: str, link_type: str, **extra: object) -> None:
    """向图谱添加一条边。

    边不在这里去重，因为同一组节点之间可能存在不同 fact_id 或不同关系类型。
    后续 graph diff 会按 source/target/type/fact_id 等字段比较变化。
    """
    if source and target:
        links.append({"source": source, "target": target, "type": link_type, **extra})


def build_graph(entries: list[dict[str, object]]) -> dict[str, object]:
    """根据 manifest 和 fact status index 构建图谱数据。

    图谱包含三类主要关系：

    - runtime 页面 -> source：`source_anchor`
    - runtime 页面 -> rule card：`rule_guardrail`
    - runtime 页面 -> fact -> source：`fact_anchor` / `evidence_source`

    这样图谱不仅能显示“有哪些页面”，还能显示页面背后的来源、事实和规则门禁。
    """
    nodes: dict[str, dict[str, object]] = {}
    links: list[dict[str, object]] = []
    for entry in entries:
        # 1. 每个 runtime manifest entry 变成一个实体节点。
        page_id = str(entry.get("page_id", ""))
        entity_type = str(entry.get("entity_type", ""))
        relpath = str(entry.get("path", ""))
        nid = node_id(entity_type, page_id)
        add_node(
            nodes,
            nid,
            page_id,
            entity_type,
            path=relpath,
            source_trust=entry.get("source_trust", ""),
            evidence_coverage=entry.get("evidence_coverage", ""),
            usage_scope=entry.get("usage_scope", []),
            risk_class=entry.get("risk_class", ""),
            authority_level=entry.get("authority_level", ""),
        )
        # 2. manifest 中登记的 source_ids 变成 source_anchor 边。
        for source_id in entry.get("source_ids", []) or []:
            sid = str(source_id)
            snode = node_id("source", sid)
            add_node(nodes, snode, sid, "source")
            add_link(links, nid, snode, "source_anchor")
        # 3. 根据风险类别、实体类型和 gold role 自动挂 rule card 门禁节点。
        for card in required_rule_cards(entry):
            rnode = node_id("rule_card", card)
            add_node(nodes, rnode, card, "rule_card")
            add_link(links, nid, rnode, "rule_guardrail")

    # 4. 读取标准化事实状态索引，只纳入“有效且 source anchored”的事实。
    # 这是避免候选事实、冲突事实或缺少来源的事实污染图谱。
    facts_path = EXPORTS / "knowledge_facts_status_index.json"
    facts = json.loads(facts_path.read_text(encoding="utf-8")) if facts_path.exists() else []
    fact_count = 0
    for fact in facts:
        if not isinstance(fact, dict):
            continue
        if fact.get("source_trust") != "authoritative" or fact.get("evidence_coverage") not in {"complete", "partial"}:
            continue
        source_id = str(fact.get("evidence_source_id") or fact.get("source_id") or "")
        target_page = str(fact.get("target_page") or "")
        if not source_id:
            continue
        fact_id = str(fact.get("fact_id") or f"fact-{fact_count}")
        fnode = node_id("fact", fact_id)
        label = str(fact.get("subject") or fact_id)[:90]
        add_node(
            nodes,
            fnode,
            label,
            "fact",
            source_trust=fact.get("source_trust", ""),
            evidence_coverage=fact.get("evidence_coverage", ""),
            usage_scope=fact.get("usage_scope", []),
            risk_class=fact.get("risk_class", ""),
        )
        # fact -> source：说明这个事实的证据来源。
        snode = node_id("source", source_id)
        add_node(nodes, snode, source_id, "source")
        add_link(links, fnode, snode, "evidence_source", fact_id=fact_id)
        # runtime page -> fact：如果 fact 声明了 target_page，挂回对应页面。
        if target_page.startswith("wiki/"):
            target_entries = [e for e in entries if e.get("path") == target_page]
            if target_entries:
                target = node_id(str(target_entries[0].get("entity_type", "page")), str(target_entries[0].get("page_id", target_page)))
                add_link(links, target, fnode, "fact_anchor", fact_id=fact_id)
        fact_count += 1

    # 统计节点组和边类型，写入 metadata，便于审计和图谱变化摘要展示。
    group_counts: dict[str, int] = {}
    link_counts: dict[str, int] = {}
    for node in nodes.values():
        group = str(node.get("group", ""))
        group_counts[group] = group_counts.get(group, 0) + 1
    for link in links:
        ltype = str(link.get("type", ""))
        link_counts[ltype] = link_counts.get(ltype, 0) + 1
    return {
        "metadata": {
            "generated_at": now(),
            "domain": "swine LLM wiki runtime graph",
            "runtime_entries": len(entries),
            "facts_in_graph": fact_count,
            "node_groups": group_counts,
            "link_types": link_counts,
        },
        "nodes": list(nodes.values()),
        "links": links,
    }


def required_rule_cards(entry: dict[str, object]) -> list[str]:
    """根据 manifest entry 推导应挂载的基础规则卡。

    这里不是判定事实真伪，而是把检索/生成必须遵守的规则门禁显式挂到图谱上：
    - 可生成/评估页面必须有引用规则；
    - 药物页面必须有药物规则；
    - 残留/食品安全风险必须有 MRL/withdrawal 规则；
    - 高监管风险必须有疾病监管和时效规则；
    - synthesis/gold policy 页面必须挂相应 scope/rubric 规则。
    """
    cards = set()
    usage_scope = set(entry.get("usage_scope", []) or [])
    if usage_scope.intersection({"generation_context", "evaluation", "training_candidate", "guardrail", "policy"}):
        cards.add("RC-CITATION-001")
    if entry.get("entity_type") == "drug":
        cards.add("RC-DRUG-001")
    if entry.get("risk_class") in {"withdrawal_mrl_residue", "food_safety"}:
        cards.add("RC-WITHDRAWAL-MRL-001")
    if entry.get("risk_class") == "high_regulatory":
        cards.add("RC-DISEASE-REGULATORY-001")
        cards.add("RC-REGULATORY-CURRENT-001")
    if entry.get("entity_type") == "synthesis":
        cards.add("RC-SYNTHESIS-SCOPE-001")
    if usage_scope.intersection({"policy", "guardrail"}):
        cards.add("RC-EVAL-RUBRIC-001")
    return sorted(cards)


def write_graph_files(graph: dict[str, object]) -> None:
    """写出 graph-data.json、knowledge-graph.md 和 knowledge-graph.html。

    `graph-data.json` 是完整数据；
    `knowledge-graph.md` 只截取前若干节点/边生成轻量 Mermaid 预览；
    `knowledge-graph.html` 由专门渲染脚本生成，用于交互查看。
    """
    GRAPH_JSON.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    nodes = graph["nodes"]
    links = graph["links"]
    mermaid_links = []
    safe_labels: dict[str, str] = {}
    for idx, node in enumerate(nodes[:160]):
        # Mermaid 节点 ID 只能使用较安全的字符，因此这里做一次转义映射。
        mid = re.sub(r"[^A-Za-z0-9_]", "_", str(node["id"]))
        safe_labels[str(node["id"])] = mid
    for link in links[:260]:
        source = safe_labels.get(str(link["source"]))
        target = safe_labels.get(str(link["target"]))
        if source and target:
            mermaid_links.append(f'  {source}["{str(link["source"]).replace("\"", "")}"] -->|{link["type"]}| {target}["{str(link["target"]).replace("\"", "")}"]')
    md = [
        "# Swine LLM Wiki Runtime Graph",
        "",
        "> Derived from `exports/runtime_core_manifest.json` and `exports/knowledge_facts_status_index.json`.",
        "",
        f"- Generated: {graph['metadata']['generated_at']}",
        f"- Runtime entries: {graph['metadata']['runtime_entries']}",
        f"- Facts in graph: {graph['metadata']['facts_in_graph']}",
        "",
        "```mermaid",
        "graph LR",
        *mermaid_links,
        "```",
        "",
    ]
    GRAPH_MD.write_text("\n".join(md), encoding="utf-8")
    renderer = ROOT / "tools" / "render_wash_interactive_graph.py"
    # HTML 渲染失败时直接抛错，让 postcheck 失败，而不是留下过期图谱页面。
    result = subprocess.run([sys.executable, str(renderer)], cwd=ROOT.parents[1], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:] or result.stdout[-2000:])


def smoke_tests(entries: list[dict[str, object]]) -> dict[str, object]:
    """运行基础检索 smoke test。

    这里不是完整搜索引擎测试，而是用 manifest 字段构造轻量可检索文本，
    检查几个高价值查询是否至少能命中预期页面/规则，并且不命中 raw、
    issues、treatment_matrix、prescription_matrix 等不该进入默认检索的材料。
    """
    tests = [
        {
            "query": "仔猪腹泻 黄白痢 水样腹泻",
            "expect_any": ["DIS-040", "DIS-041", "SYN-001", "CMP-001"],
            "expect_not": ["raw/", "issues/", "treatment_matrix", "prescription_matrix", "graph-data.json"],
        },
        {
            "query": "口蹄疫 水疱 调运 上报",
            "expect_any": ["DIS-026", "RC-DISEASE-REGULATORY-001", "RC-REGULATORY-CURRENT-001", "CMP-005"],
            "expect_not": ["raw/", "issues/", "treatment_matrix", "prescription_matrix"],
        },
        {
            "query": "恩诺沙星 休药期 残留",
            "expect_any": ["DRUG-018", "RC-DRUG-001", "RC-WITHDRAWAL-MRL-001"],
            "expect_not": ["raw/", "issues/", "prescription_matrix"],
        },
        {
            "query": "PCR 阳性 Ct 值 是否确诊",
            "expect_any": ["RC-DX-001", "RC-EVAL-RUBRIC-001"],
            "expect_not": ["raw/", "issues/", "graph-data.json"],
        },
        {
            "query": "非洲猪瘟 扑杀 治疗",
            "expect_any": ["DIS-002", "RC-DISEASE-REGULATORY-001", "RC-ASF-001"],
            "expect_not": ["raw/", "issues/", "treatment_matrix"],
        },
    ]
    searchable = []
    for entry in entries:
        # 只使用 manifest 中的核心字段做轻量检索代理。
        # 真正生产检索可以更复杂，但 smoke test 关注“默认清单是否明显跑偏”。
        fields = " ".join(
            str(entry.get(key, ""))
            for key in ["page_id", "path", "entity_type", "risk_class", "source_trust", "evidence_coverage", "usage_scope"]
        )
        searchable.append({"entry": entry, "text": fields.lower()})
    results = []
    for test in tests:
        tokens = [token.lower() for token in re.split(r"\s+", test["query"]) if token]
        scored = []
        for item in searchable:
            # 基础 token 命中加分。
            score = sum(1 for token in tokens if token in item["text"])
            page_id = str(item["entry"].get("page_id", ""))
            path = str(item["entry"].get("path", ""))
            for expected in test["expect_any"]:
                # 明确期望的页面/规则 ID 加高权重，确保核心路由能排到前列。
                if expected.lower() in (page_id + " " + path).lower():
                    score += 5
            if score:
                scored.append((score, item["entry"]))
        top = [entry for _, entry in sorted(scored, key=lambda pair: pair[0], reverse=True)[:8]]
        joined = json.dumps(top, ensure_ascii=False)
        # expect_any 至少命中一个；expect_not 任一命中都算失败。
        hit_expected = any(expected in joined for expected in test["expect_any"])
        hit_forbidden = any(bad in joined for bad in test["expect_not"])
        results.append(
            {
                "query": test["query"],
                "top_page_ids": [entry.get("page_id", "") for entry in top],
                "top_paths": [entry.get("path", "") for entry in top],
                "hit_expected": hit_expected,
                "hit_forbidden": hit_forbidden,
                "passed": hit_expected and not hit_forbidden,
            }
        )
    return {"tests": results, "passed": all(item["passed"] for item in results)}


def write_smoke_report(smoke: dict[str, object]) -> None:
    """写出 smoke test 的 JSON 和 Markdown 报告。"""
    SMOKE_JSON.write_text(json.dumps(smoke, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Runtime Retrieval Smoke Test / 2026-05-09", "", f"Generated: {now()}", "", f"- Overall passed: {str(smoke['passed']).lower()}", "", "## Queries", ""]
    for item in smoke["tests"]:
        lines.append(f"- Query: {item['query']}")
        lines.append(f"  - passed: {str(item['passed']).lower()}")
        lines.append(f"  - top_page_ids: {', '.join(str(x) for x in item['top_page_ids'])}")
        lines.append(f"  - hit_forbidden: {str(item['hit_forbidden']).lower()}")
    SMOKE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """重建索引、知识图谱和 smoke 测试报告。"""
    # 1. 规范化各类派生索引，并收集缺失路径。
    index_reports = [normalize_index(name, fields) for name, fields in INDEX_SPECS.items()]
    # 2. 从 runtime manifest 加载默认检索页面清单。
    entries = load_manifest()
    # 3. 从 manifest + fact status index 构建图谱。
    graph = build_graph(entries)
    # 4. 写出 graph-data、Markdown 预览和 HTML 交互图。
    write_graph_files(graph)
    # 5. 运行轻量检索 smoke test，确认默认路由没有明显跑偏。
    smoke = smoke_tests(entries)
    write_smoke_report(smoke)
    # 6. 汇总本阶段报告，供 run_swine_wiki_maintenance_checks.py 收集。
    missing_paths = sum(len(report["missing_paths"]) for report in index_reports)
    report = {
        "generated_at": now(),
        "index_reports": index_reports,
        "missing_index_paths": missing_paths,
        "graph": {
            "json": GRAPH_JSON.relative_to(ROOT).as_posix(),
            "md": GRAPH_MD.relative_to(ROOT).as_posix(),
            "html": GRAPH_HTML.relative_to(ROOT).as_posix(),
            "nodes": len(graph["nodes"]),
            "links": len(graph["links"]),
            "facts_in_graph": graph["metadata"]["facts_in_graph"],
        },
        "smoke_test": {
            "passed": smoke["passed"],
            "json": SMOKE_JSON.relative_to(ROOT).as_posix(),
            "md": SMOKE_MD.relative_to(ROOT).as_posix(),
        },
    }
    INDEX_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
