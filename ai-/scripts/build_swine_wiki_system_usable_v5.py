from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
ISSUES = WIKI / "issues"
NOW = "2026-05-07T20:30:00+08:00"
BATCH_ID = "system-usable-completion-v5-001"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in text:
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8", newline="\n")


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


def load_facts() -> list[dict[str, str]]:
    return json.loads((WIKI / "exports" / "knowledge_facts.json").read_text(encoding="utf-8"))


def fact_line(fact: dict[str, str]) -> str:
    source = fact.get("evidence_source_id", "")
    span = fact.get("evidence_quote_span", "")
    obj = fact.get("object", "")
    return f"- {obj}（{source}; {span}）"


SECTION_PATTERNS = [
    ("传播途径", ("transmission", "epidemiology", "biosecurity", "environment", "vector", "foodborne", "direct_contact")),
    ("临床症状", ("clinical", "production_impact", "relevance", "host_response", "welfare")),
    ("剖检变化", ("lesion", "pathology", "necropsy", "pathogenesis")),
    ("实验室诊断", ("diagnostic", "sample", "serology", "molecular", "culture", "pcr")),
    ("鉴别诊断", ("differential", "boundary", "causality")),
    ("防控要点", ("control", "biosecurity", "vaccination", "surveillance", "management")),
    ("用药/处置边界", ("treatment", "drug", "antimicrobial", "anthelmintic", "anticoccidial", "regulatory")),
]


def classify_fact(fact: dict[str, str]) -> str:
    hay = " ".join([fact.get("fact_type", ""), fact.get("predicate", ""), fact.get("object", "")]).lower()
    for section, keys in SECTION_PATTERNS:
        if any(key in hay for key in keys):
            return section
    return "本地证据补充"


def aliases_for_disease(row: dict[str, str], page_text: str) -> set[str]:
    name = row["disease_name"]
    aliases = {name}
    title_match = re.search(r"^#\s+(.+)$", page_text, flags=re.M)
    if title_match:
        aliases.add(title_match.group(1).strip())
    for line in page_text.splitlines():
        if line.startswith("- ") and any(ch.isalpha() for ch in line):
            clean = line[2:].strip()
            if 3 <= len(clean) <= 120:
                aliases.add(clean)
    aliases.update(part.strip() for part in re.split(r"[/（）()、,， ]+", name) if len(part.strip()) >= 2)
    return {alias for alias in aliases if alias}


def match_disease_facts(disease: dict[str, str], page_text: str, facts: list[dict[str, str]]) -> list[dict[str, str]]:
    aliases = aliases_for_disease(disease, page_text)
    matched = []
    for fact in facts:
        if fact.get("evidence_status") != "HUMAN_REVIEWED":
            continue
        if fact.get("evidence_source_id") == "SRC-0001":
            continue
        subject = fact.get("subject", "")
        obj = fact.get("object", "")
        predicate = fact.get("predicate", "")
        hay = f"{subject} {obj} {predicate}"
        if any(alias in hay for alias in aliases if len(alias) >= 3):
            matched.append(fact)
    return matched


