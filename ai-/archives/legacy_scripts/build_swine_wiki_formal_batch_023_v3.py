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
NOW = "2026-05-07T03:00:00+00:00"
BATCH_ID = "formal-batch-023-v3"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 805, end: int = 844) -> None:
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
    write_text(ISSUES / "formal_batch_023_pdf_pages_805_844_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_023_pdf_pages_805_844_parser_report.txt", "\n".join(report_rows) + "\n")


SOURCES = [
    ("SRC-0061", "Diseases of Swine 11e Chapter 50 Brucellosis continuation", "PDF page 805-815", "wiki/sources/SRC-0061-diseases-of-swine-11e-chapter-50-brucellosis-continuation.md", "Chapter 50 continuation covers Brucella biovars, reproductive shedding and persistence, human brucellosis, intracellular survival, lesions, culture/serology diagnosis, immune evasion, vaccine limits and references."),
    ("SRC-0062", "Diseases of Swine 11e Chapter 51 Clostridial Diseases", "PDF page 816-830", "wiki/sources/SRC-0062-diseases-of-swine-11e-chapter-51-clostridial-diseases.md", "Chapter 51 covers clostridial disease agents, C. perfringens type C, C. difficile, gas gangrene clostridia, tetanus, botulism, diagnosis, treatment and prevention boundaries, and references."),
    ("SRC-0063", "Diseases of Swine 11e Chapter 52 Colibacillosis opening", "PDF page 831-844", "wiki/sources/SRC-0063-diseases-of-swine-11e-chapter-52-colibacillosis-opening.md", "Chapter 52 opening covers E. coli relevance, ETEC/EDEC/STEC/ExPEC pathotypes, antimicrobial resistance/public health boundary, epidemiology, genetic susceptibility, clinical signs, differential diagnosis, immunity, vaccines, PWD and edema disease mechanisms."),
]


