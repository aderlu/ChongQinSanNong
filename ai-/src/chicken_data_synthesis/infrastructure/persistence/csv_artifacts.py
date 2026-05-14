from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from chicken_data_synthesis.infrastructure.knowledge import compact_wiki_audit_for_csv


FINAL_RESULT_FIELDS = (
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
    "answer_json",
    "evidence_anchors",
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
)

PILOT_SUMMARY_FIELDS = (
    "generator_key",
    "generator_model",
    "samples",
    "success_count",
    "success_rate",
    "avg_final_score",
    "structured_pass_rate",
    "fatal_risk_rate",
    "arbitration_rate",
    "avg_generation_seconds",
    "avg_total_judge_seconds",
)

COMPAT_FINAL_RESULT_FIELDS = FINAL_RESULT_FIELDS
COMPAT_PILOT_SUMMARY_FIELDS = PILOT_SUMMARY_FIELDS


def write_csv(
    output_file: str | Path,
    fieldnames: Sequence[str],
    rows: Iterable[Mapping[str, Any] | Sequence[Any]],
    *,
    encoding: str = "utf-8-sig",
    include_header: bool = True,
) -> Path:
    """Write rows to a CSV file using a stable field order."""
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding=encoding) as csvfile:
        writer = csv.writer(csvfile)
        if include_header:
            writer.writerow(fieldnames)
        for row in rows:
            writer.writerow(_coerce_row_values(row, fieldnames))

    return path


def append_csv_row(
    output_file: str | Path,
    fieldnames: Sequence[str],
    row: Mapping[str, Any] | Sequence[Any],
    *,
    encoding: str = "utf-8-sig",
    include_header: bool = True,
) -> Path:
    """Append a single CSV row and avoid duplicating a UTF-8 BOM."""
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = path.exists()
    file_has_content = file_exists and path.stat().st_size > 0
    append_encoding = _resolve_append_encoding(encoding, file_has_content)

    with path.open("a", newline="", encoding=append_encoding) as csvfile:
        writer = csv.writer(csvfile)
        if include_header and not file_has_content:
            writer.writerow(fieldnames)
        writer.writerow(_coerce_row_values(row, fieldnames))

    return path