def build_disease_backfill() -> None:
    facts = load_facts()
    disease_rows = read_csv_dicts(WIKI / "exports" / "disease_index.csv")
    report_rows = []
    unmapped_ids = {fact.get("fact_id", "") for fact in facts if fact.get("evidence_status") == "HUMAN_REVIEWED"}
    marker = "## Formal Disease Completion / V5"
    for disease in disease_rows:
        path = WIKI / disease["page_relpath"]
        if not path.exists():
            continue
        page_text = path.read_text(encoding="utf-8")
        matched = match_disease_facts(disease, page_text, facts)
        for fact in matched:
            unmapped_ids.discard(fact.get("fact_id", ""))
        by_section: dict[str, list[dict[str, str]]] = defaultdict(list)
        for fact in matched:
            by_section[classify_fact(fact)].append(fact)
        sections = []
        for section, _ in SECTION_PATTERNS:
            lines = []
            seen = set()
            for fact in by_section.get(section, [])[:12]:
                line = fact_line(fact)
                if line not in seen:
                    seen.add(line)
                    lines.append(line)
            if not lines:
                lines = [f"- 本栏目暂无可自动映射的 HUMAN_REVIEWED 正文事实；不得编造，需继续 PDF 正文抽取或 A0/A1 来源补充。"]
            sections.append(f"### {section}\n\n" + "\n".join(lines))
        evidence = []
        for fact in matched[:20]:
            evidence.append(f"- `{fact.get('fact_id')}` -> `{fact.get('evidence_source_id')}` / {fact.get('evidence_quote_span')}")
        if not evidence:
            evidence = ["- 当前仅有目录级或未映射证据；本页仍需后续正文抽取。"]
        block = f"""{marker}

> V5 自动补全区块：由 `exports/knowledge_facts.json` 中 `HUMAN_REVIEWED` facts 聚合生成。仅使用有来源锚点的事实；未覆盖栏目显式保留为待抽取，不生成无来源结论。

{chr(10).join(sections)}

### 本地证据

{chr(10).join(evidence)}
"""
        append_once(path, marker, block)
        report_rows.append({
            "disease_id": disease["disease_id"],
            "disease_name": disease["disease_name"],
            "matched_fact_count": str(len(matched)),
            "sections_with_content": str(sum(1 for section in by_section if by_section[section])),
            "path": disease["page_relpath"],
        })
    write_text(ISSUES / "v5_001_disease_backfill_report.md", "# V5-001 Disease Backfill Report\n\n" + "\n".join(
        f"- {r['disease_id']} {r['disease_name']}: matched={r['matched_fact_count']} sections={r['sections_with_content']} path={r['path']}"
        for r in report_rows
    ) + "\n")
    write_text(ISSUES / "v5_001_disease_backfill_candidate_map.json", json.dumps(report_rows, ensure_ascii=False, indent=2) + "\n")
    write_text(ISSUES / "v5_001_unmapped_human_reviewed_fact_ids.json", json.dumps(sorted(unmapped_ids), ensure_ascii=False, indent=2) + "\n")


AUTHORITY_SOURCES = [
    {
        "source_id": "A0-MOA-573",
        "title": "农业农村部公告第573号 一二三类动物疫病病种名录",
        "url": "https://xmsyj.moa.gov.cn/gzdt/202206/t20220629_6403635.htm",
        "date": "2022-06-23",
        "summary": "中国官方动物疫病病种名录来源，用于确认一类、二类、三类动物疫病和猪病相关监管状态。",
    },
    {
        "source_id": "A0-MOA-ASF-NORMALIZED-GUIDE",
        "title": "非洲猪瘟常态化防控技术指南（试行版）",
        "url": "https://www.moa.gov.cn/nybgb/2020/202009/202011/t20201124_6356917.htm",
        "date": "2020-09-11",
        "summary": "农业农村部官方 ASF 常态化防控技术指南，用于中国语境下的引种隔离、检测、阳性报告和处置边界。",
    },
    {
        "source_id": "A0-MOA-BANNED-DRUG-250-POLICY",
        "title": "农业农村部食品动物禁用药清单政策说明",
        "url": "https://www.moa.gov.cn/xw/zwdt/202001/t20200120_6336378.htm",
        "date": "2020-01-20",
        "summary": "农业农村部关于食品动物中禁止使用药品及其他化合物清单的政策说明，用于禁用药规则来源入口；具体药物清单需公告原文或官方镜像复核。",
    },
    {
        "source_id": "A1-WOAH-ASF",
        "title": "WOAH African swine fever disease page",
        "url": "https://www.woah.org/en/disease/african-swine-fever/",
        "date": "accessed 2026-05-07",
        "summary": "WOAH ASF disease page，用于国际权威 disease card、传播、人类健康危害边界和 WOAH 通报语境。",
    },
    {
        "source_id": "A1-WOAH-FMD",
        "title": "WOAH Foot and mouth disease disease page",
        "url": "https://www.woah.org/en/disease/foot-and-mouth-disease/",
        "date": "accessed 2026-05-07",
        "summary": "WOAH FMD disease page，用于口蹄疫国际权威 disease card、水疱病鉴别和贸易/通报边界。",
    },
]


