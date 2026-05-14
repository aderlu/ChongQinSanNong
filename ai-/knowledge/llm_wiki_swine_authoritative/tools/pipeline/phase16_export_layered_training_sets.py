from __future__ import annotations

import argparse
import csv
import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TZ = timezone(timedelta(hours=8))

LAYER_TO_FILE = {
    "L1_retrieval_grounded": "sft_l1_retrieval_grounded.jsonl",
    "L2_diagnosis_support": "sft_l2_diagnosis_support.jsonl",
    "L3_differential_support": "sft_l3_differential_support.jsonl",
    "L4_control_boundary": "sft_l4_control_boundary.jsonl",
    "L5_drug_boundary_negative": "sft_l5_drug_boundary_negative.jsonl",
    "L6_regulatory_guardrail": "eval_l6_regulatory_guardrail.jsonl",
    "L7_judge_calibration": "eval_l7_judge_calibration.jsonl",
    "L1_L4_high_value": "sft_l1_l4_high_value.jsonl",
    "L1_L4_borderline": "sft_l1_l4_borderline.jsonl",
    "boundary_refusal_train": "sft_boundary_refusal_train.jsonl",
    "format_repair_queue": "training_set_format_repair_queue.jsonl",
}
QUEUE_TO_FILE = {
    "review_queue": "training_set_review_queue.jsonl",
    "rejected_queue": "training_set_rejected_queue.jsonl",
}
POSITIVE_SFT_LAYERS = {
    "L1_retrieval_grounded",
    "L2_diagnosis_support",
    "L3_differential_support",
    "L4_control_boundary",
}
PHASE18_SEARCH_GLOBS = (
    "semantic_reviewed_samples/*.jsonl",
    "semantic_evaluated_samples/*.jsonl",
    "reviewed_samples/*semantic*.jsonl",
    "reviewed_samples/*phase18*.jsonl",
    "**/*semantic*review*.jsonl",
    "**/*phase18*.jsonl",
)
PHASE18_DECISION_ALIASES = (
    "accepted",
    "review",
    "rejected",
)
PRODUCTION_CSV_FIELDS = [
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
    "sample_id",
    "plan_id",
    "ability_layer",
    "entity_id",
    "entity_type",
    "risk_class",
    "expected_output_type",
    "export_bucket",
    "export_decision",
    "phase15_final_decision",
    "phase18_semantic_decision",
    "phase18_judge_status",
    "phase18_judge_a_status",
    "phase18_judge_b_status",
    "phase18_arbiter_status",
    "training_intent",
    "evidence_depth_class",
    "page_gold_ready",
    "evidence_units",
    "source_trust",
    "evidence_coverage",
    "evidence_anchor_count",
    "style_clinical_conversation_score",
    "style_dict_like_detected",
    "style_english_template_label_detected",
    "style_naturalized",
]
TRAINING_MAIN_CSV_FIELDS = [
    "sample_id",
    "plan_id",
    "ability_layer",
    "entity_id",
    "entity_type",
    "risk_class",
    "expected_output_type",
    "user_query",
    "assistant_answer",
    "source_trust",
    "evidence_coverage",
    "evidence_anchor_count",
    "training_intent",
    "evidence_depth_class",
    "page_gold_ready",
    "evidence_units",
    "phase15_final_decision",
    "phase18_semantic_decision",
    "phase18_judge_status",
    "phase18_judge_a_status",
    "phase18_judge_b_status",
    "phase18_arbiter_status",
    "export_bucket",
    "export_decision",
    "final_label",
    "final_total_score",
    "final_weighted_total_score",
    "final_fatal_risk",
    "final_structured_pass",
    "judge_a_total_score",
    "judge_a_weighted_total_score",
    "judge_a_final_label",
    "judge_a_fatal_risk",
    "judge_a_structured_pass",
    "judge_a_evidence_fidelity",
    "judge_a_clinical_reasoning",
    "judge_a_safety_boundary",
    "judge_a_question_resolution",
    "judge_a_training_utility",
    "judge_b_total_score",
    "judge_b_weighted_total_score",
    "judge_b_final_label",
    "judge_b_fatal_risk",
    "judge_b_structured_pass",
    "judge_b_risk_control",
    "judge_b_unsupported_expansion_control",
    "judge_b_answer_completeness",
    "judge_b_citation_integrity",
    "judge_b_language_naturalness",
    "needed_arbitration",
    "arbiter_final_total_score",
    "arbiter_weighted_total_score",
    "arbiter_final_label",
    "arbiter_fatal_risk",
    "arbiter_structured_pass",
    "arbiter_consensus_reliability",
    "arbiter_safety_override",
    "arbiter_evidence_sufficiency",
    "arbiter_training_value",
    "arbiter_calibration_consistency",
    "style_clinical_conversation_score",
    "style_dict_like_detected",
    "style_english_template_label_detected",
    "style_naturalized",
    "metadata",
]


def today() -> str:
    return datetime.now(TZ).strftime("%Y%m%d")


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def latest_jsonl(directory: Path, prefix: str) -> Path:
    files = sorted(directory.glob(f"{prefix}_*.jsonl"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {directory}")
    return files[0]


def resolve_path(value: str, root: Path, default_dir: Path, prefix: str) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    return latest_jsonl(default_dir, prefix)


def resolve_optional_path(value: str, root: Path, search_root: Path, globs: tuple[str, ...]) -> Path | None:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    matches: list[Path] = []
    for pattern in globs:
        matches.extend(search_root.glob(pattern))
    files = sorted({path.resolve() for path in matches if path.is_file()}, key=lambda path: path.stat().st_mtime, reverse=True)
    return files[0] if files else None


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("sample_id")): row for row in rows if row.get("sample_id")}


def phase15_passed(row: dict[str, Any]) -> bool:
    return (
        row.get("final_decision") == "accepted"
        and bool((row.get("fact_level_check") or {}).get("passed"))
        and bool((row.get("hard_gate_check") or {}).get("passed"))
    )


def get_nested(row: dict[str, Any], *path: str) -> Any:
    current: Any = row
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def first_present(row: dict[str, Any], paths: tuple[tuple[str, ...], ...]) -> Any:
    for path in paths:
        value = get_nested(row, *path)
        if value is not None and value != "":
            return value
    return None


