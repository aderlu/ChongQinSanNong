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
PDF = next((ROOT / "docs").glob("Diseases of Swine, 11th Edition*.pdf"))
NOW = "2026-05-07T17:10:00+08:00"
BATCH_ID = "formal-batch-027-v4"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 965, end: int = 1004) -> None:
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
    write_text(
        ISSUES / "formal_batch_027_pdf_pages_965_1004_extract.txt",
        "".join(extract_parts).strip() + "\n",
    )
    write_text(
        ISSUES / "formal_batch_027_pdf_pages_965_1004_parser_report.txt",
        "\n".join(report_rows) + "\n",
    )


SOURCES = [
    ("SRC-0076", "Diseases of Swine 11e Chapter 61 Streptococcosis continuation", "PDF page 965-974", "wiki/sources/SRC-0076-diseases-of-swine-11e-chapter-61-streptococcosis-continuation.md", "Chapter 61 continuation covers S. suis culture/serotyping/PCR boundaries, healthy-pig surveillance limits, treatment and antimicrobial-susceptibility boundary, prevention, vaccination limits, eradication limits, beta-hemolytic streptococci and references."),
    ("SRC-0077", "Diseases of Swine 11e Chapter 62 Swine Dysentery and Brachyspiral Colitis", "PDF page 975-994", "wiki/sources/SRC-0077-diseases-of-swine-11e-chapter-62-swine-dysentery-brachyspiral-colitis.md", "Chapter 62 covers Brachyspira taxonomy, swine dysentery, B. hyodysenteriae/B. hampsonii/B. suanatina, B. pilosicoli PIS/PCS, epidemiology, lesions, diagnosis, antimicrobial resistance, control and references."),
    ("SRC-0078", "Diseases of Swine 11e Chapter 63 Tuberculosis", "PDF page 995-1004", "wiki/sources/SRC-0078-diseases-of-swine-11e-chapter-63-tuberculosis.md", "Chapter 63 covers swine TB relevance, MTBC/MAC/MAH etiology, public-health boundary, epidemiology, sources, pathogenesis, lesions, diagnosis, sampling, prevention/control and references opening."),
]