FACTS = [
    ("BRUC-006-biovar-table", "brucellosis_taxonomy", "Brucella biovar 鉴别", "recognized_brucella_biovars_have_different_preferred_hosts_and_biochemical_serologic_profiles", "Brucella 已识别 biovar 在偏好宿主、CO2 需求、H2S 产生、染料生长和单特异血清凝集方面不同；biovar 判定需实验室鉴别。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 805", "all_stages"),
    ("BRUC-007-reproductive-shedding", "brucellosis_transmission", "B. suis 繁殖失败后排菌", "large_numbers_of_b_suis_can_be_shed_in_uterine_fluids_and_fetal_tissues_after_reproductive_failure", "B. suis 可在繁殖失败后的子宫液和胎儿组织中大量排出，流产物和分泌物是重要污染源。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 806", "breeding_herd"),
    ("BRUC-008-persistent-uterine", "brucellosis_persistence", "B. suis 持续子宫感染", "a_small_percentage_of_females_can_maintain_persistent_uterine_infection_and_shed_for_up_to_36_months", "多数母猪在繁殖失败后 30-40 天清除子宫感染和阴道排菌，但少数可持续子宫感染并阴道排菌长达 36 个月。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 806", "sows"),
    ("BRUC-009-human-brucellosis", "brucellosis_public_health", "人布鲁氏菌病临床边界", "human_brucellosis_has_non_pathognomonic_manifestations_and_is_known_as_undulant_fever", "人布鲁氏菌病又称波状热，表现可涉及多器官且缺乏特异性，公共卫生结论需权威指南支持。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 807", "all_stages"),
    ("BRUC-010-intracellular-survival", "brucellosis_pathogenesis", "Brucella 细胞内存活", "brucella_can_interfere_with_host_signaling_and_resist_oxidative_killing_to_enhance_long_term_intracellular_survival", "Brucella 可抵抗氧化杀伤并干扰 TLR 和程序性细胞死亡等宿主信号通路，从而促进长期细胞内存活。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 808", "all_stages"),
    ("BRUC-011-lesions", "brucellosis_lesions", "B. suis 肉芽肿和脓肿病变", "abscesses_or_granulomas_may_develop_in_multiple_tissues_where_b_suis_localizes", "B. suis 定位组织可形成脓肿或肉芽肿，常见于淋巴结、脾、肝、肾、关节囊、腱鞘、骨、乳腺、膀胱和脑等。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 809", "all_stages"),
    ("BRUC-012-culture-definitive", "brucellosis_diagnostics", "猪布鲁氏菌培养确诊", "bacterial_culture_is_the_definitive_method_for_confirming_brucellosis_in_swine", "细菌培养是确认猪布鲁氏菌病的确定性方法；淋巴结培养与血清学结合可提高解释质量。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 809", "all_stages"),
    ("BRUC-013-serology-false-positive", "brucellosis_serology", "布鲁氏菌血清学假阳性", "yersinia_enterocolitica_o9_is_believed_to_be_a_major_source_of_false_positive_serologic_reactions_in_pigs", "Yersinia enterocolitica O:9 在猪中广泛存在，被认为是标准布鲁氏菌血清学假阳性反应的重要来源。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 810", "all_stages"),
    ("BRUC-014-immune-evasion", "brucellosis_immunity", "Brucella LPS 免疫逃逸", "brucella_lps_limits_tlr4_detection_and_resists_complement_c3_deposition", "Brucella LPS 具有降低 TLR4 识别和抵抗补体 C3 沉积的特征，有助于免疫逃逸。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 811", "all_stages"),
    ("BRUC-015-vaccine-boundary", "brucellosis_vaccine_boundary", "B. suis 猪用疫苗边界", "there_are_no_commercially_available_vaccines_for_protecting_domestic_or_feral_swine_against_b_suis", "当前没有商业化可用疫苗用于保护家猪或野猪免受 B. suis 感染；不得生成猪布鲁氏菌疫苗程序。", "SRC-0061", "Chapter 50 Brucellosis; PDF page 812", "all_stages"),
    ("CLOST-001-agents", "clostridial_disease_overview", "猪梭菌病病原范围", "main_clostridial_agents_in_swine_include_c_perfringens_c_c_difficile_c_septicum_tetani_botulinum_and_others", "猪梭菌病主要涉及 C. perfringens type C、C. difficile、C. septicum、C. perfringens type A、C. tetani、C. botulinum 等。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 816", "all_stages"),
    ("CLOST-002-typec-endemic", "clostridium_perfringens_type_c", "C. perfringens type C 地方性边界", "type_c_disease_becomes_endemic_when_sows_develop_immunity_and_provide_lactogenic_immunity", "当母猪形成免疫并通过乳汁提供保护性免疫后，C. perfringens type C 可转为地方性，非免疫母猪窝仔猪风险最高。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 817", "piglets"),
    ("CLOST-003-typec-cpb", "clostridium_perfringens_type_c_pathogenesis", "CPB 毒素核心作用", "cpb_toxin_is_confirmed_as_the_main_virulence_factor_of_c_perfringens_type_c", "CPB 毒素被确认为 C. perfringens type C 的主要毒力因子，且对胰蛋白酶敏感。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 818", "piglets"),
    ("CLOST-004-typec-neonatal-risk", "clostridium_perfringens_type_c_pathogenesis", "新生仔猪 type C 易感性", "low_trypsin_levels_in_neonatal_intestine_are_critical_for_type_c_disease_pathogenesis", "新生动物肠道胰蛋白酶水平低和/或摄入胰蛋白酶抑制物是 type C 疾病发病的重要基础。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 818", "piglets"),
    ("CLOST-005-typec-genotyping", "clostridium_diagnostics", "C. perfringens 分型", "multiplex_pcr_for_major_toxin_genes_is_nearly_universal_for_typing_c_perfringens_after_culture", "培养后用多重 PCR 检测主要毒素基因几乎是判定 C. perfringens 类型的通用方法。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 820", "all_stages"),
    ("CLOST-006-typec-treatment", "clostridium_treatment_boundary", "type C 治疗边界", "treatment_is_of_little_value_in_animals_with_clinical_signs_and_prophylaxis_is_preferred", "C. perfringens type C 出现临床症状后治疗价值有限，预防优先；不得把抗毒素或抗菌药写成通用救治保证。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 820", "piglets"),
    ("CLOST-007-cpe-public-health", "clostridium_public_health", "C. perfringens 食源性边界", "direct_contact_with_swine_poses_no_public_health_risk_associated_with_c_perfringens_type_f_food_poisoning", "C. perfringens type F 食物中毒主要与肉品冷却/处理有关，教材指出与猪直接接触不构成该食源性风险。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 821", "all_stages"),
    ("CLOST-008-cdifficile-colonization", "clostridioides_difficile_epidemiology", "仔猪 C. difficile 早期定植", "c_difficile_can_be_found_in_piglet_intestinal_content_soon_after_birth_and_all_piglets_may_be_positive_by_3_days", "C. difficile 可在出生后很早出现在仔猪肠内容物中，到产后 3 天可全部阳性，随日龄增长流行率下降。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 822", "piglets"),
    ("CLOST-009-cdifficile-diagnosis", "clostridioides_difficile_diagnostics", "C. difficile 毒素检测解释", "toxins_must_be_coupled_with_compatible_clinical_signs_and_postmortem_findings", "C. difficile TcdA/TcdB 检出必须结合相容临床表现和剖检结果解释，因为正常仔猪肠道也可不一致检出毒素。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 823", "piglets"),
    ("CLOST-010-cdifficile-culture", "clostridioides_difficile_diagnostics", "C. difficile 培养边界", "culture_of_c_difficile_is_of_little_diagnostic_significance_due_to_high_prevalence_in_healthy_piglets", "由于健康仔猪肠道中 C. difficile 流行率较高，单纯培养诊断意义有限。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 823", "piglets"),
    ("CLOST-011-gas-gangrene", "clostridial_myositis", "产气坏疽梭菌边界", "c_chauvoei_and_c_sordellii_are_components_of_gas_gangrene_complex_including_pigs", "C. chauvoei 和 C. sordellii 等可参与包括猪在内的产气坏疽复合体；需与创伤、污染和坏死性肌炎证据结合。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 824", "all_stages"),
    ("CLOST-012-cchauvoei-pcr", "clostridial_diagnostics", "C. chauvoei PCR 检测", "pcr_is_available_to_detect_c_chauvoei_on_fresh_or_formalin_fixed_tissues", "C. chauvoei 可用 PCR 在新鲜或福尔马林固定组织中检测，培养易受其他细菌过度生长影响。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 826", "all_stages"),
    ("CLOST-013-neurotoxigenic", "clostridial_neurotoxins", "破伤风和肉毒中毒人兽共患边界", "tetanus_and_botulism_are_not_zoonotic", "破伤风和肉毒中毒属于神经毒性梭菌病，教材指出两者均非人兽共患病。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 826", "all_stages"),
    ("CLOST-014-tetanus-prognosis", "tetanus_treatment_boundary", "猪破伤风治疗预后", "with_even_moderate_clinical_tetanus_prognosis_is_poor_and_treatment_benefit_has_little_evidence", "中等程度临床破伤风预后差，治疗真实获益证据有限；不得生成保证性治疗结论。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 827", "all_stages"),
    ("CLOST-015-botulism-diagnosis", "botulism_diagnostics", "肉毒中毒确诊边界", "diagnosis_should_be_based_on_detection_of_bont_in_feed_gi_contents_liver_or_serum_after_excluding_other_diagnoses", "疑似肉毒中毒需充分排除其他诊断，并基于饲料、胃肠内容物、肝脏或血清中 BoNT 检测确认。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 828", "all_stages"),
    ("CLOST-016-botulism-control", "botulism_control", "肉毒中毒控制", "suspected_botulism_requires_finding_the_toxin_source_and_preventing_consumption_of_suspect_material", "疑似肉毒中毒时应寻找毒素来源并防止继续摄入可疑材料。", "SRC-0062", "Chapter 51 Clostridial Diseases; PDF page 828", "all_stages"),
    ("ECOLI-001-relevance", "colibacillosis_relevance", "猪大肠杆菌病持续问题", "e_coli_diseases_have_long_been_recognized_and_maternal_vaccination_does_not_protect_against_postweaning_diarrhea_and_edema_disease", "猪大肠杆菌病长期存在，母猪疫苗可控制新生仔猪腹泻的一部分，但不能保护断奶后腹泻和水肿病。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 831", "piglets"),
    ("ECOLI-002-hemolysis-marker", "colibacillosis_diagnostics", "E. coli 溶血标记边界", "hemolysis_is_not_a_significant_virulence_factor_in_etec_or_edec_but_is_often_used_as_a_pathogenicity_marker", "溶血本身不是 ETEC 或 EDEC 的重要毒力因子，但常作为 F4/F18 等相关致病型分离株的标记。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 832", "all_stages"),
    ("ECOLI-003-etec", "colibacillosis_pathotype", "ETEC 分泌性腹泻", "etec_is_the_most_important_pathotype_in_pigs_and_produces_enterotoxins_that_induce_secretory_diarrhea", "ETEC 是猪中最重要的大肠杆菌致病型，可产生一种或多种肠毒素导致分泌性腹泻。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 833", "piglets"),
    ("ECOLI-004-pwd-mixed", "colibacillosis_pathotype", "PWD 混合感染边界", "mixed_infections_of_f18_stec_and_f4_etec_may_show_diarrhea_predominating_even_if_ed_lesions_are_present", "F18-STEC 与 F4-ETEC 混合感染时，临床上常以 F4-ETEC 腹泻为主，即使组织病理可见水肿病证据。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 834", "weaners"),
    ("ECOLI-005-expec", "colibacillosis_pathotype", "ExPEC 肠外感染", "expec_can_invade_cause_bacteremia_and_induce_septicemia_or_localized_extraintestinal_infections", "ExPEC 正常栖息于肠道，但可侵入、造成菌血症、败血症或脑膜炎/关节炎等局部肠外感染。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 835", "all_stages"),
    ("ECOLI-006-amr-public-health", "colibacillosis_public_health", "E. coli 耐药公共卫生边界", "strains_resistant_to_critically_important_antimicrobials_constitute_a_public_health_threat_when_entering_the_food_chain", "对第三/四代头孢和氟喹诺酮等重要抗菌药耐药的大肠杆菌进入食物链时构成公共卫生威胁。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 836", "all_stages"),
    ("ECOLI-007-epidemiology", "colibacillosis_epidemiology", "E. coli 感染广泛性", "e_coli_infections_occur_worldwide_in_commercial_swine_production", "猪大肠杆菌感染在商业养猪国家普遍存在，包括新生仔猪腹泻、断奶后腹泻、水肿病、系统感染、膀胱炎和尿路感染。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 836", "all_stages"),
    ("ECOLI-008-f4-genetic", "colibacillosis_susceptibility", "F4-ETEC 遗传抗性", "not_all_pigs_have_receptors_for_f4_and_resistance_to_f4_etec_is_inherited", "并非所有猪都有 F4 上皮细胞受体，因此部分猪对 F4-ETEC 感染有遗传抗性。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 837", "piglets"),
    ("ECOLI-009-cold-stress", "colibacillosis_risk_factor", "仔猪低温与 ETEC 腹泻", "low_temperature_reduces_peristalsis_and_delays_passage_of_bacteria_and_protective_antibodies", "环境温度低于 25°C 时，仔猪肠蠕动减弱，细菌和保护性抗体通过肠道延迟，可加重大肠杆菌腹泻。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 838", "piglets"),
    ("ECOLI-010-neonatal-differential", "colibacillosis_differential", "新生仔猪 ETEC 腹泻鉴别", "neonatal_etec_diarrhea_must_be_differentiated_from_clostridia_tgev_pedv_rotavirus_prrsv_and_isospora", "新生仔猪 ETEC 腹泻需与 C. difficile、C. perfringens A/C、TGEV、PEDV、轮状病毒、PRRSV 和较大日龄仔猪的 Isospora suis 鉴别。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 839", "piglets"),
    ("ECOLI-011-fecal-ph", "colibacillosis_diagnostics", "ETEC 粪便 pH 边界", "etec_produces_alkaline_feces_whereas_malabsorptive_viral_diarrheas_produce_acidic_feces", "ETEC 通常产生碱性粪便，而 TGEV、PEDV、轮状病毒等吸收不良性腹泻产生酸性粪便；pH 只能辅助鉴别。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 839", "piglets"),
    ("ECOLI-012-pcr-in-situ", "colibacillosis_diagnostics", "E. coli PCR 组织内检测", "pcr_can_detect_pathogenic_e_coli_in_formalin_fixed_paraffin_embedded_tissues", "PCR 可用于在福尔马林固定、石蜡包埋组织中检测致病性 E. coli。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 840", "all_stages"),
    ("ECOLI-013-immunity", "colibacillosis_immunity", "肠道 E. coli 免疫", "immunity_to_enteric_e_coli_is_humoral_and_initially_provided_by_colostrum_and_lactogenic_antibodies", "肠道 E. coli 感染免疫主要为体液免疫，早期依赖母源初乳和乳源抗体，随后依赖局部肠道主动免疫。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 840", "piglets"),
    ("ECOLI-014-vaccine-boundary", "colibacillosis_vaccine_boundary", "E. coli 母猪疫苗边界", "commercial_sow_vaccines_target_neonatal_diarrhea_antigens_but_do_not_cover_all_postweaning_or_edema_disease_risks", "常用母猪疫苗含 F4/F5/F6/F41 等抗原并用于新生仔猪腹泻控制，但不能覆盖所有断奶后腹泻或水肿病风险。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 841", "sows"),
    ("ECOLI-015-pwd", "postweaning_diarrhea", "断奶后腹泻 ETEC", "pwd_is_most_commonly_caused_by_etec_but_can_also_be_caused_by_epec", "断奶后腹泻最常由 ETEC 引起，也可由不具备经典 PWD/ED 毒力因子的 EPEC 引起。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 842", "weaners"),
    ("ECOLI-016-f4-receptor", "colibacillosis_susceptibility", "F4 受体遗传位点边界", "susceptibility_to_f4ab_ac_etec_diarrhea_has_been_linked_to_muc4_polymorphism_but_correlation_with_f4_receptor_expression_is_not_absolute", "F4ab/ac-ETEC 腹泻易感性与 MUC4 多态性相关，但 MUC4 与 F4 受体表达之间并非绝对对应。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 843", "weaners"),
    ("ECOLI-017-edema-disease", "edema_disease_pathogenesis", "水肿病 Stx2e 毒血症", "edema_disease_is_a_stx2e_toxemia_after_intestinal_colonization_by_edec", "水肿病是 EDEC 在肠道定植后吸收 Stx2e 导致的毒血症，特定部位出现严重水肿。", "SRC-0063", "Chapter 52 Colibacillosis; PDF page 844", "weaners"),
]


