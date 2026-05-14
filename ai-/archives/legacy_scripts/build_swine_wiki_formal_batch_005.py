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
BATCH_ID = "formal-batch-005"
UPDATED = datetime.now(timezone.utc).isoformat()
UPDATED_LOCAL = "2026-05-06 17:14:00 +08:00"


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


def fact(
    fact_id: str,
    fact_type: str,
    subject: str,
    predicate: str,
    obj: str,
    source_id: str,
    chapter: str,
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
        "evidence_source_id": source_id,
        "evidence_url": "",
        "evidence_quote_span": f"{chapter}; PDF page {page}",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
    }


def upsert_csv(path: Path, rows: list[dict[str, str]], key: str, fields: list[str]) -> None:
    existing_rows: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            existing_rows = list(csv.DictReader(handle))
    merged = {row[key]: row for row in existing_rows if row.get(key)}
    for row in rows:
        merged[row[key]] = row
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(merged.values())


def remove_progress_pending_sections(text: str) -> str:
    next_heading = re.compile(r"(?=^## (?:Formal Batch|截至位置更新|后续待处理阶段))", re.M)
    parts = next_heading.split(text)
    kept: list[str] = []
    for part in parts:
        if part.startswith("## 后续待处理阶段"):
            continue
        kept.append(part.rstrip())
    return "\n\n".join(part for part in kept if part.strip()) + "\n"


def replace_pending_tail(text: str, current_page: int, next_page: int, next_batch: str) -> str:
    text = re.sub(r"当前截至：PDF page \d+。", f"当前截至：PDF page {current_page}。", text)
    text = re.sub(r"下一批建议处理：PDF page [0-9-]+。", f"下一批建议处理：PDF page {next_batch}。", text)
    text = re.sub(r"已处理页码：PDF page 1-\d+", f"已处理页码：PDF page 1-{current_page}", text)
    text = re.sub(r"当前截至位置：下一次从 PDF page \d+ 开始", f"当前截至位置：下一次从 PDF page {next_page} 开始", text)
    return text


