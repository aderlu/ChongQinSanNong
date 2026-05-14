from __future__ import annotations

import json
import re
import statistics
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"


# Entity pages are not required to contain textbook-style clinical facets.
# Those facets are evidence-driven optional dimensions because MOA/regulatory
# sources often do not cover them.
CORE_SECTIONS: list[str] = []
OPTIONAL_FACETS = [
    "\u4f20\u64ad\u9014\u5f84",
    "\u4e34\u5e8a\u75c7\u72b6",
    "\u5256\u68c0\u53d8\u5316",
    "\u5b9e\u9a8c\u5ba4\u8bca\u65ad",
    "\u9274\u522b\u8bca\u65ad",
    "\u9632\u63a7\u8981\u70b9",
]
SOURCE_RE = re.compile(r"\b(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+)\b|source_id=|fact_id=|https?://")
SOURCE_ID_RE = re.compile(r"\b(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+|RULE-[A-Z0-9-]+)\b")
PLACEHOLDER_TOKENS = [
    "\u5f85\u6b63\u6587\u62bd\u53d6",
    "\u6682\u65e0\u53ef\u81ea\u52a8\u6620\u5c04",
    "\u5f85\u590d\u6838",
    "\u4e0d\u53ef\u4f5c\u4e3a\u5b8c\u6574\u4e34\u5e8a\u77e5\u8bc6\u9875",
    "\u4e0d\u5f97\u7f16\u9020",
]


def section_body(text: str, heading: str, level: str = "##") -> str:
    match = re.search(
        rf"^{re.escape(level)} {re.escape(heading)}\s*\n(.*?)(?=\n{re.escape(level)} |\Z)",
        text,
        flags=re.S | re.M,
    )
    return match.group(1).strip() if match else ""


def sourced(body: str) -> bool:
    return bool(SOURCE_RE.search(body))


def placeholder(body: str) -> bool:
    return (not body) or any(token in body for token in PLACEHOLDER_TOKENS)


def front_matter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.M)
    return match.group(1).strip() if match else ""


def source_ids(text: str) -> set[str]:
    return set(SOURCE_ID_RE.findall(text))


def disease_task_use(text: str) -> str:
    ids = source_ids(text)
    status = front_matter_value(text, "evidence_status")
    if not ids:
        return "blocked"
    if status == "HUMAN_REVIEWED" and len(ids) >= 3:
        return "train_ready"
    if len(ids) >= 2:
        return "generation_ready_limited"
    return "retrieval_only"


def drug_task_use(text: str) -> str:
    ids = source_ids(text)
    role = front_matter_value(text, "gold_dataset_use")
    status = front_matter_value(text, "evidence_status")
    has_authority = any(item.startswith(("A0-", "A1-")) for item in ids)
    if not ids:
        return "blocked"
    if "positive_label_candidate" in role and has_authority:
        return "train_ready"
    if status == "HUMAN_REVIEWED" or len(ids) >= 2:
        return "generation_ready_limited"
    return "retrieval_only"


def csv_group_counts(path: Path, column: str) -> dict[str, int]:
    if not path.exists():
        return {}
    counts: dict[str, int] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            value = (row.get(column) or "").strip() or "<blank>"
            counts[value] = counts.get(value, 0) + 1
    return counts