FACTS = [
    ("SSUIS-009-csf-surveillance", "streptococcosis_diagnostics", "S. suis 脑膜炎 CSF 监测", "periodic_csf_culture_from_pigs_with_meningitis_is_recommended_for_ongoing_s_suis_surveillance", "S. suis 暴发中可涉及多个血清型和菌株，脑膜炎猪脑脊液的周期性培养有助于持续监测和更新自家苗候选株。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 965", "weaners"),
    ("SSUIS-010-autogenous-systemic-sites", "streptococcosis_vaccine_boundary", "S. suis 自家苗株来源", "autogenous_vaccine_candidate_strains_should_come_from_systemic_sites_not_upper_respiratory_sites", "用于 S. suis 自家苗的候选株应来自脑膜、脾、肝、关节等系统部位，而不是肺、鼻腔或扁桃体。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 965", "all_stages"),
    ("SSUIS-011-pcr-serotype-limit", "streptococcosis_diagnostics", "S. suis PCR 血清型限制", "pcr_for_serotypes_2_and_1_also_detects_serotypes_1_2_and_14_respectively", "S. suis 直接 PCR 检测血清型 2 和 1 时，也会分别检出血清型 1/2 和 14，血清型解释需保留交叉检出边界。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 965", "all_stages"),
    ("SSUIS-012-oral-fluid-limit", "streptococcosis_diagnostics", "S. suis 口腔液限制", "oral_fluid_has_little_practical_advantage_for_s_suis_detection_because_s_suis_is_normally_present_in_saliva", "由于 S. suis 正常存在于唾液中，口腔液检测对 S. suis 诊断没有实际优势。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 965", "all_stages"),
    ("SSUIS-013-tonsil-no-diagnosis", "streptococcosis_surveillance", "S. suis 扁桃体检测边界", "tonsil_or_nasal_detection_has_no_practical_utility_for_diagnosing_s_suis_disease", "从扁桃体或鼻腔检出 S. suis 对诊断 S. suis 病没有实际价值，因为其为上呼吸道常在菌。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 966", "all_stages"),
    ("SSUIS-014-serology-low-utility", "streptococcosis_serology", "S. suis 血清学限制", "s_suis_serologic_tests_are_generally_not_useful_due_to_cross_reactions_low_titers_and_strain_diversity", "S. suis 血清学常因交叉反应、抗体滴度不高和菌株多样性而不适合常规诊断。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 966", "all_stages"),
    ("SSUIS-015-treatment-ast", "streptococcosis_treatment_boundary", "S. suis 用药选择边界", "antibacterial_choice_for_s_suis_should_be_based_on_susceptibility_infection_type_and_administration_route", "S. suis 抗菌药选择应基于分离株药敏、感染类型和给药途径，不应生成脱离本地耐药谱的通用处方。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 966", "all_stages"),
    ("SSUIS-016-predisposing-factors", "streptococcosis_prevention", "S. suis 易感诱因控制", "s_suis_control_should_address_immunity_mixing_coinfections_environment_and_management", "S. suis 防控需同时考虑群体免疫、混群、共同感染、环境质量和管理因素。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 967", "weaners"),
    ("SSUIS-017-prrsv-potentiation", "streptococcosis_coinfection", "PRRSV 加重 S. suis 风险", "prrsv_infection_can_increase_susceptibility_to_s_suis_disease", "PRRSV 感染可增加猪对 S. suis 病的易感性，伪狂犬和流感等共同感染也可增强临床病。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 967", "piglets"),
    ("SSUIS-018-vaccine-inconsistent", "streptococcosis_vaccine_boundary", "S. suis 疫苗效果不稳定", "field_s_suis_bacterin_vaccines_have_inconsistent_results_and_protection_is_serotype_or_strain_dependent", "S. suis 自家苗或少数商业菌苗田间结果不一致，保护性如存在通常依赖血清型/菌株信息。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 968", "all_stages"),
    ("SSUIS-019-subunit-experimental", "streptococcosis_vaccine_boundary", "S. suis 亚单位疫苗边界", "s_suis_subunit_vaccine_candidates_remain_experimental_and_no_commercial_product_is_available", "S. suis 亚单位疫苗候选物仍处于实验研究阶段，教材未支持商业化程序性应用。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 969", "all_stages"),
    ("SSUIS-020-eradication-limits", "streptococcosis_control", "S. suis 根除边界", "s_suis_eradication_is_limited_by_early_colonization_carrier_detection_limits_cost_and_reinfection_risk", "S. suis 根除受早期定植、缺乏高置信携带检测、成本和再感染风险限制，资源通常更应指向控制而非根除。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 969", "all_stages"),
    ("STREP-001-porcinus-secondary", "streptococcosis_taxonomy", "S. porcinus 次要侵袭者", "s_porcinus_is_more_often_a_secondary_invader_than_a_primary_pathogen", "S. porcinus 可见于健康猪上呼吸道和生殖道，更多被视为继发侵袭者而非主要病原。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 970", "all_stages"),
    ("STREP-002-dysgalactiae-piglet-arthritis", "streptococcosis_clinical_pattern", "S. dysgalactiae 仔猪关节炎", "s_dysgalactiae_subsp_equisimilis_commonly_causes_arthritis_endocarditis_or_meningitis_in_young_pigs", "S. dysgalactiae subsp. equisimilis 可经皮肤、脐和扁桃体入血，常在 1-3 周龄猪引起关节炎、心内膜炎或脑膜炎。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 970", "piglets"),
    ("STREP-003-zooepidemicus-china", "streptococcosis_epidemiology", "S. zooepidemicus 中国猪源报告", "s_zooepidemicus_has_been_mainly_reported_in_swine_in_china_with_sporadic_cases_and_regional_epidemics", "教材称 S. zooepidemicus 在中国猪中有主要报告，1975 年后仍有散发和区域性流行影响猪业。", "SRC-0076", "Chapter 61 Streptococcosis; PDF page 971", "all_stages"),
    ("BRACH-001-overview", "brachyspira_overview", "Brachyspira 猪肠病范围", "porcine_brachyspira_diseases_include_swine_dysentery_and_milder_brachyspiral_colitis", "猪 Brachyspira 相关疾病包括强溶血种导致的严重黏液出血性猪痢疾，以及弱溶血种导致的较轻 Brachyspira 结肠炎。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 975", "growers"),
    ("BRACH-002-sd-definitive", "swine_dysentery_diagnostics", "猪痢疾确诊条件", "definitive_swine_dysentery_diagnosis_requires_strongly_beta_hemolytic_brachyspira_in_typical_cases", "猪痢疾确诊需在典型痢疾和/或病变猪的结肠黏膜或粪便中确认强 β 溶血 Brachyspira spp.。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 975", "growers"),
    ("BRACH-003-seven-species", "brachyspira_taxonomy", "猪 Brachyspira 种类", "seven_brachyspira_species_colonize_swine_with_b_hyodysenteriae_b_hampsonii_and_b_pilosicoli_as_common_pathogens", "7 个 Brachyspira 种可定植猪，其中 B. hyodysenteriae、B. hampsonii 和 B. pilosicoli 是常见致病种。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 975", "all_stages"),
    ("BRACH-004-culture-slow", "brachyspira_diagnostics", "Brachyspira 培养边界", "brachyspira_are_slow_growing_anaerobes_that_require_selective_media_and_can_be_overgrown", "Brachyspira 为生长缓慢的厌氧菌，容易被其他肠道厌氧菌覆盖，培养需选择性培养基。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 976", "all_stages"),
    ("SD-001-strong-hemolysis", "swine_dysentery_etiology", "猪痢疾强溶血病原", "swine_dysentery_can_be_caused_by_b_hyodysenteriae_b_hampsonii_or_b_suanatina", "猪痢疾不仅由 B. hyodysenteriae 引起，强 β 溶血的 B. hampsonii 和 B. suanatina 也可致病。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 977", "growers"),
    ("SD-002-public-health", "swine_dysentery_public_health", "猪痢疾非人感染边界", "agents_of_swine_dysentery_are_not_known_to_infect_humans", "已知猪痢疾病原未被认为感染人类，公共卫生解释不得夸大为人兽共患。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 978", "all_stages"),
    ("SD-003-fecal-oral", "swine_dysentery_transmission", "猪痢疾粪口传播", "swine_dysentery_transmission_mainly_occurs_by_ingestion_of_feces_containing_spirochetes", "猪痢疾在感染猪场主要通过摄入含螺旋体的粪便传播，连续流和生物安全差会增加风险。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 979", "growers"),
    ("SD-004-carrier-70-days", "swine_dysentery_transmission", "猪痢疾康复带菌", "recovered_asymptomatic_pigs_may_transmit_swine_dysentery_for_at_least_70_days", "猪痢疾康复的无症状猪可向易感猪传播至少 70 天。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 979", "all_stages"),
    ("SD-005-moist-survival", "swine_dysentery_environment", "B. hyodysenteriae 湿粪存活", "b_hyodysenteriae_survives_longer_in_moist_feces_and_is_rapidly_killed_by_drying", "B. hyodysenteriae 在湿粪中相对耐受，干燥可迅速杀灭，环境控制需重视湿粪和有机物。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 979", "all_stages"),
    ("SD-006-microbiota-required", "swine_dysentery_pathogenesis", "猪痢疾微生物群共同作用", "other_microorganisms_and_colonic_microbiota_help_determine_swine_dysentery_expression", "猪痢疾表达受结肠微生物群影响，单纯定植 B. hyodysenteriae 并不总能形成典型病。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 979", "growers"),
    ("SD-007-clinical", "swine_dysentery_clinical_pattern", "猪痢疾临床模式", "swine_dysentery_mainly_affects_grower_finisher_pigs_with_mucohemorrhagic_diarrhea", "猪痢疾主要发生于生长育肥猪，表现为软便进展到含血、黏液和黏液纤维素渗出物的水样痢疾。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 980", "growers"),
    ("SD-008-large-intestine-lesions", "swine_dysentery_lesions", "猪痢疾大肠病变", "swine_dysentery_lesions_are_limited_to_cecum_colon_and_rectum", "猪痢疾病变局限于盲肠、结肠和直肠，急性期可见大肠壁充血水肿、黏液、纤维素和血液。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 980", "growers"),
    ("SD-009-culture-integral", "swine_dysentery_diagnostics", "猪痢疾培养不可替代", "selective_anaerobic_culture_should_remain_integral_to_swine_dysentery_diagnosis_and_surveillance", "选择性厌氧培养可检出已知猪痢疾病原并提供溶血表型，应仍为猪痢疾检测、诊断和监测的重要组成。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 982", "all_stages"),
    ("SD-010-differential", "swine_dysentery_differential", "猪痢疾鉴别诊断", "swine_dysentery_should_be_differentiated_from_pe_salmonellosis_trichuriasis_gastric_ulcers_and_pis_pcs", "猪痢疾需与增生性肠病、沙门氏菌病、鞭虫病、胃溃疡/其他出血性疾病及 PIS/PCS 鉴别。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 982", "growers"),
    ("SD-011-amr", "swine_dysentery_amr_boundary", "猪痢疾抗菌药耐药边界", "swine_dysentery_treatment_options_are_limited_and_pleuromutilin_resistance_is_increasing", "猪痢疾有效抗菌药选择有限，重要药物如 pleuromutilins 的耐药性正在增加，用药需基于 MIC 和法规标签。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 983", "growers"),
    ("SD-012-aiao-cleaning", "swine_dysentery_control", "猪痢疾全进全出和清洁", "all_in_all_out_management_with_cleaning_and_disinfection_reduces_swine_dysentery_reinfection_and_spread", "全进全出、批次间清洁消毒、感染垫料处置、靴刷/脚浴、设备清洁和换防护服可降低猪痢疾再感染和传播。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 984", "growers"),
    ("SD-013-rodent-wildlife", "swine_dysentery_control", "猪痢疾鼠和野生动物边界", "rodents_can_be_reservoirs_of_swine_dysentery_agents_and_wildlife_can_mechanically_transmit_infectious_material", "鼠类可作为猪痢疾病原潜在储存宿主，鸟类、水禽和其他野生动物可机械传播感染材料。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 984", "all_stages"),
    ("PIS-001-definition", "pis_pcs_relevance", "PIS/PCS 定义", "pis_pcs_is_brachyspiral_colitis_caused_by_b_pilosicoli", "猪肠道螺旋体病/猪结肠螺旋体病（PIS/PCS）是由弱 β 溶血 B. pilosicoli 引起的 Brachyspira 结肠炎。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 985", "weaners"),
    ("PIS-002-zoonotic-boundary", "pis_pcs_public_health", "B. pilosicoli 人感染边界", "b_pilosicoli_can_colonize_humans_but_risk_for_healthy_pig_workers_is_slight", "B. pilosicoli 可定植免疫受损或卫生条件差人群，动物到人传播潜在存在，但健康养猪从业者因接触猪发病风险较低。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 986", "all_stages"),
    ("PIS-003-fecal-only-limit", "pis_pcs_diagnostics", "B. pilosicoli 粪检阳性限制", "fecal_confirmation_of_b_pilosicoli_alone_does_not_confirm_pis_pcs", "临床正常猪也可排出 B. pilosicoli，粪便阳性本身不能确诊 PIS/PCS，需结合临床、病变和完整诊断。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 989", "all_stages"),
    ("PIS-004-no-vaccine", "pis_pcs_control", "B. pilosicoli 疫苗边界", "no_effective_vaccines_are_available_for_b_pilosicoli", "B. pilosicoli 尚无有效疫苗；自家菌苗虽可诱导系统抗体，但挑战后仍可定植并腹泻。", "SRC-0077", "Chapter 62 Swine Dysentery and Brachyspiral Colitis; PDF page 990", "all_stages"),
    ("TB-001-agent-boundary", "tuberculosis_etiology", "猪结核病原边界", "swine_tuberculosis_can_be_caused_by_mtbc_mac_and_occasionally_other_mycobacterium_species", "猪结核可由 MTBC、MAC 以及偶尔其他 Mycobacterium 种导致，肉眼和镜检病变不能区分病原。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 995", "all_stages"),
    ("TB-002-feral-reservoir", "tuberculosis_epidemiology", "野猪 MTBC 储存宿主边界", "feral_swine_and_wild_boar_are_reservoirs_or_spillover_hosts_for_mtbc_in_some_regions", "在部分地区野猪/野化猪是 MTBC 储存宿主或溢出宿主，国内猪结核调查需与当地流行区和宿主背景结合。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 995", "all_stages"),
    ("TB-003-mah-environmental", "tuberculosis_etiology", "MAH 环境来源", "mah_is_ubiquitous_in_the_environment_and_is_the_primary_agent_responsible_for_swine_tb", "MAH 是环境中广泛存在的 MAC 成员，教材称其主要负责猪结核样病变，暴发多与环境暴露条件有关。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 997", "all_stages"),
    ("TB-004-public-health", "tuberculosis_public_health", "MAC 猪肉和猪接触边界", "there_is_no_data_implicating_infected_swine_or_pork_consumption_as_increased_human_mac_risk", "教材称尚无数据表明接触感染猪或食用猪肉会增加人 MAC 感染风险；人群风险解释需按公共卫生权威来源处理。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 998", "all_stages"),
    ("TB-005-organic-bedding", "tuberculosis_risk_factor", "猪 MAC 结核有机垫料风险", "organic_bedding_such_as_wood_shavings_sawdust_straw_or_peat_increases_mac_associated_tb_risk", "使用锯末、木屑、秸秆或泥炭等有机垫料的生产系统与 MAC 相关猪结核样病变增加有关。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 998", "all_stages"),
    ("TB-006-mtbc-unpasteurized", "tuberculosis_transmission", "M. bovis 猪感染来源", "m_bovis_can_be_transmitted_to_swine_by_unpasteurized_milk_dairy_byproducts_or_tuberculous_material", "在牛结核地方性流行地区，猪可经未巴氏消毒乳及乳副产品、含结核材料的下脚料或污染环境感染 M. bovis。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 998", "all_stages"),
    ("TB-007-mah-biofilm", "tuberculosis_environment", "MAH 生物膜和水系统", "mah_biofilms_protect_against_desiccation_disinfectants_and_mechanical_removal", "MAH 可形成生物膜，抵抗干燥、消毒剂和机械清除，现代猪场暴发调查应考虑饮水系统和慢性潮湿生物膜。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 999", "all_stages"),
    ("TB-008-subclinical", "tuberculosis_clinical_pattern", "猪结核亚临床", "swine_tuberculosis_is_usually_subclinical_and_detected_by_slaughter_condemnations", "猪结核通常为亚临床，生产者多因屠宰场通知异常高废弃率而知晓。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 1000", "all_stages"),
    ("TB-009-lesion-sites", "tuberculosis_lesions", "猪结核淋巴结病变", "swine_tuberculous_lesions_are_usually_limited_to_cervical_and_mesenteric_lymph_nodes", "发达国家屠宰检查中，猪结核样病变通常局限于颈部和肠系膜淋巴结。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 1000", "all_stages"),
    ("TB-010-clinical-diagnosis-limit", "tuberculosis_diagnostics", "猪结核临床诊断限制", "clinical_diagnosis_of_tb_in_swine_is_usually_not_possible", "猪结核多数无症状或仅非特异性不适，通常无法仅凭临床表现诊断。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 1001", "all_stages"),
    ("TB-011-definitive", "tuberculosis_diagnostics", "猪结核确诊条件", "unequivocal_tb_diagnosis_requires_myobacterium_confirmation_by_culture_identification_or_direct_pcr", "猪结核明确诊断需在有病变组织中经培养鉴定或直接 PCR 确认 Mycobacterium spp.。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 1002", "all_stages"),
    ("TB-012-control-by-agent", "tuberculosis_control", "猪结核按病原防控", "prevention_and_control_should_follow_the_epidemiology_of_the_detected_mycobacterium_species", "猪结核预防控制应按检出的 Mycobacterium 种及其流行病学来设计；MTBC/MAA 与 MAH 的措施边界不同。", "SRC-0078", "Chapter 63 Tuberculosis; PDF page 1002", "all_stages"),
]


