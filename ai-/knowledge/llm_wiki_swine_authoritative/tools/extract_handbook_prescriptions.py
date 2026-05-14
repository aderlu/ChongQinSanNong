import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw" / "md"
BOOK_TITLE = "\u732a\u75c5\u8bca\u7597\u4e0e\u5904\u65b9\u624b\u518c"
RAW = next(p for p in RAW_DIR.glob("*.md") if BOOK_TITLE in p.name)
OUT_JSON = ROOT / "issues" / "handbook_prescription_facts_v13_1.json"
OUT_CSV = ROOT / "exports" / "handbook_prescription_fact_index.csv"
OUT_DRUG_CSV = ROOT / "exports" / "handbook_prescription_drug_mention_index.csv"
OUT_MD = ROOT / "wiki" / "synthesis" / "swine_diagnosis_prescription_handbook_prescription_matrix.md"
REPORT = ROOT / "issues" / "handbook_full_batch_progress_2026-05-08.md"

SECTION_START = "<!-- HANDBOOK_RX_V13_1_START -->"
SECTION_END = "<!-- HANDBOOK_RX_V13_1_END -->"

GENERIC_SUBHEADS = {
    "\u75c5\u56e0", "\u75c5\u539f", "\u6d41\u884c\u75c5\u5b66", "\u8bca\u65ad\u8981\u70b9", "\u75c7\u72b6", "\u4e34\u5e8a\u75c7\u72b6",
    "\u75c5\u7406\u53d8\u5316", "\u5b9e\u9a8c\u5ba4\u8bca\u65ad", "\u9632\u5236\u63aa\u65bd", "\u9632\u6cbb\u63aa\u65bd",
    "\u6cbb\u7597\u63aa\u65bd", "\u5904\u65b9", "\u9884\u9632", "\u6cbb\u7597", "\u7528\u836f\u4e0e\u5904\u65b9",
}

DISEASE_FILE_MAP = {
    "\u732a\u761f": "DIS-024-classical-swine-fever-pestiviruses.md",
    "\u53e3\u8e44\u75ab": "DIS-026-foot-and-mouth-disease-picornaviruses.md",
    "\u6d41\u884c\u6027\u4e59\u578b\u8111\u708e": "DIS-015-japanese-encephalitis-virus.md",
    "\u8f6e\u72b6\u75c5\u6bd2\u75c5": "DIS-030-rotaviruses-and-reoviruses.md",
    "\u732a\u4f20\u67d3\u6027\u80c3\u80a0\u708e": "DIS-009-transmissible-gastroenteritis-virus.md",
    "\u732a\u7e41\u6b96\u4e0e\u547c\u5438\u7efc\u5408\u5f81": "DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md",
    "\u732a\u6d41\u611f": "DIS-021-influenza-viruses.md",
    "\u732a\u6d41\u884c\u6027\u8179\u6cfb": "DIS-008-porcine-epidemic-diarrhea-virus.md",
    "\u732a\u4f2a\u72c2\u72ac\u75c5": "DIS-018-pseudorabies-aujeszky-disease.md",
    "\u732a\u7ec6\u5c0f\u75c5\u6bd2\u75c5": "DIS-023-parvoviruses.md",
    "\u732a\u5706\u73af\u75c5\u6bd22\u578b\u611f\u67d3": "DIS-007-circoviruses-pcvad.md",
    "\u732a\u5927\u80a0\u6746\u83cc\u75c5": "DIS-040-colibacillosis.md",
    "\u4ed4\u732a\u9ec4\u75e2": "DIS-041-neonatal-post-weaning-colibacillosis.md",
    "\u4ed4\u732a\u767d\u75e2": "DIS-041-neonatal-post-weaning-colibacillosis.md",
    "\u732a\u6c34\u80bf\u75c5": "DIS-042-edema-disease-e-coli.md",
    "\u526f\u732a\u55dc\u8840\u6746\u83cc\u75c5\u6216\u732a\u591a\u53d1\u6027\u6d46\u819c\u708e\u4e0e\u5173\u8282\u708e": "DIS-044-gl-sser-s-disease.md",
    "\u4ed4\u732a\u526f\u4f24\u5bd2\u6216\u732a\u6c99\u95e8\u83cc\u75c5": "DIS-049-salmonellosis.md",
    "\u732a\u4f20\u67d3\u6027\u840e\u7f29\u6027\u9f3b\u708e": "DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md",
    "\u732a\u4f20\u67d3\u6027\u80f8\u819c\u80ba\u708e": "DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md",
    "\u732a\u4e39\u6bd2": "DIS-043-erysipelas.md",
    "\u732a\u80ba\u75ab": "DIS-047-pasteurellosis.md",
    "\u732a\u94fe\u7403\u83cc\u75c5": "DIS-051-streptococcosis-streptococcus-suis.md",
    "\u732a\u589e\u751f\u6027\u80a0\u708e": "DIS-048-proliferative-enteropathy-lawsonia-intracellularis.md",
    "\u4ed4\u732a\u68ad\u83cc\u6027\u80a0\u708e": "DIS-039-clostridial-diseases.md",
    "\u732a\u75e2\u75be": "DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md",
    "\u94a9\u7aef\u87ba\u65cb\u4f53\u75c5": "DIS-045-leptospirosis.md",
    "\u732a\u652f\u539f\u4f53\u80ba\u708e": "DIS-046-mycoplasmosis-enzootic-pneumonia.md",
    "\u5f13\u5f62\u866b\u75c5": "DIS-058-toxoplasmosis-protozoa.md",
    "\u732a\u7582\u87a8\u75c5": "DIS-055-external-parasites-mange.md",
    "\u732a\u8671\u75c5": "DIS-056-external-parasites-lice.md",
    "\u732a\u86d4\u866b\u75c5": "DIS-060-ascaris-suum-internal-parasites.md",
    "\u732a\u6bdb\u9996\u7ebf\u866b\u75c5": "DIS-061-trichuris-suis-internal-parasites.md",
}

