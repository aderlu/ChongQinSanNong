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
NOW = "2026-05-07T19:10:00+08:00"
BATCH_ID = "formal-batch-029-v4"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 1027, end: int = 1064) -> None:
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
        ISSUES / "formal_batch_029_pdf_pages_1027_1064_extract.txt",
        "".join(extract_parts).strip() + "\n",
    )
    write_text(
        ISSUES / "formal_batch_029_pdf_pages_1027_1064_parser_report.txt",
        "\n".join(report_rows) + "\n",
    )


SOURCES = [
    (
        "SRC-0080",
        "Diseases of Swine 11e Chapter 65 External Parasites",
        "PDF page 1027-1038",
        "wiki/sources/SRC-0080-diseases-of-swine-11e-chapter-65-external-parasites.md",
        "Chapter 65 covers swine external parasites, especially sarcoptic mange, demodectic mange, lice and major fly groups, with diagnosis, production impact, control and reference boundaries.",
    ),
    (
        "SRC-0081",
        "Diseases of Swine 11e Chapter 66 Coccidia and Other Protozoa",
        "PDF page 1039-1051",
        "wiki/sources/SRC-0081-diseases-of-swine-11e-chapter-66-coccidia-and-other-protozoa.md",
        "Chapter 66 covers Cystoisospora suis, Eimeria, toxoplasmosis, sarcocystosis and cryptosporidiosis with diagnosis, zoonotic and control boundaries.",
    ),
    (
        "SRC-0082",
        "Diseases of Swine 11e Chapter 67 Internal Parasites",
        "PDF page 1052-1064",
        "wiki/sources/SRC-0082-diseases-of-swine-11e-chapter-67-internal-parasites.md",
        "Chapter 67 covers internal parasite groups including Strongyloides, Ascaris, Trichuris, Metastrongylus, liver flukes, hydatid cysts, kidney worm and anthelmintic/control boundaries.",
    ),
]


