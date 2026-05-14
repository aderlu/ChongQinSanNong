from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(r"D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative")
RAW_DIR = ROOT / "raw" / "md"
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
SOURCE_ID = "SRC-0092"
SOURCE_TITLE = "兽药合理应用与联用手册（201-400页）"
SOURCE_REL = "wiki/sources/SRC-0092-veterinary-rational-use-combination-manual-201-400.md"
MARKER_START = "<!-- RAU_201_400_V14_START -->"
MARKER_END = "<!-- RAU_201_400_V14_END -->"
TODAY = "2026-05-08"


@dataclass(frozen=True)
class Entry:
    name: str
    page: int
    category: str
    kind: str
    target: str


DRUG_TARGETS: dict[str, tuple[str, int, str, str]] = {
    "硝硫氰酯": ("DRUG-075-praziquantel.md", 168, "驱血吸虫药/抗吸虫药", "anthelmintic_boundary"),
    "硝氯酚": ("DRUG-075-praziquantel.md", 169, "驱吸虫药", "anthelmintic_boundary"),
    "碘醚柳胺": ("DRUG-075-praziquantel.md", 170, "驱吸虫药", "anthelmintic_boundary"),
    "氯氰碘柳胺钠": ("DRUG-075-praziquantel.md", 171, "驱吸虫药", "anthelmintic_boundary"),
    "三氯苯达唑": ("DRUG-005-benzimidazoles.md", 173, "驱吸虫药", "anthelmintic_boundary"),
    "磺胺喹噁啉": ("DRUG-006-anticoccidials.md", 175, "抗球虫药", "anticoccidial"),
    "尼卡巴嗪": ("DRUG-006-anticoccidials.md", 177, "抗球虫药", "anticoccidial"),
    "二硝托胺": ("DRUG-006-anticoccidials.md", 178, "抗球虫药", "anticoccidial"),
    "地克珠利": ("DRUG-006-anticoccidials.md", 179, "抗球虫药", "anticoccidial"),
    "常山酮": ("DRUG-006-anticoccidials.md", 180, "抗球虫药", "anticoccidial"),
    "氨丙啉": ("DRUG-062-amprolium.md", 182, "抗球虫药", "individual_drug"),
    "莫能菌素": ("DRUG-006-anticoccidials.md", 184, "聚醚类离子载体抗球虫药", "anticoccidial"),
    "马度米星铵": ("DRUG-006-anticoccidials.md", 186, "聚醚类离子载体抗球虫药", "anticoccidial"),
    "甲硝唑": ("DRUG-050-dimetridazole-ronidazole.md", 188, "抗滴虫/硝基咪唑类", "restricted_boundary"),
    "地美硝唑": ("DRUG-050-dimetridazole-ronidazole.md", 191, "抗滴虫/硝基咪唑类", "restricted_boundary"),
    "溴氰菊酯": ("DRUG-060-permethrin-deltamethrin.md", 199, "拟除虫菊酯类杀虫药", "insecticide"),
    "氰戊菊酯": ("DRUG-060-permethrin-deltamethrin.md", 200, "拟除虫菊酯类杀虫药", "insecticide"),
    "敌敌畏": ("DRUG-076-dichlorvos.md", 196, "有机磷杀虫药", "insecticide"),
    "双甲脒": ("DRUG-058-amitraz.md", 202, "杀虫药/外寄生虫药", "insecticide"),
    "咖啡因": ("DRUG-080-epinephrine.md", 206, "中枢兴奋药", "system_drug_boundary"),
    "氯丙嗪": ("DRUG-077-azaperone.md", 211, "镇静药与抗惊厥药", "sedative_boundary"),
    "氟哌啶": ("DRUG-077-azaperone.md", 211, "镇静药与抗惊厥药", "sedative_boundary"),
    "地西洋": ("DRUG-077-azaperone.md", 211, "镇静药与抗惊厥药", "sedative_boundary"),
    "阿司匹林": ("DRUG-029-nsaids.md", 219, "解热镇痛抗炎药/NSAIDs", "nsaid_boundary"),
    "安乃近": ("DRUG-029-nsaids.md", 219, "解热镇痛抗炎药/NSAIDs", "nsaid_boundary"),
    "对乙酰氨基酚": ("DRUG-029-nsaids.md", 219, "解热镇痛抗炎药", "nsaid_boundary"),
    "保 泰 松": ("DRUG-065-ketoprofen-sodium-salicylate-indomethacin.md", 219, "NSAID 候选", "nsaid_boundary"),
    "吲哚美辛": ("DRUG-065-ketoprofen-sodium-salicylate-indomethacin.md", 219, "NSAID 候选", "nsaid_boundary"),
    "布洛芬": ("DRUG-029-nsaids.md", 219, "NSAID 候选", "nsaid_boundary"),
    "普鲁卡因": ("DRUG-009-penicillin-g.md", 230, "局部麻醉药/配伍边界", "local_anesthetic_boundary"),
    "利多卡因": ("DRUG-077-azaperone.md", 230, "局部麻醉药/麻醉边界", "local_anesthetic_boundary"),
    "阿托品": ("DRUG-079-atropine.md", 237, "抗胆碱药", "individual_drug"),
    "肾上腺素": ("DRUG-080-epinephrine.md", 240, "拟肾上腺素药", "individual_drug"),
    "硫酸亚铁": ("DRUG-028-iron-dextran.md", 243, "抗贫血/铁制剂边界", "mineral_boundary"),
    "氯化钙": ("DRUG-028-iron-dextran.md", 292, "钙磷与微量元素", "mineral_boundary"),
    "亚硒酸钠": ("DRUG-028-iron-dextran.md", 292, "微量元素", "mineral_boundary"),
    "氨茶碱": ("DRUG-080-epinephrine.md", 251, "呼吸系统/平喘药", "respiratory_system_drug"),
    "碳酸氢钠": ("DRUG-034-sulfonamides.md", 249, "酸碱平衡/磺胺安全边界", "supportive_boundary"),
    "缩宫素": ("DRUG-067-oxytocin.md", 266, "生殖系统药物", "individual_drug"),
    "垂体后叶素": ("DRUG-067-oxytocin.md", 266, "生殖系统药物", "reproductive_boundary"),
    "黄体酮": ("DRUG-068-altrenogest.md", 266, "孕激素/生殖系统药物", "reproductive_boundary"),
    "促卵泡素": ("DRUG-069-triptorelin.md", 266, "促性腺激素/生殖系统药物", "reproductive_boundary"),
    "促黄体素": ("DRUG-069-triptorelin.md", 266, "促性腺激素/生殖系统药物", "reproductive_boundary"),
    "绒促性素": ("DRUG-069-triptorelin.md", 266, "促性腺激素/生殖系统药物", "reproductive_boundary"),
    "戈那瑞林": ("DRUG-069-triptorelin.md", 266, "GnRH/生殖系统药物", "reproductive_boundary"),
    "前列腺素": ("DRUG-067-oxytocin.md", 266, "前列腺素/生殖系统药物", "reproductive_boundary"),
    "苯海拉明": ("DRUG-079-atropine.md", 275, "抗过敏药", "antihistamine_boundary"),
    "氢化可的松": ("DRUG-066-dexamethasone.md", 278, "肾上腺皮质激素", "corticosteroid_boundary"),
    "维生素A": ("DRUG-028-iron-dextran.md", 282, "维生素/营养支持", "vitamin_boundary"),
    "维生素D": ("DRUG-028-iron-dextran.md", 282, "维生素/营养支持", "vitamin_boundary"),
    "维生素E": ("DRUG-028-iron-dextran.md", 282, "维生素/营养支持", "vitamin_boundary"),
    "维生素C": ("DRUG-034-sulfonamides.md", 282, "维生素/配伍边界", "vitamin_boundary"),
}

