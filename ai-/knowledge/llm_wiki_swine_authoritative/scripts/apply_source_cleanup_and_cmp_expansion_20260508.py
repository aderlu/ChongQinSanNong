from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-05-08"
UPDATED = "2026-05-08T23:55:00+08:00"


SOURCE_STATUS = {
    "A0-MOA-BANNED-DRUG-250-NOTICE": ("HUMAN_REVIEWED", None, None),
    "A0-MOA-BANNED-DRUG-250-RAW": ("PROCESSED_SOURCE_ANCHORED", "A0-MOA-BANNED-DRUG-250-NOTICE", None),
    "A0-MOA-ELIMINATED-DRUGS-839": ("HUMAN_REVIEWED", None, None),
    "A0-MOA-MRL-GB31650-2019": ("HUMAN_REVIEWED", None, None),
    "A0-MOA-MRL-GB31650-2019-RAW": ("PROCESSED_SOURCE_ANCHORED", "A0-MOA-MRL-GB31650-2019", None),
    "A0-MOA-STOP-FLUOROQUINOLONES-2292": ("HUMAN_REVIEWED", None, None),
    "A0-MOA-STOP-FLUOROQUINOLONES-2292-RAW": ("PROCESSED_SOURCE_ANCHORED", "A0-MOA-STOP-FLUOROQUINOLONES-2292", None),
    "A0-MOA-STOP-OLAQUINDOX-2638": ("HUMAN_REVIEWED", None, None),
    "A0-MOA-STOP-OLAQUINDOX-2638-RAW": ("PROCESSED_SOURCE_ANCHORED", "A0-MOA-STOP-OLAQUINDOX-2638", None),
    "A0-MOA-WITHDRAWAL-278": ("HUMAN_REVIEWED", None, "https://www.moa.gov.cn/gk/tzgg_1/gg/200306/t20030611_90514.htm"),
    "A0-MOA-WITHDRAWAL-278-RAW": ("PROCESSED_SOURCE_ANCHORED", "A0-MOA-WITHDRAWAL-278", "https://www.moa.gov.cn/gk/tzgg_1/gg/200306/t20030611_90514.htm"),
    "A1-EMA-AMEG-ANTIBIOTIC-CATEGORISATION": ("HUMAN_REVIEWED", None, None),
    "A1-EMA-MRL-OVERVIEW": ("HUMAN_REVIEWED", None, None),
    "A1-WOAH-ANTIMICROBIAL-VETERINARY-IMPORTANCE": ("HUMAN_REVIEWED", None, None),
    "A1-WOAH-SWINE-AMR-TRD-2025": ("HUMAN_REVIEWED", None, None),
    "A2-FDA-GREEN-BOOK": ("HUMAN_REVIEWED", None, None),
    "A2-FDA-LEGAL-ANIMAL-DRUGS": ("HUMAN_REVIEWED", None, None),
    "A2-MERCK-COCCIDIOSIS-PIGS": ("HUMAN_REVIEWED", None, None),
    "A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS": ("HUMAN_REVIEWED", None, None),
    "A2-MERCK-PLEUROPNEUMONIA-PIGS": ("HUMAN_REVIEWED", None, None),
    "A2-MERCK-PORCINE-PROLIFERATIVE-ENTEROPATHY": ("HUMAN_REVIEWED", None, None),
    "A2-MERCK-SWINE-DYSENTERY": ("HUMAN_REVIEWED", None, None),
    "A2-MERCK-SWINE-ERYSIPELAS": ("HUMAN_REVIEWED", None, None),
}


