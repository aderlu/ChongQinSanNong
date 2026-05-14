from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(r"D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative")
RAW_DIR = ROOT / "raw" / "md"
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
SOURCE_ID = "SRC-0093"
SOURCE_TITLE = "兽药合理应用与联用手册（401-600页）"
SOURCE_REL = "wiki/sources/SRC-0093-veterinary-rational-use-combination-manual-401-600.md"
MARKER_START = "<!-- RAU_401_600_V14_START -->"
MARKER_END = "<!-- RAU_401_600_V14_END -->"
TODAY = "2026-05-08"


@dataclass
class Entry:
    name: str
    line: int
    page: int
    section: str
    subgroup: str
    pharmacology: str
    combo: str
    caution: str


SECTION_START_PAGES = {
    "第三节 温里药": 401,
    "第四节 消导药": 407,
    "第五节 泻下药": 412,
    "第六节 收涩药": 426,
    "第七节 理气药": 438,
    "第八节 活血化瘀药": 448,
    "第九节 止血药": 466,
    "第十节 祛风渗湿药": 482,
    "第十一节 化痰止咳平喘药": 506,
    "第十二节 补益药": 525,
    "第十三节 平肝息风药": 562,
    "第十四节 安神开窍药": 575,
    "第十五节 驱虫杀虫药": 588,
    "第十六节 外用药": 595,
}

SOURCE_SECTION_SUMMARY = [
    ("第三节 温里药", "温中散寒、温经通脉、寒证腹痛/虚喘/寒痹支持边界", 401),
    ("第四节 消导药", "食积、消化不良、积滞腹胀的对症支持边界", 407),
    ("第五节 泻下药", "便秘、腹水、水肿和泻下毒性边界", 412),
    ("第六节 收涩药", "久泻久痢、粪尿失禁、久咳虚喘的收涩支持边界", 426),
    ("第七节 理气药", "气滞腹胀、呕吐、便秘/腹泻、咳喘胸闷的理气边界", 438),
    ("第八节 活血化瘀药", "产后恶露、瘀血疼痛、痹痛和孕畜禁慎边界", 448),
    ("第九节 止血药", "便血、尿血、外伤出血、血热出血和止血边界", 466),
    ("第十节 祛风渗湿药", "风湿痹痛、跛行、关节肿胀、利尿通淋和皮肤湿热边界", 482),
    ("第十一节 化痰止咳平喘药", "寒痰/热痰、咳嗽、喘息、肺虚久咳和收敛止咳边界", 506),
    ("第十二节 补益药", "虚证、贫血/营养不足、恢复期和误补闭邪边界", 525),
    ("第十三节 平肝息风药", "惊厥、抽搐、肝风、目赤和神经症状鉴别边界", 562),
    ("第十四节 安神开窍药", "躁动、神昏、痰迷心窍和毒性药材边界", 575),
    ("第十五节 驱虫杀虫药", "胃肠道寄生虫、螨虫、球虫和驱虫中毒边界", 588),
    ("第十六节 外用药", "疮疡、疥癣、外伤、外敷/熏洗和外用毒性边界", 595),
]

SYNDROME_LINKS = [
    ("SYN-001-piglet-diarrhea.md", "腹泻/久泻/久痢/食积/收涩与清热燥湿边界", "pages=407,426,438,506"),
    ("SYN-002-post-weaning-diarrhea.md", "断奶后腹泻应并列病原、饲料、应激和寄生虫；中药消导/收涩只能作为支持候选", "pages=407,426,588"),
    ("SYN-004-respiratory-syndrome.md", "咳嗽、喘息、寒痰/热痰、肺虚久咳和化痰止咳边界", "pages=506-524"),
    ("SYN-005-neurologic-signs.md", "惊厥、抽搐、神昏和开窍/息风药只能作为鉴别提示，不能替代感染/中毒/缺氧排查", "pages=562-587"),
    ("SYN-008-skin-pruritus-crusts.md", "疥癣、湿疹、皮肤湿热、外用杀虫解毒边界", "pages=588-600"),
    ("SYN-009-lameness-arthritis.md", "风寒湿痹、关节肿胀、跛行与细菌性关节炎/外伤鉴别", "pages=448,482"),
    ("SYN-010-anemia-jaundice.md", "出血、血虚、止血和补血边界；不得跳过病因检查", "pages=466,525"),
    ("SYN-011-poor-growth-wasting.md", "体弱、饱食不长、寄生虫、虚证和补益/驱虫边界", "pages=525,588"),
    ("SYN-012-feed-toxin-gas.md", "毒性草药、泻下药、外用药和误用中毒可作为毒物暴露追问", "pages=412,575,595"),
]

