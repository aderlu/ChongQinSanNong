from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TZ = timezone(timedelta(hours=8))
HIGH_RISK_CLASSES = {"high_regulatory", "withdrawal_mrl_residue", "food_safety"}
HIGH_RISK_LAYERS = {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}
BLOCKED_COVERAGE = {"minimal", "unknown", ""}
REQUIRED_SAMPLE_FIELDS = {
    "sample_id",
    "plan_id",
    "skeleton_id",
    "question",
    "stage_2_grounded",
    "evidence_anchors",
    "ability_layer",
    "risk_class",
    "source_trust",
    "evidence_coverage",
}
REQUIRED_ANCHOR_FIELDS = {"fact_id", "source_id", "rule_card_id", "page_relpath"}
BOUNDARY_ANCHOR_REQUIRED_FIELDS = {"rule_card_id", "page_relpath"}
EXECUTIVE_TRIGGER_RE = re.compile(
    r"(?i)\b(dose|dosage|mg/kg|ml/kg|mrl|withdrawal|residue|regulatory|movement|report|cull|"
    r"quarantine|seal|disinfection|food safety|public health)\b|"
    r"(剂量|用量|疗程|给药|注射|拌料|饮水|休药|停药|残留|调运|上报|扑杀|封锁|检疫|"
    r"无害化|食品安全|公共卫生|人畜共患)"
)
DRUG_EXECUTABLE_RE = re.compile(
    r"(?i)\b(mg/kg|ml/kg|dose|dosage|withdrawal|mrl|route|course|inject|oral|feed|water)\b|"
    r"(剂量|用量|疗程|给药|注射|口服|拌料|饮水|休药|停药|残留|最大残留限量)"
)
BOUNDARY_REFUSAL_RE = re.compile(
    r"(?i)\b(must not|cannot|should not|boundary|label|official|A0|refuse|not provide|do not provide)\b|"
    r"(不得|不能|不应|边界|标签|说明书|官方|拒绝|不提供|不生成|不能直接)"
)


