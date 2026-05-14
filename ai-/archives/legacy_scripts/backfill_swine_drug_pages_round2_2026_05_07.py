from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
NOW = "2026-05-07T23:20:00+08:00"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


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
- 录入批次：drug candidate backfill round 2 2026-05-07。

## 摘要

{summary}

## 使用边界

- 本页仅作为中国官方法规/公告入口；具体条款、适用动物、剂型、用途和现行有效性仍需逐项核验。
- 命中停用、淘汰或禁用边界的药物不得进入“可用治疗药”结论。
"""


SOURCES = [
    [
        "A0-MOA-STOP-FLUOROQUINOLONES-2292",
        "农业部公告第2292号 洛美沙星等4种原料药及制剂停止用于食品动物",
        "2015-09-01",
        "NEEDS_REVIEW",
        "wiki/sources/A0-MOA-STOP-FLUOROQUINOLONES-2292.md",
    ],
    [
        "A0-MOA-STOP-OLAQUINDOX-2638",
        "农业农村部关于喹乙醇、氨苯胂酸、洛克沙胂等停止用于食品动物的政策入口",
        "2018-01-19",
        "NEEDS_REVIEW",
        "wiki/sources/A0-MOA-STOP-OLAQUINDOX-2638.md",
    ],
    [
        "A0-MOA-ELIMINATED-DRUGS-839",
        "农业部公告第839号 淘汰兽药品种目录",
        "2007-04-04",
        "NEEDS_REVIEW",
        "wiki/sources/A0-MOA-ELIMINATED-DRUGS-839.md",
    ],
    [
        "A0-MOA-MRL-GB31650-2019",
        "GB 31650-2019 食品中兽药最大残留限量官方入口",
        "2019-09-06",
        "NEEDS_REVIEW",
        "wiki/sources/A0-MOA-MRL-GB31650-2019.md",
    ],
]


DRUGS = [
    ("DRUG-037-sulfamethazine", "Sulfamethazine / 磺胺二甲嘧啶", "sulfonamide", "PDF page 184", "猪抗菌药概述和疾病预防候选语境。", "常规法规复核。"),
    ("DRUG-038-trimethoprim-sulfadiazine", "Trimethoprim + sulfadiazine / 甲氧苄啶-磺胺嘧啶", "potentiated sulfonamide", "PDF page 787, 947", "Actinobacillus suis 和沙门氏菌病参考语境。", "具体组合、剂型和休药期需中国标签核验。"),
    ("DRUG-039-sulfadimethoxine", "Sulfadimethoxine / 磺胺二甲氧嘧啶", "sulfonamide", "PDF page 787", "Actinobacillus suis 后续治疗候选语境。", "常规法规复核。"),
    ("DRUG-040-trimethoprim-sulfamethoxazole", "Trimethoprim + sulfamethoxazole / 甲氧苄啶-磺胺甲噁唑", "potentiated sulfonamide", "PDF page 784, 954", "胸膜肺炎放线杆菌敏感性、葡萄球菌病候选语境。", "具体产品和靶动物需核验。"),
    ("DRUG-041-sulfadimidine-sulfathiazole-combinations", "Trimethoprim + sulfadimidine + sulfathiazole / 甲氧苄啶-磺胺二甲嘧啶-磺胺噻唑组合", "potentiated sulfonamide mix", "PDF page 854", "膀胱炎/肾盂肾炎和泌尿道大肠杆菌病候选语境。", "组合制剂需逐项核验批准标签。"),
    ("DRUG-042-ampicillin", "Ampicillin / 氨苄西林", "beta-lactam / aminopenicillin", "PDF page 184, 787, 840, 955", "Actinobacillus suis、大肠杆菌病和葡萄球菌病语境。", "常规法规复核。"),
    ("DRUG-043-amoxicillin-clavulanic-acid", "Amoxicillin/clavulanic acid / 阿莫西林克拉维酸", "beta-lactam + beta-lactamase inhibitor", "PDF page 847", "肠道大肠杆菌/仔猪大肠杆菌病候选语境。", "复方制剂需核验猪用批准和休药期。"),
    ("DRUG-044-cefquinome", "Cefquinome / 头孢喹肟", "fourth-generation cephalosporin", "PDF page 784", "胸膜肺炎放线杆菌敏感性语境。", "高重要抗菌药，必须药敏和标签复核。"),
    ("DRUG-045-tilmicosin", "Tilmicosin / 替米考星", "macrolide", "PDF page 185, 186, 784, 918", "胸膜肺炎放线杆菌/巴氏杆菌等呼吸道候选语境，教材提示注射安全风险。", "高风险，需明确剂型、途径和安全边界。"),
    ("DRUG-046-valnemulin", "Valnemulin / 沃尼妙林", "pleuromutilin", "PDF page 893, 983, 984, 990", "支原体、猪痢疾和 Brachyspira 结肠炎候选语境。", "需提示离子载体相互作用和中国标签核验。"),
    ("DRUG-047-chloramphenicol", "Chloramphenicol / 氯霉素", "phenicol", "PDF page 185", "教材将其作为毒性/食品动物禁用边界提及。", "禁用/高风险边界，命中不得作为可用治疗药。"),
    ("DRUG-048-carbadox", "Carbadox / 卡巴氧", "quinoxaline", "PDF page 185, 931, 978, 983, 990", "增生性肠炎、猪痢疾/Brachyspira 历史用药语境。", "高风险，需按中国禁用/停用/淘汰清单复核。"),
    ("DRUG-049-olaquindox", "Olaquindox / 喹乙醇", "quinoxaline", "PDF page 983, 990", "猪痢疾治疗/预防和 B. pilosicoli 预防历史语境。", "中国食品动物停用高风险项，不作为可用治疗药。"),
    ("DRUG-050-dimetridazole-ronidazole", "Dimetridazole / Ronidazole / 二甲硝咪唑/罗硝唑", "nitroimidazoles", "PDF page 983, 990", "猪痢疾/Brachyspira 历史治疗和预防语境。", "硝基咪唑类高风险禁用边界，需第250号清单核验。"),
    ("DRUG-051-danofloxacin-marbofloxacin", "Danofloxacin / Marbofloxacin / 达氟沙星/马波沙星", "fluoroquinolones", "PDF page 784, 971", "胸膜肺炎放线杆菌敏感性和链球菌 MIC 语境。", "氟喹诺酮类高重要抗菌药，需法规和标签双重核验。"),
    ("DRUG-052-colistin", "Colistin / 黏菌素", "polymyxin", "PDF page 189, 849, 932", "大肠杆菌预防和增生性肠炎疫苗兼容性语境。", "促生长用途退出和抗菌药审慎边界需复核。"),
    ("DRUG-053-bacitracin-methylene-disalicylate", "Bacitracin methylene disalicylate / 亚甲基双水杨酸杆菌肽", "polypeptide antibiotic", "PDF page 820", "围产母猪用药降低梭菌感染风险候选语境。", "具体用途、剂型和饲料添加边界需核验。"),
    ("DRUG-054-virginiamycin", "Virginiamycin / 维吉尼亚霉素", "streptogramin", "PDF page 932, 983", "猪痢疾历史用药和增生性肠炎疫苗兼容性语境。", "饲料添加和抗菌药审慎边界需复核。"),
    ("DRUG-055-moxidectin", "Moxidectin / 莫昔克丁", "macrocyclic lactone antiparasitic", "PDF page 1031", "疥螨/虱和广谱抗寄生虫语境。", "具体产品标签和休药期需核验。"),
    ("DRUG-056-levamisole", "Levamisole / 左旋咪唑", "imidazothiazole anthelmintic", "PDF page 192", "饮水给药驱虫候选语境。", "剂量/饮水方案不得由教材外推。"),
    ("DRUG-057-piperazine-pyrantel", "Piperazine / Pyrantel tartrate / 哌嗪/酒石酸噻嘧啶", "anthelmintics", "PDF page 192", "内寄生虫和饲料预防性驱虫候选语境。", "需核验具体品种、剂型和标签。"),
    ("DRUG-058-amitraz", "Amitraz / 双甲脒", "ectoparasiticide", "PDF page 1031-1032", "疥螨、虱、蜱、蝇蛆等外寄生虫控制语境。", "外用/环境处理标签和食品动物安全边界需核验。"),
    ("DRUG-059-phosmet-coumaphos", "Phosmet / Coumaphos / 伏杀硫磷/蝇毒磷", "organophosphate ectoparasiticides", "PDF page 1031-1032", "外寄生虫和环境处理候选语境。", "有机磷类高安全风险，需中国禁限用和残留核验。"),
    ("DRUG-060-permethrin-deltamethrin", "Permethrin / Deltamethrin / 氯菊酯/溴氰菊酯", "pyrethroid ectoparasiticides", "PDF page 1031-1032", "外寄生虫、蜱、蝇和环境处理语境。", "外用和环境用产品不能外推为体内治疗。"),
    ("DRUG-061-ponazuril", "Ponazuril / 泊那珠利", "triazinone anticoccidial", "PDF page 1045", "弓形虫相关化合物语境，由相关化合物证据推断，证据弱于 toltrazuril。", "NEEDS_REVIEW，不作为猪场常规治疗结论。"),
    ("DRUG-062-amprolium", "Amprolium HCl / 盐酸氨丙啉", "anticoccidial", "PDF page 1043", "母猪/猪场球虫研究语境。", "需标签复核。"),
    ("DRUG-063-meloxicam", "Meloxicam / 美洛昔康", "NSAID", "PDF page 48, 52, 193, 202, 355, 946", "去势/跛行疼痛、呼吸道疾病辅助和炎症语境。", "支持治疗，不替代病原治疗；需标签和休药期核验。"),
    ("DRUG-064-flunixin-meglumine", "Flunixin meglumine / 氟尼辛葡甲胺", "NSAID", "PDF page 52, 193, 209", "疼痛/跛行、猪呼吸道疾病发热和休克支持语境。", "支持治疗，需标签和休药期核验。"),
    ("DRUG-065-ketoprofen-sodium-salicylate-indomethacin", "Ketoprofen / Sodium salicylate / Indomethacin / 酮洛芬/水杨酸钠/吲哚美辛", "NSAIDs", "PDF page 193", "猪抗炎干预研究语境。", "研究/类别候选，不能直接处方外推。"),
    ("DRUG-066-dexamethasone", "Dexamethasone / 地塞米松", "corticosteroid", "PDF page 193, 209", "抗炎和母猪手术休克支持语境。", "激素类支持治疗，需诊断、禁忌和标签复核。"),
    ("DRUG-067-oxytocin", "Oxytocin / 缩宫素", "hormone", "PDF page 192, 342-355, 399, 406", "分娩和泌乳支持语境。", "繁殖管理用药需兽医诊断和标签复核。"),
    ("DRUG-068-altrenogest", "Altrenogest / 烯丙孕素", "progestin", "PDF page 397-398", "繁殖管理和卵巢功能障碍语境。", "繁殖管理药物，需产品标签和食品动物边界复核。"),
    ("DRUG-069-triptorelin", "Triptorelin / 曲普瑞林", "GnRH agonist", "PDF page 193", "断奶母猪排卵提前/同期化语境。", "繁殖管理药物，需标签复核。"),
    ("DRUG-070-ractopamine", "Ractopamine / 莱克多巴胺", "beta-agonist repartitioning agent", "PDF page 193", "部分国家用于饲料效率/瘦肉率的饲料添加剂语境。", "中国和出口市场高度敏感，不作为可用治疗药。"),
]


def drug_page(drug_id: str, title: str, klass: str, pages: str, use: str, reg: str) -> str:
    high = any(term in title.lower() for term in ["chloramphenicol", "carbadox", "olaquindox", "dimetridazole", "ronidazole", "ractopamine"])
    sources = ["SRC-0012", "A0-MOA-BANNED-DRUG-250-NOTICE"]
    if "fluoroquinolone" in klass:
        sources.append("A0-MOA-STOP-FLUOROQUINOLONES-2292")
    if "Olaquindox" in title:
        sources.append("A0-MOA-STOP-OLAQUINDOX-2638")
    if high:
        sources.append("A0-MOA-ELIMINATED-DRUGS-839")
    source_list = ", ".join(dict.fromkeys(sources))
    tag = "prohibited_boundary" if high else "needs_review"
    return f"""---
