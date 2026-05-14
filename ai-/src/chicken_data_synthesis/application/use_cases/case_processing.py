from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from chicken_data_synthesis.application.services import (
    build_case_error_result,
    build_case_result_base,
    build_completed_case_result,
    build_rule_blocked_result,
    should_require_arbitration,
)

CasePayload = dict[str, Any]
CaseResult = dict[str, Any]
ModelConfig = dict[str, Any]
TimedCasePayload = tuple[CasePayload | None, float]
GenerateCaseCallable = Callable[[str, str, ModelConfig], TimedCasePayload]
EvaluateRuleBaseCallable = Callable[[CasePayload], CasePayload]
EvaluateJudgeCallable = Callable[[CasePayload, str, ModelConfig], TimedCasePayload]
ArbitrateCaseCallable = Callable[[CasePayload, CasePayload, CasePayload, ModelConfig], TimedCasePayload]


@dataclass(frozen=True)
class CaseWorkflowTask:
    index: int
    disease_name: str
    generator_key: str
    generator_config: ModelConfig
    judge_a_config: ModelConfig
    judge_b_config: ModelConfig
    arbiter_config: ModelConfig
    evaluation_mode: str


def build_case_workflow_task(task_data: Sequence[Any]) -> CaseWorkflowTask:
    if len(task_data) != 8:
        raise ValueError("Case workflow task must contain 8 items.")

    (
        index,
        disease_name,
        generator_key,
        generator_config,
        judge_a_config,
        judge_b_config,
        arbiter_config,
        evaluation_mode,
    ) = task_data

    return CaseWorkflowTask(
        index=int(index),
        disease_name=str(disease_name),
        generator_key=str(generator_key),
        generator_config=dict(generator_config),
        judge_a_config=dict(judge_a_config),
        judge_b_config=dict(judge_b_config),
        arbiter_config=dict(arbiter_config),
        evaluation_mode=str(evaluation_mode),
    )


def run_case_workflow(
    task: CaseWorkflowTask,
    *,
    generate_case: GenerateCaseCallable,
    evaluate_rule_base: EvaluateRuleBaseCallable,
    evaluate_case: EvaluateJudgeCallable,
    arbitrate_case: ArbitrateCaseCallable,
    arbitration_threshold: float,
) -> CaseResult:
    result = build_case_result_base(
        task.index,
        task.disease_name,
        task.generator_key,
        task.generator_config["name"],
    )

    try:
        case_data, generation_seconds = generate_case(
            task.disease_name,
            task.generator_key,
            task.generator_config,
        )
        if case_data is None:
            return build_case_error_result(
                result,
                "案例生成失败",
                generation_seconds=round(generation_seconds, 2),
            )

        result["generation_seconds"] = round(generation_seconds, 2)
        result["case_data"] = case_data

        rule_base_result = evaluate_rule_base(case_data)
        result["rule_base_result"] = rule_base_result
        if rule_base_result.get("hard_block"):
            return build_rule_blocked_result(result, rule_base_result, error="规则底座拦截")

        judge_a_result, judge_a_seconds = evaluate_case(case_data, "judge_a", task.judge_a_config)
        result["judge_a_seconds"] = round(judge_a_seconds, 2)
        if judge_a_result is None:
            return build_case_error_result(result, "裁判A评分失败")
        result["judge_a_result"] = judge_a_result

        judge_b_result, judge_b_seconds = evaluate_case(case_data, "judge_b", task.judge_b_config)
        result["judge_b_seconds"] = round(judge_b_seconds, 2)
        if judge_b_result is None:
            return build_case_error_result(result, "裁判B评分失败")
        result["judge_b_result"] = judge_b_result

        need_arbitration = should_require_arbitration(
            judge_a_result,
            judge_b_result,
            arbitration_threshold,
        )
        result["needed_arbitration"] = need_arbitration

        arbiter_result: Mapping[str, Any] | None = None
        arbiter_seconds = 0.0
        if need_arbitration:
            arbiter_result, arbiter_seconds = arbitrate_case(
                case_data,
                judge_a_result,
                judge_b_result,
                task.arbiter_config,
            )
            result["arbiter_seconds"] = round(arbiter_seconds, 2)
            result["arbiter_result"] = arbiter_result

        return build_completed_case_result(
            result,
            case_data=case_data,
            rule_base_result=rule_base_result,
            judge_a_result=judge_a_result,
            judge_b_result=judge_b_result,
            arbitration_threshold=arbitration_threshold,
            arbiter_result=dict(arbiter_result) if isinstance(arbiter_result, Mapping) else None,
            generation_seconds=generation_seconds,
            judge_a_seconds=judge_a_seconds,
            judge_b_seconds=judge_b_seconds,
            arbiter_seconds=arbiter_seconds,
        )
    except Exception as exc:
        return build_case_error_result(result, str(exc))


__all__ = [
    "ArbitrateCaseCallable",
    "CasePayload",
    "CaseResult",
    "CaseWorkflowTask",
    "EvaluateJudgeCallable",
    "EvaluateRuleBaseCallable",
    "GenerateCaseCallable",
    "ModelConfig",
    "TimedCasePayload",
    "build_case_workflow_task",
    "run_case_workflow",
]
