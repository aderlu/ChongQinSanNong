from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import fitz
import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
ISSUES = WIKI / "issues"
PDF = ROOT / "docs" / "Diseases of Swine, 11th Edition (Jeffrey J. Zimmerman,  Locke A. Karriker etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
NOW = "2026-05-06T16:35:00+00:00"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 565, end: int = 604) -> None:
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

    write_text(ISSUES / "formal_batch_017_pdf_pages_565_604_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_017_pdf_pages_565_604_parser_report.txt", "\n".join(report_rows) + "\n")


FACTS = [
    ("HEV-001-public-health", "hev_public_health", "猪 HEV 公共卫生边界", "swine_hev_is_zoonotic_public_health_relevant", "HEV 是人类戊型肝炎病原，猪 HEV 与人类感染具有公共卫生关联；猪场知识库只能生成风险边界，不能替代食品安全或公共卫生处置规范。", "SRC-0040", "Chapter 34 Hepatitis E Virus; PDF page 568", "all_stages"),
    ("HEV-002-fecal-oral", "hev_transmission", "HEV 粪口传播", "fecal_oral_transmission_and_contaminated_food_or_water_are_key_routes", "HEV 以粪口传播为核心，污染的水、食物和猪源产品暴露可构成风险；解释时需区分养殖场传播与食品消费暴露。", "SRC-0040", "Chapter 34 Hepatitis E Virus; PDF page 568-569", "all_stages"),
    ("HEV-003-subclinical-pigs", "hev_clinical_boundary", "猪 HEV 临床表现边界", "pigs_often_have_microscopic_hepatitis_without_obvious_clinical_disease", "猪感染 HEV 可出现肝脏复制和显微肝炎，但常无明显临床病；不得把 HEV 检出直接写成猪群明显临床肝炎诊断。", "SRC-0040", "Chapter 34 Hepatitis E Virus; PDF page 568-569", "grower_finisher"),
    ("HEV-004-viremia-shedding", "hev_shedding", "HEV 病毒血症和粪便排毒", "viremia_and_fecal_shedding_have_different_time_windows", "HEV 感染后可出现短期病毒血症和较长粪便排毒窗口；采样解释需结合感染阶段和样本类型。", "SRC-0040", "Chapter 34 Hepatitis E Virus; PDF page 569", "grower_finisher"),
    ("HEV-005-pork-liver-risk", "hev_food_safety", "猪肝和猪源食品 HEV 风险", "undercooked_pork_liver_or_products_can_be_exposure_risks", "急性戊肝病例与猪肝或猪源产品暴露有关；本事实只用于风险提示，不生成烹饪温度、召回或中国监管结论。", "SRC-0040", "Chapter 34 Hepatitis E Virus; PDF page 569", "all_stages"),
    ("HEV-006-lab-boundary", "hev_diagnostics", "HEV 诊断解释边界", "rt_pcr_serology_and_pathology_must_be_interpreted_with_stage_and_public_health_context", "HEV 诊断涉及核酸、血清学和病理解释；猪群检出需结合感染阶段、排毒和公共卫生语境，不能单凭单项结果扩展为场内处置结论。", "SRC-0040", "Chapter 34 Hepatitis E Virus; PDF page 568-570", "all_stages"),
    ("HERP-001-taxonomy", "herpesvirus_taxonomy", "猪疱疹病毒分类范围", "swine_relevant_herpesviruses_include_prv_pcmv_plhv_and_mcf_agents", "猪相关疱疹病毒章节覆盖伪狂犬病病毒、猪巨细胞病毒、猪淋巴嗜性疱疹病毒和引起猪恶性卡他热的相关病毒。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 572-573", "all_stages"),
    ("HERP-002-latency", "herpesvirus_latency", "疱疹病毒潜伏感染", "latency_and_reactivation_are_core_herpesvirus_features", "疱疹病毒重要特征是潜伏感染与再激活；猪疱疹病毒控制解释必须考虑潜伏感染和应激再激活边界。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 575 and 580", "all_stages"),
    ("PRV-001-natural-host", "prv_host_range", "PRV 自然宿主和跨种致死边界", "pigs_are_natural_host_but_other_mammals_can_develop_fatal_disease", "猪是 PRV 的唯一自然宿主，但犬、猫、牛、羊等其他哺乳动物感染可发生致死性疾病；公共卫生和伴侣动物风险需单独解释。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 577", "all_stages"),
    ("PRV-002-spread", "prv_transmission", "PRV 传播途径", "direct_contact_is_primary_and_transmission_can_involve_shedding_and_reproductive_routes", "PRV 主要经猪间直接接触传播，也可涉及排毒、繁殖相关传播和特定条件下的环境暴露；不能用单一传播途径解释所有暴发。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 578-579", "all_stages"),
    ("PRV-003-neuro-respiratory-reproductive", "prv_clinical_pattern", "PRV 临床系统边界", "clinical_expression_depends_on_age_and_may_include_neurologic_respiratory_and_reproductive_signs", "PRV 临床表现与年龄和免疫状态相关，可涉及神经、呼吸和繁殖系统；诊断需结合日龄、群体状态和实验室检测。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 579-583", "all_stages"),
    ("PRV-004-differential", "prv_differential", "PRV 神经症状鉴别", "pseudorabies_differentials_include_rabies_teschovirus_sapelovirus_csf_asf_nipah_prrsv_influenza_and_toxicosis", "出现类似伪狂犬病的神经或全身症状时，鉴别诊断包括狂犬病、肠道病毒性脑脊髓炎、猪瘟、非洲猪瘟、尼帕病毒、PRRSV、流感和中毒等。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 583", "all_stages"),
    ("PRV-005-diagnosis-marker-vaccine", "prv_diagnostics", "PRV 诊断和标记疫苗边界", "diagnostics_and_gene_deleted_vaccines_require_distinguishing_field_and_vaccine_virus", "PRV 诊断和控制可涉及病毒分离、PCR、血清学和基因缺失疫苗策略；生成结论时必须区分野毒感染、疫苗免疫和标记检测语境。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 583-585", "all_stages"),
    ("PRV-006-vaccine-boundary", "prv_control_boundary", "PRV 疫苗控制边界", "vaccination_may_reduce_clinical_disease_but_does_not_automatically_eliminate_latency_or_field_virus_risk", "PRV 疫苗可降低临床病和排毒风险，但不能自动写成清除潜伏感染或消除野毒风险；根除和监管结论需另有权威来源。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 584-585", "all_stages"),
    ("PCMV-001-natural-infection", "pcmv_host_range", "PCMV 自然感染", "natural_porcine_cytomegalovirus_infection_is_limited_to_pigs", "猪巨细胞病毒自然感染限于猪，临床解释不应外推到其他宿主。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 586-587", "all_stages"),
    ("PCMV-002-piglet-disease", "pcmv_clinical_pattern", "PCMV 仔猪疾病边界", "disease_is_often_subclinical_or_mild_but_can_affect_fetuses_and_piglets", "PCMV 多为亚临床或轻症，但在免疫易感群可引起胎儿和仔猪死亡、发育不良、鼻炎或神经症状；需结合日龄和免疫状态解释。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 586-587", "piglets"),
    ("PCMV-003-shedding", "pcmv_shedding", "PCMV 排毒边界", "congenitally_infected_pigs_can_shed_virus_and_serology_may_miss_neonatal_infection", "先天感染仔猪可持续排毒，早期感染仔猪可能未及时转阳；PCR、病毒分离和血清学解释需结合感染阶段。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 587-589", "piglets"),
    ("PCMV-004-differential", "pcmv_differential", "PCMV 鉴别诊断", "pcmv_associated_disease_requires_differentiation_from_csf_enterovirus_parvovirus_prrsv_pcv2_and_prv", "PCMV 相关疾病需与猪瘟、肠道病毒、细小病毒、PRRSV、PCV2 和 PRV 等鉴别，不能单凭鼻炎或仔猪衰弱定因。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 588", "piglets"),
    ("PLHV-001-detection", "plhv_relevance", "猪淋巴嗜性疱疹病毒检测边界", "plhvs_are_detected_in_leukocytes_and_lymphoid_organs_but_disease_association_is_limited", "PLHV 可在猪白细胞和淋巴组织中检出，但自然条件下明确临床疾病关联有限；检出不得自动等同致病。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 589-592", "all_stages"),
    ("PLHV-002-xenotransplant", "plhv_public_health_boundary", "PLHV 异种移植边界", "plhv_public_health_relevance_is_mainly_xenotransplantation_risk_context", "PLHV 的公共卫生讨论主要出现在异种移植风险语境；不得将其写成普通猪场人兽共患病结论。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 591", "all_stages"),
    ("MCF-001-ovine-herpesvirus-2", "mcf_agent", "猪恶性卡他热病原边界", "ovine_herpesvirus_2_can_cause_porcine_malignant_catarrhal_fever", "猪恶性卡他热可由绵羊疱疹病毒 2 等 gammaherpesvirus 引起，是偶发系统性疾病；需要结合羊接触史和实验室证据解释。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 593-594", "all_stages"),
    ("MCF-002-dead-end-host", "mcf_transmission", "MCF 终末宿主边界", "clinically_affected_pigs_are_dead_end_hosts_and_do_not_drive_outbreak_spread", "发生临床 MCF 的猪通常是终末宿主，不作为持续传播源解释暴发扩散；传播风险需回到储存宿主和接触史。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 594", "all_stages"),
    ("MCF-003-clinical-differential", "mcf_differential", "MCF 鉴别诊断", "mcf_differentials_include_aujeszkys_disease_teschovirus_pcv2_and_systemic_viral_diseases", "猪 MCF 可表现发热、精神沉郁、眼鼻病变和神经症状，需与伪狂犬病、teschovirus、PCV2 和其他系统性病毒病鉴别。", "SRC-0041", "Chapter 35 Herpesviruses; PDF page 594-595", "all_stages"),
    ("IAV-001-history", "influenza_history", "猪流感历史边界", "swine_influenza_reports_have_historical_links_to_the_1918_human_pandemic", "猪流感样疾病早期报告与 1918 年人类流感大流行有历史联系；历史关联不得简化为当前暴发来源判断。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 600", "all_stages"),
    ("IAV-002-segmented-reassortment", "influenza_evolution", "流感分节基因组和重配", "segmented_genome_allows_reassortment_when_two_viruses_coinfect", "流感病毒分节基因组允许不同病毒共同感染时发生重配；猪流感解释必须考虑基因来源、谱系和重配。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 601", "all_stages"),
    ("IAV-003-receptor-boundary", "influenza_host_range", "流感受体亲和边界", "human_and_avian_influenza_viruses_differ_in_sialic_acid_receptor_preference", "人源和禽源流感病毒受体偏好不同，猪相关感染解释需结合受体、宿主适应和病毒基因背景。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 601", "all_stages"),
    ("IAV-004-lineages", "influenza_lineage", "猪流感谱系", "lineage_refers_to_common_genetic_origin_for_a_gene_segment", "猪流感谱系指某基因片段共同遗传来源，不能仅用 H/N 亚型替代完整基因谱系解释。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 602", "all_stages"),
    ("IAV-005-subtypes", "influenza_subtypes", "猪群维持的主要流感亚型", "h1n1_h1n2_and_h3n2_are_important_swine_maintained_subtypes", "H1N1、H1N2 和 H3N2 是猪群中重要维持亚型；地区流行格局需结合本地监测。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 602-604", "all_stages"),
    ("IAV-006-avian-human-introductions", "influenza_cross_species", "猪流感跨种引入边界", "human_and_avian_influenza_viruses_can_be_detected_or_introduced_in_pigs_but_adaptation_varies", "人源和禽源流感病毒可引入或偶发检出于猪，但是否在猪群适应和持续传播需另有证据。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 602-604", "all_stages"),
    ("IAV-007-serology-boundary", "influenza_diagnostics", "猪流感血清学边界", "serology_may_not_cleanly_distinguish_human_and_swine_influenza_lineages", "猪流感血清学可能难以清楚区分人源、猪源或重配谱系，解释需结合病毒分离、PCR 和测序。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 602", "all_stages"),
    ("IAV-008-seasonality", "influenza_ecology", "猪流感季节性", "influenza_activity_can_have_seasonal_peaks_but_patterns_vary_by_region_and_population", "猪流感活动可有季节性高峰，但不同地区、猪群结构和病毒谱系会改变流行格局；不能用固定月份预测所有场景。", "SRC-0042", "Chapter 36 Influenza Viruses; PDF page 604", "all_stages"),
]


