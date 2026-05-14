from __future__ import annotations

import json
from typing import Any, Dict, List

from .renderer import render_template

PromptMessage = Dict[str, str]
PromptMessages = List[PromptMessage]


def _build_messages(system_prompt: str, user_prompt: str) -> PromptMessages:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _json_dumps(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _append_knowledge_context(prompt: str, knowledge_context: str = "") -> str:
    normalized = str(knowledge_context or "").strip()
    if not normalized:
        return prompt
    return (
        f"{prompt}\n\n"
        "【LLM Wiki 知识底座约束】\n"
        f"{normalized}\n\n"
        "使用要求：优先遵循 LLM Wiki 中的疾病、规则、药物和来源事实；"
        "涉及禁用药、休药期、强制免疫、报告/隔离等高风险内容时，"
        "若知识上下文不足，必须输出保守处理建议，不得凭空补全。"
        "最终样本必须保留 answer_json、evidence_anchors 和自然语言字段中的 source=... 标准引用。"
    )


def _append_target_disease_contract(prompt: str, disease_name: str = "") -> str:
    target = str(disease_name or "").strip()
    if not target:
        return prompt
    return (
        f"{prompt}\n\n"
        "【目标疾病一致性约束】\n"
        f"- 本样本目标疾病是：{target}。\n"
        "- diagnosis 的主要诊断必须显式写出该目标疾病，或写出该目标疾病与所用同义名/旧称之间的关系。\n"
        "- 如果问诊表现更像其他疾病，必须把目标疾病列入鉴别诊断并解释为何不作为主诊断；不能静默改成另一个疾病。"
    )


def build_consultation_draft_messages(
    disease_name: str,
    scenario_hint: str = "",
    knowledge_context: str = "",
) -> PromptMessages:
    system_prompt = render_template(
        "generation_query_system_prompt.j2",
        disease_name=disease_name,
    )
    user_prompt = render_template(
        "generation_query_user_prompt.j2",
        disease_name=disease_name,
        scenario_hint=scenario_hint,
    )
    system_prompt = _append_target_disease_contract(system_prompt, disease_name)
    return _build_messages(_append_knowledge_context(system_prompt, knowledge_context), user_prompt)


def build_blind_completion_messages(
    user_query: str,
    metadata: Dict[str, Any] | None = None,
    *,
    disease_name: str = "",
    knowledge_context: str = "",
) -> PromptMessages:
    system_prompt = render_template(
        "generation_completion_system_prompt.j2",
        disease_name=disease_name,
    )
    user_prompt = render_template(
        "generation_completion_user_prompt.j2",
        disease_name=disease_name,
        user_query=user_query,
        metadata_json=_json_dumps(metadata or {}),
    )
    system_prompt = _append_target_disease_contract(system_prompt, disease_name)
    return _build_messages(_append_knowledge_context(system_prompt, knowledge_context), user_prompt)


def build_judge_messages(case_data: Dict[str, Any], knowledge_context: str = "") -> PromptMessages:
    system_prompt = render_template("judge_system_prompt.j2")
    user_prompt = render_template(
        "judge_user_prompt.j2",
        user_query=str(case_data.get("user_query", "")),
        diagnosis=str(case_data.get("diagnosis", "")),
        prescription=str(case_data.get("prescription", "")),
        withdrawal_period=str(case_data.get("withdrawal_period", "")),
        answer_json=_json_dumps(case_data.get("answer_json", {})),
        evidence_anchors=_json_dumps(case_data.get("evidence_anchors", [])),
        metadata_json=_json_dumps(case_data.get("metadata", {})),
    )
    return _build_messages(_append_knowledge_context(system_prompt, knowledge_context), user_prompt)


def build_arbiter_messages(
    case_data: Dict[str, Any],
    judge_a_result: Dict[str, Any],
    judge_b_result: Dict[str, Any],
    knowledge_context: str = "",
) -> PromptMessages:
    system_prompt = render_template("arbiter_system_prompt.j2")
    user_prompt = render_template(
        "arbiter_user_prompt.j2",
        case_json=_json_dumps(case_data),
        judge_a_json=_json_dumps(judge_a_result),
        judge_b_json=_json_dumps(judge_b_result),
    )
    return _build_messages(_append_knowledge_context(system_prompt, knowledge_context), user_prompt)
