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
RAW_JSON = ROOT / "raw" / "web" / "web_access_dis008_ped_authority_20260511" / "SRC-DIS008-PED-WEB-20260511.json"
DISEASE_PAGE = ROOT / "wiki" / "diseases" / "DIS-008-porcine-epidemic-diarrhea-virus.md"
SOURCE_DIR = ROOT / "wiki" / "sources"
SOURCE_INDEX = ROOT / "exports" / "source_index.csv"
FACTS_JSON = ROOT / "exports" / "knowledge_facts.json"
EVIDENCE_EXPANSION = ROOT / "wiki" / "evidence_expansions" / "diseases" / "phase4_runtime_compaction" / "DIS-008-porcine-epidemic-diarrhea-virus" / "008-Web-Access-Authority-Reinforcement-2026-05-11.md"
ISSUES = ROOT / "issues"
UPDATED = "2026-05-11T17:25:00+08:00"
TZ = timezone(timedelta(hours=8))

SOURCE_IDS = ["A1-WOAH-PED", "A1-USDA-APHIS-PED-TECH-NOTE-2023"]
ALLOWED_SUFFIXES = ("woah.org", "aphis.usda.gov")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_raw() -> dict[str, object]:
    payload = json.loads(read_text(RAW_JSON))
    required = ["source_id", "disease_id", "accessed_at", "authority_sources", "supported_claims", "do_not_extrapolate"]
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise ValueError(f"raw evidence missing required fields: {missing}")
    if payload["source_id"] != "SRC-DIS008-PED-WEB-20260511":
        raise ValueError("unexpected raw source_id")
    if payload["disease_id"] != "DIS-008":
        raise ValueError("unexpected disease_id")
    sources = payload.get("authority_sources")
    if not isinstance(sources, list) or len(sources) < 2:
        raise ValueError("authority_sources must include WOAH and USDA APHIS evidence")
    seen_ids = {str(source.get("source_id", "")) for source in sources if isinstance(source, dict)}
    for source_id in SOURCE_IDS:
        if source_id not in seen_ids:
            raise ValueError(f"missing source {source_id}")
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("authority_sources items must be objects")
        url = str(source.get("url", ""))
        domain = urlparse(url).netloc.lower()
        if not source.get("domain_confirmed"):
            raise ValueError(f"domain_confirmed is false for {url}")
        if not any(domain == suffix or domain.endswith("." + suffix) for suffix in ALLOWED_SUFFIXES):
            raise ValueError(f"non-authority domain rejected: {url}")
    return payload


def source_by_id(raw: dict[str, object], source_id: str) -> dict[str, object]:
    for item in raw["authority_sources"]:
        if isinstance(item, dict) and item.get("source_id") == source_id:
            return item
    raise ValueError(f"source not found: {source_id}")


def source_page_text(source: dict[str, object]) -> str:
    source_id = str(source["source_id"])
    explicit = "\n".join(f"- {item}" for item in source.get("explicit_dis008_support", []))
    limitations = "\n".join(f"- {item}" for item in source.get("limitations", []))
    return f"""---
tags: [source, swine, authority, web_access, ped]
source_id: {source_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
source_status: source_anchored
authority_level: {source.get('authority_level_suggestion', 'A1')}
url: {source.get('url', '')}
---

# {source.get('title', source_id)}

## Source

- URL: {source.get('url', '')}
- Publisher: {source.get('publisher', '')}
- Page type: {source.get('page_type', '')}
- Accessed at: {source.get('accessed_at', '2026-05-11')}
- Domain confirmed: {source.get('domain', '')}
- Last modified header: {source.get('last_modified_header', '')}

## Supported Conclusions

{explicit}

## Do Not Extrapolate

{limitations}
"""