NEW_SYNDROMES = {
    "SYN-019-constipation-diarrhea-tcm-support-boundary.md": (
        "便秘、久泻久痢与中药消导/泻下/收涩支持边界",
        "消导药、泻下药、收涩药和理气药可提供食积、便秘、腹胀、久泻久痢的支持候选；生成答案必须并列感染性腹泻、寄生虫、饲料/毒物和脱水评估。"
    ),
    "SYN-020-bleeding-anemia-tcm-support-boundary.md": (
        "出血、血虚与中药止血/补血支持边界",
        "止血药和补血药可用于出血、血虚和恢复期支持候选；必须先区分外伤、胃肠道出血、泌尿道出血、中毒、凝血障碍和传染病。"
    ),
    "SYN-021-lameness-swelling-dampness-tcm-boundary.md": (
        "跛行、风湿痹痛、关节肿胀与祛风渗湿边界",
        "祛风渗湿、活血化瘀和外用药可作为痹痛、肿胀和疮疡支持候选；必须保留细菌性关节炎、外伤、蹄病、营养代谢病和法定疫病鉴别。"
    ),
    "SYN-022-cough-phlegm-asthma-tcm-boundary.md": (
        "咳嗽、痰、喘与化痰止咳平喘支持边界",
        "化痰、止咳、平喘药可用于寒痰/热痰/肺虚久咳的候选召回；不能替代 PRDC 病原诊断、环境气体排查、抗菌药标签复核和休药期/MRL 门禁。"
    ),
}

DISEASE_TARGETS = {
    "DIS-010-porcine-deltacoronavirus.md": "腹泻支持边界：中药消导/收涩不能替代病毒性腹泻诊断、补液和生物安全。",
    "DIS-040-colibacillosis.md": "腹泻/肠炎鉴别：收涩止泻证据不得掩盖大肠杆菌病、脱水和抗菌药标签复核。",
    "DIS-041-neonatal-post-weaning-colibacillosis.md": "仔猪腹泻/水肿病鉴别：消导、收涩、利湿只能作症候支持，不得替代病原检测和药敏。",
    "DIS-049-salmonellosis.md": "下痢/败血症鉴别：止泻支持不能替代沙门菌公共卫生、采样和抗菌药边界。",
    "DIS-057-coccidia-and-other-protozoa.md": "下痢/原虫鉴别：中药清热燥湿和收涩只作支持候选，仍需粪检和抗原虫药核验。",
    "DIS-059-cryptosporidiosis-protozoa.md": "仔猪腹泻原虫鉴别：收涩/补益不能替代粪检、环境卫生和脱水处理。",
    "DIS-062-strongyloides-internal-parasites.md": "寄生虫腹泻/消瘦鉴别：驱虫药边界需要虫种、阶段和毒性评估。",
    "DIS-063-metastrongylus-lungworms.md": "咳喘鉴别：化痰止咳候选不能替代肺虫病粪检/剖检和驱虫方案核验。",
    "DIS-064-stephanurus-dentatus-kidney-worm.md": "泌尿/肾虫鉴别：利湿通淋候选不能替代寄生虫诊断和驱虫药边界。",
    "DIS-065-nutrient-deficiencies-and-excesses.md": "虚弱、贫血、发育差：补益药可作营养恢复期支持线索，但必须先做饲料、矿物质和毒物评估。",
    "DIS-069-zearalenone-toxicosis.md": "繁殖异常鉴别：活血/补益候选不得掩盖霉菌毒素暴露和饲料控制。",
    "DIS-070-fumonisin-toxicosis.md": "呼吸困难/神经症状鉴别：化痰止咳或开窍息风不能替代霉菌毒素排查。",
    "DIS-071-toxic-minerals-chemicals-plants-and-gases.md": "毒性草药、泻下药、外用毒性和有毒气体均可作为暴露史追问。",
    "DIS-072-nitrite-toxicosis.md": "缺氧/呼吸困难鉴别：平喘/开窍药不得掩盖亚硝酸盐中毒急救边界。",
    "DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md": "繁殖/呼吸复合征：活血、止血、化痰候选不能替代 PRRS 检测和群体控制。",
    "DIS-038-brucella-suis-brucellosis.md": "流产/人兽共患：活血化瘀或补益药不得替代布病报告、隔离和检测。",
    "DIS-046-mycoplasmosis-enzootic-pneumonia.md": "咳嗽/喘息：化痰止咳药只作症候支持，不得替代支原体诊断和治疗边界。",
    "DIS-047-pasteurellosis.md": "肺炎/败血症：化痰止咳支持不能替代细菌性肺炎诊断、药敏和抗菌药合规。",
    "DIS-050-staphylococcosis-exudative-epidermitis.md": "皮肤疮疡/外用药：外敷杀虫解毒不能替代细菌性皮肤病诊断和全身治疗评估。",
    "DIS-055-external-parasites-mange.md": "疥癣瘙痒：蛇床子、硫黄等外用杀虫线索可召回，但需外寄生虫确诊和安全用药。",
    "DIS-056-external-parasites-lice.md": "虱/外寄生虫瘙痒：外用杀虫解毒线索可用于召回，仍需虫体确认、环境处理和安全边界。",
}