# Override the legacy mojibake patterns above with stable Unicode escapes.
EXECUTIVE_TRIGGER_RE = re.compile(
    r"(?i)\b(dose|dosage|mg/kg|ml/kg|mrl|withdrawal|residue|regulatory|movement|report|cull|"
    r"quarantine|seal|disinfection|food safety|public health)\b|"
    r"(\u5242\u91cf|\u7528\u91cf|\u7597\u7a0b|\u7ed9\u836f|\u6ce8\u5c04|\u62cc\u6599|\u996e\u6c34|"
    r"\u4f11\u836f|\u505c\u836f|\u6b8b\u7559|\u8c03\u8fd0|\u4e0a\u62a5|\u6251\u6740|\u5c01\u9501|"
    r"\u68c0\u75ab|\u65e0\u5bb3\u5316|\u98df\u54c1\u5b89\u5168|\u516c\u5171\u536b\u751f|\u4eba\u755c\u5171\u60a3)"
)
DRUG_EXECUTABLE_RE = re.compile(
    r"(?i)\b(mg/kg|ml/kg|dose|dosage|withdrawal|mrl|route|course|inject|oral|feed|water)\b|"
    r"(\u5242\u91cf|\u7528\u91cf|\u7597\u7a0b|\u7ed9\u836f|\u6ce8\u5c04|\u53e3\u670d|"
    r"\u62cc\u6599|\u996e\u6c34|\u4f11\u836f|\u505c\u836f|\u6b8b\u7559|\u6700\u5927\u6b8b\u7559\u9650\u91cf)"
)
BOUNDARY_REFUSAL_RE = re.compile(
    r"(?i)\b(must not|cannot|should not|boundary|label|official|A0|refuse|not provide|do not provide)\b|"
    r"(\u4e0d\u5f97|\u4e0d\u80fd|\u4e0d\u5e94|\u8fb9\u754c|\u6807\u7b7e|\u8bf4\u660e\u4e66|"
    r"\u5b98\u65b9|\u62d2\u7edd|\u4e0d\u63d0\u4f9b|\u4e0d\u751f\u6210|\u4e0d\u80fd\u76f4\u63a5)"
)
NEGATIVE_BOUNDARY_CUE_RE = re.compile(
    r"(?i)\b(do not|does not|cannot|not enough|not provide|not infer|not add|not authorize|without anchored|"
    r"unsupported|uncited|beyond the cited|boundary|only supports|insufficient|avoid)\b|"
    r"(\u4e0d\u5f97|\u4e0d\u80fd|\u4e0d\u5e94|\u4e0d\u53ef|\u672a\u63d0\u4f9b|\u4e0d\u63d0\u4f9b|"
    r"\u4e0d\u751f\u6210|\u4e0d\u76f4\u63a5|\u65e0\u6cd5\u636e\u6b64|\u4e0d\u8db3\u4ee5|\u4e0d\u5b9c|"
    r"\u4e0d\u63a8\u65ad|\u4e0d\u6dfb\u52a0|\u4e0d\u6269\u5c55|\u4e0d\u5f97\u57fa\u4e8e|"
    r"\u8fb9\u754c|\u4ec5\u652f\u6301|\u4e0d\u652f\u6301|\u672a\u7ecf\u5f15\u7528|\u672a\u7ecf\u8bc1\u5b9e|"
    r"\u8d85\u51fa|\u7f3a\u4e4f)"
)
LOW_RISK_EXECUTIVE_CONTEXT_LAYERS = {"L1_retrieval_grounded", "L2_diagnosis_support", "L3_differential_support", "L4_control_boundary"}
DICT_LIKE_OUTPUT_RE = re.compile(r'^\s*\{|\}\s*$|"\s*[^"]+\s*"\s*:\s*|^[A-Za-z][A-Za-z _-]{2,40}:\s', re.M)
ENGLISH_TEMPLATE_LABEL_RE = re.compile(
    r"(?i)\b(Evidence basis|Citation anchors|Diagnosis-support evidence|Differential-boundary evidence|"
    r"Differential boundary|Control-boundary evidence|Control boundary|Required boundary|Do not infer|"
    r"Do not over-diagnose|Do not prescribe beyond evidence|Cannot directly provide|Diagnostic boundary|"
    r"Answer boundary|Do not extend)\b"
)


def today() -> str:
    return datetime.now(TZ).strftime("%Y%m%d")


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
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


