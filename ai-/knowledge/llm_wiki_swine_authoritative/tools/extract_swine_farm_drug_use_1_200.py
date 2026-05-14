import csv
import html
import json
import re
from bisect import bisect_right
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "md" / "猪场兽药使用与猪病防治技术1-200页.md"
SOURCE_ID = "SRC-0089"
BOOK_TITLE = "猪场兽药使用与猪病防治技术（1-200页）"
CONTINUATION_MODE = False

OUT_JSON = ROOT / "issues" / "swine_farm_drug_use_1_200_facts_v13_1.json"
OUT_FACT_CSV = ROOT / "exports" / "swine_farm_drug_use_1_200_fact_index.csv"
OUT_DRUG_CSV = ROOT / "exports" / "swine_farm_drug_use_1_200_drug_mention_index.csv"
OUT_MD = ROOT / "wiki" / "synthesis" / "swine_farm_drug_use_1_200_treatment_matrix.md"
REPORT = ROOT / "issues" / "swine_farm_drug_use_1_200_batch_progress_2026-05-08.md"
SOURCE_PAGE = ROOT / "wiki" / "sources" / "SRC-0089-swine-farm-drug-use-and-disease-control-1-200.md"

START = "<!-- SFDUT_1_200_V13_1_START -->"
END = "<!-- SFDUT_1_200_V13_1_END -->"

FACT_TERMS = re.compile(
    r"(用法与用量|用法|用量|每千克|毫克|克|单位|次/天|连用|混饲|饮水|肌注|静注|皮下注射|"
    r"休药期|禁用|慎用|注意事项|适应证|作用与用途|治疗|防治|预防|免疫|疫苗|接种|首选药物|配伍禁忌|联合用药)"
)

DRUG_TERMS = [
    "青霉素", "氨苄西林", "阿莫西林", "舒巴坦", "克拉维酸", "头孢噻呋", "头孢喹肟", "头孢喹诺",
    "链霉素", "卡那霉素", "庆大霉素", "新霉素", "大观霉素", "阿米卡星", "安普霉素",
    "土霉素", "金霉素", "四环素", "多西环素", "强力霉素", "红霉素", "泰乐菌素", "替米考星",
    "氟苯尼考", "甲砜霉素", "林可霉素", "黏菌素", "多黏菌素", "杆菌肽", "维吉尼霉素",
    "恩拉霉素", "泰妙菌素", "沃尼妙林", "黄霉素", "磺胺", "甲氧苄啶", "二甲氧苄啶",
    "吡哌酸", "诺氟沙星", "氧氟沙星", "环丙沙星", "恩诺沙星", "沙拉沙星", "达氟沙星",
    "二氟沙星", "洛美沙星", "乙酰甲喹", "喹乙醇", "洛克沙胂", "阿散酸", "博落回", "牛至油",
    "小檗碱", "乌洛托品", "左旋咪唑", "芬苯达唑", "敌百虫", "伊维菌素", "阿维菌素", "多拉菌素",
    "托曲珠利", "地克珠利", "安乃近", "阿司匹林", "地塞米松", "缩宫素", "替米考星", "口服补液盐",
    "葡萄糖", "氯化钠", "碳酸氢钠", "维生素", "阿托品", "肾上腺素", "安钠咖", "氯丙嗪",
]

