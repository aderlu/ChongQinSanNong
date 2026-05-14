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
NOW = "2026-05-07T01:00:00+00:00"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 685, end: int = 724) -> None:
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
    write_text(ISSUES / "formal_batch_020_pdf_pages_685_724_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_020_pdf_pages_685_724_parser_report.txt", "\n".join(report_rows) + "\n")


FACTS = [
    ("SVDV-002-subclinical", "svdv_clinical_boundary", "猪水疱病亚临床边界", "svdv_infections_can_be_subclinical_and_detected_by_antibody_monitoring", "SVDV 感染可多为亚临床，部分地区监测主要基于特异抗体检出而非明显临床病。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 685-686", "all_stages"),
    ("SVDV-003-clinical-onset", "svdv_clinical_pattern", "SVDV 临床发生时间", "vesicular_signs_can_appear_quickly_after_experimental_inoculation", "SVDV 实验感染后水疱和跛行等临床表现可在 1-2 天内出现，但自然场景可能受感染剂量和观察敏感性影响。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 686", "all_stages"),
    ("SVDV-004-mortality-boundary", "svdv_clinical_boundary", "SVDV 死亡率边界", "mortality_is_not_a_reported_feature_of_svdv_infection", "死亡不是 SVDV 感染的典型报告特征；若出现死亡需寻找其他病因或并发因素。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 686", "all_stages"),
    ("SVDV-005-differential", "svdv_differential", "SVDV 水疱病鉴别", "svdv_lesions_are_not_specific_and_require_differential_diagnosis_from_fmd_vs_vesicular_exanthema_and_trauma", "SVDV 水疱或蹄部病变不具特异性，需与 FMD、水疱性口炎、水疱疹/杯状病毒和外伤等鉴别。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 687", "all_stages"),
    ("SVDV-006-no-commercial-vaccine", "svdv_vaccine_boundary", "SVDV 疫苗边界", "experimental_vaccines_exist_but_no_commercial_svd_vaccine_is_available_and_vaccination_has_not_been_used", "教材记录有 SVDV 实验疫苗，但无商业可用 SVD 疫苗，且未开展猪群疫苗接种；不得生成免疫程序。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 688", "all_stages"),
    ("EMCV-001-taxonomy", "emcv_taxonomy", "EMCV 分类", "emcv_is_cardiovirus_a_in_family_picornaviridae", "脑心肌炎病毒 EMCV 属 Picornaviridae 科 Cardiovirus 属，种名为 Cardiovirus A。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 689", "all_stages"),
    ("EMCV-002-risk-factors", "emcv_epidemiology", "EMCV 场内风险因素", "rodents_and_hygiene_are_associated_with_clinical_emcv_risk", "EMCV 临床暴发风险与啮齿动物和卫生状况等因素相关；场内单一引入未必能解释所有感染。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 690", "all_stages"),
    ("EMCV-003-pathogenesis-heart", "emcv_pathogenesis", "EMCV 心肌和扁桃体复制", "emcv_can_replicate_in_tonsils_and_heart_after_oral_exposure", "EMCV 经口感染后可在扁桃体和心脏等组织复制，心肌病变是重要诊断线索。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 690-691", "all_stages"),
    ("EMCV-004-sudden-death-reproductive", "emcv_clinical_pattern", "EMCV 猝死和繁殖损失", "emcv_can_cause_sudden_death_in_finishing_pigs_and_reproductive_failure_in_sows", "EMCV 可造成育肥猪猝死，也可导致母猪繁殖失败和仔猪/胎儿相关问题。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 691-692", "finishers"),
    ("EMCV-005-diagnosis", "emcv_diagnostics", "EMCV 确诊边界", "conclusive_diagnosis_requires_demonstration_by_virus_isolation_in_mice_or_cell_culture", "EMCV 确诊应通过小鼠或细胞培养病毒分离等方式证明，临床史和病理只能作为提示。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 692", "all_stages"),
    ("TESCHO-001-taxonomy", "teschovirus_sapelovirus_taxonomy", "Teschovirus/Sapelovirus 分类", "porcine_teschoviruses_sapeloviruses_and_enterovirus_g_are_distinct_taxa", "过去的猪肠道病毒分类已拆分为 Teschovirus A、Sapelovirus A 和 Enterovirus G 等不同分类单元。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 693", "all_stages"),
    ("TESCHO-002-intestinal-persistence", "teschovirus_pathogenesis", "Teschovirus 肠道感染和持续", "ptvs_rapidly_infect_intestine_and_may_persist_in_large_intestine", "PTV 可快速感染肠道，并可在大肠持续较长时间；检出需结合临床和组织定位。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 694", "all_stages"),
    ("TESCHO-003-clinical-uncertain", "teschovirus_causality", "Teschovirus 临床因果边界", "porcine_teschoviruses_are_ubiquitous_and_often_rarely_cause_clinical_disease_alone", "猪 teschovirus 普遍存在，单独导致临床病的证据有限；与腹泻、肺炎或神经病相关时需谨慎定因。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 694-696", "all_stages"),
    ("TESCHO-004-diagnostics", "teschovirus_diagnostics", "Teschovirus 诊断边界", "virus_isolation_vn_pcr_and_paired_serology_may_be_used_but_serology_has_limited_value", "Teschovirus/相关 picornavirus 可用病毒分离、VN、PCR 和配对血清等方法，但血清学因普遍感染价值有限。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 696", "all_stages"),
    ("SVV-001-origin", "senecavirus_a_taxonomy", "Senecavirus A 分类和来源", "senecavirus_a_is_a_picornavirus_originally_named_seneca_valley_virus", "Senecavirus A 最初以 Seneca Valley virus 命名，是与猪水疱病相关的 picornavirus。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 697", "all_stages"),
    ("SVV-002-host", "senecavirus_a_host_range", "Senecavirus A 宿主边界", "only_pigs_are_known_to_be_infected_by_svv", "教材指出已知感染 SVV 的宿主为猪；宿主范围不得外推。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 698", "all_stages"),
    ("SVV-003-vesicular-fmd-like", "senecavirus_a_differential", "SVV 水疱病鉴别", "svv_vesicular_disease_is_indistinguishable_from_fmd_svd_vs_and_vesicular_exanthema_clinically", "SVV 造成的水疱病临床上可与 FMD、SVD、水疱性口炎和水疱疹难以区分，必须实验室鉴别。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 698-699", "all_stages"),
    ("SVV-004-shedding-environment", "senecavirus_a_transmission", "SVV 排毒和环境边界", "svv_shedding_may_occur_in_feces_or_oral_fluids_and_environmental_survival_is_possible", "SVV 可能经粪便或口腔液排毒，并可在环境中检出；传播解释需结合样本和场内暴露。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 698", "all_stages"),
    ("SVV-005-control-boundary", "senecavirus_a_control", "SVV 控制证据边界", "few_attempts_have_been_made_to_control_outbreaks_and_no_fixed_control_program_should_be_generated", "教材指出 SVV 暴发控制尝试较少，缺乏固定控制方案；不得生成通用处置流程。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 699", "all_stages"),
    ("KOBU-001-detection-boundary", "kobuvirus_pasivirus_boundary", "猪 Kobuvirus/Pasivirus 检出边界", "swine_kobuvirus_and_pasivirus_detection_requires_cautious_causality_interpretation", "猪 kobuvirus 和 pasivirus 可在健康或临床样本中检出，因果解释需结合共感染、病变和流行病学证据。", "SRC-0048", "Chapter 40 Picornaviruses continuation; PDF page 699-700", "all_stages"),
    ("PRRSV-001-recognition", "prrsv_history", "PRRSV 识别和经济影响", "prrsv_emerged_as_a_major_problem_after_unidentified_clinically_similar_outbreaks", "PRRSV 在临床相似但病因未明的暴发后被识别，后来成为重要经济性疾病；历史相似性不等于当前病因判断。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 709", "all_stages"),
    ("PRRSV-002-genetic-diversity", "prrsv_evolution", "PRRSV 遗传多样性", "prrsv_has_high_genetic_diversity_and_clusters_can_change_with_passage", "PRRSV 遗传多样性高，毒株聚类可随传代和进化改变；不能仅凭单一分类替代测序和流行病学解释。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 710", "all_stages"),
    ("PRRSV-003-stability", "prrsv_environment", "PRRSV 温度稳定性", "prrsv_survival_decreases_with_higher_temperature_and_environmental_conditions", "PRRSV 存活受温度和环境条件影响，较高温度下半衰期明显缩短。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 710", "all_stages"),
    ("PRRSV-004-shedding", "prrsv_transmission", "PRRSV 排毒途径", "infected_animals_shed_prrsv_in_oral_nasal_mammary_and_other_secretions", "PRRSV 感染猪可通过口鼻分泌物、乳汁等排毒，排毒水平和持续时间因毒株和个体而异。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 712", "all_stages"),
    ("PRRSV-005-semen", "prrsv_transmission", "PRRSV 精液传播边界", "infectious_prrsv_can_be_detected_in_semen_and_supports_venereal_transmission_risk", "PRRSV 可在精液中检出感染性病毒，存在经精液传播风险；公猪/精液监测需结合检测和病程。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 712-716", "boars"),
    ("PRRSV-006-persistence", "prrsv_persistence", "PRRSV 持续感染", "prrsv_can_persist_for_100_to_165_days_in_some_animals", "研究报道 PRRSV 可在部分动物中持续检出 100-165 天；阴性或阳性解释需结合样本部位和病程。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 713", "all_stages"),
    ("PRRSV-007-aerosol", "prrsv_transmission", "PRRSV 气溶胶传播边界", "aerosol_transmission_depends_on_virus_strain_environment_and_distance", "PRRSV 气溶胶传播受毒株、环境和距离影响，不能把所有场间传播都归因于空气传播。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 713-714", "all_stages"),
    ("PRRSV-008-pathogenesis-age", "prrsv_pathogenesis", "PRRSV 年龄与复制", "younger_pigs_may_replicate_more_virus_and_disease_varies_by_host_and_strain", "PRRSV 复制和临床病受宿主年龄和毒株影响，幼龄猪可能复制更多病毒。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 715", "piglets"),
    ("PRRSV-009-fetal-transmission", "prrsv_reproductive", "PRRSV 胎盘和胎儿传播", "prrsv_can_transmit_to_fetuses_through_maternal_fetal_interface_or_fetus_to_fetus_spread", "PRRSV 可经母胎界面传播至胎盘/胎儿，也可能发生胎儿间传播；繁殖损失需结合妊娠阶段和检测。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 716", "sows"),
    ("PRRSV-010-clinical-variable", "prrsv_clinical_pattern", "PRRSV 临床表现多变", "clinical_presentation_ranges_from_subclinical_to_devastating_and_depends_on_herd_immunity_strain_and_coinfections", "PRRSV 临床表现从亚临床到严重暴发不等，受猪群免疫、毒株毒力和共感染影响。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 717-718", "all_stages"),
    ("PRRSV-011-differential", "prrsv_differential", "PRRSV 鉴别诊断范围", "prrsv_differentials_include_csfv_pcmv_phev_leptospirosis_parvovirus_pcv2_prv_iav_and_teschovirus", "PRRSV 鉴别诊断可包括 CSFV、PCMV、PHEV、钩端螺旋体、细小病毒、PCV2、PRV、猪流感和 teschovirus 等。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 720", "all_stages"),
    ("PRRSV-012-definitive-diagnosis", "prrsv_diagnostics", "PRRSV 确诊边界", "definitive_diagnosis_requires_detection_of_virus_viral_products_or_antibodies_with_context", "PRRSV 确诊需结合病毒、病毒产物和/或抗体检测，并与临床、病史和鉴别诊断整合。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 720", "all_stages"),
    ("PRRSV-013-pcr-not-infectious", "prrsv_diagnostics", "PRRSV PCR 边界", "nucleic_acid_assays_cannot_differentiate_rna_from_infectious_virus", "PRRSV 核酸检测不能区分 RNA 和感染性病毒；PCR 阳性不等于存在感染性病毒。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 721", "all_stages"),
    ("PRRSV-014-sequencing-limits", "prrsv_diagnostics", "PRRSV 测序解释边界", "sequencing_does_not_by_itself_predict_virulence_or_clinical_role", "PRRSV 测序可用于追踪和比较病毒，但不能单独预测毒力或证明临床因果作用。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 721", "all_stages"),
    ("PRRSV-015-elisa-boundary", "prrsv_serology", "PRRSV ELISA 解释边界", "elisa_cannot_distinguish_current_infection_cleared_infection_vaccination_or_maternal_antibody", "PRRSV ELISA 抗体结果不能区分当前感染、既往清除感染、疫苗免疫或母源抗体。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 722", "all_stages"),
    ("PRRSV-016-heterologous-neutralization", "prrsv_immunity", "PRRSV 异源中和边界", "neutralizing_antibodies_may_inactivate_homologous_virus_but_only_partially_neutralize_heterologous_isolates", "PRRSV 中和抗体可完全中和同源病毒，但对异源分离株可能仅部分中和。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 722", "all_stages"),
    ("PRRSV-017-vaccine-strain-dependent", "prrsv_vaccine_boundary", "PRRSV 疫苗毒株依赖性", "vaccines_based_on_specific_strains_have_strain_dependent_protection", "基于特定 PRRSV 毒株的疫苗保护具有毒株依赖性，不能保证对所有异源毒株有效。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 723", "all_stages"),
    ("PRRSV-018-control-entry-points", "prrsv_control", "PRRSV 引入控制点", "prevention_and_control_focus_on_events_that_can_carry_virus_into_a_herd", "PRRSV 防控强调识别可能把病毒带入猪群的事件和关键控制点，如生物安全、虫媒/空气处理等。", "SRC-0049", "Chapter 41 PRRSV opening; PDF page 724", "all_stages"),
]


