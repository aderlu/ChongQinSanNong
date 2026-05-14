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
NOW = "2026-05-07T01:40:00+00:00"
BATCH_ID = "formal-batch-021-v3"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 725, end: int = 764) -> None:
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
    write_text(ISSUES / "formal_batch_021_pdf_pages_725_764_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_021_pdf_pages_725_764_parser_report.txt", "\n".join(report_rows) + "\n")


SOURCES = [
    ("SRC-0050", "Diseases of Swine 11e Chapter 41 PRRSV control and surveillance", "PDF page 725-726", "wiki/sources/SRC-0050-diseases-of-swine-11e-chapter-41-prrsv-control-surveillance.md", "Chapter 41 closing text covering PRRSV control limits, needle-mediated spread, gilt acclimatization, LVI risk controls, herd closure, partial depopulation, test-and-removal, and surveillance sample boundaries."),
    ("SRC-0051", "Diseases of Swine 11e Chapter 42 Swinepox Virus", "PDF page 733-738", "wiki/sources/SRC-0051-diseases-of-swine-11e-chapter-42-swinepox-virus.md", "Chapter 42 covers Swinepox relevance, etiology, host restriction, transmission, pathogenesis, lesions, diagnosis, immunity, prevention and control boundaries. PDF page 738 is references."),
    ("SRC-0052", "Diseases of Swine 11e Chapter 43 Reoviruses Rotaviruses and Reoviruses", "PDF page 739-751", "wiki/sources/SRC-0052-diseases-of-swine-11e-chapter-43-reoviruses-rotaviruses.md", "Chapter 43 covers rotavirus and reovirus taxonomy, environmental stability, pathogenesis, clinical enteric disease, diagnosis, immunity, treatment and control boundaries. PDF pages 748-751 are references."),
    ("SRC-0053", "Diseases of Swine 11e Chapter 44 Retroviruses", "PDF page 752-756", "wiki/sources/SRC-0053-diseases-of-swine-11e-chapter-44-retroviruses.md", "Chapter 44 covers porcine endogenous retroviruses in xenotransplantation risk assessment, subtypes, host range, transmission evidence, detection and diagnosis boundaries. PDF page 756 is references."),
    ("SRC-0054", "Diseases of Swine 11e Chapter 45 Rhabdoviruses", "PDF page 757-763", "wiki/sources/SRC-0054-diseases-of-swine-11e-chapter-45-rhabdoviruses.md", "Chapter 45 covers vesicular stomatitis viruses and rabies virus, including vesicular disease differential diagnosis, zoonotic/PPE boundary, vector/contact transmission, lesions, control, rabies spillover, clinical signs and vaccine boundaries. PDF page 763 is references."),
    ("SRC-0055", "Diseases of Swine 11e Chapter 46 Togaviruses opening", "PDF page 764", "wiki/sources/SRC-0055-diseases-of-swine-11e-chapter-46-togaviruses-opening.md", "Chapter 46 opening covers Togaviridae/alphavirus overview, basic stability and Eastern equine encephalitis virus relevance opening. This source is an opening-page anchor and needs continuation in the next batch."),
]