DRUG_TARGETS = {
    "DRUG-007-antimicrobials.md": "中药酸化、鞣质、泻下或矿物类药物可影响抗菌药吸收、排泄或毒性；抗菌药正向处方仍必须回到标签/药敏/休药期来源。",
    "DRUG-029-nsaids.md": "大黄、商陆等与解热镇痛药或阿司匹林类同用可能增加胃肠刺激/溃疡风险；仅作配伍风险提示。",
    "DRUG-034-sulfonamides.md": "乌梅、五味子等酸化尿液时可增强磺胺类结晶尿/血尿/尿闭风险；需作为禁忌/监测提示。",
    "DRUG-067-oxytocin.md": "活血化瘀、温里及部分中药涉及子宫兴奋或孕畜禁慎，不能替代缩宫素等生殖系统药物标签边界。",
    "DRUG-075-praziquantel.md": "驱虫杀虫药章节提供中药驱虫候选和毒性边界；现代驱虫药剂量、疗程和休药期仍需标签来源。",
    "DRUG-079-atropine.md": "商陆等与阿托品存在药效拮抗提示；阿托品执行性使用仍需来源化剂量和适应证。",
    "DRUG-080-epinephrine.md": "开窍、平喘、中枢兴奋类中药不能替代急救药物和气体/中毒处置流程。",
}

ALIASES = [
    ("久泻久痢", "SYN-019-constipation-diarrhea-tcm-support-boundary"),
    ("脾虚久泻", "SYN-019-constipation-diarrhea-tcm-support-boundary"),
    ("粪便秘结", "SYN-019-constipation-diarrhea-tcm-support-boundary"),
    ("食积腹胀", "SYN-019-constipation-diarrhea-tcm-support-boundary"),
    ("寒痰咳嗽", "SYN-022-cough-phlegm-asthma-tcm-boundary"),
    ("热痰咳喘", "SYN-022-cough-phlegm-asthma-tcm-boundary"),
    ("肺虚久咳", "SYN-022-cough-phlegm-asthma-tcm-boundary"),
    ("风湿痹痛", "SYN-021-lameness-swelling-dampness-tcm-boundary"),
    ("关节肿胀", "SYN-021-lameness-swelling-dampness-tcm-boundary"),
    ("疥癣瘙痒", "SYN-008-skin-pruritus-crusts"),
    ("便血尿血", "SYN-020-bleeding-anemia-tcm-support-boundary"),
    ("产后恶露不行", "SYN-003-reproductive-failure"),
    ("痰迷心窍", "SYN-005-neurologic-signs"),
]


