from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
FACTS = WIKI / "exports" / "knowledge_facts.json"
NOW = datetime.now(timezone.utc).isoformat()


PAGE_FACTS = {
    "DIS-003-anelloviruses-torque-teno-sus-viruses.md": [
        "TTSUV-001-causal-role-not-established",
        "TTSUV-004-public-health-boundary",
        "TTSUV-005-no-specific-clinical-signs",
        "TTSUV-006-diagnosis",
    ],
    "DIS-004-astroviruses.md": [
        "PASTV-001-causal-role-obscure",
        "PASTV-004-zoonotic-potential-unclear",
        "PASTV-005-epidemiology-worldwide-high-prevalence",
        "PASTV-006-transmission-and-extraintestinal-detection",
        "PASTV-007-pathogenesis-complexity",
        "PASTV-008-diagnosis-limitations",
        "PASTV-009-control-boundary",
    ],
    "DIS-005-bunyaviruses-akabane-lumbo-oya-tahyna.md": [
        "BUNYA-001-swine-susceptibility-boundary",
        "BUNYA-004-public-health-boundary",
        "BUNYA-005-vector-and-geography",
        "BUNYA-006-akabane-serology-maternal-antibody",
        "BUNYA-008-clinical-lesion-boundary",
        "BUNYA-009-diagnostic-methods",
        "BUNYA-010-control-boundary",
    ],
    "DIS-006-caliciviruses-norovirus-sapovirus-vesicular-exanthema-virus.md": [
        "CALI-004-ves-clinical-indistinguishable",
        "CALI-008-ves-diagnosis-differentiation",
        "CALI-009-porcine-noro-sapo-recognition",
        "CALI-010-human-calicivirus-reservoir-boundary",
        "CALI-012-porcine-calicivirus-diagnostics",
    ],
    "DIS-014-filoviruses-reston-ebolavirus-zaire-ebolavirus.md": [
        "FILO-001-swine-relevance-restv-ebov",
        "RESTV-001-swine-field-infection",
        "RESTV-002-clinical-signs-boundary",
        "EBOV-001-field-vs-experimental",
        "EBOV-006-diagnosis-bsl4-boundary",
        "EBOV-007-diagnostic-methods",
    ],
    "DIS-016-west-nile-virus-and-other-flaviviruses.md": [
        "FLAVI-001-overview",
        "WNV-001-public-health",
        "WNV-002-pig-amplification-boundary",
        "WNV-003-pig-clinical-boundary",
        "WNV-004-diagnosis-cross-reaction",
    ],
    "DIS-017-hepatitis-e-virus.md": [
        "HEV-001-public-health",
        "HEV-002-fecal-oral",
        "HEV-003-subclinical-pigs",
        "HEV-004-viremia-shedding",
        "HEV-005-pork-liver-risk",
        "HEV-006-lab-boundary",
    ],
}


GENERAL_FACTS = [
    "SAM-001-diagnostic-question-drives-plan",
    "SAM-002-submission-form-context",
    "SAM-006-acute-untreated-selection",
    "SAM-010-pathogen-biology-sample-site",
    "SAM-015-fresh-samples-cross-contamination",
    "DTX-024-qpcr-not-infectivity",
    "DRG-002-benefit-risk-2aee4f263dad2d98046bb67515e900c0",
    "AUTH-017-food-animal-banned-drug-policy",
]


def line(fact: dict[str, str]) -> str:
    return (
        f"- {fact.get('object', '').strip()} "
        f"({fact.get('evidence_source_id', '')}; {fact.get('evidence_quote_span', '')})"
    )


def block(title: str, facts: list[dict[str, str]]) -> str:
    return "\n".join([f"### {title}", "", *(line(f) for f in facts), ""])


def main() -> None:
    facts = json.loads(FACTS.read_text(encoding="utf-8"))
    by_id = {str(f.get("fact_id")): f for f in facts}
    general = [by_id[fid] for fid in GENERAL_FACTS if fid in by_id]
    sampling = [f for f in general if f["fact_id"].startswith(("SAM-", "DTX-"))]
    drug = [f for f in general if f["fact_id"].startswith(("DRG-", "AUTH-017"))]

    touched: list[str] = []
    for filename, fact_ids in PAGE_FACTS.items():
        path = WIKI / "wiki" / "diseases" / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        marker = "## Low Frequency Virus QA Reinforcement / V7"
        if marker in text:
            continue
        specific = [by_id[fid] for fid in fact_ids if fid in by_id]
        payload = [
            "",
            marker,
            "",
            f"> {NOW} added for swine QA dataset generation. This block uses Diseases of Swine 11e HUMAN_REVIEWED facts and does not create dose, withdrawal-period, culling, quarantine or public-health execution instructions.",
            "",
            block("病原、临床和因果边界", specific),
            block("实验室诊断与采样边界", sampling),
            block("防控与用药边界", drug),
            "### 问答生成注意事项",
            "",
            "- 低频病毒病不得用单项检出直接定因；应写成“疑似/需鉴别/需结合共感染和病变”。",
            "- 对人兽共患或公共卫生内容，只能提示风险边界，不能生成食品召回、暴露后处置或监管执行命令。",
            "- 无商业化疫苗、无特异治疗或诊断试剂不成熟时，应转向采样、隔离观察、支持性管理和权威实验室确认。",
            "",
        ]
        path.write_text(text.rstrip() + "\n" + "\n".join(payload), encoding="utf-8", newline="\n")
        touched.append(filename)

    report = {
        "timestamp": NOW,
        "pages_reinforced": touched,
        "fact_source": "knowledge_facts.json HUMAN_REVIEWED facts from Diseases of Swine 11e plus existing boundary facts",
        "authoritative_fact_mutation": "none",
    }
    out = WIKI / "issues" / "swine_low_frequency_viruses_v7_2026-05-07.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    log = WIKI / "log.md"
    log.write_text(
        log.read_text(encoding="utf-8").rstrip()
        + f"\n- 2026-05-07 low-frequency-virus-v7 | reinforced {len(touched)} sparse viral disease pages for QA dataset generation. Report: `issues/{out.name}`.\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
