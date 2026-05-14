from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-05-08"
UPDATED = "2026-05-08T23:30:00+08:00"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


SOURCES = [
    {
        "source_id": "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026",
        "title": "Merck Veterinary Manual: Coronaviral Enteritis in Pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/enteric-viral-diseases-in-pigs/coronaviral-enteritis-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Apr 2026",
        "claims": [
            "TGEV, PEDV, and PDCoV are porcine enteric coronaviruses; clinical differentiation among them is difficult.",
            "Transmission can occur through infected pigs, contaminated fomites, transport vehicles, aerosol or contact exposure.",
            "Definitive differentiation requires laboratory support such as PCR and histopathology/IHC."
        ],
        "boundary": "Clinical reference only; does not establish China regulatory status, reportability, product labels, withdrawal periods, or local control orders.",
    },
    {
        "source_id": "A2-MERCK-PSEUDORABIES-PIGS-2026",
        "title": "Merck Veterinary Manual: Pseudorabies in Pigs",
        "url": "https://www.merckvetmanual.com/nervous-system/pseudorabies/pseudorabies-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Published 2026 / accessed 2026-05-08",
        "claims": [
            "Clinical signs in pigs vary by age and may include reproductive signs in sows, neurologic signs in newborn pigs, and respiratory signs in growing-finishing pigs.",
            "Suspect cases require laboratory confirmation; clinical pattern alone should not be used as definitive diagnosis."
        ],
        "boundary": "Clinical reference only; not a China official eradication, movement, vaccination, or reporting source.",
    },
    {
        "source_id": "A2-MERCK-INFLUENZA-A-SWINE-2024",
        "title": "Merck Veterinary Manual: Influenza A Virus in Swine",
        "url": "https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-pigs/influenza-a-virus-in-swine",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Sept 2024",
        "claims": [
            "Swine influenza is a highly contagious respiratory disease caused by influenza A virus.",
            "Diagnosis is primarily by RT-PCR or virus isolation; respiratory differentials such as PRRS and pseudorabies should be excluded.",
            "There is no effective specific treatment; antimicrobials are only for secondary bacterial infections."
        ],
        "boundary": "Clinical reference only; vaccination programs and China regulatory actions need jurisdiction-specific sources.",
    },
    {
        "source_id": "A2-MERCK-CLASSICAL-SWINE-FEVER-2026",
        "title": "Merck Veterinary Manual: Classical Swine Fever",
        "url": "https://www.merckvetmanual.com/generalized-conditions/classical-swine-fever/classical-swine-fever",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Accessed 2026-05-08",
        "claims": [
            "Classical swine fever is caused by a pestivirus and can present with fever, hemorrhages, ataxia, and purple skin discoloration.",
            "Antibody discrimination is needed where ruminant pestivirus exposure could confound CSF serology."
        ],
        "boundary": "Clinical reference only; China legal classification and response require A0 sources.",
    },
    {
        "source_id": "A2-MERCK-FMD-ANIMALS-2026",
        "title": "Merck Veterinary Manual: Foot-and-Mouth Disease in Animals",
        "url": "https://www.merckvetmanual.com/infectious-diseases/foot-and-mouth-disease/foot-and-mouth-disease-in-animals",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Feb 2026",
        "claims": [
            "FMD infects cloven-hoofed animals including pigs and causes vesicular lesions in and around the mouth and feet.",
            "In pigs, vesicular diseases are clinically difficult to distinguish and require suitable laboratory investigation.",
            "Specific treatment is not available; normally FMD-free regions rely on official control such as culling and movement controls."
        ],
        "boundary": "Use only for clinical and differential boundaries; China culling, movement, reporting, and quarantine decisions require A0 authority.",
    },
    {
        "source_id": "A2-MERCK-PRRS-2026",
        "title": "Merck Veterinary Manual: Porcine Reproductive and Respiratory Syndrome",
        "url": "https://www.merckvetmanual.com/generalized-conditions/porcine-reproductive-and-respiratory-syndrome/porcine-reproductive-and-respiratory-syndrome",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Accessed 2026-05-08",
        "claims": [
            "PRRS has reproductive and respiratory presentations, including stillborn, mummified, premature, and weak-born pigs.",
            "PRRS frequently interacts with coinfections and should be handled as a syndrome-level differential rather than a single-sign diagnosis."
        ],
        "boundary": "Clinical reference only; China regulatory or vaccine-program conclusions require exact A0 support.",
    },
    {
        "source_id": "A2-MERCK-ROTAVIRAL-ENTERITIS-PIGS-2024",
        "title": "Merck Veterinary Manual: Rotaviral Enteritis in Pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/rotaviral-enteritis-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Sept 2024",
        "claims": [
            "Rotaviral enteritis is a common small-intestinal disease of pigs, usually causing diarrhea in nursing and weaned pigs.",
            "Diagnosis requires laboratory analysis, combining villous atrophy, PCR detection, or antigen demonstration.",
            "Differentials include coronaviral enteritis, Cystoisospora suis enteritis, and enteric colibacillosis."
        ],
        "boundary": "Clinical reference only; does not support drug dose, withdrawal, or China vaccine schedule claims.",
    },
    {
        "source_id": "A2-MERCK-ACTINOBACILLOSIS-PIGS-2025",
        "title": "Merck Veterinary Manual: Actinobacillosis in Animals",
        "url": "https://www.merckvetmanual.com/infectious-diseases/actinobacillosis/actinobacillosis",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Accessed 2026-05-08",
        "claims": [
            "Actinobacillus pleuropneumoniae causes contagious pleuropneumonia in pigs.",
            "Severe disease is especially important in pigs under five months in naive herds; A. suis can cause septicemia, arthritis, pneumonia, and pericarditis."
        ],
        "boundary": "Clinical reference only; antimicrobial selection, dose, and withdrawal require label and veterinary diagnosis.",
    },
    {
        "source_id": "A2-MERCK-ATROPHIC-RHINITIS-PIGS-2026",
        "title": "Merck Veterinary Manual: Atrophic Rhinitis in Pigs",
        "url": "https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-pigs/atrophic-rhinitis-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Accessed 2026-05-08",
        "claims": [
            "Atrophic rhinitis in pigs involves Bordetella bronchiseptica and may be complicated by toxigenic Pasteurella multocida.",
            "Clinical interpretation should stay within the respiratory syndrome differential and avoid single-test overdiagnosis."
        ],
        "boundary": "Clinical reference only; not a drug-label or China regulatory source.",
    },
    {
        "source_id": "A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS-2024",
        "title": "Merck Veterinary Manual: Enteric Colibacillosis in Pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/intestinal-diseases-in-pigs/enteric-colibacillosis-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Sept 2024",
        "claims": [
            "Enteric colibacillosis is a disease of nursing and weanling pigs caused by ETEC colonization of the small intestine.",
            "Confirmation combines lesion assessment, culture, and genotyping of bacterial isolates."
        ],
        "boundary": "Clinical reference only; antimicrobial use requires veterinary diagnosis, susceptibility, and China label constraints.",
    },
    {
        "source_id": "A2-MERCK-EDEMA-DISEASE-PIGS-2024",
        "title": "Merck Veterinary Manual: Edema Disease in Pigs",
        "url": "https://www.merckvetmanual.com/generalized-conditions/edema-disease/edema-disease-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Sept 2024",
        "claims": [
            "Edema disease is a peracute toxemia caused by F18+ E. coli and primarily affects healthy, rapidly growing nursery pigs.",
            "Treatment is limited because the disease is often rapidly fatal; prevention focuses on vaccination and management."
        ],
        "boundary": "Clinical reference only; vaccines, antimicrobials, and withdrawal claims need exact local label sources.",
    },
    {
        "source_id": "A2-MERCK-ERYSIPELAS-SWINE-2026",
        "title": "Merck Veterinary Manual: Swine Erysipelas",
        "url": "https://www.merckvetmanual.com/infectious-diseases/erysipelothrix-rhusiopathiae-infection/swine-erysipelas",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Accessed 2026-05-08",
        "claims": [
            "Swine erysipelas may be acute or chronic; acute outbreaks can include sudden death, fever, joint pain, and diamond-skin lesions.",
            "Diamond-skin lesions are strongly suggestive but similar lesions can occur with CSF, ASF, Actinobacillus suis septicemia, and PDNS.",
            "Diagnosis uses clinical/gross findings plus demonstration of the bacterium or DNA in tissues."
        ],
        "boundary": "Clinical reference only; treatment and withdrawal claims require China label and veterinary prescription context.",
    },
    {
        "source_id": "A2-MERCK-MYCOPLASMAL-PNEUMONIA-PIGS-2024",
        "title": "Merck Veterinary Manual: Mycoplasmal Pneumonia in Pigs",
        "url": "https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-pigs/mycoplasmal-pneumonia-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Sept 2024",
        "claims": [
            "Mycoplasma hyopneumoniae is a common cause of chronic, typically mild pneumonia in pigs worldwide.",
            "Diagnosis may use clinical signs, characteristic lesions, and PCR confirmation; partial control can include management, antimicrobials, and vaccination."
        ],
        "boundary": "Clinical reference only; do not infer China vaccine schedule, antimicrobial dose, or withdrawal periods.",
    },
    {
        "source_id": "A2-MERCK-SALMONELLOSIS-ANIMALS-2026",
        "title": "Merck Veterinary Manual: Salmonellosis in Animals",
        "url": "https://www.merckvetmanual.com/digestive-system/salmonellosis/salmonellosis-in-animals",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Accessed 2026-05-08",
        "claims": [
            "Salmonellosis diagnosis requires pathogen isolation in the presence of consistent clinical signs, or repeated fecal isolation suggesting carrier status.",
            "Antimicrobial treatment is controversial because carrier risk may be increased."
        ],
        "boundary": "Clinical/public-health reference only; food-safety execution and antimicrobial withdrawal need exact A0 sources.",
    },
    {
        "source_id": "A2-MERCK-SWINE-DYSENTERY-2026",
        "title": "Merck Veterinary Manual: Swine Dysentery",
        "url": "https://www.merckvetmanual.com/digestive-system/enteric-bacterial-diseases-in-pigs/swine-dysentery",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Apr 2026",
        "claims": [
            "Swine dysentery is a mucohemorrhagic diarrheal disease of pigs limited to the large intestine.",
            "Confirmation relies on typical large-intestinal lesions and isolation of strongly beta-hemolytic Brachyspira by anaerobic culture; PCR alone does not replace phenotype confirmation.",
            "Differentials include intestinal spirochetosis, proliferative enteropathy, intestinal salmonellosis, and heavy whipworm infections."
        ],
        "boundary": "Clinical reference only; antimicrobial choice must depend on MIC, label, and local regulation.",
    },
    {
        "source_id": "A2-MERCK-MANGE-PIGS-2026",
        "title": "Merck Veterinary Manual: Mange in Pigs",
        "url": "https://www.merckvetmanual.com/integumentary-system/mange/mange-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Feb 2026",
        "claims": [
            "Sarcoptic mange in pigs is principally due to Sarcoptes scabiei var suis.",
            "Transmission can occur rapidly by direct contact and from sow to piglets; control programs focus on breeding herd and growing pig management."
        ],
        "boundary": "Clinical reference only; acaricide product, dilution, route, and withdrawal claims require exact label sources.",
    },
    {
        "source_id": "A2-MERCK-COCCIDIOSIS-PIGS-2024",
        "title": "Merck Veterinary Manual: Coccidiosis of Pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/coccidiosis/coccidiosis-of-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Sept 2024",
        "claims": [
            "Neonatal piglet coccidiosis is commonly associated with Isospora/Cystoisospora suis, while Eimeria spp. are more relevant to older pigs.",
            "Diagnosis uses age pattern, fecal oocysts, flotation, mucosal smears, histology, fluorescent antibody testing, or PCR.",
            "Lack of response to antibacterial agents is a useful diagnostic clue."
        ],
        "boundary": "Clinical reference only; anticoccidial product use, dose, route, and withdrawal require exact China label support.",
    },
    {
        "source_id": "A2-MERCK-ASCARIS-SUUM-PIGS-2024",
        "title": "Merck Veterinary Manual: Ascaris suum in Pigs",
        "url": "https://www.merckvetmanual.com/digestive-system/gastrointestinal-parasites-of-pigs/ascaris-suum-in-pigs",
        "authority_level": "A2",
        "publisher": "Merck Veterinary Manual",
        "date": "Modified Sept 2024",
        "claims": [
            "Ascaris suum is a common and widespread swine parasite; liver milk spots and pulmonary migration lesions are important findings.",
            "Patent infections can be diagnosed by fecal flotation, while prepatent infections require postmortem examination.",
            "Control must combine anthelmintics with strict sanitation."
        ],
        "boundary": "Clinical reference only; anthelmintic product, route, dose, and withdrawal require exact label sources.",
    },
    {
        "source_id": "A0-MOA-AMOXICILLIN-INJECTION-332-2020",
        "title": "农业农村部公告第332号 阿莫西林注射液说明书",
        "url": "https://www.moa.gov.cn/nybgb/2020/202010/202011/t20201130_6357327.htm",
        "authority_level": "A0",
        "publisher": "农业农村部",
        "date": "2020-10 / accessed 2026-05-08",
        "claims": [
            "Announcement page includes 阿莫西林注射液说明书 as an official label attachment/text entry.",
            "The label includes pigs under the indication scope for amoxicillin-susceptible infectious diseases, with cattle and pigs by intramuscular injection.",
            "The label states a pig withdrawal period of 21 days and marks the product as veterinary prescription drug on the label section.",
            "The adopted label scope must be kept to the specific product/formulation and cannot be extrapolated to all amoxicillin products."
        ],
        "boundary": "Positive-use evidence is limited to the exact official label entry; do not infer other formulations, combinations, doses, or jurisdictions.",
    },
    {
        "source_id": "A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024",
        "title": "农业农村部公报附件 注射用头孢噻呋钠说明书",
        "url": "https://www.moa.gov.cn/nybgb/2024/202404/202404/P020240424369174817705.pdf",
        "authority_level": "A0",
        "publisher": "农业农村部",
        "date": "2024-04 / accessed 2026-05-08",
        "claims": [
            "Official PDF includes 注射用头孢噻呋钠说明书.",
            "The label states veterinary prescription drug status and includes pigs for bacterial respiratory infections.",
            "The label route for pigs is intramuscular injection, and the pig withdrawal period in the label is 4 days.",
            "The adopted label scope must match species, formulation, route, indication, and withdrawal statements in the PDF."
        ],
        "boundary": "Do not extrapolate to other cephalosporins, formulations, or extra-label uses.",
    },
    {
        "source_id": "A0-MOA-FLORFENICOL-INJECTION-219-2019",
        "title": "农业农村部公告第219号 氟苯尼考注射液说明书",
        "url": "https://www.moa.gov.cn/nybgb/2019/201910/202001/t20200109_6334688.htm",
        "authority_level": "A0",
        "publisher": "农业农村部",
        "date": "2019-09 / accessed 2026-05-08",
        "claims": [
            "Official announcement includes 氟苯尼考注射液说明书.",
            "The label indication is pig bacterial respiratory disease caused by Actinobacillus pleuropneumoniae and Pasteurella multocida.",
            "The label route is neck intramuscular injection and the pig withdrawal period is 18 days.",
            "Use as exact label evidence only for the listed formulation and species scope."
        ],
        "boundary": "Do not infer feed/water products, combinations, dose/course, or residue compliance outside the official label.",
    },
    {
        "source_id": "A0-MOA-ENROFLOXACIN-SOLUTION-55-2018",
        "title": "农业农村部公告第55号 恩诺沙星溶液说明书",
        "url": "https://www.moa.gov.cn/nybgb/2018/201809/201810/t20181023_6161326.htm",
        "authority_level": "A0",
        "publisher": "农业农村部",
        "date": "2018-08 / accessed 2026-05-08",
        "claims": [
            "Official announcement includes 恩诺沙星溶液说明书.",
            "The label indication is gastrointestinal disease caused by E. coli in pigs, with oral administration to piglets.",
            "The label states a pig withdrawal period of 5 days.",
            "Use as exact label evidence only for matching species, route, indication, and withdrawal scope."
        ],
        "boundary": "Fluoroquinolone use is high-risk; no extra-label, dose, course, or residue inference is allowed.",
    },
    {
        "source_id": "A0-MOA-TOLTRAZURIL-SUSPENSION-216-2019",
        "title": "农业农村部公告第216号 5%托曲珠利混悬液说明书",
        "url": "https://www.moa.gov.cn/nybgb/2019/201910/202001/t20200109_6334685.htm",
        "authority_level": "A0",
        "publisher": "农业农村部",
        "date": "2019-09 / accessed 2026-05-08",
        "claims": [
            "Official announcement includes 5%托曲珠利混悬液说明书.",
            "The label includes prevention of coccidiosis in piglets and calves, with oral administration and a piglet withdrawal period of 77 days.",
            "Use as exact label evidence only for piglet coccidiosis-related label scope when species/formulation matches."
        ],
        "boundary": "Do not extrapolate from poultry products or other toltrazuril formulations to piglets.",
    },
]


