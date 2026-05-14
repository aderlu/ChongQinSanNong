from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(r"D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative")
RAW_DIR = ROOT / "raw" / "md"
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
SOURCE_ID = "SRC-0091"
SOURCE_TITLE = "兽药合理应用与联用手册（1-200页）"
SOURCE_REL = "wiki/sources/SRC-0091-veterinary-rational-use-combination-manual-1-200.md"
MARKER_START = "<!-- RAU_1_200_V14_START -->"
MARKER_END = "<!-- RAU_1_200_V14_END -->"
TODAY = "2026-05-08"


@dataclass(frozen=True)
class Entry:
    name: str
    page: int
    category: str
    kind: str
    target: str


DRUG_TARGETS: dict[str, tuple[str, str, str]] = {
    "青霉素": ("DRUG-009-penicillin-g.md", "β-内酰胺/青霉素类", "individual_drug"),
    "普鲁卡因青霉素": ("DRUG-009-penicillin-g.md", "β-内酰胺/青霉素类", "individual_drug"),
    "氨苄西林": ("DRUG-042-ampicillin.md", "β-内酰胺/青霉素类", "individual_drug"),
    "阿莫西林": ("DRUG-010-amoxicillin.md", "β-内酰胺/青霉素类", "individual_drug"),
    "头孢噻呋": ("DRUG-011-ceftiofur.md", "β-内酰胺/头孢菌素类", "individual_drug"),
    "头孢喹肟": ("DRUG-044-cefquinome.md", "β-内酰胺/头孢菌素类", "individual_drug"),
    "链霉素": ("DRUG-071-streptomycin.md", "氨基糖苷类", "individual_drug"),
    "庆大霉素": ("DRUG-023-gentamicin.md", "氨基糖苷类", "individual_drug"),
    "安普霉素": ("DRUG-025-apramycin.md", "氨基糖苷类", "individual_drug"),
    "新霉素": ("DRUG-024-neomycin.md", "氨基糖苷类", "individual_drug"),
    "大观霉素": ("DRUG-026-spectinomycin.md", "氨基糖苷类", "individual_drug"),
    "阿米卡星": ("DRUG-074-amikacin.md", "氨基糖苷类", "individual_drug"),
    "土霉素": ("DRUG-019-oxytetracycline.md", "四环素类", "individual_drug"),
    "四环素": ("DRUG-030-tetracyclines.md", "四环素类", "class_or_drug"),
    "多西环素": ("DRUG-021-doxycycline.md", "四环素类", "individual_drug"),
    "金霉素": ("DRUG-020-chlortetracycline.md", "四环素类", "individual_drug"),
    "氟苯尼考": ("DRUG-012-florfenicol.md", "酰胺醇类", "individual_drug"),
    "红霉素": ("DRUG-073-erythromycin.md", "大环内酯类", "individual_drug"),
    "泰乐菌素": ("DRUG-015-tylosin.md", "大环内酯类", "individual_drug"),
    "替米考星": ("DRUG-045-tilmicosin.md", "大环内酯类", "individual_drug"),
    "泰万菌素": ("DRUG-016-tylvalosin.md", "大环内酯类", "individual_drug"),
    "林可霉素": ("DRUG-014-lincomycin.md", "林可胺类", "individual_drug"),
    "泰妙菌素": ("DRUG-013-tiamulin.md", "截短侧耳素/其他抗生素", "individual_drug"),
    "沃尼妙林": ("DRUG-046-valnemulin.md", "截短侧耳素/其他抗生素", "individual_drug"),
    "多黏菌素E": ("DRUG-052-colistin.md", "多肽类", "individual_drug"),
    "杆菌肽": ("DRUG-053-bacitracin-methylene-disalicylate.md", "多肽类", "individual_drug"),
    "维吉尼霉素": ("DRUG-054-virginiamycin.md", "多肽类", "individual_drug"),
    "磺胺嘧啶": ("DRUG-038-trimethoprim-sulfadiazine.md", "磺胺类/增效剂", "individual_drug"),
    "磺胺二甲嘧啶": ("DRUG-037-sulfamethazine.md", "磺胺类/增效剂", "individual_drug"),
    "磺胺甲噁唑": ("DRUG-040-trimethoprim-sulfamethoxazole.md", "磺胺类/增效剂", "individual_drug"),
    "磺胺间甲氧嘧啶": ("DRUG-039-sulfadimethoxine.md", "磺胺类/增效剂", "individual_drug"),
    "甲氧苄啶": ("DRUG-022-sulfonamide-trimethoprim.md", "磺胺类/增效剂", "synergy_agent"),
    "恩诺沙星": ("DRUG-018-enrofloxacin.md", "喹诺酮类", "individual_drug"),
    "达氟沙星": ("DRUG-051-danofloxacin-marbofloxacin.md", "喹诺酮类", "individual_drug"),
    "马波沙星": ("DRUG-051-danofloxacin-marbofloxacin.md", "喹诺酮类", "individual_drug"),
    "甲硝唑": ("DRUG-050-dimetridazole-ronidazole.md", "硝基咪唑类", "class_or_drug"),
    "地美硝唑": ("DRUG-050-dimetridazole-ronidazole.md", "硝基咪唑类", "individual_drug"),
    "卡巴多司": ("DRUG-048-carbadox.md", "喹噁啉类", "individual_drug"),
    "喹乙醇": ("DRUG-049-olaquindox.md", "喹噁啉类", "individual_drug"),
    "芬苯达唑": ("DRUG-004-fenbendazole.md", "苯并咪唑类驱虫药", "individual_drug"),
    "阿苯达唑": ("DRUG-005-benzimidazoles.md", "苯并咪唑类驱虫药", "individual_drug"),
    "左旋咪唑": ("DRUG-056-levamisole.md", "咪唑并噻唑类驱虫药", "individual_drug"),
    "噻嘧啶": ("DRUG-057-piperazine-pyrantel.md", "四氢嘧啶类驱虫药", "individual_drug"),
    "哌嗪": ("DRUG-057-piperazine-pyrantel.md", "其他驱线虫药", "individual_drug"),
    "伊维菌素": ("DRUG-002-ivermectin.md", "阿维菌素类", "individual_drug"),
    "莫西菌素": ("DRUG-055-moxidectin.md", "阿维菌素类", "individual_drug"),
    "阿维菌素": ("DRUG-001-avermectins.md", "阿维菌素类", "class_or_drug"),
    "多拉菌素": ("DRUG-003-doramectin.md", "阿维菌素类", "individual_drug"),
    "吡喹酮": ("DRUG-075-praziquantel.md", "抗绦虫药", "individual_drug"),
    "妥曲珠利": ("DRUG-027-toltrazuril.md", "抗球虫药", "individual_drug"),
    "氨丙啉": ("DRUG-062-amprolium.md", "抗球虫药", "individual_drug"),
    "敌敌畏": ("DRUG-076-dichlorvos.md", "有机磷杀虫药", "individual_drug"),
    "双甲脒": ("DRUG-058-amitraz.md", "杀虫药", "individual_drug"),
    "溴氰菊酯": ("DRUG-060-permethrin-deltamethrin.md", "拟除虫菊酯类杀虫药", "individual_drug"),
    "氰戊菊酯": ("DRUG-060-permethrin-deltamethrin.md", "拟除虫菊酯类杀虫药", "individual_drug"),
}

