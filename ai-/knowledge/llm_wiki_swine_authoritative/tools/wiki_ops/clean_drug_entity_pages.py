import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DRUG_DIR = ROOT / "wiki" / "drugs"
DRUG_INDEX = ROOT / "exports" / "drug_page_index.csv"
REPORT = ROOT / "issues" / "drug_entity_page_cleanup_2026-05-08.md"
SUMMARY_JSON = ROOT / "issues" / "drug_entity_page_cleanup_2026-05-08.json"
UPDATED = "2026-05-08T23:59:00+08:00"

SOURCE_LIKE_RE = re.compile(r"(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+|RULE-[A-Z0-9-]+)")
FACT_ID_RE = re.compile(r"(?:fact_id=|`)([A-Z]{2,}[A-Z0-9]*-[A-Z0-9][A-Z0-9._-]+)")


def split_front_matter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    meta = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body


def render_front_matter(meta):
    order = [
        "tags",
        "drug_id",
        "updated",
        "evidence_status",
        "jurisdiction",
        "gold_dataset_use",
        "drug_page_status",
        "sources",
        "candidate_source",
    ]
    lines = ["---"]
    for key in order:
        if key in meta:
            lines.append(f"{key}: {meta[key]}")
    for key in sorted(k for k in meta if k not in order):
        lines.append(f"{key}: {meta[key]}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def parse_list(value):
    value = (value or "").strip()
    if value.startswith("[") and value.endswith("]"):
        inside = value[1:-1].strip()
        if not inside:
            return []
        return [x.strip().strip("'\"") for x in inside.split(",") if x.strip()]
    return [value] if value else []


def list_value(items):
    out = []
    for item in items:
        if item and item not in out:
            out.append(item)
    return "[" + ", ".join(out) + "]"


def source_like_ids(text):
    return sorted(set(SOURCE_LIKE_RE.findall(text or "")))


def fact_ids(text):
    raw = FACT_ID_RE.findall(text)
    return sorted({x.rstrip("`.;,") for x in raw if not x.startswith(("SRC-", "RC-", "RULE-")) and x != "HUMAN_REVIEWED"})


def profile(text, meta):
    sources = source_like_ids(text)
    facts = fact_ids(text)
    pages = re.findall(r"\b(?:PDF page|page|p\.)\s*[0-9]+", text, flags=re.I)
    batch_blocks = sorted(set(re.findall(r"<!--\s*([A-Z0-9_]+_START)\s*-->", text)))
    has_handbook = "HANDBOOK_RX_V13_1_START" in text or "HANDBOOK-RX-" in text
    has_vtop = "VTOP_V13_1_START" in text or "VTOP-" in text
    has_sfdut = "SFDUT_1_200_V13_1_START" in text or "SFDUT_200_363_V13_1_START" in text or "SFDUT1-" in text or "SFDUT2-" in text
    has_label_candidate = "v11_label_candidate" in text or "positive_label_candidate" in text
    drug_id = meta.get("drug_id", "")
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.M)
    title = title_match.group(1) if title_match else ""
    regulated = (
        "food-animal-banned-drug-list" in drug_id
        or "banned-drug-list" in drug_id
        or "食品动物禁用药清单" in title
    )
    executable_signals = (not regulated) and (has_handbook or has_sfdut or any(x in text for x in ["dose=", "meat_withhold=", "withdrawal_or_meat_withhold", "用法与用量", "dose_route_course"]))

    if regulated:
        status = "regulatory_boundary_page"
        evidence_status = "HUMAN_REVIEWED"
        tag = "regulatory_boundary_page"
        gold_use = "boundary_only"
    elif executable_signals and (len(facts) >= 2 or has_handbook or has_sfdut):
        status = "source_anchored_drug_evidence_page"
        evidence_status = "HUMAN_REVIEWED"
        tag = "drug_evidence_page"
        gold_use = "evidence_linked_candidate"
    elif sources and (len(facts) >= 1 or pages):
        status = "partial_drug_evidence_page"
        evidence_status = "NEEDS_REVIEW"
        tag = "partial_drug_evidence_page"
        gold_use = "boundary_only"
    else:
        status = "drug_stub_page"
        evidence_status = "NEEDS_REVIEW"
        tag = "drug_stub_page"
        gold_use = "boundary_only"

    return {
        "sources": sources,
        "facts": facts,
        "page_anchor_count": len(pages),
        "batch_blocks": batch_blocks,
        "has_handbook": has_handbook,
        "has_vtop": has_vtop,
        "has_sfdut": has_sfdut,
        "has_label_candidate": has_label_candidate,
        "regulated": regulated,
        "executable_signals": executable_signals,
        "status": status,
        "evidence_status": evidence_status,
        "tag": tag,
        "gold_use": gold_use,
    }