def ensure_source_page(source: dict[str, object]) -> Path:
    source_id = str(source["source_id"])
    path = SOURCE_DIR / f"{source_id}.md"
    if source_id == "A1-WOAH-PED" and path.exists():
        text = read_text(path)
        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        section = f"""## Web Access authority reinforcement / 2026-05-11

- Web Access rechecked the WOAH disease page for PED identity, non-zoonotic boundary, faecal-oral transmission, neonatal severity, clinical similarity to porcine gastroenteritis, strict biosecurity / early detection, no-specific-treatment boundary, and WOAH listed-disease boundary.
- This reinforcement supports `DIS008-WEB-001-woah-nonzoonotic-coronavirus`, `DIS008-WEB-002-woah-age-morbidity-mortality`, `DIS008-WEB-003-woah-fecal-oral-biosecurity-early-detection`, and `DIS008-WEB-004-woah-clinical-similarity-no-specific-treatment`.
- Do not extrapolate this international source into China-specific reporting, quarantine, culling, movement-control, farm-closure, vaccination schedule, dose, withdrawal, MRL, residue, or food-safety conclusions.
"""
        heading = "## Web Access authority reinforcement / 2026-05-11"
        if heading in text:
            text = re.sub(r"\n## Web Access authority reinforcement / 2026-05-11\n.*?(?=\n## |\Z)", "\n" + section.rstrip() + "\n", text, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + section
        write_text(path, text)
        return path
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


def ensure_source_index(raw: dict[str, object], relpaths: dict[str, str]) -> None:
    rows = read_source_index()
    by_id = {row.get("source_id", ""): row for row in rows}
    for source in raw["authority_sources"]:
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("source_id", ""))
        if source_id not in SOURCE_IDS:
            continue
        by_id[source_id] = {
            "source_id": source_id,
            "title": str(source.get("title", source_id)),
            "pages": str(source.get("url", "")),
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": relpaths[source_id],
        }
    write_source_index(list(by_id.values()))


