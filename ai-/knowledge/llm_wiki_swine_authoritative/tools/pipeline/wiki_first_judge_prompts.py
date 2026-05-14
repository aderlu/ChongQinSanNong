from __future__ import annotations

from typing import Any, Mapping


PASS_THRESHOLD = 80.0
REVIEW_THRESHOLD = 60.0
ARBITRATION_SCORE_GAP = 8.0
SCORECARD_VERSION = "wiki_first_g_eval_v2"

HIGH_RISK_CLASSES = {"high_regulatory", "withdrawal_mrl_residue", "food_safety"}
HIGH_RISK_LAYERS = {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}

JUDGE_A_DIMENSIONS: dict[str, int] = {
    "evidence_fidelity": 28,
    "clinical_reasoning": 22,
    "safety_boundary": 20,
    "question_resolution": 15,
    "training_utility": 15,
}

JUDGE_B_DIMENSIONS: dict[str, int] = {
    "risk_control": 30,
    "unsupported_expansion_control": 20,
    "answer_completeness": 20,
    "citation_integrity": 15,
    "language_naturalness": 15,
}

ARBITER_DIMENSIONS: dict[str, int] = {
    "consensus_reliability": 25,
    "safety_override": 30,
    "evidence_sufficiency": 20,
    "training_value": 15,
    "calibration_consistency": 10,
}

JUDGE_A_RUBRIC: dict[str, str] = {
    "evidence_fidelity": "是否严格基于已给出的 fact/source/rule/page 锚点回答，不虚构、不越界。",
    "clinical_reasoning": "是否在当前证据边界内给出合理的诊断支持、鉴别或控制逻辑。",
    "safety_boundary": "是否在高风险或边界场景下明确拒绝越权建议，并说明不能直接执行什么。",
    "question_resolution": "是否正面回应用户问题，而不是只堆引用或只复述边界。",
    "training_utility": "是否足够清晰、自然、可训练，适合作为高质量单轮 SFT 样本。",
}

JUDGE_B_RUBRIC: dict[str, str] = {
    "risk_control": "回答是否有效降低错误执行、违规用药、错误监管建议等风险。",
    "unsupported_expansion_control": "是否避免补充未被证据支持的事实、处置、剂量、监管动作。",
    "answer_completeness": "在允许的证据边界内，回答是否尽量完整，不空泛。",
    "citation_integrity": "关键结论是否有清晰可追溯的 citation 和 evidence anchor 支撑。",
    "language_naturalness": "语言是否自然、专业、像真实临床咨询，而不是模板/对象串。",
}

ARBITER_RUBRIC: dict[str, str] = {
    "consensus_reliability": "两位裁判的共识是否足够稳定，是否存在需要保守化处理的明显分歧。",
    "safety_override": "当安全风险与训练价值冲突时，是否优先采取更安全的结论。",
    "evidence_sufficiency": "最终结论是否与当前证据充分性匹配，不夸大可用性。",
    "training_value": "最终是否适合作为训练样本，或更适合进入 review / reject / repair 队列。",
    "calibration_consistency": "仲裁结论是否与前置 hard gate、Phase15/18 信号保持一致。",
}

# Keep the scorecard text readable for future LLM-judge prompt assembly.  Some
# historical Windows console writes left the first rubric block mojibaked, so
# these clean UTF-8 definitions intentionally override the earlier constants.
JUDGE_A_RUBRIC = {
    "evidence_fidelity": "是否严格基于已给出的 fact/source/rule/page 锚点回答，不虚构、不越界。",
    "clinical_reasoning": "是否在当前证据边界内给出合理的诊断支持、鉴别或控制逻辑。",
    "safety_boundary": "是否在高风险或边界场景下明确拒绝越权建议，并说明不能直接执行什么。",
    "question_resolution": "是否正面回应用户问题，而不是只堆引用或只复述边界。",
    "training_utility": "是否足够清晰、自然、可训练，适合作为高质量单轮 SFT 样本。",
}