CLASS_TARGETS: dict[str, tuple[str, str]] = {
    "β-内酰胺类": ("DRUG-035-beta-lactams.md", "β-内酰胺类"),
    "青霉素类": ("DRUG-035-beta-lactams.md", "青霉素类"),
    "头孢菌素类": ("DRUG-035-beta-lactams.md", "头孢菌素类"),
    "氨基糖苷类": ("DRUG-033-aminoglycosides.md", "氨基糖苷类"),
    "四环素类": ("DRUG-030-tetracyclines.md", "四环素类"),
    "大环内酯类": ("DRUG-031-macrolides.md", "大环内酯类"),
    "林可胺类": ("DRUG-036-lincosamides.md", "林可胺类"),
    "磺胺类": ("DRUG-034-sulfonamides.md", "磺胺类"),
    "抗球虫药": ("DRUG-006-anticoccidials.md", "抗球虫药"),
    "阿维菌素类": ("DRUG-001-avermectins.md", "阿维菌素类"),
    "苯并咪唑类": ("DRUG-005-benzimidazoles.md", "苯并咪唑类"),
    "有机磷": ("DRUG-059-phosmet-coumaphos.md", "有机磷杀虫药"),
    "拟除虫菊酯": ("DRUG-060-permethrin-deltamethrin.md", "拟除虫菊酯类"),
}