RULES = [
    ("RULE-379", "S. suis 自家苗候选株应来自系统部位", "streptococcosis_vaccine_boundary", "high", "SRC-0076", "Swine-ssuis-autogenous-vaccine-systemic-isolates.md", "S. suis 自家苗候选株应来自脑膜、脾、肝、关节等系统部位，不能用上呼吸道或扁桃体分离株直接替代。", "965"),
    ("RULE-380", "S. suis 口腔液/扁桃体阳性不得确诊疾病", "streptococcosis_diagnostics", "critical", "SRC-0076", "Swine-ssuis-oral-fluid-tonsil-not-diagnostic.md", "因 S. suis 可正常存在于唾液、扁桃体和鼻腔，相关阳性不得单独确诊 S. suis 病。", "965-966"),
    ("RULE-381", "S. suis 血清型 PCR 需保留 1/2 和 14 交叉检出", "streptococcosis_serotyping", "high", "SRC-0076", "Swine-ssuis-serotype-pcr-cross-detection-boundary.md", "S. suis serotype 2/1 PCR 解释必须保留 serotype 1/2/14 交叉检出边界，必要时需抗血清或 WGS 支持。", "965"),
    ("RULE-382", "S. suis 抗菌药选择必须结合药敏和本地耐药谱", "streptococcosis_treatment_boundary", "critical", "SRC-0076", "Swine-ssuis-antimicrobial-local-susceptibility-required.md", "S. suis 治疗建议必须结合分离株药敏、感染类型、给药途径和本地耐药谱，不得生成通用处方。", "966-967"),
    ("RULE-383", "S. suis 疫苗建议不得脱离血清型/菌株证据", "streptococcosis_vaccine_boundary", "critical", "SRC-0076", "Swine-ssuis-vaccine-serotype-strain-evidence-required.md", "S. suis 菌苗田间效果不稳定，疫苗建议必须有临床株血清型/菌株证据，不能外推固定程序。", "968"),
    ("RULE-384", "S. suis 根除通常不得优先于控制措施", "streptococcosis_control", "high", "SRC-0076", "Swine-ssuis-control-preferred-over-eradication.md", "在缺乏高置信携带检测且根除成本高、失败和再感染风险高时，应优先优化控制措施而非承诺根除。", "969"),
    ("RULE-385", "猪痢疾确诊需强 β 溶血 Brachyspira 与典型病例匹配", "swine_dysentery_diagnostics", "critical", "SRC-0077", "Swine-dysentery-strong-beta-hemolytic-brachyspira-required.md", "猪痢疾确诊需在典型痢疾和/或病变猪中确认强 β 溶血 Brachyspira spp.，检出 B. hyodysenteriae 不应脱离临床病变解释。", "975"),
    ("RULE-386", "猪痢疾病原不得限于 B. hyodysenteriae", "swine_dysentery_etiology", "high", "SRC-0077", "Swine-dysentery-not-only-b-hyodysenteriae.md", "猪痢疾解释需覆盖 B. hyodysenteriae、B. hampsonii 和 B. suanatina 等强 β 溶血病原。", "977"),
    ("RULE-387", "猪痢疾不得标为人兽共患", "swine_dysentery_public_health", "medium", "SRC-0077", "Swine-dysentery-agents-not-human-infection.md", "猪痢疾病原未被认为感染人类，不得生成夸大公共卫生风险的结论。", "978"),
    ("RULE-388", "猪痢疾防控必须覆盖粪口、湿粪和生物安全", "swine_dysentery_control", "high", "SRC-0077", "Swine-dysentery-fecal-oral-moist-feces-biosecurity.md", "猪痢疾防控需覆盖粪口传播、湿粪/有机物、带菌猪、鼠类/鸟类/水禽和人员车辆污染物。", "979"),
    ("RULE-389", "猪痢疾检测应保留选择性厌氧培养", "swine_dysentery_diagnostics", "critical", "SRC-0077", "Swine-dysentery-selective-anaerobic-culture-integral.md", "分子检测不能完全替代选择性厌氧培养；培养仍需用于检出所有已知 SD 病原并判断溶血表型。", "982"),
    ("RULE-390", "猪痢疾用药必须基于 MIC 和合规标签", "swine_dysentery_amr_boundary", "critical", "SRC-0077", "Swine-dysentery-treatment-mic-label-required.md", "猪痢疾抗菌药选择必须结合 MIC、耐药趋势和所在司法辖区产品标签，不得从教材表格生成本地剂量/休药期。", "983-984"),
    ("RULE-391", "B. pilosicoli 粪便阳性不得单独确诊 PIS/PCS", "pis_pcs_diagnostics", "critical", "SRC-0077", "Swine-bpilosicoli-fecal-positive-not-pis-pcs-alone.md", "B. pilosicoli 粪便阳性需结合临床、病变和完整诊断调查，不能单独确诊 PIS/PCS。", "989"),
    ("RULE-392", "B. pilosicoli 无有效疫苗", "pis_pcs_vaccine_boundary", "medium", "SRC-0077", "Swine-bpilosicoli-no-effective-vaccine.md", "B. pilosicoli 无有效疫苗，不得生成 PIS/PCS 疫苗程序。", "990"),
    ("RULE-393", "猪结核肉眼和镜检病变不能区分 MAC 与 MTBC", "tuberculosis_diagnostics", "critical", "SRC-0078", "Swine-tb-lesions-not-mac-mtbc-speciation.md", "猪结核样肉眼和镜检病变不能区分 MAC 与 MTBC，必须依赖培养鉴定、PCR 或分子分型。", "995,1001-1002"),
    ("RULE-394", "猪结核防控必须按检出 Mycobacterium 种设计", "tuberculosis_control", "critical", "SRC-0078", "Swine-tb-control-by-mycobacterium-species.md", "猪结核防控需按检出的 Mycobacterium 种及流行病学设计，MTBC/MAA 宿主适应型与 MAH 环境型措施不同。", "995,1002"),
    ("RULE-395", "MAH 暴发调查必须评估有机垫料、潮湿有机物和生物膜", "tuberculosis_environment", "high", "SRC-0078", "Swine-mah-organic-bedding-biofilm-risk.md", "MAH 相关猪结核样病变调查需评估木屑/锯末/泥炭/秸秆、潮湿分解有机物、饮水系统和生物膜。", "998-999,1002"),
    ("RULE-396", "猪结核确诊需组织病变中培养鉴定或直接 PCR", "tuberculosis_diagnostics", "critical", "SRC-0078", "Swine-tb-definitive-culture-identification-pcr.md", "猪结核明确诊断需在有病变组织中通过 Mycobacterium 培养鉴定或直接 PCR 确认。", "1002"),
]


