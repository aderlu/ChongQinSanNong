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
DISEASE = ROOT / "wiki" / "diseases" / "DIS-026-foot-and-mouth-disease-picornaviruses.md"
EVIDENCE_DIR = ROOT / "wiki" / "evidence_expansions" / "diseases" / "phase4_runtime_compaction" / "DIS-026-foot-and-mouth-disease-picornaviruses"
ISSUES = ROOT / "issues"
TZ = timezone(timedelta(hours=8))

UPDATED_AT = "2026-05-11T20:55:00+08:00"


SOURCES_TO_ADD = {
    "A1-FAO-FMD-DISEASE-2026": {
        "file": "A1-FAO-FMD-DISEASE-2026.md",
        "title": "FAO Foot-and-mouth disease official animal health page",
        "url": "https://www.fao.org/animal-health/animal-diseases/foot-and-mouth-disease/",
        "publisher": "Food and Agriculture Organization of the United Nations (FAO)",
        "body": [
            "# FAO Foot-and-mouth disease official animal health page",
            "",
            "## Source",
            "",
            "- URL: https://www.fao.org/animal-health/animal-diseases/foot-and-mouth-disease/",
            "- Publisher: Food and Agriculture Organization of the United Nations (FAO)",
            "- Accessed: 2026-05-11",
            "- Jurisdiction: international animal-health reference",
            "",
            "## Usable Boundary",
            "",
            "- Use for international FMD disease identity, food-security/trade impact, susceptible cloven-hoofed animal framing including pigs, and broad control strategy concepts such as vaccination, movement controls, and biosecurity.",
            "- Use for generation and evaluation boundaries where FMD is framed as an economically significant transboundary animal disease.",
            "",
            "## Do-not-extrapolate Boundary",
            "",
            "- Do not use this source alone for China-specific legal reporting, culling, movement restrictions, compensation, vaccine program, slaughter, food-chain release, drug dose, withdrawal period, or MRL claims.",
        ],
    },
    "A1-USDA-APHIS-FMD-DISEASE-2026": {
        "file": "A1-USDA-APHIS-FMD-DISEASE-2026.md",
        "title": "USDA APHIS Foot-and-Mouth Disease page",
        "url": "https://www.aphis.usda.gov/livestock-poultry-disease/cattle/foot-and-mouth",
        "publisher": "USDA Animal and Plant Health Inspection Service (APHIS)",
        "body": [
            "# USDA APHIS Foot-and-Mouth Disease page",
            "",
            "## Source",
            "",
            "- URL: https://www.aphis.usda.gov/livestock-poultry-disease/cattle/foot-and-mouth",
            "- Publisher: USDA Animal and Plant Health Inspection Service (APHIS)",
            "- Page last modified: 2025-07-30",
            "- Accessed: 2026-05-11",
            "- Jurisdiction: United States official animal-health reference",
            "",
            "## Usable Boundary",
            "",
            "- Use for FMD as a severe, fast-spreading disease affecting cloven-hoofed animals including pigs, sheep, goats, cattle, and deer.",
            "- Use for high-level reporting prompts and subtype/vaccine-boundary framing, including that many types/subtypes exist and immunity to one type does not protect against others.",
            "",
            "## Do-not-extrapolate Boundary",
            "",
            "- Do not use this source alone for China-specific execution rules, local quarantine/culling/movement orders, drug dose, withdrawal period, MRL, or food-chain release claims.",
        ],
    },
    "A1-USDA-APHIS-FMD-NAHLN-2026": {
        "file": "A1-USDA-APHIS-FMD-NAHLN-2026.md",
        "title": "USDA APHIS NAHLN Surveillance and Preparedness FMD section",
        "url": "https://www.aphis.usda.gov/labs/nahln/surveillance-preparedness",
        "publisher": "USDA Animal and Plant Health Inspection Service (APHIS)",
        "body": [
            "# USDA APHIS NAHLN Surveillance and Preparedness FMD section",
            "",
            "## Source",
            "",
            "- URL: https://www.aphis.usda.gov/labs/nahln/surveillance-preparedness",
            "- Publisher: USDA Animal and Plant Health Inspection Service (APHIS)",
            "- Page last modified: 2026-03-04",
            "- Accessed: 2026-05-11",
            "- Jurisdiction: United States official diagnostic-network preparedness reference",
            "",
            "## Usable Boundary",
            "",
            "- Use for laboratory preparedness and FAD investigation routing boundaries: FMD-approved NAHLN laboratories maintain training and proficiency status, and duplicate samples may support preliminary screening when official conditions are met.",
            "- Use to reinforce that preliminary screening and confirmatory testing are official-process issues, not field diagnosis by clinical signs alone.",
            "",
            "## Do-not-extrapolate Boundary",
            "",
            "- Do not use this source to infer active national FMD surveillance, local field action authority, China-specific rules, or any drug/withdrawal/MRL/food-chain claims.",
        ],
    },
}


