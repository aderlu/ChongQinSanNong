from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
EXPORTS = WIKI / "exports"
ISSUES = WIKI / "issues"
PDF = ROOT / "docs" / "Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman,  Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
NOW = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AuthoritySource:
    source_id: str
    title: str
    url: str
    authority_level: str
    evidence_status: str
    summary: str
    use_for: str


AUTHORITY_SOURCES = [
    AuthoritySource(
        "A1-WOAH-ASF-DISEASE",
        "WOAH African swine fever disease page",
        "https://www.woah.org/en/disease/african-swine-fever/",
        "A1",
        "HUMAN_REVIEWED",
        "International animal-health authority page for ASF clinical, diagnostic, transmission, reporting and control boundaries.",
        "ASF regulatory and diagnostic boundary checks.",
    ),
    AuthoritySource(
        "A1-WOAH-FMD-DISEASE",
        "WOAH Foot and mouth disease disease page",
        "https://www.woah.org/en/disease/foot-and-mouth-disease/",
        "A1",
        "HUMAN_REVIEWED",
        "International authority page for FMD, including high-consequence livestock disease boundaries.",
        "Vesicular disease and FMD hard-block retrieval.",
    ),
    AuthoritySource(
        "A1-WOAH-CSF-DISEASE",
        "WOAH Classical swine fever disease page",
        "https://www.woah.org/en/disease/classical-swine-fever/",
        "A1",
        "HUMAN_REVIEWED",
        "International authority page for CSF recognition, diagnosis and control.",
        "Fever, cyanosis, hemorrhage and regulatory differential cases.",
    ),
    AuthoritySource(
        "A1-WOAH-AUJESZKY-DISEASE",
        "WOAH Aujeszky's disease disease page",
        "https://www.woah.org/en/disease/aujeszkys-disease/",
        "A1",
        "HUMAN_REVIEWED",
        "International authority page for Aujeszky's disease / pseudorabies.",
        "Neurologic and reproductive differential cases.",
    ),
    AuthoritySource(
        "A1-WOAH-PRRS-DISEASE",
        "WOAH Porcine reproductive and respiratory syndrome disease page",
        "https://www.woah.org/en/disease/porcine-reproductive-and-respiratory-syndrome/",
        "A1",
        "HUMAN_REVIEWED",
        "International authority page for PRRS respiratory and reproductive disease boundaries.",
        "Respiratory and reproductive differential retrieval.",
    ),
    AuthoritySource(
        "A1-USDA-APHIS-ASF",
        "USDA APHIS African swine fever information",
        "https://www.aphis.usda.gov/livestock-poultry-disease/swine/african-swine-fever",
        "A1",
        "HUMAN_REVIEWED",
        "US federal animal-health authority page for ASF prevention and response information.",
        "ASF response and producer-facing biosecurity boundaries.",
    ),
    AuthoritySource(
        "A1-USDA-APHIS-SWINE-BRUCELLOSIS",
        "USDA APHIS swine brucellosis information",
        "https://www.aphis.usda.gov/livestock-poultry-disease/swine/swine-brucellosis",
        "A1",
        "HUMAN_REVIEWED",
        "US federal animal-health authority page for swine brucellosis.",
        "Zoonotic reproductive disease boundary checks.",
    ),
    AuthoritySource(
        "A1-FAO-ASF",
        "FAO African swine fever resources",
        "https://www.fao.org/animal-health/situation-updates/african-swine-fever/",
        "A1",
        "HUMAN_REVIEWED",
        "FAO animal-health resources for ASF situation, prevention and control.",
        "ASF biosecurity and control context.",
    ),
]


MANUAL_ALIASES = {
    "DIS-002": ["非洲猪瘟", "ASF", "African swine fever", "African swine fever virus"],
    "DIS-003": ["猪环曲病毒", "托克特诺病毒", "TTSuV", "Torque teno sus virus", "anellovirus"],
    "DIS-004": ["猪星状病毒", "星状病毒", "PoAstV", "porcine astrovirus", "astrovirus"],
    "DIS-008": ["猪流行性腹泻", "PED", "PEDV", "porcine epidemic diarrhea"],
    "DIS-009": ["猪传染性胃肠炎", "TGE", "TGEV", "transmissible gastroenteritis"],
    "DIS-018": ["伪狂犬病", "奥耶斯基病", "Aujeszky's disease", "pseudorabies", "PRV"],
    "DIS-024": ["猪瘟", "经典猪瘟", "CSF", "classical swine fever"],
    "DIS-026": ["口蹄疫", "FMD", "foot and mouth disease"],
    "DIS-028": ["猪繁殖与呼吸综合征", "PRRS", "PRRSV", "蓝耳病"],
    "DIS-038": ["猪布鲁氏菌病", "布鲁氏菌病", "Brucella suis", "swine brucellosis"],
    "DIS-052": ["猪痢疾", "swine dysentery", "Brachyspira hyodysenteriae"],
}

