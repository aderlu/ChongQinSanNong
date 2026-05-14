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
RAW_JSON = ROOT / "raw" / "web" / "web_access_dis045_leptospirosis_20260511" / "SRC-DIS045-LEPTO-WEB-20260511.json"
DISEASE_PAGE = ROOT / "wiki" / "diseases" / "DIS-045-leptospirosis.md"
SOURCE_INDEX = ROOT / "exports" / "source_index.csv"
FACTS_JSON = ROOT / "exports" / "knowledge_facts.json"
ISSUES = ROOT / "issues"
SOURCE_DIR = ROOT / "wiki" / "sources"
UPDATED = "2026-05-11T12:45:00+08:00"
TODAY = "2026-05-11"
TZ = timezone(timedelta(hours=8))

ALLOWED_OFFICIAL_SUFFIXES = (
    "moa.gov.cn",
    "nhc.gov.cn",
    "samr.gov.cn",
    "openstd.samr.gov.cn",
    "gov.cn",
    "woah.org",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def slug(value: str) -> str:
    text = re.sub(r"https?://", "", value.lower())
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:48] or "official-source"


def authority_prefix(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    if domain.endswith(".gov.cn") or domain == "gov.cn":
        return "A0"
    if domain.endswith("woah.org"):
        return "A1"
    return "A0"


def source_id_for(source: dict[str, object], index: int) -> str:
    url = str(source.get("url", ""))
    title = str(source.get("title", ""))
    prefix = authority_prefix(url)
    return f"{prefix}-DIS045-LEPTO-WEB-{index:02d}-{slug(title or url).upper()}"


def validate_domain(url: str) -> None:
    domain = urlparse(url).netloc.lower()
    if not domain:
        raise ValueError(f"missing domain: {url}")
    if not any(domain == suffix or domain.endswith("." + suffix) for suffix in ALLOWED_OFFICIAL_SUFFIXES):
        raise ValueError(f"non-official domain rejected: {url}")


def load_raw() -> dict[str, object]:
    payload = json.loads(read_text(RAW_JSON))
    required = [
        "source_id",
        "title",
        "disease_id",
        "disease_name",
        "accessed_at",
        "publisher",
        "authority_level_suggestion",
        "evidence_status_suggestion",
        "official_sources",
        "summary",
        "supported_claims",
        "do_not_extrapolate",
        "extraction_method",
    ]
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise ValueError(f"raw evidence missing required fields: {missing}")
    if payload["source_id"] != "SRC-DIS045-LEPTO-WEB-20260511":
        raise ValueError("unexpected source_id")
    if payload["disease_id"] != "DIS-045":
        raise ValueError("unexpected disease_id")
    if not isinstance(payload["official_sources"], list) or not payload["official_sources"]:
        raise ValueError("official_sources must be a non-empty array")
    for source in payload["official_sources"]:
        if not isinstance(source, dict):
            raise ValueError("official_sources items must be objects")
        url = str(source.get("url", ""))
        validate_domain(url)
        if source.get("official_domain_confirmed") is False:
            raise ValueError(f"official_domain_confirmed is false: {url}")
    return payload


def claims_for_source(source: dict[str, object]) -> list[str]:
    for key in ["explicit_dis045_support", "explicit_support", "explicit_disease_support", "supported_information"]:
        value = source.get(key)
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
    return []


def limitations_for_source(source: dict[str, object]) -> list[str]:
    value = source.get("limitations") or source.get("do_not_extrapolate") or []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return [
        "不得外推治疗、用药、剂量、疗程、休药期、MRL、食品安全、检疫、扑杀、调运或其他执行性监管结论。",
    ]


def source_page(source: dict[str, object], source_id: str) -> str:
    claims = claims_for_source(source)
    if not claims:
        claims = ["本来源仅按 raw JSON 中的页面标题、URL、发布机构、访问时间和摘要字段作为 DIS-045 官方来源候选登记；具体事实由 supported_claims 单独入库。"]
    claim_block = "\n".join(f"- {item}" for item in claims)
    limit_block = "\n".join(f"- {item}" for item in limitations_for_source(source))
    return f"""---
tags: [source, swine, authority, dis045_web_access]
source_id: {source_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
source_status: source_anchored
authority_level: {authority_prefix(str(source.get('url', '')))}
url: {source.get('url', '')}
---

# {source.get('title', source_id)}

## 来源

- URL: {source.get('url', '')}
- 发布机构：{source.get('publisher', '')}
- 页面类型：{source.get('page_type', '')}
- 发布日期：{source.get('published_date', '')}
- 访问时间：{source.get('accessed_at', '')}
- 官方域名确认：{source.get('domain', urlparse(str(source.get('url', ''))).netloc)}

## 可支持结论

{claim_block}

## 不得外推边界

{limit_block}
"""


def read_source_index() -> list[dict[str, str]]:
    with SOURCE_INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_source_index(rows: list[dict[str, str]]) -> None:
    fields = ["source_id", "title", "pages", "evidence_status", "relpath"]
    with SOURCE_INDEX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def register_sources(raw: dict[str, object]) -> list[dict[str, str]]:
    rows = read_source_index()
    by_id = {row.get("source_id", ""): row for row in rows}
    registered = []
    for index, source in enumerate(raw["official_sources"], start=1):
        source_id = source_id_for(source, index)
        path = SOURCE_DIR / f"{source_id}.md"
        write_text(path, source_page(source, source_id))
        relpath = path.relative_to(ROOT).as_posix()
        by_id[source_id] = {
            "source_id": source_id,
            "title": str(source.get("title", source_id)),
            "pages": str(source.get("url", "")),
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": relpath,
        }
        registered.append({"source_id": source_id, "url": str(source.get("url", "")), "relpath": relpath})
    write_source_index(list(by_id.values()))
    return registered


def source_for_claim(claim: dict[str, object], registered: list[dict[str, str]]) -> dict[str, str]:
    url = str(claim.get("supporting_source_url") or claim.get("url") or "")
    for source in registered:
        if url and url == source["url"]:
            return source
    return registered[0]


def fact_object(claim: dict[str, object], index: int, registered: list[dict[str, str]]) -> dict[str, object]:
    source = source_for_claim(claim, registered)
    text = str(claim.get("claim") or claim.get("text") or claim.get("summary") or "").strip()
    if not text:
        raise ValueError(f"supported_claims[{index}] has no claim text")
    return {
        "fact_id": f"DIS045-WEB-{index:03d}-{slug(text)}",
        "fact_type": "official_web_access_claim",
        "subject": "猪钩端螺旋体病",
        "predicate": "official_source_supported_boundary_or_metadata",
        "object": text,
        "fact_confidence": "0.86",
        "evidence_source": source["source_id"],
        "evidence_source_id": source["source_id"],
        "evidence_url": source["url"],
        "evidence_quote_span": "raw supported_claims; raw_json=raw/web/web_access_dis045_leptospirosis_20260511/SRC-DIS045-LEPTO-WEB-20260511.json",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "China/official_source_scope",
        "target_page": "wiki/diseases/DIS-045-leptospirosis.md",
    }


def upsert_facts(raw: dict[str, object], registered: list[dict[str, str]]) -> list[str]:
    facts = json.loads(read_text(FACTS_JSON))
    by_id = {fact.get("fact_id"): idx for idx, fact in enumerate(facts) if isinstance(fact, dict)}
    fact_ids = []
    for index, claim in enumerate(raw["supported_claims"], start=1):
        if not isinstance(claim, dict):
            claim = {"claim": str(claim)}
        fact = fact_object(claim, index, registered)
        fact_ids.append(fact["fact_id"])
        if fact["fact_id"] in by_id:
            facts[by_id[fact["fact_id"]]] = fact
        else:
            facts.append(fact)
    write_text(FACTS_JSON, json.dumps(facts, ensure_ascii=False, indent=2) + "\n")
    return fact_ids


def update_frontmatter_sources(text: str, source_ids: list[str]) -> str:
    match = re.search(r"^sources:\s*\[(.*?)\]\s*$", text, re.M)
    if not match:
        return text
    current = [item.strip() for item in match.group(1).split(",") if item.strip()]
    for source_id in source_ids:
        if source_id not in current:
            current.append(source_id)
    return text[: match.start()] + "sources: [" + ", ".join(current) + "]" + text[match.end() :]


def update_disease_page(raw: dict[str, object], registered: list[dict[str, str]], fact_ids: list[str]) -> None:
    text = read_text(DISEASE_PAGE)
    text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
    text = update_frontmatter_sources(text, [item["source_id"] for item in registered])
    source_lines = "\n".join(f"- `{item['source_id']}`: {item['url']}" for item in registered)
    fact_lines = "\n".join(f"- `{fact_id}`" for fact_id in fact_ids)
    boundaries = raw.get("do_not_extrapolate", [])
    if isinstance(boundaries, list):
        boundary_lines = "\n".join(f"- {item}" for item in boundaries)
    else:
        boundary_lines = f"- {boundaries}"
    section = f"""## Web Access 官方来源入库 / 2026-05-11

### Sources

{source_lines}

### Facts

{fact_lines}

### 不得外推边界

{boundary_lines}

- 本次来源不得单独生成猪钩端螺旋体病治疗、剂量、疗程、休药期、MRL、食品安全、检疫、扑杀、调运或执行性监管结论，除非 raw evidence 中存在逐条可核验的官方原文支持。
"""
    heading = "## Web Access 官方来源入库 / 2026-05-11"
    if heading in text:
        text = re.sub(r"\n## Web Access 官方来源入库 / 2026-05-11\n.*?(?=\n## |\Z)", "\n" + section.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + section
    write_text(DISEASE_PAGE, text)


def run_status_standardization() -> None:
    script = ROOT / "tools" / "standardize_source_fact_status.py"
    result = subprocess.run([sys.executable, str(script)], cwd=ROOT.parents[1], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:] or result.stdout[-2000:])


def write_log(raw: dict[str, object], registered: list[dict[str, str]], fact_ids: list[str]) -> None:
    ISSUES.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "raw_json": RAW_JSON.relative_to(ROOT).as_posix(),
        "source_ids": [item["source_id"] for item in registered],
        "fact_ids": fact_ids,
        "disease_page": DISEASE_PAGE.relative_to(ROOT).as_posix(),
        "boundary": "Only explicit raw supported_claims were registered; high-risk executable conclusions remain blocked unless exact official source support exists.",
    }
    write_text(ISSUES / "dis045_leptospirosis_web_access_ingest_2026-05-11.json", json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    write_text(
        ISSUES / "dis045_leptospirosis_web_access_ingest_2026-05-11.md",
        "# DIS-045 Leptospirosis Web Access Formal Ingest\n\n"
        f"- Raw JSON: `{payload['raw_json']}`\n"
        f"- Sources: {', '.join(payload['source_ids'])}\n"
        f"- Facts: {', '.join(payload['fact_ids'])}\n"
        "- Boundary: high-risk executable conclusions remain blocked without exact official source support.\n",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    raw = load_raw()
    registered = register_sources(raw)
    fact_ids = upsert_facts(raw, registered)
    update_disease_page(raw, registered, fact_ids)
    run_status_standardization()
    write_log(raw, registered, fact_ids)


if __name__ == "__main__":
    main()