def normalize_decision(value: Any) -> str:
    raw = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if raw in {"accepted", "pass", "passed", "allow", "allowed", "approved", "approve"}:
        return "accepted"
    if raw in {"review", "needs_review", "manual_review", "candidate", "uncertain", "escalate", "escalated"}:
        return "review"
    if raw in {"rejected", "reject", "failed", "fail", "blocked", "deny", "denied"}:
        return "rejected"
    return raw


def normalize_status(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    lowered = raw.lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "pass": "passed",
        "ok": "passed",
        "approve": "accepted",
        "approved": "accepted",
        "manual_review": "review",
        "needs_review": "review",
        "fail": "failed",
        "reject": "rejected",
    }
    return aliases.get(lowered, lowered)


def collect_reason_lists(row: dict[str, Any], paths: tuple[tuple[str, ...], ...]) -> list[str]:
    reasons: list[str] = []
    seen: set[str] = set()
    for path in paths:
        value = get_nested(row, *path)
        items: list[Any]
        if isinstance(value, list):
            items = value
        elif value in (None, ""):
            items = []
        else:
            items = [value]
        for item in items:
            reason = str(item).strip()
            if reason and reason not in seen:
                seen.add(reason)
                reasons.append(reason)
    return reasons


def extract_phase18_fields(row: dict[str, Any], *, allow_final_decision_fallback: bool) -> dict[str, Any]:
    decision_paths: list[tuple[str, ...]] = [
        ("semantic_decision",),
        ("semantic_final_decision",),
        ("phase18_semantic_decision",),
        ("final_semantic_decision",),
        ("semantic_final_metrics", "semantic_final_decision"),
        ("semantic_review", "decision"),
        ("semantic_gate", "decision"),
        ("phase18", "semantic_decision"),
        ("phase18", "decision"),
    ]
    if allow_final_decision_fallback:
        decision_paths.extend((("final_decision",), ("decision",)))
    semantic_decision = normalize_decision(first_present(row, tuple(decision_paths)))
    judge_status = normalize_status(
        first_present(
            row,
            (
                ("judge_status",),
                ("double_judge_status",),
                ("judge_consensus",),
                ("semantic_final_metrics", "final_label"),
                ("phase18", "judge_status"),
                ("phase18", "double_judge_status"),
            ),
        )
    )
    judge_a_status = normalize_status(
        first_present(
            row,
            (
                ("judge_a_status",),
                ("judge_1_status",),
                ("judge1_status",),
                ("judge_a", "status"),
                ("judge_1", "status"),
                ("judge_a_result", "final_label"),
                ("phase18", "judge_a_status"),
            ),
        )
    )
    judge_b_status = normalize_status(
        first_present(
            row,
            (
                ("judge_b_status",),
                ("judge_2_status",),
                ("judge2_status",),
                ("judge_b", "status"),
                ("judge_2", "status"),
                ("judge_b_result", "final_label"),
                ("phase18", "judge_b_status"),
            ),
        )
    )
    arbiter_status = normalize_status(
        first_present(
            row,
            (
                ("arbiter_status",),
                ("arbiter_decision",),
                ("arbitration_status",),
                ("arbiter_result", "arbiter_final_label"),
                ("arbiter_result", "final_label"),
                ("phase18", "arbiter_status"),
                ("phase18", "arbiter_decision"),
            ),
        )
    )
    reject_reasons = collect_reason_lists(
        row,
        (
            ("semantic_reject_reasons",),
            ("semantic_rejected_reasons",),
            ("phase18_reject_reasons",),
            ("phase18", "reject_reasons"),
            ("reject_reasons",),
        ),
    )
    review_reasons = collect_reason_lists(
        row,
        (
            ("semantic_review_reasons",),
            ("phase18_review_reasons",),
            ("review_reasons",),
            ("phase18", "review_reasons"),
        ),
    )
    return {
        "semantic_decision": semantic_decision,
        "judge_status": judge_status,
        "judge_a_status": judge_a_status,
        "judge_b_status": judge_b_status,
        "arbiter_status": arbiter_status,
        "reject_reasons": reject_reasons,
        "review_reasons": review_reasons,
    }


def has_phase18_signal(row: dict[str, Any], *, allow_final_decision_fallback: bool) -> bool:
    phase18 = extract_phase18_fields(row, allow_final_decision_fallback=allow_final_decision_fallback)
    return any(
        phase18[key]
        for key in (
            "semantic_decision",
            "judge_status",
            "judge_a_status",
            "judge_b_status",
            "arbiter_status",
            "reject_reasons",
            "review_reasons",
        )
    )


def load_phase18_lookup(phase18_path: Path | None, evaluated: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], Path | None]:
    if phase18_path:
        rows = read_jsonl(phase18_path)
        if not rows:
            raise RuntimeError(
                f"Phase18 file is empty or unreadable: {phase18_path}. "
                "Re-run Phase18 after Phase15 has completed and produced a non-empty semantic result."
            )
        return by_id(rows), phase18_path
    inline_rows = [row for row in evaluated if has_phase18_signal(row, allow_final_decision_fallback=False)]
    if inline_rows:
        return by_id(inline_rows), None
    raise FileNotFoundError(
        "Phase18 semantic review results are required. Provide --phase18 or enrich evaluated samples with Phase18 fields."
    )


