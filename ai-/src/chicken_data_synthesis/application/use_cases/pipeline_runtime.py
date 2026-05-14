from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from chicken_data_synthesis.application.services.task_planning import (
    filter_pending_tasks as filter_runtime_pending_tasks,
    resolve_milestones as resolve_stage_milestones,
    resolve_parallel_count,
)
from chicken_data_synthesis.infrastructure.persistence import (
    dedupe_results_by_index,
    get_completed_indexes,
)


@dataclass(slots=True, frozen=True)
class RuntimeOptions:
    mode: str
    evaluation_mode: str
    sample_count: int
    parallel_count: int
    milestones: tuple[int, ...]
    generator_key: str = ""
    resume_from: str = ""
    clear_temp: bool = True


@dataclass(slots=True, frozen=True)
class ResumeState:
    snapshot_path: str
    mode: str
    sample_count: int
    completed_target: int
    parallel_count: int | None
    milestones: tuple[int, ...]
    results: tuple[dict[str, Any], ...]
    completed_indexes: frozenset[int]


@dataclass(slots=True)
class ExecutionState:
    results: list[dict[str, Any]]
    completed_target: int
    completed_indexes: set[int]


@dataclass(slots=True, frozen=True)
class StageTarget:
    target_total: int
    start_index: int
    batch_size: int
    should_run: bool


@dataclass(slots=True, frozen=True)
class OutputPaths:
    timestamp: str
    run_prefix: str
    output_dir: str
    temp_dir: str
    log_file: str
    error_log_file: str
    result_csv: str
    summary_csv: str
    latest_snapshot_file: str


@dataclass(slots=True, frozen=True)
class PipelineRuntimePlan:
    options: RuntimeOptions
    resume_state: ResumeState | None
    stage_targets: tuple[StageTarget, ...]
    output_paths: OutputPaths


@dataclass(slots=True, frozen=True)
class PipelineExecutionContext:
    options: RuntimeOptions
    resume_state: ResumeState | None
    execution_state: ExecutionState
    stage_targets: tuple[StageTarget, ...]
    output_paths: OutputPaths


@dataclass(slots=True, frozen=True)
class StageBatchPlan:
    stage_target: StageTarget
    raw_tasks: tuple[Any, ...]
    pending_tasks: tuple[Any, ...]
    completed_indexes: frozenset[int]
    completed_target_before: int
    completed_target_after: int
    should_skip: bool


@dataclass(slots=True, frozen=True)
class StageCompletionPlan:
    stage_target: StageTarget
    completed_target_before: int
    completed_target_after: int
    stage_result_count: int
    total_result_count: int
    snapshot_target_hint: int


def normalize_runtime_options(
    *,
    mode: str,
    cli_samples: int = 0,
    cli_parallel: int = 0,
    raw_milestones: str = "",
    evaluation_mode: str = "legacy",
    generator_key: str = "",
    resume_from: str = "",
    config: Mapping[str, Any] | None = None,
    default_parallel: int = 1,
) -> RuntimeOptions:
    runtime_config = dict(config or {})
    normalized_mode = "production" if str(mode).lower() == "production" else "pilot"
    pilot_config = _as_mapping(runtime_config.get("pilot"))
    production_config = _as_mapping(runtime_config.get("production"))

    default_samples = int(
        pilot_config.get("sample_count", 30)
        if normalized_mode == "pilot"
        else runtime_config.get("total_samples", 1000)
    )
    sample_count = int(cli_samples) if int(cli_samples) > 0 else default_samples
    parallel_count = resolve_parallel_count(
        normalized_mode,
        cli_parallel,
        pilot_config=pilot_config,
        production_config=production_config,
        default_parallel=default_parallel,
    )
    milestones = tuple(
        resolve_stage_milestones(
            sample_count,
            raw_milestones,
            production_config=production_config,
        )
        if normalized_mode == "production"
        else []
    )
    normalized_resume_from = str(resume_from or "").strip()
    return RuntimeOptions(
        mode=normalized_mode,
        evaluation_mode=str(evaluation_mode or "legacy"),
        sample_count=sample_count,
        parallel_count=parallel_count,
        milestones=milestones,
        generator_key=str(generator_key or "").strip(),
        resume_from=normalized_resume_from,
        clear_temp=not bool(normalized_resume_from),
    )