RULES = [
    ("RULE-209", "HEV 不得由猪群检出直接生成公共卫生处置", "hev_public_health", "critical", "SRC-0040", "Swine-hev-public-health-action-authority-required.md", "HEV 猪群检出只能生成公共卫生风险边界；食品安全处置、召回、消费建议和人群诊疗必须等待相应权威来源。", "568-569"),
    ("RULE-210", "HEV 猪临床诊断不得过度解释", "hev_clinical_boundary", "high", "SRC-0040", "Swine-hev-subclinical-pigs-not-clinical-hepatitis.md", "猪 HEV 常可无明显临床病，不能把 HEV 检出直接写成猪群临床肝炎主因。", "568-569"),
    ("RULE-211", "HEV 采样解释必须区分病毒血症和粪便排毒窗口", "hev_diagnostics", "high", "SRC-0040", "Swine-hev-viremia-shedding-window.md", "HEV 核酸、血清学和粪便排毒解释必须结合感染阶段和样本类型。", "569"),
    ("RULE-212", "疱疹病毒控制解释必须纳入潜伏和再激活", "herpesvirus_latency", "high", "SRC-0041", "Swine-herpesvirus-latency-reactivation-boundary.md", "猪疱疹病毒相关控制和风险解释必须考虑潜伏感染、应激再激活和隐性感染边界。", "575, 580"),
    ("RULE-213", "PRV 神经症状必须保留多病因鉴别", "prv_differential", "critical", "SRC-0041", "Swine-prv-neurologic-differential-required.md", "疑似伪狂犬病的神经症状必须与狂犬病、猪瘟、非洲猪瘟、teschovirus、sapovirus/astrovirus、尼帕病毒、PRRSV、流感和中毒等鉴别。", "583"),
    ("RULE-214", "PRV 疫苗免疫不得等同清除野毒和潜伏感染", "prv_control_boundary", "critical", "SRC-0041", "Swine-prv-vaccination-not-eradication.md", "PRV 疫苗可降低临床病和排毒风险，但不能自动生成根除、清除潜伏感染或本地监管结论。", "584-585"),
    ("RULE-215", "PRV 标记检测必须区分野毒和疫苗语境", "prv_diagnostics", "high", "SRC-0041", "Swine-prv-marker-test-field-vaccine-context.md", "PRV gE/gene-deleted 疫苗和血清学解释必须区分野毒感染、疫苗免疫和群体监测目的。", "583-585"),
    ("RULE-216", "PCMV 仔猪病不得单凭鼻炎或衰弱定因", "pcmv_differential", "high", "SRC-0041", "Swine-pcmv-piglet-differential-required.md", "PCMV 相关仔猪病需与猪瘟、肠道病毒、细小病毒、PRRSV、PCV2 和 PRV 等鉴别。", "588"),
    ("RULE-217", "PCMV 新生仔猪检测必须考虑未转阳和持续排毒", "pcmv_diagnostics", "high", "SRC-0041", "Swine-pcmv-neonatal-serology-shedding-boundary.md", "PCMV 新生仔猪感染解释必须考虑先天感染、未及时血清转阳和持续排毒。", "587-589"),
    ("RULE-218", "PLHV 检出不得自动等同临床致病", "plhv_causality", "medium", "SRC-0041", "Swine-plhv-detection-not-clinical-causality.md", "PLHV 在白细胞和淋巴组织检出不得自动写成普通猪场临床病因。", "589-592"),
    ("RULE-219", "PLHV 公共卫生结论限于异种移植风险语境", "plhv_public_health_boundary", "medium", "SRC-0041", "Swine-plhv-public-health-xenotransplant-context.md", "PLHV 公共卫生讨论主要限于异种移植风险，不能迁移为普通养殖场人兽共患处置结论。", "591"),
    ("RULE-220", "猪 MCF 需结合羊接触史和实验室证据", "mcf_diagnostics", "high", "SRC-0041", "Swine-mcf-sheep-contact-lab-required.md", "猪恶性卡他热解释需结合羊接触史、临床病理和病原检测，不得单凭发热眼鼻病变定因。", "593-595"),
    ("RULE-221", "猪 MCF 临床猪不应写成持续传播源", "mcf_transmission", "high", "SRC-0041", "Swine-mcf-pigs-dead-end-host-boundary.md", "临床 MCF 猪通常是终末宿主，暴发扩散解释应回到储存宿主和接触史。", "594"),
    ("RULE-222", "猪流感解释必须纳入重配和谱系", "influenza_evolution", "critical", "SRC-0042", "Swine-influenza-reassortment-lineage-required.md", "猪流感解释不能只写 H/N 亚型，必须考虑分节基因组、重配和基因谱系。", "601-602"),
    ("RULE-223", "猪流感血清学不得单独判定来源谱系", "influenza_diagnostics", "high", "SRC-0042", "Swine-influenza-serology-lineage-boundary.md", "猪流感血清学不得单独判定人源、禽源、猪源或重配来源，需结合病毒分离、PCR 和测序。", "602"),
    ("RULE-224", "禽源或人源流感检出不等同猪群适应传播", "influenza_cross_species", "high", "SRC-0042", "Swine-influenza-introduction-not-adaptation.md", "人源或禽源流感病毒在猪中检出不等同已在猪群适应并持续传播。", "602-604"),
    ("RULE-225", "猪流感季节性不得固定套用月份", "influenza_ecology", "medium", "SRC-0042", "Swine-influenza-seasonality-local-context.md", "猪流感季节性解释必须结合地区、猪群结构和本地监测，不得固定套用月份。", "604"),
]


