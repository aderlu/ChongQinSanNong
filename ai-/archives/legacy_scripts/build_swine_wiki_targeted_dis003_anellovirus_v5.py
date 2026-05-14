from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
ISSUES = WIKI / "issues"
NOW = "2026-05-07T20:45:00+08:00"
SOURCE_ID = "SRC-0083"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in text:
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8", newline="\n")


FACTS = [
    ("TTSUV-001-disease-link-not-established", "diagnostic_boundary", "猪环曲病毒/托克特诺病毒感染", "disease_link_not_clearly_established", "TTSuV 与猪病之间的因果联系尚未清楚建立，单独检出 TTSuV 不应作为疾病定因。", "Chapter 26 Anelloviruses; PDF page 478"),
    ("TTSUV-002-ubiquitous-worldwide", "epidemiology", "猪环曲病毒/托克特诺病毒感染", "ubiquitous_worldwide_and_shared_between_wild_boars_and_domestic_pigs", "TTSuV 被认为在全球广泛存在，同一类 TTSuV 毒株可在野猪和家猪之间循环。", "Chapter 26 Anelloviruses; PDF page 478"),
    ("TTSUV-003-transmission-samples", "transmission", "猪环曲病毒/托克特诺病毒感染", "detected_in_tissues_blood_semen_colostrum_nasal_and_fecal_samples", "TTSuV 可在组织、血液、精液、初乳、鼻腔和粪便样本中检出，提示存在水平和垂直传播可能。", "Chapter 26 Anelloviruses; PDF page 478"),
    ("TTSUV-004-age-detection", "epidemiology", "猪环曲病毒/托克特诺病毒感染", "serum_and_nasal_detection_increases_with_age", "TTSuV 在血清和鼻腔排出物中的检出率随日龄增加，提示传播效率较高。", "Chapter 26 Anelloviruses; PDF page 478"),
    ("TTSUV-005-replication-sites", "pathogenesis", "猪环曲病毒/托克特诺病毒感染", "fetal_high_load_in_lung_heart_spleen_kidney_and_possible_lymphoid_targets", "胎儿中 TTSuV 高浓度见于肺、心、脾和肾；较大猪只的淋巴组织和 T 细胞可能为重要靶位。", "Chapter 26 Anelloviruses; PDF page 478"),
    ("TTSUV-006-no-specific-clinical-signs", "clinical_sign", "猪环曲病毒/托克特诺病毒感染", "no_clinical_signs_specifically_associated_with_ttsuv", "目前没有特异性临床症状可归因于 TTSuV 感染，健康猪中也可高比例检出。", "Chapter 26 Anelloviruses; PDF page 478-479"),
    ("TTSUV-007-experimental-lesions-boundary", "lesion_pattern", "猪环曲病毒/托克特诺病毒感染", "gnotobiotic_pig_inoculation_caused_mild_interstitial_pneumonia_thymic_atrophy_glomerulonephropathy_and_liver_infiltrates", "无菌猪 TTSuV1 组织匀浆接种试验可见轻度间质性肺炎、短暂胸腺萎缩、膜性肾小球肾病和轻度肝淋巴细胞/组织细胞浸润，但常规猪实验资料缺乏。", "Chapter 26 Anelloviruses; PDF page 479"),
    ("TTSUV-008-pcv2-cofactor-undetermined", "differential_diagnosis", "猪环曲病毒/托克特诺病毒感染", "cofactor_role_in_pcv2_systemic_disease_is_undetermined", "TTSuV 是否作为 PCV2 系统性疾病的协同因子仍未确定，需与 PCV2 相关疾病和共感染解释分开。", "Chapter 26 Anelloviruses; PDF page 479"),
    ("TTSUV-009-diagnosis-dna-antibody", "diagnostic_method", "猪环曲病毒/托克特诺病毒感染", "diagnosis_based_on_viral_dna_or_antibodies_no_virus_isolation_protocols", "TTSuV 尚无已描述的病毒分离方案，诊断主要基于病毒 DNA 或抗体检测。", "Chapter 26 Anelloviruses; PDF page 479"),
    ("TTSUV-010-research-methods-only", "diagnostic_boundary", "猪环曲病毒/托克特诺病毒感染", "pcr_and_elisa_methods_are_research_purpose_without_commercial_methods", "TTSuV PCR/qPCR 和 ELISA 方法主要用于研究，教材称无商业化检测方法可用。", "Chapter 26 Anelloviruses; PDF page 479"),
    ("TTSUV-011-public-health-boundary", "public_health_boundary", "猪环曲病毒/托克特诺病毒感染", "no_documented_transmission_of_swine_anelloviruses_to_humans", "教材称尚无猪环曲病毒向人传播的记录；猪源材料或肉品中检出 DNA 的生物学意义未确定。", "Chapter 26 Anelloviruses; PDF page 478"),
    ("TTSUV-012-control-impact-not-established", "control_boundary", "猪环曲病毒/托克特诺病毒感染", "herd_health_impact_and_control_consequences_not_established", "TTSuV 感染对猪群健康的影响和防控后果尚未建立，不能生成固定免疫或净化程序。", "Chapter 26 Anelloviruses; PDF page 479"),
]


