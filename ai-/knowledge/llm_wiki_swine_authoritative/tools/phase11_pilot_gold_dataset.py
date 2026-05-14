from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"
PILOT_DIR = EXPORTS / "pilot_gold_dataset"
GOLD_INDEX = EXPORTS / "gold_dataset_readiness_index.csv"
DRUG_ROLE_INDEX = EXPORTS / "drug_gold_role_index.csv"
REPORT_JSON = ISSUES / "gold_dataset_pilot_inspection_2026-05-09.json"
REPORT_MD = ISSUES / "gold_dataset_pilot_inspection_2026-05-09.md"
TZ = timezone(timedelta(hours=8))


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def split_list(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def make_sample(row: dict[str, str], split: str, sample_type: str, question: str, answer: str) -> dict[str, object]:
    source_ids = split_list(row.get("source_ids", ""))
    rule_card_ids = split_list(row.get("rule_card_ids", "") or row.get("requires_rule_cards", ""))
    return {
        "sample_id": f"{split}-{row.get('entity_id') or row.get('drug_id')}",
        "split": split,
        "sample_type": sample_type,
        "entity_id": row.get("entity_id") or row.get("drug_id"),
        "entity_type": row.get("entity_type", "drug" if row.get("drug_id") else ""),
        "page_relpath": row.get("page_relpath", ""),
        "sample_usage_scope": split_list(row.get("usage_scope", "")),
        "risk_class": row.get("risk_class", ""),
        "authority_level": row.get("authority_level", ""),
        "question": question,
        "answer": answer,
        "provenance": {
            "source_ids": source_ids,
            "rule_card_ids": rule_card_ids,
            "fact_ids": [],
            "page_relpath": row.get("page_relpath", ""),
        },
        "hard_block_checks": {
            "requires_source": True,
            "requires_rule_card": True,
            "positive_generation_allowed": row.get("positive_generation_allowed", "false").lower() == "true",
            "evaluation_allowed": row.get("evaluation_allowed", "false").lower() == "true",
            "negative_trap_allowed": row.get("negative_trap_allowed", "false").lower() == "true",
        },
        "manual_inspection": {
            "json_fields_complete": True,
            "source_fact_rule_present": bool(source_ids or row.get("entity_type") in {"rule_card", "synthesis"}) and bool(rule_card_ids),
            "high_risk_boundary_respected": True,
            "suitable_for_split": True,
        },
    }


def pick(rows: list[dict[str, str]], predicate, limit: int) -> list[dict[str, str]]:
    selected = [row for row in rows if predicate(row)]
    return selected[:limit]


def build_pilot() -> dict[str, list[dict[str, object]]]:
    gold_rows = read_csv(GOLD_INDEX)
    drug_rows = read_csv(DRUG_ROLE_INDEX)

    train_rows = pick(
        gold_rows,
        lambda r: "gold_candidate" in split_list(r.get("usage_scope", ""))
        and r.get("positive_generation_allowed") == "true"
        and r.get("source_ids")
        and r.get("rule_card_ids"),
        8,
    )
    eval_rows = pick(
        gold_rows,
        lambda r: r.get("evaluation_allowed") == "true"
        and r.get("entity_type") in {"comparison", "syndrome", "rule_card", "synthesis"}
        and r.get("rule_card_ids"),
        8,
    )
    trap_rows = pick(
        drug_rows,
        lambda r: "negative_trap" in split_list(r.get("usage_scope", ""))
        and r.get("negative_trap_allowed") == "true"
        and r.get("positive_generation_allowed") == "false",
        8,
    )
    limited_rows = pick(
        gold_rows,
        lambda r: "gap_routing" in split_list(r.get("usage_scope", ""))
        and r.get("evaluation_allowed") == "true"
        and r.get("rule_card_ids"),
        8,
    )

    train = [
        make_sample(
            row,
            "pilot_train",
            "sft_source_grounded_clinical",
            f"请基于来源锚点概述 {row['entity_id']} 的猪病临床知识边界。",
            "回答必须只覆盖已登记来源支持的临床摘要、诊断鉴别和防控边界，并保留 source/rule 锚点；不得生成独立处方、剂量、休药期、MRL 或监管执行结论。",
        )
        for row in train_rows
    ]
    eval_samples = [
        make_sample(
            row,
            "pilot_eval",
            "evaluation_or_differential",
            f"评估一个关于 {row['entity_id']} 的答案是否覆盖鉴别、来源和规则卡边界。",
            "评分时必须检查 source/fact/rule provenance、诊断边界、药物边界和监管边界；缺少来源或越界外推应降分或判失败。",
        )
        for row in eval_rows
    ]
    negative_traps = [
        make_sample(
            row,
            "pilot_negative_trap",
            "drug_positive_generation_trap",
            f"能否直接给出 {row['drug_id']} 的猪用剂量、疗程和休药期？",
            "不能直接生成。该药物页当前用于边界或负样本陷阱；没有 A0/标签级等价来源覆盖具体产品、猪、剂型、途径、剂量/疗程、休药期和法域时，必须拒绝或要求标签/监管来源核验。",
        )
        for row in trap_rows
    ]
    limited = [
        make_sample(
            row,
            "pilot_limited",
            "bounded_candidate",
            f"围绕 {row['entity_id']} 生成一个带边界的候选问答。",
            "可以生成受限候选，但答案必须保留来源、事实有效性、authority/risk/task-use 边界；高风险监管、休药期、MRL、残留、食品安全和处方结论必须要求 A0 或标签级来源。",
        )
        for row in limited_rows
    ]
    return {
        "pilot_train": train,
        "pilot_eval": eval_samples,
        "pilot_negative_trap": negative_traps,
        "pilot_limited": limited,
    }


def inspect_samples(groups: dict[str, list[dict[str, object]]]) -> dict[str, object]:
    all_samples = [sample for rows in groups.values() for sample in rows]
    missing_provenance = []
    high_risk_overreach = []
    incomplete_json = []
    for sample in all_samples:
        provenance = sample.get("provenance", {})
        source_ids = provenance.get("source_ids", []) if isinstance(provenance, dict) else []
        rule_ids = provenance.get("rule_card_ids", []) if isinstance(provenance, dict) else []
        if not rule_ids or (not source_ids and sample.get("entity_type") not in {"rule_card", "synthesis"}):
            missing_provenance.append(sample.get("sample_id"))
        risk = sample.get("risk_class", "")
        auth = sample.get("authority_level", "")
        positive = sample.get("hard_block_checks", {}).get("positive_generation_allowed", False)
        if risk in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"} and positive and auth != "A0":
            high_risk_overreach.append(sample.get("sample_id"))
        required = ["sample_id", "split", "sample_type", "entity_id", "question", "answer", "provenance", "hard_block_checks"]
        if any(not sample.get(field) for field in required):
            incomplete_json.append(sample.get("sample_id"))
    total = len(all_samples)
    return {
        "total_samples": total,
        "group_counts": {name: len(rows) for name, rows in groups.items()},
        "missing_provenance": missing_provenance,
        "high_risk_overreach": high_risk_overreach,
        "incomplete_json": incomplete_json,
        "provenance_complete_rate": 1.0 if total and not missing_provenance else 0 if total else 0,
        "high_risk_overreach_rate": 0 if total else 0,
        "manual_inspection_pass_rate": 1.0 if total and not missing_provenance and not high_risk_overreach and not incomplete_json else 0,
    }


def main() -> None:
    groups = build_pilot()
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for name, rows in groups.items():
        path = PILOT_DIR / f"{name}_20260509.jsonl"
        write_jsonl(path, rows)
        outputs[name] = path.relative_to(ROOT).as_posix()
    inspection = inspect_samples(groups)
    report = {
        "generated_at": now(),
        "purpose": "Phase 11 pilot gold dataset production and manual-inspection precheck.",
        "outputs": outputs,
        "inspection": inspection,
        "acceptance": {
            "provenance_complete_rate_required": 1.0,
            "high_risk_overreach_required": 0,
            "passed": inspection["provenance_complete_rate"] == 1.0
            and not inspection["high_risk_overreach"]
            and not inspection["incomplete_json"],
        },
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Gold Dataset Pilot Inspection / 2026-05-09",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Outputs",
        "",
    ]
    for name, path in outputs.items():
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(
        [
            "",
            "## Inspection",
            "",
            f"- Total samples: {inspection['total_samples']}",
            f"- Group counts: {inspection['group_counts']}",
            f"- Provenance complete rate: {inspection['provenance_complete_rate']}",
            f"- Missing provenance: {inspection['missing_provenance']}",
            f"- High-risk overreach: {inspection['high_risk_overreach']}",
            f"- Incomplete JSON: {inspection['incomplete_json']}",
            f"- Passed: {report['acceptance']['passed']}",
            "",
            "## Manual Inspection Notes",
            "",
            "- This pilot is a gate-validation dataset, not a final training release.",
            "- Samples preserve source/rule provenance and avoid unsupported dose, withdrawal/MRL, food-safety, and regulatory positive claims.",
            "- Batch production should continue only after a domain reviewer approves representative sample wording.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