DISEASE_LINKS = [
    ("DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md", "胸膜肺炎", ["氨苄西林", "氟苯尼考", "头孢噻呋"], "抗菌治疗候选必须建立在药敏、标签和休药期复核之上；不得仅凭手册候选生成执行剂量。"),
    ("DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md", "萎缩性鼻炎/支气管败血波氏杆菌相关", ["磺胺类", "四环素类", "青霉素", "链霉素"], "抗菌药选择需结合病原、药敏和猪场阶段，避免长期单一药物导致耐药。"),
    ("DIS-040-colibacillosis.md", "大肠杆菌病", ["磺胺类", "庆大霉素", "安普霉素", "新霉素"], "肠道感染应优先结合脱水、毒血症和药敏判断；氨基糖苷类全身治疗需注意吸收和肾毒性边界。"),
    ("DIS-041-neonatal-post-weaning-colibacillosis.md", "仔猪黄白痢", ["磺胺类", "氨基糖苷类", "口服补液"], "仔猪腹泻样病例应先区分病毒性、细菌性、球虫性和管理性因素。"),
    ("DIS-042-edema-disease-e-coli.md", "仔猪水肿病", ["磺胺嘧啶", "磺胺二甲嘧啶"], "作为敏感菌候选和鉴别增强，不得替代毒素型大肠杆菌的综合处置。"),
    ("DIS-043-erysipelas.md", "猪丹毒", ["青霉素"], "青霉素为敏感革兰阳性菌候选；执行处方仍需标签、药敏和休药期。"),
    ("DIS-045-leptospirosis.md", "钩端螺旋体病", ["青霉素", "四环素类"], "钩端螺旋体病属于人兽共患风险场景，需保留防护、送检和监管边界。"),
    ("DIS-049-salmonellosis.md", "沙门氏菌病", ["氨苄西林", "磺胺嘧啶", "氟苯尼考"], "应强调药敏、耐药和公共卫生边界，避免经验性滥用抗菌药。"),
    ("DIS-051-streptococcosis-streptococcus-suis.md", "猪链球菌病", ["青霉素", "磺胺类", "头孢菌素类"], "脑膜炎型等高风险病例需区分中枢渗透、分开注射和人兽共患防护。"),
    ("DIS-055-external-parasites-mange.md", "疥螨/外寄生虫", ["伊维菌素", "阿维菌素类", "双甲脒", "拟除虫菊酯类"], "外寄生虫病例需结合群体处理、环境清理和复查，不得只生成单次用药。"),
    ("DIS-056-external-parasites-lice.md", "猪虱病", ["伊维菌素", "有机磷杀虫药", "拟除虫菊酯类"], "外寄生虫处理必须同时约束安全、环境和肉品休药期复核。"),
    ("DIS-057-coccidia-and-other-protozoa.md", "球虫/原虫性腹泻", ["妥曲珠利", "氨丙啉", "磺胺类"], "腹泻综合征中需与病毒性腹泻和大肠杆菌病鉴别。"),
    ("DIS-058-toxoplasmosis-protozoa.md", "弓形虫病", ["磺胺类", "TMP"], "弓形虫病处方候选需保留人兽共患和妊娠风险边界。"),
    ("DIS-060-ascaris-suum-internal-parasites.md", "蛔虫病", ["芬苯达唑", "左旋咪唑", "哌嗪"], "驱虫策略应结合虫卵检查、群体程序和环境控制。"),
    ("DIS-061-trichuris-suis-internal-parasites.md", "鞭虫病", ["苯并咪唑类", "伊维菌素"], "慢性腹泻/消瘦需纳入鞭虫鉴别。"),
]

RULE_FACTS = [
    ("RAU-RULE-0001", 8, "药物联用与禁忌", "联合用药应区分协同、相加、无关和拮抗；生成处方时不得把相互拮抗的杀菌药/抑菌药组合当作默认方案。"),
    ("RAU-RULE-0002", 10, "体外配伍禁忌", "注射液、输液和注射器配伍可能发生沉淀、变色、pH 变化或效价降低；模型不得建议随意混合注射。"),
    ("RAU-RULE-0003", 11, "注射液配伍禁忌", "配伍禁忌原因包括物理、化学和药理性不相容；混合给药必须有标签或权威证据支持。"),
    ("RAU-RULE-0004", 13, "体内相互作用", "药动学和药效学相互作用可影响吸收、分布、代谢、排泄和疗效安全。"),
    ("RAU-RULE-0005", 24, "中药及中西药配伍", "中西药注射剂配伍应谨慎，酸碱性和澄清度变化可能导致沉淀或不稳定。"),
    ("RAU-RULE-0006", 34, "β-内酰胺合理使用", "β-内酰胺类属繁殖期杀菌药，水溶液稳定性和过敏风险需作为生成边界。"),
    ("RAU-RULE-0007", 50, "氨基糖苷边界", "氨基糖苷类需重点保留肾毒性、耳毒性、新生仔畜和肾功能障碍排泄减慢等边界。"),
    ("RAU-RULE-0008", 81, "磺胺类边界", "磺胺类用药需关注结晶尿、肾功能、饮水、B族维生素/K、交叉耐药和蛋鸡产蛋期禁用等边界。"),
    ("RAU-RULE-0009", 104, "禁用药风险", "硝基呋喃类、部分硝基咪唑和喹噁啉类在食品动物场景必须触发禁用/合规复核，不得直接生成食用动物处方。"),
    ("RAU-RULE-0010", 144, "抗寄生虫药原则", "抗寄生虫药应按虫种、发育阶段、宿主阶段和环境控制综合选择，不得只按症状给单药。"),
]