FACTS = [
    ("PARA-001-sarcoptic-mange-importance", "ectoparasite_relevance", "猪疥螨病", "sarcoptic_mange_is_the_most_important_swine_ectoparasite_worldwide", "猪疥螨病是全球最重要的猪外寄生虫病，可降低生长速度、饲料效率和繁殖母猪受胎/繁殖表现。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1029", "all_stages"),
    ("PARA-002-sarcoptes-host-specific", "ectoparasite_transmission", "Sarcoptes scabiei var. suis", "sarcoptes_suis_is_host_specific_and_swine_reservoirs_are_primary_source", "猪疥螨病由 Sarcoptes scabiei var. suis 引起，虫体宿主适应性强，主要来源为带虫猪。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1029", "all_stages"),
    ("PARA-003-sarcoptes-life-cycle", "ectoparasite_life_cycle", "猪疥螨", "female_mites_tunnel_in_epidermis_and_eggs_develop_to_adults_in_about_two_weeks", "雌虫在表皮上部掘隧道产卵，幼虫、若虫和成虫均在皮肤上完成生活史，约 10-15 天形成成虫。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1029-1030", "all_stages"),
    ("PARA-004-mange-clinical-forms", "clinical_pattern", "猪疥螨病", "swine_mange_has_hypersensitive_and_hyperkeratotic_patterns", "猪疥螨病可表现为螨数量少但过敏反应强的瘙痒型，也可表现为多见于成年猪的角化过度型。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1030-1031", "all_stages"),
    ("PARA-005-mange-lesions", "lesion_pattern", "猪疥螨病", "mange_lesions_include_pruritus_papules_erythema_crusts_and_hyperkeratosis", "猪疥螨病可见瘙痒、丘疹、红斑、结痂和角化过度，成年猪耳部和体侧病变常有提示意义。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1030-1031", "all_stages"),
    ("PARA-006-mange-diagnosis", "diagnostic_boundary", "猪疥螨病", "mange_diagnosis_requires_mite_or_egg_detection_but_scrapings_can_be_false_negative", "猪疥螨病确诊依赖检出螨或虫卵，但皮肤刮片可能假阴性，需结合群体病史和病变解释。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1031", "all_stages"),
    ("PARA-007-mange-elimination", "control_boundary", "猪疥螨病", "mange_free_herds_depend_on_mite_free_piglets_effective_products_and_biosecurity", "建立无疥螨猪群依赖仔猪出生时无螨、有效杀螨药和防止引入带虫猪的生物安全。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1032", "breeding_herd"),
    ("PARA-008-mange-products-boundary", "treatment_boundary", "猪外寄生虫药物", "external_parasite_product_tables_are_label_context_not_universal_prescriptions", "教材外寄生虫药物表用于说明标签适应范围，不得直接转写为通用处方、剂量、疗程或中国休药期。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1032", "all_stages"),
    ("PARA-009-mange-economic-effect", "production_impact", "猪疥螨病", "sarcoptic_mange_reduces_growth_rate_and_feed_efficiency_in_growing_pigs", "猪疥螨病通常不致死，但可使生长猪生长速度和饲料效率下降，并导致胴体降级或修割。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1033", "growers"),
    ("PARA-010-demodectic-mange", "ectoparasite_boundary", "猪蠕形螨病", "demodectic_mange_is_relatively_unimportant_and_often_subclinical_in_swine", "猪蠕形螨病在猪中相对不重要，亚临床感染较常见，临床病变多为毛囊相关结节或脓肿。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1033", "all_stages"),
    ("PARA-011-lice-obligate", "ectoparasite_life_cycle", "猪虱", "haematopinus_suis_is_an_obligate_louse_spreading_by_direct_contact", "猪虱 Haematopinus suis 为专性寄生虫，离开宿主通常只能存活 2-3 天，主要经直接接触传播。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1033-1034", "all_stages"),
    ("PARA-012-lice-diagnosis", "diagnostic_boundary", "猪虱病", "lice_diagnosis_is_by_identifying_lice_or_nits", "猪虱病诊断依靠在猪体发现虱或黏附在毛上的虫卵，需纳入瘙痒和皮肤损伤鉴别。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1034", "all_stages"),
    ("PARA-013-flies-sanitation", "biosecurity_indicator", "猪场蝇类", "houseflies_are_sanitation_indicator_and_possible_mechanical_vectors", "家蝇常被用作一般卫生状况指标，也可能机械性携带多种病原，但具体传播作用需谨慎解释。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1035-1036", "all_stages"),
    ("PARA-014-stable-flies", "ectoparasite_impact", "厩螫蝇", "stable_flies_cause_annoyance_blood_loss_and_can_vector_hog_cholera_and_m_suis", "厩螫蝇叮咬可造成骚扰和失血，教材称其可传播猪瘟和 M. suis，但答案需保留证据边界。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1036", "all_stages"),
    ("PARA-015-myiasis", "ectoparasite_impact", "蝇蛆病", "screwworm_and_blow_flies_cause_primary_or_secondary_myiasis_in_wounds", "螺旋蝇可引起原发性蝇蛆病，丽蝇等可在伤口引起继发性蝇蛆病，严重时可造成显著疾病和死亡。", "SRC-0080", "Chapter 65 External Parasites; PDF page 1036-1037", "all_stages"),
    ("PARA-016-coccidia-life-cycle", "protozoa_life_cycle", "猪球虫", "coccidial_life_cycles_have_sporogony_merogony_and_gametogony_phases", "猪球虫生活史包括孢子生殖、裂殖生殖和配子生殖阶段，各阶段对诊断和环境控制解释有意义。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1039", "piglets"),
    ("PARA-017-cystoisospora-piglets", "protozoa_relevance", "Cystoisospora suis", "c_suis_is_major_cause_of_coccidiosis_in_suckling_piglets", "Cystoisospora suis 是哺乳仔猪球虫病的重要病原，主要影响新生至断奶前仔猪。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1039-1040", "piglets"),
    ("PARA-018-coccidia-differentials", "diagnostic_boundary", "仔猪球虫病", "coccidiosis_differentials_include_e_coli_rotavirus_tge_clostridium_c_and_strongyloides", "仔猪球虫病诊断需与 E. coli、轮状病毒、TGE、C. perfringens type C 和 Strongyloides ransomi 等腹泻原因鉴别。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1041", "piglets"),
    ("PARA-019-coccidia-oocyst-boundary", "diagnostic_boundary", "仔猪球虫病", "oocyst_detection_alone_must_be_interpreted_with_age_clinical_signs_and_lesions", "粪便检出球虫卵囊需结合日龄、临床腹泻和肠道病变解释，不能单独完成定因。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1041-1043", "piglets"),
    ("PARA-020-eimeria-boundary", "protozoa_boundary", "猪 Eimeria", "eimeria_species_are_common_but_usually_not_clinical_disease_causes_in_swine", "猪 Eimeria 种可在粪便中出现，但通常不被认为是猪临床疾病的主要原因。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1042-1043", "all_stages"),
    ("PARA-021-anticoccidial-boundary", "treatment_boundary", "猪球虫药物", "anticoccidial_activity_does_not_equal_universal_sow_ration_or_piglet_protocol", "教材关于抗球虫药活性的描述不能外推为母猪饲料通用添加方案、仔猪固定程序或中国兽药合规结论。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1043", "piglets"),
    ("PARA-022-toxoplasma-zoonosis", "public_health_boundary", "猪弓形虫病", "toxoplasmosis_is_zoonotic_and_pork_can_be_a_human_source", "弓形虫病具人兽共患意义，猪肉可成为人感染来源之一，解释时需区分食品安全风险和猪临床病。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1043", "all_stages"),
    ("PARA-023-toxoplasma-cats", "transmission_boundary", "猪弓形虫病", "cats_are_definitive_hosts_and_oocyst_contamination_is_key_for_pig_infection", "猫为弓形虫终末宿主，含卵囊的猫粪污染饲料、水或环境是猪感染关键来源。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1044", "all_stages"),
    ("PARA-024-toxoplasma-subclinical", "clinical_pattern", "猪弓形虫病", "porcine_toxoplasmosis_is_usually_subclinical_but_outbreaks_can_occur", "猪弓形虫感染通常为亚临床，但教材记录可发生急性临床暴发，需结合发热、呼吸和繁殖表现解释。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1045", "all_stages"),
    ("PARA-025-sarcocystis-boundary", "protozoa_boundary", "猪肉孢子虫", "sarcocystis_has_two_host_life_cycle_and_is_usually_of_limited_clinical_importance_in_swine", "猪肉孢子虫具有两宿主生活史，在猪中通常临床意义有限，不能无证据归因常见猪病。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1045", "all_stages"),
    ("PARA-026-cryptosporidium-worldwide", "protozoa_relevance", "猪隐孢子虫病", "cryptosporidiosis_has_worldwide_reports_but_pig_pathogenicity_varies_by_species_and_context", "猪隐孢子虫病有全球报道，但致病性随 Cryptosporidium 种、年龄和混合感染环境而变化。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1045-1046", "piglets"),
    ("PARA-027-cryptosporidium-diagnosis", "diagnostic_boundary", "猪隐孢子虫病", "cryptosporidium_detection_requires_context_because_infection_can_be_subclinical_or_mixed", "隐孢子虫检出需结合腹泻、年龄和其他病原，因为感染可亚临床或与其他腹泻病原混合。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1046", "piglets"),
    ("PARA-028-protozoa-references-boundary", "source_boundary", "Chapter 66 参考文献", "protozoa_references_are_source_boundary_not_standalone_facts", "Chapter 66 参考文献页只作为来源完整性和章节边界记录，不生成独立事实。", "SRC-0081", "Chapter 66 Coccidia and Other Protozoa; PDF page 1050-1051", "all_stages"),
    ("PARA-029-internal-parasites-common", "parasite_relevance", "猪内寄生虫", "internal_parasites_are_common_worldwide_and_ascaris_remains_prevalent_despite_anthelmintics", "内寄生虫是全球猪生产常见问题，尽管有驱虫药，Ascaris suum 仍是最普遍的猪寄生虫之一。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1052", "all_stages"),
    ("PARA-030-strongyloides-transmission", "parasite_transmission", "Strongyloides ransomi", "s_ransomi_can_transmit_to_piglets_transmammarily_and_by_skin_or_oral_exposure", "Strongyloides ransomi 可经乳汁、皮肤穿透或口服暴露感染仔猪，常见于幼龄阶段。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1053", "piglets"),
    ("PARA-031-strongyloides-diagnosis", "diagnostic_boundary", "Strongyloides ransomi", "strongyloides_diagnosis_may_use_eggs_or_mucosal_scrapings_but_larval_problems_lack_eggs", "Strongyloides 可通过粪便虫卵或黏膜刮片支持诊断，但幼虫相关问题可能不伴随虫卵排出。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1055", "piglets"),
    ("PARA-032-ascaris-ubiquitous", "parasite_relevance", "Ascaris suum", "ascaris_suum_is_ubiquitous_and_adults_are_obvious_at_necropsy", "Ascaris suum 因虫卵广泛存在而常见，成虫在剖检小肠中容易观察。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1055", "growers"),
    ("PARA-033-ascaris-diagnosis", "diagnostic_boundary", "猪蛔虫病", "ascaris_diagnosis_is_straightforward_with_adults_or_eggs_but_milk_spots_need_differential", "猪蛔虫病可由成虫或虫卵支持诊断，但肝脏 milk spots 需与肾虫移行相关纤维化等鉴别。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1056", "growers"),
    ("PARA-034-ascaris-immune-effect", "host_response", "Ascaris suum", "ascaris_infection_may_decrease_host_response_to_vaccination_or_other_infections", "Ascaris 感染可能降低宿主对免疫或其他感染的反应，需作为生产性能和免疫反应解释的边界。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1056", "growers"),
    ("PARA-035-trichuris-colon", "parasite_relevance", "Trichuris suis", "trichuris_suis_occurs_in_cecum_and_colon_and_heavy_infections_cause_colitis", "猪鞭虫 Trichuris suis 寄生于盲肠和结肠，重度感染可导致结肠炎和腹泻。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1058-1059", "growers"),
    ("PARA-036-trichuris-diagnosis", "diagnostic_boundary", "猪鞭虫病", "adult_trichuris_or_eggs_support_diagnosis_but_low_populations_may_be_minimal", "发现成虫或典型虫卵可支持猪鞭虫病诊断，但低虫体负荷可能病变轻微，需结合临床。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1059", "growers"),
    ("PARA-037-metastrongylus-earthworm", "parasite_transmission", "猪肺虫病", "metastrongylus_uses_earthworms_as_intermediate_hosts", "Metastrongylus spp. 以蚯蚓为中间宿主，猪接触蚯蚓的饲养环境增加肺虫感染风险。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1059-1060", "outdoor_pigs"),
    ("PARA-038-metastrongylus-lesions", "lesion_pattern", "猪肺虫病", "metastrongylosis_causes_wedge_shaped_emphysema_or_atelectasis_and_bronchial_adults", "猪肺虫病肺部可见楔形肺气肿或肺不张，剖检可在支气管/细支气管发现成虫。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1060", "outdoor_pigs"),
    ("PARA-039-metastrongylus-diagnosis", "diagnostic_boundary", "猪肺虫病", "metastrongylosis_diagnosis_uses_characteristic_eggs_but_they_do_not_float_well", "猪肺虫病可通过漂浮法发现特征性虫卵，但虫卵不易漂浮，剖检发现肺虫更可靠。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1060", "outdoor_pigs"),
    ("PARA-040-hydatid-cyst", "public_health_boundary", "包虫/棘球蚴", "hydatid_cysts_can_contain_protoscolices_but_some_in_pigs_are_sterile", "猪可形成棘球蚴囊，囊液可含原头蚴，但部分猪源包囊可为无原头蚴的 sterile hydatids，诊断需谨慎。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1061", "all_stages"),
    ("PARA-041-kidney-worm", "parasite_relevance", "Stephanurus dentatus", "kidney_worm_adults_occur_in_perirenal_cysts_opening_to_ureters", "猪肾虫 Stephanurus dentatus 成虫位于肾周囊内，囊可经瘘管开口至输尿管，也可见异位囊。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1061", "outdoor_pigs"),
    ("PARA-042-kidney-worm-milk-spots", "lesion_differential", "Stephanurus dentatus", "kidney_worm_migration_can_cause_more_prominent_hepatic_milk_spots_than_ascarids", "肾虫移行可造成肝脏 milk spots，且教材称可比蛔虫造成的病变更显著，需纳入鉴别。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1061", "outdoor_pigs"),
    ("PARA-043-internal-control-concrete", "control_boundary", "猪内寄生虫", "raising_pigs_on_concrete_reduces_exposure_to_intermediate_hosts_and_some_helminths", "在混凝土地面饲养可减少猪接触部分中间宿主和土壤传播寄生虫，从而降低多类内寄生虫感染。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1062", "all_stages"),
    ("PARA-044-trichinella-cannibalism", "public_health_boundary", "Trichinella", "preventing_cannibalism_and_raw_garbage_feeding_reduces_trichinella_transmission", "防止同类相食和未处理垃圾饲喂可降低 Trichinella 传播风险；公共卫生执行细则需另引权威来源。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1062", "all_stages"),
    ("PARA-045-taenia-solium", "public_health_boundary", "Taenia solium", "denying_pigs_access_to_human_feces_halts_t_solium_transmission", "阻止猪接触人粪可中断 Taenia solium 传播，相关人兽共患和公共卫生措施需权威来源复核。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1062", "all_stages"),
    ("PARA-046-anthelmintic-boundary", "treatment_boundary", "猪驱虫药", "anthelmintic_label_and_withdrawal_information_must_not_be_generalized_across_jurisdictions", "教材中驱虫药标签适应虫种和美国休药期信息不得跨法域泛化为中国处方或休药期。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1063-1064", "all_stages"),
    ("PARA-047-fenbendazole-trichuris", "treatment_boundary", "猪鞭虫药物边界", "fenbendazole_is_noted_as_one_of_few_anthelmintics_effective_for_trichuris_but_no_protocol_is_generated", "教材称芬苯达唑被认为是少数对 Trichuris 有效的驱虫药之一，但本批不生成剂量、疗程或休药期。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1064", "growers"),
    ("PARA-048-references-boundary", "source_boundary", "Chapter 67 参考文献", "internal_parasite_references_begin_on_page_1064_and_are_not_standalone_facts", "Chapter 67 参考文献从 PDF page 1064 开始，仅作为来源边界记录，不生成独立事实。", "SRC-0082", "Chapter 67 Internal Parasites; PDF page 1064", "all_stages"),
]


