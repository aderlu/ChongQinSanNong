from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
RAW_URLS = WIKI / "raw" / "urls"
RAW_PDFS = WIKI / "raw" / "pdfs"
SOURCES_DIR = WIKI / "wiki" / "sources"
ISSUES = WIKI / "issues"
NOW = "2026-05-07T23:55:00+08:00"


SOURCES = [
    {
        "source_id": "A0-MOA-BANNED-DRUG-250-RAW",
        "title": "MOA Notice No. 250 banned drugs and compounds for food animals",
        "url": "https://www.moa.gov.cn/govpublic/xmsyj/202001/t20200106_6334375.htm",
        "authority_level": "official",
        "source_type": "html",
        "category": "china_prohibited_boundary",
        "use": "Chinese hard boundary for banned/prohibited substances; not treatment efficacy.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A0-MOA-STOP-FLUOROQUINOLONES-2292-RAW",
        "title": "MOA Notice No. 2292 stopping four fluoroquinolones for food animals",
        "url": "https://www.moa.gov.cn/govpublic/SYJ/201509/t20150907_4819267.htm",
        "authority_level": "official",
        "source_type": "html",
        "category": "china_stopped_drug_boundary",
        "use": "Chinese hard boundary for lomefloxacin, pefloxacin, ofloxacin and norfloxacin in food animals.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A0-MOA-STOP-OLAQUINDOX-2638-RAW",
        "title": "MOA policy entry on stopping olaquindox, arsanilic acid and roxarsone in food animals",
        "url": "https://www.moa.gov.cn/xw/zwdt/201801/t20180119_6135358.htm",
        "authority_level": "official",
        "source_type": "html",
        "category": "china_stopped_drug_boundary",
        "use": "Chinese hard boundary for olaquindox and organic arsenicals; distinguish treatment, feed additive and growth-promotion contexts.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A0-MOA-WITHDRAWAL-278-RAW",
        "title": "MOA Notice No. 278 withdrawal period provisions",
        "url": "https://www.moa.gov.cn/nybgb/2003/snqi/201711/t20171126_5919564.htm",
        "authority_level": "official",
        "source_type": "html",
        "category": "china_withdrawal_boundary",
        "use": "Chinese withdrawal-period source entry; lower priority than current product labels and later notices.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A0-MOA-MRL-GB31650-2019-RAW",
        "title": "MOA GB 31650-2019 veterinary drug maximum residue limits news entry",
        "url": "https://www.moa.gov.cn/xw/zwdt/201910/t20191008_6329518.htm",
        "authority_level": "official",
        "source_type": "html",
        "category": "china_residue_boundary",
        "use": "Chinese MRL source entry; MRL existence does not equal swine approval.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A1-WOAH-SWINE-AMR-TRD-2025",
        "title": "WOAH Technical Reference Document listing antimicrobial agents of veterinary importance for swine",
        "url": "https://www.woah.org/app/uploads/2025/04/trd-swine.pdf",
        "authority_level": "guideline",
        "source_type": "pdf",
        "category": "amr_prudence_swine",
        "use": "Swine-specific antimicrobial importance and AMR risk prioritisation; explicitly not a treatment guideline.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A1-WOAH-ANTIMICROBIAL-VETERINARY-IMPORTANCE",
        "title": "WOAH list of antimicrobial agents of veterinary importance",
        "url": "https://www.woah.org/en/for-the-media/amr/oie-amr-standards/",
        "authority_level": "guideline",
        "source_type": "html",
        "category": "amr_prudence_global",
        "use": "Global antimicrobial importance source entry for AMR stewardship; not a prescription source.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A1-EMA-AMEG-ANTIBIOTIC-CATEGORISATION",
        "title": "EMA AMEG categorisation of antibiotics for use in animals",
        "url": "https://www.ema.europa.eu/system/files/documents/report/ameg-infographic-categorisation-antibiotics_en.pdf",
        "authority_level": "guideline",
        "source_type": "pdf",
        "category": "amr_prudence_eu",
        "use": "Antibiotic categorisation for responsible veterinary use; does not replace treatment guidelines.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A1-EMA-MRL-OVERVIEW",
        "title": "EMA establishing maximum residue limits for veterinary medicines",
        "url": "https://www.ema.europa.eu/en/veterinary-regulatory-overview/research-development-veterinary-medicines/maximum-residue-limits-mrl/establishing-maximum-residue-limits-veterinary-medicines",
        "authority_level": "official",
        "source_type": "html",
        "category": "residue_boundary_eu",
        "use": "EU MRL concept, table 1 allowed substances and table 2 prohibited substances boundary; not China approval.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-FDA-GREEN-BOOK",
        "title": "FDA Approved Animal Drug Products Green Book",
        "url": "https://www.fda.gov/animal-veterinary/products/approved-animal-drug-products-green-book",
        "authority_level": "official",
        "source_type": "html",
        "category": "us_label_entry",
        "use": "US approved animal drug product entry point; useful for label/approval cross-check, not China approval.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-FDA-LEGAL-ANIMAL-DRUGS",
        "title": "FDA how to tell if a drug is legally marketed for animals",
        "url": "https://www.fda.gov/animal-veterinary/unapproved-animal-drugs/how-can-i-tell-if-drug-legally-marketed-animals",
        "authority_level": "official",
        "source_type": "html",
        "category": "us_label_entry",
        "use": "US legal-marketing boundary for animal drugs; supports label verification workflow.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-MERCK-SWINE-ERYSIPELAS",
        "title": "Merck Veterinary Manual swine erysipelas",
        "url": "https://www.merckvetmanual.com/infectious-diseases/erysipelothrix-rhusiopathiae-infection/swine-erysipelas",
        "authority_level": "guideline",
        "source_type": "html",
        "category": "treatment_efficacy_candidate",
        "use": "Treatment candidate source for erysipelas: penicillin, ampicillin, ceftiofur, tetracyclines and NSAID support.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS",
        "title": "Merck Veterinary Manual enteric colibacillosis in pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/enteric-colibacillosis-in-pigs",
        "authority_level": "guideline",
        "source_type": "html",
        "category": "treatment_efficacy_candidate",
        "use": "Treatment candidate source for ETEC: prompt antimicrobials based on MIC plus fluid/electrolyte restoration.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-MERCK-PORCINE-PROLIFERATIVE-ENTEROPATHY",
        "title": "Merck Veterinary Manual porcine proliferative enteropathy",
        "url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/porcine-proliferative-enteropathy",
        "authority_level": "guideline",
        "source_type": "html",
        "category": "treatment_efficacy_candidate",
        "use": "Treatment candidate source for Lawsonia intracellularis: antimicrobials and vaccination.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-MERCK-SWINE-DYSENTERY",
        "title": "Merck Veterinary Manual swine dysentery",
        "url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/swine-dysentery",
        "authority_level": "guideline",
        "source_type": "html",
        "category": "treatment_efficacy_candidate",
        "use": "Treatment candidate source for Brachyspira/swine dysentery: pleuromutilins, carbadox, lincomycin and tylosin; carbadox legality must be checked.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-MERCK-COCCIDIOSIS-PIGS",
        "title": "Merck Veterinary Manual coccidiosis of pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/coccidiosis/coccidiosis-of-pigs",
        "authority_level": "guideline",
        "source_type": "html",
        "category": "treatment_efficacy_candidate",
        "use": "Treatment candidate source for pig coccidiosis: toltrazuril, sulfonamides, amprolium and environmental control; local legality required.",
        "status": "NEEDS_REVIEW",
    },
    {
        "source_id": "A2-MERCK-PLEUROPNEUMONIA-PIGS",
        "title": "Merck Veterinary Manual pleuropneumonia in pigs",
        "url": "https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-pigs/pleuropneumonia-in-pigs?query=respiratory+rate",
        "authority_level": "guideline",
        "source_type": "html",
        "category": "treatment_efficacy_candidate",
        "use": "Treatment candidate source for APP pleuropneumonia: ceftiofur, tilmicosin, tetracyclines, synthetic penicillins, tylosin and sulfonamides.",
        "status": "NEEDS_REVIEW",
    },
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:90] or hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def fetch(url: str) -> tuple[bytes, str, int | None, str | None]:
    req = Request(url, headers={"User-Agent": "Codex swine wiki source fetch/2026-05-07"})
    try:
        with urlopen(req, timeout=45) as resp:
            data = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            return data, content_type, resp.status, None
    except HTTPError as exc:
        return exc.read(), exc.headers.get("Content-Type", ""), exc.code, str(exc)
    except URLError as exc:
        return b"", "", None, str(exc)


