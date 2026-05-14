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
DISEASE = ROOT / "wiki" / "diseases" / "DIS-051-streptococcosis-streptococcus-suis.md"
EVIDENCE_DIR = ROOT / "wiki" / "evidence_expansions" / "diseases" / "phase4_runtime_compaction" / "DIS-051-streptococcosis-streptococcus-suis"
ISSUES = ROOT / "issues"
TZ = timezone(timedelta(hours=8))

UPDATED_AT = "2026-05-13T23:35:00+08:00"

SOURCE_ID = "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026"
SOURCE_FILE = "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026.md"
SOURCE_URL = "https://www.merckvetmanual.com/generalized-conditions/streptococcal-infections-in-pigs/streptococcus-suis-infection-in-pigs"

SOURCE_TEXT = """---
type: source
source_id: A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026
source_path: https://www.merckvetmanual.com/generalized-conditions/streptococcal-infections-in-pigs/streptococcus-suis-infection-in-pigs
source_type: url
authority_level: A2
legacy_evidence_status: HUMAN_REVIEWED
source_status: source_anchored
created: 2026-05-13T23:35:00+08:00
updated: 2026-05-13T23:35:00+08:00
sources: []
---

# Merck Veterinary Manual: Streptococcus suis Infection in Pigs

## 来源

- URL: https://www.merckvetmanual.com/generalized-conditions/streptococcal-infections-in-pigs/streptococcus-suis-infection-in-pigs
- 发布机构：Merck Veterinary Manual
- 发布/修订日期：Accessed 2026-05-13
- 访问日期：2026-05-13
- 权威等级：A2

## 可支持结论

- `S. suis` 是断奶后仔猪重要的细菌性病原，可导致败血症、脑膜炎、关节炎和心内膜炎。
- 临床健康猪可带菌，扁桃体是自然生态位；传播可与分娩、哺乳、保育混群和健康带菌猪调运有关。
- 诊断需结合病史、临床表现、病变、病原分离和分型；扁桃体或鼻腔检出需谨慎解释，不能直接当成致病证据。
- 防控可涉及早期识别、管理、治疗和自家疫苗讨论，但不得外推为中国处方、休药期、MRL 或监管结论。

## 不得外推边界

- 本来源仅支持国际教材级猪病事实与诊断/防控边界，不替代中国现行监管、报告、检疫、扑杀、调运、免疫程序或食品安全结论。
- 页面中的抗菌药和治疗讨论不得直接转写为固定处方、剂量、疗程、休药期或 MRL 结论。
"""