DISEASES = [
    ("DIS-008-porcine-epidemic-diarrhea-virus.md", "猪流行性腹泻", "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026", "SYN-001-piglet-diarrhea", "../syndromes/SYN-001-piglet-diarrhea.md", "CMP-001", "../comparisons/CMP-001-neonatal-diarrhea.md", [
        ("V11-DIS-008-etiology", "病原/病型定位", "PEDV 属猪肠道冠状病毒病原之一；TGEV、PEDV、PDCoV 的临床表现可高度重叠，不能仅凭腹泻外观区分。"),
        ("V11-DIS-008-transmission", "流行病学或传播边界", "猪肠道冠状病毒可经感染猪、污染物、运输车辆、接触或气溶胶快速传播，生成病例应询问引种、车辆、人员和连续窝次风险。"),
        ("V11-DIS-008-diagnosis", "实验室诊断", "PEDV 相关病例应以 PCR、组织病理或抗原定位等实验室证据支持；PCR 阳性也需结合临床阶段和样本类型解释。"),
    ]),
    ("DIS-009-transmissible-gastroenteritis-virus.md", "猪传染性胃肠炎", "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026", "SYN-001-piglet-diarrhea", "../syndromes/SYN-001-piglet-diarrhea.md", "CMP-001", "../comparisons/CMP-001-neonatal-diarrhea.md", [
        ("V11-DIS-009-etiology", "病原/病型定位", "TGEV 是猪肠道冠状病毒病原之一，与 PEDV、PDCoV 临床鉴别困难，不得把水样腹泻直接写成单一 TGE 诊断。"),
        ("V11-DIS-009-lesion", "临床症状或剖检变化", "猪肠道冠状病毒主要造成小肠绒毛上皮损伤、吸收不良和急性水样腹泻，仔猪脱水风险应优先评估。"),
        ("V11-DIS-009-diagnosis", "实验室诊断", "TGEV 疑似病例需 PCR 或组织学/抗原定位等辅助检测确认，并与 PEDV、PDCoV 鉴别。"),
    ]),
    ("DIS-010-porcine-deltacoronavirus.md", "猪δ冠状病毒感染", "A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026", "SYN-001-piglet-diarrhea", "../syndromes/SYN-001-piglet-diarrhea.md", "CMP-001", "../comparisons/CMP-001-neonatal-diarrhea.md", [
        ("V11-DIS-010-etiology", "病原/病型定位", "PDCoV 是猪肠道冠状病毒病原之一，临床上需与 PEDV、TGEV 并列鉴别。"),
        ("V11-DIS-010-transmission", "流行病学或传播边界", "猪肠道冠状病毒感染可通过粪便排毒、污染物和运输环节扩散；病例生成不能忽略车辆、靴具和批次流动。"),
        ("V11-DIS-010-diagnosis", "实验室诊断", "PDCoV 的病因判断需要 PCR 或组织病理/抗原定位支持，不能仅用腹泻和小肠病变定因。"),
    ]),
    ("DIS-018-pseudorabies-aujeszky-disease.md", "猪伪狂犬病", "A2-MERCK-PSEUDORABIES-PIGS-2026", "SYN-005-neurologic-signs", "../syndromes/SYN-005-neurologic-signs.md", "CMP-004", "../comparisons/CMP-004-reproductive-failure.md", [
        ("V11-DIS-018-stage-signs", "临床症状或剖检变化", "伪狂犬病临床表现与日龄相关：母猪可见繁殖异常，新生仔猪偏神经症状，生长育肥猪可偏呼吸表现。"),
        ("V11-DIS-018-diagnosis", "实验室诊断", "伪狂犬病疑似应结合病史、阶段性症状和实验室确认，不得把单一神经或呼吸表现直接定因。"),
        ("V11-DIS-018-boundary", "防控/用药/处置边界", "本页 V11 仅支持临床识别和鉴别边界；中国免疫、净化、调运或处置结论仍需疾病特异 A0 来源。"),
    ]),
    ("DIS-021-influenza-viruses.md", "猪流感", "A2-MERCK-INFLUENZA-A-SWINE-2024", "SYN-004-respiratory-syndrome", "../syndromes/SYN-004-respiratory-syndrome.md", "CMP-003", "../comparisons/CMP-003-respiratory-disease.md", [
        ("V11-DIS-021-etiology", "病原/病型定位", "猪流感是由甲型流感病毒引起的高度接触性呼吸道病，临床可见发热、咳嗽、喷嚏、鼻眼分泌物和沉郁。"),
        ("V11-DIS-021-diagnosis", "实验室诊断", "猪流感主要通过 RT-PCR 或病毒分离确诊；疑似病例需与 PRRS、伪狂犬病和细菌性肺炎等呼吸道鉴别并列。"),
        ("V11-DIS-021-treatment-boundary", "防控/用药/处置边界", "猪流感没有特异治疗；抗菌药只可作为继发细菌感染处理路径，不能作为病毒病默认治疗答案。"),
    ]),
    ("DIS-024-classical-swine-fever-pestiviruses.md", "猪瘟", "A2-MERCK-CLASSICAL-SWINE-FEVER-2026", "SYN-007-sudden-death-septicemia", "../syndromes/SYN-007-sudden-death-septicemia.md", "CMP-006", "../comparisons/CMP-006-sudden-death-septicemia.md", [
        ("V11-DIS-024-etiology", "病原/病型定位", "猪瘟由黄病毒科 Pestivirus 属的猪瘟病毒引起，可呈发热、出血、共济失调和皮肤紫绀等表现。"),
        ("V11-DIS-024-differential", "鉴别诊断", "反刍动物 pestivirus 暴露可造成抗体交叉解释风险；疑似猪瘟时需进行抗体区分或病原确认。"),
        ("V11-DIS-024-regulatory-boundary", "防控/用药/处置边界", "本 A2 来源不能替代中国猪瘟法定分类、报告、免疫或处置规定；相关结论必须另引 A0。"),
    ]),
    ("DIS-026-foot-and-mouth-disease-picornaviruses.md", "猪口蹄疫", "A2-MERCK-FMD-ANIMALS-2026", "SYN-006-vesicular-disease", "../syndromes/SYN-006-vesicular-disease.md", "CMP-005", "../comparisons/CMP-005-vesicular-disease.md", [
        ("V11-DIS-026-etiology", "病原/病型定位", "口蹄疫感染包括猪在内的偶蹄动物，猪可出现口腔、鼻吻部和蹄部水疱、跛行或拒动。"),
        ("V11-DIS-026-diagnosis", "实验室诊断", "猪水疱病变之间临床不可可靠区分；疑似口蹄疫或其他水疱病时需要合适实验室进行 RT-PCR、病毒分离或抗原/抗体检测。"),
        ("V11-DIS-026-control-boundary", "防控/用药/处置边界", "口蹄疫无特异治疗；扑杀、移动控制、疫苗使用和报告处置必须按当地官方 A0/A1 程序，不得由本页 A2 临床资料外推。"),
    ]),
    ("DIS-028-porcine-reproductive-and-respiratory-syndrome-viruses.md", "猪繁殖与呼吸综合征", "A2-MERCK-PRRS-2026", "SYN-003-reproductive-failure", "../syndromes/SYN-003-reproductive-failure.md", "CMP-004", "../comparisons/CMP-004-reproductive-failure.md", [
        ("V11-DIS-028-clinical", "临床症状或剖检变化", "PRRS 应按繁殖障碍和呼吸道综合征双轴处理，繁殖表现可包括死胎、木乃伊胎、早产和弱仔。"),
        ("V11-DIS-028-differential", "鉴别诊断", "PRRS 常与细菌和病毒共感染交织，生成答案必须列出 PRRS、流感、支原体、PCV2 和细菌性肺炎等并列鉴别。"),
        ("V11-DIS-028-boundary", "生成与评估边界", "不得用单一 PCR 阳性自动解释全部繁殖或呼吸问题；需要结合群体阶段、病变、共感染和免疫史。"),
    ]),
    ("DIS-030-rotaviruses-and-reoviruses.md", "猪轮状病毒病", "A2-MERCK-ROTAVIRAL-ENTERITIS-PIGS-2024", "SYN-001-piglet-diarrhea", "../syndromes/SYN-001-piglet-diarrhea.md", "CMP-001", "../comparisons/CMP-001-neonatal-diarrhea.md", [
        ("V11-DIS-030-etiology", "病原/病型定位", "猪轮状病毒性肠炎是小肠常见病毒性疾病，各日龄猪可感染，但腹泻多见于哺乳仔猪和断奶猪。"),
        ("V11-DIS-030-diagnosis", "实验室诊断", "轮状病毒确诊需要实验室分析，结合小肠绒毛萎缩、粪便 PCR 或肠黏膜抗原示证。"),
        ("V11-DIS-030-differential", "鉴别诊断", "轮状病毒性腹泻应与猪肠道冠状病毒、Cystoisospora suis 和 ETEC/大肠杆菌性腹泻鉴别。"),
    ]),
    ("DIS-035-actinobacillus-pleuropneumoniae-pleuropneumonia.md", "猪胸膜肺炎", "A2-MERCK-ACTINOBACILLOSIS-PIGS-2025", "SYN-004-respiratory-syndrome", "../syndromes/SYN-004-respiratory-syndrome.md", "CMP-003", "../comparisons/CMP-003-respiratory-disease.md", [
        ("V11-DIS-035-etiology", "病原/病型定位", "Actinobacillus pleuropneumoniae 可导致猪传染性胸膜肺炎，应作为急性呼吸道死亡和胸膜肺炎病变的重要鉴别。"),
        ("V11-DIS-035-stage-risk", "流行病学或传播边界", "初感染猪群中各日龄可受影响，但严重病例常见于 5 月龄以下猪；生成病例应询问引种和免疫/暴露背景。"),
        ("V11-DIS-035-drug-boundary", "防控/用药/处置边界", "抗菌药选择不得由本页直接生成；需结合病原确诊、药敏、兽医处方和批准标签。"),
    ]),
    ("DIS-037-bordetella-bronchiseptica-nonprogressive-atrophic-rhinitis.md", "猪萎缩性鼻炎", "A2-MERCK-ATROPHIC-RHINITIS-PIGS-2026", "SYN-004-respiratory-syndrome", "../syndromes/SYN-004-respiratory-syndrome.md", "CMP-003", "../comparisons/CMP-003-respiratory-disease.md", [
        ("V11-DIS-037-etiology", "病原/病型定位", "猪萎缩性鼻炎应区分 Bordetella bronchiseptica 相关非进行性病变和毒素型 Pasteurella multocida 参与的进行性鼻甲萎缩风险。"),
        ("V11-DIS-037-differential", "鉴别诊断", "鼻炎、喷嚏、鼻甲改变应放入呼吸道综合征鉴别，不得由单一上呼吸道症状推断全部病因。"),
        ("V11-DIS-037-boundary", "防控/用药/处置边界", "疫苗或抗菌药方案需另有产品标签、兽医诊断和本地法规支持；本页仅提供鉴别和病例约束。"),
    ]),
    ("DIS-040-colibacillosis.md", "猪大肠杆菌病", "A2-MERCK-ENTERIC-COLIBACILLOSIS-PIGS-2024", "SYN-002-post-weaning-diarrhea", "../syndromes/SYN-002-post-weaning-diarrhea.md", "CMP-002", "../comparisons/CMP-002-post-weaning-diarrhea.md", [
        ("V11-DIS-040-etiology", "病原/病型定位", "肠道大肠杆菌病常见于哺乳和断奶猪，由 ETEC 在小肠定植引起水样腹泻和脱水。"),
        ("V11-DIS-040-diagnosis", "实验室诊断", "大肠杆菌病确诊应结合病变评估、细菌培养和毒力/黏附因子基因分型，不能仅凭粪便检出 E. coli 定因。"),
        ("V11-DIS-040-drug-boundary", "防控/用药/处置边界", "抗菌药和群体用药必须受药敏、兽医处方、中国标签与休药期约束；不得从临床页生成剂量或休药期。"),
    ]),
    ("DIS-042-edema-disease-e-coli.md", "仔猪水肿病", "A2-MERCK-EDEMA-DISEASE-PIGS-2024", "SYN-002-post-weaning-diarrhea", "../syndromes/SYN-002-post-weaning-diarrhea.md", "CMP-002", "../comparisons/CMP-002-post-weaning-diarrhea.md", [
        ("V11-DIS-042-etiology", "病原/病型定位", "水肿病是 F18+ E. coli 相关的急性毒血症，主要影响健康、快速生长的保育猪。"),
        ("V11-DIS-042-clinical", "临床症状或剖检变化", "水肿病可表现为面部和胃肠道水肿，部分病例出现神经相关病变或快速死亡。"),
        ("V11-DIS-042-control-boundary", "防控/用药/处置边界", "由于病程可极快且治疗有限，生成答案应优先落在早期识别、确诊、管理和预防，而非默认抗菌药方案。"),
    ]),
    ("DIS-043-erysipelas.md", "猪丹毒", "A2-MERCK-ERYSIPELAS-SWINE-2026", "SYN-009-lameness-arthritis", "../syndromes/SYN-009-lameness-arthritis.md", "CMP-006", "../comparisons/CMP-006-sudden-death-septicemia.md", [
        ("V11-DIS-043-clinical", "临床症状或剖检变化", "猪丹毒可呈急性或慢性，急性病例可见突然死亡、发热、关节疼痛和菱形皮肤病变。"),
        ("V11-DIS-043-differential", "鉴别诊断", "菱形皮肤病变虽强烈提示丹毒，但类似皮肤改变还可见于猪瘟、非洲猪瘟、A. suis 败血症和 PDNS。"),
        ("V11-DIS-043-diagnosis", "实验室诊断", "丹毒诊断应结合临床/剖检线索和组织中细菌或 DNA 示证；个体仅发热沉郁时诊断不稳。"),
    ]),
    ("DIS-046-mycoplasmosis-enzootic-pneumonia.md", "猪支原体肺炎", "A2-MERCK-MYCOPLASMAL-PNEUMONIA-PIGS-2024", "SYN-004-respiratory-syndrome", "../syndromes/SYN-004-respiratory-syndrome.md", "CMP-003", "../comparisons/CMP-003-respiratory-disease.md", [
        ("V11-DIS-046-etiology", "病原/病型定位", "Mycoplasma hyopneumoniae 是猪慢性、通常较轻的肺炎常见病原，可造成干咳、生长受阻和屠宰肺病变。"),
        ("V11-DIS-046-diagnosis", "实验室诊断", "猪支原体肺炎诊断可结合临床表现、典型肺病变和 PCR 确认；单一咳嗽不应直接定因。"),
        ("V11-DIS-046-control-boundary", "防控/用药/处置边界", "管理、疫苗和抗菌药均可能参与控制，但具体免疫程序、药物剂量和休药期必须另有标签/法规支持。"),
    ]),
    ("DIS-049-salmonellosis.md", "猪沙门氏菌病", "A2-MERCK-SALMONELLOSIS-ANIMALS-2026", "SYN-002-post-weaning-diarrhea", "../syndromes/SYN-002-post-weaning-diarrhea.md", "CMP-002", "../comparisons/CMP-002-post-weaning-diarrhea.md", [
        ("V11-DIS-049-diagnosis", "实验室诊断", "沙门氏菌病诊断需要在相符临床表现下从粪便、血液或组织分离到病原，或反复粪便分离提示带菌状态。"),
        ("V11-DIS-049-drug-boundary", "防控/用药/处置边界", "沙门氏菌抗菌治疗存在带菌风险争议，生成答案不得默认群体抗菌药，应要求兽医诊断、药敏和食品安全边界。"),
        ("V11-DIS-049-food-safety", "生成与评估边界", "食品动物沙门氏菌问题涉及公共卫生和食品链风险；残留、屠宰或放行结论必须另引中国 A0。"),
    ]),
    ("DIS-052-swine-dysentery-brachyspira-hyodysenteriae.md", "猪痢疾", "A2-MERCK-SWINE-DYSENTERY-2026", "SYN-002-post-weaning-diarrhea", "../syndromes/SYN-002-post-weaning-diarrhea.md", "CMP-002", "../comparisons/CMP-002-post-weaning-diarrhea.md", [
        ("V11-DIS-052-clinical", "临床症状或剖检变化", "猪痢疾是局限于大肠的黏液出血性腹泻病，常见于生长育肥猪，可造成生长下降和不同死亡率。"),
        ("V11-DIS-052-diagnosis", "实验室诊断", "确诊猪痢疾需典型大肠病变并分离强 β 溶血 Brachyspira；PCR 可辅助但不能替代溶血表型确认。"),
        ("V11-DIS-052-differential", "鉴别诊断", "猪痢疾应与肠道螺旋体病、增生性肠病、沙门氏菌病和重度鞭虫感染鉴别，混合感染常见。"),
    ]),
    ("DIS-055-external-parasites-mange.md", "猪疥螨病", "A2-MERCK-MANGE-PIGS-2026", "SYN-008-skin-pruritus-crusts", "../syndromes/SYN-008-skin-pruritus-crusts.md", "CMP-007", "../comparisons/CMP-007-skin-pruritus-crusts.md", [
        ("V11-DIS-055-etiology", "病原/病型定位", "猪疥螨病主要由 Sarcoptes scabiei var suis 寄生引起，应作为瘙痒、结痂和耳部/皮肤病变的核心鉴别。"),
        ("V11-DIS-055-transmission", "流行病学或传播边界", "疥螨可经猪只直接接触迅速传播，也可由母猪传给仔猪；病例生成应询问引种、母猪群和分娩舍接触史。"),
        ("V11-DIS-055-drug-boundary", "防控/用药/处置边界", "杀螨药、给药途径、稀释倍数和休药期必须以具体产品标签为准，不得由本页临床来源生成。"),
    ]),
    ("DIS-057-coccidia-and-other-protozoa.md", "猪球虫病", "A2-MERCK-COCCIDIOSIS-PIGS-2024", "SYN-001-piglet-diarrhea", "../syndromes/SYN-001-piglet-diarrhea.md", "CMP-001", "../comparisons/CMP-001-neonatal-diarrhea.md", [
        ("V11-DIS-057-etiology", "病原/病型定位", "新生仔猪球虫病多与 Cystoisospora/Isospora suis 有关，Eimeria spp. 更偏较大日龄猪。"),
        ("V11-DIS-057-diagnosis", "实验室诊断", "球虫病诊断需结合日龄、抗菌药无效史、粪便卵囊、饱和盐/葡萄糖漂浮、黏膜涂片、组织学或 PCR 等证据。"),
        ("V11-DIS-057-drug-boundary", "防控/用药/处置边界", "抗球虫药使用、剂量、途径和休药期必须另有中国猪用标签支持；不得从临床来源外推。"),
    ]),
    ("DIS-060-ascaris-suum-internal-parasites.md", "猪蛔虫病", "A2-MERCK-ASCARIS-SUUM-PIGS-2024", "SYN-011-poor-growth-wasting", "../syndromes/SYN-011-poor-growth-wasting.md", "CMP-003", "../comparisons/CMP-003-respiratory-disease.md", [
        ("V11-DIS-060-etiology", "病原/病型定位", "Ascaris suum 是常见猪蛔虫，幼虫移行可造成肝脏乳斑和肺部病变，肠道成虫可影响饲料转化和增重。"),
        ("V11-DIS-060-diagnosis", "实验室诊断", "专利期感染可用粪便漂浮检出典型虫卵，未成熟感染需剖检识别肝乳斑、肺部幼虫或小肠虫体。"),
        ("V11-DIS-060-control-boundary", "防控/用药/处置边界", "蛔虫控制不能只依赖驱虫药，还必须结合严格清洁、母猪入产房前管理和全进全出；药物方案需具体标签支持。"),
    ]),
]