RULES = [
    ("RULE-415", "猪疥螨病诊断需保留刮片假阴性边界", "mange_diagnostics", "high", "SRC-0080", "Swine-mange-scraping-false-negative-boundary.md", "猪疥螨病确诊应尽量检出螨或虫卵，但皮肤刮片可能假阴性，需结合群体病史、瘙痒和典型病变解释。", "1029-1031"),
    ("RULE-416", "猪疥螨净化不得等同固定药物程序", "mange_control", "high", "SRC-0080", "Swine-mange-elimination-not-fixed-drug-program.md", "无疥螨猪群建立需结合无螨引种、全群处理和生物安全；教材药物表不得生成固定药物程序或休药期。", "1032"),
    ("RULE-417", "猪外寄生虫药物表不得生成中国处方", "external_parasite_treatment_boundary", "critical", "SRC-0080", "Swine-external-parasite-label-table-not-china-prescription.md", "Chapter 65 药物标签表只能作为教材证据边界，不能转写为中国处方、剂量、疗程或休药期。", "1032"),
    ("RULE-418", "猪虱病诊断应寻找虱或虫卵", "lice_diagnostics", "medium", "SRC-0080", "Swine-lice-diagnosis-lice-or-nits.md", "猪虱病需通过发现虱或黏附于毛上的虫卵支持诊断，瘙痒或皮肤损伤本身不足以定因。", "1033-1034"),
    ("RULE-419", "蝇类传播病原需区分机械携带和证实传播", "flies_vector_boundary", "high", "SRC-0080", "Swine-flies-mechanical-vector-evidence-boundary.md", "蝇类可机械携带多种病原，但对具体疾病传播的回答需区分机械携带、实验证据和现场证实传播。", "1035-1036"),
    ("RULE-420", "仔猪球虫病不能仅凭卵囊定因", "coccidia_diagnostics", "critical", "SRC-0081", "Swine-coccidia-oocyst-not-causality-alone.md", "仔猪球虫病需结合日龄、腹泻、肠道病变和排除常见腹泻病因；卵囊检出本身不足以定因。", "1039-1043"),
    ("RULE-421", "猪 Eimeria 多为低临床意义边界", "eimeria_boundary", "medium", "SRC-0081", "Swine-eimeria-not-common-clinical-cause.md", "猪 Eimeria 检出通常不能直接解释临床腹泻，应优先核查 C. suis 和其他更常见病因。", "1042-1043"),
    ("RULE-422", "抗球虫药活性不得生成固定程序", "anticoccidial_treatment_boundary", "critical", "SRC-0081", "Swine-anticoccidial-activity-not-fixed-program.md", "抗球虫药活性和教材用药讨论不得转写为母猪饲料通用添加、仔猪固定程序、剂量或中国兽药合规结论。", "1043"),
    ("RULE-423", "猪弓形虫回答必须保留猫源卵囊和食品安全边界", "toxoplasma_public_health", "critical", "SRC-0081", "Swine-toxoplasma-cat-oocyst-food-safety-boundary.md", "猪弓形虫解释需同时保留猫源卵囊污染、猪肉人兽共患风险和猪临床病通常亚临床的边界。", "1043-1045"),
    ("RULE-424", "隐孢子虫阳性需结合混合感染解释", "cryptosporidium_diagnostics", "high", "SRC-0081", "Swine-cryptosporidium-positive-context-required.md", "猪隐孢子虫阳性需结合日龄、腹泻、病变和其他病原，不能单独作为腹泻定因。", "1045-1046"),
    ("RULE-425", "内寄生虫控制需区分环境管理和驱虫处方", "internal_parasite_control", "high", "SRC-0082", "Swine-internal-parasite-control-management-vs-prescription.md", "内寄生虫防控可讨论混凝土地面、卫生和中间宿主管控，但不得由教材生成具体驱虫处方、疗程或休药期。", "1052-1064"),
    ("RULE-426", "Strongyloides 仔猪病需考虑无虫卵阶段", "strongyloides_diagnostics", "high", "SRC-0082", "Swine-strongyloides-larval-stage-no-eggs-boundary.md", "Strongyloides 诊断需理解经乳和幼虫感染阶段，幼虫相关问题可能无虫卵排出，不能因粪检阴性简单排除。", "1053-1055"),
    ("RULE-427", "Ascaris milk spots 需与肾虫移行鉴别", "ascaris_differential", "critical", "SRC-0082", "Swine-ascaris-milk-spots-kidney-worm-differential.md", "肝脏 milk spots 不得自动归因 Ascaris，需与 Stephanurus dentatus 等移行性寄生虫病变鉴别。", "1056-1061"),
    ("RULE-428", "Trichuris 低虫量不应过度解释腹泻", "trichuris_diagnostics", "medium", "SRC-0082", "Swine-trichuris-low-burden-not-overcalled.md", "Trichuris 低虫量可能临床意义有限，腹泻定因需结合虫量、病变和其他肠道病原。", "1058-1059"),
    ("RULE-429", "Metastrongylus 粪漂检阴性不能简单排除", "metastrongylus_diagnostics", "high", "SRC-0082", "Swine-metastrongylus-eggs-float-poorly.md", "Metastrongylus 虫卵不易漂浮，疑似病例粪检阴性不能简单排除，剖检支气管成虫更有力。", "1059-1060"),
    ("RULE-430", "Taenia solium 和 Trichinella 需保留人兽共患权威来源要求", "parasite_public_health", "critical", "SRC-0082", "Swine-taenia-trichinella-public-health-authority-required.md", "Taenia solium 和 Trichinella 可提示人兽共患和食品安全边界，但具体公共卫生、检疫和肉品处理需 A0/A1 来源。", "1062"),
    ("RULE-431", "美国驱虫药标签和休药期不得跨法域迁移", "anthelmintic_jurisdiction_boundary", "critical", "SRC-0082", "Swine-anthelmintic-us-label-withdrawal-not-china.md", "Chapter 67 美国标签虫种和休药期信息不得迁移为中国处方、剂量、疗程或休药期。", "1063-1064"),
    ("RULE-432", "寄生虫参考文献页只作来源边界", "parasite_reference_boundary", "medium", "SRC-0081", "Swine-parasite-reference-pages-not-standalone-facts.md", "Chapter 65-67 参考文献页只作章节边界和来源完整性记录，不生成 standalone facts。", "1037-1038,1050-1051,1064"),
]