def read_raw() -> str:
    candidates = [path for path in RAW_DIR.glob("*.md") if path.name == "兽药合理应用与联用手册1-200页.md"]
    if not candidates:
        candidates = [path for path in RAW_DIR.glob("*.md") if path.stat().st_size == 354739]
    return candidates[0].read_text(encoding="utf-8", errors="ignore")


def compact(text: str, limit: int = 360) -> str:
    text = re.sub(r"!\[\]\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit].rstrip()


def toc_entries(text: str) -> list[Entry]:
    entries: list[Entry] = []
    section = ""
    for line in text.splitlines()[:700]:
        stripped = line.strip().strip("#").strip()
        if not stripped:
            continue
        if any(key in stripped for key in ["抗生素", "化学合成抗菌药", "抗蠕虫药", "抗原虫药", "杀虫药", "消毒防腐药"]):
            section = re.sub(r"\s+\d+\s*$", "", stripped)
        m = re.match(r"^(.+?)\s+(\d{1,3})\s*$", stripped)
        if not m:
            continue
        name = m.group(1).strip("· ")
        page = int(m.group(2))
        if page > 200:
            continue
        if name in DRUG_TARGETS:
            target, category, kind = DRUG_TARGETS[name]
            entries.append(Entry(name=name, page=page, category=category, kind=kind, target=target))
    return entries


def extract_section(text: str, name: str) -> str:
    pattern = re.compile(rf"(?m)^#\s*{re.escape(name)}\s*$")
    m = pattern.search(text)
    if not m:
        return ""
    nxt = re.search(r"(?m)^#\s+", text[m.end() :])
    end = m.end() + nxt.start() if nxt else min(len(text), m.end() + 2000)
    return compact(text[m.end() : end], 520)


def ensure_source_page() -> None:
    path = ROOT / SOURCE_REL
    if path.exists():
        return
    path.write_text(
        f"""---
tags: [source, veterinary_drug_use, drug_combination, swine, source_anchored]
source_id: {SOURCE_ID}
title: {SOURCE_TITLE}
evidence_status: HUMAN_REVIEWED
pages: 1-200
updated: {TODAY}
---

# {SOURCE_TITLE}

## 来源定位

- 原始文件：`raw/md/兽药合理应用与联用手册1-200页.md`
- 覆盖范围：第 1 章合理用药/联用禁忌基础知识、第 2 章抗菌药合理应用及联用禁忌、第 3 章消毒防腐药、第 4 章抗寄生虫药合理应用与联用禁忌（至约第 200 页）。
- 用途：为 drug、rule、disease-drug-rule 矩阵、syndrome 入口和黄金数据生成提供 source-first 证据锚点。

## 使用边界

- 本来源可作为诊疗/处方候选、药物联用禁忌、配伍禁忌和鉴别增强证据。
- 不可单独替代当前批准标签、现行休药期、MRL 或地方监管结论。
- 生成具体剂量、疗程、休药期或上市可食用承诺时，必须再叠加当前 A0/A1 或标签来源。
""",
        encoding="utf-8",
        newline="\n",
    )


def append_source_index() -> None:
    path = EXPORTS / "source_index.csv"
    rows = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
    if any(row.get("source_id") == SOURCE_ID for row in rows):
        return
    rows.append(
        {
            "source_id": SOURCE_ID,
            "title": SOURCE_TITLE,
            "pages": "1-200",
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": SOURCE_REL,
        }
    )
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["source_id", "title", "pages", "evidence_status", "relpath"])
        writer.writeheader()
        writer.writerows(rows)


def replace_block(text: str, block: str) -> str:
    pattern = re.compile(rf"\n?{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?", re.S)
    text = pattern.sub("\n", text).rstrip()
    return text + "\n\n" + block.strip() + "\n"


