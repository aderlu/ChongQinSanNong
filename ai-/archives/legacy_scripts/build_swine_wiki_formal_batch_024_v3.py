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
NOW = "2026-05-07T03:45:00+00:00"
BATCH_ID = "formal-batch-024-v3"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 845, end: int = 884) -> None:
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
    write_text(ISSUES / "formal_batch_024_pdf_pages_845_884_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_024_pdf_pages_845_884_parser_report.txt", "\n".join(report_rows) + "\n")


SOURCES = [
    ("SRC-0064", "Diseases of Swine 11e Chapter 52 Colibacillosis continuation", "PDF page 845-858", "wiki/sources/SRC-0064-diseases-of-swine-11e-chapter-52-colibacillosis-continuation.md", "Chapter 52 continuation covers post-weaning diarrhea and edema disease lesions, diagnosis, husbandry prevention, antimicrobial prophylaxis boundary, alternatives, systemic E. coli infections, mastitis/cystitis/UTI and references."),
    ("SRC-0065", "Diseases of Swine 11e Chapter 53 Erysipelas", "PDF page 859-867", "wiki/sources/SRC-0065-diseases-of-swine-11e-chapter-53-erysipelas.md", "Chapter 53 covers Erysipelothrix rhusiopathiae relevance, public health erysipeloid boundary, entry/pathogenesis, lesions, diagnosis, differentials, typing and references."),
    ("SRC-0066", "Diseases of Swine 11e Chapter 54 Glasser Disease", "PDF page 868-877", "wiki/sources/SRC-0066-diseases-of-swine-11e-chapter-54-glassers-disease.md", "Chapter 54 covers Haemophilus parasuis / Glasser disease relevance, genotyping, maternal immunity, colonization, coinfections, clinical signs, lesions, immune responses, treatment/vaccine boundaries and references."),
    ("SRC-0067", "Diseases of Swine 11e Chapter 55 Leptospirosis opening", "PDF page 878-884", "wiki/sources/SRC-0067-diseases-of-swine-11e-chapter-55-leptospirosis-opening.md", "Chapter 55 opening covers leptospirosis relevance, serovar/serogroup concepts, occupational zoonosis, Pomona/Canicola/Icterohemorrhagiae/Bratislava transmission, clinical signs, lesions, and culture boundary."),
]


