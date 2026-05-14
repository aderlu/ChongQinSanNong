from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
PDF = ROOT / "docs" / "Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman,  Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
ISSUES = WIKI / "issues"
SYNTHESIS = WIKI / "wiki" / "synthesis"
NOW = "2026-05-07T23:58:00+08:00"


DRUG_TERMS = {
    "penicillin_g": ["penicillin g", "procaine penicillin", "potassium penicillin", "penicillin"],
    "amoxicillin": ["amoxicillin"],
    "ampicillin": ["ampicillin"],
    "amoxicillin_clavulanic_acid": ["amoxicillin/clavulanic", "clavulanic"],
    "ceftiofur": ["ceftiofur"],
    "cefquinome": ["cefquinome"],
    "florfenicol": ["florfenicol"],
    "tiamulin": ["tiamulin"],
    "valnemulin": ["valnemulin"],
    "lincomycin": ["lincomycin"],
    "tylosin": ["tylosin"],
    "tylvalosin": ["tylvalosin"],
    "tulathromycin": ["tulathromycin"],
    "tilmicosin": ["tilmicosin"],
    "enrofloxacin": ["enrofloxacin"],
    "danofloxacin_marbofloxacin": ["danofloxacin", "marbofloxacin"],
    "oxytetracycline": ["oxytetracycline"],
    "chlortetracycline": ["chlortetracycline"],
    "doxycycline": ["doxycycline"],
    "tetracyclines": ["tetracycline", "tetracyclines"],
    "sulfonamides": ["sulfonamide", "sulfonamides", "sulfamethazine", "sulfadimidine", "sulfadiazine", "sulfathiazole", "sulfadimethoxine", "sulfamethoxazole", "sulfaquinoxaline"],
    "trimethoprim_sulfa": ["trimethoprim", "trimethoprim-sulfonamide", "trimethoprim sulfonamide"],
    "gentamicin": ["gentamicin"],
    "apramycin": ["apramycin"],
    "neomycin": ["neomycin"],
    "spectinomycin": ["spectinomycin"],
    "colistin": ["colistin"],
    "bacitracin_methylene_disalicylate": ["bacitracin methylene disalicylate", "bacitracin"],
    "virginiamycin": ["virginiamycin"],
    "carbadox": ["carbadox"],
    "olaquindox": ["olaquindox"],
    "dimetridazole_ronidazole": ["dimetridazole", "ronidazole"],
    "chloramphenicol": ["chloramphenicol"],
    "ivermectin": ["ivermectin"],
    "doramectin": ["doramectin"],
    "moxidectin": ["moxidectin"],
    "fenbendazole": ["fenbendazole"],
    "levamisole": ["levamisole"],
    "piperazine_pyrantel": ["piperazine", "pyrantel"],
    "amitraz": ["amitraz"],
    "phosmet_coumaphos": ["phosmet", "coumaphos"],
    "permethrin_deltamethrin": ["permethrin", "deltamethrin"],
    "toltrazuril": ["toltrazuril"],
    "ponazuril": ["ponazuril"],
    "amprolium": ["amprolium"],
    "meloxicam": ["meloxicam"],
    "flunixin": ["flunixin"],
    "ketoprofen_salicylate_indomethacin": ["ketoprofen", "sodium salicylate", "indomethacin"],
    "dexamethasone": ["dexamethasone"],
    "oxytocin": ["oxytocin"],
    "altrenogest": ["altrenogest"],
    "triptorelin": ["triptorelin"],
    "ractopamine": ["ractopamine"],
}


HIGH_RISK = {
    "chloramphenicol",
    "carbadox",
    "olaquindox",
    "dimetridazole_ronidazole",
    "ractopamine",
    "colistin",
    "cefquinome",
    "ceftiofur",
    "enrofloxacin",
    "danofloxacin_marbofloxacin",
}


def read_chapters() -> list[dict[str, object]]:
    rows = []
    with (WIKI / "exports" / "source_index.csv").open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if not row["source_id"].startswith("SRC-"):
                continue
            title = row["title"]
            pages = row["pages"]
            match = re.search(r"PDF page\s+(\d+)(?:-(\d+))?", pages)
            if not match:
                continue
            start = int(match.group(1))
            end = int(match.group(2) or match.group(1))
            rows.append({"source_id": row["source_id"], "title": title, "start": start, "end": end})
    return sorted(rows, key=lambda row: (row["start"], row["end"]))


def chapter_for(page: int, chapters: list[dict[str, object]]) -> dict[str, object] | None:
    for chapter in chapters:
        if int(chapter["start"]) <= page <= int(chapter["end"]):
            return chapter
    return None


def clean_context(text: str, term: str) -> str:
    low = text.lower()
    pos = low.find(term.lower())
    if pos == -1:
        return ""
    start = max(0, pos - 160)
    end = min(len(text), pos + len(term) + 160)
    snippet = re.sub(r"\s+", " ", text[start:end]).strip()
    return snippet


def relation_hint(snippets: list[str]) -> str:
    hay = " ".join(snippets).lower()
    if any(word in hay for word in ["prohibited", "banned", "illegal", "withdrawn", "not approved", "historical"]):
        return "boundary_or_historical"
    if any(word in hay for word in ["treatment", "treated", "therapy", "effective", "used", "administer", "control", "prevention", "prophylaxis"]):
        return "treatment_or_control_candidate"
    if any(word in hay for word in ["susceptible", "susceptibility", "mic", "resistance"]):
        return "susceptibility_candidate"
    return "mention_candidate"


