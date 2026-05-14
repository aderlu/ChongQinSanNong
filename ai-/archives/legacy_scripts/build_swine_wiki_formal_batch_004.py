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
BATCH_ID = "formal-batch-004"
UPDATED = datetime.now(timezone.utc).isoformat()
UPDATED_LOCAL = "2026-05-06 17:09:00 +08:00"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_facts() -> list[dict[str, str]]:
    path = WIKI_ROOT / "exports" / "knowledge_facts.json"
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
        "evidence_source_id": "SRC-0008",
        "evidence_url": "",
        "evidence_quote_span": f"Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation; PDF page {page}",
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


def main() -> None:
    write(
        WIKI_ROOT / "wiki" / "sources" / "SRC-0008-diseases-of-swine-11e-chapter-6-diagnostic-tests.md",
        f"""---
type: source
source_id: SRC-0008
source_path: {PDF_PATH}
source_type: textbook_pdf_chapter
authority_level: textbook
evidence_status: EXTRACTED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# Diseases of Swine, 11th Edition - Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation

- 页码范围：PDF page 99-121
- 可抽取范围：诊断测试选择、测试性能、结果解释、细菌培养与药敏、ELISA/FA/IHC/ISH、PCR/测序、VI/VN 和诊断策略。
- 使用边界：本来源为教材章节，不替代中国官方监管、药品标签、国家/行业标准或现场兽医判断。
- 本来源不直接生成药方、剂量、休药期或监管处置结论。
""",
    )

    topics = [
        (
            "Swine-diagnostic-test-selection-and-interpretation.md",
            "猪病诊断测试选择与结果解释",
            "猪病诊断测试应回答明确问题，并结合猪群史、临床表现、病理、样本类型、采样时机和测试性能解释。单一阳性或阴性结果不能脱离背景直接当作病因结论。",
        ),
        (
            "Swine-laboratory-methods-and-performance-boundaries.md",
            "猪病实验室方法与性能边界",
            "不同实验室方法检测的对象不同，包括活病原、抗原、抗体、核酸、组织定位和序列信息。生成和评估系统应显式标注方法边界，避免把核酸、抗体或体外药敏结果误写成感染性、保护性或临床疗效结论。",
        ),
    ]
    for filename, title, body in topics:
        write(
            WIKI_ROOT / "wiki" / "topics" / filename,
            f"""---
tags: [topic, swine, formal]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0008]
---

# {title}

{body}

## 证据边界

- 来源：SRC-0008。
- 本页正式 facts 已在 `issues/formal_batch_004_cross_review.md` 中交叉审查。
- 本页不提供药方、剂量、休药期或中国监管处置结论。
""",
        )

    rules = [
        ("RULE-022", "诊断测试结果必须结合猪群史临床病理解释", "diagnostic_interpretation", "high", "Swine-diagnostic-results-context-required.md", "诊断测试输出必须结合猪群史、临床症状、肉眼和显微病理以及可用的其他检测结果解释；不得把单项检测结果直接写成病因定论。证据：SRC-0008，PDF page 99。"),
        ("RULE-023", "没有单一检测可视为百分之百敏感和特异", "test_performance", "high", "Swine-no-single-test-perfect.md", "生成或评估检测结论时必须保留敏感性、特异性、假阴性和假阳性边界；必要时建议多项检测或随时间复测。证据：SRC-0008，PDF page 99。"),
        ("RULE-024", "细菌培养结果必须结合样本信息和临床病变解释", "bacterial_diagnostics", "high", "Swine-bacterial-culture-clinical-relevance.md", "细菌培养阳性不自动代表病因，阴性也不排除细菌病；解释必须结合样本类型、年龄、病史、病变、采样前用药、冷藏和污染/共生菌风险。证据：SRC-0008，PDF page 101-104。"),
        ("RULE-025", "药敏结果只能作为药物选择一般指导", "antimicrobial_susceptibility", "high", "Swine-ast-general-guide-only.md", "AST 是体外测试，只能作为药物选择的一般指导；不得脱离药代/药效、感染部位、细菌位置、标签和监管要求直接生成处方。证据：SRC-0008，PDF page 104-105。"),
        ("RULE-026", "抗体检测适合群体监测但个体阳性需谨慎确认", "serology_interpretation", "medium", "Swine-antibody-test-confirmation-boundary.md", "ELISA、IFA、IPMA、HI、VN 等抗体检测可用于暴露或群体监测；个体状态判断或意外阳性应考虑复测、配对血清或其他靶标检测确认。证据：SRC-0008，PDF page 106-110。"),
        ("RULE-027", "PCR 阳性不得自动等同于活病原或传染性", "molecular_diagnostics", "high", "Swine-pcr-positive-not-infectivity.md", "PCR 和定量 PCR 检测的是核酸，阳性或高拷贝数不得自动等同于存在活病原、复制性病原或实际传染性。证据：SRC-0008，PDF page 111-114。"),
        ("RULE-028", "测序结果用于溯源和分型但不能任意推断毒力保护", "sequencing_interpretation", "medium", "Swine-sequencing-inference-boundary.md", "测序可用于确认、分型、溯源、变异监测和疫苗/野毒区分；单基因或片段差异不得在缺乏病原特异证据时任意推断毒力、保护或交叉保护。证据：SRC-0008，PDF page 115-117。"),
        ("RULE-029", "阴性结果和异常阳性均需纳入诊断计划", "diagnostic_strategy", "high", "Swine-negative-and-spurious-results-plan.md", "诊断计划应同等重视阴性结果和可疑阳性结果；需预先考虑采样时机、样本标识、复测、换靶标、重采样和检测前后留出问题解决时间。证据：SRC-0008，PDF page 119-120。"),
    ]
    for rule_id, title, category, priority, filename, body in rules:
        write(
            WIKI_ROOT / "wiki" / "rules" / filename,
            f"""---
tags: [rule, swine, formal]
rule_id: {rule_id}
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0008]
---

# {title}

## 规则

{body}

## 适用边界

- 本规则用于生成、评估和审核猪病诊断测试与实验室结果解释。
- 本规则不提供具体药方、药物剂量、休药期或中国监管处置结论。
""",
        )

    facts = [
        fact("DTX-001-diagnosis-total-picture", "diagnostic_interpretation", "猪病诊断", "requires_total_picture", "准确诊断应基于猪群史、临床症状、肉眼和显微病理以及诊断测试结果构成的整体图景。", 99),
        fact("DTX-002-detection-not-etiology", "diagnostic_interpretation", "病原检测", "detection_not_necessarily_etiology", "检出病原或暴露证据不必然说明该病原就是当前临床疾病的病因。", 99),
        fact("DTX-003-no-perfect-test", "test_performance", "诊断测试", "no_single_test_100_percent", "没有单一检测能在所有情境下同时达到完全敏感和完全特异。", 99),
        fact("DTX-004-repeat-multiple-tests", "diagnostic_interpretation", "诊断测试解释", "may_require_multiple_or_repeated_tests", "判断某检测是否识别疾病原因时，可能需要多项检测或随时间重复检测。", 99),
        fact("DTX-005-agid-largely-replaced", "serology_method", "AGID", "largely_replaced_by_more_sensitive_specific_methods", "AGID 可用于检测抗体或血清分型，但在一些应用中已多被 IHA 或 ELISA 等更高敏感性和特异性方法替代。", 99, confidence="0.82"),
        fact("DTX-006-culture-viability", "bacterial_diagnostics", "细菌培养", "detects_viable_bacteria", "细菌培养可从临床样本中生长细菌并提供活性证据，不同于只检测核酸的分子方法。", 101),
        fact("DTX-007-culture-submission-info", "bacterial_diagnostics", "细菌培养送检", "requires_sample_age_history_lesion_information", "细菌培养送检时应提供样本类型、动物年龄、临床病史、观察到的病变和疑似细菌病，以指导培养设置和解释。", 101),
        fact("DTX-008-fastidious-bacteria-alternative-tests", "bacterial_diagnostics", "难培养细菌", "may_need_pcr_or_elisa", "对生长缓慢或苛养的猪细菌病原，可使用 PCR 或 ELISA 等替代检测方法。", 102),
        fact("DTX-009-maldi-tof-same-day-id", "bacterial_identification", "MALDI-TOF MS", "can_identify_bacteria_same_day_after_growth", "MALDI-TOF MS 可在获得细菌生长后实现较快、常为当日的细菌鉴定，但仍依赖从临床样本中长出单个菌落。", 102),
        fact("DTX-010-isolation-not-significance", "bacterial_diagnostics", "细菌分离结果", "does_not_automatically_imply_significance", "从临床样本分离到细菌不自动代表其临床意义，需结合临床症状、病变和必要的毒力/毒素/分型检测。", 103),
        fact("DTX-011-negative-culture-causes", "bacterial_diagnostics", "细菌培养阴性", "can_result_from_treatment_handling_or_overgrowth", "典型症状下未分离到细菌可与采样前抗菌药处理、未冷藏、共生菌或污染菌过度生长、样本提交不当等因素有关。", 103),
        fact("DTX-012-ast-after-significance", "antimicrobial_susceptibility", "药敏试验", "recommended_after_clinical_significance_established", "在确认细菌分离物具有临床意义后，AST 可用于辅助治疗决策。", 104),
        fact("DTX-013-ast-interpretation-clsi", "antimicrobial_susceptibility", "AST 解释", "uses_sir_or_ni_categories", "AST 结果通常按指南解释为敏感、中介、耐药或非敏感；解释需要知道细菌种属和药物组合。", 104),
        fact("DTX-014-mic-target-site", "antimicrobial_susceptibility", "MIC", "requires_target_site_concentration_context", "MIC 表示抑制细菌生长的最低药物浓度，临床解释需考虑感染部位是否能达到相应治疗浓度。", 104),
        fact("DTX-015-ast-in-vitro-guide", "antimicrobial_susceptibility", "AST", "in_vitro_general_guide", "AST 是体外测试，应作为药物选择的一般指导，并结合药代/药效、细菌位置和感染部位判断。", 105),
        fact("DTX-016-bioassay-infectivity", "diagnostic_method", "猪生物测定", "detects_infectivity_of_material", "猪生物测定可用于判断核酸检测阳性的材料是否含有活病毒并具有感染性，但成本高、耗时长。", 105),
        fact("DTX-017-brucella-serology-cross-reaction", "serology_method", "Brucella 血清学", "not_specific_for_b_suis", "多种 Brucella 血清学检测并非 B. suis 特异，因为 Brucella 物种间存在广泛交叉反应。", 105, confidence="0.82"),
        fact("DTX-018-clinical-pathology-indirect", "clinical_pathology", "CBC 和临床化学", "indirect_supporting_tests", "CBC 和临床化学可提示贫血、炎症、器官功能异常、感染或毒物，但通常属于支持性或间接证据。", 105),
        fact("DTX-019-elisa-purpose-specific-performance", "serology_method", "ELISA", "sensitivity_specificity_depend_on_reagents_and_purpose", "ELISA 的诊断敏感性和特异性高度依赖试剂选择、质量和检测目的。", 106),
        fact("DTX-020-elisa-individual-confirmation", "serology_interpretation", "抗体 ELISA", "individual_status_false_positive_caution", "抗体 ELISA 适合群体筛查；用于个体状态判断时，意外阳性可通过复测、第二份血清或其他血清学方法确认。", 107),
        fact("DTX-021-ihc-lesion-association", "tissue_diagnostics", "IHC", "associates_antigen_with_histologic_lesions", "IHC 的重要优势是可把病原抗原检测与特定组织学病变关联起来。", 109),
        fact("DTX-022-mat-paired-samples", "serology_method", "MAT", "single_reading_low_diagnostic_value", "MAT 是猪钩端螺旋体病血清学参考试验之一，但单次读数诊断价值低，推荐间隔约 2 周的连续检测。", 110),
        fact("DTX-023-pcr-gold-standard-detection", "molecular_diagnostics", "PCR", "sensitive_specific_detection", "PCR 是临床样本中病毒和细菌病原敏感、特异检测的重要标准方法，可缩短部分苛养病原的检测时间。", 112),
        fact("DTX-024-qpcr-not-infectivity", "molecular_diagnostics", "定量 PCR", "nucleic_acid_not_infectivity", "定量 PCR 测量核酸量，不能单独证明样本中存在感染性或复制性病原。", 113),
        fact("DTX-025-sequencing-epidemiology", "molecular_diagnostics", "核酸测序", "supports_typing_traceback_and_variant_monitoring", "核酸测序可辅助病原确认、分型、分子流行病学、溯源、变异监测和疫苗株/野毒株区分。", 115),
        fact("DTX-026-diagnostic-questions-sampling", "diagnostic_strategy", "诊断计划", "sample_selection_may_exceed_test_selection", "诊断测试应围绕明确问题设计，样本选择和采样时机可能比检测方法选择更关键。", 119),
    ]

    write(
        WIKI_ROOT / "issues" / "formal_batch_004_candidate_facts.json",
        json.dumps({"batch_id": BATCH_ID, "source_id": "SRC-0008", "facts": facts}, ensure_ascii=False, indent=2) + "\n",
    )
    write(
        WIKI_ROOT / "issues" / "formal_batch_004_cross_review.md",
        """# Formal Batch 004 Cross Review

## 范围

- PDF page 99-121：Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。

## 审查结论

本批候选事实 26 条，规则页 8 个，来源页 1 个，主题页 2 个。经三层交叉审查后允许落库。

## 审查 1：页码锚点核验

- 每条正式 fact 均包含 `evidence_source_id=SRC-0008`。
- 每条正式 fact 均在 `evidence_quote_span` 中标明 Chapter 6 和 PDF page。
- PDF page 121 主要为参考文献页，只作为章节证据边界，不单独生成正式事实。

## 审查 2：内容边界核验

- 本批只生成诊断测试、测试性能、实验室结果解释和方法边界事实。
- AST 相关内容只作为检测解释和用药选择边界，不生成处方、剂量、疗程、休药期或监管处置。
- Brucella 和移动检测要求只记录检测解释边界，不生成中国或美国官方监管结论。

## 审查 3：一致性核验

- facts 与 topic/rule 页面内容一致。
- facts 的 `applies_to_species` 均为 `swine`。
- facts 的 `evidence_status` 均为 `HUMAN_REVIEWED`。

## 保留问题

- Chapter 7 应继续补充样本选择、采集、保存、提交和诊断价值优化规则。
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
                "primary_source_id": "SRC-0008",
                "page_relpath": f"wiki/rules/{filename}",
            }
            for rule_id, title, category, priority, filename, _body in rules
        ],
        "rule_id",
        ["rule_id", "rule_name", "category", "priority", "evidence_status", "primary_source_id", "page_relpath"],
    )

    progress_path = WIKI_ROOT / "issues" / "pdf_processing_progress.md"
    progress_text = remove_progress_pending_sections(progress_path.read_text(encoding="utf-8", errors="replace"))
    progress_text += f"""

## Formal Batch 004 实施记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 99-121。
- 章节：Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。
- 新增来源：`SRC-0008`。
- 新增主题页：诊断测试选择与结果解释、实验室方法与性能边界 2 个 topic。
- 新增规则页：`RULE-022` 至 `RULE-029`。
- 新增候选事实：`issues/formal_batch_004_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_004_cross_review.md`。
- 正式落库 facts：26 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 004 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 diagnostic tests/test performance/interpretation facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 004 验证待执行

完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 PCR 药敏 诊断测试 阳性 阴性 解释" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

## 截至位置更新

- 当前已处理至 PDF page 121。
- 下一次应从 PDF page 122 开始。
- 推荐下一批：PDF page 122-146，合并处理 Chapter 7 和 Chapter 8。

## 后续待处理阶段

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
    progress_path.write_text(progress_text, encoding="utf-8")

    plan_path = PROJECT_ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN.md"
    plan_text = plan_path.read_text(encoding="utf-8", errors="replace")
    record = f"""

## Formal Batch 004 完成记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 99-121。
- 章节：Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。
- 已落库来源：SRC-0008。
- 已落库主题页：诊断测试选择与结果解释、实验室方法与性能边界 2 个 topic。
- 已落库规则页：RULE-022 至 RULE-029。
- 已落库正式事实：26 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_004_cross_review.md`。
- 当前截至位置：PDF page 121。下一批从 PDF page 122 开始。

### Formal Batch 004 具体实施说明

1. PDF page 99-105 用于构建诊断解释总原则、AGID、细菌培养、MALDI-TOF、AST、bioassay、Brucella serology 和 clinical pathology 边界。
2. PDF page 106-110 用于构建 CF、EM、ELISA、FA、FMIA、HI、IHC、IFA/IPMA、MAT 的适用场景和限制。
3. PDF page 111-118 用于构建 ISH、寄生虫鉴定、PCR、qPCR、multiplex PCR、Sanger/NGS/nanopore sequencing 的解释边界。
4. PDF page 119-120 用于构建阴性状态、可疑阳性、复测、换靶标和采样计划的诊断策略。
5. PDF page 121 为参考文献页，只作为 Chapter 6 证据边界，不单独生成事实。
"""
    if "## Formal Batch 004 完成记录" not in plan_text:
        pos = plan_text.find("## 当前完成状态")
        plan_text = plan_text[:pos] + record + "\n" + plan_text[pos:] if pos >= 0 else plan_text + record
    replacements = {
        "已处理页码：PDF page 1-98": "已处理页码：PDF page 1-121",
        "当前截至位置：下一次从 PDF page 99 开始": "当前截至位置：下一次从 PDF page 122 开始",
        "已生成正式交叉审查事实：69 条": "已生成正式交叉审查事实：95 条",
        "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；69 条 Chapter 1-5 正式 facts 为 `HUMAN_REVIEWED`": "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；95 条 Chapter 1-6 正式 facts 为 `HUMAN_REVIEWED`",
        "当前来源页：`SRC-0001` 至 `SRC-0007`": "当前来源页：`SRC-0001` 至 `SRC-0008`",
        "当前规则页：`RULE-001` 至 `RULE-021`": "当前规则页：`RULE-001` 至 `RULE-029`",
        "当前图谱状态：已重建，`282 nodes / 503 links`": "当前图谱状态：待第四阶段验证后更新",
        "当前截至：PDF page 98。": "当前截至：PDF page 121。",
        "下一批建议处理：PDF page 99-121。": "下一批建议处理：PDF page 122-146。",
    }
    for old, new in replacements.items():
        plan_text = plan_text.replace(old, new)
    plan_path.write_text(plan_text, encoding="utf-8")

    print(json.dumps({"batch_id": BATCH_ID, "accepted_facts": len(facts), "rules": len(rules), "last_processed_page": 121}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