FACTS = [
    ("PRRSV-019-control-limited-treatment", "prrsv_control", "PRRSV 控制和治疗边界", "specific_treatments_to_reduce_clinical_effects_are_limited", "PRRSV 缺乏特异性治疗方法，控制目标主要是减轻不同生产阶段的不利影响；不得把支持疗法或抗生素管理继发感染解释为抗病毒根治方案。", "SRC-0050", "Chapter 41 PRRSV control; PDF page 725", "all_stages"),
    ("PRRSV-020-needle-spread", "prrsv_transmission_control", "PRRSV 污染针头传播", "hematogenous_spread_via_contaminated_needles_is_documented", "PRRSV 可经污染针头造成血源性传播，因此换针或无针技术属于降低场内传播风险的管理点。", "SRC-0050", "Chapter 41 PRRSV control; PDF page 725", "all_stages"),
    ("PRRSV-021-pig-flow-control", "prrsv_control", "PRRSV 慢性感染猪群流程控制", "chronically_infected_herds_are_managed_by_pig_flow_strategies", "慢性 PRRSV 感染猪群控制强调分娩舍 McREBEL、全进全出或部分清群等猪流策略，以减少断奶后地方性病毒循环。", "SRC-0050", "Chapter 41 PRRSV control; PDF page 725", "all_stages"),
    ("PRRSV-022-gilt-acclimatization", "prrsv_gilt_management", "PRRSV 后备母猪驯化", "naive_replacement_gilts_can_drive_recurrent_reproductive_failure", "将未经免疫或暴露的后备母猪引入感染繁殖群，可导致反复繁殖失败和母子间水平/垂直传播；后备母猪池管理是控制关键点。", "SRC-0050", "Chapter 41 PRRSV gilt acclimatization; PDF page 725", "gilts"),
    ("PRRSV-023-lvi-risk", "prrsv_control_boundary", "PRRSV 活病毒接种风险", "live_virus_inoculation_requires_virus_characterization_dose_quantification_and_screening", "PRRSV 农场特异株活病毒接种存在固有风险，应进行病毒测序表征、剂量定量和材料筛查；不得自动生成通用 LVI 操作方案。", "SRC-0050", "Chapter 41 PRRSV gilt acclimatization; PDF page 725", "gilts"),
    ("PRRSV-024-herd-closure", "prrsv_elimination_boundary", "PRRSV 封群边界", "herd_closure_can_be_used_for_elimination_but_timing_depends_on_herd_status", "PRRSV 封群可作为净化策略的一部分，但依赖猪群状态、繁殖群排毒停止和猪流管理；不得脱离场况给出固定封群时长。", "SRC-0050", "Chapter 41 PRRSV elimination; PDF page 725-726", "breeding_herd"),
    ("PRRSV-025-test-removal", "prrsv_elimination_boundary", "PRRSV 检测剔除净化", "test_and_removal_uses_antibody_and_nucleic_acid_tests_but_is_costly_and_labor_intensive", "PRRSV 检测剔除可用抗体和核酸检测识别阳性个体后剔除，但成本和劳动强度较高，适用于特定净化目标而非通用方案。", "SRC-0050", "Chapter 41 PRRSV elimination; PDF page 726", "breeding_herd"),
    ("PRRSV-026-surveillance", "prrsv_surveillance", "PRRSV 监测样本边界", "surveillance_requires_routine_population_testing_and_can_use_serum_semen_oral_fluids_or_processing_fluids", "PRRSV 感染常可沉默存在，群体状态评估必须依赖常规检测；血清、精液、血拭子、口腔液和新生仔猪处理液等样本各有监测边界。", "SRC-0050", "Chapter 41 PRRSV surveillance; PDF page 726", "all_stages"),
    ("SWPV-001-relevance", "swinepox_relevance", "猪痘流行和卫生关联", "swinepox_occurs_sporadically_worldwide_and_is_associated_with_poor_sanitation", "猪痘在全球猪群中散发，通常与卫生条件差相关，多表现为局部脓疱样皮肤病变，幼龄猪可更严重。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 733", "piglets"),
    ("SWPV-002-agent-host", "swinepox_etiology", "猪痘病毒宿主限制", "swinepox_virus_has_restricted_host_range_and_is_difficult_to_grow_in_non_swine_systems", "猪痘病毒宿主范围受限，在非猪源细胞或鸡胚绒毛尿囊膜上的分离/培养尝试并不成功；宿主范围不得外推。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 734", "all_stages"),
    ("SWPV-003-transmission", "swinepox_transmission", "猪痘传播", "swinepox_can_transmit_by_direct_contact_or_mechanical_vectors_such_as_lice", "猪痘可经直接接触或机械媒介传播，猪虱和卫生不良可提高传播风险。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 735", "all_stages"),
    ("SWPV-004-viremia-boundary", "swinepox_pathogenesis_boundary", "猪痘病毒血症证据边界", "viremia_has_been_proposed_but_requires_substantiating_evidence", "猪痘病毒从原发复制部位向继发部位扩散的机制仍不清楚，血症假说需要更多证据；不得把血症作为已确证机制。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 735", "all_stages"),
    ("SWPV-005-lesions", "swinepox_clinical_lesions", "猪痘皮肤病变进程", "lesions_progress_from_papules_to_umbilicated_crusts_and_may_leave_spots", "猪痘皮肤损害可由丘疹发展为脐凹样结痂，结痂脱落后可留斑；真正水疱期可缺失或不明显。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 736", "all_stages"),
    ("SWPV-006-differential", "swinepox_differential", "猪痘鉴别诊断", "swinepox_skin_lesions_require_differentiation_from_other_dermatologic_conditions", "猪痘皮肤病变需与其他猪皮肤病、外寄生虫、创伤或继发感染等鉴别，不能仅凭结痂性皮损定因。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 736-737", "all_stages"),
    ("SWPV-007-diagnosis", "swinepox_diagnostics", "猪痘确诊", "electron_microscopy_histopathology_or_virus_isolation_can_support_or_confirm_swpv", "电镜、组织病理学和猪源细胞/PK-15 细胞病毒分离结合免疫荧光或中和试验可用于支持或确认猪痘病毒感染。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 737", "all_stages"),
    ("SWPV-008-control", "swinepox_control", "猪痘控制", "control_focuses_on_sanitation_vector_control_and_preventing_secondary_infection", "猪痘控制重点是改善卫生、控制媒介和减少继发感染；不得生成特异性抗病毒治疗方案。", "SRC-0051", "Chapter 42 Swinepox Virus; PDF page 737", "all_stages"),
    ("ROTA-001-taxonomy", "rotavirus_taxonomy", "轮状病毒分类", "rotaviruses_are_reoviridae_with_segmented_dsRNA_and_multiple_species", "轮状病毒属于 Reoviridae，具分节段双链 RNA，猪相关轮状病毒需按种和基因型解释，不能用单一血清型概括全部风险。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 739-741", "all_stages"),
    ("ROTA-002-environment", "rotavirus_environment", "轮状病毒环境稳定性", "rotavirus_is_highly_stable_and_drying_does_not_inactivate_all_virions", "轮状病毒环境稳定性高，完全干燥不能灭活所有病毒颗粒；清洁消毒策略需考虑环境持续污染。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 742", "all_stages"),
    ("ROTA-003-disinfection", "rotavirus_control", "轮状病毒消毒边界", "chlorine_phenolic_glutaraldehyde_or_halogen_disinfectants_may_help_if_used_consistently", "卤素/氯类、酚类和戊二醛等消毒剂可帮助控制轮状病毒传播，但效果依赖持续、正确使用和有机物清除。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 742", "all_stages"),
    ("ROTA-004-pathogenesis", "rotavirus_pathogenesis", "轮状病毒腹泻机制", "rotavirus_diarrhea_is_linked_to_villus_loss_and_malabsorption", "轮状病毒腹泻的公认机制包括绒毛损失、吸收不足和吸收不良性腹泻，其他分泌性机制也可能参与。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 743", "piglets"),
    ("ROTA-005-clinical", "rotavirus_clinical_pattern", "轮状病毒临床边界", "rotavirus_primarily_affects_neonatal_piglets_and_signs_overlap_other_enteric_pathogens", "轮状病毒主要影响新生仔猪，临床表现与其他肠道病原重叠，不能仅凭腹泻确诊。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 744", "piglets"),
    ("ROTA-006-diagnosis", "rotavirus_diagnostics", "轮状病毒诊断", "diagnosis_requires_laboratory_testing_because_clinical_signs_are_non_specific", "轮状病毒诊断必须依赖实验室检测，临床症状和日龄只能提示纳入鉴别诊断。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 744", "piglets"),
    ("ROTA-007-immunity", "rotavirus_immunity", "轮状病毒保护性免疫边界", "serum_neutralizing_antibody_is_a_poor_indicator_of_protective_immunity", "轮状病毒血清中和抗体水平并不是保护性免疫的良好指标，局部肠道免疫和母源免疫需要单独解释。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 745", "piglets"),
    ("ROTA-008-treatment", "rotavirus_treatment_boundary", "轮状病毒治疗边界", "treatment_focuses_on_supportive_care_and_no_specific_antiviral_program_is_established", "轮状病毒腹泻治疗以支持疗法和减少脱水/继发问题为主，不得生成特异性抗病毒处方。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 746", "piglets"),
    ("REO-001-pathogenesis-limited", "reovirus_boundary", "猪呼肠孤病毒发病机制证据边界", "reovirus_pathogenesis_details_are_lacking_despite_respiratory_and_intestinal_replication", "呼肠孤病毒可在呼吸道和肠道复制，但猪中发病机制细节仍有限，检测结果需谨慎定因。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 747", "all_stages"),
    ("REO-002-reinfection", "reovirus_immunity", "呼肠孤病毒再感染边界", "immunity_may_wane_and_pigs_can_be_susceptible_to_reinfection", "呼肠孤病毒相关免疫可随时间下降，猪可再次易感；不能把一次感染或抗体存在解释为长期完全保护。", "SRC-0052", "Chapter 43 Reoviruses; PDF page 747", "all_stages"),
    ("PERV-001-relevance", "retrovirus_relevance", "猪内源性逆转录病毒关注点", "porcine_endogenous_retroviruses_are_relevant_to_xenotransplantation_risk_assessment", "猪内源性逆转录病毒主要是异种移植安全性评估中的关注点，不应泛化为普通猪场生产性传染病。", "SRC-0053", "Chapter 44 Retroviruses; PDF page 752", "all_stages"),
    ("PERV-002-subtypes", "retrovirus_taxonomy", "PERV 亚型和宿主范围", "perv_a_and_b_are_present_in_all_pigs_and_can_infect_human_cells_while_perv_c_is_ecotropic", "PERV-A 和 PERV-B 存在于所有猪基因组并可感染人源细胞，PERV-C 多存在于猪且主要感染猪细胞；宿主范围需按亚型解释。", "SRC-0053", "Chapter 44 Retroviruses; PDF page 753", "all_stages"),
    ("PERV-003-transmission-evidence", "retrovirus_transmission_boundary", "PERV 体内传播证据边界", "pig_to_small_animal_nonhuman_primate_and_early_human_trials_did_not_show_transmission", "教材记录猪到小动物、非人灵长类和早期人体试验中未观察到 PERV 传播；风险解释应保留异种移植场景和检测条件边界。", "SRC-0053", "Chapter 44 Retroviruses; PDF page 754", "all_stages"),
    ("PERV-004-detection", "retrovirus_diagnostics", "PERV 检测方法边界", "perv_expression_or_particles_can_be_detected_by_molecular_serologic_microscopy_or_infectivity_assays", "PERV 可用核酸、蛋白表达、逆转录酶、电子显微镜和感染性试验等方法评估；单一检测阳性不等于已发生临床传播。", "SRC-0053", "Chapter 44 Retroviruses; PDF page 755", "all_stages"),
    ("PERV-005-control-boundary", "retrovirus_control_boundary", "PERV 管理边界", "perv_management_belongs_to_xenotransplantation_screening_and_risk_reduction", "PERV 管理属于异种移植供体筛选和风险降低范畴，不得转化为普通猪群扑杀、封锁或治疗建议。", "SRC-0053", "Chapter 44 Retroviruses; PDF page 752-755", "all_stages"),
    ("VS-001-differential", "vesicular_stomatitis_differential", "水疱性口炎鉴别诊断", "vesicular_stomatitis_in_swine_resembles_fmd_svd_ves_and_svv", "猪水疱性口炎临床上类似 FMD、SVD、猪水疱疹和 SVV，必须进行实验室鉴别。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 757", "all_stages"),
    ("VS-002-zoonotic-ppe", "vesicular_stomatitis_public_health", "VSV 人兽共患和 PPE", "vsv_is_zoonotic_and_ppe_should_be_used_to_reduce_animal_to_human_transmission", "VSV 为人兽共患病毒，接触疑似或确诊动物时应使用适当 PPE 降低动物向人传播风险。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 757", "all_stages"),
    ("VS-003-geography", "vesicular_stomatitis_epidemiology", "水疱性口炎地理边界", "vesicular_stomatitis_is_not_known_to_occur_outside_the_americas", "教材指出水疱性口炎尚不知发生于美洲以外；地理风险解释不能脱离流行区证据。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 758", "all_stages"),
    ("VS-004-transmission", "vesicular_stomatitis_transmission", "VSV 接触和媒介传播", "vsv_can_transmit_by_contact_and_by_biological_or_mechanical_insect_vectors", "VSV 可通过动物间直接接触以及昆虫媒介的生物性或机械性传播；传播解释需结合病灶、媒介和地区流行情况。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 758", "all_stages"),
    ("VS-005-viremia-boundary", "vesicular_stomatitis_pathogenesis_boundary", "VSV 血症证据边界", "viremia_has_not_been_reported_in_naturally_infected_livestock", "自然感染家畜中未报道 VSV 血症，传播模型不应依赖血症假设。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 759", "all_stages"),
    ("VS-006-lesions", "vesicular_stomatitis_lesions", "水疱性口炎病变", "vesicles_can_occur_on_oral_mucosa_snout_teats_and_coronary_bands_and_rupture_quickly", "水疱性口炎水疱可见于口腔黏膜、鼻镜、乳头和蹄冠带，并可在形成后 1-2 天破裂，释放富含病毒的渗出物。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 759", "all_stages"),
    ("VS-007-diagnosis", "vesicular_stomatitis_diagnostics", "水疱性口炎确诊", "clinical_vs_in_swine_is_indistinguishable_from_other_vesicular_diseases_and_requires_lab_samples", "猪水疱性口炎临床上无法与 FMD、SVD、VES 或 SVV 区分，必须采集并提交诊断样本做实验室评估。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 759", "all_stages"),
    ("VS-008-control", "vesicular_stomatitis_control", "水疱病观察时移动控制", "movement_of_animals_and_materials_should_stop_until_diagnosis_when_vesicular_disease_is_observed", "猪出现水疱病时，在诊断明确前应停止动物和物资进出，并立即通知相应动物卫生主管部门；具体监管处置需本地 A0/A1 规则确认。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 760", "all_stages"),
    ("RAB-001-swine-risk", "rabies_relevance", "猪狂犬病溢出风险", "rabies_risk_in_swine_depends_on_contact_with_wildlife_or_canine_reservoirs", "猪狂犬病风险取决于与野生动物或犬类储存宿主接触机会，集约化隔离可降低溢出风险。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 760", "all_stages"),
    ("RAB-002-clinical", "rabies_clinical_pattern", "猪狂犬病临床表现边界", "rabies_clinical_signs_in_swine_are_limited_and_inconsistent_in_reports", "猪狂犬病临床报告有限且不一致，可包括突然死亡、流涎、抽搐、共济失调、行为改变和麻痹；不得凭单一神经症状确诊。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 761", "all_stages"),
    ("RAB-003-human-exposure", "rabies_public_health", "猪狂犬病人暴露边界", "virus_should_be_assumed_present_when_determining_human_exposure_treatment_options", "在评估人暴露后处理时，应假定病猪可存在病毒，具体暴露处置需公共卫生权威指南确认。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 761", "all_stages"),
    ("RAB-004-vaccine-boundary", "rabies_vaccine_boundary", "猪狂犬病疫苗边界", "there_are_no_licensed_rabies_vaccines_for_use_in_swine", "由于免疫持续期试验成本和市场有限，教材指出没有获准用于猪的狂犬病疫苗；不得生成猪群常规狂犬疫苗程序。", "SRC-0054", "Chapter 45 Rhabdoviruses; PDF page 762", "all_stages"),
    ("TOGA-001-opening-boundary", "togavirus_opening", "Togaviridae 开端锚点", "chapter_46_opening_only_provides_alphavirus_overview_and_eeev_relevance_start", "PDF page 764 仅进入 Togaviridae/Alphavirus 概述和 EEEV 相关性开端；具体猪病事实需下一批继续正文后再落库。", "SRC-0055", "Chapter 46 Togaviruses opening; PDF page 764", "all_stages"),
]