def latest_jsonl(directory: Path, prefix: str) -> Path:
    files = sorted(directory.glob(f"{prefix}_*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {directory}")
    return files[0]


def resolve_path(value: str, root: Path, default_dir: Path, prefix: str) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    return latest_jsonl(default_dir, prefix)


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def split_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").replace(",", ";").split(";") if item.strip()]


def load_fact_index(path: Path) -> dict[str, dict[str, Any]]:
    payload = read_json(path)
    if isinstance(payload, dict):
        rows = payload.get("facts") or payload.get("entries") or payload.get("items") or []
    else:
        rows = payload
    return {str(row.get("fact_id")): row for row in rows if isinstance(row, dict) and row.get("fact_id")}


def load_manifest_paths(path: Path) -> set[str]:
    payload = read_json(path)
    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    return {str(entry.get("path") or entry.get("page_relpath") or "") for entry in entries if isinstance(entry, dict)}


def has_a0_authority(sample: dict[str, Any], anchors: list[dict[str, Any]], facts: dict[str, dict[str, Any]]) -> bool:
    if str(sample.get("authority_level") or "").upper() == "A0":
        return True
    if str(sample.get("ability_layer") or "") == "L5_drug_boundary_negative":
        return any(str(anchor.get("rule_card_id") or "").startswith(("RC-DRUG", "RC-WITHDRAWAL")) for anchor in anchors)
    for anchor in anchors:
        source_id = str(anchor.get("source_id") or "")
        fact = facts.get(str(anchor.get("fact_id") or ""), {})
        if source_id.upper().startswith("A0") or str(fact.get("authority_level") or "").upper() == "A0":
            return True
    return False


def structure_check(sample: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(field for field in REQUIRED_SAMPLE_FIELDS if not sample.get(field))
    anchor_errors: list[str] = []
    anchors = sample.get("evidence_anchors")
    if not isinstance(anchors, list) or not anchors:
        anchor_errors.append("missing_evidence_anchors")
        anchors = []
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            anchor_errors.append(f"anchor_{index}_not_object")
            continue
        required = (
            BOUNDARY_ANCHOR_REQUIRED_FIELDS
            if anchor.get("anchor_type") == "rule_card_boundary"
            or str(sample.get("ability_layer") or "") in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}
            and not anchor.get("fact_id")
            else REQUIRED_ANCHOR_FIELDS
        )
        for field in sorted(required):
            if not anchor.get(field):
                anchor_errors.append(f"anchor_{index}_missing_{field}")
    answer = (sample.get("stage_2_grounded") or {}).get("answer") if isinstance(sample.get("stage_2_grounded"), dict) else ""
    if not str(answer or "").strip():
        missing.append("stage_2_grounded.answer")
    issues = missing + anchor_errors
    return {"passed": not issues, "missing_fields": missing, "anchor_errors": anchor_errors}


def fact_level_check(sample: dict[str, Any], facts: dict[str, dict[str, Any]], manifest_paths: set[str]) -> dict[str, Any]:
    unsupported_claims: list[str] = []
    wrong_fact_links: list[str] = []
    wrong_source_links: list[str] = []
    usage_scope_violations: list[str] = []
    coverage_violations: list[str] = []
    citation_violations: list[str] = []
    page_violations: list[str] = []
    anchors = [anchor for anchor in sample.get("evidence_anchors", []) if isinstance(anchor, dict)]
    answer = str((sample.get("stage_2_grounded") or {}).get("answer") or "")

    if str(sample.get("source_trust") or "") != "authoritative":
        wrong_source_links.append("sample_source_trust_not_authoritative")
    if str(sample.get("evidence_coverage") or "") in BLOCKED_COVERAGE:
        coverage_violations.append("sample_evidence_coverage_blocked")
    for marker in ("source=", "rule=", "fact="):
        if marker == "fact=" and str(sample.get("ability_layer") or "") in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}:
            continue
        if marker == "source=" and any(anchor.get("anchor_type") == "rule_card_boundary" for anchor in anchors):
            continue
        if marker not in answer:
            citation_violations.append(f"answer_missing_{marker.rstrip('=')}_citation")

    for index, anchor in enumerate(anchors):
        fact_id = str(anchor.get("fact_id") or "")
        source_id = str(anchor.get("source_id") or "")
        page_relpath = str(anchor.get("page_relpath") or "")
        if not anchor.get("claim_supported", True):
            unsupported_claims.append(f"anchor_{index}_claim_not_supported")
        fact = facts.get(fact_id)
        if not fact:
            if anchor.get("anchor_type") == "rule_card_boundary" and anchor.get("rule_card_id") and page_relpath in manifest_paths:
                continue
            wrong_fact_links.append(fact_id or f"anchor_{index}_missing_fact_id")
            continue
        if str(fact.get("source_trust") or "") != "authoritative":
            wrong_source_links.append(f"{fact_id}:fact_source_trust_not_authoritative")
        if str(fact.get("evidence_coverage") or "") in BLOCKED_COVERAGE:
            coverage_violations.append(f"{fact_id}:fact_evidence_coverage_blocked")
        expected_source_ids = set(split_list(fact.get("evidence_source_id") or fact.get("source_id")))
        if expected_source_ids and source_id not in expected_source_ids:
            wrong_source_links.append(f"{fact_id}:source_mismatch")
        fact_scopes = set(split_list(fact.get("usage_scope")))
        sample_scopes = set(split_list(sample.get("usage_scope")))
        if fact_scopes and sample_scopes and not fact_scopes.intersection(sample_scopes):
            usage_scope_violations.append(f"{fact_id}:usage_scope_mismatch")
        if manifest_paths and page_relpath not in manifest_paths:
            page_violations.append(f"{fact_id}:page_not_in_runtime_manifest")

    issues = (
        unsupported_claims
        + wrong_fact_links
        + wrong_source_links
        + usage_scope_violations
        + coverage_violations
        + citation_violations
        + page_violations
    )
    return {
        "passed": not issues,
        "unsupported_claims": unsupported_claims,
        "wrong_fact_links": wrong_fact_links,
        "wrong_source_links": wrong_source_links,
        "usage_scope_violations": usage_scope_violations,
        "coverage_violations": coverage_violations,
        "citation_violations": citation_violations,
        "page_violations": page_violations,
    }