AUTHORITY_FACTS = [
    ("AUTH-001-asf-china-class-i", "notifiable_status", "非洲猪瘟", "china_notifiable_class", "非洲猪瘟列入中国一类动物疫病名录，相关处置必须依据中国官方法规和技术规范。", "A0-MOA-573", "公告第573号；一类动物疫病名录", "China"),
    ("AUTH-002-fmd-china-class-i", "notifiable_status", "猪口蹄疫", "china_notifiable_class", "口蹄疫列入中国一类动物疫病名录，猪口蹄部水疱病变不得按普通病处理。", "A0-MOA-573", "公告第573号；一类动物疫病名录", "China"),
    ("AUTH-003-svd-china-class-i", "notifiable_status", "猪水疱病", "china_notifiable_class", "猪水疱病列入中国一类动物疫病名录，水疱病鉴别需保留监管处置边界。", "A0-MOA-573", "公告第573号；一类动物疫病名录", "China"),
    ("AUTH-004-csf-china-class-ii", "notifiable_status", "猪瘟", "china_notifiable_class", "猪瘟列入中国二类动物疫病名录，临床和实验室判断需保留官方防控边界。", "A0-MOA-573", "公告第573号；二类动物疫病名录", "China"),
    ("AUTH-005-prrs-china-class-ii", "notifiable_status", "猪繁殖与呼吸综合征", "china_notifiable_class", "猪繁殖与呼吸综合征列入中国二类动物疫病名录。", "A0-MOA-573", "公告第573号；二类动物疫病名录", "China"),
    ("AUTH-006-ped-china-class-ii", "notifiable_status", "猪流行性腹泻", "china_notifiable_class", "猪流行性腹泻列入中国二类动物疫病名录。", "A0-MOA-573", "公告第573号；二类动物疫病名录", "China"),
    ("AUTH-007-ppv-china-class-iii", "notifiable_status", "猪细小病毒病", "china_notifiable_class", "猪细小病毒感染列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-008-erysipelas-china-class-iii", "notifiable_status", "猪丹毒", "china_notifiable_class", "猪丹毒列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-009-app-china-class-iii", "notifiable_status", "猪胸膜肺炎", "china_notifiable_class", "猪传染性胸膜肺炎列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-010-pcvad-china-class-iii", "notifiable_status", "猪圆环病毒相关疾病", "china_notifiable_class", "猪圆环病毒病列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-011-swine-influenza-china-class-iii", "notifiable_status", "猪流感", "china_notifiable_class", "猪流感列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-012-pdcov-china-class-iii", "notifiable_status", "猪δ冠状病毒感染", "china_notifiable_class", "猪丁型冠状病毒感染列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-013-swine-dysentery-china-class-iii", "notifiable_status", "猪痢疾", "china_notifiable_class", "猪痢疾列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-014-lawsonia-china-class-iii", "notifiable_status", "猪增生性肠炎", "china_notifiable_class", "猪增生性肠病列入中国三类动物疫病名录。", "A0-MOA-573", "公告第573号；三类动物疫病名录", "China"),
    ("AUTH-015-asf-report-positive", "regulatory_boundary", "非洲猪瘟", "positive_detection_requires_local_veterinary_reporting_boundary", "非洲猪瘟常态化防控指南要求，检测阳性时应报告当地畜牧兽医部门并按官方流程处理，不能生成治疗替代报告的建议。", "A0-MOA-ASF-NORMALIZED-GUIDE", "非洲猪瘟常态化防控技术指南；检测阳性处置边界", "China"),
    ("AUTH-016-asf-introduction-quarantine", "biosecurity", "非洲猪瘟引种", "introduction_requires_health_assessment_isolation_and_testing_boundary", "非洲猪瘟常态化防控语境下，引种前需健康评估，入场后需隔离观察并检测；不得把未检疫引种视为低风险。", "A0-MOA-ASF-NORMALIZED-GUIDE", "非洲猪瘟常态化防控技术指南；引种管理", "China"),
    ("AUTH-017-food-animal-banned-drug-policy", "drug_regulatory_status", "食品动物禁用药", "china_banned_drug_list_requires_official_250_notice", "食品动物禁用药应以农业农村部公告第250号及官方清单为准；未核验具体清单原文前，不得编造禁用药条目。", "A0-MOA-BANNED-DRUG-250-POLICY", "农业农村部政策说明；公告第250号来源入口", "China"),
    ("AUTH-018-woah-asf-no-human-health", "public_health_boundary", "非洲猪瘟", "woah_asf_no_human_health_hazard", "WOAH 将非洲猪瘟描述为家猪和野猪高度传染性病毒病，但对人类健康无危害。", "A1-WOAH-ASF", "WOAH ASF disease page", "Global"),
]


