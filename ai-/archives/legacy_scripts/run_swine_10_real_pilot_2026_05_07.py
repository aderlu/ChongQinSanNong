from __future__ import annotations

import csv
import argparse
import hashlib
import json
import re
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
for item in (str(ROOT), str(SRC_DIR)):
    if item not in sys.path:
        sys.path.insert(0, item)

from chicken_data_synthesis.infrastructure.config import ModelRegistry, load_config
from chicken_data_synthesis.infrastructure.knowledge import (
    build_llm_wiki_context,
    build_wiki_audit_metadata,
)
from chicken_data_synthesis.infrastructure.llm import (
    KeyPoolRegistry,
    build_openai_client,
    build_retry_policy,
    call_chat_completion_with_retry,
    extract_json_from_response,
)


WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
RESULTS = ROOT / "results" / "swine_10_real_pilot"
ISSUES = WIKI / "issues"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


TASKS = [
    {
        "case_id": "SWINE10-001",
        "target": "非洲猪瘟",
        "type": "regulatory_hard_block",
        "scenario": "育肥猪高热、死亡率快速升高、皮肤发绀，要求模型判断是否能先用抗生素观察。",
    },
    {
        "case_id": "SWINE10-002",
        "target": "猪流行性腹泻",
        "type": "diarrhea_case",
        "scenario": "哺乳仔猪水样腹泻、同窝快速传播、母猪轻微腹泻，要求鉴别 PED/TGE/轮状病毒/大肠杆菌。",
    },
    {
        "case_id": "SWINE10-003",
        "target": "猪大肠杆菌病",
        "type": "diarrhea_treatment_boundary",
        "scenario": "断奶后一周腹泻、脱水、部分死亡，用户询问能否直接全群用抗菌药和休药期。",
    },
    {
        "case_id": "SWINE10-004",
        "target": "猪胸膜肺炎",
        "type": "respiratory_case",
        "scenario": "保育猪急性咳喘、死亡、剖检胸膜炎和出血坏死性肺炎，要求给出诊断和采样。",
    },
    {
        "case_id": "SWINE10-005",
        "target": "猪支原体肺炎",
        "type": "respiratory_differential",
        "scenario": "慢性咳嗽、低死亡率、生长迟缓、通风差，要求区分支原体、PRRS、巴氏杆菌和环境因素。",
    },
    {
        "case_id": "SWINE10-006",
        "target": "猪痢疾",
        "type": "drug_interaction_boundary",
        "scenario": "育肥猪血痢，用户已有泰妙菌素和含离子载体饲料，询问能否一起用。",
    },
    {
        "case_id": "SWINE10-007",
        "target": "猪球虫病",
        "type": "parasite_case",
        "scenario": "7-14日龄仔猪糊状腹泻、抗菌药效果差，要求判断球虫病和托曲珠利边界。",
    },
    {
        "case_id": "SWINE10-008",
        "target": "猪霉菌毒素中毒",
        "type": "toxin_feed_case",
        "scenario": "更换玉米后采食下降、呕吐、母猪繁殖异常，要求识别 DON/ZEA/黄曲霉毒素并说明检测。",
    },
    {
        "case_id": "SWINE10-009",
        "target": "猪疥螨病",
        "type": "ectoparasite_case",
        "scenario": "种猪耳后结痂、剧痒、全群蹭痒，要求鉴别疥螨和虱病并说明控制措施。",
    },
    {
        "case_id": "SWINE10-010",
        "target": "猪链球菌病",
        "type": "neuro_septicemia_case",
        "scenario": "保育猪跛行、神经症状、突然死亡，要求鉴别链球菌、伪狂犬、仔猪水肿病并说明药敏边界。",
    },
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
    parser = argparse.ArgumentParser(description="Run a small real swine wiki pilot.")
    parser.add_argument("--limit", type=int, default=len(TASKS), help="Number of tasks to run from the fixed pilot set.")
    parser.add_argument("--generator-key", default="swine_hunyuan_turbos", help="Primary candidate model key for draft and answer generation.")
    parser.add_argument("--judge-key", default="judge_swine_ernie45_turbo32k", help="Primary candidate model key for judge evaluation.")
    parser.add_argument(
        "--generator-fallback-keys",
        default="swine_ernie45_turbo32k,swine_hunyuan20_instruct,swine_deepseek_v32,swine_deepseek_v4_flash",
        help="Comma-separated generator candidate fallback keys.",
    )
    parser.add_argument(
        "--judge-fallback-keys",
        default="judge_swine_hunyuan20_instruct,judge_swine_hunyuan_turbos,judge_swine_deepseek_v32,judge_swine_deepseek_v4_flash",
        help="Comma-separated judge candidate fallback keys.",
    )
    parser.add_argument("--draft-max-tokens", type=int, default=900)
    parser.add_argument("--answer-max-tokens", type=int, default=1600)
    parser.add_argument("--judge-max-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--parallel", type=int, default=1, help="Number of cases to run concurrently.")
    return parser.parse_args()


def tuned_model_config(model_config: Mapping[str, Any], *, max_tokens: int) -> dict[str, Any]:
    tuned = dict(model_config)
    tuned["max_tokens"] = int(max_tokens)
    tuned["timeout"] = int(ARGS.timeout)
    return tuned


def call_model(model_config: Mapping[str, Any], messages: list[dict[str, str]], *, max_retries: int | None = None):
    result = call_chat_completion_with_retry(
        dict(model_config),
        messages,
        expected_output="json",
        retry_policy=build_retry_policy(
            max_retries=ARGS.max_retries if max_retries is None else max_retries,
            request_interval_seconds=0.3,
            backoff_base_seconds=1.0,
            backoff_jitter_seconds=0.5,
        ),
        registry=KEY_POOL,
        client_builder=lambda config, **kwargs: build_openai_client(
            config,
            default_base_url=BASE_URL,
            **kwargs,
        ),
    )
    return result


def parse_key_chain(primary_key: str, fallback_keys: str) -> list[str]:
    keys: list[str] = []
    for key in [primary_key, *str(fallback_keys or "").split(",")]:
        normalized = str(key).strip()
        if normalized and normalized not in keys:
            keys.append(normalized)
    return keys


def fingerprint_key(api_key: str) -> str:
    if not api_key:
        return ""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12]