def build_final_result_row(result: Mapping[str, Any]) -> dict[str, Any]:
    case_data = _as_mapping(result.get("case_data"))
    judge_a = _as_mapping(result.get("judge_a_result"))
    judge_b = _as_mapping(result.get("judge_b_result"))
    arbiter = _as_mapping(result.get("arbiter_result"))
    final_metrics = _as_mapping(result.get("final_metrics"))
    rule_base_result = _as_mapping(result.get("rule_base_result"))
    wiki_audit = compact_wiki_audit_for_csv(_as_mapping(rule_base_result.get("wiki_audit")))
    target_in_diagnosis = final_metrics.get("target_disease_in_diagnosis")
    if target_in_diagnosis in (None, ""):
        target = str(result.get("disease_name", "") or "")
        target_in_diagnosis = bool(target and target in str(case_data.get("diagnosis", "") or ""))
    target_mismatch = final_metrics.get("target_disease_mismatch")
    if target_mismatch in (None, ""):
        target_mismatch = bool(target_in_diagnosis is False)
    final_fatal = final_metrics.get("fatal_risk")
    if final_fatal in (None, ""):
        final_fatal = bool(rule_base_result.get("fatal_risk") or judge_a.get("fatal_risk") or judge_b.get("fatal_risk"))
    final_label = final_metrics.get("final_label", "")
    if final_label == "pass" and (final_fatal or target_mismatch):
        final_label = "review"

    return {
        "case_id": result.get("case_id", ""),
        "index": _display_index(result.get("index", 0)),
        "disease_name": result.get("disease_name", ""),
        "generator_key": result.get("generator_key", ""),
        "generator_model": result.get("generator_model", ""),
        "success": "成功" if result.get("success") else "失败",
        "error": result.get("error", ""),
        "species": case_data.get("species", ""),
        "user_query": case_data.get("user_query", ""),
        "diagnosis": case_data.get("diagnosis", ""),
        "prescription": case_data.get("prescription", ""),
        "withdrawal_period": case_data.get("withdrawal_period", ""),
        "answer_json": json.dumps(case_data.get("answer_json", {}), ensure_ascii=False),
        "evidence_anchors": json.dumps(case_data.get("evidence_anchors", []), ensure_ascii=False),
        "metadata": json.dumps(case_data.get("metadata", {}), ensure_ascii=False),
        "rule_hard_block": rule_base_result.get("hard_block", False),
        "rule_fatal_risk": rule_base_result.get("fatal_risk", False),
        "rule_codes": "|".join(rule_base_result.get("codes", []) or []),
        "rule_messages": " | ".join(rule_base_result.get("messages", []) or []),
        "target_disease_in_diagnosis": target_in_diagnosis,
        "target_disease_mismatch": target_mismatch,
        "final_fatal_risk": final_fatal,
        "wiki_dir": wiki_audit["wiki_dir"],
        "wiki_fact_count": wiki_audit["wiki_fact_count"],
        "wiki_page_count": wiki_audit["wiki_page_count"],
        "wiki_context_query": wiki_audit["wiki_context_query"],
        "wiki_evidence_status_counts": wiki_audit["wiki_evidence_status_counts"],
        "wiki_evidence_source_ids": wiki_audit["wiki_evidence_source_ids"],
        "wiki_context_chars": wiki_audit["wiki_context_chars"],
        "generation_seconds": result.get("generation_seconds", 0),
        "judge_a_model": judge_a.get("judge_model", ""),
        "judge_a_total_score": judge_a.get("total_score", ""),
        "judge_a_diagnosis_accuracy": judge_a.get("diagnosis_accuracy", ""),
        "judge_a_pathology_logic": judge_a.get("pathology_logic", ""),
        "judge_a_prescription_safety": judge_a.get("prescription_safety", ""),
        "judge_a_data_quality": judge_a.get("data_quality", ""),
        "judge_a_fatal_risk": judge_a.get("fatal_risk", ""),
        "judge_a_structured_pass": judge_a.get("structured_pass", ""),
        "judge_a_summary": judge_a.get("summary", ""),
        "judge_b_model": judge_b.get("judge_model", ""),
        "judge_b_total_score": judge_b.get("total_score", ""),
        "judge_b_diagnosis_accuracy": judge_b.get("diagnosis_accuracy", ""),
        "judge_b_pathology_logic": judge_b.get("pathology_logic", ""),
        "judge_b_prescription_safety": judge_b.get("prescription_safety", ""),
        "judge_b_data_quality": judge_b.get("data_quality", ""),
        "judge_b_fatal_risk": judge_b.get("fatal_risk", ""),
        "judge_b_structured_pass": judge_b.get("structured_pass", ""),
        "judge_b_summary": judge_b.get("summary", ""),
        "needed_arbitration": "是" if result.get("needed_arbitration") else "否",
        "arbiter_model": arbiter.get("arbiter_model", ""),
        "arbiter_agreed_with_judge": arbiter.get("agreed_with_judge", ""),
        "arbiter_final_label": arbiter.get("final_label", ""),
        "arbiter_reason": arbiter.get("reason", ""),
        "final_total_score": final_metrics.get("final_total_score", ""),
        "final_diagnosis_accuracy": final_metrics.get("final_diagnosis_accuracy", ""),
        "final_pathology_logic": final_metrics.get("final_pathology_logic", ""),
        "final_prescription_safety": final_metrics.get("final_prescription_safety", ""),
        "final_data_quality": final_metrics.get("final_data_quality", ""),
        "final_label": final_label,
        "judge_a_seconds": result.get("judge_a_seconds", 0),
        "judge_b_seconds": result.get("judge_b_seconds", 0),
        "arbiter_seconds": result.get("arbiter_seconds", 0),
    }


def write_final_results_csv(
    results: Iterable[Mapping[str, Any]],
    output_file: str | Path,
    *,
    encoding: str = "utf-8-sig",
    sort_by_index: bool = True,
) -> Path:
    ordered_results = list(results)
    if sort_by_index:
        ordered_results.sort(key=_result_sort_key)

    rows = [build_final_result_row(result) for result in ordered_results]
    return write_csv(output_file, FINAL_RESULT_FIELDS, rows, encoding=encoding)