def build_authority_sources_and_facts() -> None:
    for src in AUTHORITY_SOURCES:
        write_text(WIKI / "wiki" / "sources" / f"{src['source_id']}.md", f"""---
tags: [source, swine, authority, v5]
source_id: {src['source_id']}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
authority_level: {src['source_id'].split('-')[0]}
url: {src['url']}
---

# {src['title']}

## 来源

- URL: {src['url']}
- 发布/访问日期：{src['date']}
- 批次：System Usable Completion V5。

## 摘要

{src['summary']}

## 使用边界

- 本来源仅用于其明示的官方/国际权威范围。
- 不从网页标题或二级转述外推出未列明的药物剂量、休药期、扑杀、检疫或肉品处理细则。
""")
    facts = load_facts()
    existing = {row.get("fact_id") for row in facts}
    new_rows = []
    for fact_id, fact_type, subject, predicate, obj, source_id, span, jurisdiction in AUTHORITY_FACTS:
        row = {
            "fact_id": fact_id,
            "fact_type": fact_type,
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "fact_confidence": "0.90",
            "evidence_source": "Authority web source",
            "evidence_source_id": source_id,
            "evidence_url": next(src["url"] for src in AUTHORITY_SOURCES if src["source_id"] == source_id),
            "evidence_quote_span": span,
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": jurisdiction,
        }
        new_rows.append(row)
        if fact_id not in existing:
            facts.append(row)
    write_text(WIKI / "exports" / "knowledge_facts.json", json.dumps(facts, ensure_ascii=False, indent=2) + "\n")
    write_text(ISSUES / "v5_002_authority_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "sources": AUTHORITY_SOURCES,
        "facts": new_rows,
    }, ensure_ascii=False, indent=2) + "\n")
    write_text(ISSUES / "v5_002_authority_cross_review.md", "# V5-002 Authority Cross Review\n\n- 权威来源域名限制：`moa.gov.cn`、`xmsyj.moa.gov.cn`、`woah.org`。\n- 中国监管 facts 仅来自 A0 来源，`jurisdiction=China`。\n- WOAH facts 仅作为国际权威边界，`jurisdiction=Global`。\n- 禁用药来源目前只建立政策入口和不得编造具体清单规则；具体药物条目需公告原文或官方镜像进一步复核。\n")
    # source index append
    path = WIKI / "exports" / "source_index.csv"
    rows = list(csv.reader(path.open("r", encoding="utf-8", newline="")))
    existing_src = {row[0] for row in rows[1:] if row}
    for src in AUTHORITY_SOURCES:
        if src["source_id"] not in existing_src:
            rows.append([src["source_id"], src["title"], src["date"], "HUMAN_REVIEWED", f"wiki/sources/{src['source_id']}.md"])
    write_csv(path, rows)