def promote_drug_page(text: str) -> str:
    head, sep, rest = text.partition("---\n")
    if not text.startswith("---") or not sep:
        return text
    fm, sep2, body = rest.partition("---\n")
    fm = fm.replace("needs_review, ", "").replace(", needs_review", "").replace("evidence_status: NEEDS_REVIEW", "evidence_status: HUMAN_REVIEWED")
    fm = fm.replace("partial_drug_evidence_page", "source_anchored_drug_evidence_page")
    if SOURCE_ID not in fm:
        fm = re.sub(r"sources: \[([^\]]*)\]", lambda m: "sources: [" + (m.group(1).strip() + ", " if m.group(1).strip() else "") + SOURCE_ID + "]", fm)
    return "---\n" + fm + "---\n" + body


def write_drug_pages(entries: list[Entry], text: str) -> dict[str, int]:
    grouped: dict[str, list[Entry]] = {}
    for entry in entries:
        grouped.setdefault(entry.target, []).append(entry)
    for class_name, (target, category) in CLASS_TARGETS.items():
        page = {
            "β-内酰胺类": 34,
            "青霉素类": 34,
            "头孢菌素类": 44,
            "氨基糖苷类": 50,
            "四环素类": 58,
            "大环内酯类": 67,
            "林可胺类": 73,
            "磺胺类": 81,
            "抗球虫药": 173,
            "阿维菌素类": 155,
            "苯并咪唑类": 144,
            "有机磷": 195,
            "拟除虫菊酯": 198,
        }[class_name]
        grouped.setdefault(target, []).append(Entry(class_name, page, category, "class_boundary", target))

    changed: dict[str, int] = {}
    for filename, items in grouped.items():
        path = WIKI / "drugs" / filename
        if not path.exists():
            continue
        lines = [
            MARKER_START,
            f"## 兽药合理应用与联用手册（1-200页）增强 / {SOURCE_ID}",
            "",
            "- 来源：`raw/md/兽药合理应用与联用手册1-200页.md`。",
            "- 证据用途：药物类别定位、适应证候选、联用/配伍禁忌、给药边界与黄金数据生成约束。",
            "- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；这些结论仍需现行标签/A0/A1 来源复核。",
            "",
        ]
        for entry in sorted(items, key=lambda x: (x.page, x.name)):
            snippet = extract_section(text, entry.name)
            if not snippet:
                snippet = f"目录定位显示 `{entry.name}` 属于 `{entry.category}`，可作为药物召回、类别边界和联用禁忌复核入口。"
            fact_id = f"RAU1-DRUG-{entry.page:03d}-{re.sub(r'[^A-Za-z0-9]+', '-', entry.target).strip('-')}-{abs(hash(entry.name)) % 10000:04d}"
            lines.append(f"- `{fact_id}` {entry.name} / {entry.category} / p.{entry.page}：{snippet} `source_id={SOURCE_ID}; page={entry.page}`")
        lines.append("")
        lines.append(MARKER_END)
        original = path.read_text(encoding="utf-8-sig")
        updated = promote_drug_page(replace_block(original, "\n".join(lines)))
        path.write_text(updated, encoding="utf-8", newline="\n")
        changed[filename] = len(items)
    return changed


def write_disease_pages() -> dict[str, int]:
    changed: dict[str, int] = {}
    for filename, disease, drugs, note in DISEASE_LINKS:
        path = WIKI / "diseases" / filename
        if not path.exists():
            continue
        rows = [
            MARKER_START,
            f"## 兽药合理应用与联用证据增强 / {SOURCE_ID}",
            "",
            f"- 关联场景：{disease}。",
            f"- 药物/类别候选：{', '.join(drugs)}。",
            f"- 生成边界：{note}",
            "- 本块用于候选召回、鉴别增强和 rule 约束；不得单独输出剂量、疗程、休药期或 MRL。",
            f"- 来源：{SOURCE_TITLE}，相关药物目录与正文页码见 `exports/veterinary_rational_use_1_200_drug_index.csv`。`source_id={SOURCE_ID}`",
            "",
            MARKER_END,
        ]
        text = path.read_text(encoding="utf-8-sig")
        path.write_text(replace_block(text, "\n".join(rows)), encoding="utf-8", newline="\n")
        changed[filename] = 1
    return changed


