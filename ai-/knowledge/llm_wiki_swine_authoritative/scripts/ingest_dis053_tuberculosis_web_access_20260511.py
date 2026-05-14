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
RAW_JSON = ROOT / "raw" / "web" / "web_access_dis053_tuberculosis_20260511" / "SRC-DIS053-TB-WEB-20260511.json"
DISEASE_PAGE = ROOT / "wiki" / "diseases" / "DIS-053-tuberculosis.md"
SOURCE_DIR = ROOT / "wiki" / "sources"
SOURCE_INDEX = ROOT / "exports" / "source_index.csv"
FACTS_JSON = ROOT / "exports" / "knowledge_facts.json"
ISSUES = ROOT / "issues"
UPDATED = "2026-05-11T12:30:00+08:00"
TODAY = "2026-05-11"
TZ = timezone(timedelta(hours=8))

MOA_SOURCE_ID = "A0-MOA-573"
GBT_SOURCE_ID = "A0-SAMR-GBT-18645-2020-ANIMAL-TB-DIAGNOSIS"

OFFICIAL_DOMAIN_SUFFIXES = (
    "moa.gov.cn",
    "samr.gov.cn",
    "openstd.samr.gov.cn",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def load_raw() -> dict[str, object]:
    payload = json.loads(read_text(RAW_JSON))
    required = [
        "source_id",
        "disease_id",
        "disease_name",
        "accessed_at",
        "official_sources",
        "supported_claims",
        "do_not_extrapolate",
        "extraction_method",
    ]
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise ValueError(f"raw evidence missing required fields: {missing}")
    if payload["source_id"] != "SRC-DIS053-TB-WEB-20260511":
        raise ValueError("unexpected raw source_id")
    if payload["disease_id"] != "DIS-053":
        raise ValueError("unexpected disease_id")
    official_sources = payload.get("official_sources")
    if not isinstance(official_sources, list) or len(official_sources) < 2:
        raise ValueError("official_sources must contain the MOA and SAMR evidence pages")
    for source in official_sources:
        if not isinstance(source, dict):
            raise ValueError("official_sources items must be objects")
        url = str(source.get("url", ""))
        domain = urlparse(url).netloc.lower()
        if not source.get("official_domain_confirmed"):
            raise ValueError(f"official_domain_confirmed is false for {url}")
        if not any(domain == suffix or domain.endswith("." + suffix) for suffix in OFFICIAL_DOMAIN_SUFFIXES):
            raise ValueError(f"non-official domain rejected: {url}")
    return payload


def official_source_by_url(raw: dict[str, object], needle: str) -> dict[str, object]:
    for item in raw["official_sources"]:
        if needle in str(item.get("url", "")):
            return item
    raise ValueError(f"official source not found for {needle}")


def source_page_text(source: dict[str, object], source_id: str) -> str:
    explicit = "\n".join(f"- {item}" for item in source.get("explicit_dis053_support", []))
    limitations = "\n".join(f"- {item}" for item in source.get("limitations", []))
    standard_lines = []
    if source_id == GBT_SOURCE_ID:
        standard_lines = [
            f"- 标准号：{source.get('standard_number', '')}",
            f"- 标准中文名称：{source.get('standard_name', '')}",
            f"- 标准状态：{source.get('standard_status', '')}",
            f"- 发布日期：{source.get('published_date', '')}",
            f"- 实施日期：{source.get('implementation_date', '')}",
            f"- 主管部门：{source.get('competent_department', '')}",
        ]
    else:
        standard_lines = [
            f"- 签发/施行信息：{source.get('signed_date_or_effective_date', '')}",
        ]
    standard_block = "\n".join(line for line in standard_lines if line.strip() != "-")
    return f"""---
tags: [source, swine, authority, dis053_web_access]
source_id: {source_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
source_status: source_anchored
authority_level: A0
url: {source.get('url', '')}
---

# {source.get('title', source_id)}

## 来源

- URL: {source.get('url', '')}
- 发布机构：{source.get('publisher', '')}
- 来源栏目/平台：{source.get('content_source_or_department', '')}
- 页面类型：{source.get('page_type', '')}
- 发布日期：{source.get('published_date', '')}
- 访问时间：{source.get('accessed_at', '')}
- 官方域名确认：{source.get('domain', '')} / parent={source.get('parent_official_domain', '')}
{standard_block}

## 可支持结论

{explicit}

## 不得外推边界

{limitations}
"""


def ensure_source_page(source_id: str, source: dict[str, object]) -> Path:
    path = SOURCE_DIR / f"{source_id}.md"
    if source_id == MOA_SOURCE_ID and path.exists():
        text = read_text(path)
        section = """## DIS-053 Web Access 官方边界补充 / 2026-05-11

- 农业农村部公告第573号可用于确认动物疫病病种名录及疾病名称位置边界；本次 raw evidence 指出牛结核病位于牛病条目，猪病条目未列出猪结核病。`fact_id=DIS053-WEB-001-moa573-list-boundary`
- 不得把牛结核病条目外推为猪结核病的分类、处置、扑杀、检疫、调运、治疗、剂量、休药期、MRL 或食品安全结论。`fact_id=DIS053-WEB-002-moa573-non-extrapolation-boundary`
"""
        if "## DIS-053 Web Access 官方边界补充 / 2026-05-11" not in text:
            write_text(path, text.rstrip() + "\n\n" + section)
        return path
    write_text(path, source_page_text(source, source_id))
    return path


def read_source_index() -> list[dict[str, str]]:
    with SOURCE_INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_source_index(rows: list[dict[str, str]]) -> None:
    fieldnames = ["source_id", "title", "pages", "evidence_status", "relpath"]
    with SOURCE_INDEX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def ensure_source_index(source_id: str, source: dict[str, object], relpath: str) -> None:
    rows = read_source_index()
    by_id = {row.get("source_id", ""): row for row in rows}
    by_id[source_id] = {
        "source_id": source_id,
        "title": str(source.get("title", source_id)),
        "pages": str(source.get("url", "")),
        "evidence_status": "HUMAN_REVIEWED",
        "relpath": relpath,
    }
    write_source_index(list(by_id.values()))


def fact_rows(raw: dict[str, object], moa: dict[str, object], gbt: dict[str, object]) -> list[dict[str, object]]:
    raw_relpath = RAW_JSON.relative_to(ROOT).as_posix()
    target_page = "wiki/diseases/DIS-053-tuberculosis.md"
    return [
        {
            "fact_id": "DIS053-WEB-001-moa573-list-boundary",
            "fact_type": "official_registry_boundary",
            "subject": "猪结核病",
            "predicate": "china_animal_disease_list_boundary",
            "object": "农业农村部公告第573号发布《一、二、三类动物疫病病种名录》；本次官方来源读取显示牛结核病位于牛病条目，猪病条目未列出猪结核病。",
            "fact_confidence": "0.88",
            "evidence_source": MOA_SOURCE_ID,
            "evidence_source_id": MOA_SOURCE_ID,
            "evidence_url": str(moa.get("url", "")),
            "evidence_quote_span": "raw official_sources[MOA].explicit_dis053_support; raw_json=" + raw_relpath,
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": "China",
            "target_page": target_page,
        },
        {
            "fact_id": "DIS053-WEB-002-moa573-non-extrapolation-boundary",
            "fact_type": "official_non_extrapolation_boundary",
            "subject": "猪结核病",
            "predicate": "must_not_extrapolate_from_bovine_tuberculosis_registry_entry",
            "object": "不得把公告第573号中的牛结核病条目外推为猪结核病的分类、处置、扑杀、检疫、调运、治疗、剂量、休药期、MRL 或食品安全结论。",
            "fact_confidence": "0.90",
            "evidence_source": MOA_SOURCE_ID,
            "evidence_source_id": MOA_SOURCE_ID,
            "evidence_url": str(moa.get("url", "")),
            "evidence_quote_span": "raw official_sources[MOA].limitations; raw_json=" + raw_relpath,
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": "China",
            "target_page": target_page,
        },
        {
            "fact_id": "DIS053-WEB-003-gbt18645-current-standard-metadata",
            "fact_type": "official_standard_metadata",
            "subject": "动物结核病诊断技术",
            "predicate": "has_current_national_standard_metadata",
            "object": "全国标准信息公共服务平台页面显示 GB/T 18645-2020《动物结核病诊断技术》为现行标准，发布日期和实施日期均为2020-12-14，主管部门为农业农村部。",
            "fact_confidence": "0.88",
            "evidence_source": GBT_SOURCE_ID,
            "evidence_source_id": GBT_SOURCE_ID,
            "evidence_url": str(gbt.get("url", "")),
            "evidence_quote_span": "raw official_sources[SAMR].standard metadata; raw_json=" + raw_relpath,
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": "China",
            "target_page": target_page,
        },
        {
            "fact_id": "DIS053-WEB-004-gbt18645-metadata-only-boundary",
            "fact_type": "official_standard_boundary",
            "subject": "猪结核病",
            "predicate": "standard_info_page_is_metadata_only",
            "object": "GB/T 18645-2020 标准信息页仅支持标准存在、现行状态及发布元数据；本次未读取并核验标准全文，不得生成具体检测步骤、采样要求、阳性判定、确诊规则或实验室 SOP。",
            "fact_confidence": "0.90",
            "evidence_source": GBT_SOURCE_ID,
            "evidence_source_id": GBT_SOURCE_ID,
            "evidence_url": str(gbt.get("url", "")),
            "evidence_quote_span": "raw official_sources[SAMR].limitations; raw_json=" + raw_relpath,
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": "China",
            "target_page": target_page,
        },
    ]


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


def update_disease_page() -> None:
    text = read_text(DISEASE_PAGE)
    text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
    text = update_frontmatter_sources(text, [MOA_SOURCE_ID, GBT_SOURCE_ID])
    section = f"""## Web Access 官方来源入库 / 2026-05-11

- 本次正式入库只采用 raw JSON 中已确认官方域名的原文来源：`{MOA_SOURCE_ID}` 与 `{GBT_SOURCE_ID}`；raw JSON 仅作为提取审计记录，不作为 A0 source 节点替代原文。
- 农业农村部公告第573号支持动物疫病名录及名称位置边界：牛结核病位于牛病条目，猪病条目未列出猪结核病。`fact_id=DIS053-WEB-001-moa573-list-boundary; source_id={MOA_SOURCE_ID}`
- 不得把牛结核病条目外推为猪结核病分类、处置、扑杀、检疫、调运、治疗、剂量、休药期、MRL 或食品安全结论。`fact_id=DIS053-WEB-002-moa573-non-extrapolation-boundary; source_id={MOA_SOURCE_ID}`
- 全国标准信息公共服务平台页面支持 GB/T 18645-2020《动物结核病诊断技术》的现行标准元数据；本次未核验标准全文。`fact_id=DIS053-WEB-003-gbt18645-current-standard-metadata; source_id={GBT_SOURCE_ID}`
- GB/T 18645-2020 信息页不得外推为具体检测步骤、采样要求、阳性判定、确诊规则或实验室 SOP。`fact_id=DIS053-WEB-004-gbt18645-metadata-only-boundary; source_id={GBT_SOURCE_ID}`
- 本次来源不支持猪结核病当前可执行剂量、疗程、休药期、MRL 或合规结论。`raw_json=raw/web/web_access_dis053_tuberculosis_20260511/SRC-DIS053-TB-WEB-20260511.json`
"""
    heading = "## Web Access 官方来源入库 / 2026-05-11"
    if heading in text:
        text = re.sub(r"\n## Web Access 官方来源入库 / 2026-05-11\n.*?(?=\n## |\Z)", "\n" + section.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + section
    write_text(DISEASE_PAGE, text)


def run_status_standardization() -> None:
    script = ROOT / "tools" / "standardize_source_fact_status.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT.parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:] or result.stdout[-2000:])


def write_ingest_log(summary: dict[str, object]) -> None:
    ISSUES.mkdir(parents=True, exist_ok=True)
    log_json = ISSUES / "dis053_tuberculosis_web_access_ingest_2026-05-11.json"
    log_md = ISSUES / "dis053_tuberculosis_web_access_ingest_2026-05-11.md"
    write_text(log_json, json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# DIS-053 Tuberculosis Web Access Formal Ingest",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Raw JSON: `{summary['raw_json']}`",
        f"- Sources registered: {', '.join(summary['source_ids'])}",
        f"- Facts upserted: {summary['facts_changed']}",
        "",
        "## Boundary",
        "",
        "- Only explicit official-source statements were registered.",
        "- No treatment, dose, course, withdrawal period, MRL, food-safety, culling, quarantine, movement-control, or regulatory execution conclusion was added.",
    ]
    write_text(log_md, "\n".join(lines) + "\n")


def main() -> None:
    raw = load_raw()
    moa = official_source_by_url(raw, "moa.gov.cn")
    gbt = official_source_by_url(raw, "openstd.samr.gov.cn")

    moa_path = ensure_source_page(MOA_SOURCE_ID, moa)
    gbt_path = ensure_source_page(GBT_SOURCE_ID, gbt)
    ensure_source_index(MOA_SOURCE_ID, moa, moa_path.relative_to(ROOT).as_posix())
    ensure_source_index(GBT_SOURCE_ID, gbt, gbt_path.relative_to(ROOT).as_posix())

    facts_changed = upsert_facts(fact_rows(raw, moa, gbt))
    update_disease_page()
    run_status_standardization()

    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "raw_json": RAW_JSON.relative_to(ROOT).as_posix(),
        "source_ids": [MOA_SOURCE_ID, GBT_SOURCE_ID],
        "source_pages": [moa_path.relative_to(ROOT).as_posix(), gbt_path.relative_to(ROOT).as_posix()],
        "facts_changed": facts_changed,
        "fact_ids": [
            "DIS053-WEB-001-moa573-list-boundary",
            "DIS053-WEB-002-moa573-non-extrapolation-boundary",
            "DIS053-WEB-003-gbt18645-current-standard-metadata",
            "DIS053-WEB-004-gbt18645-metadata-only-boundary",
        ],
        "disease_page": DISEASE_PAGE.relative_to(ROOT).as_posix(),
        "boundary": "No treatment, dose, course, withdrawal, MRL, food-safety, culling, quarantine, movement-control, or regulatory execution conclusion added.",
    }
    write_ingest_log(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
