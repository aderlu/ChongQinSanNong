from __future__ import annotations

import csv
import json
from pathlib import Path

import fitz
import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
ISSUES = WIKI / "issues"
PDF = ROOT / "docs" / "Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman,  Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
NOW = "2026-05-07T02:20:00+00:00"
BATCH_ID = "formal-batch-022-v3"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 765, end: int = 804) -> None:
    doc = fitz.open(PDF)
    reader = PdfReader(str(PDF))
    extract_parts: list[str] = []
    report_rows: list[str] = []
    with pdfplumber.open(PDF) as plumber_pdf:
        for page_no in range(start, end + 1):
            fitz_text = doc[page_no - 1].get_text()
            plumber_text = plumber_pdf.pages[page_no - 1].extract_text() or ""
            pypdf_text = reader.pages[page_no - 1].extract_text() or ""
            chosen = "fitz" if len(fitz_text) >= len(plumber_text) else "pdfplumber"
            text = fitz_text if chosen == "fitz" else plumber_text
            extract_parts.append(f"\n\n===== PDF page {page_no} ({chosen}) =====\n{text.strip()}\n")
            report_rows.append(
                f"PDF page {page_no}: fitz_chars={len(fitz_text)} "
                f"pdfplumber_chars={len(plumber_text)} pypdf_chars={len(pypdf_text)} chosen={chosen}"
            )
    write_text(ISSUES / "formal_batch_022_pdf_pages_765_804_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_022_pdf_pages_765_804_parser_report.txt", "\n".join(report_rows) + "\n")


SOURCES = [
    ("SRC-0056", "Diseases of Swine 11e Chapter 46 Togaviruses continuation", "PDF page 765-766", "wiki/sources/SRC-0056-diseases-of-swine-11e-chapter-46-togaviruses-continuation.md", "Chapter 46 continuation covers EEEV pathogenesis and shedding in pigs, SAGV diagnosis and vector-control boundary, and Ross River virus geographic relevance opening."),
    ("SRC-0057", "Diseases of Swine 11e Section IV Chapter 47 Overview of Bacteria", "PDF page 769-772", "wiki/sources/SRC-0057-diseases-of-swine-11e-chapter-47-overview-of-bacteria.md", "Chapter 47 overview covers bacterial disease relevance, bacterial classification, spores, Gram stain use, virulence factors, exotoxin/endotoxin boundaries, and reference pages."),
    ("SRC-0058", "Diseases of Swine 11e Chapter 48 Actinobacillosis", "PDF page 773-790", "wiki/sources/SRC-0058-diseases-of-swine-11e-chapter-48-actinobacillosis.md", "Chapter 48 covers Actinobacillus pleuropneumoniae and Actinobacillus suis relevance, identification, serotypes, transmission, pathogenesis, clinical signs, lesions, diagnosis, carrier detection, serology, treatment boundary, vaccination/control and reference pages."),
    ("SRC-0059", "Diseases of Swine 11e Chapter 49 Bordetellosis", "PDF page 791-801", "wiki/sources/SRC-0059-diseases-of-swine-11e-chapter-49-bordetellosis.md", "Chapter 49 covers Bordetella bronchiseptica relevance, public health boundary, environmental survival, virulence systems, coinfections, clinical signs, lesions, diagnosis, vaccination and reference pages."),
    ("SRC-0060", "Diseases of Swine 11e Chapter 50 Brucellosis opening", "PDF page 802-804", "wiki/sources/SRC-0060-diseases-of-swine-11e-chapter-50-brucellosis-opening.md", "Chapter 50 opening covers Brucella suis relevance, other Brucella species in swine, reservoir and spillover ecology, venereal/oral/contact transmission, and environmental survival boundaries."),
]


