from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Mapping

from chicken_data_synthesis.application.use_cases.pipeline_runtime import (
    PipelineExecutionContext,
    PipelineRuntimePlan,
    build_pipeline_runtime_plan,
    build_stage_completion_plan,
    plan_stage_batch,
    prepare_pipeline_execution_context,
)

PipelineUseCaseInput = PipelineRuntimePlan | PipelineExecutionContext
LogCallable = Callable[[str, bool], None]


@dataclass(frozen=True)
class PipelineUseCaseHooks:
    build_tasks: Callable[[str, int, int, str], Sequence[Any]]
    run_task_batch: Callable[[str, list[Any], list[dict[str, Any]], datetime, int, int, int, list[int] | None], tuple[list[dict[str, Any]], int]]
    save_stage_snapshot: Callable[[str, int, list[dict[str, Any]], int, int, list[int] | None, int], str]
    save_emergency_snapshot: Callable[[str, int, list[dict[str, Any]], int, int, list[int] | None], str]
    write_outputs: Callable[[Sequence[Mapping[str, Any]], str, str | None], Mapping[str, str]]
    summarize_results: Callable[[Sequence[Mapping[str, Any]]], Mapping[str, Any]]
    build_resume_lines: Callable[[str, int, int], Sequence[str]]
    print_header: Callable[[str, int, int, list[int] | None, str], None]
    build_stage_summary_lines: Callable[[int, Sequence[Mapping[str, Any]], Sequence[Mapping[str, Any]]], Sequence[str]]
    build_completion_lines: Callable[[str, Mapping[str, Any], float, str, str, int | None], Sequence[str]]
    filter_pending_tasks: Callable[[Sequence[Any], set[int]], Sequence[Any]] | None
    log: LogCallable
    now: Callable[[], datetime]


@dataclass(frozen=True)
class PipelineUseCaseResult:
    context: PipelineExecutionContext
    result_csv: str
    summary_csv: str
    summary: Mapping[str, Any]
    elapsed_total_seconds: float
    interrupted: bool = False
    error: str = ""


def prepare_pipeline_argv(argv: Sequence[str] | None = None) -> tuple[str, ...] | None:
    """Normalize pipeline CLI arguments before handing them to the script adapter."""

    if argv is None:
        return None
    return tuple(argv)


def prepare_pipeline_use_case_context(
    runtime_input: PipelineUseCaseInput,
) -> PipelineExecutionContext:
    """Normalize a runtime plan or execution context for the application layer."""

    if isinstance(runtime_input, PipelineExecutionContext):
        return runtime_input
    return prepare_pipeline_execution_context(runtime_input)