FACTS_TO_ADD = [
    {
        "fact_id": "DIS026-WEB-001-fao-fmd-impact-control",
        "fact_type": "disease_boundary",
        "subject": "Foot-and-mouth disease in pigs",
        "predicate": "fao_transboundary_impact_and_control_boundary",
        "object": "FAO frames FMD as a highly contagious disease of cloven-hoofed animals including pigs; it is not a human-health threat but can severely affect food security, livelihoods, and trade. Broad control concepts include vaccination, movement controls, and biosecurity, but China-specific execution still requires A0 sources.",
        "fact_confidence": "high",
        "evidence_source": "FAO FMD official animal health page",
        "evidence_source_id": "A1-FAO-FMD-DISEASE-2026",
        "evidence_url": "https://www.fao.org/animal-health/animal-diseases/foot-and-mouth-disease/",
        "evidence_quote_span": "FAO Foot-and-mouth disease page; lines 47-57 in web-access open result",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "Global",
        "target_page": "wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md",
    },
    {
        "fact_id": "DIS026-WEB-002-usda-aphis-species-subtype-report",
        "fact_type": "reporting_boundary",
        "subject": "Foot-and-mouth disease in pigs",
        "predicate": "aphis_species_subtype_and_reporting_boundary",
        "object": "USDA APHIS identifies pigs among FMD-affected cloven-hoofed animals, notes multiple virus types/subtypes with type-specific immunity, and directs suspected or diagnosed reportable animal diseases to animal-health officials. This supports reporting-boundary prompts, not jurisdiction-free execution orders.",
        "fact_confidence": "high",
        "evidence_source": "USDA APHIS Foot-and-Mouth Disease page",
        "evidence_source_id": "A1-USDA-APHIS-FMD-DISEASE-2026",
        "evidence_url": "https://www.aphis.usda.gov/livestock-poultry-disease/cattle/foot-and-mouth",
        "evidence_quote_span": "APHIS FMD page; lines 180-233 in web-access open result",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "United States official reference",
        "target_page": "wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md",
    },
    {
        "fact_id": "DIS026-WEB-003-usda-nahln-fmd-preparedness",
        "fact_type": "diagnostic_boundary",
        "subject": "Foot-and-mouth disease laboratory diagnosis",
        "predicate": "nahln_preliminary_screening_and_confirmatory_boundary",
        "object": "USDA APHIS NAHLN states that there is not an active national FMD surveillance program in NAHLN laboratories, but FMD-approved laboratories maintain training and proficiency for preparedness; during a foreign animal disease investigation, duplicate samples may support preliminary screening while confirmatory testing follows official channels.",
        "fact_confidence": "high",
        "evidence_source": "USDA APHIS NAHLN Surveillance and Preparedness",
        "evidence_source_id": "A1-USDA-APHIS-FMD-NAHLN-2026",
        "evidence_url": "https://www.aphis.usda.gov/labs/nahln/surveillance-preparedness",
        "evidence_quote_span": "APHIS NAHLN Surveillance and Preparedness; lines 229-232 in web-access open result",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "United States official reference",
        "target_page": "wiki/diseases/DIS-026-foot-and-mouth-disease-picornaviruses.md",
    },
]


RUNTIME_BLOCK = """
## Authority Web Refresh / 2026-05-11

> This additive refresh was produced through the guarded CRUD decision workflow. It adds international authority anchors for FMD impact, reporting, and diagnostic-preparedness boundaries. It does not replace China A0 control rules and does not authorize local culling, movement, vaccination, slaughter, food-chain, drug, withdrawal-period, or MRL claims.

### International disease and impact boundary

- FAO frames FMD as a highly contagious disease of cloven-hoofed animals including pigs; it is not a human-health threat but can severely affect food security, livelihoods, and trade. Broad control concepts include vaccination, movement controls, and biosecurity, but China-specific execution still requires A0 sources. `fact_id=DIS026-WEB-001-fao-fmd-impact-control; source_id=A1-FAO-FMD-DISEASE-2026`

### Reporting and subtype boundary

- USDA APHIS identifies pigs among FMD-affected cloven-hoofed animals, notes multiple virus types/subtypes with type-specific immunity, and directs suspected or diagnosed reportable animal diseases to animal-health officials. This supports reporting-boundary prompts, not jurisdiction-free execution orders. `fact_id=DIS026-WEB-002-usda-aphis-species-subtype-report; source_id=A1-USDA-APHIS-FMD-DISEASE-2026`

### Laboratory preparedness boundary

- USDA APHIS NAHLN states that there is not an active national FMD surveillance program in NAHLN laboratories, but FMD-approved laboratories maintain training and proficiency for preparedness; during a foreign animal disease investigation, duplicate samples may support preliminary screening while confirmatory testing follows official channels. `fact_id=DIS026-WEB-003-usda-nahln-fmd-preparedness; source_id=A1-USDA-APHIS-FMD-NAHLN-2026`

### Enforcement boundary

- These A1 sources strengthen international retrieval and diagnostic/reporting boundaries only. China-specific reporting, quarantine, culling, movement, vaccination program, slaughter, compensation, food-chain release, drug dose, withdrawal period, and MRL claims must still route to `A0-MOA-573`, `A0-MOA-FMD-CONTROL-GUIDE-2024`, `A0-MOA-ANIMAL-DISEASE-MONITORING-2021-2025`, current official implementation documents, and rule cards.
"""