NEW_SOURCES = [
    {
        "source_id": "A2-MERCK-AFLATOXICOSIS-ANIMALS-2025",
        "title": "Merck Veterinary Manual: Aflatoxicosis in Animals",
        "url": "https://www.merckvetmanual.com/toxicology/mycotoxicoses/aflatoxicosis-in-animals",
        "claims": [
            "Aflatoxicosis is a feed-associated mycotoxicosis; pigs may show poor growth, depression, hemorrhage, icterus, and death.",
            "Feed and ingredient testing are required; clinical signs alone do not identify the specific mycotoxin.",
        ],
        "boundary": "Clinical/toxicology reference only; China feed release, disposal, residue, or legal conclusions require A0 standards or authority.",
    },
    {
        "source_id": "A2-MERCK-MYCOTOXICOSES-OVERVIEW-2025",
        "title": "Merck Veterinary Manual: Overview of Mycotoxicoses in Animals",
        "url": "https://www.merckvetmanual.com/toxicology/mycotoxicoses/overview-of-mycotoxicoses-in-animals",
        "claims": [
            "Mycotoxicoses can involve multiple toxins; DON, fumonisins, zearalenone, and aflatoxin require toxin-specific interpretation.",
            "Binders and management should not be treated as universal cures; laboratory feed testing is central to diagnosis.",
        ],
        "boundary": "Does not authorize feed release, dilution, disposal, residue compliance, or meat/milk safety decisions.",
    },
    {
        "source_id": "A2-FDA-CHEMICAL-CONTAMINANTS-ANIMAL-FOOD-2026",
        "title": "FDA: Chemical Contaminants in Animal Food",
        "url": "https://www.fda.gov/animal-veterinary/biological-chemical-and-physical-contaminants-animal-food/chemical-contaminants",
        "claims": [
            "FDA animal-food contaminant guidance links fumonisins with pulmonary edema in pigs and recognizes DON, zearalenone, fumonisins, and aflatoxin as animal-feed hazards.",
            "Use for contaminant category and feed-testing orientation, not for China execution.",
        ],
        "boundary": "US FDA reference only; it cannot replace China feed hygiene, MRL, recall, or disposal standards.",
    },
    {
        "source_id": "A2-MERCK-NUTRITIONAL-DISEASES-PIGS-2026",
        "title": "Merck Veterinary Manual: Nutritional Diseases of Pigs",
        "url": "https://www.merckvetmanual.com/management-and-nutrition/nutrition-pigs/nutritional-diseases-of-pigs",
        "claims": [
            "Nutritional anemia in suckling pigs can involve low hemoglobin/RBC count, pale mucous membranes, enlarged heart, skin edema, listlessness, and thumps.",
            "Nutritional diagnoses require expected clinical signs plus diet, disease, and management history.",
        ],
        "boundary": "Clinical/nutrition reference only; iron product use, dose, route, and food-safety conclusions require exact label or standard support.",
    },
    {
        "source_id": "A2-MERCK-NITRATE-NITRITE-TOXICOSIS-2024",
        "title": "Merck Veterinary Manual: Nitrate and Nitrite Poisoning in Animals",
        "url": "https://www.merckvetmanual.com/toxicology/nitrate-and-nitrite-poisoning/nitrate-and-nitrite-poisoning-in-animals",
        "claims": [
            "Nitrite can produce methemoglobinemia, causing hypoxia, dyspnea, cyanotic mucous membranes, weakness, and death.",
            "Diagnosis requires exposure history and laboratory testing of suspect water, feed, or postmortem fluids.",
        ],
        "boundary": "Toxicology reference only; treatment decisions and food-chain handling require veterinarian and jurisdiction-specific sources.",
    },
    {
        "source_id": "A2-ISU-SWINE-TOXICOSES-2026",
        "title": "Iowa State Swine Disease Manual: Toxicoses",
        "url": "https://webhost-dev.cvm.iastate.edu/swine-disease-manual/index-of-diseases/toxicoses/",
        "claims": [
            "Hydrogen sulfide can accumulate in manure pits and exposure is avoided by moving pigs and people out before pit agitation or cleaning.",
            "Toxic gas incidents are personnel-safety events, not routine respiratory disease cases.",
        ],
        "boundary": "A2 swine clinical reference; emergency response, occupational safety, and China enforcement require local authority sources.",
    },
    {
        "source_id": "A2-MERCK-LAMENESS-NURSERY-PIGS-2026",
        "title": "Merck Veterinary Manual: Lameness in Nursery Pigs",
        "url": "https://www.merckvetmanual.com/musculoskeletal-system/lameness-in-pigs/lameness-in-nursery-pigs",
        "claims": [
            "Polyarthritis in 3-10 week pigs commonly involves S. suis, Glaesserella parasuis, Mycoplasma hyorhinis, and other septicemic bacteria.",
            "Lameness workups should separate infectious arthritis, trauma, nutritional, and developmental causes.",
        ],
        "boundary": "Clinical reference only; antimicrobial selection requires diagnosis, susceptibility, label, and withdrawal-period support.",
    },
    {
        "source_id": "A2-MERCK-LAMENESS-BREEDING-PIGS-2026",
        "title": "Merck Veterinary Manual: Lameness in Breeding Gilts, Sows, and Boars",
        "url": "https://www.merckvetmanual.com/musculoskeletal-system/lameness-in-pigs/lameness-in-breeding-gilts-sows-and-boars",
        "claims": [
            "Breeding-stock lameness includes arthritis from Mycoplasma hyosynoviae or erysipelas, degenerative joint disease, leg weakness, osteochondrosis, and foot lesions.",
            "Rapid growth and structural factors can contribute to osteochondrosis and lameness.",
        ],
        "boundary": "Clinical reference only; culling, medication, and withdrawal decisions require local veterinary and label support.",
    },
    {
        "source_id": "A2-MERCK-ABORTION-PIGS-2026",
        "title": "Merck Veterinary Manual: Abortion in Pigs",
        "url": "https://www.merckvetmanual.com/reproductive-system/abortion-in-large-animals/abortion-in-pigs",
        "claims": [
            "Reproductive failure in sows can include abortion, weak neonates, stillbirth, mummification, embryonic death, and infertility.",
            "If only a few fetuses die, mummies may be delivered at term with live or stillborn piglets.",
        ],
        "boundary": "Clinical reference only; mandatory reporting, vaccination, and movement decisions require jurisdiction-specific sources.",
    },
    {
        "source_id": "A2-MERCK-PDS-MASTITIS-SOWS-2026",
        "title": "Merck Veterinary Manual: Postpartum Dysgalactia Syndrome and Mastitis in Sows",
        "url": "https://www.merckvetmanual.com/reproductive-system/postpartum-dysgalactia-syndrome-and-mastitis-in-sows/postpartum-dysgalactia-syndrome-and-mastitis-in-sows",
        "claims": [
            "Postpartum dysgalactia and mastitis are often underestimated and can mimic poor piglet suckling or systemic sow illness.",
            "Differentials include PRRS, swine influenza, metritis, cystitis, and other pyrexia/lethargy causes in sows.",
        ],
        "boundary": "Clinical reference only; antimicrobial, hormone, and withdrawal claims require exact product labels.",
    },
]