PDF_TERMS = [
    ("DIS-002", "African Swine Fever Virus", 443, 476),
    ("DIS-003", "Torque teno sus virus", 453, 456),
    ("DIS-004", "Astroviruses", 457, 460),
    ("DIS-008", "Porcine Epidemic Diarrhea Virus", 488, 524),
    ("DIS-009", "Transmissible Gastroenteritis Virus", 488, 524),
    ("DIS-018", "Aujeszky", 554, 575),
    ("DIS-024", "Classical Swine Fever", 622, 641),
    ("DIS-026", "Foot-and-Mouth Disease", 641, 664),
    ("DIS-028", "Porcine Reproductive and Respiratory Syndrome", 665, 705),
    ("DIS-038", "Brucella suis", 778, 792),
    ("DIS-052", "Swine Dysentery", 951, 972),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{key: row.get(key, "") for key in fieldnames} for row in rows])


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()


def load_disease_index() -> list[dict[str, str]]:
    return read_csv(EXPORTS / "disease_index.csv")


def build_alias_index(diseases: list[dict[str, str]]) -> Path:
    rows: list[dict[str, str]] = []
    for disease in diseases:
        disease_id = disease.get("disease_id", "")
        canonical = disease.get("disease_name", "")
        page_relpath = disease.get("page_relpath", "")
        aliases = [canonical]
        if page_relpath:
            slug = Path(page_relpath).stem
            parts = slug.split("-", 2)
            if len(parts) == 3:
                aliases.append(parts[2].replace("-", " "))
        aliases.extend(MANUAL_ALIASES.get(disease_id, []))
        for alias in dict.fromkeys(item.strip() for item in aliases if item.strip()):
            rows.append(
                {
                    "canonical_id": disease_id,
                    "canonical_name": canonical,
                    "alias": alias,
                    "language": "zh" if re.search(r"[\u4e00-\u9fff]", alias) else "en",
                    "alias_type": "canonical" if alias == canonical else "synonym",
                    "page_relpath": page_relpath,
                }
            )
    out = EXPORTS / "alias_index.csv"
    write_csv(out, rows, ["canonical_id", "canonical_name", "alias", "language", "alias_type", "page_relpath"])
    return out


def write_authority_sources() -> tuple[Path, Path]:
    for source in AUTHORITY_SOURCES:
        path = WIKI / "wiki" / "sources" / f"{source.source_id}.md"
        if path.exists():
            continue
        text = f"""---
source_id: {source.source_id}
source_type: authoritative_web
authority_level: {source.authority_level}
evidence_status: {source.evidence_status}
external_url: {source.url}
updated: {NOW}
---

# {source.title}

## Source

- URL: {source.url}
- Authority level: {source.authority_level}
- Evidence status: {source.evidence_status}

## Dataset Use

{source.summary}

Use for: {source.use_for}

## Boundary

This source page is a retrieval and audit anchor. It does not authorize dose, course, withdrawal-period, culling, transport, or local regulatory instructions unless the generated answer also cites the applicable jurisdiction-specific A0/A1 source.
"""
        path.write_text(text, encoding="utf-8", newline="\n")

    rows = read_csv(EXPORTS / "source_index.csv")
    existing = {row.get("source_id") for row in rows}
    for source in AUTHORITY_SOURCES:
        if source.source_id in existing:
            continue
        rows.append(
            {
                "source_id": source.source_id,
                "title": source.title,
                "pages": source.url,
                "evidence_status": source.evidence_status,
                "relpath": f"wiki/sources/{source.source_id}.md",
            }
        )
    out = EXPORTS / "source_index.csv"
    write_csv(out, rows, ["source_id", "title", "pages", "evidence_status", "relpath"])
    return out, WIKI / "wiki" / "sources"