def call_model_with_fallback(
    model_configs: list[dict[str, Any]],
    messages: list[dict[str, str]],
    *,
    max_tokens: int,
    required_json_keys: list[str] | None = None,
) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    attempts = []
    last_result = None
    for model_config in model_configs:
        tuned = tuned_model_config(model_config, max_tokens=max_tokens)
        result = call_model(tuned, messages)
        parsed = parse_json(result.content)
        has_required_json = bool(parsed) and all(key in parsed for key in (required_json_keys or []))
        attempts.append(
            {
                "model": tuned.get("name"),
                "success": result.success,
                "elapsed_seconds": round(result.elapsed_seconds, 2),
                "attempts": result.attempts,
                "api_key_fingerprint": fingerprint_key(result.api_key),
                "error_category": result.error_category,
                "error": result.error,
                "parsed_json": bool(parsed),
                "has_required_json": has_required_json,
                "usage": result.usage,
                "cost": result.cost,
            }
        )
        if result.success and has_required_json:
            return result, tuned, {"model_fallback_attempts": attempts, "parsed": parsed}
        last_result = result
    if last_result is None:
        raise RuntimeError("No model configs available for fallback.")
    return last_result, dict(model_configs[-1]), {"model_fallback_attempts": attempts, "parsed": {}}


def parse_json(content: str | None) -> dict[str, Any]:
    payload = extract_json_from_response(content or "")
    return payload if isinstance(payload, dict) else {}


def build_draft_messages(task: Mapping[str, str], context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是资深猪病数据集构建助手。请只输出 JSON。\n"
                "任务：生成一条真实养猪场问诊草稿，不要输出诊断、治疗方案、剂量或休药期。\n"
                "必须使用猪作为物种；metadata 必须含 disease_name、case_type、severity、scene_tags、required_anchors。\n"
                "病例线索要像真实养殖户提问，包含日龄/阶段、群体规模、症状、病程、环境或用药线索。\n"
                "LLM Wiki 约束如下：\n"
                f"{context}"
            ),
        },
        {
            "role": "user",
            "content": (
                f"目标疾病/主题：{task['target']}\n"
                f"题型：{task['type']}\n"
                f"场景：{task['scenario']}\n"
                "输出 JSON schema: {\"species\":\"猪\",\"user_query\":\"...\",\"metadata\":{...}}"
            ),
        },
    ]


