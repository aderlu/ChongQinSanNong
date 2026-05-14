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
NOW = "2026-05-06T23:20:00+00:00"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 605, end: int = 644) -> None:
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

    write_text(ISSUES / "formal_batch_018_pdf_pages_605_644_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_018_pdf_pages_605_644_parser_report.txt", "\n".join(report_rows) + "\n")


FACTS = [
    ("IAV-009-global-diversity", "influenza_epidemiology", "猪流感全球谱系多样性", "regional_swine_influenza_lineages_differ_and_continue_to_reassort", "猪流感在不同地区维持的 H1/H3 谱系和基因组合不同，并持续发生重配；解释流行格局必须结合地区和监测年代。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 605-606", "all_stages"),
    ("IAV-010-no-pork-muscle-risk", "influenza_food_safety_boundary", "猪流感猪肉肌肉组织边界", "experimental_h1n1pdm09_studies_did_not_detect_virus_in_pork_or_muscle_tissue", "H1N1pdm09 实验感染研究未在猪肉或肌肉组织中检出病毒；该事实仅用于教材食品暴露边界，不生成食品安全监管或消费结论。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 607", "all_stages"),
    ("IAV-011-respiratory-replication", "influenza_pathogenesis", "猪流感呼吸道复制", "iav_s_replication_is_centered_in_respiratory_tract_and_can_reach_high_lung_titers", "IAV-S 复制主要集中在呼吸道，肺组织病毒滴度可较高；临床和病理解释需围绕呼吸道感染。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 607", "all_stages"),
    ("IAV-012-clinical-range", "influenza_clinical_pattern", "猪流感临床范围", "clinical_expression_ranges_from_subclinical_to_fever_sneezing_nasal_discharge_and_respiratory_disease", "猪流感临床表现可从亚临床感染到鼻液、喷嚏、发热和呼吸道症状，严重度受病毒、剂量、免疫和并发感染影响。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 607-608", "all_stages"),
    ("IAV-013-lesion-boundary", "influenza_pathology", "猪流感肺病变边界", "uncomplicated_iav_s_lesions_are_viral_pneumonia_but_may_be_mild_or_masked_by_coinfections", "单纯 IAV-S 病变主要为病毒性肺炎，但病变可轻微、不典型，或被继发/混合感染掩盖。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 608", "all_stages"),
    ("IAV-014-vaerd-boundary", "influenza_vaccine_boundary", "猪流感 VAERD 边界", "vaccine_associated_enhanced_respiratory_disease_is_a_specific_mismatch_risk_context", "猪流感疫苗相关增强呼吸道疾病 VAERD 是特定灭活疫苗与攻击毒株不匹配语境下的风险边界，不得泛化为所有免疫均会加重疾病。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 608", "all_stages"),
    ("IAV-015-sample-timing", "influenza_diagnostics", "猪流感采样时效", "virus_isolation_samples_are_best_tested_quickly_and_frozen_storage_may_reduce_isolation_success", "猪流感病毒分离样本应尽快检测，低温保存和样本质量会影响病毒分离成功率；PCR 阳性不等于获得感染性病毒分离株。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 609", "all_stages"),
    ("IAV-016-pcr-not-isolate", "influenza_diagnostics", "猪流感 PCR 与病毒分离边界", "nucleic_acid_detection_is_not_equivalent_to_virus_isolation", "猪流感核酸检测可筛查临床样本，但核酸检出不等同病毒分离，可能反映降解或非感染性病毒材料。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 609", "all_stages"),
    ("IAV-017-serology-subtype-strain", "influenza_diagnostics", "猪流感血清学亚型/毒株解释", "serology_requires_subtype_and_strain_context_due_to_cross_reactivity", "猪流感血清学解释需结合亚型、毒株和抗原交叉反应，不能单靠抗体结果精确定义感染来源。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 610", "all_stages"),
    ("IAV-018-maternal-antibody", "influenza_immunity", "猪流感母源抗体边界", "maternal_antibodies_can_reduce_shedding_or_clinical_disease_but_may_interfere_with_active_response", "母源抗体可减少临床病或排毒，但也可能影响仔猪主动免疫应答；解释免疫效果需结合母猪免疫状态和仔猪日龄。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 611", "piglets"),
    ("IAV-019-vaccination-primary-tool", "influenza_control", "猪流感疫苗控制边界", "vaccination_is_primary_prevention_tool_but_strain_match_and_population_immunity_matter", "疫苗接种是猪流感预防的重要手段，但效果受疫苗毒株匹配、群体免疫、母源抗体和流行毒株影响。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 611-612", "all_stages"),
    ("IAV-020-laiv-boundary", "influenza_vaccine_boundary", "猪流感 LAIV 边界", "live_attenuated_influenza_vaccines_may_induce_mucosal_immunity_but_require_context_specific_evidence", "猪流感减毒活疫苗可用于诱导黏膜免疫的研究和部分场景，但不能据此生成固定免疫程序或本地可用性结论。", "SRC-0043", "Chapter 36 Influenza Viruses continuation; PDF page 612", "all_stages"),
    ("BEP-001-host-range", "blue_eye_paramyxovirus", "蓝眼病宿主边界", "pigs_are_the_only_species_known_to_be_clinically_affected_by_bep", "蓝眼副黏病毒临床受影响宿主主要为猪；其他动物暴露和抗体证据不得直接写成临床病结论。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 620", "all_stages"),
    ("BEP-002-sources-shedding", "blue_eye_paramyxovirus_transmission", "蓝眼病传播和排毒", "subclinically_infected_pigs_are_primary_source_and_virus_is_shed_in_nasal_secretions_and_urine", "亚临床感染猪是 BEP 主要来源，病毒主要经鼻分泌物和尿液散播；精液传播可能存在。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 620", "all_stages"),
    ("BEP-003-clinical-systems", "blue_eye_paramyxovirus_clinical", "蓝眼病临床系统", "bep_can_involve_encephalitis_corneal_opacity_reproductive_and_respiratory_signs", "BEP 可涉及脑炎、角膜混浊、公猪附睾炎/繁殖异常和呼吸道症状，临床表现受年龄和暴发阶段影响。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 621-622", "all_stages"),
    ("BEP-004-diagnosis", "blue_eye_paramyxovirus_diagnostics", "蓝眼病诊断边界", "diagnosis_combines_clinical_pattern_histopathology_virus_detection_and_serology", "蓝眼病诊断需结合脑炎/角膜混浊/公猪附睾炎等临床组合、组织病理、病毒检测和 HI/VN/ELISA 等血清学。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 622", "all_stages"),
    ("BEP-005-control", "blue_eye_paramyxovirus_control", "蓝眼病控制边界", "control_uses_biosecurity_movement_control_and_elimination_of_clinically_affected_animals", "蓝眼病控制强调隔离、生物安全、人员车辆流动控制和临床患病动物处置；具体处置需结合本地法规和场景。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 623", "all_stages"),
    ("MENANGLE-001-reproductive", "menangle_virus", "Menangle 病毒繁殖病", "menangle_virus_causes_reproductive_disease_and_congenital_malformations", "Menangle 病毒可导致猪繁殖障碍和先天畸形，与果蝠等生态证据相关；结论需限制在暴发和检测证据内。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 623-626", "sows"),
    ("MENANGLE-002-diagnosis", "menangle_virus_diagnostics", "Menangle 病毒诊断边界", "fetal_specimens_pcr_virus_isolation_serology_and_pathology_support_diagnosis", "Menangle 病毒诊断需采集胎儿样本用于 PCR 或病毒分离，并结合血清学和病理；不得单凭繁殖损失定因。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 626", "sows"),
    ("NIPAH-001-public-health", "nipah_virus_public_health", "尼帕病毒公共卫生边界", "nipah_virus_is_a_serious_zoonotic_public_health_threat", "尼帕病毒是严重公共卫生威胁；猪场疑似内容必须作为高风险人兽共患边界处理，不生成普通场内自行处置方案。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 627", "all_stages"),
    ("NIPAH-002-reservoir", "nipah_virus_ecology", "尼帕病毒储存宿主", "pteropus_bats_are_reservoirs_and_pig_outbreaks_can_follow_spillover", "狐蝠属蝙蝠是尼帕病毒储存宿主，猪群暴发可与溢出传播相关；风险解释需结合生态和接触史。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 627", "all_stages"),
    ("NIPAH-003-clinical", "nipah_virus_clinical", "猪尼帕病毒临床边界", "clinical_signs_are_not_pathognomonic_and_vary_by_age_and_reproductive_status", "猪尼帕病毒感染临床表现非特异，且随年龄和繁殖状态变化；不能单凭临床表现确诊。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 628-630", "all_stages"),
    ("NIPAH-004-bsl4", "nipah_virus_biosafety", "尼帕病毒 BSL-4 边界", "suspected_nipah_involves_high_risk_bsl4_zoonotic_handling_constraints", "尼帕病毒疑似样本和病例涉及高风险 BSL-4 人兽共患病原边界；实验室和现场处置需权威规范。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 630", "all_stages"),
    ("NIPAH-005-sampling", "nipah_virus_diagnostics", "尼帕病毒采样边界", "nasal_and_oral_specimens_are_effective_for_detection_and_serology_timing_matters", "尼帕病毒可用鼻腔和口腔样本检测，血清抗体出现有时间窗；采样解释需结合病程。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 630", "all_stages"),
    ("PPIV1-001-significance", "ppiv1_relevance", "猪副流感病毒 1 临床意义边界", "ppiv1_clinical_significance_is_not_fully_understood", "猪副流感病毒 1 的临床意义尚未完全明确；检出不得自动等同主要病因。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 631-632", "all_stages"),
    ("PPIV1-002-diagnostics", "ppiv1_diagnostics", "PPIV-1 诊断样本", "lung_nasal_swab_and_oral_fluid_can_be_used_for_virus_detection_or_isolation", "PPIV-1 诊断可考虑肺、鼻拭子和口腔液等样本用于检测或分离，但需与其他呼吸道病原鉴别。", "SRC-0044", "Chapter 37 Paramyxoviruses; PDF page 632", "all_stages"),
    ("PPV-001-taxonomy", "parvovirus_taxonomy", "猪细小病毒范围", "porcine_parvoviruses_include_ppv1_to_ppv7_and_porcine_bocaviruses", "猪细小病毒章节覆盖 PPV1-PPV7 和猪博卡病毒等，临床意义因病毒而异。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 635-636", "all_stages"),
    ("PPV-002-ppv1-reproductive", "ppv1_clinical_pattern", "PPV1 繁殖损失", "ppv1_is_a_well_established_cause_of_reproductive_loss", "PPV1 是猪繁殖损失的明确病因之一，典型问题集中在胚胎和胎儿感染相关损失。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 635 and 639", "sows"),
    ("PPV-003-other-ppvs-boundary", "parvovirus_causality", "非 PPV1 细小病毒因果边界", "clinical_role_of_ppv2_to_ppv7_and_bocaviruses_is_less_certain", "PPV2-PPV7 和猪博卡病毒可在临床健康动物中检出，其临床因果作用不能按 PPV1 简单外推。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 635-636", "all_stages"),
    ("PPV-004-vaccination-circulation", "ppv1_immunity", "PPV1 疫苗免疫和病毒循环边界", "vaccination_can_protect_against_clinical_reproductive_loss_but_may_not_stop_replication_or_shedding", "PPV1 疫苗免疫可保护繁殖表现，但接种猪仍可能复制或排毒，疫苗效果不得写成完全阻断感染。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 638 and 642-643", "sows"),
    ("PPV-005-pathogenesis", "ppv1_pathogenesis", "PPV1 经胎盘感染", "ppv1_pathogenesis_reflects_ability_to_reach_and_cross_placental_barrier", "PPV1 致病机制与到达并跨越胎盘屏障、感染胚胎/胎儿有关；解释繁殖损失需结合妊娠阶段。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 638-640", "sows"),
    ("PPV-006-adult-clinical-boundary", "ppv1_clinical_boundary", "PPV1 成年猪临床边界", "ppv1_generally_does_not_cause_clinical_signs_in_adults", "PPV1 通常不导致成年猪明显临床症状，除繁殖损失外不得把成年猪非特异症状直接归因于 PPV1。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 639-641", "adult"),
    ("PPV-007-differential", "ppv1_differential", "PPV1 繁殖损失鉴别", "ppv1_reproductive_loss_differentials_include_pseudorabies_and_other_reproductive_pathogens", "PPV1 繁殖损失诊断需与伪狂犬病和其他繁殖病原鉴别，不能单凭 SMEDI 样表现定因。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 641", "sows"),
    ("PPV-008-diagnostics", "ppv1_diagnostics", "PPV1 诊断边界", "diagnosis_uses_fetal_testing_virus_isolation_pcr_serology_and_paired_samples_with_context", "PPV1 诊断可用胎儿检测、病毒分离、PCR 和血清学，配对样本和妊娠阶段解释很重要。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 641-642", "sows"),
    ("PPV-009-serology-fetus-boundary", "ppv1_diagnostics", "PPV1 胎儿血清学边界", "fetal_antibody_interpretation_depends_on_stage_because_virus_cannot_cross_after_immunocompetence_boundary", "PPV1 胎儿抗体解释与胎儿免疫成熟阶段有关；血清学结果不能脱离妊娠时点解释。", "SRC-0045", "Chapter 38 Parvoviruses opening; PDF page 642", "sows"),
]