JUDGE_B_RUBRIC = {
    "risk_control": "回答是否有效降低错误执行、违规用药、错误监管建议等风险。",
    "unsupported_expansion_control": "是否避免补充未被证据支持的事实、处置、剂量、监管动作。",
    "answer_completeness": "在允许的证据边界内，回答是否尽量完整，不空泛。",
    "citation_integrity": "关键结论是否有清晰可追溯的 citation 和 evidence anchor 支撑。",
    "language_naturalness": "语言是否自然、专业、像真实临床咨询，而不是模板或对象串。",
}

ARBITER_RUBRIC = {
    "consensus_reliability": "两位裁判的共识是否足够稳定，是否存在需要保守化处理的明显分歧。",
    "safety_override": "当安全风险与训练价值冲突时，是否优先采取更安全的结论。",
    "evidence_sufficiency": "最终结论是否与当前证据充分性匹配，不夸大可用性。",
    "training_value": "最终是否适合作为训练样本，或更适合进入 review / reject / repair 队列。",
    "calibration_consistency": "仲裁结论是否与前置 hard gate、Phase15/18 信号保持一致。",
}

JUDGE_COMMON_OUTPUT_FIELDS = (
    "judge_id",
    "judge_contract_version",
    "judge_input",
    "dimension_scores",
    "dimension_weights",
    "dimension_reasons",
    "total_score",
    "weighted_total_score",
    "scorecard_version",
    "fatal_risk",
    "structured_pass",
    "final_label",
    "passed",
    "summary",
    "strengths",
    "weaknesses",
    "flags",
)

ARBITER_OUTPUT_FIELDS = (
    "arbiter_contract_version",
    "arbiter_input",
    "trigger_codes",
    "dimension_scores",
    "dimension_weights",
    "dimension_reasons",
    "final_total_score",
    "weighted_total_score",
    "scorecard_version",
    "agreed_with_judge",
    "final_label",
    "fatal_risk",
    "structured_pass",
    "reason",
    "summary",
    "strengths",
    "weaknesses",
    "final_flags",
    "score_breakdown",
)

JUDGE_A_SYSTEM_PROMPT = """
Role: judge_a for wiki-first grounded sample review.
Focus:
- use a rubric-based weighted scorecard
- score each dimension independently before computing total score
- evaluate only with the provided question, grounded answer, anchors, and phase15 signals
- keep evidence boundary and hard safety constraints irreversible
Output style:
- JSON only
- preserve dimension_scores / dimension_weights / weighted_total_score / fatal_risk / structured_pass / final_label contract
- short summary, strengths, weaknesses, plus brief dimension reasons
""".strip()

JUDGE_B_SYSTEM_PROMPT = """
Role: judge_b for wiki-first grounded sample review.
Focus:
- use a rubric-based weighted scorecard
- emphasize training risk, unsupported expansion, citation integrity, and language naturalness
- evaluate only against the provided evidence boundary and declared task type
Output style:
- JSON only
- preserve dimension_scores / dimension_weights / weighted_total_score / fatal_risk / structured_pass / final_label contract
- short summary, strengths, weaknesses, plus brief dimension reasons
""".strip()

ARBITER_SYSTEM_PROMPT = """
Role: arbiter for wiki-first grounded sample review.
Focus:
- compare judge_a and judge_b
- explain arbitration trigger codes
- resolve final_total_score / final_label / fatal_risk conservatively using a weighted arbitration scorecard
- keep hard gate and evidence boundary decisions irreversible
Output style:
- JSON only
- preserve dimension_scores / dimension_weights / weighted_total_score / final_total_score / agreed_with_judge / final_label contract
- short reason, summary, strengths, weaknesses, plus brief dimension reasons
""".strip()

JUDGE_GENERAL_EVALUATION_STEPS = [
    "先判断回答是否严格限制在给定 evidence anchors 和 hard gate 范围内。",
    "逐项查看回答是否真正回应用户问题，而不是只重复标签、目录信息或空泛边界话术。",
    "对高风险样本，优先检查是否存在越权建议、错误执行动作、违规处置或无来源结论。",
    "对低风险正样本，检查信息密度、自然度和训练可用性，避免模板腔和对象串。",
    "最后按维度给分，并依据权重合成总分，再给出 pass / review / reject。",
]


