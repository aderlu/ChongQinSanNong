from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from chicken_data_synthesis.application.services.benchmark_planning import build_benchmark_combinations


@dataclass(frozen=True)
class BenchmarkPlanningInput:
    config: Mapping[str, Any]
    cases_payload: Mapping[str, Any]
    output_dir: str | Path
    timestamp: str


@dataclass(frozen=True)
class BenchmarkCombination:
    combination_key: str
    generator_key: str
    judge_keys: tuple[str, str, str]


@dataclass(frozen=True)
class BenchmarkDataset:
    dataset_key: str
    dataset_name: str
    benchmark_style: str
    task_type: str
    cases: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class BenchmarkOutputPaths:
    timestamp: str
    detail_csv: str
    summary_csv: str


@dataclass(frozen=True)
class BenchmarkWorkItem:
    case_id: str
    benchmark_style: str
    task_type: str
    dataset_key: str
    dataset_name: str
    combination_key: str
    generator_key: str
    judge_keys: tuple[str, str, str]
    sample_index: int
    case_seed: Mapping[str, Any]


@dataclass(frozen=True)
class BenchmarkExecutionPlan:
    base_url: str
    request_interval: float
    samples_per_generator: int
    output_paths: BenchmarkOutputPaths
    datasets: tuple[BenchmarkDataset, ...]
    combinations: tuple[BenchmarkCombination, ...]
    work_items: tuple[BenchmarkWorkItem, ...]


@dataclass(frozen=True)
class BenchmarkRunResult:
    detail_csv: str
    summary_csv: str
    detail_rows: tuple[Mapping[str, Any], ...]
    summary_rows: tuple[Mapping[str, Any], ...]
    processed_cases: int
    dataset_count: int
    combination_count: int


def build_benchmark_planning_input(
    config: Mapping[str, Any],
    cases_payload: Mapping[str, Any],
    output_dir: str | Path,
    timestamp: str,
) -> BenchmarkPlanningInput:
    return BenchmarkPlanningInput(
        config=config,
        cases_payload=cases_payload,
        output_dir=output_dir,
        timestamp=timestamp,
    )


def normalize_benchmark_case_seed(
    seed: Mapping[str, Any],
    dataset: Mapping[str, Any],
    sample_index: int,
) -> dict[str, Any]:
    normalized = dict(seed)
    normalized["sample_index"] = sample_index
    normalized["benchmark_style"] = normalized.get(
        "benchmark_style",
        dataset.get("benchmark_style", "legacy_case_benchmark"),
    )
    normalized["task_type"] = normalized.get("task_type", dataset.get("task_type", "case_generation"))
    normalized["instance_id"] = normalized.get(
        "instance_id",
        f"{dataset.get('dataset_key', 'dataset')}-{sample_index:03d}",
    )
    normalized.setdefault("disease_name", normalized.get("title", "未命名病例"))
    normalized.setdefault("scenario_hint", normalized.get("context", ""))
    normalized.setdefault("problem_statement", normalized.get("issue", ""))
    if "acceptance_criteria" not in normalized:
        normalized["acceptance_criteria"] = normalized.get("checks", [])
    return normalized


def normalize_benchmark_combination(raw: Mapping[str, Any], fallback_index: int = 1) -> BenchmarkCombination:
    judge_keys = [str(item).strip() for item in raw.get("judge_keys", ()) if str(item).strip()]
    while len(judge_keys) < 3:
        judge_keys.append("")
    combination_key = str(raw.get("combination_key") or f"combo_{fallback_index}")
    return BenchmarkCombination(
        combination_key=combination_key,
        generator_key=str(raw["generator_key"]),
        judge_keys=(judge_keys[0], judge_keys[1], judge_keys[2]),
    )


def normalize_benchmark_dataset(raw: Mapping[str, Any], fallback_index: int = 1) -> BenchmarkDataset:
    dataset_key = str(raw.get("dataset_key") or f"dataset_{fallback_index}")
    dataset_name = str(raw.get("dataset_name") or dataset_key)
    benchmark_style = str(raw.get("benchmark_style") or "legacy_case_benchmark")
    task_type = str(raw.get("task_type") or "case_generation")
    cases = tuple(dict(case) for case in raw.get("cases", ()))
    if not cases:
        raise ValueError(f"Dataset '{dataset_key}' has no cases")
    return BenchmarkDataset(
        dataset_key=dataset_key,
        dataset_name=dataset_name,
        benchmark_style=benchmark_style,
        task_type=task_type,
        cases=cases,
    )


def build_benchmark_datasets_from_payload(
    cases_payload: Mapping[str, Any],
    samples_per_generator: int,
) -> tuple[BenchmarkDataset, ...]:
    datasets_payload = cases_payload.get("datasets")
    if datasets_payload:
        datasets: list[BenchmarkDataset] = []
        for index, dataset in enumerate(datasets_payload, start=1):
            source_items = list(dataset.get("cases", ())) or list(dataset.get("instances", ()))
            if not source_items:
                continue
            expanded_cases = tuple(
                normalize_benchmark_case_seed(
                    source_items[seed_index % len(source_items)],
                    dataset,
                    seed_index + 1,
                )
                for seed_index in range(max(int(samples_per_generator), 0))
            )
            if not expanded_cases:
                continue
            datasets.append(
                normalize_benchmark_dataset(
                    {
                        "dataset_key": dataset.get("dataset_key", f"dataset_{index}"),
                        "dataset_name": dataset.get("dataset_name", dataset.get("dataset_key", "dataset")),
                        "benchmark_style": dataset.get(
                            "benchmark_style",
                            cases_payload.get("benchmark_style", "legacy_case_benchmark"),
                        ),
                        "task_type": dataset.get("task_type", cases_payload.get("task_type", "case_generation")),
                        "cases": expanded_cases,
                    },
                    fallback_index=index,
                )
            )
        if not datasets:
            raise ValueError("No cases found in datasets")
        return tuple(datasets)

    cases = list(cases_payload.get("cases", ()))
    if not cases:
        raise ValueError("No cases found in sample_cases.json")

    expanded_cases = tuple(
        normalize_benchmark_case_seed(
            cases[seed_index % len(cases)],
            {
                "dataset_key": "default",
                "benchmark_style": cases_payload.get("benchmark_style", "legacy_case_benchmark"),
                "task_type": cases_payload.get("task_type", "case_generation"),
            },
            seed_index + 1,
        )
        for seed_index in range(max(int(samples_per_generator), 0))
    )
    if not expanded_cases:
        raise ValueError("No cases found in sample_cases.json")
    return (
        normalize_benchmark_dataset(
            {
                "dataset_key": "default",
                "dataset_name": "default",
                "benchmark_style": cases_payload.get("benchmark_style", "legacy_case_benchmark"),
                "task_type": cases_payload.get("task_type", "case_generation"),
                "cases": expanded_cases,
            }
        ),
    )