def availability_section(p):
    source_line = ", ".join(p["sources"]) if p["sources"] else "未识别"
    block_line = ", ".join(p["batch_blocks"]) if p["batch_blocks"] else "无批处理增强块"
    if p["status"] == "regulatory_boundary_page":
        usable = "本页主要用于禁用、限用、监管和越界识别；不得作为正向处方来源。"
    elif p["status"] == "source_anchored_drug_evidence_page":
        usable = "本页已具备来源锚定的药物证据，可用于药物召回、处方候选、配伍/禁忌提示、剂量或疗程事实定位。"
    elif p["status"] == "partial_drug_evidence_page":
        usable = "本页只有部分来源锚定证据，可用于药物召回、边界提示和后续标签核验任务规划。"
    else:
        usable = "本页仍是药物占位页，仅可用于实体召回和后续抽取任务规划。"

    if p["status"] == "regulatory_boundary_page":
        exec_note = "- 本页用于阻断或限制越界用药；正向治疗方案必须转到具体药物页、产品标签、处方规则和当地法规来源。"
    elif p["executable_signals"]:
        exec_note = (
            "- 页面含剂量、疗程、给药途径、休药期或处方候选信号；实际回答必须逐条保留来源页码，"
            "并复核靶动物、产品/剂型、适应证、处方管理、休药期/MRL、禁停用和当地法规。"
        )
    else:
        exec_note = (
            "- 页面不具备可执行处方条件；不得从药物名、类别或教材候选外推出剂量、疗程、休药期、MRL 或食品安全结论。"
        )
    return "\n".join([
        "## 药物知识页可用性",
        "",
        f"- 页面状态：{p['status']}；`evidence_status={p['evidence_status']}`；`gold_dataset_use={p['gold_use']}`。",
        f"- 可用边界：{usable}",
        f"- 来源覆盖：{source_line}；页码锚点：{p['page_anchor_count']}；批处理增强块：{block_line}。",
        f"- 已识别事实锚点：{len(p['facts'])} 条。",
        exec_note,
        "- 新增或改写药物事实必须保留 `source_id/fact_id/page` 或等价锚点；缺失字段不得由模型猜测补全。",
        "",
    ])


def normalize_body(body, p):
    section = availability_section(p)
    body = re.sub(r"\n?## 药物知识页可用性\n\n.*?(?=^## |\Z)", "\n", body, flags=re.S | re.M)
    body = re.sub(r"\n{3,}", "\n\n", body).lstrip()
    # Put the unified section after the title and any immediate evidence-status block if present.
    m = re.search(r"^# .+\n", body, flags=re.M)
    if not m:
        return section + "\n" + body.rstrip() + "\n"
    insert_pos = m.end()
    status_block = re.search(r"\A(.*?^## 证据状态\n\n.*?)(?=^## |\Z)", body, flags=re.S | re.M)
    if status_block:
        insert_pos = status_block.end()
    return (body[:insert_pos].rstrip() + "\n\n" + section + "\n" + body[insert_pos:].lstrip()).rstrip() + "\n"