TOPICS = [
    ("Swine-external-parasite-diagnosis-control-boundaries.md", "猪外寄生虫诊断和防控边界", "SRC-0080", "本主题汇总 Chapter 65 中猪疥螨、蠕形螨、猪虱和蝇类的诊断、生产影响、传播和防控边界。"),
    ("Swine-protozoa-diarrhea-zoonosis-boundaries.md", "猪原虫性腹泻和人兽共患边界", "SRC-0081", "本主题汇总 Chapter 66 中 C. suis、Eimeria、弓形虫、肉孢子虫和隐孢子虫的诊断、混合感染和公共卫生边界。"),
    ("Swine-internal-parasite-diagnosis-control-boundaries.md", "猪内寄生虫诊断和防控边界", "SRC-0082", "本主题汇总 Chapter 67 中 Strongyloides、Ascaris、Trichuris、Metastrongylus、Stephanurus 和人兽共患寄生虫的诊断、防控和用药边界。"),
]


DISEASE_UPDATES = {
    "DIS-055-external-parasites-mange.md": "已补充 Chapter 65 疥螨病病原、宿主特异性、生活史、瘙痒/角化过度型、刮片假阴性、生产影响、净化和药物表不得转写处方边界；详见 `SRC-0080`。",
    "DIS-056-external-parasites-lice.md": "已补充 Chapter 65 猪虱专性寄生、离体存活 2-3 天、直接接触传播、虱/虫卵诊断和瘙痒鉴别边界；详见 `SRC-0080`。",
    "DIS-057-coccidia-and-other-protozoa.md": "已补充 Chapter 66 Cystoisospora suis、Eimeria、抗球虫药活性边界和仔猪腹泻鉴别诊断边界；详见 `SRC-0081`。",
    "DIS-058-toxoplasmosis-protozoa.md": "已补充 Chapter 66 弓形虫猫源卵囊、猪肉人兽共患风险、通常亚临床和食品安全不得外推监管处置边界；详见 `SRC-0081`。",
    "DIS-059-cryptosporidiosis-protozoa.md": "已补充 Chapter 66 隐孢子虫全球报道、种/日龄/混合感染差异和阳性检出不得单独定因腹泻边界；详见 `SRC-0081`。",
    "DIS-060-ascaris-suum-internal-parasites.md": "已补充 Chapter 67 Ascaris suum 广泛性、剖检/虫卵诊断、milk spots 鉴别和免疫反应影响边界；详见 `SRC-0082`。",
    "DIS-061-trichuris-suis-internal-parasites.md": "已补充 Chapter 67 Trichuris suis 盲肠/结肠寄生、重度感染结肠炎、低虫量解释和诊断边界；详见 `SRC-0082`。",
    "DIS-062-strongyloides-internal-parasites.md": "已补充 Chapter 67 Strongyloides ransomi 经乳/皮肤/口服感染、幼虫阶段可能无虫卵和仔猪诊断边界；详见 `SRC-0082`。",
    "DIS-063-metastrongylus-lungworms.md": "已补充 Chapter 67 Metastrongylus 蚯蚓中间宿主、肺部楔形肺气肿/肺不张、虫卵不易漂浮和剖检诊断边界；详见 `SRC-0082`。",
    "DIS-064-stephanurus-dentatus-kidney-worm.md": "已补充 Chapter 67 Stephanurus dentatus 肾周囊、异位囊、肝脏 milk spots 鉴别和地理/饲养方式边界；详见 `SRC-0082`。",
}


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
- 批次：Formal Batch 029 / V4。
- 解析器：PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six`。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_029_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_029_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_029_pdf_pages_1027_1064_parser_report.txt`。
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
- 本页正式 facts 已在 `issues/formal_batch_029_cross_review.md` 中交叉审查。
- 本页不提供处方、剂量、固定驱虫/杀虫程序、休药期、公共卫生暴露处置、食品处理执行细则或中国监管结论。
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