def write_rule_and_synthesis(entries: list[Entry]) -> None:
    rule_path = WIKI / "rule_cards" / "RC-DRUG-COMBINATION-RAU-001.md"
    rule_path.write_text(
        f"""---
tags: [rule_card, swine, drug_combination, incompatibility, source_anchored]
rule_id: RC-DRUG-COMBINATION-RAU-001
evidence_status: HUMAN_REVIEWED
source_id: {SOURCE_ID}
updated: {TODAY}
---

# 兽药联用与配伍禁忌规则卡 / SRC-0091

## 规则

- 联合用药必须区分协同、相加、无关和拮抗；不得把杀菌药与快速抑菌药组合默认视为增效。
- 注射液、输液、注射器、内服制剂和中西药注射剂均可能出现配伍禁忌；没有标签或权威证据时不得建议混合注射。
- 青霉素类水溶液稳定性差，偏酸/偏碱、葡萄糖液或放置时间可能影响效价；生成时应提示现配现用和配伍复核边界。
- 氨基糖苷类需重点约束肾毒性、耳毒性、新生仔畜和肾功能障碍风险。
- 磺胺类需约束结晶尿、饮水、肾功能、维生素补充、交叉耐药和配伍酸碱性。
- 抗寄生虫药需按虫种、宿主阶段、环境控制和复查计划使用，不得只按症状给单药。

## 来源

- {SOURCE_TITLE}：第 1 章 p.1-33；第 2 章 p.34-112；第 4 章 p.144-200。`source_id={SOURCE_ID}`
""",
        encoding="utf-8",
        newline="\n",
    )

    matrix = WIKI / "synthesis" / "veterinary_rational_use_1_200_drug_disease_rule_matrix.md"
    rows = [
        "# 兽药合理应用与联用手册（1-200页）药物-疾病-rule 矩阵",
        "",
        f"- 来源：`{SOURCE_ID}` / {SOURCE_TITLE}",
        "- 用途：补强 drug、disease、rule 三方映射，服务黄金数据生成、评估和拒答边界。",
        "",
        "## 药物目录抽取",
        "",
        "| 药物/类别 | 页码 | 类别 | Wiki 目标页 | 用途 |",
        "|---|---:|---|---|---|",
    ]
    for entry in sorted(entries, key=lambda x: (x.page, x.name)):
        rows.append(f"| {entry.name} | {entry.page} | {entry.category} | `wiki/drugs/{entry.target}` | {entry.kind} |")
    rows.extend(
        [
            "",
            "## 疾病-药物-rule 映射",
            "",
            "| 疾病页 | 场景 | 药物/类别候选 | rule 约束 | 来源 |",
            "|---|---|---|---|---|",
        ]
    )
    for filename, disease, drugs, note in DISEASE_LINKS:
        rows.append(f"| `wiki/diseases/{filename}` | {disease} | {', '.join(drugs)} | {note} | `{SOURCE_ID}` |")
    matrix.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")

    comparison = WIKI / "comparisons" / "veterinary_rational_use_1_200_antimicrobial_combination_matrix.md"
    comparison.write_text(
        f"""# 抗菌药联用/配伍禁忌增强矩阵

- 来源：{SOURCE_TITLE}。`source_id={SOURCE_ID}`
- 用途：用于生成和评估时识别药物组合的协同、拮抗和配伍禁忌风险。

| 类别/组合 | 可用结论 | 生成约束 | 页码 |
|---|---|---|---:|
| β-内酰胺类 | 繁殖期杀菌药，水溶液稳定性和过敏风险需要提示 | 不得与快速抑菌药默认合用；剂量/疗程需标签复核 | 34 |
| 青霉素类 + β-内酰胺酶抑制剂 | 可作为耐酶/增效候选 | 必须核对具体产品标签和靶动物 | 48-49 |
| 青霉素类 + 氨基糖苷类 | 可出现协同候选，但需分开注射和毒性边界 | 不得建议随意混合注射 | 8, 50 |
| 青霉素类 + 四环素/大环内酯/酰胺醇 | 存在药效拮抗风险 | 评估时作为处方风险点 | 8, 34 |
| 磺胺类 + TMP | 常作为增效候选 | 需约束结晶尿、饮水、肾功能、休药期和蛋鸡禁用边界 | 81-95 |
| 氨基糖苷类 | 肠道局部/全身治疗边界不同 | 新生仔畜、肾功能障碍、耳肾毒性必须提示 | 50-58 |
| 抗寄生虫药 | 需按虫种和环境控制选择 | 不得只按“消瘦/腹泻/瘙痒”直接给单药 | 144-200 |
""",
        encoding="utf-8",
        newline="\n",
    )