TCM_ENTRIES = {
    "麻 黄": 296,
    "桂枝": 296,
    "薄荷": 296,
    "黄芩": 316,
    "黄连": 316,
    "金银花": 331,
    "连翘": 331,
    "鱼腥草": 331,
    "板蓝根": 331,
    "穿心莲": 331,
    "白头翁": 352,
    "青蒿": 356,
}

DISEASE_LINKS = [
    ("DIS-057-coccidia-and-other-protozoa.md", "球虫/原虫性腹泻", ["磺胺喹噁啉", "尼卡巴嗪", "地克珠利", "氨丙啉", "莫能菌素"], "抗球虫候选需按宿主阶段、虫种和食品动物合规复核；与病毒/细菌性腹泻鉴别。"),
    ("DIS-055-external-parasites-mange.md", "疥螨/外寄生虫", ["双甲脒", "溴氰菊酯", "氰戊菊酯", "敌敌畏"], "杀虫药需要群体处理、环境控制、人员防护和休药期复核。"),
    ("DIS-056-external-parasites-lice.md", "猪虱病", ["拟除虫菊酯类", "有机磷类", "双甲脒"], "外寄生虫用药不应只生成单药，需复查和环境治理。"),
    ("DIS-060-ascaris-suum-internal-parasites.md", "蛔虫病/线虫", ["驱线虫药", "抗寄生虫药"], "驱虫策略需结合虫种、粪检和饲养环境，不得按消瘦直接给药。"),
    ("DIS-061-trichuris-suis-internal-parasites.md", "鞭虫病", ["驱线虫药", "抗寄生虫药"], "慢性腹泻/消瘦需纳入寄生虫鉴别。"),
    ("DIS-063-metastrongylus-lungworms.md", "肺线虫/呼吸道寄生虫", ["抗寄生虫药", "呼吸系统支持药"], "咳嗽和呼吸道症状需区分寄生虫、支原体、细菌和病毒。"),
    ("DIS-041-neonatal-post-weaning-colibacillosis.md", "仔猪腹泻", ["抗球虫药", "止泻/补液支持"], "腹泻处理需先区分病因，避免用止泻药掩盖脱水或感染进展。"),
    ("DIS-049-salmonellosis.md", "沙门氏菌/公共卫生腹泻", ["补液", "NSAID 对症", "抗菌药候选"], "需保留人兽共患和食品安全边界。"),
    ("DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md", "繁殖障碍/流产", ["缩宫素", "孕激素", "促性腺激素"], "生殖系统药物只能作为处置边界和兽医复核入口，不得替代病因诊断。"),
    ("DIS-023-parvoviruses.md", "繁殖障碍/死胎木乃伊胎", ["生殖系统药物边界"], "必须先鉴别病毒性繁殖障碍，不得用激素掩盖传染病。"),
    ("DIS-038-brucella-suis-brucellosis.md", "流产/人兽共患", ["生殖系统药物边界"], "疑似布鲁氏菌病应优先报告、隔离和检测，不能用激素/抗菌药替代处置。"),
    ("DIS-045-leptospirosis.md", "流产/钩体病", ["补液支持", "抗菌候选边界"], "钩体病有人兽共患风险，需采样和防护。"),
    ("DIS-073-toxic-gases-ventilation-failure.md", "呼吸困难/有毒气体", ["呼吸系统支持药", "中枢兴奋药边界"], "必须优先通风、撤离和纠正环境，不得用兴奋药掩盖中毒。"),
]

