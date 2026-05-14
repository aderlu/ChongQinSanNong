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
ISSUES = ROOT / "issues"
TZ = timezone(timedelta(hours=8))

UPDATED_AT = "2026-05-12T00:00:00+08:00"
ACCESSED = "2026-05-12"


SOURCE_UPDATES = {
    "A1-USDA-APHIS-SWINE-BRUCELLOSIS": {
        "file": "A1-USDA-APHIS-SWINE-BRUCELLOSIS.md",
        "title": "USDA APHIS swine brucellosis information",
        "url": "https://www.aphis.usda.gov/livestock-poultry-disease/swine/swine-brucellosis",
        "publisher": "USDA Animal and Plant Health Inspection Service (APHIS)",
        "page_last_modified": "2025-07-30",
        "authority_level": "A1",
        "usable_boundary": [
            "Use for swine brucellosis disease identity, B. suis causation, reproductive-loss and lameness pattern, wild-swine reservoir/exposure boundary, zoonotic warning, and US report-routing language.",
            "Use as an animal-health authority anchor for bounded generation and evaluation prompts.",
        ],
        "do_not_extrapolate": [
            "Do not use this source alone for China-specific reporting, quarantine, culling, movement, compensation, slaughter, food-chain release, drug dose, withdrawal period, or MRL claims.",
            "Do not turn the US reporting text into jurisdiction-free execution orders.",
        ],
    },
    "A1-WOAH-BRUCELLOSIS": {
        "file": "A1-WOAH-BRUCELLOSIS.md",
        "title": "WOAH brucellosis disease page",
        "url": "https://www.woah.org/en/disease/brucellosis/",
        "publisher": "World Organisation for Animal Health (WOAH)",
        "page_last_modified": "not stated on extracted page",
        "authority_level": "A1",
        "usable_boundary": [
            "Use for Brucella spp. disease identity, B. suis/swine inclusion, WOAH listed-disease/reportability framing, zoonotic boundary, transmission via birth fluids/environment/mucosa, and diagnostic confirmation boundary.",
            "Use with MOA China brucellosis sources when questions ask for China-specific animal disease control.",
        ],
        "do_not_extrapolate": [
            "Do not infer China-specific disposal, compensation, movement-control, vaccination, or official herd action rules from this international page.",
            "Do not infer human diagnosis/treatment or species-specific prevalence beyond the page text.",
        ],
    },
    "A2-CDC-BRUCELLOSIS": {
        "file": "A2-CDC-BRUCELLOSIS.md",
        "title": "CDC brucellosis public-health page",
        "url": "https://www.cdc.gov/brucellosis/about/index.html",
        "publisher": "U.S. Centers for Disease Control and Prevention",
        "page_last_modified": "2024-05-02",
        "authority_level": "A2",
        "usable_boundary": [
            "Use for public-health, occupational exposure, hunting/wild-hog exposure, animal-product exposure, and laboratory exposure boundaries.",
            "Use as support when distinguishing human health risk from animal disease control.",
        ],
        "do_not_extrapolate": [
            "Do not use as the primary source for swine herd control, China animal policy, pig clinical signs, veterinary testing, culling, vaccination, or treatment protocols.",
            "Do not import human antibiotic treatment details into swine disease runtime guidance.",
        ],
    },
}


