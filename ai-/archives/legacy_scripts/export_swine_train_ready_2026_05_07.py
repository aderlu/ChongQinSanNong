from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results" / "swine_qa_dataset" / "swine_qa_dataset_20260507_130918_usable_candidates.csv"
OUTPUT_DIR = ROOT / "results" / "swine_qa_dataset"
ALIAS_INDEX = ROOT / "knowledge" / "llm_wiki_swine_authoritative" / "exports" / "alias_index.csv"

SOURCE_RE = re.compile(r"\b(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+)\b")
INTERNAL_ANCHOR_RE = re.compile(r"\b[a-z][a-z0-9]+(?:_[a-z0-9]+){2,}\b")
DOSE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:mg/kg|mg|ml|mL|g/L|g|ppm|IU|万单位)", re.I)
WITHDRAWAL_RE = re.compile(r"\d+\s*(?:天|日|小时|hour|hours|day|days).{0,12}(?:休药|停药|withdrawal)", re.I)
EXECUTABLE_RISK_RE = re.compile(
    r"(?:剂量|用量|疗程|休药|停药|withdrawal|MRL|残留|可食|出栏|上市|销售|扑杀|调运|检疫|无害化|强制免疫)",
    re.I,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export strict train-ready JSONL from swine QA candidate CSV.")
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-jsonl", default="")
    parser.add_argument("--rejects-csv", default="")
    parser.add_argument("--min-score", type=float, default=82.0)
    parser.add_argument("--min-standard-citations", type=int, default=2)
    parser.add_argument(
        "--policy",
        choices=["balanced", "strict_authority"],
        default="balanced",
        help="balanced accepts any qualified source for clinical data; strict_authority keeps A0/A1 hard gates.",
    )
    return parser.parse_args()


def load_aliases() -> dict[str, set[str]]:
    aliases: dict[str, set[str]] = {}
    if not ALIAS_INDEX.exists():
        return aliases
    with ALIAS_INDEX.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            canonical = row.get("canonical_name", "").strip()
            alias = row.get("alias", "").strip()
            if not canonical or not alias:
                continue
            aliases.setdefault(canonical, set()).add(alias)
            aliases.setdefault(alias, set()).add(canonical)
            aliases[canonical].add(canonical)
    return aliases


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def parse_json(value: str, default: Any) -> Any:
    try:
        return json.loads(value) if value else default
    except json.JSONDecodeError:
        return default


def as_float(value: str) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def answer_text(row: dict[str, str]) -> str:
    return "\n".join(
        [
            row.get("diagnosis", ""),
            row.get("prescription", ""),
            row.get("withdrawal_period", ""),
            row.get("answer_json", ""),
            row.get("golden_answer", ""),
            row.get("evidence_anchors", ""),
        ]
    ).strip()


def is_authority_source(source: str) -> bool:
    return source.startswith(("A0-", "A1-"))


def is_qualified_source(source: str) -> bool:
    return bool(SOURCE_RE.fullmatch(source))


def infer_task_use(row: dict[str, str], sources: set[str], args: argparse.Namespace) -> str:
    text = answer_text(row)
    score = as_float(row.get("final_total_score", ""))
    if row.get("final_label") != "pass" or row.get("final_fatal_risk") == "True":
        return "blocked"
    if score < args.min_score:
        return "eval_ready"
    if len(sources) < args.min_standard_citations:
        return "generation_ready_limited"
    if EXECUTABLE_RISK_RE.search(text) and not any(is_authority_source(source) for source in sources):
        return "generation_ready_limited"
    return "train_ready"


def disease_alias_hit(row: dict[str, str], aliases: dict[str, set[str]]) -> bool:
    diagnosis = row.get("diagnosis", "").lower()
    disease = row.get("disease_name", "").strip()
    candidates = set(aliases.get(disease, set()))
    candidates.add(disease)
    metadata = parse_json(row.get("metadata", ""), {})
    for key in ["disease_name", "target_disease", "canonical_name", "english_name"]:
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            candidates.add(value.strip())
            candidates.update(aliases.get(value.strip(), set()))
    for key in ["aliases", "abbreviations", "common_names"]:
        value = metadata.get(key)
        if isinstance(value, list):
            candidates.update(str(item).strip() for item in value if str(item).strip())
    return any(alias and alias.lower() in diagnosis for alias in candidates)


def evaluate_row(row: dict[str, str], aliases: dict[str, set[str]], args: argparse.Namespace) -> list[str]:
    reasons: list[str] = []
    text = answer_text(row)
    sources = set(SOURCE_RE.findall(text))
    score = as_float(row.get("final_total_score", ""))
    if row.get("final_label") != "pass":
        reasons.append("final_label_not_pass")
    if score < args.min_score:
        reasons.append("score_below_min")
    if row.get("final_fatal_risk") == "True":
        reasons.append("fatal_risk")
    if not disease_alias_hit(row, aliases):
        reasons.append("target_disease_alias_not_in_diagnosis")
    if len(sources) < args.min_standard_citations:
        reasons.append("too_few_standard_citations")
    if INTERNAL_ANCHOR_RE.search(text) and len(sources) == 0:
        reasons.append("internal_anchor_without_source_id")
    if args.policy == "strict_authority":
        if DOSE_RE.search(text) and not any(is_authority_source(source) for source in sources):
            reasons.append("specific_dose_without_authority_source")
        if WITHDRAWAL_RE.search(text) and not any(is_authority_source(source) for source in sources):
            reasons.append("specific_withdrawal_without_authority_source")
    else:
        if DOSE_RE.search(text) and not sources:
            reasons.append("specific_dose_without_qualified_source")
        if WITHDRAWAL_RE.search(text) and not any(is_authority_source(source) for source in sources):
            reasons.append("specific_withdrawal_without_label_or_official_source")
    answer_json = parse_json(row.get("answer_json", ""), {})
    if not answer_json:
        reasons.append("missing_answer_json")
    else:
        for key in ["diagnosis", "action_plan", "withdrawal_boundary", "evidence_sources"]:
            if key not in answer_json:
                reasons.append(f"answer_json_missing_{key}")
        evidence_sources = answer_json.get("evidence_sources")
        if not isinstance(evidence_sources, list) or len([x for x in evidence_sources if SOURCE_RE.fullmatch(str(x))]) < args.min_standard_citations:
            reasons.append("answer_json_too_few_evidence_sources")
    return reasons


def build_messages(row: dict[str, str]) -> list[dict[str, str]]:
    answer = parse_json(row.get("answer_json", ""), {})
    if not answer:
        answer = {
            "diagnosis": row.get("diagnosis", ""),
            "action_plan": row.get("prescription", ""),
            "withdrawal_boundary": row.get("withdrawal_period", ""),
        }
    answer.setdefault("natural_language_answer", {
        "diagnosis": row.get("diagnosis", ""),
        "treatment_or_action": row.get("prescription", ""),
        "withdrawal_period_boundary": row.get("withdrawal_period", ""),
    })
    return [
        {
            "role": "system",
            "content": "你是猪病问诊辅助模型。必须基于证据回答，涉及诊断、采样、监管、用药和休药期时保留标准 source=... 引用；不得编造剂量、疗程或休药期。",
        },
        {"role": "user", "content": row.get("user_query", "")},
        {"role": "assistant", "content": json.dumps(answer, ensure_ascii=False, separators=(",", ":"))},
    ]


def build_gold_record(row: dict[str, str], input_path: Path, task_use: str) -> dict[str, Any]:
    answer = parse_json(row.get("answer_json", ""), {})
    evidence_anchors = parse_json(row.get("evidence_anchors", ""), [])
    metadata = parse_json(row.get("metadata", ""), {})
    citations = sorted(set(SOURCE_RE.findall(answer_text(row))))
    return {
        "case_id": row.get("case_id", ""),
        "task_type": row.get("training_task_type", "swine_clinical_qa_source_grounded"),
        "task_use": task_use,
        "species": row.get("species", "猪"),
        "disease_name": row.get("disease_name", ""),
        "user_query": row.get("user_query", ""),
        "messages": build_messages(row),
        "answer_json": answer,
        "evidence": {
            "citations": citations,
            "anchors": evidence_anchors,
            "wiki_dir": row.get("wiki_dir", ""),
            "wiki_context_query": row.get("wiki_context_query", ""),
            "wiki_fact_count": row.get("wiki_fact_count", ""),
            "wiki_page_count": row.get("wiki_page_count", ""),
        },
        "quality": {
            "final_label": row.get("final_label", ""),
            "final_total_score": as_float(row.get("final_total_score", "")),
            "final_diagnosis_accuracy": as_float(row.get("final_diagnosis_accuracy", "")),
            "final_pathology_logic": as_float(row.get("final_pathology_logic", "")),
            "final_prescription_safety": as_float(row.get("final_prescription_safety", "")),
            "final_data_quality": as_float(row.get("final_data_quality", "")),
            "judge_a_model": row.get("judge_a_model", ""),
            "judge_b_model": row.get("judge_b_model", ""),
            "arbiter_model": row.get("arbiter_model", ""),
        },
        "safety": {
            "final_fatal_risk": row.get("final_fatal_risk", ""),
            "rule_codes": row.get("rule_codes", ""),
            "rule_messages": row.get("rule_messages", ""),
        },
        "metadata": {
            **metadata,
            "source_csv": str(input_path),
            "schema": "swine_sft_gold_v2_balanced_source_use",
        },
    }


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_csv)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_jsonl = Path(args.output_jsonl) if args.output_jsonl else OUTPUT_DIR / f"swine_train_ready_{stamp}.jsonl"
    rejects_csv = Path(args.rejects_csv) if args.rejects_csv else OUTPUT_DIR / f"swine_train_ready_rejects_{stamp}.csv"
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)

    rows = read_rows(input_path)
    aliases = load_aliases()
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for row in rows:
        reasons = evaluate_row(row, aliases, args)
        sources = set(SOURCE_RE.findall(answer_text(row)))
        task_use = infer_task_use(row, sources, args)
        if reasons:
            rejected.append(
                {
                    "case_id": row.get("case_id", ""),
                    "disease_name": row.get("disease_name", ""),
                    "final_label": row.get("final_label", ""),
                    "final_total_score": row.get("final_total_score", ""),
                    "task_use": task_use,
                    "reject_reasons": "|".join(reasons),
                }
            )
            continue
        accepted.append(build_gold_record(row, input_path, task_use))

    with output_jsonl.open("w", encoding="utf-8", newline="\n") as fh:
        for item in accepted:
            fh.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")

    with rejects_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["case_id", "disease_name", "final_label", "final_total_score", "task_use", "reject_reasons"])
        writer.writeheader()
        writer.writerows(rejected)

    summary = {
        "input_csv": str(input_path),
        "output_jsonl": str(output_jsonl),
        "rejects_csv": str(rejects_csv),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "min_score": args.min_score,
        "min_standard_citations": args.min_standard_citations,
        "policy": args.policy,
        "accepted_task_use_counts": {
            task_use: sum(1 for item in accepted if item.get("task_use") == task_use)
            for task_use in sorted({str(item.get("task_use")) for item in accepted})
        },
    }
    summary_path = output_jsonl.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