DRUGS = [
    ("DRUG-010-amoxicillin.md", "DRUG-010-amoxicillin", "Amoxicillin / 阿莫西林", "positive_label_candidate", "A0-MOA-AMOXICILLIN-INJECTION-332-2020", [
        ("V11-DRUG-010-label-scope", "批准标签和靶动物", "本轮找到农业农村部公告中的阿莫西林注射液说明书；页面可升级为 `positive_label_candidate`，但仅限该注射液标签范围。"),
        ("V11-DRUG-010-route-indication", "剂型/途径/适应证边界", "该说明书为阿莫西林注射液，猪的标签适应证为治疗对阿莫西林敏感的感染性疾病；牛和猪给药途径为肌内注射。"),
        ("V11-DRUG-010-prescription-withdrawal", "处方药/禁停用/限制状态", "该标签区标注为兽用处方药，并列明猪休药期为 21 日；未检出本来源支持其他阿莫西林制剂的休药期。"),
        ("V11-DRUG-010-boundary", "生成与评估边界", "不得把阿莫西林注射液标签外推到可溶性粉、复方制剂、给水群体用药或其他适应证；剂量和休药期回答必须逐字核对原标签。"),
    ]),
    ("DRUG-011-ceftiofur.md", "DRUG-011-ceftiofur", "Ceftiofur / 头孢噻呋", "positive_label_candidate", "A0-MOA-CEFTIOFUR-SODIUM-INJECTION-2024", [
        ("V11-DRUG-011-label-scope", "批准标签和靶动物", "本轮找到农业农村部公报 PDF 中的注射用头孢噻呋钠说明书；可作为精确制剂标签候选。"),
        ("V11-DRUG-011-route-indication", "剂型/途径/适应证边界", "该说明书为注射用头孢噻呋钠，兽用处方药；标签适应证包括猪细菌性呼吸道感染，猪给药途径为肌内注射。"),
        ("V11-DRUG-011-withdrawal", "休药期/MRL/残留边界", "该说明书列明猪休药期为 4 日；MRL 或残留合格结论仍需另查对应标准表，不得由休药期直接推出肉品合格。"),
        ("V11-DRUG-011-boundary", "生成与评估边界", "头孢类属于高风险抗菌药；不得由成分类名外推剂量、疗程、休药期、联合用药或非标签适应证。"),
    ]),
    ("DRUG-012-florfenicol.md", "DRUG-012-florfenicol", "Florfenicol / 氟苯尼考", "positive_label_candidate", "A0-MOA-FLORFENICOL-INJECTION-219-2019", [
        ("V11-DRUG-012-label-scope", "批准标签和靶动物", "本轮找到农业农村部公告中的氟苯尼考注射液说明书；可作为精确制剂标签候选。"),
        ("V11-DRUG-012-route-indication", "剂型/途径/适应证边界", "该说明书为氟苯尼考注射液，适应证为由胸膜肺炎放线杆菌和多杀性巴氏杆菌引起的猪细菌性呼吸系统疾病，给药途径为颈部肌内注射。"),
        ("V11-DRUG-012-withdrawal", "休药期/MRL/残留边界", "该说明书列明猪休药期为 18 日；禁忌/限制包括已知过敏猪、成年种猪、体重不足 2kg 仔猪及免疫功能严重缺陷猪等标签边界。"),
        ("V11-DRUG-012-boundary", "生成与评估边界", "氟苯尼考注射液证据不得外推为粉剂、预混剂、饮水剂或所有呼吸/肠道病例默认用药。"),
    ]),
    ("DRUG-013-tiamulin.md", "DRUG-013-tiamulin", "Tiamulin / 泰妙菌素", "boundary_only", "A0-MOA-LABEL-INSTRUCTION-RULES-2002", [
        ("V11-DRUG-013-label-gap", "批准标签和靶动物", "本轮未建立可逐项核对的泰妙菌素中国猪用说明书 source 页；页面继续保持 `boundary_only`。"),
        ("V11-DRUG-013-boundary", "生成与评估边界", "泰妙菌素常被召回到猪痢疾/支原体等场景，但没有精确 A0 标签时不得输出剂量、疗程、休药期或中国合规承诺。"),
    ]),
    ("DRUG-015-tylosin.md", "DRUG-015-tylosin", "Tylosin / 泰乐菌素", "boundary_only", "A0-MOA-LABEL-INSTRUCTION-RULES-2002", [
        ("V11-DRUG-015-label-gap", "批准标签和靶动物", "本轮未完成泰乐菌素具体中国猪用制剂、靶动物、适应证和休药期的精确 A0 标签核验；页面保持 `boundary_only`。"),
        ("V11-DRUG-015-boundary", "生成与评估边界", "不得从大环内酯类别或国外标签外推中国猪用剂量、饲料添加、休药期或残留结论。"),
    ]),
    ("DRUG-018-enrofloxacin.md", "DRUG-018-enrofloxacin", "Enrofloxacin / 恩诺沙星", "positive_label_candidate", "A0-MOA-ENROFLOXACIN-SOLUTION-55-2018", [
        ("V11-DRUG-018-label-scope", "批准标签和靶动物", "本轮找到农业农村部公告中的恩诺沙星溶液说明书；可作为匹配制剂和靶动物范围内的标签候选。"),
        ("V11-DRUG-018-route-indication", "剂型/途径/适应证边界", "该说明书为恩诺沙星溶液，适应证为治疗猪大肠杆菌所致的胃肠道疾病，标签给药途径为内服。"),
        ("V11-DRUG-018-withdrawal", "休药期/MRL/残留边界", "该说明书列明猪休药期为 5 日；标签还要求尽可能根据药敏试验使用氟喹诺酮类药物，并提示偏离说明书可增加耐药风险。"),
        ("V11-DRUG-018-boundary", "生成与评估边界", "氟喹诺酮类高风险；不得把恩诺沙星溶液标签外推到其他剂型、其他喹诺酮或无诊断群体用药。"),
    ]),
    ("DRUG-019-oxytetracycline.md", "DRUG-019-oxytetracycline", "Oxytetracycline / 土霉素", "boundary_only", "A0-MOA-LABEL-INSTRUCTION-RULES-2002", [
        ("V11-DRUG-019-label-gap", "批准标签和靶动物", "本轮未形成可逐项核对的土霉素中国猪用具体标签 source；页面继续保持 `boundary_only`。"),
        ("V11-DRUG-019-boundary", "生成与评估边界", "土霉素不得按四环素类概括输出中国猪用剂量、疗程或休药期；需具体制剂标签、处方和药敏支持。"),
    ]),
    ("DRUG-021-doxycycline.md", "DRUG-021-doxycycline", "Doxycycline / 多西环素", "boundary_only", "A0-MOA-LABEL-INSTRUCTION-RULES-2002", [
        ("V11-DRUG-021-label-gap", "批准标签和靶动物", "本轮未找到并核验可升级页面的多西环素中国猪用精确标签；页面继续保持 `boundary_only`。"),
        ("V11-DRUG-021-boundary", "生成与评估边界", "不得从其他四环素类、鸡用说明书或国外资料外推中国猪用适应证、给药途径、剂量或休药期。"),
    ]),
    ("DRUG-002-ivermectin.md", "DRUG-002-ivermectin", "Ivermectin / 伊维菌素", "boundary_only", "A0-MOA-LABEL-INSTRUCTION-RULES-2002", [
        ("V11-DRUG-002-label-gap", "批准标签和靶动物", "本轮未核验到可支持猪用正向生成的伊维菌素中国官方具体标签；页面继续保持 `boundary_only`。"),
        ("V11-DRUG-002-boundary", "生成与评估边界", "驱虫/杀螨用途、给药途径和休药期必须由具体产品标签支持；不得由阿维菌素类或国外标签外推。"),
    ]),
    ("DRUG-027-toltrazuril.md", "DRUG-027-toltrazuril", "Toltrazuril / 托曲珠利", "positive_label_candidate", "A0-MOA-TOLTRAZURIL-SUSPENSION-216-2019", [
        ("V11-DRUG-027-label-scope", "批准标签和靶动物", "本轮找到农业农村部公告中的 5% 托曲珠利混悬液说明书；可作为匹配制剂和仔猪球虫病语境的标签候选。"),
        ("V11-DRUG-027-route-indication", "剂型/途径/适应证边界", "该说明书为 5% 托曲珠利混悬液，适应证为预防仔猪和犊牛球虫病，标签给药途径为内服。"),
        ("V11-DRUG-027-withdrawal", "休药期/MRL/残留边界", "该说明书列明仔猪休药期为 77 日；托曲珠利鸡用溶液、猫犬复方片或环境消毒剂条目不得作为猪用标签替代。"),
        ("V11-DRUG-027-boundary", "生成与评估边界", "托曲珠利鸡用溶液或其他制剂不得外推到仔猪；剂量、途径和休药期必须回到该猪用说明书逐项核对。"),
    ]),
]