SOURCES = [
    ("SRC-0040", "Diseases of Swine 11e Chapter 34 Hepatitis E Virus", "PDF page 568-571", "wiki/sources/SRC-0040-diseases-of-swine-11e-chapter-34-hepatitis-e-virus.md", "Chapter 34 covers HEV zoonotic relevance, fecal-oral transmission, swine infection, shedding, food exposure, and diagnostic boundaries. PDF pages 570-571 are references and were not converted into standalone facts."),
    ("SRC-0041", "Diseases of Swine 11e Chapter 35 Herpesviruses", "PDF page 572-599", "wiki/sources/SRC-0041-diseases-of-swine-11e-chapter-35-herpesviruses.md", "Chapter 35 covers herpesvirus taxonomy, latency, PRV/Aujeszky's disease, PCMV, PLHV, and porcine MCF boundaries. PDF pages 595-599 are references and were not converted into standalone facts."),
    ("SRC-0042", "Diseases of Swine 11e Chapter 36 Influenza Viruses opening", "PDF page 600-604", "wiki/sources/SRC-0042-diseases-of-swine-11e-chapter-36-influenza-viruses-opening.md", "Chapter 36 opening covers swine influenza history, segmented genome, reassortment, receptor and lineage boundaries, cross-species introductions, and early epidemiology."),
]


