"""Benchmark combination planning services."""

from __future__ import annotations

import itertools
from typing import Any, Dict, Iterable, List, Mapping, Sequence


MAX_JUDGE_SLOTS = 3
DEFAULT_JUDGE_SLOTS = 2


def normalize_judge_slots(value: Any, *, default: int = DEFAULT_JUDGE_SLOTS, max_slots: int = MAX_JUDGE_SLOTS) -> int:
    """Clamp judge slots into the supported range."""
    try:
        slots = int(value)
    except (TypeError, ValueError):
        slots = default
    return max(1, min(slots, max_slots))


def pad_judge_keys(judge_keys: Sequence[str], *, width: int = MAX_JUDGE_SLOTS) -> List[str]:
    """Pad judge keys to a fixed width for downstream CSV compatibility."""
    padded = list(judge_keys[:width])
    while len(padded) < width:
        padded.append("")
    return padded


def build_explicit_benchmark_combinations(
    combinations: Iterable[Mapping[str, Any]],
    *,
    default_prefix: str = "combo_",
) -> List[Dict[str, Any]]:
    """Build combinations from explicit config entries, skipping empty judge groups."""
    planned: List[Dict[str, Any]] = []
    for index, item in enumerate(combinations, start=1):
        judge_keys = list(item.get("judge_keys", []))
        if not judge_keys:
            continue
        planned.append(
            {
                "combination_key": item.get("combination_key", f"{default_prefix}{index}"),
                "generator_key": item["generator_key"],
                "judge_keys": pad_judge_keys(judge_keys),
            }
        )
    return planned


def build_generated_benchmark_combinations(
    generator_keys: Sequence[str],
    evaluator_keys: Sequence[str],
    *,
    judge_slots: Any = DEFAULT_JUDGE_SLOTS,
) -> List[Dict[str, Any]]:
    """Expand generator and evaluator keys into benchmark combinations."""
    resolved_slots = normalize_judge_slots(judge_slots)
    combinations: List[Dict[str, Any]] = []
    for generator_key in generator_keys:
        for judge_group in itertools.combinations(evaluator_keys, resolved_slots):
            combinations.append(
                {
                    "combination_key": f"{generator_key}__{'__'.join(judge_group)}",
                    "generator_key": generator_key,
                    "judge_keys": pad_judge_keys(judge_group),
                }
            )
    return combinations


def build_benchmark_combinations(config: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """Plan benchmark combinations using explicit combos first, then cartesian expansion."""
    benchmark_cfg = config["benchmark"]
    explicit = benchmark_cfg.get("combinations", [])
    if explicit:
        return build_explicit_benchmark_combinations(explicit)

    generators = benchmark_cfg["generator_candidates"]
    evaluators = benchmark_cfg["evaluator_candidates"]
    generator_keys = list(benchmark_cfg.get("generator_keys", generators.keys()))
    evaluator_keys = list(benchmark_cfg.get("evaluator_keys", evaluators.keys()))
    return build_generated_benchmark_combinations(
        generator_keys,
        evaluator_keys,
        judge_slots=benchmark_cfg.get("judge_slots", DEFAULT_JUDGE_SLOTS),
    )