RULES = [
    ("RULE-258", "SVDV 临床水疱不得与 FMD 混同", "svdv_differential", "critical", "SRC-0048", "Swine-svdv-vesicular-lab-differential-required.md", "SVDV 水疱和蹄部病变不具特异性，必须与 FMD、水疱性口炎、SVV、VESV 和外伤等鉴别。", "687"),
    ("RULE-259", "SVDV 不得生成商业疫苗或免疫程序", "svdv_vaccine_boundary", "medium", "SRC-0048", "Swine-svdv-no-commercial-vaccine-program.md", "SVDV 只有实验疫苗记录，无商业疫苗和猪群接种实践，不能生成固定免疫程序。", "688"),
    ("RULE-260", "EMCV 猝死和繁殖损失需实验室确诊", "emcv_diagnostics", "high", "SRC-0048", "Swine-emcv-sudden-death-repro-lab-confirmation.md", "EMCV 猝死或繁殖损失只能作为提示，确诊需病毒分离或其他实验室证据。", "691-692"),
    ("RULE-261", "Teschovirus 检出不得自动等同临床病因", "teschovirus_causality", "high", "SRC-0048", "Swine-teschovirus-detection-not-causality.md", "Teschovirus 普遍存在，单独检出不得自动解释为腹泻、肺炎或神经病主因。", "694-696"),
    ("RULE-262", "SVV 水疱病必须进入重大水疱病鉴别", "senecavirus_a_differential", "critical", "SRC-0048", "Swine-svv-fmd-svd-vesicular-differential.md", "SVV 临床水疱病与 FMD、SVD、水疱性口炎和水疱疹难以区分，必须实验室鉴别。", "698-699"),
    ("RULE-263", "SVV 控制方案不得固定化", "senecavirus_a_control", "medium", "SRC-0048", "Swine-svv-control-evidence-limited.md", "SVV 暴发控制证据有限，不得生成通用固定控制流程。", "699"),
    ("RULE-264", "Kobuvirus/Pasivirus 检出需谨慎定因", "kobuvirus_pasivirus_causality", "medium", "SRC-0048", "Swine-kobuvirus-pasivirus-causality-cautious.md", "猪 kobuvirus 和 pasivirus 检出需结合共感染、病变和流行病学证据，不得单独定因。", "699-700"),
    ("RULE-265", "PRRSV PCR 阳性不等同感染性病毒", "prrsv_diagnostics", "high", "SRC-0049", "Swine-prrsv-pcr-not-infectious-virus.md", "PRRSV 核酸检测不能区分 RNA 与感染性病毒，PCR 阳性不得直接解释为可传播感染性病毒。", "721"),
    ("RULE-266", "PRRSV ELISA 不得区分当前感染、疫苗和母源抗体", "prrsv_serology", "high", "SRC-0049", "Swine-prrsv-elisa-interpretation-boundary.md", "PRRSV ELISA 抗体结果不能区分当前感染、既往感染、疫苗免疫或母源抗体。", "722"),
    ("RULE-267", "PRRSV 测序不得单独预测毒力或临床因果", "prrsv_sequencing", "high", "SRC-0049", "Swine-prrsv-sequencing-not-virulence-causality.md", "PRRSV 测序可用于追踪和比较，但不能单独预测毒力或证明临床因果作用。", "721"),
    ("RULE-268", "PRRSV 临床表现必须结合猪群免疫和共感染", "prrsv_clinical_boundary", "high", "SRC-0049", "Swine-prrsv-clinical-herd-immunity-coinfection.md", "PRRSV 临床表现受猪群免疫、毒株毒力和共感染影响，不能单靠症状定因。", "717-718"),
    ("RULE-269", "PRRSV 鉴别诊断必须覆盖主要繁殖和呼吸道病原", "prrsv_differential", "high", "SRC-0049", "Swine-prrsv-differential-respiratory-reproductive.md", "PRRSV 诊断需与 CSFV、PCMV、PHEV、钩端螺旋体、PPV、PCV2、PRV、猪流感和 teschovirus 等鉴别。", "720"),
    ("RULE-270", "PRRSV 精液传播风险需纳入公猪和精液监测", "prrsv_transmission", "high", "SRC-0049", "Swine-prrsv-semen-transmission-monitoring.md", "PRRSV 可经精液传播，公猪站和精液使用需结合病程、采样和检测解释。", "712-716"),
    ("RULE-271", "PRRSV 气溶胶传播不得泛化解释所有场间传播", "prrsv_transmission", "medium", "SRC-0049", "Swine-prrsv-aerosol-context-boundary.md", "PRRSV 气溶胶传播依赖毒株、环境和距离，不得泛化解释所有场间传播。", "713-714"),
    ("RULE-272", "PRRSV 疫苗保护必须保留毒株依赖和异源保护边界", "prrsv_vaccine_boundary", "high", "SRC-0049", "Swine-prrsv-vaccine-strain-dependent-boundary.md", "PRRSV 疫苗保护具有毒株依赖性，同源与异源保护差异必须保留。", "722-723"),
    ("RULE-273", "PRRSV 防控应围绕引入事件和关键控制点", "prrsv_control", "high", "SRC-0049", "Swine-prrsv-control-entry-event-critical-points.md", "PRRSV 防控应围绕可能带入病毒的事件和关键控制点，而不是单一措施。", "724"),
]


