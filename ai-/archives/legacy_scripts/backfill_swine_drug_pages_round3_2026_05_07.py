from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
NOW = "2026-05-08T00:08:00+08:00"


DRUGS = [
    {
        "id": "DRUG-071-streptomycin",
        "title": "Streptomycin / 链霉素",
        "klass": "aminoglycoside",
        "pages": "PDF page 884; also resistance/boundary mentions in staphylococcosis contexts",
        "use": "Leptospirosis traditional treatment candidate; PDF notes clinical outbreak treatment for affected and at-risk pigs.",
        "boundary": "US veterinary availability and food-animal residue/legal status require strict review; in China must be checked against approved labels and prohibited/residue rules.",
        "sources": ["SRC-0067", "SRC-0068", "A0-MOA-BANNED-DRUG-250-NOTICE", "A0-MOA-MRL-GB31650-2019-RAW"],
    },
    {
        "id": "DRUG-072-tildipirosin",
        "title": "Tildipirosin / 替地匹罗星",
        "klass": "macrolide",
        "pages": "PDF page 812",
        "use": "Leptospirosis small-sample experimental context with oxytetracycline + tildipirosin; not a herd eradication strategy.",
        "boundary": "Evidence is narrow and not a general prescription basis; verify product label, species, indication and withdrawal period.",
        "sources": ["SRC-0060", "SRC-0061", "A0-MOA-BANNED-DRUG-250-NOTICE"],
    },
    {
        "id": "DRUG-073-erythromycin",
        "title": "Erythromycin / 红霉素",
        "klass": "macrolide",
        "pages": "PDF page 884-885; staphylococcosis resistance boundary mentions",
        "use": "Leptospirosis alternative/control candidate context; resistance boundary in Staphylococcus hyicus contexts.",
        "boundary": "Older macrolide candidate; legality, label and resistance must be reviewed before any use conclusion.",
        "sources": ["SRC-0067", "SRC-0068", "SRC-0074", "A0-MOA-BANNED-DRUG-250-NOTICE"],
    },
    {
        "id": "DRUG-074-amikacin",
        "title": "Amikacin / 阿米卡星",
        "klass": "aminoglycoside",
        "pages": "PDF page 946",
        "use": "Salmonellosis candidate/reserve antimicrobial context.",
        "boundary": "High-importance aminoglycoside/reserve context; must be treated as high-review and not routine herd medication.",
        "sources": ["SRC-0073", "A1-WOAH-SWINE-AMR-TRD-2025", "A0-MOA-BANNED-DRUG-250-NOTICE"],
    },
    {
        "id": "DRUG-075-praziquantel",
        "title": "Praziquantel / 吡喹酮",
        "klass": "anthelmintic / cestocide",
        "pages": "PDF page 1062",
        "use": "Taenia solium public-health lifecycle context; treatment of human definitive hosts, not routine treatment of infected pigs.",
        "boundary": "Do not infer pig treatment from human definitive-host treatment; use as zoonotic/public-health boundary.",
        "sources": ["SRC-0082", "A1-WOAH-PORCINE-CYSTICERCOSIS"],
    },
    {
        "id": "DRUG-076-dichlorvos",
        "title": "Dichlorvos / 敌敌畏",
        "klass": "organophosphate anthelmintic/insecticide",
        "pages": "PDF page 1064",
        "use": "Internal parasite treatment table context for Ascaris/Oesophagostomum/Trichuris/Strongyloides-related coverage.",
        "boundary": "Organophosphate high-toxicity and residue/legal-risk candidate; must verify prohibited/eliminated status and label before any use conclusion.",
        "sources": ["SRC-0082", "A0-MOA-ELIMINATED-DRUGS-839", "A0-MOA-BANNED-DRUG-250-NOTICE"],
    },
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


def drug_page(drug: dict[str, object]) -> str:
    sources = ", ".join(drug["sources"])
    high = drug["id"] in {"DRUG-071-streptomycin", "DRUG-074-amikacin", "DRUG-076-dichlorvos"}
    tag = "high_review" if high else "needs_review"
    return f"""---
tags: [drug, swine, v7, evidence_only, {tag}]
drug_id: {drug["id"]}
updated: {NOW}
evidence_status: NEEDS_REVIEW
jurisdiction: Global
sources: [{sources}]
candidate_source: subagent_pdf_deep_scan_2026-05-07
---

# {drug["title"]}

## 证据状态

- 页面类型：`evidence_only` + `NEEDS_REVIEW`。
- 本页来自 Diseases of Swine 11e PDF 深度解析，用于补齐治疗候选矩阵中缺少的单列药物。
- 本页不是处方页；未完成标签、禁限用、药敏和休药期复核前，不得生成剂量、疗程或中国合规承诺。

## 药物类别

- {drug["klass"]}

## 教材候选证据

- 候选页码：{drug["pages"]}。
- PDF 语境：{drug["use"]}

## 合规和安全边界

- {drug["boundary"]}
- 命中高风险/人医关键药/有机磷/人用公共卫生语境时，必须优先做禁用、停用、淘汰、残留、标签和兽医处方复核。

## V7 生成可用边界

- 可用于题型：候选召回、疾病-药物关系复核、禁限用风险识别、要求用户提供标签/公告/药敏证据。
- 不可用于题型：剂量、疗程、给药途径、群体投药、休药期、残留合格承诺或“可用于中国猪场”的直接结论。
"""


def main() -> None:
    for drug in DRUGS:
        write_text(WIKI / "wiki" / "drugs" / f"{drug['id']}.md", drug_page(drug))

    index_path = WIKI / "exports" / "drug_page_index.csv"
    rows = read_csv(index_path)
    header = rows[0]
    by_id = {row[0]: row for row in rows[1:] if row}
    for drug in DRUGS:
        status = "high_review_needs_review" if drug["id"] in {"DRUG-071-streptomycin", "DRUG-074-amikacin", "DRUG-076-dichlorvos"} else "evidence_only_needs_review"
        by_id[drug["id"]] = [drug["id"], drug["title"], status, f"wiki/drugs/{drug['id']}.md"]
    write_csv(index_path, [header] + sorted(by_id.values(), key=lambda row: row[0]))

    report = WIKI / "issues" / "drug_candidate_ingest_assessment_round3_2026-05-07.md"
    write_text(
        report,
        f"""# Drug Candidate Ingest Assessment Round 3 - 2026-05-07

## 本次处理

- 根据 PDF 深度解析子任务，新增 `DRUG-071` 到 `DRUG-076`，共 {len(DRUGS)} 个单列药物页面。
- 新增药物：streptomycin、tildipirosin、erythromycin、amikacin、praziquantel、dichlorvos。
- 更新 `exports/drug_page_index.csv`。

## 入库边界

- 全部为 `NEEDS_REVIEW`。
- `streptomycin`、`amikacin`、`dichlorvos` 标记为高复核。
- `praziquantel` 仅作为 Taenia solium 公共卫生生命周期边界，不从人终宿主治疗外推为猪治疗。
- 未写入 `exports/knowledge_facts.json`。
""",
    )

    summary = WIKI / "issues" / "swine_wiki_authority_pdf_enrichment_summary_2026-05-07.md"
    write_text(
        summary,
        """# Swine Wiki Authority + PDF Enrichment Summary - 2026-05-07

## 已完成

- 下载/缓存 17 个权威网页或 PDF 来源到 `raw/urls` 与 `raw/pdfs`，并建立 source pages。
- 生成权威来源 manifest：`issues/authority_web_fetch_manifest_2026-05-07.json`。
- 生成 PDF 疾病-药物候选矩阵：`issues/swine_pdf_treatment_candidate_matrix_2026-05-07.csv`，共 178 行。
- 新增 derived synthesis：`wiki/synthesis/swine_treatment_candidate_matrix_v7.md`。
- 本轮新增 6 个药物页，使 drug 页面总数达到 76。

## 重要质量边界

- MOA/中国政府来源用于中国禁用、停用、标签、残留、休药期和说明书规则边界。
- Merck/EMA/FDA/WOAH/FAO 可用于治疗候选、产品证据、AMR 审慎或国际对照，但不能替代中国禁用/合规判断。
- 本轮未把候选写入正式 `knowledge_facts.json`。

## 后续建议

- 对 Merck 403 页面用浏览器/人工保存或官方可下载版本补原文快照。
- 对 FDA Green Book 使用 `animaldrugsatfda.fda.gov` 的查询/API 或人工导出补充产品级标签。
- 将 PDF 候选矩阵按疾病页批量回填为 `NEEDS_REVIEW` 候选小节，人工复核后再升级事实。
""",
    )

    log_path = WIKI / "log.md"
    log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Wiki Log\n"
    marker = "2026-05-07 drug-backfill-round3"
    if marker not in log_text:
        log_path.write_text(
            log_text.rstrip()
            + "\n\n"
            + f"{marker} | added {len(DRUGS)} additional PDF deep-scan drug pages; updated drug index; facts unchanged.\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"added_or_updated={len(DRUGS)}")


if __name__ == "__main__":
    main()