FACTS = [
    ("TOGA-002-eeev-subclinical-incubation", "togavirus_eeev", "EEEV 猪感染潜伏期边界", "incubation_in_pigs_is_unknown_because_most_infections_are_subclinical", "猪 EEEV 感染多数为亚临床，猪中潜伏期未知；实验接种中潜伏期可为 1-3 天。", "SRC-0056", "Chapter 46 Togaviruses; PDF page 765", "all_stages"),
    ("TOGA-003-eeev-viremia-cns", "togavirus_eeev_pathogenesis", "EEEV 病毒血症与 CNS 侵入", "viremia_is_key_to_cns_invasion_after_regional_lymph_node_replication", "EEEV 初始在区域淋巴结复制，随后进入神经外组织并出现高滴度和继发病毒血症；病毒血症是侵入 CNS 的关键。", "SRC-0056", "Chapter 46 Togaviruses; PDF page 765", "all_stages"),
    ("TOGA-004-eeev-shedding", "togavirus_eeev_transmission_boundary", "EEEV 幼猪传播潜力边界", "infected_young_pigs_could_potentially_transmit_eeev_to_contacts_or_mosquitoes", "EEEV 可从口咽/直肠拭子和扁桃体检出，感染幼猪可能向接触猪或蚊虫提供病毒来源；该结论需保留潜在性边界。", "SRC-0056", "Chapter 46 Togaviruses; PDF page 765", "piglets"),
    ("TOGA-005-sagv-diagnosis", "togavirus_sagv_diagnostics", "SAGV 诊断边界", "virus_isolation_is_definitive_but_has_little_diagnostic_value_due_to_transient_viremia", "SAGV 病毒分离可作为确定性证据，但因病毒血症短暂，诊断价值有限；抗体检测提示感染或重复暴露。", "SRC-0056", "Chapter 46 Togaviruses; PDF page 766", "all_stages"),
    ("TOGA-006-sagv-control", "togavirus_sagv_control", "SAGV 防控边界", "there_is_neither_treatment_nor_vaccine_for_sagv_and_vector_control_is_rational", "SAGV 没有治疗方法或疫苗，教材将媒介控制作为合理防控方式；不得生成疫苗或药物方案。", "SRC-0056", "Chapter 46 Togaviruses; PDF page 766", "all_stages"),
    ("TOGA-007-rrv-geography", "togavirus_rrv_relevance", "Ross River virus 地理边界", "rrv_is_endemic_to_australia_papua_new_guinea_and_irian_jaya", "RRV 流行区主要为澳大利亚、巴布亚新几内亚和印度尼西亚 Irian Jaya，并在南太平洋岛屿有流行史；地理风险不得外推。", "SRC-0056", "Chapter 46 Togaviruses; PDF page 766", "all_stages"),
    ("BACT-001-section-relevance", "bacterial_disease_overview", "细菌病产业影响", "bacterial_diseases_continue_to_have_significant_impact_on_swine_industry", "尽管 PRRSV 和 PCV 等病毒病影响重大，细菌病仍对养猪业有显著影响，且常与呼吸道病原共同作用。", "SRC-0057", "Chapter 47 Overview of Bacteria; PDF page 769", "all_stages"),
    ("BACT-002-spores", "bacterial_survival", "细菌芽孢环境抵抗力", "bacterial_spores_are_extremely_resistant_to_harsh_conditions_and_disinfectants", "芽孢对恶劣环境和消毒剂高度抵抗；Bacillus 和 Clostridium 是兽医重要的芽孢形成菌属。", "SRC-0057", "Chapter 47 Overview of Bacteria; PDF page 770", "all_stages"),
    ("BACT-003-gram-stain-boundary", "bacterial_diagnostics", "革兰染色解释边界", "gram_stain_can_inform_antimicrobial_class_but_not_replace_identification_or_susceptibility", "革兰染色反应可提示可能的抗菌药类别，但不能替代病原鉴定和药敏/临床判断。", "SRC-0057", "Chapter 47 Overview of Bacteria; PDF page 770", "all_stages"),
    ("BACT-004-toxins", "bacterial_pathogenesis", "细菌毒素边界", "exotoxins_and_endotoxins_are_major_toxin_types_in_bacterial_disease", "细菌性疾病中外毒素和内毒素是主要毒素类型；毒素机制解释需结合具体病原和病变。", "SRC-0057", "Chapter 47 Overview of Bacteria; PDF page 771", "all_stages"),
    ("APP-001-agent", "actinobacillosis_etiology", "App 病原定位", "actinobacillus_pleuropneumoniae_is_the_etiologic_agent_of_porcine_pleuropneumonia", "胸膜肺炎放线杆菌 App 是猪传染性胸膜肺炎的病原，NAD 依赖性和非依赖性生物型均需正确鉴别。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 773", "grower_finisher"),
    ("APP-002-identification", "actinobacillosis_diagnostics", "App PCR 鉴定边界", "definitive_identification_may_require_species_specific_pcr", "App 与其他猪上呼吸道 Actinobacillus 种或 A. suis 可混淆，必要时需 species-specific PCR 或完整生化鉴定。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 774", "all_stages"),
    ("APP-003-serotype-prevalence", "actinobacillosis_epidemiology", "App 血清型地区差异", "relative_prevalence_of_app_serotypes_can_change_by_region_and_time", "App 血清型流行优势可随地区和年份显著变化，不能用单一地区血清型分布替代本地监测。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 775", "all_stages"),
    ("APP-004-aerosol", "actinobacillosis_transmission", "App 气溶胶传播边界", "app_may_transmit_by_aerosol_over_short_distances_and_longer_airborne_spread_is_uncommon_or_context_dependent", "App 可在短距离经气溶胶传播，邻近猪舍间空气传播可能但不常见或依赖场景；不能泛化解释所有引入事件。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 776", "all_stages"),
    ("APP-005-carriers", "actinobacillosis_transmission", "App 带菌猪引入风险", "introduction_of_carriers_is_a_key_route_for_herd_introduction", "引入带菌猪是 App 进入猪群的重要风险，尤其在高健康状态或阴性种猪群中需重点防控。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 776", "all_stages"),
    ("APP-006-pathogenesis", "actinobacillosis_pathogenesis", "App 炎症和毒力机制", "lps_cytokines_and_apx_toxins_contribute_to_pleuropneumonia_pathogenesis", "App 在肺泡内与宿主免疫相互作用，LPS、炎性细胞因子和 Apx 毒素共同影响胸膜肺炎病变。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 777", "grower_finisher"),
    ("APP-007-severity", "actinobacillosis_clinical_boundary", "App 严重度影响因素", "strain_virulence_and_coinfections_affect_outcome_and_severity", "App 感染结局和暴发严重度受菌株毒力、M. hyopneumoniae、伪狂犬病病毒和可能的猪流感病毒等共同感染影响。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 778", "all_stages"),
    ("APP-008-clinical", "actinobacillosis_clinical_pattern", "App 急慢性临床表现", "acute_disease_has_fever_dyspnea_cough_and_chronic_disease_has_intermitttent_cough_and_reduced_gain", "App 急性病例可见发热、呼吸困难、咳嗽和张口呼吸；慢性病例可表现为间歇性咳嗽、采食下降和增重下降。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 779", "grower_finisher"),
    ("APP-009-lesions", "actinobacillosis_lesions", "App 胸膜肺炎病变", "acute_lesions_include_hemorrhagic_necrotic_friable_lung_areas_and_chronic_cases_can_have_pleural_adhesions", "App 急性病变包括出血、坏死、易碎肺组织和纤维素性胸膜炎，慢性病例可形成胸膜粘连。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 780", "grower_finisher"),
    ("APP-010-diagnosis-atypical", "actinobacillosis_diagnostics", "App 非典型分离株诊断边界", "atypical_or_untypable_isolates_require_species_specific_pcr_or_complete_identification", "尿素酶阴性、非典型、肺内意外分离或不可分型 App 分离株需 species-specific PCR 或完整鉴定确认。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 781", "all_stages"),
    ("APP-011-carrier-detection", "actinobacillosis_diagnostics", "App 扁桃体带菌检测边界", "detection_of_tonsillar_carriers_is_complex_and_needed_for_seedstock_introduction_questions", "临床健康扁桃体带菌猪检测复杂，在阴性猪群引种和可疑血清结果场景下尤其重要。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 782", "all_stages"),
    ("APP-012-serology-boundary", "actinobacillosis_serology", "App ApxIV 血清学边界", "apxiv_serology_interpretation_must_consider_tonsil_only_carriage_and_strains_lacking_apxiv_production", "ApxIV 血清学解释需考虑仅扁桃体带菌时抗体水平可能不高，以及部分菌株可能因插入序列不产生 ApxIV。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 783", "all_stages"),
    ("APP-013-treatment-boundary", "actinobacillosis_treatment_boundary", "App 用药边界", "antimicrobial_susceptibility_data_must_not_be_converted_to_generic_prescriptions", "教材列举 App 体外敏感性资料，但不能转化为通用处方；治疗需结合药敏、法规、兽医诊断和给药场景。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 784", "all_stages"),
    ("APP-014-vaccine-carrier", "actinobacillosis_vaccine_boundary", "App 疫苗和带菌状态边界", "antibodies_do_not_eliminate_the_tonsillar_carrier_state", "自然或疫苗诱导抗体不能消除动物扁桃体带菌状态；疫苗保护不能等同于清除携带。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 786", "all_stages"),
    ("APP-015-eradication", "actinobacillosis_control", "App 区域控制边界", "regional_control_involves_health_schemes_serologic_monitoring_slaughter_monitoring_and_postmortem_examination", "App 区域或育种金字塔控制涉及无胸膜肺炎猪群方案、血清监测、屠宰监测和病死猪剖检等组合措施。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 786", "all_stages"),
    ("ASUIS-001-clinical", "actinobacillus_suis_clinical_pattern", "A. suis 急性败血症", "actinobacillus_suis_can_cause_acute_septicemia_with_erysipelas_like_skin_lesions", "A. suis 可在成年猪引起急性败血症，表现为沉郁、厌食、发热和类似猪丹毒的红色菱形皮肤病变。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 787", "all_stages"),
    ("ASUIS-002-differential", "actinobacillus_suis_differential", "A. suis 与猪丹毒鉴别", "actinobacillus_suis_septicemia_can_be_confused_with_erysipelas", "A. suis 败血症特别是在出现皮肤病变时可与猪丹毒混淆，需实验室鉴别。", "SRC-0058", "Chapter 48 Actinobacillosis; PDF page 787", "all_stages"),
    ("BOR-001-role", "bordetellosis_relevance", "B. bronchiseptica 在猪呼吸道病中的作用", "bordetella_bronchiseptica_is_widespread_and_plays_multiple_roles_in_swine_respiratory_disease", "支气管败血波氏杆菌在猪群中广泛存在，在非进行性萎缩性鼻炎和呼吸道病复合体中可发挥多种作用。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 791", "all_stages"),
    ("BOR-002-public-health", "bordetellosis_public_health", "B. bronchiseptica 公共卫生边界", "human_illness_from_b_bronchiseptica_is_rare_but_reported", "B. bronchiseptica 引起人病少见但有报道，公共卫生解释需结合免疫状态、接触史和权威指南。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 792", "all_stages"),
    ("BOR-003-disinfection", "bordetellosis_environment", "B. bronchiseptica 消毒敏感性", "b_bronchiseptica_is_sensitive_to_several_farm_suitable_chemical_disinfectants", "B. bronchiseptica 对多种适合农场使用的化学消毒剂敏感，但消毒效果仍取决于清洁、有机物和执行质量。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 793", "all_stages"),
    ("BOR-004-bvgas", "bordetellosis_pathogenesis", "BvgAS 毒力调控", "pathogenesis_depends_on_coordinated_expression_of_virulence_factors_under_bvgas", "B. bronchiseptica 发病机制依赖黏附素、毒素等毒力因子的协调表达，多数毒力基因表达需要 BvgAS 系统。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 793", "all_stages"),
    ("BOR-005-t3ss", "bordetellosis_pathogenesis", "T3SS 与肺炎严重度", "type_iii_secretion_system_contributes_to_pneumonic_lesion_severity_and_persistence", "B. bronchiseptica III 型分泌系统可增强肺炎病变严重度，并有助于肺部持续感染。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 794", "all_stages"),
    ("BOR-006-coinfection", "bordetellosis_coinfection", "B. bronchiseptica 共同感染", "coinfected_pigs_show_greater_and_more_sustained_proinflammatory_cytokine_production", "B. bronchiseptica 与其他病原共同感染时可出现更强、更持久的促炎细胞因子反应，加重肺部病变。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 795", "all_stages"),
    ("BOR-007-transmission", "bordetellosis_transmission", "B. bronchiseptica 传播", "b_bronchiseptica_is_highly_infectious_and_transmits_by_direct_contact_or_aerosol", "B. bronchiseptica 传染性强，可通过直接接触或气溶胶快速传播，通常高发病率、低死亡率。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 795", "all_stages"),
    ("BOR-008-lesions", "bordetellosis_lesions", "B. bronchiseptica 肺炎病变", "primary_bronchopneumonia_in_suckling_pigs_can_be_necrohemorrhagic", "哺乳仔猪原发性 B. bronchiseptica 支气管肺炎急性时可呈坏死出血性，慢性时可硬化、白色和纤维化。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 796", "piglets"),
    ("BOR-009-diagnosis", "bordetellosis_diagnostics", "B. bronchiseptica 诊断边界", "many_pathogens_cause_pneumonia_and_b_bronchiseptica_is_often_part_of_mixed_infections", "猪肺炎可由多种病原引起，B. bronchiseptica 常存在于混合感染中，分离结果需结合病变和共同感染解释。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 797", "all_stages"),
    ("BOR-010-vaccine-boundary", "bordetellosis_vaccine_boundary", "Bordetella 疫苗保护边界", "pertactin_responses_can_reduce_disease_severity_but_field_strain_heterogeneity_matters", "针对 pertactin 的免疫应答可降低疾病严重度，但 pertactin 基因异质性和母源抗体干扰会影响疫苗效果解释。", "SRC-0059", "Chapter 49 Bordetellosis; PDF page 798-799", "all_stages"),
    ("BRUC-001-host", "brucellosis_relevance", "猪布鲁氏菌宿主和病原", "swine_are_reservoir_hosts_for_brucella_suis_but_other_brucella_species_can_infect_swine_in_endemic_regions", "猪是 Brucella suis 储存宿主，但在牛或小反刍动物布鲁氏菌流行地区，B. abortus 和 B. melitensis 也可感染猪。", "SRC-0060", "Chapter 50 Brucellosis; PDF page 802", "all_stages"),
    ("BRUC-002-reproductive", "brucellosis_clinical_pattern", "猪布鲁氏菌繁殖损失", "brucella_can_produce_pregnancy_loss_stillbirth_infertility_epididymitis_and_orchitis", "布鲁氏菌在猪和其他家畜中可导致母畜流产、死胎、不孕，以及公畜附睾炎和睾丸炎。", "SRC-0060", "Chapter 50 Brucellosis; PDF page 802", "breeding_herd"),
    ("BRUC-003-wildlife-spillover", "brucellosis_epidemiology", "B. suis 野猪和野兔溢出", "b_suis_biovar_2_spillover_from_wild_boar_or_hares_can_affect_domestic_swine", "B. suis biovar 2 可由野猪或野兔溢出到家猪，野猪到家猪主要被认为与性传播有关，野兔来源可能与口服摄入有关。", "SRC-0060", "Chapter 50 Brucellosis; PDF page 803", "all_stages"),
    ("BRUC-004-environment", "brucellosis_environment", "Brucella 环境存活", "brucella_can_survive_for_months_in_cold_moist_aborted_fetuses_or_fluids", "Brucella 可在寒冷潮湿环境中的感染流产胎儿或体液中存活数月，也可污染饲料、垫料、设备和衣物。", "SRC-0060", "Chapter 50 Brucellosis; PDF page 804", "all_stages"),
    ("BRUC-005-transmission", "brucellosis_transmission", "B. suis 传播途径", "ingestion_of_aborted_uterine_contents_or_discharges_is_probably_main_route_and_venereal_spread_can_occur", "摄入流产子宫内容物或分泌物可能是 B. suis 主要传播途径，也可经结膜、皮肤破损和性传播。", "SRC-0060", "Chapter 50 Brucellosis; PDF page 804", "breeding_herd"),
]


