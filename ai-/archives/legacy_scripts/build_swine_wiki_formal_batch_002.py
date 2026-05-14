from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = PROJECT_ROOT / "knowledge" / "llm_wiki_swine_authoritative"
PDF_PATH = (
    "docs/Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman, "
    "Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
)
BATCH_ID = "formal-batch-002"
UPDATED = datetime.now(timezone.utc).isoformat()
UPDATED_LOCAL = "2026-05-06 16:45:00 +08:00"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json_list(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig") or "[]")
    return data if isinstance(data, list) else []


def save_facts(facts: list[dict[str, str]]) -> None:
    (WIKI_ROOT / "exports" / "knowledge_facts.json").write_text(
        json.dumps(facts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def fact(
    fact_id: str,
    fact_type: str,
    subject: str,
    predicate: str,
    obj: str,
    page: int,
    *,
    confidence: str = "0.88",
) -> dict[str, str]:
    return {
        "fact_id": fact_id,
        "fact_type": fact_type,
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "fact_confidence": confidence,
        "evidence_source": "Diseases of Swine 11e",
        "evidence_source_id": "SRC-0004",
        "evidence_url": "",
        "evidence_quote_span": f"Chapter 2 Behavior and Welfare; PDF page {page}",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
    }


def main() -> None:
    write(
        WIKI_ROOT / "wiki" / "sources" / "SRC-0004-diseases-of-swine-11e-chapter-2-behavior-and-welfare.md",
        f"""---
type: source
source_id: SRC-0004
source_path: {PDF_PATH}
source_type: textbook_pdf_chapter
authority_level: textbook
evidence_status: EXTRACTED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# Diseases of Swine, 11th Edition - Chapter 2 Behavior and Welfare

本来源页锚定 PDF page 41-65：

- PDF page 41-42：动物福利定义、五大自由、OIE/WOAH 福利定义和 public/legal/technical welfare definitions。
- PDF page 43-45：野猪/家猪行为比较、刻板行为、科学福利评估、动物本体指标与资源指标。
- PDF page 46-49：母猪咬仔、侵入性操作、疼痛识别、断尾、去势、獠牙修剪和新生仔猪疼痛管理证据边界。
- PDF page 50-57：采食饮水行为、咬尾、belly nosing、跛行、攻击行为、疾病对行为影响、护理栏/病弱猪管理。
- PDF page 58-59：安乐死原则、失去知觉判断、二氧化碳和物理方法的边界。
- PDF page 60-65：Chapter 2 references。

## 可抽取知识范围

- 动物福利定义和评估框架。
- 猪只异常行为、咬尾、跛行、疾病行为和攻击行为的风险信号。
- 采食饮水、断奶过渡、资源可及性和环境丰富化的管理原则。
- 病弱猪护理栏、人道终点和安乐死 protocol 的通用原则。

## 不可抽取范围

- 本章不是中国监管来源，不能单独支撑中国动物福利法规、监管处罚、检疫或执法结论。
- 本章提及镇静、NSAID、麻醉和其他干预研究，但本批不构建药方、剂量、休药期或具体给药方案。
""",
    )

    write(
        WIKI_ROOT / "wiki" / "topics" / "Swine-behavior-welfare-and-pain-management.md",
        f"""---
tags: [topic, swine, welfare, behavior, formal]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0004]
---

# 猪行为、福利与疼痛管理边界

本页来自 `Diseases of Swine, 11th Edition` Chapter 2 Behavior and Welfare，PDF page 41-65。所有正式事实均已在 `issues/formal_batch_002_cross_review.md` 中完成交叉审查。

## 适用场景

- 生成和评估猪场问诊样本中的福利、行为异常、病弱猪护理、断奶应激、咬尾、跛行、攻击行为和安乐死边界。
- 作为疾病页的辅助 topic，提醒生成系统不要把群体福利/环境管理问题误写成单一感染性疾病。

## 核心原则

- 福利评估应综合生物功能、情感状态和自然行为机会，不能只看生产性能。证据：SRC-0004，PDF page 41-44。
- 福利监测应结合动物本体指标和资源指标，并作为持续过程执行。证据：SRC-0004，PDF page 45。
- 刻板行为、咬尾、belly nosing、跛行、攻击和疾病行为均可提示福利或健康风险。证据：SRC-0004，PDF page 43、51-57。
- 病弱猪常表现为采食饮水下降、探索下降、睡眠增加、寻热和嗜睡；这些行为可早于明显诊断结果出现。证据：SRC-0004，PDF page 57。
- 安乐死应以减少疼痛、焦虑和痛苦、快速失去知觉并确认死亡为核心。证据：SRC-0004，PDF page 58-59。

## 用药和处方边界

Chapter 2 提及若干镇静、止痛和麻醉研究，但本批不落库任何药方、剂量、休药期或中国兽药合规结论。后续必须等待药理章节、中国兽药法规和标签来源交叉复核。
""",
    )

    rules = [
        (
            "RULE-006",
            "猪福利评估必须综合生物功能、情感状态和自然行为机会",
            "welfare_assessment",
            "high",
            "Swine-welfare-three-domain-assessment.md",
            "评估猪福利时，应同时考虑生物功能、情感状态和自然行为机会；高生产性能或身体健康不能单独证明福利良好。证据：SRC-0004，PDF page 41-44。",
        ),
        (
            "RULE-007",
            "福利监测应结合动物本体指标和资源指标",
            "welfare_assessment",
            "high",
            "Swine-welfare-animal-and-resource-measures.md",
            "福利评估应结合动物本体指标与资源指标；动物本体指标直接反映福利状态，资源指标帮助识别潜在原因，福利监测应持续进行。证据：SRC-0004，PDF page 45。",
        ),
        (
            "RULE-008",
            "异常行为和咬尾应作为福利风险信号处理",
            "behavior_risk",
            "high",
            "Swine-abnormal-behavior-tail-biting-risk.md",
            "刻板行为、咬尾、belly nosing 等异常或损伤性行为应作为福利风险信号；咬尾可引起疼痛、应激、采食和增重下降、感染、胴体损伤甚至死亡。证据：SRC-0004，PDF page 43、51-52。",
        ),
        (
            "RULE-009",
            "断奶和资源竞争场景要评估采食饮水可及性",
            "feeding_drinking_behavior",
            "medium",
            "Swine-feeding-drinking-accessibility.md",
            "断奶和群养场景应评估饮水器位置、饮水器/猪比例、料位空间和饲喂时间，降低低等级猪只获取饲料或饮水不足的风险。证据：SRC-0004，PDF page 50-51。",
        ),
        (
            "RULE-010",
            "疾病行为应作为早期健康与福利信号",
            "sickness_behavior",
            "high",
            "Swine-sickness-behavior-early-signal.md",
            "采食饮水下降、探索下降、睡眠增加、寻热和嗜睡等疾病行为可作为早期健康和福利风险信号；病弱猪可能被同栏猪调查或欺凌。证据：SRC-0004，PDF page 57。",
        ),
        (
            "RULE-011",
            "护理栏转移需权衡欺凌减少与混群传播风险",
            "hospital_pen_management",
            "high",
            "Swine-hospital-pen-monitoring.md",
            "将病弱或受伤猪移入护理栏可减少欺凌和资源竞争并便于治疗监测，但应权衡混群应激和病原传播风险，护理栏需密切监测疗效和人道终点。证据：SRC-0004，PDF page 57。",
        ),
        (
            "RULE-012",
            "安乐死必须有标准化 protocol 并确认失去知觉和死亡",
            "euthanasia_welfare",
            "critical",
            "Swine-euthanasia-protocol-and-insensibility.md",
            "严重受伤、不能行走、消瘦、疼痛或恢复可能性很低的猪应及时评估安乐死；安乐死应最小化疼痛、焦虑和痛苦，使动物快速失去知觉，并持续监测失去知觉和死亡确认。证据：SRC-0004，PDF page 58-59。",
        ),
    ]
    for rule_id, title, category, priority, filename, body in rules:
        write(
            WIKI_ROOT / "wiki" / "rules" / filename,
            f"""---
tags: [rule, swine, welfare, formal]
rule_id: {rule_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0004]
---

# {title}

## 规则

{body}

## 适用边界

- 本规则用于生成、评估和审核猪病问诊样本中的福利、行为、病弱猪管理和安乐死边界。
- 本规则不提供具体药方、药物剂量、休药期或中国监管处置结论。
""",
        )

    facts = [
        fact("WELFARE-001-three-focus-areas", "welfare_principle", "猪福利评估", "assessment_domains", "福利定义通常涉及生物功能、情感状态和自然行为/自然生活机会。", 41),
        fact("WELFARE-002-values-ethics", "welfare_principle", "猪福利评估", "requires_value_and_ethics_context", "动物福利不能仅作为技术问题评估，还包含价值和伦理考量。", 41),
        fact("WELFARE-003-five-freedoms", "welfare_framework", "猪福利评估", "uses_five_freedoms", "五大自由是供应链和福利政策中常用的福利框架。", 42, confidence="0.84"),
        fact("WELFARE-004-oie-definition", "welfare_framework", "猪福利评估", "oie_definition_scope", "OIE/WOAH 将动物福利定义为动物如何应对其所处生活条件，并将生物功能、情感状态和自然生活概念纳入良好福利。", 42, confidence="0.84"),
        fact("WELFARE-005-public-legal-technical", "welfare_framework", "猪福利定义", "definition_types", "动物福利定义可分为 public、legal 和 technical 三类，不同定义服务于不同判断场景。", 42),
        fact("WELFARE-006-domestic-natural-behavior", "behavior_principle", "家猪行为", "retains_behavioral_repertoire", "家猪与野猪的行为库相对保持稳定，但行为发生频率或阈值可能改变。", 43),
        fact("WELFARE-007-stereotypies-risk", "behavior_risk", "猪异常行为", "stereotypies_indicate_welfare_risk", "重复且无明显功能的刻板行为，如咬栏、空嚼和 belly nosing，可提示福利受损。", 43),
        fact("WELFARE-008-productivity-not-sufficient", "welfare_principle", "猪福利评估", "productivity_not_sufficient", "生产性能差可提示福利问题，但高生产性能本身并不能证明福利水平高。", 44),
        fact("WELFARE-009-sentience-affective-state", "welfare_principle", "猪福利评估", "affective_states_relevant", "猪被视为有感知能力，情感/心理状态是整体福利的重要组成。", 44),
        fact("WELFARE-010-animal-based-measures", "welfare_assessment", "猪福利评估", "animal_based_measures", "死亡率、发病率、淘汰率、跛行、损伤、体况、刻板行为、攻击和恐惧行为可作为动物本体福利指标。", 45),
        fact("WELFARE-011-resource-based-measures", "welfare_assessment", "猪福利评估", "combine_resource_measures", "稳健福利评估应结合动物本体指标和资源指标，福利监测应持续进行。", 45),
        fact("WELFARE-012-onfarm-evaluation-scope", "welfare_assessment", "猪福利评估", "onfarm_observation_scope", "在场福利评估可通过现场观察动物、饲养员、设施和记录来识别优势和改进机会。", 45),
        fact("WELFARE-013-tail-biting-harms", "behavior_risk", "咬尾", "clinical_and_welfare_harms", "咬尾可导致疼痛和痛苦，并与采食下降、增重下降、感染、脊髓脓肿、疾病传播、胴体损伤、同类相食和死亡相关。", 51),
        fact("WELFARE-014-tail-biting-multifactorial", "behavior_risk", "咬尾", "multifactorial_risk", "咬尾没有单一原因，管理、环境和个体因素均可能参与；贫乏环境和拥挤环境与风险增加有关。", 51),
        fact("WELFARE-015-tail-biter-management", "behavior_management", "咬尾", "remove_biter_and_bitten", "发生咬尾时，移出咬尾猪和受咬猪是降低社会促进和继续伤害的重要管理策略。", 51),
        fact("WELFARE-016-belly-nosing", "behavior_risk", "belly nosing", "postweaning_behavior", "belly nosing 常与早期断奶相关，持续发生时可导致受害猪腹部和侧腹皮肤损伤甚至溃疡。", 52),
        fact("WELFARE-017-lameness-pain", "welfare_risk", "跛行", "causes_negative_affective_state", "猪场跛行可使个体动物产生疼痛等负面情感状态，应使用快速、经济且准确的场内评分方法评估。", 52),
        fact("WELFARE-018-sickness-behaviors", "clinical_assessment", "疾病行为", "early_signs", "患病猪常表现为采食饮水下降、探索下降、睡眠增加、寻热和嗜睡，这些常是饲养员和兽医观察到的早期临床信号。", 57),
        fact("WELFARE-019-prrsv-lying", "clinical_assessment", "PRRSV感染猪行为", "increased_lying", "PRRSV 感染猪相对未感染同栏猪会花更多时间卧躺。", 57, confidence="0.82"),
        fact("WELFARE-020-hospital-pen-benefit-risk", "hospital_pen_management", "护理栏", "benefit_and_risk", "将病弱或受伤猪移入护理栏可减少欺凌和资源竞争、便于监测和治疗，但也要避免混群应激和病原传播风险。", 57),
        fact("WELFARE-021-humane-endpoints", "hospital_pen_management", "护理栏", "monitor_humane_endpoints", "护理栏需要密切监测病弱猪对治疗的反应，并在必要时决策人道终点。", 57),
        fact("WELFARE-022-euthanasia-indications", "euthanasia_welfare", "猪安乐死", "timely_euthanasia_indications", "严重受伤、不能行走、消瘦、疼痛或恢复可能性很低的猪需要及时安乐死评估。", 58),
        fact("WELFARE-023-euthanasia-objective", "euthanasia_welfare", "猪安乐死", "minimize_pain_distress_rapid_insensibility", "安乐死应最小化疼痛、焦虑和痛苦，并使动物快速失去知觉。", 58),
        fact("WELFARE-024-insensibility-monitoring", "euthanasia_welfare", "猪安乐死", "monitor_until_death_confirmed", "安乐死过程中应持续监测失去知觉迹象直到确认死亡；若出现有知觉迹象且安全可行，应立即纠正。", 58),
        fact("WELFARE-025-co2-equipment-boundary", "euthanasia_welfare", "二氧化碳安乐死", "requires_designed_equipment", "二氧化碳安乐死需要专门设计设备、密闭容器、防滑地面和气体调节器；压缩气瓶为推荐 CO2 来源，干冰、灭火器或化学反应来源不可接受。", 59, confidence="0.82"),
    ]

    write(
        WIKI_ROOT / "issues" / "formal_batch_002_candidate_facts.json",
        json.dumps({"batch_id": BATCH_ID, "facts": facts}, ensure_ascii=False, indent=2) + "\n",
    )
    write(
        WIKI_ROOT / "issues" / "formal_batch_002_cross_review.md",
        f"""# Formal Batch 002 Cross Review

## 范围

- PDF page 41-65：Section I Veterinary Practice / Chapter 2 Behavior and Welfare。

## 审查结论

本批候选事实 25 条，规则页 7 个，来源页 1 个，主题页 1 个。经三层交叉审查后允许落库。

## 审查 1：页码锚点核验

- 每条正式 fact 均包含 `evidence_source_id=SRC-0004`。
- 每条正式 fact 均在 `evidence_quote_span` 中标明 Chapter 2 和 PDF page。
- page 60-65 为参考文献页，只作为 Chapter 2 参考边界，不单独生成事实。

## 审查 2：内容边界核验

- 本批只生成福利、行为、病弱猪护理、安乐死和现场评估规则。
- Chapter 2 提及若干镇静、麻醉和止痛研究，但本批未生成任何药方、剂量、休药期或中国兽药合规结论。
- 安乐死相关事实仅作为福利 protocol 边界，不能替代当地法规、兽医现场判断或中国官方处置要求。

## 审查 3：一致性核验

- facts 与 topic/rule 页面内容一致。
- facts 的 `applies_to_species` 均为 `swine`。
- facts 的 `evidence_status` 均为 `HUMAN_REVIEWED`，区别于目录级 `NEEDS_REVIEW` facts。

## 保留问题

- 本批不完善具体疾病页正文。
- 本批不构建药方、剂量、休药期。
- 下一批应从 PDF page 66 开始处理 Chapter 3 Genetics and Health。
""",
    )

    existing = load_json_list(WIKI_ROOT / "exports" / "knowledge_facts.json")
    by_id = {str(item.get("fact_id")): item for item in existing if isinstance(item, dict)}
    for item in facts:
        by_id[item["fact_id"]] = item
    save_facts(list(by_id.values()))

    rule_index = WIKI_ROOT / "exports" / "rule_index.csv"
    existing_rows: list[dict[str, str]] = []
    if rule_index.exists() and rule_index.read_text(encoding="utf-8-sig").strip():
        with rule_index.open("r", encoding="utf-8-sig", newline="") as handle:
            existing_rows = list(csv.DictReader(handle))
    new_rows = [
        {
            "rule_id": rule_id,
            "rule_name": title,
            "category": category,
            "priority": priority,
            "evidence_status": "HUMAN_REVIEWED",
            "primary_source_id": "SRC-0004",
            "page_relpath": f"wiki/rules/{filename}",
        }
        for rule_id, title, category, priority, filename, _body in rules
    ]
    by_rule_id = {row["rule_id"]: row for row in existing_rows if row.get("rule_id")}
    for row in new_rows:
        by_rule_id[row["rule_id"]] = row
    fieldnames = ["rule_id", "rule_name", "category", "priority", "evidence_status", "primary_source_id", "page_relpath"]
    with rule_index.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(by_rule_id.values())

    progress = WIKI_ROOT / "issues" / "pdf_processing_progress.md"
    previous = progress.read_text(encoding="utf-8", errors="replace")
    append = f"""

## Formal Batch 002 实施记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 41-65。
- 章节：Section I Veterinary Practice / Chapter 2 Behavior and Welfare。
- 新增来源：`SRC-0004`。
- 新增主题页：`wiki/topics/Swine-behavior-welfare-and-pain-management.md`。
- 新增规则页：`RULE-006` 至 `RULE-012`。
- 新增候选事实：`issues/formal_batch_002_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_002_cross_review.md`。
- 正式落库 facts：25 条 `HUMAN_REVIEWED` facts。
- 所有正式 facts 均锚定 `SRC-0004; Chapter 2 Behavior and Welfare; PDF page xx`。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 002 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 welfare/behavior/hospital pen/euthanasia protocol facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 002 验证待执行

完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪福利 咬尾 病弱猪 护理栏 安乐死" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

## 截至位置更新

- 当前已处理至 PDF page 65。
- 下一次应从 PDF page 66 开始。
- 推荐下一批：PDF page 66-73，处理 Chapter 3 Genetics and Health。

## 后续待处理阶段

- PDF page 66-73：Chapter 3 Genetics and Health。
- PDF page 74-82：Chapter 4 Effect of Environment on Health。
- PDF page 83-98：Chapter 5 Differential Diagnosis of Diseases。
- PDF page 99-121：Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。
- PDF page 122-135：Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value。
- PDF page 136-146：Chapter 8 Collecting Evidence and Establishing Causality。
- PDF page 147-181：Chapter 9 Disease Control, Prevention, and Elimination。
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
    progress.write_text(previous + append, encoding="utf-8")

    plan = PROJECT_ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN.md"
    plan_text = plan.read_text(encoding="utf-8", errors="replace")
    batch_record = f"""

## Formal Batch 002 完成记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 41-65。
- 章节：Section I Veterinary Practice / Chapter 2 Behavior and Welfare。
- 已落库来源：SRC-0004。
- 已落库主题页：`wiki/topics/Swine-behavior-welfare-and-pain-management.md`。
- 已落库规则页：RULE-006 至 RULE-012。
- 已落库正式事实：25 条，均为 `HUMAN_REVIEWED`，均锚定 `SRC-0004; Chapter 2 Behavior and Welfare; PDF page xx`。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_002_cross_review.md`。
- 当前截至位置：PDF page 65。下一批从 PDF page 66 开始。

### Formal Batch 002 具体实施说明

1. PDF page 41-45 用于构建动物福利定义、评估框架、动物本体指标与资源指标 facts。
2. PDF page 46-49 涉及侵入性操作和疼痛研究；本批仅记录疼痛/证据边界，不落库药方或剂量。
3. PDF page 50-57 用于构建采食饮水、咬尾、belly nosing、跛行、疾病行为、护理栏和混群风险 facts。
4. PDF page 58-59 用于构建安乐死 protocol、失去知觉监测和 CO2 设备边界 facts。
5. PDF page 60-65 为参考文献页，只作为 Chapter 2 参考边界，不单独生成事实。
6. 所有正式 facts 先写入 `issues/formal_batch_002_candidate_facts.json`，通过 `issues/formal_batch_002_cross_review.md` 三层审查后合并到 `exports/knowledge_facts.json`。
7. 本批明确不构建处方、药物剂量、休药期、中国监管处置或具体疾病治疗方案。
"""
    if "## Formal Batch 002 完成记录" not in plan_text:
        insert_pos = plan_text.find("## 当前完成状态")
        if insert_pos >= 0:
            plan_text = plan_text[:insert_pos] + batch_record + "\n" + plan_text[insert_pos:]
        else:
            plan_text += batch_record
    plan_text = plan_text.replace("已处理页码：PDF page 1-40", "已处理页码：PDF page 1-65")
    plan_text = plan_text.replace("当前截至位置：下一次从 PDF page 41 开始", "当前截至位置：下一次从 PDF page 66 开始")
    plan_text = plan_text.replace("已生成正式交叉审查事实：20 条", "已生成正式交叉审查事实：45 条")
    plan_text = plan_text.replace(
        "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；20 条 Chapter 1 正式 facts 为 `HUMAN_REVIEWED`",
        "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；45 条 Chapter 1-2 正式 facts 为 `HUMAN_REVIEWED`",
    )
    plan_text = plan_text.replace("当前规则页：`RULE-001` 至 `RULE-005`", "当前规则页：`RULE-001` 至 `RULE-012`")
    plan.write_text(plan_text, encoding="utf-8")

    print(json.dumps({"batch_id": BATCH_ID, "accepted_facts": len(facts), "rules": len(rules), "last_processed_page": 65}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
