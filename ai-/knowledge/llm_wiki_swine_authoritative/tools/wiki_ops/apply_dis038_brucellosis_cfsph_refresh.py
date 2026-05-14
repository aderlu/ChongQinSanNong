from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from guarded_update_context import require_guarded_update


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
SOURCES = ROOT / "wiki" / "sources"
DISEASE = ROOT / "wiki" / "diseases" / "DIS-038-brucella-suis-brucellosis.md"
EVIDENCE_DIR = (
    ROOT
    / "wiki"
    / "evidence_expansions"
    / "diseases"
    / "phase4_runtime_compaction"
    / "DIS-038-brucella-suis-brucellosis"
)
RAW_DIR = ROOT / "raw" / "web" / "web_access_dis038_brucellosis_20260513"
ISSUES = ROOT / "issues"
TZ = timezone(timedelta(hours=8))

UPDATED_AT = "2026-05-13T22:35:00+08:00"
ACCESSED = "2026-05-13"
PDF_NAME = "A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.pdf"


SOURCE_UPDATE = {
    "source_id": "A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026",
    "file": "A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.md",
    "title": "Iowa State CFSPH Brucella suis factsheet",
    "url": "https://www.cfsph.iastate.edu/Factsheets/pdfs/brucellosis_suis.pdf",
    "publisher": "Center for Food Security and Public Health, Iowa State University",
    "page_last_modified": "factsheet PDF, accessed 2026-05-13",
    "authority_level": "A2",
    "usable_boundary": [
        "Use for swine brucellosis transmission, host range, reproductive-clinical pattern, zoonotic/public-health relevance, and environmental survival boundaries stated in the factsheet.",
        "Use for retrieval, differential, diagnostic-boundary, and public-health exposure prompts where claims stay within the factsheet language.",
    ],
    "do_not_extrapolate": [
        "Do not use this source alone for China-specific reporting, quarantine, culling, movement, compensation, slaughter, food-chain release, vaccination program, drug dose, withdrawal period, or MRL claims.",
        "Do not promote descriptive host-range or transmission statements into farm execution orders without current A0/A1 control sources.",
    ],
}


