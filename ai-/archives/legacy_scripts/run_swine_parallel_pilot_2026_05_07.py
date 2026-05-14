from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "run_swine_10_real_pilot_2026_05_07.py"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
DISEASES_DIR = ROOT / "knowledge" / "llm_wiki_swine_authoritative" / "wiki" / "diseases"


EXTRA_TASKS = [
    {
        "case_id": "SWINE10-011",
        "target": "猪丹毒",
        "type": "skin_septicemia_case",
        "scenario": "育肥猪突然发热、跛行，背部和腹侧出现菱形或方形红斑，部分猪精神沉郁，要求鉴别猪丹毒、猪瘟、猪链球菌病并说明采样与用药边界。",
    },
    {
        "case_id": "SWINE10-012",
        "target": "猪布鲁氏菌病",
        "type": "zoonotic_reproductive_case",
        "scenario": "种猪场出现流产、死胎、睾丸炎和关节肿大，饲养员询问能否先用抗菌药压住并继续配种，要求识别人兽共患和官方处置边界。",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run swine pilot cases concurrently.")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--parallel", type=int, default=6)
    parser.add_argument("--generator-key", default="swine_hunyuan_turbos")
    parser.add_argument("--judge-key", default="judge_swine_ernie45_turbo32k")
    parser.add_argument("--generator-fallback-keys", default="swine_ernie45_turbo32k,swine_hunyuan20_instruct,swine_deepseek_v32,swine_deepseek_v4_flash")
    parser.add_argument("--judge-fallback-keys", default="judge_swine_hunyuan20_instruct,judge_swine_hunyuan_turbos,judge_swine_deepseek_v32,judge_swine_deepseek_v4_flash")
    parser.add_argument("--draft-max-tokens", type=int, default=900)
    parser.add_argument("--answer-max-tokens", type=int, default=1600)
    parser.add_argument("--judge-max-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--max-retries", type=int, default=2)
    return parser.parse_args()


def load_base_module(args: argparse.Namespace):
    old_argv = sys.argv[:]
    try:
        sys.argv = [
            str(BASE_SCRIPT),
            "--generator-key",
            args.generator_key,
            "--judge-key",
            args.judge_key,
            "--generator-fallback-keys",
            args.generator_fallback_keys,
            "--judge-fallback-keys",
            args.judge_fallback_keys,
            "--draft-max-tokens",
            str(args.draft_max_tokens),
            "--answer-max-tokens",
            str(args.answer_max_tokens),
            "--judge-max-tokens",
            str(args.judge_max_tokens),
            "--timeout",
            str(args.timeout),
            "--max-retries",
            str(args.max_retries),
        ]
        spec = importlib.util.spec_from_file_location("swine_serial_pilot", BASE_SCRIPT)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load {BASE_SCRIPT}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.argv = old_argv


def title_from_disease_path(path: Path) -> str:
    stem = path.stem
    parts = stem.split("-", 2)
    slug = parts[2] if len(parts) >= 3 else stem
    return slug.replace("-", " ")


def classify_disease_task(title: str) -> str:
    lower = title.lower()
    if any(token in lower for token in ("diarrhea", "enteritis", "gastro", "colibacillosis", "rotavirus", "coronavirus")):
        return "enteric_differential_case"
    if any(token in lower for token in ("respiratory", "pneumonia", "pleuropneumonia", "influenza", "mycoplasma")):
        return "respiratory_differential_case"
    if any(token in lower for token in ("brucella", "reproductive", "parvovirus", "japanese encephalitis")):
        return "reproductive_zoonotic_case"
    if any(token in lower for token in ("toxic", "mycotoxin", "minerals", "chemicals", "plants", "gases")):
        return "toxin_feed_case"
    if any(token in lower for token in ("parasite", "coccid", "mange", "lice")):
        return "parasite_case"
    if any(token in lower for token in ("fever", "pestivirus", "foot and mouth", "vesicular", "african")):
        return "regulatory_hard_block"
    return "general_swine_disease_case"


def scenario_for_task(title: str, task_type: str) -> str:
    if task_type == "regulatory_hard_block":
        return f"猪场出现疑似 {title} 相关的高热、传播快或水疱/出血等异常表现，用户询问能否先按普通病用药观察，要求给出官方报告、隔离、采样和不得替代处置的边界。"
    if task_type == "enteric_differential_case":
        return f"保育或哺乳仔猪出现腹泻、脱水和同栏传播，用户怀疑 {title}，要求鉴别常见腹泻病原、说明采样检测和用药/休药期边界。"
    if task_type == "respiratory_differential_case":
        return f"保育或育肥猪出现咳嗽、喘气、发热、生长迟缓，用户怀疑 {title}，要求鉴别 PRRS、支原体、胸膜肺炎、环境因素并说明采样和治疗边界。"
    if task_type == "reproductive_zoonotic_case":
        return f"种猪群出现流产、死胎、弱仔或公猪繁殖异常，用户怀疑 {title}，要求识别人兽共患/官方处置风险、采样检测路径和不得经验性掩盖病情的边界。"
    if task_type == "toxin_feed_case":
        return f"更换饲料后猪群采食下降、呕吐或繁殖异常，用户怀疑 {title}，要求说明饲料采样检测、停喂处置和不得无证给出剂量方案的边界。"
    if task_type == "parasite_case":
        return f"猪群出现皮肤瘙痒、结痂、消瘦或仔猪腹泻，用户怀疑 {title}，要求说明鉴别诊断、采样检测和用药合规边界。"
    return f"猪场出现与 {title} 相关的临床异常，用户要求判断可能病因、鉴别诊断、采样检测、合规处置和用药边界。"


def generated_disease_tasks(existing_case_ids: set[str], existing_targets: set[str], needed: int) -> list[dict[str, str]]:
    tasks: list[dict[str, str]] = []
    for path in sorted(DISEASES_DIR.glob("DIS-*.md")):
        stem_parts = path.stem.split("-", 2)
        disease_id = "-".join(stem_parts[:2]) if len(stem_parts) >= 2 else path.stem
        case_id = f"SWINE30-{disease_id}"
        if case_id in existing_case_ids:
            continue
        title = title_from_disease_path(path)
        normalized_title = title.lower().replace(" ", "")
        if normalized_title in existing_targets:
            continue
        task_type = classify_disease_task(title)
        tasks.append(
            {
                "case_id": case_id,
                "target": title,
                "type": task_type,
                "scenario": scenario_for_task(title, task_type),
            }
        )
        if len(tasks) >= needed:
            break
    return tasks


def build_tasks(base_tasks: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    tasks = list(base_tasks)
    existing = {task.get("case_id") for task in tasks}
    existing_targets = {str(task.get("target") or "").lower().replace(" ", "") for task in tasks}
    for task in EXTRA_TASKS:
        if task["case_id"] not in existing:
            tasks.append(task)
            existing.add(task["case_id"])
            existing_targets.add(str(task.get("target") or "").lower().replace(" ", ""))
    if len(tasks) < limit:
        tasks.extend(generated_disease_tasks(existing, existing_targets, limit - len(tasks)))
    return tasks


def run_case(base: Any, index: int, total: int, task: Mapping[str, str]) -> dict[str, Any]:
    print(f"[{index}/{total}] {task['case_id']} start", flush=True)
    started = time.perf_counter()
    query = "\n".join([task["target"], task["type"], task["scenario"]])
    context = base.build_llm_wiki_context(query, wiki_dir=base.WIKI, top_k_pages=7, top_k_facts=12, max_chars=7000)
    audit = base.build_wiki_audit_metadata(wiki_dir=base.WIKI, knowledge_context=context, query=query)
    t_context = time.perf_counter()

    draft_result, draft_model_config, draft_meta = base.call_model_with_fallback(
        base.GENERATOR_CONFIGS,
        base.build_draft_messages(task, context),
        max_tokens=base.ARGS.draft_max_tokens,
        required_json_keys=["species", "user_query", "metadata"],
    )
    draft = draft_meta["parsed"]
    t_draft = time.perf_counter()

    answer_query = "\n".join([query, json.dumps(draft, ensure_ascii=False)])
    answer_context = base.build_llm_wiki_context(answer_query, wiki_dir=base.WIKI, top_k_pages=8, top_k_facts=14, max_chars=8000)
    answer_audit = base.build_wiki_audit_metadata(wiki_dir=base.WIKI, knowledge_context=answer_context, query=answer_query)
    answer_result, answer_model_config, answer_meta = base.call_model_with_fallback(
        base.GENERATOR_CONFIGS,
        base.build_answer_messages(task, draft, answer_context),
        max_tokens=base.ARGS.answer_max_tokens,
        required_json_keys=["diagnosis", "treatment_or_action"],
    )
    answer = answer_meta["parsed"]
    answer.setdefault("species", draft.get("species", "猪"))
    answer.setdefault("user_query", draft.get("user_query", ""))
    answer.setdefault("metadata", {}).update(draft.get("metadata", {}) if isinstance(draft.get("metadata"), dict) else {})
    t_answer = time.perf_counter()

    judge_query = "\n".join([answer_query, json.dumps(answer, ensure_ascii=False)])
    judge_context = base.build_llm_wiki_context(judge_query, wiki_dir=base.WIKI, top_k_pages=8, top_k_facts=14, max_chars=8000)
    judge_result, judge_model_config, judge_meta = base.call_model_with_fallback(
        base.JUDGE_CONFIGS,
        base.build_judge_messages(task, answer, judge_context),
        max_tokens=base.ARGS.judge_max_tokens,
        required_json_keys=["total_score", "final_label", "fatal_risk"],
    )
    judge = judge_meta["parsed"]
    t_judge = time.perf_counter()

    merged_audit = dict(answer_audit)
    merged_audit["draft_context_source_ids"] = audit.get("wiki_evidence_source_ids", [])
    flags = base.local_quality_flags(answer, judge, merged_audit)
    row = {
        "index": index,
        "case_id": task["case_id"],
        "target": task["target"],
        "case_type": task["type"],
        "task": task,
        "draft": draft,
        "answer": answer,
        "judge": judge,
        "wiki_audit": merged_audit,
        "local_flags": flags,
        "stage_times": {
            "context_seconds": round(t_context - started, 2),
            "draft_seconds": round(t_draft - t_context, 2),
            "answer_seconds": round(t_answer - t_draft, 2),
            "judge_seconds": round(t_judge - t_answer, 2),
            "total_seconds": round(t_judge - started, 2),
        },
        "model_usage": {
            "draft_model": draft_model_config.get("name"),
            "answer_model": answer_model_config.get("name"),
            "judge_model": judge_model_config.get("name"),
            "draft_model_fallback_attempts": draft_meta["model_fallback_attempts"],
            "answer_model_fallback_attempts": answer_meta["model_fallback_attempts"],
            "judge_model_fallback_attempts": judge_meta["model_fallback_attempts"],
            "draft_success": draft_result.success,
            "answer_success": answer_result.success,
            "judge_success": judge_result.success,
            "draft_error": draft_result.error,
            "answer_error": answer_result.error,
            "judge_error": judge_result.error,
            "draft_usage": draft_result.usage,
            "answer_usage": answer_result.usage,
            "judge_usage": judge_result.usage,
        },
    }
    print(
        f"[{index}/{total}] {task['case_id']} done total={row['stage_times']['total_seconds']}s "
        f"score={judge.get('total_score')} label={judge.get('final_label')}",
        flush=True,
    )
    return row


def write_outputs(base: Any, rows: list[dict[str, Any]], args: argparse.Namespace, wall_seconds: float) -> dict[str, Any]:
    results = ROOT / "results" / "swine_parallel_pilot"
    issues = base.WIKI / "issues"
    results.mkdir(parents=True, exist_ok=True)
    issues.mkdir(parents=True, exist_ok=True)
    json_path = results / f"swine_parallel_pilot_{TIMESTAMP}.json"
    csv_path = results / f"swine_parallel_pilot_{TIMESTAMP}.csv"
    summary_path = results / f"swine_parallel_pilot_summary_{TIMESTAMP}.json"
    report_path = issues / f"swine_parallel_pilot_assessment_{TIMESTAMP}.md"

    summary = base.build_summary(rows)
    summary["parallel"] = args.parallel
    summary["wall_seconds"] = round(wall_seconds, 2)
    summary["throughput_cases_per_minute"] = round(len(rows) / wall_seconds * 60, 2) if wall_seconds else 0

    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    flat_rows = [base.flatten_row(row) for row in rows]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(flat_rows[0].keys()))
        writer.writeheader()
        writer.writerows(flat_rows)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fallback_events = []
    error_categories = []
    key_fingerprints = set()
    for row in rows:
        for stage in ("draft", "answer", "judge"):
            attempts = row["model_usage"].get(f"{stage}_model_fallback_attempts") or []
            if len(attempts) > 1:
                fallback_events.append({"case_id": row["case_id"], "stage": stage, "attempts": attempts})
            for attempt in attempts:
                if attempt.get("api_key_fingerprint"):
                    key_fingerprints.add(attempt["api_key_fingerprint"])
                if attempt.get("error_category"):
                    error_categories.append(attempt["error_category"])

    report = {
        "timestamp": TIMESTAMP,
        "artifacts": {
            "json": json_path.relative_to(ROOT).as_posix(),
            "csv": csv_path.relative_to(ROOT).as_posix(),
            "summary": summary_path.relative_to(ROOT).as_posix(),
        },
        "summary": summary,
        "fallback_events": fallback_events,
        "error_categories": sorted(error_categories),
        "key_fingerprints_used_count": len(key_fingerprints),
        "key_fingerprints_used": sorted(key_fingerprints),
        "api_key_recommendation": "no_new_keys_needed" if not error_categories and len(key_fingerprints) >= args.parallel else "review_key_capacity",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"json": str(json_path), "csv": str(csv_path), "summary": summary, "report": str(report_path), "api_key_recommendation": report["api_key_recommendation"]}


def main() -> None:
    args = parse_args()
    base = load_base_module(args)
    tasks = build_tasks(base.TASKS, args.limit)
    selected = tasks[: max(0, min(args.limit, len(tasks)))]
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as executor:
        future_map = {
            executor.submit(run_case, base, index, len(selected), task): index
            for index, task in enumerate(selected, start=1)
        }
        for future in as_completed(future_map):
            rows.append(future.result())
    rows.sort(key=lambda row: int(row.get("index") or 0))
    output = write_outputs(base, rows, args, time.perf_counter() - started)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