def build_answer_messages(task: Mapping[str, str], draft: Mapping[str, Any], context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是资深猪病临床与数据集答案构建助手。请只输出 JSON。\n"
                "基于问诊草稿生成标准答案，必须包含 diagnosis、treatment_or_action、drug_boundary、withdrawal_period_boundary、metadata。\n"
                "所有诊断、监管、用药、采样或安全结论必须使用标准引用格式 source=SRC-0000、source=A0-...、source=A1-... 或 source=RC-...；不得只写内部 anchor key、页面路径或 source_id。\n"
                "没有中国标签/公告/药敏证据时，不得输出具体剂量、疗程、给药途径、休药期或残留合格承诺。\n"
                "疑似 ASF/FMD/禁用药/气体中毒/高风险药物时，必须触发硬边界或拒绝可执行用药方案。\n"
                "LLM Wiki 约束如下：\n"
                f"{context}"
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "target": task["target"],
                    "case_type": task["type"],
                    "scenario": task["scenario"],
                    "draft": draft,
                },
                ensure_ascii=False,
            ),
        },
    ]


def build_judge_messages(task: Mapping[str, str], case: Mapping[str, Any], context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是猪病训练数据质量评审专家。请只输出 JSON。\n"
                "按 100 分评分：evidence_anchoring 25，clinical_reasoning 20，regulatory_safety 20，drug_boundary 15，diagnostic_sampling 10，data_usability 10。\n"
                "只要出现无来源剂量、无来源休药期、禁用药可用建议、ASF/FMD 用药替代报告，fatal_risk=true。\n"
                "输出字段：total_score, final_label(pass/review/reject), fatal_risk, strengths, weaknesses, missing_anchors, improvement_actions。若标准 source=... 引用不足 3 个，不能判 pass。\n"
                "LLM Wiki 约束如下：\n"
                f"{context}"
            ),
        },
        {
            "role": "user",
            "content": json.dumps({"task": task, "case": case}, ensure_ascii=False),
        },
    ]


def local_quality_flags(case: Mapping[str, Any], judge: Mapping[str, Any], audit: Mapping[str, Any]) -> dict[str, Any]:
    text = json.dumps(case, ensure_ascii=False)
    source_hits = sorted(set(re.findall(r"\b(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+)\b", text)))
    dosage_pattern = bool(re.search(r"\d+(?:\.\d+)?\s*(?:mg/kg|mg|ml|mL|g/L|g|ppm|IU|万单位)", text, flags=re.I))
    withdrawal_specific = bool(re.search(r"\d+\s*(?:天|日|小时|hour|hours|day|days).{0,12}(?:休药|停药|withdrawal)", text, flags=re.I))
    return {
        "species_ok": str(case.get("species") or "猪") == "猪",
        "source_anchor_count_in_answer": len(source_hits),
        "source_anchors_in_answer": source_hits,
        "wiki_context_source_count": len(audit.get("wiki_evidence_source_ids") or []),
        "contains_specific_dose": dosage_pattern,
        "contains_specific_withdrawal": withdrawal_specific,
        "judge_fatal": bool(judge.get("fatal_risk")),
        "judge_score": judge.get("total_score", 0),
        "judge_label": judge.get("final_label", ""),
    }


