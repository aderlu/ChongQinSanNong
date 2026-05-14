from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
OUT = WIKI / "exports" / "balanced_task_use_index.csv"
REPORT = WIKI / "issues" / "balanced_task_use_policy_report_2026-05-08.json"

SOURCE_RE = re.compile(r"\b(?:A0-[A-Z0-9-]+|A1-[A-Z0-9-]+|A2-[A-Z0-9-]+|SRC-\d{4}|RC-[A-Z0-9-]+|RULE-[A-Z0-9-]+)\b")
EXECUTABLE_RE = re.compile(
    r"(?:剂量|用量|疗程|休药|停药|withdrawal|MRL|残留|可食|出栏|上市|销售|扑杀|调运|检疫|无害化|强制免疫)",
    re.I,
)


def front_matter(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.M)
    return match.group(1).strip() if match else ""


def entity_title(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.M)
    return match.group(1).strip() if match else fallback


def source_ids(text: str) -> set[str]:
    return set(SOURCE_RE.findall(text))


def task_use(entity_type: str, text: str) -> tuple[str, str]:
    ids = source_ids(text)
    evidence_status = front_matter(text, "evidence_status")
    gold_role = front_matter(text, "gold_dataset_use")
    has_authority = any(item.startswith(("A0-", "A1-")) for item in ids)
    has_src_or_secondary = any(item.startswith(("A2-", "SRC-", "RC-", "RULE-")) for item in ids)
    has_executable = bool(EXECUTABLE_RE.search(text))

    if not ids:
        return "blocked", "no qualified source id found"
    if entity_type == "drug":
        if "positive_label_candidate" in gold_role and has_authority:
            return "train_ready", "positive label candidate with authority/label source"
        if has_executable and not has_authority:
            return "generation_ready_limited", "executable drug claim requires label/authority source"
        if evidence_status == "HUMAN_REVIEWED" or has_src_or_secondary:
            return "generation_ready_limited", "qualified source available for bounded drug discussion"
        return "retrieval_only", "drug page has weak source signal"

    if has_executable and not has_authority:
        return "generation_ready_limited", "executable disease/regulatory claim requires authority source"
    if evidence_status == "HUMAN_REVIEWED" and len(ids) >= 3:
        return "train_ready", "reviewed page with multiple qualified anchors"
    if len(ids) >= 2:
        return "generation_ready_limited", "qualified sources support bounded clinical generation"
    return "retrieval_only", "single-source page should be used for recall/context"


def iter_entities() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entity_type, subdir in [("disease", "diseases"), ("drug", "drugs")]:
        for path in sorted((WIKI / "wiki" / subdir).glob("*.md")):
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            use, reason = task_use(entity_type, text)
            ids = sorted(source_ids(text))
            rows.append(
                {
                    "entity_type": entity_type,
                    "entity_id": front_matter(text, f"{entity_type}_id") or path.stem.split("-", 1)[0],
                    "title": entity_title(text, path.stem),
                    "task_use": use,
                    "reason": reason,
                    "evidence_status": front_matter(text, "evidence_status"),
                    "gold_dataset_use": front_matter(text, "gold_dataset_use"),
                    "qualified_source_count": str(len(ids)),
                    "has_authority_source": str(any(item.startswith(("A0-", "A1-")) for item in ids)),
                    "has_executable_terms": str(bool(EXECUTABLE_RE.search(text))),
                    "page_relpath": path.relative_to(WIKI).as_posix(),
                    "source_ids": ";".join(ids),
                }
            )
    return rows


def main() -> None:
    rows = iter_entities()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "entity_type",
        "entity_id",
        "title",
        "task_use",
        "reason",
        "evidence_status",
        "gold_dataset_use",
        "qualified_source_count",
        "has_authority_source",
        "has_executable_terms",
        "page_relpath",
        "source_ids",
    ]
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    by_type: dict[str, dict[str, int]] = {}
    for row in rows:
        counts[row["task_use"]] = counts.get(row["task_use"], 0) + 1
        bucket = by_type.setdefault(row["entity_type"], {})
        bucket[row["task_use"]] = bucket.get(row["task_use"], 0) + 1
    REPORT.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "policy": "balanced_source_use_v16",
                "index": str(OUT),
                "rows": len(rows),
                "task_use_counts": counts,
                "task_use_counts_by_entity_type": by_type,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"index": str(OUT), "report": str(REPORT), "task_use_counts": counts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