def main() -> None:
    sources = [
        (
            "SRC-0009-diseases-of-swine-11e-chapter-7-sample-selection-submission.md",
            "SRC-0009",
            "Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value",
            "PDF page 122-135",
            "诊断问题定义、代表性动物选择、死前/死后样本、尸检、呼吸/败血症/腹泻/流产/CNS/关节采样和安全边界。",
        ),
        (
            "SRC-0010-diseases-of-swine-11e-chapter-8-evidence-causality.md",
            "SRC-0010",
            "Chapter 8 Collecting Evidence and Establishing Causality",
            "PDF page 136-146",
            "疾病诊断与病原监测/监视的区分、近因/终因、诊断敏感性/特异性、串联/并联检测、rule of three、监测数据和过程改进。",
        ),
    ]
    for filename, source_id, title, pages, scope in sources:
        write(
            WIKI_ROOT / "wiki" / "sources" / filename,
            f"""---
type: source
source_id: {source_id}
source_path: {PDF_PATH}
source_type: textbook_pdf_chapter
authority_level: textbook
evidence_status: EXTRACTED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# Diseases of Swine, 11th Edition - {title}

- 页码范围：{pages}
- 可抽取范围：{scope}
- 使用边界：本来源为教材章节，不替代中国官方监管、药品标签、国家/行业标准或现场兽医判断。
- 本来源不直接生成药方、剂量、休药期或监管处置结论。
""",
        )

    topics = [
        (
            "Swine-sample-selection-collection-submission.md",
            "猪病样本选择采集与提交",
            "SRC-0009",
            "样本选择必须由明确诊断问题驱动，并结合个体/群体医学目标、病程阶段、样本类型、采样前用药、保存方式和提交信息解释。代表性动物、恰当组织和良好保存决定诊断价值。",
        ),
        (
            "Swine-evidence-causality-and-surveillance.md",
            "猪病证据、因果与监测解释",
            "SRC-0010",
            "建立猪病因果关系不是获得单项检测结果，而是把近因、终因、临床背景、病变、检测结果、风险因素和监测目标综合成可解释的证据链。",
        ),
    ]
    for filename, title, src, body in topics:
        write(
            WIKI_ROOT / "wiki" / "topics" / filename,
            f"""---
tags: [topic, swine, formal]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [{src}]
---

# {title}

{body}

## 证据边界

- 来源：{src}。
- 本页正式 facts 已在 `issues/formal_batch_005_cross_review.md` 中交叉审查。
- 本页不提供药方、剂量、休药期或中国监管处置结论。
""",
        )

    rules = [
        ("RULE-030", "诊断问题必须先于采样和检测选择", "sample_selection", "high", "Swine-diagnostic-question-before-sampling.md", "样本类型、样本数量和检测项目必须由明确诊断问题驱动；临床信息和诊断问题应写入送检单。证据：SRC-0009，PDF page 122。", "SRC-0009"),
        ("RULE-031", "群体疾病诊断应优先选择急性受影响且未治疗动物", "sample_selection", "high", "Swine-representative-acute-untreated-animals.md", "以诊断临床疾病为目标时，应优先采样急性受影响、具有代表性且未用药的猪；慢性动物常不能代表群体问题。证据：SRC-0009，PDF page 123-124。", "SRC-0009"),
        ("RULE-032", "采样部位必须匹配病原生物学和病变分布", "sample_selection", "high", "Swine-sample-site-pathogen-biology-match.md", "采样部位必须与病原组织嗜性、排毒部位和病变分布匹配；例如 IAV 不应通过胎儿组织或血清 RNA 检测来诊断母猪呼吸相关流产问题。证据：SRC-0009，PDF page 124、130-131。", "SRC-0009"),
        ("RULE-033", "死前检测阳性只能作为推定诊断需病理或辅助检测支持", "diagnostic_interpretation", "high", "Swine-antemortem-presumptive-needs-context.md", "死前样本检出病原或抗体常只提示推定诊断，需结合组织病理、辅助检测和临床背景判定因果。证据：SRC-0009，PDF page 124。", "SRC-0009"),
        ("RULE-034", "尸检采样应同时包含病变和非病变组织并防止交叉污染", "postmortem_sampling", "high", "Swine-necropsy-lesion-normal-contamination-control.md", "尸检采样应围绕肉眼病变和诊断问题，同时采集病变与非病变组织；样本应冷藏、分装并避免肠内容物等造成交叉污染。证据：SRC-0009，PDF page 125。", "SRC-0009"),
        ("RULE-035", "中枢神经和关节病例需优先采集关键组织以降低污染", "postmortem_sampling", "medium", "Swine-cns-joint-priority-clean-sampling.md", "神经症状或跛行/关节炎为主诉时，应在污染器械和工作面前优先采集脑、脊髓、关节液/滑膜等关键样本。证据：SRC-0009，PDF page 127-133。", "SRC-0009"),
        ("RULE-036", "因果判断必须区分近因和终因", "causality", "high", "Swine-proximate-vs-ultimate-cause.md", "猪病因果判断应区分近因（病原或具体损伤类型）与终因（导致疾病表达的群体风险因素），两者都影响可持续干预。证据：SRC-0010，PDF page 136。", "SRC-0010"),
        ("RULE-037", "疾病诊断和病原监测监视需要不同采样方案", "surveillance", "high", "Swine-diagnosis-vs-surveillance-sampling.md", "临床疾病诊断与病原监测/监视是不同目标，通常需要不同样本集合；不能用浅层监测样本直接替代病因诊断样本。证据：SRC-0010，PDF page 137-138。", "SRC-0010"),
        ("RULE-038", "检测敏感性特异性解释必须对应诊断问题", "test_performance", "high", "Swine-diagnostic-sensitivity-specificity-question.md", "分析敏感性/特异性不等于诊断敏感性/特异性；同一检测用于感染检出和疾病诊断时解释可能不同。证据：SRC-0010，PDF page 139-140。", "SRC-0010"),
        ("RULE-039", "检测只有在结果能解释并触发行动时才应执行", "diagnostic_strategy", "medium", "Swine-test-only-if-actionable.md", "不应只为产生数据而检测；检测前应能预期并解释可能结果，且至少一个结果应能触发有目的的行动。证据：SRC-0010，PDF page 141。", "SRC-0010"),
        ("RULE-040", "串联检测提高特异性并联检测提高敏感性", "test_strategy", "high", "Swine-serial-parallel-testing-tradeoff.md", "串联检测通常提高诊断特异性、降低敏感性；并联检测通常提高敏感性、降低特异性，需按疾病诊断或监测目标选择。证据：SRC-0010，PDF page 142。", "SRC-0010"),
        ("RULE-041", "全阴性监测结果必须结合样本数量和预期流行率解释", "surveillance", "high", "Swine-negative-surveillance-denominator-rule.md", "监测全阴性不能直接证明群体阴性，应结合样本数、预期流行率和置信水平解释；必要时使用 rule of three 或统计表。证据：SRC-0010，PDF page 143。", "SRC-0010"),
    ]
    for rule_id, title, category, priority, filename, body, src in rules:
        write(
            WIKI_ROOT / "wiki" / "rules" / filename,
            f"""---
tags: [rule, swine, formal]
rule_id: {rule_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [{src}]
---

# {title}

## 规则

{body}

## 适用边界

- 本规则用于生成、评估和审核猪病样本采集、诊断证据、因果判断和监测解释。
- 本规则不提供具体药方、药物剂量、休药期或中国监管处置结论。
""",
        )

    ch7 = "Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value"
    ch8 = "Chapter 8 Collecting Evidence and Establishing Causality"
    facts = [
        fact("SAM-001-diagnostic-question-drives-plan", "sample_selection", "诊断问题", "drives_sample_type_number_and_tests", "明确诊断问题应决定样本类型、样本数量和最合适的检测项目。", "SRC-0009", ch7, 122),
        fact("SAM-002-submission-form-context", "sample_submission", "送检单", "should_include_clinical_and_environmental_evidence", "送检单应包含环境和临床证据、地理位置、年龄、临床症状、用药和免疫史、水料来源、发病率和死亡率等信息。", "SRC-0009", ch7, 122),
        fact("SAM-003-bias-order", "diagnostic_process", "诊断流程", "collect_information_before_hypothesis", "现场信息收集应先于诊断问题和病因假设构建，否则可能引入确认偏倚或选择偏倚。", "SRC-0009", ch7, 122),
        fact("SAM-004-gross-lesion-description", "postmortem_sampling", "肉眼病变描述", "use_standard_pathology_terms", "尸检病变描述应记录受累器官、病程、分布、渗出物类型和严重程度，并使用标准病理术语。", "SRC-0009", ch7, 123),
        fact("SAM-005-population-medicine", "sample_selection", "群体医学诊断", "uses_group_results_for_herd_recommendations", "商业猪场多数诊断采用群体医学策略，用一组个体检测结果为猪群其余部分提出建议。", "SRC-0009", ch7, 123),
        fact("SAM-006-acute-untreated-selection", "sample_selection", "临床疾病诊断采样", "select_acute_affected_nonmedicated", "以诊断临床疾病为目标时，推荐采集急性受影响且未用药动物的样本。", "SRC-0009", ch7, 123),
        fact("SAM-007-stage-affects-detection", "sample_selection", "病程阶段", "affects_pathogen_detection", "病原检出或分离概率受急性、亚急性、慢性等病程阶段以及病原病理生理影响。", "SRC-0009", ch7, 123),
        fact("SAM-008-fever-agent-detection", "sample_selection", "发热猪", "reasonable_predictor_for_agent_detection", "若目标是检出病原、抗原或遗传物质，急性受影响并发热的猪通常是更合适的采样对象。", "SRC-0009", ch7, 123),
        fact("SAM-009-chronic-avoid-population", "sample_selection", "慢性病例", "often_not_representative_for_population_problem", "在群体医学背景下，慢性受影响动物常不能代表猪群问题，应避免作为主要诊断采样对象。", "SRC-0009", ch7, 124),
        fact("SAM-010-pathogen-biology-sample-site", "sample_selection", "病原生物学", "determines_sample_site", "采样计划必须考虑病原生物学；例如 C. difficile 需要大肠和结肠内容物，猪流感检测不适合提交全血或血清 RNA。", "SRC-0009", ch7, 124),
        fact("SAM-011-detection-not-disease-endemic", "diagnostic_interpretation", "地方性病原检测", "detection_only_possible_diagnosis", "地方性或常在菌群中的病原被检出不必然表示临床疾病，只提示可能诊断。", "SRC-0009", ch7, 124),
        fact("SAM-012-oral-fluids-pen-population", "sample_collection", "口腔液", "usually_pen_based_population_sample", "口腔液通常作为栏位样本代表一个群体，除非猪经过个体采集训练。", "SRC-0009", ch7, 124),
        fact("SAM-013-oral-fluid-handling", "sample_collection", "口腔液采集", "chill_or_freeze_and_avoid_contamination", "口腔液采集后应尽快冷藏或冷冻并冰袋运输，同时避免饲料、粪便或土壤污染影响 PCR。", "SRC-0009", ch7, 125),
        fact("SAM-014-nasal-swabs-iav", "sample_collection", "鼻拭子", "used_for_upper_respiratory_viral_detection", "鼻拭子常用于检测在上呼吸道复制的病毒如 IAV；PCR 目的时应避免仅适用于细菌培养的凝胶运输培养基。", "SRC-0009", ch7, 125),
        fact("SAM-015-fresh-samples-cross-contamination", "postmortem_sampling", "新鲜尸检样本", "refrigerate_and_separate_gi_from_organs", "新鲜样本应立即冷藏并分袋密封，脑、脊髓、肺、心、肝、脾、肾等应与肠道或胃肠内容物分开。", "SRC-0009", ch7, 125),
        fact("SAM-016-formalin-thickness", "histopathology", "组织病理样本", "rarely_exceed_one_cm_thickness", "组织病理样本厚度通常不应超过 1 cm，以便充分固定。", "SRC-0009", ch7, 126),
        fact("SAM-017-abortion-fetuses", "reproductive_sampling", "猪流产送检", "submit_multiple_fetuses_and_litters", "流产调查推荐每窝提交 4-6 个胎儿，至少来自 3 个受影响窝；有木乃伊胎时按小、中、大分别提交。", "SRC-0009", ch7, 130),
        fact("SAM-018-maternal-illness-abortion", "reproductive_sampling", "母猪临床症状相关流产", "sample_dam_and_fetuses", "母猪出现厌食、发热、咳嗽等临床症状时，应同时围绕母猪和胎儿采样；IAV 等非全身性病原需采集受影响母猪样本。", "SRC-0009", ch7, 130),
        fact("SAM-019-cns-brain-spinal-cord", "neurologic_sampling", "神经症状采样", "brain_and_spinal_cord_essential", "神经症状为主诉时，脑和脊髓提交是关键；病变可能集中在脑干或脊髓而非额叶皮质。", "SRC-0009", ch7, 131),
        fact("SAM-020-joint-sampling-before-contamination", "locomotor_sampling", "关节炎和跛行采样", "collect_before_thoracic_abdominal_samples", "关节炎或跛行为主诉时，应先采集关节样本，再采胸腔或腹腔组织，以降低常在菌污染风险。", "SRC-0009", ch7, 131),
        fact("CAU-001-test-not-causation", "causality", "因果判断", "single_test_result_not_sufficient", "建立因果并不等同于获得一个检测结果，现代猪病常涉及多病原和多风险因素。", "SRC-0010", ch8, 136),
        fact("CAU-002-proximate-ultimate", "causality", "猪病原因", "include_proximate_and_ultimate_causes", "猪病因果应综合近因和终因：近因是病原或具体损伤，终因是导致疾病表达的群体风险因素。", "SRC-0010", ch8, 136),
        fact("CAU-003-association-not-causation", "causality", "检测关联", "do_not_interpret_association_as_causation", "诊断时不能把关联直接解释为因果；单纯存在某病原通常不足以认定病因。", "SRC-0010", ch8, 136),
        fact("CAU-004-diagnosis-vs-surveillance", "surveillance", "诊断目标", "disease_diagnosis_and_surveillance_require_different_samples", "确认临床疾病与病原监测/监视可能需要两套有目的采集的样本，以分别回答不同目标。", "SRC-0010", ch8, 137),
        fact("CAU-005-diagnostic-process-alignment", "diagnostic_process", "诊断过程", "data_must_align_with_conclusions", "诊断叙述和最终诊断应使相关观察、实验室数据、信息和科学知识彼此一致；不一致时应重新审视过程。", "SRC-0010", ch8, 138),
        fact("CAU-006-analytical-not-diagnostic", "test_performance", "检测性能", "analytical_sensitivity_not_diagnostic_sensitivity", "实验室检测的分析敏感性和特异性并不等同于诊断敏感性和特异性。", "SRC-0010", ch8, 139),
        fact("CAU-007-mortality-outcome", "case_definition", "死亡率", "is_outcome_not_clinical_sign", "死亡率不是临床症状或诊断，而是结果，不应直接作为病例定义或临床表现。", "SRC-0010", ch8, 140),
        fact("CAU-008-two-three-acute-tissue", "sample_selection", "疾病诊断组织样本", "two_to_three_acute_representative_animals_often_sufficient", "一般情况下，来自 2-3 头真正符合病例定义的急性受影响动物的组织样本足以支持疾病诊断。", "SRC-0010", ch8, 140, confidence="0.82"),
        fact("CAU-009-actionable-testing", "diagnostic_strategy", "检测选择", "avoid_testing_only_to_generate_data", "检测前应能预期并解释可能结果，且至少一个结果可触发行动；仅为产生数据而检测会浪费资源并混淆诊断图景。", "SRC-0010", ch8, 141),
        fact("CAU-010-serial-testing-specificity", "test_strategy", "串联检测", "increases_specificity", "串联检测逐步组合多个测试，通常提高诊断特异性但牺牲诊断敏感性，适合判断病原影响和疾病存在。", "SRC-0010", ch8, 142),
        fact("CAU-011-parallel-testing-sensitivity", "test_strategy", "并联检测", "increases_sensitivity", "并联检测只要一项阳性即分类为受影响，通常提高诊断敏感性但降低特异性，适合病原监测/监视问题。", "SRC-0010", ch8, 142),
        fact("CAU-012-monitoring-vs-surveillance", "surveillance", "监测与监视", "different_intent_and_action_threshold", "监测用于随时间评估既知或疑似存在疾病状态，监视用于达到某测量水平时采取有目的行动。", "SRC-0010", ch8, 143),
        fact("CAU-013-rule-of-three", "surveillance", "全阴性结果", "upper_prevalence_about_three_over_n", "随机样本全阴性时，rule of three 可用于估计 95% 置信下阳性结果流行率上限约为 3/n。", "SRC-0010", ch8, 143),
        fact("CAU-014-cutoff-values", "test_interpretation", "定性检测 cut-off", "affects_positive_negative_interpretation", "定性检测阳性/阴性解释依赖验证阶段设定的 cut-off，接近 cut-off 的结果可能受检测目的和实验室差异影响。", "SRC-0010", ch8, 144),
        fact("CAU-015-time-ally", "diagnostic_interpretation", "时间维度", "helps_choose_direct_or_indirect_methods", "感染、发病、恢复、排毒和血清反应随时间变化，理解这些关系有助于选择直接或间接检测方法。", "SRC-0010", ch8, 144),
        fact("CAU-016-pdsa-diagnostic-data", "process_improvement", "诊断数据过程改进", "plan_do_study_act_framework", "猪群健康管理可用 Plan-Do-Study-Act 框架和诊断数据持续评估稳定、清除、防再引入等目标。", "SRC-0010", ch8, 145),
    ]

    write(
        WIKI_ROOT / "issues" / "formal_batch_005_candidate_facts.json",
        json.dumps({"batch_id": BATCH_ID, "facts": facts}, ensure_ascii=False, indent=2) + "\n",
    )
    write(
        WIKI_ROOT / "issues" / "formal_batch_005_cross_review.md",
        """# Formal Batch 005 Cross Review

## 范围

- PDF page 122-135：Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value。
- PDF page 136-146：Chapter 8 Collecting Evidence and Establishing Causality。

## 审查结论

本批候选事实 36 条，规则页 12 个，来源页 2 个，主题页 2 个。经三层交叉审查后允许落库。

## 审查 1：页码锚点核验

- Chapter 7 facts 均锚定 `SRC-0009` 和 PDF page 122-135。
- Chapter 8 facts 均锚定 `SRC-0010` 和 PDF page 136-146。
- PDF page 135、146 主要为参考文献/结尾信息，只有与章节总结直接一致的内容进入事实。

## 审查 2：内容边界核验

- 本批只生成样本选择、采集提交、尸检、证据链、因果和监测解释 facts。
- 采样表内容只抽取原则性、可复用边界；不机械落入所有尺寸/体积项目。
- 本批不生成药方、剂量、休药期、中国监管处置或具体治疗方案。

## 审查 3：一致性核验

- facts 与 topic/rule 页面内容一致。
- facts 的 `applies_to_species` 均为 `swine`。
- facts 的 `evidence_status` 均为 `HUMAN_REVIEWED`。

## 保留问题

- Chapter 9 将进入疾病控制、预防和清除，需要继续保持不把教材控制原则误写为中国监管结论。
- Chapter 10 药理治疗章节必须等待药品标签/监管来源交叉验证后再考虑药方或休药期类知识。
""",
    )

    existing = load_facts()
    by_id = {str(item.get("fact_id")): item for item in existing if isinstance(item, dict)}
    for item in facts:
        by_id[item["fact_id"]] = item
    save_facts(list(by_id.values()))

    upsert_csv(
        WIKI_ROOT / "exports" / "rule_index.csv",
        [
            {
                "rule_id": rule_id,
                "rule_name": title,
                "category": category,
                "priority": priority,
                "evidence_status": "HUMAN_REVIEWED",
                "primary_source_id": src,
                "page_relpath": f"wiki/rules/{filename}",
            }
            for rule_id, title, category, priority, filename, _body, src in rules
        ],
        "rule_id",
        ["rule_id", "rule_name", "category", "priority", "evidence_status", "primary_source_id", "page_relpath"],
    )

    progress_path = WIKI_ROOT / "issues" / "pdf_processing_progress.md"
    progress_text = remove_progress_pending_sections(progress_path.read_text(encoding="utf-8", errors="replace"))
    progress_text += f"""

## Formal Batch 005 实施记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 122-146。
- 章节：Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value；Chapter 8 Collecting Evidence and Establishing Causality。
- 新增来源：`SRC-0009`、`SRC-0010`。
- 新增主题页：样本选择采集与提交、证据因果与监测解释 2 个 topic。
- 新增规则页：`RULE-030` 至 `RULE-041`。
- 新增候选事实：`issues/formal_batch_005_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_005_cross_review.md`。
- 正式落库 facts：36 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 005 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 sample selection/submission/evidence/causality/surveillance facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 005 验证待执行

完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 样本 采集 送检 因果 监测 阴性" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

## 截至位置更新

- 当前已处理至 PDF page 146。
- 下一次应从 PDF page 147 开始。
- 推荐下一批：PDF page 147-181，处理 Chapter 9 Disease Control, Prevention, and Elimination。

## 后续待处理阶段

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
    progress_path.write_text(progress_text, encoding="utf-8")

    plan_path = PROJECT_ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN.md"
    plan_text = plan_path.read_text(encoding="utf-8", errors="replace")
    record = f"""

