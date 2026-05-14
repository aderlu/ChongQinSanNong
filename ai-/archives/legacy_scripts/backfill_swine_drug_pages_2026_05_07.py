from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
NOW = "2026-05-07T22:45:00+08:00"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


DRUGS = [
    {
        "id": "DRUG-009-penicillin-g",
        "title": "Penicillin G / 青霉素G",
        "klass": "beta-lactam / penicillin",
        "sources": ["SRC-0012", "SRC-0062", "SRC-0065", "SRC-0075", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在 Chapter 10 以及猪丹毒、链球菌病、梭菌病、放线杆菌病、炭疽、李斯特菌病和脓肿相关章节中多次命中 Penicillin G / penicillin。",
            "候选页码：PDF page 184, 186, 190, 784, 820, 825, 827, 865, 966, 967, 1006, 1009, 1018, 1022。",
        ],
        "uses": "猪丹毒、链球菌病、梭菌病等革兰阳性菌相关治疗候选；必须以药敏、当地标签和兽医处方复核。",
    },
    {
        "id": "DRUG-010-amoxicillin",
        "title": "Amoxicillin / 阿莫西林",
        "klass": "beta-lactam / aminopenicillin",
        "sources": ["SRC-0012", "SRC-0062", "SRC-0063", "SRC-0075", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在 Chapter 10、梭菌性肠炎预防、放线杆菌敏感性、大肠杆菌病和链球菌病语境中命中 amoxicillin。",
            "候选页码：PDF page 184, 187, 190, 784, 820, 847, 967。",
        ],
        "uses": "氨基青霉素类抗菌候选；不得从教材直接生成中国处方、给水用药方案或休药期。",
    },
    {
        "id": "DRUG-011-ceftiofur",
        "title": "Ceftiofur / 头孢噻呋",
        "klass": "third-generation cephalosporin",
        "sources": ["SRC-0012", "SRC-0059", "SRC-0063", "SRC-0070", "SRC-0074", "SRC-0075", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在放线杆菌病、支气管败血波氏杆菌混合呼吸道病、大肠杆菌耐药、巴氏杆菌肺炎、葡萄球菌病和链球菌病语境中命中 ceftiofur。",
            "候选页码：PDF page 184, 187, 188, 190, 784, 787, 798, 836, 840, 847, 918, 919, 946, 954, 966, 967。",
        ],
        "uses": "呼吸道和系统性细菌病抗菌候选；因第三代头孢公共卫生重要性，生成答案必须优先提示诊断、药敏和合规复核。",
    },
    {
        "id": "DRUG-012-florfenicol",
        "title": "Florfenicol / 氟苯尼考",
        "klass": "phenicol",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0075", "SRC-0073", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在 Chapter 10、放线杆菌病、支原体病、链球菌病和沙门氏菌病语境中命中 florfenicol。",
            "候选页码：PDF page 185, 784, 893, 966。",
        ],
        "uses": "酰胺醇类抗菌候选；需要与氯霉素禁用边界区分，不能混同为同一合规状态。",
    },
    {
        "id": "DRUG-013-tiamulin",
        "title": "Tiamulin / 泰妙菌素",
        "klass": "pleuromutilin",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0071", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在猪痢疾、Brachyspira 结肠炎、支原体病、增生性肠炎、放线杆菌病和钩端螺旋体语境中命中 tiamulin。",
            "候选页码：PDF page 185, 188, 784, 787, 893, 931, 967, 983, 984, 990, 1099, 1100。",
        ],
        "uses": "截短侧耳素类候选，常见于 Brachyspira、支原体和 Lawsonia 相关语境；需提示离子载体相互作用等安全边界。",
    },
    {
        "id": "DRUG-014-lincomycin",
        "title": "Lincomycin / 林可霉素",
        "klass": "lincosamide",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0074", "SRC-0075", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在猪痢疾、Brachyspira 结肠炎、支原体病、葡萄球菌病、链球菌病和蹄部皮肤病变语境中命中 lincomycin。",
            "候选页码：PDF page 184, 784, 893, 898, 954, 983, 984, 990, 1020。",
        ],
        "uses": "林可酰胺类抗菌候选；可用于候选检索和越界识别，不输出剂量或疗程。",
    },
    {
        "id": "DRUG-015-tylosin",
        "title": "Tylosin / 泰乐菌素",
        "klass": "macrolide",
        "sources": ["SRC-0012", "SRC-0059", "SRC-0069", "SRC-0071", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在增生性肠炎、猪痢疾、Brachyspira 结肠炎、支原体病、萎缩性鼻炎和钩端螺旋体语境中命中 tylosin。",
            "候选页码：PDF page 185, 784, 823, 884, 893, 931, 983, 984, 990, 1084, 1100。",
        ],
        "uses": "大环内酯类候选；必须保留耐药和标签复核边界。",
    },
    {
        "id": "DRUG-016-tylvalosin",
        "title": "Tylvalosin / 泰万菌素",
        "klass": "macrolide",
        "sources": ["SRC-0012", "SRC-0071", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在增生性肠炎、猪痢疾和 Brachyspira 控制语境中命中 tylvalosin。",
            "候选页码：PDF page 185, 931, 983, 984, 990。",
        ],
        "uses": "大环内酯类候选，偏 Lawsonia/Brachyspira 语境；中国适用性需标签复核。",
    },
    {
        "id": "DRUG-017-tulathromycin",
        "title": "Tulathromycin / 泰拉霉素",
        "klass": "macrolide",
        "sources": ["SRC-0012", "SRC-0059", "SRC-0070", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在放线杆菌病、波氏杆菌/巴氏杆菌混合呼吸道病和巴氏杆菌肺炎语境中命中 tulathromycin。",
            "候选页码：PDF page 185, 190, 784, 798, 918, 919。",
        ],
        "uses": "呼吸道病大环内酯候选；不得将美国标签直接转写为中国适应证。",
    },
    {
        "id": "DRUG-018-enrofloxacin",
        "title": "Enrofloxacin / 恩诺沙星",
        "klass": "fluoroquinolone",
        "sources": ["SRC-0012", "SRC-0059", "SRC-0063", "SRC-0070", "SRC-0075", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在放线杆菌病、波氏杆菌病、大肠杆菌病/产后乳房炎-无乳综合征、巴氏杆菌肺炎和链球菌病语境中命中 enrofloxacin。",
            "候选页码：PDF page 185, 186, 187, 190, 784, 798, 836, 854, 918, 919, 954, 955, 966。",
        ],
        "uses": "氟喹诺酮类抗菌候选；属于高关注抗菌药，答案应优先建议实验室诊断、药敏和合规标签核验。",
    },
    {
        "id": "DRUG-019-oxytetracycline",
        "title": "Oxytetracycline / 土霉素",
        "klass": "tetracycline",
        "sources": ["SRC-0012", "SRC-0062", "SRC-0065", "SRC-0067", "SRC-0069", "SRC-0070", "SRC-0075", "A0-MOA-WITHDRAWAL-278"],
        "evidence": [
            "教材候选表将 oxytetracycline 纳入 tetracycline 类，并在放线杆菌病、波氏杆菌/萎缩性鼻炎、梭菌病、猪丹毒、钩端螺旋体、支原体、巴氏杆菌和链球菌病语境中命中。",
            "候选页码：PDF page 185, 186, 187, 190, 784, 798, 820, 825, 827, 865, 875, 884, 893, 898, 918, 919, 931, 937, 954, 955, 966, 970, 971, 1006, 1009, 1022。",
            "农业部公告第278号可作为停药期法规入口之一，但具体剂型、产品和现行有效性仍需复核。",
        ],
        "uses": "四环素类具体药物候选；广泛语境不等于广谱处方，应保留耐药/药敏边界。",
    },
    {
        "id": "DRUG-020-chlortetracycline",
        "title": "Chlortetracycline / 金霉素",
        "klass": "tetracycline",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0071", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 chlortetracycline 纳入 tetracycline 类，主要作为四环素类抗菌候选进入呼吸道、肠道和螺旋体相关语境。",
            "候选页码见 tetracyclines 汇总：PDF page 185, 186, 187, 190, 784, 798, 820, 825, 827, 865, 875, 884, 893, 898, 918, 919, 931, 937, 954, 955, 966, 970, 971, 1006, 1009, 1022。",
        ],
        "uses": "四环素类具体药物候选；不得生成群体长期添加方案或促生长用途。",
    },
    {
        "id": "DRUG-021-doxycycline",
        "title": "Doxycycline / 多西环素",
        "klass": "tetracycline",
        "sources": ["SRC-0012", "SRC-0067", "SRC-0069", "SRC-0070", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 doxycycline 纳入 tetracycline 类，并在钩端螺旋体、支原体和呼吸道细菌语境中提供候选依据。",
            "候选页码见 tetracyclines 汇总：PDF page 185, 186, 187, 190, 784, 798, 820, 825, 827, 865, 875, 884, 893, 898, 918, 919, 931, 937, 954, 955, 966, 970, 971, 1006, 1009, 1022。",
        ],
        "uses": "四环素类具体药物候选；中国标签、适应证和休药期需逐项核验。",
    },
    {
        "id": "DRUG-022-sulfonamide-trimethoprim",
        "title": "Sulfonamide-trimethoprim combinations / 磺胺-甲氧苄啶类组合",
        "klass": "potentiated sulfonamide",
        "sources": ["SRC-0012", "SRC-0059", "SRC-0063", "SRC-0070", "SRC-0074", "SRC-0075", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在急性呼吸道感染、萎缩性鼻炎、大肠杆菌病、放线杆菌病、葡萄球菌病、链球菌病和沙门氏菌病语境中命中 sulfonamides / trimethoprim-sulfonamide combinations。",
            "候选页码：PDF page 184, 186, 192, 784, 787, 798, 840, 847, 854, 918, 923, 946, 954, 955, 966, 967, 1022。",
        ],
        "uses": "增效磺胺组合候选；需注意具体成分、适应证和残留合规。",
    },
    {
        "id": "DRUG-023-gentamicin",
        "title": "Gentamicin / 庆大霉素",
        "klass": "aminoglycoside",
        "sources": ["SRC-0012", "SRC-0063", "SRC-0075", "SRC-0076", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 gentamicin 纳入 aminoglycosides，并在大肠杆菌病、放线杆菌病、支原体排除/可变、链球菌病和李斯特菌病语境中命中。",
            "候选页码：PDF page 184, 186, 189, 784, 787, 836, 840, 847, 849, 854, 884, 893, 931, 946, 955, 967, 971, 976, 983, 1018, 1020, 1024。",
        ],
        "uses": "氨基糖苷类候选；毒性和食品动物标签边界必须显式保留。",
    },
    {
        "id": "DRUG-024-neomycin",
        "title": "Neomycin / 新霉素",
        "klass": "aminoglycoside",
        "sources": ["SRC-0012", "SRC-0063", "SRC-0082", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 neomycin 纳入 aminoglycosides，主要出现在肠道细菌和驱虫药表附近的用药边界语境中。",
            "候选页码见 aminoglycosides 汇总：PDF page 184, 186, 189, 784, 787, 836, 840, 847, 849, 854, 884, 893, 931, 946, 955, 967, 971, 976, 983, 1018, 1020, 1024。",
        ],
        "uses": "氨基糖苷类具体药物候选；不得输出无标签的口服/群体给药方案。",
    },
    {
        "id": "DRUG-025-apramycin",
        "title": "Apramycin / 安普霉素",
        "klass": "aminoglycoside",
        "sources": ["SRC-0012", "SRC-0063", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 apramycin 纳入 aminoglycosides，并在大肠杆菌病等肠道细菌候选语境中命中。",
            "候选页码见 aminoglycosides 汇总：PDF page 184, 186, 189, 784, 787, 836, 840, 847, 849, 854, 884, 893, 931, 946, 955, 967, 971, 976, 983, 1018, 1020, 1024。",
        ],
        "uses": "氨基糖苷类具体药物候选；需要按中国批准产品核验。",
    },
    {
        "id": "DRUG-026-spectinomycin",
        "title": "Spectinomycin / 壮观霉素",
        "klass": "aminocyclitol / aminoglycoside-related",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 spectinomycin 与 aminoglycosides/lincomycin-spectinomycin 语境并列，命中支原体、猪痢疾和肠道细菌相关章节。",
            "候选页码见 aminoglycosides 汇总及 lincomycin 条目：PDF page 184, 186, 189, 784, 787, 836, 840, 847, 849, 854, 884, 893, 931, 946, 955, 967, 971, 976, 983, 1018, 1020, 1024。",
        ],
        "uses": "壮观霉素/林可-壮观组合候选；应拆分具体产品标签核验。",
    },
    {
        "id": "DRUG-027-toltrazuril",
        "title": "Toltrazuril / 托曲珠利",
        "klass": "triazinone anticoccidial",
        "sources": ["SRC-0081", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在哺乳仔猪 Cystoisospora suis 球虫病语境中命中 toltrazuril，并将弓形虫相关化合物讨论作为边界。",
            "候选页码：PDF page 1043, 1045。",
        ],
        "uses": "抗球虫具体药物候选；只能作为球虫病治疗候选证据，需标签和休药期复核。",
    },
    {
        "id": "DRUG-028-iron-dextran",
        "title": "Iron dextran / 右旋糖酐铁",
        "klass": "mineral hematinic / supportive therapy",
        "sources": ["SRC-0012", "SRC-0069", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在 Mycoplasma suis 贫血支持治疗、哺乳仔猪缺铁和铁制剂中毒边界语境中命中 iron dextran / injectable iron。",
            "候选页码：PDF page 281, 901, 1075, 1076。",
        ],
        "uses": "补铁/支持治疗候选，不属于抗菌药；需区分预防性补铁、贫血支持和铁中毒风险。",
    },
    {
        "id": "DRUG-029-nsaids",
        "title": "NSAIDs / 非甾体抗炎药",
        "klass": "anti-inflammatory supportive therapy",
        "sources": ["SRC-0012", "SRC-0066", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表在 Glässer 病支持恢复和一般药理/支持护理语境中命中 NSAIDs。",
            "候选页码：PDF page 193, 194, 209, 240, 355, 875, 946。",
        ],
        "uses": "支持治疗类别候选，不是病原治疗；具体药物、适应证和休药期必须按标签核验。",
    },
    {
        "id": "DRUG-030-tetracyclines",
        "title": "Tetracyclines / 四环素类",
        "klass": "antimicrobial class",
        "sources": ["SRC-0012", "SRC-0062", "SRC-0065", "SRC-0067", "SRC-0069", "SRC-0070", "SRC-0075", "A0-MOA-WITHDRAWAL-278"],
        "evidence": [
            "教材候选表将 oxytetracycline、chlortetracycline、doxycycline 纳入四环素类，并跨多个细菌和螺旋体章节命中。",
            "候选页码：PDF page 185, 186, 187, 190, 784, 798, 820, 825, 827, 865, 875, 884, 893, 898, 918, 919, 931, 937, 954, 955, 966, 970, 971, 1006, 1009, 1022。",
        ],
        "uses": "药物类别页，用于召回具体药物和耐药边界；优先落到具体药物页面再核验标签。",
    },
    {
        "id": "DRUG-031-macrolides",
        "title": "Macrolides / 大环内酯类",
        "klass": "antimicrobial class",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0071", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 tylosin、tylvalosin、tulathromycin、tilmicosin 等作为大环内酯类候选，主要命中支原体、增生性肠炎、猪痢疾、丹毒敏感性和钩端螺旋体语境。",
            "候选页码：PDF page 185, 186, 812, 865, 884, 893, 898, 899, 931, 983, 1015。",
        ],
        "uses": "药物类别页；不得把类别证据替代具体药物标签。",
    },
    {
        "id": "DRUG-032-pleuromutilins",
        "title": "Pleuromutilins / 截短侧耳素类",
        "klass": "antimicrobial class",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0071", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 tiamulin/valnemulin 作为截短侧耳素类候选，主要命中猪痢疾、Brachyspira 结肠炎、支原体病和增生性肠炎。",
            "候选页码：PDF page 185, 893, 931, 983, 984。",
        ],
        "uses": "药物类别页；需提示与离子载体等相互作用风险。",
    },
    {
        "id": "DRUG-033-aminoglycosides",
        "title": "Aminoglycosides / 氨基糖苷类",
        "klass": "antimicrobial class",
        "sources": ["SRC-0012", "SRC-0063", "SRC-0075", "SRC-0076", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 gentamicin、neomycin、apramycin、spectinomycin 等纳入氨基糖苷相关候选。",
            "候选页码：PDF page 184, 186, 189, 784, 787, 836, 840, 847, 849, 854, 884, 893, 931, 946, 955, 967, 971, 976, 983, 1018, 1020, 1024。",
        ],
        "uses": "药物类别页；必须保留肾/耳毒性、给药途径、食品动物标签和残留边界。",
    },
    {
        "id": "DRUG-034-sulfonamides",
        "title": "Sulfonamides / 磺胺类",
        "klass": "antimicrobial class",
        "sources": ["SRC-0012", "SRC-0059", "SRC-0063", "SRC-0070", "SRC-0074", "SRC-0075", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 sulfonamides 和 trimethoprim-sulfonamide combinations 纳入急性呼吸道、大肠杆菌、放线杆菌、葡萄球菌、链球菌和沙门氏菌语境。",
            "候选页码：PDF page 184, 186, 192, 784, 787, 798, 840, 847, 854, 918, 923, 946, 954, 955, 966, 967, 1022。",
        ],
        "uses": "药物类别页；具体成分、组合比例和产品标签需复核。",
    },
    {
        "id": "DRUG-035-beta-lactams",
        "title": "Beta-lactams / β-内酰胺类",
        "klass": "antimicrobial class",
        "sources": ["SRC-0012", "SRC-0065", "SRC-0066", "SRC-0069", "SRC-0075", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将青霉素、氨基青霉素和头孢菌素归入 β-内酰胺类，同时指出支原体无细胞壁、对 β-内酰胺无效这一负向边界。",
            "候选页码：PDF page 184, 186, 875, 893, 971。",
        ],
        "uses": "药物类别页；可用于抗菌谱边界和支原体误用识别。",
    },
    {
        "id": "DRUG-036-lincosamides",
        "title": "Lincosamides / 林可酰胺类",
        "klass": "antimicrobial class",
        "sources": ["SRC-0012", "SRC-0069", "SRC-0077", "A0-MOA-BANNED-DRUG-250-NOTICE"],
        "evidence": [
            "教材候选表将 lincomycin 作为林可酰胺代表，命中支原体病、猪痢疾和丹毒敏感性语境。",
            "候选页码：PDF page 184, 186, 893, 983, 984。",
        ],
        "uses": "药物类别页；用于关联林可霉素和组合制剂候选。",
    },
]