def build_pipeline_use_case_plan(
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
    """Create a pipeline runtime plan without invoking the legacy CLI bridge."""

    return build_pipeline_runtime_plan(
        mode=mode,
        cli_samples=cli_samples,
        cli_parallel=cli_parallel,
        raw_milestones=raw_milestones,
        evaluation_mode=evaluation_mode,
        generator_key=generator_key,
        resume_from=resume_from,
        config=config,
        output_dir=output_dir,
        temp_dir=temp_dir,
        timestamp=timestamp,
        resume_state=resume_state,
        default_parallel=default_parallel,
    )


def execute_pipeline_use_case(
    runtime_input: PipelineUseCaseInput,
    *,
    hooks: PipelineUseCaseHooks,
) -> PipelineUseCaseResult:
    """Execute a normalized pipeline context through injected orchestration hooks."""

    context = prepare_pipeline_use_case_context(runtime_input)
    mode = context.options.mode
    sample_count = context.options.sample_count
    parallel_count = context.options.parallel_count
    milestones = list(context.options.milestones)
    evaluation_mode = context.options.evaluation_mode
    results = context.execution_state.results
    completed_target = context.execution_state.completed_target
    completed_indexes = context.execution_state.completed_indexes

    if context.resume_state:
        for line in hooks.build_resume_lines(
            context.resume_state.snapshot_path,
            len(results),
            completed_target,
        ):
            hooks.log(str(line), False)

    hooks.print_header(mode, sample_count, parallel_count, milestones, evaluation_mode)
    started_at = hooks.now()

    try:
        if mode == "pilot":
            pilot_target = context.stage_targets[0]
            tasks = list(
                hooks.build_tasks(
                    mode,
                    pilot_target.start_index,
                    pilot_target.batch_size,
                    evaluation_mode,
                )
            )
            if hooks.filter_pending_tasks is not None:
                tasks = list(hooks.filter_pending_tasks(tasks, completed_indexes))
            hooks.log(f"\n[1/4] 已生成任务，共 {len(tasks)} 条待处理", False)
            hooks.log("\n[2/4] 启动并行处理...", False)
            hooks.run_task_batch(
                mode,
                tasks,
                results,
                started_at,
                parallel_count,
                sample_count,
                completed_target,
                milestones,
            )
        else:
            hooks.log("\n[1/4] 生产任务按里程碑分批运行", False)
            for stage_target in context.stage_targets:
                raw_tasks = list(
                    hooks.build_tasks(
                        mode,
                        stage_target.start_index,
                        stage_target.batch_size,
                        evaluation_mode,
                    )
                )
                stage_plan = plan_stage_batch(
                    stage_target,
                    raw_tasks,
                    completed_indexes=completed_indexes,
                    completed_target=completed_target,
                )

                if stage_plan.should_skip:
                    completed_target = stage_plan.completed_target_after
                    hooks.log(f"\n[2/4] 跳过里程碑 {stage_target.target_total}：对应样本已在快照中完成", False)
                    continue

                hooks.log(
                    f"\n[2/4] 开始批次：累计目标 {stage_plan.completed_target_after} 条，本批新增 {len(stage_plan.pending_tasks)} 条",
                    False,
                )
                stage_results, _stage_failures = hooks.run_task_batch(
                    mode,
                    list(stage_plan.pending_tasks),
                    results,
                    started_at,
                    parallel_count,
                    sample_count,
                    stage_plan.completed_target_after,
                    milestones,
                )
                completed_indexes = {int(item.get("index")) for item in results if item.get("index") is not None}
                completion_plan = build_stage_completion_plan(stage_plan, stage_results, results)
                completed_target = completion_plan.completed_target_after
                for line in hooks.build_stage_summary_lines(
                    completion_plan.snapshot_target_hint,
                    stage_results,
                    results,
                ):
                    hooks.log(str(line), False)

                snapshot_path = hooks.save_stage_snapshot(
                    mode,
                    sample_count,
                    results,
                    completed_target,
                    parallel_count,
                    milestones,
                    completion_plan.snapshot_target_hint,
                )
                hooks.log(f"  阶段快照: {snapshot_path}", False)
    except KeyboardInterrupt:
        snapshot_file = hooks.save_emergency_snapshot(
            mode,
            sample_count,
            results,
            completed_target,
            parallel_count,
            milestones,
        )
        hooks.log(f"\n[INTERRUPT] 已写出应急快照: {snapshot_file}", True)
        return PipelineUseCaseResult(
            context=context,
            result_csv=context.output_paths.result_csv,
            summary_csv=context.output_paths.summary_csv,
            summary={},
            elapsed_total_seconds=(hooks.now() - started_at).total_seconds(),
            interrupted=True,
        )
    except Exception as exc:
        snapshot_file = hooks.save_emergency_snapshot(
            mode,
            sample_count,
            results,
            completed_target,
            parallel_count,
            milestones,
        )
        hooks.log(f"\n[ERROR] 运行异常: {exc}", True)
        hooks.log(f"[ERROR] 已写出应急快照: {snapshot_file}", True)
        return PipelineUseCaseResult(
            context=context,
            result_csv=context.output_paths.result_csv,
            summary_csv=context.output_paths.summary_csv,
            summary={},
            elapsed_total_seconds=(hooks.now() - started_at).total_seconds(),
            error=str(exc),
        )

    hooks.log("\n[3/4] 一次性写出最终结果...", False)
    written_artifacts = hooks.write_outputs(
        results,
        context.output_paths.result_csv,
        summary_csv=context.output_paths.summary_csv or None,
    )
    elapsed_total = (hooks.now() - started_at).total_seconds()
    summary = hooks.summarize_results(results)
    for line in hooks.build_completion_lines(
        mode,
        summary,
        elapsed_total,
        str(written_artifacts.get("result_csv", context.output_paths.result_csv)),
        str(written_artifacts.get("summary_csv", context.output_paths.summary_csv or "")),
        sample_count,
    ):
        hooks.log(str(line), False)
    return PipelineUseCaseResult(
        context=context,
        result_csv=str(written_artifacts.get("result_csv", context.output_paths.result_csv)),
        summary_csv=str(written_artifacts.get("summary_csv", context.output_paths.summary_csv or "")),
        summary=summary,
        elapsed_total_seconds=elapsed_total,
    )


def run_pipeline_use_case(
    argv: Sequence[str] | None = None,
    *,
    runtime_input: PipelineUseCaseInput | None = None,
    hooks: PipelineUseCaseHooks | None = None,
) -> PipelineExecutionContext | PipelineUseCaseResult | None:
    """Run the pipeline use case or normalize a runtime plan for downstream execution."""

    if runtime_input is not None:
        if hooks is not None:
            return execute_pipeline_use_case(runtime_input, hooks=hooks)
        return prepare_pipeline_use_case_context(runtime_input)

    from scripts.master_chicken_data import main as pipeline_entrypoint

    prepared_argv = prepare_pipeline_argv(argv)
    pipeline_entrypoint(argv=list(prepared_argv) if prepared_argv is not None else None)
    return None


def run_pipeline_cli(argv: Sequence[str] | None = None) -> None:
    """Run the current production/pilot pipeline through the use-case entrypoint."""

    run_pipeline_use_case(argv=argv)


__all__ = [
    "build_pipeline_use_case_plan",
    "PipelineUseCaseHooks",
    "PipelineUseCaseInput",
    "PipelineUseCaseResult",
    "execute_pipeline_use_case",
    "prepare_pipeline_argv",
    "prepare_pipeline_use_case_context",
    "run_pipeline_cli",
    "run_pipeline_use_case",
]
