from __future__ import annotations

import csv
import json
from pathlib import Path

import fitz
import pdfplumber
from pdfminer.high_level import extract_text as pdfminer_extract_text


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
ISSUES = WIKI / "issues"
PDF = next((ROOT / "docs").glob("Diseases of Swine, 11th Edition*.pdf"))
NOW = "2026-05-07T22:15:00+08:00"
BATCH_ID = "formal-batch-030-v6-status-agnostic"
STATUS = "PROCESSED_SOURCE_ANCHORED"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in existing:
        path.write_text(existing.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8", newline="\n")


def extract_pdf_pages(start: int = 1065, end: int = 1111) -> None:
    doc = fitz.open(PDF)
    parts: list[str] = []
    report: list[str] = []
    with pdfplumber.open(PDF) as plumber_pdf:
        for page_no in range(start, end + 1):
            fitz_text = doc[page_no - 1].get_text("text")
            plumber_text = plumber_pdf.pages[page_no - 1].extract_text() or ""
            miner_text = pdfminer_extract_text(str(PDF), page_numbers=[page_no - 1]) or ""
            candidates = {"fitz": fitz_text, "pdfplumber": plumber_text, "pdfminer": miner_text}
            chosen = max(candidates, key=lambda key: len(candidates[key]))
            parts.append(f"\n\n===== PDF page {page_no} ({chosen}) =====\n{candidates[chosen].strip()}\n")
            report.append(
                f"PDF page {page_no}: fitz_chars={len(fitz_text)} "
                f"pdfplumber_chars={len(plumber_text)} pdfminer_chars={len(miner_text)} chosen={chosen}"
            )
    write_text(ISSUES / "formal_batch_030_pdf_pages_1065_1111_extract.txt", "".join(parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_030_pdf_pages_1065_1111_parser_report.txt", "\n".join(report) + "\n")


SOURCES = [
    {
        "source_id": "SRC-0084",
        "title": "Diseases of Swine 11e Chapter 68 Nutrient Deficiencies and Excesses",
        "pages": "PDF page 1065-1078",
        "relpath": "wiki/sources/SRC-0084-diseases-of-swine-11e-chapter-68-nutrient-deficiencies-and-excesses.md",
        "summary": "Chapter 68 covers diagnosis boundaries for nutritional deficiencies and excesses, feed sampling, micronutrients, salt/water interaction, vitamins, trace minerals and mineral toxicities.",
    },
    {
        "source_id": "SRC-0085",
        "title": "Diseases of Swine 11e Chapter 69 Mycotoxins in Grains and Feeds",
        "pages": "PDF page 1079-1095",
        "relpath": "wiki/sources/SRC-0085-diseases-of-swine-11e-chapter-69-mycotoxins-in-grains-and-feeds.md",
        "summary": "Chapter 69 covers mold and mycotoxin risk in grains and feeds, acute and chronic mycotoxicosis patterns, feed testing, aflatoxins, trichothecenes/DON, zearalenone, ergot alkaloids and fumonisins.",
    },
    {
        "source_id": "SRC-0086",
        "title": "Diseases of Swine 11e Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases",
        "pages": "PDF page 1096-1111",
        "relpath": "wiki/sources/SRC-0086-diseases-of-swine-11e-chapter-70-toxic-minerals-chemicals-plants-and-gases.md",
        "summary": "Chapter 70 covers mineral, chemical, plant and gas toxicoses in swine, including diagnostic context, feed/water/environment exposure history, nitrite, sodium ion/water deprivation and manure gas hazards.",
    },
]


FACTS = [
    ("NINF-001-nutrition-linear-diagnosis-boundary", "diagnostic_boundary", "猪营养缺乏与过量综合征", "nutritional_diagnosis_not_linear", "营养缺乏或过量的诊断很少是单一直线式归因，必须结合日粮、阶段、临床表现、病变、生产记录和实验室资料解释。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1067", "Global"),
    ("NINF-002-nutrition-feed-review", "diagnostic_workflow", "猪营养问题调查", "feed_formulation_and_processing_review_required", "怀疑营养因素时，应核查配方、原料变更、混合均匀性、热加工、储存、采食量和水源，而不是只凭一个临床体征定因。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1068-1069", "Global"),
    ("NINF-003-nutrition-reference-values-boundary", "diagnostic_boundary", "猪营养检测", "reference_values_require_context", "血液或组织营养指标参考值需要结合采样部位、年龄、日粮、疾病状态和实验室方法解释，不能机械套用。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1070", "Global"),
    ("NINF-004-salt-water-toxicity", "toxicosis_boundary", "猪钠/盐中毒", "salt_toxicity_depends_on_water_access", "钠或盐相关毒性高度依赖饮水可及性；评估时必须同时追问盐摄入、水源中断、饮水设备和群体暴露。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1071", "Global"),
    ("NINF-005-vitamin-d-toxicity", "toxicosis_pattern", "猪维生素D过量", "vitamin_d_excess_can_cause_mineralization_risk", "长期或过量维生素D摄入可造成毒性风险，解释时需要结合剂量、持续时间以及钙磷和其他矿物质背景。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1072", "Global"),
    ("NINF-006-selenium-toxic-trace", "toxicosis_pattern", "猪硒过量", "selenium_is_highly_toxic_trace_element", "硒是饲料中最具毒性的必需微量元素之一，怀疑时应核查补充源、混料错误和群体暴露。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1073", "Global"),
    ("NINF-007-copper-toxicity", "toxicosis_pattern", "猪铜过量", "copper_toxicity_can_cause_hemolytic_crisis", "铜毒性可导致溶血危象等严重后果，不能把促生长或营养补充语境直接等同为安全无限添加。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1075", "Global"),
    ("NINF-008-mineral-interactions", "nutrition_boundary", "猪矿物质营养", "excess_minerals_can_reduce_absorption_of_others", "过量矿物质可干扰其他矿物质吸收，矿物质异常应按相互作用和整体日粮背景解释。", "SRC-0084", "Chapter 68 Nutrient Deficiencies and Excesses; PDF page 1076", "Global"),
    ("NINF-009-mycotoxin-feed-grains", "toxicosis_source", "猪霉菌毒素中毒", "most_swine_mycotoxin_problems_involve_feed_grains", "多数猪霉菌毒素问题与受毒素产生真菌污染的饲料谷物有关，风险可发生在收获、储存或运输环节。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1079-1080", "Global"),
    ("NINF-010-mycotoxicosis-feed-consumption", "toxicosis_definition", "猪霉菌毒素中毒", "mycotoxicosis_results_from_consumption_of_contaminated_feed", "霉菌毒素中毒源于采食被毒素污染的饲料；临床表现可能急性、亚急性或慢性。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1080-1081", "Global"),
    ("NINF-011-mycotoxin-testing-feed", "diagnostic_boundary", "猪霉菌毒素检测", "feed_testing_supports_but_does_not_replace_case_context", "谷物或饲料霉菌毒素检测可支持暴露判断，但应与采食量、批次、临床表现、病变和其他疾病鉴别一起解释。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1082", "Global"),
    ("NINF-012-aflatoxin-liver-lesions", "lesion_pattern", "猪黄曲霉毒素中毒", "aflatoxicosis_has_hepatic_lesions", "黄曲霉毒素中毒可见肝脏相关病变，急性至亚急性病例可出现沉郁和肝毒性表现。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1082-1083", "Global"),
    ("NINF-013-aflatoxin-additives-boundary", "treatment_boundary", "猪黄曲霉毒素中毒", "feed_additive_claims_not_universal_treatment", "教材关于霉菌毒素吸附剂或预防性添加剂的讨论不能直接生成通用治疗方案、剂量或中国合规结论。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1084", "Global"),
    ("NINF-014-don-feed-refusal", "clinical_pattern", "猪呕吐毒素/DON中毒", "don_is_associated_with_feed_refusal", "DON 是玉米、大麦和小麦等饲料中常见霉菌毒素，可与采食下降或拒食相关，需结合饲料检测和群体表现解释。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1085-1086", "Global"),
    ("NINF-015-mycotoxin-feed-refusal-difficult", "diagnostic_boundary", "猪霉菌毒素相关拒食", "feed_refusal_has_many_differentials", "霉菌毒素相关拒食是复杂诊断问题，不能仅凭拒食就归因于 DON 或其他单一毒素。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1086", "Global"),
    ("NINF-016-zearalenone-estrogenic", "clinical_pattern", "猪玉米赤霉烯酮中毒", "zea_is_estrogenic_mycotoxin", "ZEA 是具有雌激素样作用的霉菌毒素，解释繁殖道或阴户肿胀相关表现时应纳入饲料暴露鉴别。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1088", "Global"),
    ("NINF-017-fumonisin-high-exposure", "toxicosis_pattern", "猪富马毒素中毒", "high_fumonisin_exposure_can_cause_pulmonary_or_hepatic_toxicosis", "高水平富马毒素暴露可造成肺水肿或肝毒性相关问题，饲料检测和临床病理应一起解释。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1091-1092", "Global"),
    ("NINF-018-fumonisin-safe-level-boundary", "regulatory_boundary", "猪富马毒素中毒", "safe_level_requires_authority_or_feed_standard", "富马毒素安全水平或监管限量不能从教材讨论直接外推，需另引官方饲料或监管标准。", "SRC-0085", "Chapter 69 Mycotoxins in Grains and Feeds; PDF page 1092", "Global"),
    ("NINF-019-toxic-agent-history", "diagnostic_workflow", "猪矿物质与化学物中毒", "toxic_agent_assessment_requires_exposure_history", "毒物相关病例评估必须追问饲料、水源、环境、工业污染、药物/添加剂、杀虫剂、垫料和群体暴露史。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1096", "Global"),
    ("NINF-020-iron-toxicity", "toxicosis_pattern", "猪铁中毒", "young_pigs_can_be_susceptible_to_iron_toxicosis", "幼猪可能对铁中毒更敏感；铁过量也可能干扰其他元素利用，需结合补铁和饲料来源解释。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1097", "Global"),
    ("NINF-021-fluorine-sources", "toxicosis_source", "猪氟中毒", "fluorine_exposure_can_come_from_industrial_or_feed_phosphate_sources", "氟暴露可与工业污染、污染土壤作物或含氟较高的饲料级磷酸盐来源相关。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1098", "Global"),
    ("NINF-022-arsenical-differential", "diagnostic_boundary", "猪有机砷/苯胂酸类中毒", "arsenical_toxicosis_can_mimic_neurologic_or_salt_toxicity", "苯胂酸类等有机砷中毒可能与钠离子中毒、有机汞中毒或部分病毒性神经病相混淆。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1099", "Global"),
    ("NINF-023-ionophore-stop-exposure", "control_boundary", "猪离子载体中毒", "ionophore_toxicosis_control_starts_with_stopping_exposure", "怀疑离子载体中毒时，防止进一步中毒的核心是停止相关给药或饲料暴露并核查混料错误。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1100", "Global"),
    ("NINF-024-op-carbamate-signs", "clinical_pattern", "猪有机磷/氨基甲酸酯中毒", "op_or_carbamate_toxicosis_has_cholinergic_signs", "有机磷或氨基甲酸酯中毒可见流泪、缩瞳、呼吸困难、发绀、呼吸道分泌物增多和支气管收缩等胆碱能相关表现。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1101", "Global"),
    ("NINF-025-paraquat-toxicosis", "toxicosis_boundary", "猪百草枯中毒", "paraquat_can_cause_swine_toxicosis", "百草枯可造成猪中毒，相关判断应基于暴露史、临床经过和毒理检测，而非单一非特异症状。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1103", "Global"),
    ("NINF-026-nitrite-acute-signs", "clinical_pattern", "猪亚硝酸盐中毒", "acute_nitrite_toxicosis_has_rapid_systemic_signs", "急性亚硝酸盐中毒可快速出现全身性缺氧相关表现，需结合水源/饲料暴露和实验室证据。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1105", "Global"),
    ("NINF-027-sodium-ion-histology", "diagnostic_boundary", "猪钠离子中毒/水剥夺", "sodium_ion_toxicosis_requires_history_and_histology_context", "钠离子中毒诊断需结合饮水剥夺或盐摄入史、神经表现、病理组织学和鉴别诊断。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1107", "Global"),
    ("NINF-028-toxic-gases-manure", "toxicosis_source", "猪有毒气体与通风失败损伤", "manure_decomposition_can_release_hazardous_gases", "粪污分解可释放氨、硫化氢等有害气体；通风失败、搅动粪池或封闭空间可增加毒性暴露风险。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1108", "Global"),
    ("NINF-029-ammonia-low-level", "toxicosis_boundary", "猪舍氨气暴露", "typical_low_ammonia_less_than_10_ppm_not_toxic_but_context_matters", "教材称动物设施中低于 10 ppm 的常见氨浓度通常无毒，但呼吸道刺激、通风和混合气体暴露仍需结合现场判断。", "SRC-0086", "Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases; PDF page 1109", "Global"),
    ("NINF-030-reference-pages-boundary", "source_boundary", "Section VI 参考文献", "reference_pages_are_boundary_not_standalone_facts", "Chapter 68-70 参考文献页只作为章节完整性和来源边界记录，不生成独立疾病事实。", "SRC-0084", "Chapter 68-70 reference sections; PDF page 1077-1078, 1093-1095, 1110-1111", "Global"),
]


RULES = [
    ("RULE-433", "营养缺乏或过量不得单一线性定因", "nutrition_diagnosis", "critical", "SRC-0084", "Swine-nutritional-diagnosis-not-linear.md", "营养缺乏或过量诊断必须结合日粮、采食、水源、阶段、病变、生产记录和实验室资料，不得凭单一体征或单项检测定因。", "1067-1070"),
    ("RULE-434", "盐/钠相关中毒必须追问饮水可及性", "salt_water_toxicity", "critical", "SRC-0084", "Swine-salt-sodium-toxicity-water-access-required.md", "解释盐或钠相关中毒时必须核查饮水可及性、水源中断和饮水设备；没有饮水背景不得直接定因。", "1071"),
    ("RULE-435", "维生素和微量元素过量不得外推为安全添加", "nutrient_excess_boundary", "high", "SRC-0084", "Swine-vitamin-mineral-excess-not-safe-addition.md", "维生素D、硒、铜等营养素存在毒性边界，营养补充语境不得外推为安全无限添加。", "1072-1076"),
    ("RULE-436", "霉菌毒素诊断必须结合饲料批次和病例背景", "mycotoxin_diagnostics", "critical", "SRC-0085", "Swine-mycotoxin-feed-testing-context-required.md", "霉菌毒素检测结果必须结合饲料批次、采食量、临床表现、病变和鉴别诊断解释，不得把单一阳性检测直接等同病因。", "1079-1082"),
    ("RULE-437", "霉菌毒素吸附剂讨论不得生成通用治疗处方", "mycotoxin_treatment_boundary", "critical", "SRC-0085", "Swine-mycotoxin-additive-not-universal-treatment.md", "教材关于吸附剂或饲料处理的讨论不得生成通用治疗方案、剂量、休药期或中国合规结论。", "1084-1087"),
    ("RULE-438", "DON 相关拒食需要广泛鉴别", "don_feed_refusal", "high", "SRC-0085", "Swine-don-feed-refusal-differentials-required.md", "拒食或采食下降不得自动归因 DON；必须结合饲料检测、批次暴露、其他霉菌毒素和非毒素性原因。", "1085-1086"),
    ("RULE-439", "ZEA 相关繁殖表现必须追溯饲料暴露", "zearalenone_boundary", "high", "SRC-0085", "Swine-zearalenone-reproductive-feed-exposure.md", "阴户肿胀或雌激素样表现可提示 ZEA 暴露，但仍需追溯饲料来源和排除其他繁殖系统问题。", "1088"),
    ("RULE-440", "富马毒素安全水平必须另引官方标准", "fumonisin_regulatory_boundary", "critical", "SRC-0085", "Swine-fumonisin-safe-level-authority-required.md", "富马毒素安全水平、监管限量或饲料放行结论必须另引官方饲料/监管标准，不能从教材讨论直接外推。", "1091-1092"),
    ("RULE-441", "毒物病例必须先建立暴露史", "toxicology_diagnostics", "critical", "SRC-0086", "Swine-toxicology-exposure-history-required.md", "矿物质、化学物、植物和气体中毒评估必须先建立饲料、水源、环境、药物、杀虫剂和群体暴露史。", "1096"),
    ("RULE-442", "有机砷等中毒需与神经病和盐中毒鉴别", "arsenical_differential", "high", "SRC-0086", "Swine-arsenical-neurologic-salt-differential.md", "苯胂酸类等有机砷中毒可能类似钠离子中毒、有机汞中毒或病毒性神经病，不能仅凭神经症状定因。", "1099"),
    ("RULE-443", "离子载体中毒首要边界是停止暴露和核查混料", "ionophore_control", "high", "SRC-0086", "Swine-ionophore-stop-exposure-mixing-error.md", "怀疑离子载体中毒时，回答应优先提示停止相关暴露、隔离问题饲料并核查混料错误，而非生成经验处方。", "1100"),
    ("RULE-444", "有机磷/氨基甲酸酯中毒需保留胆碱能体征组合", "op_carbamate_toxicosis", "high", "SRC-0086", "Swine-op-carbamate-cholinergic-signs.md", "有机磷或氨基甲酸酯中毒解释应保留缩瞳、流泪、呼吸分泌物、支气管收缩等胆碱能体征组合和暴露史。", "1101"),
    ("RULE-445", "亚硝酸盐中毒不得脱离水源/饲料暴露", "nitrite_toxicosis", "critical", "SRC-0086", "Swine-nitrite-water-feed-exposure-required.md", "急性亚硝酸盐中毒判断必须结合水源或饲料暴露、快速缺氧表现和实验室证据，不得用非特异突然死亡单独定因。", "1105"),
    ("RULE-446", "钠离子中毒需要饮水剥夺和组织学背景", "sodium_ion_toxicosis", "critical", "SRC-0086", "Swine-sodium-ion-water-deprivation-histology.md", "钠离子中毒诊断应结合饮水剥夺或盐摄入史、神经症状、组织学和鉴别诊断，不能只凭高盐饲料传闻定因。", "1107"),
    ("RULE-447", "粪污气体和通风失败必须作为群体暴露事件处理", "toxic_gas_boundary", "critical", "SRC-0086", "Swine-manure-gas-ventilation-group-exposure.md", "怀疑粪污气体或通风失败时，应按环境和群体暴露事件解释，重点核查通风、粪池搅动、封闭空间和人员安全。", "1108-1109"),
    ("RULE-448", "教材毒理内容不得直接生成中国执法处置", "toxicology_regulatory_boundary", "critical", "SRC-0086", "Swine-toxicology-textbook-not-china-enforcement.md", "教材毒理事实可用于病因和鉴别，但食品处理、执法、召回、处罚或中国监管处置必须另引 A0/A1 来源。", "1096-1111"),
]


DISEASE_BLOCKS = {
    "DIS-065-nutrient-deficiencies-and-excesses.md": [
        ("实验室诊断", "营养缺乏或过量诊断很少是单一直线式归因；应结合配方、原料变更、混合均匀性、热加工、储存、采食量、水源、临床表现、病变、生产记录和实验室结果解释（`SRC-0084`, PDF page 1067-1070）。"),
        ("鉴别诊断", "营养异常需要与感染性疾病、管理问题、饮水中断、毒物暴露和霉菌毒素问题鉴别；单个体征或单项指标不足以定因（`SRC-0084`, PDF page 1067-1070）。"),
        ("防控要点", "防控重点是日粮和原料审查、加工与储存控制、混料核查、水源保障以及按阶段营养需求管理（`SRC-0084`, PDF page 1068-1076）。"),
    ],
    "DIS-066-mycotoxins-in-grains-and-feeds.md": [
        ("传播途径", "猪霉菌毒素问题多数与污染饲料谷物有关，风险可出现在收获、储存、运输或饲喂环节（`SRC-0085`, PDF page 1079-1080）。"),
        ("临床症状", "霉菌毒素中毒表现可为急性、亚急性或慢性，常见问题包括采食下降、生产性能变化、肝毒性、繁殖异常或特定胆碱/神经样问题，需按毒素类别解释（`SRC-0085`, PDF page 1080-1092）。"),
        ("实验室诊断", "谷物或饲料检测支持暴露判断，但需结合批次、采食量、临床、病变和其他疾病鉴别，不得把单项检测直接等同病因（`SRC-0085`, PDF page 1082）。"),
    ],
    "DIS-067-aflatoxin-toxicosis.md": [
        ("临床症状", "急性至亚急性黄曲霉毒素中毒可出现沉郁和肝毒性相关表现（`SRC-0085`, PDF page 1082-1083）。"),
        ("剖检变化", "黄曲霉毒素中毒可见肝脏相关病变，回答时应与饲料暴露和检测结果共同解释（`SRC-0085`, PDF page 1083）。"),
        ("用药/处置边界", "教材关于添加剂或饲料处理的讨论不得直接生成通用治疗、剂量、休药期或中国饲料放行结论（`SRC-0085`, PDF page 1084）。"),
    ],
    "DIS-068-don-trichothecene-toxicosis.md": [
        ("临床症状", "DON 是玉米、大麦和小麦等饲料中常见霉菌毒素，可与采食下降或拒食相关（`SRC-0085`, PDF page 1085-1086）。"),
        ("鉴别诊断", "采食下降或拒食不是 DON 的特异表现，必须结合饲料检测、批次暴露、其他霉菌毒素和非毒素性原因鉴别（`SRC-0085`, PDF page 1086）。"),
    ],
    "DIS-069-zearalenone-toxicosis.md": [
        ("临床症状", "ZEA 是具有雌激素样作用的霉菌毒素，解释阴户肿胀或繁殖道相关表现时应纳入饲料暴露鉴别（`SRC-0085`, PDF page 1088）。"),
        ("鉴别诊断", "ZEA 相关表现需与正常发情、繁殖系统疾病、管理因素和其他饲料问题区分（`SRC-0085`, PDF page 1088）。"),
    ],
    "DIS-070-fumonisin-toxicosis.md": [
        ("临床症状", "高水平富马毒素暴露可造成肺水肿或肝毒性相关问题；解释时需要饲料检测、临床病理和群体暴露证据（`SRC-0085`, PDF page 1091-1092）。"),
        ("用药/处置边界", "富马毒素安全水平或监管限量不能从教材讨论直接外推，需另引官方饲料或监管标准（`SRC-0085`, PDF page 1092）。"),
    ],
    "DIS-071-toxic-minerals-chemicals-plants-and-gases.md": [
        ("传播途径", "毒物暴露可来自饲料、水源、环境、工业污染、药物/添加剂、杀虫剂、植物、垫料或粪污气体（`SRC-0086`, PDF page 1096-1109）。"),
        ("实验室诊断", "毒物病例需要建立暴露史并结合毒理检测、病理、群体分布和鉴别诊断；非特异症状不能单独定因（`SRC-0086`, PDF page 1096-1111）。"),
        ("鉴别诊断", "有机砷、钠离子中毒、有机汞中毒和部分病毒性神经病可互相混淆，需结合暴露史和组织学/毒理证据（`SRC-0086`, PDF page 1099-1107）。"),
    ],
    "DIS-072-nitrite-toxicosis.md": [
        ("临床症状", "急性亚硝酸盐中毒可快速出现全身性缺氧相关表现，需结合水源或饲料暴露和实验室证据解释（`SRC-0086`, PDF page 1105）。"),
        ("鉴别诊断", "突然死亡或发绀不能单独定因亚硝酸盐中毒，应与其他窒息性、循环性和毒物性事件鉴别（`SRC-0086`, PDF page 1105）。"),
    ],
    "DIS-073-toxic-gases-ventilation-failure.md": [
        ("传播途径", "粪污分解可释放氨、硫化氢等有害气体；通风失败、搅动粪池或封闭空间可增加暴露风险（`SRC-0086`, PDF page 1108-1109）。"),
        ("防控要点", "疑似粪污气体或通风失败事件应按群体环境暴露处理，优先核查通风、粪池搅动、封闭空间和人员安全（`SRC-0086`, PDF page 1108-1109）。"),
    ],
}


AUTHORITY_WEB_SOURCES = [
    ("A0-MOA-573", "农业农村部公告第573号：一、二、三类动物疫病病种名录", "https://xmsyj.moa.gov.cn/gzdt/202206/t20220629_6403635.htm", "China regulatory source for notifiable disease class boundaries."),
    ("A0-MOA-ASF-NORMALIZED-GUIDE", "非洲猪瘟常态化防控技术指南（试行版）", "https://www.moa.gov.cn/nybgb/2020/202009/202011/t20201124_6356917.htm", "China ASF prevention/control source for reporting, movement and testing boundaries."),
    ("A0-MOA-BANNED-DRUG-250-POLICY", "食品动物中禁止使用的药品及其他化合物清单政策入口", "https://www.moa.gov.cn/xw/zwdt/202001/t20200120_6336378.htm", "China banned drug policy entry; concrete drug list still requires original notice verification."),
    ("A1-WOAH-ASF", "WOAH African swine fever disease page", "https://www.woah.org/en/disease/african-swine-fever/", "International authority disease page for ASF boundaries."),
    ("A1-WOAH-FMD", "WOAH Foot and mouth disease disease page", "https://www.woah.org/en/disease/foot-and-mouth-disease/", "International authority disease page for vesicular disease differential boundaries."),
    ("A1-WOAH-CSF", "WOAH Classical swine fever disease page", "https://www.woah.org/en/disease/classical-swine-fever/", "International authority disease page for CSF boundaries."),
    ("A1-WOAH-AUJESZKY", "WOAH Aujeszky's disease disease page", "https://www.woah.org/en/disease/aujeszkys-disease/", "International authority disease page for pseudorabies/Aujeszky's disease."),
    ("A1-WOAH-PRRS", "WOAH PRRS technical disease card/manual entry", "https://www.woah.org/", "Search-verified authority domain entry; exact chapter/manual PDF should be pinned before deriving new PRRS facts."),
]


def make_source_pages() -> None:
    for src in SOURCES:
        write_text(WIKI / src["relpath"], f"""---
tags: [source, swine, textbook, formal, v6]
source_id: {src["source_id"]}
updated: {NOW}
evidence_status: {STATUS}
source_type: textbook_pdf
authority_level: A2
---

# {src["title"]}

## 范围

- 来源：本地 PDF `docs/Diseases of Swine, 11th Edition ...pdf`
- 页码范围：{src["pages"]}
- 批次：{BATCH_ID}
- 解析器：PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six`

## 摘要

{src["summary"]}

## 使用边界

- 本来源用于生成和评估时可直接作为 source-anchored evidence 使用。
- 中国监管、药物剂量、休药期、食品处置、召回、检疫和扑杀仍需 A0/A1 来源。
""")


def make_rules() -> None:
    for rule_id, title, category, priority, source_id, filename, body, pages in RULES:
        write_text(WIKI / "wiki" / "rules" / filename, f"""---
tags: [rule, swine, formal, v6]
rule_id: {rule_id}
updated: {NOW}
evidence_status: {STATUS}
sources: [{source_id}]
---

# {title}

## 规则

{body} 证据：{source_id}，PDF page {pages}。

## 适用边界

- 本规则用于生成、评估和审核猪病知识库中的非传染性疾病、营养、霉菌毒素和毒理问题。
- 本规则不提供具体药物剂量、固定治疗程序、休药期、食品处置执行细则或中国监管处置结论。
""")


def update_facts() -> None:
    path = WIKI / "exports" / "knowledge_facts.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {row.get("fact_id") for row in data}
    new_rows = []
    for fact_id, fact_type, subject, predicate, obj, source_id, span, jurisdiction in FACTS:
        if fact_id in existing:
            continue
        new_rows.append({
            "fact_id": fact_id,
            "fact_type": fact_type,
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "fact_confidence": "0.88",
            "evidence_source": "Diseases of Swine 11e",
            "evidence_source_id": source_id,
            "evidence_url": "",
            "evidence_quote_span": span,
            "evidence_status": STATUS,
            "applies_to_species": "swine",
            "applies_to_stage": "all_stages",
            "jurisdiction": jurisdiction,
        })
    data.extend(new_rows)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_text(ISSUES / "formal_batch_030_candidate_facts.json", json.dumps(new_rows, ensure_ascii=False, indent=2) + "\n")


def update_disease_pages() -> None:
    marker = "## Formal Batch 030 / V6 Source-Anchored Completion"
    for filename, sections in DISEASE_BLOCKS.items():
        path = WIKI / "wiki" / "diseases" / filename
        if not path.exists():
            continue
        body = [marker, "", f"> 本节由 `{BATCH_ID}` 补全；用于生成和评估时按 source-anchored evidence 直接检索，不再按 HUMAN_REVIEWED/NEEDS_REVIEW 区分。"]
        for heading, text in sections:
            body.extend(["", f"### {heading}", "", f"- {text}"])
        append_once(path, marker, "\n".join(body))


def update_indexes() -> None:
    source_index = WIKI / "exports" / "source_index.csv"
    with source_index.open("r", encoding="utf-8-sig", newline="") as fh:
        source_rows = list(csv.DictReader(fh))
        source_fields = list(source_rows[0].keys()) if source_rows else ["source_id", "title", "pages", "evidence_status", "relpath"]
    existing_sources = {row["source_id"] for row in source_rows}
    for src in SOURCES:
        if src["source_id"] not in existing_sources:
            source_rows.append({
                "source_id": src["source_id"],
                "title": src["title"],
                "pages": src["pages"],
                "evidence_status": STATUS,
                "relpath": src["relpath"],
            })
    with source_index.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=source_fields)
        writer.writeheader()
        writer.writerows(source_rows)

    rule_index = WIKI / "exports" / "rule_index.csv"
    with rule_index.open("r", encoding="utf-8-sig", newline="") as fh:
        rule_rows = list(csv.DictReader(fh))
        rule_fields = list(rule_rows[0].keys()) if rule_rows else ["rule_id", "rule_name", "category", "priority", "evidence_status", "primary_source_id", "page_relpath"]
    existing_rules = {row["rule_id"] for row in rule_rows}
    for rule_id, title, category, priority, source_id, filename, _body, _pages in RULES:
        if rule_id not in existing_rules:
            rule_rows.append({
                "rule_id": rule_id,
                "rule_name": title,
                "category": category,
                "priority": priority,
                "evidence_status": STATUS,
                "primary_source_id": source_id,
                "page_relpath": f"wiki/rules/{filename}",
            })
    with rule_index.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=rule_fields)
        writer.writeheader()
        writer.writerows(rule_rows)


def write_authority_web_registry() -> None:
    rows = [
        "# Authority Web Source Search / 2026-05-07",
        "",
        "本文件记录本轮通过 web access 检索并纳入候选来源池的官方/国际权威入口。生成和评估可直接使用已经落库且有 URL/source_id 的事实；对尚未落成事实的入口，只能作为后续补全任务，不得由标题外推具体结论。",
        "",
        "| source_id | title | url | use_boundary |",
        "| --- | --- | --- | --- |",
    ]
    for source_id, title, url, boundary in AUTHORITY_WEB_SOURCES:
        rows.append(f"| `{source_id}` | {title} | {url} | {boundary} |")
    write_text(ISSUES / "authority_web_source_search_2026-05-07.md", "\n".join(rows) + "\n")


def update_status_agnostic_policy() -> None:
    marker = "## V6 生成/评估临时取用策略"
    block = f"""{marker}

- 本轮按用户要求，生成和评估暂不区分 `HUMAN_REVIEWED` 与 `NEEDS_REVIEW`。
- 可直接使用的最低门槛调整为：事实或页面必须有明确 `evidence_source_id`、来源页、URL 或 PDF page 锚点。
- 没有来源锚点的内容仍不得作为生成或评估结论。
- 中国监管、处方、剂量、休药期、食品处理、扑杀、检疫和公共卫生执行细则仍需 A0/A1 权威来源。
"""
    for rel in [
        "wiki/synthesis/swine_answer_evaluation_rubric.md",
        "wiki/synthesis/swine_case_generation_context.md",
        "wiki/synthesis/swine_pdf_vs_authority_source_policy.md",
    ]:
        append_once(WIKI / rel, marker, block)


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_030_cross_review.md", f"""# Formal Batch 030 / V6 Cross Review

- 批次：{BATCH_ID}
- 处理范围：PDF page 1065-1111。
- 章节边界：Chapter 68 Nutrient Deficiencies and Excesses；Chapter 69 Mycotoxins in Grains and Feeds；Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases；1112 以后为 Index，未处理为 standalone facts。
- PDF 解析：已生成 `formal_batch_030_pdf_pages_1065_1111_extract.txt` 与 parser report，逐页选择字符数最高解析器。
- 新增来源：`SRC-0084` 至 `SRC-0086`。
- 新增 facts：{len(FACTS)} 条，状态统一标记 `{STATUS}`，用于生成和评估时不再按 HUMAN_REVIEWED/NEEDS_REVIEW 区分。
- 新增规则：`RULE-433` 至 `RULE-448`。
- 疾病页补全：DIS-065 至 DIS-073 的非传染性疾病、霉菌毒素、毒物和气体相关条目。
- 权威网站：已写入 `authority_web_source_search_2026-05-07.md`，只把官方域名入口作为 source registry；未落成具体 facts 的入口不得外推结论。
- 保留边界：中国监管、用药剂量、休药期、食品处理、检疫、扑杀和公共卫生执行细则仍需 A0/A1 来源。
""")


def update_progress() -> None:
    marker = "## Formal Batch 030 / V6 实施记录"
    block = f"""{marker}

- 完成时间：{NOW}
- 处理范围：PDF page 1065-1111。
- 章节边界：Section VI Noninfectious Diseases；Chapter 68 Nutrient Deficiencies and Excesses；Chapter 69 Mycotoxins in Grains and Feeds；Chapter 70 Toxic Minerals, Chemicals, Plants, and Gases。
- 新增来源：`SRC-0084` 至 `SRC-0086`。
- 新增 facts：{len(FACTS)} 条 `{STATUS}` facts。
- 新增规则：`RULE-433` 至 `RULE-448`。
- 补全疾病页：`DIS-065` 至 `DIS-073`。
- 权威网站来源登记：`issues/authority_web_source_search_2026-05-07.md`。
- 状态策略：本轮按用户要求，生成和评估暂不区分 `HUMAN_REVIEWED` 与 `NEEDS_REVIEW`；只要求事实具备来源锚点。
- 后续入口：PDF page 1112-1132 为 Index，可用于术语映射，不建议生成 standalone facts。
"""
    append_once(WIKI / "issues" / "pdf_processing_progress_v4.md", marker, block)


def main() -> None:
    extract_pdf_pages()
    make_source_pages()
    make_rules()
    update_facts()
    update_disease_pages()
    update_indexes()
    write_authority_web_registry()
    update_status_agnostic_policy()
    write_cross_review()
    update_progress()


if __name__ == "__main__":
    main()
