import csv
import html
import json
import re
from bisect import bisect_right
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "md" / "Veterinary Treatment of Pigs.md"
SOURCE_ID = "SRC-0088"
BOOK_TITLE = "Veterinary Treatment of Pigs"

OUT_FACTS_JSON = ROOT / "issues" / "veterinary_treatment_of_pigs_facts_v13_1.json"
OUT_FACTS_CSV = ROOT / "exports" / "veterinary_treatment_of_pigs_fact_index.csv"
OUT_MED_CSV = ROOT / "exports" / "veterinary_treatment_of_pigs_medicine_index.csv"
OUT_MD = ROOT / "wiki" / "synthesis" / "veterinary_treatment_of_pigs_treatment_matrix.md"
REPORT = ROOT / "issues" / "veterinary_treatment_of_pigs_batch_progress_2026-05-08.md"
SOURCE_PAGE = ROOT / "wiki" / "sources" / "SRC-0088-veterinary-treatment-of-pigs.md"

START = "<!-- VTOP_V13_1_START -->"
END = "<!-- VTOP_V13_1_END -->"

CHAPTER_PAGES = {
    "Animal Husbandry": 1,
    "1 Animal Husbandry": 1,
    "2 Nutrition": 26,
    "3 Making a Diagnosis and Post-mortem Technique": 31,
    "4 Veterinary Equipment": 38,
    "5 Vaccines": 43,
    "6 Sedation, Analgesia, Anaesthesia and Euthanasia": 50,
    "7 Surgical Procedures": 55,
    "8 Diseases of the Gastroenteric System": 68,
    "9 Diseases of the Respiratory and Circulatory Systems": 82,
    "10 Diseases of the Urino-genital System": 92,
    "11 Diseases of the Neurological System": 104,
    "12 Diseases of the Skin": 110,
    "13 Multisystemic Diseases": 119,
    "14 Notifiable Diseases": 125,
    "15 Poisons and Causes of Sudden Death": 131,
    "16 Zoonotic Diseases": 141,
    "Appendix: Veterinary Medicines": 149,
    "Glossary": 161,
    "References": 167,
    "Index": 169,
}

DISEASE_FILE_MAP = {
    "epidemic diarrhoea": "DIS-008-porcine-epidemic-diarrhea-virus.md",
    "porcine epidemic diarrhoea": "DIS-008-porcine-epidemic-diarrhea-virus.md",
    "rotavirus infection": "DIS-030-rotaviruses-and-reoviruses.md",
    "transmissible gastroenteritis": "DIS-009-transmissible-gastroenteritis-virus.md",
    "vomiting wasting disease": "DIS-011-hemagglutinating-encephalomyelitis-virus.md",
    "clostridial diarrhoea": "DIS-039-clostridial-diseases.md",
    "clostridium": "DIS-039-clostridial-diseases.md",
    "escherichia coli diarrhoea": "DIS-040-colibacillosis.md",
    "e. coli": "DIS-040-colibacillosis.md",
    "oedema disease": "DIS-042-edema-disease-e-coli.md",
    "salmonellosis": "DIS-049-salmonellosis.md",
    "proliferative enteropathy": "DIS-048-proliferative-enteropathy-lawsonia-intracellularis.md",
    "ileitis": "DIS-048-proliferative-enteropathy-lawsonia-intracellularis.md",
    "swine dysentery": "DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md",
    "ascaris suum": "DIS-060-ascaris-suum-internal-parasites.md",
    "trichuris suis": "DIS-061-trichuris-suis-internal-parasites.md",
    "actinobacillosis": "DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md",
    "actinobacillus pleuropneumoniae": "DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md",
    "atrophic rhinitis": "DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md",
    "bordetella bronchiseptica rhinitis": "DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md",
    "enzootic pneumonia": "DIS-046-mycoplasmosis-enzootic-pneumonia.md",
    "mycoplasma hyopneumoniae": "DIS-046-mycoplasmosis-enzootic-pneumonia.md",
    "pasteurellosis": "DIS-047-pasteurellosis.md",
    "streptococcal": "DIS-051-streptococcosis-streptococcus-suis.md",
    "streptococcus suis": "DIS-051-streptococcosis-streptococcus-suis.md",
    "erysipelas": "DIS-043-erysipelas.md",
    "leptospirosis": "DIS-045-leptospirosis.md",
    "brucellosis": "DIS-038-brucella-suis-brucellosis.md",
    "toxoplasmosis": "DIS-058-toxoplasmosis-protozoa.md",
    "post-weaning multisystemic wasting syndrome": "DIS-007-circoviruses-pcvad.md",
    "porcine reproductive and respiratory syndrome": "DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md",
    "swine influenza": "DIS-021-influenza-viruses.md",
    "aujeszky": "DIS-018-pseudorabies-aujeszky-disease.md",
    "classical swine fever": "DIS-024-classical-swine-fever-pestiviruses.md",
    "foot and mouth disease": "DIS-026-foot-and-mouth-disease-picornaviruses.md",
    "mange": "DIS-055-external-parasites-mange.md",
    "scabies": "DIS-055-external-parasites-mange.md",
    "lice": "DIS-056-external-parasites-lice.md",
}