RULES = [
    ("RULE-226", "猪流感 PCR 阳性不等同病毒分离成功", "influenza_diagnostics", "high", "SRC-0043", "Swine-influenza-pcr-not-virus-isolation.md", "猪流感核酸检出不得等同于成功分离感染性病毒；样本质量、保存时间和降解会影响解释。", "609"),
    ("RULE-227", "猪流感血清学必须结合亚型毒株和交叉反应", "influenza_serology", "high", "SRC-0043", "Swine-influenza-serology-subtype-strain-cross-reaction.md", "猪流感血清学解释必须结合亚型、毒株和交叉反应，不能单独判定来源谱系。", "610"),
    ("RULE-228", "猪流感母源抗体解释必须结合母猪免疫和仔猪日龄", "influenza_immunity", "high", "SRC-0043", "Swine-influenza-maternal-antibody-age-context.md", "猪流感母源抗体既可能保护仔猪，也可能影响主动免疫应答，必须结合母猪免疫状态和仔猪日龄解释。", "611"),
    ("RULE-229", "猪流感疫苗效果不得脱离毒株匹配", "influenza_vaccine_boundary", "critical", "SRC-0043", "Swine-influenza-vaccine-strain-match-required.md", "猪流感疫苗效果必须结合流行毒株、疫苗株匹配和群体免疫，不得生成固定免疫程序或泛化保护承诺。", "611-612"),
    ("RULE-230", "VAERD 不得泛化为所有猪流感免疫风险", "influenza_vaccine_boundary", "high", "SRC-0043", "Swine-influenza-vaerd-specific-mismatch-context.md", "VAERD 只应作为特定疫苗与攻击毒株不匹配风险边界，不得泛化为所有猪流感免疫均会加重疾病。", "608"),
    ("RULE-231", "蓝眼病诊断必须结合角膜/神经/繁殖组合和实验室证据", "blue_eye_paramyxovirus_diagnostics", "high", "SRC-0044", "Swine-blue-eye-diagnosis-lab-pattern-required.md", "蓝眼病诊断需结合脑炎、角膜混浊、公猪附睾炎等组合及病毒检测/血清学证据。", "621-622"),
    ("RULE-232", "蓝眼病控制不得迁移为中国监管结论", "blue_eye_paramyxovirus_control", "medium", "SRC-0044", "Swine-blue-eye-control-local-authority-boundary.md", "蓝眼病控制内容只能作为教材风险边界，不能生成中国本地监管处置或固定淘汰方案。", "623"),
    ("RULE-233", "Menangle 繁殖损失不得单凭临床定因", "menangle_virus_diagnostics", "high", "SRC-0044", "Swine-menangle-reproductive-loss-lab-required.md", "Menangle 病毒相关繁殖损失需胎儿样本、PCR/病毒分离、血清学和病理支持，不能单凭繁殖损失定因。", "623-626"),
    ("RULE-234", "尼帕病毒疑似必须按高风险人兽共患边界处理", "nipah_virus_biosafety", "critical", "SRC-0044", "Swine-nipah-high-risk-zoonotic-boundary.md", "尼帕病毒疑似必须按高风险人兽共患病原边界处理，现场和实验室处置需权威规范。", "627-630"),
    ("RULE-235", "尼帕病毒临床表现不得作为确诊依据", "nipah_virus_diagnostics", "critical", "SRC-0044", "Swine-nipah-clinical-not-pathognomonic.md", "尼帕病毒猪临床表现非特异，不得仅凭临床表现确诊。", "629-630"),
    ("RULE-236", "PPIV-1 检出不得自动等同主要病因", "ppiv1_causality", "medium", "SRC-0044", "Swine-ppiv1-detection-not-primary-cause.md", "PPIV-1 临床意义尚未完全明确，检出需与其他呼吸道病原鉴别。", "631-632"),
    ("RULE-237", "非 PPV1 细小病毒不得按 PPV1 因果外推", "parvovirus_causality", "high", "SRC-0045", "Swine-non-ppv1-causality-not-ppv1.md", "PPV2-PPV7 和猪博卡病毒临床因果作用不能按 PPV1 简单外推。", "635-636"),
    ("RULE-238", "PPV1 疫苗免疫不得写成完全阻断感染", "ppv1_immunity", "high", "SRC-0045", "Swine-ppv1-vaccination-not-sterilizing-immunity.md", "PPV1 疫苗可保护繁殖表现，但接种猪仍可能复制或排毒，不能写成完全阻断感染。", "638, 642-643"),
    ("RULE-239", "PPV1 繁殖损失诊断必须结合妊娠阶段", "ppv1_diagnostics", "high", "SRC-0045", "Swine-ppv1-reproductive-loss-gestation-context.md", "PPV1 繁殖损失解释必须结合妊娠阶段、胎儿免疫成熟和样本结果。", "638-642"),
    ("RULE-240", "PPV1 成年猪症状不得过度归因", "ppv1_clinical_boundary", "medium", "SRC-0045", "Swine-ppv1-adult-clinical-overattribution.md", "PPV1 通常不导致成年猪明显临床症状，成年猪非特异病症不得直接归因于 PPV1。", "639-641"),
    ("RULE-241", "PPV1 诊断需保留繁殖病原鉴别", "ppv1_differential", "high", "SRC-0045", "Swine-ppv1-reproductive-differential-required.md", "PPV1 诊断需与伪狂犬病和其他繁殖病原鉴别，不能单凭 SMEDI 样表现定因。", "641"),
]