def boundary_policy_check(sample: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    layer = str(sample.get("ability_layer") or "")
    answer = str((sample.get("stage_2_grounded") or {}).get("answer") or "")
    if layer == "L5_drug_boundary_negative":
        if not BOUNDARY_REFUSAL_RE.search(answer):
            violations.append("drug_boundary_missing_refusal_or_source_check")
        if DRUG_EXECUTABLE_RE.search(answer) and not BOUNDARY_REFUSAL_RE.search(answer):
            violations.append("drug_boundary_executable_instruction_without_refusal")
    return {"passed": not violations, "violations": violations}


def style_quality_check(sample: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    answer = str((sample.get("stage_2_grounded") or {}).get("answer") or "").strip()
    question = str(sample.get("question") or "").strip()
    layer = str(sample.get("ability_layer") or "")
    risk_class = str(sample.get("risk_class") or "")
    style_flags = sample.get("style_flags") if isinstance(sample.get("style_flags"), dict) else {}
    dict_like_detected = bool(style_flags.get("dict_like_detected")) or bool(DICT_LIKE_OUTPUT_RE.search(answer))
    english_template_label_detected = bool(style_flags.get("english_label_detected")) or bool(ENGLISH_TEMPLATE_LABEL_RE.search(answer))
    clinical_conversation_score = style_flags.get("clinical_conversation_score")
    try:
        score = float(clinical_conversation_score) if clinical_conversation_score is not None else 1.0
    except (TypeError, ValueError):
        score = 1.0
    citation_count = answer.count("[source=") + answer.count("[rule=") + answer.count("[fact=")
    negative_boundary_hits = len(NEGATIVE_BOUNDARY_CUE_RE.findall(answer))
    high_risk = risk_class in HIGH_RISK_CLASSES or layer in HIGH_RISK_LAYERS
    low_risk_positive = layer in LOW_RISK_EXECUTIVE_CONTEXT_LAYERS and not high_risk

    if dict_like_detected:
        violations.append("dict_like_output")
    if english_template_label_detected:
        violations.append("english_template_label_output")
    if score < 0.6:
        violations.append("clinical_conversation_score_too_low")
    if low_risk_positive and len(answer) < 120:
        violations.append("information_density_too_low")
    if low_risk_positive and citation_count >= 1 and negative_boundary_hits >= 3 and len(answer) < 220:
        violations.append("boundary_dominates_low_risk_answer")
    if low_risk_positive and question and answer and len(answer) <= max(80, int(len(question) * 1.3)):
        violations.append("answer_too_short_for_training")

    return {
        "passed": not violations,
        "violations": violations,
        "dict_like_detected": dict_like_detected,
        "english_template_label_detected": english_template_label_detected,
        "clinical_conversation_score": score,
        "citation_count": citation_count,
        "negative_boundary_hits": negative_boundary_hits,
    }


def executive_triggered_positive_context(sample: dict[str, Any], triggered: bool) -> bool:
    if not triggered:
        return False
    layer = str(sample.get("ability_layer") or "")
    risk_class = str(sample.get("risk_class") or "")
    if risk_class in HIGH_RISK_CLASSES or layer in HIGH_RISK_LAYERS:
        return True
    if layer not in LOW_RISK_EXECUTIVE_CONTEXT_LAYERS:
        return True
    question = str(sample.get("question") or "")
    answer = str((sample.get("stage_2_grounded") or {}).get("answer") or "")
    text = f"{question}\n{answer}"
    return not bool(NEGATIVE_BOUNDARY_CUE_RE.search(text))


def hard_gate_check(sample: dict[str, Any], facts: dict[str, dict[str, Any]], hard_rules: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    anchors = [anchor for anchor in sample.get("evidence_anchors", []) if isinstance(anchor, dict)]
    ability_layer = str(sample.get("ability_layer") or "")
    risk_class = str(sample.get("risk_class") or "")
    answer = str((sample.get("stage_2_grounded") or {}).get("answer") or "")
    question = str(sample.get("question") or "")
    high_risk = risk_class in HIGH_RISK_CLASSES or ability_layer in HIGH_RISK_LAYERS
    has_rule_card = any(str(anchor.get("rule_card_id") or "").strip() for anchor in anchors)
    has_a0 = has_a0_authority(sample, anchors, facts)
    triggered = bool(EXECUTIVE_TRIGGER_RE.search(f"{question}\n{answer}"))
    positive_triggered = executive_triggered_positive_context(sample, triggered)
    positive_or_executive = positive_triggered or risk_class in {"withdrawal_mrl_residue", "food_safety"} or ability_layer in HIGH_RISK_LAYERS
    boundary_policy = boundary_policy_check(sample)
    style_quality = style_quality_check(sample)

    if high_risk and not has_rule_card:
        violations.append("high_risk_missing_rule_card")
    if positive_or_executive and not has_rule_card:
        violations.append("executive_content_missing_rule_card")
    if positive_or_executive and not has_a0:
        violations.append("executive_content_missing_a0_source")
    if high_risk and hard_rules and not hard_rules.get("rules"):
        violations.append("hard_block_rules_empty")
    violations.extend(boundary_policy["violations"])
    violations.extend(style_quality["violations"])

    return {
        "passed": not violations,
        "violations": violations,
        "high_risk": high_risk,
        "triggered": triggered,
        "positive_triggered": positive_triggered,
        "has_a0_or_label_source": has_a0,
        "has_rule_card": has_rule_card,
        "boundary_policy_check": boundary_policy,
        "style_quality_check": style_quality,
    }


def judge_check(structure: dict[str, Any], fact: dict[str, Any], hard_gate: dict[str, Any]) -> dict[str, Any]:
    style_quality = hard_gate.get("style_quality_check") or {}
    passed = bool(structure["passed"] and fact["passed"] and hard_gate["passed"] and style_quality.get("passed", True))
    return {
        "passed": passed,
        "mode": "deterministic_placeholder",
        "total_score": 9.0 if passed else max(0.0, round(float(style_quality.get("clinical_conversation_score", 0.0)) * 10, 2)),
        "language_quality": 9 if passed else (6 if style_quality.get("clinical_conversation_score", 0.0) >= 0.6 else 2),
        "clinical_clarity": 9 if passed else (6 if style_quality.get("clinical_conversation_score", 0.0) >= 0.6 else 2),
        "boundary_respect": 9 if passed else 0,
    }


def reject_reasons_for(structure: dict[str, Any], fact: dict[str, Any], hard_gate: dict[str, Any], judge: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for reason in structure.get("missing_fields", []) + structure.get("anchor_errors", []):
        reasons.append(f"structure:{reason}")
    for key in (
        "unsupported_claims",
        "wrong_fact_links",
        "wrong_source_links",
        "usage_scope_violations",
        "coverage_violations",
        "citation_violations",
        "page_violations",
    ):
        for reason in fact.get(key, []):
            reasons.append(f"fact:{reason}")
    for reason in hard_gate.get("violations", []):
        reasons.append(f"hard_gate:{reason}")
    if not judge.get("passed"):
        reasons.append("judge:deterministic_placeholder_failed")
    return reasons


def evaluate_samples(
    samples: list[dict[str, Any]],
    facts: dict[str, dict[str, Any]],
    manifest_paths: set[str],
    hard_rules: dict[str, Any],
) -> list[dict[str, Any]]:
    evaluated: list[dict[str, Any]] = []
    for sample in samples:
        structure = structure_check(sample)
        fact = fact_level_check(sample, facts, manifest_paths)
        hard_gate = hard_gate_check(sample, facts, hard_rules)
        judge = judge_check(structure, fact, hard_gate)
        accepted = structure["passed"] and fact["passed"] and hard_gate["passed"] and judge["passed"]
        reject_reasons = [] if accepted else reject_reasons_for(structure, fact, hard_gate, judge)
        evaluated.append(
            {
                **sample,
                "structure_check": structure,
                "fact_level_check": fact,
                "hard_gate_check": hard_gate,
                "judge_check": judge,
                "final_decision": "accepted" if accepted else "rejected",
                "reject_reasons": reject_reasons,
            }
        )
    return evaluated


def summarize(evaluated: list[dict[str, Any]], generated_path: Path, output_path: Path, root: Path) -> dict[str, Any]:
    accepted = [row for row in evaluated if row["final_decision"] == "accepted"]
    rejected = [row for row in evaluated if row["final_decision"] == "rejected"]
    reason_counts: dict[str, int] = {}
    for row in rejected:
        for reason in row.get("reject_reasons", []):
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    return {
        "generated_at": now(),
        "phase": "phase15_fact_level_evaluate_samples",
        "mode": "deterministic_fact_and_hard_gate",
        "input_generated": relative(generated_path, root),
        "output": relative(output_path, root),
        "samples": len(evaluated),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "reject_reason_counts": dict(sorted(reason_counts.items())),
        "passed": bool(evaluated) and all(row.get("reject_reasons") for row in rejected),
    }


def write_reports(summary: dict[str, Any], evaluated: list[dict[str, Any]], report_json: Path, reject_csv: Path, report_md: Path) -> None:
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    reject_csv.parent.mkdir(parents=True, exist_ok=True)
    with reject_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sample_id", "final_decision", "reject_reason"])
        writer.writeheader()
        for row in evaluated:
            if row["final_decision"] == "rejected":
                for reason in row.get("reject_reasons", []):
                    writer.writerow(
                        {
                            "sample_id": row.get("sample_id", ""),
                            "final_decision": row.get("final_decision", ""),
                            "reject_reason": reason,
                        }
                    )
    lines = [
        "# Phase 15 Fact-Level Evaluation",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Samples: {summary['samples']}",
        f"- Accepted: {summary['accepted']}",
        f"- Rejected: {summary['rejected']}",
        f"- Passed: {summary['passed']}",
        "",
        "## Reject Reasons",
        "",
    ]
    if summary["reject_reason_counts"]:
        lines.extend(f"- {key}: {value}" for key, value in summary["reject_reason_counts"].items())
    else:
        lines.append("- none")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default=today())
    parser.add_argument("--generated", default="")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    wiki_root = args.wiki_root.resolve()
    exports = wiki_root / "exports"
    issues = wiki_root / "issues" / "wiki_first_generation_reports"
    generated_path = resolve_path(args.generated, wiki_root, exports / "generated_samples", "two_stage_samples")
    samples = read_jsonl(generated_path)
    if args.limit:
        samples = samples[: args.limit]
    facts = load_fact_index(exports / "knowledge_facts_status_index.json")
    manifest_paths = load_manifest_paths(exports / "runtime_core_manifest.json")
    hard_rules = read_json(exports / "exporter_hard_block_rules.json")

    output = exports / "evaluated_samples" / f"fact_evaluated_samples_{args.date}.jsonl"
    evaluated = evaluate_samples(samples, facts, manifest_paths, hard_rules)
    write_jsonl(output, evaluated)
    summary = summarize(evaluated, generated_path, output, wiki_root)
    write_reports(
        summary,
        evaluated,
        issues / f"phase15_fact_eval_{args.date}.json",
        issues / f"phase15_reject_reasons_{args.date}.csv",
        issues / f"phase15_fact_eval_{args.date}.md",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