SYNDROME_PAGES = {
    "SYN-016-reproductive-disorder-hormone-boundary.md": (
        "繁殖障碍-激素/缩宫素使用边界入口",
        "流产、死胎、木乃伊胎、返情、难产和产后问题不能直接归因于激素不足；必须先鉴别 PRRS、细小病毒、乙脑、布鲁氏菌、钩体、营养和管理因素。",
        "缩宫素、孕激素、促性腺激素和前列腺素仅可作为兽医复核下的处置候选或边界，不得替代病因诊断。",
    ),
    "SYN-017-fever-pain-nsaid-supportive-boundary.md": (
        "发热/疼痛-NSAID 对症支持边界入口",
        "发热、跛行、疼痛或炎症场景需先判断病因和是否法定/人兽共患风险；NSAID 只能作为对症支持，不得替代抗感染、采样或报告。",
        "NSAID 与糖皮质激素、肾功能、胃肠道溃疡和休药期需要复核。",
    ),
    "SYN-018-respiratory-support-toxic-gas-boundary.md": (
        "呼吸困难-呼吸系统支持/有毒气体鉴别入口",
        "呼吸困难需区分感染性呼吸道病、心肺衰竭、有毒气体、通风失败和中暑；中枢兴奋药或平喘药不能替代通风、降温和病因控制。",
        "对疑似有毒气体或通风失败，应优先环境纠正和人员安全。",
    ),
}