def normalize_resume_state(
    raw_state: Mapping[str, Any] | None,
    *,
    snapshot_path: str = "",
    fallback_mode: str = "pilot",
    fallback_sample_count: int = 0,
) -> ResumeState | None:
    if not isinstance(raw_state, Mapping):
        return None

    deduped_results = tuple(deepcopy(dedupe_results_by_index(raw_state.get("results", []))))
    sample_count = _coerce_int(raw_state.get("sample_count"), fallback_sample_count)
    completed_target = _coerce_int(raw_state.get("completed_target"), 0)
    normalized_completed_target = min(max(completed_target, 0), sample_count) if sample_count > 0 else max(completed_target, 0)
    normalized_milestones = tuple(
        resolve_stage_milestones(
            sample_count,
            None,
            production_config={"milestones": raw_state.get("milestones", [])},
        )
        if sample_count > 0
        else []
    )
    return ResumeState(
        snapshot_path=str(snapshot_path or ""),
        mode=str(raw_state.get("mode") or fallback_mode or "pilot"),
        sample_count=sample_count,
        completed_target=normalized_completed_target,
        parallel_count=_coerce_optional_int(raw_state.get("parallel_count")),
        milestones=normalized_milestones,
        results=deduped_results,
        completed_indexes=frozenset(get_completed_indexes(deduped_results)),
    )


def build_stage_targets(
    mode: str,
    sample_count: int,
    *,
    milestones: Sequence[int] | None = None,
    completed_target: int = 0,
) -> tuple[StageTarget, ...]:
    normalized_mode = "production" if str(mode).lower() == "production" else "pilot"
    normalized_sample_count = max(int(sample_count), 0)
    if normalized_sample_count <= 0:
        return ()

    if normalized_mode == "pilot":
        return (
            StageTarget(
                target_total=normalized_sample_count,
                start_index=0,
                batch_size=normalized_sample_count,
                should_run=normalized_sample_count > 0,
            ),
        )

    targets: list[StageTarget] = []
    previous_target = 0
    for raw_target in milestones or (normalized_sample_count,):
        target_total = int(raw_target)
        if target_total <= previous_target:
            continue
        targets.append(
            StageTarget(
                target_total=target_total,
                start_index=previous_target,
                batch_size=target_total - previous_target,
                should_run=target_total > int(completed_target),
            )
        )
        previous_target = target_total
    return tuple(targets)


def plan_output_paths(
    *,
    output_dir: str | Path,
    temp_dir: str | Path,
    mode: str,
    sample_count: int,
    timestamp: str,
) -> OutputPaths:
    normalized_output_dir = str(Path(output_dir))
    normalized_temp_dir = str(Path(temp_dir))
    run_prefix = f"{mode}_{int(sample_count)}_{timestamp}"
    result_csv = str(Path(normalized_output_dir) / f"swine_disease_dataset_{mode}_{timestamp}.csv")
    summary_csv = (
        str(Path(normalized_output_dir) / f"pilot_model_comparison_{timestamp}.csv")
        if str(mode).lower() == "pilot"
        else ""
    )
    return OutputPaths(
        timestamp=timestamp,
        run_prefix=run_prefix,
        output_dir=normalized_output_dir,
        temp_dir=normalized_temp_dir,
        log_file=str(Path(normalized_output_dir) / f"{run_prefix}.log"),
        error_log_file=str(Path(normalized_output_dir) / f"{run_prefix}.err.log"),
        result_csv=result_csv,
        summary_csv=summary_csv,
        latest_snapshot_file=str(Path(normalized_temp_dir) / "latest_progress_snapshot.json"),
    )


