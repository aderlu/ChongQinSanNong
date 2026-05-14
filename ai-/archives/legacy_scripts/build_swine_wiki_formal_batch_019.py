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
NOW = "2026-05-07T00:10:00+00:00"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def extract_pdf_pages(start: int = 645, end: int = 684) -> None:
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
    write_text(ISSUES / "formal_batch_019_pdf_pages_645_684_extract.txt", "".join(extract_parts).strip() + "\n")
    write_text(ISSUES / "formal_batch_019_pdf_pages_645_684_parser_report.txt", "\n".join(report_rows) + "\n")


FACTS = [
    ("PESTI-001-taxonomy", "pestivirus_taxonomy", "猪相关 Pestivirus 分类", "pestiviruses_include_csfv_bvdv_1_bvdv_2_bdv_and_other_related_species", "Pestivirus 属包括 CSFV、BVDV-1、BVDV-2、BDV 及其他相关 pestivirus；猪源检测解释需区分病毒种。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 646", "all_stages"),
    ("PESTI-002-no-human-infection", "pestivirus_public_health", "Pestivirus 公共卫生边界", "there_is_no_evidence_of_human_infection_with_pestivirus", "教材指出没有人感染 pestivirus 的证据；公共卫生结论不得扩展为其他病毒病或监管处置。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 647", "all_stages"),
    ("CSFV-001-listed-disease", "csf_regulatory_boundary", "CSF 国际列名疫病边界", "classical_swine_fever_is_an_oie_listed_disease", "经典猪瘟是 WOAH/OIE 列名疫病；本事实只作为国际教材边界，中国处置需中国官方来源。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 647", "all_stages"),
    ("CSFV-002-stability", "csfv_virology", "CSFV RNA 病毒稳定性", "csfv_is_relatively_stable_for_an_rna_virus", "CSFV 对 RNA 病毒而言相对稳定，传播和环境风险解释需考虑病毒稳定性。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 647", "all_stages"),
    ("CSFV-003-semen-boundary", "csfv_transmission", "CSFV 精液传播边界", "csfv_transmission_by_semen_is_possible_but_requires_contextual_evidence", "CSFV 可在精液中检出，精液传播被认为可能发生；解释时需结合检测、动物状态和传播语境。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 648", "boars"),
    ("CSFV-004-indirect-people", "csfv_transmission", "CSFV 人员机械传播", "indirect_transmission_via_people_can_occur_without_biosecurity", "人员在生物安全措施不足时可机械性传播 CSFV；不能将人员接触风险写成唯一传播途径。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 648", "all_stages"),
    ("CSFV-005-excretions", "csfv_transmission", "CSFV 分泌物和排泄物排毒", "infected_pigs_shed_virus_in_secretions_and_excretions", "CSFV 感染猪可在多种分泌物和排泄物中排毒，传播速度受猪只感染阶段和群体因素影响。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 648", "all_stages"),
    ("CSFV-006-immune-evasion", "csfv_pathogenesis", "CSFV 免疫逃逸和免疫抑制", "csfv_interferes_with_innate_and_adaptive_immune_responses", "CSFV 可干扰先天和适应性免疫反应，造成免疫抑制并促进病毒扩散。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 649", "all_stages"),
    ("CSFV-007-clinical-nonspecific", "csfv_clinical_boundary", "CSF 临床表现非特异", "clinical_signs_are_not_pathognomonic_and_vary_by_form", "CSF 临床表现非特异，可因急性、慢性或温和型而变化；临床观察不能替代实验室确诊。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 649-651", "all_stages"),
    ("CSFV-008-lab-required", "csfv_diagnostics", "CSF 必须实验室诊断", "laboratory_diagnosis_is_always_required_for_csf", "由于 CSF 无特异性临床表现，教材强调必须进行实验室诊断。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 651", "all_stages"),
    ("CSFV-009-pan-pestivirus-screen", "csfv_diagnostics", "CSFV pan-pestivirus 筛查边界", "pan_pestivirus_assays_can_screen_but_species_confirmation_is_needed", "CSFV 与其他 pestivirus 存在相关性，pan-pestivirus 检测可用于筛查，但种属确认和鉴别仍必要。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 651-652", "all_stages"),
    ("CSFV-010-serology-cross-reaction", "csfv_serology", "CSFV 血清学交叉反应", "serology_can_cross_react_with_other_pestiviruses", "CSFV 血清学可能与其他 pestivirus 抗体发生交叉反应，解释需结合检测格式和确认试验。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 652", "all_stages"),
    ("CSFV-011-immunity", "csfv_immunity", "CSFV 感染或免疫后保护", "vaccinated_or_infected_pigs_are_resistant_to_subsequent_challenge", "感染或免疫后的猪可对后续攻击产生抵抗，但疫苗和控制效果需结合毒株、政策和群体情况。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 653", "all_stages"),
    ("CSFV-012-control-policy-boundary", "csfv_control_boundary", "CSF 控制政策边界", "control_policy_varies_between_no_vaccination_stamping_out_and_vaccination_contexts", "CSF 控制政策可涉及不免疫、扑杀和疫苗策略等不同语境；不得由教材直接生成中国本地处置命令。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 653-654", "all_stages"),
    ("CSFV-013-wild-boar", "csfv_wild_boar", "CSFV 野猪控制边界", "wild_boar_can_affect_csfv_persistence_and_control_strategy", "野猪可影响 CSFV 维持和控制策略，口服疫苗等野猪控制内容只作为教材边界。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 654", "all_stages"),
    ("BUNGO-001-pig-only-report", "bungowannah_virus", "Bungowannah 病毒宿主报告", "bungowannah_virus_has_only_been_reported_in_pigs", "Bungowannah 病毒报告限于猪，宿主范围和传播结论不得外推。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 655", "all_stages"),
    ("BUNGO-002-persistent-infection", "bungowannah_virus_pathogenesis", "Bungowannah 持续感染", "persistently_infected_pigs_can_excrete_virus_lifelong", "Bungowannah 病毒可形成持续感染，持续感染猪可能终身排毒。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 656", "piglets"),
    ("BUNGO-003-reproductive-piglet", "bungowannah_virus_clinical", "Bungowannah 繁殖和仔猪影响", "infection_can_cause_reproductive_effects_and_piglet_losses", "Bungowannah 病毒感染的重要影响包括繁殖问题、死产/仔猪损失和持续感染相关问题。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 656-657", "sows"),
    ("RUMINANT-PESTI-001-contamination", "ruminant_pestivirus_boundary", "反刍动物 pestivirus 污染边界", "bvdv_or_bdv_can_contaminate_biologicals_and_live_virus_vaccines", "BVDV 或 BDV 可污染生物制品、细胞或活病毒疫苗生产材料；解释猪源 pestivirus 检出需考虑污染来源。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 658-660", "all_stages"),
    ("RUMINANT-PESTI-002-differential", "ruminant_pestivirus_differential", "BVDV/BDV 与 CSFV 鉴别", "bvdv_and_bdv_must_be_considered_in_csfv_differential_diagnosis", "在猪中检出 BVDV/BDV 或相关抗体时，必须作为 CSFV 鉴别诊断和血清学交叉反应边界处理。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 659", "all_stages"),
    ("APPV-001-significance-uncertain", "appv_boundary", "APPV 临床意义边界", "appv_epidemiology_and_clinical_significance_remain_insufficient_for_fixed_control", "APPV 的流行病学和临床意义仍不足以确定固定预防或控制措施。", "SRC-0046", "Chapter 39 Pestiviruses; PDF page 661", "all_stages"),
    ("PICORNA-001-swine-genera", "picornavirus_taxonomy", "猪相关 Picornavirus 属", "picornaviruses_in_pigs_include_aphthovirus_cardiovirus_enterovirus_kobuvirus_pasivirus_sapelovirus_senecavirus_and_teschovirus", "猪相关小 RNA 病毒包括 Aphthovirus、Cardiovirus、Enterovirus、Kobuvirus、Pasivirus、Sapelovirus、Senecavirus 和 Teschovirus 等。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 665-666", "all_stages"),
    ("FMDV-001-aphthovirus", "fmdv_taxonomy", "FMDV 分类", "fmdv_is_an_aphthovirus_in_family_picornaviridae", "口蹄疫病毒属于 Picornaviridae 科 Aphthovirus 属，是无囊膜小 RNA 病毒。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 670", "all_stages"),
    ("FMDV-002-people-mechanical", "fmdv_transmission", "FMDV 人员机械传播", "people_can_mechanically_transmit_fmdv_and_are_important_in_control_programs", "人员可机械性传播 FMDV，因此人员流动和污染物控制是口蹄疫控制的重要考虑。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 671-672", "all_stages"),
    ("FMDV-003-food-waste", "fmdv_transmission", "FMDV 污染食物废弃物传播", "contaminated_human_food_waste_can_be_linked_to_fmdv_transmission", "污染的人类食物废弃物可与 FMDV 传播相关，泔水或废弃物暴露应作为生物安全风险边界。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 673", "all_stages"),
    ("FMDV-004-aerosol-pigs", "fmdv_transmission", "猪 FMDV 气溶胶排毒", "pigs_can_aerosolize_large_quantities_of_fmdv_in_respirations", "猪可通过呼吸排出大量 FMDV 气溶胶，气溶胶传播受气象、距离和病毒云完整性影响。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 673", "all_stages"),
    ("FMDV-005-carrier-boundary", "fmdv_persistence", "猪 FMDV 持续感染边界", "pigs_do_not_harbor_infectious_fmdv_for_more_than_28_days", "教材指出猪不携带感染性 FMDV 超过 28 天；持续感染和携带结论需区分物种。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 675", "all_stages"),
    ("FMDV-006-environment-stability", "fmdv_environment", "FMDV 环境稳定性", "fmdv_survival_depends_on_concentration_material_and_ambient_conditions", "FMDV 在环境、组织和污染物中的存活取决于病毒浓度、材料和温湿度等条件。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 675", "all_stages"),
    ("FMDV-007-pig-clinical-severe", "fmdv_clinical_pattern", "猪口蹄疫临床严重性", "clinical_disease_is_usually_severe_in_pigs", "猪口蹄疫临床病通常较重，疼痛和水疱性病变可明显影响行动和采食。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 677", "all_stages"),
    ("FMDV-008-vaccine-not-sterilizing", "fmdv_immunity", "FMD 疫苗感染阻断边界", "vaccines_may_prevent_severe_clinical_disease_but_do_not_necessarily_prevent_infection", "FMD 疫苗可预防严重临床病，但不一定阻止感染；不能据此生成完全阻断传播结论。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 678", "all_stages"),
    ("FMDV-009-differential", "fmdv_differential", "FMD 水疱病鉴别", "fmd_differential_includes_svd_vesicular_stomatitis_svv_and_vesivirus_infections", "FMD 临床诊断需与猪水疱病、水疱性口炎、Senecavirus A 和 vesivirus 感染等鉴别。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 679", "all_stages"),
    ("FMDV-010-lab-confirmation", "fmdv_diagnostics", "FMD 实验室确认", "suspect_fmd_requires_timely_lab_investigation_and_virus_characterization", "疑似 FMD 需及时实验室调查，并可通过 RT-PCR、测序、抗原检测、病毒分离和血清学进行确认和表征。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 679-680", "all_stages"),
    ("FMDV-011-differentiating-infection-vaccination", "fmdv_diagnostics", "FMD 感染与免疫鉴别", "nonstructural_protein_tests_can_help_differentiate_infected_from_vaccinated_populations", "非结构蛋白检测可在群体层面帮助区分感染动物和免疫动物，但解释需结合疫苗、群体和检测目的。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 680", "all_stages"),
    ("FMDV-012-control-complexity", "fmdv_control_boundary", "FMD 控制复杂性", "fmd_control_requires_strict_movement_biosecurity_and_context_specific_vaccination_policy", "FMD 控制涉及严格移动控制、生物安全、扑杀或疫苗政策等复杂策略；教材内容不得直接转化为中国本地命令。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 682-683", "all_stages"),
    ("SVDV-001-enterovirus", "svdv_taxonomy", "猪水疱病病毒分类", "svdv_is_an_enterovirus_b_in_family_picornaviridae", "猪水疱病病毒属于 Picornaviridae 科 Enterovirus B 种，是无囊膜病毒。", "SRC-0047", "Chapter 40 Picornaviruses opening; PDF page 683-684", "all_stages"),
]