DRUG_FILE_MAP = {
    "ivermectin": "DRUG-002-ivermectin.md",
    "ivermectins": "DRUG-002-ivermectin.md",
    "doramectin": "DRUG-003-doramectin.md",
    "fenbendazole": "DRUG-004-fenbendazole.md",
    "flubendazole": "DRUG-005-benzimidazoles.md",
    "amoxicillin": "DRUG-010-amoxicillin.md",
    "ceftiofur": "DRUG-011-ceftiofur.md",
    "florfenicol": "DRUG-012-florfenicol.md",
    "tiamulin": "DRUG-013-tiamulin.md",
    "lincomycin": "DRUG-014-lincomycin.md",
    "tylosin": "DRUG-015-tylosin.md",
    "tulathromycin": "DRUG-017-tulathromycin.md",
    "sulathromycin": "DRUG-017-tulathromycin.md",
    "enrofloxacin": "DRUG-018-enrofloxacin.md",
    "oxytetracycline": "DRUG-019-oxytetracycline.md",
    "chlortetracycline": "DRUG-020-chlortetracycline.md",
    "doxycycline": "DRUG-021-doxycycline.md",
    "trimethoprim": "DRUG-022-sulfonamide-trimethoprim.md",
    "gentamicin": "DRUG-023-gentamicin.md",
    "neomycin": "DRUG-024-neomycin.md",
    "spectinomycin": "DRUG-026-spectinomycin.md",
    "spectromycin": "DRUG-026-spectinomycin.md",
    "toltrazuril": "DRUG-027-toltrazuril.md",
    "iron": "DRUG-028-iron-dextran.md",
    "flunixin": "DRUG-064-flunixin-meglumine.md",
    "ketoprofen": "DRUG-065-ketoprofen-sodium-salicylate-indomethacin.md",
    "sodium salicylate": "DRUG-065-ketoprofen-sodium-salicylate-indomethacin.md",
    "salicylate": "DRUG-065-ketoprofen-sodium-salicylate-indomethacin.md",
    "meloxicam": "DRUG-063-meloxicam.md",
    "dexamethasone": "DRUG-066-dexamethasone.md",
    "dexamethazone": "DRUG-066-dexamethasone.md",
    "oxytocin": "DRUG-067-oxytocin.md",
    "altrenogest": "DRUG-068-altrenogest.md",
    "azaperone": "DRUG-077-azaperone.md",
    "pentobarbital": "DRUG-078-pentobarbital.md",
}