def merge_reasons(*reason_lists: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for reasons in reason_lists:
        for item in reasons:
            reason = str(item).strip()
            if reason and reason not in seen:
                seen.add(reason)
                merged.append(reason)
    return merged


def bool_text(value: Any) -> str:
    return "True" if bool(value) else "False"


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def phase18_summary(semantic_row: dict[str, Any] | None) -> dict[str, Any]:
    if semantic_row is None:
        return {
            "semantic_decision": "missing",
            "judge_status": "",
            "judge_a_status": "",
            "judge_b_status": "",
            "arbiter_status": "",
            "reject_reasons": ["phase18:missing_result"],
            "review_reasons": ["phase18:missing_result"],
        }
    phase18 = extract_phase18_fields(semantic_row, allow_final_decision_fallback=True)
    decision = phase18["semantic_decision"]
    if decision not in PHASE18_DECISION_ALIASES:
        phase18["semantic_decision"] = "review"
        fallback_reason = f"phase18:unrecognized_semantic_decision:{decision or 'missing'}"
        phase18["review_reasons"] = merge_reasons(phase18["review_reasons"], [fallback_reason])
    if phase18["semantic_decision"] == "rejected" and not phase18["reject_reasons"]:
        phase18["reject_reasons"] = ["phase18:rejected_without_reason"]
    if phase18["semantic_decision"] == "review" and not phase18["review_reasons"]:
        phase18["review_reasons"] = ["phase18:review_without_reason"]
    return phase18


def flatten_anchor_source_ids(anchors: list[dict[str, Any]]) -> str:
    source_ids: list[str] = []
    seen: set[str] = set()
    for anchor in anchors:
        source_id = str(anchor.get("source_id") or "").strip()
        if source_id and source_id not in seen:
            seen.add(source_id)
            source_ids.append(source_id)
    return "|".join(source_ids)


def evidence_status_counts(anchors: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for anchor in anchors:
        key = "SUPPORTED" if anchor.get("claim_supported", True) else "UNSUPPORTED"
        counts[key] = counts.get(key, 0) + 1
    return counts


def extract_dimension_score(payload: dict[str, Any], *keys: str) -> Any:
    scores = payload.get("dimension_scores") if isinstance(payload.get("dimension_scores"), dict) else {}
    for key in keys:
        if key in scores:
            return scores.get(key, "")
    return ""


def production_metadata(
    generated: dict[str, Any],
    evaluated: dict[str, Any],
    semantic_row: dict[str, Any] | None,
    decision: dict[str, Any],
    *,
    export_bucket: str,
) -> dict[str, Any]:
    metadata = generated.get("metadata") if isinstance(generated.get("metadata"), dict) else {}
    phase18 = decision["phase18"]
    return {
        **metadata,
        "sample_id": generated.get("sample_id", ""),
        "plan_id": generated.get("plan_id", ""),
        "skeleton_id": generated.get("skeleton_id", ""),
        "ability_layer": generated.get("ability_layer") or evaluated.get("ability_layer", ""),
        "entity_id": generated.get("entity_id", ""),
        "entity_type": generated.get("entity_type", ""),
        "risk_class": generated.get("risk_class", ""),
        "expected_output_type": generated.get("expected_output_type", ""),
        "usage_scope": generated.get("usage_scope", []),
        "evidence_anchors": generated.get("evidence_anchors", []),
        "source_trust": generated.get("source_trust", ""),
        "evidence_coverage": generated.get("evidence_coverage", ""),
        "training_intent": generated.get("training_intent", ""),
        "evidence_depth_class": generated.get("evidence_depth_class", ""),
        "page_gold_ready": generated.get("page_gold_ready", ""),
        "evidence_units": generated.get("evidence_units", ""),
        "style_flags": generated.get("style_flags", {}),
        "style_rewrites": generated.get("style_rewrites", []),
        "phase15_final_decision": decision["phase15_final_decision"],
        "phase15_reject_reasons": decision["phase15_reject_reasons"],
        "phase18_semantic_decision": phase18["semantic_decision"],
        "phase18_judge_status": phase18["judge_status"],
        "phase18_judge_a_status": phase18["judge_a_status"],
        "phase18_judge_b_status": phase18["judge_b_status"],
        "phase18_arbiter_status": phase18["arbiter_status"],
        "phase18_reject_reasons": phase18["reject_reasons"],
        "phase18_review_reasons": phase18["review_reasons"],
        "export_bucket": export_bucket,
        "export_decision": decision["export_decision"],
        "semantic_row_present": bool(semantic_row),
    }


def build_production_csv_row(
    generated: dict[str, Any],
    evaluated: dict[str, Any],
    semantic_row: dict[str, Any] | None,
    decision: dict[str, Any],
    *,
    index: int,
    export_bucket: str,
    wiki_root: Path,
) -> dict[str, Any]:
    stage_1 = generated.get("stage_1_draft") if isinstance(generated.get("stage_1_draft"), dict) else {}
    stage_2 = generated.get("stage_2_grounded") if isinstance(generated.get("stage_2_grounded"), dict) else {}
    anchors = [anchor for anchor in generated.get("evidence_anchors", []) if isinstance(anchor, dict)]
    judge_a = semantic_row.get("judge_a_result") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("judge_a_result"), dict) else {}
    judge_b = semantic_row.get("judge_b_result") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("judge_b_result"), dict) else {}
    arbiter = semantic_row.get("arbiter_result") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("arbiter_result"), dict) else {}
    metrics = semantic_row.get("semantic_final_metrics") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("semantic_final_metrics"), dict) else {}
    style_flags = generated.get("style_flags") if isinstance(generated.get("style_flags"), dict) else {}
    phase18 = decision["phase18"]
    entity_id = str(generated.get("entity_id") or "")
    disease_name = entity_id if entity_id else str(generated.get("sample_id") or "")
    metadata = production_metadata(generated, evaluated, semantic_row, decision, export_bucket=export_bucket)
    answer_text = str(stage_2.get("answer") or "").replace("\r", " ").replace("\n", " / ")
    draft_text = str(stage_1.get("answer") or "").replace("\r", " ").replace("\n", " / ")
    source_ids = flatten_anchor_source_ids(anchors)
    status_counts = evidence_status_counts(anchors)
    final_total_score = metrics.get("final_total_score", metrics.get("total_score", judge_a.get("total_score", "")))
    final_label = metrics.get("final_label") or phase18["semantic_decision"] or decision["export_decision"]
    question = str(generated.get("question") or "").replace("\r", " ").replace("\n", " / ")
    return {
        "case_id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"swine-wiki-{generated.get('sample_id', '')}")),
        "index": str(index),
        "disease_name": disease_name,
        "generator_key": str(generated.get("generation_mode") or "wiki_pipeline"),
        "generator_model": str(stage_2.get("generator") or generated.get("model") or ""),
        "success": "成功" if decision["export_decision"] == "accepted" else "待复核" if decision["export_decision"] == "review" else "拒绝",
        "error": "",
        "species": "猪",
        "user_query": question,
        "diagnosis": answer_text,
        "prescription": "",
        "withdrawal_period": "",
        "metadata": json_text(metadata),
        "rule_hard_block": bool_text(any(str(reason).startswith("hard_gate:") for reason in decision["phase15_reject_reasons"])),
        "rule_fatal_risk": bool_text(False),
        "rule_codes": "|".join(reason.replace("hard_gate:", "") for reason in decision["phase15_reject_reasons"] if str(reason).startswith("hard_gate:")),
        "rule_messages": "|".join(decision["export_reasons"]),
        "target_disease_in_diagnosis": bool_text(bool(answer_text)),
        "target_disease_mismatch": bool_text(False),
        "final_fatal_risk": bool_text(metrics.get("fatal_risk", False)),
        "wiki_dir": str(wiki_root),
        "wiki_fact_count": "",
        "wiki_page_count": "",
        "wiki_context_query": "\n".join(part for part in [question, draft_text, answer_text] if part),
        "wiki_evidence_status_counts": json_text(status_counts),
        "wiki_evidence_source_ids": source_ids,
        "wiki_context_chars": str(len(question) + len(draft_text) + len(answer_text)),
        "generation_seconds": "",
        "judge_a_model": judge_a.get("judge_model", judge_a.get("model", "")),
        "judge_a_total_score": judge_a.get("total_score", ""),
        "judge_a_diagnosis_accuracy": extract_dimension_score(judge_a, "clinical_correctness", "clinical_reasoning"),
        "judge_a_pathology_logic": extract_dimension_score(judge_a, "reasoning_consistency", "question_resolution"),
        "judge_a_prescription_safety": extract_dimension_score(judge_a, "safety_boundary_clarity", "safety_boundary"),
        "judge_a_data_quality": extract_dimension_score(judge_a, "training_usability", "training_utility"),
        "judge_a_fatal_risk": bool_text(judge_a.get("fatal_risk", False)),
        "judge_a_structured_pass": bool_text(judge_a.get("structured_pass", False)),
        "judge_a_summary": str(judge_a.get("summary", "")),
        "judge_b_model": judge_b.get("judge_model", judge_b.get("model", "")),
        "judge_b_total_score": judge_b.get("total_score", ""),
        "judge_b_diagnosis_accuracy": extract_dimension_score(judge_b, "answer_completeness"),
        "judge_b_pathology_logic": extract_dimension_score(judge_b, "dataset_fit", "citation_integrity"),
        "judge_b_prescription_safety": extract_dimension_score(judge_b, "safety_risk", "risk_control"),
        "judge_b_data_quality": extract_dimension_score(judge_b, "language_quality", "language_naturalness"),
        "judge_b_fatal_risk": bool_text(judge_b.get("fatal_risk", False)),
        "judge_b_structured_pass": bool_text(judge_b.get("structured_pass", False)),
        "judge_b_summary": str(judge_b.get("summary", "")),
        "needed_arbitration": "是" if bool(semantic_row and semantic_row.get("needed_arbitration")) else "否",
        "arbiter_model": arbiter.get("judge_model", arbiter.get("model", "")),
        "arbiter_agreed_with_judge": str(semantic_row.get("arbiter_agreed_with_judge", "")) if isinstance(semantic_row, dict) else "",
        "arbiter_final_label": arbiter.get("final_label", ""),
        "arbiter_reason": str(arbiter.get("reason", "")),
        "final_total_score": final_total_score,
        "final_diagnosis_accuracy": extract_dimension_score(judge_a, "clinical_correctness", "clinical_reasoning"),
        "final_pathology_logic": extract_dimension_score(judge_a, "reasoning_consistency", "question_resolution"),
        "final_prescription_safety": extract_dimension_score(judge_a, "safety_boundary_clarity", "safety_boundary"),
        "final_data_quality": extract_dimension_score(judge_a, "training_usability", "training_utility"),
        "final_label": final_label,
        "judge_a_seconds": "",
        "judge_b_seconds": "",
        "arbiter_seconds": "",
        "sample_id": generated.get("sample_id", ""),
        "plan_id": generated.get("plan_id", ""),
        "ability_layer": generated.get("ability_layer") or evaluated.get("ability_layer", ""),
        "entity_id": generated.get("entity_id", ""),
        "entity_type": generated.get("entity_type", ""),
        "risk_class": generated.get("risk_class", ""),
        "expected_output_type": generated.get("expected_output_type", ""),
        "export_bucket": export_bucket,
        "export_decision": decision["export_decision"],
        "phase15_final_decision": decision["phase15_final_decision"],
        "phase18_semantic_decision": phase18["semantic_decision"],
        "phase18_judge_status": phase18["judge_status"],
        "phase18_judge_a_status": phase18["judge_a_status"],
        "phase18_judge_b_status": phase18["judge_b_status"],
        "phase18_arbiter_status": phase18["arbiter_status"],
        "training_intent": generated.get("training_intent", ""),
        "evidence_depth_class": generated.get("evidence_depth_class", ""),
        "page_gold_ready": generated.get("page_gold_ready", ""),
        "evidence_units": generated.get("evidence_units", ""),
        "source_trust": generated.get("source_trust", ""),
        "evidence_coverage": generated.get("evidence_coverage", ""),
        "evidence_anchor_count": str(len(anchors)),
        "style_clinical_conversation_score": style_flags.get("clinical_conversation_score", ""),
        "style_dict_like_detected": bool_text(style_flags.get("dict_like_detected", False)),
        "style_english_template_label_detected": bool_text(style_flags.get("english_label_detected", False)),
        "style_naturalized": bool_text(style_flags.get("naturalized", False)),
    }


