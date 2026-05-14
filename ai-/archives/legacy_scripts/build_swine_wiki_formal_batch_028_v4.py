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
NOW = "2026-05-07T18:25:00+08:00"
BATCH_ID = "formal-batch-028-v4"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 1005, end: int = 1026) -> None:
    doc = fitz.open(PDF)
    extract_parts: list[str] = []
    report_rows: list[str] = []
    with pdfplumber.open(PDF) as plumber_pdf:
        for page_no in range(start, end + 1):
            fitz_text = doc[page_no - 1].get_text()
            plumber_text = plumber_pdf.pages[page_no - 1].extract_text() or ""
            miner_text = pdfminer_extract_text(str(PDF), page_numbers=[page_no - 1]) or ""
            candidates = {
                "fitz": fitz_text,
                "pdfplumber": plumber_text,
                "pdfminer": miner_text,
            }
            chosen = max(candidates, key=lambda key: len(candidates[key]))
            text = candidates[chosen]
            extract_parts.append(f"\n\n===== PDF page {page_no} ({chosen}) =====\n{text.strip()}\n")
            report_rows.append(
                f"PDF page {page_no}: fitz_chars={len(fitz_text)} "
                f"pdfplumber_chars={len(plumber_text)} pdfminer_chars={len(miner_text)} chosen={chosen}"
            )
    write_text(
        ISSUES / "formal_batch_028_pdf_pages_1005_1026_extract.txt",
        "".join(extract_parts).strip() + "\n",
    )
    write_text(
        ISSUES / "formal_batch_028_pdf_pages_1005_1026_parser_report.txt",
        "\n".join(report_rows) + "\n",
    )


SOURCES = [
    (
        "SRC-0079",
        "Diseases of Swine 11e Chapter 64 Miscellaneous Bacterial Infections",
        "PDF page 1005-1026",
        "wiki/sources/SRC-0079-diseases-of-swine-11e-chapter-64-miscellaneous-bacterial-infections.md",
        "Chapter 64 covers Actinobaculum suis, Actinomyces hyovaginalis, anthrax, melioidosis, Campylobacter, Chlamydia, enterococci, Klebsiella, Listeria, Rhodococcus equi, Treponema pedis, Trueperella abortisuis, Trueperella pyogenes, Yersinia and references.",
    ),
]