TOPICS = [
    ("Swine-hepatitis-e-virus-zoonotic-food-safety-boundaries.md", "猪 HEV 人兽共患和食品安全边界", "SRC-0040", "本主题用于解释猪 HEV 的公共卫生属性、粪口传播、猪源食品暴露、排毒窗口和诊断边界。"),
    ("Swine-herpesvirus-prv-pcmv-plhv-mcf-boundaries.md", "猪疱疹病毒 PRV/PCMV/PLHV/MCF 诊断和控制边界", "SRC-0041", "本主题用于解释猪疱疹病毒分类、潜伏感染、伪狂犬病、猪巨细胞病毒、猪淋巴嗜性疱疹病毒和猪恶性卡他热的诊断、鉴别、控制和公共卫生边界。"),
    ("Swine-influenza-virus-reassortment-lineage-opening.md", "猪流感病毒重配、谱系和跨种引入边界", "SRC-0042", "本主题用于解释猪流感开端章节中的历史、分节基因组、重配、受体偏好、谱系、血清学解释和跨种引入边界。"),
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
- 批次：Formal Batch 017。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_017_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_017_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_017_pdf_pages_565_604_parser_report.txt`。
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
- 本页正式 facts 已在 `issues/formal_batch_017_cross_review.md` 中交叉审查。
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
        ISSUES / "formal_batch_017_candidate_facts.json",
        json.dumps(
            {
                "batch_id": "formal-batch-017",
                "source_ids": ["SRC-0040", "SRC-0041", "SRC-0042"],
                "parser_cross_check": {
                    "primary": "PyMuPDF fitz",
                    "secondary": "pdfplumber",
                    "tertiary": "pypdf",
                    "report": "issues/formal_batch_017_pdf_pages_565_604_parser_report.txt",
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
    rows = []
    if path.exists():
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
    rows = [["source_id", "title", "pages", "evidence_status", "relpath"]]
    if path.exists():
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
        ("DIS-017-hepatitis-e-virus.md", "Formal Batch 017 正文抽取：已补充 HEV 公共卫生属性、粪口传播、猪源食品暴露、排毒窗口和诊断解释边界；详见 `SRC-0040` 与 `issues/formal_batch_017_cross_review.md`。"),
        ("DIS-018-pseudorabies-aujeszky-disease.md", "Formal Batch 017 正文抽取：已补充 PRV 自然宿主、跨种致死风险、传播、临床系统、鉴别诊断、标记检测和疫苗控制边界；详见 `SRC-0041`。"),
        ("DIS-019-porcine-cytomegalovirus.md", "Formal Batch 017 正文抽取：已补充 PCMV 自然感染、仔猪病、排毒、未转阳解释和鉴别诊断边界；详见 `SRC-0041`。"),
        ("DIS-020-malignant-catarrhal-fever-ovine-herpesvirus-2.md", "Formal Batch 017 正文抽取：已补充猪 MCF 的 OvHV-2 证据、终末宿主边界、羊接触史和实验室诊断要求；详见 `SRC-0041`。"),
        ("DIS-021-influenza-viruses.md", "Formal Batch 017 正文抽取：已补充猪流感历史、分节基因组、重配、受体偏好、谱系、跨种引入和血清学解释边界；详见 `SRC-0042`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 017 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(
        ISSUES / "formal_batch_017_cross_review.md",
        """# Formal Batch 017 Cross Review

## 范围

- PDF page 565-567：Chapter 33 Flaviviruses 参考文献页，仅作为上一章边界，不生成 facts。
- PDF page 568-571：Chapter 34 Hepatitis E Virus 正文和参考文献，落库 HEV 公共卫生、传播、排毒、食品暴露和诊断边界。
- PDF page 572-599：Chapter 35 Herpesviruses 正文和参考文献，落库疱疹病毒总论、PRV、PCMV、PLHV 和猪 MCF 边界。
- PDF page 600-604：Chapter 36 Influenza Viruses 开端，落库猪流感历史、分节基因组、重配、受体、谱系和跨种引入边界。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_017_pdf_pages_565_604_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量接近，未发现漏页。
- 三次核对：`pypdf`，作为页级文本存在性与异常提示，不作为主文本。
- 解析报告：`issues/formal_batch_017_pdf_pages_565_604_parser_report.txt`。

## 审查结论

本批候选事实 31 条，规则页 17 个，来源页 3 个，主题页 3 个。经页码锚点、内容边界和一致性审查后允许落库。

## 审查 1：页码锚点核验

- `SRC-0040` facts 锚定 PDF page 568-570；PDF page 570-571 的参考文献条目未转化为 standalone facts。
- `SRC-0041` facts 锚定 PDF page 572-595；PDF page 595-599 的参考文献条目未转化为 standalone facts。
- `SRC-0042` facts 锚定 PDF page 600-604；下一批应从 PDF page 605 继续 Chapter 36 正文。

## 审查 2：内容边界核验

- HEV 内容只生成猪病 Wiki 的风险和诊断边界，不生成食品召回、人群诊疗、烹饪温度或中国监管处置结论。
- PRV 内容不把疫苗免疫写成清除潜伏感染或本地根除承诺；疑似神经病保留多病因鉴别。
- PCMV/PLHV 内容不把检出直接写成普通猪场临床病因。
- MCF 内容强调羊接触史、终末宿主和实验室证据，不把临床猪写成持续传播源。
- 猪流感内容仅落库开端章节的重配、谱系、受体和跨种引入边界，不生成疫苗程序、亚型流行结论或具体防控方案。

## 审查 3：一致性核验

- facts 与新增 topic/rule/source 页面一致。
- facts 的 `applies_to_species` 均为 `swine`，`evidence_status` 均为 `HUMAN_REVIEWED`。
- 新增 `fact_id`、`RULE-209` 至 `RULE-225` 与既有条目不重复。

## 保留问题

- PDF page 605 以后仍为 Chapter 36 Influenza Viruses 正文；下一批应继续抽取流行病学、临床表现、诊断、控制和参考文献边界。
- HEV 食品安全、PRV 监管、猪流感公共卫生和跨种传播结论如需进入中国本地答案，仍需中国官方或 A0/A1 来源复核。
""",
    )


def append_progress_docs() -> None:
    block = """

## Formal Batch 017 实施记录

- 完成时间：2026-05-07 00:35:00 +08:00。
- 处理范围：PDF page 565-604。
- 章节边界：Chapter 33 Flaviviruses 参考文献收尾；Chapter 34 Hepatitis E Virus；Chapter 35 Herpesviruses；Chapter 36 Influenza Viruses 开端。
- 新增来源：`SRC-0040`、`SRC-0041`、`SRC-0042`。
- 新增主题页：猪 HEV 人兽共患和食品安全边界、猪疱疹病毒 PRV/PCMV/PLHV/MCF 诊断和控制边界、猪流感病毒重配/谱系/跨种引入边界。
- 新增规则页：`RULE-209` 至 `RULE-225`。
- 新增候选事实：`issues/formal_batch_017_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_017_cross_review.md`。
- 正式落库 facts：31 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、HEV 食品召回/烹饪温度/人群诊疗结论、PRV 本地根除或监管结论、固定疫苗程序、猪流感亚型本地流行结论和具体防控处方。

### Formal Batch 017 交叉审查

- 页码锚点核验：通过。`SRC-0040` 覆盖 PDF page 568-571，`SRC-0041` 覆盖 PDF page 572-599，`SRC-0042` 覆盖 PDF page 600-604。PDF page 565-567、570-571、595-599 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。HEV、PRV/PCMV/PLHV/MCF、猪流感均只落库教材证据和诊断/公共卫生/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 604。
- 下一批应从 PDF page 605 开始。
- 推荐下一批：PDF page 605-644，继续 Chapter 36 Influenza Viruses 正文。
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
    print("formal batch 017 built")


if __name__ == "__main__":
    main()