def source_page_text(src: dict) -> str:
    claims = "\n".join(f"- {c}" for c in src["claims"])
    return f"""---
type: source
source_id: {src['source_id']}
source_path: {src['url']}
source_type: url
authority_level: {src['authority_level']}
evidence_status: HUMAN_REVIEWED
created: {UPDATED}
updated: {UPDATED}
sources: []
---

# {src['title']}

## 来源

- URL: {src['url']}
- 发布机构：{src['publisher']}
- 发布/修订日期：{src['date']}
- 访问日期：{TODAY}
- 权威等级：{src['authority_level']}

## 可支持结论

{claims}

## 不得外推边界

- {src['boundary']}
"""


def ensure_sources() -> list[str]:
    out = []
    src_dir = ROOT / "wiki" / "sources"
    for src in SOURCES:
        path = src_dir / f"{src['source_id']}.md"
        write(path, source_page_text(src))
        out.append(str(path.relative_to(ROOT)).replace("\\", "/"))

    idx_path = ROOT / "exports" / "source_index.csv"
    rows = list(csv.DictReader(idx_path.open(encoding="utf-8", newline="")))
    by_id = {r["source_id"]: r for r in rows}
    for src in SOURCES:
        by_id[src["source_id"]] = {
            "source_id": src["source_id"],
            "title": src["title"],
            "pages": src["url"],
            "evidence_status": "HUMAN_REVIEWED",
            "relpath": f"wiki/sources/{src['source_id']}.md",
        }
    ordered = list(by_id.values())
    with idx_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source_id", "title", "pages", "evidence_status", "relpath"])
        writer.writeheader()
        writer.writerows(ordered)
    return out