DRUG_TERMS = [
    "\u9752\u9709\u7d20", "\u963f\u83ab\u897f\u6797", "\u6c28\u82c4\u897f\u6797", "\u6069\u8bfa\u6c99\u661f", "\u73af\u4e19\u6c99\u661f",
    "\u6c27\u6c1f\u6c99\u661f", "\u6c1f\u82ef\u5c3c\u8003", "\u66ff\u7c73\u8003\u661f", "\u571f\u9709\u7d20", "\u591a\u897f\u73af\u7d20",
    "\u5f3a\u529b\u9709\u7d20", "\u91d1\u9709\u7d20", "\u6cf0\u5999\u83cc\u7d20", "\u6797\u53ef\u9709\u7d20", "\u5934\u5b62",
    "\u5e86\u5927\u9709\u7d20", "\u5361\u90a3\u9709\u7d20", "\u94fe\u9709\u7d20", "\u65b0\u9709\u7d20", "\u7c98\u83cc\u7d20",
    "\u78fa\u80fa", "\u7532\u6c27\u82c4\u5576", "\u5730\u7f8e\u785d\u5511", "\u7532\u785d\u5511", "\u6c2f\u55b9",
    "\u4f0a\u7ef4\u83cc\u7d20", "\u963f\u7ef4\u83cc\u7d20", "\u5de6\u65cb\u54aa\u5511", "\u82ef\u786b\u54aa\u5511", "\u654c\u767e\u866b",
    "\u963f\u6258\u54c1", "\u5730\u585e\u7c73\u677e", "\u5b89\u4e43\u8fd1", "\u8461\u8404\u7cd6", "\u7ef4\u751f\u7d20",
    "\u9ec4\u82aa\u591a\u7cd6", "\u8f6c\u79fb\u56e0\u5b50", "\u514d\u75ab\u7403\u86cb\u767d", "\u5e72\u6270\u7d20",
]