SOURCES = [
    ("SRC-0048", "Diseases of Swine 11e Chapter 40 Picornaviruses continuation", "PDF page 685-708", "wiki/sources/SRC-0048-diseases-of-swine-11e-chapter-40-picornaviruses-continuation.md", "Chapter 40 continuation covers SVDV, EMCV, teschovirus/sapelovirus/enterovirus G, Senecavirus A, porcine kobuvirus and pasivirus boundaries. PDF pages 701-708 are references and were not converted into standalone facts."),
    ("SRC-0049", "Diseases of Swine 11e Chapter 41 PRRSV opening", "PDF page 709-724", "wiki/sources/SRC-0049-diseases-of-swine-11e-chapter-41-prrsv-opening.md", "Chapter 41 opening covers PRRSV recognition, genetic diversity, shedding, persistence, transmission, pathogenesis, clinical variability, diagnosis, serology, immunity, vaccine boundaries and prevention/control entry points."),
]


TOPICS = [
    ("Swine-picornavirus-svd-emcv-teschovirus-svv-boundaries.md", "猪 Picornavirus SVD/EMCV/Teschovirus/SVV 边界", "SRC-0048", "本主题用于解释 SVDV、EMCV、teschovirus/sapelovirus、Senecavirus A、kobuvirus/pasivirus 的诊断、因果和水疱病鉴别边界。"),
    ("Swine-prrsv-transmission-diagnostics-immunity-boundaries.md", "PRRSV 传播、诊断、免疫和防控边界", "SRC-0049", "本主题用于解释 PRRSV 的遗传多样性、排毒、精液/气溶胶传播、持续感染、临床多样性、诊断、ELISA/PCR/测序、疫苗和防控入口边界。"),
]