TREATMENT_TERMS = re.compile(
    r"\b(treatment|treated|treat|dose|dosage|given|administered|injection|injectable|oral|orally|"
    r"vaccin|antibiotic|antimicrobial|NSAID|analgesia|anaesthesia|euthanasia|withhold|withdrawal|"
    r"licensed|cascade|not licensed|should not be used)\b",
    re.I,
)
DOSE_TERMS = re.compile(
    r"(\b\d+(?:\.\d+)?\s*(?:mg|ml|kg|iu|days?|weeks?|h|min)\b|\bmg\b|\bml\b|\bIU\b|\\mathrm|withdraw|withhold)",
    re.I,
)


def clean(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(s).lower()).strip()


def parse_pages(s: str):
    out = []
    s = s.replace("鈥?", "-").replace("–", "-").replace("—", "-")
    for part in re.split(r",\s*", s):
        m = re.search(r"(\d{1,3})(?:-(\d{1,3}))?", part)
        if m:
            out.append(int(m.group(1)))
            if m.group(2):
                out.append(int(m.group(2)))
    return sorted(set(out))


def chapter_anchors(lines):
    anchors = []
    for i, line in enumerate(lines, 1):
        h = clean(line).lstrip("# ").strip()
        if h in CHAPTER_PAGES:
            anchors.append((i, CHAPTER_PAGES[h], h))
    return sorted(anchors)


def infer_page(line_no, anchors):
    starts = [a[0] for a in anchors]
    pos = bisect_right(starts, line_no) - 1
    if pos < 0:
        return None, "unmapped"
    line_a, page_a, title_a = anchors[pos]
    if pos + 1 >= len(anchors):
        return page_a, "chapter_anchor"
    line_b, page_b, _ = anchors[pos + 1]
    if page_b <= page_a or line_b <= line_a:
        return page_a, "chapter_anchor"
    frac = (line_no - line_a) / (line_b - line_a)
    page = int(round(page_a + frac * (page_b - page_a)))
    page = max(page_a, min(page_b - 1, page))
    return page, "chapter_interpolated"


def parse_index(lines):
    index = {}
    in_index = False
    for line in lines:
        c = clean(line)
        heading = c.lstrip("# ").strip()
        if heading == "Index":
            in_index = True
            continue
        if not in_index or not c:
            continue
        m = re.match(r"(.+?)\s+((?:\d{1,3}(?:[鈥?\-–]\d{1,3})?)(?:,\s*\d{1,3}(?:[鈥?\-–]\d{1,3})?)*)$", c)
        if not m:
            continue
        term = norm(m.group(1))
        pages = parse_pages(m.group(2))
        if term and pages:
            index.setdefault(term, set()).update(pages)
    return {k: sorted(v) for k, v in index.items()}


def index_page_for(text, index):
    n = norm(text)
    if not n:
        return None
    candidates = []
    for k, pages in index.items():
        if n == k or n in k or k in n:
            candidates.append((abs(len(k) - len(n)), len(k), pages[0]))
    if not candidates:
        return None
    return sorted(candidates)[0][2]


def current_context(line, current):
    c = clean(line)
    if not c.startswith("# "):
        return current
    h = c.lstrip("# ").strip()
    if h in CHAPTER_PAGES or re.match(r"^\d+\s+", h):
        current["chapter"] = h
        current["heading"] = ""
    elif h and not h.lower().startswith(("fig.", "table ")):
        current["heading"] = h
    return current


def fact_page(line_no, heading, text, anchors, index):
    for candidate in (heading, text):
        page = index_page_for(candidate, index)
        if page:
            return page, "index"
    return infer_page(line_no, anchors)


def classify_fact(text):
    low = text.lower()
    if "withhold" in low or "withdrawal" in low:
        return "withdrawal_or_meat_withhold"
    if "vaccin" in low:
        return "vaccination"
    if "not licensed" in low or "should not be used" in low or "cascade" in low:
        return "licensing_or_cascade"
    if "euthanasia" in low or "pentobarb" in low:
        return "euthanasia"
    if "mg" in low or " ml" in low or "\\mathrm" in text:
        return "dose_or_route"
    return "treatment_candidate"