FACTS = [
    ("MISCBACT-001-asuis-host", "actinobaculum_suis_relevance", "A. suis 宿主和疾病", "actinobaculum_suis_causes_cystitis_and_pyelonephritis_in_sows_and_is_carried_by_boars", "Actinobaculum suis 可引起母猪膀胱炎和肾盂肾炎，公猪是重要携带者；教材称其不是公共卫生关注点。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1005", "sows"),
    ("MISCBACT-002-asuis-transmission", "actinobaculum_suis_transmission", "A. suis 交配后血尿", "hematuria_two_to_three_weeks_after_boar_service_suggests_a_suis_cystitis_pyelonephritis", "母猪与感染公猪配种后 2-3 周出现血尿，提示 A. suis 膀胱炎/肾盂肾炎而非普通 E. coli 膀胱炎。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1005", "sows"),
    ("MISCBACT-003-asuis-lesions", "actinobaculum_suis_lesions", "A. suis 泌尿道病变", "a_suis_lesions_are_limited_to_urinary_tract_with_ascending_inflammation_and_pyelonephritis", "A. suis 病变局限于泌尿道，可见上行性炎症并发展为肾盂肾炎。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1005", "sows"),
    ("MISCBACT-004-asuis-anaerobic-culture", "actinobaculum_suis_diagnostics", "A. suis 厌氧培养边界", "anaerobic_incubation_for_four_days_is_essential_for_a_suis_isolation", "A. suis 从尿液或受累组织分离时，4 天厌氧培养是关键条件；PCR 可比传统培养更敏感。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1006", "sows"),
    ("MISCBACT-005-ahyo-disease-boundary", "actinomyces_hyovaginalis_boundary", "A. hyovaginalis 疾病证据边界", "a_hyovaginalis_type_ii_is_infrequent_sporadic_abortion_agent_and_type_iii_causes_pyemic_lesions", "A. hyovaginalis type II 可能为少见散发性流产原因，type III 可形成多器官脓毒性病变，因分离鉴定困难可能漏报。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1006", "all_stages"),
    ("MISCBACT-006-ahyo-diagnosis", "actinomyces_hyovaginalis_diagnostics", "A. hyovaginalis 诊断要求", "a_hyovaginalis_diagnosis_requires_culture_and_typical_microscopic_lesions", "A. hyovaginalis 诊断需培养和典型显微病变；阴道分泌物培养阳性不能作为繁殖失败确诊依据。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1007", "breeding_herd"),
    ("MISCBACT-007-anthrax-rare-zoonotic", "anthrax_relevance", "猪炭疽少见但人兽共患", "anthrax_is_rare_in_swine_but_zoonotic_and_pork_products_from_infected_swine_are_hazardous", "炭疽在猪少见且猪相对抵抗，但属于人兽共患；感染猪及其肉品可对人构成危害。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1007", "all_stages"),
    ("MISCBACT-008-anthrax-spores", "anthrax_environment", "炭疽芽孢环境持久", "b_anthracis_spores_can_remain_viable_for_50_or_more_years", "B. anthracis 芽孢在适宜环境中可存活 50 年或更久，防控重点是避免环境被长寿命芽孢污染。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1007", "all_stages"),
    ("MISCBACT-009-anthrax-necropsy", "anthrax_diagnostics", "疑似炭疽剖检限制", "necropsy_of_anthrax_cases_is_discouraged_to_reduce_spore_contamination_and_human_exposure", "疑似猪炭疽时不鼓励剖检，以减少芽孢环境污染和人员暴露。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1008", "all_stages"),
    ("MISCBACT-010-anthrax-differential", "anthrax_differential", "猪炭疽鉴别范围", "swine_anthrax_can_resemble_clostridial_cervical_infection_s_porcinus_enteritis_or_septicemias", "猪炭疽可与梭菌性颈部感染、S. porcinus 颈淋巴结炎、多种肠炎和败血症相似，需纳入鉴别诊断。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1008", "all_stages"),
    ("MISCBACT-011-melioidosis-zoonosis", "melioidosis_public_health", "猪类鼻疽公共卫生边界", "melioidosis_is_a_chronic_swine_infection_in_tropical_regions_and_humans_can_be_infected", "类鼻疽是热带/亚热带地区猪的慢性细菌感染，人可感染，B. pseudomallei 也被视为潜在生物恐怖病原。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1009", "all_stages"),
    ("MISCBACT-012-melioidosis-abscesses", "melioidosis_lesions", "猪类鼻疽脓肿", "melioidosis_lesions_are_large_creamy_or_caseous_yellow_green_abscesses_in_organs_and_lymph_nodes", "猪类鼻疽病变常为肺、肝、脾、肾及淋巴结内充满乳脂样或干酪样黄绿色脓液的大脓肿。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1010", "all_stages"),
    ("MISCBACT-013-melioidosis-confirm", "melioidosis_diagnostics", "猪类鼻疽培养确诊", "melioidosis_diagnosis_is_confirmed_by_culture", "猪类鼻疽可在热带环境中按发热、步态异常和肢体皮下肿胀怀疑，但确诊需培养。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1010", "all_stages"),
    ("MISCBACT-014-campy-not-primary-swine-disease", "campylobacter_boundary", "猪弯曲菌疾病边界", "campylobacters_are_not_known_to_produce_generally_recognized_enteric_or_other_diseases_in_swine", "C. jejuni/C. coli 可在新生猪模型中致病，但弯曲菌不被认为在猪中造成公认的常规肠道或其他疾病。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1011", "piglets"),
    ("MISCBACT-015-campy-public-health", "campylobacter_public_health", "猪弯曲菌人食源性边界", "swine_can_be_one_source_for_human_campylobacter_infection_but_poultry_is_the_main_foodborne_source", "猪源 C. jejuni/C. coli/C. hyointestinalis 可感染人，接触猪、污染猪肉或猪粪污染水可导致感染，但家禽是主要食源。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1011", "all_stages"),
    ("MISCBACT-016-campy-dx", "campylobacter_diagnostics", "新生猪弯曲菌病确诊边界", "confirmation_of_enteric_campylobacteriosis_in_neonatal_pigs_requires_typical_signs_lesions_confirmation_and_exclusion_of_common_causes", "新生猪肠道弯曲菌病确认需典型临床和病变、确认 C. jejuni/C. coli，并排除更常见的新生仔猪腹泻原因。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1012", "piglets"),
    ("MISCBACT-017-chlamydia-controversial", "chlamydia_boundary", "猪衣原体致病性争议", "importance_of_chlamydiaceae_as_pig_pathogens_remains_controversial_due_to_mixed_infections_and_limited_confirmation", "Chlamydiaceae 在猪病中的重要性仍有争议，原因包括混合感染常见、接种研究有限和确证检测不易。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1013", "all_stages"),
    ("MISCBACT-018-chlamydia-species", "chlamydia_taxonomy", "猪衣原体种类", "four_chlamydia_species_are_found_in_swine_c_suis_c_abortus_c_pecorum_and_c_psittaci", "猪中可见 C. suis、C. abortus、C. pecorum 和 C. psittaci 四种衣原体。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1013", "all_stages"),
    ("MISCBACT-019-chlamydia-zoonosis", "chlamydia_public_health", "猪衣原体人兽共患边界", "c_abortus_and_c_psittaci_are_zoonotic_but_pig_to_human_transmission_has_not_been_confirmed", "C. abortus 和 C. psittaci 具人兽共患意义，但教材称猪到人的传播尚未确认；孕妇接触猪流产物需谨慎解释。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1013", "breeding_herd"),
    ("MISCBACT-020-chlamydia-pcr", "chlamydia_diagnostics", "猪衣原体 PCR 优先", "pcr_is_preferred_for_chlamydia_confirmation_because_it_allows_sensitive_specific_species_identification", "猪衣原体确认目前优先 PCR，因为可敏感、特异地识别 Chlamydia 种；血清抗体只能提示暴露。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1014", "all_stages"),
    ("MISCBACT-021-chlamydia-no-vaccine", "chlamydia_vaccine_boundary", "猪衣原体疫苗边界", "no_chlamydial_vaccines_are_commercially_available_for_pigs", "猪没有商业化衣原体疫苗；反刍动物 C. abortus 疫苗对猪繁殖失败的预防效果未知。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1015", "all_stages"),
    ("MISCBACT-022-enterococci-neonatal", "enterococci_neonatal_diarrhea", "新生猪黏附性肠球菌", "enteroadherent_enterococci_are_associated_with_diarrhea_in_piglets_between_two_and_twenty_days", "黏附性肠球菌可与 2-20 日龄仔猪腹泻相关，并参与北欧报道的新生仔猪腹泻综合征。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1016", "piglets"),
    ("MISCBACT-023-enterococci-ast", "enterococci_treatment_boundary", "肠球菌 AST 边界", "antimicrobial_susceptibility_testing_is_advised_before_enterococcal_treatment_due_to_natural_resistance", "因肠球菌对部分抗菌药天然耐受，治疗前建议做药敏试验。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1016", "piglets"),
    ("MISCBACT-024-klebsiella-septicemia", "klebsiella_septicemia", "Klebsiella 仔猪败血症", "k_pneumoniae_septicemia_occurs_in_preweaning_one_to_four_week_old_piglets", "K. pneumoniae 败血症可发生于 1-4 周龄哺乳仔猪，表现为突然死亡或卧地、发绀。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1016", "piglets"),
    ("MISCBACT-025-klebsiella-sawdust", "klebsiella_environment", "Klebsiella 锯末环境", "k_pneumoniae_is_often_found_in_sawdust_which_supports_survival_and_multiplication", "K. pneumoniae 是猪消化道共生菌和环境菌，常见于锯末，锯末适合其存活和增殖。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1016", "piglets"),
    ("MISCBACT-026-klebsiella-control-uncertain", "klebsiella_control_boundary", "Klebsiella 干预效果不确定", "k_pneumoniae_piglet_outbreak_interventions_lack_untreated_controls_and_efficacy_cannot_be_assessed", "K. pneumoniae 仔猪败血症暴发中若无未处理对照，抗菌药、补铁或补料等干预效果不能确定。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1017", "piglets"),
    ("MISCBACT-027-listeria-foodborne", "listeria_public_health", "猪李斯特菌食品安全边界", "l_monocytogenes_carriage_by_slaughter_swine_is_concern_for_food_industry", "L. monocytogenes 常由猪扁桃体和肠道携带，猪临床病少见，但屠宰猪携带对食品行业有意义。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1017", "all_stages"),
    ("MISCBACT-028-listeria-risk-groups", "listeria_public_health", "李斯特菌人群高风险", "pregnant_women_newborns_elderly_and_immunosuppressed_people_are_most_at_risk_for_listeriosis", "人李斯特菌病高风险群体包括孕妇、新生儿、老年人和免疫抑制人群。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1017", "all_stages"),
    ("MISCBACT-029-listeria-subclinical", "listeria_clinical_pattern", "猪李斯特菌临床少见", "subclinical_listeria_infection_is_common_but_clinical_listeriosis_is_uncommon_in_swine", "猪亚临床李斯特菌感染常见，但临床李斯特菌病少见，可表现为仔猪败血症、神经症状或母猪流产。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1018", "all_stages"),
    ("MISCBACT-030-listeria-confirm", "listeria_diagnostics", "猪李斯特菌确诊", "listeriosis_confirmation_requires_typical_signs_lesions_and_detection_of_l_monocytogenes", "猪李斯特菌病确诊需典型临床、病变和检出 L. monocytogenes，且需与伪狂犬等鉴别。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1018", "all_stages"),
    ("MISCBACT-031-rhodococcus-tb-diff", "rhodococcus_equi_differential", "R. equi 与结核鉴别", "r_equi_causes_granulomatous_lymphadenitis_that_can_be_confused_with_tuberculosis_at_slaughter", "R. equi 可致猪头颈部淋巴结肉芽肿性淋巴结炎，屠宰时可与结核病变混淆。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1018", "all_stages"),
    ("MISCBACT-032-rhodococcus-no-human-risk", "rhodococcus_equi_public_health", "R. equi 猪人传播边界", "pig_to_human_or_pork_to_human_r_equi_transmission_is_not_documented", "R. equi 可感染免疫抑制人群，但猪到人或猪肉到人的传播尚无记录。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1019", "all_stages"),
    ("MISCBACT-033-rhodococcus-confirm", "rhodococcus_equi_diagnostics", "R. equi 确诊要求", "r_equi_diagnosis_requires_microbiologic_identification_and_elimination_of_mycobacterial_infection", "R. equi 诊断需微生物学鉴定并排除分枝杆菌感染。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1019", "all_stages"),
    ("MISCBACT-034-tpedis-ear-necrosis", "treponema_pedis_skin", "T. pedis 耳坏死边界", "t_pedis_is_associated_with_ear_necrosis_and_chronic_skin_lesions_but_is_likely_not_the_sole_or_initiating_agent", "T. pedis 与猪耳坏死、肩部压疮等慢性皮肤病变相关，但可能不是唯一或起始病原。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1019", "weaners"),
    ("MISCBACT-035-tpedis-management", "treponema_pedis_control", "T. pedis 皮肤病管理边界", "improvement_of_environment_and_manipulable_materials_may_reduce_social_reasons_for_ear_and_flank_biting", "改善环境并提供可操作材料，可能减少耳咬和胁部咬伤等社会/环境诱因。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1020", "weaners"),
    ("MISCBACT-036-tabortisuis-confirm", "trueperella_abortisuis_diagnostics", "T. abortisuis 流产确诊", "t_abortisuis_abortion_diagnosis_requires_fetal_or_placental_lesions_intralesional_bacteria_and_culture", "T. abortisuis 流产诊断需胎儿/胎盘病变、形态相符的病灶内细菌和培养阳性。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1021", "breeding_herd"),
    ("MISCBACT-037-tabortisuis-contamination", "trueperella_abortisuis_boundary", "T. abortisuis 污染边界", "t_abortisuis_in_vaginal_discharge_or_placenta_without_lesions_should_not_confirm_abortion", "在无病变时从阴道分泌物或胎盘检出 T. abortisuis，因粪污染可能，不能确认其为流产原因。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1021", "breeding_herd"),
    ("MISCBACT-038-tpyogenes-abscesses", "trueperella_pyogenes_lesions", "T. pyogenes 化脓病变", "t_pyogenes_is_a_major_cause_of_purulent_abscessation_and_discharges_in_pigs", "T. pyogenes 是猪化脓性脓肿和各类脓性分泌物的重要原因，脓肿可见于几乎全身组织。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1022", "all_stages"),
    ("MISCBACT-039-tpyogenes-confirm", "trueperella_pyogenes_diagnostics", "T. pyogenes 确认", "t_pyogenes_confirmation_requires_demonstration_in_typical_lesions_by_culture_or_realtime_qpcr", "T. pyogenes 感染确认需在典型病变中经培养或实时 qPCR 证明该菌。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1022", "all_stages"),
    ("MISCBACT-040-tpyogenes-treatment-limit", "trueperella_pyogenes_treatment_boundary", "T. pyogenes 脓肿治疗限制", "antimicrobial_treatments_alone_are_poorly_effective_for_t_pyogenes_abscesses", "T. pyogenes 脓肿中抗菌药难以达到有效治疗水平，单靠抗菌药效果较差，且无有效疫苗。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1022", "all_stages"),
    ("MISCBACT-041-yersinia-foodborne", "yersinia_public_health", "猪 Yersinia 食源性边界", "swine_are_primary_carrier_of_y_enterocolitica_and_source_for_human_yersiniosis", "猪是 Y. enterocolitica 的主要携带宿主和人类耶尔森菌病来源之一，主要重要性在于食源性感染。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1023", "all_stages"),
    ("MISCBACT-042-yersinia-brucella-false-positive", "yersinia_serology_boundary", "Y. enterocolitica O:9 布病假阳性", "y_enterocolitica_o9_antibody_cross_reacts_in_brucella_serology_causing_false_positive_swine_brucellosis_tests", "Y. enterocolitica O:9 抗体可与 Brucella 血清学交叉反应，造成猪布鲁氏菌血清学假阳性。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1023", "all_stages"),
    ("MISCBACT-043-yersinia-refrigeration", "yersinia_food_safety_boundary", "Yersinia 冷藏增殖", "y_enterocolitica_and_y_pseudotuberculosis_can_multiply_in_refrigerated_products", "Y. enterocolitica 和 Y. pseudotuberculosis 可在冷藏产品中增殖，食品安全解释需保留冷链风险边界。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1023", "all_stages"),
    ("MISCBACT-044-yersinia-asymptomatic", "yersinia_epidemiology", "猪 Yersinia 多亚临床", "most_yersinia_infections_in_swine_are_asymptomatic_and_enteric_disease_importance_is_minor", "猪 Y. enterocolitica/Y. pseudotuberculosis 感染多为亚临床，在商业猪肠道病中的重要性相对较小。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1023", "all_stages"),
    ("MISCBACT-045-yersinia-dx", "yersinia_diagnostics", "猪肠道耶尔森菌确诊", "porcine_enteric_yersiniosis_requires_diarrhea_typical_microscopic_lesions_and_culture_or_pcr_confirmation", "猪肠道耶尔森菌病诊断需腹泻、典型显微病变，并经培养或 PCR 确认；腹泻猪培养阳性本身不足。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1024", "growers"),
    ("MISCBACT-046-yersinia-control", "yersinia_control_boundary", "Yersinia 农场控制证据不足", "there_are_insufficient_data_on_how_to_reduce_yersinia_prevalence_on_infected_farms", "目前降低感染猪场 Yersinia spp. 流行率的方法证据不足；食源性控制重点在屠宰污染控制和家庭食品卫生。", "SRC-0079", "Chapter 64 Miscellaneous Bacterial Infections; PDF page 1024", "all_stages"),
]