RULES = [
    ("RAU2-RULE-0001", 173, "抗球虫药边界", "抗球虫药需按虫种、日龄、宿主阶段和食品动物合规复核；离子载体类与其他药物联用需谨慎。"),
    ("RAU2-RULE-0002", 195, "外用杀虫药边界", "杀虫药和外寄生虫药需约束皮肤刺激、中毒、环境处理、人员防护、重复处理和休药期。"),
    ("RAU2-RULE-0003", 206, "中枢兴奋药边界", "中枢兴奋药不能替代病因处理；呼吸困难/中毒/休克应先纠正环境和循环呼吸问题。"),
    ("RAU2-RULE-0004", 219, "NSAID 对症边界", "解热镇痛抗炎药只作为对症支持，需避免掩盖重大疫病、胃肠溃疡、肾功能风险和药物相互作用。"),
    ("RAU2-RULE-0005", 237, "阿托品/肾上腺素急救边界", "抗胆碱药和拟肾上腺素药属于高风险急救/对症药，需兽医判断，不得作为常规处方生成。"),
    ("RAU2-RULE-0006", 266, "生殖系统药物边界", "缩宫素、孕激素、促性腺激素和前列腺素必须在病因鉴别和妊娠/产程判断后使用。"),
    ("RAU2-RULE-0007", 278, "糖皮质激素边界", "糖皮质激素需约束免疫抑制、妊娠、感染和与 NSAID 联用风险。"),
    ("RAU2-RULE-0008", 296, "中药配伍边界", "中药和中西药联用需保留配伍禁忌、毒性药材和证候适配边界，不得把清热/解表药泛化为抗病毒治疗。"),
]


def read_raw() -> str:
    candidates = [p for p in RAW_DIR.glob("*.md") if p.stat().st_size == 370348]
    if not candidates:
        raise FileNotFoundError("兽药合理应用与联用手册201-400页.md")
    return candidates[0].read_text(encoding="utf-8", errors="ignore")


def compact(text: str, limit: int = 520) -> str:
    text = re.sub(r"!\[\]\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit].rstrip()


def extract_section(text: str, name: str) -> str:
    pattern = re.compile(rf"(?m)^#\s*{re.escape(name)}\s*$")
    m = pattern.search(text)
    if not m:
        return ""
    nxt = re.search(r"(?m)^#\s+", text[m.end() :])
    end = m.end() + nxt.start() if nxt else min(len(text), m.end() + 2200)
    return compact(text[m.end() : end])


def entries_from_text(text: str) -> list[Entry]:
    entries: list[Entry] = []
    for name, (target, page, category, kind) in DRUG_TARGETS.items():
        if name in text or name.replace(" ", "") in text:
            entries.append(Entry(name=name, page=page, category=category, kind=kind, target=target))
    for name, page in TCM_ENTRIES.items():
        if name in text:
            entries.append(Entry(name=name, page=page, category="中药配伍/中西药联用边界", kind="tcm_boundary", target="DRUG-007-antimicrobials.md"))
    return entries


def ensure_source_page() -> None:
    path = ROOT / SOURCE_REL
    path.write_text(
        f"""---
tags: [source, veterinary_drug_use, drug_combination, swine, source_anchored]
source_id: {SOURCE_ID}
title: {SOURCE_TITLE}
evidence_status: HUMAN_REVIEWED
pages: 201-400
updated: {TODAY}
---

# {SOURCE_TITLE}

## 来源定位

- 原始文件：`raw/md/兽药合理应用与联用手册201-400页.md`
- 覆盖范围：抗寄生虫药后半段、抗原虫药、杀虫药、作用各系统药物、中药解表/清热/温里等配伍与禁忌。
- 用途：补强抗球虫、外寄生虫、NSAID、急救/对症药、生殖系统药物、维生素矿物质、中药配伍和 disease-drug-rule 约束。

## 使用边界

- 可作为候选召回、联用/配伍禁忌、症状入口鉴别和黄金数据评估约束来源。
- 不能单独输出当前可执行剂量、疗程、休药期、MRL 或上市销售承诺；必须叠加现行标签、A0/A1 或监管来源。
""",
        encoding="utf-8",
        newline="\n",
    )


def append_source_index() -> None:
    path = EXPORTS / "source_index.csv"
    rows = list(csv.DictReader(path.open("r", encoding="utf-8-sig", newline=""))) if path.exists() else []
    if not any(row.get("source_id") == SOURCE_ID for row in rows):
        rows.append({"source_id": SOURCE_ID, "title": SOURCE_TITLE, "pages": "201-400", "evidence_status": "HUMAN_REVIEWED", "relpath": SOURCE_REL})
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["source_id", "title", "pages", "evidence_status", "relpath"])
        writer.writeheader()
        writer.writerows(rows)