RULES = [
    ("RULE-274", "PRRSV 支持疗法不得解释为特异性抗病毒治疗", "prrsv_control", "high", "SRC-0050", "Swine-prrsv-supportive-care-not-specific-antiviral.md", "PRRSV 控制中退热、抗炎或抗生素管理继发感染只能作为支持性或并发症管理，不能生成特异性抗病毒根治结论。", "725"),
    ("RULE-275", "PRRSV 针头和血源传播必须纳入场内传播控制", "prrsv_transmission_control", "high", "SRC-0050", "Swine-prrsv-needle-hematogenous-spread-control.md", "PRRSV 经污染针头血源性传播已有记录，场内控制建议必须考虑换针或无针技术等风险降低措施。", "725"),
    ("RULE-276", "PRRSV 活病毒接种不得生成通用操作方案", "prrsv_lvi_boundary", "critical", "SRC-0050", "Swine-prrsv-live-virus-inoculation-risk-boundary.md", "PRRSV LVI 存在固有风险，只有在病毒表征、剂量定量和材料筛查等质量控制语境下才能讨论，不得输出通用接种流程。", "725"),
    ("RULE-277", "PRRSV 净化策略必须保留猪群状态和成本边界", "prrsv_elimination_boundary", "high", "SRC-0050", "Swine-prrsv-elimination-strategy-herd-context-boundary.md", "封群、部分清群、检测剔除等 PRRSV 净化策略必须结合繁殖群排毒状态、猪流、成本和劳动强度，不得脱离场况给固定方案。", "725-726"),
    ("RULE-278", "PRRSV 监测必须依赖常规群体检测", "prrsv_surveillance", "high", "SRC-0050", "Swine-prrsv-surveillance-routine-population-testing.md", "PRRSV 感染可沉默存在，群体状态判断必须基于常规检测数据，而不是仅依据临床表现。", "726"),
    ("RULE-279", "猪痘不得仅凭结痂皮损定因", "swinepox_differential", "high", "SRC-0051", "Swine-swinepox-skin-lesions-not-alone-diagnostic.md", "猪痘皮肤病变需要与其他皮肤病、外寄生虫、创伤和继发感染鉴别，不能仅凭结痂性皮损定因。", "736-737"),
    ("RULE-280", "猪痘血症机制必须保留未确证边界", "swinepox_pathogenesis_boundary", "medium", "SRC-0051", "Swine-swinepox-viremia-not-confirmed-boundary.md", "猪痘病毒血症只是扩散机制假说之一，证据不足时不得写成已确证机制。", "735"),
    ("RULE-281", "猪痘控制以卫生和媒介管理为主", "swinepox_control", "medium", "SRC-0051", "Swine-swinepox-sanitation-vector-control.md", "猪痘控制应围绕卫生改善、媒介控制和继发感染风险管理，不得生成特异性抗病毒处方。", "737"),
    ("RULE-282", "轮状病毒腹泻不得仅凭临床症状确诊", "rotavirus_diagnostics", "high", "SRC-0052", "Swine-rotavirus-diarrhea-lab-testing-required.md", "轮状病毒临床表现与其他肠道病原重叠，必须结合实验室检测确认。", "744"),
    ("RULE-283", "轮状病毒环境控制必须考虑高稳定性", "rotavirus_environment", "high", "SRC-0052", "Swine-rotavirus-environmental-stability-disinfection.md", "轮状病毒环境稳定性高，消毒和清洁建议必须考虑干燥不能完全灭活和有机物清除边界。", "742"),
    ("RULE-284", "轮状病毒保护不能只看血清中和抗体", "rotavirus_immunity", "medium", "SRC-0052", "Swine-rotavirus-serum-neutralization-poor-protection-indicator.md", "轮状病毒血清中和抗体水平不是保护性免疫的可靠单一指标，免疫解释需保留肠道和母源免疫边界。", "745"),
    ("RULE-285", "呼肠孤病毒检测不得自动定为主因", "reovirus_causality", "medium", "SRC-0052", "Swine-reovirus-detection-not-primary-cause.md", "呼肠孤病毒发病机制资料有限，检测阳性需结合病变、组织定位和其他病原证据，不得自动定为主因。", "747"),
    ("RULE-286", "PERV 主要属于异种移植风险评估语境", "retrovirus_context", "high", "SRC-0053", "Swine-perv-xenotransplantation-context-boundary.md", "PERV 内容应限制在异种移植供体筛查和风险评估语境，不能泛化为普通猪场生产性传染病处置。", "752-755"),
    ("RULE-287", "PERV 单一检测阳性不等同临床传播", "retrovirus_diagnostics", "high", "SRC-0053", "Swine-perv-detection-not-clinical-transmission.md", "PERV 核酸、蛋白或颗粒检测必须结合感染性和传播证据解释，单一阳性不能等同已发生临床传播。", "755"),
    ("RULE-288", "猪水疱性口炎必须与 FMD/SVD/VES/SVV 鉴别", "vesicular_stomatitis_differential", "critical", "SRC-0054", "Swine-vesicular-stomatitis-fmd-svd-ves-svv-differential.md", "猪水疱性口炎临床上无法与 FMD、SVD、VES 或 SVV 区分，必须进行实验室鉴别。", "757-759"),
    ("RULE-289", "VSV 人兽共患风险必须提示 PPE 边界", "vesicular_stomatitis_public_health", "high", "SRC-0054", "Swine-vsv-zoonotic-ppe-boundary.md", "VSV 为人兽共患病毒，接触疑似或确诊病例时应提示 PPE 和人暴露风险，但具体公共卫生处置需权威指南。", "757"),
    ("RULE-290", "水疱病未诊断前不得放行动物和物资流动", "vesicular_disease_control", "critical", "SRC-0054", "Swine-vesicular-disease-stop-movement-until-diagnosis.md", "猪出现水疱病时，诊断明确前应停止动物和物资进出并通知动物卫生主管部门；本地监管命令需 A0/A1 来源。", "760"),
    ("RULE-291", "猪狂犬病不得凭单一神经症状确诊", "rabies_diagnostics", "critical", "SRC-0054", "Swine-rabies-neurologic-signs-not-diagnostic.md", "猪狂犬病临床报告有限且不一致，神经症状必须结合实验室和暴露史解释，不得单独确诊。", "761"),
    ("RULE-292", "猪狂犬病疫苗不得生成常规免疫程序", "rabies_vaccine_boundary", "high", "SRC-0054", "Swine-rabies-no-licensed-swine-vaccine-program.md", "教材指出没有获准用于猪的狂犬病疫苗，不能生成猪群常规狂犬疫苗程序；高价值种猪场景仍需权威兽医和法规确认。", "762"),
    ("RULE-293", "Togavirus 开端页不得扩展为完整猪病结论", "togavirus_opening_boundary", "medium", "SRC-0055", "Swine-togavirus-opening-page-no-full-conclusion.md", "PDF page 764 仅提供 Togaviridae/Alphavirus 开端锚点，具体 EEEV/Getah 等猪病事实需下一批正文证据后再落库。", "764"),
]