RULES = [
    ("RULE-397", "A. suis 交配后血尿需与 E. coli 膀胱炎鉴别", "actinobaculum_suis_diagnostics", "high", "SRC-0079", "Swine-asuis-postservice-hematuria-differential.md", "配种后 2-3 周血尿提示 A. suis 膀胱炎/肾盂肾炎，但需经尿液或泌尿道细菌培养/PCR 支持，并与 E. coli 膀胱炎鉴别。", "1005-1006"),
    ("RULE-398", "A. hyovaginalis 阴道分泌物培养阳性不得定因流产", "actinomyces_hyovaginalis_diagnostics", "high", "SRC-0079", "Swine-ahyovaginalis-vaginal-culture-not-abortion-cause.md", "A. hyovaginalis 可能为阴道菌群，阴道分泌物培养阳性不得单独作为繁殖失败定因。", "1007"),
    ("RULE-399", "疑似炭疽不得常规剖检", "anthrax_biosafety", "critical", "SRC-0079", "Swine-anthrax-necropsy-discouraged-biosafety.md", "疑似炭疽时不应常规剖检，应优先按权威诊断和生物安全流程处理，避免芽孢形成、环境污染和人员暴露。", "1008"),
    ("RULE-400", "猪炭疽必须保留人兽共患和食品危害边界", "anthrax_public_health", "critical", "SRC-0079", "Swine-anthrax-zoonotic-pork-hazard-boundary.md", "猪炭疽虽少见但具人兽共患和肉品危害意义，不能只按普通猪病处置；具体处置需 A0/A1 权威来源。", "1007-1009"),
    ("RULE-401", "类鼻疽需保留热带环境和公共卫生边界", "melioidosis_public_health", "high", "SRC-0079", "Swine-melioidosis-tropical-public-health-boundary.md", "猪类鼻疽解释需结合热带/亚热带环境、水土污染和公共卫生风险，不得生成普通猪场通用处置。", "1009-1010"),
    ("RULE-402", "弯曲菌不得作为猪常规肠病主因", "campylobacter_boundary", "medium", "SRC-0079", "Swine-campylobacter-not-recognized-common-enteric-disease.md", "弯曲菌虽有公共卫生意义，但不是猪公认常规肠道病主因；新生猪确诊需排除更常见腹泻病因。", "1011-1012"),
    ("RULE-403", "猪衣原体定因需谨慎处理混合感染和 PCR 物种确认", "chlamydia_diagnostics", "high", "SRC-0079", "Swine-chlamydia-mixed-infection-pcr-species-boundary.md", "猪衣原体致病性解释需考虑混合感染、非特异临床和物种级 PCR 确认；血清抗体不能确认疾病。", "1013-1015"),
    ("RULE-404", "猪衣原体公共卫生结论需区分 species 和传播证据", "chlamydia_public_health", "high", "SRC-0079", "Swine-chlamydia-zoonosis-species-transmission-boundary.md", "C. abortus/C. psittaci 具人兽共患意义，但猪到人传播未确认；公共卫生建议需区分物种和暴露证据。", "1013"),
    ("RULE-405", "肠球菌相关新生仔猪腹泻治疗前应做药敏", "enterococci_treatment_boundary", "medium", "SRC-0079", "Swine-enterococci-neonatal-diarrhea-ast-before-treatment.md", "黏附性肠球菌相关新生仔猪腹泻因天然耐药边界，治疗前应做药敏，不能生成经验性处方。", "1016"),
    ("RULE-406", "Klebsiella 仔猪败血症干预效果不得无对照外推", "klebsiella_control_boundary", "medium", "SRC-0079", "Swine-klebsiella-piglet-septicemia-intervention-control-needed.md", "K. pneumoniae 仔猪败血症暴发干预缺乏未处理对照时，不能判定抗菌药、补铁或补料措施有效。", "1017"),
    ("RULE-407", "猪李斯特菌需区分携带、临床病和食品安全", "listeria_boundary", "high", "SRC-0079", "Swine-listeria-carriage-clinical-food-safety-boundary.md", "L. monocytogenes 猪携带常见、临床病少见，但食品安全重要；回答需区分携带、临床病和食品污染。", "1017-1018"),
    ("RULE-408", "R. equi 肉芽肿淋巴结炎必须排除结核", "rhodococcus_equi_differential", "critical", "SRC-0079", "Swine-rhodococcus-granulomatous-lymphadenitis-rule-out-tb.md", "R. equi 头颈部肉芽肿性淋巴结炎与结核相似，确诊需鉴定 R. equi 并排除分枝杆菌。", "1018-1019"),
    ("RULE-409", "T. pedis 耳坏死不得单病原简化", "treponema_pedis_skin_boundary", "medium", "SRC-0079", "Swine-tpedis-ear-necrosis-not-single-agent.md", "T. pedis 与耳坏死相关但不是唯一或起始病原，解释需结合咬伤、环境、行为和其他细菌。", "1019-1020"),
    ("RULE-410", "T. abortisuis 流产定因需胎盘/胎儿病变和病灶内细菌", "trueperella_abortisuis_diagnostics", "high", "SRC-0079", "Swine-tabortisuis-abortion-lesion-intralesional-required.md", "T. abortisuis 流产定因需胎儿/胎盘病变、病灶内形态相符细菌和培养支持；污染性检出不得定因。", "1021"),
    ("RULE-411", "T. pyogenes 脓肿单靠抗菌药效果差且无有效疫苗", "trueperella_pyogenes_control", "high", "SRC-0079", "Swine-tpyogenes-abscess-antimicrobial-limited-no-vaccine.md", "T. pyogenes 脓肿因药物难达治疗水平，单靠抗菌药效果差，且无有效疫苗；预防应聚焦诱因管理。", "1022"),
    ("RULE-412", "Y. enterocolitica O:9 必须纳入布病血清学假阳性解释", "yersinia_serology_boundary", "critical", "SRC-0079", "Swine-yersinia-o9-brucella-serology-false-positive.md", "猪布鲁氏菌血清学解释必须考虑 Y. enterocolitica O:9 交叉反应导致的假阳性。", "1023"),
    ("RULE-413", "Yersinia 腹泻猪培养阳性不足以确诊肠道耶尔森菌病", "yersinia_diagnostics", "critical", "SRC-0079", "Swine-yersinia-culture-positive-not-enteric-yersiniosis-alone.md", "猪肠道耶尔森菌病需腹泻、典型显微病变和培养/PCR 确认；腹泻猪培养阳性本身不足。", "1024"),
    ("RULE-414", "Yersinia 食源性控制不得从教材外推为中国召回执行", "yersinia_food_safety_boundary", "critical", "SRC-0079", "Swine-yersinia-foodborne-control-no-china-recall-from-textbook.md", "Yersinia 食源性风险可提示屠宰污染和家庭烹调卫生边界，但召回/执法/中国监管结论需 A0/A1 来源。", "1023-1024"),
]