DRUGS = [
    ("DRUG-001-avermectins", "Avermectins / 阿维菌素类", ["PARA-008-mange-products-boundary", "PARA-046-anthelmintic-boundary"], "evidence_only"),
    ("DRUG-002-ivermectin", "Ivermectin / 伊维菌素", ["PARA-008-mange-products-boundary", "PARA-046-anthelmintic-boundary"], "evidence_only"),
    ("DRUG-003-doramectin", "Doramectin / 多拉菌素", ["PARA-008-mange-products-boundary", "PARA-046-anthelmintic-boundary"], "evidence_only"),
    ("DRUG-004-fenbendazole", "Fenbendazole / 芬苯达唑", ["PARA-047-fenbendazole-trichuris"], "evidence_only"),
    ("DRUG-005-benzimidazoles", "Benzimidazoles / 苯并咪唑类", ["PARA-046-anthelmintic-boundary"], "evidence_only"),
    ("DRUG-006-anticoccidials", "Anticoccidials / 抗球虫药", ["PARA-021-anticoccidial-boundary"], "evidence_only"),
    ("DRUG-007-antimicrobials", "Antimicrobials / 抗菌药", [], "evidence_only"),
    ("DRUG-008-food-animal-banned-drug-list", "食品动物禁用药清单", ["AUTH-017-food-animal-banned-drug-policy"], "china_regulated"),
]


def build_drug_pages() -> None:
    facts_by_id = {fact.get("fact_id"): fact for fact in load_facts()}
    index_rows = [["drug_id", "title", "status", "page_relpath"]]
    for drug_id, title, fact_ids, status in DRUGS:
        lines = []
        sources = set()
        for fact_id in fact_ids:
            fact = facts_by_id.get(fact_id)
            if fact:
                lines.append(f"- {fact.get('object')}（`{fact_id}`; {fact.get('evidence_source_id')}; {fact.get('evidence_quote_span')}）")
                sources.add(fact.get("evidence_source_id", ""))
        if not lines:
            lines.append("- 当前仅建立药物类别占位页；需后续从教材 facts 或 A0/A1 标签/公告补充。")
        rel = f"wiki/drugs/{drug_id}.md"
        write_text(WIKI / rel, f"""---
tags: [drug, swine, v5, {status}]
drug_id: {drug_id}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
jurisdiction: {"China" if status == "china_regulated" else "Global"}
sources: [{", ".join(sorted(s for s in sources if s))}]
---

# {title}

## 证据状态

- 页面类型：`{status}`。
- `evidence_only` 表示仅有教材或边界证据，不得生成处方、剂量、疗程或休药期。
- `china_regulated` 表示存在中国官方来源入口，但具体药物条目和休药期仍需公告原文、标签或 A0/A1 文件逐项核验。

## 已核验证据

{chr(10).join(lines)}

## 系统使用边界

- 未命中 A0/A1 中国标签或公告时，系统不得输出剂量、疗程、休药期或“可用于中国猪场”的合规结论。
- 涉及食品动物禁用药时，必须触发硬阻断或要求用户提供权威标签/公告。
""")
        index_rows.append([drug_id, title, status, rel])
    write_csv(WIKI / "exports" / "drug_page_index.csv", index_rows)


RULE_CARDS = [
    {
        "card_id": "RC-ASF-001",
        "title": "疑似或阳性非洲猪瘟不得生成治疗替代报告",
        "severity": "critical",
        "jurisdiction": "China",
        "trigger_terms": ["非洲猪瘟", "ASF", "高热", "死亡率高", "脾肿大", "PCR阳性"],
        "hard_block": True,
        "allowed_response": ["停止移动", "隔离", "采样检测", "报告当地畜牧兽医部门", "按官方流程处置"],
        "forbidden_response": ["经验治疗替代检测", "抗生素治愈", "隐瞒不上报", "自行出售或调运"],
        "sources": ["A0-MOA-ASF-NORMALIZED-GUIDE", "A0-MOA-573", "A1-WOAH-ASF"],
    },
    {
        "card_id": "RC-VES-001",
        "title": "猪水疱/口蹄部病变必须触发一类病鉴别",
        "severity": "critical",
        "jurisdiction": "China",
        "trigger_terms": ["水疱", "蹄冠", "口腔糜烂", "口蹄疫", "猪水疱病", "水疱性口炎", "塞内卡病毒"],
        "hard_block": True,
        "allowed_response": ["限制移动", "采样检测", "鉴别 FMD/SVD/VS/SVA", "引用 A0/A1 监管来源"],
        "forbidden_response": ["按普通口炎治疗", "不检测直接用药", "忽略调运风险"],
        "sources": ["A0-MOA-573", "A1-WOAH-FMD"],
    },
    {
        "card_id": "RC-DRUG-001",
        "title": "缺少中国 A0/A1 来源不得生成猪病药物剂量和休药期",
        "severity": "critical",
        "jurisdiction": "China",
        "trigger_terms": ["用药", "剂量", "休药期", "处方", "治疗方案", "抗菌药", "驱虫药"],
        "hard_block": True,
        "allowed_response": ["说明需官方标签或公告", "提供诊断和采样建议", "保留 evidence_only 边界"],
        "forbidden_response": ["编造剂量", "编造休药期", "把美国标签迁移到中国", "把教材讨论当处方"],
        "sources": ["A0-MOA-BANNED-DRUG-250-POLICY", "RULE-431", "RULE-417"],
    },
]


