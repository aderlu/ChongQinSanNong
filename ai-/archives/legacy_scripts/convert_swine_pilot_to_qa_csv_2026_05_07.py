from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "results" / "swine_parallel_pilot"
OUTPUT_DIR = ROOT / "results" / "swine_qa_dataset"


FIELDNAMES = [
    "case_id",
    "index",
    "disease_name",
    "generator_key",
    "generator_model",
    "success",
    "error",
    "species",
    "user_query",
    "diagnosis",
    "prescription",
    "withdrawal_period",
    "metadata",
    "rule_hard_block",
    "rule_fatal_risk",
    "rule_codes",
    "rule_messages",
    "target_disease_in_diagnosis",
    "target_disease_mismatch",
    "final_fatal_risk",
    "wiki_dir",
    "wiki_fact_count",
    "wiki_page_count",
    "wiki_context_query",
    "wiki_evidence_status_counts",
    "wiki_evidence_source_ids",
    "wiki_context_chars",
    "generation_seconds",
    "judge_a_model",
    "judge_a_total_score",
    "judge_a_diagnosis_accuracy",
    "judge_a_pathology_logic",
    "judge_a_prescription_safety",
    "judge_a_data_quality",
    "judge_a_fatal_risk",
    "judge_a_structured_pass",
    "judge_a_summary",
    "judge_b_model",
    "judge_b_total_score",
    "judge_b_diagnosis_accuracy",
    "judge_b_pathology_logic",
    "judge_b_prescription_safety",
    "judge_b_data_quality",
    "judge_b_fatal_risk",
    "judge_b_structured_pass",
    "judge_b_summary",
    "needed_arbitration",
    "arbiter_model",
    "arbiter_agreed_with_judge",
    "arbiter_final_label",
    "arbiter_reason",
    "final_total_score",
    "final_diagnosis_accuracy",
    "final_pathology_logic",
    "final_prescription_safety",
    "final_data_quality",
    "final_label",
    "judge_a_seconds",
    "judge_b_seconds",
    "arbiter_seconds",
    "answer_json",
    "judge_json",
    "local_flags_json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert swine pilot JSON into chicken-production-like QA CSV.")
    parser.add_argument("--input-json", default="", help="Path to swine_parallel_pilot_*.json. Defaults to latest.")
    parser.add_argument("--output-csv", default="", help="Output CSV path. Defaults to results/swine_qa_dataset.")
    return parser.parse_args()


def latest_input() -> Path:
    files = sorted(DEFAULT_INPUT_DIR.glob("swine_parallel_pilot_*.json"))
    files = [p for p in files if "summary" not in p.name]
    if not files:
        raise FileNotFoundError(f"No swine pilot JSON found in {DEFAULT_INPUT_DIR}")
    return files[-1]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "；".join(as_text(item) for item in value if item is not None)
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            if item in ("", None, [], {}):
                continue
            parts.append(f"{key}: {as_text(item)}")
        return "；".join(parts)
    return str(value)


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def disease_aliases(disease_name: str, metadata: dict[str, Any]) -> list[str]:
    aliases: list[str] = []
    for value in [
        disease_name,
        metadata.get("disease_name"),
        metadata.get("target_disease"),
        metadata.get("canonical_name"),
        metadata.get("english_name"),
    ]:
        if isinstance(value, str) and value.strip():
            aliases.append(value.strip())
    for key in ["aliases", "alias", "abbreviations", "common_names"]:
        value = metadata.get(key)
        if isinstance(value, str):
            aliases.append(value.strip())
        elif isinstance(value, list):
            aliases.extend(str(item).strip() for item in value if str(item).strip())

    manual = {
        "anelloviruses torque teno sus viruses": ["猪环曲病毒", "托克特诺病毒", "TTSuV", "Torque teno sus virus"],
        "astroviruses": ["猪星状病毒", "星状病毒", "PoAstV", "astrovirus"],
        "猪布鲁氏菌病": ["布鲁氏菌病", "Brucella suis", "猪布鲁氏杆菌病"],
        "猪痢疾": ["swine dysentery", "Brachyspira hyodysenteriae"],
    }
    for key, values in manual.items():
        if disease_name.lower() == key.lower() or key.lower() in disease_name.lower():
            aliases.extend(values)
    return list(dict.fromkeys(alias for alias in aliases if alias))


def score_component(judge: dict[str, Any], names: list[str]) -> str:
    for name in names:
        value = judge.get(name)
        if value not in (None, ""):
            return str(value)
    return ""