def update_index(items):
    if not DRUG_INDEX.exists():
        return False
    rows = list(csv.DictReader(DRUG_INDEX.open("r", encoding="utf-8-sig", newline="")))
    if not rows:
        return False
    by_rel = {f"wiki/drugs/{x['file']}": x for x in items}
    changed = False
    for row in rows:
        rel = row.get("page_relpath", "")
        item = by_rel.get(rel)
        if not item:
            continue
        if row.get("status") != item["status"]:
            row["status"] = item["status"]
            changed = True
        srcs = ";".join(item["sources"])
        if "sources" in row and row.get("sources") != srcs:
            row["sources"] = srcs
            changed = True
        if "updated" in row and row.get("updated") != UPDATED:
            row["updated"] = UPDATED
            changed = True
    if changed:
        with DRUG_INDEX.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    return changed


def main():
    items = []
    for path in sorted(DRUG_DIR.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        meta, body = split_front_matter(original)
        p = profile(original, meta)

        tags = parse_list(meta.get("tags", "[]"))
        tags = [t for t in tags if t not in {"v5", "v7", "v11_label_candidate", "v13_1", "evidence_only", "china_regulated", "drug_evidence_page", "partial_drug_evidence_page", "regulatory_boundary_page", "drug_stub_page"}]
        for tag in ["drug", "swine", p["tag"], "cleaned_v13_2"]:
            if tag not in tags:
                tags.append(tag)
        meta["tags"] = list_value(tags)
        meta["updated"] = UPDATED
        meta["evidence_status"] = p["evidence_status"]
        meta["gold_dataset_use"] = p["gold_use"]
        meta["drug_page_status"] = p["status"]
        meta_sources = source_like_ids(meta.get("sources", ""))
        meta["sources"] = list_value(sorted(set(meta_sources + p["sources"])))
        if p["regulated"] and "jurisdiction" not in meta:
            meta["jurisdiction"] = "China"

        new_body = normalize_body(body, p)
        new_text = render_front_matter(meta) + "\n" + new_body
        if new_text != original:
            path.write_text(new_text, encoding="utf-8")

        items.append({
            "file": path.name,
            "drug_id": meta.get("drug_id", path.stem),
            "status": p["status"],
            "evidence_status": p["evidence_status"],
            "gold_use": p["gold_use"],
            "sources": parse_list(meta["sources"]),
            "fact_count": len(p["facts"]),
            "page_anchor_count": p["page_anchor_count"],
            "batch_blocks": p["batch_blocks"],
            "regulated": p["regulated"],
            "executable_signals": p["executable_signals"],
        })

    index_changed = update_index(items)
    by_status = {}
    for x in items:
        by_status[x["status"]] = by_status.get(x["status"], 0) + 1
    SUMMARY_JSON.write_text(json.dumps({
        "total_pages": len(items),
        "by_status": by_status,
        "drug_index_updated": index_changed,
        "pages": items,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Drug Entity Page Cleanup / 2026-05-08",
        "",
        f"- Drug pages processed: {len(items)}",
        f"- Status counts: {by_status}",
        f"- Drug index updated: {index_changed}",
        "- Scope: front matter, unified drug-page availability boundaries, source normalization, and drug index status.",
        "- Guardrail: existing drug facts, citations, source_id/fact_id/page anchors, and batch evidence blocks were preserved.",
        "",
        "## Pages",
        "",
    ]
    for x in items:
        lines.append(
            f"- `{x['file']}`: {x['status']}; evidence={x['evidence_status']}; "
            f"sources={','.join(x['sources'])}; facts={x['fact_count']}; pages={x['page_anchor_count']}; blocks={len(x['batch_blocks'])}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "processed": len(items),
        "by_status": by_status,
        "drug_index_updated": index_changed,
        "report": str(REPORT.relative_to(ROOT)),
        "summary": str(SUMMARY_JSON.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