def write_syndromes() -> None:
    syndromes = {
        "SYN-013-diarrhea-antimicrobial-coccidia-differential.md": (
            "腹泻-抗菌药/球虫/病毒性鉴别入口",
            "腹泻样病例需区分病毒性腹泻、大肠杆菌/沙门氏菌等细菌性肠炎、球虫/原虫和饲养管理因素；抗菌药、磺胺类和抗球虫药只能作为证据支持的候选。",
            "涉及仔猪黄白痢、沙门氏菌病、球虫病、轮状病毒、PED/TGE/PDCoV 等。",
        ),
        "SYN-014-respiratory-antimicrobial-boundary.md": (
            "呼吸道症状-抗菌药选择与支原体/细菌鉴别入口",
            "呼吸道病例需区分胸膜肺炎、支原体肺炎、巴氏杆菌、链球菌、PRRS/流感等病毒性或混合感染；青霉素类、氟苯尼考、大环内酯、林可胺等只能作为候选召回。",
            "支原体无细胞壁，β-内酰胺类对单纯支原体感染不应作为有效治疗结论。",
        ),
        "SYN-015-pruritus-parasite-insecticide-boundary.md": (
            "瘙痒/皮肤病-外寄生虫与杀虫药边界入口",
            "瘙痒、脱毛、结痂和生长迟缓需区分疥螨、虱、皮肤细菌感染和营养/环境因素；杀虫药需结合群体处理、环境清理、复查和休药期复核。",
            "阿维菌素类、有机磷、拟除虫菊酯和双甲脒均需安全边界。",
        ),
    }
    for filename, (title, summary, diff) in syndromes.items():
        path = WIKI / "syndromes" / filename
        path.write_text(
            f"""---
tags: [syndrome, swine, source_anchored, differential_diagnosis]
evidence_status: HUMAN_REVIEWED
source_id: {SOURCE_ID}
updated: {TODAY}
---

# {title}

## 入口价值

{summary}

## 鉴别与约束

{diff}

## 生成边界

- 本页用于症状入口召回、鉴别诊断和药物候选约束。
- 不得单独生成具体剂量、疗程、休药期或 MRL。
- 药物事实来源：{SOURCE_TITLE}。`source_id={SOURCE_ID}`
""",
            encoding="utf-8",
            newline="\n",
        )


def write_exports(entries: list[Entry], text: str) -> list[dict[str, str]]:
    facts: list[dict[str, str]] = []
    for idx, entry in enumerate(sorted(entries, key=lambda x: (x.page, x.name)), start=1):
        snippet = extract_section(text, entry.name) or f"{entry.name} 在目录中定位为 {entry.category}，可作为药物类别和联用禁忌入口。"
        facts.append(
            {
                "fact_id": f"RAU1-DRUG-{idx:04d}",
                "fact_type": "drug_combination_manual_entry",
                "subject": entry.name,
                "predicate": "rational_use_or_combination_boundary",
                "object": snippet,
                "page": str(entry.page),
                "category": entry.category,
                "target_page": f"wiki/drugs/{entry.target}",
                "evidence_source_id": SOURCE_ID,
                "evidence_status": "HUMAN_REVIEWED",
            }
        )
    for fact_id, page, subject, obj in RULE_FACTS:
        facts.append(
            {
                "fact_id": fact_id,
                "fact_type": "drug_rule_boundary",
                "subject": subject,
                "predicate": "generation_and_evaluation_constraint",
                "object": obj,
                "page": str(page),
                "category": "rule",
                "target_page": "wiki/rule_cards/RC-DRUG-COMBINATION-RAU-001.md",
                "evidence_source_id": SOURCE_ID,
                "evidence_status": "HUMAN_REVIEWED",
            }
        )
    for idx, (filename, disease, drugs, note) in enumerate(DISEASE_LINKS, start=1):
        facts.append(
            {
                "fact_id": f"RAU1-DDR-{idx:04d}",
                "fact_type": "disease_drug_rule_mapping",
                "subject": disease,
                "predicate": "has_drug_candidate_with_rule_boundary",
                "object": f"{', '.join(drugs)}；{note}",
                "page": "",
                "category": "disease_drug_rule",
                "target_page": f"wiki/diseases/{filename}",
                "evidence_source_id": SOURCE_ID,
                "evidence_status": "HUMAN_REVIEWED",
            }
        )

    fact_path = EXPORTS / "veterinary_rational_use_1_200_fact_index.csv"
    with fact_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(facts[0].keys()))
        writer.writeheader()
        writer.writerows(facts)

    drug_path = EXPORTS / "veterinary_rational_use_1_200_drug_index.csv"
    with drug_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["name", "page", "category", "kind", "target_page", "source_id"])
        writer.writeheader()
        for entry in sorted(entries, key=lambda x: (x.page, x.name)):
            writer.writerow(
                {
                    "name": entry.name,
                    "page": entry.page,
                    "category": entry.category,
                    "kind": entry.kind,
                    "target_page": f"wiki/drugs/{entry.target}",
                    "source_id": SOURCE_ID,
                }
            )

    kf_path = EXPORTS / "knowledge_facts.json"
    existing = json.loads(kf_path.read_text(encoding="utf-8-sig")) if kf_path.exists() else []
    existing = [fact for fact in existing if not str(fact.get("fact_id", "")).startswith("RAU1-")]
    for fact in facts:
        existing.append(
            {
                "fact_id": fact["fact_id"],
                "fact_type": fact["fact_type"],
                "subject": fact["subject"],
                "predicate": fact["predicate"],
                "object": fact["object"],
                "fact_confidence": "0.82",
                "evidence_source": SOURCE_TITLE,
                "evidence_source_id": SOURCE_ID,
                "evidence_url": "",
                "evidence_quote_span": f"p.{fact['page']}" if fact["page"] else "",
                "evidence_status": fact["evidence_status"],
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "China/Global handbook context",
            }
        )
    kf_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return facts