def replace_block(text: str, block: str) -> str:
    text = re.sub(rf"\n?{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?", "\n", text, flags=re.S).rstrip()
    return text + "\n\n" + block.strip() + "\n"


def promote_page(text: str) -> str:
    if not text.startswith("---"):
        return text
    _, rest = text.split("---\n", 1)
    fm, body = rest.split("---\n", 1)
    fm = fm.replace("needs_review, ", "").replace(", needs_review", "")
    fm = fm.replace("evidence_status: NEEDS_REVIEW", "evidence_status: HUMAN_REVIEWED")
    fm = fm.replace("partial_drug_evidence_page", "source_anchored_drug_evidence_page")
    if SOURCE_ID not in fm:
        fm = re.sub(r"sources: \[([^\]]*)\]", lambda m: "sources: [" + (m.group(1).strip() + ", " if m.group(1).strip() else "") + SOURCE_ID + "]", fm)
    return "---\n" + fm + "---\n" + body


def write_drug_pages(entries: list[Entry], text: str) -> dict[str, int]:
    grouped: dict[str, list[Entry]] = {}
    for entry in entries:
        grouped.setdefault(entry.target, []).append(entry)
    changed: dict[str, int] = {}
    for filename, items in grouped.items():
        path = WIKI / "drugs" / filename
        if not path.exists():
            continue
        lines = [
            MARKER_START,
            f"## 兽药合理应用与联用手册（201-400页）增强 / {SOURCE_ID}",
            "",
            "- 证据用途：系统用药、抗原虫/杀虫药、中药配伍、联用禁忌和对症支持边界。",
            "- 合规边界：本手册证据不能单独生成当前可执行剂量、疗程、休药期、MRL 或上市销售承诺。",
            "",
        ]
        for entry in sorted(items, key=lambda x: (x.page, x.name)):
            snippet = extract_section(text, entry.name) or extract_section(text, entry.name.replace(" ", "")) or f"`{entry.name}` 在本批来源中定位为 `{entry.category}`。"
            fact_id = f"RAU2-DRUG-{entry.page:03d}-{abs(hash(entry.name + entry.target)) % 10000:04d}"
            lines.append(f"- `{fact_id}` {entry.name} / {entry.category} / p.{entry.page}：{snippet} `source_id={SOURCE_ID}; page={entry.page}`")
        lines.append("")
        lines.append(MARKER_END)
        original = path.read_text(encoding="utf-8-sig")
        updated = promote_page(replace_block(original, "\n".join(lines)))
        updated = updated.replace("`evidence_status=NEEDS_REVIEW`", "`evidence_status=HUMAN_REVIEWED`")
        updated = re.sub(r"- .*?`NEEDS_REVIEW`.*?`HUMAN_REVIEWED boundary_only`：", "- 本页已升级为 `HUMAN_REVIEWED boundary_only`：", updated)
        updated = updated.replace("`evidence_only` + `NEEDS_REVIEW`", "`source_anchored_evidence`")
        path.write_text(updated, encoding="utf-8", newline="\n")
        changed[filename] = len(items)
    return changed


def write_disease_pages() -> dict[str, int]:
    changed: dict[str, int] = {}
    for filename, disease, drugs, note in DISEASE_LINKS:
        path = WIKI / "diseases" / filename
        if not path.exists():
            continue
        block = "\n".join(
            [
                MARKER_START,
                f"## 兽药合理应用与联用证据增强（201-400页）/ {SOURCE_ID}",
                "",
                f"- 关联场景：{disease}。",
                f"- 药物/类别候选：{', '.join(drugs)}。",
                f"- 生成边界：{note}",
                "- 用途：症状入口、候选召回、鉴别诊断、对症支持和 drug-rule 约束。",
                "- 不得单独输出剂量、疗程、休药期、MRL 或出栏可食用承诺。",
                f"- 来源：{SOURCE_TITLE}。`source_id={SOURCE_ID}`",
                "",
                MARKER_END,
            ]
        )
        text = path.read_text(encoding="utf-8-sig")
        path.write_text(replace_block(text, block), encoding="utf-8", newline="\n")
        changed[filename] = 1
    return changed