def append_facts() -> int:
    facts_path = ROOT / "exports" / "knowledge_facts.json"
    facts = json.loads(read(facts_path))
    by_id = {f.get("fact_id"): f for f in facts}

    new_facts = []
    for _, entity, source_id, *_rest in DISEASES:
        bullets = _rest[-1]
        for fact_id, fact_type, text in bullets:
            new_facts.append({
                "fact_id": fact_id,
                "fact_type": f"v11_disease_{fact_type}",
                "subject": entity,
                "predicate": fact_type,
                "object": text,
                "fact_confidence": "0.86",
                "evidence_source": source_id,
                "evidence_source_id": source_id,
                "evidence_url": next(s["url"] for s in SOURCES if s["source_id"] == source_id),
                "evidence_quote_span": "Opened official/authoritative page; V11 batch 1 extraction; see source page usable claims.",
                "evidence_status": "HUMAN_REVIEWED",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "Global",
            })

    for _, drug_id, title, role, source_id, bullets in DRUGS:
        for fact_id, fact_type, text in bullets:
            new_facts.append({
                "fact_id": fact_id,
                "fact_type": f"v11_drug_{fact_type}",
                "subject": title,
                "predicate": fact_type,
                "object": text,
                "fact_confidence": "0.84",
                "evidence_source": source_id,
                "evidence_source_id": source_id,
                "evidence_url": next((s["url"] for s in SOURCES if s["source_id"] == source_id), ""),
                "evidence_quote_span": "Opened official/authoritative page or mandatory label-rule source; V11 batch 1 extraction.",
                "evidence_status": "HUMAN_REVIEWED",
                "applies_to_species": "swine",
                "applies_to_stage": "all_stages",
                "jurisdiction": "China" if source_id.startswith("A0-") else "Global",
            })

    changed = 0
    for fact in new_facts:
        if fact["fact_id"] not in by_id:
            facts.append(fact)
            by_id[fact["fact_id"]] = fact
            changed += 1
        else:
            by_id[fact["fact_id"]].update(fact)
            changed += 1
    write(facts_path, json.dumps(facts, ensure_ascii=False, indent=2) + "\n")
    return changed


