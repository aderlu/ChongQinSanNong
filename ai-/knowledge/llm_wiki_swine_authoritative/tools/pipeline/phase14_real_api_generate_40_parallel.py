from __future__ import annotations

import argparse
import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = Path(__file__).resolve().parent
TZ = timezone(timedelta(hours=8))
DEFAULT_DATE = datetime.now(TZ).strftime("%Y%m%d")
DEFAULT_OUTPUT_TAG = "cn_real40_parallel8"


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def load_module(filename: str, module_name: str) -> Any:
    path = TOOLS_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            item = json.loads(line.lstrip("\ufeff"))
            if isinstance(item, dict):
                rows.append(item)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def latest_jsonl(directory: Path, prefix: str) -> Path:
    files = sorted(directory.glob(f"{prefix}_*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {directory}")
    return files[0]


def resolve_path(value: str, root: Path, default_dir: Path, prefix: str) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    return latest_jsonl(default_dir, prefix)


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def balanced_skeletons(
    skeletons: list[dict[str, Any]],
    plans: list[dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    plan_map = {str(plan.get("plan_id")): plan for plan in plans if plan.get("plan_id")}
    buckets: dict[str, list[dict[str, Any]]] = {}
    for skeleton in skeletons:
        plan = plan_map.get(str(skeleton.get("plan_id"))) or {}
        layer = str(plan.get("ability_layer") or skeleton.get("ability_layer") or "")
        buckets.setdefault(layer, []).append(skeleton)

    order = [
        "L1_retrieval_grounded",
        "L2_diagnosis_support",
        "L3_differential_support",
        "L4_control_boundary",
        "L5_drug_boundary_negative",
        "L6_regulatory_guardrail",
        "L7_judge_calibration",
    ]
    selected: list[dict[str, Any]] = []
    cursor = 0
    while len(selected) < limit:
        progressed = False
        for layer in order:
            bucket = buckets.get(layer, [])
            if cursor < len(bucket):
                selected.append(bucket[cursor])
                progressed = True
                if len(selected) >= limit:
                    break
        if not progressed:
            break
        cursor += 1
    return selected


def chunked(rows: list[dict[str, Any]], chunk_size: int) -> list[list[dict[str, Any]]]:
    return [rows[index : index + chunk_size] for index in range(0, len(rows), chunk_size)]


def build_llm_client(phase14: Any, args: argparse.Namespace) -> Any:
    return phase14.build_llm_client(
        argparse.Namespace(
            mode=phase14.REAL_API_MODE,
            base_url=args.base_url,
            model=args.model,
            api_key=args.api_key,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
    )


def run_chunk(
    *,
    worker_index: int,
    skeleton_chunk: list[dict[str, Any]],
    plan_map: dict[str, dict[str, Any]],
    phase14: Any,
    args: argparse.Namespace,
    offset: int,
) -> dict[str, Any]:
    llm_client = build_llm_client(phase14, args)
    samples: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for local_index, skeleton in enumerate(skeleton_chunk, start=1):
        global_index = offset + local_index
        plan = plan_map.get(str(skeleton.get("plan_id"))) or {}
        sample_id = f"GEN-P8-{global_index:06d}"
        try:
            sample = phase14.generate_sample(
                sample_id=sample_id,
                skeleton=skeleton,
                plan=plan,
                mode=phase14.REAL_API_MODE,
                llm_client=llm_client,
            )
            if sample is None:
                failures.append(
                    {
                        "worker": worker_index,
                        "sample_id": sample_id,
                        "plan_id": skeleton.get("plan_id", ""),
                        "reason": "generate_sample_returned_none",
                    }
                )
                continue
            sample["parallel_worker"] = worker_index
            samples.append(sample)
        except Exception as exc:
            failures.append(
                {
                    "worker": worker_index,
                    "sample_id": sample_id,
                    "plan_id": skeleton.get("plan_id", ""),
                    "reason": type(exc).__name__,
                    "message": str(exc)[:500],
                }
            )
    return {"worker": worker_index, "samples": samples, "failures": failures}


def summarize(
    *,
    samples: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    skeleton_path: Path,
    plan_path: Path,
    output_path: Path,
    root: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    ability_layer_counts: dict[str, int] = {}
    worker_counts: dict[str, int] = {}
    fallback_samples: list[str] = []
    generation_errors: list[dict[str, Any]] = []
    for sample in samples:
        layer = str(sample.get("ability_layer") or "")
        worker = str(sample.get("parallel_worker") or "")
        ability_layer_counts[layer] = ability_layer_counts.get(layer, 0) + 1
        worker_counts[worker] = worker_counts.get(worker, 0) + 1
        if sample.get("generation_fallback"):
            fallback_samples.append(str(sample.get("sample_id") or ""))
        if sample.get("generation_error"):
            generation_errors.append(
                {
                    "sample_id": sample.get("sample_id", ""),
                    "generation_error": sample.get("generation_error", ""),
                }
            )

    return {
        "generated_at": now(),
        "phase": "phase14_real_api_generate_40_parallel",
        "mode": "real-api",
        "parallel_workers": args.parallel,
        "requested": args.limit,
        "generated": len(samples),
        "failed": len(failures),
        "generation_model": args.model,
        "prompt_version": getattr(load_module("phase14_generate_two_stage_samples.py", "phase14_meta"), "PROMPT_VERSION"),
        "input_skeletons": relative(skeleton_path, root),
        "input_plan": relative(plan_path, root),
        "output": relative(output_path, root),
        "ability_layer_counts": dict(sorted(ability_layer_counts.items())),
        "worker_counts": dict(sorted(worker_counts.items())),
        "fallback_samples": fallback_samples,
        "generation_errors": generation_errors,
        "failures": failures,
        "passed": len(samples) == args.limit and not failures,
    }


def write_report(summary: dict[str, Any], report_json: Path, report_md: Path) -> None:
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Phase 14 Real API Parallel Generation",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Requested: {summary['requested']}",
        f"- Generated samples: {summary['generated']}",
        f"- Failed samples: {summary['failed']}",
        f"- Workers: {summary['parallel_workers']}",
        f"- Model: {summary['generation_model']}",
        f"- Passed: {summary['passed']}",
        "",
        "## Ability Layers",
        "",
    ]
    for key, value in summary["ability_layer_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Worker Counts", ""])
    for key, value in summary["worker_counts"].items():
        lines.append(f"- worker_{key}: {value}")
    if summary["failures"]:
        lines.extend(["", "## Failures", ""])
        for item in summary["failures"][:20]:
            lines.append(f"- {item}")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run 8-way parallel real API generation for 40 wiki-first samples.")
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default=DEFAULT_DATE)
    parser.add_argument("--tag", default=DEFAULT_OUTPUT_TAG)
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--parallel", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=5)
    parser.add_argument("--skeletons", default="")
    parser.add_argument("--plan", default="")
    parser.add_argument("--base-url", default="")
    parser.add_argument("--model", default="hunyuan-turbos-20250926")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=int, default=90)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.wiki_root.resolve()
    exports = root / "exports"
    issues = root / "issues" / "wiki_first_generation_reports"
    skeleton_path = resolve_path(args.skeletons, root, exports / "answer_skeletons", "wiki_answer_skeletons")
    plan_path = resolve_path(args.plan, root, exports / "planned_samples", "wiki_sample_plan")

    phase14 = load_module("phase14_generate_two_stage_samples.py", "phase14_generate_two_stage_samples")
    skeletons = read_jsonl(skeleton_path)
    plans = read_jsonl(plan_path)
    selected = balanced_skeletons(skeletons, plans, args.limit)
    if len(selected) < args.limit:
        raise RuntimeError(f"Requested {args.limit} samples, but only selected {len(selected)} skeletons.")
    plan_map = {str(plan.get("plan_id")): plan for plan in plans if plan.get("plan_id")}

    chunks = chunked(selected, args.chunk_size)
    chunks = chunks[: args.parallel]
    if sum(len(chunk) for chunk in chunks) < args.limit:
        raise RuntimeError("Chunking produced fewer samples than requested.")

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = []
        offset = 0
        for worker_index, skeleton_chunk in enumerate(chunks, start=1):
            futures.append(
                executor.submit(
                    run_chunk,
                    worker_index=worker_index,
                    skeleton_chunk=skeleton_chunk,
                    plan_map=plan_map,
                    phase14=phase14,
                    args=args,
                    offset=offset,
                )
            )
            offset += len(skeleton_chunk)
        for future in as_completed(futures):
            results.append(future.result())

    samples = sorted(
        [sample for result in results for sample in result["samples"]],
        key=lambda item: str(item.get("sample_id") or ""),
    )
    failures = sorted(
        [failure for result in results for failure in result["failures"]],
        key=lambda item: (str(item.get("worker") or ""), str(item.get("sample_id") or "")),
    )

    output_path = exports / "generated_samples" / f"two_stage_samples_{args.date}_{args.tag}.jsonl"
    write_jsonl(output_path, samples)
    summary = summarize(
        samples=samples,
        failures=failures,
        skeleton_path=skeleton_path,
        plan_path=plan_path,
        output_path=output_path,
        root=root,
        args=args,
    )
    write_report(
        summary,
        issues / f"phase14_parallel_generation_{args.date}_{args.tag}.json",
        issues / f"phase14_parallel_generation_{args.date}_{args.tag}.md",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