def write_rule_cards() -> list[Path]:
    cards = {
        "RC-CITATION-001": (
            "标准证据引用门禁",
            "high",
            "所有诊断、采样、监管、用药、休药期结论必须使用标准 `source=SRC-0000`、`source=A0-...` 或 `source=RC-...` 格式。内部 anchor key、裸页面路径、source_id 字样不能作为训练可用引用。",
        ),
        "RC-TRAIN-READY-001": (
            "训练可用样本门禁",
            "critical",
            "训练可用样本必须 pass、无 fatal risk、目标疾病别名命中诊断、回答标准引用不少于 3 个，且不得包含无来源剂量或无来源具体休药期。",
        ),
        "RC-ALIAS-001": (
            "疾病别名归一化门禁",
            "high",
            "疾病命中、证据检索和评审必须使用 exports/alias_index.csv，不得只用原始 target 字符串做硬匹配。",
        ),
    }
    paths: list[Path] = []
    for card_id, (title, severity, body) in cards.items():
        path = WIKI / "wiki" / "rule_cards" / f"{card_id}.md"
        text = f"""---
card_id: {card_id}
severity: {severity}
jurisdiction: Global
hard_block: {"true" if severity == "critical" else "false"}
evidence_status: HUMAN_REVIEWED
updated: {NOW}
---

# {title}

## Rule

{body}

## Enforcement

- Candidate generation: inject this card whenever a case asks for diagnosis, treatment, sampling, regulation, sale, withdrawal period, or public-health boundary.
- CSV conversion: compute local flags from normalized aliases and standard citations.
- Train-ready export: reject records that violate this card.
"""
        path.write_text(text, encoding="utf-8", newline="\n")
        paths.append(path)

    index_path = EXPORTS / "rule_card_index.csv"
    rows = read_csv(index_path)
    existing = {row.get("card_id") for row in rows}
    for path in paths:
        card_id = path.stem
        if card_id in existing:
            continue
        title = cards[card_id][0]
        severity = cards[card_id][1]
        rows.append(
            {
                "card_id": card_id,
                "title": title,
                "severity": severity,
                "jurisdiction": "Global",
                "hard_block": "True" if severity == "critical" else "False",
                "page_relpath": path.relative_to(WIKI).as_posix(),
            }
        )
    write_csv(index_path, rows, ["card_id", "title", "severity", "jurisdiction", "hard_block", "page_relpath"])
    return paths