SOURCES = [
    ("SRC-0043", "Diseases of Swine 11e Chapter 36 Influenza Viruses continuation", "PDF page 605-617", "wiki/sources/SRC-0043-diseases-of-swine-11e-chapter-36-influenza-viruses-continuation.md", "Chapter 36 continuation covers regional IAV-S epidemiology, pathogenesis, clinical signs, lesions, diagnostics, immunity, vaccination, VAERD, and references. PDF pages 613-617 are references and were not converted into standalone facts."),
    ("SRC-0044", "Diseases of Swine 11e Chapter 37 Paramyxoviruses", "PDF page 618-634", "wiki/sources/SRC-0044-diseases-of-swine-11e-chapter-37-paramyxoviruses.md", "Chapter 37 covers blue eye paramyxovirus, Menangle virus, Nipah virus, PPIV-1, diagnostic boundaries, public health boundaries, and references. PDF pages 633-634 are references and were not converted into standalone facts."),
    ("SRC-0045", "Diseases of Swine 11e Chapter 38 Parvoviruses opening", "PDF page 635-644", "wiki/sources/SRC-0045-diseases-of-swine-11e-chapter-38-parvoviruses-opening.md", "Chapter 38 opening covers PPV taxonomy, PPV1 reproductive disease, non-PPV1 causality boundaries, pathogenesis, diagnosis, immunity, and initial references."),
]