EVIDENCE_EXPANSION = """
# DIS-026 FMD Authority Web Refresh / 2026-05-11

## Scope

This evidence expansion records the web-access authority refresh for `DIS-026-foot-and-mouth-disease-picornaviruses`.

## Sources Added

- `A1-FAO-FMD-DISEASE-2026`: FAO official FMD animal-health page.
- `A1-USDA-APHIS-FMD-DISEASE-2026`: USDA APHIS FMD disease page.
- `A1-USDA-APHIS-FMD-NAHLN-2026`: USDA APHIS NAHLN surveillance and preparedness page.

## Facts Added

- `DIS026-WEB-001-fao-fmd-impact-control`
- `DIS026-WEB-002-usda-aphis-species-subtype-report`
- `DIS026-WEB-003-usda-nahln-fmd-preparedness`

## Governance Boundary

- This refresh is additive.
- Existing A0 China official anchors remain controlling for China-specific reporting, quarantine, culling, movement, vaccination program, slaughter, compensation, food-chain, drug, withdrawal-period, and MRL claims.
- A1 international/US sources are used for retrieval, international disease framing, diagnostic preparedness, and evaluation traps only.
"""


def source_frontmatter(source_id: str, source: dict[str, object]) -> str:
    return "\n".join(
        [
            "---",
            "tags: [source, swine, authority, web_access, fmd, dis026]",
            f"source_id: {source_id}",
            "source_type: official_web_page",
            "authority_level: A1",
            "evidence_status: HUMAN_REVIEWED",
            "source_status: source_anchored",
            f"updated: {UPDATED_AT}",
            f"external_url: {source['url']}",
            "---",
            "",
        ]
    )


def write_source_pages() -> list[str]:
    written: list[str] = []
    for source_id, source in SOURCES_TO_ADD.items():
        path = SOURCES / str(source["file"])
        text = source_frontmatter(source_id, source) + "\n".join(source["body"]).rstrip() + "\n"
        path.write_text(text, encoding="utf-8")
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
    if not fieldnames:
        fieldnames = ["source_id", "title", "pages", "evidence_status", "relpath"]
    by_id = {row.get("source_id", ""): row for row in rows if row.get("source_id")}
    for source_id, source in SOURCES_TO_ADD.items():
        by_id[source_id] = {
            "source_id": source_id,
            "title": str(source["title"]),
            "pages": str(source["url"]),
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": f"wiki/sources/{source['file']}",
        }
    write_csv(path, sorted(by_id.values(), key=lambda row: row.get("source_id", "")), fieldnames)


def update_knowledge_facts() -> None:
    path = EXPORTS / "knowledge_facts.json"
    facts = json.loads(path.read_text(encoding="utf-8-sig"))
    by_id = {fact.get("fact_id"): fact for fact in facts if isinstance(fact, dict) and fact.get("fact_id")}
    for fact in FACTS_TO_ADD:
        by_id[fact["fact_id"]] = fact
    path.write_text(json.dumps(list(by_id.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_disease_page() -> None:
    text = DISEASE.read_text(encoding="utf-8")
    for source_id in SOURCES_TO_ADD:
        if source_id not in text.split("---", 2)[1]:
            text = text.replace("sources: [", f"sources: [{source_id}, ", 1)
    marker = "## Authority Web Refresh / 2026-05-11"
    if marker not in text:
        text = text.rstrip() + "\n\n" + RUNTIME_BLOCK.strip() + "\n"
    DISEASE.write_text(text, encoding="utf-8")


def write_evidence_expansion() -> str:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE_DIR / "010-Authority-Web-Refresh-2026-05-11.md"
    path.write_text(EVIDENCE_EXPANSION.strip() + "\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def write_execution_report(source_pages: list[str], evidence_path: str) -> str:
    report = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "target": "DIS-026 foot-and-mouth disease",
        "mode": "web_access_authority_refresh",
        "crud_action": "create/update",
        "sources_added": list(SOURCES_TO_ADD),
        "facts_added": [fact["fact_id"] for fact in FACTS_TO_ADD],
        "source_pages": source_pages,
        "runtime_page": DISEASE.relative_to(ROOT).as_posix(),
        "evidence_expansion": evidence_path,
        "old_data_handling": "keep",
        "runtime_impact": "update",
        "gold_dataset_impact": "update via rebuilt fact status/readiness indexes",
        "boundary": "A1 sources do not replace China A0 execution rules.",
    }
    path = ISSUES / "dis026_fmd_authority_web_refresh_2026-05-11.json"
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
                "sources_added": len(SOURCES_TO_ADD),
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