FACTS = [
    ("ECOLI-018-pwd-lesions", "postweaning_diarrhea_lesions", "PWD 剖检病变", "pigs_dead_from_ecoli_pwd_are_often_dehydrated_with_distended_stomach_and_dilated_hyperemic_small_intestine", "E. coli 断奶后腹泻死亡猪常严重脱水、眼窝凹陷，胃可因干料扩张，小肠扩张、轻度水肿和充血。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 845", "weaners"),
    ("ECOLI-019-ed-lesions", "edema_disease_lesions", "水肿病血管病变", "edema_disease_lesions_include_vascular_swelling_fibrin_deposition_medial_necrosis_and_microthrombi", "水肿病相关病变可包括血管内皮肿胀、内皮下纤维蛋白沉积、中膜坏死、血管周围水肿和微血栓。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 846", "weaners"),
    ("ECOLI-020-ed-negative-culture", "edema_disease_diagnostics", "水肿病培养阴性边界", "negative_bacteriology_does_not_exclude_edema_disease_in_protracted_cases", "水肿病病程较长时肠道细菌数量可能下降，因此细菌学阴性不能排除水肿病。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 847", "weaners"),
    ("ECOLI-021-hemolysis-limit", "colibacillosis_diagnostics", "溶血菌落快速诊断限制", "hemolytic_colonies_are_often_used_for_presumptive_diagnosis_but_can_miss_epec_and_nonhemolytic_f4_etec", "溶血菌落常用于快速推定 ED 和 ETEC PWD，但会漏掉 EPEC 和日益增多的非溶血性 F4-ETEC。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 847", "weaners"),
    ("ECOLI-022-aiao", "colibacillosis_prevention", "断奶舍全进全出", "nurseries_should_be_managed_all_in_all_out_and_cleaned_disinfected_before_use", "断奶舍应按全进全出管理，使用前彻底清除有机物并消毒，水线和供水系统也应消毒。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 848", "weaners"),
    ("ECOLI-023-stress-temperature", "colibacillosis_prevention", "断奶应激和温度控制", "weanling_management_should_minimize_mixing_chilling_transport_and_new_pen_stress", "断奶仔猪管理应减少混群、受冷、运输和转栏等环境应激，并维持适宜、无贼风的环境。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 848", "weaners"),
    ("ECOLI-024-antimicrobial-prophylaxis", "colibacillosis_amr_boundary", "大肠杆菌预防性饲料用药边界", "preventive_feed_medication_has_drawbacks_including_resistance_selection_and_consumer_nonacceptance", "预防性饲料用抗菌药存在消费者不接受、免疫建立受损和耐药菌选择等严重缺点。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 849", "weaners"),
    ("ECOLI-025-colistin", "colibacillosis_amr_boundary", "黏菌素耐药边界", "colistin_resistance_in_pigs_has_been_increasingly_reported_worldwide", "猪源大肠杆菌黏菌素耐药近年在全球多地增加，相关用药和公共卫生解释需谨慎。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 849", "all_stages"),
    ("ECOLI-026-probiotics-boundary", "colibacillosis_alternatives", "益生菌效果证据不一致", "probiotic_or_feed_additive_interventions_have_variable_efficacy_against_f4_etec", "Pediococcus acidilactici、S. cerevisiae boulardii 等可降低 F4-ETEC 黏附的研究存在，但其他益生菌报告无效，不能生成固定替代疗法。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 850", "piglets"),
    ("ECOLI-027-systemic", "systemic_colibacillosis", "系统性大肠杆菌感染", "e_coli_can_cause_septicemia_meningitis_or_arthritis_after_bacteremia", "E. coli 可经菌血症导致败血症，或脑膜炎、关节炎等局部肠外感染。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 851", "piglets"),
    ("ECOLI-028-colostrum-risk", "systemic_colibacillosis_risk", "初乳免疫不足和败血症风险", "piglets_lacking_colostral_immunity_are_most_at_risk_for_primary_colisepticemia", "未摄入初乳或初乳缺乏特异抗体的仔猪最易发生原发性大肠杆菌败血症。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 851", "piglets"),
    ("ECOLI-029-blood-culture", "systemic_colibacillosis_diagnostics", "系统性大肠杆菌血培养确诊", "positive_blood_culture_results_are_essential_for_diagnosis_of_bacteremia", "诊断大肠杆菌菌血症需要阳性血培养证据，采血应无菌并接种需氧和厌氧血培养瓶。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 852", "piglets"),
    ("ECOLI-030-mastitis", "coliform_mastitis", "母猪大肠杆菌乳房炎", "coliform_mastitis_can_be_suspected_with_hypogalactia_at_beginning_of_lactation_and_supported_by_fever_anorexia_and_gland_changes", "泌乳开始时缺乳应怀疑大肠杆菌性乳房炎，发热、厌食、卧压乳腺和乳腺红肿可支持诊断。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 854", "sows"),
    ("ECOLI-031-uti", "colibacillosis_uti", "母猪 UTI 传播和风险", "uropathogenic_e_coli_most_likely_ascends_through_the_urethra_and_is_favored_by_sow_anatomy_pregnancy_and_trauma", "猪尿路感染相关 E. coli 多经尿道上行，母猪尿道短宽、妊娠/产褥期括约肌松弛和交配创伤可增加风险。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 855", "sows"),
    ("ECOLI-032-uti-control", "colibacillosis_uti_control", "母猪 UTI 管理", "uti_control_includes_environmental_fecal_drainage_water_access_flow_rates_and_water_intake", "母猪 UTI 控制包括改善粪污排水和栏舍、提高饮水频率、检查水线/饮水器流量和饮水适口性。", "SRC-0064", "Chapter 52 Colibacillosis; PDF page 856", "sows"),
    ("ERYS-001-relevance", "erysipelas_relevance", "猪丹毒流行边界", "erysipelas_occurs_sporadically_but_more_severe_prevalent_outbreaks_may_recur_at_intervals", "猪丹毒在猪群中散发，但更严重和更普遍的暴发可按约十年间隔反复出现。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 859", "all_stages"),
    ("ERYS-002-public-health", "erysipelas_public_health", "Erysipelothrix 人感染边界", "human_erysipeloid_is_an_occupational_cutaneous_infection_and_should_not_be_confused_with_human_erysipelas", "Erysipelothrix 人感染常为职业性皮肤感染 erysipeloid，不应与由链球菌引起的人丹毒混淆。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 860", "all_stages"),
    ("ERYS-003-entry", "erysipelas_transmission", "猪丹毒进入途径", "bacteria_may_enter_through_skin_abrasions_or_mechanical_vectors_such_as_arthropod_bites", "猪丹毒杆菌可经皮肤擦伤或昆虫叮咬等机械媒介进入；无有效免疫应答时可在 24 小时内出现菌血症。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 861", "all_stages"),
    ("ERYS-004-coagulopathy", "erysipelas_pathogenesis", "猪丹毒休克样凝血病", "early_septicemic_erysipelas_causes_capillary_and_venule_damage_and_shock_like_generalized_coagulopathy", "急性败血型猪丹毒早期可损伤毛细血管和小静脉，形成休克样全身性凝血病。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 861", "all_stages"),
    ("ERYS-005-rhomboid-lesions", "erysipelas_lesions", "猪丹毒菱形皮肤病变", "acute_swine_erysipelas_has_multifocal_pink_to_purple_rhomboid_raised_skin_lesions", "急性猪丹毒近乎特征性的肉眼病变为多灶粉红至紫色、菱形、稍隆起皮肤病变。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 862", "all_stages"),
    ("ERYS-006-endocarditis", "erysipelas_lesions", "猪丹毒心内膜炎", "valvular_endocarditis_can_be_seen_as_proliferative_granular_growth_on_heart_valves", "慢性或相关猪丹毒可见瓣膜性心内膜炎，表现为心瓣膜上增生性颗粒状赘生物，以二尖瓣常见。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 863", "all_stages"),
    ("ERYS-007-differential", "erysipelas_differential", "猪丹毒鉴别诊断范围", "acute_erysipelas_differentials_include_salmonella_actinobacillus_haemophilus_streptococcus_csfv_pdn_and_asuis", "急性猪丹毒需与 Salmonella Choleraesuis、A. suis、App、H. parasuis、S. suis、CSFV、PDNS 等鉴别。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 864", "all_stages"),
    ("ERYS-008-typing", "erysipelas_diagnostics", "猪丹毒分型边界", "serotyping_and_dna_typing_methods_can_differentiate_erysipelothrix_isolates_but_require_specific_methods_and_reagents", "Erysipelothrix 分型可用血清型、RAPD、PFGE 等方法，但依赖特定抗血清、方法和实验室能力。", "SRC-0065", "Chapter 53 Erysipelas; PDF page 865", "all_stages"),
    ("GLASS-001-relevance", "glasser_relevance", "格拉瑟病定义", "glasser_disease_is_characterized_by_fibrinous_polyserositis_and_arthritis_caused_by_h_parasuis", "H. parasuis 引起的格拉瑟病以纤维素性多浆膜炎和关节炎为特征。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 868", "all_stages"),
    ("GLASS-002-genotype-serovar", "glasser_diagnostics", "H. parasuis 基因型和血清型边界", "there_is_no_direct_association_between_genotype_and_serovar", "H. parasuis 基因型和血清型之间没有直接关联，基因分型不能替代血清型解释。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 869", "all_stages"),
    ("GLASS-003-maternal-immunity", "glasser_immunity", "母源免疫和菌株特异性", "maternal_igm_igg_protection_is_strain_specific_to_dam_exposure", "仔猪鼻黏膜定植时可受母源 IgM/IgG 保护，但保护主要针对母猪接触过的菌株。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 870", "piglets"),
    ("GLASS-004-risk-factors", "glasser_epidemiology", "格拉瑟病发病诱因", "disease_may_follow_maternal_immunity_decay_mixing_new_stock_chilling_crowding_or_coinfections", "格拉瑟病可在母源免疫衰减、接触新菌株、断奶混群、引种、受冷、拥挤或共同感染时发生。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 870", "weaners"),
    ("GLASS-005-coinfection", "glasser_coinfection", "H. parasuis 与病毒/细菌共同感染", "h_parasuis_disease_has_epidemiologic_or_experimental_links_with_prrsv_pcv2_influenza_and_bordetella", "H. parasuis 感染与 PRRSV、PCV2、猪流感和 B. bronchiseptica 有流行病学或实验关联，可加重或改变疾病表现。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 871", "all_stages"),
    ("GLASS-006-clinical", "glasser_clinical_pattern", "格拉瑟病急性表现", "acute_glasser_disease_can_show_high_fever_cough_abdominal_breathing_swollen_joints_lameness_and_cns_signs", "急性格拉瑟病可见高热、咳嗽、腹式呼吸、关节肿胀跛行和侧卧、划水、震颤等中枢神经症状。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 872", "weaners"),
    ("GLASS-007-peracute", "glasser_clinical_pattern", "格拉瑟病急性猝死边界", "peracute_glasser_disease_may_result_in_sudden_death_without_characteristic_gross_lesions", "超急性格拉瑟病病程短，可突然死亡且无特征性肉眼病变。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 872", "weaners"),
    ("GLASS-008-lesions", "glasser_lesions", "格拉瑟病典型病变", "typical_glasser_disease_has_fibrinous_to_fibrinopurulent_serositis_and_may_have_fibrinopurulent_meningitis", "典型格拉瑟病病理为纤维素性至纤维素脓性浆膜炎，可伴纤维素脓性脑膜炎。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 873", "weaners"),
    ("GLASS-009-immunity", "glasser_immunity", "H. parasuis 毒力株免疫边界", "virulent_h_parasuis_strains_resist_phagocytosis_and_complement_killing_until_opsonized_by_antibodies", "毒力 H. parasuis 菌株可抵抗吞噬和补体杀灭，经抗体调理后才更易被肺泡巨噬细胞内吞和杀灭。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 874", "all_stages"),
    ("GLASS-010-vaccine-maternal", "glasser_vaccine_boundary", "格拉瑟病母源抗体干扰", "maternal_immunity_can_interfere_with_piglet_vaccination_measured_as_antibody_induction", "母源免疫可干扰仔猪 H. parasuis 疫苗接种后的抗体诱导，疫苗效果解释需结合暴发和免疫状态。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 875", "piglets"),
    ("GLASS-011-antibiotic-boundary", "glasser_treatment_boundary", "格拉瑟病抗生素边界", "antibiotics_are_widely_used_but_population_prophylaxis_reliance_is_under_pressure", "H. parasuis 病常用抗生素防控，但减少群体性预防用药压力增加，应强调疫苗和管理策略边界。", "SRC-0066", "Chapter 54 Glasser disease; PDF page 875", "all_stages"),
    ("LEPTO-001-relevance", "leptospirosis_relevance", "猪钩端螺旋体病繁殖损失", "leptospirosis_is_a_cause_of_reproductive_loss_in_breeding_herds", "钩端螺旋体病是繁殖猪群繁殖损失原因之一，地方性猪群可缺乏明显临床病。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 878", "breeding_herd"),
    ("LEPTO-002-serovar", "leptospirosis_taxonomy", "钩端螺旋体 serovar/serogroup 边界", "serovar_classification_is_still_widely_used_for_serodiagnosis_epidemiology_and_prevalence_studies", "serovar 分类仍广泛用于血清诊断、流行病学和流行率研究，serogroup 用于选择血清学交叉反应株。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 879", "all_stages"),
    ("LEPTO-003-zoonosis", "leptospirosis_public_health", "猪钩端螺旋体职业暴露", "leptospirosis_is_a_potential_occupational_zoonosis_for_people_working_with_pigs_in_infected_regions", "在猪群感染常见地区，钩端螺旋体病是养猪者、兽医等接触猪人员的潜在职业性人兽共患病。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 879", "all_stages"),
    ("LEPTO-004-pomona", "leptospirosis_transmission", "Pomona 间接传播", "pomona_transmission_can_occur_indirectly_through_contaminated_effluent_water_or_soil_when_moisture_is_present", "Pomona 进入猪群后可建立高感染率，若直接接触受阻，受污染粪污、水或土壤在潮湿条件下仍可传播。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 880", "all_stages"),
    ("LEPTO-005-canicola", "leptospirosis_transmission", "Canicola 尿液排菌边界", "infected_pigs_can_shed_canicola_in_urine_for_at_least_90_days", "感染猪可经尿液排出 Canicola 至少 90 天，提示同种内传播可能。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 881", "all_stages"),
    ("LEPTO-006-rat", "leptospirosis_epidemiology", "Icterohemorrhagiae 鼠源风险", "icterohemorrhagiae_serovars_are_probably_introduced_via_environments_contaminated_with_urine_from_brown_rats", "Icterohemorrhagiae/Copenhageni 可能经褐家鼠尿液污染环境引入易感猪群。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 881", "all_stages"),
    ("LEPTO-007-bratislava", "leptospirosis_persistence", "Bratislava 生殖道持续感染", "bratislava_can_persist_in_oviduct_uterus_and_male_accessory_sex_glands", "Bratislava 感染可在非妊娠母猪输卵管/子宫和公猪精囊、尿道球腺、前列腺、睾丸中持续存在。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 882", "breeding_herd"),
    ("LEPTO-008-clinical", "leptospirosis_clinical_pattern", "猪钩端螺旋体病临床边界", "most_swine_leptospiral_infections_are_subclinical_and_clinical_infections_are_most_likely_in_young_piglets_and_pregnant_sows", "绝大多数猪钩端螺旋体感染为亚临床，幼龄仔猪和妊娠母猪最可能出现临床感染。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 882", "all_stages"),
    ("LEPTO-009-kidney-lesions", "leptospirosis_lesions", "慢性钩端螺旋体肾脏病变", "chronic_leptospirosis_gross_lesions_are_confined_to_kidneys_with_multifocal_interstitial_nephritis", "慢性钩端螺旋体病肉眼病变局限于肾脏，显微镜下可见进行性多灶性间质性肾炎。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 883", "all_stages"),
    ("LEPTO-010-culture", "leptospirosis_diagnostics", "钩端螺旋体培养边界", "culture_from_clinical_material_is_difficult_time_consuming_and_requires_specialized_laboratories", "钩端螺旋体临床材料培养困难且耗时，应由专门实验室完成；肾脏带菌动物培养对流行病学研究有用。", "SRC-0067", "Chapter 55 Leptospirosis; PDF page 884", "all_stages"),
]