def mentioned_drugs(text):
    low = f" {norm(text)} "
    hits = []
    for term in DRUG_FILE_MAP:
        if f" {norm(term)} " in low:
            hits.append(term)
    return sorted(set(hits))


def disease_target(heading, text):
    low = f" {norm(' '.join([heading or '', text or '']))} "
    for term, path in DISEASE_FILE_MAP.items():
        if f" {norm(term)} " in low:
            return path
    return ""


def extract_text_facts(lines, anchors, index):
    facts = []
    current = {"chapter": "", "heading": ""}
    first_content_line = min((a[0] for a in anchors), default=1)
    for i, line in enumerate(lines, 1):
        current = current_context(line, current)
        if i < first_content_line:
            continue
        c = clean(line)
        if not c or c.startswith("#") or len(c) < 35:
            continue
        if i >= 4041:
            continue
        if not TREATMENT_TERMS.search(c):
            continue
        if not (DOSE_TERMS.search(c) or mentioned_drugs(c) or current["chapter"].startswith(("5 ", "6 ", "8 ", "9 ", "10 ", "11 ", "12 ", "13 ", "14 ", "15 ", "16 "))):
            continue
        page, method = fact_page(i, current["heading"], c, anchors, index)
        facts.append({
            "fact_id": f"VTOP-TX-{len(facts)+1:04d}",
            "source_id": SOURCE_ID,
            "book": BOOK_TITLE,
            "fact_type": classify_fact(c),
            "page": page,
            "page_method": method,
            "line_start": i,
            "line_end": i,
            "chapter": current["chapter"],
            "heading": current["heading"],
            "disease_page": disease_target(current["heading"], c),
            "drug_mentions": "; ".join(mentioned_drugs(c)),
            "text": c[:1800],
        })
    return facts


def parse_table_rows(table_html):
    rows = []
    for tr in re.findall(r"<tr>(.*?)</tr>", table_html, flags=re.S | re.I):
        cells = [clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S | re.I)]
        if cells:
            rows.append(cells)
    return rows


def extract_medicine_rows(lines, anchors, index):
    text = "\n".join(lines)
    meds = []
    table_name = ""
    for m in re.finditer(r"(Table A\.\d+[^.\n]*\.)\s*.*?\n\s*(<table>.*?</table>)", text, flags=re.S):
        table_name = clean(m.group(1))
        line_no = text[:m.start()].count("\n") + 1
        rows = parse_table_rows(m.group(2))
        if not rows:
            continue
        header = [norm(x) for x in rows[0]]
        if len(header) < 4 or "medicine" not in header[0] or "dose" not in " ".join(header):
            continue
        for cells in rows[1:]:
            if len(cells) < 4:
                continue
            medicine, active, dose, withhold = cells[:4]
            if not medicine or medicine.lower() == "medicine":
                continue
            page = index_page_for(medicine, index) or index_page_for(active, index)
            method = "index" if page else "appendix_interpolated"
            if not page:
                page, _ = infer_page(line_no, anchors)
            meds.append({
                "fact_id": f"VTOP-MED-{len(meds)+1:04d}",
                "source_id": SOURCE_ID,
                "book": BOOK_TITLE,
                "fact_type": "veterinary_medicine_table",
                "table": table_name,
                "medicine": medicine,
                "active_substance": active,
                "dose": dose,
                "meat_withhold_days": withhold,
                "page": page,
                "page_method": method,
                "line_start": line_no,
                "line_end": line_no,
                "drug_mentions": "; ".join(mentioned_drugs(" ".join(cells))),
            })
    return meds


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def update_index_csv(path, row_key, row):
    if not path.exists():
        return False
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        rows = list(reader)
    for k in row:
        if k not in fields:
            fields.append(k)
    rows = [r for r in rows if r.get(row_key) != row[row_key]]
    rows.append({k: row.get(k, "") for k in fields})
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return True