FACTS_TO_ADD = [
    {
        "fact_id": "DIS038-WEB-001-aphis-causation-reproductive-zoonotic",
        "fact_type": "brucellosis_authority_boundary",
        "subject": "猪布鲁氏菌病",
        "predicate": "aphis_b_suis_reproductive_zoonotic_boundary",
        "object": "USDA APHIS identifies swine brucellosis as an infectious disease caused by Brucella suis, describes chronic inflammatory lesions in reproductive organs with abortion, infertility and weak piglets, notes possible joint involvement with lameness, and warns that infected pigs can expose people.",
        "fact_confidence": "high",
        "evidence_source": "USDA APHIS swine brucellosis information",
        "evidence_source_id": "A1-USDA-APHIS-SWINE-BRUCELLOSIS",
        "evidence_url": "https://www.aphis.usda.gov/livestock-poultry-disease/swine/swine-brucellosis",
        "evidence_quote_span": "web-access CDP extract; title Disease Alert: Swine Brucellosis; accessed 2026-05-12",
        "evidence_status": "HUMAN_REVIEWED",
        "source_status": "source_anchored",
        "fact_validity": "valid",
        "authority_level": "A1",
        "risk_class": "public_health",
        "task_use_status": "generation_ready_limited",
        "applies_to_species": "swine",
        "applies_to_stage": "breeding_herd",
        "jurisdiction": "United States official animal-health reference",
        "target_page": "wiki/diseases/DIS-038-brucella-suis-brucellosis.md",
    },
    {
        "fact_id": "DIS038-WEB-002-aphis-wild-swine-and-report-routing",
        "fact_type": "brucellosis_reservoir_reporting_boundary",
        "subject": "猪布鲁氏菌病",
        "predicate": "aphis_wild_swine_reservoir_and_us_report_routing_boundary",
        "object": "USDA APHIS states the disease was eliminated from US commercial swine in 2011 but remains present in wild swine, making pigs exposed to feral swine at risk; suspected herd disease should route through an accredited veterinarian and US reportable-disease channels as applicable.",
        "fact_confidence": "high",
        "evidence_source": "USDA APHIS swine brucellosis information",
        "evidence_source_id": "A1-USDA-APHIS-SWINE-BRUCELLOSIS",
        "evidence_url": "https://www.aphis.usda.gov/livestock-poultry-disease/swine/swine-brucellosis",
        "evidence_quote_span": "web-access CDP extract; title Disease Alert: Swine Brucellosis; accessed 2026-05-12",
        "evidence_status": "HUMAN_REVIEWED",
        "source_status": "source_anchored",
        "fact_validity": "valid",
        "authority_level": "A1",
        "risk_class": "high_regulatory",
        "task_use_status": "generation_ready_limited",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "United States official animal-health reference",
        "target_page": "wiki/diseases/DIS-038-brucella-suis-brucellosis.md",
    },
    {
        "fact_id": "DIS038-WEB-003-woah-listed-transmission-diagnostic",
        "fact_type": "brucellosis_international_boundary",
        "subject": "布鲁氏菌病",
        "predicate": "woah_listed_transmission_and_diagnostic_boundary",
        "object": "WOAH frames B. suis in swine as a listed brucellosis disease, describes reproductive failure/abortion with bacterial shedding in birth fluids and environmental persistence under cool moist conditions, and states diagnostic confirmation requires serology followed by prescribed laboratory tests to isolate and identify the bacteria.",
        "fact_confidence": "high",
        "evidence_source": "WOAH brucellosis disease page",
        "evidence_source_id": "A1-WOAH-BRUCELLOSIS",
        "evidence_url": "https://www.woah.org/en/disease/brucellosis/",
        "evidence_quote_span": "web-access CDP extract; title Brucellosis - WOAH; accessed 2026-05-12",
        "evidence_status": "HUMAN_REVIEWED",
        "source_status": "source_anchored",
        "fact_validity": "valid",
        "authority_level": "A1",
        "risk_class": "diagnostic",
        "task_use_status": "generation_ready_limited",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "international animal-health reference",
        "target_page": "wiki/diseases/DIS-038-brucella-suis-brucellosis.md",
    },
    {
        "fact_id": "DIS038-WEB-004-cdc-occupational-public-health-boundary",
        "fact_type": "brucellosis_public_health_boundary",
        "subject": "布鲁氏菌病公共卫生边界",
        "predicate": "cdc_animal_product_occupational_and_laboratory_exposure_boundary",
        "object": "CDC identifies pigs and wild hogs among animals linked to human brucellosis exposure and lists exposure routes including contaminated animal products, inhalation, body fluids contacting mucosa, hunting/meat-hide preparation, animal-vaccine accidents, and laboratory sample work; this supports human-exposure boundaries, not swine herd-control protocols.",
        "fact_confidence": "high",
        "evidence_source": "CDC brucellosis public-health page",
        "evidence_source_id": "A2-CDC-BRUCELLOSIS",
        "evidence_url": "https://www.cdc.gov/brucellosis/about/index.html",
        "evidence_quote_span": "web-access CDP extract; title About Brucellosis | CDC; accessed 2026-05-12",
        "evidence_status": "HUMAN_REVIEWED",
        "source_status": "source_anchored",
        "fact_validity": "valid",
        "authority_level": "A2",
        "risk_class": "public_health",
        "task_use_status": "generation_ready_limited",
        "applies_to_species": "swine",
        "applies_to_stage": "human_exposure_boundary",
        "jurisdiction": "United States public-health reference",
        "target_page": "wiki/diseases/DIS-038-brucella-suis-brucellosis.md",
    },
]


