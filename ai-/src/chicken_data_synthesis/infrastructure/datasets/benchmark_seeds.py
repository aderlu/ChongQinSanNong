from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List, Mapping


DEFAULT_BENCHMARK_STYLE = "legacy_case_benchmark"
DEFAULT_TASK_TYPE = "case_generation"


def normalize_case_seed(seed: Mapping[str, Any], dataset: Mapping[str, Any], sample_index: int) -> Dict[str, Any]:
    normalized = deepcopy(dict(seed))
    normalized["sample_index"] = sample_index
    normalized["benchmark_style"] = normalized.get(
        "benchmark_style",
        dataset.get("benchmark_style", DEFAULT_BENCHMARK_STYLE),
    )
    normalized["task_type"] = normalized.get(
        "task_type",
        dataset.get("task_type", DEFAULT_TASK_TYPE),
    )
    normalized["instance_id"] = normalized.get(
        "instance_id",
        f"{dataset.get('dataset_key', 'dataset')}-{sample_index:03d}",
    )
    normalized.setdefault("disease_name", normalized.get("title", "未命名病例"))
    normalized.setdefault("scenario_hint", normalized.get("context", ""))
    normalized.setdefault("problem_statement", normalized.get("issue", ""))
    if "acceptance_criteria" not in normalized:
        normalized["acceptance_criteria"] = deepcopy(normalized.get("checks", []))
    return normalized


def expand_case_seeds(
    source_items: Iterable[Mapping[str, Any]],
    dataset: Mapping[str, Any],
    samples_per_generator: int,
) -> List[Dict[str, Any]]:
    seed_list = list(source_items)
    if not seed_list:
        return []
    sample_count = max(0, int(samples_per_generator))
    return [
        normalize_case_seed(seed_list[index % len(seed_list)], dataset, index + 1)
        for index in range(sample_count)
    ]


def normalize_dataset_seed_group(
    dataset: Mapping[str, Any],
    root_payload: Mapping[str, Any],
    samples_per_generator: int,
    dataset_index: int,
) -> Dict[str, Any]:
    cases = list(dataset.get("cases", []))
    instances = list(dataset.get("instances", []))
    source_items = cases or instances
    expanded_cases = expand_case_seeds(source_items, dataset, samples_per_generator)
    return {
        "dataset_key": dataset.get("dataset_key", f"dataset_{dataset_index}"),
        "dataset_name": dataset.get("dataset_name", dataset.get("dataset_key", "dataset")),
        "benchmark_style": dataset.get(
            "benchmark_style",
            root_payload.get("benchmark_style", DEFAULT_BENCHMARK_STYLE),
        ),
        "task_type": dataset.get(
            "task_type",
            root_payload.get("task_type", DEFAULT_TASK_TYPE),
        ),
        "cases": expanded_cases,
    }


def load_dataset_seeds_from_payload(
    payload: Mapping[str, Any],
    samples_per_generator: int,
) -> List[Dict[str, Any]]:
    datasets = list(payload.get("datasets", []))
    if datasets:
        normalized: List[Dict[str, Any]] = []
        for dataset_index, dataset in enumerate(datasets, start=1):
            dataset_group = normalize_dataset_seed_group(
                dataset,
                payload,
                samples_per_generator=samples_per_generator,
                dataset_index=dataset_index,
            )
            if dataset_group["cases"]:
                normalized.append(dataset_group)
        if not normalized:
            raise ValueError("No cases found in datasets")
        return normalized

    cases = list(payload.get("cases", []))
    if not cases:
        raise ValueError("No cases found in sample_cases.json")

    expanded = expand_case_seeds(
        cases,
        {
            "dataset_key": "default",
            "benchmark_style": payload.get("benchmark_style", DEFAULT_BENCHMARK_STYLE),
            "task_type": payload.get("task_type", DEFAULT_TASK_TYPE),
        },
        samples_per_generator=samples_per_generator,
    )
    return [
        {
            "dataset_key": "default",
            "dataset_name": "default",
            "benchmark_style": payload.get("benchmark_style", DEFAULT_BENCHMARK_STYLE),
            "task_type": payload.get("task_type", DEFAULT_TASK_TYPE),
            "cases": expanded,
        }
    ]


__all__ = [
    "DEFAULT_BENCHMARK_STYLE",
    "DEFAULT_TASK_TYPE",
    "expand_case_seeds",
    "load_dataset_seeds_from_payload",
    "normalize_case_seed",
    "normalize_dataset_seed_group",
]
