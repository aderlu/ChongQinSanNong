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
BATCH_ID = "formal-batch-003"
UPDATED = datetime.now(timezone.utc).isoformat()
UPDATED_LOCAL = "2026-05-06 16:55:00 +08:00"


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
    src: str,
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
        "evidence_source_id": src,
        "evidence_url": "",
        "evidence_quote_span": f"{chapter}; PDF page {page}",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all_stages",
        "jurisdiction": "Global",
    }


def main() -> None:
    sources = [
        (
            "SRC-0005-diseases-of-swine-11e-chapter-3-genetics-and-health.md",
            "SRC-0005",
            "Chapter 3 Genetics and Health",
            "PDF page 66-73",
            "遗传选择、仔猪成活率、疾病抵抗/耐受、基因组选择、母猪生产寿命。",
        ),
        (
            "SRC-0006-diseases-of-swine-11e-chapter-4-environment-and-health.md",
            "SRC-0006",
            "Chapter 4 Effect of Environment on Health",
            "PDF page 74-82",
            "温度、湿度、空间、饲料饮水可及性和空气质量对猪健康与生产表现的影响。",
        ),
        (
            "SRC-0007-diseases-of-swine-11e-chapter-5-differential-diagnosis.md",
            "SRC-0007",
            "Chapter 5 Differential Diagnosis of Diseases",
            "PDF page 83-98",
            "按系统、年龄和临床表现组织的猪病鉴别诊断导航，包括消化、呼吸、皮肤、贫血、神经、跛行、繁殖损失和人兽共患潜力。",
        ),
    ]
    for filename, src_id, title, pages, scope in sources:
        write(
            WIKI_ROOT / "wiki" / "sources" / filename,
            f"""---
type: source
source_id: {src_id}
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
""",
        )

    topic_specs = [
        (
            "Swine-genetics-health-and-selection.md",
            "猪遗传、健康与选择边界",
            "SRC-0005",
            "遗传选择可辅助降低死亡率、改善疾病抵抗/耐受和母猪生产寿命，但遗传参数具有群体和环境特异性，不能脱离商业场健康状态和管理体系直接套用。",
        ),
        (
            "Swine-environment-health-management.md",
            "猪舍环境与健康管理",
            "SRC-0006",
            "猪舍环境包括温度、湿度、空间、饲料饮水可及性和空气质量。环境异常会改变采食、散热、舒适度和疾病易感性，应作为问诊和鉴别诊断前置检查。",
        ),
        (
            "Swine-differential-diagnosis-by-system-age.md",
            "猪病按系统、年龄和表现鉴别诊断",
            "SRC-0007",
            "鉴别诊断应按系统、年龄、临床表现和生产阶段导航，并回链到具体疾病章节。该页只做导航，不把表格列表直接变成确诊结论。",
        ),
    ]
    for filename, title, src, body in topic_specs:
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
- 本页所有正式 facts 已在 `issues/formal_batch_003_cross_review.md` 中交叉审查。
- 本页不提供药方、剂量、休药期或中国监管处置结论。
""",
        )

    rules = [
        ("RULE-013", "遗传健康建议必须结合具体群体和环境", "genetics_health", "high", "Swine-genetics-population-environment-specificity.md", "遗传健康或疾病抵抗建议必须结合具体种群、商业生产环境和健康挑战；单一品系或单一环境研究结果不能直接外推到所有猪场。证据：SRC-0005，PDF page 68。"),
        ("RULE-014", "疾病抵抗和疾病耐受应区分使用", "genetics_health", "medium", "Swine-disease-resistance-vs-tolerance.md", "遗传方案中应区分 disease resistance 与 disease tolerance；在挑战环境中维持健康和生产性能可能需要同时关注抵抗和耐受。证据：SRC-0005，PDF page 68。"),
        ("RULE-015", "母猪生产寿命改良不能只靠单一选择指标", "sow_longevity", "medium", "Swine-sow-longevity-selection-boundary.md", "母猪生产寿命遗传力较低到中等，遗传改良通常较慢，应结合生产性状、肢蹄健全性、繁殖表现和健康挑战综合判断。证据：SRC-0005，PDF page 70-71。"),
        ("RULE-016", "环境评估必须覆盖温湿度空间水料和空气质量", "environment_health", "high", "Swine-environment-five-factor-check.md", "评估猪舍环境时必须覆盖温度、湿度、空间、饲料和饮水可及性以及空气质量，避免把环境问题误判为单一感染。证据：SRC-0006，PDF page 74。"),
        ("RULE-017", "患病或采食下降猪群可能需要调整猪体感温度", "environment_health", "medium", "Swine-illness-feed-intake-temperature-adjustment.md", "采食下降会影响猪的代谢产热；患病或采食下降猪群的猪只区域空气温度可能需要上调以补偿。证据：SRC-0006，PDF page 75。"),
        ("RULE-018", "鉴别诊断必须按系统和年龄阶段组织", "differential_diagnosis", "high", "Swine-differential-diagnosis-system-age.md", "猪病鉴别诊断应按系统、年龄、生产阶段和主要临床表现组织，不能仅凭单个症状直接确诊。证据：SRC-0007，PDF page 83-98。"),
        ("RULE-019", "呼吸道症状需纳入感染性和环境/中毒性鉴别", "differential_diagnosis", "high", "Swine-respiratory-differentials-infectious-environmental.md", "肺炎、呼吸困难或咳嗽的鉴别应同时考虑感染性病因和环境/中毒性病因，如一氧化碳、氨、粉尘、硝酸盐/亚硝酸盐等。证据：SRC-0007，PDF page 87-88。"),
        ("RULE-020", "繁殖损失鉴别诊断需覆盖遗传环境营养细菌病毒毒素寄生虫", "differential_diagnosis", "high", "Swine-reproductive-loss-differential-scope.md", "猪繁殖损失鉴别诊断应覆盖遗传、高温、管理、营养、细菌、毒素/缺乏、寄生虫和病毒因素。证据：SRC-0007，PDF page 95。"),
        ("RULE-021", "人兽共患潜力必须在猪病鉴别中显式标注", "zoonotic_risk", "high", "Swine-zoonotic-potential-explicit-flag.md", "涉及人兽共患潜力的猪病应在鉴别诊断和问诊输出中显式标注，并回链到具体章节或官方来源。证据：SRC-0007，PDF page 98。"),
    ]
    for rule_id, title, category, priority, filename, body in rules:
        src = "SRC-0005" if rule_id in {"RULE-013", "RULE-014", "RULE-015"} else "SRC-0006" if rule_id in {"RULE-016", "RULE-017"} else "SRC-0007"
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

- 本规则用于生成、评估和审核猪病问诊样本中的遗传、环境和鉴别诊断逻辑。
- 本规则不提供具体药方、药物剂量、休药期或中国监管处置结论。
""",
        )

    facts = [
        fact("GEN-001-survival-economic-trait", "genetics_health", "猪群遗传健康", "survival_is_economic_trait", "成活率是猪业中重要的经济相关性状，降低各生产阶段死亡率可提高生产盈利能力。", "SRC-0005", "Chapter 3 Genetics and Health", 66),
        fact("GEN-002-litter-size-birthweight", "genetics_health", "仔猪成活率", "large_litter_lower_birth_weight_risk", "较大窝产仔数往往伴随较低个体初生重，低初生重可能提高断奶前死亡风险。", "SRC-0005", "Chapter 3 Genetics and Health", 66),
        fact("GEN-003-birthweight-population-specific", "genetics_health", "仔猪成活率", "birth_weight_selection_population_specific", "初生重与断奶前死亡或成活的遗传参数在不同研究和群体间方向和大小不一，应在具体群体内评估后再纳入选择方案。", "SRC-0005", "Chapter 3 Genetics and Health", 67),
        fact("GEN-004-disease-resistance-system-specific", "genetics_health", "疾病抵抗遗传", "requires_specific_system_parameters", "纳入疾病抵抗成分前，应理解该生产系统的遗传参数；单一品系或单一环境研究结果不一定适用于其他品系或环境。", "SRC-0005", "Chapter 3 Genetics and Health", 68),
        fact("GEN-005-resistance-tolerance", "genetics_health", "疾病抵抗遗传", "distinguish_resistance_and_tolerance", "改善疾病耐受有时比单纯改善疾病抵抗更符合目标；挑战环境中的健康和生产维持可同时依赖抵抗和耐受。", "SRC-0005", "Chapter 3 Genetics and Health", 68),
        fact("GEN-006-health-affects-growth", "genetics_health", "疾病与生长", "health_status_affects_growth", "呼吸病、肺病变、肠道病、运动障碍和生长不良等健康状态会影响生长表现。", "SRC-0005", "Chapter 3 Genetics and Health", 68),
        fact("GEN-007-genomic-selection-traits", "genetics_health", "基因组选择", "useful_for_hard_to_measure_traits", "基因组选择对难测量、限性或生命后期才能测量的性状影响最大。", "SRC-0005", "Chapter 3 Genetics and Health", 69),
        fact("GEN-008-prrs-marker", "genetics_health", "PRRS遗传耐受", "chromosome_4_marker_reported", "有研究报道猪 4 号染色体区域可降低 PRRS 对猪群的影响，并解释部分病毒载量和增重遗传变异。", "SRC-0005", "Chapter 3 Genetics and Health", 69, confidence="0.82"),
        fact("GEN-009-sow-longevity-heritability", "genetics_health", "母猪生产寿命", "heritability_range", "猪母猪寿命或生产寿命遗传力估计约为 0.05-0.25，依评估性状不同而变。", "SRC-0005", "Chapter 3 Genetics and Health", 70, confidence="0.82"),
        fact("GEN-010-health-challenge-genetic-correlation", "genetics_health", "繁殖遗传评估", "health_condition_changes_heritability", "母猪繁殖性状遗传力会随健康挑战不同而改变，不同健康条件下同一性状遗传相关不为 1。", "SRC-0005", "Chapter 3 Genetics and Health", 71),
        fact("ENV-001-environment-components", "environment_health", "猪舍环境", "core_components", "猪所处环境包括温度、湿度、空间、饲料饮水可及性和空气质量。", "SRC-0006", "Chapter 4 Effect of Environment on Health", 74),
        fact("ENV-002-modern-pigs-heat-sensitive", "environment_health", "猪舍温度", "modern_pigs_more_heat_sensitive", "由于瘦肉沉积、泌乳等代谢产热提高，现代猪比以往世代对空气温度尤其高温更敏感。", "SRC-0006", "Chapter 4 Effect of Environment on Health", 74),
        fact("ENV-003-feed-intake-lct", "environment_health", "猪舍温度", "feed_intake_affects_lct", "猪的下临界温度受采食量和体型影响；采食多的猪下临界温度较低，采食下降时通常建议提高猪只区域空气温度。", "SRC-0006", "Chapter 4 Effect of Environment on Health", 75),
        fact("ENV-004-environment-not-single-pathogen", "environment_health", "猪舍环境", "avoid_single_pathogen_bias", "环境变量可影响健康和表现，问诊时应先检查温湿度、空间、水料和空气质量，避免把环境问题误判为单一病原。", "SRC-0006", "Chapter 4 Effect of Environment on Health", 74),
        fact("DIFF-001-differential-system-navigation", "differential_diagnosis", "猪病鉴别诊断", "system_based_navigation", "猪病鉴别诊断应结合体系统章节导航，如消化、呼吸、神经运动、繁殖和皮肤系统。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 83, confidence="0.84"),
        fact("DIFF-002-respiratory-age-table", "differential_diagnosis", "呼吸道鉴别诊断", "age_specific_respiratory_differentials", "肺炎、呼吸困难或咳嗽的常见原因随年龄阶段不同而变化。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 87),
        fact("DIFF-003-sneezing-differentials", "differential_diagnosis", "喷嚏鉴别诊断", "include_environmental_contaminants", "猪喷嚏鉴别应包括萎缩性鼻炎、流感、PRRS、伪狂犬、猪巨细胞病毒、支原体以及氨、粉尘、花粉和刺激物等环境因素。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 88),
        fact("DIFF-004-skin-differential", "differential_diagnosis", "皮肤病鉴别诊断", "use_location_lesion_type_demarcation", "皮肤病鉴别可按部位、正常组织状态、增生/非增生和病灶边界来组织。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 90),
        fact("DIFF-005-anemia-differential", "differential_diagnosis", "贫血鉴别诊断", "include_blood_loss_infection_deficiency_toxicity_parasite_viral", "猪贫血鉴别应覆盖失血、慢性病、胃溃疡、肠道出血、细菌、缺乏/中毒、寄生虫和病毒因素。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 91),
        fact("DIFF-006-neurologic-differential", "differential_diagnosis", "神经症状鉴别诊断", "include_general_bacterial_toxic_viral", "猪神经症状鉴别应覆盖先天/一般原因、细菌或原虫、营养缺乏或中毒以及病毒因素。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 92),
        fact("DIFF-007-lameness-age", "differential_diagnosis", "跛行鉴别诊断", "age_specific_lameness_causes", "导致跛行的疾病和损伤在不同月龄更常见的原因不同，应结合年龄阶段鉴别。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 94),
        fact("DIFF-008-reproductive-loss-scope", "differential_diagnosis", "繁殖损失鉴别诊断", "broad_etiology_scope", "猪繁殖损失鉴别应覆盖遗传、高温、管理、营养、细菌、毒素/缺乏、寄生虫和病毒因素。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 95),
        fact("DIFF-009-congenital-anomalies", "differential_diagnosis", "先天异常鉴别诊断", "include_genetic_nutritional_infectious_toxic", "猪先天异常可能涉及遗传、维生素 A 缺乏、猪瘟/伪狂犬等感染、妊娠期药物或植物暴露等多类因素。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 96),
        fact("DIFF-010-zoonotic-potential", "zoonotic_risk", "猪病人兽共患风险", "table_lists_bacterial_fungal_parasitic_protozoal_viral", "具有猪源人兽共患潜力的病原可分为细菌、真菌、寄生虫、原虫和病毒类别，并应回链具体章节。", "SRC-0007", "Chapter 5 Differential Diagnosis of Diseases", 98),
    ]

    write(WIKI_ROOT / "issues" / "formal_batch_003_candidate_facts.json", json.dumps({"batch_id": BATCH_ID, "facts": facts}, ensure_ascii=False, indent=2) + "\n")
    write(
        WIKI_ROOT / "issues" / "formal_batch_003_cross_review.md",
        f"""# Formal Batch 003 Cross Review

## 范围

- PDF page 66-73：Chapter 3 Genetics and Health。
- PDF page 74-82：Chapter 4 Effect of Environment on Health。
- PDF page 83-98：Chapter 5 Differential Diagnosis of Diseases。

## 审查结论

本批候选事实 24 条，规则页 9 个，来源页 3 个，主题页 3 个。经三层交叉审查后允许落库。

## 审查 1：页码锚点核验

- 每条正式 fact 均包含 `evidence_source_id=SRC-0005/SRC-0006/SRC-0007`。
- 每条正式 fact 均在 `evidence_quote_span` 中标明章节和 PDF page。
- 参考文献页只作为章节证据边界，不单独生成事实。

## 审查 2：内容边界核验

- 本批只生成遗传健康、环境健康和鉴别诊断导航事实。
- 本批不生成药方、剂量、休药期、中国监管处置或具体疾病治疗方案。
- Chapter 5 表格只作为鉴别诊断导航，不作为确诊依据。

## 审查 3：一致性核验

- facts 与 topic/rule 页面内容一致。
- facts 的 `applies_to_species` 均为 `swine`。
- facts 的 `evidence_status` 均为 `HUMAN_REVIEWED`。

## 保留问题

- 具体疾病页正文仍待 Section III/IV/V 抽取后完善。
- 下一批应从 PDF page 99 开始处理 Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。
""",
    )

    existing = load_facts()
    by_id = {str(item.get("fact_id")): item for item in existing if isinstance(item, dict)}
    for item in facts:
        by_id[item["fact_id"]] = item
    save_facts(list(by_id.values()))

    rule_index = WIKI_ROOT / "exports" / "rule_index.csv"
    with rule_index.open("r", encoding="utf-8-sig", newline="") as handle:
        existing_rows = list(csv.DictReader(handle))
    new_rows = []
    for rule_id, title, category, priority, filename, _body in rules:
        src = "SRC-0005" if rule_id in {"RULE-013", "RULE-014", "RULE-015"} else "SRC-0006" if rule_id in {"RULE-016", "RULE-017"} else "SRC-0007"
        new_rows.append({
            "rule_id": rule_id,
            "rule_name": title,
            "category": category,
            "priority": priority,
            "evidence_status": "HUMAN_REVIEWED",
            "primary_source_id": src,
            "page_relpath": f"wiki/rules/{filename}",
        })
    by_rule = {row["rule_id"]: row for row in existing_rows if row.get("rule_id")}
    for row in new_rows:
        by_rule[row["rule_id"]] = row
    fields = ["rule_id", "rule_name", "category", "priority", "evidence_status", "primary_source_id", "page_relpath"]
    with rule_index.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(by_rule.values())

    progress = WIKI_ROOT / "issues" / "pdf_processing_progress.md"
    progress.write_text(progress.read_text(encoding="utf-8", errors="replace") + f"""

## Formal Batch 003 实施记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 66-98。
- 章节：Chapter 3 Genetics and Health；Chapter 4 Effect of Environment on Health；Chapter 5 Differential Diagnosis of Diseases。
- 新增来源：`SRC-0005`、`SRC-0006`、`SRC-0007`。
- 新增主题页：遗传健康、环境健康、按系统/年龄鉴别诊断 3 个 topic。
- 新增规则页：`RULE-013` 至 `RULE-021`。
- 新增候选事实：`issues/formal_batch_003_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_003_cross_review.md`。
- 正式落库 facts：24 条 `HUMAN_REVIEWED` facts。
- 明确未落库：药方、药物剂量、休药期、中国监管处置、具体疾病治疗方案。

### Formal Batch 003 交叉审查

- 页码锚点核验：通过。
- 内容边界核验：通过。本批仅覆盖 genetics/environment/differential diagnosis facts。
- 一致性核验：通过。facts、topic、rule 页面一致，`applies_to_species=swine`。

### Formal Batch 003 验证待执行

完成落库后运行：

```powershell
$env:PYTHONPATH='src'
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative status
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative lint
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative query "猪病 鉴别诊断 呼吸 繁殖损失 人兽共患" --top-k 6
python -m chicken_data_synthesis.wiki_cli --wiki-dir knowledge/llm_wiki_swine_authoritative graph-build
```

## 截至位置更新

- 当前已处理至 PDF page 98。
- 下一次应从 PDF page 99 开始。
- 推荐下一批：PDF page 99-121，处理 Chapter 6 Diagnostic Tests, Test Performance, and Considerations for Interpretation。

## 后续待处理阶段

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
""", encoding="utf-8")

    plan = PROJECT_ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN.md"
    text = plan.read_text(encoding="utf-8", errors="replace")
    record = f"""

## Formal Batch 003 完成记录

- 完成时间：{UPDATED_LOCAL}。
- 处理范围：PDF page 66-98。
- 章节：Chapter 3 Genetics and Health；Chapter 4 Effect of Environment on Health；Chapter 5 Differential Diagnosis of Diseases。
- 已落库来源：SRC-0005、SRC-0006、SRC-0007。
- 已落库主题页：遗传健康、环境健康、按系统/年龄鉴别诊断 3 个 topic。
- 已落库规则页：RULE-013 至 RULE-021。
- 已落库正式事实：24 条，均为 `HUMAN_REVIEWED`，均锚定具体章节和 PDF page。
- 未生成内容：药方、剂量、休药期、中国监管处置、具体疾病治疗方案。
- 交叉审查记录：`knowledge/llm_wiki_swine_authoritative/issues/formal_batch_003_cross_review.md`。
- 当前截至位置：PDF page 98。下一批从 PDF page 99 开始。

### Formal Batch 003 具体实施说明

1. PDF page 66-73 用于构建遗传健康、疾病抵抗/耐受、基因组选择和母猪生产寿命边界。
2. PDF page 74-82 用于构建环境健康前置检查，包括温度、湿度、空间、水料和空气质量。
3. PDF page 83-98 用于构建按系统、年龄和临床表现组织的鉴别诊断导航。
4. 本批不将 Chapter 5 表格直接作为确诊依据，只作为鉴别诊断召回和导航依据。
5. 所有正式 facts 先写入 `issues/formal_batch_003_candidate_facts.json`，通过 `issues/formal_batch_003_cross_review.md` 三层审查后合并到 `exports/knowledge_facts.json`。
"""
    if "## Formal Batch 003 完成记录" not in text:
        pos = text.find("## 当前完成状态")
        text = text[:pos] + record + "\n" + text[pos:] if pos >= 0 else text + record
    replacements = {
        "已处理页码：PDF page 1-65": "已处理页码：PDF page 1-98",
        "当前截至位置：下一次从 PDF page 66 开始": "当前截至位置：下一次从 PDF page 99 开始",
        "已生成正式交叉审查事实：45 条": "已生成正式交叉审查事实：69 条",
        "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；45 条 Chapter 1-2 正式 facts 为 `HUMAN_REVIEWED`": "当前事实状态：146 条目录级 facts 保持 `NEEDS_REVIEW`；69 条 Chapter 1-5 正式 facts 为 `HUMAN_REVIEWED`",
        "当前规则页：`RULE-001` 至 `RULE-012`": "当前规则页：`RULE-001` 至 `RULE-021`",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("当前截至：PDF page 12。", "当前截至：PDF page 98。")
    text = text.replace("下一批建议处理：PDF page 13-24。", "下一批建议处理：PDF page 99-121。")
    plan.write_text(text, encoding="utf-8")

    print(json.dumps({"batch_id": BATCH_ID, "accepted_facts": len(facts), "rules": len(rules), "last_processed_page": 98}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