RUNTIME_BLOCK = """
## Authority Web Refresh / 2026-05-12

> This additive refresh was produced through the guarded CRUD decision workflow. It strengthens source/fact anchors for swine brucellosis identity, reproductive signs, wild-swine exposure, zoonotic/public-health risk, WOAH listed-disease framing, and diagnostic/reporting boundaries. It does not replace China A0 animal-disease control sources and does not authorize local culling, movement, vaccination, slaughter, compensation, food-chain, drug, withdrawal-period, or MRL claims.

### Disease identity and swine clinical boundary

- USDA APHIS identifies swine brucellosis as an infectious disease caused by `Brucella suis`; the authority summary supports reproductive-loss patterns such as abortion, infertility and weak piglets, possible joint involvement with lameness, and human-exposure warning. `fact_id=DIS038-WEB-001-aphis-causation-reproductive-zoonotic; source_id=A1-USDA-APHIS-SWINE-BRUCELLOSIS`
- USDA APHIS states the disease was eliminated from US commercial swine in 2011 but remains present in wild swine; pigs exposed to feral swine are at risk. Suspected herd disease routes through an accredited veterinarian and US reportable-disease channels where applicable, not through model-generated execution orders. `fact_id=DIS038-WEB-002-aphis-wild-swine-and-report-routing; source_id=A1-USDA-APHIS-SWINE-BRUCELLOSIS`

### WOAH and diagnostic boundary

- WOAH frames `B. suis` in swine as a listed brucellosis disease, describes reproductive failure/abortion with shedding in birth fluids and environmental persistence under cool moist conditions, and keeps confirmation tied to serology plus prescribed laboratory tests to isolate and identify the bacteria. `fact_id=DIS038-WEB-003-woah-listed-transmission-diagnostic; source_id=A1-WOAH-BRUCELLOSIS`

### Public-health exposure boundary

- CDC supports human-exposure boundaries for infected animals or contaminated animal products, including pigs and wild hogs, occupational animal/body-fluid exposure, hunting/meat-hide preparation, animal-vaccine accidents, and laboratory sample work. This source must not be used as the primary swine herd-control protocol. `fact_id=DIS038-WEB-004-cdc-occupational-public-health-boundary; source_id=A2-CDC-BRUCELLOSIS`

### Enforcement boundary

- These A1/A2 authority sources strengthen retrieval, differential, diagnostic-boundary, report-routing, and public-health exposure answers only. China-specific reporting, quarantine, culling, movement, vaccination program, slaughter, compensation, food-chain release, drug dose, withdrawal period, and MRL claims must still route to current China A0/A1 sources and rule cards.
"""


EVIDENCE_EXPANSION = """
# DIS-038 Brucellosis Authority Web Refresh / 2026-05-12

## Scope

This evidence expansion records the web-access authority refresh for `DIS-038-brucella-suis-brucellosis`.

## Web Access Acquisition

- Tool path used: `C:/Users/admin/.codex/skills/web-access/SKILL.md`.
- Dependency precheck: `node C:/Users/admin/.codex/skills/web-access/scripts/check-deps.mjs` passed with Node, Chrome and proxy ready.
- Acquisition method: Chrome CDP proxy opened official source pages and extracted rendered page text on 2026-05-12.

## Sources Updated

- `A1-USDA-APHIS-SWINE-BRUCELLOSIS`: USDA APHIS swine brucellosis page, last modified 2025-07-30.
- `A1-WOAH-BRUCELLOSIS`: WOAH brucellosis disease page.
- `A2-CDC-BRUCELLOSIS`: CDC About Brucellosis page, dated 2024-05-02.

## Facts Added

- `DIS038-WEB-001-aphis-causation-reproductive-zoonotic`
- `DIS038-WEB-002-aphis-wild-swine-and-report-routing`
- `DIS038-WEB-003-woah-listed-transmission-diagnostic`
- `DIS038-WEB-004-cdc-occupational-public-health-boundary`

## Governance Boundary

- This refresh is additive.
- Existing source and fact records are kept; no source, fact, runtime page, rule card or gold sample is deleted.
- A1/A2 sources do not replace China A0 official control rules.
- Runtime additions remain short source/fact-routed summaries; full web pages are not copied into runtime.
"""


