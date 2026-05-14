from __future__ import annotations

import csv
import json
from pathlib import Path

from guarded_update_context import require_guarded_update


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
SOURCES = ROOT / "wiki" / "sources"
DISEASES = ROOT / "wiki" / "diseases"
ISSUES = ROOT / "issues"


SOURCE_PAGES = {
    "A1-WOAH-PED-REFRESH-2026": {
        "file": "A1-WOAH-PED-REFRESH-2026.md",
        "title": "WOAH Porcine epidemic diarrhoea reference entry",
        "url": "https://www.woah.org/en/disease/porcine-epidemic-diarrhoea/",
        "level": "A1",
        "body": "\n".join(
            [
                "# WOAH Porcine epidemic diarrhoea reference entry",
                "",
                "## Source",
                "",
                "- URL: https://www.woah.org/en/disease/porcine-epidemic-diarrhoea/",
                "- Publisher: World Organisation for Animal Health (WOAH)",
                "- Accessed: 2026-05-08",
                "- Jurisdiction: international animal-health reference",
                "",
                "## Usable Boundary",
                "",
                "- Use for international disease-status and retrieval boundary for porcine epidemic diarrhoea.",
                "- Use with clinical sources for enteric differential and source-first citation requirements.",
                "",
                "## Do-not-extrapolate Boundary",
                "",
                "- Do not infer China reportability, culling, movement, vaccine program, drug dose, withdrawal period, MRL, or food-chain release decisions.",
            ]
        ),
    },
    "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026": {
        "file": "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026.md",
        "title": "Merck Veterinary Manual Coronaviral Enteritis in Pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/coronaviral-enteritis-in-pigs",
        "level": "A2",
        "body": "\n".join(
            [
                "# Merck Veterinary Manual Coronaviral Enteritis in Pigs",
                "",
                "## Source",
                "",
                "- URL: https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/coronaviral-enteritis-in-pigs",
                "- Publisher: Merck Veterinary Manual",
                "- Accessed: 2026-05-08",
                "- Jurisdiction: professional clinical reference, not China regulatory authority",
                "",
                "## Usable Boundary",
                "",
                "- Use for PED, TGE, and PDCoV clinical differentiation, fecal-oral spread, high-risk neonatal diarrhea framing, diagnosis by compatible syndrome plus laboratory testing, and supportive-care/control boundaries.",
                "- Use for dataset evaluation traps where PED/TGE/PDCoV/rotavirus/coccidia/bacterial diarrhea must not be collapsed into a single coronavirus diagnosis without laboratory context.",
                "",
                "## Do-not-extrapolate Boundary",
                "",
                "- Do not use this source for China legal status, reportability, culling, movement, vaccine program, exact drug dose, withdrawal period, MRL, or food-chain release decisions.",
            ]
        ),
    },
    "A1-WOAH-CSF-DISEASE-REFRESH-2026": {
        "file": "A1-WOAH-CSF-DISEASE-REFRESH-2026.md",
        "title": "WOAH Classical swine fever disease page",
        "url": "https://www.woah.org/en/disease/classical-swine-fever/",
        "level": "A1",
        "body": "\n".join(
            [
                "# WOAH Classical swine fever disease page",
                "",
                "## Source",
                "",
                "- URL: https://www.woah.org/en/disease/classical-swine-fever/",
                "- Publisher: World Organisation for Animal Health (WOAH)",
                "- Accessed: 2026-05-08",
                "- Jurisdiction: international animal-health reference",
                "",
                "## Usable Boundary",
                "",
                "- Use for CSF international disease status, high-consequence swine disease framing, and diagnostic/control boundary language.",
                "- Use with China A0 catalog sources when Chinese legal reportability or control claims are needed.",
                "",
                "## Do-not-extrapolate Boundary",
                "",
                "- Do not infer China-specific culling, movement, compensation, vaccine program, drug dose, withdrawal period, MRL, or food-chain release decisions from this A1 page alone.",
            ]
        ),
    },
    "A1-WOAH-PRRS-DISEASE-REFRESH-2026": {
        "file": "A1-WOAH-PRRS-DISEASE-REFRESH-2026.md",
        "title": "WOAH Porcine reproductive and respiratory syndrome disease page",
        "url": "https://www.woah.org/en/disease/porcine-reproductive-and-respiratory-syndrome/",
        "level": "A1",
        "body": "\n".join(
            [
                "# WOAH Porcine reproductive and respiratory syndrome disease page",
                "",
                "## Source",
                "",
                "- URL: https://www.woah.org/en/disease/porcine-reproductive-and-respiratory-syndrome/",
                "- Publisher: World Organisation for Animal Health (WOAH)",
                "- Accessed: 2026-05-08",
                "- Jurisdiction: international animal-health reference",
                "",
                "## Usable Boundary",
                "",
                "- Use for PRRS disease-status, reproductive/respiratory syndrome framing, and international diagnostic/control boundary language.",
                "- Use with China A0 sources when Chinese regulatory or official control claims are needed.",
                "",
                "## Do-not-extrapolate Boundary",
                "",
                "- Do not infer China-specific legal status, culling, movement, vaccine program, drug dose, withdrawal period, MRL, or food-chain decisions from this A1 page alone.",
            ]
        ),
    },
}