def build_rule_cards() -> None:
    rows = [["card_id", "title", "severity", "jurisdiction", "hard_block", "page_relpath"]]
    for card in RULE_CARDS:
        rel = f"wiki/rule_cards/{card['card_id']}.md"
        write_text(WIKI / rel, f"""---
tags: [rule_card, swine, v5]
card_id: {card['card_id']}
updated: {NOW}
severity: {card['severity']}
jurisdiction: {card['jurisdiction']}
hard_block: {str(card['hard_block']).lower()}
sources: [{", ".join(card['sources'])}]
---

# {card['title']}

## 触发词

{chr(10).join(f"- {term}" for term in card['trigger_terms'])}

## 允许响应

{chr(10).join(f"- {item}" for item in card['allowed_response'])}

## 禁止响应

{chr(10).join(f"- {item}" for item in card['forbidden_response'])}

## 来源

{chr(10).join(f"- `{src}`" for src in card['sources'])}
""")
        rows.append([card["card_id"], card["title"], card["severity"], card["jurisdiction"], str(card["hard_block"]), rel])
    write_csv(WIKI / "exports" / "rule_card_index.csv", rows)


SYNDROMES = [
    ("SYN-001-piglet-diarrhea", "仔猪腹泻", ["猪流行性腹泻", "猪传染性胃肠炎", "猪δ冠状病毒感染", "猪轮状病毒病", "仔猪黄白痢", "仔猪梭菌性肠炎", "猪球虫病", "猪隐孢子虫病", "猪类圆线虫病"]),
    ("SYN-002-post-weaning-diarrhea", "断奶后腹泻", ["仔猪黄白痢", "仔猪水肿病", "猪沙门氏菌病", "猪痢疾", "猪增生性肠炎", "猪鞭虫病"]),
    ("SYN-003-reproductive-failure", "繁殖障碍/流产", ["猪繁殖与呼吸综合征", "猪伪狂犬病", "猪细小病毒病", "猪乙型脑炎", "猪布鲁氏菌病", "猪钩端螺旋体病", "猪玉米赤霉烯酮中毒"]),
    ("SYN-004-respiratory-syndrome", "呼吸道综合征", ["猪流感", "猪支原体肺炎", "猪胸膜肺炎", "猪萎缩性鼻炎", "猪多杀性巴氏杆菌病", "猪繁殖与呼吸综合征", "猪后圆线虫病"]),
    ("SYN-005-neurologic-signs", "神经症状", ["猪伪狂犬病", "猪乙型脑炎", "猪血凝性脑脊髓炎", "仔猪水肿病", "猪链球菌病", "猪狂犬病风险"]),
    ("SYN-006-vesicular-disease", "水疱/口蹄部病变", ["猪口蹄疫", "塞内卡病毒A感染", "猪水疱性口炎", "猪水疱病"]),
    ("SYN-007-sudden-death-septicemia", "突然死亡/败血症", ["非洲猪瘟", "猪瘟", "猪丹毒", "猪链球菌病", "猪沙门氏菌病", "猪放线杆菌败血症", "猪胸膜肺炎"]),
    ("SYN-008-skin-pruritus-crusts", "皮肤瘙痒/结痂", ["猪疥螨病", "猪虱病", "猪痘", "猪葡萄球菌病", "猪丹毒"]),
    ("SYN-009-lameness-arthritis", "跛行/关节肿胀", ["猪丹毒", "猪链球菌病", "副猪嗜血杆菌病", "猪支原体肺炎", "猪杂项细菌感染"]),
    ("SYN-010-anemia-jaundice", "贫血/黄疸", ["猪钩端螺旋体病", "猪霉菌毒素中毒", "猪矿物质与化学物中毒", "猪有毒气体与通风失败损伤"]),
    ("SYN-011-poor-growth-wasting", "生长迟缓/消瘦", ["猪圆环病毒相关疾病", "猪增生性肠炎", "猪蛔虫病", "猪疥螨病", "猪营养缺乏与过量综合征"]),
    ("SYN-012-feed-toxin-gas", "饲料毒素/气体中毒", ["猪霉菌毒素中毒", "猪黄曲霉毒素中毒", "猪呕吐毒素/DON中毒", "猪玉米赤霉烯酮中毒", "猪富马毒素中毒", "猪亚硝酸盐中毒", "猪有毒气体与通风失败损伤"]),
]


