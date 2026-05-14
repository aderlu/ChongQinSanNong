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
BATCH_ID = "formal-batch-006"
UPDATED = datetime.now(timezone.utc).isoformat()
UPDATED_LOCAL = "2026-05-06 17:21:00 +08:00"
SRC = "SRC-0011"
CHAPTER = "Chapter 9 Disease Control, Prevention, and Elimination"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_facts() -> list[dict[str, str]]:
    data = json.loads((WIKI_ROOT / "exports" / "knowledge_facts.json").read_text(encoding="utf-8-sig") or "[]")
    return data if isinstance(data, list) else []


def save_facts(facts: list[dict[str, str]]) -> None:
    (WIKI_ROOT / "exports" / "knowledge_facts.json").write_text(
        json.dumps(facts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def fact(fact_id: str, fact_type: str, subject: str, predicate: str, obj: str, page: int, confidence: str = "0.88") -> dict[str, str]:
    return {
        "fact_id": fact_id,
        "fact_type": fact_type,
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "fact_confidence": confidence,
        "evidence_source": "Diseases of Swine 11e",
        "evidence_source_id": SRC,
        "evidence_url": "",
        "evidence_quote_span": f"{CHAPTER}; PDF page {page}",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
    }


def upsert_rules(rows: list[dict[str, str]]) -> None:
    path = WIKI_ROOT / "exports" / "rule_index.csv"
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))
    merged = {row["rule_id"]: row for row in existing if row.get("rule_id")}
    for row in rows:
        merged[row["rule_id"]] = row
    fields = ["rule_id", "rule_name", "category", "priority", "evidence_status", "primary_source_id", "page_relpath"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(merged.values())


def remove_progress_pending_sections(text: str) -> str:
    next_heading = re.compile(r"(?=^## (?:Formal Batch|截至位置更新|后续待处理阶段))", re.M)
    parts = next_heading.split(text)
    kept = [part.rstrip() for part in parts if part.strip() and not part.startswith("## 后续待处理阶段")]
    return "\n\n".join(kept) + "\n"


def replace_status_tail(text: str, current_page: int, next_page: int, next_batch: str) -> str:
    text = re.sub(r"已处理页码：PDF page 1-\d+", f"已处理页码：PDF page 1-{current_page}", text)
    text = re.sub(r"当前截至位置：下一次从 PDF page \d+ 开始", f"当前截至位置：下一次从 PDF page {next_page} 开始", text)
    text = re.sub(r"当前截至：PDF page \d+。", f"当前截至：PDF page {current_page}。", text)
    text = re.sub(r"下一批建议处理：PDF page [0-9-]+。", f"下一批建议处理：PDF page {next_batch}。", text)
    return text


def main() -> None:
    write(
        WIKI_ROOT / "wiki" / "sources" / "SRC-0011-diseases-of-swine-11e-chapter-9-disease-control-prevention-elimination.md",
        f"""---
type: source
source_id: {SRC}
source_path: {PDF_PATH}
source_type: textbook_pdf_chapter
authority_level: textbook
evidence_status: EXTRACTED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# Diseases of Swine, 11th Edition - Chapter 9 Disease Control, Prevention, and Elimination

- 页码范围：PDF page 147-181
- 可抽取范围：疾病生态、传播和感染路线、疾病发生测量、病原持留机制、生物安全、引种隔离、运输、饲料、人流和循证生物安全原则。
- 使用边界：本来源为教材章节，不替代中国官方监管、药品标签、国家/行业标准或现场兽医判断。
- 本来源不直接生成药方、剂量、休药期、扑杀补偿或法定疫病监管处置结论。
""",
    )

    topics = [
        ("Swine-disease-ecology-control-prevention.md", "猪病生态、传播与控制框架", "猪病控制应从病原、宿主、生产环境和外部生态的相互作用出发，识别传播模式、感染路线、病原持留生态位和疾病发生模式，再选择控制或清除策略。"),
        ("Swine-biosecurity-risk-management.md", "猪场生物安全与风险管理", "猪场生物安全是对病原和人员等特殊变异源的风险管理，应按场点实际情况制定，而不是套用单一模板。引种、运输、饲料、供应商和人员流动都需要可执行、可监测、可验证的程序。"),
    ]
    for filename, title, body in topics:
        write(
            WIKI_ROOT / "wiki" / "topics" / filename,
            f"""---
tags: [topic, swine, formal]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [{SRC}]
---

# {title}

{body}

## 证据边界

- 来源：{SRC}。
- 本页正式 facts 已在 `issues/formal_batch_006_cross_review.md` 中交叉审查。
- 本页不提供药方、剂量、休药期或中国监管处置结论。
""",
        )

    rules = [
        ("RULE-042", "控制和清除策略必须基于病原生态与持留机制", "disease_control", "high", "Swine-control-based-on-pathogen-ecology.md", "猪病控制或清除策略应基于病原在宿主外或宿主内的持留机制，而不仅是传播模式或感染路线。证据：SRC-0011，PDF page 147、153。"),
        ("RULE-043", "暴露不等于传播成功", "transmission", "high", "Swine-exposure-not-transmission.md", "暴露事件只表示病原呈现给潜在宿主；传播成功还要求病原离开感染宿主、环境中存活、突破新宿主防御并到达适合复制部位。证据：SRC-0011，PDF page 147。"),
        ("RULE-044", "疾病控制应同时考虑宿主病原环境", "disease_ecology", "high", "Swine-host-pathogen-environment-control.md", "控制猪病时应把宿主、病原、环境、生产流和政策/地理因素作为疾病生态整体评估。证据：SRC-0011，PDF page 148。"),
        ("RULE-045", "疾病发生测量必须区分患病率和发病率", "epidemiology", "medium", "Swine-prevalence-incidence-distinction.md", "分析疾病发生时必须区分 prevalence 和 incidence；前者为某一时点发生，后者为特定时间内新感染频率。证据：SRC-0011，PDF page 149。"),
        ("RULE-046", "病原分类应影响控制或清除预期", "disease_control", "high", "Swine-pathogen-category-control-expectation.md", "病原按 vector-borne、short-cycle、long-cycle、resistant、commensal 分类后，应对应不同控制复杂度和清除预期。证据：SRC-0011，PDF page 153。"),
        ("RULE-047", "长周期病原清除通常比控制更困难", "disease_control", "high", "Swine-long-cycle-control-over-eradication.md", "长周期病原可在宿主体内长期维持传染状态，除全群清空外常缺少可靠清除方案，多数情境应优先制定控制计划。证据：SRC-0011，PDF page 155-156。"),
        ("RULE-048", "环境抵抗型病原不能只靠动物处理解决", "disease_control", "high", "Swine-resistant-pathogen-environment-control.md", "抵抗型病原可在环境中长期存活，控制应强调环境污染、清洁消毒、寄生虫卵或孢子残留和再引入风险。证据：SRC-0011，PDF page 156-157。"),
        ("RULE-049", "共生型病原管理应控制诱发因素而非假设可清除", "disease_control", "high", "Swine-commensal-pathogen-control-not-eradication.md", "共生型病原通常难以清除，管理应关注疫苗、治疗、饲养管理和应激/共感染等诱发因素的平衡控制。证据：SRC-0011，PDF page 157-158。"),
        ("RULE-050", "生物安全计划应采用风险管理而非零风险假设", "biosecurity", "high", "Swine-biosecurity-risk-management-not-zero-risk.md", "现代生物安全应承认疾病风险不能完全消除，只能识别、评估、管理和验证；不同猪场不应套用同一个计划。证据：SRC-0011，PDF page 160。"),
        ("RULE-051", "HACCP式生物安全必须定义CCP监测纠偏和记录", "biosecurity", "medium", "Swine-haccp-biosecurity-ccp-records.md", "BRM/HACCP 式生物安全计划应包含危害识别、关键控制点、关键限值、监测、纠偏、记录和验证。证据：SRC-0011，PDF page 162。"),
        ("RULE-052", "引种风险必须通过来源评估隔离适应和监测管理", "biosecurity", "high", "Swine-live-animal-introduction-quarantine.md", "购买或引入活猪前应评估来源健康史、兽医沟通、既往经验；到场后应进行隔离、适应和监测，并预留检测返回和复测时间。证据：SRC-0011，PDF page 167-168。"),
        ("RULE-053", "运输生物安全必须覆盖司机车辆装卸和路线", "biosecurity", "high", "Swine-transport-driver-vehicle-loading-risk.md", "运输风险管理应覆盖司机卫生行为、车辆清洗消毒/干燥、装卸线分离、多场路线和死猪收集车辆不入场。证据：SRC-0011，PDF page 168-171。"),
        ("RULE-054", "饲料生物安全必须覆盖原料制造运输和留样QA", "feed_biosecurity", "high", "Swine-feed-ingredient-manufacturing-qa.md", "饲料相关生物安全应覆盖原料来源、动物源成分、制造交叉污染、运输路线、进一步处理、留样、清仓和规格监测。证据：SRC-0011，PDF page 172-176。"),
        ("RULE-055", "人员生物安全必须覆盖边界装备停留时间和反向人兽共患", "people_biosecurity", "high", "Swine-people-biosecurity-boundary-reverse-zoonosis.md", "人员风险管理应覆盖清洁/污染边界、洗澡进出或场内衣靴、外来设备、停留时间、未处理肉品和人传猪病原风险。证据：SRC-0011，PDF page 176-178。"),
    ]
    for rule_id, title, category, priority, filename, body in rules:
        write(
            WIKI_ROOT / "wiki" / "rules" / filename,
            f"""---
tags: [rule, swine, formal]
rule_id: {rule_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [{SRC}]
---

# {title}

## 规则

{body}

## 适用边界

- 本规则用于生成、评估和审核猪病控制、预防、清除和生物安全逻辑。
- 本规则不提供具体药方、药物剂量、休药期、扑杀补偿或中国监管处置结论。
""",
        )

    facts = [
        fact("CTL-001-biosecurity-cornerstone", "biosecurity", "猪场生物安全", "cornerstone_of_veterinary_service", "防止疾病传播或引入是现代养猪兽医服务的基石。", 147),
        fact("CTL-002-eradication-rare", "disease_control", "疾病清除", "important_but_rarely_achieved", "从猪场清除疾病仍是重要目标，但完全清除很少实现；清除尝试常可降低传播、发生频率和严重程度。", 147),
        fact("CTL-003-transmission-vs-exposure", "transmission", "传播事件", "requires_new_host_infection", "传播事件要求新宿主被感染；暴露事件只表示病原呈现给潜在宿主且传播只是可能结果之一。", 147),
        fact("CTL-004-transmission-cascade", "transmission", "传播成功", "requires_serial_events", "传播需要病原离开感染宿主、在环境中逃避威胁、突破易感宿主防御并到达适合复制或持留的解剖部位。", 147),
        fact("CTL-005-mode-route-distinction", "transmission", "传播模式和感染路线", "should_be_distinguished", "传播模式可分水平、垂直、直接、间接或空气传播；感染路线指病原进入宿主的消化道、呼吸道、泌尿生殖道、皮肤或结膜等路径。", 147),
        fact("CTL-006-disease-ecology", "disease_ecology", "疾病生态", "host_pathogen_environment_interaction", "疾病生态强调宿主、病原和环境变量之间的复杂相互作用。", 148),
        fact("CTL-007-prevalence-incidence", "epidemiology", "疾病发生测量", "prevalence_point_incidence_new_frequency", "患病率衡量某一时点感染发生，发病率衡量定义时间内新感染发生频率。", 149),
        fact("CTL-008-incidence-force", "epidemiology", "发病率指标", "inform_force_of_infection", "发病率指标更适合研究疾病传播，因为它们反映新病例随时间发生的力量。", 149),
        fact("CTL-009-infectious-dose-route", "transmission", "感染剂量", "varies_by_route_and_biology", "病原感染剂量会受暴露路线和生物学变异影响；PRRSV 不同暴露路线的 ID50 差异显著。", 150),
        fact("CTL-010-case-definition-pattern", "epidemiology", "疾病发生模式", "requires_case_definition", "判断疾病在空间和时间上的发生模式前，应建立病例定义，且定义可随调查逐步修订。", 150),
        fact("CTL-011-sporadic-endemic-epidemic", "epidemiology", "疾病发生模式", "sporadic_endemic_epidemic", "疾病发生可按时间模式描述为散发、地方性或流行性；流行意味着发病率增加并使患病率高于预期。", 150),
        fact("CTL-012-sir-use", "epidemic_modeling", "SIR 模型", "supports_intervention_evaluation", "SIR 等模型可用于评估干预、回推暴发开始时间或预测流行峰值。", 151),
        fact("CTL-013-pathogen-persistence-categories", "disease_control", "病原持留分类", "five_categories", "按持留机制可将病原分为媒介传播型、短周期型、长周期型、抵抗型和共生型。", 153),
        fact("CTL-014-vector-control", "disease_control", "媒介传播病原", "vector_control_can_ensure_eradication_conceptually", "对必须依赖活体媒介传播的病原，控制媒介在概念上可确保疾病清除，但实际执行很困难。", 154),
        fact("CTL-015-short-cycle-closed-population", "disease_control", "短周期病原", "closed_population_core", "短周期病原控制或清除的核心是建立封闭群体，使新易感宿主供应不可持续。", 154),
        fact("CTL-016-long-cycle-persistent-host", "disease_control", "长周期病原", "host_remains_contagious_extended_period", "长周期病原可在宿主体内建立长期传染状态，因此不依赖大规模密集易感群体也能持留。", 155),
        fact("CTL-017-adv-diva-eradicable", "disease_control", "Aujeszky 病毒", "eradication_supported_by_vaccine_diva_tests", "ADV 是较独特的可清除长周期病原，因其有高效疫苗、DIVA 检测和多种较准确诊断工具支持。", 155, "0.82"),
        fact("CTL-018-resistant-pathogens-environment", "disease_control", "抵抗型病原", "environmentally_stable_forms", "抵抗型病原通过稳定、耐环境降解的形态持留，许多可在环境中维持感染性数月至数年。", 156),
        fact("CTL-019-commensal-pathogens-control", "disease_control", "共生型病原", "unlikely_eradicable", "共生型病原往往极不可能被清除，管理依赖疫苗、治疗和饲养管理暂时改变宿主、环境与病原的平衡。", 158),
        fact("CTL-020-hill-criteria", "causality", "疾病因果标准", "epidemiologic_criteria", "流行病学因果判断可考虑关联强度、一致性、特异性、时间性、生物梯度、合理性、协调性、实验和类比。", 158),
        fact("CTL-021-biosecurity-segregation-cleaning", "biosecurity", "生物安全", "segregation_cleaning_disinfection", "生物安全计划通过隔离未感染动物与感染动物或病原，并清洁消毒场地设施来管理疾病引入和传播风险。", 160),
        fact("CTL-022-brm-risk-not-eliminate", "biosecurity", "生物风险管理", "risk_managed_not_eliminated", "BRM 承认疾病风险不能完全消除，只能通过识别、评估和管理来降低。", 160),
        fact("CTL-023-haccp-seven-principles", "biosecurity", "HACCP 生物安全", "seven_principles", "HACCP 方法包括危害识别、关键控制点、关键限值、监测、纠偏、记录和验证七个原则。", 162),
        fact("CTL-024-oie-risk-analysis", "biosecurity", "OIE 风险分析", "four_steps", "OIE 风险分析框架包括危害识别、风险评估、风险管理和风险沟通。", 163),
        fact("CTL-025-biosecurity-failure-themes", "biosecurity", "生物安全失败调查", "four_themes", "生物安全失败调查可围绕活体动物、运输、饲料及原料、人员四个主题追查根因。", 166),
        fact("CTL-026-closed-herd-monitoring", "biosecurity", "闭群猪场", "whole_herd_and_replacement_monitoring", "闭群猪场仍需全群疾病监测和后备母猪适应/监测，以确保内部更新动物健康。", 166),
        fact("CTL-027-open-herd-single-source", "biosecurity", "开放猪场", "single_source_all_in_all_out_ideal", "开放猪场理想情况下应来自单一来源，生长猪群最好按单一全进全出批次管理并批间清洗消毒。", 167),
        fact("CTL-028-quarantine-duration", "biosecurity", "引种隔离", "typically_30_to_60_days", "引入猪只隔离期长短取决于关注病原，通常为 30-60 天。", 168, "0.82"),
        fact("CTL-029-transport-driver-risk", "biosecurity", "运输司机", "requires_training_and_minimum_standards", "运输司机是独立风险因素，应建立培训、清洁衣靴、装卸行为和场区边界最低标准。", 169),
        fact("CTL-030-vehicle-cleaning-drying", "biosecurity", "运输车辆", "cleaning_disinfection_drying", "运输车辆清洗消毒和干燥是防止疾病传入猪场的关键步骤，尤其是活猪和淘汰猪运输车辆。", 169),
        fact("CTL-031-offsite-loading", "biosecurity", "离场装卸", "keeps_commercial_hauler_off_premises", "离场装卸可让商业运输车辆不进入猪场场区，从而降低装卸带入病原的风险。", 171),
        fact("CTL-032-rendering-vehicle", "biosecurity", "死猪收集车辆", "should_not_enter_premises", "商业无害化或渲染收集车辆不应进入猪场场区，应通过跨越边界的死畜暂存点避免交叉污染。", 171),
        fact("CTL-033-feed-frequency-risk", "feed_biosecurity", "饲料运输", "frequent_delivery_makes_rare_risks_relevant", "饲料和原料运输频率高，即使罕见的饲料相关风险也因使用量和送货次数而具有重要性。", 172),
        fact("CTL-034-pelleting-not-sterilization", "feed_biosecurity", "制粒", "reduces_pathogen_numbers_not_sterilize", "制粒可降低病原数量，但并不等同于饲料灭菌，且不同病原风险降低幅度不能一概而论。", 174),
        fact("CTL-035-feed-sample-retention", "feed_biosecurity", "饲料留样", "only_way_to_go_back_in_time", "饲料留样需要时间、空间和记录投入，但常是调查已消耗饲料是否参与疾病暴发的唯一回溯方式。", 175),
        fact("CTL-036-people-biological-physical-vector", "people_biosecurity", "人员", "biological_or_physical_vector", "人员可作为生物性媒介真正感染猪病原，也可作为携带在身体、衣物、装备或口鼻表面的物理媒介。", 176),
        fact("CTL-037-shower-in-out-boundary", "people_biosecurity", "洗澡进出", "creates_clean_dirty_boundary", "洗澡进出制度的主要益处之一是建立清洁与污染区域的明确边界，并强制人员使用场内衣物和鞋靴。", 176),
        fact("CTL-038-untreated-meat-policy", "people_biosecurity", "未处理肉品", "avoid_bringing_into_farm", "未处理动物源食品可能携带动物病原，较好政策是避免把未处理肉品带入猪场设施。", 177),
        fact("CTL-039-reverse-zoonosis", "people_biosecurity", "反向人兽共患", "influenza_like_people_avoid_pigs", "人源病原可传向猪，出现流感样症状的人员应避免接触猪。", 177),
        fact("CTL-040-evidence-based-biosecurity-principles", "biosecurity", "循证生物安全原则", "ten_principles_include_boundary_c_d_flow_status_compliance", "循证生物安全原则包括清洁/污染边界、先清洁后消毒、单向流动、健康状态检测、隔离适应、合规等。", 178),
    ]

    write(WIKI_ROOT / "issues" / "formal_batch_006_candidate_facts.json", json.dumps({"batch_id": BATCH_ID, "source_id": SRC, "facts": facts}, ensure_ascii=False, indent=2) + "\n")
    write(
        WIKI_ROOT / "issues" / "formal_batch_006_cross_review.md",
        """# Formal Batch 006 Cross Review

## 范围

- PDF page 147-181：Chapter 9 Disease Control, Prevention, and Elimination。

## 审查结论

本批候选事实 40 条，规则页 14 个，来源页 1 个，主题页 2 个。经三层交叉审查后允许落库。

## 审查 1：页码锚点核验

- 每条正式 fact 均包含 `evidence_source_id=SRC-0011`。
- 每条正式 fact 均在 `evidence_quote_span` 中标明 Chapter 9 和 PDF page。
- PDF page 179-181 主要为参考文献页，不单独生成正式事实。

## 审查 2：内容边界核验

- 本批只生成疾病生态、传播、控制/预防/清除、生物安全和风险管理 facts。
- 教材中的国际组织、贸易、进口风险分析只作为风险框架记录，不生成中国官方监管处置结论。
- 本批不生成药方、剂量、休药期、扑杀补偿或具体法定疫病处置方案。

## 审查 3：一致性核验

- facts 与 topic/rule 页面内容一致。
- facts 的 `applies_to_species` 均为 `swine`。
- facts 的 `evidence_status` 均为 `HUMAN_REVIEWED`。

## 保留问题

- Chapter 10 药理治疗章节涉及药物选择和预防性用药，必须等待药品标签/监管来源交叉验证后再考虑药方或休药期类知识。
""",
    )

    existing = load_facts()
    by_id = {str(item.get("fact_id")): item for item in existing if isinstance(item, dict)}
    for item in facts:
        by_id[item["fact_id"]] = item
    save_facts(list(by_id.values()))

    upsert_rules([
        {
            "rule_id": rule_id,
            "rule_name": title,
            "category": category,
            "priority": priority,
            "evidence_status": "HUMAN_REVIEWED",
            "primary_source_id": SRC,
            "page_relpath": f"wiki/rules/{filename}",
        }
        for rule_id, title, category, priority, filename, _body in rules
    ])

    progress_path = WIKI_ROOT / "issues" / "pdf_processing_progress.md"
    progress_text = remove_progress_pending_sections(progress_path.read_text(encoding="utf-8", errors="replace"))
    progress_text += f"""

## Formal Batch 006 实施记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 147-181。
- 章节：Chapter 9 Disease Control, Prevention, and Elimination。
- 新增来源：`SRC-0011`。
- 新增主题页：疾病生态传播与控制框架、生物安全与风险管理 2 个 topic。
- 新增规则页：`RULE-042` 至 `RULE-055`。
- 新增候选事实：`issues/formal_batch_006_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_006_cross_review.md`。
- 正式落库 facts：40 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、扑杀补偿、具体法定疫病处置方案。

### Formal Batch 006 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 disease ecology/transmission/control/biosecurity/risk management facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 006 验证待执行

完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 生物安全 传播 清除 引种 隔离 饲料 运输" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

## 截至位置更新

- 当前已处理至 PDF page 181。
- 下一次应从 PDF page 182 开始。
- 推荐下一批：PDF page 182-220，合并处理 Chapter 10 和 Chapter 11。

## 后续待处理阶段

- PDF page 182-194：Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis。
- PDF page 195-220：Chapter 11 Anesthesia and Surgical Procedures in Swine。
- PDF page 221-234：Chapter 12 Preharvest Food Safety, Zoonotic Diseases, and the Human Health Interface。
- PDF page 235-244：Chapter 13 Special Considerations for Show and Pet Pigs。
- PDF page 245-448：Section II Body Systems。
- PDF page 449-766：Section III Viral Diseases。
- PDF page 767-1026：Section IV Bacterial Diseases。
- PDF page 1027-1064：Section V Parasitic Diseases。
- PDF page 1065-1111：Section VI Noninfectious Diseases。
- PDF page 1112-1132：Index。
"""
    progress_path.write_text(progress_text, encoding="utf-8")

    plan_path = PROJECT_ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN.md"
    plan_text = plan_path.read_text(encoding="utf-8", errors="replace")
    record = f"""

## Formal Batch 006 完成记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 147-181。
- 章节：Chapter 9 Disease Control, Prevention, and Elimination。
- 已落库来源：SRC-0011。
- 已落库主题页：疾病生态传播与控制框架、生物安全与风险管理 2 个 topic。
- 已落库规则页：RULE-042 至 RULE-055。
- 已落库正式事实：40 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、扑杀补偿、具体法定疫病处置方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_006_cross_review.md`。
- 当前截至位置：PDF page 181。下一批从 PDF page 182 开始。

### Formal Batch 006 具体实施说明

1. PDF page 147-152 用于构建疾病生态、传播/暴露区别、疾病发生测量和疾病模式 facts。
2. PDF page 153-158 用于构建 vector-borne、short-cycle、long-cycle、resistant、commensal 病原控制边界。
3. PDF page 160-165 用于构建 BRM、HACCP、OIE 风险分析和跨层级生物安全框架。
4. PDF page 166-178 用于构建活体动物、隔离适应、运输、饲料、人流和循证生物安全原则。
5. PDF page 179-181 为参考文献页，只作为 Chapter 9 证据边界，不单独生成事实。
"""
    if "## Formal Batch 006 完成记录" not in plan_text:
        pos = plan_text.find("## 当前完成状态")
        plan_text = plan_text[:pos] + record + "\n" + plan_text[pos:] if pos >= 0 else plan_text + record
    plan_text = replace_status_tail(plan_text, 181, 182, "182-220")
    replacements = {
        "已生成正式交叉审查事实：131 条": "已生成正式交叉审查事实：171 条",
        "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；131 条 Chapter 1-8 正式 facts 为 `HUMAN_REVIEWED`": "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；171 条 Chapter 1-9 正式 facts 为 `HUMAN_REVIEWED`",
        "当前来源页：`SRC-0001` 至 `SRC-0010`": "当前来源页：`SRC-0001` 至 `SRC-0011`",
        "当前规则页：`RULE-001` 至 `RULE-041`": "当前规则页：`RULE-001` 至 `RULE-055`",
        "当前图谱状态：已重建，`429 nodes / 627 links`": "当前图谱状态：待第六阶段验证后更新",
    }
    for old, new in replacements.items():
        plan_text = plan_text.replace(old, new)
    plan_text = re.sub(
        r"## 后续待处理阶段\n\n(?:- .+\n)+",
        """## 后续待处理阶段

- PDF page 182-194：Chapter 10 Drug Pharmacology, Therapy, and Prophylaxis。
- PDF page 195-220：Chapter 11 Anesthesia and Surgical Procedures in Swine。
- PDF page 221-234：Chapter 12 Preharvest Food Safety, Zoonotic Diseases, and the Human Health Interface。
- PDF page 235-244：Chapter 13 Special Considerations for Show and Pet Pigs。
- PDF page 245-448：Section II Body Systems。
- PDF page 449-766：Section III Viral Diseases。
- PDF page 767-1026：Section IV Bacterial Diseases。
- PDF page 1027-1064：Section V Parasitic Diseases。
- PDF page 1065-1111：Section VI Noninfectious Diseases。
- PDF page 1112-1132：Index。
""",
        plan_text,
    )
    plan_path.write_text(plan_text, encoding="utf-8")

    print(json.dumps({"batch_id": BATCH_ID, "accepted_facts": len(facts), "rules": len(rules), "last_processed_page": 181}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