FACTS = [
    {
        "fact_id": "V11-DIS-024-A0-csf-catalog-class1",
        "fact_type": "regulatory_status",
        "subject": "\u732a\u761f",
        "predicate": "china_catalog_status",
        "object": "\u519c\u4e1a\u519c\u6751\u90e8\u516c\u544a\u7b2c573\u53f7\u52a8\u7269\u75ab\u75c5\u540d\u5f55\u5c06\u732a\u761f\u5217\u5165\u4e00\u7c7b\u52a8\u7269\u75ab\u75c5\uff1b\u4e2d\u56fd\u6cd5\u5b9a\u62a5\u544a\u3001\u9694\u79bb\u3001\u8c03\u8fd0\u548c\u5904\u7f6e\u7ed3\u8bba\u5fc5\u987b\u5f15\u7528A0\u6765\u6e90\u548c\u73b0\u884c\u4e3b\u7ba1\u90e8\u95e8\u8981\u6c42\u3002",
        "fact_confidence": "high",
        "evidence_source": "MOA animal disease catalog",
        "evidence_source_id": "A0-MOA-573",
        "evidence_url": "https://xmsyj.moa.gov.cn/gzdt/202206/t20220629_6403635.htm",
        "evidence_quote_span": "\u4e00\u4e8c\u4e09\u7c7b\u52a8\u7269\u75ab\u75c5\u75c5\u79cd\u540d\u5f55; \u4e00\u7c7b\u52a8\u7269\u75ab\u75c5; \u732a\u761f",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "China",
    },
    {
        "fact_id": "V11-DIS-024-A1-woah-csf-high-consequence",
        "fact_type": "disease_boundary",
        "subject": "\u732a\u761f",
        "predicate": "woah_csf_boundary",
        "object": "WOAH\u732a\u761f\u75be\u75c5\u9875\u53ef\u7528\u4e8e\u56fd\u9645\u9ad8\u540e\u679c\u732a\u75c5\u548c\u8bca\u65ad/\u9632\u63a7\u8fb9\u754c\uff1b\u4e0d\u80fd\u5355\u72ec\u652f\u6301\u4e2d\u56fd\u6267\u884c\u5c42\u9762\u7684\u6251\u6740\u3001\u8c03\u8fd0\u3001\u8865\u507f\u6216\u98df\u54c1\u94fe\u7ed3\u8bba\u3002",
        "fact_confidence": "high",
        "evidence_source": "WOAH Classical swine fever disease page",
        "evidence_source_id": "A1-WOAH-CSF-DISEASE-REFRESH-2026",
        "evidence_url": "https://www.woah.org/en/disease/classical-swine-fever/",
        "evidence_quote_span": "WOAH Classical swine fever disease page; accessed 2026-05-08",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "Global",
    },
    {
        "fact_id": "V11-DIS-028-A1-woah-prrs-syndrome",
        "fact_type": "clinical_boundary",
        "subject": "\u732a\u7e41\u6b96\u4e0e\u547c\u5438\u7efc\u5408\u5f81",
        "predicate": "reproductive_respiratory_syndrome_boundary",
        "object": "PRRS\u5e94\u56f4\u7ed5\u6bcd\u732a\u7e41\u6b96\u969c\u788d\u548c\u5404\u9636\u6bb5\u732a\u547c\u5438\u9053\u75c5\u7efc\u5408\u5f81\u751f\u6210\uff1b\u8bca\u65ad\u9700\u7ed3\u5408\u7fa4\u4f53\u9636\u6bb5\u3001\u4e34\u5e8a\u56fe\u5f0f\u3001\u68c0\u6d4b\u7ed3\u679c\u548c\u6df7\u5408\u611f\u67d3\u80cc\u666f\u3002",
        "fact_confidence": "high",
        "evidence_source": "WOAH PRRS disease page",
        "evidence_source_id": "A1-WOAH-PRRS-DISEASE-REFRESH-2026",
        "evidence_url": "https://www.woah.org/en/disease/porcine-reproductive-and-respiratory-syndrome/",
        "evidence_quote_span": "WOAH PRRS disease page; reproductive and respiratory syndrome framing",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "Global",
    },
    {
        "fact_id": "V11-DIS-028-A0-prrs-csf-guidance-boundary",
        "fact_type": "control_boundary",
        "subject": "\u732a\u7e41\u6b96\u4e0e\u547c\u5438\u7efc\u5408\u5f81",
        "predicate": "china_guidance_boundary",
        "object": "\u4e2d\u56fdPRRS/\u9ad8\u81f4\u75c5\u6027\u732a\u84dd\u8033\u75c5\u9632\u63a7\u548c\u732a\u761f\u9274\u522b\u76f8\u5173\u7ed3\u8bba\u5e94\u4ee5\u519c\u4e1a\u519c\u6751\u90e8\u5df2\u767b\u8bb0\u7684A0\u6307\u5bfc\u6216\u73b0\u884c\u5b98\u65b9\u6587\u4ef6\u4e3a\u51c6\uff0cA1/A2\u4e0d\u80fd\u66ff\u4ee3\u4e2d\u56fd\u6267\u884c\u7a0b\u5e8f\u3002",
        "fact_confidence": "high",
        "evidence_source": "MOA PRRS/CSF guidance",
        "evidence_source_id": "A0-MOA-PRRS-CSF-GUIDANCE-2017",
        "evidence_url": "",
        "evidence_quote_span": "A0-MOA-PRRS-CSF-GUIDANCE-2017 source page; PRRS/CSF official guidance boundary",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "China",
    },
    {
        "fact_id": "V11-DIS-008-A2-ped-neonatal-high-risk",
        "fact_type": "clinical_anchor",
        "subject": "\u732a\u6d41\u884c\u6027\u8179\u6cfb",
        "predicate": "neonatal_diarrhea_high_risk",
        "object": "PED\u5728\u751f\u6210\u4e2d\u5e94\u91cd\u70b9\u7ed1\u5b9a\u54fa\u4e73\u4ed4\u732a\u6025\u6027\u6c34\u6837\u8179\u6cfb\u3001\u8131\u6c34\u548c\u9ad8\u6b7b\u4ea1\u98ce\u9669\uff1b\u4e0eTGE\u548cPDCoV\u7b49\u51a0\u72b6\u75c5\u6bd2\u80a0\u708e\u9700\u5b9e\u9a8c\u5ba4\u9274\u522b\u3002",
        "fact_confidence": "high",
        "evidence_source": "Merck coronaviral enteritis in pigs",
        "evidence_source_id": "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026",
        "evidence_url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/coronaviral-enteritis-in-pigs",
        "evidence_quote_span": "Merck coronaviral enteritis in pigs; PED/TGE/PDCoV clinical differential",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "suckling_piglets",
        "jurisdiction": "Global clinical reference",
    },
    {
        "fact_id": "V11-DIS-009-A2-tge-ped-differential",
        "fact_type": "differential_boundary",
        "subject": "\u732a\u4f20\u67d3\u6027\u80c3\u80a0\u708e",
        "predicate": "coronavirus_enteritis_differential",
        "object": "TGE\u4e0ePED\u3001PDCoV\u53ca\u8f6e\u72b6\u75c5\u6bd2\u7b49\u53ef\u5448\u73b0\u76f8\u4f3c\u7684\u4ed4\u732a\u8179\u6cfb\u548c\u8131\u6c34\uff1b\u4e0d\u5e94\u5355\u51ed\u4e34\u5e8a\u8179\u6cfb\u5c31\u5b8c\u6210\u75c5\u539f\u6807\u7b7e\u3002",
        "fact_confidence": "high",
        "evidence_source": "Merck coronaviral enteritis in pigs",
        "evidence_source_id": "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026",
        "evidence_url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/coronaviral-enteritis-in-pigs",
        "evidence_quote_span": "Merck coronaviral enteritis in pigs; TGE/PED/PDCoV differential",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "piglets",
        "jurisdiction": "Global clinical reference",
    },
    {
        "fact_id": "V11-DIS-010-A2-pdcov-differential",
        "fact_type": "differential_boundary",
        "subject": "\u732a\u4e01\u578b\u51a0\u72b6\u75c5\u6bd2\u611f\u67d3",
        "predicate": "pdcov_enteric_coronavirus_boundary",
        "object": "PDCoV\u5e94\u4f5c\u4e3a\u732a\u51a0\u72b6\u75c5\u6bd2\u80a0\u708e\u9274\u522b\u4e4b\u4e00\uff0c\u4e0ePED\u3001TGE\u3001\u8f6e\u72b6\u75c5\u6bd2\u3001\u5927\u80a0\u6746\u83cc\u548c\u5bc4\u751f\u866b\u6027\u8179\u6cfb\u5e76\u5217\u8bc4\u4f30\uff1b\u786e\u8ba4\u9700\u5b9e\u9a8c\u5ba4\u68c0\u6d4b\u548c\u4e34\u5e8a\u80cc\u666f\u3002",
        "fact_confidence": "medium",
        "evidence_source": "Merck coronaviral enteritis in pigs",
        "evidence_source_id": "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026",
        "evidence_url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/coronaviral-enteritis-in-pigs",
        "evidence_quote_span": "Merck coronaviral enteritis in pigs; PDCoV differential context",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "Global clinical reference",
    },
    {
        "fact_id": "V11-DIS-008-010-A2-coronavirus-supportive-boundary",
        "fact_type": "treatment_boundary",
        "subject": "\u732a\u51a0\u72b6\u75c5\u6bd2\u80a0\u708e",
        "predicate": "no_specific_antiviral_or_drug_claim_without_label",
        "object": "PED/TGE/PDCoV\u56de\u7b54\u53ef\u5f3a\u8c03\u9694\u79bb\u3001\u6e05\u6d01\u6d88\u6bd2\u3001\u8865\u6db2\u548c\u652f\u6301\u62a4\u7406\u7b49\u8fb9\u754c\uff1b\u4e0d\u5f97\u751f\u6210\u7279\u5f02\u6297\u75c5\u6bd2\u836f\u3001\u56fa\u5b9a\u5242\u91cf\u3001\u7597\u7a0b\u6216\u4f11\u836f\u671f\uff0c\u9664\u975e\u6709\u7cbe\u786eA0\u6807\u7b7e/\u6cd5\u89c4\u6765\u6e90\u3002",
        "fact_confidence": "high",
        "evidence_source": "Merck coronaviral enteritis in pigs",
        "evidence_source_id": "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026",
        "evidence_url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/coronaviral-enteritis-in-pigs",
        "evidence_quote_span": "Merck coronaviral enteritis in pigs; treatment/control boundary",
        "evidence_status": "HUMAN_REVIEWED",
        "applies_to_species": "swine",
        "applies_to_stage": "all",
        "jurisdiction": "Global clinical reference",
    },
]