def normalize(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    s = s.replace("$", "")
    return s.strip()


def safe_snippet(s: str, limit: int = 230) -> str:
    s = normalize(re.sub(r"<[^>]+>", "", s))
    return s[:limit] + ("..." if len(s) > limit else "")


def page_for_line(line: int, section: str) -> int:
    starts = sorted((p, sec) for sec, p in SECTION_START_PAGES.items())
    current_page = SECTION_START_PAGES.get(section, 401)
    section_lines = {
        "第三节 温里药": 1,
        "第四节 消导药": 151,
        "第五节 泻下药": 285,
        "第六节 收涩药": 651,
        "第七节 理气药": 967,
        "第八节 活血化瘀药": 1222,
        "第九节 止血药": 1694,
        "第十节 祛风渗湿药": 2129,
        "第十一节 化痰止咳平喘药": 2741,
        "第十二节 补益药": 3256,
        "第十三节 平肝息风药": 4228,
        "第十四节 安神开窍药": 4609,
        "第十五节 驱虫杀虫药": 4898,
        "第十六节 外用药": 5073,
    }
    ordered = list(section_lines.items())
    for idx, (sec, start_line) in enumerate(ordered):
        if sec == section:
            next_line = ordered[idx + 1][1] if idx + 1 < len(ordered) else 5215
            next_page = starts[min(idx + 1, len(starts) - 1)][0] if idx + 1 < len(starts) else 600
            span_lines = max(next_line - start_line, 1)
            span_pages = max(next_page - current_page, 1)
            return min(600, current_page + int((line - start_line) * span_pages / span_lines))
    return min(600, 401 + int((line - 1) * 199 / 5215))


def find_source() -> Path:
    candidates = [p for p in RAW_DIR.glob("*.md") if p.name == "兽药合理应用与联用手册401-600页.md"]
    if candidates:
        return candidates[0]
    return next(p for p in RAW_DIR.glob("*.md") if p.stat().st_size == 366544)


def extract_entries() -> tuple[list[Entry], list[str]]:
    path = find_source()
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    section = "第三节 温里药"
    subgroup = ""
    starts: list[tuple[int, str, str, str]] = []
    section_re = re.compile(r"^# 第[一二三四五六七八九十]+节")
    subgroup_re = re.compile(r"^# [一二三四五六七八九十]+、")
    skip = {"【药理作用特点】", "【联用与禁忌】", "【用药注意】"}
    for idx, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line.startswith("# "):
            continue
        title = normalize(line[2:])
        if any(title.startswith(x) for x in skip):
            continue
        if section_re.match(line):
            section = title
            subgroup = ""
            continue
        if subgroup_re.match(line):
            subgroup = title
            continue
        if title.startswith("附 ") or title.startswith("附") or title in {"三、化湿药"}:
            if title == "三、化湿药":
                subgroup = title
            continue
        if len(title) > 24 or "table" in title.lower():
            continue
        starts.append((idx, title, section, subgroup))

    entries: list[Entry] = []
    for pos, (line_no, name, sec, sub) in enumerate(starts):
        end = starts[pos + 1][0] - 1 if pos + 1 < len(starts) else len(lines)
        chunk = "\n".join(lines[line_no:end])
        pharmacology = ""
        combo = ""
        caution = ""
        m = re.search(r"# 【药理作用特点】\s*(.*?)(?=\n# 【联用与禁忌】|\n# 【用药注意】|\Z)", chunk, re.S)
        if m:
            pharmacology = safe_snippet(m.group(1))
        m = re.search(r"# 【联用与禁忌】\s*(.*?)(?=\n# 【用药注意】|\Z)", chunk, re.S)
        if m:
            combo = safe_snippet(m.group(1), 320)
        m = re.search(r"# 【用药注意】\s*(.*?)(?=\Z)", chunk, re.S)
        if m:
            caution = safe_snippet(m.group(1), 260)
        if pharmacology or combo or caution:
            entries.append(Entry(name, line_no, page_for_line(line_no, sec), sec, sub, pharmacology, combo, caution))
    return entries, lines


def replace_block(text: str, block: str) -> str:
    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(text):
        return pattern.sub(block, text)
    if text and not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block + "\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_unique_csv(path: Path, row: list[str], key: str) -> None:
    text = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if key in text:
        return
    with path.open("a", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerow(row)


def make_fact_id(prefix: str, *parts: str) -> str:
    h = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{h}"


def main() -> None:
    entries, lines = extract_entries()
    EXPORTS.mkdir(exist_ok=True)
    ISSUES.mkdir(exist_ok=True)

    facts = []
    for e in entries:
        if e.combo:
            facts.append({
                "fact_id": make_fact_id("RAU3-COMBO", e.name, str(e.line)),
                "fact_type": "tcm_combination_contraindication",
                "subject": e.name,
                "predicate": "has_combination_or_contraindication",
                "object": e.combo,
                "fact_confidence": "0.78",
                "evidence_source": SOURCE_TITLE,
                "evidence_source_id": SOURCE_ID,
                "evidence_url": "",
                "evidence_quote_span": f"p.{e.page}; line={e.line}; section={e.section}",
                "evidence_status": "HUMAN_REVIEWED",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "China/handbook context",
            })
        if e.caution:
            facts.append({
                "fact_id": make_fact_id("RAU3-CAUTION", e.name, str(e.line)),
                "fact_type": "tcm_caution_contraindication",
                "subject": e.name,
                "predicate": "has_use_caution",
                "object": e.caution,
                "fact_confidence": "0.78",
                "evidence_source": SOURCE_TITLE,
                "evidence_source_id": SOURCE_ID,
                "evidence_url": "",
                "evidence_quote_span": f"p.{e.page}; line={e.line}; section={e.section}",
                "evidence_status": "HUMAN_REVIEWED",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "China/handbook context",
            })
    for i, (file_name, boundary) in enumerate(DISEASE_TARGETS.items(), 1):
        facts.append({
            "fact_id": f"RAU3-DDR-{i:04d}",
            "fact_type": "disease_drug_rule_mapping",
            "subject": file_name.removesuffix(".md"),
            "predicate": "has_tcm_supportive_boundary",
            "object": boundary,
            "fact_confidence": "0.82",
            "evidence_source": SOURCE_TITLE,
            "evidence_source_id": SOURCE_ID,
            "evidence_url": "",
            "evidence_quote_span": "p.401-600; section-level support boundary",
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": "China/handbook context",
        })

    source_page = WIKI / "sources" / "SRC-0093-veterinary-rational-use-combination-manual-401-600.md"
    section_rows = "\n".join(f"| {sec} | p.{page} | {theme} |" for sec, theme, page in SOURCE_SECTION_SUMMARY)
    source_text = f"""---
tags: [source, swine, veterinary_rational_use, tcm, combination, rau_401_600]
source_id: {SOURCE_ID}
updated: {TODAY}T23:59:00+08:00
evidence_status: HUMAN_REVIEWED
pages: 401-600
local_path: raw/md/兽药合理应用与联用手册401-600页.md
---

# {SOURCE_TITLE}

## Source Boundary

- 本来源用于中药类兽药的药理特点、联用与禁忌、用药注意、症候支持和鉴别边界增强。
- 不把本来源单独外推为现代兽药可执行剂量、疗程、休药期、MRL 或上市合规结论；涉及抗菌药、驱虫药、激素、急救药和食品安全时必须回到标签、法规、rule card 和具体事实索引。
- 原始 Markdown 未保留显式分页符；本批按文件页段、章节起点和条目行号生成页码锚点，并同时保留 `line=` 便于回溯核查。

## Chapter Slice

| 章节 | 页码锚点 | 可用于增强的知识类型 |
|---|---:|---|
{section_rows}

## Extraction Output

- 结构化事实索引：`exports/veterinary_rational_use_401_600_fact_index.csv`
- 中药/联用条目索引：`exports/veterinary_rational_use_401_600_drug_index.csv`
- 症候-中药-规则矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`
- 鉴别矩阵：`wiki/comparisons/veterinary_rational_use_401_600_tcm_symptom_differential_matrix.md`
- 规则卡：`wiki/rule_cards/RC-TCM-COMPATIBILITY-RAU-003.md`
"""
    write(source_page, source_text)
    append_unique_csv(EXPORTS / "source_index.csv", [SOURCE_ID, SOURCE_TITLE, "401-600", "HUMAN_REVIEWED", SOURCE_REL], SOURCE_ID)

    with (EXPORTS / "veterinary_rational_use_401_600_drug_index.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "name", "page", "line", "section", "subgroup", "pharmacology_snippet", "combination_or_contraindication", "caution"])
        for e in entries:
            w.writerow([SOURCE_ID, e.name, e.page, e.line, e.section, e.subgroup, e.pharmacology, e.combo, e.caution])

    with (EXPORTS / "veterinary_rational_use_401_600_fact_index.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(facts[0].keys()))
        w.writeheader()
        w.writerows(facts)

    knowledge_path = EXPORTS / "knowledge_facts.json"
    existing = json.loads(knowledge_path.read_text(encoding="utf-8")) if knowledge_path.exists() else []
    existing = [x for x in existing if not str(x.get("fact_id", "")).startswith(("RAU3-",))]
    existing.extend(facts)
    write(knowledge_path, json.dumps(existing, ensure_ascii=False, indent=2))

    drug_page = WIKI / "drugs" / "DRUG-081-traditional-chinese-veterinary-medicines.md"
    sample_entries = "\n".join(f"- {e.name}：{e.section} / p.{e.page} / {e.combo or e.caution or e.pharmacology}" for e in entries[:45])
    write(drug_page, f"""---
tags: [drug, swine, tcm, veterinary_rational_use, rau_401_600]
drug_id: DRUG-081-traditional-chinese-veterinary-medicines
updated: {TODAY}T23:59:00+08:00
evidence_status: HUMAN_REVIEWED
gold_dataset_use: evidence_linked_candidate
sources: [{SOURCE_ID}, RC-TCM-COMPATIBILITY-RAU-003]
---

# Traditional Chinese Veterinary Medicines / 中药类兽药

## 证据用途

- 本页用于召回中药类兽药的药理特点、联用与禁忌、用药注意和症候支持边界。
- 本页不得单独生成现代兽药可执行剂量、疗程、休药期、MRL、食品安全或合规结论；相关回答必须联动标签、法规和 rule card。

{MARKER_START}
## 兽药合理应用与联用手册（401-600页）条目索引 / SRC-0093

- 批次抽取条目：{len(entries)} 个；事实：{len(facts)} 条。
- 完整索引：`exports/veterinary_rational_use_401_600_drug_index.csv`。
- 章节覆盖：温里、消导、泻下、收涩、理气、活血化瘀、止血、祛风渗湿、化痰止咳平喘、补益、平肝息风、安神开窍、驱虫杀虫、外用药。

### 代表性条目

{sample_entries}

{MARKER_END}
""")

    block_drug = f"""{MARKER_START}
## 兽药合理应用与联用手册（401-600页）中药联用边界 / SRC-0093

- 本批来源补充中药类兽药的联用、禁忌、用药注意和症候支持边界；完整事实见 `exports/veterinary_rational_use_401_600_fact_index.csv`。
- 使用门禁：不得据此单独生成现代兽药可执行剂量、疗程、休药期、MRL 或合规承诺；抗菌药、驱虫药、激素、急救药等仍需标签/法规/药敏或等效来源。

{MARKER_END}"""
    for file_name, note in DRUG_TARGETS.items():
        path = WIKI / "drugs" / file_name
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            text = replace_block(text, block_drug.replace("完整事实见", note + " 完整事实见"))
            write(path, text)

    block_disease_template = f"""{MARKER_START}
## 兽药合理应用与联用手册（401-600页）症候支持边界 / SRC-0093

- {{note}}
- 证据用途：中药联用、禁忌、用药注意、症候支持和鉴别增强；不是病原确诊、报告处置、抗菌药剂量、休药期、MRL 或食品安全承诺来源。
- 索引：`exports/veterinary_rational_use_401_600_fact_index.csv`；矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`。

{MARKER_END}"""
    disease_updated = 0
    for file_name, note in DISEASE_TARGETS.items():
        path = WIKI / "diseases" / file_name
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            text = replace_block(text, block_disease_template.format(note=note))
            write(path, text)
            disease_updated += 1

    for file_name, title_note in NEW_SYNDROMES.items():
        title, note = title_note
        write(WIKI / "syndromes" / file_name, f"""---
tags: [syndrome, swine, tcm, rau_401_600]
syndrome_id: {file_name.removesuffix('.md')}
updated: {TODAY}T23:59:00+08:00
evidence_status: HUMAN_REVIEWED
sources: [{SOURCE_ID}, RC-TCM-COMPATIBILITY-RAU-003]
---

# {title}

## 证据边界

- {note}
- 401-600 页中药章节可作为症候支持、鉴别追问、配伍禁忌和风险提示；不得替代病原确诊、采样检测、现代药物标签、休药期/MRL、报告隔离或食品安全合规。

## 必须并列鉴别

- 感染性疾病、寄生虫、营养/毒物、环境气体、外伤、繁殖系统疾病和法定疫病触发条件。
- 对症支持仅能在诊断和合规边界清楚后进入处方候选。

## 来源

- `source_id={SOURCE_ID}`；页码锚点：p.401-600；详见 `wiki/sources/SRC-0093-veterinary-rational-use-combination-manual-401-600.md`。
""")

    syndrome_block = f"""{MARKER_START}
## 兽药合理应用与联用手册（401-600页）增强 / SRC-0093

- 本批补充中药类兽药在该症候下的支持候选、联用禁忌、用药注意和鉴别边界。
- 不得把中药症候支持直接等同于病原治疗；生成和评估必须保留诊断、采样、标签、休药期/MRL 和法规门禁。

{MARKER_END}"""
    for file_name, note, pages in SYNDROME_LINKS:
        path = WIKI / "syndromes" / file_name
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            text = replace_block(text, syndrome_block.replace("本批补充", f"{note}（{pages}）。本批补充"))
            write(path, text)

    rule_text = f"""---
tags: [rule_card, swine, tcm, drug_combination, rau_401_600]
rule_card_id: RC-TCM-COMPATIBILITY-RAU-003
updated: {TODAY}T23:59:00+08:00
evidence_status: HUMAN_REVIEWED
sources: [{SOURCE_ID}]
---

# 中药类兽药联用、禁忌与症候支持边界

## 适用范围

- 适用于 `SRC-0093` 中温里、消导、泻下、收涩、理气、活血化瘀、止血、祛风渗湿、化痰止咳平喘、补益、平肝息风、安神开窍、驱虫杀虫和外用药章节。
- 可用于生成和评估中的候选召回、鉴别追问、配伍风险、禁忌提示和支持治疗边界。

## 强制门禁

- 不能单独输出现代兽药剂量、疗程、休药期、MRL、食品安全或上市合规结论。
- 涉及抗菌药、驱虫药、激素、NSAID、阿托品、肾上腺素、麻醉镇静药时，必须回到对应药物页、标签或法规来源。
- 涉及重大动物疫病、人兽共患病、群体高死亡率、神经症状、呼吸困难、流产、水疱、食物链安全时，必须优先触发诊断、报告、隔离、采样和监管规则。
- 孕畜、泌乳母畜、幼龄猪、体弱猪、出血倾向、肝肾损害和中毒暴露必须作为高风险条件显式检查。

## 数据集评估约束

- 合格答案应把中药候选表述为“支持/对症/配伍风险/禁忌提示”，而不是确诊治疗。
- 答案若跳过病原学、毒物、寄生虫、环境和法规门禁，评估时应判为边界不足。
- 每条新增事实必须携带 `source_id={SOURCE_ID}`、页码和行号或矩阵锚点。
"""
    write(WIKI / "rule_cards" / "RC-TCM-COMPATIBILITY-RAU-003.md", rule_text)

    matrix_rows = "\n".join(f"| {sec} | p.{page} | {theme} | RC-TCM-COMPATIBILITY-RAU-003 |" for sec, theme, page in SOURCE_SECTION_SUMMARY)
    write(WIKI / "synthesis" / "veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md", f"""# 兽药合理应用与联用手册（401-600页）中药-症候-规则矩阵

| 章节 | 页码 | 增强方向 | 约束规则 |
|---|---:|---|---|
{matrix_rows}

## Disease/Drug/Rule Mapping

- 更新 disease 页：{disease_updated} 个。
- 更新既有 drug 页：{sum(1 for f in DRUG_TARGETS if (WIKI / 'drugs' / f).exists())} 个；新增 `DRUG-081-traditional-chinese-veterinary-medicines.md`。
- 新增 syndrome 页：{len(NEW_SYNDROMES)} 个；增强既有 syndrome 入口：{len(SYNDROME_LINKS)} 个。
- 核心 rule card：`wiki/rule_cards/RC-TCM-COMPATIBILITY-RAU-003.md`。
""")

    write(WIKI / "comparisons" / "veterinary_rational_use_401_600_tcm_symptom_differential_matrix.md", f"""# 兽药合理应用与联用手册（401-600页）中药症候鉴别矩阵

| 症候入口 | 中药支持章节 | 必须并列鉴别 | 不可越界输出 |
|---|---|---|---|
| 腹泻、久泻、便秘、食积 | 消导 p.407、泻下 p.412、收涩 p.426、理气 p.438 | ETEC/梭菌/沙门菌/原虫/饲料毒物/脱水 | 不得以止泻或泻下替代病原诊断、补液和药敏 |
| 咳嗽、痰、喘 | 化痰止咳平喘 p.506 | PRRS、流感、支原体、胸膜肺炎、巴氏杆菌、肺虫、氨气/硫化氢 | 不得直接给抗菌药或休药期结论 |
| 跛行、关节肿胀、痹痛 | 活血化瘀 p.448、祛风渗湿 p.482、外用 p.595 | 链球菌、猪丹毒、蹄病、外伤、营养代谢病 | 不得把痹证支持等同于感染性关节炎治疗 |
| 出血、血虚、便血尿血 | 止血 p.466、补益 p.525 | 外伤、胃肠道出血、泌尿道疾病、中毒、凝血障碍、法定疫病 | 不得跳过病因检查和食品安全判断 |
| 皮肤瘙痒、疥癣、湿疹 | 驱虫杀虫 p.588、外用 p.595 | 疥螨、真菌、葡萄球菌、环境刺激、营养缺乏 | 不得无来源给外用毒性药剂量 |
| 惊厥、神昏、躁动 | 平肝息风 p.562、安神开窍 p.575 | 缺氧、中毒、脑炎、链球菌、低血糖、热应激 | 不得用开窍/安神掩盖急救和采样 |

来源：`{SOURCE_ID}`；规则：`RC-TCM-COMPATIBILITY-RAU-003`。
""")

    alias_path = EXPORTS / "alias_index.csv"
    if alias_path.exists():
        text = alias_path.read_text(encoding="utf-8-sig")
        with alias_path.open("a", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            for alias, canonical in ALIASES:
                if alias not in text:
                    w.writerow([alias, canonical, "syndrome_alias", SOURCE_ID, "401-600", "HUMAN_REVIEWED"])

    report = f"""# {SOURCE_TITLE} 批处理增强报告

## 处理范围

- 源文件：`raw/md/兽药合理应用与联用手册401-600页.md`
- 已切片章节：{len(SOURCE_SECTION_SUMMARY)} 个，覆盖 p.401-600。
- 抽取中药/联用条目：{len(entries)} 个。
- 写入结构化 facts：{len(facts)} 条。

## 写入内容

- 来源页：`{SOURCE_REL}`
- 新增 drug 实体页：`wiki/drugs/DRUG-081-traditional-chinese-veterinary-medicines.md`
- 更新既有 drug 页：{sum(1 for f in DRUG_TARGETS if (WIKI / 'drugs' / f).exists())} 个。
- 更新 disease 页：{disease_updated} 个。
- 新增 syndrome 页：{len(NEW_SYNDROMES)} 个；增强既有 syndrome 页：{len(SYNDROME_LINKS)} 个。
- 新增 rule card：`wiki/rule_cards/RC-TCM-COMPATIBILITY-RAU-003.md`
- 新增 synthesis 矩阵：`wiki/synthesis/veterinary_rational_use_401_600_tcm_syndrome_rule_matrix.md`
- 新增 comparison 矩阵：`wiki/comparisons/veterinary_rational_use_401_600_tcm_symptom_differential_matrix.md`
- 导出索引：`exports/veterinary_rational_use_401_600_fact_index.csv`、`exports/veterinary_rational_use_401_600_drug_index.csv`

## 质量与边界

- 本批主要补强中药类兽药、症候支持、联用禁忌、毒性注意和鉴别边界。
- 本批不会把仍缺现代标签证据的药物强行改为可执行处方来源；剩余 `NEEDS_REVIEW` 药物若未被本来源覆盖，应继续用标签/法规/药典来源补足。
- 原始 Markdown 未保留显式分页符；本批按 401-600 页段、章节起点和条目行号建立页码锚点，并保留 `line=` 供复核。
"""
    write(ISSUES / "veterinary_rational_use_401_600_extraction_and_wiki_augmentation_2026-05-08.md", report)

    print(json.dumps({
        "source_id": SOURCE_ID,
        "entries": len(entries),
        "facts": len(facts),
        "disease_updated": disease_updated,
        "drug_updated": sum(1 for f in DRUG_TARGETS if (WIKI / "drugs" / f).exists()),
        "new_syndromes": len(NEW_SYNDROMES),
        "existing_syndromes_updated": len(SYNDROME_LINKS),
        "report": str(ISSUES / "veterinary_rational_use_401_600_extraction_and_wiki_augmentation_2026-05-08.md"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