def build_benchmark_output_paths(output_dir: str | Path, timestamp: str) -> BenchmarkOutputPaths:
    root = Path(output_dir)
    return BenchmarkOutputPaths(
        timestamp=timestamp,
        detail_csv=str(root / f"candidate_benchmark_detail_{timestamp}.csv"),
        summary_csv=str(root / f"candidate_benchmark_summary_{timestamp}.csv"),
    )


def build_benchmark_work_items(
    datasets: Sequence[BenchmarkDataset],
    combinations: Sequence[BenchmarkCombination],
) -> tuple[BenchmarkWorkItem, ...]:
    items: list[BenchmarkWorkItem] = []
    for dataset in datasets:
        for combination in combinations:
            for offset, case_seed in enumerate(dataset.cases, start=1):
                sample_index = _coerce_sample_index(case_seed, offset)
                case_id = (
                    f"{combination.combination_key}-"
                    f"{dataset.dataset_key}-"
                    f"{sample_index:03d}"
                )
                items.append(
                    BenchmarkWorkItem(
                        case_id=case_id,
                        benchmark_style=str(case_seed.get("benchmark_style") or dataset.benchmark_style),
                        task_type=str(case_seed.get("task_type") or dataset.task_type),
                        dataset_key=dataset.dataset_key,
                        dataset_name=dataset.dataset_name,
                        combination_key=combination.combination_key,
                        generator_key=combination.generator_key,
                        judge_keys=combination.judge_keys,
                        sample_index=sample_index,
                        case_seed=case_seed,
                    )
                )
    return tuple(items)


def build_benchmark_execution_plan(
    config: Mapping[str, Any],
    prepared_datasets: Iterable[Mapping[str, Any]],
    output_dir: str | Path,
    timestamp: str,
) -> BenchmarkExecutionPlan:
    benchmark_cfg = config["benchmark"]
    datasets = tuple(
        normalize_benchmark_dataset(dataset, fallback_index=index)
        for index, dataset in enumerate(prepared_datasets, start=1)
    )
    combinations = tuple(
        normalize_benchmark_combination(item, fallback_index=index)
        for index, item in enumerate(build_benchmark_combinations(config), start=1)
    )
    output_paths = build_benchmark_output_paths(output_dir, timestamp)
    work_items = build_benchmark_work_items(datasets, combinations)
    return BenchmarkExecutionPlan(
        base_url=str(config["api"]["base_url"]),
        request_interval=float(config.get("request_interval", 0.5)),
        samples_per_generator=max(0, int(benchmark_cfg.get("samples_per_generator", 0))),
        output_paths=output_paths,
        datasets=datasets,
        combinations=combinations,
        work_items=work_items,
    )


def build_benchmark_execution_plan_from_payload(
    config: Mapping[str, Any],
    cases_payload: Mapping[str, Any],
    output_dir: str | Path,
    timestamp: str,
) -> BenchmarkExecutionPlan:
    benchmark_cfg = config["benchmark"]
    samples_per_generator = max(0, int(benchmark_cfg.get("samples_per_generator", 0)))
    datasets = build_benchmark_datasets_from_payload(cases_payload, samples_per_generator)
    combinations = tuple(
        normalize_benchmark_combination(item, fallback_index=index)
        for index, item in enumerate(build_benchmark_combinations(config), start=1)
    )
    output_paths = build_benchmark_output_paths(output_dir, timestamp)
    work_items = build_benchmark_work_items(datasets, combinations)
    return BenchmarkExecutionPlan(
        base_url=str(config["api"]["base_url"]),
        request_interval=float(config.get("request_interval", 0.5)),
        samples_per_generator=samples_per_generator,
        output_paths=output_paths,
        datasets=datasets,
        combinations=combinations,
        work_items=work_items,
    )


def build_benchmark_run_result(
    plan: BenchmarkExecutionPlan,
    detail_rows: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
) -> BenchmarkRunResult:
    return BenchmarkRunResult(
        detail_csv=plan.output_paths.detail_csv,
        summary_csv=plan.output_paths.summary_csv,
        detail_rows=tuple(detail_rows),
        summary_rows=tuple(summary_rows),
        processed_cases=len(detail_rows),
        dataset_count=len(plan.datasets),
        combination_count=len(plan.combinations),
    )


def _coerce_sample_index(case_seed: Mapping[str, Any], fallback_index: int) -> int:
    try:
        value = int(case_seed.get("sample_index", fallback_index))
    except (TypeError, ValueError):
        value = fallback_index
    return max(1, value)