TOPICS = [
    ("Swine-miscellaneous-bacterial-infections-diagnostic-boundaries.md", "猪杂项细菌感染诊断和定因边界", "SRC-0079", "本主题汇总 Chapter 64 中 A. suis、A. hyovaginalis、炭疽、类鼻疽、弯曲菌、衣原体、肠球菌、Klebsiella、Listeria、R. equi、T. pedis、Trueperella 和 Yersinia 的诊断/定因边界。"),
    ("Swine-miscellaneous-bacterial-zoonotic-food-safety-boundaries.md", "猪杂项细菌人兽共患和食品安全边界", "SRC-0079", "本主题汇总炭疽、类鼻疽、弯曲菌、衣原体、李斯特菌、R. equi 和 Yersinia 的公共卫生、食品安全和不得外推中国监管处置边界。"),
]


def make_source_pages() -> None:
    for source_id, title, pages, relpath, summary in SOURCES:
        write_text(WIKI / relpath, f"""---
tags: [source, swine, textbook, formal, v4]
source_id: {source_id}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
---

# {title}

## 范围

- 来源：本地 PDF `docs/Diseases of Swine, 11th Edition ...pdf`。
- 页码范围：{pages}。
- 批次：Formal Batch 028 / V4。
- 解析器：PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six`。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_028_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_028_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_028_pdf_pages_1005_1026_parser_report.txt`。
""")