def source_page(src: dict[str, str], raw_relpath: str, sha256: str, bytes_len: int, http_status: int | None, error: str | None) -> str:
    err = error or ""
    return f"""---
type: source
source_id: {src["source_id"]}
source_path: {src["url"]}
source_type: {src["source_type"]}
authority_level: {src["authority_level"]}
evidence_status: {src["status"]}
created: {NOW}
updated: {NOW}
sources: []
raw_relpath: {raw_relpath}
sha256: {sha256}
http_status: {http_status or ""}
---

# {src["title"]}

## 来源

- URL: {src["url"]}
- 本地缓存：`{raw_relpath}`
- SHA256: `{sha256}`
- HTTP status: `{http_status or ""}`
- Fetch error: `{err}`

## 可用范围

- 类别：`{src["category"]}`。
- 用途：{src["use"]}

## 使用边界

- `treatment_efficacy_candidate` 可用于治疗候选、鉴别和复核路径，但仍不能替代本地标签、禁用清单、处方或药敏证据。
- `china_*_boundary` 优先用于中国禁用、停用、残留、休药期硬边界；命中违法或禁用时不得作为可用治疗药。
- `amr_prudence_*` 和 `residue_boundary_*` 用于审慎用药、AMR 或残留风险，不直接生成治疗方案。
"""