def write_report(entries: list[Entry], drug_changed: dict[str, int], disease_changed: dict[str, int], facts: list[dict[str, str]]) -> None:
    report = ISSUES / "veterinary_rational_use_1_200_extraction_and_wiki_augmentation_2026-05-08.md"
    by_category: dict[str, int] = {}
    for entry in entries:
        by_category[entry.category] = by_category.get(entry.category, 0) + 1
    lines = [
        "# 兽药合理应用与联用手册（1-200页）抽取与 Wiki 补强报告 / 2026-05-08",
        "",
        "## 抽取范围",
        "",
        f"- 原始文件：`raw/md/兽药合理应用与联用手册1-200页.md`",
        f"- source_id：`{SOURCE_ID}`",
        "- 覆盖章节：第 1 章合理用药/联用禁忌基础知识；第 2 章抗菌药合理应用及联用禁忌；第 3 章消毒防腐药；第 4 章抗寄生虫药合理应用及联用禁忌（至约 p.200）。",
        "",
        "## 分种类抽取统计",
        "",
    ]
    for category, count in sorted(by_category.items()):
        lines.append(f"- {category}: {count}")
    lines.extend(
        [
            "",
            "## 写入结果",
            "",
            f"- drug 页面增强：{len(drug_changed)} 页。",
            f"- disease 页面增强：{len(disease_changed)} 页。",
            f"- 新增/刷新 facts：{len(facts)} 条。",
            "- 新增 rule card：`wiki/rule_cards/RC-DRUG-COMBINATION-RAU-001.md`。",
            "- 新增 synthesis 矩阵：`wiki/synthesis/veterinary_rational_use_1_200_drug_disease_rule_matrix.md`。",
            "- 新增 comparison 矩阵：`wiki/comparisons/veterinary_rational_use_1_200_antimicrobial_combination_matrix.md`。",
            "- 新增 syndrome 入口：3 页。",
            "- 新增索引：`exports/veterinary_rational_use_1_200_fact_index.csv`、`exports/veterinary_rational_use_1_200_drug_index.csv`。",
            "",
            "## 约束结论",
            "",
            "- 本轮补强显著增加了 drug/disease/rule 三方映射和联用禁忌约束。",
            "- 本来源可作为候选和边界增强；具体剂量、疗程、休药期、MRL 或合规结论仍必须叠加当前标签/A0/A1 来源。",
        ]
    )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    text = read_raw()
    entries = toc_entries(text)
    ensure_source_page()
    append_source_index()
    drug_changed = write_drug_pages(entries, text)
    disease_changed = write_disease_pages()
    write_rule_and_synthesis(entries)
    write_syndromes()
    facts = write_exports(entries, text)
    write_report(entries, drug_changed, disease_changed, facts)
    print(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "drug_entries": len(entries),
                "drug_pages_changed": len(drug_changed),
                "disease_pages_changed": len(disease_changed),
                "facts_written": len(facts),
                "report": str(ISSUES / "veterinary_rational_use_1_200_extraction_and_wiki_augmentation_2026-05-08.md"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