def render_source_page(source_id: str, source: dict[str, object]) -> str:
    lines = [
        "---",
        "tags: [source, swine, authority, official, brucellosis, zoonosis, web_access_refresh]",
        f"source_id: {source_id}",
        "source_type: authoritative_web",
        f"authority_level: {source['authority_level']}",
        "evidence_status: HUMAN_REVIEWED",
        "source_status: source_anchored",
        f"external_url: {source['url']}",
        f"updated: {UPDATED_AT}",
        "---",
        "",
        f"# {source['title']}",
        "",
        "## Source",
        "",
        f"- URL: {source['url']}",
        f"- Publisher: {source['publisher']}",
        f"- Page last modified: {source['page_last_modified']}",
        f"- Accessed: {ACCESSED}",
        f"- Authority level: {source['authority_level']}",
        "- Evidence status: HUMAN_REVIEWED",
        "",
        "## Usable Boundary",
        "",
    ]
    lines.extend(f"- {item}" for item in source["usable_boundary"])
    lines.extend(["", "## Do-not-extrapolate Boundary", ""])
    lines.extend(f"- {item}" for item in source["do_not_extrapolate"])
    lines.extend(
        [
            "",
            "## 可支持结论",
            "",
            "- 支持范围以本页来源摘要、URL/path、页码/章节、表格和已登记 facts 为准。",
            "",
            "## 不得外推边界",
            "",
            "- 不得超出 `authority_level` 和原文明确支持范围；剂量、疗程、休药期、MRL、残留、食品安全、检疫、扑杀、调运、报告等高风险结论必须另有 A0 或标签级等价来源支持。",
            "",
        ]
    )
    return "\n".join(lines)


def write_source_pages() -> list[str]:
    written: list[str] = []
    for source_id, source in SOURCE_UPDATES.items():
        path = SOURCES / str(source["file"])
        path.write_text(render_source_page(source_id, source), encoding="utf-8")
        written.append(path.relative_to(ROOT).as_posix())
    return written


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def update_source_index() -> None:
    path = EXPORTS / "source_index.csv"
    rows, fieldnames = read_csv(path)
    by_id = {row.get("source_id", ""): row for row in rows if row.get("source_id")}
    for source_id, source in SOURCE_UPDATES.items():
        existing = dict(by_id.get(source_id, {}))
        existing.update(
            {
                "source_id": source_id,
                "title": str(source["title"]),
                "pages": str(source["url"]),
                "evidence_status": "HUMAN_REVIEWED",
                "relpath": f"wiki/sources/{source['file']}",
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


def ensure_sources_in_frontmatter(text: str) -> str:
    head, body = text.split("---", 2)[1:]
    for source_id in SOURCE_UPDATES:
        if source_id not in head:
            head = head.replace("sources: [", f"sources: [{source_id}, ", 1)
    return f"---{head}---{body}"


def update_disease_page() -> None:
    text = DISEASE.read_text(encoding="utf-8")
    text = ensure_sources_in_frontmatter(text)
    marker = "## Authority Web Refresh / 2026-05-12"
    if marker not in text:
        text = text.rstrip() + "\n\n" + RUNTIME_BLOCK.strip() + "\n"
    DISEASE.write_text(text, encoding="utf-8")


def write_evidence_expansion() -> str:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE_DIR / "003-Authority-Web-Refresh-2026-05-12.md"
    path.write_text(EVIDENCE_EXPANSION.strip() + "\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def write_execution_report(source_pages: list[str], evidence_path: str) -> str:
    report = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "target": "DIS-038 brucella suis brucellosis",
        "mode": "web_access_authority_refresh",
        "crud_action": "update",
        "sources_updated": list(SOURCE_UPDATES),
        "facts_added": [fact["fact_id"] for fact in FACTS_TO_ADD],
        "source_pages": source_pages,
        "runtime_page": DISEASE.relative_to(ROOT).as_posix(),
        "evidence_expansion": evidence_path,
        "old_data_handling": "keep",
        "runtime_impact": "update",
        "gold_dataset_impact": "update via rebuilt fact status/readiness indexes",
        "boundary": "A1/A2 sources do not replace China A0 execution rules.",
    }
    path = ISSUES / "dis038_brucellosis_authority_web_refresh_2026-05-12.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def refresh_fact_status() -> None:
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


def main() -> None:
    require_guarded_update()
    source_pages = write_source_pages()
    update_source_index()
    update_knowledge_facts()
    update_disease_page()
    evidence_path = write_evidence_expansion()
    report_path = write_execution_report(source_pages, evidence_path)
    refresh_fact_status()
    print(
        json.dumps(
            {
                "sources_updated": len(SOURCE_UPDATES),
                "facts_added": len(FACTS_TO_ADD),
                "runtime_page_updated": DISEASE.relative_to(ROOT).as_posix(),
                "evidence_expansion": evidence_path,
                "report": report_path,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
