#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楦＄梾榛勯噾鏁版嵁闆嗘瀯寤鸿剼鏈?
鏀寔涓ょ妯″紡锛?1. pilot: 鍊欓€夋墽琛屾ā鍨嬪皬鏍锋湰璇曡窇
2. production: 鍗曚竴鎵ц妯″瀷鎸夐噷绋嬬鍒嗘壒鐢熶骇
"""

import argparse
import json
import os
import random
import shutil
import sys
import time
import traceback
from collections.abc import Sequence
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from chicken_data_synthesis.application.services import (
    BatchExecutionSettings,
    arbitrate_case_with_fallbacks,
    build_case_tasks,
    build_completion_summary_context,
    build_completion_visible_metadata as build_generation_completion_visible_metadata,
    build_batch_progress_message,
    build_failure_log_message,
    build_stage_summary_context,
    build_stage_summary_lines_from_context,
    evaluate_case_with_fallbacks,
    evaluate_rule_base_case,
    execute_task_batch,
    filter_pending_tasks as filter_runtime_pending_tasks,
    normalize_judge_result,
    resolve_evaluation_mode as resolve_pipeline_evaluation_mode,
    run_generation_with_strategy,
    summarize_results as summarize_pipeline_results,
)
from chicken_data_synthesis.interfaces.cli import (
    build_completion_lines,
    build_header_lines,
    build_resume_lines,
)
from chicken_data_synthesis.application.use_cases.pipeline_runtime import (
    build_pipeline_runtime_plan,
)
from chicken_data_synthesis.application.use_cases import (
    PipelineUseCaseHooks,
    build_case_workflow_task,
    run_case_workflow,
    run_pipeline_use_case,
)
from chicken_data_synthesis.infrastructure.config import ModelRegistry, load_config
from chicken_data_synthesis.infrastructure.llm import (
    KeyPoolRegistry,
    RetryPolicy,
    build_openai_client,
    build_retry_policy,
    call_chat_completion_with_retry,
    extract_json_from_response as extract_json_payload,
)
from chicken_data_synthesis.infrastructure.knowledge import (
    build_wiki_audit_metadata,
    build_llm_wiki_context,
    load_llm_wiki,
    resolve_llm_wiki_dir,
)
from chicken_data_synthesis.infrastructure.prompts import (
    build_arbiter_messages,
    build_blind_completion_messages,
    build_consultation_draft_messages,
    build_judge_messages,
    render_template,
)
from chicken_data_synthesis.infrastructure.persistence import (
    dedupe_results_by_index,
    get_completed_indexes as collect_completed_indexes,
    load_snapshot,
    save_progress_runtime_snapshot,
    trim_snapshot_history as trim_snapshot_files,
    write_pipeline_output_artifacts,
)

CONFIG = load_config(PROJECT_ROOT)
MODEL_REGISTRY = ModelRegistry.from_config(CONFIG)

BASE_URL = CONFIG["api"]["base_url"]
MODELS = {role: MODEL_REGISTRY.get_role(role) for role in MODEL_REGISTRY.list_roles()}
CANDIDATE_MODELS = {
    candidate_key: MODEL_REGISTRY.get_candidate(candidate_key)
    for candidate_key in MODEL_REGISTRY.list_candidates()
}
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "results")
TEMP_DIR = os.path.join(PROJECT_ROOT, "temp")
MAX_PARALLEL = int(CONFIG.get("max_parallel", 4))
MAX_FAILURES = int(CONFIG.get("max_failures", 15))
PRODUCTION_CONFIG = CONFIG.get("production", {})
LOGGING_CONFIG = CONFIG.get("logging", {})
SNAPSHOT_CONFIG = CONFIG.get("snapshot", {})
RUNTIME_CONFIG = CONFIG.get("runtime", {})
EVALUATION_CONFIG = CONFIG.get("evaluation", {})
RULE_BASE_CONFIG = CONFIG.get("rule_base", {})
GENERATION_CONFIG = CONFIG.get("generation", {})
LLM_WIKI_DIR = resolve_llm_wiki_dir(CONFIG, PROJECT_ROOT)
LLM_WIKI = load_llm_wiki(LLM_WIKI_DIR)

RUN_CONTEXT: Dict[str, Any] = {
    "log_file": "",
    "error_log_file": "",
}
KEY_POOL_REGISTRY = KeyPoolRegistry()
CURRENT_EVALUATION_MODE = "legacy"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chicken golden dataset builder.")
    parser.add_argument(
        "--mode",
        choices=["pilot", "production"],
        default="pilot" if CONFIG.get("pilot", {}).get("enabled", True) else "production",
        help="Run mode.",
    )
    parser.add_argument(
        "--generator-key",
        default="",
        help="Override production generator candidate key.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=0,
        help="Override sample count.",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=0,
        help="Override parallel worker count.",
    )
    parser.add_argument(
        "--milestones",
        default="",
        help="Comma-separated production milestones.",
    )
    parser.add_argument(
        "--resume-from",
        default="",
        help="Resume from a snapshot file.",
    )
    parser.add_argument(
        "--evaluation-mode",
        choices=["auto", "legacy", "deepeval"],
        default="auto",
        help="Evaluation mode: auto, legacy, or deepeval.",
    )
    return parser.parse_args(argv)

def log_message(message: str, error: bool = False) -> None:
    try:
        print(message, flush=True)
    except UnicodeEncodeError:
        safe_message = message.encode("gbk", errors="replace").decode("gbk", errors="replace")
        print(safe_message, flush=True)
    path = RUN_CONTEXT["error_log_file"] if error else RUN_CONTEXT["log_file"]
    if path:
        with open(path, "a", encoding="utf-8") as file:
            file.write(f"{message}\n")


def setup_run_logging(mode: str, sample_count: int, timestamp: str = "") -> Dict[str, str]:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"{mode}_{sample_count}_{timestamp}"
    log_file = os.path.join(OUTPUT_DIR, f"{prefix}.log")
    error_log_file = os.path.join(OUTPUT_DIR, f"{prefix}.err.log")
    RUN_CONTEXT["log_file"] = log_file
    RUN_CONTEXT["error_log_file"] = error_log_file
    for path in (log_file, error_log_file):
        with open(path, "w", encoding="utf-8") as file:
            file.write("")
    return {"timestamp": timestamp, "log_file": log_file, "error_log_file": error_log_file}


def resolve_snapshot_settings() -> Dict[str, int]:
    return {
        "save_every_results": max(int(SNAPSHOT_CONFIG.get("save_every_results", 25)), 1),
        "keep_latest": max(int(SNAPSHOT_CONFIG.get("keep_latest", 5)), 1),
        "dispatch_chunk_size": max(int(PRODUCTION_CONFIG.get("dispatch_chunk_size", 20)), 1),
        "progress_log_every": max(int(LOGGING_CONFIG.get("progress_log_every", 5)), 1),
        "worker_max_cases_per_child": max(int(RUNTIME_CONFIG.get("worker_max_cases_per_child", 4)), 1),
    }


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    payload = extract_json_payload(response_text)
    return payload if isinstance(payload, dict) else None


def call_api_with_backoff(
    model_config: Dict[str, Any],
    messages: List[Dict[str, str]],
    expected_output: str = "",
    max_retries: int = 3,
) -> Tuple[Optional[str], Optional[str], float]:
    result = call_chat_completion_with_retry(
        model_config,
        messages,
        expected_output=expected_output,
        retry_policy=build_retry_policy(
            max_retries=max_retries,
            request_interval_seconds=float(CONFIG.get("request_interval", 0)),
            backoff_base_seconds=1.0,
            backoff_jitter_seconds=1.0,
        ),
        registry=KEY_POOL_REGISTRY,
        client_builder=lambda config, **kwargs: build_openai_client(
            config,
            default_base_url=BASE_URL,
            **kwargs,
        ),
    )
    return result.content, result.reasoning, result.elapsed_seconds


def build_wiki_query(*parts: Any, disease_name: str = "") -> str:
    values = [str(disease_name or "").strip()]
    values.extend(str(part or "").strip() for part in parts)
    return "\n".join(value for value in values if value)


def build_wiki_context(query: str, *, top_k_pages: int = 5, top_k_facts: int = 8) -> str:
    return build_llm_wiki_context(
        query,
        wiki_dir=LLM_WIKI_DIR,
        top_k_pages=top_k_pages,
        top_k_facts=top_k_facts,
    )


def resolve_generation_diseases() -> List[str]:
    wiki_names = [name for name in LLM_WIKI.disease_names() if name.strip()]
    configured_names = [str(name) for name in CONFIG.get("common_chicken_diseases", []) if str(name).strip()]
    return list(dict.fromkeys(wiki_names or configured_names))


def build_generation_prompt(disease_name: str) -> List[Dict[str, str]]:
    system_prompt = render_template(
        "generation_system_prompt.j2",
        disease_name=disease_name,
    )
    user_prompt = render_template(
        "generation_user_prompt.j2",
        disease_name=disease_name,
        scenario_hint="",
    )
    system_prompt = (
        f"{system_prompt}\n\n"
        "【LLM Wiki 知识底座约束】\n"
        f"{build_wiki_context(disease_name)}\n\n"
        "使用要求：生成样本必须与知识底座中的疾病实体、鉴别诊断、用药合规和监管事实一致；"
        "对未被知识底座支持的剂量、休药期或强制处置，不得编造为确定结论。"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def build_query_draft_prompt(disease_name: str) -> List[Dict[str, str]]:
    return build_consultation_draft_messages(
        disease_name=disease_name,
        scenario_hint="",
        knowledge_context=build_wiki_context(disease_name),
    )


def build_completion_prompt(disease_name: str, query_draft: Dict[str, Any]) -> List[Dict[str, str]]:
    safe_metadata = build_generation_completion_visible_metadata(
        query_draft,
        GENERATION_CONFIG.get("completion_visible_metadata_keys", []),
    )
    blind_completion = bool(GENERATION_CONFIG.get("blind_completion", True))
    query_text = build_wiki_query(
        query_draft.get("user_query", ""),
        json.dumps(safe_metadata, ensure_ascii=False),
        disease_name=disease_name,
    )
    return build_blind_completion_messages(
        user_query=query_draft.get("user_query", ""),
        metadata=safe_metadata,
        disease_name=disease_name,
        knowledge_context=build_wiki_context(query_text),
    )


def build_geval_prompt(case_data: Dict[str, Any]) -> List[Dict[str, str]]:
    metadata = case_data.get("metadata", {})
    disease_name = ""
    if isinstance(metadata, dict):
        disease_name = str(metadata.get("disease_name", "") or "")
    query = "\n".join(
        [
            disease_name,
            str(case_data.get("user_query", "")),
            str(case_data.get("diagnosis", "")),
            str(case_data.get("prescription", "")),
            json.dumps(metadata, ensure_ascii=False),
        ]
    )
    return build_judge_messages(case_data, knowledge_context=build_wiki_context(query, top_k_pages=6, top_k_facts=10))


def evaluate_rule_base(case_data: Dict[str, Any]) -> Dict[str, Any]:
    result = evaluate_rule_base_case(case_data, RULE_BASE_CONFIG)
    metadata = case_data.get("metadata", {})
    disease_name = str(metadata.get("disease_name", "") or "") if isinstance(metadata, dict) else ""
    query = build_wiki_query(
        case_data.get("user_query", ""),
        case_data.get("diagnosis", ""),
        case_data.get("prescription", ""),
        case_data.get("withdrawal_period", ""),
        json.dumps(metadata, ensure_ascii=False),
        disease_name=disease_name,
    )
    context = build_wiki_context(query, top_k_pages=6, top_k_facts=10)
    result["llm_wiki_context"] = context
    result["wiki_audit"] = build_wiki_audit_metadata(
        wiki_dir=LLM_WIKI_DIR,
        knowledge_context=context,
        query=query,
    )
    return result


def evaluate_case_legacy(
    case_data: Dict[str, Any],
    judge_label: str,
    judge_config: Dict[str, Any],
) -> Tuple[Optional[Dict[str, Any]], float]:
    started_at = time.perf_counter()
    content, _, _ = call_api_with_backoff(
        judge_config,
        build_geval_prompt(case_data),
        expected_output="json",
    )
    if not content:
        return None, time.perf_counter() - started_at

    result = extract_json_from_response(content)
    if result is None:
        return None, time.perf_counter() - started_at

    result["judge_label"] = judge_label
    result["judge_model"] = judge_config["name"]
    return normalize_judge_result(result), time.perf_counter() - started_at


def build_arbitration_prompt(
    case_data: Dict[str, Any],
    judge_a_result: Dict[str, Any],
    judge_b_result: Dict[str, Any],
) -> List[Dict[str, str]]:
    metadata = case_data.get("metadata", {})
    disease_name = str(metadata.get("disease_name", "") or "") if isinstance(metadata, dict) else ""
    query = "\n".join(
        [
            disease_name,
            str(case_data.get("user_query", "")),
            str(case_data.get("diagnosis", "")),
            str(case_data.get("prescription", "")),
            str(judge_a_result.get("summary", "")),
            str(judge_b_result.get("summary", "")),
        ]
    )
    return build_arbiter_messages(
        case_data,
        judge_a_result,
        judge_b_result,
        knowledge_context=build_wiki_context(query, top_k_pages=6, top_k_facts=10),
    )


def arbitrate_case(
    case_data: Dict[str, Any],
    judge_a_result: Dict[str, Any],
    judge_b_result: Dict[str, Any],
    arbiter_config: Dict[str, Any],
) -> Tuple[Optional[Dict[str, Any]], float]:
    content, reasoning, elapsed = call_api_with_backoff(
        arbiter_config,
        build_arbitration_prompt(case_data, judge_a_result, judge_b_result),
        expected_output="json",
    )
    if not content:
        return None, elapsed

    result = extract_json_from_response(content)
    if result is None:
        return None, elapsed

    result["arbiter_model"] = arbiter_config["name"]
    result["arbiter_reasoning_content"] = reasoning or ""
    return result, elapsed

TaskTuple = Tuple[int, str, str, Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], str]


def process_single_case(task_data: TaskTuple) -> Dict[str, Any]:
    task = build_case_workflow_task(task_data)
    global CURRENT_EVALUATION_MODE
    CURRENT_EVALUATION_MODE = task.evaluation_mode
    return run_case_workflow(
        task,
        generate_case=lambda disease_name, generator_key, generator_config: run_generation_with_strategy(
            disease_name,
            generator_key,
            generator_config,
            candidate_models=CANDIDATE_MODELS,
            generation_config=GENERATION_CONFIG,
            call_model=call_api_with_backoff,
            parse_payload=extract_json_from_response,
            build_messages=build_generation_prompt,
            build_query_messages=build_query_draft_prompt,
            build_completion_messages=build_completion_prompt,
        ),
        evaluate_rule_base=evaluate_rule_base,
        evaluate_case=lambda case_data, judge_label, primary_config: evaluate_case_with_fallbacks(
            case_data,
            judge_label,
            primary_config,
            candidate_models=CANDIDATE_MODELS,
            evaluation_mode=CURRENT_EVALUATION_MODE,
            project_config=CONFIG,
            legacy_evaluator=evaluate_case_legacy,
        ),
        arbitrate_case=lambda case_data, judge_a_result, judge_b_result, primary_config: arbitrate_case_with_fallbacks(
            case_data,
            judge_a_result,
            judge_b_result,
            primary_config,
            candidate_models=CANDIDATE_MODELS,
            arbitrate_case=arbitrate_case,
        ),
        arbitration_threshold=float(CONFIG["scoring"]["arbitration_threshold"]),
    )


def build_tasks_for_range(mode: str, start_index: int, sample_count: int, evaluation_mode: str) -> List[TaskTuple]:
    return build_case_tasks(
        mode=mode,
        start_index=start_index,
        sample_count=sample_count,
        evaluation_mode=evaluation_mode,
        diseases=resolve_generation_diseases(),
        pilot_config=CONFIG.get("pilot", {}),
        candidate_models=CANDIDATE_MODELS,
        default_models=MODELS,
        disease_picker=random.choice,
    )


def trim_snapshot_history(prefix: str, keep_latest: int) -> None:
    trim_snapshot_files(TEMP_DIR, prefix, keep_latest)


def load_progress_snapshot(snapshot_path: str) -> Dict[str, Any]:
    return load_snapshot(snapshot_path)


def save_emergency_snapshot(
    mode: str,
    sample_count: int,
    results: List[Dict[str, Any]],
    completed_target: int,
    parallel_count: int,
    milestones: Optional[List[int]] = None,
) -> str:
    return save_progress_runtime_snapshot(
        mode=mode,
        sample_count=sample_count,
        results=results,
        completed_target=completed_target,
        parallel_count=parallel_count,
        directory=TEMP_DIR,
        snapshot_kind="emergency",
        milestones=milestones,
        keep_latest=resolve_snapshot_settings()["keep_latest"],
        target_hint=completed_target,
    )


def run_task_batch(
    mode: str,
    tasks: List[TaskTuple],
    all_results: List[Dict[str, Any]],
    started_at: datetime,
    parallel_count: int,
    sample_count: int,
    completed_target: int,
    milestones: Optional[List[int]] = None,
) -> Tuple[List[Dict[str, Any]], int]:
    settings = resolve_snapshot_settings()
    batch_settings = BatchExecutionSettings(
        progress_log_every=settings["progress_log_every"],
        snapshot_every=settings["save_every_results"],
        dispatch_chunk_size=settings["dispatch_chunk_size"],
        worker_max_cases_per_child=settings["worker_max_cases_per_child"],
        max_failures=MAX_FAILURES,
    )

    def save_progress(all_runtime_results: Iterable[Dict[str, Any]]) -> None:
        save_progress_runtime_snapshot(
            mode=mode,
            sample_count=sample_count,
            results=all_runtime_results,
            completed_target=completed_target,
            parallel_count=parallel_count,
            directory=TEMP_DIR,
            snapshot_kind="progress",
            milestones=milestones,
            keep_latest=resolve_snapshot_settings()["keep_latest"],
            target_hint=completed_target,
        )

    execution = execute_task_batch(
        tasks,
        process_single_case,
        all_results,
        parallel_count=parallel_count,
        settings=batch_settings,
        started_at=started_at,
        sample_count=sample_count,
        log_message=lambda message, error=False: log_message(message, error=error),
        build_failure_message=build_failure_log_message,
        build_progress_message=build_batch_progress_message,
        save_snapshot=save_progress,
    )
    return execution.stage_results, execution.failure_count


def print_header(
    mode: str,
    sample_count: int,
    parallel_count: int,
    milestones: Optional[List[int]] = None,
    evaluation_mode: str = "legacy",
) -> None:
    lines = build_header_lines(
        mode=mode,
        sample_count=sample_count,
        parallel_count=parallel_count,
        evaluation_mode=evaluation_mode,
        project_name=CONFIG.get("project_name", ""),
        version=CONFIG.get("version", ""),
        request_interval=CONFIG.get("request_interval", 0),
        snapshot_settings=resolve_snapshot_settings(),
        pilot_config=CONFIG.get("pilot", {}),
        production_models=MODELS,
        milestones=milestones,
        log_file=RUN_CONTEXT["log_file"],
        error_log_file=RUN_CONTEXT["error_log_file"],
        title="鸡病黄金数据集构建系统",
    )
    for line in lines:
        log_message(line)


def prepare_dirs(clear_temp: bool = True) -> None:
    if clear_temp and os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_resume_state(resume_from: str) -> Optional[Dict[str, Any]]:
    if not resume_from:
        return None
    if not os.path.exists(resume_from):
        raise FileNotFoundError(f"鏈壘鍒板揩鐓ф枃浠? {resume_from}")
    return load_progress_snapshot(resume_from)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    global CURRENT_EVALUATION_MODE
    requested_mode = args.mode
    CURRENT_EVALUATION_MODE = resolve_pipeline_evaluation_mode(
        requested_mode,
        args.evaluation_mode,
        EVALUATION_CONFIG,
    )
    raw_resume_state = load_resume_state(args.resume_from)
    runtime_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    runtime_plan = build_pipeline_runtime_plan(
        mode=requested_mode,
        cli_samples=args.samples,
        cli_parallel=args.parallel,
        raw_milestones=args.milestones,
        evaluation_mode=CURRENT_EVALUATION_MODE,
        generator_key=args.generator_key,
        resume_from=args.resume_from,
        config=CONFIG,
        output_dir=OUTPUT_DIR,
        temp_dir=TEMP_DIR,
        timestamp=runtime_timestamp,
        resume_state=raw_resume_state,
        default_parallel=MAX_PARALLEL,
    )
    mode = runtime_plan.options.mode
    sample_count = runtime_plan.options.sample_count
    parallel_count = runtime_plan.options.parallel_count
    milestones = list(runtime_plan.options.milestones)

    if mode == "production" and args.generator_key:
        generator_key = args.generator_key
        if generator_key not in CANDIDATE_MODELS:
            raise ValueError(f"鏈壘鍒?generator key: {generator_key}")
        MODELS["generator"] = CANDIDATE_MODELS[generator_key]

    prepare_dirs(clear_temp=runtime_plan.options.clear_temp)
    setup_run_logging(mode, sample_count, runtime_plan.output_paths.timestamp)

    pipeline_hooks = PipelineUseCaseHooks(
        build_tasks=build_tasks_for_range,
        run_task_batch=run_task_batch,
        save_stage_snapshot=lambda run_mode, total_samples, results, current_target, workers, active_milestones, snapshot_target: save_progress_runtime_snapshot(
            mode=run_mode,
            sample_count=total_samples,
            results=results,
            completed_target=current_target,
            parallel_count=workers,
            directory=TEMP_DIR,
            snapshot_kind="stage",
            milestones=active_milestones,
            keep_latest=resolve_snapshot_settings()["keep_latest"],
            target_hint=snapshot_target,
        ),
        save_emergency_snapshot=save_emergency_snapshot,
        write_outputs=lambda results, result_csv, summary_csv=None: write_pipeline_output_artifacts(
            results,
            result_csv,
            summary_csv=summary_csv,
        ),
        summarize_results=summarize_pipeline_results,
        build_resume_lines=lambda snapshot_path, result_count, completed_target: build_resume_lines(
            snapshot_path=snapshot_path,
            result_count=result_count,
            completed_target=completed_target,
        ),
        print_header=print_header,
        build_stage_summary_lines=lambda target_total, stage_results, all_results: build_stage_summary_lines_from_context(
            build_stage_summary_context(target_total, stage_results, all_results)
        ),
        build_completion_lines=lambda run_mode, summary, elapsed_total_seconds, result_csv, summary_csv, total_samples=None: build_completion_lines(
            **build_completion_summary_context(
                mode=run_mode,
                summary=summary,
                elapsed_total_seconds=elapsed_total_seconds,
                result_csv=result_csv,
                summary_csv=summary_csv or None,
                sample_count=total_samples,
                parallel_count=parallel_count,
            )
        ),
        filter_pending_tasks=lambda tasks, completed_indexes: list(filter_runtime_pending_tasks(tasks, completed_indexes)),
        log=lambda message, error=False: log_message(message, error=error),
        now=datetime.now,
    )
    try:
        run_pipeline_use_case(runtime_input=runtime_plan, hooks=pipeline_hooks)
    except Exception:
        log_message(traceback.format_exc(), error=True)
        raise


if __name__ == "__main__":
    main()