def build_training_main_csv_row(
    generated: dict[str, Any],
    evaluated: dict[str, Any],
    semantic_row: dict[str, Any] | None,
    decision: dict[str, Any],
    *,
    export_bucket: str,
) -> dict[str, Any]:
    stage_2 = generated.get("stage_2_grounded") if isinstance(generated.get("stage_2_grounded"), dict) else {}
    style_flags = generated.get("style_flags") if isinstance(generated.get("style_flags"), dict) else {}
    judge_a = semantic_row.get("judge_a_result") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("judge_a_result"), dict) else {}
    judge_b = semantic_row.get("judge_b_result") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("judge_b_result"), dict) else {}
    arbiter = semantic_row.get("arbiter_result") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("arbiter_result"), dict) else {}
    metrics = semantic_row.get("semantic_final_metrics") if isinstance(semantic_row, dict) and isinstance(semantic_row.get("semantic_final_metrics"), dict) else {}
    judge_a_scores = judge_a.get("dimension_scores") if isinstance(judge_a.get("dimension_scores"), dict) else {}
    judge_b_scores = judge_b.get("dimension_scores") if isinstance(judge_b.get("dimension_scores"), dict) else {}
    arbiter_scores = arbiter.get("dimension_scores") if isinstance(arbiter.get("dimension_scores"), dict) else {}
    metadata = production_metadata(generated, evaluated, semantic_row, decision, export_bucket=export_bucket)
    return {
        "sample_id": generated.get("sample_id", ""),
        "plan_id": generated.get("plan_id", ""),
        "ability_layer": generated.get("ability_layer") or evaluated.get("ability_layer", ""),
        "entity_id": generated.get("entity_id", ""),
        "entity_type": generated.get("entity_type", ""),
        "risk_class": generated.get("risk_class", ""),
        "expected_output_type": generated.get("expected_output_type", ""),
        "user_query": str(generated.get("question") or ""),
        "assistant_answer": str(stage_2.get("answer") or ""),
        "source_trust": generated.get("source_trust", ""),
        "evidence_coverage": generated.get("evidence_coverage", ""),
        "evidence_anchor_count": len(generated.get("evidence_anchors", []) if isinstance(generated.get("evidence_anchors"), list) else []),
        "training_intent": generated.get("training_intent", ""),
        "evidence_depth_class": generated.get("evidence_depth_class", ""),
        "page_gold_ready": generated.get("page_gold_ready", ""),
        "evidence_units": generated.get("evidence_units", ""),
        "phase15_final_decision": decision["phase15_final_decision"],
        "phase18_semantic_decision": decision["phase18"]["semantic_decision"],
        "phase18_judge_status": decision["phase18"]["judge_status"],
        "phase18_judge_a_status": decision["phase18"]["judge_a_status"],
        "phase18_judge_b_status": decision["phase18"]["judge_b_status"],
        "phase18_arbiter_status": decision["phase18"]["arbiter_status"],
        "export_bucket": export_bucket,
        "export_decision": decision["export_decision"],
        "final_label": metrics.get("final_label", ""),
        "final_total_score": metrics.get("final_total_score", ""),
        "final_weighted_total_score": arbiter.get("weighted_total_score", "") if arbiter else metrics.get("final_total_score", ""),
        "final_fatal_risk": metrics.get("fatal_risk", False),
        "final_structured_pass": metrics.get("structured_pass", False),
        "judge_a_total_score": judge_a.get("total_score", ""),
        "judge_a_weighted_total_score": judge_a.get("weighted_total_score", ""),
        "judge_a_final_label": judge_a.get("final_label", ""),
        "judge_a_fatal_risk": judge_a.get("fatal_risk", False),
        "judge_a_structured_pass": judge_a.get("structured_pass", False),
        "judge_a_evidence_fidelity": judge_a_scores.get("evidence_fidelity", ""),
        "judge_a_clinical_reasoning": judge_a_scores.get("clinical_reasoning", ""),
        "judge_a_safety_boundary": judge_a_scores.get("safety_boundary", ""),
        "judge_a_question_resolution": judge_a_scores.get("question_resolution", ""),
        "judge_a_training_utility": judge_a_scores.get("training_utility", ""),
        "judge_b_total_score": judge_b.get("total_score", ""),
        "judge_b_weighted_total_score": judge_b.get("weighted_total_score", ""),
        "judge_b_final_label": judge_b.get("final_label", ""),
        "judge_b_fatal_risk": judge_b.get("fatal_risk", False),
        "judge_b_structured_pass": judge_b.get("structured_pass", False),
        "judge_b_risk_control": judge_b_scores.get("risk_control", ""),
        "judge_b_unsupported_expansion_control": judge_b_scores.get("unsupported_expansion_control", ""),
        "judge_b_answer_completeness": judge_b_scores.get("answer_completeness", ""),
        "judge_b_citation_integrity": judge_b_scores.get("citation_integrity", ""),
        "judge_b_language_naturalness": judge_b_scores.get("language_naturalness", ""),
        "needed_arbitration": bool(semantic_row and semantic_row.get("needed_arbitration")),
        "arbiter_final_total_score": arbiter.get("final_total_score", ""),
        "arbiter_weighted_total_score": arbiter.get("weighted_total_score", ""),
        "arbiter_final_label": arbiter.get("final_label", ""),
        "arbiter_fatal_risk": arbiter.get("fatal_risk", False),
        "arbiter_structured_pass": arbiter.get("structured_pass", False),
        "arbiter_consensus_reliability": arbiter_scores.get("consensus_reliability", ""),
        "arbiter_safety_override": arbiter_scores.get("safety_override", ""),
        "arbiter_evidence_sufficiency": arbiter_scores.get("evidence_sufficiency", ""),
        "arbiter_training_value": arbiter_scores.get("training_value", ""),
        "arbiter_calibration_consistency": arbiter_scores.get("calibration_consistency", ""),
        "style_clinical_conversation_score": style_flags.get("clinical_conversation_score", ""),
        "style_dict_like_detected": style_flags.get("dict_like_detected", False),
        "style_english_template_label_detected": style_flags.get("english_label_detected", False),
        "style_naturalized": style_flags.get("naturalized", False),
        "metadata": json_text(metadata),
    }