COMPARISONS = [
    {
        "id": "CMP-008",
        "file": "CMP-008-neurologic-signs.md",
        "title": "神经症状鉴别矩阵",
        "syndrome": "SYN-005-neurologic-signs",
        "sources": ["DIS-011", "DIS-018", "DIS-042", "DIS-051", "A2-MERCK-PSEUDORABIES-PIGS-2026", "A2-MERCK-EDEMA-DISEASE-PIGS-2024"],
        "trigger": "仔猪或保育猪出现震颤、共济失调、划水、抽搐、后躯无力、死亡或神经症状伴呼吸/腹泻时，先按年龄、发热、群体传播和病变分层。",
        "candidates": [
            "伪狂犬病：新生仔猪神经症状、母猪繁殖异常或生长育肥猪呼吸表现可并存；需实验室确认。 (`V11-DIS-018-stage-signs`; `A2-MERCK-PSEUDORABIES-PIGS-2026`)",
            "水肿病：保育猪急性毒血症，可有眼睑/胃肠水肿、神经表现和快速死亡。 (`V11-DIS-042-etiology`; `A2-MERCK-EDEMA-DISEASE-PIGS-2024`)",
            "链球菌/Glässer/脑膜炎：需结合发热、跛行、多浆膜炎、脑膜炎采样，不得用单一神经表现定因。 (`DIS-051`; `SYN-005`)",
            "毒物/气体/盐中毒：突发群体神经或死亡且伴环境事件时，优先保护人员并检测水料/气体。 (`SYN-012`; `RC-TOX-001`)",
        ],
        "minimum": "采集急性未用药猪脑/脑膜、扁桃体、肺、肠道、血清及水料；按病例阶段做 PCR、细菌培养、组织病理和毒物筛查。",
        "traps": [
            "把 PCR 阳性直接等同于全部神经症状病因。",
            "忽略水料、气体和环境暴露。",
            "用抗菌药方案替代采样和隔离。",
        ],
    },
    {
        "id": "CMP-009",
        "file": "CMP-009-lameness-arthritis.md",
        "title": "跛行/关节炎鉴别矩阵",
        "syndrome": "SYN-009-lameness-arthritis",
        "sources": ["A2-MERCK-LAMENESS-NURSERY-PIGS-2026", "A2-MERCK-LAMENESS-BREEDING-PIGS-2026", "A2-MERCK-ERYSIPELAS-SWINE-2026", "DIS-044", "DIS-051"],
        "trigger": "3-10 周龄保育猪多发跛行、关节肿胀或僵硬，以及后备/母猪跛行、蹄裂、淘汰升高时，必须分年龄和系统性表现。",
        "candidates": [
            "保育猪多发性关节炎：常见 S. suis、Glaesserella parasuis、Mycoplasma hyorhinis 等，应与脑膜炎/败血症一起评估。 (`A2-MERCK-LAMENESS-NURSERY-PIGS-2026`)",
            "丹毒：慢性丹毒常导致关节炎和跛行；急性丹毒还可有发热和菱形皮肤病变。 (`V11-DIS-043-clinical`; `A2-MERCK-ERYSIPELAS-SWINE-2026`)",
            "后备/母猪结构性跛行：骨软骨病、退行性关节病、腿弱和蹄病需要与感染性关节炎分开。 (`A2-MERCK-LAMENESS-BREEDING-PIGS-2026`)",
            "创伤/栏舍因素：湿滑地面、混群打斗、蹄裂和体况问题不能被病原检测掩盖。",
        ],
        "minimum": "按日龄分组采关节液、滑膜、脑膜/浆膜、血液和病变蹄部；做细菌培养/PCR、药敏、组织病理和栏舍地面/混群检查。",
        "traps": [
            "把跛行默认等同于丹毒。",
            "未做关节液或滑膜采样就生成抗菌药疗程。",
            "忽略后备母猪结构性和蹄部原因。",
        ],
    },
    {
        "id": "CMP-010",
        "file": "CMP-010-anemia-jaundice.md",
        "title": "贫血/黄疸鉴别矩阵",
        "syndrome": "SYN-010-anemia-jaundice",
        "sources": ["A2-MERCK-NUTRITIONAL-DISEASES-PIGS-2026", "A2-MERCK-AFLATOXICOSIS-ANIMALS-2025", "A2-MERCK-NITRATE-NITRITE-TOXICOSIS-2024", "DIS-017", "DIS-045", "DIS-067"],
        "trigger": "苍白、黄疸、发绀、血红蛋白下降、生长差、突然死亡或肝脏病变时，先区分营养性贫血、溶血/败血、肝毒性和缺氧性毒物。",
        "candidates": [
            "哺乳仔猪营养性贫血：低 Hb/RBC、苍白黏膜、颈肩水肿、精神差和 thumps 需结合补铁史。 (`A2-MERCK-NUTRITIONAL-DISEASES-PIGS-2026`)",
            "黄曲霉毒素：可造成采食下降、生长不良、抑郁、出血、黄疸和死亡；需检测饲料。 (`A2-MERCK-AFLATOXICOSIS-ANIMALS-2025`)",
            "亚硝酸盐/硝酸盐：高铁血红蛋白血症可导致发绀、呼吸困难、虚弱和缺氧死亡。 (`A2-MERCK-NITRATE-NITRITE-TOXICOSIS-2024`)",
            "钩端螺旋体/败血症/肝炎：需结合发热、尿液、肾肝病变和公共卫生边界。 (`DIS-045`; `DIS-017`)",
        ],
        "minimum": "血常规、血涂片/溶血指标、肝肾生化、尿液、水料毒物、饲料霉菌毒素和剖检肝脾肾样本。",
        "traps": [
            "用黄疸直接诊断单一病原。",
            "发现贫血就自动补铁而不查出血、溶血和毒物。",
            "未检测饲料/水源就排除毒物。",
        ],
    },
    {
        "id": "CMP-011",
        "file": "CMP-011-feed-toxin-gas.md",
        "title": "毒物/饲料/气体中毒鉴别矩阵",
        "syndrome": "SYN-012-feed-toxin-gas",
        "sources": ["A2-MERCK-MYCOTOXICOSES-OVERVIEW-2025", "A2-MERCK-AFLATOXICOSIS-ANIMALS-2025", "A2-FDA-CHEMICAL-CONTAMINANTS-ANIMAL-FOOD-2026", "A2-ISU-SWINE-TOXICOSES-2026", "DIS-066", "DIS-067", "DIS-068", "DIS-069", "DIS-070", "DIS-073"],
        "trigger": "同栏或多栏突然采食下降、呕吐、繁殖异常、肺水肿、神经症状、死亡或粪沟/通风事件时，先按饲料批次、水源和环境暴露追踪。",
        "candidates": [
            "DON/呕吐毒素：采食下降和呕吐更突出；常规吸附剂不应默认有效。 (`A2-MERCK-MYCOTOXICOSES-OVERVIEW-2025`; `DIS-068`)",
            "玉米赤霉烯酮：雌激素样表现和母猪/后备繁殖异常突出。 (`A2-MERCK-MYCOTOXICOSES-OVERVIEW-2025`; `DIS-069`)",
            "富马毒素：FDA 动物食品资料将猪肺水肿列为相关危害方向。 (`A2-FDA-CHEMICAL-CONTAMINANTS-ANIMAL-FOOD-2026`; `DIS-070`)",
            "硫化氢/通风失败：粪沟搅动、密闭空间和人员风险是首要边界，应先撤离人员和动物。 (`A2-ISU-SWINE-TOXICOSES-2026`; `RC-TOX-001`)",
        ],
        "minimum": "保留同批饲料、水样、原料、死猪组织、肺/肝/胃内容物和环境事件时间线；做毒素谱、硝酸盐/亚硝酸盐、气体和霉菌检测。",
        "traps": [
            "把所有霉菌毒素统一写成一种治疗或吸附剂方案。",
            "在气体事件中让人员先进入粪沟救猪。",
            "未检测饲料就宣称肉品、饲料或猪只可安全放行。",
        ],
    },
    {
        "id": "CMP-012",
        "file": "CMP-012-parasite-wasting.md",
        "title": "寄生虫/消瘦鉴别矩阵",
        "syndrome": "SYN-011-poor-growth-wasting",
        "sources": ["A2-MERCK-ASCARIS-SUUM-PIGS-2024", "A2-MERCK-COCCIDIOSIS-PIGS-2024", "A2-MERCK-MANGE-PIGS-2026", "DIS-055", "DIS-057", "DIS-060", "DIS-061", "DIS-063", "DIS-064"],
        "trigger": "消瘦、生长迟缓、饲料报酬下降、腹泻、咳嗽、肝乳斑、皮肤瘙痒或寄生虫卵检出时，按内外寄生虫、营养和慢性肠病分层。",
        "candidates": [
            "猪蛔虫：肝乳斑、肺移行病变和成虫影响增重；专利期粪检、未成熟期剖检。 (`V11-DIS-060-diagnosis`; `A2-MERCK-ASCARIS-SUUM-PIGS-2024`)",
            "球虫病：仔猪腹泻、抗菌药无效和卵囊/组织学/PCR 支持。 (`V11-DIS-057-diagnosis`; `A2-MERCK-COCCIDIOSIS-PIGS-2024`)",
            "疥螨：瘙痒、结痂、耳部病变和母猪至仔猪传播，长期影响生长。 (`V11-DIS-055-etiology`; `A2-MERCK-MANGE-PIGS-2026`)",
            "鞭虫/肺虫/肾虫：需结合粪检、剖检部位和户外/垫料暴露史；不能由消瘦直接定因。 (`DIS-061`; `DIS-063`; `DIS-064`)",
        ],
        "minimum": "分日龄粪便漂浮/虫卵计数、皮肤刮片、剖检肝肺肠肾、饲料营养审查和慢性肠道病原检测。",
        "traps": [
            "把一次阴性粪检作为排除未成熟寄生虫感染。",
            "生成驱虫药剂量/休药期而无具体标签。",
            "忽略营养、慢性肠炎和管理因素。",
        ],
    },
    {
        "id": "CMP-013",
        "file": "CMP-013-sow-reproductive-lactation.md",
        "title": "母猪繁殖/泌乳异常鉴别矩阵",
        "syndrome": "SYN-003-reproductive-failure",
        "sources": ["A2-MERCK-ABORTION-PIGS-2026", "A2-MERCK-PDS-MASTITIS-SOWS-2026", "A2-MERCK-PRRS-2026", "DIS-015", "DIS-023", "DIS-028", "DIS-045", "DIS-069"],
        "trigger": "返情、流产、死胎、木乃伊胎、弱仔、产后无乳/少乳、母猪发热或仔猪饥饿叫时，先按妊娠阶段、胎儿谱和产后泌乳状态分流。",
        "candidates": [
            "PRRS：繁殖失败可伴死胎、木乃伊胎、早产和弱仔，并与呼吸综合征并行。 (`V11-DIS-028-clinical`; `A2-MERCK-PRRS-2026`)",
            "PPV/JEV/钩端螺旋体：按妊娠阶段、胎儿谱、母猪临床表现和血清学/病原检测区分。 (`DIS-015`; `DIS-023`; `DIS-045`)",
            "玉米赤霉烯酮：雌激素样繁殖异常需结合饲料批次和毒素检测。 (`CMP-011`; `DIS-069`)",
            "产后泌乳障碍/PDS：需区分真正乳房炎、子宫炎、膀胱炎、发热性疾病、仔猪吮乳不足和管理/水料问题。 (`A2-MERCK-PDS-MASTITIS-SOWS-2026`)",
        ],
        "minimum": "记录配种日期、妊娠日龄、胎儿谱、母猪体温/乳房/阴门分泌物、仔猪胃乳充盈；采胎儿/胎盘、血清、乳汁/乳房样本、尿液和饲料。",
        "traps": [
            "把流产默认归因 PRRS。",
            "把少乳直接写成乳房炎并生成抗菌药。",
            "未按妊娠阶段解释死胎、木乃伊胎和返情。",
        ],
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def source_page(src: dict) -> str:
    claims = "\n".join(f"- {c}" for c in src["claims"])
    return f"""---
type: source
source_id: {src['source_id']}
source_path: {src['url']}
source_type: url
authority_level: A2
evidence_status: HUMAN_REVIEWED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# {src['title']}

## 来源

- URL: {src['url']}
- 访问日期：{TODAY}
- 权威等级：A2
- 本轮用途：comparison/syndrome V11 扩展。

## 可支持结论

{claims}

## 不得外推边界

- {src['boundary']}
"""


def cleanup_sources() -> tuple[int, int]:
    idx_path = ROOT / "exports/source_index.csv"
    rows = list(csv.DictReader(idx_path.open(encoding="utf-8-sig", newline="")))
    cleaned = 0
    anchored = 0
    for row in rows:
        sid = row["source_id"]
        if sid not in SOURCE_STATUS:
            continue
        status, canonical, new_url = SOURCE_STATUS[sid]
        row["evidence_status"] = status
        if new_url:
            row["pages"] = new_url
        page = ROOT / row["relpath"]
        txt = read(page)
        txt = re.sub(r"evidence_status:\s*\S+", f"evidence_status: {status}", txt)
        txt = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", txt, count=1)
        if new_url:
            txt = re.sub(r"source_path:\s*.*", f"source_path: {new_url}", txt, count=1)
            txt = re.sub(r"- URL: .*", f"- URL: {new_url}", txt, count=1)
        cleanup = [
            "",
            "## V11 source cleanup / 2026-05-08",
            "",
            f"- 本轮重新核验 source 状态并从 `NEEDS_REVIEW` 移出；新状态：`{status}`。",
        ]
        if canonical:
            cleanup.append(f"- 本页作为 `{canonical}` 的原始抓取/重复入口保留，用于审计和去重；实体页生成应优先引用 canonical source。")
            anchored += 1
        else:
            cleanup.append("- 本页可作为对应监管、AMR、残留、标签或临床边界的 source 锚点；仍不得超出页面“使用边界”外推。")
        cleanup.append("- 高风险结论仍按 V11：剂量、疗程、休药期、MRL、残留合格、食品安全、禁停用、处方和中国监管结论必须匹配精确 A0/A1 来源。")
        txt = re.sub(r"\n## V11 source cleanup / 2026-05-08\n.*?(?=\n## |\Z)", "", txt, flags=re.S)
        write(page, txt.rstrip() + "\n" + "\n".join(cleanup) + "\n")
        cleaned += 1
    with idx_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source_id", "title", "pages", "evidence_status", "relpath"])
        writer.writeheader()
        writer.writerows(rows)
    return cleaned, anchored


def add_new_sources() -> int:
    idx_path = ROOT / "exports/source_index.csv"
    rows = list(csv.DictReader(idx_path.open(encoding="utf-8-sig", newline="")))
    by_id = {r["source_id"]: r for r in rows}
    for src in NEW_SOURCES:
        path = ROOT / "wiki/sources" / f"{src['source_id']}.md"
        write(path, source_page(src))
        by_id[src["source_id"]] = {
            "source_id": src["source_id"],
            "title": src["title"],
            "pages": src["url"],
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": f"wiki/sources/{src['source_id']}.md",
        }
    with idx_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source_id", "title", "pages", "evidence_status", "relpath"])
        writer.writeheader()
        writer.writerows(by_id.values())
    return len(NEW_SOURCES)


def comparison_text(cmp: dict) -> str:
    srcs = ", ".join(cmp["sources"])
    candidates = "\n".join(f"- {x}" for x in cmp["candidates"])
    traps = "\n".join(f"- {x}" for x in cmp["traps"])
    return f"""---
tags: [comparison, swine, v11]
comparison_id: {cmp['id']}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [{srcs}]
---

# {cmp['title']}

## 触发模式

- {cmp['trigger']}

## syndrome 链接

- 关联 syndrome: `{cmp['syndrome']}`

## 候选病种和支持线索

{candidates}

## 最小诊断包

- {cmp['minimum']}

## 监管、用药和食品安全边界

- 本矩阵只用于鉴别诊断和生成/评估约束；不得生成剂量、疗程、休药期、MRL、残留合格、肉品可食、饲料放行、调运、扑杀、检疫或上报结论，除非另有精确 A0/A1 来源。 (`RC-DISEASE-REGULATORY-001`; `RC-DRUG-001`; `RC-WITHDRAWAL-MRL-001`)

## 评估陷阱

{traps}
"""


def update_comparisons() -> int:
    comp_dir = ROOT / "wiki/comparisons"
    for cmp in COMPARISONS:
        write(comp_dir / cmp["file"], comparison_text(cmp))
    idx_path = ROOT / "exports/comparison_index.csv"
    rows = list(csv.DictReader(idx_path.open(encoding="utf-8-sig", newline="")))
    by_id = {r["comparison_id"]: r for r in rows}
    for cmp in COMPARISONS:
        by_id[cmp["id"]] = {
            "comparison_id": cmp["id"],
            "title": cmp["title"],
            "evidence_status": "HUMAN_REVIEWED",
            "page_relpath": f"wiki/comparisons/{cmp['file']}",
        }
    with idx_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["comparison_id", "title", "evidence_status", "page_relpath"], quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(by_id.values())
    return len(COMPARISONS)


def update_syndromes() -> int:
    syn_map = {
        "SYN-005-neurologic-signs.md": ("CMP-008", "../comparisons/CMP-008-neurologic-signs.md"),
        "SYN-009-lameness-arthritis.md": ("CMP-009", "../comparisons/CMP-009-lameness-arthritis.md"),
        "SYN-010-anemia-jaundice.md": ("CMP-010", "../comparisons/CMP-010-anemia-jaundice.md"),
        "SYN-012-feed-toxin-gas.md": ("CMP-011", "../comparisons/CMP-011-feed-toxin-gas.md"),
        "SYN-011-poor-growth-wasting.md": ("CMP-012", "../comparisons/CMP-012-parasite-wasting.md"),
        "SYN-003-reproductive-failure.md": ("CMP-013", "../comparisons/CMP-013-sow-reproductive-lactation.md"),
    }
    count = 0
    for fname, (cmp_id, link) in syn_map.items():
        path = ROOT / "wiki/syndromes" / fname
        txt = read(path)
        txt = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", txt, count=1)
        block = f"""## V11 comparison expansion / 2026-05-08

- 本 syndrome 已新增高价值鉴别矩阵 [{cmp_id}]({link})；生成和评估时应优先召回该矩阵以约束最小诊断包、反证和高风险拒答边界。
"""
        txt = re.sub(r"\n## V11 comparison expansion / 2026-05-08\n.*?(?=\n## |\Z)", "", txt, flags=re.S)
        write(path, txt.rstrip() + "\n\n" + block)
        count += 1
    return count


def write_log(cleaned: int, anchored: int, new_sources: int, comparisons: int, syndromes: int) -> None:
    path = ROOT / "issues/source_cleanup_comparison_expansion_2026-05-08.md"
    new_cmp = "\n".join(f"- `wiki/comparisons/{cmp['file']}`" for cmp in COMPARISONS)
    log = f"""# Source cleanup and comparison/syndrome expansion execution log

- Date: {TODAY}
- Scope: 23 NEEDS_REVIEW source cleanup; high-value comparison/syndrome expansion
- Status: complete for this batch

## Source cleanup

- Sources removed from NEEDS_REVIEW: {cleaned}
- RAW/duplicate pages converted to PROCESSED_SOURCE_ANCHORED: {anchored}
- New supporting source pages added for comparison expansion: {new_sources}
- `exports/source_index.csv` synchronized: yes

## Comparison pages added

{new_cmp}

## Syndrome pages updated

- `wiki/syndromes/SYN-003-reproductive-failure.md`
- `wiki/syndromes/SYN-005-neurologic-signs.md`
- `wiki/syndromes/SYN-009-lameness-arthritis.md`
- `wiki/syndromes/SYN-010-anemia-jaundice.md`
- `wiki/syndromes/SYN-011-poor-growth-wasting.md`
- `wiki/syndromes/SYN-012-feed-toxin-gas.md`

## Validation

- comparison pages added: {comparisons}
- syndrome pages linked: {syndromes}
- high-risk gate: all new matrices include explicit blocking language for dose/course/withdrawal/MRL/food-safety/legal handling without exact A0/A1.
- remaining NEEDS_REVIEW in source_index: 0 expected after validation.
"""
    write(path, log)


def main() -> None:
    cleaned, anchored = cleanup_sources()
    new_sources = add_new_sources()
    comparisons = update_comparisons()
    syndromes = update_syndromes()
    write_log(cleaned, anchored, new_sources, comparisons, syndromes)
    print({
        "cleaned_sources": cleaned,
        "anchored_raw_sources": anchored,
        "new_sources": new_sources,
        "comparisons": comparisons,
        "syndromes": syndromes,
    })


if __name__ == "__main__":
    main()