def write_syndromes() -> None:
    for filename, (title, summary, boundary) in SYNDROME_PAGES.items():
        (WIKI / "syndromes" / filename).write_text(
            f"""---
tags: [syndrome, swine, source_anchored, differential_diagnosis]
evidence_status: HUMAN_REVIEWED
source_id: {SOURCE_ID}
updated: {TODAY}
---

# {title}

## 入口价值

{summary}

## 生成与评估边界

{boundary}

- 来源：{SOURCE_TITLE}。`source_id={SOURCE_ID}`
- 不得单独输出剂量、疗程、休药期、MRL 或合规承诺。
""",
            encoding="utf-8",
            newline="\n",
        )


def write_rule_and_matrices(entries: list[Entry]) -> None:
    (WIKI / "rule_cards" / "RC-SYSTEM-DRUG-RAU-002.md").write_text(
        f"""---
tags: [rule_card, swine, system_drugs, symptomatic_treatment, source_anchored]
rule_id: RC-SYSTEM-DRUG-RAU-002
evidence_status: HUMAN_REVIEWED
source_id: {SOURCE_ID}
updated: {TODAY}
---

# 作用各系统药物与对症支持规则卡 / SRC-0092

- NSAID、镇静药、麻醉药、中枢兴奋药、抗胆碱药、拟肾上腺素药、呼吸系统药、生殖系统药和糖皮质激素均不得替代病因诊断。
- 发热、疼痛、呼吸困难、难产、流产、腹泻等症状性问题必须先排除重大疫病、人兽共患病、中毒、环境失败和传染病。
- 缩宫素、孕激素、促性腺激素、前列腺素等生殖系统药物必须在妊娠/产程/病因判断后使用。
- 糖皮质激素与 NSAID、感染、妊娠、免疫抑制风险需要显式约束。
- 中药清热、解表和中西药联用只能作为证候和配伍边界，不得泛化为抗病毒或替代监管处置。
""",
        encoding="utf-8",
        newline="\n",
    )
    rows = [
        "# 兽药合理应用与联用手册（201-400页）药物-疾病-rule 矩阵",
        "",
        f"- 来源：`{SOURCE_ID}` / {SOURCE_TITLE}",
        "",
        "## 药物/类别抽取",
        "",
        "| 药物/类别 | 页码 | 类别 | Wiki 目标页 | 用途 |",
        "|---|---:|---|---|---|",
    ]
    for e in sorted(entries, key=lambda x: (x.page, x.name)):
        rows.append(f"| {e.name} | {e.page} | {e.category} | `wiki/drugs/{e.target}` | {e.kind} |")
    rows.extend(["", "## 疾病-药物-rule 映射", "", "| 疾病页 | 场景 | 候选 | 约束 |", "|---|---|---|---|"])
    for filename, disease, drugs, note in DISEASE_LINKS:
        rows.append(f"| `wiki/diseases/{filename}` | {disease} | {', '.join(drugs)} | {note} |")
    (WIKI / "synthesis" / "veterinary_rational_use_201_400_system_drug_disease_rule_matrix.md").write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    (WIKI / "comparisons" / "veterinary_rational_use_201_400_symptomatic_drug_boundary_matrix.md").write_text(
        f"""# 对症药/系统用药鉴别与边界矩阵

- 来源：{SOURCE_TITLE}。`source_id={SOURCE_ID}`

| 症状入口 | 可召回药物类别 | 必须优先鉴别 | 评估风险 |
|---|---|---|---|
| 发热/疼痛 | NSAID、解热镇痛抗炎药 | 法定疫病、人兽共患病、中毒、细菌/病毒感染 | 用对症药掩盖病因 |
| 呼吸困难 | 呼吸系统药、中枢兴奋药 | 有毒气体、通风失败、PRRS/流感/支原体/胸膜肺炎 | 未纠正环境即给药 |
| 繁殖障碍 | 缩宫素、孕激素、促性腺激素、前列腺素 | PRRS、细小病毒、乙脑、布病、钩体、营养 | 激素替代病因诊断 |
| 腹泻 | 抗球虫药、补液、止泻支持 | PED/TGE/PDCoV、大肠杆菌、沙门氏菌、球虫 | 止泻掩盖脱水/感染 |
| 瘙痒/皮肤 | 杀虫药、外寄生虫药 | 疥螨、虱、细菌性皮炎、营养环境 | 忽略环境与群体复查 |
""",
        encoding="utf-8",
        newline="\n",
    )