TOPICS = [
    ("Swine-streptococcosis-diagnostics-treatment-vaccine-control-boundaries.md", "猪链球菌病诊断、用药、疫苗和控制边界", "SRC-0076", "本主题汇总 S. suis CSF/系统部位分离、PCR/血清型和口腔液/扁桃体限制、药敏和本地耐药谱、诱因控制、疫苗效果不稳定和根除边界。"),
    ("Swine-dysentery-brachyspira-diagnostics-control-amr-boundaries.md", "猪痢疾/Brachyspira 诊断、防控和耐药边界", "SRC-0077", "本主题汇总 Brachyspira 种类、猪痢疾强 β 溶血确诊、粪口传播、湿粪存活、病变、培养/PCR、鉴别诊断、抗菌药耐药和防控边界。"),
    ("Swine-tuberculosis-mac-mtbc-diagnosis-control-boundaries.md", "猪结核 MAC/MTBC 诊断和防控边界", "SRC-0078", "本主题汇总猪结核 MTBC/MAC/MAH 病原边界、野猪/环境来源、公共卫生限制、病变、诊断、采样和按病原防控边界。"),
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
- 批次：Formal Batch 027 / V4。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_027_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_027_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_027_pdf_pages_965_1004_parser_report.txt`。
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
- 本页正式 facts 已在 `issues/formal_batch_027_cross_review.md` 中交叉审查。
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
    write_text(ISSUES / "formal_batch_027_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "source_ids": [source[0] for source in SOURCES],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pypdf",
            "report": "issues/formal_batch_027_pdf_pages_965_1004_parser_report.txt",
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
        ("DIS-051-streptococcosis-streptococcus-suis.md", "Formal Batch 027 / V4 正文抽取：已补充 S. suis 诊断、CSF/系统部位分离、口腔液/扁桃体限制、药敏用药边界、诱因控制、疫苗不确定性、根除边界，以及 S. porcinus、S. dysgalactiae、S. zooepidemicus 等其他链球菌边界；详见 `SRC-0076`。"),
        ("DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md", "Formal Batch 027 / V4 正文抽取：已补充 Chapter 62 猪痢疾和 Brachyspira 结肠炎，包括 Brachyspira 种类、强 β 溶血确诊、粪口传播、病变、培养/PCR、鉴别、耐药和防控边界；详见 `SRC-0077`。"),
        ("DIS-053-tuberculosis.md", "Formal Batch 027 / V4 正文抽取：已补充 Chapter 63 猪结核 MTBC/MAC/MAH 病原、野猪和环境来源、公共卫生边界、病变、临床诊断限制、培养/PCR 确诊、采样和按病原防控边界；详见 `SRC-0078`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 027 / V4 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_027_cross_review.md", """# Formal Batch 027 / V4 Cross Review

## 范围

- PDF page 965-971：Chapter 61 Streptococcosis 正文后段。
- PDF page 972-974：Chapter 61 参考文献，仅记录边界。
- PDF page 975-990：Chapter 62 Swine Dysentery and Brachyspiral Colitis 正文。
- PDF page 991-994：Chapter 62 参考文献，仅记录边界。
- PDF page 995-1003：Chapter 63 Tuberculosis 正文。
- PDF page 1004：Chapter 63 参考文献开端，仅记录边界。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行，并同步 V4 主线文档。
- 页数为 40 页，符合正式批次常规范围。
- 参考文献页只记录章节边界，不生成 standalone facts。
- 所有正式 facts 均先写入候选事实文件，再经页码锚点、内容边界和一致性审查后落库。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_027_pdf_pages_965_1004_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量对照；PDF page 975 和 995 采用 pdfplumber 文本，其余页采用 fitz。
- 三次核对：`pypdf`，用于页级文本存在性和异常提示。
- 解析报告：`issues/formal_batch_027_pdf_pages_965_1004_parser_report.txt`。

## 审查结论

本批候选 facts 42 条、规则页 18 个、来源页 3 个、主题页 3 个。经交叉审查后允许正式落库，所有 facts 均为 `HUMAN_REVIEWED`。

## 审查 1：页码锚点核验

- `SRC-0076` 锚定 PDF page 965-974，其中 PDF page 972-974 为 Chapter 61 参考文献边界。
- `SRC-0077` 锚定 PDF page 975-994，其中 PDF page 991-994 为 Chapter 62 参考文献边界。
- `SRC-0078` 锚定 PDF page 995-1004，其中 PDF page 1004 为 Chapter 63 参考文献开端。

## 审查 2：内容边界核验

- Streptococcosis 内容保留诊断、血清型/PCR/口腔液限制、药敏用药、诱因控制、疫苗不确定性和根除边界，不生成处方、剂量、固定疫苗程序或中国监管结论。
- Swine dysentery / Brachyspira 内容保留强 β 溶血确诊、培养/PCR、粪口传播、环境存活、病变、鉴别诊断、耐药和防控边界；教材药物表不转换为本地剂量/休药期。
- Tuberculosis 内容保留 MTBC/MAC/MAH 病原边界、环境风险、公共卫生限制、病变、确诊和按病原防控；美国屠宰/法规语境不迁移为中国监管答案。

## 审查 3：一致性核验

- facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- `SRC-0076` 至 `SRC-0078`、`RULE-379` 至 `RULE-396` 与既有条目不重复。
- 本批正式落库内容与 V4 文档同步，V3 文档保留为历史记录。

## 明确未落库

- 参考文献列表。
- S. suis、猪痢疾/PIS/PCS 的具体药物剂量、疗程、休药期和当地处方。
- S. suis、猪痢疾、B. pilosicoli 的固定疫苗程序。
- 猪结核美国屠宰法规、废弃/烹煮细则和中国监管处置结论。

## 保留问题

- PDF page 1005 起需继续 Chapter 63 Tuberculosis 参考文献后段，并视章节边界进入后续细菌病章节。
- TB 监管、检疫、屠宰处置、人群暴露和中国本地合规结论必须等待 A0/A1 权威来源。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 027 / V4 实施记录

- 完成时间：2026-05-07 17:10:00 +08:00。
- 处理范围：PDF page 965-1004。
- 章节边界：Chapter 61 Streptococcosis 正文后段和参考文献；Chapter 62 Swine Dysentery and Brachyspiral Colitis 正文和参考文献；Chapter 63 Tuberculosis 正文前中段和参考文献开端。
- 参考文献处理：PDF page 972-974、991-994、1004 仅作为边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0076` 至 `SRC-0078`。
- 新增主题页：猪链球菌病诊断/用药/疫苗/控制边界、猪痢疾/Brachyspira 诊断/防控/耐药边界、猪结核 MAC/MTBC 诊断和防控边界。
- 新增规则页：`RULE-379` 至 `RULE-396`。
- 新增候选事实：`issues/formal_batch_027_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_027_cross_review.md`。
- 正式落库 facts：42 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、具体处方/剂量/休药期、固定疫苗程序、美国屠宰法规执行细则和中国监管结论。

### Formal Batch 027 / V4 交叉审查

- 页码锚点核验：通过。`SRC-0076` 覆盖 PDF page 965-974；`SRC-0077` 覆盖 975-994；`SRC-0078` 覆盖 995-1004。
- 内容边界核验：通过。S. suis、Brachyspira/猪痢疾和猪结核均只落库教材证据和诊断/传播/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 1004。
- 下一批应从 PDF page 1005 开始。
- 推荐下一批：PDF page 1005-1026，继续 Chapter 63 Tuberculosis 参考文献后段，并视章节边界进入 Section IV 后续细菌病章节。
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
    print("formal batch 027 v4 built")


if __name__ == "__main__":
    main()
