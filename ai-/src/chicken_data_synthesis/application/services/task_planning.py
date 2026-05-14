from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any, TypeVar


TaskT = TypeVar("TaskT")


def filter_pending_tasks(
    tasks: Sequence[TaskT],
    completed_indexes: set[int] | Sequence[int],
    *,
    index_getter: Callable[[TaskT], Any] | None = None,
) -> list[TaskT]:
    completed = {int(value) for value in completed_indexes}
    if not completed:
        return list(tasks)

    resolved_getter = index_getter or _default_task_index_getter
    return [
        task
        for task in tasks
        if int(resolved_getter(task)) not in completed
    ]


def resolve_parallel_count(
    mode: str,
    cli_parallel: int,
    *,
    pilot_config: Mapping[str, Any] | None = None,
    production_config: Mapping[str, Any] | None = None,
    default_parallel: int = 1,
) -> int:
    if int(cli_parallel) > 0:
        return int(cli_parallel)

    normalized_default = max(int(default_parallel), 1)
    mode_key = "production" if str(mode).lower() == "production" else "pilot"
    selected_config = production_config if mode_key == "production" else pilot_config
    if not isinstance(selected_config, Mapping):
        return normalized_default

    try:
        configured_parallel = int(selected_config.get("parallel", normalized_default))
    except (TypeError, ValueError):
        return normalized_default
    return max(configured_parallel, 1)


def resolve_milestones(
    sample_count: int,
    raw_milestones: str | None = None,
    *,
    production_config: Mapping[str, Any] | None = None,
    ensure_terminal: bool = True,
) -> list[int]:
    normalized_sample_count = int(sample_count)
    if normalized_sample_count <= 0:
        return []

    if raw_milestones and raw_milestones.strip():
        source_values: Sequence[Any] = [
            item.strip()
            for item in raw_milestones.split(",")
            if item.strip()
        ]
    else:
        configured_values = []
        if isinstance(production_config, Mapping):
            configured_values = production_config.get("milestones", []) or []
        source_values = list(configured_values)

    normalized_values = sorted(
        {
            int(value)
            for value in source_values
            if _is_valid_milestone_value(value, normalized_sample_count)
        }
    )

    if ensure_terminal and normalized_sample_count not in normalized_values:
        normalized_values.append(normalized_sample_count)
    return normalized_values


def build_case_tasks(
    *,
    mode: str,
    start_index: int,
    sample_count: int,
    evaluation_mode: str,
    diseases: Sequence[str],
    pilot_config: Mapping[str, Any] | None = None,
    candidate_models: Mapping[str, Mapping[str, Any]] | None = None,
    default_models: Mapping[str, Mapping[str, Any]] | None = None,
    disease_picker: Callable[[Sequence[str]], Any] | None = None,
) -> list[tuple[Any, ...]]:
    normalized_mode = "production" if str(mode).lower() == "production" else "pilot"
    normalized_sample_count = max(int(sample_count), 0)
    if normalized_sample_count <= 0:
        return []

    disease_values = list(diseases)
    if not disease_values:
        raise ValueError("diseases must not be empty")

    pilot_settings = pilot_config if isinstance(pilot_config, Mapping) else {}
    candidates = candidate_models if isinstance(candidate_models, Mapping) else {}
    defaults = default_models if isinstance(default_models, Mapping) else {}
    picker = disease_picker or (lambda values: values[0])

    judge_keys = list(pilot_settings.get("primary_judges", [])) if normalized_mode == "pilot" else []
    judge_a_config = _resolve_model_config(judge_keys[0] if len(judge_keys) > 0 else "", candidates, defaults, "judge_a")
    judge_b_config = _resolve_model_config(judge_keys[1] if len(judge_keys) > 1 else "", candidates, defaults, "judge_b")
    arbiter_key = str(pilot_settings.get("arbiter", "") or "") if normalized_mode == "pilot" else ""
    arbiter_config = _resolve_model_config(arbiter_key, candidates, defaults, "arbiter")

    if normalized_mode == "pilot":
        tasks: list[tuple[Any, ...]] = []
        task_index = int(start_index)
        for generator_key in pilot_settings.get("generator_candidates", []):
            generator_config = candidates[generator_key]
            for _ in range(normalized_sample_count):
                tasks.append(
                    (
                        task_index,
                        picker(disease_values),
                        generator_key,
                        generator_config,
                        judge_a_config,
                        judge_b_config,
                        arbiter_config,
                        evaluation_mode,
                    )
                )
                task_index += 1
        return tasks

    generator_key = "generator_default"
    generator_config = defaults["generator"]
    return [
        (
            index,
            picker(disease_values),
            generator_key,
            generator_config,
            judge_a_config,
            judge_b_config,
            arbiter_config,
            evaluation_mode,
        )
        for index in range(int(start_index), int(start_index) + normalized_sample_count)
    ]


def _default_task_index_getter(task: TaskT) -> Any:
    if isinstance(task, Mapping):
        return task["index"]
    return task[0]


def _is_valid_milestone_value(value: Any, sample_count: int) -> bool:
    try:
        normalized = int(value)
    except (TypeError, ValueError):
        return False
    return 0 < normalized <= sample_count


def _resolve_model_config(
    candidate_key: str,
    candidate_models: Mapping[str, Mapping[str, Any]],
    default_models: Mapping[str, Mapping[str, Any]],
    default_key: str,
) -> Mapping[str, Any]:
    if candidate_key and candidate_key in candidate_models:
        return candidate_models[candidate_key]
    return default_models[default_key]


__all__ = [
    "build_case_tasks",
    "filter_pending_tasks",
    "resolve_milestones",
    "resolve_parallel_count",
]