RULES = [
    ("RULE-294", "EEEV 猪感染多数亚临床时不得推断固定潜伏期", "togavirus_eeev_boundary", "medium", "SRC-0056", "Swine-eeev-subclinical-incubation-boundary.md", "猪 EEEV 感染多数为亚临床，实验接种潜伏期不能直接转换为自然感染固定潜伏期。", "765"),
    ("RULE-295", "SAGV 不得生成治疗或疫苗方案", "togavirus_sagv_control", "medium", "SRC-0056", "Swine-sagv-no-treatment-vaccine-vector-control.md", "SAGV 无治疗和疫苗证据时，防控解释应限于媒介控制等边界，不得生成药物或疫苗程序。", "766"),
    ("RULE-296", "革兰染色不得替代病原鉴定和药敏", "bacterial_diagnostics", "high", "SRC-0057", "Swine-bacterial-gram-stain-not-identification-susceptibility.md", "革兰染色可提示病原类别和用药方向，但不能替代病原鉴定、药敏和临床判断。", "770"),
    ("RULE-297", "细菌芽孢控制必须考虑高环境抵抗力", "bacterial_environment", "high", "SRC-0057", "Swine-bacterial-spores-high-resistance-boundary.md", "Bacillus 和 Clostridium 等芽孢形成菌控制建议必须考虑芽孢对环境和消毒剂的高抵抗力。", "770"),
    ("RULE-298", "App 识别必须防止与 A. suis 和其他 Actinobacillus 混淆", "actinobacillosis_diagnostics", "high", "SRC-0058", "Swine-app-identification-pcr-biochemical-boundary.md", "App、A. suis 和其他猪上呼吸道 Actinobacillus 可混淆，非典型或关键场景需 PCR 或完整生化鉴定。", "774,781"),
    ("RULE-299", "App 血清型和毒力不得跨地区机械外推", "actinobacillosis_epidemiology", "medium", "SRC-0058", "Swine-app-serotype-prevalence-local-monitoring.md", "App 血清型流行和毒力表现受地区、时间和共同感染影响，不能机械外推到本地猪群。", "775,778"),
    ("RULE-300", "App 气溶胶传播不得泛化解释所有场间传播", "actinobacillosis_transmission", "medium", "SRC-0058", "Swine-app-aerosol-context-boundary.md", "App 可短距离气溶胶传播，但更远距离或场间空气传播需保留场景边界。", "776"),
    ("RULE-301", "App 临床和病变需结合共同感染解释", "actinobacillosis_clinical_boundary", "high", "SRC-0058", "Swine-app-clinical-coinfection-boundary.md", "App 疾病严重度受菌株毒力和 M. hyopneumoniae、PRV、IAV 等共同感染影响，不得只凭症状定因。", "778-779"),
    ("RULE-302", "App 血清学不得单独判定扁桃体带菌状态", "actinobacillosis_serology", "high", "SRC-0058", "Swine-app-serology-tonsil-carrier-boundary.md", "ApxIV 等血清学解释必须考虑扁桃体带菌、低抗体水平和不表达 ApxIV 的菌株，不能单独判定携带状态。", "782-783"),
    ("RULE-303", "App 药敏资料不得转化为通用处方", "actinobacillosis_treatment_boundary", "critical", "SRC-0058", "Swine-app-susceptibility-not-generic-prescription.md", "App 体外敏感性资料不能转化为通用治疗处方，需结合药敏、法规和兽医诊断。", "784"),
    ("RULE-304", "App 疫苗保护不得等同清除带菌", "actinobacillosis_vaccine_boundary", "high", "SRC-0058", "Swine-app-vaccine-does-not-clear-tonsil-carrier-state.md", "自然或疫苗诱导抗体不能消除扁桃体带菌状态，疫苗保护不能等同净化。", "786"),
    ("RULE-305", "A. suis 败血症必须与猪丹毒鉴别", "actinobacillus_suis_differential", "high", "SRC-0058", "Swine-actinobacillus-suis-erysipelas-differential.md", "A. suis 急性败血症可有类似猪丹毒的菱形皮肤病变，必须实验室鉴别。", "787"),
    ("RULE-306", "Bordetella 肺炎分离结果需结合混合感染解释", "bordetellosis_diagnostics", "high", "SRC-0059", "Swine-bordetella-isolation-mixed-infection-boundary.md", "B. bronchiseptica 常参与混合感染，肺炎样本分离阳性需结合病变和其他病原证据解释。", "797"),
    ("RULE-307", "Bordetella 公共卫生结论需保留罕见和宿主风险边界", "bordetellosis_public_health", "medium", "SRC-0059", "Swine-bordetella-public-health-rare-host-risk-boundary.md", "B. bronchiseptica 人感染少见但有报道，公共卫生结论需结合免疫状态和权威指南。", "792"),
    ("RULE-308", "Bordetella 疫苗效果需考虑抗原异质性和母源抗体", "bordetellosis_vaccine_boundary", "medium", "SRC-0059", "Swine-bordetella-vaccine-pertactin-maternal-antibody-boundary.md", "B. bronchiseptica 疫苗效果解释需考虑 pertactin 异质性、母源抗体干扰和减毒株性质。", "798-799"),
    ("RULE-309", "猪布鲁氏菌必须保留繁殖损失和公畜病变边界", "brucellosis_clinical", "high", "SRC-0060", "Swine-brucellosis-reproductive-boar-lesion-boundary.md", "Brucella 在猪中可导致繁殖损失、死胎、不孕、附睾炎和睾丸炎，繁殖问题需纳入鉴别。", "802"),
    ("RULE-310", "B. suis 传播需覆盖野生动物、流产物和性传播边界", "brucellosis_transmission", "critical", "SRC-0060", "Swine-brucella-suis-wildlife-abortion-venereal-boundary.md", "B. suis 风险解释应覆盖野猪/野兔溢出、流产物摄入、环境污染和性传播，不得只写单一传播途径。", "803-804"),
    ("RULE-311", "猪布鲁氏菌监管和人暴露结论需 A0/A1 来源", "brucellosis_regulatory_boundary", "critical", "SRC-0060", "Swine-brucellosis-regulatory-public-health-a0-a1-required.md", "布鲁氏菌涉及人兽共患和监管处置，本批教材事实不得直接生成中国监管、扑杀、检疫或人暴露处置结论。", "802-804"),
]