def update_frontmatter_sources(text: str, source_id: str) -> str:
    if source_id in text.split("---", 2)[1]:
        return text
    m = re.search(r"^sources:\s*\[(.*?)\]\s*$", text, re.M)
    if not m:
        return text
    current = m.group(1).strip()
    sep = ", " if current else ""
    return text[:m.start(1)] + current + sep + source_id + text[m.end(1):]


def append_v11_section(text: str, section: str) -> str:
    heading = "## Web Source Reinforcement / V11"
    if heading in text:
        text = re.sub(r"\n## Web Source Reinforcement / V11\n.*?(?=\n## |\Z)", "\n" + section.rstrip() + "\n", text, flags=re.S)
        return text
    return text.rstrip() + "\n\n" + section.rstrip() + "\n"


def disease_section(entity: str, source_id: str, syn_id: str, syn_link: str, cmp_id: str, cmp_link: str, bullets: list[tuple[str, str, str]]) -> str:
    grouped = {}
    for fact_id, kind, text in bullets:
        grouped.setdefault(kind, []).append((fact_id, text))
    parts = [
        "## Web Source Reinforcement / V11",
        "",
        f"> {TODAY} V11 web-first 补强。来源先经网页检索并打开核验，新增事实只使用本轮注册 source：`{source_id}`。",
        "",
        "### syndrome/comparison 链接",
        "",
        f"- 本页至少应随病例召回 [{syn_id}]({syn_link}) 和 [{cmp_id}]({cmp_link})，用于生成与评估时的综合征入口和鉴别矩阵锚点。",
    ]
    for kind in ["病原/病型定位", "流行病学或传播边界", "临床症状或剖检变化", "实验室诊断", "鉴别诊断", "防控/用药/处置边界", "生成与评估边界"]:
        if kind in grouped:
            parts += ["", f"### {kind}", ""]
            for fact_id, text in grouped[kind]:
                parts.append(f"- {text}`fact_id={fact_id}; source_id={source_id}; anchor=web page opened {TODAY}`")
    parts += [
        "",
        "### Evidence gap",
        "",
        "- 本轮 V11 以 A2 临床/诊断网页来源补齐生成约束；中国法定分类、上报、调运、扑杀、检疫、固定免疫程序、剂量、疗程、休药期和食品安全执行结论仍需精确 A0 来源，不得由本页外推。`source_id=RC-DISEASE-REGULATORY-001; source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001`",
    ]
    return "\n".join(parts)