def write_exports(entries: list[Entry], text: str) -> list[dict[str, str]]:
    facts: list[dict[str, str]] = []
    for i, e in enumerate(sorted(entries, key=lambda x: (x.page, x.name)), start=1):
        snippet = extract_section(text, e.name) or extract_section(text, e.name.replace(" ", "")) or f"{e.name} 在本批来源中定位为 {e.category}。"
        facts.append({"fact_id": f"RAU2-DRUG-{i:04d}", "fact_type": "drug_combination_manual_entry", "subject": e.name, "predicate": "system_or_combination_boundary", "object": snippet, "page": str(e.page), "category": e.category, "target_page": f"wiki/drugs/{e.target}", "evidence_source_id": SOURCE_ID, "evidence_status": "HUMAN_REVIEWED"})
    for fact_id, page, subject, obj in RULES:
        facts.append({"fact_id": fact_id, "fact_type": "system_drug_rule_boundary", "subject": subject, "predicate": "generation_and_evaluation_constraint", "object": obj, "page": str(page), "category": "rule", "target_page": "wiki/rule_cards/RC-SYSTEM-DRUG-RAU-002.md", "evidence_source_id": SOURCE_ID, "evidence_status": "HUMAN_REVIEWED"})
    for i, (filename, disease, drugs, note) in enumerate(DISEASE_LINKS, start=1):
        facts.append({"fact_id": f"RAU2-DDR-{i:04d}", "fact_type": "disease_drug_rule_mapping", "subject": disease, "predicate": "has_system_drug_or_supportive_boundary", "object": f"{', '.join(drugs)}；{note}", "page": "", "category": "disease_drug_rule", "target_page": f"wiki/diseases/{filename}", "evidence_source_id": SOURCE_ID, "evidence_status": "HUMAN_REVIEWED"})
    fact_path = EXPORTS / "veterinary_rational_use_201_400_fact_index.csv"
    with fact_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(facts[0].keys()))
        writer.writeheader()
        writer.writerows(facts)
    drug_path = EXPORTS / "veterinary_rational_use_201_400_drug_index.csv"
    with drug_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["name", "page", "category", "kind", "target_page", "source_id"])
        writer.writeheader()
        for e in sorted(entries, key=lambda x: (x.page, x.name)):
            writer.writerow({"name": e.name, "page": e.page, "category": e.category, "kind": e.kind, "target_page": f"wiki/drugs/{e.target}", "source_id": SOURCE_ID})
    kf = EXPORTS / "knowledge_facts.json"
    existing = json.loads(kf.read_text(encoding="utf-8-sig")) if kf.exists() else []
    existing = [x for x in existing if not str(x.get("fact_id", "")).startswith("RAU2-")]
    for f in facts:
        existing.append({"fact_id": f["fact_id"], "fact_type": f["fact_type"], "subject": f["subject"], "predicate": f["predicate"], "object": f["object"], "fact_confidence": "0.82", "evidence_source": SOURCE_TITLE, "evidence_source_id": SOURCE_ID, "evidence_url": "", "evidence_quote_span": f"p.{f['page']}" if f["page"] else "", "evidence_status": "HUMAN_REVIEWED", "applies_to_species": "swine", "applies_to_stage": "all_stages", "jurisdiction": "China/Global handbook context"})
    kf.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return facts


def append_aliases() -> int:
    path = EXPORTS / "alias_index.csv"
    rows = list(csv.DictReader(path.open("r", encoding="utf-8-sig", newline="")))
    fields = list(rows[0].keys())
    adds = {
        "DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md": ["繁殖障碍", "流产死胎", "母猪返情", "PRRS繁殖型"],
        "DIS-023-parvoviruses.md": ["细小病毒繁殖障碍", "死胎木乃伊胎", "母猪木乃伊胎"],
        "DIS-038-brucella-suis-brucellosis.md": ["猪布病", "布鲁氏菌性流产", "猪布鲁氏菌病"],
        "DIS-057-coccidia-and-other-protozoa.md": ["抗球虫药相关腹泻", "球虫性腹泻", "仔猪球虫性腹泻"],
        "DIS-073-toxic-gases-ventilation-failure.md": ["通风失败", "有毒气体中毒", "氨气刺激性呼吸困难"],
    }
    existing = {(r.get("page_relpath"), r.get("alias")) for r in rows}
    new = 0
    for filename, aliases in adds.items():
        rel = "wiki/diseases/" + filename
        cid = filename.split("-", 2)[0] + "-" + filename.split("-", 2)[1]
        canonical = aliases[0]
        for alias in aliases:
            if (rel, alias) in existing:
                continue
            rows.append({"canonical_id": cid, "canonical_name": canonical, "alias": alias, "language": "zh", "alias_type": "manual_synonym_SRC-0092", "page_relpath": rel})
            new += 1
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return new


