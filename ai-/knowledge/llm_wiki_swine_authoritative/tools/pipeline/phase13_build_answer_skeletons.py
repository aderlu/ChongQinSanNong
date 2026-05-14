from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues" / "wiki_first_generation_reports"
TZ = timezone(timedelta(hours=8))
MOJIBAKE_RE = re.compile(r"[\uFFFD]|锛\?|銆\?|鏈|璇ユ|鐚|涓嶅|瑙勮寖")


def today() -> str:
    return datetime.now(TZ).strftime("%Y%m%d")


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


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


def ensure_recent_nonempty_jsonl(path: Path, *, max_age_seconds: int = 300) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Required upstream file is missing: {path}")
    rows = read_jsonl(path)
    if not rows:
        raise RuntimeError(f"Required upstream file is empty or unreadable: {path}")
    age_seconds = (datetime.now(TZ) - datetime.fromtimestamp(path.stat().st_mtime, TZ)).total_seconds()
    if age_seconds > max_age_seconds:
        raise RuntimeError(
            f"Upstream file looks stale ({age_seconds:.1f}s old > {max_age_seconds}s): {path}. "
            "Re-run the previous phase before continuing."
        )
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def split_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").replace(",", ";").split(";") if item.strip()]


def claim_rule_cards(plan: dict[str, Any], *, for_fact_claim: bool = False) -> list[str]:
    cards = split_list(plan.get("required_rule_cards"))
    if for_fact_claim and "RC-CITATION-001" not in cards:
        cards.append("RC-CITATION-001")
    return cards