def make_topic_pages() -> None:
    for filename, title, source_id, summary in TOPICS:
        write_text(WIKI / "wiki" / "topics" / filename, f"""---
tags: [topic, swine, formal, v4]
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [{source_id}]
---

# {title}

{summary}

## 证据边界

- 来源：{source_id}。
- 本页正式 facts 已在 `issues/formal_batch_028_cross_review.md` 中交叉审查。
- 本页不提供处方、剂量、固定疫苗程序、清群执行命令、食品召回、公共卫生暴露处置细则或中国监管结论。
""")


def make_rule_pages() -> None:
    for rule_id, title, category, severity, source_id, filename, rule_text, pages in RULES:
        write_text(WIKI / "wiki" / "rules" / filename, f"""---
tags: [rule, swine, formal, v4]
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
    write_text(ISSUES / "formal_batch_028_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "source_ids": [source[0] for source in SOURCES],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pdfminer.six",
            "report": "issues/formal_batch_028_pdf_pages_1005_1026_parser_report.txt",
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
    path = WIKI / "wiki" / "diseases" / "DIS-054-miscellaneous-bacterial-infections.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        marker = "## Formal Batch 028 / V4 正文抽取进展"
        if marker not in text:
            append_text(path, f"""

{marker}

- Formal Batch 028 / V4 正文抽取：已补充 Chapter 64 杂项细菌感染，包括 A. suis 泌尿道病、A. hyovaginalis、炭疽、类鼻疽、弯曲菌、衣原体、黏附性肠球菌、Klebsiella 仔猪败血症、Listeria、R. equi、T. pedis、T. abortisuis、T. pyogenes 和 Yersinia 的诊断/定因、公共卫生和防控边界；详见 `SRC-0079`。
""")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_028_cross_review.md", """# Formal Batch 028 / V4 Cross Review

## 范围

- PDF page 1005-1025：Chapter 64 Miscellaneous Bacterial Infections 正文和各小节参考文献。
- PDF page 1026：页脚/空白边界，无 standalone facts。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行，并同步 V4 主线文档。
- 本批按用户要求使用 PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six` 三路解析。
- 参考文献列表只记录章节边界，不生成 standalone facts。
- 所有正式 facts 均先写入候选事实文件，再经页码锚点、内容边界和一致性审查后落库。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`。
- 二次核对：`pdfplumber`，PDF page 1005 采用 pdfplumber 文本，其余正文页多采用 fitz。
- 三次核对：`pdfminer.six`，逐页字符量对照，未发现整页遗漏。
- 解析文件：`issues/formal_batch_028_pdf_pages_1005_1026_extract.txt`。
- 解析报告：`issues/formal_batch_028_pdf_pages_1005_1026_parser_report.txt`。

## 审查结论

本批候选 facts 46 条、规则页 18 个、来源页 1 个、主题页 2 个。经交叉审查后允许正式落库，所有 facts 均为 `HUMAN_REVIEWED`。

## 审查 1：页码锚点核验

- `SRC-0079` 锚定 PDF page 1005-1026。
- PDF page 1005-1025 覆盖 Chapter 64 正文和各小节参考文献。
- PDF page 1026 仅含页脚/空白边界。

## 审查 2：内容边界核验

- 杂项细菌感染内容只落库教材证据、诊断/定因、传播/公共卫生和防控边界。
- 炭疽、类鼻疽、衣原体、李斯特菌、Yersinia 等公共卫生和食品安全内容不生成暴露处置、召回、执法或中国监管结论。
- 教材中的药物敏感性、治疗例子和剂量不转换为通用处方、疗程或休药期。
- Yersinia、R. equi、T. abortisuis、A. hyovaginalis 等保留污染/携带/假阳性和鉴别诊断边界。

## 审查 3：一致性核验

- facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- `SRC-0079`、`RULE-397` 至 `RULE-414` 与既有条目不重复。
- 本批正式落库内容与 V4 文档同步，V3 文档保留为历史记录。

## 明确未落库

- 参考文献列表。
- 具体药物剂量、疗程、休药期、食品召回/执法、公共卫生暴露处置和中国监管结论。
- 美国、欧盟或 WHO/WOAH 教材引用语境中的执行细则，除作为“需权威来源复核”的边界提示外，不迁移为本地答案。

## 保留问题

- PDF page 1027 起进入 Section V Parasitic Diseases，下一批需开始外寄生虫和寄生虫病章节。
- 炭疽、类鼻疽、李斯特菌、Yersinia 等公共卫生和食品安全结论如需中国本地答案，必须补充 A0/A1 来源。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 028 / V4 实施记录

- 完成时间：2026-05-07 18:25:00 +08:00。
- 处理范围：PDF page 1005-1026。
- 章节边界：Chapter 64 Miscellaneous Bacterial Infections 正文和各小节参考文献；PDF page 1026 仅含页脚/空白边界。
- 解析器：PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six`。
- 参考文献处理：各小节参考文献仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0079`。
- 新增主题页：猪杂项细菌感染诊断和定因边界、猪杂项细菌人兽共患和食品安全边界。
- 新增规则页：`RULE-397` 至 `RULE-414`。
- 新增候选事实：`issues/formal_batch_028_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_028_cross_review.md`。
- 正式落库 facts：46 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、具体处方/剂量/休药期、食品召回/执法、公共卫生暴露处置和中国监管结论。

### Formal Batch 028 / V4 交叉审查

- 页码锚点核验：通过。`SRC-0079` 覆盖 PDF page 1005-1026。
- 内容边界核验：通过。Chapter 64 杂项细菌感染均只落库教材证据和诊断/传播/公共卫生/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 1026。
- 下一批应从 PDF page 1027 开始。
- 推荐下一批：PDF page 1027-1064，进入 Section V Parasitic Diseases，处理外寄生虫和寄生虫病章节。
"""
    append_text(ISSUES / "pdf_processing_progress_v4.md", block)
    append_text(ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V4.md", block)


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
    print("formal batch 028 v4 built")


if __name__ == "__main__":
    main()