def extract_pdf_hits(max_pages_per_term: int = 4) -> Path:
    reader = PdfReader(str(PDF))
    hits: list[dict[str, object]] = []
    for disease_id, term, start_page, end_page in PDF_TERMS:
        found = 0
        for page_number in range(start_page, min(end_page, len(reader.pages)) + 1):
            if found >= max_pages_per_term:
                break
            try:
                text = reader.pages[page_number - 1].extract_text() or ""
            except Exception:
                continue
            lower = text.lower()
            lower_term = term.lower()
            if lower_term not in lower:
                continue
            pos = lower.find(lower_term)
            start = max(0, pos - 120)
            end = min(len(text), pos + len(term) + 220)
            snippet = re.sub(r"\s+", " ", text[start:end]).strip()
            hits.append(
                {
                    "disease_id": disease_id,
                    "term": term,
                    "pdf_page_number": page_number,
                    "snippet_preview": snippet[:420],
                    "source_id": "SRC-0001",
                    "source_path": str(PDF),
                    "next_action": "Use this page hit for human-reviewed fact extraction; do not promote automatically to train-ready facts.",
                }
            )
            found += 1
    out = ISSUES / "swine_pdf_priority_page_hits_2026-05-07.json"
    out.write_text(json.dumps(hits, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return out


def append_dataset_quality_page() -> Path:
    path = WIKI / "wiki" / "synthesis" / "swine_dataset_generation_validity_gate_v7.md"
    text = f"""---
tags: [synthesis, swine, dataset, qa, evidence_gate, generation_gate]
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0001, RC-CITATION-001, RC-TRAIN-READY-001, RC-ALIAS-001]
---

# Swine Dataset Generation Validity Gate V7

## Purpose

This retrieval page defines the minimum evidence package for swine QA dataset generation. It should be injected into draft, answer, judge and export stages.

## Required Evidence Package

- Disease identity must be normalized through `exports/alias_index.csv`.
- The answer must cite standard anchors only: `source=SRC-0000`, `source=A0-...`, `source=A1-...`, or `source=RC-...`.
- Diagnosis requires at least one disease-specific source and one differential or diagnostic-sampling source.
- Treatment or action language requires a drug/regulatory boundary rule card.
- Withdrawal-period language must stay as a boundary statement unless a jurisdiction-specific approved label source is present.
- Regulated or zoonotic disease cases must include the applicable official source before any management language.

## Train-ready Reject Reasons

- `final_label` is not `pass`.
- `target_disease_mismatch` is true after alias normalization.
- Standard citation count is less than 3.
- The answer contains a specific dose or specific withdrawal period without an A0/A1 label source.
- The answer uses internal fact keys instead of source IDs.
- Any judge marks `fatal_risk=true`.

## PDF Backfill Boundary

The local textbook PDF is a source for chapter/page discovery and human-reviewed candidate facts. Automatic scripts may write page-hit manifests, but facts extracted from the PDF should be promoted only after review and paraphrasing.
"""
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def reinforce_priority_pages() -> list[Path]:
    blocks = {
        "DIS-003-anelloviruses-torque-teno-sus-viruses.md": [
            "## Dataset Alias and Causality Boundary / V7",
            "",
            "- Alias set for dataset matching: 猪环曲病毒, 托克特诺病毒, TTSuV, Torque teno sus virus, anellovirus. (source=RC-ALIAS-001)",
            "- TTSuV detection must not be used as a single-cause diagnosis unless the answer also explains uncertainty, co-infection assessment, and alternative differentials. (source=RC-CITATION-001)",
            "- Sampling advice should distinguish diagnostic investigation from treatment; no antiviral treatment or withdrawal-period claim is allowed without a verified label source. (source=RC-TRAIN-READY-001)",
            "",
        ],
        "DIS-004-astroviruses.md": [
            "## Dataset Alias and Enteric Differential Boundary / V7",
            "",
            "- Alias set for dataset matching: 猪星状病毒, 星状病毒, PoAstV, porcine astrovirus, astrovirus. (source=RC-ALIAS-001)",
            "- Suspected porcine astrovirus diarrhea must be generated as an enteric differential, not as a definitive single-cause diagnosis without laboratory context. (source=RC-CITATION-001)",
            "- Sampling language should prefer fresh feces or intestinal diagnostic material only when supported by retrieved disease or diagnostic sampling facts; treatment remains supportive unless a label source exists. (source=RC-TRAIN-READY-001)",
            "",
        ],
        "DIS-002-african-swine-fever-virus.md": [
            "## Authority Web Reinforcement / V7",
            "",
            "- ASF answers should retrieve both textbook evidence and official authority anchors such as WOAH, USDA APHIS, FAO, and China A0 sources where jurisdictional claims are made. (source=A1-WOAH-ASF-DISEASE; source=A1-USDA-APHIS-ASF; source=A1-FAO-ASF)",
            "- Treatment language must not replace reporting, restriction, diagnostic confirmation, or official response boundaries. (source=RC-ASF-001; source=RC-TRAIN-READY-001)",
            "",
        ],
        "DIS-038-brucella-suis-brucellosis.md": [
            "## Zoonotic Authority Reinforcement / V7",
            "",
            "- Swine brucellosis cases must include zoonotic and reproductive-disease boundaries and avoid empirical antibiotic suppression as a training answer. (source=A1-USDA-APHIS-SWINE-BRUCELLOSIS; source=RC-TRAIN-READY-001)",
            "- Human exposure, official testing, herd movement, culling or regulatory action should not be invented without a jurisdiction-specific official source. (source=RC-CITATION-001)",
            "",
        ],
    }
    touched: list[Path] = []
    for filename, lines in blocks.items():
        path = WIKI / "wiki" / "diseases" / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig")
        marker = lines[0]
        if marker in text:
            continue
        path.write_text(text.rstrip() + "\n\n" + "\n".join(lines), encoding="utf-8", newline="\n")
        touched.append(path)
    return touched


def write_report(outputs: dict[str, object]) -> Path:
    out = ISSUES / "swine_wiki_quality_upgrade_2026-05-07.json"
    out.write_text(json.dumps(outputs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    md = ISSUES / "swine_wiki_quality_upgrade_2026-05-07.md"
    lines = [
        "# Swine Wiki Quality Upgrade - 2026-05-07",
        "",
        "## Outputs",
        "",
    ]
    for key, value in outputs.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "- PDF extraction is limited to page-hit manifests for human review; no automatic dose, withdrawal-period, or regulatory action facts are promoted.",
            "- Web authority pages are registered as retrieval anchors and must be paired with jurisdiction-specific sources for local regulatory instructions.",
            "- Dataset generation should use alias normalization and train-ready gates before exporting SFT data.",
            "",
        ]
    )
    md.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return out


def path_list(paths: Iterable[Path]) -> list[str]:
    return [path.relative_to(ROOT).as_posix() for path in paths]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upgrade swine wiki quality gates, aliases, authority sources, and PDF hit manifest.")
    parser.add_argument("--skip-pdf", action="store_true", help="Skip PDF page-hit extraction.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ISSUES.mkdir(parents=True, exist_ok=True)
    diseases = load_disease_index()
    alias_index = build_alias_index(diseases)
    source_index, source_dir = write_authority_sources()
    rule_cards = write_rule_cards()
    gate_page = append_dataset_quality_page()
    reinforced = reinforce_priority_pages()
    pdf_hits = None if args.skip_pdf else extract_pdf_hits()

    outputs = {
        "alias_index": alias_index.relative_to(ROOT).as_posix(),
        "source_index": source_index.relative_to(ROOT).as_posix(),
        "authority_source_dir": source_dir.relative_to(ROOT).as_posix(),
        "rule_cards": path_list(rule_cards),
        "generation_gate_page": gate_page.relative_to(ROOT).as_posix(),
        "reinforced_disease_pages": path_list(reinforced),
        "pdf_hit_manifest": "" if pdf_hits is None else pdf_hits.relative_to(ROOT).as_posix(),
    }
    report = write_report(outputs)
    print(json.dumps({"report": report.relative_to(ROOT).as_posix(), **outputs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