EXTRA_SOURCES = [
    [
        "A0-MOA-BANNED-DRUG-250-NOTICE",
        "农业农村部公告第250号 食品动物中禁止使用的药品及其他化合物清单",
        "2019-12-27",
        "NEEDS_REVIEW",
        "wiki/sources/A0-MOA-BANNED-DRUG-250-NOTICE.md",
    ],
    [
        "A0-MOA-WITHDRAWAL-278",
        "农业部公告第278号 兽药停药期规定",
        "2003-05-22",
        "NEEDS_REVIEW",
        "wiki/sources/A0-MOA-WITHDRAWAL-278.md",
    ],
]


def source_page(source_id: str, title: str, url: str, date: str, summary: str) -> str:
    return f"""---
type: source
source_id: {source_id}
source_path: {url}
source_type: url
authority_level: official
evidence_status: NEEDS_REVIEW
created: {NOW}
updated: {NOW}
sources: []
---

# {title}

## 来源

- URL: {url}
- 发布/生效日期：{date}
- 录入批次：drug candidate backfill 2026-05-07。

## 摘要

{summary}

## 使用边界

- 本来源仅作为中国官方法规/公告入口；具体药物条目、剂型、产品批准文号、适应证和休药期仍需逐项复核。
- 不得把教材剂量、美国标签或本页摘要直接外推成中国处方。
"""


