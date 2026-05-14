from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Sequence
from typing import Any, Callable, Mapping

from chicken_data_synthesis.application.services import (
    aggregate_judge_rows,
    build_benchmark_detail_base_row,
    build_benchmark_summary_context,
    build_benchmark_summary_context_key,
    build_generation_failure_judge_rows,
    build_judge_columns,
    collect_benchmark_summary_rows,
    normalize_benchmark_judge_result,
)
from chicken_data_synthesis.application.use_cases.run_benchmark import (
    BenchmarkExecutionPlan,
    BenchmarkRunResult,
    BenchmarkPlanningInput,
    build_benchmark_run_result,
    build_benchmark_execution_plan_from_payload,
    build_benchmark_planning_input,
)

BenchmarkUseCaseInput = BenchmarkPlanningInput | BenchmarkExecutionPlan
prepare_benchmark_planning_input = build_benchmark_planning_input

BenchmarkCallModel = Callable[
    [dict[str, Any], str, list[dict[str, str]], float, str, int],
    tuple[str | None, str | None, float],
]
BenchmarkParsePayload = Callable[[str | None], Mapping[str, Any] | None]
BenchmarkPromptBuilder = Callable[[Mapping[str, Any]], list[dict[str, str]]]
BenchmarkNormalizeGenerationCase = Callable[[str, Mapping[str, Any], str, str], Mapping[str, Any]]
BenchmarkWriteCsv = Callable[[Path, tuple[str, ...], Sequence[Mapping[str, Any]]], None]
BenchmarkAppendCsvRow = Callable[[Path, tuple[str, ...], Mapping[str, Any], bool], None]


@dataclass(frozen=True)
class BenchmarkExecutionDependencies:
    call_model: BenchmarkCallModel
    parse_payload: BenchmarkParsePayload
    build_generation_messages: BenchmarkPromptBuilder
    build_judge_messages: BenchmarkPromptBuilder
    normalize_generation_case: BenchmarkNormalizeGenerationCase
    write_csv: BenchmarkWriteCsv
    append_csv_row: BenchmarkAppendCsvRow


@dataclass(frozen=True)
class BenchmarkExecutionSettings:
    detail_fields: tuple[str, ...]
    summary_fields: tuple[str, ...]
    max_retries: int = 3


def prepare_benchmark_argv(argv: Sequence[str] | None = None) -> tuple[str, ...] | None:
    """Normalize benchmark CLI arguments before handing them to the script adapter."""

    if argv is None:
        return None
    return tuple(argv)


def prepare_benchmark_use_case_input(runtime_input: BenchmarkUseCaseInput) -> BenchmarkExecutionPlan:
    """Normalize a planning input or execution plan for downstream benchmark execution."""

    if isinstance(runtime_input, BenchmarkExecutionPlan):
        return runtime_input
    return build_benchmark_execution_plan_from_payload(
        runtime_input.config,
        runtime_input.cases_payload,
        runtime_input.output_dir,
        runtime_input.timestamp,
    )


def build_benchmark_use_case_plan(
    *,
    config,
    cases_payload,
    output_dir,
    timestamp: str,
) -> BenchmarkExecutionPlan:
    """Create a benchmark execution plan without invoking the legacy CLI bridge."""

    planning_input = prepare_benchmark_planning_input(
        config=config,
        cases_payload=cases_payload,
        output_dir=output_dir,
        timestamp=timestamp,
    )
    return prepare_benchmark_use_case_input(planning_input)