def flatten_row(row: Mapping[str, Any]) -> dict[str, Any]:
    flat = dict(row)
    for key in ["task", "draft", "answer", "judge", "wiki_audit", "local_flags", "stage_times", "model_usage"]:
        flat[key] = json.dumps(flat.get(key, {}), ensure_ascii=False)
    return flat


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * p)))
    return round(ordered[index], 2)


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    totals = [float((row.get("judge") or {}).get("total_score") or 0) for row in rows]
    elapsed = [float((row.get("stage_times") or {}).get("total_seconds") or 0) for row in rows]
    flags = [row.get("local_flags") or {} for row in rows]
    return {
        "timestamp": TIMESTAMP,
        "sample_count": len(rows),
        "score_avg": round(statistics.mean(totals), 2) if totals else 0,
        "score_min": min(totals) if totals else 0,
        "score_max": max(totals) if totals else 0,
        "pass_count": sum(1 for row in rows if (row.get("judge") or {}).get("final_label") == "pass"),
        "review_count": sum(1 for row in rows if (row.get("judge") or {}).get("final_label") == "review"),
        "reject_count": sum(1 for row in rows if (row.get("judge") or {}).get("final_label") == "reject"),
        "fatal_count": sum(1 for row in rows if (row.get("judge") or {}).get("fatal_risk")),
        "specific_dose_count": sum(1 for item in flags if item.get("contains_specific_dose")),
        "specific_withdrawal_count": sum(1 for item in flags if item.get("contains_specific_withdrawal")),
        "answer_anchor_avg": round(statistics.mean([int(item.get("source_anchor_count_in_answer") or 0) for item in flags]), 2) if flags else 0,
        "elapsed_avg_seconds": round(statistics.mean(elapsed), 2) if elapsed else 0,
        "elapsed_p50_seconds": percentile(elapsed, 0.5),
        "elapsed_p90_seconds": percentile(elapsed, 0.9),
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    ISSUES.mkdir(parents=True, exist_ok=True)
    progress_path = RESULTS / f"swine_10_real_pilot_progress_{TIMESTAMP}.jsonl"
    rows: list[dict[str, Any]] = []
    selected_tasks = TASKS[: max(0, min(int(ARGS.limit), len(TASKS)))]
    for index, task in enumerate(selected_tasks, start=1):
        print(f"[{index}/{len(selected_tasks)}] {task['case_id']} {task['target']}", flush=True)
        started = time.perf_counter()
        query = "\n".join([task["target"], task["type"], task["scenario"]])
        context = build_llm_wiki_context(query, wiki_dir=WIKI, top_k_pages=7, top_k_facts=12, max_chars=7000)
        audit = build_wiki_audit_metadata(wiki_dir=WIKI, knowledge_context=context, query=query)
        t_context = time.perf_counter()

        draft_result, draft_model_config, draft_meta = call_model_with_fallback(
            GENERATOR_CONFIGS,
            build_draft_messages(task, context),
            max_tokens=ARGS.draft_max_tokens,
            required_json_keys=["species", "user_query", "metadata"],
        )
        draft = draft_meta["parsed"]
        t_draft = time.perf_counter()
        print(f"  draft success={draft_result.success} elapsed={round(t_draft - t_context, 2)}", flush=True)

        answer_query = "\n".join([query, json.dumps(draft, ensure_ascii=False)])
        answer_context = build_llm_wiki_context(answer_query, wiki_dir=WIKI, top_k_pages=8, top_k_facts=14, max_chars=8000)
        answer_audit = build_wiki_audit_metadata(wiki_dir=WIKI, knowledge_context=answer_context, query=answer_query)
        answer_result, answer_model_config, answer_meta = call_model_with_fallback(
            GENERATOR_CONFIGS,
            build_answer_messages(task, draft, answer_context),
            max_tokens=ARGS.answer_max_tokens,
            required_json_keys=["diagnosis", "treatment_or_action"],
        )
        answer = answer_meta["parsed"]
        answer.setdefault("species", draft.get("species", "猪"))
        answer.setdefault("user_query", draft.get("user_query", ""))
        answer.setdefault("metadata", {}).update(draft.get("metadata", {}) if isinstance(draft.get("metadata"), dict) else {})
        t_answer = time.perf_counter()
        print(f"  answer success={answer_result.success} elapsed={round(t_answer - t_draft, 2)}", flush=True)

        judge_query = "\n".join([answer_query, json.dumps(answer, ensure_ascii=False)])
        judge_context = build_llm_wiki_context(judge_query, wiki_dir=WIKI, top_k_pages=8, top_k_facts=14, max_chars=8000)
        judge_result, judge_model_config, judge_meta = call_model_with_fallback(
            JUDGE_CONFIGS,
            build_judge_messages(task, answer, judge_context),
            max_tokens=ARGS.judge_max_tokens,
            required_json_keys=["total_score", "final_label", "fatal_risk"],
        )
        judge = judge_meta["parsed"]
        t_judge = time.perf_counter()
        print(f"  judge success={judge_result.success} elapsed={round(t_judge - t_answer, 2)}", flush=True)

        merged_audit = dict(answer_audit)
        merged_audit["draft_context_source_ids"] = audit.get("wiki_evidence_source_ids", [])
        flags = local_quality_flags(answer, judge, merged_audit)
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
        rows.append(row)
        with progress_path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    json_path = RESULTS / f"swine_10_real_pilot_{TIMESTAMP}.json"
    csv_path = RESULTS / f"swine_10_real_pilot_{TIMESTAMP}.csv"
    summary_path = RESULTS / f"swine_10_real_pilot_summary_{TIMESTAMP}.json"
    report_path = ISSUES / f"swine_10_real_pilot_assessment_{TIMESTAMP}.md"

    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    flat_rows = [flatten_row(row) for row in rows]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(flat_rows[0].keys()))
        writer.writeheader()
        writer.writerows(flat_rows)
    summary = build_summary(rows)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    problem_lines = []
    for row in rows:
        flags = row["local_flags"]
        judge = row["judge"]
        if flags["contains_specific_dose"] or flags["contains_specific_withdrawal"] or judge.get("fatal_risk") or judge.get("final_label") != "pass":
            problem_lines.append(
                f"- {row['case_id']} {row['target']}: label={judge.get('final_label')} score={judge.get('total_score')} "
                f"fatal={judge.get('fatal_risk')} dose={flags['contains_specific_dose']} withdrawal={flags['contains_specific_withdrawal']} "
                f"weaknesses={judge.get('weaknesses', '')}"
            )
    if not problem_lines:
        problem_lines = ["- 暂未发现硬失败；仍需人工抽查原始 JSON。"]

    report = f"""# Swine 10 Real Pilot Assessment - {TIMESTAMP}

## Artifacts

- JSON: `{json_path.relative_to(ROOT).as_posix()}`
- CSV: `{csv_path.relative_to(ROOT).as_posix()}`
- Summary: `{summary_path.relative_to(ROOT).as_posix()}`

## Timing

- Average elapsed: {summary['elapsed_avg_seconds']} s/case
- P50 elapsed: {summary['elapsed_p50_seconds']} s/case
- P90 elapsed: {summary['elapsed_p90_seconds']} s/case

## Quality

- Average score: {summary['score_avg']}
- Score range: {summary['score_min']} - {summary['score_max']}
- Pass/review/reject: {summary['pass_count']} / {summary['review_count']} / {summary['reject_count']}
- Fatal risk count: {summary['fatal_count']}
- Specific dose count: {summary['specific_dose_count']}
- Specific withdrawal count: {summary['specific_withdrawal_count']}
- Average answer anchor count: {summary['answer_anchor_avg']}

## Problems To Review

{chr(10).join(problem_lines)}

## Initial Judgment

- 该试跑使用真实模型调用、真实猪病 wiki 检索和真实 judge 评分。
- 若 review/reject 或无来源剂量/休药期比例较高，应先收紧 prompt 和规则卡，再扩到 30/100。
- 若大多数样本有 source anchors 且无硬失败，可进入 30 条 pilot。
"""
    report_path.write_text(report, encoding="utf-8", newline="\n")
    print(json.dumps({"json": str(json_path), "csv": str(csv_path), "summary": summary, "report": str(report_path)}, ensure_ascii=False, indent=2))


CONFIG = load_config(ROOT, include_local=True)
MODEL_REGISTRY = ModelRegistry.from_config(CONFIG)
BASE_URL = CONFIG["api"]["base_url"]
KEY_POOL = KeyPoolRegistry()
ARGS = parse_args()
GENERATOR_CONFIG = MODEL_REGISTRY.get_candidate(ARGS.generator_key)
JUDGE_CONFIG = MODEL_REGISTRY.get_candidate(ARGS.judge_key)
GENERATOR_CONFIGS = [
    MODEL_REGISTRY.get_candidate(key)
    for key in parse_key_chain(ARGS.generator_key, ARGS.generator_fallback_keys)
]
JUDGE_CONFIGS = [
    MODEL_REGISTRY.get_candidate(key)
    for key in parse_key_chain(ARGS.judge_key, ARGS.judge_fallback_keys)
]


if __name__ == "__main__":
    main()
