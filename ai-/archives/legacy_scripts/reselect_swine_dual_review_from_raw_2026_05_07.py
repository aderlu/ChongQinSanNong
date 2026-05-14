from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "swine_weak_wiki_production"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
DOSE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:mg/kg|mg|ml|mL|g/L|g|ppm|IU|万单位)", re.I)
WITHDRAW_RE = re.compile(r"\d+\s*(?:天|日|小时|hour|hours|day|days).{0,12}(?:休药|停药|withdrawal)", re.I)


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    return normalized in {"true", "1", "yes", "y", "是", "有", "高风险"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def score(row: Mapping[str, str]) -> float:
    try:
        return float(row.get("final_total_score") or 0)
    except Exception:
        return 0.0


def row_text(row: Mapping[str, str]) -> str:
    return "\n".join([row.get("user_query", ""), row.get("diagnosis", ""), row.get("prescription", ""), row.get("withdrawal_period", "")])


def local_fatal(row: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []
    text = row_text(row)
    if row.get("species") != "猪":
        reasons.append("species_not_swine")
    if row.get("target_disease_mismatch") == "True":
        reasons.append("target_disease_mismatch")
    if DOSE_RE.search(text):
        reasons.append("specific_dose")
    if WITHDRAW_RE.search(row.get("withdrawal_period", "")):
        reasons.append("specific_withdrawal")
    if row.get("judge_a_fatal_risk") == "True":
        reasons.append("first_pass_fatal")
    return reasons


def final_decision(row: Mapping[str, str], judge_b: Mapping[str, Any], arbiter: Mapping[str, Any] | None, local_reasons: list[str]) -> tuple[str, float, bool]:
    b_score = float(judge_b.get("total_score") or 0)
    if arbiter:
        label = str(arbiter.get("arbiter_final_label") or "review")
        final_score = float(arbiter.get("arbiter_final_score") or min(score(row), b_score))
        fatal = as_bool(arbiter.get("arbiter_fatal_risk"))
        if local_reasons and "target_disease_mismatch" not in local_reasons:
            fatal = True
        return label, final_score, fatal
    if local_reasons:
        return "reject", min(score(row), b_score), True
    if row.get("final_label") == "pass" and judge_b.get("final_label") == "pass" and score(row) >= 80 and b_score >= 80 and not as_bool(judge_b.get("fatal_risk")):
        return "pass", round((score(row) + b_score) / 2, 2), False
    if min(score(row), b_score) >= 75 and not as_bool(judge_b.get("fatal_risk")):
        return "review", round((score(row) + b_score) / 2, 2), False
    return "reject", round((score(row) + b_score) / 2, 2), as_bool(judge_b.get("fatal_risk"))


def update_row(item: Mapping[str, Any], fieldnames: list[str]) -> dict[str, str]:
    row = dict(item["row"])
    judge_b = item.get("judge_b") or {}
    arbiter = item.get("arbiter") or {}
    local_reasons = local_fatal(row)
    label, final_score, fatal = final_decision(row, judge_b, arbiter, local_reasons)
    row["judge_b_model"] = str(item.get("judge_b_model") or "")
    row["judge_b_total_score"] = str(judge_b.get("total_score", ""))
    row["judge_b_diagnosis_accuracy"] = str(judge_b.get("diagnosis_accuracy", ""))
    row["judge_b_pathology_logic"] = str(judge_b.get("pathology_logic", ""))
    row["judge_b_prescription_safety"] = str(judge_b.get("prescription_safety", ""))
    row["judge_b_data_quality"] = str(judge_b.get("data_quality", ""))
    row["judge_b_fatal_risk"] = "True" if as_bool(judge_b.get("fatal_risk")) else "False"
    row["judge_b_structured_pass"] = "True" if judge_b.get("final_label") == "pass" else "False"
    row["judge_b_summary"] = str(judge_b.get("summary") or "")
    row["needed_arbitration"] = "True" if item.get("needed_arbitration") else "False"
    row["arbiter_model"] = str(item.get("arbiter_model") or "")
    row["arbiter_agreed_with_judge"] = str(arbiter.get("arbiter_agreed_with_judge", ""))
    row["arbiter_final_label"] = str(arbiter.get("arbiter_final_label", ""))
    row["arbiter_reason"] = str(arbiter.get("arbiter_reason", ""))
    row["final_total_score"] = str(final_score)
    row["final_fatal_risk"] = "True" if fatal else "False"
    row["final_label"] = label
    row["judge_b_seconds"] = str(item.get("elapsed", ""))
    row["rule_codes"] = "|".join(local_reasons)
    row["rule_messages"] = "|".join(local_reasons)
    return {key: row.get(key, "") for key in fieldnames}


def main() -> None:
    parser = argparse.ArgumentParser(description="Recompute dual-review selection from saved raw JSON.")
    parser.add_argument("--raw-json", required=True)
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--target", type=int, default=300)
    args = parser.parse_args()

    input_path = Path(args.input_csv)
    fieldnames = list(read_rows(input_path)[0].keys())
    reviewed = json.loads(Path(args.raw_json).read_text(encoding="utf-8"))
    updated = [update_row(item, fieldnames) for item in reviewed]
    updated.sort(key=lambda row: (row.get("final_label") != "pass", row.get("final_fatal_risk") != "False", -float(row.get("final_total_score") or 0), int(row.get("index") or 0)))
    valid = [row for row in updated if row.get("final_label") == "pass" and row.get("final_fatal_risk") == "False" and not local_fatal(row)]
    final_rows = valid[: args.target]
    rejects = [row for row in updated if row not in final_rows]

    stem = input_path.stem
    out_full = RESULTS / f"{stem}_dual_reviewed_reselected_{TIMESTAMP}.csv"
    out_final = RESULTS / f"{stem}_dual_final{args.target}_reselected_{TIMESTAMP}.csv"
    out_rejects = RESULTS / f"{stem}_dual_rejects_reselected_{TIMESTAMP}.csv"
    summary_path = RESULTS / f"{stem}_dual_review_reselected_summary_{TIMESTAMP}.json"

    write_rows(out_full, updated, fieldnames)
    write_rows(out_final, final_rows, fieldnames)
    write_rows(out_rejects, rejects, fieldnames)
    valid_scores = [float(row.get("final_total_score") or 0) for row in final_rows]
    summary = {
        "input_csv": str(input_path),
        "raw_json": str(Path(args.raw_json)),
        "second_reviewed": len(reviewed),
        "dual_valid": len(valid),
        "final_selected": len(final_rows),
        "target": args.target,
        "final_score_avg": round(statistics.mean(valid_scores), 2) if valid_scores else 0,
        "final_score_min": min(valid_scores) if valid_scores else 0,
        "final_score_max": max(valid_scores) if valid_scores else 0,
        "arbitration_count": sum(1 for item in reviewed if item.get("needed_arbitration")),
        "output_full": str(out_full),
        "output_final": str(out_final),
        "output_rejects": str(out_rejects),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({**summary, "summary": str(summary_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