def main() -> None:
    chapters = read_chapters()
    doc = fitz.open(PDF)
    rows_by_key: dict[tuple[str, str], dict[str, object]] = {}
    for page_index in range(doc.page_count):
        page_no = page_index + 1
        text = doc.load_page(page_index).get_text("text")
        low = text.lower()
        chapter = chapter_for(page_no, chapters)
        if not chapter:
            continue
        for drug_id, terms in DRUG_TERMS.items():
            hit_terms = [term for term in terms if term.lower() in low]
            if not hit_terms:
                continue
            key = (str(chapter["source_id"]), drug_id)
            row = rows_by_key.setdefault(
                key,
                {
                    "source_id": chapter["source_id"],
                    "chapter": chapter["title"],
                    "drug_candidate": drug_id,
                    "hit_terms": set(),
                    "pdf_pages": set(),
                    "contexts": [],
                    "risk_flag": "high_review" if drug_id in HIGH_RISK else "standard_review",
                },
            )
            row["hit_terms"].update(hit_terms)
            row["pdf_pages"].add(page_no)
            if len(row["contexts"]) < 3:
                row["contexts"].append(clean_context(text, hit_terms[0]))

    final_rows = []
    for row in rows_by_key.values():
        contexts = [ctx for ctx in row["contexts"] if ctx]
        final_rows.append({
            "source_id": row["source_id"],
            "chapter": row["chapter"],
            "drug_candidate": row["drug_candidate"],
            "hit_terms": "; ".join(sorted(row["hit_terms"])),
            "pdf_pages": "; ".join(str(p) for p in sorted(row["pdf_pages"])),
            "relation_hint": relation_hint(contexts),
            "risk_flag": row["risk_flag"],
            "context_sample": " | ".join(contexts[:2]),
            "evidence_status": "NEEDS_REVIEW",
        })
    final_rows.sort(key=lambda row: (row["source_id"], row["drug_candidate"]))

    json_path = ISSUES / "swine_pdf_treatment_candidate_matrix_2026-05-07.json"
    csv_path = ISSUES / "swine_pdf_treatment_candidate_matrix_2026-05-07.csv"
    md_path = ISSUES / "swine_pdf_treatment_candidate_matrix_2026-05-07.md"
    json_path.write_text(json.dumps(final_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(final_rows[0].keys()))
        writer.writeheader()
        writer.writerows(final_rows)

    by_chapter = defaultdict(list)
    for row in final_rows:
        if row["relation_hint"] in {"treatment_or_control_candidate", "susceptibility_candidate", "boundary_or_historical"}:
            by_chapter[row["chapter"]].append(row)
    lines = [
        "# Swine PDF Treatment Candidate Matrix - 2026-05-07",
        "",
        f"- Source PDF: `{PDF.relative_to(ROOT).as_posix()}`",
        f"- Parser: PyMuPDF full text scan.",
        f"- Candidate rows: {len(final_rows)}.",
        "- Status: candidate only; no dose, route, course, withdrawal period or legal-use conclusion is promoted to facts.",
        "",
    ]
    for chapter, chapter_rows in sorted(by_chapter.items()):
        lines.append(f"## {chapter}")
        lines.append("")
        for row in chapter_rows[:18]:
            lines.append(
                f"- `{row['drug_candidate']}` pages {row['pdf_pages']} -> `{row['relation_hint']}`; risk `{row['risk_flag']}`; terms: {row['hit_terms']}"
            )
        lines.append("")
    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")

    synthesis = f"""---
tags: [synthesis, swine, v7, treatment_candidates, needs_review]
updated: {NOW}
evidence_status: NEEDS_REVIEW
sources: [SRC-0012, SRC-0058, SRC-0059, SRC-0062, SRC-0063, SRC-0064, SRC-0065, SRC-0069, SRC-0070, SRC-0071, SRC-0072, SRC-0073, SRC-0074, SRC-0075, SRC-0076, SRC-0077, SRC-0080, SRC-0081, SRC-0082]
---

# Swine Treatment Candidate Matrix / 猪病治疗候选矩阵

## 来源和状态

- 本页由 PyMuPDF 对 `Diseases of Swine, 11th Edition` 全文扫描生成。
- 详细候选表：`issues/swine_pdf_treatment_candidate_matrix_2026-05-07.csv`。
- 本页是 `NEEDS_REVIEW` 派生页，不是处方页，也不是中国合规结论。

## 可用边界

- 可用于疾病-药物候选召回、药物类别归并、药敏/诊断/标签复核提示。
- 不可直接生成剂量、疗程、给药途径、群体投药、休药期或残留承诺。
- 命中 `high_review` 时，必须优先查禁用/停用/淘汰清单、AMR 审慎来源和产品标签。

## 候选概览

- 候选关系行数：{len(final_rows)}。
- 高复核药物包括：ceftiofur、cefquinome、fluoroquinolones、colistin、chloramphenicol、carbadox、olaquindox、nitroimidazoles、ractopamine。
"""
    (SYNTHESIS / "swine_treatment_candidate_matrix_v7.md").write_text(synthesis.rstrip() + "\n", encoding="utf-8", newline="\n")

    log_path = WIKI / "log.md"
    log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Wiki Log\n"
    marker = "2026-05-07 pdf-treatment-candidate-matrix"
    if marker not in log_text:
        log_path.write_text(
            log_text.rstrip()
            + "\n\n"
            + f"{marker} | generated {len(final_rows)} PDF disease-drug treatment candidate rows with PyMuPDF; added derived synthesis page; facts unchanged.\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"candidate_rows={len(final_rows)}")


if __name__ == "__main__":
    main()