def build_pilot_summary_rows(results: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    for result in results:
        generator_key = result.get("generator_key", "")
        if generator_key not in summary:
            summary[generator_key] = {
                "generator_model": result.get("generator_model", ""),
                "total": 0,
                "success": 0,
                "structured_pass": 0,
                "fatal_risk_count": 0,
                "arbitration_count": 0,
                "total_score_sum": 0.0,
                "generation_seconds_sum": 0.0,
                "judge_seconds_sum": 0.0,
            }

        item = summary[generator_key]
        item["total"] += 1
        item["generation_seconds_sum"] += _to_float(result.get("generation_seconds", 0.0))
        item["judge_seconds_sum"] += (
            _to_float(result.get("judge_a_seconds", 0.0))
            + _to_float(result.get("judge_b_seconds", 0.0))
            + _to_float(result.get("arbiter_seconds", 0.0))
        )

        if result.get("success"):
            item["success"] += 1
            final_metrics = _as_mapping(result.get("final_metrics"))
            judge_a = _as_mapping(result.get("judge_a_result"))
            judge_b = _as_mapping(result.get("judge_b_result"))
            item["total_score_sum"] += _to_float(final_metrics.get("final_total_score", 0))
            if judge_a.get("structured_pass") and judge_b.get("structured_pass"):
                item["structured_pass"] += 1
            if final_metrics.get("fatal_risk") or judge_a.get("fatal_risk") or judge_b.get("fatal_risk"):
                item["fatal_risk_count"] += 1
            if result.get("needed_arbitration"):
                item["arbitration_count"] += 1

    rows: list[dict[str, Any]] = []
    for generator_key, item in summary.items():
        total = item["total"] or 1
        success = item["success"]
        rows.append(
            {
                "generator_key": generator_key,
                "generator_model": item["generator_model"],
                "samples": item["total"],
                "success_count": success,
                "success_rate": round(success / total * 100, 2),
                "avg_final_score": round(item["total_score_sum"] / success, 2) if success else 0,
                "structured_pass_rate": round(item["structured_pass"] / success * 100, 2) if success else 0,
                "fatal_risk_rate": round(item["fatal_risk_count"] / success * 100, 2) if success else 0,
                "arbitration_rate": round(item["arbitration_count"] / success * 100, 2) if success else 0,
                "avg_generation_seconds": round(item["generation_seconds_sum"] / total, 2),
                "avg_total_judge_seconds": round(item["judge_seconds_sum"] / total, 2),
            }
        )

    return rows


def write_pilot_summary_csv(
    results: Iterable[Mapping[str, Any]],
    output_file: str | Path,
    *,
    encoding: str = "utf-8-sig",
) -> Path:
    rows = build_pilot_summary_rows(results)
    return write_csv(output_file, PILOT_SUMMARY_FIELDS, rows, encoding=encoding)


def write_pipeline_output_artifacts(
    results: Iterable[Mapping[str, Any]],
    result_csv: str | Path,
    *,
    summary_csv: str | Path | None = None,
    encoding: str = "utf-8-sig",
    sort_by_index: bool = True,
) -> dict[str, Path | None]:
    ordered_results = list(results)
    result_csv_path = write_final_results_csv(
        ordered_results,
        result_csv,
        encoding=encoding,
        sort_by_index=sort_by_index,
    )
    summary_csv_path = None
    if summary_csv:
        summary_csv_path = write_pilot_summary_csv(
            ordered_results,
            summary_csv,
            encoding=encoding,
        )
    return {
        "result_csv": result_csv_path,
        "summary_csv": summary_csv_path,
    }


save_final_results = write_final_results_csv
save_pilot_summary = write_pilot_summary_csv


def _coerce_row_values(
    row: Mapping[str, Any] | Sequence[Any],
    fieldnames: Sequence[str],
) -> list[Any]:
    if isinstance(row, Mapping):
        return [row.get(fieldname, "") for fieldname in fieldnames]
    if isinstance(row, Sequence) and not isinstance(row, (str, bytes, bytearray)):
        return list(row)
    raise TypeError("CSV rows must be mappings or non-string sequences.")


def _resolve_append_encoding(encoding: str, file_has_content: bool) -> str:
    if encoding.lower().replace("_", "-") == "utf-8-sig" and file_has_content:
        return "utf-8"
    return encoding


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _display_index(value: Any) -> int:
    try:
        return int(value) + 1
    except (TypeError, ValueError):
        return 1


def _result_sort_key(result: Mapping[str, Any]) -> int:
    try:
        return int(result.get("index", 0))
    except (TypeError, ValueError):
        return 0


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


__all__ = [
    "COMPAT_FINAL_RESULT_FIELDS",
    "COMPAT_PILOT_SUMMARY_FIELDS",
    "FINAL_RESULT_FIELDS",
    "PILOT_SUMMARY_FIELDS",
    "append_csv_row",
    "build_final_result_row",
    "build_pilot_summary_rows",
    "save_final_results",
    "save_pilot_summary",
    "write_csv",
    "write_final_results_csv",
    "write_pipeline_output_artifacts",
    "write_pilot_summary_csv",
]