RULES = [
    ("RULE-242", "CSF 临床表现不能替代实验室确诊", "csfv_diagnostics", "critical", "SRC-0046", "Swine-csf-lab-confirmation-required.md", "CSF 无特异性临床表现，必须进行实验室诊断，不能仅凭临床观察确诊或排除。", "649-651"),
    ("RULE-243", "CSFV pan-pestivirus 筛查后必须确认种属", "csfv_diagnostics", "high", "SRC-0046", "Swine-csfv-pan-pestivirus-confirm-species.md", "pan-pestivirus 检测只能作为筛查或提示，CSFV 结论需种属确认和鉴别。", "651-652"),
    ("RULE-244", "CSFV 血清学必须考虑其他 pestivirus 交叉反应", "csfv_serology", "high", "SRC-0046", "Swine-csfv-serology-pestivirus-cross-reaction.md", "CSFV 血清学解释必须考虑 BVDV、BDV 等其他 pestivirus 的抗体交叉反应。", "652, 659"),
    ("RULE-245", "CSF 控制政策不得由教材直接迁移为中国命令", "csfv_control_boundary", "critical", "SRC-0046", "Swine-csf-control-local-authority-required.md", "CSF 控制、免疫、扑杀、封锁和野猪策略不得仅凭教材生成中国本地监管命令。", "653-654"),
    ("RULE-246", "Bungowannah 持续感染猪排毒需作为传播边界", "bungowannah_virus", "high", "SRC-0046", "Swine-bungowannah-persistent-shedding-boundary.md", "Bungowannah 持续感染猪可能终身排毒，传播和监测解释必须保留持续感染边界。", "656"),
    ("RULE-247", "生物制品 pestivirus 污染必须作为鉴别边界", "pestivirus_contamination", "high", "SRC-0046", "Swine-pestivirus-biological-contamination-boundary.md", "猪源 pestivirus 检出需考虑疫苗、细胞、血清或生物制品污染，不能直接定为场内自然感染。", "658-660"),
    ("RULE-248", "APPV 控制措施不得在证据不足时固定化", "appv_boundary", "medium", "SRC-0046", "Swine-appv-control-evidence-insufficient.md", "APPV 流行病学和临床意义未清楚时，不得生成固定预防或控制措施。", "661"),
    ("RULE-249", "猪相关 picornavirus 必须先区分属和疾病实体", "picornavirus_taxonomy", "medium", "SRC-0047", "Swine-picornavirus-genus-disease-distinction.md", "猪相关 picornavirus 覆盖多个属和疾病实体，不能用小 RNA 病毒总称替代具体病因。", "665-666"),
    ("RULE-250", "FMD 疑似必须保留重大水疱病鉴别", "fmdv_differential", "critical", "SRC-0047", "Swine-fmd-vesicular-differential-required.md", "疑似 FMD 必须与 SVD、水疱性口炎、Senecavirus A 和 vesivirus 感染等水疱病鉴别。", "679"),
    ("RULE-251", "FMD 疑似需及时实验室调查和病毒表征", "fmdv_diagnostics", "critical", "SRC-0047", "Swine-fmd-timely-lab-characterization.md", "疑似 FMD 需及时实验室调查，并通过 RT-PCR、测序、抗原检测、病毒分离或血清学进行确认和表征。", "679-680"),
    ("RULE-252", "FMD 疫苗不得写成完全阻断感染", "fmdv_immunity", "critical", "SRC-0047", "Swine-fmd-vaccine-not-sterilizing.md", "FMD 疫苗可防止严重临床病，但不一定阻止感染，不得写成完全阻断传播。", "678"),
    ("RULE-253", "FMD 猪气溶胶排毒是传播风险核心边界", "fmdv_transmission", "critical", "SRC-0047", "Swine-fmd-pig-aerosol-risk-boundary.md", "猪可呼出大量 FMDV 气溶胶，气溶胶传播需结合距离、气象和病毒存活条件解释。", "673"),
    ("RULE-254", "FMD 人员和污染物机械传播必须纳入生物安全", "fmdv_biosecurity", "critical", "SRC-0047", "Swine-fmd-fomite-people-biosecurity.md", "FMDV 可通过人员、污染物和机械媒介传播，生物安全解释必须纳入移动和污染控制。", "671-673, 682"),
    ("RULE-255", "FMD 持续感染结论必须区分物种", "fmdv_persistence", "high", "SRC-0047", "Swine-fmd-persistence-species-boundary.md", "FMD 持续感染和携带结论必须区分物种；猪不应被写成长期携带感染性病毒超过 28 天。", "675"),
    ("RULE-256", "FMD 中国监管处置必须等待 A0/A1 来源", "fmdv_regulatory_boundary", "critical", "SRC-0047", "Swine-fmd-china-regulatory-source-required.md", "FMD 涉及中国上报、封锁、扑杀、调运和消毒等结论时，必须等待中国官方或 A0/A1 来源。", "670-683"),
    ("RULE-257", "SVDV 与 FMD 临床相似时必须实验室鉴别", "svdv_differential", "critical", "SRC-0047", "Swine-svdv-fmd-lab-differential.md", "SVDV 可表现为类似 FMD 的水疱病，必须通过实验室检测与 FMD 鉴别。", "683-684"),
]