def build_pipeline_runtime_plan(
    *,
    mode: str,
    cli_samples: int = 0,
    cli_parallel: int = 0,
    raw_milestones: str = "",
    evaluation_mode: str = "legacy",
    generator_key: str = "",
    resume_from: str = "",
    config: Mapping[str, Any] | None = None,
    output_dir: str | Path,
    temp_dir: str | Path,
    timestamp: str,
    resume_state: Mapping[str, Any] | None = None,
    default_parallel: int = 1,
) -> PipelineRuntimePlan:
    options = normalize_runtime_options(
        mode=mode,
        cli_samples=cli_samples,
        cli_parallel=cli_parallel,
        raw_milestones=raw_milestones,
        evaluation_mode=evaluation_mode,
        generator_key=generator_key,
        resume_from=resume_from,
        config=config,
        default_parallel=default_parallel,
    )
    normalized_resume = normalize_resume_state(
        resume_state,
        snapshot_path=resume_from,
        fallback_mode=options.mode,
        fallback_sample_count=options.sample_count,
    )
    effective_completed_target = normalized_resume.completed_target if normalized_resume else 0
    stage_targets = build_stage_targets(
        options.mode,
        options.sample_count,
        milestones=options.milestones,
        completed_target=effective_completed_target,
    )
    output_paths = plan_output_paths(
        output_dir=output_dir,
        temp_dir=temp_dir,
        mode=options.mode,
        sample_count=options.sample_count,
        timestamp=timestamp,
    )
    return PipelineRuntimePlan(
        options=options,
        resume_state=normalized_resume,
        stage_targets=stage_targets,
        output_paths=output_paths,
    )


def prepare_pipeline_execution_context(plan: PipelineRuntimePlan) -> PipelineExecutionContext:
    execution_state = initialize_execution_state(plan.resume_state)
    return PipelineExecutionContext(
        options=plan.options,
        resume_state=plan.resume_state,
        execution_state=execution_state,
        stage_targets=plan.stage_targets,
        output_paths=plan.output_paths,
    )


def plan_stage_batch(
    stage_target: StageTarget,
    tasks: Sequence[Any],
    *,
    completed_indexes: Iterable[int] | None = None,
    completed_target: int = 0,
) -> StageBatchPlan:
    normalized_tasks = tuple(tasks)
    normalized_completed_indexes = frozenset(int(value) for value in (completed_indexes or ()))
    pending_tasks = tuple(filter_runtime_pending_tasks(normalized_tasks, normalized_completed_indexes))
    completed_target_before = max(int(completed_target), 0)
    completed_target_after = max(completed_target_before, int(stage_target.target_total))
    return StageBatchPlan(
        stage_target=stage_target,
        raw_tasks=normalized_tasks,
        pending_tasks=pending_tasks,
        completed_indexes=normalized_completed_indexes,
        completed_target_before=completed_target_before,
        completed_target_after=completed_target_after,
        should_skip=not pending_tasks,
    )


def build_stage_completion_plan(
    stage_batch_plan: StageBatchPlan,
    stage_results: Sequence[Any],
    results: Sequence[Mapping[str, Any]],
) -> StageCompletionPlan:
    return StageCompletionPlan(
        stage_target=stage_batch_plan.stage_target,
        completed_target_before=stage_batch_plan.completed_target_before,
        completed_target_after=stage_batch_plan.completed_target_after,
        stage_result_count=len(tuple(stage_results)),
        total_result_count=len(tuple(results)),
        snapshot_target_hint=stage_batch_plan.stage_target.target_total,
    )


def initialize_execution_state(resume_state: ResumeState | None) -> ExecutionState:
    if not resume_state:
        return ExecutionState(
            results=[],
            completed_target=0,
            completed_indexes=set(),
        )

    return ExecutionState(
        results=[dict(item) for item in resume_state.results],
        completed_target=int(resume_state.completed_target),
        completed_indexes=set(resume_state.completed_indexes),
    )


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _coerce_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default)


def _coerce_optional_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


__all__ = [
    "OutputPaths",
    "ExecutionState",
    "PipelineExecutionContext",
    "PipelineRuntimePlan",
    "ResumeState",
    "RuntimeOptions",
    "StageTarget",
    "StageBatchPlan",
    "StageCompletionPlan",
    "build_pipeline_runtime_plan",
    "build_stage_targets",
    "build_stage_completion_plan",
    "initialize_execution_state",
    "normalize_resume_state",
    "normalize_runtime_options",
    "plan_output_paths",
    "plan_stage_batch",
    "prepare_pipeline_execution_context",
]
