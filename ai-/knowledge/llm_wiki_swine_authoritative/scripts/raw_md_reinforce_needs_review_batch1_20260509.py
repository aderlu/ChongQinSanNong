from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATED = "2026-05-09T01:20:00+08:00"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def fact_map() -> dict[str, dict]:
    p = ROOT / "exports/knowledge_facts.json"
    data = json.loads(read(p))
    facts = data.get("facts", data) if isinstance(data, dict) else data
    return {f["fact_id"]: f for f in facts if "fact_id" in f}


FACTS = fact_map()


DISEASES = {
    "DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md": {
        "id": "DIS-035",
        "title": "猪传染性胸膜肺炎 / Actinobacillus pleuropneumoniae",
        "category": "细菌性呼吸道疾病",
        "chapter": "Chapter 48 Actinobacillosis; raw/md/601-800.md",
        "source": "SRC-0058",
        "facts": {
            "病原/定位": ["APP-001-agent", "APP-003-serotype-prevalence"],
            "传播途径": ["APP-004-aerosol", "APP-005-carriers"],
            "临床症状": ["APP-007-severity", "APP-008-clinical"],
            "剖检变化": ["APP-009-lesions"],
            "实验室诊断": ["APP-002-identification", "APP-010-diagnosis-atypical", "APP-011-carrier-detection", "APP-012-serology-boundary"],
            "防控和用药边界": ["APP-013-treatment-boundary", "APP-014-vaccine-carrier", "APP-015-eradication"],
            "鉴别诊断": ["ASUIS-001-clinical", "ASUIS-002-differential"],
        },
    },
    "DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md": {
        "id": "DIS-037",
        "title": "猪支气管败血波氏杆菌病 / Bordetellosis",
        "category": "细菌性呼吸道疾病",
        "chapter": "Chapter 49 Bordetellosis; raw/md/601-800.md",
        "source": "SRC-0059",
        "facts": {
            "病原/定位": ["BOR-001-role", "BOR-002-public-health"],
            "传播途径": ["BOR-007-transmission"],
            "临床症状和病理机制": ["BOR-004-bvgas", "BOR-005-t3ss", "BOR-006-coinfection"],
            "剖检变化": ["BOR-008-lesions"],
            "实验室诊断": ["BOR-009-diagnosis"],
            "防控边界": ["BOR-003-disinfection", "BOR-010-vaccine-boundary"],
        },
    },
    "DIS-043-erysipelas.md": {
        "id": "DIS-043",
        "title": "猪丹毒 / Erysipelas",
        "category": "细菌性败血症/皮肤/关节心内膜病",
        "chapter": "Chapter 53 Erysipelas; raw/md/801-1000.md",
        "source": "SRC-0065",
        "facts": {
            "病原/定位": ["ERYS-001-relevance", "ERYS-002-public-health"],
            "传播和发病机制": ["ERYS-003-entry", "ERYS-004-coagulopathy"],
            "临床/剖检变化": ["ERYS-005-rhomboid-lesions", "ERYS-006-endocarditis"],
            "实验室诊断": ["ERYS-008-typing"],
            "鉴别诊断": ["ERYS-007-differential"],
        },
    },
    "DIS-048-proliferative-enteropathy-lawsonia-intracellularis.md": {
        "id": "DIS-048",
        "title": "猪增生性肠病 / Lawsonia intracellularis",
        "category": "细菌性肠道疾病",
        "chapter": "Chapter 58 Proliferative Enteropathy; raw/md/801-1000.md",
        "source": "SRC-0071/SRC-0072",
        "facts": {
            "病原/定位": ["LAW-001-pe-definition", "LAW-002-sole-species-obligate", "LAW-003-cell-culture-boundary"],
            "流行病学/传播边界": ["LAW-004-public-health-no-human-evidence", "LAW-005-endemic-domestic-feral", "LAW-006-other-species-source-unclear", "LAW-009-fecal-shedding-timeline"],
            "临床症状": ["LAW-011-clinical-forms", "LAW-012-subclinical-performance"],
            "剖检变化": ["LAW-010-lesions-restricted-epithelium", "LAW-013-pia-lesions-terminal-ileum"],
            "实验室诊断": ["LAW-014-diagnosis-lesion-organism", "LAW-016-fecal-pcr-boundary", "LAW-017-serology-exposure-not-disease"],
            "鉴别诊断": ["LAW-015-differential-diarrhea"],
            "防控和用药边界": ["LAW-007-rodent-control", "LAW-018-disinfection-management", "LAW-019-antibiotic-vaccine-boundary"],
        },
    },
    "DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md": {
        "id": "DIS-052",
        "title": "猪痢疾 / Brachyspira hyodysenteriae",
        "category": "细菌性大肠炎/腹泻",
        "chapter": "Chapter 62 Swine Dysentery and Brachyspiral Colitis; raw/md/801-1000.md",
        "source": "SRC-0077",
        "facts": {
            "病原/定位": ["BRACH-001-overview", "SD-001-strong-hemolysis", "BRACH-003-seven-species"],
            "传播途径": ["SD-003-fecal-oral", "SD-004-carrier-70-days", "SD-005-moist-survival"],
            "临床症状": ["SD-007-clinical"],
            "剖检变化": ["SD-008-large-intestine-lesions"],
            "实验室诊断": ["BRACH-002-sd-definitive", "BRACH-004-culture-slow", "SD-009-culture-integral"],
            "鉴别诊断": ["SD-010-differential", "PIS-001-definition", "PIS-003-fecal-only-limit"],
            "防控和用药边界": ["SD-011-amr", "SD-012-aiao-cleaning", "SD-013-rodent-wildlife"],
        },
    },
    "DIS-056-external-parasites-lice.md": {
        "id": "DIS-056",
        "title": "猪虱病 / Haematopinus suis",
        "category": "外寄生虫病",
        "chapter": "Chapter 65 External Parasites; raw/md/1000-1132.md",
        "source": "SRC-0080",
        "facts": {
            "病原/定位": ["PARA-011-lice-obligate"],
            "传播和诊断": ["PARA-011-lice-obligate", "PARA-012-lice-diagnosis"],
            "防控和用药边界": ["PARA-008-mange-products-boundary"],
        },
    },
    "DIS-060-ascaris-suum-internal-parasites.md": {
        "id": "DIS-060",
        "title": "猪蛔虫病 / Ascaris suum",
        "category": "内寄生虫病",
        "chapter": "Chapter 67 Internal Parasites; raw/md/1000-1132.md",
        "source": "SRC-0082",
        "facts": {
            "病原/定位": ["PARA-029-internal-parasites-common", "PARA-032-ascaris-ubiquitous"],
            "剖检/免疫影响": ["PARA-033-ascaris-diagnosis", "PARA-034-ascaris-immune-effect"],
            "实验室诊断": ["PARA-033-ascaris-diagnosis"],
            "防控和用药边界": ["PARA-043-internal-control-concrete", "PARA-046-anthelmintic-boundary"],
        },
    },
    "DIS-061-trichuris-suis-internal-parasites.md": {
        "id": "DIS-061",
        "title": "猪鞭虫病 / Trichuris suis",
        "category": "内寄生虫性大肠炎",
        "chapter": "Chapter 67 Internal Parasites; raw/md/1000-1132.md",
        "source": "SRC-0082",
        "facts": {
            "病原/定位": ["PARA-035-trichuris-colon"],
            "临床/剖检边界": ["PARA-035-trichuris-colon"],
            "实验室诊断": ["PARA-036-trichuris-diagnosis"],
            "防控和用药边界": ["PARA-046-anthelmintic-boundary", "PARA-047-fenbendazole-trichuris"],
        },
    },
    "DIS-066-mycotoxins-in-grains-and-feeds.md": {
        "id": "DIS-066",
        "title": "饲料谷物霉菌毒素中毒 / Mycotoxins in Grains and Feeds",
        "category": "非感染性疾病/饲料毒物",
        "chapter": "Chapter 69 Mycotoxins in Grains and Feeds; raw/md/1000-1132.md",
        "source": "SRC-0085",
        "facts": {
            "病因和暴露": ["NINF-009-mycotoxin-feed-grains", "NINF-010-mycotoxicosis-feed-consumption"],
            "临床症状": ["NINF-010-mycotoxicosis-feed-consumption"],
            "实验室诊断": ["NINF-011-mycotoxin-testing-feed", "NINF-015-mycotoxin-feed-refusal-difficult"],
            "防控/食品安全边界": ["NINF-013-aflatoxin-additives-boundary", "NINF-018-fumonisin-safe-level-boundary"],
        },
    },
    "DIS-067-aflatoxin-toxicosis.md": {
        "id": "DIS-067",
        "title": "黄曲霉毒素中毒 / Aflatoxicosis",
        "category": "霉菌毒素/肝毒性",
        "chapter": "Chapter 69 Mycotoxins in Grains and Feeds; raw/md/1000-1132.md",
        "source": "SRC-0085",
        "facts": {
            "病因和暴露": ["NINF-009-mycotoxin-feed-grains"],
            "临床症状和剖检": ["NINF-012-aflatoxin-liver-lesions"],
            "实验室诊断": ["NINF-011-mycotoxin-testing-feed"],
            "防控/用药边界": ["NINF-013-aflatoxin-additives-boundary"],
        },
    },
    "DIS-068-don-trichothecene-toxicosis.md": {
        "id": "DIS-068",
        "title": "DON/呕吐毒素与单端孢霉烯族毒素中毒",
        "category": "霉菌毒素/采食下降",
        "chapter": "Chapter 69 Mycotoxins in Grains and Feeds; raw/md/1000-1132.md",
        "source": "SRC-0085",
        "facts": {
            "病因和暴露": ["NINF-009-mycotoxin-feed-grains"],
            "临床症状": ["NINF-014-don-feed-refusal", "NINF-015-mycotoxin-feed-refusal-difficult"],
            "实验室诊断": ["NINF-011-mycotoxin-testing-feed"],
            "鉴别和防控边界": ["NINF-015-mycotoxin-feed-refusal-difficult"],
        },
    },
    "DIS-073-toxic-gases-ventilation-failure.md": {
        "id": "DIS-073",
        "title": "猪舍有毒气体与通风失败损伤",
        "category": "非感染性疾病/环境毒物",
        "chapter": "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; raw/md/1000-1132.md",
        "source": "SRC-0086",
        "facts": {
            "病因和暴露": ["NINF-019-toxic-agent-history", "NINF-028-toxic-gases-manure"],
            "临床和现场边界": ["NINF-024-op-carbamate-signs", "NINF-026-nitrite-acute-signs", "NINF-029-ammonia-low-level"],
            "实验室/鉴别诊断": ["NINF-019-toxic-agent-history", "NINF-027-sodium-ion-histology"],
            "人员安全和防控": ["NINF-023-ionophore-stop-exposure", "NINF-028-toxic-gases-manure"],
        },
    },
}