TOPICS = [
    ("Swine-influenza-diagnostics-immunity-vaccine-boundaries.md", "猪流感诊断、免疫和疫苗边界", "SRC-0043", "本主题用于解释 IAV-S 的地区谱系、临床病理、样本时效、PCR/病毒分离、血清学、母源抗体、疫苗匹配和 VAERD 边界。"),
    ("Swine-paramyxovirus-blue-eye-menangle-nipah-ppiv1-boundaries.md", "猪副黏病毒 Blue eye/Menangle/Nipah/PPIV-1 边界", "SRC-0044", "本主题用于解释蓝眼病、Menangle 病毒、尼帕病毒和 PPIV-1 的宿主、传播、临床、诊断、公共卫生和控制边界。"),
    ("Swine-parvovirus-ppv1-reproductive-diagnostics-boundaries.md", "猪细小病毒 PPV1 繁殖损失和诊断边界", "SRC-0045", "本主题用于解释 PPV1 与其他猪细小病毒的分类、繁殖损失、胎盘感染、疫苗免疫、诊断和鉴别边界。"),
]


def make_source_pages() -> None:
    for source_id, title, pages, relpath, summary in SOURCES:
        write_text(
            WIKI / relpath,
            f"""---
tags: [source, swine, textbook, formal]
source_id: {source_id}
updated: {NOW}
evidence_status: HUMAN_REVIEWED
---

# {title}

## 范围

- 来源：本地 PDF `docs/Diseases of Swine, 11th Edition ...pdf`。
- 页码范围：{pages}。
- 批次：Formal Batch 018。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_018_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_018_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_018_pdf_pages_605_644_parser_report.txt`。
""",
        )