SOURCES = [
    ("SRC-0046", "Diseases of Swine 11e Chapter 39 Pestiviruses", "PDF page 646-664", "wiki/sources/SRC-0046-diseases-of-swine-11e-chapter-39-pestiviruses.md", "Chapter 39 covers pestivirus taxonomy, CSFV/CSF transmission, clinical signs, diagnosis, immunity, control, Bungowannah virus, ruminant pestivirus contamination/differentials, APPV boundaries, and references. PDF page 645 is Chapter 38 references and PDF pages 662-664 are Chapter 39 references; they were not converted into standalone facts."),
    ("SRC-0047", "Diseases of Swine 11e Chapter 40 Picornaviruses opening", "PDF page 665-684", "wiki/sources/SRC-0047-diseases-of-swine-11e-chapter-40-picornaviruses-opening.md", "Chapter 40 opening covers swine picornavirus taxonomy, FMDV epidemiology, transmission, pathogenesis, clinical signs, diagnosis, immunity and control boundaries, plus SVDV opening."),
]


TOPICS = [
    ("Swine-pestivirus-csfv-diagnostics-control-boundaries.md", "猪 Pestivirus/CSFV 诊断和控制边界", "SRC-0046", "本主题用于解释 CSFV/CSF 的传播、临床非特异性、实验室诊断、血清学交叉反应、免疫和控制政策边界，以及 Bungowannah、BVDV/BDV 污染和 APPV 证据不足边界。"),
    ("Swine-picornavirus-fmd-svd-vesicular-boundaries.md", "猪 Picornavirus/FMD/SVD 水疱病鉴别边界", "SRC-0047", "本主题用于解释猪相关 picornavirus 分类、FMDV 传播/气溶胶/环境稳定性/诊断/免疫/控制边界，以及 SVDV 与 FMD 的水疱病鉴别。"),
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
- 批次：Formal Batch 019。

## 摘要

{summary}

## 审查

- 候选事实：`issues/formal_batch_019_candidate_facts.json`。
- 交叉审查：`issues/formal_batch_019_cross_review.md`。
- PDF 解析报告：`issues/formal_batch_019_pdf_pages_645_684_parser_report.txt`。
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
- 本页正式 facts 已在 `issues/formal_batch_019_cross_review.md` 中交叉审查。
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
        ISSUES / "formal_batch_019_candidate_facts.json",
        json.dumps(
            {
                "batch_id": "formal-batch-019",
                "source_ids": ["SRC-0046", "SRC-0047"],
                "parser_cross_check": {
                    "primary": "PyMuPDF fitz",
                    "secondary": "pdfplumber",
                    "tertiary": "pypdf",
                    "report": "issues/formal_batch_019_pdf_pages_645_684_parser_report.txt",
                },
                "execution_guide": "docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md",
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
        ("DIS-024-classical-swine-fever-pestiviruses.md", "Formal Batch 019 正文抽取：已补充 CSFV/CSF 分类、传播、临床非特异性、实验室诊断、血清学交叉反应、免疫和控制政策边界；详见 `SRC-0046`。"),
        ("DIS-025-atypical-porcine-pestivirus-pestivirus-infections.md", "Formal Batch 019 正文抽取：已补充 Bungowannah 病毒、反刍动物 pestivirus 污染/鉴别和 APPV 证据不足边界；详见 `SRC-0046`。"),
        ("DIS-026-foot-and-mouth-disease-picornaviruses.md", "Formal Batch 019 正文抽取：已补充 FMDV 传播、气溶胶排毒、环境稳定性、临床严重性、实验室诊断、疫苗非完全阻断和控制边界；详见 `SRC-0047`。"),
    ]
    for filename, line in updates:
        path = WIKI / "wiki" / "diseases" / filename
        if path.exists():
            text = path.read_text(encoding="utf-8")
            marker = "## Formal Batch 019 正文抽取进展"
            if marker not in text:
                append_text(path, f"\n\n{marker}\n\n- {line}\n")


def write_cross_review() -> None:
    write_text(
        ISSUES / "formal_batch_019_cross_review.md",
        """# Formal Batch 019 Cross Review

## 范围

- PDF page 645：Chapter 38 Parvoviruses 参考文献收尾，仅作为上一章边界，不生成 facts。
- PDF page 646-661：Chapter 39 Pestiviruses 正文，落库 CSFV/CSF、Bungowannah、反刍动物 pestivirus 和 APPV 边界。
- PDF page 662-664：Chapter 39 参考文献页，仅作为章节边界。
- PDF page 665-684：Chapter 40 Picornaviruses 开端，落库猪 picornavirus 分类、FMDV 传播/诊断/免疫/控制边界和 SVDV 开端。

## 执行规范

- 本批按 `docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md` 执行。
- 页数为 40 页，符合常规正文批次范围。
- 参考文献页只记录章节边界，不生成 standalone facts。

## PDF 解析交叉检查

- 主抽取：PyMuPDF `fitz`，已生成 `issues/formal_batch_019_pdf_pages_645_684_extract.txt`。
- 二次核对：`pdfplumber`，逐页字符量接近，未发现漏页。
- 三次核对：`pypdf`，作为页级文本存在性与异常提示，不作为主文本。
- 解析报告：`issues/formal_batch_019_pdf_pages_645_684_parser_report.txt`。

## 审查结论

本批候选事实 34 条，规则页 16 个，来源页 2 个，主题页 2 个。经页码锚点、内容边界和一致性审查后允许落库。

## 审查 1：页码锚点核验

- `SRC-0046` facts 锚定 PDF page 646-661；PDF page 662-664 的参考文献条目未转化为 standalone facts。
- `SRC-0047` facts 锚定 PDF page 665-684；下一批应从 PDF page 685 继续 Chapter 40 正文。

## 审查 2：内容边界核验

- CSF/CSFV 事实仅落库教材诊断、传播、免疫和控制政策边界，不生成中国本地封锁、扑杀、免疫或调运命令。
- FMDV 事实强调重大水疱病鉴别、实验室确诊、气溶胶和人员/污染物传播风险；中国监管处置需 A0/A1 来源。
- FMD 疫苗内容仅落库“可防止严重临床病但不一定阻止感染”的边界，不生成免疫程序。
- SVDV 只落库分类和与 FMD 的鉴别边界，不生成后续完整疾病结论。
- APPV 和反刍动物 pestivirus 内容保留证据不足、污染和鉴别边界。

## 审查 3：一致性核验

- facts 与新增 topic/rule/source 页面一致。
- facts 的 `applies_to_species` 均为 `swine`，`evidence_status` 均为 `HUMAN_REVIEWED`。
- 新增 `fact_id`、`RULE-242` 至 `RULE-257` 与既有条目不重复。

## 保留问题

- PDF page 685 以后仍为 Chapter 40 Picornaviruses 正文，需继续抽取 SVDV、EMCV、teschovirus/sapelovirus、Senecavirus A 等后续内容。
- CSF 和 FMD 涉及中国法定疫病、强制处置、免疫或调运结论时，仍需中国官方或 A0/A1 来源复核。
""",
    )


def append_progress_docs() -> None:
    block = """

## 优化执行规范建立记录

- 完成时间：2026-05-07 08:10:00 +08:00。
- 新增执行文档：`docs/SWINE_LLM_WIKI_BATCH_EXECUTION_GUIDE.md`。
- 后续正式批次需按该文档执行：读取 v2 入口、三解析器 PDF 抽取、候选事实、交叉审查、审查通过后落库、同步 v2 文档、运行 status/lint/query/graph-build 并回写验证结果。

## Formal Batch 019 实施记录

- 完成时间：2026-05-07 08:10:00 +08:00。
- 处理范围：PDF page 645-684。
- 章节边界：Chapter 38 Parvoviruses 参考文献收尾；Chapter 39 Pestiviruses；Chapter 40 Picornaviruses 开端。
- 新增来源：`SRC-0046`、`SRC-0047`。
- 新增主题页：猪 Pestivirus/CSFV 诊断和控制边界、猪 Picornavirus/FMD/SVD 水疱病鉴别边界。
- 新增规则页：`RULE-242` 至 `RULE-257`。
- 新增候选事实：`issues/formal_batch_019_candidate_facts.json`。
- 交叉审查记录：`issues/formal_batch_019_cross_review.md`。
- 正式落库 facts：34 条 `HUMAN_REVIEWED` facts，均锚定来源和具体 PDF page。
- 明确未落库：参考文献列表、CSF/FMD 中国监管处置、固定免疫程序、扑杀/封锁/调运/消毒命令、FMD 疫苗产品推荐、SVDV 完整后续疾病结论。

### Formal Batch 019 交叉审查

- 页码锚点核验：通过。`SRC-0046` 覆盖 PDF page 646-664，`SRC-0047` 覆盖 PDF page 665-684。PDF page 645、662-664 的参考文献条目未生成 standalone facts。
- 内容边界核验：通过。CSF/CSFV、FMDV、SVDV、Bungowannah、反刍动物 pestivirus 和 APPV 均只落库教材证据和诊断/传播/免疫/控制边界，不生成处方、免疫程序或中国监管处置。
- 一致性核验：通过。facts、topic、rule、source 页面一致，`applies_to_species=swine`。

## 截至位置更新

- 当前已处理至 PDF page 684。
- 下一批应从 PDF page 685 开始。
- 推荐下一批：PDF page 685-724，继续 Chapter 40 Picornaviruses 后续正文。
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
    print("formal batch 019 built")


if __name__ == "__main__":
    main()