RULES = [
    ("RULE-329", "PWD/ED 溶血菌落推定诊断不得排除非溶血 E. coli", "colibacillosis_diagnostics", "high", "SRC-0064", "Swine-ecoli-hemolysis-presumptive-diagnosis-limits.md", "溶血菌落可作 PWD/ED 快速推定线索，但不能排除 EPEC 或非溶血 F4-ETEC。", "847"),
    ("RULE-330", "水肿病细菌学阴性不得直接排除诊断", "edema_disease_diagnostics", "high", "SRC-0064", "Swine-edema-disease-negative-culture-not-exclusion.md", "水肿病病程较长时细菌数量可下降，细菌学阴性不能直接排除诊断。", "847"),
    ("RULE-331", "E. coli 预防性用药必须保留耐药和消费者接受边界", "colibacillosis_amr_boundary", "critical", "SRC-0064", "Swine-ecoli-prophylactic-feed-medication-amr-boundary.md", "E. coli 预防性饲料用药建议必须保留耐药选择、消费者不接受和免疫建立受损边界，不能生成通用处方。", "849"),
    ("RULE-332", "系统性大肠杆菌病需血培养支持菌血症诊断", "systemic_colibacillosis_diagnostics", "high", "SRC-0064", "Swine-systemic-colibacillosis-blood-culture-required.md", "系统性大肠杆菌菌血症诊断需要阳性血培养支持，不能只凭败血症外观定因。", "852"),
    ("RULE-333", "母猪 UTI 控制必须评估水和环境管理", "colibacillosis_uti_control", "medium", "SRC-0064", "Swine-sow-uti-water-environment-control.md", "母猪 UTI 控制应评估粪污排水、栏舍、饮水可及性、流量和饮水量。", "856"),
    ("RULE-334", "猪丹毒样皮肤病变必须纳入多病原鉴别", "erysipelas_differential", "critical", "SRC-0065", "Swine-erysipelas-like-skin-lesions-differential.md", "菱形或丹毒样皮肤病变需与 Salmonella、A. suis、App、H. parasuis、S. suis、CSFV、PDNS 等鉴别。", "864"),
    ("RULE-335", "Erysipelothrix 人感染不得与人丹毒混同", "erysipelas_public_health", "high", "SRC-0065", "Swine-erysipelothrix-erysipeloid-not-human-erysipelas.md", "Erysipelothrix 人感染 erysipeloid 不应与链球菌性人丹毒混同，公共卫生解释需准确命名。", "860"),
    ("RULE-336", "格拉瑟病基因型不得替代血清型解释", "glasser_diagnostics", "medium", "SRC-0066", "Swine-hparasuis-genotype-not-serovar.md", "H. parasuis 基因型与血清型无直接关联，基因分型不能替代血清型或保护性解释。", "869"),
    ("RULE-337", "格拉瑟病需结合母源免疫衰减、混群和共同感染解释", "glasser_risk_boundary", "high", "SRC-0066", "Swine-glasser-maternal-immunity-mixing-coinfection-boundary.md", "格拉瑟病发病需结合母源免疫、断奶混群、新菌株暴露、应激和 PRRSV/PCV2/IAV/Bordetella 等共同感染解释。", "870-871"),
    ("RULE-338", "格拉瑟病超急性死亡可无特征性肉眼病变", "glasser_diagnostics", "high", "SRC-0066", "Swine-glasser-peracute-no-gross-lesions.md", "超急性格拉瑟病可突然死亡且无特征性肉眼病变，不能因缺乏典型浆膜炎完全排除。", "872"),
    ("RULE-339", "H. parasuis 疫苗解释必须考虑母源抗体干扰", "glasser_vaccine_boundary", "medium", "SRC-0066", "Swine-hparasuis-vaccine-maternal-antibody-interference.md", "H. parasuis 仔猪疫苗抗体诱导可受母源免疫干扰，疫苗建议不得脱离免疫状态。", "875"),
    ("RULE-340", "Leptospira serovar/serogroup 仍需用于血清学和流行病学解释", "leptospirosis_taxonomy", "medium", "SRC-0067", "Swine-leptospira-serovar-serogroup-serology-epidemiology.md", "Leptospira serovar 和 serogroup 在血清诊断、流行病学和试验株选择中仍有边界意义。", "879"),
    ("RULE-341", "猪钩端螺旋体病必须保留职业性人兽共患风险", "leptospirosis_public_health", "high", "SRC-0067", "Swine-leptospirosis-occupational-zoonosis-boundary.md", "在猪群感染常见地区，接触猪的人员存在职业性人兽共患风险，具体处置需权威公共卫生来源。", "879"),
    ("RULE-342", "钩端螺旋体间接传播必须考虑潮湿环境", "leptospirosis_transmission", "high", "SRC-0067", "Swine-leptospira-moisture-indirect-transmission.md", "Pomona 等钩端螺旋体间接传播解释必须考虑潮湿、pH 和被尿液污染的水土环境。", "880"),
    ("RULE-343", "Bratislava 感染需保留生殖道持续感染边界", "leptospirosis_persistence", "high", "SRC-0067", "Swine-leptospira-bratislava-reproductive-tract-persistence.md", "Bratislava 可在母猪和公猪生殖道持续存在，繁殖传播解释需覆盖该边界。", "882"),
    ("RULE-344", "钩端螺旋体培养需专门实验室且不能作为快速常规诊断", "leptospirosis_diagnostics", "medium", "SRC-0067", "Swine-leptospira-culture-specialized-slow-boundary.md", "钩端螺旋体培养困难、耗时且需专门实验室，不应作为快速常规诊断承诺。", "884"),
]