def fact_rows(raw: dict[str, object]) -> list[dict[str, object]]:
    raw_relpath = RAW_JSON.relative_to(ROOT).as_posix()
    target_page = "wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md"
    rows = []
    for claim in raw["supported_claims"]:
        if not isinstance(claim, dict):
            raise ValueError("supported_claims items must be objects")
        fact_id = str(claim.get("fact_id", "")).strip()
        text = str(claim.get("claim", "")).strip()
        source_id = str(claim.get("supporting_source_id", "")).strip()
        if not fact_id or not text or source_id not in SOURCE_IDS:
            raise ValueError(f"invalid claim row: {claim}")
        rows.append(
            {
                "fact_id": fact_id,
                "fact_type": "authority_web_access_claim",
                "subject": "猪流行性腹泻",
                "predicate": "authority_supported_ped_boundary_or_fact",
                "object": text,
                "fact_confidence": "0.88",
                "evidence_source": source_id,
                "evidence_source_id": source_id,
                "evidence_url": str(claim.get("supporting_source_url", "")),
                "evidence_quote_span": "raw supported_claims; raw_json=" + raw_relpath,
                "evidence_status": "HUMAN_REVIEWED",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages_with_neonatal_high_risk",
                "jurisdiction": "International / US technical note scope",
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
    return text[: match.start()] + "sources: [" + ", ".join(current) + "]" + text[match.end() :]


def update_disease_page(raw: dict[str, object], fact_ids: list[str]) -> None:
    text = read_text(DISEASE_PAGE)
    text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
    text = update_frontmatter_sources(text, SOURCE_IDS)
    fact_lines = "\n".join(f"- `{fact_id}`" for fact_id in fact_ids)
    limit_lines = "\n".join(f"- {item}" for item in raw.get("do_not_extrapolate", []))
    section = f"""## Web Access authority source ingest / 2026-05-11

### Sources

- `A1-WOAH-PED`: https://www.woah.org/en/disease/porcine-epidemic-diarrhoea/
- `A1-USDA-APHIS-PED-TECH-NOTE-2023`: https://www.aphis.usda.gov/sites/default/files/ped_tech_note.pdf

### Facts

{fact_lines}

### Governance boundary

{limit_lines}

- This update adds source-anchored PED identity, non-zoonotic, susceptible-age, transmission, diagnostic-differential, early-detection, biosecurity, and treatment-boundary facts only.
- It does not add executable prescriptions, antimicrobial choices, dose, route, treatment course, withdrawal period, MRL, residue, food-safety, or China-specific regulatory execution conclusions.
- Detailed evidence is routed to `{EVIDENCE_EXPANSION.relative_to(ROOT).as_posix()}`.
"""
    heading = "## Web Access authority source ingest / 2026-05-11"
    if heading in text:
        text = re.sub(r"\n## Web Access authority source ingest / 2026-05-11\n.*?(?=\n## |\Z)", "\n" + section.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + section
    write_text(DISEASE_PAGE, text)


def write_evidence_expansion(raw: dict[str, object]) -> None:
    fact_lines = []
    for claim in raw["supported_claims"]:
        fact_lines.append(
            f"- `{claim['fact_id']}` ({claim['supporting_source_id']}): {claim['claim']}"
        )
    source_lines = []
    for source in raw["authority_sources"]:
        source_lines.append(f"- `{source['source_id']}`: {source['title']} - {source['url']}")
    boundary_lines = "\n".join(f"- {item}" for item in raw["do_not_extrapolate"])
    text = f"""---
tags: [evidence_expansion, swine, ped, web_access, authority]
updated: {UPDATED}
disease_id: DIS-008
sources: [{", ".join(SOURCE_IDS)}]
---

# DIS-008 PED Web Access Authority Reinforcement

## Sources

{chr(10).join(source_lines)}

## Registered Fact Anchors

{chr(10).join(fact_lines)}

## Boundary

{boundary_lines}

This evidence expansion is not a default runtime fact dump. It preserves the authority-source intake rationale for audit and graph traceability.
"""
    write_text(EVIDENCE_EXPANSION, text)


def run_status_standardization() -> None:
    script = ROOT / "tools" / "standardize_source_fact_status.py"
    result = subprocess.run([sys.executable, str(script)], cwd=ROOT.parents[1], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:] or result.stdout[-2000:])


def write_ingest_log(summary: dict[str, object]) -> None:
    ISSUES.mkdir(parents=True, exist_ok=True)
    json_path = ISSUES / "dis008_ped_web_access_ingest_2026-05-11.json"
    md_path = ISSUES / "dis008_ped_web_access_ingest_2026-05-11.md"
    write_text(json_path, json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# DIS-008 PED Web Access Formal Ingest",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Raw JSON: `{summary['raw_json']}`",
        f"- Sources registered or updated: {', '.join(summary['source_ids'])}",
        f"- Facts changed: {summary['facts_changed']}",
        f"- Evidence expansion: `{summary['evidence_expansion']}`",
        f"- Disease page: `{summary['disease_page']}`",
        "",
        "## Boundary",
        "",
        "- Only explicit WOAH and USDA APHIS authority-source statements were registered.",
        "- No executable prescription, dose, route, course, withdrawal period, MRL, residue, food-safety, or China-specific regulatory execution conclusion was added.",
    ]
    write_text(md_path, "\n".join(lines) + "\n")


def main() -> None:
    raw = load_raw()
    relpaths = {}
    for source_id in SOURCE_IDS:
        path = ensure_source_page(source_by_id(raw, source_id))
        relpaths[source_id] = path.relative_to(ROOT).as_posix()
    ensure_source_index(raw, relpaths)
    facts = fact_rows(raw)
    facts_changed = upsert_facts(facts)
    write_evidence_expansion(raw)
    update_disease_page(raw, [fact["fact_id"] for fact in facts])
    run_status_standardization()
    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "raw_json": RAW_JSON.relative_to(ROOT).as_posix(),
        "source_ids": SOURCE_IDS,
        "source_pages": [relpaths[source_id] for source_id in SOURCE_IDS],
        "facts_changed": facts_changed,
        "fact_ids": [fact["fact_id"] for fact in facts],
        "evidence_expansion": EVIDENCE_EXPANSION.relative_to(ROOT).as_posix(),
        "disease_page": DISEASE_PAGE.relative_to(ROOT).as_posix(),
        "boundary": "No prescriptions, dose, route, course, withdrawal, MRL, food-safety, or China-specific regulatory execution conclusion added.",
    }
    write_ingest_log(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