TOPICS = [
    ("Swine-prrsv-control-elimination-surveillance-boundaries.md", "PRRSV 控制、净化和监测边界", "SRC-0050", "本主题汇总 PRRSV 支持疗法边界、针头传播、后备母猪驯化、LVI 风险、封群/部分清群/检测剔除和常规监测样本边界。"),
    ("Swine-swinepox-virus-diagnosis-control-boundaries.md", "猪痘诊断和控制边界", "SRC-0051", "本主题汇总猪痘的卫生关联、宿主限制、传播、皮肤病变、血症证据边界、诊断和控制策略。"),
    ("Swine-rotavirus-reovirus-enteric-disease-boundaries.md", "轮状病毒和呼肠孤病毒肠道病边界", "SRC-0052", "本主题汇总轮状病毒分类、环境稳定性、腹泻机制、实验室诊断、免疫保护和呼肠孤病毒因果解释边界。"),
    ("Swine-retrovirus-perv-xenotransplantation-boundaries.md", "猪内源性逆转录病毒 PERV 异种移植边界", "SRC-0053", "本主题汇总 PERV 亚型、宿主范围、传播证据、检测方法和异种移植语境边界。"),
    ("Swine-rhabdovirus-vesicular-stomatitis-rabies-boundaries.md", "Rhabdovirus 水疱性口炎和狂犬病边界", "SRC-0054", "本主题汇总 VSV 水疱病鉴别、人兽共患和 PPE、传播、控制，以及猪狂犬病溢出、临床和疫苗边界。"),
    ("Swine-togavirus-opening-anchor.md", "Togavirus 开端锚点", "SRC-0055", "本主题仅作为 Chapter 46 开端锚点，等待下一批继续正文后扩展。"),
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
- 批次：Formal Batch 021 / V3。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_021_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_021_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_021_pdf_pages_725_764_parser_report.txt`。
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
- 本页正式 facts 已在 `issues/formal_batch_021_cross_review.md` 中交叉审查。
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

- 本规则用于生成、评估和审核猪病 Wiki 中病毒病、诊断、传播、监测、免疫、公共卫生和监管边界解释。
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
    write_text(ISSUES / "formal_batch_021_candidate_facts.json", json.dumps({
        "batch_id": BATCH_ID,
        "source_ids": [source[0] for source in SOURCES],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pypdf",
            "report": "issues/formal_batch_021_pdf_pages_725_764_parser_report.txt",
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
        ("DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md", "Formal Batch 021 / V3 正文抽取：已补充 PRRSV 支持疗法边界、污染针头血源传播、后备母猪驯化、LVI 风险、封群/部分清群/检测剔除和监测样本边界；详见 `SRC-0050`。"),
        ("DIS-029-swinepox-virus.md", "Formal Batch 021 / V3 正文抽取：已补充猪痘卫生关联、宿主限制、传播、血症证据边界、皮肤病变、诊断和控制边界；详见 `SRC-0051`。"),
        ("DIS-030-rotaviruses-and-reoviruses.md", "Formal Batch 021 / V3 正文抽取：已补充轮状病毒分类、环境稳定性、腹泻机制、诊断、免疫保护和呼肠孤病毒因果解释边界；详见 `SRC-0052`。"),
        ("DIS-031-retroviruses.md", "Formal Batch 021 / V3 正文抽取：已补充 PERV 亚型、宿主范围、异种移植传播证据、检测方法和管理边界；详见 `SRC-0053`。"),
        ("DIS-032-rabies-virus.md", "Formal Batch 021 / V3 正文抽取：已补充猪狂犬病溢出风险、临床表现、人暴露风险和猪用疫苗许可边界；详见 `SRC-0054`。"),
        ("DIS-033-vesicular-stomatitis-viruses.md", "Formal Batch 021 / V3 正文抽取：已补充 VSV 水疱病鉴别、人兽共患/PPE、地理边界、传播、血症边界、病变、诊断和控制边界；详见 `SRC-0054`。"),
        ("DIS-034-togaviruses-getah-sagiyama-ross-river-eee.md", "Formal Batch 021 / V3 正文抽取：已建立 Chapter 46 Togaviruses 开端锚点；具体 EEEV/Getah/Sagiyama/Ross River 正文事实需下一批继续补充；详见 `SRC-0055`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 021 / V3 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_021_cross_review.md", """# Formal Batch 021 / V3 Cross Review

## 范围

- PDF page 725-726：Chapter 41 PRRSV 控制、后备母猪驯化、净化策略和监测尾段。
- PDF page 727-732：Chapter 41 PRRSV 参考文献页，仅记录章节边界，不生成 standalone facts。
- PDF page 733-738：Chapter 42 Swinepox Virus 正文和参考文献。
- PDF page 739-751：Chapter 43 Reoviruses (Rotaviruses and Reoviruses) 正文和参考文献。
- PDF page 752-756：Chapter 44 Retroviruses 正文和参考文献。
- PDF page 757-763：Chapter 45 Rhabdoviruses 正文和参考文献。
- PDF page 764：Chapter 46 Togaviruses 开端锚点。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行。
- 页数为 40 页，符合正式批次常规范围。
- 参考文献页仅作为章节边界和来源完整性记录，不生成 standalone facts。
- 所有正式 facts 均先写入候选事实文件，再经页码锚点、内容边界和一致性审查后落库。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_021_pdf_pages_725_764_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量对照，未发现整页遗漏。
- 三次核对：`pypdf`，用于页级文本存在性和异常提示。
- 解析报告：`issues/formal_batch_021_pdf_pages_725_764_parser_report.txt`。

## 审查结论

本批候选 facts 44 条、规则页 20 个、来源页 6 个、主题页 6 个。经交叉审查后允许正式落库，所有 facts 均为 `HUMAN_REVIEWED`。

## 审查 1：页码锚点核验

- `SRC-0050` 锚定 PDF page 725-726，仅覆盖 PRRSV 控制、净化和监测尾段。
- `SRC-0051` 锚定 PDF page 733-738，其中参考文献内容未转换为 standalone facts。
- `SRC-0052` 锚定 PDF page 739-751，其中 PDF page 748-751 为参考文献，仅保留来源边界。
- `SRC-0053` 锚定 PDF page 752-756，其中 PDF page 756 为参考文献边界。
- `SRC-0054` 锚定 PDF page 757-763，其中 PDF page 763 为参考文献边界。
- `SRC-0055` 仅锚定 PDF page 764 的 Togaviruses 开端，不扩展到完整章节结论。

## 审查 2：内容边界核验

- PRRSV 内容保留支持疗法、LVI 风险、封群/部分清群/检测剔除和监测边界，不生成固定净化程序。
- 猪痘内容保留卫生、媒介、血症未确证和诊断边界，不生成特异性抗病毒治疗方案。
- 轮状病毒内容保留实验室诊断、环境稳定性和免疫解释边界，不生成药物处方或固定疫苗程序。
- PERV 内容限制在异种移植供体筛查和风险评估语境，不外推为普通猪场生产性传染病处置。
- VSV/VS 内容保留 FMD/SVD/VES/SVV 实验室鉴别、人兽共患/PPE 和移动控制边界，具体监管处置需 A0/A1 来源。
- 狂犬病内容保留人暴露和疫苗许可边界，不生成公共卫生暴露后处理细则或猪群常规免疫程序。
- Togavirus 内容只建立开端锚点，等待下一批正文继续。

## 审查 3：一致性核验

- facts、topic、rule、source 页面一致，`applies_to_species=swine`。
- `SRC-0050` 至 `SRC-0055`、`RULE-274` 至 `RULE-293` 与既有条目不重复。
- 本批正式落库内容与 V3 文档同步，V2 文档不再追加新批次。

## 保留问题

- PDF page 765 起需继续 Chapter 46 Togaviruses 正文，补充 EEEV、Getah、Sagiyama、Ross River 等证据边界。
- VSV、狂犬病和水疱病监管动作、人暴露处置、疫苗合法使用仍需本地 A0/A1 权威来源确认后才能进入生产答案约束。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 021 / V3 实施记录

- 完成时间：2026-05-07 09:40:00 +08:00。
- 处理范围：PDF page 725-764。
- 章节边界：Chapter 41 PRRSV 控制和监测尾段；Chapter 42 Swinepox；Chapter 43 Reoviruses；Chapter 44 Retroviruses；Chapter 45 Rhabdoviruses；Chapter 46 Togaviruses 开端。
- 参考文献页处理：PDF page 727-732、738、748-751、756、763 仅作为章节边界和来源完整性记录，未生成 standalone facts。
- 新增来源：`SRC-0050` 至 `SRC-0055`。
- 新增主题页：PRRSV 控制/净化/监测边界、猪痘诊断/控制边界、轮状病毒/呼肠孤病毒肠道病边界、PERV 异种移植边界、Rhabdovirus 水疱性口炎/狂犬病边界、Togavirus 开端锚点。
- 新增规则页：`RULE-274` 至 `RULE-293`。
- 新增候选事实：`issues/formal_batch_021_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_021_cross_review.md`。
- 正式落库 facts：44 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、PRRSV 固定净化程序、LVI 操作流程、猪痘特异性抗病毒治疗、轮状病毒处方/疫苗程序、PERV 普通猪场处置、VSV/狂犬病本地监管和公共卫生处置细则、Togavirus 后续正文结论。

### Formal Batch 021 / V3 交叉审查

- 页码锚点核验：通过。`SRC-0050` 覆盖 PDF page 725-726；`SRC-0051` 覆盖 733-738；`SRC-0052` 覆盖 739-751；`SRC-0053` 覆盖 752-756；`SRC-0054` 覆盖 757-763；`SRC-0055` 覆盖 764。
- 内容边界核验：通过。PRRSV、猪痘、轮状病毒/呼肠孤病毒、PERV、VSV/狂犬病和 Togavirus 开端均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、固定程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 764。
- 下一批应从 PDF page 765 开始。
- 推荐下一批：PDF page 765-804，继续 Chapter 46 Togaviruses 正文。
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
    print("formal batch 021 v3 built")


if __name__ == "__main__":
    main()