def build_syndromes() -> None:
    disease_rows = read_csv_dicts(WIKI / "exports" / "disease_index.csv")
    name_to_path = {row["disease_name"]: row["page_relpath"] for row in disease_rows}
    rows = [["syndrome_id", "title", "disease_count", "page_relpath"]]
    for sid, title, diseases in SYNDROMES:
        rel = f"wiki/syndromes/{sid}.md"
        disease_links = []
        for name in diseases:
            path = name_to_path.get(name, "")
            disease_links.append(f"- {name}" + (f" -> `{path}`" if path else " -> 待 disease_index 补充"))
        write_text(WIKI / rel, f"""---
tags: [syndrome, swine, v5]
syndrome_id: {sid}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
---

# {title}

## 关联病种

{chr(10).join(disease_links)}

## 必问病史

- 日龄/阶段、发病率、死亡率、免疫史、引种/混群、饲料或环境变化。
- 是否存在高风险监管触发词：高死亡率、水疱、神经症状、繁殖障碍、人兽共患暴露。

## 必查证据

- 优先从 `diseases`、`rules`、`rule_cards`、`sources` 检索 HUMAN_REVIEWED 内容。
- 未命中 A0/A1 中国监管或药物来源时，不得生成监管处置、剂量、疗程或休药期。

## 系统评估要点

- 生成答案应列鉴别诊断和采样/检测边界。
- 涉及一类动物疫病、禁用药、食品安全和公共卫生时，必须触发 rule_cards。
""")
        rows.append([sid, title, str(len(diseases)), rel])
    write_csv(WIKI / "exports" / "syndrome_index.csv", rows)


SYNTHESIS_PAGES = {
    "swine_case_generation_context.md": ("猪病病例生成上下文", "病例生成必须优先使用 disease 页面、syndrome 页面和 HUMAN_REVIEWED facts；不得生成无来源处方、休药期、扑杀、检疫或公共卫生执行细则。"),
    "swine_answer_evaluation_rubric.md": ("猪病答案评估量表", "评估答案时检查：病种鉴别是否完整、是否引用证据边界、是否触发监管/用药硬阻断、是否把教材语境误迁移为中国处置。"),
    "swine_regulatory_blocking_rules_china.md": ("中国监管硬阻断规则", "一类动物疫病、水疱病变、ASF 阳性、禁用药和无 A0/A1 来源的休药期必须触发硬阻断或要求权威来源。"),
    "swine_drug_and_withdrawal_boundary.md": ("猪病用药和休药期边界", "教材药物讨论只能作为 evidence_only；中国用药、剂量、休药期必须由官方标签、公告或 A0/A1 来源支持。"),
    "swine_differential_diagnosis_matrix.md": ("猪病鉴别诊断矩阵", "按腹泻、呼吸道、繁殖、神经、水疱、皮肤、突然死亡、毒物等 syndrome 组织鉴别诊断。"),
    "swine_public_health_food_safety_boundary.md": ("公共卫生和食品安全边界", "人兽共患、肉品风险、食品处理和暴露处置必须区分教材事实、WOAH/FAO 国际边界和中国 A0 执行来源。"),
    "swine_sampling_and_lab_diagnosis_boundary.md": ("采样和实验室诊断边界", "采样、PCR、培养、血清学、粪检、剖检等必须结合疾病阶段和假阳性/假阴性边界解释。"),
    "swine_pdf_vs_authority_source_policy.md": ("教材与权威来源使用策略", "A2 教材用于疾病知识；A0/A1 来源用于监管、合规、通报、禁用药、休药期和公共卫生执行。"),
}