def combined_decision(evaluated: dict[str, Any], semantic_row: dict[str, Any] | None) -> dict[str, Any]:
    phase15_accepted = phase15_passed(evaluated)
    phase18 = phase18_summary(semantic_row)
    phase15_reasons = [str(item) for item in evaluated.get("reject_reasons") or []]
    if not phase15_accepted:
        export_decision = "rejected"
        reasons = merge_reasons(phase15_reasons, phase18["reject_reasons"])
    elif phase18["semantic_decision"] == "accepted":
        export_decision = "accepted"
        reasons = []
    elif phase18["semantic_decision"] == "rejected":
        export_decision = "rejected"
        reasons = merge_reasons(phase18["reject_reasons"])
    else:
        export_decision = "review"
        reasons = merge_reasons(phase18["review_reasons"])
    return {
        "phase15_passed": phase15_accepted,
        "phase15_final_decision": str(evaluated.get("final_decision") or ""),
        "phase15_reject_reasons": phase15_reasons,
        "phase18": phase18,
        "export_decision": export_decision,
        "export_reasons": reasons,
    }


def expected_behavior(evaluated: dict[str, Any], generated: dict[str, Any]) -> str:
    if evaluated.get("expected_behavior"):
        return str(evaluated["expected_behavior"])
    reasons = ";".join(str(item) for item in evaluated.get("reject_reasons") or [])
    layer = str(generated.get("ability_layer") or evaluated.get("ability_layer") or "")
    if "hard_gate" in reasons or layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}:
        return "boundary_or_refusal_required"
    if phase15_passed(evaluated):
        return "source_grounded_answer"
    return "do_not_use_for_positive_sft"