def execute_benchmark_use_case(
    plan: BenchmarkExecutionPlan,
    *,
    config: Mapping[str, Any],
    dependencies: BenchmarkExecutionDependencies,
    settings: BenchmarkExecutionSettings,
) -> BenchmarkRunResult:
    """Execute a prepared benchmark plan without going through the legacy CLI bridge."""

    generators = config["benchmark"]["generator_candidates"]
    evaluators = config["benchmark"]["evaluator_candidates"]

    detail_path = Path(plan.output_paths.detail_csv)
    summary_path = Path(plan.output_paths.summary_csv)
    detail_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    combo_lookup = {
        combination.combination_key: {
            "combination_key": combination.combination_key,
            "generator_key": combination.generator_key,
            "judge_keys": list(combination.judge_keys),
        }
        for combination in plan.combinations
    }
    evaluator_models = {key: value["name"] for key, value in evaluators.items()}
    detail_rows: list[dict[str, Any]] = []
    summary_contexts: dict[tuple[str, str], dict[str, Any]] = {}

    dependencies.write_csv(detail_path, settings.detail_fields, [])

    for work_item in plan.work_items:
        generator_config = generators[work_item.generator_key]
        selected_evaluators = {
            judge_key: evaluators[judge_key]
            for judge_key in work_item.judge_keys
            if judge_key
        }
        case_seed = dict(work_item.case_seed)
        content, error, generation_seconds = dependencies.call_model(
            generator_config,
            plan.base_url,
            dependencies.build_generation_messages(case_seed),
            plan.request_interval,
            "json",
            settings.max_retries,
        )
        parsed_generation = dependencies.parse_payload(content)
        base_row = build_benchmark_detail_base_row(
            work_item,
            case_seed,
            generator_model=generator_config["name"],
            generation_success=parsed_generation is not None,
            generation_error=error or "",
            generation_seconds=generation_seconds,
        )
        if parsed_generation is not None:
            case_data = dict(
                dependencies.normalize_generation_case(
                    str(case_seed.get("disease_name", "")),
                    parsed_generation,
                    work_item.generator_key,
                    generator_config["name"],
                )
            )
            base_row.update(
                {
                    "species": case_data["species"],
                    "user_query": case_data["user_query"],
                    "diagnosis": case_data["diagnosis"],
                    "prescription": case_data["prescription"],
                    "withdrawal_period": case_data["withdrawal_period"],
                    "metadata_json": _serialize_metadata(case_data.get("metadata")),
                }
            )
            judge_rows = _evaluate_benchmark_case(
                case_data,
                selected_evaluators,
                base_url=plan.base_url,
                request_interval=plan.request_interval,
                dependencies=dependencies,
                max_retries=settings.max_retries,
            )
        else:
            judge_rows = build_generation_failure_judge_rows(selected_evaluators)

        base_row.update(aggregate_judge_rows(judge_rows))
        base_row.update(build_judge_columns(judge_rows))
        detail_rows.append(base_row)
        dependencies.append_csv_row(detail_path, settings.detail_fields, base_row, include_header=False)

        summary_key = build_benchmark_summary_context_key(work_item)
        summary_context = summary_contexts.setdefault(
            summary_key,
            build_benchmark_summary_context(
                work_item,
                combo_lookup[work_item.combination_key],
                generator_model=generator_config["name"],
            ),
        )
        summary_context["generator_rows"].append(base_row)

    summary_rows = collect_benchmark_summary_rows(
        summary_contexts,
        evaluator_models=evaluator_models,
        requested_samples=plan.samples_per_generator,
    )

    dependencies.write_csv(detail_path, settings.detail_fields, detail_rows)
    dependencies.write_csv(summary_path, settings.summary_fields, summary_rows)
    return build_benchmark_run_result(plan, detail_rows=detail_rows, summary_rows=summary_rows)


def run_benchmark_use_case(
    argv: Sequence[str] | None = None,
    *,
    runtime_input: BenchmarkUseCaseInput | None = None,
    execution_config: Mapping[str, Any] | None = None,
    execution_dependencies: BenchmarkExecutionDependencies | None = None,
    execution_settings: BenchmarkExecutionSettings | None = None,
) -> BenchmarkExecutionPlan | BenchmarkRunResult | None:
    """Run the benchmark use case or normalize a plan for downstream execution."""

    if runtime_input is not None:
        plan = prepare_benchmark_use_case_input(runtime_input)
        if execution_config is not None and execution_dependencies is not None and execution_settings is not None:
            return execute_benchmark_use_case(
                plan,
                config=execution_config,
                dependencies=execution_dependencies,
                settings=execution_settings,
            )
        return plan

    prepared_argv = prepare_benchmark_argv(argv)
    raise RuntimeError(
        "Legacy benchmark CLI has been removed from the trimmed project layout. "
        "Use build_benchmark_use_case_plan() and execute_benchmark_use_case() with explicit dependencies instead."
        f" argv={list(prepared_argv) if prepared_argv is not None else []}"
    )


def run_benchmark_cli(argv: Sequence[str] | None = None) -> None:
    """Run the benchmark entrypoint through the application-layer use case."""

    run_benchmark_use_case(argv=argv)


def _evaluate_benchmark_case(
    case_data: Mapping[str, Any],
    evaluators: Mapping[str, dict[str, Any]],
    *,
    base_url: str,
    request_interval: float,
    dependencies: BenchmarkExecutionDependencies,
    max_retries: int,
) -> list[dict[str, Any]]:
    judge_rows: list[dict[str, Any]] = []
    for judge_key, judge_config in evaluators.items():
        if not judge_key:
            continue
        content, error, elapsed = dependencies.call_model(
            judge_config,
            base_url,
            dependencies.build_judge_messages(dict(case_data)),
            request_interval,
            "json",
            max_retries,
        )
        parsed = dependencies.parse_payload(content)
        judge_row = {
            "judge_key": judge_key,
            "judge_model": judge_config["name"],
            "judge_seconds": round(elapsed, 3),
            "parse_ok": parsed is not None,
            "error": error or "",
        }
        if parsed is None:
            judge_row.update(
                {
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
        else:
            judge_row.update(normalize_benchmark_judge_result(parsed))
        judge_rows.append(judge_row)
    return judge_rows


def _serialize_metadata(metadata: Any) -> str:
    import json

    return json.dumps(metadata or {}, ensure_ascii=False)


__all__ = [
    "BenchmarkExecutionDependencies",
    "BenchmarkExecutionSettings",
    "BenchmarkUseCaseInput",
    "build_benchmark_use_case_plan",
    "execute_benchmark_use_case",
    "prepare_benchmark_argv",
    "prepare_benchmark_planning_input",
    "prepare_benchmark_use_case_input",
    "run_benchmark_cli",
    "run_benchmark_use_case",
]