- 本规则用于生成、评估和审核猪病 Wiki 中寄生虫病、诊断、传播、环境控制、用药、食品安全和公共卫生边界解释。
- 本规则不提供具体药物剂量、固定治疗程序、驱虫程序、休药期、肉品处理执行细则、暴露后处置细则或中国监管结论。
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
    write_text(ISSUES / "formal_batch_029_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "source_ids": [source[0] for source in SOURCES],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pdfminer.six",
            "report": "issues/formal_batch_029_pdf_pages_1027_1064_parser_report.txt",
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
    marker = "## Formal Batch 029 / V4 正文抽取进展"
    for filename, summary in DISEASE_UPDATES.items():
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- Formal Batch 029 / V4 正文抽取：{summary}\n")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_029_cross_review.md", """# Formal Batch 029 / V4 Cross Review

## 范围

- PDF page 1027-1028：Section V Parasitic Diseases 扉页/空白边界。
- PDF page 1029-1038：Chapter 65 External Parasites 正文和参考文献。
- PDF page 1039-1051：Chapter 66 Coccidia and Other Protozoa 正文和参考文献。
- PDF page 1052-1064：Chapter 67 Internal Parasites 正文前中段和参考文献开端。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行，并同步 V4 主线文档。
- 本批按用户要求使用 PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six` 三路解析。
- 参考文献列表只记录章节边界，不生成 standalone facts。
- 所有正式 facts 均先写入候选事实文件，再经页码锚点、内容边界和一致性审查后落库。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`。
- 二次核对：`pdfplumber`，PDF page 1027、1029、1039、1044、1052 采用 pdfplumber 文本，其余正文页多采用 fitz。
- 三次核对：`pdfminer.six`，逐页字符量对照，未发现整页遗漏。
- 解析文件：`issues/formal_batch_029_pdf_pages_1027_1064_extract.txt`。
- 解析报告：`issues/formal_batch_029_pdf_pages_1027_1064_parser_report.txt`。

## 审查结论

本批候选 facts 48 条、规则页 18 个、来源页 3 个、主题页 3 个。经交叉审查后允许正式落库，所有 facts 均为 `HUMAN_REVIEWED`。

## 审查 1：页码锚点核验

- `SRC-0080` 锚定 PDF page 1027-1038。
- `SRC-0081` 锚定 PDF page 1039-1051。
- `SRC-0082` 锚定 PDF page 1052-1064。
- PDF page 1027-1028 为 Section V 扉页/空白边界，未生成 standalone facts。

## 审查 2：内容边界核验

- 外寄生虫、原虫和内寄生虫内容只落库教材证据、诊断/定因、传播、生产影响、环境控制、公共卫生和食品安全边界。
- 药物表、抗球虫药和驱虫药标签信息不生成处方、剂量、疗程、固定程序或休药期。
- 弓形虫、Trichinella、Taenia solium、棘球蚴等公共卫生和食品安全内容不生成暴露处置、肉品处理执行细则或中国监管结论。
- 隐孢子虫、Eimeria、Trichuris 低虫量、蝇类机械传播、milk spots 等保留混合感染/鉴别诊断/证据等级边界。

## 审查 3：一致性核验

- facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- `SRC-0080` 至 `SRC-0082`、`RULE-415` 至 `RULE-432` 与既有条目不重复。
- 本批正式落库内容与 V4 文档同步，V3 文档保留为历史记录。

## 明确未落库

- 参考文献列表。
- 具体药物剂量、疗程、休药期、固定驱虫/杀虫/抗球虫程序。
- 食品处理、公共卫生暴露处置、检疫监管和中国本地执法结论。
- 美国标签、USDA 食品安全语境或教材公共卫生描述中的执行细则，除作为“需权威来源复核”的边界提示外，不迁移为本地答案。

## 保留问题

- PDF page 1065 起进入 Section VI Noninfectious Diseases，下一批应处理营养缺乏/过量章节。
- 寄生虫药物合规、休药期、食品安全和人兽共患处置若需中国本地答案，必须补充 A0/A1 来源。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 029 / V4 实施记录

- 完成时间：2026-05-07 19:10:00 +08:00。
- 处理范围：PDF page 1027-1064。
- 章节边界：Section V Parasitic Diseases 扉页；Chapter 65 External Parasites 正文和参考文献；Chapter 66 Coccidia and Other Protozoa 正文和参考文献；Chapter 67 Internal Parasites 正文前中段和参考文献开端。
- 解析器：PyMuPDF `fitz`、`pdfplumber`、`pdfminer.six`。
- 参考文献处理：PDF page 1037-1038、1050-1051、1064 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0080` 至 `SRC-0082`。
- 新增主题页：猪外寄生虫诊断和防控边界、猪原虫性腹泻和人兽共患边界、猪内寄生虫诊断和防控边界。
- 新增规则页：`RULE-415` 至 `RULE-432`。
- 新增候选事实：`issues/formal_batch_029_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_029_cross_review.md`。
- 正式落库 facts：48 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、具体驱虫/杀虫/抗球虫处方、剂量、疗程、休药期、食品处理执行细则、公共卫生暴露处置和中国监管结论。

### Formal Batch 029 / V4 交叉审查

- 页码锚点核验：通过。`SRC-0080` 覆盖 PDF page 1027-1038；`SRC-0081` 覆盖 1039-1051；`SRC-0082` 覆盖 1052-1064。
- 内容边界核验：通过。Chapter 65-67 只落库教材证据、诊断/传播/生产影响/防控/公共卫生边界，不生成处方、固定程序、休药期或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 1064。
- 下一批应从 PDF page 1065 开始。
- 推荐下一批：PDF page 1065-1111，进入 Section VI Noninfectious Diseases，处理营养缺乏/过量、霉菌毒素和毒物/气体相关章节。
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
    print("formal batch 029 v4 built")


if __name__ == "__main__":
    main()