def _anchor_snapshot(anchor: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "anchor_type": str(anchor.get("anchor_type") or ""),
        "claim_id": str(anchor.get("claim_id") or ""),
        "fact_id": str(anchor.get("fact_id") or ""),
        "source_id": str(anchor.get("source_id") or ""),
        "rule_card_id": str(anchor.get("rule_card_id") or ""),
        "page_relpath": str(anchor.get("page_relpath") or ""),
        "claim_supported": bool(anchor.get("claim_supported", True)),
    }


def _sample_context(sample: Mapping[str, Any]) -> dict[str, Any]:
    anchors = [item for item in sample.get("evidence_anchors", []) if isinstance(item, Mapping)]
    answer = ""
    stage_2 = sample.get("stage_2_grounded")
    if isinstance(stage_2, Mapping):
        answer = str(stage_2.get("answer") or "")
    return {
        "sample_id": str(sample.get("sample_id") or ""),
        "plan_id": str(sample.get("plan_id") or ""),
        "ability_layer": str(sample.get("ability_layer") or ""),
        "risk_class": str(sample.get("risk_class") or ""),
        "expected_output_type": str(sample.get("expected_output_type") or ""),
        "question": str(sample.get("question") or ""),
        "grounded_answer": answer,
        "anchor_count": len(anchors),
        "anchors": [_anchor_snapshot(anchor) for anchor in anchors[:8]],
        "phase15": {
            "final_decision": str(sample.get("final_decision") or ""),
            "structure_passed": bool((sample.get("structure_check") or {}).get("passed")),
            "fact_passed": bool((sample.get("fact_level_check") or {}).get("passed")),
            "hard_gate_passed": bool((sample.get("hard_gate_check") or {}).get("passed")),
            "hard_gate_high_risk": bool((sample.get("hard_gate_check") or {}).get("high_risk")),
            "hard_gate_triggered": bool((sample.get("hard_gate_check") or {}).get("triggered")),
            "reject_reasons": list(sample.get("reject_reasons") or []),
        },
    }


def build_judge_a_input(sample: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "system_prompt": JUDGE_A_SYSTEM_PROMPT,
        "scorecard_version": SCORECARD_VERSION,
        "evaluation_steps": JUDGE_GENERAL_EVALUATION_STEPS,
        "dimensions": JUDGE_A_DIMENSIONS,
        "rubric": JUDGE_A_RUBRIC,
        "label_thresholds": {"pass": PASS_THRESHOLD, "review": REVIEW_THRESHOLD},
        "sample": _sample_context(sample),
    }


def build_judge_b_input(sample: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "system_prompt": JUDGE_B_SYSTEM_PROMPT,
        "scorecard_version": SCORECARD_VERSION,
        "evaluation_steps": JUDGE_GENERAL_EVALUATION_STEPS,
        "dimensions": JUDGE_B_DIMENSIONS,
        "rubric": JUDGE_B_RUBRIC,
        "label_thresholds": {"pass": PASS_THRESHOLD, "review": REVIEW_THRESHOLD},
        "sample": _sample_context(sample),
    }


def build_arbiter_input(
    sample: Mapping[str, Any],
    judge_a_result: Mapping[str, Any],
    judge_b_result: Mapping[str, Any],
    trigger_codes: list[str],
) -> dict[str, Any]:
    return {
        "system_prompt": ARBITER_SYSTEM_PROMPT,
        "scorecard_version": SCORECARD_VERSION,
        "evaluation_steps": JUDGE_GENERAL_EVALUATION_STEPS,
        "score_gap_threshold": ARBITRATION_SCORE_GAP,
        "dimensions": ARBITER_DIMENSIONS,
        "rubric": ARBITER_RUBRIC,
        "sample": _sample_context(sample),
        "trigger_codes": list(trigger_codes),
        "judge_a_result": dict(judge_a_result),
        "judge_b_result": dict(judge_b_result),
    }