def latest_jsonl(directory: Path, prefix: str) -> Path:
    files = sorted(directory.glob(f"{prefix}_*.jsonl"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {directory}")
    return files[0]


def date_from_plan(path: Path) -> str:
    match = re.search(r"(\d{8})", path.name)
    return match.group(1) if match else today()


def relative_or_absolute(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def fact_text(fact: dict[str, Any]) -> str:
    subject = str(fact.get("subject") or "").strip()
    predicate = str(fact.get("predicate") or "").strip()
    obj = str(fact.get("object") or "").strip()
    parts = [part for part in [subject, predicate, obj] if part]
    return "；".join(parts) if parts else str(fact.get("fact_id") or "")


def contains_mojibake(value: str) -> bool:
    return bool(MOJIBAKE_RE.search(value or ""))


def fact_matches_plan(fact: dict[str, Any], plan: dict[str, Any]) -> bool:
    entity_id = str(plan.get("entity_id") or "")
    page = str(plan.get("page_relpath") or "")
    target = str(fact.get("target_page") or "")
    fact_id = str(fact.get("fact_id") or "")
    if target and target == page:
        return True
    if entity_id and fact_id.startswith(entity_id):
        return True
    subject = str(fact.get("subject") or "")
    return bool(entity_id and entity_id in subject)


def fact_scope_allowed(fact: dict[str, Any], plan: dict[str, Any]) -> bool:
    fact_scopes = set(split_list(fact.get("usage_scope")))
    plan_layer = str(plan.get("ability_layer") or "")
    if not fact_scopes:
        return False
    if plan_layer == "L1_retrieval_grounded":
        return "retrieval" in fact_scopes
    if plan_layer == "L2_diagnosis_support":
        return bool(fact_scopes.intersection({"diagnosis_support", "gold_candidate", "retrieval"}))
    if plan_layer == "L3_differential_support":
        return bool(fact_scopes.intersection({"differential_support", "gold_candidate", "retrieval"}))
    if plan_layer == "L4_control_boundary":
        return bool(fact_scopes.intersection({"control_support", "gold_candidate", "retrieval"}))
    if plan_layer == "L5_drug_boundary_negative":
        return bool(fact_scopes.intersection({"drug_boundary", "negative_trap", "retrieval"}))
    if plan_layer == "L6_regulatory_guardrail":
        return bool(fact_scopes.intersection({"regulatory_boundary", "control_support", "retrieval", "gold_candidate"}))
    return "retrieval" in fact_scopes


def select_facts(facts: list[dict[str, Any]], plan: dict[str, Any], limit: int = 4) -> list[dict[str, Any]]:
    candidates = [
        fact
        for fact in facts
        if str(fact.get("source_trust") or "") == "authoritative"
        and str(fact.get("evidence_coverage") or "") in {"complete", "partial"}
        and fact_matches_plan(fact, plan)
        and fact_scope_allowed(fact, plan)
    ]
    candidates.sort(
        key=lambda fact: (
            0 if str(fact.get("evidence_coverage")) == "complete" else 1,
            str(fact.get("fact_id") or ""),
        )
    )
    return candidates[:limit]


def claim_type_for(plan: dict[str, Any]) -> str:
    mapping = {
        "L1_retrieval_grounded": "retrieval_grounded_fact",
        "L2_diagnosis_support": "diagnosis_boundary",
        "L3_differential_support": "differential_boundary",
        "L4_control_boundary": "control_boundary",
        "L5_drug_boundary_negative": "drug_boundary",
        "L6_regulatory_guardrail": "regulatory_boundary",
    }
    return mapping.get(str(plan.get("ability_layer") or ""), "retrieval_grounded_fact")


def must_not_include_for(plan: dict[str, Any]) -> list[str]:
    layer = str(plan.get("ability_layer") or "")
    risk = str(plan.get("risk_class") or "")
    items = list((plan.get("question_blueprint") or {}).get("must_not_ask_about") or [])
    if layer == "L5_drug_boundary_negative" or risk in {"withdrawal_mrl_residue", "food_safety"}:
        items.append("不得给出无标签或无 A0 来源的剂量、疗程、给药途径、休药期或 MRL 结论")
    if layer == "L6_regulatory_guardrail" or risk == "high_regulatory":
        items.append("不得给出无当前官方来源的上报、封锁、扑杀、调运或监管执行结论")
    return list(dict.fromkeys(str(item) for item in items if str(item)))


def hard_gate_profile_for(plan: dict[str, Any]) -> dict[str, Any]:
    layer = str(plan.get("ability_layer") or "")
    risk = str(plan.get("risk_class") or "")
    high_risk = risk in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"} or layer in {
        "L5_drug_boundary_negative",
        "L6_regulatory_guardrail",
    }
    return {
        "requires_a0_or_label_source": high_risk,
        "blocks_dose_course": layer == "L5_drug_boundary_negative" or risk in {"withdrawal_mrl_residue", "food_safety"},
        "blocks_withdrawal_mrl": layer == "L5_drug_boundary_negative" or risk in {"withdrawal_mrl_residue", "food_safety"},
        "blocks_regulatory_action_without_a0": layer == "L6_regulatory_guardrail" or risk == "high_regulatory",
        "high_risk": high_risk,
    }


def boundary_claim(plan: dict[str, Any], index: int) -> dict[str, Any]:
    cards = claim_rule_cards(plan)
    layer = str(plan.get("ability_layer") or "")
    if layer == "L5_drug_boundary_negative":
        claim = "该样本用于药物边界或负样本训练；没有标签级或 A0 来源覆盖具体产品、猪、剂型、途径、剂量、疗程和休药期时，不得生成执行性处方。"
    elif layer == "L6_regulatory_guardrail":
        claim = "该样本用于监管边界训练；涉及上报、封锁、扑杀、调运等执行性结论时，必须依据当前官方法规或主管部门要求，不能由模型直接替代决策。"
    else:
        claim = "该样本仅能基于已登记来源和规则卡生成边界性回答，不得扩展未锚定结论。"
    return {
        "claim_id": f"CLAIM-{plan['plan_id']}-{index:03d}",
        "claim_type": claim_type_for(plan),
        "claim": claim,
        "fact_ids": [],
        "source_ids": split_list(plan.get("source_ids")),
        "rule_card_ids": cards,
        "page_relpath": plan.get("page_relpath", ""),
    }


def fact_claim(plan: dict[str, Any], fact: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "claim_id": f"CLAIM-{plan['plan_id']}-{index:03d}",
        "claim_type": claim_type_for(plan),
        "claim": fact_text(fact),
        "fact_ids": [str(fact.get("fact_id") or "")],
        "source_ids": split_list(fact.get("evidence_source_id") or fact.get("source_id")),
        "rule_card_ids": claim_rule_cards(plan, for_fact_claim=True),
        "page_relpath": str(fact.get("target_page") or plan.get("page_relpath") or ""),
        "evidence_quote_span": str(fact.get("evidence_quote_span") or ""),
    }


def build_skeletons(plans: list[dict[str, Any]], facts: list[dict[str, Any]], limit: int | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    skeletons: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    for plan in plans:
        selected = select_facts(facts, plan)
        claims = [fact_claim(plan, fact, index + 1) for index, fact in enumerate(selected)]
        if not claims and split_list(plan.get("required_rule_cards")):
            claims = [boundary_claim(plan, 1)]
        if not claims:
            gaps.append({"plan_id": plan.get("plan_id"), "entity_id": plan.get("entity_id"), "reason": "no_fact_or_rule_anchor"})
            continue
        skeleton = {
            "skeleton_id": f"SKEL-{plan['plan_id']}",
            "plan_id": plan["plan_id"],
            "entity_id": plan.get("entity_id", ""),
            "entity_type": plan.get("entity_type", ""),
            "ability_layer": plan.get("ability_layer", ""),
            "question_intent": (plan.get("question_blueprint") or {}).get("intent", plan.get("task_type", "")),
            "answer_mode": "boundary_first" if str(plan.get("expected_output_type")) == "boundary_or_refusal" else "source_grounded",
            "must_include_claims": claims,
            "must_not_include": must_not_include_for(plan),
            "required_citations": {
                "min_source_count": 1 if any(claim.get("source_ids") for claim in claims) else 0,
                "min_rule_card_count": 1 if split_list(plan.get("required_rule_cards")) else 0,
                "require_fact_id": any(claim.get("fact_ids") for claim in claims),
                "require_page_relpath": True,
            },
            "hard_gate_profile": hard_gate_profile_for(plan),
        }
        if any(contains_mojibake(str(value)) for value in skeleton["must_not_include"]):
            gaps.append({"plan_id": plan.get("plan_id"), "entity_id": plan.get("entity_id"), "reason": "mojibake_in_boundary_text"})
            continue
        if any(contains_mojibake(str(claim.get("claim") or "")) for claim in claims):
            gaps.append({"plan_id": plan.get("plan_id"), "entity_id": plan.get("entity_id"), "reason": "mojibake_in_claim_text"})
            continue
        skeletons.append(skeleton)
        if limit and len(skeletons) >= limit:
            break
    return skeletons, gaps


def summarize(skeletons: list[dict[str, Any]], gaps: list[dict[str, Any]], plan_path: Path, output: Path, root: Path) -> dict[str, Any]:
    layer_counts: dict[str, int] = {}
    for item in skeletons:
        layer = str(item.get("ability_layer") or "")
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    return {
        "generated_at": now(),
        "phase": "phase13_build_answer_skeletons",
        "input_plan": relative_or_absolute(plan_path, root),
        "output": relative_or_absolute(output, root),
        "skeletons": len(skeletons),
        "skeletons_generated": len(skeletons),
        "gaps": len(gaps),
        "ability_layer_counts": layer_counts,
        "gap_sample": gaps[:20],
        "gap_report": gaps,
        "passed": bool(skeletons),
    }


def write_report(summary: dict[str, Any], report_json: Path, report_md: Path) -> None:
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Phase 13 Answer Skeletons",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Skeletons: {summary['skeletons']}",
        f"- Gaps: {summary['gaps']}",
        f"- Passed: {summary['passed']}",
        "",
        "## Ability Layers",
        "",
    ]
    for key, value in sorted(summary["ability_layer_counts"].items()):
        lines.append(f"- {key}: {value}")
    if summary["gap_sample"]:
        lines.extend(["", "## Gap Sample", ""])
        lines.extend(f"- {item}" for item in summary["gap_sample"])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default="")
    parser.add_argument("--plan", default="")
    parser.add_argument("--plan-file", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--max-plan-age-seconds", type=int, default=300)
    args = parser.parse_args()

    wiki_root = args.wiki_root.resolve()
    exports = wiki_root / "exports"
    issues = wiki_root / "issues" / "wiki_first_generation_reports"
    plan_arg = args.plan_file or args.plan
    plan_path = Path(plan_arg) if plan_arg else latest_jsonl(exports / "planned_samples", "wiki_sample_plan")
    if not plan_path.is_absolute():
        plan_path = wiki_root / plan_path

    output_date = args.date or date_from_plan(plan_path)
    plans = ensure_recent_nonempty_jsonl(plan_path, max_age_seconds=args.max_plan_age_seconds)
    facts = read_json(exports / "knowledge_facts_status_index.json")
    if not isinstance(facts, list):
        raise TypeError("knowledge_facts_status_index must be a list")

    skeletons, gaps = build_skeletons(plans, [fact for fact in facts if isinstance(fact, dict)], limit=args.limit or None)
    if not skeletons:
        raise RuntimeError(
            f"Phase13 generated zero skeletons from plan {plan_path}. "
            "This usually indicates upstream race conditions, stale input, or fact/plan mismatch."
        )

    output = exports / "answer_skeletons" / f"wiki_answer_skeletons_{output_date}.jsonl"
    write_jsonl(output, skeletons)
    summary = summarize(skeletons, gaps, plan_path, output, wiki_root)
    write_report(
        summary,
        issues / f"phase13_answer_skeletons_{output_date}.json",
        issues / f"phase13_answer_skeletons_{output_date}.md",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