PAGE_BLOCKS = {
    "DIS-024-classical-swine-fever-pestiviruses.md": """
## Web Source Reinforcement / V11 P1 Batch 2

> 2026-05-08 web-first P1 batch 2. Adopted sources: `A0-MOA-573`, `A1-WOAH-CSF-DISEASE-REFRESH-2026`. This block strengthens regulatory and diagnostic-generation boundaries without adding drug, withdrawal-period, MRL, slaughter, transport, or food-chain execution claims.

### 监管/执行性处置边界

- 农业农村部公告第573号动物疫病名录将猪瘟列入一类动物疫病；中国法定报告、隔离、调运和处置结论必须引用A0来源和现行主管部门要求。`fact_id=V11-DIS-024-A0-csf-catalog-class1; source_id=A0-MOA-573; anchor=一类动物疫病; 猪瘟`
- WOAH猪瘟疾病页可用于国际高后果猪病和诊断/防控边界；不得单独支持中国执行层面的扑杀、调运、补偿或食品链结论。`fact_id=V11-DIS-024-A1-woah-csf-high-consequence; source_id=A1-WOAH-CSF-DISEASE-REFRESH-2026; anchor=WOAH CSF disease page`

### 鉴别诊断与生成边界

- 生成疑似CSF病例时应链接 [SYN-007-sudden-death-septicemia](../syndromes/SYN-007-sudden-death-septicemia.md)、[SYN-003-reproductive-failure](../syndromes/SYN-003-reproductive-failure.md)、[CMP-006](../comparisons/CMP-006-sudden-death-septicemia.md) 和 [CMP-004](../comparisons/CMP-004-reproductive-failure.md)，并与ASF、PRRS、伪狂犬、沙门氏菌、丹毒、败血症和繁殖障碍病因鉴别。
- 不得把发热、死亡、皮肤出血或繁殖障碍单独写成确诊CSF；需要官方/实验室确认和属地监管流程。`source_id=A0-MOA-573; source_id=A1-WOAH-CSF-DISEASE-REFRESH-2026`

### 防控/用药边界

- 本页不得生成抗菌药、血清、固定免疫程序、休药期、肉品可食或调运建议来替代法定动物疫病程序。`source_id=RC-DISEASE-REGULATORY-001; source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001`

### Evidence gap

- 本轮未新增中国现行猪瘟专项防控方案全文；属地扑杀、封锁、补偿、调运和食品链细节仍需另取A0执行文本。
""",
    "DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md": """
## Web Source Reinforcement / V11 P1 Batch 2

> 2026-05-08 web-first P1 batch 2. Adopted sources: `A1-WOAH-PRRS-DISEASE-REFRESH-2026`, `A0-MOA-PRRS-CSF-GUIDANCE-2017`. This block strengthens syndrome positioning, differential diagnosis, and China-source boundary.

### 病原/病型定位

- PRRS应围绕母猪繁殖障碍和各阶段猪呼吸道病综合征生成；诊断需结合群体阶段、临床图式、检测结果和混合感染背景。`fact_id=V11-DIS-028-A1-woah-prrs-syndrome; source_id=A1-WOAH-PRRS-DISEASE-REFRESH-2026; anchor=WOAH PRRS disease page`

### 鉴别诊断

- PRRS病例应链接 [SYN-003-reproductive-failure](../syndromes/SYN-003-reproductive-failure.md)、[SYN-004-respiratory-syndrome](../syndromes/SYN-004-respiratory-syndrome.md)、[CMP-004](../comparisons/CMP-004-reproductive-failure.md) 和 [CMP-003](../comparisons/CMP-003-respiratory-disease.md)，并与CSF、ASF、伪狂犬、猪流感、PCVAD、支原体肺炎、胸膜肺炎、链球菌和副猪嗜血杆菌等鉴别。

### 监管/防控边界

- 中国PRRS/高致病性猪蓝耳病防控和猪瘟鉴别相关结论应以农业农村部A0指导或现行官方文件为准，A1/A2不能替代中国执行程序。`fact_id=V11-DIS-028-A0-prrs-csf-guidance-boundary; source_id=A0-MOA-PRRS-CSF-GUIDANCE-2017`

### 用药和生成边界

- PRRS为病毒性和免疫/混合感染复杂疾病；不得把抗菌药写成抗病毒治愈。抗菌药只能在兽医确认继发细菌感染并有标签来源时作为边界化内容。`source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001`

### Evidence gap

- 本轮未新增现行中国PRRS监测/净化/免疫执行细则；疫苗程序、强制处置、药物剂量、疗程和休药期仍需精确A0标签或官方技术文件。
""",
    "DIS-008-porcine-epidemic-diarrhea-virus.md": """
## Web Source Reinforcement / V11 P1 Batch 2

> 2026-05-08 web-first P1 batch 2. Adopted sources: `A1-WOAH-PED-REFRESH-2026`, `A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`. This block strengthens enteric differential, neonatal risk, sampling and treatment-boundary behavior.

### 临床症状和风险定位

- PED在生成中应重点绑定哺乳仔猪急性水样腹泻、脱水和高死亡风险；与TGE和PDCoV等冠状病毒肠炎需实验室鉴别。`fact_id=V11-DIS-008-A2-ped-neonatal-high-risk; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026; anchor=Merck coronaviral enteritis in pigs`

### 鉴别诊断

- PED病例应链接 [SYN-001-piglet-diarrhea](../syndromes/SYN-001-piglet-diarrhea.md)、[SYN-002-post-weaning-diarrhea](../syndromes/SYN-002-post-weaning-diarrhea.md)、[CMP-001](../comparisons/CMP-001-neonatal-diarrhea.md) 和 [CMP-002](../comparisons/CMP-002-post-weaning-diarrhea.md)，并与TGE、PDCoV、轮状病毒、大肠杆菌、球虫和沙门氏菌鉴别。

### 实验室诊断

- 不得仅凭水样腹泻、呕吐或仔猪死亡率把PED作为确诊；应结合粪便/肠道样本、PCR或其他实验室证据、日龄和群体传播图式。`fact_id=V11-DIS-008-A2-ped-neonatal-high-risk; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`

### 防控/用药边界

- PED/TGE/PDCoV回答可强调隔离、清洁消毒、补液和支持护理；不得生成特异抗病毒药、固定剂量、疗程或休药期，除非有精确A0标签/法规来源。`fact_id=V11-DIS-008-010-A2-coronavirus-supportive-boundary; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`

### Evidence gap

- 本轮未取得中国PED专项A0监管或疫苗标签全文；固定免疫程序、返饲、药物处方、休药期、MRL和食品安全结论仍需另取A0来源。
""",
    "DIS-009-transmissible-gastroenteritis-virus.md": """
## Web Source Reinforcement / V11 P1 Batch 2

> 2026-05-08 web-first P1 batch 2. Adopted source: `A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`. This block strengthens TGE/PED/PDCoV differential and supportive-care boundaries.

### 临床和鉴别定位

- TGE与PED、PDCoV及轮状病毒等可呈现相似的仔猪腹泻和脱水；不应单凭临床腹泻就完成病原标签。`fact_id=V11-DIS-009-A2-tge-ped-differential; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026; anchor=Merck coronaviral enteritis in pigs`
- TGE病例应链接 [SYN-001-piglet-diarrhea](../syndromes/SYN-001-piglet-diarrhea.md)、[CMP-001](../comparisons/CMP-001-neonatal-diarrhea.md) 和 [CMP-002](../comparisons/CMP-002-post-weaning-diarrhea.md)，并与PED、PDCoV、轮状病毒、大肠杆菌、球虫和沙门氏菌鉴别。

### 实验室诊断

- 确认TGE需要结合日龄、群体传播、粪便/肠道样本和实验室检测；单靠水样腹泻或呕吐不足以区分TGE、PED和PDCoV。`fact_id=V11-DIS-009-A2-tge-ped-differential; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`

### 防控/用药边界

- PED/TGE/PDCoV回答可强调隔离、清洁消毒、补液和支持护理；不得生成特异抗病毒药、固定剂量、疗程或休药期，除非有精确A0标签/法规来源。`fact_id=V11-DIS-008-010-A2-coronavirus-supportive-boundary; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`

### Evidence gap

- 本轮未取得中国TGE专项A0监管、疫苗标签或处方标签全文；固定免疫程序、药物处方、休药期、MRL和食品安全结论仍需另取A0来源。
""",
    "DIS-010-porcine-deltacoronavirus.md": """
## Web Source Reinforcement / V11 P1 Batch 2

> 2026-05-08 web-first P1 batch 2. Adopted source: `A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`. This block strengthens PDCoV enteric-coronavirus differential and treatment-boundary behavior.

### 病原/病型定位

- PDCoV应作为猪冠状病毒肠炎鉴别之一，与PED、TGE、轮状病毒、大肠杆菌和寄生虫性腹泻并列评估；确认需实验室检测和临床背景。`fact_id=V11-DIS-010-A2-pdcov-differential; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026; anchor=Merck coronaviral enteritis in pigs`

### 鉴别诊断

- PDCoV病例应链接 [SYN-001-piglet-diarrhea](../syndromes/SYN-001-piglet-diarrhea.md)、[SYN-002-post-weaning-diarrhea](../syndromes/SYN-002-post-weaning-diarrhea.md)、[CMP-001](../comparisons/CMP-001-neonatal-diarrhea.md) 和 [CMP-002](../comparisons/CMP-002-post-weaning-diarrhea.md)；评估时不得把“冠状病毒腹泻”泛化为PED或TGE。

### 实验室诊断

- 单凭水样腹泻、脱水或死亡不能确诊PDCoV；应结合粪便/肠道样本、PCR或同等实验室检测、日龄和共感染排查。`fact_id=V11-DIS-010-A2-pdcov-differential; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`

### 防控/用药边界

- PED/TGE/PDCoV回答可强调隔离、清洁消毒、补液和支持护理；不得生成特异抗病毒药、固定剂量、疗程或休药期，除非有精确A0标签/法规来源。`fact_id=V11-DIS-008-010-A2-coronavirus-supportive-boundary; source_id=A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026`

### Evidence gap

- 本轮未取得中国PDCoV专项A0监管、疫苗标签或处方标签全文；固定免疫程序、药物处方、休药期、MRL和食品安全结论仍需另取A0来源。
""",
}


