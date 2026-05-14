from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = PROJECT_ROOT / "knowledge" / "llm_wiki_swine_authoritative"
PDF_PATH = (
    "docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman, "
    "Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
)


def slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return text or "swine-disease"


def main() -> None:
    updated = datetime.now(timezone.utc).isoformat()
    items = [
        ("猪腺病毒感染", "Adenoviruses", "病毒病", "Section III Viral Diseases", 24, 462, "extended", False),
        ("非洲猪瘟", "African Swine Fever Virus", "病毒病", "Section III Viral Diseases", 25, 467, "core", True),
        ("猪环曲病毒/托克特诺病毒感染", "Anelloviruses / Torque teno sus viruses", "病毒病", "Section III Viral Diseases", 26, 477, "extended", False),
        ("猪星状病毒感染", "Astroviruses", "病毒病", "Section III Viral Diseases", 27, 481, "extended", False),
        ("猪布尼亚病毒相关感染", "Bunyaviruses: Akabane, Lumbo, Oya, Tahyna", "病毒病", "Section III Viral Diseases", 28, 485, "extended", False),
        ("猪杯状病毒感染", "Caliciviruses: norovirus, sapovirus, vesicular exanthema virus", "病毒病", "Section III Viral Diseases", 29, 488, "extended", False),
        ("猪圆环病毒相关疾病", "Circoviruses / PCVAD", "病毒病", "Section III Viral Diseases", 30, 497, "core", False),
        ("猪流行性腹泻", "Porcine epidemic diarrhea virus", "病毒病", "Section III Viral Diseases", 31, 512, "core", False),
        ("猪传染性胃肠炎", "Transmissible gastroenteritis virus", "病毒病", "Section III Viral Diseases", 31, 512, "core", False),
        ("猪δ冠状病毒感染", "Porcine deltacoronavirus", "病毒病", "Section III Viral Diseases", 31, 512, "core", False),
        ("猪血凝性脑脊髓炎", "Hemagglutinating encephalomyelitis virus", "病毒病", "Section III Viral Diseases", 31, 512, "extended", False),
        ("猪呼吸道冠状病毒感染", "Porcine respiratory coronavirus", "病毒病", "Section III Viral Diseases", 31, 512, "extended", False),
        ("猪托罗病毒感染", "Porcine torovirus", "病毒病", "Section III Viral Diseases", 31, 512, "extended", False),
        ("猪丝状病毒相关感染", "Filoviruses: Reston ebolavirus, Zaire ebolavirus", "病毒病/人兽共患风险", "Section III Viral Diseases", 32, 548, "review", True),
        ("猪乙型脑炎", "Japanese encephalitis virus", "病毒病/繁殖障碍", "Section III Viral Diseases", 33, 554, "core", True),
        ("猪西尼罗病毒相关感染", "West Nile virus and other flaviviruses", "病毒病", "Section III Viral Diseases", 33, 554, "extended", False),
        ("猪戊型肝炎", "Hepatitis E Virus", "病毒病/人兽共患风险", "Section III Viral Diseases", 34, 568, "extended", False),
        ("猪伪狂犬病", "Pseudorabies / Aujeszky disease", "病毒病", "Section III Viral Diseases", 35, 572, "core", True),
        ("猪巨细胞病毒感染", "Porcine cytomegalovirus", "病毒病", "Section III Viral Diseases", 35, 572, "extended", False),
        ("猪恶性卡他热相关感染", "Malignant catarrhal fever / ovine herpesvirus 2", "病毒病", "Section III Viral Diseases", 35, 572, "extended", False),
        ("猪流感", "Influenza Viruses", "病毒病/呼吸道病", "Section III Viral Diseases", 36, 600, "core", False),
        ("猪副黏病毒相关感染", "Paramyxoviruses", "病毒病", "Section III Viral Diseases", 37, 618, "extended", False),
        ("猪细小病毒病", "Parvoviruses", "病毒病/繁殖障碍", "Section III Viral Diseases", 38, 635, "core", False),
        ("猪瘟", "Classical Swine Fever / Pestiviruses", "病毒病", "Section III Viral Diseases", 39, 646, "core", True),
        ("非典型猪瘟病毒感染", "Atypical porcine pestivirus / pestivirus infections", "病毒病", "Section III Viral Diseases", 39, 646, "extended", False),
        ("猪口蹄疫", "Foot-and-mouth disease / Picornaviruses", "病毒病", "Section III Viral Diseases", 40, 665, "core", True),
        ("塞内卡病毒A感染", "Senecavirus A / Picornaviruses", "病毒病/水疱病鉴别", "Section III Viral Diseases", 40, 665, "core", True),
        ("猪繁殖与呼吸综合征", "Porcine Reproductive and Respiratory Syndrome Viruses", "病毒病", "Section III Viral Diseases", 41, 709, "core", True),
        ("猪痘", "Swinepox Virus", "病毒病/皮肤病", "Section III Viral Diseases", 42, 733, "extended", False),
        ("猪轮状病毒病", "Rotaviruses and Reoviruses", "病毒病/腹泻病", "Section III Viral Diseases", 43, 739, "core", False),
        ("猪反转录病毒相关感染", "Retroviruses", "病毒病", "Section III Viral Diseases", 44, 752, "review", False),
        ("猪狂犬病风险", "Rabies virus", "病毒病/人兽共患风险", "Section III Viral Diseases", 45, 757, "review", True),
        ("猪水疱性口炎", "Vesicular stomatitis viruses", "病毒病/水疱病鉴别", "Section III Viral Diseases", 45, 757, "core", True),
        ("猪甲病毒相关感染", "Togaviruses: Getah, Sagiyama, Ross River, EEE", "病毒病", "Section III Viral Diseases", 46, 764, "extended", False),
        ("猪胸膜肺炎", "Actinobacillus pleuropneumoniae pleuropneumonia", "细菌病/呼吸道病", "Section IV Bacterial Diseases", 48, 773, "core", False),
        ("猪放线杆菌败血症", "Actinobacillus suis septicemia/pleuropneumonia", "细菌病", "Section IV Bacterial Diseases", 48, 773, "extended", False),
        ("猪萎缩性鼻炎", "Bordetella bronchiseptica nonprogressive atrophic rhinitis", "细菌病/呼吸道病", "Section IV Bacterial Diseases", 49, 791, "core", False),
        ("猪布鲁氏菌病", "Brucella suis brucellosis", "细菌病/繁殖障碍/人兽共患风险", "Section IV Bacterial Diseases", 50, 802, "core", True),
        ("仔猪梭菌性肠炎", "Clostridial diseases", "细菌病/肠道病", "Section IV Bacterial Diseases", 51, 816, "core", False),
        ("猪大肠杆菌病", "Colibacillosis", "细菌病/肠道病", "Section IV Bacterial Diseases", 52, 831, "core", False),
        ("仔猪黄白痢", "Neonatal/post-weaning colibacillosis", "细菌病/腹泻病", "Section IV Bacterial Diseases", 52, 831, "core", False),
        ("仔猪水肿病", "Edema disease / E. coli", "细菌病/神经水肿综合征", "Section IV Bacterial Diseases", 52, 831, "core", False),
        ("猪丹毒", "Erysipelas", "细菌病/败血症/皮肤关节病", "Section IV Bacterial Diseases", 53, 859, "core", False),
        ("副猪嗜血杆菌病", "Glässer’s disease", "细菌病/多发性浆膜炎", "Section IV Bacterial Diseases", 54, 868, "core", False),
        ("猪钩端螺旋体病", "Leptospirosis", "细菌病/繁殖障碍/人兽共患风险", "Section IV Bacterial Diseases", 55, 878, "core", True),
        ("猪支原体肺炎", "Mycoplasmosis / enzootic pneumonia", "细菌病/呼吸道病", "Section IV Bacterial Diseases", 56, 887, "core", False),
        ("猪多杀性巴氏杆菌病", "Pasteurellosis", "细菌病/呼吸道病", "Section IV Bacterial Diseases", 57, 908, "core", False),
        ("猪增生性肠炎", "Proliferative enteropathy / Lawsonia intracellularis", "细菌病/肠道病", "Section IV Bacterial Diseases", 58, 922, "core", False),
        ("猪沙门氏菌病", "Salmonellosis", "细菌病/肠道病/败血症", "Section IV Bacterial Diseases", 59, 936, "core", False),
        ("猪葡萄球菌病", "Staphylococcosis / exudative epidermitis", "细菌病/皮肤病", "Section IV Bacterial Diseases", 60, 950, "extended", False),
        ("猪链球菌病", "Streptococcosis / Streptococcus suis", "细菌病/脑膜炎/败血症", "Section IV Bacterial Diseases", 61, 958, "core", True),
        ("猪痢疾", "Swine dysentery / Brachyspira hyodysenteriae", "细菌病/肠道病", "Section IV Bacterial Diseases", 62, 975, "core", False),
        ("猪结核病", "Tuberculosis", "细菌病/人兽共患风险", "Section IV Bacterial Diseases", 63, 995, "review", True),
        ("猪杂项细菌感染", "Miscellaneous bacterial infections", "细菌病", "Section IV Bacterial Diseases", 64, 1005, "review", False),
        ("猪疥螨病", "External parasites / mange", "寄生虫病/皮肤病", "Section V Parasitic Diseases", 65, 1029, "core", False),
        ("猪虱病", "External parasites / lice", "寄生虫病/皮肤病", "Section V Parasitic Diseases", 65, 1029, "extended", False),
        ("猪球虫病", "Coccidia and other protozoa", "寄生虫病/腹泻病", "Section V Parasitic Diseases", 66, 1039, "core", False),
        ("猪弓形虫病", "Toxoplasmosis / protozoa", "寄生虫病/人兽共患风险", "Section V Parasitic Diseases", 66, 1039, "core", True),
        ("猪隐孢子虫病", "Cryptosporidiosis / protozoa", "寄生虫病/腹泻病", "Section V Parasitic Diseases", 66, 1039, "extended", False),
        ("猪蛔虫病", "Ascaris suum / internal parasites", "寄生虫病", "Section V Parasitic Diseases", 67, 1052, "core", False),
        ("猪鞭虫病", "Trichuris suis / internal parasites", "寄生虫病/肠道病", "Section V Parasitic Diseases", 67, 1052, "extended", False),
        ("猪类圆线虫病", "Strongyloides / internal parasites", "寄生虫病/腹泻病", "Section V Parasitic Diseases", 67, 1052, "extended", False),
        ("猪后圆线虫病", "Metastrongylus / lungworms", "寄生虫病/呼吸道病", "Section V Parasitic Diseases", 67, 1052, "extended", False),
        ("猪肾虫病", "Stephanurus dentatus / kidney worm", "寄生虫病", "Section V Parasitic Diseases", 67, 1052, "extended", False),
        ("猪营养缺乏与过量综合征", "Nutrient deficiencies and excesses", "非感染性疾病/营养代谢", "Section VI Noninfectious Diseases", 68, 1067, "core", False),
        ("猪霉菌毒素中毒", "Mycotoxins in grains and feeds", "非感染性疾病/中毒病", "Section VI Noninfectious Diseases", 69, 1079, "core", False),
        ("猪黄曲霉毒素中毒", "Aflatoxin toxicosis", "非感染性疾病/中毒病", "Section VI Noninfectious Diseases", 69, 1079, "extended", False),
        ("猪呕吐毒素/DON中毒", "DON / trichothecene toxicosis", "非感染性疾病/中毒病", "Section VI Noninfectious Diseases", 69, 1079, "extended", False),
        ("猪玉米赤霉烯酮中毒", "Zearalenone toxicosis", "非感染性疾病/繁殖障碍/中毒病", "Section VI Noninfectious Diseases", 69, 1079, "extended", False),
        ("猪富马毒素中毒", "Fumonisin toxicosis", "非感染性疾病/中毒病", "Section VI Noninfectious Diseases", 69, 1079, "extended", False),
        ("猪矿物质与化学物中毒", "Toxic minerals, chemicals, plants, and gases", "非感染性疾病/中毒病", "Section VI Noninfectious Diseases", 70, 1096, "core", False),
        ("猪亚硝酸盐中毒", "Nitrite toxicosis", "非感染性疾病/中毒病", "Section VI Noninfectious Diseases", 70, 1096, "extended", False),
        ("猪有毒气体与通风失败损伤", "Toxic gases / ventilation failure", "非感染性疾病/环境管理", "Section VI Noninfectious Diseases", 70, 1096, "core", False),
    ]

    (WIKI_ROOT / "wiki" / "sources").mkdir(parents=True, exist_ok=True)
    source_page = WIKI_ROOT / "wiki" / "sources" / "SRC-0001-diseases-of-swine-11e-toc.md"
    source_page.write_text(
        f"""---
type: source
source_id: SRC-0001
source_path: {PDF_PATH}
source_type: textbook_pdf_toc
authority_level: textbook
evidence_status: EXTRACTED
created: {updated}
updated: {updated}
sources: []
---

# Diseases of Swine, 11th Edition - TOC Anchor

本来源页仅记录本地 PDF 的目录级证据，用于建立猪病 LLM Wiki 的初始覆盖蓝图。

- 本轮已识别页码范围：PDF page 1-12，其中 page 7-12 为 Contents。
- 本轮未抽取正文诊疗建议、剂量、免疫程序或监管结论。
- 目录证据可用于确认章节存在、章节题名、疾病类别和正文起始页；不能单独作为处方、诊断标准或休药期依据。

## 本地文件

- `{PDF_PATH}`

## 下一步

按章节分批抽取正文，每批完成后更新 `issues/pdf_processing_progress.md` 和对应疾病页。
""",
        encoding="utf-8",
    )

    topics = {
        "Start-here-for-swine-case-triage.md": "猪病问诊分诊入口",
        "Swine-differential-diagnosis-navigation.md": "猪病鉴别诊断导航",
        "Swine-regulatory-reporting-and-quarantine.md": "猪病监管上报、检疫与处置边界",
        "Swine-medication-legality-and-withdrawal.md": "猪用药合规、食品安全与休药期边界",
        "Swine-source-verification-workflow.md": "猪病 Wiki 来源核验工作流",
    }
    for filename, title in topics.items():
        (WIKI_ROOT / "wiki" / "topics" / filename).write_text(
            f"""---
tags: [topic, swine]
updated: {updated}
evidence_status: NEEDS_REVIEW
sources: [SRC-0001]
---

# {title}

本页为猪病 LLM Wiki 初始工作流页。当前仅完成目录级覆盖建模，正式诊断、治疗、免疫、扑杀、上报和休药期规则需要后续正文抽取与 A0/A1 来源复核。

## 使用边界

- 先从 `exports/disease_index.csv` 定位目标病种。
- 监管、强制处置、禁限用药和休药期以中国官方来源为准。
- 目录级教材来源只用于建立覆盖范围，不直接支撑金标答案中的临床断言。
""",
            encoding="utf-8",
        )

    disease_dir = WIKI_ROOT / "wiki" / "diseases"
    disease_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    facts = []
    for idx, (cn, en, cat, section, chapter, page, target, reg) in enumerate(items, start=1):
        did = f"DIS-{idx:03d}"
        rel = f"wiki/diseases/{did}-{slugify(en)}.md"
        status = "needs_cn_regulatory_anchor" if reg else "needs_body_extraction"
        official = "待中国官方来源复核" if reg else "未在本轮目录级处理中确认"
        (WIKI_ROOT / rel).write_text(
            f"""---
tags: [disease, swine, initial]
disease_id: {did}
updated: {updated}
evidence_status: NEEDS_REVIEW
sources: [SRC-0001]
---

# {cn}

## 英文/教材章节名

- {en}

## 病原与分类

- 初始分类：{cat}
- 教材章节：{section}，Chapter {chapter}
- 正文起始页：PDF page {page}

## 中国监管状态

- {official}
- 本页尚未完成 A0/A1 监管来源核验，不能单独用于强制处置、上报、扑杀、免疫或跨区调运结论。

## 典型宿主与阶段

- Applies to species: swine
- 生产阶段、日龄和易感群体待正文抽取。

## 传播途径

- 待正文抽取。

## 临床症状

- 待正文抽取。

## 剖检变化

- 待正文抽取。

## 实验室诊断

- 待正文抽取；涉及法定疫病时需补充中国标准、WOAH 或官方实验室指南。

## 鉴别诊断

- 待正文抽取；水疱病、急性高热败血症、繁殖障碍、腹泻和呼吸道综合征应建立专题鉴别页。

## 防控要点

- 待正文抽取；涉及疫苗、净化、扑杀、封锁、无害化处理时必须引用监管来源。

## 用药/处置边界

- 待正文抽取和中国兽药合规复核。
- 法定疫病或疑似重大动物疫病不得生成经验性治疗替代确诊/上报/隔离建议。

## 本地证据

- [SRC-0001](../sources/SRC-0001-diseases-of-swine-11e-toc.md) - 本地 PDF 目录级章节锚点。

## 当前可用性边界

- 当前状态：目录级覆盖页。
- 可用于召回目标病种和规划抽取任务；不可作为完整临床知识页。
""",
            encoding="utf-8",
        )
        rows.append(
            {
                "disease_id": did,
                "disease_name": cn,
                "category": cat,
                "official_china_status": official,
                "coverage_target": target,
                "china_standard_required": "yes" if reg else "review",
                "clinical_page_required": "yes",
                "regulatory_anchor_required": "yes" if reg else "review",
                "coverage_gap_status": status,
                "primary_source_id": "SRC-0001",
                "page_relpath": rel,
                "standard_count": "0",
            }
        )
        facts.append(
            {
                "fact_id": f"{did}-toc-category",
                "fact_type": "disease_attribute",
                "subject": cn,
                "predicate": "category",
                "object": cat,
                "fact_confidence": "0.70",
                "evidence_source": "local_textbook_toc",
                "evidence_source_id": "SRC-0001",
                "evidence_url": "",
                "evidence_quote_span": "",
                "evidence_status": "NEEDS_REVIEW",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "Global",
            }
        )
        facts.append(
            {
                "fact_id": f"{did}-toc-page-anchor",
                "fact_type": "source_anchor",
                "subject": cn,
                "predicate": "textbook_chapter_start_page",
                "object": str(page),
                "fact_confidence": "0.75",
                "evidence_source": "local_textbook_toc",
                "evidence_source_id": "SRC-0001",
                "evidence_url": "",
                "evidence_quote_span": "",
                "evidence_status": "NEEDS_REVIEW",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "Global",
            }
        )

    with (WIKI_ROOT / "exports" / "disease_index.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (WIKI_ROOT / "exports" / "rule_index.csv").write_text(
        "rule_id,rule_name,category,priority,evidence_status,primary_source_id,page_relpath\n",
        encoding="utf-8-sig",
    )
    (WIKI_ROOT / "exports" / "drug_page_index.csv").write_text(
        "drug_id,drug_name,category,evidence_status,primary_source_id,page_relpath\n",
        encoding="utf-8-sig",
    )
    (WIKI_ROOT / "exports" / "knowledge_facts.json").write_text(
        json.dumps(facts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    (WIKI_ROOT / "issues" / "pdf_processing_progress.md").write_text(
        f"""# Diseases of Swine PDF 分批处理进度

## 当前状态

- PDF 总页数：1132
- 文件：`{PDF_PATH}`
- 本轮处理：page 1-12
- 本轮有效抽取：page 7-12 Contents；书签 outline 83 条
- 本轮产物：
  - `wiki/sources/SRC-0001-diseases-of-swine-11e-toc.md`
  - `exports/disease_index.csv`
  - `exports/knowledge_facts.json`
  - `wiki/diseases/DIS-001` 到 `DIS-{len(items):03d}` 初始疾病页
  - `wiki/topics/` 初始工作流页

## 截至位置

下一次应从 PDF page 13 开始。

推荐下一批：page 13-24，处理 Contributors、Editors’ Note、Acknowledgments，只记录版本/编辑者/来源元数据，不进入疾病事实。

随后正文批次建议：

- page 25-244：Section I Veterinary Practice，抽取诊疗流程、采样、药理、食品安全、鉴别诊断方法，生成 topic/rule 页。
- page 245-448：Section II Body Systems，抽取系统病和综合征导航，生成 syndrome/topic 页。
- page 449-766：Section III Viral Diseases，按每章建立/完善病毒病 disease 页。
- page 767-1026：Section IV Bacterial Diseases，按每章建立/完善细菌病 disease 页。
- page 1027-1064：Section V Parasitic Diseases，完善寄生虫病 disease 页。
- page 1065-1111：Section VI Noninfectious Diseases，完善营养、中毒、环境管理 disease/syndrome 页。
- page 1112-1132：Index，只用于补别名和交叉引用。

## 质量规则

- 目录级事实全部保持 `NEEDS_REVIEW`，不得作为最终处方、监管、诊断标准依据。
- 正文抽取时只保存摘要和结构化事实，不复制长段原文。
- 每批完成后必须更新本文件的“截至位置”。
""",
        encoding="utf-8",
    )

    (WIKI_ROOT / "README.md").write_text(
        f"""# Swine Disease LLM Wiki

本知识库是 `llm_wiki_chicken_authoritative` 的同构猪病知识库，当前处于 Phase 1/2 初始建设阶段。

- 当前覆盖：{len(items)} 个猪病/综合征/中毒类条目。
- 当前证据：本地 `Diseases of Swine, 11th Edition` PDF 目录级锚点。
- 当前边界：尚未完成正文抽取、中国官方来源核验、药物合规和休药期规则建设。

查看进度：`issues/pdf_processing_progress.md`。
""",
        encoding="utf-8",
    )

    print(json.dumps({"diseases": len(items), "facts": len(facts), "last_processed_page": 12}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