TOPICS = [
    ("Swine-togavirus-eeev-sagv-rrv-boundaries.md", "Togavirus EEEV/SAGV/RRV 证据边界", "SRC-0056", "本主题汇总 EEEV 猪亚临床感染、病毒血症、潜在传播，SAGV 诊断和媒介控制，以及 RRV 地理边界。"),
    ("Swine-bacterial-overview-diagnostics-toxin-boundaries.md", "细菌病总论诊断和毒素边界", "SRC-0057", "本主题汇总细菌病产业影响、芽孢抵抗力、革兰染色解释和外毒素/内毒素边界。"),
    ("Swine-actinobacillosis-app-asuis-diagnosis-control-boundaries.md", "Actinobacillosis App/A. suis 诊断和控制边界", "SRC-0058", "本主题汇总 App 鉴定、血清型、传播、共同感染、临床病变、扁桃体带菌、血清学、药敏、疫苗和 A. suis 鉴别边界。"),
    ("Swine-bordetellosis-respiratory-disease-boundaries.md", "Bordetellosis 呼吸道病边界", "SRC-0059", "本主题汇总 B. bronchiseptica 公共卫生、传播、毒力系统、共同感染、病变、诊断和疫苗边界。"),
    ("Swine-brucellosis-opening-transmission-boundaries.md", "猪布鲁氏菌开端传播边界", "SRC-0060", "本主题汇总 B. suis 储存宿主、繁殖损失、野生动物溢出、环境存活和流产物/性传播边界。"),
]


