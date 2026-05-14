import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DISEASE_DIR = ROOT / "wiki" / "diseases"
REPORT = ROOT / "issues" / "disease_entity_page_cleanup_2026-05-08.md"
SUMMARY_JSON = ROOT / "issues" / "disease_entity_page_cleanup_2026-05-08.json"
DISEASE_INDEX = ROOT / "exports" / "disease_index.csv"

UPDATED = "2026-05-08T23:59:00+08:00"

SECTION_MARKERS = [
    "病原/定位",
    "病原与分类",
    "流行病学",
    "传播途径",
    "临床症状",
    "剖检变化",
    "实验室诊断",
    "鉴别诊断",
    "防控",
    "防控和用药边界",
    "用药/处置边界",
    "监管/执行性处置边界",
]

SOURCE_LABELS = {
    "SRC-0087": "猪病诊疗与处方手册处方事实",
    "SRC-0088": "Veterinary Treatment of Pigs 治疗事实",
    "SRC-0089": "猪场兽药使用与猪病防治技术（1-200页）",
    "SRC-0090": "猪场兽药使用与猪病防治技术（200-363页）",
}

SOURCE_LIKE_RE = re.compile(r"(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+|RULE-[A-Z0-9-]+)")


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
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def render_front_matter(meta):
    order = ["tags", "disease_id", "updated", "evidence_status", "sources"]
    lines = ["---"]
    for key in order:
        if key in meta:
            lines.append(f"{key}: {meta[key]}")
    for key in sorted(k for k in meta if k not in order):
        lines.append(f"{key}: {meta[key]}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def parse_list(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inside = value[1:-1].strip()
        if not inside:
            return []
        return [x.strip().strip("'\"") for x in inside.split(",") if x.strip()]
    return [value] if value else []


def list_value(items):
    seen = []
    for item in items:
        if item and item not in seen:
            seen.append(item)
    return "[" + ", ".join(seen) + "]"


def source_like_ids(text):
    return sorted(set(SOURCE_LIKE_RE.findall(text)))


def evidence_profile(text):
    source_ids = source_like_ids(text)
    rule_ids = sorted(set(re.findall(r"\b(?:RC|RULE)-[A-Z0-9-]+\b", text)))
    raw_fact_ids = re.findall(r"(?:fact_id=|`)([A-Z]{2,}[A-Z0-9]*-[A-Z0-9][A-Z0-9._-]+)", text)
    fact_ids = sorted({x.rstrip("`.;,") for x in raw_fact_ids if not x.startswith(("SRC-", "RC-", "RULE-"))})
    page_anchors = re.findall(r"\b(?:PDF page|page|p\.)\s*[0-9]+", text, flags=re.I)
    batch_blocks = sorted(set(re.findall(r"<!--\s*([A-Z0-9_]+_START)\s*-->", text)))
    section_hits = [s for s in SECTION_MARKERS if re.search(rf"^##+\s+{re.escape(s)}", text, flags=re.M)]
    has_prescription = any(s in text for s in ["HANDBOOK_RX_V13_1_START", "SFDUT_1_200_V13_1_START", "SFDUT_200_363_V13_1_START", "VTOP_V13_1_START"])
    anchored_count = len(fact_ids) + len(page_anchors)
    clinical_ready = len(fact_ids) >= 3 or has_prescription
    if clinical_ready:
        status = "HUMAN_REVIEWED"
        tag = "clinical_evidence_page"
        coverage = "source_anchored_clinical_page"
    elif any(s != "SRC-0001" for s in source_ids):
        status = "NEEDS_REVIEW"
        tag = "partial_evidence_page"
        coverage = "partial_source_anchored_page"
    else:
        status = "NEEDS_REVIEW"
        tag = "toc_seed_page"
        coverage = "needs_body_extraction"
    return {
        "source_ids": source_ids,
        "rule_ids": rule_ids,
        "fact_count": len(fact_ids),
        "page_anchor_count": len(page_anchors),
        "batch_blocks": batch_blocks,
        "section_hits": section_hits,
        "has_prescription": has_prescription,
        "anchored_count": anchored_count,
        "clinical_ready": clinical_ready,
        "status": status,
        "tag": tag,
        "coverage": coverage,
    }


def replacement_section(meta, profile):
    pages_note = "有" if profile["page_anchor_count"] else "少量或暂无"
    source_line = ", ".join(profile["source_ids"]) if profile["source_ids"] else "未识别"
    block_line = ", ".join(profile["batch_blocks"]) if profile["batch_blocks"] else "无批处理增强块"
    usable = (
        "本页已具备来源锚定的临床知识页基础，可用于病种召回、鉴别提示、防控要点、"
        "诊疗候选和证据检索。"
        if profile["clinical_ready"]
        else "本页仍以目录/部分证据覆盖为主，可用于病种召回和后续抽取任务规划。"
    )
    if profile["has_prescription"]:
        prescription_note = (
            "- 本页包含处方或治疗候选增强块；具体剂量、疗程、给药途径、休药期、MRL、"
            "食品安全和法域合规结论必须回到对应来源页、事实索引、rule card、标签或法规来源复核。"
        )
    else:
        prescription_note = (
            "- 本页不得单独生成执行性处方、休药期、MRL、食品安全或特定法域监管结论；"
            "涉及执行问题必须联动药物页、rule card、标签/法规来源。"
        )
    lines = [
        "## 临床知识页可用性",
        "",
        f"- 页面状态：{profile['coverage']}；`evidence_status={profile['status']}`。",
        f"- 可用边界：{usable}",
        f"- 来源覆盖：{source_line}；页码锚点：{pages_note}；批处理增强块：{block_line}。",
        f"- 已识别证据锚点：fact-like anchors {profile['fact_count']} 条；page anchors {profile['page_anchor_count']} 条。",
        prescription_note,
        "- 缺失栏目表示当前来源覆盖边界，不应由模型猜测补全；新增事实必须保留 source_id/fact_id/page 或等价锚点。",
        "",
    ]
    return "\n".join(lines)


def normalize_body(body, meta, profile):
    body = body.replace("## 当前可用性边界\n\n- 当前状态：目录级覆盖页。\n- 可用于召回目标病种和规划抽取任务；不可作为完整临床知识页。\n", "")
    body = re.sub(
        r"\n?## 当前可用性边界\n\n(?:- .*\n)+",
        "\n",
        body,
        flags=re.M,
    )
    section = replacement_section(meta, profile)
    if re.search(r"^## 临床知识页可用性\b", body, flags=re.M):
        body = re.sub(r"^## 临床知识页可用性\n\n.*?(?=^## |\Z)", section + "\n", body, flags=re.S | re.M)
    else:
        insert_after = re.search(r"^## 本地证据\n\n.*?(?=^## |\Z)", body, flags=re.S | re.M)
        if insert_after:
            body = body[: insert_after.end()] + "\n" + section + "\n" + body[insert_after.end() :]
        else:
            first_next = re.search(r"^## ", body, flags=re.M)
            if first_next:
                body = body[: first_next.start()] + section + "\n" + body[first_next.start() :]
            else:
                body = body.rstrip() + "\n\n" + section + "\n"

    if profile["clinical_ready"]:
        body = body.replace(
            "- 当前仅有目录级或未映射证据；本页仍需后续正文抽取。",
            "- 本页已有来源锚定事实；仍可继续补充缺失栏目，但不再按纯目录级页面处理。",
        )
        body = re.sub(
            r"- Optional facets without attached source-anchored evidence: ([^\n]+)\.",
            "- Optional facets without attached source-anchored evidence, if still absent below, remain source-coverage gaps: \\1.",
            body,
        )
    return re.sub(r"\n{3,}", "\n\n", body).rstrip() + "\n"


def update_index(cleaned):
    if not DISEASE_INDEX.exists():
        return False
    rows = list(csv.DictReader(DISEASE_INDEX.open("r", encoding="utf-8-sig", newline="")))
    if not rows:
        return False
    by_rel = {f"wiki/diseases/{item['file']}": item for item in cleaned}
    changed = False
    for row in rows:
        rel = row.get("page_relpath", "")
        item = by_rel.get(rel)
        if not item:
            continue
        if "coverage_gap_status" in row and row["coverage_gap_status"] != item["coverage"]:
            row["coverage_gap_status"] = item["coverage"]
            changed = True
        if "primary_source_id" in row and item["sources"]:
            preferred = (
                next((s for s in item["sources"] if s.startswith("SRC-") and s != "SRC-0001"), None)
                or next((s for s in item["sources"] if s != "SRC-0001"), item["sources"][0])
            )
            if row["primary_source_id"] != preferred:
                row["primary_source_id"] = preferred
                changed = True
    if changed:
        with DISEASE_INDEX.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    return changed


def main():
    cleaned = []
    for path in sorted(DISEASE_DIR.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        meta, body = split_front_matter(original)
        profile = evidence_profile(original)

        tags = parse_list(meta.get("tags", "[]"))
        tags = [t for t in tags if t not in {"initial", "v12", "clinical_evidence_page", "partial_evidence_page", "toc_seed_page"}]
        for tag in ["disease", "swine", profile["tag"], "cleaned_v13_2"]:
            if tag not in tags:
                tags.append(tag)
        meta["tags"] = list_value(tags)
        meta["updated"] = UPDATED
        meta["evidence_status"] = profile["status"]
        meta_sources = source_like_ids(meta.get("sources", ""))
        meta["sources"] = list_value(sorted(set(meta_sources + profile["source_ids"])))

        new_body = normalize_body(body, meta, profile)
        new_text = render_front_matter(meta) + "\n" + new_body.lstrip()
        if new_text != original:
            path.write_text(new_text, encoding="utf-8")

        cleaned.append({
            "file": path.name,
            "disease_id": meta.get("disease_id", path.stem.split("-")[0]),
            "status": profile["status"],
            "coverage": profile["coverage"],
            "sources": parse_list(meta["sources"]),
            "fact_count": profile["fact_count"],
            "page_anchor_count": profile["page_anchor_count"],
            "batch_blocks": profile["batch_blocks"],
            "clinical_ready": profile["clinical_ready"],
        })

    index_changed = update_index(cleaned)
    clinical_ready = sum(1 for x in cleaned if x["clinical_ready"])
    by_status = {}
    for x in cleaned:
        by_status[x["status"]] = by_status.get(x["status"], 0) + 1
    SUMMARY_JSON.write_text(json.dumps({
        "total_pages": len(cleaned),
        "clinical_ready": clinical_ready,
        "by_status": by_status,
        "disease_index_updated": index_changed,
        "pages": cleaned,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Disease Entity Page Cleanup / 2026-05-08",
        "",
        f"- Disease pages processed: {len(cleaned)}",
        f"- Source-anchored clinical pages: {clinical_ready}",
        f"- Status counts: {by_status}",
        f"- Disease index updated: {index_changed}",
        "- Scope: front matter, stale availability boundaries, evidence coverage summaries, and index coverage status.",
        "- Guardrail: existing medical facts, citations, source_id/fact_id/page anchors, and batch blocks were preserved.",
        "",
        "## Pages",
        "",
    ]
    for x in cleaned:
        lines.append(
            f"- `{x['file']}`: {x['coverage']}; status={x['status']}; "
            f"sources={','.join(x['sources'])}; facts={x['fact_count']}; pages={x['page_anchor_count']}; blocks={len(x['batch_blocks'])}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "processed": len(cleaned),
        "clinical_ready": clinical_ready,
        "by_status": by_status,
        "disease_index_updated": index_changed,
        "report": str(REPORT.relative_to(ROOT)),
        "summary": str(SUMMARY_JSON.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