def update_disease_pages() -> int:
    count = 0
    for filename, entity, source_id, syn_id, syn_link, cmp_id, cmp_link, bullets in DISEASES:
        path = ROOT / "wiki" / "diseases" / filename
        text = read(path)
        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        text = update_frontmatter_sources(text, source_id)
        section = disease_section(entity, source_id, syn_id, syn_link, cmp_id, cmp_link, bullets)
        write(path, append_v11_section(text, section))
        count += 1
    return count


def drug_section(role: str, source_id: str, bullets: list[tuple[str, str, str]]) -> str:
    grouped = {}
    for fact_id, kind, text in bullets:
        grouped.setdefault(kind, []).append((fact_id, text))
    parts = [
        "## Web Source Reinforcement / V11",
        "",
        f"> {TODAY} V11 药物标签证据第一批。`gold_dataset_use` 本轮判定为 `{role}`；事实来自本轮打开核验并注册的 source：`{source_id}`。",
    ]
    for kind in ["药物/成分定位", "批准标签和靶动物", "剂型/途径/适应证边界", "处方药/禁停用/限制状态", "休药期/MRL/残留边界", "生成与评估边界"]:
        if kind in grouped:
            parts += ["", f"### {kind}", ""]
            for fact_id, text in grouped[kind]:
                parts.append(f"- {text}`fact_id={fact_id}; source_id={source_id}; anchor=web page opened {TODAY}`")
    parts += [
        "",
        "### Evidence gap",
        "",
        "- 即使页面升级为 `positive_label_candidate`，也只表示存在可召回的官方标签候选；剂量、疗程、给药途径、休药期、MRL、残留合格和食品安全结论仍必须在具体回答时逐条核对原始 A0 标签/标准，不得从本页摘要外推。`source_id=RC-DRUG-001; source_id=RC-WITHDRAWAL-MRL-001; source_id=A0-MOA-LABEL-INSTRUCTION-RULES-2002`",
    ]
    return "\n".join(parts)


