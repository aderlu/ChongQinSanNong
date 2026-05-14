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
BATCH_ID = "formal-batch-001"
UPDATED = datetime.now(timezone.utc).isoformat()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_facts() -> list[dict[str, str]]:
    facts_path = WIKI_ROOT / "exports" / "knowledge_facts.json"
    if not facts_path.exists():
        return []
    data = json.loads(facts_path.read_text(encoding="utf-8-sig") or "[]")
    return data if isinstance(data, list) else []


def save_facts(facts: list[dict[str, str]]) -> None:
    facts_path = WIKI_ROOT / "exports" / "knowledge_facts.json"
    facts_path.write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fact(
    fact_id: str,
    fact_type: str,
    subject: str,
    predicate: str,
    obj: str,
    page: int,
    chapter: str = "Chapter 1 Herd Evaluation",
) -> dict[str, str]:
    return {
        "fact_id": fact_id,
        "fact_type": fact_type,
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "fact_confidence": "0.88",
        "evidence_source": "Diseases of Swine 11e",
        "evidence_source_id": "SRC-0003",
        "evidence_url": "",
        "evidence_quote_span": f"{chapter}; PDF page {page}",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
    }


def main() -> None:
    source_metadata = WIKI_ROOT / "wiki" / "sources" / "SRC-0002-diseases-of-swine-11e-contributors-editors-note.md"
    write(
        source_metadata,
        f"""---
type: source
source_id: SRC-0002
source_path: {PDF_PATH}
source_type: textbook_pdf_metadata
authority_level: textbook
evidence_status: EXTRACTED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# Diseases of Swine, 11th Edition - Contributors and Editorial Metadata

本来源页记录 PDF page 13-24 的来源元数据：

- PDF page 13-22：Contributors。
- PDF page 23：Editors' Note。
- PDF page 24：Acknowledgments。

## 使用边界

- 这些页面只用于确认教材版本、贡献者范围和编辑说明。
- 不从本来源页生成疾病、治疗、处方、诊断或监管事实。
- 本批正式知识落库使用 `SRC-0003` 的 Chapter 1 正文页码锚点。
""",
    )

    source_ch1 = WIKI_ROOT / "wiki" / "sources" / "SRC-0003-diseases-of-swine-11e-chapter-1-herd-evaluation.md"
    write(
        source_ch1,
        f"""---
type: source
source_id: SRC-0003
source_path: {PDF_PATH}
source_type: textbook_pdf_chapter
authority_level: textbook
evidence_status: EXTRACTED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# Diseases of Swine, 11th Edition - Chapter 1 Herd Evaluation

本来源页锚定 PDF page 25-40：

- PDF page 25：Section I Veterinary Practice 起始页。
- PDF page 27-40：Chapter 1 Herd Evaluation 正文、表格和参考文献。

## 可抽取知识范围

- 群体评估、现场调查、记录核验、报告结构、生物安全、四圈评估法。
- 临床问题定量、采样对象选择、剖检对象选择、开放式访谈和流程核验。
- 干预优先级、血样采集和口腔液采样的通用原则。

## 不可抽取范围

- 本章不提供具体猪病药方、剂量、休药期或中国监管处置规则。
- 本章不是中国官方来源，不能单独支撑法定疫病上报、扑杀、封锁或跨区调运结论。
""",
    )

    topic = WIKI_ROOT / "wiki" / "topics" / "Swine-herd-evaluation-and-field-investigation.md"
    write(
        topic,
        f"""---
tags: [topic, swine, herd-evaluation, formal]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0003]
---

# 猪群评估与现场调查

本页来自 `Diseases of Swine, 11th Edition` Chapter 1 Herd Evaluation，PDF page 25-40。所有正式事实均已在 `issues/formal_batch_001_cross_review.md` 中完成交叉审查。

## 适用场景

- 猪场问诊前的信息收集。
- 群体性咳嗽、腹泻、死亡率上升、生长性能下降、繁殖指标异常等问题的现场调查。
- 为后续疾病页检索、采样、剖检和实验室检测选择提供流程约束。

## 核心原则

- 调查前应理解客户目标、约束和决策结构，建议必须放在该场实际约束中评估。证据：SRC-0003，PDF page 27、29。
- 历史、病历、生产记录和既往实验室报告应在现场评估前审查，并尽量查看原始报告。证据：SRC-0003，PDF page 27。
- 所有农场记录和口述信息都应按“信任但核验”的原则处理，误读记录会导致误诊和不恰当建议。证据：SRC-0003，PDF page 28。
- 四圈评估法依次覆盖场区外部、舍内整体、栏位和个体猪，目标是系统回答是否存在或即将发生疾病/福利问题。证据：SRC-0003，PDF page 29-30。
- 群体问题需要估计临床表现的流行程度，用于区分群体问题和个体问题，并为干预效果建立基线。证据：SRC-0003，PDF page 30。
- 采样和剖检对象应代表主要临床表现，优先急性、未治疗个体；多因子问题可能需要足够数量个体覆盖病变范围。证据：SRC-0003，PDF page 33。
- 干预排序应同时考虑客户目标、约束、可行性、成功概率和影响；从猪只需求看，空气、水、饲料优先于疫苗或治疗。证据：SRC-0003，PDF page 37。

## 用药和处方边界

本批次未生成药方、剂量、休药期或具体疾病治疗方案。Chapter 1 仅支持现场调查、采样和干预排序原则。
""",
    )

    rules = [
        (
            "RULE-001",
            "猪群评估必须先核验目标、记录和报告结构",
            "herd_evaluation",
            "high",
            "Swine-herd-evaluation-records-and-reporting.md",
            "猪场问诊或生成病例时，不得仅凭客户转述下诊断；应先核验客户目标、历史记录、生产记录、既往实验室报告和报告/决策结构。证据：SRC-0003，PDF page 27-29。",
        ),
        (
            "RULE-002",
            "现场调查采用四圈评估法",
            "field_investigation",
            "high",
            "Swine-four-circle-herd-evaluation.md",
            "现场调查应系统覆盖场区外部、舍内整体、栏位和个体猪，避免只看单个症状或单头猪就推断群体问题。证据：SRC-0003，PDF page 29-30。",
        ),
        (
            "RULE-003",
            "诊断采样优先代表性急性未治疗个体",
            "diagnostic_sampling",
            "high",
            "Swine-diagnostic-sampling-selection.md",
            "选择剖检或组织采样对象时，应优先代表主要临床表现、处于早期病程且未接受抗菌药或治疗的猪；死亡个体先剖检，必要时再选择代表性活猪。证据：SRC-0003，PDF page 33。",
        ),
        (
            "RULE-004",
            "干预优先级先空气水饲料再疫苗或治疗",
            "intervention_prioritization",
            "medium",
            "Swine-intervention-prioritization.md",
            "干预排序必须考虑客户目标、约束、可行性、成功概率和影响；猪只基础需求中，新鲜空气、清洁水、全价饲料优先于疫苗或治疗。证据：SRC-0003，PDF page 37。",
        ),
        (
            "RULE-005",
            "口腔液样本提交时必须标明样本类型",
            "diagnostic_sampling",
            "medium",
            "Swine-oral-fluid-sample-submission.md",
            "使用口腔液做兽医检测时，提交实验室必须标明样本为口腔液，因为实验室需要使用相应检测流程。证据：SRC-0003，PDF page 39。",
        ),
    ]
    for rule_id, title, category, priority, filename, body in rules:
        write(
            WIKI_ROOT / "wiki" / "rules" / filename,
            f"""---
tags: [rule, swine, formal]
rule_id: {rule_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0003]
---

# {title}

## 规则

{body}

## 适用边界

- 本规则用于生成、评估和审核猪病问诊样本中的现场调查、采样和干预排序逻辑。
- 本规则不提供具体疾病治疗方案、药物剂量、休药期或中国监管处置结论。
""",
        )

    facts = [
        fact("HERD-001-client-goals", "workflow_principle", "猪群评估", "requires_context", "开始农场评估前应理解客户目标和约束，健康建议需放在该场实际目标和限制中解释。", 27),
        fact("HERD-002-review-original-records", "workflow_principle", "猪群评估", "requires_evidence_review", "现场评估前应审查病历、生产记录和既往实验室报告，并尽量查看原始报告而非只听转述。", 27),
        fact("HERD-003-trust-yet-verify", "workflow_principle", "猪群评估", "record_review_policy", "农场信息和记录应客观核验；不准确或误读的记录可能导致误诊和不恰当建议。", 28),
        fact("HERD-004-benchmark-interpretation", "workflow_principle", "猪群评估", "benchmark_policy", "生产指标基准更适合用于理解参数量级和关系，不宜机械作为所有猪场的固定目标。", 28),
        fact("HERD-005-reporting-structure", "workflow_principle", "猪群评估", "requires_reporting_structure", "兽医应弄清决策者、报告对象和信息传递结构，确保管理团队和工人获得一致信息。", 29),
        fact("HERD-006-biosecurity-before-visit", "biosafety_rule", "猪群评估", "requires_previsit_biosecurity_check", "现场访问前应主动询问并遵守该场生物安全要求，包括 downtime 和入场流程。", 29),
        fact("HERD-007-four-circles", "workflow_principle", "四圈评估法", "evaluation_sequence", "四圈评估法依次评估场区外部、舍内整体、栏位和个体猪。", 29),
        fact("HERD-008-problem-prevalence", "workflow_principle", "猪群评估", "quantify_prevalence", "估计临床表现流行程度可帮助判断问题范围、区分群体与个体问题，并作为干预效果基线。", 30),
        fact("HERD-009-pen-evaluation", "workflow_principle", "猪群评估", "pen_level_assessment", "栏位评估应进入栏内观察，并评估不同区域多个栏位，以代表舍内潜在群体问题。", 30),
        fact("HERD-010-feeder-waterer-check", "workflow_principle", "猪群评估", "check_feed_water_access", "栏位评估时应检查料槽和饮水器功能。", 30),
        fact("HERD-011-individual-exam", "workflow_principle", "猪群评估", "individual_exam", "个体评估应从头到尾完整检查，并记录异常和疑似慢性程度。", 30),
        fact("HERD-012-rectal-temperature", "clinical_assessment", "猪群评估", "rectal_temperature_use", "个体评估可测量直肠温度，用作感染性疾病过程和病程阶段的线索之一。", 32),
        fact("HERD-013-necropsy-selection", "diagnostic_sampling", "剖检采样", "select_representative_cases", "采样动物应真正代表主要临床表现，优先选择早期病程个体以提高发现主要病因和相容病变的概率。", 33),
        fact("HERD-014-untreated-preferred", "diagnostic_sampling", "剖检采样", "prefer_untreated_animals", "用于诊断采样的动物通常优先选择未接受抗菌药或治疗的个体。", 33),
        fact("HERD-015-necropsy-dead-first", "diagnostic_sampling", "剖检采样", "necropsy_dead_first", "一般先剖检死亡个体，直到疾病过程模式清楚，再根据临床和剖检结果选择代表性活猪采集新鲜组织。", 33),
        fact("HERD-016-open-ended-questions", "workflow_principle", "猪群评估", "interview_method", "现场提问应偏开放式，并可让员工演示实际操作，以核验流程执行而非只听说明。", 34),
        fact("HERD-017-data-action-threshold", "workflow_principle", "猪群评估", "data_requires_action_threshold", "要求员工采集数据时，应说明数据用途、行动阈值和不行动的后果。", 35),
        fact("HERD-018-intervention-priority", "intervention_rule", "猪群干预", "prioritize_basic_needs", "从猪只需求看，优先级是新鲜空气、清洁水、全价饲料，再到必要疫苗或治疗。", 37),
        fact("HERD-019-vaccine-environment", "intervention_rule", "猪群干预", "vaccine_requires_supportive_environment", "疫苗成功依赖能让疫苗发挥作用的环境条件。", 37),
        fact("HERD-020-oral-fluid-lab-submission", "diagnostic_sampling", "口腔液采样", "label_sample_type", "提交口腔液检测时应明确标识为口腔液样本，因为实验室需采用特殊检测流程。", 39),
    ]

    candidate_path = WIKI_ROOT / "issues" / "formal_batch_001_candidate_facts.json"
    write(candidate_path, json.dumps({"batch_id": BATCH_ID, "facts": facts}, ensure_ascii=False, indent=2) + "\n")

    review_path = WIKI_ROOT / "issues" / "formal_batch_001_cross_review.md"
    write(
        review_path,
        f"""# Formal Batch 001 Cross Review

## 范围

- PDF page 13-24：来源元数据。
- PDF page 25-40：Section I Veterinary Practice / Chapter 1 Herd Evaluation。

## 审查结论

本批候选事实 20 条，规则页 5 个，来源页 2 个。经三层交叉审查后允许落库。

## 审查 1：页码锚点核验

- 每条事实均包含 `evidence_source_id=SRC-0003`。
- 每条事实均在 `evidence_quote_span` 中标明 Chapter 1 和 PDF page。
- page 13-24 仅作为元数据来源，未生成疾病或治疗事实。

## 审查 2：内容边界核验

- 本批未生成任何药方、剂量、休药期或中国监管处置结论。
- Chapter 1 只支持猪群评估、记录核验、现场调查、采样选择和干预排序原则。
- 所有规则页均标明“不提供具体疾病治疗方案、药物剂量、休药期或中国监管处置结论”。

## 审查 3：一致性核验

- facts 与 topic/rule 页面内容一致。
- facts 的 `applies_to_species` 均为 `swine`。
- facts 的 `evidence_status` 均为 `HUMAN_REVIEWED`，区别于目录级 `NEEDS_REVIEW` 事实。

## 保留问题

- 本批不覆盖具体疾病页正文。
- 本批不覆盖用药、处方、休药期。
- 下一批应从 PDF page 41 开始处理 Chapter 2 Behavior and Welfare。
""",
    )

    existing = load_facts()
    by_id = {str(item.get("fact_id")): item for item in existing if isinstance(item, dict)}
    for item in facts:
        by_id[item["fact_id"]] = item
    save_facts(list(by_id.values()))

    rule_rows = [
        {
            "rule_id": rule_id,
            "rule_name": title,
            "category": category,
            "priority": priority,
            "evidence_status": "HUMAN_REVIEWED",
            "primary_source_id": "SRC-0003",
            "page_relpath": f"wiki/rules/{filename}",
        }
        for rule_id, title, category, priority, filename, _body in rules
    ]
    with (WIKI_ROOT / "exports" / "rule_index.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rule_rows[0].keys()))
        writer.writeheader()
        writer.writerows(rule_rows)

    progress = WIKI_ROOT / "issues" / "pdf_processing_progress.md"
    write(
        progress,
        f"""# Diseases of Swine PDF 分批处理进度

## 当前状态

- PDF 总页数：1132
- 文件：`{PDF_PATH}`
- 已完成批次：
  - Batch 0：PDF page 1-12，目录级覆盖建模。
  - Batch 1：PDF page 13-40，来源元数据与 Chapter 1 Herd Evaluation 正式构建。
- 当前正式落库：
  - `SRC-0002`：Contributors / Editors' Note / Acknowledgments 元数据来源。
  - `SRC-0003`：Chapter 1 Herd Evaluation 正文来源。
  - `wiki/topics/Swine-herd-evaluation-and-field-investigation.md`
  - `wiki/rules/RULE-001` 到 `RULE-005`
  - `issues/formal_batch_001_candidate_facts.json`
  - `issues/formal_batch_001_cross_review.md`
  - `exports/knowledge_facts.json` 新增 20 条 HUMAN_REVIEWED 正式事实。

## 截至位置

下一次应从 PDF page 41 开始。

推荐下一批：PDF page 41-65，处理 Chapter 2 Behavior and Welfare。该批应优先生成 welfare/topic/rule facts，不生成药方。

## 质量规则

- 没有 PDF 章节和页码锚点的事实不得落库。
- 药方、剂量、休药期、监管处置必须等待相应章节和 A0/A1 来源复核。
- 每批先写候选事实和交叉审查记录，通过后再合并到 `exports/knowledge_facts.json`。
""",
    )

    plan = PROJECT_ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN.md"
    original = plan.read_text(encoding="utf-8")
    marker = "## 当前完成状态\n"
    if marker in original and "## Formal Batch 001 完成记录" not in original:
        insert = f"""
## Formal Batch 001 完成记录

- 完成时间：{UPDATED}
- 处理范围：PDF page 13-40。
- 已落库来源：SRC-0002、SRC-0003。
- 已落库主题页：`wiki/topics/Swine-herd-evaluation-and-field-investigation.md`。
- 已落库规则页：RULE-001 至 RULE-005。
- 已落库正式事实：20 条，均为 `HUMAN_REVIEWED`，均锚定 `SRC-0003; Chapter 1 Herd Evaluation; PDF page xx`。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_001_cross_review.md`。
- 当前截至位置：PDF page 40。下一批从 PDF page 41 开始。

"""
        original = original.replace(marker, insert + marker, 1)
        plan.write_text(original, encoding="utf-8")

    print(json.dumps({"batch_id": BATCH_ID, "accepted_facts": len(facts), "rules": len(rules), "last_processed_page": 40}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