def compact_tx(f):
    return f"- `{f['fact_id']}` {f['fact_type']} / p.{f['page']} / {f['heading']}: {f['text'][:420]} `source_id={SOURCE_ID}; page={f['page']}; line={f['line_start']}`"


def compact_med(m):
    return f"- `{m['fact_id']}` {m['medicine']} ({m['active_substance']}): dose={m['dose']}; meat_withhold={m['meat_withhold_days']} days. `source_id={SOURCE_ID}; page={m['page']}; table={m['table']}`"


def write_matrix(text_facts, med_rows, lines, anchors, index):
    by_chapter = {}
    for f in text_facts:
        by_chapter.setdefault(f["chapter"], []).append(f)
    md = [
        "---",
        "tags: [synthesis, swine, veterinary_treatment_of_pigs, treatment_matrix, executable_source, v13_1]",
        "updated: 2026-05-08T23:59:00+08:00",
        "evidence_status: HUMAN_REVIEWED",
        f"sources: [{SOURCE_ID}]",
        "---",
        "",
        f"# {BOOK_TITLE} Treatment and Medicine Fact Matrix",
        "",
        "## Scope",
        "",
        f"- Raw file: `{RAW.relative_to(ROOT).as_posix()}`.",
        f"- Raw lines processed: {len(lines)}.",
        f"- Chapter page anchors: {len(anchors)}.",
        f"- Index page anchors: {len(index)}.",
        f"- Text treatment facts extracted: {len(text_facts)}.",
        f"- Appendix medicine rows extracted: {len(med_rows)}.",
        "- Policy: facts from this source may support treatment candidates, dose/course/route, meat withhold and UK/EU-labelled product context when the exact page and source are retained.",
        "",
        "## Appendix Medicine Rows",
        "",
    ]
    for m in med_rows:
        md.append(compact_med(m))
    md.append("")
    md.append("## Text Treatment Facts")
    md.append("")
    for chapter, rows in sorted(by_chapter.items(), key=lambda kv: kv[1][0]["page"] or 9999):
        md.append(f"### {chapter or 'Unchaptered'}")
        md.append("")
        for f in rows:
            md.append(compact_tx(f))
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def update_entity_pages(text_facts, med_rows):
    touched_diseases = []
    by_disease = {}
    for f in text_facts:
        if f["disease_page"]:
            by_disease.setdefault(f["disease_page"], []).append(f)
    for rel, rows in sorted(by_disease.items()):
        path = ROOT / "wiki" / "diseases" / rel
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        old = re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", "\n", old, flags=re.S)
        pages = sorted({str(r["page"]) for r in rows if r["page"]}, key=lambda x: int(x))
        sec = [
            "",
            START,
            f"## {BOOK_TITLE} Treatment Evidence (SRC-0088, V13.1 batch)",
            "",
            f"- Batch status: {len(rows)} treatment facts linked to this disease page.",
            f"- Source pages: {', '.join(pages)}.",
            f"- Full matrix: `wiki/synthesis/{OUT_MD.name}`; fact index: `exports/{OUT_FACTS_CSV.name}`.",
            "",
        ]
        sec.extend(compact_tx(r) for r in rows[:35])
        if len(rows) > 35:
            sec.append(f"- Additional linked rows omitted here: {len(rows)-35}; see `exports/{OUT_FACTS_CSV.name}`.")
        sec.extend(["", END, ""])
        path.write_text(old.rstrip() + "\n" + "\n".join(sec), encoding="utf-8")
        touched_diseases.append(str(path.relative_to(ROOT)))

    touched_drugs = []
    by_drug = {}
    for m in med_rows:
        for term in m["drug_mentions"].split("; "):
            target = DRUG_FILE_MAP.get(term)
            if target:
                by_drug.setdefault(target, {"med": [], "tx": []})["med"].append(m)
    for f in text_facts:
        for term in f["drug_mentions"].split("; "):
            target = DRUG_FILE_MAP.get(term)
            if target:
                by_drug.setdefault(target, {"med": [], "tx": []})["tx"].append(f)
    for rel, groups in sorted(by_drug.items()):
        path = ROOT / "wiki" / "drugs" / rel
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        old = re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", "\n", old, flags=re.S)
        med = groups["med"]
        tx = groups["tx"]
        pages = sorted({str(r["page"]) for r in med + tx if r.get("page")}, key=lambda x: int(x))
        sec = [
            "",
            START,
            f"## {BOOK_TITLE} Medicine Evidence (SRC-0088, V13.1 batch)",
            "",
            f"- Batch status: {len(med)} appendix medicine rows and {len(tx)} text treatment mentions linked to this drug page.",
            f"- Source pages: {', '.join(pages) if pages else 'UNMAPPED'}.",
            f"- Medicine index: `exports/{OUT_MED_CSV.name}`; treatment matrix: `wiki/synthesis/{OUT_MD.name}`.",
            "",
        ]
        sec.extend(compact_med(r) for r in med[:25])
        sec.extend(compact_tx(r) for r in tx[:15])
        omitted = max(0, len(med) - 25) + max(0, len(tx) - 15)
        if omitted:
            sec.append(f"- Additional linked rows omitted here: {omitted}; see exported indexes.")
        sec.extend(["", END, ""])
        path.write_text(old.rstrip() + "\n" + "\n".join(sec), encoding="utf-8")
        touched_drugs.append(str(path.relative_to(ROOT)))
    return touched_diseases, touched_drugs