def build_source() -> None:
    write_text(WIKI / "wiki" / "sources" / "SRC-0083-diseases-of-swine-11e-chapter-26-anelloviruses.md", f"""---
tags: [source, swine, textbook, formal, v5]
source_id: {SOURCE_ID}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
---

# Diseases of Swine 11e Chapter 26 Anelloviruses

## 范围

- 来源：本地 PDF `docs/Diseases of Swine, 11th Edition ...pdf`。
- 页码范围：PDF page 478-479。
- 批次：Targeted Disease Completion V5 / DIS-003。
- 解析文件：`issues/formal_batch_014_pdf_pages_445_484_extract.txt`。

## 摘要

本来源补充 TTSuV/猪环曲病毒章节中传播、临床症状、病变、诊断、公共卫生和防控边界，重点保留“单独检出不等于定因”和“疾病关联尚未明确”的证据边界。
""")
    path = WIKI / "exports" / "source_index.csv"
    rows = list(csv.reader(path.open("r", encoding="utf-8", newline="")))
    existing = {row[0] for row in rows[1:] if row}
    if SOURCE_ID not in existing:
        rows.append([SOURCE_ID, "Diseases of Swine 11e Chapter 26 Anelloviruses", "PDF page 478-479", "HUMAN_REVIEWED", "wiki/sources/SRC-0083-diseases-of-swine-11e-chapter-26-anelloviruses.md"])
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


def build_facts() -> None:
    path = WIKI / "exports" / "knowledge_facts.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {row.get("fact_id") for row in data}
    new_rows = []
    for fact_id, fact_type, subject, predicate, obj, span in FACTS:
        row = {
            "fact_id": fact_id,
            "fact_type": fact_type,
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "fact_confidence": "0.88",
            "evidence_source": "Diseases of Swine 11e",
            "evidence_source_id": SOURCE_ID,
            "evidence_url": "",
            "evidence_quote_span": span,
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": "Global",
        }
        new_rows.append(row)
        if fact_id not in existing:
            data.append(row)
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    write_text(ISSUES / "v5_003_dis003_anellovirus_candidate_facts.json", json.dumps({
        "batch_id": "targeted-dis003-anellovirus-v5",
        "source_id": SOURCE_ID,
        "facts": new_rows,
    }, ensure_ascii=False, indent=2) + "\n")