def main() -> None:
    disease_pages = sorted((WIKI / "wiki" / "diseases").glob("*.md"))
    facts_path = WIKI / "exports" / "knowledge_facts.json"
    facts = json.loads(facts_path.read_text(encoding="utf-8-sig")) if facts_path.exists() else []
    source_anchored = [
        fact
        for fact in facts
        if fact.get("evidence_source_id") and (fact.get("evidence_quote_span") or fact.get("evidence_url"))
    ]

    disease_gaps: list[dict[str, object]] = []
    section_counts = {section: {"sourced": 0, "placeholder": 0} for section in CORE_SECTIONS}
    optional_facet_counts = {section: {"sourced": 0, "gap": 0} for section in OPTIONAL_FACETS}
    lengths: list[int] = []

    for page in disease_pages:
        text = page.read_text(encoding="utf-8-sig", errors="replace")
        lengths.append(len(text))
        gaps: list[str] = []

        for section in CORE_SECTIONS:
            body = section_body(text, section)
            if sourced(body):
                section_counts[section]["sourced"] += 1
            if placeholder(body):
                section_counts[section]["placeholder"] += 1
                gaps.append(section)

        optional_block = section_body(text, "Evidence-backed optional facets")
        gap_block = section_body(text, "Evidence gaps")
        for section in OPTIONAL_FACETS:
            facet_body = section_body(optional_block, section, level="###")
            if sourced(facet_body):
                optional_facet_counts[section]["sourced"] += 1
            if section in gap_block:
                optional_facet_counts[section]["gap"] += 1

        disease_gaps.append({"page": page.name, "length": len(text), "core_gaps": gaps})

    disease_task_use_counts: dict[str, int] = {}
    for page in disease_pages:
        task_use = disease_task_use(page.read_text(encoding="utf-8-sig", errors="replace"))
        disease_task_use_counts[task_use] = disease_task_use_counts.get(task_use, 0) + 1

    drug_task_use_counts: dict[str, int] = {}
    for page in sorted((WIKI / "wiki" / "drugs").glob("*.md")):
        task_use = drug_task_use(page.read_text(encoding="utf-8-sig", errors="replace"))
        drug_task_use_counts[task_use] = drug_task_use_counts.get(task_use, 0) + 1

    small_dirs = {}
    for sub in ["drugs", "rule_cards", "syndromes", "synthesis", "topics"]:
        pages = sorted((WIKI / "wiki" / sub).glob("*.md"))
        lens = [len(p.read_text(encoding="utf-8-sig", errors="replace")) for p in pages]
        small_dirs[sub] = {
            "count": len(pages),
            "median_len": int(statistics.median(lens)) if lens else 0,
            "min_len": min(lens) if lens else 0,
        }

    report = {
        "disease_count": len(disease_pages),
        "fact_count": len(facts),
        "source_anchored_fact_count": len(source_anchored),
        "disease_length_median": int(statistics.median(lengths)) if lengths else 0,
        "disease_pages_under_2500_chars": sum(1 for length in lengths if length < 2500),
        "core_section_counts": section_counts,
        "optional_facet_counts": optional_facet_counts,
        "balanced_task_use_policy": {
            "train_ready": "usable for filtered SFT/evaluation when clinical claims are source-grounded; A0/A1 is required only for executable regulatory, label, withdrawal, MRL, slaughter, movement, culling, or food-safety claims",
            "generation_ready_limited": "usable for candidate generation with explicit boundaries and standard citations from any qualified source level",
            "retrieval_only": "usable for recall/context only, not direct answer claims",
            "blocked": "insufficient source signal",
        },
        "disease_task_use_counts": disease_task_use_counts,
        "drug_task_use_counts": drug_task_use_counts,
        "disease_index_coverage_gap_status_counts": csv_group_counts(WIKI / "exports" / "disease_index.csv", "coverage_gap_status"),
        "drug_gold_role_counts": csv_group_counts(WIKI / "exports" / "drug_gold_role_index.csv", "gold_dataset_use"),
        "drug_index_evidence_status_counts": csv_group_counts(WIKI / "exports" / "drug_gold_role_index.csv", "evidence_status"),
        "optional_facet_policy": (
            "\u4f20\u64ad\u9014\u5f84\u3001\u4e34\u5e8a\u75c7\u72b6\u3001\u5256\u68c0\u53d8\u5316\u3001"
            "\u5b9e\u9a8c\u5ba4\u8bca\u65ad\u3001\u9274\u522b\u8bca\u65ad\u548c\u9632\u63a7\u8981\u70b9"
            "\u4e3a\u8bc1\u636e\u9a71\u52a8\u53ef\u9009\u7ef4\u5ea6\uff1b\u7f3a\u53e3\u7edf\u8ba1\u4e0d\u4f5c\u4e3a\u5b9e\u4f53\u9875\u5931\u8d25\u9879\u3002"
        ),
        "small_dirs": small_dirs,
        "worst_disease_core_gaps": sorted(
            disease_gaps,
            key=lambda row: (len(row["core_gaps"]), -int(row["length"])),
            reverse=True,
        )[:25],
    }
    out = WIKI / "issues" / "dataset_readiness_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