def style_quality_from_rows(generated: dict[str, Any], evaluated: dict[str, Any]) -> dict[str, Any]:
    generated_flags = generated.get("style_flags") if isinstance(generated.get("style_flags"), dict) else {}
    hard_gate = evaluated.get("hard_gate_check") if isinstance(evaluated.get("hard_gate_check"), dict) else {}
    evaluated_flags = hard_gate.get("style_quality_check") if isinstance(hard_gate.get("style_quality_check"), dict) else {}
    return {
        "dict_like_detected": bool(
            generated_flags.get("dict_like_detected") or evaluated_flags.get("dict_like_detected")
        ),
        "english_template_label_detected": bool(
            generated_flags.get("english_label_detected") or evaluated_flags.get("english_template_label_detected")
        ),
        "clinical_conversation_score": evaluated_flags.get(
            "clinical_conversation_score",
            generated_flags.get("clinical_conversation_score", 0.0),
        ),
        "passed": bool(evaluated_flags.get("passed", True)),
        "violations": list(evaluated_flags.get("violations") or []),
    }


def route_bucket(layer: str, generated: dict[str, Any], evaluated: dict[str, Any], decision: dict[str, Any]) -> str | None:
    style_quality = style_quality_from_rows(generated, evaluated)
    training_intent = str(generated.get("training_intent") or "")
    evidence_depth_class = str(generated.get("evidence_depth_class") or "")
    export_decision = str(decision.get("export_decision") or "")

    if style_quality["dict_like_detected"] or style_quality["english_template_label_detected"]:
        return "format_repair_queue"
    if export_decision != "accepted":
        return None
    if layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}:
        return "boundary_refusal_train"
    if layer in POSITIVE_SFT_LAYERS:
        score = float(style_quality.get("clinical_conversation_score") or 0.0)
        if training_intent == "positive_sft" and evidence_depth_class == "substantive" and score >= 0.8:
            return "L1_L4_high_value"
        return "L1_L4_borderline"
    return None


def build_training_sample(
    generated: dict[str, Any],
    evaluated: dict[str, Any],
    decision: dict[str, Any],
    *,
    export_bucket: str,
    calibration: bool = False,
) -> dict[str, Any]:
    stage_2 = generated.get("stage_2_grounded") if isinstance(generated.get("stage_2_grounded"), dict) else {}
    phase18 = decision["phase18"]
    export_decision = decision["export_decision"]
    export_reasons = decision["export_reasons"]
    metadata = {
        "sample_id": generated.get("sample_id", ""),
        "entity_id": generated.get("entity_id", ""),
        "entity_type": generated.get("entity_type", ""),
        "risk_class": generated.get("risk_class", ""),
        "usage_scope": generated.get("usage_scope", []),
        "evidence_anchors": generated.get("evidence_anchors", []),
        "fact_eval_passed": bool((evaluated.get("fact_level_check") or {}).get("passed")),
        "hard_gate_passed": bool((evaluated.get("hard_gate_check") or {}).get("passed")),
        "source_trust": generated.get("source_trust", ""),
        "evidence_coverage": generated.get("evidence_coverage", ""),
        "training_intent": generated.get("training_intent", ""),
        "evidence_depth_class": generated.get("evidence_depth_class", ""),
        "page_gold_ready": generated.get("page_gold_ready", ""),
        "evidence_units": generated.get("evidence_units", ""),
        "style_flags": generated.get("style_flags", {}),
        "style_rewrites": generated.get("style_rewrites", []),
        "final_decision": evaluated.get("final_decision", ""),
        "expected_behavior": expected_behavior(evaluated, generated),
        "export_bucket": export_bucket,
        "export_decision": export_decision,
        "phase15": {
            "passed": decision["phase15_passed"],
            "final_decision": decision["phase15_final_decision"],
            "reject_reasons": decision["phase15_reject_reasons"],
        },
        "phase18": {
            "semantic_decision": phase18["semantic_decision"],
            "judge_status": phase18["judge_status"],
            "judge_a_status": phase18["judge_a_status"],
            "judge_b_status": phase18["judge_b_status"],
            "arbiter_status": phase18["arbiter_status"],
        },
    }
    if calibration or export_decision != "accepted":
        metadata["reject_reasons"] = merge_reasons(decision["phase15_reject_reasons"], phase18["reject_reasons"])
    if export_decision == "review":
        metadata["review_reasons"] = export_reasons
    elif export_reasons:
        metadata["reject_reasons"] = merge_reasons(metadata.get("reject_reasons", []), export_reasons)
    return {
        "sample_id": generated.get("sample_id", ""),
        "ability_layer": generated.get("ability_layer") or evaluated.get("ability_layer", ""),
        "messages": [
            {"role": "user", "content": str(generated.get("question") or "")},
            {"role": "assistant", "content": str(stage_2.get("answer") or "")},
        ],
        "metadata": metadata,
    }