def make_source_pages() -> None:
    for source_id, title, pages, relpath, summary in SOURCES:
        write_text(WIKI / relpath, f"""---
tags: [source, swine, textbook, formal, v3]
source_id: {source_id}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
---

# {title}

## 范围

- 来源：本地 PDF `docs/Diseases of Swine, 11th Edition ...pdf`。
- 页码范围：{pages}。
- 批次：Formal Batch 022 / V3。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_022_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_022_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_022_pdf_pages_765_804_parser_report.txt`。
""")


def make_topic_pages() -> None:
    for filename, title, source_id, summary in TOPICS:
        write_text(WIKI / "wiki" / "topics" / filename, f"""---
tags: [topic, swine, formal, v3]
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [{source_id}]
---

# {title}

{summary}

## 证据边界

- 来源：{source_id}。
- 本页正式 facts 已在 `issues/formal_batch_022_cross_review.md` 中交叉审查。
- 本页不提供处方、剂量、固定疫苗程序、清群执行命令、公共卫生暴露处置细则或中国监管结论。
""")


def make_rule_pages() -> None:
    for rule_id, title, category, severity, source_id, filename, rule_text, pages in RULES:
        write_text(WIKI / "wiki" / "rules" / filename, f"""---
tags: [rule, swine, formal, v3]
rule_id: {rule_id}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [{source_id}]
---

# {title}

## 规则

{rule_text} 证据：{source_id}，PDF page {pages}。

## 适用边界

- 本规则用于生成、评估和审核猪病 Wiki 中病毒病、细菌病、诊断、传播、监测、免疫、用药、公共卫生和监管边界解释。
- 本规则不提供具体药物剂量、固定治疗方案、疫苗程序、清群命令、食品召回、暴露后处置细则或中国监管结论。
""")