FACTS_TO_ADD = [
    {
        "fact_id": "DIS038-WEB-005-cfsph-transmission-exposure",
        "fact_type": "brucellosis_transmission_boundary",
        "subject": "猪布鲁氏菌病",
        "predicate": "cfsph_transmission_and_exposure_boundary",
        "object": "The CFSPH Brucella suis factsheet describes transmission through contact with infected reproductive discharges, aborted fetuses, semen, and contaminated environments, and notes that venereal spread and contact with feral or wild swine can sustain exposure risk.",
        "fact_confidence": "high",
        "evidence_source": "Iowa State CFSPH Brucella suis factsheet",
        "evidence_source_id": "A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026",
        "evidence_url": "https://www.cfsph.iastate.edu/Factsheets/pdfs/brucellosis_suis.pdf",
        "evidence_quote_span": "PDF page 2-3; transmission/exposure section; extracted 2026-05-13",
        "evidence_status": "HUMAN_REVIEWED",
        "source_status": "source_anchored",
        "fact_validity": "valid",
        "authority_level": "A2",
        "risk_class": "public_health",
        "task_use_status": "generation_ready_limited",
        "applies_to_species": "swine",
        "applies_to_stage": "breeding_herd",
        "jurisdiction": "international animal/public-health reference",
        "target_page": "wiki/diseases/DIS-038-brucella-suis-brucellosis.md",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "DIS038-WEB-006-cfsph-clinical-pattern",
        "fact_type": "brucellosis_clinical_boundary",
        "subject": "猪布鲁氏菌病",
        "predicate": "cfsph_reproductive_and_lameness_pattern_boundary",
        "object": "The CFSPH Brucella suis factsheet supports a reproductive-loss pattern including abortion, infertility, stillbirth, weak piglets, and possible lameness or paralysis related to reproductive or musculoskeletal involvement, while keeping confirmation separate from clinical suspicion.",
        "fact_confidence": "high",
        "evidence_source": "Iowa State CFSPH Brucella suis factsheet",
        "evidence_source_id": "A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026",
        "evidence_url": "https://www.cfsph.iastate.edu/Factsheets/pdfs/brucellosis_suis.pdf",
        "evidence_quote_span": "PDF page 3-4; clinical signs section; extracted 2026-05-13",
        "evidence_status": "HUMAN_REVIEWED",
        "source_status": "source_anchored",
        "fact_validity": "valid",
        "authority_level": "A2",
        "risk_class": "diagnostic",
        "task_use_status": "generation_ready_limited",
        "applies_to_species": "swine",
        "applies_to_stage": "breeding_herd",
        "jurisdiction": "international animal/public-health reference",
        "target_page": "wiki/diseases/DIS-038-brucella-suis-brucellosis.md",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "DIS038-WEB-007-cfsph-zoonotic-boundary",
        "fact_type": "brucellosis_public_health_boundary",
        "subject": "猪布鲁氏菌病公共卫生边界",
        "predicate": "cfsph_zoonotic_hunter_occupational_boundary",
        "object": "The CFSPH Brucella suis factsheet supports zoonotic risk from pigs and feral swine, including occupational and hunting-related exposure, but it must be used as a public-health exposure boundary rather than a primary herd-control or treatment protocol.",
        "fact_confidence": "high",
        "evidence_source": "Iowa State CFSPH Brucella suis factsheet",
        "evidence_source_id": "A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026",
        "evidence_url": "https://www.cfsph.iastate.edu/Factsheets/pdfs/brucellosis_suis.pdf",
        "evidence_quote_span": "PDF page 1-2 and 4-5; zoonotic/public-health sections; extracted 2026-05-13",
        "evidence_status": "HUMAN_REVIEWED",
        "source_status": "source_anchored",
        "fact_validity": "valid",
        "authority_level": "A2",
        "risk_class": "public_health",
        "task_use_status": "generation_ready_limited",
        "applies_to_species": "swine",
        "applies_to_stage": "human_exposure_boundary",
        "jurisdiction": "international animal/public-health reference",
        "target_page": "wiki/diseases/DIS-038-brucella-suis-brucellosis.md",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
]


RUNTIME_BLOCK = """
## Authority Web Refresh / 2026-05-13

> This additive refresh was produced through the guarded CRUD decision workflow using a source-anchored CFSPH factsheet PDF downloaded through the web-access workflow. It strengthens transmission, clinical-pattern, and zoonotic/public-health boundaries for swine brucellosis. It does not replace China A0 animal-disease control sources and does not authorize local reporting, culling, movement, vaccination, slaughter, compensation, food-chain, drug, withdrawal-period, or MRL claims.

### Transmission and exposure boundary

- The Iowa State CFSPH Brucella suis factsheet describes transmission through infected reproductive discharges, aborted fetuses, semen, contaminated environments, and exposure to feral or wild swine. This strengthens source-anchored transmission routing but does not create jurisdiction-free control orders. `fact_id=DIS038-WEB-005-cfsph-transmission-exposure; source_id=A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`

### Clinical-pattern boundary

- The same factsheet supports a reproductive-loss pattern including abortion, infertility, stillbirth, weak piglets, and possible lameness/paralysis involvement, while keeping clinical suspicion separate from confirmation. `fact_id=DIS038-WEB-006-cfsph-clinical-pattern; source_id=A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`

### Zoonotic/public-health boundary

- CFSPH also supports zoonotic risk from pigs and feral swine, including occupational and hunting-related exposure. This is a public-health exposure boundary, not a standalone herd-control, treatment, or local regulatory protocol. `fact_id=DIS038-WEB-007-cfsph-zoonotic-boundary; source_id=A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`

### Enforcement boundary

- These A2 facts strengthen retrieval, differential, clinical-boundary, and public-health exposure answers only. China-specific reporting, quarantine, culling, movement, vaccination program, slaughter, compensation, food-chain release, drug dose, withdrawal period, and MRL claims must still route to current China A0/A1 sources and rule cards.
"""


EVIDENCE_EXPANSION = """
# DIS-038 Brucellosis CFSPH Authority Refresh / 2026-05-13

## Scope

This evidence expansion records the web-access acquisition and controlled refresh for `DIS-038-brucella-suis-brucellosis`.

## Web Access Acquisition

- Skill path: `C:/Users/admin/.codex/skills/web-access/SKILL.md`
- Dependency precheck: `node C:/Users/admin/.codex/skills/web-access/scripts/check-deps.mjs`
- Browser/CDP proxy confirmed available through `http://localhost:3456/targets`
- Authority source discovered from CFSPH technical factsheet index and downloaded as raw PDF through the governance workflow

## Raw Evidence

- `raw/web/web_access_dis038_brucellosis_20260513/A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026.pdf`
- `raw/web/web_access_dis038_brucellosis_20260513/A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026-pages.txt`

## Source Added

- `A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026`

## Facts Added

- `DIS038-WEB-005-cfsph-transmission-exposure`
- `DIS038-WEB-006-cfsph-clinical-pattern`
- `DIS038-WEB-007-cfsph-zoonotic-boundary`

## Governance Boundary

- This refresh is additive and keeps all existing A0/A1/A2 source and fact records.
- The new source is A2, not A0 or A1.
- The new source cannot replace China-specific reporting, quarantine, culling, movement, compensation, slaughter, food-chain release, vaccination, dose, withdrawal-period, or MRL rules.
- Runtime additions remain short source/fact-routed summaries. Full PDF text stays outside runtime.
"""


def render_source_page() -> str:
    lines = [
        "---",
        "tags: [source, swine, authority, cfsph, brucellosis, zoonosis, web_access_refresh]",
        f"source_id: {SOURCE_UPDATE['source_id']}",
        "source_type: authoritative_pdf",
        f"authority_level: {SOURCE_UPDATE['authority_level']}",
        "evidence_status: HUMAN_REVIEWED",
        "source_status: source_anchored",
        f"external_url: {SOURCE_UPDATE['url']}",
        f"updated: {UPDATED_AT}",
        "---",
        "",
        f"# {SOURCE_UPDATE['title']}",
        "",
        "## Source",
        "",
        f"- URL: {SOURCE_UPDATE['url']}",
        f"- Publisher: {SOURCE_UPDATE['publisher']}",
        f"- Page last modified: {SOURCE_UPDATE['page_last_modified']}",
        f"- Accessed: {ACCESSED}",
        f"- Authority level: {SOURCE_UPDATE['authority_level']}",
        f"- Raw PDF: raw/web/web_access_dis038_brucellosis_20260513/{PDF_NAME}",
        "",
        "## Usable Boundary",
        "",
    ]
    lines.extend(f"- {item}" for item in SOURCE_UPDATE["usable_boundary"])
    lines.extend(["", "## Do-not-extrapolate Boundary", ""])
    lines.extend(f"- {item}" for item in SOURCE_UPDATE["do_not_extrapolate"])
    lines.extend(
        [
            "",
            "## 可支持结论",
            "",
            "- 支持范围以该 PDF 原文、页码锚点、raw 提取文件和已登记 facts 为准。",
            "",
            "## 不得外推边界",
            "",
            "- 不得将 A2 事实表外推为中国法域的执行命令、药物方案、休药期、MRL 或食品安全放行结论。",
            "",
        ]
    )
    return "\n".join(lines)


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_source_page() -> str:
    path = SOURCES / SOURCE_UPDATE["file"]
    path.write_text(render_source_page(), encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def update_source_index() -> None:
    path = EXPORTS / "source_index.csv"
    rows, fieldnames = read_csv(path)
    by_id = {row.get("source_id", ""): row for row in rows if row.get("source_id")}
    source_id = SOURCE_UPDATE["source_id"]
    existing = dict(by_id.get(source_id, {}))
    existing.update(
        {
            "source_id": source_id,
            "title": str(SOURCE_UPDATE["title"]),
            "pages": str(SOURCE_UPDATE["url"]),
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": f"wiki/sources/{SOURCE_UPDATE['file']}",
        }
    )
    by_id[source_id] = existing
    write_csv(path, sorted(by_id.values(), key=lambda row: row.get("source_id", "")), fieldnames)


def update_knowledge_facts() -> None:
    path = EXPORTS / "knowledge_facts.json"
    facts = json.loads(path.read_text(encoding="utf-8-sig"))
    by_id = {fact.get("fact_id"): fact for fact in facts if isinstance(fact, dict) and fact.get("fact_id")}
    for fact in FACTS_TO_ADD:
        by_id[fact["fact_id"]] = fact
    path.write_text(json.dumps(list(by_id.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_source_in_frontmatter(text: str) -> str:
    head, body = text.split("---", 2)[1:]
    source_id = SOURCE_UPDATE["source_id"]
    if source_id not in head:
        head = head.replace("sources: [", f"sources: [{source_id}, ", 1)
    return f"---{head}---{body}"


def update_disease_page() -> None:
    text = DISEASE.read_text(encoding="utf-8")
    text = ensure_source_in_frontmatter(text)
    marker = "## Authority Web Refresh / 2026-05-13"
    if marker not in text:
        text = text.rstrip() + "\n\n" + RUNTIME_BLOCK.strip() + "\n"
    DISEASE.write_text(text, encoding="utf-8")


def write_evidence_expansion() -> str:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE_DIR / "007-CFSPH-Authority-Web-Refresh-2026-05-13.md"
    path.write_text(EVIDENCE_EXPANSION.strip() + "\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def write_pdf_page_extract() -> str:
    from pypdf import PdfReader

    pdf_path = RAW_DIR / PDF_NAME
    reader = PdfReader(str(pdf_path))
    lines: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").replace("\r\n", "\n").replace("\r", "\n").strip()
        lines.append(f"## PAGE {index}\n")
        lines.append(text)
        lines.append("")
    output = RAW_DIR / "A2-CFSPH-BRUCELLA-SUIS-FACTSHEET-2026-pages.txt"
    output.write_text("\n".join(lines), encoding="utf-8")
    return output.relative_to(ROOT).as_posix()


def write_execution_report(source_page: str, evidence_path: str, extract_path: str) -> str:
    report = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "target": "DIS-038 brucella suis brucellosis",
        "mode": "web_access_authority_refresh",
        "crud_action": "create/update",
        "source_added": SOURCE_UPDATE["source_id"],
        "facts_added": [fact["fact_id"] for fact in FACTS_TO_ADD],
        "source_page": source_page,
        "runtime_page": DISEASE.relative_to(ROOT).as_posix(),
        "evidence_expansion": evidence_path,
        "raw_pdf": f"raw/web/web_access_dis038_brucellosis_20260513/{PDF_NAME}",
        "raw_extract": extract_path,
        "old_data_handling": "keep",
        "runtime_impact": "update",
        "gold_dataset_impact": "update via rebuilt fact status/readiness indexes",
        "boundary": "A2 source does not replace China A0/A1 execution rules.",
    }
    path = ISSUES / "dis038_brucellosis_cfsph_refresh_2026-05-13.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def refresh_fact_status() -> None:
    # After the enterprise cleanup, source/fact status normalization lives under
    # tools/wiki_ops. Keep the call explicit here so guarded updates keep using
    # the maintained path instead of a removed legacy wrapper.
    script = ROOT / "tools" / "wiki_ops" / "standardize_source_fact_status.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT.parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:] or result.stdout[-2000:])


def main() -> None:
    require_guarded_update()
    source_page = write_source_page()
    update_source_index()
    update_knowledge_facts()
    update_disease_page()
    evidence_path = write_evidence_expansion()
    extract_path = write_pdf_page_extract()
    report_path = write_execution_report(source_page, evidence_path, extract_path)
    refresh_fact_status()
    print(
        json.dumps(
            {
                "source_added": SOURCE_UPDATE["source_id"],
                "facts_added": len(FACTS_TO_ADD),
                "runtime_page_updated": DISEASE.relative_to(ROOT).as_posix(),
                "evidence_expansion": evidence_path,
                "raw_extract": extract_path,
                "report": report_path,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