def export_layers(
    evaluated: list[dict[str, Any]],
    generated: list[dict[str, Any]],
    semantic_by_id: dict[str, dict[str, Any]],
    out_dir: Path,
    wiki_root: Path,
) -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    gen_by_id = by_id(generated)
    buckets: dict[str, list[dict[str, Any]]] = {layer: [] for layer in LAYER_TO_FILE}
    queue_buckets: dict[str, list[dict[str, Any]]] = {name: [] for name in QUEUE_TO_FILE}
    routing_manifest_rows: list[dict[str, Any]] = []
    production_rows: list[dict[str, Any]] = []
    production_train_ready_rows: list[dict[str, Any]] = []
    for eval_row in evaluated:
        gen = gen_by_id.get(str(eval_row.get("sample_id") or ""))
        if not gen:
            continue
        decision = combined_decision(eval_row, semantic_by_id.get(str(eval_row.get("sample_id") or "")))
        layer = str(gen.get("ability_layer") or eval_row.get("ability_layer") or "L7_judge_calibration")
        routed_bucket = route_bucket(layer, gen, eval_row, decision)
        export_bucket = routed_bucket or layer
        production_row = build_production_csv_row(
            gen,
            eval_row,
            semantic_by_id.get(str(eval_row.get("sample_id") or "")),
            decision,
            index=len(production_rows) + 1,
            export_bucket=export_bucket,
            wiki_root=wiki_root,
        )
        production_rows.append(production_row)
        if decision["export_decision"] == "accepted":
            production_train_ready_rows.append(production_row)
        if layer in POSITIVE_SFT_LAYERS and decision["export_decision"] == "accepted":
            buckets[layer].append(build_training_sample(gen, eval_row, decision, export_bucket=layer))
        elif layer == "L5_drug_boundary_negative" and decision["export_decision"] == "accepted":
            buckets[layer].append(build_training_sample(gen, eval_row, decision, export_bucket=layer))
        elif layer == "L6_regulatory_guardrail":
            buckets[layer].append(build_training_sample(gen, eval_row, decision, export_bucket=layer))
        if routed_bucket:
            buckets[routed_bucket].append(build_training_sample(gen, eval_row, decision, export_bucket=routed_bucket))
        buckets["L7_judge_calibration"].append(
            build_training_sample(gen, eval_row, decision, export_bucket="L7_judge_calibration", calibration=True)
        )
        if decision["export_decision"] == "review":
            queue_buckets["review_queue"].append(
                build_training_sample(gen, eval_row, decision, export_bucket="review_queue", calibration=True)
            )
        elif decision["export_decision"] == "rejected":
            queue_buckets["rejected_queue"].append(
                build_training_sample(gen, eval_row, decision, export_bucket="rejected_queue", calibration=True)
            )
        routing_manifest_rows.append(
            {
                "sample_id": str(eval_row.get("sample_id") or ""),
                "ability_layer": layer,
                "phase15_final_decision": decision["phase15_final_decision"],
                "phase15_passed": decision["phase15_passed"],
                "phase18_semantic_decision": decision["phase18"]["semantic_decision"],
                "phase18_judge_status": decision["phase18"]["judge_status"],
                "phase18_judge_a_status": decision["phase18"]["judge_a_status"],
                "phase18_judge_b_status": decision["phase18"]["judge_b_status"],
                "phase18_arbiter_status": decision["phase18"]["arbiter_status"],
                "export_bucket": export_bucket,
                "export_decision": decision["export_decision"],
            }
        )
    for layer, filename in LAYER_TO_FILE.items():
        write_jsonl(out_dir / filename, buckets[layer])
    for queue_name, filename in QUEUE_TO_FILE.items():
        write_jsonl(out_dir / filename, queue_buckets[queue_name])
    training_main_rows = [
        build_training_main_csv_row(
            gen_by_id[str(row.get("sample_id") or "")],
            next(item for item in evaluated if str(item.get("sample_id") or "") == str(row.get("sample_id") or "")),
            semantic_by_id.get(str(row.get("sample_id") or "")),
            combined_decision(
                next(item for item in evaluated if str(item.get("sample_id") or "") == str(row.get("sample_id") or "")),
                semantic_by_id.get(str(row.get("sample_id") or "")),
            ),
            export_bucket=str(row.get("export_bucket") or row.get("export_decision") or ""),
        )
        for row in routing_manifest_rows
        if str(row.get("sample_id") or "") in gen_by_id
    ]
    training_main_train_ready_rows = [row for row in training_main_rows if str(row.get("export_decision") or "") == "accepted"]
    return buckets, queue_buckets, routing_manifest_rows, production_rows, production_train_ready_rows, training_main_rows, training_main_train_ready_rows