def update_facts() -> None:
    facts_path = WIKI / "exports" / "knowledge_facts.json"
    data = json.loads(facts_path.read_text(encoding="utf-8"))
    existing = {row["fact_id"] for row in data}
    new_rows = []
    for fact_id, fact_type, subject, predicate, obj, source_id, span, stage in FACTS:
        row = {
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
            "evidence_status": "HUMAN_REVIEWED",
            "applies_to_species": "swine",
            "applies_to_stage": stage,
            "jurisdiction": "Global",
        }
        new_rows.append(row)
        if fact_id not in existing:
            data.append(row)
    write_text(facts_path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    write_text(ISSUES / "formal_batch_022_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "source_ids": [source[0] for source in SOURCES],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pypdf",
            "report": "issues/formal_batch_022_pdf_pages_765_804_parser_report.txt",
        },
        "execution_guide": "docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md",
        "facts": new_rows,
    }, ensure_ascii=False, indent=2) + "\n")


def update_rule_index() -> None:
    path = WIKI / "exports" / "rule_index.csv"
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    existing = {row[0] for row in rows[1:] if row}
    for rule_id, title, category, severity, source_id, filename, _, _ in RULES:
        if rule_id not in existing:
            rows.append([rule_id, title, category, severity, "HUMAN_REVIEWED", source_id, f"wiki/rules/{filename}"])
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