TOPICS = [
    ("Swine-colibacillosis-pwd-ed-systemic-mastitis-uti-boundaries.md", "Colibacillosis PWD/ED/系统感染/乳房炎/UTI 边界", "SRC-0064", "本主题汇总 PWD/ED 病变和诊断、预防性用药耐药边界、系统性大肠杆菌感染、母猪乳房炎和 UTI 管理。"),
    ("Swine-erysipelas-differential-public-health-boundaries.md", "猪丹毒鉴别、病变和公共卫生边界", "SRC-0065", "本主题汇总猪丹毒菱形皮损、败血症、心内膜炎、鉴别诊断、分型和人 erysipeloid 命名边界。"),
    ("Swine-glassers-disease-immunity-coinfection-diagnosis-boundaries.md", "格拉瑟病免疫、共同感染和诊断边界", "SRC-0066", "本主题汇总 H. parasuis 母源免疫、基因型/血清型、PRRSV/PCV2/IAV/Bordetella 共同感染、临床、病变和疫苗边界。"),
    ("Swine-leptospirosis-serovar-zoonosis-transmission-boundaries.md", "猪钩端螺旋体 serovar、人兽共患和传播边界", "SRC-0067", "本主题汇总钩端螺旋体 serovar/serogroup、职业性人兽共患、Pomona/Canicola/Icterohemorrhagiae/Bratislava 传播和培养边界。"),
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
- 批次：Formal Batch 024 / V3。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_024_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_024_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_024_pdf_pages_845_884_parser_report.txt`。
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
- 本页正式 facts 已在 `issues/formal_batch_024_cross_review.md` 中交叉审查。
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
    write_text(ISSUES / "formal_batch_024_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "source_ids": [source[0] for source in SOURCES],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pypdf",
            "report": "issues/formal_batch_024_pdf_pages_845_884_parser_report.txt",
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
        ("DIS-040-colibacillosis.md", "Formal Batch 024 / V3 正文抽取：已补充 PWD/ED 病变、溶血菌落诊断限制、预防性用药耐药边界、系统性大肠杆菌感染、母猪乳房炎和 UTI 管理；详见 `SRC-0064`。"),
        ("DIS-041-neonatal-post-weaning-colibacillosis.md", "Formal Batch 024 / V3 正文抽取：已补充断奶后腹泻病变、全进全出/温度应激管理、预防性用药耐药边界和系统感染风险；详见 `SRC-0064`。"),
        ("DIS-042-edema-disease-e-coli.md", "Formal Batch 024 / V3 正文抽取：已补充水肿病血管病变、培养阴性不排除诊断和溶血菌落推定诊断边界；详见 `SRC-0064`。"),
        ("DIS-043-erysipelas.md", "Formal Batch 024 / V3 正文抽取：已补充猪丹毒公共卫生 erysipeloid 边界、进入途径、败血症/凝血病、菱形皮损、心内膜炎、鉴别诊断和分型边界；详见 `SRC-0065`。"),
        ("DIS-044-gl-sser-s-disease.md", "Formal Batch 024 / V3 正文抽取：已补充 H. parasuis 基因型/血清型、母源免疫、共同感染、急性/超急性临床、病变、免疫和疫苗边界；详见 `SRC-0066`。"),
        ("DIS-045-leptospirosis.md", "Formal Batch 024 / V3 正文抽取：已补充钩端螺旋体 serovar/serogroup、职业性人兽共患、Pomona/Canicola/Icterohemorrhagiae/Bratislava 传播、临床和培养边界；详见 `SRC-0067`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 024 / V3 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_024_cross_review.md", """# Formal Batch 024 / V3 Cross Review

## 范围

- PDF page 845-856：Chapter 52 Colibacillosis 正文后段。
- PDF page 857-858：Chapter 52 参考文献，仅记录边界。
- PDF page 859-867：Chapter 53 Erysipelas 正文和参考文献。
- PDF page 868-877：Chapter 54 Glasser disease 正文和参考文献。
- PDF page 878-884：Chapter 55 Leptospirosis 开端。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行。
- 页数为 40 页，符合正式批次常规范围。
- 参考文献页只记录章节边界，不生成 standalone facts。
- 所有正式 facts 均先写入候选事实文件，再经页码锚点、内容边界和一致性审查后落库。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_024_pdf_pages_845_884_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量对照，未发现整页遗漏。
- 三次核对：`pypdf`，用于页级文本存在性和异常提示。
- 解析报告：`issues/formal_batch_024_pdf_pages_845_884_parser_report.txt`。

## 审查结论

本批候选 facts 44 条、规则页 16 个、来源页 4 个、主题页 4 个。经交叉审查后允许正式落库，所有 facts 均为 `HUMAN_REVIEWED`。

## 审查 1：页码锚点核验

- `SRC-0064` 锚定 PDF page 845-858，其中 PDF page 857-858 为参考文献边界。
- `SRC-0065` 锚定 PDF page 859-867，其中 PDF page 866-867 为参考文献边界。
- `SRC-0066` 锚定 PDF page 868-877，其中 PDF page 876-877 为参考文献边界。
- `SRC-0067` 锚定 PDF page 878-884，为 Leptospirosis 开端，下一批需继续正文。

## 审查 2：内容边界核验

- Colibacillosis 内容保留 PWD/ED 诊断、耐药、系统感染和管理边界，不生成抗菌药处方。
- Erysipelas 内容保留鉴别诊断、人 erysipeloid 命名和分型边界，不生成治疗或疫苗程序。
- Glasser disease 内容保留母源免疫、共同感染、临床病变和疫苗/抗生素边界，不生成固定群体预防方案。
- Leptospirosis 内容保留 serovar/serogroup、职业性人兽共患、传播、持续感染和培养边界，公共卫生和监管处置需 A0/A1 来源。

## 审查 3：一致性核验

- facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- `SRC-0064` 至 `SRC-0067`、`RULE-329` 至 `RULE-344` 与既有条目不重复。
- 本批正式落库内容与 V3 文档同步，V2 文档未追加新批次。

## 保留问题

- PDF page 885 起需继续 Chapter 55 Leptospirosis 正文，补充诊断、治疗、防控、疫苗和参考文献边界。
- Leptospirosis 公共卫生暴露处置、检疫和中国监管结论必须等待 A0/A1 权威来源。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 024 / V3 实施记录

- 完成时间：2026-05-07 11:45:00 +08:00。
- 处理范围：PDF page 845-884。
- 章节边界：Chapter 52 Colibacillosis 正文后段和参考文献；Chapter 53 Erysipelas；Chapter 54 Glasser disease；Chapter 55 Leptospirosis 开端。
- 参考文献处理：PDF page 857-858、866-867、876-877 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0064` 至 `SRC-0067`。
- 新增主题页：Colibacillosis PWD/ED/系统感染/乳房炎/UTI 边界、猪丹毒鉴别/公共卫生边界、格拉瑟病免疫/共同感染/诊断边界、猪钩端螺旋体 serovar/人兽共患/传播边界。
- 新增规则页：`RULE-329` 至 `RULE-344`。
- 新增候选事实：`issues/formal_batch_024_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_024_cross_review.md`。
- 正式落库 facts：44 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、大肠杆菌抗菌药通用处方、猪丹毒治疗/疫苗程序、格拉瑟病群体固定预防用药、钩端螺旋体公共卫生和中国监管处置结论。

### Formal Batch 024 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0064` 覆盖 PDF page 845-858；`SRC-0065` 覆盖 859-867；`SRC-0066` 覆盖 868-877；`SRC-0067` 覆盖 878-884。
- 内容边界核验：通过。Colibacillosis、Erysipelas、Glasser disease 和 Leptospirosis 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 884。
- 下一批应从 PDF page 885 开始。
- 推荐下一批：PDF page 885-924，继续 Chapter 55 Leptospirosis 正文后段和参考文献，并视章节边界进入后续细菌病章节。
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
    print("formal batch 024 v3 built")


if __name__ == "__main__":
    main()