def update_disease() -> None:
    disease = WIKI / "wiki" / "diseases" / "DIS-003-anelloviruses-torque-teno-sus-viruses.md"
    marker = "## Targeted Disease Completion / V5 - Chapter 26 Anelloviruses"
    block = f"""{marker}

### 传播途径

- TTSuV 可在组织、血液、精液、初乳、鼻腔和粪便样本中检出，提示存在水平和垂直传播可能（`SRC-0083`, PDF page 478）。
- TTSuV 在血清和鼻腔排出物中的检出率随日龄增加，提示传播效率较高（`SRC-0083`, PDF page 478）。

### 临床症状

- 目前没有特异性临床症状可归因于 TTSuV 感染，健康猪中也可高比例检出（`SRC-0083`, PDF page 478-479）。
- TTSuV 与 PCV2 系统性疾病、PDNS 样病变、增重下降和肺炎等关联仍具争议，不能把 TTSuV 单独检出作为定因（`SRC-0083`, PDF page 479）。

### 剖检变化

- 无菌猪 TTSuV1 组织匀浆接种试验可见轻度间质性肺炎、短暂胸腺萎缩、膜性肾小球肾病和轻度肝淋巴细胞/组织细胞浸润；但常规猪临床病理实验资料缺乏（`SRC-0083`, PDF page 479）。

### 实验室诊断

- TTSuV 尚无已描述的病毒分离方案，诊断主要基于病毒 DNA 或抗体检测（`SRC-0083`, PDF page 479）。
- PCR/qPCR 和 ELISA 方法主要用于研究，教材称无商业化检测方法可用（`SRC-0083`, PDF page 479）。

### 鉴别诊断

- TTSuV 是否作为 PCV2 系统性疾病的协同因子仍未确定，需与 PCV2 相关疾病和共感染解释分开（`SRC-0083`, PDF page 479）。

### 防控要点

- TTSuV 感染对猪群健康的影响和防控后果尚未建立，不能生成固定免疫、净化或用药程序（`SRC-0083`, PDF page 479）。

### 公共卫生边界

- 教材称尚无猪环曲病毒向人传播的记录；猪源材料或肉品中检出 DNA 的生物学意义未确定（`SRC-0083`, PDF page 478）。
"""
    append_once(disease, marker, block)


def write_cross_review() -> None:
    write_text(ISSUES / "v5_003_dis003_anellovirus_cross_review.md", f"""# V5-003 DIS-003 Anellovirus Cross Review

## 范围

- 来源：`issues/formal_batch_014_pdf_pages_445_484_extract.txt`。
- 章节：Chapter 26 Anelloviruses。
- 页码：PDF page 478-479。

## 审查结论

- 新增来源：`SRC-0083`。
- 新增 facts：{len(FACTS)} 条，均为 `HUMAN_REVIEWED`。
- 更新 disease：`wiki/diseases/DIS-003-anelloviruses-torque-teno-sus-viruses.md`。

## 内容边界

- 允许落库：传播样本、潜在水平/垂直传播、无特异临床症状、实验性病变、PCR/ELISA 研究用途、公共卫生未证实传播、防控影响未建立。
- 明确不落库：固定免疫程序、净化程序、处方、监管处置、把 TTSuV 单独检出解释为疾病定因。
""")


def append_progress() -> None:
    block = """

## Targeted Disease Completion V5 / DIS-003 Anelloviruses

- 完成时间：2026-05-07 20:45:00 +08:00。
- 处理范围：Chapter 26 Anelloviruses，PDF page 478-479。
- 新增来源：`SRC-0083`。
- 新增 facts：12 条 `HUMAN_REVIEWED` facts。
- 更新疾病页：`wiki/diseases/DIS-003-anelloviruses-torque-teno-sus-viruses.md`，补充传播途径、临床症状、剖检变化、实验室诊断、鉴别诊断、防控和公共卫生边界。
- 明确边界：TTSuV 与疾病因果关系尚未清楚建立，单独检出不得定因；不得生成固定免疫/净化/用药程序。
"""
    for path in [
        ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V4.md",
        ISSUES / "pdf_processing_progress_v4.md",
        ROOT / "docs" / "SWINE_LLM_WIKI_SYSTEM_USABLE_COMPLETION_PLAN.md",
    ]:
        append_once(path, "## Targeted Disease Completion V5 / DIS-003 Anelloviruses", block)


def main() -> None:
    build_source()
    build_facts()
    update_disease()
    write_cross_review()
    append_progress()
    print("targeted DIS-003 anellovirus v5 built")


if __name__ == "__main__":
    main()