def drug_page(row: dict[str, object]) -> str:
    source_list = ", ".join(str(x) for x in row["sources"])
    evidence = "\n".join(f"- {line}" for line in row["evidence"])
    return f"""---
tags: [drug, swine, v7, evidence_only, needs_review]
drug_id: {row["id"]}
updated: {NOW}
evidence_status: NEEDS_REVIEW
jurisdiction: Global
sources: [{source_list}]
candidate_source: issues/drug_pdf_candidate_extraction_2026-05-07.md
---

# {row["title"]}

## 证据状态

- 页面类型：`evidence_only` + `NEEDS_REVIEW`。
- 本页来自教材 PDF 候选抽取和有限权威来源入口整理，用于扩大 drug 检索覆盖面。
- 未完成中国批准产品、说明书、休药期、禁限用和药敏证据逐项复核前，不得生成处方、剂量、疗程或中国合规承诺。

## 药物类别

- {row["klass"]}

## 教材候选证据

{evidence}

## 疾病/用途候选

- {row["uses"]}

## 中国合规复核边界

- 食品动物禁用药边界以农业农村部公告第250号原文及后续有效公告为准。
- 休药期不得由教材、美国标签或同类药外推；必须核验中国现行兽药标签、批准文号、公告或兽医处方依据。
- 涉及抗菌药时，应优先建议病原诊断、药敏试验、病程阶段判断和兽医处方路径。

## V7 生成可用边界

- 可用于题型：药物候选召回、同类药识别、误用/越界识别、要求用户提供标签或公告的追问。
- 不可用于题型：剂量、给药途径、疗程、联合用药、群体投药、休药期、残留合格承诺或替代法定疫病报告。
"""