def write_source_page():
    SOURCE_PAGE.write_text(
        "\n".join([
            "---",
            f"source_id: {SOURCE_ID}",
            f"title: {BOOK_TITLE}",
            "author: Graham R. Duncanson",
            "publisher: CABI",
            "publication_year: 2013",
            "evidence_status: HUMAN_REVIEWED",
            "jurisdiction_context: UK/EU licensed medicines and cascade principle as described by the source",
            "raw_file: raw/md/Veterinary Treatment of Pigs.md",
            "---",
            "",
            f"# {BOOK_TITLE}",
            "",
            "This source is used as a structured treatment, medicine, dose, route, meat-withhold and disease-management evidence source for swine wiki enhancement. Each extracted fact must retain `source_id=SRC-0088` and a page number.",
            "",
            "Use boundary: product licensing and meat-withhold statements are source-date and jurisdiction-context dependent; generated answers should preserve the UK/EU context unless independently verified for another jurisdiction.",
            "",
        ]),
        encoding="utf-8",
    )


def main():
    lines = RAW.read_text(encoding="utf-8").splitlines()
    anchors = chapter_anchors(lines)
    index = parse_index(lines)
    text_facts = extract_text_facts(lines, anchors, index)
    med_rows = extract_medicine_rows(lines, anchors, index)

    OUT_FACTS_JSON.write_text(json.dumps(text_facts + med_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(OUT_FACTS_CSV, text_facts, [
        "fact_id", "source_id", "fact_type", "page", "page_method", "line_start", "line_end",
        "chapter", "heading", "disease_page", "drug_mentions", "text",
    ])
    write_csv(OUT_MED_CSV, med_rows, [
        "fact_id", "source_id", "fact_type", "table", "medicine", "active_substance", "dose",
        "meat_withhold_days", "page", "page_method", "line_start", "line_end", "drug_mentions",
    ])
    write_matrix(text_facts, med_rows, lines, anchors, index)
    touched_diseases, touched_drugs = update_entity_pages(text_facts, med_rows)
    write_source_page()

    updates = []
    if update_index_csv(ROOT / "exports" / "source_index.csv", "source_id", {
        "source_id": SOURCE_ID,
        "title": BOOK_TITLE,
        "pages": "2013; pages 1-169; raw/md/Veterinary Treatment of Pigs.md",
        "evidence_status": "HUMAN_REVIEWED",
        "relpath": "wiki/sources/SRC-0088-veterinary-treatment-of-pigs.md",
    }):
        updates.append("exports/source_index.csv")
    if update_index_csv(ROOT / "exports" / "synthesis_index.csv", "id", {
        "id": "SYNTH-VTOP-TREATMENT-MATRIX",
        "title": f"{BOOK_TITLE} treatment and medicine matrix",
        "path": f"wiki/synthesis/{OUT_MD.name}",
        "sources": SOURCE_ID,
        "updated": "2026-05-08T23:59:00+08:00",
    }):
        updates.append("exports/synthesis_index.csv")
    if update_index_csv(ROOT / "exports" / "drug_page_index.csv", "id", {
        "id": "VTOP-MEDICINE-INDEX",
        "title": f"{BOOK_TITLE} appendix medicine product index",
        "path": f"exports/{OUT_MED_CSV.name}",
        "sources": SOURCE_ID,
        "updated": "2026-05-08T23:59:00+08:00",
    }):
        updates.append("exports/drug_page_index.csv")
    for drug_id, title, relpath in [
        ("DRUG-077-azaperone", "Azaperone", "wiki/drugs/DRUG-077-azaperone.md"),
        ("DRUG-078-pentobarbital", "Pentobarbital", "wiki/drugs/DRUG-078-pentobarbital.md"),
    ]:
        update_index_csv(ROOT / "exports" / "drug_page_index.csv", "drug_id", {
            "drug_id": drug_id,
            "title": title,
            "status": "evidence_only",
            "page_relpath": relpath,
            "sources": SOURCE_ID,
            "updated": "2026-05-08T23:59:00+08:00",
        })

    exactish = sum(1 for r in text_facts + med_rows if r.get("page_method") == "index")
    total = len(text_facts) + len(med_rows)
    report = [
        "# Veterinary Treatment of Pigs batch progress / 2026-05-08",
        "",
        f"- Raw file: `{RAW.relative_to(ROOT).as_posix()}`",
        f"- Raw lines processed: {len(lines)}",
        f"- Chapter page anchors: {len(anchors)}",
        f"- Index page anchors: {len(index)}",
        f"- Text treatment facts extracted: {len(text_facts)}",
        f"- Appendix medicine rows extracted: {len(med_rows)}",
        f"- Total structured facts: {total}",
        f"- Facts with index-derived exact page: {exactish}",
        f"- Facts with chapter/interpolated page: {total - exactish}",
        f"- Disease wiki pages updated: {len(touched_diseases)}",
        f"- Drug wiki pages updated: {len(touched_drugs)}",
        f"- Index files updated: {', '.join(updates)}",
        f"- Fact CSV: `exports/{OUT_FACTS_CSV.name}`",
        f"- Medicine CSV: `exports/{OUT_MED_CSV.name}`",
        f"- Matrix: `wiki/synthesis/{OUT_MD.name}`",
        "",
        "## Updated disease pages",
        "",
    ]
    report.extend(f"- `{p}`" for p in touched_diseases)
    report.extend(["", "## Updated drug pages", ""])
    report.extend(f"- `{p}`" for p in touched_drugs)
    report.extend([
        "",
        "## Notes",
        "",
        "- This run completed the whole file rather than only batch 1 because the file size and structure were tractable.",
        "- Page assignment prioritizes the book index; chapter interpolation is retained as `page_method=chapter_interpolated` where the index has no exact row-level entry.",
        "- Product licensing and meat-withhold statements retain the source's UK/EU/cascade context.",
    ])
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "raw_lines": len(lines),
        "chapter_page_anchors": len(anchors),
        "index_page_anchors": len(index),
        "text_treatment_facts": len(text_facts),
        "appendix_medicine_rows": len(med_rows),
        "total_facts": total,
        "index_page_facts": exactish,
        "interpolated_page_facts": total - exactish,
        "disease_pages_updated": len(touched_diseases),
        "drug_pages_updated": len(touched_drugs),
        "index_updates": updates,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