def manifest(
    buckets: dict[str, list[dict[str, Any]]],
    queue_buckets: dict[str, list[dict[str, Any]]],
    routing_manifest_rows: list[dict[str, Any]],
    evaluated: list[dict[str, Any]],
    evaluated_path: Path,
    generated_path: Path,
    phase18_path: Path | None,
    manifest_path: Path,
    root: Path,
    production_csv_path: Path,
    production_train_ready_csv_path: Path,
    training_main_csv_path: Path,
    training_main_train_ready_csv_path: Path,
) -> dict[str, Any]:
    phase15_decisions: dict[str, int] = {}
    export_decisions: dict[str, int] = {}
    semantic_decisions: dict[str, int] = {}
    judge_status_counts: dict[str, int] = {}
    judge_a_status_counts: dict[str, int] = {}
    judge_b_status_counts: dict[str, int] = {}
    arbiter_status_counts: dict[str, int] = {}
    for row in evaluated:
        decision = str(row.get("final_decision") or "")
        phase15_decisions[decision] = phase15_decisions.get(decision, 0) + 1
    for row in routing_manifest_rows:
        export_decision = row["export_decision"]
        semantic_decision = row["phase18_semantic_decision"]
        export_decisions[export_decision] = export_decisions.get(export_decision, 0) + 1
        semantic_decisions[semantic_decision] = semantic_decisions.get(semantic_decision, 0) + 1
        for key, counts in (
            ("phase18_judge_status", judge_status_counts),
            ("phase18_judge_a_status", judge_a_status_counts),
            ("phase18_judge_b_status", judge_b_status_counts),
            ("phase18_arbiter_status", arbiter_status_counts),
        ):
            status = str(row.get(key) or "")
            if status:
                counts[status] = counts.get(status, 0) + 1
    layer_counts = {layer: len(rows) for layer, rows in buckets.items()}
    queue_counts = {queue: len(rows) for queue, rows in queue_buckets.items()}
    file_layer_counts = {LAYER_TO_FILE[layer]: count for layer, count in layer_counts.items()}
    file_queue_counts = {QUEUE_TO_FILE[queue]: count for queue, count in queue_counts.items()}
    return {
        "generated_at": now(),
        "phase": "phase16_export_layered_training_sets",
        "input_samples": len(evaluated),
        "accepted": export_decisions.get("accepted", 0),
        "review": export_decisions.get("review", 0),
        "rejected": export_decisions.get("rejected", 0),
        "accept_reject_counts": {
            "accepted": export_decisions.get("accepted", 0),
            "rejected": export_decisions.get("rejected", 0),
        },
        "accept_review_reject_counts": {
            "accepted": export_decisions.get("accepted", 0),
            "review": export_decisions.get("review", 0),
            "rejected": export_decisions.get("rejected", 0),
        },
        "phase15_decision_counts": phase15_decisions,
        "phase18_semantic_decision_counts": semantic_decisions,
        "phase18_judge_status_counts": judge_status_counts,
        "phase18_judge_a_status_counts": judge_a_status_counts,
        "phase18_judge_b_status_counts": judge_b_status_counts,
        "phase18_arbiter_status_counts": arbiter_status_counts,
        "decision_counts": export_decisions,
        "layer_counts": {**layer_counts, **queue_counts, **file_layer_counts, **file_queue_counts},
        "files": {
            **{layer: f"exports/training_sets/{filename}" for layer, filename in LAYER_TO_FILE.items()},
            **{queue: f"exports/training_sets/{filename}" for queue, filename in QUEUE_TO_FILE.items()},
            "production_csv": rel(production_csv_path, root),
            "production_train_ready_csv": rel(production_train_ready_csv_path, root),
            "training_main_csv": rel(training_main_csv_path, root),
            "training_main_train_ready_csv": rel(training_main_train_ready_csv_path, root),
        },
        "input_files": {
            "evaluated": rel(evaluated_path, root),
            "generated": rel(generated_path, root),
            "phase18": rel(phase18_path, root) if phase18_path else "inline:evaluated_samples",
        },
        "input_file_hashes": {
            "evaluated_sha256": sha256(evaluated_path),
            "generated_sha256": sha256(generated_path),
            "phase18_sha256": sha256(phase18_path) if phase18_path else "inline:evaluated_samples",
        },
        "phase18": {
            "source_mode": "external_file" if phase18_path else "inline_evaluated_samples",
            "semantic_decision_counts": semantic_decisions,
            "judge_status_counts": judge_status_counts,
            "judge_a_status_counts": judge_a_status_counts,
            "judge_b_status_counts": judge_b_status_counts,
            "arbiter_status_counts": arbiter_status_counts,
        },
        "empty_layer_reasons": {
            layer: "No eligible Phase15+Phase18 accepted or calibration samples for this layer in current input batch."
            for layer, count in {**layer_counts, **queue_counts}.items()
            if count == 0
        },
        "manifest": rel(manifest_path, root),
        "passed": True,
    }


def write_report(summary: dict[str, Any], report_json: Path, report_md: Path) -> None:
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Phase 16 Layered Training Export",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Input samples: {summary['input_samples']}",
        f"- Accepted: {summary['accepted']}",
        f"- Review: {summary['review']}",
        f"- Rejected: {summary['rejected']}",
        "",
        "## Layer Counts",
        "",
    ]
    for layer, count in sorted(summary["layer_counts"].items()):
        lines.append(f"- {layer}: {count}")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default=today())
    parser.add_argument("--evaluated", default="")
    parser.add_argument("--generated", default="")
    parser.add_argument("--phase18", default="")
    args = parser.parse_args()
    root = args.wiki_root.resolve()
    exports = root / "exports"
    issues = root / "issues" / "wiki_first_generation_reports"
    evaluated_path = resolve_path(args.evaluated, root, exports / "evaluated_samples", "fact_evaluated_samples")
    generated_path = resolve_path(args.generated, root, exports / "generated_samples", "two_stage_samples")
    evaluated = read_jsonl(evaluated_path)
    generated = read_jsonl(generated_path)
    phase18_path = resolve_optional_path(args.phase18, root, exports, PHASE18_SEARCH_GLOBS)
    semantic_by_id, resolved_phase18_path = load_phase18_lookup(phase18_path, evaluated)
    out_dir = exports / "training_sets"
    buckets, queue_buckets, routing_manifest_rows, production_rows, production_train_ready_rows, training_main_rows, training_main_train_ready_rows = export_layers(
        evaluated,
        generated,
        semantic_by_id,
        out_dir,
        root,
    )
    production_csv_path = out_dir / f"swine_wiki_training_dataset_production_{args.date}.csv"
    production_train_ready_csv_path = out_dir / f"swine_wiki_training_dataset_production_train_ready_{args.date}.csv"
    training_main_csv_path = out_dir / f"swine_wiki_training_main_{args.date}.csv"
    training_main_train_ready_csv_path = out_dir / f"swine_wiki_training_main_train_ready_{args.date}.csv"
    write_csv(production_csv_path, production_rows, PRODUCTION_CSV_FIELDS)
    write_csv(production_train_ready_csv_path, production_train_ready_rows, PRODUCTION_CSV_FIELDS)
    write_csv(training_main_csv_path, training_main_rows, TRAINING_MAIN_CSV_FIELDS)
    write_csv(training_main_train_ready_csv_path, training_main_train_ready_rows, TRAINING_MAIN_CSV_FIELDS)
    manifest_path = out_dir / f"training_set_manifest_{args.date}.json"
    summary = manifest(
        buckets,
        queue_buckets,
        routing_manifest_rows,
        evaluated,
        evaluated_path,
        generated_path,
        resolved_phase18_path,
        manifest_path,
        root,
        production_csv_path,
        production_train_ready_csv_path,
        training_main_csv_path,
        training_main_train_ready_csv_path,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(summary, issues / f"phase16_training_export_{args.date}.json", issues / f"phase16_training_export_{args.date}.md")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