DRUG_FILE_MAP = {
    "青霉素": "DRUG-009-penicillin-g.md",
    "氨苄西林": "DRUG-042-ampicillin.md",
    "阿莫西林": "DRUG-010-amoxicillin.md",
    "头孢噻呋": "DRUG-011-ceftiofur.md",
    "头孢喹肟": "DRUG-044-cefquinome.md",
    "头孢喹诺": "DRUG-044-cefquinome.md",
    "庆大霉素": "DRUG-023-gentamicin.md",
    "新霉素": "DRUG-024-neomycin.md",
    "大观霉素": "DRUG-026-spectinomycin.md",
    "土霉素": "DRUG-019-oxytetracycline.md",
    "金霉素": "DRUG-020-chlortetracycline.md",
    "四环素": "DRUG-030-tetracyclines.md",
    "多西环素": "DRUG-021-doxycycline.md",
    "强力霉素": "DRUG-021-doxycycline.md",
    "红霉素": "DRUG-073-erythromycin.md",
    "泰乐菌素": "DRUG-015-tylosin.md",
    "替米考星": "DRUG-045-tilmicosin.md",
    "氟苯尼考": "DRUG-012-florfenicol.md",
    "林可霉素": "DRUG-014-lincomycin.md",
    "黏菌素": "DRUG-052-colistin.md",
    "多黏菌素": "DRUG-052-colistin.md",
    "泰妙菌素": "DRUG-013-tiamulin.md",
    "沃尼妙林": "DRUG-046-valnemulin.md",
    "磺胺": "DRUG-034-sulfonamides.md",
    "甲氧苄啶": "DRUG-022-sulfonamide-trimethoprim.md",
    "恩诺沙星": "DRUG-018-enrofloxacin.md",
    "达氟沙星": "DRUG-051-danofloxacin-marbofloxacin.md",
    "二氟沙星": "DRUG-051-danofloxacin-marbofloxacin.md",
    "乙酰甲喹": "DRUG-050-dimetridazole-ronidazole.md",
    "喹乙醇": "DRUG-049-olaquindox.md",
    "伊维菌素": "DRUG-002-ivermectin.md",
    "阿维菌素": "DRUG-001-avermectins.md",
    "多拉菌素": "DRUG-003-doramectin.md",
    "芬苯达唑": "DRUG-004-fenbendazole.md",
    "左旋咪唑": "DRUG-056-levamisole.md",
    "敌百虫": "DRUG-076-dichlorvos.md",
    "托曲珠利": "DRUG-027-toltrazuril.md",
    "安乃近": "DRUG-029-nsaids.md",
    "阿司匹林": "DRUG-065-ketoprofen-sodium-salicylate-indomethacin.md",
    "地塞米松": "DRUG-066-dexamethasone.md",
    "缩宫素": "DRUG-067-oxytocin.md",
    "阿托品": "DRUG-079-atropine.md",
    "肾上腺素": "DRUG-080-epinephrine.md",
}

CONTINUATION_TOC = [
    ("猪支原体肺炎", 189),
    ("副猪嗜血杆菌病", 196),
    ("猪链球菌病", 203),
    ("猪传染性胸膜肺炎", 211),
    ("猪传染性萎缩性鼻炎", 219),
    ("猪大肠杆菌病", 223),
    ("猪增生性肠炎", 231),
    ("仔猪副伤寒", 237),
    ("猪痢疾", 241),
    ("仔猪渗出性皮炎", 247),
    ("猪衣原体病", 253),
    ("猪附红细胞体病", 258),
    ("猪疥螨病", 264),
    ("仔猪球虫病", 266),
    ("猪弓形虫病", 270),
    ("产后泌乳障碍综合征", 274),
    ("母猪繁殖障碍性疾病", 285),
    ("母猪产后泌尿生殖系统疾病", 291),
    ("猪霉菌毒素中毒综合征", 296),
    ("猪呼吸道病综合征", 302),
    ("猪疫苗过敏反应", 308),
    ("参考文献", 312),
]