FACTS_TO_ADD = [
    {
        "fact_id": "SSUIS-101-carrier-tonsil-and-colonization",
        "fact_type": "streptococcus_suis_epidemiology",
        "subject": "猪链球菌病",
        "predicate": "s_suis_is_commonly_carried_in_upper_respiratory_tract_and_tonsils",
        "object": "S. suis 可作为猪上呼吸道常在菌存在，扁桃体被视为自然生态位；临床健康猪可携带多个血清型。",
        "fact_confidence": "0.90",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page: S suis is a normal inhabitant of the upper respiratory tract ... tonsils are considered a natural niche; clinically healthy pigs are carriers of multiple serotypes.",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-102-transmission-colonization-mixing",
        "fact_type": "streptococcus_suis_transmission",
        "subject": "猪链球菌病",
        "predicate": "piglets_acquire_colonization_during_parturition_nursing_and_postweaning_mixing",
        "object": "仔猪可在分娩、哺乳过程中获得定植，保育期失去母源抗体后，亚临床带菌猪在混群时可成为同栏猪感染来源。",
        "fact_confidence": "0.90",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page: Piglets become colonized during parturition and while nursing; subclinical carriers serve as a source of infection after mixing and commingling in the nursery.",
        "applies_to_species": "swine",
        "applies_to_stage": "piglets_weaned_pigs",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-103-herd-to-herd-carrier-movement",
        "fact_type": "streptococcus_suis_transmission",
        "subject": "猪链球菌病",
        "predicate": "between_herd_transmission_occurs_via_movement_of_healthy_carrier_pigs",
        "object": "猪群间传播可经健康带菌猪调运和混群发生；高毒力菌株进入易感猪群后可在断奶猪中引发临床病。",
        "fact_confidence": "0.89",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page: Transmission between herds occurs by movement and mixing of healthy carrier pigs; introduction of a highly virulent strain into a naive herd may result in disease.",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-104-clinical-septicemia-meningitis-arthritis",
        "fact_type": "streptococcus_suis_clinical_pattern",
        "subject": "猪链球菌病",
        "predicate": "principal_clinical_patterns_include_septicemia_meningitis_polyarthritis_and_sudden_death",
        "object": "猪链球菌病主要临床模式包括败血症、猝死、脑膜炎、多发性关节炎和心内膜炎，最常见于断奶后仔猪。",
        "fact_confidence": "0.92",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page summary and clinical findings: causing mainly septicemia with sudden death, meningitis, arthritis, and endocarditis, mostly in postweaned piglets.",
        "applies_to_species": "swine",
        "applies_to_stage": "postweaned_piglets",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-105-early-clinical-signs-and-age-window",
        "fact_type": "streptococcus_suis_clinical_pattern",
        "subject": "猪链球菌病",
        "predicate": "early_signs_include_fever_inappetence_depression_lameness_and_possible_peracute_death",
        "object": "早期可见发热、食欲下降、沉郁和游走性跛行；急性败血型病例可在无明显前驱症状时死亡，4至9周龄断奶后仔猪最易感。",
        "fact_confidence": "0.91",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page: earliest sign is fever ... inappetence, depression, shifting lameness; peracute pigs may be found dead; most susceptible mainly 4 to 9 weeks old.",
        "applies_to_species": "swine",
        "applies_to_stage": "postweaned_piglets",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-106-lesions-meningitis-serositis-septicemia",
        "fact_type": "streptococcus_suis_lesions",
        "subject": "猪链球菌病",
        "predicate": "principal_lesions_include_meningitis_arthritis_endocarditis_polyserositis_and_septicemia_signs",
        "object": "主要病变可见脑膜炎、关节炎、心内膜炎、类似副猪嗜血杆菌病的多发性浆膜炎，以及脾大和点状出血等败血症表现。",
        "fact_confidence": "0.91",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page lesions: lymphadenopathy, meningitis, arthritis, endocarditis, polyserositis, splenomegaly, petechial hemorrhages indicating septicemia.",
        "applies_to_species": "swine",
        "applies_to_stage": "weaned_piglets",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-107-diagnosis-history-culture-serotyping",
        "fact_type": "streptococcus_suis_diagnostics",
        "subject": "猪链球菌病",
        "predicate": "presumptive_diagnosis_uses_history_signs_lesions_and_confirmation_requires_isolation_with_typing",
        "object": "初步诊断需结合病史、临床表现、年龄和肉眼病变；确诊应有病原分离、分型，必要时辅以显微病理。",
        "fact_confidence": "0.92",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page diagnosis: presumptive diagnosis based on history, clinical signs, age, gross lesions; isolation and serotyping confirm diagnosis.",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-108-diagnosis-tonsil-nasal-boundary",
        "fact_type": "streptococcus_suis_diagnostics",
        "subject": "猪链球菌病",
        "predicate": "tonsil_or_nasal_detection_of_virulent_strains_does_not_by_itself_establish_causation",
        "object": "由于扁桃体和鼻腔本就是常见定植部位，单独在这些部位检出毒力株不能直接证明其为临床病因，且分离株需 PCR 确认真实 S. suis 身份。",
        "fact_confidence": "0.93",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page: detection of virulent strains from tonsils or nasal cavities should be avoided ... normal inhabitant; strains isolated from tonsils must be confirmed by PCR assay.",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
    {
        "fact_id": "SSUIS-109-differential-glaesser-actinobacillus-others",
        "fact_type": "streptococcus_suis_differential",
        "subject": "猪链球菌病",
        "predicate": "differentials_include_g_parasuis_actinobacillus_suis_e_coli_erysipelas_salmonella_and_other_joint_pathogens",
        "object": "鉴别诊断需区分格拉瑟氏病、放线杆菌败血症、大肠杆菌、猪丹毒、沙门氏菌病及其他链球菌/葡萄球菌性关节炎等。",
        "fact_confidence": "0.90",
        "evidence_source": "Merck Veterinary Manual",
        "evidence_source_id": "A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026",
        "evidence_url": SOURCE_URL,
        "evidence_quote_span": "Merck page differentials: meningitis caused by G parasuis; septicemia caused by G parasuis, Actinobacillus suis, E coli, Erysipelothrix rhusiopathiae, or Salmonella Choleraesuis; polyarthritis caused by other pathogens.",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval", "gold_candidate"],
    },
]

RUNTIME_BLOCK = """
## Authority Web Refresh / 2026-05-13

- This additive refresh supplements the existing local textbook and China A0 boundary sources with a Merck Veterinary Manual A2 page, using explicit `fact_id/source_id/anchor` metadata so the update can be audited and admitted into the `wiki-native` 主图谱.
- The refresh is limited to epidemiology, transmission, clinical pattern, lesion, diagnosis, differential diagnosis, and control boundaries. It does not authorize executable antimicrobial regimen, dose, route, withdrawal period, MRL, culling, movement-control, or jurisdiction-specific regulatory actions.

## 传播途径

- 临床健康猪可带有多个血清型的 `S. suis`，其上呼吸道尤其扁桃体可作为自然生态位。`fact_id=SSUIS-101-carrier-tonsil-and-colonization; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Epidemiology and Transmission`
- 仔猪可在分娩和哺乳过程中获得定植，保育期混群时亚临床带菌猪可成为同栏感染来源。`fact_id=SSUIS-102-transmission-colonization-mixing; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Epidemiology and Transmission`
- 猪群间传播可通过健康带菌猪的调运和混群发生；高毒力菌株进入易感猪群后可在断奶猪中引发临床病。`fact_id=SSUIS-103-herd-to-herd-carrier-movement; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Epidemiology and Transmission`

## 临床症状

- 猪链球菌病主要表现为败血症、猝死、脑膜炎、多发性关节炎和心内膜炎，最常见于断奶后仔猪。`fact_id=SSUIS-104-clinical-septicemia-meningitis-arthritis; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Clinical Findings`
- 早期可见发热、食欲下降、沉郁和游走性跛行；急性败血型病例可在缺乏明显前驱症状时死亡。`fact_id=SSUIS-105-early-clinical-signs-and-age-window; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Clinical Findings`

## 剖检变化

- 主要病变可见脑膜炎、关节炎、心内膜炎、纤维素性浆膜炎，以及脾大和点状出血等败血症表现。`fact_id=SSUIS-106-lesions-meningitis-serositis-septicemia; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Lesions`

## 实验室诊断

- 初步诊断应结合病史、临床表现、年龄和肉眼病变；确诊需有病原分离、分型，必要时辅以显微病理。`fact_id=SSUIS-107-diagnosis-history-culture-serotyping; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Diagnosis`
- 由于扁桃体和鼻腔是常见定植部位，单独从这些部位检出毒力株不能直接证明其为致病原因；相关分离株需 PCR 等方法确认真实 `S. suis` 身份。`fact_id=SSUIS-108-diagnosis-tonsil-nasal-boundary; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Diagnosis`

## 鉴别诊断

- 脑膜炎、败血症和多发性关节炎场景需与格拉瑟氏病、放线杆菌败血症、大肠杆菌、猪丹毒、沙门氏菌病及其他化脓性关节炎病原区分。`fact_id=SSUIS-109-differential-glaesser-actinobacillus-others; source_id=A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026; anchor=Merck Veterinary Manual Streptococcus suis Infection in Pigs / Diagnosis`

## 防控要点

- 本次 A2 补充支持病例识别、鉴别诊断排序、实验室解释和评估打分；若问题进入药物执行、休药期、MRL、扑杀、报告、调运、屠宰和食品安全，仍必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应 A0/A1 来源。
"""

EVIDENCE_EXPANSION_TEXT = """
# DIS-051 Streptococcus suis Authority Web Refresh / 2026-05-13

## Scope

This evidence expansion records the real authority-source refresh for `DIS-051-streptococcosis-streptococcus-suis`.

## Source Added

- `A2-MERCK-STREPTOCOCCUS-SUIS-PIGS-2026`

## Why This Refresh Was Needed

- Before this refresh, the runtime page still declared evidence gaps for transmission, clinical signs, lesions, laboratory diagnosis, differential diagnosis, and control points.
- The page existed in the wiki but had `evidence_units=0` and `page_gold_ready=false` in the current `wiki-native` build report, which meant the main graph could not admit verified semantic edges from this page.

## Facts Added

- `SSUIS-101-carrier-tonsil-and-colonization`
- `SSUIS-102-transmission-colonization-mixing`
- `SSUIS-103-herd-to-herd-carrier-movement`
- `SSUIS-104-clinical-septicemia-meningitis-arthritis`
- `SSUIS-105-early-clinical-signs-and-age-window`
- `SSUIS-106-lesions-meningitis-serositis-septicemia`
- `SSUIS-107-diagnosis-history-culture-serotyping`
- `SSUIS-108-diagnosis-tonsil-nasal-boundary`
- `SSUIS-109-differential-glaesser-actinobacillus-others`

## Governance Boundary

- This refresh is additive and does not silently delete existing textbook or A0 regulatory evidence.
- China official outbreak/control handling still routes to `A0-MOA-STREP-SUIS-CONTROL-2005` and rule cards.
- Merck A2 evidence is used here for disease facts, differential diagnosis, and laboratory interpretation boundaries, not for executable drug or regulatory conclusions.
"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def write_source_page() -> str:
    path = SOURCES / SOURCE_FILE
    write_text(path, SOURCE_TEXT)
    return path.relative_to(ROOT).as_posix()


def update_source_index() -> None:
    path = EXPORTS / "source_index.csv"
    rows, fieldnames = read_csv(path)
    if not fieldnames:
        fieldnames = ["source_id", "title", "pages", "evidence_coverage", "relpath"]
    by_id = {row.get("source_id", ""): row for row in rows if row.get("source_id")}
    by_id[SOURCE_ID] = {
        "source_id": SOURCE_ID,
        "title": "Merck Veterinary Manual: Streptococcus suis Infection in Pigs",
        "pages": SOURCE_URL,
        "evidence_coverage": "complete",
        "relpath": f"wiki/sources/{SOURCE_FILE}",
    }
    write_csv(path, sorted(by_id.values(), key=lambda row: row.get("source_id", "")), fieldnames)


def update_knowledge_facts() -> None:
    path = EXPORTS / "knowledge_facts.json"
    facts = json.loads(path.read_text(encoding="utf-8"))
    by_id = {fact.get("fact_id"): fact for fact in facts if isinstance(fact, dict) and fact.get("fact_id")}
    for fact in FACTS_TO_ADD:
        by_id[fact["fact_id"]] = fact
    path.write_text(json.dumps(list(by_id.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_disease_page() -> None:
    text = DISEASE.read_text(encoding="utf-8")
    if SOURCE_ID not in text.split("---", 2)[1]:
        text = text.replace("sources: [", f"sources: [{SOURCE_ID}, ", 1)
    marker = "## Authority Web Refresh / 2026-05-13"
    if marker not in text:
        insert_after = "## 用药/处置边界\n"
        if insert_after in text:
            anchor = "## 本地证据"
            if anchor in text:
                text = text.replace(anchor, RUNTIME_BLOCK.strip() + "\n\n" + anchor, 1)
            else:
                text = text.rstrip() + "\n\n" + RUNTIME_BLOCK.strip() + "\n"
    DISEASE.write_text(text, encoding="utf-8")


def write_evidence_expansion() -> str:
    path = EVIDENCE_DIR / "009-Authority-Web-Refresh-2026-05-13.md"
    write_text(path, EVIDENCE_EXPANSION_TEXT.strip() + "\n")
    return path.relative_to(ROOT).as_posix()


def refresh_fact_status() -> None:
    script = ROOT / "tools" / "wiki_ops" / "standardize_source_fact_status.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT.parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-4000:] or result.stdout[-4000:])


def write_execution_report(source_page: str, evidence_path: str) -> str:
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "target": "DIS-051 streptococcosis / Streptococcus suis",
        "mode": "web_access_authority_refresh",
        "crud_action": "create/update",
        "source_added": SOURCE_ID,
        "facts_added": [fact["fact_id"] for fact in FACTS_TO_ADD],
        "source_page": source_page,
        "runtime_page": DISEASE.relative_to(ROOT).as_posix(),
        "evidence_expansion": evidence_path,
        "old_data_handling": "keep_existing_additive_refresh",
        "runtime_impact": "update",
        "gold_dataset_impact": "page may become gold-ready after native graph rebuild",
        "boundary": "A2 disease facts only; no executable drug or China regulatory override.",
    }
    path = ISSUES / "dis051_streptococcus_suis_authority_web_refresh_2026-05-13.json"
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    require_guarded_update()
    source_page = write_source_page()
    update_source_index()
    update_knowledge_facts()
    update_disease_page()
    evidence_path = write_evidence_expansion()
    refresh_fact_status()
    report_path = write_execution_report(source_page, evidence_path)
    print(
        json.dumps(
            {
                "source_added": SOURCE_ID,
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
