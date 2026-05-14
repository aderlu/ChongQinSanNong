from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
EXPORTS = WIKI / "exports"
ISSUES = WIKI / "issues"

NOW = datetime.now(timezone.utc).isoformat()


RULE_RELPATH_FIXES = {
    "wiki/rules/Swine-biosecurity-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-biosecurity-risk-management-not-zero-risk.md",
    "wiki/rules/Swine-drug-therapy-benefit-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-drug-therapy-benefit-risk-objective.md",
    "wiki/rules/Swine-malignant-hyperthermia-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-malignant-hyperthermia-risk-screening.md",
    "wiki/rules/Swine-gastric-ulcer-necropsy-and-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-gastric-ulcer-necropsy-and-risk-factors.md",
    "wiki/rules/Swine-controlled-exposure-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-controlled-exposure-risk-benefit.md",
    "wiki/rules/Swine-claw-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-claw-risk-conformation-floor-nutrition.md",
    "wiki/rules/Swine-tge-feedback-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-tge-feedback-risk-boundary.md",
    "wiki/rules/Swine-nipah-high-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-nipah-high-risk-zoonotic-boundary.md",
    "wiki/rules/Swine-fmd-pig-aerosol-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-fmd-pig-aerosol-risk-boundary.md",
    "wiki/rules/Swine-prrsv-live-virus-inoculation-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-prrsv-live-virus-inoculation-risk-boundary.md",
    "wiki/rules/Swine-bordetella-public-health-rare-host-risk-2aee4f263dad2d98046bb67515e900c0.md": "wiki/rules/Swine-bordetella-public-health-rare-host-risk-boundary.md",
}


TARGET_DISEASE_FACTS = {
    "DIS-043-erysipelas.md": [
        "ERYS-003-entry",
        "ERYS-005-rhomboid-lesions",
        "ERYS-006-endocarditis",
        "ERYS-007-differential",
        "ERYS-008-typing",
        "AUTH-008-erysipelas-china-class-iii",
    ],
    "DIS-057-coccidia-and-other-protozoa.md": [
        "PARA-017-cystoisospora-piglets",
        "PARA-018-coccidia-differentials",
        "PARA-019-coccidia-oocyst-boundary",
    ],
    "DIS-058-toxoplasmosis-protozoa.md": [
        "FSH-014-toxoplasma-risk-2aee4f263dad2d98046bb67515e900c0",
        "PARA-022-toxoplasma-zoonosis",
        "PARA-023-toxoplasma-cats",
        "PARA-024-toxoplasma-subclinical",
    ],
    "DIS-002-african-swine-fever-virus.md": [
        "AUTH-001-asf-china-class-i",
        "AUTH-015-asf-report-positive",
        "AUTH-018-woah-asf-no-human-health",
        "ASF-017-pcr-and-hat",
        "ASF-012-clinical-spectrum-and-differentials",
    ],
    "DIS-008-porcine-epidemic-diarrhea-virus.md": [
        "AUTH-006-ped-china-class-ii",
        "PEDV-008-diagnosis-combined-clinical-lab",
        "PEDV-006-differential",
    ],
    "DIS-009-transmissible-gastroenteritis-virus.md": [
        "TGEV-014-feedback-risk-2aee4f263dad2d98046bb67515e900c0",
        "COV-008-pcr-differentiation",
        "COV-013-paired-serum-retrospective",
    ],
    "DIS-015-japanese-encephalitis-virus.md": [
        "JEV-004-diagnosis-samples",
        "JEV-005-serology-cross-reaction",
    ],
    "DIS-018-pseudorabies-aujeszky-disease.md": [
        "PRV-004-differential",
        "AUTH-019-woah-aujeszky-notifiable-boundary",
    ],
}


GENERAL_FACT_IDS = [
    "SAM-001-diagnostic-question-drives-plan",
    "SAM-002-submission-form-context",
    "SAM-006-acute-untreated-selection",
    "SAM-010-pathogen-biology-sample-site",
    "SAM-015-fresh-samples-cross-contamination",
    "DTX-024-qpcr-not-infectivity",
    "DRG-002-benefit-risk-2aee4f263dad2d98046bb67515e900c0",
    "DRG-004-culture-sensitivity-objective",
    "DRG-022-treatment-failure-reassess-sample",
    "AUTH-017-food-animal-banned-drug-policy",
]