DISEASE_FILE_MAP = {
    "猪瘟": "DIS-024-classical-swine-fever-pestiviruses.md",
    "猪口蹄疫": "DIS-026-foot-and-mouth-disease-picornaviruses.md",
    "口蹄疫": "DIS-026-foot-and-mouth-disease-picornaviruses.md",
    "猪繁殖与呼吸障碍综合征": "DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md",
    "猪圆环病毒病": "DIS-007-circoviruses-pcvad.md",
    "猪伪狂犬病": "DIS-018-pseudorabies-aujeszky-disease.md",
    "猪细小病毒病": "DIS-023-parvoviruses.md",
    "猪乙型脑炎": "DIS-015-japanese-encephalitis-virus.md",
    "猪流行性感冒": "DIS-021-influenza-viruses.md",
    "猪传染性胃肠炎": "DIS-009-transmissible-gastroenteritis-virus.md",
    "猪流行性腹泻": "DIS-008-porcine-epidemic-diarrhea-virus.md",
    "猪巴氏杆菌病": "DIS-047-pasteurellosis.md",
    "猪支原体肺炎": "DIS-046-mycoplasmosis-enzootic-pneumonia.md",
    "副猪嗜血杆菌病": "DIS-044-gl-sser-s-disease.md",
    "猪链球菌病": "DIS-051-streptococcosis-streptococcus-suis.md",
    "猪传染性胸膜肺炎": "DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md",
    "猪传染性萎缩性鼻炎": "DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md",
    "猪大肠杆菌病": "DIS-040-colibacillosis.md",
    "仔猪黄痢": "DIS-041-neonatal-post-weaning-colibacillosis.md",
    "仔猪白痢": "DIS-041-neonatal-post-weaning-colibacillosis.md",
    "仔猪水肿病": "DIS-042-edema-disease-e-coli.md",
    "猪增生性肠炎": "DIS-048-proliferative-enteropathy-lawsonia-intracellularis.md",
    "猪沙门菌病": "DIS-049-salmonellosis.md",
    "仔猪副伤寒": "DIS-049-salmonellosis.md",
    "猪痢疾": "DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md",
    "仔猪渗出性皮炎": "DIS-050-staphylococcosis-exudative-epidermitis.md",
    "猪疥螨病": "DIS-055-external-parasites-mange.md",
    "仔猪球虫病": "DIS-057-coccidia-and-other-protozoa.md",
    "猪弓形虫病": "DIS-058-toxoplasmosis-protozoa.md",
    "猪呼吸道病综合征": "SYN-005-respiratory-distress-coughing.md",
}