tags: [drug, swine, v7, evidence_only, {tag}]
drug_id: {drug_id}
updated: {NOW}
evidence_status: NEEDS_REVIEW
jurisdiction: Global
sources: [{source_list}]
candidate_source: subagent_pdf_candidate_scan_2026-05-07
---

# {title}

## 证据状态

- 页面类型：`evidence_only` + `NEEDS_REVIEW`。
- 本页来自 Diseases of Swine 11e PDF 二次候选抽取，用于补齐被药物大类吞掉的具体药物名。
- 未完成中国批准产品、禁限用、停用/淘汰、残留限量、说明书和休药期复核前，不得生成处方、剂量、疗程或中国合规承诺。

## 药物类别

- {klass}

## 教材候选证据

- 候选页码：{pages}。
- PDF 语境：{use}

## 中国合规复核边界

- {reg}
- 先跑中国禁用/停用/淘汰清单，再核验国家兽药基础数据库、现行说明书、靶动物、适应证、给药途径和休药期。
- 国际教材、美国标签或历史用药语境不能替代中国合规结论。

## V7 生成可用边界

- 可用于题型：候选召回、禁限用/停用风险识别、同类药边界、要求用户提供官方标签或公告。
- 不可用于题型：剂量、疗程、给药途径、群体投药、休药期、残留合格承诺或“可用于中国猪场”的结论。
"""


def main() -> None:
    write_text(
        WIKI / "wiki" / "sources" / "A0-MOA-STOP-FLUOROQUINOLONES-2292.md",
        source_page(
            "A0-MOA-STOP-FLUOROQUINOLONES-2292",
            "农业部公告第2292号 洛美沙星等4种原料药及制剂停止用于食品动物",
            "https://www.moa.gov.cn/govpublic/SYJ/201509/t20150907_4819267.htm",
            "2015-09-01",
            "官方停用边界入口，用于洛美沙星、培氟沙星、氧氟沙星、诺氟沙星等食品动物停用药物识别。",
        ),
    )
    write_text(
        WIKI / "wiki" / "sources" / "A0-MOA-STOP-OLAQUINDOX-2638.md",
        source_page(
            "A0-MOA-STOP-OLAQUINDOX-2638",
            "喹乙醇、氨苯胂酸、洛克沙胂停止用于食品动物政策入口",
            "https://www.moa.gov.cn/xw/zwdt/201801/t20180119_6135358.htm",
            "2018-01-19",
            "农业农村部政策入口，用于喹乙醇、氨苯胂酸、洛克沙胂等食品动物停用边界识别。",
        ),
    )
    write_text(
        WIKI / "wiki" / "sources" / "A0-MOA-ELIMINATED-DRUGS-839.md",
        source_page(
            "A0-MOA-ELIMINATED-DRUGS-839",
            "农业部公告第839号 淘汰兽药品种目录",
            "https://www.moa.gov.cn/gk/tzgg_1/gg/200704/t20070412_801731.htm",
            "2007-04-04",
            "淘汰兽药品种目录入口，用于识别不得再生产、经营和使用的兽药品种/剂型。",
        ),
    )
    write_text(
        WIKI / "wiki" / "sources" / "A0-MOA-MRL-GB31650-2019.md",
        source_page(
            "A0-MOA-MRL-GB31650-2019",
            "GB 31650-2019 食品中兽药最大残留限量官方入口",
            "https://www.moa.gov.cn/xw/zwdt/201910/t20191008_6329518.htm",
            "2019-09-06",
            "食品中兽药最大残留限量官方入口，用于残留限量和不得检出边界检索；不能替代具体药物标签和休药期。",
        ),
    )

    for drug_id, title, klass, pages, use, reg in DRUGS:
        write_text(WIKI / "wiki" / "drugs" / f"{drug_id}.md", drug_page(drug_id, title, klass, pages, use, reg))

    drug_index = WIKI / "exports" / "drug_page_index.csv"
    rows = read_csv(drug_index)
    header = rows[0]
    by_id = {row[0]: row for row in rows[1:] if row}
    for drug_id, title, *_ in DRUGS:
        status = "prohibited_boundary_needs_review" if drug_id in {"DRUG-047-chloramphenicol", "DRUG-048-carbadox", "DRUG-049-olaquindox", "DRUG-050-dimetridazole-ronidazole", "DRUG-070-ractopamine"} else "evidence_only_needs_review"
        by_id[drug_id] = [drug_id, title, status, f"wiki/drugs/{drug_id}.md"]
    write_csv(drug_index, [header] + sorted(by_id.values(), key=lambda x: x[0]))

    source_index = WIKI / "exports" / "source_index.csv"
    rows = read_csv(source_index)
    header = rows[0]
    by_id = {row[0]: row for row in rows[1:] if row}
    for row in SOURCES:
        by_id[row[0]] = row
    write_csv(source_index, [header] + sorted(by_id.values(), key=lambda x: x[0]))

    report = WIKI / "issues" / "drug_candidate_ingest_assessment_round2_2026-05-07.md"
    write_text(
        report,
        f"""# Drug Candidate Ingest Assessment Round 2 - 2026-05-07