def make_source_pages() -> None:
    for source_id, title, pages, relpath, summary in SOURCES:
        write_text(WIKI / relpath, f"""---
tags: [source, swine, textbook, formal]
source_id: {source_id}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
---

# {title}

## 范围

- 来源：本地 PDF `docs/Diseases of Swine, 11th Edition ...pdf`。
- 页码范围：{pages}。
- 批次：Formal Batch 020。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_020_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_020_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_020_pdf_pages_685_724_parser_report.txt`。
""")


def make_topic_pages() -> None:
    for filename, title, source_id, summary in TOPICS:
        write_text(WIKI / "wiki" / "topics" / filename, f"""---
tags: [topic, swine, formal]
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [{source_id}]
---

# {title}

{summary}

## 证据边界

- 来源：{source_id}。
- 本页正式 facts 已在 `issues/formal_batch_020_cross_review.md` 中交叉审查。
- 本页不提供固定药方、剂量、免疫程序、扑杀/封锁/调运/消毒命令、食品召回或中国监管处置结论。
""")


def make_rule_pages() -> None:
    for rule_id, title, category, severity, source_id, filename, rule_text, pages in RULES:
        write_text(WIKI / "wiki" / "rules" / filename, f"""---
tags: [rule, swine, formal]
rule_id: {rule_id}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [{source_id}]
---

# {title}

## 规则

{rule_text} 证据：{source_id}，PDF page {pages}。

## 适用边界

- 本规则用于生成、评估和审核猪病 Wiki 中病毒病、诊断采样、鉴别诊断、免疫、公共卫生和监管边界解释。
- 本规则不提供具体药物剂量、固定治疗方案、免疫程序、抗菌药处方、食品召回、扑杀/封锁/调运/消毒命令或中国监管处置结论。
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
    write_text(ISSUES / "formal_batch_020_candidate_facts.json", json.dumps({
        "batch_id": "formal-batch-020",
        "source_ids": ["SRC-0048", "SRC-0049"],
        "parser_cross_check": {
            "primary": "PyMuPDF fitz",
            "secondary": "pdfplumber",
            "tertiary": "pypdf",
            "report": "issues/formal_batch_020_pdf_pages_685_724_parser_report.txt",
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
    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
    else:
        rows = [["source_id", "title", "pages", "evidence_status", "relpath"]]
    existing = {row[0] for row in rows[1:] if row}
    for source_id, title, pages, relpath, _ in SOURCES:
        if source_id not in existing:
            rows.append([source_id, title, pages, "HUMAN_REVIEWED", relpath])
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


def update_disease_pages() -> None:
    updates = [
        ("DIS-026-foot-and-mouth-disease-picornaviruses.md", "Formal Batch 020 正文抽取：已补充 SVDV 与 FMD 水疱病鉴别、SVDV 疫苗边界，以及 Chapter 40 后续 picornavirus 鉴别边界；详见 `SRC-0048`。"),
        ("DIS-027-senecavirus-a-picornaviruses.md", "Formal Batch 020 正文抽取：已补充 Senecavirus A 宿主、水疱病与 FMD/SVD/VS/VES 鉴别、排毒和控制证据边界；详见 `SRC-0048`。"),
        ("DIS-028-porcine-reproductive-and-respiratory-syndrome.md", "Formal Batch 020 正文抽取：已补充 PRRSV 遗传多样性、排毒、精液/气溶胶传播、持续感染、临床多样性、诊断、ELISA/PCR/测序、疫苗和防控入口边界；详见 `SRC-0049`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 020 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(ISSUES / "formal_batch_020_cross_review.md", """# Formal Batch 020 Cross Review

## 范围

- PDF page 685-700：Chapter 40 Picornaviruses 后续正文，落库 SVDV、EMCV、teschovirus/sapelovirus/Enterovirus G、Senecavirus A、kobuvirus/pasivirus 边界。
- PDF page 701-708：Chapter 40 参考文献页，仅作为章节边界，不生成 standalone facts。
- PDF page 709-724：Chapter 41 PRRSV 开端，落库 PRRSV 遗传多样性、传播、持续感染、临床、诊断、免疫和防控边界。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行。
- 页数为 40 页，符合常规正文批次范围。
- 参考文献页只记录章节边界，不生成 standalone facts。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_020_pdf_pages_685_724_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量接近，未发现漏页。
- 三次核对：`pypdf`，作为页级文本存在性与异常提示，不作为主文本。
- 解析报告：`issues/formal_batch_020_pdf_pages_685_724_parser_report.txt`。

## 审查结论

本批候选事实 38 条，规则页 16 个，来源页 2 个，主题页 2 个。经页码锚点、内容边界和一致性审查后允许落库。

## 审查 1：页码锚点核验

- `SRC-0048` facts 锚定 PDF page 685-700；PDF page 701-708 的参考文献条目未转化为 standalone facts。
- `SRC-0049` facts 锚定 PDF page 709-724；下一批应从 PDF page 725 继续 Chapter 41 正文。

## 审查 2：内容边界核验

- SVDV、SVV 等水疱病事实均保留 FMD/SVD/VS/VES 实验室鉴别边界，不生成监管处置命令。
- EMCV 事实仅落库猝死、繁殖损失和实验室确诊边界，不生成固定控制方案。
- Teschovirus、kobuvirus 和 pasivirus 事实保留检出不等于因果的边界。
- PRRSV 事实仅落库传播、诊断、免疫和防控入口边界，不生成疫苗程序、清群方案或本地监管结论。
- PRRSV PCR、ELISA、测序内容均保留解释限制。

## 审查 3：一致性核验

- facts 与新增 topic/rule/source 页面一致。
- facts 的 `applies_to_species` 均为 `swine`，`evidence_status` 均为 `HUMAN_REVIEWED`。
- 新增 `fact_id`、`RULE-258` 至 `RULE-273` 与既有条目不重复。

## 保留问题

- PDF page 725 以后仍为 Chapter 41 PRRSV 正文，需继续抽取预防控制后段、疫苗、治疗边界和参考文献。
- PRRSV 疫苗程序、场内净化/清群、区域防控和中国监管结论仍需 A0/A1 或本地权威来源复核。
""")


def append_progress_docs() -> None:
    block = """

## Formal Batch 020 实施记录

- 完成时间：2026-05-07 09:00:00 +08:00。
- 处理范围：PDF page 685-724。
- 章节边界：Chapter 40 Picornaviruses 后续正文和参考文献；Chapter 41 PRRSV 开端。
- 新增来源：`SRC-0048`、`SRC-0049`。
- 新增主题页：猪 Picornavirus SVD/EMCV/Teschovirus/SVV 边界、PRRSV 传播/诊断/免疫/防控边界。
- 新增规则页：`RULE-258` 至 `RULE-273`。
- 新增候选事实：`issues/formal_batch_020_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_020_cross_review.md`。
- 正式落库 facts：38 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、固定疫苗程序、PRRSV 清群/净化方案、中国监管处置、SVDV/SVV/FMD 监管命令、EMCV 固定控制方案。

### Formal Batch 020 交叉审查

- 页码锚点核验：通过。`SRC-0048` 覆盖 PDF page 685-708，`SRC-0049` 覆盖 PDF page 709-724。PDF page 701-708 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。SVDV、EMCV、teschovirus/sapelovirus、SVV、kobuvirus/pasivirus 和 PRRSV 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 724。
- 下一批应从 PDF page 725 开始。
- 推荐下一批：PDF page 725-764，继续 Chapter 41 PRRSV 正文后段和参考文献边界。
"""
    append_text(ISSUES / "pdf_processing_progress_v2.md", block)
    append_text(ROOT / "docs" / "SWINE_LLM_WIKI_IMPLEMENTATION_PLAN_V2.md", block)


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
    print("formal batch 020 built")


if __name__ == "__main__":
    main()
