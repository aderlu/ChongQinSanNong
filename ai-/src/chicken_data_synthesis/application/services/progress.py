from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Sequence


def summarize_results(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    success_count = sum(1 for item in results if item.get("success"))
    arbitration_count = sum(1 for item in results if item.get("needed_arbitration"))
    fatal_risk_count = 0
    score_sum = 0.0
    generation_sum = 0.0
    judge_sum = 0.0

    for item in results:
        judge_a = _as_mapping(item.get("judge_a_result"))
        judge_b = _as_mapping(item.get("judge_b_result"))
        final_metrics = _as_mapping(item.get("final_metrics"))
        rule_base = _as_mapping(item.get("rule_base_result"))
        if final_metrics.get("fatal_risk") or rule_base.get("fatal_risk") or judge_a.get("fatal_risk") or judge_b.get("fatal_risk"):
            fatal_risk_count += 1
        if item.get("success"):
            score_sum += float(final_metrics.get("final_total_score", 0) or 0)
        generation_sum += float(item.get("generation_seconds", 0) or 0)
        judge_sum += (
            float(item.get("judge_a_seconds", 0) or 0)
            + float(item.get("judge_b_seconds", 0) or 0)
            + float(item.get("arbiter_seconds", 0) or 0)
        )

    total = len(results) or 1
    generation_values = [_to_float(item.get("generation_seconds")) for item in results]
    judge_a_values = [_to_float(item.get("judge_a_seconds")) for item in results]
    judge_b_values = [_to_float(item.get("judge_b_seconds")) for item in results]
    arbiter_values = [_to_float(item.get("arbiter_seconds")) for item in results]
    review_values = [
        judge_a_values[index] + judge_b_values[index] + arbiter_values[index]
        for index in range(len(results))
    ]
    end_to_end_values = [
        generation_values[index] + review_values[index]
        for index in range(len(results))
    ]

    return {
        "total": len(results),
        "success_count": success_count,
        "failure_count": len(results) - success_count,
        "arbitration_count": arbitration_count,
        "fatal_risk_count": fatal_risk_count,
        "avg_final_score": round(score_sum / success_count, 2) if success_count else 0,
        "avg_generation_seconds": round(generation_sum / total, 2),
        "avg_judge_seconds": round(judge_sum / total, 2),
        "timing": {
            "generation": _summarize_seconds(generation_values),
            "judge_a": _summarize_seconds(judge_a_values),
            "judge_b": _summarize_seconds(judge_b_values),
            "arbiter": _summarize_seconds(arbiter_values),
            "review_total": _summarize_seconds(review_values),
            "case_end_to_end": _summarize_seconds(end_to_end_values),
            "total_model_work_seconds": round(sum(end_to_end_values), 2),
        },
    }


def build_stage_summary_context(
    target_total: int,
    stage_results: Sequence[Mapping[str, Any]],
    all_results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "target_total": int(target_total),
        "stage_summary": summarize_results(stage_results),
        "total_summary": summarize_results(all_results),
    }


def build_stage_summary_lines_from_context(summary_context: Mapping[str, Any]) -> list[str]:
    stage_summary = _as_mapping(summary_context.get("stage_summary"))
    total_summary = _as_mapping(summary_context.get("total_summary"))
    target_total = int(summary_context.get("target_total", 0) or 0)
    return [
        f"\n[阶段完成] 已达到 {target_total} 条",
        (
            f"  本阶段: 成功 {stage_summary.get('success_count', 0)} | "
            f"失败 {stage_summary.get('failure_count', 0)} | "
            f"均分 {stage_summary.get('avg_final_score', 0)} | "
            f"仲裁 {stage_summary.get('arbitration_count', 0)}"
        ),
        (
            f"  累计: 成功 {total_summary.get('success_count', 0)} | "
            f"失败 {total_summary.get('failure_count', 0)} | "
            f"均分 {total_summary.get('avg_final_score', 0)} | "
            f"仲裁 {total_summary.get('arbitration_count', 0)} | "
            f"致命风险 {total_summary.get('fatal_risk_count', 0)}"
        ),
    ]


def build_completion_summary_context(
    mode: str,
    summary: Mapping[str, Any],
    elapsed_total_seconds: float,
    result_csv: str,
    summary_csv: str | None,
    sample_count: int,
    parallel_count: int | None = None,
) -> dict[str, Any]:
    normalized_summary = dict(summary)
    timing = _as_mapping(normalized_summary.get("timing"))
    total_model_work_seconds = _to_float(timing.get("total_model_work_seconds"))
    if elapsed_total_seconds > 0 and total_model_work_seconds > 0:
        timing = dict(timing)
        timing["wall_clock_seconds"] = round(float(elapsed_total_seconds), 2)
        timing["parallel_work_ratio"] = round(total_model_work_seconds / float(elapsed_total_seconds), 2)
        if parallel_count:
            timing["parallel_efficiency"] = round(
                total_model_work_seconds / (float(elapsed_total_seconds) * int(parallel_count)),
                2,
            )
        normalized_summary["timing"] = timing
    return {
        "mode": str(mode),
        "summary": normalized_summary,
        "elapsed_total_seconds": float(elapsed_total_seconds),
        "result_csv": result_csv,
        "summary_csv": summary_csv,
        "sample_count": int(sample_count),
    }


def build_stage_summary_lines(
    target_total: int,
    stage_results: Sequence[Mapping[str, Any]],
    all_results: Sequence[Mapping[str, Any]],
) -> list[str]:
    return build_stage_summary_lines_from_context(
        build_stage_summary_context(target_total, stage_results, all_results)
    )


def build_batch_progress_message(
    processed_in_stage: int,
    batch_size: int,
    all_results: Sequence[Mapping[str, Any]],
    started_at: datetime,
    sample_count: int,
) -> str:
    elapsed = (datetime.now() - started_at).total_seconds()
    global_completed = len(all_results)
    success_count = sum(1 for item in all_results if item.get("success"))
    avg_seconds = elapsed / global_completed if global_completed else 0
    remaining = max(sample_count - global_completed, 0)
    eta_seconds = int(avg_seconds * remaining) if avg_seconds else 0
    return (
        f"      [批次 {processed_in_stage}/{batch_size}] 累计成功:{success_count} | "
        f"累计失败:{global_completed - success_count} | 已用:{int(elapsed)}s | 预计剩余:{eta_seconds}s"
    )


def build_failure_log_message(result: Mapping[str, Any]) -> str:
    return (
        f"      [失败] index={result.get('index', '')} | "
        f"disease={result.get('disease_name', '')} | "
        f"error={result.get('error', '')}"
    )


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _to_float(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _percentile(sorted_values: Sequence[float], percentile: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction


def _summarize_seconds(values: Sequence[float]) -> dict[str, float]:
    normalized = [float(value or 0) for value in values]
    nonzero = [value for value in normalized if value > 0]
    ordered = sorted(nonzero or normalized)
    count = len(nonzero)
    if not ordered:
        return {
            "count": 0,
            "total": 0.0,
            "avg": 0.0,
            "min": 0.0,
            "p50": 0.0,
            "p95": 0.0,
            "max": 0.0,
        }
    total_seconds = sum(normalized)
    denominator = count if count else len(normalized)
    return {
        "count": count,
        "total": round(total_seconds, 2),
        "avg": round(total_seconds / denominator, 2) if denominator else 0.0,
        "min": round(min(ordered), 2),
        "p50": round(_percentile(ordered, 0.50), 2),
        "p95": round(_percentile(ordered, 0.95), 2),
        "max": round(max(ordered), 2),
    }


__all__ = [
    "build_completion_summary_context",
    "build_batch_progress_message",
    "build_failure_log_message",
    "build_stage_summary_context",
    "build_stage_summary_lines",
    "build_stage_summary_lines_from_context",
    "summarize_results",
]