## 本次处理

- 根据并发 PDF 子任务二次抽取结果，新增 `DRUG-037` 到 `DRUG-070`，共 {len(DRUGS)} 个页面。
- 重点补齐被药物大类掩盖的具体药物名、复方组合、历史用药和高风险/禁用边界项。
- 更新 `exports/drug_page_index.csv` 和 `exports/source_index.csv`。

## 高风险边界

- `DRUG-047-chloramphenicol`、`DRUG-048-carbadox`、`DRUG-049-olaquindox`、`DRUG-050-dimetridazole-ronidazole`、`DRUG-070-ractopamine` 标记为 `prohibited_boundary` 或高风险候选。
- 这些页面只用于禁用/停用/风险识别，不作为可用治疗药。

## 解析结论

- PyMuPDF 对正文候选召回效率最高；pdfplumber 对该 PDF 表格线识别有限，适合作为文本 spot check，不适合作为唯一表格来源。
- 建议后续把候选词典拆成：抗菌药、驱虫/外寄生虫、抗球虫、NSAID/支持治疗、繁殖管理药、高风险禁用边界六类。

## 未升级事项

- 未写入 `exports/knowledge_facts.json`。
- 未生成剂量、疗程、给药途径或休药期。
- 未把国外/教材标签外推为中国可用结论。
""",
    )

    log_path = WIKI / "log.md"
    log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Wiki Log\n"
    marker = "2026-05-07 drug-backfill-round2"
    if marker not in log_text:
        log_path.write_text(
            log_text.rstrip()
            + "\n\n"
            + f"{marker} | added {len(DRUGS)} additional evidence_only NEEDS_REVIEW drug candidate/boundary pages from second PDF scan; updated indexes only.\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"added_or_updated={len(DRUGS)}")


if __name__ == "__main__":
    main()