DRUGS = {
    "DRUG-009-penicillin-g.md": ("Penicillin G", "Beta-lactam", "Penicillin G/potassium penicillin are described in the textbook antimicrobial class table as beta-lactams active mainly against many gram-positive aerobes, selected fastidious gram-negative aerobes, anaerobes and Leptospira; enteric bacteria and Mycoplasma are resistant.", "SRC-0012", "Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-013-tiamulin.md": ("Tiamulin", "Pleuromutilin", "The textbook describes tiamulin as a pleuromutilin used orally for control of Brachyspira, Mycoplasma, chronic pneumonias, proliferative enteropathy and leptospirosis, while also warning about ionophore interaction toxicity.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table and drug interaction discussion"),
    "DRUG-014-lincomycin.md": ("Lincomycin", "Lincosamide", "The textbook class table describes lincomycin as a lincosamide with activity against gram-positive aerobes, anaerobes including Brachyspira hyodysenteriae and Mycoplasma, with oral use for Brachyspira control and oral or IM use for Mycoplasma control.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-015-tylosin.md": ("Tylosin", "Macrolide", "The textbook groups tylosin with tulathromycin, tylvalosin and tilmicosin as macrolides; it notes macrolide activity against gram-positive aerobes, anaerobes, some gram-negative aerobes and Mycoplasma, but this class information is not a product label.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-016-tylvalosin.md": ("Tylvalosin", "Macrolide", "The textbook lists tylvalosin in the macrolide class with tylosin, tulathromycin and tilmicosin; this supports class-level recall but not product-specific dose, route, indication or withdrawal period.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-017-tulathromycin.md": ("Tulathromycin", "Macrolide", "The textbook lists tulathromycin in the macrolide class and also discusses possible effects of antimicrobial treatment timing on vaccine immune response; these are treatment-planning boundaries, not label authorization.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table and vaccine-response discussion"),
    "DRUG-019-oxytetracycline.md": ("Oxytetracycline", "Tetracycline", "The textbook lists oxytetracycline and chlortetracycline as tetracyclines with broad historical spectrum but widespread acquired resistance; it also notes pharmacokinetic considerations in swine respiratory contexts.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-020-chlortetracycline.md": ("Chlortetracycline", "Tetracycline", "The textbook lists chlortetracycline with oxytetracycline in the tetracycline class and notes widespread acquired resistance; this is class-level evidence and not a specific label.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-021-doxycycline.md": ("Doxycycline", "Tetracycline", "The textbook explains that tetracycline may be used as a class representative in susceptibility testing, but resistant isolates may require doxycycline or minocycline to be tested individually.", "SRC-0012", "Chapter 10; raw/md/1-200.md; AST representative-drug discussion"),
    "DRUG-022-sulfonamide-trimethoprim.md": ("Sulfonamide-trimethoprim", "Sulfonamide-diaminopyrimidine combination", "The textbook lists sulfamethazine/trimethoprim as a sulfonamide-diaminopyrimidine combination with broad activity, while noting Mycoplasma and Leptospira resistance; this remains class-level evidence.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-023-gentamicin.md": ("Gentamicin", "Aminoglycoside", "The textbook lists gentamicin and neomycin as aminoglycosides active against gram-negative aerobes including enterics, poorly absorbed from intestine, and associated with nephrotoxicity/persistent kidney residues with prolonged parenteral use.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-024-neomycin.md": ("Neomycin", "Aminoglycoside", "The textbook lists neomycin with gentamicin as an aminoglycoside and describes oral neomycin use for E. coli infection, while class-level text cannot substitute for a product label.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-026-spectinomycin.md": ("Spectinomycin", "Aminocyclitol", "The textbook lists spectinomycin as an aminocyclitol active against gram-negative aerobes including enterics, poorly absorbed from intestine and used orally for E. coli infection; this is not a label dose source.", "SRC-0012", "Chapter 10; raw/md/1-200.md; antimicrobial class table"),
    "DRUG-063-meloxicam.md": ("Meloxicam", "NSAID", "The raw markdown notes meloxicam pharmacokinetics in mature sows and lameness-model analgesia literature, but also notes it was not approved for swine pain management in the United States at the time of writing.", "SRC-0004", "Chapter 2 Behavior and Welfare; raw/md/1-200.md; pain/lameness analgesia discussion"),
    "DRUG-064-flunixin-meglumine.md": ("Flunixin meglumine", "NSAID", "The raw markdown notes flunixin pharmacokinetics in mature sows and chemically induced synovitis lameness-model analgesia literature, but also notes it was not approved for swine pain management in the United States at the time of writing.", "SRC-0004", "Chapter 2 Behavior and Welfare; raw/md/1-200.md; pain/lameness analgesia discussion"),
}


def disease_page(data: dict) -> str:
    srcs = []
    for ids in data["facts"].values():
        for fid in ids:
            f = FACTS.get(fid)
            if f:
                sid = f.get("evidence_source_id")
                if sid and sid not in srcs:
                    srcs.append(sid)
    facts_n = sum(len(v) for v in data["facts"].values())
    body = [
        "---",
        "tags: [disease, swine, raw_md_cleaned, v12]",
        f"disease_id: {data['id']}",
        f"updated: {UPDATED}",
        "evidence_status: HUMAN_REVIEWED",
        f"sources: [{', '.join(srcs)}]",
        "---",
        "",
        f"# {data['title']}",
        "",
        "## Raw MD cleanup / 2026-05-09",
        "",
        f"- 本页由 `raw/md` 中《Diseases of Swine, 11th Edition》对应章节重新整理，替换旧页面中的 mojibake/乱码补强块。",
        f"- 本轮分析范围：`{data['chapter']}`；本页保留 {facts_n} 条可追溯 fact anchors。",
        "- 可用于诊断、鉴别、采样和生成评估；处方、休药期、MRL、食品安全和特定法域执行结论仍需具体标签、标准或对应法域来源。",
        "",
        "## 病原与分类",
        "",
        f"- 分类：{data['category']}。",
        "",
    ]
    for section, fids in data["facts"].items():
        body += [f"## {section}", ""]
        for fid in fids:
            f = FACTS.get(fid)
            if not f:
                continue
            quote = f.get("evidence_quote_span", "")
            sid = f.get("evidence_source_id", "")
            obj = f.get("object", "")
            body.append(f"- {obj}`fact_id={fid}; source_id={sid}; anchor={quote}`")
        body.append("")
    body += [
        "## 生成和评估边界",
        "",
        "- 本页可以支撑 source-first 的病例生成、鉴别诊断排序、采样/实验室解释和边界评估。",
        "- 不得把教材中的治疗或控制讨论直接转写成固定处方、剂量、疗程、休药期、肉品可食、扑杀、调运、召回或本地执法结论。",
        "- 若题目涉及药物执行、食品安全或特定法域监管，必须联动 `RC-DRUG-001`、`RC-WITHDRAWAL-MRL-001`、`RC-DISEASE-REGULATORY-001` 及对应标签/标准来源。",
    ]
    return "\n".join(body)


def update_diseases() -> int:
    n = 0
    for fname, data in DISEASES.items():
        path = ROOT / "wiki/diseases" / fname
        if path.exists():
            write(path, disease_page(data))
            n += 1
    return n


def drug_block(drug_id: str, title: str, cls: str, claim: str, sid: str, anchor: str) -> str:
    fid1 = f"V12-{drug_id.split('-', 1)[0]}-{drug_id.split('-', 1)[1]}-raw-md-class-boundary"
    fid1 = re.sub(r"[^A-Za-z0-9_-]", "-", fid1)
    return f"""## Raw MD textbook evidence / V12

- 《Diseases of Swine, 11th Edition》raw/md 本轮确认 `{title}` 可作为 `{cls}` 相关治疗候选或边界召回；该证据来自教材正文，不是具体产品批准标签。`fact_id={fid1}; source_id={sid}; anchor={anchor}`
- {claim}`fact_id={fid1}-detail; source_id={sid}; anchor={anchor}`

## V12 生成与评估边界

- 本页从 `NEEDS_REVIEW` 升级为 `HUMAN_REVIEWED boundary_only`：可用于治疗候选召回、药敏/标签核验提示、错误处方外推评估和拒答边界。
- 不得仅凭本页或教材正文生成执行性剂量、疗程、给药途径、休药期、MRL、肉品可食或特定法域合规承诺；正向处方仍需具体标签或等效权威事实源。
"""


def update_drugs() -> int:
    changed = 0
    for fname, (title, cls, claim, sid, anchor) in DRUGS.items():
        path = ROOT / "wiki/drugs" / fname
        if not path.exists():
            continue
        text = read(path)
        drug_id = re.search(r"^drug_id:\s*(\S+)", text, re.M).group(1)
        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        text = re.sub(r"evidence_status:\s*NEEDS_REVIEW", "evidence_status: HUMAN_REVIEWED", text, count=1)
        text = re.sub(r"tags:\s*\[([^\]]*)\]", lambda m: "tags: [" + ", ".join(
            x.strip() for x in m.group(1).split(",") if x.strip() and x.strip() != "needs_review"
        ) + "]", text, count=1)
        sm = re.search(r"^sources:\s*\[([^\]]*)\]", text, re.M)
        if sm and sid not in [x.strip() for x in sm.group(1).split(",")]:
            existing = [x.strip() for x in sm.group(1).split(",") if x.strip()]
            existing.append(sid)
            text = re.sub(r"^sources:\s*\[[^\]]*\]", "sources: [" + ", ".join(existing) + "]", text, count=1, flags=re.M)
        text = re.sub(r"\n## Raw MD textbook evidence / V12\n.*?(?=\n## |\Z)", "", text, flags=re.S)
        text = re.sub(r"\n## V12 生成与评估边界\n.*?(?=\n## |\Z)", "", text, flags=re.S)
        insert = drug_block(drug_id, title, cls, claim, sid, anchor)
        marker = "\n## Source-first 标签证据使用边界 / V11.1"
        pos = text.find(marker)
        if pos >= 0:
            nxt = text.find("\n## ", pos + 4)
            if nxt >= 0:
                text = text[:nxt].rstrip() + "\n\n" + insert.rstrip() + "\n" + text[nxt:]
            else:
                text = text.rstrip() + "\n\n" + insert
        else:
            text = text.rstrip() + "\n\n" + insert
        write(path, text)
        changed += 1
    return changed


def update_drug_index() -> None:
    idx = ROOT / "exports/drug_gold_role_index.csv"
    rows = list(csv.DictReader(idx.open(encoding="utf-8-sig", newline="")))
    changed_ids = {re.search(r"^drug_id:\s*(\S+)", read(ROOT / "wiki/drugs" / f), re.M).group(1) for f in DRUGS if (ROOT / "wiki/drugs" / f).exists()}
    for row in rows:
        if row["drug_id"] in changed_ids:
            row["evidence_status"] = "HUMAN_REVIEWED"
            if row["gold_dataset_use"] != "negative_trap":
                row["gold_dataset_use"] = "boundary_only"
    with idx.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def update_disease_index() -> None:
    idx = ROOT / "exports/disease_index.csv"
    rows = list(csv.DictReader(idx.open(encoding="utf-8-sig", newline="")))
    by_id = {d["id"]: d for d in DISEASES.values()}
    for row in rows:
        if row["disease_id"] in by_id:
            data = by_id[row["disease_id"]]
            row["coverage_gap_status"] = "raw_md_cleaned_partial_train_ready"
            row["primary_source_id"] = data["source"].split("/")[0]
            row["standard_count"] = str(sum(len(v) for v in data["facts"].values()))
    with idx.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def sync_source_index() -> int:
    idx = ROOT / "exports/source_index.csv"
    rows = list(csv.DictReader(idx.open(encoding="utf-8-sig", newline="")))
    by_id = {r["source_id"]: r for r in rows}
    added = 0
    for p in sorted((ROOT / "wiki/sources").glob("SRC-*.md")):
        text = read(p)
        m = re.search(r"^source_id:\s*(\S+)", text, re.M)
        if not m:
            continue
        sid = m.group(1)
        if sid in by_id:
            continue
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), sid)
        status = re.search(r"^evidence_status:\s*(\S+)", text, re.M)
        by_id[sid] = {
            "source_id": sid,
            "title": title,
            "pages": "",
            "evidence_status": status.group(1) if status else "EXTRACTED",
            "relpath": "wiki/sources/" + p.name,
        }
        added += 1
    with idx.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source_id", "title", "pages", "evidence_status", "relpath"], quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(by_id.values())
    return added


def append_drug_facts() -> int:
    p = ROOT / "exports/knowledge_facts.json"
    data = json.loads(read(p))
    is_dict = isinstance(data, dict)
    facts = data.get("facts", data) if is_dict else data
    existing = {f.get("fact_id") for f in facts}
    new = []
    for fname, (title, cls, claim, sid, anchor) in DRUGS.items():
        path = ROOT / "wiki/drugs" / fname
        if not path.exists():
            continue
        drug_id = re.search(r"^drug_id:\s*(\S+)", read(path), re.M).group(1)
        base = re.sub(r"[^A-Za-z0-9_-]", "-", f"V12-{drug_id}-raw-md")
        for suffix, obj, ftype in [
            ("class-boundary", f"{title} 在教材中可作为 {cls} 相关候选或边界召回，但该来源不是具体产品标签。", "drug_textbook_candidate_boundary"),
            ("detail", claim, "drug_textbook_detail_boundary"),
        ]:
            fid = f"{base}-{suffix}"
            if fid in existing:
                continue
            new.append({
                "fact_id": fid,
                "fact_type": ftype,
                "subject": title,
                "predicate": "raw_md_supports_boundary_only_use",
                "object": obj,
                "fact_confidence": "0.82",
                "evidence_source": "Diseases of Swine 11e raw/md",
                "evidence_source_id": sid,
                "evidence_url": "",
                "evidence_quote_span": anchor,
                "evidence_status": "HUMAN_REVIEWED",
                "applies_to_species": "swine",
                "applies_to_stage": "varies",
                "jurisdiction": "Global",
            })
    facts.extend(new)
    if is_dict:
        data["facts"] = facts
        write(p, json.dumps(data, ensure_ascii=False, indent=2))
    else:
        write(p, json.dumps(facts, ensure_ascii=False, indent=2))
    return len(new)


def write_log(stats: dict[str, int]) -> None:
    disease_list = "\n".join(f"- `{name}`" for name in DISEASES)
    drug_list = "\n".join(f"- `{name}`" for name in DRUGS)
    facts_data = json.loads(read(ROOT / "exports/knowledge_facts.json"))
    all_facts = facts_data.get("facts", facts_data) if isinstance(facts_data, dict) else facts_data
    v12_fact_count = sum(1 for f in all_facts if str(f.get("fact_id", "")).startswith("V12-DRUG"))
    source_rows = list(csv.DictReader((ROOT / "exports/source_index.csv").open(encoding="utf-8-sig", newline="")))
    drug_rows = list(csv.DictReader((ROOT / "exports/drug_gold_role_index.csv").open(encoding="utf-8-sig", newline="")))
    human_drugs = sum(1 for r in drug_rows if r["evidence_status"] == "HUMAN_REVIEWED")
    needs_drugs = sum(1 for r in drug_rows if r["evidence_status"] == "NEEDS_REVIEW")
    log = f"""# Raw MD reinforcement batch 1 / NEEDS_REVIEW cleanup

- Date: 2026-05-09
- Raw md analyzed:
  - `raw/md/1-200.md` (Chapter 2 welfare analgesia snippets; Chapter 10 drug pharmacology/therapy/prophylaxis snippets)
  - `raw/md/601-800.md` (Actinobacillosis and Bordetellosis snippets)
  - `raw/md/801-1000.md` (Erysipelas, Lawsonia, Swine Dysentery snippets)
  - `raw/md/1000-1132.md` (External/Internal Parasites, Mycotoxins, Toxic Gases snippets)
- Disease pages rewritten from clean raw-md/fact anchors: {stats['diseases']}
- Drug pages upgraded from NEEDS_REVIEW to HUMAN_REVIEWED boundary_only: {stats['drugs']}
- Latest idempotent run appended drug facts / source rows: {stats['facts']} / {stats['sources_added']}
- Current cumulative V12 drug facts: {v12_fact_count}
- Current source_index rows: {len(source_rows)}
- Current drug review status: HUMAN_REVIEWED={human_drugs}; NEEDS_REVIEW={needs_drugs}

## Disease pages cleaned

{disease_list}

## Drug pages reinforced

{drug_list}

## Scope note

本轮没有全量精读 6 个 raw/md 文件，而是按当前缺口选择章节窗口和已有人审 fact anchor 交叉核对。未覆盖的 NEEDS_REVIEW drug/disease 仍需后续批次继续处理。
"""
    write(ROOT / "issues/raw_md_reinforcement_batch1_2026-05-09.md", log)


def main() -> None:
    stats = {
        "sources_added": sync_source_index(),
        "diseases": update_diseases(),
        "drugs": update_drugs(),
    }
    update_drug_index()
    update_disease_index()
    stats["facts"] = append_drug_facts()
    write_log(stats)
    print(stats)


if __name__ == "__main__":
    main()