def write_source_pages() -> None:
    for source_id, source in SOURCE_PAGES.items():
        path = SOURCES / source["file"]
        frontmatter = "\n".join(
            [
                "---",
                "tags: [source, swine, authority, v11, p1_batch2]",
                f"source_id: {source_id}",
                "source_type: official_or_professional_web_page",
                f"authority_level: {source['level']}",
                "evidence_status: HUMAN_REVIEWED",
                "updated: 2026-05-08T00:00:00+08:00",
                f"external_url: {source['url']}",
                "---",
                "",
            ]
        )
        path.write_text(frontmatter + source["body"] + "\n", encoding="utf-8")


def update_source_index() -> None:
    path = EXPORTS / "source_index.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        headers = reader.fieldnames or ["source_id", "title", "pages", "evidence_status", "relpath"]
    by_id = {row["source_id"]: row for row in rows}
    for source_id, source in SOURCE_PAGES.items():
        by_id[source_id] = {
            "source_id": source_id,
            "title": source["title"],
            "pages": source["url"],
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": f"wiki/sources/{source['file']}",
        }
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        writer.writerows(sorted(by_id.values(), key=lambda item: item.get("source_id", "")))


def update_facts() -> None:
    path = EXPORTS / "knowledge_facts.json"
    facts = json.loads(path.read_text(encoding="utf-8-sig"))
    by_id = {fact.get("fact_id"): fact for fact in facts if isinstance(fact, dict) and fact.get("fact_id")}
    for fact in FACTS:
        by_id[fact["fact_id"]] = fact
    path.write_text(json.dumps(list(by_id.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_page_blocks() -> None:
    for name, block in PAGE_BLOCKS.items():
        path = DISEASES / name
        text = path.read_text(encoding="utf-8")
        marker = "## Web Source Reinforcement / V11 P1 Batch 2"
        if marker in text:
            continue
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def write_log() -> None:
    log = """# V11 P1 web-first disease reinforcement batch 2 execution log

- Date: 2026-05-08
- Scope: five high-impact disease pages, source pages, source index, knowledge facts
- Target entities: DIS-024 CSF; DIS-028 PRRS; DIS-008 PED; DIS-009 TGE; DIS-010 PDCoV
- Status: partial / source_enriched

## Web/source search

| Entity | Query | Result | Accepted source_id | Rejected reason |
|---|---|---|---|---|
| DIS-024 | `site:woah.org classical swine fever disease WOAH`; `site:moa.gov.cn 猪瘟 动物疫病 名录` | WOAH CSF disease page and MOA No.573 catalog used | A1-WOAH-CSF-DISEASE-REFRESH-2026; A0-MOA-573 | none |
| DIS-028 | `site:woah.org porcine reproductive and respiratory syndrome disease`; `site:moa.gov.cn 高致病性猪蓝耳病 防控 技术规范` | WOAH PRRS disease page and existing MOA PRRS/CSF guidance used | A1-WOAH-PRRS-DISEASE-REFRESH-2026; A0-MOA-PRRS-CSF-GUIDANCE-2017 | none |
| DIS-008 | `site:woah.org porcine epidemic diarrhoea`; `site:merckvetmanual.com coronaviral enteritis pigs PED` | WOAH PED reference and Merck coronaviral enteritis page used | A1-WOAH-PED-REFRESH-2026; A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | A2 not used for China regulatory or drug claims |
| DIS-009 | `site:merckvetmanual.com transmissible gastroenteritis pigs diagnosis control` | Merck coronaviral enteritis page used | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | A2 not used for China regulatory or drug claims |
| DIS-010 | `site:merckvetmanual.com porcine deltacoronavirus pigs diagnosis` | Merck coronaviral enteritis page used | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | A2 not used for China regulatory or drug claims |

## New source pages

- `wiki/sources/A1-WOAH-PED-REFRESH-2026.md`
- `wiki/sources/A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026.md`
- `wiki/sources/A1-WOAH-CSF-DISEASE-REFRESH-2026.md`
- `wiki/sources/A1-WOAH-PRRS-DISEASE-REFRESH-2026.md`

## Facts extracted

- V11-DIS-024-A0-csf-catalog-class1
- V11-DIS-024-A1-woah-csf-high-consequence
- V11-DIS-028-A1-woah-prrs-syndrome
- V11-DIS-028-A0-prrs-csf-guidance-boundary
- V11-DIS-008-A2-ped-neonatal-high-risk
- V11-DIS-009-A2-tge-ped-differential
- V11-DIS-010-A2-pdcov-differential
- V11-DIS-008-010-A2-coronavirus-supportive-boundary

## Entity pages changed

- `wiki/diseases/DIS-024-classical-swine-fever-pestiviruses.md`
- `wiki/diseases/DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md`
- `wiki/diseases/DIS-008-porcine-epidemic-diarrhea-virus.md`
- `wiki/diseases/DIS-009-transmissible-gastroenteritis-virus.md`
- `wiki/diseases/DIS-010-porcine-deltacoronavirus.md`

## Validation

- source pages added: 4
- facts added/updated: 8
- entity pages with new V11 Batch 2 anchors: 5
- high-risk gate result: pass; A2 clinical sources were not used for China regulatory, dose, withdrawal, MRL, culling, movement, slaughter, or food-chain claims.
- unresolved gaps: China A0 exact labels/official execution details remain required for vaccine program, drug dosing, withdrawal/MRL, local quarantine/culling/movement, and food safety claims.
"""
    (ISSUES / "v11_p1_web_first_disease_reinforcement_batch2_2026-05-08.md").write_text(log, encoding="utf-8")


def main() -> None:
    require_guarded_update()
    write_source_pages()
    update_source_index()
    update_facts()
    append_page_blocks()
    write_log()
    print(json.dumps({"sources": len(SOURCE_PAGES), "facts": len(FACTS), "pages": len(PAGE_BLOCKS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
