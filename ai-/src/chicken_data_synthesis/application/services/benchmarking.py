from __future__ import annotations

import json
import statistics
from typing import Any, Dict, Iterable, Mapping, Sequence

from chicken_data_synthesis.infrastructure.evaluation.normalizers import normalize_judge_payload


def compute_label(avg_total_score: float, fatal_risk_rate: float, structured_pass_rate: float) -> str:
    if fatal_risk_rate > 0:
        return "reject"
    if avg_total_score >= 90 and structured_pass_rate >= 1:
        return "pass"
    if avg_total_score >= 75:
        return "review"
    return "reject"


def build_generation_failure_judge_rows(
    evaluators: Mapping[str, Mapping[str, Any]],
    *,
    error: str = "generation_failed",
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for judge_key, judge_config in evaluators.items():
        if not judge_key:
            continue
        rows.append(
            {
                "judge_key": judge_key,
                "judge_model": judge_config.get("name", ""),
                "judge_seconds": 0.0,
                "parse_ok": False,
                "error": error,
                "total_score": 0.0,
                "diagnosis_accuracy": 0.0,
                "pathology_logic": 0.0,
                "prescription_safety": 0.0,
                "data_quality": 0.0,
                "fatal_risk": False,
                "structured_pass": False,
                "summary": "",
            }
        )
    return rows


def normalize_benchmark_judge_result(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = normalize_judge_payload(payload, allow_ratio_scale=True)
    return {
        "total_score": normalized["total_score"],
        "diagnosis_accuracy": normalized["diagnosis_accuracy"],
        "pathology_logic": normalized["pathology_logic"],
        "prescription_safety": normalized["prescription_safety"],
        "data_quality": normalized["data_quality"],
        "fatal_risk": normalized["fatal_risk"],
        "structured_pass": normalized["structured_pass"],
        "summary": normalized["summary"],
    }


def aggregate_judge_rows(judge_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    judge_scores = [float(row.get("total_score", 0.0) or 0.0) for row in judge_rows if row.get("parse_ok")]
    avg_total = round(statistics.mean(judge_scores), 2) if judge_scores else 0.0
    avg_diag = round(_mean_or_zero(float(row.get("diagnosis_accuracy", 0.0) or 0.0) for row in judge_rows), 2)
    avg_logic = round(_mean_or_zero(float(row.get("pathology_logic", 0.0) or 0.0) for row in judge_rows), 2)
    avg_rx = round(_mean_or_zero(float(row.get("prescription_safety", 0.0) or 0.0) for row in judge_rows), 2)
    avg_quality = round(_mean_or_zero(float(row.get("data_quality", 0.0) or 0.0) for row in judge_rows), 2)
    fatal_risk_rate = round(
        sum(1 for row in judge_rows if row.get("fatal_risk")) / max(len(judge_rows), 1),
        4,
    )
    structured_pass_rate = round(
        sum(1 for row in judge_rows if row.get("structured_pass")) / max(len(judge_rows), 1),
        4,
    )

    return {
        "judge_count_success": sum(1 for row in judge_rows if row.get("error") == ""),
        "judge_count_parse_ok": sum(1 for row in judge_rows if row.get("parse_ok")),
        "avg_total_score": avg_total,
        "avg_diagnosis_accuracy": avg_diag,
        "avg_pathology_logic": avg_logic,
        "avg_prescription_safety": avg_rx,
        "avg_data_quality": avg_quality,
        "score_stddev": round(statistics.pstdev(judge_scores), 2) if len(judge_scores) > 1 else 0.0,
        "fatal_risk_rate": fatal_risk_rate,
        "structured_pass_rate": structured_pass_rate,
        "overall_label": compute_label(avg_total, fatal_risk_rate, structured_pass_rate),
    }


def build_judge_columns(judge_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    columns: dict[str, Any] = {}
    for index, judge_row in enumerate(judge_rows, start=1):
        prefix = f"judge_{index}_"
        columns[prefix + "key"] = judge_row.get("judge_key", "")
        columns[prefix + "model"] = judge_row.get("judge_model", "")
        columns[prefix + "total_score"] = judge_row.get("total_score", 0.0)
        columns[prefix + "diagnosis_accuracy"] = judge_row.get("diagnosis_accuracy", 0.0)
        columns[prefix + "pathology_logic"] = judge_row.get("pathology_logic", 0.0)
        columns[prefix + "prescription_safety"] = judge_row.get("prescription_safety", 0.0)
        columns[prefix + "data_quality"] = judge_row.get("data_quality", 0.0)
        columns[prefix + "fatal_risk"] = judge_row.get("fatal_risk", False)
        columns[prefix + "structured_pass"] = judge_row.get("structured_pass", False)
        columns[prefix + "summary"] = judge_row.get("summary", "")
        columns[prefix + "seconds"] = judge_row.get("judge_seconds", 0.0)
        columns[prefix + "parse_ok"] = judge_row.get("parse_ok", False)
        columns[prefix + "error"] = judge_row.get("error", "")
    return columns


def build_benchmark_summary_row(
    *,
    benchmark_style: str,
    task_type: str,
    dataset_key: str,
    dataset_name: str,
    combo: Mapping[str, Any],
    generator_model: str,
    evaluator_models: Mapping[str, str],
    generator_rows: Sequence[Mapping[str, Any]],
    requested_samples: int,
) -> dict[str, Any]:
    judge_keys = list(combo.get("judge_keys", []))
    while len(judge_keys) < 3:
        judge_keys.append("")

    return {
        "benchmark_style": benchmark_style,
        "task_type": task_type,
        "dataset_key": dataset_key,
        "dataset_name": dataset_name,
        "combination_key": combo["combination_key"],
        "generator_key": combo["generator_key"],
        "generator_model": generator_model,
        "judge_1_key": judge_keys[0],
        "judge_1_model": evaluator_models.get(judge_keys[0], ""),
        "judge_2_key": judge_keys[1],
        "judge_2_model": evaluator_models.get(judge_keys[1], ""),
        "judge_3_key": judge_keys[2],
        "judge_3_model": evaluator_models.get(judge_keys[2], ""),
        "requested_samples": requested_samples,
        "success_count": len([row for row in generator_rows if row.get("generator_success")]),
        "failed_count": requested_samples - len([row for row in generator_rows if row.get("generator_success")]),
        "success_rate": round(
            len([row for row in generator_rows if row.get("generator_success")]) / max(requested_samples, 1),
            4,
        ),
        "avg_generation_seconds": round(_mean_or_zero(row.get("generation_seconds", 0.0) for row in generator_rows), 3),
        "avg_judge_seconds": round(
            _mean_or_zero(
                row.get("judge_1_seconds", 0.0) + row.get("judge_2_seconds", 0.0) + row.get("judge_3_seconds", 0.0)
                for row in generator_rows
            ),
            3,
        ),
        "avg_total_score": round(_mean_or_zero(row.get("avg_total_score", 0.0) for row in generator_rows), 2),
        "avg_diagnosis_accuracy": round(
            _mean_or_zero(row.get("avg_diagnosis_accuracy", 0.0) for row in generator_rows),
            2,
        ),
        "avg_pathology_logic": round(
            _mean_or_zero(row.get("avg_pathology_logic", 0.0) for row in generator_rows),
            2,
        ),
        "avg_prescription_safety": round(
            _mean_or_zero(row.get("avg_prescription_safety", 0.0) for row in generator_rows),
            2,
        ),
        "avg_data_quality": round(_mean_or_zero(row.get("avg_data_quality", 0.0) for row in generator_rows), 2),
        "score_stddev_mean": round(_mean_or_zero(row.get("score_stddev", 0.0) for row in generator_rows), 2),
        "fatal_risk_rate": round(_mean_or_zero(row.get("fatal_risk_rate", 0.0) for row in generator_rows), 4),
        "structured_pass_rate": round(
            _mean_or_zero(row.get("structured_pass_rate", 0.0) for row in generator_rows),
            4,
        ),
        "pass_rate": round(
            sum(1 for row in generator_rows if row.get("overall_label") == "pass") / max(requested_samples, 1),
            4,
        ),
        "review_rate": round(
            sum(1 for row in generator_rows if row.get("overall_label") == "review") / max(requested_samples, 1),
            4,
        ),
        "reject_rate": round(
            sum(1 for row in generator_rows if row.get("overall_label") == "reject") / max(requested_samples, 1),
            4,
        ),
    }


def build_benchmark_detail_base_row(
    work_item: Any,
    case_seed: Mapping[str, Any],
    *,
    generator_model: str,
    generation_success: bool,
    generation_error: str,
    generation_seconds: float,
) -> dict[str, Any]:
    return {
        "case_id": getattr(work_item, "case_id"),
        "benchmark_style": getattr(work_item, "benchmark_style"),
        "task_type": getattr(work_item, "task_type"),
        "instance_id": case_seed.get("instance_id", ""),
        "dataset_key": getattr(work_item, "dataset_key"),
        "dataset_name": getattr(work_item, "dataset_name"),
        "combination_key": getattr(work_item, "combination_key"),
        "sample_index": getattr(work_item, "sample_index"),
        "disease_name": case_seed.get("disease_name", ""),
        "scenario_hint": case_seed.get("scenario_hint", ""),
        "problem_statement": case_seed.get("problem_statement", ""),
        "acceptance_criteria_json": json.dumps(case_seed.get("acceptance_criteria", []), ensure_ascii=False),
        "generator_key": getattr(work_item, "generator_key"),
        "generator_model": generator_model,
        "generator_success": generation_success,
        "generator_error": generation_error,
        "generation_seconds": round(generation_seconds, 3),
        "species": "",
        "user_query": "",
        "diagnosis": "",
        "prescription": "",
        "withdrawal_period": "",
        "metadata_json": "",
    }


def build_benchmark_summary_context_key(work_item: Any) -> tuple[str, str]:
    return getattr(work_item, "dataset_key"), getattr(work_item, "combination_key")


def build_benchmark_summary_context(
    work_item: Any,
    combo: Mapping[str, Any],
    *,
    generator_model: str,
) -> dict[str, Any]:
    return {
        "benchmark_style": getattr(work_item, "benchmark_style"),
        "task_type": getattr(work_item, "task_type"),
        "dataset_key": getattr(work_item, "dataset_key"),
        "dataset_name": getattr(work_item, "dataset_name"),
        "combo": dict(combo),
        "generator_model": generator_model,
        "generator_rows": [],
    }


def collect_benchmark_summary_rows(
    summary_contexts: Mapping[tuple[str, str], Mapping[str, Any]],
    *,
    evaluator_models: Mapping[str, str],
    requested_samples: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary_context in summary_contexts.values():
        rows.append(
            build_benchmark_summary_row(
                benchmark_style=str(summary_context["benchmark_style"]),
                task_type=str(summary_context["task_type"]),
                dataset_key=str(summary_context["dataset_key"]),
                dataset_name=str(summary_context["dataset_name"]),
                combo=summary_context["combo"],
                generator_model=str(summary_context["generator_model"]),
                evaluator_models=evaluator_models,
                generator_rows=summary_context["generator_rows"],
                requested_samples=requested_samples,
            )
        )
    return rows


def _mean_or_zero(values: Iterable[Any]) -> float:
    normalized = [float(value or 0.0) for value in values]
    return statistics.mean(normalized) if normalized else 0.0