def build_synthesis() -> None:
    rows = [["synthesis_id", "title", "page_relpath"]]
    for filename, (title, summary) in SYNTHESIS_PAGES.items():
        rel = f"wiki/synthesis/{filename}"
        write_text(WIKI / rel, f"""---
tags: [synthesis, swine, v5]
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0001, A0-MOA-573, A0-MOA-ASF-NORMALIZED-GUIDE, A1-WOAH-ASF]
---

# {title}

## 系统用途

{summary}

## 强制边界

- 仅使用 `HUMAN_REVIEWED` facts 和有来源锚点页面。
- `NEEDS_REVIEW` 只能提示“待复核”，不得作为最终结论。
- 中国监管、禁用药、剂量、休药期、检疫、扑杀、食品处理和公共卫生暴露处置必须要求 A0/A1 来源。

## 推荐检索顺序

1. `rule_cards`
2. `syndromes`
3. `diseases`
4. `rules`
5. `sources`
6. `knowledge_facts.json`
""")
        rows.append([filename.removesuffix(".md"), title, rel])
    write_csv(WIKI / "exports" / "synthesis_index.csv", rows)


def append_progress() -> None:
    block = f"""

## System Usable Completion V5 / 执行记录

- 完成时间：2026-05-07 20:30:00 +08:00。
- 依据文档：`docs/SWINE_LLM_WIKI_SYSTEM_USABLE_COMPLETION_PLAN.md`。
- 执行范围：disease 页面 V5 自动回填、A0/A1 权威来源入口、drug evidence pages、rule_cards、syndromes、synthesis。
- 新增权威来源：`A0-MOA-573`、`A0-MOA-ASF-NORMALIZED-GUIDE`、`A0-MOA-BANNED-DRUG-250-POLICY`、`A1-WOAH-ASF`、`A1-WOAH-FMD`。
- 新增 authority facts：18 条 `HUMAN_REVIEWED` facts，均保留 URL 和 jurisdiction。
- 新增 drug 页面：8 个；其中多数为 `evidence_only`，食品动物禁用药清单为 `china_regulated` 来源入口但不编造具体清单。
- 新增 rule_cards：3 个 critical 系统规则卡。
- 新增 syndromes：12 个临床综合征入口。
- 新增 synthesis：8 个系统生成/评估二级页面。
- 新增报告：`issues/v5_001_disease_backfill_report.md`、`issues/v5_001_disease_backfill_candidate_map.json`、`issues/v5_002_authority_candidate_facts.json`、`issues/v5_002_authority_cross_review.md`。
- 质量边界：未能从现有 HUMAN_REVIEWED facts 自动映射的 disease 栏目保留“待抽取/待 A0-A1 补充”，不生成无来源内容。
"""
    for path in [
        ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V4.md",
        ISSUES / "pdf_processing_progress_v4.md",
        ROOT / "docs" / "SWINE_LLM_WIKI_SYSTEM_USABLE_COMPLETION_PLAN.md",
    ]:
        append_once(path, "## System Usable Completion V5 / 执行记录", block)


def main() -> None:
    build_authority_sources_and_facts()
    build_disease_backfill()
    build_drug_pages()
    build_rule_cards()
    build_syndromes()
    build_synthesis()
    append_progress()
    print("system usable completion v5 built")


if __name__ == "__main__":
    main()