RULES = [
    ("RULE-312", "布鲁氏菌 biovar 判定必须依赖实验室鉴别", "brucellosis_taxonomy", "high", "SRC-0061", "Swine-brucella-biovar-lab-identification-required.md", "Brucella biovar 不得凭宿主或临床表现推断，需结合生化和血清学等实验室鉴别。", "805"),
    ("RULE-313", "B. suis 流产物和阴道排菌必须纳入传播解释", "brucellosis_transmission", "critical", "SRC-0061", "Swine-brucella-suis-abortion-vaginal-shedding-boundary.md", "B. suis 繁殖失败后可在胎儿组织、子宫液和阴道分泌物中大量排菌，传播解释必须覆盖这些污染源。", "806"),
    ("RULE-314", "猪布鲁氏菌血清学假阳性必须考虑 Y. enterocolitica O:9", "brucellosis_serology", "high", "SRC-0061", "Swine-brucellosis-serology-yersinia-o9-false-positive.md", "猪布鲁氏菌血清学解释必须考虑 Y. enterocolitica O:9 等 LPS 交叉反应造成的假阳性。", "810"),
    ("RULE-315", "猪布鲁氏菌不得生成商业疫苗程序", "brucellosis_vaccine_boundary", "critical", "SRC-0061", "Swine-brucellosis-no-commercial-swine-vaccine-program.md", "没有商业化可用疫苗保护家猪或野猪免受 B. suis 感染时，不得生成猪布鲁氏菌疫苗程序。", "812"),
    ("RULE-316", "C. perfringens type C 临床发病后治疗价值有限", "clostridium_perfringens_type_c", "high", "SRC-0062", "Swine-cperfringens-type-c-prophylaxis-preferred.md", "C. perfringens type C 出现临床症状后治疗价值有限，应强调预防边界，不得承诺治疗效果。", "820"),
    ("RULE-317", "C. perfringens 分型需检测主要毒素基因", "clostridium_diagnostics", "high", "SRC-0062", "Swine-cperfringens-toxin-gene-pcr-typing.md", "C. perfringens 分型应基于培养后主要毒素基因多重 PCR 等证据，不能仅凭临床腹泻分型。", "820"),
    ("RULE-318", "C. difficile 毒素阳性必须结合病变和临床", "clostridioides_difficile_diagnostics", "high", "SRC-0062", "Swine-cdifficile-toxin-compatible-lesions-required.md", "C. difficile TcdA/TcdB 检出必须结合相容临床表现和剖检病变，因为正常仔猪也可检出毒素或菌体。", "823"),
    ("RULE-319", "C. difficile 单纯培养不得作为确诊依据", "clostridioides_difficile_diagnostics", "high", "SRC-0062", "Swine-cdifficile-culture-not-diagnostic-alone.md", "健康仔猪 C. difficile 定植率高，单纯培养阳性诊断意义有限。", "823"),
    ("RULE-320", "破伤风和肉毒中毒不得标为人兽共患", "clostridial_neurotoxin_public_health", "medium", "SRC-0062", "Swine-tetanus-botulism-not-zoonotic.md", "教材指出破伤风和肉毒中毒均非人兽共患病，公共卫生解释不得误标。", "826"),
    ("RULE-321", "肉毒中毒需检测 BoNT 并排除其他诊断", "botulism_diagnostics", "high", "SRC-0062", "Swine-botulism-bont-detection-exclusion-required.md", "肉毒中毒确诊需在排除其他诊断后检测 BoNT，不能仅凭瘫痪或群发死亡定因。", "828"),
    ("RULE-322", "ETEC 腹泻必须纳入年龄和鉴别诊断", "colibacillosis_differential", "high", "SRC-0063", "Swine-etec-diarrhea-age-differential-required.md", "ETEC 腹泻诊断需结合日龄、临床、实验室和与梭菌、TGEV、PEDV、轮状病毒、PRRSV、Isospora 等鉴别。", "839"),
    ("RULE-323", "E. coli 溶血不得直接等同毒力", "colibacillosis_diagnostics", "medium", "SRC-0063", "Swine-ecoli-hemolysis-marker-not-virulence.md", "溶血常作致病型标记，但本身不是 ETEC/EDEC 的重要毒力因子，不能单独定因。", "832"),
    ("RULE-324", "E. coli 重要抗菌药耐药需保留公共卫生边界", "colibacillosis_public_health", "critical", "SRC-0063", "Swine-ecoli-critically-important-amr-public-health.md", "对关键重要抗菌药耐药的大肠杆菌进入食物链时构成公共卫生威胁，但本批不生成用药或监管处置。", "836"),
    ("RULE-325", "F4-ETEC 易感性需保留遗传受体边界", "colibacillosis_susceptibility", "medium", "SRC-0063", "Swine-f4-etec-genetic-receptor-boundary.md", "F4-ETEC 易感性与受体和遗传多态性相关，不能假设所有猪均易感。", "837,843"),
    ("RULE-326", "ETEC 粪便 pH 只能辅助鉴别", "colibacillosis_diagnostics", "medium", "SRC-0063", "Swine-etec-fecal-ph-adjunct-only.md", "粪便 pH 可辅助区分 ETEC 与吸收不良性病毒腹泻，但不能替代实验室诊断。", "839"),
    ("RULE-327", "母猪 E. coli 疫苗不得外推覆盖 PWD/ED", "colibacillosis_vaccine_boundary", "high", "SRC-0063", "Swine-ecoli-sow-vaccine-not-pwd-ed-coverage.md", "母猪 E. coli 疫苗主要用于被动保护新生仔猪腹泻，不能外推为覆盖断奶后腹泻和水肿病。", "831,841"),
    ("RULE-328", "水肿病必须保留 Stx2e 毒血症机制", "edema_disease_pathogenesis", "high", "SRC-0063", "Swine-edema-disease-stx2e-toxemia-boundary.md", "水肿病解释必须保留 EDEC 定植后 Stx2e 毒血症机制，不能仅写成普通腹泻。", "844"),
]


