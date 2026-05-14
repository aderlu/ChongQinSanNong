from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from multiprocessing import Pool
from typing import Any, Callable, Mapping, Sequence, TypeVar


TaskT = TypeVar("TaskT")
ResultRow = dict[str, Any]


@dataclass(slots=True)
class BatchExecutionSettings:
    progress_log_every: int
    snapshot_every: int
    dispatch_chunk_size: int
    worker_max_cases_per_child: int
    max_failures: int


@dataclass(slots=True)
class BatchExecutionResult:
    stage_results: list[ResultRow]
    failure_count: int
    aborted: bool = False


def chunk_tasks(tasks: Sequence[TaskT], chunk_size: int) -> list[list[TaskT]]:
    normalized_chunk_size = max(int(chunk_size), 1)
    return [
        list(tasks[start:start + normalized_chunk_size])
        for start in range(0, len(tasks), normalized_chunk_size)
    ]


def execute_task_batch(
    tasks: Sequence[TaskT],
    worker: Callable[[TaskT], Mapping[str, Any]],
    all_results: list[ResultRow],
    *,
    parallel_count: int,
    settings: BatchExecutionSettings,
    started_at: datetime,
    sample_count: int,
    log_message: Callable[[str, bool], None],
    build_failure_message: Callable[[Mapping[str, Any]], str],
    build_progress_message: Callable[[int, int, Sequence[Mapping[str, Any]], datetime, int], str],
    save_snapshot: Callable[[Sequence[Mapping[str, Any]]], None] | None = None,
    pool_factory: Callable[..., Any] = Pool,
) -> BatchExecutionResult:
    stage_results: list[ResultRow] = []
    failure_count = 0
    batch_size = len(tasks)

    if batch_size == 0:
        return BatchExecutionResult(stage_results=stage_results, failure_count=failure_count, aborted=False)

    dispatch_chunks = chunk_tasks(tasks, settings.dispatch_chunk_size)
    for chunk_index, task_chunk in enumerate(dispatch_chunks, 1):
        log_message(
            f"    [分发块 {chunk_index}/{len(dispatch_chunks)}] 本块 {len(task_chunk)} 条 | "
            f"并发 {parallel_count} | 每个子进程处理 {settings.worker_max_cases_per_child} 条后重建"
        )
        with pool_factory(processes=parallel_count, maxtasksperchild=settings.worker_max_cases_per_child) as pool:
            for raw_result in pool.imap_unordered(worker, task_chunk, chunksize=1):
                result = dict(raw_result)
                stage_results.append(result)
                all_results.append(result)

                if not result.get("success"):
                    failure_count += 1
                    log_message(build_failure_message(result), True)

                processed_in_stage = len(stage_results)
                if _should_emit_progress(processed_in_stage, batch_size, settings.progress_log_every):
                    log_message(
                        build_progress_message(
                            processed_in_stage,
                            batch_size,
                            all_results,
                            started_at,
                            sample_count,
                        )
                    )

                if save_snapshot and _should_emit_progress(processed_in_stage, batch_size, settings.snapshot_every):
                    save_snapshot(all_results)

                if failure_count >= settings.max_failures:
                    log_message(f"[STOP] 当前批次失败次数达到 {settings.max_failures}，提前停止该批次。", True)
                    terminate = getattr(pool, "terminate", None)
                    if callable(terminate):
                        terminate()
                    return BatchExecutionResult(
                        stage_results=stage_results,
                        failure_count=failure_count,
                        aborted=True,
                    )

        log_message(f"    [分发块完成] 已处理 {len(stage_results)}/{batch_size} 条")

    return BatchExecutionResult(stage_results=stage_results, failure_count=failure_count, aborted=False)


def _should_emit_progress(processed: int, total: int, every: int) -> bool:
    normalized_every = max(int(every), 1)
    return processed % normalized_every == 0 or processed == total


__all__ = [
    "BatchExecutionResult",
    "BatchExecutionSettings",
    "chunk_tasks",
    "execute_task_batch",
]
