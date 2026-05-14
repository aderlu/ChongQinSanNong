from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
RAW_JSON = ROOT / "raw" / "web" / "web_access_dis033_vesicular_stomatitis_20260511" / "SRC-DIS033-VS-WEB-20260511.json"
DISEASE_PAGE = ROOT / "wiki" / "diseases" / "DIS-033-vesicular-stomatitis-viruses.md"
SOURCE_DIR = ROOT / "wiki" / "sources"
SOURCE_INDEX = ROOT / "exports" / "source_index.csv"
FACTS_JSON = ROOT / "exports" / "knowledge_facts.json"
ISSUES = ROOT / "issues"
UPDATED = "2026-05-11T16:45:00+08:00"
TZ = timezone(timedelta(hours=8))

SOURCE_ID = "A0-USDA-APHIS-VS-2026"
ALLOWED_SUFFIXES = ("aphis.usda.gov", "usda.gov")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def load_raw() -> dict[str, object]:
    payload = json.loads(read_text(RAW_JSON))
    required = ["source_id", "disease_id", "accessed_at", "official_sources", "supported_claims", "do_not_extrapolate"]
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise ValueError(f"raw evidence missing required fields: {missing}")
    if payload["source_id"] != "SRC-DIS033-VS-WEB-20260511":
        raise ValueError("unexpected raw source_id")
    if payload["disease_id"] != "DIS-033":
        raise ValueError("unexpected disease_id")
    sources = payload.get("official_sources")
    if not isinstance(sources, list) or len(sources) != 1:
        raise ValueError("official_sources must contain exactly one APHIS evidence page")
    source = sources[0]
    if not isinstance(source, dict):
        raise ValueError("official_sources[0] must be an object")
    url = str(source.get("url", ""))
    domain = urlparse(url).netloc.lower()
    if not source.get("official_domain_confirmed"):
        raise ValueError(f"official_domain_confirmed is false for {url}")
    if not any(domain == suffix or domain.endswith("." + suffix) for suffix in ALLOWED_SUFFIXES):
        raise ValueError(f"non-official domain rejected: {url}")
    return payload


def source_page_text(source: dict[str, object]) -> str:
    claims = "\n".join(f"- {item}" for item in source.get("explicit_dis033_support", []))
    limits = "\n".join(f"- {item}" for item in source.get("limitations", []))
    return f"""---
tags: [source, swine, authority, official, usda, aphis, vesicular_stomatitis]
source_id: {SOURCE_ID}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
source_status: source_anchored
authority_level: A0
url: {source.get('url', '')}
---

# USDA APHIS Vesicular Stomatitis Virus Official Disease Alert

## Source

- URL: {source.get('url', '')}
- Publisher: {source.get('publisher', '')}
- Page type: {source.get('page_type', '')}
- Last modified: {source.get('last_modified', '')}
- Accessed at: 2026-05-11
- Official domain confirmed: {source.get('domain', '')} / parent={source.get('parent_official_domain', '')}

## Supported Conclusions

{claims}

## Do Not Extrapolate

{limits}
"""


def ensure_source_page(raw: dict[str, object]) -> Path:
    source = raw["official_sources"][0]
    path = SOURCE_DIR / f"{SOURCE_ID}.md"
    write_text(path, source_page_text(source))
    return path


def read_source_index() -> list[dict[str, str]]:
    with SOURCE_INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_source_index(rows: list[dict[str, str]]) -> None:
    fieldnames = ["source_id", "title", "pages", "evidence_status", "relpath"]
    with SOURCE_INDEX.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def ensure_source_index(raw: dict[str, object], relpath: str) -> None:
    source = raw["official_sources"][0]
    rows = read_source_index()
    by_id = {row.get("source_id", ""): row for row in rows}
    by_id[SOURCE_ID] = {
        "source_id": SOURCE_ID,
        "title": str(source.get("title", SOURCE_ID)),
        "pages": str(source.get("url", "")),
        "evidence_status": "HUMAN_REVIEWED",
        "relpath": relpath,
    }
    write_source_index(list(by_id.values()))


def fact_rows(raw: dict[str, object]) -> list[dict[str, object]]:
    raw_relpath = RAW_JSON.relative_to(ROOT).as_posix()
    target_page = "wiki/diseases/DIS-033-vesicular-stomatitis-viruses.md"
    rows = []
    for claim in raw["supported_claims"]:
        if not isinstance(claim, dict):
            raise ValueError("supported_claims items must be objects")
        text = str(claim.get("claim", "")).strip()
        fact_id = str(claim.get("fact_id", "")).strip()
        if not fact_id or not text:
            raise ValueError(f"invalid claim row: {claim}")
        rows.append(
            {
                "fact_id": fact_id,
                "fact_type": "official_web_access_claim",
                "subject": "Vesicular stomatitis in swine",
                "predicate": "official_aphis_supported_boundary_or_fact",
                "object": text,
                "fact_confidence": "0.88",
                "evidence_source": SOURCE_ID,
                "evidence_source_id": SOURCE_ID,
                "evidence_url": str(claim.get("supporting_source_url", "")),
                "evidence_quote_span": "raw supported_claims; raw_json=" + raw_relpath,
                "evidence_status": "HUMAN_REVIEWED",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "United States / official source scope",
                "target_page": target_page,
            }
        )
    return rows