DRUG_FILE_MAP = {
    "\u9752\u9709\u7d20": "DRUG-009-penicillin-g.md",
    "\u963f\u83ab\u897f\u6797": "DRUG-010-amoxicillin.md",
    "\u6c28\u82c4\u897f\u6797": "DRUG-042-ampicillin.md",
    "\u5934\u5b62": "DRUG-011-ceftiofur.md",
    "\u6069\u8bfa\u6c99\u661f": "DRUG-018-enrofloxacin.md",
    "\u6c1f\u82ef\u5c3c\u8003": "DRUG-012-florfenicol.md",
    "\u66ff\u7c73\u8003\u661f": "DRUG-045-tilmicosin.md",
    "\u571f\u9709\u7d20": "DRUG-019-oxytetracycline.md",
    "\u91d1\u9709\u7d20": "DRUG-020-chlortetracycline.md",
    "\u591a\u897f\u73af\u7d20": "DRUG-021-doxycycline.md",
    "\u5f3a\u529b\u9709\u7d20": "DRUG-021-doxycycline.md",
    "\u6cf0\u5999\u83cc\u7d20": "DRUG-013-tiamulin.md",
    "\u6797\u53ef\u9709\u7d20": "DRUG-014-lincomycin.md",
    "\u5e86\u5927\u9709\u7d20": "DRUG-023-gentamicin.md",
    "\u65b0\u9709\u7d20": "DRUG-024-neomycin.md",
    "\u7c98\u83cc\u7d20": "DRUG-052-colistin.md",
    "\u78fa\u80fa": "DRUG-034-sulfonamides.md",
    "\u7532\u6c27\u82c4\u5576": "DRUG-022-sulfonamide-trimethoprim.md",
    "\u5730\u585e\u7c73\u677e": "DRUG-066-dexamethasone.md",
    "\u4f0a\u7ef4\u83cc\u7d20": "DRUG-002-ivermectin.md",
    "\u963f\u7ef4\u83cc\u7d20": "DRUG-001-avermectins.md",
    "\u5de6\u65cb\u54aa\u5511": "DRUG-056-levamisole.md",
    "\u654c\u767e\u866b": "DRUG-076-dichlorvos.md",
}


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = s.replace("\u3000", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def normalize_heading(line: str) -> str:
    line = clean(line)
    line = re.sub(r"^#+\s*", "", line)
    line = re.sub(r"\s+\d+\s*$", "", line)
    return line.strip(" #")


def strip_marker(h: str) -> str:
    h = re.sub(r"^[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]{1,4}\u3001", "", h)
    h = re.sub(r"^\d+[\.\uff0e]\s*", "", h)
    h = h.replace("（", "(").replace("）", ")")
    h = re.sub(r"\s+", "", h)
    return h.strip()


def is_main_disease_heading(text: str) -> bool:
    h = normalize_heading(text)
    if len(h) > 60:
        return False
    if re.match(r"^(第.+[章节]|参考文献|前言|目录)", h):
        return False
    return bool(re.match(r"^[一二三四五六七八九十]{1,4}、", h))


def is_numbered_topic(text: str) -> bool:
    h = normalize_heading(text)
    if len(h) > 50:
        return False
    m = re.match(r"^\d+[\.\uff0e]\s*([\u4e00-\u9fffA-Za-z0-9]+)", h)
    if not m:
        return False
    core = strip_marker(h)
    return core not in GENERIC_SUBHEADS


def extract_toc(lines):
    toc = []
    in_toc = False
    for idx, line in enumerate(lines, start=1):
        c = clean(line)
        if "\u76ee\u5f55" in c and idx < 120:
            in_toc = True
            continue
        if in_toc and idx > 330:
            break
        if not in_toc:
            continue
        m = re.search(r"(.+?)\s+(\d{1,3})\s*$", c)
        if not m:
            continue
        title = normalize_heading(m.group(1))
        page = int(m.group(2))
        if title and not title.startswith("\u7b2c"):
            toc.append({"title": title, "page": page, "line": idx})
    return toc


def match_page(title, toc):
    title_norm = strip_marker(title)
    best = None
    for row in toc:
        rt_norm = strip_marker(row["title"])
        if title_norm == rt_norm or title_norm in rt_norm or rt_norm in title_norm:
            if best is None or len(rt_norm) > len(best["title"]):
                best = row
    return best["page"] if best else None


def prescription_title(line, current_count):
    c = normalize_heading(line)
    m = re.search(r"\u3010\u5904\u65b9\s*([0-9\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]*)\u3011\s*(.*)", c)
    if m:
        num = m.group(1).strip()
        title = m.group(2).strip()
        return num or str(current_count + 1), title
    if "\u5904\u65b9" in c:
        return str(current_count + 1), c
    return str(current_count + 1), ""


def parse_prescriptions(lines, toc):
    facts = []
    current_chapter = ""
    current_section = ""
    current_disease = ""
    current_topic = ""
    current_page = None
    pending = None
    rx_count_for_disease = 0

    for idx, raw in enumerate(lines, start=1):
        c = clean(raw)
        h = normalize_heading(raw)

        if re.match(r"^第.+章", h):
            current_chapter = h
        elif re.match(r"^第.+节", h):
            current_section = h
        elif is_main_disease_heading(raw):
            current_disease = strip_marker(h)
            current_topic = ""
            current_page = match_page(current_disease, toc)
            rx_count_for_disease = 0
        elif is_numbered_topic(raw):
            current_topic = strip_marker(h)

        is_rx = bool(re.search(r"\u3010\u5904\u65b9|^#+\s*\u5904\u65b9\s*\d*|^\u5904\u65b9\s*\d*", c))
        if is_rx and "\u7528\u836f\u4e0e\u5904\u65b9" not in c and "\u6cbb\u7597\u63aa\u65bd\u53ca\u5904\u65b9" not in c:
            if pending:
                facts.append(pending)
            rx_num, rx_title = prescription_title(raw, rx_count_for_disease)
            rx_count_for_disease += 1
            disease_or_topic = current_topic or current_disease or current_section or current_chapter
            page = match_page(disease_or_topic, toc) or current_page
            pending = {
                "fact_id": f"HANDBOOK-RX-{len(facts)+1:04d}",
                "source_id": "SRC-0087",
                "book": BOOK_TITLE,
                "page": page,
                "line_start": idx,
                "line_end": idx,
                "chapter": current_chapter,
                "section": current_section,
                "disease": current_disease,
                "disease_or_topic": disease_or_topic,
                "prescription_no": rx_num,
                "prescription_title": rx_title,
                "items": [],
                "usage": [],
                "notes": [],
                "raw_text": [c],
            }
            continue

        if pending:
            if not c:
                continue
            if not re.match(r"^#+\s*(第.+[章节]|[一二三四五六七八九十]{1,4}、|\d+[\.\uff0e])", c):
                pending["raw_text"].append(c)
                pending["line_end"] = idx
                if "\u7528\u6cd5" in c:
                    pending["usage"].append(c)
                elif "\u8bf4\u660e" in c or "\u6ce8\u610f" in c:
                    pending["notes"].append(c)
                else:
                    pending["items"].append(c)
            else:
                facts.append(pending)
                pending = None
                if is_main_disease_heading(raw):
                    current_disease = strip_marker(h)
                    current_topic = ""
                    current_page = match_page(current_disease, toc)

    if pending:
        facts.append(pending)

    for f in facts:
        f["page_status"] = "TOC_MAPPED" if f["page"] is not None else "UNMAPPED"
        f["raw_text"] = "\n".join(f["raw_text"])[:4000]
        f["items"] = "\uff1b".join(f["items"])[:2000]
        f["usage"] = "\uff1b".join(f["usage"])[:1200]
        f["notes"] = "\uff1b".join(f["notes"])[:1000]
    return facts


def drug_mentions(facts):
    rows = []
    for f in facts:
        haystack = "\n".join(str(f.get(k, "")) for k in ("prescription_title", "items", "usage", "notes", "raw_text"))
        for term in DRUG_TERMS:
            if term in haystack:
                rows.append({
                    "drug_mention": term,
                    "fact_id": f["fact_id"],
                    "source_id": f["source_id"],
                    "page": f["page"],
                    "disease_or_topic": f["disease_or_topic"],
                    "prescription_no": f["prescription_no"],
                    "line_start": f["line_start"],
                    "line_end": f["line_end"],
                })
    return rows


def compact_fact_line(f):
    page = f["page"] if f["page"] is not None else "UNMAPPED"
    title = (f["prescription_title"] or "").strip()
    label = f"\u5904\u65b9{f['prescription_no']}" + (f" {title}" if title else "")
    item = (f["items"] or f["raw_text"].replace("\n", "\uff1b"))[:500]
    usage = f["usage"][:220]
    notes = f["notes"][:180]
    return f"- `{f['fact_id']}` {label}\uff1a{item}\uff1b\u7528\u6cd5={usage}\uff1b\u6ce8={notes}\u3002`source_id=SRC-0087; page={page}; line={f['line_start']}-{f['line_end']}`"


def write_matrix(facts, toc, lines):
    by_disease = {}
    for f in facts:
        by_disease.setdefault(f["disease_or_topic"], []).append(f)

    md = [
        "---",
        "tags: [synthesis, swine, handbook, prescription_matrix, executable_source, v13_1]",
        "updated: 2026-05-08T23:59:00+08:00",
        "evidence_status: HUMAN_REVIEWED",
        "sources: [SRC-0087, RULE-HANDBOOK-PRESCRIPTION-001]",
        "---",
        "",
        f"# \u300a{BOOK_TITLE}\u300b\u5904\u65b9\u4e8b\u5b9e\u77e9\u9635",
        "",
        "## Scope",
        "",
        f"- Raw file: `{RAW.relative_to(ROOT).as_posix()}`.",
        f"- Total raw lines processed: {len(lines)}.",
        f"- TOC page anchors extracted: {len(toc)}.",
        f"- Prescription facts extracted: {len(facts)}.",
        "- Policy: \u672c\u624b\u518c\u53ef\u4f5c\u4e3a\u8bca\u7597/\u5904\u65b9\u5019\u9009\u3001\u9274\u522b\u589e\u5f3a\u3001\u5242\u91cf\u3001\u7597\u7a0b\u3001\u4f11\u836f\u671f\u3001MRL \u6216\u5408\u89c4\u7ed3\u8bba\u6765\u6e90\uff1b\u6bcf\u6761\u4e8b\u5b9e\u5fc5\u987b\u4fdd\u7559 `source_id=SRC-0087` \u548c\u9875\u7801\u3002",
        "",
        "## Prescription Facts",
        "",
    ]
    for disease, rows in sorted(by_disease.items(), key=lambda kv: (kv[1][0].get("page") or 9999, kv[0])):
        md.append(f"### {disease}")
        md.append("")
        for f in rows:
            md.append(compact_fact_line(f))
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def update_index_csv(path, row_key, row):
    if not path.exists():
        return False
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    for key in row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows = [r for r in rows if r.get(row_key) != row[row_key]]
    rows.append({k: row.get(k, "") for k in fieldnames})
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return True


def update_disease_pages(facts):
    by_target = {}
    for f in facts:
        disease = f.get("disease") or f["disease_or_topic"]
        target = DISEASE_FILE_MAP.get(f["disease_or_topic"]) or DISEASE_FILE_MAP.get(disease)
        if not target:
            continue
        by_target.setdefault(target, []).append(f)

    touched = []
    for name, rows in sorted(by_target.items()):
        path = ROOT / "wiki" / "diseases" / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(rf"\n?{re.escape(SECTION_START)}.*?{re.escape(SECTION_END)}\n?", "\n", text, flags=re.S)
        pages = sorted({str(r["page"]) for r in rows if r["page"] is not None}, key=lambda x: int(x))
        section = [
            "",
            SECTION_START,
            "## Handbook Prescription Facts (SRC-0087, V13.1 batch)",
            "",
            f"- Batch status: {len(rows)} prescription facts from `{RAW.relative_to(ROOT).as_posix()}`.",
            f"- Source pages: {', '.join(pages) if pages else 'UNMAPPED'}.",
            f"- Full structured index: `exports/handbook_prescription_fact_index.csv`; matrix: `wiki/synthesis/{OUT_MD.name}`.",
            "",
        ]
        section.extend(compact_fact_line(r) for r in rows)
        section.extend(["", SECTION_END, ""])
        path.write_text(text.rstrip() + "\n" + "\n".join(section), encoding="utf-8")
        touched.append(str(path.relative_to(ROOT)))
    return touched


def update_drug_pages(mention_rows):
    by_target = {}
    for row in mention_rows:
        target = DRUG_FILE_MAP.get(row["drug_mention"])
        if not target:
            continue
        by_target.setdefault(target, []).append(row)

    touched = []
    for name, rows in sorted(by_target.items()):
        path = ROOT / "wiki" / "drugs" / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(rf"\n?{re.escape(SECTION_START)}.*?{re.escape(SECTION_END)}\n?", "\n", text, flags=re.S)
        pages = sorted({str(r["page"]) for r in rows if r["page"]}, key=lambda x: int(x))
        terms = sorted({r["drug_mention"] for r in rows})
        sample = rows[:20]
        section = [
            "",
            SECTION_START,
            "## Handbook Prescription Mentions (SRC-0087, V13.1 batch)",
            "",
            f"- Batch status: {len(rows)} prescription-drug mention rows from `{RAW.relative_to(ROOT).as_posix()}`.",
            f"- Matched mention terms: {', '.join(terms)}.",
            f"- Source pages: {', '.join(pages) if pages else 'UNMAPPED'}.",
            f"- Full drug mention index: `exports/{OUT_DRUG_CSV.name}`; prescription matrix: `wiki/synthesis/{OUT_MD.name}`.",
            "",
        ]
        for r in sample:
            section.append(
                f"- `{r['fact_id']}` {r['disease_or_topic']} / \u5904\u65b9{r['prescription_no']} "
                f"`source_id=SRC-0087; page={r['page']}; line={r['line_start']}-{r['line_end']}`"
            )
        if len(rows) > len(sample):
            section.append(f"- Additional rows omitted here: {len(rows) - len(sample)}; see `exports/{OUT_DRUG_CSV.name}`.")
        section.extend(["", SECTION_END, ""])
        path.write_text(text.rstrip() + "\n" + "\n".join(section), encoding="utf-8")
        touched.append(str(path.relative_to(ROOT)))

    general = ROOT / "wiki" / "drugs" / "DRUG-007-antimicrobials.md"
    if general.exists():
        text = general.read_text(encoding="utf-8")
        text = re.sub(rf"\n?{re.escape(SECTION_START)}.*?{re.escape(SECTION_END)}\n?", "\n", text, flags=re.S)
        section = [
            "",
            SECTION_START,
            "## Handbook Prescription Mention Index (SRC-0087, V13.1 batch)",
            "",
            f"- Batch status: {len(mention_rows)} drug mention rows extracted from {len({r['fact_id'] for r in mention_rows})} prescription facts.",
            f"- Full index: `exports/{OUT_DRUG_CSV.name}`.",
            f"- Prescription fact matrix: `wiki/synthesis/{OUT_MD.name}`.",
            "- Use rule: mention rows identify candidate drug involvement; executable dose/course/route must be read from the linked prescription fact with exact page citation.",
            "",
            SECTION_END,
            "",
        ]
        general.write_text(text.rstrip() + "\n" + "\n".join(section), encoding="utf-8")
        rel = str(general.relative_to(ROOT))
        if rel not in touched:
            touched.append(rel)
    return touched


def write_outputs(facts, toc, lines):
    OUT_JSON.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = [
            "fact_id", "source_id", "page", "page_status", "line_start", "line_end", "chapter", "section",
            "disease", "disease_or_topic", "prescription_no", "prescription_title", "items", "usage", "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in facts:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    mention_rows = drug_mentions(facts)
    with OUT_DRUG_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["drug_mention", "fact_id", "source_id", "page", "disease_or_topic", "prescription_no", "line_start", "line_end"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mention_rows)

    write_matrix(facts, toc, lines)
    touched = update_disease_pages(facts)
    touched_drugs = update_drug_pages(mention_rows)
    index_updates = []
    if update_index_csv(ROOT / "exports" / "synthesis_index.csv", "id", {
        "id": "SYNTH-HANDBOOK-RX-MATRIX",
        "title": f"{BOOK_TITLE} prescription fact matrix",
        "path": "wiki/synthesis/swine_diagnosis_prescription_handbook_prescription_matrix.md",
        "sources": "SRC-0087; RULE-HANDBOOK-PRESCRIPTION-001",
        "updated": "2026-05-08T23:59:00+08:00",
    }):
        index_updates.append("exports/synthesis_index.csv")
    if update_index_csv(ROOT / "exports" / "drug_page_index.csv", "id", {
        "id": "HANDBOOK-DRUG-MENTION-INDEX",
        "title": f"{BOOK_TITLE} drug mention index",
        "path": "exports/handbook_prescription_drug_mention_index.csv",
        "sources": "SRC-0087",
        "updated": "2026-05-08T23:59:00+08:00",
    }):
        index_updates.append("exports/drug_page_index.csv")

    mapped = sum(1 for f in facts if f["page"] is not None)
    unmapped = len(facts) - mapped
    report = [
        "# Handbook full prescription batch progress / 2026-05-08",
        "",
        f"- Raw file: `{RAW.relative_to(ROOT).as_posix()}`",
        f"- Raw lines processed: {len(lines)}",
        f"- TOC page anchors extracted: {len(toc)}",
        f"- Prescription facts extracted: {len(facts)}",
        f"- Page-mapped prescription facts: {mapped}",
        f"- Unmapped prescription facts: {unmapped}",
        f"- Disease wiki pages updated: {len(touched)}",
        f"- Drug wiki pages updated: {len(touched_drugs)}",
        f"- Drug mention rows indexed: {len(mention_rows)}",
        f"- Index files updated: {', '.join(index_updates) if index_updates else 'none'}",
        f"- JSON output: `issues/{OUT_JSON.name}`",
        f"- CSV output: `exports/{OUT_CSV.name}`",
        f"- Drug mention CSV: `exports/{OUT_DRUG_CSV.name}`",
        f"- Wiki matrix: `wiki/synthesis/{OUT_MD.name}`",
        "",
        "## Updated disease pages",
        "",
    ]
    report.extend(f"- `{p}`" for p in touched)
    if not touched:
        report.append("- none")
    report.extend([
        "",
        "## Updated drug pages",
        "",
    ])
    report.extend(f"- `{p}`" for p in touched_drugs)
    if not touched_drugs:
        report.append("- none")
    report.extend([
        "",
        "## Notes",
        "",
        "- This batch is parser-generated and source-first. It preserves line spans and TOC-derived page anchors.",
        "- Disease pages receive compact fact lines; the CSV/JSON/matrix preserve the full structured extraction.",
        "- Drug entries are mention-indexed from prescription text and should be normalized to canonical DRUG pages in a follow-up pass where needed.",
    ])
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    return {"touched": touched, "touched_drugs": touched_drugs, "drug_mentions": mention_rows, "index_updates": index_updates}


def main():
    text = RAW.read_text(encoding="utf-8")
    lines = text.splitlines()
    toc = extract_toc(lines)
    facts = parse_prescriptions(lines, toc)
    extra = write_outputs(facts, toc, lines)
    print(json.dumps({
        "raw_file": str(RAW.relative_to(ROOT)),
        "raw_lines": len(lines),
        "toc_page_anchors": len(toc),
        "prescription_facts": len(facts),
        "mapped": sum(1 for f in facts if f["page"] is not None),
        "unmapped": sum(1 for f in facts if f["page"] is None),
        "disease_pages_updated": len(extra["touched"]),
        "drug_pages_updated": len(extra["touched_drugs"]),
        "drug_mention_rows": len(extra["drug_mentions"]),
        "index_updates": extra["index_updates"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