def main() -> None:
    write_text(
        WIKI / "wiki" / "sources" / "A0-MOA-BANNED-DRUG-250-NOTICE.md",
        source_page(
            "A0-MOA-BANNED-DRUG-250-NOTICE",
            "农业农村部公告第250号 食品动物中禁止使用的药品及其他化合物清单",
            "https://www.moa.gov.cn/govpublic/xmsyj/202001/t20200106_6334375.htm",
            "2019-12-27；2020-01-06发布",
            "农业农村部公告第250号发布食品动物中禁止使用的药品及其他化合物清单，并说明原农业部公告第193号、235号、560号等文件中的相关内容同时废止。",
        ),
    )
    write_text(
        WIKI / "wiki" / "sources" / "A0-MOA-WITHDRAWAL-278.md",
        source_page(
            "A0-MOA-WITHDRAWAL-278",
            "农业部公告第278号 兽药国家标准和专业标准中部分品种停药期规定",
            "https://www.moa.gov.cn/nybgb/2003/snqi/201711/t20171126_5919564.htm",
            "2003-05-22",
            "农业部公告第278号是部分兽药停药期规定的官方入口，可作为历史法规/公告检索锚点；现行有效性、修订和具体产品标签仍需复核。",
        ),
    )

    for row in DRUGS:
        write_text(WIKI / "wiki" / "drugs" / f"{row['id']}.md", drug_page(row))

    index_path = WIKI / "exports" / "drug_page_index.csv"
    existing = read_csv(index_path)
    header = existing[0]
    rows = existing[1:]
    by_id = {row[0]: row for row in rows if row}
    for row in DRUGS:
        by_id[row["id"]] = [
            row["id"],
            row["title"],
            "evidence_only_needs_review",
            f"wiki/drugs/{row['id']}.md",
        ]
    sorted_rows = sorted(by_id.values(), key=lambda item: item[0])
    write_csv(index_path, [header] + sorted_rows)

    source_index_path = WIKI / "exports" / "source_index.csv"
    source_rows = read_csv(source_index_path)
    source_header = source_rows[0]
    source_by_id = {row[0]: row for row in source_rows[1:] if row}
    for row in EXTRA_SOURCES:
        source_by_id[row[0]] = row
    write_csv(source_index_path, [source_header] + sorted(source_by_id.values(), key=lambda item: item[0]))

    issue = WIKI / "issues" / "drug_candidate_ingest_assessment_2026-05-07.md"
    write_text(
        issue,
        f"""# Drug Candidate Ingest Assessment - 2026-05-07

## 本次处理

- 从 `issues/drug_pdf_candidate_extraction_2026-05-07.md` 中评估并落地药物候选页。
- 新增 drug 页面：{len(DRUGS)} 个，范围为 `DRUG-009` 到 `DRUG-036`。
- 更新索引：`exports/drug_page_index.csv`。
- 新增官方来源入口：`A0-MOA-BANNED-DRUG-250-NOTICE`、`A0-MOA-WITHDRAWAL-278`。

## 解析库评估

- 现有候选表已经使用 PyMuPDF 全量扫描，并用 pdfplumber/pdfminer 对关键页做 spot check。
- 三个解析器在 Chapter 10、Chapter 62、Chapter 65-67 的关键药物词命中一致，说明用已有 PDF 解析库可显著提升效率和可复核性。
- 当前中文名出现 mojibake 的候选表不应直接作为中文实体来源；本次中文药名按常用兽药译名人工校正，并保留 `NEEDS_REVIEW`。

## 入库边界

- 新页面全部为 `evidence_only + NEEDS_REVIEW`，用于检索覆盖和后续人工复核。
- 未写入 `exports/knowledge_facts.json`，避免把候选抽取误升级为正式事实。
- 任何剂量、疗程、给药途径、休药期、中国可用性结论，均需中国现行标签/公告/批准文号或兽医处方依据。

## 权威来源入口

- 农业农村部公告第250号：食品动物禁用药清单原文入口。
- 农业部公告第278号：部分兽药停药期规定入口，需核验现行有效性和具体产品标签。
- 教材来源：`Diseases of Swine, 11th Edition` Chapter 10、49-62、65-67 的候选页码。

## 后续复核建议

- 第一优先级：把 `DRUG-009` 到 `DRUG-036` 按中国批准产品、说明书、禁限用状态、休药期来源逐项核验。
- 第二优先级：对 ceftiofur、enrofloxacin、aminoglycosides 等公共卫生重要抗菌药增加硬边界规则卡。
- 第三优先级：把 PDF 页码候选转为结构化 candidate facts，但保持 `NEEDS_REVIEW`，通过人工复核后再升级。
""",
    )

    log_path = WIKI / "log.md"
    log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Wiki Log\n"
    marker = "2026-05-07 drug-backfill"
    if marker not in log_text:
        log_path.write_text(
            log_text.rstrip()
            + "\n\n"
            + f"{marker} | added {len(DRUGS)} evidence_only NEEDS_REVIEW drug candidate pages from Diseases of Swine PDF extraction; updated drug/source indexes; did not mutate authoritative facts.\n",
            encoding="utf-8",
            newline="\n",
        )

    print(f"added_or_updated={len(DRUGS)}")


if __name__ == "__main__":
    main()