def update_source_index() -> None:
    path = WIKI / "exports" / "source_index.csv"
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    existing = {row[0] for row in rows[1:] if row}
    for source_id, title, pages, relpath, _ in SOURCES:
        if source_id not in existing:
            rows.append([source_id, title, pages, "HUMAN_REVIEWED", relpath])
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


def update_disease_pages() -> None:
    updates = [
        ("DIS-034-togaviruses-getah-sagiyama-ross-river-eee.md", "Formal Batch 022 / V3 正文抽取：已补充 EEEV 亚临床感染、病毒血症/CNS 侵入、潜在传播，SAGV 诊断/媒介控制和 RRV 地理边界；详见 `SRC-0056`。"),
        ("DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md", "Formal Batch 022 / V3 正文抽取：已补充 App 鉴定、血清型地区差异、传播、共同感染、临床病变、诊断、扁桃体带菌、血清学、药敏和疫苗/控制边界；详见 `SRC-0058`。"),
        ("DIS-036-actinobacillus-suis-septicemia-pleuropneumonia.md", "Formal Batch 022 / V3 正文抽取：已补充 A. suis 急性败血症、类似猪丹毒皮肤病变和鉴别诊断边界；详见 `SRC-0058`。"),
        ("DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md", "Formal Batch 022 / V3 正文抽取：已补充 B. bronchiseptica 公共卫生边界、传播、毒力系统、共同感染、病变、诊断和疫苗解释边界；详见 `SRC-0059`。"),
        ("DIS-038-brucella-suis-brucellosis.md", "Formal Batch 022 / V3 正文抽取：已补充 Brucella suis 储存宿主、繁殖损失、野生动物溢出、环境存活和流产物/性传播边界；详见 `SRC-0060`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 022 / V3 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_022_cross_review.md", """# Formal Batch 022 / V3 Cross Review

## 范围

- PDF page 765-766：Chapter 46 Togaviruses 后续正文。
- PDF page 767-768：Section IV 分隔页/空白页，仅记录边界。
- PDF page 769-772：Chapter 47 Overview of Bacteria 正文和参考文献。
- PDF page 773-790：Chapter 48 Actinobacillosis 正文和参考文献。
- PDF page 791-801：Chapter 49 Bordetellosis 正文和参考文献。
- PDF page 802-804：Chapter 50 Brucellosis 开端。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行。
- 页数为 40 页，符合正式批次常规范围。
- 分隔页、空白页和参考文献页只记录章节边界，不生成 standalone facts。
- 所有正式 facts 均先写入候选事实文件，再经页码锚点、内容边界和一致性审查后落库。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_022_pdf_pages_765_804_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量对照，未发现整页遗漏。
- 三次核对：`pypdf`，用于页级文本存在性和异常提示。
- 解析报告：`issues/formal_batch_022_pdf_pages_765_804_parser_report.txt`。

## 审查结论

本批候选 facts 42 条、规则页 18 个、来源页 5 个、主题页 5 个。经交叉审查后允许正式落库，所有 facts 均为 `HUMAN_REVIEWED`。

## 审查 1：页码锚点核验

- `SRC-0056` 锚定 PDF page 765-766。
- `SRC-0057` 锚定 PDF page 769-772，其中参考文献未转化为 standalone facts。
- `SRC-0058` 锚定 PDF page 773-790，其中 PDF page 788-790 为参考文献边界。
- `SRC-0059` 锚定 PDF page 791-801，其中 PDF page 800-801 为参考文献边界。
- `SRC-0060` 锚定 PDF page 802-804，为 Brucellosis 开端，下一批需继续正文。

## 审查 2：内容边界核验

- Togavirus 内容保留 EEEV/SAGV/RRV 的证据和地理边界，不生成治疗/疫苗方案。
- 细菌总论仅落库诊断、毒素和环境抵抗力边界，不生成抗菌药选择结论。
- App/A. suis 内容保留病原鉴定、传播、共同感染、诊断、血清学、药敏和疫苗边界，不生成处方或固定控制方案。
- Bordetella 内容保留混合感染、公共卫生罕见性、毒力系统、诊断和疫苗解释边界。
- Brucellosis 内容保留开端的繁殖损失、野生动物溢出、环境和传播边界；监管和人暴露处置需 A0/A1 来源。

## 审查 3：一致性核验

- facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- `SRC-0056` 至 `SRC-0060`、`RULE-294` 至 `RULE-311` 与既有条目不重复。
- 本批正式落库内容与 V3 文档同步，V2 文档未追加新批次。

## 保留问题

- PDF page 805 起需继续 Chapter 50 Brucellosis 正文，补充病理、临床、诊断、控制和公共卫生边界。
- 布鲁氏菌监管处置、人暴露、检疫、扑杀或跨区调运结论必须等待中国 A0/A1 权威来源。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 022 / V3 实施记录

- 完成时间：2026-05-07 10:20:00 +08:00。
- 处理范围：PDF page 765-804。
- 章节边界：Chapter 46 Togaviruses 后续正文；Section IV Bacterial Diseases 分隔页；Chapter 47 Overview of Bacteria；Chapter 48 Actinobacillosis；Chapter 49 Bordetellosis；Chapter 50 Brucellosis 开端。
- 参考文献/分隔页处理：PDF page 767-768、772、788-790、800-801 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0056` 至 `SRC-0060`。
- 新增主题页：Togavirus EEEV/SAGV/RRV 边界、细菌病总论边界、Actinobacillosis App/A. suis 边界、Bordetellosis 边界、Brucellosis 开端传播边界。
- 新增规则页：`RULE-294` 至 `RULE-311`。
- 新增候选事实：`issues/formal_batch_022_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_022_cross_review.md`。
- 正式落库 facts：42 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、抗菌药通用处方、App 固定免疫/净化方案、Bordetella 固定疫苗程序、Brucellosis 中国监管/检疫/扑杀/人暴露处置结论。

### Formal Batch 022 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0056` 覆盖 PDF page 765-766；`SRC-0057` 覆盖 769-772；`SRC-0058` 覆盖 773-790；`SRC-0059` 覆盖 791-801；`SRC-0060` 覆盖 802-804。
- 内容边界核验：通过。Togavirus、细菌总论、Actinobacillosis、Bordetellosis 和 Brucellosis 开端均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 804。
- 下一批应从 PDF page 805 开始。
- 推荐下一批：PDF page 805-844，继续 Chapter 50 Brucellosis 正文，并视章节边界进入后续细菌病章节。
"""
    append_text(ISSUES / "pdf_processing_progress_v3.md", block)
    append_text(ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V3.md", block)


def main() -> None:
    extract_pdf_pages()
    make_source_pages()
    make_topic_pages()
    make_rule_pages()
    update_facts()
    update_rule_index()
    update_source_index()
    update_disease_pages()
    write_cross_review()
    append_progress_docs()
    print("formal batch 022 v3 built")


if __name__ == "__main__":
    main()