def upsert_facts(new_facts: list[dict[str, object]]) -> int:
    facts = json.loads(read_text(FACTS_JSON))
    by_id = {fact.get("fact_id"): idx for idx, fact in enumerate(facts) if isinstance(fact, dict)}
    changed = 0
    for fact in new_facts:
        fact_id = fact["fact_id"]
        if fact_id in by_id:
            if facts[by_id[fact_id]] != fact:
                facts[by_id[fact_id]] = fact
                changed += 1
        else:
            facts.append(fact)
            changed += 1
    write_text(FACTS_JSON, json.dumps(facts, ensure_ascii=False, indent=2) + "\n")
    return changed


def update_frontmatter_sources(text: str, source_ids: list[str]) -> str:
    match = re.search(r"^sources:\s*\[(.*?)\]\s*$", text, re.M)
    if not match:
        return text
    current = [item.strip() for item in match.group(1).split(",") if item.strip()]
    for source_id in source_ids:
        if source_id not in current:
            current.append(source_id)
    replacement = "sources: [" + ", ".join(current) + "]"
    return text[: match.start()] + replacement + text[match.end() :]


def update_disease_page(raw: dict[str, object], fact_ids: list[str]) -> None:
    text = read_text(DISEASE_PAGE)
    text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
    text = update_frontmatter_sources(text, [SOURCE_ID])
    source = raw["official_sources"][0]
    fact_lines = "\n".join(f"- `{fact_id}`" for fact_id in fact_ids)
    limits = raw.get("do_not_extrapolate", [])
    limit_lines = "\n".join(f"- {item}" for item in limits)
    section = f"""## Web Access official source ingest / 2026-05-11

### Source

- `{SOURCE_ID}`: {source.get('url', '')}
- Authority: USDA APHIS official disease alert; official domain confirmed through Web Access.
- Last modified on source page: {source.get('last_modified', '')}

### Facts

{fact_lines}

### Governance boundary

{limit_lines}

- This update adds source-anchored host, transmission, lesion, U.S. reporting-boundary, and movement/trade impact facts only.
- It does not add treatment, dose, course, withdrawal period, MRL, residue, food-safety, China-specific reporting, quarantine, culling, or movement-control conclusions.
"""
    heading = "## Web Access official source ingest / 2026-05-11"
    if heading in text:
        text = re.sub(r"\n## Web Access official source ingest / 2026-05-11\n.*?(?=\n## |\Z)", "\n" + section.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + section
    write_text(DISEASE_PAGE, text)


def run_status_standardization() -> None:
    script = ROOT / "tools" / "standardize_source_fact_status.py"
    result = subprocess.run([sys.executable, str(script)], cwd=ROOT.parents[1], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:] or result.stdout[-2000:])


def write_ingest_log(summary: dict[str, object]) -> None:
    ISSUES.mkdir(parents=True, exist_ok=True)
    json_path = ISSUES / "dis033_vesicular_stomatitis_web_access_ingest_2026-05-11.json"
    md_path = ISSUES / "dis033_vesicular_stomatitis_web_access_ingest_2026-05-11.md"
    write_text(json_path, json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# DIS-033 Vesicular Stomatitis Web Access Formal Ingest",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Raw JSON: `{summary['raw_json']}`",
        f"- Source registered: `{SOURCE_ID}`",
        f"- Facts changed: {summary['facts_changed']}",
        f"- Disease page: `{summary['disease_page']}`",
        "",
        "## Boundary",
        "",
        "- Only explicit APHIS official-source statements were registered.",
        "- No treatment, dose, course, withdrawal period, MRL, residue, food-safety, China-specific regulatory action, quarantine, culling, or movement-control conclusion was added.",
    ]
    write_text(md_path, "\n".join(lines) + "\n")


def main() -> None:
    raw = load_raw()
    source_path = ensure_source_page(raw)
    ensure_source_index(raw, source_path.relative_to(ROOT).as_posix())
    facts = fact_rows(raw)
    facts_changed = upsert_facts(facts)
    update_disease_page(raw, [fact["fact_id"] for fact in facts])
    run_status_standardization()
    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "raw_json": RAW_JSON.relative_to(ROOT).as_posix(),
        "source_id": SOURCE_ID,
        "source_page": source_path.relative_to(ROOT).as_posix(),
        "facts_changed": facts_changed,
        "fact_ids": [fact["fact_id"] for fact in facts],
        "disease_page": DISEASE_PAGE.relative_to(ROOT).as_posix(),
        "boundary": "No treatment, dose, course, withdrawal, MRL, food-safety, China-specific regulatory action, quarantine, culling, or movement-control conclusion added.",
    }
    write_ingest_log(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