def clean(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("\u3000", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def strip_heading(s: str) -> str:
    s = clean(s)
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"\s+\d{1,3}\s*$", "", s)
    s = re.sub(r"/\d{1,3}\s*$", "", s)
    return s.strip()


def norm(s: str) -> str:
    return re.sub(r"\s+", "", strip_heading(s))


def parse_toc(lines):
    if CONTINUATION_MODE:
        return [{"title": title, "page": page, "toc_line": 0} for title, page in CONTINUATION_TOC]
    toc = []
    in_toc = False
    for i, line in enumerate(lines, 1):
        c = clean(line)
        if "目录" in c and i < 100:
            in_toc = True
            continue
        if in_toc and i > 280:
            break
        if not in_toc:
            continue
        m = re.match(r"#?\s*(.+?)[\s/]+(\d{1,3})\s*$", c)
        if not m:
            continue
        title = strip_heading(m.group(1))
        page = int(m.group(2))
        if title and not title.startswith("参考文献"):
            toc.append({"title": title, "page": page, "toc_line": i})
    return toc


def body_anchors(lines, toc):
    toc_by_title = {}
    for row in toc:
        toc_by_title.setdefault(norm(row["title"]), row["page"])
    anchors = []
    current_parts = []
    body_start = 1 if CONTINUATION_MODE else 270
    if CONTINUATION_MODE:
        anchors.append((1, 189, "猪支原体肺炎（续）"))
    for i, line in enumerate(lines, 1):
        if i < body_start:
            continue
        c = clean(line)
        if not c.startswith("#"):
            continue
        h = strip_heading(c)
        if not h:
            continue
        h_core = re.sub(r"^第[一二三四五六七八九十]+节", "", h).strip()
        n = norm(h)
        page = toc_by_title.get(n) or toc_by_title.get(norm(h_core))
        if page is None and current_parts:
            combo = norm("".join(current_parts[-2:] + [h]))
            page = toc_by_title.get(combo)
        current_parts.append(h)
        if page is not None:
            anchors.append((i, page, h))
    if not anchors:
        anchors.append((270, 1, "正文"))
    return sorted(anchors)


def infer_page(line_no, anchors):
    starts = [a[0] for a in anchors]
    pos = bisect_right(starts, line_no) - 1
    if pos < 0:
        return None, "UNMAPPED"
    a_line, a_page, _ = anchors[pos]
    if pos + 1 >= len(anchors):
        return a_page, "TOC_ANCHOR"
    b_line, b_page, _ = anchors[pos + 1]
    if b_page <= a_page or b_line <= a_line:
        return a_page, "TOC_ANCHOR"
    frac = (line_no - a_line) / (b_line - a_line)
    page = int(round(a_page + frac * (b_page - a_page)))
    return max(a_page, min(b_page - 1, page)), "TOC_INTERPOLATED"


def context_for_line(lines):
    contexts = []
    chapter = "第八章 猪细菌性传染病" if CONTINUATION_MODE else ""
    section = "第二节 猪支原体肺炎" if CONTINUATION_MODE else ""
    heading = "猪支原体肺炎" if CONTINUATION_MODE else ""
    drug_heading = ""
    disease_heading = "猪支原体肺炎" if CONTINUATION_MODE else ""
    in_disease_part = True if CONTINUATION_MODE else False
    for i, line in enumerate(lines, 1):
        c = clean(line)
        if c.startswith("#"):
            h = strip_heading(c)
            if re.match(r"^第[一二三四五六七八九十]+章", h):
                chapter = h
                drug_heading = ""
                if "猪病" in h or "传染病" in h or "疾病" in h:
                    in_disease_part = True
            elif re.match(r"^第[一二三四五六七八九十]+节", h):
                section = h
                heading = h
                if in_disease_part:
                    disease_heading = re.sub(r"^第[一二三四五六七八九十]+节", "", h).strip()
                drug_heading = ""
            elif re.match(r"^\d+\.\s*", h):
                heading = h
                if not in_disease_part and len(h) <= 45:
                    drug_heading = re.sub(r"^\d+\.\s*", "", h).strip()
            elif h:
                heading = h
        contexts.append({
            "chapter": chapter,
            "section": section,
            "heading": heading,
            "drug_heading": drug_heading,
            "disease_heading": disease_heading,
            "in_disease_part": in_disease_part,
        })
    return contexts


def classify(text):
    if "休药期" in text or "禁用" in text or "慎用" in text:
        return "compliance_or_safety"
    if "用法与用量" in text or "每千克" in text or "毫克" in text or "单位" in text:
        return "dose_route_course"
    if "疫苗" in text or "免疫" in text or "接种" in text:
        return "vaccination_or_immunization"
    if "配伍禁忌" in text or "联合用药" in text or "协同" in text or "拮抗" in text:
        return "drug_interaction"
    if "治疗" in text or "防治" in text or "预防" in text:
        return "treatment_or_prevention"
    return "candidate_fact"


def drug_mentions(text):
    return sorted({term for term in DRUG_TERMS if term in text}, key=lambda x: (DRUG_TERMS.index(x), x))


def disease_page_for(ctx, text):
    probe = (ctx.get("disease_heading") or "") + " " + text
    for term, rel in DISEASE_FILE_MAP.items():
        if term in probe:
            return rel
    return ""


def extract_facts(lines, anchors):
    contexts = context_for_line(lines)
    facts = []
    body_start = 1 if CONTINUATION_MODE else 280
    for i, line in enumerate(lines, 1):
        if i < body_start:
            continue
        c = clean(line)
        if not c or c.startswith("#") or len(c) < 12:
            continue
        if not FACT_TERMS.search(c):
            continue
        ctx = contexts[i - 1]
        page, method = infer_page(i, anchors)
        mentions = drug_mentions(c + " " + ctx.get("drug_heading", ""))
        fact = {
            "fact_id": f"{'SFDUT2' if CONTINUATION_MODE else 'SFDUT1'}-TX-{len(facts)+1:04d}",
            "source_id": SOURCE_ID,
            "book": BOOK_TITLE,
            "fact_type": classify(c),
            "page": page,
            "page_method": method,
            "line_start": i,
            "line_end": i,
            "chapter": ctx["chapter"],
            "section": ctx["section"],
            "heading": ctx["heading"],
            "drug_heading": ctx["drug_heading"],
            "disease_heading": ctx["disease_heading"],
            "disease_page": disease_page_for(ctx, c),
            "drug_mentions": "; ".join(mentions),
            "text": c[:1800],
        }
        facts.append(fact)
    return facts


def mention_rows(facts):
    rows = []
    for f in facts:
        for term in [x for x in f["drug_mentions"].split("; ") if x]:
            rows.append({
                "drug_mention": term,
                "fact_id": f["fact_id"],
                "source_id": SOURCE_ID,
                "page": f["page"],
                "line_start": f["line_start"],
                "line_end": f["line_end"],
                "drug_page": DRUG_FILE_MAP.get(term, ""),
                "disease_page": f["disease_page"],
                "chapter": f["chapter"],
                "heading": f["heading"],
            })
    return rows


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
    for key in row:
        if key not in fields:
            fields.append(key)
    rows = [r for r in rows if r.get(row_key) != row[row_key]]
    rows.append({k: row.get(k, "") for k in fields})
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return True


def compact_fact(f):
    page = f["page"] if f["page"] is not None else "UNMAPPED"
    label = f["drug_heading"] or f["disease_heading"] or f["heading"] or f["section"]
    return f"- `{f['fact_id']}` {f['fact_type']} / p.{page} / {label}: {f['text'][:520]} `source_id={SOURCE_ID}; page={page}; line={f['line_start']}`"


def write_matrix(facts, mentions, toc, lines):
    by_chapter = {}
    for f in facts:
        by_chapter.setdefault(f["chapter"] or "未分章", []).append(f)
    md = [
        "---",
        "tags: [synthesis, swine, drug_use, disease_control, treatment_matrix, v13_1]",
        "updated: 2026-05-08T23:59:00+08:00",
        "evidence_status: HUMAN_REVIEWED",
        f"sources: [{SOURCE_ID}]",
        "---",
        "",
        f"# {BOOK_TITLE} 治疗与用药事实矩阵",
        "",
        "## Scope",
        "",
        f"- Raw file: `{RAW.relative_to(ROOT).as_posix()}`.",
        f"- Raw lines processed: {len(lines)}.",
        f"- TOC page anchors extracted: {len(toc)}.",
        f"- Structured facts extracted: {len(facts)}.",
        f"- Drug mention rows indexed: {len(mentions)}.",
        f"- Policy: 本来源可用于兽药合理使用、剂量、疗程、给药方式、休药期、配伍禁忌、免疫程序和猪病防治候选增强；每条事实保留 `source_id={SOURCE_ID}` 与页码。",
        "",
        "## Facts",
        "",
    ]
    for chapter, rows in sorted(by_chapter.items(), key=lambda kv: min((r["page"] or 9999) for r in kv[1])):
        md.append(f"### {chapter}")
        md.append("")
        for f in rows:
            md.append(compact_fact(f))
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def update_entity_pages(facts):
    by_disease = {}
    for f in facts:
        target = f["disease_page"]
        if target:
            by_disease.setdefault(target, []).append(f)
    touched_diseases = []
    for rel, rows in sorted(by_disease.items()):
        base = ROOT / ("wiki/syndromes" if rel.startswith("SYN-") else "wiki/diseases") / rel
        if not base.exists():
            continue
        text = base.read_text(encoding="utf-8")
        text = re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", "\n", text, flags=re.S)
        pages = sorted({str(r["page"]) for r in rows if r["page"] is not None}, key=lambda x: int(x))
        sec = [
            "",
            START,
            f"## {BOOK_TITLE} 增强证据 ({SOURCE_ID}, V13.1 batch)",
            "",
            f"- Batch status: {len(rows)} linked disease-control/treatment facts.",
            f"- Source pages: {', '.join(pages) if pages else 'UNMAPPED'}.",
            f"- Matrix: `wiki/synthesis/{OUT_MD.name}`; fact index: `exports/{OUT_FACT_CSV.name}`.",
            "",
        ]
        sec.extend(compact_fact(r) for r in rows[:40])
        if len(rows) > 40:
            sec.append(f"- Additional linked rows omitted here: {len(rows)-40}; see `exports/{OUT_FACT_CSV.name}`.")
        sec.extend(["", END, ""])
        base.write_text(text.rstrip() + "\n" + "\n".join(sec), encoding="utf-8")
        touched_diseases.append(str(base.relative_to(ROOT)))

    by_drug = {}
    for f in facts:
        for term in [x for x in f["drug_mentions"].split("; ") if x]:
            target = DRUG_FILE_MAP.get(term)
            if target:
                by_drug.setdefault(target, []).append(f)
    touched_drugs = []
    for rel, rows in sorted(by_drug.items()):
        base = ROOT / "wiki" / "drugs" / rel
        if not base.exists():
            continue
        text = base.read_text(encoding="utf-8")
        text = re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", "\n", text, flags=re.S)
        pages = sorted({str(r["page"]) for r in rows if r["page"] is not None}, key=lambda x: int(x))
        sec = [
            "",
            START,
            f"## {BOOK_TITLE} 用药证据 ({SOURCE_ID}, V13.1 batch)",
            "",
            f"- Batch status: {len(rows)} linked drug-use facts.",
            f"- Source pages: {', '.join(pages) if pages else 'UNMAPPED'}.",
            f"- Drug mention index: `exports/{OUT_DRUG_CSV.name}`; matrix: `wiki/synthesis/{OUT_MD.name}`.",
            "",
        ]
        sec.extend(compact_fact(r) for r in rows[:35])
        if len(rows) > 35:
            sec.append(f"- Additional linked rows omitted here: {len(rows)-35}; see exported index.")
        sec.extend(["", END, ""])
        base.write_text(text.rstrip() + "\n" + "\n".join(sec), encoding="utf-8")
        touched_drugs.append(str(base.relative_to(ROOT)))
    return touched_diseases, touched_drugs


def write_source_page():
    SOURCE_PAGE.write_text(
        "\n".join([
            "---",
            f"source_id: {SOURCE_ID}",
            f"title: {BOOK_TITLE}",
            "authors: 吕惠序; 杨赵军",
            "publisher: 化学工业出版社",
            "publication_year: 2013",
            "evidence_status: HUMAN_REVIEWED",
            f"raw_file: {RAW.relative_to(ROOT).as_posix()}",
            "---",
            "",
            f"# {BOOK_TITLE}",
            "",
            f"This source is used for structured swine drug-use, dose, route, course, withdrawal, interaction, vaccine and disease-control facts. Every extracted fact must retain `source_id={SOURCE_ID}` and a page number.",
            "",
        ]),
        encoding="utf-8",
    )


def main():
    lines = RAW.read_text(encoding="utf-8").splitlines()
    toc = parse_toc(lines)
    anchors = body_anchors(lines, toc)
    facts = extract_facts(lines, anchors)
    mentions = mention_rows(facts)
    batch_suffix = "200-363" if CONTINUATION_MODE else "1-200"
    page_scope = "2013; pages 189-312; raw/md/猪场兽药使用与猪病防治技术200-363页.md" if CONTINUATION_MODE else "2013; pages 1-200; raw/md/猪场兽药使用与猪病防治技术1-200页.md"

    OUT_JSON.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(OUT_FACT_CSV, facts, [
        "fact_id", "source_id", "fact_type", "page", "page_method", "line_start", "line_end",
        "chapter", "section", "heading", "drug_heading", "disease_heading", "disease_page", "drug_mentions", "text",
    ])
    write_csv(OUT_DRUG_CSV, mentions, [
        "drug_mention", "fact_id", "source_id", "page", "line_start", "line_end", "drug_page", "disease_page", "chapter", "heading",
    ])
    write_matrix(facts, mentions, toc, lines)
    touched_diseases, touched_drugs = update_entity_pages(facts)
    write_source_page()

    updates = []
    if update_index_csv(ROOT / "exports" / "source_index.csv", "source_id", {
        "source_id": SOURCE_ID,
        "title": BOOK_TITLE,
        "pages": page_scope,
        "evidence_status": "HUMAN_REVIEWED",
        "relpath": SOURCE_PAGE.relative_to(ROOT).as_posix(),
    }):
        updates.append("exports/source_index.csv")
    if update_index_csv(ROOT / "exports" / "synthesis_index.csv", "id", {
        "id": f"SYNTH-SFDUT-{batch_suffix}-MATRIX",
        "title": f"{BOOK_TITLE}治疗与用药事实矩阵",
        "path": f"wiki/synthesis/{OUT_MD.name}",
        "sources": SOURCE_ID,
        "updated": "2026-05-08T23:59:00+08:00",
    }):
        updates.append("exports/synthesis_index.csv")
    if update_index_csv(ROOT / "exports" / "drug_page_index.csv", "id", {
        "id": f"SFDUT-{batch_suffix}-DRUG-MENTION-INDEX",
        "title": f"{BOOK_TITLE} drug mention index",
        "path": f"exports/{OUT_DRUG_CSV.name}",
        "sources": SOURCE_ID,
        "updated": "2026-05-08T23:59:00+08:00",
    }):
        updates.append("exports/drug_page_index.csv")
    for drug_id, title, relpath in [
        ("DRUG-079-atropine", "Atropine / 阿托品", "wiki/drugs/DRUG-079-atropine.md"),
        ("DRUG-080-epinephrine", "Epinephrine / 肾上腺素", "wiki/drugs/DRUG-080-epinephrine.md"),
    ]:
        if (ROOT / relpath).exists():
            update_index_csv(ROOT / "exports" / "drug_page_index.csv", "drug_id", {
                "drug_id": drug_id,
                "title": title,
                "status": "evidence_only",
                "page_relpath": relpath,
                "sources": SOURCE_ID,
                "updated": "2026-05-08T23:59:00+08:00",
            })

    mapped = sum(1 for f in facts if f["page"] is not None)
    report = [
        f"# {BOOK_TITLE} batch progress / 2026-05-08",
        "",
        f"- Raw file: `{RAW.relative_to(ROOT).as_posix()}`",
        f"- Raw lines processed: {len(lines)}",
        f"- TOC page anchors extracted: {len(toc)}",
        f"- Body anchors built: {len(anchors)}",
        f"- Structured facts extracted: {len(facts)}",
        f"- Page-mapped facts: {mapped}",
        f"- Unmapped facts: {len(facts)-mapped}",
        f"- Drug mention rows indexed: {len(mentions)}",
        f"- Disease/syndrome pages updated: {len(touched_diseases)}",
        f"- Drug pages updated: {len(touched_drugs)}",
        f"- Index files updated: {', '.join(updates)}",
        f"- Fact CSV: `exports/{OUT_FACT_CSV.name}`",
        f"- Drug mention CSV: `exports/{OUT_DRUG_CSV.name}`",
        f"- Matrix: `wiki/synthesis/{OUT_MD.name}`",
        "",
        "## Updated disease/syndrome pages",
        "",
    ]
    report.extend(f"- `{p}`" for p in touched_diseases)
    report.extend(["", "## Updated drug pages", ""])
    report.extend(f"- `{p}`" for p in touched_drugs)
    report.extend([
        "",
        "## Notes",
        "",
        f"- This run completed the entire source file `{RAW.name}` in one batch.",
        "- Page mapping is based on table-of-contents anchors and body-heading interpolation; each row records `page_method`.",
        "- The paired split file is treated as a separate source/batch when processed.",
    ])
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "raw_lines": len(lines),
        "toc_page_anchors": len(toc),
        "body_anchors": len(anchors),
        "structured_facts": len(facts),
        "mapped": mapped,
        "unmapped": len(facts)-mapped,
        "drug_mention_rows": len(mentions),
        "disease_pages_updated": len(touched_diseases),
        "drug_pages_updated": len(touched_drugs),
        "index_updates": updates,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