def load_facts() -> dict[str, dict[str, str]]:
    facts = json.loads((EXPORTS / "knowledge_facts.json").read_text(encoding="utf-8"))
    return {str(fact.get("fact_id")): fact for fact in facts}


def fact_line(fact: dict[str, str]) -> str:
    source_id = fact.get("evidence_source_id", "")
    quote = fact.get("evidence_quote_span", "")
    return f"- {fact.get('object', '').strip()} ({source_id}; {quote})"


def update_rule_index() -> list[dict[str, str]]:
    path = EXPORTS / "rule_index.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
        fieldnames = list(rows[0].keys())

    changed = []
    for row in rows:
        old = row.get("page_relpath", "")
        if old in RULE_RELPATH_FIXES:
            row["page_relpath"] = RULE_RELPATH_FIXES[old]
            changed.append({"rule_id": row["rule_id"], "old": old, "new": row["page_relpath"]})

    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return changed


def section(title: str, facts: list[dict[str, str]]) -> str:
    lines = [f"### {title}", ""]
    lines.extend(fact_line(fact) for fact in facts)
    lines.append("")
    return "\n".join(lines)


def append_disease_reinforcement(facts_by_id: dict[str, dict[str, str]]) -> list[str]:
    touched = []
    general = [facts_by_id[fid] for fid in GENERAL_FACT_IDS if fid in facts_by_id]
    for filename, fact_ids in TARGET_DISEASE_FACTS.items():
        path = WIKI / "wiki" / "diseases" / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        marker = "## Dataset QA Reinforcement / V6"
        if marker in text:
            continue
        specific = [facts_by_id[fid] for fid in fact_ids if fid in facts_by_id]
        sampling = [fact for fact in general if fact["fact_id"].startswith(("SAM-", "DTX-"))]
        drug = [fact for fact in general if fact["fact_id"].startswith(("DRG-", "AUTH-017"))]
        block = [
            "",
            marker,
            "",
            "> 2026-05-07 V6 数据集训练补强块。仅使用 HUMAN_REVIEWED 或 A0/A1 锚定事实，目标是减少微调样本中的零锚点、泛化采样建议、经验性用药和重大疫病监管外推。",
            "",
            section("实验室诊断与采样规范", sampling),
            section("本病种特异锚点", specific),
            section("鉴别诊断、防控和药物边界", drug),
            "### 生成训练样本时的硬边界",
            "",
            "- 不得把单一 PCR/qPCR 阳性、抗体阳性或卵囊检出直接写成定因结论；必须结合日龄、病程、病变、群体流行病学和采样质量。",
            "- 不得从教材页码直接外推中国上报、封锁、扑杀、调运或固定免疫程序；中国监管结论必须引用 A0/A1 来源。",
            "- 不得生成具体剂量、疗程或休药期；需要用药时只能提示按兽医处方、批准标签、药敏和本地法规复核。",
            "",
        ]
        path.write_text(text.rstrip() + "\n" + "\n".join(block), encoding="utf-8", newline="\n")
        touched.append(filename)
    return touched