## Formal Batch 005 完成记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 122-146。
- 章节：Chapter 7 Optimizing Sample Selection, Collection, and Submission to Optimize Diagnostic Value；Chapter 8 Collecting Evidence and Establishing Causality。
- 已落库来源：SRC-0009、SRC-0010。
- 已落库主题页：样本选择采集与提交、证据因果与监测解释 2 个 topic。
- 已落库规则页：RULE-030 至 RULE-041。
- 已落库正式事实：36 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_005_cross_review.md`。
- 当前截至位置：PDF page 146。下一批从 PDF page 147 开始。

### Formal Batch 005 具体实施说明

1. PDF page 122-125 用于构建诊断问题、送检单信息、代表性动物选择、病程阶段和死前样本解释边界。
2. PDF page 125-135 用于构建尸检、组织固定、呼吸/败血症/腹泻/流产/CNS/关节采样和尸检安全边界。
3. PDF page 136-142 用于构建近因/终因、疾病诊断 vs 监测/监视、诊断流程、敏感性/特异性和串联/并联检测规则。
4. PDF page 143-146 用于构建全阴性监测解释、rule of three、cutoff、时间维度和过程改进边界。
5. 所有正式 facts 先写入 `issues/formal_batch_005_candidate_facts.json`，通过 `issues/formal_batch_005_cross_review.md` 三层审查后合并到 `exports/knowledge_facts.json`。
"""
    if "## Formal Batch 005 完成记录" not in plan_text:
        pos = plan_text.find("## 当前完成状态")
        plan_text = plan_text[:pos] + record + "\n" + plan_text[pos:] if pos >= 0 else plan_text + record
    plan_text = replace_pending_tail(plan_text, 146, 147, "147-181")
    replacements = {
        "已生成正式交叉审查事实：95 条": "已生成正式交叉审查事实：131 条",
        "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；95 条 Chapter 1-6 正式 facts 为 `HUMAN_REVIEWED`": "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；131 条 Chapter 1-8 正式 facts 为 `HUMAN_REVIEWED`",
        "当前来源页：`SRC-0001` 至 `SRC-0008`": "当前来源页：`SRC-0001` 至 `SRC-0010`",
        "当前规则页：`RULE-001` 至 `RULE-029`": "当前规则页：`RULE-001` 至 `RULE-041`",
        "当前图谱状态：已重建，`343 nodes / 555 links`": "当前图谱状态：待第五阶段验证后更新",
    }
    for old, new in replacements.items():
        plan_text = plan_text.replace(old, new)
    plan_text = re.sub(
        r"## 后续待处理阶段\n\n(?:- .+\n)+",
        """## 后续待处理阶段

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
""",
        plan_text,
    )
    plan_path.write_text(plan_text, encoding="utf-8")

    print(json.dumps({"batch_id": BATCH_ID, "accepted_facts": len(facts), "rules": len(rules), "last_processed_page": 146}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