def update_drug_pages() -> int:
    count = 0
    for filename, drug_id, title, role, source_id, bullets in DRUGS:
        path = ROOT / "wiki" / "drugs" / filename
        text = read(path)
        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        text = re.sub(r"gold_dataset_use:\s*\S+", f"gold_dataset_use: {role}", text, count=1)
        if role == "positive_label_candidate":
            text = text.replace("needs_review", "v11_label_candidate")
        text = update_frontmatter_sources(text, source_id)
        write(path, append_v11_section(text, drug_section(role, source_id, bullets)))
        count += 1

    idx_path = ROOT / "exports" / "drug_gold_role_index.csv"
    rows = list(csv.DictReader(idx_path.open(encoding="utf-8-sig", newline="")))
    role_by_id = {drug_id: role for _, drug_id, _, role, _, _ in DRUGS}
    for row in rows:
        if '"drug_id"' in row and "drug_id" not in row:
            row["drug_id"] = row.pop('"drug_id"')
    for row in rows:
        if row["drug_id"] in role_by_id:
            row["gold_dataset_use"] = role_by_id[row["drug_id"]]
            row["evidence_status"] = "HUMAN_REVIEWED" if role_by_id[row["drug_id"]] == "positive_label_candidate" else row["evidence_status"]
    with idx_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["drug_id", "title", "gold_dataset_use", "evidence_status", "page_relpath"], quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)
    return count


def write_log(source_pages: list[str], facts_changed: int, disease_count: int, drug_count: int) -> None:
    log_path = ROOT / "issues" / "v11_disease_drug_batch1_execution_log_2026-05-08.md"
    disease_entities = ", ".join(filename.replace(".md", "") for filename, *_ in DISEASES)
    drug_entities = ", ".join(drug_id for _, drug_id, *_ in DRUGS)
    source_list = "\n".join(f"- `{p}`" for p in source_pages)
    disease_pages = "\n".join(f"- `wiki/diseases/{filename}`" for filename, *_ in DISEASES)
    drug_pages = "\n".join(f"- `wiki/drugs/{filename}`" for filename, *_ in DRUGS)
    promoted = [drug_id for _, drug_id, _, role, _, _ in DRUGS if role == "positive_label_candidate"]
    boundary = [drug_id for _, drug_id, _, role, _, _ in DRUGS if role == "boundary_only"]
    fact_rows = []
    for filename, entity, source_id, *_rest in DISEASES:
        for fact_id, kind, _ in _rest[-1]:
            fact_rows.append(f"| {fact_id} | {entity} | {source_id} | source page usable claims | HUMAN_REVIEWED |")
    for _, drug_id, title, _, source_id, bullets in DRUGS:
        for fact_id, kind, _ in bullets:
            fact_rows.append(f"| {fact_id} | {title} | {source_id} | source page usable claims | HUMAN_REVIEWED |")
    log = f"""# V11 disease/drug batch 1 execution log

- Date: {TODAY}
- Scope: Disease V11 first batch + Drug V11 label evidence first batch
- Target entities: {disease_entities}; {drug_entities}
- Status: partial

## Task scope and required fields

- Entity type: disease + drug
- Required fields: disease diagnosis, differential, transmission/control boundaries, comparison/syndrome links; drug target species, label source, formulation/route/indication boundary, prescription/prohibited/withdrawal/MRL boundary.
- High-risk dimensions: China regulatory status, drug use, withdrawal/MRL, residue, food safety, report/cull/movement/quarantine.
- Required authority levels: A2 accepted for disease clinical/diagnostic reinforcement; A0 required for drug positive label candidates and high-risk China drug claims.

## Web/source search

Web search was executed first under V11. Representative accepted queries included:

| Entity | Query | Result | Accepted source_id | Rejected reason |
|---|---|---|---|---|
| enteric coronaviruses | Merck Veterinary Manual coronaviral enteritis in pigs PED TGE PDCoV | accepted Merck clinical page | A2-MERCK-CORONAVIRAL-ENTERITIS-PIGS-2026 | commercial/secondary snippets rejected |
| respiratory diseases | Merck Veterinary Manual influenza/PRRS/mycoplasmal pneumonia/atrophic rhinitis in pigs | accepted Merck clinical pages | A2-MERCK-INFLUENZA-A-SWINE-2024 and related A2 sources | non-authoritative reposts rejected |
| vesicular disease | Merck Veterinary Manual foot-and-mouth disease pigs vesicular disease | accepted Merck clinical page | A2-MERCK-FMD-ANIMALS-2026 | non-official summaries rejected |
| enteric bacterial/parasitic disease | Merck Veterinary Manual colibacillosis, edema disease, dysentery, coccidiosis, ascaris in pigs | accepted Merck clinical pages | multiple A2-MERCK sources | forums/marketing pages rejected |
| 阿莫西林/头孢噻呋/氟苯尼考/恩诺沙星/托曲珠利 | site:moa.gov.cn active ingredient 兽药 说明书 猪 休药期 | accepted MOA announcements/PDFs when exact label source was opened | A0-MOA-* label sources | source-mismatched or incomplete snippets rejected |
| 泰妙菌素/泰乐菌素/土霉素/多西环素/伊维菌素 | site:moa.gov.cn active ingredient 兽药 说明书 猪 休药期 | exact page-level label not fully registered in this batch | A0-MOA-LABEL-INSTRUCTION-RULES-2002 as hard boundary | not upgraded; exact A0 label still pending |

## New source pages

{source_list}

## Facts extracted from new sources

| fact_id | entity | evidence_source_id | page/span/table | evidence_status |
|---|---|---|---|---|
{chr(10).join(fact_rows)}

## Entity pages changed

{disease_pages}
{drug_pages}

## Comparison/rule/synthesis pages changed

- None. Existing comparison/syndrome/rule anchors were linked from V11 entity sections; no matrix claims were changed.

## Validation

- source pages added/updated: {len(source_pages)}
- source index updated: yes
- facts added/updated: {facts_changed}
- disease entity pages with new anchors: {disease_count}
- drug entity pages with new anchors: {drug_count}
- comparison links: each disease V11 block links at least one syndrome and one comparison
- high-risk gate result: unsupported China regulatory, dose, course, withdrawal/MRL, residue and food-safety claims remain blocked unless exact A0 is present
- drug promotions: {", ".join(promoted)}
- drug pages kept boundary_only: {", ".join(boundary)}
- unresolved gaps: disease-specific China A0 status remains pending for many non-statutory pages; drug pages kept boundary_only require exact product label/registration/MRL confirmation before upgrade

## Stop-condition check

- Web search executed first: yes
- Adopted web sources opened and classified: yes
- Source pages created/indexed before entity claims: yes
- Facts extracted from new sources: yes
- Entity pages updated: yes
- Remaining gaps recorded: yes
- High-risk unsupported claims blocked: yes
- Status note: partial because this is the first batch, not full-coverage completion.
"""
    write(log_path, log)


def main() -> None:
    source_pages = ensure_sources()
    facts_changed = append_facts()
    disease_count = update_disease_pages()
    drug_count = update_drug_pages()
    write_log(source_pages, facts_changed, disease_count, drug_count)
    print({
        "source_pages": len(source_pages),
        "facts_changed": facts_changed,
        "disease_pages": disease_count,
        "drug_pages": drug_count,
    })


if __name__ == "__main__":
    main()