def write_synthesis_page(facts_by_id: dict[str, dict[str, str]]) -> Path:
    path = WIKI / "wiki" / "synthesis" / "swine_dataset_training_quality_boundaries_v6.md"
    facts = [facts_by_id[fid] for fid in GENERAL_FACT_IDS if fid in facts_by_id]
    text = [
        "---",
        "tags: [synthesis, swine, dataset, qa, sampling, drug_boundary, regulatory_boundary]",
        f"updated: {NOW}",
        "evidence_status: HUMAN_REVIEWED",
        "sources: [SRC-0008, SRC-0009, SRC-0012, A0-MOA-573, A0-MOA-BANNED-DRUG-250-POLICY]",
        "---",
        "",
        "# Swine Dataset Training Quality Boundaries V6",
        "",
        "This page is a retrieval target for dataset generation and judging. It consolidates sampling, laboratory diagnosis, drug boundary, and regulatory boundary facts that should be injected when disease-specific pages are sparse.",
        "",
        section("Sampling and lab diagnosis", [f for f in facts if f["fact_id"].startswith(("SAM-", "DTX-"))]),
        section("Drug and treatment boundary", [f for f in facts if f["fact_id"].startswith(("DRG-", "AUTH-017"))]),
        "## Use in generation",
        "",
        "- Require at least two source anchors in every answer candidate when the case contains diagnosis, treatment, regulatory action, or sampling advice.",
        "- Prefer acute untreated representative animals for diagnostic sampling; include submission form context and sample handling details.",
        "- If the disease is A0/A1 regulated or zoonotic, include official-reporting and public-health boundaries before treatment language.",
        "- Keep all dose, course and withdrawal-period fields as boundary statements unless a verified local label source is present.",
        "",
    ]
    path.write_text("\n".join(text).rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_topic_pages(facts_by_id: dict[str, dict[str, str]]) -> list[Path]:
    topic_specs = [
        (
            "swine-laboratory-diagnosis-and-sampling-boundaries.md",
            "Swine Laboratory Diagnosis and Sampling Boundaries",
            ["SAM-001-diagnostic-question-drives-plan", "SAM-002-submission-form-context", "SAM-006-acute-untreated-selection", "SAM-010-pathogen-biology-sample-site", "SAM-015-fresh-samples-cross-contamination", "DTX-024-qpcr-not-infectivity"],
            "用于所有猪病问诊样本的实验室诊断、采样数量、采样对象、送检单和样本保存边界。",
        ),
        (
            "swine-differential-diagnosis-boundaries.md",
            "Swine Differential Diagnosis Boundaries",
            ["DTX-026-diagnostic-questions-sampling", "SAM-003-bias-order", "SAM-011-detection-not-disease-endemic", "PCV-017-qualitative-pcr-boundary", "COV-008-pcr-differentiation", "PHEV-002-diagnosis"],
            "用于阻断单一症状、单一阳性检测或单一病名直接定因，要求结合临床、病变、群体和实验室证据。",
        ),
        (
            "swine-major-disease-regulatory-boundaries.md",
            "Swine Major Disease Regulatory Boundaries",
            ["AUTH-001-asf-china-class-i", "AUTH-002-fmd-china-class-i", "AUTH-003-svd-china-class-i", "AUTH-004-csf-china-class-ii", "AUTH-005-prrs-china-class-ii", "AUTH-006-ped-china-class-ii", "AUTH-015-asf-report-positive"],
            "用于重大疫病、人兽共患和法定动物疫病问诊样本，避免把教材事实外推为中国强制处置命令。",
        ),
        (
            "swine-drug-use-and-withdrawal-boundaries.md",
            "Swine Drug Use and Withdrawal Boundaries",
            ["DRG-002-benefit-risk-2aee4f263dad2d98046bb67515e900c0", "DRG-004-culture-sensitivity-objective", "DRG-022-treatment-failure-reassess-sample", "AUTH-017-food-animal-banned-drug-policy"],
            "用于所有治疗建议样本，强调药物获益风险、培养药敏、治疗失败复核、禁用药来源和不得生成剂量/休药期。",
        ),
    ]
    paths: list[Path] = []
    for filename, title, fact_ids, purpose in topic_specs:
        page = WIKI / "wiki" / "topics" / filename
        facts = [facts_by_id[fid] for fid in fact_ids if fid in facts_by_id]
        source_ids = sorted({fact.get("evidence_source_id", "") for fact in facts if fact.get("evidence_source_id")})
        text = [
            "---",
            "tags: [topic, swine, dataset_quality, v6]",
            f"updated: {NOW}",
            "evidence_status: HUMAN_REVIEWED",
            "sources: [" + ", ".join(source_ids) + "]",
            "---",
            "",
            f"# {title}",
            "",
            purpose,
            "",
            section("Reviewed facts", facts),
            "## Dataset use",
            "",
            "- 生成问诊答案时必须写明证据锚点，优先使用 source id、PDF page、A0/A1 source page 或 rule card。",
            "- 无法确认中国标签、批准适应证、剂量、疗程或休药期时，只能输出边界说明，不能输出固定处方。",
            "- 重大动物疫病、疑似法定疫病和人兽共患风险必须先写监管/生物安全边界，再写支持性处置。",
            "",
        ]
        page.write_text("\n".join(text).rstrip() + "\n", encoding="utf-8", newline="\n")
        paths.append(page)
    return paths


def update_synthesis_index(page: Path) -> bool:
    path = EXPORTS / "synthesis_index.csv"
    rel = page.relative_to(WIKI).as_posix()
    row = {
        "page_id": page.stem,
        "title": "Swine Dataset Training Quality Boundaries V6",
        "category": "dataset_quality",
        "evidence_status": "HUMAN_REVIEWED",
        "page_relpath": rel,
    }
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
            fieldnames = list(rows[0].keys()) if rows else list(row.keys())
    else:
        rows = []
        fieldnames = list(row.keys())
    if any(existing.get("page_relpath") == rel for existing in rows):
        return False
    for key in row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows.append({key: row.get(key, "") for key in fieldnames})
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return True


def write_report(
    rule_changes: list[dict[str, str]],
    disease_pages: list[str],
    synthesis_page: Path,
    synthesis_index_added: bool,
    topic_pages: list[Path],
) -> Path:
    report = {
        "timestamp": NOW,
        "rule_index_fixes": rule_changes,
        "disease_pages_reinforced": disease_pages,
        "synthesis_page": synthesis_page.relative_to(ROOT).as_posix(),
        "synthesis_index_added": synthesis_index_added,
        "topic_pages": [path.relative_to(ROOT).as_posix() for path in topic_pages],
        "policy": {
            "authoritative_fact_mutation": "none",
            "dose_or_withdrawal_generation": "none",
            "source_boundary": "existing HUMAN_REVIEWED PDF facts plus existing A0/A1 web source pages",
        },
    }
    out = ISSUES / "swine_llm_wiki_optimization_v6_2026-05-07.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    md = ISSUES / "swine_llm_wiki_optimization_v6_2026-05-07.md"
    lines = [
        "# Swine LLM Wiki Optimization V6 - 2026-05-07",
        "",
        "## Actions",
        "",
        f"- Fixed {len(rule_changes)} missing rule index targets by pointing `rule_index.csv` at existing reviewed rule pages.",
        f"- Added Dataset QA Reinforcement / V6 blocks to {len(disease_pages)} high-priority disease pages.",
        f"- Added synthesis retrieval page `{synthesis_page.relative_to(WIKI).as_posix()}`.",
        f"- Added {len(topic_pages)} topic retrieval pages for sampling, differential diagnosis, regulation and drug boundaries.",
        "",
        "## Reinforcement scope",
        "",
        "- Laboratory diagnosis and sampling: SRC-0008/SRC-0009 diagnostic testing and sample submission facts.",
        "- Differential diagnosis and prevention: disease-specific HUMAN_REVIEWED facts where available.",
        "- Major disease regulatory boundary: existing A0/A1 source pages such as A0-MOA-573 and WOAH disease pages.",
        "- Drug boundary: SRC-0012 drug therapy principles plus A0 banned-drug policy boundary; no dose, course or withdrawal period was generated.",
        "",
        "## Disease pages",
        "",
    ]
    lines.extend(f"- `{name}`" for name in disease_pages)
    lines.extend(["", "## Topic pages", ""])
    lines.extend(f"- `{path.relative_to(WIKI).as_posix()}`" for path in topic_pages)
    md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
    return out


def append_log(report: Path) -> None:
    log = WIKI / "log.md"
    entry = (
        f"\n- 2026-05-07 swine-optimization-v6 | fixed missing rule index targets; "
        f"added dataset QA reinforcement for sampling, lab diagnosis, differential diagnosis, "
        f"regulatory and drug-use boundaries. Report: `{report.relative_to(WIKI).as_posix()}`.\n"
    )
    log.write_text(log.read_text(encoding="utf-8").rstrip() + entry, encoding="utf-8", newline="\n")


def main() -> None:
    facts_by_id = load_facts()
    rule_changes = update_rule_index()
    disease_pages = append_disease_reinforcement(facts_by_id)
    synthesis_page = write_synthesis_page(facts_by_id)
    topic_pages = write_topic_pages(facts_by_id)
    synthesis_index_added = update_synthesis_index(synthesis_page)
    report = write_report(rule_changes, disease_pages, synthesis_page, synthesis_index_added, topic_pages)
    append_log(report)
    print(
        json.dumps(
            {
                "rule_index_fixes": len(rule_changes),
                "disease_pages_reinforced": len(disease_pages),
                "topic_pages": len(topic_pages),
                "synthesis_page": synthesis_page.as_posix(),
                "report": report.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