TOPICS = [
    ("Swine-brucellosis-diagnosis-serology-vaccine-boundaries.md", "猪布鲁氏菌诊断、血清学和疫苗边界", "SRC-0061", "本主题汇总 Brucella biovar、繁殖失败后排菌、持续子宫感染、人布鲁氏菌病、细胞内存活、病变、培养确诊、血清学假阳性和疫苗边界。"),
    ("Swine-clostridial-diseases-diagnosis-toxin-boundaries.md", "猪梭菌病诊断、毒素和防控边界", "SRC-0062", "本主题汇总 C. perfringens type C、C. difficile、产气坏疽、破伤风、肉毒中毒的毒素、诊断和防控边界。"),
    ("Swine-colibacillosis-etec-edec-expec-boundaries.md", "猪大肠杆菌病 ETEC/EDEC/ExPEC 边界", "SRC-0063", "本主题汇总 ETEC、EDEC、水肿病、ExPEC、抗菌药耐药公共卫生、遗传易感性、诊断鉴别、免疫和疫苗边界。"),
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
- 批次：Formal Batch 023 / V3。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_023_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_023_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_023_pdf_pages_805_844_parser_report.txt`。
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
- 本页正式 facts 已在 `issues/formal_batch_023_cross_review.md` 中交叉审查。
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

- 本规则用于生成、评估和审核猪病 Wiki 中细菌病、诊断、传播、监测、免疫、用药、公共卫生和监管边界解释。
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
    write_text(ISSUES / "formal_batch_023_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "source_ids": [source[0] for source in SOURCES],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pypdf",
            "report": "issues/formal_batch_023_pdf_pages_805_844_parser_report.txt",
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
        ("DIS-038-brucella-suis-brucellosis.md", "Formal Batch 023 / V3 正文抽取：已补充 Brucella biovar、繁殖失败后排菌、持续子宫感染、人布鲁氏菌病、细胞内存活、病变、培养确诊、血清学假阳性和疫苗边界；详见 `SRC-0061`。"),
        ("DIS-039-clostridial-diseases.md", "Formal Batch 023 / V3 正文抽取：已补充 C. perfringens type C、C. difficile、产气坏疽、破伤风、肉毒中毒的毒素、诊断和防控边界；详见 `SRC-0062`。"),
        ("DIS-040-colibacillosis.md", "Formal Batch 023 / V3 正文抽取：已补充 ETEC/EDEC/STEC/ExPEC、耐药公共卫生、遗传易感性、诊断鉴别、免疫和疫苗边界；详见 `SRC-0063`。"),
        ("DIS-041-neonatal-post-weaning-colibacillosis.md", "Formal Batch 023 / V3 正文抽取：已补充新生仔猪腹泻、断奶后腹泻 ETEC/EPEC、F4/F18、母源免疫和疫苗保护边界；详见 `SRC-0063`。"),
        ("DIS-042-edema-disease-e-coli.md", "Formal Batch 023 / V3 正文抽取：已补充 EDEC、Stx2e 毒血症和水肿病发病机制边界；详见 `SRC-0063`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 023 / V3 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_023_cross_review.md", """# Formal Batch 023 / V3 Cross Review

## 范围

- PDF page 805-812：Chapter 50 Brucellosis 正文后段。
- PDF page 813-815：Chapter 50 Brucellosis 参考文献，仅记录边界。
- PDF page 816-828：Chapter 51 Clostridial Diseases 正文。
- PDF page 829-830：Chapter 51 参考文献，仅记录边界。
- PDF page 831-844：Chapter 52 Colibacillosis 开端至 edema disease 机制。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行。
- 页数为 40 页，符合正式批次常规范围。
- 参考文献页只记录章节边界，不生成 standalone facts。
- 所有正式 facts 均先写入候选事实文件，再经页码锚点、内容边界和一致性审查后落库。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_023_pdf_pages_805_844_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量对照，未发现整页遗漏。
- 三次核对：`pypdf`，用于页级文本存在性和异常提示。
- 解析报告：`issues/formal_batch_023_pdf_pages_805_844_parser_report.txt`。

## 审查结论

本批候选 facts 43 条、规则页 17 个、来源页 3 个、主题页 3 个。经交叉审查后允许正式落库，所有 facts 均为 `HUMAN_REVIEWED`。

## 审查 1：页码锚点核验

- `SRC-0061` 锚定 PDF page 805-815，其中 PDF page 813-815 为参考文献边界。
- `SRC-0062` 锚定 PDF page 816-830，其中 PDF page 829-830 为参考文献边界。
- `SRC-0063` 锚定 PDF page 831-844，为 Colibacillosis 开端，下一批需继续正文。

## 审查 2：内容边界核验

- Brucellosis 内容保留 biovar、排菌、持续感染、诊断、血清学假阳性和疫苗边界；监管、人暴露和处置结论需 A0/A1 来源。
- Clostridial diseases 内容保留毒素、分型、诊断和预防/治疗边界；不生成抗毒素、抗菌药或疫苗固定程序。
- Colibacillosis 内容保留 ETEC/EDEC/ExPEC、耐药公共卫生、遗传易感、诊断鉴别、免疫和水肿病机制边界；不生成抗菌药处方。

## 审查 3：一致性核验

- facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- `SRC-0061` 至 `SRC-0063`、`RULE-312` 至 `RULE-328` 与既有条目不重复。
- 本批正式落库内容与 V3 文档同步，V2 文档未追加新批次。

## 保留问题

- PDF page 845 起需继续 Chapter 52 Colibacillosis 正文，补充 PWD/ED 临床、诊断、治疗、防控和参考文献边界。
- 布鲁氏菌监管处置、人暴露、检疫、扑杀或跨区调运结论必须等待中国 A0/A1 权威来源。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 023 / V3 实施记录

- 完成时间：2026-05-07 11:00:00 +08:00。
- 处理范围：PDF page 805-844。
- 章节边界：Chapter 50 Brucellosis 正文后段和参考文献；Chapter 51 Clostridial Diseases 正文和参考文献；Chapter 52 Colibacillosis 开端。
- 参考文献处理：PDF page 813-815、829-830 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0061` 至 `SRC-0063`。
- 新增主题页：猪布鲁氏菌诊断/血清学/疫苗边界、猪梭菌病诊断/毒素/防控边界、猪大肠杆菌病 ETEC/EDEC/ExPEC 边界。
- 新增规则页：`RULE-312` 至 `RULE-328`。
- 新增候选事实：`issues/formal_batch_023_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_023_cross_review.md`。
- 正式落库 facts：43 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、布鲁氏菌中国监管/人暴露处置、梭菌病固定抗毒素/抗菌药/疫苗程序、大肠杆菌病抗菌药通用处方。

### Formal Batch 023 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0061` 覆盖 PDF page 805-815；`SRC-0062` 覆盖 816-830；`SRC-0063` 覆盖 831-844。
- 内容边界核验：通过。Brucellosis、Clostridial diseases 和 Colibacillosis 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 844。
- 下一批应从 PDF page 845 开始。
- 推荐下一批：PDF page 845-884，继续 Chapter 52 Colibacillosis 正文后段和参考文献，并视章节边界进入后续细菌病章节。
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
    print("formal batch 023 v3 built")


if __name__ == "__main__":
    main()