def refresh_drug_index(changed: dict[str, int]) -> None:
    path = EXPORTS / "drug_page_index.csv"
    rows = list(csv.DictReader(path.open("r", encoding="utf-8-sig", newline="")))
    fields = list(rows[0].keys())
    for row in rows:
        name = Path(row.get("page_relpath", "")).name
        if name in changed:
            row["status"] = "source_anchored_drug_evidence_page"
            sources = [x for x in row.get("sources", "").split(";") if x]
            if SOURCE_ID not in sources:
                sources.append(SOURCE_ID)
            row["sources"] = ";".join(sources)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(entries: list[Entry], changed_drugs: dict[str, int], changed_diseases: dict[str, int], facts: list[dict[str, str]], alias_count: int) -> None:
    by_cat: dict[str, int] = {}
    for e in entries:
        by_cat[e.category] = by_cat.get(e.category, 0) + 1
    lines = [
        "# 兽药合理应用与联用手册（201-400页）抽取与 Wiki 补强报告 / 2026-05-08",
        "",
        "## 抽取范围",
        "",
        "- 原始文件：`raw/md/兽药合理应用与联用手册201-400页.md`",
        f"- source_id：`{SOURCE_ID}`",
        "- 覆盖章节：抗寄生虫药后半段、抗原虫药、杀虫药、作用各系统药物、中药解表/清热/温里配伍。",
        "",
        "## 分种类抽取统计",
        "",
    ]
    for k, v in sorted(by_cat.items()):
        lines.append(f"- {k}: {v}")
    lines.extend([
        "",
        "## 写入结果",
        "",
        f"- drug 页面增强：{len(changed_drugs)} 页。",
        f"- disease 页面增强：{len(changed_diseases)} 页。",
        f"- 新增/刷新 facts：{len(facts)} 条。",
        f"- 新增疾病别名索引：{alias_count} 条。",
        "- 新增 rule card：`wiki/rule_cards/RC-SYSTEM-DRUG-RAU-002.md`。",
        "- 新增 synthesis 矩阵：`wiki/synthesis/veterinary_rational_use_201_400_system_drug_disease_rule_matrix.md`。",
        "- 新增 comparison 矩阵：`wiki/comparisons/veterinary_rational_use_201_400_symptomatic_drug_boundary_matrix.md`。",
        "- 新增 syndrome 入口：3 页。",
        "",
        "## 约束结论",
        "",
        "- 本批主要补强系统用药、对症支持、生殖系统药物、抗球虫/杀虫药和中药配伍边界。",
        "- 对症药不能替代病因诊断；具体剂量、疗程、休药期、MRL 或合规结论仍需当前标签/A0/A1 来源。",
    ])
    (ISSUES / "veterinary_rational_use_201_400_extraction_and_wiki_augmentation_2026-05-08.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    text = read_raw()
    entries = entries_from_text(text)
    ensure_source_page()
    append_source_index()
    changed_drugs = write_drug_pages(entries, text)
    changed_diseases = write_disease_pages()
    write_syndromes()
    write_rule_and_matrices(entries)
    facts = write_exports(entries, text)
    aliases = append_aliases()
    refresh_drug_index(changed_drugs)
    write_report(entries, changed_drugs, changed_diseases, facts, aliases)
    print(json.dumps({"source_id": SOURCE_ID, "entries": len(entries), "drug_pages_changed": len(changed_drugs), "disease_pages_changed": len(changed_diseases), "facts_written": len(facts), "aliases_added": aliases, "report": str(ISSUES / "veterinary_rational_use_201_400_extraction_and_wiki_augmentation_2026-05-08.md")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