def convert_row(row: dict[str, Any]) -> dict[str, Any]:
    draft = row.get("draft") if isinstance(row.get("draft"), dict) else {}
    answer = row.get("answer") if isinstance(row.get("answer"), dict) else {}
    judge = row.get("judge") if isinstance(row.get("judge"), dict) else {}
    audit = row.get("wiki_audit") if isinstance(row.get("wiki_audit"), dict) else {}
    flags = row.get("local_flags") if isinstance(row.get("local_flags"), dict) else {}
    stage_times = row.get("stage_times") if isinstance(row.get("stage_times"), dict) else {}
    model_usage = row.get("model_usage") if isinstance(row.get("model_usage"), dict) else {}

    metadata = answer.get("metadata") if isinstance(answer.get("metadata"), dict) else {}
    merged_metadata = dict(draft.get("metadata") if isinstance(draft.get("metadata"), dict) else {})
    merged_metadata.update(metadata)
    merged_metadata.setdefault("case_type", row.get("case_type", ""))
    merged_metadata.setdefault("target_disease", row.get("target", ""))

    diagnosis = as_text(answer.get("diagnosis"))
    prescription_parts = [
        as_text(answer.get("treatment_or_action")),
        as_text(answer.get("drug_boundary")),
        as_text(answer.get("sampling_plan")),
    ]
    prescription = "\n".join(part for part in prescription_parts if part)
    withdrawal = as_text(answer.get("withdrawal_period_boundary") or answer.get("withdrawal_period"))

    disease_name = str(row.get("target") or merged_metadata.get("disease_name") or "")
    aliases = disease_aliases(disease_name, merged_metadata)
    diagnosis_contains = bool(aliases and any(alias.lower() in diagnosis.lower() for alias in aliases))
    label = str(judge.get("final_label") or "")

    return {
        "case_id": row.get("case_id", ""),
        "index": row.get("index", ""),
        "disease_name": disease_name,
        "generator_key": "swine_hunyuan_turbos",
        "generator_model": model_usage.get("answer_model") or model_usage.get("draft_model") or "",
        "success": "成功" if answer else "失败",
        "error": model_usage.get("answer_error") or model_usage.get("draft_error") or "",
        "species": answer.get("species") or draft.get("species") or "猪",
        "user_query": answer.get("user_query") or draft.get("user_query") or "",
        "diagnosis": diagnosis,
        "prescription": prescription,
        "withdrawal_period": withdrawal,
        "metadata": json_text(merged_metadata),
        "rule_hard_block": "True" if flags.get("judge_fatal") else "False",
        "rule_fatal_risk": "True" if flags.get("judge_fatal") else "False",
        "rule_codes": "",
        "rule_messages": "",
        "target_disease_in_diagnosis": "True" if diagnosis_contains else "False",
        "target_disease_mismatch": "False" if diagnosis_contains else "True",
        "final_fatal_risk": "True" if judge.get("fatal_risk") else "False",
        "wiki_dir": audit.get("wiki_dir", ""),
        "wiki_fact_count": audit.get("wiki_fact_count", ""),
        "wiki_page_count": audit.get("wiki_page_count", ""),
        "wiki_context_query": audit.get("wiki_context_query", ""),
        "wiki_evidence_status_counts": json_text(audit.get("wiki_evidence_status_counts", {})),
        "wiki_evidence_source_ids": json_text(audit.get("wiki_evidence_source_ids", [])),
        "wiki_context_chars": audit.get("wiki_context_chars", ""),
        "generation_seconds": stage_times.get("total_seconds", ""),
        "judge_a_model": model_usage.get("judge_model", ""),
        "judge_a_total_score": judge.get("total_score", ""),
        "judge_a_diagnosis_accuracy": score_component(judge, ["diagnosis_accuracy", "clinical_reasoning", "clinical_fit_score"]),
        "judge_a_pathology_logic": score_component(judge, ["pathology_logic", "diagnostic_sampling", "evidence_anchoring"]),
        "judge_a_prescription_safety": score_component(judge, ["prescription_safety", "drug_boundary", "regulatory_safety"]),
        "judge_a_data_quality": score_component(judge, ["data_quality", "data_usability"]),
        "judge_a_fatal_risk": "True" if judge.get("fatal_risk") else "False",
        "judge_a_structured_pass": "True" if label == "pass" else "False",
        "judge_a_summary": as_text(judge.get("strengths")) + ("\n问题：" + as_text(judge.get("weaknesses")) if judge.get("weaknesses") else ""),
        "judge_b_model": "",
        "judge_b_total_score": "",
        "judge_b_diagnosis_accuracy": "",
        "judge_b_pathology_logic": "",
        "judge_b_prescription_safety": "",
        "judge_b_data_quality": "",
        "judge_b_fatal_risk": "",
        "judge_b_structured_pass": "",
        "judge_b_summary": "",
        "needed_arbitration": "False",
        "arbiter_model": "",
        "arbiter_agreed_with_judge": "",
        "arbiter_final_label": "",
        "arbiter_reason": "",
        "final_total_score": judge.get("total_score", ""),
        "final_diagnosis_accuracy": score_component(judge, ["diagnosis_accuracy", "clinical_reasoning", "clinical_fit_score"]),
        "final_pathology_logic": score_component(judge, ["pathology_logic", "diagnostic_sampling", "evidence_anchoring"]),
        "final_prescription_safety": score_component(judge, ["prescription_safety", "drug_boundary", "regulatory_safety"]),
        "final_data_quality": score_component(judge, ["data_quality", "data_usability"]),
        "final_label": label,
        "judge_a_seconds": stage_times.get("judge_seconds", ""),
        "judge_b_seconds": "",
        "arbiter_seconds": "",
        "answer_json": json_text(answer),
        "judge_json": json_text(judge),
        "local_flags_json": json_text(flags),
    }


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_json) if args.input_json else latest_input()
    rows = json.loads(input_path.read_text(encoding="utf-8"))
    output = Path(args.output_csv) if args.output_csv else OUTPUT_DIR / f"swine_qa_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    converted = [convert_row(row) for row in rows]
    with output.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(converted)
    summary = {
        "input_json": str(input_path),
        "output_csv": str(output),
        "rows": len(converted),
        "pass": sum(1 for row in converted if row["final_label"] == "pass"),
        "review": sum(1 for row in converted if row["final_label"] == "review"),
        "reject": sum(1 for row in converted if row["final_label"] == "reject"),
    }
    summary_path = output.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