def main() -> None:
    RAW_URLS.mkdir(parents=True, exist_ok=True)
    RAW_PDFS.mkdir(parents=True, exist_ok=True)
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for src in SOURCES:
        data, content_type, status, error = fetch(src["url"])
        ext = ".pdf" if src["source_type"] == "pdf" or "pdf" in content_type.lower() else ".html"
        raw_dir = RAW_PDFS if ext == ".pdf" else RAW_URLS
        filename = f"{src['source_id']}-{slugify(src['title'])}{ext}"
        raw_path = raw_dir / filename
        raw_path.write_bytes(data)
        sha256 = hashlib.sha256(data).hexdigest()
        raw_rel = raw_path.relative_to(WIKI).as_posix()
        write_text = source_page(src, raw_rel, sha256, len(data), status, error)
        (SOURCES_DIR / f"{src['source_id']}.md").write_text(write_text.rstrip() + "\n", encoding="utf-8", newline="\n")
        manifest.append({
            **src,
            "raw_relpath": raw_rel,
            "sha256": sha256,
            "bytes": len(data),
            "http_status": status,
            "content_type": content_type,
            "error": error or "",
        })
        time.sleep(0.25)

    (ISSUES / "authority_web_fetch_manifest_2026-05-07.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    with (ISSUES / "authority_web_fetch_manifest_2026-05-07.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)

    index_path = WIKI / "exports" / "source_index.csv"
    rows = []
    with index_path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    by_id = {row[0]: row for row in rows[1:] if row}
    for src in SOURCES:
        by_id[src["source_id"]] = [
            src["source_id"],
            src["title"],
            src["url"],
            src["status"],
            f"wiki/sources/{src['source_id']}.md",
        ]
    with index_path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows([header] + sorted(by_id.values(), key=lambda row: row[0]))

    report = """# Authority Web Fetch Report - 2026-05-07

## Summary

- Downloaded official/guideline web sources and PDFs to `raw/urls` and `raw/pdfs`.
- Created source pages in `wiki/sources` with local cache path, SHA256, authority level and use boundary.
- Updated `exports/source_index.csv`.
- Did not mutate `exports/knowledge_facts.json`.

## Source-use policy

- Merck Veterinary Manual pages are treatment-efficacy candidates and disease-management references.
- WOAH/EMA/FDA sources are stewardship, residue or label-verification references, not direct China legality.
- MOA sources are China hard-boundary references for banned/stopped/withdrawal/MRL checks.
"""
    (ISSUES / "authority_web_fetch_report_2026-05-07.md").write_text(report, encoding="utf-8", newline="\n")

    log_path = WIKI / "log.md"
    log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Wiki Log\n"
    marker = "2026-05-07 authority-web-fetch"
    if marker not in log_text:
        log_path.write_text(
            log_text.rstrip()
            + "\n\n"
            + f"{marker} | fetched {len(SOURCES)} authority web/PDF sources to raw cache; created source pages and updated source index; facts unchanged.\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"fetched={len(SOURCES)}")


if __name__ == "__main__":
    main()