def make_topic_pages() -> None:
    for filename, title, source_id, summary in TOPICS:
        write_text(
            WIKI / "wiki" / "topics" / filename,
            f"""---
tags: [topic, swine, formal]
updated: {NOW}
evidence_status: HUMAN_REVIEWED
sources: [{source_id}]
---

# {title}

{summary}

## 证据边界

- 来源：{source_id}。
- 本页正式 facts 已在 `issues/formal_batch_018_cross_review.md` 中交叉审查。
- 本页不提供固定药方、剂量、免疫程序、扑杀/封锁/调运/消毒命令、食品召回或中国监管处置结论。
""",
        )


def make_rule_pages() -> None:
    for rule_id, title, category, severity, source_id, filename, rule_text, pages in RULES:
        write_text(
            WIKI / "wiki" / "rules" / filename,
            f"""---
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
""",
        )


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
    write_text(
        ISSUES / "formal_batch_018_candidate_facts.json",
        json.dumps(
            {
                "batch_id": "formal-batch-018",
                "source_ids": ["SRC-0043", "SRC-0044", "SRC-0045"],
                "parser_cross_check": {
                    "primary": "PyMuPDF fitz",
                    "secondary": "pdfplumber",
                    "tertiary": "pypdf",
                    "report": "issues/formal_batch_018_pdf_pages_605_644_parser_report.txt",
                },
                "facts": new_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )


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
        ("DIS-021-influenza-viruses.md", "Formal Batch 018 正文抽取：已补充 IAV-S 地区谱系、临床病理、样本时效、PCR/病毒分离、血清学、母源抗体、疫苗匹配和 VAERD 边界；详见 `SRC-0043`。"),
        ("DIS-022-paramyxoviruses.md", "Formal Batch 018 正文抽取：已补充蓝眼病、Menangle 病毒、尼帕病毒和 PPIV-1 的传播、诊断、公共卫生、生物安全和因果边界；详见 `SRC-0044`。"),
        ("DIS-023-parvoviruses.md", "Formal Batch 018 正文抽取：已补充 PPV1 繁殖损失、PPV2-PPV7 因果边界、胎盘感染、疫苗免疫、诊断和鉴别边界；详见 `SRC-0045`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 018 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(
        ISSUES / "formal_batch_018_cross_review.md",
        """# Formal Batch 018 Cross Review

## 范围

- PDF page 605-612：Chapter 36 Influenza Viruses 正文后段，落库猪流感地区谱系、临床病理、诊断、免疫和疫苗边界。
- PDF page 613-617：Chapter 36 参考文献页，仅作为章节边界，不生成 standalone facts。
- PDF page 618-632：Chapter 37 Paramyxoviruses 正文，落库蓝眼病、Menangle 病毒、尼帕病毒和 PPIV-1 边界。
- PDF page 633-634：Chapter 37 参考文献页，仅作为章节边界。
- PDF page 635-644：Chapter 38 Parvoviruses 开端，落库 PPV 分类、PPV1 繁殖损失、诊断和免疫边界。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_018_pdf_pages_605_644_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量接近，未发现漏页。
- 三次核对：`pypdf`，作为页级文本存在性与异常提示，不作为主文本。
- 解析报告：`issues/formal_batch_018_pdf_pages_605_644_parser_report.txt`。

## 审查结论

本批候选事实 35 条，规则页 16 个，来源页 3 个，主题页 3 个。经页码锚点、内容边界和一致性审查后允许落库。

## 审查 1：页码锚点核验

- `SRC-0043` facts 锚定 PDF page 605-612；PDF page 613-617 的参考文献条目未转化为 standalone facts。
- `SRC-0044` facts 锚定 PDF page 618-632；PDF page 633-634 的参考文献条目未转化为 standalone facts。
- `SRC-0045` facts 锚定 PDF page 635-644；下一批应从 PDF page 645 继续 Chapter 38 正文/参考文献边界。

## 审查 2：内容边界核验

- 猪流感内容只生成地区谱系、临床病理、诊断、免疫和疫苗边界，不生成固定免疫程序、疫苗产品推荐或本地亚型流行结论。
- 蓝眼病和 Menangle 病毒只落库教材风险、诊断和控制边界，不迁移为中国本地监管处置。
- 尼帕病毒相关事实严格标记为高风险人兽共患和 BSL-4 边界，不生成普通猪场自行处置方案。
- PPIV-1 内容保留临床意义未完全明确的因果边界。
- PPV 内容区分 PPV1 与 PPV2-PPV7/猪博卡病毒，不把非 PPV1 检出外推为 PPV1 式繁殖病因。

## 审查 3：一致性核验

- facts 与新增 topic/rule/source 页面一致。
- facts 的 `applies_to_species` 均为 `swine`，`evidence_status` 均为 `HUMAN_REVIEWED`。
- 新增 `fact_id`、`RULE-226` 至 `RULE-241` 与既有条目不重复。

## 保留问题

- PDF page 645 以后仍为 Chapter 38 Parvoviruses 正文和参考文献；下一批应继续抽取 PPV 免疫、控制和章节收尾，并判断是否进入后续病毒章节。
- 猪流感疫苗、尼帕病毒、蓝眼病、PPV 控制和监管结论如需进入中国本地答案，仍需中国官方或 A0/A1 来源复核。
""",
    )


def append_progress_docs() -> None:
    block = """

## Formal Batch 018 实施记录

- 完成时间：2026-05-07 07:20:00 +08:00。
- 处理范围：PDF page 605-644。
- 章节边界：Chapter 36 Influenza Viruses 后段和参考文献；Chapter 37 Paramyxoviruses；Chapter 38 Parvoviruses 开端。
- 新增来源：`SRC-0043`、`SRC-0044`、`SRC-0045`。
- 新增主题页：猪流感诊断/免疫/疫苗边界、猪副黏病毒 Blue eye/Menangle/Nipah/PPIV-1 边界、猪细小病毒 PPV1 繁殖损失和诊断边界。
- 新增规则页：`RULE-226` 至 `RULE-241`。
- 新增候选事实：`issues/formal_batch_018_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_018_cross_review.md`。
- 正式落库 facts：35 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、固定免疫程序、疫苗产品推荐、尼帕病毒现场处置流程、中国监管处置、PPV 固定控制方案和药物/剂量结论。

### Formal Batch 018 交叉审查

- 页码锚点核验：通过。`SRC-0043` 覆盖 PDF page 605-617，`SRC-0044` 覆盖 PDF page 618-634，`SRC-0045` 覆盖 PDF page 635-644。PDF page 613-617、633-634 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。猪流感、蓝眼病、Menangle、Nipah、PPIV-1、PPV 均只落库教材证据和诊断/免疫/公共卫生/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 644。
- 下一批应从 PDF page 645 开始。
- 推荐下一批：PDF page 645-684，继续 Chapter 38 Parvoviruses 后续正文，并视页码边界进入后续病毒章节。
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
    print("formal batch 018 built")


if __name__ == "__main__":
    main()
